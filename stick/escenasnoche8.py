"""TURNO DE NOCHE 8 — "Si el camión llega antes de las 6, no firmes nada" (escenas 3D con turno3d)."""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter
from motor import *
from motor3d import *
from turno3d import *

G = __import__("guionnoche8" + ("_en" if IDIOMA == "en" else ""))
PUERTA = (-2.9, -0.3)                    # entrada de la tienda
MOST = (1.15, -1.3)                      # el anciano, frente a ti, al otro lado del mostrador
CAMION = (-1.5, 8.6)                      # el camión, aparcado de cara a la tienda, con los faros encendidos
CAJA = (1.0, 1.12, -1.92)                # la caja, sobre el mostrador

def _yaw_a_mi(x, z):
    return math.atan2(1.4 - x, -2.7 - z)

def _camion(esc, z=CAMION[1], faros=1.0):
    M = camion(esc, CAMION[0], z, yaw=math.pi, faros=faros)
    return [tuple((M @ np.array([sx * 0.82, 0.95, 3.62, 1.0]))[:3]) for sx in (-1, 1)]

def _luces_camion(faros_, f=1.0):
    return [Luz((fx, 1.2, fz - 1.2), (255, 246, 210), 9.0, fuerza=0.9 * f) for fx, fy, fz in faros_[:1]]

def _destellos(img, cam, faros_, f=1.0, blur=10):
    """los faros del camión atravesando la niebla (halos 2D)"""
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
    for p_ in faros_:
        q = proyectar(cam, p_)
        if q:
            for r, al in ((150, 45), (75, 100), (28, 255)):
                r_ = r * min(2.0, 9.0 / max(q[2], 1.0))
                dc.ellipse((q[0] - r_, q[1] - r_ * 0.7, q[0] + r_, q[1] + r_ * 0.7), fill=(255, 246, 210, int(al * f)))
    capa = capa.filter(ImageFilter.GaussianBlur(blur))
    img.paste(capa, (0, 0), capa)
    return img

def _anciano_ofrece(esc, t, ofrece=1.0, cara="neutral", albaran_=True):
    """el anciano, al otro lado del mostrador, tendiéndote el albarán"""
    x, z = MOST
    yaw = _yaw_a_mi(x, z)
    p = add(STAND, pose(a2u=lerp(20, 78, ofrece), a2l=lerp(30, 12, ofrece), head=-8))
    anciano(esc, p, x, z, yaw=yaw, cara=cara)
    if albaran_:
        # la mano derecha queda delante, a la altura del pecho: el albarán sale de ahí hacia ti
        fx, fz = math.sin(yaw), math.cos(yaw)
        hx, hz = x + fx * 0.6 * ofrece + fz * 0.03, z + fz * 0.6 * ofrece - fx * 0.03
        albaran3d(esc, hx, lerp(0.95, 1.16, ofrece), hz, yaw=yaw, inclina=-1.25)

def _fondo(t, blur=12):
    esc = mundo(t)
    faros_ = _camion(esc)
    _anciano_ofrece(esc, t, ofrece=1.0, albaran_=False)
    cam = cam_mostrador(t, mira=(1.1, 1.3, -1.0), fov=50)
    img = esc.render(cam, luces_base(extra=_luces_camion(faros_)))
    img = _destellos(img, cam, faros_)
    return img.filter(ImageFilter.GaussianBlur(blur))

# ---------- 1. arranque: el anciano de las pesetas, a un palmo, tendiéndote el albarán ----------
def arranque(t, D, fi):
    esc = mundo(t)
    faros_ = _camion(esc)
    _anciano_ofrece(esc, t, ofrece=1.0)
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(1.4, 1.58, -2.66), mira=(lerp(1.2, 1.15, k), 1.5, -1.3), fov=lerp(44, 39, k), roll=0.012 * math.sin(t * 1.2))
    img = esc.render(cam, luces_base(extra=_luces_camion(faros_) + [Luz((1.3, 2.2, -2.0), FLUOR, 3.0, fuerza=0.7)]))
    img = _destellos(img, cam, faros_)
    img = aclarar(img, 1.25, 0.85)
    rot = lambda im: rotulo_regla(im, 8, G.REGLA_CORTA, p=1.0, y=430)
    return img, dict(grain=8, glitch=0.2 if fi % 19 < 2 else 0.0, overlay=rot, tint=((255, 0, 30), 0.08))

