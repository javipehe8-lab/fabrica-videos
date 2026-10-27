"""Escenas del episodio. Cada una: f(t, D, fi) -> (imagen 1080x1920, efectos)."""
import math, random
from functools import lru_cache
from motor import *

@lru_cache(None)
def base(kind):
    if kind == "cuarto": return gradient((22, 28, 50), (12, 15, 28))
    if kind == "ciudad": return gradient((8, 11, 30), (34, 42, 78))
    if kind == "alba": return gradient((70, 86, 118), (170, 172, 186))
    if kind == "hospital": return gradient((150, 188, 194), (104, 140, 148))
    if kind == "oscuro": return gradient((10, 10, 16), (18, 18, 28))
    if kind == "calle": return gradient((14, 16, 30), (40, 38, 58))
    if kind == "amanecer": return gradient((80, 100, 170), (255, 214, 150), mid=(255, 150, 105))
    if kind == "morado": return gradient((30, 18, 50), (14, 10, 24))

GOLD, GLASS = (212, 170, 80), (27, 42, 74)

def cuarto(F, ventana_vacia=True, t=0.0, enemigo=0.0):
    F.rect(-400, 1250, 1500, 2600, fill=(10, 12, 20))
    F.line([(-400, 1250), (1500, 1250)], (40, 46, 70), 6)
    # ventana
    F.rect(380, 500, 700, 880, fill=GLASS)
    F.circle((620, 580), 34, fill=(220, 226, 236))
    for i in range(12):
        r = random.Random(i); F.circle((390 + r.random() * 300, 510 + r.random() * 360), 2.2, fill=(200, 210, 230))
    if enemigo > 0:
        y = lerp(1000, 868, ease_out(enemigo))
        SONRIENTE.draw(F, add(STAND, jitter(t, 6, 3)), 540, y, f=-1, snap=False)
    F.rect(380, 880, 700, 1250, fill=(22, 28, 48))
    F.rect(372, 492, 708, 888, outline=(60, 70, 108), w=16)
    F.line([(540, 500), (540, 880)], (60, 70, 108), 10); F.line([(380, 690), (700, 690)], (60, 70, 108), 10)
    # camas
    for x0 in (80, 640):
        F.rect(x0, 1150, x0 + 360, 1250, fill=(70, 80, 116))
        F.rect(x0, 1132, x0 + 360, 1160, fill=(150, 160, 196))
        F.rect(x0 + 20 if x0 < 500 else x0 + 250, 1100, x0 + 110 if x0 < 500 else x0 + 340, 1140, fill=(205, 210, 230))
        for lx in (x0 + 12, x0 + 348): F.line([(lx, 1250), (lx, 1290)], (50, 58, 86), 10)

def ventana(t, D, fi):
    z = lerp(1.22, 1.45, ease(t / D))
    F = Frame(base("cuarto"), dict(x=lerp(520, 470, ease(t / D)), y=lerp(880, 840, ease(t / D)), z=z))
    ap = seg(t, 1.3, 2.2)
    cuarto(F, t=t, enemigo=ap)
    s = ease(seg(t, 0.6, 1.2))
    p = mix(pose(l1u=0, l2u=0, l1l=0, l2l=0, a1u=10, a2u=-10), pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=40, a1l=30, a2u=-20), s)
    LEO.draw(F, add(p, jitter(t, 2 * s, 1)), lerp(250, 230, s), lerp(1135, 1150, s), f=1, rot=lerp(-90, 0, s), snap=False,
             face="scared" if t > 1.4 else ("closed" if t < 0.6 else "neutral"))
    fx = dict(glitch=0.25 if (ap > 0 and fi % 7 < 2) else 0.0)
    return F.finish(), fx

def cara(t, D, fi):
    sh = 18 * (1 - seg(t, 0, D)) + 6
    F = Frame(base("oscuro"), dict(x=540 + noise(t * 30, 1) * sh / 4, y=640, z=lerp(3.6, 4.4, ease(t / D)), sx=noise(t * 40) * sh, sy=noise(t * 40, 2) * sh))
    F.rect(300, 400, 800, 900, fill=GLASS)
    SONRIENTE.draw(F, add(STAND, jitter(t, 10, 5)), 540, 760, f=-1, snap=False)
    F.rect(380, 880, 700, 1250, fill=(22, 28, 48))
    F.line([(380, 690), (700, 690)], (60, 70, 108), 6)
    return F.finish(), dict(flash=((255, 255, 255), 1 - seg(t, 0, 0.3)), glitch=0.5 + 0.3 * (fi % 4 == 0), tint=((255, 30, 40), 0.25))

