"""Si oyes esto a las 3AM — 14: "El reflejo que tarda". A las tres, en el espejo del baño, tu reflejo lo hace todo un
segundo tarde (parpadear, levantar la cara, la mano). Te acercas; tú te paras y él sigue acercándose, sonriendo. Pega la
mano al cristal: "Ahora te toca a ti". La luz parpadea y, cuando vuelve, estás dentro del espejo; fuera, él te sonríe y
apaga la luz.
Piezas nuevas reutilizables: bano (pared de azulejos con el hueco del espejo, lavabo, fluorescente y reloj), espejo_bano
(lo que se ve dentro del espejo, recortado), de_espaldas (tú visto de espaldas en primer plano) y reflejo_fig (tu reflejo:
de frente, con parpadeo, cara asustada o la sonrisa de escenas3am10)."""
import math
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am
from escenas3am5 import _osc
from escenas3am10 import cara_sonrisa, parpadeo
from escenas3am13 import mano_cristal

ROJO = (255, 40, 40)
TUBO = (200, 230, 255)                     # fluorescente frío del baño
AZULEJO = (58, 74, 76)
MX0, MY0, MX1, MY1 = 200, 330, 880, 1020   # hueco del espejo
ENC = 1066                                 # encimera del lavabo
LAG = 1.0                                  # el reflejo va un segundo tarde
YO = Fig(shirt=TU.shirt, scale=2.6)        # tú, de espaldas, en primer plano
RF = Fig(shirt=TU.shirt, scale=2.2)        # tu reflejo
_BG = {}
def fondo(k="a"):
    if k not in _BG: _BG[k] = gradient((20, 24, 30), (8, 10, 14))
    return _BG[k]

# ---------- piezas ----------
def _azulejos(F, x0, y0, x1, y1, col=AZULEJO, paso=110):
    F.rect(x0, y0, x1, y1, fill=col)
    lc = _osc(col, 0.7)
    gx = math.ceil(x0 / paso) * paso
    while gx < x1: F.line([(gx, y0), (gx, y1)], lc, 4, round_=False); gx += paso
    gy = math.ceil(y0 / paso) * paso
    while gy < y1: F.line([(x0, gy), (x1, gy)], lc, 4, round_=False); gy += paso

def dentro_espejo(F, t):
    """el baño reflejado: azulejos más oscuros y la puerta abierta a oscuras detrás de ti"""
    _azulejos(F, MX0, MY0, MX1, MY1, col=(40, 52, 56))
    F.rect(MX0 + 40, MY0 + 120, MX0 + 230, MY1, fill=(6, 6, 10))
    F.rect(MX0 + 230, MY0 + 120, MX0 + 256, MY1, fill=(60, 50, 44))

def bano(F, t, luz=1.0, reloj=True, tubo=1.0):
    """la pared alrededor del espejo (tapa lo que se sale del hueco), el marco, el fluorescente, el lavabo y el reloj"""
    for (a, b, c, d) in ((-900, -600, 2000, MY0), (-900, MY1, 2000, 2800), (-900, MY0, MX0, MY1), (MX1, MY0, 2000, MY1)):
        _azulejos(F, a, b, c, d)
    F.rect(MX0 - 16, MY0 - 16, MX1 + 16, MY1 + 16, outline=(150, 156, 160), w=16)
    F.line([(MX0 + 60, MY0 + 40), (MX0 + 200, MY0 + 10)], (120, 140, 150), 4)                          # brillo del cristal
    F.rect(MX0 + 80, MY0 - 70, MX1 - 80, MY0 - 36, fill=_osc((236, 246, 255), 0.35 + 0.65 * tubo), outline=(90, 96, 100), w=4)
    F.rect(MX0 - 60, ENC, MX1 + 60, ENC + 50, fill=(196, 196, 190))                                     # encimera
    F.rect(MX0 - 40, ENC + 50, MX1 + 40, 1500, fill=(60, 56, 54))
    F.ellipse(((MX0 + MX1) / 2, ENC + 22), 220, 26, fill=(150, 156, 160))                               # pila
    F.line([((MX0 + MX1) / 2, ENC), ((MX0 + MX1) / 2, ENC - 60), ((MX0 + MX1) / 2 + 50, ENC - 60)], (170, 176, 180), 14)   # grifo
    if reloj: reloj_3am(F, MX1 - 40, ENC - 40, 0.32)

