"""Escenas del episodio 15 (temporada 2, "El cristalero"): huyen con Lucía por la ciudad, el viejo cristalero los esconde
en su taller lleno de ventanas nuevas con huellas de dedos larguísimos, lo pillan hablando con el Asomado, los encierra
y su nieto ya dormía detrás de un cristal."""
import math, random
from functools import lru_cache
from motor import *
from escenas import base, GLASS
from escenas6 import NINA, coletas
from escenas7 import NINO
from escenas12 import asomado, edificios_tapados
from escenas13 import panel, huella, dormido_panel, asomado_en, PISO, VERDE

CALIDO = (255, 190, 110)

@lru_cache(None)
def fondo(kind):
    if kind == "taller": return gradient((30, 20, 16), (16, 11, 10))
    if kind == "noche": return gradient((8, 10, 14), (14, 16, 20))
    return base(kind)

# ---------- piezas nuevas ----------
CRIS = Fig(shirt=(118, 84, 58), limb=(226, 220, 210), scale=0.95)

def cristalero(F, p, x, piso=PISO, f=1, face="neutral", t=0.0):
    """el viejo cristalero: delantal de cuero, barba blanca, calvo con mechones grises y gafas redondas"""
    J = CRIS.draw(F, p, x, piso, f=f, face=face, t=t)
    sc = CRIS.scale; r = 33 * sc
    nx, ny = J["neck"]; hx_, hy_ = J["hip"]
    F.poly([(nx - 20 * sc, ny + 14 * sc), (nx + 20 * sc, ny + 14 * sc), (hx_ + 30 * sc, hy_ + 44 * sc), (hx_ - 30 * sc, hy_ + 44 * sc)],
           fill=(92, 60, 38), outline=(60, 38, 24), w=3 * sc)                                   # delantal
    hx, hy = J["head"]; blanco = (232, 232, 236)
    F.poly([(hx - r * 0.78, hy + r * 0.3), (hx + r * 0.78, hy + r * 0.3), (hx + f * r * 0.15, hy + r * 1.45)], fill=blanco)   # barba
    for s_ in (-1, 1): F.circle((hx + s_ * r * 0.92, hy - r * 0.15), r * 0.3, fill=(200, 200, 206))                          # mechones
    for dx in (-9, 11):
        F.circle((hx + f * 9 * sc + dx * sc, hy - 5 * sc), 9 * sc, outline=(40, 34, 30), w=3 * sc)                          # gafas
    return J

def ventana_nueva(F, x, y0, w, h, brillo=0.3, luz=0.0, huellas=0.0, seed=0):
    """ventana recién hecha apoyada en la pared: cristal, marco de madera clara y cruceta"""
    panel(F, x, y0, w, h, brillo=brillo, luz=luz)
    F.rect(x - 10, y0 - 10, x + w + 10, y0 + h + 10, outline=(150, 112, 70), w=14)
    F.line([(x + w / 2, y0), (x + w / 2, y0 + h)], (150, 112, 70), 10); F.line([(x, y0 + h * 0.45), (x + w, y0 + h * 0.45)], (150, 112, 70), 10)
    if huellas > 0:
        r = random.Random(seed)
        for i in range(2):
            k = ease(seg(huellas, i * 0.4, i * 0.4 + 0.6))
            if k > 0: huella(F, x + w * (0.25 + 0.5 * i) + r.uniform(-10, 10), y0 + h * (0.25 + 0.4 * i), k, 1.3)

def taller_int(F, t=0.0, lampara=1.0):
    """interior del taller: suelo de tablas, banco de trabajo con herramientas y lámpara colgante"""
    F.rect(-800, PISO, 1900, 2800, fill=(26, 18, 14))
    for i in range(-6, 14): F.line([(i * 140, PISO), (i * 140 - 60, 2000)], (36, 26, 20), 4)
    F.line([(-800, PISO), (1900, PISO)], (60, 44, 32), 6)
    for i in range(6): F.rect(-800, 200 + i * 190, 1900, 206 + i * 190, fill=(36, 26, 22))   # tablones de la pared
    F.rect(700, 1010, 1080, 1040, fill=(84, 58, 38)); F.rect(720, 1040, 744, PISO, fill=(60, 42, 28)); F.rect(1036, 1040, 1060, PISO, fill=(60, 42, 28))
    F.line([(760, 1005), (840, 980)], (130, 134, 140), 6); F.circle((930, 995), 14, fill=(80, 140, 170))   # cortavidrios y gota de cristal
    sw = 8 * math.sin(t * 1.3)
    F.line([(540, 0), (540 + sw, 300)], (40, 34, 30), 4)
    F.poly([(500 + sw, 300), (580 + sw, 300), (610 + sw, 350), (470 + sw, 350)], fill=(60, 50, 40))
    F.circle((540 + sw, 356), 18, fill=tuple(int(lerp(40, v, lampara)) for v in CALIDO))

