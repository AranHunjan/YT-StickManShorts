# How we write a Kip N Dex script

This is condensed from the research agent's report (2026-11-05). Sources are inline.

## Principles

1. **Viewers decide in 1 to 2 seconds.**
   - An animator on Zack D. Films says each Short must "grab attention within the first 1 to 2 seconds" ([Reilly](https://supersets.chrisreillyportfolio.com/zackdfilms.php)).
   - In Paddy Galloway's study of 5,400 Shorts, videos where under 60% of viewers chose to watch (rather than swipe away) rarely did well; winners sat at 70 to 90% ([thread](https://threadreaderapp.com/thread/1646898356419981315.html)).
2. **The hook must work on mute and as a thumbnail.** YouTube's advice: "Start with a question, a surprising fact, or a visually captivating moment" ([YouTube Blog](https://blog.youtube/creator-and-artist-stories/transitioning-your-long-form-content-to-youtube-shorts/)).
3. **Name the everyday object and ask How or Why.** 55% of Zack D. Films' recent titles start with How, Why, Can or What, and everyday objects are among his biggest hits ([channel](https://www.youtube.com/@zackdfilms/shorts)).
4. **Open a curiosity gap, then hint at what's coming within 3 seconds** ([Loewenstein 1994](https://www.cmu.edu/dietrich/sds/docs/loewenstein/PsychofCuriosity.pdf); Jenny Hoyos on [Creator Science](https://creatorscience.com/podcast/jenny-hoyos/)).
5. **Join beats with "but" or "so", never "and then"** ([South Park rule](https://thewrap.com/south-park-creators-visit-nyu-class-lessons-storytelling-30806); [vidIQ on Hoyos](https://vidiq.com/blog/post/how-jenny-hoyos-gets-10m-views-per-youtube-short/)).
6. **Pace it like a rollercoaster.** Fast hook, a medium middle, a joke at the peak, a quick end. Write at a 5th-grade reading level.
7. **A wrong guess, then the right answer, teaches better than a clean explanation.** In Derek Muller's studies, videos that voice a common misconception and then correct it beat polished explanations ([summary](https://thejournal.com/articles/2015/05/05/watching-videos-does-not-necessarily-lead-to-learning.aspx)). That's Kip's job. Humour should illustrate the concept, and Dex stays warm, never sneering ([review](https://www.facultyfocus.com/articles/effective-teaching-strategies/humor-in-the-classroom-40-years-of-research/)).
8. **End right after the payoff, and loop.**
   - Hoyos cut one second from an ending and retention rose from 83% to 88%.
   - Replays count as Shorts views ([TechCrunch](https://techcrunch.com/2025/03/26/youtube-is-changing-how-youtube-shorts-views-are-counted)).
9. **Calls to action are unproven.** By default: no outro and no "subscribe".
10. **Captions are subtitles, not spoilers.**
    - Sync them word by word, 1 to 3 words at a time, and never show words before they're spoken.
    - Give each speaker a colour, and give the punchline its own card ([BBC subtitle guidelines](https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/)).
11. **Length: just over a minute,** 60.3 to 61 s with the end hold, so TikTok counts it as over 1 minute (`channel.json`). That's 134 to 142 words; episode 001 was 135 words and 59.2 s.

## Hook formulas

Since 2026-11-06 the opener is being tested ([HOOK_TEST.md](HOOK_TEST.md)): formula 1 is the "question" style, and formulas 2 to 7 and 9 are the "bold" style, where the first words carry the surprise and no name or filler comes first. Each episode's style comes from `tools/episode/plan_next.py`.

1. "Hey Dex... why does your [object] have [odd detail]?"
2. "That [detail] isn't for the [object]. It's for *you*."
3. "You touch [object] every day and never noticed [detail]."
4. "Everyone thinks [detail] is for [common belief]. It isn't." (built for Kip)
5. "There are two [holes] on your [object]. Only one is for the [object]."
6. "Your [object] still has [detail] for something almost nobody owns anymore."
7. "[Object] looks like this because of [one guy in 18xx]."
8. Visual first: frame 1 is the odd detail, big, with the question as the first caption.
9. "You've been [using object] wrong your whole life." (the episode's best payoff, moved to the front)

## Beat template (about 59 s of speech, 134 to 142 words)

| # | Beat | Time | Words | Rules |
|---|---|---|---|---|
| 1 | Hook question (Kip) | 0-3 s | 6-10 | Object + odd detail; show the detail big in frame 1 |
| 2 | Kip's confident wrong theory | 3-7 s | 8-14 | One joke, animated literally |
| 3 | Dex's warm correction + hint | 7-11 s | 8-12 | Amused, kind; tease what's coming |
| 4 | Escalation ("but...") | 11-20 s | 15-22 | Raise the stakes |
| 5 | Reveal | 20-32 s | 20-28 | Plain answer + one checkable specific; Kip reacts |
| 6 | Twist ("here's the best part") | 32-46 s | 22-30 | A second payoff, ideally something to try |
| 7 | Closing joke + loop | 46-56 s | 12-18 | A callback; the last line runs into line 1; cut within 0.5 s |

## Variety

Two episodes about different objects can still feel identical if they're told the same way. Each episode records its **shape** in `shape.json`: the hook formula, the story structure, the humour, how Kip and Dex interact, the visual presentation and the ending. `python tools/episode/variety.py --vocab` lists the usual values for each.

- Change at least 2 of the 6 from each of the last 3 episodes; the linter blocks an exact copy and warns at 5 of 6.
- Never use the same hook formula, structure, visual style or ending three episodes in a row.
- The brand doesn't vary: Kip the curious know-it-all, Dex the warm explainer, verified facts, a loop at the end.

## Checklist before recording

- [ ] Line 1 follows the episode's hook style: 10 words or fewer, naming the object and its odd detail. A bold hook carries the surprise in its first words.
- [ ] The shape differs from recent episodes (`python tools/episode/variety.py N`).
- [ ] Mute test: frame 1 plus the caption explain the topic on their own.
- [ ] Kip's wrong theory is one line, 4 s or less, and easy to animate.
- [ ] Dex is amused and kind, with no sneer and no filler.
- [ ] The stakes or hint line lands by about 10 s.
- [ ] Beats join with but/so, never "and also".
- [ ] A second payoff comes after the reveal.
- [ ] Every fact is in the claim ledger with 2 sources (`python tools/episode/claims.py N`), and the script keeps each claim's qualification (which date it is, where sources disagree).
- [ ] 134 to 142 words (`channel.json`).
- [ ] Delete test: cut any line the story still works without.
- [ ] No intro and no "subscribe". The end loops into the start.
- [ ] Captions are word-synced, coloured by speaker, with keywords highlighted.
