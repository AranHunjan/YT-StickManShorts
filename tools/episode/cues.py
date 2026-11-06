#!/usr/bin/env python3
"""Turn an episode's beat-sheet sound cues ("L05@0.45") into absolute times for
the mixer, using the voice timing. Standard library only.

Usage:
  python tools/episode/cues.py episodes/001
  -> writes episodes/001/audio/sfx_cues.json (input for mix_audio.py --sfx)
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAIL = 0.9  # must match TAIL in packages/animator/src/episodes/Episode.tsx


def resolve(timing, ref):
    if ref == "END":
        return timing["duration"] + timing.get("end_hold", TAIL)
    lid, _, frac = ref.partition("@")
    ln = next(l for l in timing["lines"] if l["id"] == lid)
    return ln["start"] + (ln["end"] - ln["start"]) * float(frac or 0)


def main():
    ep = Path(sys.argv[1]).resolve()
    timing = json.loads((ep / "audio" / "timing.json").read_text())
    beats = json.loads((ep / "beats.json").read_text())
    # Paths relative to the cues file (mix_audio.py resolves them), so the file is the same in every checkout.
    rel = lambda name: Path(os.path.relpath(ROOT / "assets" / "sfx" / f"{name}.wav", ep / "audio")).as_posix()
    cues = [{"file": rel(name), "at": round(resolve(timing, ref), 3), "gain_db": gain}
            for name, ref, gain in beats["sfx"]]
    out = ep / "audio" / "sfx_cues.json"
    out.write_text(json.dumps(cues, indent=2))
    print(f"{len(cues)} cues -> {out}; episode length {timing['duration'] + timing.get('end_hold', TAIL):.2f}s")


if __name__ == "__main__":
    main()
