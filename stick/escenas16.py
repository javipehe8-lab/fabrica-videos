"""Escenas del episodio 16 (temporada 2, "El primer cristal"): el cristalero, arrepentido, les abre y confiesa que el Asomado
nació en un espejo de feria; van al parque de atracciones cerrado, entran en la casa de la risa (espejos deformes cuyos
reflejos sonríen), Carmen y Lucía encuentran el primer espejo… y en él hay dibujada la cara de Nora."""
import math, random
from functools import lru_cache
from motor import *
from escenas import base, GLASS
from escenas6 import NINA, coletas
from escenas13 import panel, huella, asomado_en, PISO, VERDE
from escenas15 import cristalero, taller_int, ventana_nueva, sabana, iluminar_, GOLD_

ROJO_F = (170, 40, 50)
BOMBILLA = (255, 214, 120)

@lru_cache(None)
def fondo(kind):
    if kind == "feria": return gradient((10, 8, 22), (34, 22, 44))
    if kind == "risa": return gradient((22, 10, 26), (12, 8, 16))
    return base(kind)

def refl(fig, sc=0.8):
    """copia de una figura para dibujarla dentro de un espejo"""
    return Fig(shirt=fig.shirt, limb=fig.limb, scale=fig.scale * sc, kind=fig.kind, extra=tuple(fig.extra))

# ---------- piezas nuevas ----------
def noria(F, cx, cy, R, t, gira=0.0, luces=0.5):
    """noria parada: aro, radios, cabinas colgando y bombillas que parpadean"""
    F.line([(cx, cy), (cx - R * 0.55, cy + R * 1.35)], (50, 44, 60), 14); F.line([(cx, cy), (cx + R * 0.55, cy + R * 1.35)], (50, 44, 60), 14)
    F.circle((cx, cy), R, outline=(70, 62, 84), w=10); F.circle((cx, cy), R * 0.82, outline=(56, 50, 70), w=5)
    a0 = gira
    for i in range(10):
        a = a0 + i * math.pi / 5
        px, py = cx + R * math.cos(a), cy + R * math.sin(a)
        F.line([(cx, cy), (px, py)], (56, 50, 70), 5)
        on = luces > 0 and (int(t * 6 + i * 3) % 4 != 0)
        F.circle((px, py), 9, fill=BOMBILLA if on else (70, 60, 50))
        F.line([(px, py), (px, py + 40)], (60, 54, 70), 4)
        F.rect(px - 30, py + 40, px + 30, py + 90, fill=(60, 30, 44), outline=(90, 60, 70), w=3)
    F.circle((cx, cy), 22, fill=(80, 70, 96))

def arco_feria(F, x, piso, t, cadena=1.0, luces=0.6):
    """entrada del parque: dos postes, arco con bombillas, rótulo, verja con cadena y cartel de CERRADO"""
    for px in (x, x + 760):
        F.rect(px - 22, piso - 760, px + 22, piso, fill=(60, 34, 46))
    F.arc((x + 380, piso - 640), 400, 200, 340, ROJO_F, 40)
    for i in range(13):
        a = math.radians(200 + i * 140 / 12)
        on = luces > 0 and (int(t * 7 + i * 5) % 5 != 0)
        F.circle((x + 380 + 400 * math.cos(a), piso - 640 + 400 * math.sin(a)), 11, fill=BOMBILLA if on else (80, 64, 50))
    F.rect(x + 160, piso - 920, x + 600, piso - 820, fill=(36, 18, 30), outline=(200, 160, 90), w=6)
    F.text((x + 380, piso - 870), tr("FERIA"), 64, (230, 190, 110))
    for i in range(12):                                                         # verja
        gx = x + 30 + i * 62
        F.line([(gx, piso - 420), (gx, piso)], (70, 66, 80), 8)
    F.line([(x, piso - 420), (x + 760, piso - 420)], (70, 66, 80), 10); F.line([(x, piso - 200), (x + 760, piso - 200)], (70, 66, 80), 8)
    if cadena > 0:
        for i in range(9):
            F.ellipse((x + 300 + i * 20, piso - 300 + 18 * math.sin(i / 8 * math.pi)), 12, 8, outline=(150, 146, 140), w=4)
        F.rect(x + 360, piso - 290, x + 400, piso - 250, fill=(120, 110, 90))
        F.rect(x + 470, piso - 380, x + 690, piso - 300, fill=(200, 190, 160), outline=(90, 30, 30), w=4)
        F.text((x + 580, piso - 340), tr("CERRADO"), 38, (150, 30, 30))