# ---------- 2. premisa: la hoja de reglas, con la regla 8 y la nota de Raúl ----------
def premisa(t, D, fi):
    esc = mundo(t)
    cam = cam_mostrador(t, mira=(0.6, 0.6, -1.5), fov=50)
    img = esc.render(cam, luces_base()).filter(ImageFilter.GaussianBlur(10))
    z = lerp(0.66, 0.71, ease(t / D))
    hoja_reglas(img, t, G.REGLAS, resalta=7, nota=G.NOTA, nota_p=seg(t, D * 0.35, D * 0.8), zoom=z, cy=850, h_extra=720)
    return aclarar(img, 1.1, 0.92), dict(grain=7)

# ---------- 3. llega: CAM 2, el camión viene derecho desde la carretera; luego el anciano entra ----------
def llega(t, D, fi):
    corte = D * 0.55
    if t < corte:
        a = ease_out(seg(t, 0, corte * 0.9))
        esc = mundo(t)
        faros_ = _camion(esc, z=lerp(20.0, CAMION[1], a))
        cam = Camara(ojo=(4.6, 4.2, 2.4), mira=(-1.5, 1.2, lerp(14, 8.5, a)), fov=58)
        img = esc.render(cam, luces_base(extra=_luces_camion(faros_)))
        img = _destellos(img, cam, faros_, blur=8)
        s = 59 * 60 + 56 + int(t * 1.6)
        h = "04" if s < 3600 else "05"; s %= 3600
        img = cctv(etiquetas(img, esc, cam), 2, f"{h}:{s // 60:02d}:{s % 60:02d}")
        return img, dict(grain=12, glitch=0.3 if t < 0.12 or fi % 17 < 2 else 0.0)
    a = ease(seg(t, corte, D))
    esc = mundo(t)
    faros_ = _camion(esc)
    x, z = lerp(PUERTA[0], MOST[0] - 0.4, a), lerp(PUERTA[1] + 0.2, MOST[1], a)
    anciano(esc, walk(t, 0.35, 0.45), x, z, yaw=_yaw_a_mi(x, z))
    cam = Camara(ojo=(1.4, 1.7, -2.75), mira=(lerp(-2.4, 0.6, a), 1.25, lerp(0.6, -1.1, a)), fov=lerp(52, 44, a))
    img = esc.render(cam, luces_base(extra=_luces_camion(faros_)))
    img = _destellos(img, cam, faros_)
    fl = max(0.0, 0.5 - (t - corte) / 0.3)
    return aclarar(img, 1.12, 0.9), dict(grain=8, flash=((255, 255, 255), fl))

# ---------- 4. albaran: el albarán, ya firmado con tu letra, con fecha de mañana ----------
def albaran_(t, D, fi):
    img = _fondo(t)
    k = ease(seg(t, 0, D))
    albaran(img, fecha=G.FECHA, firma_p=1.0, marca=seg(t, D * 0.62, D * 0.8), cy=900, escala=lerp(0.96, 1.04, k), t=t)
    return img, dict(grain=7, tint=((255, 0, 30), 0.1 * seg(t, D * 0.6, D)))

# ---------- 5. nofirmo: le devuelves el albarán; él sonríe y habla ----------
def nofirmo(t, D, fi):
    esc = mundo(t)
    faros_ = _camion(esc)
    emp = ease(seg(t, D * 0.05, D * 0.3))
    albaran3d(esc, lerp(1.35, 1.2, emp), 1.125, lerp(-2.05, -1.72, emp), yaw=0.15)
    boligrafo3d(esc, 1.6, 1.13, -1.95, yaw=0.9)
    x, z = MOST
    cab = add(STAND, pose(head=-8 - 9 * ease(seg(t, D * 0.3, D * 0.45))))
    anciano(esc, cab, x, z, yaw=_yaw_a_mi(x, z), cara="neutral")
    k = ease(seg(t, D * 0.25, D))
    cam = Camara(ojo=(lerp(1.4, 1.3, k), lerp(1.7, 1.6, k), -2.62), mira=(lerp(1.3, 1.16, k), lerp(1.05, 1.5, k), lerp(-1.8, -1.3, k)),
                 fov=lerp(48, 28, k), roll=0.015 * math.sin(t * 1.3))
    img = esc.render(cam, luces_base(extra=_luces_camion(faros_) + [Luz((1.3, 2.2, -2.0), FLUOR, 3.0, fuerza=0.6)]))
    img = _destellos(img, cam, faros_)
    if k > 0.7:                                       # la sonrisa: una raja oscura, demasiado ancha
        q = proyectar(cam, (x + 0.0, 1.47, z - 0.115))
        if q:
            d = ImageDraw.Draw(img); s = 1.0 / max(q[2], 0.5) * 300 * seg(k, 0.7, 1.0)
            d.arc((q[0] - s, q[1] - s * 0.45, q[0] + s, q[1] + s * 0.35), 15, 165, fill=(26, 14, 14), width=max(3, int(s / 9)))
    return aclarar(img, 1.12, 0.9), dict(grain=9, tint=((255, 0, 30), 0.14 * seg(t, D * 0.45, D)))

