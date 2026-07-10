"""Tests de piezas.quitar_halo / piezas.agregar_halo (fixtures sintéticas).

Los casos reproducen los fallos reales medidos el 10-jul-2026:
- aro die-cut alcanzable desde afuera → se quita entero (sin fleco)
- bolsón de aro ATRAPADO por el trazo del troquelado → también se quita
- blanco legítimo del personaje (nube/dientes) → se conserva
- arte sin halo → no-op
- agregar_halo → contorno uniforme del grosor pedido
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import piezas  # noqa: E402


def _sticker_sintetico():
    """Personaje redondo rojo con contorno oscuro + aro blanco die-cut."""
    im = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((30, 30, 170, 170), fill=(255, 255, 255, 255))     # aro blanco
    d.ellipse((50, 50, 150, 150), fill=(220, 60, 60, 255),
              outline=(40, 20, 20, 255), width=5)                # personaje
    return im


def test_quitar_halo_saca_el_aro_y_conserva_el_personaje():
    out = piezas.quitar_halo(_sticker_sintetico())
    # el personaje (centro) queda opaco y rojo
    cx, cy = out.width // 2, out.height // 2
    r, g, b, a = out.getpixel((cx, cy))
    assert a > 200 and r > 180 and g < 120
    # el aro (borde exterior del bbox nuevo ≈ contorno) ya no tiene blanco puro
    px = out.load()
    blancos = sum(1 for x in range(out.width) for y in range(out.height)
                  if px[x, y][3] > 40 and min(px[x, y][:3]) > 230)
    assert blancos < 30, "quedó aro/fleco blanco: %d px" % blancos


def test_quitar_halo_bolson_atrapado():
    """Bolsón chico de aro ENCERRADO por el trazo del troquelado (como el que
    quedaba entre la antena y la cabeza del monstruo): también tiene que salir."""
    im = Image.new("RGBA", (200, 220), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((30, 60, 170, 200), fill=(255, 255, 255, 255))     # aro
    d.ellipse((50, 80, 150, 180), fill=(220, 60, 60, 255),
              outline=(40, 20, 20, 255), width=5)
    # bolsón blanco ANGOSTO arriba de la cabeza (como los huecos reales del
    # troquelado, que abrazan la figura), cerrado por un borde oscuro
    d.rectangle((93, 44, 107, 58), fill=(40, 20, 20, 255))
    d.rectangle((95, 46, 105, 56), fill=(255, 255, 255, 255))
    out = piezas.quitar_halo(im)
    px = out.load()
    blancos = sum(1 for x in range(out.width) for y in range(out.height)
                  if px[x, y][3] > 40 and min(px[x, y][:3]) > 230)
    assert blancos < 30, "quedó bolsón atrapado: %d px" % blancos


def test_quitar_halo_conserva_blancos_internos():
    """Una 'nube': blanca por dentro con contorno oscuro — el interior queda."""
    im = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((20, 20, 180, 180), fill=(255, 255, 255, 255),
              outline=(60, 70, 90, 255), width=5)
    out = piezas.quitar_halo(im)
    r, g, b, a = out.getpixel((out.width // 2, out.height // 2))
    assert a > 200 and min(r, g, b) > 230, "se comió el blanco del personaje"


def test_quitar_halo_noop_sin_halo():
    im = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((10, 10, 110, 110), fill=(220, 60, 60, 255),
              outline=(40, 20, 20, 255), width=5)
    antes = sum(im.getchannel("A").point(lambda v: v > 40 and 255).histogram()[255:])
    out = piezas.quitar_halo(im)
    despues = sum(out.getchannel("A").point(lambda v: v > 40 and 255).histogram()[255:])
    assert despues >= antes * 0.97, "quitó de más en arte sin halo"


def test_agregar_halo_uniforme():
    im = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse((20, 20, 100, 100), fill=(220, 60, 60, 255))
    out = piezas.agregar_halo(im, grosor=12)
    assert out.width > im.width and out.height > im.height
    cx, cy = out.width // 2, out.height // 2
    # a mitad del halo (radio personaje 40 + ~6px) tiene que haber blanco opaco
    muestras = [(cx + 46, cy), (cx - 46, cy), (cx, cy + 46), (cx, cy - 46)]
    for x, y in muestras:
        r, g, b, a = out.getpixel((x, y))
        assert a > 200 and min(r, g, b) > 230, "halo no uniforme en (%d,%d)" % (x, y)
    # y bien afuera, transparente
    assert out.getpixel((2, 2))[3] == 0
