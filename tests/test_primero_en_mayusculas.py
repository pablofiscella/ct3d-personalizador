# -*- coding: utf-8 -*-
"""1.º se ve en imprenta MAYÚSCULA, salvo donde la minúscula es el contenido.

15-ago-2026. Pablo: *«todo el cuaderno de primero tiene que verse en mayúsculas»*. Y enseguida
el chequeo que salvó el cambio: *«mirá la currícula de CABA de primero y fijate si ven
minúsculas»*.

**Sí la ven, y es contenido explícito del año.** `docs/auditoria-dc-caba/grado-1.md` describe
«Parejas de letras» —DC *«Mayúscula y minúscula de la misma letra»*— como *«muestro G, tocá su
minúscula»*. En los datos: `q:"A"`, `ops:["a","e","o"]`. En mayúsculas eso queda «A» → `A|E|O`:
le pide la minúscula de la A y no le muestra ninguna.

Por eso el cambio es de VISTA (`text-transform`, así no cambia la clave del manifiesto de voz
ni deja huérfanos los mp3 grabados) y tiene DOS frenos: la excepción declarada en los datos,
al lado del DC que la justifica, y una red automática para lo que se escriba mañana.

CUATRO COSAS QUE FALLARON, y ninguna se veía leyendo el código:

1. **El `<button>` no hereda `text-transform`.** Es el estilo por defecto del navegador para
   los controles de formulario. `#juego` computaba `uppercase` y el botón computaba `none`: la
   consigna salía en mayúscula y las respuestas en minúscula — la mezcla de dos alfabetos que
   el cambio venía a sacar.
2. **El vigía se enganchaba a `DOMContentLoaded`**, que ya pasó cuando carga el player.
3. **Y vigilaba un nodo tirado**: `Shell.abrir()` hace `stage.innerHTML = ""` y crea un
   `#juego` NUEVO en cada actividad.
4. **La red automática apagaba la mayúscula en cuatro actividades sanas.** Preguntaba «¿quedan
   dos opciones iguales en mayúscula?» y en un memotest las cartas vienen DE A PARES: ya eran
   iguales antes. El barrido dio 6 excepciones cuando había 2 declaradas — otra vez un número
   que no cerró con otro.

Lo que se ve en pantalla está verificado aparte con Playwright contra el espejo dev: 64
actividades de 1.º, 2 excepciones (las declaradas), 0 en minúscula, y nada en mayúsculas
llegando a la voz.
"""
import json
import os
import re
import shutil
import subprocess

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER = os.path.join(RAIZ, "actividades_player.js")
HTML = os.path.join(RAIZ, "actividades_player.html")


def _player():
    return open(PLAYER, encoding="utf-8").read()


def _html():
    return open(HTML, encoding="utf-8").read()


def _css_sin_comentarios():
    """La hoja SIN los `/* … */`.

    Importa más de lo que parece: estas reglas van muy comentadas —cada excepción explica el
    DC que la justifica— y un test que busque `#toast` en el texto crudo lo encuentra en el
    comentario aunque el selector diga otra cosa. Pasó: una mutación que rompía la regla de
    verdad dio VERDE porque el nombre seguía nombrado dos líneas más arriba, en prosa."""
    return re.sub(r"/\*.*?\*/", " ", _html(), flags=re.S)


def _regla_mayusculas():
    """El bloque CSS que pone 1.º en mayúsculas."""
    m = re.search(r"(body\.g1:not\(\.caja-importa\)[^{]*\{[^}]*\})", _css_sin_comentarios())
    assert m, "desapareció la regla que pone 1.º en mayúsculas"
    return m.group(1)


def _reglas_g1():
    """Todos los bloques `body.g1 …` del cuaderno (el del juego y el del menú)."""
    return "\n".join(re.findall(r"(body\.g1[^{]*\{[^}]*\})", _css_sin_comentarios()))


def test_la_regla_nombra_a_los_controles_porque_no_heredan():
    """EL test de esta tanda. El navegador le pone `text-transform: none` a `button`, `input`,
    `select` y `textarea` por su cuenta, así que la herencia desde `#juego` NO les llega.
    Medido: `#juego` computaba `uppercase` y el botón de la opción computaba `none`. Si
    alguien simplifica la regla a `#juego` solo, vuelve la consigna en mayúscula con las
    respuestas en minúscula."""
    regla = _regla_mayusculas()
    for control in ("button", "input", "select", "textarea"):
        assert "#juego %s" % control in regla, (
            "la regla no nombra `#juego %s`. Los controles de formulario no heredan "
            "`text-transform`: hay que nombrarlos uno por uno." % control)


