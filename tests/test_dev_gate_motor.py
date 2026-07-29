"""Qué protege la puerta del espejo DEV en el motor — y sobre todo, qué NO.

Historia real (28-jul-2026): la puerta arrancó cubriendo TODO el motor y rompió, una por
una, las cosas que el usuario sí quería hacer. Primero abrir el cuaderno (dos veces),
después la VOZ de las actividades (el player la pide a `/tts` y le contestaba 401), y
venían las miniaturas de la tienda y las descargas.

Estos tests fijan el modelo que quedó: la clave del dev cuida el PANEL, y nada más. Todo
lo otro que sirve el motor o cuelga de un token de 16 caracteres con permiso firmado, o ya
pide la API key.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import servicio


def test_el_panel_pide_la_clave():
    for p in ["/dash", "/dash/ia-estado", "/entrar?key=x", "/api/generar", "/tipos"]:
        assert servicio.dev_path_protegido(p), p


def test_el_cuaderno_no_pide_la_clave():
    """El link lo tiene la familia y ya trae token + permiso firmado."""
    for p in ["/act/knhybBFbif9UTypq/", "/act/abc/progreso", "/armar/xyz/", "/leer/xyz/",
              "/al/xyz/"]:
        assert not servicio.dev_path_protegido(p), p


def test_la_voz_no_pide_la_clave():
    """`/tts` es la narración de las consignas. Con 401 acá, las actividades tienen
    sonido pero se quedan mudas — que es exactamente lo que reportó Pablo."""
    assert not servicio.dev_path_protegido("/tts")


def test_las_miniaturas_y_la_demo_no_piden_la_clave():
    """Las pide el <img> de la tienda y el botón "Probalo gratis", desde el navegador."""
    for p in ["/preview?tipo=kit&tema=safari", "/probar/rompecabezas/safari",
              "/cliente-bg.png", "/descarga/abc.zip"]:
        assert not servicio.dev_path_protegido(p), p


def test_sin_ruta_no_decide():
    assert servicio.dev_path_protegido("") is False
    assert servicio.dev_path_protegido(None) is False
