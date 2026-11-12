"""Escenas del episodio 19 (inicio de la TEMPORADA 3, "Lucía no tiene sombra"): la sombra de Lucía se despega de la pared
con ojos blancos; Lucía llama a Nora; Leo, Nora y Carmen llegan en coche mientras las farolas se apagan tras ellos; en el
cuarto de Lucía, con todas las luces encendidas, las sombras de todos están en la pared… menos la de Lucía. Giro: la
sombra de Nora abre los ojos y gira la cabeza hacia Lucía."""
import math, random
from motor import *
from escenas import base, cuarto
from escenas5 import iluminar
from escenas6 import NINA, coletas
from escenas8 import calle, farola, coche_draw
from escenas18 import sombra_pared, lucia_acostada

PISO = 1250
CALIDA = (255, 214, 160)
PARED = (128, 104, 92)          # pared iluminada por la lámpara
SOMB = (34, 26, 30)             # color de las sombras sobre la pared

# ---------- piezas nuevas ----------
def sombra_de(F, fig, p, x, piso, f=1, sc=1.25, col=SOMB, ojos=0.0, gira=0.0, extra=(), brazo=None):
    """sombra plana de un personaje proyectada en la pared (más grande); ojos blancos opcionales.
    extra: 'coleta', 'gorra', 'mono', 'coletas'. gira: la cabeza se vuelve hacia la derecha"""
    J = Fig(scale=fig.scale * sc).joints(p, x, piso, f)
    s = fig.scale * sc; w = 15 * s
    for seg_ in (["sh", "a2e", "a2h"], ["hip", "l2k", "l2f"], ["hip", "neck"], ["hip", "l1k", "l1f"], ["sh", "a1e", "a1h"]):
        F.line([J[k] for k in seg_], col, w)
    hc = J["head"]; r = L["head"] * s
    F.circle(hc, r, fill=col)
    if "coleta" in extra:
        F.line([(hc[0] - f * r * 0.8, hc[1] - r * 0.5), (hc[0] - f * r * 1.5, hc[1] + r * 0.1), (hc[0] - f * r * 1.4, hc[1] + r * 0.9)], col, 12 * s)
    if "gorra" in extra:
        F.line([(hc[0], hc[1] - r * 0.45), (hc[0] + f * r * 1.5, hc[1] - r * 0.45)], col, 9 * s)
    if "mono" in extra:
        F.circle((hc[0] - f * r * 0.62, hc[1] - r * 0.92), r * 0.46, fill=col)
    if "coletas" in extra:
        for dx in (-1.1, 1.1): F.ellipse((hc[0] + dx * r, hc[1] + r * 0.2), r * 0.35, r * 0.6, fill=col)
    if ojos > 0:
        g = int(255 * ojos)
        for dx in (-10, 12):
            F.ellipse((hc[0] + (dx + 12 * gira) * s, hc[1] - 5 * s), 6.5 * s, 6.5 * s * ojos, fill=(g, g, g))
    return J

def lampara_pie(F, x, piso, on=1.0):
    """lámpara de pie con pantalla"""
    F.line([(x, piso), (x, piso - 520)], (70, 60, 56), 10)
    F.ellipse((x, piso - 6), 60, 12, fill=(50, 44, 42))
    c = tuple(int(lerp(a, b, on)) for a, b in zip((80, 70, 60), (255, 226, 160)))
    F.poly([(x - 70, piso - 520), (x + 70, piso - 520), (x + 46, piso - 620), (x - 46, piso - 620)], fill=c)

def cuarto_luz(F, t):
    """el cuarto de Lucía con todas las luces encendidas: pared clara, bombilla, ventana tapada, cama"""
    F.rect(-500, 0, 1600, PISO, fill=PARED)
    F.rect(-500, PISO, 1600, 2700, fill=(52, 40, 38)); F.line([(-500, PISO), (1600, PISO)], (90, 70, 62), 8)
    F.line([(540, 0), (540, 330)], (40, 36, 34), 4); F.circle((540, 350), 26, fill=(255, 246, 210))   # bombilla del techo
    F.rect(860, 520, 1100, 820, fill=(150, 140, 120), outline=(90, 74, 60), w=14)                      # ventana tapada con periódicos
    for wx, wy in ((870, 530), (980, 530), (870, 670), (980, 670)): F.rect(wx, wy, wx + 100, wy + 130, fill=(176, 168, 146))
    F.line([(870, 530), (1090, 810)], (110, 96, 70), 8); F.line([(1090, 530), (870, 810)], (110, 96, 70), 8)

