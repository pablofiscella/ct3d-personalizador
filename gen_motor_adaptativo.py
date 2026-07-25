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
  // grado del token, por edad: edad 9 → 4°, 10 → 5°, 11 → 6°… Sin edad, asume 4°.
  _grado() { return ((typeof D !== "undefined" && D.edad) ? D.edad : 9) - 5; },
  saberDominado(sid) {
    const s = SABERES_MOTOR[sid];
    if (!s) return false;
    if (s.grado < this._grado()) return true;  // grados anteriores = asumidos dominados
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
  // ── nivelación inicial (ALEKS) ──────────────────────────────────────────────
  // ALEKS abre con un diagnóstico que UBICA al alumno; sin eso todos arrancan de
  // cero aunque ya sepan, y el motor les hace perder el tiempo con lo que ya
  // saben hacer. `ubicado` es el resultado de ese sondeo y es DISTINTO de
  // `dominado` a propósito: dominado es evidencia ganada practicando en días
  // distintos —es lo que ve el padre y lo que dispara la oferta— mientras que
  // ubicado sólo dice DÓNDE EMPEZAR. Mezclarlos daría por dominado algo que el
  // chico contestó bien una vez.
  saberUbicado(sid) {
    const st = this._store();
    return !!(st && st.ubicado && st.ubicado(sid));
  },
  // Lo que el motor considera "ya lo sabe hacer" para no volver a ofrecerlo y para
  // dar por cumplido un prerrequisito. El panel de padres NO usa esto.
  _conocidos() {
    const set = this._dominados();
    const st = this._store();
    if (st && st.ubicados) for (const sid of st.ubicados()) if (SABERES_MOTOR[sid]) set.add(sid);
    return set;
  },
  _prereqsOk(sid, dom) { return SABERES_MOTOR[sid].prereqs.every((p) => dom.has(p)); },
  // 'repaso' | 'dominado' | 'recomendado' | 'disponible' | 'reforzar'
  estadoActividad(actId) {
    const st = this._store();
    if (st && st.repasoPendiente && st.repasoPendiente(actId)) return "repaso";
    const saberes = (_JUEGO_A_SABERES[actId] || []).filter((sid) => SABERES_MOTOR[sid].grado <= this._grado());  // ignora saberes de grados posteriores
    if (!saberes.length) return "disponible";  // sin saber del grado (Extras/otra materia/otro grado)
    const dom = this._dominados();
    if (saberes.every((s) => dom.has(s))) return "dominado";
    // el frente se calcula con lo CONOCIDO (dominado + ubicado por el sondeo): un
    // prerrequisito que el chico ya sabe hacer no puede seguir frenándolo.
    const con = this._conocidos();
    if (saberes.every((s) => con.has(s))) return "disponible";   // lo ubicó el sondeo: no se lo insiste
    if (saberes.some((s) => !con.has(s) && this._prereqsOk(s, con))) return "recomendado";
    return "reforzar";
  },
  // Saberes a sondear: uno por materia del grado, de dificultad media-alta (el que
  // más información da — si lo sabe, se infieren sus prerrequisitos; si no, no se
  // asume nada). Devuelve [{sid, juego, categoria}].
  planSondeo(menuIds) {
    const enMenu = new Set(menuIds || []);
    const g = this._grado();
    const prof = (sid, vistos) => {          // profundidad en la cadena de prereqs
      if (vistos.has(sid)) return 0;         // corta ciclos por las dudas
      vistos.add(sid);
      const s = SABERES_MOTOR[sid];
      if (!s || !s.prereqs.length) return 0;
      return 1 + Math.max(...s.prereqs.map((p) => prof(p, vistos)));
    };
    const porCat = {};
    for (const sid in SABERES_MOTOR) {
      const s = SABERES_MOTOR[sid];
      if (s.grado !== g) continue;
      const juego = s.juegos.find((j) => enMenu.has(j));
      if (!juego) continue;                  // sin juego abrible no se puede sondear
      const cat = this.categoria(juego);
      (porCat[cat] = porCat[cat] || []).push({ sid, juego, cat, d: prof(sid, new Set()) });
    }
    const plan = [];
    for (const cat of CATEGORIA_ORDEN) {
      const arr = porCat[cat];
      if (!arr || !arr.length || cat === "logica") continue;   // Extras no es materia
      arr.sort((a, b) => a.d - b.d);
      plan.push(arr[Math.min(arr.length - 1, Math.floor(arr.length * 0.6))]);
    }
    return plan;
  },
  // Si el chico resolvió bien el sondeo de un saber, se dan por sabidos también sus
  // prerrequisitos: es la inferencia de ALEKS (no se puede resolver lo de arriba sin
  // lo de abajo) y es lo que hace que un sondeo corto ubique mucho.
  saberYPrereqs(sid, acc) {
    acc = acc || new Set();
    if (!SABERES_MOTOR[sid] || acc.has(sid)) return acc;
    acc.add(sid);
    for (const p of SABERES_MOTOR[sid].prereqs) this.saberYPrereqs(p, acc);
    return acc;
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
  saberCategoria(sid) { const j = (SABERES_MOTOR[sid]||{}).juegos || []; return j.length ? this.categoria(j[0]) : null; },
  // resumen por categoría para el panel de padres: dominado/en proceso/pendiente
  resumenPorCategoria() {
    const res = {}; for (const c of CATEGORIA_ORDEN) res[c] = { dom: 0, proc: 0, pend: 0, total: 0 };
    const dom = this._dominados(); const st = this._store();
    for (const sid in SABERES_MOTOR) {
      const s = SABERES_MOTOR[sid]; if (s.grado !== this._grado()) continue;   // solo el grado del token
      const cat = this.saberCategoria(sid); if (!cat || !res[cat]) continue;
      res[cat].total++;
      if (dom.has(sid)) res[cat].dom++;
      else if (st && s.juegos.some((j) => st.stars(j) > 0)) res[cat].proc++;
      else res[cat].pend++;
    }
    return res;
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
