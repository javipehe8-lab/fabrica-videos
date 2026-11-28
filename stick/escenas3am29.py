"""Si oyes esto a las 3AM — 29: "El altavoz inteligente". Tu cuarto de la historia 24 (cama alta, puerta a la derecha) con
una ventana encima de la mesilla, entreabierta, y en la mesilla el reloj (3:00) y el altavoz inteligente con su aro de luz.
Una bombilla inteligente cuelga del techo. La escalera de casa con la puerta de la calle y el panel de la alarma.
Piezas nuevas reutilizables: altavoz (altavoz cilíndrico con aro de luz que gira al escuchar/hablar), panel_alarma (teclado de
alarma con su LED rojo/verde), bombilla (bombilla del techo, encendida o apagada), ventana_abierta (ventana entreabierta con
cortina que se mueve y una cara pálida pegada al cristal), onda (forma de onda de una grabación, dibujada en pantalla) y
cuarto_altavoz (el cuarto completo)."""
import math
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, escalera_casa
from escenas3am2 import cara_palida, dedos, PIEL
from escenas3am3 import paredes, PISO
from escenas3am5 import _osc, cama_alta, tu_tumbado, manta, COLCHON
from escenas3am24 import fondo, reloj_hora, ojos_ir, visita_lado, PUERTA_X0, PUERTA_X1

ROJO = (255, 40, 40)
CIAN = (90, 200, 255)
LUNA = (170, 190, 255)
CALIDO = (255, 210, 150)
VERDE = (60, 220, 110)
WX0, WX1, WY0, WY1 = 730, 920, 560, 830       # ventana encima de la mesilla
AX, AY = 872, PISO - 190                      # base del altavoz (sobre la mesilla)
ARO = (AX, AY - 112)                          # aro de luz
RELOJ = (790, PISO - 222)
BOMBI = (470, 330)

# ---------- piezas ----------
def altavoz(F, t, aro=0.0, gira=1.0, x=AX, y=AY, s=1.0):
    """altavoz cilíndrico de tela gris; aro 0-1: el anillo de luz de arriba (un punto brillante gira alrededor)"""
    w, h = 30 * s, 110 * s
    F.rect(x - w, y - h, x + w, y, fill=(70, 72, 80), outline=(30, 30, 36), w=3)
    for k in range(5): F.line([(x - w + 4, y - h + 20 * s + k * 18 * s), (x + w - 4, y - h + 20 * s + k * 18 * s)], (58, 60, 68), 3)
    F.ellipse((x, y - h), w, 8 * s, fill=(40, 42, 48))
    F.ellipse((x, y - h), w - 3, 6 * s, outline=_osc(CIAN, 0.25 + 0.75 * aro) if aro > 0 else (60, 64, 72), w=max(2, 5 * s))
    if aro > 0:
        a = t * 7 * gira
        F.circle((x + (w - 3) * math.cos(a), y - h + 6 * s * math.sin(a)), 5 * s, fill=_osc((230, 250, 255), aro))
    return (x, y - h)

def panel_alarma(F, x, y, verde=0.0, s=1.0):
    """teclado de alarma en la pared: LED rojo (armada) o verde (desactivada)"""
    F.rect(x - 50 * s, y - 70 * s, x + 50 * s, y + 70 * s, fill=(200, 198, 190), outline=(70, 70, 66), w=4)
    F.rect(x - 38 * s, y - 58 * s, x + 38 * s, y - 28 * s, fill=(30, 44, 40))
    for i in range(3):
        for j in range(3): F.rect(x - 34 * s + i * 26 * s, y - 14 * s + j * 22 * s, x - 18 * s + i * 26 * s, y + 2 * s + j * 22 * s, fill=(150, 148, 140))
    F.circle((x, y - 43 * s), 8 * s, fill=VERDE if verde > 0.5 else ROJO)
    return (x, y - 43 * s)