def casa_risa_ext(F, x, piso, t):
    """fachada de la casa de la risa: cara sonriente pintada y puerta en la boca"""
    F.rect(x, piso - 640, x + 600, piso, fill=(70, 30, 60), outline=(40, 16, 34), w=8)
    F.poly([(x - 30, piso - 640), (x + 630, piso - 640), (x + 300, piso - 820)], fill=(90, 40, 74))
    F.text((x + 300, piso - 700), tr("CASA DE LA RISA"), 40, (240, 200, 120))
    F.circle((x + 210, piso - 520), 46, fill=(240, 236, 220)); F.circle((x + 390, piso - 520), 46, fill=(240, 236, 220))
    F.circle((x + 210, piso - 520), 18, fill=(20, 10, 16)); F.circle((x + 390, piso - 520), 18, fill=(20, 10, 16))
    F.poly([(x + 110, piso - 400), (x + 490, piso - 400), (x + 300, piso - 120)], fill=(20, 8, 14), outline=(220, 70, 80), w=10)
    for i in range(7): F.rect(x + 140 + i * 48, piso - 400, x + 176 + i * 48, piso - 360, fill=(236, 230, 210))

def espejo(F, x, y0, w, h, brillo=0.4, luz=0.0, bombillas=1.0, t=0.0):
    """espejo de feria: cristal plateado, marco rojo y dorado con bombillas"""
    col = tuple(int(lerp(a, b, luz)) for a, b in zip((52, 60, 84), (40, 100, 74)))
    F.rect(x, y0, x + w, y0 + h, fill=col)
    sh = tuple(int(lerp(a, 220, 0.2 + 0.3 * brillo)) for a in col)
    F.poly([(x + w * 0.1, y0 + h * 0.04), (x + w * 0.3, y0 + h * 0.04), (x + w * 0.1, y0 + h * 0.5), (x + w * 0.03, y0 + h * 0.5)], fill=sh)

def marco_espejo(F, x, y0, w, h, bombillas=1.0, t=0.0, seed=0):
    F.rect(x - 14, y0 - 14, x + w + 14, y0 + h + 14, outline=ROJO_F, w=22)
    F.rect(x - 24, y0 - 24, x + w + 24, y0 + h + 24, outline=GOLD_, w=6)
    n = max(3, int(h / 90))
    for i in range(n + 1):
        on = bombillas > 0 and (int(t * 5 + i * 7 + seed) % 6 != 0)
        for bx in (x - 14, x + w + 14):
            F.circle((bx, y0 + h * i / n), 8, fill=BOMBILLA if on else (80, 64, 50))

def reflejo(F, fig, x, y0, w, h, p, stretch=1.0, sc=0.8, face="neutral", t=0.0, nina=False):
    """la figura reflejada (deformada) dentro de un espejo"""
    J = refl(fig, sc).draw(F, p, x + w / 2, y0 + h - 18, f=-1, face=face, t=t, stretch=stretch)
    if nina: coletas(F, J, 0.8 * sc)
    return J

def cara_nora(F, c, k, s=1.0, t=0.0):
    """la cara de Nora dibujada con el dedo en el cristal (coleta, ojos, sonrisa), trazo a trazo"""
    cx, cy = c; col = (200, 255, 214)
    def trazo(pts, a, b, w=9):
        q = seg(k, a, b)
        if q <= 0: return
        n = max(2, int(len(pts) * q))
        F.line(pts[:n], col, w * s)
    circ = [(cx + 120 * s * math.cos(a), cy + 140 * s * math.sin(a)) for a in [i * 2 * math.pi / 36 - math.pi / 2 for i in range(37)]]
    trazo(circ, 0.0, 0.35)
    trazo([(cx + 100 * s, cy - 100 * s), (cx + 170 * s, cy - 120 * s), (cx + 210 * s, cy - 60 * s), (cx + 200 * s, cy + 20 * s)], 0.3, 0.5, 12)  # coleta
    if k > 0.5: F.circle((cx - 45 * s, cy - 25 * s), 14 * s * ease(seg(k, 0.5, 0.6)), fill=col)
    if k > 0.58: F.circle((cx + 45 * s, cy - 25 * s), 14 * s * ease(seg(k, 0.58, 0.68)), fill=col)
    smile = [(cx + 80 * s * math.cos(a), cy + 20 * s + 60 * s * math.sin(a)) for a in [math.radians(10 + i * 160 / 16) for i in range(17)]]
    trazo(smile, 0.68, 0.95, 10)

