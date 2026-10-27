"""Narra un guion en español con Kokoro (offline) y genera narracion.wav + segmentos.json con tiempos."""
import json, re, subprocess, sys, os
import numpy as np, onnxruntime as ort
from scipy.io import wavfile

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 24000
VOICE = os.environ.get("VOZ", "ef_dora")
SPEED = float(os.environ.get("VELOCIDAD", "0.95"))

_pad = "$"; _punct = ';:,.!?¡¿—…"«»“” '
_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_ipa = "ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ"
VOCAB = {c: i for i, c in enumerate([_pad] + list(_punct) + list(_letters) + list(_ipa))}

def espeak(text):
    env = dict(os.environ, LD_LIBRARY_PATH=os.path.join(HERE, "piper"))
    out = subprocess.run([os.path.join(HERE, "piper/espeak-ng"), "--path=" + os.path.join(HERE, "piper"),
                          "-v", "es", "-q", "--ipa"], input=text, capture_output=True, text=True, env=env).stdout
    return " ".join(out.split()).replace("tʃ", "ʧ").replace("dʒ", "ʤ")

def phonemize(sentence):
    # espeak descarta la puntuación: fonetizamos por trozos y la reinsertamos
    parts = re.split(r"([,;:.!?¿¡…—]+)", sentence)
    out = ""
    for p in parts:
        if not p.strip():
            continue
        if re.fullmatch(r"[,;:.!?¿¡…—]+", p):
            out = out.rstrip() + p.replace("¿", "").replace("¡", "") + " "
        else:
            out += espeak(p) + " "
    return out.strip()

def split_sentences(par):
    return [s.strip() for s in re.findall(r"[^.?!…]+(?:[.?!…]+|$)", par) if s.strip()]

def main(guion, outdir):
    sess = ort.InferenceSession(os.path.join(HERE, "kokoro.onnx"), providers=["CPUExecutionProvider"])
    voices = np.load(os.path.join(HERE, "voices.bin"))[VOICE]
    paras = [p.strip() for p in open(guion, encoding="utf-8").read().split("\n") if p.strip()]
    audio, segs, t = [], [], 0.6
    audio.append(np.zeros(int(SR * 0.6), np.float32))
    for pi, par in enumerate(paras):
        sents = split_sentences(par)
        for si, s in enumerate(sents):
            ph = phonemize(s)
            ids = [VOCAB[c] for c in ph if c in VOCAB][:508]
            wav = sess.run(None, {"tokens": np.array([[0, *ids, 0]], np.int64),
                                  "style": voices[len(ids)], "speed": np.array([SPEED], np.float32)})[0].astype(np.float32)
            dur = len(wav) / SR
            segs.append({"start": round(t, 3), "end": round(t + dur, 3), "text": s, "par": pi})
            gap = 0.75 if si == len(sents) - 1 else 0.3
            audio += [wav, np.zeros(int(SR * gap), np.float32)]
            t += dur + gap
        print(f"párrafo {pi+1}/{len(paras)}  t={t:.0f}s", flush=True)
    full = np.concatenate(audio)
    full = full / max(1e-6, np.abs(full).max()) * 0.9
    wavfile.write(os.path.join(outdir, "narracion.wav"), SR, (full * 32767).astype(np.int16))
    json.dump(segs, open(os.path.join(outdir, "segmentos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("duración total:", round(len(full) / SR, 1), "s")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
