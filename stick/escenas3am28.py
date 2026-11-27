"""Si oyes esto a las 3AM — 28: "La palabra secreta". Los dos cuartos de la historia 23 (el de tu hermana a la izquierda,
el tuyo a la derecha con la cama alta, la mesilla con el reloj y el armario), la pantalla de la llamada, el recuerdo cálido
de cuando elegisteis la palabra y el telefonillo del recibidor.
Piezas nuevas reutilizables: HERMANA + hermana_tumbada / hermana_sentada (chica con melena y pijama rosa), pantalla_hermana
(llamada en curso a pantalla completa, con onda de voz y casilla de palabra secreta que se rellena y se valida),
telefonillo (portero automático en la pared, con auricular y botón de abrir que se ilumina), movil_dentro (un móvil
encendido dentro de la rendija del armario)."""
import math
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, pelo_mama
from escenas3am3 import paredes, PISO
from escenas3am5 import _osc, manta, tu_tumbado, COLCHON, HUECO
from escenas3am23 import (dos_cuartos, armario_puertas, cama_hermano, fondo, ARM0, ARMW, ARMH, MUROX0, MUROX1,
                          HCAMA0, HCAMA1, LUNA, ROJO)

AZUL = (150, 200, 255)
CALIDO = (255, 200, 140)
VERDE = (60, 200, 110)
HERMANA = Fig(shirt=(214, 120, 170), scale=0.8)
PELO_H = (60, 36, 26)

# ---------- piezas ----------
def _pelo(F, J, sc):
    hx, hy = J["head"]; r = L["head"] * sc
    F.d.chord([*F.P(hx - r - 3 * sc, hy - r - 4 * sc), *F.P(hx + r + 3 * sc, hy + r - 8 * sc)], 180, 360, fill=PELO_H)
    for s_ in (-1, 1):
        F.line([(hx + s_ * r * 0.95, hy - r * 0.2), (hx + s_ * r * 1.05, hy + r * 1.3)], PELO_H, 12 * sc)

def hermana_tumbada(F, t, face="scared", movil=True, jit=0.0):
    """tu hermana en su cama (la del cuarto de la izquierda), con el móvil encendido delante de la cara"""
    p = add(pose(a1u=120, a1l=60, a2u=10, a2l=20), jitter(t, jit, 3))
    J = HERMANA.draw(F, p, HCAMA1 - 250, COLCHON - 12, f=-1, rot=90, snap=False, face=face, t=t)
    _pelo(F, J, HERMANA.scale)
    F.poly([(HCAMA1 - 270, COLCHON - 32), (HCAMA0 - 8, COLCHON - 20), (HCAMA0 - 8, HUECO - 4), (HCAMA1 - 270, HUECO - 4)], fill=(150, 80, 120))
    if movil:
        hx, hy = J["a1h"]
        F.rect(hx - 9, hy - 20, hx + 9, hy + 20, fill=(20, 20, 26)); F.rect(hx - 5, hy - 16, hx + 5, hy + 16, fill=AZUL)
        return J, (hx, hy)
    return J, J["head"]

def hermana_sentada(F, t, x, face="happy", susurra=0.0):
    """sentada en el borde de tu cama, mirando hacia ti (izquierda), con la mano junto a la boca"""
    p = pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=lerp(20, 150, susurra), a1l=lerp(30, 120, susurra), a2u=-20, a2l=30, head=-8 * susurra)
    J = HERMANA.draw(F, add(p, jitter(t, 0.6, 7)), x, COLCHON - 6, f=-1, snap=False, face=face, t=t)
    _pelo(F, J, HERMANA.scale)
    return J

def tu_sentado(F, t, x, face="happy", jit=0.0):
    p = add(pose(l1u=90, l1l=0, l2u=86, l2l=0, a1u=40, a1l=30, a2u=-20, a2l=20, head=6), jitter(t, jit, 5))
    return TU.draw(F, p, x, COLCHON - 6, f=1, snap=False, face=face, t=t)

