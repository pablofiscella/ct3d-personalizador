# -*- coding: utf-8 -*-
"""Las lecciones son de cada sistema. Un cuaderno de Kydo no lee la carpeta del otro.

4-ago-2026. Pablo, al ver la marca de las lámparas adentro de una lección servida en un
cuaderno de Kydo: *"no puedo creer que siga pasando. ¿Sigue compartiendo cosas?"*. Y la
decisión: *"quiero que separemos todo. Nada tiene que compartir con Casatridimensional. Si
algo se duplica está bien porque son dos sistemas distintos"*. Y la condición: *"mientras no
se filtre nada"*.

Hasta hoy había UNA carpeta de lecciones para los dos negocios, y por eso una línea escrita
en el cierre de una lección terminó apareciendo en el cuaderno del otro.

NO son dos copias a sincronizar: son dos sistemas que **pueden divergir**, que es el punto
de la regla. El día que Kydo quiera una lección distinta de la de cumpleaños, la cambia sin
pedirle permiso a nadie.

Este archivo es la condición de Pablo hecha test.
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import actividades_web as aw  # noqa: E402


def test_existen_las_dos_carpetas():
    """La de Kydo tiene que EXISTIR: si no, `_leccion_dir` cae a la de cumpleaños y la
    separación queda decorativa."""
    assert os.path.isdir(aw.LECCION_DIR), aw.LECCION_DIR
    assert os.path.isdir(aw.LECCION_DIR_KYDO), (
        "falta %s: sin esa carpeta, los cuadernos de Kydo siguen leyendo la del otro "
        "negocio" % aw.LECCION_DIR_KYDO)


def test_son_carpetas_DISTINTAS():
    """El control obvio, y el que rompería un copiar-pegar distraído."""
    assert os.path.realpath(aw.LECCION_DIR) != os.path.realpath(aw.LECCION_DIR_KYDO)


def test_un_cuaderno_escolar_lee_la_carpeta_de_kydo(monkeypatch):
    """EL test. Es la condición de Pablo hecha código: que no se filtre nada."""
    monkeypatch.setattr(aw, "_es_escolar", lambda token, reg=None: True)
    assert aw._leccion_dir("token-de-prueba") == aw.LECCION_DIR_KYDO


def test_un_cuaderno_de_cumple_lee_la_suya(monkeypatch):
    """El otro lado. Separar no puede llevarse puesto el negocio que sí funciona."""
    monkeypatch.setattr(aw, "_es_escolar", lambda token, reg=None: False)
    assert aw._leccion_dir("token-de-prueba") == aw.LECCION_DIR


def test_si_falta_la_carpeta_de_kydo_el_chico_igual_ve_la_leccion(monkeypatch, tmp_path):
    """Un despliegue a medias no puede dejar al chico sin la lección.

    Servir el video correcto importa; servir NINGUNO es peor que el problema de marca que
    esta separación viene a arreglar."""
    monkeypatch.setattr(aw, "_es_escolar", lambda token, reg=None: True)
    monkeypatch.setattr(aw, "LECCION_DIR_KYDO", str(tmp_path / "no-existe"))
    assert aw._leccion_dir("token-de-prueba") == aw.LECCION_DIR


def test_la_decision_sale_del_MISMO_flag_que_la_marca():
    """`_es_escolar` es el único que decide de qué marca es un cuaderno: el título, el
    favicon y ahora las lecciones. Si mañana cambia, cambia UNA vez.

    Un segundo criterio en paralelo es como empiezan estas cosas: dos lugares que deciden lo
    mismo terminan discrepando, y la discrepancia se descubre en producción."""
    import inspect
    fuente = inspect.getsource(aw._leccion_dir)
    assert "_es_escolar" in fuente, (
        "`_leccion_dir` dejó de usar `_es_escolar`: ahora hay dos criterios para decidir la "
        "marca de un cuaderno, y van a discrepar")


def test_kydo_tiene_TODAS_las_lecciones():
    """Separar no puede perder contenido: si a Kydo le falta una, el chico toca «¿Cómo es?»
    y no pasa nada — y eso no avisa por ningún lado."""
    if not os.path.isdir(aw.LECCION_DIR_KYDO):
        return
    ct3d = {f for f in os.listdir(aw.LECCION_DIR) if f.endswith(".mp4")}
    kydo = {f for f in os.listdir(aw.LECCION_DIR_KYDO) if f.endswith(".mp4")}
    faltan = sorted(ct3d - kydo)
    assert not faltan, "a Kydo le faltan %d lecciones: %s" % (len(faltan), faltan[:5])
