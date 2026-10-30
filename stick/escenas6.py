"""Escenas del episodio 6 (La abuela Carmen): la historia de Carmen en la 114, flashback de 1986, el nombre verdadero
y la sala de rayos X vacía."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from motor import *
from escenas import base, GOLD
from escenas2 import enemy, big
from escenas3 import cara_sonriente, LILA, YEL
from escenas4 import radiacion
from escenas5 import (iluminar, linterna_mano, LIN, cuarto114, pared_dibujos, dibujo, papel, stick_cera, cama_hosp,
                      ojos_oscuridad, CERA_NEGRA, CERA_ROJA, CERA_LILA, ROJO)

SIT6 = pose(l1u=80, l1l=-100, l2u=70, l2l=-95, a1u=30, a1l=40, a2u=-20, a2l=40, body=6)
NINA = Fig(shirt=(210, 70, 80), limb=(240, 232, 220), scale=0.8)
SOMBRA = Fig(shirt=(10, 10, 14), limb=(10, 10, 14), scale=1.0)
CERA_GRIS = (110, 110, 118)
FONDO114 = ((40, 46, 40), (16, 18, 16))

def coletas(F, J, sc=0.8, col=(110, 70, 40)):
    hx, hy = J["head"]; r = L["head"] * sc
    for s_ in (-1, 1):
        F.line([(hx + s_ * r * 0.85, hy - r * 0.4), (hx + s_ * r * 1.6, hy + r * 0.2), (hx + s_ * r * 1.45, hy + r * 0.8)], col, 8 * sc)
    F.d.chord([*F.P(hx - r - 2, hy - r - 3), *F.P(hx + r + 2, hy + r - 8)], 180, 360, fill=col)

def sepia(img, k=1.0, fi=0):
    a = np.asarray(img, np.float32)
    g = a @ np.array([0.299, 0.587, 0.114], np.float32)
    s = np.stack([g * 1.07 + 18, g * 0.86 + 10, g * 0.62], -1)
    out = a * (1 - k) + s * k
    r = random.Random(fi // 2)                      # rayas de película vieja
    for _ in range(2):
        x = r.randint(0, W - 3); out[:, x:x + 2] = out[:, x:x + 2] * 0.6 + 60
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def letras(F, cx, cy, n, t, alpha=1.0, spread=1.0, size=110, col=YEL, seed=0):
    r = random.Random(seed)
    for k in range(n):
        x = cx + (k - (n - 1) / 2) * 120 * spread + 10 * noise(t * 2, k + seed)
        y = cy + 30 * math.sin(t * 2.2 + k) + r.uniform(-20, 20) * spread
        c = tuple(int(v * alpha) for v in col)
        F.text((x, y), "?", size, c, stroke=6, scol=(0, 0, 0))

def sala114(F, seed=0, cols=6, rows=3):
    cuarto114(F)
    pared_dibujos(F, 60, 420, cols, rows, seed=seed)

# ---------- escenas ----------
def superviviente(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient(*FONDO114), dict(x=lerp(540, 600, zp), y=lerp(1020, 1060, zp), z=lerp(1.12, 1.3, zp)))
    sala114(F, seed=21)
    cama_hosp(F, 470, 1300, w=460)
    out = ease(seg(t, D * 0.3, D * 0.75))
    LEO.draw(F, pose(l1u=0, l2u=0, a1u=160, a2u=150), lerp(400, 520, out), 1300, f=1, rot=-90, snap=False, face="scared")
    NORA.draw(F, pose(l1u=0, l2u=0, a1u=160, a2u=150), lerp(330, 450, out), 1250, f=1, rot=-90, snap=False, face="scared")
    J = big(CARMEN, 1.15, F, add(pose(body=14, head=-8, a1u=80, a1l=0), jitter(t, 1.2, 3)), 820, 1300, f=-1, face="neutral", t=t)
    h_ = linterna_mano(F, J, 170)
    img = iluminar(F.finish(), F, [(h_[0], h_[1], 900, 0.32)], glows=[(J["head"], 170, 0.75)], amb=0.2, warm=(255, 250, 220))
    return img, dict(grain=10, flash=((255, 255, 240), 0.5 * (1 - seg(t, 0, 0.3))))

def quedan(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient(*FONDO114), dict(x=540, y=lerp(1040, 1080, zp), z=lerp(1.2, 1.32, zp)))
    sala114(F, seed=5)
    sitp = ease(seg(t, 0, D * 0.4))
    NORA.draw(F, mix(STAND, SIT6, sitp), 270, 1300, f=1, face="scared")
    LEO.draw(F, mix(STAND, SIT6, sitp), 420, 1300, f=1, face="neutral")
    big(CARMEN, 1.05, F, add(pose(body=10, a1u=40, a1l=60), jitter(t, 1, 2)), 760, 1300, f=-1, face="talk" if t > D * 0.5 else "neutral", t=t)
    # linterna en el suelo, apuntando al techo
    F.rect(560, 1270, 600, 1300, fill=(60, 60, 70)); F.circle((580, 1266), 12, fill=(255, 250, 220))
    img = iluminar(F.finish(), F, [((580, 1262), math.radians(-90), 900, 0.5)], glows=[((580, 1200), 380, 0.55)], amb=0.18)
    return img, dict(grain=10)

def foto(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient((22, 24, 22), (8, 9, 8)), dict(x=540, y=900, z=lerp(1.0, 1.12, zp)))
    up = ease_out(seg(t, 0, D * 0.25))
    cy = lerp(1500, 860, up); ang = lerp(-12, -3, up)
    # mano de Carmen sujetando la foto
    F.line([(900, cy + 560), (720, cy + 420)], (230, 224, 216), 40)
    papel(F, 540, cy, 640, 760, ang, col=(232, 226, 206))
    F.rect(260, cy - 330, 820, cy + 180, fill=(120, 96, 70))
    F.rect(260, cy + 60, 820, cy + 180, fill=(84, 66, 48))
    Fs = F
    J = big(NINA, 1.7, Fs, pose(a1u=95, a1l=-20, a2u=-95, a2l=20, head=-6), 470, cy + 160, f=1, face="happy")
    coletas(Fs, J, 1.7)
    papel(Fs, 620, cy - 40, 170, 210, 4)
    stick_cera(Fs, 620, cy + 40, 150, CERA_NEGRA, 3, malo=True)
    p = ease_back(seg(t, D * 0.5, D * 0.7))
    if p > 0: F.text((540, cy + 290), "1986", 90 * p, (120, 60, 40))
    img = iluminar(F.finish(), F, [], glows=[((540, 860), 520, 1.0)], amb=0.15, warm=(255, 230, 180))
    return sepia(img, 0.25, fi), dict(grain=10)

def ninya(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient((70, 70, 64), (40, 40, 36)), dict(x=540, y=lerp(1020, 1060, zp), z=lerp(1.15, 1.3, zp)))
    cuarto114(F)
    n_draw = int(4 + 14 * seg(t, 0, D * 0.8))
    r = random.Random(4)
    for k in range(n_draw):
        dibujo(F, 80 + (k % 6) * 170 + (k // 6 % 2) * 30, 440 + (k // 6) * 200, 120, 150, 70 + k)
    cama_hosp(F, 980, 1300, w=380)
    draw_p = pose(body=40, head=20, a1u=120, a1l=-30 + 20 * math.sin(t * 9), a2u=40, a2l=60, l1u=80, l1l=-110, l2u=70, l2l=-100)
    J = NINA.draw(F, draw_p, 600, 1300, f=1, face="neutral")
    coletas(F, J)
    papel(F, 760, 1290, 150, 30, 0)
    # algo mira desde la puerta
    a = ease(seg(t, D * 0.45, D * 0.75))
    F.rect(150, 640, 400, 1300, fill=(10, 10, 12))
    if a > 0: ojos_oscuridad(F, (275, 900), 60, a)
    img = sepia(F.finish(), 1.0, fi)
    return img, dict(grain=14, dark=0.05)

def festin(t, D, fi):
    gp = ease(seg(t, 0, D * 0.9))
    sh = 10 * gp
    F = Frame(gradient((60, 56, 50), (20, 18, 16)), dict(x=540, y=lerp(1050, 900, gp), z=lerp(1.25, 0.95, gp), sx=noise(t * 30) * sh, sy=noise(t * 30, 2) * sh))
    cuarto114(F)
    pared_dibujos(F, 60, 420, 6, 3, seed=70)
    cama_hosp(F, 360, 1300, w=380)
    J = NINA.draw(F, add(pose(body=-6, a1u=150, a1l=40, a2u=140, a2l=45, l1u=14, l1l=-18, l2u=-12, l2l=-14), jitter(t, 6, 1)), 400, 1300, f=1, face="scared")
    coletas(F, J)
    sc = lerp(1.0, 3.4, gp)
    enemy(F, add(pose(a1u=60 + 30 * gp, a1l=40, a2u=-70, a2l=-30, body=-10 * gp, head=-10), jitter(t, 2, 4)), 760, 1300, sc, f=-1)
    img = sepia(F.finish(), 0.85, fi)
    return img, dict(grain=14, tint=((255, 0, 30), 0.25 * gp), glitch=0.3 if gp > 0.7 and fi % 4 == 0 else 0)

def _sombra_pared(F, t, k):
    """sombra con sonrisa que crece en la pared (k = tamaño 0-1)"""
    if k <= 0.02: return
    sc = lerp(0.6, 2.6, k)
    J = SOMBRA.joints(pose(a1u=120, a1l=30, a2u=-120, a2l=-30, head=6), 900, 1180, f=-1)
    old = SOMBRA.scale; SOMBRA.scale = sc
    J = SOMBRA.draw(F, add(pose(a1u=120, a1l=30, a2u=-120, a2l=-30, head=6), jitter(t, 2, 6)), 860, 1220, f=-1, face="closed")
    SOMBRA.scale = old
    ojos_oscuridad(F, J["head"], L["head"] * sc * 1.0, min(1, k * 1.6))

def tiembla(t, D, fi):
    k = ease(seg(t, D * 0.2, D * 0.95))
    F = Frame(gradient(*FONDO114), dict(x=lerp(500, 600, k), y=lerp(1060, 980, k), z=lerp(1.3, 1.05, k)))
    sala114(F, seed=5, cols=4)
    _sombra_pared(F, t, k)
    NORA.draw(F, add(SIT6, add(pose(a1u=130, a1l=60, a2u=120, a2l=60, head=8), jitter(t, 5, 2))), 300, 1300, f=1, face="scared")
    LEO.draw(F, SIT6, 450, 1300, f=1, face="scared")
    F.rect(560, 1270, 600, 1300, fill=(60, 60, 70)); F.circle((580, 1266), 12, fill=(255, 250, 220))
    flick = 0.55 + 0.3 * (noise(t * 14, 5) > -0.2) - 0.25 * k
    img = iluminar(F.finish(), F, [((580, 1262), math.radians(-90), 900, 0.5)], glows=[((580, 1200), 360, max(0.15, flick))], amb=0.14)
    return img, dict(grain=11, tint=((255, 0, 30), 0.14 * k), glitch=0.2 if k > 0.7 and fi % 6 == 0 else 0)

def calma(t, D, fi):
    hp_ = ease(seg(t, 0, D * 0.35)); k = 1 - ease(seg(t, D * 0.4, D * 0.9))
    F = Frame(gradient(*FONDO114), dict(x=lerp(560, 520, hp_), y=1040, z=lerp(1.1, 1.3, hp_)))
    sala114(F, seed=5, cols=4)
    _sombra_pared(F, t, k * 0.9)
    J = big(CARMEN, 1.05, F, mix(pose(body=10), pose(body=36, head=-6, a1u=110, a1l=10), hp_), 520, 1300, f=-1, face="neutral", t=t)
    calm_j = jitter(t, 5 * (1 - hp_), 2)
    NORA.draw(F, add(mix(pose(a1u=130, a1l=60, a2u=120, a2l=60, head=8), pose(a1u=70, a1l=0, head=-4), hp_), add(SIT6, calm_j)), 330, 1300, f=1,
              face="scared" if hp_ < 0.8 else "closed" if t < D * 0.75 else "neutral")
    F.rect(640, 1270, 680, 1300, fill=(60, 60, 70)); F.circle((660, 1266), 12, fill=(255, 250, 220))
    img = iluminar(F.finish(), F, [((660, 1262), math.radians(-90), 900, 0.5)], glows=[((450, 1150), lerp(250, 420, 1 - k), 0.6)], amb=0.18,
                   warm=(255, 230, 190))
    return img, dict(grain=10, tint=((255, 0, 30), 0.1 * k))

def secreto(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient(*FONDO114), dict(x=540, y=lerp(900, 860, zp), z=lerp(1.6, 1.85, zp)))
    sala114(F, seed=9)
    J = big(CARMEN, 1.6, F, add(pose(body=4, a1u=60, a1l=70, a2u=-10, a2l=10), jitter(t, 1, 2)), 640, 1300, f=-1,
            face="talk" if t > D * 0.5 else "neutral", t=t)
    a = ease(seg(t, D * 0.55, D * 0.85))
    if a > 0: letras(F, 520, 640, 5, t, a, spread=0.8, size=90)
    img = iluminar(F.finish(), F, [], glows=[(J["head"], 260, 0.9), ((520, 640), 380 * a + 1, 0.8 * a)], amb=0.18, warm=(255, 240, 200))
    return img, dict(grain=9)

def nombre_luz(t, D, fi):
    F = Frame(gradient((20, 18, 34), (8, 8, 14)), dict(x=480, y=1080, z=1.3))
    F.rect(-400, 1300, 1500, 2600, fill=(10, 10, 16)); F.line([(-400, 1300), (1500, 1300)], (50, 50, 70), 5)
    J = LEO.draw(F, LIN, 250, 1300, f=1, face="angry")
    NORA.draw(F, pose(a1u=60, a1l=20, head=-6), 160, 1300, f=1, face="talk", t=t)
    h_ = linterna_mano(F, J, -6)
    fly = seg(t, D * 0.15, D * 0.6)
    burn = ease(seg(t, D * 0.55, D * 0.9))
    for k in range(5):
        pk = clamp(fly * 1.6 - k * 0.15)
        if pk <= 0: continue
        x = lerp(330, 760, ease(pk)); y = 1000 - 20 * math.sin(pk * math.pi + k)
        F.text((x, y), "?", 80, YEL, stroke=5)
    if burn < 1:
        r = random.Random(fi // 2)
        sx_ = 780 + (r.uniform(-8, 8) * burn)
        enemy(F, add(pose(a1u=150 * burn, a1l=40, a2u=-150 * burn, a2l=-40, body=-15 * burn), jitter(t, 3, 4)), sx_, 1300, 1.25 * (1 - 0.5 * burn), f=-1)
        if burn > 0:
            for _ in range(int(40 * burn)):
                F.circle((sx_ + r.uniform(-120, 120), 1300 - r.uniform(0, 400) * (1 - 0.5 * burn)), r.uniform(4, 10), fill=LILA)
    img = iluminar(F.finish(), F, [(h_[0], h_[1], 900, 0.22)], glows=[((780, 1100), 300 * burn + 1, burn)], amb=0.35, warm=(255, 250, 220))
    return img, dict(grain=8, flash=((255, 255, 240), 0.35 * math.exp(-abs(t - D * 0.7) * 10)))

def olvido(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient(*FONDO114), dict(x=560, y=lerp(920, 900, zp), z=lerp(1.5, 1.65, zp)))
    sala114(F, seed=12)
    J = big(CARMEN, 1.5, F, add(pose(body=14, head=18, a1u=30, a1l=120), jitter(t, 1, 3)), 640, 1300, f=-1, face="closed")
    fade = ease(seg(t, D * 0.2, D * 0.85))
    letras(F, 560, 620, 5, t, 1 - fade, spread=0.8 + fade, size=90)
    r = random.Random(fi // 3)
    for _ in range(int(60 * fade)):
        F.circle((r.uniform(260, 860), lerp(600, 1250, r.random() * fade)), r.uniform(2, 6), fill=(200, 180, 90))
    img = iluminar(F.finish(), F, [], glows=[(J["head"], 260, 0.75)], amb=0.18)
    return img, dict(grain=10)

def movil(t, D, fi):
    vib = noise(t * 60) * 10 * (seg(t, 0.1, 0.3) - seg(t, D * 0.7, D * 0.8))
    zp = ease(t / D)
    F = Frame(gradient((14, 14, 18), (6, 6, 8)), dict(x=540, y=900, z=lerp(1.0, 1.15, zp)))
    F.line([(140, 1700), (360, 1220)], (235, 60, 60), 70)                      # brazo de Leo
    F.circle((420, 1150), 60, fill=(240, 240, 240))
    cx, cy = 540 + vib, 860
    F.rect(cx - 220, cy - 400, cx + 220, cy + 400, fill=(24, 24, 30), outline=(90, 90, 100), w=8)
    F.rect(cx - 195, cy - 360, cx + 195, cy + 360, fill=(40, 60, 110))
    p = ease_back(seg(t, D * 0.25, D * 0.45))
    if p > 0:
        F.rect(cx - 175, cy - 220, cx + 175, cy + 40, fill=(245, 245, 250), outline=(200, 30, 40), w=6 * p)
        F.text((cx, cy - 160), "HOSPITAL", 54 * p + 1, (40, 40, 50))
        F.text((cx, cy - 60), tr("URGENTE"), 62 * p + 1, (210, 30, 40))
        radiacion(F, (cx, cy + 200), 60 * p + 1)
    img = iluminar(F.finish(), F, [], glows=[((cx, cy), 520, 1.0)], amb=0.25, warm=(170, 200, 255))
    return img, dict(grain=8, tint=((255, 0, 30), 0.08 * p))

def _sala_rx(F, op=1.0):
    F.rect(-400, 1300, 1500, 2600, fill=(40, 50, 54)); F.line([(-400, 1300), (1500, 1300)], (80, 96, 100), 6)
    F.rect(-400, 1040, 1500, 1060, fill=(70, 90, 96))
    F.rect(540, 680, 860, 1300, fill=(80, 90, 96))
    F.rect(560, 700, 840, 1300, fill=(4, 4, 6))
    F.rect(560, 590, 840, 660, fill=(200, 30, 40)); F.text((700, 625), tr("RAYOS X"), 44, (255, 255, 255))
    w = lerp(280, 50, op)
    F.poly([(560, 700), (560 + w, 700 - 40 * op), (560 + w, 1300 + 40 * op), (560, 1300)], fill=(150, 160, 164), outline=(90, 100, 104), w=6)
    if w > 140: radiacion(F, (560 + w / 2, 960), 60 * w / 280)

def sala_vacia(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient((60, 80, 86), (34, 44, 50)), dict(x=lerp(560, 600, zp), y=lerp(1020, 1000, zp), z=lerp(1.1, 1.25, zp)))
    _sala_rx(F, ease(seg(t, D * 0.1, D * 0.5)))
    w = ease(seg(t, 0, D * 0.6))
    Jl = LEO.draw(F, walk(t, 0.8) if w < 1 else STAND, lerp(-80, 430, w), 1300, f=1, face="scared")
    NORA.draw(F, walk(t + 0.3, 0.8) if w < 1 else SCARED, lerp(-200, 310, w), 1300, f=1, face="scared")
    big(CARMEN, 0.92, F, walk(t, 0.5) if w < 1 else STAND, lerp(-320, 190, w), 1300, f=1, face="neutral")
    flick = noise(t * 12, 3) > -0.4
    return F.finish(), dict(dark=0.1 if flick else 0.45, grain=10)

def llave(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient((40, 50, 56), (16, 20, 24)), dict(x=lerp(700, 640, zp), y=lerp(1180, 1120, zp), z=lerp(2.0, 1.5, zp)))
    F.rect(-400, 1300, 1500, 2600, fill=(40, 50, 54)); F.line([(-400, 1300), (1500, 1300)], (80, 96, 100), 6)
    F.rect(320, 700, 1300, 1300, fill=(22, 26, 30))
    F.rect(380, 820, 640, 1000, fill=(60, 70, 80), outline=(120, 130, 140), w=5)            # máquina de rayos X
    F.line([(510, 1000), (510, 1300)], (90, 100, 110), 14)
    F.rect(760, 1140, 1180, 1180, fill=(150, 160, 164)); F.line([(780, 1180), (780, 1300)], (100, 110, 116), 10); F.line([(1160, 1180), (1160, 1300)], (100, 110, 116), 10)
    F.rect(790, 1110, 1150, 1140, fill=(200, 200, 190))                                       # camilla vacía
    kx = 640
    F.circle((kx, 1288), 13, outline=GOLD, w=6); F.line([(kx + 12, 1288), (kx + 50, 1288)], GOLD, 6)
    F.line([(kx + 40, 1288), (kx + 40, 1298)], GOLD, 5); F.line([(kx + 50, 1288), (kx + 50, 1298)], GOLD, 5)
    sw = 600 * math.sin(t * 1.4)
    img = iluminar(F.finish(), F, [((300, 1100), math.radians(-6 + 8 * math.sin(t * 1.4)), 1200, 0.32)], glows=[((kx, 1288), 90, 0.9)], amb=0.18)
    pk = math.exp(-abs(t - D * 0.65) * 8)
    return img, dict(grain=11, tint=((255, 0, 30), 0.12 * pk), flash=((255, 30, 40), 0.25 * pk))

def huella(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient((18, 20, 22), (6, 7, 8)), dict(x=540, y=lerp(880, 900, zp), z=lerp(1.0, 1.14, zp)))
    F.rect(180, 300, 900, 1360, fill=(170, 120, 70), outline=(110, 76, 40), w=8)
    F.rect(400, 270, 680, 340, fill=(150, 150, 160), outline=(90, 90, 100), w=5)
    F.rect(230, 380, 850, 1310, fill=(244, 242, 232))
    for k in range(4): F.line([(280, 440 + k * 50), (lerp(560, 800, (k * 37 % 10) / 10), 440 + k * 50)], (150, 160, 190), 6)
    stick_cera(F, 400, 1180, 460, CERA_GRIS, 5)
    F.line([(470, 860), (480, 1180)], (120, 80, 40), 10)            # bastón
    F.circle((400, 790), 26, fill=CERA_GRIS)                          # moño
    F.text((400, 1240), "CARMEN", 56, CERA_GRIS)
    ap = ease(seg(t, D * 0.45, D * 0.75))
    if ap > 0: stick_cera(F, 660 + 10 * noise(t * 3), 1180, lerp(200, 640, ap), CERA_NEGRA, 9, malo=True)
    img = iluminar(F.finish(), F, [], glows=[((540, 820), 560, 1.0)], amb=0.12)
    return img, dict(grain=10, tint=((255, 0, 30), 0.18 * ap), glitch=0.3 if ap > 0.85 and fi % 4 == 0 else 0,
                     flash=((255, 30, 40), 0.3 * math.exp(-abs(t - D * 0.6) * 9)))

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    big(CARMEN, 2.0, F, STAND, 540, 1500, f=-1, face="neutral")
    img = F.finish(); d = ImageDraw.Draw(img)
    d.text((540, 460), tr("PARTE 7"), font=font(190), fill=YEL, anchor="mm", stroke_width=14, stroke_fill=(0, 0, 0))
    return img, {}

ESCENA_FN = dict(superviviente=superviviente, quedan=quedan, foto=foto, ninya=ninya, festin=festin, tiembla=tiembla, calma=calma,
                 secreto=secreto, nombre_luz=nombre_luz, olvido=olvido, movil=movil, sala_vacia=sala_vacia, llave=llave, huella=huella, final=final)
PAUSA = dict(superviviente=0.5, quedan=0.4, foto=0.5, ninya=0.5, festin=0.8, tiembla=0.6, calma=0.5, secreto=0.8, nombre_luz=0.6,
             olvido=0.5, movil=0.5, sala_vacia=0.5, llave=0.8, huella=1.2, final=2.0)
