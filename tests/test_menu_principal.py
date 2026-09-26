"""La pantalla principal de actividades: una sola recomendada, repasos tocables y racha.

Pablo, 11-sep-2026, mirando el menú de 4.º: *"quiero ver todo lo que podés agregar para la
pantalla principal de actividades"*. Lo medido ese día sobre el menú real: con un perfil nuevo
el motor marcaba **las 73 tarjetas** con «✨ Recomendado» —una etiqueta que llevan todas no
recomienda nada— y lo que había para repasar era un cartel de texto que no se podía tocar.

Acá se cuida:
1. La racha de días, con node y sin navegador (es una función pura a propósito).
2. Que la etiqueta de recomendada quede atada a UNA sola tarjeta.
3. Que los repasos se dibujen como tarjetas y el progreso por materia esté en su título.
"""
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
PLAYER = os.path.join(BASE, "actividades_player.js")

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")


def _fuente():
    with open(PLAYER, encoding="utf-8") as f:
        return f.read()


def _racha(dias, hoy):
    """Corre `_rachaDeDias` del player con node, recortada del archivo que se sirve."""
    js = """
      const fs = require('fs');
      const src = fs.readFileSync('actividades_player.js', 'utf8');
      const i = src.indexOf('function _rachaDeDias');
      const j = src.indexOf('\\nconst Store = {', i);
      eval(src.slice(i, j));
      console.log(JSON.stringify(_rachaDeDias(%s, %s)));
    """ % (json.dumps(dias), json.dumps(hoy))
    r = subprocess.run(["node", "-e", js], cwd=BASE, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout.strip())


def test_sin_dias_no_hay_racha():
    assert _racha([], "2026-09-11") == 0


def test_un_dia_es_racha_de_uno():
    assert _racha(["2026-09-11"], "2026-09-11") == 1


def test_dias_seguidos_se_suman():
    assert _racha(["2026-09-09", "2026-09-10", "2026-09-11"], "2026-09-11") == 3


def test_todavia_no_jugo_hoy_pero_la_racha_sigue():
    """La racha se pierde cuando se saltea un día ENTERO, no por no haber entrado todavía:
    si se cortara a la mañana, el chico abriría el cuaderno y vería que perdió algo sin
    haber hecho nada."""
    assert _racha(["2026-09-09", "2026-09-10"], "2026-09-11") == 2


def test_un_dia_salteado_corta_la_racha():
    assert _racha(["2026-09-05", "2026-09-09", "2026-09-10", "2026-09-11"], "2026-09-11") == 3


def test_el_orden_en_que_se_guardaron_no_importa():
    assert _racha(["2026-09-11", "2026-09-09", "2026-09-10"], "2026-09-11") == 3


def test_una_fecha_rota_no_rompe_el_menu():
    assert _racha(["2026-09-11"], "ayer") == 0


# ── lo que se dibuja en el menú ─────────────────────────────────────────────────────
def test_la_recomendada_es_una_sola():
    """EL motivo del cambio: la etiqueta sólo se pone si la tarjeta ES la elegida."""
    s = _fuente()
    i = s.index("const hacerCarta")
    cuerpo = s[i:s.index("_marcarCiclo();", i)]
    m = re.search(r'if \(adaptOn && \(([^)]*\)[^)]*)\)\) \{\s*\n\s*const etq = Adapt\.etiqueta', cuerpo)
    assert m, "cambió la condición de la etiqueta: revisar este test"
    cond = m.group(1)
    assert "_idSeguir" in cond, "«Recomendado» volvió a marcar todas las tarjetas"
    assert "reforzar" in cond, "se perdió «🌱 Reforzá antes», que sí es de pocas"


def test_la_elegida_sale_del_motor():
    """Desde el 25-sep-2026 (auditoría PRO-03) la elegida es la primera de la MISIÓN DE HOY que
    falta hacer, y la misión la arma el motor (`_elegirMision`: repasos, para sellar y el
    orden de `Adapt.peso`). Con la misión cumplida vuelve a `Adapt.proximaRecomendada`. Lo que
    este test sigue cuidando es lo mismo: que no aparezca una regla ajena al motor."""
    s = _fuente()
    assert "_idParaSeguir(visibles.map((m) => m.id))" in s, (
        "la tarjeta de «Seguí por acá» tiene que salir de la misión del motor")
    i = s.index("function _idParaSeguir(")
    assert "Adapt.proximaRecomendada(ids)" in s[i:s.index("\n}\n", i)], (
        "con la misión cumplida, «Seguí por acá» tiene que volver a la recomendada del motor")
    j = s.index("function _elegirMision(")
    assert "Adapt.peso(" in s[j:s.index("\n}\n", j)], "la misión dejó de usar el orden del motor"


