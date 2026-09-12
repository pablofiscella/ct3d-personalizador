"""Genera `seno_clases.py`: con qué CLASE de la seño se refuerza cada tarjeta del cuaderno.

Pablo, 11-sep-2026: *"icono de seño en cada tarjeta con practicas"*.

ESTO ES UNA COPIA, Y ES A PROPÓSITO — LA MISMA REGLA, EN EL SENTIDO QUE FALTABA
──────────────────────────────────────────────────────────────────────────────
Los temas de la seño viven en `kydo/seno/` del repo de ct3d, que es de Kydo. Este motor
atiende a las DOS marcas —el cuaderno escolar de Kydo y el que viene en los kits de
cumpleaños de Casatridimensional—, así que **no puede importar `kydo.*` en tiempo de
ejecución**: sería atar un programa compartido a un solo negocio. Del otro lado ya existe
la regla escrita y con test (`test_seno_practicar_en_el_cuaderno.py::
test_KYDO_NO_IMPORTA_el_motor_del_cuaderno`, que prohíbe que Kydo importe este motor).

Entonces: este script CORRE A MANO, lee ct3d una vez y deja el dato escrito en
`seno_clases.py`, que sí se commitea. El precio de copiar es que se desactualiza, y ese
precio se paga con `tests/test_seno_clases.py`, no con la memoria.

POR QUÉ EN UN ARCHIVO APARTE Y NO ADENTRO DE `gen_motor_adaptativo.py`
─────────────────────────────────────────────────────────────────────
Porque ese generador se corre para cualquier cambio de saberes o categorías, también en
máquinas donde `/opt/ct3d` no existe (el CI, por ejemplo). Si la tabla se armara ahí, una
corrida sin ct3d la dejaría VACÍA y en silencio, y el cuaderno perdería todos los íconos
sin que nada fallara. Separado, `motor_adaptativo.js` se regenera sin tocar esto.

LA CLAVE ES (GRADO, TARJETA) Y NO LA TARJETA SOLA
─────────────────────────────────────────────────
Hay tarjetas que se reusan en varios grados («La serie», «Tablas ninja», «Recta gigante»).
La seño **sólo abre la clase del grado del cuaderno** (`kydo/web.py`: si
`tema["grado"] != grado` redirige al índice). Con una tabla plana por tarjeta, un chico de
2.º con una tarjeta reusada pediría la clase de 4.º y lo rebotarían. Por eso el grado va
primero.

    python3 gen_seno_clases.py
"""
import importlib
import json
import os
import sys

CT3D = "/opt/ct3d/backend"
SALIDA = "seno_clases.py"
MODULOS = ["temas", "temas_lengua"] + ["temas_lengua_%d" % g for g in range(1, 8)]


def temas_de_la_seno():
    """Los temas de la seño, leídos UNA vez desde ct3d. Falla fuerte si no está."""
    if not os.path.isdir(CT3D):
        sys.exit("no encuentro %s: este script se corre en el server, no en el CI" % CT3D)
    sys.path.insert(0, CT3D)
    vistos = {}
    for m in MODULOS:
        try:
            mod = importlib.import_module("kydo.seno." + m)
        except ModuleNotFoundError:
            continue          # no todos los grados de Lengua existen (falta el 4.º)
        for v in vars(mod).values():
            if isinstance(v, dict) and isinstance(v.get("id"), str) and v.get("saber"):
                vistos.setdefault(v["id"], v)
    return vistos


