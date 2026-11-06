#!/usr/bin/env python3
"""The owner's listening score: the part of the audio check a measurement can't do.

The automatic audio check catches glitches, wrong words, odd pauses and bad gaps, but a
take can pass all of it and still sound flat or robotic. So every episode gets a short
sheet, episodes/NNN/listening.md, that the owner fills in after listening to:
  - every line the audio check flagged, and
  - a small sample of the rest: the hook, the longest line, and one more line.

Scores are 1 to 5 for: voice naturalness, emotional delivery, character distinction,
dialogue timing and humour delivery. /performance compares them with how episodes did.

Usage:
  python tools/episode/listening.py 2          # create the sheet if missing, else show its scores
  python tools/episode/listening.py 2 --json   # the scores as JSON
Standard library only. It never overwrites a sheet that already exists.
"""
import json
import re
import sys
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import episode_dir, read_json, show_text  # noqa: E402

ATTRS = ["Voice naturalness", "Emotional delivery", "Character distinction", "Dialogue timing", "Humour delivery"]
ROW = re.compile(r"^\|\s*(" + "|".join(ATTRS) + r")\s*\|\s*([1-5])?\s*\|\s*(.*?)\s*\|\s*$")


def to_listen(ep):
    """[(line id, start s, why)] for the flagged lines plus a sample of the rest."""
    timing = read_json(ep / "audio" / "timing.json")
    lines = {ln["id"]: ln for ln in timing["lines"]}
    picks = {}
    ac = ep / "audio" / "audio_check.json"
    if ac.exists():
        for ln in read_json(ac).get("lines", []):
            flags = [f for f in ln.get("flags", []) if f["severity"] in ("warn", "fail")]
            if flags:
                picks[ln["id"]] = "flagged: " + "; ".join(f"{f['kind']} ({f['severity']})" for f in flags)
    first = timing["lines"][0]["id"]
    longest = max(timing["lines"], key=lambda ln: ln["end"] - ln["start"])["id"]
    for lid, why in ((first, "sample: the hook"), (longest, "sample: the longest line")):
        picks.setdefault(lid, why)
    rest = [ln["id"] for ln in timing["lines"] if ln["id"] not in picks]
    if rest:
        picks[rest[zlib.crc32(ep.name.encode()) % len(rest)]] = "sample: one more line"
    return [(lid, lines[lid]["start"], picks[lid], lines[lid]) for lid in sorted(picks)], picks


def create(ep):
    items, _ = to_listen(ep)
    rows = "\n".join(f"| {a} |  |  |" for a in ATTRS)
    listen = "\n".join(
        f"- **{lid}** at {start:.1f} s, {ln['speaker'].title()}: \"{show_text(ln.get('text', ''))}\" ({why})"
        for lid, start, why, ln in items)
    text = f"""# Episode {ep.name}: listening score

The audio check measures glitches, words, pauses and gaps, but it can't hear whether a line
sounds natural or funny. Listen to these lines in `preview.mp4` (the times are where each
line starts), then score the whole episode. Fill in the Score column; leave the rest as is.

1 = sounds wrong, 3 = acceptable, 5 = sounds like a real cartoon.

| Attribute | Score | Notes |
|---|---|---|
{rows}

**Lines to re-voice (if any):**

## Lines to listen to

{listen}
"""
    (ep / "listening.md").write_text(text, encoding="utf-8")


def scores(ep):
    """{attribute: score or None} plus the notes, from a filled-in sheet."""
    out = {"scores": {a: None for a in ATTRS}, "notes": {}}
    path = ep / "listening.md"
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line.strip())
        if m:
            out["scores"][m.group(1)] = int(m.group(2)) if m.group(2) else None
            if m.group(3):
                out["notes"][m.group(1)] = m.group(3)
    filled = [v for v in out["scores"].values() if v is not None]
    out["complete"] = len(filled) == len(ATTRS)
    out["average"] = round(sum(filled) / len(filled), 2) if filled else None
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ep = episode_dir(sys.argv[1])
    if not (ep / "listening.md").exists():
        if not (ep / "audio" / "timing.json").exists():
            sys.exit(f"episode {ep.name} has no audio/timing.json yet")
        create(ep)
        print(f"created {ep / 'listening.md'}: the owner fills in the scores")
    s = scores(ep)
    if "--json" in sys.argv:
        print(json.dumps(s, indent=2))
    else:
        done = sum(v is not None for v in s["scores"].values())
        print(f"listening score {ep.name}: {done}/{len(ATTRS)} filled in" + (f", average {s['average']}" if s["average"] else ""))


if __name__ == "__main__":
    main()
