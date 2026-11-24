"""Si oyes esto a las 3AM — 25: "El silencio". A las tres, todos los ruidos de la casa se apagan de golpe: la nevera, el reloj,
los coches. Tu móvil vibra: tu madre, desde su cuarto, "No respires fuerte. Está escuchando". Algo alto y pálido recorre el
pasillo y se para en cada puerta, con la cabeza pegada a la madera. Se para en la tuya. Te tapas la boca. Le escribes
"Está en mi puerta". Ella contesta y, en el silencio, tu móvil vibra: "QUITA LA VIBRACIÓN". La puerta se abre.
Piezas nuevas reutilizables: cocina_noche (cocina con nevera, reloj de pared y ventana a la calle; 'parado' congela todo),
pasillo_puertas (pasillo de lado con tres puertas y la rendija de luz bajo la tuya), escucha (la figura con la cabeza ladeada
contra una puerta), bzz (rayitas de vibración alrededor del móvil), sombras_rendija (dos pies tapando la luz bajo la puerta)."""
import math
import numpy as np
from PIL import Image, ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am2 import cara_palida, dedos, PIEL
from escenas3am3 import paredes, PISO
from escenas3am5 import _osc
from escenas3am21 import chat_grupo
from escenas3am24 import (cuarto_puerta, reloj_hora, ojos_ir, visita_lado, VISITA, PUERTA_X0, PUERTA_X1)

ROJO = (255, 40, 40)
AZUL = (150, 200, 255)
LUNA = (170, 190, 255)
MAMA_T = "MAMÁ"
_BG = {}
def fondo(k="a"):
    if k not in _BG:
        _BG[k] = {"a": gradient((30, 32, 50), (10, 10, 18)), "m": gradient((12, 12, 16), (4, 4, 6))}[k]
    return _BG[k]

# ---------- piezas ----------
def bzz(F, c, t, k=1.0, r=280, col=(255, 255, 255)):
    """rayitas de vibración a los lados del móvil"""
    if k <= 0: return
    cx, cy = c
    for s_ in (-1, 1):
        for i in range(3):
            j = noise(t * 50 + i * 3 + s_) * 10
            x = cx + s_ * (r + i * 30)
            F.line([(x + j, cy - 120 + i * 20), (x - j, cy - 60 + i * 20)], col, 8 * k)
            F.line([(x - j, cy + 60 - i * 20), (x + j, cy + 120 - i * 20)], col, 8 * k)

