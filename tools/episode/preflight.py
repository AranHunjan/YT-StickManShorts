#!/usr/bin/env python3
"""Is this PC ready to make an episode? Run before the pipeline so a missing tool fails
in seconds, not after the script is written.

Checks ffmpeg, Node, the voice environments (Chatterbox + Qwen, found in this checkout
or the main checkout), Whisper and Praat in the Chatterbox environment, the GPU, the
animator's packages, and free disk space.

In a git worktree (Claude Code sessions often use one) the animator has no packages of
its own; --fix installs them from npm's local cache (no admin rights, nothing outside
this folder is touched).

Usage:
  python tools/episode/preflight.py [--fix] [--json]
Exit code 1 if something required is missing.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import envs  # noqa: E402

PROBE = ("import json, importlib.util as u\n"
         "mods = ['torch', 'librosa', 'faster_whisper', 'parselmouth', 'chatterbox']\n"
         "out = {m: bool(u.find_spec(m)) for m in mods}\n"
         "if out['torch']:\n"
         "    import torch; out['cuda'] = torch.cuda.is_available()\n"
         "print(json.dumps(out))\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fix", action="store_true", help="install the animator's packages here if they are missing")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    need, warn, info = [], [], envs.report()

    for tool in ("ffmpeg", "ffprobe", "node", "npx"):
        if not shutil.which(tool):
            need.append(f"{tool} not on PATH (README: one-time setup)")
    cb, qw = envs.python("chatterbox"), envs.python("qwen")
    if not cb:
        need.append("Chatterbox voice environment missing: run tools\\voice\\setup.ps1 in the main checkout")
    else:
        try:
            mods = json.loads(subprocess.run([str(cb), "-c", PROBE], capture_output=True, text=True, timeout=180).stdout)
        except (ValueError, subprocess.TimeoutExpired):
            mods = {}
        info["chatterbox_modules"] = mods
        for m in ("torch", "librosa", "chatterbox"):
            if not mods.get(m):
                need.append(f"{m} missing from the Chatterbox environment")
        if not mods.get("faster_whisper"):
            need.append("faster-whisper missing from the Chatterbox environment (word-synced captions, transcript check)")
        if not mods.get("parselmouth"):
            warn.append("praat-parselmouth missing: the audio check skips the Praat roughness tests "
                        f"(fix: uv pip install --python \"{cb}\" praat-parselmouth)")
        if mods.get("torch") and not mods.get("cuda"):
            warn.append("no CUDA GPU visible to torch: voices will generate very slowly on the CPU")
    if not qw:
        need.append("Qwen voice environment missing (Dex's voice): run tools\\voice\\setup.ps1")

    if not envs.node_modules():
        if args.fix and shutil.which("npm"):
            print("installing the animator's packages from the npm cache (a few minutes)...", flush=True)
            r = subprocess.run("npm ci --prefer-offline --no-audit --no-fund", cwd=ROOT / "packages" / "animator", shell=True)
            if r.returncode or not envs.node_modules():
                need.append("npm ci failed in packages/animator")
        else:
            need.append("packages/animator/node_modules missing here: run with --fix (or `npm install` in packages/animator)")
    info["animator_node_modules"] = str(envs.node_modules() or "")
    if envs.node_modules() and not (envs.node_modules() / ".remotion").exists() and not envs.remotion_browser():
        warn.append("Remotion's headless browser isn't downloaded yet: the first render downloads it (~100 MB)")

    free_gb = shutil.disk_usage(ROOT).free / 1e9
    info["free_disk_gb"] = round(free_gb, 1)
    if free_gb < 10:
        warn.append(f"only {free_gb:.0f} GB free disk: renders and takes need room")

    result = {"ok": not need, "missing": need, "warnings": warn, **info}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"preflight: {'ready' if not need else 'NOT READY'}")
        for m in need:
            print(f"  MISSING {m}")
        for w in warn:
            print(f"  warn    {w}")
        print(f"  chatterbox python: {info['chatterbox_python'] or '-'}")
        print(f"  qwen python:       {info['qwen_python'] or '-'}")
    sys.exit(0 if not need else 1)


if __name__ == "__main__":
    main()
