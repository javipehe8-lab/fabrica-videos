"""REGLAS 5 — Almacén de paquetería en Black Friday: "Si sale un paquete con tu dirección, no lo abras." (formato: ver reglas.md)"""
import math
from PIL import ImageDraw, ImageFilter
from motor import *
from motor3d import *
from escenarios3d import *
from escenarios3d import _caja_en

G = __import__("guionreglas5" + ("_en" if IDIOMA == "en" else ""))
CHALECO = (214, 200, 40)                      # chaleco reflectante del mozo
PIEL = (206, 170, 140)
PELO = (40, 30, 24)
PANT = (44, 48, 60)
MANITA = (196, 204, 210)                      # piel gris pálida de lo que hay dentro
BX, BZ, BY, S = 0.0, -6.0, 0.8, 1.6            # la caja: sobre la cinta, escala 1,6 (0,88 x 0,61 x 0,67 m)
TOPE = BY + 0.38 * S                           # altura de la tapa
ETQ = "DIEGO R."

def diego(esc, p, x, z, yaw=0.0, y=0.0, cara="neutral"):
    cab = humano(esc, p, x=x, z=z, y=y, yaw=yaw, ropa=CHALECO, piel=PIEL, pantalon=PANT, cara=cara, pelo=PELO)
    s = 1.75 / 3.06; u = lambda v: v / 100 * s
    base = cadena(mover(x, y, z), rot_y(yaw), mover(0, u(L["ul"] + L["ll"] + 6), 0), rot_x(math.radians(p.get("body", 0))))
    for yy in (0.18, 0.34):                    # bandas reflectantes del chaleco
        esc.add(caja(u(35), 0.035, u(21), (235, 235, 225)), cadena(base, mover(0, yy, 0)), sesgo=0.05)
    return cab

def nave(luces_on=None, t=0.0, vel=0.6, reloj="03:10"):
    esc = escena(niebla=((14, 15, 18), 7.0, 30.0), amb=0.14)
    L = nave_almacen(esc, luces_on=luces_on, reloj=reloj, largo=21.0)
    cinta(esc, 0.0, 3.0, -20.0, y=BY, t=t, vel=vel)
    return esc, L

def paquetes(esc, t, vel=0.6, hueco=(BZ - 1.2, BZ + 1.2), semilla=0):
    """cajas normales que avanzan por la cinta (sin tocar el hueco de la caja de Diego)"""
    for i in range(10):
        z = -22.0 + ((t * vel + i * 2.5 + semilla) % 25.0)
        if hueco[0] < z < hueco[1] or z > 2.6: continue
        caja_envio(esc, 0.0, BY, z, s=0.75 + 0.35 * ((i * 7) % 3) / 2, yaw=0.15 * ((i * 5) % 3 - 1))

def dedos(esc, t, f=1.0):
    """dedos pálidos que asoman por la junta de las solapas (con la rendija negra abierta)"""
    if f <= 0: return
    esc.add(caja(0.05 * f + 0.01, 0.008, 0.5, (0, 0, 0)), mover(BX, TOPE + 0.012, BZ), emite=True, sesgo=0.97)
    for k, dz in enumerate((-0.1, -0.035, 0.035, 0.1)):
        h = (0.15 + 0.05 * math.sin(t * 6 + k * 1.3)) * f
        esc.add(caja(0.055, h, 0.055, MANITA), cadena(mover(BX + 0.006 * math.sin(t * 9 + k), TOPE + h / 2, BZ + dz), rot_z(0.25 * math.sin(t * 4 + k))), sesgo=1.0)

def luz_caja(f=1.0, col=(255, 236, 200)):
    return Luz((BX + 0.6, TOPE + 1.0, BZ + 0.9), col, 4.0, fuerza=0.9 * f)

# ---------- escenas ----------
def arranque(t, D, fi):
    k = ease(min(1, t / D))
    esc, L = nave(t=0.0, reloj="03:10")
    caja_envio(esc, BX, BY, BZ, s=S, vibra=0.6 + 0.4 * math.sin(t * 3), t=t, etiqueta=ETQ)
    dedos(esc, t, f=1.0)
    cam = Camara(ojo=(lerp(1.5, 1.3, k), lerp(2.35, 2.2, k), lerp(-3.7, -4.0, k)), mira=(BX - 0.15, TOPE - 0.2, BZ - 0.05), fov=lerp(42, 37, k))
    img = etiquetas(esc.render(cam, L + [luz_caja(0.55)]), esc, cam)
    img = aclarar(img, 1.3, 0.85)
    return rotulo_regla(img, 1, G.REGLA, p=1.0, y=330), dict(grain=8)

