#!/usr/bin/env python3
"""How episodes did, next to how they were made: the data behind /performance.

Joins analytics/performance.csv (filled in by the owner, see analytics/README.md) with each
episode's shape.json (hook style, structure, humour...), topic source (trend or random,
from fact.md), length, and listening score (listening.md). Then it compares groups:
  - the hook test: question vs bold on "viewed vs swiped away" and average % viewed
  - trend vs random topics, and each shape dimension
  - where viewers drop off, mapped to the line being spoken at that second
Groups with fewer than 3 episodes are marked as too few to judge.

Usage:
  python tools/episode/performance.py [--platform youtube]
Prints markdown. Standard library only.
"""
import argparse
import csv
import re
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EPISODES, ROOT, hold_of, read_json, show_text  # noqa: E402
import listening  # noqa: E402
import variety  # noqa: E402

CSV = ROOT / "analytics" / "performance.csv"
METRICS = ["viewed_pct", "avg_pct_viewed", "views", "shares_per_1k"]
MIN_N = 3


def num(x):
    try:
        return float(str(x).replace(",", "").replace("%", "").strip())
    except ValueError:
        return None


def episode_info(n):
    ep = EPISODES / f"{n:03d}"
    info = {"episode": n}
    if (ep / "shape.json").exists():
        info.update({k: v for k, v in read_json(ep / "shape.json").items() if not k.startswith("_")})
    if (ep / "fact.md").exists():
        m = re.search(r"\*\*Topic source:\*\*\s*(\w+)", (ep / "fact.md").read_text(encoding="utf-8"))
        info["topic"] = m.group(1).lower() if m else "random"
    if (ep / "audio" / "timing.json").exists():
        info["timing"] = read_json(ep / "audio" / "timing.json")
        info["seconds"] = round(info["timing"]["duration"] + hold_of(info["timing"]), 1)
    s = listening.scores(ep) if (ep / "listening.md").exists() else None
    info["listening"] = s["average"] if s else None
    return info


def line_at(timing, t):
    for ln in timing["lines"]:
        if ln["start"] - 0.2 <= t <= ln["end"] + 0.2:
            return ln
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--platform", default="youtube")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if not CSV.exists():
        sys.exit("analytics/performance.csv is missing (see analytics/README.md)")
    rows = [r for r in csv.DictReader(CSV.open(encoding="utf-8")) if r.get("platform", "").lower() == args.platform and num(r.get("episode"))]
    if not rows:
        print(f"No {args.platform} rows in analytics/performance.csv yet. Fill in episodes 7 days after posting (analytics/README.md).")
        return
    eps = []
    for r in rows:
        info = episode_info(int(num(r["episode"])))
        for k in ("viewed_pct", "avg_pct_viewed", "views", "avg_view_s", "likes", "comments", "shares", "subs", "drop_at_s"):
            info[k] = num(r.get(k, ""))
        if info.get("views") and info.get("shares") is not None:
            info["shares_per_1k"] = round(1000 * info["shares"] / info["views"], 2)
        info["days"] = num(r.get("measured_after_days", ""))
        eps.append(info)

    print(f"# Performance, {args.platform}: {len(eps)} episodes\n")
    ages = {e["days"] for e in eps}
    if len(ages) > 1:
        print(f"Note: rows were measured at different ages ({sorted(a for a in ages if a is not None)} days); compare with care.\n")
    print("| Ep | Hook | Topic | s | Viewed % | Avg % viewed | Views | Shares/1k | Listening |")
    print("|---|---|---|---|---|---|---|---|---|")
    for e in sorted(eps, key=lambda e: e["episode"]):
        print(f"| {e['episode']:03d} | {e.get('hook_style', '?')} | {e.get('topic', '?')} | {e.get('seconds', '')} | "
              f"{e.get('viewed_pct') or ''} | {e.get('avg_pct_viewed') or ''} | {int(e['views']) if e.get('views') else ''} | "
              f"{e.get('shares_per_1k', '')} | {e.get('listening') or ''} |")

    def compare(key, label):
        groups = defaultdict(list)
        for e in eps:
            if e.get(key):
                groups[e[key]].append(e)
        if len(groups) < 2:
            return
        print(f"\n## {label}\n")
        print("| Group | n | " + " | ".join(METRICS) + " |")
        print("|---|---|" + "---|" * len(METRICS))
        for g, items in sorted(groups.items()):
            vals = []
            for m in METRICS:
                xs = [i[m] for i in items if i.get(m) is not None]
                vals.append(f"{st.median(xs):g}" if xs else "")
            flag = "" if len(items) >= MIN_N else " (too few to judge)"
            print(f"| {g}{flag} | {len(items)} | " + " | ".join(vals) + " |")

    compare("hook_style", "Hook test: question vs bold (medians; viewed % is what the hook decides)")
    compare("topic", "Trend vs random topics")
    for dim in variety.DIMS:
        compare(dim, f"Shape: {dim}")
    compare("listening", "By listening score")

    drops = [(e, e["drop_at_s"]) for e in eps if e.get("drop_at_s") is not None and e.get("timing")]
    if drops:
        print("\n## Where viewers drop off\n")
        for e, t in sorted(drops, key=lambda x: x[0]["episode"]):
            ln = line_at(e["timing"], t)
            what = f"{ln['id']} ({ln['speaker']}): \"{show_text(ln['text'])[:70]}\"" if ln else "between lines or in the end hold"
            print(f"- Ep {e['episode']:03d} at {t:g} s: {what}")
    print(f"\nGroups with fewer than {MIN_N} episodes are noise, not evidence. Recommend; don't change anything automatically.")


if __name__ == "__main__":
    main()
