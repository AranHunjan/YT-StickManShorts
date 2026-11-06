---
name: episode
description: Make a Kip N Dex episode with the 8-agent pipeline (fact, hooks + pre-script, definition, final script, audio, audio check, animation, final check). Use for "/episode", "make the next episode", "make one about something trending", "make a random one", "make an episode about tape measures", "redo episode 2's audio", "continue episode 2 from the animation", "just re-check episode 2".
---

# /episode

The pipeline is the saved workflow `.claude/workflows/episode.js`. It runs the agents in `.claude/agents/kipndex-*.md` one after another, with check-and-fix loops. The stages are explained in `docs/PIPELINE.md`.

## 1. Preflight

Run `python tools/episode/preflight.py`.
- **NOT READY** and only `packages/animator/node_modules` is missing (normal in a fresh worktree): run `python tools/episode/preflight.py --fix`, which installs from npm's cache.
- Anything else missing: stop and tell the owner what to install (README one-time setup). Don't start the pipeline.

## 2. Work out the arguments

For a new episode, run `python tools/episode/plan_next.py` first. It gives the next episode number, its **hook style** (the hook test alternates "question" and "bold", docs/HOOK_TEST.md) and its **topic mode** ("trend" or "random", from `channel.json`). Pass `episode`, `mode` and `hook_style` from it unless the owner said otherwise.

| Arg | When |
|---|---|
| `episode` | The number the owner named, or plan_next's for a new episode. |
| `topic` | An object or fact the owner asked for ("about tape measures"). It wins over `mode`. |
| `mode` | `trend` or `random`: plan_next's, or the owner's ("make a random one", "something trending"). |
| `hook_style` | `question` or `bold`: plan_next's. Only change it if the owner asks; changing it skews the hook test. |
| `from` | The stage to start at, for redoing part of an existing episode. |
| `until` | The stage to stop after, when the owner wants to review midway. |

Stages, in order: `fact`, `hooks`, `define`, `finalize`, `audio`, `audio-check`, `animate`, `final-check`.

Examples:
- "make the next episode": plan_next says 2, bold, trend: `{episode: 2, mode: "trend", hook_style: "bold"}`
- "make a random one": `{episode: 3, mode: "random", hook_style: "question"}` (style still from plan_next)
- "make one about shopping carts, but let me read the script first": `{episode: 2, topic: "shopping carts", hook_style: "bold", until: "finalize"}`
- "the script's approved, carry on with episode 2": `{episode: 2, from: "audio"}`
- "redo episode 2's audio": `{episode: 2, from: "audio"}`
- "just re-check episode 2": `{episode: 2, from: "final-check"}`

## 3. Run it

Call the Workflow tool with `name: "episode"` and `args` as above (a JSON object, not a string). It runs in the background. Tell the owner it started, and that voice generation and rendering are the slow parts. Don't poll it: you are notified when it finishes.

## 4. Report

When it finishes, start with the outcome in plain words:
- **ready**: the title, then what's left for the owner:
  1. watch `episodes/NNN/preview.mp4`;
  2. listen to the lines in `episodes/NNN/listening.md` and fill in its 1-5 scores (they feed `/performance`);
  3. upload with `episodes/NNN/upload.md` and `docs/PUBLISHING.md`, including each platform's AI label setting;
  4. 7 days after posting, add the numbers to `analytics/performance.csv` (analytics/README.md).
- **needs_human**: what still fails (from `reason`), and which file explains it (`review.md` or `audio/audio_review.md`).
- **paused**: where it stopped and the command to continue (`from` the next stage).
- **stopped**: the error, and whether it's a setup problem (rerun preflight) or a content problem.

Link `review.md`, `preview.mp4` and `upload.md`. Never upload or post anything yourself: publishing stays with the owner.

## If the Workflow tool isn't available

For example in a headless run, run the same stages yourself, in order, with the Agent tool (`subagent_type` = the agent name), passing the episode number, the topic mode and the hook style:

1. `kipndex-fact-finder`
2. `kipndex-hook-writer`
3. `kipndex-script-definer`
4. `kipndex-script-finalizer`
5. `kipndex-audio-producer`, then `kipndex-audio-checker`. On "fix", send the fixes back to the producer: at most 3 rounds.
6. `kipndex-animator`, then `kipndex-final-checker`. Route its fixes:
   - text: finalizer
   - script: finalizer, then producer + checker, then animator
   - audio: producer + checker, then animator
   - animation: animator

   At most 2 fix rounds.
