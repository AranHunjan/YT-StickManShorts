#!/usr/bin/env python3
"""Measure candidate voices and score them against the research-based targets in
docs/VOICE.md: average pitch, pitch variation (expressiveness), speaking rate and
loudness steadiness. Run it with the chatterbox environment (it has librosa).

Usage:
  python analyze.py                      # analyze out/voice-bakeoff
  python analyze.py --out DIR [--json results.json]

For every folder of line WAVs (and each reference clip) it reports:
  pitch_hz     median fundamental frequency (F0) of voiced speech
  range_st     pitch variation: 10th to 90th percentile F0 span in semitones
  wpm          words per minute over the trimmed speech
  loud_sd      standard deviation of loudness (dB) across speech: lower = steadier
  breaks       pitch breaks per second (jumps > 3 semitones): a glitch/warble proxy
  voiced       share of frames with a clear pitch. Below 0.2 means a whispered or
               garbled take: it is flagged BAD and left out of the averages
  score        0-100 match to that character's target profile
"""
import argparse
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Targets derived in docs/VOICE.md. (lo, hi) ideal band per metric.
TARGETS = {
    "kip": {"pitch_hz": (100, 135), "range_st": (6, 12), "wpm": (150, 180), "loud_sd": (0, 7)},
    # Dex = Qwen preset "aiden" (owner's pick, 2026-11-06): brighter and livelier than v2's deep deadpan.
    "dex": {"pitch_hz": (115, 165), "range_st": (6, 18), "wpm": (125, 160), "loud_sd": (0, 7)},
}
# How far outside the band a metric can be before it scores 0 (in the metric's units).
SLACK = {"pitch_hz": 40, "range_st": 6, "wpm": 50, "loud_sd": 6}
WORD = re.compile(r"[A-Za-z']+")
BAD_VOICED = 0.2


def measure(path, text=None):
    import librosa
    import numpy as np
    y, sr = librosa.load(str(path), sr=16000, mono=True)
    y, _ = librosa.effects.trim(y, top_db=35)
    dur = len(y) / sr
    # fmin 50 Hz so deep voices sliding into vocal fry are still tracked.
    f0, voiced, _ = librosa.pyin(y, fmin=50, fmax=350, sr=sr, frame_length=2048)
    vratio = float(np.mean(voiced))
    # Glitch proxy: sudden pitch jumps (> 3 semitones) between neighbouring voiced frames.
    fv = np.where(voiced, f0, np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        jumps = np.abs(12 * np.log2(fv[1:] / fv[:-1]))
    breaks = float(np.nansum(jumps > 3)) / max(dur, 1e-6)
    f0 = f0[voiced & ~np.isnan(f0)]
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0]
    db = 20 * np.log10(np.maximum(rms, 1e-5))
    speech = db[db > db.max() - 30]
    out = {
        "dur_s": round(dur, 2),
        "pitch_hz": round(float(np.median(f0)), 1) if len(f0) else None,
        "range_st": round(12 * math.log2(np.percentile(f0, 90) / np.percentile(f0, 10)), 1) if len(f0) > 10 else None,
        "loud_sd": round(float(np.std(speech)), 1),
        "voiced": round(vratio, 2),
        "breaks": round(breaks, 2),
        "bad": vratio < BAD_VOICED,
    }
    if text:
        words = len(WORD.findall(re.sub(r"\[[a-z ]+\]", "", text)))
        out["wpm"] = round(words / dur * 60) if dur else None
    return out


def band_score(v, lo, hi, slack):
    if v is None:
        return 0.0
    if lo <= v <= hi:
        return 1.0
    d = lo - v if v < lo else v - hi
    return max(0.0, 1 - d / slack)


def score(spk, m):
    t = TARGETS[spk]
    parts = [band_score(m.get(k), lo, hi, SLACK[k]) for k, (lo, hi) in t.items() if k in m]
    return round(100 * sum(parts) / len(parts)) if parts else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(HERE.parent.parent / "out" / "voice-bakeoff"))
    ap.add_argument("--json", help="also write results to this JSON file")
    args = ap.parse_args()
    out = Path(args.out)
    cfg = json.loads((HERE / "lines.json").read_text(encoding="utf-8"))
    lines = {ln["id"]: ln for ln in cfg["lines"]}
    results = []

    for ref in sorted((out / "refs").glob("*.wav")):
        spk = ref.stem.split("_")[0]
        if spk in cfg["voices"]:
            m = measure(ref, cfg["voices"][spk]["reference_text"])
            results.append({"set": "refs", "voice": ref.stem, "speaker": spk, **m, "score": score(spk, m)})

    for folder in sorted({p.parent for p in out.rglob("*.wav")}):
        if folder.name in ("refs", "compare"):
            continue
        per, bad = {}, {}
        for f in sorted(folder.glob("*.wav")):
            ln = lines.get(f.stem)
            if ln:
                m = measure(f, ln["text"])
                if m["bad"]:
                    bad.setdefault(ln["speaker"], []).append(f.stem)
                    print(f"BAD TAKE (voiced {m['voiced']}): {folder.name}/{f.name}")
                    continue
                per.setdefault(ln["speaker"], []).append(m)
        for spk, ms in per.items():
            agg = {"bad_takes": len(bad.get(spk, []))}
            for k in ("pitch_hz", "range_st", "wpm", "loud_sd"):
                vals = [m[k] for m in ms if m.get(k) is not None]
                agg[k] = round(sum(vals) / len(vals), 1) if vals else None
            name = "/".join(folder.relative_to(out).parts)
            results.append({"set": name, "voice": name, "speaker": spk, **agg, "score": score(spk, agg)})

    hdr = f"{'set':28} {'spk':4} {'pitch_hz':>8} {'range_st':>8} {'wpm':>5} {'loud_sd':>7} {'bad':>3} {'score':>5}"
    print(hdr)
    print("-" * len(hdr))
    for r in sorted(results, key=lambda r: (r["speaker"], -(r["score"] or 0))):
        print(f"{r['voice']:28} {r['speaker']:4} {str(r.get('pitch_hz')):>8} {str(r.get('range_st')):>8} "
              f"{str(r.get('wpm', '')):>5} {str(r.get('loud_sd')):>7} {str(r.get('bad_takes', '')):>3} {str(r['score']):>5}")
    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
