"""Si oyes esto a las 3AM — 27: "El cajero de la gasolinera". Paras a repostar a las tres; el cajero te hace señas desde
el cristal y crees que saluda. La luna de atrás de tu coche está empañada por dentro (pista: alguien respira ahí).
Al pagar, el cajero mira tu coche y te pasa un papel: "NO VUELVAS AL COCHE". En su monitor se abre tu puerta de atrás y
algo sale: llevaba ahí todo el viaje. Se sienta al volante, enciende los faros y te llama: "Sube. Te llevo a casa."
Piezas nuevas reutilizables: gasolinera (marquesina, surtidor, tienda 24 h con su escaparate y el cajero), coche_gas
(tu coche aparcado, sin nadie dentro o con la cosa al volante; vaho que respira, huella, puerta de atrás, faros),
tienda_dentro (mostrador con cristal de seguridad y ranura), cctv_surtidor (cámara de seguridad del surtidor), nota_papel."""
import math
import numpy as np
from PIL import Image, ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU
from escenas3am2 import cara_palida, dedos, PIEL, AZUL, AZUL_O
from escenas3am24 import VISITA, _ojo_pez, ojos_ir
from escenas3am26 import pantalla_cam

ROJO = (255, 40, 40)
FLUO = (210, 236, 214)                     # luz de tubo fluorescente
PISO = 1250
CAR_X = 600                                # tu coche (morro hacia la tienda, a la izquierda)
TU_X = 965                                 # tú, junto al surtidor
PUMP_X = 1060
CAJ_X = 110                                # el cajero, tras el escaparate
CAJERO = Fig(shirt=(64, 128, 88), limb=(236, 226, 212))
_BG = {}
def fondo(k="a"):
    if k not in _BG:
        _BG[k] = {"a": gradient((10, 14, 24), (4, 4, 8)), "t": gradient((30, 34, 32), (12, 14, 14))}[k]
    return _BG[k]

def tubo(t, seed=0):
    """parpadeo de un fluorescente viejo"""
    return 0.55 if noise(t * 9, seed) > 0.72 else 1.0

