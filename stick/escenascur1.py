"""Curiosidades 1 (estilo Zack D. en 2D): cabeza de maniquí de perfil, vista de rayos X de la vía aérea,
presión, rotura, cuello hinchado, placa con aire atrapado, cama de hospital con sonda.
Piezas reutilizables: fondo_claro, fondo_rx, MANIQUI, cabeza_perfil, via_aerea, mano, medidor, cama_sonda."""
import math, random
from PIL import ImageDraw
from motor import *
from escenas2 import big

PIEL, PIEL_O = (196, 198, 204), (120, 124, 134)          # maniquí gris
CLARO = ((236, 232, 226), (198, 194, 188))
RX = ((8, 20, 44), (2, 6, 16))
AZUL_RX, ROSA = (120, 200, 255), (240, 120, 140)
ROJO = (235, 40, 50)
MANIQUI = Fig(shirt=(150, 154, 164), limb=PIEL)

def fondo_claro(): return gradient(*CLARO)
def fondo_rx(): return gradient(*RX)

def cabeza_perfil(F, cx, cy, s=1.0, rx=False, cuello=1.0, mejillas=0.0, cara="neutral", t=0.0):
    """cabeza de perfil mirando a la derecha. rx=True: solo contorno azul (rayos X). Devuelve puntos clave."""
    r = 250 * s; cw = 130 * s * cuello
    nariz = (cx + r * 0.98, cy - r * 0.05); boca = (cx + r * 0.80, cy + r * 0.42)
    if rx:
        o = AZUL_RX
        F.circle((cx, cy), r, outline=o, w=6)
        F.rect(cx - cw / 2 - 10 * s, cy + r * 0.75, cx + cw / 2 + 30 * s, cy + r * 2.6, outline=o, w=6)
        F.poly([(nariz[0] - 10, nariz[1] - 50 * s), (nariz[0] + 55 * s, nariz[1] + 40 * s), (nariz[0] - 5, nariz[1] + 50 * s)], outline=o, w=5)
        F.circle((cx - r * 0.1, cy - r * 0.15), r * 0.55, outline=(60, 110, 170), w=3)      # cráneo
    else:
        F.rect(cx - cw / 2 - 10 * s, cy + r * 0.6, cx + cw / 2 + 30 * s, cy + r * 2.8, fill=PIEL, outline=PIEL_O, w=5)
        F.circle((cx, cy), r, fill=PIEL, outline=PIEL_O, w=6)
        if mejillas > 0: F.ellipse((cx + r * 0.62, cy + r * 0.28), r * 0.32 * (1 + mejillas * 0.5), r * 0.26 * (1 + mejillas * 0.6), fill=PIEL, outline=PIEL_O, w=4)
        F.poly([(nariz[0] - 10, nariz[1] - 50 * s), (nariz[0] + 55 * s, nariz[1] + 40 * s), (nariz[0] - 5, nariz[1] + 50 * s)], fill=PIEL, outline=PIEL_O, w=4)
        ex, ey = cx + r * 0.55, cy - r * 0.25
        if cara == "scared":
            F.circle((ex, ey), 30 * s, fill=(250, 250, 250), outline=PIEL_O, w=3); F.circle((ex + 8 * s, ey), 13 * s, fill=(20, 20, 26))
        elif cara == "closed":
            F.line([(ex - 25 * s, ey + 4 * s), (ex + 22 * s, ey - 6 * s)], (40, 40, 50), 7 * s)
        else:
            F.circle((ex, ey), 22 * s, fill=(250, 250, 250), outline=PIEL_O, w=3); F.circle((ex + 6 * s, ey), 11 * s, fill=(20, 20, 26))
        F.line([(boca[0] - 50 * s, boca[1]), (boca[0], boca[1] - 4 * s)], (90, 90, 100), 6 * s)
        F.ellipse((cx - r * 0.15, cy - r * 0.05), r * 0.13, r * 0.2, fill=(180, 182, 190), outline=PIEL_O, w=3)    # oreja
    garganta = (cx + 20 * s, cy + r * 1.75)
    return dict(nariz=nariz, boca=boca, garganta=garganta, r=r, cw=cw)

