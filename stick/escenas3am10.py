"""Si oyes esto a las 3AM — 10: "El ascensor". Edificio de noche: el panel del ascensor (botones hasta el 12, pantalla en 13),
la cabina vista desde dentro con las puertas abriéndose a un pasillo en perspectiva, el rellano de la planta 13 (ascensor a la
izquierda, tu puerta 12B con felpudo a la derecha) y la copia: tú mismo, de espaldas, con tu sudadera y tu llavero verde.
Piezas nuevas reutilizables: panel_ascensor, cabina (vista desde dentro), pasillo_fuga (pasillo en perspectiva),
rellano (ascensor + puerta de piso), puertas_ascensor, copia (tú, de espaldas o de frente) y cara_sonrisa (tu cara con una
sonrisa demasiado ancha)."""
import math, random
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, CASA_A, CASA_B
from escenas3am5 import _osc

PISO = 1300
ACERO, ACERO_O = (112, 116, 124), (50, 52, 58)
ROJO = (255, 40, 40)
TUBO = (190, 220, 255)               # fluorescente frío
LATON = (196, 168, 96)
COPIA = Fig(shirt=TU.shirt, scale=TU.scale)          # tú. Igual que tú
EX0, EX1, EY0 = 70, 390, 790         # hueco del ascensor en el rellano
PX0, PX1, PY0 = 640, 880, 830        # tu puerta (12B)
_BG = {}
def fondo(k="a"):
    if k not in _BG: _BG[k] = gradient(CASA_A, CASA_B) if k == "a" else gradient((20, 20, 24), (8, 8, 10))
    return _BG[k]

def parpadeo(t, seed=1, base=0.85):
    """fluorescente que falla"""
    return base + (1 - base) * (noise(t * 5, seed) > -0.2) - 0.6 * (noise(t * 13, seed + 7) > 0.82)

def pantalla(F, cx, cy, s, txt="13", flecha=1, on=1.0):
    F.rect(cx - 90 * s, cy - 50 * s, cx + 90 * s, cy + 50 * s, fill=(6, 4, 4), outline=(40, 40, 46), w=5 * s)
    col = _osc(ROJO, on)
    F.text((cx + 22 * s, cy + 4 * s), txt, 78 * s, col, stroke=2 * s, scol=(90, 0, 0))
    if flecha:
        ax, ay = cx - 52 * s, cy
        if flecha > 0: F.poly([(ax - 16 * s, ay + 12 * s), (ax + 16 * s, ay + 12 * s), (ax, ay - 16 * s)], fill=col)
        else: F.poly([(ax - 16 * s, ay - 12 * s), (ax + 16 * s, ay - 12 * s), (ax, ay + 16 * s)], fill=col)

def panel_ascensor(F, t, num="13", luz12=1.0):
    """placa de acero con la pantalla arriba y los botones del 1 al 12 (no hay 13). El 12 está pulsado"""
    F.rect(330, 280, 750, 1520, fill=ACERO, outline=ACERO_O, w=8)
    for y in range(300, 1520, 26): F.line([(340, y), (740, y + 4)], _osc(ACERO, 1.06), 2)        # cepillado
    pantalla(F, 540, 450, 1.6, num, flecha=1, on=0.85 + 0.15 * (math.sin(t * 9) > -0.6))
    for i in range(12):
        n = i + 1; col = i % 2; row = i // 2
        bx = 450 + col * 180; by = 1400 - row * 130
        lit = n == 12
        F.circle((bx, by), 48, fill=(70, 72, 78), outline=(40, 40, 44), w=4)
        F.circle((bx, by), 38, fill=_osc((255, 170, 60), 0.4 + 0.6 * luz12) if lit else (150, 154, 160))
        F.text((bx, by + 2), str(n), 34, (40, 24, 6) if lit else (40, 42, 48))
    F.rect(380, 1460, 700, 1500, fill=(70, 72, 78)); F.text((540, 1480), tr("PLANTAS 1-12"), 22, (190, 192, 198))

