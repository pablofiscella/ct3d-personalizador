"""video_interactivo_web.py — sirve un VIDEO INTERACTIVO bajo /vi/<pieza>/ (piloto, 15-sep-2026).

Mismo patrón que aventura_web (/leer/<token>/): la página y el reproductor salen del REPO, así una
mejora del reproductor llega a todas las piezas; las imágenes, la voz y el guion viven en
videos_interactivos/<pieza>/. Rutas relativas: servir SIEMPRE bajo /vi/<pieza>/.

A diferencia de los productos con token, una pieza no es de un chico: es contenido del cuaderno,
igual que una lección en video. Por eso la dirección es la pieza y no un token.
"""
import hashlib
import json
import os
import re

KIT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(KIT, "videos_interactivos")
_PIEZA_RE = re.compile(r"^[a-z0-9_]{1,60}$")
_ARCHIVO_RE = re.compile(r"^[a-z0-9_]{1,80}\.(webp|mp3)$")
_TIPOS = {"webp": "image/webp", "mp3": "audio/mpeg"}


COMUN = os.path.join(BASE, "_comun")
_VERSIONES = {}   # pieza -> (firma de los archivos, huella); ver `version`


def _carpeta(pieza):
    if not _PIEZA_RE.match(pieza or "") or pieza == "_comun":
        return None
    ruta = os.path.join(BASE, pieza)
    return ruta if os.path.isfile(os.path.join(ruta, "guion.json")) else None


def ruta_de(pieza, nombre):
    """El archivo de la pieza, o el COMÚN si no lo tiene. Carpi es de todas las piezas: tenerlo
    copiado en cada carpeta sería pagar tres imágenes por video y que envejezcan distinto."""
    carpeta = _carpeta(pieza)
    if not carpeta or not _ARCHIVO_RE.match(nombre or ""):
        return None
    for d in (carpeta, COMUN):
        ruta = os.path.join(d, nombre)
        if os.path.isfile(ruta):
            return ruta
    return None


def version(pieza):
    """Huella de TODO lo que el navegador se baja de la pieza: el reproductor, la página y cada
    imagen y cada voz.

    Por qué existe (15-sep-2026, Pablo: *"se quedó ahí y no dijo nada más después de la rima"*): los
    archivos se sirven con caché de horas y SIEMPRE con el mismo nombre, así que quien ya abrió la
    pieza se queda con el reproductor y las voces de entonces. Ese día le tocó el reproductor viejo
    con el guion nuevo —el paso final pasó a sortearse y el viejo no sabía leerlo—, y el video se
    trabó a la mitad. Es el mismo defecto que ya había mordido en los videos de divulgación:
    contenido distinto tiene que tener dirección distinta, o el navegador sirve el de antes.

    Se cuenta el CONTENIDO y no la fecha del archivo: `probar` los reescribe en cada despliegue y,
    por fecha, se tiraría la caché entera sin que hubiera cambiado nada."""
    carpeta = _carpeta(pieza)
    if not carpeta:
        return ""
    # La huella lee el contenido de todo (unos megas por pieza), y ahora la piden la lista del
    # cuaderno y cada miniatura en cada carga. Se recuerda mientras no cambie ningún archivo: la
    # firma de nombres, tamaños y fechas es barata, y si `probar` reescribe las fechas sólo se
    # vuelve a calcular — el valor sale igual, porque cuenta el contenido.
    firma = []
    for ruta in (os.path.join(KIT, "video_interactivo_player.js"),
                 os.path.join(KIT, "video_interactivo_player.html"),
                 os.path.join(carpeta, "guion.json")):
        st = os.stat(ruta)
        firma.append((ruta, st.st_size, st.st_mtime_ns))
    for d in (carpeta, COMUN):
        for n in sorted(os.listdir(d)):
            if _ARCHIVO_RE.match(n):
                st = os.stat(os.path.join(d, n))
                firma.append((d, n, st.st_size, st.st_mtime_ns))
    firma = tuple(firma)
    if _VERSIONES.get(pieza, (None,))[0] == firma:
        return _VERSIONES[pieza][1]
    h = hashlib.sha256()
    for ruta in (os.path.join(KIT, "video_interactivo_player.js"),
                 os.path.join(KIT, "video_interactivo_player.html"),
                 os.path.join(carpeta, "guion.json")):
        with open(ruta, "rb") as f:
            h.update(f.read())
    for d in (carpeta, COMUN):
        for n in sorted(os.listdir(d)):
            if not _ARCHIVO_RE.match(n):
                continue
            h.update(n.encode("utf-8"))
            with open(os.path.join(d, n), "rb") as f:
                h.update(f.read())
    _VERSIONES[pieza] = (firma, h.hexdigest()[:10])
    return _VERSIONES[pieza][1]


