"""Si oyes esto a las 3AM — 16: "El taxi". Interior del taxi desde el asiento de atrás (taxista de espaldas,
retrovisor con sus ojos que no parpadean, taxímetro con el 3:00), el taxi visto de lado cruzando el puente viejo,
las flores en la barandilla rota y la puerta abierta sobre el río, con la luz del taxi hundido en el fondo.
Piezas nuevas reutilizables: taxi_dentro, taxi_lado, puente_lado, ojos_fijos."""
import math, random
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, movil_msg, reloj_3am
from escenas3am2 import Sub, arboles

TAXISTA = Fig(shirt=(44, 50, 58), limb=(196, 200, 196))
PIEL = (196, 200, 194)                       # piel del taxista: gris verdosa, de ahogado
GORRA = (30, 34, 40)
VERDE = (60, 255, 120)                       # luz verde del taxi
NUM = "117"
NOCHE_A, NOCHE_B = (10, 13, 28), (3, 4, 8)
_BG = {}
def fondo(k=0):
    if k not in _BG: _BG[k] = gradient(NOCHE_A, NOCHE_B) if k == 0 else gradient((12, 12, 16), (3, 3, 5))
    return _BG[k]

def gotas(F, x, y, t, n=3, largo=260, seed=0):
    """gotas de agua que caen (de la gorra del taxista)"""
    for i in range(n):
        u = ((t * 1.3 + i / n + seed * 0.37) % 1.0)
        F.ellipse((x + (i - 1) * 22, y + u * largo), 4, 7, fill=(150, 180, 200))

def ojos_fijos(F, cx, cy, r, mira=(0, 0), pupila=0.32):
    """dos ojos muy abiertos, sin párpados que se muevan, con la pupila clavada en ti"""
    for dx in (-1.25, 1.25):
        ex = cx + dx * r
        F.ellipse((ex, cy), r * 0.95, r * 0.62, fill=(236, 236, 228))
        F.circle((ex + mira[0] * r * 0.3, cy + mira[1] * r * 0.2), r * 0.38, fill=(70, 80, 70))
        F.circle((ex + mira[0] * r * 0.3, cy + mira[1] * r * 0.2), r * pupila, fill=(2, 2, 4))
        F.circle((ex + mira[0] * r * 0.3 - r * 0.12, cy - r * 0.14), r * 0.08, fill=(255, 255, 255))
        F.arc((ex, cy + r * 0.05), r * 0.98, 200, 340, (120, 120, 116), r * 0.08)          # párpado de arriba, retirado
        F.arc((ex, cy - r * 0.2), r * 0.9, 25, 155, (120, 110, 110), r * 0.07)             # ojeras rojizas

