# Cuenta de cliente + "Mis compras" Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** que un cliente que compra un producto digital personalizado pueda
crear una cuenta (email + contraseña) en el checkout, y después entrar a la
tienda para ver/volver a descargar o reproducir todo lo que compró, para
siempre.

**Architecture:** todo vive en la tienda (`/opt/ct3d/backend`, Flask +
SQLite `facturas_ml.db`). Dos módulos nuevos siguiendo patrones ya
existentes en el repo: `tienda_clientes.py` (tabla + CRUD de cuentas, mismo
estilo que `tienda_checkout.py`) y `tienda_auth_cliente.py` (cookie de
sesión JWT firmada, mismo patrón que el `auth.py` de admin pero separado —
otra cookie, sin whitelist). El checkout gana un campo de contraseña; una
página nueva `/mi-cuenta` lista las compras pagas de ese email reusando el
link (`kit_download_url`) que la orden YA guarda desde siempre. El único
cambio en `ct3d-personalizador` (el servicio de generación) es dejar de
borrar automáticamente los archivos digitales — así esos links no mueren.

**Tech Stack:** Flask, SQLite (`facturas_ml.db`), PyJWT (`jwt`, ya
instalado — usado por `auth.py`), `werkzeug.security` (ya viene con
Flask) para hashear contraseñas.

## Global Constraints

- Alcance: SOLO productos digitales personalizados (todo lo que tiene
  `ml_id` con prefijo `KIT-`). Los pedidos físicos no crean cuenta ni
  aparecen en "Mis compras".
- No se migran pedidos anteriores al lanzamiento de esta feature.
- "Mis compras" es de solo lectura en esta versión: ver + descargar/
  reproducir. Nada de editar/regenerar desde la cuenta.
- Retención de archivos digitales: para siempre (en la práctica, extender
  los umbrales de borrado automático a 7300 días = ~20 años).
- Contraseñas SIEMPRE hasheadas con `werkzeug.security.generate_password_hash`
  — nunca texto plano en la base.
- Cookie de sesión de cliente: HttpOnly + Secure (fuera de localhost) +
  SameSite=Lax, firmada con el MISMO secreto que ya usa `auth.py`
  (`config.json::session_secret` — no se crea uno nuevo).
- La cuenta de cliente es un sistema separado del login de admin
  (`auth.py`): cookie distinta (`ct3d_cliente` vs `ct3d_session`), sin
  whitelist de emails.
- Nunca revelar por el flujo de "olvidé mi contraseña" si un email tiene
  o no cuenta (mismo mensaje en ambos casos).

---

### Task 1: Tabla `tienda_clientes` + módulo `tienda_clientes.py`

**Files:**
- Modify: `/opt/ct3d/backend/tienda_db.py` (agregar tabla al `_SCHEMA`)
- Create: `/opt/ct3d/backend/tienda_clientes.py`
- Test: `/opt/ct3d/backend/tests/test_tienda_clientes.py`

**Interfaces:**
- Produces: `tienda_clientes.existe(email, db_path=DB_PATH) -> bool`,
  `tienda_clientes.verificar(email, password, db_path=DB_PATH) -> bool`,
  `tienda_clientes.crear_o_verificar(email, password, db_path=DB_PATH) -> bool`
  (True si la cuenta es nueva-y-se-creó O si ya existía y la contraseña
  coincide; False si ya existía y la contraseña NO coincide),
  `tienda_clientes.set_password(email, password, db_path=DB_PATH) -> None`,
  `tienda_clientes.listar_compras(email, db_path=DB_PATH) -> list[dict]`
  (cada dict: `{"order_id": str, "pagado_en": str, "items": list[dict],
  "kit_download_url": str}`).
- Consumes: `tienda_db.DB_PATH`, `tienda_db.init_db` (para crear el
  schema en tests); `tienda_catalogo.es_digital(ml_id) -> bool` (ya
  existe, `tienda_catalogo.py:103-104`).

- [ ] **Step 1: Agregar la tabla al schema**

Editar `/opt/ct3d/backend/tienda_db.py`. En el string `_SCHEMA`, agregar
esta tabla nueva DESPUÉS de `tienda_reviews` (al final del bloque
`_SCHEMA`, antes de la comilla de cierre `"""`):

```sql
CREATE TABLE IF NOT EXISTS tienda_clientes (
  email         TEXT PRIMARY KEY,
  password_hash TEXT NOT NULL,
  creado_en     TEXT DEFAULT (datetime('now','localtime'))
);
```

- [ ] **Step 2: Escribir el test de la tabla + `existe`/`verificar`/`crear_o_verificar`**

Crear `/opt/ct3d/backend/tests/test_tienda_clientes.py`:

```python
import sqlite3, sys, importlib

def _prep(tmp_path):
    db_path = str(tmp_path / "test.db")
    # tienda_db.init_db() asume que `productos` ya existe (la crea otro
    # módulo, facturas_api.py, en producción) — acá se crea una versión
    # mínima antes, o init_db falla con "no such table: productos".
    con = sqlite3.connect(db_path)
    con.execute("CREATE TABLE productos (ml_id TEXT PRIMARY KEY, titulo TEXT, "
               "precio_ml REAL, status TEXT)")
    con.commit(); con.close()
    sys.modules.pop("tienda_db", None)
    sys.modules.pop("tienda_clientes", None)
    import tienda_db
    tienda_db.init_db(db_path)
    import tienda_clientes
    importlib.reload(tienda_clientes)
    return tienda_clientes, db_path


def test_crear_o_verificar_cuenta_nueva(tmp_path):
    tc, db = _prep(tmp_path)
    assert tc.crear_o_verificar("ana@test.com", "clave123", db) is True
    assert tc.existe("ana@test.com", db) is True
    # el email se normaliza a minúsculas
    assert tc.existe("ANA@TEST.COM", db) is True


def test_crear_o_verificar_cuenta_existente_password_correcta(tmp_path):
    tc, db = _prep(tmp_path)
    tc.crear_o_verificar("ana@test.com", "clave123", db)
    assert tc.crear_o_verificar("ana@test.com", "clave123", db) is True


def test_crear_o_verificar_cuenta_existente_password_incorrecta(tmp_path):
    tc, db = _prep(tmp_path)
    tc.crear_o_verificar("ana@test.com", "clave123", db)
    assert tc.crear_o_verificar("ana@test.com", "otra-clave", db) is False


def test_verificar_email_inexistente(tmp_path):
    tc, db = _prep(tmp_path)
    assert tc.verificar("nadie@test.com", "cualquiera", db) is False
    assert tc.existe("nadie@test.com", db) is False


def test_password_queda_hasheada_no_texto_plano(tmp_path):
    tc, db = _prep(tmp_path)
    tc.crear_o_verificar("ana@test.com", "clave123", db)
    con = sqlite3.connect(db)
    row = con.execute("SELECT password_hash FROM tienda_clientes WHERE email=?",
                      ("ana@test.com",)).fetchone()
    con.close()
    assert row[0] != "clave123"
    assert row[0].startswith(("pbkdf2:", "scrypt:"))


def test_set_password_cambia_la_clave(tmp_path):
    tc, db = _prep(tmp_path)
    tc.crear_o_verificar("ana@test.com", "vieja123", db)
    tc.set_password("ana@test.com", "nueva456", db)
    assert tc.verificar("ana@test.com", "vieja123", db) is False
    assert tc.verificar("ana@test.com", "nueva456", db) is True
```

