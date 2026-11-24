"""Kit de escenarios 3D genéricos (look PS2) para la serie "REGLAS": cada noche un sitio distinto.
Todo en metros. Las piezas se combinan para montar hospitales, hoteles, metros, piscinas, oficinas, colegios…

    esc = Escena(niebla=((20, 22, 24), 4, 22), amb=0.12); esc.etiquetas = []
    L = pasillo(esc, largo=18, puertas=[(0, "411"), (3, "412"), …], luces_on=[1,1,0,1,…])
    cama(esc, x, z); interfono(esc, …); ascensor(esc, …)
    img = esc.render(cam, L + [Luz(...)])
    img = etiquetas(img, esc, cam)       # números de puertas, carteles (de turno3d)
Ver escenasreglas1.py como modelo completo.
"""
import math
import numpy as np
from PIL import Image, ImageDraw
from motor import *
from motor3d import *
from turno3d import _caja_en, etiquetas, proyectar, cctv, aclarar, rotulo_regla, _envolver

FLUOR = (236, 246, 236)
VERDE_HOSP = (118, 140, 128)

def escena(niebla=((18, 20, 22), 4.0, 24.0), amb=0.12):
    esc = Escena(niebla=niebla, amb=amb); esc.etiquetas = []
    return esc

def habitacion(esc, x0, x1, z0, z1, alto=2.8, col_pared=(150, 150, 140), suelo=(110, 112, 108), techo=(90, 92, 90),
               sin=(), div=4):
    """caja de habitación vista desde dentro. sin: paredes que no se ponen ('n' fondo z0, 's' frente z1, 'o' x0, 'e' x1)"""
    w, d = x1 - x0, z1 - z0; cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    esc.add(subdividir(plano(w, d, suelo), div), mover(cx, 0.0, cz), fondo=True)
    esc.add(subdividir(plano(w, d, techo), div), cadena(mover(cx, alto, cz), rot_x(math.pi)))
    if 'n' not in sin: esc.add(subdividir(pared(w, alto, col_pared), div), mover(cx, 0, z0))
    if 's' not in sin: esc.add(subdividir(pared(w, alto, col_pared), div), cadena(mover(cx, 0, z1), rot_y(math.pi)))
    if 'o' not in sin: esc.add(subdividir(pared(d, alto, col_pared), div), cadena(mover(x0, 0, cz), rot_y(math.pi / 2)))
    if 'e' not in sin: esc.add(subdividir(pared(d, alto, col_pared), div), cadena(mover(x1, 0, cz), rot_y(-math.pi / 2)))

def puerta(esc, x, z, lado, num=None, abierta=0.0, col=(170, 160, 140), marco=(70, 70, 70), luz_dentro=0.0, ancho=1.0, alto=2.1):
    """puerta en una pared lateral del pasillo. lado=-1 pared izquierda (x=x, mira a +x), +1 pared derecha (mira a -x).
    abierta 0-1 (hoja girada hacia dentro). luz_dentro: el hueco brilla (habitación con luz)."""
    s = -lado
    _caja_en(esc, x - 0.03, 0, z - ancho / 2 - 0.08, x + 0.03, alto + 0.08, z - ancho / 2, marco)
    _caja_en(esc, x - 0.03, 0, z + ancho / 2, x + 0.03, alto + 0.08, z + ancho / 2 + 0.08, marco)
    _caja_en(esc, x - 0.03, alto, z - ancho / 2, x + 0.03, alto + 0.08, z + ancho / 2, marco)
    hueco = tuple(int(v * luz_dentro) for v in (230, 210, 170)) if luz_dentro > 0 else (8, 8, 10)
    _caja_en(esc, x - s * 0.02, 0, z - ancho / 2, x - s * 0.01, alto, z + ancho / 2, hueco, emite=True)
    a = abierta * 1.4
    hoja = cadena(mover(x + s * 0.02, 0, z - ancho / 2), rot_y(-s * a), mover(0, alto / 2, ancho / 2))
    esc.add(caja(0.05, alto, ancho, col), hoja, sesgo=0.05)
    esc.add(caja(0.06, 0.04, 0.14, (200, 200, 190)), cadena(hoja, mover(s * 0.04, 0.0, ancho * 0.35)))
    if num: esc.etiquetas.append(((x + s * 0.06, alto + 0.3, z), str(num), 0.18, (30, 30, 30)))
    if num: _caja_en(esc, x + s * 0.0, alto + 0.15, z - 0.25, x + s * 0.05, alto + 0.45, z + 0.25, (226, 226, 218))