def cocina_noche(F, t, parado=0.0, car_t=0.0):
    """cocina a oscuras: nevera con lucecita verde (se apaga), reloj de pared (el segundero se para) y ventana con un coche
    pasando (se congela)"""
    paredes(F, col=(30, 34, 46))
    F.rect(-900, PISO - 380, 2000, PISO - 360, fill=(54, 50, 46))                                   # encimera
    F.rect(-900, PISO - 360, 2000, PISO, fill=(40, 36, 34))
    for x in range(-900, 2000, 260): F.line([(x, PISO - 360), (x, PISO)], (26, 24, 22), 4)
    # nevera (izquierda)
    F.rect(60, PISO - 820, 380, PISO, fill=(190, 196, 202), outline=(110, 114, 120), w=6)
    F.line([(60, PISO - 560), (380, PISO - 560)], (110, 114, 120), 6)
    F.line([(340, PISO - 760), (340, PISO - 620)], (120, 124, 130), 10); F.line([(340, PISO - 500), (340, PISO - 360)], (120, 124, 130), 10)
    if parado < 0.5: F.circle((110, PISO - 780), 9, fill=(80, 255, 120))
    else: F.circle((110, PISO - 780), 9, fill=(40, 44, 46))
    if parado < 0.5:                                                                                # zumbido
        for i in range(3):
            o = (t * 60 + i * 20) % 60
            F.line([(170 + i * 50, PISO - 840 - o), (190 + i * 50, PISO - 860 - o)], (150, 160, 170), 4)
    # reloj de pared (centro)
    cx, cy = 640, 560
    F.circle((cx, cy), 110, fill=(230, 226, 214), outline=(60, 50, 40), w=10)
    for h in range(12):
        a = h / 12 * 2 * math.pi
        F.line([(cx + 86 * math.sin(a), cy - 86 * math.cos(a)), (cx + 98 * math.sin(a), cy - 98 * math.cos(a))], (40, 36, 30), 6)
    F.line([(cx, cy), (cx, cy - 70)], (30, 26, 22), 10)                                             # 3:00
    F.line([(cx, cy), (cx + 56, cy)], (30, 26, 22), 12)
    sec = (t if parado < 0.5 else 0.25) * 2 * math.pi / 3
    F.line([(cx, cy), (cx + 92 * math.sin(sec), cy - 92 * math.cos(sec))], (200, 30, 30), 4)
    F.circle((cx, cy), 10, fill=(200, 30, 30))
    # ventana a la calle (derecha) con un coche
    F.rect(900, 380, 1320, 760, fill=(14, 18, 34), outline=(70, 66, 80), w=12)
    F.line([(1110, 380), (1110, 760)], (70, 66, 80), 8)
    F.rect(910, 680, 1310, 750, fill=(22, 24, 30))
    cxr = 930 + min(car_t, 0.35) * 420
    F.line([(1010, 690), (1010, 470)], (60, 62, 70), 8); F.circle((1010, 466), 14, fill=(255, 220, 150))   # farola
    F.poly([(cxr + 150, 672), (min(cxr + 330, 1300), 640), (min(cxr + 330, 1300), 712), (cxr + 150, 688)], fill=(120, 116, 96))       # haz de los faros
    F.rect(cxr, 650, cxr + 150, 700, fill=(110, 40, 40)); F.rect(cxr + 30, 620, cxr + 110, 652, fill=(90, 34, 34))
    F.rect(cxr + 40, 626, cxr + 100, 650, fill=(30, 36, 50))
    F.circle((cxr + 30, 702), 14, fill=(10, 10, 12)); F.circle((cxr + 120, 702), 14, fill=(10, 10, 12))
    F.circle((cxr + 150, 680), 10, fill=(255, 240, 180))
    F.rect(900, 380, 1320, 390, fill=(70, 66, 80))
    return (cxr + 150, 680), (cx, cy), (110, PISO - 780)

DOORS = (100, 620, 1140)          # x izquierda de cada puerta: mamá, baño, la tuya
DW = 240
def pasillo_puertas(F, t, rendija=1.0):
    """pasillo visto de lado: tres puertas cerradas; bajo la tuya (derecha) la rendija azul de la luz de tu móvil"""
    paredes(F, col=(28, 30, 44))
    F.rect(-900, 200, 2000, 236, fill=(20, 22, 32))                                                 # techo
    for i, x in enumerate(DOORS):
        F.rect(x - 20, PISO - 600, x + DW + 20, PISO, fill=(46, 38, 32))
        F.rect(x, PISO - 580, x + DW, PISO - 8, fill=(84, 66, 52), outline=(40, 30, 24), w=4)
        F.rect(x + 30, PISO - 540, x + DW - 30, PISO - 330, outline=(66, 52, 40), w=4)
        F.rect(x + 30, PISO - 290, x + DW - 30, PISO - 60, outline=(66, 52, 40), w=4)
        F.circle((x + DW - 30, PISO - 290), 10, fill=(196, 168, 96))
    x = DOORS[2]
    if rendija > 0: F.rect(x, PISO - 8, x + DW, PISO, fill=_osc(AZUL, 0.8 * rendija))
    F.rect(DOORS[0], PISO - 8, DOORS[0] + DW, PISO, fill=(120, 60, 70))                             # cuarto de mamá: lucecita
    F.rect(1500, 300, 1700, 700, fill=(10, 14, 30), outline=(70, 66, 80), w=10)                     # ventana del fondo
    F.circle((1620, 380), 18, fill=(200, 210, 240))

