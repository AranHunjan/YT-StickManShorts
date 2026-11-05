#!/usr/bin/env python3
"""Word-level timing for captions: transcribes each line WAV with faster-whisper
(word timestamps), then maps the SCRIPT's words onto those times, so captions
show exactly what is being said, when it is said. Adds a "words" list to every
line in timing.json:  {"w": "Hey", "s": 0.41, "e": 0.62, "hi": false}
Words wrapped in *stars* in the script are marked hi (highlighter).

Usage:
  python words.py --script episodes/002/script.json --audio episodes/002/audio [--model base.en]
"""
import argparse
import difflib
import json
import re
from pathlib import Path

TOKEN = re.compile(r"\S+")
NORM = re.compile(r"[^a-z0-9']")


def norm(w):
    return NORM.sub("", w.lower())


def script_words(text):
    """Display tokens with highlight flags; [tags] removed, *spans* marked."""
    text = re.sub(r"\[[a-z ]+\]\s*", "", text)
    text = re.sub(r"\{([^|}]*)\|([^}]*)\}", lambda m: m.group(1), text)  # {show|say} -> show
    out, on = [], False
    for tok in TOKEN.findall(text):
        hi = on
        if tok.startswith("*"):
            tok, hi, on = tok[1:], True, True
        if tok.endswith("*") or tok.rstrip(".,!?…\"'").endswith("*"):
            tok = tok.replace("*", "")
            on = False
        out.append({"w": tok.replace("*", ""), "hi": hi})
    return out


def align(display, heard):
    """Give every display word a start/end from the heard words (difflib match,
    interpolating any word that wasn't matched)."""
    a = [norm(d["w"]) for d in display]
    b = [norm(h["w"]) for h in heard]
    times = [None] * len(display)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            h = heard[blk.b + k]
            times[blk.a + k] = (h["s"], h["e"])
    # interpolate gaps
    n = len(display)
    t0 = heard[0]["s"] if heard else 0.0
    t1 = heard[-1]["e"] if heard else 0.0
    i = 0
    while i < n:
        if times[i] is not None:
            i += 1
            continue
        j = i
        while j < n and times[j] is None:
            j += 1
        left = times[i - 1][1] if i > 0 else t0
        right = times[j][0] if j < n else t1
        step = (right - left) / (j - i)
        for k in range(i, j):
            times[k] = (left + step * (k - i), left + step * (k - i + 1))
        i = j
    return [{**d, "s": round(s, 3), "e": round(e, 3)} for d, (s, e) in zip(display, times)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--model", default="base.en")
    ap.add_argument("--device", default="auto")
    args = ap.parse_args()
    from faster_whisper import WhisperModel

    audio = Path(args.audio)
    script = {ln["id"]: ln for ln in json.loads(Path(args.script).read_text(encoding="utf-8"))["lines"]}
    timing_path = audio / "timing.json"
    timing = json.loads(timing_path.read_text())
    device = args.device
    if device == "auto":
        try:
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            device = "cpu"
    model = WhisperModel(args.model, device=device, compute_type="float16" if device == "cuda" else "int8")

    for ln in timing["lines"]:
        display = script_words(script[ln["id"]]["text"])
        segs, _ = model.transcribe(str(audio / "lines" / f"{ln['id']}.wav"), word_timestamps=True,
                                   initial_prompt=re.sub(r"\{([^|}]*)\|([^}]*)\}", lambda m: m.group(2), re.sub(r"[*\[\]]", "", script[ln["id"]]["text"])), language="en")
        heard = [{"w": w.word.strip(), "s": w.start, "e": w.end} for s in segs for w in (s.words or [])]
        words = align(display, heard)
        ln["words"] = [{**w, "s": round(ln["start"] + w["s"], 3), "e": round(ln["start"] + w["e"], 3)} for w in words]
        matched = sum(1 for d in display if norm(d["w"]) in {norm(h["w"]) for h in heard})
        print(f"{ln['id']}: {len(display)} words, {matched} matched by ear")
    timing_path.write_text(json.dumps(timing, indent=2))
    print(f"word timings added to {timing_path}")


if __name__ == "__main__":
    main()
