import os
from PIL import Image, ImageDraw
import cuaderno


def _mk_tema(tmp_path, identicas=False):
    base = tmp_path / "circo"; (base / "ia_draft").mkdir(parents=True)
    (base / "tema.json").write_text('{"nombre":"Circo — Gran Función","edades":[1,2,3]}',
                                    encoding="utf-8")
    # hoja de stickers: 6 figuras separadas (cada una = un componente de alpha),
    # DISTINTAS entre sí por default — el dedup perceptual de personajes_decorativos
    # colapsa las idénticas a una sola (comportamiento deseado, con test propio).
    im = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    colores = [(200, 80, 80), (80, 160, 200), (90, 190, 90),
               (220, 170, 60), (160, 90, 200), (240, 240, 240)]
    for i in range(6):
        x = 120 + (i % 3) * 300; y = 150 + (i // 3) * 360
        c = colores[0] if identicas else colores[i]
        d.ellipse([x, y, x + 150, y + 230], fill=c + (255,))
        if identicas or i % 2 == 0:
            d.ellipse([x + 45, y + 50, x + 95, y + 100], fill=(30, 30, 30, 255))
        else:
            d.rectangle([x + 30, y + 140, x + 120, y + 200], fill=(20, 20, 60, 255))
    im.save(base / "ia_draft" / "stickers_1.png")
    return base


def test_tema_nombre_corto(tmp_path, monkeypatch):
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    _mk_tema(tmp_path)
    assert cuaderno._tema_nombre("circo") == "Circo"          # corta antes del guión


def test_personajes_decorativos_devuelve_n_imagenes(tmp_path, monkeypatch):
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    monkeypatch.setattr(cuaderno, "_es_personaje_vision", lambda *a: None)  # sin red en tests
    _mk_tema(tmp_path)
    imgs = cuaderno.personajes_decorativos("circo", n=2)
    assert len(imgs) == 2
    for im in imgs:
        assert im.mode == "RGBA" and im.size[0] > 0


def test_personajes_decorativos_dedup_figuras_identicas(tmp_path, monkeypatch):
    """La misma figura repetida en la hoja NO puede salir 2 veces en una pieza
    (bug real: 2-3 monitos idénticos en la corona de safari)."""
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    monkeypatch.setattr(cuaderno, "_es_personaje_vision", lambda *a: None)
    _mk_tema(tmp_path, identicas=True)
    imgs = cuaderno.personajes_decorativos("circo", n=3)
    assert len(imgs) == 1                                     # 6 copias idénticas → 1


def test_personajes_decorativos_filtra_objetos_por_vision(tmp_path, monkeypatch):
    """Con el clasificador de visión disponible, los recortes etiquetados como
    objeto quedan afuera (bug real: una MESA y un FRASCO de 'personajes')."""
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    _mk_tema(tmp_path)
    paths = cuaderno._extraer_monstruos("circo")
    nombres = [os.path.basename(p) for p in paths]
    # el primero es "objeto" (no aparece en el dict); el resto personajes distintos
    tipos = {nm: "payaso%d" % i for i, nm in enumerate(nombres[1:])}
    monkeypatch.setattr(cuaderno, "_es_personaje_vision", lambda *a: tipos)
    imgs = cuaderno.personajes_decorativos("circo", n=6)
    assert 0 < len(imgs) <= len(tipos)                        # el "objeto" no entra


def test_personajes_decorativos_sin_stickers_lista_vacia(tmp_path, monkeypatch):
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    d = tmp_path / "vacio"; d.mkdir()
    (d / "tema.json").write_text("{}", encoding="utf-8")
    assert cuaderno.personajes_decorativos("vacio", n=2) == []   # sin fallback genérico


def test_regenerar_pagina_guarda_override_y_no_afecta_otras(tmp_path, monkeypatch):
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    _mk_tema(tmp_path)
    base = cuaderno.base_paginas("circo", 6)   # arma y cachea el cuaderno canónico
    n = len(base)
    assert n > 2
    ok = cuaderno.regenerar_pagina("circo", 6, 1)
    assert ok is True
    od = cuaderno._override_dir("circo", 6)
    assert os.path.isfile(os.path.join(od, "pg01.png"))   # quedó guardada como override
    assert not os.path.isfile(os.path.join(od, "pg00.png"))   # las demás no se tocaron
    assert not os.path.isfile(os.path.join(od, "pg02.png"))
    # pagina_efectiva ahora sirve el override para la 1, la canónica para el resto
    efectiva1 = cuaderno.pagina_efectiva("circo", 6, 1)
    assert efectiva1.size == base[1].size


def test_regenerar_pagina_idx_invalido_devuelve_false(tmp_path, monkeypatch):
    monkeypatch.setattr(cuaderno, "TEMAS", str(tmp_path))
    _mk_tema(tmp_path)
    cuaderno.base_paginas("circo", 6)
    assert cuaderno.regenerar_pagina("circo", 6, 9999) is False


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