# ---------- escenas ----------
def sombra_viva(t, D, fi):
    zz = ease(seg(t, 0, D))
    F = Frame(base("cuarto"), dict(x=lerp(300, 270, zz), y=lerp(940, 900, zz), z=lerp(1.5, 1.9, zz),
                                  sx=noise(t * 30) * 4, sy=noise(t * 30, 2) * 4))
    cuarto(F, t=t)
    F.ellipse((235, 900), 145, 250, fill=(48, 50, 84))
    sale = ease(seg(t, D * 0.15, D * 0.6))
    sombra_pared(F, lerp(240, 300, sale), 1060, t, ojos=ease(seg(t, D * 0.5, D * 0.7)), gira=ease(seg(t, D * 0.6, D * 0.85)))
    F.rect(80, 1150, 440, 1250, fill=(70, 80, 116)); F.rect(80, 1132, 440, 1160, fill=(150, 160, 196))
    F.rect(100, 1100, 190, 1140, fill=(205, 210, 230))
    lucia_acostada(F, 250, 1115, t, ojos=True)
    img = iluminar(F.finish(), F, [], glows=[((540, 690), 300, 0.45), ((280, 880), 260, 0.6)], amb=0.35, warm=(170, 180, 255))
    return img, dict(grain=10, dark=0.1, tint=((120, 120, 255), 0.08),
                     flash=((255, 255, 255), 0.35 * math.exp(-abs(t - D * 0.55) * 12)),
                     glitch=0.3 if (fi % 6 == 0 and t > D * 0.55) else 0.0)

def llamada(t, D, fi):
    zz = ease(t / D)
    F = Frame(base("cuarto"), dict(x=lerp(520, 540, zz), y=lerp(1000, 980, zz), z=lerp(1.6, 1.85, zz)))
    cuarto_luz(F, t)
    lampara_pie(F, 200, PISO)
    p = pose(head=8, body=4, a1u=150, a1l=-150, a2u=-30, a2l=40, l1u=6, l2u=-6)
    p = add(p, jitter(t, 3, 4))
    sombra_de(F, NINA, p, 620, PISO, f=1, sc=1.35, extra=("coletas",), ojos=0.6 * ease(seg(t, D * 0.7, D * 0.9)))
    J = NINA.draw(F, p, 480, PISO, f=1, face="scared")
    coletas(F, J, 0.8)
    hx, hy = J["head"]                                                          # móvil pegado a la oreja
    F.rect(hx + 24, hy - 30, hx + 50, hy + 22, fill=(24, 24, 30), outline=(120, 120, 130), w=3)
    F.rect(hx + 28, hy - 24, hx + 46, hy + 14, fill=(120, 170, 255))
    img = iluminar(F.finish(), F, [], glows=[((200, 660), 560, 1.0), ((540, 350), 380, 0.8)], amb=0.45, warm=CALIDA)
    return img, dict(grain=8, tint=((255, 180, 120), 0.04))

def viaje(t, D, fi):
    w = ease(seg(t, 0, D))
    cx = lerp(1500, 300, w)
    F = Frame(base("ciudad"), dict(x=cx + 120, y=1020, z=1.1, sx=noise(t * 20) * 3))
    lamps = (0, 520, 1040, 1560, 2080)
    calle(F, -600, 2200, seed=41, lamps=())
    for lx in lamps:                                                            # las farolas se apagan cuando el coche pasa
        on = 1.0 - ease(seg(cx - lx, -260, -140))
        farola(F, lx, 1240, on)
    F.poly([(cx - 286, 1175), (cx - 700, 1110), (cx - 700, 1290), (cx - 286, 1200)], fill=(70, 70, 70))   # faros
    coche_draw(F, cx, 1300)
    for i, dx in enumerate((-60, 60)):                                          # cabezas dentro del coche
        F.circle((cx + dx, 1080), 22, fill=(240, 240, 240))
    glows = [((cx - 450, 1180), 300, 0.9), ((cx, 1150), 260, 0.5)]
    for lx in lamps:
        on = 1.0 - ease(seg(cx - lx, -260, -140))
        if on > 0.05: glows.append(((lx - 90, 650), 230, 0.8 * on))
    img = iluminar(F.finish(), F, [], glows=glows, amb=0.25, warm=CALIDA)
    return img, dict(grain=9)