def tu_al_telefono(F, t, face="scared", jit=0.0):
    """TU tumbado en la cama alta con el móvil pegado a la oreja (luz azul en la cara)"""
    p = add(pose(a1u=170, a1l=165, a2u=10, a2l=20), jitter(t, jit, 5))
    J = TU.draw(F, p, 330, COLCHON - 12, f=1, rot=-90, snap=False, face=face)
    hx, hy = J["a1h"]
    F.rect(hx - 9, hy - 22, hx + 9, hy + 22, fill=(26, 30, 40)); F.rect(hx - 5, hy - 18, hx + 5, hy + 18, fill=AZUL)
    return J, (hx, hy)

def movil_dentro(F, on=1.0, x=None, y=None):
    """un móvil encendido, en vertical, dentro de la rendija del armario (lo sujeta algo)"""
    mx = ARM0 + ARMW / 2 if x is None else x
    y = PISO - ARMH + 400 if y is None else y
    F.rect(mx + 6, y - 26, mx + 34, y + 26, fill=(14, 14, 18))
    if on > 0:
        F.rect(mx + 9, y - 22, mx + 31, y + 22, fill=_osc(AZUL, 0.4 + 0.6 * on))
        F.circle((mx + 20, y + 12), 4, fill=_osc((220, 40, 50), on))                      # botón rojo de colgar
    for i in range(3):                                                                    # dedos pálidos alrededor
        F.line([(mx + 4, y - 14 + i * 12), (mx + 12, y - 16 + i * 12)], (186, 186, 182), 5)
    return (mx + 20, y)

def mis_cuartos(F, t, hermana=True, hface="scared", hjit=0.0):
    dos_cuartos(F, t, cama_h=False, poster=False)
    cama_hermano(F, vacia=False)
    F.rect(-560, 640, -360, 880, fill=(110, 60, 90), outline=(30, 20, 30), w=6)             # póster de tu hermana (una luna)
    F.circle((-460, 760), 54, fill=(230, 220, 180)); F.circle((-440, 744), 50, fill=(110, 60, 90))
    if hermana: return hermana_tumbada(F, t, face=hface, jit=hjit)
    return None, None

def pantalla_hermana(F, t, habla=0.0, segs=12, palabra=0.0, ok=0.0, vib=0.0, cx=540, cy=880):
    """llamada en curso con HERMANA. habla: onda de voz (llanto); palabra 0-1: la casilla se rellena; ok: tic verde"""
    cx += noise(t * 60) * 12 * vib
    F.line([(150, 1800), (370, 1300)], TU.shirt, 84); F.circle((430, 1230), 64, fill=(240, 232, 222))
    F.rect(cx - 240, cy - 440, cx + 240, cy + 440, fill=(20, 20, 26), outline=(90, 90, 100), w=8)
    F.rect(cx - 214, cy - 400, cx + 214, cy + 400, fill=(16, 22, 36))
    F.text((cx, cy - 345), "3:00", 54, ROJO)
    F.text((cx, cy - 268), tr("EN LLAMADA") + "  00:%02d" % segs, 32, (130, 220, 150))
    F.circle((cx, cy - 140), 78, fill=(150, 80, 120)); F.circle((cx, cy - 164), 27, fill=(240, 220, 210))
    F.ellipse((cx, cy - 104), 44, 26, fill=(240, 220, 210))
    F.d.chord([*F.P(cx - 31, cy - 194), *F.P(cx + 31, cy - 150)], 180, 360, fill=PELO_H)
    F.text((cx, cy - 20), tr("HERMANA"), 74, (240, 240, 250))
    if habla > 0:                                                                       # onda del llanto
        for i in range(13):
            h = 10 + 70 * abs(math.sin(t * 11 + i * 0.9) * math.sin(t * 3.1 + i * 0.4)) * habla
            x = cx - 180 + i * 30
            F.rect(x - 8, cy + 90 - h / 2, x + 8, cy + 90 + h / 2, fill=(230, 120, 150))
    if palabra > 0 or ok > 0:
        F.rect(cx - 190, cy + 160, cx + 190, cy + 330, fill=(28, 34, 52), outline=(70, 80, 110), w=4)
        F.text((cx, cy + 196), tr("PALABRA SECRETA"), 30, (170, 180, 210))
        n = int(7 * palabra + 0.001)
        for i in range(7):
            F.circle((cx - 132 + i * 44, cy + 262), 13, fill=(240, 240, 250) if i < n else (60, 66, 86))
        if ok > 0:
            s = ease_back(ok)
            F.circle((cx + 200, cy + 160), 56 * s, fill=VERDE, outline=(10, 60, 30), w=6)
            F.line([(cx + 200 - 26 * s, cy + 162), (cx + 200 - 6 * s, cy + 184 * 1 - 2), (cx + 200 + 28 * s, cy + 136)], (255, 255, 255), 12 * s)
    return (cx, cy)

