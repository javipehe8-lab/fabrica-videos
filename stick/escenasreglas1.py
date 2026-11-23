"""REGLAS 1 — Hospital, planta 4: "Si llaman desde la 414, no vayas." (modelo para la serie: ver reglas.md)"""
import math, random
from PIL import ImageDraw, ImageFilter
from motor import *
from motor3d import *
from escenarios3d import *

G = __import__("guionreglas1" + ("_en" if IDIOMA == "en" else ""))
UNIF = (74, 140, 124)                      # pijama verde de celador
PIEL = (214, 196, 180)
PUERTAS = [(-2.5, "410", 1), (-5.5, "411", -1), (-8.5, "412", 1), (-11.5, "413", -1), (-14.5, "414", -1)]
Z414 = -14.5

def oscar(esc, p, x, z, yaw=0.0, cara="neutral"):
    return humano(esc, p, x=x, z=z, yaw=yaw, ropa=UNIF, piel=PIEL, pantalon=UNIF, cara=cara, pelo=(52, 40, 32))

def planta(luces_on=None, abierta414=0.15, luz414=0.0, piloto=0.0):
    esc = escena(niebla=((14, 16, 18), 5.0, 26.0))
    pu = [p if p[1] != "414" else (p[0], p[1], p[2], abierta414, luz414) for p in PUERTAS]
    L = pasillo(esc, 18, puertas=pu, luces_on=luces_on)
    interfono(esc, -1.19, 1.55, Z414 + 1.0, -1, luz=piloto, escala_=1.8)
    return esc, L

def parpadeo(t, f=4): return 1.0 if int(t * f) % 2 == 0 else 0.25

# ---------- escenas ----------
def arranque(t, D, fi):
    k = ease(min(1, t / D))
    on = [1, 1, 1, 1, 0.35 + 0.65 * parpadeo(t, 7), 1]
    esc, L = planta(on, abierta414=0.12, piloto=parpadeo(t))
    cam = Camara(ojo=(0.25, 1.62, lerp(-6.0, -9.5, k)), mira=(-1.0, 1.35, Z414), fov=lerp(46, 38, k))
    img = etiquetas(esc.render(cam, L + [Luz((-1.0, 1.6, Z414 + 1.0), (255, 60, 50), 3.5, fuerza=0.9 * parpadeo(t))]), esc, cam)
    img = aclarar(img, 1.3, 0.85)
    return rotulo_regla(img, 1, G.REGLA, p=1.0), dict(grain=8)

def panel(t, D, fi):
    esc, L = planta(piloto=parpadeo(t))
    cam = Camara(ojo=(0.3, 1.62, 0.3), mira=(-0.2, 1.4, -15), fov=58)
    img = aclarar(esc.render(cam, L), 1.2).filter(ImageFilter.GaussianBlur(9))
    return panel_llamadas(img, ["410", "411", "412", "413", "414", "415", "416", "417"], activo="414", t=t, y=520), dict(grain=7)

def voz(t, D, fi):
    habla = seg(t, D * 0.42, D * 0.5) * (1 if t < D * 0.95 else 0)
    esc, L = planta(piloto=1.0)
    cam = Camara(ojo=(0.3, 1.62, -4.0), mira=(-0.6, 1.4, Z414), fov=50)
    img = aclarar(esc.render(cam, L), 1.1).filter(ImageFilter.GaussianBlur(8))
    z = 1 + 0.06 * ease(t / D)
    img = interfono_2d(img, "414", habla=habla, piloto=1.0 if habla else parpadeo(t), t=t)
    return img, dict(grain=10, glitch=0.25 if habla and fi % 6 == 0 else 0.0, tint=((255, 0, 30), 0.14 * habla))

def camina(t, D, fi):
    k = ease(min(1, t / D))
    z = lerp(-3.0, Z414 + 1.0, k)
    n_off = int(k * 6)                          # las luces se apagan detrás de él
    on = [0 if i * 3 + 1.5 < -z - 2 and i < n_off else 1 for i in range(6)]
    esc, L = planta(on, abierta414=0.2 + 0.3 * k, piloto=1.0)
    oscar(esc, walk(t, 0.55, 0.55), 0.1, z, yaw=math.pi)
    cam = Camara(ojo=(0.45, 1.75, z + 3.2), mira=(-0.3, 1.3, z - 4), fov=54)
    img = etiquetas(esc.render(cam, L), esc, cam)
    return aclarar(img, 1.2), dict(grain=9)

