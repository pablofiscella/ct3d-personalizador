# -*- coding: utf-8 -*-
"""El reloj de las actividades contrarreloj se frena cuando hay una lección encima.

Pablo, 03-ago-2026, jugando "Núcleo del sujeto" de 5.º: *"estaba viendo el video y por
atrás la práctica seguía sin poder contestar. O sea no sólo tapa la voz al video sino que
le queda como que no respondió nada"*. Y: *"revisá todos los que tengan respuesta por
tiempo porque les pasa lo mismo"*.

Son DOS: `tablas_contrarreloj` (2.º) y el de núcleo del sujeto (5.º). Las dos medían el
tiempo con `Date.now()` contra un `inicio` fijo, y su único guard era
`barraWrap.isConnected` — que sigue en `true` cuando se abre una lección ENCIMA: el juego
no se fue del DOM, quedó atrás. El reloj corría igual, se acababa, marcaba la pregunta
como no contestada y cantaba la siguiente por arriba del video.

Peor con `ofrecerLeccion`, que se abre SOLA en medio de la actividad ("vi que te está
costando"): el chico ni la pidió y pierde la ronda por mirarla.

Lo que se fija acá:
  1. `juegoTapado()` detecta la lección abierta y la pestaña en segundo plano.
  2. Las DOS contrarreloj acumulan tiempo JUGADO, no tiempo de reloj — y ninguna quedó
     con el patrón viejo. Es lo que atrapa a la tercera que alguien agregue mañana.
  3. La actividad no habla encima de una lección abierta.
"""
import json
import os
import shutil
import subprocess
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

PLAYER = os.path.join(_BASE, "actividades_player.js")

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")