# ---------- interior del taxi, desde el asiento de atrás ----------
ESP = (380, 330, 700, 440)                    # interior del retrovisor (mundo)
def taxi_dentro(F, t, speed=1.0, puente=0.0, giro=0.0, voz=0.0, gotea=1.0):
    """puente: 0 = carretera con árboles, 1 = puente viejo con farolas; giro: 0 = de espaldas, 1 = cabeza girada hacia ti"""
    F.rect(-600, -300, 1700, 2400, fill=(10, 12, 24))
    F.rect(-600, 820, 1700, 1200, fill=(6, 6, 9))
    if puente < 0.5:
        arboles(F, -600, 1700, 830, seed=9, off=t * speed * 60, col=(4, 5, 9), hmin=60, hmax=150)
    F.poly([(522, 820), (558, 820), (1320, 1200), (-240, 1200)], fill=(24, 24, 30))
    for k in range(7):                                       # línea central
        u = ((k + t * speed * 1.4) % 7) / 7; p0, p1 = u ** 2.2, min(1, (u + 0.05) ** 2.2)
        F.line([(540, lerp(820, 1200, p0)), (540, lerp(820, 1200, p1))], (200, 190, 130), lerp(2, 26, p0), round_=False)
    luces = []
    if puente >= 0.5:                                        # barandillas y farolas del puente
        for s_ in (-1, 1):
            F.line([(540 + s_ * 30, 800), (540 + s_ * 900, 1040)], (60, 60, 70), 8)
            F.line([(540 + s_ * 30, 812), (540 + s_ * 900, 1110)], (44, 44, 52), 5)
            for k in range(4):
                u = ((k + t * speed * 0.9) % 4) / 4; p = u ** 2
                x = 540 + s_ * lerp(40, 1000, p); h = lerp(20, 520, p)
                F.line([(x, lerp(812, 1100, p)), (x, lerp(812, 1100, p) - h)], (30, 30, 36), lerp(2, 18, p))
                F.circle((x, lerp(812, 1100, p) - h), lerp(3, 26, p), fill=(255, 190, 110)); luces.append(((x, lerp(812, 1100, p) - h), lerp(20, 160, p)))
    # carrocería por dentro
    F.rect(-600, -300, 1700, 300, fill=(14, 14, 18))
    F.poly([(-600, 300), (60, 300), (-90, 1200), (-600, 1200)], fill=(12, 12, 16))
    F.poly([(1020, 300), (1700, 300), (1700, 1200), (1170, 1200)], fill=(12, 12, 16))
    F.rect(-600, 980, 1700, 2400, fill=(16, 16, 20)); F.line([(-600, 980), (1700, 980)], (40, 40, 48), 6)
    reloj_3am(F, 540, 1040, 0.36)                            # taxímetro
    F.rect(470, 1090, 610, 1124, fill=(10, 30, 16)); F.text((540, 1107), tr("OCUPADO"), 20, (90, 220, 120))
    # asiento del copiloto, con el número del taxi en el respaldo
    F.rect(700, 820, 860, 960, fill=(26, 26, 30)); F.rect(640, 960, 1000, 1900, fill=(24, 24, 28))
    F.rect(700, 1180, 940, 1290, fill=(232, 226, 200), outline=(60, 60, 60), w=4)
    F.text((820, 1212), tr("TAXI Nº"), 30, (40, 40, 40)); F.text((820, 1258), NUM, 50, (180, 20, 20))
    # el taxista, de espaldas, con gorra; el cuello gira con 'giro'
    hx, hy = 300, 700
    F.rect(150, 920, 450, 1900, fill=(22, 22, 26))                                         # respaldo
    F.poly([(120, 1900), (140, 900), (220, 840), (380, 840), (460, 900), (480, 1900)], fill=TAXISTA.shirt)   # hombros
    F.rect(270, 760, 330, 850, fill=PIEL)                                                  # cuello
    sh = noise(t * 40, 5) * 6 * giro * (1 - giro)
    if giro < 0.5:
        F.circle((hx + sh, hy), 82, fill=(26, 24, 22))                                      # nuca: pelo mojado
        F.ellipse((hx - 80 + sh, hy + 10), 10, 22, fill=PIEL); F.ellipse((hx + 80 + sh, hy + 10), 10, 22, fill=PIEL)  # orejas
    else:
        F.ellipse((hx + sh, hy + 6), 76, 92, fill=PIEL)
        ojos_fijos(F, hx + sh, hy - 4, 30, mira=(0.6, 0.5), pupila=0.22)
        F.ellipse((hx + sh, hy + 58), 16, 8 + 26 * voz, fill=(10, 8, 10))
        F.line([(hx - 40 + sh, hy - 40), (hx - 12 + sh, hy - 34)], (40, 40, 40), 6); F.line([(hx + 12 + sh, hy - 34), (hx + 40 + sh, hy - 40)], (40, 40, 40), 6)
    F.d.chord([*F.P(hx - 92 + sh, hy - 96), *F.P(hx + 92 + sh, hy + 40)], 180, 360, fill=GORRA)   # gorra
    if giro >= 0.5: F.poly([(hx - 96 + sh, hy - 30), (hx + 96 + sh, hy - 30), (hx + 70 + sh, hy - 6), (hx - 70 + sh, hy - 6)], fill=(20, 22, 28))
    if gotea > 0: gotas(F, hx + sh, hy + 60 if giro >= 0.5 else hy + 80, t, n=3, largo=200)
    # retrovisor con sus ojos (siempre abiertos, mirándote)
    F.line([(540, 300), (540, 330)], (30, 30, 34), 18)
    F.rect(ESP[0] - 14, ESP[1] - 14, ESP[2] + 14, ESP[3] + 14, fill=(8, 8, 10), outline=(46, 46, 52), w=8)
    M = Sub(F, *ESP, fill=(14, 14, 20))
    if giro < 0.5:
        M.rect(380, 330, 700, 440, fill=(24, 26, 30))
        M.rect(380, 330, 700, 352, fill=GORRA)
        M.rect(420, 352, 660, 440, fill=PIEL)
        ojos_fijos(M, 540, 392, 30, mira=(0.15, 0.4))
    else:
        M.rect(380, 330, 700, 440, fill=(20, 22, 30))                                       # ya no está en el espejo
    M.pegar()
    return dict(espejo=(540, 385), cabeza=(hx, hy), luces=luces)

