"""Si oyes esto a las 3AM — 9: "Las huellas en la nieve". Noche nevada: el jardín visto desde tu ventana con un rastro de
huellas que solo llega a la puerta, el recibidor (puerta de la calle de la historia 3, con cerrojo y charcos), la escalera
de la historia 1 con huellas mojadas y tu cuarto, donde algo alto y nevado está de pie junto a tu cama.
Piezas nuevas reutilizables: nevada (copos), jardin_nevado (rastro de huellas en perspectiva), huella, cerrojo,
charcos_suelo, cosa_nevada (figura alta cubierta de nieve que gotea)."""
import math, random
from PIL import ImageDraw
from motor import *
from escenas2 import big
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am, cuarto_casa, escalera_casa, CASA_A, CASA_B
from escenas3am2 import cara_palida, dedos, PIEL
from escenas3am3 import paredes, puerta_calle, DX0, DX1, DY0, LATON, PISO
from escenas3am5 import _osc

NIEVE = (150, 162, 196)              # nieve de noche (azulada)
NIEVE_H = (70, 80, 112)              # huellas hundidas
FRIA = (170, 200, 255)               # luz de luna / farol frío
FAROL = (255, 206, 140)              # luz del porche
AGUA = (120, 160, 220)               # charcos (brillo)
NEVADA = Fig(shirt=(58, 64, 80), limb=(200, 204, 214), scale=1.38)   # la cosa: abrigo oscuro, piel helada, demasiado alta
_BG = {}
def fondo(k="casa"):
    if k not in _BG:
        _BG[k] = gradient(CASA_A, CASA_B) if k == "casa" else gradient((10, 14, 32), (30, 36, 60))
    return _BG[k]

def nevada(F, t, x0=-200, x1=1300, y0=0, y1=1900, n=70, seed=3, r=4, col=(220, 228, 245), vel=90):
    rr = random.Random(seed)
    for _ in range(n):
        bx, by, sp, ph = rr.uniform(x0, x1), rr.uniform(0, 1), rr.uniform(0.6, 1.4), rr.uniform(0, 6.3)
        y = y0 + ((by * (y1 - y0) + t * vel * sp) % (y1 - y0))
        x = bx + math.sin(t * 1.3 + ph) * 18
        F.circle((x, y), r * sp, fill=col)

def huella(F, c, ang, s=1.0, col=NIEVE_H, agua=False):
    """huella de pie descalzo, larga y estrecha (demasiado larga), con la punta hacia ang (grados)"""
    x, y = c; a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a) * 0.45                   # aplastada en vertical: perspectiva del suelo
    c1 = col if not agua else _osc(AGUA, 0.55)
    F.ellipse((x + ux * 10 * s, y + uy * 10 * s), 17 * s, 9 * s, fill=c1)                  # planta
    F.ellipse((x - ux * 14 * s, y - uy * 14 * s), 11 * s, 7 * s, fill=c1)                  # talón
    for i in range(4):                                                                     # dedos largos
        px = x + ux * 32 * s - uy * (i - 1.5) * 9 * s; py = y + uy * 32 * s + ux * (i - 1.5) * 4 * s
        F.circle((px + ux * 6 * s, py + uy * 6 * s), 3.4 * s, fill=c1)
    if agua: F.ellipse((x + ux * 4 * s - 4 * s, y - 2 * s), 7 * s, 2.5 * s, fill=(200, 220, 255))   # brillo del agua

# rastro: del portón (lejos, arriba a la izquierda) a la puerta de casa (cerca, abajo a la derecha)
RA, RC, RB = (250, 560), (230, 1010), (930, 1150)
def _bez(u):
    x = (1 - u) ** 2 * RA[0] + 2 * (1 - u) * u * RC[0] + u * u * RB[0]
    y = (1 - u) ** 2 * RA[1] + 2 * (1 - u) * u * RC[1] + u * u * RB[1]
    return x, y

