"""Si oyes esto a las 3AM — 7: "La estatua del payaso". Salón de una casa ajena (sofá, esquina, puerta de la escalera,
puerta de la cocina), la escalera y el pasillo de arriba con la puerta de los niños.
Piezas nuevas reutilizables: PAYASO + payaso() (figura de payaso de tamaño real: traje, gola, zapatones) con cara_payaso()
(cara pintada, ojos negros con pupilas de alfiler que te siguen, sonrisa demasiado ancha que se abre), salon_casa,
llamada (pantalla de llamada en curso), puerta_ninos."""
import math
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am, escalera_casa
from escenas3am3 import paredes, PISO
from escenas3am5 import _osc, fondo

PAYASO = Fig(shirt=(170, 160, 146), limb=(214, 208, 196), scale=1.32)
TRAJE = (168, 158, 142)                 # blanco sucio
PARCHE = (120, 30, 34)                  # rojo desvaído
PARCHE2 = (46, 70, 110)                 # azul desvaído
CARA = (226, 220, 204)
TELE = (120, 160, 255)                  # luz azul de la tele
COCINA = (255, 214, 140)
ESQUINA = 300                           # donde estaba el payaso
SOFA = (520, 880)
_QUIETO = pose(a1u=8, a1l=4, a2u=-8, a2l=4, l1u=6, l1l=-2, l2u=-6, l2l=-2)

def cara_payaso(F, c, r, mira=0.0, abre=0.0, sonrisa=1.0):
    """cara de payaso pintada: blanca y agrietada, ojos negros pintados con pupilas de alfiler, sonrisa roja demasiado ancha"""
    hx, hy = c
    for s_ in (-1, 1):                                                              # mechones de pelo rojo apagado
        for k, (dx, dy, rr) in enumerate(((1.0, -0.35, 0.42), (1.2, 0.05, 0.4), (1.02, 0.4, 0.34))):
            F.circle((hx + s_ * r * dx, hy + r * dy), r * rr, fill=(122, 34, 30) if k % 2 == 0 else (98, 26, 24))
    F.ellipse((hx, hy), r * 0.96, r * 1.08, fill=CARA, outline=(40, 36, 32), w=max(1, r * 0.05))
    F.line([(hx - r * 0.5, hy - r * 0.9), (hx - r * 0.35, hy - r * 0.55), (hx - r * 0.44, hy - r * 0.3)], (150, 144, 132), r * 0.035)  # grieta
    for s_ in (-1, 1):                                                              # sombras hundidas bajo la pintura
        F.ellipse((hx + s_ * r * 0.38, hy - r * 0.16), r * 0.3, r * 0.4, fill=(170, 164, 150))
        F.line([(hx + s_ * r * 0.16, hy - r * 0.62), (hx + s_ * r * 0.62, hy - r * 0.86)], (20, 16, 16), r * 0.06)   # cejas pintadas, muy altas
    for s_ in (-1, 1):                                                              # ojos: rombos negros pintados
        ex, ey = hx + s_ * r * 0.38, hy - r * 0.2
        F.poly([(ex, ey - r * 0.42), (ex + r * 0.2, ey), (ex, ey + r * 0.3), (ex - r * 0.2, ey)], fill=(6, 6, 8))
        F.line([(ex, ey + r * 0.3), (ex + s_ * r * 0.02, ey + r * 0.62)], (6, 6, 8), r * 0.06)       # lágrima pintada
        F.circle((ex + mira * r * 0.07, ey), r * 0.055, fill=(255, 255, 255))                       # pupila de alfiler
    w = r * (0.72 + 0.12 * sonrisa)
    # sonrisa pintada: media luna roja que llega casi a las orejas
    F.poly([(hx - w, hy + r * 0.18), (hx - w * 0.5, hy + r * 0.58), (hx, hy + r * 0.7), (hx + w * 0.5, hy + r * 0.58), (hx + w, hy + r * 0.18),
            (hx + w * 0.55, hy + r * 0.42), (hx, hy + r * 0.5), (hx - w * 0.55, hy + r * 0.42)], fill=(150, 22, 28))
    if abre > 0:                                                                    # la boca se abre: negra, con dientecillos
        oh = r * 0.42 * abre
        pts = [(hx - w * 0.8, hy + r * 0.32), (hx - w * 0.45, hy + r * 0.44 + oh * 0.6), (hx, hy + r * 0.5 + oh), (hx + w * 0.45, hy + r * 0.44 + oh * 0.6),
               (hx + w * 0.8, hy + r * 0.32), (hx + w * 0.45, hy + r * 0.44), (hx, hy + r * 0.48), (hx - w * 0.45, hy + r * 0.44)]
        F.poly(pts, fill=(4, 2, 4))
        n = 9
        for i in range(n):
            u = (i + 0.5) / n; tx = lerp(hx - w * 0.7, hx + w * 0.7, u); ty = hy + r * 0.47 - math.sin(u * math.pi) * r * -0.02
            F.poly([(tx - r * 0.045, ty - r * 0.02), (tx + r * 0.045, ty - r * 0.02), (tx, ty + r * 0.12 * (0.5 + abre * 0.5))], fill=(200, 194, 170))
    else:
        F.line([(hx - w * 0.8, hy + r * 0.32), (hx - w * 0.4, hy + r * 0.46), (hx, hy + r * 0.5), (hx + w * 0.4, hy + r * 0.46), (hx + w * 0.8, hy + r * 0.32)],
               (30, 4, 6), r * 0.05)
    F.circle((hx, hy + r * 0.08), r * 0.17, fill=(176, 20, 24))                       # nariz
    F.circle((hx - r * 0.05, hy + r * 0.03), r * 0.05, fill=(230, 120, 120))