def pasillo_fuga(F, cx, cy, x0, y0, x1, y1, t, figura=0.0, luz=1.0):
    """pasillo en perspectiva visto por un hueco (x0..x1, y0..y1) con punto de fuga (cx, cy)"""
    vw, vh = 70, 90                                                                                  # pared del fondo
    F.rect(x0, y0, x1, y1, fill=_osc((44, 42, 40), luz))
    F.poly([(x0, y1), (x1, y1), (cx + vw, cy + vh), (cx - vw, cy + vh)], fill=_osc((52, 30, 30), luz))   # moqueta
    F.poly([(x0, y0), (x1, y0), (cx + vw, cy - vh), (cx - vw, cy - vh)], fill=_osc((30, 30, 32), luz))   # techo
    F.poly([(x0, y0), (cx - vw, cy - vh), (cx - vw, cy + vh), (x0, y1)], fill=_osc((58, 56, 52), luz))   # pared izq
    F.poly([(x1, y0), (cx + vw, cy - vh), (cx + vw, cy + vh), (x1, y1)], fill=_osc((50, 48, 46), luz))   # pared dcha
    F.rect(cx - vw, cy - vh, cx + vw, cy + vh, fill=_osc((36, 34, 34), luz))
    for k, u in enumerate((0.25, 0.55, 0.8)):                                                         # tubos del techo
        a = lerp(0, 1, u)
        yy = lerp(y0, cy - vh, a); ww = lerp((x1 - x0) * 0.2, vw * 0.5, a)
        on = parpadeo(t + k * 1.3, 3 + k)
        F.rect(cx - ww, yy + 2, cx + ww, yy + 8 + 10 * (1 - a), fill=_osc(TUBO, max(0.15, on) * luz))
    for s_ in (-1, 1):                                                                                # puertas laterales
        for u in (0.35, 0.68):
            xa = lerp(x0 if s_ < 0 else x1, cx + s_ * vw, u); xb = lerp(x0 if s_ < 0 else x1, cx + s_ * vw, u + 0.12)
            ya0 = lerp(y0, cy - vh, u) + (lerp(y1, cy + vh, u) - lerp(y0, cy - vh, u)) * 0.3
            yb0 = lerp(y0, cy - vh, u + 0.12) + (lerp(y1, cy + vh, u + 0.12) - lerp(y0, cy - vh, u + 0.12)) * 0.3
            F.poly([(xa, ya0), (xb, yb0), (xb, lerp(y1, cy + vh, u + 0.12)), (xa, lerp(y1, cy + vh, u))], fill=_osc((70, 48, 36), luz))
    # al fondo, tu puerta… y alguien delante
    F.rect(cx - 30, cy - 50, cx + 30, cy + vh, fill=_osc((92, 62, 44), luz))
    if figura > 0:
        F.rect(cx - 9, cy - 10, cx + 9, cy + vh - 2, fill=_osc(TU.shirt, 0.6 * figura))
        F.circle((cx, cy - 20), 11, fill=_osc((230, 230, 230), 0.8 * figura))

def cabina(F, t, abre=1.0, figura=0.0, luz=1.0, num="13"):
    """interior del ascensor visto desde dentro, mirando a las puertas"""
    ox0, ox1, oy0, oy1 = 300, 780, 560, 1400
    gap = (ox1 - ox0) / 2 * ease(abre)
    pasillo_fuga(F, 540, 940, ox0, oy0, ox1, oy1, t, figura=figura, luz=luz)
    F.poly([(-400, -300), (ox0, oy0), (ox0, oy1), (-400, 2300)], fill=(84, 88, 96))                  # pared izq
    F.poly([(1480, -300), (ox1, oy0), (ox1, oy1), (1480, 2300)], fill=(76, 80, 88))                  # pared dcha
    F.poly([(-400, -300), (1480, -300), (ox1, oy0), (ox0, oy0)], fill=(54, 56, 62))                  # techo
    F.poly([(-400, 2300), (1480, 2300), (ox1, oy1), (ox0, oy1)], fill=(40, 40, 44))                  # suelo
    F.rect(ox0 - 30, 330, ox1 + 30, oy0, fill=(96, 100, 108))                                         # frente sobre las puertas
    pantalla(F, 540, 450, 1.0, num, flecha=0 if abre > 0 else 1)
    F.rect(ox0, oy0, ox0 + (ox1 - ox0) / 2 - gap, oy1, fill=ACERO, outline=ACERO_O, w=5)
    F.rect(ox0 + (ox1 - ox0) / 2 + gap, oy0, ox1, oy1, fill=ACERO, outline=ACERO_O, w=5)
    F.rect(ox0 - 12, oy0 - 12, ox1 + 12, oy1, outline=(60, 62, 68), w=12)
    F.poly([(860, 760), (960, 720), (960, 1060), (860, 1080)], fill=(96, 100, 108))                    # panel lateral
    for i in range(6):
        F.circle((910, 790 + i * 44), 12, fill=(255, 170, 60) if i == 0 else (150, 154, 160))

