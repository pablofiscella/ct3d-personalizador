"""Tests del cuaderno de actividades interactivo (actividades_web.py).

Mismo criterio que el resto del motor: lo que tiene respuesta correcta se
VERIFICA por código — laberinto transitable, sopa con las palabras realmente
en la grilla, sudoku válido y único, puntos normalizados."""
import json
import os
import shutil
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import actividades_web as aw  # noqa: E402

TEMA = "safari"
_TOK = "test-act-aabbccdd"


@pytest.fixture(scope="module")
def token():
    d = os.path.join(aw.ACT_DIR, _TOK)
    shutil.rmtree(d, ignore_errors=True)
    aw.crear({"nombre": "Sofía", "edad": "7"}, TEMA, token=_TOK)
    yield _TOK
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture(scope="module")
def data(token):
    return json.load(open(os.path.join(aw.ACT_DIR, token, "data.json"),
                          encoding="utf-8"))


def test_crear_genera_todo(token, data):
    d = os.path.join(aw.ACT_DIR, token)
    for fn in ("data.json", "manifest.json", "portada.jpg"):
        assert os.path.isfile(os.path.join(d, fn)), fn
    assert aw.estado(token) == "listo"
    assert len(data["personajes"]) >= 4
    assert len(data["sombras"]) == len(data["personajes"])
    for fn in data["personajes"] + data["sombras"] + data["colorear"]:
        assert os.path.isfile(os.path.join(d, fn)), fn


def test_bandas_de_edad():
    assert aw._banda("2") == "mini" and aw._banda("3") == "mini"
    assert aw._banda("4") == "media" and aw._banda("5") == "media"
    assert aw._banda("6") == "grande" and aw._banda("9") == "grande"
    assert aw._banda("") == "media"          # sin edad -> media (defecto)
    ids_mini = {m["id"] for m in aw._menu("mini", 3)}
    assert "sopa" not in ids_mini and "sudoku" not in ids_mini
    ids_grande = {m["id"] for m in aw._menu("grande", 7)}
    assert {"sopa", "sudoku", "sumas", "restas"} <= ids_grande
    # "posicion" (noción espacial arriba/abajo/adentro/afuera, Sala de 4
    # Bimestre 1 NAP, 14-jul-2026): banda media (4-5 años), no en mini ni grande
    ids_media4 = {m["id"] for m in aw._menu("media", 4)}
    assert "posicion" in ids_media4
    assert "posicion" not in ids_mini and "posicion" not in ids_grande
    # NAP Sala de 4: "conteo oral hasta el 5" — antes del 14-jul-2026 4 y 5
    # años compartían el mismo max=6 en "contar", sin distinguir dentro de
    # la banda "media".
    contar4 = next(m for m in aw._menu("media", 4) if m["id"] == "contar")
    contar5 = next(m for m in aw._menu("media", 5) if m["id"] == "contar")
    assert contar4["cfg"]["max"] == 5
    assert contar5["cfg"]["max"] == 8
    # NAP Sala de 5: "conteo oral hasta el 15 y comparación de colecciones"
    masmenos5 = next(m for m in aw._menu("media", 5) if m["id"] == "mas_menos")
    assert masmenos5["cfg"]["max"] == 8
    # "silabas" (conciencia fonológica, Bimestre 2): SOLO a los 5, no a los 4
    ids_media5 = {m["id"] for m in aw._menu("media", 5)}
    assert "silabas" in ids_media5
    assert "silabas" not in ids_media4


def test_laberintos_transitables(data):
    BIT = {"E": 4, "W": 8, "N": 1, "S": 2}
    for lab in data["laberintos"]:
        n, celdas, cam = lab["n"], lab["celdas"], lab["camino"]
        assert cam[0] == [0, 0] and cam[-1] == [n - 1, n - 1]
        for (x, y), (nx, ny) in zip(cam, cam[1:]):
            dx, dy = nx - x, ny - y
            dir_ = {(1, 0): "E", (-1, 0): "W", (0, 1): "S", (0, -1): "N"}[(dx, dy)]
            assert not celdas[y][x] & BIT[dir_], "pared en el camino"


def test_sopas_verificadas(data):
    assert data["sopas"], "banda grande sin sopas"
    for s in data["sopas"]:
        assert len(s["palabras"]) >= 4
        for w, cs in s["sol"].items():
            assert "".join(s["filas"][y][x] for x, y in cs) == w


