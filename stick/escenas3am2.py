"""Si oyes esto a las 3AM — 2: "El asiento de atrás". Carretera de noche: interior del coche en primera persona
(retrovisor, reloj 3:00), coche visto de lado con el interior a la vista, el coche que da las largas y la cosa de atrás.
Piezas nuevas reutilizables: interior_coche, coche_lado, arboles, cara_palida, Sub (dibujo recortado en un rectángulo)."""
import math, random
from PIL import Image, ImageDraw
from motor import *
from escenas2 import big, carretera
from escenas5 import iluminar
from escenas8 import coche_draw
from escenas3am1 import TU, reloj_3am

CONDUCTOR = Fig(shirt=(150, 118, 70), limb=(236, 226, 212))
PIEL = (186, 186, 182)                 # piel de la cosa
NOCHE_A, NOCHE_B = (12, 14, 30), (4, 4, 8)
_BG = {}
def fondo(k=0):
    if k not in _BG: _BG[k] = gradient(NOCHE_A, NOCHE_B) if k == 0 else gradient((14, 14, 18), (4, 4, 6))
    return _BG[k]

def pulsos(t, tiempos, dec=0.32):
    """intensidad de las largas: pico al encender y caída rápida. Devuelve (luz, tiempo desde el último pulso)"""
    luz, dt = 0.0, 99.0
    for a in tiempos:
        if t >= a:
            dt = t - a; luz = max(luz, math.exp(-dt / dec) * min(1, dt / 0.03 + 0.2))
    return luz, dt

class Sub(Frame):
    """lienzo pequeño (recortado) en coordenadas de mundo: se pega luego sobre el Frame principal"""
    def __init__(self, F, x0, y0, x1, y1, fill=(0, 0, 0)):
        self.F, self.x0, self.y0, self.z, self.sx, self.sy = F, x0, y0, F.z, 0, 0
        w, h = int((x1 - x0) * F.z * S) + 1, int((y1 - y0) * F.z * S) + 1
        self.img = Image.new("RGB", (max(1, w), max(1, h)), fill); self.d = ImageDraw.Draw(self.img)
    def P(self, x, y): return ((x - self.x0) * self.z * S, (y - self.y0) * self.z * S)
    def pegar(self):
        px, py = self.F.P(self.x0, self.y0); self.F.img.paste(self.img, (int(px), int(py)))

def cara_palida(F, c, r, abre=1.0):
    """cara de la cosa: alargada, gris, ojos negros hundidos y boca abierta (sin sonrisa)"""
    hx, hy = c
    F.ellipse((hx, hy + r * 0.1), r * 0.74, r * 1.32, fill=PIEL)
    F.d.chord([*F.P(hx - r * 0.8, hy - r * 1.3), *F.P(hx + r * 0.8, hy + r * 0.2)], 180, 360, fill=(22, 22, 26))   # pelo negro y lacio
    for s_ in (-1, 1): F.line([(hx + s_ * r * 0.72, hy - r * 0.5), (hx + s_ * r * 0.8, hy + r * 1.1)], (22, 22, 26), r * 0.22)
    for dx in (-0.3, 0.3):
        F.ellipse((hx + dx * r, hy - r * 0.02), r * 0.25, r * 0.3, fill=(150, 146, 144))    # ojeras
        F.ellipse((hx + dx * r, hy + r * 0.04), r * 0.21, r * 0.3, fill=(2, 2, 4))
    F.ellipse((hx, hy + r * 0.82), r * 0.07, r * (0.12 + 0.22 * abre), fill=(2, 2, 4))          # boca: rendija oscura
    for s_ in (-1, 1):                                                              # melena negra que le tapa media cara
        F.poly([(hx + s_ * r * 0.15, hy - r * 1.25), (hx + s_ * r * 1.0, hy - r * 0.9), (hx + s_ * r * 1.15, hy + r * 1.9),
                (hx + s_ * r * 0.62, hy + r * 1.7), (hx + s_ * r * 0.55, hy - r * 0.35), (hx + s_ * r * 0.2, hy - r * 0.6)], fill=(14, 14, 18))

def dedos(F, pts0, ang, n=4, L_=60, w=6):
    """dedos largos y finos (pálidos) desde un punto, abriéndose en abanico"""
    x, y = pts0
    for i in range(n):
        a = math.radians(ang + (i - (n - 1) / 2) * 14)
        m = (x + math.cos(a) * L_ * 0.55, y + math.sin(a) * L_ * 0.55)
        e = (x + math.cos(a + 0.35) * L_, y + math.sin(a + 0.35) * L_)
        F.line([(x, y), m, e], PIEL, w)

