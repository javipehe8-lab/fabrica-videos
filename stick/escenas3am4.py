"""Si oyes esto a las 3AM — 4: "La mirilla". Habitación de hotel de noche, la puerta con la mirilla, la vista a través
de la mirilla (todo rojo: un iris pegado al cristal), el corte transversal puerta/pasillo con el huésped de enfrente
y la rendija bajo la puerta. Piezas nuevas reutilizables: vista_mirilla (círculo de mirilla con cualquier contenido),
ojo (iris rojo con párpados que parpadean), pasillo_hotel, HUESPED, cabeza_huesped, telefono_hotel."""
import math
from PIL import Image, ImageDraw, ImageFilter
from motor import *
from escenas2 import big
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am, CASA_A, CASA_B
from escenas3am2 import PIEL
from escenas3am3 import paredes, puerta_calle, PISO, DX0, DX1, RELLANO, LATON

ROJO = (196, 14, 24)
MX, MY = 700, 1040                    # mirilla de tu puerta (puerta_calle)
HUESPED = Fig(shirt=(214, 212, 204), limb=PIEL, scale=1.45)       # albornoz blanco del hotel, piel gris
_BG = {}
def fondo(k="a"):
    if k not in _BG: _BG[k] = gradient(CASA_A, CASA_B) if k == "a" else gradient((10, 8, 8), (2, 2, 2))
    return _BG[k]

def cama_hotel(F, x0=-260, x1=330):
    F.rect(x0 - 20, PISO - 330, x0 + 30, PISO, fill=(70, 50, 40))                                  # cabecero
    F.rect(x0, PISO - 160, x1, PISO - 50, fill=(200, 196, 186)); F.rect(x0, PISO - 186, x1, PISO - 150, fill=(236, 232, 224))
    F.rect(x0 + 40, PISO - 210, x0 + 200, PISO - 176, fill=(246, 244, 238))                        # almohada
    F.rect(x1 - 200, PISO - 186, x1, PISO - 120, fill=(120, 40, 46))                               # pie de cama
    for lx in (x0 + 12, x1 - 12): F.line([(lx, PISO - 50), (lx, PISO)], (40, 32, 28), 10)

def telefono_hotel(F, x, y, colgado=True):
    F.rect(x - 52, y - 40, x + 52, y, fill=(26, 26, 30), outline=(70, 70, 76), w=3)
    F.rect(x - 30, y - 30, x + 30, y - 8, fill=(50, 50, 56))
    if colgado: F.rect(x - 60, y - 58, x + 60, y - 38, fill=(20, 20, 24))

def mesilla(F, x=420):
    F.rect(x - 75, PISO - 170, x + 75, PISO, fill=(84, 60, 44), outline=(40, 28, 20), w=4)
    F.line([(x - 60, PISO - 90), (x + 60, PISO - 90)], (50, 36, 26), 4)

def habitacion(F, rojo=0.0, pies=0.0, rellano=0.55, colgado=True):
    paredes(F, col=(34, 30, 40))
    for xx in range(-900, 2000, 90): F.line([(xx, -200), (xx, PISO - 40)], (38, 33, 45), 6)      # papel pintado
    puerta_calle(F, rellano=rellano, pies=pies)
    F.rect(670, 900, 730, 930, fill=LATON); F.text((700, 915), "214", 22, (40, 30, 20))
    if rojo > 0: F.circle((MX, MY), 5, fill=tuple(int(v * rojo) for v in (255, 30, 40)))
    cama_hotel(F); mesilla(F)
    reloj_3am(F, 420, PISO - 222, 0.32)
    telefono_hotel(F, 420 + 0, PISO - 170, colgado)

