#!/usr/bin/env python3
"""Pace normalization: time-stretch each line (pitch unchanged) so the speaker's
words per minute land inside their target band from docs/VOICE.md. Generation
pace is random, so this makes it consistent. Stretch is capped at +/-15% to stay
natural. Run with the chatterbox environment (needs librosa) and ffmpeg on PATH.

Usage:
  python pace.py --dir out/voice-bakeoff/chatterbox-final [--out DIR]

Writes adjusted WAVs to <dir>-paced (or --out) and prints what changed.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analyze import TARGETS, measure  # noqa: E402

MAX_STRETCH = 0.15


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()
    src = Path(args.dir)
    dst = Path(args.out) if args.out else src.with_name(src.name + "-paced")
    dst.mkdir(parents=True, exist_ok=True)
    lines = {ln["id"]: ln for ln in json.loads((HERE / "lines.json").read_text(encoding="utf-8"))["lines"]}

    for f in sorted(src.glob("*.wav")):
        ln = lines.get(f.stem)
        if not ln:
            continue
        lo, hi = TARGETS[ln["speaker"]]["wpm"]
        wpm = measure(f, ln["text"])["wpm"]
        tempo = 1.0
        if wpm and wpm > hi:
            tempo = max(hi / wpm, 1 - MAX_STRETCH)
        elif wpm and wpm < lo:
            tempo = min(lo / wpm, 1 + MAX_STRETCH)
        out = dst / f.name
        if abs(tempo - 1) < 0.01:
            out.write_bytes(f.read_bytes())
        else:
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(f),
                            "-af", f"rubberband=tempo={tempo:.4f}:formant=preserved", str(out)], check=True)
        print(f"{f.stem:16} {ln['speaker']:4} {wpm:>4} wpm -> tempo {tempo:.2f} -> ~{round(wpm * tempo)} wpm")


if __name__ == "__main__":
    main()
