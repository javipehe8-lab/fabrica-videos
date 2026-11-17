"""Si oyes esto a las 3AM — 18: "El niño del columpio". Desde tu ventana, a las tres, un niño con capucha se columpia solo
en el parque de enfrente, mirando al suelo. Llamas a la policía y la pantalla te ilumina la cara: el columpio se para en seco
y el niño levanta la cabeza hacia ti. Cuelgas: el columpio sigue moviéndose, vacío; él está en tu jardín, mirando arriba.
Piezas nuevas reutilizables: exterior (vista desde tu ventana: parque con columpio y farola, calle y la valla de tu jardín,
dibujable en pequeño con ox/oy/s), columpio_s (columpio doble escalable), nino_capucha (niño con capucha que levanta la cara),
cuarto_lado (tu cuarto de lado con la ventana al parque) y jardin_arriba (tu jardín visto desde la ventana, hacia abajo)."""
import math
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU
from escenas3am7 import llamada
from escenas3am13 import tu_ventana
from escenas3am5 import _osc

ROJO = (255, 40, 40)
FAROLA = (255, 214, 150)
PANTALLA = (150, 200, 255)
NINO_C = Fig(shirt=(34, 38, 52), limb=(190, 192, 200), scale=0.8)       # sudadera oscura con capucha, piel gris
CAPUCHA = (30, 34, 48)
CARA = (212, 212, 216)
_BG = {}
def fondo(k="a"):
    if k not in _BG: _BG[k] = gradient((14, 16, 28), (6, 7, 12)) if k == "a" else gradient((10, 14, 12), (4, 6, 6))
    return _BG[k]

# ---------- piezas ----------
def cara_nino(F, hc, r, alza=0.0, abre=0.0, sonrisa=0.0, f=1):
    """cabeza con capucha. alza 0: cabeza gacha (solo capucha); 1: la cara pálida, de frente, con ojos negros"""
    hx, hy = hc
    F.circle((hx, hy), r * 1.3, fill=CAPUCHA)
    oy = lerp(0.62, 0.08, alza)
    F.ellipse((hx + f * r * 0.12 * (1 - alza), hy + oy * r), r * 0.86, r * lerp(0.42, 0.98, alza), fill=(8, 8, 12))   # hueco de la capucha
    if alza > 0.15:
        k = seg(alza, 0.15, 0.6)
        F.ellipse((hx, hy + oy * r + r * 0.05), r * 0.7 * k, r * lerp(0.2, 0.86, alza), fill=CARA)
        if alza > 0.45:
            ke = seg(alza, 0.45, 0.85)
            for dx in (-0.3, 0.3):
                F.ellipse((hx + dx * r, hy + oy * r - r * 0.1), r * 0.24 * ke, r * 0.32 * ke, fill=(150, 150, 156))   # ojeras
                F.ellipse((hx + dx * r, hy + oy * r - r * 0.06), r * 0.2 * ke, r * 0.3 * ke, fill=(2, 2, 4))
            F.ellipse((hx, hy + oy * r + r * 0.52), r * 0.07 + r * 0.06 * abre, r * 0.05 + r * 0.22 * abre, fill=(2, 2, 4))

SENTADO = pose(body=4, head=16, l1u=80, l1l=-90, l2u=70, l2l=-85, a1u=168, a1l=4, a2u=-168, a2l=-4)
def nino_capucha(F, p, x, y, t=0.0, f=1, sc=1.0, alza=0.0, abre=0.0, sonrisa=0.0, snap=True, rot=0.0):
    old = NINO_C.scale; NINO_C.scale = 0.8 * sc
    J = NINO_C.draw(F, p, x, y, f=f, face="closed", t=t, snap=snap, rot=rot)
    NINO_C.scale = old
    cara_nino(F, J["head"], L["head"] * 0.8 * sc, alza=alza, abre=abre, sonrisa=sonrisa, f=f)
    return J

