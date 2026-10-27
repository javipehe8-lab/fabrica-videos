"""Escenas del episodio 2 (El faro). Reutiliza figuras, fondos y efectos del episodio 1."""
import math, random
from motor import *
from escenas import base, cuarto, GOLD, GLASS, NORA_M

WOOD, WOOD_D = (128, 84, 44), (72, 46, 22)
OLIVE, OLIVE_D = (84, 98, 58), (52, 62, 36)
BEAM = (255, 246, 200)

def enemy(F, p, x, y, scale, f=1, **kw):
    old = SONRIENTE.scale; SONRIENTE.scale = scale
    J = SONRIENTE.draw(F, p, x, y, f=f, **kw)
    SONRIENTE.scale = old
    return J

def big(fig, sc, F, p, x, y, **kw):
    old = fig.scale; fig.scale = sc
    J = fig.draw(F, p, x, y, **kw)
    fig.scale = old
    return J

# ---------- piezas ----------
def caja_draw(F, cx, cy, lid=0.0, locks=(1, 1, 1), w=300, h=180):
    """caja de madera con base en cy; lid = ángulo de apertura en grados"""
    F.rect(cx - w / 2, cy - h, cx + w / 2, cy, fill=WOOD, outline=WOOD_D, w=6)
    for k in (1, 2):
        F.line([(cx - w / 2 + 6, cy - h * k / 3), (cx + w / 2 - 6, cy - h * k / 3)], WOOD_D, 4, round_=False)
    for sx in (-1, 1):
        F.rect(cx + sx * w / 2 - (14 if sx > 0 else 0), cy - h, cx + sx * w / 2 + (14 if sx < 0 else 0), cy, fill=(60, 60, 66))
    hx, hy = cx - w / 2 - 5, cy - h
    a = math.radians(-lid)
    def R(px, py):
        dx, dy = px - hx, py - hy
        return (hx + dx * math.cos(a) - dy * math.sin(a), hy + dx * math.sin(a) + dy * math.cos(a))
    F.poly([R(hx, hy - 34), R(hx + w + 10, hy - 34), R(hx + w + 10, hy), R(hx, hy)], fill=(146, 98, 52), outline=WOOD_D, w=6)
    for i, x in enumerate((cx - 95, cx, cx + 95)):
        s = locks[i]
        if s <= 0.01: continue
        y = cy - h + 40
        F.arc((x, y - 16 * s), 18 * s, 180, 360, (170, 170, 178), 8 * s)
        F.rect(x - 24 * s, y - 16 * s, x + 24 * s, y + 22 * s, fill=GOLD, outline=(120, 90, 30), w=3)
        F.circle((x, y + 2 * s), 5 * s, fill=(60, 40, 10))

def faro_draw(F, x, yb, h=760, lit=0.0, beam_ang=None, cara=0.0, t=0.0):
    """faro con base en (x, yb). beam_ang en grados (0 = derecha)."""
    w0, w1 = 120, 74
    F.poly([(x - w0, yb), (x + w0, yb), (x + w1, yb - h), (x - w1, yb - h)], fill=(232, 232, 238), outline=(40, 40, 50), w=5)
    for k in range(1, 5):
        yy0 = yb - h * k / 5; ww = lerp(w0, w1, k / 5)
        if k % 2:
            yy1 = yb - h * (k + 0.5) / 5; ww1 = lerp(w0, w1, (k + 0.5) / 5)
            F.poly([(x - ww, yy0), (x + ww, yy0), (x + ww1, yy1), (x - ww1, yy1)], fill=(210, 50, 50))
    F.rect(x - 110, yb - h - 18, x + 110, yb - h, fill=(40, 40, 50))
    lc = (60, 70, 96) if lit < 0.05 else tuple(int(lerp(60, 255, lit) if i < 2 else lerp(96, 210, lit)) for i in range(3))
    F.rect(x - 66, yb - h - 150, x + 66, yb - h - 18, fill=lc, outline=(40, 40, 50), w=6)
    for k in (-22, 22): F.line([(x + k, yb - h - 150), (x + k, yb - h - 18)], (40, 40, 50), 5, round_=False)
    F.poly([(x - 84, yb - h - 150), (x + 84, yb - h - 150), (x, yb - h - 230)], fill=(40, 40, 50))
    F.rect(x - 22, yb - 120, x + 22, yb, fill=(70, 50, 34))
    lamp = (x, yb - h - 84)
    if cara > 0:
        enemy(F, add(pose(a1u=150 + 20 * math.sin(t * 14), a1l=-40, a2u=-150), jitter(t, 10, 4)), x, lamp[1] + 58, 0.42 * cara, f=1)
    if lit > 0 and beam_ang is not None:
        for sgn in (1, -1):
            ang = math.radians(beam_ang + (180 if sgn < 0 else 0))
            L_ = 1400; sp = 0.16
            p1 = (lamp[0] + math.cos(ang - sp) * L_, lamp[1] + math.sin(ang - sp) * L_)
            p2 = (lamp[0] + math.cos(ang + sp) * L_, lamp[1] + math.sin(ang + sp) * L_)
            F.poly([lamp, p1, p2], fill=tuple(int(lerp(c, 255, 0.0)) for c in BEAM) if sgn > 0 else (150, 146, 120))
        F.circle(lamp, 60 * lit, fill=(255, 255, 240))
    return lamp