def arboles(F, x0, x1, piso, seed=0, off=0.0, col=(6, 8, 14), hmin=180, hmax=380):
    r = random.Random(seed); x = x0 - (off % 260)
    while x < x1 + 260:
        h = r.randint(hmin, hmax); w = h * 0.42
        F.poly([(x, piso - h), (x + w / 2, piso), (x - w / 2, piso)], fill=col)
        x += r.randint(90, 200)

# ---------- interior en primera persona ----------
ESP = (345, 385, 735, 515)            # interior del retrovisor (mundo)
def interior_coche(F, t, luz=0.0, speed=1.0, cosa=0.0, sombra=None, manos=0.0, reloj=True):
    """parabrisas con la carretera, salpicadero con el reloj 3:00, volante con tus manos y el retrovisor.
    luz: largas del coche de detrás (0-1); cosa: 0 = nada, 1 = la cara de la cosa en el retrovisor;
    sombra: None o 0-1 (silueta de cabeza recortada contra la luna trasera, 1 = agachada); manos: dedos que entran por los lados"""
    F.rect(-600, -300, 1700, 2400, fill=(10, 12, 26))
    F.rect(-600, 820, 1700, 1200, fill=(8, 8, 10))
    arboles(F, -600, 1700, 830, seed=4, off=t * speed * 60, col=(4, 5, 9), hmin=60, hmax=150)
    F.poly([(522, 820), (558, 820), (1320, 1200), (-240, 1200)], fill=(26, 26, 32))
    for k in range(7):                                   # línea central que se acerca
        u = ((k + t * speed * 1.4) % 7) / 7; p0, p1 = u ** 2.2, min(1, (u + 0.05) ** 2.2)
        F.line([(540, lerp(820, 1200, p0)), (540, lerp(820, 1200, p1))], (210, 200, 140), lerp(2, 26, p0), round_=False)
    # carrocería por dentro
    F.rect(-600, -300, 1700, 330, fill=(16, 16, 20))
    F.poly([(-600, 330), (70, 330), (-90, 1200), (-600, 1200)], fill=(13, 13, 17))
    F.poly([(1010, 330), (1700, 330), (1700, 1200), (1170, 1200)], fill=(13, 13, 17))
    F.ellipse((330, 1170), 330, 80, fill=(22, 22, 26))
    F.rect(-600, 1160, 1700, 2400, fill=(18, 18, 22)); F.line([(-600, 1160), (1700, 1160)], (44, 44, 52), 6)
    if reloj: reloj_3am(F, 790, 1250, 0.42)
    # volante y manos
    F.circle((330, 1520), 250, outline=(34, 34, 38), w=42)
    for a in (200, 340, 90):
        r_ = math.radians(a); F.line([(330, 1520), (330 + math.cos(r_) * 240, 1520 + math.sin(r_) * 240)], (30, 30, 34), 30)
    F.circle((330, 1520), 70, fill=(28, 28, 32))
    tb = noise(t * 30, 3) * 3 * (luz > 0.3)
    for hx in (120, 540):
        F.line([(hx - 80 + (0 if hx < 300 else 160), 2000), (hx, 1400 + tb)], TU.shirt, 74); F.circle((hx, 1390 + tb), 38, fill=(240, 240, 240))
    # retrovisor
    F.line([(540, 330), (540, 380)], (30, 30, 34), 18)
    F.rect(ESP[0] - 16, ESP[1] - 16, ESP[2] + 16, ESP[3] + 16, fill=(8, 8, 10), outline=(46, 46, 52), w=8)
    M = Sub(F, *ESP, fill=(14, 14, 20))
    v = lambda c, k: tuple(int(lerp(a, b, k)) for a, b in zip(c[0], c[1]))
    M.rect(400, 392, 690, 478, fill=v(((44, 50, 74), (250, 248, 236)), luz))                  # luna trasera
    for hx in ((490, 600) if cosa <= 0 else ()):                                               # faros del coche de detrás
        M.circle((hx, 448), 10 + 22 * luz, fill=(255, 252, 235) if luz > 0.05 else (70, 70, 60))
    if sombra is not None:                                                                     # alguien agachándose
        sy = lerp(420, 520, sombra)
        M.circle((585, sy), 34, fill=(6, 6, 8)); M.rect(545, sy + 20, 625, sy + 120, fill=(6, 6, 8))
    M.rect(345, 470, 735, 515, fill=v(((18, 18, 24), (90, 88, 84)), luz * 0.6))                # respaldo trasero
    if cosa <= 0:
      for hx in (460, 620): M.rect(hx - 30, 452, hx + 30, 488, fill=v(((24, 24, 30), (110, 108, 104)), luz * 0.6))
    if cosa > 0:                                                                               # la cosa, sentada justo detrás
        cy = lerp(600, 455, ease(cosa))
        M.rect(420, cy + 50, 660, 560, fill=(10, 10, 12))
        cara_palida(M, (540, cy), 46, abre=0.4 + 0.6 * cosa)
    M.pegar()
    if manos > 0:                                                                              # dedos que rodean tu asiento
        for s_ in (-1, 1):
            bx = 540 + s_ * lerp(760, 420, ease(manos))
            dedos(F, (bx, 780), 0 if s_ < 0 else 180, n=4, L_=120, w=12)
    return dict(espejo=(540, 450))

