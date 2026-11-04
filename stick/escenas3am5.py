"""Si oyes esto a las 3AM — 5: "El perro te lame la mano". Tu cuarto con una cama alta (hueco oscuro debajo), el pasillo,
el baño con la ducha y el espejo empañado. Piezas nuevas reutilizables: cama_alta (con TU tumbado y la mano colgando),
lengua (lengua gris que lame), perro (tumbado o de pie), bano (lavabo, espejo empañado con texto, ducha que gotea),
COSA (la cosa pálida a cuatro patas, con cara_palida)."""
import math
from PIL import ImageDraw
from motor import *
from escenas2 import big
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am, CASA_A, CASA_B
from escenas3am2 import cara_palida, PIEL
from escenas3am3 import paredes, PISO

CAMA_X0, CAMA_X1 = 80, 720
COLCHON = PISO - 250              # parte de arriba del colchón
HUECO = PISO - 205                # parte de abajo de la cama (empieza el hueco oscuro)
LENGUA = (150, 104, 112)
FRIA = (200, 222, 255)            # luz fría del baño
COSA = Fig(shirt=PIEL, limb=PIEL, scale=1.25)
P4 = pose(body=75, head=-60, a1u=150, a1l=-30, a2u=170, a2l=-20, l1u=40, l1l=-80, l2u=20, l2l=-90)   # a cuatro patas
_BG = {}
def fondo(k="a"):
    if k not in _BG: _BG[k] = gradient(CASA_A, CASA_B) if k == "a" else gradient((26, 30, 38), (10, 12, 16))
    return _BG[k]

def _osc(c, k): return tuple(int(v * k) for v in c)

def cama_alta(F, dedos_k=0.0, ojos=0.0, t=0.0):
    """cama vista de lado, con un hueco alto y negro debajo. dedos_k: dedos pálidos asomando; ojos: dos brillos dentro"""
    F.rect(CAMA_X0 - 30, PISO - 440, CAMA_X0 + 10, PISO, fill=(80, 58, 46), outline=(40, 28, 20), w=4)       # cabecero
    F.rect(CAMA_X0, HUECO, CAMA_X1, PISO, fill=(4, 4, 7))                                                     # hueco
    for lx in (CAMA_X0 + 14, CAMA_X1 - 14): F.rect(lx - 10, HUECO, lx + 10, PISO, fill=(60, 44, 34))           # patas
    F.rect(CAMA_X0, HUECO - 20, CAMA_X1, HUECO + 6, fill=(78, 56, 42), outline=(40, 28, 20), w=3)            # somier
    F.rect(CAMA_X0, COLCHON, CAMA_X1, HUECO - 20, fill=(150, 158, 196))                                       # colchón / sábana
    F.rect(CAMA_X0 + 30, COLCHON - 34, CAMA_X0 + 190, COLCHON + 2, fill=(222, 226, 240))                       # almohada
    if ojos > 0:
        for ex in (470, 498): F.circle((ex, PISO - 96), 3.2, fill=_osc((230, 230, 240), ojos))
    if dedos_k > 0:                                                    # dedos largos apoyados en el suelo, en el borde
        c = _osc(PIEL, 0.75 * dedos_k)
        for i in range(4):
            x0 = 560 + i * 16; F.line([(x0, PISO - 6), (x0 + 30 + i * 4, PISO - 12), (x0 + 58 + i * 6, PISO - 4)], c, 6)
        F.line([(500, PISO - 14), (560, PISO - 8)], c, 12)

def manta(F):
    F.poly([(300, COLCHON - 36), (CAMA_X1 + 8, COLCHON - 20), (CAMA_X1 + 8, HUECO - 4), (300, HUECO - 4)], fill=(60, 72, 120))
    F.line([(300, COLCHON - 36), (CAMA_X1 + 8, COLCHON - 20)], (90, 104, 160), 6)

