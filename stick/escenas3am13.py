"""Si oyes esto a las 3AM — 13: "El vecino de enfrente". Cada noche a las tres el vecino de enfrente te saluda desde su
ventana iluminada y tú le devuelves el saludo; cada noche está más pegado al cristal. Hoy su ventana está vacía: tu móvil
abre solo la cámara frontal y en la foto está él, detrás de tu hombro, saludando.
Piezas nuevas reutilizables: fachada (edificio de enfrente con una ventana iluminada y alguien dentro, recortado por el
hueco), tu_ventana (tu ventana por dentro, vista en primera persona), tu_cuarto (tu cuarto de lado con la ventana a la calle),
vecino (hombre alto y pálido, camiseta interior, sonrisa demasiado ancha), saluda (pose de saludo lento), selfie (vista de la
cámara frontal) y ui_frontal (interfaz de la cámara frontal)."""
import math
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am
from escenas3am3 import paredes, PISO
from escenas3am5 import _osc
from escenas3am10 import cara_sonrisa

ROJO = (255, 40, 40)
CALIDA = (255, 196, 120)          # luz del piso de enfrente
PANTALLA = (150, 200, 255)
FLASH = (226, 234, 255)
VEC = Fig(shirt=(196, 190, 170), limb=(214, 212, 206), scale=1.25)        # camiseta interior, piel pálida, demasiado alto
FACHADA = (40, 40, 52)
WX0, WY0, WX1, WY1 = 600, 360, 1020, 1000                                  # hueco de tu ventana en tu cuarto (vista de lado)
_BG = {}
def fondo(k="a"):
    if k not in _BG: _BG[k] = gradient((20, 22, 34), (8, 9, 14))
    return _BG[k]

# ---------- piezas ----------
def saluda(t, vel=2.4, amp=24, head=0.0):
    """saludo lento con la mano derecha en alto (mueve solo el antebrazo)"""
    return pose(body=0, head=head, a1u=158, a1l=8 + amp * math.sin(t * vel), a2u=-6, a2l=4, l1u=4, l1l=-2, l2u=-4, l2l=-2)

def vecino(F, p, x, y, t=0.0, f=1, sc=1.0, abre=0.0, sonrisa=1.0, snap=True):
    """el vecino: alto, pálido, pelo negro repeinado y una sonrisa demasiado ancha"""
    old = VEC.scale; VEC.scale = 1.25 * sc
    J = VEC.draw(F, p, x, y, f=f, face="closed", t=t, stretch=1.12, snap=snap)
    VEC.scale = old
    hx, hy = J["head"]; r = L["head"] * 1.25 * sc * 1.05
    cara_sonrisa(F, (hx, hy), r, abre=abre, sonrisa=sonrisa, t=t)
    F.d.chord([*F.P(hx - r * 1.04, hy - r * 1.12), *F.P(hx + r * 1.04, hy + r * 0.06)], 180, 360, fill=(14, 14, 18))   # pelo repeinado
    F.line([(hx - r * 0.2, hy - r * 1.02), (hx - r * 0.45, hy - r * 0.6)], (40, 40, 46), r * 0.06)                  # raya
    return J

def mano_cristal(F, c, s=1.0):
    """palma abierta apoyada en el cristal"""
    x, y = c
    F.ellipse((x, y), 30 * s, 36 * s, fill=(226, 222, 214))
    for i, a in enumerate((-36, -12, 10, 32)):
        r_ = math.radians(a - 90)
        F.line([(x + math.cos(r_) * 24 * s, y + math.sin(r_) * 24 * s), (x + math.cos(r_) * 74 * s, y + math.sin(r_) * 74 * s)], (226, 222, 214), 13 * s)
    F.line([(x - 26 * s, y + 4 * s), (x - 58 * s, y - 26 * s)], (226, 222, 214), 13 * s)

