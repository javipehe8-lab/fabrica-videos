"""Si oyes esto a las 3AM — 1: "No bajes". Casa de noche: cuarto, escalera, cocina, cuarto de mamá.
Piezas reutilizables para la serie: TU (protagonista), MAMA, IMITADORA (la cosa con la bata), reloj_3am, escalera_casa,
puerta_cocina, movil_msg, puerta_cerrada."""
import math, random
from PIL import ImageDraw
from motor import *
from escenas2 import big
from escenas5 import iluminar

TU = Fig(shirt=(60, 160, 130), scale=0.85)                        # protagonista (sudadera verde)
MAMA = Fig(shirt=(225, 120, 160), limb=(240, 232, 222))            # madre (bata rosa)
IMITA = Fig(shirt=(225, 120, 160), limb=(205, 200, 196))           # la cosa: bata de mamá, piel grisácea
PELO = (90, 56, 36)
CASA_A, CASA_B = (24, 26, 40), (10, 11, 18)
COCINA = (255, 214, 140)

def pelo_mama(F, J, sc=1.0, espalda=False):
    hx, hy = J["head"]; r = L["head"] * sc
    if espalda:                                                   # vista de espaldas: toda la cabeza es pelo
        F.circle((hx, hy), r + 2 * sc, fill=PELO)
        F.line([(hx, hy + r * 0.6), (hx + 4 * sc, hy + r * 2.3)], PELO, 26 * sc)
        return
    F.d.chord([*F.P(hx - r - 3 * sc, hy - r - 4 * sc), *F.P(hx + r + 3 * sc, hy + r - 8 * sc)], 180, 360, fill=PELO)
    for s_ in (-1, 1):
        F.line([(hx + s_ * r * 0.95, hy - r * 0.2), (hx + s_ * r * 1.05, hy + r * 1.4)], PELO, 13 * sc)

def reloj_3am(F, cx, cy, s=1.0, on=True):
    F.rect(cx - 150 * s, cy - 70 * s, cx + 150 * s, cy + 70 * s, fill=(14, 14, 16), outline=(60, 60, 66), w=6 * s)
    if on: F.text((cx, cy + 4 * s), "3:00", 108 * s, (255, 40, 40), stroke=3 * s, scol=(90, 0, 0))

def cuarto_casa(F, puerta_luz=0.0, piso=1300):
    F.rect(-600, 300, 1700, piso, fill=(30, 33, 52))
    F.rect(-600, piso, 1700, 2800, fill=(14, 15, 24)); F.line([(-600, piso), (1700, piso)], (50, 54, 80), 6)
    # puerta a la derecha, entreabierta
    F.rect(760, piso - 560, 1000, piso, fill=(8, 8, 12))
    if puerta_luz > 0: F.rect(760, piso - 560, 790, piso, fill=tuple(int(v * puerta_luz) for v in COCINA))
    F.poly([(790, piso - 560), (950, piso - 590), (950, piso + 30), (790, piso)], fill=(62, 52, 46), outline=(30, 24, 20), w=4)
    F.circle((925, piso - 280), 10, fill=(200, 180, 120))
    # cama y mesilla
    F.rect(40, piso - 150, 560, piso - 50, fill=(60, 72, 110)); F.rect(40, piso - 172, 560, piso - 140, fill=(140, 150, 190))
    F.rect(40, piso - 300, 70, piso, fill=(80, 60, 50))
    for lx in (52, 548): F.line([(lx, piso - 50), (lx, piso)], (40, 46, 70), 10)
    F.rect(590, piso - 190, 720, piso, fill=(70, 54, 44), outline=(40, 30, 24), w=4)

