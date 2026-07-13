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
import os, io, json, re, secrets, threading, time, collections, hashlib, urllib.parse, urllib.request, urllib.error, base64
import html as html_lib
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
# Cache en disco de las miniaturas del catálogo: /preview NO personalizado (sin `over`)
# se re-renderiza en cada carga de la tienda (cientos de productos) → se guarda el
# resultado y se sirve del disco por PREVIEW_CACHE_TTL. TTL corto (10 min) para que al
# regenerar el arte de un tema la tienda lo refleje enseguida (igual que el Cache-Control).
PREVIEW_CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache", "preview")
PREVIEW_CACHE_TTL = 21600        # 6h: cache estable (no re-render cada 10 min). Se invalida
                                 # por tema al editar un layout / regenerar arte (ver _preview_cache_clear).
os.makedirs(PREVIEW_CACHE_DIR, exist_ok=True)
# Límite de renders Pillow CONCURRENTES: aunque la tienda pida cientos de miniaturas a la
# vez (cache frío), nunca corren más de N a la vez → la CPU no se satura ni la memoria explota.
_RENDER_SEM = threading.Semaphore(max(2, (os.cpu_count() or 4) // 2))

def _cache_tema_dir(tema):
    safe = re.sub(r"[^a-zA-Z0-9_-]", "", str(tema or ""))[:40] or "default"
    return os.path.join(PREVIEW_CACHE_DIR, safe)

def _cache_tipo_prefix(tipo):
    return re.sub(r"[^a-z0-9_-]", "", str(tipo or "").lower())[:24] or "x"

# dedupe de renders idénticos concurrentes (popup + warmer pidiendo la misma pieza)
_RENDER_LOCKS = {}
_RENDER_LOCKS_GUARD = threading.Lock()

def _preview_cache_clear(tema=None, tipo=None):
    """Borra el cache de previews de un tema (o todo). Con `tipo`, borra SOLO las
    entradas de ese tipo (prefijo del archivo) — así regenerar el calendario no
    enfría las tarjetas de todos los demás productos del tema."""
    import shutil
    try:
        if tema and tipo:
            d = _cache_tema_dir(tema)
            pref = _cache_tipo_prefix(tipo) + "-"
            if os.path.isdir(d):
                for f in os.listdir(d):
                    if f.startswith(pref):
                        try: os.remove(os.path.join(d, f))
                        except OSError: pass
            return
        shutil.rmtree(_cache_tema_dir(tema) if tema else PREVIEW_CACHE_DIR, ignore_errors=True)
        os.makedirs(PREVIEW_CACHE_DIR, exist_ok=True)
    except Exception:
        pass

def _preview_warm(tema, tipo, indices):
    """Pre-calienta el cache de tarjetas EN BACKGROUND tras regenerar/subir piezas:
    pide las miniaturas (260) y la vista grande (1200) al propio servicio, así
    cuando el popup se refresca las tarjetas ya están renderizadas (el throttle
    _RENDER_SEM sigue mandando, no satura la CPU)."""
    import urllib.request
    base = "http://127.0.0.1:%d/preview" % PORT
    qs = "tipo=%s&tema=%s" % (urllib.parse.quote(str(tipo)), urllib.parse.quote(str(tema)))
    def _go():
        for mx in (260, 1200):   # primero thumbs (render maestro); el 1200 deriva del maestro
            for i in indices:
                try:
                    # mismo fmt que usa el popup del dash (jpg) para que la clave coincida
                    urllib.request.urlopen("%s?%s&pieza=%d&max=%d&fmt=jpg" % (base, qs, int(i), mx),
                                           timeout=180).read()
                except Exception:
                    pass
    threading.Thread(target=_go, daemon=True).start()

# Página que ve el cliente si abre su audiolibro mientras aún se está generando
# (~1-2 min tras la compra). Se auto-refresca hasta que el visor esté listo.
_AUDIOLIBRO_GENERANDO_HTML = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><meta http-equiv="refresh" content="12">
<title>Tu audiolibro se está grabando…</title><style>
*{margin:0;padding:0;box-sizing:border-box}html,body{height:100%}
body{background:#2a2438;color:#efeaff;font-family:system-ui,sans-serif;text-align:center;padding:24px;
 display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px}
.emoji{font-size:64px}h1{font-size:22px;font-weight:700}p{color:#b8aede;max-width:420px;line-height:1.5}
.dots span{width:10px;height:10px;border-radius:50%;background:#6B5BD2;display:inline-block;margin:0 3px;
 animation:b 1s infinite alternate}.dots span:nth-child(2){animation-delay:.2s}.dots span:nth-child(3){animation-delay:.4s}
@keyframes b{to{opacity:.2;transform:translateY(-6px)}}
</style></head><body>
<div class="emoji">🎧</div>
<h1>Tu audiolibro se está grabando</h1>
<p>Estamos ilustrando las páginas y grabando la narración. Tarda un par de minutos.
Esta página se actualiza sola — ¡no hace falta que hagas nada!</p>
<div class="dots"><span></span><span></span><span></span></div>
</body></html>"""

# El audiolibro falló al generarse: en vez de dejar al cliente en 'grabándose'
# eterno, un cartel amable. Se auto-refresca por si un reintento manual lo resuelve.
_AUDIOLIBRO_ERROR_HTML = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><meta http-equiv="refresh" content="30">
<title>Tu audiolibro está casi listo</title><style>
*{margin:0;padding:0;box-sizing:border-box}html,body{height:100%}
body{background:#2a2438;color:#efeaff;font-family:system-ui,sans-serif;text-align:center;padding:24px;
 display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px}
.emoji{font-size:64px}h1{font-size:22px;font-weight:700}p{color:#b8aede;max-width:440px;line-height:1.5}
</style></head><body>
<div class="emoji">🎧✨</div>
<h1>Tu audiolibro está casi listo</h1>
<p>Está tardando un poquito más de lo normal — lo estamos terminando a mano para
que quede perfecto. <b>Te lo enviamos por email apenas esté</b> (unos minutos).
No hace falta que hagas nada; podés cerrar esta página tranquilo.</p>
</body></html>"""

def _leer_openai_key():
    """Key de OpenAI: del entorno, o si falta (p.ej. tras una migración que perdió
    la env del service) de config.json — el mismo archivo donde ya vive el secreto.
    También la deja en os.environ para que el QA de libro_ia (que lee el env) funcione."""
    k = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not k:
        for p in (os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"),
                  "/opt/ct3d/backend/config.json"):
            try:
                k = (json.load(open(p)).get("openai_api_key") or "").strip()
                if k:
                    break
            except Exception:
                pass
    if k and not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = k
    return k


def _leer_openrouter_key():
    """Key de OpenRouter para el failover de imágenes: del entorno, o (como la de
    OpenAI) de config.json → 'openrouter_api_key', así sobrevive una migración que
    pierda la env del service. OpenRouter es el RESPALDO cuando OpenAI toca su tope
    mensual: con la key cargada, _openai_client arma el cliente con failover
    automático y el pipeline sigue solo. Sin key, no hay respaldo (como antes)."""
    k = (os.environ.get("OPENROUTER_API_KEY") or "").strip()
    if not k:
        for p in (os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"),
                  "/opt/ct3d/backend/config.json"):
            try:
                k = (json.load(open(p)).get("openrouter_api_key") or "").strip()
                if k:
                    break
            except Exception:
                pass
    if k and not os.environ.get("OPENROUTER_API_KEY"):
        os.environ["OPENROUTER_API_KEY"] = k
    return k


OPENAI_API_KEY     = _leer_openai_key()
OPENROUTER_API_KEY = _leer_openrouter_key()
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
    """Cliente de imágenes: OpenAI directo, con failover automático a OpenRouter
    si OPENROUTER_API_KEY está configurada (el tope mensual de OpenAI nos frenó
    generaciones 2 veces el 03-jul; con respaldo, el pipeline sigue solo).
    La key sale de _leer_openrouter_key (env o config.json)."""
    or_key = (OPENROUTER_API_KEY or "").strip()
    if not OPENAI_API_KEY:
        if or_key:
            from ia_kit.client_openrouter import OpenRouterImageClient
            return OpenRouterImageClient(or_key)
        return None
    primario = OpenAIImageClient(OPENAI_API_KEY, model=OPENAI_IMAGE_MODEL)
    if or_key:
        from ia_kit.client_openrouter import OpenRouterImageClient, ClienteImagenesFailover
        return ClienteImagenesFailover(primario, OpenRouterImageClient(or_key))
    return primario

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


def _limpiar_pedidos_viejos(dias=7300):
    """Borra carpetas de pedidos (ZIP + meta) de más de `dias`. Antes eran 30 días
    (A3, minimizar PII); ahora "para siempre" en la práctica (~20 años) — el pedido
    respalda la cuenta de cliente de la tienda (Mis compras), que promete acceso
    indefinido al link ya guardado en tienda_orders.kit_download_url."""
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
        if path == "/actividades-incluidos":
            # {edad: [títulos incluidos]} de actividades-web, para que la tienda
            # reordene la galería (desbloqueados primero) al cambiar de edad.
            import actividades_web
            return self._json(200, {"ok": True, "incluidos": actividades_web.incluidos_por_edad()})
        if path == "/preview":
            q = urllib.parse.parse_qs(u.query)
            data = {c: (q.get(c, [""])[0] or "") for c in CAMPOS}
            # campos EXTRA propios de un tipo (ej. menu_entrada/menu_plato del menú
            # infantil): cualquier query param que no sea de control se suma tal cual,
            # así un tipo nuevo con campos propios no necesita tocar este endpoint.
            for k, vals in q.items():
                if k not in CAMPOS and k not in ("tema", "tipo", "max", "fmt", "over", "pieza", "cb"):
                    data[k] = vals[0] if vals else ""
            tema = q.get("tema", ["safari"])[0]
            tipo = q.get("tipo", ["kit"])[0]
            # nombre de muestra SOLO donde el nombre ES el producto (libro,
            # invitación, banderín del kit...) — en el resto de los productos el
            # preview va limpio (Pablo 9-jul-2026: "sigo viendo Tomás")
            if not data["nombre"] and (tipo.startswith("libro") or tipo in
                    ("kit", "invitacion", "cartel", "fiesta-completa",
                     "video-invitacion", "invitacion-web")):
                data["nombre"] = "Tomás"
            # tamaño + formato configurables → miniaturas del catálogo livianas
            try: max_px = max(200, min(1200, int(q.get("max", ["900"])[0])))
            except Exception: max_px = 900
            fmt = (q.get("fmt", ["png"])[0] or "png").lower()
            ov = q.get("over", [""])[0]              # personalización del cliente (JSON)
            pieza = q.get("pieza", [""])[0]          # índice de pieza (galería: todas las del ZIP)
            ctype = "image/jpeg" if fmt in ("jpg", "jpeg") else "image/png"
            # Cache en disco SOLO para miniaturas del catálogo (sin personalización `over`):
            # son deterministas y se piden cientos de veces al cargar la tienda. Las
            # previews personalizadas (con over) se rinden siempre en vivo.
            cpath = None
            if not ov:
                key_parts = sorted((k, v[0]) for k, v in q.items() if k != "cb")
                ckey = hashlib.md5(repr(key_parts).encode("utf-8")).hexdigest()
                # prefijo por tipo → invalidación selectiva (_preview_cache_clear con tipo)
                cpath = os.path.join(_cache_tema_dir(tema),
                                     _cache_tipo_prefix(tipo) + "-" + ckey + ("." + fmt))
                try:
                    if os.path.exists(cpath) and (time.time() - os.path.getmtime(cpath) < PREVIEW_CACHE_TTL):
                        with open(cpath, "rb") as fh:
                            body = fh.read()
                        self.send_response(200)
                        self.send_header("Content-Type", ctype)
                        self.send_header("Cache-Control", "public, max-age=600")
                        self.send_header("Content-Length", str(len(body)))
                        self.end_headers(); self.wfile.write(body)
                        return
                except Exception:
                    pass
            if ov:
                try: data["_over"] = json.loads(ov)
                except Exception: pass
            # Render MAESTRO por pieza (tamaño completo, sin marca de agua, cacheado):
            # la miniatura (260) y la vista grande (1200) se derivan del mismo render
            # con un resize de milisegundos — antes cada tamaño re-renderizaba la hoja
            # entera (~2s c/u) y el zoom de una tarjeta recién cargada tardaba otra vez.
            mpath = None
            if not ov and pieza != "":
                mparts = sorted((k, v[0]) for k, v in q.items() if k not in ("cb", "max", "fmt"))
                mpath = os.path.join(_cache_tema_dir(tema),
                                     _cache_tipo_prefix(tipo) + "-" +
                                     hashlib.md5(repr(mparts).encode("utf-8")).hexdigest() + ".master.png")
            # dedupe: si el warmer y el popup piden lo mismo a la vez, renderiza UNO
            lk = None
            if cpath:
                with _RENDER_LOCKS_GUARD:
                    lk = _RENDER_LOCKS.setdefault(cpath, threading.Lock())
            try:
                if lk: lk.acquire()
                body = None
                if cpath and os.path.exists(cpath) and (time.time() - os.path.getmtime(cpath) < PREVIEW_CACHE_TTL):
                    with open(cpath, "rb") as fh:   # otro hilo lo dejó listo mientras esperábamos
                        body = fh.read()
                if body is None:
                    img = None
                    if mpath and os.path.exists(mpath) and (time.time() - os.path.getmtime(mpath) < PREVIEW_CACHE_TTL):
                        try:
                            img = Image.open(mpath).convert("RGB")
                            img.thumbnail((max_px, max_px), Image.LANCZOS)
                        except Exception:
                            img = None
                    if img is None:
                        with _RENDER_SEM:        # throttle: nunca más de N renders Pillow a la vez
                            if pieza != "":
                                # con master: render a tamaño completo (después se deriva);
                                # sin master (preview personalizado con `over`): al tamaño pedido
                                try: img = productos.preview_pieza(data, tema, tipo, int(pieza),
                                                                   max_px=(4000 if mpath else max_px))
                                except Exception: img = None
                            if img is None:
                                img = productos.preview(data, tema=tema, tipo=tipo, max_px=max_px)
                                mpath = None     # el preview compuesto no se masteriza
                        if mpath:
                            try:
                                os.makedirs(os.path.dirname(mpath), exist_ok=True)
                                tmp = mpath + ".tmp"
                                img.convert("RGB").save(tmp, "PNG")
                                os.replace(tmp, mpath)
                            except Exception: pass
                            img = img.copy()
                            img.thumbnail((max_px, max_px), Image.LANCZOS)
                    img = piezas.marca_agua(img)   # marca de agua SOLO en el preview (el comprado sale limpio)
                    buf = io.BytesIO()
                    if fmt in ("jpg", "jpeg"):
                        # to_rgb (fondo BLANCO), no convert("RGB") directo: convert aplana
                        # la transparencia a NEGRO y las piezas con alpha salían oscuras
                        piezas.to_rgb(img).save(buf, "JPEG", quality=80, optimize=True)
                    else:
                        img.save(buf, "PNG")
                    body = buf.getvalue()
                    if cpath:                    # guardar en cache para las próximas cargas
                        try:
                            os.makedirs(os.path.dirname(cpath), exist_ok=True)
                            tmp = cpath + ".tmp"
                            with open(tmp, "wb") as fh: fh.write(body)
                            os.replace(tmp, cpath)
                        except Exception: pass
            finally:
                if lk:
                    lk.release()
                    with _RENDER_LOCKS_GUARD:
                        _RENDER_LOCKS.pop(cpath, None)
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            # 10 min, no 24h: si se regenera el arte de un tema, la tienda lo refleja
            # enseguida (24h dejaba fichas con imágenes viejas en navegador+Cloudflare).
            self.send_header("Cache-Control", "public, max-age=600")
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
            # en modo admin (con auth) incluye los campos marcados 'no corresponde'
            # para poder re-activarlos; el cliente normal no los ve.
            es_admin = q.get("admin", ["0"])[0] == "1" and self._admin_ok(u)
            lay = generador.layout_para_editor(pieza, tema, admin=es_admin)
            # edades que ofrece el tema (las que tienen invitación): el editor del
            # cliente limita el selector a estas, no deja poner cualquier número.
            try:
                eds = [int(x) for x in (temas.cargar_tema(tema).get("edades") or []) if 1 <= int(x) <= 7]
            except Exception:
                eds = []
            lay["edades"] = sorted(set(eds)) or [1, 2, 3]
            return self._json(200, lay)
        if path == "/cliente/piezas-texto":
            # piezas del kit que tienen texto editable (para las pestañas del editor
            # multi-pieza del cliente). Excluye las que quedaron sin campos que 'corresponden'.
            q = urllib.parse.parse_qs(u.query)
            tema = q.get("tema", ["safari"])[0]
            specs = generador.specs_de(tema)
            _LBL = {"invitacion": "✉️ Invitación", "afiche": "🎈 Afiche", "banderin": "🎉 Banderín",
                    "tarjetas_agradecimiento": "💌 Tarjeta", "cajita_sorpresa": "🎁 Cajita",
                    "decoracion_sorbetes": "🥤 Sorbetes"}
            # Se incluye toda pieza que tenga texto que "corresponde" (no oculto). Por
            # default banderín/cajita/sorbetes vienen en "no corresponde" y quedan afuera;
            # si el admin destilda alguna en un tema, pasa a tener campos y aparece acá.
            _ORDEN = ["invitacion", "afiche", "tarjetas_agradecimiento",
                      "banderin", "cajita_sorpresa", "decoracion_sorbetes"]
            lista_pz = []
            for pz in _ORDEN:
                s = specs.get(pz)
                if not s:
                    continue
                try:
                    campos = generador._effective_texts(s)   # excluye los 'no corresponde'
                except Exception:
                    campos = s.get("text") or []
                if campos:
                    lista_pz.append({"pieza": pz, "label": _LBL.get(pz, pz)})
            return self._json(200, {"ok": True, "piezas": lista_pz})
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
        # ---- STL de muestra para el visor 3D de la ficha (público, texto genérico) ----
        m = re.match(r"^/stl-muestra/([a-z]+)/([a-z0-9-]+)\.stl$", path)
        if m:
            pieza, tema_m = m.group(1), m.group(2)
            if pieza not in ("medalla", "topper", "trofeo", "cortante") or not temas.existe(tema_m):
                return self._json(404, {"ok": False, "error": "no existe"})
            try:
                data = productos.stl3d_muestra(tema_m, pieza)
            except Exception as e:
                return self._json(500, {"ok": False, "error": str(e)[:120]})
            self.send_response(200)
            self.send_header("Content-Type", "model/stl")
            self.send_header("Cache-Control", "public, max-age=604800")
            self.send_header("Access-Control-Allow-Origin", "*")  # la ficha vive en otro dominio
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        # ---- audiolibro web (página narrada con page-flip; link con token) ----
        m = re.match(r"^/al/([A-Za-z0-9_-]+)(?:/([a-z_0-9.]+))?$", path)
        if m:
            import audiolibro
            token, arch = m.group(1), m.group(2)
            if arch:
                r = audiolibro.archivo(token, arch)
                if r is None:
                    return self._json(404, {"ok": False, "error": "no existe"})
                data_b, ct = r
                # ?wm=1: marca de agua para las páginas de PREVIEW en la ficha de la tienda
                q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                if q.get("wm") and ct.startswith("image"):
                    try:
                        _im = Image.open(io.BytesIO(data_b)).convert("RGB")
                        _buf = io.BytesIO()
                        piezas.marca_agua(_im).save(_buf, "JPEG", quality=82)
                        data_b = _buf.getvalue()
                    except Exception:
                        pass
                self.send_response(200)
                self.send_header("Content-Type", ct)
                self.send_header("Cache-Control", "public, max-age=86400")
                self.send_header("Content-Length", str(len(data_b)))
                self.end_headers(); self.wfile.write(data_b)
                return
            page = audiolibro.html(token, base_url=self.base_url())
            if page is None:
                est = audiolibro.estado(token)
                if est in ("generando", "error"):
                    body = (_AUDIOLIBRO_ERROR_HTML if est == "error"
                            else _AUDIOLIBRO_GENERANDO_HTML).encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Cache-Control", "no-store")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers(); self.wfile.write(body)
                    return
                return self._json(404, {"ok": False, "error": "audiolibro no encontrado"})
            body = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
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
        # ---- actividades web (cuaderno interactivo; link con token) ----
        # OJO: el visor usa rutas RELATIVAS -> siempre servirlo bajo /act/<tok>/
        # (con barra final); /act/<tok> sin barra redirige.
        m = re.match(r"^/act/([A-Za-z0-9_-]+)(?:/([a-z_0-9.]*))?$", path)
        if m:
            import actividades_web as aw
            token, arch = m.group(1), m.group(2)
            if arch is None:
                self.send_response(301)
                self.send_header("Location", "/act/%s/" % token)
                self.end_headers()
                return
            if arch:
                r = aw.archivo(token, arch)
                if r is None:
                    return self._json(404, {"ok": False, "error": "no existe"})
                data_b, ct = r
                self.send_response(200)
                self.send_header("Content-Type", ct)
                self.send_header("Cache-Control", "public, max-age=86400")
                self.send_header("Content-Length", str(len(data_b)))
                self.end_headers(); self.wfile.write(data_b)
                return
            page = aw.html(token)
            if page is None:
                return self._json(404, {"ok": False, "error": "actividades no encontradas"})
            body = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
            return
        # ---- rompecabezas interactivo (link con token) ----
        # Igual que /act: rutas RELATIVAS -> servir SIEMPRE bajo /armar/<tok>/.
        m = re.match(r"^/armar/([A-Za-z0-9_-]+)(?:/([a-z_0-9.]*))?$", path)
        if m:
            import rompecabezas_web as rw
            token, arch = m.group(1), m.group(2)
            if arch is None:
                self.send_response(301)
                self.send_header("Location", "/armar/%s/" % token)
                self.end_headers()
                return
            if arch:
                r = rw.archivo(token, arch)
                if r is None:
                    return self._json(404, {"ok": False, "error": "no existe"})
                data_b, ct = r
                self.send_response(200)
                self.send_header("Content-Type", ct)
                self.send_header("Cache-Control", "public, max-age=86400")
                self.send_header("Content-Length", str(len(data_b)))
                self.end_headers(); self.wfile.write(data_b)
                return
            page = rw.html(token)
            if page is None:
                return self._json(404, {"ok": False, "error": "rompecabezas no encontrado"})
            body = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
            return
        # ---- mándalas para pintar (modalidad web del kit; link con token) ----
        # Igual que /act: rutas RELATIVAS -> servir SIEMPRE bajo /pintar/<tok>/.
        m = re.match(r"^/pintar/([A-Za-z0-9_-]+)(?:/([a-z_0-9.]*))?$", path)
        if m:
            import mandalas_web as mw
            token, arch = m.group(1), m.group(2)
            if arch is None:
                self.send_response(301)
                self.send_header("Location", "/pintar/%s/" % token)
                self.end_headers()
                return
            if arch:
                r = mw.archivo(token, arch)
                if r is None:
                    return self._json(404, {"ok": False, "error": "no existe"})
                data_b, ct = r
                self.send_response(200)
                self.send_header("Content-Type", ct)
                self.send_header("Cache-Control", "public, max-age=86400")
                self.send_header("Content-Length", str(len(data_b)))
                self.end_headers(); self.wfile.write(data_b)
                return
            page = mw.html(token)
            if page is None:
                return self._json(404, {"ok": False, "error": "mándalas no encontradas"})
            body = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
            return
        # ---- "elegí tu aventura" (PROTOTIPO; libro-cuento con decisiones; link con
        # token) ---- Igual que /act: rutas RELATIVAS -> servir SIEMPRE bajo /leer/<tok>/.
        m = re.match(r"^/leer/([A-Za-z0-9_-]+)(?:/([a-z_0-9.]*))?$", path)
        if m:
            import aventura_web as avw
            token, arch = m.group(1), m.group(2)
            if arch is None:
                self.send_response(301)
                self.send_header("Location", "/leer/%s/" % token)
                self.end_headers()
                return
            if arch:
                r = avw.archivo(token, arch)
                if r is None:
                    return self._json(404, {"ok": False, "error": "no existe"})
                data_b, ct = r
                self.send_response(200)
                self.send_header("Content-Type", ct)
                self.send_header("Cache-Control", "public, max-age=86400")
                self.send_header("Content-Length", str(len(data_b)))
                self.end_headers(); self.wfile.write(data_b)
                return
            page = avw.html(token)
            if page is None:
                return self._json(404, {"ok": False, "error": "aventura no encontrada"})
            body = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers(); self.wfile.write(body)
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
                    if que == "libro-audio":
                        icono, titulo, detalle = "🎧", "Tu audiolibro se está grabando", \
                            "Estamos narrando el cuento página por página. Tarda 1-2 minutos."
                    elif que == "video-invitacion":
                        icono, titulo, detalle = "🎬", "Tu video-invitación se está armando", \
                            "Estamos animando el video con los datos de tu fiesta. Tarda menos de un minuto."
                    elif que == "fiesta-completa":
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
        if path == "/dash/libro-admin":
            return self._dash_libro_admin(u)
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
        if path == "/dash/calendario-layout":
            return self._dash_calendario_layout(urllib.parse.parse_qs(u.query))
        if path == "/dash/calendario-fondo":
            return self._dash_calendario_fondo(urllib.parse.parse_qs(u.query))
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
        if path == "/dash/corona-ia-generar":
            return self._corona_ia_generar()
        if path == "/dash/fondos-ia-generar":
            return self._fondos_ia_generar()
        if path == "/dash/armar-tema":
            return self._armar_tema()
        if path == "/dash/rompe-demo":
            return self._rompe_demo()
        if path == "/dash/pieza-regenerar":
            return self._pieza_regenerar()
        if path == "/dash/agregar-edades":
            return self._dash_agregar_edades()
        if path == "/dash/ia-colorear-variantes":
            return self._ia_colorear_variantes()
        if path == "/dash/producto-upload":
            return self._dash_producto_upload()
        if path == "/dash/libro-audio-demo":
            return self._dash_libro_audio_demo()
        if path == "/dash/libro-regen":
            return self._dash_libro_regen()
        if path == "/dash/libro-nota":
            return self._dash_libro_nota()
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
        if path == "/api/al-info":
            # Valida un token de audiolibro y devuelve sus datos. Lo usa la tienda
            # para "canjear mi libro" (agregar un audiolibro a la cuenta del cliente).
            # Protegido por API-key + Cloudflare bloquea POST /api/ externo → interno.
            if not secrets.compare_digest(self.headers.get("X-API-Key", "") or "", API_KEY):
                return self._json(401, {"ok": False, "error": "API key inválida"})
            raw = self._body()
            try:
                payload = json.loads(raw or b"{}")
            except Exception:
                return self._json(400, {"ok": False, "error": "JSON inválido"})
            import audiolibro
            tok = str(payload.get("token", "")).strip()
            est = audiolibro.estado(tok)
            if est is not None:
                reg = audiolibro._cargar(tok) or {}
                return self._json(200, {"ok": True, "tipo": "libro-audio", "estado": est,
                                        "nombre": reg.get("nombre", ""), "tema": reg.get("tema", ""),
                                        "url": f"{self.base_url()}/al/{tok}"})
            # ¿es un cuaderno de actividades? (mismo canje: pegar el link /act/<tok>)
            import actividades_web as aw
            est = aw.estado(tok)
            if est is not None:
                reg = aw._cargar(tok) or {}
                return self._json(200, {"ok": True, "tipo": "actividades-web", "estado": est,
                                        "nombre": reg.get("nombre", ""), "tema": reg.get("tema", ""),
                                        "url": f"{self.base_url()}/act/{tok}/"})
            # ¿es un rompecabezas interactivo? (mismo canje: pegar el link /armar/<tok>)
            import rompecabezas_web as rw
            est = rw.estado(tok)
            if est is None:
                return self._json(404, {"ok": False, "error": "token no encontrado"})
            reg = rw._cargar(tok) or {}
            return self._json(200, {"ok": True, "tipo": "rompecabezas-web", "estado": est,
                                    "nombre": reg.get("nombre", ""), "tema": reg.get("tema", ""),
                                    "url": f"{self.base_url()}/armar/{tok}/"})
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
        if isinstance(payload.get("porPieza"), dict):   # kit multi-pieza: over por cada pieza
            data["_porPieza"] = payload["porPieza"]
        tema = str(payload.get("tema", "safari")).strip() or "safari"
        tipo = str(payload.get("tipo", "kit")).strip() or "kit"
        if not productos.existe_tipo(tipo):
            return self._json(400, {"ok": False, "error": f"tipo desconocido: {tipo}"})
        order_id = slug(payload.get("order_id", "s"))
        token = f"{order_id}-{secrets.token_hex(16)}"   # A2: 128 bits, no brute-forceable
        dest = os.path.join(DATA_DIR, token)
        if tipo == "libro-pdf":
            # Libro imprimible GENÉRICO prearmado (historia y protagonista fijos,
            # nada customizable): se copia el zip prearmado -> entrega inmediata.
            import shutil
            hist = (data.get("historia") or "").strip().lower()
            pre = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "libros_pdf", hist, "kit.zip")
            if not os.path.isfile(pre):
                return self._json(503, {"ok": False,
                                        "error": "libro-pdf no prearmado: %s" % hist})
            os.makedirs(dest, exist_ok=True)
            shutil.copyfile(pre, os.path.join(dest, "kit.zip"))
            return self._json(200, {"ok": True, "token": token,
                                    "download_url": f"{self.base_url()}/descarga/{token}"})
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
        if tipo == "actividades-web":
            # El producto ES un link (cuaderno de actividades interactivo, app viva).
            # Generación SÍNCRONA y rápida — sin llamadas IA: puzzles procedurales
            # verificados + arte ya existente del tema (recortes/colorear/escena).
            import actividades_web as aw
            try:
                tok_act = aw.crear(data, tema)
            except Exception as e:
                return self._json(500, {"ok": False, "error": str(e)[:200]})
            return self._json(200, {"ok": True, "token": token, "act_token": tok_act,
                                    "download_url": f"{self.base_url()}/act/{tok_act}/"})
        if tipo == "rompecabezas-web":
            # El producto ES un link (rompecabezas interactivo, app viva).
            # Generación SÍNCRONA y rápida — sin llamadas IA: cortes procedurales
            # (la receta del imprimible) + arte ya existente del tema.
            import rompecabezas_web as rw
            try:
                tok_r = rw.crear(data, tema)
            except Exception as e:
                return self._json(500, {"ok": False, "error": str(e)[:200]})
            return self._json(200, {"ok": True, "token": token, "rompe_token": tok_r,
                                    "download_url": f"{self.base_url()}/armar/{tok_r}/"})
        if tipo == "mandalas":
            # DOBLE modalidad en un solo producto: el visor /pintar/<tok>/ deja PINTAR las
            # mándalas online Y tiene el botón de descarga del PDF imprimible (el kit.zip que
            # se guarda en el token). Se entrega como link (como actividades-web): la tienda
            # lo trata de visor y el PDF viaja dentro. Síncrono y rápido (sin IA; el arte ya
            # está en el repo).
            import mandalas_web as mw
            try:
                tok_m = mw.crear({**data, "tema": tema})
            except Exception as e:
                return self._json(500, {"ok": False, "error": str(e)[:200]})
            return self._json(200, {"ok": True, "token": token, "mand_token": tok_m,
                                    "download_url": f"{self.base_url()}/pintar/{tok_m}/"})
        if tipo == "libro-audio":
            # Genera páginas + narración TTS (~1-2 min) EN BACKGROUND, pero devuelve
            # YA el link estable del visor /al/<tok_al>. Así la tienda lo guarda en la
            # orden y el cliente lo ve en su biblioteca apenas compra; mientras se
            # genera, el visor muestra un cartel de "grabándose".
            import audiolibro
            tok_al = secrets.token_urlsafe(12)      # link estable, se devuelve ahora
            base = self.base_url()                  # capturar acá: el worker no tiene request
            audiolibro.marcar_generando(tok_al)
            os.makedirs(dest, exist_ok=True)
            with open(os.path.join(dest, "generando.flag"), "w") as f:
                f.write("libro-audio")
            with open(os.path.join(dest, "meta.json"), "w", encoding="utf-8") as f:
                json.dump({"order_id": payload.get("order_id"), "tema": tema, "tipo": tipo,
                           "nombre": data.get("nombre", ""), "al_token": tok_al},
                          f, ensure_ascii=False, indent=2)

            def _audio_una_vez(data, dest, tema, tok_al):
                import audiolibro, zipfile, libro_ia
                escenas = None
                hist = (data.get("historia") or "").strip().lower()
                if hist in libro_ia._ESCENAS_POR_HISTORIA_LARGO:
                    # Catálogo de audiolibros: arte por combo con CACHE (generar
                    # una vez -> revisar -> reusar). Si el combo ya está cacheado
                    # la venta NO regenera nada; si falta, se genera y cachea.
                    escenas = os.path.join(dest, "escenas")
                    try:
                        libro_ia.arte_catalogo(
                            _openai_client(), tema, hist,
                            data.get("genero"), data.get("edad"), escenas,
                            progress=lambda m: print("[libro-audio]", m, flush=True),
                            fallos_log=os.path.join(dest, "qa_fallos.txt"))
                    except Exception as e:
                        print("[libro-audio] arte falló (%s) — arte del tema" % e,
                              flush=True)
                        escenas = None
                audiolibro.crear(data, tema, OPENAI_API_KEY,
                                 escenas_dir=escenas, token=tok_al)
                with zipfile.ZipFile(os.path.join(dest, "kit.zip"), "w") as z:
                    z.writestr("TU_AUDIOLIBRO.txt",
                               "Tu audiolibro narrado está en:\n%s/al/%s\n\n"
                               "Compartí ese link con la familia — dura 1 año." %
                               (base, tok_al))

            def _audio_worker(data=data, dest=dest, tema=tema, tok_al=tok_al,
                              base=base, payload=payload):
                import audiolibro
                ok = False
                # Reintento: la mayoría de las fallas son transitorias (red/timeout
                # de la API). Dos intentos antes de darlo por fallido.
                for intento in (1, 2):
                    try:
                        _audio_una_vez(data, dest, tema, tok_al)
                        ok = True
                        break
                    except Exception as e:
                        print("[libro-audio] intento %d falló: %s" % (intento, e),
                              flush=True)
                try:
                    os.remove(os.path.join(dest, "generando.flag"))
                except OSError:
                    pass
                if not ok:
                    # NO dejar al cliente en 'grabándose' eterno: marca error (el
                    # visor muestra un cartel amable) y deja registro para el
                    # vendedor en pedidos/audiolibros_fallidos.log.
                    audiolibro.marcar_error(tok_al, "generación falló tras 2 intentos")
                    try:
                        with open(os.path.join(DATA_DIR, "audiolibros_fallidos.log"),
                                  "a", encoding="utf-8") as fl:
                            fl.write("%d\torder=%s\ttok=%s\ttema=%s\thist=%s\n" % (
                                int(time.time()), payload.get("order_id"), tok_al,
                                tema, data.get("historia", "")))
                    except OSError:
                        pass
                    print("[libro-audio] ⚠️ FALLÓ definitivamente order=%s tok=%s "
                          "— regenerar a mano" % (payload.get("order_id"), tok_al),
                          flush=True)

            threading.Thread(target=_audio_worker, daemon=True).start()
            return self._json(200, {"ok": True, "token": token, "generando": True,
                                    "al_token": tok_al,
                                    "download_url": f"{base}/al/{tok_al}"})
        if tipo == "video-invitacion":
            # El render tarda 30-60s (> timeout de la tienda): async con espera.
            os.makedirs(dest, exist_ok=True)
            with open(os.path.join(dest, "generando.flag"), "w") as f:
                f.write("video-invitacion")
            with open(os.path.join(dest, "meta.json"), "w", encoding="utf-8") as f:
                json.dump({"order_id": payload.get("order_id"), "tema": tema, "tipo": tipo,
                           "nombre": data.get("nombre", "")}, f, ensure_ascii=False, indent=2)

            def _video_worker(data=data, dest=dest, tema=tema):
                try:
                    productos.generar(data, dest, tema, "video-invitacion")
                except Exception as e:
                    print("[video-invitacion] falló: %s" % e, flush=True)
                finally:
                    try:
                        os.remove(os.path.join(dest, "generando.flag"))
                    except OSError:
                        pass

            threading.Thread(target=_video_worker, daemon=True).start()
            return self._json(200, {"ok": True, "token": token, "generando": True,
                                    "download_url": f"{self.base_url()}/descarga/{token}"})
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
                                                       genero=data.get("genero"),
                                                       historia=data.get("historia"),
                                                       verificar=True,
                                                       fallos_log=os.path.join(dest, "qa_fallos.txt"))
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
            if isinstance(v.get("tpl"), str):        # texto default de un campo fijo (texto2/texto3)
                o["tpl"] = v["tpl"][:200]
            if "default_hidden" in v:                # estado del toggle "incluir" (apagado por default)
                o["default_hidden"] = bool(v["default_hidden"])
            r = v.get("repeat")                      # multiplicador: repetir el texto N veces
            if isinstance(r, dict):
                try: n = int(r.get("count", 1))
                except Exception: n = 1
                if n > 1:
                    rc = {"count": min(n, 60)}
                    try: rc["cols"] = max(1, min(int(r.get("cols", 1)), 12))
                    except Exception: rc["cols"] = 1
                    for kk in ("dx", "dy"):
                        try: rc[kk] = round(float(r.get(kk, 0)), 4)
                        except Exception: rc[kk] = 0.0
                    o["repeat"] = rc
            if o:
                clean[k] = o
        # "no corresponde": campos que el admin oculta para el cliente (no los ve).
        # Se escribe SIEMPRE (aunque vacío) para dejar registrada la decisión: algunas
        # piezas ocultan su texto por default (banderín/cajita/sorbetes) y la clave
        # presente —aunque sea []— le dice al motor "Pablo ya decidió, respetá esto".
        oc = [str(x) for x in (payload.get("oculto") or []) if isinstance(x, str) and x][:40]
        clean["_oculto"] = oc
        # campos de texto que el admin AGREGÓ a la pieza (ej: 3er texto en la tarjeta)
        nuevos = []
        for nf in (payload.get("nuevos") or [])[:20]:
            if not isinstance(nf, dict):
                continue
            fid = re.sub(r"[^a-z0-9_]", "", str(nf.get("id") or "").lower())[:24]
            if not fid:
                continue
            c = {"id": fid, "tpl": str(nf.get("tpl") or "")[:120]}
            for kk in ("x", "y", "size", "maxw", "wght"):
                if kk in nf:
                    try: c[kk] = round(float(nf[kk]), 4)
                    except Exception: pass
            if isinstance(nf.get("font"), str) and nf["font"]:
                c["font"] = nf["font"]
            if isinstance(nf.get("color"), str) and nf["color"].startswith("#"):
                c["color"] = nf["color"]
            if isinstance(nf.get("anchor"), str) and len(nf["anchor"]) == 2:
                c["anchor"] = nf["anchor"]
            c["toggleable"] = bool(nf.get("toggleable", True))
            nuevos.append(c)
        if nuevos:
            clean["_nuevos"] = nuevos
        pieza = payload.get("pieza", "invitacion")
        tema = payload.get("tema", "safari")
        p = generador.layout_file_path(pieza, tema)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(clean, f, ensure_ascii=False, indent=2)
        _preview_cache_clear(tema)   # el cambio de layout se ve en la tienda enseguida
        return self._json(200, {"ok": True, "guardado": len(clean),
                                "ocultos": len(oc), "nuevos": len(nuevos), "pieza": pieza})

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
                generador._specs_cache.pop(tema, None); _preview_cache_clear(tema)
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
    # FUENTE ÚNICA = productos (antes esta lista fija se desincronizó y la galería
    # 'Piezas del kit' no mostraba base_torta ni topper_palito — bug de Pablo 11-jul).
    _PIEZAS_EDAD = list(productos._EXTRAS_POR_EDAD)
    _PIEZAS_UNIV = list(productos._EXTRAS_UNIVERSAL)

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
            generador._specs_cache.pop(tema, None); _preview_cache_clear(tema)
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
                os.remove(path); generador._specs_cache.pop(tema, None); _preview_cache_clear(tema)
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
            # vista ADMIN: incluye el solucionario (en la tienda queda oculto)
            meta = productos.piezas_meta(tipo, tema, incluir_soluciones=True)
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
        muestra = {"nombre": ("Tomás" if tipo.startswith("libro") else ""),
                   "edad": "5", "anyo": "2026"}
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
        muestra = {"nombre": ("Tomás" if tipo.startswith("libro") else ""),
                   "edad": "5", "anyo": "2026"}
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
        # sin esto, la tarjeta del dash (y la tienda) muestran la pieza VIEJA hasta 6h
        generador._specs_cache.pop(tema, None); _preview_cache_clear(tema, tipo)
        _preview_warm(tema, tipo, [idx])
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
            generador._specs_cache.pop(tema, None); _preview_cache_clear(tema, tipo)
            _preview_warm(tema, tipo, [idx])
            return self._json(200, {"ok": True, "borrado": True})
        return self._json(200, {"ok": True, "borrado": False})

    def _cal_layout_path(self, tema):
        return os.path.join(temas.TEMAS_DIR, tema, "calendario", "layout.json")

    def _cal_default_path(self):
        # Layout base que heredan las temáticas nuevas (la última que se guardó,
        # porque "casi siempre son iguales" entre temas).
        return os.path.join(temas.TEMAS_DIR, "_calendario_layout.json")

    def _cal_load_layout(self, tema):
        p = self._cal_layout_path(tema)
        if os.path.isfile(p):
            try:
                return json.load(open(p, encoding="utf-8"))
            except Exception:
                pass
        return None

    def _cal_save_layout(self, tema, layout):
        p = self._cal_layout_path(tema)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        try:
            json.dump(layout, open(p, "w", encoding="utf-8"), ensure_ascii=False)
            # default global para temas nuevos: las DOS reglas (5 y 6 filas)
            json.dump({"base": layout.get("base", {}), "base6": layout.get("base6")},
                      open(self._cal_default_path(), "w", encoding="utf-8"),
                      ensure_ascii=False)
        except Exception:
            pass

    @staticmethod
    def _cal_completar_base6(layout, anyo):
        """Si el layout todavía no tiene la regla de 6 filas, la precarga desde el
        override puntual de algún mes de 6 filas (los ajustes a mano que ya hizo
        el usuario) para que el editor no arranque de cero."""
        if layout.get("base6"):
            return
        import calendario
        for m in calendario.meses_por_filas(anyo, 6):
            cfg = (layout.get("meses") or {}).get(str(m))
            if cfg:
                layout["base6"] = cfg
                return

    def _dash_calendario_layout(self, q):
        """Devuelve las coordenadas guardadas del calendario de un tema (memoria por
        tema): regla general `base` (meses de 5 filas), regla `base6` (meses de 6
        filas) y overrides puntuales `meses`. Si el tema no tiene, hereda el layout
        de la última temática configurada."""
        if not self._admin_ok():
            return self._deny()
        tema = slug((q.get("tema", [""]) or [""])[0])
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        layout = self._cal_load_layout(tema)
        origen = "tema"
        if not layout:
            base, base6 = {}, None
            dp = self._cal_default_path()
            if os.path.isfile(dp):
                try:
                    d = json.load(open(dp, encoding="utf-8"))
                    # formato nuevo: {"base":..., "base6":...}; viejo: la base pelada
                    base = d.get("base", d) if isinstance(d, dict) and "base" in d else d
                    base6 = d.get("base6") if isinstance(d, dict) else None
                    origen = "default"
                except Exception:
                    base = {}
            if not base:
                origen = "vacio"
            layout = {"base": base, "base6": base6, "meses": {}, "anyo": "2026"}
        try:
            anyo = int(re.sub(r"\D", "", str(layout.get("anyo") or "2026"))[:4] or "2026")
        except Exception:
            anyo = 2026
        self._cal_completar_base6(layout, anyo)
        cal_dir = os.path.join(temas.TEMAS_DIR, tema, "calendario")
        return self._json(200, {"ok": True, "layout": layout, "origen": origen,
                                "tiene_fondo": os.path.isfile(os.path.join(cal_dir, "fondo.png")),
                                "tiene_fondo6": os.path.isfile(os.path.join(cal_dir, "fondo6.png"))})

    def _dash_calendario_fondo(self, q):
        """Sirve la plantilla guardada del calendario del tema, para que el editor
        la precargue sin volver a subirla. Con `filas=6` sirve la plantilla propia
        de los meses de 6 filas (fondo6.png) si existe; si no, la general."""
        if not self._admin_ok():
            return self._deny()
        tema = slug((q.get("tema", [""]) or [""])[0])
        filas6 = ((q.get("filas", [""]) or [""])[0] or "").strip() == "6"
        cal_dir = os.path.join(temas.TEMAS_DIR, tema, "calendario")
        fondo = os.path.join(cal_dir, "fondo6.png")
        if not filas6 or not os.path.isfile(fondo):
            fondo = os.path.join(cal_dir, "fondo.png")
        if not tema or not os.path.isfile(fondo):
            return self._json(404, {"ok": False, "error": "no hay fondo"})
        data = open(fondo, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)

    def _dash_calendario_generar(self):
        """Genera el calendario superponiendo mes/días/números sobre la plantilla.
        - Con `filas` (5 o 6): regenera TODOS los meses de ese grupo con la regla
          (config) y la guarda en `base` (5) o `base6` (6). Los overrides puntuales
          de esos meses se descartan: la regla pasa a mandar.
        - Sin `mes` ni `filas`: genera los 12 (guarda base + regla de 6 filas +
          overrides por mes existentes).
        - Con `mes` (1-12): regenera SOLO ese mes con coordenadas propias (compat).
        La plantilla viene en el body; si no, se usa la guardada del GRUPO que se
        genera (fondo.png para 5 filas, fondo6.png para 6 — cada regla puede tener
        su propio arte). Guarda las coordenadas en layout.json (memoria por tema)."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        anyo_str = re.sub(r"\D", "", (q.get("anyo", ["2026"])[0] or "2026"))[:4] or "2026"
        nombre = (q.get("nombre", [""])[0] or "").strip() or "Mi familia"
        config_str = q.get("config", [""])[0] or ""
        mes_str = re.sub(r"\D", "", q.get("mes", [""])[0] or "")
        mes = int(mes_str) if mes_str else 0     # 0 = los 12
        filas_str = re.sub(r"\D", "", q.get("filas", [""])[0] or "")
        filas = int(filas_str) if filas_str in ("5", "6") else 0
        if mes and not (1 <= mes <= 12):
            return self._json(400, {"ok": False, "error": "mes inválido"})
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        try:
            config = json.loads(config_str) if config_str else None
        except Exception:
            config = None

        tdir = os.path.join(temas.TEMAS_DIR, tema)
        fondo_dir = os.path.join(tdir, "calendario")

        # Una plantilla por regla: los meses de 6 filas pueden tener SU propio arte
        # (fondo6.png). Subir la imagen editando una regla NO pisa la de la otra.
        def _fondo_path(f):
            return os.path.join(fondo_dir, "fondo6.png" if int(f) >= 6 else "fondo.png")

        def _cargar_fondo(f):
            p = _fondo_path(f)
            if os.path.isfile(p):
                return Image.open(p).convert("RGBA")
            if int(f) >= 6 and os.path.isfile(_fondo_path(5)):  # sin arte propio → el general
                return Image.open(_fondo_path(5)).convert("RGBA")
            return None

        # plantilla subida en el body (si vino): es la del grupo que se está generando
        subida = None
        try:
            n = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(n) if n else b""
            if raw:
                subida = Image.open(io.BytesIO(raw)).convert("RGBA")
        except Exception as e:
            return self._json(400, {"ok": False, "error": "imagen inválida: %s" % e})

        try:
            import calendario
            os.makedirs(fondo_dir, exist_ok=True)
            override_dir = os.path.join(tdir, "overrides", "calendario")
            os.makedirs(override_dir, exist_ok=True)

            layout = self._cal_load_layout(tema) or {"base": {}, "meses": {}, "anyo": anyo_str}
            layout.setdefault("meses", {})
            anyo_int = int(anyo_str)
            data = {"nombre": nombre, "anyo": anyo_str}

            if filas:  # regla de grupo: todos los meses de 5 (o menos) / 6 filas
                plantilla = subida or _cargar_fondo(filas)
                if plantilla is None:
                    return self._json(400, {"ok": False, "error": "sin plantilla (subí una imagen primero)"})
                if subida:
                    subida.save(_fondo_path(filas))
                grupo = calendario.meses_por_filas(anyo_int, filas)
                clave = "base6" if filas == 6 else "base"
                cfg = config or layout.get(clave) or layout.get("base") or {}
                layout[clave] = cfg
                layout["anyo"] = anyo_str
                # la regla reemplaza los ajustes puntuales de esos meses
                for m in grupo:
                    layout["meses"].pop(str(m), None)
                for m in grupo:
                    img = calendario.generar_mes_con_plantilla(data, plantilla, tema, m, cfg)
                    piezas.to_rgb(img).save(os.path.join(override_dir, "%d.png" % (m - 1)))
                self._cal_save_layout(tema, layout)
                _preview_cache_clear(tema, "calendario")   # sin esto el dash muestra los meses viejos hasta 6h
                _preview_warm(tema, "calendario", [m - 1 for m in grupo])
                return self._json(200, {"ok": True, "tema": tema, "filas": filas,
                                        "meses": grupo, "generados": len(grupo)})

            if mes:  # un solo mes (compat: ajuste puntual, con el fondo de su grupo)
                f_mes = 6 if calendario.filas_del_mes(anyo_int, mes) >= 6 else 5
                plantilla = subida or _cargar_fondo(f_mes)
                if plantilla is None:
                    return self._json(400, {"ok": False, "error": "sin plantilla (subí una imagen primero)"})
                if subida:
                    subida.save(_fondo_path(f_mes))
                cfg = config or calendario.config_para_mes(layout, anyo_int, mes)
                img = calendario.generar_mes_con_plantilla(data, plantilla, tema, mes, cfg)
                piezas.to_rgb(img).save(os.path.join(override_dir, "%d.png" % (mes - 1)))
                layout["meses"][str(mes)] = cfg
                layout["anyo"] = anyo_str
                self._cal_save_layout(tema, layout)
                _preview_cache_clear(tema, "calendario")
                _preview_warm(tema, "calendario", [mes - 1])
                return self._json(200, {"ok": True, "tema": tema, "mes": mes, "generados": 1})

            # los 12: cada mes con su regla y el fondo de su grupo
            plantilla5 = subida or _cargar_fondo(5)
            if plantilla5 is None:
                return self._json(400, {"ok": False, "error": "sin plantilla (subí una imagen primero)"})
            if subida:
                subida.save(_fondo_path(5))
            f6 = _fondo_path(6)
            plantilla6 = Image.open(f6).convert("RGBA") if os.path.isfile(f6) else plantilla5
            base = config or layout.get("base") or {}
            layout["base"] = base
            layout["anyo"] = anyo_str
            generados = []
            for m in range(1, 13):
                cfg = calendario.config_para_mes(layout, anyo_int, m)
                pl = plantilla6 if calendario.filas_del_mes(anyo_int, m) >= 6 else plantilla5
                img = calendario.generar_mes_con_plantilla(data, pl, tema, m, cfg)
                piezas.to_rgb(img).save(os.path.join(override_dir, "%d.png" % (m - 1)))
                generados.append(m)
            self._cal_save_layout(tema, layout)
            _preview_cache_clear(tema, "calendario")
            _preview_warm(tema, "calendario", list(range(12)))
            return self._json(200, {"ok": True, "tema": tema, "anyo": anyo_str,
                                    "generados": len(generados)})
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
                os.remove(path); generador._specs_cache.pop(tema, None); _preview_cache_clear(tema)
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
        generador._specs_cache.pop(tema, None); _preview_cache_clear(tema)   # por si estaba cacheada
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
        generador._specs_cache.pop(tema, None); _preview_cache_clear(tema)
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
        generador._specs_cache.pop(tema, None); _preview_cache_clear(tema)
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

    def _dash_libro_audio_demo(self):
        """Audiolibro DEMO REAL del tema para revisar desde el panel ANTES de publicar:
        genera el libro del catálogo (historia + edad → 12/20 páginas) con el MISMO
        arte por pedido + QA + voz que ve el cliente, así se pueden chequear problemas
        de imágenes. Se cachea por (tema, historia, edad). Params: tema, historia, edad.
        Con ?regen=1 fuerza regenerar (descarta el cacheado)."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        historia = (q.get("historia", ["aventura"])[0] or "aventura").strip().lower()
        edad = re.sub(r"\D", "", q.get("edad", ["5"])[0] or "5") or "5"
        regen = q.get("regen", ["0"])[0] in ("1", "true", "yes")
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        import audiolibro, libro_ia
        marca = os.path.join(temas.TEMAS_DIR, tema,
                             "audiolibro_demo_%s_%s.txt" % (historia, edad))
        if os.path.isfile(marca) and not regen:
            tok = open(marca).read().strip()
            if audiolibro._cargar(tok):
                return self._json(200, {"ok": True,
                                        "url": f"{self.base_url()}/al/{tok}"})
        if not OPENAI_API_KEY:
            return self._json(503, {"ok": False, "error": "falta OPENAI_API_KEY"})

        def trabajo(emit):
            data = {"nombre": "Alex", "edad": edad, "historia": historia,
                    "genero": "nene", "dedicatoria": "Un cuento de muestra"}
            escenas = None
            if historia in libro_ia._ESCENAS_POR_HISTORIA_LARGO:
                client = _openai_client()
                if client is not None:
                    dest = os.path.join(DATA_DIR, "demo-%s-%s-%s" % (tema, historia, edad))
                    escenas = os.path.join(dest, "escenas")
                    os.makedirs(escenas, exist_ok=True)
                    emit("Ilustrando el cuento a medida…")
                    try:
                        libro_ia.generar_ilustraciones(
                            client, tema, dest_dir=escenas, genero="nene",
                            historia=historia, catalogo=True, edad=edad,
                            verificar=True, progress=emit,
                            fallos_log=os.path.join(dest, "qa.txt"))
                    except Exception as e:
                        emit("Arte falló (%s) — uso arte del tema" % e)
                        escenas = None
            emit("Narrando el cuento…")
            tok = audiolibro.crear(data, tema, OPENAI_API_KEY, escenas_dir=escenas,
                                   progress=emit)
            with open(marca, "w") as f:
                f.write(tok)
        jid = ia_jobs.iniciar(trabajo)
        return self._json(200, {"ok": True, "job": jid})

    def _dash_libro_admin(self, u=None):
        """Grilla de TODAS las páginas de un audiolibro generado, con la
        indicación permanente del tema (se inyecta en cada prompt futuro de la
        temática) y regeneración por página que actualiza el CACHE del combo —
        así el arreglo llega a todas las ventas siguientes.
        Params: token (preview-*), tema, historia."""
        if not self._admin_ok(u):
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        token = (q.get("token", [""])[0] or "").strip()
        import audiolibro, libro_ia
        reg = audiolibro._cargar(token)
        if not reg:
            return self._json(404, {"ok": False, "error": "token inválido"})
        tema = slug(q.get("tema", [reg.get("tema") or ""])[0])
        historia = (q.get("historia", [""])[0] or "").strip().lower()
        n = int(reg.get("paginas", 20))
        v = int(reg.get("creado", 0))
        nota = libro_ia.nota_tema(tema)
        esc = html_lib.escape
        cards = "".join(
            '<figure><img src="/al/%s/pag_%02d.jpg?v=%d" loading="lazy" id="im%d">'
            '<figcaption>pág %d'
            '<button onclick="regen(%d)" id="b%d">🔄 Regenerar</button>'
            '</figcaption></figure>' % (esc(token), i, v, i, i + 1, i, i)
            for i in range(n))
        body = ("""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Retocar %(titulo)s</title><style>
*{box-sizing:border-box}body{font-family:system-ui,sans-serif;background:#f5f2fb;margin:0;padding:18px;color:#333}
h1{font-size:1.15rem;margin:0 0 4px}.sub{color:#777;font-size:.85rem;margin:0 0 14px}
textarea{width:100%%;min-height:74px;border:1px solid #cbc3e6;border-radius:10px;padding:10px;font:inherit}
.nota{background:#fff;border-radius:14px;padding:14px;margin-bottom:18px;box-shadow:0 1px 4px #0001}
.nota b{display:block;margin-bottom:6px}.nota .hint{color:#888;font-size:.8rem;margin:6px 0 8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px}
figure{background:#fff;border-radius:12px;padding:8px;margin:0;box-shadow:0 1px 4px #0001}
img{width:100%%;border-radius:8px;display:block}
figcaption{display:flex;justify-content:space-between;align-items:center;padding-top:6px;font-size:.85rem;color:#666}
button{background:#6B5BD2;color:#fff;border:0;border-radius:8px;padding:6px 10px;cursor:pointer;font-weight:700}
button:disabled{opacity:.45;cursor:wait}#msg{min-height:20px;color:#a33;font-size:.85rem;margin-top:8px}
</style></head><body>
<h1>🛠 %(titulo)s — %(n)d páginas</h1>
<p class="sub">Tema <b>%(tema)s</b> · historia <b>%(historia)s</b>. Regenerar una página actualiza también el ARTE CACHEADO del combo: las próximas ventas ya salen con el arreglo.</p>
<div class="nota"><b>📝 Indicación permanente del tema</b>
<div class="hint">Se agrega al prompt de TODAS las ilustraciones futuras de esta temática (todos los libros, todas las historias). Ej.: «el león siempre con la melena prolija», «nunca dibujar sombreros».</div>
<textarea id="nota" placeholder="Escribí acá el arreglo que quieras que se respete siempre…">%(nota)s</textarea>
<div style="margin-top:8px"><button onclick="guardar()">💾 Guardar indicación</button></div>
<div id="msg"></div></div>
<div class="grid">%(cards)s</div>
<script>
var TOKEN=%(token_js)s, TEMA=%(tema_js)s, HIST=%(hist_js)s;
function msg(t){document.getElementById('msg').textContent=t;}
function post(url, params){
  return fetch(url, {method:'POST', credentials:'same-origin',
    headers:{'Content-Type':'application/x-www-form-urlencoded'},
    body:new URLSearchParams(params).toString()}).then(r=>r.json());
}
function guardar(){
  msg('Guardando…');
  post('/dash/libro-nota',{tema:TEMA,nota:document.getElementById('nota').value})
    .then(j=>msg(j.ok?'✅ Indicación guardada — vale para todas las regeneraciones futuras.':('Error: '+j.error)))
    .catch(e=>msg('Error: '+e));
}
function regen(i){
  var b=document.getElementById('b'+i); b.disabled=true; b.textContent='⏳ Generando (~1 min)…';
  msg('');
  post('/dash/libro-regen',{token:TOKEN,tema:TEMA,historia:HIST,idx:i,
        nota:document.getElementById('nota').value})
    .then(function(j){
      b.disabled=false; b.textContent='🔄 Regenerar';
      if(j.ok){ document.getElementById('im'+i).src='/al/'+TOKEN+'/pag_'+String(i).padStart(2,'0')+'.jpg?r='+Date.now(); }
      else msg('Página '+(i+1)+': '+(j.error||'no se pudo regenerar'));
    })
    .catch(function(e){ b.disabled=false; b.textContent='🔄 Regenerar'; msg('Error: '+e); });
}
</script></body></html>""" % {
            "titulo": esc(reg.get("nombre") or token), "n": n, "tema": esc(tema),
            "historia": esc(historia or "—"), "nota": esc(nota), "cards": cards,
            "token_js": json.dumps(token), "tema_js": json.dumps(tema),
            "hist_js": json.dumps(historia)}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _leer_form(self):
        """Body application/x-www-form-urlencoded -> dict de primer valor."""
        try:
            largo = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            largo = 0
        crudo = self.rfile.read(min(largo, 65536)).decode("utf-8", "replace")
        return {k: v[0] for k, v in urllib.parse.parse_qs(crudo).items()}

    def _dash_libro_nota(self):
        """Guarda la indicación permanente del tema (ver libro_ia.nota_tema)."""
        if not self._admin_ok():
            return self._deny()
        import libro_ia
        f = self._leer_form()
        tema = slug(f.get("tema", ""))
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        libro_ia.guardar_nota_tema(tema, f.get("nota", ""))
        return self._json(200, {"ok": True})

    def _dash_libro_regen(self):
        """Regenera UNA página de un libro del catálogo: guarda la indicación
        del tema, genera el arte de nuevo (prompt + indicación + QA), lo deja
        en el CACHE del combo (las ventas siguientes lo reusan) y re-renderiza
        el JPG del libro de muestra. El audio no se toca (el texto no cambió)."""
        if not self._admin_ok():
            return self._deny()
        import audiolibro, libro_ia
        f = self._leer_form()
        token = (f.get("token") or "").strip()
        tema = slug(f.get("tema", ""))
        historia = (f.get("historia") or "").strip().lower()
        reg = audiolibro._cargar(token)
        if not reg or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "token/tema inválido"})
        if historia not in libro_ia._ESCENAS_POR_HISTORIA_LARGO:
            return self._json(400, {"ok": False, "error": "historia inválida"})
        n = int(reg.get("paginas", 20))
        try:
            idx = int(f.get("idx", "-1"))
        except ValueError:
            idx = -1
        if not 0 <= idx < n:
            return self._json(400, {"ok": False, "error": "página inválida"})
        if n < 20:
            return self._json(400, {"ok": False,
                                    "error": "retocá el libro largo (20 págs)"})
        if "nota" in f:
            libro_ia.guardar_nota_tema(tema, f.get("nota", ""))
        client = _openai_client()
        if client is None:
            return self._json(503, {"ok": False, "error": "falta OPENAI_API_KEY"})
        genero = (f.get("genero") or "nene").strip().lower()
        g = libro_ia._genero_arte(genero)
        cache = os.path.join(libro_ia.CATALOGO_ARTE, tema, historia, g)
        os.makedirs(cache, exist_ok=True)
        try:
            hechos = libro_ia.generar_ilustraciones(
                client, tema, paginas=[idx], dest_dir=cache, genero=g,
                historia=historia, catalogo=True, edad="5", verificar=True)
        except Exception as e:
            return self._json(502, {"ok": False, "error": str(e)[:180]})
        if not hechos:
            return self._json(200, {"ok": False,
                                    "error": "el QA rechazó el arte 2 veces — "
                                             "probá de nuevo o ajustá la indicación"})
        import libro as _libro
        data = {"nombre": reg.get("nombre") or "Alex", "edad": "5",
                "historia": historia, "genero": g,
                "dedicatoria": "Un cuento de muestra"}
        with _libro.usar_escenas_dir(cache):
            img = _libro.pagina_libro(idx, data, tema, catalogo=True).convert("RGB")
        img.resize((img.width * 2 // 3, img.height * 2 // 3)).save(
            os.path.join(audiolibro.AUDIOLIBROS_DIR, token, "pag_%02d.jpg" % idx),
            quality=86)
        return self._json(200, {"ok": True})

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

    # Qué arte IA hay detrás de cada pieza de la galería de productos:
    # (tipo, idx) → (módulo, pieza-del-generador). Lo usa el botón ♻ por pieza
    # (pedido de Pablo 8-jul-2026: bajar/subir/regenerar en CADA cosa del tema).
    _FONDO_DE_PIEZA = {
        ("menu", 0): ("fondos", "menu"),
        ("certificado", 0): ("fondos", "certificado"),
        ("capsula", 0): ("fondos", "capsula"),
        ("memoria", 1): ("fondos", "memoria_dorso"),
        ("rompecabezas", 0): ("fondos", "rompecabezas"),
        ("rompecabezas", 1): ("fondos", "rompecabezas"),
        ("corona", 0): ("corona", "gorro"),
        ("corona", 1): ("corona", "corona"),
    }

    def _pieza_regenerar(self):
        """Regenera el arte IA que hay DETRÁS de una pieza puntual de la galería
        (fondo del menú, arte del gorro, imagen del puzzle, página del libro...).
        Job en background + polling /dash/ia-estado, como todo lo demás."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        tipo = q.get("tipo", [""])[0]
        try:
            idx = int(q.get("pieza", ["0"])[0])
        except ValueError:
            idx = 0
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        client = _openai_client()
        if client is None:
            return self._json(503, {"ok": False, "error": "falta OPENAI_API_KEY"})
        calidad = _calidad(q)

        if tipo == "libro":
            def trabajo(emit):
                import libro_ia
                emit("Regenerando la ilustración de la página %d…" % (idx + 1))
                libro_ia.generar_ilustraciones(client, tema, [idx], calidad=calidad,
                                               progress=emit)
                emit("✓ Página lista.")
            return self._json(200, {"ok": True, "job": ia_jobs.iniciar(trabajo)})

        destino = self._FONDO_DE_PIEZA.get((tipo, idx))
        if destino is None:
            return self._json(400, {"ok": False, "error":
                "esta pieza es procedural (no tiene arte IA propio para regenerar)"})
        modulo, pieza_gen = destino

        def trabajo(emit):
            emit("Regenerando el arte de %s…" % pieza_gen)
            if modulo == "fondos":
                import fondos_ia
                fondos_ia.generar(client, tema, pieza_gen, calidad=calidad)
            else:
                import corona_ia
                corona_ia.generar(client, tema, pieza_gen, calidad=calidad)
            emit("✓ Arte nuevo listo.")
        return self._json(200, {"ok": True, "job": ia_jobs.iniciar(trabajo)})

    def _ia_estado(self):
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        jid = q.get("job", [""])[0]
        if not jid:
            # sin job: cuántos hay corriendo — chequear ANTES de reiniciar el
            # servicio (un restart mata los jobs en memoria sin dejar rastro)
            return self._json(200, {"ok": True, "activos": ia_jobs.activos()})
        st = ia_jobs.estado(jid)
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

    def _corona_ia_generar(self):
        """Genera (o regenera) el fondo IA del gorro de un tema — arte de fondo
        únicamente; el nombre/edad los sigue escribiendo el motor encima (ver corona.py/
        corona_ia.py). La corona no usa esto (ver corona_ia.py). En background +
        polling, mismo patrón que ia-generar/ia-regenerar."""
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
        import corona_ia
        def trabajo(emit):
            for pieza in ("gorro",):
                emit("Generando %s…" % pieza)
                corona_ia.generar(client, tema, pieza, calidad=calidad)
            generador._specs_cache.pop(tema, None); _preview_cache_clear(tema)  # tienda refleja el arte nuevo
        jid = ia_jobs.iniciar(trabajo)
        return self._json(200, {"ok": True, "job": jid})

    def _fondos_ia_generar(self):
        """Genera los fondos IA de los productos individuales de un tema (menú,
        certificado, cápsula, dorso del memoria — ver fondos_ia.PIEZAS) + el del
        gorro. INCREMENTAL por default (solo los que faltan); ?todo=1 regenera
        todos. Arte de fondo únicamente: la personalización la escribe siempre
        el motor encima. Background + polling, mismo patrón que ia-generar."""
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
        todo = q.get("todo", ["0"])[0] == "1"
        import fondos_ia, corona_ia
        pend = [p for p in fondos_ia.PIEZAS
                if todo or not os.path.isfile(fondos_ia.fondo_path(tema, p))]
        gorro_falta = todo or not os.path.isfile(corona_ia.fondo_path(tema, "gorro"))
        if not pend and not gorro_falta:
            return self._json(200, {"ok": True, "job": None, "total": 0,
                                    "mensaje": "Ya están todos los fondos. Usá ?todo=1 para rehacerlos."})
        def trabajo(emit):
            for pieza in pend:
                emit("Generando fondo de %s…" % pieza)
                fondos_ia.generar(client, tema, pieza, calidad=calidad)
            if gorro_falta:
                emit("Generando fondo del gorro…")
                corona_ia.generar(client, tema, "gorro", calidad=calidad)
            generador._specs_cache.pop(tema, None); _preview_cache_clear(tema)  # tienda refleja los fondos nuevos
        jid = ia_jobs.iniciar(trabajo)
        return self._json(200, {"ok": True, "job": jid,
                                "total": len(pend) + (1 if gorro_falta else 0)})

    def _armar_tema_pendientes(self, tema):
        """Qué le falta generar a un tema para estar COMPLETO (todo incremental).
        Devuelve dict de etapas con sus conteos — el botón único genera solo esto."""
        import fondos_ia, corona_ia, libro
        edades = temas.cargar_tema(tema).get("edades", [1, 2, 3])
        kit = ia_orq.contar_faltantes(temas.TEMAS_DIR, tema, edades)
        tdir = os.path.join(temas.TEMAS_DIR, tema)
        colorear = []
        for i in range(3):
            nombre = "colorear.png" if i == 0 else "colorear_%d.png" % (i + 1)
            if not any(os.path.isfile(os.path.join(tdir, d, nombre))
                       for d in ("ia_draft", "extras")):
                colorear.append(nombre)
        fondos = [p for p in fondos_ia.PIEZAS
                  if not os.path.isfile(fondos_ia.fondo_path(tema, p))]
        gorro = sum(1 for p in ("gorro", "corona")
                    if not os.path.isfile(corona_ia.fondo_path(tema, p)))
        total_lib = libro.total_paginas(tema)          # 10 legado / 15 temas nuevos
        libro_pags = [i for i in range(total_lib)
                      if not os.path.isfile(libro.override_escena_path(tema, i))]
        # libro desde cero en un tema de formato nuevo → estrena una historia
        # única de la reserva (regla de Pablo: la Nº12, Nº13... sin repetir)
        hist_nueva, hist_agotada = None, False
        if (len(libro_pags) == total_lib and not libro.historia_de_tema(tema)
                and libro.paginas_historia(tema) > libro.PAGINAS_HISTORIA):
            prox = libro.proxima_historia_libre()
            if prox:
                hist_nueva = "%s (la Nº%d)" % (libro.ARGUMENTO_LABELS.get(prox, prox),
                                               libro.numero_historia(prox))
            else:
                hist_agotada = True
        return {"kit": kit, "colorear": len(colorear), "fondos": len(fondos),
                "gorro": gorro, "libro": len(libro_pags),
                "historia_nueva": hist_nueva, "historia_agotada": hist_agotada,
                "_fondos_list": fondos, "_libro_list": libro_pags,
                "edades": edades}

    def _armar_tema(self):
        """BOTÓN ÚNICO (skill armar-kit §17): genera TODO lo que le falte al tema
        con la impronta de su ia_maestra — piezas IA del kit (incremental, crea la
        maestra si no existe), variantes de colorear del cuaderno, fondos IA de los
        productos individuales + gorro, e ilustraciones del libro. Todo lo
        procedural (menú, memoria, puzzle, cubo...) hereda automáticamente los
        personajes/fondos nuevos. ?dry=1 devuelve solo el conteo (para confirmar
        antes de gastar). ?libro=0 saltea el libro (lo más caro)."""
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
        con_libro = q.get("libro", ["1"])[0] != "0"
        pend = self._armar_tema_pendientes(tema)
        if not con_libro or pend["historia_agotada"]:
            # reserva de historias agotada: NO se genera el libro con una repetida
            # — hay que escribir argumentos nuevos primero (skill armar-kit)
            pend["libro"] = 0
        total = pend["kit"] + pend["colorear"] + pend["fondos"] + pend["gorro"] + pend["libro"]
        if q.get("dry", ["0"])[0] == "1":
            return self._json(200, {"ok": True, "dry": True, "total": total, **{
                k: v for k, v in pend.items() if not k.startswith("_")}})
        if total == 0:
            return self._json(200, {"ok": True, "job": None, "total": 0,
                                    "mensaje": "El tema ya está completo."})

        def trabajo(emit):
            import fondos_ia, corona_ia, libro_ia, shutil
            def txt(ev):     # generar_tema emite dicts; el modal genérico quiere texto
                if isinstance(ev, dict):
                    emit("%s%s %s" % (ev.get("pieza", "?"),
                                      (" (edad %s)" % ev["edad"]) if ev.get("edad") not in (None, "") else "",
                                      "✓" if ev.get("ok") else ("reintento…" if ev.get("reintentando") else "✕")))
                else:
                    emit(str(ev))
            if pend["kit"]:
                emit("— Piezas del kit (%d) —" % pend["kit"])
                ia_orq.generar_tema(client, temas.TEMAS_DIR, tema, pend["edades"],
                                    progress=txt, calidad=calidad,
                                    solo_faltantes=True, reusar_maestra=True)
            if pend["colorear"]:
                emit("— Variantes de colorear (%d) —" % pend["colorear"])
                ia_orq.generar_variantes_colorear(client, temas.TEMAS_DIR, tema, n=3,
                                                  calidad=calidad, progress=txt)
                cache = os.path.join(temas.TEMAS_DIR, tema, "actividades_cache")
                if os.path.isdir(cache):
                    shutil.rmtree(cache, ignore_errors=True)
            for pieza in pend["_fondos_list"]:
                emit("— Fondo de %s —" % pieza)
                fondos_ia.generar(client, tema, pieza, calidad=calidad)
            if pend["gorro"]:
                for p in ("gorro", "corona"):
                    if not os.path.isfile(corona_ia.fondo_path(tema, p)):
                        emit("— Fondo del %s —" % p)
                        corona_ia.generar(client, tema, p, calidad=calidad)
            if pend["libro"]:
                if pend["historia_nueva"]:
                    import libro as _libro
                    asig = _libro.asignar_historia_tema(tema)
                    if asig:
                        emit("— Historia nueva del libro: “%s” (la Nº%d) —" % (asig[1], asig[2]))
                emit("— Ilustraciones del libro (%d) —" % pend["libro"])
                libro_ia.generar_ilustraciones(client, tema, pend["_libro_list"],
                                               calidad=calidad, progress=emit)
            if pend["historia_agotada"]:
                emit("✋ Libro NO generado: se agotó la reserva de historias nuevas — "
                     "hay que escribir argumentos nuevos antes de armar más libros "
                     "(así ningún tema repite historia).")
            # precalentar el cuaderno de actividades: la primera apertura después
            # de generar tardaba MUCHO armando el caché en vivo (feedback Pablo)
            try:
                import glob as _glob
                import cuaderno as _cuad
                for ed in pend["edades"]:
                    if not _glob.glob(os.path.join(temas.TEMAS_DIR, tema,
                                                   "actividades_cache", str(ed), "b*.png")):
                        emit("— Precalentando actividades (edad %s) —" % ed)
                        _cuad.base_paginas(tema, ed)
            except Exception as e:
                emit("(precalentado de actividades falló: %s)" % e)
            # refrescar el rompecabezas web de muestra con el arte nuevo del
            # tema (el que abre el botón 🎮 de la tarjeta)
            try:
                import rompecabezas_web as _rw
                emit("— Rompecabezas web de muestra —")
                _rw.crear({"nombre": ""}, tema, token=("demo-" + tema)[:32])
            except Exception as e:
                emit("(rompecabezas de muestra falló: %s)" % e)
            emit("✓ Tema completo. Revisá las piezas en la galería y aprobá el draft.")
        jid = ia_jobs.iniciar(trabajo)
        return self._json(200, {"ok": True, "job": jid, "total": total,
                                "calidad": calidad})

    def _rompe_demo(self):
        """Crea/actualiza el rompecabezas web de MUESTRA del tema (token fijo
        demo-<tema>) y devuelve su URL — lo abre el botón 🎮 de la tarjeta del
        tema (pedido de Pablo 11-jul-2026: poder armar los rompecabezas de
        todos los temas desde el dash). Síncrono: sin IA, tarda segundos."""
        if not self._admin_ok():
            return self._deny()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        tema = slug(q.get("tema", [""])[0])
        if not tema or not temas.existe(tema):
            return self._json(400, {"ok": False, "error": "tema inválido"})
        import rompecabezas_web as rw
        try:
            # [:32] = tope del regex de tokens (un slug de tema larguísimo no
            # debe caer al token aleatorio: el link demo tiene que ser estable)
            tok = rw.crear({"nombre": ""}, tema, token=("demo-" + tema)[:32])
        except Exception as e:
            return self._json(500, {"ok": False, "error": str(e)[:200]})
        return self._json(200, {"ok": True, "token": tok, "url": "/armar/%s/" % tok})

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
            generador._specs_cache.pop(tema, None); _preview_cache_clear(tema)
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