def acantilado(F, x0=340, y0=1250, col=(10, 12, 20)):
    F.poly([(x0, 2600), (x0, y0 + 120), (x0 + 60, y0 + 40), (x0 + 160, y0), (1600, y0 - 10), (1600, 2600)], fill=col)

def camion(F, x, y, t, carga=(), lean=0.0):
    """camión militar mirando a la derecha; (x,y) = suelo bajo la rueda trasera"""
    F.rect(x - 40, y - 230, x + 330, y - 70, fill=OLIVE, outline=OLIVE_D, w=6)
    F.poly([(x - 40, y - 230), (x + 330, y - 230), (x + 300, y - 280), (x - 10, y - 280)], fill=OLIVE_D)
    F.rect(x + 340, y - 190, x + 470, y - 70, fill=OLIVE, outline=OLIVE_D, w=6)
    F.rect(x + 395, y - 175, x + 455, y - 125, fill=(150, 180, 200))
    for i, kind in enumerate(carga):
        hx = x + 30 + i * 80
        if kind in ("leo", "nora"):
            fig = LEO if kind == "leo" else NORA
            big(fig, 0.75, F, pose(a1u=20, a2u=-20), hx, y - 70, f=1, face="scared")
        elif kind == "soldado":
            big(SOLDADO, 0.75, F, pose(a1u=60, a1l=40, a2u=40, a2l=60), hx, y - 70, f=1, face="angry")
    F.rect(x - 40, y - 120, x + 330, y - 70, fill=OLIVE, outline=OLIVE_D, w=6)
    for wx in (x + 40, x + 250, x + 420):
        F.circle((wx, y - 40), 42, fill=(22, 22, 26))
        F.circle((wx, y - 40), 18, fill=(110, 110, 116))
        a = -t * 12
        F.line([(wx + math.cos(a) * 18, y - 40 + math.sin(a) * 18), (wx - math.cos(a) * 18, y - 40 - math.sin(a) * 18)], (40, 40, 44), 5)

def carretera(F, t, speed=900, y=1440):
    F.rect(-400, y, 1500, 2600, fill=(30, 30, 38))
    F.rect(-400, y, 1500, y + 12, fill=(70, 70, 82))
    off = (t * speed) % 240
    for i in range(-2, 8):
        xx = i * 240 - off
        F.rect(xx, y + 120, xx + 120, y + 136, fill=(220, 210, 140))

# ---------- escenas ----------
def caja(t, D, fi):
    F = Frame(base("cuarto"), dict(x=540, y=1000, z=lerp(1.3, 1.5, ease(t / D))))
    cuarto(F)
    put = ease(seg(t, 0.2, 1.0))
    lid = lerp(110, 0, ease(seg(t, 1.0, 1.5)))
    locks = tuple(ease_back(seg(t, D * (0.5 + 0.12 * i), D * (0.5 + 0.12 * i) + 0.25)) for i in range(3))
    if t < 1.0:
        my = lerp(820, 1120, put)
        F.ellipse((560, my), 44, 60, fill=GOLD); F.ellipse((560, my), 34, 50, fill=(175, 200, 222))
    caja_draw(F, 560, 1250, lid=lid, locks=locks)
    NORA.draw(F, mix(HOLD_UP, pose(a1u=60, a1l=20, a2u=40, a2l=30, body=12), put), 330, 1250, f=1, face="angry" if t > 1.5 else "neutral")
    LEO.draw(F, SCARED if t < 1.3 else STAND, 840, 1250, f=-1, face="scared" if t < 1.3 else "neutral")
    return F.finish(), {}

