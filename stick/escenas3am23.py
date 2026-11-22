"""Si oyes esto a las 3AM — 23: "Los golpes en la pared". Tu hermano y tú os dais las buenas noches con tres golpes en la pared
que separa vuestros cuartos. A las tres suenan; contestas. Por la mañana tu hermano vuelve: durmió en casa de Dani. Su cuarto
estaba vacío: lo que llamaba era una cosa pálida, de pie contra la pared. La noche siguiente los golpes vienen de tu armario.
Piezas nuevas reutilizables: dos_cuartos (corte de dos cuartos separados por una pared: el de tu hermano a la izquierda y el tuyo
a la derecha, con cama alta, mesilla con el reloj y armario), armario_puertas (armario de dos puertas que tiemblan y se abren
una rendija, con ojos y dedos pálidos), HERMANO + hermano() (niño con pijama azul y mochila), alto (la cosa pálida y altísima de
pie, de perfil, que llama con los nudillos), puno (puño en primer plano que golpea) y golpes_k (pulsos de tres golpes)."""
import math
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am, CASA_A, CASA_B
from escenas3am2 import PIEL, cara_palida
from escenas3am3 import paredes, PISO
from escenas3am5 import _osc, cama_alta, manta, tu_tumbado, CAMA_X0, CAMA_X1, COLCHON, HUECO
from escenas3am18 import onomato

ROJO = (255, 40, 40)
LUNA = (170, 190, 255)
DIA = (226, 218, 196)
MUROX0, MUROX1 = -30, 40            # pared que separa los dos cuartos
HCAMA0, HCAMA1 = -700, -60          # cama de tu hermano (cabecero contra la pared)
ARM0, ARMW, ARMH = 940, 270, 600    # tu armario
HERMANO = Fig(shirt=(70, 110, 200), scale=0.72)
ALTO = Fig(shirt=PIEL, limb=PIEL, scale=1.45)
_BG = {}
def fondo(k="a"):
    if k not in _BG:
        _BG[k] = {"a": gradient(CASA_A, CASA_B), "d": gradient((70, 66, 70), (36, 34, 38)), "m": gradient((40, 30, 26), (20, 14, 12))}[k]
    return _BG[k]

def golpes_k(t, t0, gap=0.3, n=3):
    """0-1: lo que dura cada golpe (pico justo en t0 + i*gap)"""
    best = 0.0
    for i in range(n):
        d = t - (t0 + i * gap)
        if -0.06 < d < 0.12: best = max(best, 1 - abs(d) / (0.06 if d < 0 else 0.12))
    return best

def golpe_n(t, t0, gap=0.3, n=3):
    """cuántos golpes han sonado ya"""
    return sum(1 for i in range(n) if t >= t0 + i * gap)

