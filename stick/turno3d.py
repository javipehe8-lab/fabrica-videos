"""Escenario 3D de "TURNO DE NOCHE": gasolinera Kilómetro 9 en la niebla (motor3d, look PS2).

Sistema de coordenadas (metros): la tienda ocupa x -5..5, z -6..0 (fachada de cristal en z=0, mirando a +z).
Marquesina sobre z 4..10 con surtidores 1-3 en x = -3, 0, 3 (z=7). Carretera a lo largo de x en z 15..21.
Detrás del mostrador (z≈-2.6) está el empleado; los clientes entran por la puerta (x≈-3, z=0).

    esc = mundo(t)                                   # toda la gasolinera
    cliente(esc, pose, x, z, yaw)                    # personajes
    img = esc.render(cam_mostrador(t), luces_base())
    img = cctv(img, 2, "03:19:44")                   # si es un plano de cámara de seguridad
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from motor import *
from motor3d import *

NIEBLA = ((40, 46, 46), 5.0, 30.0)          # color y distancias de la niebla exterior
ASFALTO, ACERA = (52, 54, 56), (84, 84, 80)
PARED, SUELO_T = (150, 146, 132), (120, 122, 116)
ROJO_G, BLANCO = (170, 40, 36), (220, 220, 210)
FLUOR = (240, 250, 230)
SODIO = (255, 180, 90)
UNIFORME = (150, 36, 36)
S4 = (8.6, 7.0)                              # dónde aparece el surtidor 4 (no debería existir)

def _caja_en(esc, x0, y0, z0, x1, y1, z1, col, emite=False, sesgo=0.0):
    esc.add(caja(x1 - x0, y1 - y0, z1 - z0, col), mover((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), emite, sesgo=sesgo)

def surtidor(esc, x, z, num, luz=1.0, col=(200, 200, 194)):
    _caja_en(esc, x - 0.15, 0, z - 0.9, x + 0.15, 0.25, z + 0.9, (110, 110, 104))      # isleta
    _caja_en(esc, x - 0.35, 0.25, z - 0.25, x + 0.35, 1.9, z + 0.25, col)
    _caja_en(esc, x - 0.28, 1.25, z + 0.251, x + 0.28, 1.65, z + 0.27, tuple(int(v * luz) for v in (80, 200, 150)), emite=True)  # pantalla
    _caja_en(esc, x - 0.36, 1.7, z - 0.26, x + 0.36, 1.9, z + 0.26, ROJO_G)
    for s in (-1, 1): _caja_en(esc, x + s * 0.36, 0.8, z - 0.05, x + s * 0.42, 1.2, z + 0.05, (30, 30, 30))  # mangueras
    # número grande en un cartelito blanco (se lee en planos cercanos)
    _caja_en(esc, x - 0.22, 1.92, z - 0.02, x + 0.22, 2.36, z + 0.02, BLANCO, emite=num == 4)
    esc.etiquetas.append(((x, 2.14, z + 0.05), str(num)))

def coche(esc, x, z, yaw=0.0, col=(40, 44, 52), faros=0.0):
    M = cadena(mover(x, 0, z), rot_y(yaw))
    esc.add(caja(1.8, 0.75, 4.2, col, base=True), cadena(M, mover(0, 0.3, 0)))
    esc.add(caja(1.6, 0.6, 2.2, tuple(int(v * 0.7) for v in col), base=True), cadena(M, mover(0, 1.05, -0.3)))
    esc.add(caja(1.55, 0.5, 0.05, (20, 24, 30)), cadena(M, mover(0, 1.35, 0.81)))     # parabrisas
    for sx in (-0.85, 0.85):
        for sz in (-1.4, 1.4): esc.add(caja(0.25, 0.6, 0.6, (14, 14, 14)), cadena(M, mover(sx, 0.3, sz)))
        f = tuple(int(v * faros) for v in (255, 250, 220)) if faros > 0 else (60, 60, 56)
        esc.add(caja(0.35, 0.18, 0.05, f), cadena(M, mover(sx * 0.75, 0.75, 2.11)), emite=faros > 0)

def farola(esc, x, z, on=1.0):
    _caja_en(esc, x - 0.08, 0, z - 0.08, x + 0.08, 6.0, z + 0.08, (70, 70, 72))
    _caja_en(esc, x - 0.08, 5.9, z - 0.08, x + 1.4, 6.05, z + 0.08, (70, 70, 72))
    _caja_en(esc, x + 0.9, 5.75, z - 0.2, x + 1.5, 5.9, z + 0.2, tuple(int(v * on) for v in SODIO), emite=True)

CABINA = (-8.0, 12.0)                       # la cabina de teléfono, junto a la carretera

def cabina(esc, x, z, luz=0.0, vibra=0.0, colgado=True):
    """cabina roja. luz: lámpara del techo (0-1). vibra: el auricular tiembla (suena). colgado=False: auricular descolgado, colgando del cable; None: sin auricular (lo tiene alguien en la mano)"""
    _caja_en(esc, x - 0.5, 0, z - 0.5, x + 0.5, 0.15, z + 0.5, (90, 90, 90))
    for sx, sz in ((-0.45, -0.45), (0.45, -0.45), (-0.45, 0.45), (0.45, 0.45)): _caja_en(esc, x + sx - 0.04, 0.15, z + sz - 0.04, x + sx + 0.04, 2.3, z + sz + 0.04, (150, 40, 36))
    _caja_en(esc, x - 0.5, 2.3, z - 0.5, x + 0.5, 2.5, z + 0.5, (150, 40, 36))
    _caja_en(esc, x - 0.15, 1.2, z - 0.45, x + 0.15, 1.6, z - 0.38, (60, 60, 62))       # teléfono
    if colgado is None: pass                                                             # alguien lo tiene en la mano
    elif colgado:
        _caja_en(esc, x - 0.2 + vibra, 1.62, z - 0.42, x + 0.2 + vibra, 1.7, z - 0.32, (20, 20, 20))   # auricular
    else:
        _caja_en(esc, x + 0.1, 0.55, z - 0.4, x + 0.16, 1.2, z - 0.34, (20, 20, 20))       # colgando del cable
    if luz > 0: _caja_en(esc, x - 0.3, 2.26, z - 0.3, x + 0.3, 2.3, z + 0.3, tuple(int(v * luz) for v in FLUOR), emite=True)

def luz_cabina(f=1.0):
    return Luz((CABINA[0], 2.1, CABINA[1]), (220, 235, 225), 5.0, fuerza=1.4 * f)

def telefono(esc, x=0.2, z=-1.9, pantalla=None, vibra=0.0):
    """teléfono de la tienda sobre el mostrador; pantalla: color de la pantallita (se ilumina al sonar)"""
    _caja_en(esc, x - 0.16, 1.12, z - 0.12, x + 0.16, 1.2, z + 0.12, (40, 40, 44), sesgo=0.7)
    _caja_en(esc, x - 0.17 + vibra, 1.2, z - 0.02, x + 0.17 + vibra, 1.27, z + 0.08, (26, 26, 28), sesgo=0.8)   # auricular
    if pantalla: _caja_en(esc, x - 0.09, 1.201, z - 0.11, x + 0.09, 1.21, z - 0.04, pantalla, emite=True, sesgo=0.9)

def cam_cabina(t=0.0, fov=40, cctv=False):
    """la cabina vista desde la tienda (a través del cristal) o desde la CAM 3"""
    if cctv: return Camara(ojo=(-5.0, 4.3, 10.3), mira=(CABINA[0], 1.1, CABINA[1]), fov=fov)
    return Camara(ojo=(0.6, 1.62, -1.2), mira=(CABINA[0], 1.2, CABINA[1]), fov=fov)

def tienda(esc, luz=1.0):
    # suelo, techo y paredes (fachada con huecos de cristal)
    esc.add(subdividir(plano(10, 6, SUELO_T), 6), mover(0, 0.01, -3), fondo=True)
    esc.add(subdividir(plano(10, 6, (90, 90, 86)), 6), cadena(mover(0, 3.0, -3), rot_x(math.pi)))
    esc.add(subdividir(pared(10, 3, PARED), 6), mover(0, 0, -6))
    esc.add(subdividir(pared(6, 3, PARED), 4), cadena(mover(-5, 0, -3), rot_y(math.pi / 2)))
    esc.add(subdividir(pared(6, 3, PARED), 4), cadena(mover(5, 0, -3), rot_y(-math.pi / 2)))
    # fachada: zócalo, dintel y pilares; cristal = huecos (se ve la niebla de fuera)
    _caja_en(esc, -5, 0, -0.1, 5, 0.8, 0.1, PARED)
    _caja_en(esc, -5, 2.4, -0.1, 5, 3.0, 0.1, PARED)
    for px in (-5, -3.8, -2.2, 0.5, 3, 5): _caja_en(esc, px - 0.08, 0.8, -0.1, px + 0.08, 2.4, 0.1, (60, 62, 64))
    _caja_en(esc, -3.7, 0, -0.06, -2.3, 0.8, 0.06, (60, 62, 64))                          # hueco de la puerta (sin zócalo)
    # rótulo exterior sobre la fachada
    _caja_en(esc, -4.6, 3.06, 0.0, 4.6, 3.7, 0.25, ROJO_G)
    _caja_en(esc, -4.4, 3.12, 0.251, 4.4, 3.6, 0.27, tuple(int(v * luz) for v in (250, 240, 220)), emite=True)
    esc.etiquetas.append(((0, 3.35, 0.3), "KILÓMETRO 9 · 24H"))
    # mostrador y caja
    _caja_en(esc, -0.5, 0, -2.2, 3.5, 1.05, -1.6, (110, 70, 50))
    _caja_en(esc, -0.55, 1.05, -2.25, 3.55, 1.12, -1.55, (180, 176, 168), sesgo=0.4)
    _caja_en(esc, 1.6, 1.12, -2.0, 2.2, 1.45, -1.7, (40, 40, 44), sesgo=0.6)             # caja registradora
    _caja_en(esc, 1.65, 1.45, -1.95, 2.15, 1.75, -1.85, (30, 30, 34))
    _caja_en(esc, 1.7, 1.5, -1.849, 2.1, 1.7, -1.84, tuple(int(v * luz) for v in (90, 220, 160)), emite=True)
    # monitor de las cámaras, detrás del mostrador
    _caja_en(esc, 2.6, 1.12, -2.1, 3.3, 1.6, -1.8, (30, 30, 30))
    _caja_en(esc, 2.65, 1.17, -1.799, 3.25, 1.55, -1.79, tuple(int(v * luz) for v in (120, 140, 130)), emite=True)
    # estanterías con productos de colores
    cols = [(180, 60, 50), (60, 120, 180), (220, 180, 60), (80, 160, 90), (200, 120, 160)]
    for k, sx in enumerate((-4.2, -2.6)):
        for sz in (-5.0, -3.6):
            _caja_en(esc, sx - 0.3, 0, sz - 0.6, sx + 0.3, 1.7, sz + 0.6, (90, 90, 96))
            for nivel in range(3):
                for j in range(3):
                    c = cols[(k + nivel + j) % 5]
                    _caja_en(esc, sx - 0.32, 0.35 + nivel * 0.5, sz - 0.5 + j * 0.35, sx + 0.32, 0.6 + nivel * 0.5, sz - 0.25 + j * 0.35, c)
    # nevera iluminada al fondo
    _caja_en(esc, 1.0, 0, -5.95, 4.5, 2.2, -5.3, (60, 62, 66))
    _caja_en(esc, 1.1, 0.2, -5.299, 4.4, 2.1, -5.28, tuple(int(v * luz) for v in (150, 190, 210)), emite=True)
    # fluorescentes del techo
    for fx in (-3, 0, 3):
        for fz in (-4.5, -1.5): _caja_en(esc, fx - 0.8, 2.95, fz - 0.1, fx + 0.8, 2.99, fz + 0.1, tuple(int(v * luz) for v in FLUOR), emite=luz > 0.1)

def exterior(esc, luz=1.0, surtidor4=0.0, coche4=0.0, cabina_kw=None):
    esc.add(subdividir(plano(60, 30, ASFALTO), 12), mover(0, 0, 10), fondo=True)
    esc.add(subdividir(plano(60, 6, (40, 42, 44)), 10), mover(0, 0.005, 18), fondo=True)  # carretera
    for k in range(-6, 7): _caja_en(esc, k * 4 - 1, 0.01, 17.92, k * 4 + 1, 0.02, 18.08, (200, 200, 190))
    # marquesina
    _caja_en(esc, -6, 4.4, 3.5, 6, 4.9, 10.5, (200, 200, 196))
    _caja_en(esc, -6.02, 4.4, 3.48, 6.02, 4.9, 3.6, ROJO_G); _caja_en(esc, -6.02, 4.4, 10.4, 6.02, 4.9, 10.52, ROJO_G)
    for lx in (-4, -1.3, 1.3, 4):
        for lz in (5, 9): _caja_en(esc, lx - 0.5, 4.38, lz - 0.3, lx + 0.5, 4.4, lz + 0.3, tuple(int(v * luz) for v in FLUOR), emite=luz > 0.1)
    for cx in (-5.4, 5.4):
        for cz in (5.0, 9.0): _caja_en(esc, cx - 0.18, 0, cz - 0.18, cx + 0.18, 4.4, cz + 0.18, (180, 180, 176))
    for i, x in enumerate((-3, 0, 3)): surtidor(esc, x, 7, i + 1, luz)
    farola(esc, 8, 14, luz); cabina(esc, *CABINA, **(cabina_kw or {}))
    # el surtidor 4: no debería existir (aparece en la niebla, al borde de la luz)
    # al final de la fila, fuera de la marquesina, donde ya no llega la luz
    if surtidor4 > 0:
        surtidor(esc, S4[0], S4[1], 4, 0.6 * surtidor4, col=tuple(int(v * (0.4 + 0.6 * surtidor4)) for v in (150, 128, 104)))
    if coche4 > 0: coche(esc, S4[0] + 2.2, S4[1] + 1.4, yaw=-math.pi / 2 - 0.25, col=(26, 28, 32), faros=coche4 if coche4 > 1 else 0)

def mundo(t=0.0, luz=1.0, surtidor4=0.0, coche4=0.0, cabina_kw=None):
    """cabina_kw: opciones de la cabina, p. ej. dict(luz=1, vibra=0.02) cuando suena"""
    esc = Escena(niebla=NIEBLA, amb=0.16)
    esc.etiquetas = []
    tienda(esc, luz); exterior(esc, luz, surtidor4, coche4, cabina_kw)
    return esc

def luces_base(luz=1.0, extra=()):
    L_ = []
    if luz > 0:
        for fx in (-3, 0, 3): L_.append(Luz((fx, 2.8, -3), FLUOR, 6.5, fuerza=0.8 * luz))
        for lx in (-3, 0, 3): L_.append(Luz((lx, 4.2, 7), FLUOR, 8.0, fuerza=0.9 * luz))
        L_.append(Luz((9.2, 5.6, 14), SODIO, 9.0, fuerza=0.7 * luz))
    return L_ + list(extra)

# ---------- el aseo (pared del fondo de la tienda) ----------
ASEO = (-1.1, -5.95)                         # centro de la puerta del aseo (x, z de la pared)

def aseo(esc, luz_dentro=0.0, tirador=0.0, agua=0.0, cartel=True):
    """puerta del aseo en la pared del fondo. luz_dentro: rendija de luz bajo la puerta (0-1).
    tirador: desplazamiento del pomo (alguien lo mueve desde dentro). agua: charco que sale por debajo (0-1). cartel: AVERIADO"""
    x, z = ASEO
    _caja_en(esc, x - 0.6, 0, z, x + 0.6, 2.25, z + 0.06, (70, 72, 74), sesgo=0.4)         # marco
    _caja_en(esc, x - 0.5, 0.035, z + 0.06, x + 0.5, 2.15, z + 0.1, (92, 118, 140), sesgo=0.5)   # puerta
    _caja_en(esc, x + 0.32, 0.98 + tirador, z + 0.1, x + 0.42, 1.04 + tirador, z + 0.18, (200, 196, 180), sesgo=0.8)  # pomo
    if luz_dentro > 0: _caja_en(esc, x - 0.48, 0.0, z + 0.07, x + 0.48, 0.035, z + 0.1, tuple(int(v * luz_dentro) for v in (230, 240, 220)), emite=True, sesgo=0.7)
    # placa ASEO sobre la puerta
    _caja_en(esc, x - 0.35, 2.3, z + 0.01, x + 0.35, 2.55, z + 0.05, BLANCO, sesgo=0.5)
    esc.etiquetas.append(((x, 2.425, z + 0.08), "ASEO", 0.17, (30, 60, 120)))
    if cartel:                                                                              # folio pegado con celo
        _caja_en(esc, x - 0.34, 1.38, z + 0.1, x + 0.34, 1.72, z + 0.115, (236, 234, 224), sesgo=0.9)
        esc.etiquetas.append(((x, 1.55, z + 0.13), "AVERIADO", min(0.1, 0.56 / (0.62 * len(tr("AVERIADO")))), (200, 30, 30)))
    if agua > 0:                                                                            # charco que sale por debajo
        r = 0.2 + 0.9 * agua
        _caja_en(esc, x - 0.45 * (0.5 + agua), 0.012, z + 0.1, x + 0.45 * (0.5 + agua), 0.016, z + 0.1 + r, (66, 80, 92), sesgo=0.6)

def huellas(esc, pts, col=(78, 86, 88)):
    """huellas mojadas en el suelo (lista de (x, z, yaw))"""
    for k, (x, z, yaw) in enumerate(pts):
        lado = 0.07 if k % 2 else -0.07
        M = cadena(mover(x + lado * math.cos(yaw), 0.013, z - lado * math.sin(yaw)), rot_y(yaw))
        esc.add(caja(0.09, 0.004, 0.17, col), M, sesgo=0.2)

def mano_llave(esc, x=1.25, y=1.3, z=-2.15, brillo=1.0):
    """tu mano con la palma hacia arriba y la llave del aseo (con su llavero rojo) encima"""
    piel = (190, 160, 140)
    _caja_en(esc, x - 0.06, y - 0.04, z - 0.32, x + 0.06, y + 0.02, z - 0.06, UNIFORME, sesgo=0.6)      # manga
    _caja_en(esc, x - 0.06, y - 0.02, z - 0.08, x + 0.06, y + 0.01, z + 0.05, piel, sesgo=0.7)          # palma
    for k in range(4): _caja_en(esc, x - 0.055 + k * 0.03, y - 0.015, z + 0.05, x - 0.035 + k * 0.03, y + 0.015, z + 0.13, piel, sesgo=0.7)
    _caja_en(esc, x - 0.1, y - 0.015, z - 0.04, x - 0.06, y + 0.015, z + 0.04, piel, sesgo=0.7)         # pulgar
    m = tuple(int(min(255, v * brillo)) for v in (190, 186, 160))
    _caja_en(esc, x - 0.008, y + 0.012, z - 0.06, x + 0.008, y + 0.024, z + 0.04, m, sesgo=0.9)   # caña de la llave
    _caja_en(esc, x - 0.025, y + 0.012, z + 0.04, x + 0.025, y + 0.024, z + 0.08, m, sesgo=0.9)   # cabeza
    _caja_en(esc, x - 0.03, y + 0.012, z - 0.16, x + 0.03, y + 0.03, z - 0.06, (180, 36, 34), sesgo=0.9)  # llavero
    esc.etiquetas.append(((x, y + 0.035, z - 0.11), "ASEO", 0.022, (245, 240, 230)))

# ---------- personajes ----------
def empleado(esc, p, x=1.2, z=-2.6, yaw=0.0, cara="neutral"):
    """tú: el empleado (uniforme rojo y gorra). Se ve poco: de espaldas, en cámaras o de lejos."""
    def gorra(e, cab, u):
        e.add(esfera(u(26), UNIFORME, 1), cadena(cab, mover(0, u(10), 0), escala(1, 0.55, 1)))
        e.add(caja(u(36), u(4), u(22), UNIFORME), cadena(cab, mover(0, u(8), u(24))))
    return humano(esc, p, x=x, z=z, yaw=yaw, ropa=UNIFORME, piel=(206, 190, 172), pantalon=(40, 42, 50), cara=cara, extra_cabeza=gorra)

def cliente(esc, p, x, z, yaw=0.0, cara="neutral", alto=1.0, abrigo=(60, 64, 58), piel=(196, 186, 176), capucha=True):
    """cliente con chubasquero largo (y capucha): la figura típica que entra de la niebla"""
    def cap(e, cab, u):
        if capucha:
            e.add(esfera(u(32), abrigo, 1), cadena(cab, mover(0, u(6), -u(8)), escala(1.08, 1.05, 1.0)))
    cab = humano(esc, p, x=x, z=z, yaw=yaw, ropa=abrigo, piel=piel, pantalon=(36, 38, 40), alto=alto, cara=cara, extra_cabeza=cap)
    s = alto * 1.75 / 3.06; u = lambda v: v / 100 * s
    # faldón del chubasquero (de la cintura a las rodillas)
    base = cadena(mover(x, 0, z), rot_y(yaw), mover(0, u(L["ul"] + L["ll"] + 6), 0))
    esc.add(prisma(u(24), u(30), u(80), tuple(int(v * 0.92) for v in abrigo), n=6), base)
    return cab

def nina(esc, p, x, z, yaw=0.0, cara="neutral", abrigo=(196, 160, 40)):
    """niña pequeña con chubasquero amarillo y capucha (empapada)"""
    return cliente(esc, p, x, z, yaw=yaw, cara=cara, alto=0.66, abrigo=abrigo, piel=(214, 204, 198))

# ---------- cámaras típicas ----------
def cam_llegada(t, D):
    k = ease(min(1, t / D))
    return Camara(ojo=(lerp(-14, -7, k), lerp(2.2, 1.8, k), lerp(26, 19, k)), mira=(0, 1.8, 3), fov=55)

def cam_mostrador(t, mira=(-3, 1.4, 1.0), fov=55, temblor=0.01):
    """plano subjetivo: tú, detrás del mostrador"""
    return Camara(ojo=(1.4 + temblor * math.sin(t * 1.7), 1.62 + temblor * math.sin(t * 2.3), -2.7), mira=mira, fov=fov)

def cam_cctv(n):
    """CAM 1 tienda (esquina alta), CAM 2 surtidores (desde la fachada), CAM 3 carretera"""
    if n == 1: return Camara(ojo=(4.6, 2.85, -0.4), mira=(-1, 0.6, -3.5), fov=70)
    if n == 2: return Camara(ojo=(-6.2, 4.0, 2.6), mira=(6.5, 0.8, 7.2), fov=60)
    return Camara(ojo=(8, 5.5, 14), mira=(-4, 0.5, 19), fov=60)

# ---------- 2D: etiquetas 3D, cámaras de seguridad, la hoja de reglas ----------
def proyectar(cam, p):
    Vm = cam.vista(); x, y, z = (Vm @ np.array([*p, 1.0]))[:3]
    if z > -0.1: return None
    f = 1 / math.tan(math.radians(cam.fov) / 2); asp = RW / RH
    return ((x * f / asp / -z * 0.5 + 0.5) * W, (-y * f / -z * 0.5 + 0.5) * H, -z)

def etiquetas(img, esc, cam, luz=1.0):
    """números de los surtidores y rótulo, dibujados encima con tamaño según la distancia"""
    d = ImageDraw.Draw(img)
    for e in esc.etiquetas:
        p, txt = e[0], e[1]                                               # (pos, texto[, alto en metros[, color]])
        q = proyectar(cam, p)
        if not q or q[2] > 24: continue
        f = 1 / math.tan(math.radians(cam.fov) / 2)
        alto_m = e[2] if len(e) > 2 else (0.32 if len(txt) <= 2 else 0.4)   # altura real del texto en metros
        size = int(min(220, alto_m / q[2] * f * H / 2))
        if size < 10: continue
        a = max(0.0, 1 - q[2] / 24)
        c0 = e[3] if len(e) > 3 else ((20, 20, 20) if len(txt) <= 2 else (200, 40, 36))
        col = tuple(int(lerp(f_, c_, a)) for f_, c_ in zip(NIEBLA[0], c0))
        d.text((q[0], q[1]), tr(txt), font=font(size), fill=col, anchor="mm")
    return img

def cctv(img, n, hora, rec=True):
    """convierte un plano en imagen de cámara de seguridad: blanco y negro, contraste, hora y número de cámara"""
    g = img.convert("L").point(lambda v: min(255, int(v * 1.25 + 8)))
    im = Image.merge("RGB", (g, g, g))
    d = ImageDraw.Draw(im)
    d.text((70, 260), f"CAM {n}", font=font(64), fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
    d.text((W - 70, 260), hora, font=font(56), fill=(255, 255, 255), anchor="ra", stroke_width=4, stroke_fill=(0, 0, 0))
    if rec:
        d.ellipse((70, 360, 110, 400), fill=(230, 30, 30)); d.text((125, 380), "REC", font=font(48), fill=(255, 255, 255), anchor="lm")
    return im

def _envolver(d, txt, fnt, ancho):
    lineas, cur = [], ""
    for w_ in txt.split():
        prueba = (cur + " " + w_).strip()
        if d.textlength(prueba, font=fnt) <= ancho: cur = prueba
        else: lineas.append(cur); cur = w_
    if cur: lineas.append(cur)
    return lineas

def hoja_reglas(img, t, lineas, resalta=None, nota=None, nota_p=0.0, zoom=1.0, cy=None, h_extra=0):
    """la hoja plastificada de reglas en primer plano (plano subjetivo).
    lineas: textos de las reglas; "?" = regla tachada con rotulador (aún no se ha descubierto).
    resalta: índice de la regla del episodio (fondo amarillo). nota: texto a mano al pie, que se escribe según nota_p (0-1)."""
    d = ImageDraw.Draw(img)
    cx = W / 2; cy = cy or 860
    w, h = 900 * zoom, (1120 + h_extra) * zoom          # h_extra: hoja más larga cuando ya hay muchas reglas
    x0, y0 = cx - w / 2, cy - h / 2
    d.rectangle((x0 + 18, y0 + 22, x0 + w + 18, y0 + h + 22), fill=(10, 10, 10))
    d.rectangle((x0, y0, x0 + w, y0 + h), fill=(226, 222, 204), outline=(120, 118, 100), width=6)
    d.text((cx, y0 + 80 * zoom), tr("REGLAS DEL TURNO DE NOCHE"), font=font(int(50 * zoom)), fill=(150, 30, 30), anchor="mm")
    y = y0 + 170 * zoom
    fnt = font(int(44 * zoom))
    for i, ln in enumerate(lineas):
        d.text((x0 + 40 * zoom, y), f"{i + 1}.", font=fnt, fill=(30, 30, 34), anchor="la")
        if ln == "?":
            d.rectangle((x0 + 100 * zoom, y + 4 * zoom, x0 + w - 50 * zoom, y + 46 * zoom), fill=(24, 24, 28))
            y += 80 * zoom; continue
        ls = _envolver(d, tr(ln), fnt, w - 160 * zoom)
        if resalta == i:
            d.rectangle((x0 + 90 * zoom, y - 6 * zoom, x0 + w - 40 * zoom, y + len(ls) * 56 * zoom + 4 * zoom), fill=(250, 230, 90))
        for k, l_ in enumerate(ls):
            d.text((x0 + 100 * zoom, y + k * 56 * zoom), l_, font=fnt, fill=(30, 30, 34), anchor="la")
        y += len(ls) * 56 * zoom + 30 * zoom
    if nota and nota_p > 0:      # nota escrita a mano al pie (se "escribe" poco a poco)
        txt = tr(nota); n = max(1, int(len(txt) * min(1, nota_p)))
        d.text((x0 + 70 * zoom, y0 + h - 120 * zoom), txt[:n], font=font(int(58 * zoom)), fill=(40, 60, 160), anchor="lm")
    return img

# ---------- piezas añadidas en la Parte 4 ----------
def anciano(esc, p, x, z, yaw=0.0, cara="neutral", abrigo=(92, 74, 56), pelo=(188, 186, 180)):
    """anciano encorvado con abrigo largo de otra época, pelo canoso y boina (seco, aunque fuera haya niebla)"""
    def boina(e, cab, u):
        e.add(esfera(u(27), (52, 48, 46), 1), cadena(cab, mover(0, u(14), -u(2)), escala(1.1, 0.42, 1.12)))
    p = add(p, pose(body=9, head=-7))
    cab = humano(esc, p, x=x, z=z, yaw=yaw, ropa=abrigo, piel=(200, 182, 168), pantalon=(56, 52, 48), alto=0.95, cara=cara, pelo=pelo, extra_cabeza=boina)
    s = 0.95 * 1.75 / 3.06; u = lambda v: v / 100 * s
    base = cadena(mover(x, 0, z), rot_y(yaw), mover(0, u(L["ul"] + L["ll"] + 6), 0))
    esc.add(prisma(u(24), u(31), u(85), tuple(int(v * 0.9) for v in abrigo), n=6), base)
    return cab

def monedas(esc, pts, col=(196, 168, 92), r=0.03, texto=None):
    """monedas sobre una superficie: pts = [(x, y, z)]; texto: lo que se lee en cada una (p. ej. "1986")"""
    for (x, y, z) in pts:
        esc.add(prisma(r, r, 0.006, col, n=10), mover(x, y + 0.006, z), sesgo=0.9)
        if texto: esc.etiquetas.append(((x, y + 0.008, z), texto, r * 0.42, (90, 70, 30)))

def tabaco(esc, x, z, y=1.12):
    """paquete de tabaco antiguo sobre el mostrador"""
    _caja_en(esc, x - 0.045, y, z - 0.03, x + 0.045, y + 0.13, z + 0.03, (220, 214, 196), sesgo=0.8)
    _caja_en(esc, x - 0.046, y + 0.07, z - 0.031, x + 0.046, y + 0.11, z + 0.031, (170, 40, 36), sesgo=0.85)

CAJA_REG = (1.9, -1.85)                      # centro de la caja registradora (x, z)

def caja_registradora(esc, fecha=None, cajon=0.0, pesetas=0, luz=1.0, fecha_col=(110, 240, 170)):
    """lado del empleado de la caja: pantalla trasera con la fecha (etiqueta) y el cajón, que se abre hacia ti (cajon 0-1).
    pesetas: cuántas monedas antiguas hay en el cajón (0 = cajón vacío)"""
    x, z = CAJA_REG
    _caja_en(esc, 1.7, 1.5, -1.962, 2.1, 1.7, -1.952, tuple(int(v * 0.35 * luz) for v in fecha_col), emite=True, sesgo=0.9)
    if fecha: esc.etiquetas.append(((x, 1.6, -1.97), fecha, 0.045, fecha_col))
    if cajon > 0:
        z0 = -2.0 - 0.38 * cajon
        _caja_en(esc, 1.58, 1.13, z0, 2.22, 1.15, z0 + 0.36, (36, 36, 40), sesgo=0.7)          # fondo
        _caja_en(esc, 1.58, 1.15, z0, 2.22, 1.24, z0 + 0.012, (46, 46, 50), sesgo=0.75)        # frente
        for k in range(1, 4): _caja_en(esc, 1.58 + k * 0.16 - 0.004, 1.15, z0, 1.58 + k * 0.16 + 0.004, 1.2, z0 + 0.36, (60, 60, 64), sesgo=0.75)
        r_ = __import__("random").Random(4)
        pts = [(1.58 + 0.08 + 0.16 * (i % 4) + r_.uniform(-0.035, 0.035), 1.15 + 0.008 * (i // 8), z0 + 0.05 + r_.uniform(0, 0.27)) for i in range(pesetas)]
        cols = [(196, 168, 92), (170, 170, 164), (206, 176, 80)]
        for i, (px, py, pz) in enumerate(pts):
            esc.add(prisma(0.022, 0.022, 0.005, cols[i % 3], n=8), mover(px, py + 0.005, pz), sesgo=0.95)

# ---------- piezas añadidas en la Parte 5 ----------
PUERTA_T = (-3.0, 0.0)                       # puerta de la tienda (x, z de la fachada)

def niebla_suelo(esc, k, origen=PUERTA_T, alcance=7.5, alto=0.4, col=(150, 158, 156), emite=False, t=0.0, semilla=5, n=90):
    """niebla baja que entra por debajo de la puerta y se extiende por el suelo de la tienda.
    k: cuánto ha avanzado (0-1). Jirones = cajas planas de distintos tamaños; con emite=True brillan un poco (para planos a oscuras)."""
    if k <= 0: return
    r_ = __import__("random").Random(semilla)
    for i in range(n):
        ang = r_.uniform(-math.pi * 0.95, -math.pi * 0.05)                 # hacia dentro de la tienda (z < 0)
        d = r_.uniform(0, 1) ** 0.8 * alcance
        if d > k * alcance: continue
        x = origen[0] + math.cos(ang) * d * 1.15 + 0.12 * math.sin(t * 0.7 + i)
        z = origen[1] + math.sin(ang) * d * 0.8 - 0.1
        if not (-4.9 < x < 4.9 and -5.9 < z < -0.05): continue
        w_, dd = r_.uniform(0.9, 2.0), r_.uniform(0.6, 1.4)
        h_ = alto * r_.uniform(0.15, 1.0) * min(1.0, 0.4 + k) * max(0.35, 1 - d / alcance * 0.6)
        c = tuple(int(v * r_.uniform(0.85, 1.05)) for v in col)
        esc.add(caja(w_, h_, dd, c, base=True), cadena(mover(x, 0.0, z), rot_y(r_.uniform(0, math.pi))), emite, sesgo=0.05)

def luz_figura(x, z, yaw, f=1.0, y=1.5):
    """resplandor frío y débil que desprende la figura de niebla (ilumina su parte delantera)"""
    return Luz((x + 0.9 * math.sin(yaw), y, z + 0.9 * math.cos(yaw)), (170, 190, 190), 2.6, fuerza=0.9 * f)

def figura_niebla(esc, p, x, z, yaw=0.0, col=(118, 126, 124), gorra=True, alto=1.08, brillo=1.0, emite=True):
    """una silueta hecha de niebla, sin cara (brilla débilmente: se ve a oscuras). gorra=True: tiene la forma de la gorra del uniforme"""
    c = tuple(int(min(255, v * brillo)) for v in col)
    def gor(e, cab, u):
        if gorra:
            e.add(esfera(u(26), c, 1), cadena(cab, mover(0, u(10), 0), escala(1, 0.55, 1)))
            e.add(caja(u(36), u(4), u(22), c), cadena(cab, mover(0, u(8), u(24))))
    n0 = len(esc.objs)
    cab = humano(esc, p, x=x, z=z, yaw=yaw, ropa=c, piel=c, pantalon=c, alto=alto, cara="ninguna", extra_cabeza=gor)
    if emite:
        for i in range(n0, len(esc.objs)):
            m, M, _, f, s = esc.objs[i]
            esc.objs[i] = (m, M, True, f, s)
    return cab

def vaho(img, texto, cx, cy, size=120, p=1.0, rot=-6, ancho=None):
    """texto escrito con el dedo en el vaho de un cristal o plástico: mancha blanquecina + letras borrosas (p: 0-1 aparece)"""
    if p <= 0: return img
    from PIL import ImageFilter
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    fnt = font(size)
    txt = tr(texto)
    while ancho and d.textlength(txt, font=fnt) > ancho and size > 30:
        size -= 4; fnt = font(size)
    tw = d.textlength(txt, font=fnt)
    d.ellipse((cx - tw / 2 - 120, cy - size * 1.5, cx + tw / 2 + 120, cy + size * 1.5), fill=(214, 222, 220, int(225 * min(1, p * 2))))
    capa = capa.filter(ImageFilter.GaussianBlur(45))
    letras = Image.new("RGBA", img.size, (0, 0, 0, 0))
    n = max(1, int(len(txt) * min(1.0, p * 1.4)))
    dl = ImageDraw.Draw(letras)
    dl.text((cx + 5, cy + 6), txt[:n], font=fnt, fill=(40, 50, 50, int(150 * min(1, p * 1.5))), anchor="mm")     # surco más oscuro
    dl.text((cx, cy), txt[:n], font=fnt, fill=(255, 255, 255, int(255 * min(1, p * 1.5))), anchor="mm")
    letras = letras.rotate(rot, center=(cx, cy), resample=Image.BICUBIC).filter(ImageFilter.GaussianBlur(3))
    out = Image.alpha_composite(Image.alpha_composite(img.convert("RGBA"), capa), letras)
    return out.convert("RGB")

def render_niebla(esc, cam, luces, k, alfa=0.75, desenfoque=10, **kw):
    """renderiza la escena con la niebla baja SEMITRANSPARENTE: se dibuja con y sin niebla y se mezclan
    (la niebla, desenfocada, se funde con lo que hay detrás). kw: opciones de niebla_suelo (t, col, emite, origen...)"""
    from PIL import ImageFilter, ImageChops
    limpio = esc.render(cam, luces)
    n0 = len(esc.objs)
    niebla_suelo(esc, k, **kw)
    if len(esc.objs) == n0: return limpio
    con = esc.render(cam, luces)
    del esc.objs[n0:]
    dif = ImageChops.difference(limpio, con).convert("L").point(lambda v: 255 if v > 6 else 0)
    mask = dif.filter(ImageFilter.GaussianBlur(desenfoque * 2.5)).point(lambda v: int(v * alfa))
    return Image.composite(con.filter(ImageFilter.GaussianBlur(desenfoque)), limpio, mask)

def cam_puerta_cctv():
    """CAM 1 girada hacia la puerta: desde la esquina alta de la derecha, a lo largo de la cristalera"""
    return Camara(ojo=(4.7, 2.8, -0.5), mira=(-3.0, 0.2, -1.0), fov=62)

# ---------- arranque (desde la Parte 6): el primer segundo tiene que parar el scroll ----------
def aclarar(img, k=1.35, gamma=0.8):
    """sube la exposición de un plano 3D (en el móvil los planos oscuros con niebla se ven como una mancha gris)"""
    import numpy as _np
    a = _np.asarray(img).astype(_np.float32) / 255.0
    a = _np.clip((a ** gamma) * k, 0, 1)
    return Image.fromarray((a * 255).astype(_np.uint8))

def rotulo_regla(img, n, texto, p=1.0, y=430, col=(235, 40, 40)):
    """'REGLA N' + la regla en grande sobre el plano de arranque (p: 0-1 para la animación de entrada).
    Va en la zona alta, lejos de los subtítulos (y > 1300)."""
    if p <= 0: return img
    d = ImageDraw.Draw(img)
    s = 0.6 + 0.4 * min(1.0, p)
    d.text((W / 2, y - 120 * s), f"{tr('REGLA')} {n}", font=font(int(120 * s)), fill=col, anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
    fnt = font(int(64 * s))
    lineas = _envolver(d, tr(texto), fnt, W - 140)
    for i, ln in enumerate(lineas[:3]):
        d.text((W / 2, y + i * 78 * s), ln, font=fnt, fill=(255, 255, 255), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    return img

# ---------- piezas añadidas en la Parte 6: el coche familiar, los pasajeros y el cuaderno de Raúl ----------
ASIENTOS = {"conductor": (0.42, 0.05), "copiloto": (-0.42, 0.05), "detras_izq": (0.42, -1.0), "detras_der": (-0.42, -1.0)}

def coche_familiar(esc, x, z, yaw=0.0, col=(58, 70, 86), faros=0.0, pilotos=0.0, ventanilla=1.0):
    """turismo familiar con la cabina ABIERTA (montantes y techo, sin cristales) para ver quién va dentro.
    Mira hacia +z local; el conductor va a la izquierda (+x local). pilotos: luces rojas de atrás (0-1).
    ventanilla: 1 = ventanilla del conductor bajada (las demás llevan un cristal oscuro hasta media altura)."""
    M = cadena(mover(x, 0, z), rot_y(yaw))
    oscuro = tuple(int(v * 0.6) for v in col)
    esc.add(caja(1.8, 0.62, 4.3, col, base=True), cadena(M, mover(0, 0.36, 0)))                  # carrocería (0.36-0.98)
    esc.add(caja(1.82, 0.08, 4.32, (30, 30, 32), base=True), cadena(M, mover(0, 0.3, 0)))        # bajos
    esc.add(caja(1.7, 0.04, 2.3, (34, 32, 30), base=True), cadena(M, mover(0, 0.97, -0.45)))     # suelo/interior oscuro
    # techo y montantes
    esc.add(caja(1.62, 0.07, 2.25, col, base=True), cadena(M, mover(0, 1.6, -0.45)))
    for sx in (-0.78, 0.78):
        for sz, inc in ((0.7, 0.35), (-0.4, 0.0), (-1.55, -0.3)):
            esc.add(caja(0.07, 0.64, 0.08, oscuro, base=True), cadena(M, mover(sx, 0.98, sz), rot_x(inc)))
    esc.add(caja(1.55, 0.04, 0.6, (24, 28, 34)), cadena(M, mover(0, 1.3, 0.85), rot_x(-0.95)))   # parabrisas (oscuro)
    # asientos (respaldos) y volante
    for n_, (sx, sz) in ASIENTOS.items():
        esc.add(caja(0.5, 0.62, 0.12, (46, 44, 48), base=True), cadena(M, mover(sx, 0.95, sz - 0.3), rot_x(-0.15)))
        esc.add(caja(0.26, 0.14, 0.1, (46, 44, 48), base=True), cadena(M, mover(sx, 1.58, sz - 0.38)))   # reposacabezas
    esc.add(prisma(0.17, 0.17, 0.03, (24, 24, 26), n=8), cadena(M, mover(0.42, 1.15, 0.5), rot_x(-1.2)))
    # cristales bajos de las otras puertas (medio subidos)
    for sx, sz, d in ((-0.81, 0.15, 1.0), (-0.81, -0.98, 1.0), (0.81, -0.98, 1.0)):
        esc.add(caja(0.02, 0.22, d, (40, 50, 58)), cadena(M, mover(sx, 1.09, sz)))
    if ventanilla < 1: esc.add(caja(0.02, 0.5 * (1 - ventanilla), 1.0, (40, 50, 58)), cadena(M, mover(0.81, 0.98 + 0.25 * (1 - ventanilla), 0.15)))
    for sx in (-0.86, 0.86):                                                                     # ruedas
        for sz in (-1.35, 1.35): esc.add(caja(0.25, 0.62, 0.62, (14, 14, 14)), cadena(M, mover(sx, 0.31, sz)))
        f = tuple(int(v * faros) for v in (255, 250, 220)) if faros > 0 else (70, 70, 64)
        esc.add(caja(0.38, 0.16, 0.05, f), cadena(M, mover(sx * 0.72, 0.78, 2.16)), emite=faros > 0)
        r = tuple(int(v * (0.3 + 0.7 * pilotos)) for v in (255, 40, 30))
        esc.add(caja(0.38, 0.14, 0.05, r), cadena(M, mover(sx * 0.72, 0.8, -2.16)), emite=pilotos > 0)
    esc.add(caja(0.5, 0.12, 0.02, (210, 210, 200)), cadena(M, mover(0, 0.62, -2.17)))           # matrícula
    return M

def pasajero(esc, M, asiento, ropa=(70, 60, 80), piel=(200, 186, 172), alto=1.0, cara="neutral", pelo=None,
             mira=0.0, brazo=None, extra_cabeza=None, gira=0.0):
    """alguien sentado en el coche M (de coche_familiar), sin piernas (quedan dentro de la carrocería).
    mira: ladea la cabeza (grados); gira: gira el cuerpo hacia la ventanilla (rad). brazo: pose del brazo derecho (a2u, a2l)"""
    sx, sz = ASIENTOS[asiento]
    s = alto * 1.75 / 3.06
    cad = 1.36 * s                                   # altura de la cadera de pie
    p = pose(head=mira, a1u=40, a1l=60, a2u=40, a2l=60)
    if brazo: p.update(a2u=brazo[0], a2l=brazo[1])
    Mw = cadena(M, mover(sx, 0, sz))
    # humano trabaja en coordenadas del mundo: sacamos posición y giro de la matriz
    px, py, pz = (Mw @ np.array([0, 0, 0, 1.0]))[:3]
    yaw = math.atan2(M[0, 2], M[2, 2]) + gira
    n0 = len(esc.objs)
    cab = humano(esc, p, x=px, z=pz, y=0.6 + (1 - alto) * 0.55 - cad, yaw=yaw, ropa=ropa, piel=piel, pantalon=ropa, alto=alto, cara=cara, pelo=pelo, extra_cabeza=extra_cabeza)
    del esc.objs[-6:]                                # fuera las piernas (las 6 últimas piezas)
    return cab

def capucha(col):
    """extra_cabeza: capucha del chubasquero (para la niña)"""
    def f(e, cab, u): e.add(esfera(u(32), col, 1), cadena(cab, mover(0, u(6), -u(8)), escala(1.08, 1.05, 1.0)))
    return f

def cuaderno3d(esc, x, y, z, yaw=0.0, abierto=False, col=(40, 70, 60)):
    """el cuaderno de Raúl en 3D (tapas verdes, hojas onduladas por el agua); se ve 'RAÚL' en la tapa"""
    M = cadena(mover(x, y, z), rot_y(yaw))
    esc.add(caja(0.22, 0.03, 0.3, col), M, sesgo=0.6)
    esc.add(caja(0.2, 0.026, 0.29, (214, 208, 186)), cadena(M, mover(0.012, 0.0, 0)), sesgo=0.65)
    esc.add(caja(0.22, 0.004, 0.3, col), cadena(M, mover(0, 0.017, 0)), sesgo=0.7)
    esc.etiquetas.append(((x, y + 0.025, z), "RAÚL", 0.05, (230, 226, 210)))

def cuaderno(img, t, pagina=0.0, lineas=(), nombre_p=0.0, mojado=0.6, cy=820, escala=1.0):
    """el cuaderno de Raúl en primer plano (2D). pagina 0 = tapa cerrada (con RAÚL escrito a mano); 1 = abierto por la última página.
    lineas: notas a mano; nombre_p (0-1): se ve 'EL SIGUIENTE:' y un nombre emborronado por el agua."""
    from PIL import ImageFilter
    d = ImageDraw.Draw(img)
    w, h = 760 * escala, 1000 * escala
    x0, y0 = W / 2 - w / 2, cy - h / 2
    d.rectangle((x0 + 22, y0 + 26, x0 + w + 22, y0 + h + 26), fill=(8, 8, 8))
    if pagina < 0.5:
        d.rectangle((x0, y0, x0 + w, y0 + h), fill=(44, 74, 62), outline=(20, 34, 30), width=8)
        d.rectangle((x0 + 60 * escala, y0 + 170 * escala, x0 + w - 60 * escala, y0 + 330 * escala), fill=(222, 216, 196))
        d.text((W / 2, y0 + 250 * escala), tr("RAÚL"), font=font(int(110 * escala)), fill=(40, 60, 160), anchor="mm")
        d.text((W / 2, y0 + 420 * escala), tr("KM 9"), font=font(int(60 * escala)), fill=(214, 210, 190), anchor="mm")
    else:
        d.rectangle((x0, y0, x0 + w, y0 + h), fill=(222, 216, 194), outline=(150, 140, 120), width=6)
        for k in range(14): d.line((x0 + 30, y0 + 120 * escala + k * 62 * escala, x0 + w - 30, y0 + 120 * escala + k * 62 * escala), fill=(170, 180, 200), width=2)
        d.line((x0 + 110 * escala, y0, x0 + 110 * escala, y0 + h), fill=(210, 120, 120), width=3)
        for i, ln in enumerate(lineas):
            fs = 54
            while d.textlength(tr(ln), font=font(int(fs * escala))) > w - 170 * escala and fs > 26: fs -= 2
            d.text((x0 + 130 * escala, y0 + 160 * escala + i * 124 * escala), tr(ln), font=font(int(fs * escala)), fill=(40, 60, 150), anchor="lm")
        if nombre_p > 0:
            yy = y0 + 160 * escala + len(lineas) * 124 * escala + 40 * escala
            d.text((x0 + 130 * escala, yy), tr("EL SIGUIENTE:"), font=font(int(64 * escala)), fill=(150, 30, 30), anchor="lm")
            # el nombre: tinta corrida por el agua (no se lee, pero es el tuyo): letras muy emborronadas y chorretones
            capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
            a = int(255 * min(1, nombre_p))
            fn = font(int(76 * escala))
            dc.text((x0 + 150 * escala, yy + 120 * escala), "Mxnuel Arxas", font=fn, fill=(40, 50, 150, a), anchor="lm")
            r_ = __import__("random").Random(6)
            tw = dc.textlength("Mxnuel Arxas", font=fn)
            for j in range(6):
                xx = x0 + 150 * escala + r_.uniform(0, tw); ll = r_.uniform(60, 200) * escala * min(1, nombre_p * 1.3)
                dc.line((xx, yy + 140 * escala, xx + 4, yy + 140 * escala + ll), fill=(40, 50, 150, int(a * 0.7)), width=int(10 * escala))
            capa = capa.filter(ImageFilter.GaussianBlur(14 * escala))
            img.paste(capa, (0, 0), capa)
    if mojado > 0:                                       # manchas de agua y hojas onduladas
        capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
        r_ = __import__("random").Random(9)
        for j in range(7):
            cx_, cy_, rr = r_.uniform(x0, x0 + w), r_.uniform(y0, y0 + h), r_.uniform(60, 160) * escala
            dc.ellipse((cx_ - rr, cy_ - rr, cx_ + rr, cy_ + rr), fill=(60, 70, 80, int(60 * mojado)))
        capa = capa.filter(ImageFilter.GaussianBlur(25))
        img.paste(capa, (0, 0), capa)
    return img

# ---------- piezas añadidas en la Parte 7: páginas que se escriben solas, bolígrafo y camión ----------
LETRA = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"   # "letra a mano" (cursiva)

def pagina(img, lineas, fecha=None, p=None, cy=900, escala=1.0, humeda=None, pluma=True, t=0.0, tinta=(30, 50, 150), mojado=0.5, size=74):
    """una página del cuaderno de Raúl en primer plano, con letra a mano que se escribe SOLA.
    lineas: textos (se traducen con tr); p: cuánto hay escrito, en líneas (2.5 = dos líneas y media; None = todo);
    fecha: cabecera arriba a la derecha (p. ej. '18 NOV 1986'); humeda: índice de la línea con la tinta aún húmeda (brilla y gotea);
    pluma: la punta de un bolígrafo, sin mano, al final de lo escrito. Devuelve la imagen."""
    from PIL import ImageFilter
    d = ImageDraw.Draw(img)
    w, h = 900 * escala, 980 * escala
    x0, y0 = W / 2 - w / 2, cy - h / 2
    d.rectangle((x0 + 22, y0 + 26, x0 + w + 22, y0 + h + 26), fill=(8, 8, 8))
    d.rectangle((x0, y0, x0 + w, y0 + h), fill=(226, 220, 198), outline=(150, 140, 120), width=6)
    paso = 118 * escala
    for k in range(9): d.line((x0 + 24, y0 + 200 * escala + k * paso, x0 + w - 24, y0 + 200 * escala + k * paso), fill=(168, 178, 200), width=2)
    d.line((x0 + 100 * escala, y0, x0 + 100 * escala, y0 + h), fill=(210, 120, 120), width=3)
    if fecha:
        d.text((x0 + w - 50 * escala, y0 + 90 * escala), tr(fecha), font=font(int(60 * escala), LETRA), fill=(160, 30, 30), anchor="rm", stroke_width=1, stroke_fill=(160, 30, 30))
    total = len(lineas) if p is None else p
    fin = None
    for i, ln in enumerate(lineas):
        if i >= total: break
        txt = tr(ln)
        fs = size
        while d.textlength(txt, font=font(int(fs * escala), LETRA)) > w - 160 * escala and fs > 30: fs -= 2
        fn = font(int(fs * escala), LETRA)
        n = len(txt) if i + 1 <= total else max(0, int(len(txt) * (total - i)))
        parte = txt[:n]
        yy = y0 + 200 * escala + i * paso - 8 * escala
        col = tinta if humeda != i else (14, 24, 90)
        d.text((x0 + 125 * escala, yy), parte, font=fn, fill=col, anchor="ls", stroke_width=1, stroke_fill=col)
        fin = (x0 + 125 * escala + d.textlength(parte, font=fn), yy - 14 * escala)
        if humeda == i:                                  # tinta fresca: brillo encima y chorretones
            capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
            r_ = __import__("random").Random(11)
            tw = d.textlength(parte, font=fn)
            for j in range(5):
                xx = x0 + 125 * escala + r_.uniform(0, tw); ll = r_.uniform(40, 130) * escala * (0.6 + 0.4 * math.sin(t * 2 + j) ** 2)
                dc.line((xx, yy, xx + 2, yy + ll), fill=(20, 30, 110, 200), width=int(7 * escala))
                dc.ellipse((xx - 6 * escala, yy + ll - 6 * escala, xx + 8 * escala, yy + ll + 8 * escala), fill=(20, 30, 110, 200))
            capa = capa.filter(ImageFilter.GaussianBlur(2))
            img.paste(capa, (0, 0), capa)
            d = ImageDraw.Draw(img)
            d.text((x0 + 125 * escala - 2, yy - 3), parte, font=fn, fill=(120, 140, 230), anchor="ls")
            d.text((x0 + 125 * escala, yy), parte, font=fn, fill=col, anchor="ls", stroke_width=1, stroke_fill=col)
    if mojado > 0:
        capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
        r_ = __import__("random").Random(9)
        for j in range(6):
            cx_, cy_, rr = r_.uniform(x0, x0 + w), r_.uniform(y0, y0 + h), r_.uniform(60, 150) * escala
            dc.ellipse((cx_ - rr, cy_ - rr, cx_ + rr, cy_ + rr), fill=(60, 70, 80, int(55 * mojado)))
        capa = capa.filter(ImageFilter.GaussianBlur(25))
        img.paste(capa, (0, 0), capa)
    if pluma and fin is not None:                        # bolígrafo sin mano: la punta en el último trazo
        d = ImageDraw.Draw(img)
        fx_, fy_ = fin[0] + 4 * math.sin(t * 23), fin[1] + 3 * math.cos(t * 31)
        L_ = 420 * escala; a = math.radians(52)          # el cuerpo baja hacia la derecha (no tapa lo escrito)
        ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
        def pt(s, o): return (fx_ + ux * s + nx * o, fy_ + uy * s + ny * o)
        d.polygon([pt(0, 0), pt(40 * escala, -9 * escala), pt(40 * escala, 9 * escala)], fill=(40, 40, 44))
        d.polygon([pt(40 * escala, -14 * escala), pt(L_, -16 * escala), pt(L_, 16 * escala), pt(40 * escala, 14 * escala)], fill=(232, 232, 236), outline=(20, 20, 24))
        d.polygon([pt(L_ - 60 * escala, -17 * escala), pt(L_, -17 * escala), pt(L_, 17 * escala), pt(L_ - 60 * escala, 17 * escala)], fill=(30, 50, 150))
        d.line([pt(70 * escala, 18 * escala), pt(L_ - 70 * escala, 18 * escala)], fill=(30, 50, 150), width=int(6 * escala))
    return img

def boligrafo3d(esc, x, y, z, yaw=0.0, inclina=0.0):
    """bolígrafo (cuerpo blanco y capuchón azul) sobre el mostrador o en la mano"""
    M = cadena(mover(x, y, z), rot_y(yaw), rot_x(inclina))
    esc.add(caja(0.012, 0.012, 0.15, (230, 230, 234)), M, sesgo=0.8)
    esc.add(caja(0.014, 0.014, 0.03, (30, 50, 150)), cadena(M, mover(0, 0, -0.07)), sesgo=0.8)

def cuaderno3d_abierto(esc, x, y, z, yaw=0.0, col=(40, 70, 60)):
    """el cuaderno de Raúl abierto sobre el mostrador (dos páginas claras con renglones de tinta)"""
    M = cadena(mover(x, y, z), rot_y(yaw))
    esc.add(caja(0.46, 0.012, 0.31, col), M, sesgo=0.6)
    for sx in (-0.115, 0.115):
        esc.add(caja(0.215, 0.012, 0.29, (226, 220, 198)), cadena(M, mover(sx, 0.012, 0)), sesgo=0.7)
        for k in range(6):
            esc.add(caja(0.15, 0.003, 0.012, (40, 60, 150)), cadena(M, mover(sx - 0.01 * k % 3, 0.019, -0.11 + k * 0.042)), sesgo=0.9)

def camion(esc, x, z, yaw=0.0, faros=0.0, col=(170, 170, 166), cabina_col=(120, 30, 30)):
    """camión de reparto SIN logotipo (cabina + caja blanca sucia). Mira hacia +z local. faros 0-1"""
    M = cadena(mover(x, 0, z), rot_y(yaw))
    esc.add(caja(2.4, 2.3, 2.0, cabina_col, base=True), cadena(M, mover(0, 0.5, 2.6)))            # cabina
    esc.add(caja(2.2, 0.8, 0.05, (20, 24, 30)), cadena(M, mover(0, 2.1, 3.61)))                    # parabrisas
    esc.add(caja(2.5, 3.0, 6.0, col, base=True), cadena(M, mover(0, 0.6, -1.5)))                   # caja de carga (lisa: sin logo)
    esc.add(caja(2.52, 0.08, 6.02, (110, 110, 106)), cadena(M, mover(0, 3.55, -1.5)))
    for sx in (-1.1, 1.1):
        for sz in (2.6, -0.5, -3.4): esc.add(caja(0.35, 1.0, 1.0, (14, 14, 14)), cadena(M, mover(sx, 0.5, sz)))
        f = tuple(int(v * faros) for v in (255, 248, 210)) if faros > 0 else (80, 80, 74)
        esc.add(caja(0.42, 0.24, 0.05, f), cadena(M, mover(sx * 0.82, 0.95, 3.62)), emite=faros > 0)
    return M

# ---------- piezas añadidas en la Parte 8: el albarán, la caja de reparto y la placa del uniforme ----------
def firma(d, x, y, ancho, p=1.0, col=(30, 50, 150), grosor=6, semilla=3):
    """una firma a mano (garabato cursivo) de izquierda a derecha; p (0-1): cuánto está trazada"""
    import random as _r
    r_ = _r.Random(semilla)
    pts, n = [], 60
    amp = [r_.uniform(0.35, 1.0) for _ in range(9)]
    for i in range(int(n * min(1, p)) + 1):
        u = i / n
        a = amp[int(u * 8.99)]
        pts.append((x + u * ancho + 22 * math.sin(u * 31), y - a * 46 * math.sin(u * 24 + 0.6) - 14 * u))
    if len(pts) > 1: d.line(pts, fill=col, width=grosor, joint="curve")
    if p >= 1: d.line((x + ancho * 0.05, y + 30, x + ancho * 0.95, y + 18), fill=col, width=grosor - 1)   # rúbrica
    return d

def nombre_emborronado(img, x, y, size=76, a=1.0, col=(40, 50, 150), anchor="lm", blur=12):
    """tu nombre, escrito pero corrido por el agua: no se llega a leer nunca"""
    from PIL import ImageFilter
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
    fn = font(int(size))
    dc.text((x, y), "Mxnuel Arxas", font=fn, fill=(*col, int(255 * a)), anchor=anchor)
    tw = dc.textlength("Mxnuel Arxas", font=fn)
    x0 = x - (tw / 2 if anchor[0] == "m" else 0)
    r_ = __import__("random").Random(6)
    for j in range(6):
        xx = x0 + r_.uniform(0, tw); ll = r_.uniform(0.6, 2.2) * size
        dc.line((xx, y + size * 0.3, xx + 4, y + size * 0.3 + ll), fill=(*col, int(180 * a)), width=max(3, int(size / 8)))
    capa = capa.filter(ImageFilter.GaussianBlur(blur))
    img.paste(capa, (0, 0), capa)
    return img

def albaran(img, fecha="20 NOV 2026", firma_p=1.0, marca=0.0, cy=900, escala=1.0, t=0.0):
    """el albarán de entrega del camión en primer plano (copia rosa). Ya viene firmado (firma_p) con TU letra;
    fecha: la de la entrega (escrita a mano); marca (0-1): círculo rojo alrededor de la fecha."""
    d = ImageDraw.Draw(img)
    w, h = 880 * escala, 1040 * escala
    x0, y0 = W / 2 - w / 2, cy - h / 2
    d.rectangle((x0 + 22, y0 + 26, x0 + w + 22, y0 + h + 26), fill=(8, 8, 8))
    d.rectangle((x0, y0, x0 + w, y0 + h), fill=(236, 218, 216), outline=(150, 120, 120), width=6)
    for k in range(int(w / (26 * escala))):                       # trepado de arriba (hoja arrancada del talonario)
        cx_ = x0 + 13 * escala + k * 26 * escala
        d.ellipse((cx_ - 6 * escala, y0 + 14 * escala, cx_ + 6 * escala, y0 + 26 * escala), fill=(120, 100, 100))
    s = lambda v: int(v * escala)
    d.text((x0 + s(50), y0 + s(95)), tr("ALBARÁN DE ENTREGA"), font=font(s(56)), fill=(40, 30, 34), anchor="lm")
    d.text((x0 + w - s(50), y0 + s(165)), "Nº 0008", font=font(s(44)), fill=(170, 30, 30), anchor="rm")
    d.line((x0 + s(40), y0 + s(210), x0 + w - s(40), y0 + s(210)), fill=(120, 90, 90), width=4)
    filas = [(tr("DESTINO:"), tr("KILÓMETRO 9")), (tr("BULTOS:"), tr("1 CAJA")), (tr("TURNO:"), tr("NOCHE"))]
    for i, (k_, v_) in enumerate(filas):
        yy = y0 + s(285) + i * s(95)
        d.text((x0 + s(50), yy), k_, font=font(s(44)), fill=(90, 60, 64), anchor="lm")
        d.text((x0 + s(400), yy), v_, font=font(s(50), LETRA), fill=(30, 50, 150), anchor="lm", stroke_width=1, stroke_fill=(30, 50, 150))
    yf = y0 + s(600)
    d.text((x0 + s(50), yf), tr("FECHA:"), font=font(s(44)), fill=(90, 60, 64), anchor="lm")
    fx = x0 + s(400)
    d.text((fx, yf), tr(fecha), font=font(s(60), LETRA), fill=(30, 50, 150), anchor="lm", stroke_width=1, stroke_fill=(30, 50, 150))
    if marca > 0:
        tw = d.textlength(tr(fecha), font=font(s(60), LETRA))
        d.ellipse((fx - s(30), yf - s(62), fx + tw + s(30), yf + s(58)), outline=(220, 30, 30), width=int(10 * min(1, marca)) + 1)
    yr = y0 + s(760)
    d.text((x0 + s(50), yr), tr("RECIBÍ:"), font=font(s(44)), fill=(90, 60, 64), anchor="lm")
    d.rectangle((x0 + s(50), yr + s(50), x0 + w - s(50), yr + s(240)), outline=(140, 110, 110), width=3)
    if firma_p > 0: firma(d, x0 + s(120), yr + s(150), w - s(260), p=firma_p, grosor=max(3, s(7)))
    return img

def caja_carton(esc, x, y, z, abierta=0.0, yaw=0.0, dentro=None, mojada=0.0):
    """caja de reparto de cartón (0.55 x 0.38 x 0.42 m) con una etiqueta blanca en la tapa.
    abierta (0-1): las solapas se abren hacia los lados. dentro: color de lo que hay dentro (p. ej. el uniforme)."""
    M = cadena(mover(x, y, z), rot_y(yaw))
    c = tuple(int(v * (1 - 0.3 * mojada)) for v in (170, 128, 82))
    w_, h_, d_ = 0.55, 0.38, 0.42
    esc.add(caja(w_, 0.02, d_, tuple(int(v * 0.8) for v in c)), cadena(M, mover(0, 0.01, 0)), sesgo=0.4)
    for sx in (-1, 1): esc.add(caja(0.02, h_, d_, c, base=True), cadena(M, mover(sx * w_ / 2, 0, 0)), sesgo=0.4)
    for sz in (-1, 1): esc.add(caja(w_, h_, 0.02, tuple(int(v * 0.92) for v in c), base=True), cadena(M, mover(0, 0, sz * d_ / 2)), sesgo=0.4)
    if dentro: esc.add(caja(w_ - 0.06, 0.03, d_ - 0.06, dentro), cadena(M, mover(0, h_ - 0.08, 0)), sesgo=0.6)
    if dentro:                                           # pliegues y cuello de la ropa doblada
        osc = tuple(int(v * 0.6) for v in dentro)
        for k in (-1, 1): esc.add(caja(0.02, 0.012, d_ - 0.1, osc), cadena(M, mover(k * 0.12, h_ - 0.05, 0)), sesgo=0.7)
        esc.add(caja(0.2, 0.02, 0.05, osc), cadena(M, mover(0, h_ - 0.045, -d_ / 2 + 0.08)), sesgo=0.7)
    a = math.pi * 0.85 * ease(abierta)
    for sx in (-1, 1):                                   # solapas
        piv = cadena(M, mover(sx * w_ / 2, h_, 0), rot_z(sx * a))
        esc.add(caja(w_ / 2, 0.012, d_, c), cadena(piv, mover(-sx * w_ / 4, 0, 0)), sesgo=0.5)
    if abierta < 0.2:                                    # etiqueta blanca sobre la tapa
        esc.add(caja(0.26, 0.004, 0.16, (236, 234, 226)), cadena(M, mover(-0.12, h_ + 0.01, 0.05)), sesgo=0.9)
    return M

def albaran3d(esc, x, y, z, yaw=0.0, inclina=0.0):
    """el albarán (hoja rosa) en 3D: en la mano del conductor o sobre el mostrador"""
    M = cadena(mover(x, y, z), rot_y(yaw), rot_x(inclina))
    esc.add(caja(0.21, 0.004, 0.27, (236, 214, 212)), M, sesgo=0.8)
    for k in range(5): esc.add(caja(0.14, 0.002, 0.01, (90, 70, 80)), cadena(M, mover(-0.02, 0.003, -0.09 + k * 0.04)), sesgo=0.9)
    esc.add(caja(0.12, 0.002, 0.012, (30, 50, 150)), cadena(M, mover(0.02, 0.003, 0.11)), sesgo=0.95)   # la firma

def pecho_placa(img, nombre, t=0.0, p=1.0, mojado=0.0):
    """plano subjetivo mirando hacia abajo: tu pecho, con el uniforme rojo y la placa con el nombre.
    nombre: lo que pone la placa (se traduce con tr). p (0-1): lo que se ha bajado la mirada (desliza el plano)."""
    from PIL import ImageFilter
    import numpy as _np
    dy = int((1 - ease(p)) * 500)
    # fondo: el mostrador, más allá del pecho
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, H), fill=(54, 50, 46))
    if 1450 + dy < H: d.rectangle((0, 1450 + dy, W, H), fill=(150, 146, 136))
    # el pecho: una curva grande de tela roja que llena el plano (con pliegues)
    ys = _np.linspace(0, 1, H)[:, None]
    xs = _np.linspace(-1, 1, W)[None, :]
    luz = 0.55 + 0.45 * _np.cos(xs * 1.3) * (0.7 + 0.3 * (1 - ys))
    pl = 0.06 * _np.sin(xs * 9 + ys * 4 + 0.4 * math.sin(t * 0.8))
    f = _np.clip(luz + pl, 0.15, 1.0)
    rojo = _np.stack([150 * f, 36 * f, 36 * f], -1).astype(_np.uint8)
    tela = Image.fromarray(rojo)
    mask = Image.new("L", (W, H), 0); dm = ImageDraw.Draw(mask)
    dm.ellipse((-420, -900 + dy, W + 420, 1560 + dy), fill=255)
    img.paste(tela, (0, 0), mask)
    d = ImageDraw.Draw(img)
    # cremallera y bolsillo
    d.line((W / 2 + 40, 0, W / 2 + 60, 1500 + dy), fill=(70, 18, 18), width=10)
    d.rectangle((560, 640 + dy, 920, 980 + dy), outline=(100, 24, 24), width=8)
    # la placa (metal dorado, letras negras grabadas)
    px0, py0, px1, py1 = 160, 560 + dy, 520, 760 + dy
    d.rounded_rectangle((px0 + 10, py0 + 14, px1 + 10, py1 + 14), 18, fill=(40, 10, 10))
    d.rounded_rectangle((px0, py0, px1, py1), 18, fill=(214, 186, 110), outline=(120, 96, 40), width=6)
    d.line((px0 + 24, py0 + 22, px1 - 60, py0 + 22), fill=(250, 236, 180), width=6)                  # brillo
    txt = tr(nombre)
    fs = 110
    while d.textlength(txt, font=font(fs)) > (px1 - px0) - 50 and fs > 40: fs -= 4
    d.text(((px0 + px1) / 2, (py0 + py1) / 2 + 6), txt, font=font(fs), fill=(26, 20, 16), anchor="mm")
    if mojado > 0:                                       # manchas de humedad en la tela
        capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
        r_ = __import__("random").Random(4)
        for j in range(7):
            cx_, cy_, rr = r_.uniform(0, W), r_.uniform(0, 1400), r_.uniform(80, 200)
            dc.ellipse((cx_ - rr, cy_ - rr + dy, cx_ + rr, cy_ + rr + dy), fill=(40, 6, 6, int(90 * mojado)))
        capa = capa.filter(ImageFilter.GaussianBlur(30))
        img.paste(capa, (0, 0), capa)
    return img

def vapor(img, cx, cy, ancho, t, n=8, alfa=90, alto=600):
    """niebla/vapor que sube de algo (2D, semitransparente y desenfocado)"""
    from PIL import ImageFilter
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
    for j in range(n):
        ph = (t * 0.35 + j / n) % 1.0
        x = cx + (j / (n - 1) - 0.5) * ancho + 40 * math.sin(t * 1.3 + j * 2)
        y = cy - ph * alto
        r = 70 + 130 * ph
        dc.ellipse((x - r, y - r * 0.7, x + r, y + r * 0.7), fill=(190, 198, 196, int(alfa * math.sin(math.pi * ph))))
    capa = capa.filter(ImageFilter.GaussianBlur(26))
    img.paste(capa, (0, 0), capa)
    return img

# ---------- piezas añadidas en la Parte 9: Raúl al otro lado del cristal ----------
UNIFORME_MOJADO = (104, 24, 26)

def _u(alto=1.0):
    s = alto * 1.75 / 3.06
    return lambda v: v / 100 * s

def raul(esc, p, x, z, yaw=0.0, cara="neutral", mojado=1.0, placa=True):
    """Raúl (o lo que queda de él): tu mismo uniforme y gorra, empapado, con una placa dorada en el pecho.
    Devuelve (cab, placa_pos): la matriz de la cabeza (para cara_puntos) y el centro 3D de la placa (para escribir el nombre en 2D)."""
    col = tuple(int(lerp(a, b, mojado)) for a, b in zip(UNIFORME, UNIFORME_MOJADO))
    def gorra(e, cab, u):
        e.add(esfera(u(26), col, 1), cadena(cab, mover(0, u(10), 0), escala(1, 0.55, 1)))
        e.add(caja(u(36), u(4), u(22), col), cadena(cab, mover(0, u(8), u(24))))
    cab = humano(esc, p, x=x, z=z, yaw=yaw, ropa=col, piel=(196, 186, 178), pantalon=(34, 36, 44), cara=cara, extra_cabeza=gorra)
    pp = None
    if placa:
        u = _u(); rb = math.radians(p.get("body", 0))
        M = cadena(mover(x, 0, z), rot_y(yaw), mover(0, u(L["ul"] + L["ll"]) + u(6), 0), rot_x(rb), mover(-u(9), u(L["torso"] * 0.72), u(10.4)))
        esc.add(caja(0.12, 0.045, 0.012, (214, 186, 110)), M, sesgo=0.8)
        pp = tuple((M @ np.array([0, 0, 0.007, 1.0]))[:3])
    return cab, pp

def cara_puntos(cab, alto=1.0):
    """posiciones 3D de los ojos (izq, der) y la boca de un humano, a partir de la matriz de la cabeza que devuelve humano()"""
    u = _u(alto); HR = L["head"] * 0.75
    P = lambda v: tuple((cab @ np.array([*v, 1.0]))[:3])
    return P((-u(12), u(4), u(HR) * 0.95)), P((u(12), u(4), u(HR) * 0.95)), P((0, -u(15), u(HR) * 0.9))

def lagrimas(img, cam, cab, p=1.0, t=0.0, col=(170, 190, 200)):
    """dos regueros brillantes que caen de los ojos (p: 0-1, lo que han bajado)"""
    if p <= 0: return img
    d = ImageDraw.Draw(img)
    for i, e in enumerate(cara_puntos(cab)[:2]):
        q = proyectar(cam, e)
        if not q: continue
        s = 300 / max(q[2], 0.3)
        largo = s * 0.55 * p
        pts = [(q[0] + math.sin(j * 0.5 + i + t) * s * 0.01, q[1] + s * 0.03 + largo * j / 8) for j in range(9)]
        d.line(pts, fill=col, width=max(3, int(s / 40)))
    return img

def sonrisa(img, cam, cab, p=1.0, ancho=1.0, col=(24, 12, 12)):
    """una sonrisa dibujada encima de la cara: una raja oscura demasiado ancha (p: 0-1 lo que se abre)"""
    if p <= 0: return img
    q = proyectar(cam, cara_puntos(cab)[2])
    if not q: return img
    d = ImageDraw.Draw(img); s = 1.0 / max(q[2], 0.3) * 110 * ancho * (0.35 + 0.65 * p)
    d.arc((q[0] - s, q[1] - s * 0.55, q[0] + s, q[1] + s * 0.35), 12, 168, fill=col, width=max(3, int(s / 8)))
    return img

def cristal(img, t=0.0, gotas=1.0, vaho_=0.0, reflejo=0.25, semilla=9, caja_=None):
    """el cristal de la puerta entre tú y lo de fuera (2D): reflejo frío, vaho en el borde inferior y gotas que resbalan.
    caja_=(x0, y0, x1, y1): zona del cristal (por defecto, toda la imagen)."""
    from PIL import ImageFilter
    x0, y0, x1, y1 = caja_ or (0, 0, W, H)
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
    if reflejo > 0:                                   # dos bandas diagonales de reflejo
        for k, off in enumerate((0.25, 0.62)):
            cx = x0 + (x1 - x0) * off
            dc.polygon([(cx - 60, y0), (cx + 90 + 40 * k, y0), (cx - 160 + 40 * k, y1), (cx - 310, y1)], fill=(200, 220, 225, int(40 * reflejo)))
    if vaho_ > 0:
        dc.rectangle((x0, y1 - (y1 - y0) * 0.28, x1, y1), fill=(200, 210, 210, int(110 * vaho_)))
    capa = capa.filter(ImageFilter.GaussianBlur(30))
    img = Image.alpha_composite(img.convert("RGBA"), capa)
    g = Image.new("RGBA", img.size, (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
    r_ = __import__("random").Random(semilla)
    for j in range(int(46 * gotas)):
        gx = r_.uniform(x0, x1); v = r_.uniform(40, 160); gy = y0 + (r_.uniform(0, y1 - y0) + t * v) % (y1 - y0)
        rr = r_.uniform(5, 13)
        dg.line((gx, gy - rr * r_.uniform(3, 12), gx, gy), fill=(220, 235, 240, 70), width=int(rr * 0.6))
        dg.ellipse((gx - rr, gy - rr, gx + rr, gy + rr * 1.2), fill=(225, 238, 242, 120), outline=(30, 40, 44, 120), width=2)
    g = g.filter(ImageFilter.GaussianBlur(1.2))
    return Image.alpha_composite(img, g).convert("RGB")

# ---------- piezas añadidas en la Parte 10: el monitor de las cámaras, la puerta de atrás y el cartel del km 10 ----------
PUERTA_A = (0.35, -5.95)                     # puerta de atrás (x, z de la pared del fondo), entre el aseo y la nevera

def puerta_atras(esc, abierta=0.0, fuera=(196, 204, 202), cartel=True):
    """puerta metálica de atrás en la pared del fondo (vista desde dentro). abierta 0-1: la hoja gira hacia fuera
    y en el hueco se ve la niebla de detrás (blanca, emite)."""
    x, z = PUERTA_A
    _caja_en(esc, x - 0.52, 0, z - 0.02, x + 0.52, 2.16, z + 0.03, (70, 72, 74))                  # marco
    if abierta > 0:
        _caja_en(esc, x - 0.44, 0.01, z + 0.031, x + 0.44, 2.08, z + 0.04, fuera, emite=True)    # el hueco: niebla
        ang = -abierta * 1.9                                                                        # la hoja, abriéndose hacia fuera (detrás de la pared)
        M = cadena(mover(x - 0.44, 0, z + 0.05), rot_y(ang), mover(0.44, 1.04, 0))
        esc.add(caja(0.88, 2.06, 0.04, (110, 116, 118)), M, sesgo=0.3)
    else:
        _caja_en(esc, x - 0.44, 0.01, z + 0.031, x + 0.44, 2.08, z + 0.07, (110, 116, 118), sesgo=0.3)
        _caja_en(esc, x - 0.4, 1.0, z + 0.07, x + 0.36, 1.07, z + 0.12, (190, 190, 186), sesgo=0.5)   # barra antipánico
    if cartel:
        _caja_en(esc, x - 0.3, 2.26, z + 0.03, x + 0.3, 2.46, z + 0.06, (40, 190, 90), emite=True)      # luz verde de SALIDA
        esc.etiquetas.append(((x, 2.36, z + 0.08), "SALIDA", 0.13, (240, 255, 240)))

def trasera(esc, luz_puerta=1.0):
    """detrás de la gasolinera: suelo de tierra y hierbajos, la pared trasera por fuera y la puerta abierta con luz"""
    esc.add(subdividir(plano(40, 30, (62, 64, 56)), 10), mover(0, 0, -21), fondo=True)
    esc.add(subdividir(pared(10, 3, (118, 114, 102)), 6), cadena(mover(0, 0, -6.05), rot_y(math.pi)))   # pared trasera, por fuera
    x, z = PUERTA_A
    _caja_en(esc, x - 0.44, 0.01, -6.1, x + 0.44, 2.08, -6.06, tuple(int(v * luz_puerta) for v in FLUOR), emite=True)
    r_ = __import__("random").Random(12)
    for i in range(40):                                                                               # matojos
        hx, hz = r_.uniform(-12, 12), r_.uniform(-25, -7)
        esc.add(prisma(0.14, 0.02, r_.uniform(0.2, 0.5), (70, 78, 56), n=4), mover(hx, 0, hz))

def luz_trasera(f=1.0):
    """la luz de la tienda que sale por la puerta de atrás, hacia la niebla"""
    x, z = PUERTA_A
    return [Luz((x, 2.0, z - 0.6), FLUOR, 9.0, dir=(0, -0.25, -1), cono=55, fuerza=1.1 * f), Luz((x, 3.0, z - 4.0), (170, 186, 186), 8.0, fuerza=0.5 * f)]

def cartel_km(esc, x, z, texto="KILÓMETRO 10", yaw=0.0, luz=1.0, alto=1.9):
    """cartel de carretera clavado en la tierra: dos postes y una placa blanca con borde rojo; el texto va en etiquetas"""
    M = cadena(mover(x, 0, z), rot_y(yaw))
    for sx in (-0.75, 0.75): esc.add(caja(0.08, alto + 0.5, 0.08, (120, 120, 116), base=True), cadena(M, mover(sx, 0, 0)))
    esc.add(caja(1.9, 0.75, 0.05, (160, 30, 30)), cadena(M, mover(0, alto, 0.03)))
    c = tuple(int(v * luz) for v in (232, 232, 222))
    esc.add(caja(1.78, 0.63, 0.02, c), cadena(M, mover(0, alto, 0.065)), sesgo=0.2)
    p = tuple((M @ np.array([0, alto, 0.1, 1.0]))[:3])
    esc.etiquetas.append((p, texto, 0.2, (24, 24, 24)))
    return p

def monitor(fondo, pantalla, t=0.0, caja_=(70, 520, 1010, 1220), lcd=None, lcd_col=(110, 240, 170), ruido=0.5):
    """el monitor de las cámaras de seguridad en primer plano (2D): carcasa beige, pantalla con la imagen CCTV
    (con líneas de barrido y viñeta) y, opcional, el reloj de la caja (lcd = "04:10:12") debajo, para comparar horas."""
    from PIL import ImageFilter
    img = fondo.copy(); d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = caja_
    d.rounded_rectangle((x0 - 40, y0 - 40, x1 + 40, y1 + 70), 40, fill=(150, 146, 128), outline=(40, 40, 36), width=6)
    d.rounded_rectangle((x0 - 10, y0 - 10, x1 + 10, y1 + 10), 26, fill=(14, 14, 14))
    pw, ph = x1 - x0, y1 - y0
    sc = max(pw / W, ph / H)
    p = pantalla.resize((int(W * sc), int(H * sc)), Image.BILINEAR)
    ox, oy = (p.width - pw) // 2, int((p.height - ph) * 0.42)
    p = p.crop((ox, oy, ox + pw, oy + ph))
    a = np.asarray(p).astype(np.float32)
    a[::4] *= 0.78                                                                    # líneas de barrido
    yy, xx = np.mgrid[0:ph, 0:pw]
    vig = 1 - 0.45 * (((xx - pw / 2) / (pw / 2)) ** 2 + ((yy - ph / 2) / (ph / 2)) ** 2) / 2
    a *= vig[..., None]
    a += np.random.default_rng(int(t * 30)).normal(0, 9 * ruido, a.shape[:2])[..., None]
    p = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    m = Image.new("L", (pw, ph), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, pw - 1, ph - 1), 22, fill=255)
    img.paste(p, (x0, y0), m)
    d.ellipse((x1 - 30, y1 + 30, x1 - 10, y1 + 50), fill=(60, 220, 90))                # piloto encendido
    if lcd:
        lx, ly = W / 2, y1 + 190
        d.rounded_rectangle((lx - 230, ly - 70, lx + 230, ly + 70), 16, fill=(20, 26, 22), outline=(80, 84, 80), width=5)
        d.text((lx, ly), lcd, font=font(96), fill=lcd_col, anchor="mm")
    return img

# ---------- piezas añadidas en la Parte 11: la otra gasolinera (kilómetro 10) y la hoja de reglas en blanco ----------
def otra_gasolinera(t=0.0, rotulo="KILÓMETRO 10 · 24H", luz=1.0, cabina_kw=None):
    """la gasolinera del kilómetro 10: idéntica a la tuya (mundo) pero con otro rótulo en la fachada"""
    esc = mundo(t, luz=luz, cabina_kw=cabina_kw)
    esc.etiquetas = [(e[0], rotulo, 0.56, (200, 30, 30)) if e[1] == "KILÓMETRO 9 · 24H" else e for e in esc.etiquetas]
    return esc

def plantilla(esc, pos, p, yaw=math.pi, cual="empleado", cara="neutral"):
    """un empleado del turno de noche (todos con TU uniforme): cual = 'anciano' (boina, pelo cano), 'raul' (empapado, con placa),
    'empleado' (tú) o 'sincara' (otro, sin cara). Devuelve la matriz de la cabeza."""
    x, z = pos
    if cual == "anciano": return anciano(esc, p, x, z, yaw=yaw, cara=cara, abrigo=UNIFORME)
    if cual == "raul": return raul(esc, p, x, z, yaw=yaw, cara=cara, mojado=0.8)[0]
    if cual == "sincara": return humano(esc, p, x=x, z=z, yaw=yaw, ropa=UNIFORME, piel=(214, 210, 204), pantalon=(40, 42, 50), cara="ninguna",
                                        extra_cabeza=lambda e, cab, u: (e.add(esfera(u(26), UNIFORME, 1), cadena(cab, mover(0, u(10), 0), escala(1, 0.55, 1))),
                                                                         e.add(caja(u(36), u(4), u(22), UNIFORME), cadena(cab, mover(0, u(8), u(24))))))
    return empleado(esc, p, x, z, yaw=yaw, cara=cara)

def pose_saludo(t, k=1.0, fase=0.0):
    """mano derecha en alto, saludando de lado a lado (k 0-1: cuánto ha subido el brazo). Todos a la vez si comparten fase."""
    return pose(a1u=-8, a1l=10, a2u=lerp(-12, 150, k), a2l=lerp(12, 30 + 24 * math.sin(t * 6 + fase), k), head=-4)

def hoja_blanca(img, texto="Regla 12:", p=1.0, cy=880, zoom=0.8, t=0.0, humeda=True, boli=True, tinta=(30, 50, 150)):
    """una hoja de reglas NUEVA, en blanco (solo la cabecera impresa), con una línea a mano arriba (p: 0-1 escrito).
    humeda: la tinta aún brilla y gotea. boli: un bolígrafo suelto al lado, recién soltado."""
    from PIL import ImageFilter
    d = ImageDraw.Draw(img)
    w, h = 900 * zoom, 1180 * zoom
    x0, y0 = W / 2 - w / 2, cy - h / 2
    d.rectangle((x0 + 18, y0 + 22, x0 + w + 18, y0 + h + 22), fill=(10, 10, 10))
    d.rectangle((x0, y0, x0 + w, y0 + h), fill=(238, 236, 226), outline=(130, 128, 112), width=6)
    d.text((W / 2, y0 + 80 * zoom), tr("REGLAS DEL TURNO DE NOCHE"), font=font(int(50 * zoom)), fill=(150, 30, 30), anchor="mm")
    for k in range(9):                                     # renglones vacíos, muy tenues
        yy = y0 + 330 * zoom + k * 88 * zoom
        d.line((x0 + 50 * zoom, yy, x0 + w - 50 * zoom, yy), fill=(214, 212, 200), width=2)
    txt = tr(texto); n = max(0, int(len(txt) * min(1.0, p)))
    if n:
        fn = font(int(120 * zoom), LETRA)
        tx, ty = x0 + 70 * zoom, y0 + 250 * zoom
        d.text((tx, ty), txt[:n], font=fn, fill=tinta, anchor="ls", stroke_width=2, stroke_fill=tinta)
        tw = d.textlength(txt[:n], font=fn)
        if humeda:
            capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
            r_ = __import__("random").Random(13)
            for j in range(4):
                xx = tx + r_.uniform(0.1, 0.9) * tw; ll = r_.uniform(50, 150) * zoom * (0.6 + 0.4 * math.sin(t * 1.5 + j) ** 2)
                dc.line((xx, ty, xx + 2, ty + ll), fill=(20, 30, 110, 210), width=int(8 * zoom))
                dc.ellipse((xx - 7 * zoom, ty + ll - 7 * zoom, xx + 9 * zoom, ty + ll + 9 * zoom), fill=(20, 30, 110, 210))
            capa = capa.filter(ImageFilter.GaussianBlur(2))
            img.paste(capa, (0, 0), capa)
            d = ImageDraw.Draw(img)
            d.text((tx - 3, ty - 4), txt[:n], font=fn, fill=(130, 150, 235), anchor="ls")
            d.text((tx, ty), txt[:n], font=fn, fill=tinta, anchor="ls", stroke_width=2, stroke_fill=tinta)
    if boli:                                               # bolígrafo suelto, en diagonal, sobre la hoja
        fx_, fy_ = x0 + w * 0.62, y0 + 300 * zoom
        L_ = 520 * zoom; a = math.radians(58)
        ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
        def pt(s, o): return (fx_ + ux * s + nx * o, fy_ + uy * s + ny * o)
        d.polygon([pt(18, 26 * zoom), pt(L_ + 18, 26 * zoom), pt(L_ + 18, 46 * zoom), pt(18, 46 * zoom)], fill=(120, 118, 104))   # sombra
        d.polygon([pt(0, 0), pt(46 * zoom, -10 * zoom), pt(46 * zoom, 10 * zoom)], fill=(40, 40, 44))
        d.polygon([pt(46 * zoom, -16 * zoom), pt(L_, -18 * zoom), pt(L_, 18 * zoom), pt(46 * zoom, 16 * zoom)], fill=(232, 232, 236), outline=(20, 20, 24))
        d.polygon([pt(L_ - 70 * zoom, -19 * zoom), pt(L_, -19 * zoom), pt(L_, 19 * zoom), pt(L_ - 70 * zoom, 19 * zoom)], fill=(30, 50, 150))
    return img
