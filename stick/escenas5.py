"""Escenas del episodio 5 (Santa Brígida): hospital abandonado, linternas, habitación 114 y la anciana."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from motor import *
from escenas import base, GOLD
from escenas2 import enemy, big
from escenas3 import cara_sonriente, LILA, YEL

ROJO = (230, 30, 50)
CERA_NEGRA, CERA_ROJA, CERA_LILA = (20, 18, 22), (220, 40, 40), (150, 80, 240)

# ---------- luz de linterna: la escena se oscurece salvo dentro de los haces ----------
def iluminar(img, F, haces=(), glows=(), amb=0.2, warm=(255, 236, 190)):
    """haces: [(mano_mundo, ángulo_rad, largo, apertura)]; glows: [(centro_mundo, radio, intensidad)]"""
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    for (hx, hy), ang, Lb, sp in haces:
        px, py = F.P(hx, hy); px, py = px / S, py / S; Ls = Lb * F.z
        pts = [(px, py)] + [(px + math.cos(ang + k * sp / 4) * Ls, py + math.sin(ang + k * sp / 4) * Ls) for k in range(-4, 5)]
        d.polygon(pts, fill=230)
        d.ellipse((px - 26, py - 26, px + 26, py + 26), fill=255)
    for (cx, cy), r, it in glows:
        px, py = F.P(cx, cy); px, py = px / S, py / S; rr = r * F.z
        d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=int(255 * it))
    m = m.filter(ImageFilter.GaussianBlur(22))
    amb = min(0.9, amb * 1.6 + 0.05)
    a = np.asarray(img, np.float32); k = np.asarray(m, np.float32)[..., None] / 255
    out = a * (amb + (1 - amb) * k) + np.array(warm, np.float32) * k * 0.07
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def linterna_mano(F, J, ang_deg, f=1):
    """dibuja la linterna en la mano delantera y devuelve el haz (mano, ángulo)"""
    hx, hy = J["a1h"]; a = math.radians(ang_deg)
    ex, ey = hx + math.cos(a) * 30, hy + math.sin(a) * 30
    F.line([(hx - math.cos(a) * 8, hy - math.sin(a) * 8), (ex, ey)], (60, 60, 70), 15)
    F.circle((ex, ey), 9, fill=(255, 250, 220))
    return (ex, ey), a

LIN = pose(a1u=82, a1l=4)          # brazo estirado sujetando la linterna

# ---------- piezas del hospital ----------
VERDE_A, VERDE_B = (44, 58, 50), (20, 26, 24)
def pasillo_h(F, x0=-600, x1=2600, nums=(108, 109, 110, 111, 112, 113), puertas_x=None, piso=1300):
    """pasillo de hospital de lado: pared, zócalo, puertas numeradas, lámparas colgantes y suelo de baldosas"""
    F.rect(x0, piso - 330, x1, piso, fill=(30, 40, 34)); F.line([(x0, piso - 330), (x1, piso - 330)], (64, 80, 70), 6)
    r = random.Random(4)
    for i in range(int((x1 - x0) / 260)):
        x = x0 + i * 260 + r.uniform(0, 120); y = r.uniform(420, 900)
        F.ellipse((x, y), r.uniform(40, 110), r.uniform(20, 60), fill=(36, 46, 40))
    px = puertas_x if puertas_x is not None else [x0 + 200 + k * 520 for k in range(len(nums))]
    for x, n in zip(px, nums):
        F.rect(x - 10, piso - 560, x + 200, piso, fill=(58, 66, 60))
        F.rect(x, piso - 550, x + 190, piso, fill=(74, 80, 72), outline=(40, 46, 40), w=5)
        F.rect(x + 50, piso - 490, x + 140, piso - 390, fill=(14, 18, 18))
        F.circle((x + 165, piso - 270), 9, fill=GOLD)
        F.rect(x + 45, piso - 625, x + 145, piso - 575, fill=(196, 192, 170), outline=(60, 56, 50), w=3)
        F.text((x + 95, piso - 600), str(n), 34, (40, 30, 26))
    for k in range(int((x1 - x0) / 700) + 1):
        lx = x0 + 400 + k * 700
        F.line([(lx, 200), (lx, 330)], (30, 30, 30), 4)
        F.poly([(lx - 50, 360), (lx + 50, 360), (lx + 24, 330), (lx - 24, 330)], fill=(60, 64, 60))
    F.rect(x0, piso, x1, piso + 1400, fill=(22, 24, 22)); F.line([(x0, piso), (x1, piso)], (70, 76, 70), 6)
    for k in range(int((x1 - x0) / 120)):
        F.line([(x0 + k * 120, piso + 4), (x0 + k * 120 - 90, piso + 400)], (30, 32, 30), 3)

def silla_ruedas(F, x, y, rot=0.0, f=1, col=(150, 154, 160)):
    """silla de ruedas con base en y; rot = giro de la rueda en radianes; f = hacia dónde mira"""
    R = 70; cx, cy = x - f * 20, y - R
    F.circle((cx, cy), R, outline=col, w=9)
    for k in range(4):
        a = rot + k * math.pi / 4
        F.line([(cx - math.cos(a) * R, cy - math.sin(a) * R), (cx + math.cos(a) * R, cy + math.sin(a) * R)], (110, 112, 118), 3)
    F.circle((cx, cy), 10, fill=col)
    F.line([(x - f * 70, y - 110), (x + f * 60, y - 110)], (90, 40, 40), 16)          # asiento
    F.line([(x - f * 70, y - 110), (x - f * 80, y - 230)], col, 9)                      # respaldo
    F.line([(x - f * 80, y - 230), (x - f * 110, y - 235)], col, 8)                     # asa
    F.line([(x - f * 72, y - 200), (x - f * 76, y - 125)], (90, 40, 40), 18)
    F.line([(x + f * 60, y - 110), (x + f * 70, y - 30)], col, 7)
    F.circle((x + f * 72, y - 16), 16, outline=col, w=5)

def camilla(F, x, y, f=1, sabana=(150, 160, 150)):
    F.rect(x - 150, y - 150, x + 150, y - 128, fill=(120, 124, 126))
    F.poly([(x - 150, y - 150), (x + 150, y - 150), (x + 140, y - 182), (x - 120, y - 190)], fill=sabana)
    F.ellipse((x + f * 110, y - 180), 40, 18, fill=(170, 176, 168))
    for lx in (x - 130, x + 130):
        F.line([(lx, y - 130), (lx, y - 20)], (110, 112, 114), 7); F.circle((lx, y - 12), 12, fill=(40, 40, 44))
    F.line([(x - 130, y - 70), (x + 130, y - 70)], (100, 102, 104), 5)

def cama_hosp(F, x, y, w=420):
    """cama de hospital con hueco debajo (patas altas)"""
    F.rect(x - w / 2, y - 220, x + w / 2, y - 180, fill=(140, 140, 146), outline=(80, 80, 86), w=4)
    F.rect(x - w / 2 + 6, y - 260, x + w / 2 - 6, y - 220, fill=(170, 168, 150))
    for lx in (x - w / 2 + 10, x + w / 2 - 10): F.line([(lx, y - 190), (lx, y)], (110, 110, 116), 9)
    F.line([(x + w / 2 - 10, y - 180), (x + w / 2 - 10, y - 380)], (120, 120, 126), 9)
    for k in range(4): F.line([(x + w / 2 - 10 - k * 0, y - 380 + k * 50), (x + w / 2 - 70, y - 380 + k * 50)], (120, 120, 126), 6)
    F.line([(x + w / 2 - 70, y - 380), (x + w / 2 - 70, y - 220)], (120, 120, 126), 7)

# ---------- dibujos infantiles con ceras ----------
def _cera(F, pts, col, w, seed):
    r = random.Random(seed)
    for k in range(2):
        F.line([(x + r.uniform(-3, 3), y + r.uniform(-3, 3)) for x, y in pts], col, w * (1 - 0.3 * k))

def stick_cera(F, cx, base_y, h, col, seed=0, malo=False, cap=False, coleta=False):
    r = h * 0.14; hy = base_y - h + r; ny = hy + r; hip = base_y - h * 0.42
    _cera(F, [(cx, ny), (cx, hip)], col, h * 0.03, seed)
    _cera(F, [(cx - h * 0.2, base_y), (cx, hip), (cx + h * 0.2, base_y)], col, h * 0.03, seed + 1)
    up = 0.15 if malo else 0.05
    _cera(F, [(cx - h * 0.3, ny + h * (0.05 - up)), (cx, ny + h * 0.1), (cx + h * 0.3, ny + h * (0.05 - up))], col, h * 0.03, seed + 2)
    if malo:
        F.circle((cx, hy), r, fill=col)
        for dx in (-0.4, 0.4): F.circle((cx + dx * r, hy - 0.25 * r), 0.2 * r, fill=(255, 255, 255))
        F.arc((cx, hy - 0.1 * r), 0.7 * r, 15, 165, (255, 255, 255), max(2, 0.16 * r))
    else:
        F.circle((cx, hy), r, outline=col, w=max(2, h * 0.025))
        F.arc((cx, hy), 0.55 * r, 30, 150, col, max(2, h * 0.02))
    if cap: F.d.chord([*F.P(cx - r, hy - r), *F.P(cx + r, hy + r)], 180, 360, fill=col)
    if coleta: _cera(F, [(cx - r * 0.7, hy - r * 0.6), (cx - r * 1.5, hy), (cx - r * 1.3, hy + r * 0.9)], col, h * 0.03, seed + 3)

def papel(F, cx, cy, w, h, ang=0.0, col=(226, 220, 196)):
    a = math.radians(ang); c, s_ = math.cos(a), math.sin(a)
    pts = [(cx + dx * c - dy * s_, cy + dx * s_ + dy * c) for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
    F.poly(pts, fill=col, outline=(150, 140, 120), w=2)
    F.circle((cx, cy - h / 2 + 10), 5, fill=(140, 30, 30))

def dibujo(F, cx, cy, w, h, seed):
    r = random.Random(seed)
    papel(F, cx, cy, w, h, r.uniform(-6, 6), col=(226 - r.randint(0, 30), 220 - r.randint(0, 30), 196 - r.randint(0, 40)))
    stick_cera(F, cx + r.uniform(-0.1, 0.1) * w, cy + h * 0.38, h * 0.75, CERA_NEGRA, seed, malo=True)
    if r.random() < 0.5: F.circle((cx + w * 0.33, cy - h * 0.33), w * 0.08, fill=(240, 200, 40))
    if r.random() < 0.6: stick_cera(F, cx - w * 0.3, cy + h * 0.38, h * 0.32, (60, 90, 200), seed + 9)

def pared_dibujos(F, x0, y0, cols, rows, dx=170, dy=200, seed=0):
    for i in range(rows):
        for j in range(cols):
            dibujo(F, x0 + j * dx + (i % 2) * 30, y0 + i * dy, 120, 150, seed + i * 31 + j)

def cuarto114(F, piso=1300):
    F.rect(-600, piso, 1700, piso + 1400, fill=(20, 22, 20)); F.line([(-600, piso), (1700, piso)], (60, 66, 60), 6)
    F.rect(-600, piso - 260, 1700, piso, fill=(30, 38, 32))

def ojos_oscuridad(F, c, r, a=1.0):
    col = tuple(int(255 * a) for _ in range(3))
    for dx in (-0.4, 0.4): F.circle((c[0] + dx * r, c[1] - 0.25 * r), 0.17 * r, fill=col)
    F.arc((c[0], c[1] - 0.1 * r), 0.66 * r, 20, 160, col, max(2, 0.12 * r))
    for i in range(-3, 4):
        an = math.radians(90 - i * 17); x, y = c[0] + math.cos(an) * 0.66 * r, c[1] - 0.1 * r + math.sin(an) * 0.66 * r
        F.line([(x, y - 0.12 * r), (x, y + 0.02 * r)], col, max(1, 0.04 * r), round_=False)

def lluvia(F, t, n=40):
    rr = random.Random(int(t * 30))
    for _ in range(n):
        x = rr.uniform(-100, 1180); y = rr.uniform(0, 1900); F.line([(x, y), (x - 8, y + 40)], (90, 100, 140), 2)

# ---------- escenas ----------
def verja(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("ciudad"), dict(x=540, y=lerp(1010, 980, zp), z=lerp(1.0, 1.1, zp)))
    F.circle((860, 380), 70, fill=(220, 224, 236)); F.circle((890, 360), 64, fill=(8, 11, 30))
    F.rect(-400, 1300, 1500, 2600, fill=(8, 10, 16))
    F.rect(140, 620, 940, 1300, fill=(36, 40, 54), outline=(20, 22, 30), w=6)
    F.poly([(100, 630), (980, 630), (540, 450)], fill=(26, 28, 40))
    F.rect(525, 310, 555, 430, fill=(150, 40, 46)); F.rect(490, 345, 590, 375, fill=(150, 40, 46))
    for r_ in range(3):
        for c_ in range(6):
            x = 190 + c_ * 125; y = 740 + r_ * 120
            lit = (r_, c_) == (0, 4) and noise(t * 7, 1) > -0.2
            F.rect(x, y, x + 70, y + 90, fill=(240, 200, 90) if lit else (14, 16, 24))
    F.rect(470, 1130, 610, 1300, fill=(4, 4, 8))
    F.rect(330, 650, 750, 710, fill=(200, 196, 180), outline=(60, 56, 50), w=4)
    F.text((540, 681), tr("SANTA BRÍGIDA"), 40, (60, 30, 30))
    w = ease(seg(t, 0, D * 0.85))
    NORA.draw(F, walk(t, 0.8) if w < 1 else STAND, lerp(-40, 420, w), 1300, f=1, face="scared")
    J = LEO.draw(F, add(walk(t + 0.2, 0.8), LIN) if w < 1 else LIN, lerp(80, 540, w), 1300, f=1, face="neutral")
    h_ = linterna_mano(F, J, 8)
    for k in range(-6, 28):
        x = k * 50
        if 250 < x < 360 and w > 0.35: continue          # hueco por el que se cuelan
        F.line([(x, 1170), (x, 1320)], (24, 26, 34), 7)
    F.line([(-400, 1190), (1500, 1190)], (24, 26, 34), 6)
    lluvia(F, t)
    img = iluminar(F.finish(), F, [(h_[0], h_[1], 700, 0.3)], amb=0.6)
    fl = math.exp(-abs(t - D * 0.25) * 12) + 0.6 * math.exp(-abs(t - D * 0.33) * 14)
    return img, dict(flash=((220, 230, 255), 0.6 * fl), grain=9)

def linternas(t, D, fi):
    zp = ease(t / D)
    cx = lerp(300, 900, zp)
    F = Frame(gradient(VERDE_A, VERDE_B), dict(x=cx, y=1050, z=1.3))
    pasillo_h(F)
    xl = cx + 40; xn = cx - 140
    Jn = NORA.draw(F, add(walk(t, 0.6), LIN), xn, 1300, f=1, face="scared")
    Jl = LEO.draw(F, add(walk(t + 0.3, 0.6), LIN), xl, 1300, f=1, face="neutral")
    a1 = 6 + 8 * math.sin(t * 1.7); a2 = 14 + 10 * math.sin(t * 1.3 + 1)
    hn = linterna_mano(F, Jn, a2); hl = linterna_mano(F, Jl, a1)
    r = random.Random(fi // 2)
    for _ in range(25):
        F.circle((cx + r.uniform(0, 500), r.uniform(900, 1250)), 2.5, fill=(200, 196, 170))
    img = iluminar(F.finish(), F, [(hl[0], hl[1], 900, 0.3), (hn[0], hn[1], 900, 0.3)],
                   glows=[((xl, 1150), 200, 0.35), ((xn, 1150), 200, 0.35)], amb=0.16)
    return img, dict(grain=10)

def camillas(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient(VERDE_A, VERDE_B), dict(x=lerp(560, 600, zp), y=1080, z=lerp(1.08, 1.14, zp)))
    pasillo_h(F, nums=(110, 111, 112), puertas_x=[-500, 860, 1500])
    camilla(F, 510, 1300, f=1); camilla(F, 760, 1300, f=1, sabana=(140, 120, 110))
    silla_ruedas(F, 1000, 1300, 0.3, f=1)
    J = LEO.draw(F, LIN, 290, 1300, f=1, face="scared")
    NORA.draw(F, SCARED, 185, 1300, f=1, face="scared")
    ang = lerp(18, -6, ease(seg(t, 0.1, D * 0.8)))
    h_ = linterna_mano(F, J, ang)
    img = F.finish()
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, D * 0.6, D * 0.8))
    if p > 0:   # flechas: todo apunta a la misma puerta
        x0, y0 = F.P(860 + 95, 1300 - 640); x0, y0 = x0 / S, y0 / S
        d.ellipse((x0 - 18 * p, y0 - 18 * p, x0 + 18 * p, y0 + 18 * p), fill=ROJO)
    img = iluminar(img, F, [(h_[0], h_[1], 1400, 0.34)], glows=[((235, 1150), 180, 0.3)], amb=0.14)
    return img, dict(grain=10, tint=((255, 0, 30), 0.08 * p))

def silla(t, D, fi):
    rollp = ease(seg(t, D * 0.1, D * 0.85))
    F = Frame(gradient(VERDE_A, VERDE_B), dict(x=520, y=1060, z=1.25, sx=noise(t * 30) * 4 * rollp, sy=noise(t * 30, 2) * 4 * rollp))
    pasillo_h(F, nums=(112, 113), puertas_x=[-120, 1100])
    x = lerp(1150, 600, rollp)
    silla_ruedas(F, x, 1300, -x / 70, f=-1)
    J = LEO.draw(F, mix(LIN, add(LIN, dict(body=-12, head=8)), rollp), 330, 1300, f=1, face="scared")
    NORA.draw(F, SCARED, 210, 1300, f=1, face="scared")
    h_ = linterna_mano(F, J, 10 + 4 * noise(t * 8, 3))
    img = iluminar(F.finish(), F, [(h_[0], h_[1], 1100, 0.32)], glows=[((270, 1150), 200, 0.3)], amb=0.14)
    return img, dict(grain=10, glitch=0.25 if rollp > 0.6 and fi % 5 == 0 else 0, tint=((255, 0, 30), 0.1 * rollp))

def huida(t, D, fi):
    cx = 500 + t * 650
    F = Frame(gradient(VERDE_A, VERDE_B), dict(x=cx, y=1060, z=1.3, sx=noise(t * 25) * 8, sy=noise(t * 25, 1) * 8))
    pasillo_h(F, x0=-800, x1=5000, nums=(101, 102, 103, 104, 105, 106, 107, 108, 109, 110))
    xl = cx + 190; xn = cx + 30
    Jn = NORA.draw(F, run(t + 0.17, 1.15), xn, 1300, f=1, face="scared")
    Jl = LEO.draw(F, run(t, 1.15), xl, 1300, f=1, face="scared")
    a = ease(seg(t, D * 0.25, D * 0.55))
    if a > 0: ojos_oscuridad(F, (cx - 290 + 40 * noise(t * 2, 4), 1020), 70, a)
    hl = (Jl["a1h"][0] + 20, Jl["a1h"][1])
    img = iluminar(F.finish(), F, [(hl, math.radians(20 * math.sin(t * 10)), 800, 0.3)],
                   glows=[((xl, 1150), 200, 0.3), ((xn, 1150), 200, 0.3), ((cx - 300, 1020), 120, 0.4 * a)], amb=0.12)
    return img, dict(grain=10, glitch=0.3 if a > 0.5 and fi % 4 == 0 else 0, tint=((255, 0, 30), 0.12 * a))

def cartel(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient(VERDE_A, VERDE_B), dict(x=lerp(300, 860, zp), y=lerp(1060, 940, zp), z=lerp(1.2, 1.7, zp)))
    pasillo_h(F, nums=(112, 113, 114), puertas_x=[-200, 300, 800])
    F.rect(30, 560, 250, 640, fill=(200, 196, 170), outline=(60, 56, 50), w=4)
    F.text((140, 600), tr("3ª PLANTA"), 30, (40, 30, 26))
    F.rect(800, 1290, 990, 1300, fill=(255, 60, 60))                       # luz roja bajo la puerta
    w = ease(seg(t, 0, D * 0.8))
    Jl = LEO.draw(F, add(walk(t, 0.6), LIN) if w < 1 else LIN, lerp(220, 600, w), 1300, f=1, face="scared")
    NORA.draw(F, walk(t + 0.3, 0.6) if w < 1 else STAND, lerp(110, 480, w), 1300, f=1, face="scared")
    h_ = linterna_mano(F, Jl, 4)
    img = iluminar(F.finish(), F, [(h_[0], h_[1], 900, 0.3)],
                   glows=[((895, 1300), 160, 0.55 + 0.2 * noise(t * 6)), ((lerp(165, 540, w), 1150), 200, 0.3)], amb=0.14)
    return img, dict(grain=10, tint=((255, 0, 30), 0.06))

def abierta(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient((40, 52, 44), (16, 20, 18)), dict(x=540, y=lerp(1000, 980, zp), z=lerp(1.1, 1.35, zp)))
    F.rect(-400, 1350, 1500, 2600, fill=(20, 22, 20)); F.line([(-400, 1350), (1500, 1350)], (56, 64, 56), 6)
    F.rect(380, 680, 700, 1350, fill=(60, 66, 58))
    F.rect(400, 700, 680, 1350, fill=(40, 6, 8))
    op = ease(seg(t, D * 0.15, D * 0.6))
    if op > 0.2:
        r = random.Random(3)
        for k in range(8): dibujo(F, 430 + r.uniform(0, 220), 780 + r.uniform(0, 320), 60, 76, k)
    w = lerp(280, 40, op)
    F.poly([(400, 700), (400 + w, 700 - 40 * op), (400 + w, 1350 + 40 * op), (400, 1350)], fill=(150, 150, 136), outline=(80, 80, 70), w=5)
    F.rect(470, 600, 610, 660, fill=(200, 196, 170), outline=(60, 56, 50), w=4)
    F.text((540, 631), "114", 46, (30, 26, 24))
    NORA.draw(F, SCARED, 180, 1350, f=1, face="scared")
    J = LEO.draw(F, LIN, 290, 1350, f=1, face="scared")
    h_ = linterna_mano(F, J, -8)
    img = iluminar(F.finish(), F, [(h_[0], h_[1], 700, 0.32)], glows=[((540, 1020), 300, 0.5 * op), ((230, 1200), 200, 0.3)], amb=0.18,
                   warm=(255, 120, 110))
    return img, dict(grain=12, tint=((255, 0, 30), 0.12 * op))

def dibujos(t, D, fi):
    F = Frame(gradient((40, 46, 40), (18, 20, 18)), dict(x=540, y=980, z=1.15))
    cuarto114(F)
    pared_dibujos(F, 60, 380, 6, 4)
    Jn = NORA.draw(F, LIN, 300, 1300, f=1, face="scared")
    Jl = LEO.draw(F, LIN, 760, 1300, f=-1, face="scared")
    a1 = -60 - 30 * math.sin(t * 1.4); a2 = -120 + 30 * math.sin(t * 1.1 + 0.5)
    hn = linterna_mano(F, Jn, a1); hl = linterna_mano(F, Jl, a2)
    img = iluminar(F.finish(), F, [(hn[0], hn[1], 900, 0.28), (hl[0], hl[1], 900, 0.28)],
                   glows=[((300, 1150), 170, 0.3), ((760, 1150), 170, 0.3)], amb=0.12)
    return img, dict(grain=11)

def fecha(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient((30, 34, 30), (12, 14, 12)), dict(x=540, y=900, z=lerp(1.0, 1.12, zp)))
    for k in range(10):
        r = random.Random(k); dibujo(F, r.uniform(-60, 1140), r.uniform(200, 1500), 170, 210, 50 + k)
    papel(F, 540, 880, 760, 900, -2)
    stick_cera(F, 540, 1220, 640, CERA_NEGRA, 7, malo=True)
    F.circle((830, 520), 60, fill=(240, 200, 40))
    p = ease_back(seg(t, D * 0.4, D * 0.6))
    if p > 0: F.text((780, 1110), "1986", 110 * p, CERA_ROJA)
    bx = lerp(380, 600, ease(seg(t, 0, D * 0.5)))
    img = iluminar(F.finish(), F, [], glows=[((bx, 860), 440, 1.0)], amb=0.1)
    return img, dict(grain=10, flash=((255, 30, 40), 0.25 * (1 - seg(t, D * 0.45, D * 0.7)) * (t > D * 0.45)))

def ultimo(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient((30, 34, 30), (12, 14, 12)), dict(x=540, y=lerp(900, 870, zp), z=lerp(1.0, 1.08, zp)))
    papel(F, 540, 760, 820, 920, 1.5, col=(240, 236, 222))
    ap = ease(seg(t, D * 0.35, D * 0.7))
    if ap > 0: stick_cera(F, 540 + 40 * noise(t * 3), 960, lerp(300, 600, ap), CERA_NEGRA, 3, malo=True)
    stick_cera(F, 370, 1070, 320, CERA_ROJA, 11, cap=True)
    stick_cera(F, 720, 1070, 290, CERA_LILA, 12, coleta=True)
    F.text((370, 1140), "LEO", 56, CERA_ROJA); F.text((720, 1140), "NORA", 56, CERA_LILA)
    img = iluminar(F.finish(), F, [], glows=[((540, 760), 500, 1.0)], amb=0.1)
    return img, dict(grain=10, tint=((255, 0, 30), 0.15 * ap), glitch=0.3 if ap > 0.8 and fi % 4 == 0 else 0)

def pasos(t, D, fi):
    F = Frame(gradient((40, 46, 40), (18, 20, 18)), dict(x=540, y=1000, z=1.2, sx=noise(t * 10) * 3))
    cuarto114(F)
    pared_dibujos(F, 520, 420, 4, 3, seed=7)
    F.rect(40, 650, 330, 1300, fill=(4, 4, 6))       # puerta abierta al pasillo
    F.rect(20, 630, 40, 1300, fill=(80, 84, 76)); F.rect(330, 630, 350, 1300, fill=(80, 84, 76))
    near = ease(seg(t, 0, D))
    Jn = NORA.draw(F, SCARED, 820, 1300, f=-1, face="scared")
    Jl = LEO.draw(F, LIN, 640, 1300, f=-1, face="scared")
    hl = linterna_mano(F, Jl, 180 - 4 + 3 * noise(t * 12))
    img = iluminar(F.finish(), F, [(hl[0], hl[1], 700, 0.3)],
                   glows=[((40, 1000), lerp(80, 260, near), lerp(0.1, 0.7, near)), ((730, 1150), 200, 0.3)], amb=0.12, warm=(255, 240, 200))
    return img, dict(grain=11)

def escondite(t, D, fi):
    F = Frame(gradient((40, 46, 40), (18, 20, 18)), dict(x=560, y=1060, z=1.3))
    cuarto114(F)
    pared_dibujos(F, 120, 520, 5, 2, seed=13)
    F.rect(-200, 650, 60, 1300, fill=(4, 4, 6))
    cama_hosp(F, 640, 1300, w=520)
    dive = ease(seg(t, 0, D * 0.5)); off = t > D * 0.62
    for fig, x0, x1, ph in ((NORA, 200, 560, 0.17), (LEO, 330, 720, 0.0)):
        if dive < 1:
            fig.draw(F, run(t + ph, 1.1), lerp(x0, x1 - 120, dive), 1300, f=1, face="scared")
        else:
            fig.draw(F, pose(l1u=0, l2u=0, l1l=0, l2l=0, a1u=170, a2u=160, head=-20), x1, 1270, f=1, rot=-90, snap=False, face="scared")
    haces = [] if off else [((lerp(330, 720, dive) + 40, 1170), math.radians(20 + 30 * dive), 700, 0.3)]
    img = iluminar(F.finish(), F, haces, glows=[((640, 1200), 300, 0.18)], amb=0.08 if off else 0.14)
    return img, dict(grain=12, dark=0.15 if off else 0)

def sombra(t, D, fi):
    F = Frame(gradient((24, 28, 24), (10, 12, 10)), dict(x=540, y=1000, z=1.0))
    F.rect(-400, 1180, 1500, 2600, fill=(16, 18, 16)); F.line([(-400, 1180), (1500, 1180)], (50, 56, 50), 5)
    F.rect(380, 620, 700, 1180, fill=(70, 78, 92)); F.rect(360, 600, 720, 620, fill=(60, 66, 58))
    st = ease(seg(t, 0, D * 0.35))
    sil = Fig(shirt=(8, 8, 10), limb=(8, 8, 10), scale=1.0, extra=("bun", "cane"))
    J = sil.draw(F, add(pose(body=10, head=12, a1u=60, a1l=20), jitter(t, 2, 4)), lerp(330, 540, st), 1180, f=1, face="neutral")
    ang = math.radians(lerp(40, 130, 0.5 + 0.5 * math.sin(t * 1.6)) if t < D * 0.8 else lerp(70, 92, seg(t, D * 0.8, D)))
    h_ = J["a1h"]
    # bajo la cama: somier arriba, patas a los lados
    F.rect(-400, 0, 1500, 440, fill=(10, 10, 12)); F.line([(-400, 440), (1500, 440)], (70, 70, 76), 14)
    for x in (40, 1040): F.line([(x, 440), (x, 1920)], (70, 70, 76), 20)
    LEO.draw(F, pose(l1u=0, l2u=0, a1u=150, a2u=170, head=-10), 760, 1290, f=-1, rot=90, snap=False, face="scared")
    NORA.draw(F, pose(l1u=0, l2u=0, a1u=150, a2u=170, head=-10), 320, 1320, f=1, rot=-90, snap=False, face="scared")
    img = iluminar(F.finish(), F, [(h_, ang, 1100, 0.26)], glows=[(h_, 60, 0.6), ((540, 900), 260, 0.35)], amb=0.12, warm=(255, 250, 220))
    return img, dict(grain=12)

def anciana(t, D, fi):
    rev = ease_out(seg(t, D * 0.05, D * 0.3))
    F = Frame(gradient((40, 46, 40), (14, 16, 14)), dict(x=lerp(560, 520, rev), y=lerp(1000, 1110, rev), z=lerp(1.0, 1.5, rev)))
    cuarto114(F, piso=1320)
    pared_dibujos(F, 60, 420, 6, 3, seed=21)
    bend = ease(seg(t, D * 0.2, D * 0.5))
    J = big(CARMEN, 1.25, F, add(mix(pose(body=10, head=10), pose(body=28, head=-16, a1u=95, a1l=-10), bend), jitter(t, 1.5, 6)),
            620, 1320, f=-1, face="neutral" if t < D * 0.55 else "talk", t=t)
    hx, hy = J["a1h"]
    F.line([(hx, hy), (hx - 40, hy + 12)], (60, 60, 70), 18); F.circle((hx - 44, hy + 13), 12, fill=(255, 250, 220))
    F.rect(-400, 1240, 1500, 1260, fill=(70, 70, 76))       # borde de la cama en primer plano
    LEO.draw(F, pose(l1u=0, l2u=0, a1u=160, a2u=150), 330, 1300, f=1, rot=-90, snap=False, face="scared")
    img = iluminar(F.finish(), F, [((hx - 44, hy + 13), math.radians(165), 600, 0.4)],
                   glows=[(J["head"], 160, 0.85), ((hx - 44, hy + 13), 90, 1.0)], amb=0.22, warm=(255, 250, 220))
    return img, dict(flash=((255, 255, 240), 0.9 * (1 - seg(t, 0, D * 0.2))), grain=9)

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    big(CARMEN, 2.0, F, STAND, 540, 1500, f=-1, face="neutral")
    img = F.finish(); d = ImageDraw.Draw(img)
    d.text((540, 460), tr("PARTE 6"), font=font(190), fill=YEL, anchor="mm", stroke_width=14, stroke_fill=(0, 0, 0))
    return img, {}

ESCENA_FN = dict(verja=verja, linternas=linternas, camillas=camillas, silla=silla, huida=huida, cartel=cartel, abierta=abierta,
                 dibujos=dibujos, fecha=fecha, ultimo=ultimo, pasos=pasos, escondite=escondite, sombra=sombra, anciana=anciana, final=final)
PAUSA = dict(verja=0.8, linternas=0.6, camillas=0.7, silla=0.8, huida=0.6, cartel=0.7, abierta=0.9, dibujos=0.7, fecha=0.8,
             ultimo=1.1, pasos=0.9, escondite=0.7, sombra=0.9, anciana=1.4, final=2.2)
