"""TURNO DE NOCHE 5 — "Si la niebla entra en la tienda, apaga todas las luces y no respires" (escenas 3D con turno3d)."""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter
from motor import *
from motor3d import *
from turno3d import *

G = __import__("guionnoche5" + ("_en" if IDIOMA == "en" else ""))
NOTA = "Yo respiré. — R."
FRENTE = (1.35, -1.2)                      # dónde se para la silueta, al otro lado del mostrador
OJO = (1.4, 1.62, -2.7)                    # tus ojos, detrás del mostrador

def _yaw_a_mi(x, z):
    return math.atan2(OJO[0] - x, OJO[2] - z)

def luz_fuera(f=1.0):
    """a oscuras solo entra la claridad fría de la niebla por el cristal"""
    return [Luz((-1.0, 2.2, 2.6), (120, 140, 150), 9.0, fuerza=0.55 * f), Luz((2.5, 2.2, 2.6), (120, 140, 150), 8.0, fuerza=0.35 * f)]

def hora(s0):
    s = 3 * 3600 + int(s0)
    return f"{s // 3600:02d}:{s // 60 % 60:02d}:{s % 60:02d}"

def _oscuro(t):
    esc = mundo(t, luz=0.0); esc.amb = 0.07
    return esc

def llegada(t, D, fi):
    """llegas a la gasolinera: la niebla, espesa, se arrastra por el asfalto hacia la tienda"""
    k = ease(min(1, t / D))
    esc = mundo(t)
    coche(esc, -9.5, 4.0, yaw=1.4, col=(70, 30, 30))
    r_ = random.Random(2)
    for i in range(40):                                                         # bancos de niebla rodando por el suelo
        x = r_.uniform(-10, 10) + 0.6 * t; z = r_.uniform(2, 16)
        esc.add(caja(r_.uniform(1.5, 3.5), r_.uniform(0.2, 0.7), r_.uniform(1, 2.5), (120, 128, 126), base=True), mover(x, 0, z), sesgo=0.05)
    cam = Camara(ojo=(lerp(1.5, -0.5, k), lerp(1.7, 1.6, k), lerp(27, 18, k)), mira=(lerp(3.0, -1.5, k), 1.5, lerp(12, 0, k)), fov=56)
    img = etiquetas(esc.render(cam, luces_base()), esc, cam)
    return img, dict(grain=8)

def lista(t, D, fi):
    esc = mundo(t)
    cam = cam_mostrador(t, mira=(0.6, 0.6, -1.5), fov=50)
    img = esc.render(cam, luces_base()).filter(ImageFilter.GaussianBlur(10))
    z = lerp(0.93, 1.0, ease(t / D))
    hoja_reglas(img, t, G.REGLAS, resalta=4 if t > D * 0.1 else None, nota=NOTA, nota_p=seg(t, D * 0.4, D * 0.85), zoom=z * 0.86, cy=790, h_extra=260)
    return img, dict(grain=6)

def niebla(t, D, fi):
    """plano subjetivo hacia la puerta: la niebla se cuela por la rendija y se extiende por el suelo"""
    k = ease(seg(t, 0, D))
    esc = mundo(t)
    parp = 0.5 if t > D * 0.7 and (fi // 2) % 5 == 0 else 1.0
    base = cam_puerta_cctv()
    cam = Camara(ojo=base.ojo, mira=base.mira, fov=lerp(62, 54, k))
    img = render_niebla(esc, cam, luces_base(parp), 0.08 + 0.6 * k, t=t, col=(190, 198, 196))
    return cctv(img, 1, hora(t)), dict(grain=10, glitch=0.25 if fi % 19 < 2 else 0.0)

def apago(t, D, fi):
    """clac: todo a oscuras. Entre las estanterías camina una silueta pálida hecha de niebla."""
    off = t > D * 0.12
    if not off:
        esc = mundo(t)
        cam = Camara(ojo=OJO, mira=(-2.6, 0.9, -0.6), fov=50)
        return render_niebla(esc, cam, luces_base(), 0.7, t=t, col=(190, 198, 196)), dict(grain=8)
    esc = _oscuro(t)
    a = ease(seg(t, D * 0.25, D))
    x, z = lerp(-3.0, -3.4, a), lerp(-0.4, -3.3, a)
    yw = math.atan2(-3.4 + 3.0, -3.3 + 0.4)
    figura_niebla(esc, walk(t, 0.3, 0.5), x, z, yaw=yw, col=(150, 160, 158), emite=False)
    yw_luz = _yaw_a_mi(x, z)
    k = ease(seg(t, D * 0.12, D))
    cam = Camara(ojo=(1.4, 1.62 + 0.006 * math.sin(t * 2.5), -2.7), mira=(lerp(-2.4, -3.0, k), lerp(0.6, 1.1, k), lerp(-1.4, -2.6, k)), fov=lerp(48, 42, k))
    img = render_niebla(esc, cam, luz_fuera() + [luz_figura(x, z, yw_luz, 0.8 + 0.15 * math.sin(t * 3))], 0.75, t=t, col=(70, 80, 80), emite=True)
    return img, dict(grain=11)

def voz(t, D, fi):
    """la silueta se para al otro lado del mostrador, inclinada hacia ti; habla con la voz de Raúl"""
    esc = _oscuro(t)
    a = ease(seg(t, 0, D * 0.3))
    x, z = lerp(0.2, FRENTE[0], a), lerp(-0.6, FRENTE[1], a)
    inc = ease(seg(t, D * 0.3, D * 0.6))
    p = walk(t, 0.3, 0.5) if a < 1 else add(STAND, pose(body=22 * inc, head=-8 * inc))
    figura_niebla(esc, p, x, z, yaw=_yaw_a_mi(x, z), col=(150, 160, 158), emite=False)
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(1.4, 1.62 + 0.006 * math.sin(t * 2.5), -2.7), mira=(lerp(x, 1.36, k), lerp(1.2, 1.45, k), lerp(z, -1.4, k)), fov=lerp(52, 44, k),
                 roll=0.012 * math.sin(t * 1.2))
    img = render_niebla(esc, cam, luz_fuera() + [luz_figura(x, z, _yaw_a_mi(x, z), 0.85 + 0.15 * math.sin(t * 3))], 0.8, t=t, col=(70, 80, 80), emite=True)
    return img, dict(grain=11, tint=((255, 0, 30), 0.14 * seg(t, D * 0.45, D)))

