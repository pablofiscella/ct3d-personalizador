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
    # 1° grado (edad 6, banda "grande"): "serie" con tope=30 (NAP: "números
    # del 1 al 30") + juego nuevo "armar_palabra" (sílabas CV, Bimestre 2) —
    # ninguno de los dos debe filtrarse a un chico de 12 años (misma banda,
    # sin diferenciar por defecto).
    ids_grande6 = {m["id"] for m in aw._menu("grande", 6)}
    ids_grande12 = {m["id"] for m in aw._menu("grande", 12)}
    assert "armar_palabra" in ids_grande6
    assert "armar_palabra" not in ids_grande12
    serie6 = next(m for m in aw._menu("grande", 6) if m["id"] == "serie")
    serie10 = next(m for m in aw._menu("grande", 10) if m["id"] == "serie")
    assert serie6["cfg"]["tope"] == 30
    # Fase 0A (19-jul-2026, docs/auditoria-dc-caba/): el tope de "serie" ahora
    # CRECE con el grado. Antes solo e==6 lo subía a 30 y el resto caía al
    # default 16 del player, así que un chico de 6 recibía números MÁS ALTOS
    # que uno de 12 (dificultad invertida). Ahora es monótono creciente hasta
    # 5° (edad 10), que es el último grado que conserva "serie": desde 6° se
    # retira con el recorte del recreo (ver más abajo).
    assert serie10["cfg"]["tope"] > serie6["cfg"]["tope"]
    # Recorte de recreo en 6°-7° (20-jul-2026, docs/auditoria-dc-caba/: "17 de
    # 25 juegos de 6° son iguales a 1°"): los juegos de recreo babyish
    # (simon/patron/agrupar/quefalta/bingo/serie) se retiran de 6°-7° (e>=11).
    # Quedan los rompecabezas universales + el contenido curricular del grado.
    _recreo_baby = {"simon", "patron", "agrupar", "quefalta", "bingo", "serie"}
    for e_alto in (11, 12):
        ids_alto = {m["id"] for m in aw._menu("grande", e_alto)}
        assert not (_recreo_baby & ids_alto), f"recreo babyish no retirado en edad {e_alto}"
    # y siguen presentes en 5° (edad 10) — el recorte es SOLO para 6°-7°.
    assert _recreo_baby & {m["id"] for m in aw._menu("grande", 10)}
    # Fase 0A (19-jul-2026) + rollout DC CABA 3° (19-jul-2026): los juegos clavados
    # en dificultad de inicial que NO escalan (sumas/restas cuentan sprites;
    # contar/mas_menos ≤9; colorear/puntos sin anclaje) se retiran de 3°-7° (e>=8).
    # Fase 0A los sacó de 4°-7°; al construir el contenido de 3° se sacaron también
    # de 3°. Siguen presentes en 1°-2° (e<=7).
    _inicial = {"sumas", "restas", "contar", "mas_menos", "colorear", "puntos"}
    for e_grande in (8, 9, 10, 11, 12):
        ids_e = {m["id"] for m in aw._menu("grande", e_grande)}
        assert not (_inicial & ids_e), f"juegos de inicial no retirados en edad {e_grande}"
    assert {"sumas", "restas"} <= {m["id"] for m in aw._menu("grande", 7)}  # 2° aún los tiene
    # resto de 1° grado (14-jul-2026, cierre del año — NAP "Ideas web" por
    # bimestre): ninguno debe filtrarse a los 12 años.
    nuevos_1grado = {"abecedario", "suma_rapida", "campo_ciudad", "planta_fruto", "materiales", "grilla100"}
    assert nuevos_1grado <= ids_grande6
    assert not (nuevos_1grado & ids_grande12)
    # sin íconos repetidos dentro del mismo menú (bug real encontrado
    # armando esto: armar_palabra/abecedario pisaban el ícono de
    # sudoku/sopa ya existentes)
    iconos = [m["icono"] for m in aw._menu("grande", 6)]
    assert len(iconos) == len(set(iconos)), "íconos repetidos en el menú de 6 años"
    # 2° grado (14-jul-2026, edad 7 — NAP "Ideas web" por bimestre):
    # ninguno se filtra a 6 ni a 12 años, sin íconos repetidos.
    ids_grande7 = {m["id"] for m in aw._menu("grande", 7)}
    nuevos_2grado = {"sustantivos", "sumas_redondas", "sinonimos_antonimos",
                      "multiplicacion_concepto", "conductor_aislante",
                      "familia_palabras", "trivia_espacial", "tablas_contrarreloj"}
    assert nuevos_2grado <= ids_grande7
    assert not (nuevos_2grado & ids_grande6)
    assert not (nuevos_2grado & ids_grande12)
    iconos7 = [m["icono"] for m in aw._menu("grande", 7)]
    assert len(iconos7) == len(set(iconos7)), "íconos repetidos en el menú de 7 años"
    # 3° grado (14-jul-2026, edad 8 — NAP "Ideas web" por bimestre):
    # ninguno se filtra a 6, 7 ni 12 años, sin íconos repetidos.
    ids_grande8 = {m["id"] for m in aw._menu("grande", 8)}
    # separador_mezclas se retiró en el rollout DC CABA 3° (reemplazado por
    # estados_materia). Se suman las 3 nuevas exclusivas de 3° (reparto con resto,
    # comparar números, estados de la materia). comprension_lectora/recta_numerica
    # NO van acá: se comparten con 4° (no son exclusivas de 3°).
    # comparar_numeros pasó a compartirse con 2° (rollout 1°/2°, 19-jul), como
    # comprension_lectora/recta_numerica → sale del set de EXCLUSIVAS de 3°.
    nuevos_3grado = {"animal_comida", "partes_oracion", "tabla_pitagorica",
                      "tiempos_verbales", "estaciones", "cuerpos_geometricos",
                      "cajero_automatico", "reparto_con_resto", "estados_materia"}
    assert nuevos_3grado <= ids_grande8
    assert not (nuevos_3grado & ids_grande6)
    assert not (nuevos_3grado & ids_grande7)
    assert not (nuevos_3grado & ids_grande12)
    iconos8 = [m["icono"] for m in aw._menu("grande", 8)]
    assert len(iconos8) == len(set(iconos8)), "íconos repetidos en el menú de 8 años"
    # 4° grado (14-jul-2026, edad 9 — NAP "Ideas web" por bimestre):
    # ninguno se filtra a 6, 7, 8 ni 12 años, sin íconos repetidos.
    ids_grande9 = {m["id"] for m in aw._menu("grande", 9)}
    nuevos_4grado = {"abstractos_concretos", "provincias_region", "acentuacion",
                      "fotosintesis", "laboratorio_electrico", "fracciones_equivalentes",
                      "angulos", "prefijos_sufijos"}
    assert nuevos_4grado <= ids_grande9
    assert not (nuevos_4grado & ids_grande6)
    assert not (nuevos_4grado & ids_grande7)
    assert not (nuevos_4grado & ids_grande8)
    assert not (nuevos_4grado & ids_grande12)
    iconos9 = [m["icono"] for m in aw._menu("grande", 9)]
    assert len(iconos9) == len(set(iconos9)), "íconos repetidos en el menú de 9 años"
    # 5° grado (14-jul-2026, edad 10 — NAP "Ideas web" por bimestre):
    # ninguno se filtra a 6, 7, 8, 9 ni 12 años, sin íconos repetidos.
    ids_grande10 = {m["id"] for m in aw._menu("grande", 10)}
    nuevos_5grado = {"trivia_colonial", "camino_digestivo", "fracciones_avanzado",
                      "analisis_sintactico", "pago_exacto", "actividad_economica",
                      "planta_potabilizadora", "derechos_constitucion"}
    assert nuevos_5grado <= ids_grande10
    assert not (nuevos_5grado & ids_grande6)
    assert not (nuevos_5grado & ids_grande7)
    assert not (nuevos_5grado & ids_grande8)
    assert not (nuevos_5grado & ids_grande9)
    assert not (nuevos_5grado & ids_grande12)
    iconos10 = [m["icono"] for m in aw._menu("grande", 10)]
    assert len(iconos10) == len(set(iconos10)), "íconos repetidos en el menú de 10 años"
    # 6° grado (14-jul-2026, edad 11 — NAP "Ideas web" por bimestre):
    # ninguno se filtra a 6-10 ni 12 años, sin íconos repetidos.
    ids_grande11 = {m["id"] for m in aw._menu("grande", 11)}
    nuevos_6grado = {"celula_partes", "hechos_opiniones", "sistema_nervioso",
                      "viaje_inmigrante", "fraccion_de_cantidad", "sufragio_argentina",
                      "energia_renovable", "poligonos_lados"}
    assert nuevos_6grado <= ids_grande11
    assert not (nuevos_6grado & ids_grande6)
    assert not (nuevos_6grado & ids_grande7)
    assert not (nuevos_6grado & ids_grande8)
    assert not (nuevos_6grado & ids_grande9)
    assert not (nuevos_6grado & ids_grande10)
    assert not (nuevos_6grado & ids_grande12)
    iconos11 = [m["icono"] for m in aw._menu("grande", 11)]
    assert len(iconos11) == len(set(iconos11)), "íconos repetidos en el menú de 11 años"
    # 7° grado (14-jul-2026, edad 12 — año de egreso, fin del NAP — "Ideas
    # web" por bimestre): ninguno se filtra a 6-11 años, sin íconos repetidos.
    ids_grande12_full = {m["id"] for m in aw._menu("grande", 12)}
    nuevos_7grado = {"traductor_algebraico", "planetas_tipo", "linea_democracia",
                      "sistema_reproductor", "estadistica_datos", "red_trofica",
                      "area_perimetro", "escape_room_egreso"}
    assert nuevos_7grado <= ids_grande12_full
    assert not (nuevos_7grado & ids_grande6)
    assert not (nuevos_7grado & ids_grande7)
    assert not (nuevos_7grado & ids_grande8)
    assert not (nuevos_7grado & ids_grande9)
    assert not (nuevos_7grado & ids_grande10)
    assert not (nuevos_7grado & ids_grande11)
    iconos12 = [m["icono"] for m in aw._menu("grande", 12)]
    assert len(iconos12) == len(set(iconos12)), "íconos repetidos en el menú de 12 años"


