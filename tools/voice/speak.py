#!/usr/bin/env python3
"""Production voice track for an episode, following the rule in docs/VOICE.md:

  for every line: generate N takes with Chatterbox in the channel voices
  (assets/voices/<speaker>.wav) -> drop bad takes (whispered/garbled) -> keep the
  take closest to the character's targets -> pace-normalize -> trim silence
  then: join all lines with short gaps -> voice.wav + timing.json

timing.json gives every line's start/end in seconds; the animation syncs to it.
Run with the chatterbox environment (needs librosa and ffmpeg on PATH).

Usage:
  python speak.py --script episodes/001/script.json --out episodes/001/audio
      [--takes 3] [--refs assets/voices] [--gap 0.28] [--lead 0.35] [--device auto]
"""
import argparse
import json
import subprocess
import sys
import time
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
from analyze import measure, score  # noqa: E402
from pace import pace_tempo, stretch  # noqa: E402

TAG = __import__("re").compile(r"\[[a-z ]+\]\s*")
SR = 24000
SHOWSAY = __import__("re").compile(r"\{([^|}]*)\|([^}]*)\}")


def spoken(text):
    """What the voice reads: [tags] and *highlight* stars removed, {show|say} -> say."""
    return SHOWSAY.sub(lambda m: m.group(2), TAG.sub("", text)).replace("*", "").strip()


