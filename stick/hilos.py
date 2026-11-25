"""Piezas del formato HILOS MALDITOS (ver hilos.md): fondos 3D en bucle + tarjetas de un foro PROPIO del canal.
El foro es ficticio y del canal ("h/relatos", logo HM): no imita a Reddit ni a ninguna web real.

    carretera(T, figura=fn(esc), faros=1.0)   -> fondo: conducir de noche entre pinos (T = tiempo global, bucle continuo)
    tarjeta_post(img, POST, p, t)             -> el post completo (arranque)
    cabecera_post(img, POST)                  -> mini cabecera arriba durante la historia
    tarjeta_edit(img, texto, POST, p, t, dur) -> "EDIT:" final escrito poco a poco
    movil_2d(img, nombre, t, sonando, segundos) -> móvil con llamada entrante / en curso
    sigueme(img, t, D)                        -> botón final "SÍGUEME PARA MÁS HILOS"
"""
import math, random
from PIL import Image, ImageDraw
from motor import *
from motor3d import *
from turno3d import aclarar

FD = "/usr/share/fonts/opentype/inter/"
def fnt(size, peso="Bold"): return font(size, FD + f"Inter-{peso}.otf")
ROJO_HM = (196, 22, 40)

# ---------------- fondo 3D: carretera de noche ----------------
VEL = 14.0          # m/s