def test_incluidos_por_edad_llega_hasta_12():
    """16-jul-2026: incluidos_por_edad() estaba fija en 2-8 (el dropdown de
    la ficha de la tienda también) aunque _menu() ya tenía el contenido NAP
    de 9 a 12 armado — Pablo no podía elegir esas edades para ver qué
    actividades trae. La tienda usa este dict para desbloquear/reordenar la
    galería "Qué incluye" según la edad elegida."""
    inc = aw.incluidos_por_edad()
    assert set(inc.keys()) == {str(e) for e in range(2, 13)}
    # cada edad nueva (9-12) trae contenido curricular real, no una copia
    # del menú de 8 años — mismo criterio que el resto del archivo (ids
    # nuevos por grado, ver test_bandas_de_edad).
    for e in ("9", "10", "11", "12"):
        assert inc[e] != inc["8"]
        assert inc[e]  # nunca vacío


def test_catalogo_juegos_incluye_9_a_12():
    """16-jul-2026: _catalogo_juegos() (arma las pestañas de /editor-simple
    y las cards de la galería "Qué incluye") solo sampleaba edades 2, 5 y 8
    — los juegos exclusivos de 9-12 (grados 4to-7mo) nunca aparecían sin
    importar qué edad se eligiera. Pablo: "pongo 8 años se actualiza pero
    no muestra las actividades distintas"."""
    ids = {j["id"] for j in aw._catalogo_juegos()}
    # un juego de cada grado nuevo: 9="abstractos_concretos" (4to), 10=
    # "trivia_colonial" (5to), 11="celula_partes" (6to), 12="traductor_algebraico"
    # (7mo/egreso) — ver test_bandas_de_edad.
    for exclusivo in ("abstractos_concretos", "trivia_colonial",
                       "celula_partes", "traductor_algebraico"):
        assert exclusivo in ids, f"{exclusivo} no está en el catálogo"
    assert len(ids) > 30  # antes del fix: 30 (solo hasta 8 años)


