#!/usr/bin/env python3
"""Production voice track for an episode, following the rule in docs/VOICE.md:

  for every line: generate N takes in the channel voices (Chatterbox clones
  assets/voices/<speaker>.wav; Qwen speaks preset voices, see voices.json)
  -> drop bad takes (whispered/garbled, or a glitch from quality.py)
  -> keep the take closest to the character's targets -> pace-normalize
  -> trim silence -> cap overlong pauses inside the line
  then: join all lines with short gaps -> voice.wav + timing.json (+ word timings)

timing.json gives every line's start/end in seconds; the animation syncs to it.
Run with the chatterbox environment (needs librosa and ffmpeg on PATH).

Per-line options in script.json (all optional):
  "pause_before": 0.45   silence before this line, in seconds (default --gap; --lead for line 1)
  "max_pause": 0.5       longest pause allowed inside the line (default 0.8 s)

Usage:
  python speak.py --script episodes/002/script.json --out episodes/002/audio
      [--takes 3] [--gap 0.16] [--lead 0.30] [--device auto]
  ... --only L03,L07 --fresh   new takes for those lines (new seeds), picked only among the new ones
  ... --resume                 only lines that have no finished WAV yet (after a timeout)
  ... --assemble               no generation: re-join the existing lines (after changing pauses)
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))
from analyze import measure, score  # noqa: E402
from pace import pace_tempo, stretch  # noqa: E402
import pauses  # noqa: E402
import quality  # noqa: E402

TAG = re.compile(r"\[[a-z ]+\]\s*")
SR = 24000
SHOWSAY = re.compile(r"\{([^|}]*)\|([^}]*)\}")
TAKE_NO = re.compile(r"_[qt](\d+)\.wav$")
MAX_PAUSE = 0.8  # approved episode 001 lines pause up to 0.78 s; longer reads as dead air


def spoken(text):
    """What the voice reads: [tags] and *highlight* stars removed, {show|say} -> say."""
    return SHOWSAY.sub(lambda m: m.group(2), TAG.sub("", text)).replace("*", "").strip()


def take_no(path):
    m = TAKE_NO.search(path.name)
    return int(m.group(1)) if m else 0


def trim(src, dst):
    """Remove leading/trailing silence so line timing is tight and predictable."""
    flt = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,areverse,"
           "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
                    "-af", flt, "-ar", str(SR), "-ac", "1", str(dst)], check=True)


def judge(take, spk, text):
    """Measure a take. Score -1 means unusable (bad take or a glitch)."""
    m = measure(take, text)
    q = quality.check(take, spk)
    m["glitches"] = [f["detail"] for f in q["flags"] if f["severity"] == "fail"]
    m["warnings"] = [f["detail"] for f in q["flags"] if f["severity"] == "warn"]
    m["median_f0"] = q["median_f0"]
    s = -1 if (m["bad"] or q["fail"]) else score(spk, m)
    return s, m


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--refs", default=str(ROOT / "assets" / "voices"))
    ap.add_argument("--takes", type=int, default=3)
    ap.add_argument("--gap", type=float, default=0.16, help="silence between lines (s); a line's pause_before overrides it")
    ap.add_argument("--lead", type=float, default=0.30, help="silence before the first line (s)")
    ap.add_argument("--device", default="auto")
    ap.add_argument("--only", help="regenerate only these line ids (comma-separated); others reuse their chosen take")
    ap.add_argument("--fresh", action="store_true", help="with --only: make new takes (new seeds) and pick only among them")
    ap.add_argument("--resume", action="store_true", help="only generate lines that have no finished line WAV yet")
    ap.add_argument("--assemble", action="store_true", help="skip generation and re-join the existing line WAVs")
    ap.add_argument("--qwen-takes", type=int, help="takes per line for qwen-custom voices (default: --takes)")
    args = ap.parse_args()
    if args.fresh and not args.only:
        sys.exit("--fresh needs --only (which lines to re-take)")

    import numpy as np
    import soundfile as sf

    script = json.loads(Path(args.script).read_text(encoding="utf-8"))
    deliveries = json.loads((HERE / "lines.json").read_text(encoding="utf-8"))["delivery"]
    out = Path(args.out)
    (out / "takes").mkdir(parents=True, exist_ok=True)
    (out / "lines").mkdir(parents=True, exist_ok=True)
    only = set(args.only.split(",")) if args.only else (set() if args.resume else None)
    unknown = (only or set()) - {ln["id"] for ln in script["lines"]}
    if unknown:
        sys.exit(f"unknown line ids: {sorted(unknown)}")
    missing_delivery = sorted({ln["delivery"] for ln in script["lines"]} - set(deliveries))
    if missing_delivery:
        sys.exit(f"deliveries not defined in tools/voice/lines.json: {missing_delivery}")

    voices = json.loads((Path(args.refs) / "voices.json").read_text(encoding="utf-8"))
    engine = lambda spk: voices.get(spk, {}).get("engine", "chatterbox")
    todo = [] if args.assemble else [
        ln for ln in script["lines"]
        if not (only is not None and ln["id"] not in only and (out / "lines" / f"{ln['id']}.wav").exists())]
    report = []
    t_start = time.time()

    if todo:
        import torch
        device = args.device
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        if not quality.praat_available():
            print("note: praat-parselmouth not installed, so takes are not checked for rough windows")

    # Qwen preset voices run in their own environment: generate their takes up front, in batches.
    import envs  # noqa: E402  (tools/envs.py: finds the environment in a worktree too)
    qwen_python = os.environ.get("QWEN_PYTHON") or str(envs.python("qwen") or HERE / ".venvs" / "qwen" / envs.VENV_PY)
    qtakes = args.qwen_takes or args.takes
    first_take = {}  # line id -> lowest take number that may be picked (--fresh skips older takes)

    def qwen_generate(spk, ids, start, n):
        v = voices[spk]
        subprocess.run([qwen_python, str(HERE / "qwen_voice.py"), "--script", args.script, "--out", str(out),
                        "--ids", ",".join(ids), "--speaker", v["speaker"], "--persona", v.get("persona", ""),
                        "--takes", str(n), "--start", str(start), "--device", args.device], check=True)

    def qwen_takes(lid):
        return [p for p in sorted((out / "takes").glob(f"{lid}_q*.wav"), key=take_no) if take_no(p) >= first_take[lid]]

    for spk in sorted({ln["speaker"] for ln in todo if engine(ln["speaker"]) == "qwen-custom"}):
        ids = [ln["id"] for ln in todo if ln["speaker"] == spk]
        if args.fresh:
            # Qwen seeds are 1000 + take number, so new numbers mean new audio.
            start = 1 + max([take_no(p) for i in ids for p in (out / "takes").glob(f"{i}_q*.wav")] or [0])
            first_take.update({i: start for i in ids})
            qwen_generate(spk, ids, start, qtakes)
        else:
            first_take.update({i: 1 for i in ids})
            need = [i for i in ids if not qwen_takes(i)]
            if need:
                qwen_generate(spk, need, 1, qtakes)

    model = None
    for ln in todo:
        final = out / "lines" / f"{ln['id']}.wav"
        spk, text = ln["speaker"], spoken(ln["text"])
        d = deliveries[ln["delivery"]]
        best = None
        if engine(spk) == "qwen-custom":
            for _ in range(3):  # up to 2 extra rounds if every take is bad
                for take in qwen_takes(ln["id"]):
                    s, m = judge(take, spk, text)
                    print(f"{ln['id']} {take.name}: {'BAD ' + '; '.join(m['glitches']) if s < 0 else s}", flush=True)
                    if best is None or s > best[0]:
                        best = (s, take, m)
                if best and best[0] >= 0:
                    break
                n = 1 + max([take_no(p) for p in (out / "takes").glob(f"{ln['id']}_q*.wav")] or [0])
                qwen_generate(spk, [ln["id"]], n, 1)
            print(f"{ln['id']} ({voices[spk]['speaker']}): best {best[0]} {best[1].name}", flush=True)
        else:
            if model is None:
                from chatterbox.tts import ChatterboxTTS
                model = ChatterboxTTS.from_pretrained(device=device)
            ref = Path(args.refs) / voices.get(spk, {}).get("ref", f"{spk}.wav")
            first = 1
            if args.fresh:
                first = 1 + max([take_no(p) for p in (out / "takes").glob(f"{ln['id']}_t*.wav")] or [0])
            n = first - 1
            while n < first - 1 + args.takes + 2:  # up to 2 extra tries if every take is bad
                n += 1
                torch.manual_seed(zlib.crc32(f"{ln['id']}-{n}".encode()))
                wav = model.generate(text, audio_prompt_path=str(ref), exaggeration=d["exaggeration"], cfg_weight=d["cfg_weight"])
                take = out / "takes" / f"{ln['id']}_t{n}.wav"
                sf.write(str(take), wav.squeeze(0).cpu().numpy(), model.sr)
                s, m = judge(take, spk, text)
                print(f"{ln['id']} take {n}: {'BAD ' + '; '.join(m['glitches']) if s < 0 else s} {m}", flush=True)
                if best is None or s > best[0]:
                    best = (s, take, m)
                if n - first + 1 >= args.takes and best[0] >= 0:
                    break
        s, take, m = best
        if s < 0:
            print(f"WARNING {ln['id']}: every take failed the checks; keeping the least bad one ({take.name})", flush=True)
        tempo = pace_tempo(spk, m.get("wpm"))
        if tempo > 1 and ("..." in ln["text"] or "…" in ln["text"]):
            tempo = 1.0  # a dramatic "..." reads as slow; speeding it up adds artefacts (episode 001)
        paced = out / "takes" / f"{ln['id']}_paced.wav"
        stretch(take, paced, tempo)
        trim(paced, final)
        capped = pauses.cap(final, ln.get("max_pause", MAX_PAUSE))
        report.append({"id": ln["id"], "speaker": spk, "take": take.name, "score": s, "tempo": round(tempo, 3),
                       **({"capped_pauses": capped} if capped else {}), **m})

    if args.assemble:
        for ln in script["lines"]:
            if "max_pause" in ln:
                for s0, old, new in pauses.cap(out / "lines" / f"{ln['id']}.wav", ln["max_pause"]):
                    print(f"{ln['id']}: pause at {s0:.2f} s shortened {old:.2f} -> {new:.2f} s")

    # Assemble the voice track and timing.
    missing = [ln["id"] for ln in script["lines"] if not (out / "lines" / f"{ln['id']}.wav").exists()]
    if missing:
        sys.exit(f"no finished WAV for {missing}: run without --assemble (or with --resume)")
    parts, timing, t = [], [], 0.0
    for i, ln in enumerate(script["lines"]):
        pause = ln.get("pause_before", args.lead if i == 0 else args.gap)
        parts.append(np.zeros(int(SR * pause), dtype="float32"))
        t += pause
        a, sr = sf.read(str(out / "lines" / f"{ln['id']}.wav"), dtype="float32")
        assert sr == SR, (ln["id"], sr)
        if a.ndim > 1:
            a = a.mean(axis=1)
        dur = len(a) / SR
        timing.append({"id": ln["id"], "speaker": ln["speaker"], "delivery": ln["delivery"],
                       "start": round(t, 3), "end": round(t + dur, 3),
                       "text": ln["text"], "caption": ln.get("caption", "")})
        parts.append(a)
        t += dur
    parts.append(np.zeros(int(SR * args.gap), dtype="float32"))
    voice = np.concatenate(parts)
    sf.write(str(out / "voice.wav"), voice, SR)
    (out / "timing.json").write_text(json.dumps({"duration": round(len(voice) / SR, 3), "lines": timing}, indent=2))
    if report:  # merge into the existing report, so --only runs keep the other lines' entries
        path = out / "takes_report.json"
        old = {r["id"]: r for r in json.loads(path.read_text())} if path.exists() else {}
        old.update({r["id"]: r for r in report})
        order = [ln["id"] for ln in script["lines"]]
        path.write_text(json.dumps([old[i] for i in order if i in old], indent=2))
    print(f"voice.wav {len(voice) / SR:.2f}s, {len(timing)} lines, generated in {time.time() - t_start:.0f}s")
    # Word-level timing for captions (needs faster-whisper; falls back to line timing without it).
    try:
        import faster_whisper  # noqa: F401
        subprocess.run([sys.executable, str(HERE / "words.py"), "--script", args.script, "--audio", str(out)], check=True)
    except ImportError:
        print("faster-whisper not installed: captions will use line timing")


if __name__ == "__main__":
    main()
