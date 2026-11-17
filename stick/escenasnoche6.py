"""TURNO DE NOCHE 6 — "Si alguien pregunta por el kilómetro 10, di que no existe" (escenas 3D con turno3d)."""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter
from motor import *
from motor3d import *
from turno3d import *

G = __import__("guionnoche6" + ("_en" if IDIOMA == "en" else ""))
CAR = (-1.7, 8.4)                          # el coche familiar, aparcado junto al surtidor 1, mirando a la carretera
VENT = (CAR[0] + 0.85, CAR[1] + 0.1)       # ventanilla del conductor (x, z)
NOTAS = ["Le dije que sí.", "Respiré.", "Ya no me acuerdo de mi cara."]
ROJO_N = (190, 40, 60)                     # chubasquero de la niña (granate, que se vea en la niebla)

def hora(h, m, s=0):
    return f"{h:02d}:{m:02d}:{s:02d}"

def familia(esc, M, cuantos=4, t=0.0, mira_padre=0.0, sonrisa=False):
    """padre (conductor), madre (copiloto), niño y niña detrás. cuantos: los que quedan (se van del último al primero, la niña nunca)"""
    orden = ["conductor", "copiloto", "detras_der"][: max(0, cuantos - 1)]
    if "conductor" in orden:
        pasajero(esc, M, "conductor", ropa=(70, 74, 90), piel=(200, 186, 172), pelo=(40, 34, 30), mira=-4, gira=mira_padre,
                 cara="neutral", brazo=(70, 50))
    if "copiloto" in orden:
        pasajero(esc, M, "copiloto", ropa=(120, 90, 80), piel=(206, 190, 178), pelo=(80, 50, 36))
    if "detras_der" in orden:
        pasajero(esc, M, "detras_der", ropa=(70, 110, 80), piel=(210, 196, 186), alto=0.72, pelo=(60, 44, 30))
    pasajero(esc, M, "detras_izq", ropa=ROJO_N, piel=(222, 214, 210), alto=0.68, extra_cabeza=capucha(ROJO_N))

def _hacia_ti(M_ojo):
    return M_ojo

# ---------- 1. arranque: la niña sola atrás, la ventanilla bajada, el cuaderno hacia ti ----------
def _nina_plano(t, D, ofrece=1.0, cerca=1.0):
    esc = mundo(t)
    M = coche_familiar(esc, *CAR, faros=0.6)
    # la niña, girada hacia ti, con el brazo fuera de la ventanilla y el cuaderno en la mano
    cab = pasajero(esc, M, "detras_izq", ropa=ROJO_N, piel=(226, 218, 214), alto=0.68, extra_cabeza=capucha(ROJO_N),
                   gira=1.25, mira=-4, brazo=(lerp(30, 80, ofrece), lerp(60, 10, ofrece)))
    if ofrece > 0.3:
        cuaderno3d(esc, CAR[0] + 0.7 + 0.3 * ofrece, 1.06 + 0.1 * ofrece, CAR[1] - 0.97, yaw=0.3)
    z0 = CAR[1] - 1.0
    cam = Camara(ojo=(lerp(1.6, 0.55, cerca), 1.48, z0 + 0.25), mira=(CAR[0] + 0.55, 1.2, z0 + 0.02), fov=lerp(42, 34, cerca))
    luces = luces_base(extra=[Luz((0.5, 2.0, z0 + 0.4), (230, 240, 230), 4.0, fuerza=1.2)])
    img = esc.render(cam, luces)
    return etiquetas(img, esc, cam)

def arranque(t, D, fi):
    k = ease(seg(t, 0, D))
    img = _nina_plano(t, D, ofrece=1.0, cerca=0.6 + 0.4 * k)
    img = aclarar(img)
    rot = lambda im: rotulo_regla(im, 6, "SI PREGUNTAN POR EL KM 10, DI QUE NO EXISTE", p=1.0, y=460)   # nítido, encima del filtro
    return img, dict(grain=8, glitch=0.2 if fi % 17 < 2 else 0.0, overlay=rot)

