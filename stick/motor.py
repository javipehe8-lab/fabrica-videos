"""Motor de animación stickman: cámara, figuras con esqueleto, primitivas y efectos. Lienzo vertical 1080x1920."""
import math, random, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, S, FPS = 1080, 1920, 2, 30
CALIDAD_HD = os.environ.get("CALIDAD", "hd") == "hd"   # contorno, sombras, brillo y bloom
FONT_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
_fonts = {}
def font(size, path=FONT_BLACK):
    k = (path, int(size))
    if k not in _fonts: _fonts[k] = ImageFont.truetype(path, max(int(size), 4))
    return _fonts[k]

# ---------- utilidades de tiempo ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def seg(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_back(x):
    x = clamp(x); c = 1.9; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def lerp(a, b, x): return a + (b - a) * x
def noise(t, seed=0):
    """ruido suave determinista 1D en [-1,1]"""
    i = math.floor(t); f = t - i
    def h(n): return random.Random(n * 7919 + seed * 104729).uniform(-1, 1)
    return lerp(h(i), h(i + 1), f * f * (3 - 2 * f))

# ---------- cámara y lienzo ----------
class Frame:
    def __init__(self, base, cam):
        self.img = base.copy()
        self.d = ImageDraw.Draw(self.img)
        self.cx, self.cy, self.z = cam.get("x", W / 2), cam.get("y", H / 2), cam.get("z", 1.0)
        self.sx, self.sy = cam.get("sx", 0), cam.get("sy", 0)
    def P(self, x, y):
        return (((x - self.cx) * self.z + W / 2 + self.sx) * S, ((y - self.cy) * self.z + H / 2 + self.sy) * S)
    def k(self, w): return max(1, w * self.z * S)
    # primitivas en coordenadas de mundo
    def line(self, pts, col, w, round_=True):
        P = [self.P(*p) for p in pts]; ww = self.k(w)
        self.d.line(P, fill=col, width=int(ww), joint="curve")
        if round_:
            for p in (P[0], P[-1]):
                r = ww / 2; self.d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col)
    def circle(self, c, r, fill=None, outline=None, w=0):
        x, y = self.P(*c); rr = r * self.z * S
        self.d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=fill, outline=outline, width=int(self.k(w)) if w else 0)
    def ellipse(self, c, rx, ry, fill=None, outline=None, w=0):
        x, y = self.P(*c); a, b = rx * self.z * S, ry * self.z * S
        self.d.ellipse([x - a, y - b, x + a, y + b], fill=fill, outline=outline, width=int(self.k(w)) if w else 0)
    def rect(self, x0, y0, x1, y1, fill=None, outline=None, w=0):
        a, b = self.P(x0, y0); c, d = self.P(x1, y1)
        self.d.rectangle([min(a, c), min(b, d), max(a, c), max(b, d)], fill=fill, outline=outline, width=int(self.k(w)) if w else 0)
    def poly(self, pts, fill=None, outline=None, w=0):
        self.d.polygon([self.P(*p) for p in pts], fill=fill, outline=outline, width=int(self.k(w)) if w else 0)
    def arc(self, c, r, a0, a1, col, w):
        x, y = self.P(*c); rr = r * self.z * S
        self.d.arc([x - rr, y - rr, x + rr, y + rr], a0, a1, fill=col, width=int(self.k(w)))
    def text(self, c, s, size, col, stroke=0, scol=(0, 0, 0)):
        f = font(size * self.z * S); x, y = self.P(*c)
        self.d.text((x, y), s, font=f, fill=col, anchor="mm", stroke_width=int(stroke * self.z * S), stroke_fill=scol)
    def finish(self):
        return self.img.reduce(S)

def gradient(top, bottom, w=W * S, h=H * S, mid=None):
    t = np.linspace(0, 1, h)[:, None, None]
    a, b = np.array(top, np.float32), np.array(bottom, np.float32)
    if mid is not None:
        m = np.array(mid, np.float32)
        g = np.where(t < 0.5, a + (m - a) * (t / 0.5), m + (b - m) * ((t - 0.5) / 0.5))
    else:
        g = a + (b - a) * t
    return Image.fromarray(np.broadcast_to(g, (h, w, 3)).astype(np.uint8))

