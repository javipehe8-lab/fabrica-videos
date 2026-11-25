"""Si oyes esto a las 3AM — 26: "La niñera por cámara". Tus padres cenan fuera. A las tres te escriben: por la cámara del
salón ven a alguien sentado contigo en el sofá. Estás solo… pero el cojín de tu lado está hundido (pista). Lo miras
fijamente: no hay nadie, pero el hueco se mueve. Tu madre, en mayúsculas: "NO LO MIRES. Ahora te está mirando". La captura:
tiene la cara pegada a la tuya. Un aliento frío en la oreja: "Ya sabes que estoy". Mientras no lo mirabas, no sabía que lo sabías.
Piezas nuevas reutilizables: cam_salon (imagen de la cámara de seguridad del salón en visión nocturna, con ojo de pez, hora y
EN DIRECTO; modos 'el', 'mira', 'solo'), cojin_hundido (el hueco en el sofá, que puede 'respirar'), sentado (la figura pálida
y altísima sentada en el sofá, de frente o con el cuello estirado hacia tu cara), pantalla_cam (la imagen de cámara a
pantalla completa, como una captura en el móvil)."""
import math
import numpy as np
from PIL import Image, ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU
from escenas3am2 import cara_palida, PIEL
from escenas3am3 import PISO
from escenas3am5 import _osc
from escenas3am7 import salon_casa, SOFA, TELE
from escenas3am21 import chat_grupo
from escenas3am24 import VISITA, _ojo_pez, ojos_ir
from escenas3am25 import bzz

ROJO = (255, 40, 40)
AZUL = (150, 200, 255)
MAMA_T = "MAMÁ"
TU_X = SOFA[0] + 95          # tú, a la izquierda del sofá
HUECO_X = SOFA[0] + 255       # el sitio de al lado (el cojín hundido)
SENT = pose(l1u=90, l1l=-90, l2u=84, l2l=-88, a1u=12, a1l=30, a2u=-10, a2l=30)
_BG = {}
def fondo(k="a"):
    if k not in _BG:
        _BG[k] = {"a": gradient((18, 18, 30), (6, 6, 10)), "m": gradient((12, 12, 16), (4, 4, 6))}[k]
    return _BG[k]

# ---------- piezas ----------
def cojin_hundido(F, k=1.0, resp=0.0):
    """el hueco en el asiento de al lado, como si alguien pesara ahí. resp: hondura extra (el hueco 'respira')"""
    if k <= 0: return
    d = k * (1 + 0.5 * resp)
    y0 = PISO - 230
    F.poly([(HUECO_X - 100, y0), (HUECO_X - 60, y0 + 14 * d), (HUECO_X, y0 + 22 * d), (HUECO_X + 60, y0 + 14 * d), (HUECO_X + 100, y0),
            (HUECO_X + 100, y0 - 3), (HUECO_X - 100, y0 - 3)], fill=(18, 14, 26))
    F.ellipse((HUECO_X, y0 + 30 * d), 86, 22 * d, fill=(58, 48, 80))                 # sombra del hundimiento en la tela
    for s_ in (-1, 1):                                                                # arrugas hacia el centro
        F.line([(HUECO_X + s_ * 110, y0 + 8), (HUECO_X + s_ * 40, y0 + 26 * d)], (50, 42, 70), 4)
        F.line([(HUECO_X + s_ * 90, y0 + 40), (HUECO_X + s_ * 30, y0 + 36 * d)], (50, 42, 70), 3)
    F.ellipse((HUECO_X, PISO - 300), 70, 26 * d, fill=(56, 48, 78))                   # el respaldo, aplastado por una espalda
    for s_ in (-1, 1):                                                                # bordes abultados alrededor del hueco
        F.line([(HUECO_X + s_ * 118, y0 - 2), (HUECO_X + s_ * 96, y0 - 8), (HUECO_X + s_ * 70, y0 + 6 * d)], (120, 106, 150), 5)

