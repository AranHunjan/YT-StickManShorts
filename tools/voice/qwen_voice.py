#!/usr/bin/env python3
"""Generate takes for lines voiced by a Qwen3-TTS CustomVoice preset speaker
(e.g. Dex = "aiden"). Runs in the qwen environment; speak.py calls it for you.
Lines are generated in one batch per take round (faster on CPU and GPU).

Usage (normally via speak.py):
  python qwen_voice.py --script episodes/001/script.json --out episodes/001/audio \
      --ids L03,L05 --speaker aiden --persona "..." [--takes 1] [--device auto]
Writes <out>/takes/<id>_q<k>.wav
"""
import argparse
import json
import re
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def spoken(text):
    text = re.sub(r"\[[a-z ]+\]\s*", "", text)
    return re.sub(r"\{([^|}]*)\|([^}]*)\}", lambda m: m.group(2), text).replace("*", "").strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--speaker", required=True)
    ap.add_argument("--persona", default="")
    ap.add_argument("--takes", type=int, default=1)
    ap.add_argument("--start", type=int, default=1, help="number of the first take to write")
    ap.add_argument("--device", default="auto")
    args = ap.parse_args()

    import soundfile as sf
    import torch
    from qwen_tts import Qwen3TTSModel

    device = args.device
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    # RTX 20-series (Turing) has no fast bfloat16, so use float16 on CUDA.
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
        device_map="cuda:0" if device == "cuda" else "cpu",
        dtype=torch.float16 if device == "cuda" else torch.float32,
    )
    deliveries = json.loads((HERE / "lines.json").read_text(encoding="utf-8"))["delivery"]
    lines = {l["id"]: l for l in json.loads(Path(args.script).read_text(encoding="utf-8"))["lines"]}
    ids = [i for i in args.ids.split(",") if i]
    takes_dir = Path(args.out) / "takes"
    takes_dir.mkdir(parents=True, exist_ok=True)

    texts = [spoken(lines[i]["text"]) for i in ids]
    instructs = [f"{args.persona} {deliveries[lines[i]['delivery']]['instruct']}.".strip() for i in ids]
    for k in range(args.start, args.start + args.takes):
        t0 = time.time()
        torch.manual_seed(1000 + k)
        wavs, sr = model.generate_custom_voice(text=texts, speaker=[args.speaker] * len(ids),
                                               language=["English"] * len(ids), instruct=instructs)
        for i, w in zip(ids, wavs):
            sf.write(str(takes_dir / f"{i}_q{k}.wav"), w, sr)
        print(f"qwen {args.speaker} take {k}: {len(ids)} lines in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
