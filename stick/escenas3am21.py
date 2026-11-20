"""Si oyes esto a las 3AM — 21: "El grupo de clase". A las tres, un número desconocido pregunta en el grupo de clase quién
está despierto. Contestas. Por privado: "Ya lo sé. Te veo." La luz de la webcam de tu portátil (abierto en la mesa,
apuntando a tu cama) está encendida y te llegan fotos tuyas; la última, hecha desde la esquina del techo.
Piezas nuevas reutilizables: chat_grupo (pantalla de mensajería de grupo o privada, con nombres de remitente, fotos dentro
de las burbujas y barra de escribir), portatil (portátil de lado con la lucecita de la webcam), mesa, cuarto_mesa (tu cuarto
con la cama alta y la mesa al lado), foto_cuarto (foto fija del cuarto como la vería una webcam o alguien en el techo),
cosa_techo (la cosa pálida agazapada en la esquina del techo, con el móvil iluminándole la cara)."""
import math, random
from PIL import Image, ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am, CASA_A, CASA_B
from escenas3am2 import cara_palida, PIEL
from escenas3am3 import paredes, PISO
from escenas3am5 import _osc, cama_alta, manta, tu_tumbado, CAMA_X0, CAMA_X1, COLCHON, HUECO
from escenas3am11 import ticks, _ajusta, pulgares, TICK

ROJO = (255, 40, 40)
AZUL = (150, 200, 255)                 # luz de pantalla
VERDE = (90, 255, 120)                 # lucecita de la webcam
MESA_Y = PISO - 290                    # tablero de la mesa
BISAGRA = (968, MESA_Y - 8)            # bisagra del portátil (la tapa mira a la izquierda, a la cama)
CAM = (986, MESA_Y - 168)              # la webcam, arriba de la tapa
TECHO = 300                            # línea del techo
ESQ = (1150, 420)                      # esquina del techo (donde está la cosa)
NUM = "+34 655 030 300"                # el número que nadie tiene guardado
_BG = {}
def fondo(k="a"):
    if k not in _BG:
        _BG[k] = {"a": gradient(CASA_A, CASA_B), "m": gradient((14, 14, 18), (6, 6, 8))}[k]
    return _BG[k]

# ---------- piezas ----------
def mesa(F):
    F.rect(740, MESA_Y, 1120, MESA_Y + 24, fill=(86, 64, 48), outline=(40, 28, 20), w=4)
    for lx in (760, 1100): F.rect(lx - 10, MESA_Y + 24, lx + 10, PISO, fill=(66, 50, 38))

def portatil(F, abre=1.0, luz=0.0, pantalla=0.0):
    """portátil de lado sobre la mesa: base, y tapa (abre 1 = abierta mirando a la cama, 0 = cerrada).
    luz: lucecita de la webcam (0 apagada, 1 encendida). pantalla: brillo de la pantalla (cara izquierda de la tapa)"""
    bx, by = BISAGRA
    F.rect(800, by - 4, bx + 6, by + 8, fill=(150, 154, 162), outline=(60, 62, 70), w=3)               # base (teclado)
    ang = math.radians(lerp(-88, 12, abre))                                                             # 0 = vertical; + hacia atrás
    Lt = 172
    tx, ty = bx + math.sin(ang) * Lt * 0 + Lt * math.sin(ang), by - Lt * math.cos(ang)
    F.line([(bx, by), (tx, ty)], (150, 154, 162), 12)                                                   # tapa
    F.line([(bx, by), (tx, ty)], (60, 62, 70), 3)
    if pantalla > 0 and abre > 0.3:                                                                     # cara de la pantalla
        nx, ny = -math.cos(ang), -math.sin(ang)
        F.line([(bx + nx * 7, by + ny * 7 - 12), (tx + nx * 7, ty + ny * 7 + 10)], _osc(AZUL, pantalla), 5)
    cx, cy = lerp(bx, tx, 0.93) - math.cos(ang) * 8, lerp(by, ty, 0.93) - math.sin(ang) * 8
    if abre > 0.3:
        F.circle((cx, cy), 4.5, fill=(30, 34, 30))                                                      # el objetivo
        if luz > 0:
            F.circle((cx - 1, cy + 11), 3.2 + 1.5 * luz, fill=tuple(int(lerp(30, v, luz)) for v in VERDE))
    return (cx, cy + 11)

