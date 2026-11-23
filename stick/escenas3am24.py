"""Si oyes esto a las 3AM — 24: "La foto de la puerta". Tu timbre con cámara te avisó a las tres: alguien en tu puerta.
Abres la grabación: una figura pálida, de pie en el porche, mira fijo al objetivo sin moverse (en infrarrojo los ojos le brillan).
Adelantas: 3:10, 3:30, 3:47, sigue ahí. A las 3:48 el porche está vacío y tu puerta, abierta. Miras la hora del móvil: 3:48.
No se fue: entró. Sube la escalera y abre la puerta de tu cuarto. "Te vi mirándome".
Piezas nuevas reutilizables: feed (imagen de cámara de timbre en infrarrojo, con ojo de pez, hora y REC/EN DIRECTO; modos
'el', 'vacio', con zoom digital), app_timbre (móvil a pantalla completa con la app del timbre: vídeo, línea de tiempo y
controles), aviso_timbre (pantalla de bloqueo con la notificación y la miniatura), VISITA + visita_lado (la figura pálida
y altísima de lado, andando), ojos_ir (los dos brillos de los ojos, pintados encima de la luz), reloj_hora, cuarto_puerta
(tu cuarto con la cama alta, la mesilla con el reloj y la puerta que se abre con la cara asomando)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, escalera_casa, CASA_A, CASA_B
from escenas3am2 import cara_palida, dedos, PIEL
from escenas3am3 import paredes, PISO
from escenas3am5 import _osc, cama_alta, manta, COLCHON
from escenas3am21 import tu_en_cama, _pega_foto

ROJO = (255, 40, 40)
AZUL = (150, 200, 255)
LUNA = (170, 190, 255)
VISITA = Fig(shirt=PIEL, limb=PIEL, scale=1.45)
PX, PY = 540, 820                      # centro del móvil
FX0, FY0, FW, FH = PX - 216, PY - 300, 432, 324   # el vídeo dentro del móvil (4:3)
PUERTA_X0, PUERTA_X1 = 960, 1200       # puerta de tu cuarto
_BG = {}
def fondo(k="a"):
    if k not in _BG:
        _BG[k] = {"a": gradient(CASA_A, CASA_B), "m": gradient((12, 12, 16), (4, 4, 6)), "p": gradient((20, 24, 22), (8, 10, 9))}[k]
    return _BG[k]

# ---------- la cámara del timbre ----------
def _porche(modo):
    """el porche visto por la cámara del timbre (mundo: 1080 de ancho, de y=555 a 1365)"""
    F = Frame(fondo("p"), dict(x=540, y=960, z=1.0))
    F.rect(-100, 400, 1200, 840, fill=(26, 30, 28))                                             # noche, jardín
    for i, (x, h) in enumerate(((120, 120), (300, 90), (760, 110), (980, 140))):                 # setos
        F.ellipse((x, 840 - h * 0.4), 150, h, fill=(44, 50, 46))
    F.rect(470, 700, 610, 840, fill=(36, 40, 38)); F.line([(470, 700), (610, 700)], (70, 76, 72), 6)   # verja
    for x in range(480, 610, 22): F.line([(x, 700), (x, 840)], (70, 76, 72), 4)
    F.line([(870, 840), (870, 600)], (60, 64, 62), 8); F.circle((870, 600), 18, fill=(230, 236, 232))  # farola lejana
    F.poly([(-100, 1400), (1200, 1400), (1200, 840), (-100, 840)], fill=(96, 100, 98))           # suelo del porche
    for k in range(-6, 8):                                                                        # baldosas en perspectiva
        F.line([(540 + k * 60, 840), (540 + k * 260, 1400)], (76, 80, 78), 4)
    for y in (880, 940, 1020, 1120, 1250): F.line([(-100, y), (1200, y)], (76, 80, 78), 4)
    F.poly([(330, 1290), (750, 1290), (800, 1400), (280, 1400)], fill=(62, 58, 54))              # felpudo
    if modo == "vacio":                                                                           # la puerta, abierta hacia dentro
        F.poly([(-100, 500), (110, 560), (110, 1300), (-100, 1400)], fill=(6, 6, 7))
        F.poly([(-100, 500), (20, 535), (20, 1330), (-100, 1400)], fill=(70, 66, 60))
        F.line([(110, 560), (110, 1300)], (120, 120, 116), 6)
        for i in range(5):                                                                        # huellas que entran
            x, y = 600 - i * 115, 1110 + i * 22 * (1 if i % 2 else 0.6)
            F.ellipse((x, y), 26, 13, fill=(46, 48, 46)); F.ellipse((x - 26, y + 2), 13, 9, fill=(46, 48, 46))
    else:
        F.poly([(-100, 500), (110, 560), (110, 1300), (-100, 1400)], fill=(70, 66, 60), outline=(40, 38, 34), w=5)
    ojos = []
    if modo == "el":                                                                              # la figura, mirando arriba
        x, piso = 560, 1170
        F.ellipse((x, piso + 6), 120, 24, fill=(70, 74, 72))
        F.poly([(x - 70, 860), (x + 70, 860), (x + 60, piso - 160), (x - 60, piso - 160)], fill=(208, 212, 210))   # torso
        for s_ in (-1, 1):
            F.line([(x + s_ * 70, 870), (x + s_ * 92, 1060), (x + s_ * 96, 1230)], (190, 194, 192), 30)   # brazos larguísimos
            F.line([(x + s_ * 26, piso - 160), (x + s_ * 34, piso)], (190, 194, 192), 34)          # piernas
        cara_palida(F, (x, 770), 70, abre=0.25)
        ojos = [(x - 21, 768), (x + 21, 768)]
        img = F.finish()
    else:
        img = F.finish()
    a = np.asarray(img, np.float32)
    g = a @ np.array([0.3, 0.59, 0.11], np.float32)
    g = np.clip((g - 20) * 1.35, 0, 255)
    a = np.stack([g * 0.82, g * 1.0, g * 0.86], -1)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if ojos:                                                                                      # ojos que brillan en infrarrojo
        gl = Image.new("L", img.size, 0); d = ImageDraw.Draw(gl)
        for ex, ey in ojos:
            px, py = F.P(ex, ey); px, py = px / S, py / S
            d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=255)
        halo = gl.filter(ImageFilter.GaussianBlur(9))
        k = (np.asarray(halo, np.float32) * 2.2 + np.asarray(gl, np.float32))[..., None] / 255
        img = Image.fromarray(np.clip(np.asarray(img, np.float32) * (1 - np.minimum(k, 1)) + 255 * np.minimum(k, 1), 0, 255).astype(np.uint8))
    return img.crop((0, 555, 1080, 1365))

_MAP = {}
def _ojo_pez(img):
    w, h = img.size
    if (w, h) not in _MAP:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        u, v = (xx - w / 2) / (w / 2), (yy - h / 2) / (w / 2)
        r2 = u * u + v * v
        f = 0.78 + 0.3 * r2
        sx, sy = np.clip(u * f * w / 2 + w / 2, 0, w - 1).astype(np.int32), np.clip(v * f * w / 2 + h / 2, 0, h - 1).astype(np.int32)
        vig = np.clip(1.25 - 0.75 * r2, 0, 1)[..., None]
        _MAP[(w, h)] = (sx, sy, vig)
    sx, sy, vig = _MAP[(w, h)]
    a = np.asarray(img, np.float32)[sy, sx] * vig
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

_FEED = {}
def feed(modo, hora, t=0.0, zoom=1.0, foco=(540, 230), rec="rec", ff=""):
    """imagen (1080x810) de la cámara del timbre. modo 'el' | 'vacio'; hora: '03:00:14'; zoom digital hacia foco;
    rec: 'rec' (grabación) | 'vivo' (EN DIRECTO); ff: texto de avance rápido ('>> x60')"""
    key = (modo, round(zoom, 2), foco)
    if key not in _FEED:
        if len(_FEED) > 40: _FEED.clear()
        base = _porche(modo)
        if zoom > 1.001:
            w, h = 1080 / zoom, 810 / zoom
            x0 = clamp(foco[0] - w / 2, 0, 1080 - w); y0 = clamp(foco[1] - h / 2, 0, 810 - h)
            base = base.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((1080, 810), Image.BILINEAR)
        _FEED[key] = _ojo_pez(base.resize((540, 405)).resize((1080, 810), Image.BILINEAR))
    img = _FEED[key].copy()
    a = np.asarray(img, np.float32)
    rng = np.random.default_rng(int(t * 30) % 997)
    a = a + rng.normal(0, 9, a.shape[:2])[..., None]
    a[::4] *= 0.86                                                                                # líneas de barrido
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.text((44, 40), hora, font=font(64), fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
    d.text((44, 740), tr("PUERTA PRINCIPAL"), font=font(40), fill=(230, 230, 230), stroke_width=3, stroke_fill=(0, 0, 0))
    if rec == "vivo":
        if int(t * 3) % 2 == 0: d.ellipse((760, 52, 796, 88), fill=ROJO)
        d.text((812, 44), tr("EN DIRECTO"), font=font(48), fill=ROJO, stroke_width=3, stroke_fill=(0, 0, 0))
    else:
        d.ellipse((860, 52, 896, 88), fill=(255, 255, 255) if int(t * 2) % 2 else (120, 120, 120))
        d.text((910, 44), "REC", font=font(48), fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
    if ff:
        d.text((1036, 760), ff, font=font(64), fill=(255, 255, 255), anchor="rs", stroke_width=4, stroke_fill=(0, 0, 0))
    return img

def _hhmm(seg_totales):
    m, s = divmod(int(seg_totales), 60)
    return f"03:{m:02d}:{s:02d}"

# ---------- el móvil ----------
def _movil(F, t, vib=0.0, mano=True):
    cx, cy = PX + noise(t * 60) * 12 * vib, PY
    if mano:
        F.line([(150, 1800), (370, 1300)], TU.shirt, 84); F.circle((430, 1240), 64, fill=(240, 232, 222))
    F.rect(cx - 250, cy - 440, cx + 250, cy + 440, fill=(20, 20, 26), outline=(90, 90, 100), w=8)
    F.rect(cx - 226, cy - 414, cx + 226, cy + 414, fill=(10, 12, 18))
    F.rect(cx + 150, cy - 396, cx + 196, cy - 374, outline=(200, 200, 210), w=3)                 # batería
    F.rect(cx + 154, cy - 392, cx + 176, cy - 378, fill=(200, 200, 210))
    return cx, cy

def aviso_timbre(F, t, foto, vib=0.0):
    """pantalla de bloqueo con la notificación del timbre y la miniatura del vídeo"""
    cx, cy = _movil(F, t, vib)
    F.rect(cx - 226, cy - 414, cx + 226, cy + 414, fill=(14, 18, 34))
    F.rect(cx - 206, cy - 300, cx + 206, cy + 200, fill=(36, 38, 48), outline=(70, 72, 86), w=3)
    F.rect(cx - 190, cy - 284, cx - 150, cy - 244, fill=(230, 60, 60))                           # icono del timbre
    F.circle((cx - 170, cy - 264), 10, fill=(255, 255, 255))
    F.text((cx - 50, cy - 264), tr("TIMBRE"), 30, (220, 220, 230))
    F.text((cx + 150, cy - 264), "3:00", 30, ROJO)
    F.text((cx, cy - 210), tr("Hay alguien en tu puerta"), 32, (250, 250, 255))
    _pega_foto(F, foto.resize((540, 405)), cx - 190, cy - 170, 380, 285)
    return (cx, cy - 30)

def app_timbre(F, t, foto, prog=0.0, etiqueta="", vivo=False, hora_movil=None, vib=0.0, controles=1.0):
    """la app del timbre: vídeo arriba, estado, línea de tiempo (prog 0-1) y controles"""
    cx, cy = _movil(F, t, vib)
    if hora_movil:
        F.text((cx - 150, cy - 385), hora_movil, 36, ROJO)
    F.text((cx, cy - 335), tr("TIMBRE · ENTRADA"), 30, (200, 204, 214))
    _pega_foto(F, foto, FX0, FY0, FW, FH)
    F.rect(FX0, FY0, FX0 + FW, FY0 + FH, outline=(70, 72, 86), w=3)
    if etiqueta:
        F.text((cx, cy + 90), etiqueta, 40, ROJO if vivo else (230, 230, 240))
    y = cy + 180
    F.line([(cx - 190, y), (cx + 190, y)], (70, 72, 86), 10)
    F.line([(cx - 190, y), (cx - 190 + 380 * prog, y)], (230, 60, 60), 10)
    F.circle((cx - 190 + 380 * prog, y), 18, fill=(255, 255, 255))
    F.text((cx - 175, y + 50), "3:00", 28, (170, 170, 180))
    F.text((cx + 160, y + 50), tr("AHORA"), 28, ROJO if vivo else (170, 170, 180))
    if controles > 0:
        yc = cy + 310
        for s_ in (-1, 1):                                                                        # ⏪ ⏩
            for k in (0, 1):
                bx = cx + s_ * (130 + k * 34)
                F.poly([(bx - s_ * 20, yc - 26), (bx + s_ * 20, yc), (bx - s_ * 20, yc + 26)], fill=(220, 220, 230))
        F.poly([(cx - 18, yc - 30), (cx + 26, yc), (cx - 18, yc + 30)], fill=(220, 220, 230))
    return (cx, cy - 140)

def reloj_hora(F, cx, cy, s=1.0, txt="3:48"):
    F.rect(cx - 150 * s, cy - 70 * s, cx + 150 * s, cy + 70 * s, fill=(14, 14, 16), outline=(60, 60, 66), w=6 * s)
    F.text((cx, cy + 4 * s), txt, 108 * s, ROJO, stroke=3 * s, scol=(90, 0, 0))

def ojos_ir(img, F, pts, k=1.0, r=5):
    """dos brillos blancos con halo, pintados después de la luz (no se oscurecen)"""
    if k <= 0: return img
    gl = Image.new("L", img.size, 0); d = ImageDraw.Draw(gl)
    for x, y in pts:
        px, py = F.P(x, y); px, py = px / S, py / S; rr = r * F.z
        d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=int(255 * k))
    m = (np.asarray(gl.filter(ImageFilter.GaussianBlur(4 * F.z + 2)), np.float32) * 1.8 + np.asarray(gl, np.float32))[..., None] / 255
    m = np.minimum(m, 1)
    a = np.asarray(img, np.float32) * (1 - m) + np.array((240, 248, 255), np.float32) * m
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

# ---------- la figura ----------
def visita_lado(F, t, x, y, f=-1, fase=0.0, cara=0.0):
    """la figura pálida y altísima de lado, andando rígida (f=-1 mira a la izquierda). cara: vuelve la cara hacia ti.
    Devuelve los ojos"""
    ph = math.sin(fase * 2 * math.pi)
    p = pose(body=8, head=6, a1u=8 + 6 * ph, a1l=4, a2u=-8 - 6 * ph, a2l=4,
             l1u=22 * ph, l1l=-6 - 14 * max(0, -ph), l2u=-22 * ph, l2l=-6 - 14 * max(0, ph))
    J = VISITA.draw(F, p, x, y, f=f, face="closed", t=t, stretch=1.15)
    hx, hy = J["head"]; r = L["head"] * VISITA.scale
    s = -f
    F.poly([(hx + s * r * 1.1, hy - r * 0.9), (hx - s * r * 0.3, hy - r * 1.15), (hx - s * r * 0.2, hy + r * 0.2),
            (hx + s * r * 0.7, hy + r * 2.4), (hx + s * r * 1.3, hy + r * 2.0)], fill=(12, 12, 16))
    if cara > 0:
        cara_palida(F, (hx, hy), r * lerp(0.7, 1.05, cara), abre=0.3)
        rr = r * lerp(0.7, 1.05, cara)
        return [(hx - 0.3 * rr, hy), (hx + 0.3 * rr, hy)]
    return [(hx + f * r * 0.55, hy - r * 0.05)]

def cuarto_puerta(F, t, abre=0.0, cara=0.0, tu_face="scared", sienta=0.6):
    """tu cuarto: cama alta, mesilla con el reloj en 3:48 y la puerta a la derecha, que se abre hacia dentro.
    cara 0-1: la cara asoma por la rendija, muy arriba, con los dedos en el canto. Devuelve (ojos, cabeza tuya, móvil)"""
    paredes(F, col=(26, 28, 44))
    F.rect(470, 560, 690, 800, fill=(10, 14, 30), outline=(70, 66, 80), w=12)                     # ventana con luna
    F.line([(580, 560), (580, 800)], (70, 66, 80), 8); F.circle((640, 610), 20, fill=(200, 210, 240))
    F.rect(760, PISO - 190, 890, PISO, fill=(70, 54, 44), outline=(40, 30, 24), w=4)              # mesilla
    reloj_hora(F, 825, PISO - 222, 0.3)
    F.rect(PUERTA_X0 - 24, PISO - 590, PUERTA_X1 + 24, PISO, fill=(46, 38, 32))                   # marco
    F.rect(PUERTA_X0, PISO - 566, PUERTA_X1, PISO, fill=(3, 3, 5))                                # pasillo a oscuras
    gap = 150 * ease(abre)
    ojos = []
    if cara > 0 and gap > 20:
        hx, hy = PUERTA_X0 + gap * 0.5, PISO - 500 + 30 * (1 - ease(cara))
        F.rect(hx - 50, hy + 60, hx + 50, PISO, fill=_osc(PIEL, 0.35))
        cara_palida(F, (hx, hy), 44, abre=0.3 + 0.2 * cara)
        ojos = [(hx - 13, hy), (hx + 13, hy)]
        for k, yy in enumerate((hy + 120, hy + 170)):
            dedos(F, (PUERTA_X0 + gap + 2, yy), 0, n=4, L_=lerp(10, 46, ease(cara)), w=8)
    ex = PUERTA_X0 + gap
    F.poly([(ex, PISO - 566), (PUERTA_X1, PISO - 566), (PUERTA_X1, PISO), (ex, PISO)], fill=(84, 66, 52), outline=(40, 30, 24), w=4)
    F.circle((ex + 26, PISO - 280), 10, fill=(196, 168, 96))
    cama_alta(F, t=t)
    J = tu_en_cama(F, t, face=tu_face, sienta=sienta)
    return ojos, J["head"], J["a1h"]

# ---------- escenas ----------
def aviso(t, D, fi):
    """primer fotograma: la miniatura de la notificación, muy cerca: la figura en infrarrojo con los ojos brillando.
    La cámara se aleja y se ve el móvil, que vibra, con el aviso del timbre a las 3:00"""
    k = ease(seg(t, D * 0.15, D * 0.75))
    F = Frame(fondo("m"), dict(x=PX, y=lerp(PY - 40, PY - 40, k), z=lerp(2.5, 1.05, k)))
    c = aviso_timbre(F, t, feed("el", "03:00:00", t), vib=1.0 - seg(t, D * 0.3, D * 0.5))
    img = iluminar(F.finish(), F, [], glows=[(c, 560, 1.0)], amb=0.3, warm=AZUL)
    return img, dict(grain=8, flash=(ROJO, 0.35 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.05))

def video(t, D, fi):
    """abres la grabación: el vídeo a pantalla casi completa; la figura, quieta, mirando al objetivo"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo("m"), dict(x=PX, y=lerp(FY0 + FH / 2 + 20, FY0 + FH / 2, k), z=lerp(2.2, 2.45, k)))
    c = app_timbre(F, t, feed("el", _hhmm(14 + t), t), prog=0.01 + 0.005 * t)
    img = iluminar(F.finish(), F, [], glows=[(c, 600, 1.0)], amb=0.3, warm=AZUL)
    return img, dict(grain=8, tint=((255, 0, 30), 0.04 + 0.06 * seg(t, D * 0.6, D)))

