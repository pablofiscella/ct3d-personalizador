"""Orquesta la generación de todas las piezas de un tema hacia ia_draft/."""
import glob
import os

import quitar_fondo
from . import catalogo
from .validate import validar_png

# invitacion es el único slot que va a la raíz temas/<tema>/; el resto va a extras/.


def _refs(tema_dir):
    # Referencias visuales para OpenAI: primero los cutouts de recortes/; si no hay,
    # el arte base del tema (invitación/afiche), que ya muestra los personajes y el estilo.
    paths = sorted(glob.glob(os.path.join(tema_dir, "recortes", "*.png")))
    if not paths:
        paths = (sorted(glob.glob(os.path.join(tema_dir, "invitacion_*.png")))
                 + sorted(glob.glob(os.path.join(tema_dir, "afiche_*.png"))))
    return [open(p, "rb").read() for p in paths[:10]]  # OpenAI admite hasta 16


def _guardar(im, draft_dir, nombre):
    os.makedirs(draft_dir, exist_ok=True)
    im.save(os.path.join(draft_dir, nombre))


def generar_tema(client, temas_dir, tema, edades, progress=None, solo=None,
                 quitar=quitar_fondo.remove_bg):
    tema_dir = os.path.join(temas_dir, tema)
    draft = os.path.join(tema_dir, "ia_draft")
    pal = catalogo.paleta_de(temas_dir, tema)
    refs = _refs(tema_dir)
    if not refs:
        raise RuntimeError(
            "El tema '%s' no tiene imágenes de referencia: subí personajes a "
            "recortes/ o cargá el arte base (invitacion_*/afiche_*)." % tema)
    # imagen maestra de estilo: ancla de consistencia, se manda como ref extra
    maestra = client.editar(refs, "Lámina maestra de estilo del tema. " +
                            catalogo.bloque_estilo(pal), catalogo._SQUARE)
    refs_full = refs + [maestra]
    generadas, errores = [], []

    def _emit(pieza, edad, ok, error=""):
        if progress:
            progress({"pieza": pieza, "edad": edad, "ok": ok, "error": error})
        (generadas if ok else errores).append({"pieza": pieza, "edad": edad, "error": error})

    for p in catalogo.PIEZAS:
        if solo and p.key not in solo:
            continue
        edades_pieza = edades if p.por_edad else [None]
        for edad in edades_pieza:
            try:
                raw = client.editar(refs_full, catalogo.prompt_de(pal, p, edad), p.size)
                im = validar_png(raw, size_esperado=tuple(int(x) for x in p.size.split("x")))
                im = im.convert("RGBA")
                if p.recorte:
                    im = quitar(im, protect=True)
                    bb = im.getbbox()
                    if bb:
                        im = im.crop(bb)
                if p.key == "invitacion":
                    nombre = "invitacion_%d.png" % int(edad)        # -> slot raíz vía aprobar
                elif p.key in catalogo.EXTRAS_POR_EDAD:
                    e = int(edad) if p.por_edad else 1              # arte único -> _1 (el motor lo reusa)
                    nombre = "%s_%d.png" % (p.key, e)              # -> extras/
                else:                                              # universal
                    nombre = "%s.png" % p.key                      # -> extras/
                _guardar(im, draft, nombre)
                _emit(p.key, edad, True)
            except Exception as e:  # una pieza que falla no frena las demás
                _emit(p.key, edad, False, str(e))
    return {"generadas": generadas, "errores": errores}