def escucha(F, t, x, piso=PISO, inclina=1.0, f=1, fase=0.0, anda=0.0):
    """la figura alta y pálida; inclina: dobla el cuello y pega la oreja a la puerta (f=1 mira a la derecha)"""
    if anda > 0:
        return visita_lado(F, t, x, piso, f=f, fase=fase)
    p = pose(body=8 + 22 * inclina, head=6 + 40 * inclina, a1u=8, a1l=4, a2u=-8, a2l=4, l1u=6, l2u=-6, l1l=-4, l2l=-4)
    J = VISITA.draw(F, p, x, piso, f=f, face="closed", t=t, stretch=1.15)
    hx, hy = J["head"]; r = L["head"] * VISITA.scale
    s = -f
    F.poly([(hx - s * r * 1.1, hy - r * 0.9), (hx + s * r * 0.3, hy - r * 1.15), (hx + s * r * 0.2, hy + r * 0.2),
            (hx - s * r * 0.7, hy + r * 2.4), (hx - s * r * 1.3, hy + r * 2.0)], fill=(12, 12, 16))
    return [(hx + f * r * 0.55, hy - r * 0.05)]

def sombras_rendija(F, x0, x1, k=1.0):
    """dos pies que tapan la rendija de luz bajo la puerta"""
    if k <= 0: return
    w = (x1 - x0)
    for c in (0.33, 0.62):
        F.rect(x0 + w * c - 26, PISO - 9, x0 + w * c + 26 * k, PISO + 1, fill=(4, 4, 6))

def _mama(p=1.0):
    return dict(txt=tr("No respires fuerte.\nEstá escuchando."), de=MAMA_T, colde=(240, 140, 180), p=p)

# ---------- escenas ----------
def reloj(t, D, fi):
    """primer fotograma: el reloj de la mesilla, 3:00 en rojo, enorme. Los dos puntos dejan de parpadear (todo se para).
    La cámara se aleja: tú en la cama, con los ojos muy abiertos y la puerta cerrada"""
    k = ease(seg(t, D * 0.45, D))
    rx, ry = 825, PISO - 222
    F = Frame(fondo(), dict(x=lerp(rx, 760, k), y=lerp(ry, 980, k), z=lerp(3.2, 1.0, k)))
    ojos, cab, mov = cuarto_puerta(F, t, abre=0.0, cara=0.0, tu_face="scared", sienta=0.0)
    F.rect(PUERTA_X0, PISO - 8, PUERTA_X1, PISO, fill=(30, 34, 50))
    parpadea = t < D * 0.12 and int(t * 4) % 2 == 0
    reloj_hora(F, rx, ry, 0.3, txt="3 00" if (t < D * 0.12 and not parpadea) else "3:00")
    img = iluminar(F.finish(), F, [], glows=[((rx, ry), 220, 0.9), (mov, 200, 0.6), ((640, 610), 200, 0.4)], amb=0.24, warm=AZUL)
    return img, dict(grain=9, flash=(ROJO, 0.4 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.08))

def nada(t, D, fi):
    """tres planos cortos: la lucecita de la nevera se apaga, el segundero se para, el coche de la calle se congela"""
    parte = min(2, int(t / (D / 3)))
    tl = t - parte * D / 3
    car, rel, nev = cocina_noche(Frame(fondo(), dict(x=0, y=0, z=1)), 0)  # posiciones
    foco = [(220, PISO - 700), (640, 560), (1110, 600)][parte]
    F = Frame(fondo(), dict(x=foco[0], y=foco[1] + 60, z=lerp(1.9, 2.1, tl / (D / 3))))
    stop = 0.0 if tl < 0.35 else 1.0
    car, rel, nev = cocina_noche(F, (parte * D / 3 + min(tl, 0.35)), parado=stop, car_t=tl)
    gl = [((640, 560), 260, 0.4), ((1110, 570), 260, 0.5)]
    if stop < 0.5: gl.append((nev, 120, 0.6)); gl.append((car, 160, 0.8))
    img = iluminar(F.finish(), F, [], glows=gl, amb=0.28, warm=LUNA)
    return img, dict(grain=9, flash=((255, 255, 255), 0.25 * (1 - seg(tl, 0, 0.15))), tint=((255, 0, 30), 0.05))

