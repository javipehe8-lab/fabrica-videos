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

def ficha_final(img, nombre, oficio, fecha, regla_rota, p=1.0, t=0.0):
    """tarjeta del final drástico: sello REGLA ROTA + ficha de la víctima (desaparecido). Distinta de la de 3AM."""
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
    txt = tr("DESAPARECIDO"); fs = 96
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
