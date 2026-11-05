# Voice samples v2 (for review)

What changed from v1:
- General American accents for both characters.
- Calm, intriguing delivery: never loud.
- Kip redesigned away from the high-pitched "Morty" sound.
- Voices picked by measurement. See [docs/VOICE.md](../../VOICE.md).

The six lines:
1. **Kip** (intrigued): "Here's something strange. The lead in your pencil... isn't lead. Not even a little."
2. **Dex** (deadpan): "It's graphite, mixed with clay. People just mistook it for lead. Two sources, Kip."
3. **Kip** (stunned): "Wait... so we've been calling it the wrong thing... for centuries?"
4. **Kip** (hushed): "And here's the part nobody tells you."
5. **Kip** (amused): "Okay. That's actually kind of amazing."
6. **Dex** (dry): "You say that every single day."

| File | What it is |
|---|---|
| `1-chatterbox-final-PICK.mp3` | **The pick.** Chatterbox cloning the channel voices, with pace normalization |
| `2-turbo-for-comparison.mp3` | Chatterbox Turbo, same voices, emotion from inline tags |
| `3-channel-voice-references.mp3` | The two permanent reference clips (`assets/voices/`) that define who Kip and Dex sound like |

## Measured (tools/voice/analyze.py)

| | Pitch | Pitch range | Words/min | Bad takes | Score /100 |
|---|---|---|---|---|---|
| Kip, Chatterbox (pick) | 135 Hz | 12.6 st | 153 | 0 | **97** |
| Dex, Chatterbox (pick) | 91 Hz | 6.9 st | 155 | 0 | **95** |
| Kip, Turbo | 134 Hz | 16.6 st | 151 | 0 | 80 |
| Dex, Turbo | 83 Hz | 7.3 st | 174 | 0 | 87 |
| *Kip v1, for reference* | *211 to 241 Hz* | | | | *57 to 75* |

Kip and Dex are about 7 semitones apart in the final lines, so they're easy to tell apart.

Generated on CPU in the cloud sandbox; your GPU gives the same quality, faster. Volume is normalized for listening.
