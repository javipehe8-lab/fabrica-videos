"""Renderiza el episodio. Uso: render.py voz_dir out_dir [--preview]"""
import json, os, sys, subprocess, multiprocessing as mp
from PIL import ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motor import *
import importlib
EP = os.environ.get("EP", "")
_g = importlib.import_module("guion" + EP + ("_en" if os.environ.get("IDIOMA") == "en" else "")); ESCENAS, TITULO, PARTE = _g.ESCENAS, _g.TITULO, _g.PARTE
# GANCHO opcional en el guion: ("escena", fraccion_de_la_escena, "TEXTO GRANDE") -> 1,2 s de impacto antes de la historia
GANCHO = getattr(_g, "GANCHO", None)
# ELECCION opcional: ("PREGUNTA", "OPCIÓN A", "OPCIÓN B") -> la escena "final" se sustituye por una tarjeta para votar en comentarios
ELECCION = getattr(_g, "ELECCION", None)

def tarjeta_eleccion(t, fi):
    F = Frame(gradient((22, 8, 30), (6, 4, 10)), dict(x=540, y=960, z=1.0))
    if noise(t * 5, 3) > -0.3:
        old = SONRIENTE.scale; SONRIENTE.scale = 3.4
        SONRIENTE.draw(F, STAND, 540, 2950, f=1); SONRIENTE.scale = old
    img = F.finish(); d = ImageDraw.Draw(img)
    q, oa, ob = ELECCION
    p = ease_back(seg(t, 0.0, 0.3))
    d.text((540, 300), tr("TÚ DECIDES"), font=font(70 * p + 1), fill=(255, 214, 0), anchor="mm", stroke_width=7, stroke_fill=(0, 0, 0))
    for i, ln in enumerate(q.split("\n")):
        d.text((540, 430 + i * 110), ln, font=font(100 * p + 1), fill=(255, 255, 255), anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
    for k, (letra, txt, col, y) in enumerate((("A", oa, (40, 120, 235), 760), ("B", ob, (225, 40, 60), 1010))):
        s = ease_back(seg(t, 0.35 + 0.2 * k, 0.6 + 0.2 * k))
        if s <= 0: continue
        pulse = 1 + 0.04 * math.sin(t * 8 + k * math.pi)
        hw, hh = 420 * s * pulse, 95 * s * pulse
        d.rounded_rectangle((540 - hw, y - hh, 540 + hw, y + hh), 40, fill=col, outline=(255, 255, 255), width=6)
        d.ellipse((540 - hw + 30, y - 62 * s, 540 - hw + 30 + 124 * s, y + 62 * s), fill=(255, 255, 255))
        d.text((540 - hw + 30 + 62 * s, y), letra, font=font(90 * s + 1), fill=col, anchor="mm")
        fs = 74
        while fs > 30 and d.textlength(txt, font=font(fs * s + 1)) > 2 * hw - 230 * s: fs -= 2
        d.text((540 + 75 * s, y), txt, font=font(fs * s + 1), fill=(255, 255, 255), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
    c = ease_back(seg(t, 1.0, 1.3)) * (1 + 0.05 * math.sin(t * 10))
    if c > 0:
        d.text((540, 1260), tr("COMENTA A O B") + " ↓", font=font(76 * c + 1), fill=(255, 214, 0), anchor="mm", stroke_width=8, stroke_fill=(0, 0, 0))
        d.rounded_rectangle((250, 1360, 830, 1480), 30, fill=(230, 30, 50))
        d.text((540, 1420), f"{tr('PARTE')} {PARTE + 1} · {tr('SÍGUEME →').replace(' →', '')}", font=font(56), fill=(255, 255, 255), anchor="mm")
    return post(img, fi, glitch=0.25 if fi % 9 == 0 else 0.0, grain=6)
G_DUR = 1.2
_e = importlib.import_module("escenas" + EP); ESCENA_FN, PAUSA = _e.ESCENA_FN, _e.PAUSA

VOZ_DELAY = 0.12

def timeline(voz):
    info = json.load(open(os.path.join(voz, "tiempos.json"), encoding="utf-8"))
    tl, t0 = [], 0.0
    if GANCHO:
        tl.append(dict(name="gancho", start=0.0, D=G_DUR, words=[])); t0 = G_DUR
    for (name, _), inf in zip(ESCENAS, info):
        D = inf["dur"] + VOZ_DELAY + PAUSA[name]
        words = []
        for fr in inf["frases"]:
            ws = fr["text"].split(); tot = sum(len(w) + 2 for w in ws); t = fr["start"]
            for w in ws:
                d = (fr["end"] - fr["start"]) * (len(w) + 2) / tot
                words.append((t + VOZ_DELAY, t + VOZ_DELAY + d, w, fr.get("quien", "NARRADOR"))); t += d
        tl.append(dict(name=name, start=t0, D=D, words=words, voz=len([s for s in tl if s["name"] != "gancho"])))
        t0 += D
    return tl, t0

def render_frame(tl, fi):
    T = fi / FPS
    sc = next((s for s in tl if s["start"] <= T < s["start"] + s["D"]), tl[-1])
    t = T - sc["start"]
    if sc["name"] == "gancho":
        g = next(s for s in tl if s["name"] == GANCHO[0])
        img, fx = ESCENA_FN[GANCHO[0]](g["D"] * GANCHO[1] + t * 0.15, g["D"], fi)
        img = post(img, fi, flash=((255, 255, 255), max(0.0, 1 - t / 0.25)), glitch=0.35 if fi % 3 == 0 else 0.1,
                   tint=((255, 0, 30), 0.25), dark=0.15)
        d = ImageDraw.Draw(img); s_ = ease_back(seg(t, 0.0, 0.18)) * (1 + 0.03 * math.sin(t * 30))
        lines = GANCHO[2].split("\n")
        for i, ln in enumerate(lines):
            d.text((540, 820 + (i - (len(lines) - 1) / 2) * 150), ln, font=font(112 * s_), fill=(255, 214, 0) if i == len(lines) - 1 else (255, 255, 255),
                   anchor="mm", stroke_width=int(13 * s_), stroke_fill=(0, 0, 0))
        return img
    if sc["name"] == "final" and ELECCION:
        return tarjeta_eleccion(t, fi)
    img, fx = ESCENA_FN[sc["name"]](t, sc["D"], fi)
    pz = 0.07 * (1 - ease_out(seg(t, 0, 0.18)))   # "punch" de zoom en cada corte
    if pz > 0.001:
        cw, ch = int(W / (1 + pz)), int(H / (1 + pz))
        img = img.crop(((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw, (H - ch) // 2 + ch)).resize((W, H))
    img = post(img, fi, flash=fx.get("flash"), glitch=fx.get("glitch", 0), dark=fx.get("dark", 0), grain=fx.get("grain", 7), tint=fx.get("tint"))
    # corte con "punch": pequeño destello en cada cambio de escena
    if sc["name"] != "final":
        img = captions(img, sc["words"], t)
        d = ImageDraw.Draw(img)
        d.text((60, 190), f"{TITULO} · {tr('PARTE')} {PARTE}", font=font(34), fill=(255, 255, 255), anchor="lm", stroke_width=4, stroke_fill=(0, 0, 0))
    return img

def worker(args):
    voz, out, k, a, b = args
    tl, _ = timeline(voz)
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", os.path.join(out, f"part{k}.mp4")],
                         stdin=subprocess.PIPE)
    for fi in range(a, b):
        p.stdin.write(render_frame(tl, fi).tobytes())
        if fi % 150 == 0: print(f"[{k}] {fi}/{b}", flush=True)
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    voz, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
    tl, total = timeline(voz)
    json.dump([{k: v for k, v in s.items() if k != "words"} for s in tl], open(os.path.join(out, "timeline.json"), "w"), indent=1)
    if "--preview" in sys.argv:
        from PIL import Image
        fr = float(os.environ.get("AT", "0.55"))
        ims = [render_frame(tl, int((s["start"] + s["D"] * fr) * FPS)).resize((270, 480)) for s in tl]
        rows = -(-len(ims) // 6)
        sheet = Image.new("RGB", (270 * 6, 480 * rows))
        for i, im in enumerate(ims): sheet.paste(im, ((i % 6) * 270, (i // 6) * 480))
        sheet.save(os.path.join(out, "preview.png")); print("total", round(total, 2)); sys.exit()
    N = int(total * FPS); n = int(os.environ.get("JOBS", "2")); step = -(-N // n)
    with mp.Pool(n) as pool:
        pool.map(worker, [(voz, out, k, k * step, min(N, (k + 1) * step)) for k in range(n)])
    with open(os.path.join(out, "parts.txt"), "w") as f:
        for k in range(n): f.write(f"file 'part{k}.mp4'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(out, "parts.txt"), "-c", "copy",
                    os.path.join(out, "video_mudo.mp4")], check=True)
    print("OK", N, "frames", round(total, 2), "s")
