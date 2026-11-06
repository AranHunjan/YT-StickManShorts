#!/usr/bin/env python3
"""Check an episode's script.json against docs/SCRIPTING.md and the fact sheet.
Errors must be fixed before recording; warnings are judgment calls for the editor.

Script markup: *word* = caption highlight, {57|fifty-seven} = caption shows 57 and the
voice says fifty-seven. Optional per-line fields: "beat" (hook, wrong_theory, correction,
escalation, reveal, twist, closer), "claims" (claim numbers from fact.md), "visual"
(what is on screen), "pause_before" / "max_pause" (seconds, used by tools/voice/speak.py).

The opening line follows the episode's hook style from shape.json (docs/HOOK_TEST.md):
"question" is Kip asking "Hey Dex... why...?"; "bold" opens straight on the surprising
claim, with no name or filler first. Length limits come from channel.json.

Usage:
  python tools/episode/lint_script.py 2        # or episodes/002
Exit code 1 when there are errors. Standard library only.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import LEGACY, ROOT, SHOWSAY, SPEAKERS, channel, episode_dir, fact_claims, read_json, report, say_text, show_text, words  # noqa: E402
import variety  # noqa: E402

# docs/SCRIPTING.md beat template: words per beat.
BEATS = {"hook": (6, 10), "wrong_theory": (8, 14), "correction": (8, 12), "escalation": (15, 22),
         "reveal": (20, 28), "twist": (22, 30), "closer": (12, 18)}
FILLER_START = re.compile(r"^(hey|hi|hello|so|okay|ok|um|well|dex|kip)\b", re.I)  # not allowed first in a bold hook
WPM = {"kip": 160, "dex": 145}  # typical delivered pace (docs/VOICE.md bands)
GAP = 0.25                # typical silence between lines, including the line edges


def lint(ep):
    errors, warnings = [], []
    path = ep / "script.json"
    if not path.exists():
        return [f"{path} is missing"], [], {}
    try:
        script = read_json(path)
    except ValueError as e:
        return [f"script.json is not valid JSON: {e}"], [], {}
    lines = script.get("lines") or []
    if not lines:
        return ["script.json has no lines"], [], {}
    deliveries = read_json(ROOT / "tools" / "voice" / "lines.json")["delivery"]
    claims = fact_claims(ep / "fact.md") if (ep / "fact.md").exists() else {}
    if not (ep / "fact.md").exists():
        errors.append("fact.md is missing: every fact needs a fact sheet")
    for key in ("episode", "title"):
        if key not in script:
            errors.append(f"script.json needs \"{key}\"")
    uses_claims = any("claims" in ln for ln in lines)

    for i, ln in enumerate(lines):
        lid = ln.get("id", f"#{i + 1}")
        where = f"{lid}:"
        if ln.get("id") != f"L{i + 1:02d}":
            errors.append(f"{where} ids must run L01, L02, ... in order (expected L{i + 1:02d})")
        if ln.get("speaker") not in SPEAKERS:
            errors.append(f"{where} speaker must be one of {SPEAKERS}")
        if ln.get("delivery") not in deliveries:
            errors.append(f"{where} delivery {ln.get('delivery')!r} is not in tools/voice/lines.json ({', '.join(deliveries)})")
        text = ln.get("text", "")
        if not text.strip():
            errors.append(f"{where} empty text")
            continue
        if text.count("*") % 2:
            errors.append(f"{where} unbalanced *highlight* stars")
        if text.count("{") != text.count("}") or text.count("{") != len(SHOWSAY.findall(text)):
            errors.append(f"{where} malformed {{show|say}} markup")
        for show, say in SHOWSAY.findall(text):
            if not show.strip() or not say.strip():
                errors.append(f"{where} empty side in {{{show}|{say}}}")
        if "—" in text or "--" in text:
            errors.append(f"{where} em dash: the owner's style is no em dashes (use a period, comma or '...')")
        if "–" in text:
            warnings.append(f"{where} en dash: prefer a comma or '...'")
        if re.search(r"\[[a-z ]+\]", text):
            warnings.append(f"{where} [tags] are only read by Chatterbox Turbo; the daily voices ignore them")
        if re.search(r"\d", SHOWSAY.sub("", text)):
            warnings.append(f"{where} digits outside {{show|say}}: write e.g. {{1896|eighteen ninety-six}} so the voice reads it right")
        low = say_text(text).lower()
        if re.search(r"\band (then|also)\b", low):
            warnings.append(f"{where} 'and then/also': join beats with 'but' or 'so' (docs/SCRIPTING.md)")
        if "subscribe" in low:
            errors.append(f"{where} no 'subscribe' calls to action (docs/SCRIPTING.md)")
        if re.search(r"\b(welcome back|in this video|today we)\b", low):
            warnings.append(f"{where} sounds like an intro: start on the hook")
        n = len(words(text))
        if n > 30:
            warnings.append(f"{where} {n} words in one line: split it (long lines are harder to voice and caption)")
        if ln.get("speaker") == "dex" and ln.get("delivery") in ("deadpan", "dry"):
            warnings.append(f"{where} Dex is warm and amused, never deadpan (docs/CHARACTERS.md)")
        cl = ln.get("claims")
        if cl is not None:
            if not isinstance(cl, list) or not all(isinstance(c, int) for c in cl):
                errors.append(f"{where} \"claims\" must be a list of claim numbers from fact.md")
            else:
                for c in cl:
                    if c not in claims:
                        errors.append(f"{where} claim {c} is not in fact.md's claims table")
                    elif not claims[c]["status"].lower().startswith("verified"):
                        errors.append(f"{where} claim {c} is not verified in fact.md ({claims[c]['status']})")
        elif uses_claims and re.search(r"\d", show_text(text)):
            warnings.append(f"{where} states a number but has no \"claims\" tag")
        if "beat" in ln and ln["beat"] not in BEATS:
            errors.append(f"{where} beat {ln['beat']!r} is not one of {', '.join(BEATS)}")
        for k in ("pause_before", "max_pause"):
            if k in ln and not (isinstance(ln[k], (int, float)) and 0.05 <= ln[k] <= 1.0):
                errors.append(f"{where} {k} must be seconds between 0.05 and 1.0")

    legacy = ep.name in LEGACY
    s_errs, s_warns, s_info = variety.check(ep)
    (warnings if legacy else errors).extend(f"shape: {e}" for e in s_errs)
    warnings.extend(f"shape: {w}" for w in s_warns)
    style = (s_info.get("shape") or {}).get("hook_style", "question")
    first = lines[0]
    hook = show_text(first.get("text", ""))
    if style == "question":
        if first.get("speaker") != "kip" or not hook.endswith("?"):
            warnings.append("L01: the question style opens with Kip asking a question (docs/HOOK_TEST.md)")
    else:
        if FILLER_START.match(hook):
            (warnings if legacy else errors).append(
                f"L01: the bold style can't spend the first second on '{hook.split()[0]}': open on the surprising claim (docs/HOOK_TEST.md)")
        if hook.lower().startswith("why"):
            warnings.append("L01: a why-question is the question style; the bold style opens with a claim")
    if len(words(first.get("text", ""))) > 10:
        warnings.append(f"L01: hook is {len(words(first.get('text', '')))} words; aim for 10 or fewer")
    if "*" not in first.get("text", ""):
        warnings.append("L01: highlight the odd detail in the hook with *stars*")
    run, prev = 0, None
    for ln in lines:
        run = run + 1 if ln.get("speaker") == prev else 1
        prev = ln.get("speaker")
        if run == 4:
            warnings.append(f"{ln.get('id')}: four lines in a row from {prev}; break it up with the other character")

    beats = [ln.get("beat") for ln in lines if ln.get("beat") in BEATS]
    if beats:
        order = list(BEATS)
        if [b for i, b in enumerate(beats) if i == 0 or b != beats[i - 1]] != sorted(dict.fromkeys(beats), key=order.index):
            warnings.append("beats are out of template order (hook, wrong_theory, correction, escalation, reveal, twist, closer)")
        for b, (lo, hi) in BEATS.items():
            n = sum(len(words(ln["text"])) for ln in lines if ln.get("beat") == b)
            if b not in beats:
                warnings.append(f"no '{b}' beat")
            elif not lo - 3 <= n <= hi + 3:
                warnings.append(f"beat '{b}' has {n} words (template {lo}-{hi})")

    length = channel()["length"]
    target, most, cap, low = tuple(length["words"]), length["max_words"], length["cap_seconds"], length["min_seconds"]
    if legacy:
        target, most, cap, low = (115, 130), 150, 59.5, 0
    total = sum(len(words(ln.get("text", ""))) for ln in lines)
    est = 0.3 + sum(len(say_text(ln.get("text", "")).split()) / WPM.get(ln.get("speaker"), 150) * 60 for ln in lines) \
        + GAP * (len(lines) - 1) + 0.9
    if total > most:
        errors.append(f"{total} words: too long to fit under {cap:g} s (target {target[0]}-{target[1]}, channel.json)")
    elif not target[0] <= total <= target[1]:
        warnings.append(f"{total} words (target {target[0]}-{target[1]})")
    longest_hold = length["end_hold"][1] - 0.9
    if est > cap:
        warnings.append(f"estimated length {est:.1f} s with the end hold: likely over the {cap:g} s cap")
    elif est + longest_hold < low:
        warnings.append(f"estimated length {est:.1f} s: likely under {low:g} s even with a longer end hold; add a few words")
    if script.get("status") != "final":
        warnings.append('script is not marked "status": "final" yet')
    stats = {"lines": len(lines), "words": total, "est_seconds": round(est, 1), "hook_style": style,
             "kip_lines": sum(ln.get("speaker") == "kip" for ln in lines),
             "dex_lines": sum(ln.get("speaker") == "dex" for ln in lines)}
    return errors, warnings, stats


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    ep = episode_dir(sys.argv[1])
    errs, warns, stats = lint(ep)
    code = report(errs, warns, f"script {ep.name}")
    print(f"  {stats}")
    sys.exit(code)