HITS = (0.25, 0.75, 1.15, 1.45, 1.7, 1.9, 2.05)
def golpes(t, D, fi):
    bump = max([math.sin(math.pi * clamp((t - h) / 0.22)) * (t >= h) * (t <= h + 0.22) for h in HITS] + [0])
    last = max([h for h in HITS if h <= t] + [-9])
    shk = 26 * math.exp(-(t - last) * 9) if last > 0 else 0
    F = Frame(base("cuarto"), dict(x=540, y=1050, z=1.35, sx=noise(t * 60) * shk, sy=noise(t * 60, 2) * shk))
    cuarto(F)
    caja_draw(F, 540 + noise(t * 30, 5) * 8 * bump, 1250 - 70 * bump, lid=10 * bump)
    wake = seg(t, 0.3, 0.7)
    for fig, x, f in ((LEO, 250, 1), (NORA, 830, -1)):
        p = mix(pose(l1u=0, l2u=0, l1l=0, l2l=0), pose(l1u=90 * f, l1l=0, l2u=86 * f, l2l=0, a1u=40, a1l=30, a2u=-20), wake)
        fig.draw(F, p, x, 1145, f=f, rot=lerp(-90 * f, 0, wake), snap=False, face="scared" if wake > 0.5 else "closed")
    img = F.finish()
    if last > 0 and t - last < 0.3:
        d = ImageDraw.Draw(img); s = ease_back(seg(t, last, last + 0.12))
        r = random.Random(int(last * 100))
        d.text((540 + r.randint(-220, 220), 760 + r.randint(-60, 60)), tr("¡BUM!"), font=font(150 * s), fill=(255, 214, 0), anchor="mm",
               stroke_width=int(12 * s), stroke_fill=(0, 0, 0))
    return img, dict(dark=0.25, flash=((255, 255, 255), 0.25 * math.exp(-(t - last) * 12) if last > 0 else 0))

CRACK = [(540, 960), (500, 900), (520, 840), (470, 760), (490, 690), (440, 610)]
CRACK2 = [(540, 960), (590, 1020), (570, 1090), (620, 1170), (600, 1250)]
CRACK3 = [(520, 840), (600, 800), (640, 740)]
def grieta(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=lerp(1.05, 1.3, ease(t / D)), sx=noise(t * 40) * 6, sy=noise(t * 40, 1) * 6))
    F.ellipse((540, 960), 330, 470, fill=GOLD); F.ellipse((540, 960), 290, 430, fill=(70, 86, 108))
    F.line([(380, 700), (470, 610)], (130, 150, 175), 10)
    g = ease(seg(t, 0.1, D * 0.45))
    for path, a0 in ((CRACK, 0), (CRACK2, 0.15), (CRACK3, 0.45)):
        k = clamp((g - a0) / (1 - a0)) * (len(path) - 1)
        n = int(k)
        pts = path[:n + 1]
        if n < len(path) - 1:
            f = k - n; a, b = path[n], path[n + 1]; pts = pts + [(lerp(a[0], b[0], f), lerp(a[1], b[1], f))]
        if len(pts) > 1: F.line(pts, (235, 240, 250), 7)
    s = ease(seg(t, D * 0.55, D * 0.8))
    if s > 0:
        col = tuple(int(lerp(c0, 255, s)) for c0 in (70, 86, 108))
        F.arc((540, 900), 160, 20, 160, col, 20)
        for i in range(-4, 5):
            an = math.radians(90 - i * 15); cx, cy = 540 + math.cos(an) * 160, 900 + math.sin(an) * 160
            F.line([(cx, cy - 28), (cx, cy + 4)], col, 8, round_=False)
        for dx in (-80, 80): F.circle((540 + dx, 860), 26 * s, fill=(255, 40, 40))
    return F.finish(), dict(glitch=0.35 * s + (0.3 if fi % 11 == 0 else 0), tint=((255, 0, 30), 0.18 * s), flash=((255, 255, 255), 0.4 * (1 - seg(t, D * 0.55, D * 0.65)) * (t > D * 0.55)))