def ojo(F, c, R, close=0.0, pupila=0.3, mira=(0, 0), t=0.0, piel=PIEL):
    """ojo enorme: esclerótica gris, iris rojo de radio R con estrías, pupila negra; párpados (close 0-1)"""
    cx, cy = c; ex, ey = cx + mira[0] * R * 0.25, cy + mira[1] * R * 0.15
    Rx, Ry = R * 2.1, R * 1.25
    F.ellipse((cx, cy), Rx, Ry, fill=(196, 190, 182))
    for k in range(6):                                                      # venitas grises (sin sangre)
        a = k * 1.05 + 0.3; F.line([(cx + math.cos(a) * Rx * 0.9, cy + math.sin(a) * Ry * 0.85),
                                    (cx + math.cos(a + 0.12) * R * 1.3, cy + math.sin(a + 0.12) * R * 1.05)], (166, 150, 146), R * 0.02)
    F.circle((ex, ey), R * 1.02, fill=(60, 0, 4))
    F.circle((ex, ey), R, fill=ROJO)
    F.circle((ex, ey), R * 0.72, fill=(222, 30, 34))
    for k in range(36):
        a = k * math.tau / 36 + 0.05 * math.sin(k * 3.1)
        F.line([(ex + math.cos(a) * R * 0.3, ey + math.sin(a) * R * 0.3), (ex + math.cos(a) * R * 0.95, ey + math.sin(a) * R * 0.95)],
               (130, 4, 12) if k % 2 else (240, 60, 50), R * 0.025)
    F.circle((ex, ey), R * (0.2 + 0.25 * pupila), fill=(4, 2, 2))
    if R < 1000: F.ellipse((ex - R * 0.42, ey - R * 0.45), R * 0.16, R * 0.11, fill=(255, 236, 230))            # brillo húmedo
    h = Ry * (1 - ease(close))
    for s_ in (-1, 1):                                                       # párpados
        pts = [(cx + Rx * 1.6 * (i / 20 * 2 - 1), cy + s_ * h * math.sqrt(max(0, 1 - ((i / 20 * 2 - 1) * 1.6 * Rx / Rx) ** 2 / 2.56)))
               for i in range(21)]
        F.poly(pts + [(cx + Rx * 1.6, cy + s_ * Ry * 4), (cx - Rx * 1.6, cy + s_ * Ry * 4)], fill=piel)
        F.line(pts, (20, 18, 18), R * 0.05)

def pasillo_hotel(F, abierta=1.0):
    """pasillo visto por la mirilla: moqueta roja, paredes, la puerta 215 de enfrente (abierta y negra)"""
    F.rect(-400, -200, 1500, 2200, fill=(70, 50, 36))
    F.poly([(-400, 1700), (1500, 1700), (700, 1060), (380, 1060)], fill=(86, 20, 26))              # moqueta
    F.poly([(-400, 300), (1500, 300), (700, 760), (380, 760)], fill=(48, 36, 30))                  # techo
    F.rect(380, 760, 700, 1060, fill=(30, 22, 18))                                                 # fondo
    F.rect(300, 640, 780, 1300, fill=(54, 40, 30))
    F.rect(330, 680, 750, 1300, fill=(10, 8, 8) if abierta else (100, 70, 50))                    # puerta de enfrente
    F.rect(500, 600, 580, 630, fill=LATON); F.text((540, 615), "215", 22, (40, 30, 20))
    F.circle((540, 380), 40, fill=(255, 210, 140))

def vista_mirilla(dibuja, t, z=1.0, r=400, c=(540, 900), tinte=None):
    """dibuja(F) pinta el contenido en coordenadas de pantalla; se recorta en un círculo de mirilla con borde de latón"""
    F = Frame(fondo("b"), dict(x=540, y=900, z=z))
    dibuja(F)
    inner = F.finish()
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(6))
    out = Image.new("RGB", (W, H), (3, 3, 4)); out.paste(inner, (0, 0), m)
    # oscurecer bordes del círculo (efecto lente) y anillo de latón
    a = np.asarray(out, np.float32); yy, xx = np.mgrid[0:H, 0:W]
    d = np.hypot(xx - c[0], yy - c[1]) / r
    a *= np.clip(1.25 - d ** 3 * 0.7, 0, 1)[..., None]
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    dd = ImageDraw.Draw(out)
    dd.ellipse((c[0] - r - 18, c[1] - r - 18, c[0] + r + 18, c[1] + r + 18), outline=(120, 100, 56), width=26)
    return out

def _tu_cama(F, t, D, s):
    TU.draw(F, mix(pose(l1u=90, l2u=90, l1l=0, l2l=0, a1u=10), pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=40, a1l=30, a2u=-20), s),
            lerp(20, 120, s), lerp(PISO - 160, PISO - 150, s), f=1, rot=lerp(-90, 0, s), snap=False,
            face="closed" if s < 0.1 else ("scared" if s > 0.6 else "neutral"))