def rastro(F, k=1.0, n=20, rojo=0.0):
    """huellas a lo largo del rastro (solo de ida). k: fracción visible desde el portón"""
    for i in range(n):
        u = i / (n - 1)
        if u > k: break
        x, y = _bez(u); x2, y2 = _bez(min(1, u + 0.01))
        ang = math.degrees(math.atan2((y2 - y) / 0.45, x2 - x))
        s = lerp(0.32, 1.0, (y - RA[1]) / (RB[1] - RA[1]))
        side = 1 if i % 2 else -1
        nx, ny = -(y2 - y), (x2 - x); ln = math.hypot(nx, ny) or 1
        col = NIEVE_H if rojo <= 0 or u < 0.8 else tuple(int(lerp(a, b, rojo)) for a, b in zip(NIEVE_H, (34, 36, 58)))   # se oscurecen
        huella(F, (x + nx / ln * 14 * s * side, y + ny / ln * 6 * s * side), ang, s * 1.15, col)

def jardin_nevado(F, t, k=1.0, farol=0.8, rojo=0.0):
    """jardín visto desde arriba: cielo, árboles, valla y portón al fondo; la pared de casa y la puerta con el farol a la derecha"""
    F.rect(-600, -400, 1700, 560, fill=(12, 16, 34))
    F.circle((820, 330), 60, fill=(200, 208, 228)); F.circle((846, 312), 56, fill=(12, 16, 34))       # luna menguante
    rr = random.Random(5)
    for i in range(16):                                                                              # árboles del fondo
        x = -300 + i * 110 + rr.uniform(-30, 30); h = rr.uniform(160, 320)
        F.poly([(x - 60, 560), (x + 60, 560), (x, 560 - h)], fill=(8, 10, 22))
        F.poly([(x - 34, 560 - h * 0.45), (x + 34, 560 - h * 0.45), (x, 560 - h * 0.95)], fill=(40, 46, 70))   # nieve en las ramas
    F.rect(-600, 556, 1700, 2000, fill=NIEVE)
    for yy in range(600, 1500, 70):                                                                  # ondulaciones de la nieve
        F.line([(-600, yy), (1700, yy + 10)], _osc(NIEVE, 0.94), 6)
    for x in range(-560, 1700, 46):                                                                  # valla
        if 200 < x < 310: continue
        F.rect(x, 500, x + 14, 566, fill=(36, 34, 40)); F.rect(x, 494, x + 14, 502, fill=(210, 216, 232))
    F.line([(-600, 520), (200, 520)], (36, 34, 40), 6); F.line([(310, 520), (1700, 520)], (36, 34, 40), 6)
    F.rect(200, 480, 214, 566, fill=(30, 28, 34)); F.rect(296, 480, 310, 566, fill=(30, 28, 34))   # portón abierto
    F.poly([(214, 500), (246, 470), (246, 560), (214, 566)], fill=(46, 42, 50))
    # pared de casa y puerta (derecha)
    F.rect(860, 640, 1700, 1500, fill=(40, 38, 50))
    F.poly([(820, 820), (1700, 820), (1700, 760), (880, 760)], fill=(26, 26, 34))
    F.rect(820, 806, 1700, 822, fill=(210, 216, 232))                                                 # nieve en el tejadillo
    F.rect(880, 900, 1020, 1150, fill=(58, 40, 30), outline=(26, 18, 14), w=5)                      # puerta
    F.circle((900, 1030), 7, fill=LATON)
    F.rect(840, 1146, 1060, 1170, fill=(110, 114, 140))                                              # escalón
    if farol > 0:
        F.rect(1040, 870, 1062, 910, fill=_osc(FAROL, farol)); F.circle((1051, 890), 10, fill=(255, 240, 210))
    rastro(F, k, rojo=rojo)

