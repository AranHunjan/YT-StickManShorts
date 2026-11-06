# Handoff: Kip N Dex (YouTube Shorts automation)

## Project
Daily ~55 s animated stick-figure Shorts: "the hidden stories of everyday things".
Channel name: **Kip N Dex**. Handle **@KipNDex** is created on YouTube, TikTok, Instagram and Facebook.
Goal: monetize. Budget: $0 until the first revenue (owner only has a Claude subscription).
Owner reviews every output. Owner writing preference: no em dashes.

## Repo
github.com/AranHunjan/YT-StickManShorts, branch **claude/friendly-bell-gfy18v**
(contains all earlier work from `claude/affectionate-newton-qgh914`; nothing merged yet).
Read first: README.md, docs/PLAN.md, docs/CHARACTERS.md, docs/VOICE.md, docs/SCRIPTING.md,
docs/FACT_BANK.md, docs/PUBLISHING.md, docs/CHANNEL.md, episodes/001/*.

## Owner's PC (run everything locally on it)
Windows 64-bit, Ryzen 7 3700X (8 cores), 16 GB RAM, RTX 2070 SUPER (8 GB; no fast bfloat16, use float16), about 110 GB free.
Earlier sessions ran in a cloud sandbox on CPU (slow, burned usage). Use the local GPU now.
Note: the setup and pipeline were only tested on Linux CPU, so the first Windows run may need small fixes.

## Setup on the PC (one time)
1. Git, Node.js 22, ffmpeg (`winget install Gyan.FFmpeg`), an up-to-date NVIDIA driver.
2. Clone the repo and check out the branch.
3. `cd packages\animator && npm install`
4. `powershell -ExecutionPolicy Bypass -File tools\voice\setup.ps1`
   (creates `tools\voice\.venvs\{kokoro,chatterbox,qwen}` with CUDA torch; first run downloads models)

## Creative decisions (settled)
- **Kip** (orange scarf, cowlick that shows emotion): curious know-it-all. Opens with the hook question,
  blurts a confidently WRONG funny theory, gets corrected, is delighted.
  Voice: Chatterbox cloning `assets/voices/kip.wav`. The owner loves it.
- **Dex** (glasses, teal bow tie): done with Kip's know-it-all attitude but warm and happy to explain; never deadpan.
  Voice: **Qwen3-TTS 1.7B CustomVoice preset "aiden"** plus a persona and per-line emotion instructions,
  set in `assets/voices/voices.json`.
- **Script format** (docs/SCRIPTING.md, based on research):
  - hook question in the first 1-2 s ("Hey Dex... why does X...?")
  - Kip's wrong theory, then Dex's warm correction plus a hint
  - escalation with "but", then the reveal, then a second payoff (something to try)
  - a closing joke that loops into the start
  - 115-130 words; every fact backed by 2 sources (fact.md), hedged where sources disagree
- **Facts:** things people see or use daily, amusing ("wait, really?"); not niche history.
  docs/FACT_BANK.md has 10 verified candidates.
- **Visuals:** notebook-paper style, steady camera (no wobble filter, no shake).
  Captions are word-synced (faster-whisper), 1-3 words per card, current word in the speaker's colour
  (Kip orange, Dex teal), *keywords* highlighted.
  Watermark: "KIP N DEX #NNN" pill top-left plus a faint "@KipNDex" under the characters.
- **Audio:** music and SFX are our own (tools/audio/synth.py), mixed to -14 LUFS.
- **Branding:** avatar (Kip with a magnifying glass, on teal) and banner in docs/branding/.

## Pipeline (per episode, in episodes/NNN/)
1. Write `fact.md`, `script.json` and `beats.json`.
   - `script.json`: `*word*` = highlight; `{57|fifty-seven}` = caption shows 57, voice says fifty-seven.
   - `beats.json`: poses, props and SFX at "Lxx@fraction".
2. Voices:
   `tools\voice\.venvs\chatterbox\Scripts\python.exe tools\voice\speak.py --script episodes\NNN\script.json --out episodes\NNN\audio`
   - generates several takes per line (Chatterbox for Kip; Qwen for Dex, batched, via `tools/voice/qwen_voice.py`)
   - bad-take gate, scores each take against the targets in `analyze.py`, pace stretch capped at 8%, trims silence
   - writes `voice.wav` and `timing.json` (with word timings)
   - `--only L14` regenerates a single line; `QWEN_PYTHON` overrides the Qwen environment path
3. Build: `python tools\episode\build.py N --preview` (sound cues, Remotion render, mix, encode, quality gate).
   `final.mp4` is gitignored; rebuild it locally.
4. Upload using `episodes/NNN/upload.md` and docs/PUBLISHING.md:
   YouTube Studio, Meta Business Suite (Instagram + Facebook in one go), TikTok Studio.
5. Remotion composition ids: register each episode in `packages/animator/src/Root.tsx` (`Ep001`, ...).
   Props live in `src/props/`.

## Lessons learned (don't repeat)
- Never pitch-shift or heavily time-stretch voice references or lines: it causes audible glitchy artifacts
  (measured with Praat: HNR, jitter, shimmer; see docs/VOICE.md).
- Qwen 0.6B CustomVoice ignores instructions; use 1.7B. Batch the lines (much faster).
- Chatterbox needs `setuptools<81`. Kokoro hard-exits if espeak's data path is longer than 160 characters
  (handled in bakeoff.py).
- Remotion: `Config.setColorSpace('bt709')` gives correct yuv420p; fonts are bundled in public/fonts.
- Be efficient with usage: long sessions and polling are expensive.
- The take score is whole-line, so it misses a glitch that lasts half a second (episode 001 L03 scored 97 with
  33% shimmer in one 0.5 s window). Check the worst 0.5 s window (Praat) and the median pitch before accepting a take.
- Qwen takes use fixed seeds (`1000 + take number`): regenerating take 1 reproduces the same audio.
  For fresh takes, run `qwen_voice.py` with a higher `--start`. Some Aiden takes come out pitched far too high
  (230 Hz against his usual ~150 Hz), so check pitch.
- The pace rule reads short lines with a dramatic "..." as slow and stretches them; keep those unstretched.
- SFX: sub-150 Hz sounds plus a noise click read as a digital glitch on phone speakers (old thud). Give low
  sounds a mid-range partial and no raw noise click.

## Current status and next steps
1. **Episode 001 "Why does Heinz ketchup say 57?"** is done and approved by the owner (59.19 s, passed QA).
   Final voicing: L14 comment prompt, Kip L09/L13 re-voiced without the old 15%/9% stretches (L09's pause
   shortened 0.2 s), Dex L03 take q10, softer thud SFX. Line gap 0.16 s, lead 0.30 s.
   `final.mp4` is gitignored: rebuild with `python tools\episode\build.py 1 --preview`.
2. Upload episode 001 to all 4 platforms.
3. Produce episodes 002+ from docs/FACT_BANK.md (tape measure, shopping cart, Coke bottle...) to build a
   posting buffer; reuse the episode 001 structure.
4. Later: automated publishing (YouTube Data API, Meta Graph API; TikTok needs an app audit before posts can
   be public) and an analytics feedback loop.
