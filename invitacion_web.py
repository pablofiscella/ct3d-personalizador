"""Invitación WEB interactiva — el producto no es un archivo: es una PÁGINA viva
por evento (link para compartir por WhatsApp) con cuenta regresiva, botón "cómo
llegar" (Google Maps) y confirmación de asistencia por WhatsApp al organizador.

Se genera sola en la compra (tipo 'invitacion-web' en /api/generar): se persiste
un JSON por evento en INVITACIONES_DIR y la página se renderiza on-the-fly con el
arte del tema. Vigencia ~180 días (las carpetas de pedidos duran 30; la invitación
tiene que vivir hasta después de la fiesta, por eso va en su propio directorio).

API: crear(data, tema) -> token · cargar(token) -> dict · html(token) -> str
     hero_png(token) -> bytes · preview_mock(data, tema) -> PIL.Image
"""
import html as html_mod
import io
import json
import os
import re
import secrets
import time

from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
INVITACIONES_DIR = os.environ.get(
    "CT3D_INVITACIONES_DIR", os.path.join(KIT, "invitaciones"))
VIGENCIA_DIAS = 7300   # "para siempre" en la práctica (~20 años) — respalda Mis compras

Wh, Hh = 1080, 720   # hero (apaisado para el encabezado de la página)


# ── datos ────────────────────────────────────────────────────────────────────

def _campo(data, k):
    return str(data.get(k) or "").strip()


