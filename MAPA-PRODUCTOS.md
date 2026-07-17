# MAPA de productos — dónde vive cada cosa

> Índice para no perderse: para cada familia de producto, dónde está la **generación**,
> el **contenido** (historias/menús), la **ruta web** y el **precio/título de venta**.
> Vale para los DOS repos: el motor (`/root/ct3d-personalizador`) y la tienda (`/opt/ct3d`).

## La convención (patrón de nombres — respetar para lo nuevo)

Hay una lógica implícita; lo viejo no siempre la respeta (ver "Inconsistencias").
De ahora en más, un producto nuevo usa:

| Sufijo | Qué es | Ejemplo |
|---|---|---|
| `<producto>.py` | versión **imprimible** (PDF) | `libro.py`, `cuaderno.py`, `rompecabezas.py` |
| `<producto>_web.py` | versión **web / link vivo** (tiene `crear()` + ruta en `servicio.py`) | `rompecabezas_web.py`, `actividades_web.py` |
| `<producto>_ia.py` | **arte IA** (OpenAI gpt-image-2) | `libro_ia.py`, `aventura_ia.py` |
| `<producto>_historias.py` / contenido | **historias / menús / bancos** (datos, sin dibujo) | `libro_historias.py`, `aventura.py` |

Y el hub central:
- **`productos.py`** → dict `TIPOS` (38 tipos): es el REGISTRO. Cada tipo tiene un adaptador
  `_piezas_<tipo>` que delega al módulo generador real. **Para saber qué existe y a qué archivo
  delega, mirá `TIPOS` en `productos.py`.**

## Mapa por familia

### Kit completo + piezas sueltas de fiesta (imprimibles PDF)
- **Registro:** `productos.TIPOS`: `kit, invitacion, cartel, actividades, milestone, rutina, babyshower, certificado, corona, antifaces, menu, capsula, papertoys, memoria, fiesta-completa`.
- **Generación:** un archivo por pieza — `certificado.py`, `corona.py` (+`corona_ia.py`), `antifaces.py`, `menu_infantil.py`, `rutina.py`, `capsula_tiempo.py`, `papertoys.py`, `memoria.py`, `baby_shower.py`, `bundle_fiesta.py`. Utilidades comunes: `piezas.py`, `generador.py`.
- **Precio/título venta:** `/opt/ct3d/backend/tienda_kit_admin.py` (`PRECIO_DEFAULT`, `titulo_default`).

### Libros de cuento
- **Registro:** `libro, libro-premium, libro-pdf, libro-audio`.
- **Imprimible (PDF):** `libro.py` — arma las páginas (solo el ensamblado).
- **Web narrado (audiolibro):** `audiolibro.py` — ruta `/al/<token>` (`servicio.py:858`).
- **TODAS las historias (una sola fuente):** `libro_historias.py` — `HISTORIAS` y `HISTORIA_DEFAULT` (ambientación por tema del libro-kit), `ARGUMENTOS`/`ARGUMENTO_LABELS`/`ARGUMENTOS_EXT` (arcos del libro-kit), y `ARGUMENTOS_LARGO`/`TITULOS`/`CORTO_IDX` (catálogo del audiolibro). `libro.py` las re-importa; `libro.HISTORIAS` etc. siguen funcionando. (Unificado en PR #96.)
- **Arte IA:** `libro_ia.py`.

### Actividades (cuaderno)
- **Registro:** `actividades` (imprimible), `actividades-web` (web).
- **Imprimible (PDF):** `cuaderno.py` — genera y VERIFICA por código. Elige qué actividades por edad en `cuaderno.py:_construir` (línea 1683).
- **Web (link vivo):** `actividades_web.py` — ruta `/act/<token>` (`servicio.py:933`). Menú de juegos por edad en `actividades_web.py:_menu` (78); catálogo para galería/editor en `_catalogo_juegos` (867).
- **Galería "qué incluye":** `actividades_web_cards.py` (screenshots del player).
- ➜ El "qué juegos por edad" está DUPLICADO (`_construir` vs `_menu`). Ver Inconsistencias #3.

### Rompecabezas
- **Registro:** `rompecabezas` (imprimible), `rompecabezas-web` (escenas), `rompecabezas-foto` (con foto).
- **Imprimible (PDF):** `rompecabezas.py`.
- **Web (link vivo):** `rompecabezas_web.py` — `crear()` (escenas del tema) y `crear_desde_foto()`; ruta `/armar/<token>` (`servicio.py:993`). Guarda en `rompecabezas_web/<token>/`.
- **Demo pública:** `/probar/rompecabezas/<tema>` → sirve `demo-<tema>` (helper `servicio._demo_rompecabezas_token`).

### "Elegí tu aventura" (PROTOTIPO, sin tienda)
- **Contenido (grafo):** `aventura.py` (`AVENTURAS`).
- **Web (link vivo):** `aventura_web.py` — ruta `/leer/<token>` (`servicio.py:1057`).
- **Arte IA:** `aventura_ia.py`. **Audio:** `aventura_audio.py`.

### Mándalas
- **Registro:** `mandalas` + niveles (`mandalas-media`, `mandalas-dificil`, `mandalas-muydificil`, y sus `-pdf`).
- **Imprimible (PDF):** `mandalas.py`.
- **Web (link vivo):** `mandalas_web.py` — ruta `/pintar/<token>` (`servicio.py:1025`).

### STL 3D
- **Registro:** `stl-medalla, stl-topper, stl-trofeo, stl-cortante, stl-pack`.
- **Generación:** `stl3d.py`.

### Calendario / Invitación web / Video
- `calendario.py` (registro `calendario`); `invitacion_web.py` (registro `invitacion-web`); `video_invitacion.py` (registro `video-invitacion`).

## "El menú" es TRES cosas distintas
- **(a) Menú de comida (producto):** `menu_infantil.py` (registro `menu`).
- **(b) Menú de actividades (qué juegos por edad):** `actividades_web.py:_menu` (78) — NO es un producto, es la selección de contenido.
- **(c) Menús de navegación (UI):** en `dash.html` y `editor_simple.html` (este último arma inputs desde `/tipos`).

## La info de un producto vive en 2 repos (importante)
- **Generación** → motor: `productos.py` + el módulo de la familia.
- **Precio/título/descripción de venta** → tienda: `/opt/ct3d/backend/tienda_kit_admin.py` (defaults) y la tabla `productos` de `facturas_ml.db` (valores reales, leídos por `tienda_catalogo.py`).
- **Ficha (HTML)** → tienda: `/opt/ct3d/backend/tienda_templates/producto.html`.

## Inconsistencias conocidas (por esto cuesta encontrar las cosas)
1. **Nombres inconsistentes:** el imprimible de actividades es `cuaderno.py` (no `actividades.py`); el web del libro es `audiolibro.py` (no `libro_web.py`). No hay regla uniforme `<x>.py`/`<x>_web.py`.
2. ~~**Historias en dos lados:** `libro_historias.py` (audiolibro) + `libro.py` HISTORIAS/ARGUMENTOS (libro-kit).~~ ✅ RESUELTO en PR #96: todo en `libro_historias.py`.
3. **Menú de actividades duplicado:** `cuaderno.py:_construir` (imprimible) y `actividades_web.py:_menu` (web) deciden por separado — pueden divergir (pasó con las edades 6-7).
4. **Producto partido en 2 repos:** generación en el motor, precio/título en la tienda + DB.
5. **`productos.py` mezcla registro + adaptadores + algunos helpers de dibujo inline** (~1600 líneas): es a la vez el índice y, en parte, implementación.