# ---------- figuras stickman ----------
L = dict(torso=100, neck=10, head=33, ua=56, la=54, ul=66, ll=64)
STAND = dict(body=0, head=0, a1u=14, a1l=12, a2u=-14, a2l=12, l1u=7, l1l=-3, l2u=-7, l2l=-3)

def pose(**kw):
    p = dict(STAND); p.update(kw); return p
def mix(p, q, x):
    return {k: lerp(p.get(k, 0), q.get(k, 0), x) for k in set(p) | set(q)}

def walk(t, amp=1.0, speed=1.0):
    ph = t * 2 * math.pi * 1.6 * speed; s = math.sin(ph)
    return dict(body=3 * amp, head=-2, a1u=-28 * s * amp, a1l=18, a2u=28 * s * amp, a2l=18,
                l1u=30 * s * amp, l1l=-28 * amp * max(0, -math.cos(ph)) - 4, l2u=-30 * s * amp,
                l2l=-28 * amp * max(0, math.cos(ph)) - 4)
def run(t, speed=1.0):
    ph = t * 2 * math.pi * 2.6 * speed; s = math.sin(ph)
    return dict(body=18, head=-12, a1u=-55 * s, a1l=85, a2u=55 * s, a2l=85,
                l1u=48 * s + 8, l1l=-75 * max(0, -math.cos(ph)) - 15, l2u=-48 * s + 8, l2l=-75 * max(0, math.cos(ph)) - 15)
SCARED = pose(body=-8, head=6, a1u=150, a1l=40, a2u=140, a2l=45, l1u=14, l1l=-18, l2u=-12, l2l=-14)
POINT = pose(a1u=88, a1l=0, head=-4)
AIM = pose(body=6, head=-4, a1u=82, a1l=6, a2u=72, a2l=40, l1u=18, l1l=-6, l2u=-14, l2l=-4)
ARMS_UP = pose(a1u=170, a1l=8, a2u=-170, a2l=-8, head=-8)
CHEER = pose(a1u=160, a1l=-20, a2u=-160, a2l=20, head=-10, l1u=20, l1l=-40, l2u=-20, l2l=-40)
HOLD_UP = pose(body=-4, head=-10, a1u=135, a1l=10, a2u=120, a2l=30, l1u=16, l1l=-4, l2u=-14, l2l=-4)
TALK = pose(a1u=50, a1l=50, a2u=-10, a2l=20)
THINK = pose(a1u=30, a1l=140, head=-10)

