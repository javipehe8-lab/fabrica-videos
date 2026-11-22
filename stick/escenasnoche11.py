"""TURNO DE NOCHE 11 — "Nunca cruces el kilómetro 10" (escenas 3D con turno3d)."""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter
from motor import *
from motor3d import *
from turno3d import *
from turno3d import _envolver

G = __import__("guionnoche11" + ("_en" if IDIOMA == "en" else ""))
# los tres de la otra gasolinera, detrás de su mostrador, mirando hacia la cristalera (hacia mí, fuera)
SITIOS = [((0.15, -2.6), "anciano"), ((0.75, -2.62), "raul"), ((1.35, -2.6), "sincara")]
HUECO = (-0.45, -2.6)                     # el sitio vacío a su lado (el mío)
CX = 0.75
CAM1_O = Camara(ojo=(0.2, 2.8, -0.15), mira=(0.2, 1.0, -2.6), fov=80)

def _luz_frente(f=1.0):
    """luz que les da en la cara (fluorescente de la tienda + el reflejo de la cristalera)"""
    return [Luz((CX, 1.9, -1.0), FLUOR, 3.6, fuerza=0.95 * f), Luz((CX, 2.4, 0.6), (160, 176, 180), 4.0, fuerza=0.45 * f)]

def _tres(t, saluda=0.0, cam=None, mira_y=1.42, sonrie=0.0):
    """los tres empleados vistos desde fuera, a través del cristal; saluda (0-1): levantan la mano todos a la vez"""
    esc = otra_gasolinera(t)
    cabs = []
    for (pos, cual) in SITIOS:
        p = pose_saludo(t, saluda) if saluda > 0 else pose(a1u=-6, a1l=8, a2u=-6, a2l=8, head=-4)
        cara = "neutral"
        cabs.append(plantilla(esc, pos, p, yaw=0.0, cual=cual, cara=cara))
    img = esc.render(cam, luces_base(extra=_luz_frente()))
    if sonrie > 0: img = sonrisa(img, cam, cabs[1], p=sonrie, ancho=1.2)
    img = cristal(img, t, gotas=0.8, vaho_=0.35, reflejo=0.3)
    return img

# ---------- 1. arranque: a través del cristal de la otra gasolinera, tres con mi uniforme me saludan a la vez ----------
def arranque(t, D, fi):
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(CX, 1.55, lerp(-0.75, -0.95, k)), mira=(CX, 1.5, -2.6), fov=lerp(52, 48, k), roll=0.01 * math.sin(t * 1.3))
    img = _tres(t, saluda=1.0, cam=cam, sonrie=1.0)
    img = aclarar(img, 1.3, 0.84)
    rot = lambda im: rotulo_regla(im, 11, G.REGLA_CORTA, p=1.0, y=440)
    return img, dict(grain=8, glitch=0.2 if fi % 19 < 2 else 0.0, overlay=rot, tint=((255, 0, 30), 0.06))

# ---------- 2. cruzo: ya he pasado el cartel; me giro: detrás de él, el resplandor de mi gasolinera se apaga ----------
def cruzo(t, D, fi):
    esc = Escena(niebla=((70, 78, 78), 4.0, 34.0), amb=0.22)
    esc.etiquetas = []
    if t < D * 0.35: f = 1.0                                   # la luz de mi gasolinera: parpadea y se apaga (ya no hay vuelta)
    elif t < D * 0.6: f = 0.15 + 0.85 * (1 if int(t * 14) % 3 else 0)
    else: f = 0.0
    trasera(esc, luz_puerta=f)
    cartel_km(esc, -0.2, -13.5, "KILÓMETRO 10", yaw=math.pi)   # el cartel, por la cara que da a la niebla
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(lerp(-0.15, 0.1, k), 1.65 + 0.03 * math.sin(t * 9), lerp(-17.4, -18.0, k)), mira=(-0.1, 1.9, -8.0), fov=46,
                 roll=0.02 * math.sin(t * 4))
    img = esc.render(cam, luz_trasera(f) + [Luz((0.4, 3.2, -15.5), (170, 186, 186), 5.0, fuerza=0.8)])
    # resplandor de las luces de la gasolinera sobre el tejado, en la niebla
    q = proyectar(cam, (0.0, 3.4, -6.0))
    if q:
        capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
        r = 520
        dc.ellipse((q[0] - r * 1.3, q[1] - r * 0.6, q[0] + r * 1.3, q[1] + r * 0.6), fill=(255, 236, 200, int(150 * f)))
        img.paste(capa.filter(ImageFilter.GaussianBlur(110)), (0, 0), capa.filter(ImageFilter.GaussianBlur(110)))
    etiquetas(img, esc, cam)
    img = aclarar(img, 1.25, 0.86)
    img = vapor(img, W / 2, 1650, 900, t, n=8, alfa=40, alto=600)
    fl = 0.25 if abs(t - D * 0.6) < 0.06 else 0.0
    return img, dict(grain=9, flash=((255, 255, 255), fl), dark=0.2 * ease(seg(t, D * 0.6, D)))

# ---------- 3. otra: en la niebla, otra gasolinera idéntica. El rótulo: KILÓMETRO 10 ----------
def otra(t, D, fi):
    esc = otra_gasolinera(t)
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(lerp(1.7, 1.4, k), 1.8, lerp(21.0, 15.0, k)), mira=(0.3, 2.6, 0.0), fov=lerp(40, 36, k))
    img = esc.render(cam, luces_base())
    etiquetas(img, esc, cam)
    return aclarar(img, 1.3, 0.85), dict(grain=8)

