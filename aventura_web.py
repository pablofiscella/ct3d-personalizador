"""aventura_web.py — modalidad WEB del prototipo "Elegí tu propia aventura": lector de
cuento con decisiones que arman un camino distinto cada vez, entregado como link vivo
`/leer/<token>/` (mismo patrón que actividades_web / rompecabezas_web / mandalas_web:
token -> manifest.json -> player servido DEL REPO).

El contenido narrativo vive en aventura.py. El arte NO se copia al token: se sirve
directo de temas/<tema>/overrides/libro/ (las mismas escenas del libro de cuento), así
el token pesa casi nada, igual que mandalas_web con mandalas_arte/.
"""
from __future__ import annotations
import json
import os
import re
import secrets
import time

import aventura
import temas as _temas

BASEDIR = os.path.dirname(os.path.abspath(__file__))
AV_DIR = os.path.join(BASEDIR, "aventura_web")           # carpetas por token (gitignored)
TEMPLATE_HTML = os.path.join(BASEDIR, "aventura_player.html")
TEMPLATE_JS = os.path.join(BASEDIR, "aventura_player.js")
_TOKEN_RE = r"[A-Za-z0-9_-]{8,32}"


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


# ── Generación (una carpeta por compra/demo) ─────────────────────────────────
def crear(data, tema=None, token=None):
    """Arma aventura_web/<token>/manifest.json con el grafo ya personalizado (nombre +
    variante de género resuelta). Devuelve el token."""
    data = dict(data or {})
    tema = (tema or data.get("tema") or "safari").strip() or "safari"
    if tema not in aventura.AVENTURAS:
        raise ValueError(f"todavía no hay aventura armada para el tema '{tema}'")
    nombre = str(data.get("nombre") or "").strip()
    genero = data.get("genero")
    g = aventura.grafo(tema, nombre, genero)
    token = token or secrets.token_urlsafe(12)
    dest = os.path.join(AV_DIR, token)
    os.makedirs(dest, exist_ok=True)
    titulo = f"La aventura de {nombre}" if nombre else "Elegí tu aventura"
    with open(os.path.join(dest, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"v": 1, "tema": tema, "titulo": titulo, "nombre": nombre,
                   "inicio": aventura.INICIO, "nodos": g, "ts": int(time.time())},
                  f, ensure_ascii=False)
    return token


def _cargar(token):
    if not re.fullmatch(_TOKEN_RE, token or ""):
        return None
    p = os.path.join(AV_DIR, token, "manifest.json")
    if not os.path.isfile(p):
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def estado(token):
    return "listo" if _cargar(token) else None


# ── Servido (visor + assets) ──────────────────────────────────────────────────
def _player_version():
    try:
        return str(int(max(os.path.getmtime(TEMPLATE_JS), os.path.getmtime(TEMPLATE_HTML))))
    except OSError:
        return "1"


def html(token):
    """El visor HTML (rutas relativas -> servir SIEMPRE bajo /leer/<token>/)."""
    reg = _cargar(token)
    if not reg:
        return None
    with open(TEMPLATE_HTML, encoding="utf-8") as f:
        t = f.read()
    # INICIO/NODOS se inyectan como JSON crudo (contexto JS), no _esc.
    return (t.replace("{{TITULO}}", _esc(reg.get("titulo") or "Elegí tu aventura"))
             .replace("{{INICIO}}", json.dumps(reg.get("inicio")))
             .replace("{{NODOS}}", json.dumps(reg.get("nodos"), ensure_ascii=False))
             .replace("{{V}}", _player_version()))


_ASSET_RE = re.compile(r"^(player\.js|[2-8](_nena)?\.png|manifest\.json)$")
_CT = {".js": "text/javascript; charset=utf-8", ".png": "image/png",
       ".json": "application/json; charset=utf-8"}


def archivo(token, nombre):
    """(bytes, content_type) de un asset, o None. player.js y las escenas salen del REPO
    (temas/<tema>/overrides/libro/ — el mismo arte del libro de cuento); manifest.json
    sale de la carpeta del token."""
    reg = _cargar(token)
    if not reg or not _ASSET_RE.fullmatch(nombre or ""):
        return None
    if nombre == "player.js":
        p = TEMPLATE_JS
    elif nombre == "manifest.json":
        p = os.path.join(AV_DIR, token, "manifest.json")
    else:
        p = os.path.join(_temas.TEMAS_DIR, reg["tema"], "overrides", "libro", nombre)
    if not os.path.isfile(p):
        return None
    ct = _CT[os.path.splitext(nombre)[1]]
    with open(p, "rb") as f:
        return f.read(), ct
