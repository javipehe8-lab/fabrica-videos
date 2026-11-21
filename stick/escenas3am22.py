"""Si oyes esto a las 3AM — 22: "La vecina de abajo". Vives en el último piso; a las tres algo arrastra muebles en tu techo.
Por la mañana la vecina de abajo subió a quejarse. En el pasillo hay arañazos del armario hasta debajo de la trampilla del
desván. El ruido se para encima de tu cama; la trampilla se abre sola, baja un brazo larguísimo y arrastra tu armario hasta
debajo, por los mismos arañazos. Asoma una cara del revés: "¿Subes tú… o bajo yo?".
Piezas nuevas reutilizables: cuarto_desvan (tu cuarto de lado con el techo, la lámpara que se balancea y, en corte, el desván
de encima), reptante (la cosa pálida a cuatro patas, de lado, o tumbada boca abajo), polvo (polvo que cae del techo),
VECINA + vecina() (señora mayor con bata, rulos y gafas), rellano_puerta (entrada de casa con la puerta abierta al rellano),
pasillo_trampilla (pasillo con el techo visto desde abajo, trampilla que se abre y suelo con arañazos), armario,
brazo_largo (brazo pálido larguísimo con dedos que agarran) y cara_reves (cara pálida colgando del revés, con el pelo hacia abajo)."""
import math
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am, CASA_A, CASA_B
from escenas3am2 import PIEL
from escenas3am3 import paredes, PISO
from escenas3am5 import _osc, cama_alta, manta, tu_tumbado, CAMA_X0, CAMA_X1, COLCHON, HUECO
from escenas3am18 import onomato

ROJO = (255, 40, 40)
LUNA = (170, 190, 255)
DIA = (220, 214, 196)
TECHO = 420                         # techo del cuarto (cara de abajo)
SUELO_D = 380                       # suelo del desván (cara de arriba del forjado)
CABEZA_X = 190                      # donde está tu cabeza en la cama
# pasillo
TP = 300                            # borde del techo del pasillo (visto desde abajo: franja TP-90..TP)
TX0, TX1 = 640, 900                 # trampilla
SUELO = PISO + 60                   # donde apoya el armario (franja de suelo en perspectiva)
AW, AH = 260, 560                   # armario
AX0, AX1 = 150, TX0                 # armario: junto a la pared → debajo de la trampilla
VECINA = Fig(shirt=(128, 84, 116), limb=(238, 224, 212), scale=0.9, extra=("bun",))
_BG = {}
def fondo(k="a"):
    if k not in _BG:
        _BG[k] = {"a": gradient(CASA_A, CASA_B), "m": gradient((14, 14, 18), (6, 6, 8)), "d": gradient((60, 58, 64), (30, 28, 32))}[k]
    return _BG[k]

# ---------- piezas ----------
def polvo(F, x, t, n=14, k=1.0, y0=TECHO):
    """polvo que cae del techo en x"""
    if k <= 0: return
    for i in range(n):
        ph = (t * 0.9 + i * 0.137) % 1.0
        xx = x + ((i * 53) % 90 - 45) + math.sin(t * 2 + i) * 6
        F.circle((xx, y0 + ph * 420), 2.6 + (i % 3), fill=_osc((170, 166, 176), k * (1 - ph * 0.7)))

def lampara(F, t, amp=0.0, x=470):
    a = math.radians(amp * math.sin(t * 2.4))
    L_ = 170
    bx, by = x + math.sin(a) * L_, TECHO + math.cos(a) * L_
    F.line([(x, TECHO), (bx, by)], (30, 30, 34), 4)
    F.poly([(bx - 22, by - 6), (bx + 22, by - 6), (bx + 52, by + 52), (bx - 52, by + 52)], fill=(120, 110, 96), outline=(60, 54, 46), w=3)
    F.circle((bx, by + 50), 14, fill=(70, 70, 76))
    return (bx, by + 40)

