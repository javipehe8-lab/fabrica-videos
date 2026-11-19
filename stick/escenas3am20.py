"""Si oyes esto a las 3AM — 20: "El GPS". Interior del coche en primera persona (como en 3am2) con un GPS pegado al
parabrisas: la ruta se mete por un camino de tierra que no sale en el mapa. En el retrovisor, los faros del coche que
te sigue; pone el intermitente, gira por el camino, sus luces se meten entre los árboles y se apagan.
Piezas nuevas reutilizables: interior_gps, gps_pantalla, camino_lado, espejo_noche."""
import math, random
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU
from escenas3am2 import Sub, arboles

NOCHE_A, NOCHE_B = (12, 14, 30), (4, 4, 8)
_BG = {}
def fondo(k=0):
    if k not in _BG: _BG[k] = gradient(NOCHE_A, NOCHE_B) if k == 0 else gradient((14, 14, 18), (4, 4, 6))
    return _BG[k]

TIERRA = (104, 80, 54)
NARANJA = (255, 150, 30)
GPS = (110, 880, 450, 1120)                  # carcasa del GPS (mundo), pegado abajo a la izquierda del parabrisas
PANT = (124, 894, 436, 1106)                 # pantalla
GC = ((GPS[0] + GPS[2]) / 2, (GPS[1] + GPS[3]) / 2)
ESP = (345, 385, 735, 515)                   # interior del retrovisor

def xr(p): return lerp(558, 1320, p)         # borde derecho de la carretera a la profundidad p (0 horizonte, 1 abajo)
def yr(p): return lerp(820, 1200, p)

def camino_lado(F, u, luces=0.0):
    """camino de tierra que sale a la derecha. u: 0 = muy lejos, 1 = ya lo estás pasando. luces: faros al fondo del camino"""
    pa, pb = clamp(u) ** 2.2, clamp(u + 0.17) ** 2.2
    if pb <= 0.002: return
    A, B = (xr(pa), yr(pa)), (xr(pb), yr(pb))
    V = (1080, 812)
    C, D_ = (lerp(B[0], V[0], 0.8), lerp(B[1], V[1], 0.8)), (lerp(A[0], V[0], 0.8), lerp(A[1], V[1], 0.8))
    F.poly([A, B, C, D_], fill=TIERRA)
    F.poly([(lerp(A[0], D_[0], 0.45), lerp(A[1], D_[1], 0.45)), (lerp(B[0], C[0], 0.45), lerp(B[1], C[1], 0.45)), C, D_], fill=(30, 24, 18))   # se pierde en lo oscuro
    for k in range(2):                                                      # roderas
        f = 0.3 + 0.4 * k
        P0 = (lerp(A[0], B[0], f), lerp(A[1], B[1], f)); P1 = (lerp(D_[0], C[0], f), lerp(D_[1], C[1], f))
        F.line([P0, (lerp(P0[0], P1[0], 0.5), lerp(P0[1], P1[1], 0.5))], (44, 34, 24), 3 + 10 * pb)
    # árboles altos a los dos lados del camino (lo convierten en un túnel)
    for (P, Q), s_ in (((A, D_), -1), ((B, C), 1)):
        for i in range(4):
            f = 0.1 + i * 0.22
            x, y = lerp(P[0], Q[0], f), lerp(P[1], Q[1], f)
            h = (60 + 520 * pb) * (1 - f * 0.6)
            F.poly([(x, y - h), (x + h * 0.22, y + 4), (x - h * 0.22, y + 4)], fill=(5, 6, 10))
    # poste torcido en la entrada, sin cartel
    F.line([(A[0] + 10, A[1]), (A[0] + 4, A[1] - 40 - 260 * pa)], (40, 34, 30), 3 + 12 * pa)
    if luces > 0:                                                           # dos faros encendidos al fondo, mirándote
        c = (lerp(A[0], D_[0], 0.6) + lerp(B[0], C[0], 0.6)) / 2, (lerp(A[1], D_[1], 0.6) + lerp(B[1], C[1], 0.6)) / 2
        for dx in (-1, 1): F.circle((c[0] + dx * (10 + 26 * pb), c[1] - 4), (5 + 12 * pb) * luces, fill=(255, 250, 220))
    return dict(centro=((A[0] + C[0]) / 2, (A[1] + C[1]) / 2), luces=c if luces > 0 else None)

