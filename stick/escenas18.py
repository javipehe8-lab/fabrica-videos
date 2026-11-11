"""Escenas del episodio 18 (FINAL DE TEMPORADA 2, "El último cristal"): las manos del Asomado tienen a Nora; sale el sol
y Leo golpea el primer espejo con la barra; el cristal se raja con el Asomado dentro y Nora se suelta; otro golpe y estalla;
los niños de la fábrica despiertan; Lucía vuelve a casa y la ciudad destapa sus ventanas. Giro de temporada 3: esa noche
Lucía apaga la luz y su sombra se queda de pie en la pared, con dos ojos blancos."""
import math, random
from motor import *
from escenas import base, cuarto, GLASS
from escenas6 import NINA, coletas
from escenas7 import NINO
from escenas12 import asomado
from escenas13 import fondo as fondo13, asomado_en, panel, nave, dormido_panel, PISO, VERDE
from escenas14 import esquirlas, suelo_cristales, marco_roto
from escenas15 import iluminar_
from escenas16 import fondo, EX, EY, EW, EH
from escenas17 import suelo, primer_espejo, marco_primero, ventanuco, barra, dedos_fuera, ALBA

SOL = (255, 200, 130)
NEGRA = Fig(shirt=(4, 4, 8), limb=(4, 4, 8), scale=0.8 * 1.35)

# ---------- piezas nuevas ----------
def rayo_sol(F, k, x=820, y=380):
    """haz de luz del amanecer que entra por el ventanuco y cae sobre el primer espejo"""
    if k <= 0: return
    for i in range(3):                                                          # bandas de luz suaves
        col = tuple(int(lerp(a, b, k * (0.45 - 0.12 * i))) for a, b in zip((22, 10, 26), (255, 170, 110)))
        sh = i * 30
        F.poly([(x + 20 + sh, y + 30), (x + 140 - sh, y + 110), (EX + EW * (0.75 - 0.1 * i), EY + EH), (EX + EW * (0.2 + 0.1 * i), EY + EH * 0.4)], fill=col)

def grietas(F, c, k, seed=5, n=9):
    """grietas que se abren desde el punto del golpe"""
    if k <= 0: return
    r = random.Random(seed)
    for _ in range(n):
        a = r.uniform(0, 2 * math.pi); ln = r.uniform(180, 520) * ease(k)
        pts = [c]; x, y = c
        for s in range(4):
            a += r.uniform(-0.5, 0.5); x += math.cos(a) * ln / 4; y += math.sin(a) * ln / 4
            x = min(max(x, EX + 6), EX + EW - 6); y = min(max(y, EY + 6), EY + EH - 6)
            pts.append((x, y))
        F.line(pts, (230, 240, 236), 4)

def edificios_luz(F, x0, x1, piso, seed=0, k=0.0):
    """edificios: k=0 ventanas tapadas con periódico y cinta; k=1 destapadas y con luz cálida"""
    r = random.Random(seed); x = x0
    while x < x1:
        w = r.randint(150, 260); h = r.randint(500, 1000); top = piso - h
        F.rect(x, top, x + w - 10, piso, fill=(30, 30, 46))
        for wy in range(int(top) + 30, piso - 60, 62):
            for wx in range(x + 18, x + w - 34, 44):
                g = r.randint(120, 160); kk = clamp(k * 1.6 - r.random() * 0.6, 0, 1)
                col = tuple(int(lerp(a, b, kk)) for a, b in zip((g, g - 6, g - 20), (255, 214, 130)))
                F.rect(wx, wy, wx + 22, wy + 32, fill=col)
                if kk < 0.5:
                    F.line([(wx + 2, wy + 2), (wx + 20, wy + 30)], (90, 82, 64), 2, round_=False)
                    F.line([(wx + 20, wy + 2), (wx + 2, wy + 30)], (90, 82, 64), 2, round_=False)
        x += w

def sombra_pared(F, x, y, t, ojos=0.0, gira=0.0):
    """la sombra de Lucía, de pie en la pared, más grande que ella; ojos blancos que se abren"""
    p = pose(head=lerp(0, 22, gira), a1u=8 + 4 * math.sin(t * 2), a1l=6, a2u=-8, a2l=6)
    J = NEGRA.draw(F, p, x, y, f=1, snap=False, face="closed")
    hx, hy = J["head"]
    for dx in (-30, 28):                                                        # coletas de sombra
        F.ellipse((hx + dx, hy + 6), 14, 26, fill=(4, 4, 8))
    if ojos > 0:
        g = int(255 * ojos); sc = 1.35
        for dx in (-12, 14):
            F.ellipse((hx + dx * sc + 14 * gira, hy - 6), 7 * sc, 7 * sc * ojos, fill=(g, g, g))
    return J

