"""Escenas del episodio 17 (temporada 2, "La trampa"): Nora hace de cebo delante del primer espejo de la casa de la risa
con el resto de espejos tapados; al amanecer el Asomado llega y hace muecas para que sonría; ella aguanta… hasta que le
enseña a Tomás, el niño que ella salvó, feliz. Nora sonríe y unos dedos larguísimos salen del cristal."""
import math, random
from functools import lru_cache
from motor import *
from escenas import base, GLASS
from escenas6 import NINA, coletas
from escenas7 import NINO
from escenas12 import asomado
from escenas13 import huella, asomado_en, PISO, VERDE
from escenas15 import sabana, iluminar_, GOLD_
from escenas16 import fondo, espejo, marco_espejo, reflejo, FIGS, EX, EY, EW, EH

PALIDO = (206, 232, 210)
ALBA = (255, 150, 110)

def suelo(F):
    F.rect(-800, PISO, 2000, 2700, fill=(24, 10, 24)); F.line([(-800, PISO), (2000, PISO)], (80, 34, 64), 6)

def primer_espejo(F, t, luz=0.5, fog=0.0):
    espejo(F, EX, EY, EW, EH, brillo=0.5, luz=luz)
    if fog > 0:                                                                 # el cristal se empaña
        col = tuple(int(lerp(a, b, fog * 0.75)) for a, b in zip((50, 90, 74), (200, 214, 206)))
        for i in range(6):
            yy = EY + EH * (1 - (i + 1) / 6 * fog)
            F.rect(EX, max(EY, yy), EX + EW, EY + EH, fill=tuple(int(lerp(c, 60, 0.12 * i)) for c in col))

def marco_primero(F, t):
    marco_espejo(F, EX, EY, EW, EH, bombillas=1.0, t=t)
    for i in range(5): F.line([(EX - 30 + i * 6, EY - 40 - i * 10), (EX + EW + 30 - i * 6, EY - 40 - i * 10)], GOLD_, 4)

def ventanuco(F, x, y, k):
    """ventanuco alto de la casa de la risa: el cielo se va poniendo rojo (amanecer)"""
    col = tuple(int(lerp(a, b, k)) for a, b in zip((20, 22, 46), ALBA))
    F.rect(x, y, x + 160, y + 120, fill=col, outline=(60, 30, 50), w=10)
    F.line([(x + 80, y), (x + 80, y + 120)], (60, 30, 50), 6)

def barra(F, J, f=1):
    hx, hy = J["a1h"]
    F.line([(hx - f * 30, hy + 40), (hx + f * 40, hy - 160)], (150, 150, 160), 12)

def dedos_fuera(F, k, t, nx):
    """manos de dedos larguísimos que salen del cristal hacia Nora"""
    for j, yy in enumerate((EY + 380, EY + 520)):
        px = lerp(EX + EW - 40, nx - 120, ease(k)) ; py = yy + 20 * math.sin(t * 4 + j)
        F.line([(EX + EW - 60, yy), (px, py)], PALIDO, 14)
        F.ellipse((px, py), 26, 32, fill=PALIDO)
        for q in range(4):
            a = math.radians(-40 + q * 26 + 8 * math.sin(t * 6 + q))
            ln = 150 + 30 * (q in (1, 2))
            mx, my = px + math.cos(a) * ln * 0.55, py + math.sin(a) * ln * 0.55
            ex, ey = px + math.cos(a * 1.2) * ln, py + math.sin(a * 1.2) * ln
            F.line([(px, py), (mx, my), (ex, ey)], PALIDO, 8)
            F.circle((ex, ey), 7, fill=(236, 248, 238))

# ---------- escenas ----------
def cebo(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(560, 600, zp), y=lerp(900, 860, zp), z=lerp(1.0, 1.25, zp), sx=noise(t * 25) * 3, sy=noise(t * 25, 1) * 3))
    suelo(F)
    fl = 1.0 if (int(t * 5) % 4 == 0 and t > D * 0.3) else 0.0
    primer_espejo(F, t, luz=0.5 + 0.3 * fl)
    asomado_en(F, (EX + EW / 2, EY + 320), 0.9 * fl, t, mueca=0.4)
    marco_primero(F, t)
    NORA.draw(F, pose(head=-8, a1u=-10, a2u=10), 790, PISO, f=-1, face="neutral")
    LEO.draw(F, pose(head=-10, a1u=30, a1l=-30), 930, PISO, f=-1, face="scared")
    img = iluminar_(F, [((EX + EW / 2, EY + 360), 460, 0.7 + 0.3 * fl), ((840, 1000), 380, 0.5)])
    return img, dict(grain=9, tint=(VERDE, 0.08 + 0.1 * fl), flash=(VERDE, 0.4 * (1 - seg(t, 0, 0.35))), glitch=0.3 * fl)