def test_seguir_por_aca_abre_la_actividad():
    s = _fuente()
    i = s.index('el("button", "seguir-aca")')
    bloque = s[i:i + 1200]
    assert "Shell.abrir(_itSeguir.id)" in bloque, "la tarjeta de arriba no abre nada"
    assert "aria-label" in bloque, "sin rótulo no la lee un lector de pantalla"


def test_los_repasos_son_tarjetas_tocables():
    s = _fuente()
    assert "cat-titulo cat-repaso" in s and "repasos.forEach((m, i) => gRep.appendChild(hacerCarta(m, i)))" in s, (
        "los repasos volvieron a ser un cartel de texto")
    assert "if (repasos.length && !adaptOn)" in s, (
        "sin motor adaptativo el cartel de siempre tiene que seguir estando")


def test_cada_materia_muestra_cuanto_lleva():
    s = _fuente()
    assert 'class="cat-prog"' in s and 'Store.sello(m.id) !== "practicando"' in s, (
        "se perdió el progreso por materia en el título de la sección")


def test_la_racha_se_anota_al_ganar():
    s = _fuente()
    i = s.index("Store.setStars(self.actual, e);")
    assert "Store.marcarDia()" in s[i:i + 300], "ganar una partida ya no cuenta para la racha"


def test_la_racha_aparece_desde_el_primer_dia_ganado():
    """Hasta el 25-sep-2026 aparecía desde el día 2 («un 🔥 1 el primer día promete una racha
    que todavía no existe»). La auditoría (PRO-03) mostró el costo: ningún chico real llegó
    al día 2, así que la racha no la vio nadie. Ahora se ve apenas gana la primera partida
    —`rachaDias` cuenta días con partida GANADA—, como «🔥 1»; antes de jugar sigue sin
    aparecer, así que no promete nada que no pasó."""
    s = _fuente()
    i = s.index('_rp = document.getElementById("hdrRacha")')
    assert re.search(r"if \(_racha >= 1\)", s[i - 200:i + 400]), "la racha volvió a esconderse el día 1"
    assert '"Día " + _racha' in s[i:i + 900], "el rótulo tiene que decir qué día de la racha es"


def test_en_primero_la_tarjeta_nueva_va_en_mayuscula():
    """1.º se ve en imprenta MAYÚSCULA (decisión de Pablo, 15-ago-2026). Si «Seguí por acá»
    quedara afuera, la tarjeta más grande del menú sería la única en minúscula: dos alfabetos
    en la misma pantalla, que es lo que esa regla vino a sacar."""
    with open(os.path.join(BASE, "actividades_player.html"), encoding="utf-8") as f:
        html = f.read()
    for sel in ("body.g1 .seguir-aca b", "body.g1 .seguir-aca small", "body.g1 .seguir-aca span"):
        assert sel in html, "falta %s en la regla de mayúsculas de 1.º" % sel


def test_los_estilos_nuevos_viajan_con_el_menu():
    """Los estilos del menú adaptativo se inyectan desde el JS: si uno queda afuera, la
    pieza se ve rota sólo en producción."""
    s = _fuente()
    i = s.index("function _adaptCSS")
    css = s[i:s.index("\nfunction ", i + 1)]      # la función entera, no los primeros N bytes
    for sel in (".seguir-aca{", ".cat-titulo small{", ".cat-titulo.cat-repaso{",
                ".filtro-estados{", ".filtro-arriba{", ".chip-est{"):
        assert sel in css, "falta el estilo de %s" % sel