def payaso(F, p, x, y, t=0.0, f=1, mira=0.0, abre=0.0, sc=1.0, cara=True, rot=0.0):
    """payaso de tamaño real: traje de parches, gola, pompones y zapatones. Quieto como una estatua."""
    old = PAYASO.scale; PAYASO.scale = 1.32 * sc
    J = PAYASO.draw(F, p, x, y, f=f, face="closed", t=t, stretch=1.12, rot=rot)
    PAYASO.scale = old
    s = sc
    (sx, sy), (hpx, hpy) = J["sh"], J["hip"]
    # traje holgado
    F.poly([(sx - 38 * s, sy - 4 * s), (sx + 38 * s, sy - 4 * s), (hpx + 62 * s, hpy + 46 * s), (hpx - 62 * s, hpy + 46 * s)], fill=TRAJE, outline=(40, 36, 32), w=4 * s)
    F.poly([(sx, sy - 4 * s), (sx + 38 * s, sy - 4 * s), (hpx + 62 * s, hpy + 46 * s), (hpx, hpy + 46 * s)], fill=PARCHE)
    for k in range(3): F.circle(((sx + hpx) / 2 - 18 * s, sy + 34 * s + k * 52 * s), 10 * s, fill=(30, 28, 30))      # botones
    # gola (cuello de volantes)
    nx, ny = J["neck"]
    for i in range(9):
        a = math.pi * (i / 8)
        F.circle((nx + math.cos(a) * 44 * s, ny + 8 * s + math.sin(a) * 10 * s - 6 * s), 15 * s, fill=(200, 194, 180), outline=(70, 64, 56), w=2 * s)
    # zapatones
    for k in ("l1f", "l2f"):
        fx, fy = J[k]
        F.ellipse((fx + f * 22 * s, fy - 6 * s), 44 * s, 18 * s, fill=(110, 20, 24), outline=(20, 6, 8), w=3 * s)
    # guantes
    for k in ("a1h", "a2h"):
        F.circle(J[k], 15 * s, fill=(206, 200, 188), outline=(40, 36, 32), w=2 * s)
    if cara: cara_payaso(F, J["head"], 44 * s, mira=mira, abre=abre)
    return J

