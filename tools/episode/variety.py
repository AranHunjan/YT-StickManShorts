#!/usr/bin/env python3
"""Episode shapes: how each episode tells its story, so two episodes about different
objects don't end up feeling identical (docs/SCRIPTING.md, "Variety").

Every episode has episodes/NNN/shape.json, written by the hook writer:
  {"hook_style": "question" | "bold",
   "hook": "why-question", "structure": "wrong-guess-reveal", "humour": "wrong-theory",
   "interaction": "kip-asks-dex-explains", "visual": "prop-showcase", "ending": "comment-prompt"}

The values below are the usual ones; a new value is allowed (with a warning) when none fits.
channel.json "variety" sets how many recent episodes to compare with and when to warn or block.

Usage:
  python tools/episode/variety.py        # every episode's shape
  python tools/episode/variety.py 2      # how episode 002 compares with the episodes before it
Standard library only.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import EPISODES, channel, episode_dir, read_json  # noqa: E402

VOCAB = {
    "hook": {
        "why-question": "Hey Dex... why does [object] have [odd detail]?",
        "for-you": "That [detail] isn't for the [object]. It's for you.",
        "never-noticed": "You touch [object] every day and never noticed [detail].",
        "myth-bust": "Everyone thinks [detail] is for [belief]. It isn't.",
        "doing-it-wrong": "You've been [using object] wrong your whole life.",
        "two-things": "There are two [holes] on your [object]. Only one is for [use].",
        "leftover": "Your [object] still has [detail] for something almost nobody owns anymore.",
        "origin-person": "[Object] looks like this because of one person in [year].",
        "big-number": "A startling number first.",
        "visual-first": "Frame 1 is the odd detail, big, with the question as the first caption.",
    },
    "structure": {
        "wrong-guess-reveal": "Kip's wrong theory, Dex's correction, escalation, reveal, twist (the template)",
        "myth-bust": "A common belief taken apart step by step",
        "origin-story": "A short story about one person or moment",
        "try-this-first": "The payoff (something to try) up front, then why it works",
        "mystery": "Dex drops clues and Kip guesses until he gets it",
        "debate": "Kip and Dex back two theories; the evidence settles it",
        "countdown": "Three surprising facts that build to the best one",
    },
    "humour": {
        "wrong-theory": "Kip's confident, wrong guess",
        "literal-visual": "A joke drawn literally on screen",
        "warm-tease": "Dex's gentle teasing",
        "kip-mishap": "Physical comedy: Kip tries it and it goes wrong",
        "absurd-escalation": "A small idea blown way out of proportion",
        "callback": "A running gag or a callback to an earlier line",
        "wordplay": "Puns and word jokes",
    },
    "interaction": {
        "kip-asks-dex-explains": "Kip asks, Dex explains (the default)",
        "dex-quizzes-kip": "Dex asks, Kip guesses",
        "kip-lectures": "Kip confidently explains, wrongly, and Dex steps in",
        "both-discover": "They work it out together",
        "kip-right": "Kip is right for once, and Dex is surprised",
    },
    "visual": {
        "prop-showcase": "One big prop, explained piece by piece",
        "cutaway": "A diagram or an inside view",
        "timeline": "Dates and history cards",
        "comparison": "Side by side, or before and after",
        "demo": "An action shown step by step",
        "scale": "Big numbers made visible",
        "map": "Places and journeys",
    },
    "ending": {
        "loop-question": "The last line runs back into the first",
        "comment-prompt": "Ask viewers a question",
        "callback-joke": "A joke tied to an earlier line",
        "try-it": "The viewer is told to try something",
        "twist": "One last surprising fact",
        "kip-mishap": "Kip tries it and it goes wrong",
    },
}
DIMS = list(VOCAB)
STYLES = ("question", "bold")


def shapes():
    """{episode name: shape} for every episode folder with a shape.json, in order."""
    out = {}
    for d in sorted(p for p in EPISODES.iterdir() if p.is_dir() and p.name.isdigit()):
        if (d / "shape.json").exists():
            try:
                out[d.name] = read_json(d / "shape.json")
            except ValueError:
                out[d.name] = {}
    return out


def check(ep):
    """(errors, warnings, info) for episode folder `ep`'s shape against the vocabulary and recent episodes."""
    errors, warnings = [], []
    path = ep / "shape.json"
    if not path.exists():
        return ["shape.json is missing: the hook writer records the episode's shape (tools/episode/variety.py)"], [], {}
    try:
        shape = read_json(path)
    except ValueError as e:
        return [f"shape.json is not valid JSON: {e}"], [], {}
    if shape.get("hook_style") not in STYLES:
        errors.append(f"shape.json: hook_style must be one of {', '.join(STYLES)}")
    for dim in DIMS:
        val = shape.get(dim)
        if not val:
            errors.append(f"shape.json: missing '{dim}' (usual values: {', '.join(VOCAB[dim])})")
        elif val not in VOCAB[dim]:
            warnings.append(f"shape.json: '{dim}' is a new value {val!r}; fine if none of {', '.join(VOCAB[dim])} fits")
    if shape.get("hook") and shape.get("hook_style") in STYLES:
        if (shape["hook"] == "why-question") != (shape["hook_style"] == "question"):
            warnings.append(f"shape.json: hook '{shape['hook']}' doesn't match hook_style '{shape['hook_style']}'")

    cfg = channel()["variety"]
    earlier = [(n, s) for n, s in shapes().items() if n.isdigit() and int(n) < int(ep.name)] if ep.name.isdigit() else list(shapes().items())
    recent = earlier[-cfg["compare_last"]:]
    sims = {}
    for n, other in recent:
        same = [d for d in DIMS if shape.get(d) and shape.get(d) == other.get(d)]
        sims[n] = len(same)
        if len(same) >= cfg["block_if_same"]:
            errors.append(f"same shape as episode {n} on all of {', '.join(same)}: change at least two of them")
        elif len(same) >= cfg["warn_if_same"]:
            warnings.append(f"almost the same shape as episode {n} ({len(same)}/6 the same: {', '.join(same)})")
    last2 = [s for _, s in earlier[-2:]]
    if len(last2) == 2:
        for dim in ("hook", "structure", "visual", "ending"):
            if shape.get(dim) and all(s.get(dim) == shape[dim] for s in last2):
                warnings.append(f"third episode in a row with {dim} '{shape[dim]}'")
    return errors, warnings, {"shape": shape, "same_as_recent": sims}


def main():
    if len(sys.argv) == 1:
        for n, s in shapes().items():
            print(n, " ".join(f"{d}={s.get(d, '?')}" for d in ["hook_style"] + DIMS))
        return 0
    if sys.argv[1] == "--vocab":
        print(json.dumps(VOCAB, indent=2))
        return 0
    ep = episode_dir(sys.argv[1])
    errs, warns, info = check(ep)
    print(f"shape {ep.name}: {'ok' if not errs else 'BLOCKED'} ({len(errs)} errors, {len(warns)} warnings)")
    for e in errs:
        print("  ERROR", e)
    for w in warns:
        print("  warn ", w)
    if info:
        print(" ", info["same_as_recent"])
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
