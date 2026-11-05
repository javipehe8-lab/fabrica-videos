"""Si oyes esto a las 3AM — 6: "El vigilabebés" (ESTILO ps2). Tu cuarto (cama alta, mesilla con el reloj y el vigilabebés),
el pasillo y el cuarto de tu hermano (cuna, móvil de estrellas, ventana cerrada, cómoda con el otro aparato).
Piezas nuevas reutilizables: vigia (vigilabebés con luces de nivel y botón de hablar), cuna_bebe, cuarto_bebe, CANTORA (la cosa)."""
import math
from PIL import ImageDraw
from motor import *
from escenas5 import iluminar
from escenas3am1 import TU, reloj_3am
from escenas3am2 import cara_palida, PIEL
from escenas3am3 import paredes, PISO
from escenas3am5 import cama_alta, manta, tu_tumbado, COLCHON, HUECO, CAMA_X0, CAMA_X1, FRIA, _osc, fondo

CANTORA = Fig(shirt=(52, 54, 60), limb=PIEL, scale=1.3)        # la cosa: camisón oscuro, piel gris, demasiado alta
NANA = (150, 255, 170)                                          # verde de las luces del aparato
MESA = (760, 1040)                                              # mesilla de tu cuarto
VIGIA_TU = (950, PISO - 200)                                    # vigilabebés de tu cuarto (base)
VIGIA_BEBE = (1000, PISO - 320)                                 # el de la cuna (encima de la cómoda)
NOCHE = (255, 200, 120)                                         # lamparita del bebé

def vigia(F, x, y, s=1.0, nivel=0.0, boton=0.0, t=0.0, col=(226, 228, 232)):
    """vigilabebés: cuerpo blanco con antena, rejilla, 5 luces de nivel (verde→rojo) y botón de hablar (rojo si se pulsa)"""
    w, h = 62 * s, 170 * s
    F.line([(x + w * 0.6, y - h), (x + w * 0.75, y - h - 70 * s)], (60, 60, 66), 9 * s)                 # antena
    F.rect(x - w, y - h, x + w, y, fill=col, outline=(90, 92, 100), w=4 * s)
    F.rect(x - w, y - 14 * s, x + w, y, fill=_osc(col, 0.7))
    for r in range(3):                                                                                     # rejilla del altavoz
        for c in range(5):
            F.circle((x - 36 * s + c * 18 * s, y - h + 26 * s + r * 17 * s), 4 * s, fill=(70, 72, 80))
    n = nivel * 5
    for k in range(5):                                                                                     # luces de nivel
        on = n > k
        c = [(90, 230, 120), (90, 230, 120), (190, 240, 90), (255, 190, 60), (255, 60, 50)][k]
        F.rect(x - 40 * s + k * 17 * s, y - 72 * s, x - 28 * s + k * 17 * s, y - 56 * s, fill=c if on else (54, 58, 60))
    F.circle((x, y - 34 * s), 13 * s, fill=(255, 40, 40) if boton > 0.5 else (120, 40, 40), outline=(60, 20, 20), w=3 * s)   # botón
    return (x, y - 34 * s)

def nivel_nana(t, on=1.0):
    """luces que bailan con la nana"""
    return on * max(0.15, 0.55 + 0.35 * math.sin(t * 5.3) + 0.15 * math.sin(t * 13.1))

def mi_cuarto(F, t, nivel=0.0, boton=0.0, puerta=0.0, cama=True):
    paredes(F, col=(34, 38, 58))
    F.rect(1120, PISO - 560, 1360, PISO, fill=(6, 6, 10))                                   # puerta al pasillo
    if puerta > 0: F.rect(1120, PISO - 560, 1150, PISO, fill=_osc(FRIA, 0.35 * puerta))
    F.rect(MESA[0], PISO - 200, MESA[1], PISO, fill=(80, 60, 48), outline=(40, 30, 24), w=4)   # mesilla
    F.rect(MESA[0] + 10, PISO - 120, MESA[1] - 10, PISO - 110, fill=(50, 38, 30))
    reloj_3am(F, 830, PISO - 236, 0.32)
    vigia(F, *VIGIA_TU, s=1.0, nivel=nivel, boton=boton, t=t)
    if cama: cama_alta(F, t=t)