# ---------- 2. premisa: la hoja de reglas; aún se ve el vaho de anoche ----------
def premisa(t, D, fi):
    esc = mundo(t)
    cam = cam_mostrador(t, mira=(0.6, 0.6, -1.5), fov=50)
    img = esc.render(cam, luces_base()).filter(ImageFilter.GaussianBlur(10))
    z = lerp(0.9, 0.97, ease(t / D))
    hoja_reglas(img, t, G.REGLAS, resalta=5, nota="Yo respiré. — R.", nota_p=1.0, zoom=z * 0.8, cy=790, h_extra=300)
    img = vaho(img, "TÚ TODAVÍA NO", W / 2, 1190, size=66, p=0.55 + 0.25 * seg(t, D * 0.4, D), ancho=700)
    return img, dict(grain=7)

# ---------- 3. coche: el padre baja la ventanilla y pregunta ----------
def coche(t, D, fi):
    esc = mundo(t)
    M = coche_familiar(esc, *CAR, faros=0.7)
    gira = ease(seg(t, D * 0.35, D * 0.6))
    familia(esc, M, 4, t, mira_padre=1.1 * gira)
    # el padre se gira hacia ti: lo rehacemos encima con giro
    k = ease(seg(t, 0, D))
    cam = Camara(ojo=(lerp(2.2, 0.9, k), 1.7, CAR[1] + lerp(1.6, 0.6, k)), mira=(CAR[0] + 0.2, 1.1, CAR[1] - 0.35), fov=lerp(50, 44, k))
    luces = luces_base(extra=[Luz((0.6, 2.2, CAR[1] + 0.4), (230, 240, 230), 4.0, fuerza=0.9)])
    img = etiquetas(esc.render(cam, luces), esc, cam)
    return img, dict(grain=7)

# ---------- 4. niego: sonríe y se va despacio hacia la niebla ----------
def niego(t, D, fi):
    corte = D * 0.38
    if t < corte:                          # el padre, de cerca, mirándote; no parpadea
        esc = mundo(t)
        M = coche_familiar(esc, *CAR, faros=0.7)
        familia(esc, M, 4, t, mira_padre=1.1)
        cam = Camara(ojo=(0.3, 1.6, CAR[1] + 0.25), mira=(VENT[0] - 0.45, 1.25, VENT[1] - 0.05), fov=30)
        luces = luces_base(extra=[Luz((0.4, 2.0, CAR[1] + 0.3), (230, 240, 230), 3.5, fuerza=1.1)])
        return esc.render(cam, luces), dict(grain=8)
    a = ease(seg(t, corte, D))
    esc = mundo(t)
    M = coche_familiar(esc, CAR[0] + 1.2 * a, CAR[1] + 9 * a, yaw=0.12 * a, faros=1.2, pilotos=1.0)
    familia(esc, M, 4, t)
    cam = Camara(ojo=(-1.4, 1.75, 4.2), mira=(CAR[0] + 0.6 * a, 1.0, CAR[1] + 6 * a), fov=50)
    luces = luces_base(extra=[Luz((CAR[0] + 1.2 * a, 1.0, CAR[1] + 9 * a - 2.4), (255, 40, 30), 3.0, fuerza=0.8)])
    img = etiquetas(esc.render(cam, luces), esc, cam)
    return img, dict(grain=8)

