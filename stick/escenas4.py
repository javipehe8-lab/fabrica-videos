"""Escenas del episodio 4 (La grabación)."""
import math, random
import numpy as np
from PIL import Image
from motor import *
from escenas import base, cuarto, GOLD, GLASS
from escenas2 import enemy, big, faro_draw
from escenas3 import cara_sonriente, LILA, YEL

ROJO = (230, 30, 50)

# ---------- piezas ----------
def oficina_bg():
    return gradient((20, 24, 30), (8, 10, 14))
_OF = None
def feed_doctor(t, fi, poss=0.0, talk=True, cara=0.0, gl=0.0, z=1.0, roll=0.0):
    """imagen 1080x810 de la grabación del doctor (contenido de la tele)"""
    global _OF
    if _OF is None: _OF = oficina_bg()
    F = Frame(_OF, dict(x=540, y=900, z=z))
    F.rect(60, 420, 360, 1000, fill=(30, 34, 42)); F.rect(720, 420, 1020, 1000, fill=(30, 34, 42))
    for k in range(4):
        F.line([(60, 500 + k * 140), (360, 500 + k * 140)], (46, 52, 62), 10)
        F.line([(720, 500 + k * 140), (1020, 500 + k * 140)], (46, 52, 62), 10)
    pz = poss > 0.5
    if cara < 0.6:
        big(DOCTOR, 3.4, F, add(pose(a1u=35, a1l=100, a2u=-30, a2l=-60), jitter(t, 3 + 5 * poss, 2)), 540 + noise(t * 3) * 10, 1760, f=1,
            face="possessed" if pz else ("talk" if talk else "neutral"), t=t)
    if cara > 0:
        r = 380 * ease_back(clamp(cara)); cara_sonriente(F, (540, 860), r)
        for i in range(-4, 5):
            a = math.radians(90 - i * 15); cx, cy = 540 + math.cos(a) * 0.66 * r, 860 - 0.1 * r + math.sin(a) * 0.66 * r
            F.line([(cx, cy - 0.13 * r), (cx, cy + 0.02 * r)], (255, 255, 255), max(2, 0.035 * r), round_=False)
    img = F.finish()
    tint = ((255, 0, 30), 0.3 * poss + 0.3 * cara) if (poss or cara) else None
    img = post(img, fi, glitch=gl, grain=14, tint=tint)
    a = np.asarray(img)[495:1305]
    if roll: a = np.roll(a, int(roll) % 810, axis=0)
    return Image.fromarray(a)

def feed_estatico(fi):
    r = np.random.default_rng(fi)
    a = (r.random((101, 135)) * 200 + 30).astype(np.uint8)
    return Image.fromarray(np.stack([a, a, a], 2)).resize((1080, 810), Image.NEAREST)