def tu(F, t, face="neutral", mira=False, jit=0.0, movil=True):
    p = add(SENT, pose(a1u=120, a1l=150)) if movil else SENT
    if mira: p = add(p, pose(head=14, body=4))
    J = TU.draw(F, add(p, jitter(t, jit, 3)), TU_X, PISO - 170, f=1, face=face)
    if movil:
        hx, hy = J["a1h"]
        F.rect(hx - 10, hy - 34, hx + 12, hy + 6, fill=(30, 40, 60)); F.rect(hx - 6, hy - 30, hx + 8, hy + 2, fill=(170, 210, 255))
    return J

def sentado(F, t, modo="el", cab_tu=None, cuerpo=True):
    """la figura sentada en el hueco. modo 'el': de frente, mirando a la tele (a la cámara). 'mira': el cuello se estira y
    la cara queda pegada a la tuya. Devuelve los ojos"""
    if cuerpo:
        J = VISITA.draw(F, SENT, HUECO_X, PISO - 170, f=-1, face="closed", t=t, stretch=1.15)
    else:
        J = VISITA.joints(SENT, HUECO_X, PISO - 170, f=-1, stretch=1.15)
    hx, hy = J["head"]; r = L["head"] * VISITA.scale
    if modo == "mira" and cab_tu is not None:
        tx, ty = cab_tu[0] + 74, cab_tu[1] - 4
        nx, ny = J["neck"]
        F.line([(nx, ny), ((nx + tx) / 2 + 10, min(ny, ty) - 60), (tx + 10, ty + 30)], PIEL, 16)      # cuello que se dobla
        hx, hy, r = tx, ty, r * 0.95
    cara_palida(F, (hx, hy), r * 1.05, abre=0.3 if modo == "el" else 0.75)
    rr = r * 1.05
    return [(hx - 0.3 * rr, hy), (hx + 0.3 * rr, hy)]

def _salon_vista(modo, t=0.0):
    """el salón como lo ve la cámara de la esquina (mundo recortado a 1080x810)"""
    F = Frame(fondo(), dict(x=700, y=PISO - 330, z=1.18))
    salon_casa(F, 0.0, cocina=0.1)
    J = tu(F, 0.0, face="neutral" if modo == "el" else "scared", mira=(modo != "el"))
    ojos = []
    if modo in ("el", "mira"):
        ojos = sentado(F, 0.0, modo, cab_tu=J["head"])
    else:
        cojin_hundido(F)
    img = F.finish()
    a = np.asarray(img, np.float32)                                               # visión nocturna (gris verdoso)
    g = a @ np.array([0.3, 0.59, 0.11], np.float32)
    g = np.clip((g - 8) * 1.9 + 18, 0, 255)
    a = np.stack([g * 0.8, g * 1.0, g * 0.84], -1)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if ojos:
        img = ojos_ir(img, F, ojos, k=1.0, r=4)
    return img.crop((0, 555, 1080, 1365))