def escalera_casa(F, piso_alto=700, piso_bajo=1300, x0=120, x1=900, n=12):
    """escalera vista de lado: baja de izquierda (arriba) a derecha (abajo); devuelve f(u)->(x,y) del pie"""
    F.rect(-600, 0, 1700, 2800, fill=(22, 23, 34))
    F.rect(-600, piso_alto, x0, piso_alto + 40, fill=(40, 40, 54))
    F.rect(x1, piso_bajo, 1700, 2800, fill=(16, 16, 22)); F.line([(x1, piso_bajo), (1700, piso_bajo)], (50, 50, 66), 6)
    dx, dy = (x1 - x0) / n, (piso_bajo - piso_alto) / n
    pts = [(x0, piso_alto)]
    for k in range(n):
        pts += [(x0 + (k + 1) * dx, piso_alto + k * dy), (x0 + (k + 1) * dx, piso_alto + (k + 1) * dy)]
    F.poly(pts + [(x1, piso_bajo + 40), (x0, piso_alto + 40)], fill=(54, 46, 40))
    F.line(pts, (96, 80, 66), 6, round_=False)
    F.line([(x0, piso_alto - 140), (x1, piso_bajo - 140)], (90, 70, 56), 10)          # barandilla
    for k in range(0, n + 1, 2):
        bx = x0 + k * dx; F.line([(bx, piso_alto + k * dy - 140 + 0), (bx, piso_alto + k * dy)], (80, 64, 50), 6)
    return lambda u: (lerp(x0, x1, u), lerp(piso_alto, piso_bajo, u))

def puerta_cocina(F, x, piso=1300, luz=1.0, w=300, h=620):
    F.rect(x - w / 2 - 30, piso - h - 30, x + w / 2 + 30, piso, fill=(40, 34, 30))
    c = tuple(int(v * luz) for v in COCINA)
    F.rect(x - w / 2, piso - h, x + w / 2, piso, fill=c)
    F.rect(x - w / 2, piso - 40, x + w / 2, piso, fill=tuple(int(v * luz * 0.7) for v in COCINA))

def imitadora(F, p, x, piso, sc=1.6, espalda=True, t=0.0, cara=0.0, f=1):
    """la cosa con la bata de mamá: demasiado alta y con los brazos demasiado largos"""
    old = IMITA.scale; IMITA.scale = sc
    J = IMITA.draw(F, p, x, piso, f=f, face="closed", t=t, stretch=1.22)
    IMITA.scale = old
    hx, hy = J["head"]; r = L["head"] * sc
    # bata hasta las rodillas
    sx, sy = J["sh"]; hpx, hpy = J["hip"]
    F.poly([(sx - 30 * sc, sy + 4 * sc), (sx + 30 * sc, sy + 4 * sc), (hpx + 48 * sc, hpy + 70 * sc), (hpx - 48 * sc, hpy + 70 * sc)], fill=(205, 105, 145))
    if cara < 0.5:
        pelo_mama(F, J, sc, espalda=True)
    else:
        F.ellipse((hx, hy + 8 * sc), r * 0.95, r * 1.35, fill=(214, 210, 206))
        F.d.chord([*F.P(hx - r - 3 * sc, hy - r - 6 * sc), *F.P(hx + r + 3 * sc, hy + r - 14 * sc)], 180, 360, fill=PELO)
        for dx in (-12, 12):
            F.ellipse((hx + dx * sc, hy - 2 * sc), 8 * sc, 13 * sc, fill=(2, 2, 4))
            F.circle((hx + dx * sc, hy - 2 * sc), 1.6 * sc, fill=(255, 255, 255))
        F.ellipse((hx, hy + 30 * sc), 9 * sc, 17 * sc, fill=(2, 2, 4))
    return J

