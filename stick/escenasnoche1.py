"""TURNO DE NOCHE 1 — "No existe el surtidor 4" (escenas 3D con turno3d)."""
import math, os
from PIL import ImageDraw, ImageFilter
from motor import *
from motor3d import *
from turno3d import *

G = __import__("guionnoche1" + ("_en" if IDIOMA == "en" else ""))
NOTA = "Yo le dije que sí. — Raúl"
HORA0 = (3, 17, 0)

def hora(seg_extra):
    s = HORA0[0] * 3600 + HORA0[1] * 60 + HORA0[2] + int(seg_extra)
    return f"{s // 3600:02d}:{s // 60 % 60:02d}:{s % 60:02d}"

def _fondo_mostrador(t, luz=1.0):
    esc = mundo(t, luz)
    cam = cam_mostrador(t, mira=(0.6, 0.6, -1.5), fov=50)
    return esc.render(cam, luces_base(luz)).filter(ImageFilter.GaussianBlur(10))

def llegada(t, D, fi):
    k = ease(min(1, t / D))
    esc = mundo(t)
    coche(esc, -9.5, 4.0, yaw=1.4, col=(70, 30, 30))                       # tu coche, aparcado a un lado
    cam = Camara(ojo=(lerp(-6, -3, k), lerp(1.7, 1.6, k), lerp(27, 17, k)), mira=(lerp(1, 0, k), 2.0, 0), fov=58)
    img = etiquetas(esc.render(cam, luces_base()), esc, cam)
    return img, dict(grain=8)

def lista(t, D, fi):
    img = _fondo_mostrador(t)
    z = lerp(0.95, 1.05, ease(t / D))
    hoja_reglas(img, t, G.REGLAS, resalta=0 if t > D * 0.25 else None, zoom=z)
    return img, dict(grain=6)