def fachada(F, t, cx=540, cy=650, s=1.0, luz=1.0, quien=1.0, cerca=0.0, sonrisa=1.0, manos=0.0):
    """el edificio de enfrente: pared oscura con ventanas apagadas y UNA iluminada (cx, cy). Dentro, el vecino saludando,
    recortado por el hueco de la ventana. cerca (0-1): cuánto se ha pegado al cristal"""
    hw, hh = 150 * s, 200 * s
    x0, y0, x1, y1 = cx - hw, cy - hh, cx + hw, cy + hh
    F.rect(cx - 2400 * s, cy - 2400 * s, cx + 2400 * s, cy + 2400 * s, fill=FACHADA)
    F.rect(x0, y0, x1, y1, fill=_osc((150, 108, 70), luz))                                         # su piso por dentro
    F.rect(x0, y1 - 90 * s, x1, y1, fill=_osc((110, 78, 52), luz))
    F.circle((cx, y0 + 30 * s), 16 * s, fill=_osc((255, 236, 190), 0.4 + 0.6 * luz))                 # bombilla
    F.line([(cx, y0), (cx, y0 + 14 * s)], (30, 26, 22), 4 * s)
    if quien > 0:
        sc = s * (0.95 + 1.25 * cerca)
        hy = cy - 30 * s + 40 * s * cerca
        vecino(F, saluda(t), cx + 10 * s, hy + 194 * sc, t=t, f=1, sc=sc, sonrisa=sonrisa, snap=False)
    if manos > 0:
        for dx in (-1, 1): mano_cristal(F, (cx + dx * 105 * s, cy + 70 * s), 0.9 * s * manos)
        F.ellipse((cx, cy + 40 * s), 70 * s, 34 * s, fill=(196, 200, 206))                            # vaho del aliento
    for (a, b, c, d) in ((cx - 2400 * s, cy - 2400 * s, cx + 2400 * s, y0), (cx - 2400 * s, y1, cx + 2400 * s, cy + 2400 * s),
                         (cx - 2400 * s, y0, x0, y1), (x1, y0, cx + 2400 * s, y1)):                      # recorte de la pared
        F.rect(a, b, c, d, fill=FACHADA)
    for i in range(-3, 4):                                                                              # ventanas apagadas
        for j in range(-3, 4):
            if i == 0 and j == 0: continue
            vx, vy = cx + i * 470 * s, cy + j * 600 * s
            F.rect(vx - hw, vy - hh, vx + hw, vy + hh, fill=(14, 16, 24), outline=(56, 56, 68), w=10 * s)
            F.rect(vx - hw - 20 * s, vy + hh, vx + hw + 20 * s, vy + hh + 22 * s, fill=(58, 58, 68))
    F.rect(x0, y0, x1, y1, outline=(84, 70, 58), w=14 * s)
    F.rect(x0 - 20 * s, y1, x1 + 20 * s, y1 + 22 * s, fill=(70, 66, 70))                                # alféizar
    for xx in (x0 + 4 * s, x1 - 40 * s):                                                                  # cortinas recogidas
        F.rect(xx, y0 + 6 * s, xx + 36 * s, y1 - 6 * s, fill=_osc((150, 60, 50), 0.4 + 0.6 * luz))
    return (cx, cy)

def tu_ventana(F, x0=90, y0=250, x1=990, y1=1170, reloj=True):
    """tu ventana por dentro (primera persona): pared, marco y el reloj en el alféizar"""
    col = (24, 26, 40)
    F.rect(-900, -400, 2000, y0, fill=col); F.rect(-900, y1, 2000, 2600, fill=col)
    F.rect(-900, -400, x0, 2600, fill=col); F.rect(x1, -400, 2000, 2600, fill=col)
    F.rect(x0 - 24, y0 - 24, x1 + 24, y1 + 24, outline=(70, 66, 76), w=24)
    F.line([(x0 + 60, y0 + 80), (x0 + 220, y0 + 20)], (60, 64, 84), 5)                                 # reflejo en el cristal
    F.rect(x0 - 70, y1 + 20, x1 + 70, y1 + 60, fill=(90, 80, 72))
    if reloj: reloj_3am(F, 540, y1 - 10, 0.55)

