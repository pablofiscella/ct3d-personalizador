"""La muestra pública que enlaza la landing de Kydo.

Dos cosas que si se rompen no se notan hasta que un cliente se queja:

1. `?muestra=<id>` es lo único que abre un juego directo. Si el parser deja de matchear,
   el botón "Probalo ahora" de la landing pasa a caer en "¿Quién juega?" — o sea, un
   formulario delante del producto, que es exactamente lo que vinimos a sacar.

2. El parser tiene que devolver null cuando NO corresponde. Un falso positivo saltearía
   la pantalla de perfil en cuadernos VENDIDOS, y ahí el chico pierde su progreso porque
   juega como "Invitado".
"""
import os
import re
import subprocess
import sys

import pytest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER = os.path.join(BASE, "actividades_player.js")
SCRIPT = os.path.join(BASE, "infra", "crear-muestra-publica.py")


def _fuente_player():
    with open(PLAYER, encoding="utf-8") as f:
        return f.read()


def test_el_player_define_el_parser_y_el_nombre_invitado():
    src = _fuente_player()
    assert "function muestraPedida()" in src
    assert "NOMBRE_INVITADO" in src


def _correr_parser(search, juegos=("angulos",)):
    """Evalúa muestraPedida() aislada, con `location` y `GAMES` inyectados."""
    src = _fuente_player()
    m = re.search(r"function muestraPedida\(\)[\s\S]*?\n\}", src)
    assert m, "no se encontró muestraPedida() en el player"
    js = """
      const GAMES = %s;
      const location = { search: %s };
      const f = %s;
      process.stdout.write(String(f()));
    """ % (
        "{" + ",".join('"%s":1' % j for j in juegos) + "}",
        '"%s"' % search,
        m.group(0).replace("function muestraPedida()", "function ()", 1),
    )
    out = subprocess.run([_node(), "-e", js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    return out.stdout.strip()


def _node():
    from shutil import which
    n = which("node")
    if not n:
        pytest.skip("node no disponible")
    return n


@pytest.mark.parametrize("search", ["", "?g=abc", "?muestra=", "?muestra=noexiste"])
def test_sin_muestra_valida_devuelve_null(search):
    # Éste es el caso que protege a los cuadernos vendidos: arranque normal, con perfil.
    assert _correr_parser(search) == "null"


@pytest.mark.parametrize("search", ["?muestra=angulos", "?muestra=angulos&x=1",
                                    "?x=1&muestra=angulos"])
def test_con_muestra_valida_devuelve_el_juego(search):
    assert _correr_parser(search) == "angulos"


def test_el_arranque_abre_la_muestra_despues_de_elegir_perfil():
    # El orden importa: elegirPerfil() termina pintando el menú (o el sondeo), así que
    # Shell.abrir tiene que ir DESPUÉS o la muestra queda tapada.
    src = _fuente_player()
    i_perfil = src.index("elegirPerfil(NOMBRE_INVITADO)")
    i_abrir = src.index("Shell.abrir(_muestra)")
    assert i_perfil < i_abrir


def test_el_script_de_la_muestra_lista_los_cuatro_links():
    out = subprocess.run([sys.executable, SCRIPT, "--listar"],
                         capture_output=True, text=True, timeout=60)
    assert out.returncode == 0, out.stderr
    # una por materia + el menú completo
    assert out.stdout.count("http") == 5
    for juego in ("angulos", "abstractos_concretos", "laboratorio_electrico",
                  "provincias_region"):
        assert "muestra=" + juego in out.stdout


def test_las_cuatro_muestras_existen_en_cuarto_grado():
    # Si un juego se saca del grado, el link abre el menú en vez de la muestra y en la
    # landing se lee como "el botón no anda". Que falle acá y no en producción.
    sys.path.insert(0, BASE)
    import actividades_web as aw
    disponibles = {it["id"] for it in aw.catalogo_actividades().get(4, [])}
    for juego in ("angulos", "abstractos_concretos", "laboratorio_electrico",
                  "provincias_region"):
        assert juego in disponibles, "%s ya no está en 4.º grado" % juego


def test_las_cuatro_muestras_tienen_leccion_en_video():
    # El argumento de venta de la landing es "son interactivas Y explican". Una muestra
    # sin el botón "¿Cómo es?" no prueba la segunda mitad.
    lec = os.path.join(BASE, "lecciones_video")
    for juego in ("angulos", "abstractos_concretos", "laboratorio_electrico",
                  "provincias_region"):
        assert os.path.exists(os.path.join(lec, "lec_%s.mp4" % juego)), juego


# ─────────────────── la muestra no es una puerta al grado ───────────────────
# Pablo, 26-jul-2026: "cuando entras a probar una actividad y pones atrás tenés acceso a
# todas las actividades de cuarto grado. Creo que desde la página no debería poder ir para
# atrás". El token de la muestra es PÚBLICO: el ← regalaba los 39 juegos de 4.º a cualquiera
# que llegara de la landing.

def test_la_muestra_cierra_las_salidas_al_menu():
    src = _fuente_player()
    assert "function cerrarSalidasDeMuestra" in src
    # las tres salidas: el ←, el 📚 de la biblioteca y el nombre (abre el selector de perfil)
    i = src.index("function cerrarSalidasDeMuestra")
    bloque = src[i:i + 700]
    for id_ in ("btnAtras", "btnBiblioteca", "hdrTitulo"):
        assert id_ in bloque, "la muestra no esconde %s" % id_


def test_pintar_menu_es_el_punto_unico_de_corte():
    """Cerrar botones no alcanza: basta UN camino olvidado (terminar la ronda, "¡Seguir
    jugando!", cerrar el panel de grandes, el diploma) para destapar el grado completo.
    El corte va en pintarMenu, por donde pasan todos."""
    src = _fuente_player()
    i = src.index("function pintarMenu()")
    cuerpo = src[i:i + 600]
    assert "MUESTRA_SOLA" in cuerpo, "pintarMenu no corta en modo muestra"
    assert cuerpo.index("MUESTRA_SOLA") < cuerpo.index("pintarMenuPlano"), \
        "el corte tiene que ir ANTES de pintar el menú"


def test_volver_menu_reabre_la_misma_actividad():
    src = _fuente_player()
    i = src.index("function volverMenu()")
    cuerpo = src[i:i + 500]
    assert "MUESTRA_SOLA" in cuerpo and "Shell.abrir(MUESTRA_SOLA)" in cuerpo


def test_las_salidas_se_cierran_ANTES_de_abrir_el_juego():
    """Si se abre primero, el juego pinta el ← y queda visible un instante — y en un celular
    ese instante alcanza para tocarlo."""
    src = _fuente_player()
    assert src.index("cerrarSalidasDeMuestra(_muestra)") < src.index("Shell.abrir(_muestra)")


def test_un_cuaderno_normal_conserva_el_boton_atras():
    """LA regresión que importa: MUESTRA_SOLA arranca en null, así que un cuaderno comprado
    no cambia en nada."""
    src = _fuente_player()
    assert "let MUESTRA_SOLA = null" in src
