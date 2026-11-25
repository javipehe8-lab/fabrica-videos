"""REGLAS 3 — Metro, último tren: "Si el tren de las 2:40 para en el andén, no subas." (formato: ver reglas.md)"""
import math, random
from functools import lru_cache
from PIL import ImageDraw, ImageFilter
from motor import *
from motor3d import *
from escenarios3d import *
from turno3d import _caja_en, proyectar

G = __import__("guionreglas3" + ("_en" if IDIOMA == "en" else ""))
UNIF = (36, 44, 70)                         # uniforme azul marino de vigilante
PIEL = (214, 190, 168)
PIEL_M = (146, 154, 150)                    # los del tren: piel gris
Z0 = 4.0                                    # morro del tren
ZP = Z0 - 7.0                               # la puerta del medio (z = -3)
ZD, ZS = ZP - 0.65, ZP + 0.15               # Dani y el sitio vacío a su lado
XB = 2.62                                   # donde se sientan (banco del fondo)

def gorra(col):
    def f(e, cab, u):
        e.add(esfera(u(26), col, 1), cadena(cab, mover(0, u(10), 0), escala(1, 0.55, 1)))
        e.add(caja(u(36), u(4), u(22), col), cadena(cab, mover(0, u(8), u(24))))
    return f

def andres(esc, p, x, z, yaw=0.0, cara="neutral"):
    cab = humano(esc, p, x=x, z=z, yaw=yaw, ropa=UNIF, piel=PIEL, pantalon=(28, 30, 40), cara=cara, extra_cabeza=gorra(UNIF))
    u = lambda v: v / 100 * (1.75 / 3.06)                     # chaleco reflectante
    M = cadena(mover(x, 0, z), rot_y(yaw), mover(0, u(L["ul"] + L["ll"] + 6), 0), rot_x(math.radians(p.get("body", 0))))
    esc.add(caja(u(36), u(26), u(22), (210, 220, 60)), cadena(M, mover(0, u(L["torso"] * 0.55), 0)), sesgo=0.02)
    esc.add(caja(u(37), u(5), u(23), (230, 230, 230)), cadena(M, mover(0, u(L["torso"] * 0.55), 0)), sesgo=0.04)
    return cab

# los desaparecidos de la línea: (z del asiento, ropa, pelo, nombre, año)
PASAJEROS = [(Z0 - 0.9, (90, 70, 50), (60, 44, 30), "Elena R.", 1987), (Z0 - 2.0, (60, 80, 70), (150, 150, 150), "Tomás G.", 1979),
             (Z0 - 4.3, (120, 100, 140), (30, 24, 20), "Pilar S.", 2003), (Z0 - 5.4, (50, 52, 60), None, "Luis C.", 1994),
             (ZP - 2.0, (140, 120, 80), (90, 60, 30), "Marta V.", 2011), (ZP - 3.1, (70, 70, 110), (40, 30, 26), "Jorge P.", 1999)]
DANI_ROPA, DANI_PELO = (150, 36, 36), (36, 26, 22)

def dani(esc, z=ZD, head=0.0, brazos=(40, 60, 40, 60), cara="neutral"):
    return sentado(esc, XB, z, yaw=-math.pi / 2, ropa=DANI_ROPA, piel=PIEL_M, pantalon=(50, 56, 80), pelo=DANI_PELO, head=head, brazos=brazos, cara=cara)

def pasajeros(esc, dz=0.0):
    for z, ropa, pelo, _, _ in PASAJEROS:
        sentado(esc, XB, z + dz, yaw=-math.pi / 2, ropa=ropa, piel=PIEL_M, pelo=pelo)

LUCES = [1, 0.5, 0, 1, 0, 0, 0.6, 0, 0]               # andén casi a oscuras

def estacion(luces_on=None, abierto=0.0, luz_tren=1.0, faros=0.0, dz=0.0, con_dani=True, con_gente=True, dani_kw=None):
    esc = escena(niebla=((6, 8, 10), 5.0, 26.0), amb=0.1)
    L = anden_metro(esc, largo=36, z0=12.0, luces_on=LUCES if luces_on is None else luces_on, reloj_z=7.0, nombre_z=-6.0)
    L += vagon_metro(esc, Z0 + dz, largo=14, puertas=(-2.5, -7.0, -11.5), abierto=abierto, luz=luz_tren, faros=faros)
    if con_gente: pasajeros(esc, dz)
    if con_dani: dani(esc, ZD + dz, **(dani_kw or {}))
    return esc, L

def parpadeo(t, f=4): return 1.0 if int(t * f) % 2 == 0 else 0.3