def cuna_bebe(F, x0=280, x1=760, t=0.0):
    """cuna de barrotes con tu hermano dormido, y el móvil de estrellas encima"""
    top, colchon = PISO - 430, PISO - 200
    F.rect(x0, colchon, x1, colchon + 40, fill=(220, 214, 200))
    F.ellipse((x0 + 120, colchon - 24), 34, 30, fill=(240, 222, 206), outline=(120, 100, 90), w=3)            # cabeza
    for dx in (-12, 12): F.line([(x0 + 120 + dx - 6, colchon - 28), (x0 + 120 + dx + 6, colchon - 28)], (60, 40, 40), 3)   # ojos cerrados
    resp = 4 * math.sin(t * 2.2)
    F.ellipse(((x0 + x1) / 2 + 40, colchon - 18), 150, 26 + resp, fill=(130, 170, 220), outline=(80, 110, 160), w=3)   # mantita
    F.rect(x0 - 24, top - 30, x0, PISO, fill=(232, 228, 220)); F.rect(x1, top - 30, x1 + 24, PISO, fill=(232, 228, 220))
    F.rect(x0, top, x1, top + 18, fill=(232, 228, 220)); F.rect(x0, colchon + 40, x1, colchon + 58, fill=(232, 228, 220))
    for bx in range(int(x0 + 30), int(x1), 44): F.line([(bx, top + 10), (bx, colchon + 48)], (232, 228, 220), 8)
    # móvil de estrellas, girando
    mx = (x0 + x1) / 2
    F.line([(x1 + 12, top - 30), (x1 + 12, top - 300), (mx, top - 300), (mx, top - 230)], (200, 200, 205), 6, round_=False)
    for k in range(3):
        a = t * 0.9 + k * 2.09
        sx = mx + 110 * math.cos(a); sz = math.sin(a)
        F.line([(mx, top - 230), (sx, top - 230 + 8 * sz)], (200, 200, 205), 4)
        F.line([(sx, top - 230 + 8 * sz), (sx, top - 150)], (200, 200, 205), 2)
        r = 22 * (0.85 + 0.15 * sz)
        F.poly([(sx + r * math.cos(math.pi / 2 + i * math.pi / 5) * (1 if i % 2 == 0 else 0.45),
                 top - 140 - r * math.sin(math.pi / 2 + i * math.pi / 5) * (1 if i % 2 == 0 else 0.45)) for i in range(10)],
               fill=(250, 220, 110))

