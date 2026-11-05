"""Escenas del episodio 12 (temporada 2, "Devuélvele la sonrisa"): la criatura nueva de la ventana (el Asomado),
la ciudad de las ventanas tapadas, Lucía, los dedos en el cristal, las muecas y la cama vacía."""
import math, random
from motor import *
from escenas import base, cuarto, GLASS
from escenas6 import NINA, coletas
from escenas8 import calle

PISO = 1250            # suelo del cuarto
VC = (540, 700)        # centro de la ventana del cuarto

# ---------- piezas nuevas ----------
def asomado(F, c, a=1.0, t=0.0, mueca=0.0, cara=1.0, dedos=1.0, base_y=880):
    """la criatura nueva (el Asomado): cara pálida verdosa, ojos huecos con pupila verde, sonrisa de oreja a oreja
    y dedos larguísimos apoyados en el cristal. mueca 0-1: la cara se estira, se ladea y los ojos cambian de tamaño."""
    def col(v, k): return tuple(int(lerp(g, x, k)) for g, x in zip(GLASS, v))
    pale, ink, green = col((206, 232, 210), a), col((8, 10, 8), a), col((120, 255, 140), a)
    for s_ in (-1, 1):                                                       # dos manos de dedos larguísimos pegadas al cristal
        k_ = max(a, dedos)
        if dedos <= 0.01: continue
        px, py = c[0] + s_ * 150, base_y - 10 - 40 * dedos                    # palma (asoma desde abajo)
        skin = col((206, 232, 210), k_); tip = col((236, 248, 238), k_)
        F.ellipse((px, py), 26, 32, fill=skin)
        for k in range(4):
            ang = math.radians(-s_ * (8 + k * 14) + 3 * math.sin(t * 5 + k))  # dedos en abanico
            ln = lerp(30, 150 + 25 * (k in (1, 2)), dedos)
            mx, my = px + math.sin(ang) * ln * 0.55, py - 20 - math.cos(ang) * ln * 0.55
            ex, ey = px + math.sin(ang * 1.25) * ln, py - 20 - math.cos(ang * 1.25) * ln
            F.line([(px + s_ * (k - 1.5) * 9, py - 20), (mx, my), (ex, ey)], skin, 8)
            F.circle((mx, my), 6, fill=skin); F.circle((ex, ey), 7, fill=tip)
    if cara <= 0 or a <= 0: return
    pale = col((206, 232, 210), a * cara); ink = col((8, 10, 8), a * cara); green = col((120, 255, 140), a * cara)
    m = mueca
    lad = 14 * m * math.sin(t * 7)                                           # ladea la cabeza
    cx, cy = c[0] + noise(t * 3, 4) * 6 + lad, c[1]
    ry = 118 * (1 + 0.22 * m * (0.5 + 0.5 * math.sin(t * 9)))
    F.ellipse((cx, cy), 92 * (1 - 0.1 * m), ry, fill=pale)
    for i, dx in enumerate((-36, 36)):
        s = 1 + 0.6 * m * math.sin(t * 8 + i * 2.5)
        F.ellipse((cx + dx, cy - 26), 20 * s, 30 * s, fill=ink)
        F.circle((cx + dx + 4 * m * math.sin(t * 11), cy - 22), 5 * s, fill=green)
    r = 104 * (1 + 0.15 * m)
    F.arc((cx, cy - 50), r, 22 - 12 * m, 158 + 12 * m, ink, 22 + 10 * m)   # sonrisa que se estira
    for i in range(-7, 8):
        an = math.radians(90 - i * 9); x, y = cx + math.cos(an) * r, cy - 50 + math.sin(an) * r
        F.line([(x, y - 9), (x, y + 9)], pale, 4, round_=False)

def ventana_abierta(F, sonrisa_vaho=1.0):
    """la ventana del cuarto abierta de par en par: hojas giradas hacia dentro y una sonrisa dibujada con los dedos en el vaho"""
    F.rect(380, 500, 700, 880, fill=(16, 24, 46))
    F.circle((620, 580), 34, fill=(220, 226, 236))
    F.rect(372, 492, 708, 888, outline=(60, 70, 108), w=16)
    for s_ in (-1, 1):                                                       # hojas abiertas (en perspectiva)
        x0 = 540 + s_ * 160; x1 = x0 + s_ * 110
        F.poly([(x0, 500), (x1, 470), (x1, 910), (x0, 880)], fill=(40, 56, 88), outline=(60, 70, 108), w=8)
    if sonrisa_vaho > 0:                                                     # sonrisa de dedos en el vaho de la hoja derecha
        k = sonrisa_vaho; c = tuple(int(lerp(40, 225, k)) for _ in range(3))
        F.arc((755, 640), 34, 20, 160, c, 6)
        F.circle((742, 640), 4, fill=c); F.circle((768, 640), 4, fill=c)
        for i in range(4): F.circle((738 + i * 10, 712 + (i % 2) * 6), 3, fill=c)

