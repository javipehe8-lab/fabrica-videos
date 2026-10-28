"""Genera la narración por escena (Kokoro offline) -> voz/NN.wav (48 kHz) + tiempos.json

Diálogos: dentro del texto de una escena, [LEO], [NORA], [DOCTOR], [CARMEN], [CORONEL], [SOLDADO], [SONRIENTE]
(cualquier otro nombre usa la voz OTRO) cambian de voz hasta el siguiente marcador o [NARRADOR].
Ej.: "Leo la buscó en el bosque. [SONRIENTE] Leo… te puedo ver." Usar de forma PUNTUAL (1-3 frases por episodio).
"""
import json, os, re, sys, importlib.util
import numpy as np, onnxruntime as ort
from scipy.io import wavfile
from scipy.signal import resample_poly

HERE = os.path.dirname(os.path.abspath(__file__))
TTS = os.path.join(HERE, "..", "tts")
spec = importlib.util.spec_from_file_location("narrar", os.path.join(TTS, "narrar.py"))
nar = importlib.util.module_from_spec(spec); spec.loader.exec_module(nar)
sys.path.insert(0, HERE)
EN = os.environ.get('IDIOMA') == 'en'
ESCENAS = __import__('guion' + os.environ.get('EP', '') + ('_en' if EN else '')).ESCENAS
if EN: os.environ.setdefault('TTS_LANG', 'en-us')

# (voz kokoro, velocidad, tono en semitonos). Cada personaje con voz DISTINTA del narrador.
# En español Kokoro solo tiene 3 voces (em_alex, em_santa, ef_dora): se diferencian con tono y efectos.
if EN:
    REPARTO = {"NARRADOR": ("am_onyx", 1.08, 0), "LEO": ("am_puck", 1.12, 1), "NORA": ("af_bella", 1.1, 1),
               "DOCTOR": ("bm_george", 1.0, 0), "CARMEN": ("bf_emma", 0.92, -2), "CORONEL": ("am_fenrir", 1.0, -1),
               "SOLDADO": ("am_adam", 1.1, 0), "SONRIENTE": ("am_fenrir", 0.9, 0), "OTRO": ("am_eric", 1.05, 0)}
else:
    REPARTO = {"NARRADOR": ("em_alex", 1.15, 0), "LEO": ("em_santa", 1.18, 4), "NORA": ("ef_dora", 1.12, 1),
               "DOCTOR": ("em_santa", 1.05, 0), "CARMEN": ("ef_dora", 0.95, -3), "CORONEL": ("em_santa", 1.0, -2),
               "SOLDADO": ("em_santa", 1.12, 1), "SONRIENTE": ("em_santa", 0.95, 0), "OTRO": ("em_santa", 1.1, 2)}
if os.environ.get("VOZ"):
    REPARTO["NARRADOR"] = (os.environ["VOZ"], float(os.environ.get("VELOCIDAD", REPARTO["NARRADOR"][1])), 0)

def tono(w, semis):
    """cambia el tono (y el ritmo) remuestreando: semis < 0 = más grave y lento"""
    if not semis: return w
    f = 2 ** (semis / 12); up, down = 100, int(round(100 * f))
    return resample_poly(w, up, down).astype(np.float32)

def monstruo(w):
    """voz del Sonriente: grave, con eco y un susurro por debajo"""
    w = tono(w, -5)
    out = np.copy(w)
    for d, g in ((int(24000 * 0.09), 0.45), (int(24000 * 0.19), 0.25)):
        out[d:] += w[:-d] * g
    rng = np.random.default_rng(1)
    env = np.convolve(np.abs(w), np.ones(400) / 400, mode="same")
    out += rng.normal(0, 1, len(w)).astype(np.float32) * env * 0.35
    return out / (np.abs(out).max() + 1e-9) * 0.9

def trozos(texto):
    """[(hablante, frase limpia)]"""
    res, quien = [], "NARRADOR"
    for parte in re.split(r"(\[[A-ZÁÉÍÓÚÑ]+\])", texto):
        m = re.fullmatch(r"\[(\w+)\]", parte.strip())
        if m: quien = m.group(1); continue
        for s in nar.split_sentences(parte):
            res.append((quien, s))
    return res

def main(out):
    os.makedirs(out, exist_ok=True)
    sess = ort.InferenceSession(os.path.join(TTS, "kokoro.onnx"), providers=["CPUExecutionProvider"])
    bank = np.load(os.path.join(TTS, "voices.bin"))
    info = []
    for i, (_, texto) in enumerate(ESCENAS):
        parts = []
        for quien, s in trozos(texto):
            vname, vel, semis = REPARTO.get(quien, REPARTO["OTRO"])
            ph = nar.phonemize(s)
            ids = [nar.VOCAB[c] for c in ph if c in nar.VOCAB][:508]
            w = sess.run(None, {"tokens": np.array([[0, *ids, 0]], np.int64), "style": bank[vname][len(ids)],
                                "speed": np.array([vel], np.float32)})[0].astype(np.float32)
            nz = np.where(np.abs(w) > 0.01)[0]
            if len(nz): w = w[max(0, nz[0] - 600): nz[-1] + 1200]
            w = monstruo(w) if quien == "SONRIENTE" else tono(w, semis)
            parts.append({"text": s, "wav": w, "quien": quien})
        sub, t, chunks = [], 0.0, []
        for k, p in enumerate(parts):
            d = len(p["wav"]) / 24000
            sub.append({"text": p["text"], "start": round(t, 3), "end": round(t + d, 3), "quien": p["quien"]})
            chunks.append(p["wav"]); t += d
            if k < len(parts) - 1:
                gap = 0.28 if parts[k + 1]["quien"] != p["quien"] else 0.14
                chunks.append(np.zeros(int(24000 * gap), np.float32)); t += gap
        wav = np.concatenate(chunks)
        wav48 = resample_poly(wav, 2, 1).astype(np.float32)
        wavfile.write(os.path.join(out, f"{i:02d}.wav"), 48000, wav48)
        info.append({"dur": round(len(wav) / 24000, 3), "frases": sub})
        print(i, round(len(wav) / 24000, 2), "s", flush=True)
    json.dump(info, open(os.path.join(out, "tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main(sys.argv[1])
