"""REGLAS 4 — Piscina municipal: "Después de cerrar, no mires el fondo de la piscina." (formato: ver reglas.md)"""
import math
from functools import lru_cache
from PIL import ImageDraw, ImageFilter
from motor import *
from motor3d import *
from escenarios3d import *
from turno3d import _caja_en, proyectar, cara_puntos, sonrisa

G = __import__("guionreglas4" + ("_en" if IDIOMA == "en" else ""))
ROJO = (204, 40, 36)                         # camiseta roja de socorrista
PIEL = (218, 186, 160)
PELO = (58, 38, 26)
NINA_ROPA, NINA_PIEL, NINA_PELO = (226, 226, 220), (168, 186, 192), (16, 14, 16)
HONDO = 2.4
NX, NZ = -0.45, -7.4                           # pies de la niña en el fondo (la cabeza hacia -z)
A_NINA = 0.7

def coleta(col):
    def f(e, cab, u):
        e.add(esfera(u(14), col, 1), cadena(cab, mover(0, u(6), -u(30)), escala(1, 1.6, 1)))
    return f

def melena(col):
    def f(e, cab, u):
        e.add(esfera(u(26), col, 1), cadena(cab, mover(0, -u(10), -u(10)), escala(1.15, 1.6, 0.8)))
    return f

def marta(esc, p, x, z, yaw=0.0, y=0.0, cara="neutral"):
    return humano(esc, p, x=x, z=z, y=y, yaw=yaw, ropa=ROJO, piel=PIEL, pantalon=PIEL, cara=cara, pelo=PELO, extra_cabeza=coleta(PELO))

def nina_fondo(esc, oscura=0.0):
    piel = tuple(int(v * (1 - 0.6 * oscura)) for v in NINA_PIEL)
    ropa = tuple(int(v * (1 - 0.6 * oscura)) for v in NINA_ROPA)
    return tumbado(esc, NX, -HONDO, NZ, ropa=ropa, piel=piel, pantalon=piel, pelo=NINA_PELO, alto=A_NINA,
                   extra_cabeza=melena(NINA_PELO), p=pose(a1u=8, a1l=4, a2u=-8, a2l=4, l1u=3, l1l=0, l2u=-3, l2l=0))

def ojos(img, cam, cab, alto=A_NINA, f=1.0):
    """ojos blancos muy abiertos con la pupila clavada en la cámara"""
    if f <= 0: return img
    d = ImageDraw.Draw(img)
    for e in cara_puntos(cab, alto)[:2]:
        q = proyectar(cam, e)
        if not q: continue
        r = 0.028 / q[2] * 1800 * alto
        d.ellipse((q[0] - r, q[1] - r * 0.8, q[0] + r, q[1] + r * 0.8), fill=tuple(int(v * f) for v in (236, 240, 236)))
        d.ellipse((q[0] - r * 0.45, q[1] - r * 0.45, q[0] + r * 0.45, q[1] + r * 0.45), fill=(6, 6, 8))
    return img

def nave(luces_on=None, focos=1.0, reloj="00:00"):
    def hacer(agua, extra=None):
        esc = escena(niebla=((8, 14, 18), 7.0, 30.0), amb=0.1)
        L = piscina(esc, hondo=HONDO, luces_on=luces_on, focos=focos, agua=agua, reloj=reloj)
        return esc, L
    return hacer

def con(hacer_base, fn):
    """añade piezas a una nave: fn(esc, agua) -> luces extra"""
    def h(agua):
        esc, L = hacer_base(agua)
        r = fn(esc, agua)
        L = L + (r if isinstance(r, list) else [])
        return esc, L
    return h

OFF = [0, 0, 0, 0, 0, 0]

# ---------- escenas ----------
def arranque(t, D, fi):
    k = ease(min(1, t / D))
    cam = Camara(ojo=(NX, lerp(1.4, 1.2, k), NZ + lerp(1.9, 1.6, k)), mira=(NX, -HONDO, NZ - 0.6), fov=lerp(50, 42, k))
    cab = []
    h = con(nave(OFF, focos=0.85 + 0.15 * math.sin(t * 9)), lambda e, a: cab.append(nina_fondo(e, oscura=1.0)))
    img, esc = render_piscina(h, cam, t, transp=0.82, ondas=0.8)
    img = ondas_2d(img, cam, (NX, -0.12, NZ - 0.6), t, n=3, f=0.7, r_max=1.8)
    img = aclarar(etiquetas(img, esc, cam), 1.05, 0.95)
    img = ojos(img, cam, cab[0], f=1.0)
    return rotulo_regla(img, 1, G.REGLA, p=1.0, y=330), dict(grain=8)

