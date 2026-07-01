import os
from PIL import Image, ImageDraw
import cuaderno


def _mk_tema(tmp_path):
    base = tmp_path / "circo"; (base / "ia_draft").mkdir(parents=True)
    (base / "tema.json").write_text('{"nombre":"Circo — Gran Función","edades":[1,2,3]}',
                                    encoding="utf-8")
    # hoja de stickers: 6 figuras separadas (cada una = un componente de alpha)
    im = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(6):
        x = 120 + (i % 3) * 300; y = 150 + (i // 3) * 360
        d.ellipse([x, y, x + 150, y + 230], fill=(200, 80, 80, 255))
        d.ellipse([x + 45, y + 50, x + 95, y + 100], fill=(30, 30, 30, 255))   # detalle interno
    im.save(base / "ia_draft" / "stickers_1.png")
    return base


def test_tema_nombre_corto(tmp_path, monkeypatch):
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    _mk_tema(tmp_path)
    assert cuaderno._tema_nombre("circo") == "Circo"          # corta antes del guión


def test_personajes_decorativos_devuelve_n_imagenes(tmp_path, monkeypatch):
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    _mk_tema(tmp_path)
    imgs = cuaderno.personajes_decorativos("circo", n=2)
    assert len(imgs) == 2
    for im in imgs:
        assert im.mode == "RGBA" and im.size[0] > 0


def test_personajes_decorativos_sin_stickers_lista_vacia(tmp_path, monkeypatch):
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    d = tmp_path / "vacio"; d.mkdir()
    (d / "tema.json").write_text("{}", encoding="utf-8")
    assert cuaderno.personajes_decorativos("vacio", n=2) == []   # sin fallback genérico


def test_build_separa_actividades_y_solucionario(tmp_path, monkeypatch):
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    _mk_tema(tmp_path)
    acts, sols = cuaderno._build("circo", "6", 1)             # banda 6-7
    assert len(acts) >= 20                                    # portada + ~25 actividades (1 por página)
    assert len(sols) >= 1                                     # al menos una hoja de soluciones
    assert all(p.size == (cuaderno.Wp, cuaderno.Hp) for p in acts + sols)
    solo = cuaderno.paginas("circo", "6", con_solucionario=False)
    assert len(solo) == len(acts)                            # sin solucionario = solo actividades


def test_bandas_escalan_por_edad(tmp_path, monkeypatch):
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    _mk_tema(tmp_path)
    n3 = len(cuaderno.paginas("circo", "3", con_solucionario=False))
    n6 = len(cuaderno.paginas("circo", "6", con_solucionario=False))
    assert n3 < n6                                            # 2-3 años tiene menos que 6-7


def test_figura_pts_corazon_cuenta():
    assert len(cuaderno._figura_pts("corazon", 100, 100, 80, 12)) == 12
