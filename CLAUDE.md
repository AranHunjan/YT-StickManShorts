# Kip N Dex

Daily animated YouTube Shorts: Kip and Dex, two stick figures, explain the hidden stories of everyday things. Status and lessons learned: `docs/HANDOFF.md`. Plan: `docs/PLAN.md`.

## Making episodes

- `/episode` runs the 8-agent pipeline described in `docs/PIPELINE.md`. The agents are `.claude/agents/kipndex-*.md`; the orchestration is `.claude/workflows/episode.js`.
- Check the PC first: `python tools/episode/preflight.py`.
- Channel-wide settings (length cap, the hook test, the share of trend days, variety rules) live in `channel.json`. `python tools/episode/plan_next.py` turns them into the next episode's plan.
- `/performance` reviews how episodes did (`analytics/performance.csv`) and writes recommendations to `docs/INSIGHTS.md`. Agents follow only its "Adopted" section.
- Open decisions for the owner: `docs/OPEN_QUESTIONS.md`.

## House rules

- No em dashes in anything written for the owner or the audience.
- Every fact needs 2 independent sources in the episode's `fact.md`. The script may only say verified claims.
- Never pitch-shift or time-stretch voice lines or reference clips: it causes audible glitches (`docs/VOICE.md`).
- Dex is warm and amused, never deadpan. The camera stays steady.
- Never upload or post anything: publishing stays with the owner.
- AI labels: answer each platform's question truthfully (`docs/AI_LABELS.md`). Never strip watermarks or metadata to avoid a label.

## Running things (Windows, from the repo root)

- Voice tools run in the Chatterbox environment: `"$(python tools/envs.py chatterbox)" tools/voice/speak.py ...`. This works in a worktree too, because the environments live in the main checkout.
- Build a video: `python tools/episode/build.py N --preview`.
