"""Si oyes esto a las 3AM — 12: "El flash". Se va la luz y haces fotos con el flash del móvil. Tu cuarto de lado (cama alta de
la historia 5) a oscuras, y las FOTOS en primera persona (desde tu cama: ventana con cortinas, escritorio, puerta, la percha
con tu abrigo y, delante, el piecero y tus pies bajo la manta), con la interfaz de la cámara encima. La cosa es la CANTORA de
la historia 6 (alta, camisón oscuro, pelo negro, cara pálida): en cada foto está más cerca. Al final te hace la foto ella,
desde el techo, con tu móvil.
Piezas nuevas reutilizables: cuarto_pov (tu cuarto visto desde la cama), pies_cama (piecero + tus pies bajo la manta),
percha (perchero con abrigo), ui_camara (interfaz de cámara de móvil sobre la imagen), galeria (móvil con una foto cenital de
tu cama y miniaturas), techo (escena dibujada al revés y girada 180°: algo colgado del techo)."""
import math, random
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am
from escenas3am3 import paredes, PISO
from escenas3am5 import _osc, cama_alta, tu_tumbado, fondo, P4, COLCHON, HUECO, CAMA_X0, CAMA_X1
from escenas3am6 import cantora, mano_dedo
from escenas3am11 import _bulto
from escenas3am2 import PIEL

ROJO = (255, 40, 40)
FLASH = (226, 234, 255)          # luz del flash (blanca y fría)
PANTALLA = (150, 200, 255)       # luz de pantalla
ABRIGO = (58, 64, 54)
QUIETA = pose(head=4, a1u=6, a1l=2, a2u=-6, a2l=2, l1u=4, l1l=-2, l2u=-4, l2l=-2)          # de pie, brazos largos colgando

# ---------- piezas ----------
def _cuarto_lado(F, t, reloj=True):
    """tu cuarto de lado (historia 5) con el reloj que se puede apagar"""
    paredes(F, col=(26, 28, 44))
    F.rect(940, PISO - 560, 1180, PISO, fill=(6, 6, 10))
    F.rect(760, PISO - 190, 890, PISO, fill=(70, 54, 44), outline=(40, 30, 24), w=4)
    reloj_3am(F, 825, PISO - 222, 0.3, on=reloj)
    cama_alta(F, t=t)

def percha(F, x=880, abrigo=True):
    """perchero de pie con tu abrigo colgado (con capucha): de lejos parece una persona"""
    F.line([(x, PISO), (x, PISO - 640)], (70, 52, 40), 12)
    for s_ in (-1, 1):
        F.line([(x, PISO - 30), (x + s_ * 70, PISO)], (70, 52, 40), 10)
        F.line([(x, PISO - 620), (x + s_ * 34, PISO - 650)], (70, 52, 40), 8)
    if abrigo:
        F.circle((x, PISO - 592), 40, fill=_osc(ABRIGO, 0.85))                                    # capucha
        F.poly([(x - 46, PISO - 580), (x + 46, PISO - 580), (x + 72, PISO - 250), (x - 72, PISO - 250)], fill=ABRIGO)
        F.line([(x, PISO - 560), (x, PISO - 260)], _osc(ABRIGO, 0.7), 4)
        for s_ in (-1, 1): F.line([(x + s_ * 48, PISO - 570), (x + s_ * 64, PISO - 330)], _osc(ABRIGO, 0.75), 22)   # mangas

