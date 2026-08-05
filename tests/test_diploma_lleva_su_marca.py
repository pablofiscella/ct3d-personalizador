# -*- coding: utf-8 -*-
"""El diploma que se gana el chico lleva la marca DE SU cuaderno.

5-ago-2026, auditando el motor para el punto 5 de la separación. `certificado.py` tenía el
dominio escrito a mano —`"casatridimensional.com.ar"`— en los cuatro pies que dibuja. O sea:

    un chico terminaba el cuaderno escolar de Kydo —tres estrellas en TODOS los juegos, que
    es un rato largo de trabajo— y el diploma que se ganaba, imprimía y mostraba en la casa
    llevaba la firma del negocio de las lámparas.

CÓMO SE ENCONTRÓ, y por qué no lo cazó nada antes: el diploma se renderiza EN VIVO cuando el
player lo pide, así que no queda ningún archivo guardado donde se note. Apareció generando el
diploma de un cuaderno escolar REAL (`revision-1ro`, `escolar_on: True`) y mirando la imagen.
Ningún grep lo habría mostrado como problema: la línea se ve perfectamente razonable.

POR QUÉ ESTE TEST MIRA LO QUE SE DIBUJA Y NO EL FUENTE
──────────────────────────────────────────────────────
Un test que busque `_dominio(data)` en el archivo pasa aunque la llamada esté en una rama
que nunca se ejecuta. Acá se intercepta `ImageDraw.text` y se junta TODO lo que el generador
escribe en la imagen: si el dominio equivocado llega al papel, aparece.

Es la misma diferencia que costó el día: `/kydo/biblioteca` respondía 200 y listaba
cuadernos —el test de "¿responde?" pasaba— sólo que eran los del otro negocio.
"""
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

import certificado  # noqa: E402


def _textos_del_diploma(monkeypatch, escolar):
    """Todo lo que el generador escribe en la imagen, para un cuaderno de esa marca.

    Se usa un tema inexistente a propósito: sin fondo de IA el generador toma la rama
    liviana y el test corre en milisegundos. Las DOS ramas dibujan el pie, y hay un test
    aparte que comprueba que ninguna se quedó con el dominio escrito a mano."""
    escritos = []
    from PIL import ImageDraw
    orig = ImageDraw.ImageDraw.text

    def espia(self, xy, text, *a, **kw):
        escritos.append(text)
        return orig(self, xy, text, *a, **kw)

    monkeypatch.setattr(ImageDraw.ImageDraw, "text", espia)
    certificado.generar_certificado_logro(
        {"nombre": "Sofía", "escolar_on": escolar}, tema="__no_existe__")
    return escritos


def test_el_diploma_de_kydo_NO_firma_con_la_otra_marca(monkeypatch):
    """EL test. Es lo que el chico imprime y pega en la heladera."""
    escritos = _textos_del_diploma(monkeypatch, escolar=True)
    malas = [t for t in escritos if "casatridimensional" in str(t).lower()]
    assert not malas, (
        "el diploma de un cuaderno de Kydo lleva la marca de las lámparas: %s" % malas)
    assert any("kydo.com.ar" in str(t) for t in escritos), (
        "el diploma de Kydo no lleva ninguna marca: %s" % escritos)


def test_el_diploma_de_cumpleanos_sigue_firmando_como_siempre(monkeypatch):
    """El control. Arreglar Kydo no puede dejar sin firma al negocio que hoy sí vende."""
    escritos = _textos_del_diploma(monkeypatch, escolar=False)
    assert any("casatridimensional.com.ar" in str(t) for t in escritos), (
        "se perdió la firma del diploma de cumpleaños: %s" % escritos)
    assert not any("kydo" in str(t).lower() for t in escritos), (
        "el diploma de cumpleaños quedó firmado por Kydo")


def test_sin_la_marca_declarada_cae_a_la_tienda(monkeypatch):
    """Un cuaderno viejo cuyo `data.json` no tiene `escolar_on` es de cumpleaños: son los
    que existían antes de que Kydo existiera. Adivinar al revés le pondría la marca escolar
    a un kit de cumpleaños ya vendido."""
    escritos = _textos_del_diploma(monkeypatch, escolar=None)
    assert any("casatridimensional.com.ar" in str(t) for t in escritos), (
        "sin `escolar_on` el diploma no cae a la marca de siempre: %s" % escritos)


def test_ninguna_rama_se_quedo_con_el_dominio_escrito_a_mano():
    """Las dos ramas del generador —con fondo de IA y sin él— dibujan el pie.

    El test de arriba sólo recorre la liviana; si la otra se quedó con el texto fijo, el
    cuaderno con arte de IA —que son TODOS los que se venden— sigue firmado mal. Acá se mira
    el fuente porque es la única forma de cubrir una rama sin renderizar el arte entero."""
    import io as _io
    import re
    src = _io.open(os.path.join(RAIZ, "certificado.py"), encoding="utf-8").read()
    src = re.sub(r"(?m)^\s*#.*$", " ", src)          # sin comentarios
    dibujos = re.findall(r"dr\.text\((.*?)font=", src, re.S)
    con_dominio = [d for d in dibujos if "casatridimensional" in d]
    assert not con_dominio, (
        "quedan %d pies con el dominio escrito a mano: %s" % (len(con_dominio), con_dominio))


def test_el_dominio_sale_de_escolar_on():
    """El interruptor es el MISMO que ya decide el título de la pestaña, el favicon y la
    carpeta de lecciones. Un segundo interruptor para lo mismo es la próxima fuga."""
    assert certificado._dominio({"escolar_on": True}) == "kydo.com.ar"
    assert certificado._dominio({"escolar_on": False}) == "casatridimensional.com.ar"
    assert certificado._dominio({}) == "casatridimensional.com.ar"
    assert certificado._dominio(None) == "casatridimensional.com.ar"