def flecha_der(F, cx, cy, s, col):
    """flecha de giro a la derecha (tallo hacia arriba y punta a la derecha)"""
    F.line([(cx - s * 0.5, cy + s * 0.7), (cx - s * 0.5, cy - s * 0.05), (cx + s * 0.25, cy - s * 0.05)], col, s * 0.28, round_=False)
    F.poly([(cx + s * 0.2, cy - s * 0.45), (cx + s * 0.75, cy - s * 0.05), (cx + s * 0.2, cy + s * 0.35)], fill=col)

def gps_pantalla(F, t, modo="giro", dist=200, flash=0.0, glitch=0.0):
    """modo: giro (ruta normal), vacio (la ruta gira hacia la nada), completa (RUTA COMPLETADA), apagada"""
    F.rect(GPS[0], GPS[1], GPS[2], GPS[3], fill=(16, 16, 18), outline=(54, 54, 60), w=6)
    F.line([(GC[0], GPS[1]), (GC[0] + 30, GPS[1] - 70)], (30, 30, 34), 16)          # brazo de la ventosa
    F.circle((GC[0] + 34, GPS[1] - 78), 22, fill=(40, 40, 46))
    M = Sub(F, *PANT, fill=(34, 42, 54))
    x0, y0, x1, y1 = PANT
    if modo == "apagada":
        for k in range(10):                                                         # estática
            yy = y0 + random.Random(int(t * 30) * 13 + k).uniform(0, y1 - y0)
            M.line([(x0, yy), (x1, yy)], (70, 74, 80), 2)
        M.pegar(); return
    rx = (x0 + x1) / 2 - 20
    # calles del mapa (a la izquierda sí hay calles; a la derecha, nada)
    for yy in (980, 1040):
        M.line([(x0, yy), (rx, yy)], (70, 80, 96), 7)
    M.line([(x0 + 40, y0 + 60), (x0 + 40, y1)], (70, 80, 96), 6)
    M.rect(rx + 30, y0 + 58, x1, y1 - 34, fill=(48, 50, 54))                      # zona gris sin datos
    for k in range(6):
        M.line([(rx + 30 + k * 40, y0 + 58), (rx + 30 + k * 40 - 60, y1 - 34)], (54, 56, 60), 3)
    M.line([(rx, y1), (rx, y0 + 40)], (120, 128, 140), 14)                         # tu carretera
    ty = 990                                                                         # punto del giro
    rojo = modo == "otra"
    if modo in ("giro", "vacio", "otra"):
        M.line([(rx, 1080), (rx, ty)], (60, 150, 255), 10)
        M.line([(rx, ty), (x1 + 10, ty - 10)], (60, 150, 255) if not rojo else (255, 60, 60), 10)   # la ruta se mete en el gris
    if modo == "completa":
        M.line([(rx, 1080), (rx, ty)], (60, 150, 255), 10); M.line([(rx, ty), (rx + 90, ty - 4)], (60, 150, 255), 10)
        M.line([(rx + 92, ty - 4), (rx + 92, ty - 40)], (230, 230, 230), 3); M.poly([(rx + 92, ty - 40), (rx + 118, ty - 32), (rx + 92, ty - 24)], fill=(60, 200, 90))
    M.poly([(rx, 1052), (rx - 14, 1080), (rx, 1072), (rx + 14, 1080)], fill=(255, 255, 255))   # tu coche
    # banner de arriba
    if modo == "completa":
        M.rect(x0, y0, x1, y0 + 56, fill=(30, 150, 70))
        M.text(((x0 + x1) / 2, y0 + 28), tr("RUTA COMPLETADA"), 21, (255, 255, 255))
    else:
        col = (40, 110, 200) if not rojo else (190, 30, 40)
        col = tuple(int(lerp(c, h, flash)) for c, h in zip(col, (230, 30, 40)))
        M.rect(x0, y0, x1, y0 + 56, fill=col)
        flecha_der(M, x0 + 34, y0 + 30, 30, (255, 255, 255))
        M.text(((x0 + x1) / 2 + 26, y0 + 18), "%d m" % dist, 17, (255, 255, 255))
        M.text(((x0 + x1) / 2 + 26, y0 + 40), tr("GIRE A LA DERECHA"), 15, (255, 255, 255))
    # barra de abajo: la hora en rojo
    M.rect(x0, y1 - 34, x1, y1, fill=(14, 16, 20))
    M.text((x0 + 50, y1 - 17), "3:00", 22, (255, 50, 50))
    M.text((x1 - 70, y1 - 17), tr("LLEGADA") if modo != "completa" else "OK", 14, (180, 186, 196))
    if glitch > 0:
        r = random.Random(int(t * 30))
        for k in range(int(6 * glitch)):
            yy = r.uniform(y0, y1); M.rect(x0, yy, x1, yy + r.uniform(3, 14), fill=(r.randint(100, 255), 30, 40))
    M.pegar()

