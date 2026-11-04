"""Escenas del episodio 11 (El amanecer, final de temporada 1): Tomás descansa y se va hacia la luz, la ciudad despierta,
la verdadera Carmen aparece en la galería del faro y, en otra ciudad, algo nuevo sonríe en la ventana de una niña."""
import math, random
from motor import *
from escenas import base, cuarto
from escenas2 import big
from escenas3 import LILA
from escenas6 import NINA, coletas
from escenas7 import NINO
from escenas8 import DORMIDOS, calle
from escenas10 import _sala_luz, chispas, cara_triste

PISO = 1450

# ---------- piezas nuevas ----------
def galeria_faro(F, t):
    """galería exterior en lo alto del faro, al amanecer: mar, sol, barandilla y pared de la torre"""
    F.circle((760, lerp(1180, 1060, ease(t / 4))), 150, fill=(255, 238, 180))
    F.rect(-400, 1200, 1500, 1460, fill=(50, 70, 112))                       # mar
    for k in range(7): F.line([(-400 + k * 300 + (t * 40) % 300, 1230 + k * 30), (-250 + k * 300 + (t * 40) % 300, 1230 + k * 30)], (255, 214, 160), 5)
    F.rect(-400, 300, 200, PISO, fill=(232, 228, 222))                       # torre
    for y in (420, 760, 1100): F.rect(-400, y, 200, y + 160, fill=(200, 50, 50))
    F.rect(-400, PISO, 1500, 2600, fill=(40, 40, 50))                        # suelo de la galería
    F.line([(-400, PISO), (1500, PISO)], (70, 72, 86), 8)
    F.line([(200, 1250), (1500, 1250)], (30, 30, 40), 12, round_=False)      # barandilla
    for x in range(240, 1500, 110): F.line([(x, 1250), (x, PISO)], (30, 30, 40), 8, round_=False)

def sonrisa_nueva(F, c, a=1.0, t=0.0):
    """la criatura nueva de la temporada 2: cara pálida verdosa, ojos huecos y una sonrisa finísima más ancha que la cara"""
    if a <= 0: return
    from escenas import GLASS
    pale = tuple(int(lerp(g, v, a)) for g, v in zip(GLASS, (206, 232, 210)))
    ink = tuple(int(lerp(g, v, a)) for g, v in zip(GLASS, (8, 10, 8)))
    cx, cy = c[0] + noise(t * 3, 4) * 6, c[1]
    F.ellipse((cx, cy), 92, 118, fill=pale)
    for dx in (-36, 36):
        F.ellipse((cx + dx, cy - 26), 20, 30, fill=ink)
        F.circle((cx + dx, cy - 22), 5, fill=tuple(int(lerp(g, v, a)) for g, v in zip(GLASS, (120, 255, 140))))
    F.arc((cx, cy - 50), 104, 22, 158, ink, 22)                             # sonrisa de oreja a oreja
    for i in range(-7, 8):
        an = math.radians(90 - i * 9); x, y = cx + math.cos(an) * 104, cy - 50 + math.sin(an) * 104
        F.line([(x, y - 9), (x, y + 9)], pale, 4, round_=False)
    for s_ in (-1, 1):                                                       # dedos larguísimos en el cristal
        for k in range(4):
            x0 = cx + s_ * (120 + k * 16)
            F.line([(x0, 880), (x0 + s_ * 6, 880 - lerp(0, 150 + 20 * (k % 2), a))], pale, 6)

def _marco_ventana(F):
    F.rect(372, 492, 708, 888, outline=(60, 70, 108), w=16)
    F.line([(540, 500), (540, 880)], (60, 70, 108), 10); F.line([(380, 690), (700, 690)], (60, 70, 108), 10)

def _nina_cama(F, t, miedo=0.0):
    p = pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=lerp(40, 150, miedo), a1l=lerp(30, 40, miedo), a2u=lerp(-20, 140, miedo), a2l=lerp(0, 45, miedo),
             body=lerp(0, -10, miedo), head=lerp(0, -8, miedo))
    J = NINA.draw(F, add(p, jitter(t, 3 * miedo, 2)), 250, 1150, f=1, snap=False, face="scared" if miedo > 0.2 else "neutral")
    coletas(F, J, 0.8)

