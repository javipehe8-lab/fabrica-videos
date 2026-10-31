"""Escenas del episodio 7 (El nombre): el archivo del sótano de Santa Brígida, la ficha de 1986 con el nombre tachado,
la primera letra (T), la foto del niño en el columpio y los dibujos de la 114 con la cara tachada."""
import math, random
import numpy as np
from PIL import Image, ImageDraw
from motor import *
from escenas import base, GOLD
from escenas2 import enemy, big
from escenas3 import cara_sonriente, LILA, YEL
from escenas5 import (iluminar, linterna_mano, LIN, cuarto114, dibujo, papel, stick_cera, ojos_oscuridad,
                      CERA_NEGRA, CERA_ROJA, CERA_LILA, ROJO)
from escenas6 import sepia, letras

ARCH_A, ARCH_B = (40, 38, 34), (12, 11, 10)
NINO = Fig(shirt=(80, 120, 190), limb=(240, 232, 220), scale=0.8)
PAPEL = (236, 230, 210)

# ---------- piezas del archivo ----------
def estanteria(F, x, piso=1300, w=260, h=760, seed=0):
    """estantería metálica llena de cajas y carpetas"""
    r = random.Random(seed)
    col = (70, 74, 80)
    for lx in (x - w / 2, x + w / 2): F.line([(lx, piso), (lx, piso - h)], col, 10)
    nb = 5
    for b in range(nb):
        y = piso - 40 - b * (h - 60) / (nb - 1)
        F.line([(x - w / 2, y), (x + w / 2, y)], (90, 94, 100), 8)
        if b == nb - 1: break
        xx = x - w / 2 + 10
        while xx < x + w / 2 - 30:
            bw = r.uniform(30, 70); bh = r.uniform(80, 140)
            c = r.choice([(150, 120, 80), (130, 104, 70), (170, 150, 110), (110, 96, 76), (190, 180, 150)])
            F.rect(xx, y - bh, xx + bw, y - 4, fill=c, outline=(50, 40, 30), w=2)
            if r.random() < 0.5: F.rect(xx + bw * 0.25, y - bh * 0.7, xx + bw * 0.75, y - bh * 0.55, fill=(230, 226, 210))
            xx += bw + r.uniform(2, 8)

def archivo(F, x0=-500, x1=1700, piso=1300, seed=0, sep=330):
    F.rect(x0 - 400, piso, x1 + 400, piso + 1400, fill=(18, 17, 15)); F.line([(x0 - 400, piso), (x1 + 400, piso)], (56, 52, 46), 6)
    for k in range(int((x1 - x0) / sep) + 1):
        estanteria(F, x0 + k * sep, piso, 260, 760, seed + k)
    for k in range(int((x1 - x0) / 700) + 1):                       # bombillas colgantes apagadas
        lx = x0 + 300 + k * 700
        F.line([(lx, 300), (lx, 420)], (30, 30, 30), 4); F.circle((lx, 436), 18, fill=(70, 66, 56))