@lru_cache(None)
def fotos(con_andres=False):
    fs = []
    for z, ropa, pelo, nom, anio in PASAJEROS[:4] + PASAJEROS[5:]:
        fs.append((retrato(lambda e, r=ropa, pe=pelo: humano(e, STAND, ropa=r, piel=PIEL, pelo=pe)), nom, anio))
    fs.insert(4, (retrato(lambda e: humano(e, STAND, ropa=DANI_ROPA, piel=PIEL, pelo=DANI_PELO)), "Daniel M.", 2021))
    if con_andres:
        fs.append((retrato(lambda e: andres(e, STAND, 0, 0)), "Andrés M.", 2026))
    return fs

def fondo_anden(blur=10):
    esc, L = estacion(con_gente=False, con_dani=False)
    cam = Camara(ojo=(-1.0, 1.7, 2.0), mira=(-3.0, 1.6, -2.0), fov=60)
    return aclarar(esc.render(cam, L), 1.1).filter(ImageFilter.GaussianBlur(blur))

def destellos(img, cam, pts, f=1.0, col=(255, 246, 210)):
    """halo de los faros (2D)"""
    from PIL import Image as _I
    capa = _I.new("RGB", img.size, (0, 0, 0)); d = ImageDraw.Draw(capa)
    for p in pts:
        q = proyectar(cam, p)
        if not q: continue
        r = 900 / max(q[2], 0.5)
        d.ellipse((q[0] - r, q[1] - r * 0.7, q[0] + r, q[1] + r * 0.7), fill=tuple(int(v * 0.8 * f) for v in col))
    from PIL import ImageChops
    return ImageChops.add(img, capa.filter(ImageFilter.GaussianBlur(40)))

def cara_cabina(esc, dz=0.0):
    """alguien pegado al cristal de la cabina, mirando"""
    x = 0.25 + 1.35; z = Z0 + dz + 0.16
    esc.add(esfera(0.14, PIEL_M, 1), cadena(mover(x, 1.62, z), escala(0.9, 1.1, 0.5)), sesgo=0.3)
    for dx in (-0.05, 0.05): esc.add(caja(0.045, 0.03, 0.02, (6, 6, 8)), mover(x + dx, 1.65, z + 0.07), sesgo=0.4)

# ---------- escenas ----------
def arranque(t, D, fi):
    k = ease(min(1, t / D))
    on = [0.3 + 0.7 * parpadeo(t, 6), 1, 0, 1, 0, 0, 0.6, 0, 0]
    esc, L = estacion(on, faros=0.75 + 0.25 * parpadeo(t, 3))
    cara_cabina(esc)
    cam = Camara(ojo=(-1.2, 1.6, lerp(11.8, 11.3, k)), mira=(0.4, lerp(1.55, 1.45, k), 0.0), fov=lerp(56, 53, k))
    img = etiquetas(esc.render(cam, L + [Luz((1.6, 0.5, Z0 + 1.0), (255, 245, 210), 5, fuerza=0.8)]), esc, cam)
    img = aclarar(img, 1.2, 0.85)
    img = destellos(img, cam, [(0.75, 0.38, Z0 + 0.12), (2.45, 0.38, Z0 + 0.12)], 0.75 + 0.25 * parpadeo(t, 3))
    return rotulo_regla(img, 1, G.REGLA, p=1.0, y=330), dict(grain=8)

def anden(t, D, fi):
    k = ease(min(1, t / D))
    esc, L = estacion()
    andres(esc, dict(STAND, head=lerp(0, 8, k)), -1.1, 0.2, yaw=math.pi / 2 + 0.25)
    cam = Camara(ojo=(lerp(-2.6, -2.4, k), 1.75, lerp(3.6, 3.0, k)), mira=(0.9, 1.25, -2.0), fov=56)
    img = etiquetas(esc.render(cam, L), esc, cam)
    return aclarar(img, 1.25), dict(grain=8)

def puertas(t, D, fi):
    ab = ease(seg(t, D * 0.08, D * 0.45))
    esc, L = estacion(abierto=ab, luz_tren=0.7 + 0.3 * ab)
    k = ease(min(1, t / D))
    cam = Camara(ojo=(-2.2, 1.6, lerp(ZP + 2.0, ZP + 1.5, k)), mira=(2.6, 1.0, ZP - 2.4), fov=60)
    img = aclarar(esc.render(cam, L), 1.15)
    return img, dict(grain=9)

def carteles(t, D, fi):
    img = fondo_anden()
    p = seg(t, D * 0.55, D * 0.75)
    img = cartel_desaparecidos(img, fotos(), resalta=4 if p > 0 else None, p_resalta=p, cy=800, t=t)
    return img, dict(grain=8, tint=((255, 0, 30), 0.1 * p))

