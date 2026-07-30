"""La marca sale del DATO, nunca escrita a mano.

Pablo, 30-jul-2026: "se siguen mezclando cosas de casatridimensional y me preocupa". Tenía
razón: aparecieron cuatro fugas en un día y todas por lo mismo — una app, dos marcas, y cada
superficie compartida tiene que elegir.

Las dos peores estaban en FALLBACKS, que es donde una fuga se esconde mejor: sólo aparecen
cuando algo falla, así que nadie las ve hasta que le pasa a un cliente.
  · `_render_portada` — la tapa dibujada. Un cuaderno ESCOLAR sin portada de grado cae acá.
  · `_render_juego_card_fallback` — la tarjeta de reemplazo de una actividad.
"""
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
import actividades_web as A  # noqa: E402


def test_la_marca_sale_de_la_linea():
    assert A.marca_de(True) == "KYDO"
    assert A.marca_de(False) == "CASATRIDIMENSIONAL"
    assert A.marca_de(None) == "CASATRIDIMENSIONAL"      # ante la duda, la de siempre


def test_ninguna_funcion_de_dibujo_escribe_la_marca_a_mano():
    """El guardián: si alguien vuelve a poner "CASATRIDIMENSIONAL" dentro de un `dr.text`,
    esto falla. Es la única forma de que no vuelva a pasar por cuarta vez."""
    src = open(os.path.join(BASE, "actividades_web.py"), encoding="utf-8").read()
    malas = []
    for m in re.finditer(r"dr\.text\([^)]*\)", src, re.S):
        if "CASATRIDIMENSIONAL" in m.group(0) or '"KYDO"' in m.group(0):
            malas.append(m.group(0)[:80])
    assert not malas, ("hay marca escrita a mano en un dibujo; usá marca_de(escolar): %s"
                       % malas)


def test_el_player_y_python_dicen_lo_mismo():
    """`marcaDelCuaderno()` en el player y `marca_de()` acá tienen que coincidir: si se
    separan, la tapa dice una marca y el visor otra."""
    js = open(os.path.join(BASE, "actividades_player.js"), encoding="utf-8").read()
    m = re.search(r"return \(typeof D [^;]*D\.escolar_on\) \? \"([^\"]+)\" : \"([^\"]+)\";", js)
    assert m, "no se encontró marcaDelCuaderno en el player"
    assert m.group(1).upper() == A.marca_de(True).upper()
    assert m.group(2).upper() == A.marca_de(False).upper()


def test_el_fallback_de_tarjeta_acepta_la_linea():
    """Si la firma pierde el parámetro, la tarjeta vuelve a decir la marca fija."""
    import inspect
    sig = inspect.signature(A._render_juego_card_fallback)
    assert "escolar" in sig.parameters