# ---------- escenas ----------
def fabricado(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(540, 520, zp), y=lerp(980, 960, zp), z=lerp(1.05, 1.3, zp), sx=noise(t * 25) * 3, sy=noise(t * 25, 1) * 3))
    taller_int(F, t, lampara=0.3)
    caras = []
    for i in range(4):
        x = -180 + i * 280; y0 = 560 + (i % 2) * 50
        ventana_nueva(F, x, y0, 220, 560 - (i % 2) * 50, brillo=0.3, luz=0.6)
        asomado_en(F, (x + 110, y0 + 240), 0.85, t + i, mueca=0.3 + 0.2 * math.sin(t * 3 + i))
        caras.append(((x + 110, y0 + 240), 230, 0.7))
    rod = pose(body=10, head=24, a1u=120, a1l=60, a2u=110, a2l=60, l1u=90, l1l=-90, l2u=10, l2l=-90)
    cristalero(F, rod, 540, PISO, f=1, face="scared", t=t)
    img = iluminar_(F, caras)
    return img, dict(grain=9, tint=(VERDE, 0.1), flash=(VERDE, 0.4 * (1 - seg(t, 0, 0.35))))

def confesion(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(560, 600, zp), y=lerp(950, 930, zp), z=lerp(1.05, 1.25, zp)))
    taller_int(F, t, lampara=0.8)
    op = ease(seg(t, D * 0.05, D * 0.35))                                       # la puerta se abre: luz de la calle
    F.rect(860, 760, 1060, PISO, fill=tuple(int(lerp(20, v, op)) for v in (70, 80, 110)))
    ow = 200 * (1 - 0.85 * op)
    F.rect(860, 760, 860 + ow, PISO, fill=(70, 46, 30), outline=(40, 26, 18), w=6)
    hab = seg(t, D * 0.4, D * 0.95)
    cristalero(F, pose(head=-4, a1u=lerp(40, 100, op) + 10 * math.sin(t * 6) * (hab > 0), a1l=30, a2u=-10), 760, PISO, f=-1,
               face="talk" if hab > 0 and int(t * 8) % 2 else "neutral", t=t)
    LEO.draw(F, pose(head=-10, a1u=30, a1l=-30), 230, PISO, f=1, face="angry")
    NORA.draw(F, pose(head=-12), 360, PISO, f=1, face="neutral")
    Jl = NINA.draw(F, pose(head=-14, a1u=20), 470, PISO, f=1, face="neutral"); coletas(F, Jl, 0.8)
    CARMEN.draw(F, pose(head=-6, a1u=40, a1l=20), 580, PISO, f=1, face="neutral")
    return F.finish(), dict(grain=7, tint=((255, 190, 110), 0.05))

def feria(t, D, fi):
    pan = ease(t / D)
    F = Frame(fondo("feria"), dict(x=lerp(420, 640, pan), y=lerp(900, 930, pan), z=lerp(0.95, 1.08, pan)))
    F.circle((180, 300), 60, fill=(220, 224, 236))
    noria(F, 820, 520, 330, t, gira=0.12 * math.sin(t * 0.8), luces=1.0)
    F.rect(-800, PISO, 2000, 2700, fill=(20, 16, 24)); F.line([(-800, PISO), (2000, PISO)], (60, 50, 66), 6)
    arco_feria(F, 40, PISO, t)
    w = ease(seg(t, 0, D * 0.85))
    for fig, dx, ph in ((CARMEN, -120, 0), (NORA, 40, 0.3), (LEO, 170, 0.6)):
        fig.draw(F, walk(t + ph, 1.0, 1.4), lerp(-400, 240, w) + dx, PISO, f=1, face="scared")
    Jl = NINA.draw(F, walk(t + 0.45, 1.0, 1.4), lerp(-400, 240, w) - 20, PISO, f=1, face="scared"); coletas(F, Jl, 0.8)
    return F.finish(), dict(grain=8, tint=((180, 120, 255), 0.05))