def salon_casa(F, t, tele=1.0, cocina=0.6, payaso_x=None, huellas=False, esquina_vacia=False):
    paredes(F, col=(32, 34, 50))
    F.rect(-900, -200, ESQUINA - 120, PISO, fill=(24, 25, 38))                            # pared del fondo, más oscura (esquina)
    F.line([(ESQUINA - 120, -200), (ESQUINA - 120, PISO)], (16, 16, 26), 8)
    F.rect(-60, PISO - 600, 170, PISO, fill=(5, 5, 8))                                    # hueco de la escalera, a oscuras
    F.rect(-80, PISO - 620, 190, PISO - 600, fill=(60, 48, 40))
    F.rect(960, PISO - 600, 1220, PISO, fill=_osc(COCINA, cocina))                        # puerta de la cocina, con luz
    F.rect(940, PISO - 620, 960, PISO, fill=(60, 48, 40))
    F.rect(-900, PISO, 2000, 3000, fill=(40, 30, 30)); F.rect(-200, PISO + 10, 1100, PISO + 70, fill=(58, 38, 40))   # alfombra
    # estantería con el reloj y una foto de la familia
    F.rect(560, PISO - 640, 860, PISO - 620, fill=(70, 54, 44))
    reloj_3am(F, 640, PISO - 668, 0.25)
    F.rect(760, PISO - 720, 840, PISO - 622, fill=(90, 70, 50)); F.rect(768, PISO - 712, 832, PISO - 630, fill=(120, 130, 150))
    for dx, h in ((-18, 40), (-2, 44), (12, 26), (24, 24)): F.line([(800 + dx, PISO - 632), (800 + dx, PISO - 632 - h)], (50, 50, 60), 6)
    # sofá
    x0, x1 = SOFA
    F.rect(x0, PISO - 330, x1, PISO - 170, fill=(70, 60, 92), outline=(30, 26, 40), w=5)
    F.rect(x0 - 30, PISO - 230, x1 + 30, PISO - 60, fill=(84, 72, 110), outline=(30, 26, 40), w=5)
    for xx in (x0 - 30, x1 - 10): F.rect(xx, PISO - 260, xx + 40, PISO - 60, fill=(76, 64, 100), outline=(30, 26, 40), w=4)
    for xx in (x0, x1 - 20): F.rect(xx, PISO - 60, xx + 20, PISO, fill=(30, 24, 20))
    if huellas or esquina_vacia:                                                          # marcas de zapatones donde estaba
        for dx in (-30, 40): F.ellipse((ESQUINA + dx, PISO + 30), 40, 12, fill=(72, 52, 54))

def tu_sofa(F, t, face="neutral", f=1, x=None, jit=0.0, movil=False):
    x = x if x is not None else SOFA[0] + 140
    p = pose(l1u=90, l1l=-90, l2u=84, l2l=-88, a1u=40, a1l=50, a2u=-20, a2l=40)
    if movil: p = add(p, pose(a1u=120, a1l=150))
    J = TU.draw(F, add(p, jitter(t, jit, 3)), x, PISO - 170, f=f, face=face)
    if movil:
        hx, hy = J["a1h"]
        F.rect(hx - 10, hy - 34, hx + 12, hy + 6, fill=(30, 40, 60)); F.rect(hx - 6, hy - 30, hx + 8, hy + 2, fill=(170, 210, 255))
    return J

def llamada(F, t, quien, cx=540, cy=860, habla=0.0, rojo=0.0):
    """pantalla de llamada en curso, en tu mano"""
    F.line([(140, 1760), (360, 1260)], TU.shirt, 80); F.circle((430, 1190), 62, fill=(240, 232, 222))
    F.rect(cx - 230, cy - 420, cx + 230, cy + 420, fill=(20, 20, 26), outline=(90, 90, 100), w=8)
    F.rect(cx - 205, cy - 380, cx + 205, cy + 380, fill=_osc((22, 30, 44), 1 - 0.3 * rojo))
    F.circle((cx, cy - 220), 70, fill=(70, 80, 100)); F.circle((cx, cy - 245), 24, fill=(160, 170, 190)); F.ellipse((cx, cy - 190), 40, 24, fill=(160, 170, 190))
    F.text((cx, cy - 110), quien, 44, (235, 235, 245))
    F.text((cx, cy - 60), "00:%02d" % (14 + int(t)), 34, (150, 160, 180))
    for i in range(13):                                                                   # onda de voz
        h = 8 + habla * (14 + 50 * abs(noise(t * 9 + i * 0.7, i)))
        F.rect(cx - 156 + i * 26, cy + 60 - h, cx - 144 + i * 26, cy + 60 + h, fill=(120, 230, 150) if rojo < 0.5 else (255, 80, 80))
    F.circle((cx, cy + 270), 50, fill=(220, 40, 50))
    F.line([(cx - 24, cy + 274), (cx + 24, cy + 274)], (255, 255, 255), 10)

