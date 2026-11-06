#!/usr/bin/env python3
"""Find and shorten pauses inside a voice line. numpy + soundfile only.

A pause is a stretch at least 35 dB under the line's peak, lasting 0.15 s or more.
Episode 001's approved lines have pauses up to 0.78 s, all at punctuation.

Usage:
  python pauses.py LINE.wav                 # list the pauses
  python pauses.py LINE.wav --cap 0.45      # shorten every inner pause to at most 0.45 s (in place)
"""
import argparse

import numpy as np
import soundfile as sf

QUIET_DB = 35   # this far under the peak counts as silence
MIN_PAUSE = 0.15
FRAME = 0.01


def _levels(a, sr):
    hop = max(1, int(sr * FRAME))
    n = len(a) // hop
    frames = a[: n * hop].reshape(n, hop)
    db = 20 * np.log10(np.maximum(np.sqrt(np.mean(frames ** 2, axis=1)), 1e-6))
    return db, hop


def _load(path):
    a, sr = sf.read(str(path), dtype="float32")
    return (a.mean(axis=1) if a.ndim > 1 else a), sr


def analyze(path):
    """{"dur", "lead", "tail", "pauses": [(start, end), ...]} in seconds. Pauses exclude the edges."""
    a, sr = _load(path)
    db, hop = _levels(a, sr)
    quiet = db < db.max() - QUIET_DB
    loud = np.flatnonzero(~quiet)
    dur = len(a) / sr
    if not len(loud):
        return {"dur": round(dur, 3), "lead": round(dur, 3), "tail": 0.0, "pauses": []}
    first, last = loud[0], loud[-1]
    pauses, i = [], first
    while i <= last:
        if quiet[i]:
            j = i
            while j <= last and quiet[j]:
                j += 1
            if (j - i) * FRAME >= MIN_PAUSE:
                pauses.append((round(i * hop / sr, 3), round(j * hop / sr, 3)))
            i = j
        else:
            i += 1
    return {"dur": round(dur, 3), "lead": round(first * hop / sr, 3),
            "tail": round(max(dur - (last + 1) * hop / sr, 0), 3), "pauses": pauses}


def cap(path, max_pause, out=None):
    """Shorten every inner pause longer than max_pause to max_pause, cutting from its middle
    with short fades so there is no click. Writes in place unless `out` is given.
    Returns the list of (start, old length, new length) changes."""
    a, sr = _load(path)
    info = analyze(path)
    changes = []
    fade = int(sr * 0.005)
    for s0, s1 in reversed(info["pauses"]):  # back to front, so earlier times stay valid
        length = s1 - s0
        if length <= max_pause + 0.01:
            continue
        keep = max_pause / 2
        c0, c1 = int((s0 + keep) * sr), int((s1 - keep) * sr)
        left, right = a[:c0].copy(), a[c1:].copy()
        if len(left) > fade and len(right) > fade:
            left[-fade:] *= np.linspace(1, 0, fade, dtype="float32")
            right[:fade] *= np.linspace(0, 1, fade, dtype="float32")
        a = np.concatenate([left, right])
        changes.append((s0, round(length, 3), round(max_pause, 3)))
    if changes or out:
        sf.write(str(out or path), a, sr)
    return list(reversed(changes))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("wav")
    ap.add_argument("--cap", type=float, help="shorten inner pauses longer than this (seconds), in place")
    args = ap.parse_args()
    if args.cap:
        for s0, old, new in cap(args.wav, args.cap):
            print(f"pause at {s0:.2f} s: {old:.2f} -> {new:.2f} s")
    print(analyze(args.wav))