# ---------- piezas ----------
def armario_puertas(F, t, jit=0.0, abre=0.0, ojos=0.0, dedos=0.0, nudillo=0.0, x=ARM0):
    """armario de dos puertas. jit: tiembla. abre 0-1: la puerta derecha se abre una rendija (negra dentro);
    ojos: dos brillos en la rendija; dedos: dedos pálidos que agarran el canto; nudillo: golpe desde dentro"""
    x += noise(t * 40) * jit
    y1, y0 = PISO, PISO - ARMH
    F.rect(x, y0, x + ARMW, y1 - 12, fill=(70, 50, 38), outline=(34, 22, 16), w=5)
    F.rect(x - 10, y0 - 18, x + ARMW + 10, y0, fill=(60, 42, 32), outline=(34, 22, 16), w=4)
    mx = x + ARMW / 2
    F.rect(x + 12, y0 + 14, mx - 4, y1 - 26, fill=(82, 60, 46), outline=(40, 28, 20), w=3)           # puerta izquierda
    F.rect(mx - 22, y0 + ARMH * 0.45, mx - 14, y0 + ARMH * 0.55, fill=(190, 168, 100))
    gap = 46 * ease(abre)
    if gap > 1:                                                                                      # rendija negra
        F.rect(mx + 2, y0 + 14, mx + 4 + gap, y1 - 26, fill=(2, 2, 4))
        if ojos > 0:
            for ey in (y0 + 210, ):
                for ex in (mx + 6 + gap * 0.3, mx + 6 + gap * 0.75):
                    F.circle((ex, ey), 4.2, fill=_osc((236, 236, 246), ojos))
        if dedos > 0:                                                                                # dedos que rodean el canto
            for i in range(4):
                fy = y0 + 280 + i * 22
                F.line([(mx + 2 + gap * 0.4, fy), (mx + 4 + gap + 14 * dedos, fy - 4), (mx + 4 + gap + 20 * dedos, fy + 10)], (8, 8, 12), 11)
                F.line([(mx + 2 + gap * 0.4, fy), (mx + 4 + gap + 14 * dedos, fy - 4), (mx + 4 + gap + 20 * dedos, fy + 10)], PIEL, 7)
    px = mx + 4 + gap
    F.poly([(px, y0 + 14), (px + (ARMW / 2 - 16) * (1 - 0.12 * ease(abre)), y0 + 14 - 6 * abre),
            (px + (ARMW / 2 - 16) * (1 - 0.12 * ease(abre)), y1 - 26 + 6 * abre), (px, y1 - 26)],
           fill=(82, 60, 46), outline=(40, 28, 20), w=3)                                             # puerta derecha
    F.rect(px + 10, y0 + ARMH * 0.45, px + 18, y0 + ARMH * 0.55, fill=(190, 168, 100))
    if nudillo > 0:                                                                                  # bulto del golpe en la madera
        F.circle((px + 60, y0 + 260), 14 + 10 * nudillo, outline=_osc((150, 120, 96), nudillo), w=4)
    for lx in (x + 14, x + ARMW - 26): F.rect(lx, y1 - 12, lx + 12, y1, fill=(40, 28, 20))
    return (mx, y0 + 230)

def cama_hermano(F, vacia=True):
    """la cama de tu hermano, espejo de la tuya: cabecero contra la pared, a la izquierda de ella"""
    F.rect(HCAMA1 - 10, PISO - 440, HCAMA1 + 30, PISO, fill=(80, 58, 46), outline=(40, 28, 20), w=4)
    F.rect(HCAMA0, HUECO, HCAMA1, PISO, fill=(4, 4, 7))
    for lx in (HCAMA0 + 14, HCAMA1 - 14): F.rect(lx - 10, HUECO, lx + 10, PISO, fill=(60, 44, 34))
    F.rect(HCAMA0, HUECO - 20, HCAMA1, HUECO + 6, fill=(78, 56, 42), outline=(40, 28, 20), w=3)
    F.rect(HCAMA0, COLCHON, HCAMA1, HUECO - 20, fill=(140, 170, 150))
    F.rect(HCAMA1 - 190, COLCHON - 34, HCAMA1 - 30, COLCHON + 2, fill=(222, 226, 240))
    if vacia:                                                                                        # cama hecha, lisa
        F.rect(HCAMA0, COLCHON - 10, HCAMA1 - 200, HUECO - 4, fill=(60, 110, 90))

def hermano_tumbado(F, t, face="closed"):
    J = HERMANO.draw(F, pose(a1u=30, a1l=80, a2u=10, a2l=20), HCAMA1 - 250, COLCHON - 12, f=-1, rot=90, snap=False, face=face, t=t)
    F.poly([(HCAMA1 - 270, COLCHON - 32), (HCAMA0 - 8, COLCHON - 20), (HCAMA0 - 8, HUECO - 4), (HCAMA1 - 270, HUECO - 4)], fill=(60, 110, 90))
    return J

