"""Regresión: el layout en disco tras generar+aprobar debe satisfacer el
contrato que lee productos.py::_piezas_kit (NO red, NO bg removal real)."""
import io
import os
from PIL import Image
from ia_kit import orquestador, aprobar, catalogo


class _FakeClient:
    def editar(self, refs, prompt, size, **kw):
        w, h = (int(x) for x in size.split("x"))
        buf = io.BytesIO(); Image.new("RGB", (w, h), "white").save(buf, "PNG")
        return buf.getvalue()


def _tema_dir(tmp_path):
    d = tmp_path / "safari"; (d / "recortes").mkdir(parents=True)
    (d / "tema.json").write_text('{"kit":{"accent":"#111111","ink":"#222222"}}')
    Image.new("RGBA", (64, 64), (255, 0, 0, 255)).save(d / "recortes" / "animal_1.png")
    return str(tmp_path)


def test_layout_en_disco_matchea_piezas_kit(tmp_path):
    td = _tema_dir(tmp_path)
    orquestador.generar_tema(_FakeClient(), td, "safari", edades=[1, 2, 3],
                             quitar=lambda im, protect=True: im)
    aprobar.aprobar(td, "safari")
    base = os.path.join(td, "safari")
    extras = os.path.join(base, "extras")
    # contrato _EXTRAS_POR_EDAD: como mínimo el sentinel <base>_1.png en extras/
    for b in catalogo.EXTRAS_POR_EDAD:
        assert os.path.exists(os.path.join(extras, "%s_1.png" % b)), b
    # contrato _EXTRAS_UNIVERSAL: <base>.png en extras/
    for b in catalogo.EXTRAS_UNIVERSAL:
        assert os.path.exists(os.path.join(extras, "%s.png" % b)), b
    # invitacion personalizada: slot raíz del tema
    assert os.path.exists(os.path.join(base, "invitacion_1.png"))