def cuarto_pov(F, t, abrigo=True):
    """tu cuarto visto desde la cama: ventana con cortinas, escritorio y silla, puerta y la percha"""
    paredes(F, col=(44, 46, 66))
    F.rect(110, 420, 390, 860, fill=(12, 16, 34), outline=(76, 66, 58), w=10)                     # ventana
    F.line([(250, 420), (250, 860)], (76, 66, 58), 8); F.line([(110, 640), (390, 640)], (76, 66, 58), 8)
    F.circle((180, 510), 24, fill=(180, 186, 206))
    F.rect(70, 390, 430, 404, fill=(60, 50, 44))
    F.poly([(84, 400), (176, 400), (156, 900), (74, 920)], fill=(104, 42, 52))                    # cortinas
    F.poly([(324, 400), (416, 400), (426, 920), (344, 900)], fill=(104, 42, 52))
    F.rect(90, PISO - 330, 470, PISO - 300, fill=(96, 72, 54))                                    # escritorio
    for lx in (106, 454): F.line([(lx, PISO - 300), (lx, PISO)], (80, 60, 46), 12)
    F.rect(160, PISO - 380, 260, PISO - 330, fill=(30, 32, 40)); F.rect(170, PISO - 372, 250, PISO - 338, fill=(18, 20, 26))   # pantalla apagada
    F.line([(380, PISO - 420), (380, PISO - 200)], (60, 46, 36), 12); F.rect(330, PISO - 210, 430, PISO - 190, fill=(70, 52, 40))  # silla
    F.line([(340, PISO - 190), (340, PISO)], (60, 46, 36), 10); F.line([(420, PISO - 190), (420, PISO)], (60, 46, 36), 10)
    F.rect(560, PISO - 600, 790, PISO, fill=(84, 66, 52), outline=(40, 30, 24), w=8)               # puerta cerrada
    F.rect(584, PISO - 570, 766, PISO - 330, outline=(66, 52, 40), w=5); F.rect(584, PISO - 290, 766, PISO - 40, outline=(66, 52, 40), w=5)
    F.circle((764, PISO - 300), 11, fill=(196, 170, 100))
    percha(F, 880, abrigo)

def pies_cama(F):
    """primer plano: el piecero de tu cama y tus pies bajo la manta"""
    F.rect(-300, 1330, 1400, 1400, fill=(86, 62, 46), outline=(40, 28, 20), w=5)
    F.rect(-300, 1395, 1400, 2700, fill=(56, 66, 110))
    for x in (400, 640): F.ellipse((x, 1420), 120, 64, fill=(68, 80, 128))
    F.line([(-300, 1395), (1400, 1395)], (90, 104, 160), 6)

def ui_camara(n, hora="3:01", flash_on=True):
    """overlay: interfaz de la cámara del móvil (rayo del flash, hora en rojo, esquinas de enfoque, botón y miniatura)"""
    def dibuja(img):
        d = ImageDraw.Draw(img)
        d.rectangle((0, 240, W, 330), fill=(0, 0, 0))
        bx, by = 90, 285                                                                           # rayo del flash
        d.polygon([(bx + 10, by - 28), (bx - 12, by + 4), (bx + 2, by + 4), (bx - 8, by + 30), (bx + 16, by - 6), (bx + 2, by - 6)],
                  fill=(255, 220, 60) if flash_on else (120, 120, 120))
        d.text((W - 80, 285), hora, font=font(40), fill=ROJO, anchor="rm")
        d.text((540, 285), f"{tr('FOTO')} {n}", font=font(34), fill=(240, 240, 240), anchor="mm")
        for (x, y, sx, sy) in ((150, 420, 1, 1), (930, 420, -1, 1), (150, 1240, 1, -1), (930, 1240, -1, -1)):   # esquinas
            d.line([(x, y), (x + 70 * sx, y)], fill=(255, 255, 255), width=5); d.line([(x, y), (x, y + 70 * sy)], fill=(255, 255, 255), width=5)
        d.rectangle((0, 1720, W, H), fill=(0, 0, 0))
        d.ellipse((540 - 64, 1810 - 64, 540 + 64, 1810 + 64), outline=(255, 255, 255), width=8)
        d.ellipse((540 - 48, 1810 - 48, 540 + 48, 1810 + 48), fill=(255, 255, 255))
        d.rectangle((150, 1770, 230, 1850), fill=(60, 60, 70), outline=(200, 200, 200), width=3)
        return img
    return dibuja

def _ella(F, x, y, t, sc=1.0, p=None, f=-1, abre=0.5):
    """la cosa (cantora de la historia 6), quieta, con los brazos larguísimos colgando"""
    J = cantora(F, add(p or QUIETA, jitter(t, 0.8, 7)), x, y, t=t, f=f, sc=sc, snap=True)
    return J