- [ ] **Step 3: Correr el test — debe fallar (falta `tienda_clientes.py`)**

Run: `cd /opt/ct3d/backend && python3 -m pytest tests/test_tienda_clientes.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'tienda_clientes'`

- [ ] **Step 4: Crear `tienda_clientes.py`**

```python
"""tienda_clientes.py — cuentas de cliente (email + contraseña), creadas en
el checkout para que después puedan entrar a `/mi-cuenta` y ver todo lo que
compraron. Contraseñas SIEMPRE hasheadas (werkzeug.security) — nunca texto
plano. Separado de tienda_orders: el email ahí sigue siendo texto libre por
pedido, acá es la identidad de la cuenta."""
import json
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

import tienda_catalogo as cat

DB_PATH = "/opt/ct3d/backend/facturas_ml.db"


def _connect(db_path):
    con = sqlite3.connect(db_path, timeout=10)
    con.row_factory = sqlite3.Row
    return con


def _norm(email):
    return (email or "").strip().lower()


def existe(email, db_path=DB_PATH):
    email = _norm(email)
    con = _connect(db_path)
    try:
        return con.execute("SELECT 1 FROM tienda_clientes WHERE email=?",
                           (email,)).fetchone() is not None
    finally:
        con.close()


def verificar(email, password, db_path=DB_PATH):
    email = _norm(email)
    con = _connect(db_path)
    try:
        row = con.execute("SELECT password_hash FROM tienda_clientes WHERE email=?",
                          (email,)).fetchone()
        return bool(row) and check_password_hash(row["password_hash"], password or "")
    finally:
        con.close()


def crear_o_verificar(email, password, db_path=DB_PATH):
    """Usado en el checkout: si el email es nuevo, crea la cuenta con esta
    contraseña (True). Si ya existe, valida la contraseña (True si coincide,
    False si no — el checkout no debe seguir en ese caso)."""
    email = _norm(email)
    if not existe(email, db_path):
        con = _connect(db_path)
        try:
            con.execute("INSERT INTO tienda_clientes (email, password_hash) VALUES (?,?)",
                        (email, generate_password_hash(password or "")))
            con.commit()
        finally:
            con.close()
        return True
    return verificar(email, password, db_path)


def set_password(email, password, db_path=DB_PATH):
    email = _norm(email)
    con = _connect(db_path)
    try:
        con.execute("UPDATE tienda_clientes SET password_hash=? WHERE email=?",
                    (generate_password_hash(password or ""), email))
        con.commit()
    finally:
        con.close()


def listar_compras(email, db_path=DB_PATH):
    """Compras digitales pagas de este email, más nuevas primero. De cada
    orden se queda solo con los ítems digital-personalizados (por si hay una
    orden mixta) y descarta las que no tengan link (generación falló)."""
    email = _norm(email)
    con = _connect(db_path)
    try:
        filas = con.execute(
            "SELECT order_id, items_json, pagado_en, kit_download_url FROM tienda_orders "
            "WHERE email=? AND estado='pagada' ORDER BY pagado_en DESC", (email,)).fetchall()
    finally:
        con.close()
    compras = []
    for f in filas:
        items = [it for it in json.loads(f["items_json"] or "[]")
                 if cat.es_digital(it.get("ml_id"))]
        if not items or not f["kit_download_url"]:
            continue
        compras.append({"order_id": f["order_id"], "pagado_en": f["pagado_en"],
                        "items": items, "kit_download_url": f["kit_download_url"]})
    return compras
```

- [ ] **Step 5: Correr el test de nuevo — debe pasar**

Run: `cd /opt/ct3d/backend && python3 -m pytest tests/test_tienda_clientes.py -v`
Expected: `6 passed`

- [ ] **Step 6: Escribir y correr el test de `listar_compras`**

Agregar a `tests/test_tienda_clientes.py`:

```python
def _crear_orden_pagada(db, order_id, email, items, kit_url):
    con = sqlite3.connect(db)
    con.execute(
        """INSERT INTO tienda_orders (order_id, estado, items_json, subtotal, total,
           email, pagado_en, kit_download_url)
           VALUES (?,?,?,?,?,?,datetime('now'),?)""",
        (order_id, "pagada", __import__("json").dumps(items), 9000, 9000,
         email, kit_url))
    con.commit(); con.close()


def test_listar_compras_solo_del_email_y_solo_digitales(tmp_path):
    tc, db = _prep(tmp_path)
    _crear_orden_pagada(db, "TND-1", "ana@test.com",
                        [{"ml_id": "KIT-LIBRO-SAFARI", "titulo": "Libro Safari", "qty": 1}],
                        "https://kit.casatridimensional.com.ar/descarga/tok1")
    _crear_orden_pagada(db, "TND-2", "otro@test.com",
                        [{"ml_id": "KIT-LIBRO-CIRCO", "titulo": "Libro Circo", "qty": 1}],
                        "https://kit.casatridimensional.com.ar/descarga/tok2")
    _crear_orden_pagada(db, "TND-3", "ana@test.com",
                        [{"ml_id": "LASER-MATE", "titulo": "Mate grabado", "qty": 1}], "")
    compras = tc.listar_compras("ana@test.com", db)
    assert len(compras) == 1
    assert compras[0]["order_id"] == "TND-1"
    assert compras[0]["kit_download_url"] == "https://kit.casatridimensional.com.ar/descarga/tok1"
```

Run: `cd /opt/ct3d/backend && python3 -m pytest tests/test_tienda_clientes.py -v`
Expected: `7 passed`

- [ ] **Step 7: Commit**

```bash
cd /opt/ct3d/backend
git add tienda_db.py tienda_clientes.py tests/test_tienda_clientes.py
git commit -m "feat: tabla y CRUD de cuentas de cliente (tienda_clientes)"
```

---

### Task 2: Sesión de cliente — `tienda_auth_cliente.py`

**Files:**
- Create: `/opt/ct3d/backend/tienda_auth_cliente.py`
- Test: `/opt/ct3d/backend/tests/test_tienda_auth_cliente.py`

**Interfaces:**
- Consumes: nada de Task 1 directamente (módulo independiente); lee
  `config.json::session_secret` (ya existe, mismo valor que usa
  `auth.py`).
