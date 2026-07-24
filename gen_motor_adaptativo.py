import sys, json; sys.path.insert(0,'.')
from saberes import SABERES
compact = {sid: {"nombre": d["nombre"], "grado": d["grado"], "eje": d["eje"],
                 "prereqs": d["prerrequisitos"], "juegos": d["juegos"]}
           for sid, d in SABERES.items()}
data = json.dumps(compact, ensure_ascii=False, indent=0).replace("\n", " ")
LOGICA = r'''
/* ── Adapt: capa de saberes sobre el Store del player (no bloquea, solo informa/ordena) ── */
const _JUEGO_A_SABERES = (() => {
  const m = {};
  for (const sid in SABERES_MOTOR)
    for (const j of SABERES_MOTOR[sid].juegos) (m[j] = m[j] || []).push(sid);
  return m;
})();

const Adapt = {
  _store() { return (typeof Store !== "undefined") ? Store : null; },
  // grado anterior (<4) = asumido dominado (el chico está en 4°); saber de 4° = dominado si
  // alguna actividad que lo mide tiene sello 'dominado'/'consolidado' en el Store.
  saberDominado(sid) {
    const s = SABERES_MOTOR[sid];
    if (!s) return false;
    if (s.grado < 4) return true;
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
    if (!saberes || !saberes.length) return "disponible";  // fuera del piloto (otra materia/lógica)
    const dom = this._dominados();
    if (saberes.every((s) => dom.has(s))) return "dominado";
    if (saberes.some((s) => !dom.has(s) && this._prereqsOk(s, dom))) return "recomendado";
    return "reforzar";  // prereqs sin dominar → conviene reforzar antes (pero se puede jugar igual)
  },
  _ORDEN: { repaso: 0, recomendado: 1, disponible: 2, dominado: 3, reforzar: 4 },
  peso(actId) { return this._ORDEN[this.estadoActividad(actId)]; },
  etiqueta(actId) {
    return ({ repaso: "🔁 Repasá", recomendado: "✨ Recomendado", disponible: "",
              dominado: "🏅 Dominado", reforzar: "🌱 Reforzá antes" })[this.estadoActividad(actId)];
  },
};
if (typeof module !== "undefined") module.exports = { Adapt, SABERES_MOTOR, _JUEGO_A_SABERES };
'''
header = ("/* Motor adaptativo — PILOTO 4° Matemática. Capa de SABERES sobre el Store del player.\n"
          "   GENERADO desde saberes.py (mantener en sync, no editar a mano el bloque de datos).\n"
          "   Gateado por D.adaptativo_on: si el token no lo tiene, el player NO lo usa y nada cambia. */\n\n")
out = header + "const SABERES_MOTOR = " + data + ";\n" + LOGICA
open("motor_adaptativo.js", "w", encoding="utf-8").write(out)
print("motor_adaptativo.js generado:", len(out), "bytes,", len(compact), "saberes")