def fluorescente(esc, x, z, y=2.78, on=1.0, largo=1.2):
    _caja_en(esc, x - 0.15, y - 0.04, z - largo / 2, x + 0.15, y, z + largo / 2, tuple(int(30 + v * on * 0.85) for v in FLUOR), emite=on > 0.05)

def pasillo(esc, largo=18.0, ancho=2.4, alto=2.8, puertas=(), luces_on=None, col_pared=VERDE_HOSP, suelo=(150, 150, 144),
            techo=(120, 122, 120), zocalo=(80, 96, 90), fondo_puerta=None):
    """pasillo que va de z=0 (detrás de la cámara) a z=-largo. puertas: [(z_pos, num, lado, abierta, luz_dentro)].
    luces_on: lista de 0-1 por fluorescente (uno cada 3 m). Devuelve las luces (Luz) para render()."""
    hw = ancho / 2
    habitacion(esc, -hw, hw, -largo, 1.0, alto, col_pared, suelo, techo, sin=('s',), div=10)
    for sx in (-hw + 0.01, hw - 0.01):
        _caja_en(esc, sx - 0.01, 0, -largo, sx + 0.01, 0.9, 1.0, zocalo)
    for p in puertas:
        zp, num = p[0], p[1]; lado = p[2] if len(p) > 2 else (-1 if int(zp * 7) % 2 == 0 else 1)
        puerta(esc, lado * hw * 0.995, zp, lado, num, p[3] if len(p) > 3 else 0.0, luz_dentro=p[4] if len(p) > 4 else 0.0)
    if fondo_puerta: puerta(esc, 0, -largo + 0.03, 0, None)   # reservado
    luces = []; n = int(largo // 3)
    for k in range(n):
        on = 1.0 if luces_on is None else (luces_on[k] if k < len(luces_on) else 1.0)
        z = -1.5 - 3 * k
        fluorescente(esc, 0, z, alto - 0.02, on)
        if on > 0.05: luces.append(Luz((0, alto - 0.3, z), FLUOR, 5.5, fuerza=0.75 * on))
    return luces

def cama(esc, x, z, yaw=0.0, sabana=(210, 214, 210), bulto=True, cabeza=None):
    """cama de hospital (cabecero hacia -z si yaw=0). bulto: alguien tapado. cabeza: color de una cara que asoma (o None)."""
    M = cadena(mover(x, 0, z), rot_y(yaw))
    for sx in (-0.42, 0.42):
        for sz in (-0.95, 0.95): esc.add(caja(0.05, 0.55, 0.05, (150, 150, 150), base=True), cadena(M, mover(sx, 0, sz)))
    esc.add(caja(0.95, 0.18, 2.0, (190, 192, 190), base=True), cadena(M, mover(0, 0.55, 0)))
    esc.add(caja(0.95, 0.6, 0.06, (160, 162, 160), base=True), cadena(M, mover(0, 0.55, -1.0)))
    esc.add(caja(0.5, 0.12, 0.35, (232, 232, 226), base=True), cadena(M, mover(0, 0.73, -0.75)))
    if bulto:
        esc.add(caja(0.7, 0.28, 1.55, sabana, base=True), cadena(M, mover(0, 0.73, 0.15)))
        esc.add(esfera(0.2, sabana if cabeza is None else cabeza, 1), cadena(M, mover(0, 0.98, -0.72)))
    return M

def monitor_constantes(esc, x, z, yaw=0.0, col=(60, 230, 120), on=1.0):
    M = cadena(mover(x, 0, z), rot_y(yaw))
    esc.add(caja(0.06, 1.3, 0.06, (120, 120, 120), base=True), M)
    esc.add(caja(0.45, 0.35, 0.12, (30, 32, 34)), cadena(M, mover(0, 1.45, 0)))
    esc.add(caja(0.38, 0.27, 0.01, tuple(int(v * on) for v in col)), cadena(M, mover(0, 1.45, 0.065)), emite=True)
    return M

def interfono(esc, x, y, z, lado=-1, luz=0.0, col=(240, 60, 50), escala_=1.0):
    """caja de interfono/timbre en una pared lateral, con rejilla y piloto que se enciende"""
    s = -lado; e = escala_
    _caja_en(esc, x, y - 0.14 * e, z - 0.11 * e, x + s * 0.06, y + 0.14 * e, z + 0.11 * e, (210, 210, 200))
    for k in range(4):
        yy = y - 0.08 * e + k * 0.035 * e
        _caja_en(esc, x + s * 0.061, yy, z - 0.07 * e, x + s * 0.066, yy + 0.015 * e, z + 0.07 * e, (60, 60, 60))
    _caja_en(esc, x + s * 0.061, y + 0.07 * e, z - 0.03 * e, x + s * 0.07, y + 0.11 * e, z + 0.03 * e, tuple(int(40 + v * luz * 0.8) for v in col), emite=True)

def panel_llamadas(img, numeros, activo=None, parpadeo=True, t=0.0, y=360):
    """panel de control de enfermería en primer plano (2D): rejilla de habitaciones con la activa en rojo"""
    d = ImageDraw.Draw(img); cols = 4; w, h = 200, 110; x0 = W / 2 - cols * w / 2
    d.rectangle((x0 - 30, y - 70, x0 + cols * w + 30, y + ((len(numeros) + cols - 1) // cols) * h + 30), fill=(24, 26, 28), outline=(90, 90, 90), width=5)
    d.text((W / 2, y - 38), tr("LLAMADAS · PLANTA 4"), font=font(40), fill=(200, 200, 190), anchor="mm")
    for i, n in enumerate(numeros):
        cx, cy = x0 + (i % cols) * w + w / 2, y + (i // cols) * h + 50
        on = (n == activo) and (not parpadeo or int(t * 4) % 2 == 0)
        d.rounded_rectangle((cx - 80, cy - 40, cx + 80, cy + 40), 10, fill=(220, 40, 40) if on else (50, 54, 56))
        d.text((cx, cy), n, font=font(46), fill=(255, 255, 255) if on else (150, 150, 150), anchor="mm")
    return img

def ascensor(esc, x, z, lado=1, abierto=0.0, luz=1.0):
    """puertas de ascensor en una pared lateral (lado +1 derecha)"""
    s = -lado
    _caja_en(esc, x - 0.03, 0, z - 0.75, x + 0.03, 2.3, z + 0.75, (110, 112, 116))
    for k in (-1, 1):
        off = k * (0.37 + 0.36 * abierto)
        _caja_en(esc, x + s * 0.02, 0, z + off - 0.36, x + s * 0.05, 2.15, z + off + 0.36, (170, 172, 176), sesgo=0.05)
    if abierto > 0: _caja_en(esc, x - s * 0.02, 0, z - 0.7 * abierto, x - s * 0.01, 2.15, z + 0.7 * abierto, tuple(int(v * luz) for v in (240, 230, 200)), emite=True)

# ---------- cierres de la serie "Reglas" ----------
def negro(img, k):
    """funde a negro (k 0-1)"""
    if k <= 0: return img
    return Image.blend(img, Image.new("RGB", img.size, (0, 0, 0)), min(1.0, k))

def ficha_final(img, nombre, oficio, fecha, regla_rota, p=1.0, t=0.0, sello="DESAPARECIDO"):
    """tarjeta del final drástico: ficha de la víctima con un sello rojo (DESAPARECIDO, FALLECIDA, SUSTITUIDA…). Distinta de la de 3AM."""
    img = negro(img, 0.82)
    d = ImageDraw.Draw(img)
    if p <= 0: return img
    s = min(1.0, p)
    d.rectangle((110, 520, W - 110, 1180), fill=(226, 222, 206), outline=(80, 76, 66), width=6)
    d.text((150, 580), tr("FICHA"), font=font(44), fill=(90, 80, 70), anchor="lm")
    d.text((150, 680), nombre, font=font(74), fill=(20, 20, 24), anchor="lm")
    d.text((150, 770), tr(oficio), font=font(46), fill=(60, 60, 60), anchor="lm")
    d.text((150, 850), tr("Visto por última vez:") + " " + fecha, font=font(40), fill=(60, 60, 60), anchor="lm")
    fr = font(38); ls = _envolver(d, tr("Regla rota:") + " " + tr(regla_rota), fr, W - 300)
    for i, l_ in enumerate(ls[:3]): d.text((150, 920 + i * 48), l_, font=fr, fill=(150, 30, 30), anchor="lm")
    # sello rojo torcido
    txt = tr(sello); fs = 96
    while ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(txt, font=font(fs)) > 600 and fs > 40: fs -= 4
    sello = Image.new("RGBA", (700, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(sello)
    sd.rounded_rectangle((10, 10, 690, 190), 20, outline=(210, 30, 30, 235), width=14)
    sd.text((350, 100), txt, font=font(fs), fill=(210, 30, 30, 235), anchor="mm")
    sello = sello.rotate(-12, expand=True, resample=Image.BICUBIC)
    esc_s = 0.6 + 0.4 * s if s < 1 else 1.0 + 0.02 * math.sin(t * 20)
    sello = sello.resize((int(sello.width * esc_s), int(sello.height * esc_s)))
    img.paste(sello, (int(W / 2 - sello.width / 2), int(1185 - sello.height / 2)), sello)
    d.text((W / 2, 1380), tr("MAÑANA, OTRAS REGLAS"), font=font(52), fill=(230, 230, 230), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    return img

def interfono_2d(img, num, habla=0.0, piloto=1.0, t=0.0, cy=700):
    """interfono en primer plano (2D, se lee bien en el móvil): rejilla, piloto rojo, número y onda de voz si habla (0-1)"""
    d = ImageDraw.Draw(img); cx = W / 2
    d.rounded_rectangle((cx - 300, cy - 380, cx + 300, cy + 380), 40, fill=(206, 206, 196), outline=(70, 70, 66), width=8)
    d.rounded_rectangle((cx - 220, cy - 300, cx + 220, cy - 40), 24, fill=(40, 42, 44))
    for k in range(9):
        y = cy - 280 + k * 28; d.line((cx - 190, y, cx + 190, y), fill=(14, 14, 16), width=12)
    r = 34; col = (int(60 + 195 * piloto), 30, 30)
    d.ellipse((cx - r, cy + 40 - r, cx + r, cy + 40 + r), fill=col, outline=(30, 30, 30), width=4)
    d.text((cx, cy + 170), str(num), font=font(110), fill=(30, 30, 34), anchor="mm")
    if habla > 0:
        for i in range(13):
            hgt = (20 + 120 * abs(math.sin(t * 9 + i * 0.8)) * habla)
            x = cx - 180 + i * 30
            d.rectangle((x - 9, cy - 170 - hgt / 2, x + 9, cy - 170 + hgt / 2), fill=(235, 50, 50))
    return img

# ---------- piezas de hotel (Reglas 2): vestíbulo con recepción, claveros y libro de reservas ----------
MADERA = (96, 62, 44)
MOQUETA = (112, 34, 38)
PAPEL_PINTADO = (88, 96, 78)

def mostrador(esc, x0, x1, z, fondo=0.6, alto=1.1, col=MADERA, tapa=(150, 120, 90)):
    """mostrador de recepción (frente hacia +z, en z). Encima: timbre y lámpara de mesa."""
    _caja_en(esc, x0, 0, z - fondo, x1, alto, z, col)
    _caja_en(esc, x0 - 0.05, alto, z - fondo - 0.05, x1 + 0.05, alto + 0.06, z + 0.06, tapa, sesgo=0.4)
    for k in range(int((x1 - x0) / 0.8)):                       # paneles del frente
        xx = x0 + 0.15 + k * 0.8
        _caja_en(esc, xx, 0.15, z + 0.001, xx + 0.6, alto - 0.15, z + 0.02, tuple(int(v * 0.8) for v in col))

def timbre(esc, x, y, z):
    _caja_en(esc, x - 0.07, y, z - 0.07, x + 0.07, y + 0.02, z + 0.07, (40, 40, 40), sesgo=0.6)
    esc.add(esfera(0.06, (220, 190, 90), 1), cadena(mover(x, y + 0.03, z), escala(1, 0.6, 1)), sesgo=0.6)

def lampara_mesa(esc, x, y, z, on=1.0):
    """lámpara de banquero (pantalla verde que brilla)"""
    _caja_en(esc, x - 0.02, y, z - 0.02, x + 0.02, y + 0.3, z + 0.02, (180, 150, 80), sesgo=0.6)
    _caja_en(esc, x - 0.18, y + 0.28, z - 0.07, x + 0.18, y + 0.38, z + 0.07, tuple(int(v * (0.4 + 0.6 * on)) for v in (60, 200, 110)), emite=True, sesgo=0.6)

def claveros(esc, x, y, z, n=(4, 3), nums=None, vacio=None, falta=(), brillo0=0.0):
    """casillero de llaves en la pared del fondo (z): n=(columnas, filas). nums: textos; la casilla 'vacio' no tiene llave.
    brillo0: la llave de la casilla '0' brilla (0-1)."""
    cols, filas = n; w, h = 0.32, 0.3
    _caja_en(esc, x - cols * w / 2 - 0.08, y - 0.08, z, x + cols * w / 2 + 0.08, y + filas * h + 0.08, z + 0.08, MADERA)
    nums = nums or [str(i) for i in range(cols * filas)]
    for i, num in enumerate(nums):
        cx = x - cols * w / 2 + (i % cols) * w + w / 2; cy = y + (filas - 1 - i // cols) * h + h / 2
        _caja_en(esc, cx - 0.13, cy - 0.12, z + 0.08, cx + 0.13, cy + 0.12, z + 0.1, (40, 26, 20))
        if num != vacio and num not in falta:
            cero = num == "0"
            c = (220, 190, 90) if not cero else tuple(int(lerp(a, b, brillo0)) for a, b in zip((190, 30, 26), (255, 30, 20)))
            _caja_en(esc, cx - 0.02, cy - 0.1, z + 0.1, cx + 0.02, cy + 0.04, z + 0.13, c, emite=cero, sesgo=0.2)
            _caja_en(esc, cx - 0.07 if cero else cx - 0.05, cy - 0.19 if cero else cy - 0.16, z + 0.1, cx + 0.07 if cero else cx + 0.05,
                     cy - 0.08, z + 0.14, c if cero else (200, 200, 190), emite=cero, sesgo=0.2)
        esc.etiquetas.append(((cx, cy + 0.08, z + 0.12), num, 0.07, (230, 210, 160)))

def vestibulo(esc, luz=1.0, brillo0=0.0, falta=(), puerta_calle=0.0):
    """vestíbulo de hotel pequeño: moqueta roja, papel pintado, mostrador en z=-3 (x -2..2), claveros detrás (pared z=-5),
    puerta de cristal a la calle en la pared derecha (x=4) y entrada al pasillo de habitaciones a la izquierda."""
    habitacion(esc, -4, 4, -5, 3, 3.0, PAPEL_PINTADO, MOQUETA, (70, 60, 52), sin=('s',), div=6)
    for sx in (-3.99, 3.99): _caja_en(esc, sx - 0.01, 0, -5, sx + 0.01, 1.0, 3, MADERA)          # zócalo de madera
    _caja_en(esc, -4, 0, -4.99, 4, 1.0, -4.97, MADERA)
    mostrador(esc, -2.0, 2.0, -3.0)
    timbre(esc, 0.9, 1.16, -3.25); lampara_mesa(esc, -1.4, 1.16, -3.3, luz)
    claveros(esc, 0.0, 1.35, -4.97, n=(4, 3), nums=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "0"], falta=falta, brillo0=brillo0)
    esc.etiquetas.append(((0.0, 2.55, -4.9), "RECEPCIÓN", 0.22, (220, 190, 110)))
    # puerta de cristal a la calle (pared derecha): hueco azul noche con lluvia
    _caja_en(esc, 3.97, 0, -0.9, 3.99, 2.3, 0.9, (50, 40, 34))
    _caja_en(esc, 3.95, 0.05, -0.8 + 1.5 * puerta_calle, 3.96, 2.25, 0.8, (18, 26, 44), emite=True)
    # pasillo de habitaciones a la izquierda (hueco oscuro) y planta
    _caja_en(esc, -3.99, 0, -3.8, -3.96, 2.4, -2.6, (10, 8, 8), emite=True)
    esc.add(prisma(0.25, 0.2, 0.5, (120, 80, 60), n=6), mover(3.3, 0.5, -4.4))
    esc.add(esfera(0.45, (40, 80, 50), 1), cadena(mover(3.3, 0.95, -4.4), escala(1, 1.3, 1)))
    luces = [Luz((-1.4, 1.6, -3.0), (120, 255, 160), 3.5, fuerza=0.9 * luz),
             Luz((0, 2.8, -1.0), (255, 200, 140), 9, fuerza=0.85 * luz),
             Luz((0, 2.6, -4.3), (255, 210, 150), 4, fuerza=0.7 * luz)]
    for fx in (-2.0, 2.0): esc.add(esfera(0.18, tuple(int(v * luz) for v in (255, 220, 160)), 1), mover(fx, 2.75, -1.0), emite=True)
    return luces

def pasillo_hotel(esc, puertas=(), luces_on=None, largo=15.0):
    """pasillo de hotel: moqueta roja, papel pintado, apliques cálidos (mismo formato de puertas que pasillo())."""
    return pasillo(esc, largo, puertas=puertas, luces_on=luces_on, col_pared=(110, 70, 64), suelo=MOQUETA, techo=(80, 70, 64), zocalo=MADERA)

def libro_reservas(img, filas, resalta=None, p_resalta=1.0, fecha="25 NOV 2026", cy=860, t=0.0):
    """libro de reservas abierto en primer plano (2D): filas (hab, nombre, noche); la fila 'resalta' se subraya en rojo."""
    d = ImageDraw.Draw(img); cx = W / 2; w, h = 960, 900
    x0, y0 = cx - w / 2, cy - h / 2
    d.rectangle((x0 + 20, y0 + 24, x0 + w + 20, y0 + h + 24), fill=(8, 6, 6))
    d.rectangle((x0, y0, x0 + w, y0 + h), fill=(236, 226, 196), outline=(90, 60, 40), width=10)
    d.line((cx, y0, cx, y0 + h), fill=(170, 150, 120), width=4)
    d.text((cx, y0 + 70), tr("RESERVAS") + " · " + fecha, font=font(48), fill=(120, 30, 30), anchor="mm")
    d.text((x0 + 50, y0 + 150), tr("HAB."), font=font(36), fill=(90, 80, 70), anchor="lm")
    d.text((x0 + 230, y0 + 150), tr("NOMBRE"), font=font(36), fill=(90, 80, 70), anchor="lm")
    for i, (hab, nom) in enumerate(filas):
        y = y0 + 240 + i * 110
        d.line((x0 + 40, y + 45, x0 + w - 40, y + 45), fill=(180, 170, 150), width=3)
        roja = (i == resalta)
        col = (40, 50, 140) if not roja else (170, 20, 20)
        d.text((x0 + 70, y), hab, font=font(64), fill=col, anchor="lm")
        d.text((x0 + 230, y), nom, font=font(58), fill=col, anchor="lm")
        if roja and p_resalta > 0:
            x1 = x0 + 220 + (w - 280) * min(1, p_resalta)
            d.line((x0 + 220, y + 38, x1, y + 38), fill=(220, 30, 30), width=9)
            d.ellipse((x0 + 30, y - 55, x0 + 120, y + 55), outline=(220, 30, 30), width=7)
    return img