- Produces: `tienda_auth_cliente.current_cliente() -> str|None` (requiere
  contexto de request Flask), `tienda_auth_cliente.set_session_cookie(resp, email) -> None`,
  `tienda_auth_cliente.clear_session_cookie(resp) -> None`,
  `tienda_auth_cliente.crear_token_reset(email) -> str`,
  `tienda_auth_cliente.verificar_token_reset(token) -> str|None`.
  Task 3 y Task 4 usan `current_cliente`/`set_session_cookie`/
  `clear_session_cookie`. Task 5 usa `crear_token_reset`/
  `verificar_token_reset`.

- [ ] **Step 1: Escribir el test (usando una app Flask mínima de prueba)**

Crear `/opt/ct3d/backend/tests/test_tienda_auth_cliente.py`:

```python
import json, sys, importlib
from flask import Flask, make_response


def _prep(tmp_path):
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({"session_secret": "test-secret-not-real"}))
    sys.modules.pop("tienda_auth_cliente", None)
    import tienda_auth_cliente as tac
    importlib.reload(tac)
    tac.CONFIG_PATH = str(cfg_path)
    app = Flask(__name__)
    return tac, app


def test_set_y_leer_cookie_de_sesion(tmp_path):
    tac, app = _prep(tmp_path)
    with app.test_request_context("/"):
        resp = make_response("ok")
        tac.set_session_cookie(resp, "ana@test.com")
        cookie_header = resp.headers["Set-Cookie"]
        assert tac.COOKIE_NAME in cookie_header
        assert "HttpOnly" in cookie_header

    # simular que el navegador manda esa cookie en el próximo request
    token = resp.headers["Set-Cookie"].split(f"{tac.COOKIE_NAME}=")[1].split(";")[0]
    with app.test_request_context("/", headers={"Cookie": f"{tac.COOKIE_NAME}={token}"}):
        assert tac.current_cliente() == "ana@test.com"


def test_sin_cookie_no_hay_sesion(tmp_path):
    tac, app = _prep(tmp_path)
    with app.test_request_context("/"):
        assert tac.current_cliente() is None


def test_cookie_invalida_no_rompe(tmp_path):
    tac, app = _prep(tmp_path)
    with app.test_request_context("/", headers={"Cookie": f"{tac.COOKIE_NAME}=basura-no-es-jwt"}):
        assert tac.current_cliente() is None


def test_clear_session_cookie_la_vacia(tmp_path):
    tac, app = _prep(tmp_path)
    with app.test_request_context("/"):
        resp = make_response("ok")
        tac.clear_session_cookie(resp)
        cookie_header = resp.headers["Set-Cookie"]
        assert f'{tac.COOKIE_NAME}=;' in cookie_header or f'{tac.COOKIE_NAME}="";' in cookie_header


def test_token_reset_valido_y_de_un_solo_proposito(tmp_path):
    tac, app = _prep(tmp_path)
    with app.test_request_context("/"):
        token = tac.crear_token_reset("ana@test.com")
        assert tac.verificar_token_reset(token) == "ana@test.com"
        # un token de sesión normal (creado por set_session_cookie) NO debe
        # servir como token de reset
        resp = make_response("ok")
        tac.set_session_cookie(resp, "ana@test.com")
        sesion_token = resp.headers["Set-Cookie"].split(f"{tac.COOKIE_NAME}=")[1].split(";")[0]
        assert tac.verificar_token_reset(sesion_token) is None


def test_token_reset_basura_devuelve_none(tmp_path):
    tac, app = _prep(tmp_path)
    with app.test_request_context("/"):
        assert tac.verificar_token_reset("no-es-un-jwt") is None
```

- [ ] **Step 2: Correr — debe fallar (falta el módulo)**

Run: `cd /opt/ct3d/backend && python3 -m pytest tests/test_tienda_auth_cliente.py -v`
Expected: FAIL con `ModuleNotFoundError: No module named 'tienda_auth_cliente'`

- [ ] **Step 3: Crear `tienda_auth_cliente.py`**

```python
"""tienda_auth_cliente.py — sesión de cliente de la tienda (cuenta creada en
el checkout, ver tienda_clientes.py). Cookie HttpOnly firmada (JWT propio),
MISMO secreto de firma que auth.py (config.json::session_secret) pero cookie
y payload propios — es un sistema separado del login de admin, sin
whitelist de emails."""
from __future__ import annotations

import datetime as dt
import json

import jwt as _jwt
from flask import request

CONFIG_PATH = "/opt/ct3d/backend/config.json"
COOKIE_NAME = "ct3d_cliente"
COOKIE_DOMAIN = ".casatridimensional.com.ar"
SESSION_DIAS = 90
RESET_HORAS = 1


def _cfg() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


def _token(email: str, exp_delta: dt.timedelta, extra: dict | None = None) -> str:
    cfg = _cfg()
    now = dt.datetime.now(dt.timezone.utc)
    payload = {"email": email, "iat": int(now.timestamp()),
               "exp": int((now + exp_delta).timestamp())}
    if extra:
        payload.update(extra)
    return _jwt.encode(payload, cfg["session_secret"], algorithm="HS256")


def _verificar(token):
    if not token:
        return None
    try:
        cfg = _cfg()
        return _jwt.decode(token, cfg["session_secret"], algorithms=["HS256"])
    except Exception:
        return None


def current_cliente():
    payload = _verificar(request.cookies.get(COOKIE_NAME))
    return payload.get("email") if payload else None


def _cookie_kwargs(value, max_age):
    host = (request.host or "").split(":")[0]
    use_domain = host.endswith("casatridimensional.com.ar")
    kwargs = dict(key=COOKIE_NAME, value=value, max_age=max_age,
                  httponly=True, samesite="Lax", path="/")
    if use_domain:
        kwargs["domain"] = COOKIE_DOMAIN
        kwargs["secure"] = True
    return kwargs


def set_session_cookie(resp, email):
    token = _token(email, dt.timedelta(days=SESSION_DIAS))
    resp.set_cookie(**_cookie_kwargs(token, SESSION_DIAS * 24 * 3600))


def clear_session_cookie(resp):
    resp.set_cookie(**_cookie_kwargs("", 0))


def crear_token_reset(email):
    return _token(email, dt.timedelta(hours=RESET_HORAS), extra={"tipo": "reset"})


def verificar_token_reset(token):
    payload = _verificar(token)
    if not payload or payload.get("tipo") != "reset":
        return None
    return payload.get("email")
```

- [ ] **Step 4: Correr de nuevo — debe pasar**

Run: `cd /opt/ct3d/backend && python3 -m pytest tests/test_tienda_auth_cliente.py -v`
Expected: `6 passed`

- [ ] **Step 5: Commit**

```bash
cd /opt/ct3d/backend
git add tienda_auth_cliente.py tests/test_tienda_auth_cliente.py
git commit -m "feat: sesión de cliente (cookie JWT), separada del login de admin"
```

