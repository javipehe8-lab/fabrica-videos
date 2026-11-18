"""Si oyes esto a las 3AM — 19: "La llamada de la abuela". El salón de casa (sofá, tele) con tu padre dormido a tu lado,
y la cocina de la abuela (azulejos, nevera abierta) con un hombre de espaldas que lleva el mismo jersey mostaza.
Piezas nuevas reutilizables: PAPA + papa() (padre con jersey mostaza; dormido, con los ojos abiertos de golpe o de espaldas),
ABU + abuela() (anciana con moño gris, gafas y teléfono inalámbrico), cocina_abuela, entrante (pantalla de llamada entrante
con cualquier nombre)."""
import math
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU
from escenas3am7 import salon_casa, llamada, SOFA, TELE
from escenas3am3 import PISO
from escenas3am5 import _osc

ROJO = (255, 40, 40)
MOSTAZA = (192, 140, 48)
PIEL_P = (228, 214, 200)
PELO_P = (52, 40, 32)
NEVERA = (200, 226, 255)
BOMBILLA = (255, 214, 150)
PAPA = Fig(shirt=MOSTAZA, limb=PIEL_P, scale=1.0)
ABU = Fig(shirt=(112, 86, 124), limb=(238, 226, 214), scale=0.92, extra=("bun",))
_BG = {}
def fondo(k="a"):
    if k not in _BG: _BG[k] = gradient((16, 16, 26), (6, 6, 10)) if k == "a" else gradient((30, 28, 24), (10, 9, 8))
    return _BG[k]

# ---------- piezas ----------
TU_X, PAPA_X = SOFA[0] + 110, SOFA[0] + 280
DORMIDO = pose(body=-14, head=-26, l1u=90, l1l=-90, l2u=84, l2l=-88, a1u=18, a1l=40, a2u=-8, a2l=36)

def cara_papa(F, c, r, ojos=0.0, boca=0.25, habla=0.0, f=1, gris=0.0):
    """cara del padre dibujada encima de la cabeza. ojos 0: cerrados (dormido); 1: abiertos de golpe, negros, con una pupila de alfiler"""
    hx, hy = c
    piel = tuple(int(lerp(a, b, gris)) for a, b in zip(PIEL_P, (196, 196, 198)))
    F.circle((hx, hy), r, fill=piel)
    F.d.chord([*F.P(hx - r - 2, hy - r - 3), *F.P(hx + r + 2, hy + r * 0.2)], 180, 360, fill=PELO_P)          # pelo corto
    ex = f * r * 0.22
    for dx in (-0.32, 0.36):
        cx_, cy_ = hx + ex + dx * r, hy - r * 0.1
        if ojos <= 0.05:
            F.line([(cx_ - r * 0.15, cy_), (cx_ + r * 0.15, cy_)], (24, 22, 26), r * 0.1)
        else:
            F.ellipse((cx_, cy_), r * 0.27, r * 0.33 * ojos, fill=_osc(piel, 0.62))                          # ojeras
            F.ellipse((cx_, cy_), r * 0.17, r * 0.27 * ojos, fill=(2, 2, 4))
            if ojos > 0.8: F.circle((cx_ + r * 0.03, cy_ - r * 0.04), r * 0.03, fill=(255, 255, 255))
    if ojos > 0.5 and habla < 0.05:                                                                             # despierto: boca recta, sin expresión
        F.line([(hx + ex - r * 0.2, hy + r * 0.52), (hx + ex + r * 0.2, hy + r * 0.52)], (14, 8, 10), r * 0.07)
    else:
        o = r * (0.06 + 0.12 * boca + 0.2 * habla)
        F.ellipse((hx + ex, hy + r * 0.5), r * 0.14, o, fill=(14, 8, 10))                                           # boca entreabierta

