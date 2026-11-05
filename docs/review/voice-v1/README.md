# Voice samples v1 (for review)

All files read the same six test lines in order:

1. **Kip** (excited): "Okay. You know the lead in your pencil? There is no lead in it. At all!"
2. **Dex** (deadpan): "Actually, it's graphite. Mixed with clay. Two sources, Kip."
3. **Kip** (mind-blown): "Wait. What? Excuse me?!"
4. **Kip** (whisper): "And here's the part nobody tells you..."
5. **Kip** (amused): "Okay, that is actually amazing."
6. **Dex** (dry): "You say that every single day."

| File | Engine | How the voices were made |
|---|---|---|
| `designed-reference-voices.mp3` | Qwen3-TTS VoiceDesign | Kip's and Dex's voices, invented from the descriptions in `tools/voice/lines.json`. These two clips are what the clone engines copy. |
| `qwen.mp3` | Qwen3-TTS VoiceDesign | Designed voices, with emotion from a written instruction per line |
| `turbo-clone.mp3` | Chatterbox Turbo | Clones the designed voices; emotion from inline tags (`[gasp]`, `[laugh]`, `[sigh]`) |
| `chatterbox-clone.mp3` | Chatterbox | Clones the designed voices; emotion from the exaggeration dial |
| `kokoro_puck-kip_george-dex.mp3` | Kokoro-82M | Built-in voices: am_puck as Kip, bm_george as Dex. Other Kokoro voices are in the full kit. |

These were generated on a CPU in the cloud sandbox. Running the same models on the RTX 2070 SUPER gives the same quality, just much faster. Volume is normalized for listening; the final mix is set to -14 LUFS.

Timing in the sandbox (4 CPU cores), as the real-time factor: seconds of compute per second of audio.

| Engine | Real-time factor |
|---|---|
| Kokoro | 0.33 (3x faster than real time) |
| Chatterbox Turbo | 2.5 |
| Chatterbox | 4.2 |
| Qwen3-TTS 1.7B | 5.9 |

A 60 s episode needs about 60 s of audio, so even the CPU numbers are workable. The GPU will be much faster.