TELX, TELY = 600, 1040
def telefonillo(F, luz=0.0, x=TELX, y=TELY):
    """portero automático en la pared del recibidor; luz: el botón de abrir (la llave) se ilumina"""
    F.rect(x - 70, y - 130, x + 70, y + 130, fill=(200, 198, 186), outline=(70, 70, 66), w=5)
    F.rect(x - 52, y - 112, x - 6, y + 100, fill=(232, 230, 220), outline=(90, 90, 86), w=4)      # auricular
    F.rect(x - 46, y - 104, x - 12, y - 64, fill=(60, 62, 64)); F.rect(x - 46, y + 52, x - 12, y + 92, fill=(60, 62, 64))
    F.line([(x - 29, y + 100), (x - 40, y + 150), (x - 20, y + 190)], (40, 40, 44), 5)              # cable rizado
    by = y + 40
    F.rect(x + 8, by - 30, x + 58, by + 30, fill=_osc((255, 220, 120), 0.35 + 0.65 * luz) if luz > 0 else (150, 148, 138),
           outline=(60, 60, 56), w=4)
    F.circle((x + 24, by), 9, outline=(40, 36, 30), w=4); F.line([(x + 32, by), (x + 50, by)], (40, 36, 30), 5)  # la llave
    F.line([(x + 44, by), (x + 44, by + 9)], (40, 36, 30), 4)
    F.rect(x + 8, y - 90, x + 58, y - 40, fill=(150, 148, 138), outline=(60, 60, 56), w=4)
    return (x + 33, by)

def regla_card(img, pp):
    if pp <= 0: return img
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((40, 130, 1040, 640), 30, fill=(0, 0, 0))
    for txt, y, fs0, col in ((tr("SI A LAS 3 ALGUIEN"), 205, 62, (255, 255, 255)), (tr("SABE VUESTRA PALABRA…"), 285, 62, (255, 255, 255)),
                             (tr("NO ABRAS"), 470, 150, (255, 40, 50))):
        fs = fs0
        while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 930: fs -= 2
        d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
    d.rounded_rectangle((230, 680, 850, 770), 26, fill=(230, 30, 50))
    d.text((540, 725), tr("SÍGUEME PARA MÁS"), font=font(50), fill=(255, 255, 255), anchor="mm")
    return img

RELOJ = (825, PISO - 222)
ARMC = (ARM0 + ARMW / 2, PISO - ARMH / 2)