def test_sudokus_validos(data):
    for su in data["sudokus"]:
        sol, puz = su["sol"], su["puz"]
        for i in range(4):
            assert sorted(sol[i]) == [0, 1, 2, 3]                    # filas
            assert sorted(f[i] for f in sol) == [0, 1, 2, 3]         # columnas
        for r0 in (0, 2):
            for c0 in (0, 2):                                        # cajas 2x2
                caja = [sol[r][c] for r in (r0, r0 + 1) for c in (c0, c0 + 1)]
                assert sorted(caja) == [0, 1, 2, 3]
        assert any(v is None for f in puz for v in f)
        for r in range(4):
            for c in range(4):
                assert puz[r][c] in (None, sol[r][c])


def test_figuras_normalizadas(data):
    for pts in data["figuras"].values():
        assert len(pts) >= 8
        assert all(0 <= x <= 1 and 0 <= y <= 1 for x, y in pts)


def test_tokens_invalidos():
    assert aw.estado("no-existe-xx") is None
    assert aw.estado("../../etc") is None
    assert aw.html("no-existe-xx") is None
    assert aw.archivo("no-existe-xx", "data.json") is None


# ─────────────────────────────────────────────────────────────────────────
# Audio-guía (14-jul-2026): "es la brecha de UX más urgente para 4-5 años,
# más urgente que sumar juegos nuevos" (investigación §2b) — consignas
# grabadas UNA vez (texto fijo del player, no personalizado), servidas como
# asset del repo igual que player.js/las fuentes.
def test_texto_para_tts_quita_emoji_conserva_el_resto():
    assert aw._texto_para_tts("Llevá a tu amigo hasta la estrella ⭐") == \
        "Llevá a tu amigo hasta la estrella"
    assert aw._texto_para_tts("Sin emoji acá") == "Sin emoji acá"


def test_slug_audio_deterministico_y_distinto_por_texto():
    a1 = aw._slug_audio("Tocá el que es DISTINTO")
    a2 = aw._slug_audio("Tocá el que es DISTINTO")
    b = aw._slug_audio("Otro texto")
    assert a1 == a2
    assert a1 != b
    assert a1.startswith("c_") and a1.endswith(".mp3")


def test_duracion_minima_escala_con_mas_vocales():
    """Encontrado 14-jul-2026 armando el juego de sílabas: una toma de TTS
    de "MARIPOSA" (4 sílabas) salió de 0.71s — la MISMA palabra en otras
    tomas dio 1.6-2.1s. El piso por conteo de vocales existe para detectar
    justo esa toma apurada/cortada y reintentar, en vez de venderla así."""
    corta = aw._duracion_minima("SOL")            # 1 vocal
    larga = aw._duracion_minima("MARIPOSA")        # 4 vocales
    assert larga > corta
    assert aw._duracion_minima("") >= 0.4          # piso absoluto, nunca 0


def test_generar_audio_consignas_idempotente_y_sirve_por_archivo(tmp_path, monkeypatch, token):
    """Mockea el TTS (no llama a ElevenLabs de verdad) para probar: genera lo
    nuevo, NO regenera lo que ya existe, el manifest mergea viejo+nuevo, y
    archivo() sirve tanto el manifest como cada mp3 a través del token."""
    monkeypatch.setattr(aw, "AUDIO_DIR", str(tmp_path))
    llamadas = []

    class FakeAudiolibro:
        @staticmethod
        def _tts_elevenlabs(texto, seed=None):
            llamadas.append(texto)
            return b"FAKE-MP3-BYTES" * 2000   # "dura" de sobra para pasar el piso de QA

        @staticmethod
        def _dur_mp3_128(mp3):
            return len(mp3) * 8 / 128000.0

    import sys
    monkeypatch.setitem(sys.modules, "audiolibro", FakeAudiolibro)

    m1 = aw.generar_audio_consignas(["Texto A", "Texto B"])
    assert len(llamadas) == 2
    assert set(m1) == {"Texto A", "Texto B"}

    # volver a pedir "Texto A" (ya existe) + un texto nuevo: NO regenera A
    m2 = aw.generar_audio_consignas(["Texto A", "Texto C"])
    assert llamadas == ["Texto A", "Texto B", "Texto C"]   # A no se repitió
    assert set(m2) == {"Texto A", "Texto B", "Texto C"}     # el manifest mergeó

    # archivo() sirve el manifest y cada mp3 a través del token real
    body, ct = aw.archivo(token, "audio_manifest.json")
    assert ct == "application/json; charset=utf-8"
    assert json.loads(body) == m2
    fn = m2["Texto A"]
    body2, ct2 = aw.archivo(token, fn)
    assert ct2 == "audio/mpeg" and body2 == b"FAKE-MP3-BYTES" * 2000


