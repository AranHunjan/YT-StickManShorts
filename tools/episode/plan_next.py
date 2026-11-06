#!/usr/bin/env python3
"""What the next episode should be, from channel.json and the episodes made so far:

  episode     the next free episode number (or --episode N)
  hook_style  "question" or "bold": the hook test alternates them (docs/HOOK_TEST.md)
  topic_mode  "trend" or "random": channel.json topics.trend_share, decided per pair of
              episodes so trend and random days split evenly across both hook styles
  length      the length rules from channel.json
  recent      the last episodes' topics and shapes, so the writers can do something different

The /episode command runs this first; the user can override any of it ("make a random one").

Usage:
  python tools/episode/plan_next.py [--episode N]
Prints JSON. Standard library only.
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EPISODES, channel, read_json  # noqa: E402


def next_episode():
    nums = [int(p.name) for p in EPISODES.iterdir() if p.is_dir() and p.name.isdigit()]
    return max(nums, default=0) + 1


def hook_style(n, test):
    if test.get("winner"):
        return test["winner"], "the hook test's winner (channel.json)"
    alt = "bold" if n % 2 == 0 else "question"
    if test["from_episode"] <= n <= test["until_episode"]:
        return alt, f"hook test, episodes {test['from_episode']}-{test['until_episode']}: even = bold, odd = question"
    if n > test["until_episode"]:
        return alt, "the hook test has ended: run /performance and set hook_test.winner in channel.json"
    return "question", "before the hook test"


def topic_mode(n, share):
    k = n // 2  # pairs: 2-3, 4-5, 6-7 ... share a mode, and each pair has one of each hook style
    return "trend" if math.floor((k + 1) * share + 1e-9) > math.floor(k * share + 1e-9) else "random"


def recent(n, count=5):
    out = []
    for d in sorted(p for p in EPISODES.iterdir() if p.is_dir() and p.name.isdigit() and int(p.name) < n)[-count:]:
        item = {"episode": d.name}
        fact = d / "fact.md"
        if fact.exists():
            text = fact.read_text(encoding="utf-8")
            for key, label in (("object", "Object"), ("topic_source", "Topic source")):
                m = re.search(rf"\*\*{label}:\*\*\s*(.+)", text)
                if m:
                    item[key] = m.group(1).strip()
        if (d / "shape.json").exists():
            item["shape"] = read_json(d / "shape.json")
        out.append(item)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--episode", type=int)
    args = ap.parse_args()
    cfg = channel()
    n = args.episode or next_episode()
    style, why_style = hook_style(n, cfg["hook_test"])
    mode = topic_mode(n, cfg["topics"]["trend_share"])
    print(json.dumps({
        "episode": n,
        "hook_style": style, "hook_style_reason": why_style,
        "topic_mode": mode, "topic_mode_reason": f"trend_share {cfg['topics']['trend_share']} (channel.json)",
        "trend_geos": cfg["topics"]["trend_geos"],
        "length": {k: v for k, v in cfg["length"].items() if not k.startswith("_")},
        "recent": recent(n),
    }, indent=2))


if __name__ == "__main__":
    main()