def ventana_marco(F, x0=80, y0=240, x1=1000, y1=1220):
    """tu ventana por dentro: pared, marco con cruz, alféizar con el reloj y escarcha en las esquinas"""
    col = (24, 26, 40)
    F.rect(-600, -400, 1700, y0, fill=col); F.rect(-600, y1, 1700, 2400, fill=col)
    F.rect(-600, -400, x0, 2400, fill=col); F.rect(x1, -400, 1700, 2400, fill=col)
    F.rect(x0 - 24, y0 - 24, x1 + 24, y1 + 24, outline=(70, 66, 76), w=24)
    mx = (x0 + x1) / 2; my = (y0 + y1) * 0.45
    F.line([(mx, y0), (mx, y1)], (70, 66, 76), 18); F.line([(x0, my), (x1, my)], (70, 66, 76), 18)
    for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):                                          # escarcha
        F.circle((cx, cy), 70, fill=(120, 136, 170)); F.circle((cx, cy), 44, fill=(150, 166, 200))
    F.rect(x0 - 70, y1 + 20, x1 + 70, y1 + 60, fill=(90, 80, 72))                                    # alféizar
    reloj_3am(F, 540, y1 - 10, 0.55)

def cerrojo(F, echado=1.0, brillo=0.0, y=980):
    """cerrojo de pasador en el canto de la puerta de la calle: el pasador entra en la guía del marco"""
    F.rect(DX1 - 96, y - 24, DX1 - 14, y + 24, fill=(150, 126, 70), outline=(90, 74, 40), w=3)       # placa
    F.rect(DX1 + 10, y - 26, DX1 + 40, y + 26, fill=(140, 116, 64), outline=(90, 74, 40), w=3)       # guía en el marco
    bx = lerp(DX1 - 20, DX1 + 34, ease(echado))
    F.rect(DX1 - 86, y - 9, bx, y + 9, fill=LATON)                                                    # pasador
    F.line([(DX1 - 60, y), (DX1 - 60, y + 34)], LATON, 10)                                           # palanca bajada
    F.circle((DX1 - 60, y + 38), 9, fill=LATON)
    if brillo > 0: F.circle((DX1 + 12, y - 4), 6 + 10 * brillo, fill=(255, 248, 220))
    return (DX1, y)

def suelo_recibidor(F, charcos=1.0, t=0.0, huellas_k=1.0):
    """franja de suelo vista un poco desde arriba, con el felpudo nevado y huellas mojadas que se alejan de la puerta (hacia la izquierda)"""
    F.rect(-900, PISO, 2000, PISO + 160, fill=(34, 30, 34))
    for x in range(-900, 2000, 120): F.line([(x, PISO), (x - 40, PISO + 160)], (26, 22, 26), 4)    # tablas
    F.ellipse((700, PISO + 40), 150, 26, fill=(70, 50, 44))                                           # felpudo
    if charcos > 0:
        F.ellipse((700, PISO + 34), 120 * charcos, 16, fill=_osc(AGUA, 0.45))
        F.ellipse((650, PISO + 30), 40 * charcos, 5, fill=(190, 210, 245))
        for i in range(7):                                                                             # huellas mojadas hacia la escalera
            u = i / 6
            if u > huellas_k: break
            x = lerp(560, -260, u); yy = PISO + (60 if i % 2 else 100)
            huella(F, (x, yy), 180, 1.1, agua=True)

def cosa_nevada(F, p, x, y, t=0.0, f=-1, sc=1.0, abre=0.3, cara=True, snap=True):
    """la cosa: altísima, abrigo oscuro, hombros y pelo cubiertos de nieve, goteando sobre el suelo"""
    old = NEVADA.scale; NEVADA.scale = 1.38 * sc
    J = NEVADA.draw(F, p, x, y, f=f, face="closed", t=t, stretch=1.22, snap=snap)
    NEVADA.scale = old
    sx, sy = J["sh"]; hx, hy = J["hip"]
    F.poly([(sx - 36 * sc, sy), (sx + 36 * sc, sy), (hx + 58 * sc, hy + 120 * sc), (hx - 58 * sc, hy + 120 * sc)], fill=(48, 54, 70))  # abrigo
    F.poly([(sx - 40 * sc, sy + 2 * sc), (sx - 28 * sc, sy - 8 * sc), (sx + 28 * sc, sy - 8 * sc), (sx + 40 * sc, sy + 2 * sc),
            (sx + 30 * sc, sy + 6 * sc), (sx - 30 * sc, sy + 6 * sc)], fill=(206, 214, 232))                  # nieve sobre los hombros
    if cara:
        cx, cy = J["head"]; r = 46 * sc
        cara_palida(F, (cx, cy), r, abre=abre)
        rr = random.Random(9)
        for _ in range(14):                                                                           # escarcha en el pelo
            a = rr.uniform(math.pi * 1.1, math.pi * 1.9); d = rr.uniform(0.85, 1.05)
            F.circle((cx + math.cos(a) * r * 0.8 * d, cy - r * 0.15 + math.sin(a) * r * 1.15 * d), rr.uniform(1.5, 3.2) * sc, fill=(200, 210, 230))
    # goteo y charco a los pies
    fy = max(J["l1f"][1], J["l2f"][1])
    F.ellipse((x, fy + 6), 90 * sc, 12 * sc, fill=_osc(AGUA, 0.4))
    for i, gx in enumerate((-40, 6, 44)):
        u = (t * 1.1 + i * 0.37) % 1
        gy = lerp(hy + 110 * sc, fy, u)
        F.ellipse((x + gx * sc, gy), 3 * sc, 6 * sc, fill=(170, 200, 250))
    return J