def aguanto(t, D, fi):
    """su cabeza sin cara a un palmo de la tuya, ladeándose, escuchando. Tú, sin respirar."""
    esc = _oscuro(t)
    inc = ease(seg(t, 0, D * 0.6))
    figura_niebla(esc, add(STAND, pose(body=22 + 16 * inc, head=-8 - 6 * inc)), FRENTE[0], FRENTE[1] - 0.05 * inc, yaw=_yaw_a_mi(*FRENTE), col=(150, 160, 158), emite=False)
    k = ease(seg(t, 0, D))
    tiembla = 0.004 * seg(t, D * 0.4, D)
    cam = Camara(ojo=(1.4 + tiembla * math.sin(t * 31), 1.62 + tiembla * math.sin(t * 27), -2.75), mira=(1.38, lerp(1.55, 1.5, k), -1.5), fov=lerp(46, 38, k),
                 roll=0.06 * math.sin(t * 0.9))
    img = esc.render(cam, luz_fuera() + [luz_figura(FRENTE[0], FRENTE[1], _yaw_a_mi(*FRENTE), 0.9, y=1.6)])
    # el borde de la imagen se oscurece: te falta el aire
    v = Image.new("L", img.size, 0); dv = ImageDraw.Draw(v)
    m = int(lerp(60, 230, seg(t, 0, D)))
    dv.ellipse((m - 200, m, W - m + 200, H - m), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(120))
    img = Image.composite(img, Image.new("RGB", img.size, (0, 0, 0)), v)
    return img, dict(grain=12, tint=((255, 0, 30), 0.1))

def giro(t, D, fi):
    """enciendes: la niebla se retira por debajo de la puerta. En la hoja, bajo la nota de Raúl, aparece escrito en el vaho: TÚ TODAVÍA NO"""
    corte = D * 0.32
    if t < corte:
        k = ease(seg(t, 0, corte))
        esc = mundo(t)
        img = render_niebla(esc, cam_puerta_cctv(), luces_base(), 0.7 * (1 - k), t=t, col=(190, 198, 196))
        return cctv(img, 1, hora(40 + t)), dict(grain=9, flash=((255, 255, 255), max(0.0, 0.8 - t / 0.3)))
    esc = mundo(t)
    cam = cam_mostrador(t, mira=(0.6, 0.6, -1.5), fov=50)
    img = esc.render(cam, luces_base()).filter(ImageFilter.GaussianBlur(10))
    z = lerp(1.0, 1.05, ease(seg(t, corte, D)))
    hoja_reglas(img, t, G.REGLAS, resalta=4, nota=NOTA, nota_p=1.0, zoom=z * 0.86, cy=790, h_extra=260)
    p = seg(t, corte + D * 0.12, D * 0.85)
    img = vaho(img, "TÚ TODAVÍA NO", W / 2, 640, size=130, p=p, ancho=760)
    return img, dict(grain=8, tint=((255, 0, 30), 0.1 * seg(t, D * 0.8, D)))

def final(t, D, fi):
    """luces encendidas, la niebla fuera. Al otro lado del cristal, una silueta con gorra, quieta, mirándote. Tarjeta REGLA 5."""
    esc = mundo(t)
    figura_niebla(esc, STAND, -1.4, 3.2, yaw=_yaw_a_mi(-1.4, 3.2), col=(150, 158, 156), brillo=0.75)
    k = ease(t / D)
    cam = Camara(ojo=OJO, mira=(lerp(-1.0, -1.3, k), 2.2, 1.5), fov=lerp(44, 36, k))
    img = esc.render(cam, luces_base())
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.15, 0.5))
    d.rectangle((0, 300, W, 840), fill=(0, 0, 0))
    d.text((W / 2, 410), f"{tr('REGLA')} 5", font=font(int(150 * p) + 1), fill=(230, 40, 40), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    regla = tr("SI ENTRA LA NIEBLA, NO RESPIRES")
    fs = 70
    while d.textlength(regla, font=font(fs)) > W - 120 and fs > 30: fs -= 2
    d.text((W / 2, 580), regla, font=font(fs), fill=(240, 240, 230), anchor="mm")
    q = ease_back(seg(t, D * 0.55, D * 0.75))
    if q > 0:
        d.rounded_rectangle((200, 700, 880, 800), 24, fill=(200, 30, 30))
        d.text((W / 2, 750), tr("MAÑANA: REGLA 6"), font=font(int(56 * q) + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=9, glitch=0.25 if fi % 11 < 2 else 0.0)

ESCENA_FN = dict(llegada=llegada, lista=lista, niebla=niebla, apago=apago, voz=voz, aguanto=aguanto, giro=giro, final=final)
PAUSA = dict(llegada=0.4, lista=0.9, niebla=0.5, apago=0.6, voz=0.7, aguanto=0.7, giro=0.9, final=1.8)
