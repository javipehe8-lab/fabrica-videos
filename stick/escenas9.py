"""Escenas del episodio 9 (El cebo): el faro se enciende solo, sonrisas dibujadas en la puerta y en los 114 escalones,
la voz falsa de Carmen y, arriba, el Sonriente esperándolos con la cara de Carmen."""
import math, random
from PIL import ImageDraw
from motor import *
from escenas import base
from escenas2 import enemy, big, faro_draw, acantilado, sala_lampara, FL
from escenas5 import iluminar

TIZA = (236, 236, 228)

def sonrisa_tiza(F, cx, cy, s=1.0, col=TIZA, k=1.0):
    """sonrisa dibujada con tiza (k = 0..1 cuánto se ha dibujado)"""
    if k <= 0: return
    F.arc((cx, cy), 46 * s, 20, 20 + 140 * k, col, 7 * s)
    if k > 0.5:
        for dx in (-22, 22): F.circle((cx + dx * s, cy - 26 * s), 7 * s, fill=col)
    if k > 0.8:
        for i in range(-2, 3):
            a = math.radians(90 - i * 22); x, y = cx + math.cos(a) * 46 * s, cy + math.sin(a) * 46 * s
            F.line([(x, y - 12 * s), (x, y)], col, 3 * s, round_=False)

def cara_sonriente(F, J, sc, f, g):
    """pinta sobre la cabeza de Carmen los ojos y la sonrisa del Sonriente (g = 0..1)"""
    if g <= 0: return
    hc = J["head"]; ex = f * 8 * sc
    for dx in (-12, 12):
        F.circle((hc[0] + ex + dx * sc, hc[1] - 8 * sc), 8.5 * sc * g, fill=(8, 8, 12))
        F.circle((hc[0] + ex + dx * sc, hc[1] - 8 * sc), 3.5 * sc * g, fill=(255, 255, 255))
    rw = 26 * sc * (0.5 + 0.5 * g)
    F.ellipse((hc[0] + ex, hc[1] + 12 * sc), rw, 11 * sc * g, fill=(10, 4, 6))
    for i in range(-4, 5):
        x = hc[0] + ex + i * rw / 5
        F.line([(x, hc[1] + 12 * sc - 9 * sc * g), (x, hc[1] + 12 * sc + 9 * sc * g)], (255, 255, 255), 2.5 * sc, round_=False)

def torre(F, smiles=0.0):
    """interior del faro: escalera en zigzag con una sonrisa de tiza en cada tramo"""
    F.rect(200, -2000, 880, 2400, fill=(30, 32, 42))
    for k in range(-1, 8):
        ya = 1600 - k * FL; yb = ya - FL
        xa, xb = (280, 800) if k % 2 == 0 else (800, 280)
        F.poly([(xa, ya), (xb, yb), (xb, yb + 26), (xa, ya + 26)], fill=(70, 72, 86))
        n = 9
        for s in range(n):
            x0 = lerp(xa, xb, s / n); y0 = lerp(ya, yb, s / n); x1 = lerp(xa, xb, (s + 1) / n)
            F.line([(x0, y0), (x0, y0 - FL / n), (x1, y0 - FL / n)], (110, 112, 128), 5, round_=False)
        F.rect(xb - 60 if k % 2 == 0 else xb, yb - 4, xb if k % 2 == 0 else xb + 60, yb + 22, fill=(70, 72, 86))
        if smiles > 0:
            sonrisa_tiza(F, 360 if k % 2 else 720, ya - 150, 0.75, k=smiles)
    for side in (200, 880): F.line([(side, -2000), (side, 2400)], (12, 12, 18), 24, round_=False)
    for k in range(-1, 8):
        F.rect(500, 1600 - k * FL - 150, 580, 1600 - k * FL - 60, fill=(40, 60, 100) if k % 3 else (12, 18, 30))

def path(v):
    k = math.floor(v); f = v - k
    ya = 1600 - k * FL; yb = ya - FL
    xa, xb = (280, 800) if k % 2 == 0 else (800, 280)
    return lerp(xa, xb, f), lerp(ya, yb, f), (1 if k % 2 == 0 else -1)