def reflejo_fig(F, p, hx, hy, sc, t=0.0, cara="neutral", sonrisa=0.0, abre=0.0):
    """tu reflejo, de frente, con la cabeza en (hx, hy). cara: neutral / closed / scared / sonrisa"""
    old = RF.scale; RF.scale = sc
    J = RF.draw(F, p, hx, hy + 143 * sc, f=1, face="closed" if cara in ("sonrisa", "fija") else cara, t=t, snap=False)
    RF.scale = old
    if cara in ("sonrisa", "fija"):                     # fija: tu cara, pero con los ojos abiertos de más y sin expresión
        r = L["head"] * sc
        cara_sonrisa(F, J["head"], r * 1.02, sonrisa=sonrisa if cara == "sonrisa" else 0.0, abre=abre, t=t)
    return J

def de_espaldas(F, p, x, hip, sc=2.6):
    """tú, de espaldas en primer plano: la nuca y la capucha verde caída"""
    old = YO.scale; YO.scale = sc
    J = YO.draw(F, p, x, hip, f=1, face="closed", snap=False)
    YO.scale = old
    hx, hy = J["head"]; r = L["head"] * sc
    F.circle((hx, hy), r, fill=_osc(YO.limb, 0.9))
    F.ellipse((J["sh"][0], J["sh"][1] + 4 * sc), r * 0.95, r * 0.42, fill=_osc(TU.shirt, 0.75))
    return J

QUIETO = pose(body=0, head=0, a1u=10, a1l=6, a2u=-10, a2l=6, l1u=4, l1l=-2, l2u=-4, l2l=-2)
def _mano(u):
    p = dict(QUIETO); p["a1u"] = lerp(10, 165, u); p["a1l"] = lerp(6, 10, u); return p

def _plano(F, t, pr, hy_r, sc_r, yo=None, cara="fija", luz=1.0, sonrisa=0.0, abre=0.0, manos=0.0, reloj=True):
    """el plano del baño: dentro del espejo el reflejo (pose pr, cabeza en (540, hy_r)), la pared, y tú de espaldas"""
    dentro_espejo(F, t)
    J = reflejo_fig(F, pr, 540, hy_r, sc_r, t=t, cara=cara, sonrisa=sonrisa, abre=abre)
    if manos > 0:
        for dx in (-1, 1): mano_cristal(F, (540 + dx * 190, hy_r + 170), 1.2 * manos)
    bano(F, t, luz=luz, reloj=reloj, tubo=luz)
    if yo is not None:
        p, x, hip, sc = yo
        de_espaldas(F, p, x, hip, sc)
    return J

def _blink(t, t0, d=0.22): return t0 <= t < t0 + d

# ---------- escenas ----------
def reloj(t, D, fi):
    """primer fotograma: tu reflejo muy cerca, mirándote fijo con la luz que falla; parpadea… tarde. Nos alejamos al baño"""
    k = ease(seg(t, D * 0.35, D * 0.95))
    F = Frame(fondo(), dict(x=540, y=lerp(600, 900, k), z=lerp(3.0, 1.0, k)))
    luz = max(0.4, parpadeo(t, 3))
    cara = "closed" if _blink(t, D * 0.52) else "fija"
    _plano(F, t, QUIETO, 640, 2.2, yo=(QUIETO, 250, 1440, 2.6) if k > 0.05 else None, cara=cara, luz=luz)
    img = iluminar(F.finish(), F, [], glows=[((540, 640), 300, 0.9 * luz), ((540, MY0 - 50), 200, 0.8 * luz), ((MX1 - 40, ENC - 40), 120, 0.7)],
                   amb=0.22, warm=TUBO)
    return img, dict(grain=9, flash=(ROJO, 0.12 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.07))

