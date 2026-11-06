# Hook test: question vs bold

**Why:** feedback on episode 001 said the first second goes on a name ("Hey Dex..."), and a "why" question isn't surprising on its own. Episode 001's best hook, that the 57 is where you're supposed to tap, arrives at 40 s. A bold opener like "You've been opening ketchup wrong your whole life" may stop more swipes. The "Hey Dex... why" opener came out of our own research (`docs/SCRIPTING.md`), so instead of switching, we test both.

## The two styles

| Style | Line 1 | On episode 001's topic |
|---|---|---|
| **question** (the current format) | Kip asks "Hey Dex... why does [object] have [odd detail]?" | "Hey Dex... why does Heinz ketchup say 57 on the bottle?" |
| **bold** | The surprising claim or payoff in the very first words, with no name, greeting or filler first | "You've been opening ketchup wrong your whole life." |

Both styles: 10 words or fewer, literally true, paid off in the video, and frame 1 shows the odd detail big. The bold formulas are listed in `python tools/episode/variety.py --vocab` (for-you, never-noticed, myth-bust, doing-it-wrong, two-things, leftover, origin-person, big-number). The script linter blocks a bold hook that starts with a name or a filler word.

## Schedule

Set in `channel.json` (`hook_test`), and applied by `tools/episode/plan_next.py`:

- Episodes 2 to 13: even episodes are **bold**, odd ones **question**.
- Topic modes go in pairs (2 and 3 trend, 4 and 5 random, and so on), so both styles get the same mix of trending and random topics: 3 episodes of each combination.

## Measuring

- **The number that matters:** YouTube Studio's "Viewed vs. swiped away", the share of people who chose to keep watching. That is what a hook decides.
- **Second:** the average percentage viewed.
- Record both 7 days after posting in `analytics/performance.csv` (`analytics/README.md`). `/performance` compares the two styles.

## Deciding

After episode 13 (6 episodes per style), a style wins if it's ahead on "viewed" by more than the spread within each style. The owner then sets `hook_test.winner` in `channel.json`, and every episode uses that style. Until then, `plan_next.py` keeps alternating and says the test is over.

Keep everything else steady during the test: posting time, length and title format. Six episodes per style is a small sample, and topics vary a lot, so treat a small gap as a tie.
