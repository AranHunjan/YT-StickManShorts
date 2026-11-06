#!/usr/bin/env python3
"""Topic ideas for the fact finder, without spending tokens on fetching.

  trends   What people are searching for and reading right now: Google Trends' daily
           trending searches for each country in channel.json (topics.trend_geos), and
           Wikipedia's most-read English articles from yesterday. The fact finder looks
           for an everyday object with a hidden story inside one of these.
  random   A truly random draw (system randomness, so not the model's favourite picks)
           of everyday objects from different categories, skipping objects already covered.

Usage:
  python tools/episode/topics.py trends [--limit 15]
  python tools/episode/topics.py random [--n 6]
Prints markdown. Standard library only. Network sources can fail; it reports and carries on.
"""
import argparse
import json
import random
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EPISODES, channel  # noqa: E402

UA = {"User-Agent": "KipNDex-topic-scout/1.0 (YouTube Shorts research; contact via the channel)"}
HT = "{https://trends.google.com/trending/rss}"
SKIP_WIKI = re.compile(r"^(Main_Page|Special:|Wikipedia:|Portal:|File:|Help:|Talk:|User:|Template:|Category:)|^-$")

OBJECTS = {
    "kitchen": ["can opener", "fork", "toaster", "microwave", "egg carton", "tea bag", "coffee filter", "oven mitt",
                "chopsticks", "ice cube tray", "measuring cup", "bread bag clip", "kettle", "salt shaker", "pepper grinder",
                "cheese grater", "pizza cutter", "whisk", "frying pan", "dish sponge"],
    "food and packaging": ["chip bag", "soda can", "pizza box", "cereal box", "milk carton", "bubble wrap", "bottle cap",
                           "fruit sticker", "aluminium foil", "chewing gum", "popcorn bag", "juice box", "egg", "bagel",
                           "pretzel", "candy cane", "sugar cube", "cupcake liner", "takeout box", "tin can"],
    "bathroom": ["toothbrush", "toothpaste tube", "toilet paper roll", "bar of soap", "shampoo bottle", "comb", "towel",
                 "bathtub", "cotton swab", "toilet flush handle", "shower curtain", "bath plug"],
    "clothing": ["jeans pocket", "zipper", "button", "shoelace tip", "sock", "hoodie strings", "t-shirt tag",
                 "belt holes", "sneaker sole", "cap button", "pocket rivet", "bow tie", "watch strap holes"],
    "office and school": ["pencil", "eraser", "stapler", "paper clip", "sticky note", "highlighter", "ruler",
                          "binder rings", "envelope window", "rubber band", "chalk", "paper sizes", "ballpoint pen"],
    "tech": ["USB plug", "phone charger", "keyboard F and J bumps", "computer mouse", "headphone jack", "QR code",
             "barcode", "battery", "TV remote", "power outlet", "QWERTY layout", "SIM card", "Wi-Fi symbol"],
    "street and travel": ["traffic light", "stop sign", "crosswalk button", "manhole cover", "parking meter",
                          "fire hydrant", "airplane window hole", "gas pump", "road reflectors", "bus seat fabric",
                          "zebra crossing", "street name sign", "train ticket"],
    "home": ["door knob", "light switch", "house key", "padlock", "smoke detector", "couch cushion", "pillow tag",
             "light bulb", "clothespin", "doormat", "welcome mat", "window blinds", "candle"],
    "money and shopping": ["coin edges", "banknote", "credit card numbers", "receipt paper", "shopping cart",
                           "price tag ending in 99", "vending machine", "gift card", "piggy bank", "plastic bag"],
    "toys and games": ["dice", "playing cards", "rubber duck", "crayons", "yo-yo", "chess pieces", "toy brick",
                       "balloon", "teddy bear", "board game money", "marbles", "kite"],
    "sports and outdoors": ["golf ball dimples", "tennis ball fuzz", "soccer ball pattern", "basketball lines",
                            "bicycle bell", "sunglasses", "umbrella", "water bottle", "frisbee", "trophy", "medal"],
}


def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def google_trends(geo, limit):
    root = ET.fromstring(fetch(f"https://trends.google.com/trending/rss?geo={geo}"))
    out = []
    for item in root.iter("item"):
        news = item.find(f"{HT}news_item")
        out.append({
            "title": (item.findtext("title") or "").strip(),
            "traffic": (item.findtext(f"{HT}approx_traffic") or "").strip(),
            "news": (news.findtext(f"{HT}news_item_title") or "").strip() if news is not None else "",
            "link": (news.findtext(f"{HT}news_item_url") or "").strip() if news is not None else "",
        })
    return out[:limit]


def wikipedia_top(limit):
    day = datetime.now(timezone.utc) - timedelta(days=1)
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/{day:%Y/%m/%d}"
    arts = json.loads(fetch(url))["items"][0]["articles"]
    arts = [a for a in arts if not SKIP_WIKI.search(a["article"])]
    return day.strftime("%Y-%m-%d"), arts[:limit]


def covered():
    """Objects already used, from every fact sheet's **Object:** line (archive included)."""
    seen = set()
    for f in list(EPISODES.glob("*/fact.md")) + list(EPISODES.glob("_archive/*/fact.md")):
        m = re.search(r"\*\*Object:\*\*\s*(.+)", f.read_text(encoding="utf-8"))
        if m:
            seen.add(m.group(1).lower())
    return seen


def cmd_trends(limit):
    now = datetime.now(timezone.utc)
    print(f"# Trending, {now:%Y-%m-%d %H:%M} UTC\n")
    print("Look for an everyday object with a surprising hidden story inside a trend. Skip tragedies, politics, "
          "crime, health scares, real people's private lives and anything that will be stale before posting.\n")
    for geo in channel()["topics"]["trend_geos"]:
        try:
            items = google_trends(geo, limit)
        except Exception as e:  # noqa: BLE001 (a feed being down shouldn't stop the others)
            print(f"## Google Trends {geo}: unavailable ({e})\n")
            continue
        print(f"## Google Trends {geo} (daily trending searches)\n")
        for it in items:
            extra = f": {it['news']}" if it["news"] else ""
            print(f"- **{it['title']}** ({it['traffic']}){extra} {it['link']}".rstrip())
        print()
    try:
        day, arts = wikipedia_top(limit * 2)
        print(f"## Wikipedia most read, {day} (English, all countries)\n")
        for a in arts:
            print(f"- {a['article'].replace('_', ' ')} ({a['views']:,} views)")
    except Exception as e:  # noqa: BLE001
        print(f"## Wikipedia most read: unavailable ({e})")
    print("\nAlso check by web search: memes trending this week (Know Your Meme), viral TikTok trends, and holidays or "
          "events in the next 3 to 10 days (an episode posts a few days after it's made).")


def cmd_random(n):
    rng = random.SystemRandom()
    seen = covered()
    cats = rng.sample(list(OBJECTS), k=min(n, len(OBJECTS)))
    print("# Random draw\n")
    print("Pick one with a surprising, verifiable hidden story (or draw again). The fact bank (docs/FACT_BANK.md) is fine too.\n")
    for cat in cats:
        options = [o for o in OBJECTS[cat] if not any(o.lower() in s for s in seen)]
        picks = rng.sample(options, k=min(3, len(options)))
        print(f"- **{cat}:** {', '.join(picks)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("trends")
    t.add_argument("--limit", type=int, default=15)
    r = sub.add_parser("random")
    r.add_argument("--n", type=int, default=6)
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.cmd == "trends":
        cmd_trends(args.limit)
    else:
        cmd_random(args.n)


if __name__ == "__main__":
    main()