def polvo(F, t, fi, cx, cy, w=500, h=400, n=30):
    r = random.Random(fi // 2)
    for _ in range(n):
        F.circle((cx + r.uniform(-w / 2, w / 2), cy + r.uniform(-h / 2, h / 2) + 20 * math.sin(t + r.random() * 6)), r.uniform(2, 4), fill=(200, 196, 170))

def garabato(F, x0, y0, x1, y1, p=1.0, seed=0, w=9, col=CERA_NEGRA):
    """tachón de cera negra en zigzag sobre un rectángulo; p = cuánto se ha dibujado (0-1)"""
    r = random.Random(seed); n = 14
    pts = []
    for k in range(n + 1):
        x = lerp(x0, x1, k / n) + r.uniform(-6, 6)
        y = (y0 if k % 2 == 0 else y1) + r.uniform(-8, 8)
        pts.append((x, y))
    m = max(2, int(len(pts) * p))
    if p > 0: F.line(pts[:m], col, w); F.line([(a + 4, b + 3) for a, b in pts[:m]], col, w * 0.7)

def ficha_draw(F, cx, cy, tach=1.0, letra=0.0, foto=True):
    """ficha médica de 1986: foto, nombre (tachado), habitación y fecha"""
    papel(F, cx, cy, 760, 980, -1.5, col=PAPEL)
    F.text((cx, cy - 400), tr("SANTA BRÍGIDA"), 44, (120, 40, 40))
    F.line([(cx - 330, cy - 360), (cx + 330, cy - 360)], (150, 140, 120), 4)
    if foto:
        F.rect(cx - 330, cy - 330, cx - 60, cy - 30, fill=(180, 170, 150), outline=(110, 100, 80), w=4)
        J = NINO.draw(F, pose(a1u=20, a2u=-20), cx - 195, cy - 50, f=1, face="closed")
    F.text((cx + 120, cy - 280), tr("PACIENTE"), 40, (60, 60, 70))
    F.text((cx + 120, cy - 200), tr("HAB.") + " 114", 54, (40, 40, 50))
    F.text((cx + 120, cy - 110), "1986", 60, (170, 40, 40))
    F.text((cx - 250, cy + 70), tr("NOMBRE:"), 40, (60, 60, 70))
    nx = cx - 140
    if letra > 0:
        c = tuple(int(lerp(40, v, letra)) for v in YEL)
        F.text((nx + 40, cy + 72), "T", 70 + 30 * letra, c, stroke=4 * letra)
    else:
        F.text((nx + 40, cy + 72), "T", 70, (40, 40, 50))
    if tach > 0: garabato(F, nx + 90, cy + 40, cx + 330, cy + 105, tach, seed=3, w=12)
    for k in range(5):
        F.line([(cx - 330, cy + 180 + k * 60), (cx + lerp(0, 300, (k * 37 % 10) / 10), cy + 180 + k * 60)], (150, 160, 190), 6)

def carpeta_draw(F, cx, cy, w=520, h=640, lid=0.0):
    F.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill=(196, 150, 90), outline=(120, 86, 40), w=6)
    F.rect(cx - w / 2 + 40, cy - h / 2 - 50, cx - w / 2 + 220, cy - h / 2 + 5, fill=(196, 150, 90), outline=(120, 86, 40), w=6)
    F.rect(cx - 170, cy - 140, cx + 170, cy + 40, fill=(240, 236, 220), outline=(90, 80, 60), w=4)
    F.text((cx, cy - 90), "114", 110, (40, 30, 26))
    F.text((cx, cy + 5), "1986", 60, (170, 40, 40))

def dib_tachado(F, cx, cy, seed, p=1.0):
    """dibujo de pared_dibujos con la cara tachada"""
    dibujo(F, cx, cy, 120, 150, seed)
    r = random.Random(seed); r.uniform(-6, 6); r.randint(0, 30); r.randint(0, 30); r.randint(0, 40); off = r.uniform(-0.1, 0.1)
    hx, hy = cx + off * 120, cy - 40
    if p > 0: garabato(F, hx - 26, hy - 22, hx + 26, hy + 22, p, seed=seed, w=6)

def pared_tachada(F, x0, y0, cols, rows, p=1.0, dx=170, dy=200, seed=0, salvo=None):
    for i in range(rows):
        for j in range(cols):
            if salvo == (i, j): continue
            pk = clamp(p * 1.8 - (i * cols + j) / (rows * cols) * 0.8)
            dib_tachado(F, x0 + j * dx + (i % 2) * 30, y0 + i * dy, seed + i * 31 + j, pk)

def dib_leo_nora(F, cx, cy, w=120, h=150, malo=0.0):
    papel(F, cx, cy, w, h, 2, col=(240, 236, 222))
    if malo > 0: stick_cera(F, cx, cy + h * 0.38, h * lerp(0.4, 0.8, malo), CERA_NEGRA, 3, malo=True)
    stick_cera(F, cx - w * 0.22, cy + h * 0.38, h * 0.45, CERA_ROJA, 11, cap=True)
    stick_cera(F, cx + w * 0.22, cy + h * 0.38, h * 0.42, CERA_LILA, 12, coleta=True)

def columpio(F, x, piso, h=520, ang=0.0):
    F.line([(x - 220, piso), (x - 150, piso - h)], (90, 70, 50), 14); F.line([(x + 220, piso), (x + 150, piso - h)], (90, 70, 50), 14)
    F.line([(x - 170, piso - h), (x + 170, piso - h)], (90, 70, 50), 14)
    top = (x, piso - h); L_ = h - 170
    sx, sy = x + math.sin(ang) * L_, piso - h + math.cos(ang) * L_
    for d_ in (-60, 60): F.line([(x + d_, piso - h), (sx + d_, sy)], (60, 50, 40), 4)
    F.rect(sx - 75, sy, sx + 75, sy + 16, fill=(110, 80, 50))
    return sx, sy

