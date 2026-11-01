"""Escenas del episodio 8 (La ciudad dormida): calles llenas de gente dormida de pie que gira la cabeza,
persecución del Sonriente, la placa de Santa Brígida con el nombre (Tomás) y el coche vacío de Carmen."""
import math, random
from PIL import ImageDraw
from motor import *
from escenas import base
from escenas2 import enemy, big
from escenas3 import YEL
from escenas5 import iluminar, ojos_oscuridad, CERA_NEGRA

# ---------- figuras: gente dormida de pie ----------
_CAMISAS = [(90, 110, 140), (140, 90, 80), (80, 120, 100), (150, 140, 110), (110, 90, 130), (70, 80, 90), (160, 120, 60)]
DORMIDOS = [Fig(shirt=c, limb=(200, 202, 210), scale=0.9) for c in _CAMISAS]
DUERME = pose(body=4, head=18, a1u=6, a1l=4, a2u=-6, a2l=4)

def dormido(F, x, piso, t, i, mira=None, giro=0.0, sc=0.9):
    """persona dormida de pie (ojos cerrados, cabeza caída, balanceo). mira = x hacia la que gira la cabeza"""
    fig = DORMIDOS[i % len(DORMIDOS)]
    r = random.Random(i * 13)
    f = 1 if r.random() < 0.5 else -1
    p = dict(DUERME); p["body"] = 4 + 3 * math.sin(t * 1.3 + i)
    if mira is not None and giro > 0:
        f = 1 if mira > x else -1
        p["head"] = lerp(18, -12, giro)
    big(fig, sc * r.uniform(0.92, 1.08), F, p, x, piso, f=f, face="closed")

def farola(F, x, piso, on=1.0):
    F.line([(x, piso), (x, piso - 640)], (40, 42, 56), 12); F.line([(x, piso - 640), (x - 80, piso - 640)], (40, 42, 56), 10)
    F.ellipse((x - 90, piso - 625), 34, 14, fill=tuple(int(lerp(50, v, on)) for v in (255, 230, 160)))

def edificios(F, x0, x1, piso, seed=0, lit=0.04):
    r = random.Random(seed); x = x0
    while x < x1:
        w = r.randint(150, 260); h = r.randint(500, 1000); top = piso - h
        F.rect(x, top, x + w - 10, piso, fill=(16, 18, 32))
        for wy in range(int(top) + 30, piso - 60, 62):
            for wx in range(x + 18, x + w - 34, 44):
                F.rect(wx, wy, wx + 22, wy + 32, fill=(255, 210, 120) if r.random() < lit else (26, 30, 48))
        x += w

def calle(F, x0, x1, piso=1300, seed=0, lamps=None):
    F.circle((860 if x1 < 2000 else x0 + 900, 380), 70, fill=(220, 224, 236))
    edificios(F, x0 - 300, x1 + 300, piso - 120, seed)
    F.rect(x0 - 600, piso - 120, x1 + 600, piso, fill=(34, 36, 46))           # acera
    F.rect(x0 - 600, piso, x1 + 600, piso + 1400, fill=(18, 19, 26))
    F.line([(x0 - 600, piso), (x1 + 600, piso)], (54, 56, 70), 6)
    for k in range(int((x1 - x0) / 240) + 4): F.rect(x0 - 300 + k * 240, piso + 160, x0 - 200 + k * 240, piso + 178, fill=(180, 176, 140))
    for k, lx in enumerate(lamps if lamps is not None else range(int(x0) + 200, int(x1), 650)):
        farola(F, lx, piso - 60, 1.0)

