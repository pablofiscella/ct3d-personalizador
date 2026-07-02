# ct3d-personalizador — Motor de piezas imprimibles

> **Propósito:** Motor Python que genera kits de cumpleaños personalizables con IA (OpenAI gpt-image-2 para el cuaderno).
> Repo hermano: `/opt/ct3d/` (backend Flask + dashboard que consume este motor).

## Qué es

Motor procedural de **10 tipos de piezas imprimibles:**
- Kit completo (invitación, cartel, actividades, etc.)
- Productos individuales: certificado, corona, antifaces, menú, rompecabezas, cápsula, calendario, papertoys, memoria
- **Libro de cuento personalizado** (`libro.py`): 10 páginas donde el chico es el protagonista — portada, dedicatoria, 7 páginas de historia (cada una con escena procedural que ILUSTRA lo que cuenta el texto: cama+invitación → luces mágicas → fiesta → problema → solución → tesoro → casita de noche) y FIN. Historia ambientada por temática (`libro.HISTORIAS`, con fallback genérico). Campos: nombre, edad, dedicatoria. Cada página se reemplaza con arte IA vía `temas/{tema}/overrides/libro/{idx}.png`.

**Tecnología:** Pillow (procedural generation) + OpenAI gpt-image-2 (cuaderno de actividades con IA) + override system (cliente puede reemplazar cualquier pieza).

**Donde vive:** `/root/ct3d-personalizador/` (repo `ct3d-personalizador.git`)

## Git: Procedimiento obligatorio

**NUNCA terminar una sesión sin confirmar que TODO está commiteado y pusheado:**

```bash
cd /root/ct3d-personalizador
git status
git add <archivos>
git commit -m "tipo: descripción"
git push origin main    # Pre-push hook bloquea si hay cambios sin trackear
```

### Pre-push hook (protección automática)
El hook en `.git/hooks/pre-push` bloquea push si hay archivos críticos sin trackear:
- `.py`, `.jsx`, `.html`, `.md` sin stagear → BLOQUEADO
- `.png` (overrides personalizados) sin trackear → BLOQUEADO

## Estructura

```
temas/                      # Temáticas (safari, circo, superhéroes, etc.)
  {tema}/                   # Carpeta por tema
    tema.json              # Config (colores, personajes)
    ia_maestra.png         # Imagen base del cuaderno IA (gitignored)
    overrides/             # Reemplazos del cliente (commiteados)
      tipo/
        0.png, 1.png...    # Piezas reemplazadas

productos.py               # Registry de tipos + generadores
certificado.py, corona.py, antifaces.py, menu_infantil.py, etc.
cuaderno.py               # Generador IA del cuaderno de actividades
piezas.py                 # Utilidades (marca de agua, RGBA→RGB, etc.)

tests/
  test_productos_overrides.py
  test_cuaderno.py
  ...
```

## Comandos clave

```bash
# Generar preview de una pieza (con marca de agua)
# GET /preview?tipo=certificado&tema=safari&nombre=Sofía

# Dashboard (panel de gestión del kit)
# Abierto en editor_simple.html (simple editor) y dash.html (panel completo)

# Tests
pytest tests/ -v
```

## Reglas

1. **Campos personalizables por tipo:** Si un tipo nuevo necesita campos (como menú), agregarlos a `productos.TIPOS[tipo]["campos"]` y `campos_labels`.
2. **Override system:** Cualquier pieza puede reemplazarse subiendo `temas/{tema}/overrides/{tipo}/{idx}.png`.
3. **Editor genérico:** `editor_simple.html` carga `/tipos` y arma inputs automáticamente — **NO tocar para agregar campos nuevos**, editar el tipo en `productos.py`.
4. **Tests:** Siempre que cambies un tipo, agregar test que verifique:
   - Piezas procedurales se generan
   - Override reemplaza la pieza
   - Campos se respetan en el preview

## Mi responsabilidad (Claude)

Cada sesión termino reportándote el estado de GIT en ambos repos (este y `/opt/ct3d/`).

---

**Contacto:** repo GitHub `pablofiscella/ct3d-personalizador`
