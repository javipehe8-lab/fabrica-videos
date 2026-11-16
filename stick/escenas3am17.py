"""Si oyes esto a las 3AM — 17: "Las escaleras de más". La escalera de casa vista de lado (13 escalones de madera y,
abajo, un "escalón" más: alguien tumbado boca abajo, atravesado al pie de la escalera), los pies en primera persona
bajando a oscuras, el móvil que lo ilumina desde arriba y tu cuarto (cama alta de la historia 5) con la cuenta en la puerta.
Piezas nuevas reutilizables: escalera_mas (escalera de lado con un escalón vivo al final), pov_escalera (mirando
tus pies desde la escalera), tumbado_pov (cuerpo boca abajo visto desde arriba, con vértebras y la cara girada),
numero (contador grande en pantalla)."""
import math
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am, CASA_A, CASA_B
from escenas3am2 import cara_palida, dedos, PIEL
from escenas3am3 import PISO
from escenas3am5 import _cuarto, tu_tumbado, CAMA_X0, CAMA_X1, COLCHON
from escenas3am11 import _bulto

ROJO = (255, 40, 40)
MOVIL = (200, 220, 255)                     # luz del móvil
MADERA, MADERA_C = (58, 46, 38), (100, 80, 64)
PIJAMA = (52, 62, 98)
CALCETIN = (210, 210, 220)
PELO = (12, 12, 16)
_BG = {}
def fondo(k="a"):
    if k not in _BG: _BG[k] = gradient(CASA_A, CASA_B) if k == "a" else gradient((10, 10, 14), (2, 2, 4))
    return _BG[k]
def _osc(c, k): return tuple(int(v * k) for v in c)

# ---------- la escalera de lado ----------
PA, PB, X0, X1, N = 560, 1240, -200, 760, 15
RX, RY = 90, 300                                     # reloj en la pared de la escalera          # 13 escalones de madera + el "escalón" 14 (vivo) + el suelo
DX, DY = (X1 - X0) / N, (PB - PA) / N
def peldano(k):
    """centro del peldaño k (0 = rellano de arriba; 14 = la cosa)"""
    return (X0 + (k + 0.5) * DX, PA + k * DY)

def escalera_mas(F, t, vivo=1.0, alza=0.0, reloj=True):
    """vivo: el escalón 14 es un cuerpo (respira); alza: levanta la cabeza y estira un brazo escaleras arriba"""
    F.rect(-900, -200, 2000, 3000, fill=(22, 23, 34))
    F.rect(-900, PA - 520, X0 + DX, PA, fill=(28, 29, 42))                        # pared del rellano
    if reloj:
        F.rect(RX - 70, RY + 36, RX + 70, RY + 46, fill=(60, 46, 38))
        reloj_3am(F, RX, RY, 0.26)
    F.rect(X0 + 14 * DX, PB, 2000, 3000, fill=(14, 14, 20)); F.line([(X0 + 14 * DX, PB), (2000, PB)], (44, 44, 60), 6)
    F.rect(X1 + 260, PB - 600, X1 + 520, PB, fill=(8, 8, 12))                     # puerta de la cocina, a oscuras
    pts = [(X0, PA)]
    for k in range(14):
        x = X0 + (k + 1) * DX
        pts += [(x, PA + k * DY), (x, PA + (k + 1) * DY)] if k < 13 else [(x, PA + k * DY), (x, PB)]
    F.poly(pts + [(X0 + 14 * DX, PB + 40), (X0, PA + 40)], fill=MADERA)
    F.line(pts, MADERA_C, 6, round_=False)
    F.line([(X0, PA - 140), (X0 + 13.6 * DX, PA + 13.6 * DY - 140)], (90, 70, 56), 10)          # barandilla
    for k in range(0, 14, 2):
        bx, by = X0 + k * DX, PA + k * DY
        F.line([(bx, by - 140), (bx, by)], (80, 64, 50), 6)
    # el escalón 14: un cuerpo atravesado, de perfil solo se ve el lomo (de la altura de un escalón)
    cx, top = X0 + 14.5 * DX, PA + 14 * DY
    resp = 4 * math.sin(t * 2.4) * vivo
    col = PIEL if vivo else MADERA
    F.d.chord([*F.P(cx - DX * 0.62, top - 10 - resp), *F.P(cx + DX * 0.62, PB + DY)], 180, 360, fill=_osc(col, 0.55))
    F.rect(cx - DX * 0.62, top + DY * 0.5, cx + DX * 0.62, PB, fill=_osc(col, 0.45))
    if alza > 0:                                                                   # se incorpora y sube un brazo
        hx, hy = cx - 6, lerp(top + 10, top - 150, ease(alza))
        F.line([(cx, top + 10), (hx, hy + 40)], PIEL, 30)
        tip = peldano(lerp(14, 11, ease(seg(alza, 0.3, 1.0))))
        F.line([(cx - 20, top + 6), (cx - 40, top - 40 * alza), (tip[0], tip[1] - 6)], PIEL, 18)
        dedos(F, (tip[0], tip[1] - 6), 200, n=4, L_=46, w=6)
        cara_palida(F, (hx, hy), 40, abre=0.5 + 0.4 * alza)
    return (cx, top)