def rapido(t, D, fi):
    """adelantas: la hora del vídeo corre (3:10… 3:30) y la figura no se ha movido ni un milímetro"""
    k = ease(seg(t, 0, D * 0.4))
    F = Frame(fondo("m"), dict(x=PX, y=lerp(FY0 + FH / 2, PY + 60, k), z=lerp(2.45, 0.95, k)))
    mins = lerp(3, 10, seg(t, 0.3, 1.3)) + lerp(0, 20, seg(t, 1.3, 2.6)) + lerp(0, 6, seg(t, 2.6, D))
    c = app_timbre(F, t, feed("el", _hhmm(mins * 60 + (t * 997) % 60), t, ff=">> x60"), prog=mins / 48, etiqueta=tr("GRABACIÓN"))
    img = iluminar(F.finish(), F, [], glows=[(c, 600, 1.0)], amb=0.3, warm=AZUL)
    return img, dict(grain=9, glitch=0.12 if fi % 7 == 0 else 0.0, tint=((255, 0, 30), 0.06))

def cuarenta(t, D, fi):
    """3:47: zoom digital hacia su cara. Los ojos blancos, fijos en el objetivo"""
    z = lerp(1.6, 2.6, ease(seg(t, 0, D * 0.9)))
    F = Frame(fondo("m"), dict(x=PX, y=FY0 + FH / 2, z=2.5))
    c = app_timbre(F, t, feed("el", _hhmm(47 * 60 + 2 + t), t, zoom=round(z * 10) / 10, foco=(560, 215)), prog=47 / 48)
    img = iluminar(F.finish(), F, [], glows=[(c, 600, 1.0)], amb=0.3, warm=AZUL)
    return img, dict(grain=10, tint=((255, 0, 30), 0.1 + 0.08 * seg(t, D * 0.5, D)), glitch=0.25 if 0 < t - D * 0.85 < 0.2 else 0.0)