def _foto(t, D, fi, x, sc, cam, n, hora, mira=0.0, extra_rojo=0.0):
    F = Frame(fondo(), cam)
    cuarto_pov(F, t)
    J = _ella(F, x, PISO if sc < 1.2 else 1430, t, sc=sc, p=add(QUIETA, pose(body=12 * mira, head=10 * mira)))
    pies_cama(F)
    img = iluminar(F.finish(), F, [], glows=[((540, 1600), 820, 1.0), ((540, 1000), 520, 0.5)], amb=0.38, warm=FLASH)
    return img, dict(grain=9, flash=((255, 255, 255), 0.95 * (1 - seg(t, 0, 0.35))), tint=((180, 200, 255), 0.06 + extra_rojo),
                     overlay=ui_camara(n, hora))

def galeria(F, t, cx=540, cy=900, pelo=1.0):
    """móvil a pantalla completa con la galería: la última foto es tu cama vista desde arriba, con pelo negro colgando
    por el borde de arriba. Debajo, las miniaturas de tus fotos (la silueta cada vez más grande)"""
    F.rect(cx - 250, cy - 450, cx + 250, cy + 450, fill=(20, 20, 26), outline=(90, 90, 100), w=8)
    F.rect(cx - 226, cy - 424, cx + 226, cy + 424, fill=(8, 8, 10))
    F.text((cx - 140, cy - 380), tr("FOTOS"), 34, (230, 230, 236))
    F.text((cx + 140, cy - 380), "3:07", 34, ROJO)
    x0, y0, x1, y1 = cx - 216, cy - 330, cx + 216, cy + 220                                        # la foto
    F.rect(x0, y0, x1, y1, fill=(150, 158, 196))                                                   # sábana (cenital)
    F.rect(x0 + 50, y0 + 40, x1 - 50, y0 + 190, fill=(226, 230, 244))                              # almohada
    F.circle((cx, y0 + 150), 74, fill=(8, 8, 12)); F.circle((cx, y0 + 150), 68, fill=(240, 240, 240))   # tu cara, mirando arriba
    for dx in (-24, 24):
        F.circle((cx + dx, y0 + 138), 15, fill=(255, 255, 255)); F.circle((cx + dx, y0 + 134), 7, fill=(10, 10, 14))
    F.rect(x0 + 20, y0 + 175, x1 - 20, y1 - 10, fill=(62, 74, 124))                                # la manta hasta la nariz
    F.line([(x0 + 20, y0 + 178), (x1 - 20, y0 + 178)], (90, 104, 160), 8)
    for s_ in (-1, 1): F.ellipse((cx + s_ * 60, y0 + 182), 26, 16, fill=(240, 240, 240))           # tus dedos agarrando la manta
    F.line([(cx - 120, y0 + 300), (cx + 100, y0 + 460)], (82, 96, 150), 6)
    for i in range(9):                                                                              # mechones de pelo negro colgando
        hx = x0 + 30 + i * 47 + (i % 2) * 10
        F.line([(hx, y0 - 2), (hx + 6 * math.sin(t * 2 + i), y0 + (80 + (i * 37) % 110) * pelo)], (8, 8, 10), 18)
    F.rect(x0, y0, x1, y1, outline=(255, 255, 255), w=3)
    F.text((cx, y1 + 40), tr("AHORA"), 30, (200, 200, 210))
    for i, (sx, s_) in enumerate(((-150, 0.3), (-50, 0.55), (50, 0.85))):                            # miniaturas
        tx, ty = cx + sx, y1 + 130
        F.rect(tx - 44, ty - 44, tx + 44, ty + 44, fill=(46, 48, 66), outline=(120, 120, 130), w=2)
        F.rect(tx - 44, ty + 10, tx + 44, ty + 44, fill=(20, 20, 30))
        F.ellipse((tx + 20 - i * 18, ty - 4), 7 * s_ + 3, 30 * s_ + 6, fill=(30, 30, 36))
        F.circle((tx + 20 - i * 18, ty - 34 * s_ - 4), 7 * s_ + 2, fill=PIEL)
    F.rect(cx + 6, y1 + 86, cx + 94, y1 + 174, fill=(150, 158, 196), outline=(255, 255, 255), w=4)
    return (cx, cy)