# ---------- piezas ----------
def coche_gas(F, x, piso, t=0.0, vaho=0.0, resp=0.0, huella=0.0, puerta=0.0, cosa=0.0, habla=0.0, faros=0.0, manguera=True):
    """tu coche aparcado (morro a la izquierda), vacío. vaho: luna de atrás empañada por dentro (resp la hace 'respirar');
    huella: mano que se apoya en el vaho desde dentro; puerta: puerta de atrás abierta (0-1); cosa: la cosa al volante;
    habla: boca abierta; faros: luces delanteras encendidas"""
    if faros > 0.02:                                                                  # haz de los faros (hacia la tienda)
        c = tuple(int(v * faros) for v in (120, 118, 96))
        F.poly([(x - 300, piso - 150), (x - 1300, piso - 420), (x - 1300, piso + 120), (x - 300, piso - 110)], fill=c)
    cab = [(x - 170, piso - 170), (x - 95, piso - 300), (x + 150, piso - 300), (x + 255, piso - 170)]
    F.poly(cab, fill=(12, 12, 18))
    F.rect(x - 8, piso - 245, x + 22, piso - 150, fill=(32, 30, 34)); F.rect(x - 4, piso - 288, x + 20, piso - 250, fill=(32, 30, 34))
    F.rect(x + 145, piso - 255, x + 185, piso - 150, fill=(30, 28, 32))               # asiento trasero
    F.line([(x - 132, piso - 238), (x - 112, piso - 178)], (20, 20, 24), 12)           # volante
    if cosa > 0:                                                                      # la cosa, al volante, encorvada contra el techo
        hy = lerp(piso - 150, piso - 252, ease(cosa))
        F.rect(x - 80, hy + 30, x + 10, piso - 160, fill=(14, 14, 16))
        cara_palida(F, (x - 38, hy), 30, abre=0.35 + 0.65 * habla)
        dedos(F, (x - 92, piso - 212), 200, n=4, L_=44, w=5)
    if vaho > 0:                                                                      # luna de atrás empañada (por dentro)
        k = vaho * (0.62 + 0.38 * resp)
        fog = tuple(int(lerp(a, b, k)) for a, b in zip((12, 12, 18), (128, 136, 146)))
        F.poly([(x + 48, piso - 292), (x + 150, piso - 292), (x + 247, piso - 176), (x + 48, piso - 176)], fill=fog)
        for i, dx in enumerate((70, 112, 160, 196)):                                  # gotitas que resbalan
            F.line([(x + dx, piso - 230 + 10 * (i % 2)), (x + dx, piso - 200 + 14 * (i % 3))], tuple(int(v * 0.6) for v in fog), 3)
        if huella > 0:                                                                # una mano apoyada desde dentro
            hx, hy = x + 125, piso - 222
            cl = (10, 10, 14)
            F.ellipse((hx, hy + 6), 20 * huella, 24 * huella, fill=cl)
            for i in range(4):
                F.line([(hx - 14 + i * 9, hy - 10), (hx - 20 + i * 11, hy - 10 - (40 + (i % 2) * 10) * huella)], cl, 7)
            F.line([(hx + 18, hy + 4), (hx + 18 + 22 * huella, hy - 12)], cl, 7)
    if puerta > 0:                                                                    # puerta de atrás abierta: hueco negro
        F.poly([(x + 40, piso - 296), (x + 150, piso - 296), (x + 252, piso - 172), (x + 255, piso - 58), (x + 40, piso - 58)], fill=(4, 4, 6))
    F.poly([(x - 315, piso - 170), (x + 300, piso - 170), (x + 300, piso - 50), (x - 315, piso - 50)], fill=AZUL, outline=AZUL_O, w=6)
    if puerta > 0:
        F.rect(x + 40, piso - 172, x + 255, piso - 56, fill=(4, 4, 6))
    F.line(cab + [cab[0]], AZUL_O, 12); F.line([(x + 40, piso - 300), (x + 40, piso - 170)], AZUL, 14)
    F.line([(x + 40, piso - 150), (x + 40, piso - 60)], AZUL_O, 4); F.rect(x - 10, piso - 140, x + 20, piso - 130, fill=(150, 160, 180))
    F.rect(x + 236, piso - 150, x + 266, piso - 122, fill=(30, 40, 60))               # tapa del depósito
    hl = tuple(int(lerp(a, b, faros)) for a, b in zip((110, 104, 80), (255, 255, 235)))
    F.rect(x - 318, piso - 150, x - 296, piso - 118, fill=hl); F.rect(x + 280, piso - 150, x + 302, piso - 118, fill=(180, 26, 26))
    for wx in (x - 190, x + 175):
        F.circle((wx, piso - 46), 50, fill=(18, 18, 22)); F.circle((wx, piso - 46), 21, fill=(110, 110, 116))
    if puerta > 0:                                                                    # la puerta, girada hacia nosotros
        p = ease(puerta)
        w_ = 215 * (1 - 0.6 * p)
        F.poly([(x + 40, piso - 300), (x + 40 + w_, piso - 300 - 30 * p), (x + 40 + w_, piso - 40 + 30 * p), (x + 40, piso - 56)],
               fill=AZUL, outline=AZUL_O, w=6)
        F.poly([(x + 48, piso - 292), (x + 34 + w_, piso - 292 - 26 * p), (x + 34 + w_, piso - 176), (x + 48, piso - 176)], fill=(70, 78, 92))
    return dict(cara=(x - 38, piso - 252), faro=(x - 307, piso - 134), vaho=(x + 150, piso - 235))