def trio(F, t, x, piso=1300, walk_=True, sp=0.6, face="scared", lin_ang=4):
    """Leo (linterna), Nora y Carmen caminando hacia la derecha; devuelve el haz"""
    Jl = LEO.draw(F, add(walk(t, sp), LIN) if walk_ else LIN, x, piso, f=1, face=face)
    NORA.draw(F, walk(t + 0.3, sp) if walk_ else SCARED, x - 130, piso, f=1, face=face)
    big(CARMEN, 0.92, F, walk(t, sp * 0.7) if walk_ else STAND, x - 260, piso, f=1, face="neutral")
    return linterna_mano(F, Jl, lin_ang)

# ---------- escenas ----------
def busqueda(t, D, fi):
    zp = ease(t / D)
    cx = lerp(420, 640, zp)
    F = Frame(gradient(ARCH_A, ARCH_B), dict(x=cx, y=lerp(1060, 1020, zp), z=lerp(1.25, 1.15, zp)))
    archivo(F, seed=2)
    a = ease(seg(t, D * 0.3, D * 0.7))
    if a > 0: ojos_oscuridad(F, (cx + 260, 900), 120, a)
    h_ = trio(F, t, lerp(360, 560, zp), lin_ang=6 + 6 * math.sin(t * 1.5))
    letras(F, cx, 560, 5, t, ease(seg(t, 0, D * 0.4)), spread=0.8, size=90)
    img = iluminar(F.finish(), F, [(h_[0], h_[1], 1000, 0.3)], glows=[((cx, 560), 400, 0.8), ((cx + 260, 900), 240, 0.6 * a)], amb=0.14)
    return img, dict(grain=10, flash=((255, 255, 240), 0.4 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.1 * a))

def sotano(t, D, fi):
    w = ease(seg(t, 0, D * 0.75))
    F = Frame(gradient((30, 34, 32), (10, 12, 11)), dict(x=lerp(360, 560, w), y=1040, z=1.25))
    F.rect(-600, 1300, 1800, 2700, fill=(20, 22, 20)); F.line([(-600, 1300), (1800, 1300)], (60, 66, 60), 6)
    F.rect(-600, 1040, 1800, 1300, fill=(30, 36, 32))
    for k in range(6): F.line([(-500 + k * 300, 300), (-500 + k * 300, 1040)], (24, 28, 26), 6)  # tuberías
    F.line([(-600, 360), (1800, 360)], (50, 56, 52), 16)
    op = ease(seg(t, D * 0.5, D * 0.85))
    F.rect(680, 720, 960, 1300, fill=(54, 58, 54)); F.rect(700, 740, 940, 1300, fill=(4, 4, 5))
    F.poly([(700, 740), (lerp(940, 740, op), 740 - 30 * op), (lerp(940, 740, op), 1300 + 30 * op), (700, 1300)], fill=(96, 100, 92), outline=(50, 54, 50), w=5)
    F.rect(710, 620, 930, 690, fill=(200, 196, 170), outline=(60, 56, 50), w=4)
    F.text((820, 655), tr("ARCHIVO"), 42, (40, 30, 26))
    F.text((560, 760), "-1", 70, (90, 96, 90))
    h_ = trio(F, t, lerp(200, 600, w), walk_=w < 1, lin_ang=lerp(10, -4, w))
    img = iluminar(F.finish(), F, [(h_[0], h_[1], 1000, 0.3)], glows=[((lerp(70, 470, w), 1150), 260, 0.35), ((820, 655), 160, 0.5)], amb=0.14)
    return img, dict(grain=10)