class Fig:
    def __init__(self, shirt=(240, 240, 240), limb=(240, 240, 240), scale=1.0, kind="human", extra=()):
        self.shirt, self.limb, self.scale, self.kind, self.extra = shirt, limb, scale, kind, set(extra)

    def joints(self, p, x, y, f=1, rot=0.0, snap=True, stretch=1.0):
        sc = self.scale
        def v(a, l): r = math.radians(a); return (f * math.sin(r) * l * sc, math.cos(r) * l * sc)
        b = p.get("body", 0); h = p.get("head", 0)
        hip = (0.0, 0.0)
        rb = math.radians(b)
        neck = (f * math.sin(rb) * L["torso"] * sc * stretch, -math.cos(rb) * L["torso"] * sc * stretch)
        sh = (neck[0] * 0.9, neck[1] * 0.9)
        rh = math.radians(b + h); dd = (L["neck"] + L["head"]) * sc
        head = (neck[0] + f * math.sin(rh) * dd, neck[1] - math.cos(rh) * dd)
        J = dict(hip=hip, neck=neck, sh=sh, head=head)
        for a in ("a1", "a2"):
            e = v(p[a + "u"] + b, L["ua"] * stretch); J[a + "e"] = (sh[0] + e[0], sh[1] + e[1])
            hnd = v(p[a + "u"] + b + p[a + "l"], L["la"] * stretch); J[a + "h"] = (J[a + "e"][0] + hnd[0], J[a + "e"][1] + hnd[1])
        for l in ("l1", "l2"):
            k = v(p[l + "u"], L["ul"] * stretch); J[l + "k"] = k
            ft = v(p[l + "u"] + p[l + "l"], L["ll"] * stretch); J[l + "f"] = (k[0] + ft[0], k[1] + ft[1])
        if rot:
            c, s_ = math.cos(math.radians(rot)), math.sin(math.radians(rot))
            J = {n: (q[0] * c - q[1] * s_, q[0] * s_ + q[1] * c) for n, q in J.items()}
        if snap:
            low = max(q[1] for n, q in J.items() if n != "head") + 6 * sc
            low = max(low, J["head"][1] + L["head"] * sc)
            dy = y - low
        else:
            dy = y
        return {n: (q[0] + x, q[1] + dy) for n, q in J.items()}

    def draw(self, F, p, x, y, f=1, rot=0.0, snap=True, face="neutral", t=0.0, stretch=1.0):
        J = self.joints(p, x, y, f, rot, snap, stretch)
        sc = self.scale; w = 13 * sc
        enemy = self.kind == "enemy"
        out = (205, 190, 255); dark = (6, 6, 10)
        if CALIDAD_HD:
            feet = max(J["l1f"][1], J["l2f"][1])
            if snap and abs(rot) < 1:   # sombra de contacto en el suelo
                F.ellipse(((J["l1f"][0] + J["l2f"][0]) / 2, feet + 4 * sc), 46 * sc, 9 * sc, fill=(0, 0, 0))
            if not enemy:              # contorno oscuro de toda la silueta (look de dibujo animado)
                ow = w + 9 * sc; ink0 = (8, 8, 12)
                for seg_ in (["sh", "a2e", "a2h"], ["hip", "l2k", "l2f"], ["hip", "neck"], ["hip", "l1k", "l1f"], ["sh", "a1e", "a1h"]):
                    F.line([J[k] for k in seg_], ink0, ow)
                F.circle(J["head"], L["head"] * sc + 4.5 * sc, fill=ink0)
        def limb(pts, col, back=False):
            if enemy:
                F.line(pts, out, w + 9 * sc); F.line(pts, dark, w)
            else:
                c = tuple(int(v * (0.72 if back else 1)) for v in col)
                F.line(pts, c, w)
        limb([J["sh"], J["a2e"], J["a2h"]], self.limb, True)
        limb([J["hip"], J["l2k"], J["l2f"]], self.limb, True)
        if "coat" in self.extra:
            hx, hy = J["hip"]; nx, ny = J["sh"]
            F.poly([(nx - 26 * sc, ny + 6 * sc), (nx + 26 * sc, ny + 6 * sc), (hx + 40 * sc, hy + 36 * sc), (hx - 40 * sc, hy + 36 * sc)],
                   fill=(236, 240, 245), outline=(150, 160, 175), w=3 * sc)
        limb([J["hip"], J["neck"]], self.shirt)
        if "rifle" in self.extra:
            hx, hy = J["a1h"]; ex, ey = J["a2h"]
            dx, dy = hx - J["sh"][0], hy - J["sh"][1]; n = math.hypot(dx, dy) or 1
            F.line([(ex - dx / n * 30 * sc, ey - dy / n * 30 * sc), (hx + dx / n * 55 * sc, hy + dy / n * 55 * sc)], (40, 44, 40), 11 * sc)
        if "clipboard" in self.extra:
            hx, hy = J["a2h"]; F.rect(hx - 22 * sc, hy - 34 * sc, hx + 22 * sc, hy + 20 * sc, fill=(170, 120, 70))
            F.rect(hx - 17 * sc, hy - 27 * sc, hx + 17 * sc, hy + 15 * sc, fill=(250, 250, 250))
        if "mirror" in self.extra:
            mx = (J["a1h"][0] + J["a2h"][0]) / 2; my = (J["a1h"][1] + J["a2h"][1]) / 2 - 30 * sc
            F.ellipse((mx, my), 44 * sc, 60 * sc, fill=(212, 170, 80))
            F.ellipse((mx, my), 34 * sc, 50 * sc, fill=(175, 200, 222))
            F.line([(mx - 14 * sc, my - 30 * sc), (mx + 10 * sc, my - 6 * sc)], (240, 248, 255), 5 * sc)
        limb([J["hip"], J["l1k"], J["l1f"]], self.limb)
        limb([J["sh"], J["a1e"], J["a1h"]], self.limb)
        if "cane" in self.extra:   # bastón (abuela Carmen) en la mano trasera
            hx, hy = J["a2h"]; fy = max(J["l1f"][1], J["l2f"][1])
            F.line([(hx + f * 4 * sc, hy), (hx + f * 10 * sc, fy)], (96, 62, 34), 8 * sc)
            F.arc((hx + f * 18 * sc, hy + 2 * sc), 14 * sc, 180, 360, (96, 62, 34), 7 * sc)
        # cabeza
        hc = J["head"]; r = L["head"] * sc
        if enemy:
            F.circle(hc, r + 5 * sc, fill=out); F.circle(hc, r, fill=dark)
            ex = f * 8 * sc
            for dx in (-12, 12):
                F.circle((hc[0] + ex + dx * sc, hc[1] - 8 * sc), 6.5 * sc, fill=(255, 255, 255))
            F.arc((hc[0] + ex, hc[1] - 6 * sc), 22 * sc, 20, 160, (255, 255, 255), 6 * sc)
            for i in range(-3, 4):
                a = math.radians(90 - i * 17); cx, cy = hc[0] + ex + math.cos(a) * 22 * sc, hc[1] - 6 * sc + math.sin(a) * 22 * sc
                F.line([(cx, cy - 6 * sc), (cx, cy + 1 * sc)], (255, 255, 255), 2.5 * sc, round_=False)
            return J
        F.circle(hc, r, fill=self.limb)
        if CALIDAD_HD:
            F.circle((hc[0] - f * r * 0.35, hc[1] - r * 0.4), r * 0.28, fill=tuple(min(255, int(v * 1.12 + 20)) for v in self.limb))
        if "bun" in self.extra:    # pelo gris recogido en un moño
            gris = (196, 196, 204)
            F.d.chord([*F.P(hc[0] - r - 2 * sc, hc[1] - r - 3 * sc), *F.P(hc[0] + r + 2 * sc, hc[1] + r - 6 * sc)], 180, 360, fill=gris)
            F.circle((hc[0] - f * r * 0.62, hc[1] - r * 0.92), r * 0.46, fill=gris, outline=(150, 150, 160), w=2 * sc)
        if "helmet" in self.extra:
            F.d.chord([*F.P(hc[0] - r - 5 * sc, hc[1] - r - 6 * sc), *F.P(hc[0] + r + 5 * sc, hc[1] + r - 2 * sc)], 180, 360, fill=(84, 100, 58))
        if "ponytail" in self.extra:
            F.line([(hc[0] - f * r * 0.8, hc[1] - r * 0.5), (hc[0] - f * r * 1.5, hc[1] + r * 0.1), (hc[0] - f * r * 1.4, hc[1] + r * 0.9)], (170, 100, 255), 11 * sc)
            F.line([(hc[0] - f * r, hc[1] - r * 0.85), (hc[0] + f * r * 0.4, hc[1] - r * 1.05)], (170, 100, 255), 9 * sc)
        if "cap" in self.extra:
            F.d.chord([*F.P(hc[0] - r - 2 * sc, hc[1] - r - 4 * sc), *F.P(hc[0] + r + 2 * sc, hc[1] + r - 8 * sc)], 180, 360, fill=(230, 60, 60))
            F.line([(hc[0], hc[1] - r * 0.35), (hc[0] + f * r * 1.5, hc[1] - r * 0.35)], (230, 60, 60), 8 * sc)
        # cara
        ex = f * 9 * sc; ink = (20, 22, 30)
        if face == "closed":
            for dx in (-9, 11):
                F.line([(hc[0] + ex + dx * sc - 5 * sc, hc[1] - 4 * sc), (hc[0] + ex + dx * sc + 5 * sc, hc[1] - 4 * sc)], ink, 3.5 * sc)
        elif face == "possessed":
            for dx in (-9, 11):
                F.circle((hc[0] + ex + dx * sc, hc[1] - 5 * sc), 6 * sc, fill=(255, 40, 40))
            F.arc((hc[0] + ex, hc[1] - 2 * sc), 15 * sc, 25, 155, ink, 4 * sc)
        else:
            er = 6.5 * sc if face == "scared" else 4.5 * sc
            for dx in (-9, 11):
                F.circle((hc[0] + ex + dx * sc, hc[1] - 5 * sc), er, fill=ink)
                if face == "scared": F.circle((hc[0] + ex + dx * sc + 1.5 * sc, hc[1] - 6.5 * sc), 2 * sc, fill=(255, 255, 255))
        if face == "scared":
            F.ellipse((hc[0] + ex, hc[1] + 14 * sc), 7 * sc, 9 * sc, fill=ink)
        elif face == "happy":
            F.arc((hc[0] + ex, hc[1] + 2 * sc), 13 * sc, 25, 155, ink, 4 * sc)
        elif face == "angry":
            for dx, s_ in ((-9, 1), (11, -1)):
                F.line([(hc[0] + ex + dx * sc - 7 * sc, hc[1] - 14 * sc - s_ * 3 * sc), (hc[0] + ex + dx * sc + 7 * sc, hc[1] - 14 * sc + s_ * 3 * sc)], ink, 3.5 * sc)
            F.line([(hc[0] + ex - 7 * sc, hc[1] + 13 * sc), (hc[0] + ex + 7 * sc, hc[1] + 13 * sc)], ink, 3.5 * sc)
        elif face == "talk":
            o = abs(math.sin(t * 22)) * 6 * sc + 2 * sc
            F.ellipse((hc[0] + ex, hc[1] + 13 * sc), 7 * sc, o, fill=ink)
        elif face == "neutral":
            F.line([(hc[0] + ex - 6 * sc, hc[1] + 13 * sc), (hc[0] + ex + 6 * sc, hc[1] + 13 * sc)], ink, 3.5 * sc)
        return J