def puerta_ninos(F, x=200, luz=0.6):
    F.rect(x - 140, PISO - 600, x + 140, PISO, fill=(70, 56, 46), outline=(30, 24, 20), w=6)
    F.circle((x + 110, PISO - 290), 10, fill=(200, 180, 120))
    F.rect(x - 60, PISO - 470, x + 50, PISO - 380, fill=(230, 226, 210))                 # dibujo infantil pegado
    F.circle((x - 20, PISO - 430), 14, fill=(240, 200, 60)); F.line([(x + 10, PISO - 400), (x + 10, PISO - 440)], (60, 120, 200), 5)
    F.rect(x - 140, PISO - 8, x + 140, PISO, fill=_osc((255, 200, 120), luz))            # luz de la lamparita por debajo

# ---------- escenas ----------
def salon(t, D, fi):
    """primer plano de la cara del payaso, iluminada desde abajo por la tele… y se abre el plano al salón"""
    k = ease(seg(t, D * 0.15, D * 0.75))
    J0 = PAYASO.joints(_QUIETO, ESQUINA, PISO, f=1, stretch=1.12)
    hx, hy = J0["head"]
    F = Frame(fondo(), dict(x=lerp(hx, 560, k), y=lerp(hy + 10, PISO - 300, k), z=lerp(3.6, 1.05, k)))
    salon_casa(F, t)
    payaso(F, _QUIETO, ESQUINA, PISO, t=t, mira=lerp(0, 1, seg(t, D * 0.6, D * 0.8)))
    tu_sofa(F, t, face="neutral" if t < D * 0.65 else "scared", movil=True)
    tv = 0.8 + 0.2 * (noise(t * 12, 5) > -0.3)
    img = iluminar(F.finish(), F, [], glows=[((hx, hy + 120), 240, 0.7 * tv), ((620, PISO - 120), 420, 0.7 * tv), ((640, PISO - 668), 120, 0.6),
                                            ((1080, PISO - 300), 300, 0.5)], amb=0.25, warm=TELE)
    return img, dict(grain=9, flash=((255, 40, 40), 0.35 * (1 - seg(t, 0, 0.25))))

def cocina(t, D, fi):
    """vuelves de la cocina con un vaso: el payaso está más cerca del sofá; en la alfombra, las marcas de sus zapatones"""
    llega = ease(seg(t, 0, D * 0.4))
    para = t > D * 0.42
    k = ease(seg(t, D * 0.45, D))
    F = Frame(fondo(), dict(x=lerp(600, 380, k), y=lerp(PISO - 330, PISO - 260, k), z=lerp(1.05, 1.5, k)))
    salon_casa(F, t, huellas=True)
    payaso(F, _QUIETO, 440, PISO, t=t, mira=1.0)
    x = lerp(1100, 920, llega)
    J = TU.draw(F, walk(t, 0.6, 0.7) if not para else add(pose(a1u=60, a1l=70, body=-6), jitter(t, 1.5, 2)), x, PISO, f=-1,
                face="scared" if para else "neutral")
    hx, hy = J["a1h"]
    vy = hy + (40 * seg(t, D * 0.46, D * 0.6) if para else 0)
    F.rect(hx - 12, vy - 30, hx + 12, vy + 6, fill=(180, 210, 230), outline=(220, 240, 255), w=2)       # vaso de agua
    img = iluminar(F.finish(), F, [], glows=[((1090, PISO - 300), 360, 0.8), ((620, PISO - 120), 380, 0.6), ((440, PISO - 420), 200, 0.5)],
                   amb=0.24, warm=TELE)
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * k), flash=((255, 255, 255), 0.3 * max(0, 1 - abs(t - D * 0.45) / 0.15)))