def surtidor(F, t, x=PUMP_X, piso=PISO, litros=0.0):
    F.rect(x - 46, piso - 300, x + 46, piso, fill=(200, 200, 204), outline=(60, 60, 66), w=6)
    F.rect(x - 46, piso - 300, x + 46, piso - 250, fill=(200, 30, 40))
    F.rect(x - 32, piso - 230, x + 32, piso - 180, fill=(10, 16, 12))
    F.text((x, piso - 205), f"{litros:05.2f}", 22, (120, 255, 150))
    F.rect(x - 60, piso - 10, x + 60, piso + 6, fill=(60, 60, 66))

def gasolinera(F, t, litros=0.0, cajero="senas", cristal=True):
    """marquesina, suelo, tienda 24 h con el cajero tras el escaparate"""
    F.rect(-1400, PISO, 2600, 2600, fill=(22, 22, 26))
    F.ellipse((700, PISO + 60), 900, 120, fill=(40, 42, 44))                          # suelo iluminado bajo la marquesina
    for i in range(-6, 10): F.line([(i * 220, PISO + 140), (i * 220 + 120, PISO + 140)], (70, 70, 60), 8)
    # tienda
    F.rect(-460, 600, 260, PISO, fill=(46, 50, 46), outline=(20, 22, 20), w=6)
    F.rect(-460, 600, 260, 680, fill=(200, 30, 40))
    F.text((-100, 641), tr("ABIERTO 24 H"), 46, (255, 255, 255))
    w0, w1, y0, y1 = -420, 220, 740, 1180
    luz = tubo(t, 3)
    F.rect(w0, y0, w1, y1, fill=tuple(int(v * (0.55 + 0.25 * luz)) for v in FLUO))
    for r_ in range(3):                                                               # estanterías
        yy = 790 + r_ * 110
        F.rect(w0 + 20, yy + 60, -100, yy + 70, fill=(90, 96, 90))
        for i in range(8): F.rect(w0 + 30 + i * 38, yy + 10 + (i % 3) * 6, w0 + 58 + i * 38, yy + 60, fill=[(180, 60, 50), (60, 110, 170), (210, 180, 60)][(i + r_) % 3])
    if cajero == "senas":
        k = math.sin(t * 13)
        p = pose(a1u=150 + 22 * k, a1l=25, a2u=-150 + 22 * math.sin(t * 13 + 1.6), a2l=-25, head=4 * k)
        CAJERO.draw(F, add(p, jitter(t, 1.0, 5)), CAJ_X, 1180, f=-1, face="scared", t=t)
    elif cajero == "mira":
        CAJERO.draw(F, pose(a1u=60, a1l=40, a2u=-20, a2l=30), CAJ_X, 1180, f=1, face="scared", t=t)
    F.rect(w0, 1080, w1, y1, fill=(60, 62, 60))                                       # mostrador
    if cristal:
        for dx in (0, 70): F.line([(w0 + 80 + dx, y1), (w0 + 300 + dx, y0)], (230, 240, 236), 6)   # reflejos
    F.rect(w0, y0, w1, y1, outline=(20, 22, 20), w=12)
    F.line([(-100, y0), (-100, y1)], (20, 22, 20), 10)
    # marquesina
    F.rect(330, 330, 1700, 410, fill=(200, 30, 40), outline=(120, 16, 20), w=6)
    F.rect(330, 395, 1700, 410, fill=(240, 240, 240))
    for i in range(4): F.rect(420 + i * 300, 410, 560 + i * 300, 426, fill=tuple(int(v * tubo(t, 10 + i)) for v in (250, 255, 250)))
    F.rect(1300, 426, 1340, PISO, fill=(170, 170, 176))

def luces_gas(F, t, extra=(), amb=0.2):
    g = [((800, 700), 700, 0.75 * tubo(t, 11)), ((-100, 960), 440, 0.75 * tubo(t, 3)), ((PUMP_X, PISO - 200), 160, 0.6)]
    return g + list(extra)

