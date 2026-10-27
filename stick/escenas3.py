"""Escenas del episodio 3 (Dentro de Nora)."""
import math, random
from motor import *
from escenas import base, cuarto, GOLD, GLASS
from escenas2 import enemy, big, sala_lampara

LILA = (205, 190, 255)
YEL = (255, 214, 0)

def cara_sonriente(F, c, r, glow=1.0):
    F.circle(c, r * 1.12, fill=LILA); F.circle(c, r, fill=(6, 6, 10))
    for dx in (-0.36, 0.36): F.circle((c[0] + dx * r, c[1] - 0.25 * r), 0.19 * r * glow, fill=(255, 255, 255))
    F.arc((c[0], c[1] - 0.1 * r), 0.66 * r, 20, 160, (255, 255, 255), max(2, 0.14 * r))

def espejo(F, c, rx, ry, crack=0.0, sonrisa=0.0, seed=0):
    F.ellipse(c, rx, ry, fill=GOLD); F.ellipse(c, rx * 0.86, ry * 0.9, fill=(70, 86, 108))
    if crack > 0:
        r = random.Random(seed)
        for k in range(5):
            a = r.uniform(0, 2 * math.pi); pts = [c]; x, y = c
            for s in range(4):
                a += r.uniform(-0.6, 0.6); L = r.uniform(0.18, 0.3) * ry * crack
                x += math.cos(a) * L; y += math.sin(a) * L; pts.append((x, y))
            F.line(pts, (235, 240, 250), 4)
    if sonrisa > 0:
        col = tuple(int(lerp(a, 255, sonrisa)) for a in (70, 86, 108))
        F.arc((c[0], c[1] - ry * 0.05), rx * 0.45, 20, 160, col, max(3, rx * 0.08))

# ---------- escenas ----------
def sonrisa(t, D, fi):
    F = Frame(base("cuarto"), dict(x=540, y=1000, z=1.3))
    cuarto(F)
    w = ease(seg(t, 0, D * 0.6))
    NORA.draw(F, walk(t, 0.6, 0.6) if w < 1 else add(STAND, jitter(t, 2, 1)), lerp(80, 430, w), 1250, f=1,
              face="possessed" if t > D * 0.5 else "neutral", t=t)
    LEO.draw(F, mix(STAND, SCARED, ease(seg(t, D * 0.55, D * 0.7))), 820, 1250, f=-1, face="happy" if t < D * 0.5 else "scared")
    return F.finish(), dict(glitch=0.25 if t > D * 0.5 and fi % 6 == 0 else 0, tint=((255, 0, 30), 0.1 * (t > D * 0.5)))

def pared(t, D, fi):
    F = Frame(base("cuarto"), dict(x=640, y=1020, z=lerp(1.35, 1.6, ease(t / D))))
    F.rect(-400, 1250, 1500, 2600, fill=(10, 12, 20))
    F.rect(860, 300, 1500, 1250, fill=(30, 36, 60))
    # reloj de pared
    c = (640, 620); F.circle(c, 90, fill=(230, 230, 236), outline=(40, 40, 50), w=8)
    a1 = t * 4.0; a2 = t * 0.33
    F.line([c, (c[0] + math.sin(a1) * 70, c[1] - math.cos(a1) * 70)], (30, 30, 36), 6)
    F.line([c, (c[0] + math.sin(a2) * 45, c[1] - math.cos(a2) * 45)], (30, 30, 36), 9)
    NORA.draw(F, add(STAND, jitter(t, 1.5, 3)), 790, 1250, f=1, face="possessed")
    F.rect(260, 1150, 600, 1250, fill=(70, 80, 116)); F.rect(260, 1132, 600, 1160, fill=(150, 160, 196))
    peek = ease(seg(t, D * 0.4, D * 0.6))
    LEO.draw(F, pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=40, a1l=30, a2u=-20), 380, 1150 - 0 * peek, f=1, rot=lerp(-90, 0, peek), snap=False, face="scared")
    F.rect(270, 1150, 600, 1210, fill=(110, 120, 160))
    return F.finish(), dict(dark=0.3)

def espejos(t, D, fi):
    zp = ease(seg(t, D * 0.55, D))
    F = Frame(base("cuarto"), dict(x=540, y=lerp(900, 860, zp), z=lerp(1.0, 1.6, zp)))
    F.rect(-400, 1300, 1500, 2600, fill=(14, 16, 26))
    for i, (x, sd) in enumerate(((250, 1), (540, 2), (830, 3))):
        cr = ease_back(seg(t, 0.25 + i * 0.35, 0.45 + i * 0.35))
        espejo(F, (x, 860), 115, 165, crack=cr, sonrisa=ease(seg(t, D * 0.7, D)) if i == 1 else 0, seed=sd)
    return F.finish(), dict(glitch=0.35 if any(abs(t - (0.25 + i * 0.35)) < 0.08 for i in range(3)) else 0)