def cuarto_mesa(F, t, abre=1.0, luz=0.0, techo=True):
    paredes(F, col=(26, 28, 44))
    if techo:
        F.rect(-900, -400, 2000, TECHO, fill=(18, 20, 32)); F.line([(-900, TECHO), (2000, TECHO)], (40, 42, 62), 6)
        F.rect(1200, TECHO, 2000, PISO, fill=(20, 22, 36)); F.line([(1200, TECHO), (1200, PISO)], (40, 42, 62), 5)   # pared del fondo
    F.rect(240, 420, 560, 700, fill=(34, 40, 60), outline=(60, 56, 70), w=10)                         # póster / corcho de clase
    for i, (x, y) in enumerate(((290, 480), (420, 470), (330, 600), (470, 610))):
        F.rect(x - 40, y - 30, x + 40, y + 30, fill=(200, 196, 170) if i % 2 else (170, 190, 210))
    cama_alta(F, t=t)
    mesa(F)
    reloj_3am(F, 1060, MESA_Y - 34, 0.18)
    return portatil(F, abre=abre, luz=luz)

def tu_en_cama(F, t, face="scared", movil=True, jit=0.6, sienta=0.0):
    """tú tumbado con el móvil encendido delante de la cara"""
    J = tu_tumbado(F, t, face=face, cuelga=0.0, sienta=sienta, jit=jit)
    manta(F)
    if movil:
        hx, hy = J["a1h"]
        F.rect(hx - 10, hy - 26, hx + 10, hy + 6, fill=(18, 18, 22)); F.rect(hx - 7, hy - 23, hx + 7, hy + 3, fill=AZUL)
    return J

def cosa_techo(F, t, x=ESQ[0], y=ESQ[1], sc=1.0, movil=1.0, abre=0.3):
    """la cosa: pálida, agazapada en la esquina del techo, con brazos larguísimos abiertos sobre las paredes y el móvil
    iluminándole la cara desde abajo"""
    c = PIEL
    for (ax, ay), (bx, by), (ex, ey) in (((x - 30, y + 20), (x - 220, y - 40), (x - 330, y + 40)),
                                         ((x + 20, y + 30), (x + 40, y + 260), (x - 20, y + 380)),
                                         ((x - 20, y + 60), (x - 180, y + 200), (x - 300, y + 160))):
        F.line([(ax * sc + x * (1 - sc), ay * sc + y * (1 - sc)), (bx * sc + x * (1 - sc), by * sc + y * (1 - sc)),
                (ex * sc + x * (1 - sc), ey * sc + y * (1 - sc))], (8, 8, 12), 30 * sc)
        F.line([(ax * sc + x * (1 - sc), ay * sc + y * (1 - sc)), (bx * sc + x * (1 - sc), by * sc + y * (1 - sc)),
                (ex * sc + x * (1 - sc), ey * sc + y * (1 - sc))], c, 20 * sc)
    F.ellipse((x - 10 * sc, y + 40 * sc), 70 * sc, 50 * sc, fill=_osc(PIEL, 0.8))                       # cuerpo encogido
    cara_palida(F, (x - 60 * sc, y + 70 * sc), 50 * sc, abre=abre)
    if movil > 0:
        px, py = x - 60 * sc, y + 200 * sc
        F.rect(px - 18 * sc, py - 30 * sc, px + 18 * sc, py + 30 * sc, fill=(16, 16, 20))
        F.rect(px - 13 * sc, py - 25 * sc, px + 13 * sc, py + 25 * sc, fill=_osc(AZUL, movil))
        F.line([(x - 10 * sc, y + 80 * sc), (px + 14 * sc, py + 10 * sc)], c, 14 * sc)
        return (px, py)
    return (x, y)