# ── el buscador y los filtros (4.º para arriba) ─────────────────────────────────────
def test_el_buscador_es_de_cuarto_para_arriba():
    """En 1.º-3.º el menú se deja como está: son menos tarjetas y un chico que recién
    aprende a leer no busca escribiendo."""
    s = _fuente()
    i = s.index('barra.id = "filtroMenu"')
    assert "gradoDelChico() >= 4" in s[i - 900:i], "el buscador aparecería también en 1.º"
    assert "visibles.length >= 20" in s[i - 900:i], "con 15 tarjetas buscar es más trabajo que mirar"


def test_buscar_no_vuelve_a_pintar_el_menu():
    """Re-pintar con cada letra pierde el scroll y re-arma 73 tarjetas."""
    s = _fuente()
    i = s.index("function _filtrarMenu")
    cuerpo = s[i:s.index("\nfunction pintarMenuPlano", i)]
    assert "pintarMenuPlano" not in cuerpo, "el filtro vuelve a pintar el menú entero"
    assert "dataset.busca" in cuerpo and "c.hidden" in cuerpo


def test_el_filtro_esconde_el_titulo_de_la_materia_vacia():
    """Un título de materia sin tarjetas abajo se lee como un error."""
    s = _fuente()
    i = s.index("function _filtrarMenu")
    assert "tit.hidden = !n" in s[i:i + 2200], "el título queda colgado cuando la sección se vacía"


def test_cada_tarjeta_dice_en_que_estado_esta():
    s = _fuente()
    assert 'c.dataset.estado = sello !== "practicando" ? "dominada" : (st ? "practicando" : "nueva")' in s, (
        "el filtro por estado no puede inventar el estado: sale del sello y de las estrellas")


def test_la_vista_en_lista_se_recuerda():
    """Si se olvida, el que la eligió la tiene que volver a elegir en cada pantalla."""
    s = _fuente()
    assert 'Store.key + "::vista"' in s and "localStorage.setItem(KVISTA" in s


def test_el_estado_se_filtra_con_fichas_y_no_con_un_desplegable():
    """Pablo, 11-sep-2026: *«no me gusta el select, no tiene buen diseño»*.

    Además del gusto hay dos motivos: un `<select>` lo dibuja el sistema operativo —no hay CSS
    que lo haga combinar con el resto, y se ve distinto en cada teléfono— y **esconde las
    opciones hasta que se lo toca**, así que el chico no se entera de que puede filtrar."""
    s = _fuente()
    i = s.index('barra.id = "filtroMenu"')
    bloque = s[i:s.index("stage.appendChild(barra)", i)]
    assert 'el("select")' not in bloque and "estadoAct" not in bloque, (
        "volvió el desplegable de estado")
    assert 'el("div", "filtro-estados")' in bloque, "no están las fichas de estado"
    for txt in ("Sin empezar", "Practicando", "Dominadas"):
        assert txt in bloque, "falta la ficha «%s»" % txt


def test_el_boton_de_vista_no_le_come_las_fichas_de_estado():
    """A 400 px las cuatro fichas de estado más el botón de vista no entran en una fila: la
    última quedaba cortada AL MEDIO contra el botón, y eso no se lee como «hay más, deslizá»
    sino como un error de dibujo (visto en el espejo el 11-sep-2026, antes de mostrarlo).

    El botón sube a la fila del buscador y las fichas se quedan con el ancho entero: lo que
    sobra recorta en el borde de la pantalla, el mismo gesto que las materias."""
    s = _fuente()
    i = s.index('barra.id = "filtroMenu"')
    bloque = s[i:s.index("stage.appendChild(barra)", i)]
    assert "abajo.appendChild(bv)" not in bloque, "el botón de vista volvió a la fila de estados"
    assert 'el("div", "filtro-arriba")' in bloque and "arriba.appendChild(bv)" in bloque, (
        "el botón de vista no está en la fila del buscador")


def test_seguir_por_aca_no_queda_pegado_al_boton_de_abajo():
    """Pablo, 11-sep-2026, con una captura: *«solo un poco mas de margen»*.

    Estaban a 2 px, y el motivo es una trampa clásica: `#stage` es bloque, así que el margen de
    abajo de uno y el de arriba del otro **se colapsan** — el hueco es el mayor de los dos y no
    la suma. Con `2 0 2` y `2 0 10` el resultado era 2 px, no 4."""
    s = _fuente()
    i = s.index(".seguir-aca{")
    m = re.search(r"margin:(\d+)px 0 (\d+)px", s[i:i + 900])
    assert m and int(m.group(2)) >= 10, "«Seguí por acá» volvió a quedar pegado a lo de abajo"
    j = s.index("function _botonModoProfe")
    m2 = re.search(r"margin:(\d+)px 0 (\d+)px", s[j:j + 1600])
    assert m2 and int(m2.group(1)) >= 10, "el botón de Modo Profe volvió a pegarse al de arriba"


