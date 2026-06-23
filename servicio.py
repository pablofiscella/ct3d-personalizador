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
import os, io, json, re, secrets, urllib.parse, urllib.request, urllib.error, base64
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
ADMIN_COOKIE = "ct3d_tok"

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

class Handler(BaseHTTPRequestHandler):
    server_version = "CT3D-Kit/1.0"

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print("[svc]", self.address_string(), fmt % args)

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
        # 1) cookie ct3d_tok
        for part in self.headers.get("Cookie", "").split(";"):
            if "=" in part:
                k, v = part.strip().split("=", 1)
                if k == ADMIN_COOKIE and secrets.compare_digest(v, API_KEY):
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
        """Set-Cookie para dejar el token guardado tras entrar con ?key=.
        httpOnly+Secure+SameSite=Lax, 30 días. Host-only (solo kit lo lee)."""
        return ("%s=%s; Path=/; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax"
                % (ADMIN_COOKIE, API_KEY))

    # ---------------- GET ----------------
    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        path = u.path
        if path == "/health":
            return self._json(200, {"ok": True, "servicio": "kit-anito-salvaje"})
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
            try: size = max(0.02, min(0.09, float(q.get("size", ["0.058"])[0])))
            except Exception: size = 0.058
            try: mx = max(300, min(1100, int(q.get("max", ["900"])[0])))
            except Exception: mx = 900
            img = mate_mod.render(texto, mate_id, font=font, size_frac=size, max_px=mx)
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
            im = piezas.marca_agua(Image.open(bp).convert("RGB"))   # con marca de agua (protege el asset)
            buf = io.BytesIO(); im.save(buf, "PNG"); data = buf.getvalue()
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
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
                try: nombre = slug(json.load(open(meta_path))["data"]["nombre"])
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
        if self.headers.get("X-API-Key") != API_KEY:
            return self._json(401, {"ok": False, "error": "API key inválida"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n) or b"{}")
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
        token = f"{order_id}-{secrets.token_hex(4)}"
        dest = os.path.join(DATA_DIR, token)
        try:
            productos.generar(data, dest, tema, tipo)
            with open(os.path.join(dest, "meta.json"), "w", encoding="utf-8") as f:
                json.dump({"order_id": payload.get("order_id"), "email": payload.get("email"),
                           "tema": tema, "tipo": tipo, "data": data}, f, ensure_ascii=False, indent=2)
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