def puertas_ascensor(F, t, abre=0.0, num="13", flecha=0, interior=None):
    """el ascensor visto desde el rellano. interior(F) dibuja lo que hay dentro de la cabina"""
    F.rect(EX0 - 40, EY0 - 150, EX1 + 40, PISO, fill=(70, 72, 78))
    F.rect(EX0, EY0, EX1, PISO, fill=(150, 146, 130))                                                  # cabina iluminada
    F.rect(EX0, PISO - 30, EX1, PISO, fill=(90, 88, 80))
    if interior: interior(F)
    gap = (EX1 - EX0) / 2 * ease(abre)
    mid = (EX0 + EX1) / 2
    F.rect(EX0, EY0, mid - gap, PISO, fill=ACERO, outline=ACERO_O, w=5)
    F.rect(mid + gap, EY0, EX1, PISO, fill=ACERO, outline=ACERO_O, w=5)
    F.rect(EX0 - 14, EY0 - 14, EX1 + 14, PISO, outline=(46, 46, 50), w=14)
    pantalla(F, mid, EY0 - 80, 0.75, num, flecha=flecha)
    F.circle((EX1 + 70, 1060), 18, fill=(60, 62, 68)); F.circle((EX1 + 70, 1060), 11, fill=(150, 154, 160))   # botón de llamada

def rellano(F, t, luz=1.0, abre=0.0, num="13", flecha=0, interior=None):
    """rellano de la planta 13: idéntico al tuyo"""
    F.rect(-900, -200, 2000, PISO, fill=_osc((40, 40, 50), luz))
    F.rect(-900, PISO, 2000, 3000, fill=_osc((40, 22, 24), luz)); F.line([(-900, PISO), (2000, PISO)], (60, 40, 40), 6)
    F.rect(-900, PISO - 40, 2000, PISO, fill=_osc((26, 24, 30), luz))
    on = parpadeo(t, 5)
    F.rect(360, 560, 720, 584, fill=_osc(TUBO, max(0.12, on)))                                         # tubo
    F.rect(340, 548, 740, 560, fill=(60, 60, 66))
    F.text((210, 640), tr("PLANTA 13"), 34, _osc((200, 200, 210), 0.7 * luz))
    puertas_ascensor(F, t, abre, num, flecha, interior)
    # tu puerta
    F.rect(PX0 - 28, PY0 - 28, PX1 + 28, PISO, fill=(46, 38, 32))
    F.rect(PX0, PY0, PX1, PISO, fill=(92, 62, 44), outline=(40, 26, 18), w=5)
    for y0, y1 in ((PY0 + 40, PY0 + 200), (PY0 + 240, PISO - 40)):
        F.rect(PX0 + 34, y0, PX1 - 34, y1, outline=(70, 46, 32), w=5)
    F.rect(PX0 + 80, PY0 - 4 + 70, PX1 - 80, PY0 + 116, fill=LATON); F.text(((PX0 + PX1) / 2, PY0 + 94), "12B", 34, (40, 30, 20))
    F.circle(((PX0 + PX1) / 2, 1030), 10, fill=LATON)
    F.circle((PX0 + 40, 1110), 16, fill=LATON, outline=(110, 90, 50), w=3)                            # bombín
    F.rect(PX0 + 26, 1140, PX0 + 54, 1184, fill=(150, 126, 70)); F.line([(PX0 + 40, 1160), (PX0 + 106, 1160)], LATON, 13)
    F.poly([(PX0 - 10, PISO + 6), (PX1 + 10, PISO + 6), (PX1 + 40, PISO + 46), (PX0 - 40, PISO + 46)], fill=(120, 84, 50))   # felpudo
    F.text(((PX0 + PX1) / 2, PISO + 27), tr("HOLA"), 26, (70, 44, 24))