def test_la_barra_se_pega_abajo_del_encabezado():
    """El encabezado también es sticky y mide distinto en cada aparato: se mide, no se adivina.

    El corte va de ancla a ancla y no por cantidad de bytes (11-sep-2026): nació leyendo los
    primeros 3.600 bytes y se puso en rojo al sumar comentarios, con `hdr.offsetHeight` en su
    lugar. Es el mismo defecto que hubo que arreglarle a `test_aviso_esi` ese mismo día: un
    test que pasa o falla según dónde cae un byte no está midiendo el código."""
    s = _fuente()
    i = s.index('barra.id = "filtroMenu"')
    bloque = s[i:s.index("const _itSeguir", i)]
    assert "hdr.offsetHeight" in bloque, "la barra se taparía con el encabezado"


def test_esconder_una_tarjeta_la_esconde_de_verdad():
    """`.carta` es flex: sin la regla, el [hidden] del navegador no la tapa."""
    s = _fuente()
    i = s.index("function _adaptCSS")
    css = s[i:s.index("\nfunction ", i + 1)]      # la función entera, no los primeros N bytes
    assert ".carta[hidden]" in css, "esconder tarjetas no funciona sin la regla"


def test_el_emoji_de_materia_se_declara_antes_de_usarse():
    """El 11-sep-2026 el menú de 4.º quedó sin NINGUNA tarjeta con este error: los chips de
    la barra de filtros usaban `EMOJI` y el `const` estaba más abajo, en la misma función. Un
    `const` usado antes de su línea no vale «indefinido»: tira ReferenceError y corta el
    dibujado entero, así que la pantalla queda con el encabezado y nada más.

    Ninguno de los tests de acá lo vio —todos leen el archivo, no la pantalla— y lo encontró
    la corrida en el espejo dev, que es para lo que está. Esto es lo más barato que sí lo
    agarra desde el código: que la declaración venga antes del primer uso."""
    s = _fuente()
    i = s.index("function pintarMenuPlano(")
    cuerpo = s[i:s.index("\nfunction ", i + 1)]
    decl = cuerpo.index("const EMOJI =")
    uso = min(m.start() for m in re.finditer(r"EMOJI\[", cuerpo))
    assert decl < uso, ("`EMOJI` se usa antes de declararse: el menú entero tira "
                        "ReferenceError y no se dibuja ninguna tarjeta")


def test_mas_alla_se_declara_antes_de_usarse():
    """SEGUNDO caso del mismo defecto en el mismo día (11-sep-2026), y éste no era mío:
    `const _masAlla` estaba DESPUÉS de la línea que lo lee (`if (m.escuela && !_masAlla)`), así
    que cualquier cuaderno donde el padre sumó actividades de la escuela tiraba ReferenceError
    y no dibujaba NINGUNA tarjeta.

    Convivió desde el commit 211aa60 porque el `&&` corta antes cuando la tarjeta no es de la
    escuela, y ningún test lo vio: todos leen el archivo. Verificado con node que efectivamente
    tira («Cannot access '_x' before initialization») y que con `escuela:false` pasa limpio."""
    s = _fuente()
    i = s.index("const hacerCarta")
    cuerpo = s[i:s.index("_marcarCiclo();", i)]
    decl = cuerpo.index("const _masAlla =")
    uso = cuerpo.index("!_masAlla")
    assert decl < uso, ("`_masAlla` se usa antes de declararse: el menú entero tira "
                        "ReferenceError en los cuadernos con actividades de la escuela")


def test_cuando_no_hay_resultados_se_avisa():
    s = _fuente()
    assert "#sinResultados" in s and "No encontré nada con" in s, (
        "una pantalla vacía sin explicación parece un cuaderno roto")