def reptante(F, x, y, t, tumba=0.0, paso=1.0, cara=0.0, sc=1.5):
    """la cosa pálida a cuatro patas, de lado, mirando a la izquierda; y = suelo bajo ella.
    tumba 0-1: se va pegando al suelo boca abajo. paso: avance de las patas. cara: brillo de los ojos"""
    h = lerp(1.0, 0.2, ease(tumba))
    c, o = PIEL, (8, 8, 12)
    S_ = (x, y - (120 * h + 14) * sc)                                # hombros
    H_ = (x + 170 * sc, y - (110 * h + 14) * sc)                     # cadera
    ph = t * 5 * paso
    def pata(base, dx, alto, fase, w):
        st = math.sin(ph + fase) * 30 * paso * sc
        lev = max(0, math.cos(ph + fase)) * 22 * paso * h * sc
        pie = (base[0] + dx * sc + st, y - 4 - lev)
        rod = (base[0] + dx * 0.4 * sc + st * 0.5, base[1] - (alto * h + 20) * sc)
        F.line([base, rod, pie], o, (w + 8) * sc); F.line([base, rod, pie], c, w * sc)
        for i in range(3): F.line([pie, (pie[0] - (22 + i * 8) * sc, pie[1] + 2)], c, 5 * sc)
    pata(H_, 60, 90, 1.6, 17); pata(S_, -90, 110, 0.0, 15)          # patas del fondo
    F.line([S_, H_], o, 52 * sc); F.line([S_, H_], c, 42 * sc)      # cuerpo flaco
    for i in range(5): F.circle((lerp(S_[0], H_[0], 0.15 + i * 0.17), lerp(S_[1], H_[1], 0.15 + i * 0.17) - 18 * sc), 5 * sc, fill=_osc(c, 0.7))   # vértebras
    hx, hy = S_[0] - 62 * sc, S_[1] + lerp(14, 22, tumba) * sc
    F.line([S_, (hx + 20 * sc, hy)], c, 22 * sc)
    r = 34 * sc
    F.ellipse((hx, hy), r, r * 1.15, fill=c)                                                     # cabeza de lado
    F.poly([(hx - r * 0.2, hy - r * 1.1), (hx + r * 1.0, hy - r * 0.7), (hx + r * 0.9, hy + r * 2.2), (hx + r * 0.1, hy + r * 1.9),
            (hx + r * 0.2, hy - r * 0.2), (hx - r * 0.6, hy - r * 0.6)], fill=(14, 14, 18))            # pelo largo hacia atrás y abajo
    F.ellipse((hx - r * 0.55, hy - r * 0.05), r * 0.2, r * 0.28, fill=(2, 2, 4))                       # ojo negro
    F.ellipse((hx - r * 0.75, hy + r * 0.6), r * 0.12, r * 0.22, fill=(2, 2, 4))                       # boca
    if cara > 0: F.circle((hx - r * 0.57, hy - r * 0.1), r * 0.07, fill=_osc((240, 240, 250), cara))
    pata(H_, 20, 90, 4.7, 18); pata(S_, -140, 110, 3.1, 16)         # patas de delante
    return (hx, hy)

def cuarto_desvan(F, t, corte=False, amp=0.0, cosa=None):
    """tu cuarto de lado (cama alta, mesilla con el reloj, ventana, puerta al pasillo) y la lámpara del techo.
    corte=True: se ve el desván de encima (vigas, muebles tapados con sábanas). cosa: (x, tumba, paso) de la cosa en el desván"""
    paredes(F, col=(26, 28, 44))
    F.rect(470, 560, 690, 800, fill=(10, 14, 30), outline=(70, 66, 80), w=12)                   # ventana con luna
    F.line([(580, 560), (580, 800)], (70, 66, 80), 8); F.circle((640, 610), 20, fill=(200, 210, 240))
    F.rect(940, PISO - 560, 1180, PISO, fill=(6, 6, 10))                                         # puerta al pasillo
    F.rect(760, PISO - 190, 890, PISO, fill=(70, 54, 44), outline=(40, 30, 24), w=4)            # mesilla
    reloj_3am(F, 825, PISO - 222, 0.3)
    cama_alta(F, t=t)
    F.rect(-900, SUELO_D, 2000, TECHO, fill=(48, 46, 56)); F.line([(-900, TECHO), (2000, TECHO)], (70, 68, 84), 5)   # forjado
    if not corte:
        F.rect(-900, -800, 2000, SUELO_D, fill=(20, 20, 30))
        return None
    F.rect(-900, -800, 2000, SUELO_D, fill=(10, 9, 12))                                         # desván a oscuras
    for i in range(-3, 9): F.line([(i * 220, SUELO_D), (i * 220 + 140, -60)], (24, 20, 18), 18)  # vigas del tejado
    F.line([(-900, 40), (2000, 40)], (26, 22, 20), 26)
    for x0, w, h in ((-180, 200, 150), (1000, 240, 190)):                                       # muebles tapados con sábanas
        F.poly([(x0, SUELO_D), (x0 + 20, SUELO_D - h), (x0 + w - 20, SUELO_D - h - 10), (x0 + w, SUELO_D)], fill=(54, 52, 58))
    F.rect(1290, SUELO_D - 160, 1300, SUELO_D, fill=(40, 30, 24)); F.rect(1250, SUELO_D - 80, 1330, SUELO_D - 70, fill=(40, 30, 24))  # silla vieja
    if cosa: return reptante(F, cosa[0], SUELO_D, t, tumba=cosa[1], paso=cosa[2], cara=cosa[3] if len(cosa) > 3 else 0.0)
    return None