def llavero(F, c, s=1.0):
    x, y = c
    F.circle((x, y), 11 * s, outline=(200, 200, 206), w=4 * s)
    F.line([(x - 4 * s, y + 10 * s), (x - 12 * s, y + 46 * s)], (200, 196, 150), 8 * s)
    F.line([(x + 6 * s, y + 10 * s), (x + 10 * s, y + 40 * s)], (190, 190, 196), 8 * s)
    F.rect(x + 10 * s, y + 6 * s, x + 30 * s, y + 34 * s, fill=TU.shirt, outline=(20, 60, 50), w=2 * s)   # tu llavero verde

def cara_sonrisa(F, c, r, abre=0.0, sonrisa=1.0, t=0.0):
    """tu cara redonda… con los ojos muy abiertos y fijos y una sonrisa demasiado ancha, llena de dientes"""
    hx, hy = c
    F.circle((hx, hy), r + r * 0.1, fill=(8, 8, 12))
    F.circle((hx, hy), r, fill=(214, 212, 206))
    F.ellipse((hx, hy + r * 0.62), r * 0.8, r * 0.3, fill=(186, 184, 178))
    for dx in (-0.36, 0.36):                                                                          # ojos: abiertos de más, ojeras, pupila diminuta
        F.ellipse((hx + dx * r, hy - r * 0.2), r * 0.27, r * 0.3, fill=(150, 146, 146))
        F.circle((hx + dx * r, hy - r * 0.22), r * 0.2, fill=(244, 240, 232), outline=(20, 22, 30), w=r * 0.035)
        F.circle((hx + dx * r + noise(t * 3, 4) * r * 0.015, hy - r * 0.22), r * 0.045, fill=(4, 4, 6))
        F.line([(hx + dx * r - r * 0.18, hy - r * 0.5), (hx + dx * r + r * 0.18, hy - r * 0.5)], (120, 116, 112), r * 0.035)   # cejas planas
    w_ = r * lerp(0.35, 0.98, sonrisa); hh = r * lerp(0.06, 0.34, sonrisa) * (1 + 0.4 * abre)
    my = hy + r * 0.3; cu = r * 0.42 * sonrisa                                                        # cuánto suben las comisuras
    xs = [i / 20 for i in range(-20, 21)]
    up = [(hx + w_ * u, my - cu * u * u - hh * 0.15 * (1 - u * u)) for u in xs]
    dn = [(hx + w_ * u, my - cu * u * u + hh * (1 - u * u) ** 0.8) for u in reversed(xs)]
    F.poly(up + dn, fill=(30, 6, 10))
    if sonrisa > 0.4:                                                                                 # dientes: dos filas apretadas
        n = 15
        for i in range(n):
            u0 = -0.92 + 1.84 * i / n; u1 = u0 + 1.84 / n * 0.86
            for fila in (0, 1):
                pts = []
                for u in (u0, u1):
                    yt = my - cu * u * u - hh * 0.15 * (1 - u * u)
                    yb = my - cu * u * u + hh * (1 - u * u) ** 0.8
                    if fila == 0: pts += [(hx + w_ * u, yt), (hx + w_ * u, yt + (yb - yt) * 0.42)]
                    else: pts += [(hx + w_ * u, yb - (yb - yt) * 0.36), (hx + w_ * u, yb)]
                F.poly([pts[0], pts[2], pts[3], pts[1]], fill=(232, 226, 204) if fila == 0 else (214, 206, 186))
    for s_ in (-1, 1):                                                                                # pliegues de las mejillas, tirantes
        F.arc((hx + s_ * w_ * 0.98, my - cu - r * 0.02), r * 0.16, 200 if s_ < 0 else 250, 290 if s_ < 0 else 340, (110, 106, 102), r * 0.035)