def test_catalogo_juegos_cubre_todas_las_edades():
    """Invariante anti-regresión (auditoría 16-jul-2026): _catalogo_juegos()
    debe incluir la UNIÓN de los menús reales de TODAS las edades del dropdown
    (2 a 12). El fix de 9-12 había salteado 6 y 7 (banda "grande"), así que sus
    15 juegos NAP nunca aparecían en la galería ni en el editor. Este test falla
    si CUALQUIER edad aporta un juego que el catálogo no lista — no solo 6-7."""
    catalogo = {j["id"] for j in aw._catalogo_juegos()}
    union = set()
    for edad in range(2, 13):
        banda = aw._banda(edad)
        union |= {m["id"] for m in aw._menu(banda, str(edad))}
    faltantes = union - catalogo
    assert not faltantes, f"el catálogo se saltea juegos de alguna edad: {sorted(faltantes)}"


def test_laberintos_transitables(data):
    BIT = {"E": 4, "W": 8, "N": 1, "S": 2}
    for lab in data["laberintos"]:
        n, celdas, cam = lab["n"], lab["celdas"], lab["camino"]
        assert cam[0] == [0, 0] and cam[-1] == [n - 1, n - 1]
        for (x, y), (nx, ny) in zip(cam, cam[1:]):
            dx, dy = nx - x, ny - y
            dir_ = {(1, 0): "E", (-1, 0): "W", (0, 1): "S", (0, -1): "N"}[(dx, dy)]
            assert not celdas[y][x] & BIT[dir_], "pared en el camino"


def test_laberintos_chicos_transitables(data):
    """laberintos_chicos (14-jul-2026, prototipo "programá el camino"):
    mismo generador/verificación que los laberintos normales, tamaño propio
    (3-4 celdas) para que la secuencia de instrucciones sea corta."""
    BIT = {"E": 4, "W": 8, "N": 1, "S": 2}
    assert len(data["laberintos_chicos"]) == 3
    for lab in data["laberintos_chicos"]:
        assert lab["n"] <= 4, "tienen que quedarse chicos: el chico arma la secuencia a mano"
        n, celdas, cam = lab["n"], lab["celdas"], lab["camino"]
        assert cam[0] == [0, 0] and cam[-1] == [n - 1, n - 1]
        for (x, y), (nx, ny) in zip(cam, cam[1:]):
            dx, dy = nx - x, ny - y
            dir_ = {(1, 0): "E", (-1, 0): "W", (0, 1): "S", (0, -1): "N"}[(dx, dy)]
            assert not celdas[y][x] & BIT[dir_], "pared en el camino"


def test_programar_camino_registrado():
    """Prototipo de pensamiento computacional (14-jul-2026, idea de Pablo) —
    provisorio en la banda base de TODAS las edades grande (1°-7°) mientras
    se valida la mecánica."""
    for edad in (6, 7, 8, 9, 10, 11, 12):
        ids = {m["id"] for m in aw._menu("grande", edad)}
        assert "programar_camino" in ids, f"falta en edad {edad}"


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