def movil_msg(F, t, D, quien, lineas, cx=540, cy=860):
    vib = noise(t * 60) * 10 * (seg(t, 0.05, 0.2) - seg(t, 0.6, 0.8))
    cx += vib
    F.line([(140, 1760), (360, 1260)], TU.shirt, 80); F.circle((430, 1190), 62, fill=(240, 240, 240))
    F.rect(cx - 230, cy - 420, cx + 230, cy + 420, fill=(20, 20, 26), outline=(90, 90, 100), w=8)
    F.rect(cx - 205, cy - 380, cx + 205, cy + 380, fill=(16, 22, 34))
    F.text((cx, cy - 300), quien, 50, (230, 230, 240))
    F.line([(cx - 205, cy - 250), (cx + 205, cy - 250)], (50, 60, 80), 3)
    for k, ln in enumerate(lineas):
        p = ease_back(seg(t, D * (0.2 + 0.18 * k), D * (0.3 + 0.18 * k)))
        if p <= 0: continue
        y = cy - 170 + k * 140
        fs = 44
        while fs > 20 and F.d.textlength(ln, font=font(fs * S)) / S > 330: fs -= 2
        F.rect(cx - 190, y - 55 * p, cx + 190, y + 55 * p, fill=(245, 245, 250), outline=(220, 220, 230), w=2)
        F.text((cx, y), ln, fs * p + 1, (30, 30, 40))
    return (cx, cy)

# ---------- escenas ----------
def llama(t, D, fi):
    k = ease(seg(t, 0.0, D * 0.45))
    F = Frame(gradient(CASA_A, CASA_B), dict(x=lerp(655, 560, k), y=lerp(1070, 1020, k), z=lerp(3.2, 1.35, k)))
    luz = 0.55 + 0.35 * (noise(t * 6, 3) > -0.3) if t > D * 0.35 else 0.0
    cuarto_casa(F, puerta_luz=luz)
    reloj_3am(F, 655, 1070, 0.42)
    s = ease(seg(t, D * 0.45, D * 0.65))
    TU.draw(F, mix(pose(l1u=90, l2u=90, l1l=0, l2l=0, a1u=10), pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=40, a1l=30, a2u=-20), s),
            lerp(250, 300, s), lerp(1140, 1150, s), f=1, rot=lerp(-90, 0, s), snap=False,
            face="closed" if t < D * 0.4 else ("scared" if t > D * 0.6 else "neutral"))
    img = F.finish()
    img = iluminar(img, F, [], glows=[((655, 1070), 260, 0.7), ((780, 1000), 320 * (luz > 0), 0.8 * luz)], amb=0.3, warm=(255, 120, 120))
    return img, dict(grain=9, flash=((255, 40, 40), 0.35 * (1 - seg(t, 0, 0.25))))

def bajas(t, D, fi):
    F = Frame(gradient(CASA_A, CASA_B), dict(x=560, y=1000, z=1.0))
    path = escalera_casa(F)
    luz = 0.35 + 0.6 * (noise(t * 9, 7) > -0.1)
    puerta_cocina(F, 1180, luz=luz, w=220)
    u = 0.08 + 0.55 * ease(seg(t, 0, D * 0.95))
    x, y = path(u)
    TU.draw(F, walk(t, 0.6, 0.6), x, y, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((1180, 1000), 520, luz), ((x, y - 120), 180, 0.35)], amb=0.18, warm=COCINA)
    return img, dict(grain=10)

def movil(t, D, fi):
    F = Frame(gradient((14, 14, 18), (6, 6, 8)), dict(x=540, y=900, z=lerp(1.0, 1.12, ease(t / D))))
    c = movil_msg(F, t, D, tr("MAMÁ"), [tr("NO BAJES."), tr("ESTOY EN MI CUARTO."), tr("YO TAMBIÉN LA HE OÍDO.")])
    img = iluminar(F.finish(), F, [], glows=[(c, 560, 1.0)], amb=0.25, warm=(170, 200, 255))
    return img, dict(grain=8, tint=((255, 0, 30), 0.12 * seg(t, D * 0.6, D)))

