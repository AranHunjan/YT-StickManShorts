#!/usr/bin/env python3
"""Voice bake-off: run the same lines through each open-source TTS engine so we
can compare them by ear. Each engine lives in its own virtual environment
(their dependencies conflict), so run this script once per engine with that
engine's Python. See tools/voice/README.md.

Engines:
  kokoro      Kokoro-82M, built-in voices (several candidates per character)
  qwen        Qwen3-TTS VoiceDesign: invents each voice from a text description
              (one per candidate design a, b, ...) and saves a reference clip per
              character and candidate into refs/<speaker>_<variant>.wav
  chatterbox  Chatterbox (exaggeration dial). Clones every candidate whose refs
              exist (folders chatterbox-clone-a, -b, ...), else its built-in voice
  turbo       Chatterbox Turbo (inline [laugh]/[gasp]/[sigh] tags). Same refs rule

Usage:
  python bakeoff.py --engine kokoro
  python bakeoff.py --engine qwen
  python bakeoff.py --engine chatterbox
  python bakeoff.py --engine turbo
  python bakeoff.py --compare          # one combined file per engine/voice

Options: --out DIR (default: out/voice-bakeoff), --device auto|cuda|cpu,
         --only 01_kip_hook,03_kip_shock (subset of line ids)
"""
import argparse
import json
import re
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAG = re.compile(r"\[[a-z ]+\]\s*")


def strip_tags(text):
    return TAG.sub("", text).strip()


def pick_device(want):
    import torch
    if want != "auto":
        return want
    return "cuda" if torch.cuda.is_available() else "cpu"


def save(path, wav, sr):
    import numpy as np
    import soundfile as sf
    path.parent.mkdir(parents=True, exist_ok=True)
    a = wav.detach().cpu().numpy() if hasattr(wav, "detach") else np.asarray(wav)
    sf.write(str(path), a.squeeze(), sr)


class Timer:
    """Reports the real-time factor: seconds of compute per second of audio."""

    def __init__(self):
        self.compute = 0.0
        self.audio = 0.0

    def add(self, seconds, n_samples, sr):
        self.compute += seconds
        self.audio += n_samples / sr

    def report(self, name):
        if self.audio:
            print(f"[{name}] {self.audio:.1f}s of audio in {self.compute:.1f}s "
                  f"(real-time factor {self.compute / self.audio:.2f}; below 1.0 is faster than real time)")


def espeak_short_path():
    """espeak-ng (used by Kokoro for unusual words) keeps its data path in a
    160-character buffer and hard-exits the whole process when the path is
    longer. If ours is too long, copy the data to a short folder and use that."""
    import os
    import shutil
    import tempfile
    import espeakng_loader
    import misaki.espeak  # noqa: F401  (sets the default, possibly too long, path)
    from phonemizer.backend.espeak.wrapper import EspeakWrapper
    src = Path(espeakng_loader.get_data_path())
    if len(str(src)) < 140:
        return
    dst = Path(os.environ.get("ESPEAK_SHORT_DIR") or tempfile.gettempdir()) / "espeak-ng-data"
    if len(str(dst)) >= 140:
        raise SystemExit("espeak-ng data path too long: set ESPEAK_SHORT_DIR to a short folder such as C:\\espeak")
    if not (dst / "phontab").exists():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    EspeakWrapper.set_data_path(str(dst))
    print(f"[kokoro] espeak-ng data path was {len(str(src))} chars; using {dst}")


def run_kokoro(cfg, lines, out, device):
    from kokoro import KPipeline
    import numpy as np
    espeak_short_path()
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M", device=device)
    pipe_gb = KPipeline(lang_code="b", repo_id="hexgrad/Kokoro-82M", device=device)
    t = Timer()
    for ln in lines:
        d = cfg["delivery"][ln["delivery"]]
        for voice in cfg["voices"][ln["speaker"]]["kokoro"]:
            p = pipe_gb if voice.startswith("b") else pipe
            t0 = time.time()
            chunks = [r.audio.numpy() for r in p(strip_tags(ln["text"]), voice=voice, speed=d["kokoro_speed"]) if r.audio is not None]
            wav = np.concatenate(chunks)
            t.add(time.time() - t0, len(wav), 24000)
            save(out / "kokoro" / voice / f"{ln['id']}.wav", wav, 24000)
            print("kokoro", voice, ln["id"])
    t.report("kokoro")


def designs_of(voice):
    """Candidate voice descriptions for a character: {"a": "...", "b": "..."}."""
    return voice.get("designs") or {"a": voice["design"]}