def tapan(t, D, fi):
    pan = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(250, 820, pan), y=930, z=1.1))
    F.rect(-800, PISO, 2000, 2700, fill=(30, 14, 30))
    for i in range(-8, 16): F.rect(i * 120, PISO, i * 120 + 60, PISO + 900, fill=(44, 20, 40))
    F.line([(-800, PISO), (2000, PISO)], (90, 40, 74), 6)
    for i in range(6):
        x = -260 + i * 260; y0 = 520; w, h = 200, PISO - 40 - y0
        tap = seg(t, D * (0.05 + 0.13 * i), D * (0.15 + 0.13 * i))
        espejo(F, x, y0, w, h, brillo=0.4)
        fig, nn = FIGS[i % 4]
        if tap < 1:
            reflejo(F, fig, x, y0, w, h, pose(head=6), stretch=(1.5, 0.6)[i % 2], sc=0.8, face="scared", t=t, nina=nn)
        marco_espejo(F, x, y0, w, h, t=t, seed=i, bombillas=0.0 if tap >= 1 else 1.0)
        if tap > 0:                                                             # la sábana baja y lo tapa
            top = lerp(y0 - 400, y0 - 20, ease(tap))
            F.poly([(x - 20, top), (x + w + 20, top + 10), (x + w + 30, min(PISO, top + h + 60)), (x - 30, min(PISO, top + h + 60))],
                   fill=(180, 176, 166), outline=(120, 116, 108), w=3)
    xs = lerp(-60, 1240, pan)
    J = LEO.draw(F, walk(t, 1.0, 1.5), xs, PISO + 60, f=1, face="angry")
    F.poly([(J["a1h"][0], J["a1h"][1]), (J["a1h"][0] + 80, J["a1h"][1] - 20), (J["a1h"][0] + 60, J["a1h"][1] + 120), (J["a1h"][0] - 10, J["a1h"][1] + 100)], fill=(180, 176, 166))
    CARMEN.draw(F, walk(t + 0.3, 0.8, 1.2), xs - 180, PISO + 60, f=1, face="neutral")
    return F.finish(), dict(grain=8, tint=((255, 120, 200), 0.04))

def espera(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(520, 600, zp), y=lerp(860, 880, zp), z=lerp(0.95, 1.1, zp)))
    suelo(F)
    alba = ease(seg(t, 0, D))
    ventanuco(F, 820, 380, alba)
    primer_espejo(F, t, luz=0.4)
    marco_primero(F, t)
    NORA.draw(F, pose(head=-6, a1u=-8, a2u=8, body=-2 + math.sin(t * 2)), 800, PISO, f=-1, face="neutral")
    Jl = barra_leo = LEO.draw(F, pose(head=-8, a1u=110, a1l=40, a2u=60, a2l=60), 975, PISO, f=-1, face="scared")
    barra(F, Jl, f=-1)
    Jn = NINA.draw(F, pose(head=-12), 230, PISO, f=1, face="scared"); coletas(F, Jn, 0.8)
    CARMEN.draw(F, pose(head=-6, a1u=40, a1l=20), 110, PISO, f=1, face="neutral")
    img = iluminar_(F, [((EX + EW / 2, EY + 360), 460, 0.6), ((900, 440), 260, 0.4 + 0.5 * alba), ((840, 1000), 380, 0.4)])
    return img, dict(grain=8, tint=(ALBA, 0.04 + 0.05 * alba))

def llega(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(560, 560, zp), y=lerp(860, 780, zp), z=lerp(1.0, 1.35, zp),
                                  sx=noise(t * 30) * 4 * zp, sy=noise(t * 30, 2) * 4 * zp))
    suelo(F)
    fog = ease(seg(t, 0, D * 0.45)) * (1 - ease(seg(t, D * 0.5, D * 0.8)))
    ap = ease(seg(t, D * 0.45, D * 0.7))
    primer_espejo(F, t, luz=0.4 + 0.4 * ap, fog=fog)
    asomado_en(F, (EX + EW / 2, EY + 320), ap, t, mueca=0.2)
    marco_primero(F, t)
    NORA.draw(F, mix(pose(head=-6), pose(body=-6, head=4, a1u=40, a2u=-20), ap), lerp(840, 870, ap), PISO, f=-1, face="scared" if ap > 0.3 else "neutral")
    img = iluminar_(F, [((EX + EW / 2, EY + 360), 480, 0.6 + 0.4 * ap), ((860, 1000), 380, 0.4)])
    return img, dict(grain=9, tint=(VERDE, 0.06 + 0.1 * ap), flash=(VERDE, 0.5 * math.exp(-abs(t - D * 0.55) * 10)),
                     glitch=0.4 if (fi % 4 == 0 and D * 0.5 < t < D * 0.7) else 0.0)

