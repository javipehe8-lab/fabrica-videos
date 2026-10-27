"""Mezcla: narración + música de tensión + efectos sintetizados, sincronizados con timeline.json. Uso: sonido.py voz_dir out_dir"""
import json, os, sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(5)
def T(d): return np.arange(int(SR * d)) / SR
def env(n, a=0.005, r=None):
    e = np.ones(n); na = max(1, int(SR * a)); e[:na] = np.linspace(0, 1, na)
    if r: e *= np.exp(-np.arange(n) / (SR * r))
    return e
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x)
def lp(x, f): return sosfilt(butter(2, f, "lowpass", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(2, f, "highpass", fs=SR, output="sos"), x)

# ---------- efectos ----------
def boom(d=1.6, f0=70):
    t = T(d); f = f0 * np.exp(-t * 2.2) + 28
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.4)
    n = lp(rng.normal(0, 1, len(t)), 900) * np.exp(-t * 6) * 0.6
    return np.tanh((s + n) * 2.2) * 0.9
def impact(): return boom(0.6, 140) * 0.7 + hp(rng.normal(0, 1, int(SR * 0.6)), 2000) * np.exp(-T(0.6) * 30) * 0.4
def whoosh(d=0.45, up=True):
    t = T(d); n = rng.normal(0, 1, len(t)); out = np.zeros_like(n)
    for i, c in enumerate(np.linspace(600, 3500, 12) if up else np.linspace(3500, 600, 12)):
        a, b = int(i * len(t) / 12), int((i + 1) * len(t) / 12)
        out[a:b] = bp(n, c * 0.7, c * 1.3)[a:b]
    return out * np.sin(np.pi * t / d) ** 2 * 0.5
def heartbeat(n=6, bpm=80):
    beat = 60 / bpm; out = np.zeros(int(SR * beat * n))
    for k in range(n):
        for off, amp in ((0, 1), (0.22, 0.7)):
            i = int(SR * (k * beat + off)); s = boom(0.35, 60)[: len(out) - i] * amp
            out[i:i + len(s)] += s
    return lp(out, 200) * 1.4
def static(d=0.6): return bp(rng.normal(0, 1, int(SR * d)), 1500, 7000) * (0.4 + 0.6 * (rng.random(int(SR * d)) > 0.6)) * 0.35
def sting(d=1.4):
    t = T(d); s = sum(np.sin(2 * np.pi * (f + 6 * np.sin(2 * np.pi * 7 * t)) * t) for f in (880, 932, 1245, 1319))
    return np.tanh(s * 0.6) * np.exp(-t * 2.5) * 0.45
def step(): return lp(rng.normal(0, 1, int(SR * 0.08)), 900) * np.exp(-T(0.08) * 60) * 0.8
def gunshot():
    t = T(0.35); n = rng.normal(0, 1, len(t))
    return np.tanh((hp(n, 300) * np.exp(-t * 40) + boom(0.35, 120) * 0.6) * 3) * 0.55
def beep(d=0.12, f=1000): t = T(d); return np.sin(2 * np.pi * f * t) * env(len(t), 0.003) * np.minimum(1, (d - t) * 60) * 0.25
def powerdown(d=1.6):
    t = T(d); f = 380 * np.exp(-t * 2.2) + 30
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.3
    return lp(s, 1600) * np.exp(-t * 1.4)
def buzz(d):
    t = T(d); s = np.sign(np.sin(2 * np.pi * 120 * t)) * (0.5 + 0.5 * (np.sin(2 * np.pi * 7.3 * t) > 0.2))
    return bp(s, 100, 2400) * 0.12
def ding():
    t = T(1.2); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((1568, 3), (2093, 4), (3136, 6))) * 0.18
def scream(d):
    t = T(d); f = 340 + 220 * np.sin(2 * np.pi * 0.7 * t) + 40 * np.sin(2 * np.pi * 23 * t)
    s = 2 * ((np.cumsum(f) / SR) % 1) - 1
    s = s + 0.5 * (2 * ((np.cumsum(f * 1.5) / SR) % 1) - 1) + 0.6 * bp(rng.normal(0, 1, len(t)), 800, 5000)
    return np.tanh(bp(s, 200, 4500) * 2.5) * np.minimum(1, t * 4) * 0.4