def tu_surtidor(F, t, face="neutral", saluda=0.0, jit=0.0):
    """tú, de pie junto al coche, con la manguera metida en el depósito"""
    p = pose(a1u=72, a1l=8, l1u=4, l2u=-4)
    if saluda > 0: p = add(p, pose(a2u=165 * saluda + 20 * math.sin(t * 10) * saluda, a2l=-20 * saluda, head=-6 * saluda))
    J = TU.draw(F, add(p, jitter(t, jit, 7)), TU_X, PISO, f=-1, face=face, t=t)
    hx, hy = J["a1h"]
    F.line([(PUMP_X - 30, PISO - 170), (PUMP_X - 40, PISO - 60), (hx + 30, hy + 60), (hx, hy)], (16, 16, 18), 9)   # manguera
    F.line([(hx, hy), (CAR_X + 252, PISO - 136)], (30, 30, 34), 14)                                           # boquerel
    return J

def manguera_sola(F):
    F.line([(PUMP_X - 30, PISO - 170), (PUMP_X - 40, PISO - 40), (CAR_X + 320, PISO - 40), (CAR_X + 290, PISO - 120)], (16, 16, 18), 9)
    F.line([(CAR_X + 290, PISO - 120), (CAR_X + 252, PISO - 136)], (30, 30, 34), 14)

# ---------- la tienda por dentro ----------
P2 = 1300
GX0, GX1, GY0, GY1 = 560, 1120, 560, 1050       # cristal de seguridad del mostrador
RAN = (640, 800)                                 # ranura
def tienda_dentro(F, t, cajero="mira", tu_face="neutral", jit=0.0, mano=0.0):
    luz = tubo(t, 21)
    F.rect(-700, 300, 1800, P2, fill=tuple(int(v * 0.32) for v in FLUO))
    F.rect(-700, P2, 1800, 2600, fill=(52, 56, 52))
    for i in range(-4, 10): F.line([(i * 200, P2), (i * 200 - 140, 2600)], (44, 48, 44), 4)
    F.rect(-200, 410, 500, 430, fill=tuple(int(v * luz) for v in (250, 255, 250)))     # tubo del techo
    # escaparate de la izquierda: fuera, tu coche bajo la marquesina
    F.rect(140, 680, 420, 1180, fill=(8, 10, 16))
    F.rect(140, 680, 420, 740, fill=(150, 24, 30))                                      # la marquesina, fuera
    F.rect(190, 1040, 370, 1086, fill=(36, 50, 80)); F.poly([(215, 1040), (240, 1000), (320, 1000), (345, 1040)], fill=(14, 14, 20))
    for wx in (220, 340): F.circle((wx, 1088), 16, fill=(14, 14, 18))
    F.rect(140, 680, 420, 1180, outline=(26, 28, 26), w=14)
    for dx in (0, 40): F.line([(170 + dx, 1180), (280 + dx, 680)], (90, 100, 110), 5)
    # cajero tras el cristal
    if cajero == "mira":
        sh = 9 * math.sin(t * 11)
        p = pose(a1u=86, a1l=6, a2u=-20, a2l=30, head=-10 + sh, body=-4)
        J = CAJERO.draw(F, add(p, jitter(t, 1.4, 4)), 830, 1080, f=-1, face="scared", t=t)
    else:
        J = CAJERO.draw(F, pose(a1u=40, a1l=60, head=-6), 830, 1080, f=-1, face="scared", t=t)
    F.rect(GX0, GY1, GX1, P2, fill=(70, 74, 70), outline=(30, 32, 30), w=8)            # mostrador
    F.rect(GX0, GY0, GX1, GY1, outline=(150, 160, 160), w=8)
    for dx in (0, 80): F.line([(GX0 + 120 + dx, GY1), (GX0 + 380 + dx, GY0)], (200, 214, 214), 5)
    F.rect(RAN[0], GY1 - 6, RAN[1], GY1 + 18, fill=(10, 10, 12))                       # ranura
    if mano > 0:
        F.ellipse((RAN[0] + 90, GY1 - 30), 36, 22, fill=CAJERO.limb)
    Jt = TU.draw(F, add(pose(a1u=60, a1l=50), jitter(t, jit, 2)), 470, P2, f=1, face=tu_face, t=t)
    return J, Jt

