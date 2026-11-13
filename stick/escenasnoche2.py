"""TURNO DE NOCHE 2 — "Si suena el teléfono de la cabina a las 3:00, no lo cojas" (escenas 3D con turno3d)."""
import math, os, random
from PIL import ImageDraw, ImageFilter
from motor import *
from motor3d import *
from turno3d import *

G = __import__("guionnoche2" + ("_en" if IDIOMA == "en" else ""))
TELF = (0.2, -1.9)                      # teléfono de la tienda, sobre el mostrador
OREJA = pose(a2u=150, a2l=140, head=-4)  # brazo derecho con el auricular en la oreja

def hora(s0):
    s = 3 * 3600 + int(s0)
    return f"{s // 3600:02d}:{s // 60 % 60:02d}:{s % 60:02d}"

def _fondo_mostrador(t, luz=1.0):
    esc = mundo(t, luz)
    cam = cam_mostrador(t, mira=(0.6, 0.6, -1.5), fov=50)
    return esc.render(cam, luces_base(luz)).filter(ImageFilter.GaussianBlur(10))

def llegada(t, D, fi):
    k = ease(min(1, t / D))
    esc = mundo(t, cabina_kw=dict(luz=0.8))
    coche(esc, -9.5, 4.0, yaw=1.4, col=(70, 30, 30))                       # tu coche
    cam = Camara(ojo=(lerp(-1, -3, k), lerp(1.8, 1.6, k), lerp(26, 17, k)), mira=(lerp(-4, -1, k), 1.8, lerp(8, 0, k)), fov=58)
    img = etiquetas(esc.render(cam, luces_base(extra=[luz_cabina(0.8)])), esc, cam)
    return img, dict(grain=8)

def lista(t, D, fi):
    img = _fondo_mostrador(t)
    z = lerp(0.95, 1.06, ease(t / D))
    hoja_reglas(img, t, G.REGLAS, resalta=1 if t > D * 0.15 else None, zoom=z)
    return img, dict(grain=6)

def suena(t, D, fi):
    """desde el mostrador: la cabina, fuera, suena en la niebla. Su luz parpadea."""
    ring = (t % 1.2) < 0.7 and t < D * 0.8
    vib = 0.025 * math.sin(t * 90) if ring else 0.0
    parp = 1.0 if (fi // 3) % 7 else 0.35
    esc = mundo(t, cabina_kw=dict(luz=parp, vibra=vib))
    k = ease(seg(t, 0, D * 0.75))
    j = 0.006 * math.sin(t * 61) if ring else 0.0
    cam = Camara(ojo=(lerp(1.2, 0.4, k) + j, 1.62 + j, lerp(-2.4, -1.0, k)), mira=(lerp(-2.5, CABINA[0], k), lerp(1.3, 1.25, k), lerp(4, CABINA[1], k)), fov=lerp(55, 24, k))
    img = esc.render(cam, luces_base(extra=[luz_cabina(parp)]))
    d = ImageDraw.Draw(img)
    # reloj digital de la pared (arriba): 03:00
    d.rounded_rectangle((W / 2 - 170, 300, W / 2 + 170, 410), 14, fill=(12, 12, 12), outline=(60, 60, 60), width=4)
    d.text((W / 2, 355), "03:00", font=font(84), fill=(240, 50, 40), anchor="mm")
    return img, dict(grain=9)

def tienda(t, D, fi):
    """el teléfono de la tienda suena; en su pantalla: CABINA"""
    ring = (t % 1.0) < 0.6
    vib = 0.012 * math.sin(t * 80) if ring else 0.0
    esc = mundo(t, cabina_kw=dict(luz=1.0))
    telefono(esc, *TELF, pantalla=(120, 230, 160), vibra=vib)
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(lerp(1.6, 1.2, k), lerp(1.85, 1.7, k), lerp(-3.4, -3.0, k)), mira=(TELF[0] - 0.2, 1.1, TELF[1] + 0.3), fov=lerp(55, 46, k))
    img = esc.render(cam, luces_base(extra=[Luz((0.6, 2.0, -2.2), FLUOR, 3, fuerza=0.6)]))
    # la pantallita, ampliada para que se lea
    q = proyectar(cam, (TELF[0], 1.21, TELF[1] - 0.075))
    if q:
        d = ImageDraw.Draw(img)
        a = ease_back(seg(t, D * 0.45, D * 0.6))
        if a > 0:
            cx, cy = q[0], q[1] - 330
            w2, h2 = 330 * a, 105 * a
            d.line((q[0], q[1], cx, cy + h2), fill=(120, 230, 160), width=5)
            d.rectangle((cx - w2, cy - h2, cx + w2, cy + h2), fill=(20, 50, 34), outline=(120, 230, 160), width=6)
            d.text((cx, cy - 38 * a), tr("LLAMADA ENTRANTE"), font=font(int(40 * a) + 1), fill=(150, 240, 180), anchor="mm")
            d.text((cx, cy + 30 * a), tr("CABINA KM 9"), font=font(int(70 * a) + 1), fill=(200, 255, 210), anchor="mm")
    return img, dict(grain=7)

