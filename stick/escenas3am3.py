"""Si oyes esto a las 3AM — 3: "Tu compañero de piso". Piso compartido de noche: tu cuarto, el recibidor con la puerta
de la calle y el gancho de las llaves, la puerta del cuarto de tu compañero y la cosa que lo imita asomando por la puerta.
Piezas nuevas reutilizables: puerta_calle (mirilla, cerradura que gira, rendija con pies, puerta que se entreabre con
algo asomando), gancho_llaves, puerta_compi."""
import math
from PIL import ImageDraw
from motor import *
from escenas2 import big
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am, cuarto_casa, movil_msg, CASA_A, CASA_B
from escenas3am2 import cara_palida, dedos, PIEL

SUDADERA = (226, 128, 44)            # la sudadera naranja de tu compañero (la lleva la cosa)
PISO = 1300
DX0, DX1, DY0 = 580, 820, 820        # puerta de la calle (bisagra a la izquierda)
RELLANO = (255, 196, 120)
MADERA, MADERA_O = (92, 62, 44), (40, 26, 18)
LATON = (196, 168, 96)
_BG = {}
def fondo():
    if "a" not in _BG: _BG["a"] = gradient(CASA_A, CASA_B)
    return _BG["a"]

def paredes(F, col=(28, 30, 46)):
    F.rect(-900, -200, 2000, PISO, fill=col)
    F.rect(-900, PISO, 2000, 3000, fill=(14, 14, 22)); F.line([(-900, PISO), (2000, PISO)], (50, 52, 76), 6)
    F.rect(-900, PISO - 40, 2000, PISO, fill=(22, 22, 34))                                       # rodapié

def gancho_llaves(F, x=330, y=960, mias=True):
    """tabla con dos ganchos: TÚ (con tus llaves y llavero verde) y ÉL (vacío)"""
    F.rect(x - 120, y - 34, x + 120, y + 14, fill=(110, 76, 50), outline=(52, 34, 22), w=4)
    for k, (gx, lab) in enumerate(((x - 60, tr("TÚ")), (x + 60, tr("ÉL")))):
        F.line([(gx, y - 6), (gx, y + 30), (gx + 12, y + 22)], (170, 170, 176), 6)
        F.rect(gx - 34, y - 30, gx + 34, y - 10, fill=(232, 222, 196))
        F.text((gx, y - 20), lab, 17, (40, 30, 24))
        if k == 0 and mias:
            F.circle((gx, y + 44), 14, outline=(200, 200, 206), w=4)
            F.line([(gx - 6, y + 56), (gx - 16, y + 104)], (200, 196, 150), 9)
            F.line([(gx + 6, y + 56), (gx + 12, y + 96)], (190, 190, 196), 9)
            F.rect(gx + 12, y + 50, gx + 34, y + 80, fill=TU.shirt)