# ── EL EMPAREJAMIENTO A MANO ─────────────────────────────────────────────────────
# 29 clases de Lengua declaran un `saber` que el motor no tiene con ningún nombre
# (`LEN-6-HIATO`, `LEN-7-PORQUES`…). No es un problema de mayúsculas —eso arregla sólo 2,
# medido— sino que la seño y el cuaderno partieron Lengua distinto. La clase existe y la
# tarjeta existe: lo único que falta es decir cuál va con cuál, y eso no lo puede deducir
# un programa.
#
# 20 de las 29 tienen una tarjeta que enseña LO MISMO. Las otras 9 quedan afuera a
# propósito y están anotadas abajo: no hay tarjeta de rimas ni de letra final en 1.º, ni de
# artículos en 2.º, ni de la hache en 6.º. **Un ícono que lleva a una clase que no es la del
# tema es peor que no tener ícono**: el chico toca «Dos puntos y raya» y le aparece una
# clase sobre la coma.
A_MANO = {
    # 1.º
    "cuantas-partes": "silabas_1",              # Cuántas partes tiene → Contá las sílabas
    # 2.º
    "la-mayuscula": "signos_2",                 # Dónde va la mayúscula → Signos y mayúsculas
    # 3.º
    "signos-de-pregunta": "dialogo_signos_3",   # Los signos que abren → Armá el diálogo
    "diminutivos-y-aumentativos": "derivadas_3",  # Más chico y más grande → Fábrica de palabras
    "ge-gue-guee": "ortografia_3ro",            # La u que no se oye → ¿Cómo se escribe?
    # 5.º
    "sujeto-tacito": "sujeto_predicado",        # El sujeto que no está escrito → Sujeto y predicado
    "be-y-ve": "homofonos_5",                   # B larga y V corta → Vaya, valla o baya
    "el-instructivo": "estructura_textos_5",    # El instructivo → Arquitecto de textos
    "los-adverbios": "clases_palabra_5",        # La palabra que dice cómo → ¿Qué clase de palabra es?
    # 6.º
    "objetos-del-verbo": "od_oi_6",             # Objeto directo e indirecto → OD, OI y transitividad
    "tilde-en-el-hiato": "tildes_6",            # La tilde que rompe el diptongo → Tildes rebeldes
    "modos-del-verbo": "conjugacion_6",         # Los modos del verbo → Conjugá el verbo
    "escribir-sin-repetir": "cohesion_6",       # Escribir sin repetir → Basta de repetir
    "circunstanciales": "sintagma_6",           # Dónde, cuándo y cómo → Radiografía de la oración
    "donde-abre-la-pregunta": "puntuacion_6",   # Dónde se abre la pregunta → Puntuación fina
    "la-idea-principal": "idea_principal_6",    # De qué se trata → Idea principal y cuadro sinóptico
    # 7.º
    "los-porques": "ortografia_7",              # Los cuatro porqués → Cazador de errores
    "armar-un-argumento": "recursos_argumentador_7",  # Armar un argumento → Recursos del argumentador
    "oracion-compuesta": "analisis_sintactico_7",     # Una oración o dos pegadas → Análisis sintáctico
    "para-que-esta-escrito": "persuasion_7",    # Para qué está escrito → Detector de persuasión
}

# Las 9 que NO se emparejan, y por qué. Se escriben para que el próximo que mire no vuelva a
# buscarlas: no es un olvido, es que el cuaderno no tiene esa tarjeta.
SIN_TARJETA = {
    "palabras-que-riman": "1.º no tiene tarjeta de rimas",
    "letra-final": "1.º sólo tiene letra INICIAL, que ya está tomada",
    "el-la-los-las": "los artículos son tarjeta de 1.º, y la seño rebota otro grado",
    "donde-termina-la-oracion": "el punto comparte tarjeta con las mayúsculas, ya tomada",
    "la-coma-cambia-todo": "5.º sólo tiene «Dos puntos y raya»: es otra cosa",
    "la-hache": "6.º no tiene tarjeta de ortografía de la hache",
    "la-descripcion": "6.º no tiene tarjeta de descripción",
    "voz-activa-y-pasiva": "7.º no tiene tarjeta de voz pasiva",
    "la-carta-formal": "7.º no tiene tarjeta de carta formal",
}


