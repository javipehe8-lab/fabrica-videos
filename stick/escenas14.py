"""Escenas del episodio 14 (temporada 2, "Sin cristal"): Leo rompe el panel de Lucía, el Asomado sale del cristal,
fuera del cristal es ciego y busca el vaho de la respiración, y los otros niños abren los ojos y sonríen a la vez."""
import math, random
from motor import *
from escenas import base, GLASS
from escenas6 import NINA, coletas
from escenas7 import NINO
from escenas12 import asomado
from escenas13 import fondo, panel, nave, dormido_panel, PISO, VERDE

PALIDO = (206, 232, 210)

# ---------- piezas nuevas ----------
def esquirlas(F, c, k, seed=0, n=26):
    """cristales que saltan desde c; k = 0..1 tiempo desde el impacto"""
    if k <= 0: return
    r = random.Random(seed)
    for _ in range(n):
        ang = r.uniform(0, 2 * math.pi); v = r.uniform(250, 700); s = r.uniform(10, 30)
        x = c[0] + math.cos(ang) * v * k; y = c[1] + math.sin(ang) * v * k + 900 * k * k
        y = min(y, PISO - 4)
        rot = r.uniform(0, 6) + k * 8
        col = (int(lerp(150, 60, k)), int(lerp(190, 90, k)), int(lerp(230, 130, k)))
        F.poly([(x + math.cos(rot + a) * s * m, y + math.sin(rot + a) * s * m) for a, m in ((0, 1), (2.2, 0.6), (4.1, 0.9))], fill=col)

def suelo_cristales(F, x0, x1, seed=3):
    r = random.Random(seed)
    for _ in range(30):
        x = r.uniform(x0, x1); s = r.uniform(6, 16)
        F.poly([(x - s, PISO - 2), (x + s * 0.4, PISO - s * 0.6), (x + s, PISO - 1)], fill=(90, 120, 150))

def marco_roto(F, x, y0, w, h, seed=1):
    """panel con el cristal reventado: solo quedan picos en el marco"""
    F.rect(x, y0, x + w, y0 + h, fill=(10, 14, 16))
    r = random.Random(seed); col = (50, 76, 110)
    for side in range(4):
        for i in range(4):
            u = (i + r.uniform(0.1, 0.9)) / 4; d = r.uniform(30, 90)
            if side == 0: p = [(x + u * w - 20, y0), (x + u * w + 20, y0), (x + u * w, y0 + d)]
            elif side == 1: p = [(x + u * w - 20, y0 + h), (x + u * w + 20, y0 + h), (x + u * w, y0 + h - d)]
            elif side == 2: p = [(x, y0 + u * h - 25), (x, y0 + u * h + 25), (x + d, y0 + u * h)]
            else: p = [(x + w, y0 + u * h - 25), (x + w, y0 + u * h + 25), (x + w - d, y0 + u * h)]
            F.poly(p, fill=col)
    F.rect(x - 8, y0 - 8, x + w + 8, y0 + h + 8, outline=(70, 82, 90), w=12)

def cuerpo_asomado(F, c, alto, t, abre=1.0):
    """cuerpo flaquísimo y pálido del Asomado fuera del cristal (bajo la cara)"""
    cx, cy = c
    cuello = (cx, cy + 110); cad = (cx + 6 * math.sin(t * 2), cy + 110 + alto * 0.45)
    F.line([cuello, cad], PALIDO, 16)
    for s_ in (-1, 1):
        rod = (cad[0] + s_ * 50, cad[1] + alto * 0.28)
        F.line([cad, rod, (rod[0] + s_ * 10, PISO)], PALIDO, 12)
        hom = (cx, cy + 150)
        codo = (cx + s_ * lerp(80, 200, abre), cy + 230 + 20 * math.sin(t * 3 + s_))
        mano = (cx + s_ * lerp(110, 330, abre), cy + lerp(380, 260, abre))
        F.line([hom, codo, mano], PALIDO, 11)
        for k in range(4):                                     # dedos larguísimos
            a = math.radians(-60 + k * 30 + 6 * math.sin(t * 5 + k)) * s_
            F.line([mano, (mano[0] + s_ * math.cos(a) * 120, mano[1] + math.sin(abs(a)) * 70 + 30)], PALIDO, 6)

