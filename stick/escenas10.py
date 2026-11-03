"""Escenas del episodio 10 (Tomás): en lo alto del faro, Leo corre a la palanca, la luz atrapa al Sonriente,
gritan su nombre verdadero y el monstruo se encoge hasta convertirse en el niño de 1986."""
import math, random
from PIL import ImageDraw
from motor import *
from escenas import base
from escenas2 import enemy, big, sala_lampara
from escenas3 import LILA, YEL
from escenas5 import iluminar
from escenas7 import NINO

PISO = 1450
LUZ = (255, 248, 210)

def rayos(F, t, k=1.0, n=10):
    """rayos de la lámpara encendida girando"""
    if k <= 0: return
    col = tuple(int(lerp(c0, c1, k)) for c0, c1 in zip((40, 40, 52), LUZ))
    for i in range(n):
        a = i * 2 * math.pi / n + t * 1.6
        F.poly([(540, 1040), (540 + math.cos(a - 0.11) * 1700, 1040 + math.sin(a - 0.11) * 1700),
                (540 + math.cos(a + 0.11) * 1700, 1040 + math.sin(a + 0.11) * 1700)], fill=col)
    F.circle((540, 1040), 110 * k + 20, fill=(255, 255, 245))

def chispas(F, x, y, t, fi, n=30, r_=260, h=600, col=LILA):
    r = random.Random(fi // 2)
    for _ in range(n):
        F.circle((x + r.uniform(-r_, r_), y - r.uniform(0, h)), r.uniform(4, 11), fill=col)

def cara_triste(F, J, sc, f=1, lagrimas=1.0, t=0.0):
    """boca triste y lágrimas sobre una cabeza dibujada con face='sad' (solo ojos)"""
    hc = J["head"]; ex = f * 9 * sc; ink = (20, 22, 30)
    F.arc((hc[0] + ex, hc[1] + 24 * sc), 11 * sc, 205, 335, ink, 3.5 * sc)
    if lagrimas > 0:
        for i, dx in enumerate((-9, 11)):
            k = (t * 0.9 + i * 0.5) % 1
            F.ellipse((hc[0] + ex + dx * sc, hc[1] + (2 + 22 * k) * sc), 3.2 * sc, 5 * sc, fill=(120, 190, 255))

def palanca_leo(F, t, lever=0.0, shake=0.0, tiro=0.0):
    tip = sala_lampara(F, lit=0.0, lever=lever, shake=shake)
    return tip

# ---------- escenas ----------
def acorralados(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("oscuro"), dict(x=lerp(500, 540, zp), y=lerp(1180, 1200, zp), z=lerp(1.35, 1.28, zp), sx=noise(t * 30) * 4, sy=noise(t * 30, 2) * 4))
    tip = sala_lampara(F)
    ex = lerp(200, 250, zp)
    J = enemy(F, add(pose(a1u=60, a1l=30, a2u=-40, a2l=20, body=8, head=-6), jitter(t, 6, 8)), ex, PISO, 2.0, f=1)
    NORA.draw(F, add(SCARED, jitter(t, 3, 2)), lerp(450, 480, zp), PISO, f=-1, face="scared")
    w = ease(seg(t, D * 0.45, D * 0.95))
    lx = lerp(620, tip[0] - 110, w)
    LEO.draw(F, run(t, 1.1) if 0 < w < 1 else (SCARED if w == 0 else pose(body=-20, a1u=70, a1l=10, a2u=60, a2l=20)), lx, PISO,
             f=1, face="scared" if w < 1 else "angry")
    img = iluminar(F.finish(), F, [], glows=[(J["head"], 260, 0.55), ((560, 1250), 380, 0.55), ((540, 1040), 220, 0.4)], amb=0.25, warm=(220, 190, 255))
    return img, dict(grain=10, tint=((255, 0, 30), 0.1))

def atascada(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("oscuro"), dict(x=lerp(560, 540, zp), y=lerp(1200, 1180, zp), z=lerp(1.28, 1.4, zp)))
    sh = 7 * math.sin(t * 48)
    tip = sala_lampara(F, shake=sh)
    LEO.draw(F, add(pose(body=-24, a1u=60, a1l=10, a2u=50, a2l=20, l1u=-24, l2u=24), jitter(t, 4, 3)), tip[0] - 100, PISO, f=1, face="angry")
    ex = lerp(250, 300, ease(seg(t, D * 0.3, D)))
    reach = ease(seg(t, D * 0.3, D * 0.8))
    J = enemy(F, add(pose(a1u=lerp(60, 92, reach), a1l=lerp(30, 0, reach), a2u=-30, body=10, head=-8), jitter(t, 5, 8)), ex, PISO, 2.0, f=1)
    NORA.draw(F, add(SCARED, jitter(t, 4, 5)), lerp(480, 510, reach), PISO, f=-1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[(J["head"], 260, 0.55), ((620, 1250), 420, 0.6)], amb=0.25, warm=(220, 190, 255))
    if t > D * 0.15:
        d = ImageDraw.Draw(img); s = ease_back(seg(t, D * 0.15, D * 0.28))
        d.text((540 + noise(t * 30) * 8, 420), tr("¡ATASCADA!"), font=font(110 * s + 1), fill=(255, 60, 60), anchor="mm", stroke_width=int(10 * s), stroke_fill=(0, 0, 0))
    return img, dict(grain=10, tint=((255, 0, 30), 0.14 * reach))

def luz_faro(t, D, fi):
    T0 = D * 0.42; on = t >= T0
    shk = 30 * math.exp(-(t - T0) * 3) if on else 5
    F = Frame(base("oscuro"), dict(x=580, y=1150, z=1.05, sx=noise(t * 50) * shk, sy=noise(t * 50, 3) * shk))
    lit = ease(seg(t, T0, T0 + 0.3))
    tip = sala_lampara(F, lit=lit, lever=ease_out(seg(t, T0 - 0.2, T0)), shake=0 if on else 8 * math.sin(t * 50))
    rayos(F, t, lit)
    e = 1 if on else 0
    J = enemy(F, add(pose(a1u=lerp(92, 160, e), a1l=lerp(0, 40, e), a2u=lerp(-30, -160, e), a2l=-40 * e, body=-10 * e),
                     jitter(t * 2, 6 + 24 * e, 9)), 330, PISO, 2.0, f=1)
    if on: chispas(F, 330, PISO, t, fi, n=26, r_=200, h=650)
    LEO.draw(F, add(pose(body=-24 + 10 * lit, a1u=60 - 60 * lit, a1l=10, a2u=50 - 50 * lit, a2l=20, l1u=-24, l2u=24), jitter(t, 4, 3)),
             tip[0] - 100, PISO, f=1, face="angry")
    NORA.draw(F, SCARED, 560, PISO, f=-1, face="scared")
    return F.finish(), dict(flash=((255, 255, 240), 0.9 * (1 - seg(t, T0, T0 + 0.5)) * on), grain=8)

def _sala_luz(F, t, k=1.0):
    sala_lampara(F, lit=k, lever=1.0)
    rayos(F, t, k)

def tomas_grito(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("oscuro"), dict(x=lerp(540, 470, zp), y=lerp(1150, 1120, zp), z=lerp(1.05, 1.25, zp), sx=noise(t * 40) * 6, sy=noise(t * 40, 2) * 6))
    _sala_luz(F, t)
    J = enemy(F, add(pose(a1u=160, a1l=40, a2u=-160, a2l=-40, body=-10), jitter(t * 2, 28, 9)), 330, PISO, 2.0, f=1)
    chispas(F, 330, PISO, t, fi, n=24, r_=200, h=650)
    gr = seg(t, D * 0.55, D)
    NORA.draw(F, pose(body=-10, a1u=lerp(30, 95, gr), a1l=0, a2u=lerp(-20, 80, gr), a2l=10, head=-6), 580, PISO, f=-1,
              face="talk" if gr > 0 else "angry", t=t)
    LEO.draw(F, pose(body=-8, a1u=40, a1l=30, head=-4), 740, PISO, f=-1, face="angry")
    img = F.finish()
    p = ease_back(seg(t, D * 0.6, D * 0.72))
    if p > 0:
        d = ImageDraw.Draw(img)
        d.text((540 + noise(t * 30) * 6, 460), tr("TOMÁS"), font=font(200 * p + 1), fill=YEL, anchor="mm", stroke_width=int(16 * p), stroke_fill=(0, 0, 0))
    return img, dict(grain=8, flash=((255, 240, 160), 0.5 * math.exp(-abs(t - D * 0.65) * 9)))

def encoge(t, D, fi):
    sq = ease(seg(t, D * 0.1, D * 0.9))
    F = Frame(base("oscuro"), dict(x=lerp(500, 460, sq), y=lerp(1150, 1250, sq), z=lerp(1.1, 1.45, sq), sx=noise(t * 50) * 10 * (1 - sq), sy=noise(t * 50, 3) * 10 * (1 - sq)))
    _sala_luz(F, t)
    sc = lerp(2.0, 0.55, sq)
    J = enemy(F, add(pose(a1u=160 - 40 * sq, a1l=40, a2u=-160 + 40 * sq, a2l=-40, body=-10), jitter(t * 2, 30 * (1 - sq) + 4, 9)), lerp(330, 420, sq), PISO, sc, f=1)
    chispas(F, lerp(330, 420, sq), PISO, t, fi, n=int(50 * (1 - sq)) + 8, r_=260 * (1 - sq) + 60, h=700 * (1 - sq) + 150)
    NORA.draw(F, SCARED, 600, PISO, f=-1, face="scared")
    LEO.draw(F, SCARED, 750, PISO, f=-1, face="scared")
    return F.finish(), dict(grain=8, flash=((255, 255, 250), 0.85 * seg(t, D * 0.85, D)))

def nino(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("oscuro"), dict(x=lerp(560, 520, zp), y=lerp(1160, 1190, zp), z=lerp(1.3, 1.5, zp)))
    k = 1 - 0.5 * ease(seg(t, 0, D * 0.4))
    _sala_luz(F, t * 0.4, k)
    J = big(NINO, 0.9, F, pose(head=8, a1u=8, a1l=10, a2u=-8, a2l=10), 420, PISO, f=1, face="sad")
    cara_triste(F, J, 0.9, f=1, lagrimas=seg(t, D * 0.3, D * 0.4), t=t)
    g = 1 - ease(seg(t, 0, D * 0.3))                                         # restos lilas del monstruo que se apagan
    if g > 0: chispas(F, 420, PISO, t, fi, n=int(30 * g), r_=150, h=400, col=tuple(int(c * g + 255 * (1 - g)) for c in LILA))
    NORA.draw(F, SCARED if t < D * 0.4 else pose(a1u=30, a1l=40, head=6), 620, PISO, f=-1, face="scared")
    LEO.draw(F, SCARED if t < D * 0.5 else STAND, 760, PISO, f=-1, face="scared")
    return F.finish(), dict(grain=7, flash=((255, 255, 250), 0.85 * (1 - seg(t, 0, 0.45))), tint=((255, 220, 160), 0.08))

def giro(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("oscuro"), dict(x=lerp(470, 480, zp), y=lerp(1230, 1250, zp), z=lerp(1.9, 2.5, zp)))
    fl = 0.35 if (t > D * 0.6 and noise(t * 14, 5) > 0.2) else 0.5     # la lámpara parpadea
    _sala_luz(F, t * 0.4, fl)
    m = ease(seg(t, D * 0.2, D * 0.55))
    J = big(NINO, 0.9, F, add(pose(head=lerp(8, -4, m), a1u=lerp(8, 82, m), a1l=lerp(10, -6, m), a2u=-8, a2l=10), jitter(t, 1.5, 3)), 420, PISO, f=1, face="sad")
    cara_triste(F, J, 0.9, f=1, lagrimas=1.0, t=t)
    NORA.draw(F, pose(a1u=30, a1l=40, head=6), 620, PISO, f=-1, face="scared")
    return F.finish(), dict(grain=9, glitch=0.2 if fl < 0.4 and fi % 3 == 0 else 0, tint=((120, 160, 255), 0.06 + 0.1 * (fl < 0.4)))

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    return F.finish(), {}

ESCENA_FN = dict(acorralados=acorralados, atascada=atascada, luz_faro=luz_faro, tomas_grito=tomas_grito, encoge=encoge, nino=nino, giro=giro, final=final)
PAUSA = dict(acorralados=0.4, atascada=0.4, luz_faro=0.7, tomas_grito=0.8, encoge=0.6, nino=0.6, giro=1.1, final=1.6)
