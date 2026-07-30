# -*- coding: utf-8 -*-
"""El motor sirve DOS marcas y tiene que saber en cuál está.

Pablo, 30-jul-2026: *"esto sigue funcionando? casatridimensional?"* — abriendo el cuaderno
de su hijo desde la biblioteca y encontrándose el dominio del otro negocio.

EL MOTOR ERA EL PUNTO CIEGO. Los guardianes de marca viven en el repo de la tienda, y el
cuaderno lo sirve ESTE repo: nadie había barrido este lado. El cuaderno escolar es Kydo y
el de cumpleaños es Casatridimensional, y hasta hoy el motor mostraba Casatridimensional
siempre, aunque la familia hubiera entrado por `mi.kydo.com.ar` (que ya apuntaba acá).

EL QUE MÁS IMPORTA ES EL DE ORIGEN. `_origen_ok` sólo aceptaba casatridimensional, así que
servir el cuaderno desde Kydo lo habría hecho CARGAR bien y rechazar cada POST: el chico
juega y el progreso no se guarda, sin ningún error visible. Es lo que hace que "cambiar el
link" parezca suficiente y no lo sea.
"""
import os
import re
import sys

import pytest

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)
SERVICIO = os.path.join(_BASE, "servicio.py")


def _src():
    with open(SERVICIO, encoding="utf-8") as f:
        return f.read()


class _Headers:
    """Lo mínimo que usan los helpers: `.get("Host")`. Un dict pelado no sirve porque
    no se le puede reemplazar `.get`."""
    def __init__(self, host):
        self._h = {"Host": host}

    def get(self, k, d=None):
        return self._h.get(k, d)


def _con_host(host):
    """Una instancia de los helpers respondiendo con ese Host."""
    H = _helpers()
    h = H.__new__(H)
    h.headers = _Headers(host)
    return h


def _helpers():
    src = _src()
    trozos = []
    for nombre in ("_es_kydo", "_marca", "_biblioteca_url"):
        m = re.search(r"    def %s\(self\):.*?(?=\n    def )" % nombre, src, re.S)
        assert m, "no encontré %s en servicio.py" % nombre
        trozos.append(m.group(0))
    ns = {}
    exec("class H:\n" + "".join(trozos), ns)
    return ns["H"]


@pytest.mark.parametrize("host,marca", [
    ("mi.kydo.com.ar", "Kydo"),
    ("kydo.com.ar", "Kydo"),
    ("www.kydo.com.ar", "Kydo"),
    ("mi.kydo.com.ar:2053", "Kydo"),          # Cloudflare con puerto alternativo
    ("MI.KYDO.COM.AR", "Kydo"),
    ("kit.casatridimensional.com.ar", "Casatridimensional"),
    ("casatridimensional.com.ar", "Casatridimensional"),
    ("nokydo.com.ar", "Casatridimensional"),  # no alcanza con que diga "kydo" adentro
    ("", "Casatridimensional"),
])
def test_la_marca_sale_del_dominio(host, marca):
    assert _con_host(host)._marca() == marca, host


def test_la_biblioteca_es_la_de_su_marca():
    for host, esperado in (("mi.kydo.com.ar", "kydo.com.ar"),
                           ("kit.casatridimensional.com.ar", "casatridimensional.com.ar")):
        url = _con_host(host)._biblioteca_url()
        assert esperado in url, (host, url)
        if esperado == "kydo.com.ar":
            assert "casatridimensional" not in url


def test_el_origen_de_kydo_esta_permitido():
    """EL importante: sin esto el cuaderno abre y el progreso NO se guarda, en silencio."""
    src = _src()
    i = src.index("def _origin_ok")
    cuerpo = src[i:src.index("\n    def ", i + 10)]
    assert "kydo.com.ar" in cuerpo, \
        "el motor rechazaría los POST del cuaderno servido desde Kydo"
    assert "casatridimensional.com.ar" in cuerpo, "no se puede perder el dominio viejo"


def test_la_csp_permite_las_dos_marcas():
    src = _src()
    m = re.search(r'"frame-ancestors[^\n]*(\n[^\n]*)?', src)
    assert m and "kydo.com.ar" in m.group(0), "la CSP dejaría a Kydo afuera"


def test_el_cartel_del_candado_no_tiene_la_marca_escrita_a_mano():
    """Era el texto que Pablo veía: «...desde su cuenta en Casatridimensional» en un
    cuaderno de Kydo."""
    src = _src()
    i = src.index("def _act_deny")
    cuerpo = src[i:src.index("\n    def ", i + 10)]
    assert "en Casatridimensional." not in cuerpo, "la marca quedó escrita a mano"
    assert "_marca()" in cuerpo and "_biblioteca_url()" in cuerpo


def test_la_raiz_manda_a_la_tienda_de_su_marca():
    """Entrar a mi.kydo.com.ar a secas y aterrizar en casatridimensional."""
    src = _src()
    i = src.index('if path == "/":')
    cuerpo = src[i:i + 700]
    assert "_es_kydo()" in cuerpo, "la raíz sigue mandando a todos al mismo lado"
    assert "https://kydo.com.ar" in cuerpo