def rayos(t, D, fi):
    F = Frame(base("hospital"), dict(x=560, y=1000, z=1.15))
    F.rect(-400, 1300, 1500, 2600, fill=(96, 124, 132))
    on = ease(seg(t, 0.2, 0.5))
    F.rect(330, 380, 850, 1000, fill=(40, 46, 52)); F.rect(350, 400, 830, 980, fill=tuple(int(lerp(20, 170, on) * k) for k in (0.8, 0.95, 1.0)))
    if on > 0.5:
        sk = Fig(shirt=(240, 248, 255), limb=(240, 248, 255), scale=1.4)
        sk.draw(F, STAND, 590, 950, f=1, face="closed")
        g = ease_back(seg(t, D * 0.55, D * 0.7))
        if g > 0: cara_sonriente(F, (590, 780), 42 * g)
    DOCTOR.draw(F, add(POINT, {"a1u": 60}), 200, 1440, f=1, face="talk" if t < D * 0.8 else "neutral", t=t)
    LEO.draw(F, SCARED if t > D * 0.6 else STAND, 900, 1440, f=-1, face="scared" if t > D * 0.6 else "neutral")
    return F.finish(), {}

def ojo_prohibido(F, c, s):
    F.ellipse(c, 110 * s, 60 * s, fill=(255, 255, 255), outline=(20, 20, 20), w=6)
    F.circle(c, 36 * s, fill=(20, 20, 30))
    F.circle(c, 150 * s, outline=(230, 30, 50), w=18 * s)
    F.line([(c[0] - 105 * s, c[1] + 105 * s), (c[0] + 105 * s, c[1] - 105 * s)], (230, 30, 50), 18 * s)

def prohibido(t, D, fi):
    F = Frame(base("hospital"), dict(x=560, y=1050, z=1.2))
    F.rect(-400, 1300, 1500, 2600, fill=(96, 124, 132))
    F.rect(240, 1110, 860, 1180, fill=(235, 238, 242)); F.rect(240, 1180, 860, 1210, fill=(90, 100, 110))
    big(NORA, 0.95, F, pose(l1u=0, l2u=0, l1l=0, l2l=0), 440, 1090, f=1, rot=-90, snap=False, face="closed")
    F.rect(480, 1085, 860, 1140, fill=(170, 150, 220))
    LEO.draw(F, mix(STAND, pose(a1u=-20, a2u=20, body=-6), ease(seg(t, D * 0.5, D * 0.7))), 940, 1440, f=-1, face="angry" if t > D * 0.6 else "scared")
    s = ease_back(seg(t, D * 0.55, D * 0.7))
    if s > 0: ojo_prohibido(F, (560, 640), s * (1 + 0.05 * math.sin(t * 8)))
    return F.finish(), dict(flash=((255, 30, 40), 0.25 * (1 - seg(t, D * 0.55, D * 0.7)) * (t > D * 0.55)))

def mirada(t, D, fi):
    zp = ease(seg(t, 0, D * 0.75))
    F = Frame(base("oscuro"), dict(x=540, y=980, z=lerp(2.2, 3.4, zp), sx=noise(t * 40) * 8 * zp, sy=noise(t * 40, 2) * 8 * zp))
    LEO.draw(F, STAND, 430, 1180, f=1, face="angry")
    NORA.draw(F, STAND, 650, 1190, f=-1, face="possessed")
    return F.finish(), dict(dark=ease(seg(t, D * 0.7, D * 0.92)), tint=((255, 0, 30), 0.2 * zp), glitch=0.4 if zp > 0.6 and fi % 4 == 0 else 0)

def caras_flotantes(F, t, n=14, seed=5, scale=1.0):
    for i in range(n):
        r = random.Random(seed + i)
        x = r.uniform(-100, 1180) + math.sin(t * r.uniform(0.3, 0.9) + i) * 40
        y = r.uniform(250, 1300) + math.cos(t * r.uniform(0.3, 0.8) + i) * 30
        cara_sonriente(F, (x, y), r.uniform(26, 70) * scale)