def espejo_noche(F, t, coche=None, intermit=False, gira=0.0, hueco=1.0, apaga=0.0, troncos=0.0):
    """retrovisor: carretera de detrás con el hueco del camino a la derecha.
    coche: distancia (0 cerca, 1 lejos) o None; gira 0-1: se mete por el camino; apaga: 1 = luces apagadas"""
    F.line([(540, 330), (540, 380)], (30, 30, 34), 18)
    F.rect(ESP[0] - 16, ESP[1] - 16, ESP[2] + 16, ESP[3] + 16, fill=(8, 8, 10), outline=(46, 46, 52), w=8)
    M = Sub(F, *ESP, fill=(10, 12, 22))
    hz = 438
    M.rect(345, 385, 735, hz, fill=(18, 22, 40))
    M.poly([(536, hz), (554, hz), (700, 515), (390, 515)], fill=(22, 22, 28))       # carretera de detrás
    arboles(M, 345, 735, hz + 2, seed=11, col=(4, 5, 9), hmin=18, hmax=44)
    gx = 600                                                                         # el hueco del camino de tierra (a la derecha)
    if hueco > 0: M.poly([(552, hz + 6), (566, hz + 9), (gx + 40, hz - 2), (gx + 20, hz - 4)], fill=(44, 34, 24))
    luces = []
    if coche is not None and apaga < 1:
        d = clamp(coche)
        cx, cy, s, r = lerp(548, 552, d), lerp(470, hz + 6, d), lerp(34, 8, d), lerp(12, 3.5, d)
        g = ease(gira)
        cx, cy = lerp(cx, gx + 32, g), lerp(cy, hz - 4, g); s *= (1 - 0.55 * g); r *= (1 - 0.45 * g)
        on = 1 - apaga
        for dx in (-1, 1):
            c = tuple(int(v * on) for v in (255, 252, 230))
            M.circle((cx + dx * s, cy), r * (0.7 + 0.3 * on), fill=c); luces.append((cx + dx * s, cy))
        if intermit and (t * 2.6) % 1 < 0.5:
            M.circle((cx + s + r * 1.6, cy + r * 0.2), r * 0.75, fill=NARANJA)
    if troncos > 0:                                                                  # troncos que tapan las luces dentro del bosque
        for k in range(7):
            tx = gx + 10 + k * 9 - (t * 6 * troncos) % 9
            M.line([(tx, hz - 30), (tx + 1, hz + 4)], (3, 3, 6), 4)
    M.rect(345, 474, 735, 515, fill=(18, 18, 24))                                   # respaldo trasero
    for hx in (460, 620): M.rect(hx - 30, 456, hx + 30, 490, fill=(24, 24, 30))
    M.pegar()
    return luces