def vecina(F, p, x, y, t=0.0, f=-1, face="angry"):
    J = VECINA.draw(F, p, x, y, f=f, face=face, t=t)
    hx, hy = J["head"]; sc = VECINA.scale
    for dx in (-9, 11): F.circle((hx + f * 9 * sc + dx * sc, hy - 5 * sc), 10 * sc, outline=(150, 130, 90), w=2.5 * sc)   # gafas
    for i in range(4): F.circle((hx - 20 * sc + i * 13 * sc, hy - 30 * sc), 7 * sc, fill=(236, 150, 180))                # rulos
    return J

DX0, DX1, DY0 = 560, 820, 760
def rellano_puerta(F, t, luz=1.0):
    F.rect(-900, -400, 2000, PISO, fill=(70, 66, 74)); F.rect(-900, PISO, 2000, 3000, fill=(40, 34, 30))
    F.line([(-900, PISO), (2000, PISO)], (90, 80, 70), 6)
    F.rect(DX0 - 26, DY0 - 26, DX1 + 26, PISO, fill=(54, 42, 34))
    F.rect(DX0, DY0, DX1, PISO, fill=_osc((176, 160, 130), luz))                                 # el rellano, de día
    F.rect(DX1 - 40, DY0 + 160, DX1, PISO - 200, fill=_osc((140, 126, 100), luz))               # barandilla de la escalera
    for i in range(5): F.line([(DX0 + 30 + i * 50, PISO - 220), (DX0 + 30 + i * 50, PISO)], _osc((110, 96, 78), luz), 6)
    F.poly([(DX0, DY0), (DX0 - 150, DY0 - 40), (DX0 - 150, PISO + 30), (DX0, PISO)], fill=(92, 62, 44), outline=(40, 26, 18), w=5)   # hoja abierta
    F.rect(140, 520, 330, 760, fill=(40, 40, 46), outline=(110, 96, 80), w=8)                    # espejo de la entrada
    F.text((DX0 + 130, DY0 - 60), "6ºB", 40, (220, 210, 180))

def armario(F, x, y=SUELO, t=0.0, jit=0.0):
    x += noise(t * 40) * jit
    F.rect(x, y - AH, x + AW, y - 12, fill=(78, 56, 42), outline=(36, 24, 18), w=5)
    F.line([(x + AW / 2, y - AH + 20), (x + AW / 2, y - 30)], (36, 24, 18), 5)
    for dx in (-16, 16): F.rect(x + AW / 2 + dx - 4, y - AH * 0.55, x + AW / 2 + dx + 4, y - AH * 0.45, fill=(190, 168, 100))
    F.rect(x - 8, y - AH - 16, x + AW + 8, y - AH, fill=(66, 46, 34), outline=(36, 24, 18), w=4)  # cornisa
    for lx in (x + 14, x + AW - 26): F.rect(lx, y - 12, lx + 12, y, fill=(40, 28, 20))
    return (x, y - AH)

