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

def cabina(esc, x, z):
    _caja_en(esc, x - 0.5, 0, z - 0.5, x + 0.5, 0.15, z + 0.5, (90, 90, 90))
    for sx, sz in ((-0.45, -0.45), (0.45, -0.45), (-0.45, 0.45), (0.45, 0.45)): _caja_en(esc, x + sx - 0.04, 0.15, z + sz - 0.04, x + sx + 0.04, 2.3, z + sz + 0.04, (150, 40, 36))
    _caja_en(esc, x - 0.5, 2.3, z - 0.5, x + 0.5, 2.5, z + 0.5, (150, 40, 36))
    _caja_en(esc, x - 0.15, 1.2, z - 0.45, x + 0.15, 1.6, z - 0.38, (30, 30, 30))       # teléfono

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

def exterior(esc, luz=1.0, surtidor4=0.0, coche4=0.0):
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
    farola(esc, 8, 14, luz); cabina(esc, -8, 12)
    # el surtidor 4: no debería existir (aparece en la niebla, al borde de la luz)
    # al final de la fila, fuera de la marquesina, donde ya no llega la luz
    if surtidor4 > 0:
        surtidor(esc, S4[0], S4[1], 4, 0.6 * surtidor4, col=tuple(int(v * (0.4 + 0.6 * surtidor4)) for v in (150, 128, 104)))
    if coche4 > 0: coche(esc, S4[0] + 2.2, S4[1] + 1.4, yaw=-math.pi / 2 - 0.25, col=(26, 28, 32), faros=coche4 if coche4 > 1 else 0)

def mundo(t=0.0, luz=1.0, surtidor4=0.0, coche4=0.0):
    esc = Escena(niebla=NIEBLA, amb=0.16)
    esc.etiquetas = []
    tienda(esc, luz); exterior(esc, luz, surtidor4, coche4)
    return esc

def luces_base(luz=1.0, extra=()):
    L_ = []
    if luz > 0:
        for fx in (-3, 0, 3): L_.append(Luz((fx, 2.8, -3), FLUOR, 6.5, fuerza=0.8 * luz))
        for lx in (-3, 0, 3): L_.append(Luz((lx, 4.2, 7), FLUOR, 8.0, fuerza=0.9 * luz))
        L_.append(Luz((9.2, 5.6, 14), SODIO, 9.0, fuerza=0.7 * luz))
    return L_ + list(extra)

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
    for p, txt in esc.etiquetas:
        q = proyectar(cam, p)
        if not q or q[2] > 24: continue
        f = 1 / math.tan(math.radians(cam.fov) / 2)
        alto_m = 0.32 if len(txt) <= 2 else 0.4                          # altura real del texto en metros
        size = int(min(220, alto_m / q[2] * f * H / 2))
        if size < 10: continue
        a = max(0.0, 1 - q[2] / 24)
        col = tuple(int(lerp(f_, c_, a)) for f_, c_ in zip(NIEBLA[0], (20, 20, 20) if len(txt) <= 2 else (200, 40, 36)))
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

def hoja_reglas(img, t, lineas, resalta=None, nota=None, nota_p=0.0, zoom=1.0, cy=None):
    """la hoja plastificada de reglas en primer plano (plano subjetivo).
    lineas: textos de las reglas; "?" = regla tachada con rotulador (aún no se ha descubierto).
    resalta: índice de la regla del episodio (fondo amarillo). nota: texto a mano al pie, que se escribe según nota_p (0-1)."""
    d = ImageDraw.Draw(img)
    cx = W / 2; cy = cy or 860
    w, h = 900 * zoom, 1120 * zoom
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
