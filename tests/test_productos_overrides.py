import os
from PIL import Image
import productos
import temas


def test_sin_override_usa_diseno_procedural(tmp_path, monkeypatch):
    monkeypatch.setattr(temas, "TEMAS_DIR", str(tmp_path))
    items = productos.piezas_tipo("safari", "certificado")
    assert len(items) == 1
    img = items[0][1]({"nombre": "Sofía", "edad": "5"})
    assert img.size[0] > 100   # el diseño procedural real, no un override


def test_con_override_usa_el_archivo_subido(tmp_path, monkeypatch):
    monkeypatch.setattr(temas, "TEMAS_DIR", str(tmp_path))
    ov = productos.override_path("safari", "certificado", 0)
    os.makedirs(os.path.dirname(ov), exist_ok=True)
    Image.new("RGBA", (77, 88), (10, 20, 30, 255)).save(ov)
    items = productos.piezas_tipo("safari", "certificado")
    img = items[0][1]({"nombre": "Sofía"})
    assert img.size == (77, 88)   # vino del override, no del diseño procedural


def test_override_path_usa_idx_correcto():
    p0 = productos.override_path("circo", "corona", 0)
    p1 = productos.override_path("circo", "corona", 1)
    assert p0.endswith(os.path.join("overrides", "corona", "0.png"))
    assert p1.endswith(os.path.join("overrides", "corona", "1.png"))
    assert p0 != p1
