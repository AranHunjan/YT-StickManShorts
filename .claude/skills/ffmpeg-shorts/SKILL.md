---
name: ffmpeg-shorts
description: FFmpeg post-production for this channel's YouTube Shorts. Use for any audio or video processing step: mixing voice, music and SFX with ducking, loudness normalization to -14 LUFS, burning captions, encoding the 1080x1920 master, making review previews and contact sheets, pitch-shifting a character voice, trimming TTS silence, platform cuts, and the pre-publish quality gate. Prefer the bundled scripts over hand-written ffmpeg commands.
---

# FFmpeg for Shorts

Tested with FFmpeg 6.1. The scripts use only the Python standard library, so they run on Linux, macOS and Windows. They need `ffmpeg` and `ffprobe` on PATH.

## Master spec (what every final file must be)

| Property | Value |
|---|---|
| Resolution | 1080x1920 (9:16), progressive |
| Video | H.264 High, `yuv420p`, `-tune animation`, CRF 18, closed GOP of fps/2, BT.709 |
| Frame rate | 30 (60 only if the render is 60) |
| Audio | AAC-LC 48 kHz stereo, 192 kbps |
| Loudness | -14 LUFS integrated, true peak at or below -1.5 dBTP |
| Container | MP4 with `+faststart` |
| Duration | 15 to 60 s (our creative cap) |

## The three scripts (use these first)

Run from the repo root. Paths are examples.

```bash
S=.claude/skills/ffmpeg-shorts/scripts

# 1. Audio: voice + looped music bed ducked under the voice + timed SFX, two-pass loudnorm
python3 $S/mix_audio.py --voice out/ep047/voice.wav --music assets/music/bed.mp3 \
    --sfx out/ep047/sfx_cues.json --out out/ep047/mix.wav

# 2. Video: mux the render with the mix, optional burned-in ASS captions, encode the master
python3 $S/encode_short.py --video out/ep047/render.mp4 --audio out/ep047/mix.wav \
    --out out/ep047/final.mp4
#    small fast proxy for the daily review:
python3 $S/encode_short.py --video out/ep047/render.mp4 --audio out/ep047/mix.wav \
    --out out/ep047/preview.mp4 --preview

# 3. Quality gate: exits 1 on failure, prints a JSON report. Never publish a file that fails.
python3 $S/check_short.py out/ep047/final.mp4
```

`sfx_cues.json` format, times in seconds:

```json
[{"file": "assets/sfx/pop.wav", "at": 1.25, "gain_db": -6},
 {"file": "assets/sfx/whoosh.wav", "at": 4.10, "gain_db": -9}]
```

Useful flags:
- `mix_audio.py`: `--music-db` (bed level before ducking, default -18), `--duration` (force the total length), `--tail` (seconds after the voice ends, default 0.6).
- `encode_short.py`: `--ass` + `--fonts-dir` to burn captions, `--fps`, `--crf`, `--preset`. `--video` also accepts an image sequence such as `frames/%05d.png`.
- `check_short.py`: `--min`, `--max`, `--lufs`, `--max-gap` (longest silence allowed inside the Short, default 0.7 s).

## Rules

1. **Encode the delivery file once.** Keep intermediates lossless (WAV for audio; PNG frames, or the renderer's high-quality output, for video). Every lossy re-encode costs quality.
2. **Loudness is set at the end**, on the full mix, never on the voice alone. `mix_audio.py` already does two-pass loudnorm.
3. **Keep captions out of the Shorts UI zones**: the bottom ~20% and the right ~15% of the frame. In ASS at PlayRes 1080x1920, use `MarginV` of 500 or more, and `MarginR` of 160 or more.
4. **Always run `check_short.py` before uploading.**
5. **Quote paths.** On Windows, inside the `ass=` / `subtitles=` filter, use forward slashes and escape the drive colon (`C\:/...`). `encode_short.py` handles this for you.
6. **Licences:** only use music and SFX listed in `assets/LICENSES.md`.

## Recipes

### Inspect

```bash
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,avg_frame_rate,pix_fmt,sample_rate -of compact in.mp4
```

### TTS clean-up

```bash
# Trim leading and trailing silence from a TTS line
ffmpeg -i line.wav -af "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse" line_trim.wav

# Speed up delivery 8% without changing pitch (atempo accepts 0.5 to 2.0 per instance)
ffmpeg -i voice.wav -af "atempo=1.08" voice_fast.wav

# A second character voice for free: pitch the narrator up, keeping formants natural
ffmpeg -i narrator_line.wav -af "rubberband=pitch=1.25:formant=preserved" stick_line.wav

# Join line files in order (all must share format; list.txt has lines like: file 'L01.wav')
ffmpeg -f concat -safe 0 -i list.txt -c copy voice.wav

# Insert 0.25 s of silence between lines: generate it once, then put it in list.txt
ffmpeg -f lavfi -i anullsrc=r=48000:cl=mono -t 0.25 gap.wav
```

### Review helpers

```bash
# Contact sheet: one frame per second, 10 thumbnails, for a quick visual check
ffmpeg -i final.mp4 -vf "fps=1,scale=216:-1,tile=5x2:padding=6:color=white" -frames:v 1 sheet.png

# Single frame at 2.5 s (thumbnail candidate)
ffmpeg -ss 2.5 -i final.mp4 -frames:v 1 thumb.png
```

### Frames and cuts

```bash
# Image sequence to video (when the renderer outputs PNG frames)
ffmpeg -framerate 30 -i frames/%05d.png -c:v libx264 -crf 12 -pix_fmt yuv420p render.mp4

# Platform cut without re-encoding (cuts land on keyframes; re-encode for frame accuracy)
ffmpeg -ss 0 -i final.mp4 -t 59.5 -c copy cut.mp4

# Weekly long-form: concatenate episode masters that share the same spec
ffmpeg -f concat -safe 0 -i episodes.txt -c copy weekly.mp4
```

### Word-by-word "pop" captions in ASS (fallback when not using the renderer's captions)

```text
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Your Font,96,&H00FFFFFF,&H0000CCFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,8,3,2,80,200,620,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.50,Cap,,0,0,0,,{\fscx120\fscy120\t(0,90,\fscx100\fscy100)}Russia taxed {\c&H00CCFF&}BEARDS
```

ASS colours are `&HBBGGRR` (blue-green-red order). Generate one `Dialogue` per 1 to 3 words from the forced-alignment word timings, and highlight the key word.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `check_short.py` fails loudness | Re-run `mix_audio.py`; do not hand-normalize the voice alone |
| Silent gap error | A TTS line has leading or trailing silence: trim it (recipe above) or tighten the line timing |
| Music pumps too much | Raise the `sidechaincompress` threshold or lower its ratio in `mix_audio.py`, or lower `--music-db` |
| Captions in the wrong font | Pass `--fonts-dir` with the TTF/OTF file, and use the font's internal family name in the ASS style |
| Banding on flat gradients | Lower `--crf` to 16, or add a little noise in the renderer |
