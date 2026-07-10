# Mándalas para pintar — DOBLE modalidad (PDF + web)

> Producto `mandalas`: un solo producto, dos entregas.
> **(1) PDF imprimible** y **(2) app web para pintar** (`/pintar/<token>/`, aparece en Mi
> biblioteca). Creado a pedido de Pablo (jul-2026).

## Qué es

6 mándalas para colorear de fácil → muy difícil (rango chicos→adultos) + portada
personalizable con el nombre + hoja "cómo imprimir".

**El arte es FIJO** (mismas mándalas para todos, no se personalizan): line-art generado
con IA (gpt-image), limpiado a **B/N puro 300dpi**, en `mandalas_arte/1..6.png` (en el
repo). Se generó UNA vez y se vende a todos → cero costo por venta. Fallback procedural
nativo en `mandalas.py` (simetría radial exacta) si faltara un asset.

**Por qué IA y no procedural:** para el LOOK la IA gana claro (más orgánica/densa). Como
las mándalas son fijas, no hace falta IA en vivo: arte estático servido del repo.

## Las dos modalidades (un solo producto)

Al comprar, `/api/generar` tipo `mandalas` (branch en `servicio.py`) llama
`mandalas_web.crear(data)` y devuelve **un link visor** `/pintar/<token>/`. Ese visor:
- **Deja PINTAR online** las 6 mándalas (balde/flood-fill sobre el line-art, paleta,
  deshacer, limpiar, guardar PNG, **persistencia en localStorage** por mándala).
- Tiene el botón **⬇️ PDF** que descarga el `kit.zip` imprimible (guardado en el token,
  con la portada personalizada).

Así una sola URL entrega las dos modalidades; la tienda lo trata de visor (como
actividades-web) y el PDF viaja dentro.

## Archivos

- `mandalas.py` — arte imprimible (portada/páginas/cómo-imprimir); usa el asset IA con
  fallback procedural. Tipo `mandalas` en `productos.TIPOS`.
- `mandalas_web.py` — modalidad web: `crear(data)` arma `mandalas_web/<token>/` (kit.zip +
  portada.jpg + manifest, gitignored); `html()/archivo()/estado()`. El player y las 6
  mándalas salen del REPO (mejoras llegan a links vendidos); solo el zip/portada por token.
- `mandalas_player.html` + `.js` — el visor para pintar (flood-fill B/N, galería de 6).
- `servicio.py` — ruta `GET /pintar/<token>[/asset]` + branch `mandalas` en `/api/generar`.
- Tienda (`/opt/ct3d/backend`): `mandalas` en `_VISORES`/`_cover_de`/`extraer_token`
  (`tienda_clientes.py`), `_KIT_TIPOS` (`tienda_catalogo.py`), CTA "🎨 Pintar"
  (`mi_cuenta.html`), y el espejo en `tienda_kit_admin.py` (TIPOS/precio/nombre).
- Tests: `tests/test_mandalas.py` (impreso) + `tests/test_mandalas_web.py` (web).

## Probar local

```bash
CT3D_PORT=8814 CT3D_API_KEY=test python3 servicio.py
curl -s -X POST localhost:8814/api/generar -H "X-API-Key: test" \
  -H "Content-Type: application/json" -d '{"tipo":"mandalas","tema":"safari","nombre":"Sofía"}'
# abrir el download_url (/pintar/<token>/) en el navegador
```

## Ideas v2

- Mándalas TEMÁTICAS con IA (motivo del tema IA + tileador radial — el híbrido).
- Guardar la galería pintada como PDF/collage; compartir; más paletas.