def nora(t, D, fi):
    zp = ease(seg(t, D * 0.72, D))
    F = Frame(base("cuarto"), dict(x=lerp(560, 540, zp), y=lerp(890, 700, zp), z=lerp(1.22, 2.0, zp)))
    cuarto(F)
    r = seg(t, 0, 1.3)
    if r < 1:
        LEO.draw(F, run(t), lerp(300, 610, r), 1250, f=1, face="scared")
    else:
        LEO.draw(F, add(mix(STAND, POINT, ease(seg(t, 1.6, 2.0))), {"a1u": 0}), 610, 1250, f=-1,
                 face="scared" if t > 2.6 else "talk", t=t)
    s = ease(seg(t, 1.1, 1.7))
    p = mix(pose(l1u=0, l2u=0, l1l=0, l2l=0), pose(l1u=-90, l1l=0, l2u=-86, l2l=0, a1u=-30, a1l=-20), s)
    look = seg(t, 2.0, 2.4)
    NORA.draw(F, p, lerp(830, 860, s), lerp(1135, 1150, s), f=1 if look < 0.5 else -1, rot=lerp(90, 0, s), snap=False,
              face="closed" if t < 1.2 else ("scared" if t > 2.6 else "neutral"))
    if t > D * 0.8:
        F.text((540, 690), "?", 150, (255, 214, 0), stroke=6)
    return F.finish(), {}

def ciudad(t, D, fi):
    F = Frame(base("ciudad"), dict(x=540, y=1000, z=lerp(1.18, 1.0, ease(t / D))))
    F.circle((820, 420), 70, fill=(225, 230, 240))
    rnd = random.Random(11); x = -260
    while x < 1340:
        w = rnd.randint(130, 230); h = rnd.randint(420, 1050); top = 1480 - h
        F.rect(x, top, x + w - 8, 1480, fill=(14, 17, 32))
        off = 0.25 * D + (x + 260) / 1600 * 0.6 * D
        for wy in range(int(top) + 30, 1450, 58):
            for wx in range(x + 18, x + w - 30, 42):
                lit = (rnd.random() < 0.7) and (t < off + rnd.random() * 0.25)
                F.rect(wx, wy, wx + 20, wy + 30, fill=(255, 210, 120) if lit else (24, 28, 46))
        x += w
    F.rect(-400, 1480, 1500, 2600, fill=(6, 7, 12))
    return F.finish(), dict(dark=0.25 * seg(t, 0.6 * D, D))

def ejercito(t, D, fi):
    F = Frame(base("alba"), dict(x=lerp(420, 560, t / D), y=1130, z=1.3, sy=abs(math.sin(t * 2 * math.pi * 1.6)) * 6))
    F.rect(-400, 1380, 1500, 2600, fill=(42, 46, 54))
    F.rect(-400, 1380, 1500, 1400, fill=(60, 64, 74))
    for i in range(8): F.rect(-300 + i * 220, 1600, -200 + i * 220, 1620, fill=(200, 200, 160))
    # barrera
    F.line([(720, 1380), (720, 1270)], (60, 60, 60), 14); F.line([(1040, 1380), (1040, 1270)], (60, 60, 60), 14)
    for i in range(8):
        F.poly([(700 + i * 45, 1250), (740 + i * 45, 1250), (760 + i * 45, 1290), (720 + i * 45, 1290)],
               fill=(220, 40, 40) if i % 2 == 0 else (245, 245, 245))
    F.line([(770, 1040), (770, 1250)], (60, 60, 60), 10)
    F.rect(650, 880, 890, 1040, fill=(255, 205, 0), outline=(20, 20, 20), w=6)
    F.text((770, 932), tr("ZONA"), 50, (20, 20, 20)); F.text((770, 992), tr("CERRADA"), 50, (20, 20, 20))
    for i in range(5):
        x = -150 + i * 160 + 150 * t
        SOLDADO.draw(F, add(walk(t + i * 0.08), {"a1u": 55, "a1l": 30, "a2u": 40, "a2l": 60}), x, 1395 + (i % 2) * 18, f=1, face="angry")
    return F.finish(), {}

