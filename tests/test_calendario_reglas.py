"""Dos reglas de configuración del calendario: meses de 5 filas (base) y de
6 filas (base6), con overrides puntuales por mes por encima de ambas.

Pedido real (jul-2026, tema espacio): los 3 meses de 6 filas necesitan otra
posición/espaciado que los 9 de 5 filas — una regla por grupo, no un ajuste
mes por mes.
"""
import calendario


def test_filas_del_mes_2026():
    # 2026 (semana lunes-primero): marzo, agosto y noviembre ocupan 6 filas.
    seis = [m for m in range(1, 13) if calendario.filas_del_mes(2026, m) >= 6]
    assert seis == [3, 8, 11]
    assert calendario.filas_del_mes(2026, 1) == 5
    assert calendario.filas_del_mes(2026, 2) == 5


def test_meses_por_filas_cubre_los_12():
    cinco = calendario.meses_por_filas(2026, 5)
    seis = calendario.meses_por_filas(2026, 6)
    assert seis == [3, 8, 11]
    assert sorted(cinco + seis) == list(range(1, 13))


def test_config_para_mes_prioridades():
    base = {"days": {"y": 817}}
    base6 = {"days": {"y": 795}}
    puntual = {"days": {"y": 700}}
    layout = {"base": base, "base6": base6, "meses": {"8": puntual}}
    # mes de 5 filas → regla general
    assert calendario.config_para_mes(layout, 2026, 1) is base
    # mes de 6 filas sin override puntual → regla de 6 filas
    assert calendario.config_para_mes(layout, 2026, 3) is base6
    # override puntual manda sobre todo
    assert calendario.config_para_mes(layout, 2026, 8) is puntual


def test_config_para_mes_sin_base6_cae_a_base():
    base = {"days": {"y": 817}}
    layout = {"base": base, "meses": {}}
    assert calendario.config_para_mes(layout, 2026, 3) is base
    assert calendario.config_para_mes(None, 2026, 3) == {}