def coche_draw(F, x, piso, puerta=0.0, sonrisa=0.0):
    """coche de Carmen visto de lado (morro a la izquierda); puerta = 0 cerrada, 1 abierta"""
    col, osc = (120, 44, 40), (70, 24, 22)
    F.rect(x - 280, piso - 170, x + 280, piso - 50, fill=col, outline=osc, w=6)
    F.poly([(x - 170, piso - 170), (x + 210, piso - 170), (x + 150, piso - 280), (x - 110, piso - 280)], fill=col, outline=osc, w=6)
    glass = (60, 80, 110)
    F.poly([(x - 150, piso - 176), (x + 10, piso - 176), (x + 10, piso - 268), (x - 100, piso - 268)], fill=glass)
    F.poly([(x + 30, piso - 176), (x + 190, piso - 176), (x + 140, piso - 268), (x + 30, piso - 268)], fill=glass)
    if sonrisa > 0:   # sonrisa dibujada con el dedo en el cristal empañado
        c = tuple(int(lerp(v, 240, sonrisa)) for v in glass)
        F.arc((x + 100, piso - 236), 34, 20, 160, c, 6)
        for dx in (-14, 14): F.circle((x + 100 + dx, piso - 240), 5, fill=c)
    F.rect(x - 286, piso - 140, x - 262, piso - 110, fill=(255, 240, 190)); F.rect(x + 262, piso - 140, x + 286, piso - 110, fill=(200, 30, 30))
    if puerta > 0:   # puerta delantera abierta hacia la cámara: hueco oscuro + puerta
        F.rect(x - 150, piso - 170, x + 10, piso - 56, fill=(10, 8, 10))
        F.poly([(x - 150, piso - 176), (x - 150 - 120 * puerta, piso - 150), (x - 150 - 120 * puerta, piso - 40), (x - 150, piso - 56)],
               fill=col, outline=osc, w=5)
    for wx in (x - 175, x + 175):
        F.circle((wx, piso - 46), 48, fill=(20, 20, 24)); F.circle((wx, piso - 46), 20, fill=(110, 110, 116))

def baston(F, x, y, ang=8):
    a = math.radians(ang); L_ = 210
    F.line([(x, y), (x + math.cos(a) * L_, y - math.sin(a) * L_)], (96, 62, 34), 9)
    ex, ey = x + math.cos(a) * L_, y - math.sin(a) * L_
    F.arc((ex + 14, ey), 16, 180, 360, (96, 62, 34), 8)

NOMBRES = [("101", "ANNA"), ("103", "DAVID"), ("106", "LUCAS"), ("109", "MARIA"), ("111", "SOFIA"), ("114", "TOMÁS")]
def placa_draw(F, cx, cy, polvo=1.0, brillo=0.0, wipe=0.0):
    """placa de bronce de la entrada con los niños de 1986"""
    F.rect(cx - 380, cy - 480, cx + 380, cy + 480, fill=(150, 112, 50), outline=(90, 64, 26), w=12)
    F.rect(cx - 350, cy - 450, cx + 350, cy + 450, outline=(200, 160, 80), w=4)
    for dx in (-330, 330):
        for dy in (-430, 430): F.circle((cx + dx, cy + dy), 10, fill=(100, 74, 30))
    F.text((cx, cy - 370), tr("SANTA BRÍGIDA"), 54, (60, 40, 14))
    F.text((cx, cy - 290), "1986", 64, (60, 40, 14))
    F.line([(cx - 300, cy - 240), (cx + 300, cy - 240)], (90, 64, 26), 5)
    for k, (hab, nom) in enumerate(NOMBRES):
        y = cy - 170 + k * 110
        ult = hab == "114"
        col = (60, 40, 14)
        if ult and brillo > 0: col = tuple(int(lerp(a, b, brillo)) for a, b in zip(col, YEL))
        F.text((cx - 200, y), tr("HAB.") + " " + hab, 46, col, stroke=3 * brillo if ult else 0)
        F.text((cx + 140, y), tr(nom) if ult else nom, 56 + (14 * brillo if ult else 0), col, stroke=4 * brillo if ult else 0)
    if polvo > 0:   # capa de polvo y telarañas; el barrido de Nora (wipe) la quita de izquierda a derecha en la última fila
        r = random.Random(4)
        for _ in range(60):
            x = cx + r.uniform(-340, 340); y = cy + r.uniform(-440, 440)
            if y > cy + 300 and x < cx - 340 + 760 * wipe: continue
            F.ellipse((x, y), r.uniform(40, 110), r.uniform(18, 40), fill=(112, 86, 44))
        F.line([(cx + 380, cy - 480), (cx + 200, cy - 300)], (180, 180, 180), 2); F.line([(cx + 380, cy - 380), (cx + 260, cy - 480)], (180, 180, 180), 2)

# ---------- escenas ----------
def dormidos(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("ciudad"), dict(x=540, y=lerp(1000, 1040, zp), z=lerp(1.0, 1.2, zp)))
    calle(F, -300, 1400, seed=3, lamps=(80, 1000))
    for i, x in enumerate((-60, 130, 250, 720, 860, 1060)):
        dormido(F, x, 1240 + (i % 2) * 20, t, i, sc=0.82)
    w = ease(seg(t, 0, D))
    NORA.draw(F, walk(t + 0.3, 0.6), lerp(340, 420, w), 1300, f=1, face="scared")
    LEO.draw(F, walk(t, 0.6), lerp(470, 560, w), 1300, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((490, 1150), 380, 0.6), ((-10, 680), 260, 0.6), ((910, 680), 260, 0.6)], amb=0.35)
    return img, dict(grain=9, flash=((255, 255, 240), 0.4 * (1 - seg(t, 0, 0.3))))