def pasillo_trampilla(F, t, abre=0.0, marcas=1.0, dentro=0.0):
    """pasillo de lado: franja de techo vista desde abajo con la trampilla (abre 0-1: la tapa cae colgando de la bisagra),
    suelo en perspectiva con arañazos del armario hasta debajo de la trampilla. dentro: brillo de dos ojos en el hueco"""
    paredes(F, col=(30, 30, 44))
    F.rect(-900, SUELO - 140, 2000, 3000, fill=(30, 25, 22))                                     # suelo
    for yy in (SUELO - 100, SUELO - 40, SUELO + 40, SUELO + 140): F.line([(-900, yy), (2000, yy)], (40, 34, 30), 3)
    F.line([(-900, SUELO - 140), (2000, SUELO - 140)], (54, 54, 72), 6)
    F.rect(-900, -800, 2000, TP, fill=(36, 36, 50))                                              # techo visto desde abajo
    F.line([(-900, TP), (2000, TP)], (70, 70, 90), 6)
    F.rect(-160, 520, 40, 900, fill=(12, 16, 30), outline=(70, 66, 80), w=10)                    # cuadro
    if marcas > 0:                                                                               # arañazos: del armario a la trampilla
        for i, (dy, a, b) in enumerate(((-30, AX0 + 30, AX1 + 40), (-22, AX0 + 60, AX1 + 20), (-8, AX0 + 10, AX1 + 60),
                                        (-34, AX0 + AW - 40, AX1 + AW - 10), (-16, AX0 + AW - 20, AX1 + AW + 10), (-4, AX0 + AW - 60, AX1 + AW - 30))):
            F.line([(a, SUELO + dy), (b, SUELO + dy + (i % 3 - 1) * 3)], _osc((190, 170, 150), marcas), 4)
    y0, y1 = TP - 82, TP - 10
    F.rect(TX0 - 12, y0 - 10, TX1 + 12, y1 + 10, fill=(26, 26, 36))                              # marco
    F.rect(TX0, y0, TX1, y1, fill=(2, 2, 3) if abre > 0.02 else (42, 42, 56), outline=(20, 20, 28), w=4)
    if abre <= 0.02:
        F.circle((TX1 - 30, (y0 + y1) / 2), 7, fill=(160, 150, 120))                             # tirador
    else:
        if dentro > 0:
            for ex in (TX0 + 150, TX0 + 170): F.circle((ex, y0 + 40), 3, fill=_osc((230, 230, 240), dentro))
        dx = (TX1 - TX0) * ease(abre)                                                            # la tapa, empujada desde dentro, se desliza
        if dx < TX1 - TX0 - 2:
            F.rect(TX0 + dx, y0 + 4, TX1, y1 - 4, fill=_osc((42, 42, 56), 1 - 0.6 * ease(abre)))
            F.line([(TX0 + dx, y0 + 4), (TX0 + dx, y1 - 4)], (8, 8, 10), 5)
    return (TX0 + (TX1 - TX0) / 2, (y0 + y1) / 2)

def brazo_largo(F, hombro, mano, t, codo=1.0, agarra=1.0, w=30):
    """brazo pálido larguísimo con el codo doblado hacia fuera y dedos que se curvan sobre lo que agarra"""
    sx, sy = hombro; hx, hy = mano
    mx, my = (sx + hx) / 2, (sy + hy) / 2
    L_ = math.hypot(hx - sx, hy - sy) + 1
    nx, ny = -(hy - sy) / L_, (hx - sx) / L_
    e = (mx + nx * 120 * codo, my + ny * 120 * codo)
    F.line([hombro, e, mano], (8, 8, 12), w + 10); F.line([hombro, e, mano], PIEL, w)
    for i in range(4):                                                                           # dedos curvados por encima
        fx = hx - 24 + i * 14
        F.line([(hx, hy - 6), (fx, hy - 22), (fx + 12 * agarra, hy + 6 + 12 * agarra)], PIEL, 9)
    return e

