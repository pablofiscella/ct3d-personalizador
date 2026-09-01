"""Video-invitación para WhatsApp — MP4 vertical (1080x1920, ~14s) animado por
código: Pillow renderiza los cuadros y ffmpeg los compila a H.264. Sin IA por
venta (costo cero, determinístico); el arte sale del tema (hero de la invitación
web + personajes + paleta). Es el tier de ENTRADA del embudo de invitaciones:
video → invitación web interactiva → Fiesta Completa.

Escenas (24 fps):
  1) 0.0-3.5s  apertura: hero del tema con zoom suave + "¡Estás invitado!"
  2) 3.5-8.0s  el nombre GRANDE con globos subiendo + "cumple N añitos"
  3) 8.0-12.0s tarjeta con fecha/hora/lugar (entra deslizando)
  4) 12.0-14.0s cierre "¡Te esperamos!" + marca

API: generar_video(data, tema, out_path) -> out_path
"""
import glob
import math
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
FPS = 24
DUR = {"apertura": 3.5, "nombre": 4.5, "datos": 4.0, "cierre": 2.0}


# La tipografia se resuelve UNA vez por proceso, no en cada llamada (31-ago-2026).
#
# `glob.glob(f"{KIT}/**/Fredoka*.ttf", recursive=True)` camina el arbol entero del
# proyecto — ~42.000 entradas — y estaba adentro de _font, o sea una vez por CADA
# pedido de letra. Medido con el motor caido: una hoja de calendario llama a _font 39
# veces y el glob se comia 6,9 de sus 7,3 segundos (95%). Como el arranque encola ~576
# hojas de warm, el motor quedaba al 143% de CPU sin completar NINGUN render (cero
# archivos escritos en 20 minutos) y /health no contestaba.
#
# El .ttf no se mueve mientras el proceso vive. Los dos candidatos que hay
# (fonts/ y web/fonts/) son el MISMO archivo (mismo md5), asi que ordenarlos no
# cambia cual gana; se ordena para que sea determinista. Si dos hilos entran a la vez
# el peor caso es que ambos globeen una vez: el resultado es el mismo, no hace falta lock.
_FREDOKA = None


def _fuentes_fredoka():
    global _FREDOKA
    if _FREDOKA is None:
        _FREDOKA = sorted(glob.glob(f"{KIT}/**/Fredoka*.ttf", recursive=True))
    return _FREDOKA


def _font(sz, bold=True):
    for p in _fuentes_fredoka():
        try:
            f = ImageFont.truetype(p, sz)
            try:
                f.set_variation_by_axes([700 if bold else 500])
            except Exception:
                pass
            return f
        except Exception:
            pass
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", sz)


def _ease(t):
    """easeInOut 0..1 — movimiento natural en vez de lineal."""
    return t * t * (3 - 2 * t)


def _assets(tema):
    """Fondo (hero de la invitación web, ya con estilo IA si el tema lo tiene),
    personajes y color del tema — todo reusado de los motores existentes."""
    import invitacion_web as iw
    hero = iw._render_hero(tema)             # 1080x720
    acc = iw._hex_rgb(iw._accent(tema))
    try:
        import cuaderno
        personajes = cuaderno.personajes_decorativos(tema, 2)
    except Exception:
        personajes = []
    return hero, acc, personajes


def _tint(rgb, p):
    return tuple(int(v + (255 - v) * p) for v in rgb[:3])


def _fondo(acc):
    im = Image.new("RGB", (W, H), _tint(acc, 0.92))
    dr = ImageDraw.Draw(im)
    top, bottom = _tint(acc, 0.82), _tint(acc, 0.95)
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        dr.line([(0, y), (W, y)], fill=c)
    return im


def _globo(dr, x, y, r, col):
    dr.ellipse([x - r, y - int(r * 1.15), x + r, y + int(r * 1.15)], fill=col)
    dr.line([x, y + int(r * 1.15), x, y + int(r * 1.15) + int(r * 1.4)],
            fill=col, width=3)


def _texto_centrado(dr, texto, cy, fs, fill, maxw=W - 160, bold=True):
    f = _font(fs, bold)
    while f.getlength(texto) > maxw and fs > 30:
        fs -= 4
        f = _font(fs, bold)
    dr.text((W / 2, cy), texto, font=f, fill=fill, anchor="mm")