---

### Task 3: Checkout crea/loguea la cuenta

**Files:**
- Modify: `/opt/ct3d/backend/tienda.py:1-25` (imports), `:438-494` (rutas
  `/checkout` GET y POST)
- Modify: `/opt/ct3d/backend/tienda_templates/checkout.html:12-33` (form
  digital — agregar campo contraseña + mensaje de error)
- Test: `/opt/ct3d/backend/tests/test_checkout_password.py`

**Interfaces:**
- Consumes: `tienda_clientes.crear_o_verificar` (Task 1),
  `tienda_auth_cliente.set_session_cookie` (Task 2).
- Produces: nada nuevo para otras tasks — este es el punto de entrada
  donde se crea la cuenta.

- [ ] **Step 1: Agregar el campo de contraseña al form digital**

En `/opt/ct3d/backend/tienda_templates/checkout.html`, dentro del PRIMER
`<form class="checkout" method="post" action="/checkout">` (el del bloque
`{% if digital %}`, alrededor de la línea 12-33), reemplazar:

```html
          <label class="field">
            <span class="field__label">WhatsApp</span>
            <input name="telefono" placeholder="11 5555 5555" required>
          </label>
        </div>
      </section>
```

por:

```html
          <label class="field">
            <span class="field__label">WhatsApp</span>
            <input name="telefono" placeholder="11 5555 5555" required>
          </label>
          <label class="field">
            <span class="field__label">Contraseña (para volver a ver tus compras)</span>
            <input name="password" type="password" minlength="6" placeholder="Elegí una contraseña" required>
          </label>
        </div>
        {% if error_password %}<p class="hint" style="color:#c0392b">{{ error_password }}</p>{% endif %}
      </section>
```

(Solo en el form digital — el form físico, más abajo en el mismo archivo,
no se toca: los pedidos físicos no crean cuenta.)

- [ ] **Step 2: Escribir el test del checkout con contraseña**

Crear `/opt/ct3d/backend/tests/test_checkout_password.py`:

```python
import json, sqlite3, sys, importlib


def _prep(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test.db")
    # tienda_db.init_db() asume que `productos` ya existe (la crea otro
    # módulo, facturas_api.py, en producción) — acá se crea una versión
    # mínima antes, o init_db falla con "no such table: productos".
    con = sqlite3.connect(db_path)
    con.execute("CREATE TABLE productos (ml_id TEXT PRIMARY KEY, titulo TEXT, "
               "precio_ml REAL, status TEXT)")
    con.commit(); con.close()
    for mod in ("tienda_db", "tienda_clientes", "tienda_auth_cliente", "tienda"):
        sys.modules.pop(mod, None)
    import tienda_db
    tienda_db.init_db(db_path)
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({"session_secret": "test-secret-not-real"}))

    import tienda_auth_cliente as tac
    importlib.reload(tac)
    tac.CONFIG_PATH = str(cfg_path)

    import tienda
    importlib.reload(tienda)
    tienda.DB_PATH = db_path
    tienda.tienda_clientes.DB_PATH = db_path

    # cart digital ya cargado, sin pasar por tienda_carrito.agregar. Igual
    # hace falta una fila real en `productos`: chk.crear_orden() revalida
    # cada ítem contra esa tabla (precio/vendible) antes de crear la orden
    # — sin la fila, el ítem se descarta como "no vendible" y la orden
    # queda vacía.
    con = sqlite3.connect(db_path)
    con.execute("INSERT INTO productos (ml_id, titulo, precio_ml, status, mostrar_en_tienda) "
               "VALUES ('KIT-LIBRO-SAFARI', 'Libro Safari', 9000, 'active', 1)")
    # "precio" queda en el JSON del carrito porque el camino de error (password
    # incorrecta) vuelve a mostrar el checkout con carro.total(items) sobre el
    # carrito CRUDO, antes de cualquier revalidación contra `productos`.
    con.execute("INSERT INTO tienda_carritos (cart_id, items_json) VALUES (?,?)",
               ("cart-1", json.dumps([{"ml_id": "KIT-LIBRO-SAFARI", "precio": 9000, "qty": 1}])))
    con.commit(); con.close()

    # evitar tocar Mercado Pago de verdad: la orden se crea, pero iniciar_pago
    # se reemplaza por un fake que no pega a la red
    monkeypatch.setattr(tienda.chk, "iniciar_pago",
                        lambda order_id, db_path=None: {"init_point": "https://mp.fake/pagar"})

    tienda.app.config["TESTING"] = True
    client = tienda.app.test_client()
    client.set_cookie("tienda_cart", "cart-1")
    return tienda, client, db_path


def test_checkout_digital_crea_cuenta_nueva(tmp_path, monkeypatch):
    tienda, client, db = _prep(tmp_path, monkeypatch)
    r = client.post("/checkout", data={"cliente": "Ana", "email": "ana@test.com",
                                       "telefono": "1155554444", "password": "clave123"})
    assert r.status_code == 302
    assert r.headers["Location"] == "https://mp.fake/pagar"
    assert tienda.tienda_clientes.existe("ana@test.com", db) is True
    # la cookie de sesión de cliente quedó seteada en la respuesta
    assert any(tienda.tienda_auth_cliente.COOKIE_NAME in h for h in r.headers.getlist("Set-Cookie"))


def test_checkout_digital_email_existente_password_incorrecta_no_crea_orden(tmp_path, monkeypatch):
    tienda, client, db = _prep(tmp_path, monkeypatch)
    tienda.tienda_clientes.crear_o_verificar("ana@test.com", "clave-original", db)
    r = client.post("/checkout", data={"cliente": "Ana", "email": "ana@test.com",
                                       "telefono": "1155554444", "password": "clave-mala"})
    assert r.status_code == 200   # vuelve a mostrar el checkout, no redirige a MP
    assert b"revis\xc3\xa1 tu contrase\xc3\xb1a" in r.data.lower() or "revisá tu contraseña" in r.get_data(as_text=True).lower()
    con = sqlite3.connect(db)
    n = con.execute("SELECT COUNT(*) FROM tienda_orders").fetchone()[0]
    con.close()
    assert n == 0


def test_checkout_digital_email_existente_password_correcta_loguea(tmp_path, monkeypatch):
    tienda, client, db = _prep(tmp_path, monkeypatch)
    tienda.tienda_clientes.crear_o_verificar("ana@test.com", "clave123", db)
    r = client.post("/checkout", data={"cliente": "Ana", "email": "ana@test.com",
                                       "telefono": "1155554444", "password": "clave123"})
    assert r.status_code == 302
    assert r.headers["Location"] == "https://mp.fake/pagar"
```

- [ ] **Step 3: Correr — debe fallar (checkout_post no maneja password todavía)**

Run: `cd /opt/ct3d/backend && python3 -m pytest tests/test_checkout_password.py -v`
Expected: FAIL (la cuenta no se crea, `tienda_clientes.existe(...)` da False)