def tu_cuarto(F, t, quien=1.0, cerca=0.0, luz=1.0):
    """tu cuarto de lado: puerta oscura a la izquierda, cama, y la ventana a la calle con el edificio de enfrente"""
    F.rect(WX0, WY0, WX1, WY1, fill=(10, 12, 22))
    fachada(F, t, 820, 640, s=0.4, quien=quien, cerca=cerca, luz=luz)
    col = (30, 32, 50)
    F.rect(-900, -400, 2000, WY0, fill=col); F.rect(-900, WY1, 2000, PISO, fill=col)
    F.rect(-900, WY0, WX0, WY1, fill=col); F.rect(WX1, WY0, 2000, WY1, fill=col)
    F.rect(-900, PISO, 2000, 3000, fill=(14, 14, 22)); F.line([(-900, PISO), (2000, PISO)], (50, 52, 76), 6)
    F.rect(-900, PISO - 40, 2000, PISO, fill=(22, 22, 34))
    F.rect(WX0 - 18, WY0 - 18, WX1 + 18, WY1 + 18, outline=(70, 66, 76), w=18)
    F.line([((WX0 + WX1) / 2, WY0), ((WX0 + WX1) / 2, WY1)], (70, 66, 76), 12)
    F.rect(WX0 - 50, WY1 + 10, WX1 + 50, WY1 + 44, fill=(90, 80, 72))
    F.rect(140, PISO - 600, 380, PISO, fill=(6, 6, 10))                                                # puerta del cuarto, abierta a oscuras
    F.rect(380, PISO - 600, 420, PISO, fill=(70, 54, 44))
    F.rect(-500, PISO - 190, 120, PISO - 120, fill=(110, 120, 160)); F.rect(-500, PISO - 120, 120, PISO, fill=(70, 54, 44))   # cama
    F.rect(70, PISO - 260, 120, PISO - 120, fill=(70, 54, 44))

def ui_frontal(hora="3:07", rec=False):
    """overlay: interfaz de la cámara frontal (abierta sola)"""
    def dibuja(img):
        d = ImageDraw.Draw(img)
        d.rectangle((0, 240, W, 330), fill=(0, 0, 0))
        d.text((W - 80, 285), hora, font=font(40), fill=ROJO, anchor="rm")
        d.text((540, 285), tr("CÁMARA FRONTAL"), font=font(34), fill=(240, 240, 240), anchor="mm")
        d.ellipse((60, 255, 120, 315), outline=(255, 255, 255), width=4)                               # icono de girar cámara
        d.polygon([(112, 272), (124, 286), (100, 286)], fill=(255, 255, 255))
        for (x, y, sx, sy) in ((150, 420, 1, 1), (930, 420, -1, 1), (150, 1240, 1, -1), (930, 1240, -1, -1)):
            d.line([(x, y), (x + 70 * sx, y)], fill=(255, 255, 255), width=5); d.line([(x, y), (x, y + 70 * sy)], fill=(255, 255, 255), width=5)
        d.rectangle((0, 1720, W, H), fill=(0, 0, 0))
        d.ellipse((540 - 64, 1810 - 64, 540 + 64, 1810 + 64), outline=(255, 255, 255), width=8)
        d.ellipse((540 - 48, 1810 - 48, 540 + 48, 1810 + 48), fill=(255, 60, 60) if rec else (255, 255, 255))
        return img
    return dibuja

