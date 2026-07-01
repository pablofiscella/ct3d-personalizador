"""Upscale de las piezas aprobadas a resolución de impresión.

Mantiene la imagen IDÉNTICA (no regenera) y la agranda con LANCZOS. El arte
flat-vector escala limpio; no agrega detalle nuevo (para eso iría un upscaler IA).
"""
import glob
import os

from PIL import Image


def upscalar_imagen(im, objetivo=2400, maxfactor=3.0):
    """Lleva el lado largo a ~`objetivo` px (factor acotado a `maxfactor`)."""
    im = im.convert("RGBA")
    lado = max(im.size)
    f = min(maxfactor, max(1.0, objetivo / lado))
    if f <= 1.01:
        return im
    return im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)


def upscalar_draft(temas_dir, tema, objetivo=2400, progress=None):
    """Upscalea en su lugar cada PNG del staging ia_draft/ del tema. Devuelve cuántas tocó.
    `progress(nombre_archivo)` se llama antes de procesar cada una (feedback en jobs largos:
    aprobar puede tardar bastante con 14+ piezas y sin esto se ve como colgado)."""
    d = os.path.join(temas_dir, tema, "ia_draft")
    n = 0
    archivos = sorted(glob.glob(os.path.join(d, "*.png")))
    for p in archivos:
        if progress:
            progress(os.path.basename(p))
        with Image.open(p) as im:
            up = upscalar_imagen(im, objetivo)
            if up.size != im.size:
                up.save(p)
                n += 1
    return n
