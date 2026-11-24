"""REGLAS 2 — Hotel, recepción de noche: "Nunca des la llave de la habitación 0." (formato: ver reglas.md)"""
import math, random
from PIL import ImageDraw, ImageFilter
from motor import *
from motor3d import *
from escenarios3d import *
from turno3d import cliente, monitor, sonrisa

G = __import__("guionreglas2" + ("_en" if IDIOMA == "en" else ""))
BLAZER = (44, 54, 96)                       # uniforme azul marino de recepción
PIEL = (222, 196, 176)
PELO = (40, 28, 22)
ABRIGO = (46, 50, 54)                       # el huésped: abrigo largo empapado
PIEL_H = (176, 180, 178)                    # piel gris, demasiado pálida
CHARCO = (40, 22, 30)

def lucia(esc, p, x, z, yaw=0.0, cara="neutral", y=0.0):
    def melena(e, cab, u):
        e.add(esfera(u(30), PELO, 1), cadena(cab, mover(0, u(4), -u(6)), escala(1.06, 1.02, 1.0)))
        e.add(caja(u(40), u(46), u(14), PELO), cadena(cab, mover(0, -u(22), -u(18))))          # melena por la espalda
    return humano(esc, p, x=x, z=z, yaw=yaw, ropa=BLAZER, piel=PIEL, pantalon=(30, 32, 44), cara=cara, extra_cabeza=melena, y=y)

def huesped(esc, p, x, z, yaw=0.0, cara="neutral"):
    return cliente(esc, p, x, z, yaw=yaw, cara=cara, abrigo=ABRIGO, piel=PIEL_H, capucha=False, alto=1.06)

def charcos(esc, pts, r=0.28):
    for i, (x, z) in enumerate(pts):
        esc.add(caja(r * (1 + 0.3 * math.sin(i * 2.1)), 0.01, r * 0.8, CHARCO), mover(x, 0.012, z), sesgo=0.1)

def gotas(img, cx, cy, ancho, alto, t, n=14, semilla=4):
    """gotas que caen del abrigo (2D)"""
    d = ImageDraw.Draw(img); rng = random.Random(semilla)
    for i in range(n):
        x = cx + rng.uniform(-ancho / 2, ancho / 2); v = rng.uniform(500, 900); f = (t * v / alto + rng.random()) % 1
        y = cy + f * alto
        d.line((x, y, x, y + 26), fill=(150, 170, 200), width=5)
    return img

def lobby(luz=1.0, brillo0=0.0, falta=(), charco=()):
    esc = escena(niebla=((16, 10, 10), 6.0, 20.0), amb=0.16)
    L = vestibulo(esc, luz=luz, brillo0=brillo0, falta=falta)
    charcos(esc, charco)
    return esc, L

def parpadeo(t, f=4): return 1.0 if int(t * f) % 2 == 0 else 0.3
POSE_DA = dict(STAND, a2u=-70, a2l=20)        # brazo extendido hacia delante (dar la llave)
POSE_COGE = dict(STAND, a1u=-62, a1l=26)

# ---------- escenas ----------
def arranque(t, D, fi):
    k = ease(min(1, t / D))
    esc, L = lobby(brillo0=parpadeo(t, 5), charco=[(0.3, -2.1), (0.8, -1.6)])
    huesped(esc, dict(STAND, head=12, a2u=-55, a2l=10), -0.05, -2.2, yaw=math.pi)         # de espaldas, en primer plano
    cam = Camara(ojo=(0.45, 1.95, lerp(-0.6, -0.9, k)), mira=(0.35, 1.6, -4.97), fov=lerp(58, 52, k))
    img = etiquetas(esc.render(cam, L + [Luz((0.6, 1.5, -4.6), (255, 50, 40), 1.6, fuerza=0.6 * parpadeo(t, 5))]), esc, cam)
    img = aclarar(img, 1.1, 0.9)
    img = gotas(img, 380, 900, 300, 800, t)
    return rotulo_regla(img, 1, G.REGLA, p=1.0), dict(grain=8)