def crear(data, tema="safari"):
    """Persiste el evento y devuelve el token público del link. Limpia vencidas."""
    token = secrets.token_urlsafe(12)
    reg = {
        "tema": tema,
        "nombre": _campo(data, "nombre") or "Cumple",
        "edad": _campo(data, "edad"),
        "fecha": _campo(data, "fecha"),
        "hora": _campo(data, "hora"),
        "lugar": _campo(data, "lugar"),
        "direccion": _campo(data, "direccion"),
        "telefono": _campo(data, "telefono"),
        "creada": int(time.time()),
    }
    os.makedirs(INVITACIONES_DIR, exist_ok=True)
    with open(os.path.join(INVITACIONES_DIR, token + ".json"), "w",
              encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
    _limpiar_vencidas()
    return token


def cargar(token):
    """dict del evento, o None si no existe / token inválido."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,32}", token or ""):
        return None
    p = os.path.join(INVITACIONES_DIR, token + ".json")
    if not os.path.isfile(p):
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _limpiar_vencidas():
    """Borra invitaciones de más de VIGENCIA_DIAS (contiene datos del evento:
    fecha/lugar/teléfono — no retener más de lo necesario)."""
    limite = time.time() - VIGENCIA_DIAS * 86400
    try:
        for fn in os.listdir(INVITACIONES_DIR):
            p = os.path.join(INVITACIONES_DIR, fn)
            if fn.endswith(".json") and os.path.getmtime(p) < limite:
                os.remove(p)
                png = p[:-5] + "_hero.png"
                if os.path.isfile(png):
                    os.remove(png)
    except OSError:
        pass


# ── helpers de contenido ─────────────────────────────────────────────────────

def parse_fecha_hora(fecha, hora):
    """(y, m, d, hh, mm) para la cuenta regresiva, o None si no se puede parsear.
    Acepta fecha 'DD/MM/AAAA' (o - o .; año de 2 dígitos ok) y hora 'HH[:MM]' con
    decorados tipo '16 hs'. La fecha del formulario es texto libre — si el cliente
    puso 'Sábado 12 de julio' no hay countdown, pero la página funciona igual."""
    m = re.search(r"(\d{1,2})[/\-.](\d{1,2})(?:[/\-.](\d{2,4}))?", fecha or "")
    if not m:
        return None
    d, mes = int(m.group(1)), int(m.group(2))
    anyo = int(m.group(3)) if m.group(3) else time.localtime().tm_year
    if anyo < 100:
        anyo += 2000
    if not (1 <= d <= 31 and 1 <= mes <= 12):
        return None
    hh, mm = 0, 0
    mh = re.search(r"(\d{1,2})(?::(\d{2}))?", hora or "")
    if mh:
        hh = min(int(mh.group(1)), 23)
        mm = min(int(mh.group(2) or 0), 59)
    return (anyo, mes, d, hh, mm)


def link_whatsapp(telefono, nombre):
    """wa.me del organizador con el mensaje de confirmación precargado, o None si
    no dejó teléfono. Normalización argentina permisiva: dígitos, saca el 0 inicial
    y el 15, antepone 549 si vino sin código de país."""
    digitos = re.sub(r"\D", "", telefono or "")
    if not digitos:
        return None
    if digitos.startswith("0"):
        digitos = digitos[1:]
    if digitos.startswith("549") and len(digitos) >= 12:
        pass
    elif digitos.startswith("54") and len(digitos) >= 11:
        digitos = "549" + digitos[2:]
    else:
        digitos = "549" + digitos   # local (área + número, ej. 1155554444)
    import urllib.parse
    msg = "¡Hola! Confirmo asistencia al cumple de %s 🎉 Somos: " % (nombre or "")
    return "https://wa.me/%s?text=%s" % (digitos, urllib.parse.quote(msg))


def link_maps(direccion, lugar):
    import urllib.parse
    consulta = ", ".join(x for x in (lugar, direccion) if x)
    if not consulta:
        return None
    return ("https://www.google.com/maps/search/?api=1&query="
            + urllib.parse.quote(consulta))


def _accent(tema):
    try:
        import temas as _temas
        d = json.load(open(os.path.join(_temas.TEMAS_DIR, tema, "tema.json")))
        h = ((d.get("kit") or {}).get("accent") or "#6B5BD2").lstrip("#")
        return "#" + h
    except Exception:
        return "#6B5BD2"


def _hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _tint(rgb, p):
    return tuple(int(v + (255 - v) * p) for v in rgb[:3])


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
        import glob
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


# ── imagen hero (encabezado de la página, con el arte del tema) ──────────────
# Dos niveles, igual que el libro: arte IA generado UNA VEZ por temática (el bueno)
# y el procedural como fallback para temas que todavía no lo generaron.

def _hero_ia_path(tema):
    import temas as _temas
    return os.path.join(_temas.TEMAS_DIR, tema or "safari", "invitacion_web_hero.png")


def generar_hero_ia(client, tema, calidad="medium"):
    """Genera con gpt-image-2 el hero del tema (una vez; queda para todas las
    invitaciones de esa temática). client = ia_kit OpenAIImageClient."""
    import libro_ia
    refs = libro_ia.referencias(tema)
    prompt = (
        "Ilustración panorámica para el encabezado de una invitación de cumpleaños "
        "infantil. Una escena festiva y alegre al aire libre con globos, banderines y "
        "confeti, con los personajes de las imágenes de referencia celebrando juntos, "
        "manteniendo su diseño exacto. Estilo ilustración infantil cálida, colores "
        "vivos. La escena llena TODA la imagen, sin marcos ni bordes. "
        "Importante: NO escribas ningún texto, número ni letra (no text, no letters)."
    )
    raw = client.editar(refs or [], prompt, "1536x1024", quality=calidad)
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    dest = _hero_ia_path(tema)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    img.save(dest)
    return dest


def _cover(img, W, H):
    s = max(W / img.width, H / img.height)
    im2 = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))),
                     Image.LANCZOS)
    x, y = (im2.width - W) // 2, (im2.height - H) // 2
    return im2.crop((x, y, x + W, y + H))


def _render_hero(tema):
    # arte IA del tema si existe
    p = _hero_ia_path(tema)
    if os.path.isfile(p):
        try:
            return _cover(Image.open(p).convert("RGB"), Wh, Hh)
        except Exception:
            pass
    return _render_hero_procedural(tema)


def _render_hero_procedural(tema):
    acc = _hex_rgb(_accent(tema))
    im = Image.new("RGB", (Wh, Hh), _tint(acc, 0.85))
    dr = ImageDraw.Draw(im)
    # cielo degradé simple
    top, bottom = _tint(acc, 0.75), _tint(acc, 0.92)
    for y in range(Hh):
        t = y / Hh
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        dr.line([(0, y), (Wh, y)], fill=c)
    # globos
    import random
    rnd = random.Random(hash(tema) & 0xffff)
    for _ in range(7):
        x, y = rnd.randint(60, Wh - 60), rnd.randint(40, 260)
        r = rnd.randint(26, 44)
        col = _tint(acc, rnd.choice([0.0, 0.25, 0.45]))
        dr.ellipse([x - r, y - int(r * 1.15), x + r, y + int(r * 1.15)], fill=col)
        dr.line([x, y + int(r * 1.15), x, y + int(r * 1.15) + 46],
                fill=_tint(acc, 0.3), width=3)
    # personajes del tema al pie
    try:
        import cuaderno
        ps = cuaderno.personajes_decorativos(tema, 3)
    except Exception:
        ps = []
    if ps:
        n = len(ps)
        for i, p in enumerate(ps):
            h = 300
            w = max(1, int(p.width * h / p.height))
            p2 = p.resize((w, h), Image.LANCZOS)
            cx = int(Wh * (i + 1) / (n + 1))
            im.paste(p2, (cx - w // 2, Hh - h - 20), p2)
    return im


def hero_png(token):
    """PNG del hero (cacheado junto al JSON; se regenera si el arte IA del tema
    apareció o cambió después). None si el token no existe."""
    reg = cargar(token)
    if not reg:
        return None
    cache = os.path.join(INVITACIONES_DIR, token + "_hero.png")
    ia = _hero_ia_path(reg["tema"])
    desactualizado = (os.path.isfile(ia) and os.path.isfile(cache)
                      and os.path.getmtime(ia) > os.path.getmtime(cache))
    if not os.path.isfile(cache) or desactualizado:
        _render_hero(reg["tema"]).save(cache)
    with open(cache, "rb") as f:
        return f.read()


# ── página HTML ──────────────────────────────────────────────────────────────

def _hero_version(tema):
    """Entero que cambia cuando cambia el arte del hero — va como ?v= en la URL
    para que Cloudflare (max-age largo) no sirva la versión vieja tras un update."""
    try:
        return int(os.path.getmtime(_hero_ia_path(tema)))
    except OSError:
        return 0


def html(token, base_url=""):
    """La página de la invitación (HTML completo, todo inline). None si no existe."""
    reg = cargar(token)
    if not reg:
        return None
    e = lambda s: html_mod.escape(s or "")
    acc = _accent(reg["tema"])
    acc_rgb = _hex_rgb(acc)
    suave = "rgb(%d,%d,%d)" % _tint(acc_rgb, 0.92)
    nombre, edad = reg["nombre"], reg["edad"]
    titulo = ("¡%s cumple %s!" % (nombre, edad)) if edad else ("¡Festejamos con %s!" % nombre)

    fh = parse_fecha_hora(reg["fecha"], reg["hora"])
    countdown_js = ""
    countdown_html = ""
    if fh:
        countdown_html = """
  <div class="cuenta" id="cuenta">
    <div class="chip"><b id="cd-d">–</b><span>días</span></div>
    <div class="chip"><b id="cd-h">–</b><span>horas</span></div>
    <div class="chip"><b id="cd-m">–</b><span>min</span></div>
    <div class="chip"><b id="cd-s">–</b><span>seg</span></div>
  </div>"""
        countdown_js = """
  var fin = new Date(%d, %d, %d, %d, %d, 0).getTime();
  function tick(){
    var t = fin - Date.now();
    if (t <= 0) { document.getElementById('cuenta').innerHTML =
      '<div class="chip llego">🎉 ¡Llegó el gran día!</div>'; return; }
    var s = Math.floor(t/1000);
    document.getElementById('cd-d').textContent = Math.floor(s/86400);
    document.getElementById('cd-h').textContent = Math.floor(s%%86400/3600);
    document.getElementById('cd-m').textContent = Math.floor(s%%3600/60);
    document.getElementById('cd-s').textContent = s%%60;
    setTimeout(tick, 1000);
  }
  tick();""" % (fh[0], fh[1] - 1, fh[2], fh[3], fh[4])

    wa = link_whatsapp(reg["telefono"], nombre)
    maps = link_maps(reg["direccion"], reg["lugar"])

    datos_filas = ""
    for icono, valor in (("📅", reg["fecha"]), ("🕒", reg["hora"]),
                          ("📍", reg["lugar"]), ("🏠", reg["direccion"])):
        if valor:
            datos_filas += ('<div class="fila"><span class="ic">%s</span>%s</div>'
                            % (icono, e(valor)))

    botones = ""
    if wa:
        botones += ('<a class="boton confirmar" href="%s" target="_blank" '
                    'rel="noopener">✅ Confirmar asistencia</a>' % e(wa))
    if maps:
        botones += ('<a class="boton mapa" href="%s" target="_blank" '
                    'rel="noopener">🗺️ Cómo llegar</a>' % e(maps))

    return """<!doctype html>
<html lang="es"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>%(titulo)s</title>
<meta property="og:title" content="%(titulo)s">
<meta property="og:description" content="¡Estás invitado! Tocá para ver la invitación 🎈">
<meta property="og:image" content="%(base)s/i/%(token)s/hero.png?v=%(hv)d">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Trebuchet MS',system-ui,sans-serif; background:%(suave)s; color:#3a3340; }
.hero { width:100%%; max-height:44vh; object-fit:cover; display:block; }
.tarjeta { max-width:520px; margin:-46px auto 26px; background:#fff; border-radius:22px;
  box-shadow:0 12px 40px rgba(0,0,0,.14); padding:30px 24px 26px; position:relative;
  text-align:center; }
h1 { color:%(acc)s; font-size:clamp(26px,7vw,40px); margin-bottom:6px; }
.sub { opacity:.65; font-size:15px; margin-bottom:18px; }
.cuenta { display:flex; gap:10px; justify-content:center; margin:18px 0 6px; flex-wrap:wrap; }
.chip { background:%(suave)s; border:2px solid %(acc)s33; border-radius:14px;
  min-width:64px; padding:10px 8px; }
.chip b { display:block; font-size:26px; color:%(acc)s; }
.chip span { font-size:11px; text-transform:uppercase; letter-spacing:.06em; opacity:.6; }
.chip.llego { font-size:18px; padding:14px 18px; color:%(acc)s; }
.datos { margin:20px auto 6px; text-align:left; max-width:360px; }
.fila { padding:9px 0; border-bottom:1px dashed %(acc)s2e; font-size:16px; }
.fila:last-child { border-bottom:0; }
.ic { display:inline-block; width:30px; }
.botones { display:flex; flex-direction:column; gap:12px; margin-top:22px; }
.boton { display:block; padding:15px 18px; border-radius:14px; text-decoration:none;
  font-weight:700; font-size:17px; transition:transform .1s; }
.boton:active { transform:scale(.97); }
.confirmar { background:#25D366; color:#fff; }
.mapa { background:%(acc)s; color:#fff; }
.pie { text-align:center; font-size:12px; opacity:.45; padding:18px 0 26px; }
.globos { position:fixed; inset:0; pointer-events:none; overflow:hidden; z-index:-1; }
.globo { position:absolute; bottom:-70px; font-size:34px; animation:subir linear infinite; }
@keyframes subir { to { transform:translateY(-120vh) rotate(12deg); } }
</style></head><body>
<div class="globos">
  <span class="globo" style="left:8%%;animation-duration:11s">🎈</span>
  <span class="globo" style="left:28%%;animation-duration:14s;animation-delay:3s">🎈</span>
  <span class="globo" style="left:55%%;animation-duration:12s;animation-delay:6s">🎉</span>
  <span class="globo" style="left:78%%;animation-duration:15s;animation-delay:1s">🎈</span>
</div>
<img class="hero" src="%(base)s/i/%(token)s/hero.png?v=%(hv)d" alt="">
<div class="tarjeta">
  <h1>%(titulo_e)s</h1>
  <div class="sub">¡Estás invitado a festejar!</div>
  %(countdown_html)s
  <div class="datos">%(datos_filas)s</div>
  <div class="botones">%(botones)s</div>
</div>
<div class="pie">casatridimensional.com.ar</div>
<script>%(countdown_js)s</script>
</body></html>""" % {
        "titulo": e(titulo), "titulo_e": e(titulo), "token": e(token),
        "base": e(base_url), "acc": acc, "suave": suave,
        "hv": _hero_version(reg["tema"]),
        "countdown_html": countdown_html, "countdown_js": countdown_js,
        "datos_filas": datos_filas, "botones": botones,
    }


# ── mock para la ficha del producto (galería de la tienda) ───────────────────

def preview_mock(data, tema="safari"):
    """Imagen tipo "celular con la invitación abierta" para la galería del producto
    — un dibujo Pillow de la página real, con los datos de ejemplo del formulario."""
    acc = _hex_rgb(_accent(tema))
    W, H = 900, 1400
    im = Image.new("RGB", (W, H), _tint(acc, 0.9))
    dr = ImageDraw.Draw(im)
    # marco de celular
    dr.rounded_rectangle([130, 60, W - 130, H - 60], 64, fill="black")
    px0, py0, px1, py1 = 150, 80, W - 150, H - 80
    dr.rounded_rectangle([px0, py0, px1, py1], 48, fill=_tint(acc, 0.93))
    # hero
    hero = _render_hero(tema).resize((px1 - px0, 300))
    im.paste(hero, (px0, py0))
    # tarjeta
    dr.rounded_rectangle([px0 + 40, py0 + 250, px1 - 40, py1 - 90], 30, fill="white")
    nombre = (str(data.get("nombre") or "").strip()) or "Valen"
    edad = (str(data.get("edad") or "").strip()) or "5"
    dr.text(((px0 + px1) / 2, py0 + 330), "¡%s cumple %s!" % (nombre, edad),
            font=_font(56), fill=acc, anchor="mm")
    dr.text(((px0 + px1) / 2, py0 + 390), "¡Estás invitado a festejar!",
            font=_font(26, False), fill=(120, 110, 125), anchor="mm")
    # chips countdown
    for i, (num, lbl) in enumerate((("12", "días"), ("07", "horas"),
                                     ("33", "min"), ("09", "seg"))):
        cx = (px0 + px1) / 2 + (i - 1.5) * 130
        dr.rounded_rectangle([cx - 55, py0 + 430, cx + 55, py0 + 540], 22,
                             fill=_tint(acc, 0.92), outline=_tint(acc, 0.6), width=3)
        dr.text((cx, py0 + 470), num, font=_font(42), fill=acc, anchor="mm")
        dr.text((cx, py0 + 515), lbl, font=_font(18, False), fill=(120, 110, 125),
                anchor="mm")
    # filas de datos (viñeta dibujada — Fredoka no tiene emojis)
    y = py0 + 590
    for txt in ("Sábado 12 de julio", "16:00 hs",
                 "Salón Arcoiris", "Av. Siempreviva 742"):
        dr.ellipse([px0 + 82, y - 9, px0 + 100, y + 9], fill=_tint(acc, 0.35))
        dr.text((px0 + 118, y), txt, font=_font(28, False), fill=(70, 62, 78),
                anchor="lm")
        dr.line([px0 + 80, y + 30, px1 - 80, y + 30], fill=_tint(acc, 0.85), width=2)
        y += 66
    # botones
    dr.rounded_rectangle([px0 + 80, y + 20, px1 - 80, y + 100], 22, fill=(37, 211, 102))
    dr.text(((px0 + px1) / 2, y + 60), "Confirmar asistencia", font=_font(30),
            fill="white", anchor="mm")
    dr.rounded_rectangle([px0 + 80, y + 120, px1 - 80, y + 200], 22, fill=acc)
    dr.text(((px0 + px1) / 2, y + 160), "Cómo llegar", font=_font(30),
            fill="white", anchor="mm")
    dr.text((W / 2, py1 - 40), "Invitación web interactiva · se comparte por WhatsApp",
            font=_font(22, False), fill=(110, 100, 118), anchor="mm")
    return im


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: OPENAI_API_KEY=... python invitacion_web.py <tema> [tema2 ...]")
        sys.exit(1)
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("Falta OPENAI_API_KEY.")
        sys.exit(1)
    from ia_kit.client import OpenAIImageClient
    cl = OpenAIImageClient(key, model=os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-2"))
    for t in sys.argv[1:]:
        print("hero IA de", t, "…")
        print("  ->", generar_hero_ia(cl, t))