# ---------- 4. dentro: detrás del mostrador, tres empleados con mi uniforme, quietos, mirándome ----------
def dentro(t, D, fi):
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(CX, 1.6, lerp(-0.12, -0.3, k)), mira=(CX, 1.38, -2.6), fov=lerp(68, 62, k))
    img = _tres(t, saluda=0.0, cam=cam)
    return aclarar(img, 1.3, 0.85), dict(grain=8)

# ---------- 5. saludo: levantan la mano a la vez, como en la cámara 2. Raúl: "Pasa. Te guardamos el sitio." ----------
def saludo(t, D, fi):
    k = ease(seg(t, 0, D))
    s = ease(seg(t, 0.1, 0.6))
    cam = Camara(ojo=(CX, 1.58, lerp(-0.3, -0.7, k)), mira=(CX, 1.45, -2.6), fov=lerp(62, 54, k), roll=0.012 * math.sin(t * 1.1))
    img = _tres(t, saluda=s, cam=cam, sonrie=ease(seg(t, D * 0.45, D * 0.7)))
    return aclarar(img, 1.3, 0.85), dict(grain=9, tint=((255, 0, 30), 0.08 * k), glitch=0.25 if abs(t - D * 0.45) < 0.08 else 0.0)

# ---------- 6. monitor: en su CAM 1 hay CUATRO detrás del mostrador; el cuarto, con la cabeza gacha, escribe: soy yo ----------
def _cam1_otra(t, escribe=1.0):
    esc = otra_gasolinera(t)
    for (pos, cual) in SITIOS:
        plantilla(esc, pos, pose(a1u=-6, a1l=8, a2u=-6, a2l=8, head=-4), yaw=0.0, cual=cual)
    pe = pose(head=28, body=9, a1u=48, a1l=46 + 6 * math.sin(t * 9) * escribe, a2u=40, a2l=40)
    empleado(esc, pe, HUECO[0], HUECO[1] + 0.12, yaw=0.0, cara="ninguna")                  # yo: el cuarto, inclinado sobre el mostrador
    img = esc.render(CAM1_O, luces_base(extra=_luz_frente(0.8)))
    return aclarar(img, 1.2, 0.88)

def _fondo_otra(t, mira=(CX, 1.3, -2.6), fov=60, blur=10):
    esc = otra_gasolinera(t)
    for (pos, cual) in SITIOS:
        plantilla(esc, pos, pose(a1u=-6, a1l=8, a2u=-6, a2l=8, head=-4), yaw=0.0, cual=cual)
    img = esc.render(Camara(ojo=(CX, 1.6, -0.2), mira=mira, fov=fov), luces_base(extra=_luz_frente()))
    return aclarar(img.filter(ImageFilter.GaussianBlur(blur)), 1.1, 0.92)

def monitor_(t, D, fi):
    s = 31 + int(t)
    pant = cctv(_cam1_otra(t), 1, f"04:{11 + s // 60:02d}:{s % 60:02d}")
    img = monitor(_fondo_otra(t), pant, t)
    k = ease(seg(t, D * 0.35, D))
    z = 1 + 0.22 * k                                   # empuje hacia el cuarto (a la izquierda de la pantalla)
    w_, h_ = int(W / z), int(H / z)
    ox = int((W - w_) * 0.12)
    img = img.crop((ox, int((H - h_) * 0.45), ox + w_, int((H - h_) * 0.45) + h_)).resize((W, H))
    return img, dict(grain=9, glitch=0.3 if fi % 21 < 2 else 0.0, tint=((255, 0, 30), 0.08 * k))

# ---------- 7. hoja: en su mostrador, una hoja de reglas en blanco; arriba, con mi letra: "Regla 12:" ----------
def _fondo_mostrador_otra(t):
    esc = otra_gasolinera(t)
    cam = Camara(ojo=(1.6, 1.75, -0.9), mira=(1.4, 1.05, -2.0), fov=55)
    img = esc.render(cam, luces_base())
    return aclarar(img.filter(ImageFilter.GaussianBlur(11)), 1.1, 0.92)

def hoja(t, D, fi):
    img = _fondo_mostrador_otra(t)
    k = ease(seg(t, 0, D))
    hoja_blanca(img, "Regla 12:", p=1.0, cy=900, zoom=lerp(0.86, 0.94, k), t=t)
    return img, dict(grain=7)

# ---------- 8. final: la tarjeta REGLA 11, sobre la hoja en blanco ----------
def final(t, D, fi):
    img = _fondo_mostrador_otra(t)
    hoja_blanca(img, "Regla 12:", p=1.0, cy=1150, zoom=0.82, t=t)
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.15, 0.5))
    d.rectangle((0, 200, W, 680), fill=(0, 0, 0))
    d.text((W / 2, 295), f"{tr('REGLA')} 11", font=font(int(150 * p) + 1), fill=(230, 40, 40), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    regla = tr("NUNCA CRUCES EL KILÓMETRO 10")
    fnt = font(64)
    for i, ln in enumerate(_envolver(d, regla, fnt, W * 0.62)[:2]):
        d.text((W / 2, 420 + i * 72), ln, font=fnt, fill=(240, 240, 230), anchor="mm")
    q = ease_back(seg(t, D * 0.55, D * 0.75))
    if q > 0:
        d.rounded_rectangle((190, 555, 890, 645), 24, fill=(200, 30, 30))
        d.text((W / 2, 600), tr("MAÑANA: REGLA 12"), font=font(int(56 * q) + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=8, glitch=0.2 if fi % 13 < 2 else 0.0)

ESCENA_FN = dict(arranque=arranque, cruzo=cruzo, otra=otra, dentro=dentro, saludo=saludo, monitor=monitor_, hoja=hoja, final=final)
PAUSA = dict(arranque=0.4, cruzo=0.5, otra=0.5, dentro=0.5, saludo=0.7, monitor=0.6, hoja=0.6, final=1.8)