def _agacha(t, D):
    """cuánto estás agachado (0-1): bajas a mojarte la cara y subes"""
    return ease(seg(t, 0.0, 0.35)) * (1 - ease(seg(t, 1.2, 1.6)))

def agua(t, D, fi):
    """te agachas al lavabo y subes; el reflejo sube un segundo después (su cara se queda abajo, sin asomar)"""
    F = Frame(fondo(), dict(x=540, y=870, z=lerp(1.05, 1.15, ease(t / D))))
    ay = _agacha(t, D); ar = _agacha(t - LAG, D) if t > LAG else _agacha(0.5, D)
    p_me = pose(body=0, head=0, a1u=30 + 60 * ay, a1l=60 * ay, a2u=-30 - 60 * ay, a2l=-60 * ay, l1u=4, l1l=-2, l2u=-4, l2l=-2)
    _plano(F, t, p_me, 640 + 360 * ar, 2.2, yo=(p_me, 250, 1440 + 300 * ay, 2.6))
    gotas = []
    if 0.3 < t < 1.6:
        for i in range(7):
            gx = 300 + 90 * math.sin(i * 2.1); gy = ENC - 40 - ((t * 400 + i * 60) % 160)
            F.circle((gx, gy), 8, fill=(170, 200, 230)); gotas.append(((gx, gy), 30, 0.3))
    img = iluminar(F.finish(), F, [], glows=[((540, 700), 380, 0.85), ((540, MY0 - 50), 200, 0.8), ((MX1 - 40, ENC - 40), 120, 0.7)] + gotas,
                   amb=0.22, warm=TUBO)
    return img, dict(grain=9, tint=((255, 0, 30), 0.1 * (t > 1.3 and t < 1.3 + LAG)))