def test_duracion_minima_mas_permisiva_en_oraciones_largas():
    """Bug real de calibración (14-jul-2026, armando 1° grado): la tasa por
    vocal de _duracion_minima() se calibró con PALABRAS sueltas (GATO,
    MARIPOSA...), que se enuncian más despacio por vocal que una ORACIÓN
    dicha con cadencia natural. Con una tasa única, la consigna YA
    VENDIDA "Escuchá la palabra y elegí cuántas partes tiene" (3.74s, 18
    vocales, en producción desde Sala de 5) quedaba MARCADA COMO ROTA por
    el propio piso — puro ruido de calibración, no un problema real de
    audio (verificado: tomas frescas independientes de otra oración nueva
    caen en el mismo rango que la ya guardada). La tasa baja solo para
    textos largos (>6 vocales) evita este falso positivo sin perder
    sensibilidad en palabras sueltas."""
    oracion_real = "Escuchá la palabra y elegí cuántas partes tiene"
    assert aw._duracion_minima(oracion_real) <= 3.74
    # una palabra corta (<=6 vocales) sigue con la tasa estricta original
    assert aw._duracion_minima("MARIPOSA") == max(0.4, 4 * 0.22)


def test_duracion_maxima_escala_con_mas_vocales():
    """Encontrado 14-jul-2026 armando 1° grado: una toma de TTS de "SAPO"
    (2 vocales, esperable ~0.7-1s como GATO/PATO/MOTO) salió de 2.72s — el
    piso no agarra esto (2.72s > mínimo), hace falta un TECHO simétrico."""
    corta = aw._duracion_maxima("SAPO")            # 2 vocales
    larga = aw._duracion_maxima("MARIPOSA")        # 4 vocales
    assert larga > corta
    assert aw._duracion_maxima("SAPO") < 2.72      # la toma rota real, fuera del rango
    assert aw._duracion_maxima("") >= 2.5          # techo absoluto


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


def test_generar_audio_consignas_descarta_toma_demasiado_larga(tmp_path, monkeypatch):
    """Regresión del bug real de "SAPO" (14-jul-2026): una toma
    desmedidamente larga (fuera del techo) no se guarda tal cual — reintenta
    hasta encontrar una dentro de rango, y no sigue probando de más una vez
    que la encuentra."""
    monkeypatch.setattr(aw, "AUDIO_DIR", str(tmp_path))
    # SAPO: minimo=0.44s, maximo=2.5s. Las primeras 2 tomas quedan MUY largas
    # (6.25s, como la toma real 2.72s que motivó este test, exagerada acá
    # para no depender de números finos); la 3ra cae en rango (1s).
    tomas = [b"X" * 100000, b"X" * 100000, b"X" * 16000, b"NUNCA-SE-USA"]
    llamadas = []

    class FakeAudiolibro:
        @staticmethod
        def _tts_elevenlabs(texto, seed=None):
            llamadas.append(seed)
            return tomas[len(llamadas) - 1]

        @staticmethod
        def _dur_mp3_128(mp3):
            return len(mp3) * 8 / 128000.0

    import sys
    monkeypatch.setitem(sys.modules, "audiolibro", FakeAudiolibro)

    m = aw.generar_audio_consignas(["SAPO"])
    assert len(llamadas) == 3   # se frena apenas encuentra una toma en rango, no prueba la 4ta
    fn = m["SAPO"]
    guardado = open(os.path.join(str(tmp_path), fn), "rb").read()
    assert guardado == tomas[2]   # se queda con la que cayó en rango, no con las largas de antes


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


def test_sopa_no_sale_pobre_ni_vacia():
    """Auditoría B6: se filtra por largo ANTES de samplear (la sopa es 10×10) y se
    descartan sopas con <4 palabras. Antes, si el sample caía en palabras largas,
    la sopa salía pobre o vacía."""
    import actividades_web as aw
    for tema in ("safari", "circo", "monstruos"):
        dj = aw._armar_data(tema, "Test", "10", 123)
        for s in dj.get("sopas", []):
            assert len(s.get("palabras", [])) >= 4, f"{tema}: sopa pobre {s.get('palabras')}"


def test_generar_audio_consignas_error_claro_sin_key(monkeypatch):
    """Auditoría B7: sin ElevenLabs, _tts_elevenlabs devuelve None y _dur_mp3_128(None)
    tiraba 'len(None)'. Ahora es un RuntimeError claro."""
    import pytest, actividades_web as aw, audiolibro
    monkeypatch.setattr(audiolibro, "_tts_elevenlabs", lambda *a, **k: None)
    with pytest.raises(RuntimeError, match="ELEVENLABS"):
        aw.generar_audio_consignas(["Encontrá las palabras escondidas."])


