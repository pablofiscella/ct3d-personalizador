import os
from PIL import Image
import libro
import productos
import temas


DATA = {"nombre": "Sofía", "edad": "5", "dedicatoria": "Para nuestra estrella."}


def test_piezas_procedurales_se_generan():
    items = productos.piezas_tipo("safari", "libro")
    assert len(items) == libro.TOTAL_PAGINAS == 10
    nombres = [n for n, _, _ in items]
    assert nombres[0] == "01_portada"
    assert nombres[1] == "02_dedicatoria"
    assert nombres[-1] == "10_fin"
    for idx in (0, 1, 4, 9):   # portada, dedicatoria, una de historia y fin
        img = items[idx][1](DATA)
        assert img.size == (libro.Wp, libro.Hp)


def test_override_reemplaza_la_pieza(tmp_path, monkeypatch):
    monkeypatch.setattr(temas, "TEMAS_DIR", str(tmp_path))
    ov = productos.override_path("safari", "libro", 3)
    os.makedirs(os.path.dirname(ov), exist_ok=True)
    Image.new("RGBA", (77, 88), (10, 20, 30, 255)).save(ov)
    items = productos.piezas_tipo("safari", "libro")
    assert items[3][1](DATA).size == (77, 88)          # la página vino del override
    assert items[4][1](DATA).size == (libro.Wp, libro.Hp)  # las demás siguen procedurales


def test_cuento_personalizado_con_nombre_y_edad():
    textos = libro.cuento(DATA, "safari")
    assert len(textos) == libro.PAGINAS_HISTORIA
    assert sum("Sofía" in t for t in textos) >= 4       # protagonista en casi todas
    assert any("contar hasta 5" in t for t in textos)   # la edad entra en la historia
    assert any("safari" in t or "sabana" in t for t in textos)  # ambientación del tema


def test_cuento_tema_desconocido_usa_fallback():
    textos = libro.cuento({"nombre": "Mateo"}, "tema-que-no-existe")
    assert len(textos) == libro.PAGINAS_HISTORIA
    assert any("Mateo" in t for t in textos)
    assert any("mundo mágico" in t for t in textos)


def test_campos_se_respetan_en_las_paginas():
    a = libro.portada({"nombre": "Sofía", "edad": "5"}, "safari").tobytes()
    b = libro.portada({"nombre": "Valentina", "edad": "5"}, "safari").tobytes()
    assert a != b                                       # el nombre cambia la portada
    c = libro.dedicatoria(DATA, "safari").tobytes()
    d = libro.dedicatoria({**DATA, "dedicatoria": "Otro texto distinto."}, "safari").tobytes()
    assert c != d                                       # la dedicatoria cambia su página


def test_paginas_deterministicas():
    a = libro.pagina_historia(2, DATA, "safari").tobytes()
    b = libro.pagina_historia(2, DATA, "safari").tobytes()
    assert a == b                                       # mismo pedido -> mismo libro


def test_tipo_publicado_y_preview():
    pub = productos.tipos_publicos()["libro"]
    assert pub["campos"] == ["nombre", "edad", "dedicatoria"]
    assert "dedicatoria" in pub["campos_labels"]
    assert len(pub["piezas"]) == 10
    img = productos.preview(DATA, "safari", "libro")
    assert img.size[0] <= 1000 and img.size[1] <= 1000
