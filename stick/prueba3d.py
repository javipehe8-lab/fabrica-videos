import sys, math, time, subprocess
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import *
from motor3d import *
OUT = "out3d_prueba/"; import os; os.makedirs(OUT, exist_ok=True)
COC = (255, 210, 140)
def pasillo(esc):
    esc.add(subdividir(plano(3, 12, (70, 62, 54)), 6), mover(0, 0, -3))           # suelo de madera
    esc.add(subdividir(plano(3, 12, (40, 40, 44)), 4), cadena(mover(0, 2.6, -3), rot_x(math.pi)))  # techo
    esc.add(subdividir(pared(12, 2.6, (96, 92, 80)), 6), cadena(mover(-1.5, 0, -3), rot_y(math.pi / 2)))
    esc.add(subdividir(pared(12, 2.6, (96, 92, 80)), 6), cadena(mover(1.5, 0, -3), rot_y(-math.pi / 2)))
    # pared del fondo con puerta iluminada (la cocina)
    esc.add(pared(1.0, 2.6, (90, 86, 76)), mover(-1.0, 0, -9)); esc.add(pared(1.0, 2.6, (90, 86, 76)), mover(1.0, 0, -9))
    esc.add(pared(1.0, 0.6, (90, 86, 76)), mover(0, 2.0, -9))
    esc.add(pared(1.0, 2.0, COC), mover(0, 0, -9.05), emite=True)
    for zz in (-1, -5): esc.add(caja(0.6, 0.9, 0.35, (60, 46, 36), base=True), mover(1.2, 0, zz))  # muebles
    esc.add(caja(0.08, 0.5, 0.35, (200, 200, 190)), mover(-1.45, 1.6, -4))   # cuadro
def frame(t, fi):
    esc = Escena(niebla=((30, 34, 32), 2.0, 10.0), amb=0.12)
    pasillo(esc)
    # la cosa: de espaldas a contraluz, demasiado alta, con bata
    giro = min(1, max(0, (t - 2.0) / 0.25))
    p = pose(a1u=4, a2u=-4, a1l=2, a2l=2)
    humano(esc, p, x=0, z=-8.4, yaw=math.pi * (1 - giro), ropa=(200, 110, 145), piel=(190, 186, 182), pantalon=(200, 110, 145), alto=1.2,
           cara="scared" if giro > 0.5 else "ninguna", pelo=(80, 52, 34))
    k = ease(min(t, 2.0) / 2.0); k2 = ease(max(0, t - 2.1) / 0.9)
    cam = Camara(ojo=(0.15 + 0.03 * math.sin(t * 2), 1.6 + 0.02 * math.sin(t * 3.1), lerp(lerp(-1.0, -5.0, k), -7.2, k2)),
                 mira=(0, lerp(1.2, 1.75, k2), -9), fov=lerp(lerp(62, 50, k), 40, k2))
    luces = [Luz((0, 1.6, -9.3), COC, 7, fuerza=1.3),
             Luz(cam.ojo + (0.2, -0.3, 0), (255, 245, 220), 7, dir=cam.mira - cam.ojo, cono=16, fuerza=1.3)]
    img = esc.render(cam, luces)
    img = post(img, fi, grain=8, glitch=0.4 if 2.0 < t < 2.4 and fi % 2 else 0, tint=((255, 0, 30), 0.25) if t > 2.0 else None)
    return ps2(img, fi, res=3)
t0 = time.time()
p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                      "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", OUT + "prueba3d.mp4"], stdin=subprocess.PIPE)
for fi in range(90):
    im = frame(fi / 30, fi); p.stdin.write(im.tobytes())
    if fi in (20, 50, 75): im.resize((360, 640)).save(OUT + f"f{fi}.png")
p.stdin.close(); p.wait(); print("s/frame", (time.time() - t0) / 90)