def riser(d):
    t = T(d); f = 200 * np.exp(t / d * np.log(8))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3 + hp(rng.normal(0, 1, len(t)), 3000) * 0.2) * (t / d) ** 2 * 0.6
def shimmer():
    t = T(1.6); return sum(np.sin(2 * np.pi * f * t) for f in (1047, 1319, 1568, 2093)) * np.exp(-t * 2) * 0.12
def chime():
    t = T(2.5); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 1.5) for f in (523, 659, 784, 1047)) * 0.12

# ---------- música ----------
def musica(total, cuts):
    t = T(total); out = np.zeros_like(t)
    cs = cuts.get("amanecer") or cuts.get("encerrado")
    calm_from, calm_to = cs
    calm = ((t >= calm_from) & (t < calm_to)).astype(float)
    calm = lp(calm, 3)  # transición suave
    tense = 1 - calm
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t)
    pad_m = sum(np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * 1.004 * t) for f in (110, 130.8, 164.8, 55))
    pad_M = sum(np.sin(2 * np.pi * f * t) + np.sin(2 * np.pi * f * 1.004 * t) for f in (110, 138.6, 164.8, 220))
    out += lp(pad_m * tense + pad_M * calm, 900) * lfo * 0.05
    beat = 60 / 110; k = boom(0.4, 90) * 0.5; hat = hp(rng.normal(0, 1, int(SR * 0.04)), 6000) * np.exp(-T(0.04) * 90) * 0.12
    nb = int(total / beat * 2)
    for i in range(nb):
        tt = i * beat / 2; j = int(tt * SR)
        if j >= len(out) or calm[min(j, len(calm) - 1)] > 0.5: continue
        if tt > cuts["final"][0]: continue
        if i % 2 == 0:
            s = k[: len(out) - j]; out[j:j + len(s)] += s
        s = hat[: len(out) - j]; out[j:j + len(s)] += s * (1 if i % 2 else 0.5)
    return out