def sombras_calle(t, D, fi):
    w = ease(seg(t, 0, D))
    F = Frame(base("ciudad"), dict(x=lerp(420, 640, w), y=980, z=1.1))
    F.circle((900, 300), 60, fill=(220, 224, 236))
    F.rect(-600, 560, 1800, 1180, fill=(104, 94, 100))                            # tapia larga
    for yy in range(600, 1180, 70): F.line([(-600, yy), (1800, yy)], (90, 80, 86), 3)
    F.rect(-600, 1180, 1800, 1300, fill=(34, 36, 46)); F.rect(-600, 1300, 1800, 2700, fill=(18, 19, 26))
    F.line([(-600, 1300), (1800, 1300)], (54, 56, 70), 6)
    for lx in (0, 900): farola(F, lx, 1240, 1.0)
    from escenas8 import DORMIDOS
    for i, sx in enumerate((150, 520, 1150)):                                  # sombras sin dueño, con ojos que los siguen
        giro = ease(seg(t, D * (0.2 + 0.15 * i), D * (0.4 + 0.15 * i)))
        sombra_de(F, DORMIDOS[i], pose(head=lerp(18, -6, giro), body=4, a1u=6, a2u=-6), sx, 1180, f=-1 if i == 2 else 1,
                  sc=1.35, col=(10, 8, 12), ojos=giro, gira=0.0)
    xs = lerp(-100, 700, w)
    for k, (fig, dx) in enumerate(((CARMEN, -260), (LEO, -130), (NORA, 0))):
        fig.draw(F, walk(t + k * 0.2, 1.0), xs + dx, 1300, f=1, face="scared")
    glows = [((-90, 620), 380, 0.9), ((810, 620), 380, 0.9), ((xs - 120, 1150), 320, 0.4)]
    img = iluminar(F.finish(), F, [], glows=glows, amb=0.3, warm=CALIDA)
    return img, dict(grain=9, tint=((120, 120, 255), 0.05), flash=((255, 255, 255), 0.25 * math.exp(-abs(t - D * 0.3) * 10)))

def _personajes(F, t, susto=0.0):
    """los cuatro en el cuarto de Lucía, cada uno con su sombra en la pared… salvo Lucía"""
    gente = [(CARMEN, 150, ("mono",), 1), (LEO, 330, ("gorra",), 1), (NORA, 520, ("coleta",), 1)]
    out = {}
    for fig, x, ex, f in gente:
        p = mix(pose(head=-4, a1u=20, a2u=-20), SCARED if fig is not CARMEN else pose(head=-6, a1u=40), susto)
        if fig is NORA: p = pose(head=-4, a1u=20, a2u=-20)
        out[fig] = (p, x, ex, f)
    return out

def cuarto19(t, D, fi):
    zz = ease(t / D)
    F = Frame(base("cuarto"), dict(x=lerp(520, 560, zz), y=lerp(900, 920, zz), z=lerp(1.0, 1.08, zz)))
    cuarto_luz(F, t)
    lampara_pie(F, 30, PISO)
    gente = _personajes(F, t)
    for fig, (p, x, ex, f) in gente.items(): sombra_de(F, fig, p, x + 110, PISO, f=f, extra=ex)
    for fig, (p, x, ex, f) in gente.items(): fig.draw(F, p, x, PISO, f=f, face="neutral")
    J = NINA.draw(F, pose(head=-6, a1u=40 + 10 * math.sin(t * 3), a2u=-20), 800, PISO, f=-1, face="scared")
    coletas(F, J, 0.8)
    img = iluminar(F.finish(), F, [], glows=[((30, 660), 600, 1.0), ((540, 350), 420, 0.8)], amb=0.5, warm=CALIDA)
    return img, dict(grain=7, tint=((255, 180, 120), 0.04))