# ---------- el puente visto de lado ----------
PISO = 1150
def puente_lado(F, t, off=0.0, roto=None, flores=0.0):
    """tablero del puente en PISO; barandilla de este lado (se dibuja con baranda() DESPUÉS del taxi)"""
    F.circle((860, 360), 62, fill=(214, 218, 230))
    r = random.Random(3); x = -900
    while x < 2400:                                                   # orilla de enfrente, a lo lejos
        h = r.randint(40, 120); F.poly([(x, PISO - 40 - h), (x + 40, PISO - 40), (x - 40, PISO - 40)], fill=(8, 10, 16)); x += r.randint(40, 90)
    F.rect(-900, PISO - 44, 2400, PISO - 36, fill=(12, 14, 20))
    F.rect(-900, PISO + 40, 2400, 3000, fill=(4, 5, 10))                # vacío bajo el puente
    for k in range(9):                                                 # río, muy abajo
        y = 1700 + k * 26
        F.line([(-900, y), (2400, y)], (22 + k * 3, 30 + k * 3, 56 + k * 4), 6)
    F.ellipse((860, 1760), 40, 140, fill=(40, 46, 70))                 # reflejo de la luna
    F.rect(-900, PISO, 2400, PISO + 40, fill=(56, 54, 52)); F.line([(-900, PISO), (2400, PISO)], (90, 88, 84), 6)
    for k in range(-2, 6):                                              # pilares
        px = k * 700 - (off % 700)
        F.rect(px - 30, PISO + 40, px + 30, 1700, fill=(16, 16, 22))
    luces = []
    for k in range(-2, 7):                                              # farolas del otro lado
        lx = k * 520 - (off * 1.0 % 520)
        F.line([(lx, PISO - 30), (lx, PISO - 520)], (30, 30, 36), 12); F.line([(lx, PISO - 520), (lx + 50, PISO - 520)], (30, 30, 36), 10)
        F.circle((lx + 50, PISO - 512), 16, fill=(255, 200, 120)); luces.append((lx + 50, PISO - 512))
    return luces

def baranda(F, off=0.0, roto=None, flores=0.0, t=0.0):
    """barandilla de este lado; roto = (x0, x1) hueco con los barrotes doblados hacia fuera; flores en el extremo izquierdo"""
    col, osc = (70, 70, 76), (36, 36, 40)
    def tramo(a, b):
        F.line([(a, PISO - 110), (b, PISO - 110)], col, 12, round_=False); F.line([(a, PISO - 60), (b, PISO - 60)], osc, 6, round_=False)
        x = a - ((a + off) % 70) + 70
        while x < b: F.line([(x, PISO - 110), (x, PISO)], osc, 6); x += 70
    if roto is None:
        tramo(-900, 2400); return
    x0, x1 = roto
    tramo(-900, x0); tramo(x1, 2400)
    for xb, s_ in ((x0, 1), (x1, -1)):                                 # barrotes rotos, doblados hacia el vacío
        F.line([(xb, PISO - 110), (xb + s_ * 40, PISO - 60), (xb + s_ * 30, PISO + 60)], col, 12)
        F.line([(xb, PISO - 60), (xb + s_ * 20, PISO + 10), (xb + s_ * 50, PISO + 90)], osc, 6)
    if flores > 0:
        fx, fy = x0 - 10, PISO - 100
        F.line([(fx - 20, fy + 10), (fx + 20, fy - 10)], (200, 200, 200), 4)          # cinta
        for i, c in enumerate([(170, 40, 50), (220, 200, 210), (190, 60, 90), (150, 30, 40), (230, 220, 200)]):
            a = math.radians(-120 + i * 28)
            px, py = fx + math.cos(a) * 34, fy + math.sin(a) * 34
            F.line([(fx, fy + 30), (px, py)], (40, 70, 40), 4)
            F.circle((px, py), 13 * flores, fill=c)
        F.poly([(fx - 18, fy + 20), (fx + 18, fy + 20), (fx + 8, fy + 70), (fx - 8, fy + 70)], fill=(200, 196, 180))

