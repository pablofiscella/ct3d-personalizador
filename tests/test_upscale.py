import os
from PIL import Image
from ia_kit import upscale


def test_upscalar_draft_llama_progress_por_archivo(tmp_path):
    d = tmp_path / "circo" / "ia_draft"; d.mkdir(parents=True)
    Image.new("RGBA", (500, 500)).save(d / "afiche_1.png")
    Image.new("RGBA", (500, 500)).save(d / "topper_1.png")
    vistos = []
    upscale.upscalar_draft(str(tmp_path), "circo", objetivo=800, progress=vistos.append)
    assert sorted(vistos) == ["afiche_1.png", "topper_1.png"]


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
