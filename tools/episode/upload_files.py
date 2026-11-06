#!/usr/bin/env python3
"""The extra files for uploading an episode, made from the finished build:

  captions.srt  Subtitles with the exact script words (YouTube's automatic captions mishear
                names like "Heinz"). Upload it in YouTube Studio (Subtitles) and to Facebook.
                Timed from audio/timing.json's word timings; each cue is one speaker, at most
                42 characters, broken at punctuation where possible.
  cover.jpg     A full-size frame for the cover on Instagram and TikTok: the hook's key word
                on screen, with the odd detail in view. Taken from final.mp4.

build.py runs this after encoding. Usage:
  python tools/episode/upload_files.py 2
Needs ffmpeg for the cover. Standard library otherwise.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import episode_dir, read_json  # noqa: E402

MAX_CHARS = 42      # one comfortable subtitle line
MAX_SECONDS = 3.5   # longer cues get split even mid-sentence
PUNCT = (".", ",", "?", "!", ":", ";", "...")


def stamp(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _text(ws):
    return " ".join(w["w"] for w in ws)


def _balanced(ws):
    """Split a too-long group in two, preferring punctuation, then the middle; recurse."""
    if len(ws) == 1 or (len(_text(ws)) <= MAX_CHARS and ws[-1]["e"] - ws[0]["s"] <= MAX_SECONDS):
        return [ws]
    mid = len(_text(ws)) / 2
    k = min(range(1, len(ws)), key=lambda k: abs(len(_text(ws[:k])) - mid) - (12 if ws[k - 1]["w"].endswith(PUNCT) else 0))
    return _balanced(ws[:k]) + _balanced(ws[k:])


def split_line(words):
    """Words of one line -> subtitle groups: one per sentence, and long sentences split in
    balanced halves, at punctuation where there is some (no one-word stragglers)."""
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if w["w"].endswith((".", "?", "!")) and not w["w"].endswith("..."):
            groups += _balanced(cur)
            cur = []
    if cur:
        groups += _balanced(cur)
    return [(g[0]["s"], g[-1]["e"], _text(g)) for g in groups]


def cues(timing):
    """[(start, end, text)]: words grouped per speaker into short subtitle lines."""
    out = []
    for ln in timing["lines"]:
        words = ln.get("words") or []
        out += split_line(words) if words else [(ln["start"], ln["end"], ln.get("caption") or ln["text"])]
    # Keep each cue on screen until just before the next one (no flicker in short gaps).
    fixed = []
    for i, (s, e, text) in enumerate(out):
        nxt = out[i + 1][0] if i + 1 < len(out) else None
        end = min(nxt - 0.02, e + 0.6) if nxt and nxt - e < 0.6 else e + (0.3 if nxt is None else 0)
        fixed.append((s, max(end, s + 0.4), text.replace("*", "")))
    return fixed


def write_srt(ep):
    timing = read_json(ep / "audio" / "timing.json")
    blocks = [f"{i}\n{stamp(s)} --> {stamp(e)}\n{text}\n" for i, (s, e, text) in enumerate(cues(timing), 1)]
    (ep / "captions.srt").write_text("\n".join(blocks), encoding="utf-8")
    return len(blocks)


def cover_time(timing):
    """Just after the hook's highlighted word appears, so the cover shows the key word."""
    first = timing["lines"][0]
    hi = [w for w in first.get("words", []) if w.get("hi")]
    return round((hi[0]["e"] + 0.25) if hi else min(first["start"] + 1.2, first["end"]), 2)


def write_cover(ep):
    final = ep / "final.mp4"
    if not final.exists():
        return None
    t = cover_time(read_json(ep / "audio" / "timing.json"))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", str(final), "-frames:v", "1", "-q:v", "2",
                    str(ep / "cover.jpg")], check=True)
    return t


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    ep = episode_dir(sys.argv[1])
    n = write_srt(ep)
    t = write_cover(ep)
    print(f"captions.srt: {n} cues" + (f"; cover.jpg from {t} s" if t is not None else "; no final.mp4 yet, so no cover"))