def llamas(t, D, fi):
    """de espaldas al payaso, con el móvil en la oreja; detrás, el payaso ladea la cabeza"""
    F = Frame(fondo(), dict(x=lerp(560, 520, ease(t / D)), y=PISO - 300, z=lerp(1.25, 1.4, ease(t / D))))
    salon_casa(F, t, huellas=True)
    lad = ease(seg(t, D * 0.4, D * 0.8))
    payaso(F, add(_QUIETO, pose(head=lerp(0, 24, lad), body=lerp(0, 6, lad))), 440, PISO, t=t, mira=1.0)
    p = pose(l1u=90, l1l=-90, l2u=84, l2l=-88, a1u=150, a1l=150, a2u=-20, a2l=40, head=4)
    J = TU.draw(F, add(p, jitter(t, 0.8, 4)), SOFA[1] - 90, PISO - 170, f=1, face="neutral")
    hx, hy = J["a1h"]
    F.rect(hx - 6, hy - 40, hx + 14, hy + 4, fill=(30, 40, 60))
    img = iluminar(F.finish(), F, [], glows=[((620, PISO - 120), 400, 0.6), ((hx, hy), 160, 0.6), ((440, PISO - 420), 180, 0.4)],
                   amb=0.24, warm=TELE)
    return img, dict(grain=10)

def padre(t, D, fi):
    habla = seg(t, 0.1, 0.3) * (1 - seg(t, D - 0.6, D - 0.3))
    rojo = seg(t, D * 0.45, D * 0.55)
    F = Frame(gradient((14, 14, 18), (6, 6, 8)), dict(x=540 + noise(t * 40) * 6 * rojo, y=900, z=lerp(1.0, 1.15, ease(t / D))))
    llamada(F, t, tr("PADRES DE LOS NIÑOS"), habla=habla, rojo=rojo)
    img = iluminar(F.finish(), F, [], glows=[((540, 860), 560, 1.0)], amb=0.25, warm=(170, 200, 255))
    return img, dict(grain=8, tint=((255, 0, 30), 0.2 * rojo))

def vacia(t, D, fi):
    """giras la cabeza: la esquina está vacía. Solo las marcas de los zapatones… y el hueco de la escalera"""
    k = ease(seg(t, 0, D * 0.35))
    z = lerp(1.3, 1.7, ease(seg(t, D * 0.35, D)))
    F = Frame(fondo(), dict(x=lerp(820, 300, k), y=PISO - 300, z=z))
    salon_casa(F, t, esquina_vacia=True)
    J = TU.draw(F, add(pose(l1u=90, l1l=-90, l2u=84, l2l=-88, a1u=60, a1l=60, a2u=-20, a2l=40, head=-6), jitter(t, 2, 4)),
                SOFA[1] - 90, PISO - 170, f=-1, face="scared")
    hit = t > D * 0.45
    img = iluminar(F.finish(), F, [], glows=[((620, PISO - 120), 380, 0.6), ((ESQUINA, PISO - 200), 300, 0.75), ((ESQUINA, PISO + 30), 160, 0.6), ((60, PISO - 300), 200, 0.1)],
                   amb=0.22, warm=TELE)
    return img, dict(grain=11, flash=((255, 255, 255), 0.5 * max(0, 1 - (t - D * 0.45) / 0.25)) if hit else None,
                     tint=((255, 0, 30), 0.18 * hit))

def escalera(t, D, fi):
    """subes corriendo; abajo, cada vez que no miras, el payaso aparece un poco más arriba"""
    F = Frame(fondo(), dict(x=540, y=980, z=1.0))
    path = escalera_casa(F)
    F.rect(1100, 900, 1400, 1300, fill=_osc(TELE, 0.25))                                  # el salón, abajo, con la tele
    u = 0.95 - 0.85 * ease_out(seg(t, 0, D * 0.9))
    x, y = path(u)
    TU.draw(F, run(t, 1.3), x, y, f=-1, face="scared")
    # el payaso: aparece a saltos (nunca se le ve moverse)
    pasos = [(0.35, 1.0), (0.55, 0.86), (0.75, 0.72), (0.9, 0.6)]
    up = None
    for fr, uu in pasos:
        if t > D * fr: up = uu
    if up is not None:
        px, py = path(up) if up < 1 else (1020, 1300)
        payaso(F, _QUIETO, px + 30, py, t=t, f=-1, mira=-1.0, sc=0.9)
    img = iluminar(F.finish(), F, [], glows=[((1180, 1050), 360, 0.5), ((x, y - 120), 200, 0.35)] +
                   ([((path(up)[0] if up < 1 else 1020, (path(up)[1] if up < 1 else 1300) - 300), 180, 0.4)] if up else []),
                   amb=0.16, warm=TELE)
    salto = any(abs(t - D * fr) < 0.06 for fr, _ in pasos)
    return img, dict(grain=11, glitch=0.35 if salto else 0.0, tint=((255, 0, 30), 0.1 * (up is not None)))