def test_niveles_activacion_escalable(tmp_path, monkeypatch):
    """Activación escalable por NIVELES (19-jul-2026): un token premium agrupa el
    menú en niveles (1 gratis, 2/3 con candado), desbloquear_nivel sube el
    nivel_max de forma monótona y registrar_solicitud captura el evento para el
    mail al comprador. Gateado por token → los links normales no cambian."""
    tok = "test-niv-11223344"
    d = os.path.join(aw.ACT_DIR, tok)
    shutil.rmtree(d, ignore_errors=True)
    try:
        aw.crear({"nombre": "Sofía", "edad": "9", "premium_on": True}, TEMA, token=tok)
        dj = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
        # el token premium expone el modelo de niveles
        assert dj.get("premium_on") is True
        assert dj.get("nivel_max") == 1
        assert len(dj.get("niveles") or []) > 1, "un token de 4° tiene varios niveles"
        assert all("nivel" in m for m in dj["menu"]), "cada item del menú lleva su nivel"
        assert {m["nivel"] for m in dj["menu"]} >= {1, 2}, "hay actividades más allá del nivel 1"

        # desbloquear_nivel: sube, es monótono (no baja) y falla claro si no existe
        assert aw.desbloquear_nivel(tok, 2) == 2
        assert json.load(open(os.path.join(d, "data.json"))).get("nivel_max") == 2
        assert aw.desbloquear_nivel(tok, 1) == 2, "bajar no baja el nivel_max"
        assert aw.desbloquear_nivel("no-existe-xyz", 2) is None

        # el nivel_max desbloqueado se PRESERVA al regenerar el token (no se
        # "pierde" la compra al re-armar)
        aw.crear({"nombre": "Sofía", "edad": "9", "premium_on": True}, TEMA, token=tok)
        assert json.load(open(os.path.join(d, "data.json"))).get("nivel_max") == 2

        # registrar_solicitud / solicitudes_pendientes (aislado a tmp)
        monkeypatch.setattr(aw, "BASEDIR", str(tmp_path))
        aw.registrar_solicitud(tok, 2, "domino")
        aw.registrar_solicitud(tok, 3, "pidio")
        sols = aw.solicitudes_pendientes()
        assert len(sols) == 2
        assert sols[0]["nivel"] == 2 and sols[0]["motivo"] == "domino"
        assert sols[1]["nivel"] == 3 and sols[1]["motivo"] == "pidio"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_token_normal_sin_niveles_no_bloquea():
    """El gate es por token: sin premium_on, el token no queda en modo premium
    (el player muestra el menú plano de siempre). Los links vivos no cambian."""
    tok = "test-normal-55667788"
    d = os.path.join(aw.ACT_DIR, tok)
    shutil.rmtree(d, ignore_errors=True)
    try:
        aw.crear({"nombre": "Sofía", "edad": "9"}, TEMA, token=tok)
        dj = json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
        assert not dj.get("premium_on")
        assert dj.get("nivel_max") == 1
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_gate_por_cuenta_flags_y_revocar():
    """Acceso gateado (Fase 2): un token con requiere_cuenta expone el estado del
    gate, revocar() lo corta, y ambos flags se PRESERVAN al regenerar el token.
    Un token normal no queda gateado (público como siempre)."""
    tok = "test-gate-aabbccdd"
    d = os.path.join(aw.ACT_DIR, tok)
    shutil.rmtree(d, ignore_errors=True)
    try:
        aw.crear({"nombre": "Sofía", "edad": "9", "requiere_cuenta": True}, TEMA, token=tok)
        assert aw.estado_gate(tok) == (True, False)          # gateado, no revocado
        assert aw.revocar(tok, True) is True                 # cortar acceso
        assert aw.estado_gate(tok) == (True, True)
        # regenerar preserva requiere_cuenta y revocado (no "des-gatea" ni "des-revoca")
        aw.crear({"nombre": "Sofía", "edad": "9"}, TEMA, token=tok)
        assert aw.estado_gate(tok) == (True, True)
        assert aw.revocar(tok, False) is False               # restaurar
        assert aw.estado_gate(tok) == (True, False)
        assert aw.revocar("no-existe-xyz", True) is None
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_token_normal_no_esta_gateado():
    tok = "test-nogate-11223344"
    d = os.path.join(aw.ACT_DIR, tok)
    shutil.rmtree(d, ignore_errors=True)
    try:
        aw.crear({"nombre": "Sofía", "edad": "9"}, TEMA, token=tok)
        assert aw.estado_gate(tok) == (False, False)         # público como siempre
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_cuenta_larga_division_guiada():
    """La cuenta paso a paso (M6 4° / M7 5°, docs/auditoria-dc-caba/): la división
    como PROCEDIMIENTO guiado, no trivia. Debe estar en 4°-7° (edad 9-12) con el
    nivel correcto (1 exacta en 4°, 2 con resto en 5°-7°), y NO en grados menores.
    El ícono no puede colisionar con otro del mismo menú (bug real ya conocido)."""
    # ausente en 1°-3° (edad <= 8)
    for edad in (6, 7, 8):
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "cuenta_larga" not in ids, f"cuenta_larga no debería estar en edad {edad}"
    # presente en 4°-7° con el nivel correcto
    niveles_esperados = {9: 1, 10: 2, 11: 2, 12: 2}
    for edad, niv in niveles_esperados.items():
        menu = aw._menu(aw._banda(edad), edad)
        cl = next((m for m in menu if m["id"] == "cuenta_larga"), None)
        assert cl is not None, f"falta cuenta_larga en edad {edad}"
        assert cl["cfg"]["nivel"] == niv, f"nivel de cuenta_larga en edad {edad}"
        # sin íconos repetidos dentro del menú (🪜 recién agregado)
        iconos = [m["icono"] for m in menu]
        assert len(iconos) == len(set(iconos)), f"íconos repetidos en edad {edad}"


