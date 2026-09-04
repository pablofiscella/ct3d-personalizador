# -*- coding: utf-8 -*-
"""Qué hizo el chico en CADA TARJETA del cuaderno, para el panel de la maestra.

POR QUÉ EXISTE (Pablo, 04-sep-2026): *"Me gustarían dos cosas: una es el desglose de qué
es lo que hizo en cada tarjeta"*. El panel del docente muestra hoy el ROLLUP por materia
—«Matemática 11 de 25»—, que sirve para ver el curso de un vistazo pero no contesta la
pregunta que una maestra hace cuando se sienta con un chico: *¿qué practicó, y cómo le
fue?*

EL DATO YA ESTABA GUARDADO Y NADIE LO DIBUJABA. `progreso.json` viene anotando, por
actividad, el escalón, las estrellas, el sello y los días en que la resolvió bien:

    "niveles": {"sopa": 2}                                       ← escalón 1..3
    "estado": {"stars": {"sopa": 3},
               "dominio": {"sopa": {"dias": ["2026-07-01", "2026-07-02"],
                                    "sello": "dominado", "repasarEn": 0}}}

Este módulo NO decide nada nuevo: lee lo guardado y le pone nombre. Toda la lógica de
cuándo algo pasa a dominado sigue viviendo en el player (`motor_adaptativo.js`), que es
quien la mide. Duplicar esa decisión acá sería tener dos motores de dominio que se van a
separar con el primer cambio.

LOS TRES ESTADOS QUE LE IMPORTAN A LA MAESTRA, y son tres y no dos:

    sin_datos    la tarjeta está en el cuaderno y el chico NUNCA la abrió
    practicando  la abrió y todavía no la resuelve bien en días distintos
    dominado /   la resolvió bien en días distintos (`consolidado` es el escalón de arriba)
    consolidado

«No lo sabe» y «todavía no lo vio» son cosas distintas, y para armar una clase la
diferencia es todo: una pide volver a explicar, la otra pide dar la hoja.
"""
import json
import os

import actividades_web as aw
import saberes
from actividades_categorias import categoria_de

#: Los sellos que el player escribe, del más flojo al más firme. El orden es el que usa el
#: panel para ordenar «lo que peor va primero», así que vive acá y no repetido en la vista.
SELLOS = ("sin_datos", "practicando", "dominado", "consolidado")

ETIQUETA_SELLO = {
    "sin_datos": "No la abrió",
    "practicando": "Practicando",
    "dominado": "Dominado",
    "consolidado": "Consolidado",
}

def _juego_a_saberes():
    """{id de actividad: [ids de saber que mide]} — el inverso de `SABERES[x]["juegos"]`.

    Es el mismo mapa que `motor_adaptativo.js` arma en el navegador (`_JUEGO_A_SABERES`).
    Acá se rearma desde `saberes.SABERES`, que es la misma fuente, así que no hay dos
    listas para mantener: si un saber cambia de juego, cambian los dos a la vez.
    """
    out = {}
    for sid, s in saberes.SABERES.items():
        for j in s.get("juegos") or []:
            out.setdefault(j, []).append(sid)
    return out