def mundo(t, D, fi):
    F = Frame(gradient((28, 28, 32), (8, 8, 10)), dict(x=540, y=1000, z=lerp(1.25, 1.0, ease(t / D))))
    caras_flotantes(F, t)
    F.rect(-400, 1400, 1500, 2600, fill=(12, 12, 14))
    LEO.draw(F, add(mix(SCARED, STAND, 0.5), {"head": 25 * math.sin(t * 2)}), 540, 1400, f=1 if math.sin(t * 2) > 0 else -1, face="scared")
    return F.finish(), dict(grain=10)

def barrotes(F, cx, base_y, h=360, w=260, rompe=0.0):
    for k in range(7):
        x = cx - w / 2 + k * w / 6
        r = random.Random(k)
        dx = r.uniform(-1, 1) * 600 * rompe; dy = -r.uniform(200, 700) * rompe + 900 * rompe * rompe
        rot = r.uniform(-1.5, 1.5) * rompe
        p0 = (x + dx, base_y + dy); p1 = (x + dx + math.sin(rot) * h, base_y + dy - math.cos(rot) * h)
        F.line([p0, p1], (255, 236, 150), 12)
    if rompe < 0.05:
        F.line([(cx - w / 2 - 10, base_y - h), (cx + w / 2 + 10, base_y - h)], (255, 236, 150), 14)
        F.line([(cx - w / 2 - 10, base_y), (cx + w / 2 + 10, base_y)], (255, 236, 150), 14)

def jaula(t, D, fi):
    F = Frame(gradient((28, 28, 32), (8, 8, 10)), dict(x=560, y=1100, z=1.25))
    caras_flotantes(F, t, n=8, seed=9, scale=0.8)
    F.rect(-400, 1400, 1500, 2600, fill=(12, 12, 14))
    F.ellipse((680, 1260), 200, 260, fill=(60, 56, 40))
    NORA.draw(F, SCARED, 680, 1400, f=-1, face="scared")
    barrotes(F, 680, 1400)
    w = ease(seg(t, 0, D * 0.5))
    LEO.draw(F, walk(t) if w < 1 else POINT, lerp(160, 380, w), 1400, f=1, face="scared" if w < 1 else "happy")
    return F.finish(), dict(grain=9)

def gigante(t, D, fi):
    rise = ease_out(seg(t, 0.2, D * 0.6))
    F = Frame(gradient((28, 28, 32), (8, 8, 10)), dict(x=560, y=lerp(1100, 900, rise), z=lerp(1.25, 1.0, rise), sx=noise(t * 40) * 10 * rise, sy=noise(t * 40, 3) * 10 * rise))
    F.rect(-400, 1400, 1500, 2600, fill=(12, 12, 14))
    enemy(F, add(pose(a1u=60, a1l=40, a2u=-60, a2l=-40, head=-8), jitter(t, 6, 4)), 760, lerp(2600, 1400, rise), 3.6, f=-1)
    F.ellipse((680, 1260), 200, 260, fill=(60, 56, 40))
    NORA.draw(F, SCARED, 680, 1400, f=-1, face="scared")
    barrotes(F, 680, 1400)
    LEO.draw(F, SCARED, 380, 1400, f=1, face="scared")
    return F.finish(), dict(tint=((255, 0, 30), 0.15 * rise), glitch=0.25 if fi % 5 == 0 and rise > 0.3 else 0)

def haz(F, hand, ang, L=1500, sp=0.13, col=(255, 248, 210)):
    F.poly([hand, (hand[0] + math.cos(ang - sp) * L, hand[1] + math.sin(ang - sp) * L), (hand[0] + math.cos(ang + sp) * L, hand[1] + math.sin(ang + sp) * L)], fill=col)

def linterna(t, D, fi):
    F = Frame(gradient((28, 28, 32), (8, 8, 10)), dict(x=560, y=1000, z=1.0))
    F.rect(-400, 1400, 1500, 2600, fill=(12, 12, 14))
    on = t > D * 0.65 and not (D * 0.7 < t < D * 0.74)
    flinch = ease(seg(t, D * 0.65, D * 0.8))
    enemy(F, add(pose(a1u=60 + 80 * flinch, a1l=40, a2u=-60 - 70 * flinch, head=-8 + 20 * flinch, body=-10 * flinch), jitter(t, 6 + 10 * flinch, 4)), 800, 1400, 3.6, f=-1)
    F.ellipse((680, 1260), 200, 260, fill=(60, 56, 40))
    NORA.draw(F, SCARED, 680, 1400, f=-1, face="scared")
    barrotes(F, 680, 1400)
    raise_ = ease(seg(t, D * 0.3, D * 0.6))
    J = LEO.draw(F, mix(STAND, pose(a1u=120, a1l=-10, body=4), raise_), 330, 1400, f=1, face="angry")
    hx, hy = J["a1h"]
    F.rect(hx - 14, hy - 14, hx + 34, hy + 14, fill=(60, 60, 70))
    if on: haz(F, (hx + 30, hy), math.radians(-38))
    return F.finish(), dict(flash=((255, 250, 220), 0.4 * (1 - seg(t, D * 0.65, D * 0.75)) * (t > D * 0.65)))