def turno(t, D, fi):
    k = ease(min(1, t / D))
    esc, L = nave(t=t)
    paquetes(esc, t, hueco=(99, 99))
    diego(esc, walk(t, 0.5, 0.6), 1.05, lerp(-1.2, -3.4, k), yaw=math.pi)
    cam = Camara(ojo=(lerp(2.4, 2.2, k), 2.2, lerp(2.2, 1.4, k)), mira=(0.3, 2.2, -10), fov=58)
    img = etiquetas(esc.render(cam, L), esc, cam)
    return aclarar(img, 1.3, 0.85), dict(grain=8)

def etiqueta(t, D, fi):
    esc, L = nave(t=0.0)
    caja_envio(esc, BX, BY, BZ, s=S, t=t)
    diego(esc, dict(STAND, body=20, a1u=50, a2u=50, a1l=30, a2l=30, head=15), BX + 0.85, BZ, yaw=-math.pi / 2)
    cam = Camara(ojo=(1.6, 2.0, BZ + 1.8), mira=(BX, TOPE, BZ), fov=50)
    img = aclarar(esc.render(cam, L + [luz_caja()]), 1.2).filter(ImageFilter.GaussianBlur(8))
    img = etiqueta_envio(img, "Diego Romero", ["C/ Olmo 14, 2º B", "28005 Madrid", tr("PESO: 78 kg")], cy=760,
                         p_resalta=ease(seg(t, D * 0.45, D * 0.75)), t=t, remite=tr("REMITE: —"))
    return img, dict(grain=7)

def voz(t, D, fi):
    k = ease(min(1, t / D))
    esc, L = nave(t=0.0)
    caja_envio(esc, BX, BY, BZ, s=S, vibra=1.0 if t > D * 0.35 else 0.3, t=t, etiqueta=ETQ)
    dedos(esc, t, f=ease(seg(t, D * 0.4, D * 0.6)))
    inc = ease(seg(t, 0.1, D * 0.5))
    diego(esc, dict(STAND, body=lerp(5, 22, inc), a1u=lerp(10, 40, inc), a2u=lerp(10, 40, inc), a1l=40, a2l=40, head=lerp(0, 12, inc)),
          BX + 0.9, BZ + 0.2, yaw=-math.pi / 2 - 0.5, cara="scared" if t > D * 0.45 else "neutral")
    cam = Camara(ojo=(lerp(2.3, 2.1, k), 1.95, BZ + lerp(2.6, 2.3, k)), mira=(BX + 0.4, 1.25, BZ - 0.1), fov=lerp(52, 46, k))
    img = etiquetas(esc.render(cam, L + [luz_caja(0.7)]), esc, cam)
    img = aclarar(img, 1.3, 0.85)
    return img, dict(grain=9)

def abre(t, D, fi):
    esc, L = nave(t=0.0)
    ab = ease(seg(t, D * 0.5, D * 0.8))
    corta = seg(t, D * 0.15, D * 0.5)
    caja_envio(esc, BX, BY, BZ, s=S, abierta=ab, vibra=(1 - ab), t=t, etiqueta=ETQ, vacio=True)
    diego(esc, dict(STAND, body=22, a1u=70, a2u=lerp(40, 70, ab), a1l=20 + 15 * math.sin(corta * 12), a2l=30, head=20),
          BX + 0.8, BZ, yaw=-math.pi / 2, cara="scared")
    if ab < 0.2:                                                # el cúter rajando la cinta adhesiva
        esc.add(caja(0.03, 0.03, 0.12, (220, 60, 30)), mover(BX + 0.02, TOPE + 0.04, BZ + lerp(0.3, -0.3, corta)), sesgo=1.2)
    cam = Camara(ojo=(-1.6, 2.2, BZ + 1.3), mira=(BX + 0.4, 1.4, BZ), fov=50)
    luz = L + [luz_caja(1.0 - 0.6 * ab)]
    img = etiquetas(esc.render(cam, luz), esc, cam)
    img = aclarar(img, 1.3, 0.85)
    golpe = D * 0.5 <= t < D * 0.56
    return img, dict(grain=9, flash=((255, 255, 255), 0.35) if golpe else None)

