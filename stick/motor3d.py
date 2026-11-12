"""Motor 3D de pocos polígonos (look PlayStation 2) sin dependencias: numpy + PIL.
Malla = (vértices Nx3, caras [(i,j,k)], color). Se dibuja con el algoritmo del pintor, sombreado plano,
linterna (luz puntual con cono), niebla por distancia y vértices "temblorosos" pegados a una rejilla de baja resolución.
Los personajes reutilizan las poses 2D de motor.py (ángulos de brazos/piernas) en su plano sagital.

Uso básico:
    cam = Camara(ojo=(0, 1.6, 4), mira=(0, 1, 0), fov=60)
    esc = Escena(niebla=((60, 66, 64), 3, 12), amb=0.25)
    esc.add(caja(4, 0.1, 4, (90, 80, 70)), mover(0, -0.05, 0))
    humano(esc, STAND, x=0, z=0, yaw=0, ropa=(60,160,130), piel=(220,215,205))
    img = esc.render(cam, luces=[Luz((0,2,2), (255,240,210), 6)])   # PIL 1080x1920
"""
import math
import numpy as np
from PIL import Image, ImageDraw
from motor import W, H, STAND, L

RW, RH = 360, 640          # resolución interna (se amplía x3 sin suavizar)

# ---------- matrices ----------
def mover(x, y, z):
    M = np.eye(4); M[:3, 3] = (x, y, z); return M
def escala(sx, sy=None, sz=None):
    sy = sx if sy is None else sy; sz = sx if sz is None else sz
    return np.diag([sx, sy, sz, 1.0])
def rot_x(a):
    c, s = math.cos(a), math.sin(a); M = np.eye(4); M[1, 1], M[1, 2], M[2, 1], M[2, 2] = c, -s, s, c; return M
def rot_y(a):
    c, s = math.cos(a), math.sin(a); M = np.eye(4); M[0, 0], M[0, 2], M[2, 0], M[2, 2] = c, s, -s, c; return M
def rot_z(a):
    c, s = math.cos(a), math.sin(a); M = np.eye(4); M[0, 0], M[0, 1], M[1, 0], M[1, 1] = c, -s, s, c; return M
def cadena(*Ms):
    R = np.eye(4)
    for M in Ms: R = R @ M
    return R

# ---------- primitivas (caras en sentido antihorario visto desde fuera) ----------
def caja(w, h, d, col, base=False):
    """caja centrada (o apoyada en y=0 si base=True). Las cajas grandes se trocean (mejor orden de dibujo)."""
    if max(w, h, d) > 1.3:
        return _caja_troceada(w, h, d, col, base)
    x, y, z = w / 2, h / 2, d / 2
    oy = y if base else 0
    V = np.array([[-x, -y, -z], [x, -y, -z], [x, y, -z], [-x, y, -z], [-x, -y, z], [x, -y, z], [x, y, z], [-x, y, z]], float)
    V[:, 1] += oy
    F = [(4, 5, 6), (4, 6, 7), (1, 0, 3), (1, 3, 2), (0, 4, 7), (0, 7, 3), (5, 1, 2), (5, 2, 6), (3, 7, 6), (3, 6, 2), (0, 1, 5), (0, 5, 4)]
    return V, F, col

def _caja_troceada(w, h, d, col, base=False, paso=0.9):
    V, F = [], []
    def cara(o, ua, va, nu, nv):
        i0 = len(V)
        for i in range(nu + 1):
            for j in range(nv + 1):
                V.append(np.array(o) + np.array(ua) * i / nu + np.array(va) * j / nv)
        for i in range(nu):
            for j in range(nv):
                p = i0 + i * (nv + 1) + j; q = i0 + (i + 1) * (nv + 1) + j
                F.extend([(p, q, q + 1), (p, q + 1, p + 1)])
    n = lambda s: max(1, math.ceil(s / paso))
    x, y, z = w / 2, h / 2, d / 2
    oy = y if base else 0
    cara((-x, -y + oy, z), (w, 0, 0), (0, h, 0), n(w), n(h))        # +z
    cara((x, -y + oy, -z), (-w, 0, 0), (0, h, 0), n(w), n(h))       # -z
    cara((x, -y + oy, z), (0, 0, -d), (0, h, 0), n(d), n(h))        # +x
    cara((-x, -y + oy, -z), (0, 0, d), (0, h, 0), n(d), n(h))       # -x
    cara((-x, y + oy, z), (w, 0, 0), (0, 0, -d), n(w), n(d))        # +y
    cara((-x, -y + oy, -z), (w, 0, 0), (0, 0, d), n(w), n(d))       # -y
    return np.array(V, float), F, col

