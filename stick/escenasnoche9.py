"""TURNO DE NOCHE 9 — "Si ves a Raúl, no le dejes entrar" (escenas 3D con turno3d)."""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter
from motor import *
from motor3d import *
from turno3d import *

G = __import__("guionnoche9" + ("_en" if IDIOMA == "en" else ""))
RAUL = (-3.0, 0.32)                       # Raúl, fuera, pegado al cristal de la puerta, mirando hacia dentro
YAW_DENTRO = math.pi                      # mirando hacia -z (hacia la tienda)
YO = (1.4, -2.6)                          # mi sitio, detrás del mostrador
CAM1_OJO, CAM1_MIRA, CAM1_FOV = (3.4, 2.7, -4.6), (-1.6, 0.8, -0.6), 58

def _luz_puerta(f=1.0):
    """la luz de la tienda que le da en la cara a través del cristal + un poco de luz fría desde fuera"""
    return [Luz((-2.9, 1.9, -1.0), FLUOR, 3.2, fuerza=0.95 * f), Luz((-3.0, 2.6, 2.2), (150, 170, 175), 3.0, fuerza=0.5 * f)]

def _p_cristal(t, golpe=0.0, llora=0.0):
    """las dos manos apoyadas en el cristal; golpe (0-1) mueve el brazo derecho; llora: hombros que tiemblan"""
    g = abs(math.sin(t * 7.0)) * golpe
    return pose(a1u=96, a1l=58, a2u=lerp(96, 120, g), a2l=lerp(58, 80, g),
                head=-4 + 3 * math.sin(t * 9) * llora, body=1.5 * math.sin(t * 11) * llora)

def _raul(esc, t, p=None, cara="scared"):
    return raul(esc, p or _p_cristal(t), RAUL[0], RAUL[1], yaw=YAW_DENTRO, cara=cara, mojado=1.0)

def _primer_plano(t, D, cara="scared", golpe=0.0, llora=1.0, zoom=(0.0, 0.0), alto_mira=1.55):
    esc = mundo(t)
    cab, pp = _raul(esc, t, _p_cristal(t, golpe, llora), cara)
    k = ease(seg(t, 0, D))
    z0 = lerp(zoom[0], zoom[1], k)
    cam = Camara(ojo=(-2.9, 1.58, lerp(-1.6, -1.1, z0)), mira=(-3.0, alto_mira, 0.4), fov=lerp(44, 38, z0),
                 roll=0.012 * math.sin(t * 1.2))
    img = esc.render(cam, luces_base(extra=_luz_puerta()))
    return img, cam, cab, pp

# ---------- 1. arranque: Raúl pegado al cristal, sonriendo demasiado ----------
def arranque(t, D, fi):
    img, cam, cab, pp = _primer_plano(t, D, cara="neutral", zoom=(0.35, 0.75), llora=0.0)
    img = sonrisa(img, cam, cab, p=1.0, ancho=1.25)
    img = cristal(img, t, gotas=1.0, vaho_=0.5)
    img = aclarar(img, 1.3, 0.85)
    rot = lambda im: rotulo_regla(im, 9, G.REGLA_CORTA, p=1.0, y=420)
    return img, dict(grain=8, glitch=0.2 if fi % 19 < 2 else 0.0, overlay=rot, tint=((255, 0, 30), 0.08))

# ---------- 2. premisa: la hoja de reglas, con la regla 9 y la nota de Raúl ----------
def premisa(t, D, fi):
    esc = mundo(t)
    cam = cam_mostrador(t, mira=(0.6, 0.6, -1.5), fov=50)
    img = esc.render(cam, luces_base()).filter(ImageFilter.GaussianBlur(10))
    z = lerp(0.62, 0.67, ease(t / D))
    hoja_reglas(img, t, G.REGLAS, resalta=8, nota=G.NOTA, nota_p=seg(t, D * 0.35, D * 0.8), zoom=z, cy=830, h_extra=800)
    return aclarar(img, 1.1, 0.92), dict(grain=7)