LEO = Fig(shirt=(235, 60, 60), extra=("cap",))
NORA = Fig(shirt=(160, 90, 255), extra=("ponytail",))
SOLDADO = Fig(shirt=(96, 115, 66), limb=(225, 228, 220), scale=0.85, extra=("helmet", "rifle"))
DOCTOR = Fig(shirt=(236, 240, 245), extra=("coat", "clipboard"))
PACIENTE = Fig(shirt=(150, 190, 220), limb=(225, 225, 230), scale=0.8)
SONRIENTE = Fig(scale=1.45, kind="enemy")
CARMEN = Fig(shirt=(96, 112, 104), limb=(230, 224, 216), scale=0.92, extra=("bun", "cane"))

def jitter(t, amt, seed=0):
    keys = ("body", "head", "a1u", "a1l", "a2u", "a2l", "l1u", "l2u")
    return {k: amt * noise(t * 9, seed + i) for i, k in enumerate(keys)}
def add(p, q): return {k: p.get(k, 0) + q.get(k, 0) for k in set(p) | set(q)}

# ---------- efectos (sobre imagen final 1x) ----------
_rng = np.random.default_rng(3)
GRAIN = [(_rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)) for _ in range(6)]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIG = (1 - 0.55 * np.clip(np.hypot((xx - W / 2) / (W * 0.75), (yy - H / 2) / (H * 0.62)), 0, 1.4) ** 2.2)[..., None].astype(np.float32)
VIG = np.clip(VIG, 0.25, 1)