def columpio_s(F, m, s, x, piso, ang=0.0, ang2=0.0):
    """columpio doble (escalable): devuelve el asiento izquierdo (el del niño)"""
    h, Lr = 330, 230
    col, cu = (70, 60, 52), (54, 50, 46)
    for d_ in (-1, 1):
        F.line([m(x + d_ * 230, piso), m(x + d_ * 170, piso - h)], col, 13 * s)
        F.line([m(x + d_ * 290, piso), m(x + d_ * 170, piso - h)], col, 13 * s)
    F.line([m(x - 190, piso - h), m(x + 190, piso - h)], col, 14 * s)
    out = None
    for cx, a in ((x - 80, ang), (x + 80, ang2)):
        sx, sy = cx + math.sin(a) * Lr, piso - h + math.cos(a) * Lr
        for d_ in (-34, 34): F.line([m(cx + d_, piso - h), m(sx + d_, sy)], cu, 3 * s)
        F.poly([m(sx - 44 * math.cos(a), sy + 44 * math.sin(a)), m(sx + 44 * math.cos(a), sy - 44 * math.sin(a)),
                m(sx + 44 * math.cos(a) + 8 * math.sin(a), sy - 44 * math.sin(a) + 8 * math.cos(a)),
                m(sx - 44 * math.cos(a) + 8 * math.sin(a), sy + 44 * math.sin(a) + 8 * math.cos(a))], fill=(96, 76, 56))
        if out is None: out = (sx, sy, a)
    return out

def mecer(t, amp=0.42, vel=2.3): return amp * math.sin(t * vel)

def exterior(F, t, ang=None, nino=1.0, alza=0.0, abre=0.0, ox=540, oy=710, s=1.0, valla=True, nino_x=None):
    """lo que se ve desde tu ventana: cielo, árboles, el parque (columpio y farola), la calle y la valla de tu jardín.
    (ox, oy) y s permiten dibujarlo en pequeño dentro de otra ventana. Devuelve dict con farola, asiento y cabeza"""
    m = lambda x, y: (ox + (x - 540) * s, oy + (y - 710) * s)
    if ang is None: ang = mecer(t)
    F.rect(*m(-900, -400), *m(2000, 2600), fill=(12, 14, 24))
    F.circle(m(830, 380), 38 * s, fill=(196, 200, 214)); F.circle(m(812, 372), 34 * s, fill=(12, 14, 24))         # luna
    for i in range(12):                                                                                         # árboles al fondo
        tx = -200 + i * 130 + (i % 3) * 30
        F.circle(m(tx, 700 - (i % 4) * 30), (90 + (i % 3) * 25) * s, fill=(10, 16, 14))
    F.rect(*m(-900, 720), *m(2000, 920), fill=(16, 24, 20))                                                    # césped del parque
    F.line([m(-900, 720), m(2000, 720)], (24, 34, 28), 4 * s)
    lamp = m(760, 870 - 380)
    F.line([m(760, 870), m(760, 870 - 380)], (40, 42, 56), 10 * s); F.line([m(760, 490), m(700, 490)], (40, 42, 56), 8 * s)
    F.ellipse(m(696, 502), 26 * s, 10 * s, fill=FAROLA)
    sx, sy, a = columpio_s(F, m, s, 420, 880, ang=ang, ang2=0.04 * math.sin(t * 1.3))
    head = None
    if nino > 0:
        J = nino_capucha(F, SENTADO, *m(sx, sy - 6), t=t, f=1, sc=0.62 * s, alza=alza, abre=abre, snap=False, rot=math.degrees(-a) * 0.8)
        head = J["head"]
    F.rect(*m(-900, 920), *m(2000, 1010), fill=(20, 20, 28))                                                   # calle
    F.line([m(-900, 920), m(2000, 920)], (44, 46, 60), 5 * s)
    if valla:
        F.rect(*m(-900, 1070), *m(2000, 2600), fill=(14, 20, 16))                                              # tu jardín
        F.line([m(-900, 1034), m(2000, 1034)], (70, 70, 80), 8 * s)
        for i in range(-10, 30):
            px = i * 60
            F.poly([m(px - 16, 1090), m(px + 16, 1090), m(px + 16, 1010), m(px, 990), m(px - 16, 1010)], fill=(62, 62, 72))
    return dict(lamp=lamp, seat=m(sx, sy), head=head or m(sx, sy - 120))