- [ ] **Step 4: Cablear el checkout**

En `/opt/ct3d/backend/tienda.py`, agregar a los imports (después de
`import tienda_reviews as reviews`, línea ~23):

```python
import tienda_clientes
import tienda_auth_cliente
```

Reemplazar la función `checkout_post` completa (líneas ~453-484) por:

```python
@app.route("/checkout", methods=["POST"])
def checkout_post():
    cid = request.cookies.get("tienda_cart") or ""
    f = request.form
    cliente = {"cliente": f.get("cliente"), "email": f.get("email"), "telefono": f.get("telefono")}
    items = carro.obtener(cid, DB_PATH) if cid else []
    email_cuenta = None
    if cat.carrito_es_digital(items):
        # Producto digital: sin envío. Entrega por link/email tras el pago.
        # Además crea o loguea la cuenta del cliente (contraseña del form) —
        # así después puede ver todo lo que compró en /mi-cuenta.
        envio_tipo = "digital"
        envio_costo = 0.0
        envio_datos = {}
        email_cuenta = (f.get("email") or "").strip().lower()
        password = f.get("password") or ""
        if not tienda_clientes.crear_o_verificar(email_cuenta, password, DB_PATH):
            return render_template("checkout.html", items=items, total=carro.total(items),
                                   cp="", opciones=[], digital=True,
                                   error_password="Ya existe una cuenta con ese email — revisá tu contraseña.")
    else:
        # Recalcular envio_costo server-side (anti-tamper): no confiar en el valor del cliente
        envio_tipo = f.get("envio_tipo")
        cp = f.get("cp")
        ops = envio.opciones(cp) if cp else []
        elegida = next((o for o in ops if o["tipo"] == envio_tipo), None)
        costo_base = float(elegida["costo"]) if elegida else 0.0
        # Aplicar ofertas de envío: gratis por umbral, 50% por lámpara con nombre
        subtotal = carro.total(items)
        envio_costo = ofertas.ajustar_envio(subtotal, costo_base, items, envio_tipo)
        envio_datos = {"cp": cp, "direccion": f.get("direccion"), "sucursal": f.get("sucursal")}
    try:
        orden = chk.crear_orden(cid, cliente, envio_tipo, envio_costo, envio_datos, DB_PATH)
    except ValueError:
        return redirect("/carrito")
    try:
        pagoinfo = chk.iniciar_pago(orden["order_id"], DB_PATH)
    except Exception:
        logger.exception("Error al iniciar pago para orden %s", orden.get("order_id"))
        return redirect("/carrito")
    # C4: si no hay token de MP, crear_preference cae a "demo" (init_point = /gracias).
    # En producción eso sería vender sin cobrar: fallamos ruidoso en vez de simular pago.
    if pagoinfo.get("demo"):
        logger.critical("Mercado Pago en modo DEMO (sin access token): la orden %s NO se cobra. "
                        "Cargá mercadopago_access_token en config.json.", orden["order_id"])
        return redirect("/carrito")
    resp = redirect(pagoinfo["init_point"])
    if email_cuenta:
        tienda_auth_cliente.set_session_cookie(resp, email_cuenta)
    return resp
```

- [ ] **Step 5: Correr de nuevo — debe pasar**

Run: `cd /opt/ct3d/backend && python3 -m pytest tests/test_checkout_password.py -v`
Expected: `3 passed`

- [ ] **Step 6: Commit**

```bash
cd /opt/ct3d/backend
git add tienda.py tienda_templates/checkout.html tests/test_checkout_password.py
git commit -m "feat: el checkout digital crea o loguea la cuenta del cliente"
```

---

### Task 4: Páginas "Mis compras" / ingresar / salir

**Files:**
- Modify: `/opt/ct3d/backend/tienda.py` (3 rutas nuevas)
- Create: `/opt/ct3d/backend/tienda_templates/mi_cuenta.html`
- Create: `/opt/ct3d/backend/tienda_templates/cliente_ingresar.html`
- Test: `/opt/ct3d/backend/tests/test_mi_cuenta.py`

**Interfaces:**
- Consumes: `tienda_clientes.existe/verificar/listar_compras` (Task 1),
  `tienda_auth_cliente.current_cliente/set_session_cookie/clear_session_cookie`
  (Task 2).
- Produces: rutas `GET /mi-cuenta`, `GET+POST /mi-cuenta/ingresar`,
  `GET /mi-cuenta/salir` — usadas también por Task 5 (el link post-reset
  redirige a `/mi-cuenta`).

- [ ] **Step 1: Escribir el test de las 3 rutas**

Crear `/opt/ct3d/backend/tests/test_mi_cuenta.py`:

```python
import json, sqlite3, sys, importlib


def _prep(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test.db")
    # tienda_db.init_db() asume que `productos` ya existe (la crea otro
    # módulo, facturas_api.py, en producción) — acá se crea una versión
    # mínima antes, o init_db falla con "no such table: productos".
    con = sqlite3.connect(db_path)
    con.execute("CREATE TABLE productos (ml_id TEXT PRIMARY KEY, titulo TEXT, "
               "precio_ml REAL, status TEXT)")
    con.commit(); con.close()
    for mod in ("tienda_db", "tienda_clientes", "tienda_auth_cliente", "tienda"):
        sys.modules.pop(mod, None)
    import tienda_db
    tienda_db.init_db(db_path)
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({"session_secret": "test-secret-not-real"}))

    import tienda_auth_cliente as tac
    importlib.reload(tac)
    tac.CONFIG_PATH = str(cfg_path)

    import tienda
    importlib.reload(tienda)
    tienda.DB_PATH = db_path
    tienda.tienda_clientes.DB_PATH = db_path

    tienda.tienda_clientes.crear_o_verificar("ana@test.com", "clave123", db_path)
    con = sqlite3.connect(db_path)
    con.execute(
        """INSERT INTO tienda_orders (order_id, estado, items_json, subtotal, total,
           email, pagado_en, kit_download_url) VALUES (?,?,?,?,?,?,datetime('now'),?)""",
        ("TND-1", "pagada",
         json.dumps([{"ml_id": "KIT-LIBRO-SAFARI", "titulo": "Libro Safari", "qty": 1}]),
         9000, 9000, "ana@test.com", "https://kit.casatridimensional.com.ar/descarga/tok1"))
    con.commit(); con.close()

    tienda.app.config["TESTING"] = True
    return tienda, tienda.app.test_client(), db_path


def test_mi_cuenta_sin_sesion_redirige_a_ingresar(tmp_path, monkeypatch):
    tienda, client, db = _prep(tmp_path, monkeypatch)
    r = client.get("/mi-cuenta")
    assert r.status_code == 302
    assert r.headers["Location"] == "/mi-cuenta/ingresar"


def test_ingresar_con_clave_correcta_loguea_y_muestra_compras(tmp_path, monkeypatch):
    tienda, client, db = _prep(tmp_path, monkeypatch)
    r = client.post("/mi-cuenta/ingresar", data={"email": "ana@test.com", "password": "clave123"})
    assert r.status_code == 302
    assert r.headers["Location"] == "/mi-cuenta"
    r2 = client.get("/mi-cuenta")
    assert r2.status_code == 200
    body = r2.get_data(as_text=True)
    assert "Libro Safari" in body
    assert "https://kit.casatridimensional.com.ar/descarga/tok1" in body


def test_ingresar_con_clave_incorrecta_no_loguea(tmp_path, monkeypatch):
    tienda, client, db = _prep(tmp_path, monkeypatch)
    r = client.post("/mi-cuenta/ingresar", data={"email": "ana@test.com", "password": "mala"})
    assert r.status_code == 200
    assert "Contraseña incorrecta" in r.get_data(as_text=True)


def test_ingresar_email_inexistente(tmp_path, monkeypatch):
    tienda, client, db = _prep(tmp_path, monkeypatch)
    r = client.post("/mi-cuenta/ingresar", data={"email": "nadie@test.com", "password": "x"})
    assert r.status_code == 200
    assert "No encontramos una cuenta" in r.get_data(as_text=True)


def test_mi_cuenta_no_muestra_compras_de_otro_email(tmp_path, monkeypatch):
    tienda, client, db = _prep(tmp_path, monkeypatch)
    tienda.tienda_clientes.crear_o_verificar("otro@test.com", "clave999", db)
    client.post("/mi-cuenta/ingresar", data={"email": "otro@test.com", "password": "clave999"})
    r = client.get("/mi-cuenta")
    assert "Libro Safari" not in r.get_data(as_text=True)


def test_salir_borra_la_sesion(tmp_path, monkeypatch):
    tienda, client, db = _prep(tmp_path, monkeypatch)
    client.post("/mi-cuenta/ingresar", data={"email": "ana@test.com", "password": "clave123"})
    client.get("/mi-cuenta/salir")
    r = client.get("/mi-cuenta")
    assert r.headers["Location"] == "/mi-cuenta/ingresar"
```

- [ ] **Step 2: Correr — debe fallar (rutas no existen)**

Run: `cd /opt/ct3d/backend && python3 -m pytest tests/test_mi_cuenta.py -v`
Expected: FAIL con 404 en `/mi-cuenta`

- [ ] **Step 3: Agregar las 3 rutas a `tienda.py`**

Agregar después de la función `gracias()` en `/opt/ct3d/backend/tienda.py`:

```python
@app.route("/mi-cuenta")
def mi_cuenta():
    email = tienda_auth_cliente.current_cliente()
    if not email:
        return redirect("/mi-cuenta/ingresar")
    compras = tienda_clientes.listar_compras(email, DB_PATH)
    return render_template("mi_cuenta.html", email=email, compras=compras)


@app.route("/mi-cuenta/ingresar", methods=["GET"])
def mi_cuenta_ingresar():
    if tienda_auth_cliente.current_cliente():
        return redirect("/mi-cuenta")
    return render_template("cliente_ingresar.html", error=None)


@app.route("/mi-cuenta/ingresar", methods=["POST"])
def mi_cuenta_ingresar_post():
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    if not tienda_clientes.existe(email, DB_PATH):
        return render_template("cliente_ingresar.html",
                               error="No encontramos una cuenta con ese email.")
    if not tienda_clientes.verificar(email, password, DB_PATH):
        return render_template("cliente_ingresar.html", error="Contraseña incorrecta.")
    resp = redirect("/mi-cuenta")
    tienda_auth_cliente.set_session_cookie(resp, email)
    return resp


@app.route("/mi-cuenta/salir")
def mi_cuenta_salir():
    resp = redirect("/")
    tienda_auth_cliente.clear_session_cookie(resp)
    return resp
```

- [ ] **Step 4: Crear `tienda_templates/mi_cuenta.html`**

```html
{% extends "base.html" %}
{% block title %}Mis compras — CASATRIDIMENSIONAL{% endblock %}
{% block content %}
<header class="section-head section-head--page">
  <h1 class="page-title">Mis compras</h1>
  <p class="section-note">{{ email }} — <a href="/mi-cuenta/salir">cerrar sesión</a></p>
</header>
{% if not compras %}
<p class="hint">Todavía no tenés compras digitales con esta cuenta.</p>
{% else %}
<div class="checkout-layout">
  <div class="checkout-main">
    {% for c in compras %}
    <section class="panel">
      <h2 class="panel__title">{{ c.pagado_en }}</h2>
      {% for it in c.items %}
      <p>{{ it.titulo }}</p>
      {% endfor %}
      <a class="btn btn-primary" href="{{ c.kit_download_url }}" target="_blank" rel="noopener">⬇️ Ver / descargar</a>
    </section>
    {% endfor %}
  </div>
</div>
{% endif %}
{% endblock %}
```

- [ ] **Step 5: Crear `tienda_templates/cliente_ingresar.html`**

```html
{% extends "base.html" %}
{% block title %}Ingresar — CASATRIDIMENSIONAL{% endblock %}
{% block content %}
<header class="section-head section-head--page">
  <h1 class="page-title">Ingresar a mi cuenta</h1>
</header>
<form class="checkout" method="post" action="/mi-cuenta/ingresar">
  <section class="panel">
    <div class="field-grid">
      <label class="field">
        <span class="field__label">Email</span>
        <input name="email" type="email" placeholder="vos@email.com" required>
      </label>
      <label class="field">
        <span class="field__label">Contraseña</span>
        <input name="password" type="password" required>
      </label>
    </div>
    {% if error %}<p class="hint" style="color:#c0392b">{{ error }}</p>{% endif %}
    <p class="hint"><a href="/mi-cuenta/recuperar">Olvidé mi contraseña</a></p>
  </section>
  <button class="btn btn-primary btn-block" type="submit">Ingresar</button>
</form>
{% endblock %}
```

- [ ] **Step 6: Correr de nuevo — debe pasar**

Run: `cd /opt/ct3d/backend && python3 -m pytest tests/test_mi_cuenta.py -v`
Expected: `6 passed`

- [ ] **Step 7: Commit**

```bash
cd /opt/ct3d/backend
git add tienda.py tienda_templates/mi_cuenta.html tienda_templates/cliente_ingresar.html tests/test_mi_cuenta.py
git commit -m "feat: página Mis compras + ingresar/salir de la cuenta"
```

---

### Task 5: "Olvidé mi contraseña"

**Files:**
- Modify: `/opt/ct3d/backend/tienda.py` (2 rutas nuevas)
- Modify: `/opt/ct3d/backend/tienda_emails.py` (agregar plantilla + envío)
- Create: `/opt/ct3d/backend/tienda_templates/cliente_recuperar.html`
- Create: `/opt/ct3d/backend/tienda_templates/cliente_reset.html`
- Test: `/opt/ct3d/backend/tests/test_recuperar_password.py`

