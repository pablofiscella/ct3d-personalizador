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
        # line-art VÁLIDO (con un área cerrada): el QA de fase 4 rechaza una
        # hoja en blanco ("sin áreas cerradas para pintar")
        im = Image.new("RGB", (w, h), "white")
        from PIL import ImageDraw as _D
        _D.Draw(im).ellipse([w*0.2, h*0.2, w*0.8, h*0.8], outline="black", width=max(6, w//80))
        buf = io.BytesIO(); im.save(buf, "PNG")
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
    # afiche: UN arte por edad (el número de edad va ILUSTRADO — cada edad el suyo)
    assert os.path.exists(os.path.join(draft, "afiche_1.png"))
    assert os.path.exists(os.path.join(draft, "afiche_2.png"))
    assert os.path.exists(os.path.join(draft, "afiche_3.png"))
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


def test_stickers_individuales_extrae_cada_figura():
    from PIL import ImageDraw
    im = Image.new("RGBA", (240, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([20, 30, 70, 90], fill=(255, 0, 0, 255))
    d.ellipse([170, 30, 220, 90], fill=(0, 0, 255, 255))   # dos figuras separadas
    sts, n = orquestador._stickers_individuales(im)
    assert n == 2 and len(sts) == 2                        # extrae cada figura (sin borde aún)
    for s in sts:                                          # conserva el arte (no vacío)
        assert s.convert("RGBA").getbbox() is not None


def test_aplanar_blanco_deja_fondo_opaco():
    """Una imagen con fondo transparente queda 100% opaca (con fondo) tras aplanar."""
    im = Image.new("RGBA", (60, 90), (0, 0, 0, 0))          # todo transparente
    from PIL import ImageDraw
    ImageDraw.Draw(im).ellipse([10, 10, 40, 40], fill=(200, 40, 40, 255))  # una figura
    out = orquestador._aplanar_blanco(im)
    alphas = [p[3] for p in out.convert("RGBA").getdata()]
    assert min(alphas) == 255                                # ningún pixel transparente
    esquina = out.convert("RGBA").getpixel((0, 0))
    assert esquina[3] == 255 and min(esquina[:3]) > 240      # el fondo es blanco opaco


def test_stickers_no_parte_figura_por_franja_fina():
    """Una figura partida por una franja transparente fina NO debe quedar en dos mitades."""
    from PIL import ImageDraw
    im = Image.new("RGBA", (240, 240), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([40, 40, 200, 200], fill=(255, 0, 0, 255))   # un cuerpo macizo
    d.rectangle([118, 40, 122, 200], fill=(0, 0, 0, 0))       # franja transparente fina que lo parte
    sts, n = orquestador._stickers_individuales(im)
    assert n == 1 and len(sts) == 1                          # se reconecta: UN solo sticker


def test_sticker_borde_uniforme():
    fig = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    from PIL import ImageDraw
    ImageDraw.Draw(fig).ellipse([8, 8, 31, 31], fill=(255, 0, 0, 255))
    out = orquestador._sticker_borde(fig, ancho=6)
    assert out.size[0] > 24 and out.size[1] > 24          # creció por el borde
    blancos = sum(1 for p in out.convert("RGBA").getdata()
                  if p[3] == 255 and min(p[:3]) > 240)
    assert blancos > 0                                    # hay borde blanco alrededor


def test_regrid_coloca_todos_separados():
    sts = [Image.new("RGBA", (30, 30), (255, 0, 0, 255)) for _ in range(16)]
    out, desc = orquestador._regrid_stickers(sts, 400, 400, menos=1)
    assert desc == 0 and out.size == (400, 400)     # entran todos, ninguno descartado
    _, n = orquestador._etiquetar(out.getchannel("A").point(lambda p: 255 if p > 10 else 0))
    assert n == 16                                  # 16 separados (no se tocan)


def test_plancha_stickers_separa_y_bordea():
    from PIL import ImageDraw
    im = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([20, 20, 70, 70], fill=(255, 0, 0, 255))
    d.ellipse([130, 130, 180, 180], fill=(0, 0, 255, 255))
    out, pocas = orquestador._plancha_stickers(im)
    blancos = sum(1 for p in out.convert("RGBA").getdata()
                  if p[3] == 255 and min(p[:3]) > 240)
    assert blancos > 0                                    # hay borde blanco
    _, n = orquestador._etiquetar(out.getchannel("A").point(lambda p: 255 if p > 10 else 0))
    assert n == 2                                         # 2 stickers separados en la grilla


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


def test_colorear_genera_y_es_byn(tmp_path):
    # la página para colorear se genera como colorear.png y el código la deja en B/N puro
    td = _tema_dir(tmp_path)
    orquestador.generar_tema(_FakeClient(), td, "safari", edades=[1],
                             solo={"colorear"}, quitar=lambda im, protect=True: im)
    p = os.path.join(td, "safari", "ia_draft", "colorear.png")
    assert os.path.exists(p)
    assert set(Image.open(p).convert("L").getdata()) <= {0, 255}   # sin grises


def test_limpiar_colorear_mata_grises():
    im = Image.new("RGBA", (20, 20), (128, 128, 128, 255))         # gris medio
    assert set(orquestador._limpiar_colorear(im).convert("L").getdata()) <= {0, 255}


def test_prompt_colorear_es_line_art():
    from ia_kit import catalogo
    p = next(x for x in catalogo.PIEZAS if x.key == "colorear")
    low = catalogo.prompt_de(catalogo._DEF, p).lower()
    assert "colorear" in low and "líneas" in low
    assert "colores planos" not in low                            # NO usa el bloque flat-vector


def test_contar_piezas():
    # invitacion ×1 (UNA_SOLA) + afiche ×N (uno por edad, número ilustrado)
    # + 12 extras + colorear ×1
    assert orquestador.contar_piezas([1, 2, 3]) == 17   # 1 + 3 + 12 + 1
    assert orquestador.contar_piezas([1]) == 15         # 1 + 1 + 12 + 1
    assert orquestador.contar_piezas([1, 2, 3, 4, 5]) == 19  # 1 + 5 + 12 + 1
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


def test_afiche_uno_por_edad_en_batch(tmp_path):
    # el afiche lleva el número de edad ILUSTRADO → uno por edad (bug: antes solo
    # la 1ª, y al agregar edades sus afiches nunca se generaban)
    td = _tema_dir(tmp_path)
    orquestador.generar_tema(_FakeClient(), td, "safari", edades=[1, 2, 3],
                             quitar=lambda im, protect=True: im)
    draft = os.path.join(td, "safari", "ia_draft")
    assert os.path.exists(os.path.join(draft, "afiche_1.png"))
    assert os.path.exists(os.path.join(draft, "afiche_2.png"))
    assert os.path.exists(os.path.join(draft, "afiche_3.png"))


def test_afiche_incremental_solo_edades_nuevas(tmp_path):
    # el caso de Pablo: con afiche_1/2/3 aprobados, agregar edades 4-5 debe contar
    # SOLO los afiches nuevos como faltantes (no regenerar los aprobados)
    td = _tema_dir(tmp_path)
    ex = os.path.join(td, "safari", "extras"); os.makedirs(ex, exist_ok=True)
    for e in (1, 2, 3):
        Image.new("RGBA", (32, 32)).save(os.path.join(ex, "afiche_%d.png" % e))
    p = next(x for x in orquestador.catalogo.PIEZAS if x.key == "afiche")
    faltan = [e for e in [1, 2, 3, 4, 5]
              if not orquestador._pieza_existe(os.path.join(td, "safari"),
                                               orquestador._nombre_pieza(p, e))]
    assert faltan == [4, 5]


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


class _ClienteModeracion:
    """Simula el bloqueo aleatorio por moderación de OpenAI: falla las primeras
    `fallas` veces con 'moderation_blocked' y después genera bien."""
    def __init__(self, fallas=0, error_real_en=None):
        self.llamadas = 0
        self.fallas = fallas
        self.error_real_en = error_real_en   # índice de llamada (1-based) con error NO-moderación
    def editar(self, refs, prompt, size, **kw):
        self.llamadas += 1
        if self.error_real_en and self.llamadas == self.error_real_en:
            raise RuntimeError("OpenAI HTTP 400: Bad Request — algo real, no moderación")
        if self.llamadas <= self.fallas:
            raise RuntimeError(
                'OpenAI HTTP 400: Bad Request — {"error": {"code": "moderation_blocked"}}')
        w, h = (int(x) for x in size.split("x"))
        im = Image.new("RGB", (w, h), "white")
        from PIL import ImageDraw as _D
        _D.Draw(im).ellipse([w*0.2, h*0.2, w*0.8, h*0.8], outline="black", width=max(6, w//80))
        buf = io.BytesIO(); im.save(buf, "PNG")
        return buf.getvalue()


def test_genera_variantes_colorear_ok(tmp_path):
    td = _tema_dir(tmp_path)
    res = orquestador.generar_variantes_colorear(_FakeClient(), td, "safari", n=3)
    draft = os.path.join(td, "safari", "ia_draft")
    assert len(res["generadas"]) == 3 and not res["errores"]
    for nombre in ("colorear.png", "colorear_2.png", "colorear_3.png"):
        assert os.path.exists(os.path.join(draft, nombre))


def test_genera_variantes_colorear_reintenta_moderacion(tmp_path):
    td = _tema_dir(tmp_path)
    cliente = _ClienteModeracion(fallas=2)   # falla 2 veces por moderación, 3ra OK
    res = orquestador.generar_variantes_colorear(cliente, td, "safari", n=1, intentos_por_variante=4)
    assert len(res["generadas"]) == 1 and not res["errores"]
    assert cliente.llamadas == 3   # 2 fallidas + 1 exitosa


def test_genera_variantes_colorear_error_real_no_insiste(tmp_path):
    td = _tema_dir(tmp_path)
    cliente = _ClienteModeracion(fallas=0, error_real_en=1)   # falla real en la 1ra, no moderación
    res = orquestador.generar_variantes_colorear(cliente, td, "safari", n=1, intentos_por_variante=4)
    assert len(res["errores"]) == 1 and not res["generadas"]
    assert cliente.llamadas == 1   # no reintenta un error que no es de moderación


def test_aprobar_afiche_va_a_extras_y_raiz(tmp_path):
    """El afiche aprobado debe quedar en extras/ (venta del kit) Y en la raíz
    (arte base de 'Invitación y afiche' / cartel) — antes solo iba a extras y
    las dos galerías mostraban afiches distintos (bug de Pablo 11-jul-2026)."""
    from ia_kit import aprobar as ia_aprobar
    base = tmp_path / "safari"; (base / "ia_draft").mkdir(parents=True)
    (base / "tema.json").write_text('{"edades":[1,2,3]}')
    Image.new("RGBA", (32, 32)).save(base / "ia_draft" / "afiche_2.png")
    Image.new("RGBA", (32, 32)).save(base / "ia_draft" / "stickers_1.png")
    ia_aprobar.aprobar(str(tmp_path), "safari")
    assert (base / "extras" / "afiche_2.png").exists()      # venta del kit
    assert (base / "afiche_2.png").exists()                 # arte base (raíz)
    assert (base / "extras" / "stickers_1.png").exists()    # el resto solo a extras
    assert not (base / "stickers_1.png").exists()
