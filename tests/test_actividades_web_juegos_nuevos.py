"""4 juegos nuevos del cuaderno interactivo (jul-2026): Escuchá y repetí (simon),
¿Dónde va? (agrupar), ¿Qué falta? (quefalta), Bingo de amigos (bingo). Reusan
personajes/paleta ya existentes — sin arte nuevo. Verificado con Playwright real
(sin errores JS, DOM correcto) antes de mergear; acá solo el contrato de _menu."""
import actividades_web as aw

NUEVOS = {"simon", "agrupar", "quefalta", "bingo"}


def test_los_4_juegos_estan_en_las_3_bandas():
    for banda, edad in (("mini", "2"), ("media", "5"), ("grande", "7")):
        ids = {m["id"] for m in aw._menu(banda, edad)}
        faltan = NUEVOS - ids
        assert not faltan, f"banda {banda}: faltan {faltan}"


def test_cfg_de_cada_juego_nuevo_tiene_las_claves_esperadas():
    menu = {m["id"]: m for m in aw._menu("grande", "7")}
    assert "colores" in menu["simon"]["cfg"] and "rondas" in menu["simon"]["cfg"]
    assert "canastas" in menu["agrupar"]["cfg"] and "rondas" in menu["agrupar"]["cfg"]
    assert "items" in menu["quefalta"]["cfg"] and "rondas" in menu["quefalta"]["cfg"]
    assert "tam" in menu["bingo"]["cfg"]


def test_dificultad_progresiva_por_banda():
    """Más colores/canastas/items/celdas cuanto más grande la banda (mini < media < grande)."""
    mini = {m["id"]: m["cfg"] for m in aw._menu("mini", "2")}
    media = {m["id"]: m["cfg"] for m in aw._menu("media", "5")}
    grande = {m["id"]: m["cfg"] for m in aw._menu("grande", "7")}
    assert mini["simon"]["colores"] <= media["simon"]["colores"] <= grande["simon"]["colores"]
    assert mini["bingo"]["tam"] <= media["bingo"]["tam"] <= grande["bingo"]["tam"]
