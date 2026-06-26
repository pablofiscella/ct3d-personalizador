#!/usr/bin/env python3
"""
Servicio de generación del kit "Un Añito Salvaje" (Fase 3).
Sin dependencias externas (solo stdlib) para deploy fácil en CT101.

Endpoints:
  GET  /health                      -> {"ok": true}
  GET  /preview?nombre=&fecha=...    -> PNG de la invitación (vista previa)
  POST /api/generar  (X-API-Key)     -> genera el kit, devuelve {token, download_url}
  GET  /descarga/<token>             -> baja el ZIP del kit

Config por variables de entorno:
  CT3D_API_KEY   clave que debe mandar WooCommerce (default: 'cambiame-ya')
  CT3D_PORT      puerto (default 8787)
  CT3D_DATA_DIR  dónde guardar los kits generados (default ./pedidos)
  CT3D_BASE_URL  URL pública del servicio (para armar el link de descarga)
"""
import os, io, json, re, secrets, threading, time, collections, urllib.parse, urllib.request, urllib.error, base64
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import piezas  # motor (generar_kit, preview_invitacion)
import productos  # registro de TIPOS de producto digital (kit, invitacion, cartel, actividades, milestone)
import mate as mate_mod  # editor de mates (grabado láser)
import generador  # layout del editor
import temas          # alta de temáticas (dashboard)
import quitar_fondo   # recorte de fondo de animalitos/números subidos
from PIL import Image

API_KEY  = os.environ.get("CT3D_API_KEY", "cambiame-ya")
PORT     = int(os.environ.get("CT3D_PORT", "8787"))
DATA_DIR = os.environ.get("CT3D_DATA_DIR", os.path.join(os.path.dirname(__file__), "pedidos"))
BASE_URL = os.environ.get("CT3D_BASE_URL", f"http://localhost:{PORT}")
# Auth del panel (dashboard + editor): token por cookie, sin login interactivo.
# Se entra una sola vez con ?key=API_KEY (link desde tu dash); kit deja una
# cookie segura y a partir de ahí todo va autenticado solo. Nadie sin el token
# (cookie, header X-API-Key o ?key=) puede tocar las rutas privadas.
ADMIN_COOKIE = "__Host-ct3d_sess"   # C3: cookie = token de sesión aleatorio, NO la API key

CAMPOS = ["nombre", "fecha", "hora", "lugar", "direccion", "telefono", "edad"]

# ---- config de WooCommerce (para publicar productos desde el panel) ----
WOO_CONFIG = os.path.join(generador.BASEDIR, "woo_config.json")
def _woo_cfg():
    try:
        return json.load(open(WOO_CONFIG, encoding="utf-8"))
    except Exception:
        return {}