def tu_escalera(F, t, k, sube=False, face="scared"):
    x, y = peldano(k)
    p = run(t, 1.3) if sube else walk(t, 0.55, 0.55)
    return TU.draw(F, p, x, y, f=-1 if sube else 1, face=face)

# ---------- POV: mirando tus pies, escalera abajo ----------
# bandas (y en pantalla) de cada cosa, con la cámara en z=1
P12 = (1460, 2200)        # el peldaño donde estás
P13 = (1180, 1440)        # el siguiente
P14 = (900, 1160)         # el "escalón" 14: el lomo de la cosa
def pov_escalera(F, t, resp=0.0, cara=0.0, aplasta=0.0, luz_suelo=0.25):
    """peldaños vistos desde arriba en primera persona; abajo del todo, la cosa atravesada boca abajo"""
    F.rect(-900, -400, 2000, 3200, fill=_osc((40, 40, 54), luz_suelo))           # suelo del pasillo de abajo
    for x in range(-900, 2000, 180): F.line([(x, -400), (x + 60, P14[0])], _osc((54, 54, 70), luz_suelo), 3)
    F.rect(-900, P14[0] - 30, 2000, P14[0], fill=_osc((30, 30, 40), luz_suelo))
    # la cosa, boca abajo, atravesada en el escalón 14 (cabeza a la izquierda)
    tumbado_pov(F, t, (560, (P14[0] + P14[1]) / 2), resp=resp, cara=cara, aplasta=aplasta)
    for (y0, y1), sh in ((P13, 1.0), (P12, 1.15)):
        F.rect(-900, y0, 2000, y1, fill=_osc(MADERA, sh))
        F.rect(-900, y0, 2000, y0 + 22, fill=_osc(MADERA_C, sh))                  # canto del peldaño
        for x in range(-880, 2000, 260): F.line([(x, y0 + 40), (x + 30, y1)], _osc(MADERA, 0.8), 3)
    F.rect(-900, P13[0] - 10, -620, P12[1], fill=(30, 26, 22))                   # zócalo izquierdo
    F.line([(1640, P13[0] - 600), (1500, P12[1])], (90, 70, 56), 22)              # barandilla