def lucia_acostada(F, x, y, t, ojos=False):
    p = pose(body=0, head=0, a1u=10, a1l=10, a2u=-10, a2l=10, l1u=4, l1l=0, l2u=-4, l2l=0)
    J = NINA.draw(F, p, x, y, f=1, rot=-88, snap=False, face="scared" if ojos else "closed")
    coletas(F, J, 0.8)
    return J

# ---------- escenas ----------
def agarrada(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(650, 660, zp), y=lerp(880, 840, zp), z=lerp(1.05, 1.25, zp),
                                  sx=noise(t * 30) * 5, sy=noise(t * 30, 2) * 5))
    suelo(F)
    ventanuco(F, 820, 380, 0.6 + 0.2 * zp)
    primer_espejo(F, t, luz=0.9)
    asomado_en(F, (EX + EW / 2, EY + 320), 1.0, t, mueca=0.8)
    marco_primero(F, t)
    tir = 0.5 + 0.5 * math.sin(t * 5)
    nx = lerp(900, 860, ease(zp)) - 12 * tir
    NORA.draw(F, add(pose(body=-14, head=-10, a1u=-40, a1l=-30, a2u=40, a2l=60), jitter(t, 4, 2)), nx, PISO, f=-1, face="scared")
    dedos_fuera(F, 1.0, t, nx + 60)
    LEO.draw(F, pose(head=-12, a1u=120, a1l=30), 1000, PISO, f=-1, face="scared")
    img = iluminar_(F, [((EX + EW / 2, EY + 360), 500, 1.0), ((880, 1000), 420, 0.6)])
    return img, dict(grain=9, tint=(VERDE, 0.12), flash=(VERDE, 0.4 * (1 - seg(t, 0, 0.35))),
                     glitch=0.3 if fi % 5 == 0 else 0.0)

def alba(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(680, 700, zp), y=lerp(860, 820, zp), z=lerp(1.05, 1.2, zp)))
    suelo(F)
    sol = ease(seg(t, 0, D * 0.5))
    ventanuco(F, 820, 380, 0.8 + 0.2 * sol)
    rayo_sol(F, sol)
    primer_espejo(F, t, luz=0.8)
    asomado_en(F, (EX + EW / 2, EY + 320), 1.0, t, mueca=0.5)
    marco_primero(F, t)
    NORA.draw(F, pose(body=-14, head=-10, a1u=-40, a1l=-30, a2u=40, a2l=60), 850, PISO, f=-1, face="scared")
    dedos_fuera(F, 1.0, t, 910)
    sube = ease(seg(t, D * 0.15, D * 0.6))
    J = LEO.draw(F, mix(pose(head=-10, a1u=60, a1l=40), pose(head=-16, body=6, a1u=175, a1l=10, a2u=150, a2l=20), sube),
                 1000, PISO, f=-1, face="talk" if (t > D * 0.55 and int(t * 8) % 2) else "angry")
    hx, hy = J["a1h"]
    F.line([(hx, hy + 30), (hx + 40 * sube, hy - 190)], (180, 180, 190), 12)       # la barra en alto
    img = iluminar_(F, [((EX + EW / 2, EY + 400), 480, 0.8), ((900, 440), 300, 0.9 * sol), ((980, 900), 380, 0.6)])
    return img, dict(grain=8, tint=(ALBA, 0.06 + 0.08 * sol), flash=(SOL, 0.2 * sol * (1 - seg(t, D * 0.5, D))))