def _correr(js_extra, tapado=False, oculto=False):
    """Evalúa la función REAL del player con un DOM de juguete.

    La función se saca del archivo con una regex y no se copia acá: una copia se
    desincroniza al primer cambio y el test pasa a medir algo que ya no existe."""
    arnes = r"""
const fs = require("fs");
const src = fs.readFileSync(%s, "utf8");
const TAPADO = %s, OCULTO = %s;
global.document = {
  hidden: OCULTO,
  querySelector: (sel) => (sel === ".comoes-fondo" && TAPADO ? {} : null),
};
eval([/function juegoTapado\(\)[\s\S]*?\n\}/]
  .map((re) => { const m = src.match(re); if (!m) throw new Error("no se encontró " + re); return m[0]; })
  .join("\n"));
%s
""" % (json.dumps(PLAYER), "true" if tapado else "false",
       "true" if oculto else "false", js_extra)
    r = subprocess.run(["node", "-e", arnes], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[:800]
    return r.stdout.strip()


# ── 1. Detectar que el juego está tapado ────────────────────────────────────────────────

def test_con_una_leccion_abierta_el_juego_esta_tapado():
    assert _correr("process.stdout.write(String(juegoTapado()))", tapado=True) == "true"


def test_sin_nada_encima_el_juego_NO_esta_tapado():
    """El control: si diera `true` siempre, el reloj no correría nunca y la actividad
    contrarreloj dejaría de ser contrarreloj."""
    assert _correr("process.stdout.write(String(juegoTapado()))") == "false"


def test_con_la_pestana_en_segundo_plano_tambien():
    """Mismo problema, otra causa: el chico cambia de pestaña o le entra una llamada."""
    assert _correr("process.stdout.write(String(juegoTapado()))", oculto=True) == "true"


# ── 2. Las dos contrarreloj acumulan tiempo JUGADO ──────────────────────────────────────

def _bloques_setinterval():
    src = open(PLAYER, encoding="utf-8").read()
    bloques, i = [], 0
    while True:
        i = src.find("intervalId = setInterval(", i)
        if i < 0:
            break
        fin = src.find("}, 100);", i)
        bloques.append(src[i:fin])
        i = fin
    return bloques


def test_las_dos_contrarreloj_frenan_el_reloj():
    """Se recorren TODOS los `setInterval` del player: si mañana aparece una tercera
    actividad por tiempo con el patrón viejo, este test la caza. Es exactamente lo que
    pidió Pablo — *"revisá todos los que tengan respuesta por tiempo"*."""
    bloques = _bloques_setinterval()
    assert len(bloques) == 2, \
        "el player tiene %d actividades por tiempo, se esperaban 2" % len(bloques)
    for n, b in enumerate(bloques, 1):
        assert "juegoTapado()" in b, \
            "la actividad por tiempo #%d no frena el reloj con una lección encima" % n
        assert "jugado / TIEMPO_MS" in b, \
            "la #%d sigue midiendo contra el reloj de pared y no el tiempo jugado" % n


def test_ninguna_mide_contra_un_inicio_fijo():
    """El patrón viejo, escrito tal cual estaba. Si vuelve, vuelve el bug."""
    for n, b in enumerate(_bloques_setinterval(), 1):
        assert "Date.now() - inicio" not in b, \
            "la actividad por tiempo #%d volvió al reloj de pared" % n


def test_el_reloj_no_avanza_mientras_esta_tapado():
    """La aritmética de la pausa, con la MISMA forma que quedó en el player."""
    js = """
let jugado = 0, ultimo = 1000;
function tick(ahora) { if (!juegoTapado()) jugado += ahora - ultimo; ultimo = ahora; }
tick(1500); tick(2000);
process.stdout.write(String(jugado));
"""
    assert _correr(js, tapado=True) == "0", "el reloj corrió con la lección abierta"
    assert _correr(js) == "1000", "el reloj no corre cuando debería"


# ── 3. La voz no se superpone al video ──────────────────────────────────────────────────

def test_no_habla_encima_de_una_leccion_abierta():
    """`mostrarComoEs` ya llamaba a `pararVoz()`, pero eso corta lo que YA sonaba: no
    impide que el juego de atrás arranque una consigna nueva un segundo después. Pablo:
    *"tapa la voz al video"*. Se corta en el origen."""
    src = open(PLAYER, encoding="utf-8").read()
    i = src.index("function reproducirConsigna(")
    # hasta el `new Audio(`: es donde se decide si suena. Una ventana fija de N caracteres
    # se queda corta o larga en cuanto el comentario de arriba cambia de tamaño.
    cuerpo = src[i:src.index("new Audio(", i) + 40]
    assert "juegoTapado()" in cuerpo, "la actividad puede hablar encima de la lección"
    # y antes de crear el Audio: cortar después no evitaría la superposición
    assert cuerpo.index("juegoTapado()") < cuerpo.index("new Audio("), \
        "el corte quedó DESPUÉS de arrancar el audio"


# ── 4. La voz muere con la pantalla que la pidió ────────────────────────────────────────
# Pablo, 03-ago-2026: *"salís de la actividad y sigue el audio de la tarjeta de donde
# venías"*. El audio es un objeto suelto: vaciar el `#stage` se lleva el DOM pero no lo
# que está sonando, así que la consigna anterior seguía hablando encima de la pantalla
# nueva. `pararVoz()` existía y no lo llamaba nadie al navegar.

_DESTINOS = [
    ("Shell.abrir", "abrir una actividad"),
    ("function pintarNivel(", "la pantalla de nivel"),
    ("function pintarMenuPlano(", "el menú de actividades"),
]


def _cuerpo_desde(marca, largo=1400):
    """El cuerpo desde la marca. `largo` generoso a propósito: estas funciones llevan
    comentarios arriba y una ventana justa se rompe con el próximo párrafo que se agregue
    — ya pasó con test_voz_deletrea_rioplatense el mismo día."""
    src = open(PLAYER, encoding="utf-8").read()
    i = src.index("  abrir(id) {" if marca == "Shell.abrir" else marca)
    return src[i:i + largo]


@pytest.mark.parametrize("marca,nombre", _DESTINOS)
def test_al_cambiar_de_pantalla_se_corta_la_voz(marca, nombre):
    """Los TRES destinos: cualquier camino del player termina en uno de estos. Si mañana
    aparece un cuarto, este test no lo sabe — pero el comentario de `Shell.abrir` dice
    dónde mirar, y los tres de acá tienen que seguir cortando."""
    assert "pararVoz()" in _cuerpo_desde(marca), \
        "al ir a %s no se corta la voz de la pantalla anterior" % nombre


def test_se_corta_ANTES_de_pintar_lo_nuevo():
    """Si se cortara después de armar la pantalla, la consigna nueva podría arrancar
    primero y la vieja la pisaría al cortarse — el mismo ruido, más difícil de ver."""
    cuerpo = _cuerpo_desde("Shell.abrir")
    assert cuerpo.index("pararVoz()") < cuerpo.index('stage.innerHTML = ""'), \
        "la voz se corta después de haber empezado a pintar"