# ---------- escenas ----------
def ventana(t, D, fi):
    """primer fotograma: el reloj 3:00 en rojo muy cerca, en el alféizar; detrás, la nieve y el rastro hasta la puerta"""
    k = ease(seg(t, 0, D * 0.85))
    F = Frame(fondo("noche"), dict(x=lerp(540, 560, k), y=lerp(1100, 800, k), z=lerp(2.1, 1.05, k)))
    jardin_nevado(F, t, k=1.0, farol=0.7 + 0.3 * (noise(t * 5, 4) > -0.6))
    nevada(F, t, 60, 1000, 240, 1220, n=60)
    ventana_marco(F)
    img = iluminar(F.finish(), F, [], glows=[((540, 1210), 230, 0.8), ((1051, 890), 200, 0.7), ((540, 800), 600, 0.55)],
                   amb=0.3, warm=FRIA)
    return img, dict(grain=9, flash=((255, 40, 40), 0.2 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.08))

def ninguna(t, D, fi):
    """la cámara sigue el rastro desde el portón hasta el escalón: todas las huellas apuntan a la puerta"""
    k = ease(seg(t, 0, D * 0.8))
    u = lerp(0.05, 0.95, k)
    cx, cy = _bez(u)
    F = Frame(fondo("noche"), dict(x=cx + 60, y=cy - 60, z=lerp(1.9, 2.4, k)))
    jardin_nevado(F, t, k=1.0, farol=0.85, rojo=seg(t, D * 0.7, D))
    nevada(F, t, -200, 1300, 300, 1400, n=50, r=3)
    img = iluminar(F.finish(), F, [], glows=[((1051, 890), 220, 0.8)], amb=0.36, warm=FRIA)
    return img, dict(grain=10, tint=((255, 0, 30), 0.14 * seg(t, D * 0.7, D)))

def bajas(t, D, fi):
    """bajas al recibidor: vaho en la boca, felpudo empapado y huellas mojadas en el suelo (pista)"""
    w = ease(seg(t, 0, D * 0.5))
    k = ease(seg(t, D * 0.45, D))
    F = Frame(fondo(), dict(x=lerp(420, 560, k), y=lerp(1120, 1210, k), z=lerp(1.4, 1.75, k)))
    paredes(F)
    puerta_calle(F, rellano=0.0)
    cerrojo(F, echado=1.0)
    suelo_recibidor(F, charcos=1.0, t=t)
    x = lerp(-60, 420, w)
    J = TU.draw(F, walk(t, 0.6, 0.7) if w < 1 else pose(head=14, body=4, a1u=30, a1l=40, a2u=-20, a2l=30), x, PISO, f=1,
                face="neutral" if w < 1 else "scared")
    hx, hy = J["head"]
    for i in range(2):                                                                 # vaho: hace frío dentro
        u = (t * 0.8 + i * 0.5) % 1
        if u < 0.7: F.circle((hx + 30 + 40 * u, hy + 6 - 20 * u), 6 + 12 * u, fill=_osc((150, 160, 190), 0.75 - 0.4 * u))
    img = iluminar(F.finish(), F, [], glows=[((700, PISO + 30), 260, 0.65), ((hx, hy), 200, 0.35), ((700, 1040), 160, 0.25)],
                   amb=0.24, warm=FRIA)
    return img, dict(grain=10)

