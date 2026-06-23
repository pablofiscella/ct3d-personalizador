# CT3D · Personalizador de kits

Motor y panel para vender **kits de cumpleaños personalizables** (PDFs imprimibles) en
WooCommerce, con cero costo marginal. El cliente elige la edad y completa sus datos; el
sistema genera las 7 piezas del kit en PDF (300 DPI) y le entrega un ZIP para descargar.

Producto inicial: **"Safari — Un Añito Salvaje"** (edades 1 / 2 / 3).

> **Actualización jun-2026:** ahora es **multi-temática** (safari + 8 temas: construcción,
> monstruos, aviadores, bomberos, artistas, campamento, superhéroes, circo) y se vende desde el
> **e-commerce propio** (casatridimensional.com.ar), no WordPress. El editor del cliente sumó edad
> libre, incluir/ocultar por dato, iconos con variantes, color y alineación por campo y por grupo.
> **Ver `docs/SISTEMA-KITS.md`** para el detalle completo.

---

## Arquitectura

Es un servicio Python **stdlib-only** (sin frameworks) corriendo en CT101, expuesto por
**Cloudflare Tunnel** en `https://kit.casatridimensional.com.ar`.

```
Cliente (WooCommerce) ──compra──► WordPress (plugin) ──POST /api/generar──► servicio.py
                                                                              │
Panel privado (tu dashboard) ──botón "Kits"──► /entrar ──cookie──► /dash + /editor
                                                                              │
                                                                       genera kit (PDFs) → ZIP
```

- **`generador.py`** — motor de render (Pillow). Carga specs por temática, dibuja los textos
  editables sobre las imágenes de fondo. Anclado vertical idéntico a canvas (WYSIWYG).
- **`piezas.py`** — las 7 piezas: invitación, afiche, topper de torta, toppers de cupcakes,
  etiquetas de botella, tags de souvenir, banderines. Texto por edad ("Un/Dos/Tres añitos").
- **`temas.py`** — alta y carga de temáticas (`temas/<id>/tema.json` + imágenes por edad).
- **`servicio.py`** — servidor HTTP (ThreadingHTTPServer). Endpoints públicos, panel y API.
- **`quitar_fondo.py`** — recorte de fondo de animalitos/números subidos al crear temáticas.
- **`dash.html`** — panel de administración (crear/publicar/editar temáticas).
- **`editor.html`** — editor visual del posicionamiento de textos (drag + sliders).

### Temáticas (`temas/<id>/`)
```
tema.json              # specs: piezas, edades, campos de texto, tamaños, render_scale
invitacion_{1,2,3}.png # fondo de la tarjeta por edad
afiche_{1,2,3}.png     # fondo del afiche por edad (alta resolución)
layouts/*.json         # posiciones guardadas desde el editor
recortes/              # animalitos y números decorados (opcional, por temática)
```

---

## Seguridad / acceso

El panel (`/dash`, `/editor` y sus APIs) es un **backend privado**: se entra **solo desde
tu dashboard**, nunca a mano.

- **Autenticación por token (cookie), sin login interactivo.** El dashboard abre
  `/entrar?key=<token>`; el servicio valida, deja una **cookie httpOnly+Secure** (30 días) y
  redirige a `/dash` con la URL limpia. A partir de ahí todo va autenticado por cookie.
- Sin cookie / token válido → **403** en todas las rutas del panel.
- El token vive en `.api_key` (lado server) y lo inyecta el **backend del dashboard**
  (`/opt/ct3d`, endpoint `/kit/entrar`) tras validar el login de Google — **nunca** viaja al
  frontend ni al bundle.
- Rutas **públicas** (no requieren token): `/health`, `/preview` (con marca de agua),
  `/descarga/<token>`, y `/api/generar` (webhook de pago, protegido con `X-API-Key`).

> Secretos fuera de git: `.api_key`, `woo_config.json`, `woo_pub.json` (ver `.gitignore`).

---

## Panel: ciclo de vida de una temática

En **Temáticas existentes** (carrusel con la imagen de fondo de cada tarjeta):

| Estado        | Acciones |
|---------------|----------|
| Sin publicar  | Abrir editor · **Publicar** · *Eliminar temática* |
| Publicada     | badge **PUBLICADO** · Abrir editor · **Republicar** · 🗑 (baja de la tienda) · *Eliminar temática* |

- **Publicar** → crea el producto en WooCommerce como **borrador** y guarda el vínculo
  tema→producto (`woo_pub.json`).
- **Republicar** → **actualiza** el mismo producto (no duplica). Precio vacío = no lo toca.
  Si el producto fue borrado en Woo, lo recrea.
- **🗑 Eliminar** → borra el producto **de la tienda**; la temática y sus imágenes quedan.
- **Eliminar temática** → borra la temática **por completo** (imágenes + config) y, si estaba
  publicada, también baja el producto. La temática **base** (`safari`) está protegida.

> Los cambios de layout/imágenes del editor se aplican **solos** a los pedidos nuevos (el kit
> se genera en el momento de la compra). No hace falta republicar para eso.

---

## Endpoints

**Públicos**
- `GET  /health` — estado.
- `GET  /preview?nombre=&fecha=…&edad=&tema=` — PNG de la invitación con marca de agua.
- `GET  /descarga/<token>` — ZIP del kit generado.
- `POST /api/generar` (`X-API-Key`) — genera el kit de un pedido, devuelve link de descarga.

**Panel (requieren cookie/token)**
- `GET  /entrar?key=` — valida, deja la cookie, redirige a `/dash`.
- `GET  /dash` · `GET /dash/temas` · `GET /dash/config`
- `GET  /editor` · `GET /editor/layout` · `GET /editor-bg.png` · `POST /editor/save`
- `POST /dash/upload` · `/dash/crear` · `/dash/config`
- `POST /dash/publicar` · `/dash/despublicar` · `/dash/eliminar-tema`

---

## Integración con el dashboard (`/opt/ct3d`)

El dashboard (React + Flask) abre el panel sin exponer el secreto:

1. Botón **"Kits personalizables"** en la sidebar (`dashboard/app-shell.jsx`).
2. Llama a `api.casatridimensional.com.ar/kit/entrar` (Flask, `backend/facturas_api.py`),
   que **requiere login de Google**, lee el token de `.api_key` del lado del server y
   redirige a `kit.casatridimensional.com.ar/entrar?key=…`.
3. El servicio del kit deja la cookie y abre `/dash`.

El panel y el editor comparten el **sistema de diseño del dashboard** (papel cálido + violeta
amatista, Titillium Web + Source Code Pro). El editor va **embebido** dentro del panel
(iframe `?embed=1`), al costado del menú.

---

## Operación / despliegue

Corre como systemd en CT101:
- `ct3d-kit.service` — el servicio (`servicio.py`), con `CT3D_API_KEY` del entorno.
- `ct3d-tunnel.service` — Cloudflare Tunnel (`cloudflared`).

```bash
# reiniciar tras un cambio de servicio.py
systemctl restart ct3d-kit.service

# dash.html / editor.html se sirven en vivo (no requieren reinicio)
```

Variables: `CT3D_API_KEY`, `CT3D_PORT` (8787), `CT3D_DATA_DIR`, `CT3D_BASE_URL`.

El plugin de WordPress está en `wordpress/` (dropdown de edad, meta `_ct3d_tema`,
auto-generación del kit al pagar, link de descarga).