def corren(t, D, fi):
    cx = 500 + t * 620
    F = Frame(base("ciudad"), dict(x=cx, y=1050, z=1.2, sx=noise(t * 25) * 6, sy=noise(t * 25, 1) * 6))
    calle(F, -400, 4500, seed=8)
    for i in range(14):
        dormido(F, -200 + i * 330 + (i % 3) * 40, 1240 + (i % 2) * 18, t, i + 3, sc=0.84)
    LEO.draw(F, run(t, 1.1), cx + 160, 1300, f=1, face="scared")
    NORA.draw(F, run(t + 0.17, 1.1), cx + 10, 1300, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((cx + 90, 1150), 420, 0.6)], amb=0.4)
    return img, dict(grain=9)

def cabezas(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("ciudad"), dict(x=lerp(480, 600, zp), y=1020, z=1.35))
    calle(F, -300, 1500, seed=12, lamps=(30, 1150))
    lx = lerp(160, 820, ease(seg(t, 0, D * 0.9)))
    xs = (60, 230, 420, 620, 800, 980)
    for i, x in enumerate(xs):
        g = ease(seg(t, D * 0.15 + i * 0.12 * D * 0.6, D * 0.3 + i * 0.12 * D * 0.6))
        dormido(F, x, 1250, t, i + 20, mira=lx, giro=g, sc=0.86)
    NORA.draw(F, walk(t + 0.3, 0.5), lx - 120, 1300, f=1, face="scared")
    LEO.draw(F, walk(t, 0.5), lx, 1300, f=1, face="scared")
    k = seg(t, D * 0.3, D)
    img = iluminar(F.finish(), F, [], glows=[((lx - 60, 1150), 360, 0.6), ((540, 1000), 600, 0.35)], amb=0.3)
    return img, dict(grain=10, tint=((255, 0, 30), 0.16 * k), glitch=0.2 if k > 0.7 and fi % 6 == 0 else 0)

def persigue(t, D, fi):
    k = ease(seg(t, 0, D * 0.85))
    sh = 4 + 8 * k
    F = Frame(base("ciudad"), dict(x=540, y=lerp(1060, 1000, k), z=lerp(1.25, 1.05, k), sx=noise(t * 30) * sh, sy=noise(t * 30, 2) * sh))
    calle(F, -300, 1500, seed=21, lamps=(140, 900))
    for i, x in enumerate((20, 1080)):
        dormido(F, x, 1250, t, i + 40, mira=540, giro=1.0, sc=0.84)
    ex = lerp(1150, 760, k)
    enemy(F, add(run(t, 0.7), jitter(t, 3, 4)), ex, 1300, lerp(1.6, 2.4, k), f=-1)
    LEO.draw(F, run(t, 1.2), lerp(480, 380, k), 1300, f=-1, face="scared")
    NORA.draw(F, run(t + 0.17, 1.2), lerp(340, 220, k), 1300, f=-1, face="scared")
    fl = 0.4 + 0.6 * (noise(t * 16, 3) > -0.2)
    img = iluminar(F.finish(), F, [], glows=[((ex, 820), 420, 0.5 * k + 0.25), ((300, 1150), 300, 0.5 * fl)], amb=0.25 * fl + 0.05, warm=(220, 160, 255))
    return img, dict(grain=12, tint=((255, 0, 30), 0.2 * k), glitch=0.35 if k > 0.6 and fi % 4 == 0 else 0)

def placa(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("ciudad"), dict(x=lerp(540, 580, zp), y=lerp(1000, 1020, zp), z=lerp(1.0, 1.25, zp)))
    F.circle((860, 380), 70, fill=(220, 224, 236)); F.circle((890, 360), 64, fill=(8, 11, 30))
    F.rect(-400, 1300, 1500, 2600, fill=(8, 10, 16))
    F.rect(60, 560, 1020, 1300, fill=(36, 40, 54), outline=(20, 22, 30), w=6)
    F.poly([(20, 570), (1060, 570), (540, 380)], fill=(26, 28, 40))
    F.rect(525, 250, 555, 360, fill=(150, 40, 46)); F.rect(490, 285, 590, 315, fill=(150, 40, 46))
    for c_ in range(6):
        x = 110 + c_ * 150
        F.rect(x, 640, x + 80, 740, fill=(14, 16, 24))
    F.rect(200, 900, 380, 1300, fill=(4, 4, 8))
    F.rect(140, 820, 440, 880, fill=(200, 196, 180), outline=(60, 56, 50), w=4)
    F.text((290, 850), tr("SANTA BRÍGIDA"), 30, (60, 30, 30))
    F.rect(600, 880, 840, 1160, fill=(150, 112, 50), outline=(90, 64, 26), w=6)     # placa en la pared
    for k in range(6): F.line([(630, 940 + k * 34), (810, 940 + k * 34)], (90, 64, 26), 5)
    w = ease(seg(t, 0, D * 0.6))
    NORA.draw(F, walk(t, 0.6) if w < 1 else pose(a1u=95, a1l=10), lerp(250, 540, w), 1300, f=1, face="scared")
    LEO.draw(F, walk(t + 0.3, 0.6) if w < 1 else LIN_LEO, lerp(110, 420, w), 1300, f=1, face="scared")
    dormido(F, 960, 1300, t, 50, mira=500, giro=1.0, sc=0.86)
    img = iluminar(F.finish(), F, [], glows=[((720, 1020), 300, 0.8), ((420, 1150), 300, 0.5)], amb=0.3)
    return img, dict(grain=9)
