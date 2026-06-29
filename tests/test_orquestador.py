import io
import os
from PIL import Image
from ia_kit import orquestador


class _FakeClient:
    def __init__(self):
        self.prompts = []
    def editar(self, refs, prompt, size, **kw):
        self.prompts.append((prompt, size))
        w, h = (int(x) for x in size.split("x"))
        buf = io.BytesIO(); Image.new("RGB", (w, h), "white").save(buf, "PNG")
        return buf.getvalue()


def _tema_dir(tmp_path):
    d = tmp_path / "safari"; (d / "recortes").mkdir(parents=True)
    (d / "tema.json").write_text('{"kit":{"accent":"#111111","ink":"#222222"}}')
    # un personaje de referencia
    Image.new("RGBA", (64, 64), (255, 0, 0, 255)).save(d / "recortes" / "animal_1.png")
    return str(tmp_path)


def test_genera_slots_por_edad_y_universales(tmp_path):
    td = _tema_dir(tmp_path)
    c = _FakeClient()
    res = orquestador.generar_tema(c, td, "safari", edades=[1, 2, 3],
                                   quitar=lambda im, protect=True: im)
    draft = os.path.join(td, "safari", "ia_draft")
    # invitacion y afiche x3
    for e in (1, 2, 3):
        assert os.path.exists(os.path.join(draft, "invitacion_%d.png" % e))
        assert os.path.exists(os.path.join(draft, "afiche_%d.png" % e))
    # universal x1
    assert os.path.exists(os.path.join(draft, "banderin.png"))
    # por_edad False (topper) -> "topper.png" x1
    assert os.path.exists(os.path.join(draft, "topper.png"))
    assert not res["errores"]


def test_solo_limita_piezas(tmp_path):
    td = _tema_dir(tmp_path)
    res = orquestador.generar_tema(_FakeClient(), td, "safari", edades=[1],
                                   solo={"banderin"}, quitar=lambda im, protect=True: im)
    draft = os.path.join(td, "safari", "ia_draft")
    assert os.path.exists(os.path.join(draft, "banderin.png"))
    assert not os.path.exists(os.path.join(draft, "invitacion_1.png"))


def test_progress_se_invoca(tmp_path):
    td = _tema_dir(tmp_path)
    eventos = []
    orquestador.generar_tema(_FakeClient(), td, "safari", edades=[1],
                             solo={"banderin"}, progress=eventos.append,
                             quitar=lambda im, protect=True: im)
    assert any(e["pieza"] == "banderin" and e["ok"] for e in eventos)
