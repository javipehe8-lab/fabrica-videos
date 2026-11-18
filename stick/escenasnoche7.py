"""TURNO DE NOCHE 7 — "No leas nada que no hayas escrito tú" (escenas 3D con turno3d)."""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter
from motor import *
from motor3d import *
from turno3d import *

G = __import__("guionnoche7" + ("_en" if IDIOMA == "en" else ""))
LIB = (1.3, 1.125, -1.95)                  # el cuaderno, abierto sobre el mostrador

def _fondo(t, blur=12, luz=1.0):
    esc = mundo(t, luz=luz)
    cuaderno3d_abierto(esc, *LIB)
    cam = cam_mostrador(t, mira=(1.3, 0.9, -1.6), fov=50)
    return esc.render(cam, luces_base(luz)).filter(ImageFilter.GaussianBlur(blur))

# ---------- 1. arranque: la página se escribe sola mientras la lees ----------
def arranque(t, D, fi):
    img = _fondo(t)
    k = ease(seg(t, 0, D))
    p = 1.55 + 0.45 * seg(t, 0.2, D * 0.8)           # "Estoy leyendo esta línea" se escribe mientras la dices
    pagina(img, G.PAG_HOY[:2], fecha=G.HOY, p=p, cy=1090, escala=lerp(1.0, 1.06, k), t=t, size=82, humeda=1)
    img = aclarar(img, 1.05, 0.95)
    rot = lambda im: rotulo_regla(im, 7, G.REGLA_CORTA, p=1.0, y=420)
    return img, dict(grain=7, glitch=0.2 if fi % 19 < 2 else 0.0, overlay=rot, tint=((255, 0, 30), 0.1))

# ---------- 2. premisa: la hoja de reglas con la regla 7; el cuaderno en el mostrador ----------
def premisa(t, D, fi):
    esc = mundo(t)
    cam = cam_mostrador(t, mira=(0.6, 0.6, -1.5), fov=50)
    img = esc.render(cam, luces_base()).filter(ImageFilter.GaussianBlur(10))
    z = lerp(0.74, 0.8, ease(t / D))
    hoja_reglas(img, t, G.REGLAS, resalta=6, nota="Yo respiré. — R.", nota_p=1.0, zoom=z, cy=820, h_extra=420)
    return aclarar(img, 1.1, 0.92), dict(grain=7)

# ---------- 3. abro: el cuaderno cerrado en el mostrador -> la tapa ----------
def abro(t, D, fi):
    corte = D * 0.45
    if t < corte:
        esc = mundo(t)
        cuaderno3d(esc, *LIB, yaw=0.2)
        k = ease(seg(t, 0, corte))
        cam = Camara(ojo=(1.45, lerp(1.75, 1.55, k), -2.65), mira=(1.3, 1.1, -1.9), fov=lerp(46, 32, k))
        luces = luces_base(extra=[Luz((1.3, 2.2, -2.2), FLUOR, 3.0, fuerza=0.8)])
        img = etiquetas(esc.render(cam, luces), esc, cam)
        return aclarar(img, 1.2, 0.88), dict(grain=7)
    img = _fondo(t)
    cuaderno(img, t, pagina=0, escala=lerp(0.92, 0.98, seg(t, corte, D)), cy=880)
    fl = max(0.0, 0.5 - (t - corte) / 0.3)
    return img, dict(grain=7, flash=((255, 255, 255), fl))

# ---------- 4. noches: las páginas pasan; cada noche, fechada en 1986 ----------
def noches(t, D, fi):
    img = _fondo(t)
    n = len(G.NOCHES)
    i = min(n - 1, int(t / (D / n)))
    tl = t - i * D / n
    fecha, linea = G.NOCHES[i]
    partes = [x.strip() + ("." if not x.strip().endswith(".") else "") for x in linea.split(". ")]
    pagina(img, partes, fecha=fecha, p=None, cy=930, escala=1.0, pluma=False, t=t, size=80)
    d = ImageDraw.Draw(img)
    if tl < 0.12:                                     # la página pasando
        d.polygon([(W / 2 - 450 + 900 * tl / 0.12, 450), (W / 2 + 450, 440), (W / 2 + 450, 1420), (W / 2 - 450 + 900 * tl / 0.12, 1410)], fill=(200, 194, 172))
    # el año, marcado en rojo para que se vea
    ya = seg(t, D * 0.45, D * 0.6)
    if ya > 0:
        d.ellipse((780, 470, 985, 595), outline=(220, 30, 30), width=int(9 * ya) + 1)
    return img, dict(grain=7, tint=((255, 0, 30), 0.08 * seg(t, D * 0.5, D)))

