"""Bundle Fiesta Completa: portada con QR, armado del ZIP y el tipo en productos."""
import io
import os
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("CT3D_INVITACIONES_DIR", tempfile.mkdtemp())

import bundle_fiesta
import productos

DATA = {"nombre": "Emma", "edad": "4", "fecha": "20/09/2026", "hora": "15:00",
        "lugar": "Casa", "direccion": "Calle Falsa 123", "telefono": "1155554444"}


def test_portada_invitacion_tiene_qr():
    img = bundle_fiesta.portada_invitacion_pdf("https://kit.example.com/i/abc123", "Emma")
    assert img.size == (1240, 1754)
    # el QR es un bloque con negros puros en la zona central
    from PIL import Image
    zona = img.crop((500, 700, 740, 940)).convert("L")
    assert min(zona.getdata()) < 40


def test_generar_bundle_estructura(monkeypatch):
    """El ZIP final agrupa cada parte en su carpeta + la portada del link primero.
    productos.generar se mockea (rápido y sin OpenSCAD/temas reales)."""
    def _fake_generar(data, dest_dir, tema, tipo):
        os.makedirs(dest_dir, exist_ok=True)
        p = os.path.join(dest_dir, "kit.zip")
        with zipfile.ZipFile(p, "w") as z:
            z.writestr("archivo_%s.pdf" % tipo, b"contenido-" + tipo.encode())
        return p
    monkeypatch.setattr(productos, "generar", _fake_generar)

    with tempfile.TemporaryDirectory() as d:
        final = bundle_fiesta.generar_bundle(DATA, d, "safari",
                                             "https://kit.example.com/i/tok123")
        z = zipfile.ZipFile(final)
        nombres = z.namelist()
        assert "1_INVITACION_WEB_link_y_QR.pdf" in nombres
        assert "2_kit_imprimible/archivo_kit.pdf" in nombres
        assert "3_libro_de_cuento/archivo_libro.pdf" in nombres
        assert "4_impresion_3d/archivo_stl-pack.pdf" in nombres
        assert z.read("2_kit_imprimible/archivo_kit.pdf") == b"contenido-kit"


def test_tipo_registrado():
    assert productos.existe_tipo("fiesta-completa")
    campos = productos.campos_tipo("fiesta-completa")
    for k in ("nombre", "fecha", "telefono", "dedicatoria"):
        assert k in campos
    # galería con una pieza por parte
    metas = productos.piezas_meta("fiesta-completa", "safari")
    assert len(metas) == 4


def test_preview_renderiza():
    img = productos.preview({"nombre": "Emma", "edad": "4"}, tema="safari",
                            tipo="fiesta-completa")
    assert img.width > 100
