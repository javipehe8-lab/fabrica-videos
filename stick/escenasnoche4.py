"""TURNO DE NOCHE 4 — "No sirvas a nadie que pague con monedas antiguas" (escenas 3D con turno3d)."""
import math, os, random
from PIL import ImageDraw, ImageFilter
from motor import *
from motor3d import *
from turno3d import *

G = __import__("guionnoche4" + ("_en" if IDIOMA == "en" else ""))
PUERTA = (-2.9, -0.3)                   # entrada de la tienda
MOST = (1.0, -1.3)                      # dónde se para el anciano, frente a la caja
HOY, ANTES = "15 NOV 2026", "15 NOV 1986"
PESETA = (196, 168, 92)
COCHE_V = (7.0, 4.2)                    # el coche viejo, aparcado junto a la fachada
VIEJO = (176, 160, 120)                 # color beige de coche de los 80
# monedas sobre el mostrador (lado del cliente) y, al devolverlas, empujadas hacia él
MON = [(1.48, -2.12), (1.56, -2.04), (1.4, -2.02), (1.51, -1.95)]

def hora(s0):
    s = 3 * 3600 + 41 * 60 + int(s0)
    return f"{s // 3600:02d}:{s // 60 % 60:02d}:{s % 60:02d}"

def _camino(a):
    return lerp(PUERTA[0], MOST[0], a), lerp(PUERTA[1], MOST[1], a)

def _yaw_a_mi(x, z):
    return math.atan2(1.4 - x, -2.7 - z)

def _base(t, luz=1.0, fecha=HOY, **kw):
    esc = mundo(t, luz); caja_registradora(esc, fecha=fecha, **kw)
    return esc

def llegada(t, D, fi):
    """llegas a la gasolinera; por la carretera, en la niebla, camina una figura encorvada sin coche"""
    k = ease(min(1, t / D))
    esc = _base(t)
    coche(esc, -9.5, 4.0, yaw=1.4, col=(70, 30, 30))
    anciano(esc, walk(t, 0.35, 0.45), lerp(5.5, 3.8, k), lerp(14.5, 9.5, k), yaw=math.pi + 0.3, cara="ninguna")
    cam = Camara(ojo=(lerp(1.5, -0.5, k), lerp(1.7, 1.6, k), lerp(27, 18, k)), mira=(lerp(4.5, 0, k), 1.7, lerp(14, 0, k)), fov=56)
    img = etiquetas(esc.render(cam, luces_base()), esc, cam)
    return img, dict(grain=8)

def lista(t, D, fi):
    esc = _base(t)
    cam = cam_mostrador(t, mira=(0.6, 0.6, -1.5), fov=50)
    img = esc.render(cam, luces_base()).filter(ImageFilter.GaussianBlur(10))
    z = lerp(0.95, 1.06, ease(t / D))
    hoja_reglas(img, t, G.REGLAS, resalta=3 if t > D * 0.12 else None, zoom=z)
    return img, dict(grain=6)

def anciano_(t, D, fi):
    """entra un anciano, despacio, y llega hasta la caja. No está mojado: no deja huellas."""
    a = ease(seg(t, D * 0.05, D * 0.85))
    esc = _base(t)
    x, z = _camino(a)
    p = walk(t, 0.35, 0.45) if 0 < a < 1 else STAND
    anciano(esc, p, x, z, yaw=_yaw_a_mi(x, z))
    parp = 0.55 if (fi // 3) % 23 == 0 else 1.0                               # el fluorescente parpadea al entrar
    cam = Camara(ojo=(1.4, 1.75 + 0.01 * math.sin(t * 2), -2.75), mira=(lerp(-2.6, 0.9, a), lerp(1.1, 1.2, a), lerp(0.4, -1.2, a)), fov=lerp(50, 44, a))
    img = esc.render(cam, luces_base(parp))
    return img, dict(grain=8)

def monedas_(t, D, fi):
    """primer plano del mostrador: el tabaco, las pesetas (1986) cayendo una a una y la pantalla de la caja: 15 NOV 2026"""
    esc = _base(t)
    anciano(esc, add(STAND, pose(a2u=40, a2l=40)), MOST[0], MOST[1], yaw=_yaw_a_mi(*MOST), cara="ninguna")
    tabaco(esc, 1.25, -1.7)
    n = min(len(MON), int(seg(t, D * 0.15, D * 0.6) * len(MON) + 0.999))
    monedas(esc, [(x, 1.12, z) for x, z in MON[:n]], PESETA, r=0.042, texto="1986")
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(lerp(1.62, 1.6, k), lerp(2.15, 2.05, k), lerp(-3.3, -3.15, k)), mira=(1.74, 1.32, -1.98), fov=lerp(52, 48, k))
    img = esc.render(cam, luces_base())
    return etiquetas(img, esc, cam), dict(grain=7)

