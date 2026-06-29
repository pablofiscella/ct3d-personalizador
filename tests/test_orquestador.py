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
    # invitacion: UNA SOLA en el draft (se copia a todas las edades recién al aprobar)
    assert os.path.exists(os.path.join(draft, "invitacion_1.png"))
    assert not os.path.exists(os.path.join(draft, "invitacion_2.png"))
    assert not os.path.exists(os.path.join(draft, "invitacion_3.png"))
    # afiche es replicable -> en el batch solo la 1ª edad (el resto se replica aparte)
    assert os.path.exists(os.path.join(draft, "afiche_1.png"))
    assert not os.path.exists(os.path.join(draft, "afiche_2.png"))
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


def test_reusa_maestra_cacheada(tmp_path):
    # 1ª vez: genera maestra + pieza (2 llamadas). 2ª con reusar_maestra: solo la pieza (1).
    td = _tema_dir(tmp_path)
    c1 = _FakeClient()
    orquestador.generar_tema(c1, td, "safari", edades=[1], solo={"banderin"},
                             quitar=lambda im, protect=True: im)
    assert len(c1.prompts) == 2
    c2 = _FakeClient()
    orquestador.generar_tema(c2, td, "safari", edades=[1], solo={"banderin"},
                             reusar_maestra=True, quitar=lambda im, protect=True: im)
    assert len(c2.prompts) == 1   # reusó la maestra cacheada


def test_expand_labels_no_fusiona_figuras_cercanas():
    from PIL import ImageDraw
    # dos cuadrados con un gap chico: el borde NO debe fusionarlos (quedan 2 figuras)
    fg = Image.new("L", (60, 30), 0)
    d = ImageDraw.Draw(fg)
    d.rectangle([8, 10, 22, 20], fill=255)
    d.rectangle([34, 10, 48, 20], fill=255)   # gap de ~12px entre ambos
    out = orquestador._expandir_labels(fg, max_r=8, gap=2)   # borde grande a propósito
    _, n = orquestador._etiquetar(out.point(lambda p: 255 if p > 128 else 0))
    assert n == 2          # siguen siendo 2 (no se pegaron)
    assert out.getpixel((28, 15)) == 0   # la línea media quedó TRANSPARENTE (gap para cortar)