def sin_sombra(t, D, fi):
    zz = ease(seg(t, D * 0.15, D * 0.8))
    F = Frame(base("cuarto"), dict(x=lerp(560, 840, zz), y=lerp(920, 930, zz), z=lerp(1.08, 1.75, zz)))
    cuarto_luz(F, t)
    lampara_pie(F, 30, PISO)
    gente = _personajes(F, t, susto=ease(seg(t, D * 0.5, D * 0.8)))
    for fig, (p, x, ex, f) in gente.items(): sombra_de(F, fig, p, x + 110, PISO, f=f, extra=ex)
    for fig, (p, x, ex, f) in gente.items(): fig.draw(F, p, x, PISO, f=f, face="scared" if t > D * 0.5 else "neutral")
    J = NINA.draw(F, add(pose(head=-6, a1u=40, a2u=-20), jitter(t, 3, 1)), 800, PISO, f=-1, face="scared")
    coletas(F, J, 0.8)
    # hueco vacío en la pared donde debería estar su sombra (contorno de tiza muy tenue para que se note la ausencia)
    if t > D * 0.55:
        a = ease(seg(t, D * 0.55, D * 0.8))
        c = tuple(int(lerp(v, 170, 0.5 * a)) for v in PARED)
        F.line([(910, PISO), (910, 900)], c, 3); F.circle((910, 840), 70, outline=c, w=3)
    img = iluminar(F.finish(), F, [], glows=[((30, 660), 600, 1.0), ((540, 350), 420, 0.8), ((880, 900), 300, 0.6)], amb=0.5, warm=CALIDA)
    return img, dict(grain=8, tint=((255, 180, 120), 0.04), flash=((255, 255, 255), 0.3 * math.exp(-abs(t - D * 0.6) * 10)))

def nora_sombra(t, D, fi):
    zz = ease(seg(t, 0, D * 0.6))
    F = Frame(base("cuarto"), dict(x=lerp(600, 660, zz), y=lerp(880, 780, zz), z=lerp(1.4, 1.8, zz),
                                  sx=noise(t * 35) * 5 * zz, sy=noise(t * 35, 2) * 5 * zz))
    cuarto_luz(F, t)
    lampara_pie(F, 30, PISO)
    ojos = ease(seg(t, D * 0.2, D * 0.4)); gira = ease(seg(t, D * 0.5, D * 0.75))
    ps = mix(pose(head=-4, a1u=20, a2u=-20), pose(head=10, a1u=80, a1l=10, a2u=-20), gira)     # la sombra alarga el brazo
    sombra_de(F, NORA, ps, 630, PISO, f=1, extra=("coleta",), ojos=ojos, gira=gira)
    NORA.draw(F, pose(head=-4, a1u=20, a2u=-20), 520, PISO, f=1, face="neutral")
    J = NINA.draw(F, add(SCARED, jitter(t, 4, 2)), 820, PISO, f=-1, face="scared")
    coletas(F, J, 0.8)
    img = iluminar(F.finish(), F, [], glows=[((30, 660), 600, 0.9), ((540, 350), 420, 0.7)], amb=0.45, warm=CALIDA)
    return img, dict(grain=10, tint=((255, 0, 30), 0.14 * gira),
                     flash=((255, 30, 40), 0.3 * math.exp(-abs(t - D * 0.3) * 10)),
                     glitch=0.4 if (fi % 4 == 0 and t > D * 0.3) else 0.0)

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    return F.finish(), {}

ESCENA_FN = dict(sombra_viva=sombra_viva, llamada=llamada, viaje=viaje, sombras_calle=sombras_calle, cuarto19=cuarto19, sin_sombra=sin_sombra,
                 nora_sombra=nora_sombra, final=final)
PAUSA = dict(sombra_viva=0.8, llamada=0.6, viaje=0.6, sombras_calle=0.7, cuarto19=0.4, sin_sombra=1.1, nora_sombra=1.8, final=2.6)
