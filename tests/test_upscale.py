from PIL import Image
from ia_kit import upscale


def test_upscalar_agranda_y_preserva_rgba_y_ratio():
    im = Image.new("RGBA", (500, 700), (255, 0, 0, 128))
    out = upscale.upscalar_imagen(im, objetivo=1400)
    assert max(out.size) >= 1400          # llega al objetivo
    assert out.mode == "RGBA"             # preserva transparencia
    assert abs(out.width / out.height - 500 / 700) < 0.01   # mismo ratio


def test_upscalar_no_achica_ni_supera_maxfactor():
    im = Image.new("RGBA", (2000, 2000))
    out = upscale.upscalar_imagen(im, objetivo=1000)   # ya es grande -> no toca
    assert out.size == (2000, 2000)