def tumbado_pov(F, t, c, resp=0.0, cara=0.0, aplasta=0.0, sc=1.0):
    """alguien tumbado boca abajo visto desde arriba: espalda flaca con vértebras, brazos estirados, pelo negro.
    cara: 0 = cabeza boca abajo (solo pelo), 1 = la cabeza girada del todo, mirándote"""
    cx, cy = c
    rb = math.sin(t * 2.4) * 10 * resp
    for dy in (-38, 38):                                                          # piernas, hacia la derecha
        F.line([(cx + 250 * sc, cy + dy * 0.6 * sc), (cx + 760 * sc, cy + dy * sc)], _osc(PIEL, 0.82), 64 * sc)
    for dy in (-1, 1):                                                            # brazos, estirados hacia la izquierda
        sh = (cx - 230 * sc, cy + dy * 70 * sc); el = (cx - 420 * sc, cy + dy * 96 * sc); mn = (cx - 640 * sc, cy + dy * 70 * sc)
        F.line([sh, el, mn], _osc(PIEL, 0.86), 34 * sc)
        dedos(F, mn, 180 + dy * 10, n=4, L_=70 * sc, w=8 * sc)
    hh = (1 + (rb - 26 * aplasta) / 92)                                          # media altura relativa (respira / se aplasta)
    perfil = [(-300, 40), (-290, 78), (-240, 100), (-150, 96), (-40, 82), (90, 66), (180, 74), (250, 86), (300, 70), (320, 30)]
    top = [(cx + px * sc, cy - py * hh * sc) for px, py in perfil]
    bot = [(cx + px * sc, cy + py * hh * sc) for px, py in reversed(perfil)]
    F.poly(top + bot, fill=PIEL)                                                  # espalda (hombros anchos, cintura flaca)
    F.circle((cx - 320 * sc, cy), 34 * sc, fill=_osc(PIEL, 0.9))                  # cuello
    for s_ in (-1, 1):                                                            # omóplatos
        F.ellipse((cx - 160 * sc, cy + s_ * 46 * hh * sc), 62 * sc, 24 * sc, fill=_osc(PIEL, 0.86))
        F.line([(cx - 60 * sc, cy + s_ * 56 * hh * sc), (cx + 80 * sc, cy + s_ * 48 * hh * sc)], _osc(PIEL, 0.82), 4 * sc)
    F.line([(cx - 260 * sc, cy), (cx + 250 * sc, cy)], _osc(PIEL, 0.8), 10 * sc)  # surco de la columna
    for i in range(14):                                                           # vértebras
        x = cx - 240 * sc + i * 36 * sc
        F.ellipse((x, cy), 10 * sc, 13 * sc, fill=_osc(PIEL, 0.82))
        F.ellipse((x - 2 * sc, cy - 3 * sc), 6 * sc, 7 * sc, fill=(212, 212, 208))
    hx, hy = cx - 340 * sc, cy
    if cara < 0.5:
        F.circle((hx, hy), 78 * sc, fill=PELO)
        for i in range(9):                                                        # melena desparramada por el peldaño
            a = math.radians(110 + i * 18)
            F.line([(hx, hy), (hx + math.cos(a) * 150 * sc, hy + math.sin(a) * 120 * sc)], PELO, 14 * sc)
    else:
        for i in range(9):
            a = math.radians(110 + i * 18)
            F.line([(hx, hy), (hx + math.cos(a) * 160 * sc, hy + math.sin(a) * 130 * sc)], PELO, 14 * sc)
        cara_palida(F, (hx, hy - 10 * sc), 78 * sc, abre=0.3 + 0.5 * min(1, cara - 0.5) * 2)

def pies(F, t, izq, der, jit=0.0):
    """tus piernas en primera persona: (x, y) de cada pie en pantalla; salen desde abajo del cuadro"""
    for (fx, fy), s_ in ((izq, -1), (der, 1)):
        j = noise(t * 30, 3 + s_) * jit
        F.line([(fx + s_ * 60, 2300), (fx + j, fy + 60)], PIJAMA, 120)
        F.line([(fx + s_ * 60 - 30, 2300), (fx + j - 30, fy + 60)], _osc(PIJAMA, 0.8), 30)
        F.ellipse((fx + j, fy), 52, 86, fill=CALCETIN)
        F.ellipse((fx + j, fy + 50), 44, 40, fill=_osc(CALCETIN, 0.85))

def numero(img, n, p, col=(255, 255, 255), xy=(540, 300), fs=220):
    """contador grande en pantalla (overlay, nítido)"""
    if p <= 0: return img
    d = ImageDraw.Draw(img)
    d.text(xy, str(n), font=font(fs * p + 1), fill=col, anchor="mm", stroke_width=int(12 * p), stroke_fill=(0, 0, 0))
    return img

# ---------- escenas ----------
def reloj(t, D, fi):
    k = ease(seg(t, 0.0, D * 0.5))
    rx, ry = RX, RY
    F = Frame(fondo(), dict(x=lerp(rx, 260, k), y=lerp(ry, 860, k), z=lerp(3.6, 1.05, k)))
    escalera_mas(F, t, vivo=1.0)
    k1 = seg(t, D * 0.45, D)
    tu_escalera(F, t, lerp(0.6, 2.2, k1), face="neutral" if t < D * 0.75 else "scared")
    img = iluminar(F.finish(), F, [], glows=[((rx, ry), 260, 0.8), (peldano(14), 160, 0.18)], amb=0.24, warm=(255, 120, 120))
    return img, dict(grain=9, flash=(ROJO, 0.35 * (1 - seg(t, 0, 0.25))), dark=0.04)

