"""Si oyes esto a las 3AM — 15: "La radio del abuelo". Cada noche a las tres, la vieja radio del abuelo se enciende sola en
tu mesilla y da el tiempo. Hoy da un aviso: se busca a un hombre en la calle del Olmo, 7 (tu casa; vives solo). Lleva abrigo
gris y sombrero… como el "perchero" del rincón, que está ahí desde el primer plano. Tú no tienes perchero. La radio se calla
y el sombrero gira hacia ti.
Piezas nuevas reutilizables: radio_vieja (radio de válvulas de madera con dial que brilla y altavoz que vibra con la voz),
cuarto_radio (tu cuarto de lado: cama, mesilla con la radio, foto del abuelo, reloj y el rincón), hombre (el hombre del
abrigo gris y sombrero que parece un perchero; gira la cabeza y enseña la cara), sobre (carta con tu dirección)."""
import math
from PIL import ImageDraw
from motor import *
from escenas2 import big
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am
from escenas3am3 import paredes, PISO
from escenas3am5 import _osc

ROJO = (255, 40, 40)
DIAL = (255, 170, 80)            # luz ámbar del dial
MADERA, MADERA_O = (112, 72, 42), (52, 32, 18)
GRIS = (70, 72, 80)              # abrigo gris
PIEL_H = (206, 202, 196)
RX, RY = 670, PISO - 190         # la radio: centro de la base, encima de la mesilla
HX = 945                         # el hombre ("perchero"), en el rincón
HS = 0.8                         # su escala en el cuarto (cabeza en PISO - 600 * HS)
COLCHON = PISO - 172
_BG = {}
def fondo(k="a"):
    if k not in _BG: _BG[k] = gradient((22, 22, 34), (8, 8, 12))
    return _BG[k]

# ---------- piezas ----------
def radio_vieja(F, cx, by, s=1.0, on=1.0, voz=0.0, t=0.0, aguja=0.35, rojo=0.0):
    """radio de madera con la parte de arriba redondeada: altavoz con rejilla a la izquierda y dial ámbar a la derecha.
    on: brillo del dial; voz: cuánto vibra el altavoz; rojo: el dial vira a rojo"""
    w, h = 90 * s, 120 * s
    x0, x1, y0 = cx - w, cx + w, by - h
    F.rect(x0, y0 + 26 * s, x1, by, fill=MADERA, outline=MADERA_O, w=4 * s)
    F.ellipse((cx, y0 + 30 * s), w, 34 * s, fill=MADERA, outline=MADERA_O, w=4 * s)
    F.rect(x0 + 4 * s, y0 + 28 * s, x1 - 4 * s, y0 + 40 * s, fill=MADERA)
    # altavoz: tela oscura con listones que tiemblan con la voz
    gx0, gx1, gy0, gy1 = x0 + 16 * s, cx - 6 * s, y0 + 30 * s, by - 16 * s
    F.rect(gx0, gy0, gx1, gy1, fill=(30, 22, 16), outline=MADERA_O, w=3 * s)
    vib = voz * (0.5 + 0.5 * abs(math.sin(t * 31)))
    for i in range(6):
        yy = gy0 + (i + 0.7) * (gy1 - gy0) / 6.4 + noise(t * 40, i) * 2.5 * s * vib
        F.line([(gx0 + 6 * s, yy), (gx1 - 6 * s, yy)], _osc((150, 104, 64), 0.8 + 0.4 * vib), 5 * s, round_=False)
    # dial
    dcol = tuple(int(lerp(a, b, rojo)) for a, b in zip(DIAL, ROJO))
    dx0, dx1, dy0, dy1 = cx + 8 * s, x1 - 14 * s, y0 + 34 * s, y0 + 74 * s
    F.rect(dx0, dy0, dx1, dy1, fill=_osc(dcol, 0.12 + 0.88 * on), outline=MADERA_O, w=3 * s)
    for k in range(7):
        xx = lerp(dx0 + 6 * s, dx1 - 6 * s, k / 6)
        F.line([(xx, dy0 + 4 * s), (xx, dy0 + (12 if k % 2 else 18) * s)], _osc((60, 30, 10), 0.6 + 0.4 * on), 2 * s, round_=False)
    ax = lerp(dx0 + 6 * s, dx1 - 6 * s, aguja)
    F.line([(ax, dy0 + 3 * s), (ax, dy1 - 3 * s)], (200, 20, 20), 3 * s, round_=False)
    for kx in (dx0 + 14 * s, dx1 - 14 * s):                                                   # botones
        F.circle((kx, by - 30 * s), 13 * s, fill=(60, 40, 24), outline=(26, 16, 8), w=2 * s)
        F.line([(kx, by - 30 * s), (kx, by - 40 * s)], (170, 150, 110), 2 * s)
    return (cx + 40 * s, y0 + 54 * s)                                                          # centro del dial (para la luz)