# ---------- escenas ----------
def llamada(t, D, fi):
    """primer fotograma: el reloj a las 3:00 en rojo, muy cerca. Se abre el plano: tú en la cama al teléfono… y el armario
    de al lado, entreabierto (la pista)"""
    k = ease(seg(t, 0.15, D * 0.85))
    F = Frame(fondo(), dict(x=lerp(RELOJ[0], 600, k), y=lerp(RELOJ[1], 1060, k), z=lerp(3.4, 1.0, k)))
    mis_cuartos(F, t, hermana=False)
    J, ph = tu_al_telefono(F, t, face="scared", jit=0.4)
    manta(F)
    c = armario_puertas(F, t, abre=0.32)
    img = iluminar(F.finish(), F, [], glows=[((640, 610), 240, 0.5), (RELOJ, 220, 0.85), (ph, 200, 0.8), (c, 160, 0.15)], amb=0.24, warm=LUNA)
    return img, dict(grain=9, flash=(ROJO, 0.35 * (1 - seg(t, 0, 0.3))), tint=((255, 0, 30), 0.06))

def llaves(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(gradient((14, 14, 18), (6, 6, 8)), dict(x=540, y=lerp(900, 860, k), z=lerp(1.2, 1.06, k)))
    c = pantalla_hermana(F, t, habla=0.5 + 0.5 * abs(math.sin(t * 2.3)), segs=8 + int(t))
    img = iluminar(F.finish(), F, [], glows=[(c, 560, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=8, tint=((255, 0, 30), 0.06))

def palabra(t, D, fi):
    """recuerdo, hace un mes: tu hermana y tú sentados en tu cama, susurrando la palabra. Al fondo, el armario entreabierto"""
    k = ease(seg(t, 0, D))
    sus = ease(seg(t, D * 0.25, D * 0.45))
    F = Frame(fondo("m"), dict(x=lerp(800, 860, k), y=lerp(1060, 1040, k), z=lerp(1.5, 1.35, k)))
    mis_cuartos(F, t, hermana=False)
    tu_sentado(F, t, 560, face="neutral")
    J = hermana_sentada(F, t, 680, face="neutral", susurra=sus)
    c = armario_puertas(F, t, abre=0.32)
    img = iluminar(F.finish(), F, [], glows=[((620, 1000), 460, 0.75), ((825, PISO - 222), 160, 0.4)], amb=0.4, warm=CALIDO)
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.05, 0.35))
    if p > 0:
        d.rounded_rectangle((300, 250, 780, 340), 20, fill=(0, 0, 0))
        d.text((540, 295), tr("HACE UN MES"), font=font(56 * p + 1), fill=(255, 220, 160), anchor="mm")
    if sus > 0.5:                                                                        # bocadillo del susurro, sin desvelar la palabra
        hx, hy = F.P(*J["head"]); hx /= S; hy /= S
        bx, by = hx - 60, hy - 150
        a = min(1, (sus - 0.5) * 4)
        d.rounded_rectangle((bx - 150, by - 50, bx + 150, by + 50), 40, fill=(250, 246, 236), outline=(40, 30, 24), width=5)
        for i in range(7):
            if i < int(7 * a + 0.01): d.ellipse((bx - 108 + i * 36 - 10, by - 10, bx - 108 + i * 36 + 10, by + 10), fill=(40, 30, 24))
    return img, dict(grain=7, tint=((255, 170, 80), 0.18))

def pides(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(gradient((14, 14, 18), (6, 6, 8)), dict(x=540, y=lerp(860, 940, k), z=lerp(1.06, 1.18, k)))
    pal = seg(t, D * 0.3, D * 0.6); ok = seg(t, D * 0.68, D * 0.8)
    c = pantalla_hermana(F, t, habla=0.8 * pal * (1 - ok) + 0.3, segs=14 + int(t), palabra=pal, ok=ok)
    img = iluminar(F.finish(), F, [], glows=[(c, 560, 1.0), ((c[0] + 200, c[1] + 160), 200, 0.5 * ok)], amb=0.25, warm=AZUL)
    return img, dict(grain=8, flash=((60, 255, 120), 0.18 * max(0, 1 - abs(t - D * 0.72) / 0.15)))

def abrir(t, D, fi):
    """recibidor a oscuras: vas al telefonillo con el móvil en la oreja; el dedo tiembla sobre el botón de abrir"""
    w = ease(seg(t, 0, D * 0.42))
    k = ease(seg(t, D * 0.4, D * 0.9))
    F = Frame(fondo(), dict(x=lerp(420, TELX + 10, k), y=lerp(1080, TELY + 30, k), z=lerp(1.4, 3.0, k)))
    paredes(F)
    F.rect(860, PISO - 560, 1100, PISO, fill=(46, 38, 32)); F.rect(884, PISO - 536, 1076, PISO, fill=(70, 50, 38))   # puerta de casa
    b = telefonillo(F, luz=0.5 + 0.5 * math.sin(t * 6) ** 2 if t > D * 0.5 else 0.0)
    x = lerp(150, 470, w)
    if w < 1:
        p = add(walk(t, 0.6, 0.7), dict(a1u=150 - walk(t, 0.6, 0.7)["a1u"], a1l=160 - 18))
    else:
        reach = ease(seg(t, D * 0.45, D * 0.65))
        p = add(pose(head=-4, a1u=150, a1l=160, a2u=lerp(-10, 88, reach), a2l=lerp(10, -6, reach)), jitter(t, 1.2, 4))
    J = TU.draw(F, p, x, PISO, f=1, face="scared", t=t)
    hx, hy = J["a1h"]
    F.rect(hx - 9, hy - 22, hx + 9, hy + 22, fill=(26, 30, 40)); F.rect(hx - 5, hy - 18, hx + 5, hy + 18, fill=AZUL)
    if w >= 1:                                                                            # el dedo, temblando sobre el botón
        fx, fy = J["a2h"]
        tx, ty = b[0] - 34 + noise(t * 30, 5) * 4, b[1] + noise(t * 30, 6) * 3
        u = ease(seg(t, D * 0.55, D * 0.75))
        ex, ey = lerp(fx, tx, u), lerp(fy, ty, u)
        F.line([(fx, fy), (ex, ey)], (240, 240, 240), 9)
        F.circle((ex, ey), 7, fill=(240, 232, 222), outline=(8, 8, 12), w=2)
    img = iluminar(F.finish(), F, [], glows=[(b, 160, 0.6 if t > D * 0.5 else 0.2), ((hx, hy), 180, 0.6), ((980, PISO - 10), 200, 0.2)],
                   amb=0.2, warm=AZUL)
    return img, dict(grain=10, tint=((255, 0, 30), 0.08 * k))

def mensaje(t, D, fi):
    F = Frame(gradient((14, 14, 18), (6, 6, 8)), dict(x=540, y=900, z=lerp(1.0, 1.1, ease(t / D))))
    c = movil_msg(F, t, D, tr("HERMANA"), [tr("NO ABRAS."), tr("ESTOY EN MI CAMA."), tr("ESA PALABRA SOLO"), tr("LA DIJIMOS UNA VEZ.")])
    img = iluminar(F.finish(), F, [], glows=[(c, 560, 1.0)], amb=0.25, warm=AZUL)
    return img, dict(grain=8, tint=((255, 0, 30), 0.16 * seg(t, D * 0.6, D)))

def armario(t, D, fi):
    """la cámara cruza la pared: tu hermana en su cama con el móvil… y tu cuarto vacío, con el armario entreabierto"""
    k = ease(seg(t, 0, D * 0.8))
    F = Frame(fondo(), dict(x=lerp(-360, ARMC[0], k), y=lerp(1040, ARMC[1] + 40, k), z=lerp(1.5, 1.9, k)))
    J, ph = mis_cuartos(F, t, hface="scared", hjit=0.6)
    manta(F)
    c = armario_puertas(F, t, abre=0.32 + 0.04 * math.sin(t * 2.2), jit=1.5 * seg(t, D * 0.7, D))
    img = iluminar(F.finish(), F, [], glows=[(ph, 220, 0.85), ((640, 610), 240, 0.45), (RELOJ, 200, 0.7), (c, 220, 0.25)], amb=0.22, warm=LUNA)
    return img, dict(grain=10, tint=((255, 0, 30), 0.12 * seg(t, D * 0.5, D)))

def susurro(t, D, fi):
    """la puerta del armario se abre un poco más: dentro brilla un móvil en llamada. Unos ojos. Unos dedos en el canto"""
    abre = 0.32 + 0.68 * ease(seg(t, D * 0.05, D * 0.3))
    mov = seg(t, D * 0.15, D * 0.3)
    ojos = seg(t, D * 0.42, D * 0.5)
    hit = seg(t, D * 0.42, D * 0.47)
    k = ease(seg(t, 0, D))
    sh = 10 * hit * (1 - seg(t, D * 0.5, D * 0.75))
    F = Frame(fondo(), dict(x=ARMC[0] + 20 + noise(t * 30) * sh, y=lerp(PISO - 300, PISO - 330, k), z=lerp(2.0, 2.9, k),
                            sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    mis_cuartos(F, t, hermana=False)
    c = armario_puertas(F, t, abre=abre, ojos=ojos, dedos=seg(t, D * 0.5, D * 0.65))
    gap = 46 * ease(abre)
    m = movil_dentro(F, on=mov, x=ARM0 + ARMW / 2 - 6 + gap * 0.4 - 14, y=PISO - ARMH + 420)
    img = iluminar(F.finish(), F, [], glows=[(m, 260, 1.2 * mov), (c, 220, 0.3 + 0.3 * ojos), (RELOJ, 160, 0.5)], amb=0.2, warm=LUNA)
    golpe = hit >= 1
    return img, dict(grain=11, flash=((255, 255, 255), max(0, 1 - (t - D * 0.44) / 0.25)) if golpe else None,
                     glitch=0.4 if golpe and fi % 3 and t < D * 0.65 else 0.0, tint=((255, 0, 30), 0.12 + 0.16 * hit))

def final(t, D, fi):
    """plano general: tú en la puerta de tu cuarto, con el móvil en la mano, mirando el armario abierto. La regla"""
    k = ease(seg(t, 0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(1000, 760, k), y=lerp(1060, 1010, k), z=lerp(1.6, 1.05, k)))
    mis_cuartos(F, t, hermana=False)
    manta(F)
    c = armario_puertas(F, t, abre=1.0, ojos=1.0, dedos=1.0)
    m = movil_dentro(F, on=0.7 + 0.3 * math.sin(t * 5) ** 2, x=ARM0 + ARMW / 2 - 6 + 46 * 0.4 - 14, y=PISO - ARMH + 420)
    J = TU.draw(F, add(pose(body=-8, head=4, a1u=60, a1l=70, a2u=-20, a2l=20), jitter(t, 2.5, 6)), 620, PISO, f=1, face="scared", t=t)
    img = iluminar(F.finish(), F, [], glows=[(c, 240, 0.5), (m, 180, 0.8), (RELOJ, 200, 0.6), (J["head"], 160, 0.3), ((640, 610), 220, 0.4)],
                   amb=0.24, warm=LUNA)
    pp = ease_back(seg(t, D * 0.42, D * 0.52)) * (1 + 0.03 * math.sin(t * 25))
    return img, dict(grain=10, tint=((255, 0, 30), 0.22 * pp if pp > 0 else 0.08), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0,
                     overlay=lambda im: regla_card(im, pp))

from escenas3am1 import movil_msg
ESCENA_FN = dict(llamada=llamada, llaves=llaves, palabra=palabra, pides=pides, abrir=abrir, mensaje=mensaje, armario=armario,
                 susurro=susurro, final=final)
PAUSA = dict(llamada=0.4, llaves=0.5, palabra=0.5, pides=0.4, abrir=0.5, mensaje=0.6, armario=0.6, susurro=0.9, final=2.4)