# ---------- escenas ----------
def descansa(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("oscuro"), dict(x=lerp(520, 500, zp), y=lerp(1200, 1230, zp), z=lerp(1.3, 1.55, zp)))
    _sala_luz(F, t * 0.4, 0.5)
    J = big(NINO, 0.9, F, add(pose(head=8, a1u=8, a1l=10, a2u=-8, a2l=10), jitter(t, 1.5, 3)), 420, PISO, f=1, face="sad")
    cara_triste(F, J, 0.9, f=1, lagrimas=1.0 - seg(t, D * 0.75, D), t=t)
    hab = seg(t, D * 0.5, D)
    NORA.draw(F, pose(body=lerp(5, 22, hab), head=10, a1u=lerp(30, 80, hab), a1l=lerp(40, 10, hab), a2u=-10, a2l=20, l1u=-10, l2u=24, l2l=-30),
              560, PISO, f=-1, face="talk" if hab > 0.05 else "neutral", t=t)
    LEO.draw(F, pose(a1u=20, a1l=30, head=6), 720, PISO, f=-1, face="neutral")
    return F.finish(), dict(grain=7, tint=((255, 220, 160), 0.08))

def hacia_luz(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("oscuro"), dict(x=lerp(520, 540, zp), y=lerp(1180, 1150, zp), z=lerp(1.3, 1.15, zp)))
    k = lerp(0.5, 1.0, ease(seg(t, 0, D * 0.6)))
    _sala_luz(F, t * 0.5, k)
    w = ease(seg(t, D * 0.15, D * 0.7))
    if w < 0.95:
        sc = lerp(0.9, 0.5, w)
        J = big(NINO, sc, F, walk(t, 0.5) if 0 < w else pose(head=4), lerp(420, 540, w), lerp(PISO, 1190, w), f=1, face="happy")
    v = seg(t, D * 0.6, D * 0.85)
    if v > 0: chispas(F, 540, 1200, t, fi, n=int(36 * (1 - v)) + 4, r_=120 + 200 * v, h=300 + 500 * v, col=(255, 250, 225))
    NORA.draw(F, pose(a1u=30, a1l=40, head=-4), 640, PISO, f=-1, face="happy" if t > D * 0.3 else "neutral")
    LEO.draw(F, pose(a1u=20, a1l=30, head=-4), 780, PISO, f=-1, face="neutral")
    return F.finish(), dict(grain=6, flash=((255, 255, 245), 0.8 * math.exp(-abs(t - D * 0.68) * 6)))

def despiertan(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("amanecer"), dict(x=540, y=lerp(1020, 1000, zp), z=lerp(1.15, 1.02, zp)))
    F.circle((540, lerp(1120, 860, zp)), 170, fill=(255, 240, 190))
    calle(F, -300, 1400, seed=5, lamps=())
    for i, x in enumerate((-40, 120, 280, 440, 620, 790, 960, 1110)):
        k = ease(seg(t, D * (0.2 + 0.07 * i), D * (0.3 + 0.07 * i)))
        fig = DORMIDOS[i % len(DORMIDOS)]
        r = random.Random(i * 13); f = 1 if r.random() < 0.5 else -1
        p = pose(body=lerp(4, 0, k) + 3 * math.sin(t * 1.3 + i) * (1 - k), head=lerp(18, -6, k), a1u=6, a1l=4, a2u=-6, a2l=4)
        big(fig, 0.82 * r.uniform(0.92, 1.08), F, p, x, 1240 + (i % 2) * 20, f=f, face="closed" if k < 0.5 else ("happy" if i % 3 == 0 else "neutral"))
    return F.finish(), dict(grain=4, flash=((255, 240, 200), 0.5 * (1 - seg(t, 0, 0.4))))