def interior_gps(F, t, speed=1.0, camino=None, luces_camino=0.0, gps=None, espejo=None):
    """parabrisas con la carretera de bosque, el camino de tierra (camino = u), el GPS y el retrovisor"""
    F.rect(-600, -300, 1700, 2400, fill=(10, 12, 26))
    F.rect(-600, 820, 1700, 1200, fill=(8, 8, 10))
    F.circle((900, 520), 40, fill=(190, 196, 214))
    arboles(F, -600, 1700, 830, seed=4, off=t * speed * 60, col=(4, 5, 9), hmin=60, hmax=150)
    F.poly([(522, 820), (558, 820), (1320, 1200), (-240, 1200)], fill=(26, 26, 32))
    for k in range(7):
        u = ((k + t * speed * 1.4) % 7) / 7; p0, p1 = u ** 2.2, min(1, (u + 0.05) ** 2.2)
        F.line([(540, lerp(820, 1200, p0)), (540, lerp(820, 1200, p1))], (210, 200, 140), lerp(2, 26, p0), round_=False)
    c = camino_lado(F, camino, luces_camino) if camino is not None else None
    # carrocería por dentro
    F.rect(-600, -300, 1700, 330, fill=(16, 16, 20))
    F.poly([(-600, 330), (70, 330), (-90, 1200), (-600, 1200)], fill=(13, 13, 17))
    F.poly([(1010, 330), (1700, 330), (1700, 1200), (1170, 1200)], fill=(13, 13, 17))
    F.ellipse((330, 1170), 330, 80, fill=(22, 22, 26))
    F.rect(-600, 1160, 1700, 2400, fill=(18, 18, 22)); F.line([(-600, 1160), (1700, 1160)], (44, 44, 52), 6)
    F.circle((330, 1520), 250, outline=(34, 34, 38), w=42)
    for a in (200, 340, 90):
        r_ = math.radians(a); F.line([(330, 1520), (330 + math.cos(r_) * 240, 1520 + math.sin(r_) * 240)], (30, 30, 34), 30)
    F.circle((330, 1520), 70, fill=(28, 28, 32))
    for hx in (120, 540):
        F.line([(hx - 80 + (0 if hx < 300 else 160), 2000), (hx, 1400)], TU.shirt, 74); F.circle((hx, 1390), 38, fill=(240, 240, 240))
    gps_pantalla(F, t, **(gps or {}))
    l = espejo_noche(F, t, **(espejo or {}))
    return dict(espejo=(540, 450), gps=GC, luces=l, camino=c["centro"] if c else None)

def _gl(c, gps_it=0.9, esp_it=0.5, extra=()):
    gl = [(c["gps"], 230, gps_it), (c["espejo"], 230, esp_it), ((540, 1020), 420, 0.5)]
    return gl + list(extra)

# ---------- escenas ----------
def gps(t, D, fi):
    k = ease(seg(t, 0.4, D * 0.85))
    F = Frame(fondo(), dict(x=lerp(GC[0], 470, k), y=lerp(GC[1], 860, k), z=lerp(3.1, 1.2, k), sx=noise(t * 3) * 3))
    c = interior_gps(F, t, gps=dict(modo="giro", dist=int(lerp(400, 250, t / D))), espejo=dict(coche=0.75))
    img = iluminar(F.finish(), F, [], glows=_gl(c, 1.0, 0.6), amb=0.45, warm=(160, 200, 255))
    return img, dict(grain=9, tint=((255, 30, 40), 0.2 * (1 - seg(t, 0, D * 0.5))))