def dos_cuartos(F, t, hermano=False, cama_h=True, poster=True):
    """corte: a la izquierda el cuarto de tu hermano, en medio la pared, a la derecha el tuyo (cama alta, mesilla, armario)"""
    paredes(F, col=(26, 28, 44))
    F.rect(-1600, -200, MUROX0, PISO, fill=(30, 26, 40))                                             # cuarto de tu hermano
    if poster:
        F.rect(-560, 640, -330, 900, fill=(40, 60, 110), outline=(20, 20, 30), w=6)                  # póster de cohete
        F.poly([(-445, 680), (-410, 760), (-410, 840), (-480, 840), (-480, 760)], fill=(200, 200, 210))
        F.poly([(-480, 840), (-445, 880), (-410, 840)], fill=(240, 140, 60))
    F.rect(MUROX0, -200, MUROX1, PISO + 30, fill=(46, 44, 60), outline=(20, 20, 30), w=4)          # la pared que os separa
    F.rect(470, 560, 690, 800, fill=(10, 14, 30), outline=(70, 66, 80), w=12)                        # tu ventana con luna
    F.line([(580, 560), (580, 800)], (70, 66, 80), 8); F.circle((640, 610), 20, fill=(200, 210, 240))
    F.rect(760, PISO - 190, 890, PISO, fill=(70, 54, 44), outline=(40, 30, 24), w=4)                 # mesilla
    reloj_3am(F, 825, PISO - 222, 0.3)
    cama_alta(F, t=t)
    if cama_h:
        cama_hermano(F, vacia=not hermano)
        if hermano: hermano_tumbado(F, t)

def alto(F, t, x, kn=0.0, gira=0.0, sombra=1.0):
    """la cosa pálida y altísima, de pie y de perfil mirando a la pared (a la derecha); kn: golpe de los nudillos;
    gira: vuelve la cara hacia ti"""
    p = pose(body=6, head=8, a1u=lerp(62, 74, kn), a1l=lerp(96, 72, kn), a2u=-6, a2l=8, l1u=4, l1l=-2, l2u=-4, l2l=-2)
    J = ALTO.draw(F, p, x, PISO, f=1, face="closed", t=t)
    hx, hy = J["head"]; r = L["head"] * ALTO.scale
    F.poly([(hx - r * 1.1, hy - r * 0.9), (hx + r * 0.3, hy - r * 1.15), (hx + r * 0.2, hy + r * 0.2),
            (hx - r * 0.7, hy + r * 2.4), (hx - r * 1.3, hy + r * 2.0)], fill=(12, 12, 16))           # melena negra
    if gira > 0:
        cara_palida(F, (hx - r * 0.1 * gira, hy), r * lerp(0.6, 1.05, gira), abre=0.3 + 0.5 * gira)
    return J

def hermano(F, t, x, face="neutral", habla=0.0):
    p = add(pose(a1u=-20, a1l=-40, a2u=20, a2l=60, head=-4), jitter(t, 1, 4))
    F.rect(x + 8, PISO - 205, x + 62, PISO - 120, fill=(200, 70, 60), outline=(90, 30, 26), w=4)      # mochila a la espalda
    J = HERMANO.draw(F, p, x, PISO, f=-1, face="talk" if habla > 0 and int(t * 8) % 2 else face, t=t)
    return J

def puno(F, t, wall_x, y, kn=0.0, lado=1):
    """puño en primer plano contra la pared (desde la derecha si lado=1). kn 0-1: golpe"""
    hx = wall_x + lado * lerp(130, 40, kn)
    F.line([(hx + lado * 40, y + 20), (hx + lado * 420, y + 260)], (8, 8, 12), 92)
    F.line([(hx + lado * 40, y + 20), (hx + lado * 420, y + 260)], (60, 160, 130), 76)               # manga de la sudadera
    F.circle((hx, y), 54, fill=(8, 8, 12)); F.circle((hx, y), 46, fill=(240, 220, 200))
    for i in range(3): F.line([(hx - lado * 30, y - 28 + i * 22), (hx - lado * 6, y - 28 + i * 22)], (190, 160, 140), 4)

def pared_cerca(F, t, sacude=0.0):
    """primer plano de la pared que os separa junto a tu almohada"""
    F.rect(-1600, -400, MUROX0, 3000, fill=(30, 26, 40))
    F.rect(MUROX0, -400, 3000, 3000, fill=(30, 32, 50))
    F.rect(MUROX0 - 6, -400, MUROX0 + 6, 3000, fill=(18, 18, 26))