def test_archivo_rechaza_mp3_con_nombre_invalido(token):
    assert aw.archivo(token, "c_notahexvalue.mp3") is None
    assert aw.archivo(token, "../../etc/passwd.mp3") is None
    assert aw.archivo(token, "c_deadbeef00.mp3") is None  # nombre válido pero no existe


def test_archivo_whitelist(token):
    assert aw.archivo(token, "manifest.json") is None      # no expuesto
    assert aw.archivo(token, "../secreto.txt") is None
    assert aw.archivo(token, "data.json")[1].startswith("application/json")
    js = aw.archivo(token, "player.js")                     # sale del REPO
    assert js and b"GAMES" in js[0]
    assert aw.archivo(token, "f1.ttf")[1] == "font/ttf"
    assert aw.archivo(token, "p00.png")[1] == "image/png"


def test_html_personalizado(token):
    page = aw.html(token)
    assert "Las actividades de Sofía" in page
    assert "player.js?v=" in page


def test_paletas_completas():
    claves = set(aw._PALETA_DEFAULT)
    for tema, pal in aw.PALETAS.items():
        assert set(pal) == claves, tema


# ─────────────────────────────────────────────────────────────────────────
# Diploma de logro (14-jul-2026): Pablo — "cuando algún peque haga todo el
# cuaderno de actividades interactivo sin errores que le agregue el
# certificado de esa actividad para que lo pueda imprimir como un logro".
# Se renderiza EN VIVO (no se pre-genera con el resto de los assets del
# token) porque depende de algo que solo se sabe DESPUÉS de jugar.
def test_certificado_logro_token_valido(token, data):
    im = aw.certificado_logro(token)
    assert im is not None
    import certificado
    assert im.size == (certificado.WpH, certificado.HpH)


def test_certificado_logro_token_invalido():
    assert aw.certificado_logro("no-existe-xx") is None
    assert aw.certificado_logro("../../etc") is None
    assert aw.certificado_logro("") is None


# ─────────────────────────────────────────────────────────────────────────
# Nombre de vuelta a la compra (14-jul-2026, revierte 452be39 del
# 12-jul-2026): GUARDIÁN — mismo criterio que el guardián de la tienda
# (tests/test_tienda_app.py::test_agregar_sin_nombre_tipos_directos), para
# que una edición paralela de productos.py no vuelva a sacarlo por error.
def test_campos_actividades_web_pide_nombre():
    import productos
    assert "nombre" in productos.TIPOS["actividades-web"]["campos"]
    assert "nombre" in productos.PERSONALIZADAS["actividades-web"]["*"]


def test_preview_mock_refleja_el_nombre_tipeado():
    """Bug real (14-jul-2026, Pablo: "cambio la edad y aparece en la
    portada... pero no el nombre"): la vista previa en vivo del formulario
    de compra manda `nombre` en la query de /preview igual que `edad`, pero
    preview_mock lo ignoraba — la portada cambiaba de edad y quedaba muda
    ante el nombre. Con nombre, personaliza (igual criterio que crear());
    sin nombre, sigue genérica (ficha pública recién cargada, nadie
    escribió nada — no mostrar un nombre de muestra)."""
    generica = aw.preview_mock({"edad": "5", "nombre": ""}, TEMA)
    personalizada = aw.preview_mock({"edad": "5", "nombre": "Valentina"}, TEMA)
    assert generica.tobytes() != personalizada.tobytes()


def test_certificado_logro_nombre_del_perfil_pisa_al_de_la_compra(token):
    """El nombre de la compra vuelve a existir (14-jul-2026) pero es solo el
    DEFAULT del primer perfil, no una personalización dura — el player
    soporta VARIOS perfiles por token (Pablo: "pueden ser 2 chicos los que
    juegan en la misma casa"), y el nombre real del certificado viaja del
    perfil activo (query param), no del manifest de la compra."""
    im_a = aw.certificado_logro(token, nombre="Valentina")
    im_b = aw.certificado_logro(token, nombre="Benjamín")
    assert im_a is not None and im_b is not None
    assert im_a.tobytes() != im_b.tobytes()


def test_certificado_logro_sin_nombre_cae_al_de_la_compra(token, data):
    """El fixture 'token' del módulo se creó con nombre='Sofía' (línea 24) —
    sin nombre explícito, no debe quedar en blanco de la nada."""
    con_nombre_compra = aw.certificado_logro(token)
    con_nombre_explicito = aw.certificado_logro(token, nombre="Sofía")
    assert con_nombre_compra.tobytes() == con_nombre_explicito.tobytes()