def html(pieza):
    """La página de la pieza, o None si no existe."""
    carpeta = _carpeta(pieza)
    if not carpeta:
        return None
    with open(os.path.join(carpeta, "guion.json"), encoding="utf-8") as f:
        guion = json.load(f)
    with open(os.path.join(KIT, "video_interactivo_player.html"), encoding="utf-8") as f:
        pagina = f.read()
    # El guion viaja entero salvo los prompts de las imágenes, que son de producción y no le sirven
    # al reproductor. `</` se escapa para que un texto nunca pueda cerrar el <script>.
    para_el_player = dict(guion)
    para_el_player["imagenes"] = {k: {"tipo": v.get("tipo")} for k, v in guion["imagenes"].items()}
    datos = json.dumps(para_el_player, ensure_ascii=False).replace("</", "<\\/")
    return (pagina.replace("{{GUION}}", datos)
                  .replace("{{VERSION}}", version(pieza))
                  .replace("{{TITULO}}", _escapar(guion.get("titulo", "")))
                  .replace("{{GRADO}}", str(int(guion.get("grado", 0)))))


def indice():
    """Los videos que hay, para la sección «Videos interactivos» del cuaderno.

    Pablo, 16-sep-2026: *"quiero que vayas agregando los videos a una última sección que se llame
    videos interactivos, antes de las tarjetas extras"*. El cuaderno la pide EN VIVO y no la lee
    de su `data.json`, porque ese archivo queda congelado el día que se compró: un video nuevo no
    le llegaría nunca a un cuaderno ya entregado. Así, sumar una pieza a `videos_interactivos/`
    alcanza para que aparezca en todos los cuadernos de su grado."""
    videos = []
    for pieza in sorted(os.listdir(BASE)):
        carpeta = _carpeta(pieza)
        if not carpeta:
            continue
        with open(os.path.join(carpeta, "guion.json"), encoding="utf-8") as f:
            g = json.load(f)
        videos.append({"pieza": pieza, "titulo": g.get("titulo") or pieza,
                       "grado": int(g.get("grado") or 0), "saber": g.get("saber"),
                       "version": version(pieza)})
    return sorted(videos, key=lambda v: (v["grado"], v["titulo"]))


# Miniatura de la tarjeta, por pieza y versión: el fondo entero pesa 300 KB y el menú de un
# celular carga todas las tarjetas juntas. Se arma una vez y se guarda en memoria.
_PORTADAS = {}


def portada(pieza):
    """La escena con la que arranca el video, chica (480 px de ancho), o None."""
    carpeta = _carpeta(pieza)
    if not carpeta:
        return None
    clave = (pieza, version(pieza))
    if clave not in _PORTADAS:
        from io import BytesIO
        from PIL import Image
        with open(os.path.join(carpeta, "guion.json"), encoding="utf-8") as f:
            g = json.load(f)
        escena = g["escenas"][g["pasos"][0]["escena"]]
        ruta = ruta_de(pieza, escena["fondo"] + ".webp")
        if not ruta:
            return None
        im = Image.open(ruta).convert("RGB")
        im.thumbnail((480, 480))
        buf = BytesIO()
        im.save(buf, "WEBP", quality=78)
        _PORTADAS[clave] = buf.getvalue()
    return _PORTADAS[clave]


def archivo(pieza, nombre):
    """(bytes, content-type) de un archivo de la pieza, o None."""
    if nombre == "portada.webp":
        datos = portada(pieza)
        return (datos, "image/webp") if datos else None
    if nombre == "player.js":
        if not _carpeta(pieza):
            return None
        with open(os.path.join(KIT, "video_interactivo_player.js"), "rb") as f:
            return f.read(), "application/javascript; charset=utf-8"
    ruta = ruta_de(pieza, nombre)
    if not ruta:
        return None
    with open(ruta, "rb") as f:
        return f.read(), _TIPOS[_ARCHIVO_RE.match(nombre).group(1)]


def _escapar(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))
