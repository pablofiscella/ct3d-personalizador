import json
import os
from ia_kit import catalogo


def _tema(tmp_path):
    d = tmp_path / "safari"
    d.mkdir()
    (d / "tema.json").write_text(json.dumps(
        {"id": "safari", "kit": {"accent": "#E0514A", "ink": "#4A4A4A", "font": "Baloo2-VF.ttf"}}))
    return str(tmp_path)


def test_paleta_lee_tema_json(tmp_path):
    pal = catalogo.paleta_de(_tema(tmp_path), "safari")
    assert pal["accent"] == "#E0514A" and pal["ink"] == "#4A4A4A"


def test_paleta_default_si_falta(tmp_path):
    d = tmp_path / "x"; d.mkdir(); (d / "tema.json").write_text("{}")
    pal = catalogo.paleta_de(str(tmp_path), "x")
    assert pal["accent"] and pal["ink"]  # hay defaults


def test_invitacion_y_afiche_por_edad():
    keys = {p.key: p for p in catalogo.PIEZAS}
    assert keys["invitacion"].por_edad is True
    assert keys["afiche"].por_edad is True
    assert keys["topper"].por_edad is False


def test_prompt_incluye_paleta_y_sin_texto():
    pal = {"accent": "#E0514A", "ink": "#4A4A4A", "font": "Baloo2"}
    inv = next(p for p in catalogo.PIEZAS if p.key == "invitacion")
    txt = catalogo.prompt_de(pal, inv, edad=3)
    assert "#E0514A" in txt
    assert "sin texto" in txt.lower() or "no text" in txt.lower()
    # la INVITACIÓN se personaliza en el editor: el arte NO lleva el número de edad
    assert "3" not in txt


def test_prompt_afiche_si_lleva_numero():
    pal = {"accent": "#E0514A", "ink": "#4A4A4A", "font": "Baloo2"}
    af = next(p for p in catalogo.PIEZAS if p.key == "afiche")
    txt = catalogo.prompt_de(pal, af, edad=3)
    assert "3" in txt  # el afiche es estático: el número va ilustrado en el arte


def test_catalogo_cubre_extras_canonicos():
    keys = {p.key for p in catalogo.PIEZAS}
    por_edad = ["afiche", "topper", "topper_palito", "base_torta", "stickers",
                "separadores", "etiqueta_botella", "cajita_sorpresa", "decoracion_sorbetes"]
    universal = ["banderin", "etiquetas_multiuso", "wrappers_cupcakes", "tarjetas_agradecimiento"]
    for b in por_edad + universal + ["invitacion"]:
        assert b in keys, b
