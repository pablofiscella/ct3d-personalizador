"""aventura_audio.py — narración por nodo del prototipo "Elegí tu aventura": un MP3 por
nodo del grafo YA PERSONALIZADO (el texto trae el nombre del chico adentro), con el
mismo motor de voz que el audiolibro (audiolibro.tts_mp3 — ElevenLabs, acento argentino,
resguardo a OpenAI si falla). Voz default: Malena (15-jul-2026, pedido de Pablo — la
misma voz elegida como default para el audiolibro; antes de esto, `generar()` no pasaba
`voz` a tts_mp3 y caía siempre en Lizy pese al cambio de default del lado de la tienda,
porque ese cambio solo vive en lo que la tienda ENVÍA, no en el default de tts_mp3).

A diferencia del arte (temas/<tema>/overrides/aventura/, cacheado por TEMA porque no
lleva texto), el audio se genera POR COMPRA en aventura_web/<token>/audio/<nodo_id>.mp3:
el texto de cada nodo trae el nombre del chico adentro, así que no hay nada para
cachear entre compras.

Uso: OPENAI_API_KEY=... ELEVENLABS_API_KEY=... python aventura_audio.py <token>
"""
import os
import sys
import zlib

import audiolibro


def _etiquetar(nid, texto):
    """Reusa audiolibro._etiqueta_pagina (etiquetas v3 de emoción) — SIN esto,
    ElevenLabs v3 tiene que adivinar la emoción del texto crudo (sobre todo en
    diálogo entre comillas) y puede salir plano o sobreactuado/distorsionado
    (feedback real de Pablo, 15-jul-2026: "suena saturado y falta de
    entonación" en la primera muestra sin etiquetar). `hook` (siempre el primer
    nodo de cualquier aventura) recibe el mismo trato de "tapa" que la portada
    del audiolibro lineal ([warmly]) MÁS [slows down] — combinación confirmada
    por Pablo tras escuchar 3 muestras (la sola [warmly] sonaba mejor pero
    "le falta un poco más de entonación y un poco más lento o más pausado").
    El resto usa solo las reglas por CONTENIDO de _etiqueta_pagina (no hay
    pos/total: el grafo no es lineal)."""
    if nid == "hook":
        # total tiene que ser > 2: con total=2, pos==total-2 (0==0) coincide
        # ANTES de llegar a pos==0 y gana "[slows down]" en vez de "[warmly]".
        # Orden [warmly] antes de [slows down]: es el orden exacto que Pablo
        # escuchó y confirmó (muestra v3, 15-jul-2026) — no cambiar sin volver
        # a probar, no hay garantía de que el orden le dé lo mismo al modelo.
        return audiolibro._etiqueta_pagina(texto, pos=0, total=3).replace(
            "[warmly] ", "[warmly] [slows down] ", 1)
    return audiolibro._etiqueta_pagina(texto)


def generar(token, nodos, dest_dir, api_key=None, tts=audiolibro.tts_mp3, progress=None,
           voz="malena"):
    """nodos: dict nodo_id -> {"texto": ...} (el grafo YA personalizado, tal cual sale
    del manifest). Genera dest_dir/<nodo_id>.mp3 para cada uno — saltea los que ya
    existen, así una corrida cortada a mitad de camino se puede reintentar sin repetir
    trabajo ni gastar de más. Devuelve la lista de paths."""
    os.makedirs(dest_dir, exist_ok=True)
    seed = zlib.crc32(token.encode())
    items = sorted(nodos.items())
    out = []
    for i, (nid, n) in enumerate(items):
        p = os.path.join(dest_dir, "%s.mp3" % nid)
        if os.path.isfile(p):
            out.append(p)
            continue
        if progress:
            progress("Nodo %d de %d (%s)…" % (i + 1, len(items), nid))
        mp3 = tts(api_key, _etiquetar(nid, n["texto"]), seed=seed, voz=voz)
        with open(p, "wb") as f:
            f.write(mp3)
        out.append(p)
    return out


if __name__ == "__main__":
    import aventura_web as avw
    token = sys.argv[1]
    reg = avw._cargar(token)
    if not reg:
        raise SystemExit(
            "token %r no existe (¿corriste aventura_web.crear primero?)" % token)
    key = os.environ.get("OPENAI_API_KEY")
    generar(token, reg["nodos"], avw.audio_dir(token), api_key=key, progress=print)
    print("LISTO")