def bombilla(F, on=1.0, x=BOMBI[0], y=BOMBI[1]):
    F.line([(x, -200), (x, y - 30)], (30, 30, 34), 4)
    F.rect(x - 12, y - 34, x + 12, y - 14, fill=(80, 80, 86))
    F.circle((x, y), 26, fill=_osc(CALIDO, 0.35 + 0.65 * on) if on > 0 else (70, 70, 76))
    return (x, y)

def ventana_abierta(F, t, cara=0.0, abre=0.35):
    """ventana entreabierta (la hoja derecha), con la luna, la cortina que se mueve y, si cara > 0, una cara pálida pegada
    al hueco, con los dedos en el alféizar. Devuelve los ojos (si hay cara)"""
    F.rect(WX0 - 12, WY0 - 12, WX1 + 12, WY1 + 12, fill=(70, 66, 80))
    F.rect(WX0, WY0, WX1, WY1, fill=(10, 14, 30))
    F.circle((780, 610), 18, fill=(200, 210, 240))
    ojos = []
    if cara > 0:
        hx, hy = WX1 - 52, WY1 - 120
        F.rect(hx - 40, hy + 50, hx + 40, WY1, fill=_osc(PIEL, 0.4))
        cara_palida(F, (hx, hy), 40 * lerp(0.85, 1.0, cara), abre=0.25 + 0.5 * cara)
        ojos = [(hx - 12, hy), (hx + 12, hy)]
        dedos(F, (hx - 30, WY1 - 4), 180, n=4, L_=34, w=7)
    F.line([((WX0 + WX1) / 2, WY0), ((WX0 + WX1) / 2, WY1)], (70, 66, 80), 8)
    g = 70 * abre                                                                       # la hoja derecha, abierta hacia dentro
    F.poly([((WX0 + WX1) / 2, WY0), (WX1 - g, WY0 + 20), (WX1 - g, WY1 - 20), ((WX0 + WX1) / 2, WY1)], outline=(90, 86, 100), w=6)
    sw = 18 * math.sin(t * 2.1) + 10 * math.sin(t * 3.7)                                # cortina que se mueve
    F.poly([(WX0 - 40, WY0 - 20), (WX0 + 10, WY0 - 20), (WX0 + 30 + sw, WY1 + 60), (WX0 - 40, WY1 + 70)], fill=(120, 96, 120))
    return ojos

def cuarto_altavoz(F, t, cara_v=0.0, luz=0.0, aro=0.0, gira=1.0, abre=0.0, cara_p=0.0, sienta=0.0, face="closed", jit=0.0, rec=False):
    """el cuarto entero. cara_v: la cara en la ventana; luz: bombilla; abre/cara_p: la puerta de la derecha y la cara que asoma
    arriba. Devuelve dict con puntos de luz y ojos"""
    paredes(F, col=(26, 28, 44))
    oj_v = ventana_abierta(F, t, cara=cara_v)
    b = bombilla(F, on=luz)
    F.rect(740, PISO - 190, 910, PISO, fill=(70, 54, 44), outline=(40, 30, 24), w=4)               # mesilla
    F.rect(752, PISO - 150, 898, PISO - 110, outline=(40, 30, 24), w=3)
    reloj_hora(F, RELOJ[0], RELOJ[1], 0.26, "3:00")
    a = altavoz(F, t, aro=aro, gira=gira)
    F.rect(PUERTA_X0 - 24, PISO - 590, PUERTA_X1 + 24, PISO, fill=(46, 38, 32))                    # marco
    F.rect(PUERTA_X0, PISO - 566, PUERTA_X1, PISO, fill=(3, 3, 5))                                 # pasillo a oscuras
    gap = 150 * ease(abre)
    oj_p = []
    if cara_p > 0 and gap > 20:
        hx, hy = PUERTA_X0 + gap * 0.5, PISO - 500 + 30 * (1 - ease(cara_p))
        F.rect(hx - 50, hy + 60, hx + 50, PISO, fill=_osc(PIEL, 0.35))
        cara_palida(F, (hx, hy), 44, abre=0.3 + 0.3 * cara_p)
        oj_p = [(hx - 13, hy), (hx + 13, hy)]
        for yy in (hy + 120, hy + 170):
            dedos(F, (PUERTA_X0 + gap + 2, yy), 0, n=4, L_=lerp(10, 46, ease(cara_p)), w=8)
    ex = PUERTA_X0 + gap
    F.poly([(ex, PISO - 566), (PUERTA_X1, PISO - 566), (PUERTA_X1, PISO), (ex, PISO)], fill=(84, 66, 52), outline=(40, 30, 24), w=4)
    F.circle((ex + 26, PISO - 280), 10, fill=(196, 168, 96))
    cama_alta(F, t=t)
    J = tu_tumbado(F, t, face=face, cuelga=0.0, sienta=sienta, jit=jit)
    manta(F)
    return dict(aro=a, bombi=b, ojos_v=oj_v, ojos_p=oj_p, cab=J["head"])

