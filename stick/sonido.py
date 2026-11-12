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
    cs = cuts.get("amanecer") or cuts.get("encerrado") or cuts.get("cinta") or (0.0, 0.0)
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

# ---------- estilos de música (varían por episodio) ----------
def _nota(f, d, kind="pluck", vel=1.0):
    t = T(d)
    if kind == "pluck":    # cuerda pulsada / pizzicato
        return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 7) * vel
    if kind == "piano":    # piano oscuro
        s = sum(np.sin(2 * np.pi * f * k * t) / k ** 1.6 for k in (1, 2, 3, 4))
        return s * np.exp(-t * 2.2) * np.minimum(1, t * 300) * vel
    if kind == "caja":     # caja de música
        s = np.sin(2 * np.pi * f * 2 * t) + 0.3 * np.sin(2 * np.pi * f * 5.4 * t)
        return s * np.exp(-t * 4) * vel
    if kind == "saw":      # sintetizador
        s = 2 * ((f * t) % 1) - 1
        return lp(s, 1800) * np.exp(-t * 5) * vel
    return np.zeros_like(t)

def _reverb(x, dec=0.45):
    out = np.copy(x)
    for d, g in ((0.031, 0.5), (0.053, 0.4), (0.089, 0.32), (0.137, 0.25), (0.21, 0.18)):
        n = int(SR * d); out[n:] += x[:-n] * g * dec * 2
    return out