def _habitacion414(t, destapada=0.0, ojos=0.0):
    esc = escena(niebla=((8, 10, 10), 3.0, 12.0), amb=0.08)
    habitacion(esc, -2.0, 2.0, -4.5, 0.4, 2.8, col_pared=(120, 128, 122), suelo=(100, 104, 100))
    M = cama(esc, 0, -2.4, 0, bulto=True, cabeza=PIEL if destapada > 0.5 else None)
    monitor_constantes(esc, 1.15, -3.2, -0.5)
    if destapada > 0.5:                         # su propia cara, mirando al techo
        for dx in (-0.07, 0.07):
            esc.add(caja(0.06, 0.03, 0.04 + 0.05 * ojos, (6, 6, 8)), cadena(M, mover(dx, 1.18, -0.70)))
        esc.add(caja(0.09, 0.03, 0.06 * ojos + 0.01, (6, 6, 8)), cadena(M, mover(0, 1.17, -0.58)))
        esc.add(esfera(0.21, (52, 40, 32), 1), cadena(M, mover(0, 0.96, -0.86), escala(1, 0.8, 0.8)))   # pelo
    luces = [Luz((1.0, 1.9, -3.0), (110, 255, 150), 4.5, fuerza=1.1), Luz((0, 2.6, 0.2), (255, 235, 200), 6, dir=(0, -0.4, -1), cono=26, fuerza=0.7)]
    return esc, luces

def cama_(t, D, fi):
    esc, L = _habitacion414(t)
    k = ease(min(1, t / D))
    cam = Camara(ojo=(0.35, 1.62, lerp(0.3, -0.4, k)), mira=(0, 0.85, -2.6), fov=lerp(55, 45, k))
    return aclarar(esc.render(cam, L), 1.35), dict(grain=10)

def cara(t, D, fi):
    abre = seg(t, D * 0.55, D * 0.75)
    esc, L = _habitacion414(t, destapada=1.0, ojos=abre)
    sh = 0.03 * abre * (1 - seg(t, D * 0.75, D))
    cam = Camara(ojo=(0.05 + sh * math.sin(t * 50), 1.95, -1.95), mira=(0, 1.0, -3.15), fov=lerp(40, 30, ease(t / D)))
    img = aclarar(esc.render(cam, L), 1.4)
    hit = abre > 0
    return img, dict(flash=((255, 255, 255), max(0, 1 - (t - D * 0.55) / 0.25)) if hit else None,
                     glitch=0.4 if hit and fi % 3 == 0 else 0.0, tint=((255, 0, 30), 0.22 * abre), grain=12)

def puerta_(t, D, fi):
    cierra = seg(t, D * 0.05, D * 0.15)
    apaga = seg(t, D * 0.3, D * 0.8)
    on = [0 if (5 - i) < apaga * 6 else 1 for i in range(6)]          # se apagan del fondo hacia la cámara
    esc, L = planta(on, abierta414=0.6 * (1 - cierra), luz414=0.0, piloto=0.0)
    cam = Camara(ojo=(1.05, 2.6, 0.6), mira=(-0.6, 0.8, -13), fov=62)
    img = cctv(esc.render(cam, L), 4, "03:12:" + f"{int(9 + t):02d}")
    img = negro(img, seg(t, D * 0.82, D))
    return img, dict(grain=14, glitch=0.5 if 0.05 * D < t < 0.2 * D else 0.0)

def final(t, D, fi):
    esc, L = planta([0, 0, 0, 0, 0, 0], abierta414=0.0, piloto=parpadeo(t, 3))
    cam = Camara(ojo=(1.05, 2.6, 0.6), mira=(-0.6, 0.8, -13), fov=62)
    img = cctv(esc.render(cam, L + [Luz((-1.0, 1.6, Z414 + 1.0), (255, 60, 50), 3.0, fuerza=parpadeo(t, 3))]), 4, tr("NOCHE SIGUIENTE") + " 03:12")
    img = ficha_final(img, G.NOMBRE, G.OFICIO, G.FECHA, G.REGLA, p=ease_back(seg(t, 0.1, 0.6)), t=t)
    return img, dict(grain=10)

ESCENA_FN = dict(arranque=arranque, panel=panel, voz=voz, camina=camina, cama=cama_, cara=cara, puerta=puerta_, final=final)
PAUSA = dict(arranque=0.3, panel=0.3, voz=0.6, camina=0.3, cama=0.4, cara=0.5, puerta=0.9, final=1.8)