def mano(t, D, fi):
    """levantas la mano. Uno… y entonces la levanta él"""
    F = Frame(fondo(), dict(x=540, y=lerp(880, 820, ease(t / D)), z=lerp(1.1, 1.3, ease(t / D))))
    u_me = ease(seg(t, 0.2, 0.8)); u_r = ease(seg(t, 0.2 + LAG + 0.6, 0.8 + LAG + 0.6))
    _plano(F, t, _mano(u_r), 640, 2.2, yo=(_mano(u_me), 250, 1440, 2.6))
    cuenta = 1.0 < t < 2.0
    def uno(img):
        if not cuenta: return img
        d = ImageDraw.Draw(img); q = ease_back(seg(t, 1.0, 1.2))
        d.text((540, 330), "1…", font=font(int(130 * q) + 1), fill=(255, 255, 255), anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
        return img
    img = iluminar(F.finish(), F, [], glows=[((540, 700), 400, 0.85), ((540, MY0 - 50), 200, 0.8), ((MX1 - 40, ENC - 40), 120, 0.7)],
                   amb=0.22, warm=TUBO)
    return img, dict(grain=9, overlay=uno, flash=((255, 255, 255), 0.35 * (1 - seg(t, 2.0, 2.3))) if t > 2.0 else None,
                     tint=((255, 0, 30), 0.1 * (t > 2.0)))

def _acerca(t):
    return ease(seg(t, 0.4, 2.8))

def acercas(t, D, fi):
    """caminas despacio hacia el espejo (te haces más pequeño, de espaldas); él se acerca también, un segundo tarde"""
    a_me = _acerca(t); a_r = _acerca(t - LAG)
    F = Frame(fondo(), dict(x=540, y=lerp(860, 800, a_me), z=lerp(1.15, 1.35, a_me)))
    sc_r = lerp(2.2, 2.9, a_r)
    _plano(F, t, QUIETO, lerp(640, 660, a_r), sc_r, yo=(add(walk(t, 0.25, 0.5), dict(l1u=0)), lerp(250, 300, a_me), lerp(1440, 1330, a_me), lerp(2.6, 2.1, a_me)))
    img = iluminar(F.finish(), F, [], glows=[((540, 680), 420, 0.85), ((540, MY0 - 50), 200, 0.8), ((MX1 - 40, ENC - 40), 120, 0.7)],
                   amb=0.2, warm=TUBO)
    return img, dict(grain=10, tint=((255, 0, 30), 0.06 + 0.06 * a_r))

def sonrisa(t, D, fi):
    """tú quieto; él sigue acercándose hasta llenar el espejo… y sonríe"""
    g = ease(seg(t, 0.0, 2.3))
    so = ease(seg(t, 2.4, 3.3))
    F = Frame(fondo(), dict(x=540, y=lerp(800, 700, g), z=lerp(1.35, 1.6, g), sx=noise(t * 30) * 4 * so, sy=noise(t * 30, 1) * 4 * so))
    sc_r = lerp(2.9, 5.2, g)
    _plano(F, t, QUIETO, lerp(660, 700, g), sc_r, yo=(QUIETO, 300, 1330, 2.1), cara="sonrisa" if so > 0 else "fija",
           sonrisa=lerp(0.3, 1.0, so))
    img = iluminar(F.finish(), F, [], glows=[((540, 700), 420, 0.9), ((540, MY0 - 50), 200, 0.8)], amb=0.18, warm=TUBO)
    return img, dict(grain=11, tint=((255, 0, 30), 0.08 + 0.14 * so), flash=((255, 255, 255), 0.5 * (1 - seg(t, 2.4, 2.7))) if so > 0 else None)

def voz(t, D, fi):
    """primer plano: su sonrisa en el cristal y la palma pegada; habla"""
    habla = 1.7 < t < 3.3
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=540, y=lerp(760, 740, k), z=lerp(1.75, 2.0, k)))
    _plano(F, t, QUIETO, 700, 5.2, cara="sonrisa", sonrisa=1.0, abre=0.5 + 0.5 * abs(math.sin(t * 7)) if habla else 0.0,
           manos=ease_back(seg(t, 0.3, 0.6)))
    img = iluminar(F.finish(), F, [], glows=[((540, 700), 360, 0.9), ((540, MY0 - 50), 200, 0.7)], amb=0.14, warm=TUBO)
    return img, dict(grain=12, tint=((255, 0, 30), 0.16 + 0.08 * k), glitch=0.2 if habla and fi % 6 == 0 else 0.0,
                     flash=((255, 255, 255), 0.3 * (1 - seg(t, 0.3, 0.5))) if t > 0.3 else None)

def luz(t, D, fi):
    """la luz parpadea hasta apagarse; vuelve: ahora el del espejo eres tú, aterrado, golpeando el cristal; fuera, tu espalda, quieta"""
    vuelve = t > 1.3
    if not vuelve:
        on = (int(t * 9) % 3 == 0) and t < 0.9
        F = Frame(fondo(), dict(x=540, y=760, z=1.6))
        _plano(F, t, QUIETO, 700, 3.0, yo=(QUIETO, 300, 1330, 2.1), cara="sonrisa", sonrisa=1.0, luz=0.3 + 0.7 * on)
        img = iluminar(F.finish(), F, [], glows=[((540, 700), 380, 0.8 * on)], amb=0.05 + 0.15 * on, warm=TUBO)
        return img, dict(grain=12, dark=0.5 * (not on))
    tl = t - 1.3
    gol = abs(math.sin(tl * 9)) * (tl > 0.3)
    F = Frame(fondo(), dict(x=540, y=lerp(820, 760, ease(seg(tl, 0, 1.5))), z=lerp(1.25, 1.45, ease(seg(tl, 0, 1.5)))))
    p = add(QUIETO, dict(a1u=120 + 30 * gol, a1l=40, a2u=-120 - 30 * gol, a2l=-40))
    _plano(F, t, add(p, jitter(t, 2.0, 3)), 640, 2.6, yo=(QUIETO, 300, 1330, 2.1), cara="scared", manos=0.9 + 0.1 * gol)
    img = iluminar(F.finish(), F, [], glows=[((540, 680), 400, 0.85), ((540, MY0 - 50), 200, 0.8)], amb=0.2, warm=TUBO)
    return img, dict(grain=11, flash=((255, 255, 255), 0.7 * (1 - seg(tl, 0, 0.3))), tint=((255, 0, 30), 0.12),
                     glitch=0.3 if tl < 0.5 and fi % 3 else 0.0)

