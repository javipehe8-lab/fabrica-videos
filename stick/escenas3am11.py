"""Si oyes esto a las 3AM — 11: "El mensaje de tu amigo". Tu mejor amigo, Dani (gorro rojo), te escribe a las tres. Lo
enterraron ayer con su móvil. Escenas: chat del móvil a pantalla completa, el cementerio con la tumba recién cubierta que
brilla por dentro, la calle vista desde tu ventana (historia 9), tu cama alta (historia 5), tus pulgares escribiendo solos,
la escalera (historia 1) y la puerta de la calle (historia 3).
Piezas nuevas reutilizables: chat (pantalla de mensajería con burbujas, ticks y barra de escribir), ticks, avatar_dani,
gorro, cara_muerto (cara gris con ojos hundidos y pupilas diminutas), dani (cuerpo con traje y móvil), tumba, pulgares."""
import math, random
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, escalera_casa, CASA_A, CASA_B
from escenas3am3 import paredes, puerta_calle, DX0, DX1, DY0, PISO
from escenas3am5 import _osc, _cuarto, cama_alta, tu_tumbado, CAMA_X0, CAMA_X1, COLCHON, HUECO
from escenas3am9 import ventana_marco

ROJO = (255, 40, 40)
AZUL = (150, 200, 255)              # luz de pantalla
TICK = (60, 170, 255)               # ticks azules de "leído"
GORRO = (200, 36, 44)               # el gorro rojo de Dani (pista visual: el avatar, la tumba y la calle)
MUERTO = (172, 178, 170)            # piel gris verdosa
TIERRA = (64, 46, 34)
DANI = Fig(shirt=(24, 24, 30), limb=(38, 38, 46), scale=1.1)               # traje negro del entierro
_BG = {}
def fondo(k="a"):
    if k not in _BG:
        _BG[k] = {"a": gradient(CASA_A, CASA_B), "m": gradient((14, 14, 18), (6, 6, 8)),
                  "n": gradient((8, 10, 24), (2, 3, 8))}[k]
    return _BG[k]

# ---------- piezas ----------
def gorro(F, c, r, col=GORRO, f=1):
    """gorro de lana rojo con vuelta y pompón"""
    hx, hy = c
    F.d.chord([*F.P(hx - r * 1.05, hy - r * 1.25), *F.P(hx + r * 1.05, hy + r * 0.55)], 180, 360, fill=col)
    F.rect(hx - r * 1.07, hy - r * 0.48, hx + r * 1.07, hy - r * 0.2, fill=_osc(col, 0.78))          # vuelta
    for i in range(-3, 4): F.line([(hx + i * r * 0.28, hy - r * 0.46), (hx + i * r * 0.28, hy - r * 0.22)], _osc(col, 0.6), r * 0.05)
    F.circle((hx + f * r * 0.15, hy - r * 1.05), r * 0.24, fill=_osc(col, 1.08))                     # pompón

def avatar_dani(F, c, r):
    """foto de perfil: Dani vivo, sonriendo, con su gorro rojo"""
    hx, hy = c
    F.circle((hx, hy), r, fill=(60, 120, 170))
    F.circle((hx, hy + r * 0.12), r * 0.62, fill=(238, 222, 200))
    for dx in (-0.22, 0.22): F.circle((hx + dx * r, hy + r * 0.06), r * 0.07, fill=(30, 30, 40))
    F.arc((hx, hy + r * 0.16), r * 0.28, 25, 155, (30, 30, 40), r * 0.07)
    gorro(F, (hx, hy + r * 0.12), r * 0.62)

def ticks(F, x, y, col, s=1.0):
    """doble check"""
    for dx in (0, 14 * s):
        F.line([(x + dx - 12 * s, y), (x + dx - 5 * s, y + 8 * s), (x + dx + 9 * s, y - 9 * s)], col, 4 * s)

def _ajusta(F, txt, fs, maxw):
    while fs > 18 and F.d.textlength(txt, font=font(fs * S)) / S > maxw: fs -= 2
    return fs

