# Cloudflare Tunnel — dejar el servicio público (estable, como systemd)

Estado en CT101 (ya hecho por mí):
- ✅ `cloudflared` instalado (`/usr/local/bin/cloudflared`, v2026.5.0).
- ✅ `ct3d-kit.service` (el generador) corriendo en `localhost:8787` — `active` + `enabled`.
- ✅ `ct3d-tunnel.service` instalado, **esperando el token**.
- ✅ API key del servicio: `f7d40f06445b55ba39c7a13ccce95dd60e27ca44beccd28e`

Falta **un solo paso tuyo**: crear el túnel con nombre en tu cuenta de Cloudflare y pegar el token.

## Pasos (5 min, en el panel de Cloudflare)

1. Entrá a **Cloudflare Zero Trust** → **Networks → Tunnels** → **Create a tunnel** → tipo **Cloudflared**.
2. Ponele un nombre (ej. `ct3d-kit`). Cloudflare te muestra un **token** (la cadena larga del comando `cloudflared ... run --token eyJ...`). **Copiá ese token.**
3. En **Public Hostnames** del túnel, agregá:
   - **Subdomain**: `kit`  · **Domain**: tu dominio en Cloudflare (ej. `casatridimensional.com`)
   - **Service**: `HTTP`  →  `localhost:8787`
   - (resultado: `https://kit.casatridimensional.com` → tu servicio)
4. Pegá el token en CT101 y arrancá el túnel:
   ```bash
   nano /etc/ct3d/cloudflared.env          # CF_TUNNEL_TOKEN=eyJ...   (reemplazá el placeholder)
   systemctl enable --now ct3d-tunnel
   systemctl status ct3d-tunnel            # debe quedar "active (running)"
   ```
5. Probá: `https://kit.casatridimensional.com/health` debería devolver `{"ok": true}`.

> Si preferís, **pasame vos el token** y lo dejo configurado y arrancado yo.

## Configurar el plugin (una vez que el túnel anda)
WooCommerce → **CT3D Kit**:
- **URL del servicio**: `https://kit.casatridimensional.com`
- **API Key**: `f7d40f06445b55ba39c7a13ccce95dd60e27ca44beccd28e`

Con eso, el preview en vivo y la descarga del cliente salen por la URL pública, y el link de descarga se arma solo según el host (no hay que tocar nada más).

## Alternativa sin dashboard (login interactivo)
Si preferís túnel por login en vez de token:
```bash
cloudflared tunnel login          # abre navegador, autorizás tu dominio
cloudflared tunnel create ct3d-kit
cloudflared tunnel route dns ct3d-kit kit.casatridimensional.com
# luego config.yml apuntando a http://localhost:8787 y correr como systemd
```
El método del token (arriba) es más simple para servidor headless.

## Comandos útiles
```bash
systemctl status ct3d-kit ct3d-tunnel
journalctl -u ct3d-tunnel -f         # ver logs del túnel
journalctl -u ct3d-kit -f            # ver logs de generación
```