# ---------- 5. vuelve: CAM 2, cada media hora, uno menos ----------
def vuelve(t, D, fi):
    paso = min(2, int(t / (D / 3)))
    cuantos = 3 - paso if paso < 2 else 2
    cuantos = [3, 2, 2][paso]
    hh = [(1, 30), (2, 0), (2, 0)][paso]
    esc = mundo(t)
    M = coche_familiar(esc, *CAR, faros=0.8)
    familia(esc, M, cuantos, t)
    tl = t - paso * D / 3
    cam = Camara(ojo=(3.4, 1.85, 9.4), mira=(CAR[0], 1.25, CAR[1] - 0.4), fov=lerp(42, 36, ease(seg(tl, 0, D / 3))))
    img = esc.render(cam, luces_base())
    img = cctv(img, 2, hora(hh[0], hh[1], int(tl * 3) % 60))
    d = ImageDraw.Draw(img)
    # contador a la vista: cuántos hay dentro
    d.text((W / 2, 1180), f"{cuantos}", font=font(150), fill=(255, 255, 255), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    return img, dict(grain=10, glitch=0.35 if tl < 0.15 else 0.0)

# ---------- 6. niña: el asiento del conductor vacío; solo ella, atrás ----------
def nina(t, D, fi):
    corte = D * 0.4
    if t < corte:                          # plano general: el coche ha vuelto y no conduce nadie
        esc = mundo(t)
        M = coche_familiar(esc, *CAR, faros=0.9)
        familia(esc, M, 1, t)
        k = ease(seg(t, 0, corte))
        cam = Camara(ojo=(lerp(1.6, 0.9, k), 1.7, CAR[1] + lerp(1.2, 0.6, k)), mira=(CAR[0] + 0.2, 1.1, CAR[1] - 0.45), fov=46)
        luces = luces_base(extra=[Luz((0.6, 2.2, CAR[1] + 0.4), (230, 240, 230), 4.0, fuerza=0.9)])
        img = etiquetas(esc.render(cam, luces), esc, cam)
        return img, dict(grain=8)
    k = seg(t, corte, D)
    img = _nina_plano(t, D, ofrece=ease(seg(t, corte, corte + D * 0.35)), cerca=0.4 + 0.6 * ease(k))
    return img, dict(grain=8, tint=((255, 0, 30), 0.1 * k))

# ---------- 7. giro: el cuaderno de Raúl; en la última página, tu nombre ----------
def giro(t, D, fi):
    esc = mundo(t)
    cam = cam_mostrador(t, mira=(0.6, 0.6, -1.5), fov=50)
    img = esc.render(cam, luces_base()).filter(ImageFilter.GaussianBlur(12))
    corte = D * 0.35
    if t < corte:
        cuaderno(img, t, pagina=0, escala=lerp(0.9, 0.95, t / corte), cy=760)
    else:
        cuaderno(img, t, pagina=1, lineas=NOTAS, nombre_p=seg(t, corte + D * 0.05, D * 0.6), escala=lerp(0.95, 1.02, ease(seg(t, corte, D))), cy=760)
    fl = max(0.0, 0.6 - abs(t - corte) / 0.25) if t > 0.2 else 0.0
    return img, dict(grain=7, flash=((255, 255, 255), fl), tint=((255, 0, 30), 0.12 * seg(t, D * 0.7, D)))

# ---------- 8. final: el coche se va sin nadie al volante. Tarjeta REGLA 6 ----------
def final(t, D, fi):
    a = ease(seg(t, 0, D))
    esc = mundo(t)
    M = coche_familiar(esc, CAR[0] + 1.0 * a, CAR[1] + 7 * a, yaw=0.1 * a, faros=1.2, pilotos=1.0)
    familia(esc, M, 1, t)
    cam = Camara(ojo=(-1.4, 1.75, 4.2), mira=(CAR[0] + 0.5 * a, 1.0, CAR[1] + 5 * a), fov=50)
    img = esc.render(cam, luces_base())
    d = ImageDraw.Draw(img)
    p = ease_back(seg(t, 0.15, 0.5))
    d.rectangle((0, 300, W, 840), fill=(0, 0, 0))
    d.text((W / 2, 410), f"{tr('REGLA')} 6", font=font(int(150 * p) + 1), fill=(230, 40, 40), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
    regla = tr("EL KILÓMETRO 10 NO EXISTE")
    fs = 70
    while d.textlength(regla, font=font(fs)) > W - 120 and fs > 30: fs -= 2
    d.text((W / 2, 580), regla, font=font(fs), fill=(240, 240, 230), anchor="mm")
    q = ease_back(seg(t, D * 0.55, D * 0.75))
    if q > 0:
        d.rounded_rectangle((200, 700, 880, 800), 24, fill=(200, 30, 30))
        d.text((W / 2, 750), tr("MAÑANA: REGLA 7"), font=font(int(56 * q) + 1), fill=(255, 255, 255), anchor="mm")
    return img, dict(grain=9, glitch=0.25 if fi % 11 < 2 else 0.0)

ESCENA_FN = dict(arranque=arranque, premisa=premisa, coche=coche, niego=niego, vuelve=vuelve, nina=nina, giro=giro, final=final)
PAUSA = dict(arranque=0.4, premisa=0.5, coche=0.5, niego=0.5, vuelve=0.5, nina=0.6, giro=0.9, final=1.8)