def fuera(t, D, fi):
    """desde dentro del espejo: fuera, él, con tu cara y tu sudadera, te sonríe; alarga la mano al interruptor… y oscuridad"""
    off = t > D * 0.78
    k = ease(seg(t, 0, D * 0.75))
    F = Frame(fondo(), dict(x=540, y=lerp(780, 740, k), z=lerp(1.25, 1.45, k)))
    _azulejos(F, -900, -600, 2000, 2800, col=(46, 58, 60))
    F.rect(70, 300, 290, 1500, fill=(6, 6, 10)); F.rect(290, 300, 316, 1500, fill=(60, 50, 44))               # puerta del baño
    F.rect(850, 720, 910, 810, fill=(220, 220, 214), outline=(120, 120, 116), w=4)                              # interruptor
    F.rect(870, 740 + 30 * off, 890, 770 + 30 * off, fill=(160, 160, 154))
    alarga = ease(seg(t, D * 0.45, D * 0.75))
    p = add(QUIETO, dict(a1u=lerp(10, 110, alarga), a1l=lerp(6, 10, alarga)))
    reflejo_fig(F, p, 560, 620, 3.2, t=t, cara="sonrisa", sonrisa=1.0)
    for (a, b, c, d) in ((-900, -600, 2000, 160), (-900, 1180, 2000, 2800), (-900, 160, 40, 1180), (1040, 160, 2000, 1180)):
        F.rect(a, b, c, d, fill=(12, 16, 20))                                                                 # el marco del espejo, por dentro
    F.rect(40, 160, 1040, 1180, outline=(110, 116, 120), w=18)
    img = iluminar(F.finish(), F, [], glows=[((560, 620), 380, 0.9), ((540, 200), 500, 0.5)], amb=0.18, warm=TUBO)
    if off:
        return img, dict(grain=12, dark=0.92, flash=((255, 255, 255), 0.25 * (1 - seg(t, D * 0.78, D * 0.84))))
    return img, dict(grain=11, tint=((120, 200, 220), 0.12), glitch=0.15 if fi % 9 == 0 else 0.0)

def final(t, D, fi):
    """a oscuras, solo el reloj rojo: dentro del espejo, tú con las manos en el cristal. Y la regla"""
    F = Frame(fondo(), dict(x=540, y=lerp(820, 800, ease(t / D)), z=1.3))
    _plano(F, t, add(QUIETO, dict(a1u=120, a1l=40, a2u=-120, a2l=-40)), 640, 2.6, cara="scared", manos=1.0, luz=0.0)
    img = iluminar(F.finish(), F, [], glows=[((MX1 - 40, ENC - 40), 220, 0.9), ((540, 700), 300, 0.35)], amb=0.08, warm=ROJO)
    pp = ease_back(seg(t, D * 0.45, D * 0.55)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 170, 1040, 620), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 TU REFLEJO"), 230, 62, (255, 255, 255)), (tr("LLEGA TARDE…"), 310, 62, (255, 255, 255)),
                                 (tr("NO TE"), 420, 104, (255, 40, 50)), (tr("ACERQUES"), 530, 104, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 650, 850, 740), 26, fill=(230, 30, 50))
        d.text((540, 695), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.2 * pp if pp > 0 else 0.08), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(reloj=reloj, agua=agua, mano=mano, acercas=acercas, sonrisa=sonrisa, voz=voz, luz=luz, fuera=fuera, final=final)
PAUSA = dict(reloj=0.5, agua=0.5, mano=0.6, acercas=0.5, sonrisa=0.7, voz=0.7, luz=0.8, fuera=0.9, final=2.4)