_FOTOS = {}
def foto_cuarto(modo):
    """foto fija (PIL, 4:3). modo 'webcam': desde el portátil, tú en la cama mirando el móvil (tono verdoso).
    modo 'esquina': desde el techo, inclinada: tú sentado, cerrando el portátil"""
    if modo in _FOTOS: return _FOTOS[modo]
    if modo == "webcam":
        F = Frame(fondo(), dict(x=320, y=COLCHON - 30, z=2.1))
        cuarto_mesa(F, 1.0, techo=False)
        J = tu_en_cama(F, 1.0, face="scared", jit=0.0)
        img = iluminar(F.finish(), F, [], glows=[(J["a1h"], 260, 1.0), (J["head"], 200, 0.7)], amb=0.35, warm=AZUL)
        img = img.crop((0, 555, 1080, 1365))
        a = np.asarray(img, np.float32); a = a * 0.55 + np.array((40, 90, 50), np.float32) * (a / 255 * 0.5 + 0.2)
        img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((270, 202)).resize((1080, 810), Image.NEAREST)
        d = ImageDraw.Draw(img); d.text((40, 40), "03:04", font=font(70), fill=(255, 255, 255))
    else:
        F = Frame(fondo(), dict(x=760, y=1020, z=1.15))
        cuarto_mesa(F, 1.0, abre=0.0, techo=False)
        p = pose(body=6, head=20, a1u=85, a1l=10, a2u=-10, a2l=10, l1u=90, l1l=-90, l2u=86, l2l=-90)
        J = TU.draw(F, p, 690, COLCHON - 4, f=1, face="scared", snap=False)                           # sentado al borde, mano en la tapa
        manta(F)
        img = iluminar(F.finish(), F, [], glows=[((800, 1000), 360, 0.8)], amb=0.5, warm=(200, 220, 255))
        img = img.rotate(-14, resample=Image.BICUBIC, expand=False).crop((0, 470, 1080, 1280))       # inclinada: desde arriba
        a = np.asarray(img, np.float32) * 0.85; img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(img); d.text((40, 40), "03:05", font=font(70), fill=(255, 255, 255))
    _FOTOS[modo] = img
    return img

def _pega_foto(F, foto, x0, y0, w, h):
    px, py = F.P(x0, y0)
    W_, H_ = int(w * F.z * S), int(h * F.z * S)
    if W_ > 4 and H_ > 4: F.img.paste(foto.resize((W_, H_)), (int(px), int(py)))

