"""Escenas del episodio 13 (temporada 2, "La fábrica de cristal"): huellas de dedos de ventana en ventana,
la vieja fábrica de cristal, el Asomado saltando de cristal en cristal y la sala de los niños dormidos tras paneles."""
import math, random
from functools import lru_cache
from motor import *
from escenas import base, GLASS
from escenas6 import NINA, coletas
from escenas7 import NINO
from escenas12 import asomado, edificios_tapados

PISO = 1250
VERDE = (120, 255, 150)

@lru_cache(None)
def fondo(kind):
    if kind == "nave": return gradient((10, 18, 22), (22, 34, 38))
    if kind == "sala": return gradient((6, 10, 12), (14, 22, 24))
    return base(kind)

# ---------- piezas nuevas ----------
def huella(F, x, y, k=1.0, s=1.0):
    """marca de dedos larguísimos en un cristal: cuatro trazos y la palma"""
    c = tuple(int(lerp(g, v, k)) for g, v in zip(GLASS, (190, 230, 200)))
    F.ellipse((x, y + 26 * s), 12 * s, 14 * s, fill=c)
    for i in range(4):
        dx = (i - 1.5) * 9 * s
        F.line([(x + dx * 0.6, y + 16 * s), (x + dx * 1.6, y - (40 + 12 * (i in (1, 2))) * s)], c, 4 * s)

def casa(F, x, piso, w=300, h=420, huellas=0.0, seed=0):
    """casita con dos ventanas tapadas y huellas de dedos en el cristal"""
    F.rect(x, piso - h, x + w, piso, fill=(26, 28, 42))
    F.poly([(x - 20, piso - h), (x + w / 2, piso - h - 130), (x + w + 20, piso - h)], fill=(36, 30, 40))
    for i, wx in enumerate((x + 40, x + w - 130)):
        wy = piso - h + 80
        F.rect(wx, wy, wx + 90, wy + 120, fill=GLASS); F.rect(wx - 6, wy - 6, wx + 96, wy + 126, outline=(60, 70, 108), w=8)
        F.line([(wx, wy), (wx + 90, wy + 120)], (90, 82, 64), 4); F.line([(wx + 90, wy), (wx, wy + 120)], (90, 82, 64), 4)
        if huellas > 0: huella(F, wx + 45, wy + 70, huellas, 0.8)
    F.rect(x + w / 2 - 40, piso - 150, x + w / 2 + 40, piso, fill=(48, 36, 30))

def fabrica_ext(F, x, piso, verde=0.0, t=0.0):
    """la vieja fábrica de cristal: nave de ladrillo con chimenea y ventanales de cuadrícula rotos"""
    F.rect(x + 560, piso - 1060, x + 660, piso - 500, fill=(38, 26, 26))                 # chimenea
    F.rect(x + 548, piso - 1080, x + 672, piso - 1040, fill=(48, 32, 30))
    F.rect(x, piso - 640, x + 800, piso, fill=(52, 30, 28))
    F.poly([(x - 30, piso - 640), (x + 400, piso - 820), (x + 830, piso - 640)], fill=(40, 24, 24))
    for i in range(3):                                                                    # ventanales
        wx = x + 60 + i * 250; wy = piso - 560
        g = 0.5 + 0.5 * math.sin(t * 3 + i * 1.7)
        col = tuple(int(lerp(a, b, verde * (0.6 + 0.4 * g))) for a, b in zip(GLASS, (60, 150, 90)))
        F.rect(wx, wy, wx + 180, wy + 300, fill=col)
        for gx in range(1, 3): F.line([(wx + gx * 60, wy), (wx + gx * 60, wy + 300)], (30, 22, 22), 6)
        for gy in range(1, 4): F.line([(wx, wy + gy * 75), (wx + 180, wy + gy * 75)], (30, 22, 22), 6)
        r = random.Random(i)
        for _ in range(2):                                                                # cristales rotos
            cx, cy = wx + r.randint(1, 2) * 60 - 30, wy + r.randint(0, 3) * 75 + 37
            F.poly([(cx - 30, cy - 37), (cx + 30, cy - 37), (cx + 8, cy + 10), (cx - 12, cy - 5)], fill=(10, 10, 16))
    F.rect(x + 320, piso - 260, x + 480, piso, fill=(20, 14, 14))                         # portón
    F.text((x + 400, piso - 700), tr("CRISTALERÍA"), 46, (150, 120, 90))