# ---------- coche visto de lado, con el interior a la vista ----------
AZUL, AZUL_O = (44, 64, 104), (22, 32, 54)
def coche_lado(F, x, piso, t=0.0, cara=0.0, dedos_k=0.0, tu_face="neutral", girado=0.0, mano=0.0):
    """tu coche (morro a la izquierda). cara: la cosa asoma tras tu asiento (0-1); dedos_k: dedos sobre tu reposacabezas;
    mano: mano pálida apoyada en la ventanilla trasera"""
    cab = [(x - 170, piso - 170), (x - 95, piso - 300), (x + 150, piso - 300), (x + 255, piso - 170)]
    F.poly(cab, fill=(12, 12, 18))
    F.rect(x + 145, piso - 255, x + 185, piso - 150, fill=(30, 28, 32))                      # asiento trasero
    if cara > 0:
        cy = lerp(piso - 120, piso - 240, ease(cara))
        F.rect(x + 50, cy + 40, x + 130, piso - 150, fill=(14, 14, 16))
        cara_palida(F, (x + 92, cy), 34, abre=cara)
    F.rect(x - 8, piso - 245, x + 22, piso - 150, fill=(32, 30, 34)); F.rect(x - 4, piso - 288, x + 20, piso - 250, fill=(32, 30, 34))
    J = TU.draw(F, pose(body=-4 + girado * 10, head=girado * 30, l1u=90, l1l=-90, l2u=86, l2l=-86, a1u=78, a1l=-6, a2u=70, a2l=-2),
                x - 55, piso - 72, f=-1 if girado < 0.5 else 1, face=tu_face, t=t)
    F.line([(x - 132, piso - 238), (x - 112, piso - 178)], (20, 20, 24), 12)                  # volante
    if dedos_k > 0:
        for i in range(4):
            F.line([(x + 52, piso - 262 + i * 8), (x + 28, piso - 294 + i * 2), (x + 6, piso - 282 + i * 3 + 8 * (1 - dedos_k))], PIEL, 5)
    if mano > 0:
        mx, my = x + 205, lerp(piso - 150, piso - 230, ease(mano))
        F.ellipse((mx, my), 22, 26, fill=PIEL)
        for i in range(4): F.line([(mx - 14 + i * 9, my - 18), (mx - 20 + i * 10, my - 64 - (i % 2) * 8)], PIEL, 6)
    F.poly([(x - 315, piso - 170), (x + 300, piso - 170), (x + 300, piso - 50), (x - 315, piso - 50)], fill=AZUL, outline=AZUL_O, w=6)
    F.line(cab + [cab[0]], AZUL_O, 12); F.line([(x + 40, piso - 300), (x + 40, piso - 170)], AZUL, 14)
    F.line([(x + 40, piso - 150), (x + 40, piso - 60)], AZUL_O, 4); F.rect(x - 10, piso - 140, x + 20, piso - 130, fill=(150, 160, 180))
    F.rect(x - 318, piso - 150, x - 296, piso - 118, fill=(255, 240, 190)); F.rect(x + 280, piso - 150, x + 302, piso - 118, fill=(220, 30, 30))
    for wx in (x - 190, x + 175):
        F.circle((wx, piso - 46), 50, fill=(18, 18, 22)); F.circle((wx, piso - 46), 21, fill=(110, 110, 116))
        a = -t * 14; F.line([(wx + math.cos(a) * 20, piso - 46 + math.sin(a) * 20), (wx - math.cos(a) * 20, piso - 46 - math.sin(a) * 20)], (40, 40, 44), 5)
    return J