FIGS = ((LEO, False), (NORA, False), (NINA, True), (CARMEN, False))
def casa_risa(t, D, fi):
    pan = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(300, 800, pan), y=930, z=1.1))
    F.rect(-800, PISO, 2000, 2700, fill=(30, 14, 30))
    for i in range(-8, 16): F.rect(i * 120, PISO, i * 120 + 60, PISO + 900, fill=(44, 20, 40))     # suelo de cuadros
    F.line([(-800, PISO), (2000, PISO)], (90, 40, 74), 6)
    ST = (1.6, 0.6, 1.35, 0.7, 1.5, 0.65)
    for i in range(6):
        x = -260 + i * 260; y0 = 520; w, h = 200, PISO - 40 - y0
        espejo(F, x, y0, w, h, brillo=0.4)
        fig, nn = FIGS[i % 4]
        reflejo(F, fig, x, y0, w, h, walk(t + i * 0.3, 0.8, 1.2), stretch=ST[i], sc=0.7 if ST[i] > 1 else 1.0, face="scared", t=t, nina=nn)
        marco_espejo(F, x, y0, w, h, t=t, seed=i)
    w = ease(seg(t, 0, D))
    xs = lerp(100, 980, w)
    for (fig, nn), dx, ph in zip(FIGS, (150, 30, -80, -200), (0.6, 0.3, 0.45, 0)):
        J = fig.draw(F, walk(t + ph, 1.0, 1.4), xs + dx, PISO + 60, f=1, face="scared")
        if nn: coletas(F, J, 0.8)
    return F.finish(), dict(grain=8, tint=((255, 120, 200), 0.04))

def sonrien(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(500, 540, zp), y=lerp(900, 860, zp), z=lerp(1.0, 1.2, zp), sx=noise(t * 30) * 3 * zp, sy=noise(t * 30, 2) * 3 * zp))
    F.rect(-800, PISO, 2000, 2700, fill=(30, 14, 30)); F.line([(-800, PISO), (2000, PISO)], (90, 40, 74), 6)
    sm = seg(t, D * 0.15, D * 0.3) > 0
    fl = seg(t, D * 0.7, D * 0.78) - seg(t, D * 0.92, D * 0.99)
    for i, (fig, nn, st, x, w, sc) in enumerate(((LEO, False, 0.6, -120, 300, 1.25), (NORA, False, 1.45, 300, 340, 1.2))):
        y0 = 420; h = PISO - 40 - y0
        espejo(F, x, y0, w, h, brillo=0.4, luz=0.3 * fl)
        if not (i == 1 and fl > 0.5):
            J = reflejo(F, fig, x, y0, w, h, pose(head=8, a1u=-30, a1l=-20, a2u=30, a2l=20), stretch=st, sc=sc,
                        face="happy" if sm else "scared", t=t, nina=nn)
            if sm:                                                              # sonrisa de oreja a oreja
                hx, hy = J["head"]; r = 33 * fig.scale * sc
                F.arc((hx, hy + r * 0.05), r * 0.66, 10, 170, (20, 10, 16), 6)
        marco_espejo(F, x, y0, w, h, t=t, seed=i)
    asomado_en(F, (470, 760), 0.95 * fl, t, mueca=0.4)
    NORA.draw(F, SCARED, 790, PISO, f=-1, face="scared")
    LEO.draw(F, pose(head=-8, a1u=40, a1l=30), 940, PISO, f=-1, face="scared")
    return F.finish(), dict(grain=9, tint=(VERDE, 0.06 + 0.1 * fl), glitch=0.4 * fl if fi % 3 == 0 else 0.0,
                            flash=((255, 255, 255), 0.4 * math.exp(-abs(t - D * 0.22) * 12)))

