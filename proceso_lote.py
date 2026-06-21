#!/usr/bin/env python3
"""Procesa en lote: quita el fondo cuadriculado y guarda recortes limpios."""
import os
from PIL import Image
from quitar_fondo import remove_bg

A = "/root/safari-img"
OUT = "/root/ct3d-personalizador/recortes"
os.makedirs(OUT, exist_ok=True)

# (origen, protect, destino)
JOBS = [
    ("Gemini_Generated_Image_2k7f5m2k7f5m2k7f.png", True,  "leon.png"),
    ("Gemini_Generated_Image_pq904zpq904zpq90.png", True,  "jirafa.png"),
    ("Gemini_Generated_Image_dr6s4jdr6s4jdr6s.png", True,  "monito.png"),
    ("Gemini_Generated_Image_a6lgza6lgza6lgza.png", True,  "elefante.png"),
    ("Gemini_Generated_Image_bs1h4kbs1h4kbs1h.png", True,  "cebra.png"),
    ("Gemini_Generated_Image_iocegjiocegjioce.png", False, "arco.png"),
    ("Gemini_Generated_Image_qg0s71qg0s71qg0s.png", True,  "numero1.png"),
    ("Gemini_Generated_Image_gden41gden41gden.png", True,  "adornos.png"),
    ("Gemini_Generated_Image_24x2xq24x2xq24x2.png", True,  "hojas.png"),
]

for src, prot, dst in JOBS:
    im = remove_bg(os.path.join(A, src), protect=prot)
    bb = im.getbbox()
    if bb:
        im = im.crop(bb)
    im.save(os.path.join(OUT, dst))
    print(f"OK  {dst:14} {im.size}  protect={prot}")
print("Listo ->", OUT)