def trece(t, D, fi):
    u = lerp(2.2, 11.0, seg(t, 0, D * 0.92))
    x, y = peldano(u)
    F = Frame(fondo(), dict(x=lerp(260, 470, seg(t, 0, D)), y=lerp(840, 1010, seg(t, 0, D)), z=1.25))
    escalera_mas(F, t)
    tu_escalera(F, t, u, face="neutral")
    img = iluminar(F.finish(), F, [], glows=[((x, y - 100), 260, 0.4), (peldano(14), 140, 0.15)], amb=0.18, warm=(180, 190, 255))
    n = int(u) + 1
    pp = ease_back(seg(u % 1, 0, 0.35)) if n < 13 else 1.0
    def ov(img):
        numero(img, n, 0.7 + 0.3 * pp, fs=200)
        ImageDraw.Draw(img).text((540, 430), "/ 13", font=font(60), fill=(200, 200, 210), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
        return img
    return img, dict(grain=10, dark=0.04, overlay=ov)

def catorce(t, D, fi):
    """POV: bajas al 13 y el otro pie sigue bajando, a oscuras… hasta algo"""
    T14 = 2.87
    F = Frame(fondo("b"), dict(x=540, y=lerp(1400, 1250, ease(seg(t, 0, D))), z=lerp(1.0, 1.12, ease(seg(t, 0, D)))))
    pov_escalera(F, t, resp=0.0, luz_suelo=0.12)
    a = ease(seg(t, 0.2, 1.0)); b = ease(seg(t, 1.6, T14))
    izq = (lerp(420, 440, a), lerp(1720, 1330, a))                                 # al 13
    der = (lerp(660, 620, b), lerp(1760, 1040, b))                                 # sigue bajando… al 14
    pies(F, t, izq, der, jit=3 * seg(t, T14, D))
    img = iluminar(F.finish(), F, [], glows=[((540, 1500), 520, 0.5), ((620, 1040), 260, 0.18 * seg(t, T14, D))], amb=0.08, warm=(170, 180, 230))
    n = 12 if t < 1.0 else 13
    def ov(img):
        if t < T14: return numero(img, n, 0.8 + 0.2 * ease_back(seg(t % 1.0 if t > 1 else t, 0, 0.3)), fs=200)
        return numero(img, 14, ease_back(seg(t, T14, T14 + 0.25)) * (1 + 0.04 * math.sin(t * 30)), col=ROJO, fs=300)
    hit = t > T14
    return img, dict(grain=12, tint=((255, 0, 30), 0.18 * hit), overlay=ov, dark=0.03,
                     flash=(ROJO, 0.35 * max(0, 1 - (t - T14) / 0.25)) if hit else None)

def blando(t, D, fi):
    """el pie sobre el escalón 14: se hunde. Está caliente"""
    k = ease(seg(t, 0, D))
    hunde = ease(seg(t, 0.2, 1.2))
    F = Frame(fondo("b"), dict(x=lerp(600, 580, k), y=lerp(1120, 1080, k), z=lerp(1.6, 2.0, k)))
    pov_escalera(F, t, aplasta=hunde * 0.6, luz_suelo=0.15)
    pies(F, t, (440, 1330), (620, 1040 + 18 * hunde), jit=2)
    img = iluminar(F.finish(), F, [], glows=[((600, 1040), 300, 0.3), ((540, 1400), 360, 0.3)], amb=0.07, warm=(255, 150, 120))
    return img, dict(grain=12, tint=((255, 60, 20), 0.1 * seg(t, 1.7, D)), dark=0.03)

def respira(t, D, fi):
    """el lomo sube y baja bajo tu pie; los dedos se mueven al borde"""
    k = ease(seg(t, 0, D))
    sube = math.sin(max(0, t - 1.6) * 2.4) * seg(t, 1.6, 2.0)
    F = Frame(fondo("b"), dict(x=lerp(560, 460, k), y=lerp(1080, 1060, k), z=lerp(2.0, 1.55, k)))
    pov_escalera(F, t, resp=seg(t, 1.6, 2.0), aplasta=0.6 - 0.3 * sube, luz_suelo=0.15)
    pies(F, t, (440, 1330), (620, 1058 - 14 * sube), jit=4 * seg(t, 1.6, 2.0))
    img = iluminar(F.finish(), F, [], glows=[((600, 1040), 320, 0.32 + 0.06 * sube), ((540, 1400), 360, 0.25)], amb=0.07, warm=(255, 150, 120))
    return img, dict(grain=12, tint=((255, 0, 30), 0.14 * seg(t, 1.8, D)), dark=0.03)

def movil(t, D, fi):
    """enciendes la linterna del móvil: alguien tumbado boca abajo… y gira la cabeza hacia ti"""
    on = seg(t, 0.35, 0.45)
    gira = seg(t, 2.6, 3.0)
    k = ease(seg(t, 0.4, D))
    F = Frame(fondo("b"), dict(x=lerp(560, 330, ease(seg(t, 2.4, 3.2))), y=lerp(1180, 1060, k), z=lerp(1.05, 1.25, ease(seg(t, 2.4, 3.2)))))
    pov_escalera(F, t, resp=1.0, cara=0.5 + 0.5 * gira if gira > 0 else 0.0, aplasta=0.0, luz_suelo=0.3)
    pies(F, t, (440, 1330), (620, 1058), jit=5)
    mx, my = 700, 1500                                                             # tu mano con el móvil
    F.rect(mx - 50, my - 90, mx + 50, my + 90, fill=(18, 18, 22)); F.rect(mx - 42, my - 80, mx + 42, my + 80, fill=_osc(MOVIL, 0.25 + 0.7 * on))
    F.line([(mx + 30, my + 90), (mx + 160, 2200)], PIJAMA, 90)
    haces = [((mx, my - 90), -math.pi / 2 - 0.25, 1100, 1.1)] if on > 0 else []
    img = iluminar(F.finish(), F, haces, glows=[((mx, my), 260, 0.5 * on), ((220, 1030), 260, 0.5 * gira)], amb=0.05, warm=MOVIL)
    hit = gira >= 1
    return img, dict(grain=11, tint=((255, 0, 30), 0.22 * hit), glitch=0.35 if hit and t < 3.6 and fi % 3 else 0.0,
                     flash=((255, 255, 255), 0.8 * max(0, 1 - (t - 3.0) / 0.25)) if hit else None)

def subes(t, D, fi):
    corte = D * 0.55
    if t < corte:
        u = lerp(13, 4, ease_out(seg(t, 0, corte)))
        F = Frame(fondo(), dict(x=380, y=900, z=1.1))
        escalera_mas(F, t, alza=seg(t, 0.2, corte))
        tu_escalera(F, t, u, sube=True)
        img = iluminar(F.finish(), F, [], glows=[(peldano(u), 220, 0.35), (peldano(13.5), 260, 0.35)], amb=0.18, warm=MOVIL)
        return img, dict(grain=11, tint=((255, 0, 30), 0.15))
    tt = t - corte
    tapa = ease(seg(tt, 0, 0.4))
    F = Frame(fondo(), dict(x=lerp(500, 460, tapa), y=PISO - 260, z=1.4))
    _cuarto(F, t)
    if tapa < 1: tu_tumbado(F, t, face="scared", cuelga=0.0, jit=2)
    if tapa > 0: _bulto(F, t, tiembla=1.5)
    img = iluminar(F.finish(), F, [], glows=[((825, PISO - 222), 220, 0.6), ((420, COLCHON - 40), 300, 0.3)], amb=0.2, warm=(255, 120, 120))
    return img, dict(grain=11, flash=((0, 0, 0), 0.6 * (1 - seg(tt, 0, 0.15))))

CUENTA = (2.51, 3.54, 4.63)                         # "Once", "Doce", "Trece" (+0.12 de retardo de voz)
def cuenta(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(640, 900, k), y=lerp(PISO - 330, PISO - 300, k), z=lerp(1.0, 1.5, k)))
    _cuarto(F, t)
    _bulto(F, t, tiembla=1.2 + sum(seg(t, c, c + 0.1) for c in CUENTA))
    n = sum(t >= c for c in CUENTA)
    if n >= 3:
        F.line([(1010, PISO - 336), (950, PISO - 330)], PIEL, 14); dedos(F, (948, PISO - 330), 175, n=4, L_=60, w=7)                     # dedos en el marco de la puerta
    img = iluminar(F.finish(), F, [], glows=[((825, PISO - 222), 200, 0.6), ((1060, PISO - 300), 300, 0.15 * n)], amb=0.18, warm=(255, 120, 120))
    def ov(img):
        for i in range(n):
            p = ease_back(seg(t, CUENTA[i], CUENTA[i] + 0.25))
            numero(img, (11, 12, 13)[i], p, col=ROJO, xy=(300 + i * 240, 330), fs=190)
        return img
    pulso = max([max(0, 1 - (t - c) / 0.2) for c in CUENTA if t >= c] + [0])
    return img, dict(grain=11, overlay=ov, tint=((255, 0, 30), 0.1 + 0.12 * pulso), dark=0.04)