def raja(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(660, 680, zp), y=lerp(820, 860, zp), z=lerp(1.2, 1.05, zp),
                                  sx=noise(t * 40) * 9 * (1 - zp), sy=noise(t * 40, 2) * 9 * (1 - zp)))
    suelo(F)
    ventanuco(F, 820, 380, 1.0)
    rayo_sol(F, 1.0)
    primer_espejo(F, t, luz=0.9)
    asomado_en(F, (EX + EW / 2, EY + 320), 1.0, t, mueca=1.0)
    grietas(F, (EX + EW * 0.7, EY + 470), seg(t, 0, D * 0.35))
    marco_primero(F, t)
    suelta = ease(seg(t, D * 0.25, D * 0.6))
    if suelta < 1: dedos_fuera(F, 1 - suelta, t, 900)
    NORA.draw(F, mix(pose(body=-14, head=-10, a1u=-40, a1l=-30, a2u=40, a2l=60), pose(body=20, head=10, a1u=80, a1l=40, a2u=100, a2l=30, l1u=30, l1l=-40), suelta),
              lerp(860, 940, suelta), PISO, f=-1, face="scared")
    LEO.draw(F, pose(head=-6, body=-10, a1u=60, a1l=20, a2u=40), 1030, PISO, f=-1, face="angry")
    img = iluminar_(F, [((EX + EW / 2, EY + 400), 520, 1.0), ((900, 1000), 420, 0.6)])
    return img, dict(grain=9, tint=(ALBA, 0.1), flash=((255, 255, 255), 0.7 * math.exp(-t * 7)),
                     glitch=0.5 if (fi % 3 == 0 and t < D * 0.5) else 0.0)

def estalla(t, D, fi):
    k = seg(t, D * 0.2, D)
    F = Frame(fondo("risa"), dict(x=lerp(620, 640, k), y=lerp(800, 840, k), z=lerp(1.2, 1.05, ease(k)),
                                  sx=noise(t * 45) * 12 * (1 - k), sy=noise(t * 45, 2) * 12 * (1 - k)))
    suelo(F)
    ventanuco(F, 820, 380, 1.0)
    rayo_sol(F, 1.0)
    if t < D * 0.2:
        primer_espejo(F, t, luz=1.0)
        asomado_en(F, (EX + EW / 2, EY + 320), 1.0, t, mueca=1.0)
        grietas(F, (EX + EW * 0.7, EY + 470), 1.0, n=14)
    else:
        marco_roto(F, EX, EY, EW, EH, seed=8)
        if k < 0.35:                                                            # la cara se deshace en el destello
            asomado_en(F, (EX + EW / 2 + noise(t * 50) * 30, EY + 320), 1 - k / 0.35, t, mueca=1.0)
        suelo_cristales(F, EX - 200, EX + EW + 300, seed=4)
    marco_primero(F, t)
    esquirlas(F, (EX + EW / 2, EY + 420), k * 1.2, seed=11, n=40)
    LEO.draw(F, pose(head=6, body=-14, a1u=120, a1l=20, a2u=100, a2l=30), 830, PISO, f=-1, face="angry")
    NORA.draw(F, SCARED, 970, PISO, f=-1, face="scared")
    img = iluminar_(F, [((EX + EW / 2, EY + 400), 560, 1.0), ((900, 1000), 420, 0.6)])
    return img, dict(grain=9, tint=(ALBA, 0.12), flash=((255, 255, 255), 0.9 * math.exp(-abs(t - D * 0.2) * 9)),
                     glitch=0.6 if (fi % 2 == 0 and D * 0.15 < t < D * 0.45) else 0.0)

def despiertos(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo13("sala"), dict(x=lerp(500, 600, zp), y=lerp(940, 920, zp), z=lerp(1.0, 1.12, zp)))
    nave(F)
    rompe = seg(t, D * 0.3, D * 0.45)
    for k in range(4):
        x = 30 + k * 260; nina = k % 2 == 0; fig = NINA if nina else NINO
        if rompe < 1:
            panel(F, x, 480, 200, 600, brillo=0.3, luz=0.5)
            J = dormido_panel(F, x, 480, 200, 600, fig, t, nina=nina)
        else:
            marco_roto(F, x, 480, 200, 600, seed=k + 20)
            sal = ease(seg(t, D * 0.45, D * 0.8))
            J = fig.draw(F, pose(head=-6, a1u=lerp(10, 150, sal) + 20 * math.sin(t * 8 + k) * sal, a1l=20), x + 100, lerp(1050, PISO, sal),
                         f=1, face="happy")
            if nina: coletas(F, J, 0.8)
    if rompe > 0: esquirlas(F, (540, 800), seg(t, D * 0.3, D * 0.7), seed=2, n=30)
    suelo_cristales(F, -100, 1100, seed=6)
    img = iluminar_(F, [((540, 800), 700, 0.5 + 0.5 * rompe)])
    return img, dict(grain=8, tint=(SOL, 0.05 + 0.08 * rompe), flash=((255, 255, 255), 0.6 * math.exp(-abs(t - D * 0.32) * 10)))

