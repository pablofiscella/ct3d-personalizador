"""Lo que faltaba de la investigación ALEKS/DreamBox, cerrado.

  - ALEKS: **nivelación inicial**. El motor abría dando por no-sabido todo el grado, así
    que al chico que ya sabe le hacía perder el tiempo. El sondeo lo UBICA. Lo que se
    verifica acá es la separación que hace que esto no rompa nada: ubicar mueve el frente
    de recomendación pero NO toca el panel de padres ni el 80% que dispara la oferta —
    porque tres respuestas bien no son dominio, y si contaran como tal estaríamos
    cobrando con evidencia falsa.

  - DreamBox: **telemetría de proceso**. El resultado solo no distingue "lo sabe" de
    "acertó tanteando". Se verifica que los campos nuevos sobrevivan el saneo del
    servidor (se descartaba todo campo desconocido) y que el informe los lea.
"""
import json
import re
import os
import subprocess
import sys

import pytest

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASEDIR)

import telemetria_informe as ti  # noqa: E402


def _node(js):
    """Corre JS contra el motor generado. Node es la única forma honesta de probar
    esto: el motor es el archivo que se sirve, no una reimplementación en Python."""
    r = subprocess.run(["node", "-e", js], cwd=BASEDIR, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


PRELUDIO = """
const m = require('./motor_adaptativo.js'); const {Adapt, SABERES_MOTOR} = m;
global.D = {edad: 9, adaptativo_on: true};
let UB = new Set();
global.Store = {ubicado: (s) => UB.has(s), ubicados: () => [...UB],
                sello: () => 'practicando', repasoPendiente: () => false, stars: () => 0};
const ids = new Set();
for (const sid in SABERES_MOTOR) { const s = SABERES_MOTOR[sid];
  if (s.grado <= 4) s.juegos.forEach((j) => ids.add(j)); }
const menu = [...ids];
"""


# ── ALEKS: nivelación inicial ────────────────────────────────────────────────────
def test_el_sondeo_propone_una_actividad_por_materia():
    out = _node(PRELUDIO + """
      const plan = Adapt.planSondeo(menu);
      console.log(JSON.stringify(plan.map((p) => [p.cat, p.sid, p.juego])));
    """)
    plan = json.loads(out)
    cats = [p[0] for p in plan]
    assert len(plan) >= 2, "un sondeo de una sola materia no vale la pena"
    assert len(cats) == len(set(cats)), "no puede repetir materia: %s" % cats
    assert "logica" not in cats, "Extras no es una materia, no se sondea"


def test_el_sondeo_solo_propone_juegos_que_el_chico_puede_abrir():
    """Sondear con un juego que no está en su menú sería una pantalla en blanco."""
    out = _node(PRELUDIO + """
      const plan = Adapt.planSondeo(menu);
      console.log(JSON.stringify(plan.every((p) => menu.indexOf(p.juego) >= 0)));
    """)
    assert out == "true"


def test_acertar_da_por_sabidos_los_prerrequisitos():
    """La inferencia de ALEKS: no se resuelve lo de arriba sin lo de abajo. Es lo que
    hace que un sondeo de 4 preguntas ubique más de 4 saberes."""
    out = _node(PRELUDIO + """
      const plan = Adapt.planSondeo(menu);
      const hondo = plan.slice().sort((a, b) => b.d - a.d)[0];
      const inf = Adapt.saberYPrereqs(hondo.sid);
      console.log(JSON.stringify({sid: hondo.sid, n: inf.size,
                                  tiene: [...inf].indexOf(hondo.sid) >= 0}));
    """)
    r = json.loads(out)
    assert r["tiene"], "tiene que incluir el saber sondeado"
    assert r["n"] > 1, "el saber más hondo del plan debería arrastrar prerrequisitos"


def test_ubicar_mueve_el_frente_de_recomendacion():
    """El objetivo entero: dejar de insistir con lo que ya sabe hacer."""
    out = _node(PRELUDIO + """
      const cuenta = () => { const c = {}; menu.forEach((i) => {
        const e = Adapt.estadoActividad(i); c[e] = (c[e] || 0) + 1; }); return c; };
      const antes = cuenta();
      const plan = Adapt.planSondeo(menu);
      for (const p of plan) for (const s of Adapt.saberYPrereqs(p.sid)) UB.add(s);
      console.log(JSON.stringify({antes: antes, despues: cuenta()}));
    """)
    r = json.loads(out)
    assert r["despues"].get("disponible", 0) > r["antes"].get("disponible", 0), \
        "lo ubicado tiene que dejar de aparecer como pendiente: %s" % r
    assert r["despues"].get("reforzar", 0) < r["antes"].get("reforzar", 0), \
        "ubicar prerrequisitos tiene que destrabar, no dejar todo igual: %s" % r


def test_ubicar_no_toca_el_panel_de_padres_ni_dispara_la_oferta():
    """LA garantía. El panel es lo que el padre lee y el ≥80% es lo que ofrece la
    materia a $2000: si el sondeo contara como dominio, venderíamos con evidencia
    falsa y el tablero mostraría un progreso que el chico no hizo."""
    out = _node(PRELUDIO + """
      const antes = JSON.stringify(Adapt.resumenPorCategoria());
      for (const sid in SABERES_MOTOR) if (SABERES_MOTOR[sid].grado === 4) UB.add(sid);
      console.log(JSON.stringify({antes: antes, despues: JSON.stringify(Adapt.resumenPorCategoria())}));
    """)
    r = json.loads(out)
    assert r["antes"] == r["despues"], \
        "ubicar TODO el grado no puede cambiar ni un número del panel"


def test_el_sondeo_no_corre_sin_el_motor_adaptativo():
    """Los links ya vendidos no tienen que ver una pantalla nueva al abrir el cuaderno."""
    src = open(os.path.join(BASEDIR, "actividades_player.js"), encoding="utf-8").read()
    i = src.index("disponible() {")
    cuerpo = src[i:i + 400]
    assert "D.adaptativo_on" in cuerpo, "el sondeo tiene que estar gateado por el flag"
    assert "sondeoHecho" in cuerpo, "no puede repetirse cada vez que abre el cuaderno"


def test_el_sondeo_se_puede_saltear():
    """Un chico que no quiere no tiene que pasar por un examen para usar su cuaderno."""
    src = open(os.path.join(BASEDIR, "actividades_player.js"), encoding="utf-8").read()
    assert "Ahora no" in src and "marcarSondeo(true)" in src


def test_el_sondeo_no_puntua():
    """No guarda estrellas ni sellos: no es un logro del chico, es el motor
    averiguando por dónde empezar."""
    src = open(os.path.join(BASEDIR, "actividades_player.js"), encoding="utf-8").read()
    i = src.index("if (typeof Sondeo !== \"undefined\" && Sondeo.activo)")
    salida = src[i:i + 260]
    assert "return" in salida
    assert src.index("Store.setStars(self.actual, e)") > i, \
        "la salida del sondeo tiene que estar ANTES de guardar estrellas"


# ── DreamBox: telemetría de proceso ──────────────────────────────────────────────
def test_el_player_manda_los_campos_de_proceso():
    src = open(os.path.join(BASEDIR, "actividades_player.js"), encoding="utf-8").read()
    i = src.index("Tel.push({")
    ev = src[i:i + 700]
    for campo in ("ms1:", "ms:", "toq:"):
        assert campo in ev, "falta %s en el evento de telemetría" % campo


def test_el_servidor_no_descarta_los_campos_nuevos():
    """El saneo del server arma un `rec` con campos explícitos y tira el resto: si no
    se agregan acá, el player los manda y se pierden en silencio."""
    src = open(os.path.join(BASEDIR, "servicio.py"), encoding="utf-8").read()
    i = src.index("def _act_telemetria")
    cuerpo = src[i:i + 2600]
    for campo in ('"ms1"', '"ms"', '"toq"'):
        assert campo in cuerpo, "el server descarta %s" % campo


def test_el_servidor_acota_valores_absurdos():
    """El player corre en el dispositivo del chico: nada de lo que manda es confiable."""
    src = open(os.path.join(BASEDIR, "servicio.py"), encoding="utf-8").read()
    i = src.index("def _act_telemetria")
    cuerpo = src[i:i + 2600]
    assert "min(" in cuerpo and "max(" in cuerpo


# ── el informe que lee todo eso ──────────────────────────────────────────────────
def _escribir(tmp_path, token, eventos, edad=9):
    d = tmp_path / token
    d.mkdir(parents=True)
    (d / "data.json").write_text(json.dumps({"edad": edad}), encoding="utf-8")
    (d / "telemetria.jsonl").write_text(
        "\n".join(json.dumps(e, ensure_ascii=False) for e in eventos), encoding="utf-8")


def test_el_informe_separa_consigna_confusa_de_contenido_dificil(tmp_path, monkeypatch):
    """La distinción que hace útil al informe: una se arregla redactando y la otra
    bajando la dificultad. Confundirlas hace perder el tiempo."""
    lento = [{"j": "confuso", "it": str(i), "ok": False, "primer": True,
              "ms1": 20000, "ms": 30000, "toq": 1, "t": 1} for i in range(8)]
    rapido = [{"j": "dificil", "it": str(i), "ok": False, "primer": True,
               "ms1": 1500, "ms": 4000, "toq": 1, "t": 1} for i in range(8)]
    _escribir(tmp_path, "tok1", lento + rapido)
    monkeypatch.setattr(ti, "ACT_DIR", str(tmp_path))
    inf = ti.informe()
    por = {f["juego"]: f for f in inf["actividades"]}
    assert "consigna confusa" in por["confuso"]["señales"]
    assert "contenido difícil" in por["dificil"]["señales"]


def test_el_informe_detecta_el_acierto_por_tanteo(tmp_path, monkeypatch):
    """El aporte de DreamBox: acertó, pero probando. El resultado solo lo daría por
    sabido."""
    evs = [{"j": "tanteo", "it": str(i), "ok": True, "primer": True,
            "ms1": 800, "ms": 9000, "toq": 14, "t": 1} for i in range(8)]
    _escribir(tmp_path, "tok1", evs)
    monkeypatch.setattr(ti, "ACT_DIR", str(tmp_path))
    inf = ti.informe()
    assert "acierta tanteando" in inf["actividades"][0]["señales"]


def test_el_informe_ignora_muestras_chicas(tmp_path, monkeypatch):
    """Dos respuestas no son un dato; reportarlas sería ruido con forma de evidencia."""
    _escribir(tmp_path, "tok1", [{"j": "poco", "it": "1", "ok": False, "primer": True, "t": 1}] * 2)
    monkeypatch.setattr(ti, "ACT_DIR", str(tmp_path))
    assert ti.informe()["actividades"] == []


def test_el_informe_agrega_varios_cuadernos(tmp_path, monkeypatch):
    """El piloto son 30 chicos: el dato sirve junto, no cuaderno por cuaderno."""
    for tk in ("a", "b", "c"):
        _escribir(tmp_path, tk, [{"j": "x", "it": str(i), "ok": True, "primer": True, "t": 1}
                                 for i in range(3)])
    monkeypatch.setattr(ti, "ACT_DIR", str(tmp_path))
    inf = ti.informe()
    assert inf["cuadernos"] == 3
    assert inf["actividades"][0]["muestra"] == 9
    assert inf["actividades"][0]["chicos"] == 3


def test_el_informe_filtra_por_grado(tmp_path, monkeypatch):
    _escribir(tmp_path, "cuarto", [{"j": "de4", "it": str(i), "ok": True, "primer": True, "t": 1}
                                   for i in range(6)], edad=9)
    _escribir(tmp_path, "sexto", [{"j": "de6", "it": str(i), "ok": True, "primer": True, "t": 1}
                                  for i in range(6)], edad=11)
    monkeypatch.setattr(ti, "ACT_DIR", str(tmp_path))
    assert [f["juego"] for f in ti.informe(grado=4)["actividades"]] == ["de4"]
    assert [f["juego"] for f in ti.informe(grado=6)["actividades"]] == ["de6"]


def test_una_linea_rota_no_invalida_el_archivo(tmp_path, monkeypatch):
    """Los eventos llegan por sendBeacon y se appendean: un corte a mitad de línea es
    esperable, y no puede hacer perder el resto del piloto."""
    d = tmp_path / "tok"
    d.mkdir()
    (d / "data.json").write_text('{"edad": 9}', encoding="utf-8")
    buenas = "\n".join(json.dumps({"j": "x", "it": str(i), "ok": True, "primer": True, "t": 1})
                       for i in range(6))
    (d / "telemetria.jsonl").write_text(buenas + '\n{"j": "x", "it": rot', encoding="utf-8")
    monkeypatch.setattr(ti, "ACT_DIR", str(tmp_path))
    assert ti.informe()["actividades"][0]["muestra"] == 6


# ── "¿Cómo es?": instrucción explícita ───────────────────────────────────────────
def _como_es():
    """Las claves y el contenido del mapa COMO_ES, leídos del player con node."""
    out = _node("""
      const fs = require('fs');
      const src = fs.readFileSync('actividades_player.js', 'utf8');
      const i = src.indexOf('const COMO_ES = {');
      const f = src.indexOf('\\nconst FRASES_BIEN');
      const COMO_ES = eval('(' + src.slice(i + 'const COMO_ES = '.length, f).trim().replace(/;$/, '') + ')');
      console.log(JSON.stringify(COMO_ES));
    """)
    return json.loads(out)


def _games_definidos():
    out = _node("""
      const fs = require('fs');
      let src = fs.readFileSync('actividades_player.js', 'utf8');
      try { src += fs.readFileSync('actividades_curriculum.js', 'utf8'); } catch (e) {}
      console.log(JSON.stringify([...new Set([...src.matchAll(/GAMES\\.(\\w+)\\s*=/g)].map((m) => m[1]))]));
    """)
    return set(json.loads(out))


def test_toda_mini_leccion_apunta_a_un_juego_real():
    """Una lección de un juego que no existe no la ve nadie: es trabajo tirado."""
    faltan = sorted(set(_como_es()) - _games_definidos())
    assert not faltan, "mini-lecciones sin juego: %s" % faltan


def test_las_mini_lecciones_estan_completas():
    """Título y al menos dos líneas de regla: una sola línea no explica nada."""
    flacas = [k for k, v in _como_es().items()
              if not v.get("t") or len(v.get("l") or []) < 2]
    assert not flacas, "mini-lecciones incompletas: %s" % flacas


def test_hay_mini_leccion_para_acentuacion():
    """Es el pedido textual de Pablo: tener siempre a mano cuál es cuál."""
    c = _como_es().get("acentuacion")
    assert c, "falta justo la que originó el pedido"
    txt = " ".join(c["l"]).lower()
    for palabra in ("aguda", "grave", "esdrújula"):
        assert palabra in txt, "la lección de acentuación no nombra %s" % palabra


def test_el_boton_aparece_solo_donde_hay_regla():
    """Un botón que dice obviedades enseña a ignorar el botón. Los juegos de dato
    (comprensión, fotosíntesis, historia) no llevan."""
    ce = _como_es()
    for sin_regla in ("memotest", "sopa", "laberinto", "comprension_lectora", "fotosintesis"):
        assert sin_regla not in ce, "%s no enseña una regla: no debería tener lección" % sin_regla


def test_el_boton_se_agrega_al_abrir_la_actividad():
    src = open(os.path.join(BASEDIR, "actividades_player.js"), encoding="utf-8").read()
    assert "botonComoEs(id)" in src and "#consigna" in src


def test_cerrar_la_leccion_corta_la_voz():
    """Si no, la voz sigue explicando encima de la actividad que ya volvió a jugar."""
    src = open(os.path.join(BASEDIR, "actividades_player.js"), encoding="utf-8").read()
    i = src.index("function mostrarComoEs")
    assert "pararVoz()" in src[i:i + 1200]
    assert "function pararVoz()" in src


# ── anti-memorización: generar en vez de escribir ────────────────────────────────
def _valpos():
    out = _node("""
      const fs = require('fs');
      const src = fs.readFileSync('actividades_player.js', 'utf8');
      const i = src.indexOf('const VALPOS_BANCO = (() => {');
      const j = src.indexOf('GAMES.valor_posicional');
      eval(src.slice(i, j).replace('const VALPOS_BANCO', 'var VALPOS_BANCO'));
      console.log(JSON.stringify(VALPOS_BANCO));
    """)
    return json.loads(out)


def test_valor_posicional_se_genera_y_no_se_memoriza():
    """Eran 14 preguntas fijas: en dos partidas las vio todas y lo que medíamos era
    memoria. Ahora el ítem sale de la regla."""
    b = _valpos()
    assert len(b) > 150, "con pocos ítems vuelve a ser memorizable (hay %d)" % len(b)


def test_ninguna_pregunta_de_valor_posicional_es_ambigua():
    """'En el número 121, ¿cuánto vale el 1?' tiene DOS respuestas correctas. Un ítem
    ambiguo le enseña al chico que la regla no cierra."""
    malos = []
    for it in _valpos():
        m = re.match(r"En el número (\d+), ¿cuánto vale el (\d)\?", it["q"])
        assert m, "formato inesperado: %s" % it["q"]
        num, dig = m.group(1), m.group(2)
        if num.index(dig) != num.rindex(dig):
            malos.append(it["q"])
    assert not malos, "preguntas con dos respuestas posibles: %s" % malos[:5]


def test_la_respuesta_de_valor_posicional_es_la_correcta():
    """La primera opción es la correcta (juegoTriviaTexto usa ops[0]); tiene que ser
    exactamente cifra × potencia de diez."""
    malos = []
    for it in _valpos():
        m = re.match(r"En el número (\d+), ¿cuánto vale el (\d)\?", it["q"])
        num, dig = m.group(1), m.group(2)
        pos = len(num) - 1 - num.index(dig)
        if it["ops"][0] != str(int(dig) * 10 ** pos):
            malos.append(it["q"])
    assert not malos, "respuesta incorrecta en: %s" % malos[:5]


def test_las_opciones_de_valor_posicional_son_distintas():
    """Dos opciones iguales dan dos botones correctos o dos incorrectos idénticos."""
    malos = [it["q"] for it in _valpos() if len(set(it["ops"])) != 3]
    assert not malos, "opciones repetidas en: %s" % malos[:5]


def _banco(nombre):
    out = _node("""
      const fs = require('fs');
      const src = fs.readFileSync('actividades_player.js', 'utf8');
      const re = new RegExp('const %s = \\\\[([\\\\s\\\\S]*?)\\\\n\\\\];');
      const m = src.match(re);
      eval('var B = [' + m[1] + '\\n];');
      console.log(JSON.stringify(B));
    """ % nombre)
    return json.loads(out)


def test_los_cuerpos_geometricos_tienen_datos_correctos():
    """Se amplió de 3 a 10. Cada cuerpo lleva caras/vértices/aristas, y si alguno está
    mal le estamos enseñando geometría equivocada a un chico de 4°."""
    esperado = {
        "el cubo": (6, 8, 12), "el prisma rectangular": (6, 8, 12),
        "la pirámide de base cuadrada": (5, 5, 8), "la pirámide de base triangular": (4, 4, 6),
        "el prisma de base triangular": (5, 6, 9), "el prisma de base pentagonal": (7, 10, 15),
        "el prisma de base hexagonal": (8, 12, 18),
        "el cilindro": (3, 0, 2), "el cono": (2, 1, 1), "la esfera": (1, 0, 0),
    }
    banco = _banco("CUERPOS_BANCO")
    assert len(banco) >= 10
    for c in banco:
        e = esperado.get(c["nombre"])
        assert e, "cuerpo sin verificar: %s" % c["nombre"]
        assert (c["caras"], c["vertices"], c["aristas"]) == e, \
            "%s tiene datos mal: %s" % (c["nombre"], c)


def test_a_los_cuerpos_redondos_no_se_les_pregunta_por_las_caras():
    """Cuántas caras tiene una esfera depende de si el manual cuenta la superficie
    curva. No vamos a enseñar una respuesta que la maestra pueda marcar mal."""
    src = open(os.path.join(BASEDIR, "actividades_player.js"), encoding="utf-8").read()
    i = src.index("GAMES.cuerpos_geometricos")
    frag = src[i:i + 2000]
    assert "item.redondo ?" in frag, "falta la restricción para los cuerpos redondos"


def test_el_poligono_declara_bien_sus_lados():
    lados = {"Triángulo": 3, "Triángulo equilátero": 3, "Triángulo isósceles": 3,
             "Triángulo escaleno": 3, "Cuadrado": 4, "Rectángulo": 4, "Rombo": 4,
             "Trapecio": 4, "Trapezoide": 4, "Romboide": 4, "Paralelogramo": 4,
             "Cuadrilátero": 4, "Pentágono": 5, "Hexágono": 6, "Heptágono": 7,
             "Octágono": 8, "Eneágono": 9, "Decágono": 10, "Endecágono": 11,
             "Dodecágono": 12}
    banco = _banco("POLIGONOS_BANCO")
    assert len(banco) >= 20
    for p in banco:
        assert lados.get(p["nombre"]) == p["lados"], "mal: %s" % p


def test_no_hay_animales_repetidos_en_el_banco():
    """Repetido = el mismo animal con dos comidas distintas: el chico acierta y le
    marcamos mal, o al revés."""
    banco = _banco("ANIMAL_COMIDA_BANCO")
    assert len(banco) >= 24
    animales = [x["animal"] for x in banco]
    assert len(animales) == len(set(animales)), "animales repetidos"


@pytest.mark.parametrize("args", [[], ["--json"], ["--grado", "4"]])
def test_el_cli_corre(tmp_path, args):
    """Que ande de verdad desde la línea de comandos, que es como se va a usar."""
    (tmp_path / "vacio").mkdir()
    env = dict(os.environ, CT3D_ACT_DIR=str(tmp_path))
    r = subprocess.run([sys.executable, os.path.join(BASEDIR, "telemetria_informe.py")] + args,
                       capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip()