def _tarjeta(item, perfil, j2s, grado):
    """Una tarjeta del cuaderno con lo que el chico hizo en ella."""
    jid = item["id"]
    est = perfil.get("estado") or {}
    dom = (est.get("dominio") or {}).get(jid) or {}
    dias = [d for d in (dom.get("dias") or []) if d]
    estrellas = int((est.get("stars") or {}).get(jid) or 0)
    escalon = int((perfil.get("niveles") or {}).get(jid) or 1)
    sello = dom.get("sello") or ""

    # SIN SELLO NO SIGNIFICA MAL: significa que no la abrió. El player escribe la entrada de
    # `dominio` recién cuando el chico resuelve algo, así que la ausencia es la señal de
    # «nunca la tocó» — y es justo lo que la maestra necesita distinguir.
    if sello not in SELLOS or sello == "sin_datos":
        sello = "practicando" if (dias or estrellas) else "sin_datos"

    # Los saberes que ESTA tarjeta mide, limitados a los del grado del chico o anteriores:
    # un juego de 4.º puede aparecer también en el mapa de 6.º, y nombrarle a la maestra un
    # saber que su alumno todavía no tiene que ver sólo confunde.
    mide = []
    for sid in j2s.get(jid) or []:
        s = saberes.SABERES.get(sid) or {}
        if grado and int(s.get("grado") or 0) > grado:
            continue
        mide.append({"id": sid, "nombre": s.get("nombre") or sid,
                     "eje": s.get("eje") or "", "grado": s.get("grado") or 0,
                     "dominado": sid in (perfil.get("dominados") or [])})
    mide.sort(key=lambda m: (m["grado"], m["nombre"]))

    return {
        "id": jid,
        "titulo": item.get("titulo") or jid,
        "icono": item.get("icono") or "",
        "categoria": item.get("categoria") or categoria_de(jid) or "logica",
        "escalon": max(1, min(3, escalon)),
        "estrellas": max(0, min(3, estrellas)),
        "sello": sello,
        "sello_txt": ETIQUETA_SELLO[sello],
        "dias": dias,
        "veces": len(dias),
        "repasar_en": int(dom.get("repasarEn") or 0),
        "mide": mide,
        # `abrio` es lo primero que se mira en la pantalla y merece no tener que deducirse
        # de tres campos: es «esta tarjeta tiene algo o está en blanco».
        "abrio": bool(dias or estrellas or sello != "sin_datos"),
    }


def desglose(token, perfil=None):
    """{"grado": n, "perfiles": {nombre: {"tarjetas": [...], "hechas": n, "total": n}}}.

    `perfil` acota a un solo chico (un cuaderno puede tener varios: hermanos que comparten
    el acceso). Sin él vienen todos.

    NUNCA LANZA por falta de datos: un token sin `progreso.json` devuelve el menú completo
    con todas las tarjetas en `sin_datos`, que es la verdad —el cuaderno existe y está
    entero por abrir— y no una pantalla rota.
    """
    d = os.path.join(aw.ACT_DIR, token)
    if not os.path.isdir(d):
        return None
    grado = aw._grado_del_token(token) or 0
    # EL MENÚ DEL CUADERNO, no el catálogo genérico del grado. No son lo mismo: un token de
    # 4.º escolar trae 73 tarjetas y `catalogo_actividades()[4]` devuelve 39, porque el
    # token suma las de su modo (escolar, premium) y las EXTRA que el padre eligió. Con el
    # catálogo genérico la maestra veía media lista, y ninguna que coincidiera con lo que
    # el chico tiene abierto. Se descubrió con un test que compara las dos listas.
    try:
        menu = (json.load(open(os.path.join(d, "data.json"), encoding="utf-8"))
                .get("menu") or [])
    except Exception:
        menu = []
    try:
        data = json.load(open(os.path.join(d, "progreso.json"), encoding="utf-8"))
        perfiles = (data or {}).get("profiles") or {}
    except Exception:
        perfiles = {}
    if not isinstance(perfiles, dict):
        perfiles = {}
    # Un cuaderno recién entregado no tiene ningún perfil todavía. Igual se contesta con la
    # lista de tarjetas: la maestra tiene que poder ver QUÉ trae el cuaderno antes de que
    # el chico lo abra — es la mitad de lo que se muestra al ofrecerlo en persona.
    if not perfiles:
        perfiles = {"": {}}

    j2s = _juego_a_saberes()
    out = {}
    for nombre, p in perfiles.items():
        if perfil is not None and nombre != perfil:
            continue
        if not isinstance(p, dict):
            p = {}
        tarjetas = [_tarjeta(it, p, j2s, grado) for it in menu]
        out[nombre] = {
            "tarjetas": tarjetas,
            "total": len(tarjetas),
            "hechas": sum(1 for t in tarjetas if t["abrio"]),
            "dominadas": sum(1 for t in tarjetas
                             if t["sello"] in ("dominado", "consolidado")),
        }
    return {"grado": grado, "perfiles": out}