# ---------- escenas ----------
def pasos(t, D, fi):
    k = ease(seg(t, 0.0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(420, 330, k), y=lerp(PISO - 222, 1100, k), z=lerp(3.4, 1.45, k)))
    pies = seg(t, D * 0.55, D * 0.7)
    habitacion(F, pies=pies, rellano=0.55 + 0.25 * pies)
    _tu_cama(F, t, D, ease(seg(t, D * 0.6, D * 0.8)))
    img = iluminar(F.finish(), F, [], glows=[((420, PISO - 222), 200, 0.6), ((700, PISO), 330, 0.4 + 0.4 * pies)], amb=0.28, warm=(255, 120, 120))
    return img, dict(grain=9, flash=((255, 40, 40), 0.35 * (1 - seg(t, 0, 0.25))))

def mirilla(t, D, fi):
    cut = D * 0.5
    if t < cut:
        w = ease(seg(t, 0, cut * 0.8))
        F = Frame(fondo(), dict(x=lerp(480, 680, w), y=lerp(1080, 1050, w), z=lerp(1.2, 2.2, w)))
        habitacion(F, pies=1.0, rellano=0.8)
        TU.draw(F, walk(t, 0.6, 0.6) if w < 1 else pose(body=8, head=6, a1u=40, a1l=60), lerp(120, 650, w), PISO, f=1, face="scared")
        img = iluminar(F.finish(), F, [], glows=[((700, PISO), 330, 0.8), ((MX, MY), 160, 0.4)], amb=0.24, warm=RELLANO)
        return img, dict(grain=10)
    u = t - cut
    img = vista_mirilla(lambda F: ojo(F, (1000 + noise(t * 0.7) * 30, 1500), 1500, pupila=0.15), t, z=lerp(1.25, 1.15, seg(u, 0, D - cut)))
    return img, dict(grain=12, flash=((255, 0, 20), 0.6 * (1 - seg(u, 0, 0.3))))

def punto(t, D, fi):
    z = lerp(1.0, 1.25, ease(t / D))
    pu = 0.25 + 0.15 * math.sin(t * 2.2)
    img = vista_mirilla(lambda F: ojo(F, (540 + noise(t * 0.5, 3) * 40, 900 + noise(t * 0.5, 4) * 30), 520, pupila=pu), t, z=z)
    return img, dict(grain=12, tint=((255, 0, 30), 0.08))

def _tu_telefono(F, t, k):
    J = TU.draw(F, add(pose(body=-4, a1u=150, a1l=50, a2u=-10, a2l=20), jitter(t, 1.5 * k, 2)), 300, PISO, f=1, face="scared")
    hx, hy = J["a1h"]
    F.rect(hx - 34, hy - 12, hx + 34, hy + 12, fill=(20, 20, 24))
    F.line([(hx + 20, hy + 10), (hx + 50, hy + 90), (420, PISO - 190)], (20, 20, 24), 4)
    return J

def llamas(t, D, fi):
    F = Frame(fondo(), dict(x=lerp(380, 400, ease(t / D)), y=1080, z=lerp(1.9, 2.1, ease(t / D))))
    habitacion(F, pies=1.0, rellano=0.75, colgado=False)
    _tu_telefono(F, t, 0.3)
    img = iluminar(F.finish(), F, [], glows=[((420, PISO - 222), 200, 0.6), ((700, PISO), 300, 0.7)], amb=0.24, warm=(255, 140, 120))
    return img, dict(grain=10)

def recepcion(t, D, fi):
    k = ease(seg(t, D * 0.35, D))
    F = Frame(fondo(), dict(x=lerp(400, MX, k), y=lerp(1080, MY, k), z=lerp(2.1, 4.2, k)))
    rojo = 0.6 + 0.4 * (noise(t * 3) > -0.4)
    habitacion(F, pies=1.0, rellano=0.75, colgado=False, rojo=rojo)
    _tu_telefono(F, t, 1.0)
    img = iluminar(F.finish(), F, [], glows=[((700, PISO), 300, 0.7), ((MX, MY), 90, 0.9 * k)], amb=0.24, warm=(255, 140, 120))
    return img, dict(grain=10, tint=((255, 0, 30), 0.15 * k))