def camino(t, D, fi):
    u = lerp(0.35, 0.75, t / D)
    k = ease(seg(t, D * 0.5, D * 0.75))
    F = Frame(fondo(), dict(x=lerp(820, GC[0] + 40, k), y=lerp(900, GC[1], k), z=lerp(1.5, 2.8, k), sx=noise(t * 3) * 3))
    c = interior_gps(F, t, camino=u, gps=dict(modo="vacio", dist=int(lerp(150, 40, t / D))), espejo=dict(coche=0.75))
    img = iluminar(F.finish(), F, [], glows=_gl(c, 1.0, 0.4, [(c["camino"], 260, 0.35)]), amb=0.47, warm=(160, 200, 255))
    return img, dict(grain=9, tint=((255, 0, 30), 0.12 * seg(t, D * 0.75, D)))

def detras(t, D, fi):
    k = ease(seg(t, D * 0.25, D))
    F = Frame(fondo(), dict(x=540, y=lerp(620, 455, k), z=lerp(1.6, 3.0, k), sx=noise(t * 3) * 3))
    c = interior_gps(F, t, camino=lerp(0.8, 1.2, seg(t, 0, D * 0.4)), gps=dict(modo="vacio", dist=0), espejo=dict(coche=0.72 + 0.02 * noise(t)))
    img = iluminar(F.finish(), F, [], glows=_gl(c, 0.7, 0.9, [(p, 30, 1.0) for p in c["luces"]]), amb=0.43, warm=(255, 250, 230))
    return img, dict(grain=9)

def insiste(t, D, fi):
    rate = lerp(1.5, 9.0, seg(t, 1.0, D))
    fl = 1.0 if (t * rate) % 1 < 0.5 and t > 1.4 else 0.0
    sh = 6 * seg(t, D * 0.4, D)
    F = Frame(fondo(), dict(x=GC[0], y=GC[1] - 20, z=lerp(2.6, 3.2, ease(t / D)), sx=noise(t * 30, 1) * sh, sy=noise(t * 30, 2) * sh))
    c = interior_gps(F, t, gps=dict(modo="vacio", dist=-int(lerp(40, 260, t / D)), flash=fl, glitch=seg(t, D * 0.7, D)), espejo=dict(coche=0.7))
    img = iluminar(F.finish(), F, [], glows=_gl(c, 0.8 + 0.2 * fl, 0.3), amb=0.40, warm=(255, 120, 120))
    return img, dict(grain=11, tint=((255, 0, 30), 0.1 + 0.15 * fl), glitch=0.3 if t > D * 0.75 and fi % 3 == 0 else 0.0)

def gira(t, D, fi):
    g = seg(t, D * 0.66, D * 0.9)
    F = Frame(fondo(), dict(x=lerp(540, 570, g), y=lerp(452, 440, g), z=lerp(3.4, 4.2, ease(t / D)), sx=noise(t * 3) * 2))
    c = interior_gps(F, t, gps=dict(modo="vacio", dist=-300), espejo=dict(coche=lerp(0.6, 0.85, seg(t, 0, D * 0.66)), intermit=t > D * 0.22, gira=g))
    img = iluminar(F.finish(), F, [], glows=_gl(c, 0.3, 0.9, [(p, 26, 1.0) for p in c["luces"]]), amb=0.41, warm=(255, 240, 200))
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * g))

def apagan(t, D, fi):
    off = t > D * 0.68
    F = Frame(fondo(), dict(x=600, y=438, z=lerp(6.0, 7.2, ease(t / D)), sx=noise(t * 3) * 2))
    pr = seg(t, 0, D * 0.68)
    c = interior_gps(F, t, gps=dict(modo="vacio", dist=-400),
                     espejo=dict(coche=0.85 + 0.15 * pr, gira=1.0, apaga=1.0 if off else 0.25 * pr, troncos=0.4 + pr))
    img = iluminar(F.finish(), F, [], glows=_gl(c, 0.1, 0.8 if not off else 0.35, [(p, 18, 1.0) for p in c["luces"]]), amb=0.39, warm=(255, 240, 200))
    hit = t > D * 0.68 and t < D * 0.68 + 0.12
    return img, dict(grain=12, dark=0.25 if off else 0.0, glitch=0.4 if hit else 0.0, tint=((255, 0, 30), 0.2 if off else 0.0))

