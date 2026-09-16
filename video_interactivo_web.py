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
    return h.hexdigest()[:10]


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


def archivo(pieza, nombre):
    """(bytes, content-type) de un archivo de la pieza, o None."""
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