def panel(F, x, y0, w, h, brillo=0.0, luz=0.0):
    """panel de cristal vertical con marco y reflejos; luz = resplandor verdoso desde dentro"""
    col = tuple(int(lerp(a, b, luz)) for a, b in zip(GLASS, (40, 90, 70)))
    F.rect(x, y0, x + w, y0 + h, fill=col)
    sh = tuple(int(lerp(a, 200, 0.25 + 0.35 * brillo)) for a in col)
    F.poly([(x + w * 0.15, y0 + h * 0.05), (x + w * 0.32, y0 + h * 0.05), (x + w * 0.12, y0 + h * 0.6), (x + w * 0.02, y0 + h * 0.6)], fill=sh)
    F.line([(x + w * 0.7, y0 + h * 0.1), (x + w * 0.55, y0 + h * 0.4)], sh, 5)
    F.rect(x - 8, y0 - 8, x + w + 8, y0 + h + 8, outline=(70, 82, 90), w=12)

def nave(F, piso=PISO):
    """interior de la fábrica: vigas, suelo y polvo"""
    F.rect(-800, piso, 1900, 2800, fill=(12, 16, 18))
    F.line([(-800, piso), (1900, piso)], (44, 56, 60), 6)
    for vx in range(-600, 1800, 420):
        F.rect(vx, 180, vx + 34, piso, fill=(24, 30, 34))
    F.rect(-800, 170, 1900, 210, fill=(28, 34, 38))
    for i in range(14):
        r = random.Random(i + 40); F.circle((r.randint(-400, 1500), r.randint(260, 1200)), 2.5, fill=(80, 100, 96))

def dormido_panel(F, x, y0, w, h, fig, t, nina=False, k=1.0):
    """niño dormido flotando detrás de un panel (ojos cerrados, brazos caídos)"""
    p = pose(body=0, head=10 + 3 * math.sin(t * 1.5 + x), a1u=8, a1l=6, a2u=-8, a2l=6, l1u=4, l1l=0, l2u=-4, l2l=0)
    J = fig.draw(F, p, x + w / 2, y0 + h - 30 + 6 * math.sin(t * 1.2 + x * 0.01), f=1, face="closed", snap=True)
    if nina: coletas(F, J, 0.8)
    return J

def asomado_en(F, c, a, t, mueca=0.2):
    """solo la cara del Asomado dentro de un cristal"""
    if a > 0.01: asomado(F, c, a, t, mueca=mueca, dedos=0.0)

# ---------- escenas ----------
def vaho(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("cuarto"), dict(x=540, y=lerp(760, 700, zp), z=lerp(1.7, 2.0, zp), sx=noise(t * 30) * 3, sy=noise(t * 30, 3) * 3))
    F.rect(-400, 1250, 1500, 2600, fill=(10, 12, 20))
    F.rect(380, 500, 700, 880, fill=GLASS)
    asomado(F, (540, 700), lerp(0.6, 1.0, seg(t, 0, D * 0.3)), t, mueca=0.2 + 0.2 * math.sin(t * 3) ** 2, dedos=1.0)
    F.rect(372, 492, 708, 888, outline=(60, 70, 108), w=16)
    F.line([(540, 500), (540, 880)], (60, 70, 108), 10); F.line([(380, 690), (700, 690)], (60, 70, 108), 10)
    return F.finish(), dict(grain=9, tint=(VERDE, 0.12), flash=(VERDE, 0.35 * (1 - seg(t, 0, 0.35))))