def ojos_ciegos(F, c, t, k=1.0):
    """tapa los ojos del Asomado con una película lechosa (ciego fuera del cristal)"""
    if k <= 0: return
    cx, cy = c[0] + noise(t * 3, 4) * 6, c[1]
    col = tuple(int(lerp(a, b, k)) for a, b in zip((8, 10, 8), (214, 222, 216)))
    for dx in (-36, 36):
        F.ellipse((cx + dx, cy - 26), 18, 27, fill=col)
        F.circle((cx + dx, cy - 22), 6, fill=tuple(int(lerp(a, b, k)) for a, b in zip((120, 255, 140), (180, 190, 186))))

def vaho_boca(F, J, t, k=1.0, f=1, seed=0):
    """nubecillas de vaho que salen de la boca"""
    if k <= 0: return
    hx, hy = J["head"]
    for i in range(3):
        ph = ((t * 0.9 + i / 3 + seed * 0.37) % 1.0)
        x = hx + f * (40 + 70 * ph); y = hy + 10 - 60 * ph
        g = int(lerp(190, 40, ph) * k)
        F.circle((x, y), 10 + 26 * ph, fill=(max(30, g), max(36, g + 6), max(40, g + 10)))

def tapa_boca(fig_pose):
    return add(fig_pose, dict(a1u=150, a1l=-150))

def lucia_suelo(F, x, t, ojos=False):
    """Lucía tumbada en brazos de Nora (en horizontal)"""
    p = pose(body=0, head=0, a1u=10, a1l=10, a2u=-10, a2l=10, l1u=4, l1l=0, l2u=-4, l2l=0)
    J = NINA.draw(F, p, x, PISO - 40, f=1, rot=-80, snap=False, face="scared" if ojos else "closed")
    coletas(F, J, 0.8)
    return J

def sonrisa_nino(F, J, k, sc=0.8, f=1):
    """ojos abiertos con pupila verde y sonrisa de oreja a oreja"""
    if k <= 0: return
    hx, hy = J["head"]; ex = f * 9 * sc; ink = (12, 14, 12)
    for dx in (-9, 11):
        F.circle((hx + ex + dx * sc, hy - 5 * sc), 6.5 * sc, fill=ink)
        F.circle((hx + ex + dx * sc, hy - 5 * sc), 2.6 * sc, fill=VERDE)
    F.rect(hx + ex - 10 * sc, hy + 9 * sc, hx + ex + 10 * sc, hy + 16 * sc, fill=tuple(int(lerp(240, 236, 0)) for _ in range(3)))
    F.arc((hx + ex, hy - 6 * sc), 20 * sc * lerp(0.6, 1.0, k), 20, 160, ink, 5 * sc)
    for i in range(-3, 4):
        an = math.radians(90 - i * 15); r = 20 * sc * lerp(0.6, 1.0, k)
        x, y = hx + ex + math.cos(an) * r, hy - 6 * sc + math.sin(an) * r
        F.line([(x, y - 4 * sc), (x, y + 2 * sc)], (240, 240, 236), 2 * sc, round_=False)