def via_aerea(F, cx, cy, s=1.0, presion=0.0, rotura=0.0, t=0.0, seed=0):
    """tubo de aire (nariz -> faringe -> tráquea) con partículas; presión 0-1 (rojo); rotura 0-1 (grieta y fuga)"""
    r = 250 * s
    P = [(cx + r * 0.95, cy + r * 0.02), (cx + r * 0.35, cy + r * 0.05), (cx + r * 0.1, cy + r * 0.35),
         (cx + r * 0.1, cy + r * 1.2), (cx + r * 0.1, cy + r * 2.6)]
    boca = [(cx + r * 0.78, cy + r * 0.42), (cx + r * 0.3, cy + r * 0.45), (cx + r * 0.12, cy + r * 0.5)]
    col = tuple(int(lerp(a, b, presion)) for a, b in zip(ROSA, ROJO))
    w = 70 * s * (1 + 0.25 * presion * (1 + 0.15 * math.sin(t * 30)))
    F.line(P, (60, 20, 30), w + 14 * s); F.line(boca, (60, 20, 30), 50 * s + 14 * s)
    F.line(P, col, w); F.line(boca, col, 50 * s)
    # partículas de aire: con presión se aprietan y vibran
    rr = random.Random(seed)
    n = int(18 + 40 * presion)
    for k in range(n):
        u = (rr.random() + t * (0.6 - 0.55 * presion)) % 1.0
        seg_i = min(3, int(u * 4)); f = u * 4 - seg_i
        x = lerp(P[seg_i][0], P[seg_i + 1][0], f) + rr.uniform(-1, 1) * w * 0.3 + noise(t * 20, k) * 8 * presion
        y = lerp(P[seg_i][1], P[seg_i + 1][1], f) + rr.uniform(-1, 1) * w * 0.3
        F.circle((x, y), (6 + 4 * presion) * s, fill=(255, 255, 255))
    g = (cx + r * 0.1, cy + r * 1.35)
    if rotura > 0:
        cr = [(g[0] - 30 * s, g[1] - 40 * s), (g[0] + 10 * s, g[1] - 5 * s), (g[0] - 15 * s, g[1] + 20 * s), (g[0] + 25 * s, g[1] + 55 * s)]
        F.line(cr[:max(2, int(len(cr) * min(1, rotura * 2)))], (255, 255, 255), 9 * s)
        for k in range(int(30 * rotura)):                         # aire que se escapa al cuello
            a = rr.uniform(-1.2, 1.2); d = rr.uniform(20, 220) * s * ease_out(rotura)
            F.circle((g[0] + math.cos(a) * d * 1.3, g[1] + math.sin(a) * d), rr.uniform(6, 14) * s, outline=(255, 255, 255), w=3)
    return dict(garganta=g)

def mano(F, x, y, s=1.0, ang=0.0, pinza=False):
    """mano de maniquí (palma + dedos) que entra desde abajo"""
    a = math.radians(ang)
    F.line([(x - math.sin(a) * 600 * s, y + math.cos(a) * 600 * s), (x, y)], PIEL, 70 * s); F.line([(x - math.sin(a) * 600 * s, y + math.cos(a) * 600 * s), (x, y)], PIEL_O, 4)
    F.circle((x, y), 55 * s, fill=PIEL, outline=PIEL_O, w=4)
    for k in range(4 if not pinza else 2):
        d = (k - 1.5) * 26 * s if not pinza else (k - 0.5) * 50 * s
        F.line([(x + d, y - 30 * s), (x + d * 1.1, y - 95 * s)], PIEL, 24 * s)

def medidor(F, x, y, v, s=1.0):
    F.rect(x - 40 * s, y - 300 * s, x + 40 * s, y + 300 * s, fill=(20, 20, 26), outline=(240, 240, 240), w=5)
    h = 590 * s * clamp(v)
    col = tuple(int(lerp(a, b, v)) for a, b in zip((80, 220, 120), ROJO))
    F.rect(x - 32 * s, y + 295 * s - h, x + 32 * s, y + 295 * s, fill=col)
    F.text((x, y - 350 * s), tr("PRESIÓN"), 40 * s, (255, 255, 255), stroke=4)

def _cuarto_claro(F, piso=1300):
    F.rect(-600, piso, 1700, 2800, fill=(176, 172, 166)); F.line([(-600, piso), (1700, piso)], (150, 146, 140), 6)

# ---------- escenas ----------
def agujero(t, D, fi):
    pr = ease(seg(t, 0, D * 0.45)); rot = seg(t, D * 0.48, D * 0.75)
    sh = 18 * (rot > 0) * (1 - rot)
    F = Frame(fondo_rx(), dict(x=540 + noise(t * 40) * sh, y=lerp(1000, 1080, ease(t / D)), z=lerp(1.05, 1.35, ease(t / D)), sx=noise(t * 50, 1) * sh))
    cabeza_perfil(F, 470, 760, 1.0, rx=True)
    via_aerea(F, 470, 760, 1.0, presion=pr, rotura=rot, t=t)
    hit = rot > 0
    return F.finish(), dict(flash=((255, 60, 60), max(0, 1 - (t - D * 0.48) / 0.3)) if hit else None, glitch=0.3 if hit and fi % 4 == 0 else 0,
                            tint=((255, 0, 30), 0.15 * rot), grain=6)

