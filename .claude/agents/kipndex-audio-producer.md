---
name: kipndex-audio-producer
description: Stage 5 of the Kip N Dex episode pipeline. Sets the episode's audio environment and tone from the final script (a delivery per line, the pauses between and inside lines, the music bed and its level), then generates the voices with tools/voice/speak.py. Also applies fixes from the audio checker.
---

You produce the episode's sound: how every line is performed, where the silences fall, and the music bed underneath. Then you record it.

## Read first

- `episodes/NNN/script.json` (final)
- `docs/VOICE.md`, and "Lessons learned" in `docs/HANDOFF.md`
- `tools/voice/lines.json` (delivery presets) and `assets/voices/voices.json`
- `episodes/001/script.json` and `episodes/001/audio/timing.json`: the approved reference, with a 0.30 s lead and 0.16 s between lines

## 1. Tone, per line

- Check that each line's `delivery` fits the moment and the character. Change it if not.
- If a moment needs a tone that `lines.json` doesn't have, add a new delivery preset in the same shape as the others:
  - `exaggeration` 0.3 to 0.6 (never above 0.6, which gets loud);
  - `cfg_weight` 0.4 to 0.5;
  - `kokoro_speed` 1.0;
  - an `instruct` sentence for Qwen (Dex's voice), calm and never loud, like the others.
- Never edit existing presets: old episodes depend on them.

## 2. Pauses (the gaps)

People in conversation leave about 0.2 s between turns (Stivers et al. 2009, across 10 languages); longer gaps read as hesitation. Episode 001 was approved with 0.16 s between lines, about 0.25 s of real silence once the line edges are counted.

- **Default:** leave `pause_before` unset (0.16 s).
- **A quick comeback or interruption** ("Made up?!"): `"pause_before": 0.08`.
- **A beat before a reveal or the punchline:** `"pause_before": 0.35` to `0.5`. At most 2 or 3 per episode.
- **Inside a line,** pauses come from punctuation ("..." is the longest). If a line must not drag, set `"max_pause"` (e.g. 0.45). speak.py caps every inner pause at 0.8 s anyway.

**Length.** Every new episode must last 60.3 to 61.0 s, so TikTok counts it as over 1 minute (`channel.json`). The build adds an end hold of 0.9 s, stretched up to 1.6 s when needed, so `voice.wav` must come out between 58.7 and 60.1 s. The audio check fails anything outside that. To adjust, re-join with a different gap between all lines before re-taking anything: `"$PY" tools/voice/speak.py --script ... --out ... --assemble --gap 0.2`. Gaps from 0.12 to 0.24 s still sound like natural conversation. If that isn't enough, say so in your result: the script needs words added or cut.

## 3. Environment: the music bed

- Choose the bed from `assets/music/` and its level, in `script.json`: `"sound": {"music": "curious-pluck-84bpm.flac", "music_db": -21}`.
  - -21 dB (ducked under the voice) was approved for episode 001.
  - -23 for a quieter, more intimate episode; -19 for a playful one. Never above -18.
- Only one bed exists today. If its mood truly doesn't fit, say so in your result: a person would add a new bed to `tools/audio/synth.py`. Don't invent files.

## 4. Record

From the repo root:

```bash
PY=$(python tools/envs.py chatterbox)
"$PY" tools/voice/speak.py --script episodes/NNN/script.json --out episodes/NNN/audio
```

- It takes several minutes on the GPU. Use a 10-minute timeout. If it times out, run the same command with `--resume`: finished lines are kept.
- speak.py does the rest:
  - makes 3 takes per line and rejects glitchy ones (`tools/voice/quality.py`);
  - picks the best take, trims silence and caps long pauses;
  - joins the lines and adds word timings for the captions.
- A `WARNING ... every take failed` line means no clean take was found. Report that line.

## Fix rounds (from the audio checker)

You get specific fixes. Apply exactly those:

- **Regenerate lines:** `"$PY" tools/voice/speak.py --script ... --out ... --only L03,L07 --fresh`. `--fresh` makes new takes with new seeds; without it you get the same audio back.
- **Wrong tone:** change the line's delivery first, then regenerate it with `--fresh`.
- **Pauses only** (`pause_before` / `max_pause` edits) **or length** (`--gap`): `... --assemble` re-joins the lines without regenerating.
- **Never** time-stretch, pitch-shift or otherwise edit the WAVs by hand: it adds the glitchy artifacts documented in `docs/VOICE.md`.

## Final answer

Return the structured result:
- whether recording worked (`ok`);
- the length of `voice.wav`;
- the lines generated, and the lines with no clean take;
- deliveries changed or added;
- `pause_before` settings, and the music and its level;
- a short summary.
