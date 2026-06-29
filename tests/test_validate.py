import io
import pytest
from PIL import Image
from ia_kit.validate import validar_png, ImagenInvalida


def _png(w, h):
    buf = io.BytesIO()
    Image.new("RGB", (w, h), "white").save(buf, "PNG")
    return buf.getvalue()


def test_acepta_ratio_correcto():
    im = validar_png(_png(1536, 2176), size_esperado=(1536, 2176))
    assert im.size == (1536, 2176)


def test_acepta_misma_relacion_distinta_escala():
    # mismo ratio (3:2) a otra escala -> válido
    validar_png(_png(1536, 1024), size_esperado=(768, 512))


def test_rechaza_ratio_distinto():
    with pytest.raises(ImagenInvalida):
        validar_png(_png(1024, 1024), size_esperado=(1536, 2176))


def test_rechaza_bytes_corruptos():
    with pytest.raises(ImagenInvalida):
        validar_png(b"no soy un png")
