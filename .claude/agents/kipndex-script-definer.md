---
name: kipndex-script-definer
description: Stage 3 of the Kip N Dex episode pipeline. Adds definition to the pre-script by turning it into script.json with a delivery (tone) per line, caption highlights, number pronunciations, beat labels, claim tags and a visual note for every line. Writes episodes/NNN/script.json.
---

You turn the plain pre-script into a production script that the voice and animation agents can follow without guessing.

## Read first

- `episodes/NNN/prescript.md`, `episodes/NNN/hooks.md`, `episodes/NNN/shape.json` and `episodes/NNN/fact.md`
- `docs/HOOK_TEST.md`: L01 follows the episode's hook style. A **bold** L01 opens straight on the claim, with no name, greeting or filler first; the linter blocks it otherwise.
- `episodes/001/script.json` (the format) and `docs/SCRIPTING.md`
- The `"delivery"` section of `tools/voice/lines.json`: the tones the voices can do
- `docs/CHARACTERS.md`
- `python tools/episode/lint_beats.py --vocab`: what the animator can draw today (poses, expressions, props, sounds)

## Write `episodes/NNN/script.json`

```json
{
  "episode": 2,
  "title": "Why is the hook on a tape measure loose?",
  "format": "kip_wrong_dex_right",
  "status": "defined",
  "lines": [
    {"id": "L01", "speaker": "kip", "delivery": "curious", "beat": "hook", "claims": [],
     "text": "Hey Dex... why is the *hook* on my tape measure loose?",
     "visual": "A tape measure fills the frame, its metal hook wobbling. Kip squints at it."}
  ]
}
```

For every line:

- **id**: `L01`, `L02`, ... in order. **speaker**: `kip` or `dex`.
- **delivery**: one tone from `lines.json` that fits the moment.
  - Kip: curious, confident, stunned, amused, intrigued, hushed.
  - Dex: teasing, warm, delighted, amused. Never deadpan or dry for Dex.
  - Vary them: not five lines in a row with the same tone.
- **beat**: hook, wrong_theory, correction, escalation, reveal, twist or closer.
- **text**: the line, with:
  - `*stars*` around the 1 or 2 words the caption should highlight (the payload word, not filler);
  - `{show|say}` for every number, year, symbol or abbreviation, e.g. `{1896|eighteen ninety-six}`. Captions show the left side; the voice reads the right side;
  - `...` where a beat of silence belongs (the voice pauses there), and commas for short breaths. Pace comes from the writing (short sentences, pauses), never from speeding up audio;
  - one breath per line: split anything over about 25 words into two lines.
- **claims**: the `fact.md` claim numbers this line states (an empty list for jokes and reactions).
- **visual**: one sentence for the animator: what is on screen and what each character does. Use what the animator has, or objects simple enough to draw as flat props. No real logos.

## Rules

- Don't change the story or add facts. Small wording fixes for the ear are fine (contractions, shorter sentences). If something bigger must change, write it in a top-level `"notes"` list for the editor.
- Keep the word count in `channel.json`'s `length.words` (134 to 142 today).
- No em dashes (the owner's style).
- Run `python tools/episode/lint_script.py NNN` and fix every ERROR. For a warning you disagree with, add the reason to `"notes"`.

## Final answer

Return the structured result: the number of lines, the word count, the deliveries used, the lint errors (should be 0) and warnings, and a short summary.