def _frame(t_total, data, hero, acc, personajes):
    """Un cuadro del video en el instante t_total (segundos)."""
    nombre = (str(data.get("nombre") or "").strip()) or "Tu peque"
    edad = str(data.get("edad") or "").strip()
    im = _fondo(acc)
    dr = ImageDraw.Draw(im)

    t = t_total
    if t < DUR["apertura"]:
        # ── apertura: hero con zoom-out suave + título fade-in ──
        p = _ease(min(t / DUR["apertura"], 1))
        z = 1.18 - 0.18 * p
        hw, hh = int(W * z), int(int(W * z) * hero.height / hero.width)
        h2 = hero.resize((hw, hh), Image.LANCZOS)
        im.paste(h2, (int((W - hw) / 2), int(H * 0.16 - (hh - H * 0.38) / 2)))
        alpha = int(255 * min(t / 1.2, 1))
        cap = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(cap)
        cd.text((W / 2, H * 0.66), "¡Estás invitado", font=_font(96),
                fill=(255, 255, 255, alpha), anchor="mm",
                stroke_width=6, stroke_fill=acc + (alpha,))
        cd.text((W / 2, H * 0.66 + 110), "a festejar!", font=_font(96),
                fill=(255, 255, 255, alpha), anchor="mm",
                stroke_width=6, stroke_fill=acc + (alpha,))
        im.paste(cap, (0, 0), cap)

    elif t < DUR["apertura"] + DUR["nombre"]:
        # ── nombre grande + globos subiendo + personajes ──
        tl = t - DUR["apertura"]
        p = _ease(min(tl / 0.8, 1))
        import random
        rnd = random.Random(7)
        for i in range(8):
            gx = rnd.randint(70, W - 70)
            base_y = H + 100 + rnd.randint(0, 500)
            gy = base_y - (tl * (H + 900) / DUR["nombre"]) * rnd.uniform(0.75, 1.1)
            _globo(dr, gx, int(gy), rnd.randint(38, 64),
                   _tint(acc, rnd.choice([0.05, 0.3, 0.5])))
        _texto_centrado(dr, "🎂" if False else "", H * 0.18, 90, acc)
        esc = 0.6 + 0.4 * p
        _texto_centrado(dr, nombre, H * 0.34, int(170 * esc), acc)
        if edad:
            _texto_centrado(dr, "¡cumple %s añitos!" % edad, H * 0.45, int(76 * esc),
                            (60, 50, 45))
        for i, pj in enumerate(personajes[:2]):
            ph = 480
            pw = max(1, int(pj.width * ph / pj.height))
            p2 = pj.resize((pw, ph), Image.LANCZOS)
            lado = -1 if i == 0 else 1
            px = int(W / 2 + lado * (W * 0.26) - pw / 2)
            py = int(H * 0.60 + (1 - p) * 260)
            im.paste(p2, (px, py), p2)

    elif t < DUR["apertura"] + DUR["nombre"] + DUR["datos"]:
        # ── tarjeta con los datos (entra deslizando desde abajo) ──
        tl = t - DUR["apertura"] - DUR["nombre"]
        p = _ease(min(tl / 0.7, 1))
        _texto_centrado(dr, "Anotá:", H * 0.16, 84, acc)
        card_y = int(H * 0.26 + (1 - p) * H * 0.5)
        dr.rounded_rectangle([90, card_y, W - 90, card_y + 880], 48, fill="white")
        y = card_y + 130
        for etiqueta, valor in (("Fecha", data.get("fecha")), ("Hora", data.get("hora")),
                                 ("Lugar", data.get("lugar")),
                                 ("Dirección", data.get("direccion"))):
            v = str(valor or "").strip()
            if not v:
                continue
            dr.text((W / 2, y), etiqueta.upper(), font=_font(34),
                    fill=_tint(acc, 0.25), anchor="mm")
            f = _font(58, False)
            while f.getlength(v) > W - 300:
                v = v[:-2]
            dr.text((W / 2, y + 70), v, font=f, fill=(60, 50, 45), anchor="mm")
            y += 200

    else:
        # ── cierre ──
        tl = t - DUR["apertura"] - DUR["nombre"] - DUR["datos"]
        pulso = 1 + 0.04 * math.sin(tl * 6)
        _texto_centrado(dr, "¡Te esperamos!", H * 0.42, int(120 * pulso), acc)
        for i, pj in enumerate(personajes[:2]):
            ph = 420
            pw = max(1, int(pj.width * ph / pj.height))
            p2 = pj.resize((pw, ph), Image.LANCZOS)
            lado = -1 if i == 0 else 1
            im.paste(p2, (int(W / 2 + lado * W * 0.24 - pw / 2), int(H * 0.55)), p2)
        dr.text((W / 2, H - 140), "casatridimensional.com.ar",
                font=_font(30, False), fill=_tint(acc, 0.35), anchor="mm")

    return im


def generar_video(data, tema="safari", out_path=None):
    """Renderiza los cuadros y compila el MP4 (H.264, compatible WhatsApp).
    ~340 cuadros a 24fps ≈ 14s de video; tarda ~30-60s de CPU."""
    hero, acc, personajes = _assets(tema)
    total = sum(DUR.values())
    n_frames = int(total * FPS)
    tmpdir = tempfile.mkdtemp(prefix="vidinv_")
    try:
        for i in range(n_frames):
            fr = _frame(i / FPS, data, hero, acc, personajes)
            fr.save(os.path.join(tmpdir, "f%05d.jpg" % i), quality=90)
        out_path = out_path or os.path.join(tmpdir, "invitacion.mp4")
        r = subprocess.run(
            ["ffmpeg", "-y", "-framerate", str(FPS),
             "-i", os.path.join(tmpdir, "f%05d.jpg"),
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
             "-preset", "fast", "-crf", "23", out_path],
            capture_output=True, text=True, timeout=300)
        if r.returncode != 0 or not os.path.isfile(out_path):
            raise RuntimeError("ffmpeg falló: %s" % r.stderr[-400:])
        return out_path
    finally:
        for f in glob.glob(os.path.join(tmpdir, "f*.jpg")):
            try:
                os.remove(f)
            except OSError:
                pass


def preview_frame(data, tema="safari"):
    """Cuadro representativo (el del nombre) para la galería de la ficha."""
    hero, acc, personajes = _assets(tema)
    return _frame(DUR["apertura"] + DUR["nombre"] * 0.75, data, hero, acc, personajes)


if __name__ == "__main__":
    import sys
    demo = {"nombre": "Valentina", "edad": "5", "fecha": "Sábado 12 de julio",
            "hora": "16:00 hs", "lugar": "Salón Arcoiris",
            "direccion": "Av. Siempreviva 742"}
    out = generar_video(demo, sys.argv[1] if len(sys.argv) > 1 else "safari",
                        "/tmp/video_invitacion_demo.mp4")
    print("OK ->", out)
