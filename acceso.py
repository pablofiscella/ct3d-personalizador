#!/usr/bin/env python3
"""Quién sos, para los links que están atados a una persona y no a quien tenga la URL.

POR QUÉ EXISTE
──────────────
19-ago-2026. Los productos web del motor (`/armar/`, `/act/`, `/al/`, `/leer/`) se
entregan como un link con token: **el que tiene la URL, entra**. Para Mercado Libre
alcanzaba —se lo mandamos a una persona por mensaje— pero para Etsy no: ahí el archivo
de entrega lo baja el comprador y lo puede reenviar, subir a un grupo, o revenderlo.

Pedido de Pablo, textual: *«Tiene que haber alguna forma asociada al mail. Si se loguea
en casatridimensional tiene acceso y no otros»* y *«con cuenta de google, no tiene que
crearse una cuenta para casatridimensional»*.

O sea: **el link deja de ser la llave; la llave es el mail**. Quien canjea la compra
entra con Google una vez, y ese mail queda de dueño del token. Después, ese link sólo
abre para ese mail.

LO QUE **NO** HACE, A PROPÓSITO
───────────────────────────────
No toca los tokens que ya existen. Un token sin dueño anotado sigue abriéndose con la
sola URL, como siempre — si no, **se rompen todos los links ya vendidos** en Mercado
Libre, que son los que hoy facturan. El candado es opt-in y se pone al crear el token.

DÓNDE VIVE EL DUEÑO
───────────────────
En `manifest.json`, NO en `data.json`: el `data.json` se lo sirve el motor al navegador
para que el player lo lea, así que cualquier cosa que se escriba ahí es pública. El mail
del comprador es un dato personal y se queda del lado del servidor.

DOS PUERTAS, LA MISMA CERRADURA
───────────────────────────────
1. **La cuenta de la tienda** (`ct3d_cliente`): quien ya compró en
   casatridimensional.com.ar tiene esa cookie, que es del dominio padre y por eso llega
   también a `kit.*`. Se valida acá, entera —firma y vencimiento—, no se mira si existe.
2. **Google** (comprador de Etsy, que no tiene cuenta nuestra): el botón manda un ID
   token, se verifica contra Google, y el motor emite su propia cookie de acceso.

EL SECRETO SE COPIA, NO SE IMPORTA
──────────────────────────────────
La derivación del secreto está copiada de `/opt/ct3d/backend/tienda_auth_cliente.py` a
propósito: regla de arquitectura de Pablo —si dos sistemas necesitan lo mismo, se copia—
y además el motor es un repo aparte que no importa nada del backend. Si allá cambia la
derivación, este archivo deja de validar: por eso `tests/test_acceso.py` compara las dos
implementaciones contra el archivo real.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import json
import os
import time
import urllib.parse
import urllib.request

import jwt as _jwt

# ── la cuenta de la tienda ───────────────────────────────────────────────────
CONFIG_TIENDA = "/opt/ct3d/backend/config.json"
COOKIE_TIENDA = "ct3d_cliente"

# ── la sesión propia del motor (la que emite el login con Google) ────────────
COOKIE_MOTOR = "ct3d_acceso"
COOKIE_DOMINIO = ".casatridimensional.com.ar"
SESION_DIAS = 90

# El cliente OAuth vive en el proyecto «Sitio Casatridimensional». Es PÚBLICO por
# diseño (viaja en el HTML de cualquiera que abra la página): no es un secreto y no
# hace falta protegerlo. El que sí es secreto —el client secret— no se usa acá: el
# flujo es de ID token, que se verifica contra Google sin él.
GOOGLE_CLIENT_ID = os.environ.get(
    "CT3D_GOOGLE_CLIENT_ID",
    "838286795258-mljes9lo4qncdnk5e0m0cpil6glok98t.apps.googleusercontent.com")

GOOGLE_TOKENINFO = "https://oauth2.googleapis.com/tokeninfo?id_token=%s"
GOOGLE_ISS = ("accounts.google.com", "https://accounts.google.com")


def normalizar(email):
    """Los mails se comparan en minúscula y sin espacios. Sin esto, «Ana@Gmail.com»
    en Etsy y «ana@gmail.com» en la cuenta serían dos personas distintas."""
    return (email or "").strip().lower()


# ── 1. la cookie de la tienda ────────────────────────────────────────────────

def _secreto_tienda():
    """Copiado de tienda_auth_cliente._secreto_cliente. Se deriva del session_secret
    en vez de usarlo crudo para que un token de cliente NUNCA sirva como sesión de
    admin — la separación es del backend y acá se respeta igual."""
    with open(CONFIG_TIENDA) as f:
        base = json.load(f)["session_secret"]
    return hmac.new(base.encode(), b"cliente", hashlib.sha256).hexdigest()


def email_de_la_tienda(cookie_header):
    """El mail del cliente logueado en la tienda, o None.

    Valida la firma y el vencimiento de verdad. El resto del motor sólo miraba si la
    cookie ESTABA (`"ct3d_cliente=" in ...`) porque ahí sólo decidía mostrar un banner;
    acá decide un acceso, así que no alcanza."""
    tok = _cookie(cookie_header, COOKIE_TIENDA)
    if not tok:
        return None
    try:
        p = _jwt.decode(tok, _secreto_tienda(), algorithms=["HS256"])
    except Exception:
        return None
    if p.get("tipo") == "reset":      # el token de «olvidé mi contraseña» no es sesión
        return None
    return normalizar(p.get("email"))


# ── 2. Google ────────────────────────────────────────────────────────────────

def email_de_google(id_token, client_id=None, _abrir=None):
    """El mail verificado por Google, o None si el token no sirve.

    Se verifica contra Google (`tokeninfo`) en vez de validar la firma con las claves
    públicas a mano: es un login, pasa una vez por comprador, y el código que no se
    escribe no tiene agujeros. Google ya chequea firma y vencimiento; lo que Google NO
    puede saber es si el token era **para nosotros**, así que el `aud` se compara acá
    —sin eso, un ID token emitido para CUALQUIER otra app entraría igual."""
    if not id_token or not isinstance(id_token, str) or len(id_token) > 8192:
        return None
    cid = client_id or GOOGLE_CLIENT_ID
    abrir = _abrir or (lambda u: urllib.request.urlopen(u, timeout=10).read())
    try:
        raw = abrir(GOOGLE_TOKENINFO % urllib.parse.quote(id_token, safe=""))
        d = json.loads(raw)
    except Exception:
        return None
    if d.get("aud") != cid:                       # emitido para otra app
        return None
    if d.get("iss") not in GOOGLE_ISS:
        return None
    if str(d.get("email_verified", "")).lower() not in ("true", "1"):
        return None
    try:
        if int(d.get("exp", 0)) <= int(time.time()):
            return None
    except (TypeError, ValueError):
        return None
    return normalizar(d.get("email"))


# ── 3. la sesión propia del motor ────────────────────────────────────────────

def _secreto_motor():
    """Otra derivación más del mismo secreto: una cookie de acceso del motor no tiene
    que servir como sesión de cliente de la tienda ni como sesión de admin."""
    with open(CONFIG_TIENDA) as f:
        base = json.load(f)["session_secret"]
    return hmac.new(base.encode(), b"motor-acceso", hashlib.sha256).hexdigest()


def sesion_crear(email, dias=SESION_DIAS):
    now = dt.datetime.now(dt.timezone.utc)
    return _jwt.encode({"email": normalizar(email), "iat": int(now.timestamp()),
                        "exp": int((now + dt.timedelta(days=dias)).timestamp())},
                       _secreto_motor(), algorithm="HS256")


def email_de_la_sesion(cookie_header):
    tok = _cookie(cookie_header, COOKIE_MOTOR)
    if not tok:
        return None
    try:
        return normalizar(_jwt.decode(tok, _secreto_motor(),
                                      algorithms=["HS256"]).get("email"))
    except Exception:
        return None


def cookie_set(token, dias=SESION_DIAS):
    """El valor del header Set-Cookie. HttpOnly para que el JS no la pueda leer;
    SameSite=Lax porque el link llega de un mail o del PDF de Etsy (navegación de
    primer nivel, que Lax sí permite)."""
    return ("%s=%s; Path=/; Max-Age=%d; HttpOnly; Secure; SameSite=Lax; Domain=%s"
            % (COOKIE_MOTOR, token, dias * 86400, COOKIE_DOMINIO))


def quien_es(cookie_header):
    """El mail de quien está mirando, por cualquiera de las dos puertas."""
    return email_de_la_sesion(cookie_header) or email_de_la_tienda(cookie_header)


# ── 4. el candado del token ──────────────────────────────────────────────────

def dueño_de(manifest):
    """El mail dueño del token, o None si el token no tiene candado.

    None es la respuesta correcta —y no un error— para los cientos de tokens creados
    antes de que esto existiera: sin dueño anotado, el link sigue siendo la llave."""
    if not isinstance(manifest, dict):
        return None
    return normalizar(manifest.get("dueño")) or None


def puede_abrir(manifest, cookie_header):
    """(ok, dueño). `ok` es True si el token no tiene candado, o si quien mira es el
    dueño. Se devuelve también el dueño para que la página de login pueda decir a qué
    cuenta pertenece — sin mostrar el mail entero."""
    d = dueño_de(manifest)
    if not d:
        return True, None
    return (quien_es(cookie_header) == d), d


def pista_de_mail(email):
    """«ana@gmail.com» → «a•••@gmail.com». Para que el dueño reconozca su cuenta sin
    publicarle el mail a quien haya conseguido el link."""
    e = normalizar(email)
    if "@" not in e:
        return ""
    u, dom = e.split("@", 1)
    return "%s%s@%s" % (u[:1], "•" * max(3, len(u) - 1), dom)


# ── utilidades ───────────────────────────────────────────────────────────────

def _cookie(header, nombre):
    """Una cookie del header, sin usar http.cookies: los valores JWT llevan puntos y
    guiones y no necesitan parseo especial, y así no hay sorpresas con cookies mal
    formadas de otro dominio."""
    for parte in (header or "").split(";"):
        parte = parte.strip()
        if parte.startswith(nombre + "="):
            return parte[len(nombre) + 1:].strip()
    return None


# ── 5. la página de login ────────────────────────────────────────────────────

BASEDIR = os.path.dirname(os.path.abspath(__file__))
LOGIN_HTML = os.path.join(BASEDIR, "acceso_login.html")

# El texto va en los dos idiomas por la misma razón que el player: el comprador de Etsy
# es de habla inglesa y el de Mercado Libre no. Se traduce a mano acá —y no con
# `idioma.py`— porque son frases de la PUERTA, no del producto: no se imprimen en
# ninguna pieza, así que no tienen por qué estar en la tabla que audita el guardián
# del kit (meterlas ahí ensuciaría un inventario que hoy dice la verdad).
TEXTOS = {
    "es": {
        "titulo": "Entrá con tu cuenta",
        "h1": "Este link es tuyo",
        "bajada": ("Para abrirlo, entrá con la cuenta de Google que usaste al comprar. "
                   "No hace falta crear ninguna cuenta nueva."),
        "cuenta": "Este link es de la cuenta %s",
        "aviso": ("Sólo usamos tu mail para reconocerte. Si entrás con otra cuenta, "
                  "no vas a poder abrirlo."),
        "error": "No pudimos verificar tu cuenta. Probá de nuevo.",
    },
    "en": {
        "titulo": "Sign in to open",
        "h1": "This link is yours",
        "bajada": ("Sign in with the Google account you used to buy it. "
                   "You don't need to create an account with us."),
        "cuenta": "This link belongs to %s",
        "aviso": ("We only use your email to recognise you. Signing in with a different "
                  "account won't open it."),
        "error": "We couldn't verify your account. Please try again.",
    },
}


def _esc(t):
    """Escapa para HTML **y** para el string de JavaScript: los mismos valores se
    interpolan en los dos lugares. Sin las comillas y la barra invertida, un `volver`
    armado a mano podría cerrar el string y meter código en la página."""
    return (str(t).replace("&", "&amp;").replace("\\", "\\\\").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;"))


def _volver_seguro(volver):
    """Sólo rutas de este sitio. Un `volver` con `http://otro.com` convertiría esta
    página en un redirector abierto: se entra con Google acá y se sale disparado a
    cualquier lado, con la confianza de nuestro dominio puesta. La regla es a
    propósito tosca — una barra, y no dos."""
    v = (volver or "/").strip()
    if not v.startswith("/") or v.startswith("//") or "\\" in v:
        return "/"
    return v


def pagina_login(volver="/", lang="es", dueño=None, client_id=None):
    """El HTML de la puerta. Se lee del repo en cada pedido, igual que los players: así
    una mejora llega también a los links ya vendidos."""
    lang = "en" if lang == "en" else "es"
    t = TEXTOS[lang]
    with open(LOGIN_HTML, encoding="utf-8") as f:
        html = f.read()
    cuenta = ""
    if dueño:
        cuenta = ('<div class="cuenta">%s</div>'
                  % _esc(t["cuenta"] % pista_de_mail(dueño)))
    for k, v in {
        "{{LANG}}": lang,
        "{{TITULO}}": _esc(t["titulo"]),
        "{{H1}}": _esc(t["h1"]),
        "{{BAJADA}}": _esc(t["bajada"]),
        "{{CUENTA}}": cuenta,
        "{{AVISO}}": _esc(t["aviso"]),
        "{{TXT_ERROR}}": _esc(t["error"]),
        "{{CLIENT_ID}}": _esc(client_id or GOOGLE_CLIENT_ID),
        "{{VOLVER}}": _esc(_volver_seguro(volver)),
    }.items():
        html = html.replace(k, v)
    return html