# ---------- 3. golpes: CAM 1 a las 3:00 (alguien en la puerta), luego desde el mostrador ----------
def golpes(t, D, fi):
    corte = D * 0.45
    esc = mundo(t)
    cab, _ = _raul(esc, t, _p_cristal(t, golpe=1.0, llora=1.0))
    if t < corte:
        empleado(esc, STAND, YO[0], YO[1], yaw=math.atan2(RAUL[0] - YO[0], RAUL[1] - YO[1]), cara="ninguna")   # yo, mirando a la puerta
        cam = Camara(ojo=CAM1_OJO, mira=CAM1_MIRA, fov=CAM1_FOV)
        img = esc.render(cam, luces_base(extra=_luz_puerta()))
        s = int(t * 1.3)
        img = cctv(aclarar(img, 1.2, 0.9), 1, f"03:00:{s:02d}")
        return img, dict(grain=12, glitch=0.3 if t < 0.12 or fi % 17 < 2 else 0.0)
    a = ease(seg(t, corte, D))
    cam = cam_mostrador(t, mira=(-3.0, 1.45, 0.3), fov=lerp(40, 30, a), temblor=0.02)
    img = esc.render(cam, luces_base(extra=_luz_puerta()))
    fl = max(0.0, 0.5 - (t - corte) / 0.3)
    return aclarar(img, 1.2, 0.88), dict(grain=8, flash=((255, 255, 255), fl))

# ---------- 4. habla: llorando, con las manos en el cristal ----------
def habla(t, D, fi):
    img, cam, cab, pp = _primer_plano(t, D, cara="scared", golpe=0.25, llora=1.0, zoom=(0.1, 0.45))
    img = lagrimas(img, cam, cab, p=0.4 + 0.6 * seg(t, 0, D), t=t)
    img = cristal(img, t, gotas=1.0, vaho_=0.4)
    return aclarar(img, 1.25, 0.86), dict(grain=8, tint=((255, 0, 30), 0.06))

# ---------- 5. placa: su placa, a un palmo: no dice Raúl, dice mi nombre (corrido por el agua) ----------
def placa(t, D, fi):
    esc = mundo(t)
    cab, pp = _raul(esc, t, pose(a1u=38, a1l=30, a2u=38, a2l=30, head=-6, body=1.2 * math.sin(t * 11)))
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(pp[0] - 0.05, pp[1] + 0.2, lerp(-1.0, -0.75, k)), mira=(pp[0] - 0.05, pp[1] + 0.12, pp[2]), fov=lerp(40, 32, k))
    img = esc.render(cam, luces_base(extra=_luz_puerta() + [Luz((pp[0], pp[1] + 0.3, pp[2] - 0.6), FLUOR, 1.5, fuerza=0.6)]))
    q = proyectar(cam, pp)
    if q:
        s = 0.12 / q[2] * (1 / math.tan(math.radians(cam.fov) / 2)) * H / 2       # ancho de la placa en píxeles
        a = seg(t, D * 0.2, D * 0.45)
        nombre_emborronado(img, q[0], q[1] + s * 0.02, size=s * 0.16, a=a, col=(26, 20, 16), anchor="mm", blur=max(6, int(s * 0.035)))
    img = cristal(img, t, gotas=1.3, vaho_=0.2, semilla=4)
    return aclarar(img, 1.2, 0.88), dict(grain=8, tint=((255, 0, 30), 0.12 * seg(t, D * 0.5, D)))