def test_cada_contenedor_que_se_transforma_nombra_sus_botones():
    """La misma trampa mordió TRES veces en una hora: el juego (las opciones), el menú (el
    rótulo de la tarjeta, que es un div adentro de un `<button>`) y el panel «¿Cómo es?» (los
    botones «▶ ver el video» y «¡Ya entendí!»). Las tres veces el contenedor computaba
    `uppercase` y el control adentro computaba `none`.

    Así que la regla queda escrita: **todo contenedor que se transforme tiene que nombrar
    también a sus botones.** Si mañana se agrega otro contenedor a la lista de arriba, este
    test lo obliga a traer su `button`."""
    reglas = _reglas_g1()
    contenedores = [c for c in ("#juego", ".comoes", ".carta",
                                "#festejo", "#logro", "#perfil", "#candado") if c in reglas]
    assert contenedores, "no encontré ningún contenedor en las reglas de 1.º"
    for c in contenedores:
        assert re.search(re.escape(c) + r"\s+(button|\.nombre)", reglas), (
            "`%s` se transforma pero no nombra lo que lleva adentro. Los controles de "
            "formulario no heredan `text-transform`: el contenedor queda en mayúscula y el "
            "botón en minúscula." % c)


def test_estan_todas_las_pantallas_del_chico():
    """El recorrido de 1.º no es sólo el menú y el tablero. Un primer barrido dio «64 de 64»
    y sonaba a terminado; lo que no cubría eran las pantallas que se abren ENCIMA y a las que
    sólo se llega jugando:

    · `#festejo`  — «¡Muy bien, Sofi!», aparece al cerrar CADA actividad
    · `#logro`    — el diploma
    · `#perfil`   — «¿Quién juega?»
    · `#candado`  — «Este nivel está guardado, pedile a tu grande que lo abra»
    · `#nivelbar` — los chips de nivel
    · `#explica`  — EL PORQUÉ. Cuelga del `<body>`, no del `#juego`, así que ninguna regla de
                    adentro del juego lo alcanzaba. Es lo que el chico lee justo cuando se
                    equivoca, y es el único de la lista que lleva el freno `caja-importa`,
                    porque en «Parejas de letras» la explicación habla de la letra chiquita.

    Un barrido que mira sólo la pantalla que uno se acordó de abrir cuenta lo que eligió
    contar."""
    reglas = _reglas_g1()
    for p in ("#festejo", "#logro", "#perfil", "#candado", "#nivelbar", "#explica"):
        assert p in reglas, (
            "`%s` es una pantalla que ve el chico de 1.º y quedó fuera de la mayúscula" % p)
    assert "body.g1:not(.caja-importa) #explica" in _html(), (
        "`#explica` tiene que llevar el freno `caja-importa`: en «Parejas de letras» la "
        "explicación nombra la letra minúscula")
    # y el Modo Profe, que es del adulto, NO se transforma
    assert "#stage {" not in reglas and "#stage," not in reglas, (
        "transformar `#stage` entero alcanzaría también al Modo Profe, que son cuatro "
        "pantallas de autor para un adulto")