def _woo_save(d):
    with open(WOO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# ---- registro de publicaciones (qué temática → qué producto de Woo) ----
PUB_CONFIG = os.path.join(generador.BASEDIR, "woo_pub.json")
def _pub_cfg():
    try:
        return json.load(open(PUB_CONFIG, encoding="utf-8"))
    except Exception:
        return {}
def _pub_save(d):
    with open(PUB_CONFIG, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def _wc_call(method, path, payload=None):
    """Llama a la API REST de WooCommerce (POST/PUT/DELETE) con clave/secreto."""
    cfg = _woo_cfg()
    url = (cfg.get("url") or "").rstrip("/")
    if not (url and cfg.get("key") and cfg.get("secret")):
        raise Exception("faltan credenciales de WooCommerce (configuralas en el panel)")
    endpoint = url + "/wp-json/wc/v3/" + path.lstrip("/")
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    auth = base64.b64encode(("%s:%s" % (cfg["key"], cfg["secret"])).encode()).decode()
    headers = {"Authorization": "Basic " + auth, "User-Agent": "CT3D-Kit/1.0"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(endpoint, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=45) as r:
        body = r.read().decode("utf-8")
        return json.loads(body) if body else {}

def _wc_crear_producto(payload):
    return _wc_call("POST", "products", payload)

def _edit_url(pid):
    return _woo_cfg().get("url", "").rstrip("/") + "/wp-admin/post.php?post=%s&action=edit" % pid

def slug(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", str(s)).strip("-").lower()
    return s or "kit"

# Headers de seguridad en TODA respuesta (A4). frame-ancestors permite que la tienda
# (apex + subdominios) embeba el editor por iframe; cualquier otro sitio no puede.
_SEC_HEADERS = [
    ("X-Content-Type-Options", "nosniff"),
    ("Referrer-Policy", "no-referrer"),
    ("Strict-Transport-Security", "max-age=63072000; includeSubDomains"),
    ("Content-Security-Policy",
     "frame-ancestors 'self' https://casatridimensional.com.ar https://*.casatridimensional.com.ar"),
]
MAX_BODY = 8 * 1024 * 1024        # 8 MB: tope de cuerpo POST (A7, anti memory-bomb)
_SEM = threading.Semaphore(16)    # máx 16 requests concurrentes (A7, anti thread-exhaustion)
_KEY_RE = re.compile(r"(key=)[^&\s\"']+", re.I)

# C3: sesiones admin con token aleatorio en memoria (la cookie ya NO es la API key;
# revocable y con TTL). Se pierden al reiniciar → el admin reentra por el link ?key=.
_SESSIONS = {}
_SESS_LOCK = threading.Lock()
_SESS_TTL = 7 * 24 * 3600

def _new_session():
    tok = secrets.token_urlsafe(32)
    now = time.monotonic()
    with _SESS_LOCK:
        for k in [k for k, exp in _SESSIONS.items() if exp < now]:
            _SESSIONS.pop(k, None)
        _SESSIONS[tok] = now + _SESS_TTL
    return tok

def _session_valid(tok):
    if not tok:
        return False
    with _SESS_LOCK:
        exp = _SESSIONS.get(tok)
    return bool(exp and exp > time.monotonic())

# A1: rate limiting por IP (ventana deslizante) en endpoints públicos pesados.
_RL = collections.defaultdict(collections.deque)
_RL_LOCK = threading.Lock()

def _rate_ok(ip, limit=40, window=60):
    if not ip or ip.startswith("127.") or ip in ("::1", "localhost"):
        return True                       # llamadas internas (la tienda) no se limitan
    now = time.monotonic()
    with _RL_LOCK:
        dq = _RL[ip]
        while dq and dq[0] < now - window:
            dq.popleft()
        if len(dq) >= limit:
            return False
        dq.append(now)
        if len(_RL) > 4096:               # poda de IPs inactivas
            for k in [k for k, v in list(_RL.items()) if not v]:
                _RL.pop(k, None)
    return True


def _limpiar_pedidos_viejos(dias=30):
    """A3: borra carpetas de pedidos (ZIP + meta) de más de `dias` — no acumular PII."""
    import shutil
    try:
        corte = time.time() - dias * 86400
        for n in os.listdir(DATA_DIR):
            p = os.path.join(DATA_DIR, n)
            try:
                if os.path.isdir(p) and os.path.getmtime(p) < corte:
                    shutil.rmtree(p, ignore_errors=True)
            except OSError:
                pass
    except OSError:
        pass


class Handler(BaseHTTPRequestHandler):
    server_version = "CT3D-Kit/1.0"
    timeout = 30                   # corta conexiones colgadas (A7, anti slowloris)

    def handle_one_request(self):
        with _SEM:                 # serializa bajo presión: no spawnea threads infinitos
            super().handle_one_request()

    def end_headers(self):
        for k, v in _SEC_HEADERS:
            self.send_header(k, v)
        super().end_headers()

    def _origin_ok(self):
        """En POST de navegador, el Origin/Referer debe ser nuestro host (anti-CSRF, A5).
        Llamadas server-to-server (sin Origin) pasan; el webhook usa además X-API-Key."""
        o = self.headers.get("Origin") or self.headers.get("Referer") or ""
        if not o:
            return True
        try:
            host = urllib.parse.urlparse(o).netloc.lower().split(":")[0]
        except Exception:
            return False
        return host == "casatridimensional.com.ar" or host.endswith(".casatridimensional.com.ar") \
            or host in ("localhost", "127.0.0.1")

    def _body(self):
        """Lee el cuerpo con tope de tamaño (A7). Devuelve None si excede MAX_BODY."""
        n = int(self.headers.get("Content-Length", "0") or 0)
        if n > MAX_BODY:
            return None
        return self.rfile.read(n) or b"{}"

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        msg = _KEY_RE.sub(r"\1***", fmt % args)    # C4/M6: nunca logear la API key
        print("[svc]", self.address_string(), msg)

    def base_url(self):
        """Arma la URL pública según los headers (Cloudflare/reverse proxy).
        Así el link de descarga es correcto sin hardcodear nada."""
        host = self.headers.get("X-Forwarded-Host") or self.headers.get("Host")
        if host:
            proto = self.headers.get("X-Forwarded-Proto") or "http"
            return f"{proto}://{host}"
        return BASE_URL

    def _admin_ok(self, u=None):
        """¿Viene el token del panel? Acepta cookie, header X-API-Key o ?key=.
        Así el link de entrada (?key=) y las llamadas AJAX (cookie/header) funcionan
        sin pedir un login. Cualquier otro → denegado."""
        # 1) cookie de sesión (token aleatorio, no la API key)
        for part in self.headers.get("Cookie", "").split(";"):
            if "=" in part:
                k, v = part.strip().split("=", 1)
                if k == ADMIN_COOKIE and _session_valid(v):
                    return True
        # 2) header X-API-Key (llamadas AJAX del panel)
        if secrets.compare_digest(self.headers.get("X-API-Key", "") or "", API_KEY):
            return True
        # 3) ?key= en la URL (link de entrada desde tu dash)
        if u is None:
            u = urllib.parse.urlparse(self.path)
        if secrets.compare_digest(urllib.parse.parse_qs(u.query).get("key", [""])[0], API_KEY):
            return True
        return False

    def _deny(self):
        """403 plano (no es un login: no pide credenciales, solo niega)."""
        body = ("Acceso restringido. Este panel se abre únicamente desde el "
                "dashboard de Casa Tridimensional.").encode("utf-8")
        self.send_response(403)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _cookie_header(self):
        """Set-Cookie con un token de SESIÓN nuevo (no la API key). __Host- + Secure +
        HttpOnly + SameSite=Lax, 7 días. Se emite tras validar el ?key= en _admin_ok."""
        return ("%s=%s; Path=/; Max-Age=604800; HttpOnly; Secure; SameSite=Lax"
                % (ADMIN_COOKIE, _new_session()))

    def _client_ip(self):
        """IP real del cliente detrás de Cloudflare (para rate limiting)."""
        return (self.headers.get("CF-Connecting-IP")
                or (self.headers.get("X-Forwarded-For") or "").split(",")[0].strip()
                or self.client_address[0])

    # ---------------- GET ----------------
    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        path = u.path
        # A1: rate limit en endpoints públicos pesados (render Pillow / descargas).
        if path.startswith(("/preview", "/mate/preview", "/cliente-bg.png",
                            "/editor-bg.png", "/descarga/", "/piezas")) \
                and not _rate_ok(self._client_ip()):
            return self._json(429, {"ok": False, "error": "demasiadas solicitudes, esperá un minuto"})
        if path == "/health":
            return self._json(200, {"ok": True, "servicio": "kit-anito-salvaje"})
        if path == "/":
            # Si sos admin (cookie/clave) → al panel de kits /dash; si no, a la tienda.
            dest = "/dash" if self._admin_ok(u) else "https://casatridimensional.com.ar"
            self.send_response(302)
            self.send_header("Location", dest)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if path == "/plugin.zip":
            # descarga del plugin de WordPress (protegida con el token; sin secretos adentro)
            if not self._admin_ok(u):
                return self._deny()
            zp = os.path.join(generador.BASEDIR, "wordpress", "ct3d-kit-personalizado.zip")
            if not os.path.isfile(zp):
                return self._json(404, {"ok": False, "error": "zip no encontrado"})
            data = open(zp, "rb").read()
            self.send_response(200)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition", 'attachment; filename="ct3d-kit-personalizado.zip"')
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers(); self.wfile.write(data)
            return
        if path == "/tipos":
            # catálogo de tipos de producto digital (descubrimiento dinámico para la tienda/ABM)
            return self._json(200, {"ok": True, "tipos": productos.tipos_publicos()})
        if path == "/piezas":
            # piezas reales de un tipo PARA UN TEMA (los kits con arte estática varían por tema)
            q = urllib.parse.parse_qs(u.query)
            tipo = q.get("tipo", ["kit"])[0]
            tema = q.get("tema", ["safari"])[0]
            return self._json(200, {"ok": True, "piezas": productos.piezas_meta(tipo, tema)})
        if path == "/preview":
            q = urllib.parse.parse_qs(u.query)
            data = {c: (q.get(c, [""])[0] or "") for c in CAMPOS}
            if not data["nombre"]:
                data["nombre"] = "Tomás"
            tema = q.get("tema", ["safari"])[0]
            tipo = q.get("tipo", ["kit"])[0]
            # tamaño + formato configurables → miniaturas del catálogo livianas
            try: max_px = max(200, min(1200, int(q.get("max", ["900"])[0])))
            except Exception: max_px = 900
            fmt = (q.get("fmt", ["png"])[0] or "png").lower()
            ov = q.get("over", [""])[0]              # personalización del cliente (JSON)
            if ov:
                try: data["_over"] = json.loads(ov)
                except Exception: pass
            pieza = q.get("pieza", [""])[0]          # índice de pieza (galería: todas las del ZIP)
            img = None
            if pieza != "":
                try: img = productos.preview_pieza(data, tema, tipo, int(pieza), max_px=max_px)
                except Exception: img = None
            if img is None:
                img = productos.preview(data, tema=tema, tipo=tipo, max_px=max_px)
            img = piezas.marca_agua(img)   # marca de agua SOLO en el preview (el kit comprado sale limpio)
            buf = io.BytesIO()
            if fmt in ("jpg", "jpeg"):
                img.convert("RGB").save(buf, "JPEG", quality=80, optimize=True)
                ctype = "image/jpeg"
            else:
                img.save(buf, "PNG"); ctype = "image/png"
            body = buf.getvalue()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "public, max-age=86400")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
            return
        if path == "/mate/svg":
            q = urllib.parse.parse_qs(u.query)
            import mate_svg
            try: iconos = json.loads(q.get("iconos", [""])[0] or "[]") or None
            except Exception: iconos = None
            dmm = None   # el diámetro sale de la config del mate (admin); query opcional
            if q.get("diam_mm", [""])[0]:
                try: dmm = max(20.0, min(200.0, float(q.get("diam_mm")[0])))
                except Exception: dmm = None
            try: size = max(0.02, min(0.09, float(q.get("size", ["0.052"])[0])))
            except Exception: size = 0.052
            svg = mate_svg.export_svg(
                (q.get("texto", [""])[0] or "")[:40],
                mate_id=os.path.basename(q.get("mate", ["demo"])[0] or "demo"),
                font=q.get("font", ["Poppins-Medium.ttf"])[0], size_frac=size,
                r=q.get("r", [""])[0] or None,
                texto_abajo=(q.get("abajo", [""])[0] or "")[:40],
                abajo_flip=q.get("flip", ["0"])[0] in ("1", "true", "on"),
                iconos=iconos, diam_mm=dmm)
            body = svg.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
            self.send_header("Content-Disposition", 'attachment; filename="mate-grabado.svg"')
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
            return
        # ---- EDITOR DE MATES (grabado láser) ----
        if path == "/mate":
            html = open(os.path.join(generador.BASEDIR, "mate.html"), encoding="utf-8").read()
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
            return
        if path == "/mate/preview":
            q = urllib.parse.parse_qs(u.query)
            texto = (q.get("texto", [""])[0] or "")[:40]
            mate_id = os.path.basename(q.get("mate", ["demo"])[0] or "demo")
            font = q.get("font", ["Poppins-SemiBold.ttf"])[0]
            try: size = max(0.02, min(0.09, float(q.get("size", ["0.052"])[0])))
            except Exception: size = 0.052
            r = q.get("r", [""])[0] or None
            texto_abajo = (q.get("abajo", [""])[0] or "")[:40]
            abajo_flip = q.get("flip", ["0"])[0] in ("1", "true", "on")
            icono = os.path.basename(q.get("icono", [""])[0] or "")
            iconos = None
            try:
                iconos = json.loads(q.get("iconos", [""])[0] or "[]") or None
            except Exception:
                iconos = None
            try: mx = max(300, min(1100, int(q.get("max", ["900"])[0])))
            except Exception: mx = 900
            img = mate_mod.render(texto, mate_id, font=font, size_frac=size, r=r, max_px=mx,
                                  texto_abajo=texto_abajo, abajo_flip=abajo_flip, icono=icono, iconos=iconos)
            buf = io.BytesIO(); img.save(buf, "JPEG", quality=82, optimize=True); body = buf.getvalue()
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.send_header("Cache-Control", "public, max-age=600")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
            return
        # ---- editor del CLIENTE (público; se incrusta en la página del producto) ----
        if path == "/cliente":
            html = open(os.path.join(generador.BASEDIR, "cliente.html"), encoding="utf-8").read()
            body = html.encode("utf-8")          # sin token: es público (no edita tu config)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
            return
        if path == "/editor-simple":
            # editor liviano (campos + preview en vivo) para piezas código-generadas
            # (milestone, actividades). Público, no edita config.
            html = open(os.path.join(generador.BASEDIR, "editor_simple.html"), encoding="utf-8").read()
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
            return
        if path == "/cliente/layout":
            q = urllib.parse.parse_qs(u.query)
            pieza = q.get("pieza", ["invitacion"])[0]
            tema = q.get("tema", ["safari"])[0]
            return self._json(200, generador.layout_para_editor(pieza, tema))
        if path == "/cliente-bg.png":
            q = urllib.parse.parse_qs(u.query)
            pieza = q.get("pieza", ["invitacion"])[0]
            edad = q.get("edad", ["1"])[0]
            tema = q.get("tema", ["safari"])[0]
            bp = generador.bg_path_for(pieza, edad, tema)
            if not bp or not os.path.isfile(bp):
                return self._json(404, {"ok": False, "error": "fondo no encontrado"})
            im = Image.open(bp).convert("RGB")
            # El editor escala el canvas; no necesita el fondo a resolución real. Algunos
            # afiches pesan 45MB (5000px) y servirlos en PNG tardaba ~18s → el browser
            # cortaba (HTTP 000). Achicamos primero y servimos JPEG: <1s y unos cientos de KB.
            im.thumbnail((1400, 1400), Image.LANCZOS)
            im = piezas.marca_agua(im)                              # marca de agua (protege el asset)
            buf = io.BytesIO(); im.save(buf, "JPEG", quality=82, optimize=True); data = buf.getvalue()
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers(); self.wfile.write(data)
            return
        m = re.match(r"^/descarga/([A-Za-z0-9_-]+)$", path)
        if m:
            token = m.group(1)
            zip_path = os.path.join(DATA_DIR, token, "kit.zip")
            meta_path = os.path.join(DATA_DIR, token, "meta.json")
            if not os.path.isfile(zip_path):
                return self._json(404, {"ok": False, "error": "kit no encontrado"})
            nombre = "kit"
            if os.path.isfile(meta_path):
                try: nombre = slug(json.load(open(meta_path)).get("nombre") or "kit")
                except Exception: pass
            data = open(zip_path, "rb").read()
            self.send_response(200)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition", f'attachment; filename="kit-anito-salvaje-{nombre}.zip"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers(); self.wfile.write(data)
            return
        # ---- entrada desde el dashboard: valida el token, deja la cookie y
        #      redirige a /dash con la URL limpia (sin el ?key= en la barra) ----
        if path == "/entrar":
            if not self._admin_ok(u):
                return self._deny()
            self.send_response(302)
            self.send_header("Location", "/dash")
            self.send_header("Set-Cookie", self._cookie_header())
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        # ---- dashboard (alta de temáticas) ----
        if path == "/dash":
            if not self._admin_ok(u):
                return self._deny()
            html = open(os.path.join(generador.BASEDIR, "dash.html"), encoding="utf-8").read()
            body = html.replace("__API_KEY__", API_KEY).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Set-Cookie", self._cookie_header())
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
            return
        if path == "/dash/temas":
            if not self._admin_ok(u):
                return self._deny()
            pub = _pub_cfg()
            base = getattr(generador, "TEMA_DEFAULT", "safari")
            out = []
            for t in temas.list_temas():
                p = pub.get(t["id"]) or {}
                t = dict(t)
                t["publicado"] = bool(p.get("id"))
                t["product_id"] = p.get("id")
                t["edit"] = p.get("edit")
                t["base"] = (t["id"] == base)   # la base no se puede eliminar
                out.append(t)
            return self._json(200, {"temas": out})
        if path == "/dash/config":
            if not self._admin_ok(u):
                return self._deny()
            c = _woo_cfg()
            return self._json(200, {"url": c.get("url", ""),
                                    "configurado": bool(c.get("key") and c.get("secret"))})
        # ---- editor visual ----
        if path == "/editor":
            if not self._admin_ok(u):
                return self._deny()
            html = open(os.path.join(generador.BASEDIR, "editor.html"), encoding="utf-8").read()
            body = html.replace("__API_KEY__", API_KEY).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Set-Cookie", self._cookie_header())
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
            return
        if path == "/editor/layout":
            if not self._admin_ok(u):
                return self._deny()
            q = urllib.parse.parse_qs(u.query)
            pieza = q.get("pieza", ["invitacion"])[0]
            tema = q.get("tema", ["safari"])[0]
            return self._json(200, generador.layout_para_editor(pieza, tema))
        if path == "/editor-bg.png":
            if not self._admin_ok(u):
                return self._deny()
            q = urllib.parse.parse_qs(u.query)
            pieza = q.get("pieza", ["invitacion"])[0]
            edad = q.get("edad", ["1"])[0]
            tema = q.get("tema", ["safari"])[0]
            bp = generador.bg_path_for(pieza, edad, tema)
            if not bp or not os.path.isfile(bp):
                return self._json(404, {"ok": False, "error": "fondo no encontrado"})
            data = open(bp, "rb").read()
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers(); self.wfile.write(data)
            return
        mi = re.match(r"^/img/([A-Za-z0-9_.-]+\.(png|jpg|jpeg))$", path)
        if mi:
            ip = os.path.join(generador.OUT, mi.group(1))
            if os.path.isfile(ip):
                data = open(ip, "rb").read()
                self.send_response(200)
                self.send_header("Content-Type", "image/png" if ip.endswith("png") else "image/jpeg")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers(); self.wfile.write(data)
                return
            return self._json(404, {"ok": False, "error": "imagen no encontrada"})
        mf = re.match(r"^/fonts/([A-Za-z0-9_.-]+\.ttf)$", path)
        if mf:
            fp = os.path.join(generador.FONTS, mf.group(1))
            if os.path.isfile(fp):
                data = open(fp, "rb").read()
                self.send_response(200)
                self.send_header("Content-Type", "font/ttf")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers(); self.wfile.write(data)
                return
            return self._json(404, {"ok": False, "error": "fuente no encontrada"})
        return self._json(404, {"ok": False, "error": "ruta no encontrada"})

    # ---------------- POST ----------------
    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if not self._origin_ok():          # A5: rechaza POST cross-site de navegador
            return self._deny()
        if path == "/editor/save":
            return self._editor_save()
        if path == "/dash/upload":
            return self._dash_upload()
        if path == "/dash/crear":
            return self._dash_crear()
        if path == "/dash/config":
            return self._dash_config()
        if path == "/dash/despublicar":
            return self._dash_despublicar()
        if path == "/dash/eliminar-tema":
            return self._dash_eliminar_tema()
        if path == "/dash/publicar":
            return self._dash_publicar()
        if path != "/api/generar":
            return self._json(404, {"ok": False, "error": "ruta no encontrada"})
        if not secrets.compare_digest(self.headers.get("X-API-Key", "") or "", API_KEY):
            return self._json(401, {"ok": False, "error": "API key inválida"})
        raw = self._body()
        if raw is None:
            return self._json(413, {"ok": False, "error": "cuerpo demasiado grande"})
        try:
            payload = json.loads(raw)
        except Exception:
            return self._json(400, {"ok": False, "error": "JSON inválido"})

        data = {c: str(payload.get(c, "")).strip() for c in CAMPOS}
        if not data["nombre"]:
            return self._json(400, {"ok": False, "error": "falta 'nombre'"})
        if isinstance(payload.get("over"), dict):    # personalización del cliente (mini-editor)
            data["_over"] = payload["over"]
        tema = str(payload.get("tema", "safari")).strip() or "safari"
        tipo = str(payload.get("tipo", "kit")).strip() or "kit"
        if not productos.existe_tipo(tipo):
            return self._json(400, {"ok": False, "error": f"tipo desconocido: {tipo}"})
        order_id = slug(payload.get("order_id", "s"))
        token = f"{order_id}-{secrets.token_hex(16)}"   # A2: 128 bits, no brute-forceable
        dest = os.path.join(DATA_DIR, token)
        try:
            productos.generar(data, dest, tema, tipo)
            # A3: meta MÍNIMA (solo lo que usa /descarga para el nombre del archivo).
            # NO se persiste PII sensible (email, teléfono, dirección, fecha).
            with open(os.path.join(dest, "meta.json"), "w", encoding="utf-8") as f:
                json.dump({"order_id": payload.get("order_id"), "tema": tema, "tipo": tipo,
                           "nombre": data.get("nombre", "")}, f, ensure_ascii=False, indent=2)
            _limpiar_pedidos_viejos()      # A3: borra carpetas con PII de +30 días
        except Exception as e:
            return self._json(500, {"ok": False, "error": f"fallo al generar: {e}"})
        return self._json(200, {"ok": True, "token": token,
                                "download_url": f"{self.base_url()}/descarga/{token}"})

    def _editor_save(self):
        if not self._admin_ok():
            return self._deny()
        try:
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json(400, {"ok": False, "error": "JSON inválido"})
        clean = {}
        for k, v in (payload.get("fields") or {}).items():
            o = {}
            for kk in ("x", "y", "size", "maxw", "wght"):
                if kk in v:
                    try: o[kk] = round(float(v[kk]), 4)
                    except Exception: pass
            # también tipografía / color / alineación (lo que se ve en el editor)
            if isinstance(v.get("font"), str) and v["font"]:
                o["font"] = v["font"]
            if isinstance(v.get("color"), str) and v["color"].startswith("#"):
                o["color"] = v["color"]
            if isinstance(v.get("anchor"), str) and len(v["anchor"]) == 2:
                o["anchor"] = v["anchor"]
            if o:
                clean[k] = o
        pieza = payload.get("pieza", "invitacion")
        tema = payload.get("tema", "safari")
        p = generador.layout_file_path(pieza, tema)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(clean, f, ensure_ascii=False, indent=2)
        return self._json(200, {"ok": True, "guardado": len(clean), "pieza": pieza})

    # ---------------- Dashboard: alta de temáticas ----------------
    def _dash_upload(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        sslot = q.get("slot", [""])[0]
        if not re.match(r"^(invitacion|afiche)_[123]$|^animal_[1-9]$|^numero_[123]$", sslot):
            return self._json(400, {"ok": False, "error": "slot inválido"})
        if not tema:
            return self._json(400, {"ok": False, "error": "falta tema"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(n)
            im = Image.open(io.BytesIO(raw)).convert("RGBA")
            tdir = os.path.join(temas.TEMAS_DIR, tema)
            if sslot.startswith("invitacion") or sslot.startswith("afiche"):
                os.makedirs(tdir, exist_ok=True)
                im.save(os.path.join(tdir, sslot + ".png"))
            else:   # animalitos / números: van a recortes/, recortándoles el fondo
                rdir = os.path.join(tdir, "recortes")
                os.makedirs(rdir, exist_ok=True)
                if quitar_fondo.ya_transparente(im):
                    bb = im.getbbox(); proc = im.crop(bb) if bb else im
                elif sslot.startswith("numero"):
                    proc = quitar_fondo.remove_checker(im)
                else:
                    proc = quitar_fondo.remove_bg(im, protect=True)
                    bb = proc.getbbox()
                    if bb: proc = proc.crop(bb)
                proc.save(os.path.join(rdir, sslot + ".png"))
        except Exception as e:
            return self._json(500, {"ok": False, "error": "upload falló: %s" % e})
        return self._json(200, {"ok": True, "slot": sslot, "tema": tema, "size": list(im.size)})

    def _dash_crear(self):
        if not self._admin_ok():
            return self._deny()
        try:
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json(400, {"ok": False, "error": "JSON inválido"})
        nombre = (payload.get("nombre") or "").strip()
        tema = slug(payload.get("id") or nombre)
        if not tema:
            return self._json(400, {"ok": False, "error": "falta nombre"})
        tdir = os.path.join(temas.TEMAS_DIR, tema)
        req = ["invitacion_1", "invitacion_2", "invitacion_3", "afiche_1", "afiche_2", "afiche_3"]
        faltan = [s for s in req if not os.path.isfile(os.path.join(tdir, s + ".png"))]
        if faltan:
            return self._json(400, {"ok": False, "error": "faltan imágenes: " + ", ".join(faltan)})
        base = json.load(open(os.path.join(temas.TEMAS_DIR, "safari", "tema.json"), encoding="utf-8"))
        base["id"] = tema
        base["nombre"] = nombre or tema
        try:    # ajustar la resolución de salida del afiche a la imagen subida
            aw = Image.open(os.path.join(tdir, "afiche_1.png")).size[0]
            dw = base["piezas"]["afiche"]["size"][0]
            base["piezas"]["afiche"]["render_scale"] = round(aw / dw, 3)
        except Exception:
            pass
        os.makedirs(os.path.join(tdir, "layouts"), exist_ok=True)
        with open(os.path.join(tdir, "tema.json"), "w", encoding="utf-8") as f:
            json.dump(base, f, ensure_ascii=False, indent=2)
        generador._specs_cache.pop(tema, None)   # por si estaba cacheada
        return self._json(200, {"ok": True, "tema": tema, "nombre": base["nombre"]})

    def _dash_config(self):
        if not self._admin_ok():
            return self._deny()
        try:
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json(400, {"ok": False, "error": "JSON inválido"})
        cfg = _woo_cfg()
        for k in ("url", "key", "secret"):
            if payload.get(k):
                cfg[k] = str(payload[k]).strip()
        _woo_save(cfg)
        return self._json(200, {"ok": True, "configurado": bool(cfg.get("key") and cfg.get("secret"))})

    def _dash_publicar(self):
        if not self._admin_ok():
            return self._deny()
        try:
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json(400, {"ok": False, "error": "JSON inválido"})
        tema = slug(payload.get("tema", ""))
        if not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "la temática no existe"})
        nombre = (payload.get("nombre") or "").strip() or ("Kit " + tema)
        precio = str(payload.get("precio", "")).strip()
        pub = _pub_cfg()
        ex = pub.get(tema) or {}
        try:
            if ex.get("id"):
                # ── REPUBLICAR: actualizar el producto existente (no duplica) ──
                upd = {"name": nombre}
                if precio:
                    upd["regular_price"] = precio   # vacío = no toca el precio actual
                try:
                    r = _wc_call("PUT", "products/%s" % ex["id"], upd)
                    accion = "republicado"
                except urllib.error.HTTPError as e:
                    if e.code != 404:
                        raise
                    ex = {}   # el producto ya no existe en Woo → lo recreamos abajo
            if not ex.get("id"):
                # ── PUBLICAR por primera vez: crear como borrador ──
                prod = {
                    "name": nombre, "type": "simple", "virtual": True, "status": "draft",
                    "regular_price": precio or "0",
                    "meta_data": [{"key": "_ct3d_kit", "value": "yes"},
                                  {"key": "_ct3d_tema", "value": tema}],
                }
                r = _wc_crear_producto(prod)
                accion = "publicado"
        except urllib.error.HTTPError as e:
            return self._json(502, {"ok": False, "error": "Woo respondió %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:200])})
        except Exception as e:
            return self._json(502, {"ok": False, "error": str(e)})
        pub[tema] = {"id": r.get("id"), "permalink": r.get("permalink"), "edit": _edit_url(r.get("id"))}
        _pub_save(pub)
        return self._json(200, {"ok": True, "accion": accion, "product_id": r.get("id"),
                                "permalink": r.get("permalink"), "edit": pub[tema]["edit"]})

    def _dash_despublicar(self):
        if not self._admin_ok():
            return self._deny()
        try:
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json(400, {"ok": False, "error": "JSON inválido"})
        tema = slug(payload.get("tema", ""))
        pub = _pub_cfg()
        ex = pub.get(tema) or {}
        if not ex.get("id"):
            return self._json(200, {"ok": True, "nota": "no estaba publicado"})
        try:
            _wc_call("DELETE", "products/%s?force=true" % ex["id"])
        except urllib.error.HTTPError as e:
            if e.code != 404:   # 404 = ya no existía; igual limpiamos el registro
                return self._json(502, {"ok": False, "error": "Woo respondió %s" % e.code})
        except Exception as e:
            return self._json(502, {"ok": False, "error": str(e)})
        pub.pop(tema, None)
        _pub_save(pub)
        return self._json(200, {"ok": True})

    def _dash_eliminar_tema(self):
        """Borra la temática por completo: imágenes + config del panel, y si estaba
        publicada también baja el producto de la tienda. La base no se toca."""
        if not self._admin_ok():
            return self._deny()
        try:
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json(400, {"ok": False, "error": "JSON inválido"})
        tema = slug(payload.get("tema", ""))
        base = getattr(generador, "TEMA_DEFAULT", "safari")
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "la temática no existe"})
        if tema == base:
            return self._json(400, {"ok": False, "error": "no se puede eliminar la temática base"})
        warn = ""
        # 1) bajar de la tienda si estaba publicada (no fatal si Woo falla)
        pub = _pub_cfg()
        ex = pub.get(tema) or {}
        if ex.get("id"):
            try:
                _wc_call("DELETE", "products/%s?force=true" % ex["id"])
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    warn = "el producto quedó en la tienda (borralo a mano)"
            except Exception:
                warn = "no se pudo contactar la tienda; borrá el producto a mano"
            pub.pop(tema, None)
            _pub_save(pub)
        # 2) borrar la carpeta del tema (ruta validada: slug + existe + dentro de TEMAS_DIR)
        import shutil
        tdir = os.path.realpath(os.path.join(temas.TEMAS_DIR, tema))
        if not tdir.startswith(os.path.realpath(temas.TEMAS_DIR) + os.sep):
            return self._json(400, {"ok": False, "error": "ruta inválida"})
        try:
            shutil.rmtree(tdir)
        except Exception as e:
            return self._json(500, {"ok": False, "error": "no se pudo borrar: %s" % e})
        generador._specs_cache.pop(tema, None)
        return self._json(200, {"ok": True, "warn": warn})

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Servicio kit en puerto {PORT}  | data: {DATA_DIR}  | API key: {'(default)' if API_KEY=='cambiame-ya' else 'set'}")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