LIN_LEO = pose(a1u=40, a1l=20)

def tomas(t, D, fi):
    g = ease(seg(t, D * 0.45, D * 0.75))
    wipe = ease(seg(t, D * 0.05, D * 0.45))
    F = Frame(gradient((26, 22, 16), (8, 7, 5)), dict(x=540, y=lerp(900, 1100, g), z=lerp(1.0, 1.32, g)))
    placa_draw(F, 540, 900, polvo=1.0, brillo=g, wipe=wipe)
    hx = lerp(150, 920, wipe); hy = 1340 + 20 * math.sin(t * 14)
    if wipe < 1:   # mano de Nora quitando el polvo
        F.line([(hx - 260, 1800), (hx - 20, hy + 40)], (160, 90, 255), 50); F.circle((hx, hy), 44, fill=(240, 240, 240))
    img = iluminar(F.finish(), F, [], glows=[((540, 900), 560, 0.9), ((680, 1250), 260 * g + 1, 1.0 * g)], amb=0.15, warm=(255, 230, 120))
    return img, dict(grain=9, flash=((255, 230, 120), 0.35 * math.exp(-abs(t - D * 0.62) * 9)))

def coche(t, D, fi):
    w = ease(seg(t, 0, D * 0.8))
    F = Frame(base("ciudad"), dict(x=lerp(400, 560, w), y=1040, z=1.2, sx=noise(t * 20) * 4))
    calle(F, -400, 1600, seed=30, lamps=(720,))
    coche_draw(F, 690, 1300, puerta=1.0)
    for i, x in enumerate((-120, 1180)): dormido(F, x, 1250, t, i + 60, mira=600, giro=1.0, sc=0.84)
    LEO.draw(F, run(t, 1.0) if w < 1 else SCARED, lerp(-40, 440, w), 1300, f=1, face="scared")
    NORA.draw(F, run(t + 0.2, 1.0) if w < 1 else SCARED, lerp(-180, 300, w), 1300, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((630, 900), 380, 0.7), ((360, 1150), 320, 0.4)], amb=0.3)
    return img, dict(grain=10)

def vacio(t, D, fi):
    zp = ease(seg(t, 0, D * 0.7))
    F = Frame(base("ciudad"), dict(x=lerp(640, 660, zp), y=lerp(1100, 1130, zp), z=lerp(1.5, 2.1, zp)))
    calle(F, -400, 1600, seed=30, lamps=(720,))
    s = ease(seg(t, D * 0.45, D * 0.75))
    coche_draw(F, 720, 1300, puerta=1.0, sonrisa=s)
    baston(F, 460, 1296, 4)
    k = seg(t, D * 0.5, D)
    img = iluminar(F.finish(), F, [], glows=[((560, 1230), 260, 0.9), ((820, 1064), 160 + 80 * s, 0.9 * s)], amb=0.2)
    return img, dict(grain=11, tint=((255, 0, 30), 0.14 * k), glitch=0.3 if s > 0.8 and fi % 4 == 0 else 0,
                     flash=((255, 30, 40), 0.25 * math.exp(-abs(t - D * 0.6) * 9)))

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    return F.finish(), {}

ESCENA_FN = dict(dormidos=dormidos, corren=corren, cabezas=cabezas, persigue=persigue, placa=placa, tomas=tomas, coche=coche, vacio=vacio, final=final)
PAUSA = dict(dormidos=0.3, corren=0.2, cabezas=0.3, persigue=0.5, placa=0.2, tomas=0.5, coche=0.2, vacio=0.8, final=1.2)