def cuarto_bebe(F, t, nivel=0.0, luna=1.0):
    paredes(F, col=(40, 44, 70))
    for xx in range(-900, 2000, 120):                                                       # papel pintado de lunares
        for yy in range(-160, PISO - 60, 120): F.circle((xx + (yy // 120 % 2) * 60, yy), 8, fill=(50, 56, 86))
    # ventana cerrada con la luna
    F.rect(-260, PISO - 860, 120, PISO - 500, fill=(80, 70, 60))
    F.rect(-240, PISO - 840, 100, PISO - 520, fill=(16, 22, 40))
    F.circle((0, PISO - 760), 34, fill=_osc((230, 230, 210), luna))
    F.line([(-70, PISO - 840), (-70, PISO - 520)], (80, 70, 60), 14); F.line([(-240, PISO - 680), (100, PISO - 680)], (80, 70, 60), 14)
    F.rect(-60, PISO - 690, -40, PISO - 660, fill=(200, 180, 120))                             # pestillo echado
    cuna_bebe(F, t=t)
    # cómoda con la lamparita y el otro vigilabebés
    F.rect(840, PISO - 320, 1160, PISO, fill=(206, 196, 180), outline=(130, 120, 110), w=4)
    for yy in (PISO - 220, PISO - 110): F.line([(860, yy), (1140, yy)], (150, 140, 128), 4)
    F.ellipse((890, PISO - 360), 34, 40, fill=NOCHE)
    vigia(F, *VIGIA_BEBE, s=0.9, nivel=nivel, col=(214, 226, 240))

def cantora(F, p, x, y, t=0.0, f=-1, sc=1.0, snap=False, cara=True):
    """la cosa: alta, encorvada, camisón oscuro, pelo negro sobre la cara pálida"""
    old = CANTORA.scale; CANTORA.scale = 1.3 * sc
    J = CANTORA.draw(F, p, x, y, f=f, face="closed", t=t, stretch=1.25, snap=snap)
    CANTORA.scale = old
    sx, sy = J["sh"]; hx, hy = J["hip"]
    F.poly([(sx - 34 * sc, sy), (sx + 34 * sc, sy), (hx + 60 * sc, hy + 40 * sc), (hx - 60 * sc, hy + 40 * sc)], fill=(44, 46, 52))
    if cara: cara_palida(F, J["head"], 46 * sc, abre=0.5)
    return J

def mano_dedo(F, punta, t=0.0, pal=True):
    """brazo largo y pálido que entra por arriba y aprieta con un dedo"""
    px, py = punta
    c = PIEL if pal else TU.shirt
    F.line([(px + 260, py - 520), (px + 80, py - 120), (px + 30, py - 40)], c, 26)
    F.line([(px + 30, py - 40), (px + 4, py - 8)], c, 11)
    for i in range(3): F.line([(px + 36 + i * 10, py - 40), (px + 18 + i * 14, py + 6)], _osc(c, 0.85), 9)

# ---------- escenas ----------
def vigila(t, D, fi):
    k = ease(seg(t, D * 0.15, D * 0.75))
    vx, vy = VIGIA_TU
    F = Frame(fondo(), dict(x=lerp(vx - 40, 560, k), y=lerp(vy - 90, PISO - 230, k), z=lerp(3.3, 1.05, k)))
    mi_cuarto(F, t, nivel=nivel_nana(t))
    tu_tumbado(F, t, face="neutral" if t > D * 0.6 else "closed", cuelga=0.0)
    manta(F)
    for i in range(3):                                                                             # la nana saliendo del altavoz
        u = (t * 0.9 + i / 3) % 1
        F.arc((vx, vy - 130), 40 + 140 * u, 200, 340, _osc(NANA, 0.7 * (1 - u)), 5)
    img = iluminar(F.finish(), F, [], glows=[((vx, vy - 90), 230, 0.9), ((830, PISO - 236), 120, 0.6), ((400, COLCHON - 60), 260, 0.35)],
                   amb=0.3, warm=(170, 255, 190))
    return img, dict(grain=9, flash=((255, 40, 40), 0.35 * (1 - seg(t, 0, 0.25))))

def solos(t, D, fi):
    s = ease(seg(t, 0.0, D * 0.4))
    F = Frame(fondo(), dict(x=lerp(560, 600, ease(t / D)), y=lerp(PISO - 280, PISO - 320, ease(t / D)), z=lerp(1.5, 1.9, ease(t / D))))
    mi_cuarto(F, t, nivel=nivel_nana(t))
    tu_tumbado(F, t, face="scared", cuelga=0.0, sienta=s, jit=1.5)
    if s < 0.5: manta(F)
    vx, vy = VIGIA_TU
    img = iluminar(F.finish(), F, [], glows=[((vx, vy - 90), 260, 0.9), ((390, COLCHON - 140), 220, 0.5)], amb=0.28, warm=(170, 255, 190))
    return img, dict(grain=10)

def contestas(t, D, fi):
    vx, vy = VIGIA_TU
    press = seg(t, D * 0.25, D * 0.32) > 0 and t < D * 0.62
    calla = t > D * 0.62
    F = Frame(fondo(), dict(x=vx - 10, y=vy - 110, z=lerp(2.6, 3.0, ease(t / D))))
    mi_cuarto(F, t, nivel=0.0 if calla else nivel_nana(t), boton=1.0 if press else 0.0, cama=False)
    bx, by = vx, vy - 34
    k = ease(seg(t, 0, D * 0.28)) * (1 - 0.4 * ease(seg(t, D * 0.65, D)))
    F.line([(bx - 420, by + 420), (lerp(bx - 300, bx - 60, k), lerp(by + 320, by + 40, k))], TU.shirt, 50)     # tu brazo
    F.circle((lerp(bx - 280, bx - 30, k), lerp(by + 300, by + 14, k)), 30, fill=(240, 232, 222))
    img = iluminar(F.finish(), F, [], glows=[((vx, vy - 90), 260, 0.95 if not calla else 0.55)], amb=0.3,
                   warm=(255, 120, 120) if press else (170, 255, 190))
    return img, dict(grain=10, tint=((0, 0, 0), 0.25 * seg(t, D * 0.62, D * 0.7)))

def pasillo(t, D, fi):
    F = Frame(fondo(), dict(x=lerp(400, 560, ease(t / D)), y=1050, z=1.25))
    paredes(F, col=(30, 32, 46))
    F.rect(-360, PISO - 560, -120, PISO, fill=(8, 8, 12))                                     # tu cuarto, a oscuras
    F.rect(860, PISO - 580, 1100, PISO, fill=(40, 36, 34))
    F.rect(880, PISO - 560, 1080, PISO, fill=_osc(NOCHE, 0.45))                               # su cuarto: lamparita
    x = lerp(60, 700, ease(seg(t, 0, D * 0.95)))
    # la cosa cruzándose contigo hacia tu cuarto (en la sombra)
    u = seg(t, D * 0.35, D * 0.75)
    if 0 < u < 1:
        cx = lerp(980, -160, u)
        cantora(F, walk(t, 0.4, 0.5), cx, PISO, t=t, f=-1, snap=True)
    TU.draw(F, walk(t, 0.6, 0.7), x, PISO, f=1, face="scared" if u > 0.3 else "neutral")
    img = iluminar(F.finish(), F, [], glows=[((980, PISO - 280), 380, 0.7), ((x, PISO - 150), 210, 0.55)], amb=0.18, warm=NOCHE)
    roce = max(0, 1 - abs(t - D * 0.55) / 0.25)
    return img, dict(grain=11, flash=((150, 200, 255), 0.45 * roce), glitch=0.3 if roce > 0.5 and fi % 2 else 0.0)

def cuna(t, D, fi):
    k = ease(seg(t, 0, D))
    F = Frame(fondo(), dict(x=lerp(420, 520, k), y=lerp(PISO - 330, PISO - 300, k), z=lerp(1.25, 1.55, k)))
    cuarto_bebe(F, t)
    TU.draw(F, add(pose(body=6, a1u=40, a1l=60, a2u=-20, a2l=30), jitter(t, 1, 3)), 900, PISO, f=-1, face="scared")
    img = iluminar(F.finish(), F, [], glows=[((890, PISO - 360), 300, 0.85), ((520, PISO - 230), 300, 0.5), ((0, PISO - 700), 200, 0.4)],
                   amb=0.3, warm=NOCHE)
    return img, dict(grain=10)

def suena(t, D, fi):
    vx, vy = VIGIA_BEBE
    habla = t > D * 0.5
    k = ease(seg(t, 0, D * 0.5))
    F = Frame(fondo(), dict(x=lerp(700, vx - 30, k), y=lerp(PISO - 320, vy - 110, k), z=lerp(1.4, 2.9, k)))
    cuarto_bebe(F, t, nivel=nivel_nana(t * 1.6) if habla else 0.0)
    if habla:
        for i in range(3):
            u = (t * 1.2 + i / 3) % 1
            F.arc((vx, vy - 120), 30 + 120 * u, 200, 340, _osc((255, 90, 90), 0.8 * (1 - u)), 5)
    img = iluminar(F.finish(), F, [], glows=[((vx, vy - 90), 240, 0.95), ((890, PISO - 360), 200, 0.6)], amb=0.25,
                   warm=(255, 140, 140) if habla else NOCHE)
    return img, dict(grain=11, tint=((255, 0, 30), 0.2 * seg(t, D * 0.5, D)), flash=((255, 255, 255), 0.4 * max(0, 1 - abs(t - D * 0.5) / 0.15)))

def entiendes(t, D, fi):
    """tu cuarto, a oscuras: un dedo largo y pálido aprieta el botón de hablar de tu vigilabebés"""
    vx, vy = VIGIA_TU
    F = Frame(fondo(), dict(x=vx - 20, y=vy - 120, z=lerp(2.3, 3.1, ease(t / D))))
    mi_cuarto(F, t, nivel=nivel_nana(t * 1.6), boton=1.0, cama=False)
    bx, by = vx, vy - 34
    mano_dedo(F, (bx + 2, by - 6), t)
    img = iluminar(F.finish(), F, [], glows=[((vx, vy - 60), 240, 0.9)], amb=0.18, warm=(255, 120, 120))
    return img, dict(grain=12, tint=((255, 0, 30), 0.15 + 0.1 * ease(t / D)), flash=((255, 255, 255), 0.5 * (1 - seg(t, 0, 0.25))),
                     glitch=0.25 if fi % 7 == 0 else 0.0)

def tucama(t, D, fi):
    """la cosa sentada en tu cama, encorvada, con tu vigilabebés en la mano… gira la cabeza hacia ti"""
    gira = ease(seg(t, D * 0.35, D * 0.55))
    hit = t >= D * 0.55
    sh = 12 * hit * (1 - seg(t, D * 0.6, D * 0.9))
    p = pose(body=lerp(30, 8, gira), head=lerp(30, -10, gira), l1u=90, l1l=-95, l2u=84, l2l=-90, a1u=130, a1l=-70, a2u=110, a2l=-60)
    J0 = CANTORA.joints(p, 520, COLCHON + 8, f=-1, snap=False, stretch=1.25)
    hx, hy = J0["head"]
    z = lerp(1.35, 2.4, ease(seg(t, D * 0.5, D * 0.8)))
    F = Frame(fondo(), dict(x=lerp(600, hx, gira) + noise(t * 30) * sh, y=lerp(PISO - 330, hy + 90, gira), z=z,
                            sx=noise(t * 40, 1) * sh, sy=noise(t * 40, 2) * sh))
    mi_cuarto(F, t, nivel=0.0, puerta=0.8)
    F.poly([(CAMA_X0, COLCHON - 10), (CAMA_X1, COLCHON - 30), (CAMA_X1, HUECO - 4), (CAMA_X0, HUECO - 4)], fill=(60, 72, 120))  # manta revuelta
    F.rect(VIGIA_TU[0] - 70, VIGIA_TU[1] - 200, VIGIA_TU[0] + 70, VIGIA_TU[1], fill=(80, 60, 48))   # ya no está en la mesilla
    J = cantora(F, p, 520, COLCHON + 8, t=t, f=-1, cara=False)
    ax, ay = J["a1h"]
    vigia(F, ax - 10, ay + 40, s=0.55, nivel=0.0, boton=1.0)
    cara_palida(F, J["head"], 46, abre=0.4 + 0.6 * hit)
    if not hit:                                                       # de espaldas: solo pelo
        F.circle(J["head"], 52, fill=(14, 14, 18))
    img = iluminar(F.finish(), F, [], glows=[((1130, PISO - 300), 300, 0.5), (J["head"], 220 if hit else 150, 0.9 if hit else 0.45)],
                   amb=0.2, warm=FRIA)
    return img, dict(grain=12, flash=((255, 255, 255), max(0, 1 - (t - D * 0.55) / 0.25)) if hit else None,
                     glitch=0.4 if hit and fi % 3 and t < D * 0.8 else 0.0, tint=((255, 0, 30), 0.2 * hit))

def final(t, D, fi):
    F = Frame(fondo(), dict(x=560, y=lerp(PISO - 330, PISO - 310, ease(t / D)), z=1.5))
    mi_cuarto(F, t, nivel=nivel_nana(t), puerta=0.6)
    vx, vy = VIGIA_TU
    if noise(t * 4, 9) > -0.4:
        p = pose(body=10, head=-6, l1u=90, l1l=-95, l2u=84, l2l=-90, a1u=60, a1l=40, a2u=40, a2l=30)
        cantora(F, p, 520, COLCHON + 8, t=t, f=-1)
    img = iluminar(F.finish(), F, [], glows=[((vx, vy - 90), 220, 0.8), ((480, COLCHON - 160), 200, 0.4)], amb=0.18, warm=(170, 255, 190))
    pp = ease_back(seg(t, D * 0.5, D * 0.6)) * (1 + 0.03 * math.sin(t * 25))
    def regla(img):
        if pp <= 0: return img
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((40, 300, 1040, 640), 30, fill=(0, 0, 0))
        for txt, y, fs0, col in ((tr("SI ALGUIEN CANTA"), 370, 66, (255, 255, 255)), (tr("EN EL VIGILABEBÉS…"), 450, 66, (255, 255, 255)),
                                 (tr("NO CONTESTES"), 560, 120, (255, 40, 50))):
            fs = fs0
            while fs > 24 and d.textlength(txt, font=font(fs * pp + 1)) > 940: fs -= 2
            d.text((540, y), txt, font=font(fs * pp + 1), fill=col, anchor="mm", stroke_width=int(10 * pp), stroke_fill=(0, 0, 0))
        d.rounded_rectangle((230, 670, 850, 770), 26, fill=(230, 30, 50))
        d.text((540, 720), tr("SÍGUEME PARA MÁS"), font=font(52), fill=(255, 255, 255), anchor="mm")
        return img
    return img, dict(grain=10, tint=((255, 0, 30), 0.25 * pp if pp > 0 else 0), glitch=0.3 if pp > 0 and fi % 5 == 0 else 0.0, overlay=regla)

ESCENA_FN = dict(vigila=vigila, solos=solos, contestas=contestas, pasillo=pasillo, cuna=cuna, suena=suena, entiendes=entiendes,
                 tucama=tucama, final=final)
PAUSA = dict(vigila=0.5, solos=0.4, contestas=0.7, pasillo=0.5, cuna=0.7, suena=0.8, entiendes=0.7, tucama=1.0, final=2.4)
