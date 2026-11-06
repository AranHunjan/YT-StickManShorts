# The episode pipeline: 8 agents

One command makes a whole episode: `/episode` in Claude Code. Eight agents take turns, each with one job. Two of them only check, and send work back when something is wrong. The owner watches the result and uploads it.

```
 1 Fact finder ─▶ 2 Hook writer ─▶ 3 Script definer ─▶ 4 Script finalizer
                                                              │
                     ┌──── fixes (up to 3 rounds) ────┐       ▼
                     ▼                                │
              5 Audio producer ─▶ 6 Audio checker ────┘
                                        │ pass
                                        ▼
              7 Animator ─▶ 8 Final checker ─▶ READY: the owner watches and uploads
                   ▲              │
                   └── fixes ─────┘  (text → 4, script → 4 → 5 → 6, audio → 5 → 6, visual → 7; up to 2 rounds)
```

| # | Agent | Its job | Writes |
|---|---|---|---|
| 1 | `kipndex-fact-finder` | Picks the topic: something trending, a random draw, or the owner's idea. Proves every claim in a claim ledger: 2 independent sources it actually opened, each with its type and a supporting quote, primary sources preferred | `fact.md`, updates `docs/FACT_BANK.md` |
| 2 | `kipndex-hook-writer` | Writes 10+ hooks in the episode's hook style (the hook test), scores them, picks one, chooses a story shape that differs from recent episodes, and drafts the story | `hooks.md`, `shape.json`, `prescript.md` |
| 3 | `kipndex-script-definer` | Adds definition, line by line: tone (delivery), caption highlights, how numbers are said, beat labels, which claim each line states, and what's on screen | `script.json` |
| 4 | `kipndex-script-finalizer` | The editor: fact-checks every line, runs the SCRIPTING.md checklist, marks the script final, and writes the upload kit | `script.json` (final), `upload.md` |
| 5 | `kipndex-audio-producer` | Sets the audio environment and tone from the script: deliveries, pauses before and inside lines, music bed and level. Then records both voices | `audio/` (voice, lines, timing, word timings) |
| 6 | `kipndex-audio-checker` | Checks the voices sound human and the gaps are natural. Sends specific fixes back to the producer | `audio/audio_check.json`, `audio/audio_review.md` |
| 7 | `kipndex-animator` | Writes the beat sheet timed to the words, with the listener reacting mid-line (tilts, nods, laughs, double-takes), draws any new props, renders, mixes and encodes | `beats.json`, new props, `final.mp4`, `preview.mp4` |
| 8 | `kipndex-final-checker` | Last check before upload: the gate, the frames, the facts, the upload kit. Sends each fix to the stage that owns it, and makes the owner's listening sheet | `review.md`, `listening.md` |

All files are in `episodes/NNN/`. Channel-wide settings (length limits, the hook test, the share of trend days, how different episodes must be) are in `channel.json` at the repo root.

## How each episode is planned

`tools/episode/plan_next.py` decides three things before the agents start, from `channel.json`:

- **The episode number:** the next free one.
- **The hook style:** "question" (Kip's "Hey Dex... why...?") or "bold" (the surprising claim first, no name). Episodes 2 to 13 alternate them to test which keeps more viewers ([HOOK_TEST.md](HOOK_TEST.md)).
- **The topic mode:** on **trend** days the fact finder looks for an everyday object inside something trending: Google Trends in 5 countries, Wikipedia's most-read pages, memes, upcoming holidays (`tools/episode/topics.py trends`). On **random** days it starts from a truly random draw of everyday objects (`topics.py random`). Half the days are trend days by default, in pairs, so both hook styles get the same mix.

Along the way the pipeline also:
- **Keeps episodes varied.** Each episode records its shape: hook formula, story structure, humour, how Kip and Dex interact, visual style and ending (`shape.json`). The linter blocks a copy of a recent episode and warns on near-copies (`tools/episode/variety.py`). This is also our protection against YouTube's rule on mass-produced, repetitive content ([AI_LABELS.md](AI_LABELS.md)).
- **Proves facts properly.** The claim ledger records, for every claim, what kind of claim it is (for dates: invented, patent filed, patent granted, first sold...), each source's type, the exact supporting passage and any qualification (`tools/episode/claims.py`).
- **Keeps the characters moving.** On every line of 4 s or more the listener reacts, and nothing on screen holds still for more than 3.5 s (`tools/episode/lint_beats.py`). The camera stays steady.
- **Lands just over a minute.** Every new episode lasts 60.3 to 61.0 s with its end hold, so TikTok counts it as over 1 minute. The end hold stretches from 0.9 to 1.6 s as needed, and the gaps between lines do the rest (`channel.json`).
- **Asks the owner to listen.** The measurements can't tell whether a line sounds natural or funny, so `listening.md` lists the flagged lines plus a small sample for the owner to score 1 to 5 on five points.

**After posting**, `/performance` (a separate command, not a ninth agent) compares how episodes did with how they were made, and writes recommendations to [INSIGHTS.md](INSIGHTS.md). Nothing changes until the owner adopts one.

## How to run it

In Claude Code, from the repo:

| You say | What runs |
|---|---|
| `/episode` | A new episode, start to finish |
| `/episode about shopping carts` | Same, with that topic if it passes the fact checks |
| `/episode, something trending` / `/episode, a random one` | Overrides the day's topic mode |
| `/episode, but let me read the script first` | Stops after stage 4; say "carry on with episode 2" to continue |
| `/episode redo episode 2's audio` | From stage 5 onwards |
| `/episode just re-check episode 2` | Stage 8 only, plus any fixes it asks for |

The `/episode` skill runs `python tools/episode/preflight.py` first, so a missing tool fails in seconds. It then starts the saved workflow (`.claude/workflows/episode.js`) in the background.

Voice generation and rendering are the slow parts. Rendering episode 001 takes about 2 minutes on the RTX 2070 PC.

## How the checks work

### The audio checker (stage 6)

No agent can listen. The checker measures what makes text-to-speech sound broken or robotic, using `tools/voice/check_audio.py` and `tools/voice/quality.py`:

| Check | What it catches | Result |
|---|---|---|
| Transcript (Whisper) vs script | Garbled, skipped or extra words; numbers not heard | 1 word off: listen. More: regenerate |
| Hum in a pause | A quiet buzz or growl between words: the episode 001 L03 glitch | Regenerate |
| Pitch | A take pitched far from the voice's normal range (Qwen's Aiden sometimes comes out at ~230 Hz) | Regenerate |
| Praat roughness (jitter, shimmer, worst 0.5 s window) | Glitchy or over-processed takes | Listen or regenerate |
| Pauses inside a line | A pause in the middle of a phrase (over 0.3 s), or dead air at punctuation (over 0.8 s) | Regenerate, or cap the pause |
| Gaps between lines | Too slow or crammed turn-taking. People leave about 0.2 s between turns ([Stivers et al. 2009](https://www.pnas.org/doi/10.1073/pnas.0903616106)); episode 001 has 0.20 to 0.28 s | Adjust `pause_before` |
| Loudness, clipping, pace, flatness | A line jumping out, distortion, rushing or dragging, a monotone read | Regenerate or change the delivery |
| Length | Over 60 s with the end hold | Back to the script |

The thresholds were calibrated on episode 001. Its 14 approved lines pass with no failure, while the 3 takes that were rejected by ear are flagged: the glitchy Dex L03 fails on hum, and the over-stretched Kip L09 and L13 get roughness warnings. Lines the checker can't be sure about are listed for the owner to listen to; that list is in `audio/audio_review.md` and `review.md`.

`speak.py` runs the same glitch checks on every take while recording, so most bad takes never reach the checker.

### The final checker (stage 8)

- `tools/episode/check_episode.py` blocks the upload when:
  - a file is missing;
  - the script or beat linter has errors;
  - the audio check failed, or ran on a different voice track;
  - `final.mp4` is older than the audio, or fails the Shorts quality gate (loudness, length, codecs, silences, black frames);
  - a claim isn't verified, the claim ledger fails `claims.py`, or the topic repeats an old episode;
  - the upload kit is missing a source link, has an overlong title, em dashes or placeholders.
- It warns when the upload kit doesn't state each platform's AI label setting, and while `listening.md` isn't scored yet.
- `tools/episode/review_frames.py` saves the first half second (the mute test) and one frame per line, with the Shorts UI zones shaded red. The agent looks at them for captions, overlaps and the right image for each line.
- It re-reads the script against the fact sheet one last time.

## What the owner still does

1. Optional: read the script before recording (`until: "finalize"`).
2. Watch `preview.mp4`, listen to the lines in `listening.md`, and fill in its 1 to 5 scores.
3. Upload with `upload.md` and [PUBLISHING.md](PUBLISHING.md), including each platform's AI label setting. The pipeline never posts anything.
4. 7 days after posting, add the numbers to `analytics/performance.csv`, and run `/performance` every week or so.

## Tools the agents use

| Tool | What it does |
|---|---|
| `tools/episode/plan_next.py` | The next episode's number, hook style, topic mode and the recent shapes |
| `tools/episode/topics.py trends` / `random` | Trending lists (Google Trends, Wikipedia most-read), or a random draw of everyday objects |
| `tools/episode/claims.py N` | The claim ledger: sources, passages, source types, date kinds |
| `tools/episode/variety.py [N]` | Episode shapes, and how episode N compares with recent ones. `--vocab` lists the usual values |
| `tools/episode/listening.py N` | Creates the owner's listening sheet, or reads its scores |
| `tools/episode/performance.py` | Performance data joined with how each episode was made (behind `/performance`) |
| `tools/episode/preflight.py [--fix]` | Is the PC ready? Finds the voice environments (in a worktree too), checks ffmpeg, Node, Whisper, Praat and the GPU; `--fix` installs the animator's packages |
| `tools/episode/lint_script.py N` | The script against SCRIPTING.md and fact.md: markup, deliveries, claims, hook length, word count, em dashes |
| `tools/episode/lint_beats.py N` | The beat sheet against what the animator can draw: poses, expressions, gestures, prop kinds, sounds, time refs, safe zones, listener reactions, long still stretches. `--vocab` lists everything available |
| `tools/voice/speak.py` | Records the voices. `--only L03 --fresh` re-takes lines with new seeds, `--resume` continues after a timeout, `--assemble` re-joins after pause changes. Per line: `pause_before`, `max_pause` |
| `tools/voice/check_audio.py episodes/NNN` | The audio checker's measurements |
| `tools/voice/quality.py`, `tools/voice/pauses.py` | Glitch detection; finding and shortening pauses |
| `tools/episode/register.py` | Registers every episode with Remotion (Ep001, Ep002, ...). `build.py` runs it |
| `tools/episode/build.py N --preview` | Cues, render, mix, encode, quality gate. `--no-render` for sound-only changes. The music bed comes from `script.json` `"sound"` |
| `tools/episode/review_frames.py N` | Frames for the visual check |
| `tools/episode/upload_files.py N` | `captions.srt` (exact-word subtitles) and `cover.jpg` for the uploads. `build.py` runs it |
| `tools/episode/check_episode.py N` | The final gate |
| `tools/envs.py chatterbox` | Prints the voice environment's Python. Voice tools run with it: `$(python tools/envs.py chatterbox) tools/voice/check_audio.py episodes/002` |

## The nightly run

A scheduled task in the Claude app, "Kip N Dex nightly episode", makes one episode every night at 3 AM, while nobody is using the plan's limits:

- It checks the plan limits first. If the 5-hour window is already in use, it waits for the reset; if the weekly limit is nearly used up, it skips the night.
- It runs `preflight.py`, then `/episode` with `plan_next.py`'s plan. If the newest episode was left unfinished, it continues that one instead.
- It never uploads, posts or commits. In the morning: watch `preview.mp4`, score `listening.md`, upload with `upload.md`.
- The computer has to be on, with the Claude app open, at 3 AM. If the app is closed, the run happens the next time it opens. The app keeps the computer awake while a run works, but it can't wake a sleeping computer.

## Running in a worktree

Claude Code sessions often run in a git worktree under `.claude/worktrees/`. The voice environments and the animator's packages are gitignored, so they exist only in the main checkout:
- the voice tools find the main checkout's environments automatically;
- `preflight.py --fix` installs the animator's packages into the worktree from npm's cache (about 15 seconds);
- `build.py` reuses the main checkout's downloaded render browser.
