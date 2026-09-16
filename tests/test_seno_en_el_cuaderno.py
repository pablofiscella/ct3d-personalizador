"""La clase de «Mi seño particular», ofrecida desde la tarjeta del cuaderno.

Pablo, 11-sep-2026: *"icono de seño en cada tarjeta con practicas"*. Y sobre quién puede
abrirla: *"no, siempre es con lo que le deja el adulto. Asi es por ahora"* — la puerta de la
seño no se toca, sigue pidiendo la sesión del adulto, que es la que está abierta en el teléfono
que le presta al chico.

POR QUÉ SE RESUELVE POR PEDIDO Y NO EN data.json
────────────────────────────────────────────────
`data.json` queda CONGELADO el día que se crea el token. De los 2.158 cuadernos escolares de
producción, **2.018 ni siquiera tienen `biblioteca_url`** (medido el 11-sep-2026): por esa vía,
nueve de cada diez se quedarían sin ícono hasta regenerarlos uno por uno. Acá se arma en cada
visita, junto con la marca del título.

LA COMPUERTA ES `escolar_on`, NO EL DOMINIO (corregido el 12-sep-2026)
─────────────────────────────────────────────────────────────────────
La primera versión pedía además que el pedido entrara por un host de Kydo. Eso NO PASA NUNCA:
el motor se sirve por `kit.casatridimensional.com.ar` en producción y por `devkit…` en el
espejo, así que el ícono no se habría visto jamás. Y los tests lo daban por bueno porque
inventaban un `X-Forwarded-Host` que en la realidad no existe.

LO QUE ESTE ARCHIVO CUIDA
─────────────────────────
1. Que un cuaderno escolar ofrezca la clase **llamado pelado**, como lo llama el servicio.
2. Que NO la ofrezca un cuaderno de cumpleaños.
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
TOK_ESC = "test-seno-escolar"
TOK_CUM = "test-seno-cumple"

aw.crear({"nombre": "Sofía", "edad": "7", "escolar_on": True}, TEMA, token=TOK_ESC)
aw.crear({"nombre": "Sofía", "edad": "7"}, TEMA, token=TOK_CUM)


def _seno(token):
    """Lo que el player va a leer en `window.SENO`, ya parseado."""
    page = aw.html(token)
    assert page, "el visor no se pudo armar para %s" % token
    assert "{{SENO}}" not in page, "quedó el marcador sin reemplazar"
    m = re.search(r"window\.SENO = (.*?);</script>", page)
    assert m, "no está la línea de window.SENO en el visor"
    return json.loads(m.group(1))


def test_el_token_de_prueba_es_realmente_escolar():
    """Si esto fuera falso, los demás pasarían por el motivo equivocado: un cuaderno de
    cumpleaños nunca ofrece la clase, así que los `null` no probarían nada."""
    assert aw._es_escolar(TOK_ESC) is True
    assert aw._es_escolar(TOK_CUM) is False


def test_el_cuaderno_escolar_ofrece_la_clase_SIN_NINGUNA_CABECERA(monkeypatch):
    """EL TEST QUE FALTABA, y su ausencia dejó la función muerta en producción (12-sep-2026).

    La primera versión exigía además que el pedido entrara por un dominio de Kydo. Eso **no pasa
    nunca**: el motor se sirve por `kit.casatridimensional.com.ar` en producción y por `devkit…`
    en el espejo. El ícono no se habría visto jamás — y la prueba que lo daba por bueno forzaba
    un `X-Forwarded-Host` inventado, o sea que verificaba una situación que no existe.

    Por eso acá se llama a `html(token)` PELADO, como lo llama el servicio de verdad. (En el
    espejo, que es donde está prendida: en producción queda apagada, ver más abajo.)"""
    monkeypatch.setenv("CT3D_ENTORNO", "dev")
    d = _seno(TOK_ESC)
    assert d, "un cuaderno escolar servido normalmente no ofrece la clase"
    assert d["base"].endswith("/kydo/seno/" + TOK_ESC), d["base"]
    assert "/kydo/seno/" in d["base"], d["base"]   # el host, en los dos tests de acá abajo
    assert len(d["clases"]) >= 10, "salieron muy pocas clases: %d" % len(d["clases"])


def test_en_el_ESPEJO_la_clase_apunta_al_Kydo_del_ESPEJO(monkeypatch):
    """Una página del espejo no puede sacar a nadie a producción.

    El sitio estaba clavado a `kydo.com.ar`, así que el cuaderno del dev mandaba al VIVO — donde
    además la seño está apagada, o sea que el chico caía en la biblioteca. Lo encontró Pablo
    probándolo el 12-sep-2026: *"me lleva a la biblioteca"*."""
    monkeypatch.setenv("CT3D_ENTORNO", "dev")
    assert _seno(TOK_ESC)["base"].startswith("https://dev.kydo.com.ar/kydo/seno/")


def test_en_PRODUCCION_apunta_al_Kydo_de_verdad(monkeypatch):
    """La otra mitad: sin la variable de entorno, el sitio es el vivo. Un test que sólo mirara
    el caso dev dejaría pasar que producción apunte al espejo, que es peor."""
    monkeypatch.delenv("CT3D_ENTORNO", raising=False)
    monkeypatch.setenv("CT3D_SENO_EN_CUADERNO", "1")        # prendida a propósito
    assert _seno(TOK_ESC)["base"].startswith("https://kydo.com.ar/kydo/seno/")


def test_en_PRODUCCION_queda_APAGADA_hasta_que_Pablo_diga(monkeypatch):
    """Pablo, 13-sep-2026: *"siguen apagados en producción hasta que te diga"*.

    Sin la variable y fuera del espejo, NO se ofrece la clase: si se subiera la rama del menú,
    el 🎓 no aparecería en ningún cuaderno de producción. Es el caso que protege este test —y
    el que antes pasaba por encima de la seño apagada—."""
    monkeypatch.delenv("CT3D_ENTORNO", raising=False)
    monkeypatch.delenv("CT3D_SENO_EN_CUADERNO", raising=False)
    assert _seno(TOK_ESC) is None, "en producción el 🎓 aparece sin que nadie lo haya prendido"


def test_las_clases_son_las_DEL_GRADO_del_cuaderno(monkeypatch):
    """La seño sólo abre la clase del grado del cuaderno: si `tema["grado"] != grado` redirige
    al índice. Mandar la tabla entera haría que tarjetas reusadas —«La serie», «Recta gigante»—
    apunten a la clase de 4.º desde 2.º y el chico rebote."""
    monkeypatch.setenv("CT3D_ENTORNO", "dev")
    d = _seno(TOK_ESC)
    delGrado = seno_clases.CLASES[2]          # edad 7 → 2.º
    assert set(d["clases"]) == set(delGrado), "no es el mapa del grado del cuaderno"
    for act, (tema, _tit) in delGrado.items():
        assert d["clases"][act][0] == tema


def test_un_cuaderno_de_CUMPLEANOS_no_ofrece_la_clase():
    """La seño es de la línea escolar, y `escolar_on` es lo que separa las dos marcas en todo
    el visor: el título, el favicon y ahora esto. Un cuaderno de safari con clases de 2.º sería
    la misma fuga que los cuadernos de cumpleaños mostrando marca de Kydo."""
    assert _seno(TOK_CUM) is None


def test_un_icono_que_no_lleva_a_ningun_lado_no_se_dibuja():
    """`null` y no `{}`: con un objeto vacío el player tendría que decidir por su cuenta, y la
    regla es que si no hay clase no hay ícono. Un ícono muerto es peor que ninguno."""
    assert "window.SENO = null;" in aw.html(TOK_CUM)


# ── lo que dibuja el player ──────────────────────────────────────────────────────
with open(os.path.join(BASE, "actividades_player.js"), encoding="utf-8") as _f:
    PLAYER = _f.read()


def test_el_icono_solo_se_dibuja_si_la_tarjeta_TIENE_clase():
    """176 de 560 tarjetas tienen clase. Dibujarlo en todas sería mandar a la mayoría a un
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
    dos marcas, y la que manda es `escolar_on` del cuaderno. El player sólo lee lo que le
    dejaron en `window.SENO`."""
    i = PLAYER.index("function _senoDeLaTarjeta")
    cuerpo = PLAYER[i:PLAYER.index("\nfunction ", i + 1)]
    assert "window.SENO" in cuerpo, "el player no lee lo que le manda el servidor"
    assert "kydo.com.ar" not in cuerpo, "el player está armando la URL de Kydo por su cuenta"


def test_la_clase_sabe_que_se_abrio_DESDE_EL_CUADERNO():
    """Pablo, 12-sep-2026: *"pongo abrir cuaderno me lleva a la lista de cuadernos. Debería
    volver atrás de dónde vine"*. La lección se abre en otra pestaña y su botón iba a `/jugar/`,
    que pasa por la biblioteca. Para poder devolverlo al cuaderno —cerrando esa pestaña— la
    lección tiene que saber de dónde vino, y eso sólo lo sabe el motor."""
    i = PLAYER.index("function _senoDeLaTarjeta")
    cuerpo = PLAYER[i:PLAYER.index("\nfunction ", i + 1)]
    assert '"?desde=cuaderno"' in cuerpo, "la clase no sabe que se abrió desde el cuaderno"


def test_el_estilo_del_icono_viaja_con_el_menu():
    """Los estilos del menú se inyectan desde el JS: uno que quede afuera se ve roto sólo en
    producción. La función entera, no los primeros N bytes."""
    i = PLAYER.index("function _adaptCSS")
    css = PLAYER[i:PLAYER.index("\nfunction ", i + 1)]
    assert ".carta .seno-ir{" in css, "falta el estilo del ícono de la seño"