# ---------- escenas ----------
K1 = 1.25                         # golpes de la primera escena (segundos)
def golpes(t, D, fi):
    """primer fotograma: tu cama de noche, muy cerca de la pared, el reloj en rojo; tres golpes la hacen temblar"""
    kn = golpes_k(t, K1)
    k = ease(seg(t, K1 + 0.8, D))
    F = Frame(fondo(), dict(x=lerp(470, 450, k), y=lerp(1020, 1040, k), z=lerp(1.3, 1.25, k), sx=noise(t * 40) * 14 * kn))
    dos_cuartos(F, t, cama_h=False)
    J = tu_tumbado(F, t, face="scared" if t > K1 else "closed", cuelga=0.0, jit=0.6 * seg(t, K1, K1 + 0.3))
    manta(F)
    img = iluminar(F.finish(), F, [], glows=[((640, 610), 260, 0.6), ((825, PISO - 222), 200, 0.8), (J["head"], 160, 0.35),
                                            ((MUROX1, COLCHON - 120), 220, 0.3 + 0.5 * kn)], amb=0.25, warm=LUNA)
    n = golpe_n(t, K1)
    if n:
        sx_, sy_ = F.P(MUROX1 + 30, COLCHON - 260)
        for i in range(n):
            img = onomato(img, tr("TOC"), 0.8 if i < n - 1 else 0.8 + 0.35 * golpes_k(t, K1 + i * 0.3, n=1),
                          (clamp(sx_ / S + 190 + i * 150, 200, 880), sy_ / S - 330 + i * 60))
    return img, dict(grain=9, flash=(ROJO, 0.35 * (1 - seg(t, 0, 0.3)) + 0.15 * kn), tint=((255, 0, 30), 0.06))