def taxi_lado(F, x, piso, t=0.0, puerta=0.0, tu_face="scared", gira=0.0):
    """taxi blanco con franja roja y luz verde en el techo (morro a la izquierda); dentro, el taxista y tú detrás"""
    cab = [(x - 170, piso - 170), (x - 95, piso - 300), (x + 150, piso - 300), (x + 255, piso - 170)]
    F.poly(cab, fill=(12, 14, 20))
    F.rect(x + 160, piso - 255, x + 200, piso - 150, fill=(30, 28, 32))
    TU.draw(F, pose(body=-4, l1u=90, l1l=-90, l2u=86, l2l=-86, a1u=40, a1l=60, a2u=30, a2l=70), x + 110, piso - 72, f=-1, face=tu_face, t=t, snap=False)
    F.rect(x - 8, piso - 245, x + 22, piso - 150, fill=(32, 30, 34))
    J = TAXISTA.draw(F, pose(body=-4, head=-160 * gira, l1u=90, l1l=-90, l2u=86, l2l=-86, a1u=78, a1l=-6, a2u=70, a2l=-2),
                     x - 55, piso - 72, f=-1, face="neutral", t=t, snap=False)
    hx, hy = J["head"]; r = L["head"] * TAXISTA.scale
    F.d.chord([*F.P(hx - r - 3, hy - r - 6), *F.P(hx + r + 3, hy + r - 4)], 180, 360, fill=GORRA)
    F.rect(hx - r - 14, hy - 8, hx, hy - 2, fill=GORRA)
    F.line([(x - 132, piso - 238), (x - 112, piso - 178)], (20, 20, 24), 12)
    blanco, osc = (222, 222, 216), (120, 120, 118)
    F.poly([(x - 315, piso - 170), (x + 300, piso - 170), (x + 300, piso - 50), (x - 315, piso - 50)], fill=blanco, outline=osc, w=6)
    F.line(cab + [cab[0]], (200, 200, 196), 12); F.line([(x + 40, piso - 300), (x + 40, piso - 170)], (200, 200, 196), 14)
    F.poly([(x - 300, piso - 120), (x + 290, piso - 140), (x + 290, piso - 120), (x - 300, piso - 100)], fill=(190, 30, 36))   # franja roja
    F.text((x + 150, piso - 85), NUM, 30, (30, 30, 30))
    F.line([(x + 40, piso - 150), (x + 40, piso - 60)], osc, 4)
    F.rect(x - 318, piso - 150, x - 296, piso - 118, fill=(255, 240, 190)); F.rect(x + 280, piso - 150, x + 302, piso - 118, fill=(220, 30, 30))
    F.rect(x - 10, piso - 330, x + 70, piso - 300, fill=(230, 230, 220), outline=osc, w=3)             # cartel TAXI
    F.text((x + 30, piso - 315), "TAXI", 22, (30, 30, 30)); F.circle((x + 86, piso - 312), 10, fill=VERDE)
    if puerta > 0:                                                                                     # puerta de atrás abierta hacia ti
        F.rect(x + 45, piso - 170, x + 250, piso - 56, fill=(10, 8, 10))
        F.poly([(x + 250, piso - 300), (x + 250 + 150 * puerta, piso - 270), (x + 250 + 150 * puerta, piso - 30), (x + 250, piso - 56)],
               fill=blanco, outline=osc, w=5)
    for wx in (x - 190, x + 175):
        F.circle((wx, piso - 46), 50, fill=(18, 18, 22)); F.circle((wx, piso - 46), 21, fill=(110, 110, 116))
        a = -t * 14; F.line([(wx + math.cos(a) * 20, piso - 46 + math.sin(a) * 20), (wx - math.cos(a) * 20, piso - 46 - math.sin(a) * 20)], (40, 40, 44), 5)
    return dict(techo=(x + 86, piso - 312), cabeza=(hx, hy))