def hermano(t, D, fi):
    habla = seg(t, D * 0.62, D * 0.7)
    gira = ease(seg(t, D * 0.15, D * 0.4))
    pat = math.sin(t * 7) * 12 * habla
    esc, L = estacion(abierto=1.0, dani_kw=dict(head=lerp(0, -6, gira), brazos=(40, 60, lerp(40, 70, habla) + pat, lerp(60, 20, habla))))
    k = ease(min(1, t / D))
    cam = Camara(ojo=(lerp(-0.9, -0.3, k), 1.35, ZP - 0.1), mira=(XB, 1.05, ZD + 0.2), fov=lerp(44, 34, k))
    img = aclarar(esc.render(cam, L), 1.35)
    return img, dict(grain=10, tint=((255, 0, 30), 0.14 * habla), glitch=0.25 if habla and fi % 7 == 0 else 0.0)

def sube(t, D, fi):
    camina = ease(seg(t, 0.0, D * 0.55))
    dentro = t > D * 0.55
    cierra = ease(seg(t, D * 0.62, D * 0.82))
    esc, L = estacion(abierto=1 - cierra)
    if not dentro:
        andres(esc, walk(t, 0.5, 0.55), lerp(-1.4, 1.2, camina), lerp(-0.6, ZP + 0.05, camina), yaw=math.pi / 2 + lerp(0.5, 0.0, camina))
    else:
        sentado(esc, XB, ZS, yaw=-math.pi / 2, ropa=UNIF, piel=PIEL, pantalon=(28, 30, 40), extra_cabeza=gorra(UNIF), head=4)
    cam = Camara(ojo=(-2.7, 1.85, 1.0), mira=(1.4, 1.2, ZP - 0.4), fov=58)
    img = aclarar(esc.render(cam, L), 1.25)
    golpe = D * 0.8 <= t < D * 0.86
    return img, dict(grain=9, glitch=0.4 if golpe else 0.0, flash=((255, 255, 255), 0.35) if golpe else None)

def _cctv_cam():
    return Camara(ojo=(-2.6, 3.3, 11.0), mira=(1.3, 0.2, -8.0), fov=58)

def linterna_suelo(esc):
    _caja_en(esc, -0.95, 0.0, 1.2, -0.85, 0.1, 1.6, (40, 40, 44))
    _caja_en(esc, -0.97, 0.0, 1.6, -0.83, 0.12, 1.66, (255, 250, 220), emite=True, sesgo=0.1)
    return Luz((-0.9, 0.2, 2.2), (255, 240, 200), 2.5, fuerza=1.0)

def camara(t, D, fi):
    va = ease(seg(t, D * 0.1, D * 0.85)) ** 1.6
    luz = 1.0 - seg(t, 0.0, D * 0.2)
    esc, L = estacion(luz_tren=0.15 + 0.85 * luz, dz=-34 * va, faros=0.0)
    if va < 0.4: sentado(esc, XB, ZS - 34 * va, yaw=-math.pi / 2, ropa=UNIF, piel=PIEL, pantalon=(28, 30, 40), extra_cabeza=gorra(UNIF))
    lz = linterna_suelo(esc)
    cam = _cctv_cam()
    img = cctv(aclarar(etiquetas(esc.render(cam, L + [lz]), esc, cam), 1.5, 0.8), 3, "02:41:" + f"{int(5 + t):02d}")
    d = ImageDraw.Draw(img)
    d.text((W / 2, 1290), tr("ANDÉN 1 · LÍNEA 6"), font=font(48), fill=(220, 220, 210), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    img = negro(img, seg(t, D * 0.88, D))
    return img, dict(grain=13, glitch=0.3 if fi % 11 == 0 else 0.0)

def final(t, D, fi):
    img = fondo_anden(12)
    pn = seg(t, 0.1, 0.5)
    img = cartel_desaparecidos(img, fotos(True), nueva=6, p_nueva=pn, resalta=6 if pn >= 1 else None, cy=820, t=t)
    if t > 1.4:
        img = ficha_final(img, G.NOMBRE, G.OFICIO, G.FECHA, G.REGLA, p=ease_back(seg(t, 1.4, 1.9)), t=t, sello=G.SELLO)
    return img, dict(grain=9)

ESCENA_FN = dict(arranque=arranque, anden=anden, puertas=puertas, carteles=carteles, hermano=hermano, sube=sube, camara=camara, final=final)
PAUSA = dict(arranque=0.3, anden=0.3, puertas=0.4, carteles=0.4, hermano=0.5, sube=0.6, camara=0.8, final=1.8)
