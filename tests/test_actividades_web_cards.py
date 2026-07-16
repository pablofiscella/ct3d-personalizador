import actividades_web as aw
import actividades_web_cards as awc


def test_banda_de_resuelve_todo_el_catalogo():
    """16-jul-2026: _banda_de() sampleaba solo (mini,2)/(media,5)/(grande,8)
    — los juegos NAP exclusivos de 9-12 (laboratorio_electrico,
    fracciones_equivalentes, traductor_algebraico, etc.) nunca encontraban
    banda y generar_tema() los saltaba para siempre (`if banda is None:
    continue`), así que su card nunca se generaba: la galería/editor caían
    al fallback de solo-título por más que el juego existiera en el player
    real. Ningún juego del catálogo completo debe quedar sin banda."""
    for j in aw._catalogo_juegos():
        banda, edad = awc._banda_de(j["id"])
        assert banda is not None, f"{j['id']} no encontró banda"
        assert edad is not None


def test_banda_de_edades_9_a_12():
    assert awc._banda_de("laboratorio_electrico") == ("grande", "9")
    assert awc._banda_de("fracciones_equivalentes") == ("grande", "9")
    assert awc._banda_de("fracciones_avanzado") == ("grande", "10")
    assert awc._banda_de("traductor_algebraico") == ("grande", "12")
    # uno del rango viejo (8 años) sigue igual, sin regresión
    assert awc._banda_de("cajero_automatico") == ("grande", "8")
