# Character bible (v1, for review)

Everything here is a proposal. Change anything, and the rig code follows this file.

## The show in one line

**Kip**, a curious stickman who is sure he already knows how the world works, keeps finding out the wild true story behind everyday things. **Dex**, his deadpan friend, always brings the receipts.

Working channel name: **Stick to the Facts**. Check that the name and handle are free on YouTube, TikTok and Instagram before we commit. Backups: "Kip Finds Out", "The Everyday Files".

## Kip (the lead)

| | |
|---|---|
| Role | Asks, guesses, tries things, gets it wrong, gets mind-blown. Narrates most episodes. |
| Personality | Endlessly curious, impulsive, a little overconfident, genuinely delighted to be proven wrong. Never mean, never dumb: he is the viewer's stand-in. |
| Signature look | Classic ink stick figure with a slightly oversized round head, plus two ownable details. |
| 1. The cowlick | One curl of hair on top that works as an **emotion meter**. It springs straight up when he's mind-blown, droops when he's sad, bends into a question mark when he's confused, and wiggles when he's excited. Readable even as a tiny thumbnail. |
| 2. The orange scarf | Brand colour (`#FF6B1A`). Its tail flows when he moves, so the screen is never static. |
| Catchphrase | "Excuse me?!" at the mind-blown moment. Used in about half the episodes, never every time. |
| Voice | Energetic, warm, fast-talking, a slightly raspy late-20s voice. Expressive: gasps, laughs, whispers. |

## Dex (the sidekick)

| | |
|---|---|
| Role | The calm expert. Corrects Kip, delivers the key fact, and holds up an **index card with the source**. Our two-source rule becomes an on-screen gag that also builds trust. |
| Personality | Deadpan, unflappable, quietly enjoys Kip's chaos. Dry one-liners. Says "Actually..." and means it. |
| Signature look | Taller and thinner than Kip, round glasses, teal bow tie (`#13A0A0`), carries index cards. |
| Voice | Low, calm, dry, measured, with a hint of amusement. |
| Screen time | 1 to 3 lines per episode. Some episodes are Kip alone, for variety. |

## How they play together (story engine)

1. Kip states a confident assumption or tries something.
2. Dex: "Actually..." and the card comes out.
3. Kip lives through the wild story (time travel, shrinking, becoming the object...).
4. Mind-blown moment: cowlick springs up.
5. A button joke, then tomorrow's teaser.

The outcome is never the same twice. Sometimes Kip is right and Dex is wrong. Sometimes Dex gets mind-blown. Sometimes they both are.

## Visual style: "drawn in a science notebook"

- **World:** warm paper (`#F4EFE4`) with a faint blue graph grid and a red margin line, like a lab notebook. It suits science, history and nature, and it is instantly recognisable in the feed.
- **Ink:** near-black (`#1B1B1F`), thick rounded lines (about 13 px at 1080 wide), so it stays readable on phones. A subtle "line boil" wobble gives a hand-drawn feel.
- **Palette:**

| Name | Hex | Use |
|---|---|---|
| Paper | `#F4EFE4` | Background |
| Ink | `#1B1B1F` | Lines, text |
| Kip orange | `#FF6B1A` | Kip, brand |
| Dex teal | `#13A0A0` | Dex, sources |
| Highlighter | `#FFE14D` | Caption highlights, emphasis |
| Alert red | `#E63946` | Danger, myths, "wrong" |
| Sky | `#4D9DE0` | Science, water, sky |
| Leaf | `#3BB273` | Nature |
| Grid | `#A9C3DB` | Notebook grid (low opacity) |

- **Captions:** Poppins ExtraBold (OFL licence), black text, with the key word swiped with a yellow highlighter marker. Kept out of the Shorts UI zones.
- **Props:** same ink weight, flat palette fills, no gradients.
- **Motion:** snappy. Anticipation, overshoot and settle, squash and stretch, and a breathing idle so nobody is ever frozen.

## Guardrails

- General audience (teens and adults): dry humour, real topics, no nursery tone.
- Original design. We don't copy any existing stickman series.
- Neither character gives health, money or legal advice.
