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


def pace_tempo(speaker, wpm):
    """Tempo factor that moves `wpm` into the speaker's band (1.0 = unchanged)."""
    lo, hi = TARGETS[speaker]["wpm"]
    if wpm and wpm > hi:
        return max(hi / wpm, 1 - MAX_STRETCH)
    if wpm and wpm < lo:
        return min(lo / wpm, 1 + MAX_STRETCH)
    return 1.0


def stretch(src, dst, tempo):
    """Time-stretch with pitch and formants preserved (ffmpeg rubberband)."""
    if abs(tempo - 1) < 0.01:
        Path(dst).write_bytes(Path(src).read_bytes())
        return
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
                    "-af", f"rubberband=tempo={tempo:.4f}:formant=preserved", str(dst)], check=True)


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
        wpm = measure(f, ln["text"])["wpm"]
        tempo = pace_tempo(ln["speaker"], wpm)
        stretch(f, dst / f.name, tempo)
        print(f"{f.stem:16} {ln['speaker']:4} {wpm:>4} wpm -> tempo {tempo:.2f} -> ~{round(wpm * tempo)} wpm")


if __name__ == "__main__":
    main()