def galeria(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("amanecer"), dict(x=lerp(620, 640, zp), y=lerp(1180, 1220, zp), z=lerp(1.2, 1.35, zp)))
    galeria_faro(F, t)
    resp = 0.5 + 0.5 * math.sin(t * 3)
    CARMEN.draw(F, pose(a1u=10, a1l=10, a2u=-10, a2l=10, l1u=4, l2u=-4, body=resp * 2), 600, PISO - 22, f=1, rot=-90, snap=False, face="closed")
    w = ease(seg(t, D * 0.25, D * 0.75))
    NORA.draw(F, run(t, 1.1) if 0 < w < 1 else (SCARED if w >= 1 else STAND), lerp(1050, 760, w), PISO, f=-1, face="scared")
    LEO.draw(F, run(t + 0.2, 1.1) if 0 < w < 1 else (SCARED if w >= 1 else STAND), lerp(1200, 890, w), PISO, f=-1, face="scared")
    return F.finish(), dict(grain=5)

def carmen_vive(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("amanecer"), dict(x=lerp(560, 540, zp), y=lerp(1220, 1240, zp), z=lerp(1.4, 1.6, zp)))
    galeria_faro(F, t + 4)
    up = ease(seg(t, 0, D * 0.3))
    pc = pose(head=-6, a1u=lerp(10, 80, up), a1l=20, a2u=lerp(-10, -70, up), a2l=-20)
    if up < 0.98:   # se incorpora: gira desde tumbada (cadera en el suelo) hasta de pie
        CARMEN.draw(F, pc, 560, lerp(PISO - 22, PISO - 118, up), f=1, rot=lerp(-90, 0, up), snap=False, face="closed" if up < 0.4 else "happy")
    else:
        CARMEN.draw(F, pc, 560, PISO, f=1, face="happy")
    h = ease(seg(t, D * 0.25, D * 0.5))
    NORA.draw(F, pose(body=8 * h, a1u=lerp(20, 85, h), a1l=lerp(20, 30, h), a2u=lerp(-20, 70, h), a2l=30), lerp(470, 490, h), PISO, f=1, face="happy")
    LEO.draw(F, pose(body=8 * h, a1u=lerp(20, 85, h), a1l=lerp(20, 30, h), a2u=lerp(-20, 70, h), a2l=30), lerp(690, 640, h), PISO, f=-1, face="happy")
    return F.finish(), dict(grain=4, tint=((255, 210, 150), 0.06))

def otra_ciudad(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("cuarto"), dict(x=lerp(480, 500, zp), y=lerp(920, 880, zp), z=lerp(1.1, 1.25, zp)))
    cuarto(F, t=t)
    _nina_cama(F, t, miedo=0.0)
    return F.finish(), dict(grain=8, tint=((120, 255, 150), 0.03))

def giro(t, D, fi):
    zz = ease_out(seg(t, D * 0.55, D * 0.75))
    F = Frame(base("cuarto"), dict(x=lerp(500, 540, zz), y=lerp(880, 760, zz), z=lerp(1.25, 1.9, zz),
                                   sx=noise(t * 40) * 8 * zz, sy=noise(t * 40, 2) * 8 * zz))
    cuarto(F, t=t)
    a = ease(seg(t, D * 0.15, D * 0.6))
    sonrisa_nueva(F, (540, 720), a, t)
    _marco_ventana(F)
    _nina_cama(F, t, miedo=ease(seg(t, D * 0.4, D * 0.6)))
    return F.finish(), dict(grain=9, glitch=0.4 * zz if fi % 3 == 0 else 0.0, flash=((120, 255, 150), 0.3 * math.exp(-abs(t - D * 0.6) * 8)),
                            tint=((120, 255, 150), 0.12 * a))

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    return F.finish(), {}

ESCENA_FN = dict(descansa=descansa, hacia_luz=hacia_luz, despiertan=despiertan, galeria=galeria, carmen_vive=carmen_vive,
                 otra_ciudad=otra_ciudad, giro=giro, final=final)
PAUSA = dict(descansa=0.5, hacia_luz=0.7, despiertan=0.6, galeria=0.5, carmen_vive=0.6, otra_ciudad=0.5, giro=1.1, final=1.6)