def niego(t, D, fi):
    """le devuelves las monedas empujándolas hacia él; levanta la cabeza y te mira (habla)"""
    habla = t > D * 0.45
    esc = _base(t)
    tabaco(esc, 0.75, -1.8)
    emp = ease(seg(t, D * 0.05, D * 0.3))
    monedas(esc, [(x - 0.3 * emp, 1.12, z + 0.45 * emp) for x, z in MON], PESETA, r=0.042)
    cab = add(STAND, pose(head=-6 - 10 * ease(seg(t, D * 0.35, D * 0.5))))
    anciano(esc, cab, MOST[0], MOST[1], yaw=_yaw_a_mi(*MOST), cara="neutral")
    k = ease(seg(t, D * 0.3, D))
    cam = Camara(ojo=(lerp(1.35, 1.25, k), lerp(1.66, 1.6, k), -2.6), mira=(lerp(1.3, 1.02, k), lerp(1.02, 1.55, k), lerp(-1.75, -1.3, k)),
                 fov=lerp(46, 30, k), roll=0.015 * math.sin(t * 1.3))
    img = esc.render(cam, luces_base())
    return img, dict(grain=9, tint=((255, 0, 30), 0.14 * seg(t, D * 0.45, D)))

def camara(t, D, fi):
    """CAM 2: un coche viejo, sin luces, al final de la marquesina. Alguien con tu uniforme le abre la puerta al anciano y mira a la cámara."""
    esc = _base(t)
    coche(esc, *COCHE_V, yaw=-math.pi / 2, col=VIEJO)
    a = ease(seg(t, 0, D * 0.6))
    ax, az = lerp(2.4, 5.0, a), lerp(2.0, 2.6, a)
    anciano(esc, walk(t, 0.35, 0.45) if a < 1 else STAND, ax, az, yaw=math.atan2(5.0 - 2.4, 2.6 - 2.0), cara="ninguna")
    gira = ease(seg(t, D * 0.62, D * 0.85))
    rx, rz = 6.2, 2.9
    yaw_cam = math.atan2(-6.2 - rx, 2.6 - rz)
    empleado(esc, add(STAND, pose(a1u=70, a1l=10, head=-5)), rx, rz, yaw=lerp(-1.6, yaw_cam, gira), cara="ninguna")
    k = ease(seg(t, 0, D * 0.85))
    base = cam_cctv(2)
    cam = Camara(ojo=base.ojo, mira=(lerp(6.5, 6.0, k), lerp(0.8, 1.0, k), lerp(7.2, 3.0, k)), fov=lerp(60, 26, k))
    img = esc.render(cam, luces_base())
    img = cctv(etiquetas(img, esc, cam), 2, hora(52 + t))
    return img, dict(grain=12, glitch=0.3 if fi % 17 < 2 else 0.0)

def giro(t, D, fi):
    """el cajón de la caja se abre solo hacia ti: lleno de pesetas"""
    ab = ease_out(seg(t, D * 0.08, D * 0.3))
    esc = _base(t, cajon=ab, pesetas=36)
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(lerp(1.75, 1.85, k), lerp(1.75, 1.62, k), lerp(-2.95, -2.75, k)), mira=(1.9, 1.17, lerp(-2.2, -2.25, k)), fov=lerp(48, 36, k))
    img = esc.render(cam, luces_base(0.85))
    q = proyectar(cam, (1.9, 1.17, -2.2))
    if q and ab > 0.9:                                         # brillos sobre el metal de las monedas
        d = ImageDraw.Draw(img); r = random.Random(fi // 3)
        for _ in range(5):
            sx, sy = q[0] + r.uniform(-260, 260), q[1] + r.uniform(-120, 160)
            d.ellipse((sx - 5, sy - 5, sx + 5, sy + 5), fill=(250, 240, 200))
    return img, dict(grain=9, tint=((255, 0, 30), 0.12 * seg(t, D * 0.5, D)))

def final(t, D, fi):
    """la pantalla de la caja: la fecha salta de 2026 a 1986. Tarjeta REGLA 4."""
    salta = t > D * 0.12 or (fi // 2) % 3 == 0
    fecha = ANTES if salta else HOY
    col = (255, 90, 70) if salta else (110, 240, 170)
    esc = _base(t, fecha=fecha, cajon=1.0, pesetas=36, fecha_col=col)
    k = ease(t / D)
    cam = Camara(ojo=(1.6, lerp(1.9, 1.85, k), lerp(-3.4, -3.15, k)), mira=(1.9, 1.72, -1.9), fov=lerp(45, 40, k))
    img = esc.render(cam, luces_base(0.85))
    img = etiquetas(img, esc, cam)
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.15, 0.5))
    d.rectangle((0, 360, W, 900), fill=(0, 0, 0))
    d.text((W / 2, 470), f"{tr('REGLA')} 4", font=font(int(150 * p) + 1), fill=(230, 40, 40), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    regla = tr("NO ACEPTES MONEDAS ANTIGUAS")
    fs = 70
    while d.textlength(regla, font=font(fs)) > W - 120 and fs > 30: fs -= 2
    d.text((W / 2, 640), regla, font=font(fs), fill=(240, 240, 230), anchor="mm")
    q = ease_back(seg(t, D * 0.55, D * 0.75))
    if q > 0:
        d.rounded_rectangle((200, 760, 880, 860), 24, fill=(200, 30, 30))
        d.text((W / 2, 810), tr("MAÑANA: REGLA 5"), font=font(int(56 * q) + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=9, glitch=0.25 if fi % 11 < 2 else 0.0)

ESCENA_FN = dict(llegada=llegada, lista=lista, anciano=anciano_, monedas=monedas_, niego=niego, camara=camara, giro=giro, final=final)
PAUSA = dict(llegada=0.4, lista=0.9, anciano=0.5, monedas=0.7, niego=0.7, camara=0.7, giro=0.8, final=1.8)