def prisma(r0, r1, h, col, n=6):
    """tronco de cono de n caras desde y=0 hasta y=-h (cuelga hacia abajo: para brazos y piernas)"""
    V = []
    for k in range(n):
        a = 2 * math.pi * k / n
        V.append([r0 * math.cos(a), 0, r0 * math.sin(a)])
    for k in range(n):
        a = 2 * math.pi * k / n
        V.append([r1 * math.cos(a), -h, r1 * math.sin(a)])
    F = []
    for k in range(n):
        a, b = k, (k + 1) % n
        F += [(a, n + b, n + a), (a, b, n + b)]
    for k in range(1, n - 1):
        F += [(0, k + 1, k), (n, n + k, n + k + 1)]
    return np.array(V, float), F, col

def esfera(r, col, sub=1):
    """esfera de pocas caras (octaedro subdividido)"""
    V = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
    F = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]
    for _ in range(sub):
        cache = {}; NF = []
        def mid(a, b):
            k = (min(a, b), max(a, b))
            if k not in cache:
                p = np.add(V[a], V[b]) / 2; p = p / np.linalg.norm(p); V.append(list(p)); cache[k] = len(V) - 1
            return cache[k]
        for a, b, c in F:
            ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
            NF += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
        F = NF
    return np.array(V, float) * r, F, col

def plano(w, d, col):
    """suelo/techo horizontal centrado en y=0 mirando hacia arriba"""
    x, z = w / 2, d / 2
    V = np.array([[-x, 0, -z], [x, 0, -z], [x, 0, z], [-x, 0, z]], float)
    return V, [(0, 2, 1), (0, 3, 2)], col

def pared(w, h, col):
    """pared vertical en el plano z=0, de x=-w/2..w/2, y=0..h, mirando hacia +z"""
    x = w / 2
    V = np.array([[-x, 0, 0], [x, 0, 0], [x, h, 0], [-x, h, 0]], float)
    return V, [(0, 1, 2), (0, 2, 3)], col

def subdividir(m, n=4):
    """parte una pared/plano en n x n trozos para que la luz y la niebla se repartan mejor"""
    V, F, col = m
    if len(V) != 4: return m
    a, b, c, d = V
    NV, NF = [], []
    for i in range(n + 1):
        for j in range(n + 1):
            u, v = i / n, j / n
            NV.append(a * (1 - u) * (1 - v) + b * u * (1 - v) + c * u * v + d * (1 - u) * v)
    for i in range(n):
        for j in range(n):
            p = i * (n + 1) + j; q = (i + 1) * (n + 1) + j
            NF += [(p, q, q + 1), (p, q + 1, p + 1)]
    flip = F[0] == (0, 2, 1)
    if flip: NF = [(x, z, y) for x, y, z in NF]
    return np.array(NV), NF, col

# ---------- cámara, luces, escena ----------
class Camara:
    def __init__(self, ojo, mira, fov=60, roll=0.0):
        self.ojo, self.mira, self.fov, self.roll = np.array(ojo, float), np.array(mira, float), fov, roll
    def vista(self):
        f = self.mira - self.ojo; f /= np.linalg.norm(f)
        up = np.array([math.sin(self.roll), math.cos(self.roll), 0.0])
        r = np.cross(f, up); r /= np.linalg.norm(r); u = np.cross(r, f)
        M = np.eye(4); M[0, :3], M[1, :3], M[2, :3] = r, u, -f
        M[:3, 3] = -M[:3, :3] @ self.ojo
        return M

class Luz:
    """luz puntual; con dir y cono (grados) es una linterna"""
    def __init__(self, pos, col=(255, 240, 210), alcance=6.0, dir=None, cono=None, fuerza=1.0):
        self.pos, self.col, self.alc, self.fuerza = np.array(pos, float), np.array(col, float) / 255, alcance, fuerza
        self.dir = None if dir is None else np.array(dir, float) / np.linalg.norm(dir)
        self.cono = cono

