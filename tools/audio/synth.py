#!/usr/bin/env python3
"""Generate the channel's own sound effects and a background music bed with code,
so every sound is ours (no licences, no Content ID claims). Needs numpy + soundfile
(the chatterbox environment has both).

Usage:
  python tools/audio/synth.py            # writes assets/sfx/*.wav and assets/music/*.wav
"""
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 48000
ROOT = Path(__file__).resolve().parents[2]
rng = np.random.default_rng(7)


def t(d):
    return np.arange(int(SR * d)) / SR


def env(n, a=0.005, r=0.1, total=None):
    """Attack/exponential-release envelope over n samples."""
    x = np.arange(n) / SR
    e = np.minimum(1, x / max(a, 1e-4)) * np.exp(-x / max(r, 1e-4))
    return e


def norm(x, peak=0.89):
    m = np.max(np.abs(x)) or 1
    return (x / m * peak).astype("float32")


def lowpass(x, cutoff):
    """One-pole low-pass (cheap, smooth)."""
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


def sweep_noise(d, f0, f1):
    """Noise whose brightness sweeps from f0 to f1 (approximate band sweep)."""
    n = rng.standard_normal(int(SR * d))
    out = np.zeros_like(n)
    seg = 512
    for s in range(0, len(n), seg):
        f = f0 + (f1 - f0) * (s / len(n))
        out[s:s + seg] = highpass(lowpass(n[s:s + seg], f * 1.6), f * 0.5)
    return out


# ---------------------------------------------------------------- effects
def pop():
    x = t(0.09)
    f = 950 * np.exp(-x * 18) + 380
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(x), 0.002, 0.03))


def whoosh():
    d = 0.42
    n = sweep_noise(d, 300, 2600)
    e = np.sin(np.pi * np.linspace(0, 1, len(n))) ** 2
    return norm(n * e, 0.7)


def ding():
    x = t(1.4)
    y = sum(a * np.sin(2 * np.pi * f * x) * np.exp(-x * dcy) for f, a, dcy in
            [(1320, 1.0, 3.0), (2640, 0.45, 5.5), (3960, 0.2, 8.0), (1980, 0.25, 4.0)])
    return norm(y * env(len(x), 0.002, 10), 0.75)


def scribble():
    parts = []
    for i in range(4):
        d = 0.09 + 0.03 * rng.random()
        n = highpass(rng.standard_normal(int(SR * d)), 2500)
        parts += [n * np.hanning(len(n)), np.zeros(int(SR * 0.03))]
    return norm(np.concatenate(parts), 0.6)


def boing():
    x = t(0.55)
    f = 180 + 140 * np.exp(-x * 4) * (1 + 0.35 * np.sin(2 * np.pi * 14 * x))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(x), 0.003, 0.22)
    return norm(y, 0.8)


def erase():
    d = 0.7
    n = lowpass(highpass(rng.standard_normal(int(SR * d)), 400), 2500)
    am = 0.55 + 0.45 * np.sin(2 * np.pi * 7 * t(d))
    return norm(n * am * np.hanning(len(n)), 0.55)


def thud():
    x = t(0.3)
    y = np.sin(2 * np.pi * (70 + 60 * np.exp(-x * 30)) * x) * env(len(x), 0.002, 0.08)
    y[: int(SR * 0.006)] += 0.6 * rng.standard_normal(int(SR * 0.006))
    return norm(y, 0.85)


def sparkle():
    out = np.zeros(int(SR * 0.6))
    for i, f in enumerate([2093, 2637, 3136, 4186]):
        s = int(SR * 0.07 * i)
        x = t(0.35)
        tone = np.sin(2 * np.pi * f * x) * env(len(x), 0.002, 0.08)
        out[s:s + len(tone)] += tone[: len(out) - s]
    return norm(out, 0.5)


def tick():
    n = highpass(rng.standard_normal(int(SR * 0.025)), 3000) * np.hanning(int(SR * 0.025))
    return norm(n, 0.5)


# ---------------------------------------------------------------- music
NOTE = {n: i for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}


def hz(name, octave):
    return 440 * 2 ** ((NOTE[name] + 12 * (octave + 1) - 69) / 12)


def pluck(f, d, vel=1.0):
    """Soft harp-like pluck: harmonics with faster decay for higher partials."""
    x = t(d)
    y = sum((1 / h) * np.sin(2 * np.pi * f * h * x) * np.exp(-x * (3 + 2.2 * h)) for h in range(1, 7))
    return vel * y * env(len(x), 0.004, 10)


def music(bars=24, bpm=84):
    """Curious, light minor-key pluck bed: Am F C G, arpeggios + soft bass + pad."""
    beat = 60 / bpm
    total = int(SR * beat * 4 * bars) + SR
    out = np.zeros(total)
    prog = [("A", ["A", "C", "E"]), ("F", ["F", "A", "C"]), ("C", ["C", "E", "G"]), ("G", ["G", "B", "D"])]
    pattern = [0, 1, 2, 1, 0, 2, 1, 2]  # eighth-note arpeggio
    for b in range(bars):
        root, tri = prog[b % 4]
        start = int(SR * beat * 4 * b)
        # bass on beats 1 and 3
        for k in (0, 2):
            s = start + int(SR * beat * k)
            x = t(beat * 1.8)
            bass = 0.5 * np.sin(2 * np.pi * hz(root, 2) * x) * env(len(x), 0.01, 0.5)
            out[s:s + len(bass)] += bass[: total - s]
        # arpeggio eighths (skip some notes for air)
        for i, idx in enumerate(pattern):
            if (b % 2 == 1 and i in (3, 7)) or (i == 5 and b % 4 == 3):
                continue
            s = start + int(SR * beat * 0.5 * i)
            octv = 4 if i < 4 else 5
            p = pluck(hz(tri[idx], octv), 1.2, 0.32 if i % 2 else 0.42)
            out[s:s + len(p)] += p[: total - s]
        # soft pad
        x = t(beat * 4)
        pad = sum(np.sin(2 * np.pi * hz(n, 3) * x * (1 + det)) for n in tri for det in (-0.002, 0.002))
        pad *= 0.05 * np.sin(np.pi * np.linspace(0, 1, len(x)))
        out[start:start + len(pad)] += pad[: total - start]
        # light shaker on offbeats
        for i in range(8):
            if i % 2 == 1:
                s = start + int(SR * beat * 0.5 * i)
                n = highpass(rng.standard_normal(int(SR * 0.04)), 6000) * np.hanning(int(SR * 0.04)) * 0.05
                out[s:s + len(n)] += n[: total - s]
    out = lowpass(out, 6000)
    return norm(out, 0.8)


def main():
    sfx_dir = ROOT / "assets" / "sfx"
    mus_dir = ROOT / "assets" / "music"
    sfx_dir.mkdir(parents=True, exist_ok=True)
    mus_dir.mkdir(parents=True, exist_ok=True)
    for name, fn in [("pop", pop), ("whoosh", whoosh), ("ding", ding), ("scribble", scribble), ("boing", boing),
                     ("erase", erase), ("thud", thud), ("sparkle", sparkle), ("tick", tick)]:
        sf.write(str(sfx_dir / f"{name}.wav"), fn(), SR)
        print("sfx", name)
    sf.write(str(mus_dir / "curious-pluck-84bpm.flac"), music(), SR, format="FLAC")
    print("music curious-pluck-84bpm")


if __name__ == "__main__":
    main()