def doctor(t, D, fi):
    F = Frame(base("hospital"), dict(x=560, y=990, z=1.15))
    F.rect(-400, 1180, 1500, 2600, fill=(96, 124, 132))
    # monitor
    flat = t > D * 0.58
    F.rect(330, 560, 750, 820, fill=(30, 34, 38)); F.rect(350, 580, 730, 800, fill=(6, 20, 14))
    pts = []
    for i in range(80):
        xx_ = 350 + i * 380 / 79
        ph = (i / 79 * 3 - t * 1.6) % 1
        yv = 0 if flat else (-90 if 0.48 < ph < 0.52 else (40 if 0.52 <= ph < 0.56 else 0))
        pts.append((xx_, 700 + yv))
    F.line(pts, (255, 60, 60) if flat else (60, 255, 140), 6)
    F.line([(540, 820), (540, 1000)], (40, 44, 50), 8)
    # cama del fondo con paciente
    F.rect(200, 1000, 880, 1070, fill=(235, 238, 242)); F.rect(200, 1070, 880, 1100, fill=(90, 100, 110))
    PACIENTE.draw(F, pose(l1u=0, l2u=0, l1l=0, l2l=0), 520, 985, f=1, rot=-90, snap=False, face="closed")
    F.rect(430, 1000, 880, 1050, fill=(160, 200, 225))
    # primer plano
    DOCTOR.draw(F, add(TALK, {"a1u": 25 * math.sin(t * 5), "a1l": 30 * math.sin(t * 4)}), 250, 1400, f=1, face="talk" if not flat else "neutral", t=t)
    sc = "scared" if t > D * 0.62 else "neutral"
    LEO.draw(F, SCARED if t > D * 0.62 else STAND, 720, 1400, f=-1, face=sc)
    NORA.draw(F, SCARED if t > D * 0.66 else STAND, 890, 1420, f=-1, face=sc)
    return F.finish(), dict(dark=0.18 * flat)

def leo_ojos(t, D, fi):
    pos = t > 0.45 and not (0.6 < t < 0.75 or 0.9 < t < 0.98)
    sh = 10 if pos else 0
    F = Frame(base("oscuro"), dict(x=540, y=1255, z=lerp(3.4, 4.0, ease(t / D)), sx=noise(t * 40) * sh, sy=noise(t * 40, 4) * sh))
    LEO.draw(F, STAND, 540, 1500, f=1, face="possessed" if pos else "scared")
    return F.finish(), dict(flash=((255, 20, 30), 0.6 * (1 - seg(t, 0.45, 0.8))), glitch=0.45 if pos and fi % 3 == 0 else 0.0,
                            tint=((255, 0, 20), 0.22 if pos else 0))

