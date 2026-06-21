# Fase 3 — Conectar el kit a WooCommerce

Dos partes: **(A)** el servicio Python que genera los kits (corre en CT101) y **(B)** el plugin de WordPress que lo conecta a tu tienda.

```
Cliente (navegador) ──escribe datos──> WooCommerce (producto)
        │  preview en vivo  ┌──────────────> GET  servicio /preview  (imagen)
        ▼
   compra y paga
        │
   WooCommerce (al pagar) ──POST /api/generar (X-API-Key)──> Servicio Python
        │                                                      genera 7 PDFs → ZIP
        ▼
   Cliente recibe link ───────────────────> GET servicio /descarga/<token>  (ZIP)
```

---

## A) Servicio Python en CT101

Archivos: `generador.py`, `quitar_fondo.py`, `piezas.py`, `servicio.py`, carpetas `fonts/` y `recortes/`.

1. **Elegí una API key larga y secreta** (ej: `openssl rand -hex 24`).
2. Editá `ct3d-kit.service`: poné tu API key, el puerto y `CT3D_BASE_URL` (ver punto 4).
3. Instalalo como servicio:
   ```bash
   cp wordpress/ct3d-kit.service /etc/systemd/system/
   systemctl daemon-reload
   systemctl enable --now ct3d-kit
   systemctl status ct3d-kit
   ```
4. **Exponé el servicio con una URL pública.** El navegador del cliente (preview y descarga) tiene que llegar al servicio, así que `192.168.1.251` **no alcanza** para clientes de internet. Opciones (de más simple a más):
   - **Cloudflare Tunnel** (recomendado, sin abrir puertos): `cloudflared tunnel --url http://localhost:8787` → te da una URL pública; o atado a un subdominio `kit.casatridimensional.com`.
   - Reverse proxy (Nginx/Caddy) con tu dominio + HTTPS, apuntando a `localhost:8787`.
   - Port-forward del router (lo menos recomendado).

   Poné esa URL pública en `CT3D_BASE_URL` (del service) y en el plugin.

> Si WooCommerce también corre dentro de tu LAN, la llamada server-to-server puede usar la IP local; pero el preview y la descarga (navegador del cliente) **siempre** necesitan la URL pública.

## B) Plugin de WordPress

1. Subí `ct3d-kit-personalizado.php` a `wp-content/plugins/ct3d-kit-personalizado/` (o instalá el ZIP).
2. Activá el plugin (requiere WooCommerce).
3. **WooCommerce → CT3D Kit**: poné la **URL pública del servicio** y la **misma API key**.
4. En el producto del kit: pestaña **General** → tildá **"Kit personalizable CT3D"**.

## Flujo para el cliente
1. Entra al producto, escribe nombre/fecha/hora/lugar/teléfono → ve la invitación actualizarse en vivo.
2. Compra. Al confirmarse el pago, WooCommerce llama al servicio y se genera el kit.
3. Ve el link **"Descargar kit"** en la página de gracias, en el email del pedido y en Mi Cuenta.

## Probar sin WordPress (local)
```bash
CT3D_API_KEY=test python3 servicio.py
# en otra terminal:
curl -X POST localhost:8787/api/generar -H "X-API-Key: test" \
  -H "Content-Type: application/json" \
  -d '{"order_id":"1","nombre":"Sofía","fecha":"Sáb 12/7","hora":"16hs","lugar":"Casa","telefono":"11..."}'
# devuelve {token, download_url} -> abrir la download_url
```

## Notas
- `/api/generar` está protegido por API key; `/descarga/<token>` usa un token impredecible; `/preview` es público (solo dibuja, no expone datos).
- Idempotente: si el pedido ya se generó, no se regenera.
- Los kits quedan en `CT3D_DATA_DIR` (un subdir por pedido). Conviene una limpieza periódica (cron) de pedidos viejos.
