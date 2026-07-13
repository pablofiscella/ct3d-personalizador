"""Cards de la galería "qué incluye" de actividades-web = SCREENSHOTS reales del
player interactivo (Pablo 13-jul-2026, viendo la primera versión con páginas
estilo cuaderno impreso: "Las imagenes que estas mostrando son las viejas. Asi
es como quiero que las muestres tal cual se ven en la web" — con una captura
del player real como referencia). Nada de mockups ni de reusar el cuaderno
impreso: se genera un token de PRUEBA, se abre en un browser headless
(Playwright/Chromium, YA instalado en esta máquina para los tests), se llama
`Shell.abrir(<juego>)` (la misma función que usa el player al tocar una
carta) y se saca una captura — pixel a pixel lo que ve el comprador.

Se genera UNA VEZ por tema (no por venta): 19 PNGs en
temas/<tema>/actividades_cards/<juego_id>.png (gitignored, como ia_maestra.png
— se regenera con este script, no se edita a mano). El bloqueo por edad se
sigue pintando ENCIMA de la captura real al servir (actividades_web._apagar_bloqueado),
no hace falta una captura por edad.

Uso:
  CLI:  python actividades_web_cards.py <tema> [--forzar]
        python actividades_web_cards.py --todos [--forzar]
"""
import os
import sys
import zlib

import actividades_web
from cuaderno import TEMAS

CARDS_DIR_NOMBRE = "actividades_cards"
_PUERTO_LOCAL = int(os.environ.get("ACTIVIDADES_CARDS_PUERTO", "8797"))
# banda representativa por juego: la PRIMERA banda (mini→media→grande) que lo
# incluye — mismo criterio de precedencia que actividades_web._catalogo_juegos().
_BANDAS = (("mini", "2"), ("media", "5"), ("grande", "8"))
# minP real del player (actividades_player.js GAMES.<id>.minP) — si el tema
# no junta suficientes personajes, el MENÚ REAL ya oculta esa carta (real:
# "un-espacio-de-locura" solo detecta 3 personajes → sudoku/bingo, que piden
# 4, quedan ocultos para cualquier comprador de ese tema, no es cosa mía).
# Forzar Shell.abrir() salteando ese guard rompía la captura (ícono de
# imagen rota) — hay que replicar el mismo guard acá.
_MINP = {"memotest": 3, "sudoku": 4, "agrupar": 2, "quefalta": 3, "bingo": 4}


def _cards_dir(tema):
    return os.path.join(TEMAS, tema, CARDS_DIR_NOMBRE)


def card_path(tema, game_id):
    return os.path.join(_cards_dir(tema), "%s.png" % game_id)


def _banda_de(game_id):
    """Primera banda (mini→media→grande) que incluye este juego."""
    for banda, edad in _BANDAS:
        if any(m["id"] == game_id for m in actividades_web._menu(banda, edad)):
            return banda, edad
    return None, None


def _token_preview(tema, banda):
    # corto y determinístico a propósito: _TOKEN_RE de actividades_web tolera
    # hasta 32 chars, y "preview-cards-un-espacio-de-locura-grande" (41) lo
    # pasaba de largo — crear() lo detectaba y generaba un token AL AZAR en
    # su lugar (bug real: la card pedía la URL fija de siempre, que nunca se
    # había creado, y tiraba 404).
    h = zlib.crc32(tema.encode()) & 0xffffffff
    codigo = {"mini": "mi", "media": "me", "grande": "gr"}[banda]
    return "pvc%s-%08x" % (codigo, h)


def _asegurar_token(tema, banda, edad):
    """Token de PRUEBA para capturar screenshots (no es una venta real) —
    regenera solo si no existe, así correr el script de nuevo es barato."""
    token = _token_preview(tema, banda)
    d = os.path.join(actividades_web.ACT_DIR, token)
    if not os.path.isfile(os.path.join(d, "data.json")):
        actividades_web.crear({"edad": edad}, tema, token=token)
    return token


def generar_tema(tema, forzar=False, progress=None):
    """Genera las 19 cards del tema. Devuelve la lista de juegos generados."""
    from playwright.sync_api import sync_playwright
    import servicio
    import http.server
    import threading
    import time

    log = progress or (lambda m: None)
    juegos = actividades_web._catalogo_juegos()
    pendientes = juegos if forzar else [
        j for j in juegos if not os.path.isfile(card_path(tema, j["id"]))]
    if not pendientes:
        log("%s: las 19 cards ya existen (usá forzar=True para regenerar)" % tema)
        return []

    os.makedirs(_cards_dir(tema), exist_ok=True)
    por_banda = {}
    for j in pendientes:
        banda, edad = _banda_de(j["id"])
        if banda is None:
            continue
        por_banda.setdefault(banda, []).append(j["id"])

    srv = http.server.HTTPServer(("127.0.0.1", _PUERTO_LOCAL), servicio.Handler)
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    time.sleep(0.3)
    hechos = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 700, "height": 1000},
                                     device_scale_factor=2)
            for banda, ids in por_banda.items():
                edad = dict(_BANDAS)[banda]
                token = _asegurar_token(tema, banda, edad)
                page.goto("http://127.0.0.1:%d/act/%s/" % (_PUERTO_LOCAL, token),
                          wait_until="networkidle")
                page.wait_for_function("typeof D !== 'undefined' && D !== null", timeout=8000)
                n_personajes = page.evaluate("P.length")
                for gid in ids:
                    if n_personajes < _MINP.get(gid, 0):
                        # el MENÚ REAL ya oculta esta carta para este tema
                        # (personajes insuficientes) — no forzarla acá:
                        # el fallback de preview_mock_extra la resuelve sola.
                        log("%s/%s SALTEADO (tema con %d personajes, %s pide %d)"
                            % (tema, gid, n_personajes, gid, _MINP[gid]))
                        continue
                    page.evaluate("(id) => { Shell.abrir(id); }", gid)
                    page.wait_for_timeout(350)
                    if gid == "memotest":
                        # arranca con TODAS las cartas boca abajo (sin peek —
                        # así es el juego real, no un estado inventado): para
                        # que la card de marketing muestre algo del tema,
                        # tocamos 2 cartas (una interacción real y alcanzable,
                        # no un estado falso) antes de la captura.
                        try:
                            botones = page.query_selector_all(".cartaMemo")
                            if len(botones) >= 2:
                                botones[0].click(); page.wait_for_timeout(150)
                                botones[2].click(); page.wait_for_timeout(150)
                        except Exception:
                            pass
                    page.screenshot(path=card_path(tema, gid))
                    hechos.append(gid)
                    log("%s/%s OK" % (tema, gid))
            browser.close()
    finally:
        srv.shutdown()
        srv.server_close()   # shutdown() para el loop, NO libera el socket
    return hechos


if __name__ == "__main__":
    forzar = "--forzar" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("Uso: python actividades_web_cards.py <tema> [--forzar]")
        print("     python actividades_web_cards.py --todos [--forzar]")
        sys.exit(1)
    if args[0] == "--todos":
        temas = sorted(d for d in os.listdir(TEMAS)
                        if os.path.isdir(os.path.join(TEMAS, d)) and not d.startswith("_"))
    else:
        temas = args
    for tema in temas:
        hechos = generar_tema(tema, forzar=forzar, progress=print)
        print("%s: %d cards generadas" % (tema, len(hechos)))