def hombre(F, x, piso, s=1.0, t=0.0, gira=0.0, ojos=0.0, dedos=0.0, inclina=0.0):
    """el hombre del rincón: sombrero, cuello del abrigo subido y abrigo gris largo con las mangas colgando. Quieto, parece un
    perchero con un abrigo. gira (0-1): la cara pálida aparece entre el ala y el cuello; ojos: dos brillos bajo el ala;
    dedos: dedos largos asoman de las mangas; inclina: la cabeza se ladea hacia abajo"""
    def P(dx, dy): return (x + dx * s, piso - dy * s)
    for sx_ in (-1, 1):                                                                        # piernas finas y zapatos
        F.line([P(sx_ * 14, 140), P(sx_ * 22, 10)], (18, 18, 22), 11 * s)
        F.ellipse(P(sx_ * 32, 6), 26 * s, 8 * s, fill=(12, 12, 14))
    F.poly([P(-60, 540), P(60, 540), P(84, 130), P(-84, 130)], fill=GRIS)                      # abrigo
    F.poly([P(-6, 536), P(6, 536), P(4, 130), P(-4, 130)], fill=_osc(GRIS, 0.7))
    F.poly([P(0, 532), P(-34, 470), P(-10, 420)], fill=_osc(GRIS, 0.82))                      # solapa
    for by_ in (400, 320, 240): F.circle(P(12, by_), 5 * s, fill=(30, 30, 34))
    for sx_ in (-1, 1):                                                                        # mangas colgando
        F.line([P(sx_ * 58, 528), P(sx_ * 80, 262)], _osc(GRIS, 0.78), 30 * s)
        if dedos > 0:
            for i in range(4):
                a = math.radians(-90 + sx_ * (6 - i * 6))
                L_ = (40 + 18 * (i % 2)) * dedos
                bx, by = P(sx_ * (74 + i * 4), 252)
                F.line([(bx, by), (bx + math.cos(a) * L_ * s * 0.25 * sx_, by - math.sin(a) * L_ * s)], PIEL_H, 6 * s)
    # cara (o sombra) entre el ala del sombrero y el cuello
    ladea = inclina * 10
    F.ellipse(P(0, 598), 36 * s, 44 * s, fill=(8, 8, 10))
    if gira > 0:
        fx = lerp(30, 0, gira)
        rx = lerp(8, 33, gira)
        F.ellipse(P(fx, 594 - ladea), rx * s, 50 * s, fill=PIEL_H)
        if gira > 0.5:
            k = seg(gira, 0.5, 1.0)
            for dx in (-13, 13):
                F.ellipse(P(fx + dx * k, 612 - ladea), 10 * s * k, 9 * s, fill=(140, 134, 130))   # ojeras hundidas
                F.circle(P(fx + dx * k, 612 - ladea), 5.5 * s * k, fill=(2, 2, 4))                 # ojos negros, sin brillo
            F.ellipse(P(fx, 574 - ladea), 19 * s * k, 3.5 * s * k, fill=(4, 4, 6))              # boca: una línea recta, larga
            F.line([P(fx - 9 * k, 594 - ladea), P(fx + 9 * k, 594 - ladea)], (170, 166, 160), 2 * s)   # sin nariz: solo una sombra
    if ojos > 0 and gira < 0.5:
        for dx in (-13, 13): F.circle(P(dx, 612), 3.4 * s, fill=_osc((255, 240, 220), ojos))
    F.poly([P(-50, 540), P(-42, 556), P(42, 556), P(50, 540)], fill=_osc(GRIS, 0.68))        # cuello subido
    # sombrero
    hy = 640 - ladea * 0.6
    F.rect(*P(-38, hy + 66), *P(38, hy + 4), fill=(38, 38, 44))
    F.ellipse(P(0, hy + 66), 38 * s, 8 * s, fill=(46, 46, 52))
    F.rect(*P(-38, hy + 18), *P(38, hy + 6), fill=(12, 12, 14))
    F.ellipse(P(0, hy), 70 * s, 11 * s, fill=(30, 30, 36))
    return P(0, 600)