def tabla():
    """{grado: {id_de_tarjeta: (id_del_tema, título de la clase)}}"""
    sys.path.insert(0, ".")
    from saberes import SABERES
    import actividades_curriculum as ac
    import actividades_web as aw

    # EL CATÁLOGO DE SABERES SE CARGA POR LA MITAD si no se está parado en el repo del
    # motor: su import de `actividades_curriculum` vive adentro de un `try/except: pass`.
    # 444 contra 119, y en silencio. Mejor cortar que escribir una tabla recortada.
    if len(SABERES) < 300:
        sys.exit("saberes llegó recortado (%d): corré esto parado en el repo del motor"
                 % len(SABERES))

    temas = temas_de_la_seno()
    out, sin_saber = {}, 0
    for t in sorted(temas.values(), key=lambda x: x["id"]):
        s = SABERES.get(t["saber"])
        if not s:
            sin_saber += 1     # el saber de la clase no existe acá (Lengua en MAYÚSCULAS)
            continue
        g = t["grado"]
        for j in (s.get("juegos") or []):
            out.setdefault(g, {}).setdefault(j, (t["id"], t["titulo"]))

    # el emparejamiento a mano, DESPUÉS del automático y sin pisarlo
    for tid, act in sorted(A_MANO.items()):
        t = temas.get(tid)
        if not t:
            sys.exit("A_MANO nombra el tema «%s», que la seño ya no tiene" % tid)
        ya = (out.get(t["grado"]) or {}).get(act)
        if ya and ya[0] != tid:
            sys.exit("A_MANO manda «%s» a la tarjeta %s, que el automático ya le dio a «%s»"
                     % (tid, act, ya[0]))
        out.setdefault(t["grado"], {})[act] = (tid, t["titulo"])
    sin = sorted(set(SIN_TARJETA) & set(A_MANO))
    if sin:
        sys.exit("estos temas están en las dos listas a la vez: %s" % ", ".join(sin))

    # SÓLO LAS TARJETAS QUE ESE GRADO REALMENTE TIENE. Un saber puede listar juegos que no
    # están en el menú de ese año; dejarlos escribiría íconos para tarjetas inexistentes.
    limpio = {}
    for g in range(1, 8):
        delGrado = {it["id"] for it in (ac.menu_de_grado(g) or [])}
        delGrado |= {it["id"] for it in (aw._menu(aw._banda(str(g + 5)), str(g + 5),
                                                  escolar=True) or [])}
        hay = {j: v for j, v in (out.get(g) or {}).items() if j in delGrado}
        if hay:
            limpio[g] = dict(sorted(hay.items()))
    return limpio, len(temas), sin_saber


def main():
    datos, total, sin_saber = tabla()
    cuantas = sum(len(v) for v in datos.values())
    if cuantas < 100:
        sys.exit("salieron sólo %d tarjetas: algo se cargó mal, no piso el archivo" % cuantas)

    cuerpo = ["# -*- coding: utf-8 -*-",
              '"""Con qué clase de «Mi seño particular» se refuerza cada tarjeta.',
              "",
              "GENERADO por gen_seno_clases.py desde kydo/seno/ de ct3d. NO editar a mano.",
              "Es una COPIA deliberada: este motor no puede importar `kydo.*` en ejecución",
              "porque atiende también a Casatridimensional. Lo que la sostiene es",
              "tests/test_seno_clases.py, que la rearma desde la fuente y falla si quedó vieja.",
              "",
              "La clave es el GRADO y después la tarjeta: hay tarjetas reusadas en varios",
              'grados y la seño sólo abre la clase del grado del cuaderno.',
              '"""',
              "",
              "# grado → {id de la tarjeta: (id del tema, título de la clase)}",
              "CLASES = {"]
    for g in sorted(datos):
        cuerpo.append("    %d: {" % g)
        for j, (tid, tit) in datos[g].items():
            cuerpo.append("        %s: (%s, %s)," % (json.dumps(j, ensure_ascii=False),
                                                     json.dumps(tid, ensure_ascii=False),
                                                     json.dumps(tit, ensure_ascii=False)))
        cuerpo.append("    },")
    cuerpo += ["}", "",
               "",
               "def de(grado, actividad):",
               '    """El tema de la seño para esa tarjeta en ese grado, o None."""',
               "    return (CLASES.get(grado) or {}).get(actividad)",
               ""]
    with open(SALIDA, "w", encoding="utf-8") as f:
        f.write("\n".join(cuerpo))
    print("%s: %d tarjetas con clase, en %d grados" % (SALIDA, cuantas, len(datos)))
    print("temas de la seño leídos: %d · sin saber conocido en el motor: %d"
          % (total, sin_saber))
    for g in sorted(datos):
        print("   %d.º: %d" % (g, len(datos[g])))


if __name__ == "__main__":
    main()
