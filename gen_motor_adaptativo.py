"""Genera motor_adaptativo.js (servido al player) desde las fuentes Python:
  - saberes.py                → SABERES_MOTOR (grafo de saberes 4° Mate) + lógica Adapt
  - actividades_categorias.py → CATEGORIA_JUEGO/ORDEN/LABEL (para separar el menú)
Correr desde el repo:  python3 gen_motor_adaptativo.py
"""
import sys, json
sys.path.insert(0, ".")
from saberes import SABERES
from actividades_categorias import CATEGORIA, CATEGORIA_ORDEN, CATEGORIA_LABEL

compact = {sid: {"nombre": d["nombre"], "grado": d["grado"], "eje": d["eje"],
                 "prereqs": d["prerrequisitos"], "juegos": d["juegos"]}
           for sid, d in SABERES.items()}
data = json.dumps(compact, ensure_ascii=False, indent=0).replace("\n", " ")
cat_juego = json.dumps(CATEGORIA, ensure_ascii=False)
cat_orden = json.dumps(CATEGORIA_ORDEN, ensure_ascii=False)
cat_label = json.dumps(CATEGORIA_LABEL, ensure_ascii=False)

LOGICA = r'''
/* ── Adapt: capa de saberes + categorías sobre el Store del player (no bloquea) ── */
const _JUEGO_A_SABERES = (() => {
  const m = {};
  for (const sid in SABERES_MOTOR)
    for (const j of SABERES_MOTOR[sid].juegos) (m[j] = m[j] || []).push(sid);
  return m;
})();

const Adapt = {
  _store() { return (typeof Store !== "undefined") ? Store : null; },
  saberDominado(sid) {
    const s = SABERES_MOTOR[sid];
    if (!s) return false;
    if (s.grado < 4) return true;              // grado anterior = asumido dominado
    const st = this._store();
    return !!st && s.juegos.some((j) => {
      const sel = st.sello(j);
      return sel === "dominado" || sel === "consolidado";
    });
  },
  _dominados() {
    const set = new Set();
    for (const sid in SABERES_MOTOR) if (this.saberDominado(sid)) set.add(sid);
    return set;
  },
  _prereqsOk(sid, dom) { return SABERES_MOTOR[sid].prereqs.every((p) => dom.has(p)); },
  // 'repaso' | 'dominado' | 'recomendado' | 'disponible' | 'reforzar'
  estadoActividad(actId) {
    const st = this._store();
    if (st && st.repasoPendiente && st.repasoPendiente(actId)) return "repaso";
    const saberes = _JUEGO_A_SABERES[actId];
    if (!saberes || !saberes.length) return "disponible";  // sin saber (Extras/otra materia)
    const dom = this._dominados();
    if (saberes.every((s) => dom.has(s))) return "dominado";
    if (saberes.some((s) => !dom.has(s) && this._prereqsOk(s, dom))) return "recomendado";
    return "reforzar";
  },
  _ORDEN: { repaso: 0, recomendado: 1, disponible: 2, dominado: 3, reforzar: 4 },
  peso(actId) { return this._ORDEN[this.estadoActividad(actId)]; },
  etiqueta(actId) {
    return ({ repaso: "🔁 Repasá", recomendado: "✨ Recomendado", disponible: "",
              dominado: "🏅 Dominado", reforzar: "🌱 Reforzá antes" })[this.estadoActividad(actId)];
  },
  // ── categorías (para separar el menú) ──
  categoria(actId) { return CATEGORIA_JUEGO[actId] || "logica"; },   // sin match → Extras
  ordenCategorias() { return CATEGORIA_ORDEN.slice(); },
  // próxima actividad recomendada del menú (repaso/recomendado), distinta de la actual
  proximaRecomendada(menuIds, excepto) {
    const cand = menuIds.filter((id) => id !== excepto && _JUEGO_A_SABERES[id] && this.peso(id) <= 1)
                        .sort((a, b) => this.peso(a) - this.peso(b));
    return cand.length ? cand[0] : null;
  },
  labelCategoria(cat) { return CATEGORIA_LABEL[cat] || cat; },
};
if (typeof module !== "undefined")
  module.exports = { Adapt, SABERES_MOTOR, CATEGORIA_JUEGO, CATEGORIA_ORDEN, CATEGORIA_LABEL };
'''

header = ("/* Motor adaptativo — PILOTO 4° Matemática. Capa de SABERES + CATEGORÍAS sobre el player.\n"
          "   GENERADO desde saberes.py + actividades_categorias.py (gen_motor_adaptativo.py). No editar\n"
          "   a mano los bloques de datos. Gateado por D.adaptativo_on: sin flag el player no lo usa. */\n\n")
out = (header
       + "const SABERES_MOTOR = " + data + ";\n"
       + "const CATEGORIA_JUEGO = " + cat_juego + ";\n"
       + "const CATEGORIA_ORDEN = " + cat_orden + ";\n"
       + "const CATEGORIA_LABEL = " + cat_label + ";\n"
       + LOGICA)
open("motor_adaptativo.js", "w", encoding="utf-8").write(out)
print("motor_adaptativo.js:", len(out), "bytes |", len(compact), "saberes |", len(CATEGORIA), "juegos categorizados")