def cara_reves(F, c, r, abre=0.4, t=0.0):
    """cara pálida colgando del revés: barbilla arriba, ojos debajo de la boca y el pelo cayendo hacia abajo"""
    hx, hy = c
    F.rect(hx - r * 0.32, hy - r * 4, hx + r * 0.32, hy - r * 1.0, fill=_osc(PIEL, 0.8))           # cuello que sale del hueco
    for i in range(12):                                                                          # pelo colgando
        dx = -r * 0.85 + i * r * 0.155
        F.line([(hx + dx, hy + r * 0.3), (hx + dx * 1.7 + 8 * math.sin(t * 1.4 + i), hy + r * (3.2 + (i * 37 % 9) / 8))], (12, 12, 16), r * 0.22)
    F.ellipse((hx, hy - r * 0.1), r * 0.74, r * 1.32, fill=PIEL)
    F.d.chord([*F.P(hx - r * 0.8, hy - r * 0.2), *F.P(hx + r * 0.8, hy + r * 1.3)], 0, 180, fill=(22, 22, 26))   # cráneo con pelo
    for dx in (-0.3, 0.3):
        F.ellipse((hx + dx * r, hy + r * 0.02), r * 0.25, r * 0.3, fill=(150, 146, 144))
        F.ellipse((hx + dx * r, hy - r * 0.04), r * 0.21, r * 0.3, fill=(2, 2, 4))
        F.circle((hx + dx * r, hy - r * 0.1), r * 0.035, fill=(240, 240, 250))
    F.ellipse((hx, hy - r * 0.7), r * 0.34, r * (0.1 + 0.16 * abre), fill=(2, 2, 4))            # boca abierta, arriba

def _pasillo_noche(F, t, ax, abre=1.0, brazo=None, cara=None, dentro=0.0, jit=0.0, tu=None):
    pasillo_trampilla(F, t, abre=abre, dentro=dentro)
    top = armario(F, ax, t=t, jit=jit)
    if tu is not None:
        TU.draw(F, add(pose(body=-6, head=-34, a1u=40, a1l=60, a2u=-30, a2l=70), jitter(t, 2, 3)), tu, SUELO - 10, f=1, face="scared")
    if cara is not None:
        bk = clamp((cara + 40) / 190)                                                            # brazos abiertos por la pared
        for s_, x0 in ((-1, TX0 + 30), (1, TX1 - 30)):
            e = (x0 + s_ * 170 * bk, TP + 30 * bk)
            m = (x0 + s_ * 260 * bk, TP + 300 * bk)
            F.line([(x0, TP - 30), e, m], (8, 8, 12), 34); F.line([(x0, TP - 30), e, m], PIEL, 24)
            for i in range(4):
                a = math.radians(70 + i * 22 if s_ < 0 else 110 - i * 22)
                F.line([m, (m[0] + math.cos(a) * 60 * bk, m[1] + math.sin(a) * 60 * bk)], PIEL, 8)
        cara_reves(F, (TX0 + 130, TP + cara), 56, abre=0.3 + 0.2 * math.sin(t * 2), t=t)
    if brazo is not None:
        brazo_largo(F, (TX0 + 200, TP - 40), brazo, t)
    return top

# ---------- escenas ----------
def techo(t, D, fi):
    """primer fotograma: el techo de cerca, la lámpara balanceándose y el polvo cayendo; el ruido cruza; bajamos hasta ti"""
    k = ease(seg(t, D * 0.25, D * 0.95))
    xs = lerp(1100, 150, seg(t, 0, D * 0.9))
    F = Frame(fondo(), dict(x=lerp(560, 480, k), y=lerp(560, 1000, k), z=lerp(2.0, 1.05, k), sx=noise(t * 30) * 4))
    cuarto_desvan(F, t)
    lb = lampara(F, t, amp=10)
    polvo(F, xs, t, k=1.0)
    J = tu_tumbado(F, t, face="scared", cuelga=0.0, jit=0.5)
    manta(F)
    img = iluminar(F.finish(), F, [], glows=[((640, 610), 260, 0.6), ((825, PISO - 222), 170, 0.6), (lb, 160, 0.25), (J["head"], 140, 0.3)], amb=0.3, warm=LUNA)
    p = 1.0 if int(t * 4) % 3 else 0.85
    sx_, sy_ = F.P(xs, TECHO - 40)
    img = onomato(img, "RRRRAAS", p * (1 - seg(t, D * 0.8, D)), (clamp(sx_ / S, 230, 850), max(170, sy_ / S - 60)), 0)
    return img, dict(grain=9, flash=(ROJO, 0.35 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.06))