def _arriba(F, t):
    paredes(F, col=(30, 30, 44))
    puerta_ninos(F, 200, luz=0.6 + 0.2 * (noise(t * 3, 2) > 0))
    F.rect(1060, PISO - 300, 1300, PISO, fill=(6, 6, 10))                                 # hueco de la escalera, detrás

def detras(t, D, fi):
    """en la puerta de los niños, de espaldas a la escalera: la cara del payaso aparece justo detrás de ti y sonríe"""
    hit = t >= D * 0.5
    sh = 14 * hit * (1 - seg(t, D * 0.65, D * 0.9))
    k = ease(seg(t, 0, D * 0.5)); k2 = ease(seg(t, D * 0.5, D * 0.8))
    tx = 420
    J0 = PAYASO.joints(pose(body=-14, head=-10, a1u=75, a1l=25, a2u=55, a2l=35), 600, PISO, f=-1, stretch=1.12)
    hx, hy = J0["head"]
    F = Frame(fondo(), dict(x=lerp(480, (tx + hx) / 2 + 40, k2) + noise(t * 30) * sh, y=lerp(PISO - 330, hy + 80, k2), z=lerp(1.3, 2.1, k2) + 0.1 * k,
                            sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    _arriba(F, t)
    if t > D * 0.2:                                                                       # ya está ahí, inclinado sobre ti
        payaso(F, pose(body=-14, head=-10, a1u=75, a1l=25, a2u=55, a2l=35), 600, PISO, t=t, f=-1, mira=-1.0, abre=ease(seg(t, D * 0.5, D * 0.75)))
    TU.draw(F, add(pose(a1u=80, a1l=10, a2u=10, a2l=10, head=-4 if not hit else 6), jitter(t, 1.0 + 2 * hit, 5)), tx, PISO, f=-1,
            face="neutral" if not hit else "scared")
    img = iluminar(F.finish(), F, [], glows=[((200, PISO - 10), 220, 0.6), ((hx, hy), 160 + 80 * hit, 0.4 + 0.4 * hit), ((tx, PISO - 260), 180, 0.35)],
                   amb=0.18, warm=(255, 200, 150))
    return img, dict(grain=12, flash=((255, 255, 255), max(0, 1 - (t - D * 0.5) / 0.25)) if hit else None,
                     glitch=0.4 if hit and fi % 3 and t < D * 0.8 else 0.0, tint=((255, 0, 30), 0.22 * hit))

def final(t, D, fi):
    """te has dado la vuelta: tú y el payaso, frente a frente, sin moveros. No puedes dejar de mirarlo."""
    F = Frame(fondo(), dict(x=500, y=lerp(PISO - 250, PISO - 240, ease(t / D)), z=1.35))
    _arriba(F, t)
    luz = 0.6 + 0.4 * (noise(t * 6, 7) > -0.5)
    payaso(F, pose(body=-10, head=-8, a1u=40, a1l=20, a2u=25, a2l=30), 640, PISO, t=t, f=-1, mira=-1.0, abre=0.35)
    TU.draw(F, add(pose(body=-6, a1u=40, a1l=60, a2u=-30, a2l=50), jitter(t, 1.5, 8)), 380, PISO, f=1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((200, PISO - 10), 240, 0.6 * luz), ((560, PISO - 420), 260, 0.45 * luz)], amb=0.2, warm=(255, 200, 150))
    pp = ease_back(seg(t, D * 0.5, D * 0.6)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 250, 1040, 620), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI VES ALGO QUE"), 315, 64, (255, 255, 255)), (tr("NO DEBERÍA ESTAR AHÍ…"), 395, 64, (255, 255, 255)),
                                 (tr("NO LE DES"), 480, 92, (255, 40, 50)), (tr("LA ESPALDA"), 565, 92, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 645, 850, 735), 26, fill=(230, 30, 50))
        d.text((540, 690), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.25 * pp if pp > 0 else 0), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(salon=salon, cocina=cocina, llamas=llamas, padre=padre, vacia=vacia, escalera=escalera, detras=detras, final=final)
PAUSA = dict(salon=0.6, cocina=0.8, llamas=0.4, padre=0.8, vacia=0.9, escalera=0.6, detras=1.1, final=2.6)
