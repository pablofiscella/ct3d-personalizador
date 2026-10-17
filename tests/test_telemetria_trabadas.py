"""Detectar la actividad que deja a un chico trabado, sin poder terminarla.

POR QUÉ EXISTE (19-sep-2026). La sopa de letras aceptaba sólo el arrastre, no lo decía en
ninguna parte, y al gesto equivocado contestaba con silencio. Una chica de 4.º grado estuvo
**once minutos** con 23 intentos fallidos. El informe de telemetría que ya existía **no lo
vio**: marca "contenido difícil" por precisión baja al primer intento, y con ese criterio
también marca al memotest —donde fallar la primera vez ES la mecánica—, así que la señal
que importaba quedaba enterrada entre falsos positivos.

Pablo: *"la telemetría tiene que hacer saltar inmediatamente estos errores y avisar para
corregirlos"*.

Lo que cuidan estos tests es que la alerta sirva para eso y no se vuelva ruido:

  · que **distinga trabarse de que algo sea difícil** — el tiempo pegado es la diferencia;
  · que **no marque al memotest**, que falla mucho y rápido y es lo que tiene que hacer;
  · que **separe por sesión y no por cuaderno**, porque los cuadernos de muestra los usan
    muchas personas con el mismo token y ahí el caso real se diluye hasta desaparecer;
  · que el aviso traiga **lo necesario para actuar**: qué actividad, cuándo y qué error.
"""
import json
import os
import subprocess
import sys

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASEDIR)

import telemetria_informe as ti  # noqa: E402

MIN = 60 * 1000
T0 = 1_758_300_000_000   # un momento cualquiera, en ms


def _escribir(tmp_path, token, eventos):
    d = tmp_path / token
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "telemetria.jsonl", "w", encoding="utf-8") as f:
        for e in eventos:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def _ev(j, t, ok, **extra):
    e = {"j": j, "it": j + "#0", "ok": ok, "primer": True, "t": t, "edad": "9"}
    e.update(extra)
    return e


def _trabadas(tmp_path, monkeypatch):
    monkeypatch.setattr(ti, "ACT_DIR", str(tmp_path))
    return ti.trabadas()


# ─────────────────── lo que TIENE que saltar ───────────────────

def test_once_minutos_sin_poder_terminar_salta(tmp_path, monkeypatch):
    """El caso real del 19-sep: 23 intentos fallidos en once minutos y casi nada bien."""
    evs = [_ev("sopa", T0 + i * 28 * 1000, i % 7 == 0, motivo=None if i % 7 == 0 else "No es esa palabra")
           for i in range(27)]
    _escribir(tmp_path, "muestra-kydo-4", evs)
    filas = _trabadas(tmp_path, monkeypatch)
    assert len(filas) == 1, filas
    f = filas[0]
    assert f["juego"] == "sopa"
    assert f["fallos"] >= ti.TRABA_FALLOS
    assert f["minutos"] >= ti.TRABA_MINUTOS
    assert f["precision"] < ti.TRABA_PRECISION


def test_el_aviso_trae_lo_necesario_para_actuar(tmp_path, monkeypatch):
    """Un aviso que no dice qué mirar obliga a investigar de cero y se ignora."""
    evs = [_ev("sopa", T0 + i * 30 * 1000, False, motivo="No es esa palabra") for i in range(12)]
    _escribir(tmp_path, "muestra-kydo-4", evs)
    f = _trabadas(tmp_path, monkeypatch)[0]
    assert f["cuaderno"] == "muestra-kydo-4"
    assert f["error_dominante"] == "No es esa palabra"
    assert f["edad"] == "9"
    assert "T" in f["cuando"]          # fecha y hora, no un número de milisegundos
    texto = ti._humano_trabadas([f])
    assert "sopa" in texto and "min" in texto


# ─────────────────── lo que NO tiene que saltar ───────────────────

