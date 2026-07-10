"""Guardián del kit de mándalas (tipo 'mandalas'). Cubre regla #4 del CLAUDE.md:
las piezas procedurales se generan, el override reemplaza una pieza, y el nombre
del comprador se respeta en la portada (la única pieza personalizada)."""
import os
import zipfile

from PIL import Image

import mandalas
import productos
import temas


def test_tipo_registrado_y_publico():
    assert "mandalas" in productos.TIPOS
    assert "mandalas" in productos.tipos_publicos()
    assert productos.TIPOS["mandalas"]["campos"] == ["nombre"]


def test_piezas_procedurales_se_generan(tmp_path, monkeypatch):
    monkeypatch.setattr(temas, "TEMAS_DIR", str(tmp_path))
    items = productos.piezas_tipo("safari", "mandalas")
    # portada + 6 mándalas + cómo imprimir
    assert len(items) == mandalas.NIVELES + 2
    for nombre, fn, _is_rgba in items:
        img = fn({"nombre": "Sofía"})
        assert img.size == mandalas.A4          # A4 300dpi REAL (evita el gotcha DPI)


def test_mandala_es_line_art_bn_puro():
    """El DIBUJO de la mándala (line-art para colorear) tiene que ser negro puro sin
    grises ni degradés (regla de imprenta armar-kit). Se prueba draw_mandala aislado del
    texto de página (número/pie), que sí es gris a propósito."""
    from PIL import Image, ImageDraw
    img = Image.new("RGB", mandalas.A4, (255, 255, 255))
    mandalas.draw_mandala(ImageDraw.Draw(img), 3)
    colores = {c for _n, c in img.getcolors(maxcolors=100000)}
    assert colores <= {(0, 0, 0), (255, 255, 255)}, \
        f"apareció un gris en el line-art: {colores - {(0,0,0),(255,255,255)}}"


def test_kit_zip_completo(tmp_path, monkeypatch):
    monkeypatch.setattr(temas, "TEMAS_DIR", str(tmp_path))
    productos.generar({"nombre": "Sofía"}, str(tmp_path), "safari", "mandalas")
    z = os.path.join(str(tmp_path), "kit.zip")
    assert os.path.exists(z)
    assert len(zipfile.ZipFile(z).namelist()) == mandalas.NIVELES + 2


def test_override_reemplaza_una_pieza(tmp_path, monkeypatch):
    monkeypatch.setattr(temas, "TEMAS_DIR", str(tmp_path))
    ov = productos.override_path("safari", "mandalas", 1)   # override de la mándala 1
    os.makedirs(os.path.dirname(ov), exist_ok=True)
    Image.new("RGBA", (77, 88), (10, 20, 30, 255)).save(ov)
    items = productos.piezas_tipo("safari", "mandalas")
    img = items[1][1]({"nombre": "Sofía"})
    assert img.size == (77, 88)   # vino del override, no del diseño procedural


def test_nombre_del_comprador_en_la_portada(monkeypatch):
    """El nombre cambia la portada (pieza personalizada) — verificable por diferencia de píxeles."""
    con = mandalas.portada({"nombre": "Sofía"}).convert("L")
    sin = mandalas.portada({"nombre": ""}).convert("L")
    assert con.size == sin.size
    dif = sum(1 for a, b in zip(con.getdata(), sin.getdata()) if a != b)
    assert dif > 1000   # el subtítulo "de Sofía" vs "para pintar" cambia bastantes píxeles


def test_dificultad_declarada_por_nivel():
    assert len(mandalas.DIFICULTAD) == mandalas.NIVELES
    assert mandalas.DIFICULTAD[0] == "Muy fácil"
    assert mandalas.DIFICULTAD[-1] == "Muy difícil"


def test_arte_ia_existe_y_es_bn_puro():
    """Los 6 assets de arte (line-art IA limpiado) están presentes y son B/N puro y cuadrados."""
    from PIL import Image
    for nivel in range(1, mandalas.NIVELES + 1):
        p = mandalas._asset(nivel)
        assert p is not None, f"falta el asset del nivel {nivel}"
        im = Image.open(p).convert("L")
        assert im.width == im.height, f"asset {nivel} no es cuadrado"
        colores = {c for _n, c in im.getcolors(maxcolors=100000)}
        assert colores <= {0, 255}, f"asset {nivel} tiene grises (no B/N puro): {colores - {0,255}}"


def test_pagina_usa_el_arte_ia_cuando_existe(monkeypatch):
    """Con asset presente, la página usa el arte IA (no el procedural). Se verifica por
    cantidad de tinta: el arte IA del nivel 6 es mucho más denso que el procedural."""
    from PIL import Image
    pg = mandalas.pagina(6, 6).convert("L")
    tinta = sum(1 for p in pg.getdata() if p < 8)
    # sin asset, draw_mandala procedural deja mucha menos tinta (line-art fino, ~1-2% de la
    # página); el arte IA nivel 6 llena el área central → ~7-8% sobre la hoja completa.
    assert tinta > pg.width * pg.height * 0.05