WX0, WY0, WX1, WY1 = 560, 380, 1000, 980
def cuarto_lado(F, t, ang=None, nino=1.0, alza=0.0):
    """tu cuarto de lado, a oscuras: la ventana al parque (en pequeño), la cama y la puerta"""
    ex = exterior(F, t, ang=ang, nino=nino, alza=alza, ox=(WX0 + WX1) / 2, oy=700, s=0.42, valla=True)
    col = (26, 28, 42)
    F.rect(-900, -400, 2000, WY0, fill=col); F.rect(-900, WY1, 2000, 1300, fill=col)
    F.rect(-900, WY0, WX0, WY1, fill=col); F.rect(WX1, WY0, 2000, WY1, fill=col)
    F.rect(-900, 1300, 2000, 3000, fill=(12, 12, 20)); F.line([(-900, 1300), (2000, 1300)], (44, 46, 66), 6)
    F.rect(WX0 - 16, WY0 - 16, WX1 + 16, WY1 + 16, outline=(64, 62, 72), w=16)
    F.line([((WX0 + WX1) / 2, WY0), ((WX0 + WX1) / 2, WY1)], (64, 62, 72), 10)
    F.rect(WX0 - 50, WY1 + 8, WX1 + 50, WY1 + 40, fill=(80, 72, 66))
    F.rect(60, 700, 280, 1300, fill=(6, 6, 10)); F.rect(280, 700, 310, 1300, fill=(60, 48, 40))                # puerta
    F.rect(-600, 1110, 20, 1180, fill=(90, 100, 140)); F.rect(-600, 1180, 20, 1300, fill=(60, 48, 40))        # cama
    return ex

def jardin_arriba(F, t, nino=1.0, alza=1.0, abre=0.0, sonrisa=0.0, ang=None, porche=0.0):
    """mirando hacia abajo desde tu ventana: la calle y el parque arriba, la valla, y tu jardín; el niño de pie, mirando arriba"""
    if ang is None: ang = mecer(t)
    F.rect(-900, -400, 2000, 2600, fill=(16, 24, 18))                                                       # césped
    for i in range(40):                                                                                     # matas de hierba
        gx, gy = (i * 197) % 1500 - 200, 700 + (i * 331) % 1300
        F.line([(gx, gy), (gx + 8, gy - 22)], (24, 36, 26), 4); F.line([(gx + 10, gy), (gx + 4, gy - 18)], (24, 36, 26), 4)
    F.rect(-900, -400, 2000, 330, fill=(16, 24, 20))                                                       # parque, lejos
    sx, sy, a = columpio_s(F, lambda x, y: (540 + (x - 540) * 0.32, 300 + (y - 880) * 0.32), 0.32, 420, 880, ang=ang)
    F.rect(-900, 330, 2000, 470, fill=(20, 20, 28))                                                        # calle
    F.line([(-900, 330), (2000, 330)], (44, 46, 60), 5)
    F.line([(-900, 520), (2000, 520)], (70, 70, 80), 8)                                                    # valla
    for i in range(-10, 30):
        px = i * 70
        F.poly([(px - 20, 600), (px + 20, 600), (px + 20, 500), (px, 476), (px - 20, 500)], fill=(62, 62, 72))
    for i in range(6): F.ellipse((540 + (i % 2) * 30, 700 + i * 200), 70, 34, fill=(40, 40, 44))           # caminito de piedras
    F.rect(780, 1500, 2000, 2600, fill=(30, 30, 36))                                                       # tejadillo del porche
    for i in range(8): F.line([(780, 1540 + i * 60), (2000, 1540 + i * 60)], (22, 22, 28), 4)
    if porche > 0: F.circle((900, 1460), 24, fill=_osc(FAROLA, 0.3 + 0.7 * porche))
    head = (540, 1000)
    if nino > 0:
        p = pose(body=-4, head=-28, a1u=10, a1l=6, a2u=-10, a2l=6, l1u=4, l1l=-2, l2u=-4, l2l=-2)
        F.ellipse((560, 1290), 120, 26, fill=(8, 10, 8))                                                  # sombra
        J = nino_capucha(F, p, 540, 1290, t=t, f=1, sc=2.3, alza=0.0, snap=True)
        head = J["head"]
        cara_nino(F, head, L["head"] * 0.8 * 2.3, alza=alza, abre=abre, sonrisa=sonrisa)
    F.rect(-900, 1760, 2000, 2600, fill=(40, 36, 34))                                                      # tu alféizar
    F.rect(-900, 1740, 2000, 1770, fill=(70, 62, 56))
    return head

