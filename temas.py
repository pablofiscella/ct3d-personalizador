#!/usr/bin/env python3
"""Carga de temáticas desde disco (temas/<id>/tema.json).
Convierte la config en specs que entiende el motor (generador.render)."""
import os, json, copy

BASEDIR = os.path.dirname(os.path.abspath(__file__))
TEMAS_DIR = os.path.join(BASEDIR, "temas")
CREAM = (244, 239, 230)

def _hex_to_rgb(h):
    if isinstance(h, (list, tuple)):
        return tuple(h)
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def list_temas():
    out = []
    if not os.path.isdir(TEMAS_DIR):
        return out
    for d in sorted(os.listdir(TEMAS_DIR)):
        cfg = os.path.join(TEMAS_DIR, d, "tema.json")
        if os.path.isfile(cfg):
            try:
                j = json.load(open(cfg, encoding="utf-8"))
                out.append({"id": d, "nombre": j.get("nombre", d),
                            "edades": j.get("edades", [1, 2, 3]),
                            "piezas": list(j.get("piezas", {}).keys())})
            except Exception:
                pass
    return out

# Extras que llevan texto personalizable (editable con el editor). Se inyectan como spec
# (campo "nombre" + layout_file) para reusar el editor genérico. Posición por defecto; el
# admin la ajusta y se guarda en temas/<tema>/layouts/<pieza>.json. El nombre del cliente
# se completa al customizar (tpl con {nombre}).
_EXTRAS_TEXTO = {
    "afiche":                  {"tpl": "FELIZ CUMPLE {nombre}",   "x": 0.5, "y": 0.86, "size": 120, "maxw": 0.58, "bg": "extras/afiche_{edad}.png",              "size_px": [1536, 2176]},
    "banderin":                {"tpl": "¡FELIZ CUMPLE {nombre}!", "x": 0.5, "y": 0.50, "size": 150, "maxw": 0.70, "bg": "extras/banderin.png",                   "size_px": [1024, 1024]},
    "cajita_sorpresa":         {"tpl": "FELIZ CUMPLE {nombre}",   "x": 0.5, "y": 0.50, "size": 130, "maxw": 0.70, "bg": "extras/cajita_sorpresa_{edad}.png",      "size_px": [1024, 1024]},
    "decoracion_sorbetes":     {"tpl": "{nombre}",                 "x": 0.5, "y": 0.50, "size": 130, "maxw": 0.55, "bg": "extras/decoracion_sorbetes_{edad}.png", "size_px": [1024, 1024]},
    # la tarjeta de agradecimiento lleva 3 líneas de texto apiladas (Pablo 9-jul-2026)
    "tarjetas_agradecimiento": {"bg": "extras/tarjetas_agradecimiento.png", "size_px": [1536, 2176],
        "campos": [
            {"id": "texto1", "tpl": "¡Gracias por venir!", "x": 0.5, "y": 0.34, "size": 110, "maxw": 0.82},
            {"id": "texto2", "tpl": "",                     "x": 0.5, "y": 0.50, "size": 88,  "maxw": 0.82},
            {"id": "texto3", "tpl": "",                     "x": 0.5, "y": 0.64, "size": 88,  "maxw": 0.82},
        ]},
}

def _inyectar_specs_texto(specs, tdir):
    inv = specs.get("invitacion", {})
    nf = next((f for f in inv.get("text", []) if f.get("id") == "nombre"), {})
    font = nf.get("font", "Baloo2-VF.ttf")
    wght = nf.get("wght")
    color = nf.get("color") if isinstance(nf.get("color"), (list, tuple)) else (74, 74, 74)
    for base, cfg in _EXTRAS_TEXTO.items():
        if base in specs:           # el tema ya lo declara explícitamente -> respetar
            continue
        if cfg.get("campos"):       # pieza con VARIOS campos de texto (ej: tarjeta con 3)
            text = [{"id": c["id"], "tpl": c.get("tpl", ""), "x": c["x"], "y": c["y"],
                     "size": c["size"], "maxw": c.get("maxw", 0.8), "anchor": "mm",
                     "font": font, "wght": wght, "color": tuple(color),
                     "editable": True, "toggleable": bool(c.get("toggleable", True))}
                    for c in cfg["campos"]]
        else:                       # pieza con 1 solo campo (formato original)
            text = [{"id": "nombre", "tpl": cfg["tpl"], "x": cfg["x"], "y": cfg["y"],
                     "size": cfg["size"], "maxw": cfg["maxw"], "anchor": "mm",
                     "font": font, "wght": wght, "color": tuple(color), "editable": True}]
        specs[base] = {
            "_dir": tdir, "bg": CREAM, "art": [], "size": list(cfg["size_px"]),
            "bgimage": cfg["bg"], "layout_file": "layouts/%s.json" % base,
            "text": text,
        }

def cargar_tema(tema_id):
    tdir = os.path.join(TEMAS_DIR, tema_id)
    cfg = json.load(open(os.path.join(tdir, "tema.json"), encoding="utf-8"))
    specs = {}
    for pieza, p in cfg.get("piezas", {}).items():
        spec = copy.deepcopy(p)
        spec["_dir"] = tdir
        spec.setdefault("bg", CREAM)
        spec["art"] = spec.get("art", [])
        for f in spec.get("text", []):
            if "color" in f:
                f["color"] = _hex_to_rgb(f["color"])
        specs[pieza] = spec
    _inyectar_specs_texto(specs, tdir)   # extras con texto editable
    return {"id": tema_id, "nombre": cfg.get("nombre", tema_id),
            "edades": cfg.get("edades", [1, 2, 3]), "specs": specs}

def existe(tema_id):
    return os.path.isfile(os.path.join(TEMAS_DIR, tema_id, "tema.json"))