def copia(F, p, x, y, t=0.0, f=1, espalda=True, cara=None, llaves=False):
    """tú. De espaldas: cabeza sin cara y la capucha verde caída en la nuca. De frente: cara_sonrisa"""
    J = COPIA.draw(F, p, x, y, f=f, face="closed", t=t)
    hx, hy = J["head"]; r = L["head"] * COPIA.scale
    sx, sy = J["sh"]
    F.ellipse((sx, sy + 2), r * 0.95, r * 0.42, fill=_osc(TU.shirt, 0.75))                              # capucha caída
    if espalda:
        F.circle((hx, hy), r, fill=COPIA.limb)
        F.circle((hx, hy), r * 0.96, fill=_osc(COPIA.limb, 0.93))
    elif cara is not None:
        cara_sonrisa(F, (hx, hy), r * 1.02, **cara)
    if llaves: llavero(F, (J["a1h"][0] + f * 6, J["a1h"][1] - 4), 0.9)
    return J

_QUIETA = pose(body=-2, head=-4, a1u=70, a1l=40, a2u=-6, a2l=4, l1u=4, l1l=-2, l2u=-4, l2l=-2)
_FRENTE = pose(body=0, head=0, a1u=8, a1l=4, a2u=-8, a2l=4, l1u=5, l1l=-2, l2u=-5, l2l=-2)

# ---------- escenas ----------
def panel(t, D, fi):
    """primer fotograma: la pantalla del ascensor marca 13 en rojo, muy cerca. Al alejarnos, los botones solo llegan al 12"""
    k = ease(seg(t, D * 0.1, D * 0.85))
    F = Frame(fondo("b"), dict(x=540, y=lerp(450, 860, k), z=lerp(2.6, 1.05, k), sx=noise(t * 30, 1) * 3, sy=noise(t * 30, 2) * 3))
    F.rect(-600, -400, 1700, 2400, fill=(84, 88, 96))
    panel_ascensor(F, t)
    img = iluminar(F.finish(), F, [], glows=[((540, 450), 300, 0.95), ((630, 690), 120, 0.6), ((540, 900), 600, 0.4)],
                   amb=0.3, warm=(255, 120, 120))
    return img, dict(grain=9, flash=(ROJO, 0.4 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.1))

def abre(t, D, fi):
    """desde dentro de la cabina: las puertas se abren a un pasillo largo; al fondo, alguien frente a una puerta"""
    a = ease(seg(t, D * 0.05, D * 0.6))
    k = ease(seg(t, D * 0.3, D))
    F = Frame(fondo(), dict(x=540, y=lerp(900, 930, k), z=lerp(1.0, 1.35, k)))
    on = parpadeo(t, 2)
    cabina(F, t, abre=a, figura=seg(t, D * 0.55, D * 0.8), luz=max(0.35, on))
    img = iluminar(F.finish(), F, [], glows=[((540, 940), 330 * a, 0.7 * max(0.3, on)), ((540, 450), 110, 0.7), ((540, 1400), 500, 0.25)],
                   amb=0.26, warm=TUBO)
    return img, dict(grain=10)