def vecina_(t, D, fi):
    grita = seg(t, D * 0.55, D * 0.62)
    sh = 9 * grita * (1 - seg(t, D * 0.7, D))
    k = ease(seg(t, D * 0.5, D * 0.65))
    F = Frame(fondo("d"), dict(x=lerp(560, 660, k), y=lerp(980, 900, k), z=lerp(1.05, 1.7, k), sx=noise(t * 30) * sh, sy=noise(t * 30, 1) * sh))
    rellano_puerta(F, t)
    pg = mix(pose(a1u=60, a1l=20, a2u=-40, a2l=110, head=4), pose(a1u=35, a1l=-10, a2u=-40, a2l=110, head=10, body=-6), grita)
    vecina(F, add(pg, jitter(t, 2 * grita, 2)), 700, PISO, t=t, f=-1, face="angry")
    TU.draw(F, pose(body=-4, head=-6, a1u=30, a1l=120, a2u=-14, a2l=12), 420, PISO, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((690, 1000), 360, 0.9), ((400, 1000), 300, 0.4)], amb=0.55, warm=DIA)
    return img, dict(grain=7, flash=((255, 255, 255), 0.2 * max(0, 1 - abs(t - D * 0.6) / 0.15)))

def solo(t, D, fi):
    """el pasillo, de día: el armario contra la pared; la cámara sigue los arañazos del suelo hasta debajo de la trampilla"""
    k = ease(seg(t, D * 0.45, D * 0.8))
    F = Frame(fondo(), dict(x=lerp(560, 560, k) + 40 * ease(t / D), y=lerp(1060, 1290, k), z=lerp(1.0, 2.0, k)))
    pasillo_trampilla(F, t)
    armario(F, AX0)
    img = iluminar(F.finish(), F, [], glows=[((520, 900), 700, 0.6), ((700, SUELO - 20), 260, 0.5 * k)], amb=0.48, warm=DIA)
    return img, dict(grain=8)

def encima(t, D, fi):
    """en corte: tu cuarto y, encima, el desván: la cosa avanza a cuatro patas y se tumba justo encima de tu cabeza"""
    k = ease(seg(t, 0, D * 0.35))
    F = Frame(fondo(), dict(x=lerp(480, 560, k), y=lerp(900, 690, k), z=lerp(1.2, 0.8, k)))
    u = seg(t, D * 0.05, D * 0.7)
    cx = lerp(1250, CABEZA_X + 100, ease_out(u))
    tumba = seg(t, D * 0.72, D * 0.9)
    lb = None
    hh = cuarto_desvan(F, t, corte=True, cosa=(cx, tumba, 1.0 if u < 1 else 0.0, seg(t, D * 0.8, D * 0.86)))
    lb = lampara(F, t, amp=8 * (1 - tumba))
    polvo(F, cx, t, k=1 - tumba)
    J = tu_tumbado(F, t, face="scared", cuelga=0.0, jit=0.4)
    manta(F)
    img = iluminar(F.finish(), F, [], glows=[((640, 610), 260, 0.6), ((825, PISO - 222), 170, 0.6), (hh, 260, 0.55), ((CABEZA_X + 200, 300), 300, 0.3), (J["head"], 140, 0.3)], amb=0.3, warm=LUNA)
    para = 0 < t - D * 0.72 < 0.15
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * tumba), glitch=0.25 if para else 0.0)

def trampilla(t, D, fi):
    abre = seg(t, D * 0.4, D * 0.75)
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(640, 770, k), y=lerp(640, 330, k), z=lerp(1.3, 2.6, k)))
    pasillo_trampilla(F, t, abre=abre, dentro=seg(t, D * 0.85, D))
    armario(F, AX0)
    img = iluminar(F.finish(), F, [], glows=[((520, 900), 420, 0.4), ((TX0 + 130, TP - 20), 300, 0.55)], amb=0.4, warm=LUNA)
    return img, dict(grain=10, tint=((255, 0, 30), 0.05 + 0.1 * abre))

