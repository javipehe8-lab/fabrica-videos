"""Genera la narración por escena (Kokoro offline) -> voz/NN.wav (48 kHz) + tiempos.json"""
import json, os, sys, importlib.util
import numpy as np, onnxruntime as ort
from scipy.io import wavfile
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
TTS = os.path.join(HERE, "..", "tts")
spec = importlib.util.spec_from_file_location("narrar", os.path.join(TTS, "narrar.py"))
nar = importlib.util.module_from_spec(spec); spec.loader.exec_module(nar)
sys.path.insert(0, HERE)
ESCENAS = __import__('guion' + os.environ.get('EP', '')).ESCENAS

VOZ = os.environ.get("VOZ", "em_alex")
VEL = float(os.environ.get("VELOCIDAD", "1.08"))

def main(out):
    os.makedirs(out, exist_ok=True)
    sess = ort.InferenceSession(os.path.join(TTS, "kokoro.onnx"), providers=["CPUExecutionProvider"])
    voices = np.load(os.path.join(TTS, "voices.bin"))[VOZ]
    info = []
    for i, (_, texto) in enumerate(ESCENAS):
        parts = []
        for s in nar.split_sentences(texto):
            ph = nar.phonemize(s)
            ids = [nar.VOCAB[c] for c in ph if c in nar.VOCAB][:508]
            w = sess.run(None, {"tokens": np.array([[0, *ids, 0]], np.int64), "style": voices[len(ids)],
                                "speed": np.array([VEL], np.float32)})[0].astype(np.float32)
            # recorta silencios de los extremos para un ritmo más rápido
            nz = np.where(np.abs(w) > 0.01)[0]
            if len(nz): w = w[max(0, nz[0] - 600): nz[-1] + 1200]
            parts.append({"text": s, "wav": w})
        sub, t, chunks = [], 0.0, []
        for k, p in enumerate(parts):
            d = len(p["wav"]) / 24000
            sub.append({"text": p["text"], "start": round(t, 3), "end": round(t + d, 3)})
            chunks.append(p["wav"]); t += d
            if k < len(parts) - 1:
                chunks.append(np.zeros(int(24000 * 0.18), np.float32)); t += 0.18
        wav = np.concatenate(chunks)
        wav48 = resample_poly(wav, 2, 1).astype(np.float32)
        wavfile.write(os.path.join(out, f"{i:02d}.wav"), 48000, wav48)
        info.append({"dur": round(len(wav) / 24000, 3), "frases": sub})
        print(i, round(len(wav) / 24000, 2), "s", flush=True)
    json.dump(info, open(os.path.join(out, "tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main(sys.argv[1])