# ---------- cámara del surtidor ----------
def _cctv_base(puerta, sale, t):
    F = Frame(fondo(), dict(x=CAR_X + 80, y=PISO - 260, z=0.95))
    gasolinera(F, t, cajero=None)
    coche_gas(F, CAR_X, PISO, t, vaho=1.0, puerta=puerta)
    manguera_sola(F); surtidor(F, t, litros=42.17)
    ojos = []
    if sale > 0:
        s = ease(sale)
        p = mix(pose(body=75, head=-50, l1u=95, l1l=-120, l2u=70, l2l=-110, a1u=150, a1l=-60, a2u=120, a2l=-40),
                pose(body=4, head=8, a1u=8, a1l=6, a2u=-6, a2l=8, l1u=6, l1l=-2, l2u=-6, l2l=-2), s)
        J = VISITA.draw(F, p, lerp(CAR_X + 190, CAR_X + 350, s), PISO, f=1, face="closed", t=t, stretch=lerp(0.95, 1.3, s))
        hx, hy = J["head"]; r = L["head"] * VISITA.scale
        cara_palida(F, (hx, hy), r * 1.05, abre=0.3 + 0.5 * s)
        ojos = [(hx - 0.3 * r * 1.05, hy), (hx + 0.3 * r * 1.05, hy)]
    img = F.finish()
    a = np.asarray(img, np.float32)                                                   # cámara de seguridad: gris verdoso
    g = a @ np.array([0.3, 0.59, 0.11], np.float32)
    g = np.clip((g - 6) * 1.7 + 16, 0, 255)
    img = Image.fromarray(np.clip(np.stack([g * 0.86, g, g * 0.9], -1), 0, 255).astype(np.uint8))
    if ojos: img = ojos_ir(img, F, ojos, k=1.0, r=4)
    return img.crop((0, 555, 1080, 1365))