def casa_lucia(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("amanecer"), dict(x=lerp(460, 600, zp), y=lerp(1000, 1020, zp), z=lerp(1.05, 1.15, zp)))
    F.circle((860, 520), 90, fill=(255, 236, 190))
    edificios_luz(F, -500, 1600, 1180, seed=12, k=ease(seg(t, D * 0.1, D * 0.8)))
    F.rect(-700, 1180, 1800, 1300, fill=(54, 50, 60)); F.rect(-700, 1300, 1800, 2700, fill=(30, 28, 36))
    F.line([(-700, 1300), (1800, 1300)], (84, 76, 86), 6)
    w = ease(seg(t, 0, D * 0.6)); stop = w >= 1
    J = NINA.draw(F, pose(head=-6, a1u=150 + 30 * math.sin(t * 8), a1l=20) if stop else run(t, 0.8), lerp(300, 840, w), 1300, f=-1 if stop else 1, face="happy")
    coletas(F, J, 0.8)
    CARMEN.draw(F, pose(head=-6, a1u=40), 230, 1300, f=1, face="happy")
    NORA.draw(F, pose(head=-8, a1u=150 + 30 * math.sin(t * 8 + 1), a1l=20), 380, 1300, f=1, face="happy")
    LEO.draw(F, pose(head=-8, a1u=40, a2u=-150, a2l=-20), 520, 1300, f=1, face="happy")
    return F.finish(), dict(grain=6, tint=(SOL, 0.06))

def su_sombra(t, D, fi):
    off = seg(t, D * 0.2, D * 0.28) >= 1
    zz = ease(seg(t, D * 0.45, D))
    F = Frame(base("cuarto"), dict(x=lerp(330, 260, zz), y=lerp(960, 900, zz), z=lerp(1.45, 2.1, zz),
                                  sx=noise(t * 30) * 4 * zz, sy=noise(t * 30, 2) * 4 * zz))
    cuarto(F, t=t)
    F.ellipse((235, 900), 145, 250, fill=(48, 50, 84) if off else (120, 100, 90))       # pared iluminada tras la cama
    # lamparita de la mesilla
    F.rect(470, 1080, 560, 1250, fill=(60, 46, 40)); F.line([(515, 1080), (515, 1010)], (90, 80, 70), 6)
    F.poly([(480, 1010), (550, 1010), (535, 960), (495, 960)], fill=(255, 220, 150) if not off else (70, 60, 50))
    ojos = ease(seg(t, D * 0.5, D * 0.65))
    sombra_pared(F, 240, 1060, t, ojos=ojos, gira=ease(seg(t, D * 0.7, D * 0.9)))   # en la pared, detrás de la cama
    F.rect(80, 1150, 440, 1250, fill=(70, 80, 116)); F.rect(80, 1132, 440, 1160, fill=(150, 160, 196))
    F.rect(100, 1100, 190, 1140, fill=(205, 210, 230))
    lucia_acostada(F, 250, 1115, t, ojos=t > D * 0.75)
    glows = [((515, 990), 420, 1.0)] if not off else [((540, 690), 300, 0.45), ((240, 880), 260, 0.5)]
    img = iluminar_(F, glows)
    return img, dict(grain=10, dark=0.0 if not off else 0.15, tint=((120, 120, 255), 0.08 if off else 0.02),
                     flash=((255, 255, 255), 0.4 * math.exp(-abs(t - D * 0.55) * 12) if off else 0.0),
                     glitch=0.3 if (off and fi % 6 == 0 and t > D * 0.55) else 0.0)

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    return F.finish(), {}

ESCENA_FN = dict(agarrada=agarrada, alba=alba, raja=raja, estalla=estalla, despiertos=despiertos,
                 casa_lucia=casa_lucia, su_sombra=su_sombra, final=final)
PAUSA = dict(agarrada=0.5, alba=0.55, raja=0.55, estalla=0.6, despiertos=0.5, casa_lucia=0.5, su_sombra=1.5, final=2.2)