def post(img, fi, flash=None, glitch=0.0, dark=0.0, grain=7.0, tint=None):
    a = np.asarray(img, np.float32)
    if dark: a *= (1 - dark)
    if tint is not None: a = a * (1 - tint[1]) + np.array(tint[0], np.float32) * tint[1] * (a / 255 * 0.6 + 0.4)
    a *= VIG
    if CALIDAD_HD:
        a = 128 + (a - 128) * 1.08                       # algo más de contraste
        small = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((W // 4, H // 4), Image.BILINEAR)
        s = np.asarray(small, np.float32); s = np.clip(s - 170, 0, 255) * 1.6
        bl = Image.fromarray(np.clip(s, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BILINEAR)
        a += np.asarray(bl, np.float32) * 0.55           # resplandor (bloom) en luces y destellos
    g = np.kron(GRAIN[fi % len(GRAIN)], np.ones((2, 2), np.float32))[:H, :W, None]
    a += g * grain
    if flash is not None and flash[1] > 0:
        a = a * (1 - flash[1]) + np.array(flash[0], np.float32) * flash[1]
    if glitch > 0:
        r = random.Random(fi)
        for _ in range(int(3 + glitch * 10)):
            y0 = r.randint(0, H - 40); hh = r.randint(8, int(30 + 140 * glitch)); sh = int(r.uniform(-1, 1) * 90 * glitch)
            a[y0:y0 + hh] = np.roll(a[y0:y0 + hh], sh, axis=1)
        o = int(14 * glitch) + 1
        a[..., 0] = np.roll(a[..., 0], o, axis=1); a[..., 2] = np.roll(a[..., 2], -o, axis=1)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

# ---------- subtítulos estilo "dopamina" ----------
def captions(img, words, t, y=1540):
    """words: lista de (inicio, fin, palabra). Muestra grupos de hasta 3 palabras con la activa resaltada."""
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w[2].endswith((".", "?", "!", "…", ",", ":")):
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    g = next((g for g in groups if g[0][0] <= t < g[-1][1] + 0.12), None)
    if not g: return img
    d = ImageDraw.Draw(img)
    pop = ease_back(seg(t, g[0][0], g[0][0] + 0.16))
    size = 96 * (0.8 + 0.2 * pop)
    f = font(size)
    clean = [w[2].strip(",.…:;").upper() for w in g]
    widths = [d.textlength(c, font=f) for c in clean]; gap = size * 0.28
    total = sum(widths) + gap * (len(clean) - 1)
    lines = [list(range(len(clean)))]
    if total > W - 120 and len(clean) > 1:
        lines = [list(range(len(clean) - 1)), [len(clean) - 1]]
    quien_g = g[0][3] if len(g[0]) > 3 else "NARRADOR"
    if quien_g != "NARRADOR":   # etiqueta con el nombre de quien habla
        NOMBRES = {"SONRIENTE": tr("EL SONRIENTE") if IDIOMA != "en" else "THE GRINNER"}
        nom = NOMBRES.get(quien_g, quien_g)
        colt = {"NORA": (170, 100, 255), "LEO": (230, 50, 50), "SONRIENTE": (200, 20, 30)}.get(quien_g, (40, 140, 230))
        fn = font(48); tw = d.textlength(nom, font=fn)
        ty = y - size * (1.1 if len(lines) > 1 else 0.6) - 70
        d.rounded_rectangle((W / 2 - tw / 2 - 26, ty - 34, W / 2 + tw / 2 + 26, ty + 34), 18, fill=colt, outline=(0, 0, 0), width=5)
        d.text((W / 2, ty), nom, font=fn, fill=(255, 255, 255), anchor="mm")
    for li, idxs in enumerate(lines):
        tw = sum(widths[i] for i in idxs) + gap * (len(idxs) - 1)
        x = (W - tw) / 2; yy_ = y + li * size * 1.08 - (len(lines) - 1) * size * 0.54
        for i in idxs:
            active = g[i][0] <= t < g[i][1] + 0.05
            quien = g[i][3] if len(g[i]) > 3 else "NARRADOR"
            col = (255, 214, 0) if active else (255, 255, 255)
            if quien == "NORA": col = (225, 190, 255) if not active else (200, 130, 255)
            elif quien == "LEO": col = (255, 200, 200) if not active else (255, 90, 90)
            elif quien == "SONRIENTE": col = (255, 40, 50)
            elif quien != "NARRADOR": col = (170, 230, 255) if not active else (90, 200, 255)
            d.text((x, yy_), clean[i], font=f, fill=col, anchor="lm", stroke_width=int(size * 0.11), stroke_fill=(0, 0, 0))
            x += widths[i] + gap
    return img


# ---------- idioma ----------
IDIOMA = os.environ.get("IDIOMA", "es")
EN = {"PARTE": "PART", "SÍGUEME →": "FOLLOW →", "¡BUM!": "BOOM!", "¡ATASCADA!": "STUCK!", "¡UNO!": "ONE!", "¡DOS!": "TWO!",
      "¡TRES!": "THREE!", "ZONA": "KEEP", "CERRADA": "OUT",
      "REC": "REC", "RAYOS X": "X-RAY", "PARA LEO Y NORA": "FOR LEO & NORA", "SANTA BRÍGIDA": "SAINT BRIGID",
      "COMENTA A O B": "COMMENT A OR B", "TÚ DECIDES": "YOU DECIDE",
      "3ª PLANTA": "3RD FLOOR", "SILENCIO": "QUIET", "URGENTE": "URGENT",
      "ARCHIVO": "RECORDS", "PACIENTE": "PATIENT", "HAB.": "ROOM", "NOMBRE:": "NAME:"}
def tr(s):
    """traduce textos fijos de pantalla al idioma activo"""
    if IDIOMA != "en": return s
    if s.startswith("PARTE "): return "PART " + s[6:]
    return EN.get(s, s)
