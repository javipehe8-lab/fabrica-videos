"""TURNO DE NOCHE 10 — "Las cámaras van 10 segundos por detrás. Si alguna va por delante, sal por la puerta de atrás" (escenas 3D)."""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter
from motor import *
from motor3d import *
from turno3d import *
from turno3d import _envolver

G = __import__("guionnoche10" + ("_en" if IDIOMA == "en" else ""))
YO = (1.4, -2.6)                          # mi sitio, detrás del mostrador (mirando hacia la tienda, +z)
DETRAS = (1.4, -3.08)                     # donde se para la figura de niebla: justo detrás de mí
CAM1 = Camara(ojo=(4.6, 2.85, -0.4), mira=(0.4, 0.9, -3.0), fov=52)         # CAM 1 (esquina alta, delante)
MANOS = pose(a1u=78, a1l=24, a2u=78, a2l=24, head=8, body=4)                # las manos en mis hombros

def _hora(seg0, t, adelanto=10):
    s = seg0 + int(t) + adelanto
    return f"04:{10 + s // 60:02d}:{s % 60:02d}"

def _tienda_cam(t, fig=None, fig_p=MANOS, me=True, niebla_k=0.0, cam=CAM1, fig_brillo=1.0, me_p=None):
    """la tienda tal como la enseña la CAM 1 (diez segundos por delante): yo detrás del mostrador y, si fig, la figura de niebla"""
    esc = mundo(t)
    puerta_atras(esc)
    luces = luces_base()
    if me:
        empleado(esc, me_p or pose(head=4, a1u=8, a2u=-8), YO[0], YO[1], yaw=0.25, cara="ninguna")
    if fig:
        figura_niebla(esc, fig_p, fig[0], fig[1], yaw=fig[2], brillo=fig_brillo)
        luces = luces + [luz_figura(fig[0], fig[1], fig[2], 0.8)]
    if niebla_k > 0:
        img = render_niebla(esc, cam, luces, niebla_k, t=t, alfa=0.7)
    else:
        img = esc.render(cam, luces)
    return aclarar(img, 1.25, 0.86)