def senal(t, D, fi):
    """recuerdo: corte de los dos cuartos; tu hermano llama tres veces y tú contestas. Todo cálido y tranquilo"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(20, 0, k), y=lerp(1060, 1040, k), z=lerp(1.0, 1.15, k)))
    dos_cuartos(F, t, hermano=True)
    kh, kt = golpes_k(t, D * 0.3, gap=0.25), golpes_k(t, D * 0.62, gap=0.25)
    J2 = hermano_tumbado(F, t, face="happy")
    F.circle((MUROX0 - 26 - 8 * kh, COLCHON - 60), 18, fill=(240, 220, 200), outline=(8, 8, 12), w=4)   # su mano en la pared
    J = tu_tumbado(F, t, face="happy", cuelga=0.0)
    manta(F)
    F.circle((MUROX1 + 26 + 8 * kt, COLCHON - 60), 18, fill=(240, 220, 200), outline=(8, 8, 12), w=4)   # la tuya
    img = iluminar(F.finish(), F, [], glows=[((640, 610), 260, 0.5), ((825, PISO - 222), 160, 0.5), ((-300, 900), 520, 0.45),
                                            ((300, 1000), 420, 0.45)], amb=0.38, warm=(255, 214, 160))
    for tt, xx in ((D * 0.3, -190), (D * 0.62, 240)):
        if t >= tt and t < tt + 1.2:
            sx_, sy_ = F.P(xx, COLCHON - 300)
            img = onomato(img, tr("TOC TOC TOC"), 0.55 * ease(seg(t, tt, tt + 0.15)), (clamp(sx_ / S, 230, 850), sy_ / S))
    return img, dict(grain=7, tint=((255, 180, 80), 0.12))

K3 = 1.15
def contestas(t, D, fi):
    """primer plano: tu puño golpea tres veces la pared; luego te duermes tranquilo"""
    kn = golpes_k(t, K3)
    k = ease(seg(t, K3 + 1.0, D * 0.95))
    F = Frame(fondo(), dict(x=lerp(220, 330, k), y=lerp(980, 1060, k), z=lerp(2.2, 1.5, k), sx=noise(t * 40) * 8 * kn))
    dos_cuartos(F, t, cama_h=False)
    J = tu_tumbado(F, t, face="happy" if t < K3 + 1.2 else "closed", cuelga=0.0)
    manta(F)
    if t < K3 + 1.2:
        puno(F, t, MUROX1, COLCHON - 160, kn=kn)
    img = iluminar(F.finish(), F, [], glows=[((640, 610), 260, 0.5), ((825, PISO - 222), 200, 0.7), (J["head"], 160, 0.35),
                                            ((MUROX1 + 100, COLCHON - 160), 260, 0.4)], amb=0.3, warm=LUNA)
    n = golpe_n(t, K3)
    if n and t < K3 + 1.4:
        for i in range(n):
            img = onomato(img, tr("TOC"), 0.8, (300 + i * 230, 560 + (i % 2) * 70))
    return img, dict(grain=8, tint=((255, 180, 80), 0.05))

def manana(t, D, fi):
    """de día: tu hermano entra con la mochila; tú, sentado en la cama, te quedas helado"""
    hab = seg(t, D * 0.48, D * 0.9)
    k = ease(seg(t, D * 0.45, D * 0.62))
    sh = 6 * seg(t, D * 0.8, D * 0.85) * (1 - seg(t, D * 0.9, D))
    F = Frame(fondo("d"), dict(x=lerp(600, 720, k), y=lerp(1000, 1040, k), z=lerp(1.0, 1.35, k), sx=noise(t * 30) * sh))
    dos_cuartos(F, t, cama_h=False)
    F.rect(930, PISO - 560, 1200, PISO, fill=(180, 170, 150))                                       # tu puerta abierta, pasillo de día
    hermano(F, t, lerp(1250, 960, ease(seg(t, 0, D * 0.35))), face="happy", habla=hab)
    J = tu_tumbado(F, t, face="scared" if t > D * 0.75 else "neutral", sienta=1.0, jit=0.6 * seg(t, D * 0.75, D * 0.8))
    img = iluminar(F.finish(), F, [], glows=[((580, 680), 520, 1.0), ((1150, 1000), 360, 0.6)], amb=0.6, warm=DIA)
    return img, dict(grain=6, flash=((255, 255, 255), 0.18 * max(0, 1 - abs(t - D * 0.82) / 0.15)))

def vacio(t, D, fi):
    """anoche, en el cuarto de tu hermano: la cama hecha y vacía. Contra la pared, de pie, algo pálido y altísimo llama.
    Al final vuelve la cara hacia ti"""
    k = ease(seg(t, 0, D * 0.55))
    gira = ease(seg(t, D * 0.72, D * 0.82))
    kn = golpes_k(t, D * 0.25, gap=0.32)
    F = Frame(fondo(), dict(x=lerp(-420, -200, k), y=lerp(1000, 820, k), z=lerp(1.1, 1.6 + 0.3 * gira, k), sx=noise(t * 40) * 10 * gira * (1 - seg(t, D * 0.85, D))))
    dos_cuartos(F, t, hermano=False)
    J = alto(F, t, -190, kn=kn, gira=gira)
    img = iluminar(F.finish(), F, [], glows=[((-300, 900), 500, 0.35), (J["head"], 260, 0.5 + 0.3 * gira), ((640, 610), 200, 0.3)],
                   amb=0.26, warm=LUNA)
    return img, dict(grain=10, tint=((255, 0, 30), 0.1 + 0.12 * gira), flash=(ROJO, 0.4 * max(0, 1 - abs(t - D * 0.74) / 0.15)),
                     glitch=0.3 if 0 < t - D * 0.72 < 0.25 and fi % 2 else 0.0)

K6 = 1.55
def noche(t, D, fi):
    """otra vez las tres: tú, con los ojos abiertos, mirando a la pared; tres golpes"""
    kn = golpes_k(t, K6)
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(460, 380, k), y=lerp(1000, 1060, k), z=lerp(1.1, 1.6, k), sx=noise(t * 40) * 10 * kn))
    dos_cuartos(F, t, cama_h=False)
    J = tu_tumbado(F, t, face="scared", cuelga=0.0, jit=0.5)
    manta(F)
    armario_puertas(F, t, jit=6 * kn)
    img = iluminar(F.finish(), F, [], glows=[((640, 610), 260, 0.6), ((825, PISO - 222), 200, 0.8), (J["head"], 160, 0.35)], amb=0.25, warm=LUNA)
    n = golpe_n(t, K6)
    if n:
        for i in range(n):
            img = onomato(img, tr("TOC"), 0.8, (330 + i * 220, 520 + (i % 2) * 70))
    return img, dict(grain=10, tint=((255, 0, 30), 0.08), flash=(ROJO, 0.12 * kn))

def armario(t, D, fi):
    """la cámara pasa de la pared al armario; los golpes vuelven, y el armario tiembla con cada uno"""
    k = ease(seg(t, 0, D * 0.45))
    t0 = D * 0.5
    kn = golpes_k(t, t0, gap=0.34)
    F = Frame(fondo(), dict(x=lerp(150, ARM0 + ARMW / 2, k), y=lerp(1050, PISO - 300, k), z=lerp(1.6, 1.9, k), sx=noise(t * 40) * 12 * kn))
    dos_cuartos(F, t, cama_h=False)
    J = tu_tumbado(F, t, face="scared", cuelga=0.0, jit=0.5)
    manta(F)
    c = armario_puertas(F, t, jit=14 * kn, nudillo=kn)
    img = iluminar(F.finish(), F, [], glows=[((640, 610), 260, 0.5), ((825, PISO - 222), 200, 0.7), (c, 300, 0.35 + 0.3 * kn)], amb=0.25, warm=LUNA)
    n = golpe_n(t, t0, gap=0.34)
    if n:
        for i in range(n):
            img = onomato(img, tr("TOC"), 0.8 + 0.3 * golpes_k(t, t0 + i * 0.34, n=1), (260 + i * 280, 480 + (i % 2) * 80))
    return img, dict(grain=10, tint=((255, 0, 30), 0.1 + 0.1 * kn), flash=(ROJO, 0.2 * kn))

def toca(t, D, fi):
    """la puerta del armario se abre una rendija: ojos, dedos en el canto y, desde dentro, tres golpes suaves"""
    abre = seg(t, D * 0.05, D * 0.3)
    ojos = seg(t, D * 0.3, D * 0.4)
    dedos = seg(t, D * 0.38, D * 0.48)
    k = ease(seg(t, 0, D))
    hit = seg(t, D * 0.42, D * 0.47)
    F = Frame(fondo(), dict(x=ARM0 + ARMW / 2 + 20, y=PISO - 360, z=lerp(2.0, 2.8, k), sx=noise(t * 40) * 8 * hit * (1 - seg(t, D * 0.5, D * 0.7))))
    dos_cuartos(F, t, cama_h=False)
    kn = golpes_k(t, D * 0.72, gap=0.3)
    c = armario_puertas(F, t, abre=abre, ojos=ojos, dedos=dedos, nudillo=kn, jit=3 * kn)
    img = iluminar(F.finish(), F, [], glows=[(c, 240, 0.45), ((825, PISO - 222), 160, 0.5)], amb=0.22, warm=LUNA)
    return img, dict(grain=10, tint=((255, 0, 30), 0.14 + 0.1 * hit), flash=(ROJO, 0.35 * max(0, 1 - abs(t - D * 0.44) / 0.15)),
                     glitch=0.3 if 0 < t - D * 0.42 < 0.25 and fi % 3 else 0.0)

def final(t, D, fi):
    """plano general: tú en la cama mirando el armario entreabierto, con ojos y dedos. La regla"""
    k = ease(seg(t, 0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(1000, 680, k), y=lerp(1050, 1000, k), z=lerp(1.6, 0.98, k)))
    dos_cuartos(F, t, cama_h=False)
    J = tu_tumbado(F, t, face="scared", cuelga=0.0, sienta=0.6, jit=0.6)
    manta(F)
    c = armario_puertas(F, t, abre=1.0, ojos=1.0, dedos=1.0)
    img = iluminar(F.finish(), F, [], glows=[(c, 240, 0.5), ((825, PISO - 222), 200, 0.6), (J["head"], 160, 0.3), ((640, 610), 220, 0.4)],
                   amb=0.25, warm=LUNA)
    pp = ease_back(seg(t, D * 0.42, D * 0.52)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 130, 1040, 640), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 LLAMAN"), 200, 62, (255, 255, 255)), (tr("A LA PARED…"), 280, 62, (255, 255, 255)),
                                 (tr("NO DEVUELVAS"), 420, 112, (255, 40, 50)), (tr("LOS GOLPES"), 545, 112, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 680, 850, 770), 26, fill=(230, 30, 50))
        d.text((540, 725), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.22 * pp if pp > 0 else 0.08), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(golpes=golpes, senal=senal, contestas=contestas, manana=manana, vacio=vacio, noche=noche, armario=armario,
                 toca=toca, final=final)
PAUSA = dict(golpes=0.5, senal=0.5, contestas=0.6, manana=0.6, vacio=0.8, noche=0.5, armario=0.6, toca=0.8, final=2.4)