def mensaje(t, D, fi):
    """el móvil vibra: mensaje de MAMÁ. 'No respires fuerte. Está escuchando.'"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo("m"), dict(x=540, y=lerp(780, 860, k), z=lerp(1.4, 1.1, k)))
    vib = 1.0 - seg(t, 0.9, 1.1)
    c = chat_grupo(F, t, [_mama(seg(t, 0.15, 0.5))], MAMA_T, tr("en línea"), vib=vib, privado=True)
    bzz(F, c, t, k=vib)
    img = iluminar(F.finish(), F, [], glows=[(c, 620, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=9, tint=((255, 0, 30), 0.05 + 0.08 * seg(t, D * 0.6, D)))

def pasillo(t, D, fi):
    """el pasillo: la figura pasa por delante de la puerta de mamá, llega a la del baño y pega la oreja, escuchando"""
    llega = seg(t, 0, D * 0.55)
    x = lerp(-200, DOORS[1] - 150, llega)
    inc = ease(seg(t, D * 0.6, D * 0.85))
    F = Frame(fondo(), dict(x=lerp(300, DOORS[1] + 100, ease(llega)), y=lerp(950, 880, inc), z=lerp(0.85, 1.05, inc)))
    pasillo_puertas(F, t)
    if llega < 1:
        ojos = escucha(F, t, x, anda=1.0, fase=llega * 5)
    else:
        ojos = escucha(F, t, x, inclina=inc)
    img = iluminar(F.finish(), F, [], glows=[((1600, 380), 500, 0.5), ((DOORS[2] + DW / 2, PISO), 220, 0.6), ((DOORS[0] + DW / 2, PISO), 160, 0.4),
                                            ((x, PISO - 500), 460, 0.9)], amb=0.24, warm=LUNA)
    img = ojos_ir(img, F, ojos, k=0.8, r=4)
    return img, dict(grain=10, tint=((255, 0, 30), 0.06 + 0.06 * inc))

def puerta(t, D, fi):
    """tu cuarto: la rendija de luz bajo tu puerta se corta con dos sombras de pies. Tú te tapas la boca con la mano"""
    sombra = seg(t, D * 0.1, D * 0.3)
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(1080, 620, k), y=lerp(1180, 1000, k), z=lerp(2.2, 1.35, k)))
    ojos, cab, mov = cuarto_puerta(F, t, abre=0.0, cara=0.0, tu_face="scared", sienta=0.0)
    reloj_hora(F, 825, PISO - 222, 0.3, txt="3:00")
    F.rect(PUERTA_X0, PISO - 8, PUERTA_X1, PISO, fill=(150, 160, 190))                           # luz del pasillo (luna)
    sombras_rendija(F, PUERTA_X0, PUERTA_X1, k=sombra)
    tapa = ease(seg(t, D * 0.45, D * 0.65))
    if tapa > 0:
        hx, hy = cab
        F.circle((lerp(hx + 70, hx + 10, tapa), lerp(hy + 60, hy + 14, tapa)), 22, fill=(240, 232, 222))
    img = iluminar(F.finish(), F, [], glows=[(mov, 220, 0.8), (cab, 140, 0.3), ((825, PISO - 222), 160, 0.5),
                                            (((PUERTA_X0 + PUERTA_X1) / 2, PISO), 200, 0.6)], amb=0.22, warm=AZUL)
    return img, dict(grain=10, tint=((255, 0, 30), 0.08 + 0.08 * sombra), flash=(ROJO, 0.25 * max(0, 1 - abs(t - D * 0.2) / 0.12)))

def escribes(t, D, fi):
    """escribes 'está en mi puerta' y lo envías"""
    txt = tr("está en mi puerta")
    n = int(len(txt) * seg(t, D * 0.1, D * 0.65))
    env_ = seg(t, D * 0.72, D * 0.85)
    msgs = [_mama()]
    if env_ > 0: msgs.append(dict(txt=txt, de=None, p=env_, tk=2))
    F = Frame(fondo("m"), dict(x=540, y=860, z=1.12 + 0.06 * seg(t, 0, D)))
    c = chat_grupo(F, t, msgs, MAMA_T, tr("en línea"), entrada="" if env_ > 0 else txt[:n], cursor=env_ <= 0, privado=True)
    img = iluminar(F.finish(), F, [], glows=[(c, 620, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=9, tint=((255, 0, 30), 0.08))

def vibra(t, D, fi):
    """el giro: llega su respuesta y el móvil vibra fuerte en el silencio. 'QUITA LA VIBRACIÓN', en rojo"""
    llega = seg(t, D * 0.12, D * 0.3)
    vib = 1.0 if t > D * 0.12 else 0.0
    msgs = [_mama(), dict(txt=tr("está en mi puerta"), de=None, tk=2)]
    if llega > 0: msgs.append(dict(txt=tr("QUITA LA\nVIBRACIÓN"), de=MAMA_T, colde=(240, 140, 180), p=llega, rojo=True))
    k = ease(seg(t, D * 0.3, D))
    F = Frame(fondo("m"), dict(x=540, y=lerp(860, 800, k), z=lerp(1.12, 1.4, k)))
    c = chat_grupo(F, t, msgs, MAMA_T, tr("en línea"), vib=vib * 1.6, privado=True)
    bzz(F, c, t, k=vib * 1.3, col=ROJO)
    img = iluminar(F.finish(), F, [], glows=[(c, 620, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=10, tint=((255, 0, 30), 0.08 + 0.16 * vib), flash=(ROJO, 0.4 * max(0, 1 - abs(t - D * 0.14) / 0.12)),
                     glitch=0.25 if vib and fi % 6 == 0 else 0.0)

def abre(t, D, fi):
    """la puerta de tu cuarto se abre despacio; muy arriba, la cara pálida asoma con la cabeza ladeada"""
    ab = seg(t, D * 0.05, D * 0.5)
    cara = seg(t, D * 0.3, D * 0.5)
    k = ease(seg(t, 0, D))
    hit = seg(t, D * 0.48, D * 0.53)
    F = Frame(fondo(), dict(x=lerp(700, 960, k), y=lerp(1000, 860, k), z=lerp(1.05, 1.7, k), sx=noise(t * 40) * 8 * hit * (1 - seg(t, D * 0.6, D * 0.75))))
    ojos, cab, mov = cuarto_puerta(F, t, abre=ab, cara=cara)
    reloj_hora(F, 825, PISO - 222, 0.3, txt="3:00")
    img = iluminar(F.finish(), F, [], glows=[(mov, 260, 1.0), (cab, 160, 0.4), ((825, PISO - 222), 180, 0.6), ((640, 610), 200, 0.4),
                                            ((PUERTA_X0 + 60, PISO - 480), 200, 0.3 * cara)], amb=0.24, warm=AZUL)
    img = ojos_ir(img, F, ojos, k=cara, r=4.5)
    return img, dict(grain=10, tint=((255, 0, 30), 0.1 + 0.12 * hit), flash=(ROJO, 0.35 * max(0, 1 - abs(t - D * 0.5) / 0.15)),
                     glitch=0.3 if 0 < t - D * 0.48 < 0.25 and fi % 2 else 0.0)

def final(t, D, fi):
    """plano general: la puerta abierta, la cara arriba y tú en la cama. La regla"""
    k = ease(seg(t, 0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(960, 700, k), y=lerp(860, 1000, k), z=lerp(1.7, 1.0, k)))
    ojos, cab, mov = cuarto_puerta(F, t, abre=1.0, cara=1.0)
    reloj_hora(F, 825, PISO - 222, 0.3, txt="3:00")
    img = iluminar(F.finish(), F, [], glows=[(mov, 260, 1.0), (cab, 160, 0.4), ((825, PISO - 222), 180, 0.6), ((640, 610), 200, 0.4),
                                            ((PUERTA_X0 + 60, PISO - 480), 200, 0.3)], amb=0.24, warm=AZUL)
    img = ojos_ir(img, F, ojos, k=0.8 + 0.2 * math.sin(t * 6), r=4.5)
    pp = ease_back(seg(t, D * 0.42, D * 0.52)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 130, 1040, 640), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3"), 200, 62, (255, 255, 255)), (tr("TODO SE CALLA…"), 280, 62, (255, 255, 255)),
                                 (tr("CÁLLATE TÚ"), 420, 100, (255, 40, 50)), (tr("TAMBIÉN"), 545, 100, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 680, 850, 770), 26, fill=(230, 30, 50))
        d.text((540, 725), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.22 * pp if pp > 0 else 0.08), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(reloj=reloj, nada=nada, mensaje=mensaje, pasillo=pasillo, puerta=puerta, escribes=escribes, vibra=vibra,
                 abre=abre, final=final)
PAUSA = dict(reloj=0.6, nada=0.7, mensaje=0.6, pasillo=0.6, puerta=0.8, escribes=0.4, vibra=0.7, abre=0.8, final=2.0)