def glows_cuarto(c, luz=0.0, aro=0.0, cara_p=0.0):
    g = [(c["aro"], 170, 0.25 + 0.75 * aro), (RELOJ, 150, 0.6), ((780, 610), 200, 0.35), ((WX1 - 60, WY1 - 120), 160, 0.2)]
    if luz > 0: g += [(c["bombi"], 900, 1.1 * luz)]
    if cara_p > 0: g += [((PUERTA_X0 + 60, PISO - 480), 200, 0.3 * cara_p)]
    return g

def onda(img, t, k=1.0, y=1020, col=(120, 220, 255), roncar=0.0, prog=0.0, texto=None):
    """forma de onda de la grabación en pantalla, con barra de progreso; roncar: una onda lenta y grave debajo"""
    if k <= 0: return img
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((90, y - 170, 990, y + 170), 30, fill=(8, 10, 18), outline=(60, 80, 110), width=4)
    if texto: d.text((540, y - 130), texto, font=font(34), fill=(170, 200, 230), anchor="mm")
    for i in range(36):
        x = 140 + i * 23
        h = (10 + 70 * abs(math.sin(t * 9 + i * 0.7) * math.sin(t * 2.3 + i * 0.31))) * k
        d.rectangle((x - 7, y - 20 - h, x + 7, y - 20 + h), fill=col)
    if roncar > 0:
        for i in range(36):
            x = 140 + i * 23
            h = 6 + 28 * roncar * max(0, math.sin(t * 2.6 - i * 0.18)) ** 2
            d.rectangle((x - 7, y + 75 - h, x + 7, y + 75 + h), fill=(255, 110, 110))
    d.line((140, y + 140, 940, y + 140), fill=(50, 60, 80), width=8)
    d.line((140, y + 140, 140 + 800 * prog, y + 140), fill=(120, 220, 255), width=8)
    d.ellipse((140 + 800 * prog - 14, y + 126, 140 + 800 * prog + 14, y + 154), fill=(255, 255, 255))
    return img

def pastilla(img, txt, k, y=300, col=VERDE):
    if k <= 0: return img
    d = ImageDraw.Draw(img)
    fs = int(56 * ease_back(min(1, k)) + 1)
    wtxt = d.textlength(txt, font=font(fs))
    d.rounded_rectangle((540 - wtxt / 2 - 40, y - 55, 540 + wtxt / 2 + 40, y + 55), 30, fill=(0, 0, 0), outline=col, width=5)
    d.text((540, y), txt, font=font(fs), fill=col, anchor="mm")
    return img