def cerrojo_(t, D, fi):
    """primer plano del cerrojo, echado por dentro. Brilla. Tu mano se acerca y no se atreve a tocarlo"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=DX1 - 30, y=lerp(1000, 990, k), z=lerp(3.0, 3.8, k)))
    paredes(F)
    puerta_calle(F, rellano=0.0)
    c = cerrojo(F, echado=1.0, brillo=seg(t, D * 0.3, D * 0.4) * (1 - seg(t, D * 0.45, D * 0.65)))
    m = ease(seg(t, D * 0.2, D * 0.6))
    hx, hy = lerp(DX1 - 400, DX1 - 150, m), 1020 + noise(t * 30, 2) * 4
    F.line([(hx - 200, hy + 120), (hx, hy)], TU.shirt, 30); F.circle((hx + 10, hy - 4), 16, fill=(240, 232, 222))
    img = iluminar(F.finish(), F, [], glows=[(c, 160, 0.85)], amb=0.2, warm=FAROL)
    return img, dict(grain=11, tint=((255, 0, 30), 0.2 * seg(t, D * 0.5, D)), dark=0.05)

def charcos(t, D, fi):
    """las huellas mojadas suben la escalera, peldaño a peldaño, hasta la puerta entreabierta de tu cuarto"""
    k = ease(seg(t, D * 0.15, D))
    F = Frame(fondo(), dict(x=lerp(820, 260, k), y=lerp(1120, 760, k), z=1.45))
    path = escalera_casa(F)
    F.rect(-260, 300, 20, 700, fill=(6, 6, 10)); F.rect(-280, 280, 40, 300, fill=(60, 48, 40))     # puerta de tu cuarto, a oscuras
    F.poly([(20, 300), (90, 320), (90, 700), (20, 700)], fill=(62, 52, 46))
    F.rect(-260, 690, 20, 700, fill=_osc(FRIA, 0.25))
    n = 12; dx = (900 - 120) / n; dy = (1300 - 700) / n
    vis = lerp(0, n + 3, ease(seg(t, 0, D * 0.85)))
    for i in range(n):                                                                  # una huella en cada peldaño (de abajo arriba)
        kk = n - 1 - i
        if i > vis: break
        huella(F, (120 + (kk + 0.5) * dx, 700 + kk * dy + 8), 200, 0.9, agua=True)
    for i, x in enumerate((60, -60, -170)):                                             # y por el rellano, hacia tu puerta
        if n + i > vis: break
        huella(F, (x, 712), 180, 0.9, agua=True)
    TU.draw(F, add(pose(head=-18, body=-6, a1u=20, a1l=30, a2u=-20, a2l=30), jitter(t, 1.2, 3)), 1010, 1300, f=-1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((lerp(900, 100, k), lerp(1300, 700, k)), 360, 0.6), ((-120, 690), 200, 0.4)],
                   amb=0.22, warm=FRIA)
    return img, dict(grain=11, tint=((255, 0, 30), 0.1 * k))

def _quieta(t):
    return pose(body=-4, head=lerp(-16, -10, 0.5 + 0.5 * math.sin(t * 0.7)), a1u=8, a1l=4, a2u=-6, a2l=4, l1u=4, l1l=-2, l2u=-4, l2l=-2)

def cuarto(t, D, fi):
    """tu cuarto desde la puerta: tu cama deshecha y, de pie a su lado, algo alto cubierto de nieve mirándola"""
    k = ease(seg(t, 0, D))
    gira = ease(seg(t, D * 0.62, D * 0.8))
    F = Frame(fondo(), dict(x=lerp(520, 600, k), y=lerp(1000, 900, k), z=lerp(1.05, 1.6, k)))
    cuarto_casa(F, puerta_luz=0.0)
    F.poly([(60, 1140), (400, 1128), (430, 1160), (70, 1168)], fill=(110, 120, 160))                     # sábana revuelta
    p = _quieta(t); p["head"] = lerp(-16, 22, gira)
    J = cosa_nevada(F, p, 640, 1300, t=t, f=-1 if gira < 0.5 else 1, abre=0.25)
    for i in range(3):                                                                                     # huellas mojadas hasta la cama
        huella(F, (900 - i * 90, 1316 + (8 if i % 2 else -6)), 180, 0.9, agua=True)
    img = iluminar(F.finish(), F, [], glows=[(J["head"], 240, 0.6), ((640, 1300), 260, 0.45), ((300, 1140), 260, 0.3)],
                   amb=0.2, warm=FRIA)
    return img, dict(grain=12, tint=((255, 0, 30), 0.15 * gira), glitch=0.25 if abs(t - D * 0.7) < 0.08 else 0.0)

def voz(t, D, fi):
    """el golpe: su cara pálida, con nieve en el pelo, muy cerca. Inclina la cabeza y te habla"""
    hit = t >= D * 0.08
    sh = 14 * hit * (1 - seg(t, D * 0.25, D * 0.55))
    k = ease(seg(t, 0, D))
    p = _quieta(t); p["head"] = 22 + 14 * ease(seg(t, D * 0.3, D * 0.8))
    old = NEVADA.scale; NEVADA.scale = 1.38; J0 = NEVADA.joints(p, 640, 1300, f=1, snap=True, stretch=1.22); NEVADA.scale = old
    hx, hy = J0["head"]
    F = Frame(fondo(), dict(x=hx + noise(t * 30) * sh, y=hy + 60, z=lerp(3.4, 3.9, k), sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    cuarto_casa(F, puerta_luz=0.0)
    cosa_nevada(F, p, 640, 1300, t=t, f=1, abre=0.3 + 0.7 * abs(math.sin(t * 6)) * (t < D * 0.85))
    img = iluminar(F.finish(), F, [], glows=[((hx, hy), 170, 0.95)], amb=0.06, warm=FRIA)
    return img, dict(grain=12, flash=((255, 255, 255), max(0, 1 - (t - D * 0.08) / 0.25)) if hit else None,
                     glitch=0.4 if hit and fi % 3 and t < D * 0.55 else 0.0, tint=((255, 0, 30), 0.12 * hit))

def final(t, D, fi):
    """plano fijo: la cosa junto a tu cama, con la cabeza ladeada hacia ti; tú, en la puerta, sin poder moverte"""
    F = Frame(fondo(), dict(x=600, y=lerp(900, 890, ease(t / D)), z=1.15))
    cuarto_casa(F, puerta_luz=0.0)
    F.poly([(60, 1140), (400, 1128), (430, 1160), (70, 1168)], fill=(110, 120, 160))
    p = _quieta(t); p["head"] = 30
    J = cosa_nevada(F, p, 600, 1300, t=t, f=1, abre=0.35)
    TU.draw(F, add(pose(body=-6, a1u=40, a1l=60, a2u=-30, a2l=50), jitter(t, 1.5, 8)), 900, 1300, f=-1, face="scared")
    luz = 0.7 + 0.3 * (noise(t * 6, 7) > -0.5)
    img = iluminar(F.finish(), F, [], glows=[(J["head"], 220, 0.6 * luz), ((900, 1100), 220, 0.4)], amb=0.2, warm=FRIA)
    pp = ease_back(seg(t, D * 0.5, D * 0.6)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 180, 1040, 600), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 HAY HUELLAS"), 240, 62, (255, 255, 255)), (tr("QUE SOLO VIENEN…"), 315, 62, (255, 255, 255)),
                                 (tr("NO BUSQUES"), 410, 96, (255, 40, 50)), (tr("QUIÉN"), 520, 96, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 625, 850, 715), 26, fill=(230, 30, 50))
        d.text((540, 670), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.25 * pp if pp > 0 else 0), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(ventana=ventana, ninguna=ninguna, bajas=bajas, cerrojo=cerrojo_, charcos=charcos, cuarto=cuarto, voz=voz, final=final)
PAUSA = dict(ventana=0.5, ninguna=0.7, bajas=0.4, cerrojo=0.8, charcos=0.5, cuarto=0.7, voz=1.0, final=2.4)
