# Voice: what the evidence says, and what we picked

## What the research says

| Finding | Source | What we do with it |
|---|---|---|
| Lower-pitched voices are typically judged **more competent and trustworthy**. | Oleszkiewicz et al. 2017, blind and sighted listeners ([PMC5486861](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5486861/)) | Both voices sit in the low-to-mid range. No high, nasal voice (the v1 "Morty" problem). |
| The preference for lower pitch is strongest in trust and competence contexts, and mixed in emotional ones. | Journal of Voice 2025, aviation trust study ([abstract](https://avesis.marmara.edu.tr/yayin/2899018a-c480-4f1f-aa7f-a72163f370a2/contextual-effects-of-vocal-pitch-on-trust-perception-in-aviation-settings)) | Dex, who delivers the facts, gets the lowest voice. Kip is a bit higher, for warmth and emotion. |
| For male voices, **lower pitch goes with higher attractiveness ratings**. Making a voice more "average" does not make it more attractive. | Ostrega et al. 2024, *Scientific Reports* ([PMC11076608](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11076608/)) | Keep distinctive, designed voices rather than generic ones. |
| Skilled narrators speak at about **150 words per minute**. Comprehension drops noticeably above 1.5x speed. | TES summary of playback-speed research ([link](https://www.tes.com/magazine/article/does-speeding-videos-podcasts-or-reading-affect-learning)); Microsoft Speaker Coach recommends 100 to 165 wpm ([link](https://support.microsoft.com/en-US/PowerPoint/suggestions-from-speaker-coach)) | Dex speaks at 125 to 155 wpm. |
| Across 6.9 million video-watching sessions, instructors who **spoke faster with enthusiasm** held attention better. | Guo, Kim & Rubin 2014, edX ([paper](https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf)) | Kip speaks a bit faster (150 to 180 wpm). His energy comes from pace and intonation, **not volume**. |
| Perceived charisma tracks **pitch range and variability, speaking rate, and pause structure**. | Niebuhr's prosody and charisma research ([example](https://typeset.io/pdf/shapes-and-timing-in-charismatic-speech-evidence-from-sounds-m381ume00z.pdf)) | Kip gets a wide pitch range (6 to 12 semitones), with deliberate pauses before reveals. That is what "intriguing" means in numbers. |
| A wider pitch range is proposed as the main cue for sounding friendly. This is a hypothesis under test, not a settled result. | Malarski & Jekiel ([link](https://repozytorium.amu.edu.pl/handle/10593/12722)) | Supports the wide range for Kip. |

Caveats:
- These studies are about listeners in general, not YouTube Shorts audiences specifically.
- Effects are moderate and vary by culture.

Our own retention data (Studio's "viewed vs swiped away" and average view percentage) overrides all of this once we have about 30 episodes.

## Targets (what `tools/voice/analyze.py` scores against)

| | Kip | Dex |
|---|---|---|
| Average pitch (F0) | 100 to 135 Hz (low-mid) | 80 to 115 Hz (low) |
| Pitch range | 6 to 12 semitones (expressive) | 4 to 9 semitones (dry, controlled) |
| Pace | 150 to 180 words per minute | 125 to 155 words per minute |
| Loudness | steady: never shouting, even when shocked | steady |
| Contrast | At least 3 semitones apart, so viewers can tell them apart instantly | |

## What we measured

v1 problem: **Kip v1 averaged 211 Hz.** Typical adult male speech sits around 85 to 155 Hz, so this is high and youthful, which is why he sounded like Morty.

v2 candidates (Qwen3-TTS VoiceDesign, General American, calm and intriguing):

| Candidate | Pitch | Range | WPM | Score /100 |
|---|---|---|---|---|
| **Kip A** | 104 Hz | 11.3 st | 157 | **100** |
| Kip B | 221 Hz | 11.5 st | 186 | 72. Described as a baritone, came out high: voice design is random, which is why we measure |
| **Dex A** | 96 Hz | 6.8 st | 161 | **94** |
| Dex B | 102 Hz | 10.4 st | 146 | 91 |

Kip A and Dex A were only 1.4 semitones apart, and Dex talked faster than Kip. So Dex's reference clip was processed once:
- 2 semitones lower (formant-preserving, so it still sounds natural)
- 5% slower

**Final pair: Kip 104 Hz / 157 wpm, Dex 87 Hz / 153 wpm, 3.2 semitones apart.** Both reference clips are saved in `assets/voices/`. They define the characters' voices permanently.

## How a voice is made: "designed reference" explained

1. **Design (once):** Qwen3-TTS reads a written description ("warm, low-mid, intriguing storyteller...") and invents a brand-new voice. It reads one sample paragraph, and that recording is the **designed reference**: the master copy of who the character sounds like. Design is random each time, so we keep the file instead of re-designing.
2. **Speak (daily):** Chatterbox clones the reference for every line. The *script* decides the emotion of each line (intrigued, hushed, stunned, amused, deadpan, dry), and the voice stays the same person.

## Engine choice: Chatterbox, with Turbo as backup

| | Chatterbox | Chatterbox Turbo |
|---|---|---|
| Emotion control | **A dial per line (exaggeration 0 to 1)**. Fine-grained, so every day's emotions can differ | Inline tags (`[chuckle]`, `[sigh]`, `[gasp]`), and the rest follows the reference |
| Speed | Slower | About 2x faster |
| Role | **Daily voice** | Fast previews and backup |

The exaggeration dial is capped at 0.6 so nothing gets loud. Each delivery's settings are in `tools/voice/lines.json`.

## Final lines (v2, Chatterbox + pace normalization)

| | Pitch | Range | WPM | Score |
|---|---|---|---|---|
| Kip | 135 Hz | 12.6 st | 153 | 97 |
| Dex | 91 Hz | 6.9 st | 155 | 95 |

The two are about 7 semitones apart in delivered lines. Expressive lines sit higher than the calm reference read, which is normal.

**Pace normalization** (`tools/voice/pace.py`): generation pace is random, so each line is time-stretched with pitch unchanged into the character's words-per-minute band, capped at 15%. Dex went from 178 to 155 wpm.

We also tried lowering `cfg_weight` to slow Dex down. It made him *faster* (187 wpm) and erratic, so we don't use it.

## Quality gate

Voice models sometimes produce a bad take: whispered, garbled, or the wrong pitch.
- `analyze.py` flags any take with too little voiced speech as **BAD**.
- In v1, one of Dex's lines failed this way in both clone engines.

Production rule:
1. Generate 3 takes per line.
2. Drop the bad ones.
3. Pace-normalize the rest.
4. Keep the take closest to the character's targets.
5. Then the human review.
