# Open questions

## Decided on 2026-11-06

| Question | Decision | What changed |
|---|---|---|
| Length | **Just over a minute: 60.3 to 61.0 s**, so TikTok counts it as over 1 minute. | `channel.json` `length`. The end hold stretches from 0.9 up to 1.6 s as needed; scripts are 134 to 142 words. Episode 001 stays 59.2 s. |
| Human voices | The owner offered their and their brother's voices for cloning, on the condition that it removes the AI labels. **It doesn't:** TikTok and Meta still count cloned speech as AI audio. So we keep the current voices, with the labels. | [AI_LABELS.md](AI_LABELS.md) |
| Episode 001's movement | **Starts from episode 002**; 001 stays as approved. | Nothing: new episodes already need listener reactions. |
| Automatic performance data | **Later:** revisit around 2026-11-20. Until then, by hand. | `analytics/README.md` |
| Daily production | **Every night at 3 AM**, or after the 5-hour limit resets. | The scheduled task "Kip N Dex nightly episode" ([PIPELINE.md](PIPELINE.md), "The nightly run") |

## Still open

1. **Recording the lines yourselves.** This is the only way to drop the AI labels on TikTok, Instagram and Facebook. It would take a few minutes a day per voice, and Kip would sound different. Say so if it's ever worth it, and the pipeline gets a recording step.
2. **Usage per episode.** The first nightly runs will show how much of the 5-hour and weekly limits one episode takes. If a week of nightly runs doesn't fit the weekly limit, options are:
   - fewer episodes a week;
   - a lighter model for the mechanical stages (the definer and the audio producer);
   - making two episodes in one window on quiet days.
3. **The hook test and trend share** are set to episodes 2 to 13 alternating, and half the days trending. Both are in `channel.json`.

## What was done with the 2026-11-06 feedback

| Feedback | Decision | Where |
|---|---|---|
| More movement | Built: mid-line reactions and gestures, required on long lines | `rig/gestures.ts`, `lint_beats.py`, the animator agent |
| Stronger opening | A test of question vs bold openers, episodes 2 to 13 | [HOOK_TEST.md](HOOK_TEST.md) |
| Trending topics, some random days | Built into the fact finder, with free trend lists and a random draw | `topics.py`, `plan_next.py` |
| AI labels | Researched: YouTube no; TikTok and Meta yes, for the AI voices | [AI_LABELS.md](AI_LABELS.md) |
| Human listening score | Built: `listening.md` per episode | `listening.py` |
| Claim ledger | Built: kind of claim, source types, passages, qualifications | `claims.py` |
| Originality beyond the topic | Built: episode shapes, copies blocked | `variety.py` |
| Performance feedback (a ninth agent) | Built as the `/performance` command instead | `performance.py`, `analytics/` |
| Don't add agents | Followed: still 8 agents | |
| TikTok's 1-minute rule | Length is now just over a minute | `channel.json` |