def espalda(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(gradient(CASA_A, CASA_B), dict(x=lerp(620, 760, k), y=lerp(980, 900, k), z=lerp(1.0, 1.35, k)))
    F.rect(-600, 0, 1700, 2800, fill=(20, 20, 30))
    puerta_cocina(F, 760, luz=0.75 + 0.2 * (noise(t * 9, 2) > 0), w=420, h=760)
    imitadora(F, add(pose(a1u=6, a1l=2, a2u=-6, a2l=2), jitter(t, 1.5, 4)), 760, 1300, sc=1.75, espalda=True, t=t)
    # tú, en primer plano en la escalera (silueta)
    big(TU, 1.3, F, add(pose(body=-6, head=4, a1u=40, a1l=60), jitter(t, 3, 1)), 420, 1460, f=1, face="scared")
    F.line([(100, 1250), (560, 1470)], (60, 48, 40), 16)
    img = iluminar(F.finish(), F, [], glows=[((760, 900), 560, 0.95)], amb=0.12, warm=COCINA)
    return img, dict(grain=11, dark=0.05)

def cabeza(t, D, fi):
    gira = seg(t, D * 0.3, D * 0.42)
    sh = 14 * gira
    F = Frame(gradient(CASA_A, CASA_B), dict(x=760 + noise(t * 30) * sh, y=lerp(800, 760, ease(t / D)), z=lerp(2.3, 2.9, ease(t / D)),
                                            sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    F.rect(-600, 0, 1700, 2800, fill=(20, 20, 30))
    puerta_cocina(F, 760, luz=0.85, w=420, h=760)
    imitadora(F, pose(a1u=6, a1l=2, a2u=-6, a2l=2), 760, 1300, sc=1.75, cara=gira, t=t)
    img = iluminar(F.finish(), F, [], glows=[((760, 700), 560, 0.95)], amb=0.12, warm=COCINA)
    hit = gira >= 1
    return img, dict(flash=((255, 255, 255), max(0, 1 - (t - D * 0.42) / 0.25)) if hit else None, glitch=0.45 if hit and fi % 3 else 0.0,
                     tint=((255, 0, 30), 0.3 if hit else 0.0), grain=12)

def subes(t, D, fi):
    F = Frame(gradient(CASA_A, CASA_B), dict(x=540, y=980, z=1.0))
    path = escalera_casa(F)
    puerta_cocina(F, 1180, luz=0.8, w=220)
    u = 0.75 - 0.75 * ease_out(seg(t, 0, D * 0.8))
    x, y = path(u)
    TU.draw(F, run(t, 1.3), x, y, f=-1, face="scared")
    # la cosa asoma al pie de la escalera, a cuatro patas
    ap = ease(seg(t, D * 0.35, D * 0.8))
    p4 = pose(body=75, head=-60, a1u=150, a1l=-30, a2u=170, a2l=-20, l1u=40, l1l=-80, l2u=20, l2l=-90)
    imitadora(F, add(p4, jitter(t, 4, 9)), lerp(1250, 1000, ap), 1300, sc=1.2, cara=1.0, t=t, f=-1)
    img = iluminar(F.finish(), F, [], glows=[((1180, 1000), 520, 0.9), ((x, y - 120), 200, 0.3)], amb=0.16, warm=COCINA)
    return img, dict(grain=11, tint=((255, 0, 30), 0.15 * ap))

def _cuarto_mama(F, piso=1300):
    F.rect(-600, 300, 1700, piso, fill=(36, 30, 46))
    F.rect(-600, piso, 1700, 2800, fill=(16, 13, 20)); F.line([(-600, piso), (1700, piso)], (60, 50, 70), 6)
    F.rect(760, piso - 560, 1000, piso, fill=(70, 56, 46), outline=(30, 24, 20), w=6)           # puerta cerrada
    F.circle((785, piso - 280), 10, fill=(200, 180, 120))
    F.line([(700, piso), (790, piso - 300)], (90, 64, 44), 14); F.rect(640, piso - 120, 720, piso, fill=(90, 64, 44))  # silla atrancando
    F.rect(20, piso - 160, 600, piso - 50, fill=(120, 70, 100)); F.rect(20, piso - 182, 600, piso - 150, fill=(200, 160, 190))

def abrazo(t, D, fi):
    F = Frame(gradient((36, 30, 46), (12, 10, 16)), dict(x=480, y=1060, z=1.25))
    _cuarto_mama(F)
    tb = jitter(t, 4, 3)
    J = MAMA.draw(F, add(pose(body=-10, a1u=100, a1l=70, a2u=80, a2l=80), tb), 400, 1130, f=1, face="scared")
    pelo_mama(F, J)
    TU.draw(F, add(pose(body=12, a1u=-90, a1l=-40, a2u=-70, a2l=-30, l1u=90, l1l=-90, l2u=90, l2l=-90), jitter(t, 3, 5)), 470, 1145, f=-1, face="closed")
    F.rect(330, 1000, 370, 1060, fill=(30, 40, 60)); F.rect(334, 1004, 366, 1056, fill=(160, 200, 255))   # su móvil
    img = iluminar(F.finish(), F, [], glows=[((350, 1030), 280, 0.85)], amb=0.25, warm=(170, 200, 255))
    return img, dict(grain=9)

def tuvoz(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(gradient((36, 30, 46), (12, 10, 16)), dict(x=lerp(700, 870, k), y=lerp(1100, 1180, k), z=lerp(1.3, 2.4, k)))
    _cuarto_mama(F)
    # rendija de luz bajo la puerta, que parpadea con la voz
    luz = 0.5 + 0.5 * (noise(t * 12, 4) > -0.2)
    F.rect(760, 1290, 1000, 1300, fill=tuple(int(v * luz) for v in COCINA))
    TU.draw(F, add(pose(body=-8, a1u=150, a1l=40, a2u=140, a2l=45), jitter(t, 2, 6)), 560, 1300, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((880, 1295), 260, luz * 0.9), ((350, 1030), 300, 0.5)], amb=0.22, warm=COCINA)
    return img, dict(grain=11, tint=((255, 0, 30), 0.2 * seg(t, D * 0.4, D)), glitch=0.2 if t > D * 0.5 and fi % 7 == 0 else 0.0)

def final(t, D, fi):
    lev = ease(seg(t, 0.2, D * 0.35))
    F = Frame(gradient((36, 30, 46), (12, 10, 16)), dict(x=520, y=1040, z=1.15))
    _cuarto_mama(F)
    J = MAMA.draw(F, mix(pose(body=-10, l1u=90, l1l=-90, l2u=90, l2l=-90), add(walk(t, 0.4, 0.4), pose(a1u=20, a2u=-20)), lev),
                  lerp(380, lerp(380, 600, ease(seg(t, D * 0.35, D * 0.8))), lev), 1300 if lev > 0.5 else 1150, f=1, face="closed")
    pelo_mama(F, J)
    TU.draw(F, add(pose(body=-20, a1u=100, a1l=0, a2u=90, a2l=10), jitter(t, 3, 8)), 300, 1300, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((880, 1295), 300, 0.8), (J["head"], 200, 0.4)], amb=0.2, warm=COCINA)
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, D * 0.62, D * 0.72)) * (1 + 0.03 * math.sin(t * 25))
    if p > 0:
        d.text((540, 520), tr("NO BAJES"), font=font(170 * p + 1), fill=(255, 40, 50), anchor="mm", stroke_width=int(14 * p), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 690, 850, 790), 26, fill=(230, 30, 50))
        d.text((540, 740), tr("SÍGUEME PARA MÁS"), font=font(52), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=10, tint=((255, 0, 30), 0.25 * p if p > 0 else 0), glitch=0.3 if p > 0 and fi % 5 == 0 else 0.0)

ESCENA_FN = dict(llama=llama, bajas=bajas, movil=movil, espalda=espalda, cabeza=cabeza, subes=subes, abrazo=abrazo, tuvoz=tuvoz, final=final)
PAUSA = dict(llama=0.3, bajas=0.2, movil=0.5, espalda=0.3, cabeza=0.6, subes=0.2, abrazo=0.3, tuvoz=0.5, final=1.5)