def tu_ventana_park(F, t, reloj=True, **kw):
    ex = exterior(F, t, **kw)
    tu_ventana(F, reloj=reloj)
    return ex

def onomato(img, txt, p, xy, rot=0):
    if p <= 0: return img
    d = ImageDraw.Draw(img)
    d.text(xy, txt, font=font(90 * p + 1), fill=(230, 230, 240), anchor="mm", stroke_width=int(8 * p), stroke_fill=(0, 0, 0))
    return img

# ---------- escenas ----------
def reloj(t, D, fi):
    """primer fotograma: el niño con capucha en el columpio, muy cerca y solo; nos alejamos hasta tu ventana con las 3:00"""
    k = ease(seg(t, D * 0.05, D * 0.85))
    F = Frame(fondo(), dict(x=lerp(370, 540, k), y=lerp(740, 880, k), z=lerp(3.0, 1.1, k)))
    ex = tu_ventana_park(F, t)
    img = iluminar(F.finish(), F, [], glows=[(ex["lamp"], 330, 0.8), (ex["seat"], 200, 0.5), ((540, 1160), 200, 0.6)], amb=0.2, warm=FAROLA)
    return img, dict(grain=9, flash=(ROJO, 0.3 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.05))

NIC = (0.12, 0.72)
def chirrido(t, D, fi):
    """zoom al columpio: chirría; el niño, cabeza gacha, mirando al suelo"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(430, 410, k), y=lerp(760, 790, k), z=lerp(1.8, 2.6, k)))
    ex = tu_ventana_park(F, t, reloj=False)
    img = iluminar(F.finish(), F, [], glows=[(ex["lamp"], 300, 0.8), (ex["seat"], 220, 0.55)], amb=0.18, warm=FAROLA)
    def ov(img):
        for i, c in enumerate(NIC):
            p = ease_back(seg(t, c, c + 0.2)) * (1 - seg(t, c + 0.8, c + 1.1))
            onomato(img, tr("ÑIC"), p, (270 + i * 520, 520 + i * 60))
        return img
    return img, dict(grain=10, overlay=ov, dark=0.04)

def oscuro(t, D, fi):
    """tu cuarto de lado, a oscuras: tú junto a la ventana; fuera, el niño columpiándose"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(620, 660, k), y=lerp(1080, 1060, k), z=lerp(1.55, 1.75, k)))
    ex = cuarto_lado(F, t)
    TU.draw(F, add(STAND, jitter(t, 0.6, 2)), 470, 1300, f=1, face="neutral", t=t)
    img = iluminar(F.finish(), F, [], glows=[(ex["lamp"], 140, 0.7), (ex["seat"], 110, 0.4), ((780, 680), 380, 0.18), ((470, 1100), 260, 0.2)], amb=0.13, warm=FAROLA)
    return img, dict(grain=11, dark=0.05)