def test_plancha_stickers_conserva_figuras_y_agrega_borde():
    from PIL import ImageDraw
    im = Image.new("RGBA", (200, 100), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([20, 30, 60, 70], fill=(255, 0, 0, 255))
    d.ellipse([140, 30, 180, 70], fill=(0, 0, 255, 255))   # dos stickers separados
    out, tocan = orquestador._plancha_stickers(im)
    # hay borde blanco
    blancos = sum(1 for p in out.convert("RGBA").getdata()
                  if p[3] == 255 and p[0] > 240 and p[1] > 240 and p[2] > 240)
    assert blancos > 0
    # siguen separados -> 2 figuras en el alpha
    _, n = orquestador._etiquetar(out.convert("RGBA").getchannel("A").point(lambda p: 255 if p > 10 else 0))
    assert n == 2


def test_palito_agrega_dowel_solido_abajo():
    from PIL import ImageDraw
    im = Image.new("RGBA", (100, 80), (0, 0, 0, 0))
    ImageDraw.Draw(im).rectangle([10, 8, 89, 70], fill=(255, 255, 255, 255))  # cuerpo macizo
    out = orquestador._palito(im)
    assert out.size[1] > 80                       # creció hacia abajo (el palito)
    cx = out.size[0] // 2
    assert out.getpixel((cx, out.size[1] - 4))[3] == 255   # palito sólido hasta abajo (no hueco)


def test_mascara_circular_recorta_a_circulo():
    im = Image.new("RGBA", (100, 100), (255, 0, 0, 255))  # cuadrado opaco
    out = orquestador._mascara_circular(im)
    cx, cy = out.size[0] // 2, out.size[1] // 2
    assert out.getpixel((cx, cy))[3] == 255   # centro opaco
    assert out.getpixel((0, 0))[3] == 0       # esquina transparente (fuera del círculo)


def test_borde_sticker_agrega_contorno_blanco():
    from PIL import ImageDraw
    im = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
    ImageDraw.Draw(im).rectangle([22, 22, 37, 37], fill=(255, 0, 0, 255))  # cuadrado rojo
    out = orquestador._borde_sticker(im, frac=0.12)
    blancos = sum(1 for p in out.getdata()
                  if p[3] == 255 and p[0] > 240 and p[1] > 240 and p[2] > 240)
    assert blancos > 0          # hay borde blanco alrededor de la figura
    assert out.size[0] > 16     # el contorno agranda respecto al cuadrado original (16px)


def test_borde_sticker_rellena_hueco_interno():
    from PIL import ImageDraw
    im = Image.new("RGBA", (90, 90), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([10, 10, 79, 79], fill=(255, 0, 0, 255))   # disco
    d.ellipse([35, 35, 54, 54], fill=(0, 0, 0, 0))        # hueco transparente en el medio
    out = orquestador._borde_sticker(im, frac=0.05)
    cx, cy = out.size[0] // 2, out.size[1] // 2
    assert out.getpixel((cx, cy))[3] == 255   # el hueco quedó relleno (opaco)


def test_contar_piezas():
    # invitacion ×1 (UNA_SOLA: se genera 1 vez y se copia) + afiche ×1 (replicable) + 12 = 14
    assert orquestador.contar_piezas([1, 2, 3]) == 14   # 1 + 1 + 12
    assert orquestador.contar_piezas([1]) == 14         # 1 + 1 + 12
    assert orquestador.contar_piezas([1, 2, 3], solo={"banderin"}) == 1


def test_invitacion_una_sola_en_draft(tmp_path):
    # la invitación se genera UNA vez y queda como UN solo draft (1 tarjeta en el panel)
    td = _tema_dir(tmp_path)
    c = _FakeClient()
    orquestador.generar_tema(c, td, "safari", edades=[1, 2, 3], solo={"invitacion"},
                             quitar=lambda im, protect=True: im)
    draft = os.path.join(td, "safari", "ia_draft")
    invs = [f for f in os.listdir(draft) if f.startswith("invitacion_")]
    assert invs == ["invitacion_1.png"]
    # solo 1 llamada a OpenAI para la pieza (maestra + 1 invitación), no 3
    assert sum(1 for pr, _ in c.prompts if "invitación" in pr.lower()) == 1


def test_solo_faltantes_saltea_lo_existente(tmp_path):
    td = _tema_dir(tmp_path)
    # 1ª tanda: genera solo banderin
    orquestador.generar_tema(_FakeClient(), td, "safari", edades=[1], solo={"banderin"},
                             quitar=lambda im, protect=True: im)
    draft = os.path.join(td, "safari", "ia_draft")
    assert os.path.exists(os.path.join(draft, "banderin.png"))
    assert orquestador.contar_faltantes(td, "safari", [1]) == orquestador.contar_piezas([1]) - 1
    # 2ª tanda INCREMENTAL: completa solo lo que falta (NO regenera banderin)
    res = orquestador.generar_tema(_FakeClient(), td, "safari", edades=[1], solo_faltantes=True,
                                   reusar_maestra=True, quitar=lambda im, protect=True: im)
    generadas = {e["pieza"] for e in res["generadas"]}
    assert "banderin" not in generadas          # ya estaba -> salteado
    assert "invitacion" in generadas            # faltaba -> generado
    assert orquestador.contar_faltantes(td, "safari", [1]) == 0   # ahora están todas


def test_afiche_solo_primera_edad_en_batch(tmp_path):
    td = _tema_dir(tmp_path)
    orquestador.generar_tema(_FakeClient(), td, "safari", edades=[1, 2, 3],
                             quitar=lambda im, protect=True: im)
    draft = os.path.join(td, "safari", "ia_draft")
    assert os.path.exists(os.path.join(draft, "afiche_1.png"))
    assert not os.path.exists(os.path.join(draft, "afiche_2.png"))   # 2 y 3 se replican aparte
    assert not os.path.exists(os.path.join(draft, "afiche_3.png"))


def test_replicar_pieza_genera_otras_edades(tmp_path):
    td = _tema_dir(tmp_path)
    orquestador.generar_tema(_FakeClient(), td, "safari", edades=[1, 2, 3],
                             quitar=lambda im, protect=True: im)   # crea afiche_1
    res = orquestador.replicar_pieza(_FakeClient(), td, "safari", "afiche", [1, 2, 3])
    draft = os.path.join(td, "safari", "ia_draft")
    assert os.path.exists(os.path.join(draft, "afiche_2.png"))
    assert os.path.exists(os.path.join(draft, "afiche_3.png"))
    assert not res["errores"]


def test_sin_referencias_falla_claro(tmp_path):
    # ni recortes/ ni arte base -> error claro, NO una llamada vacía a OpenAI
    d = tmp_path / "vacio"; d.mkdir(parents=True)
    (d / "tema.json").write_text("{}")
    with pytest.raises(RuntimeError, match="referencia"):
        orquestador.generar_tema(_FakeClient(), str(tmp_path), "vacio", edades=[1])