def cuarto_radio(F, t, on=1.0, voz=0.0, rojo=0.0, aguja=0.35, hom=None):
    """tu cuarto de lado: cama a la izquierda, mesilla con la radio, la foto del abuelo, el reloj y el rincón con el hombre"""
    paredes(F, col=(30, 30, 46))
    F.rect(990, -200, 2000, PISO, fill=(22, 22, 34))                                          # el rincón, más oscuro
    F.line([(990, -200), (990, PISO)], (18, 18, 28), 6)
    # foto del abuelo
    F.rect(260, 690, 420, 880, fill=(70, 52, 36), outline=(40, 28, 18), w=6)
    F.rect(280, 710, 400, 860, fill=(150, 140, 120))
    F.circle((340, 770), 26, fill=(90, 84, 74)); F.poly([(300, 860), (318, 806), (362, 806), (380, 860)], fill=(90, 84, 74))
    F.rect(296, 734, 384, 742, fill=(60, 56, 50))                                              # su sombrero de ala
    reloj_3am(F, 670, 880, 0.26)
    # cama
    F.rect(40, PISO - 150, 560, PISO - 50, fill=(60, 72, 110)); F.rect(40, COLCHON, 560, PISO - 140, fill=(140, 150, 190))
    F.rect(40, PISO - 300, 70, PISO, fill=(80, 60, 50))
    for lx in (52, 548): F.line([(lx, PISO - 50), (lx, PISO)], (40, 46, 70), 10)
    # mesilla y radio
    F.rect(580, PISO - 190, 760, PISO, fill=(70, 54, 44), outline=(40, 30, 24), w=4)
    F.line([(590, PISO - 110), (750, PISO - 110)], (40, 30, 24), 4); F.circle((670, PISO - 150), 6, fill=(170, 150, 100))
    d = radio_vieja(F, RX, RY, 0.75, on=on, voz=voz, t=t, aguja=aguja, rojo=rojo)
    if hom is not None: hombre(F, HX, PISO, **dict(dict(s=HS), **hom))
    return d

def tu_cama(F, t, sienta=0.0, face="closed", jit=0.0):
    p = mix(pose(l1u=2, l2u=-2, l1l=0, l2l=0, a1u=12, a1l=4, a2u=-8, a2l=4), pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=40, a1l=30, a2u=-20), sienta)
    p = add(p, jitter(t, jit, 5))
    return TU.draw(F, p, lerp(250, 300, sienta), lerp(1140, 1150, sienta), f=1, rot=lerp(-90, 0, sienta), snap=False, face=face)

def sobre(F, cx, cy, s=1.0):
    """carta con tu dirección"""
    F.rect(cx - 210 * s, cy - 120 * s, cx + 210 * s, cy + 120 * s, fill=(232, 226, 210), outline=(150, 140, 120), w=4 * s)
    F.rect(cx + 120 * s, cy - 100 * s, cx + 190 * s, cy - 20 * s, fill=(190, 60, 60), outline=(120, 30, 30), w=3 * s)   # sello
    F.text((cx - 40 * s, cy + 6 * s), tr("C/ DEL OLMO, 7"), 40 * s, (30, 30, 50))
    F.line([(cx - 170 * s, cy + 56 * s), (cx + 80 * s, cy + 56 * s)], (120, 120, 140), 4 * s)

def _luz(F, d, on, extra=()):
    return [(d, 260, 0.9 * on), ((RX, RY - 60), 520, 0.55 * on), ((670, 880), 110, 0.6)] + list(extra)

def _habla(t, a, b): return 1.0 if a < t < b else 0.0

# ---------- escenas ----------
def radio(t, D, fi):
    """primer fotograma: oscuridad, solo el 3:00 rojo; clic: el dial se enciende solo. Nos alejamos hasta ver el cuarto"""
    on = seg(t, 0.25, 0.4) * (0.85 + 0.15 * (noise(t * 12, 2) > -0.6))
    k = ease(seg(t, D * 0.3, D))
    F = Frame(fondo(), dict(x=lerp(670, 700, k), y=lerp(900, 1000, k), z=lerp(3.0, 1.35, k)))
    d = cuarto_radio(F, t, on=on, aguja=0.35 + 0.02 * math.sin(t * 3), hom=dict())
    img = iluminar(F.finish(), F, [], glows=_luz(F, d, on), amb=0.14, warm=DIAL)
    return img, dict(grain=9, flash=(DIAL, 0.35 * (1 - seg(t, 0.25, 0.6))) if t > 0.25 else None, tint=((255, 0, 30), 0.06))