def letrero(F, x, y, txt):
    F.line([(x, y + 60), (x, PISO)], (60, 60, 66), 12)
    F.rect(x - 170, y - 60, x + 170, y + 60, fill=(24, 60, 140), outline=(230, 230, 230), w=6)
    F.text((x, y), txt, 46, (240, 240, 240))

# ---------- escenas ----------
def taxi(t, D, fi):
    k = ease(seg(t, 0.15, D * 0.5))
    F = Frame(fondo(), dict(x=lerp(540, 540, k), y=lerp(1040, 900, k), z=lerp(3.4, 1.0, k), sx=noise(t * 3) * 3))
    c = taxi_dentro(F, t, speed=1.0)
    img = iluminar(F.finish(), F, [], glows=[((540, 1040), 240, 0.8), (c["espejo"], 260, 0.85), ((540, 1000), 420, 0.5), ((300, 760), 260, 0.5)],
                   amb=0.4, warm=(255, 120, 120))
    return img, dict(grain=9, dark=0.2 * (1 - k), tint=((255, 30, 40), 0.22 * (1 - seg(t, 0, D * 0.4))))

def ojos(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=540, y=385, z=lerp(2.2, 3.1, k), sx=noise(t * 20) * 2))
    c = taxi_dentro(F, t, speed=1.0)
    img = iluminar(F.finish(), F, [], glows=[(c["espejo"], 320, 0.95)], amb=0.25, warm=(220, 230, 255))
    d = ImageDraw.Draw(img)
    s = int(lerp(598, 600, seg(t, D * 0.15, D * 0.75)))                     # contador: 9:58 → 10:00 sin parpadear
    if t > D * 0.15:
        d.rounded_rectangle((300, 1180, 780, 1320), 20, fill=(0, 0, 0))
        d.text((540, 1250), "%d:%02d" % (s // 60, s % 60), font=font(90), fill=(255, 50, 50), anchor="mm")
        d.text((540, 1355), tr("SIN PARPADEAR"), font=font(40), fill=(255, 255, 255), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * seg(t, D * 0.6, D)))

def numero(t, D, fi):
    F = Frame(fondo(1), dict(x=540, y=900, z=lerp(1.0, 1.08, ease(t / D))))
    F.rect(-600, -300, 1700, 2400, fill=(8, 8, 12))
    c = movil_msg(F, t, D, tr("LUCÍA"), [tr("VOY EN EL TAXI") + " " + NUM, tr("EL TAXISTA"), tr("NO PARPADEA")])
    img = iluminar(F.finish(), F, [], glows=[(c, 560, 1.0)], amb=0.22, warm=(170, 200, 255))
    return img, dict(grain=8)

def respuesta(t, D, fi):
    F = Frame(fondo(1), dict(x=540, y=900, z=lerp(1.05, 1.2, ease(t / D)), sx=noise(t * 30) * 3 * seg(t, D * 0.5, D)))
    F.rect(-600, -300, 1700, 2400, fill=(8, 8, 12))
    c = movil_msg(F, t, D, tr("LUCÍA"), [tr("¿EL 117?"), tr("SE ESTRELLÓ EN EL"), tr("PUENTE VIEJO."), tr("EN 1998.")])
    img = iluminar(F.finish(), F, [], glows=[(c, 560, 1.0)], amb=0.22, warm=(170, 200, 255))
    golpe = t > D * 0.75
    return img, dict(grain=9, tint=((255, 0, 30), 0.22 * seg(t, D * 0.7, D)), glitch=0.25 if golpe and fi % 4 == 0 else 0.0)

def puente(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(480, 580, k), y=lerp(1180, 1120, k), z=lerp(1.2, 1.35, k), sx=noise(t * 6) * 3))
    off = t * 700
    luces = puente_lado(F, t, off=off)
    letrero(F, lerp(1500, -400, seg(t, D * 0.1, D * 0.9)), PISO - 470, tr("PUENTE VIEJO"))
    c = taxi_lado(F, 560, PISO, t)
    baranda(F, off=off)
    gl = [(p, 160, 0.7) for p in luces] + [(c["techo"], 120, 0.9), ((860, 360), 200, 0.5), ((200, PISO - 120), 300, 0.4)]
    img = iluminar(F.finish(), F, [], glows=gl, amb=0.3, warm=(255, 200, 140))
    return img, dict(grain=10)