# ---------- escenas ----------
LX = 380      # panel de Lucía
def rompe(t, D, fi):
    hit = D * 0.42
    k = seg(t, hit, hit + 1.2)
    sh = math.exp(-max(0, t - hit) * 6) * 18 if t > hit else 0
    zp = ease(t / D)
    F = Frame(fondo("nave"), dict(x=lerp(560, 540, zp), y=lerp(900, 930, zp), z=lerp(1.25, 1.1, zp),
                                  sx=noise(t * 40) * sh, sy=noise(t * 40, 2) * sh))
    nave(F)
    panel(F, -40, 480, 220, 600, brillo=0.4, luz=0.4); dormido_panel(F, -40, 480, 220, 600, NINO, t)
    panel(F, 860, 480, 220, 600, brillo=0.4, luz=0.4); dormido_panel(F, 860, 480, 220, 600, NINA, t, nina=True)
    if t < hit:
        panel(F, LX, 480, 280, 600, brillo=0.6, luz=0.5); dormido_panel(F, LX, 480, 280, 600, NINA, t, nina=True)
    else:
        marco_roto(F, LX, 480, 280, 600)
    if t > hit: suelo_cristales(F, LX - 200, LX + 500)
    sw = ease(seg(t, hit - 0.45, hit))                     # golpe con la barra
    p = pose(body=lerp(-10, 14, sw), head=-6, a1u=lerp(175, 75, sw), a1l=lerp(10, 0, sw), a2u=lerp(160, 70, sw), a2l=10,
             l1u=20, l1l=-10, l2u=-20, l2l=-6)
    J = LEO.draw(F, p, 230, PISO, f=1, face="angry")
    hx, hy = J["a1h"]; a = math.radians(lerp(175, 75, sw) + lerp(-10, 14, sw))
    F.line([(hx, hy), (hx + math.sin(a) * 200, hy + math.cos(a) * 200)], (120, 124, 130), 12)
    NORA.draw(F, SCARED, 780, PISO, f=-1, face="scared")
    esquirlas(F, (LX + 140, 760), k)
    return F.finish(), dict(grain=8, tint=(VERDE, 0.08), flash=((255, 255, 255), 0.7 * math.exp(-max(0, t - hit) * 7) if t > hit else 0),
                            glitch=0.3 if hit < t < hit + 0.2 else 0.0)

def libre(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("nave"), dict(x=lerp(520, 500, zp), y=lerp(1020, 1060, zp), z=lerp(1.4, 1.65, zp)))
    nave(F)
    marco_roto(F, 300, 480, 280, 600)
    suelo_cristales(F, 100, 900)
    J = lucia_suelo(F, 470, t, ojos=t > D * 0.65)
    NORA.draw(F, pose(body=30, head=20, a1u=120, a1l=40, a2u=100, a2l=50, l1u=90, l1l=-90, l2u=10, l2l=-100), 620, PISO, f=-1, face="scared")
    CARMEN.draw(F, pose(head=-4, a1u=30), 790, PISO, f=-1, face="neutral")
    return F.finish(), dict(grain=7, tint=(VERDE, 0.06))

def sale(t, D, fi):
    zp = ease(t / D)
    sx = noise(t * 30) * 6 * zp
    F = Frame(fondo("nave"), dict(x=540, y=lerp(900, 860, zp), z=lerp(1.05, 1.2, zp), sx=sx, sy=noise(t * 30, 2) * 6 * zp))
    nave(F)
    marco_roto(F, LX, 480, 280, 600)
    e = ease(seg(t, D * 0.1, D * 0.75))                     # sale del marco
    c = (LX + 140, lerp(760, 640, e))
    if e > 0.2: cuerpo_asomado(F, c, lerp(200, 470, e), t, abre=e)
    asomado(F, c, lerp(0.4, 1.0, e), t, mueca=0.3 + 0.3 * e, dedos=1.0 - e, base_y=lerp(880, 1000, e))
    LEO.draw(F, pose(body=-14, head=-8, a1u=60, a1l=30, a2u=-20), 140, PISO, f=1, face="scared")
    NORA.draw(F, pose(body=-10, head=-10, a1u=40, a2u=40), 900, PISO, f=-1, face="scared")
    return F.finish(), dict(grain=9, tint=(VERDE, 0.12), glitch=0.3 if fi % 6 == 0 else 0.0)

def ciego(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("nave"), dict(x=540, y=lerp(760, 720, zp), z=lerp(1.5, 1.8, zp)))
    nave(F)
    c = (540 + 70 * math.sin(t * 1.6), 700)
    cuerpo_asomado(F, c, 470, t, abre=0.6)
    asomado(F, c, 1.0, t, mueca=0.1, dedos=0.0)
    ojos_ciegos(F, c, t, ease(seg(t, D * 0.15, D * 0.5)))
    return F.finish(), dict(grain=9, tint=(VERDE, 0.1), dark=0.15)