def puerta_calle(F, abre=0.0, gira=0.0, manilla=0.0, rellano=0.35, pies=0.0, cara=0.0, garra=0.0, brillo=0.0, t=0.0):
    """abre: 0-1 (rendija de hasta 150 px por el lado derecho); gira: giro del bombín 0-1; manilla: 0-1 hacia abajo;
    pies: sombras de dos pies en la rendija de luz de abajo; cara: la cosa asoma en la rendija; garra: dedos en el canto"""
    F.rect(DX0 - 28, DY0 - 28, DX1 + 28, PISO, fill=(46, 38, 32))
    F.rect(DX0, DY0, DX1, PISO, fill=(4, 4, 6))
    gap = 150 * ease(abre)
    if gap > 1:
        F.rect(DX1 - gap, PISO - 60, DX1, PISO, fill=tuple(int(v * 0.12) for v in RELLANO))
        if cara > 0:                                                           # la cosa: alta, con la sudadera de él
            cx = DX1 - gap * 0.42; cy = lerp(1000, 905, ease(cara))
            F.rect(cx - 60, cy + 60, cx + 70, PISO, fill=tuple(int(v * 0.5) for v in SUDADERA))
            F.poly([(cx - 60, cy + 60), (cx + 70, cy + 60), (cx + 50, cy + 10), (cx - 40, cy + 10)], fill=tuple(int(v * 0.42) for v in SUDADERA))
            cara_palida(F, (cx, cy), 46, abre=0.3 + 0.7 * ease(cara))
    ex = DX1 - gap
    F.rect(DX0, DY0, ex, PISO, fill=MADERA, outline=MADERA_O, w=5)
    w_ = ex - DX0
    for y0, y1 in ((DY0 + 40, DY0 + 210), (DY0 + 250, PISO - 40)):
        F.rect(DX0 + w_ * 0.14, y0, ex - w_ * 0.14, y1, outline=(70, 46, 32), w=5)
    if gap > 1: F.line([(ex, DY0), (ex, PISO)], (130, 96, 70), 6)              # canto iluminado
    # mirilla
    F.circle((DX0 + w_ * 0.5, 1040), 11, fill=LATON); F.circle((DX0 + w_ * 0.5, 1040), 5, fill=tuple(int(v * rellano) for v in RELLANO))
    # bombín (gira) y manilla
    bx, by = ex - 38, 1110
    F.circle((bx, by), 17, fill=LATON, outline=(110, 90, 50), w=3)
    a = math.radians(90 - 90 * gira)
    F.line([(bx - math.cos(a) * 10, by - math.sin(a) * 10), (bx + math.cos(a) * 10, by + math.sin(a) * 10)], (40, 32, 20), 5)
    if brillo > 0: F.circle((bx, by), 6 + 6 * brillo, fill=(255, 250, 220))
    mx, my = ex - 38, 1160
    F.rect(mx - 14, my - 22, mx + 14, my + 22, fill=(150, 126, 70))
    am = math.radians(35 * manilla)
    F.line([(mx, my), (mx - math.cos(am) * 70, my + math.sin(am) * 70)], LATON, 14)
    # rendija de luz del rellano bajo la puerta (cerrada)
    if gap <= 1 and rellano > 0:
        F.rect(DX0, PISO - 7, DX1, PISO, fill=tuple(int(v * rellano) for v in RELLANO))
        if pies > 0:
            for px in (650, 724):
                F.rect(px, PISO - 7, px + 48, PISO, fill=(6, 5, 4))
    if garra > 0:                                                              # dedos largos rodeando el canto
        for k, yy in enumerate((1000, 1030)):
            dedos(F, (ex + 18, yy + 30 * k), 180 + 8, n=4, L_=lerp(10, 62, ease(garra)), w=9)
    return dict(bombin=(bx, by), rendija=(DX1 - gap * 0.5, 950))

def puerta_compi(F, x=640, luz=0.8):
    F.rect(x - 150, PISO - 520, x + 150, PISO, fill=(42, 34, 30))
    F.rect(x - 124, PISO - 496, x + 124, PISO, fill=(84, 66, 52), outline=(40, 30, 24), w=5)
    F.rect(x - 76, PISO - 430, x + 40, PISO - 290, fill=(40, 60, 96), outline=(20, 24, 40), w=3)     # póster
    F.circle((x - 18, PISO - 370), 30, fill=(200, 70, 60))
    F.circle((x + 96, PISO - 250), 12, fill=LATON)
    F.rect(x - 124, PISO - 8, x + 124, PISO, fill=tuple(int(v * luz) for v in (140, 190, 255)))

# ---------- escenas ----------
def timbre(t, D, fi):
    k = ease(seg(t, 0.0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(655, 560, k), y=lerp(1070, 1020, k), z=lerp(3.2, 1.35, k)))
    cuarto_casa(F, puerta_luz=0.0)
    reloj_3am(F, 655, 1070, 0.42)
    s = ease(seg(t, D * 0.4, D * 0.6))
    TU.draw(F, mix(pose(l1u=90, l2u=90, l1l=0, l2l=0, a1u=10), pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=40, a1l=30, a2u=-20), s),
            lerp(250, 300, s), lerp(1140, 1150, s), f=1, rot=lerp(-90, 0, s), snap=False,
            face="closed" if t < D * 0.35 else ("scared" if t > D * 0.55 else "neutral"))
    rings = [D * 0.3, D * 0.5, D * 0.75]
    pul = max([math.exp(-(t - r) / 0.25) for r in rings if t >= r] + [0])
    img = F.finish()
    img = iluminar(img, F, [], glows=[((655, 1070), 260, 0.7), ((870, 1000), 300, 0.25 + 0.4 * pul)], amb=0.3, warm=(255, 120, 120))
    return img, dict(grain=9, flash=((255, 40, 40), 0.35 * (1 - seg(t, 0, 0.25))), tint=((255, 0, 30), 0.1 * pul))