def chat(F, t, msgs, estado="", cx=540, cy=740, vib=0.0, entrada="", cursor=False, on=1.0, barra=True):
    """pantalla de mensajería. msgs: [dict(txt, yo, p (0-1 aparición), tk (0 sin ticks, 1 grises, 2 azules), leido (0-1), rojo)]"""
    cx += noise(t * 60) * 12 * vib
    F.rect(cx - 250, cy - 430, cx + 250, cy + 430, fill=(20, 20, 26), outline=(90, 90, 100), w=8)
    F.rect(cx - 226, cy - 404, cx + 226, cy + 404, fill=_osc((12, 18, 24), on))
    if on <= 0.02: return (cx, cy)
    for yy in range(int(cy - 230), int(cy + 320), 70):                                             # fondo de chat (dibujitos tenues)
        for xx in range(int(cx - 200), int(cx + 220), 80):
            F.circle((xx + (yy // 70 % 2) * 40, yy), 5, fill=_osc((22, 30, 38), on))
    F.text((cx - 160, cy - 375), "3:00", 36, _osc(ROJO, on))
    F.rect(cx + 150, cy - 386, cx + 196, cy - 364, outline=_osc((150, 150, 160), on), w=3)
    F.rect(cx + 154, cy - 382, cx + 166, cy - 368, fill=_osc((220, 60, 60), on))                     # batería baja
    F.rect(cx - 226, cy - 350, cx + 226, cy - 250, fill=_osc((26, 36, 44), on))
    avatar_dani(F, (cx - 160, cy - 300), 36)
    F.text((cx - 60, cy - 316), "DANI", 40, _osc((236, 240, 244), on))
    if estado:
        F.text((cx - 30, cy - 276), estado, 24, _osc((120, 230, 150) if estado != tr("últ. vez: ayer") else (150, 160, 170), on))
    y = cy - 190
    for m in msgs:
        p = ease_back(clamp(m.get("p", 1.0)))
        if p <= 0: continue
        lineas = m["txt"].split("\n")
        fs = 46
        for ln in lineas: fs = min(fs, _ajusta(F, ln, 46, 320))
        h = 58 * len(lineas) + 44
        w = max(F.d.textlength(ln, font=font(fs * S)) / S for ln in lineas) + 50
        w = max(w, 170 if m.get("yo") else 150)
        yo = m.get("yo", False)
        x0 = cx + 206 - w if yo else cx - 206
        col = (40, 110, 80) if yo else (44, 52, 60)
        if m.get("rojo"): col = (110, 20, 26)
        yc = y + h / 2
        F.rect(x0, yc - h / 2 * p, x0 + w, yc + h / 2 * p, fill=_osc(col, on))
        tx = x0 + w / 2
        for k, ln in enumerate(lineas):
            F.text((tx, y + 40 + k * 58 - (1 - p) * 10), ln, fs * p + 1, _osc((240, 242, 246), on))
        if yo and m.get("tk"):
            ticks(F, x0 + w - 30, y + h - 14, TICK if m["tk"] == 2 else (160, 170, 180), 0.9)
        lei = m.get("leido", 0.0)
        if lei > 0:                                                                                 # debajo: "✓✓ LEÍDO" en azul
            s = ease_back(lei)
            ticks(F, x0 + 22, y + h + 26, TICK, 1.1 * s)
            F.text((x0 + 120, y + h + 26), tr("LEÍDO 3:00"), 26 * s + 1, TICK)
            y += 50
        y += h + 26
    if not barra: return (cx, cy)
    # barra de escribir
    F.rect(cx - 210, cy + 320, cx + 140, cy + 384, fill=_osc((36, 44, 52), on))
    F.circle((cx + 178, cy + 352), 32, fill=_osc((40, 160, 110), on))
    F.poly([(cx + 166, cy + 336), (cx + 196, cy + 352), (cx + 166, cy + 368)], fill=_osc((240, 240, 240), on))
    txt = entrada + ("|" if cursor and int(t * 3) % 2 == 0 else "")
    if txt: F.text((cx - 120, cy + 352), txt, 34, _osc((240, 242, 246), on))
    else: F.text((cx - 90, cy + 352), tr("Mensaje"), 30, _osc((110, 120, 130), on))
    return (cx, cy)

def cara_muerto(F, c, r, abre=0.5, t=0.0, gorro_=True):
    """Dani, muerto: cara gris verdosa, ojos hundidos negros con una pupila blanca diminuta que no parpadea, boca entreabierta"""
    hx, hy = c
    F.ellipse((hx, hy + r * 0.1), r * 1.0, r * 1.22, fill=(6, 6, 8))
    F.ellipse((hx, hy + r * 0.1), r * 0.92, r * 1.14, fill=MUERTO)                                  # cara alargada
    for s_ in (-1, 1):                                                                              # pómulos hundidos
        F.ellipse((hx + s_ * r * 0.55, hy + r * 0.5), r * 0.22, r * 0.36, fill=_osc(MUERTO, 0.72))
    for dx, dy in ((-0.34, 0.0), (0.36, -0.04)):                                                    # ojos negros, enormes, desiguales
        F.ellipse((hx + dx * r, hy + dy * r), r * 0.3, r * 0.36, fill=(70, 72, 70))
        F.ellipse((hx + dx * r, hy + dy * r + r * 0.03), r * 0.24, r * 0.32, fill=(2, 2, 4))
        F.circle((hx + dx * r + noise(t * 2, 3) * r * 0.02, hy + dy * r + r * 0.05), r * 0.04, fill=(255, 255, 255))
    for dx, dy in ((-0.34, 0.0), (0.36, -0.04)):                                                    # ojeras que chorrean hacia abajo
        F.line([(hx + dx * r, hy + dy * r + r * 0.3), (hx + dx * r + r * 0.03, hy + dy * r + r * 0.62)], _osc(MUERTO, 0.6), r * 0.08)
    F.ellipse((hx + r * 0.04, hy + r * 0.78), r * 0.07, r * (0.16 + 0.22 * abre), fill=(4, 2, 4))     # boca: rendija larga y torcida
    rr = random.Random(4)
    for _ in range(9):                                                                              # tierra en la cara
        a = rr.uniform(0, 6.28); d = rr.uniform(0.3, 0.85)
        F.circle((hx + math.cos(a) * r * d, hy + math.sin(a) * r * d), r * rr.uniform(0.03, 0.07), fill=TIERRA)
    if gorro_: gorro(F, (hx, hy - r * 0.12), r, col=_osc(GORRO, 0.8))

def dani(F, p, x, y, t=0.0, f=1, sc=1.1, abre=0.2, movil=True, luz_movil=1.0):
    """Dani con el traje del entierro (camisa blanca y corbata), cara de muerto, gorro rojo y su móvil encendido en la mano"""
    old = DANI.scale; DANI.scale = sc
    J = DANI.draw(F, p, x, y, f=f, face="closed", t=t)
    DANI.scale = old
    sx, sy = J["sh"]; nx, ny = J["neck"]
    F.poly([(nx - 9 * sc, ny - 2 * sc), (nx + 9 * sc, ny - 2 * sc), (sx, sy + 26 * sc)], fill=(220, 220, 214))   # camisa
    F.poly([(sx - 4 * sc, sy + 2 * sc), (sx + 4 * sc, sy + 2 * sc), (sx + 3 * sc, sy + 34 * sc), (sx - 3 * sc, sy + 34 * sc)], fill=(20, 20, 24))
    cara_muerto(F, J["head"], L["head"] * sc * 1.05, abre=abre, t=t)
    if movil:
        hx, hy = J["a1h"]
        F.rect(hx - 10 * sc, hy - 24 * sc, hx + 10 * sc, hy + 6 * sc, fill=(18, 18, 22))
        F.rect(hx - 7 * sc, hy - 21 * sc, hx + 7 * sc, hy + 3 * sc, fill=_osc(AZUL, 0.3 + 0.7 * luz_movil))
    return J

def tumba(F, t, brillo=1.0):
    """tumba recién cubierta: lápida con DANI, su gorro rojo colgado y una luz azul que late bajo la tierra (su móvil)"""
    F.rect(-600, 1150, 1700, 2800, fill=(18, 22, 20))
    rr = random.Random(2)
    for i in range(9):                                                                              # lápidas del fondo
        x = -260 + i * 180 + rr.uniform(-40, 40); h = rr.uniform(120, 200); y0 = 1000 + rr.uniform(-20, 30)
        F.rect(x - 40, y0 - h, x + 40, y0, fill=(30, 32, 40)); F.circle((x, y0 - h), 40, fill=(30, 32, 40))
    F.rect(-600, 1000, 1700, 1150, fill=(20, 24, 22))
    F.rect(420, 760, 660, 1130, fill=(104, 106, 112), outline=(50, 50, 56), w=6)                   # lápida
    F.circle((540, 760), 120, fill=(104, 106, 112)); F.rect(426, 760, 654, 800, fill=(104, 106, 112))
    F.text((540, 860), "DANI", 56, (34, 34, 40))
    F.text((540, 930), tr("D.E.P."), 34, (44, 44, 50))
    F.d.chord([*F.P(560, 600), *F.P(660, 710)], 180, 360, fill=GORRO)                               # su gorro, encima de la lápida
    F.rect(558, 650, 662, 668, fill=_osc(GORRO, 0.75)); F.circle((612, 606), 13, fill=GORRO)
    F.ellipse((540, 1170), 330, 70, fill=TIERRA)                                                     # tierra removida
    for i in range(12):
        a = i * 0.52; F.ellipse((540 + math.cos(a) * 230, 1170 + math.sin(a) * 40), 40, 16, fill=_osc(TIERRA, 1.15))
    F.ellipse((540, 1160), 210, 36, fill=_osc(TIERRA, 1.25))
    if brillo > 0:                                                                                  # la pantalla brilla entre la tierra
        F.ellipse((540, 1172), 120 * brillo, 18 * brillo, fill=_osc(AZUL, 0.55 * brillo))
        F.rect(520, 1162, 560, 1176, fill=_osc((210, 235, 255), brillo))
        for dx, dy in ((-40, 4), (10, -6), (52, 8)):
            F.line([(540 + dx, 1172 + dy), (560 + dx, 1166 + dy)], _osc(AZUL, 0.8 * brillo), 4)
    F.circle((880, 330), 60, fill=(210, 214, 228)); F.circle((904, 314), 56, fill=(8, 10, 24))      # luna

def pulgares(F, t, cx, cy, escribe=1.0):
    """tus manos sujetando el móvil (vista en primera persona); los pulgares pulsan solos"""
    PIEL_ = (236, 226, 212)
    for s_ in (-1, 1):
        F.line([(cx + s_ * 420, 1900), (cx + s_ * 300, cy + 560)], TU.shirt, 130)                  # mangas
        F.line([(cx + s_ * 420, 1900), (cx + s_ * 300, cy + 560)], _osc(TU.shirt, 0.6), 8)
        F.ellipse((cx + s_ * 250, cy + 500), 70, 120, fill=PIEL_, outline=(8, 8, 12), w=6)          # palmas a los lados del móvil
        u = (t * 6 + (0.5 if s_ > 0 else 0)) % 1
        tx = cx + s_ * lerp(150, 60, abs(math.sin(t * 8 + s_)) * escribe)
        ty = cy + 420 - 22 * (u < 0.5) * escribe
        F.line([(cx + s_ * 240, cy + 480), (tx, ty)], (8, 8, 12), 58)                               # pulgar (contorno)
        F.line([(cx + s_ * 240, cy + 480), (tx, ty)], PIEL_, 46)
        F.ellipse((tx + s_ * 6, ty - 4), 12, 9, fill=(250, 236, 226))                               # uña

# ---------- escenas ----------
def mensaje(t, D, fi):
    """primer fotograma: el móvil vibrando, 3:00 en rojo, y el mensaje de Dani ya en pantalla"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo("m"), dict(x=540, y=lerp(600, 870, k), z=lerp(1.55, 1.08, k)))
    c = chat(F, t, [dict(txt=tr("ABRE.\nTENGO FRÍO."), p=0.75 + 0.25 * seg(t, 0.0, 0.2))], estado=tr("en línea"),
             vib=1.0 - seg(t, D * 0.3, D * 0.5))
    img = iluminar(F.finish(), F, [], glows=[(c, 620, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=9, flash=(ROJO, 0.4 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.1))

def ayer(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(fondo("n"), dict(x=540, y=lerp(900, 1020, k), z=lerp(1.0, 1.55, k)))
    tumba(F, t, brillo=0.55 + 0.45 * (math.sin(t * 5) > 0) if t > D * 0.35 else 0.0)
    on = t > D * 0.35
    img = iluminar(F.finish(), F, [], glows=[((880, 330), 300, 0.5), ((540, 900), 360, 0.35)] + ([((540, 1170), 300, 0.9)] if on else []),
                   amb=0.22, warm=AZUL)
    return img, dict(grain=11, flash=((255, 255, 255), 0.4 * max(0, 1 - abs(t - D * 0.35) / 0.12)))

def leido(t, D, fi):
    k = ease(seg(t, 0, D))
    lei = seg(t, D * 0.2, D * 0.32)
    est = tr("en línea") if t < D * 0.6 else tr("escribiendo…")
    F = Frame(fondo("m"), dict(x=lerp(540, 450, k), y=lerp(870, 650, k), z=lerp(1.1, 1.7, k)))
    c = chat(F, t, [dict(txt=tr("ABRE.\nTENGO FRÍO."), leido=lei)], estado=est, barra=False)
    img = iluminar(F.finish(), F, [], glows=[(c, 620, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=9, tint=((255, 0, 30), 0.14 * seg(t, D * 0.6, D)))

def calle(t, D, fi):
    """desde tu ventana: abajo, bajo la farola, Dani con el traje y el gorro, la cara iluminada por el móvil, mirando arriba"""
    k = ease(seg(t, D * 0.15, D))
    x0, y0, x1, y1 = 80, 240, 1000, 1220
    F = Frame(fondo("n"), dict(x=lerp(540, 340, k), y=lerp(800, 860, k), z=lerp(1.0, 2.6, k)))
    F.rect(x0, y0, x1, 700, fill=(10, 12, 26))
    for i in range(5):                                                                             # casas de enfrente
        bx = x0 + i * 200; F.rect(bx, 520 - (i % 2) * 60, bx + 180, 760, fill=(18, 20, 32))
        F.rect(bx + 70, 600, bx + 110, 650, fill=(26, 30, 46))
    F.rect(x0, 760, x1, 860, fill=(40, 40, 48))                                                      # acera de enfrente
    F.rect(x0, 860, x1, 1060, fill=(22, 22, 28))                                                     # calzada
    for xx in range(x0, x1, 160): F.rect(xx, 950, xx + 80, 964, fill=(120, 116, 96))
    F.rect(x0, 1060, x1, y1, fill=(46, 46, 54))                                                      # tu acera
    F.line([(780, 1150), (780, 560)], (40, 42, 56), 12); F.line([(780, 560), (700, 560)], (40, 42, 56), 10)   # farola
    F.ellipse((690, 575), 34, 14, fill=(255, 230, 160))
    F.ellipse((560, 1150), 220, 40, fill=(66, 64, 60))                                               # charco de luz
    J = dani(F, pose(body=-6, head=-24, a1u=40, a1l=110, a2u=-6, a2l=4, l1u=4, l1l=-2, l2u=-4, l2l=-2), 330, 1150, t=t, f=1, sc=1.0)
    ventana_marco(F, x0, y0, x1, y1)
    img = iluminar(F.finish(), F, [], glows=[((690, 600), 420, 0.8), (J["a1h"], 150, 0.9), (J["head"], 120, 0.6), ((540, 1230), 140, 0.6)],
                   amb=0.14, warm=(255, 220, 170))
    return img, dict(grain=12, tint=((255, 0, 30), 0.12 * k))

def escribe(t, D, fi):
    """llega otro mensaje, rojo: YA ME HAS LEÍDO. BAJA."""
    llega = seg(t, D * 0.25, D * 0.4)
    hit = llega >= 1
    sh = 10 * hit * (1 - seg(t, D * 0.45, D * 0.7))
    F = Frame(fondo("m"), dict(x=540 + noise(t * 30) * sh, y=880, z=lerp(1.1, 1.25, ease(t / D)), sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    c = chat(F, t, [dict(txt=tr("ABRE.\nTENGO FRÍO."), leido=1.0), dict(txt=tr("YA ME HAS LEÍDO.\nBAJA."), p=llega, rojo=True)],
             estado=tr("escribiendo…") if not hit else tr("en línea"), vib=1.0 if 0 < llega < 1 or (hit and t < D * 0.6) else 0.0)
    img = iluminar(F.finish(), F, [], glows=[(c, 620, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=10, tint=((255, 0, 30), 0.22 * hit), glitch=0.35 if hit and t < D * 0.55 and fi % 3 else 0.0,
                     flash=(ROJO, 0.4 * max(0, 1 - (t - D * 0.4) / 0.2)) if hit else None)

def _bulto(F, t, tiembla=1.0):
    """tú, tapado entero con la manta: un bulto que tiembla"""
    j = noise(t * 18, 5) * 4 * tiembla
    pts = [(CAMA_X0 + 40, COLCHON - 10)] + [(CAMA_X0 + 40 + i * 32, COLCHON - 10 - 70 * math.sin(math.pi * i / 18) ** 0.6 + (j if i % 2 else -j)) for i in range(19)]
    F.poly(pts + [(CAMA_X1 + 8, HUECO - 4), (CAMA_X0 + 30, HUECO - 4)], fill=(60, 72, 120))
    F.line(pts, (90, 104, 160), 6)

def manta(t, D, fi):
    k = ease(seg(t, 0, D))
    tapa = ease(seg(t, 0, D * 0.35))
    F = Frame(fondo(), dict(x=lerp(470, 520, k), y=lerp(PISO - 300, PISO - 260, k), z=lerp(1.2, 1.45, k)))
    _cuarto(F, t)
    if tapa < 1: tu_tumbado(F, t, face="scared", cuelga=0.0, jit=1.5)
    if tapa > 0: _bulto(F, t)
    F.rect(780, PISO - 196, 836, PISO - 186, fill=(16, 16, 20))                                     # tu móvil, boca abajo en la mesilla
    img = iluminar(F.finish(), F, [], glows=[((825, PISO - 222), 160, 0.5), ((420, COLCHON - 40), 380, 0.45)], amb=0.24, warm=(200, 200, 255))
    return img, dict(grain=10, dark=0.06)

def pulgares_(t, D, fi):
    """el móvil se enciende solo; tus pulgares escriben YA BAJO y lo envían (ticks azules al instante)"""
    on = seg(t, D * 0.08, D * 0.18)
    txt = tr("YA BAJO")
    n = int(len(txt) * seg(t, D * 0.3, D * 0.72))
    env = t > D * 0.82
    msgs = [dict(txt=tr("ABRE.\nTENGO FRÍO."), leido=1.0), dict(txt=tr("YA ME HAS LEÍDO.\nBAJA."), rojo=True)]
    if env: msgs.append(dict(txt=txt, yo=True, tk=2, p=seg(t, D * 0.82, D * 0.9)))
    F = Frame(fondo("m"), dict(x=540, y=lerp(860, 900, ease(t / D)), z=1.0))
    c = chat(F, t, msgs, estado=tr("en línea"), entrada="" if env else txt[:n], cursor=not env, on=on, vib=0.3)
    pulgares(F, t, 540, 740, escribe=1.0 if 0.25 * D < t < 0.8 * D else 0.0)
    img = iluminar(F.finish(), F, [], glows=[(c, 640, on)], amb=0.18, warm=AZUL)
    return img, dict(grain=10, flash=((255, 255, 255), 0.5 * max(0, 1 - abs(t - D * 0.12) / 0.12)), tint=((255, 0, 30), 0.18 * env))

def _puerta_abajo(F, x=1080, luz=1.0, sombra=1.0, w=180, h=520, piso=1300):
    """puerta de la calle al pie de la escalera, con un cristal esmerilado; detrás, la silueta con el gorro"""
    F.rect(x - w / 2 - 20, piso - h - 20, x + w / 2 + 20, piso, fill=(44, 36, 30))
    F.rect(x - w / 2, piso - h, x + w / 2, piso, fill=(80, 56, 42), outline=(36, 24, 18), w=4)
    gx0, gy0, gx1, gy1 = x - w / 2 + 30, piso - h + 40, x + w / 2 - 30, piso - h + 260
    F.rect(gx0, gy0, gx1, gy1, fill=_osc((120, 140, 170), 0.5 * luz))
    if sombra > 0:                                                                                   # silueta tras el cristal
        sx = x - 6; c = _osc((12, 12, 16), 1.0)
        F.rect(sx - 40, gy0 + 110, sx + 40, gy1, fill=c)
        F.circle((sx, gy0 + 76), 34, fill=c)
        F.d.chord([*F.P(sx - 36, gy0 + 30), *F.P(sx + 36, gy0 + 100)], 180, 360, fill=_osc(GORRO, 0.55 * sombra))
        F.circle((sx + 4, gy0 + 34), 9, fill=_osc(GORRO, 0.55 * sombra))
    F.circle((x - w / 2 + 24, piso - h / 2 + 30), 9, fill=(196, 168, 96))
    return ((gx0 + gx1) / 2, (gy0 + gy1) / 2)

def bajas(t, D, fi):
    """tus piernas bajan solas, rígidas, con el móvil encendido en la mano; abajo, la silueta tras el cristal"""
    u = 0.15 + 0.6 * ease(seg(t, 0, D * 0.95))
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(430, 760, k), y=lerp(880, 1020, k), z=lerp(1.6, 1.25, k)))
    path = escalera_casa(F)
    g = _puerta_abajo(F, x=1080)
    x, y = path(u)
    ph = math.sin(t * 2 * math.pi * 0.55)
    p = pose(body=4, head=8, a1u=60 + jitter(t, 3, 2).get("a1u", 0), a1l=60, a2u=-4, a2l=2,
             l1u=18 * ph, l1l=-4 - 10 * max(0, -ph), l2u=-18 * ph, l2l=-4 - 10 * max(0, ph))      # paso rígido, de muñeco
    J = TU.draw(F, p, x, y, f=1, face="scared")
    hx, hy = J["a1h"]
    F.rect(hx - 9, hy - 22, hx + 9, hy + 6, fill=(18, 18, 22)); F.rect(hx - 6, hy - 19, hx + 6, hy + 3, fill=AZUL)
    img = iluminar(F.finish(), F, [], glows=[((hx, hy), 160, 0.8), (g, 220, 0.55)], amb=0.16, warm=AZUL)
    return img, dict(grain=11, tint=((255, 0, 30), 0.12 + 0.1 * seg(t, D * 0.5, D)))

def final(t, D, fi):
    """la puerta se abre sola: Dani en el rellano, gris, con el gorro y el móvil encendido. Y la regla"""
    F = Frame(fondo(), dict(x=730, y=lerp(1060, 1040, ease(t / D)), z=2.0))
    paredes(F)
    ab = ease(seg(t, 0.1, D * 0.35))
    puerta_calle(F, abre=0.85 * ab, gira=1, rellano=0.3)
    gap = 150 * ease(0.85 * ab)
    if gap > 30:
        cx = DX1 - gap * 0.45
        F.rect(cx - 40, 950, cx + 40, PISO, fill=(20, 20, 26))                                       # traje
        F.poly([(cx - 9, 950), (cx + 9, 950), (cx, 980)], fill=(220, 220, 214))
        cara_muerto(F, (cx, 910), 40, abre=0.25 + 0.2 * math.sin(t * 2), t=t)
        F.rect(cx + 14, 980, cx + 34, 1020, fill=(18, 18, 22)); F.rect(cx + 17, 983, cx + 31, 1017, fill=AZUL)
    img = iluminar(F.finish(), F, [], glows=[((DX1 - 60, 960), 200, 0.7)], amb=0.14, warm=AZUL)
    pp = ease_back(seg(t, D * 0.5, D * 0.6)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 140, 1040, 560), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 TE ESCRIBE"), 210, 62, (255, 255, 255)), (tr("QUIEN NO PUEDE…"), 290, 62, (255, 255, 255)),
                                 (tr("NO LEAS"), 430, 150, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 1160, 850, 1250), 26, fill=(230, 30, 50))
        d.text((540, 1205), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.25 * pp if pp > 0 else 0), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(mensaje=mensaje, ayer=ayer, leido=leido, calle=calle, escribe=escribe, manta=manta, pulgares=pulgares_,
                 bajas=bajas, final=final)
PAUSA = dict(mensaje=0.4, ayer=0.6, leido=0.5, calle=0.6, escribe=0.7, manta=0.4, pulgares=0.6, bajas=0.6, final=2.4)
