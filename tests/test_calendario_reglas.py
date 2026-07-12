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


def test_mes_hoja_usa_el_fondo_de_su_grupo(tmp_path, monkeypatch):
    """El render en vivo (tarjetas del dash / piezas del kit) debe usar la MISMA
    resolución que el editor: fondo6.png + base6 para los meses de 6 filas,
    fondo.png + base para el resto. Bug real: las tarjetas mostraban otra cosa
    que lo que se armaba en el editor."""
    import json
    from PIL import Image
    monkeypatch.setattr(calendario, "TEMAS", str(tmp_path))
    d = tmp_path / "t1" / "calendario"
    d.mkdir(parents=True)
    Image.new("RGB", (1492, 1054), (0, 0, 255)).save(d / "fondo.png")    # azul → 5 filas
    Image.new("RGB", (1492, 1054), (255, 0, 0)).save(d / "fondo6.png")   # rojo → 6 filas
    json.dump({"anyo": "2026",
               "base":  {"days": {"x": 287, "y": 795, "spacingH": 110, "spacingV": 68}},
               "base6": {"days": {"x": 300, "y": 780, "spacingH": 110, "spacingV": 60}},
               "meses": {}}, open(d / "layout.json", "w"))
    ene = calendario.mes_hoja(1, 2026, (0, 0, 0), "t1").convert("RGB")   # 5 filas
    mar = calendario.mes_hoja(3, 2026, (0, 0, 0), "t1").convert("RGB")   # 6 filas
    # el arte se pastea centrado (y≈439..1315); muestrear una esquina sin texto
    px_e = ene.getpixel((30, 460))
    px_m = mar.getpixel((30, 460))
    assert px_e[2] > 200 and px_e[0] < 80, px_e   # enero sobre fondo AZUL
    assert px_m[0] > 200 and px_m[2] < 80, px_m   # marzo sobre fondo ROJO


def test_mes_hoja_sin_fondo6_cae_al_general(tmp_path, monkeypatch):
    import json
    from PIL import Image
    monkeypatch.setattr(calendario, "TEMAS", str(tmp_path))
    d = tmp_path / "t2" / "calendario"
    d.mkdir(parents=True)
    Image.new("RGB", (1492, 1054), (0, 0, 255)).save(d / "fondo.png")
    json.dump({"anyo": "2026", "base": {"days": {"x": 287, "y": 795}}, "meses": {}},
              open(d / "layout.json", "w"))
    mar = calendario.mes_hoja(3, 2026, (0, 0, 0), "t2").convert("RGB")
    assert mar.getpixel((30, 460))[2] > 200   # usa el fondo general