def picor(t, D, fi):
    k = ease(seg(t, D * 0.25, D))
    F = Frame(fondo_claro(), dict(x=lerp(540, 600, k), y=lerp(1000, 760, k), z=lerp(1.0, 2.6, k)))
    _cuarto_claro(F)
    J = big(MANIQUI, 1.6, F, pose(head=-8 - 10 * seg(t, D * 0.5, D)), 560, 1300, f=1, face="neutral")
    nz = J["head"]
    for i in range(3):                       # líneas de picor en la nariz
        a = -0.6 + i * 0.6 + 0.2 * math.sin(t * 20)
        F.line([(nz[0] + 55 + math.cos(a) * 20, nz[1] + math.sin(a) * 20), (nz[0] + 55 + math.cos(a) * 45, nz[1] + math.sin(a) * 45)], ROJO, 5)
    img = F.finish(); d = ImageDraw.Draw(img)
    p = ease_back(seg(t, D * 0.5, D * 0.65))
    if p > 0:
        d.text((790, 520), "A… A…", font=font(90 * p + 1), fill=(30, 30, 40), anchor="mm", stroke_width=6, stroke_fill=(255, 255, 255))
    return img, dict(grain=4)

def tapa(t, D, fi):
    m1 = ease_out(seg(t, D * 0.15, D * 0.4)); m2 = ease_out(seg(t, D * 0.45, D * 0.7))
    inf = ease(seg(t, D * 0.7, D)) * (1 + 0.1 * math.sin(t * 25))
    F = Frame(fondo_claro(), dict(x=560, y=960, z=1.0))
    c = cabeza_perfil(F, 440, 820, 1.0, mejillas=inf, cara="closed" if t > D * 0.4 else "neutral")
    nx, ny = c["nariz"]; bx, by = c["boca"]
    mano(F, lerp(nx + 80, nx + 20, m1), lerp(ny + 700, ny + 20, m1), 0.7, ang=-15, pinza=True)
    if m2 > 0: mano(F, lerp(bx + 200, bx + 30, m2), lerp(by + 700, by + 40, m2), 0.75, ang=-35)
    return F.finish(), dict(grain=4)

def presion(t, D, fi):
    pr = ease(seg(t, 0, D * 0.9))
    sh = 6 * pr
    F = Frame(fondo_rx(), dict(x=560 + noise(t * 40) * sh, y=1000, z=1.0, sx=noise(t * 50, 2) * sh))
    cabeza_perfil(F, 440, 700, 1.0, rx=True)
    via_aerea(F, 440, 700, 1.0, presion=pr, t=t)
    medidor(F, 930, 760, pr, 0.9)
    return F.finish(), dict(grain=5, tint=((255, 0, 30), 0.12 * pr))

def pop(t, D, fi):
    rot = seg(t, D * 0.1, D * 0.5); sh = 26 * (1 - seg(t, D * 0.1, D * 0.6)) * (t > D * 0.1)
    F = Frame(fondo_rx(), dict(x=500 + noise(t * 50) * sh, y=lerp(1050, 1120, ease(t / D)), z=lerp(1.5, 1.8, ease(t / D)), sx=noise(t * 60, 3) * sh))
    cabeza_perfil(F, 440, 700, 1.0, rx=True)
    via_aerea(F, 440, 700, 1.0, presion=1 - 0.6 * rot, rotura=rot, t=t)
    img = F.finish(); d = ImageDraw.Draw(img)
    p = ease_back(seg(t, D * 0.1, D * 0.3))
    if p > 0: d.text((760, 620), "¡POP!", font=font(170 * p + 1), fill=(255, 214, 0), anchor="mm", stroke_width=12, stroke_fill=(0, 0, 0))
    return img, dict(flash=((255, 255, 255), max(0, 1 - (t - D * 0.1) / 0.25)) if t > D * 0.1 else None, glitch=0.35 if fi % 3 == 0 and t > D * 0.1 else 0,
                     tint=((255, 0, 30), 0.2), grain=6)

def hinchado(t, D, fi):
    k = ease(seg(t, 0, D * 0.8))
    F = Frame(fondo_claro(), dict(x=520, y=1000, z=1.0))
    cabeza_perfil(F, 440, 640, 0.9, cuello=1 + 1.1 * k, cara="scared")
    mano(F, 640 + 40 * math.sin(t * 6), 1060, 0.7, ang=-20)
    for i in range(3):                         # ondas de dolor
        rr = 60 + ((t * 120 + i * 50) % 150)
        F.circle((470, 1000), rr, outline=(235, 40, 50), w=4)
    return F.finish(), dict(grain=4, tint=((255, 0, 30), 0.08 * k))