TEL = pose(body=0, head=-4, a1u=150, a1l=160, a2u=-10, a2l=10, l1u=6, l1l=-2, l2u=-6, l2l=-2)
def llamas(t, D, fi):
    corte = 1.35
    if t < corte:
        F = Frame(fondo(), dict(x=540, y=900, z=lerp(1.0, 1.08, seg(t, 0, corte))))
        F.rect(-900, -400, 2000, 2600, fill=(14, 14, 22))
        llamada(F, t, tr("POLICÍA · 112"), habla=0.0)
        img = iluminar(F.finish(), F, [], glows=[((540, 860), 520, 0.9)], amb=0.12, warm=PANTALLA)
        return img, dict(grain=9)
    tt = t - corte
    k = ease(seg(tt, 0, D - corte))
    F = Frame(fondo(), dict(x=lerp(560, 520, k), y=lerp(1080, 1080, k), z=lerp(1.8, 2.3, k)))
    ex = cuarto_lado(F, t)
    J = TU.draw(F, add(TEL, jitter(t, 0.8, 4)), 470, 1300, f=1, face="scared", t=t)
    hx, hy = J["a1h"]
    F.rect(hx - 10, hy - 34, hx + 16, hy + 14, fill=(20, 20, 26)); F.rect(hx - 6, hy - 30, hx + 12, hy + 10, fill=PANTALLA)
    on = seg(tt, 0.0, 0.3)
    img = iluminar(F.finish(), F, [], glows=[((hx, hy), 300, 0.95 * on), ((560, 1000), 520, 0.35 * on), (ex["lamp"], 120, 0.6)], amb=0.08, warm=PANTALLA)
    return img, dict(grain=10, flash=(PANTALLA, 0.4 * (1 - seg(tt, 0, 0.25))))

TSTOP, TALZA = 1.4, (2.0, 2.9)
def para(t, D, fi):
    """POV: el columpio se para en seco; el niño levanta la cabeza hacia tu ventana"""
    if t < TSTOP: ang = mecer(t)
    else: ang = mecer(TSTOP) * max(0, 1 - (t - TSTOP) / 0.08) + 0.004 * noise(t * 20, 2)
    alza = ease(seg(t, *TALZA))
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(480, 400, k), y=lerp(780, 700, k), z=lerp(1.6, 3.4, ease(seg(t, 1.2, D)))))
    ex = tu_ventana_park(F, t, reloj=False, ang=ang, alza=alza)
    img = iluminar(F.finish(), F, [], glows=[(ex["lamp"], 300, 0.8), (ex["seat"], 220, 0.55), (ex["head"], 120, 0.4 * alza)], amb=0.18, warm=FAROLA)
    stop = t > TSTOP; hit = t > TALZA[1]
    return img, dict(grain=10, tint=((255, 0, 30), 0.08 * stop + 0.14 * hit), dark=0.04,
                     flash=(ROJO, 0.5 * max(0, 1 - (t - TSTOP) / 0.2)) if stop and not hit else
                           (((255, 255, 255), 0.7 * max(0, 1 - (t - TALZA[1]) / 0.25)) if hit else None),
                     glitch=0.3 if hit and t < TALZA[1] + 0.4 and fi % 3 else 0.0)

TJARDIN = 3.6
def cuelgas(t, D, fi):
    """el columpio sigue moviéndose, vacío… y el niño está abajo, en tu jardín, mirando arriba"""
    if t < TJARDIN:
        k = ease(seg(t, 0, TJARDIN))
        F = Frame(fondo(), dict(x=lerp(420, 470, k), y=lerp(760, 800, k), z=lerp(2.6, 1.6, k)))
        ex = tu_ventana_park(F, t, reloj=False, nino=0.0)
        img = iluminar(F.finish(), F, [], glows=[(ex["lamp"], 300, 0.8), (ex["seat"], 220, 0.55)], amb=0.18, warm=FAROLA)
        return img, dict(grain=10, dark=0.04, tint=((255, 0, 30), 0.06 * seg(t, 2.6, 3.0)))
    tt = t - TJARDIN
    F = Frame(fondo("b"), dict(x=540, y=lerp(1050, 1000, seg(tt, 0, 1.5)), z=lerp(1.0, 1.25, ease(seg(tt, 0, 1.5)))))
    h = jardin_arriba(F, t, alza=1.0, sonrisa=0.0)
    img = iluminar(F.finish(), F, [], glows=[(h, 360, 0.6), ((540, 1250), 400, 0.3)], amb=0.14, warm=(200, 210, 255))
    return img, dict(grain=11, tint=((255, 0, 30), 0.16), flash=((255, 255, 255), 0.8 * max(0, 1 - tt / 0.25)),
                     glitch=0.35 if tt < 0.35 and fi % 3 else 0.0)