# ---------- escenas ----------
def faro_lejos(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("ciudad"), dict(x=lerp(540, 600, zp), y=lerp(1000, 960, zp), z=lerp(1.0, 1.15, zp)))
    F.circle((200, 380), 60, fill=(225, 230, 240))
    F.rect(-400, 1300, 1500, 2600, fill=(12, 24, 44))
    for i in range(14):
        xx = (i * 130 + t * 60) % 1500 - 200
        F.line([(xx, 1340 + (i % 4) * 60), (xx + 70, 1340 + (i % 4) * 60)], (60, 90, 130), 4)
    acantilado(F, 100, 1240, col=(14, 18, 30))
    T0 = D * 0.4; on = ease(seg(t, T0, T0 + 0.25))
    faro_draw(F, 820, 1240, h=600, lit=on, beam_ang=180 + 40 * math.sin(t * 1.4) if on > 0 else None)
    LEO.draw(F, STAND if t < T0 else SCARED, 470, 1240, f=1, face="scared")
    NORA.draw(F, STAND if t < T0 + 0.15 else SCARED, 330, 1240, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((820, 560), 520 * on + 1, 0.9 * on), ((400, 1140), 300, 0.45)], amb=0.4)
    return img, dict(grain=8, flash=((255, 250, 220), 0.55 * math.exp(-max(0, t - T0) * 6) * (t > T0)))

def puerta_faro(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("ciudad"), dict(x=lerp(500, 560, zp), y=lerp(1020, 1000, zp), z=lerp(1.05, 1.35, zp)))
    F.rect(-400, 1300, 1500, 2600, fill=(14, 18, 30))
    F.poly([(160, 1300), (920, 1300), (860, -200), (220, -200)], fill=(214, 214, 222), outline=(40, 40, 50), w=6)
    F.poly([(190, 560), (890, 560), (880, 360), (200, 360)], fill=(190, 46, 46))
    F.rect(420, 760, 660, 1300, fill=(70, 50, 34), outline=(40, 28, 18), w=8)
    ab = ease(seg(t, D * 0.55, D))
    F.rect(420, 760, 420 + 120 * ab, 1300, fill=(4, 4, 8))                      # rendija que se abre
    sonrisa_tiza(F, 560, 960, 1.4, k=ease(seg(t, D * 0.05, D * 0.4)))
    w = ease(seg(t, 0, D * 0.6))
    LEO.draw(F, walk(t, 0.5) if w < 1 else STAND, lerp(-60, 300, w), 1300, f=1, face="scared")
    NORA.draw(F, walk(t + 0.3, 0.5) if w < 1 else STAND, lerp(-200, 170, w), 1300, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((540, 980), 320, 0.75), ((200, 1150), 260, 0.45)], amb=0.3)
    return img, dict(grain=9, tint=((255, 0, 30), 0.1 * ab))

def escalones(t, D, fi):
    p = ease(seg(t, 0, D * 0.95))
    u = 0.3 + 3.6 * p
    lx, ly, lf = path(u)
    F = Frame(base("oscuro"), dict(x=540, y=ly - 260, z=1.15, sx=noise(t * 20) * 3))
    torre(F, smiles=1.0)
    nx, ny, nf = path(u - 0.2)
    NORA.draw(F, run(t + 0.2, 0.9), nx, ny, f=nf, face="scared")
    LEO.draw(F, run(t, 0.9), lx, ly, f=lf, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((lx, ly - 120), 420, 0.75), ((540, ly - 700), 300, 0.35)], amb=0.35)
    d = ImageDraw.Draw(img)
    n = min(114, int(114 * p))
    d.rounded_rectangle((640, 260, 1030, 380), 24, fill=(0, 0, 0))
    d.text((835, 320), f"{n}/114", font=font(84), fill=(255, 214, 0) if n == 114 else (255, 255, 255), anchor="mm")
    return img, dict(grain=9)

def voz_arriba(t, D, fi):
    lx, ly, lf = path(3.75)
    zp = ease(seg(t, 0, D * 0.7))
    F = Frame(base("oscuro"), dict(x=lerp(560, 540, zp), y=lerp(ly - 220, ly - 380, zp), z=lerp(1.4, 1.2, zp)))
    torre(F, smiles=1.0)
    look = pose(head=-28, body=-6, a1u=30, a1l=20, a2u=-20, a2l=20)
    nx, ny, nf = path(3.6)
    NORA.draw(F, look, nx, ny, f=nf, face="scared")
    LEO.draw(F, look, lx, ly, f=lf, face="scared")
    top = (540, ly - 900)
    for i in range(4):                                   # ondas de la voz bajando desde arriba
        k = ((t * 0.9 + i * 0.25) % 1)
        F.circle(top, 60 + 520 * k, outline=(255, 220, 160), w=max(1, 10 * (1 - k)))
    img = iluminar(F.finish(), F, [], glows=[(top, 380, 0.9), ((lx, ly - 120), 320, 0.6)], amb=0.25)
    return img, dict(grain=10, tint=((255, 180, 60), 0.06))

