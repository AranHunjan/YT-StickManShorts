#!/usr/bin/env python3
"""Build a finished episode from its voice track and beat sheet:

  register the composition -> sound cues -> Remotion render (silent)
  -> mix (voice + music + SFX, -14 LUFS) -> encode the Shorts master -> quality gate

Prerequisite: episodes/NNN/audio/voice.wav and timing.json from tools/voice/speak.py.
Needs ffmpeg and Node (Remotion) on PATH; run from anywhere.

The music bed and its level come from script.json's optional "sound" block:
  "sound": {"music": "curious-pluck-84bpm.flac", "music_db": -21}

Usage:
  python tools/episode/build.py 1              # builds episodes/001/final.mp4
  python tools/episode/build.py 1 --preview    # also a small preview.mp4 for review
  python tools/episode/build.py 1 --no-render  # re-mix and re-encode only (sound changes)
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import envs  # noqa: E402

sys.path.insert(0, str(ROOT / "tools" / "episode"))
from common import LEGACY, channel, end_hold  # noqa: E402

ANIM = ROOT / "packages" / "animator"
SKILL = ROOT / ".claude" / "skills" / "ffmpeg-shorts" / "scripts"
DEFAULT_MUSIC = "curious-pluck-84bpm.flac"
DEFAULT_MUSIC_DB = -21
TAIL = 0.9


def run(cmd, cwd=None, env=None):
    print("$", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], cwd=cwd, check=True, env=env,
                   shell=(os.name == "nt" and str(cmd[0]) == "npx"))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode", type=int)
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--no-render", action="store_true", help="reuse render.mp4 (only the sound changed)")
    ap.add_argument("--music-db", type=float, help="music bed level before ducking (default: script.json sound.music_db, else -21)")
    args = ap.parse_args()
    ep = ROOT / "episodes" / f"{args.episode:03d}"
    audio = ep / "audio"
    timing = json.loads((audio / "timing.json").read_text())
    if timing.get("_estimated"):
        sys.exit("timing.json is an estimate: run tools/voice/speak.py first")
    sound = json.loads((ep / "script.json").read_text(encoding="utf-8")).get("sound", {})
    music = ROOT / "assets" / "music" / sound.get("music", DEFAULT_MUSIC)
    if not music.exists():
        sys.exit(f"music bed not found: {music}")
    music_db = args.music_db if args.music_db is not None else sound.get("music_db", DEFAULT_MUSIC_DB)
    py = sys.executable
    # The end hold: stretched a little when needed so the video lasts just over a minute (channel.json).
    hold = end_hold(ep.name, timing["duration"])
    if ep.name not in LEGACY and timing.get("end_hold") != hold:
        timing = {"duration": timing["duration"], "end_hold": hold, "lines": timing["lines"]}
        (audio / "timing.json").write_text(json.dumps(timing, indent=2))
        print(f"end hold {hold} s -> {timing['duration'] + hold:.2f} s in total")
    hold = timing.get("end_hold", TAIL)

    run([py, ROOT / "tools" / "episode" / "register.py"])
    run([py, ROOT / "tools" / "episode" / "cues.py", ep])
    if args.no_render and (ep / "render.mp4").exists():
        print("reusing render.mp4")
    else:
        if not envs.node_modules():
            sys.exit("packages/animator/node_modules is missing here: run `python tools/episode/preflight.py --fix`")
        env = dict(os.environ)
        local_browser = (ANIM / "node_modules" / ".remotion").exists()
        if not env.get("REMOTION_BROWSER") and not local_browser and envs.remotion_browser():
            env["REMOTION_BROWSER"] = str(envs.remotion_browser())  # reuse the main checkout's download
        run(["npx", "remotion", "render", "src/index.ts", f"Ep{args.episode:03d}", ep / "render.mp4", "--muted"], cwd=ANIM, env=env)
    run([py, SKILL / "mix_audio.py", "--voice", audio / "voice.wav", "--music", music, "--music-db", music_db,
         "--sfx", audio / "sfx_cues.json", "--duration", f"{timing['duration'] + hold:.3f}", "--out", audio / "mix.wav"])
    run([py, SKILL / "encode_short.py", "--video", ep / "render.mp4", "--audio", audio / "mix.wav", "--out", ep / "final.mp4"])
    if args.preview:
        run([py, SKILL / "encode_short.py", "--video", ep / "render.mp4", "--audio", audio / "mix.wav", "--out", ep / "preview.mp4", "--preview"])
    length = channel()["length"]
    span = ["--max", "59.5"] if ep.name in LEGACY else ["--min", f"{length['min_seconds'] - 0.1:g}", "--max", f"{length['cap_seconds'] + 0.1:g}"]
    run([py, SKILL / "check_short.py", ep / "final.mp4"] + span)
    # Fingerprint what this video was built from, so check_episode.py can tell if it's stale.
    (ep / "review").mkdir(exist_ok=True)
    (ep / "review" / "build.json").write_text(json.dumps({"inputs": inputs_sha1(ep)}, indent=2))
    print(f"done: {ep / 'final.mp4'}")


def inputs_sha1(ep):
    import hashlib
    files = ["audio/voice.wav", "audio/timing.json", "beats.json", "script.json"]
    return {f: hashlib.sha1((ep / f).read_bytes()).hexdigest() for f in files if (ep / f).exists()}


if __name__ == "__main__":
    main()