def abierta(t, D, fi):
    """3:48: corte. El porche, vacío. Tu puerta, abierta hacia dentro, y unas huellas que solo entran"""
    k = ease(seg(t, D * 0.3, D))
    F = Frame(fondo("m"), dict(x=lerp(PX, PX - 80, k), y=FY0 + FH / 2 + lerp(0, 30, k), z=lerp(2.45, 2.7, k)))
    c = app_timbre(F, t, feed("vacio", _hhmm(48 * 60 + 2 + t), t), prog=0.995)
    img = iluminar(F.finish(), F, [], glows=[(c, 600, 1.0)], amb=0.3, warm=AZUL)
    return img, dict(grain=10, flash=((255, 255, 255), 0.5 * (1 - seg(t, 0, 0.25))), glitch=0.35 if t < 0.2 else 0.0,
                     tint=((255, 0, 30), 0.1))

def hora(t, D, fi):
    """la cámara se aleja: la línea de tiempo llega al final, pone EN DIRECTO; y la hora del móvil, arriba: 3:48"""
    k = ease(seg(t, 0, D * 0.35))
    k2 = ease(seg(t, D * 0.55, D * 0.75))
    zx, zy = PX - 150, PY - 385
    cam = dict(x=lerp(PX, PX, k) if k2 == 0 else lerp(PX, zx + 60, k2), y=lerp(FY0 + FH / 2, PY + 60, k) if k2 == 0 else lerp(PY + 60, zy + 60, k2),
               z=lerp(2.45, 0.95, k) if k2 == 0 else lerp(0.95, 2.6, k2))
    F = Frame(fondo("m"), cam)
    vivo = t > D * 0.3
    c = app_timbre(F, t, feed("vacio", _hhmm(48 * 60 + 5 + t), t, rec="vivo" if vivo else "rec"), prog=1.0,
                   etiqueta="● " + tr("EN DIRECTO") if vivo else tr("GRABACIÓN"), vivo=vivo,
                   hora_movil="3:48" if t > D * 0.5 else None)
    img = iluminar(F.finish(), F, [], glows=[(c, 600, 1.0)], amb=0.3, warm=AZUL)
    return img, dict(grain=9, tint=((255, 0, 30), 0.06 + 0.14 * k2), flash=(ROJO, 0.35 * max(0, 1 - abs(t - D * 0.62) / 0.15)))

