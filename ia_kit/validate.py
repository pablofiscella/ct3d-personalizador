"""Valida la imagen devuelta por OpenAI antes de aceptarla."""
import io
from PIL import Image


class ImagenInvalida(Exception):
    pass


def validar_png(raw, size_esperado=None, tol=0.06):
    try:
        im = Image.open(io.BytesIO(raw))
        im.load()
    except Exception as e:
        raise ImagenInvalida("no se pudo abrir la imagen: %s" % e)
    if size_esperado:
        r_real = im.size[0] / im.size[1]
        r_esp = size_esperado[0] / size_esperado[1]
        if abs(r_real - r_esp) / r_esp > tol:
            raise ImagenInvalida(
                "ratio %.3f != esperado %.3f" % (r_real, r_esp))
    return im