def selfie(F, t, el=0.0, jit=1.0):
    """lo que ve la cámara frontal: tu cara asustada, muy cerca, y detrás tu cuarto a oscuras (la puerta abierta).
    el > 0: el vecino detrás de tu hombro, sonriendo y saludando"""
    F.rect(-900, -400, 2000, 2600, fill=(30, 32, 48))
    F.line([(-900, 330), (2000, 380)], (40, 42, 60), 8)                                                    # esquina del techo
    F.rect(650, 360, 1010, 1500, fill=(6, 6, 10)); F.rect(1010, 360, 1060, 1500, fill=(70, 54, 44))        # la puerta abierta
    if el > 0:
        sc = 2.5
        vecino(F, saluda(t, vel=2.2, amp=26, head=-8), 760, 560 + 194 * sc, t=t, f=1, sc=sc, sonrisa=1.0, abre=0.1, snap=False)
    old = TU.scale; TU.scale = 6.0
    TU.draw(F, add(pose(body=-3, head=-6, a1u=8, a1l=2, a2u=-8, a2l=-2, l1u=4, l2u=-4), jitter(t, jit, 3)), 450,
            820 + 143 * 6, f=1, face="scared", t=t, snap=False)
    TU.scale = old
    return (450, 820)

# ---------- escenas ----------
def ventana(t, D, fi):
    """primer fotograma: el vecino muy cerca, sonriendo y saludando en su ventana iluminada; nos alejamos hasta tu ventana"""
    k = ease(seg(t, D * 0.1, D * 0.9))
    F = Frame(fondo(), dict(x=540, y=lerp(600, 760, k), z=lerp(2.6, 1.05, k)))
    c = fachada(F, t, 540, 620, s=1.0, sonrisa=0.6)
    tu_ventana(F)
    img = iluminar(F.finish(), F, [], glows=[(c, 330, 0.95), ((540, 1160), 200, 0.6)], amb=0.24, warm=CALIDA)
    return img, dict(grain=9, flash=(ROJO, 0.25 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.06))

