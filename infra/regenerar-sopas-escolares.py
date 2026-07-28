#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenera los tokens ESCOLARES para que tomen la sopa de letras por grado.

28-jul-2026. Las sopas quedan CONGELADAS dentro de `actividades/<token>/data.json`
al crear el token: el player lee ese archivo, no el motor. Así que cambiar
`_SOPA_GRADO` no toca ni un link ya entregado — hay que volver a llamar a
`crear()` con el mismo token (mismo problema y misma receta que el 25-jul con el
menú de 4°).

Cuidado central: **sólo tokens con `escolar_on`**. Regenerar uno de cumpleaños le
inyecta el contenido escolar por la edad y le cambia el producto que se vendió
(`_menu_curricular` no está gateado por el flag).

Uso:
    python3 infra/regenerar-sopas-escolares.py            # dry-run: sólo informa
    python3 infra/regenerar-sopas-escolares.py --aplicar  # regenera de verdad
    python3 infra/regenerar-sopas-escolares.py --aplicar --token abc123

Qué preserva: `crear()` usa `makedirs(exist_ok=True)`, así que no borra la carpeta
—`progreso.json` y las imágenes generadas sobreviven—. Los flags del token SÍ hay
que pasarlos de vuelta o se pierden; se re-verifican después de regenerar y el
script aborta si alguno no volvió. El progreso real del chico vive en el
localStorage de su dispositivo, no acá.
"""
import argparse
import json
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import actividades_web as aw  # noqa: E402

# Flags por token que `crear()` NO reconstruye solo (salvo nivel_max, que lee del
# data.json previo). Si alguno no vuelve después de regenerar, es una regresión.
FLAGS = ("escolar_on", "adaptativo_on", "premium_on", "requiere_cuenta",
         "revocado", "nivel_max")


def _data_path(token):
    return os.path.join(aw.ACT_DIR, token, "data.json")


def _leer(token):
    try:
        with open(_data_path(token), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _resumen_sopas(dj):
    sopas = dj.get("sopas") or []
    if not sopas:
        return "sin sopas"
    palabras = sorted({w for s in sopas for w in (s.get("lindas") or [])})
    return "%d sopas · n=%s · %d palabras distintas: %s" % (
        len(sopas), sorted({s.get("n") for s in sopas}), len(palabras),
        ", ".join(palabras[:6]) + ("…" if len(palabras) > 6 else ""))


def escolares(solo=None):
    """Tokens con `escolar_on` (los únicos que se tocan)."""
    out = []
    for token in sorted(os.listdir(aw.ACT_DIR)):
        if solo and token != solo:
            continue
        dj = _leer(token)
        if dj and dj.get("escolar_on"):
            out.append((token, dj))
    return out


def regenerar(token, dj):
    """Vuelve a armar el token conservando sus flags. Devuelve (ok, detalle)."""
    backup = _data_path(token) + ".bak-%s" % time.strftime("%Y%m%d-%H%M%S")
    shutil.copy2(_data_path(token), backup)
    data = {"nombre": dj.get("nombre"), "edad": str(dj.get("edad") or "")}
    for f in FLAGS:
        if dj.get(f) is not None:
            data[f] = dj[f]
    aw.crear(data, dj.get("tema"), token=token)
    nuevo = _leer(token)
    if not nuevo:
        return False, "no quedó data.json legible (backup en %s)" % backup
    perdidos = [f for f in FLAGS
                if dj.get(f) is not None and nuevo.get(f) != dj.get(f)]
    if perdidos:
        return False, "flags perdidos %s (backup en %s)" % (perdidos, backup)
    return True, _resumen_sopas(nuevo)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--aplicar", action="store_true",
                    help="regenerar de verdad (sin esto sólo informa)")
    ap.add_argument("--token", help="regenerar un solo token")
    args = ap.parse_args()

    tokens = escolares(args.token)
    if not tokens:
        print("No hay tokens con escolar_on que regenerar.")
        return 0

    print("%d token(s) escolares%s\n" % (len(tokens), "" if args.aplicar else " (DRY-RUN)"))
    fallados = []
    for token, dj in tokens:
        grado = "?"
        try:
            grado = int(str(dj.get("edad")).strip()) - 5
        except (TypeError, ValueError):
            pass
        print("· %-22s %s° (edad %s) tema=%s" % (token, grado, dj.get("edad"), dj.get("tema")))
        print("    antes:   %s" % _resumen_sopas(dj))
        if not args.aplicar:
            continue
        try:
            ok, detalle = regenerar(token, dj)
        except Exception as e:                      # noqa: BLE001 — informar y seguir
            ok, detalle = False, "excepción: %s" % e
        print("    después: %s" % detalle)
        if not ok:
            fallados.append((token, detalle))

    if not args.aplicar:
        print("\nDry-run: no se tocó nada. Repetí con --aplicar para regenerar.")
        return 0
    if fallados:
        print("\n%d token(s) CON PROBLEMAS:" % len(fallados))
        for token, detalle in fallados:
            print("  · %s — %s" % (token, detalle))
        return 1
    print("\nListo: %d token(s) regenerados y con sus flags intactos." % len(tokens))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