def cctv_surtidor(t, puerta=0.0, sale=0.0, hora="03:04:12", zoom=1.0, foco=(540, 405)):
    base = _cctv_base(round(puerta, 3), round(sale, 3), t)
    if zoom > 1.001:
        w, h = 1080 / zoom, 810 / zoom
        x0 = clamp(foco[0] - w / 2, 0, 1080 - w); y0 = clamp(foco[1] - h / 2, 0, 810 - h)
        base = base.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((1080, 810), Image.BILINEAR)
    img = _ojo_pez(base.resize((540, 405)).resize((1080, 810), Image.BILINEAR))
    a = np.asarray(img, np.float32)
    rng = np.random.default_rng(int(t * 30) % 997)
    a = a + rng.normal(0, 9, a.shape[:2])[..., None]; a[::4] *= 0.86
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.text((44, 40), hora, font=font(60), fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
    d.text((44, 742), tr("SURTIDOR 2 · CÁMARA 3"), font=font(40), fill=(230, 230, 230), stroke_width=3, stroke_fill=(0, 0, 0))
    if int(t * 3) % 2 == 0: d.ellipse((800, 52, 836, 88), fill=ROJO)
    d.text((852, 44), "REC", font=font(48), fill=ROJO, stroke_width=3, stroke_fill=(0, 0, 0))
    return img

def nota_papel(img, pp, rot=-5):
    """el papel del cajero, en grande, escrito a mano con prisa"""
    if pp <= 0: return img
    w, h = 820, 560
    n = Image.new("RGBA", (w, h), (238, 232, 212, 255)); d = ImageDraw.Draw(n)
    for y in range(90, h, 70): d.line((30, y, w - 30, y), fill=(170, 190, 220, 255), width=3)
    for txt, y in ((tr("NO VUELVAS"), 190), (tr("AL COCHE"), 330)):
        d.text((w / 2, y), txt, font=font(104), fill=(20, 26, 70, 255), anchor="mm")
    d.line((140, 430, 680, 418), fill=(160, 20, 20, 255), width=12)                  # subrayado con rabia
    d.line((160, 462, 640, 452), fill=(160, 20, 20, 255), width=8)
    n = n.rotate(rot, expand=True, resample=Image.BICUBIC)
    s = 0.2 + 0.8 * pp
    n = n.resize((int(n.width * s), int(n.height * s)), Image.BILINEAR)
    img.paste(n, (int(540 - n.width / 2), int(820 - n.height / 2)), n)
    return img

# ---------- escenas ----------
def senas(t, D, fi):
    """primer fotograma: la cara del cajero pegada al escaparate, aterrado, haciendo aspavientos. Se abre el plano:
    él dentro de la tienda y tú, fuera, junto al surtidor"""
    k = ease(seg(t, D * 0.3, D * 0.95))
    F = Frame(fondo(), dict(x=lerp(CAJ_X - 10, 360, k), y=lerp(905, 1000, k), z=lerp(3.4, 0.72, k)))
    gasolinera(F, t, cajero="senas")
    coche_gas(F, CAR_X, PISO, t, vaho=0.8, resp=0.5 + 0.5 * math.sin(t * 2.6))
    surtidor(F, t, litros=t * 3.1)
    tu_surtidor(F, t)
    img = iluminar(F.finish(), F, [], glows=luces_gas(F, t), amb=0.2, warm=FLUO)
    return img, dict(grain=9, flash=(ROJO, 0.4 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.1 * (1 - k)))

def saluda(t, D, fi):
    """tú, tranquilo, le devuelves el saludo con una sonrisa mientras el cajero sigue haciendo señas al fondo"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(560, 640, k), y=lerp(1010, 1040, k), z=lerp(1.0, 1.15, k)))
    gasolinera(F, t, cajero="senas")
    coche_gas(F, CAR_X, PISO, t, vaho=0.85, resp=0.5 + 0.5 * math.sin(t * 2.6))
    surtidor(F, t, litros=10 + t * 3.1)
    tu_surtidor(F, t, face="happy", saluda=ease(seg(t, D * 0.15, D * 0.35)) * (1 - ease(seg(t, D * 0.7, D * 0.85))))
    img = iluminar(F.finish(), F, [], glows=luces_gas(F, t), amb=0.2, warm=FLUO)
    return img, dict(grain=9)

def vaho(t, D, fi):
    """primer plano de la luna de atrás: empañada por dentro, el vaho crece y mengua como una respiración.
    Al final, una mano se apoya en el cristal desde dentro"""
    k = ease(seg(t, 0, D))
    resp = 0.5 + 0.5 * math.sin(t * 3.0 - math.pi / 2)
    hu = ease_out(seg(t, D * 0.72, D * 0.8))
    sh = 8 * (hu > 0) * (1 - seg(t, D * 0.8, D))
    F = Frame(fondo(), dict(x=CAR_X + 150, y=PISO - 235, z=lerp(2.4, 3.3, k), sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    gasolinera(F, t, cajero=None)
    coche_gas(F, CAR_X, PISO, t, vaho=1.0, resp=resp, huella=hu)
    tu_surtidor(F, t)
    img = iluminar(F.finish(), F, [], glows=luces_gas(F, t, [((CAR_X + 150, PISO - 235), 160, 0.5)]), amb=0.2, warm=FLUO)
    return img, dict(grain=10, tint=((255, 0, 30), 0.05 + 0.15 * hu), flash=(ROJO, 0.35 * max(0, 1 - abs(t - D * 0.76) / 0.1)))

def pagar(t, D, fi):
    """dentro de la tienda: el cajero no te mira; señala, temblando, el escaparate. Fuera, tu coche"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo("t"), dict(x=lerp(600, 560, k), y=lerp(1000, 980, k), z=lerp(1.3, 1.45, k)))
    J, Jt = tienda_dentro(F, t, cajero="mira", tu_face="neutral" if t < D * 0.55 else "scared")
    img = iluminar(F.finish(), F, [], glows=[((150, 500), 700, 0.85 * tubo(t, 21)), (J["head"], 200, 0.5), ((280, 1000), 200, 0.4)],
                   amb=0.3, warm=FLUO)
    return img, dict(grain=9, tint=((255, 0, 30), 0.08 * seg(t, D * 0.55, D)))

def papel(t, D, fi):
    """un papel sale por la ranura y, de golpe, lo lees: NO VUELVAS AL COCHE"""
    sl = ease_out(seg(t, D * 0.05, D * 0.4))
    F = Frame(fondo("t"), dict(x=lerp(740, 720, sl), y=lerp(1020, 1060, sl), z=lerp(2.6, 3.0, sl)))
    tienda_dentro(F, t, cajero="pasa", tu_face="scared", mano=1.0 - seg(t, D * 0.35, D * 0.45))
    py = lerp(GY1 - 30, GY1 + 110, sl)
    F.rect(RAN[0] + 20, GY1 + 4, RAN[1] - 20, py, fill=(238, 232, 212))
    F.line([(RAN[0] + 40, py - 40), (RAN[1] - 50, py - 44)], (20, 26, 70), 6)
    img = iluminar(F.finish(), F, [], glows=[((720, 1060), 300, 0.8 * tubo(t, 21))], amb=0.3, warm=FLUO)
    pp = ease_back(seg(t, D * 0.42, D * 0.55))
    def ov(im): return nota_papel(im, pp, rot=-5 + 2 * math.sin(t * 20) * pp)
    hit = pp > 0.5
    return img, dict(grain=9, overlay=ov, dark=0.45 * seg(t, D * 0.4, D * 0.5), tint=((255, 0, 30), 0.12 * hit),
                     flash=(ROJO, 0.35 * max(0, 1 - abs(t - D * 0.5) / 0.12)))

def monitor(t, D, fi):
    """el monitor del cajero: la cámara del surtidor. Tu coche, solo. La puerta de atrás se abre sola"""
    k = ease(seg(t, 0, D))
    pu = ease(seg(t, D * 0.3, D * 0.85))
    cam = cctv_surtidor(t, puerta=pu, hora=f"03:04:{12 + int(t):02d}", zoom=lerp(1.0, 1.35, k), foco=(600, 430))
    img = pantalla_cam(cam, z=1.0, cy=800)
    return img, dict(grain=9, glitch=0.25 if fi % 19 == 0 else 0.0, tint=((255, 0, 30), 0.05 + 0.06 * pu))

def sale(t, D, fi):
    """algo se despliega fuera de la puerta de atrás, mucho más alto que el coche, y gira la cara hacia la cámara"""
    s = seg(t, D * 0.05, D * 0.7)
    z = lerp(1.35, 1.35, 0) if t < D * 0.72 else lerp(1.35, 2.6, ease(seg(t, D * 0.72, D * 0.82)))
    cam = cctv_surtidor(t, puerta=1.0, sale=s, hora=f"03:04:{18 + int(t):02d}", zoom=z, foco=(700, 250))
    hit = t > D * 0.72
    sh = noise(t * 40) * 12 * hit * (1 - seg(t, D * 0.8, D))
    img = pantalla_cam(cam, z=1.0, cy=800, sx=sh)
    return img, dict(grain=10, glitch=0.35 if hit and fi % 3 else (0.2 if fi % 17 == 0 else 0.0), tint=((255, 0, 30), 0.08 + 0.14 * hit),
                     flash=(ROJO, 0.4 * max(0, 1 - abs(t - D * 0.74) / 0.12)))

def volante(t, D, fi):
    """desde dentro de la tienda, por el escaparate: la cosa está al volante. Los faros se encienden y te deslumbran.
    Abre la boca: 'Sube. Te llevo a casa.'"""
    k = ease(seg(t, 0, D))
    fa = ease_out(seg(t, D * 0.25, D * 0.3))
    habla = (0.5 + 0.5 * math.sin(t * 16)) if D * 0.43 < t < D * 0.9 else 0.0
    F = Frame(fondo(), dict(x=lerp(CAR_X - 20, CAR_X - 38, k), y=lerp(PISO - 200, PISO - 250, k), z=lerp(1.8, 3.2, k)))
    gasolinera(F, t, cajero=None, cristal=False)
    c = coche_gas(F, CAR_X, PISO, t, vaho=1.0, puerta=1.0, cosa=1.0, habla=habla, faros=fa)
    manguera_sola(F)
    for x_ in (CAR_X - 520, CAR_X + 420): F.rect(x_ - 16, 0, x_ + 16, 2400, fill=(16, 18, 16))   # marco del escaparate
    F.rect(-1000, PISO - 380, 2000, PISO - 360, fill=(16, 18, 16))
    img = iluminar(F.finish(), F, [], glows=[(c["cara"], 110, 0.55 + 0.3 * fa), (c["faro"], 160 + 500 * fa, 0.2 + 0.8 * fa),
                                             ((CAR_X, PISO - 500), 600, 0.5 * tubo(t, 11))], amb=0.2, warm=(255, 250, 230))
    ojos = [(c["cara"][0] - 9, c["cara"][1]), (c["cara"][0] + 9, c["cara"][1])]
    img = ojos_ir(img, F, ojos, k=0.6 * fa, r=3)
    return img, dict(grain=10, flash=((255, 255, 240), 0.55 * max(0, 1 - abs(t - D * 0.28) / 0.15)),
                     tint=((255, 0, 30), 0.06 + 0.12 * (habla > 0)), glitch=0.25 if habla > 0 and fi % 6 == 0 else 0.0)

def final(t, D, fi):
    """plano general: los faros encendidos apuntando a la tienda; la cosa al volante; tú y el cajero tras el cristal. La regla"""
    k = ease(seg(t, 0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(CAR_X - 40, 360, k), y=lerp(PISO - 240, 820, k), z=lerp(2.4, 0.72, k)))
    gasolinera(F, t, cajero="mira")
    TU.draw(F, SCARED, -150, 1180, f=1, face="scared", t=t)
    F.rect(-420, 1080, 220, 1180, fill=(60, 62, 60))
    c = coche_gas(F, CAR_X, PISO, t, vaho=1.0, puerta=1.0, cosa=1.0, habla=0.3 + 0.2 * math.sin(t * 3), faros=0.9 + 0.1 * math.sin(t * 30))
    manguera_sola(F); surtidor(F, t, litros=42.17)
    img = iluminar(F.finish(), F, [], glows=luces_gas(F, t, [(c["faro"], 600, 0.9), (c["cara"], 90, 0.6)]), amb=0.2, warm=(255, 250, 230))
    img = ojos_ir(img, F, [(c["cara"][0] - 9, c["cara"][1]), (c["cara"][0] + 9, c["cara"][1])], k=0.7, r=3)
    pp = ease_back(seg(t, D * 0.42, D * 0.52)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 130, 1040, 640), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 EL CAJERO"), 200, 62, (255, 255, 255)), (tr("TE HACE SEÑAS…"), 280, 62, (255, 255, 255)),
                                 (tr("LÉELAS"), 470, 150, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 680, 850, 770), 26, fill=(230, 30, 50))
        d.text((540, 725), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.22 * pp if pp > 0 else 0.08), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(senas=senas, saluda=saluda, vaho=vaho, pagar=pagar, papel=papel, monitor=monitor, sale=sale, volante=volante, final=final)
PAUSA = dict(senas=0.4, saluda=0.4, vaho=0.8, pagar=0.5, papel=0.8, monitor=0.6, sale=0.8, volante=0.8, final=2.4)