def main(voz, out):
    tl = json.load(open(os.path.join(out, "timeline.json")))
    total = tl[-1]["start"] + tl[-1]["D"] + 0.3
    N = int(SR * total); mixv = np.zeros(N); sfx = np.zeros(N)
    cuts = {s["name"]: (s["start"], s["start"] + s["D"]) for s in tl}
    def put(buf, x, at, g=1.0):
        i = int(at * SR)
        if i >= N: return
        x = x[: N - i]; buf[i:i + len(x)] += x * g
    for k, s in enumerate(tl):
        sr, w = wavfile.read(os.path.join(voz, f"{k:02d}.wav"))
        put(mixv, w.astype(np.float64) / (np.abs(w).max() + 1e-9) * 0.9, s["start"] + 0.12)
        a, D, n = s["start"], s["D"], s["name"]
        if k: put(sfx, whoosh(0.35), a - 0.12, 0.6)
        if n == "ventana": put(sfx, heartbeat(5, 75), a, 0.9); put(sfx, static(0.8), a + 1.3, 0.7); put(sfx, sting(1.2), a + 1.35, 0.5)
        if n == "cara": put(sfx, boom(), a, 1.0); put(sfx, sting(1.6), a, 0.9); put(sfx, static(D), a, 0.5)
        if n == "nora":
            for i in range(7): put(sfx, step(), a + i * 0.19, 0.8)
            put(sfx, riser(1.0), a + D * 0.72 - 1.0, 0.6); put(sfx, impact(), a + D * 0.72, 0.6)
        if n == "ciudad":
            put(sfx, powerdown(1.8), a + D * 0.3, 0.8)
            for i in range(6): put(sfx, impact() * 0.4, a + D * (0.3 + i * 0.1), 0.5)
        if n == "ejercito":
            for i in range(int(D / 0.31)): put(sfx, boom(0.3, 80), a + i * 0.31, 0.45)
        if n == "doctor":
            fl = a + D * 0.58; tt = a + 0.2
            while tt < fl: put(sfx, beep(), tt, 1.0); tt += 0.625
            put(sfx, beep(a + D - fl, 1000) * 0.9, fl, 1.0)
        if n == "leo_ojos": put(sfx, boom(), a + 0.45, 1.0); put(sfx, static(0.5), a + 0.45, 0.8); put(sfx, heartbeat(4, 150), a + 0.6, 0.8)
        if n == "pasillo":
            put(sfx, buzz(D * 0.78), a, 1.0)
            for i in range(int(D / 0.55)): put(sfx, boom(0.4, 50), a + 0.2 + i * 0.55, 0.5)
            put(sfx, impact(), a + D * 0.78, 0.8)
        if n == "disparos":
            tt = a + 0.1; r = np.random.default_rng(2)
            while tt < a + D * 0.66: put(sfx, gunshot(), tt, 0.7); tt += r.uniform(0.09, 0.2)
            put(sfx, whoosh(0.4), a + D * 0.66, 1.0); put(sfx, boom(), a + D * 0.7, 0.9)
            for i in range(3): put(sfx, whoosh(0.5, False), a + D * 0.72 + i * 0.06, 0.5)
        if n == "idea": put(sfx, ding(), a + D * 0.3, 1.0); put(sfx, whoosh(0.3), a + D * 0.6, 0.8); put(sfx, impact(), a + D * 0.62, 0.7)
        if n == "espejo": put(sfx, riser(D * 0.42), a, 0.8); put(sfx, shimmer(), a + D * 0.42, 1.2); put(sfx, boom(), a + D * 0.42, 0.8)
        if n == "estallido": put(sfx, scream(D * 0.5), a, 0.9); put(sfx, boom(2.5, 55), a + D * 0.5, 1.2); put(sfx, static(1.0), a + D * 0.5, 0.6)
        if n == "amanecer": put(sfx, chime(), a, 1.0)
        if n == "giro" and os.environ.get("EP", "") in ("", "1"): put(sfx, static(D * 0.8) * np.linspace(0, 1, int(SR * D * 0.8)), a, 0.6); put(sfx, sting(1.4), a + D * 0.82, 1.0); put(sfx, boom(), a + D * 0.82, 1.0)
        if n == "final": put(sfx, boom(2.0, 45), a, 0.9); put(sfx, impact(), a + 1.2, 0.6)
        # ---- episodio 2 ----
        if n == "caja":
            for i in range(3): put(sfx, impact() * 0.5, a + D * (0.5 + 0.12 * i), 0.7); put(sfx, beep(0.05, 2400), a + D * (0.5 + 0.12 * i) + 0.02, 0.8)
        if n == "golpes":
            for h in (0.25, 0.75, 1.15, 1.45, 1.7, 1.9, 2.05): put(sfx, boom(0.5, 90), a + h, 1.0)
        if n == "grieta":
            for i in range(6): put(sfx, hp(rng.normal(0, 1, int(SR * 0.06)), 2500) * np.exp(-T(0.06) * 50) * 0.6, a + 0.15 + i * 0.22, 1.0)
            put(sfx, sting(1.4), a + D * 0.55, 1.0); put(sfx, static(0.8), a + D * 0.55, 0.6)
        if n == "libro": put(sfx, whoosh(0.5, False), a + 0.2, 0.8); put(sfx, impact() * 0.5, a + D * 0.62, 0.6)
        if n == "faro": put(sfx, chime() * 0.6, a + D * 0.4, 1.0)
        if n in ("convoy", "revienta"):
            t_ = T(D); put(sfx, lp(rng.normal(0, 1, len(t_)), 180) * 0.35 * (1 if n == "convoy" else (t_ < D * 0.33)), a, 1.0)
        if n == "revienta": put(sfx, boom(2.2, 60), a + D * 0.33, 1.3); put(sfx, scream(1.6) * 0.7, a + D * 0.45, 0.8)
        if n == "ataque":
            for i in range(4): put(sfx, whoosh(0.5), a + D * (0.3 + 0.14 * i), 1.0); put(sfx, scream(0.5) * 0.5, a + D * (0.3 + 0.14 * i) + 0.1, 0.6)
            tt = a + 0.1; r = np.random.default_rng(4)
            while tt < a + D * 0.75: put(sfx, gunshot(), tt, 0.45); tt += r.uniform(0.12, 0.3)
        if n == "carrera":
            for i in range(int(D / 0.19)): put(sfx, step(), a + i * 0.19, 0.9)
            put(sfx, heartbeat(5, 140), a, 0.7)
        if n == "escalera":
            for i in range(int(D / 0.16)): put(sfx, step() * 1.2, a + i * 0.16, 0.8)
            put(sfx, riser(D), a, 0.5)
        if n == "palanca":
            for i in range(6): put(sfx, impact() * 0.35, a + D * 0.35 + i * 0.12, 0.7)
        if n == "frente": put(sfx, heartbeat(6, 90), a, 1.0); put(sfx, riser(D * 0.9), a, 0.6); put(sfx, static(0.8), a + D * 0.8, 0.6)
        if n == "luz": put(sfx, impact(), a + D * 0.45 - 0.1, 1.0); put(sfx, boom(2.0, 50), a + D * 0.45, 1.2); put(sfx, shimmer() * 2, a + D * 0.45, 1.0); put(sfx, scream(D * 0.4), a + D * 0.48, 0.8)
        if n == "encerrado": put(sfx, chime(), a + 0.1, 1.0)
        # ---- episodio 3 ----
        if n == "sonrisa": put(sfx, sting(1.2) * 0.6, a + D * 0.5, 1.0); put(sfx, static(0.4), a + D * 0.5, 0.5)
        if n == "pared":
            for i in range(int(D / 0.5)): put(sfx, beep(0.03, 1800) * 0.6, a + i * 0.5, 1.0)
        if n == "espejos":
            for i in range(3): put(sfx, impact() * 0.6, a + 0.25 + i * 0.35, 0.8); put(sfx, hp(rng.normal(0, 1, int(SR * 0.3)), 3000) * np.exp(-T(0.3) * 12) * 0.5, a + 0.25 + i * 0.35, 1.0)
        if n == "rayos": put(sfx, buzz(D * 0.8), a + 0.2, 1.0); put(sfx, sting(1.2), a + D * 0.55, 0.8)
        if n == "prohibido": put(sfx, impact(), a + D * 0.55, 0.9); put(sfx, heartbeat(3, 90), a, 0.6)
        if n == "mirada": put(sfx, heartbeat(5, 120), a, 0.9); put(sfx, riser(D * 0.7), a, 0.7); put(sfx, boom(2.0, 40), a + D * 0.75, 1.1)
        if n in ("mundo", "jaula"): put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.25, a, 1.0)
        if n == "gigante": put(sfx, boom(2.5, 45), a + 0.2, 1.1); put(sfx, scream(1.5) * 0.6, a + D * 0.5, 0.7)
        if n == "linterna": put(sfx, beep(0.05, 3000), a + D * 0.65, 1.0); put(sfx, shimmer(), a + D * 0.65, 1.0)
        if n == "destellos":
            for h in (0.3, 0.55, 0.8): put(sfx, boom(0.8, 90), a + D * h, 1.0); put(sfx, shimmer() * 0.8, a + D * h, 1.0)
            put(sfx, scream(D * 0.6) * 0.6, a + D * 0.32, 0.6)
        if n == "rescate": put(sfx, impact(), a + D * 0.15, 1.0); put(sfx, whoosh(0.5, False), a + D * 0.18, 0.8); put(sfx, chime() * 0.5, a + D * 0.6, 1.0)
        if n == "puerta":
            for i in range(int(D / 0.19)): put(sfx, step(), a + i * 0.19, 0.9)
            put(sfx, riser(D), a, 0.6)
        if n == "giro" and os.environ.get("EP") == "3":
            t_ = T(D * 0.6); put(sfx, lp(rng.normal(0, 1, len(t_)), 1500) * 0.15, a, 1.0)
            put(sfx, sting(1.4), a + D * 0.68, 1.1); put(sfx, boom(), a + D * 0.68, 1.0)
        if n == "giro" and os.environ.get("EP") == "2":
            tt = a + 0.2
            while tt < a + D * 0.2: put(sfx, beep(), tt, 1.0); tt += 0.625
            put(sfx, beep(D * 0.42, 1000) * 0.9, a + D * 0.2, 1.0)
            put(sfx, sting(1.4), a + D * 0.62, 1.1); put(sfx, boom(), a + D * 0.62, 1.0)
    mus = musica(total, cuts)
    # ducking de música y efectos bajo la voz
    vol = np.convolve(np.abs(mixv), np.ones(2400) / 2400, mode="same")
    duck = 1 - 0.45 * np.clip(vol / 0.05, 0, 1)
    mix = mixv * 1.0 + sfx * 0.55 * (0.6 + 0.4 * duck) + mus * duck * 0.9
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    st = np.stack([mix, mix], 1)
    wavfile.write(os.path.join(out, "audio.wav"), SR, (st / max(1e-9, np.abs(st).max()) * 0.95 * 32767).astype(np.int16))
    print("audio", round(total, 2))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