def cabeza_huesped(F, c, r, f=-1, brillo=1.0):
    """cabeza de perfil del huésped: gris, pelo negro y lacio, un ojo rojo enorme que brilla"""
    hx, hy = c
    F.ellipse((hx, hy + r * 0.1), r * 0.9, r * 1.25, fill=PIEL)
    F.d.chord([*F.P(hx - r, hy - r * 1.3), *F.P(hx + r, hy + r * 0.3)], 180, 360, fill=(16, 16, 18))
    F.poly([(hx - f * r * 0.1, hy - r * 1.1), (hx - f * r * 1.05, hy - r * 0.5), (hx - f * r * 1.0, hy + r * 1.6), (hx - f * r * 0.4, hy + r * 1.2)], fill=(16, 16, 18))
    ox = hx + f * r * 0.5
    F.ellipse((ox, hy), r * 0.38, r * 0.3, fill=(196, 190, 182))
    F.circle((ox + f * r * 0.06, hy), r * 0.24, fill=(int(255 * brillo), 30, 36)); F.circle((ox + f * r * 0.08, hy), r * 0.09, fill=(4, 2, 2))
    F.ellipse((hx + f * r * 0.55, hy + r * 0.8), r * 0.18, r * 0.06, fill=(30, 26, 26))           # boca: raja

def entiendes(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(540, 600, k), y=lerp(1000, 1030, k), z=lerp(1.0, 1.35, k)))
    F.rect(-900, -200, 540, PISO, fill=(26, 24, 34)); F.rect(560, -200, 2000, PISO, fill=(76, 52, 36))   # tu cuarto | pasillo
    F.rect(-900, PISO, 2000, 3000, fill=(14, 12, 16)); F.rect(560, PISO, 2000, 3000, fill=(70, 18, 22))
    for xx in range(600, 2000, 110): F.line([(xx, -200), (xx, PISO)], (84, 58, 40), 8)
    F.rect(520, 600, 580, PISO, fill=(92, 62, 44), outline=(40, 26, 18), w=4)                    # tu puerta, en corte
    F.rect(500, 560, 600, 600, fill=(40, 30, 24)); F.text((540, 470), tr("TU PUERTA"), 40, (220, 220, 230), stroke=4)
    # el huésped, inclinado, con el ojo pegado a la mirilla (la mirilla del corte está a la altura de su cabeza)
    p = add(pose(body=34, head=-26, a1u=-30, a1l=6, a2u=-40, a2l=8, l1u=-4, l1l=0, l2u=6, l2l=0), jitter(t, 0.6, 3))
    r = L["head"] * HUESPED.scale
    J0 = HUESPED.joints(p, 0, PISO, f=-1, stretch=1.25)
    J = HUESPED.draw(F, p, 588 + r * 0.95 - J0["head"][0], PISO, f=-1, face="closed", stretch=1.25)
    hx, hy = J["head"]
    sx, sy = J["sh"]; hpx, hpy = J["hip"]                                    # albornoz
    F.poly([(sx - 26, sy), (sx + 26, sy), (hpx + 50, hpy + 90), (hpx - 50, hpy + 90)], fill=(214, 212, 204))
    F.rect(520, hy - 8, 580, hy + 8, fill=(20, 16, 12)); F.rect(512, hy - 14, 524, hy + 14, fill=LATON); F.rect(576, hy - 14, 588, hy + 14, fill=LATON)
    cabeza_huesped(F, (hx, hy), r, f=-1, brillo=0.8 + 0.2 * math.sin(t * 6))
    F.line([(hx - r * 0.5, hy), (530, hy)], (255, 40, 40), 3)                # su mirada atraviesa la mirilla
    # tú, dentro, al teléfono
    _tu_telefono(F, t, 1.0)
    F.rect(380, PISO - 170, 460, PISO, fill=(84, 60, 44))
    img = iluminar(F.finish(), F, [], glows=[((900, 700), 700, 0.7), ((J['head'][0], J['head'][1]), 160, 0.9), ((300, 1100), 200, 0.35)], amb=0.18, warm=RELLANO)
    return img, dict(grain=11, tint=((255, 0, 30), 0.12 * k))