def pasillo(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    VP = (540, 860); off = t > D * 0.78
    F.poly([(-10, 1930), (1090, 1930), (640, 960), (440, 960)], fill=(26, 28, 38))
    F.poly([(-10, -10), (1090, -10), (640, 760), (440, 760)], fill=(16, 17, 24))
    F.poly([(-10, -10), (440, 760), (440, 960), (-10, 1930)], fill=(21, 24, 34))
    F.poly([(1090, -10), (640, 760), (640, 960), (1090, 1930)], fill=(21, 24, 34))
    F.rect(440, 760, 640, 960, fill=(4, 4, 8))
    def at(u, x, y):  # interpola desde el punto de fuga
        return (VP[0] + (x - VP[0]) * u, VP[1] + (y - VP[1]) * u)
    for i, u in enumerate((0.2, 0.32, 0.5, 0.78, 1.15)):
        on = (not off) and noise(t * 6, i) > -0.35
        a, b = at(u, 440, -40), at(u, 640, -40)
        F.poly([a, b, at(u * 1.08, 640, -40), at(u * 1.08, 440, -40)], fill=(255, 250, 220) if on else (40, 40, 46))
        if on:
            c = at(u * 1.04, 540, 1900)
            F.ellipse(c, 260 * u, 50 * u, fill=(48, 50, 62))
        d0, d1 = at(u, 0, 300), at(u * 1.12, 0, 300)
        F.poly([d0, d1, at(u * 1.12, 0, 1700), at(u, 0, 1700)], fill=(12, 13, 20))
        e0, e1 = at(u, 1080, 300), at(u * 1.12, 1080, 300)
        F.poly([e0, e1, at(u * 1.12, 1080, 1700), at(u, 1080, 1700)], fill=(12, 13, 20))
    u = ease(seg(t, 0, D * 0.95))
    sc = lerp(0.28, 1.25, u)
    SONRIENTE.scale = 1.45 * sc / 1.0
    SONRIENTE.draw(F, add(walk(t, 1.0, 0.8), jitter(t, 8, 9)), 540 + noise(t * 2, 7) * 20, lerp(960, 1720, u), f=1)
    SONRIENTE.scale = 1.45
    LEO.scale = 1.5
    LEO.draw(F, SCARED, 930, 1990, f=-1, face="scared")
    LEO.scale = 1.0
    return F.finish(), dict(dark=0.35 if off else 0.0, glitch=0.2 if (fi % 9 == 0) else 0.0)

def _calle(F):
    F.rect(-400, 1450, 1500, 2600, fill=(20, 21, 30))
    F.line([(-400, 1450), (1500, 1450)], (50, 52, 70), 6)
    F.line([(950, 1450), (950, 700)], (40, 42, 56), 12); F.line([(950, 700), (870, 700)], (40, 42, 56), 10)
    F.ellipse((860, 715), 34, 14, fill=(255, 230, 160))

def disparos(t, D, fi):
    k = seg(t, D * 0.66, D * 0.74)
    shk = 22 * (1 - seg(t, D * 0.7, D * 0.95)) * (t > D * 0.68)
    F = Frame(base("calle"), dict(x=560, y=1200, z=1.25, sx=noise(t * 50) * shk, sy=noise(t * 50, 3) * shk))
    _calle(F)
    ex = lerp(900, 760, ease(seg(t, 0, D * 0.7)))
    swipe = ease(k)
    pe = add(add(walk(t, 0.7, 0.6), jitter(t, 6, 2)), {"a1u": 120 * swipe, "a1l": -20 * swipe})
    if k > 0: pe = add(mix(STAND, pose(a1u=130, a1l=-10, body=-10), swipe), jitter(t, 4, 2))
    JE = SONRIENTE.draw(F, pe, ex, 1452, f=-1)
    firing = t < D * 0.66
    for i, (x, y) in enumerate(((190, 1460), (330, 1490), (470, 1520))):
        fly = seg(t, D * 0.7 + i * 0.03, D * 0.95)
        if fly > 0:
            SOLDADO.draw(F, pose(a1u=160, a2u=-150, l1u=40, l2u=-30), x - 500 * ease_out(fly), y - 500 * math.sin(fly * math.pi) * 0.8,
                         f=1, rot=-360 * fly, snap=False, face="scared")
            continue
        J = SOLDADO.draw(F, add(AIM, {"body": 4 * math.sin(t * 40) * firing}), x, y, f=1, face="angry")
        hx, hy = J["a1h"]; sx_, sy_ = J["sh"]; n = math.hypot(hx - sx_, hy - sy_)
        tip = (hx + (hx - sx_) / n * 50, hy + (hy - sy_) / n * 50)
        if firing and (fi + i * 2) % 5 < 2:
            pts = [(tip[0] + math.cos(a) * (34 if j % 2 == 0 else 14), tip[1] + math.sin(a) * (34 if j % 2 == 0 else 14))
                   for j, a in enumerate(i_ * math.pi / 5 for i_ in range(10))]
            F.poly(pts, fill=(255, 220, 90))
            F.line([(tip[0] + 40, tip[1]), (1150, tip[1] - 40 + i * 25)], (255, 240, 170), 3)
    if firing:
        for j in range(5):
            r = random.Random(fi // 2 * 10 + j); a = (fi % 6) / 6
            c = (JE["hip"][0] + r.uniform(-40, 40), JE["hip"][1] + r.uniform(-150, 10))
            F.circle(c, 18 + 30 * a, fill=(120 + int(60 * (1 - a)),) * 3)
    return F.finish(), dict(flash=((255, 255, 255), 0.7 * (1 - seg(t, D * 0.68, D * 0.78)) * (t > D * 0.68)))

NORA_M = Fig(shirt=(160, 90, 255), extra=("ponytail", "mirror"))

def idea(t, D, fi):
    pz = ease_back(seg(t, D * 0.62, D * 0.72))
    F = Frame(base("morado"), dict(x=600, y=1290, z=1.35 + 0.35 * pz))
    F.rect(-400, 1500, 1500, 2600, fill=(12, 8, 20))
    has = t > D * 0.62
    if not has:
        F.ellipse((800, 1250), 70, 100, fill=GOLD); F.ellipse((800, 1250), 55, 84, fill=(150, 170, 200))
    if has:
        NORA_M.draw(F, HOLD_UP, 540, 1500, f=1, face="angry")
    else:
        NORA.draw(F, THINK, 540, 1500, f=1, face="neutral")
    b = ease_back(seg(t, D * 0.3, D * 0.42))
    if b > 0:
        c = (540, 980 - (40 if has else 0)); r = 52 * b
        for i in range(8):
            a = i * math.pi / 4 + t
            F.line([(c[0] + math.cos(a) * r * 1.4, c[1] + math.sin(a) * r * 1.4), (c[0] + math.cos(a) * r * 1.9, c[1] + math.sin(a) * r * 1.9)], (255, 230, 90), 8)
        F.circle(c, r, fill=(255, 225, 80)); F.rect(c[0] - r * 0.4, c[1] + r * 0.8, c[0] + r * 0.4, c[1] + r * 1.3, fill=(170, 170, 180))
    return F.finish(), dict(flash=((255, 255, 255), 0.5 * (1 - seg(t, D * 0.62, D * 0.7)) * has))

def espejo(t, D, fi):
    fl = t > D * 0.42
    shk = 10 if fl else 0
    F = Frame(base("oscuro"), dict(x=520, y=1280, z=1.25, sx=noise(t * 45) * shk, sy=noise(t * 45, 1) * shk))
    F.rect(-400, 1500, 1500, 2600, fill=(8, 8, 14))
    ex = lerp(980, 820, ease(seg(t, 0, D * 0.42)))
    J = NORA_M.draw(F, add(HOLD_UP, jitter(t, 2, 4)), 380, 1500, f=1, face="angry")
    LEO.draw(F, SCARED, 170, 1500, f=1, face="closed")
    pe = add(pose(a1u=80, a1l=-10, body=-12), jitter(t, 4 + 14 * fl, 6))
    JE = SONRIENTE.draw(F, pe, ex, 1500, f=-1)
    if fl:
        m = ((J["a1h"][0] + J["a2h"][0]) / 2, (J["a1h"][1] + J["a2h"][1]) / 2 - 30)
        hc = JE["head"]; w = 30 + 20 * math.sin(t * 30)
        F.poly([m, (hc[0], hc[1] - 90 - w), (hc[0] + 40, hc[1]), (hc[0], hc[1] + 90 + w)], fill=(255, 250, 215))
        F.circle(m, 60, fill=(255, 255, 240))
    return F.finish(), dict(flash=((255, 255, 240), 0.8 * (1 - seg(t, D * 0.42, D * 0.6)) * fl), glitch=0.25 if fl and fi % 4 == 0 else 0)

def estallido(t, D, fi):
    T0 = D * 0.5; boom = t >= T0
    shk = (14 + 30 * seg(t, 0, T0)) if not boom else 40 * (1 - seg(t, T0, T0 + 1.0))
    F = Frame(base("oscuro"), dict(x=540, y=1240, z=lerp(1.15, 1.4, seg(t, 0, T0)) if not boom else lerp(1.4, 1.1, ease_out(seg(t, T0, T0 + 0.5))),
                                  sx=noise(t * 55) * shk, sy=noise(t * 55, 8) * shk))
    F.rect(-400, 1500, 1500, 2600, fill=(8, 8, 14))
    if not boom:
        amt = 12 + 40 * seg(t, 0, T0)
        SONRIENTE.draw(F, add(pose(a1u=150, a2u=-150, head=20 * math.sin(t * 25)), jitter(t * 1.5, amt, 11)), 540, 1500, f=1 if (fi // 3) % 2 else -1,
                       stretch=1 + 0.12 * math.sin(t * 40))
        fx = dict(flash=((255, 30, 40) if (fi // 3) % 2 else (255, 255, 255), 0.25), glitch=0.3, tint=((255, 0, 30), 0.2))
    else:
        u = t - T0
        F.circle((540, 1180), 120 + 1400 * ease_out(seg(u, 0, 0.6)), outline=(255, 255, 255), w=max(1, 30 * (1 - seg(u, 0, 0.6))))
        for i in range(80):
            r = random.Random(i)
            a = r.uniform(0, 2 * math.pi); v = r.uniform(500, 1600)
            x = 540 + math.cos(a) * v * u; y = 1180 + math.sin(a) * v * u + 900 * u * u
            s_ = r.uniform(10, 34) * (1 - seg(u, 0.6, 2.2)); rot = r.uniform(0, 6) + u * r.uniform(-12, 12)
            if s_ <= 1: continue
            pts = [(x + math.cos(rot + k * 2.1) * s_, y + math.sin(rot + k * 2.1) * s_) for k in range(3)]
            F.poly(pts, fill=(6, 6, 10), outline=(205, 190, 255), w=3)
        fx = dict(flash=((255, 255, 255), 1 - seg(u, 0, 0.35)))
    return F.finish(), fx

def amanecer(t, D, fi):
    F = Frame(base("amanecer"), dict(x=540, y=1100, z=lerp(1.0, 1.12, ease(t / D))))
    F.circle((540, lerp(1380, 1180, ease(t / D))), 160, fill=(255, 244, 190))
    F.ellipse((540, 1700), 1100, 300, fill=(40, 52, 40)); F.rect(-400, 1700, 1500, 2600, fill=(40, 52, 40))
    for i, (fig, x, ph) in enumerate(((LEO, 400, 0.0), (NORA, 680, 0.35))):
        j = abs(math.sin((t * 2.2 + ph) * math.pi))
        fig.draw(F, mix(STAND, CHEER, j), x, 1480 - 120 * j, f=1 if i == 0 else -1, face="happy")
    return F.finish(), dict(grain=4)

def giro(t, D, fi):
    zz = ease_out(seg(t, D * 0.82, D * 0.95))
    F = Frame(base("oscuro"), dict(x=540, y=lerp(960, 900, zz), z=lerp(1.0, 1.15, ease(t / D)) + 1.4 * zz))
    F.rect(-400, 1500, 1500, 2600, fill=(10, 10, 16))
    F.ellipse((540, 960), 330, 470, fill=GOLD); F.ellipse((540, 960), 290, 430, fill=(70, 86, 108))
    F.line([(380, 700), (470, 610)], (130, 150, 175), 10)
    a = ease(seg(t, D * 0.45, D * 0.8))
    if a > 0:
        col = tuple(int(lerp(c0, 255, a)) for c0 in (70, 86, 108))
        for dx in (-70, 70): F.circle((540 + dx, 860), 24 * a + 4, fill=col)
        F.arc((540, 880), 150, 20, 160, col, 18)
        for i in range(-4, 5):
            an = math.radians(90 - i * 15); cx, cy = 540 + math.cos(an) * 150, 880 + math.sin(an) * 150
            F.line([(cx, cy - 26), (cx, cy + 4)], col, 7, round_=False)
    return F.finish(), dict(glitch=0.6 * zz, flash=((255, 0, 30), 0.35 * zz), tint=((255, 0, 30), 0.15 * a))

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    on = noise(t * 5, 3) > -0.4
    if on:
        SONRIENTE.scale = 3.2
        SONRIENTE.draw(F, STAND, 540, 2700, f=1)
        SONRIENTE.scale = 1.45
    img = F.finish()
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.05, 0.4))
    if p > 0:
        d.text((540, 560), tr("PARTE 2"), font=font(190 * p), fill=(255, 214, 0), anchor="mm", stroke_width=int(14 * p), stroke_fill=(0, 0, 0))
    q = ease_back(seg(t, 1.2, 1.5)) * (1 + 0.06 * math.sin(t * 9))
    if q > 0:
        d.rounded_rectangle((210, 740, 870, 880), 30, fill=(230, 30, 50))
        d.text((540, 810), tr("SÍGUEME →"), font=font(84 * min(q, 1.06)), fill=(255, 255, 255), anchor="mm")
    return img, dict(glitch=0.3 if not on else 0.0)

ESCENA_FN = dict(ventana=ventana, cara=cara, nora=nora, ciudad=ciudad, ejercito=ejercito, doctor=doctor, leo_ojos=leo_ojos,
                 pasillo=pasillo, disparos=disparos, idea=idea, espejo=espejo, estallido=estallido, amanecer=amanecer, giro=giro, final=final)
# segundos extra de imagen tras la frase (pausas dramáticas)
PAUSA = dict(ventana=0.5, cara=1.1, nora=0.6, ciudad=0.8, ejercito=0.6, doctor=0.8, leo_ojos=1.0, pasillo=0.9, disparos=1.2,
             idea=0.6, espejo=0.9, estallido=1.8, amanecer=0.9, giro=1.3, final=2.2)
