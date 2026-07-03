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
from ia_kit import jobs as ia_jobs, orquestador as ia_orq, aprobar as ia_aprobar, upscale as ia_upscale
from ia_kit.client import OpenAIImageClient
from PIL import Image

API_KEY  = os.environ.get("CT3D_API_KEY", "cambiame-ya")
PORT     = int(os.environ.get("CT3D_PORT", "8787"))
DATA_DIR = os.environ.get("CT3D_DATA_DIR", os.path.join(os.path.dirname(__file__), "pedidos"))
BASE_URL = os.environ.get("CT3D_BASE_URL", f"http://localhost:{PORT}")
OPENAI_API_KEY     = os.environ.get("OPENAI_API_KEY", "")
OPENAI_IMAGE_MODEL = os.environ.get("OPENAI_IMAGE_MODEL", "gpt-image-2")
OPENAI_CALIDAD     = os.environ.get("OPENAI_CALIDAD", "low")  # low p/ depurar barato; medium/high p/ final


def _calidad(q):
    """Calidad de generación: ?calidad=low|medium|high, default OPENAI_CALIDAD."""
    c = (q.get("calidad", [""])[0] or "").lower()
    return c if c in ("low", "medium", "high") else OPENAI_CALIDAD
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

# ---- gestión de productos en la tienda Flask (reemplaza WooCommerce) ----
# El catálogo vive en la tienda (facturas_ml.db); el panel del kit publica vía los
# endpoints /kit-admin/* de facturas_api (localhost:8091), autenticando con la
# CT3D_API_KEY del propio kit (que facturas_api valida con _kit_admin_key).
TIENDA_API = os.environ.get("TIENDA_API_URL", "http://127.0.0.1:8091")
def _tienda_admin(method, path, body=None):
    """Llama a /kit-admin/* de la tienda. Devuelve (status_code, dict)."""
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"X-API-Key": API_KEY}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(TIENDA_API + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8") or "{}")
        except Exception:
            return e.code, {"ok": False, "error": "la tienda respondió HTTP %s" % e.code}
    except Exception as e:
        return 0, {"ok": False, "error": "no se pudo contactar la tienda: %s" % e}

def _openai_client():
    if not OPENAI_API_KEY:
        return None
    return OpenAIImageClient(OPENAI_API_KEY, model=OPENAI_IMAGE_MODEL)

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
MAX_BODY = 30 * 1024 * 1024       # 30 MB: tope de cuerpo POST (las piezas/arte a resolución
                                  # de impresión pesan ~15-20MB; subir admin-only). (A7)
_SEM = threading.Semaphore(16)    # máx 16 requests concurrentes (A7, anti thread-exhaustion)
# Generar thumbs decodifica PNGs de ~140MB en RAM; se limitan a 3 a la vez para no
# reventar memoria cuando el modal pide 40 miniaturas de golpe.
_THUMB_SEM = threading.Semaphore(3)
# Libro premium: ilustra 10 páginas con OpenAI por pedido (~10 min). De a UNO para
# no quemar rate-limit ni acumular gasto si entran varias compras juntas; los demás
# pedidos esperan su turno dentro del hilo de fondo (el cliente ya tiene su link).
_LIBRO_PREMIUM_SEM = threading.Semaphore(1)
_KEY_RE = re.compile(r"(key=)[^&\s\"']+", re.I)

def _pieza_thumb(exdir, archivo):
    """Devuelve el path del thumbnail (≤220px) de extras/<archivo>, generándolo en
    extras/.thumbs si falta o si la pieza cambió (por mtime). None si no se pudo."""
    src = os.path.join(exdir, archivo)
    if not os.path.isfile(src):
        return None
    tdir = os.path.join(exdir, ".thumbs")
    thumb = os.path.join(tdir, archivo)
    try:
        if os.path.isfile(thumb) and os.path.getmtime(thumb) >= os.path.getmtime(src):
            return thumb
        with _THUMB_SEM:
            os.makedirs(tdir, exist_ok=True)
            im = Image.open(src).convert("RGBA")
            im.thumbnail((220, 220), Image.LANCZOS)
            im.save(thumb)
        return thumb
    except Exception:
        return None

def _sync_edades(tema):
    """Ajusta tema.json['edades'] a las edades (1-7) que realmente tienen invitación
    cargada. Así el editor en vivo y la tienda ofrecen una edad solo cuando hay arte."""
    tdir = os.path.join(temas.TEMAS_DIR, tema)
    edades = [n for n in range(1, 8) if os.path.isfile(os.path.join(tdir, f"invitacion_{n}.png"))]
    if not edades:
        return
    cfg_path = os.path.join(tdir, "tema.json")
    try:
        cfg = json.load(open(cfg_path, encoding="utf-8")) if os.path.isfile(cfg_path) else {}
        if cfg.get("edades") != edades:
            cfg["edades"] = edades
            json.dump(cfg, open(cfg_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    except Exception:
        pass

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

def _rate_ok(ip, limit=120, window=60):
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
        # El admin (panel) queda EXENTO: carga muchas miniaturas (editor-bg.png) de una
        # sola vez al listar temáticas y no debe autobloquearse.
        if path.startswith(("/preview", "/mate/preview", "/cliente-bg.png",
                            "/editor-bg.png", "/descarga/", "/piezas")) \
                and not self._admin_ok(u) and not _rate_ok(self._client_ip()):
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
            # campos EXTRA propios de un tipo (ej. menu_entrada/menu_plato del menú
            # infantil): cualquier query param que no sea de control se suma tal cual,
            # así un tipo nuevo con campos propios no necesita tocar este endpoint.
            for k, vals in q.items():
                if k not in CAMPOS and k not in ("tema", "tipo", "max", "fmt", "over", "pieza", "cb"):
                    data[k] = vals[0] if vals else ""
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
        # ---- invitación web interactiva (pública: el link SE COMPARTE por WhatsApp) ----
        m = re.match(r"^/i/([A-Za-z0-9_-]+)(/hero\.png)?$", path)
        if m:
            import invitacion_web as iw
            token, es_hero = m.group(1), bool(m.group(2))
            if es_hero:
                png = iw.hero_png(token)
                if png is None:
                    return self._json(404, {"ok": False, "error": "no existe"})
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Cache-Control", "public, max-age=86400")
                self.send_header("Content-Length", str(len(png)))
                self.end_headers()
                self.wfile.write(png)
                return
            page = iw.html(token, base_url=self.base_url())
            if page is None:
                return self._json(404, {"ok": False, "error": "invitación no encontrada o vencida"})
            body = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        m = re.match(r"^/descarga/([A-Za-z0-9_-]+)$", path)
        if m:
            token = m.group(1)
            zip_path = os.path.join(DATA_DIR, token, "kit.zip")
            meta_path = os.path.join(DATA_DIR, token, "meta.json")
            if not os.path.isfile(zip_path):
                flag_path = os.path.join(DATA_DIR, token, "generando.flag")
                if os.path.isfile(flag_path):
                    # Generación en curso: página amigable que se recarga sola.
                    try:
                        que = open(flag_path).read().strip()
                    except OSError:
                        que = ""
                    if que == "fiesta-completa":
                        icono, titulo, detalle = "🎉", "Tu Fiesta Completa se está preparando", \
                            "Estamos armando el kit, el libro, las piezas 3D y tu invitación web. Suele tardar 1-2 minutos."
                    else:
                        icono, titulo, detalle = "🎨", "Tu libro se está ilustrando", \
                            "Cada página se pinta especialmente para este pedido. Suele tardar unos 10 minutos."
                    body = ("<!doctype html><html lang='es'><head><meta charset='utf-8'>"
                            "<meta http-equiv='refresh' content='45'>"
                            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
                            "<title>" + titulo + "…</title></head>"
                            "<body style='font-family:sans-serif;background:#FDF7EE;display:flex;"
                            "align-items:center;justify-content:center;min-height:100vh;margin:0'>"
                            "<div style='text-align:center;max-width:420px;padding:24px'>"
                            "<div style='font-size:56px'>" + icono + "</div>"
                            "<h1 style='color:#6B5BD2;font-size:24px'>" + titulo + "</h1>"
                            "<p style='color:#555;line-height:1.5'>" + detalle + "<br>Esta página se "
                            "actualiza sola — no hace falta que hagas nada.</p>"
                            "</div></body></html>").encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Cache-Control", "no-store")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return
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
        if path == "/dash/piezas-estado":
            if not self._admin_ok(u):
                return self._deny()
            return self._dash_piezas_estado(urllib.parse.parse_qs(u.query))
        if path == "/dash/pub-estado":
            return self._dash_pub_estado(urllib.parse.parse_qs(u.query))
        if path == "/dash/pieza-img":
            return self._dash_pieza_img(urllib.parse.parse_qs(u.query))
        if path == "/dash/base-estado":
            return self._dash_base_estado(urllib.parse.parse_qs(u.query))
        if path == "/dash/producto-piezas":
            return self._dash_producto_piezas(urllib.parse.parse_qs(u.query))
        if path == "/dash/producto-descargar":
            return self._dash_producto_descargar(urllib.parse.parse_qs(u.query))
        if path == "/dash/producto-zip":
            return self._dash_producto_zip(urllib.parse.parse_qs(u.query))
        if path == "/dash/ia-draft":
            return self._ia_draft(urllib.parse.parse_qs(u.query))
        if path == "/dash/ia-estado":
            return self._ia_estado()
        if path == "/dash/ia-listado":
            return self._ia_listado(urllib.parse.parse_qs(u.query))
        if path == "/dash/base-img":
            return self._dash_base_img(urllib.parse.parse_qs(u.query))
        if path == "/dash/arte-descargar":
            return self._dash_arte_descargar(urllib.parse.parse_qs(u.query))
        if path == "/dash/arte-zip":
            return self._dash_arte_zip(urllib.parse.parse_qs(u.query))
        if path == "/dash/cuaderno-estado":
            return self._dash_cuaderno_estado(urllib.parse.parse_qs(u.query))
        if path == "/dash/cuaderno-img":
            return self._dash_cuaderno_img(urllib.parse.parse_qs(u.query))
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
        if path == "/dash/upload-pieza":
            return self._dash_upload_pieza()
        if path == "/dash/ia-generar":
            return self._ia_generar()
        if path == "/dash/ia-regenerar":
            return self._ia_regenerar()
        if path == "/dash/agregar-edades":
            return self._dash_agregar_edades()
        if path == "/dash/ia-colorear-variantes":
            return self._ia_colorear_variantes()
        if path == "/dash/producto-upload":
            return self._dash_producto_upload()
        if path == "/dash/libro-ia":
            return self._dash_libro_ia()
        if path == "/dash/producto-borrar-override":
            return self._dash_producto_borrar_override()
        if path == "/dash/calendario-generar":
            return self._dash_calendario_generar()
        if path == "/dash/ia-replicar":
            return self._ia_replicar()
        if path == "/dash/ia-aprobar":
            return self._ia_aprobar()
        if path == "/dash/borrar-pieza":
            return self._dash_borrar_pieza()
        if path == "/dash/borrar-base":
            return self._dash_borrar_base()
        if path == "/dash/cuaderno-upload":
            return self._dash_cuaderno_upload()
        if path == "/dash/cuaderno-borrar":
            return self._dash_cuaderno_borrar()
        if path == "/dash/cuaderno-regenerar":
            return self._dash_cuaderno_regenerar()
        if path == "/dash/cuaderno-regenerar-pagina":
            return self._dash_cuaderno_regenerar_pagina()
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
        # campos EXTRA propios de un tipo (ej. menu_entrada/menu_plato del menú infantil):
        # ver mismo criterio en /preview.
        for k, v in payload.items():
            if k not in CAMPOS and k not in ("tema", "tipo", "order_id", "over"):
                data[k] = str(v).strip()
        tipo_pre = str(payload.get("tipo", "kit")).strip() or "kit"
        # 'nombre' solo es obligatorio si el tipo lo usa (ej. el cortante 3D no lleva
        # personalización: campos=[]).
        if not data["nombre"] and (not productos.existe_tipo(tipo_pre)
                                   or "nombre" in productos.campos_tipo(tipo_pre)):
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
        if tipo == "invitacion-web":
            # El producto ES un link (página viva), no un archivo: se crea el evento
            # y se devuelve su URL como download_url (la tienda ya sabe mostrar eso).
            import invitacion_web as iw
            tok = iw.crear(data, tema)
            # Tema sin hero IA todavía (tema nuevo): generarlo en background — la
            # primera vista usa el procedural y las siguientes ya ven el arte bueno.
            if not os.path.isfile(iw._hero_ia_path(tema)):
                client = _openai_client()
                if client is not None:
                    def _hero_worker(tema=tema):
                        try:
                            iw.generar_hero_ia(client, tema)
                        except Exception as e:
                            print("[invitacion-web] hero IA falló (%s) — queda el procedural" % e,
                                  flush=True)
                    threading.Thread(target=_hero_worker, daemon=True).start()
            return self._json(200, {"ok": True, "token": tok,
                                    "download_url": f"{self.base_url()}/i/{tok}"})
        if tipo == "fiesta-completa":
            # Bundle: genera 3 productos + STLs (~1 min) — async con página de espera.
            os.makedirs(dest, exist_ok=True)
            with open(os.path.join(dest, "generando.flag"), "w") as f:
                f.write("fiesta-completa")
            with open(os.path.join(dest, "meta.json"), "w", encoding="utf-8") as f:
                json.dump({"order_id": payload.get("order_id"), "tema": tema, "tipo": tipo,
                           "nombre": data.get("nombre", "")}, f, ensure_ascii=False, indent=2)
            data["_base_url"] = self.base_url()

            def _bundle_worker(data=data, dest=dest, tema=tema):
                try:
                    productos.generar(data, dest, tema, "fiesta-completa")
                except Exception as e:
                    print("[fiesta-completa] generación falló: %s" % e, flush=True)
                finally:
                    try:
                        os.remove(os.path.join(dest, "generando.flag"))
                    except OSError:
                        pass

            threading.Thread(target=_bundle_worker, daemon=True).start()
            return self._json(200, {"ok": True, "token": token, "generando": True,
                                    "download_url": f"{self.base_url()}/descarga/{token}"})
        if tipo == "libro-premium":
            # Ilustrar 10 páginas tarda ~10 min: la HTTP no puede esperar. Se devuelve
            # el link YA y un hilo genera; /descarga muestra "ilustrándose…" (flag)
            # hasta que kit.zip existe. Si la IA falla, el libro sale igual con el
            # arte standard del tema (el cliente SIEMPRE recibe su libro).
            client = _openai_client()
            if client is None:
                return self._json(503, {"ok": False, "error": "libro premium no disponible (falta OPENAI_API_KEY)"})
            os.makedirs(dest, exist_ok=True)
            with open(os.path.join(dest, "generando.flag"), "w") as f:
                f.write("libro-premium")
            with open(os.path.join(dest, "meta.json"), "w", encoding="utf-8") as f:
                json.dump({"order_id": payload.get("order_id"), "tema": tema, "tipo": tipo,
                           "nombre": data.get("nombre", "")}, f, ensure_ascii=False, indent=2)

            def _premium_worker(data=data, dest=dest, tema=tema):
                import libro, libro_ia
                escenas = os.path.join(dest, "escenas")
                with _LIBRO_PREMIUM_SEM:
                    try:
                        libro_ia.generar_ilustraciones(client, tema, dest_dir=escenas,
                                                       genero=data.get("genero"))
                    except Exception as e:
                        # El cliente recibe el libro IGUAL (arte standard) — pero esto
                        # es un pedido premium: dejar rastro para regenerar/compensar.
                        print("[libro-premium] IA falló (%s) — sale con arte standard" % e,
                              flush=True)
                        try:
                            with open(os.path.join(dest, "ia_fallo.txt"), "w") as ff:
                                ff.write(str(e))
                        except OSError:
                            pass
                    try:
                        with libro.usar_escenas_dir(escenas):
                            productos.generar(data, dest, tema, "libro")
                    except Exception as e:
                        print("[libro-premium] render falló: %s" % e, flush=True)
                    finally:
                        try:
                            os.remove(os.path.join(dest, "generando.flag"))
                        except OSError:
                            pass

            threading.Thread(target=_premium_worker, daemon=True).start()
            return self._json(200, {"ok": True, "token": token, "generando": True,
                                    "download_url": f"{self.base_url()}/descarga/{token}"})
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
        if not re.match(r"^(invitacion|afiche)_[1-7]$|^animal_[1-9]$|^numero_[1-7]$", sslot):
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
                generador._specs_cache.pop(tema, None)
                _pieza_thumb(tdir, sslot + ".png")   # thumb listo para el modal de arte base
                if sslot.startswith("invitacion"):
                    _sync_edades(tema)               # nueva edad con invitación → la tienda la ofrece
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

    # ---- Kit nuevo (extras/<pieza>_<edad>.png): subir cada pieza por edad, self-service ----
    _PIEZAS_EDAD = ["afiche", "topper", "stickers", "separadores", "etiqueta_botella",
                    "cajita_sorpresa", "decoracion_sorbetes"]
    _PIEZAS_UNIV = ["banderin", "etiquetas_multiuso", "wrappers_cupcakes", "tarjetas_agradecimiento"]

    def _dash_upload_pieza(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        pieza = re.sub(r"[^a-z0-9_]", "", (q.get("pieza", [""])[0] or "").lower())[:30]
        edad = re.sub(r"\D", "", q.get("edad", [""])[0] or "")[:2]   # vacío = pieza universal
        if not tema or not pieza:
            return self._json(400, {"ok": False, "error": "falta tema o pieza"})
        raw = self._body()
        if raw is None:
            return self._json(413, {"ok": False, "error": "imagen demasiado grande"})
        try:
            im = Image.open(io.BytesIO(raw)).convert("RGBA")
            exdir = os.path.join(temas.TEMAS_DIR, tema, "extras")
            os.makedirs(exdir, exist_ok=True)
            name = f"{pieza}_{edad}.png" if edad else f"{pieza}.png"
            im.save(os.path.join(exdir, name))
            generador._specs_cache.pop(tema, None)
            _pieza_thumb(exdir, name)   # deja el thumb listo para el modal
        except Exception as e:
            return self._json(500, {"ok": False, "error": "upload falló: %s" % e})
        return self._json(200, {"ok": True, "pieza": pieza, "edad": edad, "archivo": name,
                                "size": list(im.size)})

    def _dash_piezas_estado(self, q):
        tema = slug(q.get("tema", [""])[0])
        exdir = os.path.join(temas.TEMAS_DIR, tema, "extras")
        archivos = [f for f in (sorted(os.listdir(exdir)) if os.path.isdir(exdir) else [])
                    if f.lower().endswith(".png")]
        return self._json(200, {"ok": True, "tema": tema, "piezas_edad": self._PIEZAS_EDAD,
                                "piezas_univ": self._PIEZAS_UNIV, "archivos": archivos})

    def _dash_pieza_img(self, q):
        """Sirve una MINIATURA (≤220px) de la pieza cargada para el modal. Las piezas
        reales pesan decenas de MB; se cachea el thumb en extras/.thumbs (regenerado si
        la pieza cambió, por mtime). Así abrir el modal con 40 piezas es liviano."""
        if not self._admin_ok():
            return self._deny()
        tema = slug((q.get("tema", [""]) or [""])[0])
        archivo = re.sub(r"[^a-z0-9_.]", "", ((q.get("archivo", [""]) or [""])[0] or "").lower())
        if not archivo.endswith(".png") or "/" in archivo or ".." in archivo:
            return self._json(400, {"ok": False, "error": "archivo inválido"})
        exdir = os.path.join(temas.TEMAS_DIR, tema, "extras")
        if not os.path.isfile(os.path.join(exdir, archivo)):
            return self._json(404, {"ok": False, "error": "no existe"})
        thumb = _pieza_thumb(exdir, archivo)
        if not thumb:
            return self._json(500, {"ok": False, "error": "no se pudo generar la miniatura"})
        data = open(thumb, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def _dash_borrar_pieza(self):
        """Borra una pieza cargada (extras/<pieza>_<edad>.png). Para reemplazarla,
        el cliente borra y vuelve a subir; subir directamente también la pisa."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        pieza = re.sub(r"[^a-z0-9_]", "", (q.get("pieza", [""])[0] or "").lower())[:30]
        edad = re.sub(r"\D", "", q.get("edad", [""])[0] or "")[:2]
        if not tema or not pieza:
            return self._json(400, {"ok": False, "error": "falta tema o pieza"})
        name = f"{pieza}_{edad}.png" if edad else f"{pieza}.png"
        exdir = os.path.join(temas.TEMAS_DIR, tema, "extras")
        path = os.path.join(exdir, name)
        try:
            if os.path.isfile(path):
                os.remove(path); generador._specs_cache.pop(tema, None)
                thumb = os.path.join(exdir, ".thumbs", name)
                if os.path.isfile(thumb):
                    os.remove(thumb)
                return self._json(200, {"ok": True, "archivo": name})
            return self._json(404, {"ok": False, "error": "no existía"})
        except Exception as e:
            return self._json(500, {"ok": False, "error": str(e)})

    # ---- Piezas de los productos 100% procedurales (certificado/corona/calendario/…) ----
    # No tienen ia_draft/extras (no los dibuja OpenAI): se calculan al vuelo con Pillow.
    # "Override" = una imagen subida a mano que reemplaza el diseño procedural de UNA pieza
    # puntual (ej. si Pablo la mejora con otra IA y quiere usar esa versión).
    def _dash_producto_piezas(self, q):
        """Lista las piezas reales de un tipo/tema con su label y si tienen override."""
        if not self._admin_ok():
            return self._deny()
        tema = slug((q.get("tema", [""]) or [""])[0])
        tipo = re.sub(r"[^a-z0-9_]", "", ((q.get("tipo", [""]) or [""])[0] or "").lower())[:30]
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        try:
            meta = productos.piezas_meta(tipo, tema)
        except Exception as e:
            return self._json(400, {"ok": False, "error": str(e)})
        for p in meta:
            p["override"] = os.path.isfile(productos.override_path(tema, tipo, p["idx"]))
        return self._json(200, {"ok": True, "piezas": meta})

    def _dash_producto_descargar(self, q):
        """Descarga UNA pieza a resolución completa, SIN marca de agua (admin)."""
        if not self._admin_ok():
            return self._deny()
        tema = slug((q.get("tema", [""]) or [""])[0])
        tipo = re.sub(r"[^a-z0-9_]", "", ((q.get("tipo", [""]) or [""])[0] or "").lower())[:30]
        try:
            idx = int((q.get("pieza", ["0"]) or ["0"])[0])
        except ValueError:
            return self._json(400, {"ok": False, "error": "pieza inválida"})
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        try:
            items = productos.piezas_tipo(tema, tipo)
            nombre, fn, _ = items[idx]
        except Exception:
            return self._json(404, {"ok": False, "error": "pieza no encontrada"})
        muestra = {"nombre": "Tomás", "edad": "5", "anyo": "2026"}
        img = piezas.to_rgb(fn(muestra))
        buf = io.BytesIO(); img.save(buf, "PNG"); data = buf.getvalue()
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Disposition", 'attachment; filename="%s-%s-%s.png"' % (tipo, tema, nombre))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def _dash_producto_zip(self, q):
        """ZIP con TODAS las piezas de un tipo/tema a resolución completa, sin marca de agua."""
        if not self._admin_ok():
            return self._deny()
        import zipfile
        tema = slug((q.get("tema", [""]) or [""])[0])
        tipo = re.sub(r"[^a-z0-9_]", "", ((q.get("tipo", [""]) or [""])[0] or "").lower())[:30]
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        try:
            items = productos.piezas_tipo(tema, tipo)
        except Exception as e:
            return self._json(400, {"ok": False, "error": str(e)})
        muestra = {"nombre": "Tomás", "edad": "5", "anyo": "2026"}
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for nombre, fn, _ in items:
                img = piezas.to_rgb(fn(muestra))
                pbuf = io.BytesIO(); img.save(pbuf, "PNG")
                z.writestr("%s-%s-%s.png" % (tipo, tema, nombre), pbuf.getvalue())
        data = buf.getvalue()
        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition", 'attachment; filename="%s-%s.zip"' % (tipo, tema))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def _dash_producto_upload(self):
        """Sube un reemplazo (override) para UNA pieza puntual — ej. la misma pieza
        mejorada con otra IA. No toca el diseño procedural; solo lo tapa para ese tema."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        tipo = re.sub(r"[^a-z0-9_]", "", (q.get("tipo", [""])[0] or "").lower())[:30]
        try:
            idx = int(q.get("pieza", ["0"])[0])
        except ValueError:
            return self._json(400, {"ok": False, "error": "pieza inválida"})
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(n) if n else b""
            if not raw:
                return self._json(400, {"ok": False, "error": "sin archivo"})
            im = Image.open(io.BytesIO(raw)).convert("RGBA")
        except Exception as e:
            return self._json(400, {"ok": False, "error": "imagen inválida: %s" % e})
        dest = productos.override_path(tema, tipo, idx)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        im.save(dest)
        return self._json(200, {"ok": True})

    def _dash_producto_borrar_override(self):
        """Saca el reemplazo subido a mano: la pieza vuelve a su diseño procedural."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        tipo = re.sub(r"[^a-z0-9_]", "", (q.get("tipo", [""])[0] or "").lower())[:30]
        try:
            idx = int(q.get("pieza", ["0"])[0])
        except ValueError:
            return self._json(400, {"ok": False, "error": "pieza inválida"})
        dest = productos.override_path(tema, tipo, idx)
        if os.path.isfile(dest):
            os.remove(dest)
            return self._json(200, {"ok": True, "borrado": True})
        return self._json(200, {"ok": True, "borrado": False})

    def _dash_calendario_generar(self):
        """Sube UNA imagen de plantilla y genera automáticamente los 12 meses del calendario
        superponiendo mes/días/números (posición, tamaño y grosor definidos en el editor visual
        del dashboard) sobre esa imagen. Cada mes se guarda como override del tipo 'calendario'."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        anyo_str = re.sub(r"\D", "", (q.get("anyo", ["2026"])[0] or "2026"))[:4]
        nombre = (q.get("nombre", [""])[0] or "").strip() or "Mi familia"
        config_str = q.get("config", [""])[0] or ""
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        try:
            config = json.loads(config_str) if config_str else None
        except Exception:
            config = None
        try:
            n = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(n) if n else b""
            if not raw:
                return self._json(400, {"ok": False, "error": "sin archivo"})
            plantilla = Image.open(io.BytesIO(raw)).convert("RGBA")
        except Exception as e:
            return self._json(400, {"ok": False, "error": "imagen inválida: %s" % e})

        try:
            import calendario
            piezas_meses = calendario.generar_calendario_con_plantilla(
                {"nombre": nombre, "anyo": anyo_str}, plantilla, tema, config=config)
            tdir = os.path.join(temas.TEMAS_DIR, tema)
            fondo_dir = os.path.join(tdir, "calendario")
            os.makedirs(fondo_dir, exist_ok=True)
            plantilla.save(os.path.join(fondo_dir, "fondo.png"))

            override_dir = os.path.join(tdir, "overrides", "calendario")
            os.makedirs(override_dir, exist_ok=True)
            generados = []
            for idx, (archivo, maker, _) in enumerate(piezas_meses):
                img = maker({"nombre": nombre})
                p = os.path.join(override_dir, "%d.png" % idx)
                piezas.to_rgb(img).save(p)
                generados.append({"idx": idx, "archivo": archivo})
            return self._json(200, {"ok": True, "tema": tema, "anyo": anyo_str,
                                    "generados": len(generados), "meses": generados})
        except Exception as e:
            return self._json(500, {"ok": False, "error": "generación falló: %s" % e})

    # ---- Arte BASE de una temática existente (invitacion_N / afiche_N en la raíz) ----
    def _dash_base_estado(self, q):
        """Qué invitaciones/afiches base (edad 1-5) tiene cargados la temática."""
        if not self._admin_ok():
            return self._deny()
        tema = slug((q.get("tema", [""]) or [""])[0])
        tdir = os.path.join(temas.TEMAS_DIR, tema)
        files = set(os.listdir(tdir)) if os.path.isdir(tdir) else set()
        return self._json(200, {"ok": True, "tema": tema,
                                "invitacion": [n for n in range(1, 8) if f"invitacion_{n}.png" in files],
                                "afiche": [n for n in range(1, 8) if f"afiche_{n}.png" in files]})

    def _dash_base_img(self, q):
        """Miniatura del arte base (temas/<tema>/<slot>.png) para el modal."""
        if not self._admin_ok():
            return self._deny()
        tema = slug((q.get("tema", [""]) or [""])[0])
        slot = re.sub(r"[^a-z0-9_]", "", ((q.get("slot", [""]) or [""])[0] or "").lower())
        if not re.match(r"^(invitacion|afiche)_[1-7]$", slot):
            return self._json(400, {"ok": False, "error": "slot inválido"})
        tdir = os.path.join(temas.TEMAS_DIR, tema)
        archivo = slot + ".png"
        if not os.path.isfile(os.path.join(tdir, archivo)):
            return self._json(404, {"ok": False, "error": "no existe"})
        thumb = _pieza_thumb(tdir, archivo)
        if not thumb:
            return self._json(500, {"ok": False, "error": "no se pudo generar la miniatura"})
        data = open(thumb, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def _dash_arte_descargar(self, q):
        """Descarga el arte base a RESOLUCIÓN COMPLETA (invitación/afiche SIN texto: es el arte
        que genera el motor; el texto lo agrega el editor al personalizar)."""
        if not self._admin_ok():
            return self._deny()
        tema = slug((q.get("tema", [""]) or [""])[0])
        slot = re.sub(r"[^a-z0-9_]", "", ((q.get("slot", [""]) or [""])[0] or "").lower())
        if not re.match(r"^(invitacion|afiche)_[1-7]$", slot):
            return self._json(400, {"ok": False, "error": "slot inválido"})
        path = os.path.join(temas.TEMAS_DIR, tema, slot + ".png")
        if not os.path.isfile(path):
            return self._json(404, {"ok": False, "error": "no existe"})
        data = open(path, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Disposition", 'attachment; filename="%s-%s.png"' % (slot.replace("_", "-"), tema))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def _dash_arte_zip(self, q):
        """ZIP con TODAS las invitaciones (o afiches) base de un tema, SIN texto."""
        if not self._admin_ok():
            return self._deny()
        import zipfile
        tema = slug((q.get("tema", [""]) or [""])[0])
        tipo = "afiche" if ((q.get("tipo", [""]) or [""])[0] == "afiche") else "invitacion"
        tdir = os.path.join(temas.TEMAS_DIR, tema)
        buf = io.BytesIO(); n = 0
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for e in range(1, 8):
                p = os.path.join(tdir, "%s_%d.png" % (tipo, e))
                if os.path.isfile(p):
                    z.write(p, "%s-%s-%danios.png" % (tipo, tema, e)); n += 1
        if not n:
            return self._json(404, {"ok": False, "error": "no hay arte"})
        data = buf.getvalue()
        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition", 'attachment; filename="%s-%s-sin-texto.zip"' % (tipo, tema))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def _dash_borrar_base(self):
        """Borra un arte base (invitacion_N / afiche_N). La invitación de 1 año es
        obligatoria (la usa el editor y el producto) → no se puede borrar."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        slot = re.sub(r"[^a-z0-9_]", "", (q.get("slot", [""])[0] or "").lower())
        if not re.match(r"^(invitacion|afiche)_[1-7]$", slot):
            return self._json(400, {"ok": False, "error": "slot inválido"})
        if slot == "invitacion_1":
            return self._json(400, {"ok": False, "error": "la invitación de 1 año es obligatoria, no se puede borrar (sí reemplazar)"})
        tdir = os.path.join(temas.TEMAS_DIR, tema)
        path = os.path.join(tdir, slot + ".png")
        try:
            if os.path.isfile(path):
                os.remove(path); generador._specs_cache.pop(tema, None)
                thumb = os.path.join(tdir, ".thumbs", slot + ".png")
                if os.path.isfile(thumb):
                    os.remove(thumb)
                if slot.startswith("invitacion"):
                    _sync_edades(tema)
                return self._json(200, {"ok": True, "slot": slot})
            return self._json(404, {"ok": False, "error": "no existía"})
        except Exception as e:
            return self._json(500, {"ok": False, "error": str(e)})

    # ---- Cuaderno de actividades: ver/quitar/descargar/subir páginas (override) ----
    @staticmethod
    def _cuad_args(q):
        tema = slug((q.get("tema", [""]) or [""])[0])
        edad = (re.sub(r"\D", "", (q.get("edad", ["6"]) or ["6"])[0]) or "6")[:2]
        idx = int(re.sub(r"\D", "", (q.get("idx", ["0"]) or ["0"])[0]) or "0")
        return tema, edad, idx

    def _dash_cuaderno_estado(self, q):
        if not self._admin_ok():
            return self._deny()
        tema, edad, _ = self._cuad_args(q)
        try:
            import cuaderno
            return self._json(200, {"ok": True, **cuaderno.estado(tema, edad)})
        except Exception as e:
            return self._json(500, {"ok": False, "error": str(e)})

    def _dash_cuaderno_img(self, q):
        if not self._admin_ok():
            return self._deny()
        tema, edad, idx = self._cuad_args(q)
        full = (q.get("full", ["0"]) or ["0"])[0] == "1"
        try:
            import cuaderno
            img = cuaderno.pagina_efectiva(tema, edad, idx)
            if img is None:
                return self._json(404, {"ok": False, "error": "no existe"})
            if not full:
                img = img.copy(); img.thumbnail((480, 480), Image.LANCZOS)
            buf = io.BytesIO(); img.save(buf, "PNG"); data = buf.getvalue()
        except Exception as e:
            return self._json(500, {"ok": False, "error": str(e)})
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Cache-Control", "no-store")
        if full:
            self.send_header("Content-Disposition",
                             'attachment; filename="cuaderno_%s_%s_pg%02d.png"' % (tema, edad, idx))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def _dash_cuaderno_upload(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema, edad, idx = self._cuad_args(q)
        raw = self._body()
        if raw is None:
            return self._json(413, {"ok": False, "error": "imagen demasiado grande"})
        try:
            import cuaderno
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            od = cuaderno._override_dir(tema, edad); os.makedirs(od, exist_ok=True)
            im.save(os.path.join(od, "pg%02d.png" % idx))
            rm = os.path.join(od, "pg%02d.removed" % idx)
            if os.path.exists(rm):
                os.remove(rm)               # subir una página la "des-quita"
            return self._json(200, {"ok": True, "idx": idx, "size": list(im.size)})
        except Exception as e:
            return self._json(500, {"ok": False, "error": "upload falló: %s" % e})

    def _dash_cuaderno_borrar(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema, edad, idx = self._cuad_args(q)
        acc = (q.get("accion", ["quitar"]) or ["quitar"])[0]
        try:
            import cuaderno
            od = cuaderno._override_dir(tema, edad); os.makedirs(od, exist_ok=True)
            ovp = os.path.join(od, "pg%02d.png" % idx); rmp = os.path.join(od, "pg%02d.removed" % idx)
            if acc == "restaurar":          # vuelve a la página canónica original
                for p in (rmp, ovp):
                    if os.path.exists(p):
                        os.remove(p)
            else:                           # quitar la página del cuaderno
                open(rmp, "w").close()
            return self._json(200, {"ok": True, "idx": idx, "accion": acc})
        except Exception as e:
            return self._json(500, {"ok": False, "error": str(e)})

    def _dash_cuaderno_regenerar(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema, edad, _ = self._cuad_args(q)
        try:
            import cuaderno
            cuaderno.regenerar(tema, edad)
            return self._json(200, {"ok": True})
        except Exception as e:
            return self._json(500, {"ok": False, "error": str(e)})

    def _dash_cuaderno_regenerar_pagina(self):
        """Regenera SOLO una página del cuaderno (misma actividad, otro contenido interno) —
        a diferencia de 'Regenerar' (global), que rehace las 25-29 páginas."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema, edad, idx = self._cuad_args(q)
        try:
            import cuaderno
            ok = cuaderno.regenerar_pagina(tema, edad, idx)
            return self._json(200, {"ok": ok, "idx": idx})
        except Exception as e:
            return self._json(500, {"ok": False, "error": str(e)})

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
        # Flujo nuevo: alcanza con UNA invitación (la IA genera el resto desde ella
        # + los personajes de referencia). Todo lo demás es opcional.
        edades_up = [n for n in range(1, 8)
                     if os.path.isfile(os.path.join(tdir, "invitacion_%d.png" % n))]
        if not edades_up:
            return self._json(400, {"ok": False, "error": "subí al menos una invitación"})
        base = json.load(open(os.path.join(temas.TEMAS_DIR, "safari", "tema.json"), encoding="utf-8"))
        base["id"] = tema
        base["nombre"] = nombre or tema
        base["edades"] = edades_up
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

    def _dash_agregar_edades(self):
        """Marca para qué edades se ofrece el tema. Como la invitación es ÚNICA (la edad se
        agrega en el editor), copia esa única invitación a las edades elegidas: así el tema
        pasa a ofrecerlas y el afiche se puede replicar por edad. No borra edades existentes."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        pedidas = sorted({int(t) for t in (q.get("edades", [""])[0] or "").split(",")
                          if t.strip().isdigit() and 1 <= int(t.strip()) <= 7})
        if not pedidas:
            return self._json(400, {"ok": False, "error": "elegí al menos una edad"})
        tdir = os.path.join(temas.TEMAS_DIR, tema)
        fuente = next((os.path.join(tdir, "invitacion_%d.png" % n) for n in range(1, 8)
                       if os.path.isfile(os.path.join(tdir, "invitacion_%d.png" % n))), None)
        if not fuente:
            return self._json(400, {"ok": False, "error": "el tema no tiene invitación cargada"})
        import shutil
        copiadas = []
        for e in pedidas:
            dst = os.path.join(tdir, "invitacion_%d.png" % e)
            if not os.path.isfile(dst):
                shutil.copyfile(fuente, dst)
                copiadas.append(e)
        _sync_edades(tema)
        generador._specs_cache.pop(tema, None)
        edades = temas.cargar_tema(tema).get("edades", [])
        return self._json(200, {"ok": True, "edades": edades, "copiadas": copiadas})

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
        tipo = (payload.get("tipo") or "kit").lower().strip()
        nombre = (payload.get("nombre") or payload.get("titulo") or "").strip()
        precio = str(payload.get("precio", "")).strip()
        mostrar = bool(payload.get("mostrar", True))   # default True: el botón "Publicar" del
        # panel publica de verdad; pero un caller que pide mostrar=False (crear oculto para
        # revisar precio antes) DEBE respetarse (antes quedaba hardcodeado a True siempre).
        # Publica en la tienda Flask (no más WooCommerce). Cada (tipo, tema) es un
        # producto: KIT-<TEMA> (kit completo) / KIT-INVITACION-<TEMA> / KIT-CARTEL-<TEMA>…
        st, r = _tienda_admin("POST", "/kit-admin/publicar", {
            "tipo": tipo, "tema": tema,
            "precio": precio or None, "titulo": nombre or None, "mostrar": mostrar})
        if st != 200 or not r.get("ok"):
            return self._json(502 if st in (0, 502) else st,
                              {"ok": False, "error": r.get("error", "no se pudo publicar en la tienda")})
        return self._json(200, {"ok": True, "accion": "publicado", "tipo": tipo,
                                "ml_id": r.get("ml_id"), "slug": r.get("slug"),
                                "permalink": r.get("url")})

    def _dash_despublicar(self):
        if not self._admin_ok():
            return self._deny()
        try:
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json(400, {"ok": False, "error": "JSON inválido"})
        tema = slug(payload.get("tema", ""))
        tipo = (payload.get("tipo") or "kit").lower().strip()
        ml_id = payload.get("ml_id")
        # Oculta el producto de la tienda (toggle mostrar_en_tienda). No borra la fila
        # ni la temática (el arte queda; se puede re-publicar cuando quieras).
        st, r = _tienda_admin("POST", "/kit-admin/despublicar",
                              {"ml_id": ml_id, "tipo": tipo, "tema": tema, "mostrar": False})
        if st != 200 or not r.get("ok"):
            return self._json(502 if st in (0, 502) else st,
                              {"ok": False, "error": r.get("error", "no se pudo despublicar")})
        return self._json(200, {"ok": True, "ml_id": r.get("ml_id")})

    def _dash_pub_estado(self, q):
        if not self._admin_ok():
            return self._deny()
        tema = slug((q.get("tema", [""]) or [""])[0])
        st, r = _tienda_admin("GET", "/kit-admin/estado?tema=%s" % urllib.parse.quote(tema))
        if st != 200:
            return self._json(502 if st in (0, 502) else st,
                              {"ok": False, "error": r.get("error", "no se pudo consultar la tienda")})
        return self._json(200, r)

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
        # 1) ocultar de la tienda todos los productos de esta temática (no fatal si falla)
        try:
            st, est = _tienda_admin("GET", "/kit-admin/estado?tema=%s" % urllib.parse.quote(tema))
            for p in (est.get("productos") or []):
                if p.get("publicado"):
                    _tienda_admin("POST", "/kit-admin/despublicar",
                                  {"ml_id": p.get("ml_id"), "mostrar": False})
        except Exception:
            warn = "puede haber quedado algún producto en la tienda; revisalo"
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

    def _ia_draft(self, q):
        """Sirve un borrador de IA (temas/<tema>/ia_draft/<archivo>) para previsualizar."""
        if not self._admin_ok():
            return self._deny()
        tema = slug((q.get("tema", [""]) or [""])[0])
        archivo = os.path.basename((q.get("archivo", [""]) or [""])[0] or "")
        # Solo permitir .png sin subdirectorios ni traversal
        if not archivo.endswith(".png") or "/" in archivo or ".." in archivo:
            return self._json(400, {"ok": False, "error": "archivo inválido"})
        path = os.path.join(temas.TEMAS_DIR, tema, "ia_draft", archivo)
        rpath = os.path.realpath(path)
        base = os.path.realpath(os.path.join(temas.TEMAS_DIR, tema, "ia_draft"))
        if not rpath.startswith(base + os.sep):
            return self._json(400, {"ok": False, "error": "ruta inválida"})
        if not os.path.isfile(path):
            return self._json(404, {"ok": False, "error": "no existe"})
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _dash_libro_ia(self):
        """Genera con IA las ilustraciones del libro de cuento del tema y las guarda
        como overrides de escena (los mismos que la subida manual 📤: cualquier página
        se puede pisar a mano después). Sin `pieza` genera las 10; con `pieza=N` rehace
        solo esa. Devuelve un job; el progreso se consulta con /dash/ia-estado."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        client = _openai_client()
        if client is None:
            return self._json(503, {"ok": False, "error": "falta OPENAI_API_KEY"})
        paginas = None
        if q.get("pieza", [""])[0]:
            try:
                paginas = [int(q["pieza"][0])]
            except ValueError:
                return self._json(400, {"ok": False, "error": "pieza inválida"})
        calidad = _calidad(q)
        def trabajo(emit):
            import libro_ia
            libro_ia.generar_ilustraciones(client, tema, paginas, calidad=calidad,
                                           progress=emit)
        jid = ia_jobs.iniciar(trabajo)
        total = len(paginas) if paginas else 10
        return self._json(200, {"ok": True, "job": jid, "total": total, "calidad": calidad})

    def _ia_generar(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        client = _openai_client()
        if client is None:
            return self._json(503, {"ok": False, "error": "falta OPENAI_API_KEY"})
        edades = temas.cargar_tema(tema).get("edades", [1, 2, 3])
        calidad = _calidad(q)
        # "Generar kit" es INCREMENTAL: genera solo las piezas que faltan en el draft (para
        # completar una tanda que falló a mitad sin rehacer ni gastar de más). Reusa la
        # maestra cacheada. Para rehacer una pieza puntual está ↺ (regenerar).
        total = ia_orq.contar_faltantes(temas.TEMAS_DIR, tema, edades)
        if total == 0:
            return self._json(200, {"ok": True, "job": None, "total": 0,
                                    "mensaje": "Ya están todas las piezas. Usá ↺ para rehacer una."})
        def trabajo(emit):
            ia_orq.generar_tema(client, temas.TEMAS_DIR, tema, edades, progress=emit,
                                calidad=calidad, solo_faltantes=True, reusar_maestra=True)
        jid = ia_jobs.iniciar(trabajo)
        return self._json(200, {"ok": True, "job": jid, "calidad": calidad, "total": total})

    def _ia_estado(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        st = ia_jobs.estado(q.get("job", [""])[0])
        return self._json(200, {"ok": True, **st})

    def _ia_listado(self, q):
        # Borradores ya generados en ia_draft/ (para verlos al abrir el modal sin regenerar).
        if not self._admin_ok():
            return self._deny()
        tema = slug(q.get("tema", [""])[0])
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        return self._json(200, {"ok": True,
                                "archivos": ia_aprobar.listar_draft(temas.TEMAS_DIR, tema)})

    def _ia_regenerar(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        pieza = re.sub(r"[^a-z0-9_]", "", (q.get("pieza", [""])[0] or "").lower())[:30]
        client = _openai_client()
        if client is None:
            return self._json(503, {"ok": False, "error": "falta OPENAI_API_KEY"})
        edades = temas.cargar_tema(tema).get("edades", [1, 2, 3])
        ed = re.sub(r"\D", "", q.get("edad", [""])[0] or "")[:2]
        if ed and int(ed) in edades and pieza not in ia_orq.catalogo.UNA_SOLA:
            edades = [int(ed)]   # regenerar SOLO esa edad (no las otras de la pieza)
            # (la invitación es UNA_SOLA: se regenera una y se copia a todas las edades)
        calidad = _calidad(q)
        # En background (como ia-generar): regenerar es lento y un POST síncrono daba
        # 504/524 en el proxy. Reusa la maestra cacheada -> 1 sola llamada a OpenAI.
        def trabajo(emit):
            ia_orq.generar_tema(client, temas.TEMAS_DIR, tema, edades, progress=emit,
                                solo={pieza}, calidad=calidad, reusar_maestra=True)
        jid = ia_jobs.iniciar(trabajo)
        return self._json(200, {"ok": True, "job": jid})

    def _ia_colorear_variantes(self):
        """Genera las 3 variantes de 'colorear' que necesita el cuaderno de actividades
        (colorear.png/_2/_3), reintentando sola si OpenAI bloquea por moderación (aleatorio).
        Sin esto, el cuaderno cae a un fallback algorítmico roto (blob negro)."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        client = _openai_client()
        if client is None:
            return self._json(503, {"ok": False, "error": "falta OPENAI_API_KEY"})
        calidad = _calidad(q)
        def trabajo(emit):
            ia_orq.generar_variantes_colorear(client, temas.TEMAS_DIR, tema, n=3,
                                              calidad=calidad, progress=emit)
            import shutil   # el cuaderno cachea páginas armadas -> limpiar para que tome lo nuevo
            cache = os.path.join(temas.TEMAS_DIR, tema, "actividades_cache")
            if os.path.isdir(cache):
                shutil.rmtree(cache, ignore_errors=True)
        jid = ia_jobs.iniciar(trabajo)
        return self._json(200, {"ok": True, "job": jid})

    def _ia_replicar(self):
        # Replica una pieza (ej. afiche) de la 1ª edad al resto cambiando solo el número.
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        pieza = re.sub(r"[^a-z0-9_]", "", (q.get("pieza", [""])[0] or "").lower())[:30]
        client = _openai_client()
        if client is None:
            return self._json(503, {"ok": False, "error": "falta OPENAI_API_KEY"})
        edades = temas.cargar_tema(tema).get("edades", [1, 2, 3])
        if len([e for e in edades if int(e) != int(edades[0])]) == 0:
            return self._json(400, {"ok": False, "error":
                "este tema tiene una sola edad; subí invitaciones de otras edades para poder replicar"})
        calidad = _calidad(q)
        def trabajo(emit):
            ia_orq.replicar_pieza(client, temas.TEMAS_DIR, tema, pieza, edades,
                                  progress=emit, calidad=calidad)
        jid = ia_jobs.iniciar(trabajo)
        return self._json(200, {"ok": True, "job": jid})

    def _ia_aprobar(self):
        """Upscale a resolución de impresión + mover a extras/. Puede tardar bastante con
        muchas piezas (14+) -> corre en BACKGROUND con progreso por archivo, igual que
        generar/regenerar (un POST síncrono largo se veía "colgado" y arriesgaba 504/524
        en el proxy)."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        def trabajo(emit):
            try:
                ia_upscale.upscalar_draft(temas.TEMAS_DIR, tema,
                                          progress=lambda a: emit({"fase": "upscale", "archivo": a}))
            except Exception as e:
                print("[ia] upscale falló (sigo igual):", e)
            res = ia_aprobar.aprobar(temas.TEMAS_DIR, tema)
            generador._specs_cache.pop(tema, None)
            # refrescar thumbs de los archivos movidos (el modal de arte base no debe
            # mostrar el thumb viejo del slot invitacion_* sobrescrito)
            tdir = os.path.join(temas.TEMAS_DIR, tema)
            exdir = os.path.join(tdir, "extras")
            for name in res.get("movidas", []):
                try:
                    _pieza_thumb(tdir if name.startswith("invitacion_") else exdir, name)
                except Exception:
                    pass
            emit({"fase": "listo", **res})
        jid = ia_jobs.iniciar(trabajo)
        return self._json(200, {"ok": True, "job": jid})

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Servicio kit en puerto {PORT}  | data: {DATA_DIR}  | API key: {'(default)' if API_KEY=='cambiame-ya' else 'set'}")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