def parpadea(t, D, fi):
    b = seg(t, D * 0.38, D * 0.46) - seg(t, D * 0.5, D * 0.58)          # cierra y abre
    hit = t > D * 0.5
    zr = lerp(800, 330, ease(seg(t, D * 0.5, D * 0.75)))                 # tras parpadear se aparta: ves el ojo entero
    sh = 14 * seg(t, D * 0.5, D * 0.55) * (1 - seg(t, D * 0.55, D * 0.8))
    img = vista_mirilla(lambda F: ojo(F, (540 + noise(t * 30) * sh, 900 + noise(t * 30, 2) * sh), zr, close=b,
                                      pupila=0.1 if hit else 0.3, mira=(0, 0)), t, z=1.0)
    golpe = hit and t < D * 0.75
    return img, dict(grain=12, flash=((255, 255, 255), max(0, 1 - (t - D * 0.5) / 0.25)) if hit else None,
                     glitch=0.45 if golpe and fi % 3 else 0.0, tint=((255, 0, 30), 0.25 if hit else 0.05))

def rendija(t, D, fi):
    cut = D * 0.42
    if t < cut:
        img = vista_mirilla(lambda F: pasillo_hotel(F), t, z=lerp(1.0, 1.08, t / cut))
        return img, dict(grain=12, dark=0.1)
    u = seg(t, cut, D)
    F = Frame(fondo(), dict(x=700, y=PISO - 20, z=lerp(3.2, 4.4, ease(u))))
    habitacion(F, rellano=0.8)
    ab = ease(seg(t, cut + 0.3, cut + 0.7))
    for ex in (640, 760):                                                    # dos ojos rojos tumbados en la rendija
        F.ellipse((ex, PISO - 3.5), 26, 3.4 * ab + 0.1, fill=(255, 30, 40))
        F.ellipse((ex, PISO - 3.5), 6, 3.4 * ab + 0.1, fill=(4, 2, 2))
    img = iluminar(F.finish(), F, [], glows=[((700, PISO), 200, 0.6), ((700, PISO - 4), 90, 0.9 * ab)], amb=0.14, warm=(255, 60, 60))
    golpe = ab >= 1
    return img, dict(grain=12, flash=((255, 0, 20), 0.5 * max(0, 1 - (t - cut - 0.7) / 0.3)) if golpe else None,
                     tint=((255, 0, 30), 0.2 * ab), glitch=0.3 if golpe and fi % 4 == 0 else 0.0)

def final(t, D, fi):
    F = Frame(fondo(), dict(x=600, y=lerp(1060, 1080, ease(t / D)), z=1.5))
    habitacion(F, rojo=1.0, rellano=0.7)
    for ex in (640, 760): F.ellipse((ex, PISO - 3.5), 26, 3.4, fill=(255, 30, 40))
    img = iluminar(F.finish(), F, [], glows=[((MX, MY), 110, 0.9), ((700, PISO), 220, 0.8)], amb=0.16, warm=(255, 60, 60))
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, D * 0.5, D * 0.6)) * (1 + 0.03 * math.sin(t * 25))
    if p > 0:
        d.rounded_rectangle((60, 1040, 1020, 1330), 30, fill=(0, 0, 0))
        d.text((540, 1100), tr("SI TU MIRILLA ESTÁ ROJA…"), font=font(62 * p + 1), fill=(255, 255, 255), anchor="mm", stroke_width=int(8 * p), stroke_fill=(0, 0, 0))
        d.text((540, 1210), tr("NO MIRES"), font=font(150 * p + 1), fill=(255, 40, 50), anchor="mm", stroke_width=int(14 * p), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 1350, 850, 1450), 26, fill=(230, 30, 50))
        d.text((540, 1400), tr("SÍGUEME PARA MÁS"), font=font(52), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=10, tint=((255, 0, 30), 0.25 * p if p > 0 else 0), glitch=0.3 if p > 0 and fi % 5 == 0 else 0.0)

ESCENA_FN = dict(pasos=pasos, mirilla=mirilla, punto=punto, llamas=llamas, recepcion=recepcion, entiendes=entiendes,
                 parpadea=parpadea, rendija=rendija, final=final)
PAUSA = dict(pasos=0.4, mirilla=0.6, punto=0.6, llamas=0.3, recepcion=0.7, entiendes=0.6, parpadea=0.9, rendija=0.8, final=2.4)