# ---------- escenas ----------
def corte(t, D, fi):
    """primer fotograma: el reloj 3:00 en rojo muy cerca; se va la luz; se enciende tu móvil en la cama"""
    off = t > D * 0.22
    k = ease(seg(t, D * 0.3, D * 0.62))
    F = Frame(fondo(), dict(x=lerp(825, 470, k), y=lerp(PISO - 222, COLCHON - 120, k), z=lerp(3.2, 1.5, k)))
    _cuarto_lado(F, t, reloj=not off or (fi % 4 == 0 and t < D * 0.3))
    on = seg(t, D * 0.4, D * 0.5)
    J = tu_tumbado(F, t, face="scared" if on > 0 else "closed", cuelga=0.0, sienta=ease(seg(t, D * 0.3, D * 0.55)), jit=1.0 * on)
    hx, hy = J["a1h"]
    F.rect(hx - 10, hy - 24, hx + 10, hy + 6, fill=(18, 18, 22))
    F.rect(hx - 7, hy - 21, hx + 7, hy + 3, fill=_osc(PANTALLA, 0.2 + 0.8 * on))
    gl = [((825, PISO - 222), 200, 0.8)] if not off else []
    gl += [((hx, hy), 230, 0.9 * on)] if on > 0 else []
    img = iluminar(F.finish(), F, [], glows=gl, amb=0.3 if not off else 0.07, warm=(255, 120, 120) if not off else PANTALLA)
    return img, dict(grain=10, flash=(ROJO, 0.22 * (1 - seg(t, 0, 0.3))), dark=0.0 if not off else 0.08)

def foto1(t, D, fi):
    k = ease(seg(t, 0.3, D))
    return _foto(t, D, fi, 1010, 0.92, dict(x=lerp(560, 760, k), y=lerp(960, 900, k), z=lerp(1.0, 1.45, k)), 1, "3:01")