def tiempo(t, D, fi):
    """el cuarto entero: tú dormido, la radio encendida en la mesilla… y el 'perchero' en el rincón. Al 'Hoy no', estática"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(520, 540, k), y=980, z=lerp(1.02, 1.08, k)))
    corta = t > 3.1
    on = 0.9 if not corta else (0.4 + 0.6 * (fi % 3 == 0))
    d = cuarto_radio(F, t, on=on, voz=0.4 if t < 3.0 else 1.0, aguja=0.35 if not corta else 0.35 + 0.3 * seg(t, 3.1, 3.5), hom=dict())
    tu_cama(F, t, face="closed" if not corta else "scared")
    img = iluminar(F.finish(), F, [], glows=_luz(F, d, on, [((300, 1110), 200, 0.25)]), amb=0.2, warm=DIAL)
    return img, dict(grain=9, glitch=0.25 if corta and fi % 4 == 0 else 0.0, tint=((255, 0, 30), 0.12 * corta))

def aviso(t, D, fi):
    """primer plano de la radio: la aguja salta sola de emisora y el altavoz habla"""
    habla = _habla(t, 1.5, 4.8)
    F = Frame(fondo(), dict(x=RX + 20, y=RY - 70, z=lerp(2.9, 3.3, ease(t / D)), sx=noise(t * 30) * 2 * habla))
    ag = 0.35 + 0.45 * ease(seg(t, 0.5, 1.2)) + noise(t * 8, 3) * 0.02
    d = cuarto_radio(F, t, on=1.0, voz=habla, aguja=ag, rojo=0.6 * seg(t, 1.2, 2.0))
    img = iluminar(F.finish(), F, [], glows=_luz(F, d, 1.0), amb=0.18, warm=DIAL)
    return img, dict(grain=10, tint=((255, 0, 30), 0.06 + 0.1 * seg(t, 1.2, 2.0)), glitch=0.2 if 0.5 < t < 1.2 and fi % 2 else 0.0)

def casa(t, D, fi):
    """la carta con tu dirección en la mesilla; corte: tú, sentado en la cama, mirando la radio"""
    if t < 1.45:
        F = Frame(fondo(), dict(x=540, y=900, z=lerp(1.0, 1.12, ease(t / 1.45))))
        F.rect(-600, -400, 1700, 2400, fill=(60, 44, 34))                                    # la madera de la mesilla
        for yy in range(500, 1400, 90): F.line([(-600, yy), (1700, yy + 20)], (52, 38, 30), 4)
        sobre(F, 540, 880, 1.6)
        img = iluminar(F.finish(), F, [], glows=[((800, 600), 700, 0.75)], amb=0.25, warm=DIAL)
        return img, dict(grain=9, tint=((255, 0, 30), 0.05))
    tl = t - 1.45
    F = Frame(fondo(), dict(x=lerp(430, 450, ease(tl / 2)), y=1020, z=lerp(1.4, 1.55, ease(tl / 2.5))))
    d = cuarto_radio(F, t, on=1.0, voz=0.3, aguja=0.8, rojo=0.6, hom=dict())
    J = tu_cama(F, t, sienta=ease(seg(tl, 0, 0.35)), face="scared", jit=2.0)
    img = iluminar(F.finish(), F, [], glows=_luz(F, d, 1.0, [(J["head"], 170, 0.4)]), amb=0.18, warm=DIAL)
    return img, dict(grain=10, flash=((255, 255, 255), 0.4 * (1 - seg(tl, 0, 0.2))), tint=((255, 0, 30), 0.1))

def abrigo(t, D, fi):
    """la radio describe al hombre; la cámara se aparta de la radio y se desliza despacio hacia el rincón oscuro"""
    habla = _habla(t, 0.1, 2.15) + _habla(t, 2.35, 4.1)
    k = ease(seg(t, 1.6, D))
    F = Frame(fondo(), dict(x=lerp(RX + 20, 880, k), y=lerp(RY - 70, 900, k), z=lerp(3.0, 1.6, k)))
    d = cuarto_radio(F, t, on=1.0, voz=habla, aguja=0.8, rojo=0.8, hom=dict())
    img = iluminar(F.finish(), F, [], glows=_luz(F, d, 1.0), amb=0.13, warm=(255, 120, 90))
    return img, dict(grain=11, tint=((255, 0, 30), 0.12 + 0.06 * k))

def rincon(t, D, fi):
    """tú, en primer plano y de lado, sentado en la cama; al fondo, el 'perchero' con el abrigo gris y el sombrero"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(820, 880, k), y=lerp(1000, 950, k), z=lerp(1.45, 1.75, k)))
    d = cuarto_radio(F, t, on=0.85, voz=0.15, aguja=0.8, rojo=0.8, hom=dict())
    big(TU, 1.6, F, add(pose(body=-4, head=6, a1u=30, a1l=60, a2u=10, a2l=40), jitter(t, 2, 3)), 560, 1420, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=_luz(F, d, 0.85, [((HX, PISO - 380 * HS), 260, 0.35)]), amb=0.15, warm=(255, 140, 100))
    return img, dict(grain=11, tint=((255, 0, 30), 0.1))