NEAR = 0.12
def _recorta(poly):
    """Sutherland-Hodgman contra el plano z = -NEAR (espacio de cámara)"""
    out = []
    for i in range(len(poly)):
        P, Q = poly[i], poly[(i + 1) % len(poly)]
        pin, qin = P[2] <= -NEAR, Q[2] <= -NEAR
        if pin: out.append(P)
        if pin != qin:
            k = (-NEAR - P[2]) / (Q[2] - P[2]); out.append(P + (Q - P) * k)
    return out

class Escena:
    def __init__(self, niebla=((58, 62, 60), 2.5, 11.0), amb=0.22, cielo=None):
        self.objs = []; self.niebla = niebla; self.amb = amb; self.cielo = cielo
    def add(self, malla, M=None, emite=False, fondo=False, sesgo=0.0):
        """fondo=True: superficie grande de "caja" (suelo, techo, paredes de la habitación): se dibuja siempre antes que los objetos"""
        # sesgo > 0: se dibuja como si estuviera más cerca (para piezas encima de otras, p. ej. la encimera)
        self.objs.append((malla, np.eye(4) if M is None else M, emite, fondo, sesgo)); return self

    def render(self, cam, luces=(), temblor=True):
        img = Image.new("RGB", (RW, RH), self.niebla[0] if self.cielo is None else self.cielo)
        d = ImageDraw.Draw(img)
        Vm = cam.vista(); f = 1 / math.tan(math.radians(cam.fov) / 2); asp = RW / RH
        tris = []
        fog_c = np.array(self.niebla[0], float); f0, f1 = self.niebla[1], self.niebla[2]
        for (V, F, col), M, emite, fondo, sesgo in self.objs:
            Vw = (M @ np.c_[V, np.ones(len(V))].T).T[:, :3]
            Vc = (Vm @ np.c_[Vw, np.ones(len(Vw))].T).T[:, :3]
            Fa = np.array(F)
            A, B, C = Vw[Fa[:, 0]], Vw[Fa[:, 1]], Vw[Fa[:, 2]]
            N = np.cross(B - A, C - A); nl = np.linalg.norm(N, axis=1, keepdims=True); N = N / np.maximum(nl, 1e-9)
            cen = (A + B + C) / 3
            ext = Vw.max(0) - Vw.min(0)
            if ext.max() < 1.2: cen_luz = np.repeat(Vw.mean(0)[None], len(F), 0)    # objeto pequeño: luz uniforme (sin cortes en diagonal)
            else: cen_luz = cen
            zc = Vc[:, 2]
            for i, (a, b, c) in enumerate(F):
                za, zb, zcc = zc[a], zc[b], zc[c]
                if za > -NEAR and zb > -NEAR and zcc > -NEAR: continue              # todo detrás de la cámara
                vcam = cam.ojo - cen[i]
                if np.dot(N[i], vcam) <= 0: continue                                 # cara trasera
                col_ = np.array(col, float)
                if emite:
                    sh = col_
                else:
                    li = np.full(3, self.amb)
                    for lz in luces:
                        dv = lz.pos - cen_luz[i]; dist = np.linalg.norm(dv); dv /= max(dist, 1e-6)
                        k = max(0.0, float(np.dot(N[i], dv))) * max(0.0, 1 - dist / lz.alc) ** 1.3
                        if lz.dir is not None:
                            ca = float(np.dot(-dv, lz.dir)); lim = math.cos(math.radians(lz.cono))
                            k *= max(0.0, (ca - lim) / (1 - lim)) ** 0.6
                        li += lz.col * k * 1.6 * lz.fuerza
                    sh = col_ * li
                poly = [Vc[a], Vc[b], Vc[c]]
                if za > -NEAR or zb > -NEAR or zcc > -NEAR: poly = _recorta(poly)      # recorte contra el plano cercano
                if len(poly) < 3: continue
                depth = -sum(p[2] for p in poly) / len(poly)
                fz = min(1.0, max(0.0, (depth - f0) / (f1 - f0)))
                sh2 = sh * (1 - fz) + fog_c * fz
                pts = []
                for x, y, z in poly:
                    px = (x * f / asp / -z * 0.5 + 0.5) * RW; py = (-y * f / -z * 0.5 + 0.5) * RH
                    if temblor: px, py = round(px), round(py)                         # vértices pegados a la rejilla
                    pts.append((px, py))
                tris.append((depth + (1e6 if fondo else 0) - sesgo, pts, tuple(int(min(255, max(0, v))) for v in sh2)))
        tris.sort(key=lambda t: -t[0])
        for _, pts, c in tris: d.polygon(pts, fill=c)
        return img.resize((W, H), Image.NEAREST)