def tu_tumbado(F, t, face="closed", cuelga=1.0, sienta=0.0, jit=0.0):
    """TU tumbado en la cama alta; cuelga: el brazo colgando fuera de la cama (0 = recogido); sienta: se incorpora"""
    p = mix(pose(a1u=lerp(30, -90, cuelga), a1l=lerp(80, 0, cuelga), a2u=10, a2l=20),
            pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=40, a1l=30, a2u=-20), sienta)
    p = add(p, jitter(t, jit, 5))
    J = TU.draw(F, p, lerp(330, 380, sienta), lerp(COLCHON - 12, COLCHON - 6, sienta), f=1, rot=lerp(-90, 0, sienta), snap=False, face=face)
    return J

def lengua(F, base, punta, t, w=22, lame=1.0):
    """lengua gris-rosada, larga, que sube desde base hasta punta y se curva lamiendo"""
    bx, by = base; px, py = punta
    ph = math.sin(t * 7) * lame
    pts = []
    for i in range(9):
        u = i / 8
        x = lerp(bx, px, u) + math.sin(u * math.pi) * (30 + 14 * ph)
        y = lerp(by, py, u) - math.sin(u * math.pi * 0.5) * 10 * ph
        pts.append((x, y))
    for i in range(8):
        F.line([pts[i], pts[i + 1]], LENGUA, w * lerp(1.0, 0.65, i / 8))
    F.line(pts[1:-1], (120, 80, 90), 3)
    return pts[-1]

def perro(F, x, y, sc=1.0, tumbado=True, col=(160, 110, 64)):
    """perro simple de perfil; tumbado de lado, quieto y con los ojos cerrados (sin sangre)"""
    o = (40, 26, 16)
    if tumbado:
        F.ellipse((x, y - 34 * sc), 110 * sc, 36 * sc, fill=col, outline=o, w=4 * sc)
        for k, lx in enumerate((-60, -30, 40, 70)):                                               # patas estiradas
            F.line([(x + lx * sc, y - 12 * sc), (x + (lx + 34) * sc, y - 2 * sc)], col, 13 * sc)
        F.line([(x + 106 * sc, y - 40 * sc), (x + 170 * sc, y - 18 * sc)], col, 11 * sc)         # cola, caída
        hx, hy = x - 128 * sc, y - 34 * sc
        F.circle((hx, hy), 36 * sc, fill=col, outline=o, w=4 * sc)
        F.ellipse((hx - 36 * sc, hy + 10 * sc), 26 * sc, 16 * sc, fill=col, outline=o, w=3 * sc)    # hocico
        F.circle((hx - 58 * sc, hy + 6 * sc), 7 * sc, fill=(20, 14, 10))                           # trufa
        F.poly([(hx + 6 * sc, hy - 26 * sc), (hx + 40 * sc, hy - 16 * sc), (hx + 26 * sc, hy + 22 * sc)], fill=(110, 70, 40))  # oreja caída
        F.line([(hx - 18 * sc, hy - 8 * sc), (hx - 4 * sc, hy - 8 * sc)], (20, 14, 10), 4 * sc)    # ojo cerrado
        F.line([(hx + 22 * sc, hy + 14 * sc), (hx + 34 * sc, hy + 40 * sc)], (200, 30, 40), 8 * sc)   # collar rojo
        F.circle((hx + 36 * sc, hy + 46 * sc), 8 * sc, fill=(210, 190, 110))                        # chapa
    return (x - 128 * sc, y - 34 * sc)

