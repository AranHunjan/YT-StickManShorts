"""Shared helpers for the episode tools: paths, "L05@0.45" time refs, the animator's
vocabulary (poses, expressions, prop kinds, sound effects) and fact-sheet parsing.
Standard library only."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EPISODES = ROOT / "episodes"
ANIM = ROOT / "packages" / "animator"
TAIL = 0.9  # seconds held after the last line; must match TAIL in packages/animator/src/episodes/Episode.tsx
SHOWSAY = re.compile(r"\{([^|}]*)\|([^}]*)\}")
REF = re.compile(r"^(L\d{2,3})@(\d*\.?\d+)$")
SPEAKERS = ("kip", "dex")
# Episodes approved before the 2026-11-06 rules (listener reactions, hook styles, claim ledger,
# variety tags). The newer checks only warn on these instead of blocking.
LEGACY = {"001"}


def channel():
    """Channel-wide settings from channel.json at the repo root (length, hook test, topics, variety)."""
    return read_json(ROOT / "channel.json")


def episode_dir(arg):
    """'2', '002' or 'episodes/002' -> Path to the episode folder."""
    p = Path(arg)
    if p.exists() and p.is_dir():
        return p.resolve()
    return EPISODES / f"{int(str(arg).strip('/').split('/')[-1]):03d}"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def show_text(text):
    """What the captions show: {show|say} -> show, no *stars* or [tags]."""
    return SHOWSAY.sub(lambda m: m.group(1), re.sub(r"\[[a-z ]+\]\s*", "", text)).replace("*", "").strip()


def say_text(text):
    """What the voice reads: {show|say} -> say."""
    return SHOWSAY.sub(lambda m: m.group(2), re.sub(r"\[[a-z ]+\]\s*", "", text)).replace("*", "").strip()


def words(text):
    return show_text(text).split()


def parse_ref(ref, line_ids):
    """'L05@0.45' -> ('L05', 0.45); 'END' -> ('END', 1.0). Raises ValueError when invalid."""
    if ref == "END":
        return "END", 1.0
    m = REF.match(str(ref))
    if not m:
        raise ValueError(f"bad time ref {ref!r} (use 'L05@0.45' or 'END')")
    lid, frac = m.group(1), float(m.group(2))
    if lid not in line_ids:
        raise ValueError(f"time ref {ref!r} points at unknown line {lid}")
    if not 0 <= frac <= 1:
        raise ValueError(f"time ref {ref!r}: the fraction must be between 0 and 1")
    return lid, frac


def ref_order(ref, line_ids):
    """Sortable position of a ref when no timing exists yet."""
    lid, frac = parse_ref(ref, line_ids)
    return (len(line_ids), 1.0) if lid == "END" else (line_ids.index(lid), frac)


def hold_of(timing):
    """Seconds the video holds after the last line: timing.json's end_hold (set by build.py), else 0.9."""
    return timing.get("end_hold", TAIL)


def end_hold(ep_name, voice_seconds):
    """The end hold an episode should get: 0.9 s, stretched up to channel.json's end_hold maximum so
    the video lasts at least length.min_seconds. Legacy episodes keep 0.9 s."""
    if ep_name in LEGACY:
        return TAIL
    length = channel()["length"]
    lo, hi = length["end_hold"]
    return round(min(max(length["min_seconds"] - voice_seconds, lo), hi), 2)


def length_problems(ep_name, voice_seconds):
    """(severity, message) about the episode's total length, or None when it fits channel.json."""
    total = voice_seconds + end_hold(ep_name, voice_seconds)
    if ep_name in LEGACY:
        return ("warn", f"{total:.1f} s (made before the 1-minute rule)") if total > 59.5 else None
    length = channel()["length"]
    lo, hi = length["min_seconds"], length["cap_seconds"]
    if total > hi:
        return ("fail", f"{total:.1f} s with the end hold: over the {hi:g} s cap. Tighten the gaps "
                        f"(speak.py --assemble --gap 0.12) or cut words")
    if total < lo:
        return ("fail", f"{total:.1f} s even with the longest end hold: under {lo:g} s, so not over 1 minute. "
                        f"Widen the gaps (speak.py --assemble --gap 0.22) or add a few words")
    return None


def ref_time(ref, timing):
    if ref == "END":
        return timing["duration"] + hold_of(timing)
    lid, _, frac = ref.partition("@")
    ln = next(l for l in timing["lines"] if l["id"] == lid)
    return ln["start"] + (ln["end"] - ln["start"]) * float(frac or 0)