# ---------- 6. noabro: deja de llorar de golpe; la cara se queda quieta y sonríe ----------
def noabro(t, D, fi):
    cambia = D * 0.38
    quieto = t > cambia
    img, cam, cab, pp = _primer_plano(t if not quieto else cambia, D, cara="neutral" if quieto else "scared",
                                      golpe=0.0, llora=0.0 if quieto else 1.0, zoom=(0.4, 0.4))
    k = ease(seg(t, cambia, D))
    if not quieto:
        img = lagrimas(img, cam, cab, p=1.0, t=t)
    else:
        img = sonrisa(img, cam, cab, p=k, ancho=1.25)
        z = 1 + 0.12 * k                              # empuje lento hacia la cara
        w_, h_ = int(W / z), int(H / z)
        img = img.crop(((W - w_) // 2, int((H - h_) * 0.42), (W - w_) // 2 + w_, int((H - h_) * 0.42) + h_)).resize((W, H))
    img = cristal(img, t, gotas=1.0, vaho_=0.4)
    return aclarar(img, 1.25, 0.86), dict(grain=9, glitch=0.3 if abs(t - cambia) < 0.1 else 0.0, tint=((255, 0, 30), 0.14 * k))

# ---------- 7-8. la CAM 1: fuera, golpeando el cristal, estoy yo; dentro, detrás del mostrador, él ----------
def _cam1(t, saluda=0.0, mira_cam=0.0):
    esc = mundo(t)
    empleado(esc, _p_cristal(t, golpe=1.0), RAUL[0], RAUL[1], yaw=YAW_DENTRO, cara="ninguna")      # yo, fuera
    yaw_cam = math.atan2(CAM1_OJO[0] - YO[0], CAM1_OJO[2] - YO[1])
    p = pose(head=-14 * mira_cam, a2u=lerp(-14, 150, saluda), a2l=lerp(12, 30 + 20 * math.sin(t * 6) * saluda, saluda))
    cab, _ = raul(esc, p, YO[0], YO[1], yaw=lerp(math.pi * 0.85, yaw_cam, mira_cam), cara="neutral", mojado=0.0)
    cam = Camara(ojo=CAM1_OJO, mira=CAM1_MIRA, fov=CAM1_FOV)
    img = esc.render(cam, luces_base(extra=_luz_puerta()))
    return aclarar(img, 1.2, 0.9), cam, cab

def cam1(t, D, fi):
    img, cam, cab = _cam1(t, mira_cam=0.0)
    s = 47 + int(t * 1.3)
    img = cctv(img, 1, f"03:{s // 60 + 4:02d}:{s % 60:02d}")
    return img, dict(grain=12, glitch=0.35 if t < 0.12 or fi % 15 < 2 else 0.0)

def final(t, D, fi):
    k = ease(seg(t, 0, D * 0.35))
    img, cam, cab = _cam1(t, mira_cam=k, saluda=ease(seg(t, D * 0.3, D * 0.5)))
    s = 52 + int(t * 1.3)
    img = cctv(img, 1, f"03:{s // 60 + 4:02d}:{s % 60:02d}")
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.15, 0.5))
    d.rectangle((0, 230, W, 610), fill=(0, 0, 0))
    d.text((W / 2, 320), f"{tr('REGLA')} 9", font=font(int(150 * p) + 1), fill=(230, 40, 40), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    regla = tr("SI VES A RAÚL, NO LE DEJES ENTRAR")
    fs = 66
    while d.textlength(regla, font=font(fs)) > W - 100 and fs > 30: fs -= 2
    d.text((W / 2, 445), regla, font=font(fs), fill=(240, 240, 230), anchor="mm")
    q = ease_back(seg(t, D * 0.55, D * 0.75))
    if q > 0:
        d.rounded_rectangle((190, 500, 890, 590), 24, fill=(200, 30, 30))
        d.text((W / 2, 545), tr("MAÑANA: REGLA 10"), font=font(int(56 * q) + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=9, glitch=0.25 if fi % 11 < 2 else 0.0)

ESCENA_FN = dict(arranque=arranque, premisa=premisa, golpes=golpes, habla=habla, placa=placa, noabro=noabro, cam1=cam1, final=final)
PAUSA = dict(arranque=0.4, premisa=0.4, golpes=0.5, habla=0.6, placa=0.6, noabro=0.7, cam1=0.8, final=1.8)