def taller_ext(F, x, piso, puerta=0.0, t=0.0):
    """fachada del taller: ladrillo, escaparate lleno de cristales, rótulo y puerta que se abre con luz cálida"""
    F.rect(x, piso - 760, x + 760, piso, fill=(46, 30, 28))
    for row in range(12):
        for col in range(8):
            F.rect(x + col * 96 + (row % 2) * 48, piso - 760 + row * 64, x + col * 96 + (row % 2) * 48 + 90, piso - 760 + row * 64 + 58, fill=(54, 36, 32))
    F.rect(x - 20, piso - 800, x + 780, piso - 760, fill=(30, 20, 18))
    F.rect(x + 120, piso - 740, x + 640, piso - 650, fill=(24, 18, 16), outline=(150, 112, 70), w=6)
    F.text((x + 380, piso - 695), tr("CRISTALERO"), 50, (210, 170, 110))
    F.rect(x + 40, piso - 560, x + 400, piso - 150, fill=(60, 44, 30))                       # escaparate iluminado
    for i in range(4): panel(F, x + 60 + i * 84, piso - 520, 70, 340, brillo=0.5, luz=0.15)
    F.rect(x + 36, piso - 564, x + 404, piso - 146, outline=(150, 112, 70), w=10)
    dx0 = x + 480; dw = 180
    F.rect(dx0, piso - 400, dx0 + dw, piso, fill=tuple(int(lerp(20, v, puerta)) for v in (230, 170, 100)))
    ow = dw * (1 - 0.85 * puerta)
    F.rect(dx0, piso - 400, dx0 + ow, piso, fill=(70, 46, 30), outline=(40, 26, 18), w=4)
    F.circle((dx0 + ow - 24, piso - 200), 8, fill=GOLD_)

GOLD_ = (212, 170, 80)

def sabana(F, x, y0, w, h, k):
    """sábana que tapa un panel y cae (k 0 = tapado, 1 = en el suelo)"""
    if k >= 1:
        F.poly([(x - 20, PISO), (x + w + 30, PISO), (x + w + 10, PISO - 40), (x + 10, PISO - 50)], fill=(170, 166, 156)); return
    top = lerp(y0 - 20, PISO - 60, ease(k)); sk = 60 * math.sin(k * math.pi)
    F.poly([(x - 20 + sk, top), (x + w + 20 + sk, top + 10), (x + w + 30, PISO), (x - 30, PISO)], fill=(180, 176, 166), outline=(120, 116, 108), w=3)