def rastro(t, D, fi):
    pan = ease(t / D)
    F = Frame(base("calle"), dict(x=lerp(300, 1500, pan), y=980, z=1.15))
    F.circle((lerp(800, 1900, pan), 380), 70, fill=(220, 224, 236))
    edificios_tapados(F, -600, 2600, 1000, seed=13, k=1.0)
    for i in range(5):
        x = -200 + i * 420
        casa(F, x, 1250, huellas=ease(seg(t, D * (0.05 + i * 0.12), D * (0.2 + i * 0.12))), seed=i)
    F.rect(-800, 1250, 2800, 2700, fill=(18, 19, 26)); F.line([(-800, 1250), (2800, 1250)], (54, 56, 70), 6)
    xs = lerp(250, 1450, pan)
    NORA.draw(F, run(t), xs + 100, 1250, f=1, face="scared")
    LEO.draw(F, run(t + 0.2), xs, 1250, f=1, face="neutral")
    CARMEN.draw(F, walk(t, 1.0, 1.4), xs - 130, 1250, f=1, face="neutral")
    return F.finish(), dict(grain=7, tint=(VERDE, 0.04))

def fabrica(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("ciudad"), dict(x=540, y=lerp(900, 980, zp), z=lerp(0.95, 1.15, zp)))
    F.circle((880, 330), 60, fill=(220, 224, 236))
    F.rect(-600, 1250, 1700, 2700, fill=(16, 18, 22)); F.line([(-600, 1250), (1700, 1250)], (50, 52, 60), 6)
    fabrica_ext(F, 140, 1250, verde=ease(seg(t, D * 0.3, D * 0.7)), t=t)
    stop = seg(t, 0, D * 0.7)
    for fig, dx, ph in ((CARMEN, -10, 0), (LEO, 120, 0.3), (NORA, 240, 0.6)):
        F_pose = pose(head=-14) if stop >= 1 else walk(t + ph, 0.8)
        fig.draw(F, F_pose, lerp(-300, 120, ease(stop)) + dx, 1250, f=1, face="scared" if t > D * 0.6 else "neutral")
    return F.finish(), dict(grain=8, tint=(VERDE, 0.06 * seg(t, D * 0.3, D)))

PX = (60, 400, 740)        # paneles de la nave (x izquierdo)
def reflejos(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("nave"), dict(x=lerp(560, 520, zp), y=lerp(980, 940, zp), z=lerp(1.0, 1.12, zp),
                                  sx=noise(t * 30) * 4 * zp, sy=noise(t * 30, 2) * 4 * zp))
    nave(F)
    j = min(2, int(t / (D / 3.2)))                        # cristal en el que está la cara
    local = (t % (D / 3.2)) / (D / 3.2)
    for i, x in enumerate(PX):
        panel(F, x, 470, 280, 640, brillo=0.5 + 0.5 * math.sin(t * 2 + i), luz=0.35 if i == j else 0.0)
    a = ease(seg(local, 0, 0.25)) if j == 0 else 1.0
    asomado_en(F, (PX[j] + 140, 760), a, t, mueca=0.3 + 0.3 * local)
    LEO.draw(F, pose(head=-8, a1u=60, a1l=40, a2u=-30), 330, PISO, f=1, face="scared")
    NORA.draw(F, SCARED, 500, PISO, f=1, face="scared")
    CARMEN.draw(F, pose(head=-6, a1u=30), 680, PISO, f=-1, face="scared")
    jump = local < 0.12 and j > 0
    return F.finish(), dict(grain=9, tint=(VERDE, 0.1), glitch=0.4 if jump and fi % 2 == 0 else 0.0,
                            flash=(VERDE, 0.4 if jump else 0.0))

