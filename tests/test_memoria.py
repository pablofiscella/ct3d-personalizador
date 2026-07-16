import memoria


def test_relleno_sintetico_no_usa_estrella(monkeypatch):
    """15-jul-2026, Pablo: "estrellas deja 2, no 4". Si la hoja del tema ya
    aportó una estrella REAL como uno de los `imgs` (cuaderno.
    personajes_decorativos), el relleno geométrico sintético NO puede volver
    a dibujar otra estrella — daría 2 pares de estrella (uno real + uno
    geométrico) en vez de 1 solo. Sin stickers reales disponibles (mock
    devuelve []), TODO el relleno es sintético — si alguno fuera "estrella",
    acá se vería."""
    import cuaderno
    monkeypatch.setattr(cuaderno, "personajes_decorativos", lambda *a, **k: [])
    formas_pedidas = []
    original = memoria._dibujar_forma
    def _spy(forma, size, color):
        formas_pedidas.append(forma)
        return original(forma, size, color)
    monkeypatch.setattr(memoria, "_dibujar_forma", _spy)
    imgs = memoria._imagenes_pares("safari", n=6)
    assert len(imgs) == 6
    assert "estrella" not in formas_pedidas