def puerta(t, D, fi):
    """el rellano de la 13: tu felpudo, tu 12B… y alguien de espaldas, quieto, frente a tu puerta"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(420, 700, k), y=lerp(1000, 1020, k), z=lerp(1.1, 1.5, k)))
    rellano(F, t, abre=1.0, interior=lambda F: TU.draw(F, pose(head=6, a1u=10, a1l=10, a2u=-10, a2l=10), 230, PISO - 4, f=1,
                                                        face="scared" if t > D * 0.6 else "neutral"))
    J = copia(F, _QUIETA, 790, PISO, t=t, f=-1)
    on = parpadeo(t, 5)
    img = iluminar(F.finish(), F, [], glows=[((540, 600), 520, 0.6 * max(0.2, on)), (J["head"], 160, 0.4), ((230, 1050), 220, 0.5)],
                   amb=0.2, warm=TUBO)
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * seg(t, D * 0.6, D)))

def llaves(t, D, fi):
    """primer plano de su espalda: sudadera verde, la capucha caída… y en la mano, tu llavero verde en tu cerradura"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(760, 720, k), y=lerp(1000, 1080, k), z=lerp(2.2, 2.9, k)))
    rellano(F, t)
    p = dict(_QUIETA); p["a1u"] = 64 + 4 * math.sin(t * 7) * seg(t, D * 0.5, D); p["a1l"] = 44
    copia(F, p, 790, PISO, t=t, f=-1, llaves=True)
    img = iluminar(F.finish(), F, [], glows=[((PX0 + 40, 1110), 150, 0.7), ((780, 960), 240, 0.45)], amb=0.24, warm=TUBO)
    return img, dict(grain=10)

def sales(t, D, fi):
    """sales del ascensor despacio. Él deja de mover la llave… y empieza a girarse"""
    w = ease(seg(t, 0, D * 0.6))
    gira = seg(t, D * 0.7, D * 0.95)
    F = Frame(fondo(), dict(x=lerp(400, 560, w), y=1010, z=1.25))
    rellano(F, t, abre=1.0)
    x = lerp(230, 470, w)
    TU.draw(F, walk(t, 0.45, 0.6) if w < 1 else pose(body=-4, head=6, a1u=30, a1l=40, a2u=-20, a2l=30), x, PISO, f=1,
            face="neutral" if w < 1 else "scared")
    p = dict(_QUIETA); p["a1u"] = lerp(64, 8, gira); p["a1l"] = lerp(44, 4, gira)
    copia(F, p, 790, PISO, t=t, f=-1 if gira < 0.5 else 1, espalda=gira < 0.85, cara=None)
    on = parpadeo(t, 5)
    img = iluminar(F.finish(), F, [], glows=[((540, 600), 520, 0.6 * max(0.2, on)), ((x, 1100), 200, 0.35)], amb=0.2, warm=TUBO)
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * gira), dark=0.1 * gira)

def cara(t, D, fi):
    """el golpe: tu propia cara, muy cerca, con una sonrisa que se va estirando de oreja a oreja"""
    hit = t >= D * 0.05
    J0 = COPIA.joints(_FRENTE, 790, PISO, f=1)
    hx, hy = J0["head"]
    sh = 12 * hit * (1 - seg(t, D * 0.2, D * 0.5))
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=hx + noise(t * 30) * sh, y=hy + 8, z=lerp(6.4, 7.6, k), sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    rellano(F, t)
    copia(F, _FRENTE, 790, PISO, t=t, f=1, espalda=False, cara=dict(sonrisa=lerp(0.45, 1.0, ease(seg(t, D * 0.15, D * 0.8))), t=t))
    img = iluminar(F.finish(), F, [], glows=[((hx, hy + 6), 75, 0.95)], amb=0.06, warm=TUBO)
    return img, dict(grain=12, flash=((255, 255, 255), max(0, 1 - (t - D * 0.05) / 0.25)) if hit else None,
                     glitch=0.35 if hit and fi % 3 and t < D * 0.4 else 0.0, tint=((255, 0, 30), 0.2 * hit), dark=0.12)