def final(t, D, fi):
    """silencio… y junto a tu cama, la cara asoma a la altura de la manta: catorce"""
    T14, TR = 2.62, 4.1
    k = ease(seg(t, 0, T14))
    asoma = ease(seg(t, T14 - 0.3, T14 + 0.1))
    F = Frame(fondo(), dict(x=lerp(560, 650, k), y=lerp(PISO - 250, PISO - 230, k), z=lerp(1.4, 1.75, k)))
    _cuarto(F, t)
    _bulto(F, t, tiembla=0.3 + 1.5 * asoma)
    # la cosa, tumbada en el suelo junto a la cama (otra vez un escalón), y la cabeza que se levanta
    F.d.chord([*F.P(240, PISO - 60), *F.P(860, PISO + 60)], 180, 360, fill=_osc(PIEL, 0.6))
    for i in range(8):
        F.ellipse((300 + i * 60, PISO - 52), 8, 6, fill=_osc(PIEL, 0.8))                 # vértebras
    hx, hy = 760, lerp(PISO - 40, COLCHON - 50, asoma)
    if asoma > 0:
        F.line([(800, PISO - 30), (hx + 10, hy + 60)], PIEL, 40)
        dedos(F, (CAMA_X1 - 10, COLCHON - 4), 200, n=4, L_=70, w=8)
        cara_palida(F, (hx, hy), 70, abre=0.4 + 0.4 * asoma)
    img = iluminar(F.finish(), F, [], glows=[((825, PISO - 222), 220, 0.7), ((hx, hy), 260, 0.5 * asoma)], amb=0.18, warm=(255, 120, 120))
    pp = ease_back(seg(t, TR, TR + 0.3)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d_ = ImageDraw.Draw(img)
        d_.rounded_rectangle((40, 1150, 1040, 1600), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 HAY UN"), 1210, 62, (255, 255, 255)), (tr("ESCALÓN DE MÁS…"), 1290, 62, (255, 255, 255)),
                                 (tr("NO LO"), 1400, 104, ROJO), (tr("PISES"), 1510, 104, ROJO)):
            fs = fs0
            while fs > 24 and d_.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d_.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d_.rounded_rectangle((230, 1640, 850, 1730), 26, fill=(230, 30, 50))
        d_.text((540, 1685), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    hit = t > T14
    return img, dict(grain=10, tint=((255, 0, 30), 0.2 * pp if pp > 0 else (0.18 if hit else 0.0)),
                     glitch=0.3 if (pp > 0 and fi % 5 == 0) or (hit and t < T14 + 0.4 and fi % 3) else 0.0,
                     flash=((255, 255, 255), 0.7 * max(0, 1 - (t - T14) / 0.25)) if hit else None, overlay=regla)

ESCENA_FN = dict(reloj=reloj, trece=trece, catorce=catorce, blando=blando, respira=respira, movil=movil, subes=subes, cuenta=cuenta, final=final)
PAUSA = dict(reloj=0.4, trece=0.4, catorce=0.6, blando=0.5, respira=0.6, movil=0.7, subes=0.4, cuenta=0.6, final=2.4)
