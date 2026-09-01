"""La tipografía se busca UNA vez por proceso, no en cada pedido de letra.

Encontrado el 31-ago-2026 con el motor de producción colgado. `_font` hacía
`glob.glob(f"{KIT}/**/Fredoka*.ttf", recursive=True)` —un recorrido recursivo de las
~42.000 entradas del árbol del proyecto— **en cada llamada**. Medido: una hoja de
calendario llama a `_font` 39 veces, así que 6,9 de sus 7,3 segundos (95%) se iban
buscando un archivo que no se mueve nunca. Como el arranque encola ~576 hojas de warm,
el motor quedaba al 143% de CPU sin completar NINGÚN render: cero archivos escritos en
20 minutos y `/health` sin contestar.

El arreglo no cambia lo que se dibuja (se verificó que la hoja sale con el mismo sha),
sólo deja de buscar. Este guardián falla si alguien vuelve a meter el glob adentro de la
función de fuente.

Probado en rojo contra el código de antes: los 16 módulos globeaban una vez por letra.
"""
import glob
import importlib

import pytest

# 15 la llaman `_font`; stl3d la llama `_fuente_titulo`.
MODULOS = [("antifaces", "_font"), ("bundle_fiesta", "_font"), ("calendario", "_font"),
           ("capsula_tiempo", "_font"), ("certificado", "_font"), ("corona", "_font"),
           ("cuaderno", "_font"), ("invitacion_web", "_font"), ("libro", "_font"),
           ("memoria", "_font"), ("menu_infantil", "_font"), ("papertoys", "_font"),
           ("rompecabezas", "_font"), ("rutina", "_font"), ("stl3d", "_fuente_titulo"),
           ("video_invitacion", "_font")]


@pytest.mark.parametrize("nombre,fn", MODULOS)
def test_pedir_cinco_letras_busca_el_ttf_una_sola_vez(nombre, fn, monkeypatch):
    mod = importlib.import_module(nombre)
    mod._FREDOKA = None  # como un proceso recién arrancado

    veces = {"n": 0}
    real = glob.glob

    def contado(*a, **k):
        veces["n"] += 1
        return real(*a, **k)

    monkeypatch.setattr(glob, "glob", contado)
    fuente = getattr(mod, fn)
    for sz in (20, 30, 40, 50, 60):
        fuente(sz)

    assert veces["n"] == 1, (
        "%s.%s globeó %d veces para 5 pedidos de letra; tiene que globear 1 sola"
        % (nombre, fn, veces["n"]))


@pytest.mark.parametrize("nombre,fn", MODULOS)
def test_la_cache_encuentra_la_fredoka_de_verdad(nombre, fn):
    """Que no globee está bien sólo si además ENCUENTRA la fuente: una caché que
    guarda una lista vacía no falla, pero deja todo dibujado con la DejaVu de
    respaldo y eso no se nota hasta ver una pieza impresa."""
    mod = importlib.import_module(nombre)
    mod._FREDOKA = None
    rutas = mod._fuentes_fredoka()

    assert rutas, "%s no encuentra ninguna Fredoka" % nombre
    assert all(p.endswith(".ttf") for p in rutas), rutas
    assert all("Fredoka" in p for p in rutas), rutas
