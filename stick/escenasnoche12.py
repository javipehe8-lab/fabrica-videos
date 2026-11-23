"""TURNO DE NOCHE 12 (final de temporada) — "Nunca devuelvas el saludo" (escenas 3D con turno3d)."""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter
from motor import *
from motor3d import *
from turno3d import *
from turno3d import _envolver

G = __import__("guionnoche12" + ("_en" if IDIOMA == "en" else ""))
SITIOS = [((0.15, -2.6), "anciano"), ((0.75, -2.62), "raul"), ((1.35, -2.6), "sincara")]
HUECO = (-0.45, -2.6)                     # el sitio que me guardaban
CX = 0.75
OJO2 = (-0.75, 1.62, -3.45)                # mis ojos, ya detrás del mostrador (en el hueco)

def _luz_frente(f=1.0):
    return [Luz((CX, 1.9, -1.0), FLUOR, 3.6, fuerza=0.95 * f), Luz((CX, 2.4, 0.6), (160, 176, 180), 4.0, fuerza=0.45 * f)]

# ---------- 1. arranque: por encima de mi hombro, los tres con mi uniforme saludan... y yo les devuelvo el saludo ----------
def _mi_brazo(esc, t, x, z, k=1.0):
    """yo, en primer plano y hundido bajo la cámara: solo se ve mi brazo (manga del uniforme) saludando"""
    return empleado(esc, pose_saludo(t, k), x, z, yaw=math.pi, cara="ninguna")

def arranque(t, D, fi):
    k = ease(seg(t, 0, D))
    esc = otra_gasolinera(t)
    cabs = [plantilla(esc, pos, pose_saludo(t, 1.0), yaw=0.0, cual=cual) for (pos, cual) in SITIOS]
    zc = lerp(-0.35, -0.5, k)
    _mi_brazo(esc, t, CX + 0.42, zc - 0.75)
    cam = Camara(ojo=(CX - 0.12, 1.52, zc + 0.15), mira=(CX + 0.05, 1.5, -2.6), fov=lerp(60, 56, k), roll=0.01 * math.sin(t * 1.3))
    img = esc.render(cam, luces_base(extra=_luz_frente()))
    img = sonrisa(img, cam, cabs[1], p=1.0, ancho=1.2)
    img = sonrisa(img, cam, cabs[0], p=1.0, ancho=1.0)
    img = cristal(img, t, gotas=0.5, vaho_=0.2, reflejo=0.2)
    img = aclarar(img, 1.3, 0.84)
    rot = lambda im: rotulo_regla(im, 12, G.REGLA_CORTA, p=1.0, y=440)
    return img, dict(grain=8, glitch=0.2 if fi % 19 < 2 else 0.0, overlay=rot, tint=((255, 0, 30), 0.06))

# ---------- 2. mano: mi mano sigue saludando sola; parpadeo y ya estoy en el hueco, detrás del mostrador: se giran hacia mí ----------
def mano(t, D, fi):
    k = ease(seg(t, 0, D))
    salto = D * 0.45
    esc = otra_gasolinera(t)
    if t < salto:                                       # aún fuera del mostrador: mi brazo saludando, en primer plano
        cabs = [plantilla(esc, pos, pose_saludo(t, 1.0), yaw=0.0, cual=cual) for (pos, cual) in SITIOS]
        zc = lerp(-0.6, -0.8, k)
        _mi_brazo(esc, t * 1.7, CX + 0.28, zc - 0.55)
        cam = Camara(ojo=(CX + 0.05, 1.5, zc), mira=(CX - 0.05, 1.48, -2.6), fov=50, roll=0.03 * math.sin(t * 5))
        img = esc.render(cam, luces_base(extra=_luz_frente()))
        img = sonrisa(img, cam, cabs[1], p=1.0, ancho=1.2)
        return aclarar(img, 1.3, 0.85), dict(grain=9)
    g = ease(seg(t, salto, D * 0.8))                    # detrás del mostrador: los tres se giran hacia mí, sonriendo
    cabs = []
    for i, (pos, cual) in enumerate(SITIOS):
        yf = math.atan2(OJO2[0] - pos[0], OJO2[2] - pos[1])
        cabs.append(plantilla(esc, pos, pose_saludo(t, 1.0 - g), yaw=lerp(0.0, yf, ease(seg(t, salto + i * 0.12, salto + 0.5 + i * 0.12))), cual=cual))
    cam = Camara(ojo=OJO2, mira=(0.75, 1.42, -2.45), fov=lerp(60, 54, k), roll=0.015 * math.sin(t * 2))
    img = esc.render(cam, luces_base(extra=[Luz((-0.4, 2.2, -3.2), FLUOR, 3.5, fuerza=0.9)]))
    img = sonrisa(img, cam, cabs[0], p=g, ancho=1.0)
    img = sonrisa(img, cam, cabs[1], p=g, ancho=1.2)
    fl = 0.5 if abs(t - salto) < 0.07 else 0.0
    return aclarar(img, 1.3, 0.85), dict(grain=9, flash=((255, 255, 255), fl), tint=((255, 0, 30), 0.08 * g))

