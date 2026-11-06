# Kip N Dex (@KipNDex)

A daily animated Short about the hidden stories of everyday things, made almost entirely on one PC for $0.

- **Plan and decisions:** [docs/PLAN.md](docs/PLAN.md)
- **Characters:** [docs/CHARACTERS.md](docs/CHARACTERS.md)
- **Voices:** [docs/VOICE.md](docs/VOICE.md)
- **Channel setup:** [docs/CHANNEL.md](docs/CHANNEL.md)
- **Posting to YouTube, Instagram, Facebook and TikTok:** [docs/PUBLISHING.md](docs/PUBLISHING.md)

## Making an episode (Windows, from the repo root)

One-time setup: Node.js 22, ffmpeg (`winget install Gyan.FFmpeg`), `cd packages\animator && npm install`, and the voice environment (`tools\voice\setup.ps1`).

**Automatic:** in Claude Code, type `/episode`. Eight agents take it from a fact (something trending, or a random everyday object) to a checked `final.mp4`, each doing one job, with an audio checker and a final checker that send work back. See [docs/PIPELINE.md](docs/PIPELINE.md). You watch `preview.mp4`, score `listening.md`, and upload. A week later, add the numbers to `analytics/performance.csv`; `/performance` turns them into recommendations.

**By hand**, the same steps:

1. **Fact and script:** create `episodes\NNN\` with:
   - `fact.md`: the claims, each backed by two sources
   - `script.json`: who says what, with which delivery, plus the caption
   - `beats.json`: poses, props and sound cues per line
   - `upload.md`: titles, descriptions and captions

   Claude Code writes these with you, using episode 001 as the template.
2. **Voices:** generates several takes per line, auto-picks the best, and writes `voice.wav` + `timing.json`.
   - Kip is voiced by Chatterbox and Dex by Qwen's "Aiden" preset; `speak.py` runs both.
   - Word timings for the captions are added automatically.
   ```powershell
   .\tools\voice\.venvs\chatterbox\Scripts\python.exe tools\voice\speak.py --script episodes\001\script.json --out episodes\001\audio
   ```
   - Then check it: `& (python tools\envs.py chatterbox) tools\voice\check_audio.py episodes\001`
3. **Preview the animation (optional):** `cd packages\animator && npm run studio`, then open `Ep001`. New episodes appear automatically once they have `beats.json` and `audio\timing.json`.
4. **Build the finished video:** renders, mixes voice + music + SFX at -14 LUFS, encodes, and runs the quality gate:
   ```powershell
   python tools\episode\build.py 1 --preview
   ```
5. **Review:** `python tools\episode\check_episode.py 1` is the final gate. Watch `episodes\001\final.mp4`, then post it using `episodes\001\upload.md` and [docs/PUBLISHING.md](docs/PUBLISHING.md).

## Layout

| Path | What |
|---|---|
| `episodes/NNN/` | One folder per episode: fact sheet (with the claim ledger), shape, script, beats, audio, listening score, final video, upload kit |
| `channel.json` | Channel-wide settings: length cap, the hook test, trend days, variety rules |
| `analytics/` | Performance numbers typed in from each platform, for `/performance` |
| `packages/animator/` | Remotion: the stickman rig, props, captions, watermark, the episode compositions |
| `tools/voice/` | Voice generation (`speak.py`), the audio check (`check_audio.py`, `quality.py`, `pauses.py`), measurement (`analyze.py`), pacing, the bake-off kit |
| `tools/audio/synth.py` | Our own sound effects and music (no licences needed) |
| `tools/episode/` | Planning (next episode, trending topics, random draws), the claim ledger and variety checks, preflight, script and beat linters, sound-cue timing, the one-command build, review frames, the listening sheet, the performance summary, the final gate |
| `.claude/agents/`, `.claude/workflows/episode.js`, `.claude/skills/episode/` | The 8-agent pipeline behind `/episode` ([docs/PIPELINE.md](docs/PIPELINE.md)) |
| `.claude/skills/ffmpeg-shorts/` | Tested FFmpeg scripts: mix, encode, quality gate |
| `assets/` | Channel voices, sound effects, music |
| `docs/branding/` | Avatar and banner |
