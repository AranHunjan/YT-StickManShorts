#!/usr/bin/env python3
"""Glitch detection for one voice line: the problems a whole-line score misses.

Checks (calibrated on episode 001: its 14 approved lines all pass, and the
rejected Dex L03 take is caught by the "hum" check):

  hum           a quiet buzz or growl inside a pause: tonal sound 28 to 58 dB under
                the line's peak for 0.15 s or more. This was the episode 001 L03
                glitch ("Kip... [buzz] no."). FAIL
  pitch         the line's median pitch is outside the speaker's normal range
                (Qwen's Aiden sometimes comes out at ~230 Hz instead of ~150). FAIL
  rough_window  the roughest 0.5 s window (Praat jitter/shimmer) is far above what
                clean takes show. WARN
  rough_line    whole-line shimmer is high, which is what heavy time-stretching
                did to Kip's L09/L13 in episode 001. WARN

Praat numbers need praat-parselmouth (installed by tools/voice/setup.ps1); without
it the Praat checks are skipped and reported as such. Run with the chatterbox env.

Usage:
  python quality.py --speaker dex LINE.wav [LINE2.wav ...]
"""
import argparse
import json
import math

# Median pitch (Hz) a speaker's line may have, measured on loud voiced frames.
# Episode 001 approved lines: Kip 111-144 Hz, Dex 147-188 Hz.
PITCH_OK = {"kip": (80, 165), "dex": (95, 195)}
# Roughness that is unusual for each voice (episode 001 approved maxima in brackets).
ROUGH = {
    "kip": {"line_shimmer": 12.5, "win_jitter": 7.5, "win_shimmer": 32.0},  # [11.1, 6.0, 26.2]
    "dex": {"line_shimmer": 10.0, "win_jitter": 7.5, "win_shimmer": 18.0},  # [9.1, 5.7, 10.9]
}
WINDOW, HOP, MIN_PERIODS = 0.5, 0.1, 25
F0_MIN, F0_MAX = 75, 500


def _runs(mask, min_len):
    out, i, n = [], 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j < n and mask[j]:
                j += 1
            if j - i >= min_len:
                out.append((i, j))
            i = j
        else:
            i += 1
    return out


def pitch_and_hum(path):
    """Median pitch of loud voiced speech, and 'hum' segments (tonal noise in pauses)."""
    import librosa
    import numpy as np
    y, sr = librosa.load(str(path), sr=16000, mono=True)
    hop = 160  # 10 ms frames
    rms = librosa.feature.rms(y=y, frame_length=400, hop_length=hop)[0]
    db = 20 * np.log10(np.maximum(rms, 1e-6))
    f0, voiced, _ = librosa.pyin(y, fmin=60, fmax=400, sr=sr, frame_length=1024, hop_length=hop)
    n = min(len(db), len(f0))
    db, f0, voiced = db[:n], f0[:n], voiced[:n]
    peak = float(db.max())
    tonal = voiced & ~np.isnan(f0)
    loud = tonal & (db > peak - 30)
    median = float(np.median(f0[loud])) if loud.any() else None
    # f0 >= 66 Hz skips pyin's floor artefacts (it reports exactly 60 Hz in true silence).
    with np.errstate(invalid="ignore"):
        hum_mask = tonal & (f0 >= 66) & (db < peak - 28) & (db > peak - 58)
    hum = [(round(a / 100, 2), round(b / 100, 2)) for a, b in _runs(hum_mask, 15)]
    return median, hum


def praat_available():
    try:
        import parselmouth  # noqa: F401
        return True
    except ImportError:
        return False


def praat(path):
    """Whole-line HNR, jitter and shimmer, plus the roughest 0.5 s window. None without parselmouth."""
    if not praat_available():
        return None
    import parselmouth
    from parselmouth.praat import call

    def clean(v, k):
        return None if v is None or (isinstance(v, float) and math.isnan(v)) else round(v * k, 2)

    snd = parselmouth.Sound(str(path))
    dur = snd.get_total_duration()
    pp = call(snd, "To PointProcess (periodic, cc)", F0_MIN, F0_MAX)
    harm = call(snd, "To Harmonicity (cc)", 0.01, F0_MIN, 0.1, 1.0)

    def at(t0, t1):
        return {"jitter_pct": clean(call(pp, "Get jitter (local)", t0, t1, 0.0001, 0.02, 1.3), 100),
                "shimmer_pct": clean(call([snd, pp], "Get shimmer (local)", t0, t1, 0.0001, 0.02, 1.3, 1.6), 100),
                "hnr_db": clean(call(harm, "Get mean", t0, t1), 1)}

    out = at(0, 0)
    windows = []
    t = 0.0
    while t + WINDOW <= dur + 1e-6:
        if call(pp, "Get number of periods", t, t + WINDOW, 0.0001, 0.02, 1.3) >= MIN_PERIODS:
            m = at(t, t + WINDOW)
            if m["jitter_pct"] is not None and m["shimmer_pct"] is not None:
                windows.append({"t": round(t, 2), **m})
        t += HOP
    out["worst_jitter"] = max(windows, key=lambda w: w["jitter_pct"], default=None)
    out["worst_shimmer"] = max(windows, key=lambda w: w["shimmer_pct"], default=None)
    return out


def check(path, speaker):
    """All glitch checks for one line WAV. Returns {"median_f0", "hum", "praat", "flags", "fail"}."""
    median, hum = pitch_and_hum(path)
    p = praat(path)
    flags = []
    for a, b in hum:
        flags.append({"kind": "hum", "severity": "fail", "t": a,
                      "detail": f"quiet buzz or growl inside a pause at {a:.2f}-{b:.2f} s (the episode 001 L03 glitch)"})
    lo, hi = PITCH_OK.get(speaker, (60, 400))
    if median is not None and not lo <= median <= hi:
        flags.append({"kind": "pitch", "severity": "fail",
                      "detail": f"median pitch {median:.0f} Hz is outside {speaker}'s normal {lo}-{hi} Hz"})
    r = ROUGH.get(speaker)
    if p and r:
        wj, ws = p["worst_jitter"], p["worst_shimmer"]
        if wj and wj["jitter_pct"] > r["win_jitter"]:
            flags.append({"kind": "rough_window", "severity": "warn", "t": wj["t"],
                          "detail": f"rough pitch at {wj['t']:.1f}-{wj['t'] + WINDOW:.1f} s (jitter {wj['jitter_pct']}%)"})
        if ws and ws["shimmer_pct"] > r["win_shimmer"]:
            flags.append({"kind": "rough_window", "severity": "warn", "t": ws["t"],
                          "detail": f"rough loudness at {ws['t']:.1f}-{ws['t'] + WINDOW:.1f} s (shimmer {ws['shimmer_pct']}%)"})
        if p["shimmer_pct"] and p["shimmer_pct"] > r["line_shimmer"]:
            flags.append({"kind": "rough_line", "severity": "warn",
                          "detail": f"whole-line shimmer {p['shimmer_pct']}% (stretching or processing artefacts?)"})
    return {"median_f0": round(median, 1) if median else None, "hum": hum, "praat": p, "flags": flags,
            "fail": any(f["severity"] == "fail" for f in flags)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--speaker", required=True, choices=sorted(PITCH_OK))
    ap.add_argument("files", nargs="+")
    args = ap.parse_args()
    if not praat_available():
        print("note: praat-parselmouth is not installed here, so the Praat checks are skipped")
    for f in args.files:
        r = check(f, args.speaker)
        print(f, "FAIL" if r["fail"] else "ok", json.dumps({k: r[k] for k in ("median_f0", "hum", "flags")}))