def entra(t, D, fi):
    k = ease(min(1, t / D))
    x = lerp(3.5, 0.6, k); z = lerp(0.2, -2.3, k)
    esc, L = lobby(charco=[(lerp(3.5, 0.6, f), lerp(0.2, -2.3, f)) for f in (0.0, 0.3, 0.6) if f < k])
    huesped(esc, walk(t, 0.45, 0.5) if k < 0.97 else STAND, x, z, yaw=math.atan2(0.6 - 3.5, -2.3 - 0.2) + 0.0)
    lucia(esc, STAND, -0.3, -3.8, yaw=0.0, cara="neutral")
    cam = Camara(ojo=(lerp(-2.6, -2.0, k), 2.0, 1.4), mira=(x, 1.3, z), fov=50)
    img = etiquetas(esc.render(cam, L), esc, cam)
    return aclarar(img, 1.2), dict(grain=8)

def pide(t, D, fi):
    habla = seg(t, D * 0.48, D * 0.55)
    esc, L = lobby(charco=[(0.3, -2.1)])
    cab = huesped(esc, dict(STAND, head=lerp(25, 0, seg(t, D * 0.3, D * 0.5))), 0.2, -2.3, yaw=math.pi)
    cam = Camara(ojo=(-0.15 + 0.01 * math.sin(t * 2), 1.62, -3.75), mira=(0.2, 1.55, -2.3), fov=lerp(46, 34, ease(t / D)))
    img = aclarar(esc.render(cam, L + [Luz((0.2, 2.2, -1.6), (200, 210, 255), 3, fuerza=0.6)]), 1.25)
    img = gotas(img, W / 2 + 120, 1050, 300, 500, t, n=10)
    return img, dict(grain=10, tint=((40, 60, 140), 0.12 + 0.1 * habla), glitch=0.2 if habla and fi % 7 == 0 else 0.0)

def libro(t, D, fi):
    esc, L = lobby()
    cam = Camara(ojo=(0.0, 1.9, -3.9), mira=(0.0, 1.0, -2.5), fov=60)
    img = aclarar(esc.render(cam, L), 1.1).filter(ImageFilter.GaussianBlur(9))
    filas = [("1", "Sr. Gómez"), ("4", "M. Ruiz"), ("7", "Fam. Sanz"), ("0", "Lucía Ferrer")]
    p = seg(t, D * 0.35, D * 0.75)
    img = libro_reservas(img, filas, resalta=3 if p > 0 else None, p_resalta=p, cy=820)
    return img, dict(grain=8, tint=((255, 0, 30), 0.12 * seg(t, D * 0.7, D)))

def llave(t, D, fi):
    k = seg(t, D * 0.35, D * 0.8)
    esc, L = lobby(charco=[(0.4, -2.1), (0.9, -1.9)], falta=("0",))
    lucia(esc, dict(STAND, a2u=lerp(-14, -70, seg(t, D * 0.2, D * 0.4)), a2l=20), -0.45, -3.75, yaw=0.0)
    huesped(esc, dict(STAND, head=8, a1u=lerp(14, -62, seg(t, D * 0.55, D * 0.8)), a1l=26), 0.35, -2.3, yaw=math.pi)
    kx, kz = lerp(-0.2, 0.15, k), lerp(-3.35, -2.75, k)                                    # la llave cruza el mostrador
    esc.add(caja(0.03, 0.02, 0.12, (220, 190, 90)), mover(kx, 1.2, kz), sesgo=0.8)
    esc.add(caja(0.1, 0.02, 0.08, (180, 20, 20)), mover(kx, 1.2, kz + 0.09), sesgo=0.8)
    esc.etiquetas.append(((kx, 1.3, kz + 0.1), "0", 0.06, (255, 230, 230)))
    temb = 0.006 * math.sin(t * 40)
    cam = Camara(ojo=(3.7 + temb, 1.75, -3.0), mira=(-0.1, 1.3, -3.05), fov=56)
    img = etiquetas(aclarar(esc.render(cam, L + [Luz((0.0, 1.6, -2.7), (255, 220, 170), 2.5, fuerza=0.8)]), 1.25), esc, cam)
    return img, dict(grain=9)

