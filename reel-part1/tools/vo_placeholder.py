"""Placeholder narrator (local Kokoro TTS) used when no ElevenLabs key is available.
Writes audio/vo/<ID>.wav (24 kHz mono, silence trimmed)."""
import json, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
MODELS = sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-0/models"
VOICE = sys.argv[2] if len(sys.argv) > 2 else "am_michael"
k = Kokoro(f"{MODELS}/kokoro-v1.0.int8.onnx", f"{MODELS}/voices-v1.0.bin")
script = json.load(open("script.json"))
for ln in script["narration"]:
    text = ln["text"].replace("A to", "A, to").replace("B to", "B, to")
    audio, sr = k.create(text, voice=VOICE, speed=0.9, lang="en-us")
    a = np.asarray(audio, dtype=np.float32)
    thr = 0.01 * np.abs(a).max()
    idx = np.where(np.abs(a) > thr)[0]
    a = a[max(idx[0] - int(0.03 * sr), 0): idx[-1] + int(0.08 * sr)]
    sf.write(f"audio/vo/{ln['id']}.wav", a, sr)
    print(ln["id"], round(len(a) / sr, 2))
