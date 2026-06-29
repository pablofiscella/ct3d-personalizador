import os
from PIL import Image
from ia_kit import aprobar


def _draft(tmp_path, *nombres):
    d = tmp_path / "safari" / "ia_draft"; d.mkdir(parents=True)
    for n in nombres:
        Image.new("RGBA", (8, 8)).save(d / n)
    return str(tmp_path)


def test_slots_van_a_la_raiz_del_tema(tmp_path):
    td = _draft(tmp_path, "invitacion_1.png", "afiche_2.png", "banderin.png", "topper.png")
    res = aprobar.aprobar(td, "safari")
    base = os.path.join(td, "safari")
    assert os.path.exists(os.path.join(base, "invitacion_1.png"))
    assert os.path.exists(os.path.join(base, "afiche_2.png"))
    assert os.path.exists(os.path.join(base, "extras", "banderin.png"))
    assert os.path.exists(os.path.join(base, "extras", "topper.png"))
    assert res["n"] == 4
    assert not os.listdir(os.path.join(base, "ia_draft"))


def test_listar_draft(tmp_path):
    td = _draft(tmp_path, "banderin.png")
    assert aprobar.listar_draft(td, "safari") == ["banderin.png"]