def cierre(t, D, fi):
    k = ease(min(1, t / D))
    on = [1, 1, 0.6, 0, 0, 0]
    x, z = 5.0, lerp(-1.6, -4.2, k)
    h = con(nave(on), lambda e, a: marta(e, walk(t, 0.5, 0.55), x, z, yaw=math.pi))
    cam = Camara(ojo=(lerp(3.4, 3.6, k), 1.7, lerp(-9.0, -8.6, k)), mira=(5.0, 1.0, z), fov=52)
    img, esc = render_piscina(h, cam, t, transp=0.55)
    return aclarar(etiquetas(img, esc, cam), 1.3), dict(grain=8)

def grito(t, D, fi):
    apaga = seg(t, 0.0, D * 0.25)
    on = [1 - apaga, 1 - apaga, 0, 0, 0, 0]
    gira = ease(seg(t, D * 0.35, D * 0.6))
    salpica = seg(t, D * 0.3, D * 0.4)
    h = con(nave(on), lambda e, a: marta(e, dict(STAND, head=lerp(0, 6, gira)), 4.7, -4.4, yaw=lerp(math.pi, -math.pi / 2 - 0.3, gira),
                                         cara="scared" if gira > 0.7 else "neutral"))
    cam = Camara(ojo=(6.9, 1.9, -1.8), mira=(1.6, -0.2, -8.0), fov=56)
    img, esc = render_piscina(h, cam, t, transp=0.4)
    img = ondas_2d(img, cam, (0.3, -0.12, -8.0), t * 1.6, n=4, f=salpica, r_max=1.8)
    if salpica > 0:                                            # salpicaduras
        q = proyectar(cam, (0.3, 0.1, -8.0)); d = ImageDraw.Draw(img)
        for i in range(10):
            a = i * 0.63 + t * 2; r = 40 + 30 * math.sin(t * 13 + i)
            d.ellipse((q[0] + math.cos(a) * r - 7, q[1] - abs(math.sin(a)) * r * 1.3 - 7, q[0] + math.cos(a) * r + 7, q[1] - abs(math.sin(a)) * r * 1.3 + 7), fill=(220, 245, 255))
    img = aclarar(etiquetas(img, esc, cam), 1.35, 0.85)
    return img, dict(grain=9)

def mira(t, D, fi):
    k = ease(min(1, t / D))
    cam = Camara(ojo=(NX + 0.2, lerp(1.7, 1.4, k), NZ + lerp(1.2, 0.8, k)), mira=(NX, -HONDO, NZ - 0.9), fov=lerp(48, 32, k))
    cab = []
    h = con(nave(OFF), lambda e, a: cab.append(nina_fondo(e)))
    img, esc = render_piscina(h, cam, t, transp=0.8, ondas=0.6)
    img = ojos(img, cam, cab[0], f=seg(t, D * 0.45, D * 0.6))
    img = aclarar(img, 1.1, 0.95)
    return img, dict(grain=10, tint=((0, 40, 80), 0.1))

def salta(t, D, fi):
    s = seg(t, D * 0.3, D * 0.7)                                # vuelo
    x = lerp(3.75, 1.6, ease(s)); y = 0.5 * math.sin(math.pi * min(s / 0.6, 1.0)) - 2.2 * max(0.0, s - 0.6) / 0.4
    dentro = s > 0.75
    body = lerp(0, 75, ease(s))
    p = dict(STAND, body=body, a1u=lerp(14, 175, ease(s * 2)), a2u=lerp(-14, 175, ease(s * 2)), a1l=0, a2l=0)
    def piezas(e, agua):
        if not (agua and y < -0.6):
            marta(e, p, x, -8.0, y=y, yaw=-math.pi / 2)
    h = con(nave(OFF), piezas)
    cam = Camara(ojo=(6.8, 1.5, -4.4), mira=(2.8, 0.9, -8.2), fov=56)
    img, esc = render_piscina(h, cam, t, transp=0.5)
    plaf = seg(t, D * 0.62, D * 0.9)
    if plaf > 0:
        q = proyectar(cam, (1.6, 0.0, -8.0)); d = ImageDraw.Draw(img)
        for i in range(18):
            a = i * 0.35; r = (40 + 220 * ease_out(plaf)) * (0.6 + 0.4 * math.sin(i * 7.1))
            yy = q[1] - math.sin(a) * r * 1.4 * (1 - plaf * 0.6)
            d.ellipse((q[0] + math.cos(a) * r - 10, yy - 10, q[0] + math.cos(a) * r + 10, yy + 10), fill=(230, 248, 255))
        img = ondas_2d(img, cam, (1.6, -0.12, -8.0), plaf, n=3, f=1.0, r_max=2.4)
    img = aclarar(etiquetas(img, esc, cam), 1.35, 0.85)
    golpe = D * 0.62 <= t < D * 0.68
    return img, dict(grain=9, flash=((255, 255, 255), 0.4) if golpe else None)

