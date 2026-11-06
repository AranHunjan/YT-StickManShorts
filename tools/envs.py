#!/usr/bin/env python3
"""Find the voice environments and the animator's packages.

They are gitignored, so they only exist where setup ran: normally the main checkout.
A git worktree (Claude Code sessions often run in one, under .claude/worktrees/)
has none of its own, so every lookup falls back to the main checkout.

Usage:
  python tools/envs.py chatterbox     # prints that environment's python.exe (exit 1 if missing)
  python tools/envs.py qwen
  python tools/envs.py --json         # everything, as JSON
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV_PY = Path("Scripts/python.exe") if os.name == "nt" else Path("bin/python")


def main_checkout():
    """The main checkout's root when ROOT is a linked worktree, else None."""
    try:
        common = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--git-common-dir"],
                                capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    path = Path(common)
    if not path.is_absolute():
        path = (ROOT / path).resolve()
    main = path.parent if path.name == ".git" else None
    return main if main and main.resolve() != ROOT.resolve() else None


def roots():
    main = main_checkout()
    return [ROOT] + ([main] if main else [])


def python(name):
    """python.exe of tools/voice/.venvs/<name>, here or in the main checkout."""
    for r in roots():
        p = r / "tools" / "voice" / ".venvs" / name / VENV_PY
        if p.exists():
            return p
    return None


def node_modules():
    """The animator's node_modules folder in THIS checkout (Remotion must run from it)."""
    p = ROOT / "packages" / "animator" / "node_modules"
    return p if p.exists() else None


def remotion_browser():
    """An already-downloaded Chrome Headless Shell, so a worktree doesn't download its own."""
    for r in roots():
        base = r / "packages" / "animator" / "node_modules" / ".remotion"
        if base.exists():
            for exe in base.rglob("chrome-headless-shell.exe" if os.name == "nt" else "chrome-headless-shell"):
                return exe
    return None


def report():
    return {
        "root": str(ROOT),
        "main_checkout": str(main_checkout() or ""),
        "chatterbox_python": str(python("chatterbox") or ""),
        "qwen_python": str(python("qwen") or ""),
        "animator_node_modules": str(node_modules() or ""),
        "remotion_browser": str(remotion_browser() or ""),
    }


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "--json"
    if arg == "--json":
        print(json.dumps(report(), indent=2))
    else:
        p = python(arg)
        if not p:
            sys.exit(f"voice environment '{arg}' not found: run tools/voice/setup.ps1 in the main checkout")
        print(p.as_posix())
