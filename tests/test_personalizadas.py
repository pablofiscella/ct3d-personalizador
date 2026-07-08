"""BASE DE PERSONALIZACIÓN (Pablo, 10-jul-2026): las imágenes que cambian con el
editor de compra están declaradas en productos.PERSONALIZADAS. Este guardián
asegura que la base nunca quede desincronizada del editor real:
- cada tipo declarado existe en TIPOS;
- cada campo declarado lo CAPTURA el editor de ese tipo (si no, el motor jamás
  recibiría ese dato y la personalización prometida no ocurriría en la compra)."""
import productos


def test_tipos_declarados_existen():
    for tipo in productos.PERSONALIZADAS:
        assert tipo in productos.TIPOS, tipo


def test_campos_declarados_los_captura_el_editor():
    for tipo, piezas in productos.PERSONALIZADAS.items():
        campos_editor = set(productos.TIPOS[tipo].get("campos") or [])
        for pieza, campos in piezas.items():
            faltan = [c for c in campos if c not in campos_editor]
            assert not faltan, "%s/%s declara campos que el editor no pide: %s" % (
                tipo, pieza, faltan)


def test_tipos_con_nombre_estan_declarados():
    # todo tipo cuyo editor pide 'nombre' debe estar en la base (o ser de los
    # que lo ignoran a propósito: piezas de fiesta sin personalización)
    sin_nombre_a_proposito = {"antifaces", "memoria", "papertoys", "babyshower",
                              "libro-audio", "stl-medalla", "stl-topper",
                              "stl-trofeo", "stl-cortante", "stl-pack"}
    for tipo, spec in productos.TIPOS.items():
        if "nombre" in (spec.get("campos") or []):
            assert tipo in productos.PERSONALIZADAS or tipo in sin_nombre_a_proposito, tipo


def test_galeria_piezas_espeja_las_reales():
    """La galería 'Piezas del kit' (servicio._PIEZAS_EDAD/_UNIV) debe mostrar
    TODAS las piezas reales del kit — antes una lista fija se desincronizó y
    ocultaba base_torta/topper_palito (bug de Pablo 11-jul-2026)."""
    import servicio
    assert servicio.Handler._PIEZAS_EDAD == list(productos._EXTRAS_POR_EDAD)
    assert servicio.Handler._PIEZAS_UNIV == list(productos._EXTRAS_UNIVERSAL)
