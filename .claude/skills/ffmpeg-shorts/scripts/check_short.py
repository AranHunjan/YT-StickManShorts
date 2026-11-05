#!/usr/bin/env python3
"""Quality gate for a finished Short. Prints a JSON report and exits 1 when any
check fails, so the pipeline can refuse to publish a broken file.

Checks: resolution, frame rate, codecs, pixel format, faststart, duration range,
integrated loudness, true peak, silent gaps inside the video, black frames.

Standard library only. Needs ffmpeg and ffprobe on PATH.

Usage:
  python check_short.py final.mp4 [--min 15] [--max 60] [--lufs -14] \
      [--lufs-tol 1.0] [--max-tp -1.0] [--max-gap 0.7]
"""
import argparse
import json
import re
import struct
import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "format=duration:stream=codec_type,codec_name,width,height,"
               "avg_frame_rate,pix_fmt,sample_rate,channels",
               "-of", "json", path])
    return json.loads(out.stdout)


def moov_before_mdat(path):
    """Walk top-level MP4 boxes; faststart means 'moov' comes before 'mdat'."""
    with open(path, "rb") as f:
        while True:
            head = f.read(8)
            if len(head) < 8:
                return False
            size, kind = struct.unpack(">I4s", head)
            if kind == b"moov":
                return True
            if kind == b"mdat":
                return False
            if size == 1:
                size = struct.unpack(">Q", f.read(8))[0]
                f.seek(size - 16, 1)
            elif size == 0:
                return False
            else:
                f.seek(size - 8, 1)


def loudness(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn",
               "-af", "loudnorm=print_format=json", "-f", "null", "-"]).stderr
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", err, re.S)
    data = json.loads(m[-1])
    return float(data["input_i"]), float(data["input_tp"])


def silences(path, duration):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn",
               "-af", "silencedetect=noise=-45dB:d=0.3", "-f", "null", "-"]).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    gaps = []
    for i, s in enumerate(starts):
        e = ends[i] if i < len(ends) else duration
        gaps.append((round(s, 2), round(e, 2)))
    return gaps


def black_frames(path):
    err = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-an",
               "-vf", "blackdetect=d=0.2:pix_th=0.08", "-f", "null", "-"]).stderr
    return [(float(a), float(b)) for a, b in
            re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", err)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--min", type=float, default=15.0)
    ap.add_argument("--max", type=float, default=60.0)
    ap.add_argument("--lufs", type=float, default=-14.0)
    ap.add_argument("--lufs-tol", type=float, default=1.0)
    ap.add_argument("--max-tp", type=float, default=-1.0)
    ap.add_argument("--max-gap", type=float, default=0.7,
                    help="longest allowed silence inside the Short, in seconds")
    args = ap.parse_args()

    errors, warnings = [], []
    info = probe(args.file)
    dur = float(info["format"]["duration"])
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)

    if not v:
        errors.append("no video stream")
    else:
        if (v["width"], v["height"]) != (1080, 1920):
            errors.append(f"resolution {v['width']}x{v['height']}, expected 1080x1920")
        if v["codec_name"] != "h264":
            errors.append(f"video codec {v['codec_name']}, expected h264")
        if v.get("pix_fmt") != "yuv420p":
            errors.append(f"pixel format {v.get('pix_fmt')}, expected yuv420p")
        num, den = (int(x) for x in v["avg_frame_rate"].split("/"))
        fps = num / den if den else 0
        if round(fps) not in (24, 25, 30, 50, 60):
            warnings.append(f"unusual frame rate {fps:.2f}")
    if not a:
        errors.append("no audio stream")
    elif a["codec_name"] != "aac" or a.get("sample_rate") != "48000":
        warnings.append(f"audio {a['codec_name']} {a.get('sample_rate')} Hz, expected aac 48000")

    if not (args.min <= dur <= args.max):
        errors.append(f"duration {dur:.2f}s outside {args.min}-{args.max}s")
    if not moov_before_mdat(args.file):
        warnings.append("not faststart (moov after mdat); re-encode with -movflags +faststart")

    report = {"file": args.file, "duration": round(dur, 2)}
    if a:
        lufs, tp = loudness(args.file)
        report.update(integrated_lufs=lufs, true_peak_dbtp=tp)
        if abs(lufs - args.lufs) > args.lufs_tol:
            errors.append(f"loudness {lufs} LUFS, target {args.lufs} +/- {args.lufs_tol}")
        if tp > args.max_tp:
            errors.append(f"true peak {tp} dBTP above {args.max_tp}")
        # Ignore silence in the last second (the natural tail / loop point).
        gaps = [(s, e) for s, e in silences(args.file, dur)
                if (e - s) > args.max_gap and s < dur - 1.0]
        if gaps:
            errors.append(f"silent gaps longer than {args.max_gap}s at {gaps}")
    blacks = black_frames(args.file)
    if blacks:
        warnings.append(f"black frames at {blacks}")

    report.update(errors=errors, warnings=warnings, ok=not errors)
    print(json.dumps(report, indent=2))
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
