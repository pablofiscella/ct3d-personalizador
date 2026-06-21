#!/usr/bin/env python3
"""Exporta el SPEC del generador a JSON, para que el preview en vivo (canvas)
use EXACTAMENTE el mismo mapa de coordenadas que el render de Pillow."""
import json, os
from generador import SPEC, W, H

# metadatos del formulario (los campos que llena el cliente)
FORM = [
    {"var": "nombre",   "label": "Nombre del cumpleañero/a", "default": "Tomás"},
    {"var": "fecha",    "label": "Fecha",                    "default": "Sábado 12 de julio"},
    {"var": "hora",     "label": "Hora",                     "default": "16:00 hs"},
    {"var": "lugar",    "label": "Lugar",                    "default": "Salón Los Robles"},
    {"var": "telefono", "label": "Teléfono para confirmar",  "default": "11-5555-5555"},
]

# mapa fuente-archivo -> familia CSS / peso (para @font-face en el navegador)
FONTS = {
    "Poppins-Medium.ttf":   {"family": "Poppins",      "weight": 500},
    "Fredoka-VF.ttf":       {"family": "Fredoka",      "weight": 400, "variable": True},
    "DancingScript-VF.ttf": {"family": "DancingScript", "weight": 400, "variable": True},
    "Pacifico-Regular.ttf": {"family": "Pacifico",     "weight": 400},
    "Baloo2-VF.ttf":        {"family": "Baloo2",       "weight": 400, "variable": True},
}

spec = dict(SPEC)
spec["form"] = FORM
spec["fonts"] = FONTS

out = "/root/ct3d-personalizador/web/spec.json"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    json.dump(spec, f, ensure_ascii=False, indent=2)
print("OK ->", out)
print("  art:", len(spec["art"]), "capas | text:", len(spec["text"]), "campos | form:", len(spec["form"]))
