"""HILOS MALDITOS 1 — "Mi abuela desapareció tres días." Fondo: carretera de noche entre pinos (bucle continuo).
Las piezas genéricas del formato (tarjeta del post, cabecera, EDIT, móvil, carretera) están en hilos.py."""
import math
from motor import *
from motor3d import *
from hilos import carretera, tarjeta_post, cabecera_post, tarjeta_edit, movil_2d, sigueme

G = __import__("guionhilo1")
CAMISON = (226, 224, 214)

def abuela(esc, x, z, yaw=0.0, cara="neutral"):
    humano(esc, STAND, x=x, z=z, yaw=yaw, ropa=CAMISON, piel=(208, 196, 186), pantalon=CAMISON, cara=cara, pelo=(196, 194, 190))

def fondo(fi, figura=None, faros=1.0, oscuro=0.0):
    img = carretera(fi / FPS, figura=figura, faros=faros)
    return img

def titulo(t, D, fi):
    # GANCHO desde el fotograma 0: la abuela en camisón, en medio de la carretera, a la luz de los faros,
    # y la tarjeta del post ya encima (sin esperar a que aparezca).
    cerca = lerp(6.0, 16.0, ease(seg(t, 0.0, D)))
    fig = (lambda esc: abuela(esc, 1.7, -cerca, yaw=0.0)) if t < D * 0.8 or (fi // 3) % 4 else None
    img = fondo(fi, figura=fig)
    p = lerp(0.92, 1.0, ease_out(seg(t, 0.0, 0.25)))
    return img, dict(grain=6, tint=((255, 0, 30), 0.12 * max(0.0, 1 - t)),
                     overlay=lambda im: tarjeta_post(im, G.POST, p=p, t=t, cy=1480))

def _historia(fi, t, figura=None, **kw):
    img = fondo(fi, figura=figura, **kw)
    return img, dict(grain=7, overlay=lambda im: cabecera_post(im, G.POST))

def alzheimer(t, D, fi): return _historia(fi, t)
def noche(t, D, fi): return _historia(fi, t)
def coche(t, D, fi): return _historia(fi, t)
def mesa(t, D, fi): return _historia(fi, t)

def pinar(t, D, fi):
    # al final del plano, una mujer en camisón sentada… no: de pie, quieta, en el arcén. Pasa de largo.
    k = seg(t, D * 0.45, D)
    fig = (lambda esc: abuela(esc, 3.3, lerp(-34, 2, k), yaw=-math.pi / 2)) if 0 < k < 1 else None
    return _historia(fi, t, figura=fig)

def puerta(t, D, fi):
    # está en medio de la carretera, siempre a la misma distancia del coche: no la alcanzas nunca
    cerca = lerp(26, 14, ease(seg(t, 0, D)))
    parp = 1.0 if (fi // 3) % 7 else 0.35
    fig = lambda esc: abuela(esc, 1.0, -cerca, yaw=0.0, cara="neutral")
    img, fx = _historia(fi, t, figura=fig, faros=parp)
    fx["tint"] = ((255, 0, 30), 0.10 * seg(t, D * 0.55, D * 0.7))
    return img, fx

def movil(t, D, fi):
    img = fondo(fi)
    return img, dict(grain=8, dark=0.35, overlay=lambda im: cabecera_post(movil_2d(im, "ABUELA", t, sonando=True), G.POST))

def llamada(t, D, fi):
    img = fondo(fi)
    return img, dict(grain=9, dark=0.4, glitch=0.2 if fi % 8 == 0 else 0.0, tint=((255, 0, 30), 0.12),
                     overlay=lambda im: cabecera_post(movil_2d(im, "ABUELA", t, sonando=False, segundos=int(t) + 3), G.POST))

def final(t, D, fi):
    fig = lambda esc: abuela(esc, 1.0, -12.0, yaw=0.0)
    img = fondo(fi, figura=fig if (fi // 4) % 9 else None)
    p = ease_back(seg(t, 0.0, 0.3))
    return img, dict(grain=8, dark=0.35, overlay=lambda im: sigueme(tarjeta_edit(im, G.EDIT, G.POST, p=p, t=t, dur=D * 0.8), t, D))

ESCENA_FN = dict(titulo=titulo, alzheimer=alzheimer, noche=noche, pinar=pinar, coche=coche, mesa=mesa,
                 puerta=puerta, movil=movil, llamada=llamada, final=final)
PAUSA = dict(titulo=0.5, alzheimer=0.3, noche=0.3, pinar=0.4, coche=0.4, mesa=0.4, puerta=0.7, movil=0.4, llamada=0.6, final=2.2)