def test_transportador_medir_angulos():
    """Leer el transportador (M14 modo C, docs/auditoria-dc-caba/grado-5.md):
    MEDIR el ángulo leyendo el transportador (¿40° o 140°?), la escala equivocada
    como misconception. En 4° el ángulo se CLASIFICA (agudo/recto/obtuso); el
    transportador debe estar en 5°-7° (edad 10-12) y NO en 4° ni antes, sin
    colisión de íconos en el menú."""
    for edad in (6, 7, 8, 9):   # 1°-4°: no lo tienen (4° tiene 'angulos', clasificar)
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "transportador" not in ids, f"transportador no debería estar en edad {edad}"
    for edad in (10, 11, 12):
        menu = aw._menu(aw._banda(edad), edad)
        assert any(m["id"] == "transportador" for m in menu), f"falta transportador en edad {edad}"
        iconos = [m["icono"] for m in menu]
        assert len(iconos) == len(set(iconos)), f"íconos repetidos en edad {edad}"
    # 4° conserva la clasificación de ángulos (no se pisó)
    assert any(m["id"] == "angulos" for m in aw._menu(aw._banda(9), 9))


def test_reloj_leer_la_hora():
    """Leer el reloj (medida del tiempo, docs/auditoria-dc-caba/): mecánica nodal
    que faltaba entera. Debe estar en 2°-3° (edad 7-8) con el nivel correcto
    (1 = en punto y media; 2 = cuartos y de a 5/10), y NO en 1° ni 4°+, sin
    colisión de íconos en el menú."""
    for edad in (6, 9, 10):   # 1° y 4°+: no lo tienen
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "reloj" not in ids, f"reloj no debería estar en edad {edad}"
    niveles = {7: 1, 8: 2}
    for edad, niv in niveles.items():
        menu = aw._menu(aw._banda(edad), edad)
        rl = next((m for m in menu if m["id"] == "reloj"), None)
        assert rl is not None, f"falta reloj en edad {edad}"
        assert rl["cfg"]["nivel"] == niv, f"nivel de reloj en edad {edad}"
        iconos = [m["icono"] for m in menu]
        assert len(iconos) == len(set(iconos)), f"íconos repetidos en edad {edad}"


def test_arbol_probabilidad_azar():
    """Árbol de probabilidad / combinatoria (azar, docs/auditoria-dc-caba/):
    diagrama de árbol + principio multiplicativo, mecánica que faltaba entera.
    Debe estar en 6°-7° (edad 11-12) y NO en 5° ni antes, sin colisión de íconos."""
    for edad in (8, 9, 10):   # 3°-5°: no lo tienen
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "arbol_probabilidad" not in ids, f"arbol_probabilidad no debería estar en edad {edad}"
    for edad in (11, 12):
        menu = aw._menu(aw._banda(edad), edad)
        assert any(m["id"] == "arbol_probabilidad" for m in menu), f"falta arbol_probabilidad en edad {edad}"
        iconos = [m["icono"] for m in menu]
        assert len(iconos) == len(set(iconos)), f"íconos repetidos en edad {edad}"


def test_sujeto_predicado_analisis():
    """Sujeto y predicado — dividir la oración (análisis sintáctico, hueco de
    Lengua; grado-4.md lo marca ausente en 4°). Debe estar en 4°-5° (edad 9-10)
    y NO en 3° ni 6°+, sin colisión de íconos. 5° conserva la fluidez
    (analisis_sintactico) — son complementarios."""
    for edad in (7, 8, 11, 12):   # 2°/3° y 6°+: no lo tienen
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "sujeto_predicado" not in ids, f"sujeto_predicado no debería estar en edad {edad}"
    for edad in (9, 10):
        menu = aw._menu(aw._banda(edad), edad)
        assert any(m["id"] == "sujeto_predicado" for m in menu), f"falta sujeto_predicado en edad {edad}"
        iconos = [m["icono"] for m in menu]
        assert len(iconos) == len(set(iconos)), f"íconos repetidos en edad {edad}"
    # 5° mantiene la fluidez (el núcleo ya en negrita) además de la división
    assert any(m["id"] == "analisis_sintactico" for m in aw._menu(aw._banda(10), 10))


