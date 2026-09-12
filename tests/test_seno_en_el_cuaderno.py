"""La clase de «Mi seño particular», ofrecida desde la tarjeta del cuaderno.

Pablo, 11-sep-2026: *"icono de seño en cada tarjeta con practicas"*. Y sobre quién puede
abrirla: *"no, siempre es con lo que le deja el adulto. Asi es por ahora"* — la puerta de la
seño no se toca, sigue pidiendo la sesión del adulto, que es la que está abierta en el teléfono
que le presta al chico.

POR QUÉ SE RESUELVE POR PEDIDO Y NO EN data.json
────────────────────────────────────────────────
`data.json` queda CONGELADO el día que se crea el token. De los 2.158 cuadernos escolares de
producción, **2.018 ni siquiera tienen `biblioteca_url`** (medido el 11-sep-2026): por esa vía,
nueve de cada diez se quedarían sin ícono hasta regenerarlos uno por uno. Acá la dirección se
arma en cada visita, con el Host del pedido, igual que la marca del título.

LO QUE ESTE ARCHIVO CUIDA
─────────────────────────
1. Que por un dominio de Kydo el cuaderno escolar ofrezca la clase.
2. Que NO la ofrezca por el otro dominio, ni en un cuaderno de cumpleaños, ni sin `base_url`
   (que es como lo llamaban los tres llamadores viejos).
3. Que no quede el marcador `{{SENO}}` sin reemplazar, que es la forma silenciosa de romperlo.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import actividades_web as aw   # noqa: E402
import seno_clases             # noqa: E402

TEMA = "safari"
KYDO = "https://mi.kydo.com.ar"
OTRO = "https://kit.casatridimensional.com.ar"
TOK_ESC = "test-seno-escolar"
TOK_CUM = "test-seno-cumple"

aw.crear({"nombre": "Sofía", "edad": "7", "escolar_on": True}, TEMA, token=TOK_ESC)
aw.crear({"nombre": "Sofía", "edad": "7"}, TEMA, token=TOK_CUM)


def _seno(token, base_url=None):
    """Lo que el player va a leer en `window.SENO`, ya parseado."""
    page = aw.html(token, base_url=base_url) if base_url else aw.html(token)
    assert page, "el visor no se pudo armar para %s" % token
    assert "{{SENO}}" not in page, "quedó el marcador sin reemplazar"
    m = re.search(r"window\.SENO = (.*?);</script>", page)
    assert m, "no está la línea de window.SENO en el visor"
    return json.loads(m.group(1))


def test_el_token_de_prueba_es_realmente_escolar():
    """Si esto fuera falso, todos los demás pasarían por el motivo equivocado: un cuaderno de
    cumpleaños nunca ofrece la clase, así que los `null` no probarían nada."""
    assert aw._es_escolar(TOK_ESC) is True
    assert aw._es_escolar(TOK_CUM) is False


def test_por_un_dominio_de_kydo_el_cuaderno_ofrece_la_clase():
    d = _seno(TOK_ESC, KYDO)
    assert d, "no ofrece ninguna clase entrando por Kydo"
    assert d["base"].endswith("/kydo/seno/" + TOK_ESC), d["base"]
    assert d["base"].startswith("https://kydo.com.ar/"), d["base"]
    assert len(d["clases"]) >= 10, "salieron muy pocas clases: %d" % len(d["clases"])


def test_las_clases_son_las_DEL_GRADO_del_cuaderno():
    """La seño sólo abre la clase del grado del cuaderno: si `tema["grado"] != grado`
    redirige al índice. Mandar la tabla entera haría que tarjetas reusadas —«La serie»,
    «Recta gigante»— apunten a la clase de 4.º desde 2.º y el chico rebote."""
    d = _seno(TOK_ESC, KYDO)
    delGrado = seno_clases.CLASES[2]          # edad 7 → 2.º
    assert set(d["clases"]) == set(delGrado), "no es el mapa del grado del cuaderno"
    for act, (tema, _tit) in delGrado.items():
        assert d["clases"][act][0] == tema


def test_por_el_otro_dominio_no_se_ofrece():
    """El mismo cuaderno servido por el dominio de Casatridimensional no puede ofrecer una
    pantalla de Kydo: es la fuga de marca que ya costó un botón mal apuntado en julio."""
    assert _seno(TOK_ESC, OTRO) is None


def test_un_cuaderno_de_CUMPLEANOS_no_ofrece_la_clase():
    """La seño es de la línea escolar. Un cuaderno de safari con clases de 2.º sería el mismo
    error que los cuadernos de cumpleaños mostrando marca de Kydo."""
    assert _seno(TOK_CUM, KYDO) is None


def test_sin_base_url_no_rompe_ni_ofrece():
    """Los tres llamadores viejos pasan el token solo. Tienen que seguir andando, y sin saber
    por qué dominio entró el pedido no se puede ofrecer nada."""
    assert _seno(TOK_ESC) is None


def test_un_icono_que_no_lleva_a_ningun_lado_no_se_dibuja():
    """`null` y no `{}`: con un objeto vacío el player tendría que decidir por su cuenta, y la
    regla es que si no hay clase no hay ícono. Un ícono muerto es peor que ninguno."""
    page = aw.html(TOK_CUM, base_url=KYDO)
    assert "window.SENO = null;" in page


# ── lo que dibuja el player ──────────────────────────────────────────────────────
with open(os.path.join(BASE, "actividades_player.js"), encoding="utf-8") as _f:
    PLAYER = _f.read()


def test_el_icono_solo_se_dibuja_si_la_tarjeta_TIENE_clase():
    """156 de 560 tarjetas tienen clase. Dibujarlo en todas sería mandar a la mayoría a un
    índice que no habla de lo que estaban haciendo."""
    assert "const _seno = _senoDeLaTarjeta(m.id)" in PLAYER
    assert '${_seno ? `<span class="seno-ir"' in PLAYER, (
        "el ícono no está condicionado a que la tarjeta tenga clase")


def test_el_icono_abre_la_clase_y_NO_el_juego():
    """El 🎓 vive adentro del <button> de la tarjeta: sin frenar el evento, tocarlo abriría el
    juego. Es el mismo cuidado que ya tiene la corneta."""
    i = PLAYER.index('closest(".seno-ir")')
    bloque = PLAYER[i:i + 500]
    assert "ev.preventDefault(); ev.stopPropagation();" in bloque, "el toque se filtra al juego"
    assert 'window.open(_seno.url, "_blank", "noopener")' in bloque, (
        "no abre la clase en otra pestaña")


def test_la_direccion_la_pone_el_SERVIDOR_y_no_el_player():
    """El sitio de Kydo no puede estar escrito en el JS: el player es el MISMO archivo para las
    dos marcas, y la marca la decide el Host de cada pedido. El player sólo lee lo que le
    dejaron en `window.SENO`."""
    i = PLAYER.index("function _senoDeLaTarjeta")
    cuerpo = PLAYER[i:PLAYER.index("\nfunction ", i + 1)]
    assert "window.SENO" in cuerpo, "el player no lee lo que le manda el servidor"
    assert "kydo.com.ar" not in cuerpo, "el player está armando la URL de Kydo por su cuenta"


def test_el_estilo_del_icono_viaja_con_el_menu():
    """Los estilos del menú se inyectan desde el JS: uno que quede afuera se ve roto sólo en
    producción. La función entera, no los primeros N bytes."""
    i = PLAYER.index("function _adaptCSS")
    css = PLAYER[i:PLAYER.index("\nfunction ", i + 1)]
    assert ".carta .seno-ir{" in css, "falta el estilo del ícono de la seño"