def papa(F, p, x, y, t=0.0, f=1, sc=1.0, ojos=0.0, boca=0.25, habla=0.0, espalda=False, gris=0.0, rot=0.0, snap=True, sombra=False):
    old = PAPA.scale; PAPA.scale = sc
    J = PAPA.draw(F, p, x, y, f=f, face="closed", t=t, rot=rot, snap=snap)
    PAPA.scale = old
    r = L["head"] * sc
    if sombra:                                                                                                  # contraluz: cara en sombra
        F.circle(J["head"], r, fill=(46, 40, 36))
        F.d.chord([*F.P(J["head"][0] - r - 2, J["head"][1] - r - 3), *F.P(J["head"][0] + r + 2, J["head"][1] + r * 0.2)], 180, 360, fill=PELO_P)
        F.ellipse((J["head"][0] + f * r * 0.22, J["head"][1] + r * 0.5), r * 0.14, r * (0.06 + 0.25 * habla), fill=(10, 6, 8))
    elif espalda:
        F.circle(J["head"], r + 1, fill=PELO_P)                                                                 # de espaldas: solo pelo
        F.ellipse((J["head"][0] - f * r * 0.9, J["head"][1] + r * 0.1), r * 0.16, r * 0.3, fill=PIEL_P)        # oreja
    else:
        cara_papa(F, J["head"], r, ojos=ojos, boca=boca, habla=habla, f=f, gris=gris)
    return J

def abuela(F, p, x, y, t=0.0, f=1, sc=0.92, face="scared", tel=True):
    old = ABU.scale; ABU.scale = sc
    J = ABU.draw(F, p, x, y, f=f, face=face, t=t)
    ABU.scale = old
    hx, hy = J["head"]; r = L["head"] * sc
    for dx in (-9, 11):                                                                                         # gafas
        F.circle((hx + f * 9 * sc + dx * sc, hy - 5 * sc), 10 * sc, outline=(150, 130, 90), w=2.5 * sc)
    if tel:
        mx, my = J["a1h"]
        F.rect(mx - 9 * sc, my - 40 * sc, mx + 9 * sc, my + 10 * sc, fill=(40, 40, 46), outline=(90, 90, 96), w=2 * sc)
        F.circle((mx, my - 30 * sc), 3 * sc, fill=(120, 230, 150))
    return J

TEL_ABU = pose(body=4, head=6, a1u=150, a1l=150, a2u=40, a2l=110)          # teléfono en la oreja y la otra mano en la boca

def cocina_abuela(F, t, nevera=1.0):
    """cocina de la abuela: azulejos, ventana negra con visillo, nevera abierta al fondo a la derecha"""
    F.rect(-900, -200, 2000, PISO, fill=(70, 66, 52))
    for i in range(-20, 40):                                                                                    # azulejos
        F.line([(i * 70, 560), (i * 70, PISO)], (58, 54, 42), 3)
    for j in range(560, PISO, 70): F.line([(-900, j), (2000, j)], (58, 54, 42), 3)
    F.rect(-900, PISO, 2000, 3000, fill=(30, 26, 22))
    for i in range(-10, 26):                                                                                    # suelo a cuadros
        for j in range(4):
            if (i + j) % 2: F.rect(i * 90, PISO + j * 90, i * 90 + 90, PISO + j * 90 + 90, fill=(46, 40, 34))
    F.rect(-900, PISO - 360, 520, PISO - 330, fill=(110, 96, 80))                                               # encimera
    F.rect(-900, PISO - 330, 520, PISO, fill=(84, 64, 50), outline=(40, 30, 24), w=4)
    for xx in (-120, 160, 440): F.circle((xx, PISO - 300), 8, fill=(170, 150, 110))
    F.rect(60, 300, 380, 640, fill=(4, 6, 12), outline=(110, 96, 80), w=14)                                     # ventana negra
    F.line([(220, 300), (220, 640)], (110, 96, 80), 8)
    F.poly([(60, 300), (170, 300), (120, 520), (60, 560)], fill=(200, 196, 180))                                # visillo
    F.poly([(380, 300), (270, 300), (320, 520), (380, 560)], fill=(200, 196, 180))
    F.line([(720, 140), (720, 300)], (40, 40, 40), 3); F.circle((720, 320), 22, fill=_osc(BOMBILLA, 0.5 + 0.5 * nevera))  # bombilla
    # nevera abierta
    F.rect(860, PISO - 760, 1160, PISO, fill=(214, 214, 206), outline=(90, 90, 86), w=5)
    F.rect(880, PISO - 740, 1140, PISO - 20, fill=_osc(NEVERA, 0.85 * nevera))
    for yy in (PISO - 560, PISO - 380, PISO - 200): F.line([(880, yy), (1140, yy)], (150, 170, 190), 6)
    F.poly([(1160, PISO - 760), (1300, PISO - 800), (1300, PISO + 30), (1160, PISO)], fill=(190, 190, 184), outline=(90, 90, 86), w=5)  # puerta