def libro(t, D, fi):
    F = Frame(base("morado"), dict(x=540, y=1100, z=1.2))
    F.rect(-400, 1400, 1500, 2600, fill=(20, 14, 30))
    for i in range(5):  # estantería
        F.rect(-100, 380 + i * 170, 1180, 396 + i * 170, fill=(60, 40, 30))
        r = random.Random(i)
        x = -90
        while x < 1170:
            w = r.randint(24, 48); hh = r.randint(90, 150)
            F.rect(x, 380 + i * 170 - hh, x + w - 4, 380 + i * 170, fill=r.choice([(120, 40, 40), (40, 70, 110), (70, 100, 60), (140, 110, 50), (90, 60, 110)]))
            x += w
    # atril con libro
    F.poly([(440, 1400), (640, 1400), (600, 1180), (480, 1180)], fill=(80, 52, 30))
    op = ease_back(seg(t, 0.2, 0.7))
    F.poly([(540, 1180), (540 - 230 * op, 1160), (540 - 230 * op, 860), (540, 880)], fill=(236, 222, 186), outline=(120, 90, 50), w=4)
    F.poly([(540, 1180), (540 + 230 * op, 1160), (540 + 230 * op, 860), (540, 880)], fill=(244, 232, 200), outline=(120, 90, 50), w=4)
    if op > 0.9:
        ink = (60, 40, 30)
        F.circle((430, 990), 62, fill=(30, 26, 30))
        for dx in (-20, 20): F.circle((430 + dx, 975), 9, fill=(255, 255, 255))
        F.arc((430, 985), 34, 20, 160, (255, 255, 255), 6)
        for k in range(4): F.line([(350, 1080 + k * 18), (510, 1080 + k * 18)], (150, 130, 100), 4)
        cage = ease(seg(t, D * 0.62, D * 0.8))
        if cage > 0:
            for k in range(5):
                xx = 590 + k * 30
                F.line([(xx, 1060 - 140 * cage), (xx, 1060)], ink, 6)
            F.line([(580, 1060 - 140 * cage), (720, 1060 - 140 * cage)], ink, 6); F.line([(580, 1060), (720, 1060)], ink, 6)
            F.circle((655, 990), 24 * cage, fill=(30, 26, 30))
        nx = ease(seg(t, D * 0.35, D * 0.55))
        if nx > 0 and cage == 0:
            F.line([(600, 940), (700, 1040)], (200, 30, 30), 10 * nx); F.line([(700, 940), (600, 1040)], (200, 30, 30), 10 * nx)
    DOCTOR.draw(F, add(TALK, {"a1u": 30 * math.sin(t * 4)}), 210, 1400, f=1, face="talk", t=t)
    LEO.draw(F, SCARED if t > D * 0.4 else STAND, 840, 1400, f=-1, face="scared" if t > D * 0.4 else "neutral")
    NORA.draw(F, STAND, 960, 1410, f=-1, face="angry" if t > D * 0.7 else "neutral")
    return F.finish(), {}

def faro(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("ciudad"), dict(x=lerp(560, 760, zp), y=lerp(1000, 640, zp), z=lerp(1.0, 1.7, zp)))
    F.circle((220, 380), 60, fill=(225, 230, 240))
    F.rect(-400, 1300, 1500, 2600, fill=(12, 24, 44))
    for i in range(14):
        xx = (i * 130 + t * 60) % 1500 - 200
        F.line([(xx, 1340 + (i % 4) * 60), (xx + 70, 1340 + (i % 4) * 60)], (60, 90, 130), 4)
    acantilado(F, 520, 1230)
    lit = 0.5 + 0.5 * math.sin(t * 3)
    faro_draw(F, 800, 1230, h=600, lit=0.35 + 0.65 * ease(seg(t, D * 0.4, D * 0.7)) * lit, beam_ang=180 + 25 * math.sin(t * 1.2))
    return F.finish(), dict(grain=6)

def convoy(t, D, fi):
    F = Frame(base("alba"), dict(x=640, y=1180, z=1.1, sy=abs(math.sin(t * 20)) * 4))
    acantilado(F, 1120, 1080, col=(70, 80, 100))
    faro_draw(F, 1330, 1080, h=260, lit=0.0)
    carretera(F, t)
    camion(F, -380, 1440, t, carga=("soldado", "soldado", "soldado", "soldado"))
    camion(F, 280, 1440, t, carga=("leo", "nora", "soldado"))
    caja_draw(F, 540, 1370, w=120, h=80)
    return F.finish(), {}