# ---------- 3. hoja: delante de mí, la hoja de reglas en blanco; arriba, con mi letra: "Regla 12:" ----------
def _fondo_mostrador(t, blur=11):
    esc = otra_gasolinera(t)
    for (pos, cual) in SITIOS:
        plantilla(esc, pos, pose(a1u=-6, a1l=8, a2u=-6, a2l=8, head=-4), yaw=-math.pi / 2 - 0.25, cual=cual)
    cam = Camara(ojo=(-0.6, 1.75, -2.4), mira=(0.4, 1.05, -1.9), fov=60)
    img = esc.render(cam, luces_base(extra=[Luz((-0.2, 2.1, -1.6), FLUOR, 3.5, fuerza=0.9)]))
    return aclarar(img.filter(ImageFilter.GaussianBlur(blur)), 1.1, 0.92)

def hoja(t, D, fi):
    img = _fondo_mostrador(t)
    k = ease(seg(t, 0, D))
    hoja_blanca(img, G.REGLA_MANO[0], p=1.0, cy=900, zoom=lerp(0.84, 0.94, k), t=t)
    return img, dict(grain=7)

# ---------- 4. escribo: cada regla la escribió alguien justo después de perder; el bolígrafo escribe la mía ----------
def escribo(t, D, fi):
    img = _fondo_mostrador(t)
    L = G.REGLA_MANO
    p0 = len(L[0]) / sum(len(x) for x in L)
    p = lerp(p0, 1.0, ease(seg(t, D * 0.25, D * 0.9)))
    hoja_mano(img, L, p=p, cy=880, zoom=0.94, t=t, size=96, salto=150, arriba=300, titulo=True)
    return img, dict(grain=7, tint=((255, 0, 30), 0.05 * ease(seg(t, D * 0.8, D))))

# ---------- 5. nuevo: a las siete se abre la puerta; entra el nuevo del turno de noche, con su hoja ----------
def nuevo_(t, D, fi):
    k = ease(seg(t, 0, D))
    esc = mundo(t)
    z = lerp(0.9, -0.7, ease(seg(t, 0, D * 0.8)))
    p = walk(t, 0.5, 0.6) if t < D * 0.8 else add(STAND, pose(head=-6))
    nuevo(esc, p, -2.9, z, yaw=math.pi * 0.82, cara="neutral")
    cam = Camara(ojo=(-0.85 + 0.01 * math.sin(t * 1.7), 1.65, -2.6), mira=(-2.9, 1.25, lerp(0.3, -0.5, k)), fov=lerp(44, 36, k))
    img = esc.render(cam, luces_base(extra=[Luz((-2.9, 2.6, -1.2), FLUOR, 3.5, fuerza=0.9)]))
    etiquetas(img, esc, cam)
    return aclarar(img, 1.3, 0.85), dict(grain=8)

# ---------- 6. lista: su hoja está escrita ENTERA con mi letra; también la regla uno ----------
def _fondo_tienda(t, blur=12):
    esc = mundo(t)
    nuevo(esc, add(STAND, pose(head=-14, a1u=40, a1l=60, a2u=40, a2l=60)), -1.0, -1.2, yaw=0.3, hoja=False)
    img = esc.render(Camara(ojo=(-0.6, 1.62, -2.6), mira=(-1.0, 1.2, -0.6), fov=55), luces_base())
    return aclarar(img.filter(ImageFilter.GaussianBlur(blur)), 1.1, 0.92)

