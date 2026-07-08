"""Guardián de ANCHO (regla de Pablo 9-jul-2026: «lográ que nunca una actividad
se vaya del ancho»): se renderiza el cuaderno completo para varias edades y
semillas y se verifica píxel a píxel que ninguna página de actividad tenga
contenido pegado al borde de la hoja (fuera del banner, pie y nº de página).
Las figuras del fixture son ANCHAS a propósito (aspecto ~1.9, como una corona)
para estresar los layouts de filas (sumas, restas, patrón, contar)."""
import numpy as np
import pytest
from PIL import Image, ImageDraw

import cuaderno

MARGEN_MIN = 24          # px a 150dpi ≈ 4mm — nada de contenido más allá de esto


def _mk_tema_ancho(tmp_path):
    base = tmp_path / "circo"; (base / "ia_draft").mkdir(parents=True)
    (base / "tema.json").write_text('{"nombre":"Circo","edades":[1,2,3]}', encoding="utf-8")
    im = Image.new("RGBA", (1600, 1024), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    colores = [(200, 80, 80), (80, 160, 200), (90, 190, 90),
               (220, 170, 60), (160, 90, 200), (120, 120, 40)]
    for i in range(6):
        x = 60 + (i % 2) * 800; y = 80 + (i // 2) * 320
        # figuras BIEN anchas (280x150 ≈ aspecto 1.9) con detalle interno distinto
        d.ellipse([x, y, x + 280, y + 150], fill=colores[i] + (255,))
        d.ellipse([x + 30 + i * 25, y + 40, x + 80 + i * 25, y + 90], fill=(30, 30, 30, 255))
    im.save(base / "ia_draft" / "stickers_1.png")
    return base


@pytest.mark.parametrize("edad", ["2", "5", "6"])
def test_ninguna_actividad_se_va_del_ancho(tmp_path, monkeypatch, edad):
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    monkeypatch.setattr(cuaderno, "_es_personaje_vision", lambda *a: None)
    _mk_tema_ancho(tmp_path)
    for seed in (1, 7, 42):
        acts, _sols = cuaderno._build("circo", edad, seed)
        for n, pg in enumerate(acts[1:], start=1):     # sin portada (arte a sangre)
            a = np.array(pg.convert("L"))
            # zona de contenido: debajo del banner, arriba del pie/nº de página
            zona = a[cuaderno.BANNER_H + 8:cuaderno.Hp - 110]
            cols = np.where((zona < 245).any(axis=0))[0]
            if not len(cols):
                continue
            assert cols.max() <= cuaderno.Wp - MARGEN_MIN, \
                "página %d (edad %s, seed %d): contenido hasta x=%d" % (n, edad, seed, cols.max())
            assert cols.min() >= MARGEN_MIN, \
                "página %d (edad %s, seed %d): contenido desde x=%d" % (n, edad, seed, cols.min())