def revienta(t, D, fi):
    T0 = D * 0.33; boom = t >= T0
    shk = 40 * math.exp(-(t - T0) * 4) if boom else 3
    F = Frame(base("alba"), dict(x=640, y=1180, z=1.1, sx=noise(t * 55) * shk, sy=noise(t * 55, 3) * shk))
    acantilado(F, 1120, 1080, col=(70, 80, 100))
    faro_draw(F, 1330, 1080, h=260, lit=0.0)
    carretera(F, t, speed=900 * (1 - seg(t, T0, T0 + 0.6)))
    camion(F, -380, 1440, t, carga=("soldado", "soldado", "soldado", "soldado"))
    camion(F, 280, 1440, t, carga=("leo", "nora", "soldado"))
    if not boom:
        caja_draw(F, 540 + noise(t * 40) * 10, 1370, w=120, h=80)
        fx = dict(dark=0.1)
    else:
        u = t - T0
        rise = ease_out(seg(u, 0.2, 1.4))
        if rise > 0:
            enemy(F, add(pose(a1u=150, a2u=-150, head=-10), jitter(t, 8, 5)), 540, lerp(1700, 1400, rise), lerp(0.4, 3.0, rise), f=1)
        for i in range(18):
            r = random.Random(i)
            a = r.uniform(-math.pi, 0); v = r.uniform(600, 1400)
            x = 540 + math.cos(a) * v * u; y = 1330 + math.sin(a) * v * u + 1300 * u * u
            rot = r.uniform(0, 6) + u * r.uniform(-14, 14); L_ = r.uniform(30, 60)
            if y < 1500:
                F.line([(x - math.cos(rot) * L_, y - math.sin(rot) * L_), (x + math.cos(rot) * L_, y + math.sin(rot) * L_)], WOOD, 14)
        F.circle((540, 1330), 40 + 900 * ease_out(seg(u, 0, 0.5)), outline=(255, 255, 255), w=max(1, 24 * (1 - seg(u, 0, 0.5))))
        fx = dict(flash=((255, 255, 255), 1 - seg(u, 0, 0.35)), tint=((255, 0, 30), 0.15 * rise), glitch=0.25 if fi % 5 == 0 else 0)
    return F.finish(), fx

def ataque(t, D, fi):
    shk = 10 + 8 * math.sin(t * 3)
    F = Frame(base("calle"), dict(x=540, y=1150, z=1.0, sx=noise(t * 45) * shk, sy=noise(t * 45, 1) * shk))
    F.rect(-400, 1450, 1500, 2600, fill=(28, 28, 36))
    TS = [D * (0.3 + 0.14 * i) for i in range(4)]
    grab = max([math.sin(math.pi * clamp((t - s) / 0.5)) for s in TS] + [0])
    JE = enemy(F, add(pose(a1u=100 + 60 * grab, a1l=-20, a2u=-30, a2l=20, body=-6), jitter(t, 6, 7)), 760, 1460, 3.0, f=-1)
    for i, (x, y) in enumerate(((120, 1460), (260, 1480), (400, 1500), (540, 1470))):
        fly = seg(t, TS[i], TS[i] + 0.45)
        if fly > 0:
            if fly < 1:
                SOLDADO.draw(F, pose(a1u=170, a2u=-160, l1u=30, l2u=-30), lerp(x, 760, ease(fly)), lerp(y, -200, ease(fly)) ,
                             f=1, rot=-200 * fly, snap=False, face="scared")
            continue
        firing = (fi + i * 2) % 5 < 2
        J = SOLDADO.draw(F, add(AIM, {"body": 4 * math.sin(t * 40) * firing}), x, y, f=1, face="scared" if t > TS[0] else "angry")
        if firing:
            hx, hy = J["a1h"]; F.circle((hx + 60, hy - 4), 18, fill=(255, 220, 90))
    return F.finish(), dict(tint=((255, 0, 30), 0.12), glitch=0.2 if fi % 6 == 0 else 0, flash=((255, 0, 0), 0.25 * grab))