def test_ninguna_pantalla_que_se_abre_encima_queda_sin_decidir():
    """EL guardián que reemplaza a mi memoria. En vez de una lista escrita a mano —que es una
    apuesta sobre el cuaderno de mañana— se ENUMERAN las pantallas que se abren encima
    (`role="dialog"` en el HTML y los `position:fixed` que arma el JS) y se exige que cada una
    esté decidida: o va en mayúsculas, o está declarada como pantalla del adulto.

    Nace de haberme comido tres barridos seguidos. El primero miró el menú y dio «64 de 64».
    El segundo jugó y encontró el festejo. El tercero cruzó los contenedores del HTML contra
    las reglas y encontró el `#toast` —el «¡Muy bien!» de CADA acierto, el texto que más veces
    ve en toda la sesión— y el «Preparando tus juegos…». **Un barrido sólo encuentra lo que
    uno se acordó de abrir; un cruce encuentra lo que uno se olvidó.**"""
    # Las que serían del adulto y por eso NO se transformarían, con el motivo al lado.
    # Hoy está VACÍO a propósito: de las pantallas que se abren encima, ninguna es del
    # adulto — las del adulto (Modo Profe, panel de padres, nota a la familia) no son
    # diálogos con id, se dibujan en `#stage` o con clase propia. Si mañana aparece una,
    # se anota acá con el motivo en vez de hacerle un agujero a la regla.
    DEL_ADULTO = {}
    html, reglas = _html(), _reglas_g1()
    pantallas = set(re.findall(r'<\w+\s+id="([\w-]+)"[^>]*role="dialog"', html))
    pantallas |= {m.group(1) for m in re.finditer(r'\.id\s*=\s*"([\w-]+)"', _player())
                  if "position:fixed" in _player()[max(0, m.start() - 200):m.end() + 400]}
    pantallas |= {"cargando", "toast"}          # las dos que se me habían pasado
    assert len(pantallas) >= 6, "el enumerador dejó de encontrar pantallas: revisarlo"
    sin_decidir = [p for p in sorted(pantallas)
                   if not re.search(r"#" + re.escape(p) + r"\b", reglas) and p not in DEL_ADULTO]
    assert not sin_decidir, (
        "estas pantallas se le abren al chico y nadie decidió si van en mayúscula: %s. "
        "O se agregan a la regla de 1.º, o se declaran en DEL_ADULTO con el motivo."
        % ", ".join(sin_decidir))


def test_el_grado_se_marca_antes_de_la_pantalla_de_carga():
    """«Preparando tus juegos…» se ve ANTES de que exista el menú. Medido en el navegador:
    salía con el `<body>` sin ninguna clase, así que la regla de mayúsculas no la alcanzaba —
    la regla estaba escrita y no hacía nada, que es peor que no tenerla, porque cuenta como
    hecha. `gradoDelChico()` sólo mira `D.edad`, que ya está cargado en ese momento."""
    s = _player()
    i = s.find("  P = D.personajes;")
    assert i > 0, "cambió el arranque: revisar este test"
    j = s.find('$("#cargando").remove()')
    assert j > i, "cambió el orden del arranque: revisar este test"
    assert "_marcarCiclo();" in s[i:j], (
        "el grado se marca después de que se fue la pantalla de carga: lo primero que ve el "
        "chico de 1.º queda en el alfabeto que todavía no lee")


def test_es_solo_de_vista_no_cambia_el_texto():
    """Va por `text-transform`. Si algún día se hiciera con `.toUpperCase()` sobre el texto,
    cambiaría la clave del manifiesto de voz y quedarían huérfanos los mp3 ya grabados."""
    assert "text-transform: uppercase" in _regla_mayusculas()


def test_la_voz_recibe_el_texto_crudo():
    """`innerText` devuelve lo que se VE —o sea ya en mayúsculas— y el motor deletrea las
    mayúsculas cuando parecen siglas: Valeria diría «ce-a-eme-pe-o» en vez de «campo»."""
    s = _player()
    i = s.find("function _opcionesEnPantalla")
    assert i > 0, "cambió el nombre de _opcionesEnPantalla: revisar este test"
    cuerpo = s[i:i + 900]
    assert "textContent" in cuerpo, "las opciones habladas volvieron a leer lo transformado"
    assert not re.search(r"\bb\.innerText\b", cuerpo), \
        "`innerText` devuelve el texto ya en mayúsculas y la voz lo deletrea"


def test_el_vigia_se_engancha_al_juego_que_existe_ahora():
    """`Shell.abrir()` tira el stage entero y dibuja un `#juego` NUEVO en cada actividad. Un
    observer puesto una sola vez al cargar la página termina mirando un nodo fuera del
    documento — y encima el player carga DESPUÉS de `DOMContentLoaded`, así que ni siquiera
    llegaba a ponerse."""
    s = _player()
    assert "_vigilarCaja()" in s, "nadie llama al vigía de la caja"
    i = s.find('<div id="progreso"></div><div id="juego"></div>')
    assert i > 0, "cambió el armado del stage: revisar este test"
    assert "_vigilarCaja()" in s[i:i + 260], (
        "el vigía no se vuelve a enganchar cuando `Shell.abrir` dibuja el `#juego` nuevo")
    vigia = s[s.find("function _vigilarCaja"):]
    vigia = vigia[:vigia.find("\n}") + 2]
    assert "DOMContentLoaded" not in vigia, (
        "el player carga después de `DOMContentLoaded`: ese listener no se dispara nunca")