# ---------- 1. arranque: CAM 1, de cerca: la niebla, detrás de mí, con las manos en mis hombros ----------
def arranque(t, D, fi):
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(3.7, 2.55, lerp(-0.9, -1.2, k)), mira=(1.3, 1.62, -2.85), fov=lerp(38, 33, k))
    img = _tienda_cam(t, fig=(DETRAS[0] - 0.05, DETRAS[1], 0.25), cam=cam, fig_brillo=1.05)
    d = ImageDraw.Draw(img)                       # rótulo de cámara abajo (en color: mi uniforme rojo contra la niebla gris)
    d.text((70, 690), "CAM 1", font=font(60), fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
    d.text((W - 70, 690), _hora(2, t), font=font(56), fill=(255, 255, 255), anchor="ra", stroke_width=4, stroke_fill=(0, 0, 0))
    d.ellipse((290, 707, 326, 743), fill=(230, 30, 30))
    rot = lambda im: rotulo_regla(im, 10, G.REGLA_CORTA, p=1.0, y=470)
    return img, dict(grain=10, glitch=0.25 if fi % 19 < 2 else 0.0, overlay=rot, tint=((255, 0, 30), 0.06))

# ---------- 2. premisa: la hoja de reglas, con la regla 10 y la nota de Raúl ----------
def premisa(t, D, fi):
    esc = mundo(t)
    cam = cam_mostrador(t, mira=(0.6, 0.6, -1.5), fov=50)
    img = esc.render(cam, luces_base()).filter(ImageFilter.GaussianBlur(10))
    z = lerp(0.54, 0.58, ease(t / D))
    hoja_reglas(img, t, G.REGLAS, resalta=9, nota=G.NOTA, nota_p=seg(t, D * 0.35, D * 0.8), zoom=z, cy=880, h_extra=980)
    return aclarar(img, 1.1, 0.92), dict(grain=7)

def _fondo_mostrador(t, mira=(2.6, 1.0, -1.4), fov=55):
    """lo que hay detrás del monitor: el mostrador, desenfocado"""
    esc = mundo(t)
    img = esc.render(cam_mostrador(t, mira=mira, fov=fov), luces_base())
    return aclarar(img.filter(ImageFilter.GaussianBlur(9)), 1.05, 0.95)

# ---------- 3. reloj: el monitor de la CAM 1 marca 04:10:22; la caja, 04:10:12 ----------
def reloj(t, D, fi):
    pant = cctv(_tienda_cam(t, cam=Camara(ojo=(4.1, 2.7, -0.7), mira=(1.2, 1.15, -2.9), fov=44)), 1, _hora(12, t))
    k = ease(seg(t, 0, D))
    img = monitor(_fondo_mostrador(t), pant, t, lcd=_hora(12, t, 0))
    z = 1 + 0.06 * k
    w_, h_ = int(W / z), int(H / z)
    img = img.crop(((W - w_) // 2, int((H - h_) * 0.45), (W - w_) // 2 + w_, int((H - h_) * 0.45) + h_)).resize((W, H))
    return img, dict(grain=8, glitch=0.2 if fi % 23 < 2 else 0.0)

# ---------- 4. entra: en la pantalla, la niebla entra por la puerta; aquí, la puerta sigue cerrada ----------
def entra(t, D, fi):
    corte = D * 0.58
    if t < corte:
        k = seg(t, 0, corte)
        fx, fz = lerp(-3.0, -1.6, k), lerp(0.4, -1.0, k)
        p = pose(l1u=20 * math.sin(t * 5), l2u=-20 * math.sin(t * 5), a1u=10, a2u=-10)
        pant = _tienda_cam(t, fig=(fx, fz, math.atan2(YO[0] - fx, YO[1] - fz)), fig_p=p, niebla_k=0.35 + 0.4 * k, cam=cam_puerta_cctv())
        pant = cctv(pant, 1, _hora(26, t))
        return monitor(_fondo_mostrador(t), pant, t), dict(grain=9)
    # la puerta de verdad: cerrada, con la niebla quieta al otro lado del cristal
    esc = mundo(t)
    k = ease(seg(t, corte, D))
    cam = cam_mostrador(t, mira=(-3.0, 1.2, 0.0), fov=lerp(42, 32, k), temblor=0.015)
    img = esc.render(cam, luces_base(extra=[Luz((-2.6, 1.8, -1.2), FLUOR, 3.5, fuerza=0.8)]))
    fl = max(0.0, 0.45 - (t - corte) / 0.3)
    return aclarar(img, 1.4, 0.8), dict(grain=8, flash=((255, 255, 255), fl))

# ---------- 5. detras: en la pantalla, se para detrás de mí y me pone las manos encima ----------
def detras(t, D, fi):
    k = ease(seg(t, 0, D * 0.6))
    fx, fz = lerp(0.2, DETRAS[0], k), lerp(-2.9, DETRAS[1], k)
    p = pose(a1u=lerp(10, 78, k), a1l=lerp(12, 24, k), a2u=lerp(-10, 78, k), a2l=lerp(12, 24, k), head=8 * k, body=4 * k)
    cam = Camara(ojo=(4.1, 2.7, -0.7), mira=(1.2, 1.15, -2.9), fov=40)
    pant = cctv(_tienda_cam(t, fig=(fx, fz, lerp(1.2, 0.25, k)), fig_p=p, cam=cam, fig_brillo=0.8), 1, _hora(30, t))
    img = monitor(_fondo_mostrador(t), pant, t)
    z = 1 + 0.16 * ease(seg(t, D * 0.3, D))
    w_, h_ = int(W / z), int(H / z)
    img = img.crop(((W - w_) // 2, int((H - h_) * 0.45), (W - w_) // 2 + w_, int((H - h_) * 0.45) + h_)).resize((W, H))
    return img, dict(grain=9, tint=((255, 0, 30), 0.08 * k), glitch=0.3 if abs(t - D * 0.6) < 0.1 else 0.0)

# ---------- 6. nuca: plano real, por encima de mi hombro: no hay nadie, pero sale vaho junto a mi cuello ----------
def nuca(t, D, fi):
    esc = mundo(t)
    puerta_atras(esc)
    empleado(esc, pose(head=6, a1u=6, a2u=-6), YO[0], YO[1], yaw=0.25, cara="ninguna")
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(lerp(2.35, 2.2, k), 2.0, lerp(-4.3, -4.0, k)), mira=(0.4, 1.2, -0.6), fov=lerp(56, 48, k),
                 roll=0.02 * math.sin(t * 2.0))
    img = esc.render(cam, luces_base(extra=[Luz((1.8, 1.9, -3.4), (170, 190, 200), 1.6, fuerza=0.6)]))
    img = aclarar(img, 1.25, 0.86)
    img = vapor(img, 380, 1000, 300, t, n=7, alfa=int(110 + 80 * k), alto=380)
    return img, dict(grain=9, tint=((40, 90, 255), 0.10))

# ---------- 7. huyo: corro a la puerta de atrás; en la pantalla me quedo, y la niebla me lleva ----------
def huyo(t, D, fi):
    corte = D * 0.45
    if t < corte:
        k = ease(seg(t, 0, corte))
        esc = mundo(t)
        puerta_atras(esc, abierta=ease(seg(t, corte * 0.35, corte)))
        bob = 0.05 * math.sin(t * 14)
        cam = Camara(ojo=(lerp(1.2, 0.4, k), 1.6 + bob, lerp(-3.0, -4.7, k)), mira=(PUERTA_A[0], 1.1, PUERTA_A[1]), fov=58,
                     roll=0.03 * math.sin(t * 7))
        img = esc.render(cam, luces_base())
        return aclarar(img, 1.25, 0.86), dict(grain=9, glitch=0.15 if fi % 9 < 1 else 0.0)
    k = ease(seg(t, corte, D))
    cam = Camara(ojo=(4.1, 2.7, -0.7), mira=(1.2, 1.15, -2.9), fov=40)
    esc_k = 0.2 + 0.8 * k
    abr = pose(a1u=lerp(78, 60, k), a1l=lerp(24, 80, k), a2u=lerp(78, 60, k), a2l=lerp(24, 80, k), head=8, body=lerp(4, 14, k))
    pant = _tienda_cam(t, fig=(DETRAS[0], lerp(DETRAS[1], -2.85, k), 0.25), fig_p=abr, cam=cam, fig_brillo=0.9,
                       niebla_k=esc_k, me_p=pose(head=lerp(4, 30, k), a1u=8, a2u=-8, body=lerp(0, -10, k)))
    pant = cctv(pant, 1, _hora(40, t))
    fl = max(0.0, 0.5 - (t - corte) / 0.3)
    return monitor(_fondo_mostrador(t), pant, t), dict(grain=10, flash=((255, 255, 255), fl), tint=((255, 0, 30), 0.12 * k))

# ---------- 8. final: detrás de la gasolinera, en la niebla: un cartel que no estaba. KILÓMETRO 10 ----------
def final(t, D, fi):
    esc = Escena(niebla=((70, 78, 78), 3.0, 22.0), amb=0.2)
    esc.etiquetas = []
    trasera(esc)
    sp = cartel_km(esc, -0.4, -13.5, "KILÓMETRO 10")
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(0.5, 1.6, lerp(-6.9, -7.6, k)), mira=(-0.3, 2.3, -13.5), fov=lerp(46, 40, k), roll=0.01 * math.sin(t))
    img = esc.render(cam, luz_trasera() + [Luz((-0.4, 3.2, -12.0), (180, 196, 196), 4.0, fuerza=0.7)])
    etiquetas(img, esc, cam)
    img = aclarar(img, 1.2, 0.88)
    img = vapor(img, W / 2, 1500, 900, t, n=9, alfa=55, alto=700)
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.15, 0.5))
    d.rectangle((0, 200, W, 680), fill=(0, 0, 0))
    d.text((W / 2, 295), f"{tr('REGLA')} 10", font=font(int(150 * p) + 1), fill=(230, 40, 40), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    regla = tr("SI UNA CÁMARA VA POR DELANTE, SAL POR LA PUERTA DE ATRÁS")
    fnt = font(56)
    for i, ln in enumerate(_envolver(d, regla, fnt, W - 120)[:2]):
        d.text((W / 2, 420 + i * 66), ln, font=fnt, fill=(240, 240, 230), anchor="mm")
    q = ease_back(seg(t, D * 0.55, D * 0.75))
    if q > 0:
        d.rounded_rectangle((190, 555, 890, 645), 24, fill=(200, 30, 30))
        d.text((W / 2, 600), tr("MAÑANA: REGLA 11"), font=font(int(56 * q) + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=9, glitch=0.2 if fi % 13 < 2 else 0.0)

ESCENA_FN = dict(arranque=arranque, premisa=premisa, reloj=reloj, entra=entra, detras=detras, nuca=nuca, huyo=huyo, final=final)
PAUSA = dict(arranque=0.4, premisa=0.4, reloj=0.5, entra=0.6, detras=0.6, nuca=0.8, huyo=0.7, final=1.8)