def carrera(t, D, fi):
    F = Frame(base("ciudad"), dict(x=540, y=1100, z=1.05))
    near = ease(t / D)
    acantilado(F, lerp(880, 620, near), 1200, col=(14, 18, 30))
    faro_draw(F, lerp(1060, 860, near), 1200, h=lerp(360, 560, near), lit=0.15)
    F.rect(-400, 1450, 1500, 2600, fill=(18, 20, 30))
    off = (t * 800) % 160
    for i in range(-1, 10):
        F.rect(i * 160 - off, 1450, i * 160 - off + 70, 1462, fill=(50, 54, 70))
    ex = lerp(-260, 60, ease(seg(t, 0, D)))
    enemy(F, add(run(t, 0.8), jitter(t, 8, 3)), ex, 1452, 2.0, f=1)
    LEO.draw(F, run(t, 1.1), 560, 1452, f=1, face="scared")
    NORA.draw(F, run(t + 0.17, 1.1), 400, 1452, f=1, face="scared")
    return F.finish(), dict(glitch=0.15 if fi % 7 == 0 else 0)

FL = 230  # altura de cada tramo de escalera
def escalera(t, D, fi):
    u = 0.3 + 4.2 * ease(seg(t, 0, D * 0.92))
    def path(v):
        k = math.floor(v); f = v - k
        ya = 1600 - k * FL; yb = ya - FL
        xa, xb = (280, 800) if k % 2 == 0 else (800, 280)
        return lerp(xa, xb, f), lerp(ya, yb, f), (1 if k % 2 == 0 else -1)
    lx, ly, lf = path(u)
    F = Frame(base("oscuro"), dict(x=540, y=ly - 260, z=1.15))
    F.rect(200, -2000, 880, 2400, fill=(30, 32, 42))
    for k in range(-1, 8):
        ya = 1600 - k * FL; yb = ya - FL
        xa, xb = (280, 800) if k % 2 == 0 else (800, 280)
        F.poly([(xa, ya), (xb, yb), (xb, yb + 26), (xa, ya + 26)], fill=(70, 72, 86))
        n = 9
        for s in range(n):
            x0 = lerp(xa, xb, s / n); y0 = lerp(ya, yb, s / n); x1 = lerp(xa, xb, (s + 1) / n)
            F.line([(x0, y0), (x0, y0 - FL / n), (x1, y0 - FL / n)], (110, 112, 128), 5, round_=False)
        F.rect(xb - 60 if k % 2 == 0 else xb, yb - 4, xb if k % 2 == 0 else xb + 60, yb + 22, fill=(70, 72, 86))
    for side in (200, 880): F.line([(side, -2000), (side, 2400)], (12, 12, 18), 24, round_=False)
    for k in range(-1, 8):
        F.rect(500, 1600 - k * FL - 150, 580, 1600 - k * FL - 60, fill=(40, 60, 100) if k % 3 else (12, 18, 30))
    ex, ey, ef = path(u - 1.5)
    enemy(F, add(run(t, 0.7), jitter(t, 8, 2)), ex, ey, 1.15, f=ef)
    nx, ny, nf = path(u - 0.18)
    NORA.draw(F, run(t + 0.2, 1.2), nx, ny, f=nf, face="scared")
    LEO.draw(F, run(t, 1.2), lx, ly, f=lf, face="scared")
    img = F.finish()
    d = ImageDraw.Draw(img)
    n = min(114, int(114 * ease(seg(t, 0, D * 0.92))))
    d.rounded_rectangle((640, 260, 1030, 380), 24, fill=(0, 0, 0))
    d.text((835, 320), f"{n}/114", font=font(84), fill=(255, 214, 0) if n == 114 else (255, 255, 255), anchor="mm")
    return img, dict(dark=0.05)

def sala_lampara(F, lit=0.0, lever=0.0, shake=0.0):
    F.rect(-400, 1450, 1500, 2600, fill=(24, 24, 32))
    F.rect(120, 420, 960, 1180, fill=(16, 26, 46))
    for x in (120, 400, 680, 960): F.line([(x, 420), (x, 1180)], (50, 54, 70), 18, round_=False)
    F.line([(120, 800), (960, 800)], (50, 54, 70), 12, round_=False)
    F.rect(380, 1180, 700, 1450, fill=(56, 58, 70))
    col = tuple(int(lerp(a, b, lit)) for a, b in zip((110, 120, 150), (255, 250, 220)))
    F.ellipse((540, 1040), 170, 150, fill=col, outline=(60, 62, 80), w=8)
    for k in range(-3, 4): F.line([(540 + k * 40, 900), (540 + k * 40, 1180)], tuple(int(c * 0.85) for c in col), 5)
    # palanca
    F.rect(850, 1240, 930, 1450, fill=(80, 80, 92), outline=(40, 40, 50), w=4)
    a = math.radians(lerp(-40, 40, lever) + shake)
    tip = (890 + math.sin(a) * 180, 1260 - math.cos(a) * 180)
    F.line([(890, 1260), tip], (150, 150, 160), 16); F.circle(tip, 26, fill=(220, 40, 40))
    return tip