def entra(t, D, fi):
    esc = mundo(t)
    a = ease(seg(t, 0, D * 0.55))
    x, z = lerp(-3.0, 0.2, a), lerp(1.2, -0.95, a)
    yaw = math.atan2(1.4 - x, -2.7 - z) if a < 1 else math.atan2(1.4 - 0.2, -2.7 + 0.95)
    p = walk(t, 0.55, 0.55) if a < 1 else add(STAND, pose(head=-6 + 4 * math.sin(t)))
    cliente(esc, p, x, z, yaw=yaw, alto=1.05, cara="neutral")
    cam = cam_mostrador(t, mira=(lerp(-2.4, 0.3, a), 1.45, lerp(0.5, -1.1, a)), fov=lerp(55, 48, a))
    img = esc.render(cam, luces_base())
    # gotas que caen del chubasquero
    d = ImageDraw.Draw(img); r = random.Random(fi // 2)
    q = proyectar(cam, (x, 0.9, z))
    if q:
        for _ in range(6): gx = q[0] + r.uniform(-90, 90); gy = q[1] + r.uniform(0, 500); d.line((gx, gy, gx, gy + 26), fill=(150, 170, 180), width=4)
    return img, dict(grain=8)

def ventana(t, D, fi):
    ap = ease(seg(t, D * 0.4, D * 0.85))
    esc = mundo(t, surtidor4=ap, coche4=ap)
    cliente(esc, STAND, 0.2, -0.95, yaw=math.pi + 0.4, alto=1.05)
    k = ease(seg(t, 0, D * 0.7))
    cam = Camara(ojo=(0.6, 1.62, -1.2), mira=(lerp(-1.5, S4[0], k), lerp(1.4, 1.25, k), lerp(6.5, S4[1], k)), fov=lerp(55, 36, ease(seg(t, D * 0.5, D))))
    img = etiquetas(esc.render(cam, luces_base(extra=[Luz((S4[0] - 0.8, 2.6, S4[1] + 1.5), (210, 230, 220), 6, fuerza=1.7 * ap)])), esc, cam)
    return img, dict(grain=9, tint=((255, 0, 30), 0.12 * ap))

def niego(t, D, fi):
    gira = ease(seg(t, D * 0.55, D * 0.8)); va = ease(seg(t, D * 0.75, D))
    esc = mundo(t, surtidor4=1, coche4=1)
    x, z = lerp(0.2, -2.2, va), lerp(-0.95, 0.6, va)
    p = STAND if va <= 0 else walk(t, 0.55, 0.55)
    cliente(esc, p, x, z, yaw=lerp(math.atan2(1.2, -1.75), math.atan2(-2.4, 1.55) + 0.3, gira), alto=1.05, cara="neutral")
    cam = cam_mostrador(t, mira=(lerp(0.25, -1.0, va), lerp(1.75, 1.5, va), lerp(-1.0, 0.0, va)), fov=lerp(32, 50, va), temblor=0.004)
    img = esc.render(cam, luces_base())
    return img, dict(grain=8)

def camara(t, D, fi):
    esc = mundo(t, surtidor4=1, coche4=1)
    sal = ease(seg(t, 0, D))
    cliente(esc, walk(t, 0.5, 0.5), lerp(1.5, S4[0] - 1.0, sal), lerp(3.0, S4[1] + 0.8, sal), yaw=math.atan2(S4[0] - 2.5, S4[1] - 2.2), alto=1.05)
    # alguien con tu uniforme, junto al surtidor 4, saludando a la cámara
    sal_b = math.sin(t * 7)
    empleado(esc, pose(a2u=150 + 25 * sal_b, a2l=20, head=-8), S4[0] + 0.3, S4[1] - 1.3, yaw=-2.2, cara="ninguna")
    cam = cam_cctv(2); k = ease(seg(t, D * 0.3, D))
    cam = Camara(ojo=cam.ojo, mira=(lerp(6.5, S4[0], k), lerp(0.8, 1.1, k), lerp(7.2, S4[1] - 0.6, k)), fov=lerp(60, 30, k))
    img = esc.render(cam, luces_base(extra=[Luz((S4[0] - 1.5, 2.6, S4[1] - 1.0), (210, 230, 220), 6, fuerza=1.7)]))
    img = cctv(etiquetas(img, esc, cam), 2, hora(120 + t))
    return img, dict(grain=12, glitch=0.25 if fi % 17 < 2 else 0.0)

def nota(t, D, fi):
    img = _fondo_mostrador(t, luz=0.85)
    z = lerp(1.0, 1.25, ease(t / D))
    hoja_reglas(img, t, G.REGLAS, resalta=0, nota=NOTA, nota_p=seg(t, D * 0.15, D * 0.65), zoom=z, cy=lerp(860, 640, ease(t / D)))
    return img, dict(grain=7, tint=((255, 0, 30), 0.15 * seg(t, D * 0.7, D)))

def final(t, D, fi):
    faros = 2.0 if t > D * 0.3 else 0.0
    esc = mundo(t, surtidor4=1, coche4=faros or 1)
    cam = Camara(ojo=(1.5, 1.6, 4.5), mira=(S4[0] + 1.0, 1.0, S4[1] + 0.8), fov=lerp(50, 40, ease(t / D)))
    luces = luces_base(extra=[Luz((S4[0] + 0.6, 0.8, S4[1] + 1.0), (255, 250, 220), 14, dir=(-1, 0, -0.3), cono=35, fuerza=1.8)] if faros else [])
    img = esc.render(cam, luces)
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.15, 0.5))
    d.rectangle((0, 360, W, 900), fill=(0, 0, 0))
    d.text((W / 2, 470), f"{tr('REGLA')} 1", font=font(int(150 * p) + 1), fill=(230, 40, 40), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    regla = tr("NO EXISTE EL SURTIDOR 4")
    fs = 70
    while d.textlength(regla, font=font(fs)) > W - 120 and fs > 30: fs -= 2
    d.text((W / 2, 640), regla, font=font(fs), fill=(240, 240, 230), anchor="mm")
    q = ease_back(seg(t, D * 0.55, D * 0.75))
    if q > 0:
        d.rounded_rectangle((200, 760, 880, 860), 24, fill=(200, 30, 30))
        d.text((W / 2, 810), tr("MAÑANA: REGLA 2"), font=font(int(56 * q) + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=9, flash=((255, 255, 240), 0.5 * max(0, 1 - (t - D * 0.3) / 0.3)) if faros else None)

import random
ESCENA_FN = dict(llegada=llegada, lista=lista, entra=entra, ventana=ventana, niego=niego, camara=camara, nota=nota, final=final)
PAUSA = dict(llegada=0.3, lista=0.4, entra=0.4, ventana=0.5, niego=0.3, camara=0.6, nota=0.5, final=1.6)
