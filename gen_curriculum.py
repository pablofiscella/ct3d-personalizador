"""Genera `actividades_curriculum.js` desde el catálogo declarativo.

Correr desde el repo:  python3 gen_curriculum.py

El archivo generado se sirve al player DESPUÉS de player.js (necesita `GAMES` y las
factories ya definidas) y registra una entrada `GAMES.<id>` por actividad del catálogo.

NO editar el .js a mano: se pisa en la próxima corrida. La fuente es
`actividades_curriculum.py`, donde una actividad es UNA entrada de datos.
"""
import json

import actividades_curriculum as cur

problemas = cur.validar()
if problemas:
    print("CATÁLOGO INVÁLIDO — no se genera nada:")
    for p in problemas:
        print("  -", p)
    raise SystemExit(1)

out = [
    "/* Actividades del catálogo CURRICULAR — GENERADO por gen_curriculum.py.\n"
    "   No editar a mano: la fuente es actividades_curriculum.py (una actividad = una\n"
    "   entrada de datos, con el contenido del DC y el documento del que salió).\n"
    "   Se carga DESPUÉS de player.js porque registra sobre GAMES. */\n",
]

for a in cur.CATALOGO:
    out.append("/* %d° · %s — %s\n   DC: %s\n   Fuente: %s */"
               % (a["grado"], a["titulo"], a["id"], a["dc"], a["fuente"]))
    pfx = a["id"][:10]
    if a["mecanica"] == "manipular":
        # misma forma que la paramétrica: sin banco, el ejercicio se genera
        pl = "CUR_%s_PIEZAS" % a["id"].upper()
        out.append("const %s = %s;" % (pl, json.dumps(a["plantilla"], ensure_ascii=False,
                                                      indent=2)))
        out.append('GAMES.%s = juegoManipular(%s, %s, "%s");'
                   % (a["id"], pl, json.dumps(a["consigna"], ensure_ascii=False), pfx))
        out.append("")
        continue
    if a["mecanica"] == "parametrica":
        # no tiene banco: el ejercicio se genera desde la plantilla en cada ronda
        pl = "CUR_%s_PLANTILLA" % a["id"].upper()
        out.append("const %s = %s;" % (pl, json.dumps(a["plantilla"], ensure_ascii=False,
                                                      indent=2)))
        out.append('GAMES.%s = juegoParametrico(%s, %s, "%s");'
                   % (a["id"], pl, json.dumps(a["consigna"], ensure_ascii=False), pfx))
        out.append("")
        continue
    banco = "CUR_%s_BANCO" % a["id"].upper()
    out.append("const %s = %s;" % (banco, json.dumps(a["banco"], ensure_ascii=False,
                                                     indent=2)))
    if a["mecanica"] == "trivia":
        out.append('GAMES.%s = juegoTriviaTexto(%s, %s, "%s");'
                   % (a["id"], banco, json.dumps(a.get("consigna") or
                                                 "Elegí la respuesta correcta.",
                                                 ensure_ascii=False), pfx))
    elif a["mecanica"] == "clasificar":
        out.append('GAMES.%s = juegoClasificar(%s, %s, %s, "%s");'
                   % (a["id"], banco,
                      json.dumps(a["consigna"], ensure_ascii=False),
                      json.dumps(a["categorias"], ensure_ascii=False), pfx))
    elif a["mecanica"] == "ordenar":
        out.append('GAMES.%s = juegoOrdenar(%s, %s, %s, "%s");'
                   % (a["id"], banco,
                      json.dumps(a["consigna"], ensure_ascii=False),
                      json.dumps(a["explica"], ensure_ascii=False), pfx))
    else:                                    # validar() ya lo impide, red de seguridad
        raise SystemExit("mecánica sin emisor: %r" % a["mecanica"])
    out.append("")

js = "\n".join(out)
open("actividades_curriculum.js", "w", encoding="utf-8").write(js)
print("actividades_curriculum.js:", len(js), "bytes |", len(cur.CATALOGO), "actividades |",
      sum(len(a.get("banco") or []) for a in cur.CATALOGO), "ítems de banco |",
      sum(1 for a in cur.CATALOGO if a["mecanica"] == "parametrica"), "paramétricas")
