"""Orquesta la generación de todas las piezas de un tema hacia ia_draft/."""
import glob
import os

import quitar_fondo
from . import catalogo
from .validate import validar_png

_SLOTS = {"invitacion", "afiche"}   # van a temas/<tema>/ (no a extras/)


def _refs(tema_dir):
    paths = sorted(glob.glob(os.path.join(tema_dir, "recortes", "*.png")))
    return [open(p, "rb").read() for p in paths]


def _guardar(im, draft_dir, nombre):
    os.makedirs(draft_dir, exist_ok=True)
    im.save(os.path.join(draft_dir, nombre))


def generar_tema(client, temas_dir, tema, edades, progress=None, solo=None,
                 quitar=quitar_fondo.remove_bg):
    tema_dir = os.path.join(temas_dir, tema)
    draft = os.path.join(tema_dir, "ia_draft")
    pal = catalogo.paleta_de(temas_dir, tema)
    refs = _refs(tema_dir)
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
                if p.key in _SLOTS or p.por_edad:
                    nombre = "%s_%d.png" % (p.key, edad)
                else:
                    nombre = "%s.png" % p.key
                _guardar(im, draft, nombre)
                _emit(p.key, edad, True)
            except Exception as e:  # una pieza que falla no frena las demás
                _emit(p.key, edad, False, str(e))
    return {"generadas": generadas, "errores": errores}