def test_la_excepcion_viaja_con_el_dato():
    """Una lista escrita a mano en el player es una apuesta sobre el contenido de mañana. La
    excepción se declara en `actividades_curriculum.py`, al lado del DC que la justifica, y el
    generador la emite como `CAJA_IMPORTA`."""
    cur = open(os.path.join(RAIZ, "actividades_curriculum.py"), encoding="utf-8").read()
    for act in ("parejas_letras_1", "mayuscula_punto_1"):
        m = re.search(r'\{"id":"%s",([^}]{0,120})' % act, cur)
        assert m and '"caja":True' in m.group(1), \
            "%s ya no declara `caja`: en mayúsculas queda incontestable" % act
    gen = open(os.path.join(RAIZ, "gen_curriculum.py"), encoding="utf-8").read()
    assert "CAJA_IMPORTA" in gen, "el generador dejó de emitir CAJA_IMPORTA"
    js = open(os.path.join(RAIZ, "actividades_curriculum.js"), encoding="utf-8").read()
    m = re.search(r"const CAJA_IMPORTA = new Set\((\[[^\]]*\])\);", js)
    assert m, "el .js generado no trae CAJA_IMPORTA: falta correr gen_curriculum.py"
    assert set(json.loads(m.group(1))) == {"parejas_letras_1", "mayuscula_punto_1"}


@pytest.mark.skipif(shutil.which("node") is None, reason="node no está instalado")
def test_la_red_no_apaga_la_mayuscula_en_un_memotest():
    """EL otro test. Se ejecuta la función REAL del player contra tres tableros:

    - memotest (cartas repetidas, que ya eran iguales antes de transformar) → transformar
    - «Parejas de letras» (a/e/o, que en mayúscula siguen siendo distintas) → NO transformar,
      y sólo lo salva la lista declarada: la red sola lo deja pasar
    - «El gato duerme.» / «el gato duerme.» → NO transformar, ésta sí la caza la red

    Contra `textos.length`, el memotest daba falso positivo y cuatro actividades sanas se
    quedaban en minúscula.
    """
    js = r"""
const fs = require("fs");
const src = fs.readFileSync(%s, "utf8");
const m = src.match(/function _ajustarMayusculas\(\) \{[\s\S]*?\n\}/);
if (!m) { console.error("no encontré _ajustarMayusculas()"); process.exit(1); }

let clases = new Set();
const CAJA_IMPORTA = new Set(["parejas_letras_1", "mayuscula_punto_1"]);
let Shell = { actual: null };
const document = {
  body: { classList: { toggle: (c, v) => { v ? clases.add(c) : clases.delete(c); } } },
  getElementById: () => ({ querySelectorAll: () => tablero.map(
      (t) => ({ textContent: t, offsetParent: {} })) }),
};
let tablero = [];
eval(m[0]);

function probar(id, ops) {
  clases = new Set(); Shell.actual = id; tablero = ops;
  _ajustarMayusculas();
  return clases.has("caja-importa");
}
console.log(JSON.stringify({
  memotest: probar("memotest", ["🐶", "🐱", "🐶", "🐱"]),
  kiosco:   probar("kiosco_1", ["$5", "$5", "$10"]),
  parejas:  probar("parejas_letras_1", ["a", "e", "o"]),
  gato:     probar("mayuscula_dc", ["El gato duerme.", "el gato duerme.", "un perro"]),
  normal:   probar("silabas_1", ["Sol", "Luna", "Mar"]),
}));
""" % json.dumps(PLAYER)
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-2000:]
    d = json.loads(r.stdout.strip())
    assert d["memotest"] is False, (
        "la red apaga la mayúscula en un memotest: las cartas vienen de a pares y YA eran "
        "iguales antes de transformar. Hay que comparar los distintos contra los distintos.")
    assert d["kiosco"] is False, "mismo caso: opciones repetidas que no tienen que ver con la caja"
    assert d["normal"] is False, "una actividad común no tiene por qué quedar en minúscula"
    assert d["parejas"] is True, (
        "«Parejas de letras» tiene que respetar la minúscula, y la red sola NO lo caza: "
        "a/e/o siguen siendo distintas en mayúscula. Sale de la lista declarada.")
    assert d["gato"] is True, (
        "la red tiene que cazar el caso que sí rompe: dos opciones DISTINTAS que se vuelven "
        "la misma en mayúscula")
