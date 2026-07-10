"""mandalas_web.py — modalidad WEB del kit de mándalas: app para pintar en el navegador
(balde/flood-fill sobre las mándalas line-art) + descarga del PDF imprimible, entregada
como link vivo `/pintar/<token>/` (aparece en Mi biblioteca, como el audiolibro).

Un solo producto `mandalas` = DOS modalidades: el link web (pintar online) y el PDF
(botón de descarga dentro del visor). El player se sirve DESDE EL REPO (mejoras llegan a
links ya vendidos); las 6 mándalas son FIJAS y también salen del repo (mandalas_arte/),
así el token pesa casi nada. Lo único por token: el kit.zip (PDF con portada personalizada)
y la portada.jpg (cover de biblioteca).
"""
from __future__ import annotations
import json
import os
import re
import secrets
import time

import mandalas

BASEDIR = os.path.dirname(os.path.abspath(__file__))
MW_DIR = os.path.join(BASEDIR, "mandalas_web")          # carpetas por token (gitignored)
ART_DIR = os.path.join(BASEDIR, "mandalas_arte")        # las 6 mándalas fijas (en el repo)
TEMPLATE_HTML = os.path.join(BASEDIR, "mandalas_player.html")
TEMPLATE_JS = os.path.join(BASEDIR, "mandalas_player.js")
NIVELES = mandalas.NIVELES
_TOKEN_RE = r"[A-Za-z0-9_-]{8,32}"


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


# ── Generación (una carpeta por compra) ──────────────────────────────────────
def crear(data, token=None):
    """Arma mandalas_web/<token>/ con el kit.zip (PDF, portada personalizada) + portada.jpg.
    Devuelve el token. Las mándalas para pintar NO se copian (salen del repo)."""
    data = dict(data or {})
    tema = (data.get("tema") or "safari").strip() or "safari"
    token = token or secrets.token_urlsafe(12)
    dest = os.path.join(MW_DIR, token)
    os.makedirs(dest, exist_ok=True)

    # PDF imprimible (mismo pipeline que la modalidad impresa) → kit.zip en el token
    import productos
    productos.generar(data, dest, tema, "mandalas")

    # Cover de biblioteca (la portada, achicada)
    try:
        port = mandalas.portada(data).convert("RGB")
        port.thumbnail((900, 1273))
        port.save(os.path.join(dest, "portada.jpg"), quality=88)
    except Exception:
        pass

    nombre = str(data.get("nombre") or "").strip()
    titulo = f"Mándalas de {nombre}" if nombre else "Mándalas para pintar"
    with open(os.path.join(dest, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"v": 1, "nombre": nombre, "titulo": titulo, "ts": int(time.time())},
                  f, ensure_ascii=False)
    return token


def _cargar(token):
    if not re.fullmatch(_TOKEN_RE, token or ""):
        return None
    p = os.path.join(MW_DIR, token, "manifest.json")
    if not os.path.isfile(p):
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def estado(token):
    return "listo" if _cargar(token) else None


# ── Servido (visor + assets) ─────────────────────────────────────────────────
def _player_version():
    try:
        return str(int(max(os.path.getmtime(TEMPLATE_JS), os.path.getmtime(TEMPLATE_HTML))))
    except OSError:
        return "1"


def html(token):
    """El visor HTML (rutas relativas → servir SIEMPRE bajo /pintar/<token>/)."""
    reg = _cargar(token)
    if not reg:
        return None
    with open(TEMPLATE_HTML, encoding="utf-8") as f:
        t = f.read()
    # NIVELES y NOMBRE se inyectan en un <script> (contexto JS) → JSON crudo, NO _esc
    # (los labels son fijos; el nombre va JSON-encodeado para cerrar bien el string).
    niveles = json.dumps([{"src": f"mandala_{i}.png", "dif": mandalas.DIFICULTAD[i - 1]}
                          for i in range(1, NIVELES + 1)], ensure_ascii=False)
    return (t.replace("{{TITULO}}", _esc(reg.get("titulo") or "Mándalas para pintar"))
             .replace("{{NIVELES}}", niveles)
             .replace("{{NOMBRE}}", json.dumps(reg.get("nombre") or "", ensure_ascii=False))
             .replace("{{V}}", _player_version()))


_ASSET_RE = re.compile(r"^(player\.js|mandala_[1-6]\.png|portada\.jpg|kit\.zip|manifest\.json)$")
_CT = {".js": "text/javascript; charset=utf-8", ".png": "image/png", ".jpg": "image/jpeg",
       ".zip": "application/zip", ".json": "application/json; charset=utf-8"}


def archivo(token, nombre):
    """(bytes, content_type) de un asset, o None. player.js y las mándalas salen del REPO;
    kit.zip / portada.jpg / manifest.json salen de la carpeta del token."""
    if not _cargar(token) or not _ASSET_RE.fullmatch(nombre or ""):
        return None
    m = re.fullmatch(r"mandala_([1-6])\.png", nombre)
    if nombre == "player.js":
        p = TEMPLATE_JS
    elif m:
        p = os.path.join(ART_DIR, f"{m.group(1)}.png")
    else:
        p = os.path.join(MW_DIR, token, nombre)
    if not os.path.isfile(p):
        return None
    ct = _CT[os.path.splitext(nombre)[1]]
    with open(p, "rb") as f:
        return f.read(), ct


def preview_mock(data, tema=None):
    """Cover para la ficha del producto (sin crear token): la portada."""
    return mandalas.portada(data)
