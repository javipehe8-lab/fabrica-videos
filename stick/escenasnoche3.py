"""TURNO DE NOCHE 3 — "El baño está siempre roto" (escenas 3D con turno3d)."""
import math, os, random
from PIL import ImageDraw, ImageFilter
from motor import *
from motor3d import *
from turno3d import *

G = __import__("guionnoche3" + ("_en" if IDIOMA == "en" else ""))
NOTA = "Está ocupado. — R."
PUERTA = (-2.9, -0.3)                   # entrada de la tienda
MOST = (0.35, -1.25)                    # dónde se para la niña, frente al mostrador
AGUA = (150, 175, 190)

def hora(s0):
    s = 3 * 3600 + 7 * 60 + int(s0)
    return f"{s // 3600:02d}:{s // 60 % 60:02d}:{s % 60:02d}"

def _camino(a):
    """posición de la niña de la puerta al mostrador (a: 0-1)"""
    return lerp(PUERTA[0], MOST[0], a), lerp(PUERTA[1], MOST[1], a)

def _huellas_hasta(a, paso=0.09):
    yaw = math.atan2(MOST[0] - PUERTA[0], MOST[1] - PUERTA[1])
    return [(*_camino(k * paso), yaw) for k in range(int(a / paso) + 1)]

def _gotas(img, cam, p, fi, n=6, alto=420, ancho=80, semilla=0):
    q = proyectar(cam, p)
    if not q: return
    d = ImageDraw.Draw(img); r = random.Random(fi // 2 + semilla)
    for _ in range(n):
        gx = q[0] + r.uniform(-ancho, ancho); gy = q[1] + r.uniform(0, alto)
        d.line((gx, gy, gx, gy + 24), fill=AGUA, width=4)

def _fondo_mostrador(t, luz=1.0):
    esc = mundo(t, luz); aseo(esc)
    cam = cam_mostrador(t, mira=(0.6, 0.6, -1.5), fov=50)
    return esc.render(cam, luces_base(luz)).filter(ImageFilter.GaussianBlur(10))

def llegada(t, D, fi):
    """llegas a la gasolinera; bajo la marquesina, una figurita amarilla quieta en la niebla"""
    k = ease(min(1, t / D))
    esc = mundo(t); aseo(esc)
    coche(esc, -9.5, 4.0, yaw=1.4, col=(70, 30, 30))
    nina(esc, add(STAND, pose(head=-6)), 3.6, 12.6, yaw=math.pi, cara="ninguna")
    cam = Camara(ojo=(lerp(1.5, -0.5, k), lerp(1.7, 1.6, k), lerp(27, 18, k)), mira=(lerp(2.5, 0, k), 1.7, lerp(10, 0, k)), fov=56)
    img = etiquetas(esc.render(cam, luces_base()), esc, cam)
    return img, dict(grain=8)

def lista(t, D, fi):
    img = _fondo_mostrador(t)
    z = lerp(0.95, 1.06, ease(t / D))
    hoja_reglas(img, t, G.REGLAS, resalta=2 if t > D * 0.12 else None, nota=NOTA, nota_p=seg(t, D * 0.5, D * 0.85), zoom=z)
    return img, dict(grain=6)

def nina_(t, D, fi):
    """entra una niña sola con chubasquero amarillo, chorreando; deja huellas mojadas hasta el mostrador"""
    a = ease(seg(t, D * 0.05, D * 0.8))
    esc = mundo(t); aseo(esc)
    x, z = _camino(a)
    yaw = math.atan2(1.4 - x, -2.7 - z)
    p = walk(t, 0.5, 0.6) if 0 < a < 1 else add(STAND, pose(head=-14))
    nina(esc, p, x, z, yaw=yaw)
    huellas(esc, _huellas_hasta(a))
    cam = Camara(ojo=(1.4, 1.95 + 0.01 * math.sin(t * 2), -2.75), mira=(lerp(-2.6, 0.1, a), lerp(0.75, 0.85, a), lerp(0.6, -0.9, a)), fov=lerp(48, 44, a))
    img = esc.render(cam, luces_base())
    _gotas(img, cam, (x, 0.75, z), fi, n=7, alto=300, ancho=60)
    return img, dict(grain=8)

def pide(t, D, fi):
    """desde arriba del mostrador: solo asoma su cabeza; levanta la mano pidiendo la llave. Luego se da la vuelta y se va."""
    va = ease(seg(t, D * 0.72, D))
    esc = mundo(t); aseo(esc)
    huellas(esc, _huellas_hasta(1.0))
    x, z = lerp(MOST[0], -1.4, va), lerp(MOST[1], 0.2, va)
    mano = ease(seg(t, D * 0.05, D * 0.25)) * (1 - ease(seg(t, D * 0.55, D * 0.7)))
    if va <= 0:
        p = add(STAND, pose(head=-18, a2u=-14 + 80 * mano, a2l=12 + 10 * mano))
        yaw = math.atan2(1.4 - x, -2.7 - z)
    else:
        p = walk(t, 0.5, 0.6); yaw = lerp(math.atan2(1.4 - MOST[0], -2.7 - MOST[1]), math.atan2(-1.6, 1.4), ease(seg(va, 0, 0.3)))
    nina(esc, p, x, z, yaw=yaw)
    k = ease(seg(t, 0, D * 0.6))
    cam = Camara(ojo=(lerp(1.1, 0.95, k), 1.62, -2.55), mira=(lerp(MOST[0], x, va), lerp(0.9, 0.8, va), lerp(MOST[1], z, va) + 0.1), fov=lerp(46, 36, k) + 16 * va)
    img = esc.render(cam, luces_base())
    _gotas(img, cam, (x, 0.6, z), fi, n=5, alto=260, ancho=50, semilla=3)
    return img, dict(grain=8)

def puerta(t, D, fi):
    """la puerta del aseo, cerrada con llave: luz debajo, el pomo se mueve solo, sale agua"""
    voz_ = t > D * 0.5
    trem = (0.03 * math.sin(t * 55) if voz_ or (t > D * 0.25 and (fi // 4) % 3 == 0) else 0.0)
    parp = 1.0 if (fi // 2) % 9 else 0.4
    esc = mundo(t); aseo(esc, luz_dentro=parp, tirador=trem, agua=ease(seg(t, D * 0.2, D)))
    huellas(esc, _huellas_hasta(1.0))
    k = ease(seg(t, 0, D))
    x, z = ASEO
    cam = Camara(ojo=(lerp(1.4, 0.9, k), 1.62, lerp(-2.7, -3.1, k)), mira=(x, lerp(1.15, 1.1, k), z), fov=lerp(52, 38, k), roll=0.02 * math.sin(t * 1.4))
    img = esc.render(cam, luces_base(extra=[Luz((x, 0.3, z + 0.5), (220, 235, 225), 1.8, fuerza=0.9 * parp)]))
    img = etiquetas(img, esc, cam)
    return img, dict(grain=10, tint=((255, 0, 30), 0.16 * seg(t, D * 0.5, D)))

def camara(t, D, fi):
    """CAM 2: la niña está fuera, bajo la marquesina, quieta mirando la tienda. Al final gira la cabeza hacia la cámara."""
    esc = mundo(t); aseo(esc)
    gira = ease(seg(t, D * 0.6, D * 0.85))
    xn, zn = 1.5, 6.4
    yaw_cam = math.atan2(-6.2 - xn, 2.6 - zn)
    nina(esc, add(STAND, pose(head=-8)), xn, zn, yaw=lerp(math.pi, yaw_cam, gira))
    k = ease(seg(t, 0, D * 0.8))
    base = cam_cctv(2)
    cam = Camara(ojo=base.ojo, mira=(lerp(6.5, xn, k), lerp(0.8, 0.75, k), lerp(7.2, zn, k)), fov=lerp(60, 22, k))
    img = esc.render(cam, luces_base())
    img = cctv(etiquetas(img, esc, cam), 2, hora(64 + t))
    return img, dict(grain=12, glitch=0.3 if fi % 19 < 2 else 0.0)

def giro(t, D, fi):
    """primer plano: tu mano con la llave del aseo. Está empapada y gotea sobre el mostrador."""
    esc = mundo(t); aseo(esc, luz_dentro=1.0, agua=1.0)
    hx, hy, hz = 1.25, 1.32, -2.15
    brillo = 1.0 + 0.12 * math.sin(t * 9)
    mano_llave(esc, hx, hy, hz, brillo=brillo)
    ch = ease(seg(t, D * 0.2, D))                                                  # el charco sobre el mostrador crece
    esc.add(caja(0.14 + 0.1 * ch, 0.003, 0.12 + 0.08 * ch, (84, 104, 116)), mover(hx, 1.123, hz + 0.1), sesgo=0.5)
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(lerp(1.4, 1.32, k), lerp(1.85, 1.75, k), lerp(-2.85, -2.7, k)), mira=(hx, hy - 0.06, hz - 0.03), fov=lerp(46, 34, k))
    img = esc.render(cam, luces_base(0.8))
    img = etiquetas(img, esc, cam)
    _gotas(img, cam, (hx, hy - 0.02, hz - 0.02), fi, n=8, alto=360, ancho=120, semilla=7)
    # destellos del agua sobre el metal
    q = proyectar(cam, (hx, hy + 0.025, hz))
    if q:
        d = ImageDraw.Draw(img); r = random.Random(fi // 3)
        for _ in range(4):
            sx, sy = q[0] + r.uniform(-60, 60), q[1] + r.uniform(-90, 60)
            d.ellipse((sx - 6, sy - 6, sx + 6, sy + 6), fill=(235, 245, 250))
    return img, dict(grain=9, tint=((255, 0, 30), 0.14 * seg(t, D * 0.5, D)))

def final(t, D, fi):
    """la puerta del aseo: la luz de dentro se apaga. Tarjeta REGLA 3."""
    luz = 1.0 if t < D * 0.25 else 0.0
    esc = mundo(t); aseo(esc, luz_dentro=luz, agua=1.0)
    x, z = ASEO
    cam = Camara(ojo=(0.6, 1.6, -3.4), mira=(x, 1.0, z), fov=lerp(46, 36, ease(t / D)))
    img = esc.render(cam, luces_base(extra=[Luz((x, 0.3, z + 0.5), (220, 235, 225), 1.8, fuerza=0.9 * luz)]))
    img = etiquetas(img, esc, cam)
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.15, 0.5))
    d.rectangle((0, 360, W, 900), fill=(0, 0, 0))
    d.text((W / 2, 470), f"{tr('REGLA')} 3", font=font(int(150 * p) + 1), fill=(230, 40, 40), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    regla = tr("EL BAÑO SIEMPRE ESTÁ ROTO")
    fs = 70
    while d.textlength(regla, font=font(fs)) > W - 120 and fs > 30: fs -= 2
    d.text((W / 2, 640), regla, font=font(fs), fill=(240, 240, 230), anchor="mm")
    q = ease_back(seg(t, D * 0.55, D * 0.75))
    if q > 0:
        d.rounded_rectangle((200, 760, 880, 860), 24, fill=(200, 30, 30))
        d.text((W / 2, 810), tr("MAÑANA: REGLA 4"), font=font(int(56 * q) + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=9)

ESCENA_FN = dict(llegada=llegada, lista=lista, nina=nina_, pide=pide, puerta=puerta, camara=camara, giro=giro, final=final)
PAUSA = dict(llegada=0.4, lista=0.9, nina=0.5, pide=0.5, puerta=0.7, camara=0.7, giro=0.8, final=1.8)