def edificios_tapados(F, x0, x1, piso, seed=0, k=1.0):
    """edificios con todas las ventanas tapadas con papel de periódico y cinta en X"""
    r = random.Random(seed); x = x0
    while x < x1:
        w = r.randint(150, 260); h = r.randint(500, 1000); top = piso - h
        F.rect(x, top, x + w - 10, piso, fill=(18, 20, 34))
        for wy in range(int(top) + 30, piso - 60, 62):
            for wx in range(x + 18, x + w - 34, 44):
                g = int(lerp(26, r.randint(120, 160), k))
                F.rect(wx, wy, wx + 22, wy + 32, fill=(g, g - 6, g - 20))
                if k > 0.5:
                    F.line([(wx + 2, wy + 2), (wx + 20, wy + 30)], (90, 82, 64), 2, round_=False)
                    F.line([(wx + 20, wy + 2), (wx + 2, wy + 30)], (90, 82, 64), 2, round_=False)
        x += w

def lucia_cama(F, t, miedo=0.0, x=250, ojeras=1.0, cerrados=False):
    """Lucía sentada en la cama de la izquierda (NINA con coletas castañas)"""
    p = pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=lerp(40, 150, miedo), a1l=lerp(30, 40, miedo), a2u=lerp(-20, 140, miedo), a2l=lerp(0, 45, miedo),
             body=lerp(0, -10, miedo), head=lerp(0, -8, miedo))
    face = "closed" if cerrados else ("scared" if miedo > 0.2 else "neutral")
    J = NINA.draw(F, add(p, jitter(t, 3 * miedo, 2)), x, 1150, f=1, snap=False, face=face)
    coletas(F, J, 0.8)
    return J

# ---------- escenas ----------
def asomado_sc(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("cuarto"), dict(x=540, y=lerp(760, 720, zp), z=lerp(1.75, 2.05, zp), sx=noise(t * 30) * 3, sy=noise(t * 30, 3) * 3))
    cuarto(F, t=t)
    asomado(F, VC, 1.0, t, mueca=0.15 * math.sin(t * 2) ** 2, dedos=1.0)
    F.rect(372, 492, 708, 888, outline=(60, 70, 108), w=16)
    F.line([(540, 500), (540, 880)], (60, 70, 108), 10); F.line([(380, 690), (700, 690)], (60, 70, 108), 10)
    return F.finish(), dict(grain=9, tint=((120, 255, 150), 0.12), flash=((120, 255, 150), 0.35 * (1 - seg(t, 0, 0.35))))

def llegada(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("calle"), dict(x=lerp(460, 560, zp), y=lerp(1000, 1030, zp), z=lerp(1.05, 1.2, zp)))
    F.circle((860, 380), 70, fill=(220, 224, 236))
    edificios_tapados(F, -500, 1600, 1180, seed=12, k=1.0)
    F.rect(-700, 1180, 1800, 1300, fill=(34, 36, 46)); F.rect(-700, 1300, 1800, 2700, fill=(18, 19, 26))
    F.line([(-700, 1300), (1800, 1300)], (54, 56, 70), 6)
    w = ease(seg(t, 0, D * 0.85)); stop = w >= 1
    CARMEN.draw(F, pose(head=-10, a1u=20) if stop else walk(t, 0.7), lerp(-20, 330, w), 1300, f=1, face="neutral")
    NORA.draw(F, pose(head=-14, a1u=20, a1l=20) if stop else walk(t + 0.3, 0.9), lerp(120, 470, w), 1300, f=1, face="scared" if t > D * 0.5 else "neutral")
    LEO.draw(F, pose(head=-14, a1u=88, a1l=0) if stop else walk(t + 0.6, 0.9), lerp(260, 610, w), 1300, f=1, face="scared" if t > D * 0.5 else "neutral")
    return F.finish(), dict(grain=7, tint=((120, 255, 150), 0.03))

def lucia(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("cuarto"), dict(x=lerp(460, 440, zp), y=lerp(1000, 1030, zp), z=lerp(1.15, 1.35, zp)))
    cuarto(F, t=t)
    for x0 in (380, 540): F.rect(x0 + 6, 506, x0 + 154, 682, fill=(150, 142, 118))       # ventana tapada con periódicos
    for x0 in (380, 540): F.rect(x0 + 6, 698, x0 + 154, 874, fill=(140, 132, 108))
    F.line([(380, 500), (700, 880)], (90, 82, 64), 6); F.line([(700, 500), (380, 880)], (90, 82, 64), 6)
    lucia_cama(F, t, miedo=0.25 + 0.1 * math.sin(t * 3))
    CARMEN.draw(F, pose(head=6, a1u=30, a1l=30), 480, PISO, f=-1, face="neutral")
    NORA.draw(F, pose(head=8, a1u=60, a1l=30), 600, PISO, f=-1, face="neutral")
    LEO.draw(F, pose(head=6, a1u=14), 715, PISO, f=-1, face="neutral")
    return F.finish(), dict(grain=7)

