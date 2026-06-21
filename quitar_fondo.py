#!/usr/bin/env python3
"""
Quita el fondo cuadriculado (gris/blanco) "horneado" en las imagenes.
- detecta pixeles tipo-fondo: desaturados (gris/blanco) y claros.
- protect=True: solo borra los conectados al borde (preserva interiores
  claros del dibujo, ej. cuerpo del elefante, panza del leon).
- protect=False: borra todos los tipo-fondo (para marcos/hojas sin
  interiores claros grandes).
"""
import os, sys
from PIL import Image, ImageChops

DESAT_MAX = 40   # max-min <= esto  => gris/desaturado
BRIGHT_MIN = 140 # min >= esto      => claro (cubre gris 198 y blanco 255)

def bg_mask_bytes(im):
    r, g, b = im.convert("RGB").split()
    mx = ImageChops.lighter(ImageChops.lighter(r, g), b)
    mn = ImageChops.darker(ImageChops.darker(r, g), b)
    diff = ImageChops.subtract(mx, mn)
    desat = diff.point(lambda v: 255 if v <= DESAT_MAX else 0)
    bright = mn.point(lambda v: 255 if v >= BRIGHT_MIN else 0)
    mask = ImageChops.multiply(desat, bright)  # 255 donde es tipo-fondo
    return mask.tobytes(), im.width, im.height

def remove_bg(src, protect=True):
    im = (Image.open(src) if isinstance(src, str) else src).convert("RGBA")
    w, h = im.size
    mask, _, _ = bg_mask_bytes(im)
    mask = bytearray(mask)          # 255 = tipo-fondo
    remove = bytearray(w * h)       # 1 = borrar

    if protect:
        stack = []
        def seed(i):
            if mask[i] and not remove[i]:
                remove[i] = 1; stack.append(i)
        for x in range(w):
            seed(x); seed((h - 1) * w + x)
        for y in range(h):
            seed(y * w); seed(y * w + w - 1)
        while stack:
            i = stack.pop()
            x = i % w; y = i // w
            if x + 1 < w:
                j = i + 1
                if mask[j] and not remove[j]: remove[j] = 1; stack.append(j)
            if x - 1 >= 0:
                j = i - 1
                if mask[j] and not remove[j]: remove[j] = 1; stack.append(j)
            if y + 1 < h:
                j = i + w
                if mask[j] and not remove[j]: remove[j] = 1; stack.append(j)
            if y - 1 >= 0:
                j = i - w
                if mask[j] and not remove[j]: remove[j] = 1; stack.append(j)
    else:
        for i in range(w * h):
            if mask[i]: remove[i] = 1

    # construir alpha: 0 donde remove, sino conservar
    a = im.getchannel("A")
    abytes = bytearray(a.tobytes())
    for i in range(w * h):
        if remove[i]: abytes[i] = 0
    im.putalpha(Image.frombytes("L", (w, h), bytes(abytes)))
    return im

def remove_checker(src):
    """Quita el cuadriculado gris/blanco 'neutro' (incluso los huecos encerrados,
    ej. el agujero de un número). Conserva lo cálido (crema) y lo de color.
    src puede ser ruta o un PIL.Image."""
    from PIL import ImageChops
    im = Image.open(src) if isinstance(src, str) else src
    im = im.convert("RGBA")
    w, h = im.size
    r, g, b = im.convert("RGB").split()
    mx = ImageChops.lighter(ImageChops.lighter(r, g), b)
    mn = ImageChops.darker(ImageChops.darker(r, g), b)
    diff = ImageChops.subtract(mx, mn)
    neutral = diff.point(lambda v: 255 if v <= 10 else 0)   # R≈G≈B
    bright = mn.point(lambda v: 255 if v >= 150 else 0)
    mask = ImageChops.multiply(neutral, bright).tobytes()
    ab = bytearray(im.getchannel("A").tobytes())
    for i in range(w * h):
        if mask[i]:
            ab[i] = 0
    im.putalpha(Image.frombytes("L", (w, h), bytes(ab)))
    bb = im.getbbox()
    return im.crop(bb) if bb else im

def ya_transparente(im):
    """True si la imagen ya tiene bastante transparencia real (no hay que recortar)."""
    im = im.convert("RGBA")
    a = im.getchannel("A").tobytes()
    n = len(a)
    trans = sum(1 for i in range(0, n, max(1, n // 4000)) if a[i] < 20)
    return trans > (n // max(1, n // 4000)) * 0.05

if __name__ == "__main__":
    OUT = "/root/ct3d-personalizador/recortes"
    os.makedirs(OUT, exist_ok=True)
    A = "/root/safari-img"
    # (archivo, protect)
    tests = [
        ("Gemini_Generated_Image_2k7f5m2k7f5m2k7f.png", True,  "leon.png"),
        ("Gemini_Generated_Image_iocegjiocegjioce.png", False, "arco.png"),
    ]
    for src, prot, dst in tests:
        im = remove_bg(os.path.join(A, src), protect=prot)
        # recorte a contenido
        bb = im.getbbox()
        if bb: im = im.crop(bb)
        # poner sobre crema para previsualizar el resultado real
        prev = Image.new("RGBA", im.size, (244, 239, 230, 255))
        prev.alpha_composite(im)
        im.save(os.path.join(OUT, dst))
        prev.convert("RGB").save(os.path.join(OUT, "prev_" + dst.replace(".png", ".jpg")), quality=90)
        print("OK", dst, im.size)