def test_historia_originarios_sociales_4():
    """Ciencias Sociales histórico de 4° (docs/auditoria-dc-caba/grado-4.md, gap #4:
    originarios→conquista→colonia→fundaciones = 'cero actividades'). Trivia de
    contenido (complementa linea_tiempo que ordena la cronología). Debe estar en 4°
    (edad 9) y NO en 3° ni 5°+, sin colisión de íconos."""
    for edad in (7, 8, 10, 11):
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "historia_originarios" not in ids, f"historia_originarios no debería estar en edad {edad}"
    menu = aw._menu(aw._banda(9), 9)
    assert any(m["id"] == "historia_originarios" for m in menu), "falta historia_originarios en 4°"
    iconos = [m["icono"] for m in menu]
    assert len(iconos) == len(set(iconos)), "íconos repetidos en 4°"
    # 4° conserva la cronología (linea_tiempo) — son complementarios
    assert any(m["id"] == "linea_tiempo" for m in menu)


def test_dialogo_raya_lengua_4():
    """El diálogo con raya (4° grado, docs/auditoria-dc-caba/grado-4.md gap #3 de
    Lengua). Trivia de puntuación del diálogo. Debe estar en 4° (edad 9) y NO en 3°
    ni 5°+, sin colisión de íconos."""
    for edad in (7, 8, 10, 11):
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "dialogo_raya" not in ids, f"dialogo_raya no debería estar en edad {edad}"
    menu = aw._menu(aw._banda(9), 9)
    assert any(m["id"] == "dialogo_raya" for m in menu), "falta dialogo_raya en 4°"
    iconos = [m["icono"] for m in menu]
    assert len(iconos) == len(set(iconos)), "íconos repetidos en 4°"


def test_conectores_4to_nivel_simple():
    """Conectores en 4° (docs/auditoria-dc-caba/grado-4.md gap #3): se agrega con
    nivel 1 (subconjunto simple, sin adversativos cargados que quedan para 5°+).
    Ícono propio (🔗 ya lo usa prefijos_sufijos en 4°). 5°-7° lo conservan sin
    nivel (→ banco completo, comportamiento intacto)."""
    menu4 = aw._menu(aw._banda(9), 9)
    c4 = next((m for m in menu4 if m["id"] == "conectores"), None)
    assert c4 is not None, "falta conectores en 4°"
    assert c4["cfg"].get("nivel") == 1, "conectores de 4° debe ser nivel 1 (simple)"
    iconos4 = [m["icono"] for m in menu4]
    assert len(iconos4) == len(set(iconos4)), "íconos repetidos en 4°"
    # 5°-7° conservan conectores SIN nivel (banco completo, sin regresión)
    for edad in (10, 11, 12):
        c = next((m for m in aw._menu(aw._banda(edad), edad) if m["id"] == "conectores"), None)
        assert c is not None and "nivel" not in c["cfg"], f"conectores de edad {edad} no debe tener nivel"


def test_mejor_oferta_proporcionalidad_4():
    """La mejor oferta (M12, 4° grado — docs/auditoria-dc-caba/grado-4.md gap #5:
    proporcionalidad + Ed. Financiera). Debe estar en 4° (edad 9) y NO en 3° ni 5°+,
    sin colisión de íconos."""
    for edad in (7, 8, 10, 11):
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "mejor_oferta" not in ids, f"mejor_oferta no debería estar en edad {edad}"
    menu = aw._menu(aw._banda(9), 9)
    assert any(m["id"] == "mejor_oferta" for m in menu), "falta mejor_oferta en 4°"
    iconos = [m["icono"] for m in menu]
    assert len(iconos) == len(set(iconos)), "íconos repetidos en 4°"


def test_suma_columnas_3ro_rango():
    """Suma con llevada en columna en 3° (docs/auditoria-dc-caba/grado-3.md gap #1:
    algoritmo hasta 10.000, el corazón de Matemática 3°). Reusa suma_columnas con
    rango propio (3→4 cifras). 4° conserva su rango (sin cifrasMin → default 4→5)."""
    m3 = next((m for m in aw._menu(aw._banda(8), 8) if m["id"] == "suma_columnas"), None)
    assert m3 is not None, "falta suma_columnas en 3°"
    assert m3["cfg"].get("cifrasMin") == 3 and m3["cfg"].get("cifrasMax") == 4, "rango de 3° debe ser 3→4 cifras"
    iconos3 = [m["icono"] for m in aw._menu(aw._banda(8), 8)]
    assert len(iconos3) == len(set(iconos3)), "íconos repetidos en 3°"
    # 4° conserva suma_columnas SIN cifrasMin (rango grande, sin regresión)
    m4 = next((m for m in aw._menu(aw._banda(9), 9) if m["id"] == "suma_columnas"), None)
    assert m4 is not None and "cifrasMin" not in m4["cfg"], "4° no debe tener cifrasMin (rango original)"
    # 1°-2° no lo tienen
    for edad in (6, 7):
        assert not any(m["id"] == "suma_columnas" for m in aw._menu(aw._banda(edad), edad))