def escalera(t, D, fi):
    """la escalera de casa: abajo, la puerta de la calle abierta a la noche; la figura sube, rígida, escalón a escalón"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(700, 560, k), y=lerp(1000, 940, k), z=lerp(1.0, 1.25, k)))
    path = escalera_casa(F)
    F.rect(1040, 700, 1260, 1300, fill=(46, 38, 32))                                              # puerta de la calle, abierta
    F.rect(1060, 720, 1240, 1300, fill=(16, 22, 40))
    F.circle((1180, 790), 14, fill=(200, 210, 240))
    F.poly([(1060, 720), (1100, 700), (1100, 1320), (1060, 1300)], fill=(80, 56, 42), outline=(36, 24, 18), w=4)
    F.rect(-600, 300, 120, 700, fill=(28, 30, 46))                                                # arriba: el pasillo
    F.rect(-120, 160, 80, 700, fill=(62, 50, 42), outline=(36, 26, 20), w=5)                       # tu puerta, arriba
    F.rect(-120, 692, 80, 700, fill=_osc(AZUL, 0.6))                                               # la luz de tu móvil, debajo
    u = lerp(0.92, 0.55, seg(t, 0.2, D))
    x, y = path(u)
    gira = ease(seg(t, D * 0.8, D * 0.92))
    ojos = visita_lado(F, t, x, y, f=-1, fase=u * 6, cara=gira)
    img = iluminar(F.finish(), F, [], glows=[((1150, 1000), 300, 0.5), ((-20, 700), 200, 0.5), ((x, y - 300), 300, 0.35)],
                   amb=0.2, warm=LUNA)
    img = ojos_ir(img, F, ojos, k=0.9, r=4 + 2 * gira)
    return img, dict(grain=10, tint=((255, 0, 30), 0.08 + 0.12 * gira), flash=(ROJO, 0.3 * max(0, 1 - abs(t - D * 0.86) / 0.15)))

def cuarto(t, D, fi):
    """tu cuarto: tú sentado en la cama con el móvil; la puerta se abre despacio y, muy arriba, asoma su cara con los ojos
    brillando"""
    abre = seg(t, D * 0.05, D * 0.5)
    cara = seg(t, D * 0.35, D * 0.55)
    k = ease(seg(t, 0, D))
    hit = seg(t, D * 0.5, D * 0.55)
    F = Frame(fondo(), dict(x=lerp(700, 940, k), y=lerp(1000, 860, k), z=lerp(1.05, 1.7, k), sx=noise(t * 40) * 8 * hit * (1 - seg(t, D * 0.6, D * 0.75))))
    ojos, cab, mov = cuarto_puerta(F, t, abre=abre, cara=cara)
    img = iluminar(F.finish(), F, [], glows=[(mov, 260, 1.0), (cab, 160, 0.4), ((825, PISO - 222), 180, 0.6), ((640, 610), 200, 0.4),
                                            ((PUERTA_X0 + 60, PISO - 480), 200, 0.3 * cara)], amb=0.24, warm=AZUL)
    img = ojos_ir(img, F, ojos, k=cara, r=4.5)
    return img, dict(grain=10, tint=((255, 0, 30), 0.1 + 0.12 * hit), flash=(ROJO, 0.35 * max(0, 1 - abs(t - D * 0.52) / 0.15)),
                     glitch=0.3 if 0 < t - D * 0.5 < 0.25 and fi % 2 else 0.0)

def final(t, D, fi):
    """plano general: la puerta abierta, la cara arriba y tú en la cama. La regla"""
    k = ease(seg(t, 0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(940, 700, k), y=lerp(860, 1000, k), z=lerp(1.7, 1.0, k)))
    ojos, cab, mov = cuarto_puerta(F, t, abre=1.0, cara=1.0)
    img = iluminar(F.finish(), F, [], glows=[(mov, 260, 1.0), (cab, 160, 0.4), ((825, PISO - 222), 180, 0.6), ((640, 610), 200, 0.4),
                                            ((PUERTA_X0 + 60, PISO - 480), 200, 0.3)], amb=0.24, warm=AZUL)
    img = ojos_ir(img, F, ojos, k=0.8 + 0.2 * math.sin(t * 6), r=4.5)
    pp = ease_back(seg(t, D * 0.42, D * 0.52)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 130, 1040, 640), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 HAY ALGUIEN"), 200, 62, (255, 255, 255)), (tr("EN TU TIMBRE…"), 280, 62, (255, 255, 255)),
                                 (tr("NO MIRES A QUÉ"), 420, 100, (255, 40, 50)), (tr("HORA SE FUE"), 545, 100, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 680, 850, 770), 26, fill=(230, 30, 50))
        d.text((540, 725), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.22 * pp if pp > 0 else 0.08), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(aviso=aviso, video=video, rapido=rapido, cuarenta=cuarenta, abierta=abierta, hora=hora, escalera=escalera,
                 cuarto=cuarto, final=final)
PAUSA = dict(aviso=0.5, video=0.5, rapido=0.4, cuarenta=0.6, abierta=0.7, hora=0.7, escalera=0.5, cuarto=0.8, final=2.4)
