# -*- coding: utf-8 -*-
"""El código del duelo no se pierde al salir de la pantalla.

Pablo, 31-jul-2026: *"cuando un chico juega, ¿cómo le pasa el token al amigo? El que se
puso a jugar primero no tiene ningún número que compartir. Revisalo bien"*.

REPRODUCIDO EN EL NAVEGADOR, el circuito era éste: el chico toca "Empezar un duelo" →
contesta las 5 preguntas → **recién ahí** aparece el código → toca "Volver a las
actividades" → y el código **desaparece para siempre**. No se guardaba en ningún lado: ni
en el perfil, ni en el token, ni en una lista de "mis duelos".

Consecuencia real, y es peor que un detalle de interfaz: si el chico no compartía el código
en ese mismo instante —y un chico de nueve años cierra la pantalla— la partida quedaba
huérfana en el servidor 30 días, con sus 5 respuestas adentro, y el compañero no se enteraba
nunca de que lo habían desafiado. El duelo es de a dos: sin el código, es de a uno.

QUÉ SE ARREGLÓ: el código se guarda en el PERFIL (no en el token: el cuaderno lo pueden usar
dos hermanos y el duelo es de quien lo jugó), la pantalla de inicio lo muestra arriba de
todo con los botones de compartir, y avisa solo cuando el compañero ya jugó.
"""
import os
import re
import sys

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

DUELO = os.path.join(_BASE, "actividades_duelo.js")


def _src():
    return open(DUELO, encoding="utf-8").read()


def _cuerpo(marca, largo=3000):
    s = _src()
    i = s.index(marca)
    return s[i:i + largo]


def _funcion(nombre):
    """Sólo el cuerpo de esa función: una ventana por caracteres se desborda a la
    siguiente y hace que el test mida texto que no es el suyo."""
    s = _src()
    i = s.index("function %s(" % nombre)
    j = s.index("\n}", i)
    return s[i:j]


def test_el_codigo_se_guarda_apenas_se_crea_el_duelo():
    """EL arreglo. Si esto se cae, el código vuelve a existir sólo mientras la pantalla
    está abierta."""
    c = _cuerpo("const crear = () => {")
    assert "_dueloRecordar(j.codigo)" in c, \
        "el duelo se crea sin guardar el código: se pierde al salir"


def test_se_guarda_en_el_perfil_y_no_en_el_token():
    """El cuaderno lo pueden usar dos hermanos: el duelo es de quien lo jugó, no del
    aparato. Por eso va en el perfil activo y no en una clave suelta."""
    c = _funcion("_dueloRecordar")
    assert "Store._perfil()" in c, "el duelo dejó de guardarse por chico"
    assert "Store.save()" in c


def test_la_pantalla_de_inicio_muestra_los_duelos_que_esperan():
    """Sin esto el código está guardado pero el chico no lo ve, que para él es lo mismo que
    no tenerlo. Va ARRIBA de los dos botones: es lo único accionable de la pantalla, porque
    hay un compañero esperando del otro lado."""
    c = _cuerpo("const inicio = () => {")
    assert "_dueloMios()" in c, "la pantalla de inicio no lee los duelos guardados"
    assert "esperando a un compañero" in c
    assert "_dueloBotonCompartir" in c, "se muestra el código pero sin cómo compartirlo"
    i_pend = c.index("_dueloMios()")
    i_crear = c.index('"Empezar un duelo"')
    assert i_pend < i_crear, "los duelos pendientes quedaron debajo de los botones"


def test_avisa_cuando_el_companero_ya_jugo():
    """El chico no tiene por qué tocar cada duelo para enterarse: se consulta al abrir y el
    cartel cambia solo."""
    c = _cuerpo("const inicio = () => {")
    assert "¡Ya jugó tu compañero!" in c
    assert "Ver el resultado" in c


def test_deja_de_ofrecer_compartir_un_duelo_ya_cerrado():
    """Cuando ya jugaron los dos no hay a quién invitar; dejar el botón invitaría a un
    duelo que no se puede jugar."""
    c = _cuerpo("const inicio = () => {")
    assert "compartir.remove()" in c


def test_un_duelo_vencido_no_queda_pegado_para_siempre():
    """Las partidas viven 30 días (`duelos.VIDA_DIAS`). Si el código ya no existe, se saca
    de la lista en vez de dejarle al chico un número muerto en pantalla."""
    c = _cuerpo("const inicio = () => {")
    assert "_dueloOlvidar" in c, "un duelo vencido se queda en la lista para siempre"
    import duelos
    assert duelos.VIDA_DIAS == 30


def test_no_guarda_mas_que_un_puñado():
    """Sin tope, el perfil crece sin límite en el localStorage del chico."""
    s = _src()
    assert "DUELOS_GUARDADOS = 3" in s
    assert "slice(0, DUELOS_GUARDADOS)" in s


def test_lo_que_se_guarda_es_solo_el_codigo():
    """Las preguntas y los resultados ya están en el servidor: duplicarlos en el navegador
    sería guardar de más y arriesgar que queden desincronizados."""
    c = _funcion("_dueloRecordar")
    assert re.search(r"\{\s*c:\s*codigo,\s*ts:\s*Date\.now\(\)\s*\}", c), \
        "se está guardando algo más que el código y la fecha"
    assert "preguntas" not in c


def test_la_pantalla_del_codigo_avisa_que_no_se_pierde():
    """El chico tiene que saber que puede cerrar sin perderlo — si no, el arreglo existe
    pero él sigue creyendo que es ahora o nunca."""
    c = _cuerpo("function _dueloResultado(")
    assert "lo volvés a encontrar acá adentro" in c


def test_el_codigo_sigue_sin_ser_el_token_del_cuaderno():
    """No-regresión de seguridad: el código identifica la PARTIDA. Si llevara el token,
    compartirlo sería repartir la puerta del cuaderno de un chico."""
    import duelos
    assert duelos.CODIGO_RE.match("342M4")
    assert not duelos.CODIGO_RE.match("dueloTest4to12")
    c = _funcion("_dueloLink")
    assert '"/reto/" + codigo' in c, "el link compartible dejó de ser /reto/<codigo>"
    assert "token" not in c.lower()
