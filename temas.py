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
    return {"id": tema_id, "nombre": cfg.get("nombre", tema_id),
            "edades": cfg.get("edades", [1, 2, 3]), "specs": specs}

def existe(tema_id):
    return os.path.isfile(os.path.join(TEMAS_DIR, tema_id, "tema.json"))