def lista(t, D, fi):
    img = _fondo_tienda(t)
    hoja_mano(img, G.LISTA, p=1.0, cy=800, zoom=0.96, t=t, humeda=False, pluma=False)
    k = ease(seg(t, D * 0.45, D * 0.95))                # empuje hacia la regla uno
    z = 1 + 0.45 * k
    w_, h_ = int(W / z), int(H / z)
    cx, cy = lerp(W / 2, 470, k), lerp(H / 2, 470, k)
    x0 = int(min(max(0, cx - w_ / 2), W - w_)); y0 = int(min(max(0, cy - h_ / 2), H - h_))
    img = img.crop((x0, y0, x0 + w_, y0 + h_)).resize((W, H))
    return img, dict(grain=7, tint=((255, 0, 30), 0.07 * k))

# ---------- 7. camara: en la CAM 1 sale él solo detrás del mostrador; yo, a su lado, ya no salgo ----------
def _cam1(t):
    esc = mundo(t)
    mira = 0.6 * math.sin(t * 1.4)
    nuevo(esc, add(STAND, pose(head=-4)), 0.6, -2.6, yaw=mira, cara="neutral", hoja=False)
    img = esc.render(Camara(ojo=(3.0, 2.75, -0.5), mira=(0.2, 1.0, -2.7), fov=58), luces_base())
    return aclarar(img, 1.2, 0.88)

def camara(t, D, fi):
    s = 12 + int(t)
    pant = cctv(_cam1(t), 1, f"07:01:{s:02d}")
    img = monitor(_fondo_tienda(t, blur=14), pant, t)
    k = ease(seg(t, D * 0.3, D))
    z = 1 + 0.3 * k
    w_, h_ = int(W / z), int(H / z)
    ox, oy = (W - w_) // 2, int((H - h_) * 0.42)
    img = img.crop((ox, oy, ox + w_, oy + h_)).resize((W, H))
    return img, dict(grain=9, glitch=0.3 if fi % 23 < 2 else 0.0)

# ---------- 8. final: CAM 2, junto al surtidor 4, alguien con mi uniforme saluda: soy yo. Tarjeta REGLA 12 ----------
def _cam2(t):
    esc = mundo(t, surtidor4=1.0)
    fx, fz = S4[0] - 0.9, S4[1] + 0.3
    cam = Camara(ojo=(3.0, 3.0, 6.6), mira=(fx, 2.0, fz), fov=32)
    yaw = math.atan2(cam.ojo[0] - fx, cam.ojo[2] - fz)
    empleado(esc, pose_saludo(t, 1.0), fx, fz, yaw=yaw, cara="ninguna")
    img = esc.render(cam, luces_base(extra=[Luz((fx - 1.0, 3.0, fz), (190, 200, 196), 4.0, fuerza=0.8)]))
    etiquetas(img, esc, cam)
    return cctv(aclarar(img, 1.15, 0.9), 2, f"07:0{2 + int(t) // 60}:{(30 + int(t)) % 60:02d}")

def final(t, D, fi):
    img = _cam2(t)
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.15, 0.5))
    d.rectangle((0, 200, W, 680), fill=(0, 0, 0))
    d.text((W / 2, 295), f"{tr('REGLA')} 12", font=font(int(150 * p) + 1), fill=(230, 40, 40), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    regla = tr("NUNCA DEVUELVAS EL SALUDO")
    fnt = font(64)
    for i, ln in enumerate(_envolver(d, regla, fnt, W * 0.7)[:2]):
        d.text((W / 2, 420 + i * 72), ln, font=fnt, fill=(240, 240, 230), anchor="mm")
    d.text((W - 70, 730), "CAM 2", font=font(64), fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0), anchor="rm")
    d.ellipse((W - 330, 712, W - 294, 748), fill=(230, 30, 30) if int(t * 2) % 2 == 0 else (90, 20, 20))
    q = ease_back(seg(t, D * 0.55, D * 0.75))
    if q > 0:
        d.rounded_rectangle((190, 555, 890, 645), 24, fill=(200, 30, 30))
        d.text((W / 2, 600), tr("MAÑANA: REGLA 13"), font=font(int(56 * q) + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=8, glitch=0.2 if fi % 13 < 2 else 0.0)

ESCENA_FN = dict(arranque=arranque, mano=mano, hoja=hoja, escribo=escribo, nuevo=nuevo_, lista=lista, camara=camara, final=final)
PAUSA = dict(arranque=0.4, mano=0.5, hoja=0.5, escribo=0.6, nuevo=0.5, lista=0.6, camara=0.7, final=1.8)