def brazo(t, D, fi):
    """baja el brazo, agarra la cornisa del armario y lo arrastra, a tirones, por los arañazos hasta debajo de la trampilla"""
    baja = ease(seg(t, 0, D * 0.3))
    tira = seg(t, D * 0.35, D * 0.92)
    tir = tira + 0.04 * math.sin(tira * 30) * (0 < tira < 1)
    ax = lerp(AX0, AX1, ease(tir))
    F = Frame(fondo(), dict(x=lerp(520, 640, tira), y=860, z=1.0, sx=noise(t * 30) * 5 * (0 < tira < 1)))
    pasillo_trampilla(F, t, abre=1.0)
    top = armario(F, ax, t=t, jit=3 * (0 < tira < 1))
    mano_obj = (top[0] + AW - 20, top[1] - 16)
    mano = (lerp(TX0 + 220, mano_obj[0], baja), lerp(TP - 20, mano_obj[1], baja))
    brazo_largo(F, (TX0 + 200, TP - 40), mano, t, agarra=seg(t, D * 0.25, D * 0.33))
    img = iluminar(F.finish(), F, [], glows=[((520, 900), 420, 0.35), (mano, 200, 0.4)], amb=0.36, warm=LUNA)
    return img, dict(grain=10, tint=((255, 0, 30), 0.12))

def aranazos(t, D, fi):
    """primer plano: las patas del armario encajan en los arañazos; la cámara sube por el armario hasta el hueco negro"""
    k = ease(seg(t, D * 0.25, D * 0.95))
    F = Frame(fondo(), dict(x=lerp(AX1 + AW / 2, AX1 + AW / 2, k), y=lerp(SUELO - 40, TP + 120, k), z=lerp(2.6, 1.3, k)))
    pasillo_trampilla(F, t, abre=1.0, dentro=0.7 * seg(t, D * 0.7, D))
    armario(F, AX1)
    for xx in (TX0 + 40, TX1 - 50):
        for i in range(4): F.line([(xx + i * 10, TP - 14), (xx + i * 10 + 4, TP + 20 * seg(t, D * 0.6, D))], PIEL, 7)
    img = iluminar(F.finish(), F, [], glows=[((AX1 + 130, SUELO - 30), 280, 0.6 * (1 - k) + 0.2), ((TX0 + 130, TP), 220, 0.3)], amb=0.36, warm=LUNA)
    return img, dict(grain=10, tint=((255, 0, 30), 0.1))

def voz(t, D, fi):
    """la cara asoma del revés por la trampilla, con el pelo colgando, y te habla"""
    a = ease(seg(t, D * 0.05, D * 0.45))
    hit = seg(t, D * 0.45, D * 0.5)
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=TX0 + 150, y=lerp(480, 520, k), z=lerp(1.6, 2.3, k), sx=noise(t * 40) * 6 * hit * (1 - seg(t, D * 0.55, D * 0.8))))
    _pasillo_noche(F, t, AX1, cara=lerp(-140, 150, a))
    img = iluminar(F.finish(), F, [], glows=[((TX0 + 150, TP + 150 * a), 260, 0.6), ((520, 900), 400, 0.25)], amb=0.32, warm=LUNA)
    return img, dict(grain=10, tint=((255, 0, 30), 0.15 + 0.1 * hit), flash=(ROJO, 0.35 * max(0, 1 - abs(t - D * 0.46) / 0.15)),
                     glitch=0.3 if 0 < t - D * 0.45 < 0.3 and fi % 3 else 0.0)

def final(t, D, fi):
    """tú en la puerta de tu cuarto, mirando arriba; la cara colgando de la trampilla, sobre el armario. La regla"""
    k = ease(seg(t, 0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(700, 580, k), y=lerp(520, 560, k), z=lerp(1.6, 0.9, k)))
    _pasillo_noche(F, t, AX1, cara=150, tu=300)
    img = iluminar(F.finish(), F, [], glows=[((TX0 + 150, TP + 150), 260, 0.6), ((300, 1100), 260, 0.35)], amb=0.32, warm=LUNA)
    pp = ease_back(seg(t, D * 0.45, D * 0.55)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 140, 1040, 560), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 SE ARRASTRAN"), 210, 62, (255, 255, 255)), (tr("MUEBLES…"), 290, 62, (255, 255, 255)),
                                 (tr("NO SUBAS A MIRAR"), 440, 120, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 600, 850, 690), 26, fill=(230, 30, 50))
        d.text((540, 645), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.22 * pp if pp > 0 else 0.08), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(techo=techo, vecina=vecina_, solo=solo, encima=encima, trampilla=trampilla, brazo=brazo, aranazos=aranazos,
                 voz=voz, final=final)
PAUSA = dict(techo=0.5, vecina=0.5, solo=0.6, encima=0.7, trampilla=0.6, brazo=0.5, aranazos=0.6, voz=0.7, final=2.4)
