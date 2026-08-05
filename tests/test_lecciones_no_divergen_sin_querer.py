# -*- coding: utf-8 -*-
"""Las dos carpetas de lecciones pueden divergir — pero A PROPÓSITO, no por descuido.

4-ago-2026, y esto sale de un error mío que llegó a producción.

Al separar las lecciones por sistema copié `lecciones_video/` → `lecciones_video_kydo/`
ANTES de que estuviera mergeado el arreglo que sacaba la firma «Casatridimensional · Mis
Desafíos» del cierre. Resultado: el arreglo terminó en la carpeta de **cumpleaños** y la de
**Kydo** se quedó con la firma. Justo al revés de lo que correspondía, y en producción.

Tercera vez en el mismo día que copiar antes de arreglar duplica el bug. Las dos anteriores
las cazó un test; ésta la cacé mirando un fotograma del video servido, porque **no había
ningún test que comparara el CONTENIDO** — el que había escrito verificaba que a Kydo no le
faltara ninguna lección, no que fueran las correctas. Faltar y estar mal no son lo mismo.

LA REGLA QUE CUIDA ESTE ARCHIVO, y ojo con leerla mal: las dos carpetas **pueden** divergir,
porque son dos sistemas distintos y ése es el punto de la separación. Lo que no puede pasar
es que diverjan **sin que nadie lo haya decidido**. Por eso cada divergencia se declara acá
abajo con su motivo: si aparece una que no está declarada, es un descuido, y este test lo
dice antes de que llegue a la pantalla de un chico.
"""
import hashlib
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CT3D = os.path.join(BASE, "lecciones_video")
KYDO = os.path.join(BASE, "lecciones_video_kydo")

# Las divergencias DECIDIDAS. Cada una con el motivo por el que existe.
#
# Está vacío a propósito: hoy las dos carpetas tienen el mismo contenido. El día que Kydo
# quiera una lección distinta de la de cumpleaños —que es exactamente para lo que se
# separaron— se agrega acá con el motivo, y este test la deja pasar.
DIVERGENCIAS_A_PROPOSITO = {
    # "lec_ejemplo.mp4": "Kydo la regrabó el DD-mmm-AAAA porque ...",
}


def _hash(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def test_ninguna_leccion_diverge_sin_haberlo_decidido():
    """EL test. Es el que faltaba cuando mandé a producción la versión con la firma."""
    if not (os.path.isdir(CT3D) and os.path.isdir(KYDO)):
        return
    sorpresas = []
    for f in sorted(x for x in os.listdir(CT3D) if x.endswith(".mp4")):
        otro = os.path.join(KYDO, f)
        if not os.path.exists(otro) or f in DIVERGENCIAS_A_PROPOSITO:
            continue
        if _hash(os.path.join(CT3D, f)) != _hash(otro):
            sorpresas.append(f)
    assert not sorpresas, (
        "estas lecciones difieren entre los dos sistemas y nadie lo declaró: %s.\n"
        "Si la diferencia es a propósito, agregala a DIVERGENCIAS_A_PROPOSITO con el "
        "motivo. Si no, una de las dos carpetas quedó con una versión vieja — que es "
        "exactamente lo que pasó el 4-ago-2026 con la firma de la marca." % sorpresas)


def test_las_divergencias_declaradas_existen_de_verdad():
    """Una entrada que sobra deja de proteger ese archivo en silencio.

    Es el mismo cuidado que con cualquier lista blanca: la que nadie limpia termina tapando
    justo el caso que había que ver."""
    if not os.path.isdir(CT3D):
        return
    hay = {x for x in os.listdir(CT3D) if x.endswith(".mp4")}
    sobran = sorted(set(DIVERGENCIAS_A_PROPOSITO) - hay)
    assert not sobran, (
        "DIVERGENCIAS_A_PROPOSITO nombra lecciones que ya no existen: %s. Sacalas, o "
        "dejan de estar comparadas sin que nadie se entere." % sobran)


def test_hay_lecciones_que_comparar():
    """El control: si las carpetas se mueven, el test de arriba pasaría por vacío."""
    if not os.path.isdir(KYDO):
        return
    assert len([x for x in os.listdir(KYDO) if x.endswith(".mp4")]) >= 300, (
        "esperaba las ~396 lecciones de Kydo y hay menos: si se movieron de carpeta, este "
        "test dejó de proteger nada")
