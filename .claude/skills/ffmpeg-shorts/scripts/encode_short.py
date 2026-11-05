#!/usr/bin/env python3
"""Mux a rendered video with the final audio mix and encode it to the Shorts
master spec: 1080x1920, H.264 High (tuned for animation), yuv420p, closed GOP
of half the frame rate, AAC-LC 48 kHz, moov atom at the front (faststart).

Standard library only. Needs ffmpeg on PATH.

Usage:
  python encode_short.py --video render.mp4 --audio mix.wav --out final.mp4 \
      [--ass captions.ass --fonts-dir assets/fonts] [--fps 30] [--crf 18] \
      [--preset slow] [--preview]

--video may also be an image-sequence pattern such as frames/%05d.png.
--preview writes a fast, small 540x960 proxy for the daily review instead.
"""
import argparse
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ass", help="ASS subtitle file to burn in (optional)")
    ap.add_argument("--fonts-dir", help="folder with the caption fonts (for --ass)")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preset", default="slow")
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()

    w, h = (540, 960) if args.preview else (1080, 1920)
    vin = ["-i", args.video]
    if "%" in args.video:
        vin = ["-framerate", str(args.fps), "-i", args.video]

    vf = [f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos",
          f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black",
          f"fps={args.fps}"]
    if args.ass:
        esc = args.ass.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        sub = f"ass='{esc}'"
        if args.fonts_dir:
            fd = args.fonts_dir.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
            sub += f":fontsdir='{fd}'"
        vf.append(sub)
    vf.append("format=yuv420p")

    if args.preview:
        venc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "28"]
        aenc = ["-c:a", "aac", "-b:a", "96k", "-ar", "48000"]
    else:
        gop = max(args.fps // 2, 1)
        venc = ["-c:v", "libx264", "-preset", args.preset, "-tune", "animation",
                "-crf", str(args.crf), "-profile:v", "high", "-level:v", "4.2",
                "-g", str(gop), "-keyint_min", str(gop), "-sc_threshold", "0",
                "-flags", "+cgop", "-bf", "2", "-maxrate", "16M", "-bufsize", "32M",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]
        aenc = ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]

    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-y", *vin, "-i", args.audio,
           "-map", "0:v:0", "-map", "1:a:0", "-vf", ",".join(vf),
           *venc, *aenc, "-shortest", "-movflags", "+faststart", args.out]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr[-4000:])
        sys.exit("encode failed")
    print(args.out)


if __name__ == "__main__":
    main()
