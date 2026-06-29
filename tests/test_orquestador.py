import io
import os
import pytest
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
    # invitacion (slot raíz) y afiche (extra por-edad, arte distinto) x3
    for e in (1, 2, 3):
        assert os.path.exists(os.path.join(draft, "invitacion_%d.png" % e))
        assert os.path.exists(os.path.join(draft, "afiche_%d.png" % e))
    # universal x1
    assert os.path.exists(os.path.join(draft, "banderin.png"))
    # por_edad False pero FILENAME por-edad (topper) -> arte único como "topper_1.png"
    assert os.path.exists(os.path.join(draft, "topper_1.png"))
    assert not os.path.exists(os.path.join(draft, "topper.png"))
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


def test_refs_fallback_al_arte_base(tmp_path):
    # tema SIN recortes/ pero con arte base -> _refs cae al invitacion/afiche
    d = tmp_path / "safari"; d.mkdir(parents=True)
    (d / "tema.json").write_text('{"kit":{"accent":"#111111","ink":"#222222"}}')
    Image.new("RGBA", (32, 32)).save(d / "invitacion_1.png")
    Image.new("RGBA", (32, 32)).save(d / "afiche_1.png")
    assert len(orquestador._refs(str(d))) == 2
    res = orquestador.generar_tema(_FakeClient(), str(tmp_path), "safari", edades=[1],
                                   solo={"banderin"}, quitar=lambda im, protect=True: im)
    assert not res["errores"]


def test_evento_lleva_archivo_real(tmp_path):
    # el evento debe llevar el nombre de archivo REAL (la preview lo usa tal cual)
    td = _tema_dir(tmp_path)
    ev = []
    orquestador.generar_tema(_FakeClient(), td, "safari", edades=[1],
                             progress=ev.append, quitar=lambda im, protect=True: im)
    arch = {(e["pieza"], e["edad"]): e["archivo"] for e in ev if e["ok"]}
    assert arch[("invitacion", 1)] == "invitacion_1.png"
    assert arch[("topper", None)] == "topper_1.png"     # arte único per-edad -> _1
    assert arch[("banderin", None)] == "banderin.png"   # universal


def test_sin_referencias_falla_claro(tmp_path):
    # ni recortes/ ni arte base -> error claro, NO una llamada vacía a OpenAI
    d = tmp_path / "vacio"; d.mkdir(parents=True)
    (d / "tema.json").write_text("{}")
    with pytest.raises(RuntimeError, match="referencia"):
        orquestador.generar_tema(_FakeClient(), str(tmp_path), "vacio", edades=[1])