def voz(t, D, fi):
    """con el auricular en la oreja, giras despacio la cabeza hacia lo que tienes detrás: las estanterías"""
    esc = mundo(t, cabina_kw=dict(luz=1.0))
    telefono(esc, *TELF, pantalla=(120, 230, 160))
    k = ease(seg(t, D * 0.35, D))
    ang = lerp(0.3, 1.95, k)                            # de mirar a la puerta a mirar atrás (el fondo de la tienda)
    ojo = (1.0, 1.62, -2.5)
    mira = (ojo[0] - 4 * math.sin(ang), 1.35, ojo[2] + 4 * math.cos(ang))
    cam = Camara(ojo=ojo, mira=mira, fov=58, roll=0.04 * math.sin(t * 1.3))
    luz = 0.55 if (fi // 2) % 11 == 0 and t > D * 0.5 else 1.0          # el fluorescente tiembla
    img = esc.render(cam, luces_base(luz))
    return img, dict(grain=10, tint=((255, 0, 30), 0.18 * seg(t, D * 0.4, D)))

def camara(t, D, fi):
    """CAM 1: tú, al teléfono detrás del mostrador. Detrás de ti no hay nadie."""
    esc = mundo(t, cabina_kw=dict(luz=1.0))
    telefono(esc, *TELF, pantalla=(120, 230, 160))
    empleado(esc, OREJA, 0.5, -2.65, yaw=0.15, cara="ninguna")
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(4.6, 2.85, -0.4), mira=(lerp(0.0, 0.3, k), lerp(0.9, 1.2, k), lerp(-3.4, -3.6, k)), fov=lerp(58, 40, k))
    img = cctv(esc.render(cam, luces_base()), 1, hora(95 + t))
    return img, dict(grain=12, glitch=0.2 if fi % 23 < 2 else 0.0)

def giro(t, D, fi):
    """CAM 3: en la cabina hay alguien con tu uniforme, al teléfono, mirando hacia la tienda"""
    esc = mundo(t, cabina_kw=dict(luz=1.0, colgado=None))
    gira = ease(seg(t, D * 0.55, D * 0.8))
    cab = empleado(esc, add(OREJA, pose(head=-10 * gira)), CABINA[0] + 0.05, CABINA[1] + 0.05, yaw=lerp(2.56, 2.09, gira), cara="ninguna")
    esc.add(caja(0.09, 0.28, 0.1, (10, 10, 10)), cadena(cab, mover(0.17, 0.0, 0.0), rot_z(0.2)))   # el auricular, en su oreja
    k = ease(seg(t, 0, D * 0.85))
    base = cam_cabina(cctv=True)
    cam = Camara(ojo=base.ojo, mira=(CABINA[0], lerp(0.9, 1.3, k), CABINA[1]), fov=lerp(70, 36, k))
    img = esc.render(cam, luces_base(extra=[luz_cabina(1.2)]))
    img = cctv(img, 3, hora(101 + t))
    return img, dict(grain=12, glitch=0.35 if fi % 19 < 2 else 0.0)

def final(t, D, fi):
    """la cabina, vacía, con el auricular colgando del cable; tarjeta REGLA 2"""
    parp = 1.0 if (fi // 3) % 6 else 0.3
    esc = mundo(t, cabina_kw=dict(luz=parp, colgado=False))
    cam = Camara(ojo=(-4.5, 1.6, 6.0), mira=(CABINA[0], 1.0, CABINA[1]), fov=lerp(42, 32, ease(t / D)))
    img = esc.render(cam, luces_base(extra=[luz_cabina(parp)]))
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.15, 0.5))
    d.rectangle((0, 360, W, 900), fill=(0, 0, 0))
    d.text((W / 2, 470), f"{tr('REGLA')} 2", font=font(int(150 * p) + 1), fill=(230, 40, 40), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    regla = tr("NO COJAS LA CABINA A LAS 3:00")
    fs = 70
    while d.textlength(regla, font=font(fs)) > W - 120 and fs > 30: fs -= 2
    d.text((W / 2, 640), regla, font=font(fs), fill=(240, 240, 230), anchor="mm")
    q = ease_back(seg(t, D * 0.55, D * 0.75))
    if q > 0:
        d.rounded_rectangle((200, 760, 880, 860), 24, fill=(200, 30, 30))
        d.text((W / 2, 810), tr("MAÑANA: REGLA 3"), font=font(int(56 * q) + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=9)

ESCENA_FN = dict(llegada=llegada, lista=lista, suena=suena, tienda=tienda, voz=voz, camara=camara, giro=giro, final=final)
PAUSA = dict(llegada=0.4, lista=0.9, suena=0.8, tienda=0.5, voz=0.6, camara=0.7, giro=0.9, final=1.8)