def oscuro(t, D, fi):
    """a oscuras: solo tu cara iluminada por la pantalla. Al fondo, un instante, dos puntos que brillan"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(420, 520, k), y=lerp(COLCHON - 120, COLCHON - 150, k), z=lerp(1.7, 1.45, k)))
    _cuarto_lado(F, t, reloj=False)
    J = tu_tumbado(F, t, face="scared", cuelga=0.0, sienta=1.0, jit=1.5)
    hx, hy = J["a1h"]
    F.rect(hx - 10, hy - 24, hx + 10, hy + 6, fill=(18, 18, 22)); F.rect(hx - 7, hy - 21, hx + 7, hy + 3, fill=PANTALLA)
    ojos = seg(t, D * 0.55, D * 0.62) - seg(t, D * 0.85, D * 0.92)
    if ojos > 0:
        for ex in (880, 902): F.circle((ex, PISO - 500), 3.5, fill=_osc((240, 240, 250), ojos))
    img = iluminar(F.finish(), F, [], glows=[((hx, hy), 260, 0.9), ((891, PISO - 500), 60, 0.6 * ojos)], amb=0.06, warm=PANTALLA)
    return img, dict(grain=12, dark=0.06)

def foto2(t, D, fi):
    k = ease(seg(t, 0.3, D))
    return _foto(t, D, fi, 700, 1.0, dict(x=lerp(600, 720, k), y=lerp(950, 860, k), z=lerp(1.05, 1.6, k)), 2, "3:03", mira=0.4)

def foto3(t, D, fi):
    """a los pies de tu cama, inclinada sobre el piecero, mirando a cámara"""
    k = ease(seg(t, 0.2, D))
    hit = t < 0.5
    sh = 12 * (1 - seg(t, 0.2, 0.9))
    F = Frame(fondo(), dict(x=560 + noise(t * 30) * sh, y=lerp(1000, 1110, k), z=lerp(1.1, 2.1, k), sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    cuarto_pov(F, t)
    p = pose(body=0, head=6, a1u=24, a1l=14, a2u=-24, a2l=-14, l1u=4, l1l=-2, l2u=-4, l2l=-2)
    J = cantora(F, add(p, jitter(t, 0.8, 7)), 560, 1700, t=t, f=-1, sc=1.45, snap=True)
    pies_cama(F)
    for hx, hy in (J["a1h"], J["a2h"]):                                                              # dedos largos agarrando el piecero
        F.line([(hx, hy), (hx, 1336)], PIEL, 14)
        for i in range(4): F.line([(hx - 20 + i * 13, 1330), (hx - 24 + i * 14, 1378)], PIEL, 8)
    img = iluminar(F.finish(), F, [], glows=[((540, 1600), 820, 1.0), (J["head"], 300, 0.6)], amb=0.4, warm=FLASH)
    return img, dict(grain=10, flash=((255, 255, 255), 1.0 * (1 - seg(t, 0, 0.35))), tint=((255, 0, 30), 0.16),
                     glitch=0.35 if 0.35 < t < 1.0 and fi % 3 else 0.0, overlay=ui_camara(3, "3:05"))

def tapas(t, D, fi):
    """te tapas entero; tu móvil queda encima de la almohada, con la pantalla encendida"""
    k = ease(seg(t, 0, D))
    tapa = ease(seg(t, 0, D * 0.3))
    F = Frame(fondo(), dict(x=lerp(430, 360, k), y=lerp(COLCHON - 120, COLCHON - 90, k), z=lerp(1.35, 1.6, k)))
    _cuarto_lado(F, t, reloj=False)
    if tapa < 1: tu_tumbado(F, t, face="scared", cuelga=0.0, jit=1.5)
    if tapa > 0: _bulto(F, t)
    px, py = 170, COLCHON - 74
    F.rect(px - 34, py - 10, px + 34, py + 8, fill=(18, 18, 22)); F.rect(px - 30, py - 7, px + 30, py + 5, fill=PANTALLA)
    img = iluminar(F.finish(), F, [], glows=[((px, py - 20), 240, 1.0), ((420, COLCHON - 40), 300, 0.25)], amb=0.07, warm=PANTALLA)
    return img, dict(grain=11, dark=0.05)

def clic(t, D, fi):
    """silencio; una mano larga y pálida baja desde arriba, coge tu móvil de la almohada y se lo lleva hacia el techo"""
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(400, 300, k), y=lerp(COLCHON - 120, COLCHON - 260, k), z=lerp(1.6, 1.4, k)))
    _cuarto_lado(F, t, reloj=False)
    _bulto(F, t, tiembla=1.6)
    baja = ease(seg(t, D * 0.2, D * 0.5)); sube = ease(seg(t, D * 0.62, D * 0.95))
    px, py = 170, COLCHON - 74 - 700 * sube
    if baja > 0:
        tip = (px + 10, lerp(COLCHON - 600, py - 6, baja) if sube == 0 else py - 6)
        mano_dedo(F, tip, t)
    F.rect(px - 26, py - 8, px + 26, py + 6, fill=(18, 18, 22)); F.rect(px - 22, py - 5, px + 22, py + 3, fill=PANTALLA)
    img = iluminar(F.finish(), F, [], glows=[((px, py - 20), 240, 0.8)], amb=0.06, warm=PANTALLA)
    return img, dict(grain=12, tint=((255, 0, 30), 0.12 * seg(t, D * 0.4, D)), dark=0.04)

def galeria_(t, D, fi):
    k = ease(seg(t, 0.4, D))
    F = Frame(fondo(), dict(x=540, y=lerp(900, 720, k), z=lerp(1.0, 1.55, k)))
    c = galeria(F, t, pelo=0.6 + 0.4 * seg(t, D * 0.3, D))
    img = iluminar(F.finish(), F, [], glows=[(c, 640, 1.0)], amb=0.25, warm=PANTALLA)
    return img, dict(grain=9, flash=((255, 255, 255), 1.0 * (1 - seg(t, 0, 0.45))), tint=((255, 0, 30), 0.1 + 0.12 * k),
                     glitch=0.25 if t > D * 0.75 and fi % 4 == 0 else 0.0)

def techo(F, t):
    """visto desde tu cama, mirando arriba: ella pegada al techo, encima de ti, con la cara sobre la tuya, el pelo colgando
    hacia ti, los brazos larguísimos abiertos agarrados al techo y tu móvil encendido en una mano"""
    from escenas3am2 import cara_palida
    F.rect(-900, -400, 2000, 3200, fill=(40, 40, 54))                                              # el techo
    for yy in range(-400, 3200, 160): F.line([(-900, yy), (2000, yy + 40)], (46, 46, 62), 3)
    F.circle((830, 1620), 70, fill=(66, 64, 70)); F.circle((830, 1620), 50, fill=(90, 88, 92))        # plafón apagado
    cx, cy = 540, 640
    F.poly([(cx - 150, cy - 60), (cx + 150, cy - 60), (cx + 230, -380), (cx - 230, -380)], fill=(30, 32, 38))   # camisón, hacia el fondo
    sw = 3 * math.sin(t * 1.7)
    mx, my = 1010, 680 + sw
    for s_, (ex, ey), (hx, hy) in ((-1, (130, 360), (40, 60 - sw)), (1, (950, 360), (mx, my))):
        F.line([(cx + s_ * 110, cy - 150), (ex, ey), (hx, hy)], (8, 8, 12), 52)
        F.line([(cx + s_ * 110, cy - 150), (ex, ey), (hx, hy)], PIEL, 40)
        for i in range(4):                                                                        # dedos abiertos sobre el techo
            ang = math.radians(-60 + i * 35 + (180 if s_ < 0 else 0))
            F.line([(hx, hy), (hx + math.cos(ang) * 70, hy + math.sin(ang) * 70)], PIEL, 12)
    F.rect(mx - 26, my - 44, mx + 26, my + 44, fill=(18, 18, 22)); F.rect(mx - 20, my - 38, mx + 20, my + 38, fill=FLASH)
    for i in range(13):                                                                           # pelo colgando hacia ti
        dx = -150 + i * 25
        F.line([(cx + dx, cy + 100), (cx + dx * 1.15 + 10 * math.sin(t * 1.5 + i), cy + 330 + (i * 37) % 120)], (10, 10, 14), 18)
    cara_palida(F, (cx, cy), 150, abre=0.45 + 0.25 * math.sin(t * 2))
    return (cx, cy), (mx, my)

def final(t, D, fi):
    F = Frame(fondo(), dict(x=540, y=960, z=lerp(1.0, 1.08, ease(t / D))))
    c, m = techo(F, t)
    fl = 1 - seg(t, 0, 0.4)
    img = iluminar(F.finish(), F, [], glows=[(m, 300, 1.0), (c, 480, 0.85)], amb=0.2 + 0.5 * fl, warm=FLASH)
    pp = ease_back(seg(t, D * 0.45, D * 0.55)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 1130, 1040, 1530), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI A LAS 3"), 1200, 62, (255, 255, 255)), (tr("SE VA LA LUZ…"), 1280, 62, (255, 255, 255)),
                                 (tr("NO HAGAS FOTOS"), 1410, 120, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 1580, 850, 1670), 26, fill=(230, 30, 50))
        d.text((540, 1625), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, flash=((255, 255, 255), 0.9 * fl), tint=((255, 0, 30), 0.2 * pp if pp > 0 else 0.05),
                     glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(corte=corte, foto1=foto1, oscuro=oscuro, foto2=foto2, foto3=foto3, tapas=tapas, clic=clic, galeria=galeria_, final=final)
PAUSA = dict(corte=0.4, foto1=0.6, oscuro=0.5, foto2=0.6, foto3=0.8, tapas=0.4, clic=0.6, galeria=0.8, final=2.4)