**Interfaces:**
- Consumes: `tienda_clientes.existe/set_password` (Task 1),
  `tienda_auth_cliente.crear_token_reset/verificar_token_reset/set_session_cookie`
  (Task 2).
- Produces: rutas `GET+POST /mi-cuenta/recuperar`, `GET+POST /mi-cuenta/reset`.

- [ ] **Step 1: Agregar la plantilla de email en `tienda_emails.py`**

Agregar al final de `/opt/ct3d/backend/tienda_emails.py`:

```python
def reset_password_html(link):
    parrafos = ["Recibimos un pedido para restablecer tu contraseña de CASATRIDIMENSIONAL.",
                "Si no fuiste vos, podés ignorar este correo — tu contraseña actual sigue funcionando.",
                "Este link vence en 1 hora."]
    return _layout("Restablecer tu contraseña", "Restablecer contraseña 🔑",
                   parrafos, "Elegir nueva contraseña", link)


def enviar_reset_password(to, link):
    return email_inbox.enviar_email_html(
        to, "🔑 Restablecer tu contraseña — CASATRIDIMENSIONAL",
        reset_password_html(link), f"Restablecer tu contraseña: {link}")
```

- [ ] **Step 2: Escribir el test**

Crear `/opt/ct3d/backend/tests/test_recuperar_password.py`:

```python
import json, sqlite3, sys, importlib


def _prep(tmp_path, monkeypatch):
    db_path = str(tmp_path / "test.db")
    # tienda_db.init_db() asume que `productos` ya existe (la crea otro
    # módulo, facturas_api.py, en producción) — acá se crea una versión
    # mínima antes, o init_db falla con "no such table: productos".
    con = sqlite3.connect(db_path)
    con.execute("CREATE TABLE productos (ml_id TEXT PRIMARY KEY, titulo TEXT, "
               "precio_ml REAL, status TEXT)")
    con.commit(); con.close()
    for mod in ("tienda_db", "tienda_clientes", "tienda_auth_cliente", "tienda", "tienda_emails"):
        sys.modules.pop(mod, None)
    import tienda_db
    tienda_db.init_db(db_path)
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({"session_secret": "test-secret-not-real"}))

    import tienda_auth_cliente as tac
    importlib.reload(tac)
    tac.CONFIG_PATH = str(cfg_path)

    import tienda
    importlib.reload(tienda)
    tienda.DB_PATH = db_path
    tienda.tienda_clientes.DB_PATH = db_path
    tienda.tienda_clientes.crear_o_verificar("ana@test.com", "clave-vieja", db_path)

    enviados = []
    monkeypatch.setattr(tienda.tienda_emails, "enviar_reset_password",
                        lambda to, link: enviados.append((to, link)))

    tienda.app.config["TESTING"] = True
    return tienda, tienda.app.test_client(), db_path, enviados


def test_recuperar_email_con_cuenta_envia_mail(tmp_path, monkeypatch):
    tienda, client, db, enviados = _prep(tmp_path, monkeypatch)
    r = client.post("/mi-cuenta/recuperar", data={"email": "ana@test.com"})
    assert r.status_code == 200
    assert len(enviados) == 1
    assert enviados[0][0] == "ana@test.com"
    assert "/mi-cuenta/reset?token=" in enviados[0][1]


def test_recuperar_email_sin_cuenta_mismo_mensaje_sin_enviar(tmp_path, monkeypatch):
    tienda, client, db, enviados = _prep(tmp_path, monkeypatch)
    r1 = client.post("/mi-cuenta/recuperar", data={"email": "ana@test.com"})
    r2 = client.post("/mi-cuenta/recuperar", data={"email": "nadie@test.com"})
    assert r1.get_data() == r2.get_data()   # no revela si el email existe
    assert len(enviados) == 1                # solo se mandó para el que sí existe


def test_reset_con_token_valido_cambia_password(tmp_path, monkeypatch):
    tienda, client, db, enviados = _prep(tmp_path, monkeypatch)
    client.post("/mi-cuenta/recuperar", data={"email": "ana@test.com"})
    link = enviados[0][1]
    token = link.split("token=")[1]
    r = client.post("/mi-cuenta/reset", data={"token": token, "password": "clave-nueva"})
    assert r.status_code == 302
    assert r.headers["Location"] == "/mi-cuenta"
    assert tienda.tienda_clientes.verificar("ana@test.com", "clave-nueva", db) is True
    assert tienda.tienda_clientes.verificar("ana@test.com", "clave-vieja", db) is False


def test_reset_con_token_invalido_no_cambia_nada(tmp_path, monkeypatch):
    tienda, client, db, enviados = _prep(tmp_path, monkeypatch)
    r = client.post("/mi-cuenta/reset", data={"token": "basura", "password": "clave-nueva"})
    assert r.status_code == 200
    assert "venci" in r.get_data(as_text=True).lower() or "no es válido" in r.get_data(as_text=True).lower()
    assert tienda.tienda_clientes.verificar("ana@test.com", "clave-vieja", db) is True
```

- [ ] **Step 3: Correr — debe fallar (rutas no existen)**

Run: `cd /opt/ct3d/backend && python3 -m pytest tests/test_recuperar_password.py -v`
Expected: FAIL con 404

- [ ] **Step 4: Agregar las rutas a `tienda.py`**

Agregar el import (junto a los de Task 3, si no está ya):

```python
import tienda_emails
```

Agregar después de las rutas de Task 4:

```python
@app.route("/mi-cuenta/recuperar", methods=["GET"])
def mi_cuenta_recuperar():
    return render_template("cliente_recuperar.html", enviado=False)


@app.route("/mi-cuenta/recuperar", methods=["POST"])
def mi_cuenta_recuperar_post():
    email = (request.form.get("email") or "").strip().lower()
    if tienda_clientes.existe(email, DB_PATH):
        token = tienda_auth_cliente.crear_token_reset(email)
        base = config_loader.get("tienda_base_url") or "https://tienda.casatridimensional.com.ar"
        link = f"{base}/mi-cuenta/reset?token={token}"
        tienda_emails.enviar_reset_password(email, link)
    # Mismo mensaje exista o no la cuenta: no revelar qué emails están registrados.
    return render_template("cliente_recuperar.html", enviado=True)


@app.route("/mi-cuenta/reset", methods=["GET"])
def mi_cuenta_reset():
    token = request.args.get("token", "")
    email = tienda_auth_cliente.verificar_token_reset(token)
    if not email:
        return render_template("cliente_reset.html", token=None,
                               error="Este link venció o no es válido — pedí uno nuevo.")
    return render_template("cliente_reset.html", token=token, error=None)


@app.route("/mi-cuenta/reset", methods=["POST"])
def mi_cuenta_reset_post():
    token = request.form.get("token", "")
    email = tienda_auth_cliente.verificar_token_reset(token)
    if not email:
        return render_template("cliente_reset.html", token=None,
                               error="Este link venció o no es válido — pedí uno nuevo.")
    password = request.form.get("password") or ""
    if len(password) < 6:
        return render_template("cliente_reset.html", token=token,
                               error="La contraseña debe tener al menos 6 caracteres.")
    tienda_clientes.set_password(email, password, DB_PATH)
    resp = redirect("/mi-cuenta")
    tienda_auth_cliente.set_session_cookie(resp, email)
    return resp
```

