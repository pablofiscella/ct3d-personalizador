"""Mueve los borradores aprobados de ia_draft/ a los slots/extras que usa el pipeline."""
import json
import os
import shutil

_SLOT_PREFIJOS = ("invitacion_",)


def listar_draft(temas_dir, tema):
    d = os.path.join(temas_dir, tema, "ia_draft")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


def _edades_tema(base):
    try:
        e = json.load(open(os.path.join(base, "tema.json"), encoding="utf-8")).get("edades")
        return [int(x) for x in e] if e else [1, 2, 3]
    except Exception:
        return [1, 2, 3]


def aprobar(temas_dir, tema):
    base = os.path.join(temas_dir, tema)
    draft = os.path.join(base, "ia_draft")
    extras = os.path.join(base, "extras")
    os.makedirs(extras, exist_ok=True)
    edades = _edades_tema(base)
    movidas = []
    for nombre in listar_draft(temas_dir, tema):
        origen = os.path.join(draft, nombre)
        if nombre.startswith(_SLOT_PREFIJOS):
            # la invitación es la MISMA para todas las edades (el número lo pone el editor):
            # se generó una sola y acá se copia a cada slot invitacion_<edad>.png.
            for e in edades:
                shutil.copy(origen, os.path.join(base, "invitacion_%d.png" % e))
                movidas.append("invitacion_%d.png" % e)
            os.remove(origen)
        elif nombre.startswith("afiche_"):
            # el afiche lleva el número de edad ILUSTRADO (uno por edad) y vive en
            # DOS lugares: extras/ (lo usa la venta del kit) y la RAÍZ (el arte base
            # que muestra 'Invitación y afiche' y usa el cartel suelto). Antes solo
            # iba a extras/ → la raíz quedaba con el afiche viejo sin número y las
            # dos galerías mostraban cosas distintas (bug real, Pablo 11-jul-2026).
            shutil.copy(origen, os.path.join(extras, nombre))
            shutil.move(origen, os.path.join(base, nombre))
            movidas.append(nombre)
        else:
            shutil.move(origen, os.path.join(extras, nombre))
            movidas.append(nombre)
    return {"movidas": movidas, "n": len(movidas)}
