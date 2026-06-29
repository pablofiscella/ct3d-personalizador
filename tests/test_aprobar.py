import json
import os
from PIL import Image
from ia_kit import aprobar


def _draft(tmp_path, *nombres, edades=None):
    base = tmp_path / "safari"
    (base / "ia_draft").mkdir(parents=True)
    if edades is not None:
        (base / "tema.json").write_text(json.dumps({"id": "safari", "edades": edades}))
    for n in nombres:
        Image.new("RGBA", (8, 8)).save(base / "ia_draft" / n)
    return str(tmp_path)


def test_slots_van_a_la_raiz_del_tema(tmp_path):
    td = _draft(tmp_path, "invitacion_1.png", "afiche_2.png", "banderin.png", "topper_1.png",
                edades=[1, 2, 3])
    res = aprobar.aprobar(td, "safari")
    base = os.path.join(td, "safari")
    # la invitación (un solo draft) se copia a TODAS las edades del tema (raíz)
    for e in (1, 2, 3):
        assert os.path.exists(os.path.join(base, "invitacion_%d.png" % e))
    # afiche ahora es un extra: va a extras/, NO a la raíz
    assert os.path.exists(os.path.join(base, "extras", "afiche_2.png"))
    assert not os.path.exists(os.path.join(base, "afiche_2.png"))
    assert os.path.exists(os.path.join(base, "extras", "banderin.png"))
    assert os.path.exists(os.path.join(base, "extras", "topper_1.png"))
    assert res["n"] == 6   # invitacion_1/2/3 + afiche_2 + banderin + topper_1
    assert not os.listdir(os.path.join(base, "ia_draft"))


def test_invitacion_default_edades_si_falta_en_tema(tmp_path):
    td = _draft(tmp_path, "invitacion_1.png")     # sin tema.json -> edades default [1,2,3]
    aprobar.aprobar(td, "safari")
    base = os.path.join(td, "safari")
    for e in (1, 2, 3):
        assert os.path.exists(os.path.join(base, "invitacion_%d.png" % e))


def test_listar_draft(tmp_path):
    td = _draft(tmp_path, "banderin.png")
    assert aprobar.listar_draft(td, "safari") == ["banderin.png"]
