#!/usr/bin/env python3
"""Build a finished episode from its voice track and beat sheet:

  sound cues -> Remotion render (silent) -> mix (voice + music + SFX, -14 LUFS)
  -> encode the Shorts master -> quality gate

Prerequisite: episodes/NNN/audio/voice.wav and timing.json from tools/voice/speak.py.
Needs ffmpeg and Node (Remotion) on PATH; run from anywhere.

Usage:
  python tools/episode/build.py 1            # builds episodes/001/final.mp4
  python tools/episode/build.py 1 --preview  # also a small preview.mp4 for review
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANIM = ROOT / "packages" / "animator"
SKILL = ROOT / ".claude" / "skills" / "ffmpeg-shorts" / "scripts"
MUSIC = ROOT / "assets" / "music" / "curious-pluck-84bpm.flac"
TAIL = 0.9


def run(cmd, cwd=None):
    print("$", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], cwd=cwd, check=True, shell=(os.name == "nt" and str(cmd[0]) == "npx"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode", type=int)
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--music-db", type=float, default=-21)
    args = ap.parse_args()
    ep = ROOT / "episodes" / f"{args.episode:03d}"
    audio = ep / "audio"
    timing = json.loads((audio / "timing.json").read_text())
    if timing.get("_estimated"):
        sys.exit("timing.json is an estimate: run tools/voice/speak.py first")
    py = sys.executable

    run([py, ROOT / "tools" / "episode" / "cues.py", ep])
    run(["npx", "remotion", "render", "src/index.ts", f"Ep{args.episode:03d}", ep / "render.mp4", "--muted"], cwd=ANIM)
    run([py, SKILL / "mix_audio.py", "--voice", audio / "voice.wav", "--music", MUSIC, "--music-db", args.music_db,
         "--sfx", audio / "sfx_cues.json", "--duration", f"{timing['duration'] + TAIL:.3f}", "--out", audio / "mix.wav"])
    run([py, SKILL / "encode_short.py", "--video", ep / "render.mp4", "--audio", audio / "mix.wav", "--out", ep / "final.mp4"])
    if args.preview:
        run([py, SKILL / "encode_short.py", "--video", ep / "render.mp4", "--audio", audio / "mix.wav", "--out", ep / "preview.mp4", "--preview"])
    run([py, SKILL / "check_short.py", ep / "final.mp4"])
    print(f"done: {ep / 'final.mp4'}")


if __name__ == "__main__":
    main()