def palanca(t, D, fi):
    F = Frame(base("oscuro"), dict(x=640, y=1150, z=1.15))
    sh = 6 * math.sin(t * 50) * seg(t, D * 0.35, D * 0.4)
    tip = sala_lampara(F, shake=sh)
    LEO.draw(F, add(pose(body=-24, a1u=60, a1l=10, a2u=50, a2l=20, l1u=-24, l2u=24), jitter(t, 4 * (t > D * 0.35), 3)), tip[0] - 100, 1450, f=1, face="angry")
    img = F.finish()
    if t > D * 0.55:
        d = ImageDraw.Draw(img); s = ease_back(seg(t, D * 0.55, D * 0.65))
        d.text((540 + noise(t * 30) * 8, 520), tr("¡ATASCADA!"), font=font(110 * s), fill=(255, 60, 60), anchor="mm", stroke_width=int(10 * s), stroke_fill=(0, 0, 0))
    return img, {}

def frente(t, D, fi):
    zp = ease(seg(t, D * 0.5, D))
    F = Frame(base("oscuro"), dict(x=lerp(560, 600, zp), y=lerp(1150, 1000, zp), z=lerp(1.0, 1.9, zp), sx=noise(t * 40) * 6 * zp, sy=noise(t * 40, 2) * 6 * zp))
    sala_lampara(F)
    turn = seg(t, 0.4, 0.7)
    NORA.draw(F, mix(SCARED, pose(a1u=-30, a2u=30, head=-6), turn), 420, 1450, f=1 if turn > 0.5 else -1,
              face="scared" if turn < 0.5 else ("angry" if t < D * 0.75 else "possessed" if fi % 6 < 2 and t > D * 0.85 else "angry"))
    ex = lerp(1100, 760, ease(seg(t, 0, D * 0.5)))
    enemy(F, add(pose(a1u=40, a1l=30, a2u=-30, body=-8, head=-10), jitter(t, 6, 8)), ex, 1450, 2.4, f=-1)
    return F.finish(), dict(tint=((255, 0, 30), 0.25 * zp), glitch=0.3 if zp > 0.5 and fi % 4 == 0 else 0)

def luz(t, D, fi):
    T0 = D * 0.45; on = t >= T0
    shk = 30 * math.exp(-(t - T0) * 3) if on else 4
    F = Frame(base("oscuro"), dict(x=600, y=1150, z=1.05, sx=noise(t * 50) * shk, sy=noise(t * 50, 3) * shk))
    lit = ease(seg(t, T0, T0 + 0.3))
    tip = sala_lampara(F, lit=lit, lever=ease_out(seg(t, T0 - 0.15, T0)), shake=0 if on else 8 * math.sin(t * 50))
    if on:
        for k in range(10):
            a = k * math.pi / 5 + t * 2
            F.poly([(540, 1040), (540 + math.cos(a - 0.12) * 1600, 1040 + math.sin(a - 0.12) * 1600), (540 + math.cos(a + 0.12) * 1600, 1040 + math.sin(a + 0.12) * 1600)], fill=(255, 248, 210))
        F.circle((540, 1040), 220, fill=(255, 255, 245))
        sq = 1 - ease(seg(t, T0 + 0.2, D * 0.9))
        if sq > 0.02:
            enemy(F, add(pose(a1u=160, a2u=-160, head=25 * math.sin(t * 30)), jitter(t * 2, 30, 9)), lerp(760, 540, 1 - sq), lerp(1450, 1120, 1 - sq), 2.4 * sq + 0.2, f=-1)
    else:
        enemy(F, add(pose(a1u=60, a2u=-30), jitter(t, 6, 8)), 760, 1450, 2.4, f=-1)
    LEO.draw(F, add(pose(body=-24, a1u=60 - 70 * lit, a1l=10, a2u=50 - 60 * lit, a2l=20, l1u=-24, l2u=24), jitter(t, 4, 3)), tip[0] - 100 if not on else 790, 1450, f=1,
             face="angry" if not on else "closed")
    return F.finish(), dict(flash=((255, 255, 240), 0.9 * (1 - seg(t, T0, T0 + 0.5)) * on))