# ---------- 5. sola: aparece una línea nueva, sin nadie que escriba ----------
def sola(t, D, fi):
    img = _fondo(t)
    p = 2.0 + seg(t, D * 0.25, D * 0.85)
    k = ease(seg(t, 0, D))
    pagina(img, G.PAG_HOY, fecha=G.HOY, p=p, cy=960, escala=lerp(1.0, 1.08, k), t=t)
    return img, dict(grain=8, tint=((255, 0, 30), 0.1 * seg(t, D * 0.6, D)))

# ---------- 6. cam: CAM 1 — no estoy leyendo; estoy escribiendo ----------
def cam(t, D, fi):
    esc = mundo(t)
    cuaderno3d_abierto(esc, *LIB)
    escribe = math.sin(t * 9)
    p = pose(body=14, head=24, a1u=40, a1l=70, a2u=lerp(62, 70, 0.5 + 0.5 * escribe), a2l=lerp(48, 56, 0.5 + 0.5 * escribe))
    empleado(esc, p, x=1.25, z=-2.55, yaw=0.0)
    boligrafo3d(esc, 1.18 + 0.02 * escribe, 1.17, -1.98, yaw=0.6, inclina=-0.7)
    k = ease(seg(t, 0, D))
    camara = Camara(ojo=(-0.6, 2.8, -0.3), mira=(1.25, 1.2, -2.3), fov=lerp(52, 40, k))
    img = esc.render(camara, luces_base())
    img = cctv(img, 1, f"03:{14 + int(t / 2):02d}:{int(t * 7) % 60:02d}")
    return img, dict(grain=10, glitch=0.3 if t < 0.15 or fi % 23 < 2 else 0.0)

# ---------- 7. giro: la última línea, aún húmeda ----------
def giro(t, D, fi):
    img = _fondo(t)
    p = 1.0 + 2.0 * seg(t, D * 0.1, D * 0.75)
    k = ease(seg(t, 0, D))
    pagina(img, G.PAG_FIN, fecha=G.HOY, p=p, cy=930, escala=lerp(1.0, 1.1, k), humeda=2 if p > 2.2 else (1 if p > 1.3 else None), t=t)
    return img, dict(grain=7, tint=((255, 0, 30), 0.14 * seg(t, D * 0.7, D)))

# ---------- 8. final: la carretera; a lo lejos, los faros de un camión. Tarjeta REGLA 7 ----------
def final(t, D, fi):
    a = ease(seg(t, 0, D))
    esc = mundo(t)
    M = camion(esc, lerp(-17, -11, a), 18.0, yaw=math.pi / 2, faros=1.0)
    camara = Camara(ojo=(-2.5, 1.7, 11.0), mira=(-11, 1.8, 18.5), fov=52)
    faros_ = [tuple((M @ np.array([sx * 0.82, 0.95, 3.62, 1.0]))[:3]) for sx in (-1, 1)]
    luces = luces_base(extra=[Luz((f[0] + 1.5, 1.0, f[2]), (255, 248, 210), 9.0, fuerza=1.0) for f in faros_[:1]])
    img = aclarar(esc.render(camara, luces), 1.15, 0.9)
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
    for f in faros_:                                  # los faros del camión, atravesando la niebla
        q = proyectar(camara, f)
        if q:
            for r, al in ((140, 50), (70, 110), (26, 255)): dc.ellipse((q[0] - r, q[1] - r * 0.7, q[0] + r, q[1] + r * 0.7), fill=(255, 246, 210, al))
    img.paste(capa.filter(ImageFilter.GaussianBlur(8)), (0, 0), capa.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.15, 0.5))
    d.rectangle((0, 300, W, 840), fill=(0, 0, 0))
    d.text((W / 2, 410), f"{tr('REGLA')} 7", font=font(int(150 * p) + 1), fill=(230, 40, 40), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    regla = tr("NO LEAS LO QUE NO HAYAS ESCRITO")
    fs = 70
    while d.textlength(regla, font=font(fs)) > W - 120 and fs > 30: fs -= 2
    d.text((W / 2, 580), regla, font=font(fs), fill=(240, 240, 230), anchor="mm")
    q = ease_back(seg(t, D * 0.55, D * 0.75))
    if q > 0:
        d.rounded_rectangle((200, 700, 880, 800), 24, fill=(200, 30, 30))
        d.text((W / 2, 750), tr("MAÑANA: REGLA 8"), font=font(int(56 * q) + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=9, glitch=0.25 if fi % 11 < 2 else 0.0)

ESCENA_FN = dict(arranque=arranque, premisa=premisa, abro=abro, noches=noches, sola=sola, cam=cam, giro=giro, final=final)
PAUSA = dict(arranque=0.4, premisa=0.5, abro=0.5, noches=0.6, sola=0.6, cam=0.7, giro=0.9, final=1.8)