EX, EY, EW, EH = 360, 360, 360, 820      # el primer espejo
def primero(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(540, 540, zp), y=lerp(920, 880, zp), z=lerp(1.0, 1.15, zp)))
    F.rect(-800, PISO, 2000, 2700, fill=(24, 10, 24)); F.line([(-800, PISO), (2000, PISO)], (80, 34, 64), 6)
    caida = seg(t, D * 0.2, D * 0.55)
    espejo(F, EX, EY, EW, EH, brillo=0.5, luz=0.5 * ease(caida))
    for i in range(3):
        huella(F, EX + 80 + i * 100, EY + 160 + (i % 2) * 90, ease(seg(t, D * (0.55 + 0.1 * i), D * (0.7 + 0.1 * i))), 1.4)
    marco_espejo(F, EX, EY, EW, EH, bombillas=0.0, t=t)
    for i in range(5): F.line([(EX - 30 + i * 6, EY - 40 - i * 10), (EX + EW + 30 - i * 6, EY - 40 - i * 10)], GOLD_, 4)   # crestería
    sabana(F, EX, EY, EW, EH, caida)
    CARMEN.draw(F, pose(head=-6, a1u=lerp(20, 100, seg(t, D * 0.1, D * 0.25)), a1l=20), 220, PISO, f=1, face="scared" if caida > 0.4 else "neutral")
    Jl = NINA.draw(F, pose(head=-14, a1u=lerp(10, 80, seg(t, D * 0.1, D * 0.3)), a1l=30), 870, PISO, f=-1,
                   face="scared" if caida > 0.4 else "neutral"); coletas(F, Jl, 0.8)
    img = iluminar_(F, [((EX + EW / 2, EY + EH / 2), 480, 0.8 * ease(caida)), ((540, 900), 600, 0.25)])
    return img, dict(grain=8, tint=(VERDE, 0.08), flash=(VERDE, 0.3 * math.exp(-abs(t - D * 0.55) * 10)))

def giro(t, D, fi):
    zz = ease(seg(t, D * 0.35, D))
    F = Frame(fondo("risa"), dict(x=lerp(540, 600, zz), y=lerp(880, 800, zz), z=lerp(1.0, 1.4, zz),
                                  sx=noise(t * 30) * 3 * zz, sy=noise(t * 30, 2) * 3 * zz))
    F.rect(-800, PISO, 2000, 2700, fill=(24, 10, 24)); F.line([(-800, PISO), (2000, PISO)], (80, 34, 64), 6)
    espejo(F, EX, EY, EW, EH, brillo=0.5, luz=0.6)
    cara_nora(F, (EX + EW / 2, EY + 320), seg(t, 0, D * 0.5), 1.0, t)
    marco_espejo(F, EX, EY, EW, EH, bombillas=0.0, t=t)
    for i in range(5): F.line([(EX - 30 + i * 6, EY - 40 - i * 10), (EX + EW + 30 - i * 6, EY - 40 - i * 10)], GOLD_, 4)
    sabana(F, EX, EY, EW, EH, 1.0)
    atras = ease(seg(t, D * 0.55, D * 0.75))
    NORA.draw(F, mix(pose(head=-10), SCARED, atras), lerp(790, 840, atras), PISO, f=-1, face="scared")
    CARMEN.draw(F, pose(head=-6, a1u=60, a1l=30), 180, PISO, f=1, face="scared")
    img = iluminar_(F, [((EX + EW / 2, EY + 320), 420, 0.9), ((540, 900), 600, 0.25)])
    return img, dict(grain=8, tint=(VERDE, 0.1), flash=(VERDE, 0.4 * math.exp(-abs(t - D * 0.55) * 10)),
                     glitch=0.3 if (fi % 5 == 0 and t > D * 0.55) else 0.0)

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    return F.finish(), {}

ESCENA_FN = dict(fabricado=fabricado, confesion=confesion, feria=feria, casa_risa=casa_risa, sonrien=sonrien, primero=primero, giro=giro, final=final)
PAUSA = dict(fabricado=0.5, confesion=0.4, feria=0.4, casa_risa=0.4, sonrien=0.5, primero=0.5, giro=1.3, final=2.0)