def fondo(t, D, fi):
    agarra = ease(seg(t, D * 0.45, D * 0.6))
    hunde = ease(seg(t, D * 0.6, D)) * 0.5
    sonr = seg(t, D * 0.1, D * 0.4)
    cab = []
    def piezas(e, agua):
        cab.append(humano(e, dict(STAND, a1u=lerp(10, 178, agarra), a1l=0, head=-12), x=0.15, z=-8.6, y=-HONDO, yaw=math.pi / 2 + 0.6,
                          ropa=NINA_ROPA, piel=NINA_PIEL, pantalon=NINA_PIEL, pelo=NINA_PELO, alto=0.82, extra_cabeza=melena(NINA_PELO)))
        pat = math.sin(t * 9) * 25
        marta(e, dict(STAND, a1u=150 + pat, a2u=150 - pat, a1l=20, a2l=20, l1u=10 + pat * 0.4, l2u=-10 - pat * 0.4, l1l=-30, l2l=-30, head=-20),
              0.55, -8.6, y=-1.55 - hunde, yaw=math.pi / 2 + 0.3, cara="scared")
    esc = escena(niebla=((10, 60, 80), 2.0, 11.0), amb=0.2)
    L = piscina(esc, hondo=HONDO, luces_on=OFF, focos=1.0, agua=True, desde_abajo=True, nave=False)
    piezas(esc, True)
    k = ease(min(1, t / D))
    cam = Camara(ojo=(2.6, -1.9, lerp(-5.6, -6.2, k)), mira=(0.3, -1.25, -8.6), fov=lerp(58, 50, k), roll=0.05 * math.sin(t * 1.5))
    img = esc.render(cam, L + [Luz((1.8, -1.2, -6.5), (140, 230, 255), 5.0, fuerza=0.9)])
    img = sonrisa(img, cam, cab[0], p=sonr, ancho=1.3)
    img = ojos(img, cam, cab[0], alto=0.82, f=1.0)
    img = burbujas(img, cam, (0.55, -0.5 - hunde, -8.6), t, n=18, f=1.0)
    img = bajo_agua(aclarar(img, 1.3, 0.85), t, 0.8)
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * agarra), glitch=0.3 if agarra > 0 and fi % 7 == 0 else 0.0)

def camara(t, D, fi):
    sube = seg(t, D * 0.3, D * 0.5) * (1 - seg(t, D * 0.62, D * 0.8))
    hy = -0.5 + 0.9 * ease(sube)
    def piezas(e, agua):
        if hy > -0.1:
            e.add(prisma(0.065, 0.055, 0.7, PIEL), mover(0.6, hy, -8.6))
            e.add(caja(0.13, 0.2, 0.07, PIEL), mover(0.6, hy + 0.1, -8.6))
    h = con(nave(OFF, focos=0.8), piezas)
    cam = Camara(ojo=(4.6, 3.6, -3.4), mira=(0.6, -0.2, -8.6), fov=42)
    img, esc = render_piscina(h, cam, t, transp=0.25, ondas=0.3)
    img = ondas_2d(img, cam, (0.6, -0.12, -8.6), t * 1.3, n=3, f=seg(t, D * 0.3, D * 0.4) * (1 - seg(t, D * 0.85, D)), r_max=1.4)
    img = cctv(aclarar(etiquetas(img, esc, cam), 1.45, 0.8), 2, "00:2" + f"{min(9, int(t)):d}:{int(t * 7) % 60:02d}")
    d = ImageDraw.Draw(img)
    d.text((W / 2, 1290), tr("PISCINA · VASO GRANDE"), font=font(48), fill=(220, 220, 210), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    img = negro(img, seg(t, D * 0.88, D))
    return img, dict(grain=13, glitch=0.3 if fi % 11 == 0 else 0.0)

def final(t, D, fi):
    cam = Camara(ojo=(NX + 0.2, 1.6, NZ + 1.2), mira=(NX, -HONDO, NZ - 0.9), fov=46)
    def piezas(e, agua):
        tumbado(e, NX, -HONDO, NZ - 0.2, ropa=ROJO, piel=PIEL, pantalon=PIEL, pelo=PELO, extra_cabeza=coleta(PELO), cara="ninguna",
                p=pose(a1u=8, a1l=4, a2u=-8, a2l=4, l1u=3, l1l=0, l2u=-3, l2l=0))
    h = con(nave([1] * 6, focos=1.0, reloj="08:00"), piezas)
    img, esc = render_piscina(h, cam, t, transp=0.8, ondas=0.4)
    img = aclarar(img, 1.2)
    if t > 1.4:
        img = ficha_final(img, G.NOMBRE, G.OFICIO, G.FECHA, G.REGLA, p=ease_back(seg(t, 1.4, 1.9)), t=t, sello=G.SELLO)
    return img, dict(grain=9)

ESCENA_FN = dict(arranque=arranque, cierre=cierre, grito=grito, mira=mira, salta=salta, fondo=fondo, camara=camara, final=final)
PAUSA = dict(arranque=0.3, cierre=0.3, grito=0.4, mira=0.5, salta=0.5, fondo=0.6, camara=0.8, final=1.8)