def musica_estilo(total, cuts, estilo, seed=0):
    t = T(total); out = np.zeros_like(t); r = np.random.default_rng(seed)
    fin = cuts.get("final", (total, total))[0]
    def put_(x, at, g=1.0):
        i = int(at * SR)
        if 0 <= i < len(out): x = x[: len(out) - i]; out[i:i + len(x)] += x * g
    root = 110 * 2 ** (r.integers(-3, 3) / 12)
    menor = [0, 3, 7, 10, 12, 15]; mayor = [0, 4, 7, 11, 12, 14]
    if estilo == "piano":          # piano lento y disonante + dron grave
        out += lp(np.sin(2 * np.pi * root / 2 * t) + 0.6 * np.sin(2 * np.pi * root / 2 * 1.006 * t), 300) * 0.05
        tt = 0.3
        while tt < total - 1:
            f = root * 2 * 2 ** (r.choice([0, 1, 3, 6, 7, 10, 12]) / 12)
            put_(_nota(f, 3.0, "piano"), tt, 0.09); tt += r.choice([0.8, 1.2, 1.6])
        return _reverb(out)
    if estilo == "caja":           # caja de música desafinada + respiración de ruido
        mel = [r.choice(menor) for _ in range(8)]
        tt, k = 0.2, 0
        while tt < total - 0.5:
            f = root * 4 * 2 ** (mel[k % 8] / 12) * (1 + 0.012 * np.sin(tt))
            put_(_nota(f, 1.2, "caja"), tt, 0.05); tt += 0.42; k += 1
        out += lp(r.normal(0, 1, len(t)), 400) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.2 * t)) * 0.02
        return _reverb(out, 0.6)
    if estilo == "persecucion":    # arpegio rápido de sintetizador + bombo a 140
        beat = 60 / 140; arp = [0, 3, 7, 12, 7, 3]
        k = 0; tt = 0.0
        while tt < min(total, fin):
            put_(_nota(root * 2 * 2 ** (arp[k % 6] / 12), 0.2, "saw"), tt, 0.05); k += 1; tt += beat / 2
        for i in range(int(min(total, fin) / beat)):
            put_(boom(0.3, 80) * 0.5, i * beat, 1.0)
            if i % 2: put_(hp(r.normal(0, 1, int(SR * 0.08)), 2000) * np.exp(-T(0.08) * 40) * 0.25, i * beat, 1.0)
        out += lp(np.sin(2 * np.pi * root / 2 * t), 200) * 0.04
        return out
    if estilo == "curioso":        # ligero: pizzicato en mayor + golpes suaves (para curiosidades)
        beat = 60 / 112; prog = [0, 5, 9, 7]
        for i in range(int(total / (beat / 2))):
            tt = i * beat / 2
            ac = prog[(i // 8) % 4]
            f = root * 2 * 2 ** ((ac + mayor[(i * 3) % 4]) / 12)
            put_(_nota(f, 0.4, "pluck"), tt, 0.07 if i % 2 == 0 else 0.045)
            if i % 4 == 0: put_(boom(0.25, 110) * 0.35, tt, 1.0)
            if i % 4 == 2: put_(hp(r.normal(0, 1, int(SR * 0.05)), 3000) * np.exp(-T(0.05) * 60) * 0.18, tt, 1.0)
        return out
    return musica(total, cuts)      # "tension": la de siempre

ESTILOS_TERROR = ["tension", "piano", "caja", "persecucion"]
def elegir_estilo():
    """MUSICA en el guion manda; si no, se elige uno distinto según el episodio (siempre el mismo para ese episodio)"""
    ep = os.environ.get("EP", "")
    if os.environ.get("MUSICA"): return os.environ["MUSICA"]
    try:
        import importlib; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        g = importlib.import_module("guion" + ep + ("_en" if os.environ.get("IDIOMA") == "en" else ""))
        if getattr(g, "MUSICA", None): return g.MUSICA
    except Exception: pass
    if ep.startswith("cur"): return "curioso"
    import zlib
    return ESTILOS_TERROR[zlib.crc32(ep.encode()) % len(ESTILOS_TERROR)]

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
        a, D, n = s["start"], s["D"], s["name"]
        if n == "gancho":
            put(sfx, boom(1.2, 60), a, 1.2); put(sfx, sting(1.0), a, 1.0); put(sfx, static(D), a, 0.5)
            continue
        sr, w = wavfile.read(os.path.join(voz, f"{s.get('voz', k):02d}.wav"))
        put(mixv, w.astype(np.float64) / (np.abs(w).max() + 1e-9) * 0.9, s["start"] + 0.12)
        if k: put(sfx, whoosh(0.35), a - 0.12, 0.6)
        # ---- Curiosidades · 1 ----
        if os.environ.get("EP") == "cur1":
            if n == "agujero": put(sfx, riser(D * 0.45), a, 0.7); put(sfx, impact(), a + D * 0.48, 1.2); put(sfx, boom(1.2, 90), a + D * 0.48, 0.9)
            if n == "picor": put(sfx, riser(D * 0.6), a + D * 0.3, 0.4)
            if n == "tapa": put(sfx, whoosh(0.3), a + D * 0.15, 0.8); put(sfx, whoosh(0.3), a + D * 0.45, 0.8); put(sfx, lp(rng.normal(0, 1, int(SR * D * 0.3)), 200) * 0.6, a + D * 0.7, 1.0)
            if n == "presion": put(sfx, riser(D), a, 0.9); put(sfx, heartbeat(4, 130), a + 0.3, 0.6)
            if n == "pop": put(sfx, impact(), a + D * 0.1, 1.3); put(sfx, sting(1.2) * 0.7, a + D * 0.1, 0.8)
            if n == "hinchado": put(sfx, heartbeat(4, 110), a, 0.7)
            if n == "hospital":
                for i in range(int(D / 0.6)): put(sfx, beep(0.1, 1200), a + 0.2 + i * 0.6, 0.8)
            if n == "sonda":
                for i in range(7): put(sfx, beep(0.06, 900 + i * 60), a + 0.2 + i * D * 0.11, 0.7)
            if n == "final": put(sfx, whoosh(0.5), a + D * 0.42, 1.0); put(sfx, ding(), a + D * 0.65, 0.8)
            continue
        # ---- Si oyes esto a las 3AM · 12 ----
        if os.environ.get("EP") == "3am12":
            obtu_ = lambda: np.concatenate([hp(rng.normal(0, 1, int(SR * 0.03)), 2500) * np.exp(-T(0.03) * 90) * 0.9, np.zeros(int(SR * 0.06)),
                                            bp(rng.normal(0, 1, int(SR * 0.05)), 1500, 6000) * np.exp(-T(0.05) * 60) * 0.7])     # clic de la cámara
            carga_ = lambda d: np.sin(2 * np.pi * np.cumsum(2500 + 5000 * T(d) / d) / SR) * np.minimum(1, T(d) * 10) * 0.05          # pitido del flash cargando
            roce_ = lambda d: lp(rng.normal(0, 1, int(SR * d)), 600) * np.exp(-T(d) * 3) * 0.6                                      # manta
            if n == "corte": put(sfx, sting(1.2) * 0.6, a, 1.0); put(sfx, powerdown(1.2), a + D * 0.22, 1.0); put(sfx, beep(0.08, 1200) * 0.6, a + D * 0.42, 0.8)
            if n == "foto1": put(sfx, carga_(0.3), a - 0.3, 0.8); put(sfx, obtu_(), a, 1.2); put(sfx, heartbeat(3, 80), a + D * 0.5, 0.6)
            if n == "oscuro": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 200) * 0.15, a, 1.0); put(sfx, step() * 1.4, a + D * 0.7, 1.2); put(sfx, heartbeat(4, 110), a + D * 0.3, 0.7)
            if n == "foto2": put(sfx, carga_(0.3), a - 0.3, 0.8); put(sfx, obtu_(), a, 1.2); put(sfx, sting(1.4) * 0.8, a + 0.05, 0.9); put(sfx, step(), a + D * 0.8, 0.9)
            if n == "foto3":
                put(sfx, carga_(0.3), a - 0.3, 0.8); put(sfx, obtu_(), a, 1.2)
                put(sfx, boom(2.0, 55), a + 0.05, 1.3); put(sfx, sting(1.6), a + 0.05, 1.1); put(sfx, scream(1.0) * 0.5, a + 0.1, 0.6)
            if n == "tapas": put(sfx, roce_(0.6), a + 0.05, 1.0); put(sfx, heartbeat(5, 130), a + D * 0.3, 0.8)
            if n == "clic": put(sfx, riser(D * 0.6), a + D * 0.3, 0.5); put(sfx, roce_(0.3) * 0.6, a + D * 0.62, 0.8)
            if n == "galeria":
                put(sfx, carga_(0.35), a - 0.35, 1.0); put(sfx, obtu_(), a, 1.4)
                put(sfx, boom(2.0, 50), a + 0.05, 1.3); put(sfx, sting(1.6), a + 0.05, 1.1); put(sfx, heartbeat(4, 140), a + D * 0.5, 0.7)
            if n == "final": put(sfx, obtu_(), a + 0.02, 1.0); put(sfx, boom(2.2, 45), a + D * 0.45, 1.3); put(sfx, sting(1.4), a + D * 0.45, 1.0)
            continue
        # ---- Si oyes esto a las 3AM · 11 ----
        if os.environ.get("EP") == "3am11":
            def vibra_(d):                                                                       # móvil vibrando
                x = np.sin(2 * np.pi * 160 * T(d)) * (0.6 + 0.4 * np.sin(2 * np.pi * 31 * T(d)))
                return lp(x, 400) * ((T(d) % 0.9) < 0.55) * 0.5
            aviso_ = lambda: np.concatenate([beep(0.07, 1320), np.zeros(int(SR * 0.05)), beep(0.09, 1760)])   # notificación
            tecla_ = lambda: bp(rng.normal(0, 1, int(SR * 0.04)), 2000, 6000) * np.exp(-T(0.04) * 80) * 0.5
            viento_ = lambda d: bp(rng.normal(0, 1, int(SR * d)), 200, 700) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * T(d))) * 0.22
            if n == "mensaje": put(sfx, aviso_(), a + 0.02, 1.0); put(sfx, vibra_(D * 0.5), a, 0.9); put(sfx, sting(1.2) * 0.6, a, 0.9)
            if n == "ayer": put(sfx, viento_(D), a, 0.9); put(sfx, aviso_() * 0.5, a + D * 0.35, 0.6); put(sfx, heartbeat(3, 80), a + D * 0.5, 0.5)
            if n == "leido": put(sfx, beep(0.05, 2000), a + D * 0.25, 0.7); put(sfx, riser(D * 0.5), a + D * 0.5, 0.6)
            if n == "calle": put(sfx, viento_(D), a, 0.8); put(sfx, heartbeat(4, 100), a + D * 0.4, 0.7); put(sfx, sting(1.2) * 0.7, a + D * 0.75, 0.8)
            if n == "escribe":
                put(sfx, aviso_(), a + D * 0.4, 1.0); put(sfx, boom(1.8, 55), a + D * 0.4, 1.2); put(sfx, sting(1.6), a + D * 0.4, 1.0)
                put(sfx, vibra_(D * 0.3), a + D * 0.4, 0.8)
            if n == "manta": put(sfx, lp(rng.normal(0, 1, int(SR * 0.5)), 600) * np.exp(-T(0.5) * 6) * 0.6, a + 0.1, 1.0); put(sfx, heartbeat(5, 120), a + D * 0.3, 0.7)
            if n == "pulgares":
                put(sfx, beep(0.12, 900) * 0.6, a + D * 0.1, 0.8)
                for i in range(9): put(sfx, tecla_(), a + D * 0.3 + i * D * 0.045, 0.9)
                put(sfx, whoosh(0.4), a + D * 0.82, 1.0); put(sfx, sting(1.4), a + D * 0.84, 1.0)
            if n == "bajas":
                for i in range(int(D * 0.95 / 0.9)): put(sfx, step(), a + 0.2 + i * 0.9, 0.9)
                put(sfx, riser(D), a, 0.6)
            if n == "final": put(sfx, lp(rng.normal(0, 1, int(SR * 0.8)), 300) * np.exp(-T(0.8) * 3) * 0.7, a + 0.1, 1.0); put(sfx, boom(2.2, 45), a + D * 0.5, 1.3); put(sfx, sting(1.4), a + D * 0.5, 1.0)
            continue
        # ---- Si oyes esto a las 3AM · 10 ----
        if os.environ.get("EP") == "3am10":
            zumbido_ = lambda d: (np.sin(2 * np.pi * 100 * T(d)) * 0.5 + np.sin(2 * np.pi * 200 * T(d)) * 0.25) * 0.08     # fluorescente
            puertas_ = lambda d: bp(rng.normal(0, 1, int(SR * d)), 300, 1200) * np.minimum(1, T(d) * 8) * np.minimum(1, (d - T(d)) * 8) * 0.35
            golpe_ = lambda: lp(rng.normal(0, 1, int(SR * 0.25)), 500) * np.exp(-T(0.25) * 20) * 1.0 + np.sin(2 * np.pi * 180 * T(0.25)) * np.exp(-T(0.25) * 15) * 0.4
            llave_ = lambda: bp(rng.normal(0, 1, int(SR * 0.12)), 2500, 7000) * np.exp(-T(0.12) * 30) * 0.6
            if n == "panel": put(sfx, ding(), a + 0.05, 1.0); put(sfx, sting(1.2) * 0.6, a, 0.9); put(sfx, zumbido_(D), a, 0.8)
            if n == "abre": put(sfx, puertas_(D * 0.6), a + D * 0.05, 1.0); put(sfx, zumbido_(D), a, 1.0)
            if n == "puerta": put(sfx, zumbido_(D), a, 1.0); put(sfx, heartbeat(3, 90), a + D * 0.5, 0.6)
            if n == "llaves":
                for i in range(5): put(sfx, llave_(), a + D * (0.5 + i * 0.09), 0.8)
            if n == "sales":
                for i in range(int(D * 0.6 / 0.5)): put(sfx, step(), a + 0.1 + i * 0.5, 0.8)
                put(sfx, riser(D * 0.4), a + D * 0.6, 0.6)
            if n == "cara": put(sfx, boom(2.0, 55), a + D * 0.05, 1.3); put(sfx, sting(1.6), a + D * 0.05, 1.1); put(sfx, scream(1.0) * 0.5, a + D * 0.08, 0.6)
            if n == "voz":
                for i in range(int(D * 0.4 / 0.25)): put(sfx, step(), a + i * 0.25, 0.9)
                put(sfx, heartbeat(4, 120), a + D * 0.3, 0.7)
            if n == "cierra":
                put(sfx, puertas_(D * 0.4), a, 1.0); put(sfx, ding(), a + D * 0.55, 0.8)
                for i in range(5): put(sfx, golpe_(), a + D * 0.42 + i * 0.35, 1.0)
            if n == "final": put(sfx, zumbido_(D), a, 0.8); put(sfx, boom(2.2, 45), a + D * 0.5, 1.3); put(sfx, sting(1.4), a + D * 0.5, 1.0)
            continue
        # ---- Si oyes esto a las 3AM · 9 ----
        if os.environ.get("EP") == "3am9":
            viento_ = lambda d: bp(rng.normal(0, 1, int(SR * d)), 200, 700) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * T(d))) * 0.25
            cruje_ = lambda: bp(rng.normal(0, 1, int(SR * 0.22)), 900, 3500) * np.exp(-T(0.22) * 14) * 0.7      # pisada en la nieve
            gota_ = lambda: np.sin(2 * np.pi * (1400 - 900 * T(0.08)) * T(0.08)) * np.exp(-T(0.08) * 50) * 0.5   # plic
            clank_ = lambda: bp(rng.normal(0, 1, int(SR * 0.3)), 1500, 5000) * np.exp(-T(0.3) * 18) + np.sin(2 * np.pi * 2200 * T(0.3)) * np.exp(-T(0.3) * 12) * 0.4
            if n == "ventana": put(sfx, sting(1.2) * 0.6, a, 1.0); put(sfx, viento_(D), a, 0.9)
            if n == "ninguna":
                put(sfx, viento_(D), a, 0.7)
                for i in range(int(D / 0.5)): put(sfx, cruje_(), a + 0.2 + i * 0.5, 0.6)
                put(sfx, heartbeat(3, 90), a + D * 0.65, 0.6)
            if n == "bajas":
                for i in range(int(D * 0.5 / 0.42)): put(sfx, step(), a + 0.1 + i * 0.42, 0.8)
                for i in range(4): put(sfx, gota_(), a + D * (0.45 + i * 0.13), 0.8)
            if n == "cerrojo": put(sfx, clank_(), a + D * 0.32, 1.0); put(sfx, boom(1.4, 60), a + D * 0.33, 0.9); put(sfx, heartbeat(4, 110), a + D * 0.5, 0.7)
            if n == "charcos":
                for i in range(6): put(sfx, gota_(), a + 0.3 + i * D * 0.14, 0.8)
                put(sfx, riser(D), a, 0.5); put(sfx, heartbeat(4, 130), a + D * 0.4, 0.7)
            if n == "cuarto":
                put(sfx, lp(rng.normal(0, 1, int(SR * D)), 200) * 0.25, a, 1.0)
                for i in range(int(D / 0.6)): put(sfx, gota_(), a + 0.2 + i * 0.6, 0.7)
                put(sfx, bp(rng.normal(0, 1, int(SR * 0.4)), 300, 1500) * np.exp(-T(0.4) * 4) * 0.8, a + D * 0.62, 1.0)   # crujido del cuello
                put(sfx, sting(1.2) * 0.7, a + D * 0.7, 0.8)
            if n == "voz":
                put(sfx, boom(2.0, 55), a + D * 0.08, 1.3); put(sfx, sting(1.6), a + D * 0.08, 1.1); put(sfx, scream(1.0) * 0.5, a + D * 0.1, 0.6)
                put(sfx, viento_(D) * 0.6, a, 0.6)
            if n == "final": put(sfx, gota_(), a + 0.4, 0.8); put(sfx, gota_(), a + 1.0, 0.8); put(sfx, boom(2.2, 45), a + D * 0.5, 1.3); put(sfx, sting(1.4), a + D * 0.5, 1.0)
            continue
        # ---- Si oyes esto a las 3AM · 8 ----
        if os.environ.get("EP") == "3am8":
            def vibra_(d):                                                                       # móvil vibrando sobre madera
                x = np.sin(2 * np.pi * 160 * T(d)) * (0.6 + 0.4 * np.sin(2 * np.pi * 31 * T(d)))
                return lp(x, 400) * ((T(d) % 0.9) < 0.55) * 0.5
            def tono_(d, f=440):                                                                 # tono de llamada (tuuu… tuuu…)
                return np.sin(2 * np.pi * f * T(d)) * ((T(d) % 1.6) < 0.8) * 0.18
            def timbre_(d):                                                                      # politono de móvil
                x = np.zeros(int(SR * d)); notas = (988, 1319, 988, 1319, 1175, 0)
                for i in range(int(d / 0.16)):
                    f = notas[i % len(notas)]
                    if f: tn = T(0.13); y = np.sign(np.sin(2 * np.pi * f * tn)) * np.exp(-tn * 8) * 0.12; i0 = int(i * 0.16 * SR); x[i0:i0 + len(y)] += y[: len(x) - i0]
                return lp(x, 3500)
            if n == "entrante": put(sfx, sting(1.2) * 0.6, a, 1.0); put(sfx, vibra_(D), a, 0.9)
            if n == "contestas": put(sfx, static(D) * 0.3, a, 0.5); put(sfx, heartbeat(4, 90), a + D * 0.5, 0.6)
            if n == "broma": put(sfx, beep(0.1, 600), a + D * 0.5, 0.9); put(sfx, beep(0.1, 450), a + D * 0.56, 0.9)
            if n == "devuelves": put(sfx, tono_(D * 0.9), a + 0.2, 0.9)
            if n == "suena":
                put(sfx, tono_(D * 0.3), a, 0.8)
                put(sfx, lp(timbre_(D * 0.7), 1800), a + D * 0.3, 1.0); put(sfx, vibra_(D * 0.7), a + D * 0.3, 0.7)
                put(sfx, boom(1.4, 60), a + D * 0.3, 1.0); put(sfx, sting(1.2), a + D * 0.3, 0.8)
            if n == "coge":
                put(sfx, lp(timbre_(D * 0.45), 1800), a, 0.9)
                put(sfx, bp(rng.normal(0, 1, int(SR * D * 0.3)), 200, 800) * 0.35, a + D * 0.1, 0.7); put(sfx, beep(0.08, 900), a + D * 0.47, 0.8)
                put(sfx, heartbeat(4, 120), a + D * 0.5, 0.8)
            if n == "abajo":
                put(sfx, boom(2.0, 55), a + D * 0.12, 1.3); put(sfx, sting(1.6), a + D * 0.12, 1.1); put(sfx, scream(1.0) * 0.5, a + D * 0.14, 0.6)
                put(sfx, static(D * 0.8) * 0.4, a, 0.5)
            if n == "espera": put(sfx, heartbeat(5, 110), a, 0.8); put(sfx, lp(rng.normal(0, 1, int(SR * D)), 160) * 0.2, a, 1.0)
            if n == "final": put(sfx, lp(timbre_(D * 0.4), 1500), a + D * 0.4, 0.6); put(sfx, boom(2.2, 45), a + D * 0.5, 1.3); put(sfx, sting(1.4), a + D * 0.5, 1.0)
            continue
        # ---- Si oyes esto a las 3AM · 7 ----
        if os.environ.get("EP") == "3am7":
            cruje_ = lambda: bp(rng.normal(0, 1, int(SR * 0.5)), 180, 900) * np.sin(np.pi * T(0.5) / 0.5) * (0.6 + 0.4 * np.sin(2 * np.pi * 23 * T(0.5)))
            tono_ = lambda: (np.sin(2 * np.pi * 425 * T(0.4)) * 0.25) * np.minimum(1, (0.4 - T(0.4)) * 40)       # tono de llamada
            def risa_(n=5, f0=520):                                                                              # risita de payaso, apagada
                out_ = np.zeros(int(SR * (0.16 * n + 0.3)))
                for i in range(n):
                    d = 0.12; x = np.sin(2 * np.pi * (f0 - i * 25) * T(d) * (1 + 0.08 * np.sin(T(d) * 60))) * np.sin(np.pi * T(d) / d)
                    i0 = int(i * 0.16 * SR); out_[i0:i0 + len(x)] += x
                return bp(out_, 300, 2500) * 0.4
            if n == "salon": put(sfx, sting(1.2) * 0.6, a, 1.0); put(sfx, boom(1.6, 50), a, 0.6)
            if n == "cocina":
                for i in range(int(D * 0.4 / 0.4)): put(sfx, step() * 0.7, a + 0.1 + i * 0.4, 0.7)
                put(sfx, sting(1.0) * 0.6, a + D * 0.45, 0.9); put(sfx, heartbeat(4, 100), a + D * 0.5, 0.6)
            if n == "llamas":
                for i in range(2): put(sfx, tono_(), a + D * 0.35 + i * 0.9, 0.8)
                put(sfx, cruje_(), a + D * 0.6, 0.5)
            if n == "padre": put(sfx, static(D) * 0.4, a, 0.5); put(sfx, boom(1.2, 70), a + D * 0.5, 0.8); put(sfx, heartbeat(4, 120), a + D * 0.5, 0.7)
            if n == "vacia": put(sfx, whoosh(0.4), a, 0.8); put(sfx, boom(1.6, 60), a + D * 0.45, 1.1); put(sfx, sting(1.2), a + D * 0.45, 0.9)
            if n == "escalera":
                for i in range(int(D / 0.2)): put(sfx, step(), a + 0.05 + i * 0.2, 0.8)
                for fr in (0.35, 0.55, 0.75, 0.9): put(sfx, cruje_(), a + D * fr, 0.9)
            if n == "detras":
                put(sfx, risa_(), a + D * 0.15, 0.5); put(sfx, heartbeat(3, 130), a, 0.6)
                put(sfx, boom(2.0, 55), a + D * 0.5, 1.3); put(sfx, sting(1.6), a + D * 0.5, 1.1); put(sfx, scream(1.0) * 0.5, a + D * 0.52, 0.7)
            if n == "final": put(sfx, risa_(4, 440), a + D * 0.2, 0.4); put(sfx, boom(2.2, 45), a + D * 0.5, 1.3); put(sfx, sting(1.4), a + D * 0.5, 1.0)
            continue
        # ---- Si oyes esto a las 3AM · 6 ----
        if os.environ.get("EP") == "3am6":
            def nana_(d, g=1.0, f0=440):                     # nana tarareada por el altavoz del vigilabebés (Brahms, dominio público)
                mel = [(4, .5), (4, .5), (7, 1.5), (4, .5), (4, .5), (7, 1.5), (4, .5), (7, .5), (12, 1), (11, 1), (9, 1), (9, 1), (7, 1)]
                out_ = np.zeros(int(SR * d)); tt, k = 0.0, 0
                while tt < d - 0.3:
                    st, du = mel[k % len(mel)]; du *= 0.42
                    tn = T(min(du * 1.3, d - tt)); f = f0 * 2 ** (st / 12) * (1 + 0.01 * np.sin(tt * 3))
                    x = (np.sin(2 * np.pi * f * tn) + 0.25 * np.sin(4 * np.pi * f * tn)) * np.minimum(1, tn * 30) * np.exp(-tn * 1.5)
                    i0 = int(tt * SR); out_[i0:i0 + len(x)] += x[: len(out_) - i0]; tt += du; k += 1
                return (bp(out_, 400, 3000) * 0.35 + static(d)[: len(out_)] * 0.25) * g
            if n == "vigila": put(sfx, sting(1.2) * 0.5, a, 1.0); put(sfx, nana_(D), a, 0.9)
            if n == "solos": put(sfx, nana_(D, f0=415), a, 0.8); put(sfx, heartbeat(3, 80), a + D * 0.3, 0.5)
            if n == "contestas":
                put(sfx, nana_(D * 0.62, f0=440), a, 0.8); put(sfx, beep(0.08, 1500), a + D * 0.27, 1.0)
                put(sfx, static(0.5), a + D * 0.3, 0.6); put(sfx, beep(0.08, 900), a + D * 0.62, 0.8)
            if n == "pasillo":
                for i in range(int(D / 0.3)): put(sfx, step(), a + 0.05 + i * 0.3, 0.8)
                put(sfx, whoosh(0.6, False), a + D * 0.5, 1.2); put(sfx, sting(0.8) * 0.6, a + D * 0.55, 0.8)
            if n == "cuna":
                put(sfx, heartbeat(4, 90), a, 0.6)
                for i in range(int(D / 0.9)): put(sfx, _nota(880 * 2 ** ((0, 4, 7, 4)[i % 4] / 12), 1.0, "caja"), a + 0.2 + i * 0.9, 0.05)   # el móvil de la cuna
            if n == "suena": put(sfx, static(0.6), a + D * 0.45, 0.8); put(sfx, boom(1.4, 70), a + D * 0.5, 0.9); put(sfx, riser(D * 0.5), a + D * 0.5, 0.4)
            if n == "entiendes": put(sfx, impact() * 0.7, a, 0.9); put(sfx, nana_(D, f0=330), a + 0.2, 0.7); put(sfx, heartbeat(4, 130), a + D * 0.2, 0.8)
            if n == "tucama":
                put(sfx, nana_(D * 0.55, f0=300), a, 0.6); put(sfx, bp(rng.normal(0, 1, int(SR * D * 0.3)), 200, 800) * 0.3, a + D * 0.3, 0.6)
                put(sfx, boom(2.0, 55), a + D * 0.55, 1.3); put(sfx, sting(1.6), a + D * 0.55, 1.1); put(sfx, scream(1.0) * 0.5, a + D * 0.57, 0.7)
            if n == "final": put(sfx, nana_(D * 0.5, f0=300), a, 0.6); put(sfx, boom(2.2, 45), a + D * 0.5, 1.3); put(sfx, sting(1.4), a + D * 0.5, 1.0)
            continue
        # ---- Si oyes esto a las 3AM · 5 ----
        if os.environ.get("EP") == "3am5":
            lame_ = lambda: bp(rng.normal(0, 1, int(SR * 0.35)), 250, 1200) * np.sin(np.pi * T(0.35) / 0.35) * 0.7   # lametón húmedo
            gota_ = lambda: np.sin(2 * np.pi * (1400 - 900 * T(0.09) / 0.09) * T(0.09)) * np.exp(-T(0.09) * 40) * 0.5
            if n == "cama":
                put(sfx, sting(1.2) * 0.6, a, 1.0)
                for f_ in (0.52, 0.68, 0.84): put(sfx, lame_(), a + D * f_, 1.0)
            if n == "siempre":
                for f_ in (0.1, 0.35, 0.6): put(sfx, lame_(), a + D * f_, 0.8)
                put(sfx, lp(rng.normal(0, 1, int(SR * D)), 200) * 0.15, a, 1.0)
            if n == "gotea":
                for i in range(int(D / 0.55)): put(sfx, gota_(), a + 0.2 + i * 0.55, 1.0)
                put(sfx, heartbeat(3, 80), a + D * 0.4, 0.6)
            if n == "pasillo":
                for i in range(int(D / 0.42)): put(sfx, step() * 0.7, a + 0.1 + i * 0.42, 0.7); put(sfx, gota_(), a + 0.3 + i * 0.42, 0.8)
                put(sfx, buzz(D) * 0.5, a, 0.6)
            if n == "ducha":
                for i in range(int(D / 0.6)): put(sfx, gota_(), a + 0.1 + i * 0.6, 0.9)
                put(sfx, boom(1.4, 70), a + D * 0.25, 0.9); put(sfx, heartbeat(5, 110), a + D * 0.35, 0.8)
            if n == "espejo":
                put(sfx, bp(rng.normal(0, 1, int(SR * D * 0.45)), 2000, 6000) * 0.12, a + D * 0.2, 0.8)   # dedo en el cristal
                put(sfx, riser(D * 0.4), a + D * 0.5, 0.5)
            if n == "entiendes":
                put(sfx, impact() * 0.7, a, 0.9); put(sfx, lame_(), a + D * 0.3, 1.1); put(sfx, lame_(), a + D * 0.55, 1.1)
                put(sfx, heartbeat(4, 130), a + D * 0.2, 0.8)
            if n == "sale":
                put(sfx, bp(rng.normal(0, 1, int(SR * D * 0.4)), 200, 800) * 0.4, a + D * 0.08, 0.8)   # arrastre
                put(sfx, boom(2.0, 55), a + D * 0.45, 1.3); put(sfx, sting(1.6), a + D * 0.45, 1.1); put(sfx, scream(1.0) * 0.5, a + D * 0.47, 0.7)
                for i in range(6): put(sfx, step(), a + D * 0.5 + i * 0.14, 0.9)
            if n == "final": put(sfx, lame_(), a + D * 0.2, 0.8); put(sfx, boom(2.2, 45), a + D * 0.5, 1.3); put(sfx, sting(1.4), a + D * 0.5, 1.0)
            continue
        # ---- Si oyes esto a las 3AM · 4 ----
        if os.environ.get("EP") == "3am4":
            if n == "pasos":
                put(sfx, sting(1.2) * 0.6, a, 1.0)
                for i in range(6): put(sfx, step(), a + D * 0.3 + i * 0.32, 0.6 + 0.08 * i)
                put(sfx, heartbeat(3, 80), a + D * 0.75, 0.6)
            if n == "mirilla":
                for i in range(int(D * 0.4 / 0.45)): put(sfx, step() * 0.6, a + 0.1 + i * 0.45, 0.6)
                put(sfx, boom(1.6, 60), a + D * 0.5, 1.1); put(sfx, sting(1.4), a + D * 0.5, 0.9)
            if n == "punto": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 160) * 0.25, a, 1.0); put(sfx, heartbeat(5, 90), a + 0.3, 0.8)
            if n == "llamas":
                for i in range(2): put(sfx, beep(0.4, 440) * 0.8, a + 0.6 + i * 0.9, 0.8)
            if n == "recepcion": put(sfx, static(D) * 0.2, a, 0.4); put(sfx, riser(D * 0.6), a + D * 0.4, 0.5)
            if n == "entiendes": put(sfx, powerdown(0.8) * 0.5, a + 0.1, 0.6); put(sfx, heartbeat(5, 120), a + D * 0.3, 0.8)
            if n == "parpadea":
                put(sfx, riser(D * 0.45), a, 0.5)
                put(sfx, bp(rng.normal(0, 1, int(SR * 0.15)), 200, 900) * np.exp(-T(0.15) * 20), a + D * 0.42, 1.0)   # chasquido húmedo
                put(sfx, boom(2.0, 55), a + D * 0.5, 1.3); put(sfx, sting(1.6), a + D * 0.5, 1.1); put(sfx, scream(1.0) * 0.5, a + D * 0.52, 0.7)
            if n == "rendija":
                put(sfx, lp(rng.normal(0, 1, int(SR * D * 0.42)), 120) * 0.2, a, 1.0)
                put(sfx, boom(1.6, 60), a + D * 0.42 + 0.7, 1.2); put(sfx, sting(1.2), a + D * 0.42 + 0.7, 0.9)
            if n == "final": put(sfx, static(D * 0.5) * 0.3, a, 0.4); put(sfx, boom(2.2, 45), a + D * 0.5, 1.3); put(sfx, sting(1.4), a + D * 0.5, 1.0)
            continue
        # ---- Si oyes esto a las 3AM · 1 ----
        if os.environ.get("EP") == "3am2":
            motor_ = lambda d: lp(rng.normal(0, 1, int(SR * d)), 140) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * T(d))) * 0.5
            largas_ = lambda: np.pad(hp(rng.normal(0, 1, int(SR * 0.05)), 2500) * np.exp(-T(0.05) * 80) * 0.9, (0, int(SR * 0.45))) + boom(0.5, 110) * 0.35
            cruj_ = lambda: bp(rng.normal(0, 1, int(SR * 0.35)), 300, 1400) * np.exp(-T(0.35) * 5) * (rng.random(int(SR * 0.35)) > 0.7) * 1.6
            if n == "carretera":
                put(sfx, sting(1.2) * 0.6, a, 1.0); put(sfx, motor_(D), a, 0.8)
                for f_ in (0.55, 0.72, 0.86): put(sfx, largas_(), a + D * f_, 1.0)
            if n == "largas":
                put(sfx, motor_(D), a, 0.8); put(sfx, heartbeat(5, 110), a + 0.3, 0.6)
                for f_ in (0.04, 0.3, 0.53, 0.76): put(sfx, largas_(), a + D * f_, 1.1)
            if n == "cruje":
                put(sfx, motor_(D), a, 0.8)
                for f_ in (0.12, 0.42, 0.7): put(sfx, largas_(), a + D * f_, 1.0); put(sfx, cruj_(), a + D * f_ + 0.08, 1.0)
            if n == "paras":
                put(sfx, motor_(D * 0.5) * np.linspace(1, 0, int(SR * D * 0.5)), a, 0.8)
                put(sfx, bp(rng.normal(0, 1, int(SR * 0.9)), 1500, 5000) * np.linspace(0.6, 0, int(SR * 0.9)), a + 0.3, 0.5)   # frenazo
                put(sfx, impact() * 0.5, a + D * 0.8, 0.6); put(sfx, heartbeat(4, 120), a + D * 0.5, 0.7)
            if n == "conductor":
                put(sfx, impact() * 0.6, a + 0.1, 0.7)   # portazo
                for i in range(int(D * 0.38 / 0.17)): put(sfx, step(), a + 0.3 + i * 0.17, 0.9)
                put(sfx, sting(1.2), a + D * 0.42, 0.7)
                for i in range(3): put(sfx, impact() * 0.5, a + D * (0.5 + i * 0.12), 0.6)   # golpes en el cristal
            if n == "entiendes":
                put(sfx, riser(D * 0.7), a, 0.4); put(sfx, powerdown(0.8) * 0.5, a + D * 0.62, 0.7)
                put(sfx, cruj_(), a + D * 0.75, 1.1); put(sfx, heartbeat(3, 70), a + D * 0.7, 0.8)
            if n == "retrovisor":
                put(sfx, cruj_(), a + D * 0.25, 1.0)
                put(sfx, boom(2.0, 55), a + D * 0.38, 1.3); put(sfx, sting(1.6), a + D * 0.38, 1.1); put(sfx, scream(1.0) * 0.5, a + D * 0.4, 0.7)
            if n == "final": put(sfx, static(D * 0.5) * 0.4, a, 0.4); put(sfx, boom(2.2, 45), a + D * 0.55, 1.3); put(sfx, sting(1.4), a + D * 0.55, 1.0)
            continue
        # ---- Si oyes esto a las 3AM · 3 ----
        if os.environ.get("EP") == "3am3":
            def jingle_():
                o = np.zeros(int(SR * 0.5)); m_ = int(SR * 0.04)
                for i in range(8):
                    j = int(SR * i * 0.05); o[j:j + m_] += hp(rng.normal(0, 1, m_), 5000) * np.exp(-T(0.04)[:m_] * 90)
                return o * 0.9
            click_ = lambda: np.pad(hp(rng.normal(0, 1, int(SR * 0.03)), 1800) * np.exp(-T(0.03) * 120), (0, int(SR * 0.1))) * 1.2
            if n == "timbre":
                put(sfx, sting(1.2) * 0.6, a, 1.0)
                for f_ in (0.3, 0.5, 0.75): put(sfx, ding() * 0.9, a + D * f_, 1.0); put(sfx, ding() * 0.7, a + D * f_ + 0.35, 0.8)
            if n == "recibidor":
                for i in range(int(D * 0.45 / 0.42)): put(sfx, step(), a + 0.1 + i * 0.42, 0.8)
                put(sfx, riser(D * 0.5), a + D * 0.45, 0.4)
            if n == "movil":
                for i in range(3): put(sfx, bp(rng.normal(0, 1, int(SR * 0.25)), 120, 300) * 0.8, a + 0.05 + i * 0.3, 1.0)
                for f_ in (0.2, 0.38, 0.56, 0.74): put(sfx, ding() * 0.5, a + D * f_, 0.8)
                put(sfx, heartbeat(4, 100), a + D * 0.5, 0.7)
            if n == "cuarto":
                for i in range(int(D / 0.13)): put(sfx, click_() * 0.35, a + 0.1 + i * 0.13 + rng.uniform(0, 0.05), 0.6)   # teclea
            if n == "silencio": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 120) * 0.2, a, 1.0); put(sfx, heartbeat(5, 70), a + D * 0.4, 0.8)
            if n == "llavero":
                put(sfx, jingle_(), a + D * 0.32, 1.0); put(sfx, jingle_(), a + D * 0.45, 0.8)
                put(sfx, click_(), a + D * 0.66, 1.0); put(sfx, riser(D * 0.4), a + D * 0.6, 0.5)
            if n == "cerradura":
                for f_ in (0.15, 0.25, 0.38): put(sfx, click_(), a + D * f_, 1.1)
                put(sfx, impact() * 0.5, a + D * 0.4, 0.7); put(sfx, heartbeat(4, 140), a + D * 0.45, 0.8)
            if n == "asoma":
                cr = bp(rng.normal(0, 1, int(SR * D * 0.4)), 400, 1200) * (0.5 + 0.5 * np.sin(2 * np.pi * 18 * T(D * 0.4))) * 0.5
                put(sfx, cr, a, 0.8)   # chirrido de la puerta
                put(sfx, boom(2.0, 55), a + D * 0.4, 1.3); put(sfx, sting(1.6), a + D * 0.4, 1.1); put(sfx, scream(1.0) * 0.5, a + D * 0.42, 0.7)
            if n == "final": put(sfx, static(D * 0.5) * 0.3, a, 0.4); put(sfx, boom(2.2, 45), a + D * 0.5, 1.3); put(sfx, sting(1.4), a + D * 0.5, 1.0)
            continue
        if os.environ.get("EP") == "3am1":
            if n == "llama": put(sfx, sting(1.2) * 0.6, a, 1.0); put(sfx, beep(0.1, 880), a + 0.05, 1.0); put(sfx, beep(0.1, 880), a + 0.3, 1.0)
            if n == "bajas":
                for i in range(int(D / 0.42)): put(sfx, step(), a + 0.1 + i * 0.42, 0.9)
                put(sfx, buzz(D) * 0.6, a, 0.7)
            if n == "movil":
                for i in range(3): put(sfx, bp(rng.normal(0, 1, int(SR * 0.25)), 120, 300) * 0.8, a + 0.05 + i * 0.3, 1.0)
                put(sfx, ding() * 0.7, a + D * 0.25, 1.0); put(sfx, heartbeat(4, 100), a + D * 0.5, 0.7)
            if n == "espalda": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.25, a, 1.0); put(sfx, riser(D * 0.9), a, 0.5)
            if n == "cabeza":
                put(sfx, bp(rng.normal(0, 1, int(SR * 0.4)), 300, 1500) * np.exp(-T(0.4) * 4) * 0.8, a + D * 0.3, 1.0)   # crujido
                put(sfx, boom(2.0, 55), a + D * 0.42, 1.3); put(sfx, sting(1.6), a + D * 0.42, 1.1); put(sfx, scream(1.0) * 0.5, a + D * 0.45, 0.7)
            if n == "subes":
                for i in range(int(D / 0.17)): put(sfx, step(), a + i * 0.17, 0.9)
                put(sfx, heartbeat(4, 160), a, 0.8)
            if n == "abrazo": put(sfx, impact() * 0.7, a, 0.8); put(sfx, heartbeat(3, 120), a + 0.3, 0.6)
            if n == "tuvoz": put(sfx, static(D) * 0.3, a, 0.5); put(sfx, riser(D), a, 0.4)
            if n == "final": put(sfx, step(), a + 0.5, 1.0); put(sfx, step(), a + 1.1, 1.0); put(sfx, boom(2.2, 45), a + D * 0.62, 1.3); put(sfx, sting(1.4), a + D * 0.62, 1.0)
            continue
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
        # ---- episodio 4 ----
        if n == "camara": put(sfx, heartbeat(5, 110), a, 0.8); put(sfx, beep(0.08, 1400), a + D * 0.45, 1.0); put(sfx, static(0.4), a + D * 0.55, 0.6)
        if n == "grabando": put(sfx, buzz(D), a, 0.7); put(sfx, static(D) * 0.3, a, 0.5)
        if n == "sala":
            for i in range(int(D * 0.42 / 0.3)): put(sfx, step(), a + i * 0.3, 0.8)
            put(sfx, boom(1.2, 80), a + D * 0.6, 1.1); put(sfx, impact(), a + D * 0.6, 0.8)
            for i in range(3): put(sfx, beep(0.04, 3200 + 500 * i), a + D * 0.72 + i * 0.07, 0.8)
        if n == "cinta": put(sfx, chime() * 0.5, a, 1.0)
        if n == "tele": put(sfx, static(D * 0.4), a, 0.9); put(sfx, beep(0.05, 600), a + D * 0.4, 1.0); put(sfx, buzz(D * 0.6), a + D * 0.4, 0.6)
        if n == "mensaje": put(sfx, buzz(D) * 0.7, a, 0.6)
        if n == "brigida":
            t_ = T(D); put(sfx, hp(rng.normal(0, 1, len(t_)), 2500) * 0.12, a, 1.0)
            put(sfx, boom(2.4, 40), a + D * 0.3, 1.2)
        if n == "habitacion":
            t_ = T(D * 0.5); f_ = 180 + 120 * np.sin(2 * np.pi * 0.8 * t_)
            put(sfx, bp(np.sign(np.sin(2 * np.pi * np.cumsum(f_) / SR)), 300, 2000) * 0.15 * np.sin(np.pi * t_ / (D * 0.5)), a + D * 0.15, 1.0)
            put(sfx, sting(1.4), a + D * 0.55, 1.0); put(sfx, static(0.5), a + D * 0.55, 0.6)
        if n == "numero": put(sfx, impact(), a + 0.05, 1.0); put(sfx, ding(), a + D * 0.4, 1.0)
        if n == "fallo":
            put(sfx, static(D), a, 0.9)
            for i in range(5): put(sfx, impact() * 0.4, a + D * (0.15 + 0.17 * i), 0.6)
        if n == "ojos": put(sfx, heartbeat(5, 100), a, 0.9); put(sfx, riser(D * 0.9), a, 0.6)
        if n == "apagar":
            for i in range(int(D * 0.75 * 2.2)): put(sfx, beep(0.025, 420), a + i / 2.2, 1.2); put(sfx, static(0.15), a + i / 2.2, 0.5)
        if n == "cable": put(sfx, sting(1.4), a + D * 0.3, 1.0); put(sfx, heartbeat(4, 130), a + D * 0.3, 0.8)
        if n == "voz": put(sfx, static(D), a, 0.6); put(sfx, boom(2.5, 40), a + D * 0.3, 1.2); put(sfx, scream(1.6) * 0.6, a + D * 0.35, 0.7)
        # ---- episodio 5 ----
        if n == "verja":
            t_ = T(D); put(sfx, hp(rng.normal(0, 1, len(t_)), 2500) * 0.12, a, 1.0)
            put(sfx, boom(2.4, 40), a + D * 0.25, 1.2)
            for i in range(int(D * 0.85 / 0.4)): put(sfx, step() * 0.6, a + i * 0.4, 0.7)
        if n == "linternas":
            put(sfx, beep(0.03, 2600), a + 0.05, 0.8); put(sfx, beep(0.03, 2600), a + 0.25, 0.8)
            for i in range(int(D / 0.45)): put(sfx, step() * 0.7, a + i * 0.45, 0.7)
            put(sfx, lp(rng.normal(0, 1, int(SR * D)), 250) * 0.2, a, 1.0)
        if n == "camillas": put(sfx, buzz(D * 0.7), a, 0.7); put(sfx, sting(1.2) * 0.7, a + D * 0.65, 1.0)
        if n == "silla":
            t_ = T(D * 0.75); f_ = 900 + 300 * np.sin(2 * np.pi * 2.2 * t_)
            put(sfx, bp(np.sin(2 * np.pi * np.cumsum(f_) / SR) * (np.sin(2 * np.pi * 2.2 * t_) > 0.3), 600, 3000) * 0.2, a + D * 0.1, 1.0)
            put(sfx, heartbeat(4, 120), a + D * 0.4, 0.8); put(sfx, impact(), a + D * 0.85, 0.8)
        if n == "huida":
            for i in range(int(D / 0.19)): put(sfx, step(), a + i * 0.19, 0.9)
            put(sfx, heartbeat(5, 150), a, 0.7); put(sfx, sting(1.2), a + D * 0.3, 0.9); put(sfx, static(0.5), a + D * 0.3, 0.5)
        if n == "cartel":
            for i in range(int(D * 0.8 / 0.42)): put(sfx, step() * 0.7, a + i * 0.42, 0.7)
            put(sfx, buzz(D) * 0.6, a, 0.6); put(sfx, riser(D * 0.9), a, 0.5)
        if n == "abierta":
            t_ = T(D * 0.5); f_ = 140 + 90 * np.sin(2 * np.pi * 0.9 * t_)
            put(sfx, bp(np.sign(np.sin(2 * np.pi * np.cumsum(f_) / SR)), 300, 2000) * 0.15 * np.sin(np.pi * t_ / (D * 0.5)), a + D * 0.15, 1.0)
            put(sfx, impact() * 0.5, a + D * 0.62, 0.7)
        if n == "dibujos": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.25, a, 1.0); put(sfx, shimmer() * 0.6, a + 0.3, 0.8)
        if n == "fecha": put(sfx, sting(1.4), a + D * 0.45, 1.0); put(sfx, boom(1.5, 60), a + D * 0.45, 0.9)
        if n == "ultimo": put(sfx, heartbeat(4, 110), a, 0.8); put(sfx, boom(2.2, 45), a + D * 0.4, 1.1); put(sfx, static(0.6), a + D * 0.4, 0.6)
        if n == "pasos":
            for i in range(int(D / 0.7)): put(sfx, boom(0.4, 70) * (0.4 + 0.6 * i / max(1, D / 0.7)), a + 0.2 + i * 0.7, 0.8)
        if n == "escondite":
            for i in range(int(D * 0.5 / 0.19)): put(sfx, step(), a + i * 0.19, 0.8)
            put(sfx, beep(0.03, 2600), a + D * 0.62, 1.0); put(sfx, beep(0.03, 2400), a + D * 0.66, 1.0)
            put(sfx, heartbeat(3, 130), a + D * 0.65, 0.8)
        if n == "sombra":
            put(sfx, heartbeat(6, 140), a, 0.9); put(sfx, riser(D * 0.9), a, 0.6)
            for i in range(3): put(sfx, boom(0.4, 70) * 0.5, a + 0.2 + i * 0.6, 0.7)
        if n == "anciana": put(sfx, impact(), a, 1.0); put(sfx, boom(2.0, 50), a, 1.1); put(sfx, sting(1.4) * 0.7, a + D * 0.05, 0.9); put(sfx, chime() * 0.4, a + D * 0.5, 1.0)
        # ---- episodio 6 ----
        if n == "superviviente": put(sfx, impact(), a, 0.9); put(sfx, heartbeat(5, 90), a + 0.3, 0.7); put(sfx, lp(rng.normal(0, 1, int(SR * D)), 250) * 0.2, a, 1.0)
        if n == "quedan": put(sfx, beep(0.03, 2600), a + D * 0.45, 0.8); put(sfx, chime() * 0.35, a + D * 0.5, 1.0)
        if n == "foto": put(sfx, whoosh(0.4), a + 0.05, 0.8); put(sfx, sting(1.2) * 0.6, a + D * 0.5, 0.9)
        if n == "ninya":
            put(sfx, static(D) * 0.25, a, 0.6); put(sfx, shimmer() * 0.5, a + 0.2, 0.8)
            put(sfx, sting(1.2) * 0.7, a + D * 0.5, 0.9)
        if n == "festin": put(sfx, riser(D * 0.85), a, 0.8); put(sfx, heartbeat(6, 150), a, 0.8); put(sfx, scream(1.4) * 0.6, a + D * 0.7, 0.8); put(sfx, boom(2.2, 45), a + D * 0.85, 1.1)
        if n == "tiembla": put(sfx, heartbeat(6, 130), a, 0.9); put(sfx, buzz(D) * 0.7, a, 0.6); put(sfx, riser(D * 0.8), a + D * 0.2, 0.5)
        if n == "calma": put(sfx, whoosh(0.8, False), a + D * 0.45, 0.8); put(sfx, chime() * 0.5, a + D * 0.6, 1.0)
        if n == "secreto": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.2, a, 1.0); put(sfx, shimmer(), a + D * 0.55, 1.0)
        if n == "nombre_luz": put(sfx, riser(D * 0.55), a, 0.6); put(sfx, scream(1.2) * 0.7, a + D * 0.6, 0.8); put(sfx, boom(2.0, 55), a + D * 0.7, 1.0); put(sfx, shimmer(), a + D * 0.72, 1.0)
        if n == "olvido": put(sfx, whoosh(1.0, False), a + D * 0.25, 0.7); put(sfx, sting(1.4) * 0.5, a + D * 0.6, 0.8)
        if n == "movil":
            for i in range(3): put(sfx, buzz(0.35) * 2.5, a + 0.1 + i * 0.5, 1.0)
            put(sfx, beep(0.1, 1300), a + D * 0.3, 1.0); put(sfx, impact() * 0.6, a + D * 0.32, 0.8)
        if n == "sala_vacia":
            for i in range(int(D * 0.6 / 0.3)): put(sfx, step(), a + i * 0.3, 0.8)
            put(sfx, buzz(D) * 0.8, a, 0.7); put(sfx, boom(1.2, 80), a + D * 0.4, 0.9)
        if n == "llave": put(sfx, heartbeat(4, 120), a, 0.8); put(sfx, sting(1.4), a + D * 0.62, 1.0); put(sfx, boom(2.2, 45), a + D * 0.65, 1.1)
        if n == "huella": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.25, a, 1.0); put(sfx, boom(2.4, 40), a + D * 0.55, 1.2); put(sfx, static(0.7), a + D * 0.55, 0.7); put(sfx, scream(1.4) * 0.5, a + D * 0.6, 0.6)
        # ---- episodio 7 ----
        if n == "busqueda": put(sfx, impact(), a, 0.9); put(sfx, lp(rng.normal(0, 1, int(SR * D)), 250) * 0.2, a, 1.0); put(sfx, sting(1.2) * 0.6, a + D * 0.4, 0.8)
        if n == "sotano":
            for i in range(int(D * 0.75 / 0.3)): put(sfx, step(), a + i * 0.3, 0.8)
            put(sfx, buzz(D) * 0.5, a, 0.6); put(sfx, whoosh(0.9, False), a + D * 0.5, 0.7)
        if n == "estanterias": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 400) * 0.25, a, 1.0); put(sfx, heartbeat(3, 80), a + 0.3, 0.6)
        if n == "carpeta": put(sfx, whoosh(0.5), a + D * 0.35, 0.9); put(sfx, ding(), a + D * 0.6, 0.8); put(sfx, impact() * 0.5, a + D * 0.6, 0.7)
        if n == "ficha": put(sfx, whoosh(0.4), a + 0.05, 0.8); put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.2, a, 1.0)
        if n == "tachado":
            for i in range(10): put(sfx, bp(rng.normal(0, 1, int(SR * 0.09)), 1500, 5000) * np.exp(-T(0.09) * 20) * 0.5, a + D * 0.15 + i * 0.11, 1.0)
            put(sfx, sting(1.2) * 0.5, a + D * 0.7, 0.8)
        if n == "letra": put(sfx, riser(D * 0.4), a, 0.6); put(sfx, shimmer(), a + D * 0.45, 1.2); put(sfx, boom(1.4, 70), a + D * 0.45, 0.8)
        if n == "foto_nino": put(sfx, static(D) * 0.25, a, 0.6); put(sfx, chime() * 0.4, a + 0.3, 1.0); put(sfx, chime() * 0.3, a + D * 0.6, 1.0)
        if n == "apagon":
            for i in range(5): put(sfx, buzz(0.12) * 2, a + D * 0.25 + i * 0.16, 1.0)
            put(sfx, powerdown(1.2), a + D * 0.6, 0.9); put(sfx, heartbeat(4, 120), a + D * 0.65, 0.8)
        if n == "sabe": put(sfx, boom(2.2, 45), a, 1.2); put(sfx, sting(1.6), a, 1.0); put(sfx, riser(D * 0.6), a + 0.2, 0.6); put(sfx, static(0.6), a + D * 0.75, 0.6)
        if n == "huida" and os.environ.get("EP") == "7":
            for i in range(8): put(sfx, whoosh(0.3, i % 2 == 0), a + 0.2 + i * D / 9, 0.5)
        if n == "vuelta114":
            for i in range(int(D * 0.7 / 0.19)): put(sfx, step(), a + i * 0.19, 0.8)
            put(sfx, impact() * 0.6, a + D * 0.72, 0.8)
        if n == "tachados":
            for i in range(14): put(sfx, bp(rng.normal(0, 1, int(SR * 0.08)), 1500, 5000) * np.exp(-T(0.08) * 20) * 0.45, a + D * 0.1 + i * 0.12, 1.0)
            put(sfx, sting(1.4), a + D * 0.5, 1.0); put(sfx, heartbeat(5, 140), a + D * 0.4, 0.8)
        if n == "menos": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.25, a, 1.0); put(sfx, boom(2.4, 40), a + D * 0.72, 1.2); put(sfx, scream(1.4) * 0.5, a + D * 0.75, 0.6); put(sfx, static(0.7), a + D * 0.72, 0.7)
        # ---- episodio 8 ----
        if n == "dormidos": put(sfx, impact(), a, 0.9); put(sfx, lp(rng.normal(0, 1, int(SR * D)), 250) * 0.25, a, 1.0); put(sfx, chime() * 0.3, a + D * 0.4, 1.0)
        if n == "corren":
            for i in range(int(D / 0.16)): put(sfx, step(), a + i * 0.16, 0.9)
            put(sfx, heartbeat(4, 130), a, 0.6)
        if n == "cabezas":
            for i in range(6): put(sfx, bp(rng.normal(0, 1, int(SR * 0.12)), 300, 1500) * np.exp(-T(0.12) * 25) * 0.6, a + D * 0.2 + i * D * 0.11, 1.0)
            put(sfx, sting(1.2) * 0.5, a + D * 0.7, 0.8)
        if n == "persigue":
            put(sfx, boom(2.2, 45), a, 1.2); put(sfx, sting(1.6), a + 0.1, 1.0); put(sfx, riser(D * 0.7), a + 0.2, 0.6)
            for i in range(int(D / 0.3)): put(sfx, boom(0.3, 55) * 0.6, a + i * 0.3, 0.9)
        if n == "placa":
            for i in range(int(D * 0.6 / 0.2)): put(sfx, step(), a + i * 0.2, 0.8)
            put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.2, a, 1.0)
        if n == "tomas":
            for i in range(6): put(sfx, bp(rng.normal(0, 1, int(SR * 0.15)), 800, 3000) * np.sin(np.pi * T(0.15) / 0.15) * 0.3, a + D * 0.05 + i * 0.13, 1.0)
            put(sfx, riser(D * 0.4), a + D * 0.2, 0.6); put(sfx, shimmer(), a + D * 0.6, 1.2); put(sfx, boom(1.4, 70), a + D * 0.6, 0.8)
        if n == "coche":
            for i in range(int(D * 0.8 / 0.17)): put(sfx, step(), a + i * 0.17, 0.8)
            put(sfx, impact() * 0.5, a + D * 0.8, 0.8)
        if n == "vacio": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.25, a, 1.0); put(sfx, boom(2.4, 40), a + D * 0.6, 1.2); put(sfx, scream(1.2) * 0.4, a + D * 0.62, 0.6); put(sfx, static(0.6), a + D * 0.6, 0.7)
        # ---- episodio 9 ----
        if n == "faro_lejos": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.25, a, 1.0); put(sfx, powerdown(1.0)[::-1].copy(), a + D * 0.4 - 1.0, 0.6); put(sfx, boom(1.6, 60), a + D * 0.4, 1.1); put(sfx, shimmer(), a + D * 0.42, 0.8)
        if n == "puerta_faro":
            for i in range(int(D * 0.6 / 0.3)): put(sfx, step(), a + i * 0.3, 0.8)
            for i in range(5): put(sfx, bp(rng.normal(0, 1, int(SR * 0.1)), 1500, 5000) * np.exp(-T(0.1) * 20) * 0.4, a + D * 0.05 + i * 0.13, 1.0)
            put(sfx, lp(rng.normal(0, 1, int(SR * 1.2)), 500) * np.linspace(0, 0.5, int(SR * 1.2)), a + D * 0.55, 0.8); put(sfx, sting(1.2) * 0.5, a + D * 0.6, 0.8)
        if n == "escalones":
            for i in range(int(D * 0.95 / 0.17)): put(sfx, step(), a + i * 0.17, 0.85)
            put(sfx, heartbeat(5, 130), a, 0.6)
        if n == "voz_arriba": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.25, a, 1.0); put(sfx, riser(D * 0.6), a + 0.2, 0.5)
        if n == "sala_faro":
            for i in range(int(D * 0.75 / 0.4)): put(sfx, step(), a + i * 0.4, 0.7)
            put(sfx, buzz(D) * 0.4, a, 0.6); put(sfx, heartbeat(4, 90), a + D * 0.4, 0.6)
        if n == "hombro": put(sfx, heartbeat(5, 120), a, 0.8); put(sfx, sting(1.2) * 0.6, a + D * 0.72, 0.9); put(sfx, static(0.4), a + D * 0.72, 0.5)
        if n == "giro" and os.environ.get("EP") == "9":
            put(sfx, boom(2.4, 40), a + D * 0.25, 1.2); put(sfx, sting(1.6), a + D * 0.25, 1.0); put(sfx, scream(1.4) * 0.5, a + D * 0.3, 0.6)
            put(sfx, riser(D * 0.5), a + D * 0.35, 0.6); put(sfx, static(0.7), a + D * 0.8, 0.7)
        # ---- episodio 10 ----
        if n == "acorralados":
            put(sfx, heartbeat(5, 120), a, 0.7); put(sfx, sting(1.2) * 0.6, a + 0.1, 0.8)
            for i in range(int(D * 0.5 / 0.17)): put(sfx, step(), a + D * 0.45 + i * 0.17, 0.85)
        if n == "atascada":
            for i in range(6): put(sfx, impact() * 0.35, a + 0.15 + i * D * 0.14, 0.8)
            put(sfx, riser(D * 0.9), a, 0.6); put(sfx, heartbeat(4, 140), a, 0.6)
        if n == "luz_faro":
            put(sfx, impact(), a + D * 0.4, 1.0); put(sfx, boom(2.2, 55), a + D * 0.42, 1.2); put(sfx, shimmer(), a + D * 0.42, 1.2)
            put(sfx, scream(1.4) * 0.6, a + D * 0.45, 0.7)
        if n == "tomas_grito": put(sfx, buzz(D) * 0.4, a, 0.6); put(sfx, riser(D * 0.6), a, 0.6); put(sfx, boom(1.6, 70), a + D * 0.65, 1.1); put(sfx, shimmer(), a + D * 0.65, 1.2)
        if n == "encoge": put(sfx, scream(D * 0.8) * 0.6, a, 0.7); put(sfx, whoosh(D * 0.8, up=False), a + 0.1, 0.8); put(sfx, chime(), a + D * 0.85, 1.0)
        if n == "nino": put(sfx, shimmer() * 0.7, a, 0.8); put(sfx, chime() * 0.6, a + D * 0.5, 0.7)
        if n == "giro" and os.environ.get("EP") == "10":
            put(sfx, heartbeat(4, 80), a, 0.6); put(sfx, static(0.5) * 0.6, a + D * 0.6, 0.6); put(sfx, sting(1.4) * 0.7, a + D * 0.75, 0.9)
        # ---- episodio 11 (final de temporada 1) ----
        if n == "descansa": put(sfx, buzz(D) * 0.25, a, 0.5); put(sfx, chime() * 0.5, a + D * 0.55, 0.7)
        if n == "hacia_luz":
            for i in range(int(D * 0.5 / 0.35)): put(sfx, step() * 0.5, a + D * 0.15 + i * 0.35, 0.6)
            put(sfx, riser(D * 0.5), a + D * 0.2, 0.5); put(sfx, shimmer(), a + D * 0.66, 1.2); put(sfx, chime(), a + D * 0.7, 1.0)
        if n == "despiertan":
            put(sfx, shimmer() * 0.6, a, 0.8)
            for i in range(8): put(sfx, bp(rng.normal(0, 1, int(SR * 0.12)), 300, 1500) * np.exp(-T(0.12) * 25) * 0.4, a + D * (0.22 + 0.07 * i), 0.8)
        if n == "galeria":
            put(sfx, lp(rng.normal(0, 1, int(SR * D)), 400) * 0.25, a, 1.0)    # mar
            for i in range(int(D * 0.5 / 0.17)): put(sfx, step(), a + D * 0.25 + i * 0.17, 0.8)
        if n == "carmen_vive": put(sfx, chime() * 0.7, a + D * 0.3, 0.8); put(sfx, shimmer() * 0.5, a + D * 0.35, 0.6)
        if n == "otra_ciudad": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 250) * 0.25, a, 1.0); put(sfx, heartbeat(4, 70), a + D * 0.4, 0.5)
        if n == "giro" and os.environ.get("EP") == "11":
            put(sfx, heartbeat(5, 110), a, 0.6); put(sfx, riser(D * 0.5), a + D * 0.1, 0.6)
            put(sfx, boom(2.4, 40), a + D * 0.58, 1.2); put(sfx, sting(1.6), a + D * 0.58, 1.0); put(sfx, static(0.7), a + D * 0.75, 0.7)
        # ---- episodio 12 (temporada 2: el Asomado) ----
        def tap_(): return bp(rng.normal(0, 1, int(SR * 0.05)), 1800, 6000) * np.exp(-T(0.05) * 90) * 0.9   # uña contra el cristal
        if n == "asomado": put(sfx, sting(1.2) * 0.8, a, 1.0); put(sfx, heartbeat(3, 90), a + 0.3, 0.6)
        if n == "llegada":
            put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.25, a, 1.0)   # viento
            for i in range(int(D * 0.85 / 0.4)): put(sfx, step() * 0.6, a + i * 0.4, 0.7)
        if n == "lucia": put(sfx, buzz(D) * 0.2, a, 0.5); put(sfx, heartbeat(3, 70), a + D * 0.3, 0.5)
        if n == "dedos":
            for i in range(9): put(sfx, tap_(), a + D * 0.2 + i * 0.13 + (i % 3) * 0.05, 0.9)
            put(sfx, riser(D * 0.7), a + D * 0.2, 0.5)
        if n == "muecas":
            put(sfx, static(D) * 0.5, a, 0.6); put(sfx, heartbeat(6, 140), a, 0.7); put(sfx, sting(1.2), a + D * 0.45, 1.0)
            put(sfx, impact() * 0.6, a + D * 0.48, 0.9)
        if n == "aguanta": put(sfx, whoosh(D * 0.6, up=False) * 0.5, a + D * 0.2, 0.6); put(sfx, heartbeat(3, 60), a + D * 0.5, 0.4)
        if n == "giro" and os.environ.get("EP") == "12":
            put(sfx, lp(rng.normal(0, 1, int(SR * D)), 500) * 0.3, a, 1.0)    # viento por la ventana abierta
            put(sfx, riser(D * 0.5), a + D * 0.15, 0.6); put(sfx, boom(2.2, 45), a + D * 0.62, 1.2); put(sfx, sting(1.4), a + D * 0.62, 1.0)
        # ---- episodio 13 (la fábrica de cristal) ----
        if n == "vaho": put(sfx, sting(1.2) * 0.8, a, 1.0); put(sfx, heartbeat(3, 100), a + 0.3, 0.6)
        if n == "rastro":
            for i in range(int(D * 0.9 / 0.17)): put(sfx, step(), a + i * 0.17, 0.8)
            for i in range(5): put(sfx, tap_(), a + D * (0.1 + i * 0.13), 0.7)
        if n == "fabrica": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.25, a, 1.0); put(sfx, buzz(D * 0.6) * 0.3, a + D * 0.35, 0.5); put(sfx, boom(1.4, 60), a + D * 0.4, 0.8)
        if n == "reflejos":
            for i in range(3): put(sfx, impact() * 0.5, a + i * D / 3.2, 0.9); put(sfx, shimmer() * 0.5, a + i * D / 3.2, 0.7)
            put(sfx, heartbeat(5, 130), a, 0.6)
        if n == "huyen_cristal":
            for i in range(int(D * 0.95 / 0.17)): put(sfx, step(), a + i * 0.17, 0.85)
            put(sfx, riser(D * 0.6), a, 0.5); put(sfx, sting(1.0) * 0.6, a + D * 0.45, 0.8)
        if n == "sala_paneles":
            for i in range(int(D * 0.6 / 0.35)): put(sfx, step() * 0.6, a + i * 0.35, 0.7)
            put(sfx, buzz(D) * 0.25, a, 0.5)
        if n == "giro" and os.environ.get("EP") == "13":
            for i in range(4): put(sfx, beep(0.06, 120) * 2, a + D * (0.1 + 0.05 * i), 0.7)   # fluorescentes
            put(sfx, buzz(D * 0.7) * 0.4, a + D * 0.3, 0.6); put(sfx, riser(D * 0.4), a + D * 0.35, 0.6)
            put(sfx, boom(2.2, 45), a + D * 0.72, 1.2); put(sfx, sting(1.4), a + D * 0.72, 1.0)
        # ---- episodio 14 (sin cristal) ----
        def cristal_(): return hp(rng.normal(0, 1, int(SR * 0.9)), 2500) * np.exp(-T(0.9) * 6) * 0.9  # cristal que estalla
        if n == "rompe":
            put(sfx, heartbeat(3, 120), a, 0.6); put(sfx, whoosh(0.4), a + D * 0.42 - 0.4, 0.7)
            put(sfx, cristal_(), a + D * 0.42, 1.1); put(sfx, shimmer() * 0.4, a + D * 0.42, 1.0); put(sfx, impact(), a + D * 0.42, 1.0)
        if n == "libre": put(sfx, heartbeat(3, 80), a, 0.5); put(sfx, chime() * 0.4, a + D * 0.65, 0.5)
        if n == "sale":
            for i in range(6): put(sfx, tap_() * 0.6, a + D * (0.1 + i * 0.1), 0.7)
            put(sfx, riser(D * 0.7), a, 0.6); put(sfx, sting(1.2), a + D * 0.75, 1.0)
        if n == "ciego": put(sfx, lp(rng.normal(0, 1, int(SR * D)), 400) * 0.3, a, 0.8); put(sfx, heartbeat(4, 70), a + 0.2, 0.5)
        if n == "aliento":
            for i in range(4): put(sfx, lp(rng.normal(0, 1, int(SR * 0.5)), 700) * np.sin(np.pi * T(0.5) / 0.5) * 0.3, a + i * 0.6, 0.6)  # respiraciones
            put(sfx, sting(1.0) * 0.7, a + D * 0.55, 0.9)
        if n == "aguantan": put(sfx, heartbeat(6, 120), a, 0.8); put(sfx, riser(D * 0.8) * 0.6, a + D * 0.1, 0.5)
        if n == "giro" and os.environ.get("EP") == "14":
            put(sfx, buzz(D * 0.5) * 0.3, a, 0.5); put(sfx, riser(D * 0.5), a + D * 0.1, 0.6)
            put(sfx, boom(2.2, 45), a + D * 0.58, 1.2); put(sfx, sting(1.4), a + D * 0.58, 1.0); put(sfx, static(0.6), a + D * 0.62, 0.6)
        # ---- episodio 15 (el cristalero) ----
        if n == "escapan":
            for i in range(int(D * 0.95 / 0.17)): put(sfx, step(), a + i * 0.17, 0.85)
            put(sfx, sting(1.2) * 0.8, a, 1.0); put(sfx, heartbeat(4, 130), a + 0.3, 0.6)
        if n == "portal":
            put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.25, a, 1.0)
            put(sfx, bp(rng.normal(0, 1, int(SR * 0.6)), 200, 900) * np.exp(-T(0.6) * 5) * 0.5, a + D * 0.12, 0.7)   # puerta que cruje
            put(sfx, chime() * 0.5, a + D * 0.15, 0.6)
        if n == "ventanas":
            for i in range(4): put(sfx, shimmer() * 0.35, a + D * (0.1 + 0.2 * i), 0.5)
        if n == "marcas":
            for i in range(6): put(sfx, tap_(), a + D * (0.12 + 0.13 * i), 0.8)
            put(sfx, riser(D * 0.7) * 0.6, a + D * 0.2, 0.5); put(sfx, sting(1.0) * 0.6, a + D * 0.7, 0.8)
        if n == "pacto": put(sfx, buzz(D) * 0.25, a, 0.5); put(sfx, heartbeat(5, 90), a + 0.2, 0.6); put(sfx, sting(1.2) * 0.7, a + D * 0.5, 0.8)
        if n == "encerrados":
            put(sfx, impact(), a + D * 0.25, 1.1); put(sfx, beep(0.05, 300) * 2, a + D * 0.25 + 0.15, 0.8)   # portazo y llave
            for i in range(5): put(sfx, impact() * 0.4, a + D * 0.3 + i * 0.32, 0.6); put(sfx, shimmer() * 0.4, a + D * (0.35 + 0.08 * i), 0.6)
            put(sfx, riser(D * 0.5), a + D * 0.3, 0.6); put(sfx, sting(1.4), a + D * 0.8, 1.0)
        if n == "giro" and os.environ.get("EP") == "15":
            put(sfx, whoosh(0.5, up=False), a + D * 0.15, 0.7); put(sfx, heartbeat(4, 60), a + D * 0.2, 0.5)
            put(sfx, boom(2.2, 45), a + D * 0.45, 1.2); put(sfx, sting(1.4), a + D * 0.45, 1.0); put(sfx, tap_(), a + D * 0.65, 0.9)
        # ---- episodio 16 (el primer cristal) ----
        if n == "fabricado":
            put(sfx, sting(1.2) * 0.8, a, 1.0); put(sfx, buzz(D) * 0.25, a, 0.5)
            for i in range(4): put(sfx, shimmer() * 0.4, a + D * (0.1 + 0.2 * i), 0.6)
        if n == "confesion":
            put(sfx, bp(rng.normal(0, 1, int(SR * 0.6)), 200, 900) * np.exp(-T(0.6) * 5) * 0.5, a + D * 0.05, 0.7)   # puerta que cruje
            put(sfx, heartbeat(4, 80), a + D * 0.3, 0.5)
        if n == "feria":
            put(sfx, lp(rng.normal(0, 1, int(SR * D)), 300) * 0.25, a, 1.0)
            for i in range(3): put(sfx, bp(rng.normal(0, 1, int(SR * 0.7)), 120, 500) * np.exp(-T(0.7) * 3) * 0.4, a + D * (0.15 + 0.3 * i), 0.6)   # noria que chirría
            put(sfx, chime() * 0.4, a + D * 0.6, 0.5)
        if n == "casa_risa":
            for i in range(int(D * 0.95 / 0.4)): put(sfx, step(), a + i * 0.4, 0.6)
            for i in range(3): put(sfx, shimmer() * 0.4, a + D * (0.2 + 0.25 * i), 0.5)
        if n == "sonrien":
            put(sfx, sting(1.0) * 0.7, a + D * 0.28, 0.9); put(sfx, riser(D * 0.6) * 0.6, a + D * 0.2, 0.5)
            put(sfx, static(0.4), a + D * 0.72, 0.7); put(sfx, impact() * 0.6, a + D * 0.72, 0.8)
        if n == "primero":
            put(sfx, whoosh(0.5, up=False), a + D * 0.2, 0.7); put(sfx, heartbeat(4, 70), a + D * 0.3, 0.5)
            for i in range(3): put(sfx, tap_(), a + D * (0.6 + 0.1 * i), 0.8)
        if n == "giro" and os.environ.get("EP") == "16":
            for i in range(6): put(sfx, bp(rng.normal(0, 1, int(SR * 0.25)), 2000, 6000) * np.exp(-T(0.25) * 6) * 0.25, a + D * 0.08 * i, 0.5)   # dedo en el cristal
            put(sfx, riser(D * 0.5), a + D * 0.05, 0.6)
            put(sfx, boom(2.2, 45), a + D * 0.55, 1.2); put(sfx, sting(1.4), a + D * 0.55, 1.0); put(sfx, static(0.5), a + D * 0.6, 0.6)
        # ---- episodio 17 (la trampa) ----
        if n == "cebo":
            put(sfx, sting(1.2) * 0.8, a, 1.0); put(sfx, buzz(D) * 0.2, a, 0.5)
            for i in range(3): put(sfx, static(0.2), a + D * (0.35 + 0.2 * i), 0.5)
        if n == "tapan":
            for i in range(6): put(sfx, whoosh(0.4, up=False), a + D * (0.05 + 0.13 * i), 0.5)
            for i in range(int(D * 0.95 / 0.3)): put(sfx, step(), a + i * 0.3, 0.5)
        if n == "espera":
            put(sfx, heartbeat(5, 70), a + 0.2, 0.7); put(sfx, lp(rng.normal(0, 1, int(SR * D)), 200) * 0.2, a, 1.0)
        if n == "llega":
            put(sfx, riser(D * 0.5) * 0.7, a, 0.5); put(sfx, sting(1.2), a + D * 0.5, 1.0); put(sfx, impact() * 0.7, a + D * 0.5, 0.9)
        if n == "aporrea":
            for i in range(int(D / 0.35)): put(sfx, impact() * 0.5, a + i * 0.35, 0.6)            # golpes en el cristal
            put(sfx, heartbeat(6, 140), a, 0.5)
        if n == "feliz":
            put(sfx, chime() * 0.6, a + D * 0.3, 0.7); put(sfx, shimmer() * 0.5, a + D * 0.35, 0.5)
        if n == "giro" and os.environ.get("EP") == "17":
            put(sfx, chime() * 0.4, a, 0.5); put(sfx, whoosh(0.6), a + D * 0.28, 0.8)
            put(sfx, boom(2.2, 45), a + D * 0.3, 1.2); put(sfx, sting(1.4), a + D * 0.3, 1.0); put(sfx, scream(0.8) * 0.5, a + D * 0.7, 0.7)
        # ---- episodio 18 (el último cristal, final de temporada 2) ----
        if n == "agarrada":
            put(sfx, sting(1.2) * 0.8, a, 1.0); put(sfx, heartbeat(6, 130), a, 0.6)
            for i in range(3): put(sfx, static(0.2), a + D * (0.2 + 0.25 * i), 0.5)
        if n == "alba":
            put(sfx, riser(D * 0.6) * 0.7, a, 0.6); put(sfx, shimmer() * 0.6, a + D * 0.2, 0.6)
            put(sfx, whoosh(0.5), a + D * 0.5, 0.8)
        if n == "raja":
            put(sfx, impact(), a, 1.1); put(sfx, hp(rng.normal(0, 1, int(SR * 0.8)), 3000) * np.exp(-T(0.8) * 5) * 0.4, a + 0.05, 0.8)
            put(sfx, scream(0.7) * 0.5, a + D * 0.2, 0.6); put(sfx, whoosh(0.4, up=False), a + D * 0.4, 0.6)
        if n == "estalla":
            put(sfx, whoosh(0.4), a, 0.7); put(sfx, boom(2.2, 45), a + D * 0.2, 1.3); put(sfx, impact(), a + D * 0.2, 1.1)
            for i in range(10): put(sfx, bp(rng.normal(0, 1, int(SR * 0.15)), 3000, 8000) * np.exp(-T(0.15) * 20) * 0.4, a + D * (0.25 + 0.05 * i), 0.6)
        if n == "despiertos":
            put(sfx, impact() * 0.6, a + D * 0.3, 0.8); put(sfx, chime() * 0.6, a + D * 0.45, 0.7); put(sfx, shimmer() * 0.5, a + D * 0.5, 0.5)
        if n == "casa_lucia":
            put(sfx, chime() * 0.5, a + D * 0.2, 0.6)
            for i in range(int(D * 0.6 / 0.17)): put(sfx, step(), a + i * 0.17, 0.6)
        if n == "su_sombra":
            put(sfx, beep(0.05, 600), a + D * 0.24, 0.6); put(sfx, lp(rng.normal(0, 1, int(SR * D)), 200) * 0.2, a + D * 0.25, 1.0)
            put(sfx, sting(1.4), a + D * 0.55, 1.0); put(sfx, boom(2.0, 45), a + D * 0.55, 1.1); put(sfx, static(0.5), a + D * 0.6, 0.6)
        # ---- episodio 19 (Lucía no tiene sombra, inicio de la temporada 3) ----
        if n == "sombra_viva":
            put(sfx, lp(rng.normal(0, 1, int(SR * D)), 200) * 0.25, a, 1.0); put(sfx, whoosh(0.6, up=False), a + D * 0.15, 0.6)
            put(sfx, sting(1.2), a + D * 0.55, 1.0); put(sfx, static(0.4), a + D * 0.6, 0.5)
        if n == "llamada":
            for i in range(3): put(sfx, beep(0.4, 440), a + 0.1 + i * 0.7, 0.5)
            put(sfx, heartbeat(5, 120), a, 0.5)
        if n == "viaje":
            put(sfx, lp(rng.normal(0, 1, int(SR * D)), 140) * 0.5, a, 0.8)
            for i in range(4): put(sfx, buzz(0.25) * 0.6, a + D * (0.2 + 0.2 * i), 0.5); put(sfx, beep(0.04, 300), a + D * (0.22 + 0.2 * i), 0.5)
        if n == "sombras_calle":
            put(sfx, lp(rng.normal(0, 1, int(SR * D)), 180) * 0.3, a, 0.9)
            for i in range(int(D / 0.5)): put(sfx, step() * 0.7, a + i * 0.5, 0.5)
            for i in range(3): put(sfx, whoosh(0.3, up=False) * 0.6, a + D * (0.25 + 0.15 * i), 0.5)
        if n == "cuarto19":
            put(sfx, chime() * 0.4, a + D * 0.2, 0.5)
        if n == "sin_sombra":
            put(sfx, riser(D * 0.55) * 0.6, a, 0.6); put(sfx, impact() * 0.7, a + D * 0.58, 0.9); put(sfx, heartbeat(4, 110), a + D * 0.6, 0.6)
        if n == "nora_sombra":
            put(sfx, sting(1.4), a + D * 0.28, 1.0); put(sfx, boom(2.2, 45), a + D * 0.3, 1.2)
            put(sfx, whoosh(0.6), a + D * 0.55, 0.8); put(sfx, static(0.5), a + D * 0.6, 0.6)
    # voz con más pegada: compresión, presencia y algo de cuerpo (ffmpeg)
    import subprocess, tempfile
    with tempfile.TemporaryDirectory() as td:
        wavfile.write(os.path.join(td, "v.wav"), SR, (mixv / (np.abs(mixv).max() + 1e-9) * 0.9 * 32767).astype(np.int16))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(td, "v.wav"), "-af",
                        "highpass=f=75,acompressor=threshold=-24dB:ratio=4:attack=3:release=80:makeup=4,"
                        "equalizer=f=170:t=q:w=1:g=2,equalizer=f=3000:t=q:w=1.2:g=4,deesser=i=0.35,"
                        "aecho=0.9:0.4:28:0.12,alimiter=limit=0.95", os.path.join(td, "v2.wav")], check=True)
        _, v2 = wavfile.read(os.path.join(td, "v2.wav"))
        v2 = v2.astype(np.float64) / 32767
        mixv = np.zeros(N); mixv[:min(N, len(v2))] = v2[:N]
    estilo = elegir_estilo(); import zlib
    mus = musica_estilo(total, cuts, estilo, seed=zlib.crc32(os.environ.get('EP', '').encode()) % 1000)
    print('música:', estilo)
    # ducking de música y efectos bajo la voz
    vol = np.convolve(np.abs(mixv), np.ones(2400) / 2400, mode="same")
    duck = 1 - 0.7 * np.clip(vol / 0.04, 0, 1)
    duck = np.convolve(duck, np.ones(4800) / 4800, mode="same")   # sin cortes bruscos
    mix = mixv * 1.25 + sfx * 0.45 * (0.45 + 0.55 * duck) + mus * duck * 0.45
    mix = np.tanh(mix * 0.8) / np.tanh(0.8)
    st = np.stack([mix, mix], 1)
    wavfile.write(os.path.join(out, "audio.wav"), SR, (st / max(1e-9, np.abs(st).max()) * 0.95 * 32767).astype(np.int16))
    print("audio", round(total, 2))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