def hospital(t, D, fi):
    F = Frame(gradient((30, 34, 40), (14, 16, 20)), dict(x=540, y=900, z=lerp(1.0, 1.12, ease(t / D))))
    F.rect(140, 260, 940, 1260, fill=(230, 240, 250), outline=(120, 130, 140), w=14)        # negatoscopio
    F.rect(180, 300, 900, 1220, fill=(10, 18, 30))
    # tórax y cuello en rayos X
    F.rect(470, 300, 610, 640, outline=AZUL_RX, w=5)
    F.ellipse((540, 900), 300, 280, outline=AZUL_RX, w=5)
    for k in range(6): F.arc((540, 760 + k * 60), 280 - k * 10, 200, 340, (90, 150, 210), 5)
    F.line([(540, 300), (540, 840)], ROSA, 26)
    rr = random.Random(4)
    for k in range(34):
        x = 540 + rr.uniform(-1, 1) * (70 if k < 14 else 220); y = (rr.uniform(330, 640) if k < 14 else rr.uniform(700, 1000))
        p = ease_back(seg(t, 0.2 + k * 0.03, 0.5 + k * 0.03))
        if p > 0: F.circle((x, y), rr.uniform(8, 18) * p, outline=(255, 255, 255), w=4)
    img = F.finish(); d = ImageDraw.Draw(img)
    p = ease_back(seg(t, D * 0.55, D * 0.7))
    if p > 0:
        d.rounded_rectangle((300, 1330, 780, 1430), 24, fill=ROJO)
        d.text((540, 1380), tr("AIRE ATRAPADO"), font=font(56 * p + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=5)

def sonda(t, D, fi):
    F = Frame(fondo_claro(), dict(x=560, y=1040, z=1.2))
    _cuarto_claro(F)
    F.rect(160, 1120, 900, 1200, fill=(240, 240, 244), outline=(160, 160, 170), w=5); F.rect(160, 1100, 900, 1130, fill=(200, 220, 240))
    for lx in (180, 880): F.line([(lx, 1200), (lx, 1300)], (150, 150, 160), 10)
    J = MANIQUI.draw(F, pose(l1u=90, l2u=90, l1l=0, l2l=0, a1u=20, a2u=-20), 520, 1090, f=1, rot=-90, snap=False, face="closed")
    F.line([(900, 1300), (900, 640)], (160, 160, 170), 8); F.rect(860, 640, 940, 760, fill=(250, 246, 220), outline=(160, 160, 170), w=4)
    hx, hy = J["head"]
    F.line([(900, 760), (860, 860), (hx + 20, hy - 20), (hx + 10, hy + 5)], (255, 255, 255), 6)
    img = F.finish(); d = ImageDraw.Draw(img)
    n = min(7, 1 + int(7 * seg(t, 0.2, D * 0.8)))
    d.rounded_rectangle((330, 330, 750, 470), 30, fill=(20, 20, 26))
    d.text((540, 400), f"{tr('DÍA')} {n}/7", font=font(80), fill=(255, 214, 0) if n == 7 else (255, 255, 255), anchor="mm")
    return img, dict(grain=4)

def final(t, D, fi):
    F = Frame(fondo_claro(), dict(x=540, y=960, z=1.0))
    _cuarto_claro(F)
    s = ease_back(seg(t, D * 0.45, D * 0.6))
    J = big(MANIQUI, 1.7, F, mix(pose(head=-10), pose(body=-12, head=-25, a1u=30, a2u=-30), s), 540, 1300, f=1, face="closed" if s > 0.5 else "neutral")
    img = F.finish(); d = ImageDraw.Draw(img)
    if s > 0: d.text((720, 560), "¡ACHÍS!", font=font(110 * s + 1), fill=(30, 30, 40), anchor="mm", stroke_width=8, stroke_fill=(255, 255, 255))
    p = ease_back(seg(t, 0.1, 0.4))
    d.text((540, 250), tr("NO AGUANTES"), font=font(110 * p + 1), fill=ROJO, anchor="mm", stroke_width=10, stroke_fill=(255, 255, 255))
    d.text((540, 370), tr("UN ESTORNUDO"), font=font(110 * p + 1), fill=ROJO, anchor="mm", stroke_width=10, stroke_fill=(255, 255, 255))
    d.text((540, 1460), tr("Caso real · BMJ Case Reports, 2018"), font=font(38), fill=(60, 60, 70), anchor="mm")
    q = ease_back(seg(t, D * 0.65, D * 0.8))
    if q > 0:
        d.rounded_rectangle((250, 1560, 830, 1670), 30, fill=ROJO)
        d.text((540, 1615), tr("SÍGUEME PARA MÁS"), font=font(56 * q + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=4)

ESCENA_FN = dict(agujero=agujero, picor=picor, tapa=tapa, presion=presion, pop=pop, hinchado=hinchado, hospital=hospital, sonda=sonda, final=final)
PAUSA = dict(agujero=0.4, picor=0.2, tapa=0.3, presion=0.2, pop=0.5, hinchado=0.2, hospital=0.3, sonda=0.3, final=1.8)