ESPEJO = (110, 560, 470, 940)
def bano(F, luz=1.0, vaho=1.0, texto=0.0, t=0.0, gota=True, reflejo=None):
    """baño: azulejos, lavabo con espejo empañado (texto escrito con el dedo), ducha con cortina y alcachofa que gotea"""
    F.rect(-900, -200, 2000, PISO, fill=(70, 80, 90))
    for xx in range(-900, 2000, 70): F.line([(xx, -200), (xx, PISO)], (56, 64, 74), 3)
    for yy in range(-200, PISO, 70): F.line([(-900, yy), (2000, yy)], (56, 64, 74), 3)
    F.rect(-900, PISO, 2000, 3000, fill=(40, 44, 50)); F.line([(-900, PISO), (2000, PISO)], (90, 96, 104), 6)
    # espejo
    x0, y0, x1, y1 = ESPEJO
    F.rect(x0 - 16, y0 - 16, x1 + 16, y1 + 16, fill=(150, 150, 156))
    F.rect(x0, y0, x1, y1, fill=(36, 44, 54))
    if reflejo: reflejo(F)
    if vaho > 0:
        for k in range(14):
            F.ellipse((x0 + 40 + (k * 97) % 330, y0 + 50 + (k * 61) % 300), 90, 60, fill=_osc((150, 160, 170), 0.55 + 0.1 * (k % 3)))
    if texto > 0:
        lineas = [tr("LOS HUMANOS"), tr("TAMBIÉN"), tr("SABEN LAMER")]
        n = texto * len(lineas)
        for k, ln in enumerate(lineas):
            if n <= k: break
            vis = ln[: max(1, int(len(ln) * min(1, n - k)))]
            fs = 54
            while fs > 20 and F.d.textlength(ln, font=font(fs * S * F.z)) / S / F.z > (x1 - x0) - 40: fs -= 2
            F.text((x0 + (x1 - x0) / 2 - (F.d.textlength(ln, font=font(fs * S * F.z)) - F.d.textlength(vis, font=font(fs * S * F.z))) / S / F.z / 2,
                    y0 + 110 + k * 110), vis, fs, (38, 46, 56))
            F.text((x0 + (x1 - x0) / 2 - (F.d.textlength(ln, font=font(fs * S * F.z)) - F.d.textlength(vis, font=font(fs * S * F.z))) / S / F.z / 2,
                    y0 + 106 + k * 110), vis, fs, (16, 20, 26))
    # lavabo
    F.rect(130, 1010, 450, 1060, fill=(226, 228, 232), outline=(150, 152, 160), w=4)
    F.rect(260, 1060, 320, PISO, fill=(210, 212, 218))
    F.line([(290, 1010), (290, 980), (320, 980)], (170, 170, 178), 10)
    # ducha
    F.rect(600, 480, 1100, PISO, fill=(84, 96, 108))
    for xx in range(600, 1100, 60): F.line([(xx, 480), (xx, PISO)], (70, 80, 92), 3)
    F.rect(590, PISO - 50, 1100, PISO, fill=(200, 204, 210), outline=(140, 144, 150), w=4)                # plato
    F.line([(580, 470), (1100, 470)], (170, 170, 178), 10)                                                   # barra
    for k in range(5): F.line([(600 + k * 22, 476), (606 + k * 22 + 10 * math.sin(k + t), PISO - 70)], (110, 150, 150), 22)   # cortina recogida
    F.line([(1000, 470), (1000, 560), (960, 580)], (170, 170, 178), 9); F.ellipse((950, 586), 30, 12, fill=(180, 180, 188))
    if gota:
        u = (t * 1.6) % 1.0
        F.ellipse((950, lerp(600, PISO - 56, u * u)), 5, 9, fill=(190, 220, 240))
    # luz del techo que parpadea
    F.rect(380, -40, 700, -10, fill=_osc((240, 248, 255), 0.3 + 0.7 * luz))

def _cuarto(F, t, dedos_k=0.0, ojos=0.0, puerta=0.0):
    paredes(F, col=(26, 28, 44))
    F.rect(940, PISO - 560, 1180, PISO, fill=(6, 6, 10))                                       # puerta al pasillo
    if puerta > 0: F.rect(940, PISO - 560, 980, PISO, fill=_osc(FRIA, 0.35 * puerta))
    F.rect(760, PISO - 190, 890, PISO, fill=(70, 54, 44), outline=(40, 30, 24), w=4)          # mesilla
    reloj_3am(F, 825, PISO - 222, 0.3)
    cama_alta(F, dedos_k=dedos_k, ojos=ojos, t=t)