FLASH = (0.3, 0.55, 0.8)
def destellos(t, D, fi):
    hits = [D * h for h in FLASH]
    last = max([h for h in hits if h <= t] + [-9])
    k = sum(1 for h in hits if h <= t)
    shk = 26 * math.exp(-(t - last) * 8) if last > 0 else 0
    F = Frame(gradient((28, 28, 32), (8, 8, 10)), dict(x=560, y=1000, z=1.0, sx=noise(t * 50) * shk, sy=noise(t * 50, 1) * shk))
    F.rect(-400, 1400, 1500, 2600, fill=(12, 12, 14))
    back = ease_out(clamp(k / 3 + (t - last) * 0.6 if last > 0 else 0))
    enemy(F, add(pose(a1u=150, a2u=-150, head=20, body=-14), jitter(t * 1.5, 18, 6)), lerp(800, 1050, back), 1400, lerp(3.6, 2.4, back), f=-1)
    F.ellipse((680, 1260), 200, 260, fill=(60, 56, 40))
    NORA.draw(F, SCARED, 680, 1400, f=-1, face="scared")
    barrotes(F, 680, 1400)
    J = LEO.draw(F, pose(a1u=120, a1l=-10, body=4), 330, 1400, f=1, face="angry")
    hx, hy = J["a1h"]; F.rect(hx - 14, hy - 14, hx + 34, hy + 14, fill=(60, 60, 70))
    if last > 0 and t - last < 0.25: haz(F, (hx + 30, hy), math.radians(-38), sp=0.25)
    img = F.finish()
    if last > 0 and t - last < 0.35:
        d = ImageDraw.Draw(img); s = ease_back(seg(t, last, last + 0.12))
        d.text((540, 620), ["¡UNO!", "¡DOS!", "¡TRES!"][k - 1], font=font(170 * s), fill=YEL, anchor="mm", stroke_width=int(14 * s), stroke_fill=(0, 0, 0))
    return img, dict(flash=((255, 252, 230), 0.85 * math.exp(-(t - last) * 9) if last > 0 else 0))

def rescate(t, D, fi):
    F = Frame(gradient((28, 28, 32), (8, 8, 10)), dict(x=560, y=1100, z=1.25))
    F.rect(-400, 1400, 1500, 2600, fill=(12, 12, 14))
    b = ease_out(seg(t, D * 0.15, D * 0.55))
    barrotes(F, 680, 1400, rompe=b)
    hold = ease(seg(t, D * 0.55, D * 0.75))
    NORA.draw(F, mix(SCARED, pose(a2u=-70, a2l=10), hold), 680, 1400, f=-1, face="scared" if hold < 0.5 else "happy")
    LEO.draw(F, mix(pose(a1u=100, body=10), pose(a1u=75, a1l=0), hold), lerp(380, 520, hold), 1400, f=1, face="angry" if hold < 0.5 else "happy")
    return F.finish(), dict(flash=((255, 240, 180), 0.6 * (1 - seg(t, D * 0.15, D * 0.3)) * (t > D * 0.15)))

def puerta(t, D, fi):
    F = Frame(gradient((28, 28, 32), (8, 8, 10)), dict(x=560, y=1100, z=1.05))
    caras_flotantes(F, t * 3, n=10, seed=21, scale=0.7)
    F.rect(-400, 1450, 1500, 2600, fill=(12, 12, 14))
    near = ease(t / D)
    dx = lerp(1000, 820, near)
    F.rect(dx - 90, 1000, dx + 90, 1450, fill=(255, 250, 225)); F.ellipse((dx, 1440), 240, 30, fill=(90, 86, 60))
    enemy(F, add(run(t, 0.7), jitter(t, 8, 3)), lerp(-300, 0, near), 1452, 2.2, f=1)
    LEO.draw(F, run(t, 1.1), lerp(420, 640, near), 1452, f=1, face="scared")
    NORA.draw(F, run(t + 0.17, 1.1), lerp(300, 520, near), 1452, f=1, face="scared")
    return F.finish(), dict(flash=((255, 255, 240), ease(seg(t, D * 0.85, D))))