def entrante(F, t, quien, cx=540, cy=900, vib=0.0):
    """móvil a pantalla completa con una llamada entrante de 'quien'"""
    cx += noise(t * 60) * 12 * vib
    F.line([(150, 1800), (370, 1300)], TU.shirt, 84); F.circle((430, 1230), 64, fill=(240, 232, 222))
    F.rect(cx - 240, cy - 440, cx + 240, cy + 440, fill=(20, 20, 26), outline=(90, 90, 100), w=8)
    F.rect(cx - 214, cy - 400, cx + 214, cy + 400, fill=(16, 22, 36))
    F.text((cx, cy - 340), "3:00", 54, ROJO)
    F.text((cx, cy - 260), tr("LLAMADA ENTRANTE"), 34, (170, 180, 200))
    F.circle((cx, cy - 120), 82, fill=(120, 100, 130))
    F.circle((cx, cy - 150), 28, fill=(220, 210, 200)); F.circle((cx - 18, cy - 176), 14, fill=(200, 200, 210))
    F.ellipse((cx, cy - 84), 46, 28, fill=(220, 210, 200))
    F.text((cx, cy + 10), quien, 84, (240, 240, 250))
    p = 1 + 0.08 * math.sin(t * 12)
    F.circle((cx - 110, cy + 270), 54 * p, fill=(40, 190, 90)); F.circle((cx + 110, cy + 270), 54, fill=(220, 40, 50))
    F.line([(cx - 134, cy + 270), (cx - 86, cy + 270)], (255, 255, 255), 10); F.line([(cx + 86, cy + 274), (cx + 134, cy + 274)], (255, 255, 255), 10)

TEL_TU = pose(l1u=90, l1l=-90, l2u=84, l2l=-88, a1u=150, a1l=150, a2u=-20, a2l=40, head=4)
def salon_dos(F, t, tu_face="neutral", tu_jit=0.6, tel=True, **kw):
    """el salón: tú con el móvil en la oreja y tu padre dormido a tu lado"""
    salon_casa(F, t, cocina=0.15)
    J = papa(F, kw.pop("pp", DORMIDO), PAPA_X, PISO - 170, t=t, f=1, **kw)
    p = TEL_TU if tel else pose(l1u=90, l1l=-90, l2u=84, l2l=-88, a1u=40, a1l=50, a2u=-20, a2l=40)
    T = TU.draw(F, add(p, jitter(t, tu_jit, 3)), TU_X, PISO - 170, f=1, face=tu_face)
    if tel:
        hx, hy = T["a1h"]
        F.rect(hx - 8, hy - 36, hx + 12, hy + 6, fill=(30, 40, 60)); F.rect(hx - 4, hy - 32, hx + 8, hy + 2, fill=(170, 210, 255))
    return J, T

def tv(t): return 0.75 + 0.25 * (noise(t * 12, 5) > -0.3)

