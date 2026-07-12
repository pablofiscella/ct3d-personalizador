"""aventura_audio.py — narración por nodo del prototipo "Elegí tu aventura": un MP3 por
nodo del grafo YA PERSONALIZADO (el texto trae el nombre del chico adentro), con el
mismo motor de voz que el audiolibro (audiolibro.tts_mp3 — ElevenLabs Lizy, acento
argentino, resguardo a OpenAI si falla).

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


def generar(token, nodos, dest_dir, api_key=None, tts=audiolibro.tts_mp3, progress=None):
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
        mp3 = tts(api_key, n["texto"], seed=seed)
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
