"""Libro premium: arte por pedido (usar_escenas_dir), generación IA a dest_dir y
el tipo libro-premium en productos — sin llamar a OpenAI (cliente fake)."""
import io
import os
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import libro
import libro_ia
import productos


def _png_bytes(color, size=(64, 64)):
    buf = io.BytesIO()
    Image.new("RGBA", size, color).save(buf, "PNG")
    return buf.getvalue()


class _FakeClient:
    """Devuelve un PNG rojo fijo; registra las llamadas."""
    def __init__(self):
        self.llamadas = []

    def editar(self, refs, prompt, size, quality="medium"):
        self.llamadas.append({"refs": len(refs), "prompt": prompt, "size": size})
        return _png_bytes((255, 0, 0, 255))


def test_usar_escenas_dir_redirige_el_arte():
    """Con el contexto activo, _escena_efectiva_path apunta al dir del pedido."""
    with tempfile.TemporaryDirectory() as d:
        Image.new("RGBA", (32, 32), (0, 255, 0, 255)).save(os.path.join(d, "3.png"))
        con_ctx = None
        with libro.usar_escenas_dir(d):
            con_ctx = libro._escena_efectiva_path("safari", 3)
        sin_ctx = libro._escena_efectiva_path("safari", 3)
        assert con_ctx == os.path.join(d, "3.png")
        assert sin_ctx != con_ctx  # afuera del with vuelve al override del tema


def test_usar_escenas_dir_fallback_si_no_hay_archivo():
    """Página sin arte en el dir del pedido → cae al override del tema (no rompe)."""
    with tempfile.TemporaryDirectory() as d:  # dir vacío
        with libro.usar_escenas_dir(d):
            p = libro._escena_efectiva_path("safari", 5)
        assert p == libro.override_escena_path("safari", 5)


def test_pagina_renderiza_con_arte_del_pedido():
    """El render de una página usa el arte del pedido dentro del contexto: la página
    con arte rojo puro difiere de la procedural."""
    data = {"nombre": "Test", "edad": "5"}
    base = libro.pagina_libro(2, data, "safari")
    with tempfile.TemporaryDirectory() as d:
        Image.new("RGBA", (600, 600), (255, 0, 0, 255)).save(os.path.join(d, "2.png"))
        with libro.usar_escenas_dir(d):
            premium = libro.pagina_libro(2, data, "safari")
    assert base.size == premium.size
    assert base.tobytes() != premium.tobytes()  # el arte rojo cambia la página


def test_generar_ilustraciones_dest_dir():
    """Con dest_dir, las 10 ilustraciones caen ahí y NO tocan los overrides del tema."""
    fake = _FakeClient()
    with tempfile.TemporaryDirectory() as d:
        paths = libro_ia.generar_ilustraciones(fake, "safari", dest_dir=d)
        assert len(paths) == libro.TOTAL_PAGINAS
        for i, p in enumerate(paths):
            assert p == os.path.join(d, "%d.png" % i)
            assert os.path.isfile(p)
    assert len(fake.llamadas) == libro.TOTAL_PAGINAS


def test_tipo_libro_premium_existe_y_genera():
    """El tipo está registrado con los mismos campos que libro, y generar() produce
    el ZIP con las 10 páginas (camino síncrono, sin IA — arte standard)."""
    assert productos.existe_tipo("libro-premium")
    # mismos campos que libro + genero (para dibujar al protagonista en el arte por pedido)
    assert set(productos.campos_tipo("libro-premium")) == set(productos.campos_tipo("libro")) | {"genero", "historia"}
    with tempfile.TemporaryDirectory() as d:
        zip_path = productos.generar({"nombre": "Emma", "edad": "4"}, d,
                                     tema="safari", tipo="libro-premium")
        assert os.path.isfile(zip_path)
        import zipfile
        assert len(zipfile.ZipFile(zip_path).namelist()) == libro.TOTAL_PAGINAS


def test_contexto_es_por_hilo():
    """El contexto de escenas NO se filtra a otros hilos (renders concurrentes del
    dash mientras un pedido premium genera)."""
    import threading
    resultado = {}
    with tempfile.TemporaryDirectory() as d:
        Image.new("RGBA", (32, 32), (0, 0, 255, 255)).save(os.path.join(d, "1.png"))

        def otro_hilo():
            resultado["path"] = libro._escena_efectiva_path("safari", 1)

        with libro.usar_escenas_dir(d):
            t = threading.Thread(target=otro_hilo)
            t.start()
            t.join()
        assert resultado["path"] == libro.override_escena_path("safari", 1)


def test_prompt_genero_nena_y_nene():
    """El género del formulario cambia cómo se describe al protagonista en las
    escenas donde aparece (4: fiesta de bienvenida, 6: momento heroico)."""
    for idx in (4, 6):
        p_nena = libro_ia.prompt_pagina("safari", idx, genero="nena")
        p_nene = libro_ia.prompt_pagina("safari", idx, genero="Niño")  # normaliza
        p_default = libro_ia.prompt_pagina("safari", idx)
        assert "una nena pequeña vista de espaldas" in p_nena
        assert "un nene pequeño visto de espaldas" in p_nene
        assert "un niño visto de espaldas" in p_default
        assert "{protagonista}" not in p_nena  # el placeholder siempre se resuelve


def test_prompt_paginas_sin_protagonista_no_cambian():
    """Las páginas donde el chico NO aparece son idénticas con o sin género."""
    for idx in (0, 1, 2, 3, 5, 7, 8, 9):
        assert (libro_ia.prompt_pagina("safari", idx, genero="nena")
                == libro_ia.prompt_pagina("safari", idx))


def test_campo_genero_solo_en_premium():
    assert "genero" in productos.campos_tipo("libro-premium")
    assert "genero" not in productos.campos_tipo("libro")


def test_generar_ilustraciones_pasa_genero():
    """El género llega hasta el prompt que recibe el cliente de OpenAI."""
    fake = _FakeClient()
    with tempfile.TemporaryDirectory() as d:
        libro_ia.generar_ilustraciones(fake, "safari", paginas=[4], dest_dir=d, genero="nena")
    assert "una nena pequeña vista de espaldas" in fake.llamadas[0]["prompt"]