def carretera(T, figura=None, faros=1.0, vel=VEL):
    dist = T * vel
    esc = Escena(niebla=((10, 13, 22), 7.0, 42.0), amb=0.10)
    off = dist % 1.0
    for i in range(-1, 46):                                                                  # asfalto en baldosas de 1 m (luz suave, sin bandas)
        z = -(i * 1.0) + off - 0.5
        for xx in range(8): esc.add(plano(1.0, 1.0, (62, 62, 66)), mover(-3.5 + xx, 0, z), fondo=True)
        for s in (-1, 1):
            esc.add(plano(30.0, 1.0, (30, 38, 28)), mover(s * 19.0, -0.02, z), fondo=True)
            esc.add(plano(0.2, 1.0, (225, 225, 215)), mover(s * 3.7, 0.01, z))              # líneas de borde
    sp = 9.0
    for idx in range(int(dist // sp) - 1, int((dist + 80) // sp) + 1):                      # línea discontinua
        z = -(idx * sp - dist)
        esc.add(plano(0.22, 3.0, (235, 235, 222)), mover(0, 0.01, z))
    sp = 6.5
    for idx in range(int(dist // sp) - 1, int((dist + 82) // sp) + 1):                      # pinos
        for s in (-1, 1):
            r = random.Random(idx * 2 + (s > 0))
            if r.random() < 0.15: continue
            z = -(idx * sp - dist) + r.uniform(-2, 2); x = s * r.uniform(5.2, 11.0); h = r.uniform(5.5, 9.5)
            esc.add(caja(0.35, 1.6, 0.35, (50, 38, 30), base=True), mover(x, 0, z))
            esc.add(prisma(0.05, r.uniform(1.3, 2.0), h, (28, 50 + r.randint(-6, 8), 34), n=5), mover(x, 1.2, z))
    sp = 25.0
    for idx in range(int(dist // sp) - 1, int((dist + 80) // sp) + 1):                      # balizas con reflectante
        z = -(idx * sp - dist)
        for s in (-1, 1):
            esc.add(caja(0.12, 1.0, 0.12, (210, 210, 204), base=True), mover(s * 4.4, 0, z))
            esc.add(caja(0.09, 0.14, 0.03, (255, 150, 40) if s > 0 else (235, 235, 235)), mover(s * 4.4, 0.85, z + 0.07), emite=True)
    if figura: figura(esc)
    sway = 0.12 * math.sin(T * 0.37) + 0.04 * math.sin(T * 1.3)
    cam = Camara(ojo=(1.8 + sway, 1.25 + 0.015 * math.sin(T * 9), 0.0), mira=(1.5 + sway * 0.5, 0.95, -30), fov=62,
                 roll=0.012 * math.sin(T * 0.5))
    L = [Luz((1.8 + dx, 0.7, -0.5), (255, 244, 220), 34.0, dir=(0, -0.12, -1), cono=30, fuerza=1.7 * faros) for dx in (-0.65, 0.65)]
    L.append(Luz((1.8, 0.8, -6.0), (255, 240, 220), 12.0, fuerza=0.5 * faros))
    return aclarar(esc.render(cam, L), 1.25, 0.85)

# ---------------- tarjetas del foro ----------------
def _envuelve(d, txt, f, ancho):
    out, cur = [], ""
    for w in txt.split():
        prueba = (cur + " " + w).strip()
        if d.textlength(prueba, font=f) <= ancho: cur = prueba
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

def _avatar(d, cx, cy, r, letra="N", col=(90, 70, 150)):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col, outline=(255, 255, 255), width=3)
    d.text((cx, cy + 1), letra, font=fnt(int(r * 1.05), "Black"), fill=(255, 255, 255), anchor="mm")

def _cabecera(d, x, y, POST, grande=True):
    s = 1.0 if grande else 0.82
    _avatar(d, x + 34 * s, y + 34 * s, 32 * s, POST["usuario"][0].upper())
    d.text((x + 82 * s, y + 18 * s), f"h/{POST['sub']}", font=fnt(int(32 * s), "Bold"), fill=(240, 240, 242), anchor="lm")
    d.text((x + 82 * s, y + 52 * s), f"{POST['usuario']} · {POST['hace']}", font=fnt(int(27 * s), "Regular"), fill=(150, 152, 160), anchor="lm")

def _logo_hm(d, x, y):
    d.rounded_rectangle((x - 118, y - 26, x + 118, y + 26), 14, fill=ROJO_HM)
    d.text((x, y + 1), "HILOS MALDITOS", font=fnt(26, "Black"), fill=(255, 255, 255), anchor="mm")

def _capa_escalada(img, capa, p, cy):
    if p >= 0.999: img.paste(capa, (0, 0), capa); return img
    if p <= 0.01: return img
    w, h = capa.size; sw, sh = max(1, int(w * p)), max(1, int(h * p))
    c2 = capa.resize((sw, sh))
    img.paste(c2, ((w - sw) // 2, int(cy - cy * p)), c2); return img

def tarjeta_post(img, POST, p=1.0, t=0.0, cy=820):
    img = img.convert("RGB"); capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(capa)
    ft = fnt(60, "Bold"); lineas = _envuelve(d, POST["titulo"], ft, 860)
    h = 120 + len(lineas) * 74 + 130; y0 = cy - h // 2; x0, x1 = 60, 1020
    d.rounded_rectangle((x0, y0, x1, y0 + h), 30, fill=(22, 22, 26, 245), outline=(70, 70, 78), width=3)
    _cabecera(d, x0 + 34, y0 + 30, POST)
    _logo_hm(d, x1 - 150, y0 + 64)
    for i, ln in enumerate(lineas):
        d.text((x0 + 40, y0 + 130 + i * 74), ln, font=ft, fill=(250, 250, 252), anchor="lt")
    fy = y0 + h - 64
    d.rounded_rectangle((x0 + 34, fy - 32, x0 + 300, fy + 32), 32, fill=(44, 44, 52))
    d.polygon([(x0 + 66, fy - 14), (x0 + 82, fy + 10), (x0 + 50, fy + 10)], fill=(255, 90, 60))
    d.text((x0 + 167, fy), POST["votos"], font=fnt(30, "Bold"), fill=(240, 240, 240), anchor="mm")
    d.polygon([(x0 + 252, fy + 12), (x0 + 268, fy - 12), (x0 + 236, fy - 12)], fill=(150, 150, 160))
    d.rounded_rectangle((x0 + 320, fy - 32, x0 + 520, fy + 32), 32, fill=(44, 44, 52))
    d.rounded_rectangle((x0 + 346, fy - 13, x0 + 380, fy + 11), 6, outline=(200, 200, 210), width=4)
    d.text((x0 + 450, fy), POST["comentarios"], font=fnt(30, "Bold"), fill=(240, 240, 240), anchor="mm")
    d.rounded_rectangle((x0 + 540, fy - 32, x0 + 740, fy + 32), 32, fill=(44, 44, 52))
    d.text((x0 + 640, fy), "Compartir", font=fnt(28, "SemiBold"), fill=(220, 220, 228), anchor="mm")
    return _capa_escalada(img, capa, p, cy)

def cabecera_post(img, POST, y0=232):
    img = img.convert("RGB"); capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(capa)
    d.rounded_rectangle((60, y0, 1020, y0 + 160), 26, fill=(18, 18, 22, 215), outline=(70, 70, 78), width=2)
    _cabecera(d, 88, y0 + 18, POST, grande=False)
    ft = fnt(36, "Bold"); tit = POST["titulo"]
    while d.textlength(tit + "…", font=ft) > 880 and " " in tit: tit = tit.rsplit(" ", 1)[0]
    d.text((92, y0 + 118), tit + ("…" if tit != POST["titulo"] else ""), font=ft, fill=(245, 245, 248), anchor="lm")
    img.paste(capa, (0, 0), capa); return img

def tarjeta_edit(img, texto, POST, p=1.0, t=0.0, dur=3.0, cy=760):
    img = img.convert("RGB"); capa = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(capa)
    cuerpo = texto.split(":", 1)[1].strip() if texto.upper().startswith("EDIT") else texto
    fb = fnt(54, "SemiBold"); lineas = _envuelve(d, cuerpo, fb, 860)
    h = 130 + 80 + len(lineas) * 70 + 40; y0 = cy - h // 2; x0, x1 = 60, 1020
    d.rounded_rectangle((x0, y0, x1, y0 + h), 30, fill=(22, 22, 26, 245), outline=(70, 70, 78), width=3)
    _cabecera(d, x0 + 34, y0 + 30, POST); _logo_hm(d, x1 - 150, y0 + 64)
    d.text((x0 + 40, y0 + 130), "EDIT:", font=fnt(58, "Black"), fill=(255, 70, 70), anchor="lt")
    n = int(len(cuerpo) * clamp(t / max(0.1, dur))); quedan = n
    for i, ln in enumerate(lineas):
        if quedan <= 0: break
        d.text((x0 + 40, y0 + 215 + i * 70), ln[:quedan], font=fb, fill=(246, 246, 248), anchor="lt"); quedan -= len(ln) + 1
    return _capa_escalada(img, capa, p, cy)

def sigueme(img, t, D):
    s = ease_back(seg(t, D - 2.2, D - 1.8)) * (1 + 0.04 * math.sin(t * 9))
    if s <= 0: return img
    d = ImageDraw.Draw(img); hw, hh = 400 * s, 72 * s
    d.rounded_rectangle((540 - hw, 1430 - hh, 540 + hw, 1430 + hh), int(40 * s), fill=ROJO_HM, outline=(255, 255, 255), width=5)
    d.text((540, 1430), "SÍGUEME PARA MÁS HILOS", font=fnt(max(8, int(50 * s)), "Black"), fill=(255, 255, 255), anchor="mm")
    return img

def movil_2d(img, nombre, t, sonando=True, segundos=0, cy=1500):
    img = img.convert("RGB"); d = ImageDraw.Draw(img)
    vx = 10 * math.sin(t * 55) if sonando and (t % 1.2) < 0.8 else 0
    x0, x1, y0, y1 = 320 + vx, 760 + vx, cy - 330, cy + 520
    d.rounded_rectangle((x0 - 14, y0 - 14, x1 + 14, y1 + 14), 64, fill=(10, 10, 12), outline=(80, 80, 86), width=4)
    d.rounded_rectangle((x0, y0, x1, y1), 52, fill=(26, 30, 40))
    cx = (x0 + x1) / 2
    d.text((cx, y0 + 50), "03:00", font=fnt(30, "SemiBold"), fill=(230, 230, 236), anchor="mm")
    d.text((cx, y0 + 120), "Llamada entrante" if sonando else f"00:{segundos:02d}", font=fnt(32, "Regular"), fill=(170, 176, 190), anchor="mm")
    d.text((cx, y0 + 185), nombre, font=fnt(68, "Bold"), fill=(255, 255, 255), anchor="mm")
    r = 74 + (8 * math.sin(t * 6) if sonando else 0)
    d.ellipse((cx - r, y0 + 330 - r, cx + r, y0 + 330 + r), fill=(120, 124, 136))
    d.text((cx, y0 + 332), nombre[0], font=fnt(80, "Black"), fill=(255, 255, 255), anchor="mm")
    if sonando:
        for bx, col in ((cx - 110, (220, 40, 50)), (cx + 110, (40, 190, 90))):
            d.ellipse((bx - 52, y0 + 500 - 52, bx + 52, y0 + 500 + 52), fill=col)
    else:
        d.ellipse((cx - 52, y0 + 500 - 52, cx + 52, y0 + 500 + 52), fill=(220, 40, 50))
    return img