def sala_faro(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("oscuro"), dict(x=lerp(500, 560, zp), y=1150, z=lerp(1.0, 1.15, zp)))
    sala_lampara(F, lit=0.12)
    big(CARMEN, 0.92, F, pose(head=6, body=4, a1u=10, a2u=-10), 720, 1450, f=1, face="neutral")
    w = ease(seg(t, 0, D * 0.75))
    NORA.draw(F, walk(t, 0.4) if w < 1 else STAND, lerp(-60, 400, w), 1450, f=1, face="scared")
    LEO.draw(F, walk(t + 0.3, 0.4) if w < 1 else STAND, lerp(-220, 230, w), 1450, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((620, 1100), 420, 0.6), ((300, 1300), 260, 0.4)], amb=0.25, warm=(220, 200, 255))
    return img, dict(grain=10)

def hombro(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("oscuro"), dict(x=lerp(560, 600, zp), y=lerp(1150, 1100, zp), z=lerp(1.4, 1.7, zp)))
    sala_lampara(F, lit=0.12)
    tc = D * 0.72; gira = t > tc
    cj = add(pose(head=6, body=4, a1u=10, a2u=-10), jitter(t, 4 * gira, 6))
    big(CARMEN, 0.92, F, cj, 720, 1450, f=-1 if gira else 1, face="closed" if gira else "neutral")
    r = ease(seg(t, D * 0.1, D * 0.5))
    NORA.draw(F, pose(a1u=lerp(20, 82, r), a1l=lerp(20, 4, r), body=lerp(0, 8, r)), 560, 1450, f=1, face="scared")
    LEO.draw(F, SCARED if gira else STAND, 400, 1450, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((660, 1250), 360, 0.65)], amb=0.22, warm=(220, 200, 255))
    return img, dict(grain=11, glitch=0.25 if gira and fi % 5 == 0 else 0, tint=((255, 0, 30), 0.12 * gira))

def cabeza_carmen(F, hc, sc, f, g):
    """cabeza de Carmen (piel, moño gris) con la sonrisa del Sonriente encima"""
    r = 33 * sc
    F.circle(hc, r + 4.5 * sc, fill=(8, 8, 12)); F.circle(hc, r, fill=CARMEN.limb)
    gris = (196, 196, 204)
    F.d.chord([*F.P(hc[0] - r - 2 * sc, hc[1] - r - 3 * sc), *F.P(hc[0] + r + 2 * sc, hc[1] + r - 6 * sc)], 180, 360, fill=gris)
    F.circle((hc[0] - f * r * 0.62, hc[1] - r * 0.92), r * 0.46, fill=gris, outline=(150, 150, 160), w=2 * sc)
    cara_sonriente(F, dict(head=hc), sc, f, g)

def giro(t, D, fi):
    T0 = D * 0.2
    g = ease(seg(t, T0, T0 + 0.5))                 # aparece la sonrisa
    grow = ease(seg(t, T0 + 0.5, D * 0.8))         # el cuerpo de Carmen se vuelve el del Sonriente y crece
    sh = 4 + 12 * g
    F = Frame(base("oscuro"), dict(x=lerp(700, 640, grow), y=lerp(1200, 1290, grow), z=lerp(2.1, 1.2, grow),
                                   sx=noise(t * 40) * sh, sy=noise(t * 40, 2) * sh))
    sala_lampara(F, lit=0.12)
    if grow < 0.08:
        sc = 0.92
        J = big(CARMEN, sc, F, add(pose(head=-4, a1u=30 * g, a1l=30, a2u=-10), jitter(t, 3 * g, 5)), 720, 1450, f=-1, face="neutral")
    else:
        sc = lerp(0.92, 2.1, grow)
        J = enemy(F, add(pose(a1u=lerp(30, 125, grow), a1l=-30, a2u=lerp(-10, -120, grow), a2l=30, head=-4), jitter(t, 5, 3)), 740, 1450, sc, f=-1)
    cabeza_carmen(F, J["head"], sc, -1, g)
    NORA.draw(F, SCARED, lerp(560, 330, grow), 1450, f=1, face="scared")
    LEO.draw(F, SCARED, lerp(410, 180, grow), 1450, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((700, 1150), 520, 0.7), (J["head"], 300 * grow + 1, 0.6 * grow)], amb=0.25, warm=(220, 160, 255))
    return img, dict(grain=12, tint=((255, 0, 30), 0.22 * g), glitch=0.35 if g > 0.5 and fi % 4 == 0 else 0,
                     flash=((255, 30, 40), 0.35 * math.exp(-abs(t - T0 - 0.3) * 8)))

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    return F.finish(), {}

ESCENA_FN = dict(faro_lejos=faro_lejos, puerta_faro=puerta_faro, escalones=escalones, voz_arriba=voz_arriba, sala_faro=sala_faro, hombro=hombro, giro=giro, final=final)
PAUSA = dict(faro_lejos=0.3, puerta_faro=0.2, escalones=0.2, voz_arriba=0.3, sala_faro=0.2, hombro=0.4, giro=0.8, final=1.2)