def aporrea(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(600, 620, zp), y=lerp(820, 800, zp), z=lerp(1.05, 1.25, zp),
                                  sx=noise(t * 40) * 6, sy=noise(t * 40, 2) * 6))
    suelo(F)
    primer_espejo(F, t, luz=0.8)
    golpe = abs(math.sin(t * 9))
    asomado(F, (EX + EW / 2, EY + 300), 1.0, t, mueca=0.6 + 0.4 * math.sin(t * 4) ** 2, dedos=0.8 + 0.2 * golpe, base_y=EY + 640)
    for i in range(3): huella(F, EX + 70 + i * 110, EY + 720, 1.0, 1.0)
    marco_primero(F, t)
    NORA.draw(F, pose(body=-4, head=6, a1u=30, a1l=60, a2u=-20, a2l=40), 840, PISO, f=-1, face="angry")
    LEO.draw(F, pose(head=-14, a1u=150, a1l=20, a2u=40, a2l=60), 985, PISO, f=-1, face="talk" if int(t * 8) % 2 else "scared")
    img = iluminar_(F, [((EX + EW / 2, EY + 360), 500, 1.0), ((900, 1000), 420, 0.5)])
    return img, dict(grain=9, tint=(VERDE, 0.12), glitch=0.3 if fi % 6 == 0 else 0.0,
                     flash=(VERDE, 0.25 * max(0, math.sin(t * 9)) ** 8))

def feliz(t, D, fi):
    zp = ease(t / D)
    F = Frame(fondo("risa"), dict(x=lerp(560, 600, zp), y=lerp(820, 800, zp), z=lerp(1.1, 1.3, zp)))
    suelo(F)
    primer_espejo(F, t, luz=0.3)
    sale = 1 - ease(seg(t, 0, D * 0.3))
    asomado_en(F, (EX + EW / 2, EY + 320), sale, t, mueca=0.2)
    ap = ease(seg(t, D * 0.25, D * 0.5))
    if ap > 0:                                                                  # Tomás, feliz, saluda desde el cristal
        wave = 40 * math.sin(t * 8)
        NINO.draw(F, pose(head=-6, a1u=150 + wave, a1l=20, a2u=-10), EX + EW / 2, EY + EH - 30, f=1,
                  face="happy" if t > D * 0.45 else "neutral", t=t)
    marco_primero(F, t)
    suave = ease(seg(t, D * 0.5, D))
    NORA.draw(F, mix(pose(body=-4, head=6, a1u=30, a1l=60), pose(head=-4, a1u=60, a1l=-20), suave), 860, PISO, f=-1,
              face="neutral")
    img = iluminar_(F, [((EX + EW / 2, EY + 500), 480, 0.5 + 0.4 * ap), ((860, 1000), 400, 0.5)])
    return img, dict(grain=7, tint=((255, 220, 170), 0.06 * ap + 0.04))

def giro(t, D, fi):
    zz = ease(seg(t, D * 0.25, D))
    F = Frame(fondo("risa"), dict(x=lerp(640, 680, zz), y=lerp(820, 800, zz), z=lerp(1.15, 1.32, zz),
                                  sx=noise(t * 30) * 4 * zz, sy=noise(t * 30, 2) * 4 * zz))
    suelo(F)
    primer_espejo(F, t, luz=0.9)
    sm = seg(t, D * 0.05, D * 0.15) > 0
    asomado_en(F, (EX + EW / 2, EY + 320), ease(seg(t, D * 0.2, D * 0.35)), t, mueca=0.9)
    marco_primero(F, t)
    k = seg(t, D * 0.3, D * 0.75)
    J = NORA.draw(F, mix(pose(head=-4, a1u=60, a1l=-20), SCARED, ease(seg(t, D * 0.65, D * 0.8))), 880, PISO, f=-1,
                  face="happy" if t < D * 0.7 else "scared")
    if sm and t < D * 0.7:
        hx, hy = J["head"]; r = 33 * NORA.scale
        F.arc((hx, hy + r * 0.05), r * 0.6, 10, 170, (20, 10, 16), 5)
    if k > 0: dedos_fuera(F, k, t, 880)
    img = iluminar_(F, [((EX + EW / 2, EY + 360), 520, 1.0), ((880, 1000), 420, 0.6)])
    return img, dict(grain=9, tint=(VERDE, 0.1 + 0.1 * zz), flash=(VERDE, 0.5 * math.exp(-abs(t - D * 0.3) * 10)),
                     glitch=0.4 if (fi % 4 == 0 and t > D * 0.3) else 0.0)

def final(t, D, fi):
    F = Frame(base("oscuro"), dict(x=540, y=960, z=1.0))
    return F.finish(), {}

ESCENA_FN = dict(cebo=cebo, tapan=tapan, espera=espera, llega=llega, aporrea=aporrea, feliz=feliz, giro=giro, final=final)
PAUSA = dict(cebo=0.55, tapan=0.55, espera=0.55, llega=0.65, aporrea=0.65, feliz=0.55, giro=1.5, final=2.2)