def haz_faros(F, x, piso, luz):
    """haz de los faros del coche de detrás (sale a la izquierda)"""
    if luz <= 0.02: return
    c = tuple(int(v * luz) for v in (70, 68, 46))
    F.poly([(x - 290, piso - 140), (x - 1200, piso - 330), (x - 1200, piso + 60), (x - 290, piso - 110)], fill=c)

def exterior(F, t, piso=1200, speed=0.0, seed=7):
    F.circle((880, 380), 60, fill=(210, 214, 228))
    arboles(F, -900, 2200, piso - 40, seed=seed, off=t * speed * 0.35)
    F.rect(-900, piso - 40, 2200, piso - 20, fill=(20, 22, 18))
    carretera(F, t, speed=speed, y=piso - 20)

# ---------- escenas ----------
def carretera_(t, D, fi):
    k = ease(seg(t, 0.15, D * 0.5))
    F = Frame(fondo(), dict(x=lerp(790, 540, k), y=lerp(1250, 940, k), z=lerp(3.2, 1.0, k), sx=noise(t * 3) * 3))
    luz, _ = pulsos(t, [D * 0.55, D * 0.72, D * 0.86])
    c = interior_coche(F, t, luz=luz, speed=1.0)
    img = iluminar(F.finish(), F, [], glows=[((790, 1250), 240, 0.8), ((540, 1050), 420, 0.55), (c["espejo"], 260 + 500 * luz, 0.4 + 0.6 * luz)],
                   amb=0.3 + 0.4 * luz, warm=(255, 120, 120))
    return img, dict(grain=9, flash=((255, 255, 250), 0.3 * luz), dark=0.25 * (1 - k),
                     tint=((255, 30, 40), 0.2 * (1 - seg(t, 0, D * 0.4))))

def largas(t, D, fi):
    F = Frame(fondo(), dict(x=540, y=lerp(600, 560, ease(t / D)), z=lerp(1.75, 2.05, ease(t / D)), sx=noise(t * 25) * 3))
    T_ = [D * 0.04, D * 0.3, D * 0.53, D * 0.76]
    luz, dt = pulsos(t, T_)
    sombra = (ease(seg(dt, 0.2, 0.55)) if t >= T_[3] else None)
    c = interior_coche(F, t, luz=luz, speed=1.0, sombra=sombra)
    img = iluminar(F.finish(), F, [], glows=[(c["espejo"], 300 + 700 * luz, 0.5 + 0.5 * luz)], amb=0.25 + 0.5 * luz, warm=(255, 250, 230))
    return img, dict(grain=10, flash=((255, 255, 250), 0.45 * luz))

def cruje(t, D, fi):
    F = Frame(fondo(), dict(x=lerp(560, 600, ease(t / D)), y=1040, z=lerp(1.35, 1.6, ease(t / D)), sy=noise(t * 18) * 3))
    T_ = [D * 0.12, D * 0.42, D * 0.7]
    luz, dt = pulsos(t, T_, dec=0.4)
    d_k = 1 - ease(seg(dt, 0.12, 0.4)) if dt < 50 else 1.0
    exterior(F, t, piso=1200, speed=900)
    coche_lado(F, 520, 1200, t, dedos_k=d_k, tu_face="neutral" if t < T_[1] else "scared")
    img = iluminar(F.finish(), F, [], glows=[((700, 960), 260 + 300 * luz, 0.15 + 0.85 * luz), ((200, 1100), 300, 0.4), ((880, 380), 200, 0.5)],
                   amb=0.14 + 0.3 * luz, warm=(255, 250, 230))
    return img, dict(grain=11, flash=((255, 255, 250), 0.22 * luz))

def paras(t, D, fi):
    fr = ease_out(seg(t, 0, D * 0.55))
    F = Frame(fondo(), dict(x=lerp(560, 640, fr), y=1000, z=0.78, sx=noise(t * 20) * 6 * (1 - fr)))
    exterior(F, t, piso=1240, speed=900 * (1 - fr) ** 2)
    xb = lerp(1700, 1230, ease_out(seg(t, D * 0.2, D * 0.8)))
    luz = 0.85 + 0.15 * (noise(t * 5) > 0)
    haz_faros(F, xb, 1240, luz)
    coche_lado(F, 520, 1240, t * (1 - fr), tu_face="scared")
    coche_draw(F, xb, 1240)
    img = iluminar(F.finish(), F, [], glows=[((xb - 500, 1150), 520, 0.9 * luz), ((880, 380), 200, 0.5)], amb=0.2, warm=(255, 240, 200))
    return img, dict(grain=10)