def test_resta_columnas_3ro():
    """Resta con préstamo en columna en 3° (docs/auditoria-dc-caba/grado-3.md gap
    #1/#3: el otro algoritmo nodal de 3°). Debe estar en 3° (edad 8) con rango 3→4
    cifras, y NO en 1°-2° ni 4°+, sin colisión de íconos."""
    m3 = next((m for m in aw._menu(aw._banda(8), 8) if m["id"] == "resta_columnas"), None)
    assert m3 is not None, "falta resta_columnas en 3°"
    assert m3["cfg"].get("cifrasMin") == 3 and m3["cfg"].get("cifrasMax") == 4
    iconos = [m["icono"] for m in aw._menu(aw._banda(8), 8)]
    assert len(iconos) == len(set(iconos)), "íconos repetidos en 3°"
    for edad in (6, 7, 9, 10):
        assert not any(m["id"] == "resta_columnas" for m in aw._menu(aw._banda(edad), edad))


def test_silaba_tonica_3ro():
    """La sílaba tónica (3° grado — docs/auditoria-dc-caba/grado-3.md gap #2:
    acentuación, el contenido estrella de Lengua 3°). Tocar la sílaba fuerte. Debe
    estar en 3° (edad 8) y NO en 2° ni 4°+, sin colisión de íconos."""
    for edad in (6, 7, 9, 10):
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "silaba_tonica" not in ids, f"silaba_tonica no debería estar en edad {edad}"
    menu = aw._menu(aw._banda(8), 8)
    assert any(m["id"] == "silaba_tonica" for m in menu), "falta silaba_tonica en 3°"
    iconos = [m["icono"] for m in menu]
    assert len(iconos) == len(set(iconos)), "íconos repetidos en 3°"


def test_cielo_observacion_3ro():
    """Observación del cielo (3° grado — docs/auditoria-dc-caba/grado-3.md gap #5:
    bloque nuevo de CdM, ausente). Trivia de contenido. Debe estar en 3° (edad 8) y
    NO en 2° ni 4°+, sin colisión de íconos."""
    for edad in (6, 7, 9, 10):
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "cielo" not in ids, f"cielo no debería estar en edad {edad}"
    menu = aw._menu(aw._banda(8), 8)
    assert any(m["id"] == "cielo" for m in menu), "falta cielo en 3°"
    iconos = [m["icono"] for m in menu]
    assert len(iconos) == len(set(iconos)), "íconos repetidos en 3°"


def test_independencia_5to_sociales():
    """Proceso 1810-1853 en 5° (docs/auditoria-dc-caba/grado-5.md gap #3: Sociales de
    5° ausente, solo había lo colonial de 4°). Trivia de contenido. Debe estar en 5°
    (edad 10) y NO en 4° ni 6°+, sin colisión de íconos."""
    for edad in (8, 9, 11, 12):
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "independencia_arg" not in ids, f"independencia_arg no debería estar en edad {edad}"
    menu = aw._menu(aw._banda(10), 10)
    assert any(m["id"] == "independencia_arg" for m in menu), "falta independencia_arg en 5°"
    iconos = [m["icono"] for m in menu]
    assert len(iconos) == len(set(iconos)), "íconos repetidos en 5°"


def test_probabilidad_sucesos_6to():
    """Sucesos seguro/posible/imposible en 6° (docs/auditoria-dc-caba/grado-6.md gap
    #3: probabilidad, nodal por primera vez en 6°). El árbol cubre el conteo; esto,
    el lenguaje cualitativo. Debe estar en 6° (edad 11) y NO en 5° ni 7°, sin
    colisión de íconos."""
    for edad in (9, 10, 12):
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "probabilidad_sucesos" not in ids, f"no debería estar en edad {edad}"
    menu = aw._menu(aw._banda(11), 11)
    assert any(m["id"] == "probabilidad_sucesos" for m in menu), "falta probabilidad_sucesos en 6°"
    iconos = [m["icono"] for m in menu]
    assert len(iconos) == len(set(iconos)), "íconos repetidos en 6°"


def test_pubertad_6to_esi():
    """Pubertad / reproducción humana en 6° (docs/auditoria-dc-caba/grado-6.md gap #4:
    Naturales+ESI, área troncal ausente). Contenido escolar factual. Debe estar en 6°
    (edad 11) y NO en 5° ni 7°, sin colisión de íconos."""
    for edad in (9, 10, 12):
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "pubertad" not in ids, f"pubertad no debería estar en edad {edad}"
    menu = aw._menu(aw._banda(11), 11)
    assert any(m["id"] == "pubertad" for m in menu), "falta pubertad en 6°"
    iconos = [m["icono"] for m in menu]
    assert len(iconos) == len(set(iconos)), "íconos repetidos en 6°"


def test_suma_angulos_6to():
    """Suma de ángulos interiores en 6° (docs/auditoria-dc-caba/grado-6.md gap #5:
    geometría, 360°). Triángulo 180° / cuadrilátero 360° + faltante. Debe estar en 6°
    (edad 11) y NO en 5° ni 7°, sin colisión de íconos."""
    for edad in (9, 10, 12):
        ids = {m["id"] for m in aw._menu(aw._banda(edad), edad)}
        assert "suma_angulos" not in ids, f"no debería estar en edad {edad}"
    menu = aw._menu(aw._banda(11), 11)
    assert any(m["id"] == "suma_angulos" for m in menu), "falta suma_angulos en 6°"
    iconos = [m["icono"] for m in menu]
    assert len(iconos) == len(set(iconos)), "íconos repetidos en 6°"