def regla_card(img, pp):
    if pp <= 0: return img
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((40, 130, 1040, 640), 30, fill=(0, 0, 0))
    for txt, y, fs0, col in ((tr("SI A LAS 3 TU ALTAVOZ"), 200, 62, (255, 255, 255)), (tr("OBEDECE A ALGUIEN…"), 280, 62, (255, 255, 255)),
                             (tr("NO PREGUNTES"), 420, 110, (255, 40, 50)), (tr("A QUIÉN"), 545, 110, (255, 40, 50))):
        fs = fs0
        while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
        d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
    d.rounded_rectangle((230, 680, 850, 770), 26, fill=(230, 30, 50))
    d.text((540, 725), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
    return img

# ---------- escenas ----------
def luz(t, D, fi):
    """primer fotograma: el reloj a las 3:00 y el aro del altavoz encendiéndose, muy cerca. Se abre el plano: duermes; la
    ventana de encima está entreabierta… y pegada al hueco, casi a oscuras, una cara (la pista)"""
    k = ease(seg(t, 0.2, D * 0.85))
    F = Frame(fondo(), dict(x=lerp(835, 640, k), y=lerp(PISO - 330, 1000, k), z=lerp(2.6, 1.05, k)))
    aro = seg(t, 0.05, 0.4)
    c = cuarto_altavoz(F, t, cara_v=1.0, aro=aro, face="closed")
    img = iluminar(F.finish(), F, [], glows=glows_cuarto(c, aro=aro), amb=0.2, warm=LUNA)
    img = ojos_ir(img, F, c["ojos_v"], k=0.35, r=3)
    return img, dict(grain=9, flash=(ROJO, 0.35 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.06))

def orden(t, D, fi):
    """primer plano del altavoz hablando, el aro girando. Aviso en pantalla: ALARMA DESACTIVADA"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(850, 862, k), y=lerp(PISO - 250, PISO - 230, k), z=lerp(3.2, 3.8, k)))
    c = cuarto_altavoz(F, t, aro=0.7 + 0.3 * abs(math.sin(t * 6)), gira=1.6, face="closed")
    img = iluminar(F.finish(), F, [], glows=glows_cuarto(c, aro=1.0), amb=0.2, warm=LUNA)
    p = seg(t, D * 0.45, D * 0.6)
    return img, dict(grain=9, tint=((255, 0, 30), 0.05), overlay=lambda im: pastilla(im, tr("ALARMA DESACTIVADA"), p, y=330))

def solo(t, D, fi):
    """te incorporas y enciendes la bombilla. La ventana sigue entreabierta… y vacía"""
    sienta = ease(seg(t, 0.1, 0.9))
    on = 1.0 if t > D * 0.35 else 0.0
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(560, 640, k), y=lerp(1000, 980, k), z=lerp(1.15, 1.05, k)))
    c = cuarto_altavoz(F, t, luz=on, aro=0.3, sienta=sienta, face="scared", jit=0.5)
    img = iluminar(F.finish(), F, [], glows=glows_cuarto(c, luz=on, aro=0.3), amb=0.22 + 0.18 * on, warm=CALIDO if on else LUNA)
    return img, dict(grain=8, flash=((255, 230, 180), 0.3 * max(0, 1 - abs(t - D * 0.36) / 0.12)))

def preguntas(t, D, fi):
    """le hablas al altavoz desde la cama; el aro escucha y luego empieza a reproducir"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(640, 800, k), y=lerp(1000, PISO - 260, k), z=lerp(1.2, 2.2, k)))
    rep = seg(t, D * 0.55, D * 0.7)
    c = cuarto_altavoz(F, t, luz=1.0, aro=0.5 + 0.5 * rep, gira=0.6 + rep, sienta=1.0, face="scared", jit=0.4)
    img = iluminar(F.finish(), F, [], glows=glows_cuarto(c, luz=1.0, aro=0.5 + 0.5 * rep), amb=0.4, warm=CALIDO)
    return img, dict(grain=8, overlay=lambda im: pastilla(im, tr("GRABACIÓN · 3:00"), rep, y=330, col=CIAN))

def voz(t, D, fi):
    """la grabación: el altavoz muy cerca y la onda en pantalla. De fondo aparece la segunda onda: los ronquidos"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=AX, y=lerp(PISO - 240, PISO - 260, k), z=lerp(3.0, 3.6, k)))
    c = cuarto_altavoz(F, t, luz=1.0, aro=1.0, gira=1.2, sienta=1.0, face="scared")
    img = iluminar(F.finish(), F, [], glows=glows_cuarto(c, luz=1.0, aro=1.0), amb=0.36, warm=CALIDO)
    r = seg(t, D * 0.45, D * 0.65)
    return img, dict(grain=9, tint=((255, 0, 30), 0.1 * r),
                     overlay=lambda im: onda(im, t, k=0.8, roncar=r, prog=0.1 + 0.6 * t / D, texto=tr("GRABACIÓN · 3:00")))

def ronca(t, D, fi):
    """lo que grabó el altavoz, como un recuerdo frío: tú dormido roncando y, pegada a la ventana abierta, la cara pálida
    hablándole al altavoz con la boca muy abierta"""
    k = ease(seg(t, 0, D * 0.9))
    F = Frame(fondo(), dict(x=lerp(560, WX1 - 40, k), y=lerp(1000, WY1 - 60, k), z=lerp(1.1, 2.6, k)))
    c = cuarto_altavoz(F, t, cara_v=1.0, aro=1.0, gira=1.0, face="closed")
    img = iluminar(F.finish(), F, [], glows=glows_cuarto(c, aro=1.0) + [((WX1 - 52, WY1 - 120), 180, 0.5 * k)], amb=0.24, warm=(150, 220, 200))
    img = ojos_ir(img, F, c["ojos_v"], k=0.5 + 0.5 * k, r=3.5)
    def ov(im):
        d = ImageDraw.Draw(im)
        d.ellipse((70, 250, 110, 290), fill=(255, 40, 50) if int(t * 2) % 2 == 0 else (90, 0, 0))
        d.text((130, 270), "REC  03:00:%02d" % int(4 + t), font=font(44), fill=(255, 255, 255), anchor="lm")
        if k < 0.5:                                                                   # Zzz sobre tu cabeza
            hx, hy = F.P(*c["cab"]); hx /= S; hy /= S
            for i in range(3):
                d.text((hx + 40 + i * 30, hy - 60 - i * 34 - 10 * math.sin(t * 3 + i)), "z", font=font(40 + i * 10), fill=(200, 220, 255), anchor="mm")
        return im
    hit = seg(t, D * 0.55, D * 0.6)
    return img, dict(grain=12, tint=((40, 255, 160), 0.12), overlay=ov,
                     flash=((255, 255, 255), 0.4 * max(0, 1 - abs(t - D * 0.58) / 0.15)), glitch=0.25 if 0 < t - D * 0.56 < 0.25 else 0.0)

def clic(t, D, fi):
    """la escalera: abajo, el panel de la alarma en verde y la puerta de la calle que se abre hacia la noche. Algo alto entra
    y empieza a subir"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(900, 640, k), y=lerp(1040, 960, k), z=lerp(1.5, 1.1, k)))
    path = escalera_casa(F)
    ab = ease(seg(t, D * 0.15, D * 0.45))
    F.rect(1040, 700, 1260, 1300, fill=(46, 38, 32))
    F.rect(1060, 720, 1240, 1300, fill=_osc((16, 22, 40), ab) if ab > 0 else (8, 8, 10))
    if ab > 0: F.circle((1180, 790), 14, fill=_osc((200, 210, 240), ab))
    F.poly([(1060, 720), (lerp(1240, 1100, ab), lerp(720, 700, ab)), (lerp(1240, 1100, ab), lerp(1300, 1320, ab)), (1060, 1300)],
           fill=(80, 56, 42), outline=(36, 24, 18), w=4)
    pl = panel_alarma(F, 975, 960, verde=1.0, s=0.8)
    F.rect(-600, 300, 120, 700, fill=(28, 30, 46))
    F.rect(-120, 160, 80, 700, fill=(62, 50, 42), outline=(36, 26, 20), w=5)                       # tu puerta, arriba
    F.rect(-120, 692, 80, 700, fill=_osc(CALIDO, 0.7))                                             # tu luz, por debajo
    ojos = []
    if t > D * 0.45:
        u = lerp(1.0, 0.72, seg(t, D * 0.45, D))
        x, y = path(u) if u < 1 else (1150, 1300)
        ojos = visita_lado(F, t, x, y, f=-1, fase=u * 6, cara=0.0)
    fig = [((x, y - 300), 260, 0.4)] if ojos else []
    img = iluminar(F.finish(), F, [], glows=[((1150, 1000), 340, 0.2 + 0.5 * ab), (pl, 140, 0.9), ((-20, 700), 200, 0.5)] + fig, amb=0.24, warm=LUNA)
    img = ojos_ir(img, F, ojos, k=0.8, r=4)
    return img, dict(grain=10, tint=((255, 0, 30), 0.1), flash=((255, 255, 255), 0.25 * max(0, 1 - abs(t - D * 0.12) / 0.1)))

def apaga(t, D, fi):
    """tu cuarto con la luz encendida: la puerta se abre, la cara asoma muy arriba. Con tu voz: 'Apaga la luz'. El aro se
    enciende… y la bombilla se apaga"""
    abre = seg(t, D * 0.05, D * 0.4)
    cara = seg(t, D * 0.3, D * 0.45)
    off = t > D * 0.84
    k = ease(seg(t, 0, D))
    hit = seg(t, D * 0.84, D * 0.88)
    F = Frame(fondo(), dict(x=lerp(640, 760, k), y=lerp(1000, 930, k), z=lerp(1.0, 1.25, k),
                            sx=noise(t * 40) * 8 * hit * (1 - seg(t, D * 0.9, D))))
    aro = seg(t, D * 0.5, D * 0.6)
    on = 0.0 if off else 1.0
    c = cuarto_altavoz(F, t, luz=on, aro=aro, abre=abre, cara_p=cara, sienta=1.0, face="scared", jit=1.2)
    img = iluminar(F.finish(), F, [], glows=glows_cuarto(c, luz=on, aro=aro, cara_p=cara), amb=0.4 if not off else 0.12,
                   warm=CALIDO if not off else LUNA)
    img = ojos_ir(img, F, c["ojos_p"], k=cara * (1.0 if off else 0.5), r=4.5)
    return img, dict(grain=10, tint=((255, 0, 30), 0.08 + 0.14 * hit), glitch=0.35 if off and t < D * 0.92 and fi % 2 else 0.0)

def final(t, D, fi):
    """a oscuras: solo el aro del altavoz, el reloj y los ojos en la puerta. La regla"""
    k = ease(seg(t, 0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(900, 700, k), y=lerp(880, 1000, k), z=lerp(1.5, 1.0, k)))
    c = cuarto_altavoz(F, t, luz=0.0, aro=1.0, gira=0.5, abre=1.0, cara_p=1.0, sienta=1.0, face="scared", jit=2.0)
    img = iluminar(F.finish(), F, [], glows=glows_cuarto(c, aro=1.0, cara_p=1.0), amb=0.14, warm=LUNA)
    img = ojos_ir(img, F, c["ojos_p"], k=0.8 + 0.2 * math.sin(t * 6), r=4.5)
    pp = ease_back(seg(t, D * 0.42, D * 0.52)) * (1 + 0.03 * math.sin(t * 25))
    return img, dict(grain=10, tint=((255, 0, 30), 0.22 * pp if pp > 0 else 0.08), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0,
                     overlay=lambda im: regla_card(im, pp))

ESCENA_FN = dict(luz=luz, orden=orden, solo=solo, preguntas=preguntas, voz=voz, ronca=ronca, clic=clic, apaga=apaga, final=final)
PAUSA = dict(luz=0.3, orden=0.4, solo=0.3, preguntas=0.3, voz=0.5, ronca=0.6, clic=0.4, apaga=0.9, final=2.3)