# ---------- escenas ----------
def cama(t, D, fi):
    k = ease(seg(t, 0.0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(825, 420, k), y=lerp(PISO - 222, PISO - 170, k), z=lerp(3.4, 1.55, k)))
    _cuarto(F, t, ojos=0.0)
    J = tu_tumbado(F, t, face="closed")
    manta(F)
    hx, hy = J["a1h"]
    lame = seg(t, D * 0.5, D * 0.6)
    if lame > 0:
        lengua(F, (300, PISO - 70), (lerp(300, hx + 4, ease(lame)), lerp(PISO - 70, hy + 6, ease(lame))), t, lame=lame)
    img = iluminar(F.finish(), F, [], glows=[((825, PISO - 222), 200, 0.6), ((hx, hy), 240, 0.55)], amb=0.32, warm=(255, 120, 120))
    return img, dict(grain=9, flash=((255, 40, 40), 0.35 * (1 - seg(t, 0, 0.25))))

def siempre(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(380, 460, k), y=lerp(PISO - 150, PISO - 110, k), z=lerp(1.9, 2.7, k)))
    _cuarto(F, t, dedos_k=seg(t, D * 0.35, D * 0.7), ojos=0.6 + 0.4 * (math.sin(t * 2) > -0.6))
    J = tu_tumbado(F, t, face="closed")
    manta(F)
    hx, hy = J["a1h"]
    lengua(F, (300, PISO - 70), (hx + 4, hy + 6), t)
    img = iluminar(F.finish(), F, [], glows=[((hx, hy), 260, 0.6), ((540, PISO - 60), 160, 0.35)], amb=0.28, warm=(255, 150, 150))
    return img, dict(grain=10)

def gotea(t, D, fi):
    s = ease(seg(t, D * 0.2, D * 0.45))
    luz = 0.5 + 0.5 * (noise(t * 8, 2) > -0.2)
    F = Frame(fondo(), dict(x=lerp(560, 640, ease(t / D)), y=1060, z=1.25))
    _cuarto(F, t, puerta=luz)
    tu_tumbado(F, t, face="scared" if s > 0.3 else "neutral", cuelga=1 - s, sienta=s)
    if s < 0.5: manta(F)
    # gotas: ondas de sonido saliendo por la puerta
    for i in range(3):
        u = (t * 1.5 + i / 3) % 1
        F.arc((1060, PISO - 300), 30 + 120 * u, 140, 220, _osc(FRIA, 0.6 * (1 - u)), 5)
    img = iluminar(F.finish(), F, [], glows=[((960, PISO - 280), 340, 0.7 * luz), ((825, PISO - 222), 160, 0.5)], amb=0.2, warm=FRIA)
    return img, dict(grain=10)

def pasillo(t, D, fi):
    F = Frame(fondo(), dict(x=lerp(480, 600, ease(t / D)), y=1040, z=1.15))
    paredes(F, col=(24, 26, 38))
    F.rect(-300, PISO - 560, -60, PISO, fill=(8, 8, 12))                                        # tu cuarto, a oscuras
    luz = 0.5 + 0.5 * (noise(t * 10, 4) > 0.0)
    F.rect(760, PISO - 580, 1000, PISO, fill=(40, 36, 34))
    F.rect(780, PISO - 560, 980, PISO, fill=_osc(FRIA, 0.75 * luz))                             # baño, entreabierto
    F.poly([(780, PISO - 560), (850, PISO - 590), (850, PISO + 30), (780, PISO)], fill=(80, 70, 60), outline=(40, 30, 24), w=4)
    x = lerp(160, 640, ease(seg(t, 0, D * 0.95)))
    TU.draw(F, walk(t, 0.55, 0.55), x, PISO, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((880, PISO - 280), 460, 0.95 * luz), ((x, PISO - 150), 200, 0.4)], amb=0.2, warm=FRIA)
    return img, dict(grain=11)

