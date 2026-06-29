from PIL import Image
from ia_kit import cajita


def _art():
    return Image.new("RGBA", (64, 64), (200, 40, 40, 255))   # arte opaco de prueba


def test_red_tiene_las_6_caras_decoradas():
    out = cajita.armar_cajita(_art(), {"ink": "#4A4A4A"}, lado=40)
    assert out.mode == "RGBA"
    C, pad = 40, 14
    assert out.size == (pad * 2 + 3 * C, pad * 2 + 4 * C)   # cruz 3x4 + padding para solapas
    # las 6 caras de la cruz están pintadas (centro opaco)
    for (r, c) in cajita._CARAS:
        cx, cy = pad + c * C + C // 2, pad + r * C + C // 2
        assert out.getpixel((cx, cy))[3] == 255, (r, c)
    # la esquina del lienzo queda transparente (no es parte de la red)
    assert out.getpixel((0, 0))[3] == 0


def test_dibuja_lineas_y_solapas():
    out = cajita.armar_cajita(_art(), {"ink": "#222222"}, lado=60)
    ink = sum(1 for p in out.getdata() if p[3] == 255 and max(p[:3]) < 60)
    blanco_solapa = sum(1 for p in out.getdata() if p[3] == 255 and min(p[:3]) > 240)
    assert ink > 0           # hay líneas de doblez/corte (tinta)
    assert blanco_solapa > 0  # hay solapas blancas para pegar