# ---------- personaje de pocos polígonos ----------
def humano(esc, p, x=0.0, z=0.0, yaw=0.0, ropa=(60, 160, 130), piel=(214, 208, 200), pantalon=(50, 54, 70), alto=1.0,
           cara="neutral", pelo=None, y=0.0, extra_cabeza=None):
    """humano low-poly de ~1,75 m con la pose 2D p (grados); yaw en radianes (0 = mira hacia +z, hacia la cámara)."""
    s = alto * 1.75 / 3.06                      # escala: el stickman 2D mide ~306 unidades de pies a cabeza
    u = lambda v: v / 100 * s
    base = cadena(mover(x, y, z), rot_y(yaw))
    pierna = u(L["ul"] + L["ll"])
    cadera = cadena(base, mover(0, pierna + u(6), 0))
    rb = math.radians(p.get("body", 0))
    torso = cadena(cadera, rot_x(rb))
    esc.add(caja(u(34), u(L["torso"]), u(20), ropa, base=True), torso)
    cuello = cadena(torso, mover(0, u(L["torso"]), 0))
    cab = cadena(cuello, rot_x(math.radians(p.get("head", 0))), mover(0, u(L["neck"] + L["head"] * 0.72), 0))
    HR = L["head"] * 0.75                       # cabeza algo más pequeña que en 2D: proporciones más realistas
    esc.add(esfera(u(HR), piel, 1), cadena(cab, escala(0.9, 1.1, 0.95)))
    if pelo: esc.add(esfera(u(HR) * 1.02, pelo, 1), cadena(cab, mover(0, u(8), -u(12)), escala(1.04, 0.95, 0.9)))
    if cara != "ninguna":                      # ojos (y boca) como cajitas oscuras en la cara (+z)
        ojo = (16, 16, 20)
        ry = u(10) if cara == "scared" else u(6)
        for dx in (-1, 1): esc.add(caja(u(9), ry, u(3), ojo), cadena(cab, mover(dx * u(12), u(4), u(HR) * 0.92)))
        if cara == "scared": esc.add(caja(u(10), u(12), u(3), ojo), cadena(cab, mover(0, -u(16), u(HR) * 0.85)))
    if extra_cabeza: extra_cabeza(esc, cab, u)
    hombro = cadena(torso, mover(0, u(L["torso"] * 0.9), 0))
    for lado, k in ((-1, "a1"), (1, "a2")):
        sup = cadena(hombro, mover(lado * u(22), 0, 0), rot_x(math.radians(p[k + "u"]) * -1), rot_z(lado * 0.1))
        esc.add(prisma(u(7), u(6), u(L["ua"]), ropa), sup)
        inf = cadena(sup, mover(0, -u(L["ua"]), 0), rot_x(-math.radians(p[k + "l"])))
        esc.add(prisma(u(6), u(5), u(L["la"]), piel), inf)
        esc.add(caja(u(10), u(12), u(8), piel), cadena(inf, mover(0, -u(L["la"] + 5), 0)))
    for lado, k in ((-1, "l1"), (1, "l2")):
        sup = cadena(cadera, mover(lado * u(10), 0, 0), rot_x(-math.radians(p[k + "u"])))
        esc.add(prisma(u(9), u(8), u(L["ul"]), pantalon), sup)
        inf = cadena(sup, mover(0, -u(L["ul"]), 0), rot_x(-math.radians(p[k + "l"])))
        esc.add(prisma(u(8), u(6), u(L["ll"]), pantalon), inf)
        esc.add(caja(u(12), u(7), u(24), (30, 30, 34)), cadena(inf, mover(0, -u(L["ll"]) - u(2), u(6))))
    return cab
