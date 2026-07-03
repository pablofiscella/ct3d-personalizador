# Cuenta de cliente + "Mis compras" — Diseño

> **For agentic workers:** este documento es el spec aprobado por Pablo. El
> siguiente paso es un plan de implementación (superpowers:writing-plans).

**Goal:** que un cliente que compra un producto digital personalizado
(libro, libro premium, audiolibro, invitación web, etc.) pueda crear una
cuenta en el momento de pagar y, después, entrar a la tienda para ver/volver
a descargar o reproducir todo lo que compró, para siempre.

**Architecture:** todo el trabajo nuevo vive en la tienda
(`/opt/ct3d/backend`), que ya tiene la tabla de pedidos, el checkout y el
sistema de emails. El servicio de generación (`ct3d-personalizador`) no
gana ningún concepto de cuentas — solo deja de borrar los archivos
digitales, porque cada pedido ya guarda para siempre su link de
descarga/reproducción en `tienda_orders.kit_download_url`. Sacar el borrado
automático es lo único que hace falta para que esos links sigan vivos.

**Tech Stack:** Flask + SQLite (`facturas_ml.db`, ya existente), JWT en
cookie HttpOnly firmada (mismo patrón que `auth.py`, el login de admin),
`werkzeug.security` para hashear contraseñas (ya viene con Flask).

## Global Constraints

- Alcance: solo productos DIGITALES PERSONALIZADOS (libro, libro-premium,
  libro-audio, invitacion-web, calendario, etc. — lo que hoy genera un
  link/token por pedido). Los pedidos físicos (impresiones 3D) no aparecen
  en "Mis compras".
- No se migran pedidos anteriores al lanzamiento — la cuenta arranca vacía
  y solo suma compras nuevas de ahí en adelante.
- "Mis compras" en v1 es de solo lectura: ver + descargar/reproducir. Nada
  de editar/regenerar un pedido ya comprado desde la cuenta.
- Retención de archivos digitales: para siempre (se saca el borrado
  automático de 30/180/365 días existente en `ct3d-personalizador`).
- La cuenta de cliente es un sistema separado del login de admin
  (`auth.py`, Google Sign-In con whitelist) — no comparten tabla ni cookie.
- Contraseñas siempre hasheadas (`werkzeug.security.generate_password_hash`,
  nunca texto plano), cookie de sesión HttpOnly + Secure + SameSite=Lax.

---

## 1. Base de datos: tabla `tienda_clientes`

Nueva tabla en `facturas_ml.db` (mismo archivo que `tienda_orders`):

```sql
CREATE TABLE IF NOT EXISTS tienda_clientes (
  email        TEXT PRIMARY KEY,
  password_hash TEXT NOT NULL,
  creado_en    TEXT DEFAULT (datetime('now','localtime'))
);
```

`email` normalizado a minúsculas antes de cualquier lectura/escritura (evita
duplicados por mayúsculas). Es la PK — no hay un id numérico separado
porque el email YA es el identificador natural usado en `tienda_orders`.

## 2. Checkout con contraseña

En `/checkout` (`tienda.py`), el formulario de pago suma un campo
"Contraseña (para volver a ver tus compras)". Al enviar:

1. Normalizar el email a minúsculas.
2. `SELECT password_hash FROM tienda_clientes WHERE email=?`
   - **No existe fila** → crear la cuenta con
     `generate_password_hash(password)` e insertarla.
   - **Existe fila** → `check_password_hash(hash, password)`. Si no
     coincide, error de checkout (mensaje: "Ya existe una cuenta con ese
     email — revisá tu contraseña") y no se procesa el pago.
3. Si login/alta OK: emitir la cookie de sesión de cliente (ver §4) en la
   respuesta, y continuar el flujo de checkout normal (redirect a Mercado
   Pago) exactamente como hoy.

El resto del checkout (creación de la orden, MP, webhook, generación del
kit) no cambia — `tienda_orders.email` ya se guarda igual que ahora; el
único agregado es la fila en `tienda_clientes` y la cookie de sesión.

## 3. Login de cliente recurrente

Si en el paso 2 el email ya existe y la contraseña coincide, es
simplemente un login — no hace falta una pantalla separada para este caso,
el propio checkout lo resuelve. Además, dos rutas nuevas independientes del
checkout:

- `GET/POST /mi-cuenta/ingresar` — email + contraseña, para entrar sin
  comprar (por ejemplo, para ir directo a "Mis compras").
- `GET /mi-cuenta/salir` — borra la cookie de sesión, redirect a `/`.

## 4. Sesión de cliente (cookie)

Mismo patrón que `auth.py` (JWT firmado, HttpOnly), pero independiente:

- Cookie nueva, ej. `ct3d_cliente` (no reutiliza `COOKIE_NAME` de admin).
- Payload: `{"email": <email>, "exp": ...}`, firmado con
  `config.json::session_secret` (el mismo secreto que ya usa `auth.py` —
  no hace falta uno nuevo).
- Vigencia larga (ej. 90 días, se renueva en cada visita a `/mi-cuenta`).
- `current_cliente()` helper: lee la cookie, valida firma/expiración,
  devuelve el email o `None` — análogo a `auth.current_user()`.

## 5. "Mis compras" (`GET /mi-cuenta`)

Si no hay sesión de cliente → redirect a `/mi-cuenta/ingresar`.

Si hay sesión: `SELECT * FROM tienda_orders WHERE email=? AND estado='pagada' ORDER BY pagado_en DESC`
(email de la sesión, no de un parámetro de URL — nunca se lista el pedido
de otra persona). Por cada orden:

- Parsear `items_json`, quedarse solo con los ítems cuyo `tipo` es de la
  lista de tipos digitales-personalizados (misma lista que ya usa
  `tienda_kit_admin.TIPOS` / `tienda_catalogo._KIT_TIPOS`).
- Mostrar: nombre del producto, tema, fecha (`pagado_en`), y un botón que
  apunta directo a `kit_download_url` (el mismo link de siempre — sin
  tocar ni regenerar nada).
- Si una orden pagada no tiene ítems digitales (todo físico) o
  `kit_download_url` vacío (generación falló), no se le muestra botón —
  se indica "contactanos" en vez de un link roto.

Plantilla nueva `tienda_templates/mi_cuenta.html`, mismo layout/branding
que el resto de la tienda.

## 6. "Olvidé mi contraseña"

`GET/POST /mi-cuenta/recuperar`: pide el email, genera un token de un solo
uso (igual mecanismo que la cookie de sesión pero de corta vida, ej. 1
hora, con un flag `"tipo": "reset"` en el payload para que no sirva como
sesión), y envía un mail con el link `/mi-cuenta/reset?token=...`
reutilizando el layout de `tienda_emails.py::_layout`. Esa página pide la
contraseña nueva y actualiza `password_hash`.

## 7. Retención "para siempre" (`ct3d-personalizador`)

Tres mecanismos de borrado automático a desactivar (o extender a un
horizonte muy largo, ej. 20 años, que en la práctica es "para siempre" sin
tener que reescribir la lógica de borrado condicional):

- `servicio.py::_limpiar_pedidos_viejos()` — hoy 30 días sobre `pedidos/`.
- `audiolibro.py::_limpiar_vencidos()` — hoy 365 días sobre `audiolibros/`.
- `invitacion_web.py` — hoy 180 días sobre `invitaciones/`.

No se toca la lógica de idempotencia/generación en sí, solo el umbral de
borrado (o se comenta la llamada, dejando el código muerto pero disponible
por si en el futuro hay que retomar un límite).

## Error Handling

- Contraseña incorrecta en checkout → no se crea la orden ni se cobra;
  mensaje claro, el carrito se conserva.
- Email inválido / contraseña muy corta → validación en el form, mismo
  estilo que las validaciones que ya tiene `/checkout`.
- Cookie de sesión vencida o corrupta → tratar como "sin sesión", no
  crashear (`current_cliente()` atrapa excepciones de `jwt.decode` igual
  que `verify_session_cookie` en admin).
- Token de "olvidé mi contraseña" vencido o reusado → mensaje de "pedí un
  link nuevo", no se actualiza la contraseña.

## Testing

- Alta de cuenta nueva en checkout (email no existía) → fila en
  `tienda_clientes`, cookie emitida, orden se crea igual que hoy.
- Checkout con email existente + contraseña correcta → login, no duplica
  fila en `tienda_clientes`.
- Checkout con email existente + contraseña incorrecta → rechazado, sin
  crear orden.
- `/mi-cuenta` sin sesión → redirect a login.
- `/mi-cuenta` con sesión → solo aparecen las órdenes de ESE email, solo
  ítems digital-personalizados, con el `kit_download_url` correcto.
- `/mi-cuenta` no expone pedidos de otro cliente aunque se adivine un
  order_id (la query siempre filtra por el email de la cookie, nunca por
  parámetro de URL).
- Recuperar contraseña: token válido cambia la contraseña; token vencido
  no.