def estanterias(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient(ARCH_A, ARCH_B), dict(x=lerp(420, 520, zp), y=lerp(1000, 960, zp), z=lerp(1.15, 1.05, zp)))
    archivo(F, seed=7, sep=300)
    J = LEO.draw(F, LIN, 360, 1300, f=1, face="neutral")
    NORA.draw(F, STAND, 240, 1300, f=1, face="scared")
    big(CARMEN, 0.92, F, STAND, 120, 1300, f=1, face="neutral")
    ang = -40 + 50 * math.sin(t * 1.2)
    h_ = linterna_mano(F, J, ang)
    polvo(F, t, fi, 700, 900, 700, 500, 40)
    img = iluminar(F.finish(), F, [(h_[0], h_[1], 1300, 0.28)], glows=[((240, 1150), 220, 0.3)], amb=0.12)
    return img, dict(grain=11)

def carpeta(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient(ARCH_A, ARCH_B), dict(x=540, y=900, z=lerp(1.0, 1.1, zp)))
    # fila de carpetas vistas de frente
    r = random.Random(3)
    for k in range(9):
        x = 40 + k * 125
        F.rect(x, 380, x + 110, 1180, fill=r.choice([(150, 120, 80), (130, 104, 70), (170, 150, 110)]), outline=(50, 40, 30), w=3)
        F.rect(x + 15, 430, x + 95, 490, fill=(230, 226, 210)); F.text((x + 55, 460), str(1978 + k), 22, (40, 30, 26))
    out = ease_out(seg(t, D * 0.35, D * 0.8))
    F.rect(-100, 1180, 1200, 1230, fill=(90, 94, 100))
    cy = lerp(780, 860, out)
    if out > 0:
        carpeta_draw(F, 540, cy, 520 * lerp(0.25, 1, out), 640 * lerp(1.25, 1, out))
        F.line([(1100, 1500), (720, cy + 260)], (160, 90, 255), 50)          # brazo de Nora
        F.circle((700, cy + 260), 42, fill=(240, 240, 240))
    img = iluminar(F.finish(), F, [((540, 1700), math.radians(-90), 1500, 0.35)], glows=[((540, cy), 420, 0.9 * out + 0.2)], amb=0.14)
    return img, dict(grain=10, flash=((255, 240, 200), 0.3 * math.exp(-abs(t - D * 0.6) * 8)))

def ficha(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient((20, 18, 16), (6, 6, 5)), dict(x=540, y=lerp(900, 860, zp), z=lerp(0.95, 1.05, zp)))
    F.rect(140, 260, 940, 1440, fill=(196, 150, 90), outline=(120, 86, 40), w=8)
    up = ease_out(seg(t, 0, D * 0.4))
    ficha_draw(F, 540, lerp(1300, 860, up), tach=1.0)
    img = iluminar(F.finish(), F, [], glows=[((540, 860), 560, 1.0)], amb=0.12)
    return img, dict(grain=10)

def tachado(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient((20, 18, 16), (6, 6, 5)), dict(x=lerp(560, 600, zp), y=lerp(900, 930, zp), z=lerp(1.4, 2.1, zp)))
    ficha_draw(F, 540, 860, tach=ease(seg(t, D * 0.15, D * 0.75)) * 0.4 + 0.6)
    img = iluminar(F.finish(), F, [], glows=[((640, 930), 420, 1.0)], amb=0.12)
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * seg(t, D * 0.3, D)))

def letra(t, D, fi):
    g = ease(seg(t, D * 0.2, D * 0.6))
    F = Frame(gradient((20, 18, 16), (6, 6, 5)), dict(x=lerp(500, 440, g), y=930, z=lerp(2.0, 2.5, g)))
    ficha_draw(F, 540, 860, tach=1.0, letra=g)
    img = iluminar(F.finish(), F, [], glows=[((440, 930), 260 + 200 * g, 1.0)], amb=0.1, warm=(255, 230, 120))
    return img, dict(grain=9, flash=((255, 230, 120), 0.35 * math.exp(-abs(t - D * 0.45) * 9)))