def recibidor(t, D, fi):
    k = ease(seg(t, D * 0.4, D * 0.85))
    F = Frame(fondo(), dict(x=lerp(560, 330, k), y=lerp(1090, 1000, k), z=lerp(1.55, 3.0, k)))
    paredes(F)
    puerta_calle(F, rellano=0.45)
    gancho_llaves(F)
    w = ease(seg(t, 0, D * 0.45))
    x = lerp(-80, 470, w)
    TU.draw(F, walk(t, 0.6, 0.7) if w < 1 else pose(head=-10, a1u=10, a2u=-10), x, PISO, f=1 if w < 1 else -1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((700, PISO), 300, 0.6), ((390, 1000), 200, 0.55 * k + 0.2)], amb=0.24, warm=RELLANO)
    return img, dict(grain=10)

def movil(t, D, fi):
    F = Frame(gradient((14, 14, 18), (6, 6, 8)), dict(x=540, y=900, z=lerp(1.0, 1.12, ease(t / D))))
    c = movil_msg(F, t, D, tr("COMPI"), [tr("ESTOY EN MI CAMA."), tr("NO ABRAS."), tr("LLEVA UNA SEMANA"), tr("IMITÁNDOME.")])
    img = iluminar(F.finish(), F, [], glows=[(c, 560, 1.0)], amb=0.25, warm=(170, 200, 255))
    return img, dict(grain=8, tint=((255, 0, 30), 0.14 * seg(t, D * 0.6, D)))

def cuarto(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(540, 600, k), y=lerp(1060, 1110, k), z=lerp(1.5, 1.85, k)))
    paredes(F, col=(30, 30, 44))
    luz = 0.55 + 0.4 * (noise(t * 5, 2) > -0.2)
    puerta_compi(F, 760, luz=luz)
    J = TU.draw(F, add(pose(body=-4, head=-4, a1u=60, a1l=70, a2u=-10, a2l=20), jitter(t, 1.5, 3)), 430, PISO, f=1, face="scared")
    hx, hy = J["a1h"]
    F.rect(hx - 10, hy - 20, hx + 10, hy + 14, fill=(160, 200, 255))
    img = iluminar(F.finish(), F, [], glows=[((760, PISO), 240, luz * 0.9), ((hx, hy), 170, 0.6)], amb=0.22, warm=(140, 190, 255))
    return img, dict(grain=10)

def silencio(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(640, 700, k), y=lerp(1120, 1250, k), z=lerp(1.6, 3.0, k)))
    paredes(F)
    puerta_calle(F, rellano=0.75, pies=1.0)
    gancho_llaves(F)
    img = iluminar(F.finish(), F, [], glows=[((700, PISO), 320, 0.85), ((700, 1040), 120, 0.3)], amb=0.18, warm=RELLANO)
    return img, dict(grain=11, dark=0.08)

def llavero(t, D, fi):
    sh = 3 * seg(t, D * 0.3, D * 0.4) * (noise(t * 50) > 0)
    F = Frame(fondo(), dict(x=DX1 - 60, y=1120, z=lerp(2.6, 3.4, ease(t / D)), sx=noise(t * 60, 1) * sh * 4, sy=noise(t * 60, 2) * sh))
    paredes(F)
    puerta_calle(F, rellano=0.75, pies=1.0, brillo=seg(t, D * 0.62, D * 0.7) * (1 - seg(t, D * 0.7, D * 0.85)))
    img = iluminar(F.finish(), F, [], glows=[((DX1 - 38, 1110), 220, 0.75), ((700, PISO), 200, 0.6)], amb=0.18, warm=RELLANO)
    return img, dict(grain=11, tint=((255, 0, 30), 0.1 * seg(t, D * 0.6, D)))