def voz(t, D, fi):
    """pasa a tu lado sin dejar de sonreír, entra en el ascensor y se despide con la mano"""
    m = ease(seg(t, 0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(520, 300, m), y=lerp(1010, 1020, m), z=lerp(1.25, 1.6, m) + 0.8 * ease(seg(t, D * 0.45, D))))
    rellano(F, t, abre=1.0 - 0.25 * seg(t, D * 0.8, D))
    TU.draw(F, add(pose(body=-6, head=8, a1u=40, a1l=60, a2u=-30, a2l=50), jitter(t, 1.5, 8)), 470, PISO, f=-1 if m > 0.5 else 1, face="scared")
    if m < 1:
        x = lerp(790, 230, m)
        J = copia(F, add(walk(t, 0.6, 0.9), dict(head=0)), x, PISO, t=t, f=-1, espalda=False,
                  cara=dict(sonrisa=1.0, abre=0.0, t=t))
    else:
        p = dict(_FRENTE); p["a1u"] = 150 + 18 * math.sin(t * 7); p["a1l"] = 20
        J = copia(F, p, 230, PISO - 4, t=t, f=1, espalda=False, cara=dict(sonrisa=1.0, abre=abs(math.sin(t * 6)) * (t < D * 0.85), t=t))
    img = iluminar(F.finish(), F, [], glows=[(J["head"], 200, 0.7), ((230, 1050), 240, 0.5)], amb=0.18, warm=TUBO)
    return img, dict(grain=11, tint=((255, 0, 30), 0.1))

def cierra(t, D, fi):
    """las puertas se cierran con su sonrisa en la rendija; la pantalla baja a 12. Tú golpeas el acero, solo, en la 13"""
    c = ease(seg(t, 0, D * 0.4))
    baja = t > D * 0.55
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(260, 330, k), y=lerp(1000, 960, k), z=lerp(1.9, 1.5, k)))
    def dentro(F):
        p = dict(_FRENTE); p["a1u"] = 150 + 18 * math.sin(t * 7); p["a1l"] = 20
        copia(F, p, 230, PISO - 4, t=t, f=1, espalda=False, cara=dict(sonrisa=1.0, t=t))
    rellano(F, t, abre=0.75 * (1 - c), num="12" if baja else "13", flecha=-1 if baja else 0, interior=dentro)
    gol = (t > D * 0.4) * abs(math.sin(t * 9))
    TU.draw(F, pose(body=-10, head=-6, a1u=100 + 30 * gol, a1l=20, a2u=90 + 30 * gol, a2l=30, l1u=14, l1l=-6, l2u=-10, l2l=-4),
            430, PISO, f=-1, face="scared")
    on = parpadeo(t, 5)
    img = iluminar(F.finish(), F, [], glows=[((230, 1000), 260 * (1 - c) + 40, 0.6), ((230, EY0 - 80), 100, 0.7), ((540, 600), 480, 0.4 * max(0.2, on))],
                   amb=0.16, warm=TUBO)
    return img, dict(grain=11, tint=((255, 0, 30), 0.18 * baja), flash=(ROJO, 0.3 * (1 - seg(t, D * 0.55, D * 0.7))) if baja else None)

def final(t, D, fi):
    """plano fijo del rellano de la 13: tú solo frente al ascensor cerrado, la luz falla. Y la regla"""
    F = Frame(fondo(), dict(x=520, y=lerp(1000, 990, ease(t / D)), z=1.15))
    luz = 0.75 + 0.25 * (noise(t * 6, 7) > -0.5)
    rellano(F, t, luz=luz, num="1", flecha=-1)
    TU.draw(F, add(pose(body=-6, head=10, a1u=20, a1l=30, a2u=-20, a2l=30), jitter(t, 1.2, 8)), 460, PISO, f=-1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((540, 600), 480, 0.5 * luz), ((230, EY0 - 80), 90, 0.7)], amb=0.18, warm=TUBO)
    pp = ease_back(seg(t, D * 0.5, D * 0.6)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 180, 1040, 600), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 EL ASCENSOR"), 240, 62, (255, 255, 255)), (tr("PARA EN LA 13…"), 315, 62, (255, 255, 255)),
                                 (tr("NO"), 420, 104, (255, 40, 50)), (tr("SALGAS"), 525, 104, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 625, 850, 715), 26, fill=(230, 30, 50))
        d.text((540, 670), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.25 * pp if pp > 0 else 0), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(panel=panel, abre=abre, puerta=puerta, llaves=llaves, sales=sales, cara=cara, voz=voz, cierra=cierra, final=final)
PAUSA = dict(panel=0.5, abre=0.4, puerta=0.6, llaves=0.6, sales=0.6, cara=0.8, voz=0.6, cierra=0.7, final=2.4)