# ---------- 6. caja: una caja con tu nombre; dentro, tu uniforme empapado, que suelta niebla ----------
def caja(t, D, fi):
    ab = ease(seg(t, D * 0.38, D * 0.6))
    esc = mundo(t)
    _camion(esc, faros=0.6)
    caja_carton(esc, *CAJA, abierta=ab, yaw=0.0, dentro=(96, 22, 22), mojada=0.6)
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(lerp(1.3, 1.15, k), lerp(2.25, 2.2, k), lerp(-3.3, -3.0, k)), mira=(CAJA[0], CAJA[1] + 0.15, CAJA[2] + 0.05), fov=lerp(46, 40, k))
    img = esc.render(cam, luces_base(extra=[Luz((1.0, 2.4, -2.1), FLUOR, 3.0, fuerza=0.9)]))
    d = ImageDraw.Draw(img)
    if ab < 0.2:                                      # la etiqueta: PARA: + tu nombre, corrido por el agua
        q = proyectar(cam, (CAJA[0] - 0.12, CAJA[1] + 0.39, CAJA[2] + 0.05))
        if q:
            s = 0.16 / q[2] * (1 / math.tan(math.radians(cam.fov) / 2)) * H / 2
            d.text((q[0] - s * 0.7, q[1] - s * 0.22), tr("PARA:"), font=font(int(s * 0.22)), fill=(150, 30, 30), anchor="lm")
            nombre_emborronado(img, q[0] - s * 0.05, q[1] + s * 0.12, size=s * 0.2, blur=max(4, int(s * 0.05)))
    if ab > 0.3:
        q = proyectar(cam, (CAJA[0], CAJA[1] + 0.35, CAJA[2]))
        if q: vapor(img, q[0], q[1], 360, t, n=10, alfa=int(190 * ab))
    return aclarar(img, 1.15, 0.9), dict(grain=8, tint=((255, 0, 30), 0.08 * ab))

# ---------- 7. placa: miras hacia abajo: la placa del uniforme que llevas dice RAÚL ----------
def placa(t, D, fi):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    p = seg(t, 0, D * 0.4)
    pecho_placa(img, G.PLACA, t=t, p=p, mojado=0.0)
    temblor = 6 * math.sin(t * 23) * seg(t, D * 0.5, D)
    img = img.transform(img.size, Image.AFFINE, (1, 0, temblor, 0, 1, 0))
    return img, dict(grain=8, glitch=0.25 if t > D * 0.6 and fi % 13 < 2 else 0.0, tint=((255, 0, 30), 0.14 * seg(t, D * 0.55, D)))

# ---------- 8. final: la puerta; fuera, en la niebla, alguien con tu uniforme mira hacia dentro. Tarjeta REGLA 8 ----------
def final(t, D, fi):
    esc = mundo(t)
    _camion(esc, faros=0.0)
    empleado(esc, STAND, -3.0, 2.2, yaw=math.pi, cara="ninguna")
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(1.4, 1.62, -2.7), mira=(-3.0, 1.5, 1.2), fov=lerp(44, 36, k))
    img = aclarar(etiquetas(esc.render(cam, luces_base(0.9)), esc, cam), 1.15, 0.9)
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.15, 0.5))
    d.rectangle((0, 260, W, 760), fill=(0, 0, 0))
    d.text((W / 2, 370), f"{tr('REGLA')} 8", font=font(int(150 * p) + 1), fill=(230, 40, 40), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    regla = tr("NO FIRMES SI EL CAMIÓN LLEGA ANTES DE LAS 6")
    fs = 66
    while d.textlength(regla, font=font(fs)) > W - 100 and fs > 30: fs -= 2
    d.text((W / 2, 530), regla, font=font(fs), fill=(240, 240, 230), anchor="mm")
    q = ease_back(seg(t, D * 0.55, D * 0.75))
    if q > 0:
        d.rounded_rectangle((200, 620, 880, 720), 24, fill=(200, 30, 30))
        d.text((W / 2, 670), tr("MAÑANA: REGLA 9"), font=font(int(56 * q) + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=9, glitch=0.25 if fi % 11 < 2 else 0.0)

ESCENA_FN = dict(arranque=arranque, premisa=premisa, llega=llega, albaran=albaran_, nofirmo=nofirmo, caja=caja, placa=placa, final=final)
PAUSA = dict(arranque=0.4, premisa=0.4, llega=0.5, albaran=0.6, nofirmo=0.6, caja=0.6, placa=0.9, final=1.8)
