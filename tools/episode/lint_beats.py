#!/usr/bin/env python3
"""Check an episode's beats.json against what the animator can draw, before rendering.
Remotion silently draws nothing for an unknown prop and a plain stand for an unknown
pose, so mistakes only show up when someone watches the video. This catches them.

beats.json:
  "lines": {"L01": {"kip": [pose, expression], "dex": [pose, expression]}, ...}
  "moves": [{"who": "kip", "at": "L05@0.30", "gesture": "tilt", "until": "L05@0.62"},
            {"who": "dex", "at": "L02@0.70", "gesture": "laugh"},
            {"who": "kip", "at": "L12@0.45", "pose": "leanIn", "expr": "excited"}, ...]
           mid-line reactions: a pose and/or expression change, or a gesture layered on the
           current pose (nod, tilt, doubleTake, laugh, bounce, shake, emphasis; see
           packages/animator/src/rig/gestures.ts). "dur" (seconds) or "until" (a ref) sets
           how long a gesture lasts.
  "props": [{"id", "kind", "in": "L01@0", "out": "L02@0.3", "x", "y", "scale", ...}]
           (any other [ref, ref] field is a 0->1 progress animation, e.g. "squish")
  "burst": "L13@0"                       (mind-blown burst, optional)
  "sfx":   [[name, "L05@0.45", gain_db], ...]

Movement rules (docs/PLAN.md 6.7: something changes every 1.5 to 3 s):
  - nothing on screen may hold still for more than 3.5 s (warning above 3 s)
  - on every line of 4 s or more, the listener reacts at least once
  - on lines of 6 s or more, the speaker also moves mid-line (warning)
Episodes in common.LEGACY (approved before these rules) only get warnings.

Usage:
  python tools/episode/lint_beats.py 2         # or episodes/002
  python tools/episode/lint_beats.py --vocab   # list poses, expressions, gestures, props, sfx, music
Exit code 1 when there are errors. Standard library only.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import LEGACY, SPEAKERS, episode_dir, hold_of, parse_ref, read_json, ref_order, ref_time, report, vocab  # noqa: E402

FRAME_X = (150, 860)   # prop centre: clear of the edges and the right-side Shorts buttons
FRAME_Y = (450, 1200)  # below the captions (y ~372), above the bottom Shorts UI
STILL_WARN, STILL_ERROR = 3.0, 3.5  # seconds with nothing new on screen
LEGACY_STILL = 4.5     # the older, looser rule (warning only)
REACT_LINE = 4.0       # lines this long need a listener reaction
SPEAK_LINE = 6.0       # lines this long should have a mid-line move by the speaker
MOVE_GAP = 0.35        # a pose switch takes ~0.33 s; closer moves blur together
KNOWN_FIELDS = {"id", "kind", "in", "out", "x", "y", "scale", "text", "color", "word", "hi", "big57", "roll"}
MOVE_FIELDS = {"who", "at", "pose", "expr", "gesture", "dur", "until"}


def lint(ep):
    errors, warnings = [], []
    v = vocab()
    legacy = ep.name in LEGACY
    if not (ep / "beats.json").exists():
        return ["beats.json is missing"], [], {}
    try:
        beats = read_json(ep / "beats.json")
        script = read_json(ep / "script.json")
    except (ValueError, FileNotFoundError) as e:
        return [f"cannot read beats.json/script.json: {e}"], [], {}
    ids = [ln["id"] for ln in script["lines"]]
    timing = read_json(ep / "audio" / "timing.json") if (ep / "audio" / "timing.json").exists() else None

    def check_ref(ref, where):
        try:
            parse_ref(ref, ids)
            return True
        except ValueError as e:
            errors.append(f"{where}: {e}")
            return False

    lines = beats.get("lines", {})
    for lid in ids:
        if lid not in lines:
            errors.append(f"lines: {lid} has no poses")
            continue
        for who in SPEAKERS:
            pe = lines[lid].get(who)
            if not (isinstance(pe, list) and len(pe) == 2):
                errors.append(f"lines.{lid}.{who}: needs [pose, expression]")
                continue
            if pe[0] not in v["poses"]:
                errors.append(f"lines.{lid}.{who}: unknown pose {pe[0]!r} (have: {', '.join(v['poses'])})")
            if pe[1] not in v["expressions"]:
                errors.append(f"lines.{lid}.{who}: unknown expression {pe[1]!r} (have: {', '.join(v['expressions'])})")
            if who == "dex" and pe[1] == "deadpan":
                warnings.append(f"lines.{lid}.dex: Dex is never deadpan (docs/CHARACTERS.md)")
    for lid in lines:
        if lid not in ids:
            warnings.append(f"lines: {lid} is not in script.json")

    events, spans = [], []  # instants (refs) and animations ((ref, ref) ranges)
    moves = beats.get("moves", [])
    if not isinstance(moves, list):
        errors.append("moves: must be a list")
        moves = []
    good_moves = []
    for i, m in enumerate(moves):
        where = f"moves[{i}]"
        if not isinstance(m, dict):
            errors.append(f"{where}: must be an object like {{\"who\": \"kip\", \"at\": \"L05@0.3\", \"gesture\": \"nod\"}}")
            continue
        ok = True
        if m.get("who") not in SPEAKERS:
            errors.append(f"{where}: 'who' must be kip or dex")
            ok = False
        if not check_ref(m.get("at", ""), f"{where}.at"):
            ok = False
        if not any(k in m for k in ("pose", "expr", "gesture")):
            errors.append(f"{where}: needs a pose, an expr or a gesture")
            ok = False
        if "pose" in m and m["pose"] not in v["poses"]:
            errors.append(f"{where}: unknown pose {m['pose']!r} (have: {', '.join(v['poses'])})")
        if "expr" in m and m["expr"] not in v["expressions"]:
            errors.append(f"{where}: unknown expression {m['expr']!r} (have: {', '.join(v['expressions'])})")
        if m.get("who") == "dex" and m.get("expr") == "deadpan":
            warnings.append(f"{where}: Dex is never deadpan (docs/CHARACTERS.md)")
        if "gesture" in m and m["gesture"] not in v["gestures"]:
            errors.append(f"{where}: unknown gesture {m['gesture']!r} (have: {', '.join(v['gestures'])})")
            ok = False
        if "dur" in m and not (isinstance(m["dur"], (int, float)) and 0.2 <= m["dur"] <= 6):
            errors.append(f"{where}: dur must be 0.2 to 6 seconds")
            ok = False
        if "until" in m:
            if not check_ref(m["until"], f"{where}.until"):
                ok = False
            elif ok and ref_order(m["until"], ids) <= ref_order(m["at"], ids):
                errors.append(f"{where}: 'until' ({m['until']}) must come after 'at' ({m['at']})")
                ok = False
        if set(m) - MOVE_FIELDS:
            warnings.append(f"{where}: unknown fields {sorted(set(m) - MOVE_FIELDS)} are ignored")
        if ok:
            good_moves.append(m)
            events.append(m["at"])

    seen = set()
    for p in beats.get("props", []):
        pid = p.get("id", "?")
        where = f"props.{pid}"
        if pid in seen:
            errors.append(f"{where}: duplicate id")
        seen.add(pid)
        if p.get("kind") not in v["props"]:
            errors.append(f"{where}: unknown kind {p.get('kind')!r}; add a component and a case in Episode.tsx, or use one of: {', '.join(v['props'])}")
        ok = all(check_ref(p.get(k, ""), f"{where}.{k}") for k in ("in", "out"))
        if ok and ref_order(p["in"], ids) >= ref_order(p["out"], ids):
            errors.append(f"{where}: 'in' ({p['in']}) must come before 'out' ({p['out']})")
        xs = p.get("x")
        for x in (xs if isinstance(xs, list) else [xs]):
            if not isinstance(x, (int, float)):
                errors.append(f"{where}: x must be a number (or [from, to] with a 'move' progress)")
            elif not FRAME_X[0] <= x <= FRAME_X[1]:
                warnings.append(f"{where}: x={x} is near the edge or the Shorts buttons (keep {FRAME_X[0]}-{FRAME_X[1]})")
        y = p.get("y")
        if not isinstance(y, (int, float)):
            errors.append(f"{where}: y must be a number")
        elif not FRAME_Y[0] <= y <= FRAME_Y[1]:
            warnings.append(f"{where}: y={y} may hit the captions or the bottom Shorts UI (keep {FRAME_Y[0]}-{FRAME_Y[1]})")
        if isinstance(p.get("scale"), (int, float)) and not 0.2 <= p["scale"] <= 1.6:
            warnings.append(f"{where}: scale {p['scale']} is unusual (props are drawn at 1.3x this)")
        for k, val in p.items():
            if k not in KNOWN_FIELDS and isinstance(val, list) and len(val) == 2 and all(isinstance(r, str) for r in val):
                if check_ref(val[0], f"{where}.{k}") and check_ref(val[1], f"{where}.{k}"):
                    spans.append((val[0], val[1]))
        if ok:
            events += [p["in"], p["out"]]

    if beats.get("burst"):
        if check_ref(beats["burst"], "burst"):
            events.append(beats["burst"])
    for i, cue in enumerate(beats.get("sfx", [])):
        if not (isinstance(cue, list) and len(cue) == 3):
            errors.append(f"sfx[{i}]: needs [name, ref, gain_db]")
            continue
        name, ref, gain = cue
        if name not in v["sfx"]:
            errors.append(f"sfx[{i}]: unknown sound {name!r} (have: {', '.join(v['sfx'])})")
        if check_ref(ref, f"sfx[{i}]"):
            events.append(ref)
        if not isinstance(gain, (int, float)) or not -24 <= gain <= 0:
            warnings.append(f"sfx[{i}]: gain {gain} dB is outside -24..0")
    for key, val in (beats.get("kipHold") or {}).items():
        if all(check_ref(r, f"kipHold.{key}") for r in val) and len(val) == 2:
            spans.append((val[0], val[1]))
    if beats.get("dexCard"):
        for k in ("in", "out"):
            if check_ref(beats["dexCard"].get(k, ""), f"dexCard.{k}"):
                events.append(beats["dexCard"][k])

    if not any(ref_order(p["in"], ids) <= (0, 0.1) for p in beats.get("props", []) if "in" in p and _ok(p["in"], ids)):
        warnings.append("nothing on screen in frame 1: show the odd detail big from the first frame (mute test)")

    stats = {"props": len(beats.get("props", [])), "moves": len(good_moves), "sfx": len(beats.get("sfx", []))}
    if timing and not errors:
        t = lambda ref: ref_time(ref, timing)  # noqa: E731
        span_s = [(t(a), t(b)) for a, b in spans]
        for m in good_moves:
            if "gesture" in m:
                start = t(m["at"])
                span_s.append((start, t(m["until"]) if "until" in m else start + m.get("dur", v["gestures"][m["gesture"]])))
        changes = ({0.0, timing["duration"] + hold_of(timing)} | {round(t(r), 2) for r in events}
                   | {round(ln["start"], 2) for i, ln in enumerate(timing["lines"])
                      if i == 0 or lines.get(ln["id"]) != lines.get(timing["lines"][i - 1]["id"])})
        points = sorted(changes | {round(x, 2) for sp in span_s for x in sp})
        gaps = [(b - a, a) for a, b in zip(points, points[1:]) if not any(s <= (a + b) / 2 <= e for s, e in span_s)]
        still = max(gaps) if gaps else (0.0, 0.0)
        stats["longest_still_s"] = round(still[0], 2)
        msg = f"nothing changes on screen for {still[0]:.1f} s from {still[1]:.1f} s: add a reaction, a pose change or a prop beat"
        if legacy:
            if still[0] > LEGACY_STILL:
                warnings.append(msg)
        elif still[0] > STILL_ERROR:
            errors.append(msg)
        elif still[0] > STILL_WARN:
            warnings.append(msg)

        quiet = []
        for ln in timing["lines"]:
            dur = ln["end"] - ln["start"]
            if dur < REACT_LINE:
                continue
            listener = "dex" if ln["speaker"] == "kip" else "kip"
            if not any(m["who"] == listener and ln["start"] - 0.05 <= t(m["at"]) <= ln["end"] + 0.2 for m in good_moves):
                quiet.append(ln["id"])
                if not legacy:
                    errors.append(f"{ln['id']} is {dur:.1f} s long and {listener.title()} never reacts: "
                                  "add a move while they listen (tilt, nod, laugh, doubleTake...)")
            if dur >= SPEAK_LINE and not any(m["who"] == ln["speaker"] and ln["start"] + 0.3 <= t(m["at"]) <= ln["end"] for m in good_moves):
                if not legacy:
                    warnings.append(f"{ln['id']} is {dur:.1f} s long: give {ln['speaker'].title()} a mid-line move too "
                                    "(emphasis on the key word, or a pose change)")
        if legacy and quiet:
            warnings.append(f"no listener reactions on the long lines {', '.join(quiet)} (made before the movement rules)")
        stats["lines_without_reaction"] = quiet

        for who in SPEAKERS:
            marks = sorted([(t(m["at"]), "move") for m in good_moves if m["who"] == who and ("pose" in m or "gesture" in m)]
                           + [(ln["start"], "line") for ln in timing["lines"]])
            for (a, ka), (b, kb) in zip(marks, marks[1:]):
                if b - a < MOVE_GAP and "move" in (ka, kb):
                    warnings.append(f"{who}: two moves only {b - a:.2f} s apart at {a:.2f} s (leave {MOVE_GAP} s so each one reads)")
    return errors, warnings, stats


def _ok(ref, ids):
    try:
        parse_ref(ref, ids)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--vocab":
        print(json.dumps(vocab(), indent=2))
        sys.exit(0)
    ep = episode_dir(sys.argv[1])
    errs, warns, stats = lint(ep)
    code = report(errs, warns, f"beats {ep.name}")
    print(f"  {stats}")
    sys.exit(code)