# ---------- escenas ----------
TCORTE = 1.9
def llama(t, D, fi):
    """primer fotograma: el móvil vibra con 3:00 en rojo y ABUELA; luego el salón: tu padre dormido a tu lado"""
    if t < TCORTE:
        F = Frame(fondo(), dict(x=540, y=880, z=lerp(1.22, 1.05, ease(seg(t, 0, TCORTE)))))
        F.rect(-900, -400, 2000, 2600, fill=(10, 10, 16))
        entrante(F, t, tr("ABUELA"), vib=1.0)
        img = iluminar(F.finish(), F, [], glows=[((540, 860), 560, 1.0)], amb=0.15, warm=(170, 200, 255))
        return img, dict(grain=9, flash=(ROJO, 0.4 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.06))
    tt = t - TCORTE
    k = ease(seg(tt, 0, D - TCORTE))
    F = Frame(fondo(), dict(x=lerp(700, 620, k), y=lerp(PISO - 260, PISO - 330, k), z=lerp(2.0, 1.2, k)))
    J, T = salon_dos(F, t)
    img = iluminar(F.finish(), F, [], glows=[((640, PISO - 120), 420, 0.7 * tv(t)), (T["a1h"], 160, 0.7), ((640, PISO - 668), 100, 0.5)],
                   amb=0.2, warm=TELE)
    return img, dict(grain=10, flash=((170, 210, 255), 0.3 * (1 - seg(tt, 0, 0.2))))

HOMBRE_X = 950
def susurra(t, D, fi):
    """la cocina de la abuela: ella al teléfono, en primer plano; al fondo, junto a la nevera, un hombre de espaldas con jersey mostaza"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo("b"), dict(x=lerp(750, 790, k), y=lerp(PISO - 330, PISO - 380, k), z=lerp(1.55, 1.85, k)))
    cocina_abuela(F, t, nevera=0.85 + 0.15 * (noise(t * 8, 2) > -0.4))
    papa(F, add(pose(body=6, head=8, a1u=30, a1l=60, a2u=10, a2l=50), jitter(t, 0.3, 7)), HOMBRE_X, PISO, t=t, f=1, sc=1.05, espalda=True)
    abuela(F, add(TEL_ABU, jitter(t, 2.5, 4)), 560, PISO + 80, t=t, f=1, sc=1.3)
    img = iluminar(F.finish(), F, [], glows=[((1010, PISO - 400), 520, 0.9), ((720, 320), 260, 0.5), ((470, PISO - 260), 280, 0.4)],
                   amb=0.22, warm=NEVERA)
    return img, dict(grain=10, dark=0.04, tint=((255, 0, 30), 0.08 * seg(t, D * 0.5, D)))

def sofa(t, D, fi):
    """vuelta al salón: el mismo jersey mostaza. Tu padre, dormido a tu lado"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(640, PAPA_X, k), y=lerp(PISO - 300, PISO - 330, k), z=lerp(1.35, 2.1, k)))
    J, T = salon_dos(F, t, tu_face="neutral")
    img = iluminar(F.finish(), F, [], glows=[((640, PISO - 120), 420, 0.7 * tv(t)), (T["a1h"], 160, 0.7), (J["head"], 160, 0.4)],
                   amb=0.22, warm=TELE)
    return img, dict(grain=10, flash=((255, 255, 255), 0.25 * (1 - seg(t, 0, 0.2))))

