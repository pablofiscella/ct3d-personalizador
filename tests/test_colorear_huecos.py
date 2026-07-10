"""El line-art de colorear no debe tener contornos ABIERTOS que dejen 'escapar' el balde
(flood-fill) y pinten todo el fondo. Bug real: la planta de abajo-izquierda de
safari/colorear_2 tenía un gap → pintarla pintaba toda la escena. _colorear_imgs ahora
cierra los huecos (clausura morfológica)."""
import cuaderno


def _fill_frac(img, fx, fy, res=760):
    """Fracción del canvas que rellenaría el balde arrancando en (fx,fy) relativo."""
    g = img.convert("L").resize((res, res))
    px = g.load()
    W, H = g.size
    sx, sy = int(W * fx), int(H * fy)
    if px[sx, sy] < 90:
        return 0.0                       # cayó sobre una línea
    vis = bytearray(W * H)
    st = [(sx, sy)]
    vis[sy * W + sx] = 1
    n = 0
    while st:
        x, y = st.pop()
        n += 1
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < W and 0 <= ny < H and not vis[ny * W + nx] and px[nx, ny] >= 90:
                vis[ny * W + nx] = 1
                st.append((nx, ny))
    return 100.0 * n / (W * H)


def test_planta_abajo_izquierda_no_fuga_el_balde():
    """La hoja/planta de abajo-izquierda de safari/colorear_2 se rellena acotada (no derrama
    a todo el fondo). Antes del fix llenaba ~48% del canvas; con los huecos cerrados, <8%."""
    imgs = cuaderno._colorear_imgs("safari")
    assert len(imgs) >= 2
    frac = _fill_frac(imgs[1], 0.10, 0.82)
    assert frac < 8.0, f"la planta sigue fugando el balde: llena {frac:.0f}% del canvas"


def test_cerrar_huecos_no_engorda_de_mas():
    """El cierre de huecos no debe empastar el dibujo: la tinta no crece más de ~5 puntos."""
    from PIL import Image
    raw = Image.open(f"{cuaderno.TEMAS}/safari/extras/colorear_2.png").convert("RGBA")
    bg = Image.new("RGBA", raw.size, (255, 255, 255, 255))
    bg.alpha_composite(raw)
    antes = bg.convert("L").point(lambda v: 0 if v < 165 else 255)
    desp = cuaderno._cerrar_huecos_lineart(antes.copy())
    ink = lambda g: 100.0 * sum(1 for p in g.getdata() if p < 90) / (g.size[0] * g.size[1])
    assert ink(desp) - ink(antes) < 5.0
