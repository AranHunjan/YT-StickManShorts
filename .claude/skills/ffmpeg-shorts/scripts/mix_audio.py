#!/usr/bin/env python3
"""Mix one Short's audio: voice + music bed (ducked under the voice) + timed SFX,
then normalize loudness with two-pass EBU R128 (loudnorm).

Standard library only. Needs ffmpeg and ffprobe on PATH.

Usage:
  python mix_audio.py --voice voice.wav --out mix.wav \
      [--music bed.mp3] [--music-db -18] [--sfx cues.json] \
      [--duration 58.0] [--tail 0.6] [--target-lufs -14] [--true-peak -1.5]

cues.json is a list of SFX cues, times in seconds from the start:
  [{"file": "assets/sfx/pop.wav", "at": 1.25, "gain_db": -6}, ...]
SFX paths may be relative to the current folder or to the cues file.

The music file is looped if it is shorter than the Short.
Output: 48 kHz stereo 16-bit WAV, ready for encode_short.py.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SR = 48000
FMT = f"aformat=sample_fmts=fltp:sample_rates={SR}:channel_layouts=stereo"


def run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr[-4000:])
        sys.exit(f"ffmpeg failed: {' '.join(cmd[:6])} ...")
    return proc


def duration_of(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nw=1:nk=1", str(path)]).stdout.strip()
    return float(out)


def build_graph(n_sfx, has_music, music_db, sfx_cues, total):
    """Return (filtergraph, label of the mixed output)."""
    parts = []
    # Input 0: voice. Clean it up: rumble filter, de-ess, gentle compression.
    parts.append(
        f"[0:a]{FMT},highpass=f=70,deesser=i=0.4,"
        "acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,"
        f"apad,atrim=0:{total:.3f}[vclean]"
    )
    mix_inputs = []
    idx = 1
    if has_music:
        parts.append("[vclean]asplit=2[vmix][vsc]")
        # Input 1: music, looped via -stream_loop on the input, trimmed, ducked by the voice.
        parts.append(
            f"[1:a]{FMT},volume={music_db}dB,atrim=0:{total:.3f},"
            f"afade=t=in:d=0.3,afade=t=out:st={max(total - 0.5, 0):.3f}:d=0.5[mraw]"
        )
        parts.append(
            "[mraw][vsc]sidechaincompress=threshold=0.015:ratio=8:attack=15:"
            "release=400:makeup=1[mduck]"
        )
        mix_inputs += ["[vmix]", "[mduck]"]
        idx = 2
    else:
        mix_inputs.append("[vclean]")
    for i, cue in enumerate(sfx_cues):
        ms = int(round(float(cue["at"]) * 1000))
        gain = float(cue.get("gain_db", -6))
        parts.append(f"[{idx + i}:a]{FMT},volume={gain}dB,adelay={ms}|{ms}[s{i}]")
        mix_inputs.append(f"[s{i}]")
    n = len(mix_inputs)
    if n == 1:
        parts.append(f"{mix_inputs[0]}anull[mix]")
    else:
        parts.append(
            f"{''.join(mix_inputs)}amix=inputs={n}:duration=longest:normalize=0,"
            f"atrim=0:{total:.3f}[mix]"
        )
    return ";".join(parts), "[mix]"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--voice", required=True)
    ap.add_argument("--music")
    ap.add_argument("--music-db", type=float, default=-18.0,
                    help="music bed level before ducking (default -18 dB)")
    ap.add_argument("--sfx", help="JSON file with SFX cues")
    ap.add_argument("--duration", type=float,
                    help="total length in seconds (default: voice length + tail)")
    ap.add_argument("--tail", type=float, default=0.6,
                    help="seconds kept after the voice ends (default 0.6)")
    ap.add_argument("--target-lufs", type=float, default=-14.0)
    ap.add_argument("--true-peak", type=float, default=-1.5)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    total = args.duration or (duration_of(args.voice) + args.tail)
    cues = json.loads(Path(args.sfx).read_text()) if args.sfx else []
    for cue in cues:
        # SFX paths may be relative to the current folder or to the cues file.
        p = Path(cue["file"])
        if not p.is_absolute() and not p.exists():
            alt = Path(args.sfx).parent / p
            if alt.exists():
                cue["file"] = str(alt)
        if not Path(cue["file"]).exists():
            sys.exit(f"SFX file not found: {cue['file']}")

    inputs = ["-i", args.voice]
    if args.music:
        inputs += ["-stream_loop", "-1", "-i", args.music]
    for cue in cues:
        inputs += ["-i", cue["file"]]

    graph, out_label = build_graph(len(cues), bool(args.music), args.music_db, cues, total)
    norm = f"loudnorm=I={args.target_lufs}:TP={args.true_peak}:LRA=11"

    # Pass 1: measure.
    p1 = run(["ffmpeg", "-hide_banner", "-nostats", *inputs,
              "-filter_complex", f"{graph};{out_label}{norm}:print_format=json[o]",
              "-map", "[o]", "-f", "null", "-"])
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", p1.stderr, re.S)
    if not m:
        sys.exit("could not parse loudnorm measurement")
    meas = json.loads(m[-1])

    # Pass 2: apply with measured values (linear mode keeps dynamics natural).
    norm2 = (f"{norm}:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
             f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:"
             f"offset={meas['target_offset']}:linear=true")
    run(["ffmpeg", "-hide_banner", "-nostats", "-y", *inputs,
         "-filter_complex", f"{graph};{out_label}{norm2},aresample={SR}[o]",
         "-map", "[o]", "-ac", "2", "-c:a", "pcm_s16le", args.out])

    print(json.dumps({"out": args.out, "duration": round(total, 3),
                      "measured_input_lufs": float(meas["input_i"]),
                      "target_lufs": args.target_lufs}, indent=2))


if __name__ == "__main__":
    main()
