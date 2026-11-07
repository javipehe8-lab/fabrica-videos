"""Si oyes esto a las 3AM — 8: "Tu número te llama". Tu cuarto con la cama alta de la historia 5 (hueco negro debajo).
Piezas nuevas reutilizables: pantalla_llamada (móvil a pantalla completa: entrante / finalizada / llamando),
tu_movil (TU tumbado con el móvil en la oreja), movil_suelo (móvil apoyado en el suelo, bajo la cama, que vibra y alumbra)."""
import math
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am
from escenas3am2 import cara_palida, dedos, PIEL
from escenas3am5 import (fondo, _osc, _cuarto, cama_alta, manta, PISO, HUECO, COLCHON, CAMA_X0, CAMA_X1)

AZUL = (150, 200, 255)               # luz de pantalla
ROJO = (255, 40, 40)
MS = (420, PISO - 6)                 # móvil bajo la cama (base)

def pantalla_llamada(F, t, modo="entrante", cx=540, cy=900, vib=0.0, seg_=9):
    """móvil a pantalla completa. modo: entrante (botones verde/rojo), finalizada, llamando"""
    v = noise(t * 60) * 12 * vib
    cx += v
    F.line([(150, 1800), (370, 1300)], TU.shirt, 84); F.circle((430, 1230), 64, fill=(240, 232, 222))
    F.rect(cx - 240, cy - 440, cx + 240, cy + 440, fill=(20, 20, 26), outline=(90, 90, 100), w=8)
    F.rect(cx - 214, cy - 400, cx + 214, cy + 400, fill=(16, 22, 36) if modo != "finalizada" else (24, 14, 18))
    F.text((cx, cy - 340), "3:00", 54, ROJO)
    top = {"entrante": tr("LLAMADA ENTRANTE"), "finalizada": tr("LLAMADA FINALIZADA"), "llamando": tr("LLAMANDO…")}[modo]
    F.text((cx, cy - 260), top, 34, (170, 180, 200) if modo != "finalizada" else (255, 110, 110))
    F.circle((cx, cy - 120), 82, fill=(70, 80, 100)); F.circle((cx, cy - 148), 28, fill=(160, 170, 190))
    F.ellipse((cx, cy - 84), 46, 28, fill=(160, 170, 190))
    F.text((cx, cy + 10), tr("TÚ"), 96, (240, 240, 250))
    F.text((cx, cy + 90), tr("(MI NÚMERO)"), 34, (150, 160, 180))
    if modo == "entrante":
        p = 1 + 0.08 * math.sin(t * 12)
        F.circle((cx - 110, cy + 270), 54 * p, fill=(40, 190, 90)); F.circle((cx + 110, cy + 270), 54, fill=(220, 40, 50))
        F.line([(cx - 134, cy + 270), (cx - 86, cy + 270)], (255, 255, 255), 10); F.line([(cx + 86, cy + 274), (cx + 134, cy + 274)], (255, 255, 255), 10)
    elif modo == "finalizada":
        F.text((cx, cy + 180), "00:%02d" % seg_, 40, (200, 120, 120))
    else:
        for i in range(3):
            on = (int(t * 3) % 4) > i
            F.circle((cx - 50 + i * 50, cy + 190), 14, fill=(200, 210, 230) if on else (60, 66, 80))
        F.circle((cx, cy + 290), 54, fill=(220, 40, 50)); F.line([(cx - 24, cy + 294), (cx + 24, cy + 294)], (255, 255, 255), 10)
    return (cx, cy)

def tu_movil(F, t, oreja=1.0, face="scared", jit=0.0, luz=True):
    """TU tumbado en la cama con el móvil (oreja: 1 = pegado a la oreja, 0 = delante de la cara)"""
    p = pose(a1u=lerp(170, 150, 1 - oreja), a1l=lerp(165, 100, 1 - oreja), a2u=10, a2l=20)
    p = add(p, jitter(t, jit, 5))
    J = TU.draw(F, p, 330, COLCHON - 12, f=1, rot=-90, snap=False, face=face)
    hx, hy = J["a1h"]
    F.rect(hx - 9, hy - 22, hx + 9, hy + 22, fill=(26, 30, 40))
    if luz: F.rect(hx - 5, hy - 18, hx + 5, hy + 18, fill=AZUL)
    return J, (hx, hy)