def perchero(t, D, fi):
    """primer plano del sombrero y el cuello del abrigo. Bajo el ala, dos brillos: ojos"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=HX - 20, y=lerp(880, 830, k), z=lerp(2.4, 3.1, k)))
    ojos = seg(t, 1.0, 1.25)
    d = cuarto_radio(F, t, on=0.8, voz=0.0, aguja=0.8, rojo=0.8, hom=dict(ojos=ojos, t=t))
    img = iluminar(F.finish(), F, [], glows=_luz(F, d, 0.8, [((HX, PISO - 520 * HS), 220, 0.5)]), amb=0.13, warm=(255, 140, 100))
    return img, dict(grain=12, tint=((255, 0, 30), 0.1 + 0.08 * ojos), flash=((255, 255, 255), 0.3 * (1 - seg(t, 1.0, 1.3))) if t > 1.0 else None)

def gira(t, D, fi):
    """la radio se apaga (solo queda el reloj rojo); el sombrero gira despacio hacia ti y enseña una cara pálida"""
    off = t > 0.7
    on = 1.0 if not off else max(0.0, 1 - seg(t, 0.7, 0.9))
    g = ease(seg(t, 1.6, 3.0))
    hit = t > 3.0
    F = Frame(fondo(), dict(x=lerp(820, HX, ease(seg(t, 1.0, 3.0))), y=lerp(950, 840, ease(seg(t, 1.0, 3.2))),
                            z=lerp(1.5, 3.6, ease(seg(t, 1.0, 3.2))), sx=noise(t * 40) * 6 * hit, sy=noise(t * 40, 1) * 6 * hit))
    d = cuarto_radio(F, t, on=on, voz=0.0, aguja=0.8, rojo=0.8, hom=dict(gira=g, dedos=seg(t, 3.0, 3.6), t=t))
    img = iluminar(F.finish(), F, [], glows=_luz(F, d, on, [((HX, PISO - 600 * HS), 200, 0.55 * (off))]), amb=0.12, warm=ROJO if off else DIAL)
    return img, dict(grain=12, tint=((255, 0, 30), 0.12 + 0.1 * hit), dark=0.1 * off * (1 - hit),
                     flash=((255, 255, 255), 0.7 * (1 - seg(t, 3.0, 3.3))) if hit else None,
                     glitch=0.35 if hit and t < 3.5 and fi % 3 else 0.0)

def final(t, D, fi):
    """a oscuras: el hombre, de pie junto a tu cama, mirándote; la radio se vuelve a encender sola. Y la regla"""
    on = 0.25 + 0.45 * (noise(t * 10, 6) > -0.2)
    F = Frame(fondo(), dict(x=420, y=lerp(1200, 1185, ease(t / D)), z=lerp(1.45, 1.55, ease(t / D))))
    d = cuarto_radio(F, t, on=on, voz=0.6, aguja=0.8, rojo=0.9)
    tu_cama(F, t, face="scared", jit=1.0)
    c = hombre(F, 620, PISO, s=0.9, t=t, gira=1.0, dedos=1.0, inclina=0.8)
    img = iluminar(F.finish(), F, [], glows=_luz(F, d, on, [(c, 220, 0.6), ((300, 1110), 160, 0.3)]), amb=0.12, warm=(255, 110, 90))
    pp = ease_back(seg(t, D * 0.4, D * 0.5)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d_ = ImageDraw.Draw(img)
        d_.rounded_rectangle((40, 1150, 1040, 1600), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 SE ENCIENDE"), 1210, 62, (255, 255, 255)), (tr("LA RADIO…"), 1290, 62, (255, 255, 255)),
                                 (tr("ESCUCHA LA"), 1400, 104, (255, 40, 50)), (tr("DIRECCIÓN"), 1510, 104, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d_.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d_.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d_.rounded_rectangle((230, 1640, 850, 1730), 26, fill=(230, 30, 50))
        d_.text((540, 1685), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.2 * pp if pp > 0 else 0.1), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(radio=radio, tiempo=tiempo, aviso=aviso, casa=casa, abrigo=abrigo, rincon=rincon, perchero=perchero, gira=gira, final=final)
PAUSA = dict(radio=0.6, tiempo=0.5, aviso=0.6, casa=0.6, abrigo=0.7, rincon=0.7, perchero=1.0, gira=1.2, final=2.4)