def trim(src, dst):
    """Remove leading/trailing silence so line timing is tight and predictable."""
    flt = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,areverse,"
           "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
                    "-af", flt, "-ar", str(SR), "-ac", "1", str(dst)], check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--refs", default=str(ROOT / "assets" / "voices"))
    ap.add_argument("--takes", type=int, default=3)
    ap.add_argument("--gap", type=float, default=0.28, help="silence between lines (s)")
    ap.add_argument("--lead", type=float, default=0.35, help="silence before the first line (s)")
    ap.add_argument("--device", default="auto")
    ap.add_argument("--only", help="regenerate only these line ids (comma-separated); others reuse their chosen take")
    ap.add_argument("--qwen-takes", type=int, help="takes per line for qwen-custom voices (default: --takes)")
    args = ap.parse_args()

    import os
    import numpy as np
    import soundfile as sf
    import torch

    script = json.loads(Path(args.script).read_text(encoding="utf-8"))
    deliveries = json.loads((HERE / "lines.json").read_text(encoding="utf-8"))["delivery"]
    out = Path(args.out)
    (out / "takes").mkdir(parents=True, exist_ok=True)
    (out / "lines").mkdir(parents=True, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None

    device = args.device
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    voices = json.loads((Path(args.refs) / "voices.json").read_text(encoding="utf-8"))
    engine = lambda spk: voices.get(spk, {}).get("engine", "chatterbox")
    todo = [ln for ln in script["lines"]
            if not (only is not None and ln["id"] not in only and (out / "lines" / f"{ln['id']}.wav").exists())]
    report = []
    t_start = time.time()

    # Qwen preset voices run in their own environment: generate their takes up front, in batches.
    qwen_python = os.environ.get("QWEN_PYTHON") or str(HERE / ".venvs" / "qwen" / ("Scripts/python.exe" if os.name == "nt" else "bin/python"))
    qtakes = args.qwen_takes or args.takes

    def qwen_generate(spk, ids, start):
        v = voices[spk]
        subprocess.run([qwen_python, str(HERE / "qwen_voice.py"), "--script", args.script, "--out", str(out),
                        "--ids", ",".join(ids), "--speaker", v["speaker"], "--persona", v.get("persona", ""),
                        "--takes", str(qtakes if start == 1 else 1), "--start", str(start), "--device", args.device], check=True)

    for spk in {ln["speaker"] for ln in todo if engine(ln["speaker"]) == "qwen-custom"}:
        missing = [ln["id"] for ln in todo if ln["speaker"] == spk and not list((out / "takes").glob(f"{ln['id']}_q*.wav"))]
        if missing:
            qwen_generate(spk, missing, 1)

    model = None
    for ln in todo:
        final = out / "lines" / f"{ln['id']}.wav"
        spk, text = ln["speaker"], spoken(ln["text"])
        d = deliveries[ln["delivery"]]
        best = None
        if engine(spk) == "qwen-custom":
            for extra in range(3):  # up to 2 extra rounds if every take is bad
                for take in sorted((out / "takes").glob(f"{ln['id']}_q*.wav")):
                    m = measure(take, text)
                    s = score(spk, m) if not m["bad"] else -1
                    if best is None or s > best[0]:
                        best = (s, take, m)
                if best and best[0] >= 0:
                    break
                n = len(list((out / "takes").glob(f"{ln['id']}_q*.wav")))
                qwen_generate(spk, [ln["id"]], n + 1)
            print(f"{ln['id']} ({voices[spk]['speaker']}): best {best[0]} {best[1].name}", flush=True)
        if model is None and engine(spk) == "chatterbox":
            from chatterbox.tts import ChatterboxTTS
            model = ChatterboxTTS.from_pretrained(device=device)
        ref = Path(args.refs) / voices.get(spk, {}).get("ref", f"{spk}.wav")
        attempts = 0
        while engine(spk) == "chatterbox" and attempts < args.takes + 2:  # up to 2 extra tries if every take is bad
            attempts += 1
            torch.manual_seed(zlib.crc32(f"{ln['id']}-{attempts}".encode()))
            wav = model.generate(text, audio_prompt_path=str(ref), exaggeration=d["exaggeration"], cfg_weight=d["cfg_weight"])
            take = out / "takes" / f"{ln['id']}_t{attempts}.wav"
            sf.write(str(take), wav.squeeze(0).cpu().numpy(), model.sr)
            m = measure(take, text)
            s = score(spk, m) if not m["bad"] else -1
            print(f"{ln['id']} take {attempts}: {'BAD' if m['bad'] else s} {m}", flush=True)
            if best is None or s > best[0]:
                best = (s, take, m)
            if attempts >= args.takes and best[0] >= 0:
                break
        s, take, m = best
        tempo = pace_tempo(spk, m.get("wpm"))
        paced = out / "takes" / f"{ln['id']}_paced.wav"
        stretch(take, paced, tempo)
        trim(paced, final)
        report.append({"id": ln["id"], "speaker": spk, "take": take.name, "score": s, "tempo": round(tempo, 3), **m})

    # Assemble the voice track and timing.
    parts = [np.zeros(int(SR * args.lead), dtype="float32")]
    timing, t = [], args.lead
    for ln in script["lines"]:
        a, sr = sf.read(str(out / "lines" / f"{ln['id']}.wav"), dtype="float32")
        assert sr == SR, (ln["id"], sr)
        if a.ndim > 1:
            a = a.mean(axis=1)
        dur = len(a) / SR
        timing.append({"id": ln["id"], "speaker": ln["speaker"], "delivery": ln["delivery"],
                       "start": round(t, 3), "end": round(t + dur, 3),
                       "text": ln["text"], "caption": ln.get("caption", "")})
        parts += [a, np.zeros(int(SR * args.gap), dtype="float32")]
        t += dur + args.gap
    voice = np.concatenate(parts)
    sf.write(str(out / "voice.wav"), voice, SR)
    (out / "timing.json").write_text(json.dumps({"duration": round(len(voice) / SR, 3), "lines": timing}, indent=2))
    if report:
        (out / "takes_report.json").write_text(json.dumps(report, indent=2))
    print(f"voice.wav {len(voice) / SR:.2f}s, {len(timing)} lines, generated in {time.time() - t_start:.0f}s")
    # Word-level timing for captions (needs faster-whisper; falls back to line timing without it).
    try:
        import faster_whisper  # noqa: F401
        subprocess.run([sys.executable, str(HERE / "words.py"), "--script", args.script, "--audio", str(out)], check=True)
    except ImportError:
        print("faster-whisper not installed: captions will use line timing")


if __name__ == "__main__":
    main()