def _pasillo_cctv(t, D, quien_x=None, quien_z=None, abierta=0.0, luz0=0.0, apagado=0.0):
    esc = escena(niebla=((12, 8, 8), 5.0, 22.0), amb=0.12)
    on = [1 if i < 4 - int(apagado * 5) else 0 for i in range(5)]
    puertas = [(-2.5, "1", 1), (-5.5, "4", -1), (-8.5, "7", 1), (-11.5, "9", -1), (-14.0, "0", 1, abierta, luz0)]
    L = pasillo_hotel(esc, puertas=puertas, luces_on=on)
    if quien_x is not None:
        lucia(esc, walk(t, 0.5, 0.55), quien_x, quien_z, yaw=math.pi - 0.15)
    cam = Camara(ojo=(-1.0, 2.6, -4.0), mira=(0.6, 0.9, -14.0), fov=52)
    return esc, cam, L

def camara(t, D, fi):
    k = ease(seg(t, 0.0, D * 0.75))
    entra_ = seg(t, D * 0.72, D * 0.82)
    dentro = entra_ >= 1
    esc, cam, L = _pasillo_cctv(t, D, None if dentro else lerp(0.0, 0.75, k), None if dentro else lerp(-6.5, -13.7, k),
                                abierta=0.0 if dentro else 0.7, luz0=0.0 if dentro else 1.0)
    pant = cctv(aclarar(etiquetas(esc.render(cam, L), esc, cam), 1.6, 0.75), 2, "03:14:" + f"{int(20 + t):02d}")
    fondo = aclarar(lobby()[0].render(Camara(ojo=(0.0, 1.9, -3.9), mira=(0.0, 1.3, -2.0), fov=60), lobby()[1]), 1.1).filter(ImageFilter.GaussianBlur(10))
    img = monitor(fondo, pant, t=t, caja_=(70, 470, 1010, 1170))
    d = ImageDraw.Draw(img)
    d.text((W / 2, 1290), tr("PASILLO · PLANTA 1"), font=font(48), fill=(220, 220, 210), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    img = negro(img, seg(t, D * 0.88, D))
    golpe = D * 0.82 <= t < D * 0.9
    return img, dict(grain=12, glitch=0.5 if golpe else 0.0, tint=((255, 0, 30), 0.2 * entra_))

def manana(t, D, fi):
    k = ease(min(1, t / D))
    esc = escena(niebla=((60, 56, 50), 7.0, 24.0), amb=0.32)
    L = vestibulo(esc, luz=0.6, falta=("0",))
    cab = lucia(esc, dict(STAND, head=-4), 0.0, -3.75, yaw=0.0)
    cam = Camara(ojo=(0.0, 1.68, lerp(-1.4, -2.3, k)), mira=(0.0, 1.62, -3.75), fov=lerp(40, 30, k))
    img = aclarar(esc.render(cam, L + [Luz((0.5, 2.5, 0.5), (255, 245, 225), 9, fuerza=0.9)]), 1.2)
    img = sonrisa(img, cam, cab, p=ease(seg(t, D * 0.2, D * 0.7)), ancho=2.3)
    return img, dict(grain=7, tint=((255, 230, 200), 0.08))

def final(t, D, fi):
    esc, cam, L = _pasillo_cctv(t, D, apagado=1.0, luz0=0.35 * parpadeo(t, 3))
    img = cctv(etiquetas(esc.render(cam, L + [Luz((0.9, 1.4, -14.0), (255, 60, 50), 3.0, fuerza=parpadeo(t, 3))]), esc, cam), 2, tr("NOCHE SIGUIENTE") + " 03:14")
    img = ficha_final(img, G.NOMBRE, G.OFICIO, G.FECHA, G.REGLA, p=ease_back(seg(t, 0.1, 0.6)), t=t, sello=G.SELLO)
    return img, dict(grain=10)

ESCENA_FN = dict(arranque=arranque, entra=entra, pide=pide, libro=libro, llave=llave, camara=camara, manana=manana, final=final)
PAUSA = dict(arranque=0.3, entra=0.3, pide=0.5, libro=0.4, llave=0.4, camara=0.8, manana=0.6, final=1.8)