def test_el_memotest_no_salta(tmp_path, monkeypatch):
    """Fallar el primer intento ES la mecánica del memotest: si lo marca, el aviso se
    vuelve ruido y a la semana nadie lo lee. Falla mucho, pero rápido y avanzando."""
    evs = [_ev("memotest", T0 + i * 3 * 1000, i % 4 == 0) for i in range(20)]
    _escribir(tmp_path, "revision-3ro", evs)
    assert _trabadas(tmp_path, monkeypatch) == []


def test_dificil_pero_avanzando_no_salta(tmp_path, monkeypatch):
    """Diez minutos de actividad con errores, pero acertando: eso es aprender."""
    evs = [_ev("suma_columnas", T0 + i * 20 * 1000, i % 2 == 0) for i in range(40)]
    _escribir(tmp_path, "revision-4to", evs)
    assert _trabadas(tmp_path, monkeypatch) == []


def test_pocos_fallos_no_saltan(tmp_path, monkeypatch):
    """Equivocarse tres veces no es estar trabado."""
    evs = [_ev("poema_3", T0 + i * 90 * 1000, False) for i in range(3)]
    _escribir(tmp_path, "revision-2do", evs)
    assert _trabadas(tmp_path, monkeypatch) == []


# ─────────────────── el detalle que hacía invisible el caso real ───────────────────

def test_las_sesiones_se_separan_y_el_caso_no_se_diluye(tmp_path, monkeypatch):
    """LOS CUADERNOS DE MUESTRA LOS USAN MUCHAS PERSONAS con el mismo token.

    Agrupando por token, la chica de la sopa quedaba entre todas las visitas del día
    —43 fallos, 30 minutos y 60 % de aciertos, que no alarma a nadie— y no saltaba.
    Acá: una sesión con gente que juega bien, y horas después la que se traba."""
    buenos = [_ev("sopa", T0 + i * 20 * 1000, True) for i in range(40)]
    trabada = [_ev("sopa", T0 + 5 * 60 * 60 * 1000 + i * 30 * 1000, False) for i in range(14)]
    _escribir(tmp_path, "muestra-kydo-4", buenos + trabada)
    filas = _trabadas(tmp_path, monkeypatch)
    assert len(filas) == 1, "la sesión trabada se diluyó entre las buenas"
    assert filas[0]["fallos"] == 14
    assert filas[0]["aciertos"] == 0


def test_un_hueco_largo_corta_la_sesion(tmp_path, monkeypatch):
    """Dos ratos de 6 fallos separados por una hora son dos personas (o dos días), no una
    sesión de 12 fallos. Sin este corte, sumar ratos sueltos inventaría trabas."""
    a = [_ev("acentuacion", T0 + i * 60 * 1000, False) for i in range(6)]
    b = [_ev("acentuacion", T0 + 60 * 60 * 1000 + i * 60 * 1000, False) for i in range(6)]
    _escribir(tmp_path, "sb-abc", a + b)
    assert _trabadas(tmp_path, monkeypatch) == []


# ─────────────────── que se pueda usar desde afuera ───────────────────

def test_la_linea_de_comando_da_json(tmp_path, monkeypatch):
    """La alerta lo consume desde otro sistema: tiene que salir JSON parseable."""
    evs = [_ev("sopa", T0 + i * 30 * 1000, False, motivo="No es esa palabra") for i in range(12)]
    _escribir(tmp_path, "muestra-kydo-4", evs)
    env = dict(os.environ, CT3D_ACT_DIR=str(tmp_path))
    r = subprocess.run([sys.executable, "telemetria_informe.py", "--trabadas", "--json"],
                       cwd=BASEDIR, capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stderr
    filas = json.loads(r.stdout)
    assert len(filas) == 1 and filas[0]["juego"] == "sopa"


def test_sin_datos_no_rompe(tmp_path, monkeypatch):
    """Una instalación nueva no tiene telemetría. No puede explotar por eso."""
    assert _trabadas(tmp_path, monkeypatch) == []
    assert "Ninguna" in ti._humano_trabadas([])