def conductor(t, D, fi):
    F = Frame(fondo(), dict(x=500, y=1000, z=1.3, sx=noise(t * 30) * 4 * seg(t, D * 0.4, D * 0.5)))
    exterior(F, t, piso=1200)
    haz_faros(F, 1350, 1200, 1.0)
    coche_lado(F, 400, 1200, t, tu_face="scared")
    w = ease_out(seg(t, 0, D * 0.38))
    grita = t > D * 0.4
    p = run(t, 1.2) if not grita else add(pose(body=-8, head=-6, a1u=100, a1l=-5, a2u=160, a2l=20), jitter(t, 3, 2))
    CONDUCTOR.draw(F, p, lerp(1080, 780, w), 1215, f=-1, face="talk" if grita else "scared", t=t)
    img = iluminar(F.finish(), F, [], glows=[((900, 1100), 520, 0.85), ((560, 1030), 200, 0.45)], amb=0.24, warm=(255, 240, 200))
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * grita))

def entiendes(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(560, 600, k), y=lerp(1010, 990, k), z=lerp(1.8, 2.5, k)))
    apaga = 1 - ease(seg(t, D * 0.62, D * 0.72))
    exterior(F, t, piso=1200)
    haz_faros(F, 1350, 1200, apaga)
    coche_lado(F, 400, 1200, t, tu_face="scared", mano=seg(t, D * 0.72, D * 0.98), cara=0.35 * seg(t, D * 0.8, D))
    img = iluminar(F.finish(), F, [], glows=[((900, 1100), 600, 0.85 * apaga), ((520, 1000), 160, 0.35), ((605, 1000), 140, 0.6 * seg(t, D * 0.72, D))], amb=0.16 + 0.15 * apaga, warm=(255, 240, 200))
    return img, dict(grain=12, dark=0.2 * (1 - apaga), tint=((255, 0, 30), 0.18 * (1 - apaga)))

def retrovisor(t, D, fi):
    hit = seg(t, D * 0.3, D * 0.38)
    sh = 10 * hit * (1 - seg(t, D * 0.38, D * 0.7))
    F = Frame(fondo(1), dict(x=540 + noise(t * 30) * sh, y=lerp(520, 470, ease(t / D)), z=lerp(1.7, 2.6, ease(seg(t, 0, D * 0.4))),
                             sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    c = interior_coche(F, t, luz=0.0, speed=0.0, cosa=hit, manos=seg(t, D * 0.55, D))
    img = iluminar(F.finish(), F, [], glows=[(c["espejo"], 300, 0.85)], amb=0.25, warm=(200, 210, 255))
    golpe = hit >= 1
    return img, dict(grain=12, flash=((255, 255, 255), max(0, 1 - (t - D * 0.38) / 0.25)) if golpe else None,
                     glitch=0.45 if golpe and fi % 3 and t < D * 0.75 else 0.0, tint=((255, 0, 30), 0.28 if golpe else 0.0))

def final(t, D, fi):
    F = Frame(fondo(1), dict(x=540, y=lerp(700, 760, ease(t / D)), z=1.25))
    c = interior_coche(F, t, luz=0.0, speed=0.0, cosa=1.0, manos=0.75 + 0.1 * math.sin(t * 2), reloj=False)
    img = iluminar(F.finish(), F, [], glows=[(c["espejo"], 300, 0.85)], amb=0.18, warm=(200, 210, 255))
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, D * 0.55, D * 0.65)) * (1 + 0.03 * math.sin(t * 25))
    if p > 0:
        d.text((540, 900), tr("SI TE DAN LAS LARGAS…"), font=font(70 * p + 1), fill=(255, 255, 255), anchor="mm", stroke_width=int(8 * p), stroke_fill=(0, 0, 0))
        d.text((540, 1060), tr("MIRA ATRÁS"), font=font(160 * p + 1), fill=(255, 40, 50), anchor="mm", stroke_width=int(14 * p), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 1200, 850, 1300), 26, fill=(230, 30, 50))
        d.text((540, 1250), tr("SÍGUEME PARA MÁS"), font=font(52), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=10, tint=((255, 0, 30), 0.25 * p if p > 0 else 0), glitch=0.3 if p > 0 and fi % 5 == 0 else 0.0)

ESCENA_FN = dict(carretera=carretera_, largas=largas, cruje=cruje, paras=paras, conductor=conductor, entiendes=entiendes,
                 retrovisor=retrovisor, final=final)
PAUSA = dict(carretera=0.6, largas=0.9, cruje=1.0, paras=0.5, conductor=0.6, entiendes=0.9, retrovisor=1.4, final=2.6)