def completa(t, D, fi):
    on = t > 2.95
    F = Frame(fondo(), dict(x=GC[0], y=GC[1] - 10, z=lerp(2.6, 3.0, ease(t / D))))
    c = interior_gps(F, t, speed=1.0, gps=dict(modo="completa" if on else "apagada"), espejo=dict(coche=None, hueco=0.3))
    img = iluminar(F.finish(), F, [], glows=_gl(c, 0.9 if on else 0.35, 0.2), amb=0.37, warm=(160, 255, 190) if on else (160, 200, 255))
    return img, dict(grain=10, tint=((60, 255, 120), 0.08) if on else None)

def otra(t, D, fi):
    u = lerp(0.2, 0.62, t / D)
    lu = ease(seg(t, D * 0.78, D * 0.84))
    k = ease(seg(t, D * 0.55, D))
    rate = 2.5
    fl = 1.0 if (t * rate) % 1 < 0.5 else 0.0
    F = Frame(fondo(), dict(x=lerp(560, 860, k), y=lerp(880, 880, k), z=lerp(1.15, 2.0, k), sx=noise(t * 3) * 3))
    c = interior_gps(F, t, camino=u, luces_camino=lu, gps=dict(modo="otra", dist=int(lerp(300, 120, t / D)), flash=fl), espejo=dict(coche=None, hueco=0.0))
    ex = [(c["camino"], 260, 0.3)] + ([(c["camino"], 120, 0.9 * lu)] if lu > 0 else [])
    img = iluminar(F.finish(), F, [], glows=_gl(c, 0.8 + 0.2 * fl, 0.25, ex), amb=0.45, warm=(255, 140, 140))
    return img, dict(grain=10, tint=((255, 0, 30), 0.08 + 0.15 * lu), glitch=0.3 if lu > 0 and t < D * 0.88 and fi % 3 == 0 else 0.0)

def final(t, D, fi):
    fl = 1.0 if (t * 3) % 1 < 0.5 else 0.0
    F = Frame(fondo(), dict(x=GC[0] + 60, y=1150, z=lerp(1.9, 2.1, ease(t / D))))
    c = interior_gps(F, t, camino=0.5, luces_camino=1.0, gps=dict(modo="otra", dist=50, flash=fl), espejo=dict(coche=None, hueco=0.0))
    img = iluminar(F.finish(), F, [], glows=_gl(c, 0.8 + 0.2 * fl, 0.2), amb=0.37, warm=(255, 140, 140))
    pp = ease_back(seg(t, D * 0.38, D * 0.48)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d_ = ImageDraw.Draw(img)
        d_.rounded_rectangle((40, 1150, 1040, 1600), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3 EL GPS"), 1210, 66, (255, 255, 255)), (tr("INSISTE…"), 1290, 66, (255, 255, 255)),
                                 (tr("NO GIRES"), 1450, 150, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d_.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d_.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d_.rounded_rectangle((230, 1640, 850, 1730), 26, fill=(230, 30, 50))
        d_.text((540, 1685), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.2 * pp if pp > 0 else 0.1), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(gps=gps, camino=camino, detras=detras, insiste=insiste, gira=gira, apagan=apagan, completa=completa, otra=otra, final=final)
PAUSA = dict(gps=0.5, camino=0.6, detras=0.6, insiste=0.7, gira=0.7, apagan=1.0, completa=0.9, otra=0.8, final=2.4)
