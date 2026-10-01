# -*- coding: utf-8 -*-
"""Íconos que un dispositivo de unos años NO dibuja, y con qué se reemplazan al mostrarlos.

POR QUÉ EXISTE (01-oct-2026). Pablo, mirando el panel de la tarea de la seño: *"fijate tablas
ninja no tiene icono"*. En Windows 10 y en celulares viejos 🥷 (ninja) y 🟰 (signo igual
grueso) salen como un cuadradito vacío —el «tofu»—: son de **Emoji 13 (2020) y Emoji 14
(2021)**, y Windows 10 se quedó en **Emoji 12**. No falla ruidosamente: la tarjeta se ve rota
y nadie se entera hasta que alguien manda una foto (ya pasó el 04-sep-2026 con 🪆).

POR QUÉ UN MAPA Y NO SÓLO CAMBIAR EL CATÁLOGO. El catálogo ya se corrigió, pero el ícono de
cada actividad queda CONGELADO en el `data.json` del cuaderno el día que se crea: todos los
cuadernos ya entregados —y las siete muestras públicas— siguen con el ícono viejo adentro.
Así que además se traduce AL MOSTRAR: el player lo recibe en `window.EMOJI_COMPAT` (lo pinta
`actividades_web.html()` con ESTE mapa, para que haya una sola copia en este repo) y el
desglose que lee la app de Kydo ya sale traducido.

QUÉ HAY ADENTRO: los dos de hoy y los que se sacaron del catálogo el 04-sep-2026 (commit
0c76009, bloque U+1FA70–1FAFF: Emoji 12 a 15), que siguen vivos en los `data.json` viejos.
Cada reemplazo es el que ya usa el catálogo para esa tarjeta: se eligió por lo que la tarjeta
enseña, no por el parecido gráfico.

La app de Kydo (repo ct3d, `kydo/emoji_compat.py`) tiene su PROPIA copia de este mapa, a
propósito: son dos sistemas y no comparten código (regla «un sistema = una carpeta»).
"""

#: emoji que no se dibuja → uno de Emoji ≤ 5 que sí (orden: las secuencias van antes que sus
#: partes, ver `compat`).
EMOJI_COMPAT = {
    "🥷": "🥋",          # Tablas ninja (Emoji 13) — 01-oct-2026
    "🟰": "⚖️",          # Despejá la x / Fracciones equivalentes (Emoji 14) — 01-oct-2026
    # sacados del catálogo el 04-sep-2026, vivos en cuadernos ya entregados:
    "❤️‍🩹": "⚕️",        # Mitos, ITS y tipos de violencia (Emoji 13.1)
    "🪆": "📦",          # La palabra que abarca (13)
    "🫀": "❤️",          # ¿De qué sistema es? / Sistema reproductor (13)
    "🪵": "🌳",          # Objeto o material (13)
    "🪢": "➰",          # El conector justo (13)
    "🪟": "🏠",          # ¿De qué material es? (13)
    "🪜": "📊",          # Ordená los números / La cuenta paso a paso (13)
    "🪶": "🐦",          # Pueblos y colonia (13)
    "🪙": "💰",          # Pago exacto (13)
    "🫧": "💧",          # Suma rápida (14)
    "🫨": "🌋",          # Sistema nervioso (15)
    "🩺": "🏥",          # ¿Se contagia? / Anticoncepción (12, falta en celulares viejos)
    "🩹": "⚕️",          # Corregí el error (12)
    "🪐": "🌍",          # ¿Terrestre o gaseoso? / heliocentrismo (12)
}

# Las claves más largas primero: «❤️‍🩹» contiene «🩹», y reemplazar la parte dejaría «❤️‍⚕️».
_ORDEN = sorted(EMOJI_COMPAT, key=len, reverse=True)


def compat(texto):
    """El texto con cada emoji del mapa cambiado por uno que se dibuja en cualquier lado."""
    if not texto:
        return texto or ""
    for k in _ORDEN:
        if k in texto:
            texto = texto.replace(k, EMOJI_COMPAT[k])
    return texto