def amanecer(t, D, fi):
    F = Frame(base("hospital"), dict(x=540, y=1050, z=1.15))
    F.rect(-400, 1300, 1500, 2600, fill=(110, 140, 150))
    F.rect(360, 420, 720, 760, fill=(255, 226, 170)); F.circle((620, 560), 70, fill=(255, 246, 210))
    F.line([(540, 420), (540, 760)], (230, 230, 236), 10); F.line([(360, 590), (720, 590)], (230, 230, 236), 10)
    sit = ease(seg(t, 0.2, 0.9))
    for x0, fig, f in ((120, LEO, 1), (600, NORA, 1)):
        F.rect(x0, 1110, x0 + 380, 1180, fill=(235, 238, 242)); F.rect(x0, 1180, x0 + 380, 1210, fill=(90, 100, 110))
        fig.draw(F, mix(pose(l1u=90, l1l=0, l2u=86, l2l=0), pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=150, a2u=-150), ease(seg(t, 1.2, 1.6))),
                 x0 + 110, 1110, f=f, rot=lerp(-90, 0, sit), snap=False, face="closed" if sit < 0.5 else "happy")
        F.rect(x0 + 100, 1085, x0 + 380, 1140, fill=(150, 190, 220) if fig is LEO else (170, 150, 220))
    return F.finish(), dict(grain=4)

def giro(t, D, fi):
    zz = ease_out(seg(t, D * 0.68, D * 0.85))
    F = Frame(base("oscuro"), dict(x=lerp(560, 780, zz), y=lerp(1050, 790, zz), z=lerp(1.2, 3.2, zz)))
    F.rect(-400, 1350, 1500, 2600, fill=(26, 30, 36))
    for i in range(12): F.line([(-400 + i * 160, 0), (-400 + i * 160, 1350)], (24, 28, 36), 4)
    # lavabo + espejo
    F.rect(650, 1060, 910, 1110, fill=(220, 224, 230)); F.rect(740, 1110, 820, 1350, fill=(190, 196, 204))
    F.rect(640, 600, 920, 1000, fill=(120, 140, 160), outline=(200, 200, 210), w=10)
    poss = t > D * 0.68
    # reflejo del doctor (mirando hacia nosotros)
    big(DOCTOR, 0.9, F, STAND, 780, 1010, f=-1, face="possessed" if poss else "neutral", snap=True)
    F.rect(640, 1000, 920, 1060, fill=(26, 30, 36))
    # el doctor de espaldas (sin cara visible), delante del lavabo
    DOCTOR.draw(F, add(pose(a1u=60, a1l=60, a2u=50, a2l=70, head=10), {"a1l": 20 * math.sin(t * 6) * (t < D * 0.5)}), 420, 1350, f=1, face="closed")
    return F.finish(), dict(glitch=0.5 * zz, flash=((255, 0, 30), 0.2 * zz), tint=((255, 0, 30), 0.15 * zz), dark=0.1)

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    on = noise(t * 5, 3) > -0.4
    if on: big(DOCTOR, 3.4, F, STAND, 540, 2900, f=1, face="possessed")
    img = F.finish(); d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.05, 0.4))
    if p > 0: d.text((540, 560), "PARTE 4", font=font(190 * p), fill=YEL, anchor="mm", stroke_width=int(14 * p), stroke_fill=(0, 0, 0))
    q = ease_back(seg(t, 1.2, 1.5)) * (1 + 0.06 * math.sin(t * 9))
    if q > 0:
        d.rounded_rectangle((210, 740, 870, 880), 30, fill=(230, 30, 50))
        d.text((540, 810), "SÍGUEME →", font=font(84 * min(q, 1.06)), fill=(255, 255, 255), anchor="mm")
    return img, dict(glitch=0.3 if not on else 0.0, tint=((255, 0, 30), 0.12))

ESCENA_FN = dict(sonrisa=sonrisa, pared=pared, espejos=espejos, rayos=rayos, prohibido=prohibido, mirada=mirada, mundo=mundo, jaula=jaula,
                 gigante=gigante, linterna=linterna, destellos=destellos, rescate=rescate, puerta=puerta, amanecer=amanecer, giro=giro, final=final)
PAUSA = dict(sonrisa=0.8, pared=0.7, espejos=0.8, rayos=0.7, prohibido=0.8, mirada=1.0, mundo=0.7, jaula=0.6, gigante=1.0, linterna=0.8,
             destellos=0.8, rescate=0.6, puerta=0.7, amanecer=0.9, giro=1.4, final=2.2)