def ducha(t, D, fi):
    k = ease(seg(t, D * 0.25, D))
    luz = 0.6 + 0.4 * (noise(t * 9, 6) > -0.3)
    F = Frame(fondo("b"), dict(x=lerp(560, 820, k), y=lerp(1000, PISO - 90, k), z=lerp(1.0, 2.0, k)))
    bano(F, luz=luz, t=t)
    perro(F, 860, PISO - 50, sc=1.0)
    TU.draw(F, add(SCARED, jitter(t, 2, 3)), 470, PISO, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((540, 200), 700, 0.8 * luz), ((840, PISO - 80), 260, 0.6)], amb=0.25, warm=FRIA)
    return img, dict(grain=10, tint=((80, 120, 255), 0.08))

def espejo(t, D, fi):
    k = ease(seg(t, 0, D * 0.5))
    x0, y0, x1, y1 = ESPEJO
    F = Frame(fondo("b"), dict(x=lerp(420, (x0 + x1) / 2, k), y=lerp(1000, (y0 + y1) / 2 + 40, k), z=lerp(1.3, 2.2, k)))
    def refl(F_):                                                 # tu reflejo asustado
        big(TU, 1.1, F_, add(pose(body=4, a1u=150, a1l=40, a2u=-150, a2l=-40), jitter(t, 1.5, 8)), 300, y1 + 260, f=-1, face="scared")
    bano(F, luz=0.8 + 0.2 * (noise(t * 9) > -0.4), t=t, texto=seg(t, D * 0.2, D * 0.62))
    img = iluminar(F.finish(), F, [], glows=[(((x0 + x1) / 2, (y0 + y1) / 2), 380, 0.8)], amb=0.25, warm=FRIA)
    return img, dict(grain=11, tint=((255, 0, 30), 0.18 * seg(t, D * 0.55, D)))