- [ ] **Step 5: Crear `tienda_templates/cliente_recuperar.html`**

```html
{% extends "base.html" %}
{% block title %}Recuperar contraseña — CASATRIDIMENSIONAL{% endblock %}
{% block content %}
<header class="section-head section-head--page">
  <h1 class="page-title">Recuperar contraseña</h1>
</header>
{% if enviado %}
<p class="hint">Si ese email tiene una cuenta, te mandamos un link para elegir una contraseña nueva. Revisá tu correo.</p>
{% else %}
<form class="checkout" method="post" action="/mi-cuenta/recuperar">
  <section class="panel">
    <label class="field">
      <span class="field__label">Email</span>
      <input name="email" type="email" placeholder="vos@email.com" required>
    </label>
  </section>
  <button class="btn btn-primary btn-block" type="submit">Enviar link</button>
</form>
{% endif %}
{% endblock %}
```

- [ ] **Step 6: Crear `tienda_templates/cliente_reset.html`**

```html
{% extends "base.html" %}
{% block title %}Nueva contraseña — CASATRIDIMENSIONAL{% endblock %}
{% block content %}
<header class="section-head section-head--page">
  <h1 class="page-title">Elegir nueva contraseña</h1>
</header>
{% if error %}
<p class="hint" style="color:#c0392b">{{ error }}</p>
<p class="hint"><a href="/mi-cuenta/recuperar">Pedir un link nuevo</a></p>
{% else %}
<form class="checkout" method="post" action="/mi-cuenta/reset">
  <input type="hidden" name="token" value="{{ token }}">
  <section class="panel">
    <label class="field">
      <span class="field__label">Contraseña nueva</span>
      <input name="password" type="password" minlength="6" required>
    </label>
  </section>
  <button class="btn btn-primary btn-block" type="submit">Guardar</button>
</form>
{% endif %}
{% endblock %}
```

- [ ] **Step 7: Correr de nuevo — debe pasar**

Run: `cd /opt/ct3d/backend && python3 -m pytest tests/test_recuperar_password.py -v`
Expected: `4 passed`

- [ ] **Step 8: Commit**

```bash
cd /opt/ct3d/backend
git add tienda.py tienda_emails.py tienda_templates/cliente_recuperar.html tienda_templates/cliente_reset.html tests/test_recuperar_password.py
git commit -m "feat: recuperar contraseña de la cuenta de cliente"
```

---

### Task 6: Retención "para siempre" (ct3d-personalizador)

**Files:**
- Modify: `/root/ct3d-personalizador/servicio.py:240` (default de `_limpiar_pedidos_viejos`)
- Modify: `/root/ct3d-personalizador/audiolibro.py:23` (`VIGENCIA_DIAS`)
- Modify: `/root/ct3d-personalizador/invitacion_web.py:26` (`VIGENCIA_DIAS`)
- Test: correr la suite existente completa (ya cubre estos módulos)

**Interfaces:**
- No expone nada nuevo — cierra el círculo del spec: los links que
  `tienda_orders.kit_download_url` ya guarda (usados por
  `tienda_clientes.listar_compras`, Task 1) dejan de morir.

- [ ] **Step 1: Extender el umbral de `pedidos/`**

En `/root/ct3d-personalizador/servicio.py:240`, cambiar:

```python
def _limpiar_pedidos_viejos(dias=30):
    """A3: borra carpetas de pedidos (ZIP + meta) de más de `dias` — no acumular PII."""
```

por:

```python
def _limpiar_pedidos_viejos(dias=7300):
    """Borra carpetas de pedidos (ZIP + meta) de más de `dias`. Antes eran 30 días
    (A3, minimizar PII); ahora "para siempre" en la práctica (~20 años) — el pedido
    respalda la cuenta de cliente de la tienda (Mis compras), que promete acceso
    indefinido al link ya guardado en tienda_orders.kit_download_url."""
```

- [ ] **Step 2: Extender el umbral de audiolibros**

En `/root/ct3d-personalizador/audiolibro.py:23`, cambiar:

```python
VIGENCIA_DIAS = 365
```

por:

```python
VIGENCIA_DIAS = 7300   # "para siempre" en la práctica (~20 años) — respalda Mis compras
```

- [ ] **Step 3: Extender el umbral de invitaciones web**

En `/root/ct3d-personalizador/invitacion_web.py:26`, cambiar:

```python
VIGENCIA_DIAS = 180
```

por:

```python
VIGENCIA_DIAS = 7300   # "para siempre" en la práctica (~20 años) — respalda Mis compras
```

- [ ] **Step 4: Correr la suite completa — debe seguir pasando**

Run: `cd /root/ct3d-personalizador && python3 -m pytest tests/ -q`
Expected: todos los tests pasan (en particular
`tests/test_invitacion_web.py`, que ya lee `iw.VIGENCIA_DIAS`
dinámicamente — no debería requerir cambios).

- [ ] **Step 5: Commit**

```bash
cd /root/ct3d-personalizador
git add servicio.py audiolibro.py invitacion_web.py
git commit -m "feat: retención de archivos digitales para siempre (respalda Mis compras)

Los pedidos/audiolibros/invitaciones ya no se borran a los 30/365/180 días
— el link que la tienda guarda en tienda_orders.kit_download_url ahora
puede prometerse 'para siempre' en la cuenta de cliente."
git push
```

---

## Notas para el que ejecute este plan

- Los Tasks 1-5 viven en `/opt/ct3d/backend` — repo **separado** de
  `ct3d-personalizador`. Cada uno tiene su propio git; commitear en el
  repo correcto en cada paso.
- El Task 6 vive en `ct3d-personalizador` y puede hacerse en cualquier
  momento (no depende de los otros 5) — de hecho conviene hacerlo
  primero o en paralelo, porque desbloquea que los links ya empiecen a
  durar más aunque la cuenta todavía no exista.
- Ningún Task requiere reiniciar servicios de producción hasta que TODOS
  estén commiteados — recién ahí reiniciar `tienda` (puerto 8092) y, para
  el Task 6, `ct3d-kit` (puerto 8787).
- El dropdown de checkout NO cambia su estructura de envío/CP para
  compras físicas — solo el form digital gana el campo de contraseña.