def dentro(t, D, fi):
    agarra = ease(seg(t, D * 0.15, D * 0.4))
    tira = ease(seg(t, D * 0.5, D * 0.72))
    se_fue = t > D * 0.72
    esc, L = nave(t=0.0)
    caja_envio(esc, BX, BY, BZ, s=S, abierta=1.0 if not se_fue else 1.0 - ease(seg(t, D * 0.72, D * 0.8)), vibra=1.0 if se_fue else 0.0,
               t=t, vacio=True)
    if not se_fue:
        diego(esc, dict(STAND, body=lerp(8, 70, tira), a1u=lerp(65, 100, tira), a2u=lerp(65, 100, tira), a1l=10, a2l=10, head=lerp(-18, 10, tira)),
              BX, BZ - 0.75 + 0.25 * tira, y=-0.6 * tira, yaw=0.0, cara="scared")
        for k, sx in enumerate((-0.2, 0.2)):                 # manitas que salen del negro y le agarran las muñecas
            h = 0.12 + 0.28 * agarra
            base = cadena(mover(BX + sx * 0.6, TOPE - 0.05, BZ - 0.05), rot_x(-0.6 * agarra), rot_z(-sx * 0.8))
            esc.add(prisma(0.03, 0.035, h, MANITA), cadena(base, mover(0, h, 0)), sesgo=1.0)
            esc.add(esfera(0.06, MANITA, 1), cadena(base, mover(0, h, 0)), sesgo=1.1)
    cam = Camara(ojo=(BX + 0.55, 1.95, BZ + 1.45), mira=(BX, 1.45, BZ - 0.55), fov=lerp(46, 38, agarra),
                 roll=0.08 * math.sin(t * 30) * tira)
    img = etiquetas(esc.render(cam, L + [Luz((BX + 0.4, TOPE + 0.3, BZ + 0.4), (200, 214, 255), 3.0, fuerza=0.6)]), esc, cam)
    img = aclarar(img, 1.35, 0.85)
    img = negro(img, seg(t, D * 0.9, D))
    return img, dict(grain=11, tint=((255, 0, 30), 0.14 * tira), glitch=0.35 if tira > 0 and fi % 5 == 0 else 0.0,
                     flash=((255, 255, 255), 0.4) if D * 0.72 <= t < D * 0.77 else None)

def camara(t, D, fi):
    k = seg(t, 0.0, D)
    esc, L = nave(t=t, vel=0.5)
    z = BZ + 2.5 * k
    caja_envio(esc, BX, BY, z, s=S, etiqueta=ETQ, vibra=0.8 if D * 0.55 < t < D * 0.68 else 0.0, t=t)
    paquetes(esc, t, vel=0.5, hueco=(z - 1.3, z + 1.3))
    esc.add(caja(0.6, 0.03, 0.75, CHALECO), cadena(mover(1.0, 0.015, BZ + 0.3), rot_y(0.4)), emite=True, sesgo=0.1)        # su chaleco en el suelo
    esc.add(caja(0.08, 0.04, 0.2, (30, 30, 32)), cadena(mover(1.35, 0.03, BZ + 0.3), rot_y(1.1)), sesgo=0.2)    # el escáner
    cam = Camara(ojo=(2.0, 4.4, BZ + 4.2), mira=(0.3, 0.5, BZ + 0.3), fov=50)
    img = etiquetas(esc.render(cam, L), esc, cam)
    img = cctv(aclarar(img, 1.45, 0.8), 4, f"03:1{min(9, 4 + int(t))}:{int(t * 7) % 60:02d}")
    d = ImageDraw.Draw(img)
    d.text((W / 2, 1270), tr("CINTA 2 · MUELLE B"), font=font(48), fill=(220, 220, 210), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    img = negro(img, seg(t, D * 0.9, D))
    return img, dict(grain=13, glitch=0.3 if fi % 11 == 0 else 0.0)

def final(t, D, fi):
    esc = escena(niebla=((60, 58, 54), 5.0, 20.0), amb=0.3)
    habitacion(esc, -1.6, 1.6, -4.0, 2.5, 2.6, (196, 184, 160), (120, 92, 66), (180, 176, 166), sin=('s',), div=4)
    _caja_en(esc, -0.55, 0, -3.99, 0.55, 2.1, -3.97, (250, 246, 230), emite=True)                    # la puerta de la calle, abierta: luz de mañana
    caja_envio(esc, 0.0, 0.0, -2.9, s=S, etiqueta=ETQ)
    humano(esc, dict(STAND, a1u=35, a1l=40, head=12), x=0.85, z=-2.2, yaw=-2.4, ropa=(140, 110, 150), piel=(214, 190, 170),
           pantalon=(60, 60, 80), pelo=(80, 50, 30), cara="neutral")
    cam = Camara(ojo=(-0.9, 1.7, 0.9), mira=(0.1, 0.5, -2.9), fov=52)
    img = esc.render(cam, [Luz((0, 2.0, -3.6), (255, 246, 226), 7.0, fuerza=1.0), Luz((0, 2.4, 0.5), (255, 230, 200), 6.0, fuerza=0.5)])
    img = aclarar(etiquetas(img, esc, cam), 1.15)
    if t > 1.4:
        img = ficha_final(img, G.NOMBRE, G.OFICIO, G.FECHA, G.REGLA, p=ease_back(seg(t, 1.4, 1.9)), t=t, sello=G.SELLO)
    return img, dict(grain=9)

ESCENA_FN = dict(arranque=arranque, turno=turno, etiqueta=etiqueta, voz=voz, abre=abre, dentro=dentro, camara=camara, final=final)
PAUSA = dict(arranque=0.3, turno=0.3, etiqueta=0.4, voz=0.5, abre=0.5, dentro=0.6, camara=0.8, final=1.8)