_SCAN = {}
def pegar(img, F, box, feed):
    """pega la imagen de la tele en la caja (coords de mundo) con líneas de barrido"""
    (x0, y0), (x1, y1) = F.P(box[0], box[1]), F.P(box[2], box[3])
    x0, y0, x1, y1 = int(x0 / S), int(y0 / S), int(x1 / S), int(y1 / S)
    w, h = max(2, x1 - x0), max(2, y1 - y0)
    if w > 4000: return img
    im = np.asarray(feed.resize((w, h)), np.float32)
    if h not in _SCAN: _SCAN[h] = np.where((np.arange(h) // max(1, h // 200)) % 2 == 0, 1.0, 0.78).astype(np.float32)[:, None, None]
    yy_, xx_ = np.mgrid[0:h, 0:w].astype(np.float32)
    vig = (1 - 0.45 * (((xx_ - w / 2) / (w / 2)) ** 2 + ((yy_ - h / 2) / (h / 2)) ** 2) / 2)[..., None]
    im = np.clip(im * _SCAN[h] * vig * np.array((0.92, 1.0, 1.08)), 0, 255).astype(np.uint8)
    img.paste(Image.fromarray(im), (x0, y0))
    return img

TV = (150, 820, 390, 1000)   # pantalla de la tele del salón (mundo)
def tele_draw(F, glow=0.0, col=(170, 190, 220)):
    x0, y0, x1, y1 = TV
    F.line([(270, 780), (210, 690)], (90, 90, 100), 5); F.line([(270, 780), (340, 680)], (90, 90, 100), 5)
    F.rect(x0 - 40, y0 - 40, x1 + 40, y1 + 90, fill=(58, 48, 40), outline=(30, 24, 20), w=6)
    F.rect(x0 - 10, y0 - 10, x1 + 10, y1 + 10, fill=(20, 20, 24))
    for k, cx in enumerate((x1 - 10, x1 - 60)): F.circle((cx, y1 + 48), 16, fill=(30, 26, 22), outline=(120, 110, 96), w=3)
    F.rect(x0 + 10, y1 + 38, x0 + 120, y1 + 58, fill=(40, 34, 30))
    F.rect(x0 - 20, y1 + 90, x1 + 20, y1 + 120, fill=(40, 32, 26))
    for lx in (x0 - 10, x1 + 10): F.line([(lx, y1 + 120), (lx, 1300)], (40, 32, 26), 12)
    if glow > 0:
        F.poly([(x1, y0), (x1, y1), (1100, 1380), (1100, 500)], fill=tuple(int(c * 0.10 * glow + 14) for c in col))

def salon(F):
    F.rect(-400, 1300, 1500, 2600, fill=(10, 12, 20)); F.line([(-400, 1300), (1500, 1300)], (40, 46, 70), 6)
    F.rect(560, 520, 820, 760, fill=(30, 36, 58), outline=(50, 58, 90), w=10)

def sofa(F, front=False):
    if not front:
        F.rect(660, 1060, 1040, 1236, fill=(92, 58, 52), outline=(60, 36, 32), w=5)
    else:
        F.rect(640, 1232, 1040, 1300, fill=(110, 70, 62), outline=(60, 36, 32), w=5)
        F.rect(620, 1150, 680, 1300, fill=(100, 64, 56)); F.rect(1010, 1150, 1070, 1300, fill=(100, 64, 56))

SIT = pose(l1u=90, l1l=-90, l2u=86, l2l=-86, a1u=20, a1l=50, a2u=-10, a2l=40)

def radiacion(F, c, r):
    F.circle(c, r, fill=(250, 210, 0), outline=(20, 20, 20), w=5)
    x, y = F.P(*c); rr = r * 0.85 * F.z * S
    for a in (-90, 30, 150):
        F.d.pieslice([x - rr, y - rr, x + rr, y + rr], a - 30, a + 30, fill=(20, 20, 20))
    F.circle(c, r * 0.2, fill=(250, 210, 0)); F.circle(c, r * 0.13, fill=(20, 20, 20))

# ---------- escenas ----------
def camara(t, D, fi):
    zp = ease(t / D)
    sh = 6 + 6 * zp
    F = Frame(base("oscuro"), dict(x=lerp(580, 500, zp), y=lerp(1060, 1000, zp), z=lerp(1.5, 1.8, zp), sx=noise(t * 30) * sh, sy=noise(t * 30, 2) * sh))
    F.rect(-400, 1300, 1500, 2600, fill=(16, 18, 26))
    F.rect(80, 500, 420, 1100, fill=(28, 30, 40))
    for k in range(5): F.line([(80, 560 + k * 120), (420, 560 + k * 120)], (44, 46, 58), 10)
    F.rect(470, 1140, 690, 1160, fill=(70, 52, 36)); F.line([(485, 1160), (485, 1300)], (60, 44, 30), 10); F.line([(675, 1160), (675, 1300)], (60, 44, 30), 10)
    F.line([(640, 1140), (620, 1080), (650, 1060)], (60, 60, 70), 5); F.poly([(635, 1050), (675, 1050), (665, 1075), (645, 1075)], fill=(200, 170, 90))
    F.poly([(645, 1075), (665, 1075), (720, 1140), (590, 1140)], fill=(90, 80, 50))
    poss = noise(t * 3.5, 4) > 0.25 or (D * 0.55 < t < D * 0.62)
    reach = ease(seg(t, D * 0.2, D * 0.45))
    DOCTOR.draw(F, add(mix(pose(a1u=150, a1l=40, a2u=140, a2l=45, head=10), POINT, reach), jitter(t, 7, 3)), 360, 1300, f=1,
                face="possessed" if poss else "scared", t=t)
    # cámara sobre trípode
    for fx in (750, 890): F.line([(820, 1060), (fx, 1300)], (60, 60, 70), 8)
    F.line([(820, 1060), (820, 1300)], (60, 60, 70), 8)
    F.rect(770, 1000, 890, 1062, fill=(36, 36, 42), outline=(90, 90, 100), w=4)
    F.rect(720, 1012, 772, 1050, fill=(24, 24, 28)); F.circle((720, 1031), 18, fill=(60, 80, 110))
    if reach > 0.9 and (t * 2) % 1 < 0.6: F.circle((870, 990), 11, fill=(255, 30, 30))
    return F.finish(), dict(glitch=0.35 if poss and fi % 3 == 0 else 0, tint=((255, 0, 30), 0.18 if poss else 0.04), dark=0.05)

def grabando(t, D, fi):
    global _OF
    if _OF is None: _OF = oficina_bg()
    zp = ease(t / D)
    F = Frame(_OF, dict(x=540, y=lerp(820, 760, zp), z=lerp(1.0, 1.15, zp), sx=noise(t * 20) * 8, sy=noise(t * 20, 1) * 8))
    F.rect(60, 420, 360, 1300, fill=(30, 34, 42)); F.rect(720, 420, 1020, 1300, fill=(30, 34, 42))
    poss = noise(t * 4, 9) > 0.55
    big(DOCTOR, 4.4, F, add(pose(a1u=30, a1l=110, a2u=-25, a2l=-100), jitter(t, 6, 2)), 540, 1960, f=1,
        face="possessed" if poss else "talk", t=t)
    img = F.finish()
    img = post(img, fi, grain=16, glitch=0.3 if poss else 0.05, tint=((255, 0, 30), 0.2) if poss else None)
    d = ImageDraw.Draw(img)
    for (x, y, sx, sy) in ((80, 280, 1, 1), (1000, 280, -1, 1), (80, 1350, 1, -1), (1000, 1350, -1, -1)):
        d.line([(x, y + sy * 90), (x, y), (x + sx * 90, y)], fill=(255, 255, 255), width=8)
    if (t * 2) % 1 < 0.6: d.ellipse((760, 315, 800, 355), fill=(255, 30, 30))
    d.text((820, 335), tr("REC"), font=font(56), fill=(255, 255, 255), anchor="lm", stroke_width=4, stroke_fill=(0, 0, 0))
    d.text((110, 420), f"00:00:{int(t) + 3:02d}", font=font(44), fill=(255, 255, 255), anchor="lm", stroke_width=4, stroke_fill=(0, 0, 0))
    return img, dict(grain=0)

def sala(t, D, fi):
    kz = ease(seg(t, D * 0.72, D * 0.95))
    F = Frame(gradient((60, 80, 86), (34, 44, 50)), dict(x=lerp(600, 860, kz), y=lerp(1020, 1220, kz), z=lerp(1.15, 2.2, kz)))
    F.rect(-400, 1300, 1500, 2600, fill=(40, 50, 54)); F.line([(-400, 1300), (1500, 1300)], (80, 96, 100), 6)
    F.rect(-400, 1040, 1500, 1060, fill=(70, 90, 96))
    F.rect(540, 680, 860, 1300, fill=(80, 90, 96))   # marco
    F.rect(560, 700, 840, 1300, fill=(4, 4, 6))       # interior
    walk_t = seg(t, 0, D * 0.42)
    poss = noise(t * 4, 2) > 0.3
    if t < D * 0.62:
        x = lerp(80, 700, ease(walk_t))
        DOCTOR.draw(F, add(walk(t, 0.9) if walk_t < 1 else STAND, jitter(t, 4, 1)), x, 1300, f=1, face="possessed" if poss else "scared", t=t)
    cl = ease_back(seg(t, D * 0.45, D * 0.6))
    w = lerp(40, 280, cl)
    F.poly([(840 - w, 700 - 30 * (1 - cl)), (840, 700), (840, 1300), (840 - w, 1300 + 30 * (1 - cl))], fill=(150, 160, 164), outline=(90, 100, 104), w=6)
    if cl > 0.6:
        radiacion(F, (700, 960), 70)
        F.rect(650, 760, 750, 830, fill=(30, 40, 50), outline=(110, 120, 124), w=5)
    F.rect(560, 590, 840, 660, fill=(200, 30, 40)); F.text((700, 625), tr("RAYOS X"), 44, (255, 255, 255))
    k = ease_out(seg(t, D * 0.7, D * 0.85))
    if k > 0:
        kx = lerp(760, 960, k)
        F.circle((kx, 1288), 13, outline=GOLD, w=6); F.line([(kx + 12, 1288), (kx + 50, 1288)], GOLD, 6)
        F.line([(kx + 40, 1288), (kx + 40, 1298)], GOLD, 5); F.line([(kx + 50, 1288), (kx + 50, 1298)], GOLD, 5)
    shk = 18 * math.exp(-(t - D * 0.6) * 10) if t > D * 0.6 else 0
    F.sx = noise(t * 40) * shk
    return F.finish(), dict(dark=0.1, glitch=0.2 if shk > 6 else 0)

def cinta(t, D, fi):
    kz = ease(seg(t, D * 0.55, D * 0.95))
    F = Frame(base("alba"), dict(x=lerp(560, 540, kz), y=lerp(1040, 1275, kz), z=lerp(1.1, 3.2, kz)))
    F.rect(-400, 300, 1500, 1300, fill=(120, 112, 108))
    for k in range(10): F.line([(-400, 360 + k * 100), (1500, 360 + k * 100)], (108, 100, 96), 4)
    F.rect(380, 640, 700, 1300, fill=(96, 60, 36), outline=(60, 36, 20), w=10)
    F.rect(410, 680, 670, 940, outline=(70, 44, 26), w=6); F.rect(410, 980, 670, 1240, outline=(70, 44, 26), w=6)
    F.circle((640, 980), 12, fill=GOLD)
    F.rect(-400, 1300, 1500, 2600, fill=(70, 70, 74))
    F.ellipse((540, 1305), 230, 26, fill=(110, 40, 40))
    F.rect(460, 1250, 620, 1300, fill=(14, 14, 16), outline=(50, 50, 56), w=3)
    F.rect(475, 1256, 605, 1274, fill=(240, 236, 220))
    F.text((540, 1265), tr("PARA LEO Y NORA"), 9, (180, 20, 30))
    for cx in (505, 575): F.circle((cx, 1286), 8, fill=(220, 220, 220)); F.circle((cx, 1286), 3, fill=(14, 14, 16))
    wk = ease(seg(t, 0, D * 0.45))
    LEO.draw(F, walk(t) if wk < 1 else mix(STAND, pose(body=25, head=20, a1u=40, a2u=30), ease(seg(t, D * 0.45, D * 0.6))),
             lerp(1050, 780, wk), 1300, f=-1, face="neutral" if wk < 1 else "scared")
    return F.finish(), dict(grain=6)

def tele(t, D, fi):
    F = Frame(base("cuarto"), dict(x=560, y=1040, z=1.12))
    salon(F)
    on = t > D * 0.4
    tele_draw(F, glow=1.0, col=(200, 200, 200) if not on else (160, 190, 230))
    sofa(F)
    NORA.draw(F, SIT, 760, 1300, f=-1, face="neutral" if not on else "scared")
    LEO.draw(F, SIT, 930, 1300, f=-1, face="neutral" if not on else "scared")
    sofa(F, front=True)
    img = F.finish()
    feed = feed_estatico(fi) if not on else feed_doctor(t, fi, talk=False)
    pegar(img, F, TV, feed)
    return img, dict(flash=((255, 255, 255), 0.4 * (1 - seg(t, D * 0.4, D * 0.5)) * on))

def _tele_cerca(t, D, fi, z0, z1, feed, cy=910, shake=0.0):
    zp = ease(t / D)
    F = Frame(base("cuarto"), dict(x=270, y=cy, z=lerp(z0, z1, zp), sx=noise(t * 40) * shake, sy=noise(t * 40, 5) * shake))
    salon(F); tele_draw(F)
    img = F.finish()
    return pegar(img, F, TV, feed)

def mensaje(t, D, fi):
    return _tele_cerca(t, D, fi, 3.3, 3.7, feed_doctor(t, fi, talk=True), shake=2), dict(dark=0.05)

def brigida(t, D, fi):
    zp = ease(t / D)
    F = Frame(base("ciudad"), dict(x=540, y=lerp(1000, 940, zp), z=lerp(0.95, 1.12, zp)))
    F.circle((860, 380), 70, fill=(220, 224, 236)); F.circle((890, 360), 64, fill=(8, 11, 30))
    F.rect(-400, 1350, 1500, 2600, fill=(8, 10, 16))
    F.rect(140, 640, 940, 1350, fill=(36, 40, 54), outline=(20, 22, 30), w=6)
    F.poly([(100, 650), (980, 650), (540, 470)], fill=(26, 28, 40))
    F.rect(525, 330, 555, 450, fill=(150, 40, 46)); F.rect(490, 365, 590, 395, fill=(150, 40, 46))
    for r_ in range(4):
        for c_ in range(6):
            x = 190 + c_ * 125; y = 700 + r_ * 130
            if r_ == 3 and 2 <= c_ <= 3: continue
            lit = (r_, c_) == (1, 4) and noise(t * 7, 1) > -0.2
            F.rect(x, y, x + 70, y + 90, fill=(240, 200, 90) if lit else (14, 16, 24))
            if (r_ + c_ * 2) % 5 == 0:
                F.poly([(x, y), (x + 40, y + 30), (x + 18, y + 55), (x + 70, y + 90), (x, y + 90)], fill=(46, 50, 66))
    F.rect(470, 1180, 610, 1350, fill=(4, 4, 8))
    F.rect(330, 1100, 750, 1160, fill=(200, 196, 180), outline=(60, 56, 50), w=4)
    F.text((540, 1131), tr("SANTA BRÍGIDA"), 40, (60, 30, 30))
    for k in range(-4, 30): F.line([(k * 50, 1250), (k * 50, 1400)], (20, 22, 30), 7)
    F.line([(-400, 1270), (1500, 1270)], (20, 22, 30), 6)
    rr = random.Random(int(t * 30))
    for _ in range(40):
        x = rr.uniform(-100, 1180); y = rr.uniform(0, 1900); F.line([(x, y), (x - 8, y + 40)], (90, 100, 140), 2)
    fl = math.exp(-abs(t - D * 0.3) * 12) + 0.6 * math.exp(-abs(t - D * 0.38) * 14)
    return F.finish(), dict(flash=((220, 230, 255), 0.7 * fl), grain=9)

def habitacion(t, D, fi):
    zp = ease(t / D)
    F = Frame(gradient((40, 52, 44), (16, 20, 18)), dict(x=540, y=lerp(1000, 960, zp), z=lerp(1.1, 1.4, zp)))
    F.rect(-400, 1350, 1500, 2600, fill=(20, 22, 20)); F.line([(-400, 1350), (1500, 1350)], (56, 64, 56), 6)
    for k in range(-2, 9): F.line([(k * 160, 300), (k * 160 + 30, 1350)], (34, 44, 38), 3)
    F.rect(380, 680, 700, 1350, fill=(60, 66, 58))
    F.rect(400, 700, 680, 1350, fill=(2, 2, 3))
    ey = ease_out(seg(t, D * 0.55, D * 0.85))
    if ey > 0: cara_sonriente(F, (560, 960), 70 * ey)
    op = ease(seg(t, D * 0.15, D * 0.6))
    w = lerp(280, 50, op)
    F.poly([(400, 700), (400 + w, 700 - 40 * op), (400 + w, 1350 + 40 * op), (400, 1350)], fill=(150, 150, 136), outline=(80, 80, 70), w=5)
    F.rect(470, 600, 610, 660, fill=(200, 196, 170), outline=(60, 56, 50), w=4)
    F.text((540, 631), "114", 46, (30, 26, 24))
    img = F.finish()
    d = ImageDraw.Draw(img)
    d.text((1000, 1340), "1986", font=font(64), fill=(255, 255, 255), anchor="rm", stroke_width=5, stroke_fill=(0, 0, 0))
    luz = 0.35 if noise(t * 8, 3) < -0.3 else 0.0
    return img, dict(dark=luz, grain=14, glitch=0.3 if ey > 0 and fi % 5 == 0 else 0, tint=((255, 0, 30), 0.15 * ey))

def numero(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    F.rect(-400, 1300, 1500, 2600, fill=(12, 12, 18))
    fa = ease_out(seg(t, D * 0.35, D * 0.6))
    faro_draw(F, 800, 1300, h=600, lit=fa)
    pt = ease(seg(t, D * 0.25, D * 0.45))
    big(NORA, 1.9, F, mix(pose(a1u=30, a1l=120, head=10), pose(a1u=95, a1l=-5, head=-6), pt), 300, 1300, f=1,
        face="scared" if pt < 0.5 else "angry")
    img = F.finish(); d = ImageDraw.Draw(img)
    s = ease_back(seg(t, 0.05, 0.3)) * (1 + 0.05 * math.sin(t * 10))
    if s > 0:
        d.text((540, 420), "114", font=font(260 * s), fill=YEL, anchor="mm", stroke_width=int(16 * s), stroke_fill=(0, 0, 0))
    if fa > 0:
        d.text((800, 1000), "114", font=font(54 * fa), fill=(255, 255, 255), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    return img, dict(flash=((255, 214, 0), 0.35 * (1 - seg(t, 0.05, 0.3))))

def fallo(t, D, fi):
    g = 0.25 + 0.5 * ease(t / D)
    feed = feed_doctor(t, fi, poss=1.0 if noise(t * 6, 7) > 0.2 else 0.0, gl=g, roll=(t * 900) if noise(t * 2, 3) > 0.3 else 0)
    return _tele_cerca(t, D, fi, 3.5, 3.9, feed, shake=4), dict(glitch=0.15 + 0.25 * (fi % 4 == 0))

def ojos(t, D, fi):
    zp = ease(t / D)
    feed = feed_doctor(t, fi, poss=1.0, talk=False, z=lerp(1.0, 1.5, zp))
    return _tele_cerca(t, D, fi, 3.9, 4.6, feed, cy=900, shake=3), dict(tint=((255, 0, 30), 0.12), glitch=0.2 if fi % 6 == 0 else 0)

def apagar(t, D, fi):
    F = Frame(base("cuarto"), dict(x=380, y=1060, z=1.45))
    salon(F); tele_draw(F, glow=1.0, col=(255, 80, 80))
    ph = (t * 2.2) % 1
    press = 1 if ph < 0.35 and t < D * 0.75 else 0
    back = ease(seg(t, D * 0.75, D * 0.95))
    x = lerp(500, 600, back)
    LEO.draw(F, mix(pose(a1u=88, a1l=0, body=8 * press), SCARED, back), x - 18 * press, 1300, f=-1, face="angry" if back < 0.5 else "scared")
    img = F.finish()
    pegar(img, F, TV, feed_doctor(t, fi, poss=1.0, talk=False))
    return img, dict(glitch=0.25 if press and fi % 2 == 0 else 0, tint=((255, 0, 30), 0.08))

def cable(t, D, fi):
    kz = ease(seg(t, D * 0.45, D * 0.9))
    F = Frame(base("cuarto"), dict(x=lerp(520, 660, kz), y=lerp(1060, 1000, kz), z=lerp(1.25, 1.9, kz)))
    salon(F); tele_draw(F, glow=1.0, col=(255, 80, 80))
    F.rect(960, 1180, 1010, 1240, fill=(220, 220, 214), outline=(120, 120, 110), w=3)
    for dy in (1200, 1220): F.circle((985, dy), 5, fill=(30, 30, 30))
    up = ease_back(seg(t, D * 0.2, D * 0.45))
    J = NORA.draw(F, mix(pose(a1u=40, a1l=10), pose(a1u=130, a1l=-20, head=-6), up), 760, 1300, f=-1, face="scared")
    LEO.draw(F, SCARED if up > 0.5 else STAND, 560, 1300, f=-1, face="scared")
    hx, hy = J["a1h"]
    F.line([(380, 1100), (430, 1300), (700, 1302), (hx, hy + 30), (hx, hy)], (30, 30, 34), 6)
    F.rect(hx - 16, hy - 26, hx + 16, hy + 6, fill=(240, 240, 236), outline=(90, 90, 90), w=3)
    for dx in (-8, 8): F.line([(hx + dx, hy - 26), (hx + dx, hy - 46)], (200, 200, 200), 4)
    img = F.finish()
    pegar(img, F, TV, feed_doctor(t, fi, poss=1.0, talk=False))
    return img, dict(tint=((255, 0, 30), 0.1 * up), glitch=0.2 if up > 0.8 and fi % 5 == 0 else 0)

def voz(t, D, fi):
    cz = ease_out(seg(t, D * 0.3, D * 0.75))
    feed = feed_doctor(t, fi, poss=1.0, talk=False, cara=cz, gl=0.2 + 0.5 * (cz < 0.3 and t > D * 0.15))
    zz = ease(seg(t, D * 0.3, D))
    return _tele_cerca(t, D, fi, 3.4 + 1.6 * zz, 3.4 + 1.6 * zz, feed, cy=910, shake=4 + 10 * cz), \
        dict(tint=((255, 0, 30), 0.2 * cz), glitch=0.4 if fi % 4 == 0 else 0.1, flash=((255, 0, 30), 0.4 * (1 - seg(t, D * 0.3, D * 0.45)) * (t > D * 0.3)))

def final(t, D, fi):
    on = noise(t * 5, 3) > -0.4
    F = Frame(base("oscuro"), dict(x=270, y=760, z=2.6))
    F.rect(-400, 1300, 1500, 2600, fill=(8, 8, 12))
    tele_draw(F)
    img = F.finish()
    pegar(img, F, TV, feed_doctor(t, fi, cara=1.0 if on else 0.0, poss=1.0, talk=False, gl=0 if on else 0.5) if on or fi % 2 else feed_estatico(fi))
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.05, 0.4))
    if p > 0: d.text((540, 460), tr("PARTE 5"), font=font(190 * p), fill=YEL, anchor="mm", stroke_width=int(14 * p), stroke_fill=(0, 0, 0))
    q = ease_back(seg(t, 1.2, 1.5)) * (1 + 0.06 * math.sin(t * 9))
    if q > 0:
        d.rounded_rectangle((210, 640, 870, 780), 30, fill=ROJO)
        d.text((540, 710), tr("SÍGUEME →"), font=font(84 * min(q, 1.06)), fill=(255, 255, 255), anchor="mm")
    return img, dict(glitch=0.3 if not on else 0.0, tint=((255, 0, 30), 0.12))

ESCENA_FN = dict(camara=camara, grabando=grabando, sala=sala, cinta=cinta, tele=tele, mensaje=mensaje, brigida=brigida, habitacion=habitacion,
                 numero=numero, fallo=fallo, ojos=ojos, apagar=apagar, cable=cable, voz=voz, final=final)
PAUSA = dict(camara=0.8, grabando=0.7, sala=0.9, cinta=0.8, tele=0.8, mensaje=0.8, brigida=0.9, habitacion=1.0, numero=0.9, fallo=0.7,
             ojos=0.8, apagar=0.8, cable=1.0, voz=1.5, final=2.2)