TVOZ = 2.49
def voz(t, D, fi):
    """muy cerca de su cara, mirando arriba: sonríe y habla"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo("b"), dict(x=540, y=lerp(1000, 960, k), z=lerp(1.4, 3.2, k)))
    hab = seg(t, TVOZ, TVOZ + 0.2) * (1 - seg(t, TVOZ + 1.1, TVOZ + 1.3))
    h = jardin_arriba(F, t, alza=1.0, sonrisa=seg(t, 0.6, 1.6), abre=hab * (0.5 + 0.5 * abs(math.sin(t * 18))))
    img = iluminar(F.finish(), F, [], glows=[(h, 300, 0.7)], amb=0.12, warm=(200, 210, 255))
    return img, dict(grain=11, tint=((255, 0, 30), 0.1 + 0.12 * seg(t, TVOZ, TVOZ + 0.2)), dark=0.04,
                     glitch=0.25 if TVOZ < t < TVOZ + 0.3 and fi % 3 else 0.0)

GOLPES, TR = (0.55, 0.85, 1.15), 1.8
def final(t, D, fi):
    """el jardín vacío; el columpio, al fondo, sigue moviéndose; llaman a tu puerta. La regla"""
    sh = sum(max(0, 1 - (t - g) / 0.12) for g in GOLPES if t >= g)
    F = Frame(fondo("b"), dict(x=540 + 10 * sh * noise(t * 40, 1), y=lerp(1000, 980, seg(t, 0, D)), z=1.0 + 0.02 * sh))
    jardin_arriba(F, t, nino=0.0, porche=seg(t, 0.4, 0.5))
    img = iluminar(F.finish(), F, [], glows=[((900, 1460), 340, 0.7 * seg(t, 0.4, 0.5)), ((540, 300), 200, 0.3)], amb=0.14, warm=FAROLA)
    pp = ease_back(seg(t, TR, TR + 0.3)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        for i, g in enumerate(GOLPES):
            q = ease_back(seg(t, g, g + 0.15)) * (1 - seg(t, TR - 0.2, TR))
            onomato(img, tr("TOC"), q, (760 + (i % 2) * 120, 1050 - i * 150))
        if pp <= 0: return img
        d_ = ImageDraw.Draw(img)
        d_.rounded_rectangle((40, 1150, 1040, 1600), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 VES A"), 1210, 62, (255, 255, 255)), (tr("UN NIÑO SOLO…"), 1290, 62, (255, 255, 255)),
                                 (tr("NO LLAMES"), 1400, 104, ROJO), (tr("A NADIE"), 1510, 104, ROJO)):
            fs = fs0
            while fs > 24 and d_.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d_.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d_.rounded_rectangle((230, 1640, 850, 1730), 26, fill=(230, 30, 50))
        d_.text((540, 1685), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.2 * pp if pp > 0 else 0.08 * min(1, sh)),
                     glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(reloj=reloj, chirrido=chirrido, oscuro=oscuro, llamas=llamas, para=para, cuelgas=cuelgas, voz=voz, final=final)
PAUSA = dict(reloj=0.4, chirrido=0.5, oscuro=0.5, llamas=0.4, para=0.7, cuelgas=0.6, voz=0.8, final=2.4)