def encerrado(t, D, fi):
    zp = ease_out(seg(t, D * 0.35, D))
    F = Frame(base("amanecer"), dict(x=lerp(560, 640, zp), y=lerp(1050, 520, zp), z=lerp(1.0, 3.4, zp)))
    F.circle((200, 1300), 140, fill=(255, 238, 190))
    F.rect(-400, 1300, 1500, 2600, fill=(50, 90, 130))
    acantilado(F, 380, 1250, col=(36, 40, 50))
    faro_draw(F, 640, 1250, h=640, lit=1.0, beam_ang=200 + t * 50, cara=1.0, t=t)
    return F.finish(), dict(grain=4)

def giro(t, D, fi):
    T0 = D * 0.62
    zz = ease_out(seg(t, T0, T0 + 0.5))
    F = Frame(base("hospital"), dict(x=lerp(560, 290, zz), y=lerp(1080, 1078, zz), z=lerp(1.2, 4.6, zz)))
    F.rect(-400, 1300, 1500, 2600, fill=(80, 104, 112))
    F.rect(220, 1110, 780, 1180, fill=(235, 238, 242)); F.rect(220, 1180, 780, 1210, fill=(90, 100, 110))
    F.rect(225, 1065, 330, 1112, fill=(250, 250, 252))
    awake = t > T0
    big(NORA, 0.95, F, pose(l1u=0, l2u=0, l1l=0, l2l=0), 420, 1090, f=1, rot=-90, snap=False, face="possessed" if awake else "closed")
    F.rect(470, 1085, 780, 1140, fill=(170, 150, 220))
    flat = not awake
    pts = []
    for i in range(60):
        xx_ = 580 + i * 3.3; ph = (i / 59 * 2 - t * 1.4) % 1
        yv = 0 if flat and t > D * 0.2 else (-45 if 0.48 < ph < 0.52 else (20 if 0.52 <= ph < 0.56 else 0))
        pts.append((xx_, 760 + yv))
    F.rect(560, 690, 800, 830, fill=(30, 34, 38)); F.line(pts, (255, 60, 60) if flat and t > D * 0.2 else (60, 255, 140), 5)
    LEO.draw(F, pose(body=20, a1u=60, a1l=40, l1u=80, l1l=-80, l2u=70, l2l=-70), 930, 1300, f=-1, face="scared" if awake else "closed")
    return F.finish(), dict(glitch=0.5 * zz, flash=((255, 0, 30), 0.18 * zz), tint=((255, 0, 30), 0.12 * zz), dark=0.15)

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    on = noise(t * 5, 3) > -0.4
    if on:
        big(NORA, 3.4, F, STAND, 540, 2900, f=1, face="possessed")
    img = F.finish()
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.05, 0.4))
    if p > 0:
        d.text((540, 560), tr("PARTE 3"), font=font(190 * p), fill=(255, 214, 0), anchor="mm", stroke_width=int(14 * p), stroke_fill=(0, 0, 0))
    q = ease_back(seg(t, 1.2, 1.5)) * (1 + 0.06 * math.sin(t * 9))
    if q > 0:
        d.rounded_rectangle((210, 740, 870, 880), 30, fill=(230, 30, 50))
        d.text((540, 810), tr("SÍGUEME →"), font=font(84 * min(q, 1.06)), fill=(255, 255, 255), anchor="mm")
    return img, dict(glitch=0.3 if not on else 0.0, tint=((255, 0, 30), 0.12))

ESCENA_FN = dict(caja=caja, golpes=golpes, grieta=grieta, libro=libro, faro=faro, convoy=convoy, revienta=revienta, ataque=ataque,
                 carrera=carrera, escalera=escalera, palanca=palanca, frente=frente, luz=luz, encerrado=encerrado, giro=giro, final=final)
PAUSA = dict(caja=0.5, golpes=0.6, grieta=1.0, libro=0.7, faro=0.8, convoy=0.6, revienta=1.4, ataque=0.9, carrera=0.7, escalera=0.8,
             palanca=0.7, frente=1.0, luz=1.2, encerrado=0.9, giro=1.3, final=2.2)