def devuelves(t, D, fi):
    """tu cuarto de lado: tú, en tu ventana, le devuelves el saludo; enfrente, él sigue saludando"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(640, 680, k), y=lerp(960, 930, k), z=lerp(1.6, 1.8, k)))
    tu_cuarto(F, t, quien=1.0)
    TU.draw(F, add(saluda(t + 0.4, vel=2.4, amp=20), jitter(t, 0.4, 2)), 500, PISO, f=1, face="neutral", t=t)
    img = iluminar(F.finish(), F, [], glows=[((820, 640), 160, 0.9), ((560, 900), 380, 0.45)], amb=0.2, warm=CALIDA)
    return img, dict(grain=9)

DIAS = ("LUNES", "MARTES", "MIÉRCOLES")
def cerca(t, D, fi):
    """tres noches seguidas, en saltos: cada noche está más pegado al cristal y sonríe más; la última, las manos en el cristal"""
    i = min(2, int(t / (D / 3)))
    tl = t - i * D / 3
    ce = (0.0, 0.42, 0.85)[i]
    F = Frame(fondo(), dict(x=540, y=lerp(660, 640, seg(tl, 0, D / 3)), z=lerp(1.6, 1.7, seg(tl, 0, D / 3)) + 0.15 * i))
    c = fachada(F, t, 540, 620, s=1.0, cerca=ce, sonrisa=(0.6, 0.85, 1.0)[i], manos=1.0 if i == 2 else 0.0)
    tu_ventana(F)
    img = iluminar(F.finish(), F, [], glows=[(c, 330 + 60 * i, 0.95)], amb=0.24, warm=CALIDA)
    dia = tr(DIAS[i])
    def rotulo(img):
        d = ImageDraw.Draw(img)
        d.text((540, 300), dia, font=font(84), fill=(255, 255, 255), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
        d.text((540, 390), "3:00", font=font(60), fill=ROJO, anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0))
        return img
    return img, dict(grain=10, flash=((255, 255, 255), 0.6 * (1 - seg(tl, 0, 0.25))), tint=((255, 0, 30), 0.05 + 0.06 * i), overlay=rotulo)

def vacia(t, D, fi):
    """hoy: su ventana iluminada… vacía. La bombilla parpadea"""
    k = ease(seg(t, 0, D))
    luz = 0.75 + 0.25 * (noise(t * 6, 3) > -0.5)
    F = Frame(fondo(), dict(x=540, y=lerp(720, 640, k), z=lerp(1.25, 1.9, k)))
    c = fachada(F, t, 540, 620, s=1.0, quien=0.0, luz=luz)
    tu_ventana(F)
    img = iluminar(F.finish(), F, [], glows=[(c, 330, 0.9 * luz), ((540, 1160), 200, 0.6)], amb=0.2, warm=CALIDA)
    def rotulo(img):
        d = ImageDraw.Draw(img)
        d.text((540, 300), tr("HOY"), font=font(84), fill=(255, 255, 255), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
        return img
    return img, dict(grain=11, tint=((255, 0, 30), 0.08 * k), overlay=rotulo)

def movil(t, D, fi):
    """el móvil vibra en tu mano, en la ventana; se abre solo la cámara frontal: tu cara, y detrás tu cuarto a oscuras"""
    if t < D * 0.42:
        vib = 5 * (math.sin(t * 90) > 0) * ((t * 3) % 1 < 0.6)
        F = Frame(fondo(), dict(x=560, y=900, z=1.7))
        tu_cuarto(F, t, quien=0.0)
        J = TU.draw(F, add(pose(body=0, head=10, a1u=50, a1l=70, a2u=-10, a2l=4, l1u=4, l1l=-2, l2u=-4, l2l=-2), jitter(t, 0.6, 2)),
                    500, PISO, f=1, face="scared", t=t)
        hx, hy = J["a1h"]; hx += vib
        F.rect(hx - 14, hy - 30, hx + 14, hy + 8, fill=(18, 18, 22)); F.rect(hx - 10, hy - 26, hx + 10, hy + 4, fill=PANTALLA)
        img = iluminar(F.finish(), F, [], glows=[((hx, hy), 240, 1.0), ((820, 640), 160, 0.7)], amb=0.12, warm=PANTALLA)
        return img, dict(grain=10, dark=0.04)
    tl = t - D * 0.42
    F = Frame(fondo(), dict(x=540, y=900, z=lerp(1.0, 1.1, ease(seg(tl, 0, D * 0.58)))))
    c = selfie(F, t, el=0.0)
    img = iluminar(F.finish(), F, [], glows=[(c, 520, 0.9)], amb=0.14, warm=PANTALLA)
    return img, dict(grain=11, flash=((255, 255, 255), 0.5 * (1 - seg(tl, 0, 0.2))), overlay=ui_frontal())

def clic(t, D, fi):
    """¡clic! salta el flash: en la foto, detrás de tu hombro, su cara sonriente y su mano saludando"""
    k = ease(seg(t, D * 0.25, D))
    F = Frame(fondo(), dict(x=lerp(540, 700, k), y=lerp(900, 680, k), z=lerp(1.0, 1.6, k)))
    c = selfie(F, t, el=1.0, jit=0.0)
    img = iluminar(F.finish(), F, [], glows=[(c, 600, 1.0), ((760, 560), 300, 0.8)], amb=0.35, warm=FLASH)
    return img, dict(grain=9, flash=((255, 255, 255), 1.0 * (1 - seg(t, 0, 0.4))), tint=((255, 0, 30), 0.06 + 0.12 * k),
                     glitch=0.3 if t > D * 0.6 and fi % 4 == 0 else 0.0, overlay=ui_frontal(rec=True))

def _escena_cuarto(F, t, abre=0.0, giro=0.0):
    tu_cuarto(F, t, quien=0.0)
    J = vecino(F, add(saluda(t, vel=2.0, amp=26, head=14), jitter(t, 0.5, 9)), 330, PISO, t=t, f=1, sc=1.0, abre=abre)
    TJ = TU.draw(F, add(pose(body=-4, head=-6, a1u=50, a1l=70, a2u=-10, a2l=4, l1u=4, l1l=-2, l2u=-4, l2l=-2), jitter(t, 1.2, 2)),
                 560, PISO, f=1, face="scared", t=t)
    hx, hy = TJ["a1h"]
    F.rect(hx - 14, hy - 30, hx + 14, hy + 8, fill=(18, 18, 22)); F.rect(hx - 10, hy - 26, hx + 10, hy + 4, fill=PANTALLA)
    return J, TJ

def detras(t, D, fi):
    """plano general: tú en la ventana, de espaldas al cuarto; detrás de ti, delante de la puerta, él. Saludando"""
    hit = t >= D * 0.05
    sh = 14 * hit * (1 - seg(t, D * 0.2, D * 0.5))
    k = ease(seg(t, D * 0.1, D))
    F = Frame(fondo(), dict(x=lerp(500, 400, k) + noise(t * 30) * sh, y=lerp(900, 820, k), z=lerp(1.15, 1.6, k),
                            sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    J, TJ = _escena_cuarto(F, t)
    img = iluminar(F.finish(), F, [], glows=[(J["head"], 260, 0.8), (TJ["a1h"], 220, 0.8), ((820, 640), 150, 0.6)], amb=0.14, warm=FLASH)
    return img, dict(grain=11, flash=((255, 255, 255), max(0, 1 - (t - D * 0.05) / 0.3)) if hit else None,
                     glitch=0.35 if hit and t < D * 0.4 and fi % 3 else 0.0, tint=((255, 0, 30), 0.12))

def voz(t, D, fi):
    """primer plano: su cara inclinada sobre tu nuca, la sonrisa abriéndose al hablar"""
    k = ease(seg(t, 0, D))
    habla = t > D * 0.35 and t < D * 0.92
    F0 = Frame(fondo(), dict(x=540, y=960, z=1.0)); J0 = VEC.joints(saluda(t, head=14), 330, PISO, f=1, snap=True, stretch=1.12)
    hx, hy = J0["head"]
    F = Frame(fondo(), dict(x=hx + 5, y=hy + 70, z=lerp(4.0, 4.6, k)))
    _escena_cuarto(F, t, abre=0.5 + 0.5 * abs(math.sin(t * 7)) if habla else 0.1)
    img = iluminar(F.finish(), F, [], glows=[((hx, hy), 150, 0.9), ((hx + 140, hy + 120), 120, 0.6)], amb=0.1, warm=FLASH)
    return img, dict(grain=12, tint=((255, 0, 30), 0.1 + 0.1 * k), glitch=0.2 if habla and fi % 6 == 0 else 0.0)

def final(t, D, fi):
    """él, saludándote despacio en tu cuarto, y la regla"""
    F = Frame(fondo(), dict(x=440, y=lerp(830, 810, ease(t / D)), z=2.2))
    J, TJ = _escena_cuarto(F, t)
    img = iluminar(F.finish(), F, [], glows=[(J["head"], 240, 0.75), (TJ["a1h"], 200, 0.6)], amb=0.12, warm=FLASH)
    pp = ease_back(seg(t, D * 0.45, D * 0.55)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 170, 1040, 620), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3"), 230, 62, (255, 255, 255)), (tr("ALGUIEN TE SALUDA…"), 310, 62, (255, 255, 255)),
                                 (tr("NO LE DEVUELVAS"), 420, 96, (255, 40, 50)), (tr("EL SALUDO"), 530, 96, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 650, 850, 740), 26, fill=(230, 30, 50))
        d.text((540, 695), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.2 * pp if pp > 0 else 0.06), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(ventana=ventana, devuelves=devuelves, cerca=cerca, vacia=vacia, movil=movil, clic=clic, detras=detras, voz=voz, final=final)
PAUSA = dict(ventana=0.5, devuelves=0.4, cerca=0.6, vacia=0.7, movil=0.4, clic=0.8, detras=0.9, voz=0.8, final=2.4)