def movil_suelo(F, t, on=1.0, vib=0.0, alto=0.0, x=None):
    """móvil apoyado en el suelo bajo la cama, de pie, con la pantalla hacia ti. on: brillo; alto: lo levantan"""
    x = (x if x is not None else MS[0]) + noise(t * 70, 3) * 5 * vib
    y = MS[1] - alto
    F.rect(x - 26, y - 84, x + 26, y, fill=(18, 18, 24), outline=(60, 60, 70), w=3)
    if on > 0:
        F.rect(x - 21, y - 78, x + 21, y - 6, fill=_osc(AZUL, 0.35 + 0.65 * on))
        F.text((x, y - 50), tr("TÚ"), 20, _osc((20, 30, 50), on))
        F.circle((x, y - 22), 7, fill=_osc((40, 190, 90), on))
    if vib > 0:                                                                     # ondas del timbre
        for i in range(3):
            u = (t * 1.6 + i / 3) % 1
            F.arc((x, y - 44), 40 + 90 * u, 200, 340, _osc(AZUL, 0.7 * (1 - u) * vib), 4)
    return (x, y - 44)

def cara_copia(F, c, r, abre=0.0, t=0.0):
    """tu misma cara redonda… pero gris, con los ojos negros enormes y una boca demasiado ancha"""
    hx, hy = c
    F.circle((hx, hy), r, fill=(196, 196, 192), outline=(30, 30, 34), w=r * 0.08)
    F.ellipse((hx, hy + r * 0.55), r * 0.75, r * 0.3, fill=(170, 170, 166))                       # sombra de la barbilla
    for dx, dy in ((-0.34, -0.06), (0.34, -0.1)):                                              # ojos desiguales, enormes, fijos
        F.ellipse((hx + dx * r, hy + dy * r), r * 0.24, r * 0.3, fill=(140, 138, 136))
        F.ellipse((hx + dx * r, hy + dy * r + r * 0.02), r * 0.19, r * 0.26, fill=(2, 2, 4))
        F.circle((hx + dx * r, hy + dy * r + r * 0.02), r * 0.03, fill=(255, 255, 255))
    F.ellipse((hx, hy + r * 0.5), r * (0.1 + 0.04 * abre), r * (0.03 + 0.3 * abre), fill=(2, 2, 4))   # boca: rendija que se estira al hablar
    F.line([(hx - r * 0.5, hy - r * 0.5), (hx - r * 0.2, hy - r * 0.38)], (120, 118, 116), r * 0.04)  # cejas tensas, sin expresión
    F.line([(hx + r * 0.5, hy - r * 0.54), (hx + r * 0.2, hy - r * 0.42)], (120, 118, 116), r * 0.04)

def hueco_cosa(F, t, cara=1.0, abre=0.0, x=470):
    """la cosa tumbada bajo la cama: cuerpo largo en la sombra y la cara pálida mirando hacia fuera"""
    F.ellipse((x + 150, PISO - 36), 200, 30, fill=_osc(PIEL, 0.22))
    if cara > 0: cara_copia(F, (x, PISO - 86), 52, abre=abre, t=t)