def run_qwen(cfg, lines, out, device, refs_only=False):
    import torch
    from qwen_tts import Qwen3TTSModel
    # RTX 20-series (Turing) has no fast bfloat16, so use float16 on CUDA.
    dtype = torch.float16 if device == "cuda" else torch.float32
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
        device_map="cuda:0" if device == "cuda" else "cpu",
        dtype=dtype,
    )
    t = Timer()
    variants = sorted({v for voice in cfg["voices"].values() for v in designs_of(voice)})
    # Reference clips: one read per character and candidate design. Design runs are
    # random, so the voice is fixed by saving this clip and cloning it from then on.
    for spk, voice in cfg["voices"].items():
        for var, design in designs_of(voice).items():
            t0 = time.time()
            wavs, sr = model.generate_voice_design(text=voice["reference_text"], instruct=design + " Natural, conversational read.", language="English")
            t.add(time.time() - t0, len(wavs[0]), sr)
            save(out / "refs" / f"{spk}_{var}.wav", wavs[0], sr)
            print("qwen reference", spk, var)
    if not refs_only:
        for var in variants:
            for ln in lines:
                voice = cfg["voices"][ln["speaker"]]
                design = designs_of(voice).get(var) or next(iter(designs_of(voice).values()))
                d = cfg["delivery"][ln["delivery"]]
                t0 = time.time()
                wavs, sr = model.generate_voice_design(text=strip_tags(ln["text"]), instruct=f"{design} Delivery: {d['instruct']}.", language="English")
                t.add(time.time() - t0, len(wavs[0]), sr)
                save(out / f"qwen-{var}" / f"{ln['id']}.wav", wavs[0], sr)
                print("qwen", var, ln["id"])
    t.report("qwen")


def run_chatterbox(cfg, lines, out, device, turbo, only_variant=None, refs_dir=None):
    if turbo:
        from chatterbox.tts_turbo import ChatterboxTurboTTS as Model
    else:
        from chatterbox.tts import ChatterboxTTS as Model
    model = Model.from_pretrained(device=device)
    name = "turbo" if turbo else "chatterbox"
    speakers = list(cfg["voices"])
    variants = sorted({v for voice in cfg["voices"].values() for v in designs_of(voice)})
    if only_variant:
        variants = [only_variant]
    # A variant is usable once every character has a reference clip for it.
    ready = [v for v in variants if all((out / "refs" / f"{spk}_{v}.wav").exists() for spk in speakers)]
    runs = [(f"{name}-clone-{v}", {spk: out / "refs" / f"{spk}_{v}.wav" for spk in speakers}) for v in ready]
    if refs_dir:
        # The channel's permanent voices (assets/voices/<speaker>.wav).
        runs = [(f"{name}-final", {spk: Path(refs_dir) / f"{spk}.wav" for spk in speakers})]
    if not runs:
        print(f"[{name}] no designed reference clips yet: using the built-in voice (run --engine qwen first)")
        runs = [(f"{name}-builtin", None)]
    t = Timer()
    for tag, refs in runs:
        for ln in lines:
            d = cfg["delivery"][ln["delivery"]]
            kw = {}
            if refs:
                kw["audio_prompt_path"] = str(refs[ln["speaker"]])
            text = ln["text"] if turbo else strip_tags(ln["text"])
            if not turbo:
                kw.update(exaggeration=d["exaggeration"], cfg_weight=d["cfg_weight"])
            t0 = time.time()
            wav = model.generate(text, **kw)
            t.add(time.time() - t0, wav.shape[-1], model.sr)
            save(out / tag / f"{ln['id']}.wav", wav, model.sr)
            print(tag, ln["id"])
    t.report(name)


def compare(out):
    """Join each folder's lines (with short gaps) into one file for easy listening."""
    import numpy as np
    import soundfile as sf
    made = []
    for folder in sorted({p.parent for p in out.rglob("*.wav")}):
        if folder.name in ("refs", "compare"):
            continue
        parts, sr = [], None
        for f in sorted(folder.glob("*.wav")):
            a, s = sf.read(str(f), dtype="float32")
            if a.ndim > 1:
                a = a.mean(axis=1)
            if sr is None:
                sr = s
            if s != sr:
                continue
            parts += [a, np.zeros(int(sr * 0.6), dtype="float32")]
        if parts:
            name = "_".join(folder.relative_to(out).parts)
            dest = out / "compare" / f"{name}.wav"
            dest.parent.mkdir(parents=True, exist_ok=True)
            sf.write(str(dest), np.concatenate(parts), sr)
            made.append(dest)
    for m in made:
        print("wrote", m)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engine", choices=["kokoro", "qwen", "chatterbox", "turbo"])
    ap.add_argument("--compare", action="store_true")
    ap.add_argument("--out", default=str(HERE.parent.parent / "out" / "voice-bakeoff"))
    ap.add_argument("--device", default="auto")
    ap.add_argument("--only", help="comma-separated line ids")
    ap.add_argument("--variant", help="clone only this candidate voice (a, b, ...)")
    ap.add_argument("--refs-only", action="store_true", help="qwen: only design the reference clips")
    ap.add_argument("--refs-dir", help="clone these reference clips (<speaker>.wav), e.g. assets/voices")
    args = ap.parse_args()
    out = Path(args.out)

    if args.compare:
        compare(out)
        return
    if not args.engine:
        ap.error("pass --engine or --compare")

    cfg = json.loads((HERE / "lines.json").read_text(encoding="utf-8"))
    lines = cfg["lines"]
    if args.only:
        keep = set(args.only.split(","))
        lines = [ln for ln in lines if ln["id"] in keep]
    device = pick_device(args.device)
    print(f"engine={args.engine} device={device} lines={len(lines)} out={out}")

    if args.engine == "kokoro":
        run_kokoro(cfg, lines, out, device)
    elif args.engine == "qwen":
        run_qwen(cfg, lines, out, device, refs_only=args.refs_only)
    else:
        run_chatterbox(cfg, lines, out, device, turbo=args.engine == "turbo", only_variant=args.variant, refs_dir=args.refs_dir)


if __name__ == "__main__":
    main()