def flores(t, D, fi):
    fr = ease_out(seg(t, 0, D * 0.5))
    k = ease(seg(t, D * 0.45, D))
    F = Frame(fondo(), dict(x=lerp(580, 760, k), y=lerp(1120, 1080, k), z=lerp(1.35, 1.8, k)))
    off = 700 * D * 0.25 * fr                                    # se va frenando
    luces = puente_lado(F, t, off=off)
    c = taxi_lado(F, 560, PISO, t * (1 - fr))
    baranda(F, off=0, roto=(700, 880), flores=1.0, t=t)
    gl = [(p, 160, 0.7) for p in luces] + [(c["techo"], 120, 0.9), ((700, PISO - 100), 180, 0.7), ((860, 360), 200, 0.5)]
    img = iluminar(F.finish(), F, [], glows=gl, amb=0.3, warm=(255, 200, 140))
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * k))

def habla(t, D, fi):
    g = ease(seg(t, D * 0.25, D * 0.42))
    hit = g >= 1
    sh = 10 * seg(t, D * 0.42, D * 0.45) * (1 - seg(t, D * 0.45, D * 0.7))
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(420, 320, k), y=lerp(850, 720, k), z=lerp(1.5, 2.6, k), sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    voz = abs(math.sin(t * 13)) if t > D * 0.45 else 0.0
    c = taxi_dentro(F, t, speed=0.0, puente=1.0, giro=g, voz=voz)
    gl = [(p, r_, 0.6) for p, r_ in c["luces"]] + [(c["cabeza"], 260, 0.85), (c["espejo"], 200, 0.4)]
    img = iluminar(F.finish(), F, [], glows=gl, amb=0.2, warm=(200, 255, 210))
    return img, dict(grain=12, flash=((255, 255, 255), max(0, 1 - (t - D * 0.42) / 0.25)) if hit else None,
                     glitch=0.4 if hit and fi % 3 and t < D * 0.6 else 0.0, tint=((255, 0, 30), 0.25 if hit else 0.0))