# ---------- escenas ----------
def escapan(t, D, fi):
    pan = ease(t / D)
    cx = lerp(300, 1300, pan)
    F = Frame(base("calle"), dict(x=cx, y=980, z=1.15, sx=noise(t * 25) * 5, sy=noise(t * 25, 1) * 5))
    F.circle((cx + 320, 380), 70, fill=(220, 224, 236))
    edificios_tapados(F, -600, 2600, 820, seed=15, k=1.0)
    F.rect(-800, 820, 2800, PISO, fill=(28, 26, 38))
    for i in range(7):                                                          # escaparates a pie de calle
        panel(F, -300 + i * 400, 880, 300, 330, brillo=0.4, luz=0.1)
    F.rect(-800, PISO, 2800, 2700, fill=(18, 19, 26)); F.line([(-800, PISO), (2800, PISO)], (54, 56, 70), 6)
    xs = cx + 40
    # la cara del Asomado salta de escaparate en escaparate detrás de ellos
    i = int((xs - 330 + 300) // 400); px = -300 + i * 400
    asomado_en(F, (px + 150, 1050), 0.85, t, mueca=0.3)
    LEO.draw(F, run(t + 0.2), xs + 200, PISO, f=1, face="scared")
    Jn = NORA.draw(F, run(t), xs + 60, PISO, f=1, face="scared")
    Jl = NINA.draw(F, run(t + 0.4), xs - 70, PISO, f=1, face="scared"); coletas(F, Jl, 0.8)
    CARMEN.draw(F, walk(t, 1.0, 1.5), xs - 210, PISO, f=1, face="scared")
    return F.finish(), dict(grain=8, tint=(VERDE, 0.06), flash=(VERDE, 0.35 * (1 - seg(t, 0, 0.35))))

def portal(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("calle"), dict(x=lerp(520, 640, zp), y=lerp(960, 990, zp), z=lerp(1.0, 1.15, zp)))
    F.circle((900, 330), 60, fill=(220, 224, 236))
    edificios_tapados(F, -600, 1800, 1000, seed=21, k=1.0)
    F.rect(-800, PISO, 2000, 2700, fill=(18, 19, 26)); F.line([(-800, PISO), (2000, PISO)], (54, 56, 70), 6)
    op = ease(seg(t, D * 0.1, D * 0.4))
    taller_ext(F, 120, PISO, puerta=op, t=t)
    llama = math.sin(t * 9) if t > D * 0.45 else 0
    cristalero(F, pose(head=-6, a1u=lerp(20, 110, op) + 25 * llama, a1l=lerp(10, 60, op), a2u=-20), 700, PISO, f=-1, face="neutral", t=t)
    w = ease(seg(t, 0, D * 0.8)); stop = w >= 1
    for fig, dx, ph in ((CARMEN, -150, 0), (NORA, 30, 0.3), (LEO, 170, 0.6)):
        fig.draw(F, pose(head=-8) if stop else run(t + ph, 0.9), lerp(-300, 330, w) + dx, PISO, f=1, face="scared")
    Jl = NINA.draw(F, pose(head=-8) if stop else run(t + 0.45, 0.9), lerp(-300, 330, w) - 50, PISO, f=1, face="scared"); coletas(F, Jl, 0.8)
    img = F.finish()
    return img, dict(grain=7)

def ventanas(t, D, fi):
    pan = ease(t / D)
    F = Frame(fondo("taller"), dict(x=lerp(260, 820, pan), y=920, z=1.12))
    taller_int(F, t)
    for i in range(8):                                                          # ventanas nuevas apoyadas en la pared
        x = -300 + i * 230
        ventana_nueva(F, x, 640 + (i % 2) * 40, 190, PISO - 650 - (i % 2) * 40 - 10, brillo=0.3 + 0.2 * math.sin(t + i))
    cristalero(F, pose(head=-4, a1u=60, a1l=40, a2u=40, a2l=60), 900, PISO, f=-1, face="happy", t=t)
    LEO.draw(F, pose(head=-14), 330, PISO, f=1, face="neutral")
    NORA.draw(F, pose(head=-16, a1u=20), 470, PISO, f=1, face="neutral")
    Jl = NINA.draw(F, pose(head=-10, a2u=-40), 590, PISO, f=1, face="neutral"); coletas(F, Jl, 0.8)
    return F.finish(), dict(grain=7, tint=(CALIDO, 0.05))

def marcas(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("taller"), dict(x=lerp(560, 520, zp), y=lerp(1050, 1060, zp), z=lerp(1.5, 1.75, zp), sx=noise(t * 20) * 2 * zp))
    taller_int(F, t)
    ventana_nueva(F, 300, 560, 420, 660, brillo=0.4, huellas=seg(t, D * 0.1, D * 0.75), seed=2)
    ventana_nueva(F, -150, 600, 300, 620, brillo=0.3, huellas=seg(t, D * 0.35, D * 0.95), seed=5)
    ventana_nueva(F, 840, 600, 300, 620, brillo=0.3, huellas=seg(t, D * 0.45, D * 1.0), seed=7)
    NORA.draw(F, pose(head=-10, a1u=lerp(20, 120, seg(t, D * 0.6, D * 0.8)), a1l=50, body=-6), 760, PISO, f=-1,
              face="scared" if t > D * 0.5 else "neutral")
    return F.finish(), dict(grain=8, tint=(VERDE, 0.06 * seg(t, D * 0.3, D)), dark=0.1)

def pacto(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("noche"), dict(x=lerp(580, 600, zp), y=lerp(940, 930, zp), z=lerp(1.1, 1.3, zp)))
    taller_int(F, t, lampara=0.0)
    k = ease(seg(t, 0, D * 0.3))
    ventana_nueva(F, 640, 520, 360, 700, brillo=0.2, luz=0.6 * k)
    asomado(F, (820, 820), 0.95 * k, t, mueca=0.15, dedos=0.0)
    hab = seg(t, D * 0.5, D * 0.95)
    cristalero(F, pose(head=-6, a1u=lerp(40, 80, hab) + 12 * math.sin(t * 6) * (hab > 0), a1l=40, a2u=-10), 520, PISO, f=1,
               face="talk" if hab > 0 else "neutral", t=t)
    # Nora espía desde la puerta de la izquierda
    F.rect(150, 780, 360, PISO, fill=(10, 8, 8)); F.rect(150, 780, 360, PISO, outline=(60, 42, 28), w=10)
    NORA.draw(F, pose(head=6, body=-8, a1u=40, a1l=60), 300, PISO, f=1, face="scared")
    img = iluminar_(F, [((820, 820), 420, 0.8 * k)])
    return img, dict(grain=8, tint=(VERDE, 0.1))

def iluminar_(F, glows):
    from escenas5 import iluminar
    return iluminar(F.finish(), F, [], glows=glows, amb=0.4, warm=(150, 255, 170))

def encerrados(t, D, fi):
    lock = D * 0.25
    zz = ease_out(seg(t, D * 0.45, D * 0.85))
    sh = 10 * math.exp(-max(0, t - lock) * 8) if t > lock else 0
    F = Frame(fondo("noche"), dict(x=lerp(560, 600, zz), y=lerp(900, 880, zz), z=lerp(1.0, 1.2, zz),
                                   sx=noise(t * 40) * (sh + 4 * zz), sy=noise(t * 40, 2) * (sh + 4 * zz)))
    taller_int(F, t, lampara=0.2)
    caras = []
    for i in range(4):                                                          # todas las ventanas se encienden con su cara
        x = -160 + i * 270; y0 = 560 + (i % 2) * 60
        a = ease(seg(t, D * (0.35 + 0.08 * i), D * (0.5 + 0.08 * i)))
        ventana_nueva(F, x, y0, 230, 560 - (i % 2) * 60, brillo=0.3, luz=0.7 * a)
        asomado_en(F, (x + 115, y0 + 250), a * 0.9, t + i, mueca=0.35)
        caras.append(((x + 115, y0 + 250), 240, 0.7 * a))
    # puerta cerrada con llave a la derecha (Leo la golpea)
    F.rect(880, 760, 1060, PISO, fill=(70, 46, 30), outline=(40, 26, 18), w=6); F.circle((900, 1020), 9, fill=GOLD_)
    gol = abs(math.sin(t * 10)) if t > lock else 0
    LEO.draw(F, pose(body=lerp(0, 12, gol), head=-6, a1u=lerp(90, 120, gol), a1l=lerp(40, 10, gol), a2u=60, a2l=40), 790, PISO, f=1, face="angry")
    NORA.draw(F, SCARED, 300, PISO, f=1, face="scared")
    Jl = NINA.draw(F, SCARED, 430, PISO, f=-1, face="scared"); coletas(F, Jl, 0.8)
    CARMEN.draw(F, pose(head=-6, a1u=60, a1l=30), 570, PISO, f=-1, face="scared")
    img = iluminar_(F, caras + [((540, 356), 200, 0.3)])
    return img, dict(grain=9, tint=(VERDE, 0.08 + 0.1 * zz), glitch=0.3 * zz if fi % 4 == 0 else 0.0,
                     flash=((255, 255, 255), 0.5 * math.exp(-max(0, t - lock) * 9) if t > lock else 0))

def giro(t, D, fi):
    caida = seg(t, D * 0.15, D * 0.45)
    zz = ease(seg(t, D * 0.45, D))
    F = Frame(fondo("noche"), dict(x=lerp(560, 640, zz), y=lerp(920, 860, zz), z=lerp(1.1, 1.9, zz),
                                   sx=noise(t * 30) * 3 * zz, sy=noise(t * 30, 2) * 3 * zz))
    taller_int(F, t, lampara=0.3)
    PXg, PYg, PW, PH = 500, 520, 300, 700
    panel(F, PXg, PYg, PW, PH, brillo=0.3, luz=0.5 * ease(caida))
    J = dormido_panel(F, PXg, PYg, PW, PH, NINO, t)
    if t > D * 0.6: huella(F, PXg + 230, PYg + 160, ease(seg(t, D * 0.6, D * 0.8)), 1.4)   # dedos larguísimos junto al niño
    sabana(F, PXg, PYg, PW, PH, caida)
    rod = ease(seg(t, D * 0.4, D * 0.6))                                        # el abuelo cae de rodillas
    p = mix(pose(head=-4, a1u=80, a1l=40, a2u=60), pose(body=10, head=20, a1u=120, a1l=60, a2u=110, a2l=60, l1u=90, l1l=-90, l2u=10, l2l=-90), rod)
    cristalero(F, p, 380, PISO, f=1, face="scared" if rod > 0.3 else "neutral", t=t)
    img = iluminar_(F, [((PXg + PW / 2, PYg + PH / 2), 420, 0.8 * ease(caida))])
    return img, dict(grain=8, tint=(VERDE, 0.1), flash=(VERDE, 0.35 * math.exp(-abs(t - D * 0.45) * 10)))

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    return F.finish(), {}

ESCENA_FN = dict(escapan=escapan, portal=portal, ventanas=ventanas, marcas=marcas, pacto=pacto, encerrados=encerrados, giro=giro, final=final)
PAUSA = dict(escapan=0.6, portal=0.4, ventanas=0.4, marcas=0.5, pacto=0.6, encerrados=0.6, giro=1.2, final=1.9)
