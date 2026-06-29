"""Mueve los borradores aprobados de ia_draft/ a los slots/extras que usa el pipeline."""
import os
import shutil

_SLOT_PREFIJOS = ("invitacion_",)


def listar_draft(temas_dir, tema):
    d = os.path.join(temas_dir, tema, "ia_draft")
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


def aprobar(temas_dir, tema):
    base = os.path.join(temas_dir, tema)
    draft = os.path.join(base, "ia_draft")
    extras = os.path.join(base, "extras")
    os.makedirs(extras, exist_ok=True)
    movidas = []
    for nombre in listar_draft(temas_dir, tema):
        origen = os.path.join(draft, nombre)
        if nombre.startswith(_SLOT_PREFIJOS):
            destino = os.path.join(base, nombre)
        else:
            destino = os.path.join(extras, nombre)
        shutil.move(origen, destino)
        movidas.append(nombre)
    return {"movidas": movidas, "n": len(movidas)}
