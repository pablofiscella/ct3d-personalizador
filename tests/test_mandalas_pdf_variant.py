"""Variante SOLO-PDF de los kits de mándalas (mandalas-<kit>-pdf): mismo contenido que la
versión PDF+Web, pero SIN el visor /pintar/ — se entrega como ZIP genérico (/descarga/).
Dos SKUs, dos precios (Pablo: $1500 solo PDF, $2500 PDF+Web), mismo arte."""
import os
import zipfile

import mandalas
import productos


def test_las_3_variantes_pdf_existen_y_son_publicas():
    tp = productos.tipos_publicos()
    for kit in ("media", "dificil", "muydificil"):
        t = f"mandalas-{kit}-pdf"
        assert t in tp, t
        assert "solo PDF" in tp[t]["nombre"] or "solo pdf" in tp[t]["nombre"].lower()


def test_variante_pdf_no_esta_en_el_branch_del_visor_web():
    """servicio.py NO debe incluir las variantes -pdf en el branch que entrega /pintar/."""
    src = open(os.path.join(os.path.dirname(__file__), "..", "servicio.py"), encoding="utf-8").read()
    linea = [l for l in src.splitlines() if 'tipo in ("mandalas"' in l][0]
    for kit in ("media", "dificil", "muydificil"):
        assert f"mandalas-{kit}-pdf" not in linea, f"mandalas-{kit}-pdf no debería estar en el branch web"


def test_variante_pdf_y_web_generan_el_mismo_contenido(tmp_path):
    """mandalas-media y mandalas-media-pdf arman el MISMO kit.zip de 12 piezas (solo cambia
    cómo se entrega, no el contenido)."""
    d1, d2 = tmp_path / "web", tmp_path / "pdf"
    d1.mkdir(); d2.mkdir()
    productos.generar({"nombre": "Sofía"}, str(d1), "safari", "mandalas-media")
    productos.generar({"nombre": "Sofía"}, str(d2), "safari", "mandalas-media-pdf")
    n1 = zipfile.ZipFile(d1 / "kit.zip").namelist()
    n2 = zipfile.ZipFile(d2 / "kit.zip").namelist()
    assert sorted(n1) == sorted(n2)
    assert len(n1) == mandalas.N_MANDALAS + 2