def ronca(t, D, fi):
    """primer plano de su cara: boca abierta, ni un ruido. Ni un movimiento"""
    k = ease(seg(t, 0, D))
    J0 = PAPA.joints(DORMIDO, PAPA_X, PISO - 170, f=1)
    hx, hy = J0["head"]
    F = Frame(fondo(), dict(x=lerp(hx - 30, hx, k), y=lerp(hy + 60, hy + 10, k), z=lerp(3.6, 4.6, k)))
    salon_dos(F, t, tu_face="neutral", boca=0.5)
    img = iluminar(F.finish(), F, [], glows=[((hx, hy + 60), 200, 0.6 * tv(t)), ((hx - 120, hy), 140, 0.5)], amb=0.16, warm=TELE)
    def ov(img):                                                                     # "Zzz" que aparece… y se tacha
        p = ease_back(seg(t, D * 0.2, D * 0.32))
        if p <= 0: return img
        d = ImageDraw.Draw(img)
        d.text((760, 520), "Zzz…", font=font(110 * p + 1), fill=(220, 220, 235), anchor="mm", stroke_width=int(8 * p), stroke_fill=(0, 0, 0))
        c = seg(t, D * 0.5, D * 0.6)
        if c > 0: d.line([(600, 590), (lerp(600, 930, c), lerp(590, 450, c))], fill=ROJO, width=18)
        return img
    return img, dict(grain=10, dark=0.05, overlay=ov)

def insiste(t, D, fi):
    """la cocina otra vez: el hombre se ha acercado a la abuela y le habla al teléfono, con la cara en sombra"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo("b"), dict(x=lerp(500, 480, k), y=lerp(PISO - 380, PISO - 420, k), z=lerp(1.9, 2.4, k)))
    cocina_abuela(F, t, nevera=0.8)
    papa(F, add(pose(body=14, head=12, a1u=60, a1l=80, a2u=20, a2l=40), jitter(t, 0.4, 7)), 560, PISO + 40, t=t, f=-1, sc=1.2,
         sombra=True, habla=abs(math.sin(t * 9)) * seg(t, D * 0.3, D * 0.4))
    abuela(F, add(TEL_ABU, jitter(t, 2.5, 4)), 300, PISO + 60, t=t, f=1, sc=1.25)
    img = iluminar(F.finish(), F, [], glows=[((1010, PISO - 400), 420, 0.6), ((300, PISO - 260), 240, 0.4)], amb=0.17, warm=NEVERA)
    return img, dict(grain=11, dark=0.08, tint=((255, 0, 30), 0.12 * seg(t, D * 0.6, D)))

def pecho(t, D, fi):
    """tú, encogido, mirándolo; él, inmóvil del todo. Solo se mueve el grano"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(640, 700, k), y=lerp(PISO - 280, PISO - 300, k), z=lerp(1.9, 2.6, k)))
    J, T = salon_dos(F, t, tu_face="scared", tu_jit=2.5)
    sx, sy = J["sh"]; hx_, hy_ = J["hip"]
    cy = sy * 0.6 + hy_ * 0.4; cx = sx * 0.6 + hx_ * 0.4
    img = iluminar(F.finish(), F, [], glows=[((640, PISO - 120), 400, 0.6 * tv(t)), ((cx, cy), 160, 0.55), (T["a1h"], 140, 0.6)],
                   amb=0.14, warm=TELE)
    def ov(img):                                                                     # una línea plana sobre su pecho
        p = seg(t, D * 0.35, D * 0.5)
        if p <= 0: return img
        d = ImageDraw.Draw(img)
        px, py = F.P(cx, cy); px, py = px / S, py / S
        d.line([(px - 170, py), (px - 170 + 340 * p, py)], fill=ROJO, width=6)
        return img
    return img, dict(grain=11, dark=0.06, tint=((255, 0, 30), 0.1 * seg(t, D * 0.4, D)), overlay=ov)

