# Kip N Dex (@KipNDex)

A daily animated Short about the hidden stories of everyday things, made almost entirely on one PC for $0.

- **Plan and decisions:** [docs/PLAN.md](docs/PLAN.md)
- **Characters:** [docs/CHARACTERS.md](docs/CHARACTERS.md)
- **Voices:** [docs/VOICE.md](docs/VOICE.md)
- **Channel setup:** [docs/CHANNEL.md](docs/CHANNEL.md)
- **Posting to YouTube, Instagram, Facebook and TikTok:** [docs/PUBLISHING.md](docs/PUBLISHING.md)

## Making an episode (Windows, from the repo root)

One-time setup: Node.js 22, ffmpeg (`winget install Gyan.FFmpeg`), `cd packages\animator && npm install`, and the voice environment (`tools\voice\setup.ps1`).

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
3. **Preview the animation (optional):** `cd packages\animator && npm run studio`, then open `Ep001`.
4. **Build the finished video:** renders, mixes voice + music + SFX at -14 LUFS, encodes, and runs the quality gate:
   ```powershell
   python tools\episode\build.py 1 --preview
   ```
5. **Review** `episodes\001\final.mp4`, then post it using `episodes\001\upload.md` and [docs/PUBLISHING.md](docs/PUBLISHING.md).

## Layout

| Path | What |
|---|---|
| `episodes/NNN/` | One folder per episode: fact sheet, script, beats, audio, final video, upload kit |
| `packages/animator/` | Remotion: the stickman rig, props, captions, watermark, the episode compositions |
| `tools/voice/` | Voice generation (`speak.py`), measurement (`analyze.py`), pacing, the bake-off kit |
| `tools/audio/synth.py` | Our own sound effects and music (no licences needed) |
| `tools/episode/` | Sound-cue timing and the one-command build |
| `.claude/skills/ffmpeg-shorts/` | Tested FFmpeg scripts: mix, encode, quality gate |
| `assets/` | Channel voices, sound effects, music |
| `docs/branding/` | Avatar and banner |
