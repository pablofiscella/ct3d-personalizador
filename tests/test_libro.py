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


def test_override_es_la_ilustracion_y_el_texto_sigue_vivo(tmp_path, monkeypatch):
    """En el libro el override NO tapa la página completa: es el ARTE de la escena.
    La página sigue siendo A4 y el texto personalizado lo sigue escribiendo el motor."""
    monkeypatch.setattr(temas, "TEMAS_DIR", str(tmp_path))
    ov = libro.override_escena_path("safari", 2)
    assert ov == productos.override_path("safari", "libro", 2)  # mismo path que el dash
    os.makedirs(os.path.dirname(ov), exist_ok=True)
    Image.new("RGBA", (500, 500), (200, 30, 30, 255)).save(ov)   # arte rojo
    items = productos.piezas_tipo("safari", "libro")
    pg = items[2][1](DATA)   # 03_pagina_1: su texto lleva el nombre del chico
    assert pg.size == (libro.Wp, libro.Hp)                       # sigue siendo la página A4
    assert pg.getpixel((libro.Wp // 2, 500))[:3] == (200, 30, 30)  # la escena es el arte subido
    otro = items[2][1]({**DATA, "nombre": "Valentina"})
    assert pg.tobytes() != otro.tobytes()                        # el nombre sigue personalizando
    assert items[4][1](DATA).size == (libro.Wp, libro.Hp)        # las demás, procedurales


def test_override_en_portada_dedicatoria_y_fin(tmp_path, monkeypatch):
    monkeypatch.setattr(temas, "TEMAS_DIR", str(tmp_path))
    for idx in (0, 1, 9):
        ov = libro.override_escena_path("safari", idx)
        os.makedirs(os.path.dirname(ov), exist_ok=True)
        Image.new("RGBA", (400, 400), (30, 120, 200, 255)).save(ov)
    items = productos.piezas_tipo("safari", "libro")
    for idx in (0, 1, 9):
        assert items[idx][1](DATA).size == (libro.Wp, libro.Hp)


def test_generador_ia_guarda_overrides(tmp_path, monkeypatch):
    import io
    import libro_ia
    monkeypatch.setattr(temas, "TEMAS_DIR", str(tmp_path))

    class FakeClient:
        def __init__(self):
            self.llamadas = []
        def editar(self, refs, prompt, size, quality="medium"):
            self.llamadas.append((len(refs), prompt, size, quality))
            buf = io.BytesIO()
            Image.new("RGB", (64, 64), (10, 200, 10)).save(buf, "PNG")
            return buf.getvalue()

    cl = FakeClient()
    paths = libro_ia.generar_ilustraciones(cl, "safari", paginas=[2, 9])
    assert [os.path.basename(p) for p in paths] == ["2.png", "9.png"]
    assert all(os.path.isfile(p) for p in paths)
    assert cl.llamadas[0][2] == "1024x1024"       # páginas de historia: panel cuadrado
    assert cl.llamadas[1][2] == "1024x1536"       # FIN: hoja completa vertical
    # el override generado se usa en la página (escena verde)
    pg = libro.pagina_historia(0, DATA, "safari")
    assert pg.getpixel((libro.Wp // 2, 500))[:3] == (10, 200, 10)


def test_prompts_ia_con_ambientacion_y_sin_texto():
    import libro_ia
    p = libro_ia.prompt_pagina("safari", 4)
    assert "sabana" in p                          # ambientación del tema en la escena
    assert "no text" in p                         # el arte va SIN texto (lo escribe el motor)
    assert len(libro_ia._ESCENAS) == libro.TOTAL_PAGINAS


def test_cuento_personalizado_con_nombre_y_edad():
    textos = libro.cuento(DATA, "safari")
    assert len(textos) == libro.PAGINAS_HISTORIA
    assert sum("Sofía" in t for t in textos) >= 4       # protagonista en casi todas
    assert any("contar hasta 5" in t for t in textos)   # la edad entra en la historia
    assert any("safari" in t or "sabana" in t for t in textos)  # ambientación del tema


def test_cuento_tema_desconocido_usa_fallback():
    # un tema sin tema.json es "nuevo" -> 12 páginas de historia (15 en total)
    textos = libro.cuento({"nombre": "Mateo"}, "tema-que-no-existe")
    assert len(textos) == libro.PAGINAS_HISTORIA_NUEVO
    assert any("Mateo" in t for t in textos)
    assert any("mundo mágico" in t for t in textos)


def test_paginas_historia_por_tema():
    # temas existentes: pineados a 7 (no cambia el largo de lo ya vendido)
    assert libro.paginas_historia("safari") == 7
    assert libro.total_paginas("safari") == 10
    # tema nuevo (sin tema.json::libro_paginas_historia): 12 -> 15 en total
    assert libro.paginas_historia("tema-que-no-existe") == 12
    assert libro.total_paginas("tema-que-no-existe") == 15


def test_cuento_extendido_por_arco():
    data = {"nombre": "Mateo", "edad": "6"}
    for historia in ("aventura", "tesoro", "rescate", "gran-dia",
                      "noche-estrellas", "cumple-sorpresa", "pequeno-maestro",
                      "ayudar-a-todos"):
        textos = libro.cuento(dict(data, historia=historia), "tema-que-no-existe")
        assert len(textos) == 12
        assert sum("Mateo" in t for t in textos) >= 3

    # las 3 narrativas clásicas siguen andando igual en temas legado (7 páginas,
    # texto de las primeras páginas IDÉNTICO al de antes de extenderlas)
    for historia in ("tesoro", "rescate", "gran-dia"):
        legado = libro.cuento(dict(data, historia=historia), "safari")
        assert len(legado) == 7
        assert legado == [t.format(**dict(libro.HISTORIAS["safari"], nombre="Mateo",
                                          conteo="contar hasta 6", conteo_num="6"))
                          for t in libro.ARGUMENTOS[historia]]


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
