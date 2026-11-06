#!/usr/bin/env python3
"""Frames for the final visual review: the first frame (mute test and thumbnail) and one
frame from every line, with the Shorts UI zones shaded red (bottom 20%, right 15%),
plus a contact sheet of all of them. Needs ffmpeg on PATH. Standard library only.

Usage:
  python tools/episode/review_frames.py 2 [--video render.mp4]
Writes episodes/002/review/first.png, L01.png, L02.png, ... and sheet.png
"""
import argparse
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import episode_dir, read_json  # noqa: E402

FPS = 30
ZONES = "drawbox=x=0:y=ih*0.8:w=iw:h=ih*0.2:color=red@0.18:t=fill,drawbox=x=iw*0.85:y=0:w=iw*0.15:h=ih*0.8:color=red@0.18:t=fill"


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--video", help="video to sample (default: final.mp4, else render.mp4)")
    args = ap.parse_args()
    ep = episode_dir(args.episode)
    video = Path(args.video) if args.video else next((ep / f for f in ("final.mp4", "render.mp4") if (ep / f).exists()), None)
    if not video or not video.exists():
        sys.exit(f"no video in {ep}: build it first (tools/episode/build.py)")
    timing = read_json(ep / "audio" / "timing.json")
    out = ep / "review"
    out.mkdir(exist_ok=True)
    # What a viewer sees in the first half second (the mute test), then 60% into each line,
    # when its props are on screen and its caption is showing.
    shots = [("first", 0.5)] + [(ln["id"], ln["start"] + 0.6 * (ln["end"] - ln["start"])) for ln in timing["lines"]]
    for name, t in shots:
        ffmpeg("-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale=540:960,{ZONES}", str(out / f"{name}.png"))
    frames = sorted({round(t * FPS) for _, t in shots})
    cols = 5
    rows = math.ceil(len(frames) / cols)
    pick = "+".join(f"eq(n,{f})" for f in frames)
    ffmpeg("-i", str(video), "-vf", f"select='{pick}',scale=216:384,{ZONES},tile={cols}x{rows}:padding=6:color=white",
           "-fps_mode", "vfr", "-frames:v", "1", str(out / "sheet.png"))
    print(f"{len(shots)} frames + sheet.png in {out}")
    for name, t in shots:
        print(f"  {name:6} {t:6.2f} s  {out / (name + '.png')}")


if __name__ == "__main__":
    main()
