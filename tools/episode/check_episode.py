#!/usr/bin/env python3
"""Final gate before upload: are all the pieces present, current and consistent?

  files      fact sheet, script, beats, upload kit, voice, timing, final.mp4
  linters    lint_script.py and lint_beats.py have no errors
  audio      audio/audio_check.json exists, was made for this exact voice.wav, and did not FAIL
  video      final.mp4 was built from the current voice, timing, beats and script
             (build.py's review/build.json), matches the voice length, and passes the
             Shorts quality gate (check_short.py)
  facts      the claim ledger passes tools/episode/claims.py (sources, passages, date
             kinds); every claim is verified; the topic isn't a repeat
  upload     upload.md has a title under 100 characters, every fact.md source link,
             #shorts, "Made for kids: No", the AI label setting for each platform
             (docs/AI_LABELS.md), and no em dashes or placeholders
  listening  reminds the owner to fill in listening.md (tools/episode/listening.py)

Usage:
  python tools/episode/check_episode.py 2 [--json]
Writes episodes/002/review/check.json. Exit code 1 when something blocks the upload.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import claims as ledger  # noqa: E402
import lint_beats  # noqa: E402
import listening  # noqa: E402
import lint_script  # noqa: E402
from common import EPISODES, LEGACY, ROOT, channel, episode_dir, fact_claims, fact_links, hold_of, read_json  # noqa: E402

GATE = ROOT / ".claude" / "skills" / "ffmpeg-shorts" / "scripts" / "check_short.py"
REQUIRED = ["fact.md", "script.json", "beats.json", "upload.md", "audio/voice.wav", "audio/timing.json", "final.mp4"]


def topic(fact_md):
    m = re.search(r"\*\*Object:\*\*\s*(.+)", fact_md.read_text(encoding="utf-8")) if fact_md.exists() else None
    return re.sub(r"[^a-z ]", "", m.group(1).lower()).strip() if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    ep = episode_dir(args.episode)
    block, warn, info = [], [], {"episode": ep.name}

    missing = [f for f in REQUIRED if not (ep / f).exists()]
    block += [f"missing {f}" for f in missing]

    if not {"script.json", "fact.md"} & set(missing):
        errs, warns, stats = lint_script.lint(ep)
        block += [f"script: {e}" for e in errs]
        warn += [f"script: {w}" for w in warns]
        info["script"] = stats
    if not {"beats.json", "script.json"} & set(missing):
        errs, warns, stats = lint_beats.lint(ep)
        block += [f"beats: {e}" for e in errs]
        warn += [f"beats: {w}" for w in warns]
        info["beats"] = stats

    voice = ep / "audio" / "voice.wav"
    ac = ep / "audio" / "audio_check.json"
    if not ac.exists():
        block.append("audio check never ran: tools/voice/check_audio.py")
    elif voice.exists() and read_json(ac).get("voice_sha1") != hashlib.sha1(voice.read_bytes()).hexdigest():
        block.append("audio_check.json was made for a different voice.wav: re-run tools/voice/check_audio.py")
    else:
        verdict = read_json(ac)["verdict"]
        info["audio_check"] = verdict
        if verdict == "fail":
            block.append("the audio check FAILED: see audio/audio_check.json")

    timing = read_json(ep / "audio" / "timing.json") if (ep / "audio" / "timing.json").exists() else None
    if timing:
        bare = [ln["id"] for ln in timing["lines"] if not ln.get("words")]
        if bare:
            warn.append(f"no word timings for {bare}: captions fall back to whole lines (install faster-whisper)")

    final = ep / "final.mp4"
    if final.exists():
        stamp = ep / "review" / "build.json"
        if stamp.exists():  # build.py records what the video was built from
            built = read_json(stamp)["inputs"]
            changed = [f for f, h in built.items() if (ep / f).exists() and hashlib.sha1((ep / f).read_bytes()).hexdigest() != h]
        else:  # older builds: fall back to file times
            changed = [str(p.relative_to(ep)) for p in (voice, ep / "audio" / "timing.json", ep / "beats.json")
                       if p.exists() and p.stat().st_mtime > final.stat().st_mtime + 1]
        if changed:
            block.append(f"final.mp4 was built before the latest {', '.join(changed)}: rebuild (tools/episode/build.py)")
        length = channel()["length"]
        span = ["--max", "59.5" if ep.name in LEGACY else f"{length['cap_seconds'] + 0.1:g}"]
        if ep.name not in LEGACY:
            span += ["--min", f"{length['min_seconds'] - 0.1:g}"]  # must stay over 1 minute
        gate = subprocess.run([sys.executable, str(GATE), str(final)] + span, capture_output=True, text=True)
        try:
            g = json.loads(gate.stdout)
        except ValueError:
            g = {"errors": [f"quality gate crashed: {gate.stderr[-300:]}"], "warnings": []}
        info["quality_gate"] = {k: g.get(k) for k in ("duration", "integrated_lufs", "true_peak_dbtp", "ok")}
        block += [f"quality gate: {e}" for e in g.get("errors", [])]
        warn += [f"quality gate: {w}" for w in g.get("warnings", [])]
        need = timing["duration"] + hold_of(timing) if timing else None
        if need and g.get("duration") and abs(g["duration"] - need) > 0.25:
            block.append(f"final.mp4 is {g['duration']} s but the voice and end hold need {need:.2f} s: rebuild")

    fact = ep / "fact.md"
    if fact.exists():
        claims = fact_claims(fact)
        if not claims:
            block.append("fact.md has no claims table")
        for n, c in claims.items():
            if not c["status"].lower().startswith("verified"):
                block.append(f"fact.md claim {n} is not verified: {c['status']}")
            if len([s for s in re.split(r";|\band\b", c["sources"]) if s.strip()]) < 2:
                warn.append(f"fact.md claim {n} seems to list fewer than 2 sources")
        l_errs, l_warns = ledger.check(ep)
        block += [f"claims: {e}" for e in l_errs]
        warn += [f"claims: {w}" for w in l_warns]
        links = fact_links(fact)
        if len(links) < 2:
            block.append("fact.md lists fewer than 2 source links")
        info["sources"] = links
        mine = topic(fact)
        for other in sorted(EPISODES.glob("*/fact.md")) + sorted(EPISODES.glob("_archive/*/fact.md")):
            if other.parent != ep and mine and topic(other) == mine:
                block.append(f"same topic as {other.parent.name}: '{mine}'")
        if "—" in fact.read_text(encoding="utf-8"):
            warn.append("fact.md has em dashes (the owner's style is none)")

    up = ep / "upload.md"
    if up.exists():
        text = up.read_text(encoding="utf-8")
        m = re.search(r"\*\*Title:\*\*\s*(.+)", text)
        if not m:
            block.append("upload.md has no **Title:** line")
        else:
            title = m.group(1).strip()
            info["title"] = title
            if len(title) > 100:
                block.append(f"YouTube title is {len(title)} characters (limit 100)")
            elif len(title) > 70:
                warn.append(f"title is {len(title)} characters: phones cut it short")
        for link in fact_links(fact) if fact.exists() else []:
            if link not in text:
                block.append(f"upload.md is missing source link {link}")
        if "#shorts" not in text.lower():
            warn.append("upload.md: no #shorts hashtag")
        if not re.search(r"Made for kids:\s*\**No", text):
            warn.append("upload.md: say 'Made for kids: No' (docs/PUBLISHING.md)")
        if "—" in text:
            block.append("upload.md has em dashes (the owner's style is none)")
        if re.search(r"\{\{|\bTODO\b|\bTBD\b|XXX", text):
            block.append("upload.md still has placeholders (TODO, TBD, {{...}})")
        for label, pattern in (("YouTube 'Altered or synthetic content: No'", r"Altered or synthetic content:\W*No"),
                               ("Instagram/Facebook 'AI label: on'", r"\bAI label:\W*on"),
                               ("TikTok 'AI-generated content label: on'", r"AI-generated content label:\W*on")):
            if not re.search(pattern, text, re.I):
                warn.append(f"upload.md: say {label} (docs/AI_LABELS.md)")
        if f"episodes/{ep.name}/final.mp4" not in text:
            warn.append(f"upload.md should name the file episodes/{ep.name}/final.mp4")

    sheet = listening.scores(ep)
    if sheet is None:
        warn.append("no listening.md yet: run tools/episode/listening.py, then the owner listens and scores it")
    elif not sheet["complete"]:
        warn.append("listening.md isn't scored yet: the owner listens to its lines and fills in the 1-5 scores")
    else:
        info["listening"] = sheet["average"]

    verdict = "blocked" if block else "ready"
    result = {"verdict": verdict, "blockers": block, "warnings": warn, **info}
    (ep / "review").mkdir(exist_ok=True)
    (ep / "review" / "check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"episode {ep.name}: {verdict.upper()} ({len(block)} blockers, {len(warn)} warnings)")
        for b in block:
            print(f"  BLOCK {b}")
        for w in warn:
            print(f"  warn  {w}")
    sys.exit(1 if block else 0)


if __name__ == "__main__":
    main()