def _puerta_vista(F, t, abre=1.0, luz=1.0):
    """primera persona: la puerta de atrás abierta sobre el hueco de la barandilla; abajo, el río y el taxi hundido"""
    F.rect(-600, -300, 1700, 2400, fill=(6, 7, 14))
    F.circle((820, 420), 54, fill=(214, 218, 230))
    F.rect(-600, 870, 1700, 1140, fill=(4, 5, 10))                      # el vacío
    for k in range(12):                                                  # río, muy abajo
        y = 1140 + k * 34
        F.line([(-600, y + noise(t * 0.8, k) * 6), (1700, y)], (24 + k * 4, 34 + k * 4, 62 + k * 5), 8)
    w_ = 0.5 + 0.5 * math.sin(t * 2.2)                                   # el taxi del fondo: luz verde ondulando bajo el agua
    tx, ty = 560 + noise(t * 0.6, 3) * 8, 1330
    F.ellipse((tx, ty), 230, 80, fill=(16, 60, 44))
    F.rect(tx - 150, ty - 30, tx + 150, ty + 30, fill=(150, 170, 160), outline=(60, 90, 80), w=4)       # techo blanco del taxi
    F.line([(tx - 150, ty + 10), (tx + 150, ty + 4)], (150, 40, 40), 8)
    F.rect(tx - 44, ty - 64, tx + 44, ty - 32, fill=(180, 200, 190)); F.text((tx, ty - 48), "TAXI", 22, (30, 50, 40))
    F.circle((tx + 62, ty - 50), 14 + 5 * w_, fill=VERDE)
    for dx in (-120, 120): F.circle((tx + dx, ty + 30), 12, fill=(200, 240, 210))
    # borde del puente y barandilla rota a los lados
    F.rect(-600, 820, 1700, 870, fill=(50, 48, 46)); F.line([(-600, 820), (1700, 820)], (90, 88, 84), 6)
    for xb, s_ in ((290, 1), (830, -1)):
        F.line([(xb - s_ * 200, 700), (xb, 700), (xb + s_ * 50, 780), (xb + s_ * 40, 930)], (80, 80, 86), 14)
        F.line([(xb - s_ * 200, 760), (xb + s_ * 20, 770), (xb + s_ * 60, 960)], (44, 44, 50), 8)
    for i, c in enumerate([(170, 40, 50), (220, 200, 210), (190, 60, 90), (150, 30, 40)]):   # las flores, atadas
        a = math.radians(-130 + i * 30); F.circle((250 + math.cos(a) * 30, 690 + math.sin(a) * 30), 12, fill=c)
    # marco de la puerta (interior del taxi) y la puerta abierta
    F.rect(-600, -300, 200, 2400, fill=(12, 12, 16)); F.rect(920, -300, 1700, 2400, fill=(12, 12, 16))
    F.rect(-600, -300, 1700, 300, fill=(12, 12, 16)); F.rect(-600, 1620, 1700, 2400, fill=(14, 14, 18))
    F.rect(200, 1600, 920, 1640, fill=(30, 30, 34))
    dx = lerp(0, 700, ease(abre))
    F.poly([(920, 300), (920 + dx * 0.25, 260), (920 + dx * 0.25, 1680), (920, 1620)], fill=(200, 200, 194), outline=(110, 110, 108), w=5)
    # tus rodillas y tu mano en el asiento
    F.ellipse((330, 1820), 210, 110, fill=(30, 40, 60)); F.ellipse((730, 1840), 210, 110, fill=(28, 38, 58))
    F.line([(-200, 2200), (120, 1720)], TU.shirt, 90); F.circle((150, 1690), 56, fill=(240, 240, 240))
    return (tx, ty)

def puerta(t, D, fi):
    abre = ease_out(seg(t, D * 0.05, D * 0.3))
    k = ease(seg(t, D * 0.35, D))
    F = Frame(fondo(1), dict(x=560, y=lerp(960, 1260, k), z=lerp(1.0, 1.6, k), sx=noise(t * 8) * 3))
    tx = _puerta_vista(F, t, abre=abre)
    luz = 0.55 + 0.45 * math.sin(t * 2.2) ** 2
    img = iluminar(F.finish(), F, [], glows=[(tx, 260, 0.6 + 0.4 * luz * seg(t, D * 0.4, D * 0.6)), ((840, 420), 200, 0.6), ((560, 760), 360, 0.4), ((560, 1300), 420, 0.35)],
                   amb=0.22, warm=(120, 255, 170))
    return img, dict(grain=11, tint=((60, 255, 120), 0.1 * seg(t, D * 0.5, D)))

def final(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=540, y=lerp(400, 390, k), z=lerp(2.3, 2.6, k)))
    c = taxi_dentro(F, t, speed=0.0, puente=1.0)
    img = iluminar(F.finish(), F, [], glows=[(c["espejo"], 320, 0.95)], amb=0.2, warm=(200, 255, 210))
    pp = ease_back(seg(t, D * 0.4, D * 0.5)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d_ = ImageDraw.Draw(img)
        d_.rounded_rectangle((40, 1150, 1040, 1600), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 EL TAXISTA"), 1210, 62, (255, 255, 255)), (tr("NO PARPADEA…"), 1290, 62, (255, 255, 255)),
                                 (tr("NO TE BAJES"), 1400, 104, (255, 40, 50)), (tr("DONDE ÉL PARE"), 1510, 104, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d_.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d_.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d_.rounded_rectangle((230, 1640, 850, 1730), 26, fill=(230, 30, 50))
        d_.text((540, 1685), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.2 * pp if pp > 0 else 0.1), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(taxi=taxi, ojos=ojos, numero=numero, respuesta=respuesta, puente=puente, flores=flores, habla=habla, puerta=puerta, final=final)
PAUSA = dict(taxi=0.5, ojos=0.6, numero=0.4, respuesta=0.7, puente=0.5, flores=0.7, habla=1.0, puerta=1.0, final=2.4)