_CAM = {}
def cam_salon(modo, hora, t=0.0, zoom=1.0, foco=(540, 405)):
    """imagen (1080x810) de la cámara del salón, en directo"""
    key = (modo, round(zoom, 2), foco)
    if key not in _CAM:
        if len(_CAM) > 60: _CAM.clear()
        base = _salon_vista(modo)
        if zoom > 1.001:
            w, h = 1080 / zoom, 810 / zoom
            x0 = clamp(foco[0] - w / 2, 0, 1080 - w); y0 = clamp(foco[1] - h / 2, 0, 810 - h)
            base = base.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((1080, 810), Image.BILINEAR)
        _CAM[key] = _ojo_pez(base.resize((540, 405)).resize((1080, 810), Image.BILINEAR))
    img = _CAM[key].copy()
    a = np.asarray(img, np.float32)
    rng = np.random.default_rng(int(t * 30) % 997)
    a = a + rng.normal(0, 9, a.shape[:2])[..., None]
    a[::4] *= 0.86
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    d.text((44, 40), hora, font=font(60), fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
    d.text((44, 742), tr("SALÓN · CÁMARA 1"), font=font(40), fill=(230, 230, 230), stroke_width=3, stroke_fill=(0, 0, 0))
    if int(t * 3) % 2 == 0: d.ellipse((740, 52, 776, 88), fill=ROJO)
    d.text((792, 44), tr("EN DIRECTO"), font=font(48), fill=ROJO, stroke_width=3, stroke_fill=(0, 0, 0))
    return img

def pantalla_cam(cam, z=1.0, cy=830, sx=0.0, sy=0.0, marco=True):
    """la imagen de la cámara a pantalla completa sobre negro (como una captura en el móvil)"""
    out = Image.new("RGB", (W, H), (4, 4, 6))
    w, h = int(1080 * z), int(810 * z)
    im = cam.resize((w, h), Image.BILINEAR)
    out.paste(im, (int(540 - w / 2 + sx), int(cy - h / 2 + sy)))
    if marco:
        d = ImageDraw.Draw(out)
        d.rectangle((int(540 - w / 2 + sx), int(cy - h / 2 + sy), int(540 + w / 2 + sx), int(cy + h / 2 + sy)), outline=(70, 72, 86), width=4)
    return out

def _hora(t, s0=12):
    s = s0 + int(t)
    return f"03:00:{s:02d}"

def _msgs(n=2, solo=False, rojo1=0.0, rojo2=0.0):
    m = [dict(txt=tr("Por la cámara\nvemos a alguien\nsentado contigo"), de=MAMA_T, colde=(240, 140, 180))]
    if n >= 2: m.append(dict(txt=tr("¿Quién es?"), de=MAMA_T, colde=(240, 140, 180)))
    if solo: m.append(dict(txt=tr("estoy solo"), de=None, tk=2))
    if rojo1 > 0: m.append(dict(txt=tr("NO LO MIRES"), de=MAMA_T, p=rojo1, rojo=True))
    if rojo2 > 0: m.append(dict(txt=tr("Ahora te\nestá mirando"), de=MAMA_T, p=rojo2, rojo=True))
    return m

def tv(t): return 0.75 + 0.25 * (noise(t * 12, 5) > -0.3)

def _salon_real(F, t, face="neutral", mira=False, jit=0.0, hueco=1.0, resp=0.0):
    salon_casa(F, t, cocina=0.1)
    cojin_hundido(F, hueco, resp)
    return tu(F, t, face=face, mira=mira, jit=jit)

# ---------- escenas ----------
def camara(t, D, fi):
    """primer fotograma: la cámara del salón en visión nocturna, muy cerca de la cara pálida sentada a tu lado,
    mirando fijo al objetivo. Se abre el plano: tú en el sofá y, a tu lado, eso"""
    k = ease(seg(t, D * 0.25, D * 0.85))
    zoom = lerp(2.6, 1.0, k)
    cam = cam_salon("el", _hora(t), t, zoom=round(zoom, 2), foco=(590, 200))
    img = pantalla_cam(cam, z=1.0, cy=800)
    return img, dict(grain=9, flash=(ROJO, 0.45 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.06),
                     glitch=0.3 if fi % 23 == 0 else 0.0)

def mensaje(t, D, fi):
    """el móvil: tu madre, desde la cena"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo("m"), dict(x=540, y=lerp(800, 860, k), z=lerp(1.35, 1.12, k)))
    m = _msgs(2); m[0]["p"] = 0.85 + 0.15 * seg(t, 0, 0.15); m[1]["p"] = seg(t, D * 0.45, D * 0.6)
    vib = 1.0 if (t < 0.4 or D * 0.45 < t < D * 0.6) else 0.0
    c = chat_grupo(F, t, m, MAMA_T, tr("en línea"), vib=vib, privado=True)
    bzz(F, c, t, k=vib)
    img = iluminar(F.finish(), F, [], glows=[(c, 620, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=9, tint=((255, 0, 30), 0.05))

def solo(t, D, fi):
    """el salón de verdad: tú solo en el sofá, la tele parpadeando. Nadie a tu lado"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(620, 700, k), y=lerp(PISO - 330, PISO - 300, k), z=lerp(1.6, 1.15, k)))
    J = _salon_real(F, t, face="scared", hueco=0.0, jit=0.4)
    img = iluminar(F.finish(), F, [], glows=[((700, PISO - 120), 460, 0.75 * tv(t)), (J["a1h"], 160, 0.7), ((640, PISO - 668), 100, 0.5)],
                   amb=0.2, warm=TELE)
    return img, dict(grain=10, flash=((170, 210, 255), 0.3 * (1 - seg(t, 0, 0.2))))

def cojin(t, D, fi):
    """primer plano del sitio de al lado: el cojín está hundido, como si alguien pesara ahí"""
    k = ease(seg(t, 0, D))
    hit = seg(t, D * 0.3, D * 0.4)
    F = Frame(fondo(), dict(x=lerp(HUECO_X - 80, HUECO_X - 20, k), y=lerp(PISO - 250, PISO - 230, k), z=lerp(1.9, 2.6, k)))
    J = _salon_real(F, t, face="scared", hueco=1.0)
    img = iluminar(F.finish(), F, [], glows=[((HUECO_X, PISO - 120), 360, 0.7 * tv(t)), ((HUECO_X, PISO - 220), 160, 0.35 * hit)], amb=0.2, warm=TELE)
    return img, dict(grain=10, tint=((255, 0, 30), 0.1 * hit), flash=(ROJO, 0.25 * max(0, 1 - abs(t - D * 0.35) / 0.12)))

def miras(t, D, fi):
    """giras la cabeza y miras el hueco fijamente; el hueco sube y baja despacio, como si respirara"""
    k = ease(seg(t, 0, D))
    resp = 0.5 + 0.5 * math.sin(max(0, t - D * 0.45) * 3.2 - math.pi / 2) if t > D * 0.45 else 0.0
    F = Frame(fondo(), dict(x=lerp(TU_X + 60, (TU_X + HUECO_X) / 2, k), y=lerp(PISO - 330, PISO - 290, k), z=lerp(1.6, 2.1, k)))
    J = _salon_real(F, t, face="scared", mira=True, resp=resp, jit=0.6)
    img = iluminar(F.finish(), F, [], glows=[((640, PISO - 120), 420, 0.7 * tv(t)), (J["a1h"], 140, 0.6), ((HUECO_X, PISO - 230), 180, 0.3)],
                   amb=0.2, warm=TELE)
    return img, dict(grain=10, tint=((255, 0, 30), 0.06 + 0.08 * seg(t, D * 0.45, D)))

def nolomires(t, D, fi):
    """el giro: tu madre escribe en mayúsculas, en rojo"""
    r1 = seg(t, D * 0.1, D * 0.22); r2 = seg(t, D * 0.55, D * 0.67)
    hit = r2 >= 1
    sh = 10 * hit * (1 - seg(t, D * 0.7, D * 0.95))
    F = Frame(fondo("m"), dict(x=540, y=lerp(860, 820, ease(t / D)), z=lerp(1.12, 1.3, ease(t / D)), sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    m = _msgs(1, solo=True, rojo1=r1, rojo2=r2)[1:]
    vib = 1.0 if (0 < r1 < 1 or 0 < r2 < 1) else 0.0
    c = chat_grupo(F, t, m, MAMA_T, tr("en línea"), vib=vib, privado=True)
    bzz(F, c, t, k=vib, col=ROJO)
    img = iluminar(F.finish(), F, [], glows=[(c, 620, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=10, tint=((255, 0, 30), 0.1 + 0.14 * hit), glitch=0.3 if hit and t < D * 0.8 and fi % 3 else 0.0,
                     flash=(ROJO, 0.4 * max(0, 1 - abs(t - D * 0.62) / 0.15)))

def captura(t, D, fi):
    """la captura: la figura ya no mira a la cámara; el cuello doblado y la cara pegada a la tuya"""
    k = ease(seg(t, D * 0.2, D))
    zoom = lerp(1.0, 1.8, k)
    cam = cam_salon("mira", "03:01:07", t, zoom=round(zoom, 2), foco=(640, 400))
    hit = seg(t, 0, 0.12)
    sh = noise(t * 40) * 10 * (1 - seg(t, 0.2, 0.6))
    img = pantalla_cam(cam, z=1.0, cy=800, sx=sh)
    return img, dict(grain=10, tint=((255, 0, 30), 0.1 + 0.08 * k), flash=((255, 255, 255), 0.5 * (1 - hit)),
                     glitch=0.3 if fi % 9 == 0 else 0.0)

def oreja(t, D, fi):
    """primerísimo plano de tu cara: un vaho frío te roza la oreja. Al hablar, la cara pálida parpadea pegada a la tuya"""
    k = ease(seg(t, 0, D))
    J0 = TU.joints(add(SENT, pose(a1u=120, a1l=150, head=14, body=4)), TU_X, PISO - 170, f=1)
    hx, hy = J0["head"]
    F = Frame(fondo(), dict(x=lerp(hx + 40, hx + 30, k), y=lerp(hy + 30, hy + 10, k), z=lerp(3.2, 4.2, k)))
    J = _salon_real(F, t, face="scared", mira=True, jit=1.2)
    ap = t > D * 0.45 and (noise(t * 9, 3) > -0.1 or t > D * 0.8)
    ojos = []
    if ap: ojos = sentado(F, t, "mira", cab_tu=J["head"], cuerpo=False)
    else:                                                                           # vaho frío junto a la oreja
        for i in range(3):
            u = (t * 0.8 + i / 3) % 1
            F.circle((J["head"][0] + 40 + 30 * u, J["head"][1] - 10 - 20 * u), 6 + 10 * u, fill=_osc((200, 214, 240), 0.5 * (1 - u)))
    img = iluminar(F.finish(), F, [], glows=[((hx, hy + 120), 300, 0.6 * tv(t)), (J["head"], 120, 0.4)], amb=0.18, warm=TELE)
    img = ojos_ir(img, F, ojos, k=0.9, r=3)
    return img, dict(grain=10, tint=((255, 0, 30), 0.1 + 0.12 * ap), glitch=0.35 if ap and fi % 4 == 0 else 0.0,
                     flash=(ROJO, 0.35 * max(0, 1 - abs(t - D * 0.47) / 0.12)))

def final(t, D, fi):
    """plano general del salón: tú quieto y, a tu lado, eso, con la cara pegada a la tuya. La regla"""
    k = ease(seg(t, 0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(TU_X + 60, 700, k), y=lerp(PISO - 330, PISO - 330, k), z=lerp(2.6, 1.15, k)))
    J = _salon_real(F, t, face="scared", mira=True, jit=0.8)
    ojos = sentado(F, t, "mira", cab_tu=J["head"])
    img = iluminar(F.finish(), F, [], glows=[((700, PISO - 120), 460, 0.7 * tv(t)), (J["head"], 140, 0.4), ((640, PISO - 668), 100, 0.5)],
                   amb=0.2, warm=TELE)
    img = ojos_ir(img, F, ojos, k=0.8 + 0.2 * math.sin(t * 6), r=3)
    pp = ease_back(seg(t, D * 0.42, D * 0.52)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 130, 1040, 640), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 TU CÁMARA"), 200, 62, (255, 255, 255)), (tr("VE A ALGUIEN…"), 280, 62, (255, 255, 255)),
                                 (tr("NO MIRES"), 420, 100, (255, 40, 50)), (tr("AL SOFÁ"), 545, 100, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 680, 850, 770), 26, fill=(230, 30, 50))
        d.text((540, 725), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.22 * pp if pp > 0 else 0.08), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(camara=camara, mensaje=mensaje, solo=solo, cojin=cojin, miras=miras, nolomires=nolomires, captura=captura,
                 oreja=oreja, final=final)
PAUSA = dict(camara=0.5, mensaje=0.5, solo=0.5, cojin=0.7, miras=0.8, nolomires=0.6, captura=0.8, oreja=0.8, final=2.4)