def huyen_cristal(t, D, fi):
    pan = ease(t / D)
    cx = lerp(1300, 300, pan)
    F = Frame(fondo("nave"), dict(x=cx, y=960, z=1.1, sx=noise(t * 40) * 5, sy=noise(t * 40, 2) * 5))
    nave(F)
    for k in range(9):
        panel(F, -700 + k * 330, 470, 260, 600, brillo=0.5, luz=0.0)
    xs = lerp(1600, 250, pan)                               # corren hacia la izquierda
    kk = int((xs + 120 + 700) / 330); kk = max(0, min(8, kk))
    asomado_en(F, (-700 + kk * 330 + 130, 740), 1.0, t, mueca=0.7)
    g = seg(t, D * 0.45, D * 0.6)
    LEO.draw(F, add(run(t), dict(head=lerp(0, 30, g))), xs, PISO, f=-1, face="talk" if g > 0 else "scared", t=t)
    NORA.draw(F, run(t + 0.25), xs - 140, PISO, f=-1, face="scared")
    CARMEN.draw(F, run(t + 0.5, 0.8), xs + 150, PISO, f=-1, face="scared")
    return F.finish(), dict(grain=10, tint=(VERDE, 0.12), glitch=0.3 if fi % 5 == 0 else 0.0)

def sala_paneles(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("sala"), dict(x=lerp(540, 560, zp), y=lerp(1000, 960, zp), z=lerp(1.0, 1.15, zp)))
    nave(F)
    for k in range(4):
        panel(F, 40 + k * 260, 520, 200, 560, brillo=0.2, luz=0.05)
    w = ease(seg(t, 0, D * 0.6))
    LEO.draw(F, walk(t, 0.6) if w < 1 else pose(head=-10, a1u=40), lerp(-150, 420, w), PISO, f=1, face="scared")
    NORA.draw(F, walk(t + 0.3, 0.6) if w < 1 else pose(head=-12), lerp(-300, 560, w), PISO, f=1, face="scared")
    CARMEN.draw(F, walk(t + 0.6, 0.6) if w < 1 else pose(head=-6), lerp(-450, 700, w), PISO, f=1, face="neutral")
    return F.finish(), dict(grain=9, dark=0.35)

def giro(t, D, fi):
    on = seg(t, D * 0.1, D * 0.3)
    flick = on if on >= 1 or fi % 3 else 0.0                # las luces parpadean al encenderse
    pan = ease(seg(t, D * 0.3, D * 0.8))
    zz = ease_out(seg(t, D * 0.65, D * 0.85))
    F = Frame(fondo("sala"), dict(x=lerp(400, 1700, pan), y=lerp(900, 840, pan), z=lerp(1.0, 1.55, zz),
                                  sx=noise(t * 40) * 6 * zz, sy=noise(t * 40, 2) * 6 * zz))
    nave(F)
    for k in range(8):
        x = -200 + k * 280
        panel(F, x, 480, 220, 600, brillo=0.3, luz=0.6 * flick)
        last = k == 6
        if flick > 0:
            dormido_panel(F, x, 480, 220, 600, NINA if (k % 2 == 0) else NINO, t, nina=(k % 2 == 0))
        F.rect(x - 8, 472, x + 228, 1088, outline=(70, 82, 90) if not last else (int(lerp(70, 160, zz)), 255, 160), w=12)
    LEO.draw(F, pose(head=-8, a1u=40), 360, PISO, f=1, face="scared")
    NORA.draw(F, SCARED, 500, PISO, f=1, face="scared")
    return F.finish(), dict(grain=8, tint=(VERDE, 0.1 * flick), glitch=0.3 * zz if fi % 3 == 0 else 0.0,
                            flash=(VERDE, 0.3 * math.exp(-abs(t - D * 0.75) * 8)), dark=0.4 * (1 - flick))

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    return F.finish(), {}

ESCENA_FN = dict(vaho=vaho, rastro=rastro, fabrica=fabrica, reflejos=reflejos, huyen_cristal=huyen_cristal,
                 sala_paneles=sala_paneles, giro=giro, final=final)
PAUSA = dict(vaho=0.5, rastro=0.4, fabrica=0.5, reflejos=0.5, huyen_cristal=0.5, sala_paneles=0.5, giro=1.0, final=1.6)
