---
name: performance
description: Review how Kip N Dex episodes performed (analytics/performance.csv) against how they were made (hook style, shape, trend or random topic, listening score), and write recommendations to docs/INSIGHTS.md. Use for "/performance", "how are the episodes doing", "which hook style is winning", "what should we change". Recommends only; never changes channel.json, the agents, the scripting guide or any episode.
---

# /performance

The performance review. It's a separate command, not a stage of `/episode`: run it weekly, or after every few new rows of data.

1. Run `python tools/episode/performance.py`, which covers YouTube, where the hook test is measured. If other platforms have rows, also run it with `--platform tiktok`, `instagram` or `facebook`.
   - No rows yet: tell the owner how to fill in `analytics/performance.csv` (`analytics/README.md`: 7 days after posting) and stop.
2. Read the output, plus `script.json`, `shape.json`, `fact.md` and `listening.md` of the episodes with data. Read the scripts of the best and the worst episodes closely.
3. Rewrite the "Latest review" section of `docs/INSIGHTS.md`, and leave the "Adopted" section exactly as it is:
   - **Hook test:** question vs bold on "viewed vs swiped away" and average % viewed, with n per style. It's decided only with at least 5 episodes per style and a gap bigger than the spread within each style. If it's decided, recommend setting `hook_test.winner` in `channel.json`; don't set it yourself.
   - **Where viewers leave:** the drop-off seconds, the line and beat being spoken (the tool maps them), and what those lines have in common: too long, a slow setup, a weak joke, a hard word.
   - **What gets shared:** shares per 1,000 views by topic, trend vs random, and shape.
   - **Dialogue patterns:** line lengths, interaction style and humour type of the best vs the worst episodes.
   - **Listening scores** vs performance: do the lines the owner scored low match the drop-offs?
   - **Recommendations:** at most 5. Each gives its evidence and how sure it is. With fewer than 3 episodes per group, confidence is low; say so.
4. Tell the owner the top 3 recommendations in plain words. Nothing changes until they move a recommendation into "Adopted" (the writing agents read that section) or change `channel.json`.

Never change `channel.json`, the agents, `docs/SCRIPTING.md` or any episode yourself. The audience informs the strategy; the owner sets it.