def _src(rel):
    return (ANIM / "src" / rel).read_text(encoding="utf-8")


def vocab():
    """What the animator can draw today, read from its source code."""
    poses_src = _src("rig/poses.ts")
    block = poses_src[poses_src.index("export const POSES"):]
    block = block[: block.index("} satisfies")]
    poses = re.findall(r"^  (\w+):", block, re.M)
    types_src = _src("rig/types.ts")
    expr_block = types_src[types_src.index("export type Expression"): types_src.index(";", types_src.index("export type Expression"))]
    expressions = re.findall(r"'(\w+)'", expr_block)
    props = re.findall(r"case '(\w+)':", _src("episodes/Episode.tsx"))
    sfx = sorted(p.stem for p in (ROOT / "assets" / "sfx").glob("*.wav"))
    music = sorted(p.name for p in (ROOT / "assets" / "music").iterdir() if p.suffix in (".flac", ".wav", ".mp3"))
    g_src = _src("rig/gestures.ts")
    g_block = g_src[g_src.index("export const GESTURES"): g_src.index("} satisfies", g_src.index("export const GESTURES"))]
    gestures = {n: float(d) for n, d in re.findall(r"^  (\w+): \{dur: ([\d.]+)", g_block, re.M)}  # name: default seconds
    return {"poses": poses, "expressions": expressions, "props": props, "gestures": gestures, "sfx": sfx, "music": music}


CLAIM_HEAD = re.compile(r"^###\s+Claim\s+(\d+):\s*(.+)$")
CLAIM_FIELD = re.compile(r"^-\s+\*\*(Kind|Status|Qualification):\*\*\s*(.*)$")
CLAIM_SOURCE = re.compile(r"^-\s+\*\*Source:\*\*\s*\[([^\]]+)\]\((https?://[^)\s]+)\)\s*(?:\(([^)]*)\))?")


def fact_ledger(fact_md):
    """The claim ledger: '### Claim N: text' blocks with Kind, Status, Qualification and
    '- **Source:** [name](url) (type)' lines, each followed by a '> supporting passage'.
    Returns [] when the sheet has no ledger (older sheets use a table)."""
    claims, cur, src = [], None, None
    for raw in Path(fact_md).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        m = CLAIM_HEAD.match(line)
        if m:
            cur = {"n": int(m.group(1)), "claim": m.group(2).strip(), "kind": "", "status": "", "qualification": "", "sources": []}
            claims.append(cur)
            src = None
            continue
        if cur is None:
            continue
        if line.startswith("## "):
            cur = src = None
            continue
        m = CLAIM_FIELD.match(line)
        if m:
            cur[m.group(1).lower()] = m.group(2).strip()
            continue
        m = CLAIM_SOURCE.match(line)
        if m:
            src = {"name": m.group(1).strip(), "url": m.group(2), "type": (m.group(3) or "").strip(), "passage": ""}
            cur["sources"].append(src)
            continue
        if line.startswith(">") and src is not None:
            src["passage"] = (src["passage"] + " " + line.lstrip(">").strip()).strip()
    return claims


def fact_claims(fact_md):
    """Claims of a fact sheet: {number: {"claim", "sources", "status"}}, from the ledger or the older table."""
    ledger = fact_ledger(fact_md)
    if ledger:
        return {c["n"]: {"claim": c["claim"], "sources": "; ".join(s["name"] for s in c["sources"]), "status": c["status"]}
                for c in ledger}
    claims = {}
    for line in Path(fact_md).read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[0].isdigit():
            claims[int(cells[0])] = {"claim": cells[1], "sources": cells[2], "status": cells[3]}
    return claims


def fact_links(fact_md):
    """URLs listed in the fact sheet's source-links section (or anywhere, as a fallback)."""
    text = Path(fact_md).read_text(encoding="utf-8")
    section = text.split("## Source links", 1)[1] if "## Source links" in text else text
    return [u.rstrip(").,") for u in re.findall(r"https?://\S+", section)]


def report(errors, warnings, title):
    """Print a lint report; returns the exit code (1 if any error)."""
    print(f"{title}: {'FAIL' if errors else 'ok'} ({len(errors)} errors, {len(warnings)} warnings)")
    for e in errors:
        print(f"  ERROR {e}")
    for w in warnings:
        print(f"  warn  {w}")
    return 1 if errors else 0
