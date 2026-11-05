# Voice bake-off (free, runs on your PC)

Runs the same six lines (Kip and Dex, with excited, shocked, whisper, laugh, deadpan and dry delivery) through every candidate engine, so we can pick the channel's voice by ear.

| Engine | Licence | What it tests |
|---|---|---|
| Kokoro-82M | Apache 2.0 | Fast, clean, built-in voices (4 candidates for Kip, 3 for Dex) |
| Chatterbox | MIT | The "exaggeration" emotion dial |
| Chatterbox Turbo | MIT | Inline tags: `[laugh]`, `[gasp]`, `[sigh]`, `[chuckle]` ... |
| Qwen3-TTS VoiceDesign | Apache 2.0 | Invents Kip's and Dex's voices from a written description |

The run also tests the **planned production setup**:
1. Qwen3-TTS designs an original voice for each character and saves a reference clip.
2. Chatterbox and Turbo then clone those designed voices.

These are the `chatterbox-clone` and `turbo-clone` results.

## What you need

- Windows 10/11 with an NVIDIA GPU. An RTX 2070 SUPER (8 GB) is fine.
- An up-to-date NVIDIA driver. The scripts use CUDA 12.4 builds, so you need driver version 550 or newer.
- About 25 GB of free disk: roughly 10 GB of models plus the Python environments.
- A short repo path helps, for example `C:\yt\YT-StickManShorts`. The script works around long paths anyway.

## Steps

Open PowerShell in the repo folder and run:

```powershell
powershell -ExecutionPolicy Bypass -File tools\voice\setup.ps1
powershell -ExecutionPolicy Bypass -File tools\voice\run_bakeoff.ps1
```

`setup.ps1` installs `uv` (a Python manager) if needed and creates three environments under `tools\voice\.venvs\`. This happens once.

The first `run_bakeoff.ps1` run also downloads the models. After that, a full run takes a few minutes on the GPU.

## Listening

Open `out\voice-bakeoff\compare\`. There is one WAV per engine or voice, with all six lines back to back:

| File | What it is |
|---|---|
| `kokoro_am_puck.wav`, `kokoro_bm_george.wav`, ... | Kokoro built-in voices. Each file only contains the lines for the character that voice was assigned to. |
| `chatterbox-builtin.wav`, `turbo-builtin.wav` | The models' default voice |
| `qwen.wav` | Designed voices, emotion from written instructions |
| `chatterbox-clone.wav`, `turbo-clone.wav` | The designed voices, cloned. **This is the planned production setup.** |

Single lines are in the sub-folders, and the designed reference clips are in `out\voice-bakeoff\refs\`.

Score each one from 1 to 5 on:
1. Does Kip sound like Kip, and Dex like Dex?
2. Is the emotion believable (the shock, the whisper, the laugh)?
3. Is the pronunciation clean, with no glitches?
4. Would you watch 60 seconds of it?

## Changing things

- **Lines, voice descriptions, and delivery settings** live in `lines.json`.
  - To try a different Kip, edit `voices.kip.design` and re-run just Qwen and the clones:
    ```powershell
    .\tools\voice\.venvs\qwen\Scripts\python.exe tools\voice\bakeoff.py --engine qwen
    .\tools\voice\.venvs\chatterbox\Scripts\python.exe tools\voice\bakeoff.py --engine turbo
    ```
- **Your own voice:** record 10 to 20 seconds of clean speech as a WAV (it must be longer than 5 seconds). Save it as `out\voice-bakeoff\refs\kip.wav`, and keep a `dex.wav` there too. Then run the `chatterbox` and `turbo` engines.
- **Run a few lines only:** add `--only 01_kip_hook,03_kip_shock`.

## Notes

- Chatterbox output carries Resemble AI's inaudible "Perth" watermark, which marks audio as AI-generated. It doesn't affect YouTube.
- Turbo ignores the exaggeration dial. Its emotion comes from the inline tags and the reference clip.
- Never clone a real person's voice without their consent. Your own voice is fine.