def foto_nino(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient((26, 24, 22), (8, 8, 7)), dict(x=540, y=900, z=lerp(1.0, 1.12, zp)))
    papel(F, 540, 860, 760, 900, -2, col=(232, 226, 206))
    F.rect(200, 450, 880, 1220, fill=(150, 160, 150))
    F.rect(200, 1060, 880, 1220, fill=(110, 116, 96))
    F.rect(560, 460, 870, 900, fill=(190, 186, 170))                                   # pared del hospital al fondo
    for k in range(3): F.rect(590 + k * 95, 520, 660 + k * 95, 620, fill=(120, 130, 140))
    ang = 0.22 * math.sin(t * 1.6)
    sx, sy = columpio(F, 430, 1120, 560, ang)
    J = big(NINO, 1.0, F, pose(l1u=80, l1l=-90, l2u=70, l2l=-85, a1u=170, a1l=0, a2u=-170, a2l=0, head=12), sx, sy + 60, f=1, face="closed")
    img = iluminar(F.finish(), F, [], glows=[((540, 860), 520, 1.0)], amb=0.15, warm=(255, 230, 180))
    return sepia(img, 0.9, fi), dict(grain=12)

def apagon(t, D, fi):
    off = t > D * 0.62
    F = Frame(gradient(ARCH_A, ARCH_B), dict(x=520, y=1000, z=1.3 + 0.1 * ease(t / D)))
    archivo(F, seed=11)
    J = LEO.draw(F, LIN, 470, 1300, f=1, face="scared")
    NORA.draw(F, SCARED, 350, 1300, f=1, face="scared")
    big(CARMEN, 0.92, F, STAND, 230, 1300, f=1, face="neutral")
    h_ = linterna_mano(F, J, -20)
    fl = (noise(t * 18, 2) > -0.1) if t > D * 0.25 else True
    on = fl and not off
    img = iluminar(F.finish(), F, [(h_[0], h_[1], 1000, 0.3)] if on else [], glows=[((350, 1150), 260, 0.3)] if on else [], amb=0.12 if on else 0.02)
    return img, dict(grain=12, dark=0.35 if off else 0)

def sabe(t, D, fi):
    k = ease(seg(t, 0, D * 0.8))
    sh = 8 * k
    F = Frame(gradient((16, 12, 18), (4, 3, 5)), dict(x=540, y=lerp(1100, 960, k), z=lerp(1.25, 1.0, k), sx=noise(t * 30) * sh, sy=noise(t * 30, 2) * sh))
    archivo(F, x0=-300, x1=1500, seed=11, sep=420)
    enemy(F, add(pose(a1u=60 + 40 * k, a1l=50, a2u=-60 - 40 * k, a2l=-50, head=-10), jitter(t, 2, 4)), 560, 1300, lerp(1.6, 2.6, k), f=-1)
    NORA.draw(F, SCARED, 220, 1300, f=1, face="scared")
    LEO.draw(F, SCARED, 340, 1300, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((560, 700), 420, 0.6 * k + 0.2), ((280, 1150), 220, 0.3)], amb=0.14, warm=(220, 160, 255))
    return img, dict(grain=12, tint=((255, 0, 30), 0.22 * k), glitch=0.35 if k > 0.6 and fi % 4 == 0 else 0)

def huida(t, D, fi):
    cx = 500 + t * 640
    F = Frame(gradient(ARCH_A, ARCH_B), dict(x=cx, y=1060, z=1.25, sx=noise(t * 25) * 8, sy=noise(t * 25, 1) * 8))
    archivo(F, x0=-800, x1=5200, seed=20)
    xl = cx + 200; xn = cx + 60; xc = cx - 70
    Jl = LEO.draw(F, run(t, 1.15), xl, 1300, f=1, face="scared")
    NORA.draw(F, run(t + 0.17, 1.15), xn, 1300, f=1, face="scared")
    big(CARMEN, 0.92, F, run(t + 0.3, 0.9), xc, 1300, f=1, face="scared")
    r = random.Random(5)
    for i in range(26):          # papeles volando
        ph = r.uniform(0, 6); sp = r.uniform(300, 700)
        x = cx - 500 + ((t * sp + r.uniform(0, 1200)) % 1300)
        y = r.uniform(500, 1250) + 60 * math.sin(t * 4 + ph)
        a = t * r.uniform(3, 7) + ph; c, s_ = math.cos(a), math.sin(a)
        pts = [(x + dx * c - dy * s_, y + dx * s_ + dy * c) for dx, dy in ((-26, -34), (26, -34), (26, 34), (-26, 34))]
        F.poly(pts, fill=(226, 220, 196), outline=(150, 140, 120), w=2)
    a_ = ease(seg(t, D * 0.2, D * 0.5))
    if a_ > 0: ojos_oscuridad(F, (cx - 420 + 30 * noise(t * 2, 4), 980), 90, a_)
    img = iluminar(F.finish(), F, [], glows=[((xn, 1100), 380, 0.45), ((cx - 420, 980), 150, 0.4 * a_)], amb=0.14)
    return img, dict(grain=10, glitch=0.3 if a_ > 0.5 and fi % 5 == 0 else 0, tint=((255, 0, 30), 0.1 * a_))