TOJOS, TCUELGA = 1.55, 2.45
def ojos(t, D, fi):
    """primerísimo plano: sin mover nada más, abre los ojos. Y habla"""
    J0 = PAPA.joints(DORMIDO, PAPA_X, PISO - 170, f=1)
    hx, hy = J0["head"]
    ab = ease(seg(t, TOJOS, TOJOS + 0.12))
    sh = 12 * seg(t, TOJOS, TOJOS + 0.1) * (1 - seg(t, TOJOS + 0.5, TOJOS + 0.9))
    F = Frame(fondo(), dict(x=hx + noise(t * 40) * sh, y=hy + 4 + noise(t * 40, 2) * sh, z=lerp(4.2, 6.0, ease(seg(t, 0, D)))))
    habla = seg(t, TCUELGA, TCUELGA + 0.1) * (1 - seg(t, TCUELGA + 0.7, TCUELGA + 0.9))
    salon_dos(F, t, tu_face="scared", ojos=ab, boca=0.3, habla=habla * abs(math.sin(t * 16)), gris=0.85 * ab)
    img = iluminar(F.finish(), F, [], glows=[((hx, hy + 40), 200, 0.7 * tv(t))], amb=0.14, warm=TELE)
    hit = t > TOJOS
    return img, dict(grain=12, tint=((255, 0, 30), 0.25 * hit), flash=((255, 255, 255), 0.75 * max(0, 1 - (t - TOJOS) / 0.25)) if hit else None,
                     glitch=0.4 if hit and t < TOJOS + 0.4 and fi % 3 else (0.25 if TCUELGA < t < TCUELGA + 0.3 and fi % 3 else 0.0))

TR = 1.5
def final(t, D, fi):
    """el móvil se apaga; tu padre, sentado muy recto, te mira con los ojos negros. La regla"""
    F = Frame(fondo(), dict(x=600, y=lerp(PISO - 330, PISO - 360, seg(t, 0, D)), z=lerp(1.5, 1.3, ease(seg(t, 0, D)))))
    salon_casa(F, t, cocina=0.15)
    papa(F, pose(body=0, head=0, l1u=90, l1l=-90, l2u=84, l2l=-88, a1u=10, a1l=30, a2u=-8, a2l=30), PAPA_X, PISO - 170, t=t, f=-1,
         ojos=1.0, boca=0.1, gris=0.85)
    T = TU.draw(F, add(pose(body=-16, head=6, l1u=90, l1l=-90, l2u=84, l2l=-88, a1u=60, a1l=40, a2u=-30, a2l=40), jitter(t, 2.5, 3)),
                TU_X - 30, PISO - 170, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((640, PISO - 120), 400, 0.5 * tv(t)), ((PAPA_X, PISO - 380), 180, 0.4)], amb=0.14, warm=TELE)
    pp = ease_back(seg(t, TR, TR + 0.3)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        d_ = ImageDraw.Draw(img)
        q = ease_back(seg(t, 0.15, 0.4)) * (1 - seg(t, TR - 0.2, TR))
        if q > 0:
            d_.text((540, 420), tr("LLAMADA FINALIZADA"), font=font(64 * q + 1), fill=(255, 110, 110), anchor="mm", stroke_width=int(7 * q), stroke_fill=(0, 0, 0))
        if pp <= 0: return img
        d_.rounded_rectangle((40, 1150, 1040, 1600), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 LLAMA"), 1210, 62, (255, 255, 255)), (tr("LA ABUELA…"), 1290, 62, (255, 255, 255)),
                                 (tr("CRÉETELA"), 1450, 140, ROJO)):
            fs = fs0
            while fs > 24 and d_.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d_.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d_.rounded_rectangle((230, 1640, 850, 1730), 26, fill=(230, 30, 50))
        d_.text((540, 1685), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.22 * pp if pp > 0 else 0.12), dark=0.04,
                     glitch=0.3 if pp > 0 and fi % 5 == 0 else (0.3 if t < 0.25 and fi % 2 else 0.0), overlay=regla)

ESCENA_FN = dict(llama=llama, susurra=susurra, sofa=sofa, ronca=ronca, insiste=insiste, pecho=pecho, ojos=ojos, final=final)
PAUSA = dict(llama=0.4, susurra=0.5, sofa=0.4, ronca=0.6, insiste=0.5, pecho=0.8, ojos=0.8, final=2.4)
