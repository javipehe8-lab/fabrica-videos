"""Foto de perfil + portadas de la Parte 1 y 2."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter
from motor import *
from escenas import base, cuarto, GLASS
import escenas2 as e2

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
YEL, RED, WHITE = (255, 214, 0), (230, 30, 50), (255, 255, 255)

def glow_text(img, xy, s, size, fill, stroke=None, anchor="mm"):
    d = ImageDraw.Draw(img); f = font(size); sw = stroke if stroke is not None else int(size * 0.1)
    d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=(0, 0, 0))

def badge(img, text, y=150):
    d = ImageDraw.Draw(img); f = font(64); w = d.textlength(text, font=f)
    d.rounded_rectangle((70, y, 70 + w + 64, y + 100), 22, fill=RED)
    d.text((70 + 32, y + 50), text, font=f, fill=WHITE, anchor="lm")

def finish(img, tint=None):
    return post(img, 0, tint=tint, grain=5)

# ---------- foto de perfil (cuadrada, segura en círculo) ----------
F = Frame(gradient((40, 16, 60), (8, 6, 14), w=1080 * S, h=1920 * S), dict(x=540, y=700, z=1.0))
F.circle((540, 700), 470, fill=(20, 10, 32))
hc = (540, 700); r = 330; out = (205, 190, 255)
F.circle(hc, r + 26, fill=out); F.circle(hc, r, fill=(6, 6, 10))
for dx in (-120, 120): F.circle((540 + dx, 610), 62, fill=WHITE)
F.arc((540, 640), 215, 20, 160, WHITE, 46)
for i in range(-3, 4):
    a = math.radians(90 - i * 17); cx, cy = 540 + math.cos(a) * 215, 640 + math.sin(a) * 215
    F.line([(cx, cy - 50), (cx, cy + 6)], WHITE, 18, round_=False)
av = F.finish().crop((540 - 520, 960 - 520, 540 + 520, 960 + 520))
av = post_sq = av
av = av.resize((800, 800), Image.LANCZOS)
av.save(os.path.join(OUT, "foto_perfil.png"))

# ---------- portada Parte 1 ----------
F = Frame(base("cuarto"), dict(x=470, y=900, z=1.75))
cuarto(F, t=0.3, enemigo=1.0)
LEO.draw(F, pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=40, a1l=30, a2u=-20), 290, 1150, f=1, snap=False, face="scared")
img = finish(F.finish(), tint=((255, 30, 40), 0.12))
badge(img, "PARTE 1")
glow_text(img, (540, 1610), "NO LO MIRES", 150, WHITE)
glow_text(img, (540, 1780), "A LOS OJOS", 150, YEL)
img.save(os.path.join(OUT, "portada_parte1.png"))

# ---------- portada Parte 2 ----------
F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
for k in range(30):
    import random; r = random.Random(k); F.circle((r.uniform(0, 1080), r.uniform(0, 900)), 2.5, fill=(200, 205, 230))
e2.acantilado(F, 520, 1000, col=(14, 16, 26))
e2.faro_draw(F, 820, 1000, h=520, lit=1.0, beam_ang=195, cara=1.0, t=0.4)
e2.big(NORA, 3.0, F, pose(a1u=12, a2u=-12), 320, 1980, f=1, face="possessed")
img = finish(F.finish(), tint=((255, 0, 30), 0.16))
badge(img, "PARTE 2")
glow_text(img, (540, 1610), "ESTÁ DENTRO", 150, WHITE)
glow_text(img, (540, 1780), "DE NORA", 150, YEL)
img.save(os.path.join(OUT, "portada_parte2.png"))
print("ok")