def vuelta114(t, D, fi):
    w = ease(seg(t, 0, D * 0.7))
    F = Frame(gradient((40, 46, 40), (16, 18, 16)), dict(x=540, y=1040, z=1.2))
    cuarto114(F)
    for i in range(3):
        for j in range(6): dibujo(F, 60 + j * 170 + (i % 2) * 30, 420 + i * 200, 120, 150, 300 + i * 31 + j)
    F.rect(-200, 700, 60, 1300, fill=(6, 6, 8))
    Jl = LEO.draw(F, run(t, 1.0) if w < 1 else SCARED, lerp(-60, 640, w), 1300, f=1, face="scared")
    NORA.draw(F, run(t + 0.2, 1.0) if w < 1 else SCARED, lerp(-180, 480, w), 1300, f=1, face="scared")
    big(CARMEN, 0.92, F, run(t + 0.3, 0.8) if w < 1 else STAND, lerp(-320, 320, w), 1300, f=1, face="neutral")
    img = iluminar(F.finish(), F, [], glows=[((540, 1000), 520, 0.55)], amb=0.18)
    return img, dict(grain=10, dark=0.1)

def tachados(t, D, fi):
    p = ease(seg(t, D * 0.1, D * 0.75))
    zp = ease(t / D)
    F = Frame(gradient((40, 46, 40), (16, 18, 16)), dict(x=540, y=lerp(960, 900, zp), z=lerp(1.05, 1.18, zp)))
    cuarto114(F)
    pared_tachada(F, 60, 380, 6, 4, p, seed=300)
    NORA.draw(F, SCARED, 360, 1300, f=1, face="scared")
    LEO.draw(F, SCARED, 720, 1300, f=-1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((540, 800), 600, 0.7)], amb=0.16)
    return img, dict(grain=11, tint=((255, 0, 30), 0.15 * p), flash=((255, 30, 40), 0.25 * math.exp(-abs(t - D * 0.5) * 8)))

def menos(t, D, fi):
    zp = ease(seg(t, 0, D * 0.55))
    F = Frame(gradient((40, 46, 40), (16, 18, 16)), dict(x=lerp(540, 560, zp), y=lerp(800, 700, zp), z=lerp(1.2, 3.6, zp)))
    cuarto114(F)
    pared_tachada(F, 60, 380, 6, 4, 1.0, seed=300, salvo=(1, 3))
    m = ease(seg(t, D * 0.55, D * 0.9))
    dib_leo_nora(F, 60 + 3 * 170 + 30, 580, malo=m)
    img = iluminar(F.finish(), F, [], glows=[((590, 580), 160 + 80 * m, 1.0)], amb=0.12)
    return img, dict(grain=11, tint=((255, 0, 30), 0.25 * m), glitch=0.35 if m > 0.8 and fi % 4 == 0 else 0,
                     flash=((255, 30, 40), 0.3 * math.exp(-abs(t - D * 0.75) * 9)))

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    img = F.finish(); d = ImageDraw.Draw(img)
    d.text((540, 460), tr("PARTE 8"), font=font(190), fill=YEL, anchor="mm", stroke_width=14, stroke_fill=(0, 0, 0))
    return img, {}

ESCENA_FN = dict(busqueda=busqueda, sotano=sotano, estanterias=estanterias, carpeta=carpeta, ficha=ficha, tachado=tachado, letra=letra,
                 foto_nino=foto_nino, apagon=apagon, sabe=sabe, huida=huida, vuelta114=vuelta114, tachados=tachados, menos=menos, final=final)
PAUSA = dict(busqueda=0.5, sotano=0.4, estanterias=0.4, carpeta=0.5, ficha=0.4, tachado=0.5, letra=0.8, foto_nino=0.6, apagon=0.7,
             sabe=0.8, huida=0.4, vuelta114=0.4, tachados=0.6, menos=1.2, final=2.0)