def aliento(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("nave"), dict(x=lerp(560, 600, zp), y=lerp(930, 900, zp), z=lerp(1.0, 1.15, zp)))
    nave(F)
    marco_roto(F, 760, 480, 280, 600)
    c = (lerp(960, 880, zp), 640)
    cuerpo_asomado(F, c, 470, t, abre=0.8)
    asomado(F, c, 1.0, t, mueca=0.2, dedos=0.0); ojos_ciegos(F, c, t)
    g = seg(t, D * 0.55, D * 0.7)
    vk = 1 - seg(t, D * 0.75, D * 0.95)
    figs = ((CARMEN, 160, "talk" if g > 0 else "scared"), (LEO, 330, "scared"), (NORA, 500, "scared"))
    for i, (fig, x, fc) in enumerate(figs):
        J = fig.draw(F, SCARED if fig is not CARMEN else pose(head=-4, a1u=lerp(30, 120, g), a1l=lerp(0, 60, g)), x, PISO, f=1, face=fc, t=t)
        vaho_boca(F, J, t, vk, seed=i)
    Jl = NINA.draw(F, pose(head=-6, a1u=20, a2u=-20), 620, PISO, f=1, face="scared"); coletas(F, Jl, 0.8)
    vaho_boca(F, Jl, t, vk, seed=4)
    return F.finish(), dict(grain=8, tint=(VERDE, 0.08))

def aguantan(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("nave"), dict(x=lerp(520, 470, zp), y=lerp(990, 1000, zp), z=lerp(1.3, 1.5, zp),
                                  sx=noise(t * 20) * 2, sy=noise(t * 20, 2) * 2))
    nave(F)
    Jn = NORA.draw(F, tapa_boca(pose(head=-4)), 300, PISO, f=1, face="scared")
    Jl = NINA.draw(F, tapa_boca(pose(head=-4)), 450, PISO, f=1, face="scared"); coletas(F, Jl, 0.8)
    # mano del Asomado barriendo el aire delante de Lucía
    hx = lerp(900, 380, ease(seg(t, D * 0.1, D * 0.85))); hy = 760 + 20 * math.sin(t * 2)
    F.line([(1200, 520), (hx + 120, hy - 60), (hx, hy)], PALIDO, 12)
    for k in range(4):
        a = math.radians(160 + k * 14 + 6 * math.sin(t * 6 + k))
        mx, my = hx + math.cos(a) * 80, hy + math.sin(a) * 50 + 20
        ex, ey = hx + math.cos(a) * 170, hy + math.sin(a) * 60 + 60
        F.line([(hx, hy), (mx, my), (ex, ey)], PALIDO, 7); F.circle((ex, ey), 6, fill=(236, 248, 238))
    return F.finish(), dict(grain=8, tint=(VERDE, 0.08), dark=0.2)

def giro(t, D, fi):
    op = ease(seg(t, D * 0.55, D * 0.65))                 # abren los ojos y sonríen a la vez
    pan = ease(seg(t, 0, D * 0.55))
    zz = ease_out(seg(t, D * 0.55, D * 0.8))
    F = Frame(fondo("sala"), dict(x=lerp(400, 1310, pan), y=lerp(900, 1010, zz), z=lerp(1.0, 2.5, zz),
                                  sx=noise(t * 40) * 6 * zz, sy=noise(t * 40, 2) * 6 * zz))
    nave(F)
    for k in range(7):
        x = -200 + k * 280
        panel(F, x, 480, 220, 600, brillo=0.3, luz=0.6)
        nina = k % 2 == 0; fig = NINA if nina else NINO
        J = dormido_panel(F, x, 480, 220, 600, fig, t, nina=nina)
        sonrisa_nino(F, J, op)
    return F.finish(), dict(grain=8, tint=(VERDE, 0.1 + 0.1 * op), glitch=0.35 * zz if fi % 3 == 0 else 0.0,
                            flash=(VERDE, 0.4 * math.exp(-abs(t - D * 0.58) * 10)))

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    return F.finish(), {}

ESCENA_FN = dict(rompe=rompe, libre=libre, sale=sale, ciego=ciego, aliento=aliento, aguantan=aguantan, giro=giro, final=final)
PAUSA = dict(rompe=0.5, libre=0.4, sale=0.5, ciego=0.4, aliento=0.5, aguantan=0.5, giro=1.0, final=1.6)
