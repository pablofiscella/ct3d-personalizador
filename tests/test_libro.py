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


def test_sin_pie_saca_la_url_sin_tocar_el_resto(tmp_path, monkeypatch):
    """15-jul-2026: las fotos de Mercado Libre de los audiolibros reusaban
    páginas del PDF del producto imprimible (con "casatridimensional.com.ar"
    al pie) — ML las tomó como derivación fuera de la plataforma y puso en
    revisión las 22 publicaciones desde el 10-jul. sin_pie=True saca SOLO el
    pie, sin afectar el resto de la página (portada, dedicatoria, historia,
    fin — los 4 tipos de página)."""
    monkeypatch.setattr(temas, "TEMAS_DIR", str(tmp_path))
    for idx in (0, 1, 4, 9):   # portada, dedicatoria, historia, fin
        con_pie = libro.pagina_libro(idx, DATA, "safari", catalogo=True, sin_pie=False)
        sin_pie = libro.pagina_libro(idx, DATA, "safari", catalogo=True, sin_pie=True)
        assert con_pie.size == sin_pie.size
        assert list(con_pie.getdata()) != list(sin_pie.getdata())  # el pie cambió algo
    # chequeo directo en dedicatoria (fondo CREAM liso ahí, sin otros elementos
    # cerca del pie): el texto "c" de casatridimensional empieza cerca del
    # borde izquierdo de esa franja — con pie, ese pixel NO es fondo; sin pie,
    # sí lo es.
    con_pie = libro.pagina_libro(1, DATA, "safari", catalogo=True, sin_pie=False)
    sin_pie = libro.pagina_libro(1, DATA, "safari", catalogo=True, sin_pie=True)
    y = libro.Hp - 52
    fondo = con_pie.getpixel((30, y))   # esquina de la franja, nunca tiene texto
    con_algo_de_texto = any(con_pie.getpixel((x, y)) != fondo
                            for x in range(int(libro.Wp * 0.35), int(libro.Wp * 0.65)))
    sin_nada_de_texto = all(sin_pie.getpixel((x, y)) == fondo
                            for x in range(int(libro.Wp * 0.35), int(libro.Wp * 0.65)))
    assert con_algo_de_texto
    assert sin_nada_de_texto


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
    # sin el catálogo; el texto sale con la mayúscula automática de inicio de frase)
    for historia in ("tesoro", "rescate", "gran-dia"):
        legado = libro.cuento(dict(data, historia=historia), "safari")
        assert len(legado) == 7
        assert legado == [libro._capitalizar_frases(
            t.format(**dict(libro.HISTORIAS["safari"], nombre="Mateo",
                            conteo="contar hasta 6", conteo_num="6")))
            for t in libro.ARGUMENTOS[historia]]


def test_catalogo_audiolibro_largo_por_edad():
    """El audiolibro (catalogo=True) usa la versión rica con largo por edad:
    9 páginas de historia hasta 3 años, 17 de 4 en adelante, desacoplado del tema."""
    for historia in libro.ARGUMENTOS_LARGO:
        chico = libro.cuento({"nombre": "Mia", "edad": "3", "historia": historia},
                             "safari", catalogo=True)
        grande = libro.cuento({"nombre": "Mia", "edad": "5", "historia": historia},
                              "safari", catalogo=True)
        assert len(chico) == 9 and len(grande) == 17
        assert sum("Mia" in t for t in grande) >= 3
        # el corto conserva el arranque y SIEMPRE el cierre para dormir
        assert chico[0] == grande[0] and chico[-1] == grande[-1]
        # el corto es exactamente el subconjunto CORTO_IDX del largo (misma edad)
        largo3 = [libro.ARGUMENTOS_LARGO[historia][i] for i in libro.CORTO_IDX]
        assert len(chico) == len(largo3)
        # ninguna página arranca en minúscula (la mayúscula automática funciona)
        assert not [t for t in grande if t[:1].islower()]

    # sin catalogo (libro de kit), el mismo tema/historia NO cambia de largo
    kit = libro.cuento({"nombre": "Mia", "edad": "5", "historia": "tesoro"}, "safari")
    assert len(kit) == 7


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