def entiendes(t, D, fi):
    """bajo la cama, otra vez: no era tu perro. La cosa tumbada en el hueco, con la lengua fuera, mirándote"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(400, 420, k), y=lerp(PISO - 150, PISO - 130, k), z=lerp(2.0, 2.4, k)))
    _cuarto(F, t)
    F.ellipse((600, PISO - 36), 190, 30, fill=_osc(PIEL, 0.28))                               # su cuerpo, en la sombra
    for i in range(4):
        x0 = 330 + i * 14; F.line([(x0, PISO - 6), (x0 - 30, PISO - 12), (x0 - 56, PISO - 4)], _osc(PIEL, 0.8), 6)
    cx, cy = 420, PISO - 100
    cara_palida(F, (cx, cy), 48, abre=1.0)
    J = tu_tumbado(F, t, face="closed")
    manta(F)
    hx, hy = J["a1h"]
    lengua(F, (cx - 2, cy + 48), (hx + 4, hy + 6), t, w=18)
    img = iluminar(F.finish(), F, [], glows=[((cx, cy), 200, 0.9), ((hx, hy), 200, 0.5)], amb=0.2, warm=(255, 120, 120))
    return img, dict(grain=12, tint=((255, 0, 30), 0.15 + 0.1 * k), flash=((255, 255, 255), 0.6 * (1 - seg(t, 0, 0.3))),
                     glitch=0.25 if fi % 6 == 0 else 0.0)

def sale(t, D, fi):
    """tu cuarto: unos dedos y luego una cara salen de debajo de la cama… y la cosa se lanza hacia ti a cuatro patas"""
    sl = ease(seg(t, D * 0.08, D * 0.42))           # asoma la cabeza
    hit = t >= D * 0.45
    ven = ease(seg(t, D * 0.45, D * 0.8))
    sh = 14 * hit * (1 - seg(t, D * 0.6, D * 0.85))
    x = lerp(560, 640, ven); pz = add(P4, jitter(t, 6, 9))
    hx0, hy0 = COSA.joints(pz, x, PISO, f=1, stretch=1.2)["head"]
    F = Frame(fondo(), dict(x=lerp(500, hx0, ven) + noise(t * 30) * sh, y=lerp(PISO - 170, hy0 + 60, ven), z=lerp(1.5, 2.6, ven),
                            sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    _cuarto(F, t, puerta=0.8, dedos_k=1.0 if not hit else 0.0)
    F.poly([(CAMA_X0, COLCHON - 10), (CAMA_X1, COLCHON - 30), (CAMA_X1, HUECO - 4), (CAMA_X0, HUECO - 4)], fill=(60, 72, 120))   # cama vacía
    if not hit:
        cara_palida(F, (640, lerp(PISO + 40, PISO - 60, sl)), 44, abre=0.4)
        F.rect(500, PISO, 900, PISO + 400, fill=(14, 14, 22))                                  # el suelo tapa lo que aún no ha salido
        F.rect(CAMA_X0, HUECO - 20, CAMA_X1, HUECO + 6, fill=(78, 56, 42))
        img = iluminar(F.finish(), F, [], glows=[((640, PISO - 60), 160, 0.7 * sl), ((960, PISO - 300), 300, 0.5)], amb=0.18, warm=FRIA)
        return img, dict(grain=12, tint=((255, 0, 30), 0.1 * sl))
    J = COSA.draw(F, pz, x, PISO, f=1, face="closed", stretch=1.2)
    cara_palida(F, J["head"], 46, abre=1.0)
    lengua(F, (J["head"][0], J["head"][1] + 46), (J["head"][0] + 20, J["head"][1] + 130), t, w=12, lame=0.6)
    img = iluminar(F.finish(), F, [], glows=[((960, PISO - 300), 360, 0.6), (J["head"], 240, 0.9)], amb=0.18, warm=FRIA)
    return img, dict(grain=12, flash=((255, 255, 255), max(0, 1 - (t - D * 0.45) / 0.25)),
                     glitch=0.45 if fi % 3 and t < D * 0.75 else 0.0, tint=((255, 0, 30), 0.2))

def final(t, D, fi):
    F = Frame(fondo(), dict(x=430, y=lerp(PISO - 230, PISO - 210, ease(t / D)), z=1.7))
    _cuarto(F, t, ojos=1.0, dedos_k=1.0)
    J = tu_tumbado(F, t, face="scared", cuelga=0.0, jit=2)
    manta(F)
    lengua(F, (300, PISO - 70), (300 + 40 * math.sin(t * 2), HUECO - 30), t, w=20)
    img = iluminar(F.finish(), F, [], glows=[((300, HUECO), 220, 0.6), ((480, PISO - 96), 120, 0.5)], amb=0.18, warm=(255, 120, 120))
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, D * 0.5, D * 0.6)) * (1 + 0.03 * math.sin(t * 25))
    if p > 0:
        d.rounded_rectangle((40, 330, 1040, 620), 30, fill=(0, 0, 0))
        d.text((540, 395), tr("SI ALGO TE LAME LA MANO…"), font=font(60 * p + 1), fill=(255, 255, 255), anchor="mm", stroke_width=int(8 * p), stroke_fill=(0, 0, 0))
        d.text((540, 515), tr("NO LA BAJES"), font=font(140 * p + 1), fill=(255, 40, 50), anchor="mm", stroke_width=int(14 * p), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 650, 850, 750), 26, fill=(230, 30, 50))
        d.text((540, 700), tr("SÍGUEME PARA MÁS"), font=font(52), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=10, tint=((255, 0, 30), 0.25 * p if p > 0 else 0), glitch=0.3 if p > 0 and fi % 5 == 0 else 0.0)

ESCENA_FN = dict(cama=cama, siempre=siempre, gotea=gotea, pasillo=pasillo, ducha=ducha, espejo=espejo, entiendes=entiendes,
                 sale=sale, final=final)
PAUSA = dict(cama=0.5, siempre=0.5, gotea=0.4, pasillo=0.3, ducha=0.7, espejo=0.8, entiendes=0.7, sale=0.9, final=2.4)
