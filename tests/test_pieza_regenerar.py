"""El mapa (tipo, idx) → arte IA del botón ♻ por pieza debe apuntar a piezas
que los generadores realmente conocen (si se renombra una pieza en fondos_ia
o corona_ia, este test avisa antes de que el botón rompa en producción)."""
import fondos_ia
import servicio


def test_mapa_regeneracion_apunta_a_piezas_reales():
    for (tipo, idx), (modulo, pieza) in servicio.Handler._FONDO_DE_PIEZA.items():
        if modulo == "fondos":
            assert pieza in fondos_ia.PIEZAS, (tipo, idx, pieza)
        else:
            import corona_ia
            assert pieza in corona_ia._PIEZAS, (tipo, idx, pieza)


def test_tipos_del_mapa_existen_en_productos():
    import productos
    tipos = {t for (t, _i) in servicio.Handler._FONDO_DE_PIEZA}
    for t in tipos:
        assert t in productos.TIPOS, t
