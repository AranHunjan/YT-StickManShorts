#!/usr/bin/env python3
"""Check an episode's claim ledger in fact.md: every claim the script says, with the exact
evidence behind it. Two sources that agree aren't enough on their own, so each source
also records what kind of source it is and the passage that supports the claim.

The ledger, under "## Claim ledger" in fact.md:

  ### Claim 3: Heinz already made more than 60 products in 1896.
  - **Kind:** count, at a date (1896)
  - **Status:** verified
  - **Qualification:** "more than 60" is the company's own figure; say "more than 60", not an exact number
  - **Source:** [Heinz company history](https://www.kraftheinzcompany.com/...) (primary: the company's own archive)
    > "By 1896 the company was making more than 60 products..."
  - **Source:** [Smithsonian Magazine](https://www.smithsonianmag.com/...) (secondary: magazine history piece)
    > "...the company was still actually selling more than 57..."

Kinds that involve a date must say which date it is. Invented, patent filed, patent granted,
first sold and founded are different dates and easy to mix up.
Source types: primary (the company, a patent, a law, an archive, the person's own account),
secondary (news, magazines, books, museums), tertiary (encyclopedias such as Wikipedia).

Rules: verified status; at least 2 sources from different websites; a supporting passage for
every source; at least one primary or secondary source; a primary source where practical
(warning); a date kind for any claim with a year in it. Older sheets (common.LEGACY) use the
old table and only get warnings.

Usage:
  python tools/episode/claims.py 2
Exit code 1 when there are errors. Standard library only.
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import LEGACY, episode_dir, fact_ledger, report  # noqa: E402

YEAR = re.compile(r"\b(1[5-9]\d\d|20\d\d)s?\b")
DATE_KIND = re.compile(r"invent|patent|first sold|sold|introduc|launch|trademark|found|event|first used|renam|law|release|built|opened|discover|start", re.I)
TYPES = ("primary", "secondary", "tertiary")


def site(url):
    """Registrable domain, roughly: en.wikipedia.org -> wikipedia.org, www.bbc.co.uk -> bbc.co.uk."""
    host = urlparse(url).netloc.lower().split(":")[0]
    parts = [p for p in host.split(".") if p not in ("www", "amp", "m")]
    if len(parts) >= 3 and len(parts[-1]) == 2 and parts[-2] in ("co", "com", "org", "net", "gov", "ac", "edu"):
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def check(ep):
    errors, warnings = [], []
    fact = ep / "fact.md"
    if not fact.exists():
        return ["fact.md is missing"], []
    ledger = fact_ledger(fact)
    if not ledger:
        msg = "fact.md has no claim ledger ('### Claim N:' blocks under '## Claim ledger'; see tools/episode/claims.py)"
        (warnings if ep.name in LEGACY else errors).append(msg)
        return errors, warnings
    seen = set()
    for c in ledger:
        tag = f"claim {c['n']}"
        if c["n"] in seen:
            errors.append(f"{tag}: duplicate number")
        seen.add(c["n"])
        if not c["status"].lower().startswith("verified"):
            errors.append(f"{tag} is not verified: {c['status'] or 'no status'}")
        srcs = c["sources"]
        if len(srcs) < 2:
            errors.append(f"{tag} has {len(srcs)} source(s); it needs 2 independent ones")
        elif len({site(s["url"]) for s in srcs}) < 2:
            errors.append(f"{tag}: all its sources are on {site(srcs[0]['url'])}; they aren't independent")
        for s in srcs:
            if len(s["passage"]) < 15:
                errors.append(f"{tag}: source '{s['name']}' has no supporting passage (a '> quote' line under it)")
            kind = s["type"].split(":")[0].strip().lower()
            if kind not in TYPES:
                warnings.append(f"{tag}: source '{s['name']}' should say its type: (primary|secondary|tertiary: what it is)")
        kinds = [s["type"].split(":")[0].strip().lower() for s in srcs]
        if srcs and all(k == "tertiary" for k in kinds):
            errors.append(f"{tag} rests only on encyclopedias: add a primary or secondary source")
        elif srcs and "primary" not in kinds:
            warnings.append(f"{tag} has no primary source (the company, a patent, an archive...); add one where practical")
        if YEAR.search(c["claim"]) and not DATE_KIND.search(c["kind"]):
            errors.append(f"{tag} has a year: its Kind must say which date (invented, patent filed, patent granted, first sold, founded, event...)")
        elif not c["kind"]:
            warnings.append(f"{tag} has no Kind (what sort of fact it is)")
        if not c["qualification"]:
            warnings.append(f"{tag}: write a Qualification, or 'none'")
    return errors, warnings


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    ep = episode_dir(sys.argv[1])
    errs, warns = check(ep)
    sys.exit(report(errs, warns, f"claims {ep.name}"))