def chat_grupo(F, t, msgs, titulo, sub="", cx=540, cy=900, vib=0.0, entrada="", cursor=False, barra=True, privado=False):
    """msgs: [dict(txt, de (remitente o None si eres tú), colde, p, tk, rojo, foto=(modo))]"""
    cx += noise(t * 60) * 12 * vib
    F.rect(cx - 250, cy - 430, cx + 250, cy + 430, fill=(20, 20, 26), outline=(90, 90, 100), w=8)
    F.rect(cx - 226, cy - 404, cx + 226, cy + 404, fill=(12, 18, 24))
    for yy in range(int(cy - 230), int(cy + 320), 70):
        for xx in range(int(cx - 200), int(cx + 220), 80):
            F.circle((xx + (yy // 70 % 2) * 40, yy), 5, fill=(22, 30, 38))
    F.text((cx - 160, cy - 375), "3:00", 36, ROJO)
    F.rect(cx + 150, cy - 386, cx + 196, cy - 364, outline=(150, 150, 160), w=3)
    F.rect(cx + 154, cy - 382, cx + 166, cy - 368, fill=(220, 60, 60))
    F.rect(cx - 226, cy - 350, cx + 226, cy - 250, fill=(26, 36, 44))
    if privado:                                                                                    # avatar vacío (gris, sin cara)
        F.circle((cx - 170, cy - 300), 36, fill=(70, 74, 80))
        F.circle((cx - 170, cy - 310), 14, fill=(40, 42, 46)); F.ellipse((cx - 170, cy - 280), 22, 12, fill=(40, 42, 46))
    else:                                                                                          # avatar del grupo: pizarra
        F.circle((cx - 170, cy - 300), 36, fill=(40, 120, 90))
        F.rect(cx - 192, cy - 316, cx - 148, cy - 288, fill=(30, 60, 44), outline=(200, 180, 140), w=3)
    fs = _ajusta(F, titulo, 36, 300)
    F.text((cx + 20, cy - 318), titulo, fs, (236, 240, 244))
    if sub: F.text((cx + 20, cy - 276), sub, 22, (150, 160, 170) if sub != tr("en línea") else (120, 230, 150))
    y = cy - 214
    for m in msgs:
        p = ease_back(clamp(m.get("p", 1.0)))
        if p <= 0: continue
        yo = m.get("de") is None
        foto = m.get("foto")
        if foto:
            w, h = 400, 300 + 20
        else:
            lineas = m["txt"].split("\n")
            fsz = 44
            for ln in lineas: fsz = min(fsz, _ajusta(F, ln, 44, 330))
            w = max(F.d.textlength(ln, font=font(fsz * S)) / S for ln in lineas) + 50
            w = max(w, 160 if yo else 150)
            h = 56 * len(lineas) + 40
        nom = m.get("de") and not privado
        if nom: h += 30
        x0 = cx + 206 - w if yo else cx - 206
        col = (40, 110, 80) if yo else (44, 52, 60)
        if m.get("rojo"): col = (110, 20, 26)
        yc = y + h / 2
        F.rect(x0, yc - h / 2 * p, x0 + w, yc + h / 2 * p, fill=col)
        if p > 0.9:
            yy = y
            if nom:
                F.text((x0 + 14 + F.d.textlength(m["de"], font=font(22 * S)) / S / 2, y + 20), m["de"], 22, m.get("colde", (240, 160, 80)))
                yy += 30
            if foto:
                _pega_foto(F, foto_cuarto(foto), x0 + 10, yy + 10, w - 20, (w - 20) * 0.75)
            else:
                for k, ln in enumerate(lineas):
                    F.text((x0 + w / 2, yy + 38 + k * 56), ln, fsz, (240, 242, 246))
            if yo and m.get("tk"):
                ticks(F, x0 + w - 30, y + h - 14, TICK if m["tk"] == 2 else (160, 170, 180), 0.9)
        y += h + 22
    if not barra: return (cx, cy)
    F.rect(cx - 210, cy + 320, cx + 140, cy + 384, fill=(36, 44, 52))
    F.circle((cx + 178, cy + 352), 32, fill=(40, 160, 110))
    F.poly([(cx + 166, cy + 336), (cx + 196, cy + 352), (cx + 166, cy + 368)], fill=(240, 240, 240))
    txt = entrada + ("|" if cursor and int(t * 3) % 2 == 0 else "")
    if txt: F.text((cx - 140 + F.d.textlength(txt, font=font(34 * S)) / S / 2, cy + 352), txt, 34, (240, 242, 246))
    else: F.text((cx - 90, cy + 352), tr("Mensaje"), 30, (110, 120, 130))
    return (cx, cy)

def _grupo_msgs():
    return [dict(txt=tr("¿mañana hay examen?"), de="Lucía", colde=(240, 160, 80)),
            dict(txt=tr("no sé, buenas noches"), de="Marcos", colde=(120, 200, 255)),
            dict(txt=tr("¿QUIÉN ESTÁ\nDESPIERTO?"), de=NUM, colde=(255, 90, 90))]

TIT_G = "CLASE 4ºB"

# ---------- escenas ----------
def grupo(t, D, fi):
    """primer fotograma: el móvil vibrando a las 3:00 con la pregunta ya llegando"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo("m"), dict(x=lerp(500, 500, k), y=lerp(780, 880, k), z=lerp(1.5, 1.12, k)))
    m = _grupo_msgs(); m[2]["p"] = 0.8 + 0.2 * seg(t, 0, 0.2)
    c = chat_grupo(F, t, m, TIT_G, tr("31 participantes"), vib=1.0 - seg(t, D * 0.3, D * 0.5))
    img = iluminar(F.finish(), F, [], glows=[(c, 620, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=9, flash=(ROJO, 0.4 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.1))

def nadie(t, D, fi):
    k = ease(seg(t, D * 0.2, D))
    F = Frame(fondo("m"), dict(x=lerp(540, 420, k), y=lerp(880, 840, k), z=lerp(1.12, 2.3, k)))
    c = chat_grupo(F, t, _grupo_msgs(), TIT_G, tr("31 participantes"))
    img = iluminar(F.finish(), F, [], glows=[(c, 620, 1.0), ((360, 845), 200, 0.4 * k)], amb=0.25, warm=AZUL)
    return img, dict(grain=10, tint=((255, 0, 30), 0.16 * k))

def portatil_(t, D, fi):
    """el cuarto: tú en la cama con el móvil; a tu lado, en la mesa, el portátil abierto apuntando a la cama"""
    k = ease(seg(t, D * 0.3, D))
    F = Frame(fondo(), dict(x=lerp(565, CAM[0] - 60, k), y=lerp(1000, CAM[1] + 40, k), z=lerp(1.1, 2.6, k)))
    l = cuarto_mesa(F, t, luz=0.25)
    J = tu_en_cama(F, t)
    img = iluminar(F.finish(), F, [], glows=[(J["a1h"], 240, 0.9), ((1060, MESA_Y - 34), 90, 0.5), (l, 30, 0.6), ((900, 900), 400, 0.3)], amb=0.36, warm=AZUL)
    return img, dict(grain=10, tint=((255, 0, 30), 0.06))

def contestas(t, D, fi):
    n = int(2 * seg(t, D * 0.15, D * 0.45))
    env = t > D * 0.6
    m = _grupo_msgs()
    if env: m.append(dict(txt=tr("yo"), de=None, tk=2 if t > D * 0.8 else 1, p=seg(t, D * 0.6, D * 0.7)))
    F = Frame(fondo("m"), dict(x=540, y=lerp(860, 900, ease(t / D)), z=1.0))
    c = chat_grupo(F, t, m, TIT_G, tr("31 participantes"), entrada="" if env else tr("yo")[:n], cursor=not env)
    pulgares(F, t, 540, 830, escribe=1.0 if D * 0.12 < t < D * 0.55 else 0.0)
    img = iluminar(F.finish(), F, [], glows=[(c, 640, 1.0)], amb=0.2, warm=AZUL)
    return img, dict(grain=9)

def privado(t, D, fi):
    a1 = seg(t, D * 0.38, D * 0.46); a2 = seg(t, D * 0.62, D * 0.7)
    hit = a2 >= 1
    sh = 10 * hit * (1 - seg(t, D * 0.72, D * 0.92))
    F = Frame(fondo("m"), dict(x=540 + noise(t * 30) * sh, y=840, z=lerp(1.1, 1.3, ease(t / D)), sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    m = [dict(txt=tr("YA LO SÉ."), de=NUM, p=a1, rojo=True), dict(txt=tr("TE VEO."), de=NUM, p=a2, rojo=True)]
    c = chat_grupo(F, t, m, NUM, tr("en línea"), privado=True, vib=1.0 if (0 < a1 < 1 or 0 < a2 < 1 or (hit and t < D * 0.8)) else 0.0)
    img = iluminar(F.finish(), F, [], glows=[(c, 620, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=10, tint=((255, 0, 30), 0.1 + 0.15 * hit), glitch=0.35 if hit and t < D * 0.8 and fi % 3 else 0.0,
                     flash=(ROJO, 0.4 * max(0, 1 - (t - D * 0.7) / 0.2)) if hit else None)

def luz(t, D, fi):
    """primerísimo plano de la tapa del portátil: la lucecita verde se enciende fuerte"""
    on = seg(t, D * 0.35, D * 0.42)
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=CAM[0] - 20, y=CAM[1] + 10, z=lerp(3.6, 5.2, k), sx=noise(t * 3) * 2))
    l = cuarto_mesa(F, t, luz=0.25 + 0.75 * on)
    img = iluminar(F.finish(), F, [], glows=[(l, 60 + 60 * on, 0.4 + 0.6 * on), ((CAM[0] - 200, CAM[1] + 60), 300, 0.25)], amb=0.25, warm=VERDE if on else AZUL)
    hit = 0 < t - D * 0.42 < 0.15
    return img, dict(grain=10, tint=((60, 255, 90), 0.1 * on), glitch=0.3 if hit else 0.0)

def foto(t, D, fi):
    a = seg(t, D * 0.15, D * 0.25)
    k = ease(seg(t, D * 0.35, D))
    F = Frame(fondo("m"), dict(x=lerp(540, 520, k), y=lerp(860, 660, k), z=lerp(1.1, 2.1, k)))
    m = [dict(txt=tr("YA LO SÉ."), de=NUM, rojo=True), dict(txt=tr("TE VEO."), de=NUM, rojo=True), dict(foto="webcam", de=NUM, p=a)]
    c = chat_grupo(F, t, m, NUM, tr("en línea"), privado=True, vib=1.0 if 0 < a < 1 else 0.0, barra=False)
    img = iluminar(F.finish(), F, [], glows=[(c, 640, 1.0)], amb=0.28, warm=AZUL)
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * k), flash=((255, 255, 255), 0.35 * max(0, 1 - abs(t - D * 0.22) / 0.1)))

def esquina(t, D, fi):
    """cierras la tapa de golpe; el móvil vibra: otra foto, inclinada, desde arriba: tú cerrándolo"""
    corte = D * 0.42
    if t < corte:
        ab = 1 - ease(seg(t, corte * 0.35, corte * 0.75))
        F = Frame(fondo(), dict(x=800, y=1000, z=1.5, sx=noise(t * 40) * 12 * (ab < 0.05)))
        cuarto_mesa(F, t, abre=ab, luz=1.0 if ab > 0.3 else 0.0)
        s_ = ease(seg(t, 0, corte * 0.35))
        p = mix(pose(a1u=40, a1l=30, a2u=-20, l1u=90, l1l=0, l2u=86, l2l=0),
                pose(body=6, head=20, a1u=95, a1l=20, a2u=-10, a2l=10, l1u=90, l1l=-90, l2u=86, l2l=-90), s_)
        J = TU.draw(F, add(p, jitter(t, 1.5, 4)), lerp(380, 690, s_), COLCHON - 4, f=1, face="scared", snap=False)
        manta(F)
        img = iluminar(F.finish(), F, [], glows=[((CAM[0], CAM[1]), 120, 0.8 * ab), ((800, 1000), 360, 0.45)], amb=0.36, warm=(200, 220, 255))
        golpe = 0 < t - corte * 0.75 < 0.12
        return img, dict(grain=10, flash=((255, 255, 255), 0.25) if golpe else None)
    u = t - corte
    a = seg(u, 0.1, 0.25)
    k = ease(seg(u, 0.3, D - corte))
    F = Frame(fondo("m"), dict(x=540, y=lerp(900, 964, k), z=lerp(1.1, 2.3, k)))
    m = [dict(txt=tr("TE VEO."), de=NUM, rojo=True), dict(foto="esquina", de=NUM, p=a)]
    c = chat_grupo(F, t, m, NUM, tr("en línea"), privado=True, vib=1.0 if a < 1 else 0.0, barra=False)
    img = iluminar(F.finish(), F, [], glows=[(c, 640, 1.0)], amb=0.28, warm=AZUL)
    return img, dict(grain=11, tint=((255, 0, 30), 0.2 * k), glitch=0.3 if a >= 1 and u < 0.5 and fi % 3 == 0 else 0.0,
                     flash=(ROJO, 0.4 * max(0, 1 - abs(u - 0.22) / 0.12)))

def final(t, D, fi):
    """la cámara sube despacio por la pared hasta la esquina del techo: la cosa, agazapada, con el móvil en la mano. La regla"""
    k = ease(seg(t, D * 0.05, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(760, ESQ[0] - 120, k), y=lerp(1080, ESQ[1] - 60, k), z=lerp(1.7, 1.25, k)))
    cuarto_mesa(F, t, abre=0.0)
    TU.draw(F, pose(body=6, head=-30, a1u=60, a1l=40, a2u=-10, a2l=10, l1u=90, l1l=-90, l2u=86, l2l=-90), 690, COLCHON - 4, f=1, face="scared", snap=False)
    manta(F)
    ph = cosa_techo(F, t, abre=0.25 + 0.15 * math.sin(t * 2), movil=0.8 + 0.2 * (math.sin(t * 9) > 0))
    img = iluminar(F.finish(), F, [], glows=[(ph, 220, 1.0), ((ESQ[0] - 60, ESQ[1] + 70), 160, 0.5), ((700, 1000), 300, 0.3)], amb=0.24, warm=AZUL)
    pp = ease_back(seg(t, D * 0.45, D * 0.55)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 140, 1040, 560), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 PREGUNTAN"), 210, 62, (255, 255, 255)), (tr("QUIÉN ESTÁ DESPIERTO…"), 290, 62, (255, 255, 255)),
                                 (tr("NO CONTESTES"), 440, 130, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 600, 850, 690), 26, fill=(230, 30, 50))
        d.text((540, 645), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.22 * pp if pp > 0 else 0.08), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(grupo=grupo, nadie=nadie, portatil=portatil_, contestas=contestas, privado=privado, luz=luz, foto=foto,
                 esquina=esquina, final=final)
PAUSA = dict(grupo=0.4, nadie=0.5, portatil=0.6, contestas=0.4, privado=0.7, luz=0.6, foto=0.7, esquina=0.6, final=2.4)