def cerradura(t, D, fi):
    g = ease(seg(t, D * 0.08, D * 0.38)); m = ease(seg(t, D * 0.45, D * 0.6)) * (1 - 0.3 * seg(t, D * 0.62, D * 0.7))
    k = ease(seg(t, D * 0.55, D * 0.95))
    F = Frame(fondo(), dict(x=lerp(DX1 - 40, 560, k), y=lerp(1120, 1100, k), z=lerp(3.4, 1.7, k)))
    paredes(F)
    puerta_calle(F, gira=g, manilla=m, rellano=0.75, pies=1.0)
    gancho_llaves(F)
    b = ease(seg(t, D * 0.55, D))
    TU.draw(F, add(mix(pose(), SCARED, b), jitter(t, 2 * b, 4)), lerp(500, 390, b), PISO, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((DX1 - 38, 1130), 260, 0.8), ((700, PISO), 260, 0.6)], amb=0.2, warm=RELLANO)
    return img, dict(grain=12, tint=((255, 0, 30), 0.25 * g))

def asoma(t, D, fi):
    ab = seg(t, 0, D * 0.4); hit = seg(t, D * 0.3, D * 0.4)
    sh = 12 * hit * (1 - seg(t, D * 0.4, D * 0.7))
    F = Frame(fondo(), dict(x=lerp(600, 720, ease(ab)) + noise(t * 30) * sh, y=lerp(1100, 1020, ease(ab)), z=lerp(1.7, 2.3, ease(ab)),
                            sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    paredes(F)
    puerta_calle(F, abre=ab * 0.85, gira=1, rellano=0.75, cara=hit, garra=seg(t, D * 0.4, D * 0.7))
    big(TU, 0.85, F, add(SCARED, jitter(t, 3, 6)), 360, PISO, f=1, face="scared")
    golpe = hit >= 1
    img = iluminar(F.finish(), F, [], glows=[((760, 930), 220, 0.75), ((700, PISO), 260, 0.5)], amb=0.18, warm=(220, 220, 255))
    return img, dict(grain=12, flash=((255, 255, 255), max(0, 1 - (t - D * 0.4) / 0.25)) if golpe else None,
                     glitch=0.45 if golpe and fi % 3 and t < D * 0.7 else 0.0, tint=((255, 0, 30), 0.28 if golpe else 0.0))

def final(t, D, fi):
    F = Frame(fondo(), dict(x=730, y=lerp(1040, 1060, ease(t / D)), z=2.0))
    paredes(F)
    puerta_calle(F, abre=0.85 + 0.03 * math.sin(t * 1.5), gira=1, rellano=0.75, cara=1.0, garra=1.0)
    img = iluminar(F.finish(), F, [], glows=[((760, 930), 220, 0.75)], amb=0.16, warm=(220, 220, 255))
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, D * 0.5, D * 0.6)) * (1 + 0.03 * math.sin(t * 25))
    if p > 0:
        d.rounded_rectangle((60, 1040, 1020, 1330), 30, fill=(0, 0, 0))
        d.text((540, 1100), tr("SI OLVIDÓ SUS LLAVES…"), font=font(66 * p + 1), fill=(255, 255, 255), anchor="mm", stroke_width=int(8 * p), stroke_fill=(0, 0, 0))
        d.text((540, 1210), tr("NO ABRAS"), font=font(150 * p + 1), fill=(255, 40, 50), anchor="mm", stroke_width=int(14 * p), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 1350, 850, 1450), 26, fill=(230, 30, 50))
        d.text((540, 1400), tr("SÍGUEME PARA MÁS"), font=font(52), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=10, tint=((255, 0, 30), 0.25 * p if p > 0 else 0), glitch=0.3 if p > 0 and fi % 5 == 0 else 0.0)

ESCENA_FN = dict(timbre=timbre, recibidor=recibidor, movil=movil, cuarto=cuarto, silencio=silencio, llavero=llavero,
                 cerradura=cerradura, asoma=asoma, final=final)
PAUSA = dict(timbre=0.4, recibidor=0.5, movil=1.0, cuarto=0.4, silencio=0.9, llavero=0.9, cerradura=0.8, asoma=0.9, final=2.4)