def dedos(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("cuarto"), dict(x=lerp(500, 540, zp), y=lerp(980, 820, zp), z=lerp(1.15, 1.5, zp)))
    cuarto(F, t=t)
    asomado(F, VC, 0.0, t, dedos=ease(seg(t, D * 0.15, D * 0.8)))
    F.rect(372, 492, 708, 888, outline=(60, 70, 108), w=16)
    F.line([(540, 500), (540, 880)], (60, 70, 108), 10); F.line([(380, 690), (700, 690)], (60, 70, 108), 10)
    lucia_cama(F, t, miedo=ease(seg(t, D * 0.4, D * 0.7)))
    NORA.draw(F, SCARED if t > D * 0.6 else pose(head=-12), 720, PISO, f=-1, face="scared")
    LEO.draw(F, pose(head=-14, a1u=60, a1l=40), 860, PISO, f=-1, face="scared")
    return F.finish(), dict(grain=8, tint=((120, 255, 150), 0.05))

def muecas(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("cuarto"), dict(x=lerp(520, 500, zp), y=lerp(990, 1010, zp), z=lerp(1.45, 1.35, zp),
                                   sx=noise(t * 40) * 6, sy=noise(t * 40, 2) * 6))
    cuarto(F, t=t)
    asomado(F, VC, 1.0, t, mueca=0.4 + 0.6 * ease(seg(t, 0, D * 0.5)), dedos=1.0)
    F.rect(372, 492, 708, 888, outline=(60, 70, 108), w=16)
    F.line([(540, 500), (540, 880)], (60, 70, 108), 10); F.line([(380, 690), (700, 690)], (60, 70, 108), 10)
    lucia_cama(F, t, miedo=0.8)
    g = seg(t, D * 0.45, D * 0.6)
    NORA.draw(F, add(pose(body=lerp(0, 14, g), head=4, a1u=lerp(30, 100, g), a1l=lerp(30, 10, g), a2u=lerp(-30, -100, g), a2l=-10, l1u=-14, l2u=20),
                     jitter(t, 2, 5)), 520, PISO, f=-1, face="talk" if g > 0 else "scared", t=t)
    return F.finish(), dict(grain=10, glitch=0.35 if fi % 4 == 0 else 0.0, tint=((120, 255, 150), 0.14),
                            flash=((120, 255, 150), 0.25 * math.exp(-abs(t - D * 0.5) * 8)))

def aguanta(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("cuarto"), dict(x=lerp(380, 360, zp), y=lerp(1020, 1060, zp), z=lerp(1.3, 1.55, zp)))
    cuarto(F, t=t)
    a = 1 - ease(seg(t, D * 0.2, D * 0.7))                                    # la cosa se va apagando en el cristal
    asomado(F, VC, a, t, mueca=0.3, dedos=a)
    F.rect(372, 492, 708, 888, outline=(60, 70, 108), w=16)
    F.line([(540, 500), (540, 880)], (60, 70, 108), 10); F.line([(380, 690), (700, 690)], (60, 70, 108), 10)
    dorm = t > D * 0.7
    lucia_cama(F, t, miedo=lerp(0.5, 0.0, seg(t, 0, D * 0.7)), cerrados=dorm)
    NORA.draw(F, pose(body=8, head=12, a1u=40, a1l=60, l1u=70, l1l=-80, l2u=60, l2l=-70), 560, PISO - 70, f=-1, face="closed" if dorm else "neutral")
    return F.finish(), dict(grain=7, dark=0.25 * seg(t, D * 0.6, D))

def giro(t, D, fi):
    pan = ease(seg(t, D * 0.35, D * 0.75))
    zz = ease_out(seg(t, D * 0.6, D * 0.8))
    F = Frame(base("alba"), dict(x=lerp(260, 620, pan), y=lerp(1080, 720, pan), z=lerp(1.4, 1.9, pan),
                                 sx=noise(t * 40) * 7 * zz, sy=noise(t * 40, 2) * 7 * zz))
    cuarto(F, t=t)
    ventana_abierta(F, sonrisa_vaho=ease(seg(t, D * 0.55, D * 0.8)))
    F.rect(90, 1112, 300, 1136, fill=(205, 210, 230))                         # sábana revuelta, cama vacía
    F.poly([(160, 1132), (330, 1110), (430, 1150), (200, 1158)], fill=(170, 178, 210))
    return F.finish(), dict(grain=8, tint=((255, 220, 200), 0.05), glitch=0.3 * zz if fi % 3 == 0 else 0.0,
                            flash=((120, 255, 150), 0.3 * math.exp(-abs(t - D * 0.65) * 8)))

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    return F.finish(), {}

ESCENA_FN = dict(asomado=asomado_sc, llegada=llegada, lucia=lucia, dedos=dedos, muecas=muecas, aguanta=aguanta, giro=giro, final=final)
PAUSA = dict(asomado=0.5, llegada=0.4, lucia=0.4, dedos=0.5, muecas=0.5, aguanta=0.4, giro=0.9, final=1.4)
