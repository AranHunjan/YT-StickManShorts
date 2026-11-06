#!/usr/bin/env python3
"""Audio check for an episode's voice track: does it sound like two people talking?

Nothing here can listen, so it measures what makes TTS sound broken or robotic:

  per line   transcript vs script (garbled, skipped or extra words), numbers heard,
             glitches (quality.py: buzz in a pause, wrong pitch, rough windows),
             pauses: where they fall (at punctuation or mid-phrase) and how long,
             loudness jumps between lines, clipping, pace, flat (monotone) delivery
  between    the silence between lines (turn gaps). People average about 0.2 s
             between turns in conversation (Stivers et al. 2009, PNAS, 10 languages);
             episode 001 was approved with 0.2-0.4 s of real silence between lines
  overall    total length: just over 1 minute (channel.json length, tools/episode/common.py)

Thresholds come from episode 001: its approved track has no FAIL here.
Run with the chatterbox environment (librosa, faster-whisper, praat-parselmouth).

Usage:
  python tools/voice/check_audio.py episodes/002 [--no-transcript]
Writes episodes/002/audio/audio_check.json. Exit code 1 when anything FAILs.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analyze import TARGETS, measure  # noqa: E402
import pauses  # noqa: E402
import quality  # noqa: E402

TAIL = 0.9  # seconds the video holds after the last line (Episode.tsx)
SHOWSAY = re.compile(r"\{([^|}]*)\|([^}]*)\}")
NUMWORDS = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
               "sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety "
               "hundred thousand million billion".split())
# Spellings Whisper picks at random, mapped to one form (applied to script and transcript alike).
SAME = {"ok": "okay", "alright": "allright", "two": "to", "too": "to", "four": "for"}
CONTRACTIONS = [(r"n't\b", " not"), (r"'s\b", " is"), (r"'re\b", " are"), (r"'ve\b", " have"),
                (r"'ll\b", " will"), (r"'m\b", " am"), (r"'d\b", " would")]
PUNCT_END = re.compile(r"(\.\.\.|…|[.,!?:;—-])[\"')\]]*$")

# Pause limits inside a line (seconds): at punctuation, and mid-phrase (no punctuation).
PAUSE_PUNCT = (0.8, 1.0)   # (warn above, fail above). speak.py caps pauses at 0.8 s
PAUSE_MID = (0.3, 0.5)     # episode 001 has mid-phrase breaths of 0.18-0.22 s
GAP = (0.1, 0.65, 0.85)    # between lines: warn below, warn above, fail above
LEVEL_DB = (4.0, 6.0)      # line loudness vs that speaker's median: warn, fail


def spoken(text):
    return SHOWSAY.sub(lambda m: m.group(2), re.sub(r"\[[a-z ]+\]\s*", "", text)).replace("*", "").strip()


def tokens(text):
    """Lower-case words for comparing script and transcript. Contractions are expanded on
    both sides ("number's" and "number is" both become "number is"), so either spelling matches."""
    text = text.lower().replace("—", " ").replace("-", " ").replace("’", "'")
    for pat, rep in CONTRACTIONS:
        text = re.sub(pat, rep, text)
    return [SAME.get(t, t) for t in (w.replace("'", "") for w in re.findall(r"[a-z0-9']+", text)) if t]


def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def contains(seq, sub):
    return any(seq[i:i + len(sub)] == sub for i in range(len(seq) - len(sub) + 1)) if sub else True


def transcript_flags(text, heard):
    """Compare what was heard with the script. Numbers are checked separately because
    Whisper writes them as digits or words at random."""
    flags = []
    words = lambda toks: [t for t in toks if t not in NUMWORDS and not any(c.isdigit() for c in t)]
    want, got = words(tokens(spoken(text))), words(tokens(heard))
    errors = edit_distance(want, got)
    import difflib
    sm = difflib.SequenceMatcher(None, want, got, autojunk=False)
    missing = [w for op, a0, a1, _, _ in sm.get_opcodes() if op in ("delete", "replace") for w in want[a0:a1]]
    extra = [w for op, _, _, b0, b1 in sm.get_opcodes() if op in ("insert", "replace") for w in got[b0:b1]]
    if errors:
        # Severity from letter errors, which shrug off Whisper's near-misses and word splits
        # ("ketchup say" heard as "catch up save" is 4 letters of 39). Garbled takes miss far more.
        a, b = "".join(want), "".join(got)
        letters = edit_distance(a, b)
        rate = letters / max(1, len(a))
        sev = "fail" if rate >= 0.2 and letters >= 4 else "warn"
        flags.append({"kind": "transcript", "severity": sev,
                      "detail": f"{errors} word error(s) ({rate:.0%} of letters): missing {missing or '-'}, heard instead/extra {extra or '-'}"})
    heard_all = tokens(heard)
    for show, say in SHOWSAY.findall(text):
        if not (contains(heard_all, tokens(show)) or contains(heard_all, tokens(say))):
            flags.append({"kind": "number", "severity": "warn", "detail": f"'{show}' ('{say}') not clearly heard"})
    for hi in re.findall(r"\*([^*]+)\*", SHOWSAY.sub(lambda m: m.group(2), text)):
        lost = [t for t in tokens(hi) if t not in NUMWORDS and t not in heard_all]
        if lost:
            flags.append({"kind": "keyword", "severity": "warn", "detail": f"highlighted word(s) {lost} not heard"})
    return errors, flags


def level(path):
    """(speech level dB, peak dBFS): level = mean of 10 ms frames within 30 dB of the peak."""
    a, sr = sf.read(str(path), dtype="float32")
    if a.ndim > 1:
        a = a.mean(axis=1)
    hop = int(sr * 0.01)
    n = len(a) // hop
    rms = np.sqrt(np.mean(a[: n * hop].reshape(n, hop) ** 2, axis=1))
    db = 20 * np.log10(np.maximum(rms, 1e-6))
    active = db[db > db.max() - 30]
    return round(float(10 * np.log10(np.mean(10 ** (active / 10)))), 1), round(float(20 * np.log10(max(np.abs(a).max(), 1e-6))), 1)


def classify_pauses(ln, info):
    """Attach each pause to the word it follows and say if it sits at punctuation.
    Whisper's word times drift by a few tenths of a second, so a pause belongs to the
    word gap it overlaps most; failing that, to the nearest word boundary."""
    words = [{**w, "s": w["s"] - ln["start"], "e": w["e"] - ln["start"]} for w in ln.get("words", [])]
    out = []
    for p0, p1 in info["pauses"]:
        best = None
        for i in range(len(words) - 1):
            g0, g1 = words[i]["e"], words[i + 1]["s"]
            overlap = min(p1, g1) - max(p0, g0)
            if overlap > 0 and (best is None or best[0] != "overlap" or overlap > best[1]):
                best = ("overlap", overlap, i)
        if best is None:
            mid = (p0 + p1) / 2
            near = [(abs((words[i]["e"] + words[i + 1]["s"]) / 2 - mid), i) for i in range(len(words) - 1)]
            d, i = min(near, default=(None, None))
            best = ("near", d, i) if d is not None and d < 0.9 else None
        after = words[best[2]]["w"] if best else None
        kind = "unknown" if after is None else ("punct" if PUNCT_END.search(after) else "mid")
        out.append({"t": round(p0, 2), "len": round(p1 - p0, 2), "after": after, "kind": kind})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode", help="episode folder, e.g. episodes/002")
    ap.add_argument("--no-transcript", action="store_true", help="skip the Whisper transcript check")
    ap.add_argument("--model", default="base.en")
    args = ap.parse_args()
    ep = Path(args.episode)
    audio = ep / "audio"
    script = {ln["id"]: ln for ln in json.loads((ep / "script.json").read_text(encoding="utf-8"))["lines"]}
    timing = json.loads((audio / "timing.json").read_text())

    whisper = None
    if not args.no_transcript:
        try:
            from faster_whisper import WhisperModel
            import torch
            dev = "cuda" if torch.cuda.is_available() else "cpu"
            whisper = WhisperModel(args.model, device=dev, compute_type="float16" if dev == "cuda" else "int8")
        except ImportError:
            print("faster-whisper not installed: transcript check skipped")

    lines = []
    for ln in timing["lines"]:
        wav = audio / "lines" / f"{ln['id']}.wav"
        spk, text = ln["speaker"], script[ln["id"]]["text"]
        m = measure(wav, spoken(text))
        q = quality.check(wav, spk)
        info = pauses.analyze(wav)
        lvl, peak = level(wav)
        flags = list(q["flags"])
        row = {"id": ln["id"], "speaker": spk, "delivery": ln["delivery"], "text": text,
               "dur": m["dur_s"], "wpm": m.get("wpm"), "pitch_hz": q["median_f0"], "range_st": m["range_st"],
               "level_db": lvl, "peak_dbfs": peak, "edge": [info["lead"], info["tail"]]}
        if m["bad"]:
            flags.append({"kind": "bad_take", "severity": "fail", "detail": f"mostly unvoiced ({m['voiced']}): whispered or garbled"})
        if peak > -0.3:
            flags.append({"kind": "clipping", "severity": "fail", "detail": f"peak {peak} dBFS: the line is clipped"})
        row["pauses"] = classify_pauses(ln, info)
        for p in row["pauses"]:
            warn, fail = PAUSE_MID if p["kind"] == "mid" else PAUSE_PUNCT
            where = f"after '{p['after']}'" if p["after"] else f"at {p['t']} s"
            if p["len"] > warn:
                flags.append({"kind": "pause", "severity": "fail" if p["len"] > fail else "warn", "t": p["t"],
                              "detail": f"{p['len']:.2f} s pause {where}" + (" in the middle of a phrase" if p["kind"] == "mid" else "")})
        for w in ln.get("words", [])[:-1]:
            if w["w"].endswith(("...", "…")) and not any(p["after"] == w["w"] for p in row["pauses"]):
                flags.append({"kind": "rushed", "severity": "info", "detail": f"no audible pause at '{w['w']}'"})
        n_words = len(tokens(spoken(text)))
        lo, hi = TARGETS[spk]["wpm"]
        if m.get("wpm") and n_words >= 6 and not lo * 0.85 <= m["wpm"] <= hi * 1.15:
            flags.append({"kind": "pace", "severity": "warn", "detail": f"{m['wpm']} wpm, {spk}'s band is {lo}-{hi}"})
        if m["range_st"] is not None and n_words >= 5 and m["range_st"] < 3.0:
            flags.append({"kind": "flat", "severity": "warn", "detail": f"pitch range only {m['range_st']} semitones: may sound robotic"})
        if whisper:
            segs, _ = whisper.transcribe(str(wav), language="en", beam_size=5, condition_on_previous_text=False)
            row["heard"] = " ".join(s.text.strip() for s in segs).strip()
            row["word_errors"], tflags = transcript_flags(text, row["heard"])
            flags += tflags
        row["flags"] = flags
        lines.append(row)

    # Loudness jumps: compare each line with that speaker's median level.
    for spk in {r["speaker"] for r in lines}:
        med = float(np.median([r["level_db"] for r in lines if r["speaker"] == spk]))
        for r in (r for r in lines if r["speaker"] == spk):
            d = r["level_db"] - med
            if abs(d) > LEVEL_DB[0]:
                r["flags"].append({"kind": "level", "severity": "fail" if abs(d) > LEVEL_DB[1] else "warn",
                                   "detail": f"{abs(d):.1f} dB {'louder' if d > 0 else 'quieter'} than {spk}'s other lines"})

    # Silence between lines = trailing quiet of one line + the gap + leading quiet of the next.
    gaps = []
    for a, b, ra, rb in zip(timing["lines"], timing["lines"][1:], lines, lines[1:]):
        silence = round(ra["edge"][1] + (b["start"] - a["end"]) + rb["edge"][0], 2)
        g = {"between": f"{a['id']}-{b['id']}", "silence": silence, "same_speaker": a["speaker"] == b["speaker"], "flags": []}
        if silence > GAP[2]:
            g["flags"].append({"kind": "gap", "severity": "fail", "detail": f"{silence:.2f} s of dead air"})
        elif silence > GAP[1]:
            g["flags"].append({"kind": "gap", "severity": "warn", "detail": f"{silence:.2f} s: a long beat; fine only before a reveal"})
        elif silence < GAP[0]:
            g["flags"].append({"kind": "gap", "severity": "warn", "detail": f"{silence:.2f} s: lines run into each other"})
        gaps.append(g)

    overall = []
    sys.path.insert(0, str(HERE.parent / "episode"))
    from common import end_hold, length_problems  # channel.json's length window (tools/episode/common.py)
    total = timing["duration"] + end_hold(ep.name, timing["duration"])
    problem = length_problems(ep.name, timing["duration"])
    if problem:
        overall.append({"kind": "length", "severity": problem[0], "detail": problem[1]})
    pitch = {s: float(np.median([r["pitch_hz"] for r in lines if r["speaker"] == s and r["pitch_hz"]])) for s in {r["speaker"] for r in lines}}
    if len(pitch) == 2:
        a, b = sorted(pitch.values())
        contrast = 12 * np.log2(b / a)
        if contrast < 1.5:
            overall.append({"kind": "contrast", "severity": "warn", "detail": f"Kip and Dex are only {contrast:.1f} semitones apart"})

    every = [f for r in lines for f in r["flags"]] + [f for g in gaps for f in g["flags"]] + overall
    verdict = "fail" if any(f["severity"] == "fail" for f in every) else "warn" if any(f["severity"] == "warn" for f in every) else "pass"
    import hashlib
    voice_sha1 = hashlib.sha1((audio / "voice.wav").read_bytes()).hexdigest() if (audio / "voice.wav").exists() else None
    result = {"episode": ep.name, "verdict": verdict, "voice_sha1": voice_sha1,
              "duration_with_hold": round(total, 2), "median_pitch": pitch,
              "praat": quality.praat_available(), "transcript": bool(whisper),
              "overall": overall, "lines": lines, "gaps": gaps}
    (audio / "audio_check.json").write_text(json.dumps(result, indent=2))

    print(f"audio check {ep.name}: {verdict.upper()}  ({total:.1f} s with the end hold)")
    for r in lines:
        marks = [f"{f['severity'].upper()} {f['kind']}: {f['detail']}" for f in r["flags"] if f["severity"] != "info"]
        print(f"  {r['id']} {r['speaker']:3} {r['dur']:5.2f}s {str(r['wpm']):>4} wpm {str(r['pitch_hz']):>6} Hz"
              f" {r['level_db']:6.1f} dB  {'ok' if not marks else ' | '.join(marks)}")
    for g in gaps:
        for f in g["flags"]:
            print(f"  gap {g['between']}: {f['severity'].upper()} {f['detail']}")
    for f in overall:
        print(f"  {f['severity'].upper()} {f['kind']}: {f['detail']}")
    if not result["praat"]:
        print("  note: praat-parselmouth missing, rough-window checks skipped")
    print(f"report: {audio / 'audio_check.json'}")
    sys.exit(1 if verdict == "fail" else 0)


if __name__ == "__main__":
    main()