# ---------- escenas ----------
def entrante(t, D, fi):
    """primer fotograma: la pantalla del móvil, 3:00 en rojo, y quien llama eres TÚ"""
    k = ease(seg(t, 0, D))
    F = Frame(gradient((14, 14, 18), (6, 6, 8)), dict(x=540, y=lerp(760, 880, k), z=lerp(1.5, 1.05, k)))
    c = pantalla_llamada(F, t, "entrante", cy=800, vib=0.6 + 0.4 * (math.sin(t * 9) > 0))
    img = iluminar(F.finish(), F, [], glows=[(c, 600, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=9, flash=(ROJO, 0.4 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.1))

def contestas(t, D, fi):
    """en la cama, hablando. Pista: bajo la cama hay una lucecita azul encendida (otra pantalla)"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(430, 400, k), y=lerp(PISO - 260, PISO - 150, k), z=lerp(1.45, 1.9, k)))
    _cuarto(F, t)
    J, ph = tu_movil(F, t, face="scared", jit=1.0)
    manta(F)
    pul = 0.5 + 0.2 * math.sin(t * 3)
    movil_suelo(F, t, on=pul)
    img = iluminar(F.finish(), F, [], glows=[(ph, 200, 0.6), ((MS[0], MS[1] - 44), 130, 0.6 * pul), ((825, PISO - 222), 160, 0.45)],
                   amb=0.22, warm=AZUL)
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * seg(t, D * 0.4, D)))

def broma(t, D, fi):
    """cuelgas: tu pantalla y la lucecita de debajo de la cama se apagan a la vez"""
    off = t > D * 0.55
    F = Frame(fondo(), dict(x=410, y=PISO - 170, z=1.7))
    _cuarto(F, t)
    J, ph = tu_movil(F, t, oreja=1 - ease(seg(t, D * 0.1, D * 0.45)), face="neutral", luz=not off)
    manta(F)
    movil_suelo(F, t, on=0.0 if off else 0.55)
    gl = [((825, PISO - 222), 160, 0.45)] + ([] if off else [(ph, 220, 0.7), ((MS[0], MS[1] - 44), 130, 0.6)])
    img = iluminar(F.finish(), F, [], glows=gl, amb=0.2, warm=AZUL)
    return img, dict(grain=10, dark=0.1 if off else 0.0)

def devuelves(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(gradient((14, 14, 18), (6, 6, 8)), dict(x=540, y=900, z=lerp(1.0, 1.12, k)))
    c = pantalla_llamada(F, t, "llamando")
    img = iluminar(F.finish(), F, [], glows=[(c, 560, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=8)

def suena(t, D, fi):
    """la cámara baja al hueco de la cama: un móvil se enciende y vibra en la oscuridad"""
    on = t > D * 0.3
    k = ease(seg(t, D * 0.25, D))
    sh = 8 * on * (1 - seg(t, D * 0.4, D * 0.7))
    F = Frame(fondo(), dict(x=lerp(460, MS[0], k) + noise(t * 30) * sh, y=lerp(PISO - 170, PISO - 70, k), z=lerp(1.7, 2.9, k),
                            sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    _cuarto(F, t)
    J, ph = tu_movil(F, t, oreja=0.0, face="scared", jit=1.5)
    manta(F)
    m = movil_suelo(F, t, on=1.0 if on else 0.0, vib=1.0 if on else 0.0)
    gl = [(ph, 200, 0.6)] + ([(m, 300, 1.0)] if on else [])
    img = iluminar(F.finish(), F, [], glows=gl, amb=0.16, warm=AZUL)
    return img, dict(grain=11, flash=((255, 255, 255), 0.5 * max(0, 1 - abs(t - D * 0.3) / 0.15)), tint=((255, 0, 30), 0.12 * on))

def coge(t, D, fi):
    """unos dedos largos y pálidos salen de la oscuridad, cogen el móvil y se lo llevan… a una cara"""
    ag = ease(seg(t, D * 0.1, D * 0.45))
    sube = ease(seg(t, D * 0.5, D * 0.85))
    F = Frame(fondo(), dict(x=lerp(MS[0], 470, sube), y=PISO - 80, z=lerp(3.0, 2.6, sube)))
    _cuarto(F, t)
    mx = lerp(MS[0], 540, sube)
    hueco_cosa(F, t, cara=sube, abre=0.3, x=470)
    m = movil_suelo(F, t, on=1.0, vib=1.0 - ag, alto=0, x=mx) if sube < 0.05 else movil_suelo(F, t, on=1.0, x=mx, alto=lerp(0, 40, sube))
    # mano: desde la derecha (oscuridad) hasta el móvil
    hx = lerp(700, mx + 30, ag); hy = MS[1] - 50 - lerp(0, 40, sube)
    F.line([(760, PISO - 30), (hx + 30, hy + 10)], PIEL, 14)
    dedos(F, (hx + 20, hy + 6), 200, n=4, L_=56, w=6)
    img = iluminar(F.finish(), F, [], glows=[(m, 260, 1.0)], amb=0.12, warm=AZUL)
    return img, dict(grain=12, tint=((255, 0, 30), 0.15 * sube))

def abajo(t, D, fi):
    """el golpe: la cara pálida bajo tu cama, iluminada por el móvil pegado a su oreja, hablando con tu voz"""
    hit = t >= D * 0.12
    sh = 14 * hit * (1 - seg(t, D * 0.3, D * 0.6))
    k = ease(seg(t, 0, D))
    cx, cy = 470, PISO - 92
    F = Frame(fondo(), dict(x=cx + 20 + noise(t * 30) * sh, y=cy - 10, z=lerp(3.3, 3.8, k), sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    _cuarto(F, t)
    hueco_cosa(F, t, cara=1.0, abre=0.3 + 0.7 * abs(math.sin(t * 7)) * (t < D * 0.8), x=cx)
    m = movil_suelo(F, t, on=1.0, x=cx + 66, alto=40)
    F.line([(cx + 160, PISO - 20), (cx + 96, PISO - 90)], PIEL, 12)
    dedos(F, (cx + 90, PISO - 92), 160, n=4, L_=40, w=5)
    img = iluminar(F.finish(), F, [], glows=[(m, 200, 1.0)], amb=0.05, warm=AZUL)
    return img, dict(grain=12, flash=((255, 255, 255), max(0, 1 - (t - D * 0.12) / 0.25)) if hit else None,
                     glitch=0.4 if hit and fi % 3 and t < D * 0.6 else 0.0, tint=((255, 0, 30), 0.25 * hit))

def espera(t, D, fi):
    """plano general: tú, encogido en la cama sin moverte; debajo, el brillo del móvil, dos ojos y los dedos en el borde"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(420, 470, k), y=lerp(PISO - 150, PISO - 230, k), z=lerp(2.0, 1.45, k)))
    _cuarto(F, t, ojos=0.7 + 0.3 * (math.sin(t * 2) > -0.7), dedos_k=1.0)
    movil_suelo(F, t, on=0.35, x=440)
    J, ph = tu_movil(F, t, oreja=0.0, face="scared", jit=2.0, luz=False)
    manta(F)
    img = iluminar(F.finish(), F, [], glows=[((440, PISO - 50), 140, 0.45), ((484, PISO - 96), 130, 0.8), ((825, PISO - 222), 160, 0.45)],
                   amb=0.26, warm=(255, 120, 120))
    return img, dict(grain=11, tint=((255, 0, 30), 0.12))

def final(t, D, fi):
    F = Frame(fondo(), dict(x=470, y=lerp(PISO - 230, PISO - 210, ease(t / D)), z=1.7))
    _cuarto(F, t, ojos=1.0, dedos_k=1.0)
    movil_suelo(F, t, on=0.6 + 0.4 * (math.sin(t * 9) > 0), vib=1.0 if t > D * 0.4 else 0.0, x=440)
    J, ph = tu_movil(F, t, oreja=0.0, face="scared", jit=2.0, luz=False)
    manta(F)
    img = iluminar(F.finish(), F, [], glows=[((440, PISO - 50), 200, 0.7), ((484, PISO - 96), 120, 0.5)], amb=0.18, warm=(255, 120, 120))
    pp = ease_back(seg(t, D * 0.5, D * 0.6)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 300, 1040, 620), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3"), 370, 64, (255, 255, 255)), (tr("TE LLAMAS TÚ…"), 450, 64, (255, 255, 255)),
                                 (tr("HAZ CASO"), 550, 120, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 650, 850, 740), 26, fill=(230, 30, 50))
        d.text((540, 695), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.25 * pp if pp > 0 else 0), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(entrante=entrante, contestas=contestas, broma=broma, devuelves=devuelves, suena=suena, coge=coge, abajo=abajo,
                 espera=espera, final=final)
PAUSA = dict(entrante=0.4, contestas=0.6, broma=0.5, devuelves=0.3, suena=0.8, coge=0.5, abajo=0.9, espera=0.6, final=2.4)
