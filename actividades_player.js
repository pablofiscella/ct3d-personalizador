/* ══ Player del cuaderno de actividades interactivo — Casatridimensional ══
   Un solo archivo, vanilla JS, rutas RELATIVAS (vive bajo /act/<token>/).
   Contrato: data.json trae paleta + menú por edad + puzzles YA VERIFICADOS
   (laberinto con salida, sopa completa, sudoku único — generados en Python).
   Principios (investigación 10-jul-2026): targets ≥76px, tap primero, cero
   fail states (el error sacude suave y deja seguir), feedback inmediato,
   elogio al esfuerzo, festejo corto, sin timers ni puntajes que bajen. */
"use strict";

const $ = (s) => document.querySelector(s);
/* Alto disponible para el tablero (viewport - header - consigna - progreso):
   los juegos DEBEN entrar sin scroll — feedback Pablo 10-jul: en el celu había
   que scrollear y la consigna quedaba arriba. */
function ajustarAlto() {
  const j = $("#juego");
  document.documentElement.style.setProperty("--hdrH", ($("#hdr").offsetHeight || 74) + "px");
  if (!j) return;
  const alto = Math.max(280, innerHeight - j.getBoundingClientRect().top - 30);
  document.documentElement.style.setProperty("--altoJuego", alto + "px");
}
const el = (tag, cls, html) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html !== undefined) e.innerHTML = html;
  return e;
};
const rint = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
const shuffle = (arr) => {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};
const sample = (arr, n) => shuffle(arr).slice(0, n);
const espera = (ms) => new Promise((r) => setTimeout(r, ms));

// Consigna variada (15-jul-2026, Pablo: "esto repetitivo se da en varias,
// hay que tratar de que sea más natural" — la mayoría de los juegos de
// clasificación repiten LITERALMENTE la misma consigna hasta 10 veces por
// partida). Ronda 0 dice la consigna completa (da contexto); de ahí en más
// alterna al azar entre variantes CORTAS reutilizables — nunca contenido a
// medida por juego (76 juegos, no escala escribir cada uno a mano).
// Concordancia de género real (Pablo: "si es una palabra en femenino, esta
// otra... que tenga sentido"): "m" para masculino (este material/animal/
// ángulo/planeta), "f" para femenino (esta provincia/palabra/planta/
// afirmación), "n" (neutro, "esto") cuando el ítem mostrado varía de
// género ronda a ronda (un emoji de objeto/animal cualquiera) — "esto" no
// fuerza concordancia con nada, es la opción segura ahí.
const CONSIGNA_CORTA_MASC = ["¿Y este?", "¿Y este otro?", "¿Este también?", "¿Y ahora este?", "¿Qué decís de este?"];
const CONSIGNA_CORTA_FEM = ["¿Y esta?", "¿Y esta otra?", "¿Esta también?", "¿Y ahora esta?", "¿Qué decís de esta?"];
const CONSIGNA_CORTA_NEUTRO = ["¿Y esto?", "¿Y esto otro?", "¿Esto también?", "¿Y ahora esto?", "¿Qué decís de esto?"];
// "Bolsa" sin repetir (15-jul-2026, Pablo: "después del tercero dijo 'y
// este?' siempre lo mismo... que no se repita tanto" — con puro azar sobre
// pocas opciones el mismo texto podía salir 2 veces seguidas fácil).
// Estado por INSTANCIA de juego Y por `key` (WeakMap<ctx, {[key]: {bolsa,
// anterior}}> — `ctx` es un objeto nuevo cada vez que se entra a un juego,
// se libera solo al salir; `key` separa "bolsas" independientes dentro del
// MISMO juego, ej. mas_menos necesita una bolsa para MÁS y otra para MENOS
// sin que se mezclen). Se baraja el set completo, se saca SIN reponer hasta
// vaciarla (no repite ninguna hasta agotar las demás) y al rebarajar se
// evita que la primera que toque sea la misma que la última usada, para
// que tampoco repita justo en el borde entre una bolsa y la siguiente.
const _bolsaEstado = new WeakMap();
function sacarDeBolsa(ctx, key, set) {
  let porJuego = _bolsaEstado.get(ctx);
  if (!porJuego) { porJuego = {}; _bolsaEstado.set(ctx, porJuego); }
  let b = porJuego[key];
  if (!b) { b = { bolsa: [], anterior: null }; porJuego[key] = b; }
  if (!b.bolsa.length) {
    b.bolsa = shuffle(set);
    const ultimo = b.bolsa.length - 1;
    if (ultimo > 0 && b.bolsa[ultimo] === b.anterior) {
      [b.bolsa[0], b.bolsa[ultimo]] = [b.bolsa[ultimo], b.bolsa[0]];
    }
  }
  b.anterior = b.bolsa.pop();
  return b.anterior;
}
// consignaVariada: ronda 0 dice la consigna completa (da contexto); de ahí
// en más alterna entre variantes CORTAS reutilizables — nunca contenido a
// medida por juego (76 juegos, no escala escribir cada uno a mano).
// Concordancia de género real (Pablo: "si es una palabra en femenino, esta
// otra... que tenga sentido"): "m" para masculino (este material/animal/
// ángulo/planeta), "f" para femenino (esta provincia/palabra/planta/
// afirmación), "n" (neutro, "esto") cuando el ítem mostrado varía de
// género ronda a ronda (un emoji de objeto/animal cualquiera) — "esto" no
// fuerza concordancia con nada, es la opción segura ahí.
function consignaVariada(ctx, ronda, textoLargo, genero) {
  if (ronda === 0) { _bolsaEstado.delete(ctx); ctx.consigna(textoLargo); return; }
  const set = genero === "f" ? CONSIGNA_CORTA_FEM : genero === "n" ? CONSIGNA_CORTA_NEUTRO : CONSIGNA_CORTA_MASC;
  ctx.consigna(sacarDeBolsa(ctx, "generica", set));
}

let D = null;            // data.json
let P = [];              // personajes (filenames)
const GAMES = {};        // registro de juegos

/* ── audio-guía (14-jul-2026): consignas grabadas — texto fijo del player,
   no personalizado, así que es UN solo archivo por frase para TODOS los
   tokens (mismo criterio que player.js/las fuentes: mejora una vez, llega
   a todos los links ya vendidos). Best-effort: si el manifest no existe
   (producto sin audio todavía) o el archivo puntual no está grabado, el
   player sigue andando en silencio — nunca bloquea la actividad. */
let AudioManifest = {};
let vozActual = null;
async function cargarAudioManifest() {
  try {
    const r = await fetch("audio_manifest.json");
    if (r.ok) AudioManifest = await r.json();
  } catch (e) { /* sin audio-guía para este token: se juega en silencio */ }
}
// Devuelve una Promise<boolean> (true = terminó de sonar de verdad) — los
// llamadores "fire and forget" de siempre (ctx.consigna) simplemente no la
// esperan, cero cambio de comportamiento para ellos. La lección de suma en
// columnas SÍ la espera (ver decirYesperar) para encadenar frases sin
// atropellarse: antes usaba pausas fijas "a ojo" y, si la frase real duraba
// más que la pausa, la siguiente la cortaba en seco (Pablo 15-jul-2026:
// "entre cuando explica 0 + 4 no hace pausa y queda el audio muy junto").
function reproducirConsigna(txt) {
  if (vozActual) { vozActual.pause(); vozActual = null; }
  if (!Sfx.on) return Promise.resolve(false);
  // Texto FIJO → mp3 pregrabado del manifest (voz argentina, instantáneo).
  // Texto DINÁMICO (consignas/explicaciones generadas, que no están en el
  // manifest) → endpoint /tts on-demand, MISMA voz argentina, cacheado en el
  // server. Antes el texto dinámico quedaba en silencio (19-jul-2026).
  const archivo = AudioManifest[txt] || ("/tts?t=" + encodeURIComponent(txt));
  const audio = new Audio(archivo);
  vozActual = audio;
  return new Promise((resolve) => {
    audio.addEventListener("ended", () => resolve(true), { once: true });
    audio.addEventListener("error", () => resolve(false), { once: true });
    audio.play().catch(() => resolve(false));   // autoplay bloqueado hasta el primer toque: no rompe nada
  });
}
// Desbloqueo de audio (15-jul-2026): algunos navegadores móviles (sobre todo
// iOS) solo permiten reproducir audio con sonido si el .play() ocurre cerca
// de un toque real — la lección de suma en columnas encadena varias voces
// con pausas de 1-2s entre cada una (para leer/escuchar cómodo), y esas
// llamadas tardías podían quedar mudas aunque el primer sonido del juego sí
// se escuchara. Reproduce (mute) un clip real en el primer toque de verdad
// para "activar" el audio del resto de la sesión.
let _audioDesbloqueado = false;
function desbloquearAudio() {
  if (_audioDesbloqueado) return;
  const archivo = Object.values(AudioManifest)[0];
  if (!archivo) return;   // el manifest todavía no cargó — se reintenta en el próximo toque
  _audioDesbloqueado = true;
  const a = new Audio(archivo);
  a.volume = 0;
  a.play().then(() => { a.pause(); a.currentTime = 0; }).catch(() => { _audioDesbloqueado = false; });
}
document.addEventListener("click", desbloquearAudio, { capture: true });

/* ── persistencia (perfiles + estrellas + sonido) por token ── */
/* Perfiles (14-jul-2026, Pablo: "pueden ser 2 chicos los que juegan en la
   misma casa" — el link/token es UNO solo por compra, pero cada hermano
   entra con su propio nombre y junta SUS estrellas, no las del otro; cada
   uno gana su propio diploma. Formato viejo (antes de esto) guardaba
   {stars,sound} sueltos — se migra a un perfil placeholder para no perder
   el progreso ya juntado. */
/* ── Capa 0 · SELLO DE DOMINIO SOSTENIDO + REPASO ESPACIADO (cierre de Capa 0,
   docs/auditoria-dc-caba/): una actividad se "domina de verdad" no con 3★ de una
   (que puede ser suerte de un día), sino SOSTENIÉNDOLO en 2 DÍAS distintos; ahí
   queda "dominada" y vuelve en un REPASO a los pocos días — si lo pasa, queda
   "consolidada" (y se re-agenda un repaso de mantenimiento). Aditivo: las
   estrellas y el festejo de siempre no cambian; esto suma el sello real. ── */
const REPASO_DIAS = 3;            // dominado → repaso a los 3 días
const REPASO_LARGO_DIAS = 10;     // consolidado → repaso de mantenimiento a los 10
const DIA_MS = 86400000;
function _hoyStr(d) {
  d = d || new Date();
  return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") +
         "-" + String(d.getDate()).padStart(2, "0");
}

const Store = {
  key: "ct3d_act::" + location.pathname.replace(/\/$/, ""),
  data: { sound: true, activeProfile: null, profiles: {} },
  load() {
    try {
      const raw = JSON.parse(localStorage.getItem(this.key) || "{}");
      if (raw.stars && !raw.profiles) {          // migración formato viejo (sin perfiles)
        raw.profiles = { "Jugador 1": { stars: raw.stars } };
        raw.activeProfile = "Jugador 1";
        delete raw.stars;
      }
      Object.assign(this.data, raw);
    } catch (e) {}
  },
  save() { try { localStorage.setItem(this.key, JSON.stringify(this.data)); } catch (e) {} },
  _perfil() { return this.data.profiles[this.data.activeProfile]; },
  stars(id) {
    const p = this._perfil();
    return (p && p.stars[id]) || 0;
  },
  setStars(id, n) {
    const p = this._perfil();
    if (p && n > this.stars(id)) { p.stars[id] = n; this.save(); }
  },
  total() {
    const p = this._perfil();
    return p ? Object.values(p.stars).reduce((a, b) => a + b, 0) : 0;
  },
  // ── sello de dominio sostenido (Capa 0) ──
  dom(id) {
    const p = this._perfil();
    return (p && p.dominio && p.dominio[id]) || null;
  },
  sello(id) {                       // 'practicando' | 'dominado' | 'consolidado'
    const d = this.dom(id);
    return d ? d.sello : "practicando";
  },
  repasoPendiente(id) {             // ya dominado/consolidado y le toca repaso
    const d = this.dom(id);
    return !!(d && (d.sello === "dominado" || d.sello === "consolidado") &&
              d.repasarEn && Date.now() >= d.repasarEn);
  },
  repasosPendientes(menu) {
    return (menu || []).filter((m) => this.repasoPendiente(m.id)).map((m) => m.id);
  },
  // se llama al ganar con e>=3 (nivel de dominio). Devuelve el evento nuevo:
  // 'dominado' | 'consolidado' | null. `hoy` (YYYY-MM-DD) inyectable para tests.
  registrarDominio(id, e, hoy) {
    const p = this._perfil();
    if (!p || e < 3) return null;
    if (!p.dominio) p.dominio = {};
    const d = p.dominio[id] || (p.dominio[id] = { dias: [], sello: "practicando", repasarEn: 0 });
    const hoyS = hoy || _hoyStr();
    if (d.dias.indexOf(hoyS) === -1) d.dias.push(hoyS);
    const eraRepaso = this.repasoPendiente(id);
    let evt = null;
    if (d.sello === "practicando" && d.dias.length >= 2) {
      d.sello = "dominado"; d.repasarEn = Date.now() + REPASO_DIAS * DIA_MS; evt = "dominado";
    } else if (eraRepaso && d.sello === "dominado") {
      d.sello = "consolidado"; d.repasarEn = Date.now() + REPASO_LARGO_DIAS * DIA_MS; evt = "consolidado";
    } else if (eraRepaso && d.sello === "consolidado") {
      d.repasarEn = Date.now() + REPASO_LARGO_DIAS * DIA_MS;   // mantenimiento OK, re-agenda
    }
    this.save();
    return evt;
  },
};

/* ── Capa 0 · C1+C5 (19-jul-2026, docs/auditoria-dc-caba/CAPA-0-MOTOR-DOMINIO.md):
   telemetría de PRIMER INTENTO por ítem. Aditivo: no cambia ninguna mecánica ni
   lo que ve el chico — solo registra {juego, ítem, edad, primer intento, correcto}
   para poder VER con datos qué actividad quedó muy fácil/difícil. Buffer local por
   token (localStorage) + envío best-effort al motor; si el endpoint aún no existe
   (se construye en el incremento C5-server), los datos quedan en el buffer local y
   NO rompe nada. La compuerta de dominio que USA estos datos es C2, aparte. ── */
const Tel = {
  key() { return Store.key + "::tel"; },
  buf: null,
  _load() {
    if (this.buf) return;
    try { this.buf = JSON.parse(localStorage.getItem(this.key()) || "[]"); }
    catch (e) { this.buf = []; }
  },
  push(ev) {
    this._load();
    this.buf.push(ev);
    // cap defensivo: nunca dejar crecer el localStorage sin límite.
    if (this.buf.length > 800) this.buf.splice(0, this.buf.length - 800);
    try { localStorage.setItem(this.key(), JSON.stringify(this.buf)); } catch (e) {}
    this._enviar(ev);
  },
  _enviar(ev) {
    // best-effort, no bloquea el juego. sendBeacon no tira error si el endpoint
    // todavía no existe (queda encolado); el sink del server es el próximo paso.
    try {
      if (navigator.sendBeacon)
        navigator.sendBeacon("telemetria", new Blob([JSON.stringify(ev)], { type: "application/json" }));
    } catch (e) { /* sin telemetría remota para este token: queda en el buffer local */ }
  },
};

/* ── sonidos sintetizados (WebAudio — sin assets, latencia cero) ── */
const Sfx = {
  ctx: null, on: true,
  _ctx() {
    if (!this.ctx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (AC) this.ctx = new AC();
    }
    if (this.ctx && this.ctx.state === "suspended") this.ctx.resume();
    return this.ctx;
  },
  _nota(f, t0, dur, tipo, vol) {
    const c = this._ctx();
    if (!c || !this.on) return;
    const o = c.createOscillator(), g = c.createGain();
    o.type = tipo || "triangle"; o.frequency.value = f;
    g.gain.setValueAtTime(0, c.currentTime + t0);
    g.gain.linearRampToValueAtTime(vol || 0.16, c.currentTime + t0 + 0.015);
    g.gain.exponentialRampToValueAtTime(0.001, c.currentTime + t0 + dur);
    o.connect(g).connect(c.destination);
    o.start(c.currentTime + t0); o.stop(c.currentTime + t0 + dur + 0.05);
  },
  ok() { this._nota(660, 0, 0.12); this._nota(880, 0.09, 0.2); },
  bien() { [523, 659, 784, 1047].forEach((f, i) => this._nota(f, i * 0.07, 0.18)); },
  casi() { this._nota(300, 0, 0.15, "sine", 0.1); this._nota(260, 0.12, 0.2, "sine", 0.09); },
  pop() { this._nota(900 + Math.random() * 300, 0, 0.07, "square", 0.06); },
  tick(i) { this._nota(523 * Math.pow(2, (i % 8) / 12 * 2), 0, 0.12, "triangle", 0.13); },
  flip() { this._nota(500, 0, 0.06, "sine", 0.07); this._nota(700, 0.05, 0.06, "sine", 0.07); },
  fanfarria() {
    [523, 659, 784, 1047, 784, 1047, 1319].forEach((f, i) => this._nota(f, i * 0.09, 0.25));
    this._nota(262, 0.55, 0.5, "sine", 0.1);
  },
};

/* ── confeti (canvas liviano, colores de la paleta del tema) ── */
const Confeti = {
  cv: null, cx: null, parts: [], corriendo: false,
  init() { this.cv = $("#confeti"); this.cx = this.cv.getContext("2d"); },
  tirar(n) {
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const pal = [D.paleta.ac, D.paleta.ac2, D.paleta.star, "#6EC1E4", "#F78FB3"];
    this.cv.width = innerWidth; this.cv.height = innerHeight;
    for (let i = 0; i < (n || 120); i++) {
      this.parts.push({
        x: Math.random() * innerWidth, y: -20 - Math.random() * innerHeight * 0.4,
        vx: (Math.random() - 0.5) * 3, vy: 2.5 + Math.random() * 4,
        w: 7 + Math.random() * 7, h: 10 + Math.random() * 8,
        rot: Math.random() * Math.PI, vr: (Math.random() - 0.5) * 0.25,
        color: pal[i % pal.length],
      });
    }
    if (!this.corriendo) { this.corriendo = true; requestAnimationFrame(() => this.paso()); }
  },
  paso() {
    const c = this.cx;
    c.clearRect(0, 0, this.cv.width, this.cv.height);
    this.parts = this.parts.filter((p) => p.y < this.cv.height + 30);
    for (const p of this.parts) {
      p.x += p.vx; p.y += p.vy; p.rot += p.vr;
      c.save(); c.translate(p.x, p.y); c.rotate(p.rot);
      c.fillStyle = p.color; c.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
      c.restore();
    }
    if (this.parts.length) requestAnimationFrame(() => this.paso());
    else { this.corriendo = false; c.clearRect(0, 0, this.cv.width, this.cv.height); }
  },
};

/* ── frases de aliento (elogian el ESFUERZO, voseo rioplatense) ── */
const FRASES_BIEN = ["¡Muy bien!", "¡Genial!", "¡Lo lograste!", "¡Excelente!", "¡Así se hace!", "¡Qué bien!"];
const FRASES_FESTEJO = [
  "¡Cuánto esfuerzo le pusiste!", "¡Lo resolviste vos!", "¡Qué bien pensaste!",
  "¡Sos de no rendirte!", "¡Jugaste con mucha atención!",
];
const FRASES_CASI = ["¡Casi! Probá otra vez", "Mmm… ¡probá de nuevo!", "¡Ya casi!"];

function toast(txt) {
  const t = $("#toast");
  t.textContent = txt;
  t.classList.remove("ver");
  void t.offsetWidth;        // reinicia la animación
  t.classList.add("ver");
}

/* ── Capa 0 · C3 (docs/auditoria-dc-caba/): explicación del PORQUÉ en el error.
   El toast dura 1.1s (muy poco para leer); esto es una burbuja aparte que dura
   ~4s y se va al acertar. Solo aparece si el juego pasa un motivo a ctx.casi();
   los juegos que llaman casi() sin motivo (los viejos) no muestran nada. ── */
let _explicaTimer = null;
function mostrarExplicacion(txt) {
  let e = document.getElementById("explica");
  if (!e) {
    e = document.createElement("div");
    e.id = "explica";
    e.setAttribute("role", "status");
    e.style.cssText = "position:fixed;left:50%;bottom:88px;transform:translateX(-50%);"
      + "max-width:min(92vw,520px);background:#2b2b3a;color:#fff;padding:13px 18px;"
      + "border-radius:16px;font-size:17px;line-height:1.35;text-align:center;"
      + "box-shadow:0 8px 30px rgba(0,0,0,.35);z-index:60;opacity:0;"
      + "transition:opacity .2s;pointer-events:none";
    document.body.appendChild(e);
  }
  e.textContent = "💡 " + txt;
  requestAnimationFrame(() => { e.style.opacity = "1"; });
  clearTimeout(_explicaTimer);
  _explicaTimer = setTimeout(() => { e.style.opacity = "0"; }, 4200);
  reproducirConsigna(txt);   // Capa 0 · C3: la explicación se LEE en voz alta (voz argentina vía /tts)
}
function ocultarExplicacion() {
  const e = document.getElementById("explica");
  if (e) e.style.opacity = "0";
}

/* ── diploma de logro (14-jul-2026): cuaderno COMPLETO, sin errores en
   ningún juego (3 estrellas = 0 fallos, mismo criterio que Shell.ctx().win).
   Progreso vive solo en localStorage (Store) — no hay servidor que lo
   valide, mismo nivel de confianza que el resto de los links por token. */
function juegosDelMenu() {
  return D.menu.filter((m) => GAMES[m.id] && P.length >= (GAMES[m.id].minP || 0));
}
function todoCompleto() {
  const js = juegosDelMenu();
  return js.length > 0 && js.every((m) => Store.stars(m.id) === 3);
}
function certificadoUrl() {
  return "certificado.png?nombre=" + encodeURIComponent(Store.data.activeProfile || "");
}

/* ── shell de juego: consigna + progreso + festejo ── */
const Shell = {
  actual: null, nivelActual: null, fallos: 0, _rondas: 0, _nuevoLogro: false,
  // Capa 0 · C1: estado de PRIMER INTENTO por ronda (lo consume la telemetría
  // Tel y, más adelante, la compuerta de dominio C2).
  _itemId: null, _rondaResp: false, _rondaIdx: 0, primerOk: 0, primerTotal: 0,
  abrir(id) {
    const item = D.menu.find((m) => m.id === id);
    if (!item || !GAMES[id]) return;
    this.actual = id; this.fallos = 0;
    this._itemId = null; this._rondaResp = false; this._rondaIdx = 0;
    this.primerOk = 0; this.primerTotal = 0;
    $("#btnAtras").classList.add("ver");
    const stage = $("#stage");
    stage.innerHTML = "";
    stage.appendChild(el("div", "", `
      <div id="consigna"><img class="pista" id="consignaPista" alt="" style="display:none">
        <div class="texto" id="consignaTexto"></div></div>
      <div id="progreso"></div><div id="juego"></div>`));
    scrollTo(0, 0);
    GAMES[id].crear(this.ctx(item));
    requestAnimationFrame(ajustarAlto);
  },
  ctx(item) {
    const self = this;
    // Capa 0 · C1+C5: registra el resultado de la PRIMERA respuesta de la ronda
    // (closure, robusta ante cómo cada juego invoque bien/casi) y lo manda a Tel.
    // No cambia ninguna mecánica ni lo que ve el chico.
    const registrar = (ok, motivo) => {
      const primer = !self._rondaResp;
      self._rondaResp = true;
      if (primer) { self.primerTotal++; if (ok) self.primerOk++; }
      Tel.push({
        j: self.actual,
        it: self._itemId != null ? self._itemId : (self.actual + "#" + self._rondaIdx),
        edad: (D && D.edad) || null,
        ok: ok, primer: primer, motivo: motivo || null, t: Date.now(),
      });
    };
    return {
      cfg: item.cfg || {}, D, P,
      juego: $("#juego"),
      consigna(txt, pistaSrc) {
        $("#consignaTexto").innerHTML = txt;
        const p = $("#consignaPista");
        if (pistaSrc) { p.src = pistaSrc; p.style.display = ""; }
        else p.style.display = "none";
        reproducirConsigna(txt);
      },
      rondas(n) {
        self._rondas = n;
        const pr = $("#progreso");
        pr.innerHTML = "";
        for (let i = 0; i < n; i++) pr.appendChild(el("i"));
        this.ronda(0);
      },
      // Capa 0 · C1: un juego puede declarar el id del ítem de la ronda para
      // etiquetar la telemetría con precisión; si no lo hace, se usa un id
      // sintético "<juego>#<ronda>". Aditivo: el que no lo llama anda igual.
      item(id) { self._itemId = id; },
      ronda(i) {
        self._rondaIdx = i;
        self._rondaResp = false;   // ronda nueva → la próxima respuesta es "primer intento"
        ocultarExplicacion();
        document.querySelectorAll("#progreso i").forEach((d, j) => {
          d.className = j < i ? "hecho" : (j === i ? "actual" : "");
        });
      },
      bien(txt) { registrar(true); ocultarExplicacion(); Sfx.ok(); toast(txt || FRASES_BIEN[rint(0, FRASES_BIEN.length - 1)]); },
      casi(motivo) { registrar(false, motivo); self.fallos++; Sfx.casi(); if (motivo) mostrarExplicacion(motivo); },
      win(estrellas) {
        // Capa 0 · C2 (compuerta de dominio, docs/auditoria-dc-caba/): las
        // estrellas miden DOMINIO real —aciertos al PRIMER intento— no "completé
        // con pocos fallos" (que se lograba por eliminación / a la segunda). El
        // festejo de COMPLETAR se mantiene igual (el chico siempre lo recibe);
        // lo que cambia es cuántas estrellas.
        //   - estrella explícita del juego (ctx.win(n): sopa, laberinto…) → se respeta
        //   - juego con rondas registradas (C1) → por precisión de 1er intento
        //   - juego sin rondas registradas (colorear, etc.) → fallback viejo por fallos
        // El "sello de dominado sostenido en 2 sesiones" + diploma es el próximo
        // incremento (necesita timestamps entre sesiones); esto ya deja el dato.
        let e;
        if (estrellas !== undefined) {
          e = estrellas;
        } else if (self.primerTotal > 0) {
          const acc = self.primerOk / self.primerTotal;
          e = acc >= 0.9 ? 3 : (acc >= 0.7 ? 2 : 1);
        } else {
          e = self.fallos === 0 ? 3 : (self.fallos <= 2 ? 2 : 1);
        }
        const yaEstabaCompleto = todoCompleto();
        Store.setStars(self.actual, e);
        // Capa 0 · sello de dominio sostenido: registra el día si fue nivel de
        // dominio (3★) y avisa si recién ahora quedó 'dominado'/'consolidado'.
        const evtDom = e >= 3 ? Store.registrarDominio(self.actual, e) : null;
        if (!yaEstabaCompleto && todoCompleto()) self._nuevoLogro = true;
        pintarHeader();
        festejar(e, evtDom);
        // activación escalable por niveles: si al ganar (3★) quedó DOMINADO el
        // nivel de esta actividad (≥80% con 3★) y hay un nivel siguiente, avisar
        // al adulto UNA vez (motivo='domino' → la tienda le manda el mail) y
        // ofrecerle al chico desbloquearlo. Solo con premium_on → los links
        // normales no ven nada de esto.
        if (e >= 3 && D.premium_on && item) {
          const n = item.nivel || 1;
          const haySiguiente = (D.niveles || []).some((x) => x.nivel === n + 1);
          if (haySiguiente && nivelDominado(n) && !yaAvisado("domino_" + n)) {
            pedirDesbloqueo(n + 1, "domino");
            if (nivelBloqueado(n + 1)) setTimeout(() => ofertaNivel(n + 1), 3200);
          }
        }
      },
      confeti(n) { Confeti.tirar(n); },
    };
  },
};

function festejar(estrellas, evtDom) {
  Sfx.fanfarria();
  Confeti.tirar(evtDom ? 220 : 140);   // extra confeti cuando quedó el sello
  const nombre = Store.data.activeProfile;
  // Capa 0 · el festejo del SELLO (dominado/consolidado) pisa el festejo común.
  if (evtDom === "dominado") {
    $("#festejoTitulo").textContent = nombre ? `🏅 ¡Lo dominaste, ${nombre}!` : "🏅 ¡Lo dominaste!";
    $("#festejoFrase").textContent = "Te salió bien en dos días distintos: ya lo sabés de verdad.";
  } else if (evtDom === "consolidado") {
    $("#festejoTitulo").textContent = nombre ? `🌟 ¡Sos un crack, ${nombre}!` : "🌟 ¡Sos un crack!";
    $("#festejoFrase").textContent = "Lo repasaste y te lo acordás perfecto. ¡Consolidado!";
  } else {
    $("#festejoTitulo").textContent = nombre ? `¡Muy bien, ${nombre}!` : "¡Muy bien!";
    $("#festejoFrase").textContent = FRASES_FESTEJO[rint(0, FRASES_FESTEJO.length - 1)];
  }
  const cont = $("#festejoEstrellas");
  cont.innerHTML = "";
  for (let i = 0; i < 3; i++) {
    const s = el("span", "", i < estrellas ? "⭐" : "☆");
    cont.appendChild(s);
    if (i < estrellas) setTimeout(() => { s.classList.add("gana"); Sfx.tick(i * 3); }, 450 + i * 380);
    else { s.style.opacity = 0.35; }
  }
  $("#festejo").classList.add("ver");
}

function cerrarFestejo() { $("#festejo").classList.remove("ver"); }

function mostrarLogro() {
  $("#btnVerLogro").href = certificadoUrl();
  Confeti.tirar(220);
  Sfx.fanfarria();
  $("#logro").classList.add("ver");
}
function cerrarLogro() { $("#logro").classList.remove("ver"); }

/* ── selector de jugador: varios chicos, un solo link (token) ── */
function abrirPerfil() {
  const lista = $("#perfilLista");
  lista.innerHTML = "";
  Object.keys(Store.data.profiles).forEach((n) => {
    const b = el("button", "btn suave");
    b.type = "button";
    b.textContent = n;
    b.addEventListener("click", () => elegirPerfil(n));
    lista.appendChild(b);
  });
  // sin perfil activo (primera vez) no hay nada que cancelar
  $("#perfilCancelar").style.display = Store.data.activeProfile ? "" : "none";
  // Nombre de la compra (14-jul-2026) como DEFAULT del primer perfil, no
  // como personalización dura: solo se precarga si todavía no hay ningún
  // perfil creado — así el caso de 1 solo chico es un solo toque ("¡Jugar!"
  // sin escribir nada), y si juega un segundo chico en la misma casa, esta
  // misma pantalla ya lo resuelve (perfil 1 queda de botón arriba, el
  // input para el nombre nuevo arranca vacío, no repite el de la compra).
  const esElPrimerPerfil = Object.keys(Store.data.profiles).length === 0;
  $("#perfilInput").value = esElPrimerPerfil ? (D.nombre || "") : "";
  $("#perfil").classList.add("ver");
  $("#perfilInput").focus();
  // cursor al final (no seleccionar todo el texto): se entiende que se
  // puede seguir escribiendo/borrar sin que el nombre completo se vea
  // "marcado" en azul (Pablo, 14-jul-2026 — encontró raro el resaltado)
  const largo = $("#perfilInput").value.length;
  $("#perfilInput").setSelectionRange(largo, largo);
}
function cerrarPerfil() { $("#perfil").classList.remove("ver"); }
function elegirPerfil(nombre) {
  nombre = (nombre || "").trim().slice(0, 20);
  if (!nombre) return;
  if (!Store.data.profiles[nombre]) Store.data.profiles[nombre] = { stars: {} };
  Store.data.activeProfile = nombre;
  Store.save();
  cerrarPerfil();
  pintarHeader();
  pintarMenu();
}

/* ── menú principal ── */
function pintarHeader() {
  $("#totalEstrellas").textContent = Store.total();
  $("#hdrNombre").textContent = Store.data.activeProfile ? `¡Hola, ${Store.data.activeProfile}!` : "¡Hola!";
  $("#hdrSub").textContent = `${D.tema_nombre} · Casatridimensional`;
  $("#mascoHdr").src = P[0];
  $("#mascoFestejo").src = P[0];
}

/* ── Activación escalable por NIVELES (19-jul-2026, docs/auditoria-dc-caba/):
   las actividades se agrupan en niveles (1 = gratis del kit; 2 y 3 = premium con
   candado). Todo gateado por D.premium_on: los links normales no lo tienen →
   ven el menú plano de siempre, cero cambio. El chico nunca compra: pide/avisa
   y el adulto desbloquea desde el mail (esa parte vive en la tienda). ── */
function nivelMax() { return D.nivel_max || 1; }
function nivelBloqueado(n) { return !!(D.premium_on && n > nivelMax()); }
function itemsDeNivel(n) {
  return D.menu.filter((m) => (m.nivel || 1) === n && GAMES[m.id] && P.length >= (GAMES[m.id].minP || 0));
}
function nivelDominado(n) {
  const items = itemsDeNivel(n);
  if (!items.length) return false;
  const dom = items.filter((m) => Store.stars(m.id) >= 3).length;
  return dom / items.length >= 0.8;
}
// evita avisar más de una vez por (link, evento): el mail al adulto sale una vez.
function yaAvisado(clave) {
  try {
    const k = "act_avisos_" + location.pathname + "_" + (Store.data.activeProfile || "");
    const s = JSON.parse(localStorage.getItem(k) || "{}");
    if (s[clave]) return true;
    s[clave] = 1; localStorage.setItem(k, JSON.stringify(s));
    return false;
  } catch (e) { return false; }
}
function pedirDesbloqueo(nivel, motivo) {
  try {
    fetch("quiero-desbloquear", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ nivel: nivel, motivo: motivo || "pidio" }) });
  } catch (e) { /* best-effort: si no llega, no rompe nada */ }
}
function ofertaNivel(n) {
  const nv = (D.niveles || []).find((x) => x.nivel === n);
  if (!nv) return;
  let ov = document.getElementById("oferta");
  if (!ov) { ov = el("div"); ov.id = "oferta"; ov.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.55);display:grid;place-items:center;z-index:80;padding:16px"; document.body.appendChild(ov); }
  ov.innerHTML = "";
  const card = el("div");
  card.style.cssText = "background:var(--card,#fff);color:var(--ink,#222);max-width:340px;padding:24px 22px;border-radius:22px;text-align:center;box-shadow:0 14px 44px rgba(0,0,0,.45)";
  card.innerHTML = "<div style='font-size:46px'>🌟</div><h2 style='margin:8px 0'>¡Dominaste tu nivel!</h2><p style='opacity:.85;font-size:15px;line-height:1.4'>Ya estás listo para el <b>Nivel " + n + " · " + nv.nombre + "</b>. ¿Le avisamos a tu adulto para que lo abra?</p>";
  const bSi = el("button", "", "📩 ¡Avisarle a mi adulto!");
  bSi.style.cssText = "display:block;width:100%;padding:14px;margin-top:14px;border:none;border-radius:14px;background:var(--ac,#4a90d9);color:#fff;font-weight:700;font-size:16px;cursor:pointer";
  const bNo = el("button", "", "Ahora no");
  bNo.style.cssText = "display:block;width:100%;padding:10px;margin-top:8px;border:none;background:transparent;color:inherit;cursor:pointer;opacity:.7";
  bSi.addEventListener("click", () => { pedirDesbloqueo(n, "pidio"); Sfx.fanfarria && Sfx.fanfarria(); card.innerHTML = "<div style='font-size:46px'>🎉</div><h2 style='margin:8px 0'>¡Listo!</h2><p style='opacity:.85;line-height:1.4'>Le avisamos a tu adulto. Cuando lo abra, vas a poder jugar el nivel nuevo.</p>"; setTimeout(() => ov.remove(), 2800); });
  bNo.addEventListener("click", () => ov.remove());
  card.appendChild(bSi); card.appendChild(bNo); ov.appendChild(card);
}

// ── navegación del menú ──────────────────────────────────────────────
// premium_on → entra directo a las actividades del nivel, con la BARRA DE
// NIVELES fija arriba (el actual + los candados, siempre a la vista); si no,
// el menú plano de siempre.
function nivelInicial() {
  // arranca en el nivel donde está el chico (el más alto que tenga desbloqueado)
  const desbloq = (D.niveles || []).filter((x) => !nivelBloqueado(x.nivel)).map((x) => x.nivel);
  return desbloq.length ? Math.max.apply(null, desbloq) : 1;
}
function pintarMenu() {
  if (D.premium_on && (D.niveles || []).length > 1) return pintarNivel(nivelInicial());
  return pintarMenuPlano(D.menu);
}
// "atrás" de un juego: si está en un nivel, vuelve a las actividades de ese
// nivel; si no, al menú.
function volverMenu() {
  if (D.premium_on && Shell.nivelActual) return pintarNivel(Shell.nivelActual);
  return pintarMenu();
}

// la barra de niveles fija: chip por nivel (el actual resaltado, los bloqueados
// con 🔒). Tocar otro nivel abierto lo abre; tocar uno con candado → avisar.
function barraNiveles(actual) {
  const bar = el("div"); bar.id = "nivelbar";
  (D.niveles || []).forEach((x) => {
    const bloq = nivelBloqueado(x.nivel);
    const chip = el("button", "nivchip" + (x.nivel === actual ? " on" : "") + (bloq ? " bloq" : ""));
    chip.type = "button";
    chip.innerHTML = (bloq ? "🔒 " : x.icono + " ") + "Nivel " + x.nivel;
    chip.addEventListener("click", () => {
      Sfx.pop();
      if (x.nivel === actual) return;
      if (bloq) pantallaCandado(x); else pintarNivel(x.nivel);
    });
    bar.appendChild(chip);
  });
  return bar;
}

function pintarNivel(n) {
  Shell.actual = null; Shell.nivelActual = n;
  $("#btnAtras").classList.remove("ver");
  const nv = (D.niveles || []).find((x) => x.nivel === n) || { nombre: "", icono: "🌱" };
  const stage = $("#stage"); stage.innerHTML = "";
  stage.appendChild(barraNiveles(n));         // ← barra fija arriba
  const bienv = el("div"); bienv.id = "bienvenida";
  bienv.innerHTML = `<h1>${nv.icono} Nivel ${n} · ${nv.nombre}</h1><p>Elegí una actividad y ganá estrellas ⭐</p>
    <a id="pillLogro" class="${todoCompleto() ? "ver" : ""}" href="${certificadoUrl()}" target="_blank" rel="noopener">🏆 Ver mi diploma</a>`;
  stage.appendChild(bienv);
  pintarMenuPlano(itemsDeNivel(n), stage);
}

// pinta una grilla de actividades (lista ya filtrada). Reusa la misma carta.
function pintarMenuPlano(items, stage) {
  Shell.actual = null;
  if (!stage) {
    Shell.nivelActual = null;
    $("#btnAtras").classList.remove("ver");
    stage = $("#stage"); stage.innerHTML = "";
    const bienv = el("div"); bienv.id = "bienvenida";
    bienv.innerHTML = `<h1>${D.titulo}</h1><p>Elegí un juego y ganá estrellas ⭐</p>
      <a id="pillLogro" class="${todoCompleto() ? "ver" : ""}" href="${certificadoUrl()}" target="_blank" rel="noopener">🏆 Ver mi diploma</a>`;
    stage.appendChild(bienv);
  }
  // Capa 0 · nota de repaso del día (arriba del menú) si hay algo para repasar.
  const repasos = items.filter((m) => GAMES[m.id] && Store.repasoPendiente(m.id));
  if (repasos.length) {
    stage.appendChild(el("div", "repaso-nota",
      `🔁 Tenés ${repasos.length} ${repasos.length === 1 ? "repaso" : "repasos"} para hacer hoy — ¡a ver si te lo acordás!`));
  }
  const menu = el("div"); menu.id = "menu";
  items.forEach((m, i) => {
    if (!GAMES[m.id]) return;
    if (P.length < (GAMES[m.id].minP || 0)) return;   // tema con pocos personajes
    const st = Store.stars(m.id);
    const sello = Store.sello(m.id);           // Capa 0 · sello sostenido
    const repaso = Store.repasoPendiente(m.id);
    const c = el("button", "carta" + (repaso ? " repaso" : ""));
    // las cartas alternan emoji y personajes del tema para que el menú viva
    const conSprite = i % 3 === 1 && P[(i / 3 | 0) + 1];
    let est;
    if (repaso) est = "🔁 ¡Repasá!";
    else if (sello === "consolidado") est = "🌟 ¡Lo sabés!";
    else if (sello === "dominado") est = "🏅 Dominado";
    else est = st ? "⭐".repeat(st) : "&nbsp;";
    c.innerHTML = `
      <div class="icono">${conSprite ? `<img src="${P[(i / 3 | 0) + 1]}" alt="">` : m.icono}</div>
      <div class="nombre">${m.titulo}</div>
      <div class="mini-est">${est}</div>
      ${conSprite ? `<div class="chip">${m.icono}</div>` : ""}`;
    c.addEventListener("click", () => { Sfx.pop(); Shell.abrir(m.id); });
    menu.appendChild(c);
  });
  stage.appendChild(menu);
}

function pantallaCandado(nv) {
  const volverA = Shell.nivelActual || nivelInicial();
  Shell.actual = null; Shell.nivelActual = null;
  $("#btnAtras").classList.remove("ver");
  const stage = $("#stage"); stage.innerHTML = "";
  stage.appendChild(barraNiveles(nv.nivel));   // barra fija arriba (candado actual resaltado)
  const box = el("div"); box.id = "candado";
  const volverBtn = () => {
    const v = el("button", "btn suave", "‹ Volver a jugar");
    v.type = "button";
    v.addEventListener("click", () => { Sfx.pop(); pintarNivel(volverA); });
    return v;
  };
  box.innerHTML = `
    <div class="cand-ico">🔒</div>
    <h1>Nivel ${nv.nivel} · ${nv.nombre}</h1>
    <p>Este nivel está guardado. Pedile a tu grande que lo abra — le mandamos un mail para que pueda hacerlo.</p>`;
  const bSi = el("button", "btn verde", "📩 Avisarle a mi adulto");
  bSi.type = "button";
  bSi.addEventListener("click", () => {
    pedirDesbloqueo(nv.nivel, "pidio");
    Sfx.fanfarria && Sfx.fanfarria();
    box.innerHTML = `<div class="cand-ico">🎉</div><h1>¡Listo!</h1>
      <p>Le avisamos a tu adulto. Cuando lo abra, vas a poder jugar el Nivel ${nv.nivel}.</p>`;
    box.appendChild(volverBtn());
  });
  box.appendChild(bSi);
  box.appendChild(el("div", "cand-nota", "💛 Vos no comprás nada — lo hace tu adulto desde su mail"));
  box.appendChild(volverBtn());
  stage.appendChild(box);
}

/* ── arranque ── */
async function boot() {
  const r = await fetch("data.json");
  D = await r.json();
  P = D.personajes;
  // paleta del tema → CSS vars (todo el look sale de acá)
  const root = document.documentElement;
  for (const [k, v] of Object.entries(D.paleta)) root.style.setProperty("--" + k, v);
  document.title = D.titulo + " · Casatridimensional";
  let meta = document.querySelector('meta[name="theme-color"]');
  if (!meta) { meta = document.createElement("meta"); meta.name = "theme-color"; document.head.appendChild(meta); }
  meta.content = D.paleta.ac;
  Store.load();
  Sfx.on = Store.data.sound !== false;
  $("#btnSonido").textContent = Sfx.on ? "🔊" : "🔇";
  Confeti.init();
  cargarAudioManifest();   // en paralelo, no bloquea el arranque
  // precarga de personajes (los juegos los usan al instante)
  await Promise.all(P.map((src) => new Promise((res) => {
    const im = new Image(); im.onload = im.onerror = res; im.src = src;
  })));
  $("#cargando").remove();
  if (Store.data.activeProfile && Store.data.profiles[Store.data.activeProfile]) {
    pintarHeader(); pintarMenu();
  } else {
    abrirPerfil();   // primera vez con este link: preguntar quién juega
  }

  $("#btnAtras").addEventListener("click", () => { Sfx.pop(); volverMenu(); });
  $("#hdrTitulo").addEventListener("click", () => { Sfx.pop(); abrirPerfil(); });
  $("#perfilJugar").addEventListener("click", () => elegirPerfil($("#perfilInput").value));
  $("#perfilInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter") elegirPerfil($("#perfilInput").value);
  });
  $("#perfilCancelar").addEventListener("click", cerrarPerfil);
  $("#btnSonido").addEventListener("click", () => {
    Sfx.on = !Sfx.on;
    Store.data.sound = Sfx.on; Store.save();
    $("#btnSonido").textContent = Sfx.on ? "🔊" : "🔇";
    if (!Sfx.on && vozActual) { vozActual.pause(); vozActual = null; }
    if (Sfx.on) Sfx.pop();
  });
  $("#btnSeguir").addEventListener("click", () => {
    cerrarFestejo(); volverMenu();
    if (Shell._nuevoLogro) { Shell._nuevoLogro = false; mostrarLogro(); }
  });
  $("#btnOtraVez").addEventListener("click", () => {
    const id = Shell.actual;
    cerrarFestejo();
    if (id) Shell.abrir(id);
  });
  $("#btnCerrarLogro").addEventListener("click", cerrarLogro);
  addEventListener("resize", () => requestAnimationFrame(ajustarAlto));
  ajustarAlto();
  // iOS: desbloquear el audio en el primer toque
  addEventListener("pointerdown", function una() {
    Sfx._ctx(); removeEventListener("pointerdown", una);
  }, { once: true });
}
document.addEventListener("DOMContentLoaded", boot);

/* ═══════════ JUEGOS — cada uno registra GAMES[id] = {crear(ctx)} ═══════════ */

/* ── MEMOTEST — memoria de trabajo. Pares de personajes del tema. ── */
GAMES.memotest = {
  minP: 3,
  crear(ctx) {
    const pares = Math.min(ctx.cfg.pares || 6, P.length);
    ctx.consigna("Encontrá las parejas");
    ctx.rondas(pares);
    const sprites = sample(P, pares);
    const mazo = shuffle(sprites.concat(sprites).map((s, i) => ({ s, id: i })));
    const cols = pares <= 3 ? 3 : 4;
    const grid = el("div"); grid.id = "memo";
    grid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    ctx.juego.appendChild(el("div", "tablero")).appendChild(grid);
    let abiertas = [], bloqueado = false, halladas = 0;
    requestAnimationFrame(() => {
      const disp = innerHeight - grid.getBoundingClientRect().top - 18;
      const filas = Math.ceil(mazo.length / cols);
      const maxW = Math.min(660, (disp - (filas - 1) * 10) * cols / (filas * 4 / 3));
      if (maxW > 220) grid.style.maxWidth = maxW + "px";
      grid.style.margin = "0 auto";
    });
    mazo.forEach((carta) => {
      const c = el("button", "cartaMemo", `
        <div class="cara dorso">★</div>
        <div class="cara frente"><img src="${carta.s}" alt=""></div>`);
      c.addEventListener("click", async () => {
        if (bloqueado || c.classList.contains("abierta")) return;
        Sfx.flip();
        c.classList.add("abierta");
        abiertas.push({ c, s: carta.s });
        if (abiertas.length < 2) return;
        bloqueado = true;
        const [a, b] = abiertas;
        if (a.s === b.s) {
          a.c.classList.add("lista"); b.c.classList.add("lista");
          halladas++;
          ctx.ronda(halladas);
          Sfx.ok();
          if (halladas === pares) { await espera(600); ctx.win(); }
        } else {
          ctx.casi();
          await espera(850);
          a.c.classList.remove("abierta"); b.c.classList.remove("abierta");
        }
        abiertas = []; bloqueado = false;
      });
      grid.appendChild(c);
    });
  },
};

/* ── SOPA DE LETRAS — arrastrá sobre las letras (8 direcciones, ida o vuelta) ── */
GAMES.sopa = {
  crear(ctx) {
    const s = D.sopas[rint(0, D.sopas.length - 1)];
    if (!s) return;
    const n = s.n;
    ctx.consigna("Encontrá las palabras escondidas");
    ctx.rondas(s.palabras.length);
    const wrap = el("div"); wrap.id = "sopaWrap";
    const tab = el("div", "tablero");
    const grid = el("div", "lienzo"); grid.id = "sopa";
    grid.style.gridTemplateColumns = `repeat(${n}, 1fr)`;
    const celdas = [];
    for (let y = 0; y < n; y++)
      for (let x = 0; x < n; x++) {
        const c = el("div", "celda", s.filas[y][x]);
        c.dataset.x = x; c.dataset.y = y;
        grid.appendChild(c); celdas.push(c);
      }
    tab.appendChild(grid); wrap.appendChild(tab);
    const lista = el("div"); lista.id = "sopaPalabras";
    const chips = {};
    s.lindas.forEach((linda, i) => {
      const w = s.palabras[i];
      chips[w] = el("div", "palabra", linda);
      lista.appendChild(chips[w]);
    });
    wrap.appendChild(lista);
    ctx.juego.appendChild(wrap);
    requestAnimationFrame(() => {
      const disp = innerHeight - grid.getBoundingClientRect().top - 14;
      const lado = Math.min(620, Math.max(260, disp - 118));   // 118 ≈ lista de palabras
      wrap.style.maxWidth = lado + "px";
      wrap.style.margin = "0 auto";
    });

    const at = (x, y) => celdas[y * n + x];
    const halladas = new Set();
    let ancla = null, marcadas = [];

    const celdaDesdeEvento = (ev) => {
      const t = document.elementFromPoint(ev.clientX, ev.clientY);
      return t && t.classList && t.classList.contains("celda") ? t : null;
    };
    const linea = (x0, y0, x1, y1) => {
      // recta "imantada" a las 8 direcciones — perdona el dedo torcido
      let dx = x1 - x0, dy = y1 - y0;
      const len = Math.max(Math.abs(dx), Math.abs(dy));
      if (!len) return [[x0, y0]];
      const sx = Math.abs(dx) > len / 2 ? Math.sign(dx) : 0;
      const sy = Math.abs(dy) > len / 2 ? Math.sign(dy) : 0;
      const out = [];
      for (let i = 0; i <= len; i++) {
        const x = x0 + sx * i, y = y0 + sy * i;
        if (x < 0 || y < 0 || x >= n || y >= n) break;
        out.push([x, y]);
      }
      return out;
    };
    const limpiar = () => { marcadas.forEach((c) => c.classList.remove("marca")); marcadas = []; };
    const marcar = (cs) => {
      limpiar();
      cs.forEach(([x, y]) => {
        const c = at(x, y);
        if (!c.classList.contains("hallada")) c.classList.add("marca");
        marcadas.push(c);
      });
    };

    grid.addEventListener("pointerdown", (ev) => {
      const c = celdaDesdeEvento(ev);
      if (!c) return;
      grid.setPointerCapture(ev.pointerId);
      ancla = [+c.dataset.x, +c.dataset.y];
      marcar([ancla]);
    });
    grid.addEventListener("pointermove", (ev) => {
      if (!ancla) return;
      const c = celdaDesdeEvento(ev);
      if (c) marcar(linea(ancla[0], ancla[1], +c.dataset.x, +c.dataset.y));
    });
    const soltar = () => {
      if (!ancla) return;
      const cs = marcadas.map((c) => [+c.dataset.x, +c.dataset.y]);
      const txt = cs.map(([x, y]) => s.filas[y][x]).join("");
      const rev = txt.split("").reverse().join("");
      const hit = s.palabras.find((w) => !halladas.has(w) && (w === txt || w === rev));
      if (hit) {
        halladas.add(hit);
        marcadas.forEach((c) => { c.classList.remove("marca"); c.classList.add("hallada"); });
        chips[hit].classList.add("hallada");
        ctx.ronda(halladas.size);
        ctx.bien();
        if (halladas.size === s.palabras.length) setTimeout(() => ctx.win(3), 700);
      } else {
        if (cs.length > 2) ctx.casi();
        limpiar();
      }
      ancla = null; marcadas = [];
    };
    grid.addEventListener("pointerup", soltar);
    grid.addEventListener("pointercancel", soltar);
  },
};

/* ── LABERINTO — llevá al personaje arrastrando; las paredes frenan solas ── */
GAMES.laberinto = {
  crear(ctx) {
    const labs = D.laberintos.slice(ctx.cfg.desde || 0);
    ctx.rondas(labs.length);
    let nivel = 0;
    const arrancar = () => {
      ctx.ronda(nivel);
      ctx.consigna("Llevá a tu amigo hasta la estrella ⭐", P[nivel % P.length]);
      ctx.juego.innerHTML = "";
      const lab = labs[nivel];
      const n = lab.n, C = 64, M = 10, S = n * C + M * 2;
      const NS = "http://www.w3.org/2000/svg";
      const svg = document.createElementNS(NS, "svg");
      svg.setAttribute("viewBox", `0 0 ${S} ${S}`);
      svg.setAttribute("class", "svgJuego lienzo");
      // paredes desde el bitmask (N=1 S=2 E=4 W=8)
      let d = "";
      const X = (x) => M + x * C, Y = (y) => M + y * C;
      for (let y = 0; y < n; y++)
        for (let x = 0; x < n; x++) {
          const b = lab.celdas[y][x];
          if (b & 1) d += `M${X(x)} ${Y(y)}h${C}`;
          if (b & 8) d += `M${X(x)} ${Y(y)}v${C}`;
          if (y === n - 1 && (b & 2)) d += `M${X(x)} ${Y(y + 1)}h${C}`;
          if (x === n - 1 && (b & 4)) d += `M${X(x + 1)} ${Y(y)}v${C}`;
        }
      const muros = document.createElementNS(NS, "path");
      muros.setAttribute("d", d);
      muros.setAttribute("stroke", D.paleta.ink);
      muros.setAttribute("stroke-width", 9);
      muros.setAttribute("stroke-linecap", "round");
      muros.setAttribute("fill", "none");
      // rastro del recorrido
      const rastro = document.createElementNS(NS, "polyline");
      rastro.setAttribute("stroke", D.paleta.ac2);
      rastro.setAttribute("stroke-width", 14);
      rastro.setAttribute("stroke-linecap", "round");
      rastro.setAttribute("stroke-linejoin", "round");
      rastro.setAttribute("fill", "none");
      rastro.setAttribute("opacity", "0.5");
      // meta (estrella) y jugador (personaje del tema)
      const meta = document.createElementNS(NS, "text");
      meta.textContent = "⭐";
      meta.setAttribute("font-size", C * 0.62);
      meta.setAttribute("text-anchor", "middle");
      meta.setAttribute("x", X(n - 1) + C / 2);
      meta.setAttribute("y", Y(n - 1) + C * 0.72);
      const pj = document.createElementNS(NS, "image");
      pj.setAttribute("href", P[nivel % P.length]);
      const PJS = C * 0.74;
      pj.setAttribute("width", PJS); pj.setAttribute("height", PJS);
      let cur = { x: 0, y: 0 };
      const ubicar = () => {
        pj.setAttribute("x", X(cur.x) + (C - PJS) / 2);
        pj.setAttribute("y", Y(cur.y) + (C - PJS) / 2);
      };
      const pasos = [[0, 0]];
      const pintarRastro = () =>
        rastro.setAttribute("points", pasos.map(([x, y]) => `${X(x) + C / 2},${Y(y) + C / 2}`).join(" "));
      ubicar(); pintarRastro();
      svg.append(rastro, muros, meta, pj);
      const tab = el("div", "tablero");
      tab.appendChild(svg);
      ctx.juego.appendChild(tab);

      const abierta = (x, y, dir) => !(lab.celdas[y][x] & { N: 1, S: 2, E: 4, W: 8 }[dir]);
      const paso = (dx, dy) => {
        const nx = cur.x + dx, ny = cur.y + dy;
        if (nx < 0 || ny < 0 || nx >= n || ny >= n) return false;
        const dir = dx === 1 ? "E" : dx === -1 ? "W" : dy === 1 ? "S" : "N";
        if (!abierta(cur.x, cur.y, dir)) return false;
        cur = { x: nx, y: ny };
        pasos.push([nx, ny]);
        if (pasos.length > 2 && pasos[pasos.length - 3][0] === nx && pasos[pasos.length - 3][1] === ny)
          pasos.splice(pasos.length - 3, 2);   // volver atrás borra el rastro
        ubicar(); pintarRastro();
        return true;
      };
      let arrastrando = false;
      const celdaDePuntero = (ev) => {
        const r = svg.getBoundingClientRect();
        // el SVG no tiene preserveAspectRatio explícito -> usa el default
        // "xMidYMid meet": el contenido CUADRADO (viewBox S×S) se escala
        // UNIFORME por el lado más chico del recuadro CSS y se centra,
        // dejando margen vacío en el otro eje. .svgJuego tiene max-height
        // (capa el alto en pantallas anchas y bajas) con width:100% -> en
        // esos casos el recuadro NO es cuadrado. Escalar X e Y por separado
        // contra el recuadro COMPLETO (ancho/alto tal cual, sin restar ese
        // margen) fue el fix anterior para el eje vertical, pero rompe el
        // eje horizontal apenas el ancho excede al alto: el margen quedaba
        // sumado adentro del cálculo, mapeando el puntero varias celdas más
        // a la derecha de donde tocabas — "tengo que poner el puntero del
        // lado izquierdo para que se mueva, si voy para la derecha no se
        // mueve" (con el seguimiento estrictamente local, ni un pixel de
        // error tolera). Fix: reproducir "meet" tal cual — una sola escala
        // (el mínimo de ancho/alto) y restar el margen de centrado de cada
        // eje antes de convertir a celda.
        const escala = Math.min(r.width, r.height) / S;
        const margenX = (r.width - S * escala) / 2;
        const margenY = (r.height - S * escala) / 2;
        return {
          x: Math.floor(((ev.clientX - r.left - margenX) / escala - M) / C),
          y: Math.floor(((ev.clientY - r.top - margenY) / escala - M) / C),
        };
      };
      // 16-jul-2026 (Pablo, quinta vuelta de la misma historia): todos los
      // intentos anteriores (línea recta, BFS libre, BFS con tolerancia,
      // BFS con ritmo de caminata) tenían la MISMA raíz: calculaban un
      // camino HACIA donde estaba el puntero y lo recorrían, aunque fuera
      // larguísimo o cruzara al otro lado de una pared por otro pasillo.
      // Pablo lo aclaró del todo: "el mouse tiene que quedar siempre arriba
      // del dibujo [el personaje pegado al cursor], pero si pasa al otro
      // lado de la pared no tiene que seguir recorriendo hasta ahí, tiene
      // que quedar donde estaba" — no es "encontrale un camino a donde
      // apunto", es seguimiento LOCAL: el personaje solo avanza si la
      // posición del puntero es la celda vecina directa (una sola, abierta)
      // de donde está PARADO ahora mismo. Si el puntero cae en cualquier
      // otra celda (lejos, o vecina pero con pared en el medio), no pasa
      // nada — el personaje se queda exactamente donde estaba, sin buscarle
      // la vuelta por ningún otro pasillo. getCoalescedEvents() sigue
      // siendo necesario: como el trazo real del mouse/dedo recorre el
      // pasillo dibujado punto a punto, cada muestra intermedia SÍ cae en
      // una celda vecina de la anterior — así el personaje queda pegado al
      // cursor durante todo el arrastre, sin pathfinding de por medio.
      let llegando = false;   // guard: dos eventos de puntero casi simultáneos
      // llegando a la meta no deben disparar llegada() dos veces (corrompía
      // "nivel" y rompía el nivel siguiente — bug real visto en pruebas)
      const seguir = (ev) => {
        if (llegando) return;
        const eventos = (ev.getCoalescedEvents && ev.getCoalescedEvents().length)
          ? ev.getCoalescedEvents() : [ev];
        for (const e of eventos) {
          const objetivo = celdaDePuntero(e);
          if (objetivo.x < 0 || objetivo.y < 0 || objetivo.x >= n || objetivo.y >= n) continue;
          const dx = objetivo.x - cur.x, dy = objetivo.y - cur.y;
          if (Math.abs(dx) + Math.abs(dy) === 1) paso(dx, dy);   // vecino directo: paso() ya rechaza si hay pared
          // cualquier otro caso (misma celda, o lejos) no mueve nada — se queda donde estaba
          if (cur.x === n - 1 && cur.y === n - 1) { llegando = true; llegada(); return; }
        }
      };
      const llegada = async () => {
        svg.style.pointerEvents = "none";
        Sfx.bien();
        Confeti.tirar(60);
        nivel++;
        ctx.ronda(nivel);
        if (nivel >= labs.length) { await espera(700); ctx.win(3); }
        else { toast("¡Lo lograste! Ahora uno más grande…"); await espera(1100); arrancar(); }
      };
      svg.addEventListener("pointerdown", (ev) => {
        // cualquier toque en el tablero arranca el seguimiento — no hace
        // falta apoyar el dedo justo sobre el personaje. seguir() de por sí
        // solo mueve si el puntero cae justo en una celda vecina abierta,
        // así que tocar lejos no hace nada (no busca un camino hasta ahí).
        arrastrando = true; svg.setPointerCapture(ev.pointerId); seguir(ev);
      });
      svg.addEventListener("pointermove", (ev) => { if (arrastrando) seguir(ev); });
      svg.addEventListener("pointerup", () => { arrastrando = false; });
      svg.addEventListener("pointercancel", () => { arrastrando = false; });
    };
    arrancar();
  },
};

/* ── SUDOKU 4×4 — con personajes en vez de números (solución única) ── */
GAMES.sudoku = {
  minP: 4,
  crear(ctx) {
    const s = D.sudokus[rint(0, D.sudokus.length - 1)];
    if (!s) return;
    const caras = sample(P, 4);
    ctx.consigna("Cada amigo aparece UNA vez por fila, columna y cuadrado");
    const faltan = s.puz.flat().filter((v) => v === null).length;
    ctx.rondas(faltan);
    // leyenda
    const leg = el("div"); leg.id = "sudokuLegend";
    caras.forEach((c, i) => leg.appendChild(el("div", "leg", `<img src="${c}" alt="">`)));
    ctx.juego.appendChild(leg);
    const tab = el("div", "tablero");
    const grid = el("div"); grid.id = "sudoku";
    tab.appendChild(grid);
    ctx.juego.appendChild(tab);
    const pick = el("div"); pick.id = "sudokuPick";
    ctx.juego.appendChild(pick);

    const tablero = s.puz.map((f) => f.slice());
    const celdas = [];
    let sel = null, puestas = 0;
    const choca = (r, c, v) => {
      for (let i = 0; i < 4; i++) {
        if (i !== c && tablero[r][i] === v) return true;
        if (i !== r && tablero[i][c] === v) return true;
      }
      const r0 = r < 2 ? 0 : 2, c0 = c < 2 ? 0 : 2;
      for (let i = r0; i < r0 + 2; i++)
        for (let j = c0; j < c0 + 2; j++)
          if ((i !== r || j !== c) && tablero[i][j] === v) return true;
      return false;
    };
    const pintarPick = () => {
      pick.innerHTML = "";
      if (sel === null) return;
      caras.forEach((c, v) => {
        const b = el("button", "op", `<img src="${c}" alt="">`);
        b.addEventListener("click", () => poner(v));
        pick.appendChild(b);
      });
    };
    const poner = async (v) => {
      if (sel === null) return;
      const { r, c, celda } = sel;
      if (choca(r, c, v)) {
        ctx.casi();
        celda.innerHTML = `<img src="${caras[v]}" alt="">`;
        celda.classList.add("choca");
        await espera(650);
        celda.classList.remove("choca");
        celda.innerHTML = "";
        return;
      }
      tablero[r][c] = v;
      celda.innerHTML = `<img src="${caras[v]}" alt="">`;
      celda.classList.remove("eligiendo");
      celda.classList.add("anim-pop");
      Sfx.pop();
      sel = null; pintarPick();
      puestas++;
      ctx.ronda(puestas);
      if (tablero.flat().every((x, i) => x === s.sol.flat()[i])) {
        await espera(500); ctx.win();
      }
    };
    for (let r = 0; r < 4; r++)
      for (let c = 0; c < 4; c++) {
        const v = s.puz[r][c];
        const celda = el("button", "celda" + (v !== null ? " fija" : ""));
        if (v !== null) celda.innerHTML = `<img src="${caras[v]}" alt="">`;
        else celda.addEventListener("click", () => {
          if (tablero[r][c] !== null) {           // tocar una puesta la levanta
            tablero[r][c] = null; celda.innerHTML = "";
            puestas--; ctx.ronda(puestas);
          }
          celdas.forEach((x) => x.classList.remove("eligiendo"));
          celda.classList.add("eligiendo");
          Sfx.flip();
          sel = { r, c, celda };
          pintarPick();
        });
        grid.appendChild(celda); celdas.push(celda);
      }
  },
};

/* ── ¡A PINTAR! — balde de pintura sobre el line-art IA del tema ── */
GAMES.colorear = {
  crear(ctx) {
    if (!D.colorear || !D.colorear.length) { ctx.consigna("Este tema no tiene dibujos todavía"); return; }
    let idx = 0;
    ctx.consigna("Tocá el dibujo para pintarlo");
    ctx.rondas(0);
    const wrap = el("div"); wrap.id = "colWrap";
    const cv = el("canvas"); cv.id = "colLienzo";
    const cx = cv.getContext("2d", { willReadFrequently: true });
    // paleta de pintor: colores del tema + clásicos de infantil
    const COLORES = [D.paleta.ac, D.paleta.ac2, D.paleta.star, "#E25555", "#F2984A",
      "#F7D154", "#6FBF5A", "#4FB3BF", "#5B8DEF", "#9B6BD6", "#F78FB3", "#8D6E63",
      "#FFFFFF"];
    let color = COLORES[0];
    const paleta = el("div"); paleta.id = "colPaleta";
    COLORES.forEach((c, i) => {
      const g = el("button", "gota" + (i === 0 ? " activa" : ""));
      g.style.background = c;
      if (c === "#FFFFFF") g.title = "borrador";
      g.addEventListener("click", () => {
        color = c;
        paleta.querySelectorAll(".gota").forEach((x) => x.classList.remove("activa"));
        g.classList.add("activa");
        Sfx.pop();
      });
      paleta.appendChild(g);
    });
    const botones = el("div"); botones.id = "colBotones";
    const bUndo = el("button", "btn suave", "↩️ Deshacer");
    const bOtro = el("button", "btn suave", "🖼️ Otro dibujo");
    const bBajar = el("button", "btn suave", "⬇️ Guardar");
    const bListo = el("button", "btn verde", "✅ ¡Listo!");
    botones.append(bUndo, bOtro, bBajar, bListo);
    wrap.append(cv, paleta, botones);
    ctx.juego.appendChild(wrap);

    let historia = [];
    const cargar = () => {
      const im = new Image();
      im.onload = () => {
        const maxW = Math.min(880, ctx.juego.clientWidth - 8);
        const esc = Math.min(1, maxW / im.width);
        cv.width = Math.round(im.width * esc);
        cv.height = Math.round(im.height * esc);
        cx.fillStyle = "#fff";
        cx.fillRect(0, 0, cv.width, cv.height);
        cx.drawImage(im, 0, 0, cv.width, cv.height);
        historia = [];
        // que canvas + paleta + botones entren juntos en la pantalla (el CSS
        // escala el canvas; acá el tope exacto midiendo la botonera real).
        // 14-jul-2026 (Pablo: "verificá que todas entren en el alto de
        // pantalla"): el buffer fijo "-42" no conocía el padding-bottom real
        // de #stage en mobile (calc(64px + safe-area-inset-bottom), regla
        // @media max-width:560px) — se leía el padding de #stage al vuelo
        // en vez de adivinar un número fijo, así no se desincroniza si ese
        // CSS cambia de nuevo.
        requestAnimationFrame(() => {
          const stage = document.getElementById("stage");
          const pb = stage ? parseFloat(getComputedStyle(stage).paddingBottom) || 0 : 0;
          const libre = innerHeight - wrap.getBoundingClientRect().top
            - paleta.offsetHeight - botones.offsetHeight - pb - 24;
          cv.style.maxHeight = Math.max(180, libre) + "px";
        });
      };
      im.src = D.colorear[idx];
    };
    cargar();

    const hexRgb = (h) => {
      h = h.replace("#", "");
      return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
    };
    // balde: pinta la región contigua clara (los trazos oscuros son frontera)
    const balde = (x0, y0) => {
      const W = cv.width, H = cv.height;
      const img = cx.getImageData(0, 0, W, H);
      const px = img.data;
      const at = (x, y) => (y * W + x) * 4;
      const esLinea = (i) => px[i] < 90 && px[i + 1] < 90 && px[i + 2] < 90;
      const i0 = at(x0, y0);
      if (esLinea(i0)) return false;
      const [R, G, B] = hexRgb(color);
      const r0 = px[i0], g0 = px[i0 + 1], b0 = px[i0 + 2];
      if (Math.abs(r0 - R) + Math.abs(g0 - G) + Math.abs(b0 - B) < 12) return false;
      const parecido = (i) =>
        Math.abs(px[i] - r0) + Math.abs(px[i + 1] - g0) + Math.abs(px[i + 2] - b0) < 110;
      if (historia.length >= 14) historia.shift();
      historia.push(cx.getImageData(0, 0, W, H));
      const pila = [[x0, y0]];
      const visto = new Uint8Array(W * H);
      visto[y0 * W + x0] = 1;
      while (pila.length) {
        const [x, y] = pila.pop();
        const i = at(x, y);
        px[i] = R; px[i + 1] = G; px[i + 2] = B; px[i + 3] = 255;
        const vecinos = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]];
        for (const [nx, ny] of vecinos) {
          if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;
          const k = ny * W + nx;
          if (visto[k]) continue;
          const ni = k * 4;
          if (esLinea(ni) || !parecido(ni)) continue;
          visto[k] = 1;
          pila.push([nx, ny]);
        }
      }
      cx.putImageData(img, 0, 0);
      return true;
    };
    cv.addEventListener("pointerdown", (ev) => {
      const r = cv.getBoundingClientRect();
      const x = Math.round((ev.clientX - r.left) * (cv.width / r.width));
      const y = Math.round((ev.clientY - r.top) * (cv.height / r.height));
      if (x < 0 || y < 0 || x >= cv.width || y >= cv.height) return;
      if (balde(x, y)) Sfx.tick(rint(0, 5));
    });
    bUndo.addEventListener("click", () => {
      const im = historia.pop();
      if (im) { cx.putImageData(im, 0, 0); Sfx.flip(); }
    });
    bOtro.addEventListener("click", () => {
      idx = (idx + 1) % D.colorear.length;
      cargar(); Sfx.pop();
    });
    bBajar.addEventListener("click", () => {
      const a = document.createElement("a");
      a.download = (Store.data.activeProfile ? Store.data.activeProfile.toLowerCase() + "-" : "") + "dibujo.png";
      a.href = cv.toDataURL("image/png");
      a.click();
      toast("¡Guardado! 🖼️");
    });
    bListo.addEventListener("click", () => ctx.win(3));
  },
};

/* ── ¿CUÁNTOS HAY? — contá tocando: cada toque numera y suena (do-re-mi) ── */
// Pablo 15-jul-2026: "cuantos hay, donde hay mas hay varios que deberian
// mejorar esto" — mismo mecanismo de variedad que el resto, con frases
// propias (contar cantidades no encaja en el patrón este/esta/esto).
const CONTAR_CORTAS = ["¿Y ahora cuántos hay?", "¿Cuántos hay acá?", "¿Y estos, cuántos son?", "¿Contamos de nuevo?"];
GAMES.contar = {
  crear(ctx) {
    const max = ctx.cfg.max || 5, rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    // Ronda 1: la fórmula lineal sola daba SIEMPRE la misma secuencia exacta
    // (1,2,3,4,5) — le agregué jitter, pero quedó ordenada de menor a mayor
    // (.sort()), así que el patrón "cada ronda es más que la anterior" seguía
    // siendo 100% predecible (Pablo, 12-jul). Ahora: mismo conjunto de
    // cantidades variadas, pero el ORDEN en que aparecen también es al azar —
    // ninguna relación entre el número de ronda y cuánto hay que contar.
    let cantidades = [];
    for (let i = 0; i < rondas; i++) {
      const lineal = Math.round(1 + (max - 1) * i / (rondas - 1 || 1));
      cantidades.push(Math.min(max, Math.max(1, lineal + rint(-1, 1))));
    }
    cantidades = shuffle(cantidades);   // shuffle() devuelve una COPIA, no muta in-place
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.juego.innerHTML = "";
      const nBichos = cantidades[ronda];
      const objetivo = P[rint(0, Math.min(5, P.length - 1))];
      if (ronda === 0) ctx.consigna(`¿Cuántos hay? ¡Tocalos para contarlos!`, objetivo);
      else ctx.consigna(sacarDeBolsa(ctx, "contar", CONTAR_CORTAS), objetivo);
      const esc = el("div", "escena");
      if (D.escena) {
        const f = el("img", "fondo"); f.src = D.escena; f.alt = "";
        esc.appendChild(f);
      } else esc.style.minHeight = "340px";
      // distractores: otro personaje que NO hay que contar (bandas no-mini)
      const conDistractores = D.banda !== "mini" && nBichos >= 3;
      const distractor = conDistractores ? P.find((p) => p !== objetivo) : null;
      const puestos = [];
      const cabe = (x, y) => puestos.every(([px2, py2]) => Math.hypot(px2 - x, py2 - y) > 17);
      const poner = (src, esObjetivo) => {
        let x, y, tries = 0;
        do { x = rint(4, 82); y = rint(6, 74); tries++; } while (!cabe(x, y) && tries < 80);
        puestos.push([x, y]);
        const b = el("button", "bicho");
        b.style.cssText = `left:${x}%;top:${y}%;width:14%;aspect-ratio:1`;
        b.innerHTML = `<img src="${src}" alt="">`;
        if (esObjetivo) b.dataset.obj = "1";
        esc.appendChild(b);
        return b;
      };
      for (let i = 0; i < nBichos; i++) poner(objetivo, true);
      if (distractor) for (let i = 0; i < Math.min(3, nBichos - 1); i++) poner(distractor, false);
      ctx.juego.appendChild(esc);

      let contados = 0, resuelto = false;
      esc.addEventListener("click", (ev) => {
        const b = ev.target.closest(".bicho");
        if (!b || resuelto) return;
        if (!b.dataset.obj) {           // distractor: se corre a un costado, no cuenta
          b.classList.add("anim-brinco");
          Sfx.casi();
          return;
        }
        if (b.classList.contains("contado")) return;
        b.classList.add("contado", "anim-brinco");
        contados++;
        Sfx.tick(contados);
        b.appendChild(el("div", "num", contados));
      });

      const ops = el("div", "ops");
      const distr = new Set([nBichos]);
      while (distr.size < 3) {
        const v = nBichos + rint(-2, 2);
        if (v >= 1 && v <= max + 2) distr.add(v);
      }
      shuffle([...distr]).forEach((v) => {
        const b = el("button", "op", v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === nBichos) {
            resuelto = true;
            b.classList.add("bien");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.classList.add("casi");
            setTimeout(() => b.classList.remove("casi"), 450);
            ctx.casi();
            if (contados < nBichos) toast("¡Contalos tocándolos! 👆");
          }
        });
        ops.appendChild(b);
      });
      ctx.juego.appendChild(ops);
    };
    jugar();
  },
};

/* ── SUMAS y RESTAS — con grupos de personajes para contar tocando ── */
function juegoCuentas(resta) {
  return {
    crear(ctx) {
      const max = ctx.cfg.max || 10, rondas = ctx.cfg.rondas || 5;
      ctx.rondas(rondas);
      let ronda = 0;
      const jugar = () => {
        ctx.ronda(ronda);
        ctx.juego.innerHTML = "";
        const dif = (ronda + 1) / rondas;      // sube la dificultad
        let a, b, res;
        if (resta) {
          a = rint(2, Math.max(3, Math.round(max * dif)));
          b = rint(1, a - 1);
          res = a - b;
          ctx.consigna(`Había ${a} y se fueron ${b}… ¿cuántos quedan?`);
        } else {
          const tope = Math.max(3, Math.round(max * dif));
          a = rint(1, tope - 1);
          b = rint(1, Math.max(1, tope - a));
          res = a + b;
          ctx.consigna("¿Cuántos hay entre todos? Podés contarlos tocando");
        }
        const s1 = P[ronda % P.length], s2 = P[(ronda + 1) % P.length];
        const fila = el("div", "cuentaGrande");
        const grupo = (nSprites, src, idos) => {
          const g = el("div", "grupoSprites");
          for (let i = 0; i < nSprites; i++) {
            const im = el("img");
            im.src = src;
            if (idos && i >= nSprites - idos) im.classList.add("ida");
            im.addEventListener("click", () => { im.classList.add("anim-brinco"); Sfx.tick(i + 1);
              setTimeout(() => im.classList.remove("anim-brinco"), 600); });
            g.appendChild(im);
          }
          return g;
        };
        if (resta) {
          fila.append(grupo(a, s1, b), el("span", "", "→"), el("span", "", "?"));
        } else {
          fila.append(grupo(a, s1), el("span", "", "+"), grupo(b, s2), el("span", "", "="), el("span", "", "?"));
        }
        ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
        const ops = el("div", "ops");
        const distr = new Set([res]);
        while (distr.size < 3) {
          const v = res + rint(-2, 2);
          if (v >= 0) distr.add(v);
        }
        let resuelto = false;
        shuffle([...distr]).forEach((v) => {
          const btn = el("button", "op", v);
          btn.addEventListener("click", async () => {
            if (resuelto) return;
            if (v === res) {
              resuelto = true;
              btn.classList.add("bien");
              ctx.bien();
              ronda++;
              await espera(900);
              if (ronda >= rondas) ctx.win();
              else jugar();
            } else {
              btn.classList.add("casi");
              setTimeout(() => btn.classList.remove("casi"), 450);
              ctx.casi();
            }
          });
          ops.appendChild(btn);
        });
        ctx.juego.appendChild(ops);
      };
      jugar();
    },
  };
}
GAMES.sumas = juegoCuentas(false);
GAMES.restas = juegoCuentas(true);

/* ── UNÍ LOS PUNTOS — tocá en orden; la figura se revela y se pinta ── */
GAMES.puntos = {
  crear(ctx) {
    const figuras = ctx.cfg.figuras || ["estrella"];
    ctx.rondas(figuras.length);
    let nivel = 0;
    const jugar = () => {
      ctx.ronda(nivel);
      consignaVariada(ctx, nivel, "Uní los puntos en orden: 1, 2, 3…", "f");
      ctx.juego.innerHTML = "";
      const pts = D.figuras[figuras[nivel]];
      const S = 640;
      const NS = "http://www.w3.org/2000/svg";
      const svg = document.createElementNS(NS, "svg");
      svg.setAttribute("viewBox", `0 0 ${S} ${S}`);
      svg.setAttribute("class", "svgJuego");
      svg.style.maxWidth = "560px";
      svg.style.margin = "0 auto";
      svg.style.display = "block";
      const XY = pts.map(([x, y]) => [40 + x * (S - 80), 30 + y * (S - 80)]);
      const forma = document.createElementNS(NS, "path");
      forma.setAttribute("fill", D.paleta.star);
      forma.setAttribute("opacity", "0");
      const trazo = document.createElementNS(NS, "polyline");
      trazo.setAttribute("stroke", D.paleta.ac);
      trazo.setAttribute("stroke-width", 7);
      trazo.setAttribute("fill", "none");
      trazo.setAttribute("stroke-linecap", "round");
      trazo.setAttribute("stroke-linejoin", "round");
      svg.append(forma, trazo);
      let sig = 0;
      const nodos = XY.map(([x, y], i) => {
        const g = document.createElementNS(NS, "g");
        g.style.cursor = "pointer";
        g.setAttribute("transform", `translate(${x} ${y})`);
        const hit = document.createElementNS(NS, "circle");   // target grande invisible
        hit.setAttribute("r", 34); hit.setAttribute("fill", "transparent");
        const c = document.createElementNS(NS, "circle");
        c.setAttribute("r", 15);
        c.setAttribute("fill", D.paleta.card);
        c.setAttribute("stroke", D.paleta.ink);
        c.setAttribute("stroke-width", 3.5);
        const t = document.createElementNS(NS, "text");
        t.textContent = i + 1;
        t.setAttribute("y", -22);
        t.setAttribute("text-anchor", "middle");
        t.setAttribute("font-size", 26);
        t.setAttribute("font-family", "Baloo, sans-serif");
        t.setAttribute("fill", D.paleta.ink);
        g.append(hit, c, t);
        g.addEventListener("pointerdown", () => {
          if (i !== sig) {
            if (i > sig) { Sfx.casi(); const a = nodos[sig].querySelector("circle:nth-child(2)");
              a.setAttribute("fill", D.paleta.ac2); setTimeout(() => a.setAttribute("fill", D.paleta.card), 500); }
            return;
          }
          Sfx.tick(i + 1);
          c.setAttribute("fill", D.paleta.ac);
          sig++;
          trazo.setAttribute("points", XY.slice(0, sig).map((p) => p.join(",")).join(" "));
          if (sig === XY.length) fin();
        });
        svg.appendChild(g);
        return g;
      });
      const fin = async () => {
        trazo.setAttribute("points", XY.concat([XY[0]]).map((p) => p.join(",")).join(" "));
        forma.setAttribute("d", "M" + XY.map((p) => p.join(" ")).join(" L") + " Z");
        forma.setAttribute("opacity", "0.55");
        Sfx.bien();
        Confeti.tirar(60);
        nivel++;
        ctx.ronda(nivel);
        if (nivel >= figuras.length) { await espera(900); ctx.win(3); }
        else { toast("¡Una figura más!"); await espera(1100); jugar(); }
      };
      ctx.juego.appendChild(el("div", "tablero")).appendChild(svg);
    };
    jugar();
  },
};

/* ── SOMBRAS — arrastrá cada personaje hasta su silueta (imán al soltar) ── */
GAMES.sombra = {
  crear(ctx) {
    const pares = ctx.cfg.pares || 3, rondas = ctx.cfg.rondas || 2;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "Llevá a cada amigo hasta su sombra", "m");
      ctx.juego.innerHTML = "";
      const idxs = sample(P.map((_, i) => i), pares);
      const tab = el("div", "tablero lienzo");
      const wrap = el("div");
      wrap.style.cssText = "display:flex;justify-content:space-between;gap:16px";
      const izq = el("div"), der = el("div");
      izq.style.cssText = der.style.cssText =
        "display:flex;flex-direction:column;gap:18px;align-items:center;flex:1";
      wrap.append(izq, der);
      tab.appendChild(wrap);
      ctx.juego.appendChild(tab);
      let TAM = Math.min(130, Math.floor((innerWidth - 140) / Math.max(3, pares)) + 40);
      const dispS = innerHeight - tab.getBoundingClientRect().top - 48;
      TAM = Math.max(64, Math.min(TAM, Math.floor((dispS - (pares - 1) * 18 - 16) / pares)));
      const siluetas = shuffle(idxs).map((ix) => {
        const d = el("div", "silueta", `<img src="${(D.sombras || P)[ix]}" alt="">`);
        d.style.cssText = `width:${TAM}px;height:${TAM}px`;
        d.dataset.s = String(ix);
        der.appendChild(d);
        return d;
      });
      let listos = 0;
      idxs.forEach((ix) => {
        const s = P[ix];
        const a = el("div", "arrastrable", `<img src="${s}" alt="">`);
        a.style.cssText = `width:${TAM}px;height:${TAM}px`;
        izq.appendChild(a);
        let sx = 0, sy = 0, ox = 0, oy = 0, activo = false;
        a.addEventListener("pointerdown", (ev) => {
          activo = true;
          a.setPointerCapture(ev.pointerId);
          sx = ev.clientX; sy = ev.clientY;
          const m = /translate\((-?[\d.]+)px, (-?[\d.]+)px\)/.exec(a.style.transform || "");
          ox = m ? +m[1] : 0; oy = m ? +m[2] : 0;
          a.style.transition = "none"; a.style.zIndex = 20;
          Sfx.pop();
        });
        a.addEventListener("pointermove", (ev) => {
          if (!activo) return;
          a.style.transform = `translate(${ox + ev.clientX - sx}px, ${oy + ev.clientY - sy}px)`;
        });
        const soltar = (ev) => {
          if (!activo) return;
          activo = false;
          a.style.zIndex = 5;
          const ra = a.getBoundingClientRect();
          const cx0 = ra.left + ra.width / 2, cy0 = ra.top + ra.height / 2;
          let mejor = null, dist = 1e9;
          siluetas.forEach((sil) => {
            if (sil.classList.contains("llena")) return;
            const rs = sil.getBoundingClientRect();
            const d = Math.hypot(rs.left + rs.width / 2 - cx0, rs.top + rs.height / 2 - cy0);
            if (d < dist) { dist = d; mejor = sil; }
          });
          if (mejor && dist < TAM * 0.75 && mejor.dataset.s === String(ix)) {
            mejor.classList.add("llena");
            a.remove();
            ctx.bien();
            listos++;
            if (listos === pares) {
              ronda++;
              setTimeout(() => {
                if (ronda >= rondas) ctx.win();
                else jugar();
              }, 900);
            }
          } else {
            if (mejor && dist < TAM * 0.75) ctx.casi();
            a.style.transition = "transform .35s ease";
            a.style.transform = "translate(0px, 0px)";
          }
        };
        a.addEventListener("pointerup", soltar);
        a.addEventListener("pointercancel", soltar);
      });
    };
    jugar();
  },
};

/* ── SEGUÍ EL PATRÓN — ¿qué sigue? (predice matemática: el "sleeper") ── */
GAMES.patron = {
  crear(ctx) {
    const nivel = ctx.cfg.nivel || 1, rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let MOLDES = { 1: ["AB"], 2: ["AB", "ABC", "AABB"], 3: ["ABC", "ABB", "AABB", "ABCD"] }[nivel] || ["AB"];
    MOLDES = MOLDES.filter((m) => new Set(m.split("")).size <= P.length);
    if (!MOLDES.length) MOLDES = ["AB"];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Qué sigue? Seguí el patrón", "m");
      ctx.juego.innerHTML = "";
      const molde = MOLDES[rint(0, MOLDES.length - 1)];
      const kinds = sample(P, new Set(molde.split("")).size);
      const mapa = {}; [...new Set(molde.split(""))].forEach((ch, i) => (mapa[ch] = kinds[i]));
      const seq = [];
      while (seq.length < Math.max(6, molde.length * 2 + 1))
        seq.push(...molde.split("").map((ch) => mapa[ch]));
      const vista = seq.slice(0, Math.max(6, molde.length * 2 + 1));
      const rta = vista[vista.length - 1];
      const TAM = Math.min(86, Math.floor((Math.min(innerWidth, 1020) - 130) / vista.length) - 10);
      const fila = el("div", "filaSprites");
      const spriteEls = [];
      vista.forEach((s, i) => {
        if (i === vista.length - 1) {
          const h = el("div", "hueco", "?");
          h.style.cssText = `width:${TAM + 20}px;height:${TAM + 20}px`;
          fila.appendChild(h);
          spriteEls.push(h);
        } else {
          const d = el("div", "spriteQuieto", `<img src="${s}" alt="">`);
          d.querySelector("img").style.cssText = `width:${TAM}px;height:${TAM}px`;
          fila.appendChild(d);
          spriteEls.push(d);
        }
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
      const ops = el("div", "ops");
      const opciones = new Set([rta]);
      for (const p of shuffle(P)) { if (opciones.size >= 3) break; opciones.add(p); }
      let resuelto = false;
      shuffle([...opciones]).forEach((s) => {
        const b = el("button", "op", `<img src="${s}" alt="">`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (s === rta) {
            resuelto = true;
            const h = spriteEls[spriteEls.length - 1];
            h.className = "spriteQuieto anim-pop";
            h.innerHTML = `<img src="${s}" alt="" style="width:${TAM}px;height:${TAM}px">`;
            // ola de brincos: el patrón "canta" completo
            spriteEls.forEach((d, i) => setTimeout(() => {
              d.classList.add("anim-brinco"); Sfx.tick(i + 1);
            }, i * 110));
            ctx.bien();
            ronda++;
            await espera(1000 + spriteEls.length * 110);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.classList.add("casi");
            setTimeout(() => b.classList.remove("casi"), 450);
            ctx.casi();
            // andamiaje: el patrón se repasa solo, resaltando en orden
            spriteEls.slice(0, -1).forEach((d, i) => setTimeout(() => d.classList.add("anim-brinco"), i * 140));
            setTimeout(() => spriteEls.forEach((d) => d.classList.remove("anim-brinco")),
              spriteEls.length * 140 + 700);
          }
        });
        ops.appendChild(b);
      });
      ctx.juego.appendChild(ops);
    };
    jugar();
  },
};

/* ── EL DISTINTO — atención visual: tocá el que no es igual ── */
GAMES.diferente = {
  crear(ctx) {
    const opciones = ctx.cfg.opciones || 4, rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "Tocá el que es DISTINTO", "m");
      ctx.juego.innerHTML = "";
      const [base, raro] = sample(P, 2);
      const pos = rint(0, opciones - 1);
      const fila = el("div", "filaSprites");
      const TAM = Math.min(150, Math.floor((innerWidth - 90) / opciones) - 10);
      let resuelto = false;
      for (let i = 0; i < opciones; i++) {
        const s = i === pos ? raro : base;
        const b = el("button", "spriteBtn", `<img src="${s}" alt="">`);
        b.querySelector("img").style.cssText = `width:${TAM}px;height:${TAM}px`;
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (i === pos) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.classList.add("casi"); // wiggle suave
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      }
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── EL MÁS GRANDE — noción de tamaño (alterna grande/chico) ── */
const TAMANO_GRANDE_CORTAS = ["¿Y ahora, el MÁS GRANDE?", "Tocá el MÁS GRANDE otra vez", "¿Cuál es más GRANDE?"];
const TAMANO_CHICO_CORTAS = ["¿Y ahora, el MÁS CHICO?", "Tocá el MÁS CHICO otra vez", "¿Cuál es más CHICO?"];
GAMES.tamano = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      // mini: siempre "grande" (más simple); el resto: al azar de verdad —
      // alternar por paridad de ronda hacía que, jugado dos veces, ya se
      // supiera sin mirar que la ronda 2 siempre pedía "el más chico".
      const grande = D.banda === "mini" || rint(0, 1) === 0;
      if (ronda === 0) {
        ctx.consigna(grande ? "Tocá el MÁS GRANDE" : "Ahora tocá el MÁS CHICO");
      } else {
        ctx.consigna(sacarDeBolsa(ctx, grande ? "grande" : "chico", grande ? TAMANO_GRANDE_CORTAS : TAMANO_CHICO_CORTAS));
      }
      ctx.juego.innerHTML = "";
      const s = P[rint(0, P.length - 1)];
      const escalas = shuffle([0.42, 0.62, 0.82, 1.05]);
      const objetivo = grande ? Math.max(...escalas) : Math.min(...escalas);
      const fila = el("div", "filaSprites");
      fila.style.alignItems = "flex-end";
      fila.style.minHeight = "200px";
      const BASE = Math.min(160, innerWidth / 4);
      let resuelto = false;
      escalas.forEach((k) => {
        const b = el("button", "spriteBtn", `<img src="${s}" alt="">`);
        const px2 = Math.round(BASE * k);
        b.querySelector("img").style.cssText = `width:${px2}px;height:${px2}px`;
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (k === objetivo) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿DÓNDE HAY MÁS? — comparación de cantidades (alterna más/menos) ── */
// Pablo 15-jul-2026: mismo mecanismo de variedad, con frases propias por
// dirección — acá lo que varía no es un objeto (este/esta/esto), es la
// DIRECCIÓN de la pregunta (MÁS o MENOS), así que cada bolsa es independiente
// (sacarDeBolsa con `key` distinta) para no mezclar variantes de una con la
// otra a mitad de partida.
const MAS_CORTAS = ["Tocá el grupo que tiene MÁS", "¿Cuál tiene MÁS?", "¿Y ahora, dónde hay MÁS?"];
const MENOS_CORTAS = ["Tocá el grupo que tiene MENOS", "¿Cuál tiene MENOS?", "¿Y ahora, dónde hay MENOS?"];
GAMES.mas_menos = {
  crear(ctx) {
    const max = ctx.cfg.max || 6, rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      // mini: siempre "más" (más simple); el resto: al azar de verdad — igual
      // bug que en tamano, alternar por paridad se aprendía de memoria.
      const buscaMas = D.banda === "mini" || rint(0, 1) === 0;
      if (ronda === 0) {
        ctx.consigna(buscaMas ? "¿Dónde hay MÁS? Tocá el grupo" : "¿Dónde hay MENOS? Tocá el grupo");
      } else {
        ctx.consigna(sacarDeBolsa(ctx, buscaMas ? "mas" : "menos", buscaMas ? MAS_CORTAS : MENOS_CORTAS));
      }
      ctx.juego.innerHTML = "";
      let a = rint(1, max), b = rint(1, max);
      while (a === b) b = rint(1, max);
      const [s1, s2] = sample(P, 2);
      const cont = el("div"); cont.id = "dosGrupos";
      let resuelto = false;
      const grupos = [];
      [[a, s1], [b, s2]].forEach(([nCant, src]) => {
        const g = el("button", "grupo");
        for (let i = 0; i < nCant; i++) g.appendChild(el("img")).src = src;
        const num = el("span", "grupo__num", String(nCant));
        g.appendChild(num);
        g.addEventListener("click", async () => {
          if (resuelto) return;
          const gana = buscaMas ? Math.max(a, b) : Math.min(a, b);
          if (nCant === gana) {
            resuelto = true;
            g.style.outline = `6px solid var(--ok)`;
            g.querySelectorAll("img").forEach((im, i) =>
              setTimeout(() => im.classList.add("anim-brinco"), i * 70));
            ctx.bien();
            ronda++;
            await espera(1000);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            g.style.animation = "sacudir .4s ease";
            setTimeout(() => (g.style.animation = ""), 450);
            ctx.casi();
            // feedback elaborado: mostrar la cantidad de CADA grupo un
            // instante para que pueda volver a contar y comparar, en vez
            // de solo saber "esta no era" por descarte.
            grupos.forEach((gr) => gr.querySelector(".grupo__num").classList.add("ver"));
            await espera(1400);
            grupos.forEach((gr) => gr.querySelector(".grupo__num").classList.remove("ver"));
          }
        });
        grupos.push(g);
        cont.appendChild(g);
      });
      ctx.juego.appendChild(cont);
    };
    jugar();
  },
};

/* ── ¿DÓNDE ESTÁ? — noción espacial (14-jul-2026, Sala de 4 Bimestre 1:
   arriba/abajo/adentro/afuera). Una caja de referencia fija + 2 sprites en
   posiciones CONTRASTANTES del MISMO eje (arriba↔abajo o adentro↔afuera,
   nunca mezclados) — el distractor siempre es el opuesto conceptual, igual
   criterio que el resto del motor: nunca al azar puro. ── */
GAMES.posicion = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let ronda = 0;
    const PARES = [
      { pos: "arriba", op: "abajo", txt: "ARRIBA de la caja" },
      { pos: "abajo", op: "arriba", txt: "ABAJO de la caja" },
      { pos: "adentro", op: "afuera", txt: "ADENTRO de la caja" },
      { pos: "afuera", op: "adentro", txt: "AFUERA de la caja" },
    ];
    const jugar = () => {
      ctx.ronda(ronda);
      const par = PARES[rint(0, PARES.length - 1)];
      ctx.consigna(`Tocá lo que está ${par.txt}`);
      ctx.juego.innerHTML = "";
      const s = P[rint(0, P.length - 1)];
      const cont = el("div", "cajaPosicion");
      cont.appendChild(el("div", "cajaPosicion__caja"));
      let resuelto = false;
      // orden al azar para que la posición en pantalla no delate la respuesta
      shuffle([par.pos, par.op]).forEach((p) => {
        const b = el("button", `spriteBtn cajaPosicion__${p}`, `<img src="${s}" alt="">`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (p === par.pos) {
            resuelto = true;
            b.querySelector("img").classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            // en la img, no en el botón: el botón usa transform para su
            // posición absoluta (arriba/abajo/adentro/afuera) y una
            // animación que también setea transform se la pisaría.
            const im = b.querySelector("img");
            im.style.animation = "sacudir .4s ease";
            setTimeout(() => (im.style.animation = ""), 450);
            ctx.casi();
          }
        });
        cont.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(cont);
    };
    jugar();
  },
};

/* ── LA SERIE — completá el número que falta (+1 o +2) ── */
/* ── ¿CUÁNTAS PARTES? — conciencia fonológica (14-jul-2026, Sala de 5
   Bimestre 2 NAP: "sílabas, aplaudirlas"). Primer juego del motor con
   componente de AUDIO real, no decorativo: se ESCUCHA la palabra (nunca se
   muestra escrita — el objetivo es el sonido, no la lectura) y se elige
   cuántas partes tiene. Distractores SIEMPRE ±1 (el error real de contar
   sílabas es equivocarse por una, nunca al azar). El emoji de la palabra
   se revela recién DESPUÉS de acertar — mostrarlo antes dejaría "adivinar"
   por asociación visual en vez de escuchar de verdad. ── */
GAMES.silabas = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    const BANCO = [
      { p: "SOL", e: "☀️", s: 1 }, { p: "PAN", e: "🍞", s: 1 }, { p: "MAR", e: "🌊", s: 1 },
      { p: "GATO", e: "🐱", s: 2 }, { p: "CASA", e: "🏠", s: 2 }, { p: "LUNA", e: "🌙", s: 2 }, { p: "PERRO", e: "🐶", s: 2 },
      { p: "PELOTA", e: "⚽", s: 3 }, { p: "ZAPATO", e: "👟", s: 3 }, { p: "CAMISA", e: "👕", s: 3 },
      { p: "MARIPOSA", e: "🦋", s: 4 }, { p: "ELEFANTE", e: "🐘", s: 4 }, { p: "BICICLETA", e: "🚲", s: 4 },
    ];
    let usadas = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = BANCO.filter((w) => !usadas.includes(w.p));
      if (!disp.length) { usadas = []; disp = BANCO; }
      const palabra = disp[rint(0, disp.length - 1)];
      usadas.push(palabra.p);
      consignaVariada(ctx, ronda, "Escuchá la palabra y elegí cuántas partes tiene", "f");
      ctx.juego.innerHTML = "";
      const tablero = el("div", "tablero silabasTablero");
      const zonaEmoji = el("div", "silabasEmoji", "❓");
      tablero.appendChild(zonaEmoji);
      const btnEscuchar = el("button", "btn suave", "🔊 Escuchar de nuevo");
      btnEscuchar.type = "button";
      btnEscuchar.addEventListener("click", () => reproducirConsigna(palabra.p));
      tablero.appendChild(btnEscuchar);
      const fila = el("div", "filaSprites");
      fila.style.marginTop = "18px";
      let opciones = [palabra.s];
      if (palabra.s > 1) opciones.push(palabra.s - 1);
      opciones.push(palabra.s + 1);
      if (opciones.length < 3) opciones.push(palabra.s + 2);
      opciones = shuffle(opciones);
      let resuelto = false;
      opciones.forEach((n) => {
        const b = el("button", "spriteBtn", `<span style="font-size:34px;font-family:'Baloo',sans-serif">${n}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (n === palabra.s) {
            resuelto = true;
            zonaEmoji.textContent = palabra.e;   // recién ahora se revela
            zonaEmoji.classList.add("anim-pop");
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(1100);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
            reproducirConsigna(palabra.p);   // reescuchar tras errar: feedback elaborado sin texto
          }
        });
        fila.appendChild(b);
      });
      tablero.appendChild(fila);
      ctx.juego.appendChild(tablero);
      // la palabra se escucha automáticamente después de la consigna
      setTimeout(() => reproducirConsigna(palabra.p), 1300);
    };
    jugar();
  },
};

/* ── ARMÁ LA PALABRA — sílabas CV (14-jul-2026, 1° grado NAP Bimestre 2:
   "sílabas directas... construir palabras arrastrando sílabas desordenadas").
   Sin drag de verdad (mismo criterio que agrupar: más robusto en mobile) —
   las sílabas se tocan EN ORDEN y van llenando los huecos de arriba. No hay
   "distractor": todas las sílabas mostradas son parte de la palabra, el
   desafío es la SECUENCIA, no elegir la correcta entre ajenas. ── */
GAMES.armar_palabra = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    const BANCO = [
      { p: "GATO", e: "🐱", s: ["GA", "TO"] },
      { p: "LUNA", e: "🌙", s: ["LU", "NA"] },
      { p: "CASA", e: "🏠", s: ["CA", "SA"] },
      { p: "SAPO", e: "🐸", s: ["SA", "PO"] },
      { p: "MOTO", e: "🏍️", s: ["MO", "TO"] },
      { p: "PATO", e: "🦆", s: ["PA", "TO"] },
      { p: "PELOTA", e: "⚽", s: ["PE", "LO", "TA"] },
    ];
    let usadas = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = BANCO.filter((w) => !usadas.includes(w.p));
      if (!disp.length) { usadas = []; disp = BANCO; }
      const palabra = disp[rint(0, disp.length - 1)];
      usadas.push(palabra.p);
      consignaVariada(ctx, ronda, "Escuchá la palabra y tocá las sílabas en orden para armarla", "f");
      ctx.juego.innerHTML = "";
      const tablero = el("div", "tablero armarPalabraTablero");
      tablero.appendChild(el("div", "armarPalabraEmoji", palabra.e));
      const filaSlots = el("div", "armarPalabraSlots");
      const slots = palabra.s.map(() => el("div", "armarPalabraSlot", ""));
      slots.forEach((s) => filaSlots.appendChild(s));
      tablero.appendChild(filaSlots);
      const btnEscuchar = el("button", "btn suave", "🔊 Escuchar de nuevo");
      btnEscuchar.type = "button";
      btnEscuchar.addEventListener("click", () => reproducirConsigna(palabra.p));
      tablero.appendChild(btnEscuchar);
      const filaSilabas = el("div", "filaSprites armarPalabraSilabas");
      filaSilabas.style.marginTop = "18px";
      let siguiente = 0;
      let resuelto = false;
      shuffle(palabra.s.map((s, i) => ({ s, i }))).forEach(({ s, i }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:28px;font-family:'Baloo',sans-serif">${s}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto || b.disabled) return;
          if (i === siguiente) {
            b.disabled = true;
            b.classList.add("anim-brinco");
            slots[i].textContent = s;
            slots[i].classList.add("anim-pop");
            Sfx.tick(siguiente + 1);
            siguiente++;
            if (siguiente >= palabra.s.length) {
              resuelto = true;
              ctx.bien();
              ronda++;
              await espera(1100);
              if (ronda >= rondas) ctx.win();
              else jugar();
            }
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        filaSilabas.appendChild(b);
      });
      tablero.appendChild(filaSilabas);
      ctx.juego.appendChild(tablero);
      setTimeout(() => reproducirConsigna(palabra.p), 1300);
    };
    jugar();
  },
};

/* ── ABECEDARIO — orden alfabético (14-jul-2026, 1° grado NAP Bimestre 1:
   "el abecedario", "ordenar alfabéticamente"). Mismo patrón tap-en-orden que
   armar_palabra, reusa sus mismas clases CSS (huecos arriba, letras abajo
   mezcladas) — acá no hay audio por letra individual, es orden VISUAL, no
   fonético (a diferencia de silabas/armar_palabra, que sí dependen de oído). ── */
const ABECEDARIO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ".split("");
GAMES.abecedario = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    const nLetras = ctx.cfg.letras || 4;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "Tocá las letras en orden del abecedario", "n");
      ctx.juego.innerHTML = "";
      const idxs = new Set();
      while (idxs.size < nLetras) idxs.add(rint(0, ABECEDARIO.length - 1));
      const correctas = [...idxs].sort((a, b) => a - b).map((i) => ABECEDARIO[i]);
      const tablero = el("div", "tablero armarPalabraTablero");
      const filaSlots = el("div", "armarPalabraSlots");
      const slots = correctas.map(() => el("div", "armarPalabraSlot", ""));
      slots.forEach((s) => filaSlots.appendChild(s));
      tablero.appendChild(filaSlots);
      const filaLetras = el("div", "filaSprites");
      filaLetras.style.marginTop = "18px";
      let siguiente = 0;
      let resuelto = false;
      shuffle(correctas.map((s, i) => ({ s, i }))).forEach(({ s, i }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:30px;font-family:'Baloo',sans-serif">${s}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto || b.disabled) return;
          if (i === siguiente) {
            b.disabled = true;
            b.classList.add("anim-brinco");
            slots[i].textContent = s;
            slots[i].classList.add("anim-pop");
            Sfx.tick(siguiente + 1);
            siguiente++;
            if (siguiente >= correctas.length) {
              resuelto = true;
              ctx.bien();
              ronda++;
              await espera(1100);
              if (ronda >= rondas) ctx.win();
              else jugar();
            }
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        filaLetras.appendChild(b);
      });
      tablero.appendChild(filaLetras);
      ctx.juego.appendChild(tablero);
    };
    jugar();
  },
};

/* ── SUMA RÁPIDA — burbujas que sumen 10 (14-jul-2026, 1° grado NAP
   Bimestre 2 "Ideas web": "tocar burbujas que sumen 10"). Tocar DOS
   burbujas cuya suma dé el objetivo; los distractores se generan evitando
   que formen un segundo par válido por accidente (ambigüedad). ── */
GAMES.suma_rapida = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    const objetivo = 10;   // NAP literal: "burbujas que sumen 10" — fijo (la consigna grabada dice "10")
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "Tocá dos burbujas que sumen 10", "n");
      ctx.juego.innerHTML = "";
      const a = rint(1, objetivo - 1);
      const b = objetivo - a;
      let nums = [a, b];
      let guardas = 0;
      while (nums.length < 5 && guardas < 50) {
        guardas++;
        const v = rint(1, objetivo - 1);
        if (nums.some((n) => n + v === objetivo)) continue;
        nums.push(v);
      }
      nums = shuffle(nums);
      const fila = el("div", "filaSprites");
      let elegido = null;
      let resuelto = false;
      nums.forEach((v, idx) => {
        const btn = el("button", "spriteBtn", `<span style="font-size:30px;font-family:'Baloo',sans-serif">${v}</span>`);
        btn.addEventListener("click", async () => {
          if (resuelto || btn.disabled) return;
          if (elegido === null) {
            elegido = { idx, v, btn };
            btn.classList.add("elegido");
            return;
          }
          if (elegido.idx === idx) return;
          if (elegido.v + v === objetivo) {
            resuelto = true;
            btn.disabled = true;
            elegido.btn.disabled = true;
            btn.classList.add("anim-pop");
            elegido.btn.classList.add("anim-pop");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            // capturar el botón ANTES de resetear `elegido` — el setTimeout
            // corre 450ms después, cuando `elegido` ya es null (bug real
            // encontrado en vivo 14-jul-2026: "Cannot read properties of
            // null (reading 'btn')" al errar el segundo toque)
            const prevBtn = elegido.btn;
            prevBtn.classList.remove("elegido");
            btn.style.animation = "sacudir .4s ease";
            prevBtn.style.animation = "sacudir .4s ease";
            setTimeout(() => { btn.style.animation = ""; prevBtn.style.animation = ""; }, 450);
            ctx.casi();
            elegido = null;
          }
        });
        fila.appendChild(btn);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── CAMPO O CIUDAD — clasificar (14-jul-2026, 1° grado NAP Bimestre 3
   "Ideas web": "clasificar ¿Campo o Ciudad? arrastrando elementos"). Banco
   FIJO por emoji (no sprites del tema — tiene que dar el mismo contenido
   curricular en los 12 temas). Tap-sin-drag, 2 categorías etiquetadas. ── */
const CAMPO_CIUDAD_BANCO = [
  { e: "🐄", cat: "campo" }, { e: "🚜", cat: "campo" }, { e: "🌾", cat: "campo" },
  { e: "🐓", cat: "campo" }, { e: "🐖", cat: "campo" },
  { e: "🏢", cat: "ciudad" }, { e: "🚦", cat: "ciudad" }, { e: "🚌", cat: "ciudad" },
  { e: "🏬", cat: "ciudad" }, { e: "🚕", cat: "ciudad" },
];
GAMES.campo_ciudad = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es del campo o de la ciudad?", "n");
      ctx.juego.innerHTML = "";
      let disp = CAMPO_CIUDAD_BANCO.filter((x) => !usados.includes(x.e));
      if (!disp.length) { usados = []; disp = CAMPO_CIUDAD_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.e);
      const arriba = el("div", "tablero");
      const cont = el("div", "spriteQuieto anim-pop", `<span style="font-size:80px">${item.e}</span>`);
      arriba.appendChild(cont);
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      [{ cat: "campo", label: "🌾 Campo" }, { cat: "ciudad", label: "🏙️ Ciudad" }].forEach(({ cat, label }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:24px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (cat === item.cat) {
            resuelto = true;
            cont.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿QUÉ FRUTO DA? — unir planta con su fruto/semilla (14-jul-2026, 1°
   grado NAP Bimestre 3 "Ideas web"). Banco chico (4 pares) — 3 opciones por
   ronda, 1 correcta + 2 distractoras de OTROS pares del banco. ── */
const PLANTA_FRUTO_BANCO = [
  { planta: "🌳", fruto: "🍎" },   // árbol — manzana
  { planta: "🌴", fruto: "🥥" },   // palmera — coco
  { planta: "🌿", fruto: "🍓" },   // planta baja — frutilla
  { planta: "🌱", fruto: "🥕" },   // brote — zanahoria
  // agregados 14-jul-2026 (banco ampliado de 4 a 6, NO a 10: es un juego
  // 100% de emoji sin texto — Unicode no tiene suficientes emoji de
  // "planta" distinguibles con un fruto real y correcto detrás para
  // llegar a 10 sin repetir símbolo o inventar una pareja botánicamente
  // falsa. 6 es el techo honesto de este juego puntual hasta que tenga
  // ilustración propia en vez de solo emoji).
  { planta: "🌸", fruto: "🍒" },   // cerezo en flor — cereza
  { planta: "🪴", fruto: "🌶️" },   // planta en maceta — ají
];
GAMES.planta_fruto = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Qué fruto da esta planta?", "f");
      ctx.juego.innerHTML = "";
      let disp = PLANTA_FRUTO_BANCO.filter((x) => !usados.includes(x.planta));
      if (!disp.length) { usados = []; disp = PLANTA_FRUTO_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.planta);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto", `<span style="font-size:80px">${item.planta}</span>`));
      ctx.juego.appendChild(arriba);
      let opciones = [item.fruto];
      while (opciones.length < 3) {
        const otro = PLANTA_FRUTO_BANCO[rint(0, PLANTA_FRUTO_BANCO.length - 1)].fruto;
        if (!opciones.includes(otro)) opciones.push(otro);
      }
      opciones = shuffle(opciones);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      opciones.forEach((f) => {
        const b = el("button", "spriteBtn", `<span style="font-size:44px">${f}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (f === item.fruto) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── TABLAS NINJA (M17, 4° grado — docs/auditoria-dc-caba/grado-4.md): fluidez
   de la tabla pitagórica, EL gatekeeper multiplicativo que a 4° le faltaba por
   completo (pedido por los 3 revisores del panel). GENERADA (no banco fijo).
   Distractores por MISCONCEPTION real (Capa 0 · C4), no al azar: tabla vecina
   (a×(b±1), (a±1)×b) y suma en vez de producto (a+b). Cada error incorrecto trae
   SU explicación del porqué (Capa 0 · C3). La dificultad sube dentro de la sesión:
   tablas bajas → altas → mezcla. cfg.nivel fija un piso. ── */
GAMES.tablas_ninja = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    const nivel = ctx.cfg.nivel || 1;
    ctx.rondas(rondas);
    let ronda = 0;
    const rango = () => {
      const prog = rondas > 1 ? ronda / (rondas - 1) : 1;
      if (nivel >= 3 || prog > 0.66) return [rint(2, 9), rint(2, 9)];   // mezcla
      if (nivel === 2 || prog > 0.33) return [rint(6, 9), rint(2, 9)];  // tablas altas
      return [rint(2, 5), rint(2, 9)];                                   // tablas bajas
    };
    const jugar = () => {
      ctx.ronda(ronda);
      const [a, b] = rango();
      const correcto = a * b;
      ctx.item("tablas_ninja#" + a + "x" + b);   // C1: telemetría por ítem real
      ctx.consigna("¿Cuánto es " + a + " por " + b + "?");
      ctx.juego.innerHTML = "";
      // distractores por error típico, cada uno con SU explicación (C3/C4)
      const cand = [];
      if (b < 12) cand.push({ v: a * (b + 1), m: a + "×" + (b + 1) + " es " + (a * (b + 1)) + ". Te pasaste una tabla: " + a + "×" + b + " es una menos." });
      if (b > 1)  cand.push({ v: a * (b - 1), m: a + "×" + (b - 1) + " es " + (a * (b - 1)) + ". Te faltó una tabla: " + a + "×" + b + " es una más." });
      cand.push({ v: a + b, m: a + "+" + b + " es " + (a + b) + ", pero acá multiplicamos: " + a + " veces el " + b + "." });
      if (a < 12) cand.push({ v: (a + 1) * b, m: (a + 1) + "×" + b + " es " + ((a + 1) * b) + ": esa es la tabla del " + (a + 1) + ", no la del " + a + " (" + a + "×" + b + ")." });
      const opciones = [{ v: correcto, ok: true }];
      shuffle(cand).forEach((d) => {
        if (opciones.length >= 3) return;
        if (d.v > 0 && !opciones.some((o) => o.v === d.v)) opciones.push(d);
      });
      // relleno defensivo si algún caso chico no dejó 2 distractores únicos
      let intento = 0;
      while (opciones.length < 3 && intento++ < 20) {
        const v = correcto + rint(1, 4) * (rint(0, 1) ? 1 : -1);
        if (v > 0 && !opciones.some((o) => o.v === v))
          opciones.push({ v: v, m: "Contá de " + a + " en " + a + ": " + a + "×" + b + " es " + correcto + "." });
      }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const btn = el("button", "op", o.v);
        btn.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) {
            resuelto = true;
            btn.classList.add("anim-pop");
            ctx.bien();
            ronda++;
            await espera(950);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            btn.classList.add("casi");
            setTimeout(() => btn.classList.remove("casi"), 450);
            ctx.casi(o.m);   // C3: explica ESTE error puntual
          }
        });
        fila.appendChild(btn);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── FÁBRICA DE MULTIPLICAR (M5, 4° grado — docs/auditoria-dc-caba/grado-4.md):
   multiplicación MÁS ALLÁ de las tablas —el corazón operatorio de 4°—. Fase mental
   (trivia) de la secuencia CPA del dossier. GENERADA. Distractores por misconception
   real (Capa 0 · C4): ceros de menos/de más en ×10/×100/×1000, y multiplicar solo
   una parte del número en 2 cifras × 1 cifra. Explicación por error (Capa 0 · C3).
   La dificultad sube: valor posicional (×10/100/1000) → 2 cifras × 1 cifra. ── */
GAMES.multiplicar = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    const nivel = ctx.cfg.nivel || 1;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const prog = rondas > 1 ? ronda / (rondas - 1) : 1;
      const fase = (nivel >= 2 || prog > 0.5) ? 2 : 1;
      let a, b, correcto;
      const cand = [];
      if (fase === 1) {
        const base = [10, 100, 1000][rint(0, prog > 0.66 ? 2 : (prog > 0.33 ? 1 : 0))];
        a = rint(2, 99); b = base; correcto = a * b;
        cand.push({ v: a * (base / 10), m: "Le faltan ceros. Por " + base + ", escribí el " + a + " y después TODOS los ceros del " + base + "." });
        cand.push({ v: a * (base * 10), m: "Te sobra un cero. Contá los ceros del " + base + " y ponés justo esos." });
        cand.push({ v: a + base, m: a + " más " + base + " es sumar; acá es " + a + " VECES el " + base + "." });
      } else {
        a = rint(12, 99); b = rint(3, 9); correcto = a * b;
        const dec = Math.floor(a / 10) * 10, uni = a % 10;
        cand.push({ v: (dec * b) + uni, m: "Multiplicaste las decenas pero dejaste la unidad suelta. TODO el " + a + " va por " + b + "." });
        cand.push({ v: dec + (uni * b), m: "Multiplicaste solo la unidad. Las decenas del " + a + " también van por " + b + "." });
        cand.push({ v: a * (b - 1), m: "Esa es " + a + " × " + (b - 1) + ". Acá es por " + b + "." });
        cand.push({ v: a + b, m: a + " más " + b + " es sumar; acá multiplicamos." });
      }
      ctx.item("multiplicar#" + a + "x" + b);
      ctx.consigna("¿Cuánto es " + a + " por " + b + "?");
      ctx.juego.innerHTML = "";
      const opciones = [{ v: correcto, ok: true }];
      shuffle(cand).forEach((d) => {
        if (opciones.length >= 3) return;
        if (d.v > 0 && d.v !== correcto && !opciones.some((o) => o.v === d.v)) opciones.push(d);
      });
      let intento = 0;
      while (opciones.length < 3 && intento++ < 25) {
        const v = correcto + rint(1, 9) * (rint(0, 1) ? 10 : -10);
        if (v > 0 && !opciones.some((o) => o.v === v)) opciones.push({ v: v, m: "Volvé a hacer la cuenta con cuidado." });
      }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const btn = el("button", "op", o.v);
        btn.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) {
            resuelto = true; btn.classList.add("anim-pop"); ctx.bien();
            ronda++; await espera(950);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else {
            btn.classList.add("casi"); setTimeout(() => btn.classList.remove("casi"), 450);
            ctx.casi(o.m);
          }
        });
        fila.appendChild(btn);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── LA DIVISIÓN (M6, 4° grado — docs/auditoria-dc-caba/grado-4.md): la OTRA
   pared de 4° (con la multiplicación, el gap #1). Fase de trivia de la secuencia
   del dossier: división como "cuántas veces entra". GENERADA, exacta (el resto es
   fase posterior). Distractores por misconception (Capa 0 · C4): cociente vecino
   (off-by-one) y confundir con la resta. Explicación por error (Capa 0 · C3).
   Sube: cocientes de tabla → 2 cifras ÷ 1 cifra. ── */
GAMES.dividir = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    const nivel = ctx.cfg.nivel || 1;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const prog = rondas > 1 ? ronda / (rondas - 1) : 1;
      const fase = (nivel >= 2 || prog > 0.5) ? 2 : 1;
      let divisor, cociente;
      if (fase === 1) {
        divisor = rint(2, 9); cociente = rint(2, 9);
      } else {
        divisor = rint(2, 6); cociente = rint(11, Math.max(12, Math.floor(99 / divisor)));
      }
      const dividendo = divisor * cociente;
      const correcto = cociente;
      const cand = [
        { v: cociente + 1, m: divisor + " × " + (cociente + 1) + " es " + (divisor * (cociente + 1)) + ", se pasa de " + dividendo + "." },
        { v: cociente - 1, m: divisor + " × " + (cociente - 1) + " es " + (divisor * (cociente - 1)) + ", no llega a " + dividendo + "." },
        { v: dividendo - divisor, m: "Eso es restar. Dividir es buscar cuántas veces entra el " + divisor + " en " + dividendo + "." },
      ];
      ctx.item("dividir#" + dividendo + "e" + divisor);
      ctx.consigna("¿Cuánto es " + dividendo + " dividido " + divisor + "?");
      ctx.juego.innerHTML = "";
      const opciones = [{ v: correcto, ok: true }];
      shuffle(cand).forEach((d) => {
        if (opciones.length >= 3) return;
        if (d.v > 0 && d.v !== correcto && !opciones.some((o) => o.v === d.v)) opciones.push(d);
      });
      let intento = 0;
      while (opciones.length < 3 && intento++ < 25) {
        const v = correcto + rint(1, 4) * (rint(0, 1) ? 1 : -1);
        if (v > 0 && !opciones.some((o) => o.v === v)) opciones.push({ v: v, m: "¿Cuántas veces entra el " + divisor + " en " + dividendo + "?" });
      }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const btn = el("button", "op", o.v);
        btn.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) {
            resuelto = true; btn.classList.add("anim-pop"); ctx.bien();
            ronda++; await espera(950);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else {
            btn.classList.add("casi"); setTimeout(() => btn.classList.remove("casi"), 450);
            ctx.casi(o.m);
          }
        });
        fila.appendChild(btn);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── LA CUENTA PASO A PASO (M6 4° / M7 5° — docs/auditoria-dc-caba/): la división
   como PROCEDIMIENTO, no como trivia. Es LA pared de 4°-5° y el alumno lo pidió
   textual ("hacerla paso a paso, no solo elegir"; grado-5.md). Algoritmo POR
   APROXIMACIONES / cocientes parciales (el que enseña el DC, más accesible que el
   gancho): se le va restando al dividendo de a MÚLTIPLOS AMIGABLES del divisor
   (d × k × 10^p), con la resta acumulada VISIBLE y el cociente armándose cifra por
   cifra (estimación de cifras del cociente). Cada paso = elegir cuánto entra en el
   lugar más alto. nivel 1 (4°): ÷1 cifra, exacta. nivel 2 (5°+): con resto + la
   comprobación c × d + r = D (análisis del resto). Capa 0: cada paso errado baja la
   estrella al PRIMER intento (C2) y nombra el error (C3): "se pasa" / "todavía
   entra uno más grande" / "olvidaste el resto". La estrella solo cuenta 3★ si toda
   la cuenta salió sin un solo paso mal. ── */
GAMES.cuenta_larga = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 8;
    const nivel = ctx.cfg.nivel || 1;
    ctx.rondas(rondas);
    let ronda = 0;

    // genera D ÷ d según nivel (cociente de 2 cifras siempre; nivel 2 con resto)
    const generar = () => {
      if (nivel === 1) {
        const d = rint(2, 9), q = rint(11, 99);
        return { D: d * q, d, q, r: 0 };
      }
      const d = rint(3, 12), q = rint(11, 99), r = rint(1, d - 1);
      return { D: d * q + r, d, q, r };
    };

    // el "cacho" más grande que se puede restar de una vez: d × k × 10^p, con p el
    // lugar más alto donde el divisor entra y k (1..9) las veces que entra ahí.
    const mejorPaso = (R, d) => {
      let p = 0;
      while (d * 10 ** (p + 1) <= R) p++;
      let k = Math.floor(R / (d * 10 ** p));
      if (k > 9) k = 9;   // defensivo: nunca debería pasar (p es el lugar más alto)
      return { k, p, mult: d * k * 10 ** p, unidad: k * 10 ** p };
    };

    const jugar = () => {
      const { D, d } = generar();
      ctx.ronda(ronda);
      ctx.item("cuenta_larga#" + D + "e" + d);
      ctx.consigna("Dividí " + D + " entre " + d + ": restá de a poco hasta que no entre más.");
      ctx.juego.innerHTML = "";

      let R = D, coc = 0;
      const panel = el("div", "tablero cuenta");
      panel.appendChild(el("div", "cuenta-cab",
        '<span class="cuenta-D">' + D + '</span> ÷ <span class="cuenta-d">' + d + '</span>'));
      const estado = el("div", "cuenta-estado"); panel.appendChild(estado);
      const log = el("div", "cuenta-log"); panel.appendChild(log);
      const zona = el("div", "cuenta-zona"); panel.appendChild(zona);
      ctx.juego.appendChild(panel);

      const pintarEstado = () => {
        estado.innerHTML =
          '<div class="cuenta-chip"><small>me falta repartir</small><b>' + R + '</b></div>' +
          '<div class="cuenta-chip ac"><small>cociente</small><b>' + coc + '</b></div>';
      };

      const finRonda = async () => {
        ctx.bien();
        ronda++;
        await espera(950);
        if (ronda >= rondas) ctx.win(); else jugar();
      };

      const terminar = () => {
        pintarEstado();
        zona.innerHTML = "";
        if (R === 0) {
          zona.appendChild(el("p", "cuenta-preg", "¡No sobró nada! " + D + " ÷ " + d + " = " + coc));
          finRonda(); return;
        }
        if (nivel === 1) {
          zona.appendChild(el("p", "cuenta-preg", D + " ÷ " + d + " = " + coc + " y sobran " + R));
          finRonda(); return;
        }
        // nivel 2 — análisis del resto: comprobar c × d + r = D
        zona.appendChild(el("p", "cuenta-preg",
          "Sobran " + R + ". Comprobá: " + coc + " × " + d + " + " + R + " = ?"));
        const correcto = D;                       // = coc*d + R
        const cand = [correcto, coc * d, D + d].filter((v, i, a) => v > 0 && a.indexOf(v) === i);
        const fila = el("div", "ops");
        let hecho = false;
        shuffle(cand).forEach((v) => {
          const btn = el("button", "op", v);
          btn.addEventListener("click", async () => {
            if (hecho) return;
            if (v === correcto) { hecho = true; btn.classList.add("bien", "anim-pop"); await espera(550); finRonda(); }
            else { btn.classList.add("casi"); ctx.casi("Acordate: cociente × divisor + resto tiene que dar el número de arriba (" + D + ")."); }
          });
          fila.appendChild(btn);
        });
        zona.appendChild(fila);
      };

      const paso = () => {
        pintarEstado();
        zona.innerHTML = "";
        if (R < d) { terminar(); return; }        // ya no entra → resto final
        const best = mejorPaso(R, d);
        zona.appendChild(el("p", "cuenta-preg", "¿Cuánto le puedo sacar al " + R + "?"));
        // opciones: el cacho justo + pasarse (k+1/k+2) + quedarse corto (k-1/k-2)
        const ops = [{ k: best.k, ok: true }];
        const meter = (o) => { if (ops.length < 3 && !ops.some((x) => x.k === o.k)) ops.push(o); };
        if (best.k > 1) meter({ k: best.k - 1 });
        meter({ k: best.k + 1 });
        meter({ k: best.k + 2 });
        if (best.k > 2) meter({ k: best.k - 2 });
        const fila = el("div", "ops");
        let resuelto = false;
        shuffle(ops).forEach((o) => {
          const unidad = o.k * 10 ** best.p, mult = d * unidad;
          const btn = el("button", "op cuenta-op", d + " × " + unidad + "<small>= " + mult + "</small>");
          btn.addEventListener("click", async () => {
            if (resuelto) return;
            if (o.ok) {
              resuelto = true; btn.classList.add("bien", "anim-pop");
              R -= mult; coc += unidad;
              log.appendChild(el("div", "cuenta-linea", "− " + mult + "  <i>(" + d + " × " + unidad + ")</i>"));
              await espera(680); paso();
            } else if (mult > R) {
              btn.classList.add("casi");
              ctx.casi(d + " × " + unidad + " = " + mult + ", y solo te queda " + R + ". Se pasa.");
            } else {
              btn.classList.add("casi");
              ctx.casi("Todavía entra un cacho más grande: fijate cuántas veces entra el " + d + ".");
            }
          });
          fila.appendChild(btn);
        });
        zona.appendChild(fila);
      };

      paso();
    };
    jugar();
  },
};

/* ── DUELO DE FRACCIONES (M10, 4° grado — docs/auditoria-dc-caba/grado-4.md):
   comparación de fracciones CON BARRAS (Singapore CPA, no negociable para
   fracciones — skill §2). Ataca la misconception #1 de fracciones: "1/4 es mayor
   que 1/2 porque 4 > 2". Genera 3 tipos: mismo denominador (mandan los de
   arriba), mismo numerador y distinto denominador (la trampa: más pedazos = más
   chicos) y equivalentes (pintan lo mismo). Explicación por misconception
   apuntando a las barras (Capa 0 · C3). Reusa el render de barra de
   fracciones_equivalentes. ── */
GAMES.duelo_fracciones = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    const barra = (num, den) => {
      const cont = el("div", "fraccionBarra");
      for (let i = 0; i < den; i++) cont.appendChild(el("div", "fraccionBarra__seg" + (i < num ? " lleno" : "")));
      return cont;
    };
    const val = (f) => f.n / f.d;
    const equiv = [[1, 2, 2, 4], [1, 2, 3, 6], [1, 3, 2, 6], [1, 4, 2, 8], [2, 3, 4, 6], [3, 4, 6, 8], [1, 2, 4, 8]];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const prog = rondas > 1 ? ronda / (rondas - 1) : 1;
      const tipo = prog > 0.66 ? 2 : (prog > 0.33 ? 1 : 0);
      let A, B, iguales = false;
      if (tipo === 2 && rint(0, 2) === 0) {
        const e = equiv[rint(0, equiv.length - 1)];
        A = { n: e[0], d: e[1] }; B = { n: e[2], d: e[3] }; iguales = true;
      } else {
        const modo = tipo === 1 ? 1 : (tipo === 0 ? 0 : rint(0, 1));  // 0=mismo den, 1=mismo num (trampa)
        if (modo === 1) {
          const n = rint(1, 3);
          let d1 = rint(2, 8), d2 = rint(2, 8);
          while (d2 === d1) d2 = rint(2, 8);
          A = { n: n, d: d1 }; B = { n: n, d: d2 };
        } else {
          const d = rint(3, 8);
          let n1 = rint(1, d - 1), n2 = rint(1, d - 1);
          while (n2 === n1) n2 = rint(1, d - 1);
          A = { n: n1, d: d }; B = { n: n2, d: d };
        }
      }
      const mayor = iguales ? "iguales" : (val(A) > val(B) ? "a" : "b");
      ctx.item("duelo_fracciones#" + A.n + "/" + A.d + "_" + B.n + "/" + B.d);
      ctx.consigna("¿Cuál pinta MÁS?");
      ctx.juego.innerHTML = "";
      const explicaChica = (chica, grande) => {
        if (chica.n === grande.n && chica.d !== grande.d)
          return "Partiste en más pedazos (" + chica.d + "): cada pedazo es más CHICO. Mirá las barras.";
        if (chica.d === grande.d)
          return "Con el mismo denominador manda el de arriba: " + grande.n + " es más que " + chica.n + ".";
        return "Mirá las barras: una pinta más que la otra.";
      };
      const cards = [{ key: "a", frac: A }, { key: "b", frac: B }, { key: "iguales", frac: null }];
      const fila = el("div", "filaSprites fraccionesOpciones");
      let resuelto = false;
      shuffle(cards).forEach((c) => {
        const b = el("button", "spriteBtn fraccionBtn");
        if (c.frac) {
          b.appendChild(barra(c.frac.n, c.frac.d));
          const lbl = el("div", "", c.frac.n + "/" + c.frac.d);
          lbl.style.cssText = "font-weight:700;font-size:20px;margin-top:6px";
          b.appendChild(lbl);
        } else {
          const lbl = el("div", "", "Son iguales");
          lbl.style.cssText = "font-weight:700;font-size:18px;padding:18px 6px";
          b.appendChild(lbl);
        }
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (c.key === mayor) {
            resuelto = true; b.classList.add("anim-brinco"); ctx.bien();
            ronda++; await espera(950);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else {
            b.style.animation = "sacudir .4s ease"; setTimeout(() => (b.style.animation = ""), 450);
            let motivo;
            if (mayor === "iguales") motivo = "Fijate las barras: pintan lo MISMO. " + A.n + "/" + A.d + " y " + B.n + "/" + B.d + " son iguales.";
            else if (c.key === "iguales") motivo = "No pintan lo mismo: mirá las barras, una llena más que la otra.";
            else motivo = explicaChica(c.frac, mayor === "a" ? A : B);
            ctx.casi(motivo);
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── REPARTO JUSTO (M8, 4° grado — docs/auditoria-dc-caba/grado-4.md): la
   fracción como RESULTADO de repartir (dividir en partes iguales), con barra CPA.
   Reparto ≤ 1 (N objetos entre M chicos, N<M → cada uno recibe N/M). Distractores
   por misconception: dar 1/M (olvidar que hay N para repartir) o equivocar el
   denominador (cantidad de chicos). Explicación por error (Capa 0 · C3). ── */
GAMES.reparto_fracciones = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    const barra = (num, den) => {
      const cont = el("div", "fraccionBarra");
      for (let i = 0; i < den; i++) cont.appendChild(el("div", "fraccionBarra__seg" + (i < num ? " lleno" : "")));
      return cont;
    };
    const OBJ = [["🍫", "chocolates"], ["🍕", "pizzas"], ["🎂", "tortas"], ["🥧", "tartas"]];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const M = rint(3, 6);              // chicos = denominador
      const N = rint(1, M - 1);          // objetos = numerador (N<M → fracción < 1)
      const obj = OBJ[rint(0, OBJ.length - 1)];
      ctx.item("reparto#" + N + "e" + M);
      ctx.consigna("Reparto " + N + " " + obj[1] + " " + obj[0] + " entre " + M + " chicos en partes iguales. ¿Cuánto le toca a cada uno?");
      ctx.juego.innerHTML = "";
      const cand = [];
      if (N > 1) cand.push({ n: 1, d: M, m: "Hay " + N + " para repartir, no 1: a cada uno le tocan " + N + " pedazos de 1/" + M + "." });
      cand.push({ n: N, d: M + 1, m: "El denominador es la cantidad de chicos: son " + M + ", no " + (M + 1) + "." });
      if (N + 1 < M) cand.push({ n: N + 1, d: M, m: "Contá de nuevo: son " + N + " " + obj[1] + " entre " + M + " chicos." });
      if (N - 1 >= 1) cand.push({ n: N - 1, d: M, m: "Contá de nuevo: son " + N + " " + obj[1] + " entre " + M + " chicos." });
      const opciones = [{ n: N, d: M, ok: true }];
      shuffle(cand).forEach((c) => {
        if (opciones.length >= 3) return;
        if (!opciones.some((o) => o.n === c.n && o.d === c.d)) opciones.push(c);
      });
      let pad = 1;
      while (opciones.length < 3 && pad < M) {
        const nn = ((N + pad - 1) % (M - 1)) + 1;   // 1..M-1, fracción propia
        if (!opciones.some((o) => o.n === nn)) opciones.push({ n: nn, d: M, m: "Contá de nuevo: son " + N + " entre " + M + " chicos." });
        pad++;
      }
      const fila = el("div", "filaSprites fraccionesOpciones");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "spriteBtn fraccionBtn");
        b.appendChild(barra(o.n, o.d));
        const lbl = el("div", "", o.n + "/" + o.d); lbl.style.cssText = "font-weight:700;font-size:20px;margin-top:6px";
        b.appendChild(lbl);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) {
            resuelto = true; b.classList.add("anim-brinco"); ctx.bien();
            ronda++; await espera(950);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else {
            b.style.animation = "sacudir .4s ease"; setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi(o.m);
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── COMPLETAR EL ENTERO (M9, 4° grado — docs/auditoria-dc-caba/grado-4.md):
   fracciones en la MEDIDA (litros/kilos): ¿cuánto falta para 1 entero? Con barra
   CPA que muestra lo que ya se tiene. Complemento a 1 = (den−num)/den. Distractor
   estrella (misconception): devolver la MISMA fracción que ya se tiene. Explicación
   por error (Capa 0 · C3). ── */
GAMES.completar_entero = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    const barra = (num, den) => {
      const cont = el("div", "fraccionBarra");
      for (let i = 0; i < den; i++) cont.appendChild(el("div", "fraccionBarra__seg" + (i < num ? " lleno" : "")));
      return cont;
    };
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const d = rint(2, 6);
      const num = rint(1, d - 1);              // lo que ya tengo (< 1)
      const fn = d - num;                       // lo que falta (numerador correcto)
      const med = ["litro", "kilo"][rint(0, 1)];
      ctx.item("completar#" + num + "e" + d);
      ctx.consigna("Tenés " + num + "/" + d + " de " + med + ". ¿Cuánto falta para 1 " + med + " entero?");
      ctx.juego.innerHTML = "";
      // muestra lo que YA se tiene (barra CPA)
      const top = el("div", "tablero");
      top.appendChild(el("div", "", "Ya tenés:")).style.cssText = "font-weight:600;margin-bottom:4px";
      top.appendChild(barra(num, d));
      ctx.juego.appendChild(top);
      const faltanMsg = "Contá los pedazos vacíos: del " + num + "/" + d + " al " + d + "/" + d + " faltan " + fn + ".";
      const cand = [];
      if (num !== fn) cand.push({ n: num, d: d, m: "Eso es lo que YA tenés. Falta lo que va desde " + num + "/" + d + " hasta " + d + "/" + d + " (el entero)." });
      if (fn + 1 <= d) cand.push({ n: fn + 1, d: d, m: faltanMsg });
      if (fn - 1 >= 1) cand.push({ n: fn - 1, d: d, m: faltanMsg });
      const opciones = [{ n: fn, d: d, ok: true }];
      shuffle(cand).forEach((c) => {
        if (opciones.length >= 3) return;
        if (!opciones.some((o) => o.n === c.n && o.d === c.d)) opciones.push(c);
      });
      let pad = 1;
      while (opciones.length < 3 && pad <= d) {
        const nn = ((fn + pad - 1) % d) + 1;   // 1..d, distinto del resto
        if (!opciones.some((o) => o.n === nn)) opciones.push({ n: nn, d: d, m: faltanMsg });
        pad++;
      }
      const fila = el("div", "filaSprites fraccionesOpciones");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "spriteBtn fraccionBtn");
        b.appendChild(barra(o.n, o.d));
        const lbl = el("div", "", o.n + "/" + o.d); lbl.style.cssText = "font-weight:700;font-size:20px;margin-top:6px";
        b.appendChild(lbl);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) {
            resuelto = true; b.classList.add("anim-brinco"); ctx.bien();
            ronda++; await espera(950);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else {
            b.style.animation = "sacudir .4s ease"; setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi(o.m);
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── DUELO DE DECIMALES (M11, 4° grado — docs/auditoria-dc-caba/grado-4.md):
   decimales en uso social (precios/medidas). Ataca LA misconception de decimales:
   "12,45 > 12,5 porque 45 > 5" (leer los decimales como enteros). Comparar dos
   decimales con distinta cantidad de cifras. Explicación: igualar los decimales
   (Capa 0 · C3). ── */
GAMES.duelo_decimales = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const ent = rint(1, 24);
      let a = rint(1, 9);                 // A = ent,a   (1 decimal → a0 centésimos)
      let b = rint(11, 99);               // B = ent,b   (2 decimales)
      while (a * 10 === b) b = rint(11, 99);
      const A = { s: ent + "," + a, v: ent + a / 10, cent: a * 10 };
      const B = { s: ent + "," + b, v: ent + b / 100, cent: b };
      const mayor = A.v > B.v ? "a" : "b";
      const contexto = rint(0, 1) === 0
        ? { pre: "¿Qué precio es MÁS caro?", u: "$" }
        : { pre: "¿Qué medida es MÁS grande?", u: "" };
      ctx.item("decimales#" + A.s + "_" + B.s);
      ctx.consigna(contexto.pre);
      ctx.juego.innerHTML = "";
      const motivo = "Igualá los decimales: " + A.s + " es " + ent + "," + a + "0. Compará " + A.cent + " con " + B.cent + " centésimos, no la cantidad de números.";
      const cards = [{ key: "a", o: A }, { key: "b", o: B }];
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(cards).forEach((c) => {
        const btn = el("button", "op", contexto.u + c.o.s);
        btn.addEventListener("click", async () => {
          if (resuelto) return;
          if (c.key === mayor) {
            resuelto = true; btn.classList.add("anim-pop"); ctx.bien();
            ronda++; await espera(950);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else {
            btn.classList.add("casi"); setTimeout(() => btn.classList.remove("casi"), 450);
            ctx.casi(motivo);
          }
        });
        fila.appendChild(btn);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── PROBLEMAS DE VERDAD (M7, 4° grado — docs/auditoria-dc-caba/grado-4.md):
   problemas aplicados de multiplicación y división (la operatoria en contexto).
   Generador de plantillas. Distractores por misconception: elegir la operación
   equivocada (sumar en vez de multiplicar, etc.). Explicación C3. ── */
GAMES.problemas_mult_div = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const tipo = rint(0, 1);
      let texto, correcto, cand;
      if (tipo === 0) {
        // multiplicación: cajas × por caja
        const cajas = rint(3, 9), cada = rint(4, 12);
        correcto = cajas * cada;
        texto = "Hay " + cajas + " cajas con " + cada + " figuritas cada una. ¿Cuántas figuritas hay en total?";
        cand = [
          { v: cajas + cada, m: "Sumaste. Son " + cajas + " cajas de " + cada + " cada una: hay que multiplicar." },
          { v: cajas * cada - cada, m: "Contá TODAS las cajas: son " + cajas + ", no " + (cajas - 1) + "." },
          { v: cada - cajas, m: "Eso es restar. Cada caja aporta " + cada + " figuritas." },
        ];
      } else {
        // división: total ÷ grupos
        const grupos = rint(3, 8), cada = rint(3, 9);
        const total = grupos * cada;
        correcto = cada;
        texto = "Reparto " + total + " caramelos en " + grupos + " bolsas iguales. ¿Cuántos caramelos van en cada bolsa?";
        cand = [
          { v: total - grupos, m: "Eso es restar. Repartir en partes iguales es dividir " + total + " entre " + grupos + "." },
          { v: total + grupos, m: "Sumaste. Hay que repartir " + total + " entre " + grupos + " bolsas." },
          { v: cada + 1, m: "Fijate: " + grupos + " × " + (cada + 1) + " se pasa de " + total + "." },
        ];
      }
      ctx.item("problema#" + tipo + "_" + correcto);
      ctx.consigna(texto);
      ctx.juego.innerHTML = "";
      const opciones = [{ v: correcto, ok: true }];
      shuffle(cand).forEach((d) => {
        if (opciones.length >= 3) return;
        if (d.v > 0 && d.v !== correcto && !opciones.some((o) => o.v === d.v)) opciones.push(d);
      });
      let intento = 0;
      while (opciones.length < 3 && intento++ < 20) {
        const v = correcto + rint(1, 6) * (rint(0, 1) ? 1 : -1);
        if (v > 0 && !opciones.some((o) => o.v === v)) opciones.push({ v: v, m: "Volvé a leer el problema con cuidado." });
      }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const btn = el("button", "op", o.v);
        btn.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) {
            resuelto = true; btn.classList.add("anim-pop"); ctx.bien();
            ronda++; await espera(950);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else {
            btn.classList.add("casi"); setTimeout(() => btn.classList.remove("casi"), 450);
            ctx.casi(o.m);
          }
        });
        fila.appendChild(btn);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── PLURALES CON Z (L10, 4° grado — docs/auditoria-dc-caba/grado-4.md): plurales
   de palabras terminadas en -z (la z cambia a c). Banco fijo (memorizar el ítem
   ES el objetivo). Distractor por misconception: no cambiar la z (luz→luzes).
   Explicación con la regla (Capa 0 · C3). ── */
const PLURALES_Z_BANCO = [
  "luz", "pez", "nuez", "lápiz", "cruz", "voz", "raíz", "feliz", "capaz", "nariz", "arroz", "juez",
];
GAMES.plurales_z = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    const plural = (w) => w.slice(0, -1) + "ces";
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = PLURALES_Z_BANCO.filter((w) => !usados.includes(w));
      if (!disp.length) { usados = []; disp = PLURALES_Z_BANCO.slice(); }
      const w = disp[rint(0, disp.length - 1)];
      usados.push(w);
      const correcto = plural(w);
      ctx.item("plural_z#" + w);
      ctx.consigna("El plural de «" + w + "» es…");
      ctx.juego.innerHTML = "";
      const opciones = [
        { t: correcto, ok: true },
        { t: w + "es", m: "Las palabras con Z cambian la z por C en plural: " + w + " → " + correcto + "." },
        { t: w, m: "En plural hay que agregar la terminación: " + w + " → " + correcto + "." },
      ];
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const btn = el("button", "op", o.t);
        btn.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) {
            resuelto = true; btn.classList.add("anim-pop"); ctx.bien();
            ronda++; await espera(950);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else {
            btn.classList.add("casi"); setTimeout(() => btn.classList.remove("casi"), 450);
            ctx.casi(o.m);
          }
        });
        fila.appendChild(btn);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── MECÁNICA NUEVA: ORDENAR (commit-then-check) — 19-jul-2026, mecánica que el
   motor no tenía (docs/auditoria-dc-caba/). El chico toca las tarjetas en el
   orden correcto; cada toque le pone su número; al completar TODAS se chequea
   junto (no de a una). Si se equivoca, explica el porqué (Capa 0 · C3) y vuelve
   a mezclar la MISMA tanda para reintentar (cero fail state). Reusable: línea de
   tiempo, ordenar el cuento, secuencias de proceso, etc. ── */
function juegoOrdenar(BANCO, consignaTxt, explicaTxt, idPrefijo) {
  return {
    crear(ctx) {
      const rondas = ctx.cfg.rondas || Math.min(8, BANCO.length);
      ctx.rondas(rondas);
      let usados = [], ronda = 0;
      const nuevoSet = () => {
        let disp = BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
        if (!disp.length) { usados = []; disp = BANCO.map((_, i) => i); }
        const idx = disp[rint(0, disp.length - 1)];
        usados.push(idx);
        return idx;
      };
      const render = (setIdx) => {
        ctx.ronda(ronda);
        ctx.consigna(consignaTxt);
        ctx.item(idPrefijo + "#" + setIdx);
        ctx.juego.innerHTML = "";
        const correcto = BANCO[setIdx].items;                 // en ORDEN correcto
        const mezcla = shuffle(correcto.map((t, i) => ({ t: t, pos: i })));
        const seq = [];
        const cont = el("div", "");
        cont.style.cssText = "display:flex;flex-direction:column;gap:8px;max-width:560px;margin:0 auto;width:100%";
        const chequear = () => {
          const ok = seq.every((p, k) => p === k);
          if (ok) {
            ctx.bien();
            ronda++;
            setTimeout(() => { if (ronda >= rondas) ctx.win(); else render(nuevoSet()); }, 1150);
          } else {
            ctx.casi(explicaTxt);
            setTimeout(() => render(setIdx), 2000);            // reintenta la MISMA tanda, re-mezclada
          }
        };
        mezcla.forEach((o) => {
          const b = el("button", "op");
          b.style.cssText = "text-align:left;position:relative;padding-left:16px;width:100%";
          b.textContent = o.t;
          b.addEventListener("click", () => {
            if (b.dataset.puesto) return;
            seq.push(o.pos);
            b.dataset.puesto = String(seq.length);
            b.style.paddingLeft = "48px";
            b.style.opacity = "0.65";
            const badge = el("span", "", String(seq.length));
            badge.style.cssText = "position:absolute;left:10px;top:50%;transform:translateY(-50%);background:#2b2b3a;color:#fff;border-radius:50%;width:28px;height:28px;display:grid;place-items:center;font-weight:700";
            b.appendChild(badge);
            if (seq.length === correcto.length) chequear();
          });
          cont.appendChild(b);
        });
        ctx.juego.appendChild(cont);
      };
      render(nuevoSet());
    },
  };
}

/* ── LÍNEA DE TIEMPO (S3, 4° grado): ordenar hitos históricos (conquista, colonia,
   virreinatos) del más antiguo al más nuevo. Usa la mecánica ORDENAR. Los años
   quedan a la vista como andamiaje. ── */
const LINEA_TIEMPO_BANCO = [
  { items: ["Colón llega a América (1492)", "Primera fundación de Buenos Aires (1536)", "Segunda fundación de Buenos Aires (1580)"] },
  { items: ["Primera fundación de Buenos Aires (1536)", "Se crea el Virreinato del Perú (1542)", "Se crea el Virreinato del Río de la Plata (1776)"] },
  { items: ["Vivían los pueblos originarios en América", "Llegan los españoles a América (1492)", "Se funda el Virreinato del Río de la Plata (1776)"] },
  { items: ["Colón llega a América (1492)", "Segunda fundación de Buenos Aires (1580)", "Se crea el Virreinato del Río de la Plata (1776)"] },
  { items: ["Primera fundación de Buenos Aires (1536)", "Se crea el Virreinato del Perú (1542)", "Segunda fundación de Buenos Aires (1580)"] },
  { items: ["Colón llega a América (1492)", "Se crea el Virreinato del Perú (1542)", "Se crea el Virreinato del Río de la Plata (1776)"] },
];
GAMES.linea_tiempo = juegoOrdenar(LINEA_TIEMPO_BANCO, "Ordená del más ANTIGUO al más nuevo. Tocá en orden.", "Ordená por año: el más viejo (el número más chico) va primero.", "linea_tiempo");

/* ── HISTORIA EN ORDEN (L15, 4° grado): ordenar las partes de un cuento (situación
   inicial → conflicto → resolución). Usa la mecánica ORDENAR. Sin años: es lógica
   narrativa (qué pasó primero). ── */
const HISTORIA_ORDEN_BANCO = [
  { items: ["Un chico encontró un huevo raro en el bosque", "Del huevo salió un dragón que crecía sin parar", "Se hicieron amigos y volaron juntos por el cielo"] },
  { items: ["María quería aprender a andar en bici", "Se caía y se caía, y le dolían las rodillas", "Después de practicar toda la semana, ya andaba sola"] },
  { items: ["A Tomás se le perdió el perro en la plaza", "Lo buscó por todos lados y no aparecía", "Un vecino lo había guardado y se lo devolvió"] },
  { items: ["Los amigos plantaron una semilla en una maceta", "Pasaban los días y la semilla no crecía", "Con agua y sol, al fin brotó una plantita"] },
  { items: ["Sofía empezó a preparar una torta", "Se dio cuenta de que faltaba el azúcar", "Fue a comprarla, la terminó y quedó riquísima"] },
];
GAMES.historia_orden = juegoOrdenar(HISTORIA_ORDEN_BANCO, "Ordená el cuento: ¿qué pasó primero? Tocá en orden.", "Pensá: primero cómo empieza, después el problema, y al final cómo se resuelve.", "historia_orden");

/* ── PUEBLOS ORIGINARIOS Y LA COLONIA (4° grado — docs/auditoria-dc-caba/grado-4.md,
   gap #4: "Ciencias Sociales histórico completo — originarios → conquista → colonia
   → fundaciones de Buenos Aires: CERO actividades"). linea_tiempo ya ORDENA la
   cronología; esto enseña el CONTENIDO (quiénes eran, qué pasó, por qué). Trivia de
   opción múltiple con distractores por misconception (Capa 0 · C4) y explicación del
   porqué en cada error (Capa 0 · C3). La opción correcta es siempre ops[0]; se
   barajan al mostrar. Contenido curado, históricamente correcto y a nivel 9 años. ── */
const HISTORIA4_BANCO = [
  { q: "¿Quiénes vivían en nuestro territorio ANTES de que llegaran los españoles?",
    ops: ["Los pueblos originarios, como diaguitas, guaraníes y tehuelches", "Los españoles", "No vivía nadie, estaba vacío"],
    m: "Mucho antes de los españoles ya vivían acá los pueblos originarios: diaguitas, guaraníes, tehuelches y muchos más." },
  { q: "Los diaguitas vivían en los cerros del noroeste. ¿A qué se dedicaban?",
    ops: ["Cultivaban maíz en terrazas en las laderas", "Cazaban ballenas en el mar", "Fabricaban autos de metal"],
    m: "Los diaguitas eran agricultores: armaban terrazas en los cerros para cultivar maíz y zapallo." },
  { q: "Los tehuelches vivían en la Patagonia. Eran un pueblo…",
    ops: ["Nómade: cazaban guanacos y se trasladaban", "Que vivía siempre en casas de piedra", "De navegantes que cruzaban el océano"],
    m: "Los tehuelches eran nómades: se movían de un lugar a otro siguiendo a los guanacos que cazaban." },
  { q: "¿Qué quiere decir que un pueblo era «nómade»?",
    ops: ["Que se trasladaba de un lugar a otro", "Que vivía siempre en el mismo lugar", "Que no tenía jefes ni familias"],
    m: "Nómade = que no vive fijo en un lugar, sino que se traslada buscando comida." },
  { q: "¿En qué año llegó Cristóbal Colón a América?",
    ops: ["En 1492", "En 1810", "En 1776"],
    m: "Colón llegó a América en 1492. (En 1810 fue la Revolución de Mayo, mucho después.)" },
  { q: "¿Qué buscaba Colón cuando cruzó el océano?",
    ops: ["Un camino a Asia navegando hacia el oeste", "El Polo Sur", "Oro en la Luna"],
    m: "Colón quería llegar a Asia (las Indias) por el mar hacia el oeste, y sin querer se encontró con América." },
  { q: "¿Cómo se llama la etapa en que los españoles dominaron por la fuerza a los pueblos originarios?",
    ops: ["La conquista", "La independencia", "La excursión"],
    m: "Se llama la conquista: los españoles ocuparon el territorio y sometieron a los pueblos originarios." },
  { q: "¿Qué les dio ventaja a los españoles en la conquista?",
    ops: ["Las armas de fuego y los caballos", "Que eran muchísimos más", "Que hablaban el mismo idioma que los originarios"],
    m: "Los españoles trajeron caballos y armas de fuego, que los pueblos originarios no conocían." },
  { q: "Durante la época colonial, ¿quién gobernaba nuestro territorio?",
    ops: ["El rey de España, a través de sus autoridades", "Un presidente elegido por el pueblo", "Los caciques de los pueblos originarios"],
    m: "En la colonia mandaba el rey de España desde muy lejos, con autoridades que lo representaban acá." },
  { q: "En la época colonial, el Cabildo era…",
    ops: ["El gobierno de la ciudad", "Una iglesia muy grande", "Un barco español"],
    m: "El Cabildo era el gobierno de la ciudad: se ocupaba de la limpieza, los precios y el orden." },
  { q: "¿Qué era una pulpería en la época colonial?",
    ops: ["Una tienda donde se vendía de todo y se juntaba la gente", "Una fábrica de pelotas", "Una escuela de música"],
    m: "La pulpería era el almacén del pueblo: se compraba de todo y la gente se reunía a charlar." },
  { q: "¿Quiénes eran los «criollos» en la colonia?",
    ops: ["Los hijos de españoles nacidos en América", "Los reyes que vivían en España", "Los pueblos originarios de la selva"],
    m: "Criollos eran los hijos de españoles pero nacidos acá, en América." },
  { q: "¿Por qué Buenos Aires se tuvo que fundar DOS veces?",
    ops: ["La primera fundación fracasó y se abandonó; se fundó de nuevo más tarde", "Porque a nadie le gustaba el nombre", "Porque la ciudad se mudó de provincia"],
    m: "La 1ª fundación (1536) fracasó por el hambre y los ataques, y la abandonaron. Recién en 1580 se fundó de nuevo y quedó." },
  { q: "¿Quién hizo la PRIMERA fundación de Buenos Aires, en 1536?",
    ops: ["Pedro de Mendoza", "Juan de Garay", "Cristóbal Colón"],
    m: "Pedro de Mendoza fundó Buenos Aires por primera vez en 1536, pero esa ciudad no sobrevivió." },
  { q: "¿Quién fundó Buenos Aires por SEGUNDA vez, en 1580?",
    ops: ["Juan de Garay", "Pedro de Mendoza", "José de San Martín"],
    m: "Juan de Garay volvió a fundar Buenos Aires en 1580, y esta vez la ciudad quedó para siempre." },
];
GAMES.historia_originarios = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 8;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.consigna("Elegí la respuesta correcta.");
      ctx.juego.innerHTML = "";
      let libres = HISTORIA4_BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!libres.length) { usados = []; libres = HISTORIA4_BANCO.map((_, i) => i); }
      const idx = libres[rint(0, libres.length - 1)];
      usados.push(idx);
      const item = HISTORIA4_BANCO[idx];
      ctx.item("historia4#" + idx);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:21px;font-family:'Baloo',sans-serif">${item.q}</span>`));
      ctx.juego.appendChild(arriba);
      const correcta = item.ops[0];
      const fila = el("div", "opsTexto");
      fila.setAttribute("data-ok", correcta);
      let resuelto = false;
      shuffle(item.ops).forEach((op) => {
        const b = el("button", "op-texto", op);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op === correcta) {
            resuelto = true; b.classList.add("bien", "anim-pop"); ctx.bien();
            ronda++; await espera(950);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else {
            b.classList.add("casi"); ctx.casi(item.m);
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── Helper genérico de trivia de opción múltiple con opciones de TEXTO largo
   (contenido: historia, gramática, ciencias). Banco de {q, ops, m}: ops[0] es la
   correcta, se barajan al mostrar; el error muestra la explicación m (Capa 0 · C3)
   con distractores por misconception (C4). Reusable para futuras actividades de
   contenido en vez de duplicar el mismo esqueleto. ── */
function juegoTriviaTexto(banco, consigna, idPrefix, rondasDefault) {
  return {
    crear(ctx) {
      const rondas = ctx.cfg.rondas || rondasDefault || 8;
      ctx.rondas(rondas);
      let usados = [], ronda = 0;
      const jugar = () => {
        ctx.ronda(ronda);
        ctx.consigna(consigna);
        ctx.juego.innerHTML = "";
        let libres = banco.map((_, i) => i).filter((i) => !usados.includes(i));
        if (!libres.length) { usados = []; libres = banco.map((_, i) => i); }
        const idx = libres[rint(0, libres.length - 1)];
        usados.push(idx);
        const item = banco[idx];
        ctx.item(idPrefix + "#" + idx);
        const arriba = el("div", "tablero");
        arriba.appendChild(el("div", "spriteQuieto",
          `<span style="font-size:21px;font-family:'Baloo',sans-serif">${item.q}</span>`));
        ctx.juego.appendChild(arriba);
        const correcta = item.ops[0];
        const fila = el("div", "opsTexto");
        fila.setAttribute("data-ok", correcta);
        let resuelto = false;
        shuffle(item.ops).forEach((op) => {
          const b = el("button", "op-texto", op);
          b.addEventListener("click", async () => {
            if (resuelto) return;
            if (op === correcta) {
              resuelto = true; b.classList.add("bien", "anim-pop"); ctx.bien();
              ronda++; await espera(950);
              if (ronda >= rondas) ctx.win(); else jugar();
            } else {
              b.classList.add("casi"); ctx.casi(item.m);
            }
          });
          fila.appendChild(b);
        });
        ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
      };
      jugar();
    },
  };
}

/* ── EL DIÁLOGO CON RAYA (4° grado — docs/auditoria-dc-caba/grado-4.md, gap #3 de
   Lengua: "sin sujeto/predicado (ya hecho), conectores, diálogo con raya,
   estructura narrativa"). Enseña a puntuar el diálogo: la RAYA (—) abre lo que dice
   el personaje y otra raya va antes de la aclaración del narrador (—dijo/—preguntó).
   Trivia "¿cuál está bien escrito?": la correcta vs. errores reales (comillas en vez
   de raya, falta la raya de apertura, falta la raya del narrador). Capa 0 C3/C4. ── */
const DIALOGO_BANCO = [
  { q: "Pedro dice que tiene hambre:",
    ops: ["—Tengo hambre —dijo Pedro.", "\"Tengo hambre\", dijo Pedro.", "Tengo hambre —dijo Pedro."],
    m: "El diálogo abre con raya (—) pegada a lo que dice el personaje. En español usamos raya, no comillas." },
  { q: "Ana pregunta si van a jugar:",
    ops: ["—¿Vamos a jugar? —preguntó Ana.", "¿Vamos a jugar? preguntó Ana.", "—¿Vamos a jugar? preguntó Ana."],
    m: "Va una raya al inicio y OTRA raya antes de la aclaración del narrador (—preguntó Ana)." },
  { q: "La maestra saluda a los chicos:",
    ops: ["—¡Buen día, chicos! —dijo la maestra.", "\"¡Buen día, chicos!\" dijo la maestra.", "¡Buen día, chicos! dijo la maestra."],
    m: "El diálogo se marca con raya (—): una abre lo que dice y otra abre la aclaración del narrador." },
  { q: "Tomás pide ayuda:",
    ops: ["—¿Me ayudás? —pidió Tomás.", "—¿Me ayudás? pidió Tomás.", "¿Me ayudás? —pidió Tomás."],
    m: "Falta una raya: recordá que van DOS, una antes de lo dicho y otra antes de «pidió Tomás»." },
  { q: "Mamá llama a cenar:",
    ops: ["—¡A cenar! —llamó mamá.", "'¡A cenar!' llamó mamá.", "¡A cenar! —llamó mamá."],
    m: "El diálogo abre con raya (—) al inicio, no con comillas ni sin nada." },
  { q: "Sofía grita que ganó:",
    ops: ["—¡Gané! —gritó Sofía.", "—¡Gané! gritó Sofía.", "\"¡Gané!\", gritó Sofía."],
    m: "Antes de la aclaración del narrador (gritó Sofía) va otra raya: —gritó Sofía." },
  { q: "El abuelo empieza un cuento:",
    ops: ["—Había una vez… —empezó el abuelo.", "Había una vez… empezó el abuelo.", "—Había una vez… empezó el abuelo."],
    m: "Van dos rayas: una abre lo que dice y otra abre «empezó el abuelo»." },
  { q: "Lucía pregunta la hora:",
    ops: ["—¿Qué hora es? —preguntó Lucía.", "\"¿Qué hora es?\" preguntó Lucía.", "¿Qué hora es? preguntó Lucía."],
    m: "En un diálogo usamos raya (—), no comillas, y la raya abre lo que dice el personaje." },
  { q: "El capitán da la orden:",
    ops: ["—¡Todos a bordo! —ordenó el capitán.", "¡Todos a bordo! ordenó el capitán.", "—¡Todos a bordo! ordenó el capitán."],
    m: "Falta la raya antes de la aclaración: —ordenó el capitán." },
  { q: "Juan se despide:",
    ops: ["—¡Hasta mañana! —dijo Juan.", "'¡Hasta mañana!' dijo Juan.", "¡Hasta mañana! —dijo Juan."],
    m: "El diálogo abre con raya (—), no con comillas simples ni sin marca." },
  { q: "La nena avisa que llueve:",
    ops: ["—¡Está lloviendo! —avisó la nena.", "—¡Está lloviendo! avisó la nena.", "\"¡Está lloviendo!\" avisó la nena."],
    m: "Antes de «avisó la nena» va otra raya: la aclaración del narrador también se abre con raya." },
  { q: "El nene contesta que sí:",
    ops: ["—Sí, quiero —contestó el nene.", "Sí, quiero contestó el nene.", "—Sí, quiero contestó el nene."],
    m: "Van dos rayas: —Sí, quiero —contestó el nene." },
];
GAMES.dialogo_raya = juegoTriviaTexto(DIALOGO_BANCO, "¿Cuál está bien escrito?", "dialogo_raya");

/* ── EL CIELO DE DÍA Y DE NOCHE (3° grado — docs/auditoria-dc-caba/grado-3.md,
   gap #5: "observación del cielo", uno de los dos bloques nuevos de CdM de 3°,
   ausente; el slot de ciencias lo ocupaba `estaciones`, de inicial). Trivia de
   contenido (reusa juegoTriviaTexto): día/noche y por qué, salida y puesta del Sol,
   las sombras según la altura del Sol, la Luna (refleja al Sol, cambia de forma),
   las estrellas (soles lejanos), el telescopio. Curado, correcto y a nivel 8 años.
   Distractores por misconception (C4) + explicación (C3). ── */
const CIELO_BANCO = [
  { q: "¿Qué vemos en el cielo de DÍA?",
    ops: ["El Sol", "La Luna llena y las estrellas", "No se ve nada"],
    m: "De día vemos el Sol; la Luna y las estrellas se ven mucho mejor de noche." },
  { q: "¿Por qué hay día y noche?",
    ops: ["Porque la Tierra gira: a veces nuestra parte mira al Sol y a veces no", "Porque el Sol se apaga a la noche", "Porque la Luna tapa al Sol todas las noches"],
    m: "La Tierra gira sobre sí misma. Cuando nuestra parte mira al Sol es de día; cuando mira al otro lado, es de noche." },
  { q: "¿Por dónde SALE el Sol a la mañana?",
    ops: ["Por el este", "Por el oeste", "Justo por arriba de nuestra cabeza"],
    m: "El Sol sale por el este (donde amanece) y se esconde por el oeste al atardecer." },
  { q: "¿Dónde está el Sol al MEDIODÍA?",
    ops: ["Bien alto en el cielo", "Abajo, tocando el suelo", "No se ve al mediodía"],
    m: "Al mediodía el Sol llega a su punto más alto en el cielo." },
  { q: "¿Cuándo son más LARGAS las sombras?",
    ops: ["A la mañana temprano y al atardecer", "Al mediodía", "De noche, con la Luna"],
    m: "Cuando el Sol está bajito (mañana y tarde), las sombras se estiran largas. Al mediodía, con el Sol alto, son cortitas." },
  { q: "Al MEDIODÍA de un día soleado, tu sombra…",
    ops: ["Es corta, casi debajo tuyo", "Es larguísima", "Desaparece para siempre"],
    m: "Con el Sol bien alto, la sombra queda corta y casi a tus pies." },
  { q: "¿Qué vemos en el cielo de NOCHE, sin nubes?",
    ops: ["La Luna y las estrellas", "El Sol", "Un arcoíris"],
    m: "De noche vemos la Luna y las estrellas; el Sol está iluminando el otro lado de la Tierra." },
  { q: "¿La Luna tiene luz propia?",
    ops: ["No: nos refleja la luz del Sol", "Sí, es una estrella caliente", "Sí, tiene fuego adentro"],
    m: "La Luna no brilla sola: como un espejo, nos refleja la luz del Sol." },
  { q: "Las estrellas son…",
    ops: ["Soles enormes que están muy muy lejos", "Lamparitas colgadas en el cielo", "Agujeritos en el cielo"],
    m: "Cada estrella es un sol gigante, pero está tan lejos que la vemos chiquitita." },
  { q: "Si mirás la Luna varias noches seguidas, ves que…",
    ops: ["Cambia de forma con los días (fases)", "Es siempre exactamente igual", "Se apaga una semana entera"],
    m: "La Luna va cambiando de forma: creciente, llena, menguante… son sus fases." },
  { q: "¿Qué instrumento usan para ver mejor las estrellas y los planetas?",
    ops: ["El telescopio", "El microscopio", "La brújula"],
    m: "El telescopio acerca lo que está lejísimos, como las estrellas y los planetas. (El microscopio es para lo muy chiquito.)" },
  { q: "Cuando en Argentina es de día, del otro lado de la Tierra…",
    ops: ["Es de noche", "También es de día", "No hay nada"],
    m: "Como la Tierra es redonda y gira, mientras de un lado es de día, del otro es de noche." },
  { q: "Durante el día, el Sol parece moverse en el cielo…",
    ops: ["Del este al oeste", "Del oeste al este", "No se mueve nada"],
    m: "El Sol parece cruzar el cielo del este (a la mañana) al oeste (a la tarde)." },
  { q: "¿Por qué de día casi no vemos las estrellas?",
    ops: ["Porque la luz del Sol es tan fuerte que las tapa", "Porque de día se apagan", "Porque se van a otro país"],
    m: "Las estrellas siguen ahí de día, pero la luz del Sol es tan brillante que no las deja ver." },
];
GAMES.cielo = juegoTriviaTexto(CIELO_BANCO, "Elegí la respuesta correcta.", "cielo");

/* ── EL CEREBRO Y LAS DEFENSAS (7° — docs/auditoria-dc-caba/grado-7.md gap #4:
   sistema nervioso + inmune/vacunas = 0). Trivia de contenido (juegoTriviaTexto). ── */
const SISNERV_BANCO = [
  { q: "¿Qué órgano es el «jefe» que controla todo el cuerpo?", ops: ["El cerebro", "El corazón", "El estómago"], m: "El cerebro dirige y controla el cuerpo." },
  { q: "El cerebro, la médula espinal y los nervios forman el sistema…", ops: ["nervioso", "digestivo", "respiratorio"], m: "Juntos forman el sistema nervioso." },
  { q: "¿Para qué sirven los nervios?", ops: ["Llevan mensajes entre el cerebro y el resto del cuerpo", "Bombean la sangre", "Digieren la comida"], m: "Los nervios transmiten mensajes hacia y desde el cerebro." },
  { q: "Sacás la mano rápido al tocar algo caliente. Eso es…", ops: ["un reflejo, para protegerte", "una casualidad", "algo del estómago"], m: "Es un acto reflejo: el cuerpo reacciona rapidísimo para cuidarte." },
  { q: "Los cinco sentidos mandan la información al…", ops: ["cerebro", "corazón", "hígado"], m: "Los sentidos envían la información al cerebro, que la interpreta." },
  { q: "¿Qué protege al cerebro?", ops: ["El cráneo (los huesos de la cabeza)", "Solo la piel", "Nada"], m: "El cráneo es una caja de huesos que protege al cerebro." },
  { q: "Dormir bien es importante porque…", ops: ["el cerebro descansa y se recupera", "no sirve para nada", "hace mal"], m: "Durante el sueño el cerebro descansa y ordena lo aprendido." },
  { q: "¿Qué son las vacunas?", ops: ["Preparados que enseñan al cuerpo a defenderse de una enfermedad", "Caramelos", "Solo vitaminas para crecer"], m: "La vacuna entrena al cuerpo para defenderse de una enfermedad." },
  { q: "Las vacunas sirven sobre todo para…", ops: ["prevenir enfermedades antes de que aparezcan", "curar cuando ya estás grave", "nada"], m: "Las vacunas previenen: preparan las defensas ANTES de enfermarte." },
  { q: "El sistema que nos defiende de los microbios se llama…", ops: ["sistema inmune (o inmunitario)", "sistema nervioso", "sistema óseo"], m: "El sistema inmune combate los microbios que nos enferman." },
  { q: "Cuando te vacunás, tu cuerpo aprende a fabricar…", ops: ["defensas contra esa enfermedad", "más huesos", "sangre nueva"], m: "El cuerpo genera defensas (anticuerpos) contra esa enfermedad." },
  { q: "¿Por qué conviene que muchas personas estén vacunadas?", ops: ["Así la enfermedad casi no se puede contagiar", "Solo por moda", "No sirve"], m: "Si la mayoría está vacunada, la enfermedad casi no circula y protege a todos." },
  { q: "La fiebre suele aparecer cuando…", ops: ["el cuerpo está luchando contra una infección", "tenés hambre", "hace frío afuera"], m: "La fiebre es una señal de que el cuerpo está combatiendo una infección." },
  { q: "Para cuidar el cerebro conviene…", ops: ["dormir bien y usar casco al andar en bici", "no dormir nunca", "golpearse la cabeza"], m: "Dormir bien y proteger la cabeza (casco) cuidan el sistema nervioso." },
];
GAMES.cerebro_defensas = juegoTriviaTexto(SISNERV_BANCO, "Elegí la respuesta correcta.", "cerebro");

/* ── LUZ Y MATERIALES (2° — docs/auditoria-dc-caba/grado-2.md gap #5: el único eje
   de Naturales del grado, sin actividad). Fuentes de luz, sombras, transparente/
   opaco. Trivia (juegoTriviaTexto). ── */
const LUZMAT_BANCO = [
  { q: "¿Qué necesitamos para poder VER las cosas?", ops: ["Luz", "Silencio", "Frío"], m: "Sin luz no podemos ver: la luz nos deja ver las cosas." },
  { q: "De día, la principal fuente de luz es…", ops: ["el Sol", "la Luna", "una vela"], m: "De día, la luz viene del Sol." },
  { q: "¿Cuál da su PROPIA luz?", ops: ["Una lámpara encendida", "Un espejo", "Una piedra"], m: "La lámpara encendida es una fuente de luz; el espejo solo refleja." },
  { q: "¿Cuál NO tiene luz propia?", ops: ["La Luna (refleja la del Sol)", "El Sol", "Una linterna encendida"], m: "La Luna no brilla sola: refleja la luz del Sol." },
  { q: "Cuando la luz no puede pasar por un objeto, se forma…", ops: ["una sombra", "un arcoíris", "un ruido"], m: "Si un objeto tapa la luz, detrás se forma su sombra." },
  { q: "Un material por el que la luz PASA y se ve bien es…", ops: ["el vidrio", "la madera", "el cartón"], m: "El vidrio es transparente: deja pasar la luz." },
  { q: "Un material por el que la luz NO pasa es…", ops: ["la madera", "el vidrio limpio", "el agua clara"], m: "La madera es opaca: no deja pasar la luz." },
  { q: "El vidrio transparente deja pasar la luz, entonces es…", ops: ["transparente", "opaco", "blando"], m: "Transparente = deja pasar la luz y se ve del otro lado." },
  { q: "Si ponés tu mano entre una linterna y la pared, ves…", ops: ["la sombra de tu mano", "un color nuevo", "nada"], m: "Tu mano tapa la luz y se dibuja su sombra en la pared." },
  { q: "¿De qué material suele ser una ventana para dejar entrar la luz?", ops: ["Vidrio", "Madera", "Metal"], m: "La ventana es de vidrio para que entre la luz." },
  { q: "La madera es un material…", ops: ["opaco (no deja pasar la luz)", "transparente", "líquido"], m: "La madera es opaca: la luz no la atraviesa." },
  { q: "Para hacer sombras chinas necesitás…", ops: ["una luz y un objeto que la tape", "mucho silencio", "agua"], m: "Con una luz y un objeto delante se arma la sombra." },
  { q: "¿Cuál de estos es una fuente de luz?", ops: ["El fuego", "Una roca", "Una silla"], m: "El fuego da luz propia: es una fuente de luz." },
  { q: "Un vaso de vidrio y una taza de cerámica: ¿por cuál pasa la luz?", ops: ["Por el vaso de vidrio", "Por la taza de cerámica", "Por ninguno"], m: "El vidrio es transparente; la cerámica es opaca." },
];
GAMES.luz_materiales = juegoTriviaTexto(LUZMAT_BANCO, "Elegí la respuesta correcta.", "luzmat");

/* ── CAZADOR DE ERRORES (7° — docs/auditoria-dc-caba/grado-7.md L14: ortografía,
   queja #1 de las familias, estaba en cero). Elegir la palabra bien escrita:
   tildación (agudas/graves/esdrújulas), b/v, g/j, h, homófonos y diéresis. ── */
const ORTO7_BANCO = [
  { q: "El vegetal grande con tronco y hojas:", ops: ["árbol", "arbol", "árvol"], m: "«árbol» lleva tilde (grave terminada en consonante) y va con B." },
  { q: "El órgano que late en el pecho:", ops: ["corazón", "corazon", "corasón"], m: "«corazón» es aguda terminada en N: lleva tilde. Y va con Z." },
  { q: "Las personas, la multitud:", ops: ["gente", "jente", "guente"], m: "«gente» va con G." },
  { q: "Votar o escoger a alguien:", ops: ["elegir", "elejir", "eleguir"], m: "«elegir» va con G." },
  { q: "Un recado o texto que enviás:", ops: ["mensaje", "mensage", "menzaje"], m: "Las palabras terminadas en -aje van con J: mensaje." },
  { q: "Lo duro y blanco que tenemos por dentro:", ops: ["hueso", "ueso", "huezo"], m: "«hueso» empieza con H (muda)." },
  { q: "Construir o fabricar algo:", ops: ["hacer", "acer", "aser"], m: "«hacer» empieza con H y va con C." },
  { q: "En este mismo momento:", ops: ["ahora", "aora", "ahorra"], m: "«ahora» lleva H en el medio (y una sola R)." },
  { q: "El pasado del verbo estar (él ___):", ops: ["estuvo", "estubo", "estuvó"], m: "«estuvo» va con V." },
  { q: "«Yo ___ caminando» (pasado de ir):", ops: ["iba", "iva", "hiba"], m: "«iba» (del verbo ir) va con B." },
  { q: "La persona que cura a los enfermos:", ops: ["médico", "medico", "médicó"], m: "«médico» es esdrújula: todas llevan tilde." },
  { q: "Lo contrario de difícil:", ops: ["fácil", "facil", "fásil"], m: "«fácil» es grave terminada en consonante: lleva tilde." },
  { q: "«Espero que ___ sol» (del verbo haber):", ops: ["haya", "halla", "aya"], m: "«haya» (del verbo haber) va con H y con Y." },
  { q: "«Hoy ___ mucho calor» (del verbo hacer):", ops: ["hace", "ase", "hase"], m: "«hace» (del verbo hacer) va con H y con C." },
  { q: "La pena o timidez que se siente:", ops: ["vergüenza", "verguenza", "vergenza"], m: "«vergüenza» lleva diéresis (ü) para que suene la U: güe." },
  { q: "El animal alto de cuello largo:", ops: ["jirafa", "girafa", "jiraffa"], m: "«jirafa» va con J." },
];
GAMES.cazador_errores = juegoTriviaTexto(ORTO7_BANCO, "Tocá la palabra bien escrita.", "orto7");

/* ── VALOR POSICIONAL (2° — docs/auditoria-dc-caba/grado-2.md gap #2: valor
   posicional hasta 1.000, ausente). Cuánto vale cada cifra, descomposición,
   unidades/decenas/centenas. Trivia (juegoTriviaTexto). ── */
const VALPOS_BANCO = [
  { q: "En el número 45, ¿cuánto vale el 4?", ops: ["40", "4", "400"], m: "El 4 está en las decenas: vale 40." },
  { q: "En el número 235, ¿cuánto vale el 2?", ops: ["200", "20", "2"], m: "El 2 está en las centenas: vale 200." },
  { q: "En el número 235, ¿cuánto vale el 3?", ops: ["30", "3", "300"], m: "El 3 está en las decenas: vale 30." },
  { q: "En el número 235, ¿cuánto vale el 5?", ops: ["5", "50", "500"], m: "El 5 está en las unidades: vale 5." },
  { q: "En el número 70, ¿cuánto vale el 7?", ops: ["70", "7", "700"], m: "El 7 está en las decenas: vale 70." },
  { q: "¿Cuántas decenas hay en 60?", ops: ["6", "60", "16"], m: "60 = 6 decenas (6 grupos de 10)." },
  { q: "¿Cuántas centenas hay en 300?", ops: ["3", "30", "300"], m: "300 = 3 centenas (3 grupos de 100)." },
  { q: "El número 100 tiene…", ops: ["1 centena, 0 decenas y 0 unidades", "10 centenas", "100 decenas"], m: "100 = 1 centena, 0 decenas y 0 unidades." },
  { q: "¿Qué número es 2 centenas, 4 decenas y 5 unidades?", ops: ["245", "2045", "254"], m: "2 centenas (200) + 4 decenas (40) + 5 = 245." },
  { q: "¿Qué número es 3 decenas y 6 unidades?", ops: ["36", "360", "63"], m: "3 decenas (30) + 6 unidades = 36." },
  { q: "En el número 508, ¿cuánto vale el 0?", ops: ["0", "50", "500"], m: "No hay decenas: el 0 vale 0." },
  { q: "¿Cuál 5 vale MÁS: el de 52 o el de 25?", ops: ["El de 52 (vale 50)", "El de 25 (vale 5)", "Valen igual"], m: "En 52 el 5 está en las decenas (50); en 25, en las unidades (5)." },
  { q: "300 + 40 + 5 = ", ops: ["345", "3045", "0345"], m: "3 centenas + 4 decenas + 5 unidades = 345." },
  { q: "¿Cuántas decenas tiene el número 89?", ops: ["8", "9", "89"], m: "El 8 está en las decenas: 89 tiene 8 decenas." },
];
GAMES.valor_posicional = juegoTriviaTexto(VALPOS_BANCO, "Elegí la respuesta correcta.", "valpos");

/* ── LOS SENTIDOS (1° — Conocimiento del Mundo, el cuerpo y los 5 sentidos).
   Trivia con pista visual (emoji) y opciones cortas para 1° (juegoTriviaTexto). ── */
const SENTIDOS_BANCO = [
  { q: "👀 ¿Con qué parte del cuerpo VES?", ops: ["Los ojos", "Las orejas", "La nariz"], m: "Con los ojos vemos: es el sentido de la vista." },
  { q: "👂 ¿Con qué OÍS los sonidos?", ops: ["Los oídos", "Los ojos", "La lengua"], m: "Con los oídos escuchamos: es el sentido del oído." },
  { q: "👃 ¿Con qué OLÉS?", ops: ["La nariz", "La boca", "Los pies"], m: "Con la nariz olemos: es el sentido del olfato." },
  { q: "👅 ¿Con qué sentís el GUSTO de la comida?", ops: ["La lengua", "Los ojos", "Las manos"], m: "Con la lengua sentimos los sabores: es el gusto." },
  { q: "✋ ¿Con qué sentís si algo es suave o áspero?", ops: ["La piel", "Los oídos", "La nariz"], m: "Con la piel sentimos: es el sentido del tacto." },
  { q: "🍋 Un limón es…", ops: ["ácido", "dulce como el azúcar", "salado como el mar"], m: "El limón es ácido: lo sentís con el gusto." },
  { q: "🌸 Para saber si una flor huele rico usás…", ops: ["la nariz", "la lengua", "los pies"], m: "El olor lo sentís con la nariz (olfato)." },
  { q: "🌈 Para ver los colores usás…", ops: ["los ojos", "los oídos", "las manos"], m: "Los colores los ves con los ojos (vista)." },
  { q: "🧊 Si tocás un hielo, sentís que está…", ops: ["frío", "caliente", "dulce"], m: "El hielo está frío: lo sentís con el tacto." },
  { q: "🍬 Un caramelo es…", ops: ["dulce", "amargo", "salado"], m: "El caramelo es dulce: lo sentís con el gusto." },
  { q: "🔊 Un ruido muy fuerte lo escuchás con…", ops: ["los oídos", "los ojos", "la nariz"], m: "Los sonidos los oís con los oídos." },
  { q: "🎵 La música la disfrutás con el sentido del…", ops: ["oído", "gusto", "olfato"], m: "La música se escucha con el oído." },
];
GAMES.sentidos = juegoTriviaTexto(SENTIDOS_BANCO, "Elegí la respuesta correcta.", "sentidos");

/* ── CAMINO A LA INDEPENDENCIA (5° grado — docs/auditoria-dc-caba/grado-5.md, gap
   #3: "ausencia total del proceso 1810-1853 en Sociales — al alumno de 5° se le
   ofrece el contenido de 4° [colonial] y nada del suyo"). Trivia de contenido (reusa
   juegoTriviaTexto) sobre el proceso: Revolución de Mayo (1810), la bandera de
   Belgrano (1812), la Declaración de la Independencia (1816, Tucumán), San Martín y
   el cruce de los Andes, Güemes en el norte, unitarios vs federales, y la
   Constitución (1853). Curado, correcto y a nivel 10 años. C4 + C3. ── */
const INDEPENDENCIA_BANCO = [
  { q: "¿Qué pasó el 25 de mayo de 1810?",
    ops: ["Se formó la Primera Junta de gobierno (la Revolución de Mayo)", "Se declaró la Independencia", "Llegó Cristóbal Colón a América"],
    m: "El 25 de mayo de 1810 se formó la Primera Junta: fue el primer gobierno patrio, la Revolución de Mayo." },
  { q: "Antes de 1810, ¿quién gobernaba en el Río de la Plata?",
    ops: ["Un virrey, que representaba al rey de España", "Un presidente elegido por el pueblo", "Los caudillos de cada provincia"],
    m: "Gobernaba el virrey en nombre del rey de España; en 1810 una junta de criollos lo reemplazó." },
  { q: "En el Cabildo Abierto del 22 de mayo de 1810 se discutió…",
    ops: ["Si el virrey debía seguir gobernando o no", "A qué país venderle el trigo", "Dónde mudar la capital"],
    m: "Los vecinos debatieron si el virrey debía seguir; se resolvió formar una junta de gobierno propia." },
  { q: "¿Quién creó la bandera argentina, en 1812?",
    ops: ["Manuel Belgrano", "José de San Martín", "Domingo Sarmiento"],
    m: "Manuel Belgrano creó la bandera en 1812, a orillas del río Paraná." },
  { q: "El 9 de julio de 1816, en Tucumán, se…",
    ops: ["Declaró la Independencia de España", "Firmó la Constitución", "Fundó Buenos Aires"],
    m: "El 9 de julio de 1816 el Congreso de Tucumán declaró la Independencia: dejamos de depender de España." },
  { q: "¿Por qué fue importante declarar la Independencia?",
    ops: ["Para gobernarnos solos, sin depender del rey de España", "Para volver a ser una colonia", "Para elegir un rey español"],
    m: "Declarar la independencia significó decidir nuestro propio destino, sin depender de España." },
  { q: "¿Qué hizo San Martín para liberar a Chile y a Perú?",
    ops: ["Cruzó la cordillera de los Andes con su ejército", "Construyó barcos en Buenos Aires", "Se quedó gobernando en Tucumán"],
    m: "San Martín cruzó los Andes con el Ejército de los Andes y liberó primero Chile y después Perú." },
  { q: "El Ejército de los Andes cruzó…",
    ops: ["La cordillera de los Andes", "El océano Atlántico", "El desierto del Sahara"],
    m: "Cruzó la altísima cordillera de los Andes: una hazaña enorme por el frío y la altura." },
  { q: "Mientras San Martín cruzaba los Andes, ¿quién defendía el norte con sus gauchos?",
    ops: ["Martín Miguel de Güemes", "Cristóbal Colón", "Juan de Garay"],
    m: "Güemes y sus gauchos frenaron a los españoles en el norte (Salta), protegiendo la retaguardia." },
  { q: "Después de la independencia, hubo muchos años de…",
    ops: ["Peleas internas entre las provincias (unitarios y federales)", "Paz total y acuerdo entre todos", "Gobierno de un rey"],
    m: "Las provincias no se ponían de acuerdo en cómo organizar el país: unitarios contra federales." },
  { q: "Los UNITARIOS querían que…",
    ops: ["Buenos Aires tuviera un gobierno central fuerte sobre todo el país", "Cada provincia se gobernara sola", "Volviera el rey de España"],
    m: "Los unitarios querían un gobierno central fuerte en Buenos Aires que mandara sobre las provincias." },
  { q: "Los FEDERALES querían que…",
    ops: ["Cada provincia se gobernara a sí misma", "Mandara solamente Buenos Aires", "Gobernara un virrey otra vez"],
    m: "Los federales defendían la autonomía de cada provincia frente al poder central de Buenos Aires." },
  { q: "¿Qué se sancionó en 1853?",
    ops: ["La Constitución Nacional", "La primera bandera", "La Revolución de Mayo"],
    m: "En 1853 se sancionó la Constitución Nacional, que organizó el país con sus leyes." },
  { q: "¿Para qué sirve la Constitución?",
    ops: ["Es la ley más importante: organiza el país y protege nuestros derechos", "Es un mapa de las provincias", "Es un impuesto que se paga"],
    m: "La Constitución es la ley principal: dice cómo se gobierna el país y cuáles son nuestros derechos." },
  { q: "¿Qué pasó PRIMERO?",
    ops: ["La Revolución de Mayo (1810)", "La Declaración de la Independencia (1816)", "La Constitución Nacional (1853)"],
    m: "El orden fue: 1810 la Revolución de Mayo, 1816 la Independencia y 1853 la Constitución." },
];
GAMES.independencia_arg = juegoTriviaTexto(INDEPENDENCIA_BANCO, "Elegí la respuesta correcta.", "independencia");

/* ── ¿CÓMO SE ESCRIBE? — 2° grado (docs/auditoria-dc-caba/grado-2.md, gap #1: los
   dígrafos y las opacidades ortográficas son "el contenido insignia de 2°,
   trivialmente gamificable, ausente por completo"). Elegir la palabra bien escrita,
   con una pista visual: dígrafos (ll/ch/qu/gu/rr), b/v, mb/nv, s/c/z y la separación
   entre palabras (el error de escritura más frecuente del grado). Distractores = los
   errores típicos (C4) + explicación de la regla (C3). Reusa juegoTriviaTexto. ── */
const ORTO2_BANCO = [
  { q: "🐴 El animal que relincha:", ops: ["caballo", "cabayo", "cavallo"], m: "Va con LL y con B: caballo." },
  { q: "🧀 Lo que se hace con la leche:", ops: ["queso", "keso", "cueso"], m: "El sonido /ke/ se escribe QU: queso." },
  { q: "🎸 El instrumento de cuerdas:", ops: ["guitarra", "gitarra", "guitara"], m: "Va con GU (sonido /gi/) y con RR: guitarra." },
  { q: "☔ El agua que cae del cielo:", ops: ["lluvia", "yuvia", "luvia"], m: "Va con LL: lluvia." },
  { q: "🪑 Sirve para sentarse:", ops: ["silla", "siya", "cilla"], m: "Va con LL: silla." },
  { q: "🐔 El ave que pone huevos:", ops: ["gallina", "gayina", "galina"], m: "Va con LL: gallina." },
  { q: "🐄 El animal que da leche:", ops: ["vaca", "baca", "vaka"], m: "Va con V: vaca." },
  { q: "🚢 Navega por el agua:", ops: ["barco", "varco", "barrco"], m: "Va con B: barco." },
  { q: "🪟 Se abre para ver afuera:", ops: ["ventana", "bentana", "ventanna"], m: "Va con V: ventana." },
  { q: "⛄ La estación más fría del año:", ops: ["invierno", "inbierno", "imvierno"], m: "Se escribe NV: invierno." },
  { q: "🥁 Se toca golpeándolo:", ops: ["tambor", "tanbor", "tamvor"], m: "Antes de B va M: tambor." },
  { q: "🍫 El dulce marrón que hacen con cacao:", ops: ["chocolate", "xocolate", "chocolat"], m: "Va con CH: chocolate." },
  { q: "🎒 Lo llevás a la escuela en la espalda:", ops: ["mochila", "mochilla", "mochyla"], m: "Va con CH y una sola L: mochila." },
  { q: "🦊 El animal naranja y astuto:", ops: ["zorro", "sorro", "zoro"], m: "Va con Z y con RR: zorro." },
  { q: "🐷 El animal que dice «oink»:", ops: ["chancho", "chanco", "chansho"], m: "Va con CH: chancho." },
  { q: "👦 «___ me quiere mucho». ¿Cómo se escribe?", ops: ["mi mamá", "mimamá", "mimama"], m: "Son DOS palabras separadas: «mi mamá»." },
];
GAMES.ortografia_2do = juegoTriviaTexto(ORTO2_BANCO, "Tocá la palabra bien escrita.", "orto2");

/* ── PROPORCIONALIDAD DIRECTA E INVERSA (7° grado — docs/auditoria-dc-caba/grado-7.md,
   gap #5: "proporcionalidad directa e inversa = 0; la INVERSA es contenido nuevo y
   nodal de 7°"). Juego GENERADO, 3 modos: (1) directa (más cosas → más plata, calcular),
   (2) inversa (más obreros → menos días, calcular — el nodal nuevo), (3) clasificar
   una situación como directa o inversa. Números enteros. El distractor clave de la
   inversa es la respuesta que daría alguien que la trata como DIRECTA (multiplica en
   vez de dividir). Explicación con la cuenta (C3). ── */
const PROPORC_CLASIF = [
  { s: "Cuantos más kilos de pan comprás, más plata pagás.", c: "Directa" },
  { s: "Cuantos más obreros trabajan, menos días tarda la obra.", c: "Inversa" },
  { s: "Cuanto más rápido va el auto, menos tiempo dura el viaje.", c: "Inversa" },
  { s: "Cuantas más horas trabajás, más sueldo cobrás.", c: "Directa" },
  { s: "Cuantas más canillas abrís, menos tarda en llenarse el tanque.", c: "Inversa" },
  { s: "Cuantas más entradas comprás, más plata gastás.", c: "Directa" },
  { s: "Cuantas más personas se reparten la pizza, menos porciones toca a cada una.", c: "Inversa" },
  { s: "Cuantos más litros de nafta cargás, más pagás.", c: "Directa" },
];
GAMES.proporcionalidad = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 8;
    ctx.rondas(rondas);
    let ronda = 0;
    const gen = () => {
      const modo = ["directa", "inversa", "clasificar"][rint(0, 2)];
      if (modo === "clasificar") {
        const it = PROPORC_CLASIF[rint(0, PROPORC_CLASIF.length - 1)];
        return { q: it.s + " ¿Es proporcionalidad directa o inversa?",
                 ok: it.c, wrongs: [it.c === "Directa" ? "Inversa" : "Directa"],
                 m: it.c === "Directa"
                    ? "Es DIRECTA: si una cantidad aumenta, la otra también aumenta."
                    : "Es INVERSA: si una cantidad aumenta, la otra DISMINUYE." };
      }
      if (modo === "directa") {
        const u = [20, 25, 50, 100][rint(0, 3)], n1 = rint(2, 5), f = rint(2, 3), n2 = n1 * f, c1 = n1 * u, ans = n2 * u;
        const cosa = ["lápices", "manzanas", "cuadernos", "alfajores", "figuritas"][rint(0, 4)];
        return { q: n1 + " " + cosa + " cuestan $" + c1 + ". ¿Cuánto cuestan " + n2 + " " + cosa + "?",
                 ok: "$" + ans, wrongs: ["$" + c1, "$" + (c1 + u)],
                 m: "Es directa: cada uno sale $" + u + ", así que " + n2 + " cuestan " + n2 + " × " + u + " = $" + ans + "." };
      }
      const mult = rint(2, 3), A = rint(2, 6), B = A * mult, T = mult * rint(2, 6), ans = T / mult;
      const ctxs = [
        { who: "obreros", verb: "terminan una obra", unit: "días" },
        { who: "canillas", verb: "llenan el tanque", unit: "horas" },
        { who: "máquinas", verb: "arman el pedido", unit: "horas" },
      ][rint(0, 2)];
      return { q: A + " " + ctxs.who + " " + ctxs.verb + " en " + T + " " + ctxs.unit + ". ¿En cuánto lo hacen " + B + " " + ctxs.who + "?",
               ok: ans + " " + ctxs.unit, wrongs: [(T * mult) + " " + ctxs.unit, T + " " + ctxs.unit],
               m: "Es inversa: al haber MÁS " + ctxs.who + ", tardan MENOS. " + A + " × " + T + " = " + (A * T) + " de trabajo; " + (A * T) + " ÷ " + B + " = " + ans + " " + ctxs.unit + "." };
    };
    const jugar = () => {
      ctx.ronda(ronda);
      const it = gen();
      ctx.item("proporc#" + ronda);
      ctx.consigna("Elegí la respuesta correcta.");
      ctx.juego.innerHTML = "";
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:20px;font-family:'Baloo',sans-serif">${it.q}</span>`));
      ctx.juego.appendChild(arriba);
      const ops = [{ v: it.ok, ok: true }];
      it.wrongs.forEach((v) => { if (!ops.some((o) => o.v === v)) ops.push({ v: v }); });
      const fila = el("div", "opsTexto");
      fila.setAttribute("data-ok", it.ok);
      let resuelto = false;
      shuffle(ops).forEach((o) => {
        const b = el("button", "op-texto", o.v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) {
            resuelto = true; b.classList.add("bien", "anim-pop"); ctx.bien();
            ronda++; await espera(900); if (ronda >= rondas) ctx.win(); else jugar();
          } else { b.classList.add("casi"); ctx.casi(it.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── CRECER Y CAMBIAR — LA PUBERTAD (6° grado — docs/auditoria-dc-caba/grado-6.md,
   gap #4: "reproducción humana / pubertad (Naturales + ESI) = 0", área troncal
   ausente mientras se sirve contenido de 7°). Contenido escolar de Naturales/ESI de
   6°, tratado de forma FACTUAL y respetuosa: los cambios de la pubertad (físicos y
   emocionales, a distinto ritmo en cada persona), la higiene, la reproducción humana
   en términos básicos (óvulo/espermatozoide/útero) y el eje ESI de cuidado del
   propio cuerpo (tu cuerpo es tuyo; ante dudas, un adulto de confianza). Distractores
   por misconception (C4) + explicación (C3). ── */
const PUBERTAD_BANCO = [
  { q: "¿Qué es la pubertad?",
    ops: ["La etapa en que el cuerpo cambia de a poco, de niño/a a adulto/a", "Una enfermedad que hay que curar", "Algo que pasa en un solo día"],
    m: "La pubertad es la etapa natural en que el cuerpo va cambiando, de niño/a hacia adulto/a." },
  { q: "¿Todas las personas empiezan la pubertad a la misma edad?",
    ops: ["No, cada cuerpo tiene su propio ritmo", "Sí, todos el mismo día", "Solo los varones tienen pubertad"],
    m: "Cada persona empieza a una edad distinta: todos los ritmos son normales." },
  { q: "Durante la pubertad, es normal que…",
    ops: ["El cuerpo crezca más rápido y vaya cambiando", "No cambie nada nunca", "El cuerpo se achique"],
    m: "En la pubertad el cuerpo pega un «estirón» y cambia: es lo esperable." },
  { q: "Además de lo físico, en la pubertad también pueden cambiar…",
    ops: ["Las emociones y el humor", "El color de los ojos para siempre", "La cantidad de dedos"],
    m: "Es normal tener cambios de humor y nuevos intereses: también es parte de crecer." },
  { q: "Como en la pubertad se transpira más, es importante…",
    ops: ["Bañarse seguido y cuidar la higiene", "No lavarse nunca", "Taparse la nariz"],
    m: "Con más transpiración, la higiene diaria (bañarse, desodorante) ayuda a sentirse bien." },
  { q: "Al crecer, el cuerpo de la mujer empieza a producir…",
    ops: ["Óvulos", "Semillas", "Plumas"],
    m: "En la pubertad, el cuerpo de la mujer empieza a producir óvulos." },
  { q: "Al crecer, el cuerpo del varón empieza a producir…",
    ops: ["Espermatozoides", "Óvulos", "Hojas"],
    m: "El cuerpo del varón empieza a producir espermatozoides." },
  { q: "Para que se forme un bebé, se tienen que unir…",
    ops: ["Un óvulo y un espermatozoide", "Dos óvulos", "Dos semillas"],
    m: "Cuando se unen un óvulo y un espermatozoide, puede empezar a formarse un bebé." },
  { q: "Antes de nacer, el bebé crece durante unos 9 meses en…",
    ops: ["El útero de la mamá", "El estómago", "Un huevo"],
    m: "El bebé se desarrolla en el útero de la mamá durante unos 9 meses." },
  { q: "Si un compañero pasa por cambios distintos a los tuyos…",
    ops: ["Es normal: cada uno tiene su ritmo, hay que respetarlo", "Hay que burlarse", "Algo anda mal con él"],
    m: "Cada cuerpo cambia a su tiempo. Lo que corresponde es el respeto, no la burla." },
  { q: "Tu cuerpo es tuyo, así que…",
    ops: ["Nadie puede tocarte sin tu permiso", "Cualquiera puede hacer lo que quiera", "No importa lo que sientas"],
    m: "Tu cuerpo es tuyo y nadie puede tocarte sin tu permiso. Si algo te incomoda, contale a un adulto de confianza." },
  { q: "Si tenés dudas sobre los cambios de tu cuerpo, lo mejor es…",
    ops: ["Preguntarle a un adulto de confianza (familia, docente, médico/a)", "No preguntar nunca", "Creer cualquier cosa que diga internet"],
    m: "Ante las dudas, lo mejor es preguntar a un adulto de confianza o a un/a profesional de la salud." },
  { q: "Los cambios de la pubertad son…",
    ops: ["Una parte natural de crecer, le pasa a todo el mundo", "Algo de lo que avergonzarse", "Un castigo"],
    m: "Crecer y cambiar es natural: le pasa a todas las personas." },
  { q: "En los varones, durante la pubertad, es común que…",
    ops: ["La voz se vuelva más grave", "Desaparezca la voz", "Les crezcan alas"],
    m: "En la pubertad, la voz de los varones suele volverse más grave." },
];
GAMES.pubertad = juegoTriviaTexto(PUBERTAD_BANCO, "Elegí la respuesta correcta.", "pubertad");

/* ── LA SUMA DE LOS ÁNGULOS (6° grado — docs/auditoria-dc-caba/grado-6.md, gap #5:
   geometría de 6° "360°, suma de ángulos interiores" ausente, enmascarada por
   poligonos_lados que es de 3°-4°). Complementa el transportador (medir) y
   cuadrilateros con la propiedad nodal: los ángulos de un triángulo suman 180° y los
   de un cuadrilátero 360°. 3 modos GENERADOS: concepto (¿cuánto suman?), triángulo
   faltante (dados 2, hallar el 3°) y cuadrilátero faltante (dados 3, hallar el 4°).
   Ángulos enteros. Distractores por misconception (C4: sumar los dados en vez de
   restar del total, confundir 180 con 360) + explicación con la cuenta (C3). ── */
GAMES.suma_angulos = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 8;
    ctx.rondas(rondas);
    let ronda = 0;
    const deg = (n) => n + "°";
    const gen = () => {
      const modo = ["tri", "cuad", "concepto"][rint(0, 2)];
      if (modo === "concepto") {
        const tri = rint(0, 1) === 0, s = tri ? 180 : 360, o = tri ? 360 : 180;
        const fig = tri ? "un triángulo" : "un cuadrilátero";
        return { q: "¿Cuánto suman TODOS los ángulos de " + fig + "?", ok: deg(s), wrongs: [deg(o), "90°"],
                 m: "Los ángulos de " + fig + " siempre suman " + s + "°." };
      }
      if (modo === "tri") {
        const a = rint(35, 95), b = rint(35, 150 - a), c = 180 - a - b;
        return { q: "Dos ángulos de un triángulo miden " + a + "° y " + b + "°. ¿Cuánto mide el tercero?",
                 ok: deg(c), wrongs: [deg(a + b), deg(180 - a)],
                 m: "Los ángulos de un triángulo suman 180°: 180 − " + a + " − " + b + " = " + c + "°." };
      }
      let a = rint(60, 110), b = rint(60, 110), c = rint(60, 110), d = 360 - a - b - c, g = 0;
      while ((d < 40 || d > 160) && g++ < 40) { a = rint(60, 110); b = rint(60, 110); c = rint(60, 110); d = 360 - a - b - c; }
      return { q: "Tres ángulos de un cuadrilátero miden " + a + "°, " + b + "° y " + c + "°. ¿Cuánto mide el cuarto?",
               ok: deg(d), wrongs: [deg(a + b + c), deg(360 - a - b)],
               m: "Los ángulos de un cuadrilátero suman 360°: 360 − " + a + " − " + b + " − " + c + " = " + d + "°." };
    };
    const jugar = () => {
      ctx.ronda(ronda);
      const it = gen();
      ctx.item("angsuma#" + ronda);
      ctx.consigna("Elegí la respuesta correcta.");
      ctx.juego.innerHTML = "";
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:21px;font-family:'Baloo',sans-serif">${it.q}</span>`));
      ctx.juego.appendChild(arriba);
      const ops = [{ v: it.ok, ok: true }];
      const add = (v) => { if (ops.length < 3 && !ops.some((o) => o.v === v)) ops.push({ v: v }); };
      it.wrongs.forEach(add);
      let guard = 0;
      while (ops.length < 3 && guard++ < 40) add(deg(rint(2, 17) * 10));
      const fila = el("div", "opsTexto");
      fila.setAttribute("data-ok", it.ok);
      let resuelto = false;
      shuffle(ops).forEach((o) => {
        const b = el("button", "op-texto", o.v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) {
            resuelto = true; b.classList.add("bien", "anim-pop"); ctx.bien();
            ronda++; await espera(900); if (ronda >= rondas) ctx.win(); else jugar();
          } else { b.classList.add("casi"); ctx.casi(it.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿SEGURO, POSIBLE O IMPOSIBLE? (6° grado — docs/auditoria-dc-caba/grado-6.md,
   gap #3: "probabilidad y estadística... sucesos posibles/imposibles/seguros",
   contenido que el DC hace nodal POR PRIMERA VEZ en 6°). El árbol de probabilidad
   cubre el CONTEO de resultados; esto cubre el lenguaje cualitativo de la
   probabilidad: clasificar un suceso como seguro (pasa siempre), posible (puede
   pasar o no) o imposible (no pasa nunca). Banco curado con contextos claros (dado,
   bolsa de bolitas, moneda, hechos cotidianos). Capa 0 C3: el error explica por qué
   es de esa categoría. ── */
const SUCESOS_BANCO = [
  { e: "Tirás un dado y sale un número del 1 al 6", c: "seguro", m: "El dado SIEMPRE cae en un número del 1 al 6: es seguro." },
  { e: "Tirás un dado y sale un 7", c: "imposible", m: "El dado no tiene el 7: sacar un 7 es imposible." },
  { e: "Tirás un dado y sale un número par", c: "posible", m: "Puede salir par (2, 4, 6) o impar (1, 3, 5): es posible, no seguro." },
  { e: "Tirás un dado y sale un número menor que 10", c: "seguro", m: "Todos los números del dado (1 al 6) son menores que 10: es seguro." },
  { e: "Sacás una bolita de una bolsa que tiene SOLO bolitas rojas, y sale roja", c: "seguro", m: "Si todas son rojas, sacar roja es seguro." },
  { e: "Sacás una bolita azul de una bolsa que tiene solo bolitas rojas", c: "imposible", m: "No hay bolitas azules en la bolsa: es imposible." },
  { e: "Sacás una bolita roja de una bolsa con bolitas rojas y verdes", c: "posible", m: "Puede salir roja o verde: es posible." },
  { e: "Tirás una moneda y sale cara", c: "posible", m: "Puede salir cara o cruz: es posible (tenés la mitad de chances)." },
  { e: "Mañana a la mañana sale el sol", c: "seguro", m: "El sol sale todos los días: es seguro." },
  { e: "Un gato pone un huevo", c: "imposible", m: "Los gatos no ponen huevos: es imposible." },
  { e: "Mañana llueve en tu ciudad", c: "posible", m: "Puede llover o no: es posible, depende del clima." },
  { e: "Dos más dos es igual a cinco", c: "imposible", m: "2 + 2 siempre da 4: que dé 5 es imposible." },
  { e: "Una persona vive 500 años", c: "imposible", m: "Nadie vive 500 años: es imposible." },
  { e: "El próximo mes tiene por lo menos un día lunes", c: "seguro", m: "Todos los meses tienen varios lunes: es seguro." },
  { e: "Sacás un caramelo de menta de una bolsa con caramelos de menta y de frutilla", c: "posible", m: "Puede salir de menta o de frutilla: es posible." },
  { e: "Un número par termina en 0, 2, 4, 6 u 8", c: "seguro", m: "Todo número par termina en 0, 2, 4, 6 u 8: es seguro." },
];
GAMES.probabilidad_sucesos = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const LBL = { seguro: "✅ Seguro", posible: "🤔 Posible", imposible: "🚫 Imposible" };
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.consigna("¿Es seguro, posible o imposible?");
      ctx.juego.innerHTML = "";
      let libres = SUCESOS_BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!libres.length) { usados = []; libres = SUCESOS_BANCO.map((_, i) => i); }
      const idx = libres[rint(0, libres.length - 1)]; usados.push(idx);
      const it = SUCESOS_BANCO[idx]; ctx.item("suceso#" + idx);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:21px;font-family:'Baloo',sans-serif">${it.e}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      fila.setAttribute("data-c", it.c);
      let resuelto = false;
      shuffle(["seguro", "posible", "imposible"]).forEach((cat) => {
        const b = el("button", "spriteBtn", `<span style="font-size:18px;font-family:'Baloo',sans-serif">${LBL[cat]}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (cat === it.c) {
            resuelto = true; b.classList.add("anim-brinco"); ctx.bien();
            ronda++; await espera(900);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else {
            b.style.animation = "sacudir .4s ease"; setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi(it.m);
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
      const nota = el("div", "tonica-nota",
        "Seguro = pasa siempre · Posible = puede pasar o no · Imposible = no pasa nunca");
      ctx.juego.appendChild(el("div", "tablero")).appendChild(nota);
    };
    jugar();
  },
};

/* ── LA MEJOR OFERTA (M12, 4° grado — docs/auditoria-dc-caba/grado-4.md, gap #5:
   proporcionalidad directa + Educación Financiera). 3 modos GENERADOS: (1) valor
   unitario (N cuestan $T → 1 cuesta T÷N), (2) doble/triple (1 cuesta $U → K cuestan
   U×K), (3) mejor oferta (dos precios por cantidades distintas → cuál conviene por
   unidad, incluso cuando el más barato tiene mayor total). Precios redondos.
   Distractores por misconception (C4: sumar en vez de multiplicar, no dividir,
   mirar el total en vez del precio unitario) + explicación del porqué (C3). ── */
const OFERTA_COSAS = [
  { s: "alfajor", p: "alfajores" }, { s: "figurita", p: "figuritas" }, { s: "manzana", p: "manzanas" },
  { s: "lápiz", p: "lápices" }, { s: "chupetín", p: "chupetines" }, { s: "empanada", p: "empanadas" },
  { s: "sticker", p: "stickers" }, { s: "globo", p: "globos" },
];
GAMES.mejor_oferta = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 8;
    ctx.rondas(rondas);
    let ronda = 0;
    const U_SET = [50, 100, 150, 200, 250, 300];
    const money = (n) => "$" + n;
    const genItem = () => {
      const cosa = OFERTA_COSAS[rint(0, OFERTA_COSAS.length - 1)];
      const modo = ["unitario", "varios", "oferta"][rint(0, 2)];
      if (modo === "unitario") {
        const N = rint(2, 5), U = U_SET[rint(0, U_SET.length - 1)], T = N * U;
        return { q: `${N} ${cosa.p} cuestan ${money(T)}. ¿Cuánto cuesta 1?`,
                 ops: [money(U), money(T), money(N * T)],
                 m: `Si ${N} cuestan ${money(T)}, dividís: ${T} ÷ ${N} = ${U}. Cada uno sale ${money(U)}.` };
      }
      if (modo === "varios") {
        const U = U_SET[rint(0, U_SET.length - 1)], K = rint(2, 4);
        return { q: `1 ${cosa.s} cuesta ${money(U)}. ¿Cuánto cuestan ${K}?`,
                 ops: [money(U * K), money(U + K), money(U * (K + 1))],
                 m: `Si 1 cuesta ${money(U)}, ${K} cuestan ${U} × ${K} = ${U * K} (se multiplica, no se suma).` };
      }
      const UU = [150, 180, 200, 250];
      const uA = UU[rint(0, UU.length - 1)]; let uB = uA;
      while (uB === uA) uB = UU[rint(0, UU.length - 1)];
      const nA = rint(2, 5), nB = rint(2, 5);
      const A = `${nA} por ${money(uA * nA)}`, B = `${nB} por ${money(uB * nB)}`;
      const barato = uA < uB ? A : B, caro = uA < uB ? B : A;
      return { q: `¿Qué oferta de ${cosa.p} conviene MÁS?`,
               ops: [barato, caro, "Las dos cuestan lo mismo"],
               m: `Fijate el precio de CADA uno: ${A} = ${money(uA)} c/u y ${B} = ${money(uB)} c/u. Conviene el más barato por unidad.` };
    };
    const jugar = () => {
      ctx.ronda(ronda);
      const item = genItem();
      ctx.item("oferta#" + ronda);
      ctx.consigna("Leé el problema y elegí la respuesta.");
      ctx.juego.innerHTML = "";
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:21px;font-family:'Baloo',sans-serif">${item.q}</span>`));
      ctx.juego.appendChild(arriba);
      const correcta = item.ops[0];
      const fila = el("div", "opsTexto");
      fila.setAttribute("data-ok", correcta);
      let resuelto = false;
      shuffle(item.ops).forEach((op) => {
        const b = el("button", "op-texto", op);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op === correcta) {
            resuelto = true; b.classList.add("bien", "anim-pop"); ctx.bien();
            ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar();
          } else {
            b.classList.add("casi"); ctx.casi(item.m);
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── MECÁNICA NUEVA: RECTA NUMÉRICA (M1 "Recta gigante", 4° grado) — 19-jul-2026,
   otra mecánica que el motor no tenía (docs/auditoria-dc-caba/). Ubicar un número
   en la recta: la recta se parte en 10 zonas y el chico toca la zona donde cae el
   número (proporcionalidad/orden de magnitud). Rangos 0-10.000 → 0-100.000.
   Explicación por error apuntando al tramo correcto (Capa 0 · C3). ── */
GAMES.recta_numerica = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    const fmt = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const prog = rondas > 1 ? ronda / (rondas - 1) : 1;
      const max = prog > 0.5 ? (ctx.cfg.max2 || 100000) : (ctx.cfg.max1 || 10000);
      const paso = max / 10;
      const g100 = Math.max(1, Math.round(max / 100));       // paso "redondo" que escala con el rango
      const target = rint(1, Math.floor(max / g100) - 1) * g100;   // en (0, max); entero también si max<100 (1°/2°)
      const zonaOK = Math.min(9, Math.floor(target / paso));
      ctx.item("recta#" + max + "_" + target);
      ctx.consigna("¿Dónde está el " + fmt(target) + "?  (de 0 a " + fmt(max) + ")");
      ctx.juego.innerHTML = "";
      const wrap = el("div", ""); wrap.style.cssText = "max-width:600px;margin:0 auto;width:100%";
      const linea = el("div", ""); linea.style.cssText = "display:flex;gap:3px;width:100%";
      let resuelto = false;
      for (let i = 0; i < 10; i++) {
        const z = el("button", "rectaZona");
        z.style.cssText = "flex:1;height:48px;border:2px solid #8a8a99;background:rgba(140,140,160,.14);cursor:pointer;border-radius:7px";
        z.addEventListener("click", () => {
          if (resuelto) return;
          if (i === zonaOK) {
            resuelto = true; z.style.background = "#7bd88f"; ctx.bien();
            ronda++;
            setTimeout(() => { if (ronda >= rondas) ctx.win(); else jugar(); }, 1000);
          } else {
            z.style.background = "#e08a8a"; setTimeout(() => { z.style.background = "rgba(140,140,160,.14)"; }, 450);
            ctx.casi("El " + fmt(target) + " está entre " + fmt(zonaOK * paso) + " y " + fmt((zonaOK + 1) * paso) + ". ¿Está más cerca del 0 o del " + fmt(max) + "?");
          }
        });
        linea.appendChild(z);
      }
      wrap.appendChild(linea);
      const labels = el("div", ""); labels.style.cssText = "display:flex;justify-content:space-between;margin-top:6px;font-weight:700";
      labels.appendChild(el("span", "", "0"));
      labels.appendChild(el("span", "", fmt(max / 2)));
      labels.appendChild(el("span", "", fmt(max)));
      wrap.appendChild(labels);
      ctx.juego.appendChild(el("div", "tablero")).appendChild(wrap);
    };
    jugar();
  },
};

/* ── MECÁNICA NUEVA: COMPRENSIÓN LECTORA (L9/L17 "Detective de textos", 4° grado)
   — 19-jul-2026, mecánica que el motor no tenía (docs/auditoria-dc-caba/): mostrar
   un texto y hacer preguntas, incluidas las INFERENCIALES (la respuesta no está
   literal, se deduce de pistas). El texto queda a la vista; la consigna (pregunta)
   se lee en voz alta; el chico lee el texto. Explicación que remite al texto
   (Capa 0 · C3). ── */
const COMPRENSION_BANCO = [
  {
    texto: "Martín guardó la bici en el garaje y entró corriendo a la casa. Tenía las zapatillas llenas de barro y el pelo mojado. «No te olvides de secarte», le dijo la mamá desde la cocina.",
    preguntas: [
      { q: "¿Dónde guardó Martín la bici?", ops: ["En el garaje", "En la cocina", "En su cuarto"], ok: 0, m: "El texto lo dice: guardó la bici en el garaje." },
      { q: "¿Qué tiempo hacía afuera?", ops: ["Estaba lloviendo", "Había mucho sol", "Estaba nevando"], ok: 0, m: "No lo dice directo, pero el pelo mojado y el barro son pistas de que llovía." },
    ],
  },
  {
    texto: "Lucía abrió la heladera y no encontró nada para el desayuno. Suspiró, agarró unas monedas del frasco y salió a la panadería de la esquina. Volvió con el pan calentito.",
    preguntas: [
      { q: "¿A dónde fue Lucía?", ops: ["A la panadería", "A la escuela", "A la casa de una amiga"], ok: 0, m: "El texto dice que salió a la panadería de la esquina." },
      { q: "¿Por qué salió a comprar?", ops: ["No había nada para desayunar", "Quería pasear", "La mandó la mamá"], ok: 0, m: "Se deduce: abrió la heladera y no encontró nada para el desayuno." },
    ],
  },
  {
    texto: "El equipo de Joaquín perdió el partido por un gol. En el vestuario nadie hablaba y algunos tenían los ojos llorosos. El técnico les dijo: «La próxima ganamos».",
    preguntas: [
      { q: "¿Por cuánto perdieron?", ops: ["Por un gol", "Por tres goles", "Empataron"], ok: 0, m: "El texto dice que perdieron por un gol." },
      { q: "¿Cómo se sentían los jugadores?", ops: ["Tristes", "Contentos", "Aburridos"], ok: 0, m: "No lo dice con esa palabra, pero nadie hablaba y tenían los ojos llorosos: estaban tristes." },
    ],
  },
  {
    texto: "Cuando sonó el timbre, todos los chicos guardaron los cuadernos y salieron corriendo al patio. Ana se quedó ordenando sus lápices con calma antes de salir.",
    preguntas: [
      { q: "¿Qué hicieron los chicos cuando sonó el timbre?", ops: ["Salieron corriendo al patio", "Siguieron escribiendo", "Se fueron a casa"], ok: 0, m: "El texto lo dice: guardaron los cuadernos y salieron corriendo al patio." },
      { q: "¿Cómo es Ana comparada con los demás?", ops: ["Más tranquila y ordenada", "La más apurada", "La más ruidosa"], ok: 0, m: "Mientras todos corrían, Ana ordenaba sus lápices con calma: es más tranquila." },
    ],
  },
];
// ===== BANCOS DE COMPRENSIÓN POR GRADO (3°→7°) — escalados en longitud y
// dificultad; ver comprensionBanco() abajo. COMPRENSION_BANCO (arriba) quedó
// como el set corto original (fallback histórico). =====
/* COMPRENSION_2 (2° grado — docs/auditoria-dc-caba/grado-2.md gap #3: "en el grado
   cuyo objetivo es consolidar la lectura, no hay nada para leer más largo que una
   palabra"). Textos CORTOS (2-3 oraciones simples) con preguntas literales + una
   inferencia sencilla, a nivel de un chico de 7 años que recién afianza la lectura. */
const COMPRENSION_2 = [
  { texto: "Sofía tiene un gato blanco que se llama Nube. A Nube le gusta dormir arriba de la heladera, porque ahí está calentito. Todas las noches, Sofía le da leche antes de ir a dormir.", preguntas: [
    { q: "¿Cómo se llama el gato de Sofía?", ops: ["Nube", "Sofía", "Leche"], ok: 0, m: "El texto dice: «un gato blanco que se llama Nube»." },
    { q: "¿Por qué a Nube le gusta dormir arriba de la heladera?", ops: ["Porque ahí está calentito", "Porque hay leche", "Porque es blando"], ok: 0, m: "El texto dice que duerme ahí «porque ahí está calentito»." } ] },
  { texto: "En el patio de la escuela hay un árbol muy grande. En primavera se llena de flores rosas. Los chicos juegan a su sombra cuando hace mucho calor.", preguntas: [
    { q: "¿De qué color son las flores del árbol?", ops: ["Rosas", "Rojas", "Blancas"], ok: 0, m: "El texto dice: «se llena de flores rosas»." },
    { q: "¿Por qué los chicos juegan debajo del árbol cuando hace calor?", ops: ["Por la sombra", "Por las flores", "Por los frutos"], ok: 0, m: "El árbol da sombra, y a la sombra hace menos calor." } ] },
  { texto: "Juan perdió un diente comiendo una manzana. Se asustó un poco, pero su mamá le dijo que era normal. Esa noche puso el diente abajo de la almohada.", preguntas: [
    { q: "¿Cómo perdió el diente Juan?", ops: ["Comiendo una manzana", "Jugando al fútbol", "Cepillándose"], ok: 0, m: "El texto dice: «perdió un diente comiendo una manzana»." },
    { q: "¿Dónde puso el diente esa noche?", ops: ["Abajo de la almohada", "En un vaso", "En el bolsillo"], ok: 0, m: "El texto dice: «puso el diente abajo de la almohada»." } ] },
  { texto: "La tortuga de Martina se llama Lenta. Camina muy despacio por el jardín y come hojas de lechuga. Cuando tiene miedo, esconde la cabeza adentro del caparazón.", preguntas: [
    { q: "¿Qué come la tortuga Lenta?", ops: ["Hojas de lechuga", "Manzanas", "Pan"], ok: 0, m: "El texto dice: «come hojas de lechuga»." },
    { q: "¿Qué hace la tortuga cuando tiene miedo?", ops: ["Esconde la cabeza en el caparazón", "Corre rápido", "Grita"], ok: 0, m: "El texto dice que «esconde la cabeza adentro del caparazón»." } ] },
  { texto: "Hoy llueve mucho. Lucía no puede salir a la plaza, así que arma un fuerte con las sillas y una manta. Adentro lee cuentos con una linterna.", preguntas: [
    { q: "¿Por qué Lucía no sale a la plaza?", ops: ["Porque llueve mucho", "Porque es de noche", "Porque está enferma"], ok: 0, m: "El texto empieza: «Hoy llueve mucho. Lucía no puede salir»." },
    { q: "¿Con qué armó el fuerte?", ops: ["Con sillas y una manta", "Con cajas", "Con almohadas"], ok: 0, m: "El texto dice: «arma un fuerte con las sillas y una manta»." } ] },
  { texto: "Pedro fue a la panadería con su abuelo. Compraron pan, facturas y un pan dulce. En el camino de vuelta, Pedro llevó la bolsa con mucho cuidado.", preguntas: [
    { q: "¿Con quién fue Pedro a la panadería?", ops: ["Con su abuelo", "Con su hermana", "Solo"], ok: 0, m: "El texto dice: «fue a la panadería con su abuelo»." },
    { q: "¿Por qué Pedro llevó la bolsa con cuidado?", ops: ["Para que no se aplaste lo que compraron", "Porque pesaba mucho", "Porque estaba rota"], ok: 0, m: "Llevaba pan y facturas: por eso la cuidaba para no aplastarlas." } ] },
  { texto: "Mía plantó una semilla en una maceta. Todos los días la riega y la pone al sol. Después de dos semanas, salió una plantita verde.", preguntas: [
    { q: "¿Qué hace Mía todos los días con la semilla?", ops: ["La riega y la pone al sol", "La guarda en un cajón", "La cambia de maceta"], ok: 0, m: "El texto dice: «Todos los días la riega y la pone al sol»." },
    { q: "¿Qué salió después de dos semanas?", ops: ["Una plantita verde", "Una flor roja", "Nada"], ok: 0, m: "El texto dice: «salió una plantita verde»." } ] },
  { texto: "El perro de Ana se llama Tito. A Tito le encanta correr atrás de la pelota. Cuando Ana llega de la escuela, Tito mueve la cola de contento.", preguntas: [
    { q: "¿Qué le encanta hacer a Tito?", ops: ["Correr atrás de la pelota", "Dormir todo el día", "Comer lechuga"], ok: 0, m: "El texto dice: «le encanta correr atrás de la pelota»." },
    { q: "¿Cómo se da cuenta Ana de que Tito está contento?", ops: ["Porque mueve la cola", "Porque ladra fuerte", "Porque se esconde"], ok: 0, m: "El texto dice que «mueve la cola de contento»." } ] },
  { texto: "En el zoológico, Bruno vio una jirafa altísima. La jirafa comía hojas de la parte más alta de un árbol. Bruno sacó una foto para mostrarle a su hermana.", preguntas: [
    { q: "¿Qué comía la jirafa?", ops: ["Hojas de la parte más alta del árbol", "Pasto del suelo", "Frutas"], ok: 0, m: "El texto dice: «comía hojas de la parte más alta de un árbol»." },
    { q: "¿Para qué sacó Bruno una foto?", ops: ["Para mostrársela a su hermana", "Para venderla", "Para la escuela"], ok: 0, m: "El texto dice: «sacó una foto para mostrarle a su hermana»." } ] },
  { texto: "Cami se cayó de la bici y se raspó la rodilla. Su papá le puso una curita y un beso. En un ratito, Cami ya estaba jugando de nuevo.", preguntas: [
    { q: "¿Qué se raspó Cami?", ops: ["La rodilla", "El codo", "La mano"], ok: 0, m: "El texto dice: «se raspó la rodilla»." },
    { q: "¿Qué le puso el papá en la rodilla?", ops: ["Una curita", "Una venda gigante", "Hielo"], ok: 0, m: "El texto dice: «le puso una curita y un beso»." } ] },
];
const COMPRENSION_3 = [
  {
    texto: "Todas las mañanas, Tomás toma el colectivo 60 para ir a la escuela. Se sienta al lado de la ventanilla porque le gusta mirar los árboles de la avenida. Un día se quedó dormido y casi se pasa de parada, pero el señor de al lado lo despertó a tiempo. Desde entonces, Tomás lleva un despertador chiquito en la mochila.",
    preguntas: [
      { q: "¿Qué colectivo toma Tomás para ir a la escuela?", ops: ["El 60", "El 12", "El 152"], ok: 0, m: "El texto dice: «toma el colectivo 60 para ir a la escuela»." },
      { q: "¿Por qué ahora Tomás lleva un despertador en la mochila?", ops: ["Para no quedarse dormido y pasarse de parada", "Porque le gusta saber la hora", "Porque el señor se lo regaló"], ok: 0, m: "Casi se pasa de parada por quedarse dormido, así que el despertador lo ayuda a no dormirse en el viaje." }
    ]
  },
  {
    texto: "El hornero es un pájaro muy conocido en el campo argentino. Con barro y pajitas construye un nido con forma de horno, bien firme, que aguanta la lluvia y el viento. Trabaja en pareja durante varios días. Cuando termina, el nido queda tan resistente que otros pájaros lo usan después de que el hornero se muda.",
    preguntas: [
      { q: "¿Con qué materiales construye su nido el hornero?", ops: ["Con barro y pajitas", "Con hojas y piedras", "Con plumas y ramas gruesas"], ok: 0, m: "El texto dice: «Con barro y pajitas construye un nido con forma de horno»." },
      { q: "¿Por qué otros pájaros pueden usar el nido más tarde?", ops: ["Porque queda muy resistente y el hornero se muda", "Porque el hornero los invita a vivir con él", "Porque el nido es blando y cómodo"], ok: 0, m: "El nido queda tan resistente y el hornero se muda, por eso otros pájaros lo aprovechan." }
    ]
  },
  {
    texto: "Martina encontró una llave dorada debajo de un ladrillo del patio. No sabía qué puerta abría. La probó en el portón, en el ropero y hasta en la casita del perro, pero ninguna cerradura le servía. Esa noche soñó que la llave abría un cofre lleno de caramelos. A la mañana siguiente se la mostró a su abuela, que sonrió y le dijo que era la llave de un viejo reloj.",
    preguntas: [
      { q: "¿Dónde encontró Martina la llave?", ops: ["Debajo de un ladrillo del patio", "Dentro del ropero", "En la casita del perro"], ok: 0, m: "El texto dice: «encontró una llave dorada debajo de un ladrillo del patio». En el ropero solo la probó." },
      { q: "¿Para qué servía realmente la llave?", ops: ["Para abrir un viejo reloj", "Para abrir un cofre de caramelos", "Para abrir el portón"], ok: 0, m: "La abuela le dijo que «era la llave de un viejo reloj»; lo del cofre de caramelos fue solo un sueño." }
    ]
  },
  {
    texto: "El arcoíris aparece cuando el sol sale después de la lluvia. La luz del sol atraviesa las gotitas de agua que quedan en el aire y se separa en muchos colores. Por eso siempre vemos el arcoíris del lado contrario al sol. Si mirás hacia donde está el sol, no vas a encontrarlo nunca.",
    preguntas: [
      { q: "¿Cuándo aparece el arcoíris?", ops: ["Cuando el sol sale después de la lluvia", "Cuando hay mucho viento", "Cuando es de noche"], ok: 0, m: "El texto dice: «aparece cuando el sol sale después de la lluvia»." },
      { q: "Si querés ver un arcoíris, ¿hacia dónde te conviene mirar?", ops: ["Hacia el lado contrario al sol", "Directo hacia el sol", "Hacia el piso"], ok: 0, m: "El texto dice que «siempre vemos el arcoíris del lado contrario al sol»." }
    ]
  },
  {
    texto: "Hace muchos años, cuando todavía no había electricidad en las casas, la gente usaba faroles a vela para caminar de noche. Un señor llamado el farolero recorría las calles cada tarde y encendía uno por uno los faroles de la ciudad. Al amanecer volvía a pasar para apagarlos. Cuando llegó la luz eléctrica, ese oficio fue desapareciendo.",
    preguntas: [
      { q: "¿Qué hacía el farolero cada tarde?", ops: ["Encendía los faroles de la ciudad", "Apagaba las velas de las casas", "Vendía velas en la calle"], ok: 0, m: "El texto dice que el farolero «encendía uno por uno los faroles de la ciudad»." },
      { q: "¿Por qué el oficio de farolero fue desapareciendo?", ops: ["Porque llegó la luz eléctrica", "Porque nadie salía de noche", "Porque se terminaron las velas"], ok: 0, m: "El texto dice: «Cuando llegó la luz eléctrica, ese oficio fue desapareciendo»." }
    ]
  },
  {
    texto: "En la casa de Lucía el sábado es día de feria. Su papá arma dos bolsos grandes y caminan cuatro cuadras hasta la plaza. Ahí compran verduras, frutas y a veces flores para la abuela. A Lucía le encanta elegir las mandarinas más grandes. Cuando vuelven, ayuda a guardar todo en la heladera y se gana un jugo de naranja.",
    preguntas: [
      { q: "¿Qué día van a la feria Lucía y su papá?", ops: ["El sábado", "El domingo", "El lunes"], ok: 0, m: "El texto dice: «el sábado es día de feria»." },
      { q: "¿Por qué llevan dos bolsos grandes?", ops: ["Para poder traer todo lo que compran", "Porque viven muy lejos de la plaza", "Porque van a vender cosas"], ok: 0, m: "Compran verduras, frutas y flores, así que necesitan los bolsos para cargar todo lo que llevan a casa." }
    ]
  },
  {
    texto: "El yaguareté es el felino más grande de América y vive en el norte de la Argentina. Es un excelente nadador y no le tiene miedo al agua, algo raro entre los gatos. Se alimenta de otros animales y caza casi siempre de noche. Hoy quedan muy pocos, por eso hay parques donde está protegido para que no desaparezca.",
    preguntas: [
      { q: "¿En qué parte de la Argentina vive el yaguareté?", ops: ["En el norte", "En el sur", "En la ciudad"], ok: 0, m: "El texto dice que el yaguareté «vive en el norte de la Argentina»." },
      { q: "¿Por qué hay parques donde el yaguareté está protegido?", ops: ["Porque quedan muy pocos y no se quiere que desaparezca", "Porque es muy manso y juega con la gente", "Porque le gusta mucho nadar"], ok: 0, m: "El texto dice: «quedan muy pocos, por eso hay parques donde está protegido para que no desaparezca»." }
    ]
  },
  {
    texto: "Benjamín quería jugar al fútbol, pero justo empezó a llover fuerte. En vez de enojarse, agarró una sábana vieja, la ató entre dos sillas y armó una carpa en el living. Adentro puso una linterna y sus muñecos. Su hermanita se sumó con galletitas. Cuando el papá llegó del trabajo, encontró a los dos riéndose dentro de la carpa y dijo que era el mejor campamento del mundo.",
    preguntas: [
      { q: "¿Con qué armó Benjamín la carpa?", ops: ["Con una sábana vieja atada entre dos sillas", "Con cajas de cartón", "Con ramas del jardín"], ok: 0, m: "El texto dice que «agarró una sábana vieja, la ató entre dos sillas y armó una carpa»." },
      { q: "¿Qué hizo Benjamín cuando no pudo jugar al fútbol?", ops: ["Buscó otra manera de divertirse", "Se quedó llorando todo el día", "Se fue a dormir enojado"], ok: 0, m: "«En vez de enojarse», armó una carpa en el living, así que buscó divertirse de otra forma." }
    ]
  }
];

const COMPRENSION_4 = [
  {
    texto: "Las abejas viven en colmenas donde cada una tiene una tarea. Las obreras salen a buscar néctar de las flores y, al volver, hacen una especie de bailecito para avisarles a las demás dónde hay comida. Con ese baile marcan la dirección y la distancia. Además, cuando visitan las flores, transportan el polen de una a otra sin darse cuenta, y así ayudan a que nazcan nuevas plantas y frutas. Por eso se dice que las abejas son fundamentales para el campo: sin ellas, muchísimos alimentos que comemos todos los días serían mucho más difíciles de conseguir.",
    preguntas: [
      { q: "¿Para qué hacen un bailecito las abejas obreras?", ops: ["Para avisar a las demás dónde hay comida", "Para descansar después de volar", "Para asustar a otros insectos"], ok: 0, m: "El texto dice que bailan «para avisarles a las demás dónde hay comida», marcando dirección y distancia." },
      { q: "¿Por qué las abejas son importantes para el campo?", ops: ["Porque llevan el polen y ayudan a que nazcan plantas y frutas", "Porque hacen mucho ruido al volar", "Porque construyen colmenas muy grandes"], ok: 0, m: "El texto explica que transportan polen de una flor a otra «y así ayudan a que nazcan nuevas plantas y frutas»." },
      { q: "En el texto, la palabra «fundamentales» quiere decir…", ops: ["muy importantes, necesarias", "divertidas y curiosas", "peligrosas"], ok: 0, m: "El texto dice que sin las abejas muchos alimentos serían difíciles de conseguir, así que «fundamentales» significa muy importantes." }
    ]
  },
  {
    texto: "Camila siempre había sido la más tímida del grado. Cuando la maestra preguntaba algo, ella sabía la respuesta, pero las palabras se le quedaban atragantadas y prefería mirar el pupitre. Un día la escuela organizó una feria de ciencias y a Camila le tocó explicar un volcán de bicarbonato. Al principio le temblaban las manos, pero cuando empezó a contar cómo funcionaba, se olvidó de los nervios. Los chicos hacían preguntas y ella respondía cada vez con más ganas. Al terminar, la maestra le dijo que había sido la mejor explicación de la feria. Camila volvió a su casa sintiendo que algo dentro de ella había cambiado para siempre.",
    preguntas: [
      { q: "¿Qué tuvo que explicar Camila en la feria de ciencias?", ops: ["Un volcán de bicarbonato", "El sistema solar", "El ciclo del agua"], ok: 0, m: "El texto dice que «a Camila le tocó explicar un volcán de bicarbonato»." },
      { q: "¿Qué le pasó a Camila mientras explicaba?", ops: ["Se fue soltando y perdió los nervios", "Se puso a llorar y se fue", "Se quedó muda todo el tiempo"], ok: 0, m: "«Cuando empezó a contar cómo funcionaba, se olvidó de los nervios» y respondía «cada vez con más ganas»." },
      { q: "La frase «las palabras se le quedaban atragantadas» significa que Camila…", ops: ["no se animaba a decir lo que pensaba", "se olvidaba de todo lo estudiado", "hablaba demasiado rápido"], ok: 0, m: "Sabía la respuesta pero «prefería mirar el pupitre», así que no lograba animarse a hablar." }
    ]
  },
  {
    texto: "Antes de que existieran las heladeras, guardar la comida en verano era un problema serio. En muchas casas se usaba la fresquera, un mueble de madera con puertitas de tela metálica que se colgaba en un lugar fresco y con sombra. La tela dejaba pasar el aire pero no las moscas, así que la comida se conservaba un poco más. Para tener hielo, algunas familias lo compraban a un repartidor que pasaba con un carro cargado de grandes barras heladas envueltas en aserrín. El aserrín ayudaba a que el hielo no se derritiera tan rápido. Cuando aparecieron las heladeras eléctricas, todo esto quedó en el recuerdo de los abuelos.",
    preguntas: [
      { q: "¿Qué era la fresquera?", ops: ["Un mueble de madera con puertitas de tela metálica", "Una heladera eléctrica muy antigua", "Un carro que repartía hielo"], ok: 0, m: "El texto dice que la fresquera era «un mueble de madera con puertitas de tela metálica»." },
      { q: "¿Para qué envolvían las barras de hielo en aserrín?", ops: ["Para que no se derritieran tan rápido", "Para que pesaran menos", "Para que se vieran más lindas"], ok: 0, m: "El texto dice que «el aserrín ayudaba a que el hielo no se derritiera tan rápido»." },
      { q: "En el texto, «se conservaba» quiere decir que la comida…", ops: ["se mantenía en buen estado más tiempo", "se cocinaba sola", "se llenaba de moscas"], ok: 0, m: "La tela no dejaba pasar las moscas, así que la comida «se conservaba un poco más», es decir, duraba mejor." }
    ]
  },
  {
    texto: "El profe de música propuso un desafío: cada chico tenía que traer un instrumento hecho con materiales reciclados. Joaquín no sabía qué hacer hasta que su mamá le mostró una caja de zapatos vacía y unas gomitas elásticas. Estiró las gomitas alrededor de la caja, dejando un huequito en el medio, y descubrió que al puntearlas sonaban como una guitarra chiquita. Cuanto más finita era la gomita, más agudo era el sonido. El día de la muestra, Joaquín tocó una canción sencilla y varios compañeros quisieron copiarle la idea. El profe lo felicitó y le dijo que había entendido de qué se trataba la música.",
    preguntas: [
      { q: "¿Con qué hizo Joaquín su instrumento?", ops: ["Con una caja de zapatos y gomitas elásticas", "Con latas y piedritas", "Con botellas y arena"], ok: 0, m: "El texto dice que usó «una caja de zapatos vacía y unas gomitas elásticas»." },
      { q: "Según el texto, ¿qué pasaba con el sonido cuando la gomita era más finita?", ops: ["El sonido era más agudo", "El sonido era más grave", "No sonaba nada"], ok: 0, m: "El texto dice: «Cuanto más finita era la gomita, más agudo era el sonido»." },
      { q: "En el texto, «puntearlas» se refiere a…", ops: ["tocar las gomitas con los dedos para hacerlas sonar", "romperlas de un tirón", "atarlas con un nudo"], ok: 0, m: "Al «puntearlas sonaban como una guitarra chiquita», así que es tocarlas con los dedos para que suenen." }
    ]
  },
  {
    texto: "El río Paraná es uno de los más importantes de la Argentina. Nace en Brasil y recorre miles de kilómetros hasta unirse con otros ríos y desembocar en el Río de la Plata. Por sus aguas navegan enormes barcos que llevan granos, como la soja y el maíz, hacia otros países. En sus orillas viven muchísimos animales: carpinchos, yacarés y aves de todos los colores. Además, el río forma islas y humedales que funcionan como una gran esponja natural: absorben el agua de las crecidas y ayudan a que no se inunden las ciudades cercanas. Cuidar el Paraná es cuidar a toda la vida que depende de él.",
    preguntas: [
      { q: "¿Qué transportan los barcos que navegan por el Paraná?", ops: ["Granos, como la soja y el maíz", "Autos y camiones", "Turistas de vacaciones"], ok: 0, m: "El texto dice que los barcos «llevan granos, como la soja y el maíz, hacia otros países»." },
      { q: "¿Por qué el texto compara los humedales con una esponja?", ops: ["Porque absorben el agua de las crecidas", "Porque son de color amarillo", "Porque flotan sobre el río"], ok: 0, m: "El texto dice que «absorben el agua de las crecidas y ayudan a que no se inunden las ciudades cercanas»." },
      { q: "En el texto, «desembocar» significa que el río…", ops: ["termina su recorrido volcando sus aguas en otro", "se seca por completo", "cambia de color"], ok: 0, m: "El río recorre kilómetros «hasta unirse con otros ríos y desembocar en el Río de la Plata», o sea que ahí termina y vuelca sus aguas." }
    ]
  },
  {
    texto: "En el fondo de la casa vivía una gata callejera a la que nadie se animaba a acariciar. Bufaba apenas alguien se acercaba y se escondía entre los cajones. Valentina decidió ganarse su confianza de a poco. Todos los días le dejaba un platito de comida un pasito más cerca de la puerta y se sentaba a leer en silencio, sin mirarla. La gata la observaba de lejos. Pasaron dos semanas hasta que, una tarde, el animal se acercó y se acostó al sol, cerca de sus pies. Valentina no se movió ni la tocó: entendió que la paciencia había hecho su trabajo. Con el tiempo, la gata terminó durmiendo en su regazo.",
    preguntas: [
      { q: "¿Qué hacía Valentina todos los días para ganarse a la gata?", ops: ["Le dejaba comida cada vez más cerca y leía en silencio", "La perseguía por el patio", "La agarraba y la abrazaba"], ok: 0, m: "El texto dice que «le dejaba un platito de comida un pasito más cerca» y «se sentaba a leer en silencio, sin mirarla»." },
      { q: "¿Por qué Valentina no se movió cuando la gata se acostó cerca?", ops: ["Para no asustarla y no romper la confianza", "Porque estaba dormida", "Porque no la había visto"], ok: 0, m: "«Entendió que la paciencia había hecho su trabajo», así que no quiso asustar a la gata con un movimiento." },
      { q: "En el texto, «bufaba» describe que la gata…", ops: ["hacía un sonido de enojo para alejar a la gente", "ronroneaba contenta", "maullaba de hambre"], ok: 0, m: "Bufaba «apenas alguien se acercaba» y se escondía, así que era una señal de enojo o miedo, no de cariño." }
    ]
  },
  {
    texto: "Manuel Belgrano es recordado por haber creado la bandera argentina, pero pocos saben que también fue un gran defensor de la educación. Cuando el gobierno le entregó una importante suma de dinero como premio por sus victorias militares, él decidió no quedarse con nada. Pidió que ese dinero se usara para construir cuatro escuelas en distintos pueblos, porque estaba convencido de que un país solo podía progresar si su gente sabía leer y escribir. Belgrano vivió de manera sencilla y murió sin riquezas. Muchos años después, su gesto sigue siendo un ejemplo de que hay personas que piensan más en el bien de todos que en el propio.",
    preguntas: [
      { q: "¿Qué pidió Belgrano que se hiciera con el dinero del premio?", ops: ["Que se construyeran cuatro escuelas", "Que se comprara una casa para él", "Que se armara un ejército más grande"], ok: 0, m: "El texto dice que «pidió que ese dinero se usara para construir cuatro escuelas en distintos pueblos»." },
      { q: "¿Qué muestra sobre Belgrano su decisión con el dinero?", ops: ["Que le importaba más el bien de todos que su propio beneficio", "Que le tenía miedo al dinero", "Que no le gustaban las escuelas"], ok: 0, m: "El texto concluye que Belgrano pensaba «más en el bien de todos que en el propio»." },
      { q: "En el texto, «progresar» significa…", ops: ["mejorar y avanzar", "quedarse igual que siempre", "achicarse"], ok: 0, m: "Belgrano creía que el país «solo podía progresar si su gente sabía leer y escribir», es decir, mejorar y avanzar." }
    ]
  },
  {
    texto: "Cuando cortás una cebolla, muchas veces se te llenan los ojos de lágrimas sin que tengas ganas de llorar. Eso no pasa por casualidad. La cebolla, al ser cortada, libera un gas invisible que sube hasta los ojos. El cuerpo, para protegerse de ese gas que le molesta, produce lágrimas que ayudan a limpiarlo. Es un truco natural que tiene nuestro organismo para cuidar una parte tan delicada. Existen algunos trucos para que moleste menos, como enfriar la cebolla en la heladera antes de cortarla o mojar el cuchillo con agua. Así el gas se dispersa más lento y llega menos cantidad a los ojos.",
    preguntas: [
      { q: "¿Qué libera la cebolla cuando la cortás?", ops: ["Un gas invisible que sube a los ojos", "Un líquido pegajoso", "Un polvo blanco"], ok: 0, m: "El texto dice que la cebolla «libera un gas invisible que sube hasta los ojos»." },
      { q: "¿Por qué el cuerpo produce lágrimas al cortar cebolla?", ops: ["Para protegerse y limpiar el gas que molesta", "Porque estamos tristes", "Porque tenemos sueño"], ok: 0, m: "El cuerpo, «para protegerse de ese gas que le molesta, produce lágrimas que ayudan a limpiarlo»." },
      { q: "En el texto, «se dispersa» quiere decir que el gas…", ops: ["se reparte y se aleja por el aire", "se vuelve más fuerte", "se convierte en agua"], ok: 0, m: "Enfriar la cebolla hace que «el gas se disperse más lento y llegue menos a los ojos», o sea que se reparte por el aire." }
    ]
  }
];

const COMPRENSION_5 = [
  {
    texto: "Los pingüinos de Magallanes son unas de las aves más queridas de la costa argentina. Cada primavera, miles de ellos llegan a las playas de la Patagonia, sobre todo a Punta Tombo, en la provincia de Chubut, para formar sus nidos y tener sus pichones. Aunque son pájaros, no pueden volar: sus alas se transformaron en aletas que les sirven para nadar a gran velocidad y bucear detrás de los peces de los que se alimentan. En tierra caminan de manera torpe, balanceándose de un lado a otro, pero en el agua son verdaderos atletas. Los machos y las hembras se turnan para cuidar los huevos y buscar comida, y son capaces de reconocer la voz de su pareja entre miles de pingüinos que graznan al mismo tiempo. Cuando los pichones crecen y aprenden a nadar, toda la colonia emprende un largo viaje por el mar hacia aguas más cálidas. En los últimos años, los científicos estudian con atención a estos animales, porque los cambios en la temperatura del océano y la contaminación con petróleo ponen en peligro su supervivencia. Proteger sus playas es una manera de asegurar que sigan volviendo cada primavera.",
    preguntas: [
      { q: "¿De qué trata principalmente el texto?", ops: ["De cómo viven los pingüinos de Magallanes y por qué hay que protegerlos", "De cómo aprenden a volar los pingüinos", "De las playas más lindas de Chubut"], ok: 0, m: "El texto describe la vida de estos pingüinos y termina explicando que hay que proteger sus playas; nunca dice que vuelen ni es una guía de playas." },
      { q: "¿Por qué el texto dice que los pingüinos son «verdaderos atletas» en el agua?", ops: ["Porque nadan a gran velocidad y bucean muy bien", "Porque caminan mucho por la playa", "Porque vuelan largas distancias"], ok: 0, m: "En el agua «nadan a gran velocidad y bucean detrás de los peces», a diferencia de la tierra, donde caminan torpes." },
      { q: "En el texto, «colonia» se refiere a…", ops: ["el gran grupo de pingüinos que vive junto", "un tipo de nido de barro", "una playa sin animales"], ok: 0, m: "Se habla de «toda la colonia» que emprende el viaje y de «miles de pingüinos» juntos, así que es el grupo entero." }
    ]
  },
  {
    texto: "Feliciano heredó de su abuelo una vieja bicicleta con el cuadro oxidado y las gomas pinchadas. Sus amigos le decían que era un fierro viejo que no servía para nada, pero él veía otra cosa. Se acordaba de las tardes en que el abuelo lo llevaba sentado en el caño, contándole historias mientras pedaleaban por el barrio. Durante todo un mes, Feliciano juntó lo que ganaba lavando autos y compró cámaras nuevas, aceite para la cadena y una lata de pintura azul. Su tío, que sabía de mecánica, le enseñó a ajustar los frenos y a poner los rayos derechos. No fue fácil: más de una vez le quedaban las manos negras de grasa y las cosas no salían a la primera. Pero Feliciano no aflojó. Cuando por fin terminó, la bicicleta parecía otra. Brillaba al sol y andaba suave, sin un solo ruido. La primera vuelta la dio despacio, saludando a los vecinos, y sintió que de alguna manera su abuelo iba pedaleando con él. Los mismos amigos que se habían reído le pidieron para dar una vuelta. Feliciano se la prestó, pero les aclaró una cosa: esa bicicleta no se vendía por ningún precio.",
    preguntas: [
      { q: "¿Cuál es la idea principal del cuento?", ops: ["Feliciano recupera con esfuerzo la bicicleta de su abuelo porque tiene un valor especial para él", "Feliciano aprende a lavar autos para ganar dinero", "Feliciano vende una bicicleta vieja a sus amigos"], ok: 0, m: "Todo el texto muestra cómo Feliciano arregla la bici por lo que significa; al final aclara que «no se vendía por ningún precio»." },
      { q: "¿Por qué Feliciano sentía que su abuelo «iba pedaleando con él»?", ops: ["Porque la bicicleta le traía el recuerdo de su abuelo", "Porque el abuelo estaba sentado atrás", "Porque la bici andaba sola"], ok: 0, m: "El texto cuenta los recuerdos de las tardes con el abuelo; la frase expresa esa emoción, no algo que pasara de verdad." },
      { q: "En el texto, «no aflojó» significa que Feliciano…", ops: ["no se rindió y siguió adelante", "no ajustó bien los frenos", "se olvidó del proyecto"], ok: 0, m: "A pesar de que «las cosas no salían a la primera», siguió trabajando; «no aflojó» es no rendirse." }
    ]
  },
  {
    texto: "El 25 de mayo de 1810 es una de las fechas más importantes de la historia argentina, pero lo que pasó ese día suele contarse de manera muy simplificada. En aquel entonces, el territorio que hoy llamamos Argentina era una colonia que dependía de España, y el máximo representante del rey era el virrey. Durante varios días de esa semana, un grupo de vecinos de Buenos Aires se reunió para discutir quién debía gobernar, ya que en España el rey había sido tomado prisionero por los ejércitos de Francia. Después de mucho debate, el 25 de mayo se formó la Primera Junta, un gobierno propio integrado por criollos, es decir, personas nacidas en América. Todavía no era una declaración de independencia: eso llegaría recién seis años más tarde, en 1816. Pero fue un primer paso enorme, porque por primera vez las decisiones no venían de España sino de personas de estas tierras. Aquellos días de mayo estuvieron llenos de discusiones, dudas y valentía. No hubo paraguas ni lluvia como muchas veces se dibuja: esa es una imagen inventada. Lo verdaderamente importante fue que un grupo de personas se animó a imaginar que podían decidir su propio futuro.",
    preguntas: [
      { q: "¿Cuál es la idea central del texto?", ops: ["El 25 de mayo de 1810 se formó un gobierno propio, un primer paso hacia la independencia", "El 25 de mayo de 1810 la Argentina declaró su independencia", "El 25 de mayo llovió mucho en Buenos Aires"], ok: 0, m: "El texto aclara que se formó la Primera Junta y que «todavía no era una declaración de independencia»; lo de la lluvia es «una imagen inventada»." },
      { q: "¿Por qué los vecinos se reunieron a discutir quién debía gobernar?", ops: ["Porque el rey de España había sido tomado prisionero", "Porque querían elegir un nuevo virrey español", "Porque España les había pedido ayuda militar"], ok: 0, m: "El texto dice que se reunieron «ya que en España el rey había sido tomado prisionero por los ejércitos de Francia»." },
      { q: "En el texto, «criollos» se refiere a…", ops: ["personas nacidas en América", "soldados venidos de Francia", "representantes del rey de España"], ok: 0, m: "El texto define a los criollos como «personas nacidas en América»." }
    ]
  },
  {
    texto: "¿Alguna vez te preguntaste por qué el cielo es celeste durante el día y se pone anaranjado al atardecer? La respuesta está en la luz del sol y en el aire que rodea la Tierra. Aunque la luz del sol parece blanca, en realidad está formada por todos los colores del arcoíris mezclados. Cuando esa luz entra en nuestra atmósfera, choca contra millones de partículas diminutas que hay en el aire. El color azul es el que más se dispersa, es decir, el que más rebota en todas direcciones. Por eso, cuando levantás la vista en un día despejado, ves el cielo teñido de celeste: es la luz azul rebotando por todos lados. Al atardecer, en cambio, el sol está más bajo y su luz tiene que atravesar una porción de aire mucho más gruesa antes de llegar a tus ojos. En ese camino largo, el azul se pierde casi por completo y quedan los tonos rojizos y anaranjados, que logran pasar. Por eso los atardeceres se pintan de colores cálidos. Entender esto nos permite mirar el cielo con otros ojos: cada color que vemos es en realidad una pista de cómo viaja la luz.",
    preguntas: [
      { q: "¿De qué trata principalmente el texto?", ops: ["De por qué el cielo cambia de color según la hora del día", "De cómo se forma el arcoíris después de la lluvia", "De por qué el sol es de color blanco"], ok: 0, m: "El texto explica por qué el cielo es celeste de día y anaranjado al atardecer." },
      { q: "¿Por qué al atardecer el cielo se ve anaranjado y no celeste?", ops: ["Porque la luz atraviesa más aire y el azul se pierde en el camino", "Porque el sol se apaga de a poco", "Porque el aire se llena de nubes rojas"], ok: 0, m: "El texto dice que al atardecer la luz «atraviesa una porción de aire mucho más gruesa» y «el azul se pierde casi por completo»." },
      { q: "En el texto, «se dispersa» significa que la luz…", ops: ["rebota y se reparte en todas direcciones", "se apaga lentamente", "se vuelve más caliente"], ok: 0, m: "El texto aclara que el azul «se dispersa, es decir, el que más rebota en todas direcciones»." }
    ]
  },
  {
    texto: "En la escuela de Renata decidieron armar una huerta en un rincón del patio que estaba abandonado. Al principio parecía imposible: el suelo estaba duro, lleno de piedras y de yuyos secos. La maestra les explicó que una huerta no se hace de un día para el otro y que iban a tener que trabajar en equipo y tener paciencia. Los chicos se organizaron por grupos. Unos aflojaron la tierra con palas, otros la mezclaron con abono, y otros armaron carteles para saber dónde iba cada planta. Sembraron lechuga, rabanitos, tomates y algunas flores para atraer insectos que ayudan a las plantas. Cada grado se hizo cargo de regar durante una semana. No todo salió bien: algunas semillas no brotaron y una helada quemó las primeras plantitas. En vez de abandonar, volvieron a sembrar y taparon los canteros con nailon durante las noches frías. Después de dos meses, cosecharon sus primeros rabanitos y los repartieron en el comedor. Renata contó en su casa que lo mejor no fue comer lo que plantaron, sino descubrir que, trabajando entre todos y sin rendirse, un rincón olvidado se podía transformar en algo lleno de vida.",
    preguntas: [
      { q: "¿Cuál es la idea principal del texto?", ops: ["Con trabajo en equipo y paciencia, los chicos transformaron un rincón abandonado en una huerta", "Los rabanitos son la verdura más fácil de plantar", "Las heladas siempre arruinan las huertas escolares"], ok: 0, m: "Todo el texto muestra el esfuerzo compartido y el cierre lo dice: un rincón olvidado «se podía transformar en algo lleno de vida»." },
      { q: "¿Qué hicieron los chicos cuando la helada quemó las primeras plantitas?", ops: ["Volvieron a sembrar y protegieron los canteros de noche", "Abandonaron la huerta y buscaron otro patio", "Le echaron la culpa a la maestra"], ok: 0, m: "«En vez de abandonar, volvieron a sembrar y taparon los canteros con nailon durante las noches frías»." },
      { q: "En el texto, «cosecharon» significa que los chicos…", ops: ["juntaron lo que había crecido en la huerta", "plantaron nuevas semillas", "regaron las plantas"], ok: 0, m: "Después de dos meses «cosecharon sus primeros rabanitos y los repartieron», es decir, recogieron lo que habían cultivado." }
    ]
  },
  {
    texto: "El tero es un ave muy común en los campos y las plazas de la Argentina, y tiene fama de ser el mejor vigilante de la llanura. Apenas percibe que alguien o algo se acerca, lanza su grito característico, un teru-teru fuerte y repetido que se escucha desde lejos. Por eso, en el campo se dice que donde hay un tero difícilmente algo pase desapercibido. Lo más curioso es la manera en que protege su nido. El tero no construye grandes refugios: pone sus huevos directamente en el suelo, en un huequito apenas disimulado entre el pasto. Como quedan tan expuestos, desarrolló una estrategia muy astuta. Cuando un intruso se acerca al nido, el tero se aleja de él caminando y se hace el herido, arrastrando un ala como si estuviera lastimado. El intruso lo sigue, creyendo que atrapará una presa fácil, y así se aleja cada vez más de los huevos. Cuando el peligro ya está lejos, el tero levanta vuelo sano y salvo. Gracias a esta actuación, muchos huevos logran sobrevivir. El tero demuestra que, en la naturaleza, la inteligencia puede ser tan valiosa como la fuerza para sobrevivir.",
    preguntas: [
      { q: "¿Cuál es la idea central del texto?", ops: ["El tero usa su grito y una actuación astuta para protegerse y cuidar su nido", "El tero es el ave más grande de la Argentina", "El tero construye enormes nidos en los árboles"], ok: 0, m: "El texto describe su grito de alerta y su truco de hacerse el herido; justamente aclara que NO hace grandes nidos." },
      { q: "¿Por qué el tero se hace el herido cuando alguien se acerca al nido?", ops: ["Para que el intruso lo siga y se aleje de los huevos", "Porque de verdad está lastimado", "Para asustar al intruso con su grito"], ok: 0, m: "El intruso «lo sigue» y «se aleja cada vez más de los huevos»; después el tero «levanta vuelo sano y salvo»." },
      { q: "En el texto, «desapercibido» quiere decir…", ops: ["sin ser notado", "sin hacer ruido", "muy asustado"], ok: 0, m: "Se dice que «donde hay un tero difícilmente algo pase desapercibido» porque el tero avisa; es decir, algo no pasa sin ser notado." }
    ]
  },
  {
    texto: "El mate es mucho más que una infusión: es una costumbre que une a millones de personas en la Argentina, Uruguay, Paraguay y el sur de Brasil. Su historia empieza mucho antes de que llegaran los españoles a América. Los guaraníes, pueblos originarios de esta región, ya conocían la yerba mate y la usaban tanto por su sabor como por la energía que les daba para las largas caminatas. Cuando los europeos llegaron, al principio desconfiaron de esta bebida, pero con el tiempo se acostumbraron y ayudaron a que su consumo se extendiera. Durante muchos años, la yerba se recolectaba de plantas silvestres en el monte. Recién más tarde se aprendió a cultivarla en grandes plantaciones, sobre todo en las provincias de Misiones y Corrientes, donde el clima cálido y húmedo es ideal. Hoy el mate forma parte de la vida cotidiana. Se comparte en la ronda familiar, entre compañeros de trabajo o de estudio, y hasta tiene su propia manera de tomarse: uno ceba y los demás esperan su turno. Ese gesto de pasar el mismo mate de mano en mano es, quizás, lo que mejor explica por qué esta bebida se volvió un símbolo de encuentro y amistad.",
    preguntas: [
      { q: "¿Cuál es la idea principal del texto?", ops: ["El mate tiene una larga historia y se convirtió en un símbolo de encuentro", "El mate fue inventado por los españoles al llegar a América", "El mate solo se cultiva en Brasil"], ok: 0, m: "El texto recorre su origen guaraní y termina diciendo que es «un símbolo de encuentro y amistad»; aclara que los españoles al principio «desconfiaron»." },
      { q: "¿Por qué la yerba mate se cultiva sobre todo en Misiones y Corrientes?", ops: ["Porque el clima cálido y húmedo de esas provincias es ideal", "Porque ahí vivían todos los españoles", "Porque son las provincias más grandes del país"], ok: 0, m: "El texto dice que se cultiva ahí «donde el clima cálido y húmedo es ideal»." },
      { q: "En el texto, «silvestres» describe plantas que…", ops: ["crecen solas en la naturaleza, sin ser cultivadas", "fueron plantadas por los guaraníes", "crecen únicamente en macetas"], ok: 0, m: "La yerba «se recolectaba de plantas silvestres en el monte» antes de que «se aprendiera a cultivarla», así que crecían solas." }
    ]
  }
];

const COMPRENSION_6 = [
  {
    texto: "El carpincho es el roedor más grande del mundo y habita en gran parte de la Argentina, especialmente cerca de ríos, lagunas y humedales del Litoral. Un ejemplar adulto puede medir más de un metro de largo y pesar alrededor de sesenta kilos, casi lo mismo que una persona. A pesar de su tamaño, es un animal tranquilo y sociable que vive en grupos de diez o más individuos. Su cuerpo está perfectamente adaptado a la vida en el agua. Tiene los ojos, la nariz y las orejas en la parte alta de la cabeza, de modo que puede permanecer casi sumergido y seguir viendo y respirando. Entre los dedos tiene pequeñas membranas que lo convierten en un excelente nadador, y cuando se siente amenazado por un puma o un yacaré, se zambulle y puede quedarse bajo el agua varios minutos. Los carpinchos se alimentan de pasto y plantas acuáticas. Como todo roedor, sus dientes crecen durante toda la vida, así que necesitan masticar constantemente para desgastarlos. En los últimos años se los ve cada vez más cerca de las ciudades, e incluso dentro de barrios construidos sobre antiguos humedales, lo que generó no pocas discusiones entre los vecinos. Para muchos, la llegada de los carpinchos a esos barrios es una molestia, porque comen el pasto de los jardines y cruzan las calles. Sin embargo, hay que recordar algo importante: esos terrenos fueron durante miles de años el hogar natural de estos animales, mucho antes de que existieran las casas. En mi opinión, aprender a convivir con la fauna que estaba antes que nosotros es una de las tareas más urgentes de nuestro tiempo. Los especialistas explican que los carpinchos no son peligrosos si no se los molesta y que su presencia suele ser una señal de que el ambiente todavía conserva algo de vida silvestre. Observarlos de lejos, sin alimentarlos ni perseguirlos, es la mejor manera de compartir el espacio. Al fin y al cabo, el desafío no es echarlos, sino entender que la naturaleza y la ciudad pueden encontrar un equilibrio.",
    preguntas: [
      { q: "¿Cuál es la idea principal del texto?", ops: ["El carpincho es un animal adaptado al agua cuya llegada a las ciudades nos invita a aprender a convivir con la fauna", "Los carpinchos son animales peligrosos que hay que sacar de los barrios", "El carpincho es el único roedor del mundo que sabe nadar", "Los humedales del Litoral deberían convertirse en barrios"], ok: 0, m: "El texto describe al carpincho y sus adaptaciones y sostiene que el desafío es «entender que la naturaleza y la ciudad pueden encontrar un equilibrio»." },
      { q: "¿Por qué el carpincho tiene los ojos, la nariz y las orejas en la parte alta de la cabeza?", ops: ["Para poder estar casi sumergido y aun así ver y respirar", "Para escuchar mejor a los otros carpinchos", "Para parecer más grande ante los pumas", "Para protegerse del sol del verano"], ok: 0, m: "El texto dice que gracias a esa ubicación «puede permanecer casi sumergido y seguir viendo y respirando»." },
      { q: "¿Cuál de estas afirmaciones del texto es una OPINIÓN y no un hecho comprobable?", ops: ["Aprender a convivir con la fauna es una de las tareas más urgentes de nuestro tiempo", "El carpincho es el roedor más grande del mundo", "Los carpinchos tienen pequeñas membranas entre los dedos", "Un carpincho adulto puede pesar alrededor de sesenta kilos"], ok: 0, m: "La afirmación sobre las «tareas más urgentes» expresa lo que piensa el autor (dice «en mi opinión»); las otras tres son datos que se pueden verificar." }
    ]
  },
  {
    texto: "Entre finales del siglo XIX y comienzos del siglo XX, la Argentina recibió una de las mayores olas de inmigración de su historia. Millones de personas llegaron en barco desde Europa, sobre todo desde Italia y España, aunque también vinieron de países como Rusia, Polonia, Siria y el Líbano. Escapaban del hambre, de las guerras o simplemente buscaban una vida mejor en un país que prometía trabajo y tierra. El viaje no era nada sencillo. La travesía en barco podía durar semanas, en condiciones incómodas y con muchas personas amontonadas. Al llegar a Buenos Aires, los recién llegados pasaban por el Hotel de Inmigrantes, un enorme edificio donde recibían alojamiento y comida durante unos días mientras conseguían trabajo. Muchos no hablaban español y no conocían a nadie. Buena parte de estos inmigrantes se instaló en los conventillos, casas viejas y grandes divididas en muchas piezas, donde cada familia ocupaba una sola habitación y compartía el patio, la cocina y el baño con el resto. Aunque las condiciones eran duras y a veces había conflictos, en esos patios también nacieron amistades, se mezclaron idiomas y costumbres, y surgieron cosas tan nuestras como el tango y el lunfardo, esa manera especial de hablar. El aporte de los inmigrantes cambió para siempre la forma de ser del país. Trajeron oficios, comidas, palabras y música que hoy sentimos como propias. Basta pensar en la pizza, en las pastas de los domingos o en apellidos de todo tipo que conviven en cualquier aula argentina. Para mí, esta historia deja una enseñanza que sigue siendo valiosa: un país se enriquece cuando abre sus puertas y mezcla lo que traen personas de orígenes distintos. No siempre fue fácil ni estuvo libre de injusticias, porque muchos inmigrantes sufrieron el desprecio o trabajaron en condiciones muy malas. Pero, con el tiempo, aquellos que llegaron con una valija y pocas palabras se convirtieron en los abuelos y bisabuelos de una parte enorme de los argentinos de hoy. Conocer de dónde venimos nos ayuda a entender mejor quiénes somos.",
    preguntas: [
      { q: "¿Cuál es la idea central del texto?", ops: ["La gran ola de inmigración europea transformó para siempre la cultura y la forma de ser de la Argentina", "El viaje en barco desde Europa era muy cómodo y rápido", "Los conventillos eran los mejores lugares para vivir en la ciudad", "La Argentina solo recibió inmigrantes de Italia y España"], ok: 0, m: "El texto recorre la llegada de los inmigrantes y concluye que «el aporte de los inmigrantes cambió para siempre la forma de ser del país»." },
      { q: "¿Por qué en los conventillos surgieron cosas como el tango y el lunfardo?", ops: ["Porque en ellos se mezclaron personas de distintos orígenes, idiomas y costumbres", "Porque el gobierno obligaba a los inmigrantes a cantar", "Porque eran casas muy grandes y lujosas", "Porque allí solo vivían músicos famosos"], ok: 0, m: "El texto dice que en esos patios «se mezclaron idiomas y costumbres, y surgieron cosas tan nuestras como el tango y el lunfardo»." },
      { q: "¿Cuál de estas frases del texto es una OPINIÓN del autor?", ops: ["Un país se enriquece cuando abre sus puertas y mezcla lo que traen personas de orígenes distintos", "Los inmigrantes llegaban en barco después de un viaje de varias semanas", "En el Hotel de Inmigrantes recibían alojamiento y comida", "Muchos inmigrantes vinieron de Italia y de España"], ok: 0, m: "La frase sobre que «un país se enriquece» expresa lo que piensa el autor («Para mí...»); las otras tres son hechos verificables." }
    ]
  },
  {
    texto: "El faro del Cabo llevaba encendido más de cien años cuando llegó Ernesto, el nuevo farero. Era un hombre callado que había pedido ese puesto justamente porque quería estar lejos de todo. El pueblo más cercano quedaba a dos horas de caminata por la costa, y los únicos vecinos eran las gaviotas y el ruido eterno del mar. Los primeros días fueron difíciles. La soledad, que Ernesto había buscado con tantas ganas, de pronto le pesaba en el pecho. De noche, la luz del faro giraba sobre las olas y él se quedaba mirándola, preguntándose si no se había equivocado. «Este es el lugar más triste del mundo», pensó una madrugada, mientras el viento golpeaba las ventanas. Una mañana, entre las rocas, encontró a un perro flaco y empapado que temblaba de frío. No tenía collar ni dueño. Ernesto lo secó con una manta vieja, le dio de comer lo poco que tenía y lo dejó dormir cerca de la estufa. El perro, al que llamó Cabo, no volvió a separarse de él. Con el tiempo, algo cambió. Ernesto empezó a hablar en voz alta, primero con el perro y después consigo mismo. Descubrió que le gustaba anotar en un cuaderno los barcos que pasaban a lo lejos y las formas que dibujaban las nubes. Aprendió a reconocer cada estrella y a leer el mar como quien lee una cara conocida. Los sábados caminaba hasta el pueblo, compraba pan y cambiaba unas pocas palabras con el almacenero, y esas charlas breves empezaron a gustarle. Un año después, cuando le ofrecieron un traslado a un faro más cómodo y cercano a la ciudad, Ernesto lo pensó apenas un segundo antes de decir que no. Había llegado buscando escapar de la gente y, sin darse cuenta, había encontrado algo mejor: un lugar en el mundo y un amigo de cuatro patas. Aquella madrugada en la que había creído estar en el sitio más triste de la Tierra le parecía ahora muy lejana. El faro seguía girando su luz sobre las olas, igual que siempre, pero Ernesto ya no lo miraba con tristeza, sino como se mira un hogar.",
    preguntas: [
      { q: "¿Cuál es la idea principal del cuento?", ops: ["Ernesto buscaba estar solo, pero terminó encontrando un hogar y compañía en el faro", "Ernesto se arrepintió de haber ido al faro y volvió a la ciudad", "El faro dejó de funcionar después de cien años", "Cabo era un perro con dueño que se había perdido"], ok: 0, m: "El relato muestra cómo Ernesto pasa de la tristeza a sentir el faro «como se mira un hogar»; al final rechaza el traslado." },
      { q: "¿Por qué Ernesto rechazó el traslado a un faro más cómodo?", ops: ["Porque ya se sentía en casa y no quería dejar lo que había encontrado", "Porque el otro faro estaba roto", "Porque en la ciudad le pagaban poco", "Porque Cabo no quería mudarse"], ok: 0, m: "El texto dice que había encontrado «un lugar en el mundo y un amigo», por eso dijo que no «apenas un segundo» después." },
      { q: "En la historia, la frase «Este es el lugar más triste del mundo» es…", ops: ["una opinión de Ernesto, que refleja cómo se sentía en ese momento", "un hecho comprobable sobre el faro", "una información sobre el clima del Cabo", "una regla del trabajo de farero"], ok: 0, m: "Es lo que Ernesto pensó y sintió una madrugada; después el mismo lugar le parece un hogar, así que era una opinión, no un dato." }
    ]
  },
  {
    texto: "Cada vez que tiramos algo a la basura, ese objeto no desaparece: empieza un largo viaje que muchas veces termina en un relleno sanitario, un enorme terreno donde se entierran los residuos de las ciudades. En la Argentina, una sola persona genera en promedio alrededor de un kilo de basura por día. Si multiplicamos eso por millones de habitantes, el resultado es una montaña de residuos difícil de imaginar. El problema es que muchos de esos materiales tardan muchísimo tiempo en descomponerse. Una cáscara de banana puede desaparecer en unas pocas semanas, pero una botella de plástico puede permanecer cientos de años sin deshacerse, y una lata de aluminio, varias décadas. Mientras tanto, ocupan espacio y pueden contaminar el suelo y el agua. Frente a esto, el reciclaje aparece como una de las mejores herramientas. Reciclar significa transformar un material usado en uno nuevo: con botellas de plástico se pueden fabricar prendas de abrigo, y con papel usado, más papel. Para que esto funcione, hace falta separar los residuos en casa, distinguiendo lo que sirve para reciclar de lo que no. En muchas ciudades argentinas, buena parte de este trabajo lo realizan los recuperadores urbanos, antes conocidos como cartoneros. Recorren las calles juntando cartón, plástico y metal que después venden a las plantas de reciclaje. Durante mucho tiempo su tarea fue mirada con desprecio, pero hoy se reconoce que cumplen un papel fundamental para el ambiente. Creo que todos deberíamos hacernos responsables de la basura que producimos, porque el planeta que dejemos depende de las decisiones que tomemos cada día. Gestos pequeños, como usar una botella recargable, evitar los envases de un solo uso o separar los residuos, parecen insignificantes, pero sumados entre millones de personas hacen una diferencia enorme. El desafío no es solamente reciclar más, sino también generar menos basura desde el principio. Cuidar el ambiente no es tarea de unos pocos ni algo que pueda esperar: es una responsabilidad compartida que empieza en cada casa, en cada escuela y en cada barrio.",
    preguntas: [
      { q: "¿Cuál es la idea central del texto?", ops: ["La basura es un problema serio y reducirla y reciclarla es una responsabilidad compartida", "Los rellenos sanitarios son el mejor destino para la basura", "El plástico se descompone tan rápido como una cáscara de banana", "Solo los recuperadores urbanos deben ocuparse de la basura"], ok: 0, m: "El texto plantea el problema de los residuos y concluye que cuidar el ambiente «es una responsabilidad compartida que empieza en cada casa»." },
      { q: "¿Por qué el texto dice que una botella de plástico es más problemática que una cáscara de banana?", ops: ["Porque tarda cientos de años en descomponerse y sigue ocupando espacio", "Porque es más grande y pesada", "Porque no se puede reciclar de ninguna manera", "Porque huele peor que la banana"], ok: 0, m: "El texto contrasta que la banana desaparece «en unas pocas semanas» y la botella «puede permanecer cientos de años sin deshacerse»." },
      { q: "¿Cuál de estas afirmaciones del texto es una OPINIÓN?", ops: ["Todos deberíamos hacernos responsables de la basura que producimos", "Una persona genera en promedio alrededor de un kilo de basura por día", "Con botellas de plástico se pueden fabricar prendas de abrigo", "Los recuperadores urbanos juntan cartón, plástico y metal"], ok: 0, m: "La frase «todos deberíamos hacernos responsables» expresa lo que cree el autor («Creo que...»); las otras tres son datos verificables." }
    ]
  },
  {
    texto: "Cada año, entre los meses de junio y diciembre, las aguas de la Península Valdés, en la provincia de Chubut, se convierten en el escenario de un espectáculo asombroso: la llegada de las ballenas francas australes. Estos gigantes del mar recorren miles de kilómetros desde sus zonas de alimentación, más al sur, hasta estas costas protegidas, donde encuentran aguas tranquilas para aparearse y tener sus crías. Una ballena franca adulta puede medir hasta quince metros y pesar unas cuarenta toneladas, más que varios camiones juntos. A pesar de semejante tamaño, se alimenta de animales diminutos: filtra el agua del mar con unas estructuras llamadas barbas y atrapa pequeños organismos parecidos a camarones. No tiene dientes ni representa peligro alguno para las personas. Las crías nacen midiendo unos cinco metros y se alimentan de la leche de su madre, que es tan espesa y nutritiva que el ballenato crece a un ritmo increíble. Durante los primeros meses, madre y cría permanecen muy cerca, y no es raro verlas jugar en la superficie, sacando las aletas o saltando fuera del agua en un movimiento que los científicos todavía no terminan de explicar del todo. Hace poco más de un siglo, estas ballenas fueron cazadas sin control por su grasa y su aceite, y estuvieron a punto de desaparecer para siempre. Por suerte, la caza fue prohibida y la especie comenzó a recuperarse lentamente. Hoy, la observación de ballenas se convirtió en una actividad turística que atrae a visitantes de todo el mundo y que da trabajo a muchas familias de la zona. A mi entender, la historia de la ballena franca es una de las lecciones más esperanzadoras que nos dio la naturaleza: demuestra que, cuando los seres humanos decidimos protegerla en lugar de explotarla, la vida encuentra la manera de volver. Todavía quedan amenazas, como los choques con embarcaciones o la contaminación, pero cada temporada en que las ballenas regresan a Valdés es una prueba de que vale la pena cuidarlas. Verlas emerger del agua, enormes y pacíficas, es un recordatorio de que compartimos el planeta con criaturas extraordinarias.",
    preguntas: [
      { q: "¿Cuál es la idea principal del texto?", ops: ["La ballena franca austral se recuperó gracias a su protección y hoy es un ejemplo de lo que se logra al cuidar la naturaleza", "Las ballenas francas son peligrosas para los turistas de Chubut", "La caza de ballenas sigue siendo la principal actividad de Valdés", "Las ballenas francas tienen dientes enormes para cazar"], ok: 0, m: "El texto cuenta cómo la especie casi desaparece y se recupera, y afirma que demuestra que «cuando decidimos protegerla... la vida encuentra la manera de volver»." },
      { q: "¿Por qué las ballenas francas eligen las aguas de la Península Valdés?", ops: ["Porque son aguas tranquilas y protegidas, buenas para tener sus crías", "Porque ahí encuentran más alimento que en el sur", "Porque huyen de las embarcaciones turísticas", "Porque el agua es más profunda que en otros lugares"], ok: 0, m: "El texto dice que llegan a «estas costas protegidas, donde encuentran aguas tranquilas para aparearse y tener sus crías»." },
      { q: "¿Cuál de estas frases del texto es una OPINIÓN del autor?", ops: ["La historia de la ballena franca es una de las lecciones más esperanzadoras que nos dio la naturaleza", "Una ballena franca adulta puede pesar unas cuarenta toneladas", "Las crías se alimentan de la leche de su madre", "La caza de ballenas fue prohibida"], ok: 0, m: "La frase sobre la «lección más esperanzadora» expresa lo que opina el autor («A mi entender...»); las otras tres son hechos verificables." }
    ]
  },
  {
    texto: "En casi todos los barrios de la Argentina hay un club. A veces es un edificio grande con canchas y pileta, y a veces apenas un galpón con un par de arcos y una mesa de ping-pong. Pero, más allá de su tamaño, el club de barrio cumple una función que va mucho más allá del deporte. Los clubes nacieron hace más de un siglo, muchas veces gracias al esfuerzo de un grupo de vecinos que se juntaban para jugar al fútbol o al básquet. Con el tiempo, esos espacios crecieron y empezaron a ofrecer todo tipo de actividades: natación, gimnasia, ajedrez, teatro, murga. Para miles de chicos y chicas, el club fue y sigue siendo el lugar donde aprendieron a jugar en equipo, a ganar y a perder, y a hacer amigos que a veces duran toda la vida. Lo interesante es que la mayoría de estos clubes no persigue ganar dinero. Se sostienen con la cuota de los socios y con el trabajo de muchas personas que colaboran sin cobrar, solo por cariño a la institución. Los profesores, los dirigentes y los padres que llevan y traen a los chicos forman una red que mantiene el club en pie temporada tras temporada. En los últimos años, con tantas pantallas y actividades individuales, algunos temen que los clubes pierdan importancia. Sin embargo, siguen siendo un refugio en muchos barrios, sobre todo en los más humildes, donde ofrecen a los chicos un lugar seguro para pasar la tarde, lejos de la calle. Estoy convencido de que los clubes de barrio son uno de los tesoros más valiosos que tiene nuestra sociedad y que merecen mucho más apoyo del que reciben. No se trata solamente de formar deportistas: se trata de enseñar valores, de crear comunidad y de dar oportunidades a quienes tal vez no las tienen en otro lado. Cuidar un club es cuidar a todo un barrio. Cada vez que un vecino paga su cuota, un profe da una clase o un grupo de padres organiza una rifa para arreglar un vestuario, están sosteniendo algo que ningún celular ni ninguna pantalla podrá reemplazar del todo.",
    preguntas: [
      { q: "¿Cuál es la idea central del texto?", ops: ["El club de barrio es mucho más que deporte: forma valores, crea comunidad y merece ser cuidado", "Los clubes de barrio existen solo para ganar dinero", "Las pantallas ya reemplazaron por completo a los clubes", "Los clubes grandes son los únicos que sirven"], ok: 0, m: "El texto sostiene que el club «cumple una función que va mucho más allá del deporte» y que merece apoyo; aclara que la mayoría «no persigue ganar dinero»." },
      { q: "¿Por qué el texto dice que los clubes son importantes sobre todo en los barrios más humildes?", ops: ["Porque ofrecen a los chicos un lugar seguro para pasar la tarde, lejos de la calle", "Porque ahí las cuotas son más caras", "Porque son los únicos que tienen pileta", "Porque no dejan entrar a los adultos"], ok: 0, m: "El texto dice que en los barrios más humildes «ofrecen a los chicos un lugar seguro para pasar la tarde, lejos de la calle»." },
      { q: "¿Cuál de estas afirmaciones del texto es una OPINIÓN?", ops: ["Los clubes de barrio son uno de los tesoros más valiosos que tiene nuestra sociedad", "Muchos clubes se sostienen con la cuota de los socios", "Los clubes nacieron hace más de un siglo", "Algunos clubes ofrecen natación, ajedrez y teatro"], ok: 0, m: "La frase sobre que son «uno de los tesoros más valiosos» expresa la convicción del autor («Estoy convencido de que...»); las otras tres son hechos." }
    ]
  }
];

const COMPRENSION_7 = [
  {
    texto: "Muy pocos lugares del planeta despiertan tanta fascinación como la Antártida, ese continente helado que se extiende en el extremo sur de la Tierra. La Argentina tiene una relación especial con él: mantiene bases científicas allí desde hace más de un siglo, y la Base Orcadas, inaugurada en 1904, es la más antigua de todo el continente que sigue funcionando de forma ininterrumpida. En esas bases, hombres y mujeres pasan meses aislados, soportando temperaturas que pueden bajar de los cuarenta grados bajo cero, para estudiar el clima, el hielo y la vida que, contra todo pronóstico, habita en semejante frío. La Antártida no pertenece a ningún país. En 1959, varias naciones firmaron un tratado que la declaró un territorio dedicado exclusivamente a la paz y a la ciencia, donde está prohibido explotar sus recursos o instalar bases militares. Este acuerdo es considerado uno de los grandes logros de la cooperación internacional: demuestra que, cuando existe voluntad, los países pueden dejar de lado sus disputas para cuidar un bien común. Pero lo que hoy convierte a la Antártida en un lugar clave no es solo su belleza ni su historia, sino la información que guarda. En sus capas de hielo, formadas a lo largo de cientos de miles de años, quedaron atrapadas burbujas de aire antiquísimo. Al analizarlas, los científicos pueden reconstruir cómo era la atmósfera en el pasado remoto y compararla con la actual. Gracias a esos estudios sabemos, con enorme precisión, que la temperatura del planeta está subiendo a un ritmo poco habitual y que buena parte de ese cambio se relaciona con la actividad humana. El deshielo de la Antártida no es un problema lejano que solo afecte a los pingüinos. Si esas gigantescas masas de hielo se derritieran, el nivel de los mares subiría lo suficiente como para inundar ciudades costeras de todo el mundo, incluidas muchas de nuestro país. Por eso, lo que ocurre en ese continente remoto nos incumbe a todos, aunque nunca lleguemos a pisarlo. Conviene, entonces, mirar a la Antártida con otros ojos. No es apenas un desierto blanco y silencioso en el fin del mundo, sino una especie de gran biblioteca natural y un termómetro del planeta entero. Los datos que allí se obtienen deberían servirnos como una advertencia y, al mismo tiempo, como una guía para tomar mejores decisiones. Proteger ese continente helado y sostener la ciencia que allí se hace no es un lujo ni un capricho de exploradores: es una forma concreta de proteger el futuro de la humanidad.",
    preguntas: [
      { q: "¿Cuál sería el mejor resumen del texto?", ops: ["La Antártida es un territorio de paz y ciencia cuyo estudio nos advierte sobre el cambio climático, y por eso conviene protegerla", "La Argentina fue el primer país en conquistar y poseer la Antártida", "La Antártida es un desierto helado donde no se puede hacer nada útil", "El principal problema de la Antártida es que allí viven demasiados pingüinos"], ok: 0, m: "El texto une la historia, el tratado de paz, el valor científico del hielo y el riesgo del deshielo, y concluye que protegerla «es una forma concreta de proteger el futuro de la humanidad»." },
      { q: "¿Por qué el texto compara a la Antártida con una «gran biblioteca natural»?", ops: ["Porque en su hielo se conserva información sobre cómo era la atmósfera del pasado", "Porque allí se guardan libros muy antiguos", "Porque es un lugar tan silencioso como una biblioteca", "Porque solo pueden entrar científicos con permiso"], ok: 0, m: "El texto explica que en el hielo «quedaron atrapadas burbujas de aire antiquísimo» que permiten «reconstruir cómo era la atmósfera en el pasado»." },
      { q: "¿Cuál es la principal intención del autor al escribir este texto?", ops: ["Concientizar sobre la importancia de la Antártida y la necesidad de protegerla", "Convencer al lector de viajar de vacaciones a la Antártida", "Enseñar a construir una base científica en el hielo", "Contar una aventura de exploradores perdidos en el frío"], ok: 0, m: "A lo largo del texto el autor destaca el valor científico y ambiental de la Antártida y cierra pidiendo protegerla, así que busca concientizar, no invitar a viajar ni narrar una aventura." }
    ]
  },
  {
    texto: "A fines del siglo XIX y durante buena parte del XX, los trenes fueron el corazón que hacía latir a la Argentina. Miles de kilómetros de vías cruzaban el país de punta a punta, uniendo la ciudad más grande con el pueblo más pequeño y perdido de la llanura. Alrededor de cada estación crecía una comunidad: aparecían el almacén, la escuela, la plaza y las casas de los ferroviarios. Se decía, con razón, que muchos pueblos habían nacido gracias al tren. El ferrocarril no solo transportaba personas. Por sus vagones viajaban el trigo, el maíz y el ganado que hacían famosa a la Argentina en el mundo, y también las cartas, los diarios y las noticias que mantenían conectadas a familias separadas por enormes distancias. Para un chico de un pueblo del interior, ver llegar la locomotora, enorme y humeante, era uno de los espectáculos más impresionantes que podía imaginar. Sin embargo, a partir de la segunda mitad del siglo XX, muchos ramales empezaron a cerrar. Las razones fueron varias: el crecimiento de los camiones y los autos, la falta de inversión para mantener las vías y decisiones políticas que consideraron que ciertos trenes ya no eran rentables. En la década de 1990, el cierre se aceleró y cientos de estaciones quedaron abandonadas de un día para el otro. Las consecuencias fueron duras. Muchos pueblos que habían nacido y crecido alrededor de una estación se quedaron, literalmente, sin su motor. Sin tren, no llegaba el trabajo ni los visitantes, y numerosas familias tuvieron que mudarse a las ciudades. Hoy, quien recorre el interior argentino puede encontrar decenas de estaciones fantasma: edificios hermosos, con relojes detenidos y andenes vacíos donde ya no se detiene ningún tren. Es cierto que ningún país puede sostener servicios que nadie usa, y que el transporte cambió en todo el mundo. Pero vale la pena preguntarse si no se actuó con demasiada ligereza. Cerrar un ramal se hace en un día; reconstruir un pueblo que se quedó sin su razón de ser puede llevar generaciones, si es que se logra alguna vez. En los últimos años han surgido proyectos para reactivar algunos trenes, tanto de pasajeros como de carga. Recuperar el ferrocarril no significa volver al pasado, sino reconocer que fue, y podría volver a ser, una herramienta poderosa para integrar el país y darle vida a esos pueblos olvidados. La historia de nuestros trenes nos deja una enseñanza incómoda: a veces se destruye en poco tiempo aquello que costó décadas construir.",
    preguntas: [
      { q: "¿Cuál es la síntesis más completa del texto?", ops: ["El ferrocarril fue clave para poblar y conectar la Argentina, y su cierre perjudicó a muchos pueblos, por lo que valdría la pena recuperarlo", "Los trenes fueron reemplazados por los camiones porque eran más lentos y peligrosos", "La historia del ferrocarril demuestra que los pueblos del interior nunca necesitaron el tren", "Los trenes solo servían para transportar trigo, maíz y ganado al exterior"], ok: 0, m: "El texto recorre el auge del tren, las consecuencias de su cierre y termina defendiendo que recuperarlo «podría volver a ser una herramienta poderosa para integrar el país»." },
      { q: "¿Por qué el autor llama «estaciones fantasma» a esos edificios del interior?", ops: ["Porque quedaron abandonados y vacíos, sin trenes que se detengan", "Porque la gente cree que están embrujados", "Porque fueron construidos para asustar a los viajeros", "Porque son más antiguos que el resto del pueblo"], ok: 0, m: "El texto las describe como «edificios hermosos, con relojes detenidos y andenes vacíos donde ya no se detiene ningún tren», es decir, abandonados." },
      { q: "¿Cuál es la postura del autor sobre el cierre de los ramales?", ops: ["Reconoce que el transporte cambió, pero critica que se haya actuado con demasiada ligereza", "Cree que fue una decisión totalmente acertada y necesaria", "Sostiene que los trenes nunca deberían haber existido", "Piensa que los pueblos del interior no merecían tener tren"], ok: 0, m: "El autor admite que «ningún país puede sostener servicios que nadie usa», pero se pregunta «si no se actuó con demasiada ligereza» y defiende recuperar el ferrocarril." }
    ]
  },
  {
    texto: "Delfina odiaba los lunes, y ese lunes en particular parecía decidido a darle la razón. Se había quedado dormida, había perdido el colectivo y había llegado a la escuela con una prueba de matemática para la que no había estudiado lo suficiente. Cuando la profesora repartió las hojas, sintió que el estómago se le cerraba. En el banco de al lado estaba Rocío, la chica nueva, que había llegado al colegio hacía apenas dos semanas. Casi no hablaba con nadie y siempre parecía mirar todo desde una distancia prudente, como si esperara que en cualquier momento le pidieran que se fuera. Delfina nunca le había dirigido la palabra; no por mala, sino por esa costumbre tan común de no ver a quienes están un poco fuera del grupo. Durante la prueba, Delfina notó que Rocío resolvía los ejercicios con una rapidez asombrosa. Estuvo tentada de copiarle, pero algo la frenó. Al terminar la hora, mientras guardaban las cosas, se animó a decirle que había visto que se le daba muy bien la matemática. Rocío levantó la vista, sorprendida de que alguien le hablara, y respondió con una sonrisa tímida que en su escuela anterior era la que siempre ayudaba a los demás. Así, sin planearlo, empezó una costumbre. Los recreos que antes Rocío pasaba sola se transformaron en encuentros en los que le explicaba a Delfina esos temas que a ella se le hacían un nudo imposible. Pero lo que Delfina ganó no fue solamente aprender a despejar ecuaciones. Descubrió que Rocío tenía una manera muy suya de ver el mundo, que se reía de cosas insólitas y que sabía escuchar como pocos. Un mes después, cuando la profesora entregó las notas de la siguiente prueba, Delfina se encontró con un número que hacía tiempo no veía en sus carpetas. Pero, curiosamente, no fue eso lo que la puso más contenta. Al salir, Rocío la esperaba en la puerta, y ya no era la chica nueva que miraba todo de lejos: era, simplemente, su amiga. Esa tarde, mientras volvía a casa, Delfina pensó en lo cerca que había estado de no decirle nada a Rocío, de dejarla pasar como una desconocida más. Un gesto tan pequeño como reconocer lo que otro sabe hacer bien había cambiado el rumbo de dos personas. Se dio cuenta de algo que no iba a olvidar: muchas veces, las mejores cosas de la vida empiezan por animarse a mirar a quien nadie mira, y por tener el coraje de dar el primer paso.",
    preguntas: [
      { q: "¿Cuál es el mejor resumen del cuento?", ops: ["Delfina se anima a hablarle a una compañera nueva y, al hacerlo, gana una amiga y aprende el valor de incluir a los demás", "Delfina copia en una prueba de matemática y después se arrepiente", "Rocío ayuda a toda la clase a estudiar para un examen importante", "Delfina odia los lunes porque siempre le va mal en matemática"], ok: 0, m: "El relato muestra cómo un gesto de Delfina hacia Rocío las vuelve amigas; la enseñanza final es «animarse a mirar a quien nadie mira»." },
      { q: "¿Por qué Rocío se sorprendió cuando Delfina le habló?", ops: ["Porque casi nadie le dirigía la palabra y se sentía fuera del grupo", "Porque Delfina le había copiado en la prueba", "Porque no entendía bien el idioma", "Porque Delfina le hablaba en voz muy alta"], ok: 0, m: "El texto dice que Rocío «casi no hablaba con nadie» y se muestra «sorprendida de que alguien le hablara»." },
      { q: "¿Qué buscó transmitir principalmente el autor con este cuento?", ops: ["Que un pequeño gesto de acercamiento hacia quien está solo puede cambiar la vida de las personas", "Que estudiar matemática es la única forma de hacer amigos", "Que no hay que confiar en los compañeros nuevos", "Que los lunes son el peor día de la semana"], ok: 0, m: "El cierre del cuento señala que «las mejores cosas de la vida empiezan por animarse a mirar a quien nadie mira», que es el mensaje central." }
    ]
  },
  {
    texto: "Pasamos aproximadamente un tercio de nuestra vida durmiendo. Visto así, podría parecer una enorme pérdida de tiempo: horas y horas en las que no estudiamos, no jugamos ni producimos nada. Sin embargo, la ciencia demostró exactamente lo contrario. Dormir no es apagarse, sino todo lo opuesto: mientras descansamos, dentro de nuestro cuerpo y, sobre todo, de nuestro cerebro ocurre un trabajo intensísimo e imprescindible. Durante el sueño, el cerebro ordena y guarda lo que aprendimos en el día. Es como si, al final de la jornada, un bibliotecario invisible tomara todos los recuerdos desparramados y los acomodara en su lugar, decidiendo cuáles conservar y cuáles descartar. Por eso, un estudiante que duerme bien la noche antes de una prueba suele recordar mejor lo estudiado que otro que se quedó despierto repasando hasta la madrugada. Aunque parezca mentira, a veces se aprende más durmiendo que forzando el estudio sin descanso. El sueño también cumple una función reparadora. Mientras dormimos, el cuerpo produce sustancias que ayudan a crecer, fortalece las defensas contra las enfermedades y repara los tejidos gastados durante el día. Dormir poco, de manera repetida, se relaciona con problemas de memoria, mal humor, dificultad para concentrarse y hasta con enfermedades a largo plazo. Los adolescentes son un caso especial. Su reloj interno cambia y hace que naturalmente tengan sueño más tarde por la noche, pero al mismo tiempo necesitan dormir más horas que un adulto: entre ocho y diez para funcionar bien. El problema es que muchos se acuestan tarde, muchas veces con la pantalla del celular a pocos centímetros de la cara, y luego deben levantarse temprano para ir a la escuela. La luz de las pantallas, además, engaña al cerebro y le hace creer que todavía es de día, retrasando aún más el sueño. Frente a esto, conviene tomar el descanso tan en serio como cualquier otra tarea importante. No se trata de dormir por vagancia, sino de darle al cuerpo la herramienta que necesita para aprender, crecer y estar de buen humor. Apagar las pantallas un rato antes de acostarse, mantener horarios parecidos todos los días y crear un ambiente tranquilo son gestos sencillos que marcan una gran diferencia. Quizás deberíamos cambiar la idea de que dormir es tiempo perdido. En realidad, es una de las inversiones más inteligentes que podemos hacer con nuestras horas. Cada noche de buen sueño es una manera silenciosa de cuidarnos y de preparar el cuerpo y la mente para todo lo que vendrá al día siguiente. Dormir bien, lejos de ser una debilidad, es una de las formas más poderosas de estar despiertos.",
    preguntas: [
      { q: "¿Cuál es la idea central del texto?", ops: ["Dormir no es tiempo perdido, sino un proceso esencial para aprender, crecer y estar sanos", "Los adolescentes duermen demasiado y por eso les va mal en la escuela", "Estudiar hasta la madrugada es la mejor forma de aprobar una prueba", "El sueño sirve únicamente para descansar los músculos"], ok: 0, m: "El texto sostiene que durante el sueño ocurre «un trabajo intensísimo e imprescindible» y concluye que dormir «es una de las inversiones más inteligentes»." },
      { q: "¿Por qué un estudiante que duerme bien suele recordar mejor lo estudiado?", ops: ["Porque durante el sueño el cerebro ordena y guarda lo aprendido en el día", "Porque al dormir se olvida de los nervios", "Porque estudia más horas que los demás", "Porque el sueño borra los recuerdos difíciles"], ok: 0, m: "El texto compara al cerebro dormido con «un bibliotecario invisible» que acomoda los recuerdos «en su lugar»." },
      { q: "¿Con qué intención principal escribió el autor este texto?", ops: ["Convencer al lector de que valore el sueño y lo cuide como algo importante", "Explicar cómo se fabrican las camas más cómodas", "Contar la historia de un estudiante que no dormía", "Demostrar que los adultos duermen más que los chicos"], ok: 0, m: "El texto argumenta a favor de tomar el descanso «tan en serio como cualquier otra tarea importante» y da consejos para dormir mejor, así que busca convencer de valorarlo." }
    ]
  },
  {
    texto: "Cuando pensamos en personas que cambiaron el mundo, no siempre imaginamos a un médico nacido en un barrio de La Plata. Sin embargo, René Favaloro, hijo de un carpintero y una modista, llegó a ser uno de los cirujanos más importantes de la historia de la medicina. Su historia es la de alguien que unió el talento con una profunda convicción de que la ciencia debía estar al servicio de la gente. Favaloro se recibió de médico y, durante doce años, trabajó como médico rural en un pueblo pequeño de la provincia de La Pampa. Allí atendía de todo: partos, accidentes, enfermedades comunes. Esa experiencia le enseñó algo que nunca olvidaría: que la salud no debía ser un privilegio de pocos. Con el tiempo, sintió que necesitaba formarse más y viajó a los Estados Unidos, a una clínica famosa, donde se dedicó a estudiar el corazón. Fue allí donde, a fines de la década de 1960, desarrolló una técnica que salvaría millones de vidas: el bypass coronario. En términos sencillos, la operación consiste en tomar un pequeño vaso sanguíneo de otra parte del cuerpo y usarlo para crear un desvío que lleve la sangre más allá de una arteria del corazón que está tapada. Gracias a ese procedimiento, personas que antes estaban condenadas a morir por problemas cardíacos pudieron seguir viviendo durante muchos años. Con la fama y el prestigio ganados, Favaloro podría haberse quedado en el exterior, trabajando cómodamente y ganando mucho dinero. Pero tomó una decisión que sorprendió a muchos: volver a la Argentina. Quería que los avances de la medicina llegaran también a su país y soñaba con formar a nuevos médicos. Fundó una institución dedicada a la investigación, la enseñanza y la atención de pacientes, sin importar si podían pagar o no. Su vida, sin embargo, no tuvo un final feliz. Las dificultades económicas de su fundación y la falta de apoyo lo llevaron a una situación desesperante, y en el año 2000 murió en medio de esa angustia. Su muerte conmocionó al país y dejó una pregunta incómoda: cómo era posible que alguien que había dado tanto se sintiera tan solo. Recordar a Favaloro no debería ser solamente rendir homenaje a un gran científico. Su historia nos interpela y nos obliga a preguntarnos qué clase de sociedad queremos ser: una que sostiene a quienes trabajan por el bien común, o una que los abandona. Su legado, hecho de conocimiento y de generosidad, sigue latiendo, como un corazón al que él le enseñó a seguir andando.",
    preguntas: [
      { q: "¿Cuál es la mejor síntesis del texto?", ops: ["Favaloro fue un médico brillante que puso la ciencia al servicio de la gente, y su historia nos hace reflexionar sobre cómo tratamos a quienes trabajan por el bien común", "Favaloro inventó el bypass para hacerse rico en los Estados Unidos", "Favaloro fue un carpintero que se hizo famoso en La Plata", "La principal enseñanza de Favaloro es que hay que estudiar en el exterior"], ok: 0, m: "El texto recorre su vocación de servicio, su invento y su regreso al país, y cierra preguntando qué sociedad queremos ser; además, Favaloro resignó comodidad y dinero." },
      { q: "¿Por qué Favaloro decidió volver a la Argentina en lugar de quedarse en el exterior?", ops: ["Porque quería que los avances de la medicina llegaran a su país y formar nuevos médicos", "Porque en los Estados Unidos no lo dejaban operar", "Porque en su país le pagaban mucho más dinero", "Porque no había logrado desarrollar el bypass afuera"], ok: 0, m: "El texto dice que «quería que los avances de la medicina llegaran también a su país y soñaba con formar a nuevos médicos»." },
      { q: "¿Cuál es la intención del autor en el cierre del texto?", ops: ["Invitar al lector a reflexionar sobre cómo la sociedad trata a quienes trabajan por el bien común", "Explicar paso a paso cómo se realiza una operación de corazón", "Convencer al lector de estudiar medicina en el exterior", "Demostrar que los médicos rurales ganan poco dinero"], ok: 0, m: "El cierre dice que su historia «nos obliga a preguntarnos qué clase de sociedad queremos ser», así que busca la reflexión, no explicar la cirugía." }
    ]
  },
  {
    texto: "Todos los días, sin darnos cuenta, recibimos cientos de mensajes que buscan convencernos de comprar algo. Están en la televisión, en los carteles de la calle, en los videos de internet e incluso escondidos dentro de los juegos del celular. La publicidad se volvió tan común que muchas veces ni siquiera notamos que está ahí, trabajando sobre nuestros deseos. Y, sin embargo, entender cómo funciona es una de las herramientas más útiles que podemos tener hoy. El objetivo de un aviso publicitario no es informarnos, sino hacernos sentir algo. Rara vez una propaganda de gaseosa habla de lo que la bebida realmente contiene; en cambio, nos muestra a un grupo de jóvenes riéndose, disfrutando de un día perfecto en la playa. El mensaje oculto es sencillo: si comprás este producto, vas a ser feliz y vas a pertenecer a ese grupo. La publicidad no vende objetos, vende la promesa de una vida mejor. Los chicos y adolescentes son un público especialmente buscado por las marcas, y no por casualidad. Se sabe que las costumbres que se forman en la infancia suelen durar toda la vida, así que ganar un cliente joven es ganarlo, muchas veces, para siempre. Por eso muchos productos usan colores llamativos, personajes de dibujos animados o influencers que los chicos admiran. Nada de esto significa que la publicidad sea, en sí misma, algo malo. Gracias a ella nos enteramos de productos y servicios que pueden sernos útiles, y muchas actividades que disfrutamos gratis se financian con avisos. El problema no es que exista, sino creer todo lo que nos dice sin cuestionarlo. Aquí es donde aparece una habilidad fundamental: el pensamiento crítico. Se trata de aprender a mirar cada mensaje y preguntarse quién lo hizo, para qué, y qué es lo que en realidad me están tratando de vender. ¿Necesito de verdad este producto o simplemente me hicieron sentir que lo necesito? ¿Es cierto lo que promete o es solo una imagen atractiva? Formar esa mirada atenta no nos vuelve desconfiados ni amargados; al contrario, nos hace más libres. Una persona que entiende cómo funciona la publicidad puede elegir con la cabeza y no solo con la emoción del momento. Puede disfrutar de un buen aviso, reírse de él, e incluso admirar su ingenio, sin dejar que decida por ella. En un mundo que nos empuja a comprar todo el tiempo, aprender a preguntar antes de creer es casi un acto de rebeldía. Y esa rebeldía, la de pensar por uno mismo, es tal vez una de las cosas más valiosas que la escuela y la familia pueden ayudarnos a cultivar.",
    preguntas: [
      { q: "¿Cuál es la idea central del texto?", ops: ["Conviene desarrollar pensamiento crítico para entender la publicidad y no dejar que decida por nosotros", "Toda la publicidad es mentirosa y habría que prohibirla", "La publicidad siempre informa con exactitud sobre los productos", "Los chicos no deberían mirar televisión ni usar el celular"], ok: 0, m: "El texto aclara que el problema no es que la publicidad exista, sino «creer todo lo que nos dice sin cuestionarlo», y defiende el pensamiento crítico." },
      { q: "Según el texto, ¿por qué una propaganda de gaseosa muestra jóvenes felices en la playa en vez de hablar del producto?", ops: ["Porque busca hacernos sentir que, al comprarlo, seremos felices y parte de ese grupo", "Porque la playa es el mejor lugar para tomar gaseosa", "Porque no le permiten mostrar el producto por ley", "Porque los jóvenes son los únicos que compran gaseosa"], ok: 0, m: "El texto explica que «la publicidad no vende objetos, vende la promesa de una vida mejor» y que el mensaje oculto es que serás feliz y pertenecerás al grupo." },
      { q: "¿Cuál es la principal intención del autor?", ops: ["Enseñar al lector a analizar la publicidad con espíritu crítico antes de creerle", "Recomendar las mejores marcas de gaseosa del mercado", "Convencer al lector de que nunca compre nada", "Explicar cómo se filma un aviso publicitario"], ok: 0, m: "El autor cierra afirmando que «aprender a preguntar antes de creer» es valioso y quiere que el lector piense por sí mismo, no que deje de comprar ni que aprenda a filmar avisos." }
    ]
  }
];

// Comprensión lectora ESCALADA POR GRADO (docs/auditoria-dc-caba/): hasta ahora
// los 5 grados (3°-7°) usaban el MISMO banco de 4 textos cortos → se quemaba en 1
// sesión + la regresión 5°→6° (6° debe leer textos largos, ≥350 palabras). Ahora
// cada grado tiene su banco, con textos y preguntas que crecen en longitud y
// dificultad (literal → inferencia → idea principal / hecho-vs-opinión / crítica).
// Los COMPRENSION_N los define el bloque de contenido de abajo.
function comprensionBanco(edad) {
  const porGrado = { 7: COMPRENSION_2, 8: COMPRENSION_3, 9: COMPRENSION_4, 10: COMPRENSION_5, 11: COMPRENSION_6, 12: COMPRENSION_7 };
  return porGrado[edad | 0] || COMPRENSION_3;
}

GAMES.comprension_lectora = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 8;
    ctx.rondas(rondas);
    const BANCO = comprensionBanco(D.edad);   // banco del grado del token
    let ronda = 0, usados = [], pIdx = -1, qi = 0;
    const nuevoPasaje = () => {
      let disp = BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!disp.length) { usados = []; disp = BANCO.map((_, i) => i); }
      pIdx = disp[rint(0, disp.length - 1)]; usados.push(pIdx); qi = 0;
    };
    const render = () => {
      ctx.ronda(ronda);
      const pasaje = BANCO[pIdx];
      const preg = pasaje.preguntas[qi];
      ctx.item("comprension#" + pIdx + "_" + qi);
      ctx.consigna(preg.q);
      ctx.juego.innerHTML = "";
      const box = el("div", "");
      box.style.cssText = "max-width:600px;margin:0 auto 14px;padding:14px 16px;background:rgba(140,140,160,.12);border-radius:12px;font-size:17px;line-height:1.5;text-align:left";
      box.textContent = pasaje.texto;
      ctx.juego.appendChild(box);
      const opts = preg.ops.map((t, i) => ({ t: t, ok: i === preg.ok, m: preg.m }));
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opts).forEach((o) => {
        const b = el("button", "op", o.t);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) {
            resuelto = true; b.classList.add("anim-pop"); ctx.bien();
            ronda++; qi++;
            await espera(950);
            if (ronda >= rondas) { ctx.win(); return; }
            if (qi >= pasaje.preguntas.length) nuevoPasaje();
            render();
          } else {
            b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450);
            ctx.casi(o.m);
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    nuevoPasaje(); render();
  },
};

/* ── REPARTO CON RESTO (M11, 3° grado — docs/auditoria-dc-caba/grado-3.md): la
   división con resto, EL nodal que estrena 3° y define el pasaje al 2° ciclo.
   Trivia generada: repartir en partes iguales, decir cuántos a cada uno Y cuántos
   sobran. Distractores por misconception real (Capa 0 · C4): resto mayor que la
   cantidad de amigos (imposible), uno de más, ignorar el resto. Explicación C3. ── */
GAMES.reparto_con_resto = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    const OBJ = [["🍬", "caramelos"], ["🍪", "galletitas"], ["⚽", "pelotas"], ["🎈", "globos"], ["🖍️", "crayones"]];
    const fmt = (c, r) => c + " a cada uno" + (r > 0 ? ", sobran " + r : ", no sobra nada");
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const prog = rondas > 1 ? ronda / (rondas - 1) : 1;
      const N = rint(2, prog > 0.5 ? 6 : 4);          // amigos = divisor
      const coc = rint(2, prog > 0.5 ? 9 : 5);        // a cada uno = cociente
      const resto = rint(0, N - 1);                    // sobran (siempre < amigos)
      const total = N * coc + resto;
      const obj = OBJ[rint(0, OBJ.length - 1)];
      ctx.item("reparto_resto#" + total + "e" + N);
      ctx.consigna("Reparto " + total + " " + obj[1] + " " + obj[0] + " entre " + N + " amigos, en partes iguales. ¿Cuántos a cada uno y cuántos sobran?");
      ctx.juego.innerHTML = "";
      const correcto = fmt(coc, resto);
      const cand = [
        { t: fmt(coc, resto + N), m: "Si sobran " + (resto + N) + " y hay " + N + " amigos, se puede dar uno más a cada uno. El resto tiene que ser MENOR que " + N + "." },
        { t: fmt(coc + 1, resto), m: (coc + 1) + " a cada uno serían " + ((coc + 1) * N) + ", y hay solo " + total + "." },
        { t: (resto > 0 ? fmt(coc, 0) : fmt(coc - 1, N - 1)), m: (resto > 0 ? total + " no se reparte justo entre " + N + ": sobran " + resto + "." : "Se reparte justo: " + coc + " a cada uno, no sobra nada.") },
      ];
      const opciones = [{ t: correcto, ok: true }];
      shuffle(cand).forEach((d) => { if (opciones.length < 3 && !opciones.some((o) => o.t === d.t)) opciones.push(d); });
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", o.t);
        b.style.cssText = "text-align:left";
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(1000); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── TRES EN FILA (M2, 3° grado): leer, comparar y ordenar números de 3-4 cifras.
   Consigna rotativa (mayor / menor / el del medio) sobre 3 numerales. Ataca la
   trampa de comparar por "cuántos números tiene" o la primera cifra. Explicación
   C3: contar cifras primero, después comparar de izquierda a derecha. ── */
GAMES.comparar_numeros = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    const fmt = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const prog = rondas > 1 ? ronda / (rondas - 1) : 1;
      const topeMax = ctx.cfg.max || 9999;                 // 3° default 4 cifras; 1°=20, 2°=999
      const maxN = prog > 0.5 ? topeMax : Math.max(9, Math.round(topeMax / 10));
      const minN = Math.max(1, Math.round(topeMax / (prog > 0.5 ? 100 : 1000)));
      let nums = [];
      while (nums.length < 3) { const x = rint(minN, maxN); if (!nums.includes(x)) nums.push(x); }
      const sorted = [...nums].sort((a, b) => a - b);
      const modo = rint(0, 2);
      const correctoVal = modo === 0 ? sorted[2] : (modo === 1 ? sorted[0] : sorted[1]);
      const preg = modo === 0 ? "¿Cuál es el MAYOR?" : (modo === 1 ? "¿Cuál es el MENOR?" : "¿Cuál está en el MEDIO?");
      ctx.item("comparar#" + modo + "_" + correctoVal);
      ctx.consigna(preg);
      ctx.juego.innerHTML = "";
      const motivo = "Fijate primero cuántas cifras tiene cada número; si tienen las mismas, compará cifra por cifra desde la izquierda.";
      const opciones = nums.map((n) => ({ v: n, ok: n === correctoVal }));
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", fmt(o.v));
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(motivo); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ESTADOS DE LA MATERIA (C1, 3° grado): clasificar sólido / líquido / gaseoso.
   El gaseoso es lo NUEVO de 3° (2° trabaja sólido/líquido). Reemplaza a
   separador_mezclas. Explicación C3 con la propiedad de cada estado. ── */
const ESTADOS_BANCO = [
  { cosa: "El hielo 🧊", r: "Sólido" }, { cosa: "El agua del vaso 💧", r: "Líquido" }, { cosa: "El vapor de la pava ♨️", r: "Gaseoso" },
  { cosa: "Una piedra 🪨", r: "Sólido" }, { cosa: "La leche 🥛", r: "Líquido" }, { cosa: "El aire 💨", r: "Gaseoso" },
  { cosa: "Un bloque de madera 🧱", r: "Sólido" }, { cosa: "El jugo 🧃", r: "Líquido" }, { cosa: "El humo 🌫️", r: "Gaseoso" },
  { cosa: "Una moneda 🪙", r: "Sólido" }, { cosa: "El aceite 🫗", r: "Líquido" }, { cosa: "Las burbujas de aire 🫧", r: "Gaseoso" },
];
GAMES.estados_materia = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    const OPC = ["Sólido", "Líquido", "Gaseoso"];
    const EXPL = {
      "Sólido": "Los sólidos tienen forma propia y no se derraman (como el hielo o una piedra).",
      "Líquido": "Los líquidos toman la forma del recipiente y se pueden verter (como el agua o el jugo).",
      "Gaseoso": "Los gases no tienen forma y se esparcen por el aire (como el vapor o el humo).",
    };
    let usados = [], ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = ESTADOS_BANCO.filter((x) => !usados.includes(x.cosa));
      if (!disp.length) { usados = []; disp = ESTADOS_BANCO.slice(); }
      const it = disp[rint(0, disp.length - 1)]; usados.push(it.cosa);
      ctx.item("estados#" + it.r);
      ctx.consigna(it.cosa + ", ¿en qué estado está?");
      ctx.juego.innerHTML = "";
      const opciones = OPC.map((o) => ({ t: o, ok: o === it.r }));
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", o.t);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(EXPL[it.r]); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── EL CONECTOR JUSTO (L16, 5° grado — docs/auditoria-dc-caba/grado-5.md):
   completar una oración con el conector correcto (cloze). Nodal de 5° señalado
   por la maestra. Distractores = otros conectores que CAMBIAN el sentido; la
   explicación dice qué relación marca el correcto (Capa 0 · C3). ── */
const CONECTORES_BANCO = [
  { f: "Quería salir a jugar … estaba lloviendo.", ok: "pero", d: ["porque", "así que"], m: "«pero» marca oposición: querés algo y aparece un obstáculo." },
  { f: "Me quedé adentro … estaba lloviendo.", ok: "porque", d: ["pero", "aunque"], m: "«porque» da la causa: la lluvia es el motivo." },
  { f: "Estudió toda la semana, … aprobó.", ok: "por eso", d: ["pero", "aunque"], m: "«por eso» marca la consecuencia de estudiar." },
  { f: "Salió a la calle … hacía mucho frío.", ok: "aunque", d: ["porque", "por eso"], m: "«aunque» = algo pasa A PESAR de un obstáculo (el frío)." },
  { f: "Es muy inteligente; …, no le gusta estudiar.", ok: "sin embargo", d: ["por eso", "porque"], m: "«sin embargo» contrasta: algo y otra cosa que no encaja." },
  { f: "Llegó tarde … perdió el colectivo.", ok: "porque", d: ["aunque", "sin embargo"], m: "«porque» da la causa de llegar tarde." },
  { f: "Practicó mucho, … todavía le cuesta.", ok: "pero", d: ["por eso", "porque"], m: "«pero» contrasta el esfuerzo con el resultado." },
  { f: "Terminó de comer … se lavó los dientes.", ok: "y después", d: ["pero", "porque"], m: "«y después» ordena en el tiempo: primero una cosa, luego la otra." },
  { f: "No trajo paraguas, … se mojó toda.", ok: "así que", d: ["aunque", "sin embargo"], m: "«así que» marca la consecuencia de no traer paraguas." },
  { f: "Le gustan los perros … les tiene un poco de miedo.", ok: "aunque", d: ["porque", "por eso"], m: "«aunque» = le gustan A PESAR del miedo." },
  { f: "Se hizo de noche, … encendieron las luces.", ok: "entonces", d: ["pero", "aunque"], m: "«entonces» marca qué pasó como consecuencia." },
  { f: "El equipo jugó bien, … perdió el partido.", ok: "sin embargo", d: ["porque", "por eso"], m: "«sin embargo» contrasta: jugó bien y aun así perdió." },
  // ampliado 20-jul-2026 (de 12 a 24 — engrosar bancos nodales, docs/auditoria-dc-caba/)
  { f: "Tenía mucho sueño, … me fui a dormir.", ok: "así que", d: ["pero", "aunque"], m: "«así que» marca la consecuencia de tener sueño." },
  { f: "Ahorró todo el año, … se compró la bici.", ok: "por eso", d: ["pero", "aunque"], m: "«por eso» une el ahorro con su consecuencia." },
  { f: "Sabía la respuesta, … no la dijo.", ok: "pero", d: ["porque", "por eso"], m: "«pero» contrasta: la sabía y aun así no la dijo." },
  { f: "Llegó tarde … había mucho tránsito.", ok: "porque", d: ["aunque", "sin embargo"], m: "«porque» da la causa de llegar tarde." },
  { f: "No estudió nada; …, aprobó igual.", ok: "sin embargo", d: ["por eso", "así que"], m: "«sin embargo» contrasta lo esperado con lo que pasó." },
  { f: "Le gusta el fútbol … nunca fue a la cancha.", ok: "aunque", d: ["porque", "por eso"], m: "«aunque» = le gusta A PESAR de no haber ido nunca." },
  { f: "Primero ordenó su cuarto … salió a jugar.", ok: "y después", d: ["porque", "aunque"], m: "«y después» ordena en el tiempo: primero una cosa, luego la otra." },
  { f: "Estaba cansado, … siguió trabajando.", ok: "pero", d: ["por eso", "así que"], m: "«pero» contrasta el cansancio con seguir trabajando." },
  { f: "Se cortó la luz, … encendimos velas.", ok: "así que", d: ["aunque", "sin embargo"], m: "«así que» marca lo que hicimos como consecuencia." },
  { f: "Practica todos los días, … todavía no le sale.", ok: "pero", d: ["por eso", "porque"], m: "«pero» contrasta el esfuerzo con el resultado." },
  { f: "Hacía mucho calor, … abrimos las ventanas.", ok: "por eso", d: ["aunque", "pero"], m: "«por eso» marca la consecuencia del calor." },
  { f: "Quería salir a andar en bici, … se le pinchó la rueda.", ok: "pero", d: ["así que", "porque"], m: "«pero» marca el obstáculo que apareció." },
];
/* ── Subconjunto de conectores para 4° grado (docs/auditoria-dc-caba/grado-4.md,
   gap #3 de Lengua). Solo los que el DC pide en 4°: temporales (y después…),
   causales (porque, por eso, así que) y la oposición simple (pero). SIN
   adversativos cargados (aunque, sin embargo), que quedan para 5°+. Los distractores
   también son del set simple, así no aparecen conectores que el chico no vio. ── */
const CONECTORES4_BANCO = [
  { f: "Primero me puse las medias … las zapatillas.", ok: "y después", d: ["porque", "pero"], m: "«y después» ordena en el tiempo: una cosa y luego la otra." },
  { f: "Me quedé en casa … llovía mucho.", ok: "porque", d: ["y después", "pero"], m: "«porque» da la causa: la lluvia es el motivo." },
  { f: "Estudié un montón, … me saqué un diez.", ok: "por eso", d: ["porque", "pero"], m: "«por eso» marca la consecuencia de estudiar." },
  { f: "Terminé la tarea … salí a jugar.", ok: "y después", d: ["porque", "por eso"], m: "«y después» ordena: primero la tarea, luego el juego." },
  { f: "Quería helado, … no había en la heladera.", ok: "pero", d: ["porque", "así que"], m: "«pero» marca oposición: querías algo y aparece un obstáculo." },
  { f: "Se largó a llover, … abrimos los paraguas.", ok: "así que", d: ["porque", "pero"], m: "«así que» marca la consecuencia de que llueva." },
  { f: "No desayunó, … al mediodía tenía mucha hambre.", ok: "por eso", d: ["pero", "y después"], m: "«por eso» une la causa (no desayunar) con su consecuencia." },
  { f: "Me lavé las manos … me senté a comer.", ok: "y después", d: ["porque", "pero"], m: "«y después» ordena en el tiempo las dos acciones." },
  { f: "Ganamos el partido … practicamos toda la semana.", ok: "porque", d: ["pero", "y después"], m: "«porque» da la causa de haber ganado." },
  { f: "Hacía mucho calor, … prendimos el ventilador.", ok: "así que", d: ["porque", "pero"], m: "«así que» marca lo que hicimos como consecuencia del calor." },
];
GAMES.conectores = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    // nivel 1 (4°): subconjunto simple (temporales, causales, «pero»). nivel 2+
    // (5°-7°, default): banco completo, con adversativos (aunque, sin embargo).
    const banco = (ctx.cfg.nivel || 2) <= 1 ? CONECTORES4_BANCO : CONECTORES_BANCO;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = banco.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!disp.length) { usados = []; disp = banco.map((_, i) => i); }
      const idx = disp[rint(0, disp.length - 1)]; usados.push(idx);
      const it = banco[idx];
      ctx.item("conector#" + idx);
      ctx.consigna("Completá: " + it.f);
      ctx.juego.innerHTML = "";
      const opciones = shuffle([{ t: it.ok, ok: true }].concat(it.d.map((x) => ({ t: x, ok: false }))));
      const fila = el("div", "ops");
      fila.setAttribute("data-ok", it.ok);
      let resuelto = false;
      opciones.forEach((o) => {
        const b = el("button", "op", o.t);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(it.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ORDENÁ LOS NÚMEROS (1°/2° grado — docs/auditoria-dc-caba/): ordenar de menor
   a mayor, con la mecánica ORDENAR (tocar en orden, commit-then-check). Rango y
   cantidad por cfg (1°: 3 números ≤20; 2°: 4 números ≤100). Escala a grados
   mayores subiendo cfg.max/cfg.cant. Explicación C3 al errar. ── */
GAMES.ordenar_numeros = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    const cant = ctx.cfg.cant || 3;
    const max = ctx.cfg.max || 20;
    const fmt = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    ctx.rondas(rondas);
    let ronda = 0;
    const render = () => {
      ctx.ronda(ronda);
      ctx.consigna("Ordená de MENOR a MAYOR. Tocá los números en orden.");
      ctx.juego.innerHTML = "";
      let nums = [];
      while (nums.length < cant) { const x = rint(1, max); if (!nums.includes(x)) nums.push(x); }
      const correcto = nums.slice().sort((a, b) => a - b);
      ctx.item("ordnum#" + correcto.join("_"));
      const mezcla = shuffle(correcto.map((n, i) => ({ n: n, pos: i })));
      const seq = [];
      const cont = el("div", "");
      cont.style.cssText = "display:flex;flex-wrap:wrap;gap:12px;justify-content:center;max-width:520px;margin:0 auto";
      const chequear = () => {
        const ok = seq.every((p, k) => p === k);
        if (ok) { ctx.bien(); ronda++; setTimeout(() => { if (ronda >= rondas) ctx.win(); else render(); }, 1100); }
        else { ctx.casi("Buscá primero el más CHICO, después el que sigue, hasta el más grande."); setTimeout(render, 2000); }
      };
      mezcla.forEach((o) => {
        const b = el("button", "op", fmt(o.n));
        b.style.cssText = "min-width:74px;font-size:23px;position:relative";
        b.addEventListener("click", () => {
          if (b.dataset.puesto) return;
          seq.push(o.pos);
          b.dataset.puesto = String(seq.length);
          b.style.opacity = "0.55";
          const badge = el("span", "", String(seq.length));
          badge.style.cssText = "position:absolute;right:-6px;top:-6px;background:#2b2b3a;color:#fff;border-radius:50%;width:24px;height:24px;display:grid;place-items:center;font-size:13px;font-weight:700";
          b.appendChild(badge);
          if (seq.length === correcto.length) chequear();
        });
        cont.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(cont);
    };
    render();
  },
};

/* ── EQUIVALENCIAS DE MEDIDA (M17, 5° grado — docs/auditoria-dc-caba/grado-5.md):
   nodal que estrena 5° (gap señalado por maestra y auditor). Convertir unidades
   (m↔cm, km↔m, kg↔g, l↔ml…). GENERADA. Distractores por misconception: cantidad
   de ceros equivocada. Explicación con la equivalencia base (Capa 0 · C3). ── */
GAMES.equivalencias_medida = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    const CONV = [
      { u1: "metro", u1p: "metros", u2: "centímetros", f: 100 },
      { u1: "kilómetro", u1p: "kilómetros", u2: "metros", f: 1000 },
      { u1: "kilo", u1p: "kilos", u2: "gramos", f: 1000 },
      { u1: "litro", u1p: "litros", u2: "mililitros", f: 1000 },
      { u1: "metro", u1p: "metros", u2: "milímetros", f: 1000 },
      { u1: "centímetro", u1p: "centímetros", u2: "milímetros", f: 10 },
    ];
    const fmt = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const c = CONV[rint(0, CONV.length - 1)];
      const N = rint(1, 9);
      const correcto = N * c.f;
      ctx.item("medida#" + N + "_" + c.u1 + "_" + c.u2);
      ctx.consigna("¿Cuántos " + c.u2 + " hay en " + N + " " + (N === 1 ? c.u1 : c.u1p) + "?");
      ctx.juego.innerHTML = "";
      const cand = [
        { v: N * (c.f / 10), m: "Faltan ceros: 1 " + c.u1 + " son " + fmt(c.f) + " " + c.u2 + "." },
        { v: N * (c.f * 10), m: "Sobra un cero: 1 " + c.u1 + " son " + fmt(c.f) + " " + c.u2 + "." },
      ];
      if (N > 1) cand.push({ v: c.f, m: "Eso es 1 " + c.u1 + ". Acá son " + N + ": multiplicá por " + N + "." });
      const opciones = [{ v: correcto, ok: true }];
      shuffle(cand).forEach((d) => { if (opciones.length < 3 && d.v > 0 && d.v !== correcto && !opciones.some((o) => o.v === d.v)) opciones.push(d); });
      let intento = 0;
      while (opciones.length < 3 && intento++ < 20) { const v = correcto * (rint(2, 4)); if (!opciones.some((o) => o.v === v)) opciones.push({ v: v, m: "1 " + c.u1 + " son " + fmt(c.f) + " " + c.u2 + "." }); }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", fmt(o.v));
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿CANTÓ O CANTABA? (L15, 5° grado — docs/auditoria-dc-caba/grado-5.md): pretérito
   perfecto simple vs. imperfecto en la narración (la traba n°1 al escribir cuentos,
   gap de la maestra). Cloze: completar con la forma correcta. Explicación con la
   regla (Capa 0 · C3). ── */
const VERBOS_PASADO_BANCO = [
  { f: "Todos los veranos … a la playa con mis abuelos.", ok: "íbamos", d: "fuimos", m: "El imperfecto (íbamos) es para algo que pasaba SIEMPRE, una costumbre." },
  { f: "Ayer … al cine una sola vez.", ok: "fui", d: "iba", m: "El perfecto (fui) es para algo que pasó UNA vez y terminó." },
  { f: "Cuando era chico, … con autitos.", ok: "jugaba", d: "jugué", m: "El imperfecto (jugaba) describe una costumbre del pasado." },
  { f: "El sábado pasado … un gol en el partido.", ok: "metí", d: "metía", m: "El perfecto (metí) es una acción puntual que terminó." },
  { f: "La abuela … tortas todos los domingos.", ok: "hacía", d: "hizo", m: "El imperfecto (hacía) es para lo habitual, lo de siempre." },
  { f: "De golpe … un ruido y todos se asustaron.", ok: "sonó", d: "sonaba", m: "El perfecto (sonó) marca algo que pasó de repente y terminó." },
  { f: "Antes … en una casa con jardín.", ok: "vivíamos", d: "vivimos", m: "El imperfecto (vivíamos) describe cómo era la vida antes." },
  { f: "El lunes … temprano para el examen.", ok: "estudié", d: "estudiaba", m: "El perfecto (estudié) es una acción concreta de un día." },
  { f: "Mientras llovía, nosotros … adentro tranquilos.", ok: "jugábamos", d: "jugamos", m: "El imperfecto (jugábamos) es la acción de fondo mientras pasaba otra cosa." },
  { f: "Esa mañana … el sol y salimos a pasear.", ok: "salió", d: "salía", m: "El perfecto (salió) es un hecho puntual de esa mañana." },
  { f: "Todas las noches mi mamá me … un cuento.", ok: "leía", d: "leyó", m: "El imperfecto (leía) es una costumbre repetida." },
  { f: "Cuando terminó la película, … las luces.", ok: "encendieron", d: "encendían", m: "El perfecto (encendieron) es lo que pasó al terminar, una vez." },
];
GAMES.verbos_pasado = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = VERBOS_PASADO_BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!disp.length) { usados = []; disp = VERBOS_PASADO_BANCO.map((_, i) => i); }
      const idx = disp[rint(0, disp.length - 1)]; usados.push(idx);
      const it = VERBOS_PASADO_BANCO[idx];
      ctx.item("verbopas#" + idx);
      ctx.consigna("Completá: " + it.f);
      ctx.juego.innerHTML = "";
      const opciones = shuffle([{ t: it.ok, ok: true }, { t: it.d, ok: false }]);
      const fila = el("div", "ops");
      let resuelto = false;
      opciones.forEach((o) => {
        const b = el("button", "op", o.t);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(it.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── MI BUENOS AIRES QUERIDO (S9, 5° grado — docs/auditoria-dc-caba/grado-5.md):
   la ciudad — Plaza de Mayo, Cabildo, Casa Rosada, barrios (gap señalado por la
   maestra: la salida al Cabildo se hace todos los años). Trivia con explicación
   (Capa 0 · C3). ── */
const BUENOS_AIRES_BANCO = [
  { q: "¿Dónde se reunió el primer gobierno patrio en 1810?", ok: "El Cabildo", d: ["El Obelisco", "La Bombonera"], m: "En el Cabildo se formó la Primera Junta, el 25 de mayo de 1810." },
  { q: "¿Dónde trabaja hoy el presidente de la Argentina?", ok: "La Casa Rosada", d: ["El Cabildo", "El Congreso"], m: "La Casa Rosada, frente a la Plaza de Mayo, es la sede del gobierno." },
  { q: "¿Qué monumento alto está en el centro, sobre la 9 de Julio?", ok: "El Obelisco", d: ["El Cabildo", "La Catedral"], m: "El Obelisco se levantó en 1936 en la avenida 9 de Julio." },
  { q: "¿Cómo se llama la plaza principal, frente a la Casa Rosada?", ok: "Plaza de Mayo", d: ["Plaza Francia", "Plaza Italia"], m: "La Plaza de Mayo es el corazón histórico de la Ciudad." },
  { q: "¿Qué río tiene Buenos Aires en su costa?", ok: "El Río de la Plata", d: ["El Paraná", "El río Uruguay"], m: "Buenos Aires está a orillas del Río de la Plata." },
  { q: "¿En qué barrio están las casas de colores y el Caminito?", ok: "La Boca", d: ["Palermo", "Recoleta"], m: "La Boca, con sus casas de chapa pintadas, fue un barrio de inmigrantes junto al Riachuelo." },
  { q: "El Cabildo, en la época colonial, ¿qué era?", ok: "Como la municipalidad", d: ["Una iglesia", "Un mercado"], m: "El Cabildo era el gobierno de la ciudad en la colonia." },
  { q: "¿Qué edificio religioso está al lado de la Plaza de Mayo?", ok: "La Catedral", d: ["El Cabildo", "El Obelisco"], m: "En la Catedral Metropolitana descansan los restos de San Martín." },
  { q: "Las Madres de Plaza de Mayo, ¿dónde caminan cada jueves?", ok: "Alrededor de la Pirámide de Mayo", d: ["En el Obelisco", "En La Boca"], m: "Las Madres marchan alrededor de la Pirámide, en la Plaza de Mayo." },
  { q: "¿Cómo llegaron muchas familias a Buenos Aires hace 100 años?", ok: "En barco, como inmigrantes", d: ["En avión", "En tren desde el sur"], m: "A fines del 1800 y principios del 1900 llegaron muchos inmigrantes en barco por el puerto." },
];
GAMES.buenos_aires = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = BUENOS_AIRES_BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!disp.length) { usados = []; disp = BUENOS_AIRES_BANCO.map((_, i) => i); }
      const idx = disp[rint(0, disp.length - 1)]; usados.push(idx);
      const it = BUENOS_AIRES_BANCO[idx];
      ctx.item("baires#" + idx);
      ctx.consigna(it.q);
      ctx.juego.innerHTML = "";
      const opciones = shuffle([{ t: it.ok, ok: true }].concat(it.d.map((x) => ({ t: x, ok: false }))));
      const fila = el("div", "ops");
      let resuelto = false;
      opciones.forEach((o) => {
        const b = el("button", "op", o.t);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(it.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿CUÁL ES PRIMO? (M2, 6° grado — docs/auditoria-dc-caba/grado-6.md): primos y
   compuestos, nodal de 6°. Elegir el primo entre 3 números; los distractores son
   compuestos y la explicación NOMBRA un divisor (Capa 0 · C3/C4). ── */
function _esPrimo(n) { if (n < 2) return false; for (let i = 2; i * i <= n; i++) if (n % i === 0) return false; return true; }
GAMES.numeros_primos = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let p; do { p = rint(2, 47); } while (!_esPrimo(p));
      const opciones = [{ v: p, ok: true }];
      let intento = 0;
      while (opciones.length < 3 && intento++ < 60) {
        const c = rint(4, 60);
        if (!_esPrimo(c) && !opciones.some((o) => o.v === c)) {
          let d = 2; while (c % d !== 0) d++;
          opciones.push({ v: c, ok: false, m: c + " es compuesto: se divide por " + d + " (" + d + "×" + (c / d) + "). El primo solo se divide por 1 y por sí mismo." });
        }
      }
      ctx.item("primo#" + p);
      ctx.consigna("¿Cuál de estos números es PRIMO?");
      ctx.juego.innerHTML = "";
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", o.v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ORDEN DE LAS OPERACIONES (M4, 6° grado — docs/auditoria-dc-caba/grado-6.md):
   jerarquía (primero × y ÷, después + y −), nodal de 6°. Ataca la misconception de
   resolver de izquierda a derecha. GENERADA. Explicación con el orden (C3). ── */
GAMES.jerarquia_operaciones = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const a = rint(2, 9), b = rint(2, 9), c = rint(2, 9);
      const tipo = rint(0, 1);
      let texto, correcto, malo, paso;
      if (tipo === 0) { texto = a + " + " + b + " × " + c; correcto = a + b * c; malo = (a + b) * c; paso = b + "×" + c + "=" + (b * c) + ", y después " + a + "+" + (b * c) + "=" + correcto; }
      else { texto = a + " × " + b + " + " + c; correcto = a * b + c; malo = a * (b + c); paso = a + "×" + b + "=" + (a * b) + ", y después " + (a * b) + "+" + c + "=" + correcto; }
      ctx.item("jerarq#" + texto.replace(/ /g, ""));
      ctx.consigna("¿Cuánto es   " + texto + "  ?");
      ctx.juego.innerHTML = "";
      const motivo = "Primero se multiplica, después se suma: " + paso + ".";
      const opciones = [{ v: correcto, ok: true }];
      if (malo !== correcto) opciones.push({ v: malo, m: motivo });
      let intento = 0;
      while (opciones.length < 3 && intento++ < 20) { const v = correcto + rint(1, 6) * (rint(0, 1) ? 1 : -1); if (v > 0 && !opciones.some((o) => o.v === v)) opciones.push({ v: v, m: motivo }); }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", o.v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── EL PORCENTAJE JUSTO (M13b, 6° grado — docs/auditoria-dc-caba/grado-6.md):
   porcentaje de una cantidad, nodal de 6°. GENERADA con resultados enteros.
   Explicación relacionando el % con la fracción (C3). ── */
GAMES.porcentajes = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    const PS = [10, 25, 50, 75, 100];
    const MULT = { 10: 10, 25: 4, 50: 2, 75: 4, 100: 1 };
    const NOMBRE = { 10: "la décima parte", 25: "la cuarta parte", 50: "la mitad", 75: "tres cuartos", 100: "el total" };
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const p = PS[rint(0, PS.length - 1)];
      const N = rint(2, 12) * MULT[p];
      const correcto = N * p / 100;
      ctx.item("porc#" + p + "de" + N);
      ctx.consigna("¿Cuánto es el " + p + "% de " + N + "?");
      ctx.juego.innerHTML = "";
      const motivo = "El " + p + "% es " + NOMBRE[p] + " de " + N + ", o sea " + correcto + ".";
      const cand = [
        { v: N * p / 10, m: motivo },
        { v: N - p, m: "No es restar: el " + p + "% de " + N + " es tomar " + p + " de cada 100." },
      ];
      const opciones = [{ v: correcto, ok: true }];
      shuffle(cand).forEach((d) => { if (opciones.length < 3 && d.v > 0 && d.v !== correcto && !opciones.some((o) => o.v === d.v)) opciones.push(d); });
      let intento = 0;
      while (opciones.length < 3 && intento++ < 20) { const v = correcto + rint(1, 5) * (rint(0, 1) ? 1 : -1); if (v > 0 && !opciones.some((o) => o.v === v)) opciones.push({ v: v, m: motivo }); }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", o.v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── POTENCIAS (7° grado — docs/auditoria-dc-caba/grado-7.md): potenciación,
   nodal de 7°. GENERADA. Ataca LA misconception: b² = b×2 (en vez de b×b).
   Explicación desarrollando la potencia (Capa 0 · C3). ── */
GAMES.potencias = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const base = rint(2, 9), exp = rint(2, 3);
      const correcto = Math.pow(base, exp);
      const es = exp === 2 ? "²" : "³";
      const desarrollo = Array(exp).fill(base).join("×") + " = " + correcto;
      ctx.item("pot#" + base + "e" + exp);
      ctx.consigna("¿Cuánto es  " + base + es + "  ?");
      ctx.juego.innerHTML = "";
      const cand = [
        { v: base * exp, m: base + es + " no es " + base + "×" + exp + ". Es " + base + " multiplicado por sí mismo: " + desarrollo + "." },
        { v: correcto + base, m: base + es + " = " + desarrollo + "." },
      ];
      const opciones = [{ v: correcto, ok: true }];
      shuffle(cand).forEach((d) => { if (opciones.length < 3 && d.v > 0 && d.v !== correcto && !opciones.some((o) => o.v === d.v)) opciones.push(d); });
      let intento = 0;
      while (opciones.length < 3 && intento++ < 20) { const v = correcto + rint(1, 6) * (rint(0, 1) ? 1 : -1); if (v > 0 && !opciones.some((o) => o.v === v)) opciones.push({ v: v, m: base + es + " = " + desarrollo + "." }); }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", o.v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── PROBLEMAS DE VARIOS PASOS (7° grado — docs/auditoria-dc-caba/grado-7.md):
   problemas de 2 pasos, nodal de 7° (el panel encontró el clúster vacío). Banco
   con distractores por error de proceso (olvidar un paso, operación equivocada).
   Explicación con los dos pasos (Capa 0 · C3). ── */
const PROB_MULTI_BANCO = [
  { t: "Compré 3 cajas de 12 alfajores y regalé 8. ¿Cuántos me quedaron?", ok: 28, d: [{ v: 36, m: "Te faltó restar los 8 regalados: 3×12=36, y 36−8=28." }, { v: 4, m: "Primero multiplicá (3×12=36), recién después restá 8." }] },
  { t: "En el micro había 45 personas. Bajaron 12 y subieron 8. ¿Cuántas quedaron?", ok: 41, d: [{ v: 65, m: "Bajaron 12 (se restan) y subieron 8 (se suman): 45−12+8=41." }, { v: 25, m: "Los 8 que subieron se SUMAN: 45−12+8=41." }] },
  { t: "Un libro tiene 200 páginas. Leí 60 el lunes y 45 el martes. ¿Cuántas me faltan?", ok: 95, d: [{ v: 305, m: "Lo leído se RESTA del total: 200−60−45=95." }, { v: 140, m: "Restá los dos días: 200−60−45=95." }] },
  { t: "Hay 4 mesas con 6 sillas cada una. Se rompieron 5 sillas. ¿Cuántas sirven?", ok: 19, d: [{ v: 24, m: "Faltó restar las 5 rotas: 4×6=24, y 24−5=19." }, { v: 20, m: "4×6=24, después restá 5 → 19." }] },
  { t: "Junté $500. Gasté $180 en un regalo y $120 en la torta. ¿Cuánto me quedó?", ok: 200, d: [{ v: 320, m: "Restá los DOS gastos: 500−180−120=200." }, { v: 800, m: "Los gastos se RESTAN: 500−180−120=200." }] },
  { t: "Un cine tiene 8 filas de 15 butacas. Ya se ocuparon 90. ¿Cuántas quedan libres?", ok: 30, d: [{ v: 120, m: "Faltó restar las 90 ocupadas: 8×15=120, y 120−90=30." }, { v: 105, m: "8×15=120, después restá 90 → 30." }] },
  { t: "Compré 6 paquetes de 8 figuritas. Repetidas tenía 12. ¿Cuántas nuevas quedaron?", ok: 36, d: [{ v: 48, m: "Restá las 12 repetidas: 6×8=48, y 48−12=36." }, { v: 26, m: "6×8=48, recién ahí restá 12 → 36." }] },
  { t: "Tenía $250. Mi abuela me dio $100 y compré un libro de $130. ¿Cuánto me quedó?", ok: 220, d: [{ v: 480, m: "El libro se RESTA: 250+100−130=220." }, { v: 20, m: "Los $100 se SUMAN: 250+100−130=220." }] },
];
GAMES.problemas_multipaso = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = PROB_MULTI_BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!disp.length) { usados = []; disp = PROB_MULTI_BANCO.map((_, i) => i); }
      const idx = disp[rint(0, disp.length - 1)]; usados.push(idx);
      const it = PROB_MULTI_BANCO[idx];
      ctx.item("probmulti#" + idx);
      ctx.consigna(it.t);
      ctx.juego.innerHTML = "";
      const opciones = [{ v: it.ok, ok: true }].concat(it.d.map((x) => ({ v: x.v, m: x.m })));
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", o.v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ENGLISH TIME (Inglés, 7° grado — docs/auditoria-dc-caba/grado-7.md): área
   NUEVA pedida por el panel (Lengua Extranjera). Vocabulario básico. Explicación
   con el significado (Capa 0 · C3). ── */
const INGLES_BANCO = [
  { q: "¿Cómo se dice «perro» en inglés?", ok: "dog", d: ["cat", "cow"], m: "«dog» es perro; «cat» es gato." },
  { q: "¿Cómo se dice «casa» en inglés?", ok: "house", d: ["horse", "mouse"], m: "«house» es casa; «horse» es caballo." },
  { q: "¿Qué significa «red»?", ok: "rojo", d: ["verde", "azul"], m: "«red» es rojo; «green» es verde, «blue» es azul." },
  { q: "¿Cómo se dice «gracias» en inglés?", ok: "thank you", d: ["please", "sorry"], m: "«thank you» es gracias; «please» es por favor." },
  { q: "¿Qué número es «three»?", ok: "3", d: ["2", "4"], m: "«three» es 3; «two» es 2, «four» es 4." },
  { q: "¿Cómo se dice «agua» en inglés?", ok: "water", d: ["milk", "juice"], m: "«water» es agua; «milk» es leche." },
  { q: "¿Qué significa «book»?", ok: "libro", d: ["mesa", "silla"], m: "«book» es libro; «table» es mesa." },
  { q: "¿Cómo saludás a la mañana en inglés?", ok: "good morning", d: ["good night", "goodbye"], m: "«good morning» es buenos días; «good night» es buenas noches." },
  { q: "¿Qué color es «yellow»?", ok: "amarillo", d: ["negro", "blanco"], m: "«yellow» es amarillo; «black» es negro, «white» es blanco." },
  { q: "¿Cómo se dice «familia» en inglés?", ok: "family", d: ["friend", "people"], m: "«family» es familia; «friend» es amigo." },
  { q: "¿Qué significa «happy»?", ok: "feliz", d: ["triste", "cansado"], m: "«happy» es feliz; «sad» es triste." },
  { q: "¿Cómo se dice «escuela» en inglés?", ok: "school", d: ["street", "store"], m: "«school» es escuela; «street» es calle." },
];
GAMES.ingles_basico = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = INGLES_BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!disp.length) { usados = []; disp = INGLES_BANCO.map((_, i) => i); }
      const idx = disp[rint(0, disp.length - 1)]; usados.push(idx);
      const it = INGLES_BANCO[idx];
      ctx.item("ingles#" + idx);
      ctx.consigna(it.q);
      ctx.juego.innerHTML = "";
      const opciones = shuffle([{ t: it.ok, ok: true }].concat(it.d.map((x) => ({ t: x, ok: false }))));
      const fila = el("div", "ops");
      let resuelto = false;
      opciones.forEach((o) => {
        const b = el("button", "op", o.t);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(it.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── DEL DÉCIMO A LA COMA (M11, 5° grado — docs/auditoria-dc-caba/grado-5.md):
   equivalencia fracción decimal ↔ expresión decimal, nodal de 5°. Banco de
   equivalencias comunes. Explicación con décimos/centésimos (Capa 0 · C3). ── */
const DEC_FRAC_BANCO = [
  { q: "0,5 es igual a la fracción…", ok: "1/2", d: ["1/5", "5/1"], m: "0,5 son 5 décimos = 5/10 = 1/2 (la mitad)." },
  { q: "0,25 es igual a la fracción…", ok: "1/4", d: ["2/5", "1/25"], m: "0,25 son 25 centésimos = 25/100 = 1/4." },
  { q: "1/2 escrito como decimal es…", ok: "0,5", d: ["0,2", "1,2"], m: "1/2 es la mitad = 0,5." },
  { q: "3/10 escrito como decimal es…", ok: "0,3", d: ["0,03", "3,0"], m: "3/10 son 3 décimos = 0,3." },
  { q: "0,75 es igual a la fracción…", ok: "3/4", d: ["7/5", "3/5"], m: "0,75 son 75 centésimos = 75/100 = 3/4." },
  { q: "1/4 escrito como decimal es…", ok: "0,25", d: ["0,4", "1,4"], m: "1/4 es 25 centésimos = 0,25." },
  { q: "7/10 escrito como decimal es…", ok: "0,7", d: ["0,07", "7,10"], m: "7/10 son 7 décimos = 0,7." },
  { q: "0,1 es igual a la fracción…", ok: "1/10", d: ["1/100", "10/1"], m: "0,1 es un décimo = 1/10." },
  { q: "0,50 y 0,5, ¿son iguales?", ok: "Sí, son iguales", d: ["No, 0,50 es más", "No, 0,5 es más"], m: "0,50 = 0,5: los ceros a la derecha después de la coma no cambian el valor." },
  { q: "9/100 escrito como decimal es…", ok: "0,09", d: ["0,9", "9,00"], m: "9/100 son 9 centésimos = 0,09." },
];
GAMES.decimales_fraccion = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = DEC_FRAC_BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!disp.length) { usados = []; disp = DEC_FRAC_BANCO.map((_, i) => i); }
      const idx = disp[rint(0, disp.length - 1)]; usados.push(idx);
      const it = DEC_FRAC_BANCO[idx];
      ctx.item("decfrac#" + idx);
      ctx.consigna(it.q);
      ctx.juego.innerHTML = "";
      const opciones = shuffle([{ t: it.ok, ok: true }].concat(it.d.map((x) => ({ t: x, ok: false }))));
      const fila = el("div", "ops");
      let resuelto = false;
      opciones.forEach((o) => {
        const b = el("button", "op", o.t);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(it.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── SUMÁ FRACCIONES (5° grado — docs/auditoria-dc-caba/grado-5.md): suma de
   fracciones de IGUAL denominador, nodal de 5°. GENERADA. Ataca la misconception
   de sumar también los denominadores. Explicación con la regla (Capa 0 · C3). ── */
GAMES.suma_fracciones = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const den = rint(4, 9);
      const a = rint(1, den - 2);
      const b = rint(1, den - 1 - a);            // a+b < den → resultado propio
      const sum = a + b;
      ctx.item("sumafrac#" + a + "_" + b + "_" + den);
      ctx.consigna("¿Cuánto es  " + a + "/" + den + "  +  " + b + "/" + den + "  ?");
      ctx.juego.innerHTML = "";
      const motivo = "Con el MISMO denominador, se suman los de arriba y el de abajo queda igual: " + a + "+" + b + "=" + sum + ", entonces " + sum + "/" + den + ".";
      const cand = [
        { t: sum + "/" + (den + den), m: "El denominador NO se suma: queda " + den + ". " + motivo },
        { t: (sum + 1) + "/" + den, m: motivo },
      ];
      const opciones = [{ t: sum + "/" + den, ok: true }];
      shuffle(cand).forEach((d) => { if (opciones.length < 3 && !opciones.some((o) => o.t === d.t)) opciones.push(d); });
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b2 = el("button", "op", o.t);
        b2.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b2.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b2.classList.add("casi"); setTimeout(() => b2.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b2);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── DETECTIVES DEL CIELO (C5, 5° grado — docs/auditoria-dc-caba/grado-5.md):
   astros — el Sol como estrella, la Luna que refleja, fases y eclipses. Trivia
   con explicación (Capa 0 · C3). ── */
const ASTRO5_BANCO = [
  { q: "¿La Luna tiene luz propia?", ok: "No, refleja la del Sol", d: ["Sí, es una estrella", "Solo cuando está llena"], m: "La Luna no brilla sola: refleja la luz del Sol." },
  { q: "¿Qué es el Sol?", ok: "Una estrella", d: ["Un planeta", "Un satélite"], m: "El Sol es la estrella más cercana a la Tierra." },
  { q: "¿Por qué de día no vemos las estrellas?", ok: "La luz del Sol las tapa", d: ["Se apagan de día", "Se van al otro lado"], m: "Las estrellas siguen ahí, pero la luz del Sol es tan fuerte que no las deja ver." },
  { q: "¿Qué gira alrededor de la Tierra?", ok: "La Luna", d: ["El Sol", "Marte"], m: "La Luna es el satélite natural de la Tierra y gira a su alrededor." },
  { q: "La Luna se ve distinta cada noche. Eso se llama…", ok: "Las fases de la Luna", d: ["Un eclipse", "Una estrella fugaz"], m: "Las fases (nueva, creciente, llena, menguante) son las formas en que vemos la Luna a lo largo del mes." },
  { q: "Un eclipse de Sol pasa cuando…", ok: "La Luna se pone entre el Sol y la Tierra", d: ["El Sol se apaga un rato", "La Tierra choca la Luna"], m: "En un eclipse solar, la Luna tapa al Sol visto desde la Tierra." },
  { q: "¿Qué planeta habitamos?", ok: "La Tierra", d: ["La Luna", "El Sol"], m: "Vivimos en el planeta Tierra, que gira alrededor del Sol." },
  { q: "¿Qué está MÁS lejos de la Tierra?", ok: "El Sol", d: ["La Luna", "Las nubes"], m: "La Luna está mucho más cerca que el Sol." },
];
GAMES.detectives_cielo = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = ASTRO5_BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!disp.length) { usados = []; disp = ASTRO5_BANCO.map((_, i) => i); }
      const idx = disp[rint(0, disp.length - 1)]; usados.push(idx);
      const it = ASTRO5_BANCO[idx];
      ctx.item("astro5#" + idx);
      ctx.consigna(it.q);
      ctx.juego.innerHTML = "";
      const opciones = shuffle([{ t: it.ok, ok: true }].concat(it.d.map((x) => ({ t: x, ok: false }))));
      const fila = el("div", "ops");
      let resuelto = false;
      opciones.forEach((o) => {
        const b = el("button", "op", o.t);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(it.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── Helper reusable de TRIVIA por BANCO (19-jul-2026): items {q, ok, d:[...], m}.
   Consigna = q; opciones = ok + distractores mezclados; al errar explica m (C3). ── */
function juegoTriviaBanco(BANCO, idPrefijo) {
  return {
    crear(ctx) {
      const rondas = ctx.cfg.rondas || 10;
      ctx.rondas(rondas);
      let usados = [], ronda = 0;
      const jugar = () => {
        ctx.ronda(ronda);
        let disp = BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
        if (!disp.length) { usados = []; disp = BANCO.map((_, i) => i); }
        const idx = disp[rint(0, disp.length - 1)]; usados.push(idx);
        const it = BANCO[idx];
        ctx.item(idPrefijo + "#" + idx);
        ctx.consigna(it.q);
        ctx.juego.innerHTML = "";
        const opciones = shuffle([{ t: it.ok, ok: true }].concat(it.d.map((x) => ({ t: x, ok: false }))));
        const fila = el("div", "ops");
        let resuelto = false;
        opciones.forEach((o) => {
          const b = el("button", "op", o.t);
          b.addEventListener("click", async () => {
            if (resuelto) return;
            if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
            else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(it.m); }
          });
          fila.appendChild(b);
        });
        ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
      };
      jugar();
    },
  };
}

/* ── 6° grado (docs/auditoria-dc-caba/grado-6.md) — cuadriláteros (M15a) e
   historia de la organización nacional 1862-1930. ── */
const CUADRI_BANCO = [
  { q: "¿Qué figura tiene 4 lados iguales Y 4 ángulos rectos?", ok: "El cuadrado", d: ["El rombo", "El rectángulo"], m: "El cuadrado tiene 4 lados iguales y 4 ángulos rectos. El rombo tiene lados iguales pero no ángulos rectos." },
  { q: "El rectángulo tiene…", ok: "4 ángulos rectos", d: ["4 lados iguales", "3 lados"], m: "El rectángulo tiene 4 ángulos rectos; los lados son iguales de a pares (largos y cortos)." },
  { q: "¿Qué figura tiene 4 lados iguales pero puede estar inclinada (sin ángulos rectos)?", ok: "El rombo", d: ["El cuadrado", "El trapecio"], m: "El rombo tiene los 4 lados iguales pero sus ángulos no son rectos." },
  { q: "¿Cuántos lados tiene un cuadrilátero?", ok: "4", d: ["3", "5"], m: "Cuadri- significa cuatro: todos los cuadriláteros tienen 4 lados." },
  { q: "El trapecio se reconoce porque…", ok: "Tiene un solo par de lados paralelos", d: ["Tiene todos los lados iguales", "Es redondo"], m: "El trapecio tiene un solo par de lados paralelos." },
  { q: "¿Cuál NO es un cuadrilátero?", ok: "El triángulo", d: ["El cuadrado", "El rombo"], m: "El triángulo tiene 3 lados; los cuadriláteros tienen 4." },
  { q: "El paralelogramo tiene…", ok: "Los lados opuestos paralelos", d: ["Un solo par paralelo", "Ningún lado paralelo"], m: "El paralelogramo tiene los dos pares de lados opuestos paralelos." },
  { q: "Las diagonales del cuadrado…", ok: "Son iguales y se cruzan en el medio", d: ["Son de distinto largo", "No se cruzan"], m: "En el cuadrado las dos diagonales miden lo mismo y se cortan en el centro." },
];
GAMES.cuadrilateros = juegoTriviaBanco(CUADRI_BANCO, "cuadri");
const ORG_NAC_BANCO = [
  { q: "Después de 1853, ¿qué se sancionó para organizar el país?", ok: "La Constitución Nacional", d: ["Una ley de aduanas", "El himno"], m: "En 1853 se sancionó la Constitución Nacional, que organizó el país." },
  { q: "Entre 1880 y 1930 llegaron a la Argentina muchos…", ok: "Inmigrantes de Europa", d: ["Turistas", "Soldados"], m: "En esa época llegaron millones de inmigrantes europeos buscando trabajo." },
  { q: "El ferrocarril, en esa época, servía sobre todo para…", ok: "Llevar productos del campo al puerto", d: ["Pasear los domingos", "La guerra"], m: "El tren llevaba cereales y carne del campo al puerto para exportar." },
  { q: "La Ley 1420 (1884) estableció que la primaria fuera…", ok: "Gratuita y obligatoria", d: ["Solo para ricos", "Solo religiosa"], m: "La Ley 1420 hizo la primaria gratuita, obligatoria y laica." },
  { q: "La Ley Sáenz Peña (1912) estableció el voto…", ok: "Secreto y obligatorio", d: ["Solo para dueños de tierras", "Cantado en voz alta"], m: "La Ley Sáenz Peña estableció el voto secreto y obligatorio." },
  { q: "A la Argentina de esa época se la llamaba…", ok: "El granero del mundo", d: ["El taller del mundo", "La isla del tesoro"], m: "Exportaba tanto grano y carne que la llamaban 'el granero del mundo'." },
];
GAMES.organizacion_nacional = juegoTriviaBanco(ORG_NAC_BANCO, "orgnac");

/* ── 6° · PRODUCTO DE FRACCIONES (generada): a/b × c/d = (a·c)/(b·d). Ataca el
   error de sumar en vez de multiplicar. Explicación con la regla (C3). ── */
GAMES.multiplicar_fracciones = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const a = rint(1, 4), b = rint(2, 5), c = rint(1, 4), d = rint(2, 5);
      const num = a * c, den = b * d;
      ctx.item("mulfrac#" + a + b + c + d);
      ctx.consigna("¿Cuánto es  " + a + "/" + b + " × " + c + "/" + d + "  ?");
      ctx.juego.innerHTML = "";
      const motivo = "Se multiplica arriba con arriba y abajo con abajo: " + a + "×" + c + "=" + num + " y " + b + "×" + d + "=" + den + " → " + num + "/" + den + ".";
      const cand = [
        { t: (a + c) + "/" + (b + d), m: "Acá se MULTIPLICA, no se suma. " + motivo },
        { t: (a * c) + "/" + (b + d), m: "El de abajo también se multiplica: " + b + "×" + d + "=" + den + ". " + motivo },
      ];
      const opciones = [{ t: num + "/" + den, ok: true }];
      shuffle(cand).forEach((x) => { if (opciones.length < 3 && !opciones.some((o) => o.t === x.t)) opciones.push(x); });
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b2 = el("button", "op", o.t);
        b2.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b2.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b2.classList.add("casi"); setTimeout(() => b2.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b2);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── 7° grado (docs/auditoria-dc-caba/grado-7.md) — ecuaciones simples (álgebra
   inicial), homófonos (ortografía) e historia del s.XX. ── */
GAMES.ecuaciones_simples = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const tipo = rint(0, 2);
      let texto, x, motivo, malo;
      if (tipo === 0) { x = rint(2, 15); const a = rint(1, 9); texto = "x + " + a + " = " + (x + a); malo = (x + a) + a; motivo = "Para despejar x hacé la operación contraria: " + (x + a) + " − " + a + " = " + x + "."; }
      else if (tipo === 1) { x = rint(4, 16); const a = rint(1, 9); texto = "x − " + a + " = " + (x - a); malo = (x - a) - a; motivo = "Para despejar x sumá: " + (x - a) + " + " + a + " = " + x + "."; }
      else { const a = rint(2, 6); x = rint(2, 9); texto = a + " × x = " + (a * x); malo = a * x - a; motivo = "Para despejar x dividí: " + (a * x) + " ÷ " + a + " = " + x + "."; }
      ctx.item("ecu#" + texto.replace(/ /g, ""));
      ctx.consigna("Si  " + texto + " ,  ¿cuánto vale x?");
      ctx.juego.innerHTML = "";
      const opciones = [{ v: x, ok: true }];
      if (malo > 0 && malo !== x) opciones.push({ v: malo, m: motivo });
      let intento = 0;
      while (opciones.length < 3 && intento++ < 20) { const v = x + rint(1, 5) * (rint(0, 1) ? 1 : -1); if (v > 0 && !opciones.some((o) => o.v === v)) opciones.push({ v: v, m: motivo }); }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", o.v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};
const HOMOFONOS_BANCO = [
  { q: "Completá: Vamos … si llegó el paquete.", ok: "a ver", d: ["haber"], m: "«a ver» (mirar/comprobar) va separado; «haber» es el verbo (había, ha comido)." },
  { q: "Completá: Tiene que … terminado la tarea.", ok: "haber", d: ["a ver"], m: "«haber» es el verbo (haber terminado); «a ver» es mirar." },
  { q: "Completá: … un gato arriba del techo.", ok: "Hay", d: ["Ahí"], m: "«hay» es del verbo haber (existe); «ahí» señala un lugar." },
  { q: "Completá: El libro está … , sobre la mesa.", ok: "ahí", d: ["hay"], m: "«ahí» señala un lugar; «hay» significa que existe." },
  { q: "Completá: Ayer … un accidente en la esquina.", ok: "tuvo", d: ["tubo"], m: "«tuvo» es del verbo tener; «tubo» es un caño." },
  { q: "Completá: El agua pasa por el … de la pileta.", ok: "tubo", d: ["tuvo"], m: "«tubo» es un caño; «tuvo» es del verbo tener." },
  { q: "Completá: — ¿Venís? — ¡… , claro!", ok: "sí", d: ["si"], m: "«sí» (afirmación) lleva tilde; «si» (condición) no." },
  { q: "Completá: No sé … voy a poder ir.", ok: "si", d: ["sí"], m: "«si» condicional va sin tilde; «sí» afirmación lleva tilde." },
  // ampliado 20-jul-2026 (de 8 a 20 — engrosar bancos nodales, docs/auditoria-dc-caba/)
  { q: "Completá: Ya está … la tarea.", ok: "hecho", d: ["echo"], m: "«hecho» es del verbo hacer; «echo» es de echar (tirar)." },
  { q: "Completá: Yo te … de menos.", ok: "echo", d: ["hecho"], m: "«echo de menos» es del verbo echar; «hecho» es de hacer." },
  { q: "Completá: Espero que le … bien en la prueba.", ok: "vaya", d: ["valla"], m: "«vaya» es del verbo ir; «valla» es una cerca." },
  { q: "Completá: El caballo saltó la … del corral.", ok: "valla", d: ["vaya"], m: "«valla» es la cerca u obstáculo; «vaya» es del verbo ir." },
  { q: "Completá: Le dije «…» al vecino.", ok: "hola", d: ["ola"], m: "«hola» es el saludo; «ola» es la del mar." },
  { q: "Completá: Vivo en una … con jardín.", ok: "casa", d: ["caza"], m: "«casa» es la vivienda; «caza» es de cazar animales." },
  { q: "Completá: ¿Lo … desde acá?", ok: "ves", d: ["vez"], m: "«ves» es del verbo ver; «vez» es una ocasión (una vez)." },
  { q: "Completá: Cayó un … en la tormenta.", ok: "rayo", d: ["rallo"], m: "«rayo» es el de la tormenta; «rallo» es de rallar queso." },
  { q: "Completá: ¿Ya … terminado la tarea?", ok: "has", d: ["as"], m: "«has» es del verbo haber (has comido); «as» es la carta o un campeón." },
  { q: "Completá: La … sube por el tronco del árbol.", ok: "savia", d: ["sabia"], m: "«savia» es el líquido del árbol; «sabia» es una mujer que sabe mucho." },
  { q: "Completá: Hay que … en las elecciones.", ok: "votar", d: ["botar"], m: "«votar» es elegir en elecciones; «botar» es tirar algo." },
  { q: "Completá: Vivo en el … piso (el número 6).", ok: "sexto", d: ["cesto"], m: "«sexto» es el número; «cesto» es la canasta." },
];
GAMES.homofonos = juegoTriviaBanco(HOMOFONOS_BANCO, "homof");
const SIGLOXX_BANCO = [
  { q: "¿Quién fue presidente desde 1946, muy ligado a los derechos de los trabajadores?", ok: "Juan Domingo Perón", d: ["José de San Martín", "Manuel Belgrano"], m: "Perón fue presidente desde 1946; su gobierno impulsó derechos de los trabajadores." },
  { q: "En 1976, en la Argentina, hubo…", ok: "Un golpe de Estado (dictadura)", d: ["Un mundial de fútbol", "La independencia"], m: "En 1976 un golpe militar interrumpió la democracia; fue una dictadura." },
  { q: "¿En qué año volvió la democracia tras la última dictadura?", ok: "1983", d: ["1810", "1955"], m: "En 1983 se recuperó la democracia con elecciones libres." },
  { q: "El 24 de marzo se recuerda…", ok: "El Día de la Memoria", d: ["El Día de la Bandera", "La independencia"], m: "El 24 de marzo es el Día Nacional de la Memoria por la Verdad y la Justicia." },
  { q: "¿Qué derecho consiguieron las mujeres en 1947?", ok: "El voto femenino", d: ["Manejar autos", "Ir a la escuela"], m: "En 1947 se sancionó la ley del voto femenino; votaron por primera vez en 1951." },
  { q: "En democracia, ¿quién elige a los gobernantes?", ok: "El pueblo, votando", d: ["Un rey", "El ejército"], m: "En democracia, la gente elige a sus representantes con el voto." },
];
GAMES.argentina_sigloXX = juegoTriviaBanco(SIGLOXX_BANCO, "sigloxx");

/* ── 3° grado (docs/auditoria-dc-caba/grado-3.md) — orden alfabético (L4, con la
   mecánica ORDENAR: palabras que empiezan igual, se desempata por la 2ª letra) y
   ortografía (L3: -aba, z→ces, mb/nv). ── */
const ALFAB_BANCO = [
  { items: ["banana", "boca", "brazo", "burro"] },
  { items: ["casa", "cielo", "codo", "cuna"] },
  { items: ["mano", "mesa", "mono", "muela"] },
  { items: ["pan", "perro", "pino", "pollo"] },
  { items: ["rana", "reto", "risa", "rosa"] },
  { items: ["sala", "selva", "silla", "sopa"] },
  { items: ["tapa", "techo", "tiza", "toldo"] },
  { items: ["dado", "dedo", "disco", "duende"] },
];
GAMES.orden_alfabetico = juegoOrdenar(ALFAB_BANCO, "Ordená de la A a la Z. Tocá las palabras en orden.", "Cuando empiezan con la misma letra, mirá la SEGUNDA letra para ordenar.", "alfab");
const ORTO3_BANCO = [
  { q: "El plural de «luz» es…", ok: "luces", d: ["luzes"], m: "Las palabras con Z cambian la z por C en plural: luz → luces." },
  { q: "Yo antes … todos los días (jugar, en pasado).", ok: "jugaba", d: ["jugava"], m: "El pasado terminado en -aba se escribe con B: jugaba, cantaba." },
  { q: "¿Cómo se escribe? «ta…ién»", ok: "también (mb)", d: ["tanbién (nb)"], m: "Antes de B y P va M, no N: también, campo." },
  { q: "El plural de «lápiz» es…", ok: "lápices", d: ["lápizes"], m: "Con Z → C en plural: lápiz → lápices." },
  { q: "Ella … una canción (cantar, en pasado).", ok: "cantaba", d: ["cantava"], m: "El imperfecto -aba va con B." },
  { q: "¿Cómo se escribe? «i…vierno»", ok: "invierno (nv)", d: ["imvierno (mv)"], m: "Antes de V va N: invierno, envidia." },
  { q: "El plural de «feliz» es…", ok: "felices", d: ["felizes"], m: "Z → C en plural: feliz → felices." },
  { q: "Nosotros … en la plaza (caminar, en pasado).", ok: "caminábamos", d: ["caminávamos"], m: "El imperfecto -ábamos va con B." },
];
GAMES.ortografia_3ro = juegoTriviaBanco(ORTO3_BANCO, "orto3");

/* ── 3° · PROBLEMAS (M13, generada): problemas de 1 paso (×, +, −) con números de
   3° grado. Distractores por operación equivocada. Explicación (C3). ── */
GAMES.problemas_3ro = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    const OBJ = [["figuritas"], ["caramelos"], ["lápices"], ["galletitas"], ["stickers"]];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const obj = OBJ[rint(0, OBJ.length - 1)][0];
      const tipo = rint(0, 2);
      let texto, correcto, motivo;
      if (tipo === 0) { const c = rint(2, 9), n = rint(2, 6); correcto = c * n; texto = "En cada caja hay " + c + " " + obj + ". ¿Cuántas hay en " + n + " cajas?"; motivo = n + " cajas de " + c + " → " + n + "×" + c + "=" + correcto + "."; }
      else if (tipo === 1) { const a = rint(10, 40), b = rint(5, 30); correcto = a + b; texto = "Tenía " + a + " " + obj + " y me regalaron " + b + ". ¿Cuántas tengo?"; motivo = "Me dieron más, así que sumo: " + a + "+" + b + "=" + correcto + "."; }
      else { const a = rint(20, 50), b = rint(5, 19); correcto = a - b; texto = "Tenía " + a + " " + obj + " y regalé " + b + ". ¿Cuántas me quedaron?"; motivo = "Di algunas, así que resto: " + a + "−" + b + "=" + correcto + "."; }
      ctx.item("prob3#" + tipo + "_" + correcto);
      ctx.consigna(texto);
      ctx.juego.innerHTML = "";
      const opciones = [{ v: correcto, ok: true }];
      let intento = 0;
      while (opciones.length < 3 && intento++ < 30) { const v = correcto + rint(1, 8) * (rint(0, 1) ? 1 : -1); if (v > 0 && !opciones.some((o) => o.v === v)) opciones.push({ v: v, m: motivo }); }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", o.v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿CON QUÉ LETRA EMPIEZA? (1° grado — docs/auditoria-dc-caba/grado-1.md):
   conciencia fonológica — reconocer el sonido/letra inicial. La consigna se LEE
   en voz alta (voz argentina, ya funciona) → el chico ESCUCHA la palabra. Trivia
   con la letra correcta + distractores. Explicación con el sonido (C3). ── */
const LETRA_INICIAL_BANCO = [
  { q: "¿Con qué letra empieza «sol»?", ok: "S", d: ["L", "O"], m: "«sol» empieza con el sonido /s/: la letra S." },
  { q: "¿Con qué letra empieza «luna»?", ok: "L", d: ["N", "U"], m: "«luna» empieza con el sonido /l/: la letra L." },
  { q: "¿Con qué letra empieza «pato»?", ok: "P", d: ["B", "T"], m: "«pato» empieza con el sonido /p/: la letra P." },
  { q: "¿Con qué letra empieza «mesa»?", ok: "M", d: ["N", "S"], m: "«mesa» empieza con el sonido /m/: la letra M." },
  { q: "¿Con qué letra empieza «casa»?", ok: "C", d: ["S", "A"], m: "«casa» empieza con el sonido /k/: la letra C." },
  { q: "¿Con qué letra empieza «dedo»?", ok: "D", d: ["B", "T"], m: "«dedo» empieza con el sonido /d/: la letra D." },
  { q: "¿Con qué letra empieza «rana»?", ok: "R", d: ["L", "N"], m: "«rana» empieza con el sonido /r/: la letra R." },
  { q: "¿Con qué letra empieza «foca»?", ok: "F", d: ["V", "C"], m: "«foca» empieza con el sonido /f/: la letra F." },
  { q: "¿Con qué letra empieza «gato»?", ok: "G", d: ["J", "C"], m: "«gato» empieza con el sonido /g/: la letra G." },
  { q: "¿Con qué letra empieza «nube»?", ok: "N", d: ["M", "U"], m: "«nube» empieza con el sonido /n/: la letra N." },
  { q: "¿Con qué letra empieza «bota»?", ok: "B", d: ["P", "D"], m: "«bota» empieza con el sonido /b/: la letra B." },
  { q: "¿Con qué letra empieza «tren»?", ok: "T", d: ["D", "R"], m: "«tren» empieza con el sonido /t/: la letra T." },
];
GAMES.letra_inicial = juegoTriviaBanco(LETRA_INICIAL_BANCO, "letraini");

/* ── ANTERIOR Y SIGUIENTE (1°/2° grado — docs/auditoria-dc-caba/): el anterior y
   el posterior de un número (NAP nodal). GENERADA, rango por cfg.max (1°=100,
   2°=1000). Explicación con "uno más / uno menos" (C3). ── */
GAMES.anterior_siguiente = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    const max = ctx.cfg.max || 100;
    ctx.rondas(rondas);
    const fmt = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const n = rint(2, max - 1);
      const dir = rint(0, 1);   // 0 = después/siguiente, 1 = antes/anterior
      const correcto = dir === 0 ? n + 1 : n - 1;
      ctx.item("antsig#" + dir + "_" + n);
      ctx.consigna(dir === 0 ? "¿Qué número va JUSTO DESPUÉS del " + fmt(n) + "?" : "¿Qué número va JUSTO ANTES del " + fmt(n) + "?");
      ctx.juego.innerHTML = "";
      const motivo = dir === 0 ? "Después del " + fmt(n) + " viene el " + fmt(n + 1) + " (uno más)." : "Antes del " + fmt(n) + " está el " + fmt(n - 1) + " (uno menos).";
      const cand = [
        { v: dir === 0 ? n - 1 : n + 1, m: "Ese es el de al lado, pero para el OTRO lado. " + motivo },
        { v: n, m: "Ese es el MISMO número " + fmt(n) + ". " + motivo },
      ];
      const opciones = [{ v: correcto, ok: true }];
      shuffle(cand).forEach((d) => { if (opciones.length < 3 && d.v > 0 && d.v !== correcto && !opciones.some((o) => o.v === d.v)) opciones.push(d); });
      let intento = 0;
      while (opciones.length < 3 && intento++ < 20) { const v = correcto + rint(2, 5) * (rint(0, 1) ? 1 : -1); if (v > 0 && !opciones.some((o) => o.v === v)) opciones.push({ v: v, m: motivo }); }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", fmt(o.v));
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── CONTAR SALTANDO (2° grado — docs/auditoria-dc-caba/grado-2.md): contar de a
   2, de a 5, de a 10 (NAP nodal de 2°). GENERADA. Muestra 3 números de la serie
   y pide el que sigue. Explicación con el salto (C3). ── */
GAMES.contar_saltando = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const paso = [2, 5, 10][rint(0, 2)];
      const inicio = rint(1, 8) * paso;
      const serie = [inicio, inicio + paso, inicio + 2 * paso];
      const correcto = inicio + 3 * paso;
      ctx.item("saltar#" + paso + "_" + inicio);
      ctx.consigna("Contando de a " + paso + ":  " + serie.join(", ") + ", …  ¿qué número sigue?");
      ctx.juego.innerHTML = "";
      const motivo = "Vas sumando " + paso + " cada vez: " + serie[2] + " + " + paso + " = " + correcto + ".";
      const cand = [
        { v: correcto - paso, m: "Ese ya lo dijiste. " + motivo },
        { v: correcto + 1, m: "El salto es de " + paso + ", no de 1. " + motivo },
        { v: serie[2] + 1, m: "Hay que sumar " + paso + ", no 1. " + motivo },
      ];
      const opciones = [{ v: correcto, ok: true }];
      shuffle(cand).forEach((d) => { if (opciones.length < 3 && d.v > 0 && d.v !== correcto && !opciones.some((o) => o.v === d.v)) opciones.push(d); });
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(opciones).forEach((o) => {
        const b = el("button", "op", o.v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) { resuelto = true; b.classList.add("anim-pop"); ctx.bien(); ronda++; await espera(950); if (ronda >= rondas) ctx.win(); else jugar(); }
          else { b.classList.add("casi"); setTimeout(() => b.classList.remove("casi"), 450); ctx.casi(o.m); }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿DE QUÉ MATERIAL ES? — trivia (14-jul-2026, 1° grado NAP Bimestre 4
   "Ideas web": "trivia de materiales — ¿vidrio, madera o metal para una
   ventana?"). Opciones de TEXTO (no emoji — no hay glifo distintivo por
   material sin ambigüedad con los objetos del banco). ── */
const MATERIALES_BANCO = [
  { obj: "🪟", material: "Vidrio" }, { obj: "🍷", material: "Vidrio" },
  { obj: "🪑", material: "Madera" }, { obj: "🚪", material: "Madera" },
  { obj: "🔔", material: "Metal" }, { obj: "🥄", material: "Metal" },
  // agregados 14-jul-2026 (banco ampliado de 6 a 10). MATS es una lista
  // fija de 3 botones (Vidrio/Madera/Metal) — cualquier ítem nuevo tiene
  // que usar exactamente uno de esos 3.
  { obj: "🔑", material: "Metal" }, { obj: "🪞", material: "Vidrio" },
  { obj: "🎻", material: "Madera" }, { obj: "🍾", material: "Vidrio" },
];
GAMES.materiales = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    const MATS = ["Vidrio", "Madera", "Metal"];
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿De qué material es?", "n");
      ctx.juego.innerHTML = "";
      let disp = MATERIALES_BANCO.filter((x) => !usados.includes(x.obj));
      if (!disp.length) { usados = []; disp = MATERIALES_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.obj);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto", `<span style="font-size:80px">${item.obj}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle(MATS).forEach((m) => {
        const b = el("button", "spriteBtn", `<span style="font-size:24px;font-family:'Baloo',sans-serif">${m}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (m === item.material) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── GRILLA 1-100 — rompecabezas numérico (14-jul-2026, 1° grado NAP
   Bimestre 4 "Ideas web": "rompecabezas numérico de la grilla 1-100 en
   baldosas 10×10"). Simplificado a UNA decena por ronda (10 baldosas, layout
   2×5) en vez del grid completo de 100 celdas — a esta edad un grid de 100
   objetivos táctiles no entra en pantalla con el tamaño mínimo de blanco
   táctil que ya usa el resto del motor (skill §4b). ── */
GAMES.grilla100 = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.consigna("¿Qué número falta en la grilla?");
      ctx.juego.innerHTML = "";
      const desde = rint(1, 9) * 10 + 1;   // 11, 21, ... 91 — una decena completa
      const nums = Array.from({ length: 10 }, (_, i) => desde + i);
      const falta = rint(0, 9);
      const grilla = el("div", "grilla100");
      const celdas = nums.map((n, i) =>
        el("div", i === falta ? "grilla100Celda hueco" : "grilla100Celda", i === falta ? "?" : String(n)));
      celdas.forEach((c) => grilla.appendChild(c));
      ctx.juego.appendChild(grilla);
      const ops = el("div", "ops");
      const distr = new Set([nums[falta]]);
      let guardas = 0;
      while (distr.size < 3 && guardas < 100) {
        guardas++;
        const v = nums[falta] + rint(-12, 12);
        if (v > 0 && v <= 100 && !nums.includes(v)) distr.add(v);
      }
      let resuelto = false;
      shuffle([...distr]).forEach((v) => {
        const b = el("button", "op", v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === nums[falta]) {
            resuelto = true;
            celdas[falta].textContent = v;
            celdas[falta].classList.remove("hueco");
            celdas[falta].classList.add("anim-pop");
            ctx.bien();
            ronda++;
            await espera(1000);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.classList.add("casi");
            setTimeout(() => b.classList.remove("casi"), 450);
            ctx.casi();
          }
        });
        ops.appendChild(b);
      });
      ctx.juego.appendChild(ops);
    };
    jugar();
  },
};

/* ── SUSTANTIVOS COMUNES Y PROPIOS (14-jul-2026, 2° grado NAP Bimestre 1
   "Ideas web": "arrastrar el sustantivo a Comunes vs. Propios"). Mismo
   patrón de clasificar 2 categorías que campo_ciudad, con palabras (la
   mayúscula del propio es la pista visual, no hace falta explicarla). ── */
const SUSTANTIVOS_BANCO = [
  { p: "perro", tipo: "comun" }, { p: "ciudad", tipo: "comun" }, { p: "pelota", tipo: "comun" },
  { p: "silla", tipo: "comun" }, { p: "río", tipo: "comun" },
  { p: "Rex", tipo: "propio" }, { p: "Salta", tipo: "propio" }, { p: "María", tipo: "propio" },
  { p: "Argentina", tipo: "propio" }, { p: "Luna", tipo: "propio" },
];
GAMES.sustantivos = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es un sustantivo común o propio?", "f");
      ctx.juego.innerHTML = "";
      let disp = SUSTANTIVOS_BANCO.filter((x) => !usados.includes(x.p));
      if (!disp.length) { usados = []; disp = SUSTANTIVOS_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.p);
      const arriba = el("div", "tablero");
      const cont = el("div", "spriteQuieto anim-pop",
        `<span style="font-size:44px;font-family:'Baloo',sans-serif">${item.p}</span>`);
      arriba.appendChild(cont);
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      [{ tipo: "comun", label: "Común" }, { tipo: "propio", label: "Propio" }].forEach(({ tipo, label }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:24px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (tipo === item.tipo) {
            resuelto = true;
            cont.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── SUMAS REDONDAS (14-jul-2026, 2° grado NAP Bimestre 1 "Ideas web":
   "rompecabezas de sumas que den números redondos — 150+50=200"). Mismo
   patrón que suma_rapida (Sala... 1° grado) pero con banco de números
   REDONDOS y objetivo variable (100/200/300) mostrado en pantalla, no en
   el audio fijo (la consigna no puede decir un número que cambia). ── */
GAMES.sumas_redondas = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    const OBJETIVOS = [100, 200, 300];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "Tocá dos números que sumen el número redondo", "n");
      ctx.juego.innerHTML = "";
      const objetivo = OBJETIVOS[rint(0, OBJETIVOS.length - 1)];
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:36px;font-family:'Baloo',sans-serif">Formá ${objetivo}</span>`));
      ctx.juego.appendChild(arriba);
      const REDONDOS = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250].filter((v) => v < objetivo);
      const a = REDONDOS[rint(0, REDONDOS.length - 1)];
      const b = objetivo - a;
      let nums = [a, b];
      let guardas = 0;
      while (nums.length < 5 && guardas < 100) {
        guardas++;
        const v = REDONDOS[rint(0, REDONDOS.length - 1)];
        if (!nums.includes(v) && !nums.some((n) => n + v === objetivo)) nums.push(v);
      }
      nums = shuffle(nums);
      const fila = el("div", "filaSprites");
      let elegido = null;
      let resuelto = false;
      nums.forEach((v, idx) => {
        const btn = el("button", "spriteBtn", `<span style="font-size:24px;font-family:'Baloo',sans-serif">${v}</span>`);
        btn.addEventListener("click", async () => {
          if (resuelto || btn.disabled) return;
          if (elegido === null) {
            elegido = { idx, v, btn };
            btn.classList.add("elegido");
            return;
          }
          if (elegido.idx === idx) return;
          if (elegido.v + v === objetivo) {
            resuelto = true;
            btn.disabled = true;
            elegido.btn.disabled = true;
            btn.classList.add("anim-pop");
            elegido.btn.classList.add("anim-pop");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            const prevBtn = elegido.btn;   // capturar ANTES de resetear elegido (bug real de suma_rapida)
            prevBtn.classList.remove("elegido");
            btn.style.animation = "sacudir .4s ease";
            prevBtn.style.animation = "sacudir .4s ease";
            setTimeout(() => { btn.style.animation = ""; prevBtn.style.animation = ""; }, 450);
            ctx.casi();
            elegido = null;
          }
        });
        fila.appendChild(btn);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── SINÓNIMOS Y ANTÓNIMOS (14-jul-2026, 2° grado NAP Bimestre 2 "Ideas
   web": "unir sinónimos/antónimos"). Cada palabra del banco declara su
   propia relación (sin/ant) — la consigna FIJA se elige según el ítem, dos
   grabaciones distintas (no puede ser una sola: cambia la pregunta). ── */
const SINANT_BANCO = [
  { p: "Contento", rel: "sin", correcta: "Feliz", distractoras: ["Triste", "Cansado"] },
  { p: "Grande", rel: "ant", correcta: "Chico", distractoras: ["Enorme", "Alto"] },
  { p: "Rápido", rel: "sin", correcta: "Veloz", distractoras: ["Lento", "Fuerte"] },
  { p: "Caliente", rel: "ant", correcta: "Frío", distractoras: ["Tibio", "Ardiente"] },
  { p: "Lindo", rel: "sin", correcta: "Hermoso", distractoras: ["Feo", "Raro"] },
  { p: "Alto", rel: "ant", correcta: "Bajo", distractoras: ["Grande", "Ancho"] },
  // agregados 14-jul-2026 (banco ampliado de 6 a 10).
  { p: "Fuerte", rel: "sin", correcta: "Potente", distractoras: ["Débil", "Suave"] },
  { p: "Cerca", rel: "ant", correcta: "Lejos", distractoras: ["Cercano", "Próximo"] },
  { p: "Difícil", rel: "sin", correcta: "Complicado", distractoras: ["Fácil", "Simple"] },
  { p: "Empezar", rel: "ant", correcta: "Terminar", distractoras: ["Comenzar", "Iniciar"] },
];
GAMES.sinonimos_antonimos = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.juego.innerHTML = "";
      let disp = SINANT_BANCO.filter((x) => !usados.includes(x.p));
      if (!disp.length) { usados = []; disp = SINANT_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.p);
      ctx.consigna(item.rel === "sin" ? "¿Cuál es el sinónimo?" : "¿Cuál es el antónimo?");
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:34px;font-family:'Baloo',sans-serif">${item.p}</span>`));
      ctx.juego.appendChild(arriba);
      const opciones = shuffle([item.correcta, ...item.distractoras]);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      opciones.forEach((op) => {
        const b = el("button", "spriteBtn", `<span style="font-size:22px;font-family:'Baloo',sans-serif">${op}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op === item.correcta) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── SUMA REPETIDA → MULTIPLICACIÓN (14-jul-2026, 2° grado NAP Bimestre 2
   "Ideas web": "asociar suma repetida con su multiplicación — 2+2+2+2 →
   2×4"). Distractores por CANTIDAD/SUMANDO incorrectos (no por el orden
   conmutado — 4×2 también da 8, no es un distractor pedagógicamente
   honesto, solo confundiría con una convención de escritura). ── */
GAMES.multiplicacion_concepto = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Qué multiplicación es esta suma?", "n");
      ctx.juego.innerHTML = "";
      const sumando = rint(2, 5);
      const veces = rint(2, 4);
      const texto = Array.from({ length: veces }, () => sumando).join(" + ");
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:28px;font-family:'Baloo',sans-serif">${texto}</span>`));
      ctx.juego.appendChild(arriba);
      const correcta = `${sumando}×${veces}`;
      const opciones = new Set([correcta]);
      let guardas = 0;
      while (opciones.size < 3 && guardas < 50) {
        guardas++;
        const s2 = Math.max(2, sumando + rint(-1, 1));
        const v2 = Math.max(2, veces + rint(-1, 1));
        const op = `${s2}×${v2}`;
        if (op !== correcta) opciones.add(op);
      }
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle([...opciones]).forEach((op) => {
        const b = el("button", "spriteBtn", `<span style="font-size:26px;font-family:'Baloo',sans-serif">${op}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op === correcta) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿SE CALIENTA RÁPIDO? — conductor/aislante (14-jul-2026, 2° grado NAP
   Bimestre 3 "Ideas web": "simulador de cocina — clasificar materiales por
   si se calientan rápido -metal- o no -madera/plástico-"). Mismo patrón de
   clasificar 2 categorías que campo_ciudad. ── */
const CONDUCTOR_BANCO = [
  { e: "🥄", cat: "conductor" }, { e: "🍳", cat: "conductor" }, { e: "🔑", cat: "conductor" }, { e: "🚰", cat: "conductor" },
  { e: "🥢", cat: "aislante" }, { e: "🧦", cat: "aislante" }, { e: "🧺", cat: "aislante" }, { e: "📖", cat: "aislante" },
  // agregados 14-jul-2026 (banco ampliado de 8 a 10). Es sobre calor
  // (¿se calienta rápido?), no electricidad — mismo criterio "cocina"
  // que el resto del banco.
  { e: "🔪", cat: "conductor" }, { e: "🧤", cat: "aislante" },
];
GAMES.conductor_aislante = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Se calienta rápido o no?", "n");
      ctx.juego.innerHTML = "";
      let disp = CONDUCTOR_BANCO.filter((x) => !usados.includes(x.e));
      if (!disp.length) { usados = []; disp = CONDUCTOR_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.e);
      const arriba = el("div", "tablero");
      const cont = el("div", "spriteQuieto anim-pop", `<span style="font-size:80px">${item.e}</span>`);
      arriba.appendChild(cont);
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      [{ cat: "conductor", label: "🔥 Se calienta rápido" }, { cat: "aislante", label: "🧊 No se calienta" }].forEach(({ cat, label }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:19px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (cat === item.cat) {
            resuelto = true;
            cont.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── FAMILIA DE PALABRAS (14-jul-2026, 2° grado NAP Bimestre 3 "Ideas
   web": "completar palabra con su familia correcta" — ej. PAN → PANADERÍA). ── */
const FAMILIA_BANCO = [
  { raiz: "PAN", correcta: "PANADERÍA", distractoras: ["ZAPATO", "ESCUELA"] },
  { raiz: "FLOR", correcta: "FLORERO", distractoras: ["LIBRO", "CAMISA"] },
  { raiz: "LIBRO", correcta: "LIBRERÍA", distractoras: ["PELOTA", "VENTANA"] },
  { raiz: "LECHE", correcta: "LECHERO", distractoras: ["SILLA", "CAMINO"] },
  { raiz: "PESCADO", correcta: "PESCADERÍA", distractoras: ["MESA", "JARDÍN"] },
  // agregados 14-jul-2026 (banco ampliado de 5 a 10).
  { raiz: "ZAPATO", correcta: "ZAPATERÍA", distractoras: ["MESA", "PERRO"] },
  { raiz: "DIENTE", correcta: "DENTISTA", distractoras: ["SILLA", "RÍO"] },
  { raiz: "CARTA", correcta: "CARTERO", distractoras: ["SOL", "GATO"] },
  { raiz: "JARDÍN", correcta: "JARDINERO", distractoras: ["LUNA", "MESA"] },
  { raiz: "RELOJ", correcta: "RELOJERÍA", distractoras: ["PATO", "NUBE"] },
];
GAMES.familia_palabras = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Qué palabra es de la misma familia?", "f");
      ctx.juego.innerHTML = "";
      let disp = FAMILIA_BANCO.filter((x) => !usados.includes(x.raiz));
      if (!disp.length) { usados = []; disp = FAMILIA_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.raiz);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:32px;font-family:'Baloo',sans-serif">${item.raiz}</span>`));
      ctx.juego.appendChild(arriba);
      const opciones = shuffle([item.correcta, ...item.distractoras]);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      opciones.forEach((op) => {
        const b = el("button", "spriteBtn", `<span style="font-size:19px;font-family:'Baloo',sans-serif">${op}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op === item.correcta) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── TRIVIA ESPACIAL (14-jul-2026, 2° grado NAP Bimestre 4 "Ideas web":
   "trivia espacial — día/noche/ambos"). Mismo patrón de trivia de 3
   opciones que materiales (1° grado). ── */
const ESPACIAL_BANCO = [
  { e: "☀️", cuando: "Día" }, { e: "🌙", cuando: "Noche" }, { e: "⭐", cuando: "Noche" },
  { e: "☁️", cuando: "Ambos" }, { e: "🌤️", cuando: "Día" }, { e: "🌌", cuando: "Noche" },
  // agregados 14-jul-2026 (banco ampliado de 6 a 10). OPS es una lista
  // fija de 3 botones (Día/Noche/Ambos).
  { e: "🌧️", cuando: "Ambos" }, { e: "🌈", cuando: "Día" },
  { e: "🦉", cuando: "Noche" }, { e: "🌫️", cuando: "Ambos" },
];
GAMES.trivia_espacial = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    const OPS = ["Día", "Noche", "Ambos"];
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Se ve de día, de noche o en ambos?", "n");
      ctx.juego.innerHTML = "";
      let disp = ESPACIAL_BANCO.filter((x) => !usados.includes(x.e));
      if (!disp.length) { usados = []; disp = ESPACIAL_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.e);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto", `<span style="font-size:80px">${item.e}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle(OPS).forEach((op) => {
        const b = el("button", "spriteBtn", `<span style="font-size:22px;font-family:'Baloo',sans-serif">${op}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op === item.cuando) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── TABLAS CONTRARRELOJ (14-jul-2026, 2° grado NAP Bimestre 4 "Ideas
   web": "cálculo mental contrarreloj con tablas del 2, 5 y 10"). PRIMERA
   mecánica de timer del motor — cero fail states: si se acaba el tiempo,
   no penaliza duro, solo regenera la MISMA ronda con una cuenta nueva
   (como un "casi" más). Guarda de seguridad real: si el jugador navega a
   otra pantalla a mitad de ronda, el intervalo NO puede saberlo solo (el
   shell no tiene hook de "juego cerrado") — se autodetecta chequeando si
   su propio nodo sigue conectado al documento, y si no, se apaga solo en
   vez de seguir de fondo mutando el fallos/ctx de OTRO juego ya abierto. ── */
const RAPIDO_CORTAS = ["¡Otra vez, rápido!", "¡Vamos, rápido!", "¡Dale, rápido!"];
GAMES.tablas_contrarreloj = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    const TABLAS = [2, 5, 10];
    const TIEMPO_MS = 6000;
    let ronda = 0;
    let intervalId = null;
    const jugar = () => {
      if (intervalId) { clearInterval(intervalId); intervalId = null; }
      ctx.ronda(ronda);
      ctx.consigna(ronda === 0 ? "Elegí rápido: ¿cuánto es?" : sacarDeBolsa(ctx, "rapido", RAPIDO_CORTAS));
      ctx.juego.innerHTML = "";
      const tabla = TABLAS[rint(0, TABLAS.length - 1)];
      const factor = rint(1, 10);
      const correcta = tabla * factor;
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:40px;font-family:'Baloo',sans-serif">${tabla} × ${factor}</span>`));
      ctx.juego.appendChild(arriba);
      const barraWrap = el("div", "barraTiempo");
      const barra = el("div", "barraTiempo__fill");
      barraWrap.appendChild(barra);
      ctx.juego.appendChild(barraWrap);
      const opciones = new Set([correcta]);
      let guardas = 0;
      while (opciones.size < 3 && guardas < 50) {
        guardas++;
        const v = correcta + rint(-tabla * 2, tabla * 2);
        if (v > 0 && v !== correcta) opciones.add(v);
      }
      let resuelto = false;
      const inicio = Date.now();
      intervalId = setInterval(() => {
        if (!barraWrap.isConnected) {   // el jugador se fue a otra pantalla — no seguir de fondo
          clearInterval(intervalId);
          intervalId = null;
          return;
        }
        const restante = Math.max(0, 1 - (Date.now() - inicio) / TIEMPO_MS);
        barra.style.width = (restante * 100) + "%";
        if (restante <= 0 && !resuelto) {
          clearInterval(intervalId);
          intervalId = null;
          ctx.casi();
          jugar();   // se acabó el tiempo: cuenta nueva, misma ronda, sin penalizar duro
        }
      }, 100);
      const fila = el("div", "filaSprites");
      shuffle([...opciones]).forEach((v) => {
        const b = el("button", "spriteBtn", `<span style="font-size:26px;font-family:'Baloo',sans-serif">${v}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === correcta) {
            resuelto = true;
            if (intervalId) { clearInterval(intervalId); intervalId = null; }
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿QUÉ COME? — unir animal con su comida (14-jul-2026, 3° grado NAP
   Bimestre 1 "Ideas web": "unir cráneo/pico del animal con su comida").
   Mismo patrón de matching de 3 opciones que planta_fruto. ── */
const ANIMAL_COMIDA_BANCO = [
  { animal: "🦁", comida: "🥩" }, { animal: "🐰", comida: "🥕" }, { animal: "🐝", comida: "🌸" },
  { animal: "🐼", comida: "🎋" }, { animal: "🦉", comida: "🐭" },
  // agregados 14-jul-2026 (banco ampliado de 5 a 10).
  { animal: "🐵", comida: "🍌" }, { animal: "🐘", comida: "🥜" }, { animal: "🐻", comida: "🍯" },
  { animal: "🐮", comida: "🌾" }, { animal: "🐿️", comida: "🌰" },
];
GAMES.animal_comida = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Qué come este animal?", "m");
      ctx.juego.innerHTML = "";
      let disp = ANIMAL_COMIDA_BANCO.filter((x) => !usados.includes(x.animal));
      if (!disp.length) { usados = []; disp = ANIMAL_COMIDA_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.animal);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto", `<span style="font-size:80px">${item.animal}</span>`));
      ctx.juego.appendChild(arriba);
      let opciones = [item.comida];
      while (opciones.length < 3) {
        const otro = ANIMAL_COMIDA_BANCO[rint(0, ANIMAL_COMIDA_BANCO.length - 1)].comida;
        if (!opciones.includes(otro)) opciones.push(otro);
      }
      opciones = shuffle(opciones);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      opciones.forEach((c) => {
        const b = el("button", "spriteBtn", `<span style="font-size:44px">${c}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (c === item.comida) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── SUSTANTIVO, ADJETIVO O VERBO (14-jul-2026, 3° grado NAP Bimestre 1
   "Ideas web": "clasificar palabras en sustantivo/adjetivo/verbo"). Mismo
   patrón de clasificar que campo_ciudad, extendido a 3 categorías. ── */
const PARTES_ORACION_BANCO = [
  { p: "Perro", tipo: "sustantivo" }, { p: "Casa", tipo: "sustantivo" }, { p: "Escuela", tipo: "sustantivo" },
  { p: "Corre", tipo: "verbo" }, { p: "Salta", tipo: "verbo" }, { p: "Come", tipo: "verbo" },
  { p: "Grande", tipo: "adjetivo" }, { p: "Rápido", tipo: "adjetivo" }, { p: "Lindo", tipo: "adjetivo" },
  { p: "Feliz", tipo: "adjetivo" }, // agregado 14-jul-2026 (banco ampliado de 9 a 10)
  // ampliado 20-jul-2026 (de 10 a 22 — engrosar bancos nodales, docs/auditoria-dc-caba/)
  { p: "Árbol", tipo: "sustantivo" }, { p: "Maestra", tipo: "sustantivo" }, { p: "Pelota", tipo: "sustantivo" },
  { p: "Río", tipo: "sustantivo" },
  { p: "Lee", tipo: "verbo" }, { p: "Escribe", tipo: "verbo" }, { p: "Canta", tipo: "verbo" },
  { p: "Duerme", tipo: "verbo" }, { p: "Juega", tipo: "verbo" },
  { p: "Alto", tipo: "adjetivo" }, { p: "Azul", tipo: "adjetivo" }, { p: "Suave", tipo: "adjetivo" },
];
GAMES.partes_oracion = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es sustantivo, adjetivo o verbo?", "f");
      ctx.juego.innerHTML = "";
      let disp = PARTES_ORACION_BANCO.filter((x) => !usados.includes(x.p));
      if (!disp.length) { usados = []; disp = PARTES_ORACION_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.p);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto anim-pop",
        `<span style="font-size:38px;font-family:'Baloo',sans-serif">${item.p}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle(["sustantivo", "adjetivo", "verbo"]).forEach((tipo) => {
        const b = el("button", "spriteBtn", `<span style="font-size:19px;font-family:'Baloo',sans-serif">${tipo}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (tipo === item.tipo) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── BÚSQUEDA DEL TESORO — tabla pitagórica (14-jul-2026, 3° grado NAP
   Bimestre 2 "Ideas web": "búsqueda del tesoro en la tabla pitagórica —
   tocar el casillero correcto"). Simplificado a una grilla de 9 resultados
   (no la tabla 10×10 completa — mismo criterio de tamaño de blanco táctil
   que ya usó grilla100 en 1° grado) con distractores que son productos
   REALES de otras tablas (no números al azar — un distractor de "37" sería
   obviamente falso, nunca aparece en ninguna tabla). ── */
GAMES.tabla_pitagorica = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.juego.innerHTML = "";
      const tabla = rint(2, 9);
      const factor = rint(2, 9);
      const correcta = tabla * factor;
      // consigna de audio FIJA (el "6 × 7" cambia cada ronda — no puede
      // grabarse, mismo criterio que "Formá {objetivo}" en sumas_redondas)
      consignaVariada(ctx, ronda, "Buscá el resultado de la multiplicación", "n");
      const arribaOp = el("div", "tablero");
      arribaOp.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:34px;font-family:'Baloo',sans-serif">${tabla} × ${factor}</span>`));
      ctx.juego.appendChild(arribaOp);
      const opciones = new Set([correcta]);
      let guardas = 0;
      while (opciones.size < 9 && guardas < 150) {
        guardas++;
        const v = rint(2, 9) * rint(2, 9);
        if (v !== correcta) opciones.add(v);
      }
      const grid = el("div", "grilla100 tablaPitagoricaGrid");
      let resuelto = false;
      shuffle([...opciones]).forEach((v) => {
        const c = el("div", "grilla100Celda tablaPitagoricaCelda", String(v));
        c.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === correcta) {
            resuelto = true;
            c.classList.add("anim-pop");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            c.style.animation = "sacudir .4s ease";
            setTimeout(() => (c.style.animation = ""), 450);
            ctx.casi();
          }
        });
        grid.appendChild(c);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(grid);
    };
    jugar();
  },
};

/* ── PASADO, PRESENTE O FUTURO (14-jul-2026, 3° grado NAP Bimestre 2
   "Ideas web": "clasificar verbos por tiempo verbal"). Mismo patrón de
   clasificar de 3 categorías que partes_oracion. ── */
const TIEMPOS_BANCO = [
  { p: "Corrí", tiempo: "pasado" }, { p: "Comí", tiempo: "pasado" }, { p: "Salté", tiempo: "pasado" },
  { p: "Corro", tiempo: "presente" }, { p: "Como", tiempo: "presente" }, { p: "Salto", tiempo: "presente" },
  { p: "Correré", tiempo: "futuro" }, { p: "Comeré", tiempo: "futuro" }, { p: "Saltaré", tiempo: "futuro" },
  { p: "Jugaré", tiempo: "futuro" }, // agregado 14-jul-2026 (banco ampliado de 9 a 10)
];
GAMES.tiempos_verbales = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Pasado, presente o futuro?", "f");
      ctx.juego.innerHTML = "";
      let disp = TIEMPOS_BANCO.filter((x) => !usados.includes(x.p));
      if (!disp.length) { usados = []; disp = TIEMPOS_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.p);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto anim-pop",
        `<span style="font-size:38px;font-family:'Baloo',sans-serif">${item.p}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle(["pasado", "presente", "futuro"]).forEach((tiempo) => {
        const b = el("button", "spriteBtn", `<span style="font-size:19px;font-family:'Baloo',sans-serif">${tiempo}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (tiempo === item.tiempo) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿QUÉ ESTACIÓN ES? (14-jul-2026, 3° grado NAP Bimestre 3 "Ideas web":
   "simular el movimiento de la Tierra para identificar estaciones" —
   simplificado a trivia de reconocimiento, sin simulación real del
   movimiento orbital). ── */
const ESTACIONES_BANCO = [
  { e: "☀️", estacion: "Verano" }, { e: "🍂", estacion: "Otoño" },
  { e: "⛄", estacion: "Invierno" }, { e: "🌷", estacion: "Primavera" },
  // agregados 14-jul-2026 (banco ampliado de 4 a 10 — más de un símbolo
  // por estación, no estaciones nuevas: solo hay 4). Los botones de
  // respuesta se dedupan en el propio juego (Set sobre "estacion").
  { e: "🏖️", estacion: "Verano" }, { e: "🕶️", estacion: "Verano" },
  { e: "🍁", estacion: "Otoño" }, { e: "🧣", estacion: "Otoño" },
  { e: "🧤", estacion: "Invierno" },
  { e: "🌸", estacion: "Primavera" },
];
GAMES.estaciones = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 4;
    ctx.rondas(rondas);
    const OPS = [...new Set(ESTACIONES_BANCO.map((x) => x.estacion))];
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Qué estación del año es?", "f");
      ctx.juego.innerHTML = "";
      let disp = ESTACIONES_BANCO.filter((x) => !usados.includes(x.e));
      if (!disp.length) { usados = []; disp = ESTACIONES_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.e);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto", `<span style="font-size:80px">${item.e}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle(OPS).forEach((op) => {
        const b = el("button", "spriteBtn", `<span style="font-size:19px;font-family:'Baloo',sans-serif">${op}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op === item.estacion) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── CARAS, VÉRTICES Y ARISTAS (14-jul-2026, 3° grado NAP Bimestre 3
   "Ideas web": "rotar cuerpos geométricos 3D y contar caras/aristas/
   vértices" — el motor no tiene render 3D en ningún lado, simplificado a
   conteo sobre una imagen fija; la rotación real queda deliberadamente
   afuera, ver informe). Consigna de audio FIJA y genérica — la pregunta
   específica (qué cuerpo, qué propiedad) se muestra en pantalla como texto
   dinámico, mismo criterio que "Formá {objetivo}" en sumas_redondas. ── */
const CUERPOS_BANCO = [
  { e: "🧊", nombre: "el cubo", caras: 6, vertices: 8, aristas: 12 },
  { e: "📦", nombre: "el prisma rectangular", caras: 6, vertices: 8, aristas: 12 },
  { e: "🔺", nombre: "la pirámide", caras: 5, vertices: 5, aristas: 8 },
];
GAMES.cuerpos_geometricos = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "Contá y elegí la respuesta correcta", "f");
      ctx.juego.innerHTML = "";
      const item = CUERPOS_BANCO[rint(0, CUERPOS_BANCO.length - 1)];
      const propKey = ["caras", "vertices", "aristas"][rint(0, 2)];
      const propLabel = { caras: "caras", vertices: "vértices", aristas: "aristas" }[propKey];
      const correcta = item[propKey];
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto", `
        <div style="font-size:70px">${item.e}</div>
        <div style="font-size:19px;font-family:'Baloo',sans-serif;margin-top:8px">¿Cuántas ${propLabel} tiene ${item.nombre}?</div>`));
      ctx.juego.appendChild(arriba);
      const opciones = new Set([correcta]);
      let guardas = 0;
      while (opciones.size < 3 && guardas < 50) {
        guardas++;
        const v = Math.max(1, correcta + rint(-3, 3));
        if (v !== correcta) opciones.add(v);
      }
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle([...opciones]).forEach((v) => {
        const b = el("button", "spriteBtn", `<span style="font-size:26px;font-family:'Baloo',sans-serif">${v}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === correcta) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── SEPARADOR DE MEZCLAS (14-jul-2026, 3° grado NAP Bimestre 4 "Ideas
   web": "separador de mezclas virtual — arrastrar colador/imán/filtro").
   Adaptado a tap (mismo criterio que agrupar: sin drag real, más robusto
   en mobile) — texto en vez de emoji para la mezcla, no hay glifo preciso
   para "limaduras de hierro y arena". ── */
const MEZCLAS_BANCO = [
  { mezcla: "Fideos en agua", herramienta: "Colador" },
  { mezcla: "Limaduras de hierro y arena", herramienta: "Imán" },
  { mezcla: "Café molido y agua", herramienta: "Filtro" },
  { mezcla: "Papas hervidas y agua", herramienta: "Colador" },
  // agregados 14-jul-2026 (banco ampliado de 4 a 10). HERRAMIENTAS es una
  // lista fija de 3 botones (Colador/Imán/Filtro) — cualquier ítem nuevo
  // tiene que usar exactamente una de esas 3, nunca una categoría nueva.
  { mezcla: "Arroz cocido y agua", herramienta: "Colador" },
  { mezcla: "Verduras hervidas y agua", herramienta: "Colador" },
  { mezcla: "Clavos de metal y arena", herramienta: "Imán" },
  { mezcla: "Tachuelas y aserrín", herramienta: "Imán" },
  { mezcla: "Agua turbia con tierra fina", herramienta: "Filtro" },
  { mezcla: "Té y agua", herramienta: "Filtro" },
];
GAMES.separador_mezclas = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 4;
    ctx.rondas(rondas);
    const HERRAMIENTAS = ["Colador", "Imán", "Filtro"];
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Con qué herramienta separás esta mezcla?", "f");
      ctx.juego.innerHTML = "";
      let disp = MEZCLAS_BANCO.filter((x) => !usados.includes(x.mezcla));
      if (!disp.length) { usados = []; disp = MEZCLAS_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.mezcla);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:24px;font-family:'Baloo',sans-serif">${item.mezcla}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle(HERRAMIENTAS).forEach((h) => {
        const b = el("button", "spriteBtn", `<span style="font-size:20px;font-family:'Baloo',sans-serif">${h}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (h === item.herramienta) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── CAJERO AUTOMÁTICO (14-jul-2026, 3° grado NAP Bimestre 4 "Ideas web":
   "retirar la combinación exacta de billetes"). Mismo patrón probado de
   suma_rapida/sumas_redondas (tocar 2 que sumen el objetivo) con billetes
   en vez de números — de paso resuelve "la tiendita" que había quedado
   pendiente del backlog de 1° grado (mismo mecanismo, distinto disfraz). ── */
GAMES.cajero_automatico = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    const BILLETES = [10, 20, 50, 100, 200, 500, 1000];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "Tocá los billetes que sumen el monto exacto", "n");
      ctx.juego.innerHTML = "";
      const idxA = rint(0, BILLETES.length - 1);
      let idxB = rint(0, BILLETES.length - 1);
      while (idxB === idxA) idxB = rint(0, BILLETES.length - 1);
      const a = BILLETES[idxA], b = BILLETES[idxB];
      const objetivo = a + b;
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:32px;font-family:'Baloo',sans-serif">Retirá $${objetivo}</span>`));
      ctx.juego.appendChild(arriba);
      let nums = [a, b];
      let guardas = 0;
      while (nums.length < 5 && guardas < 100) {
        guardas++;
        const v = BILLETES[rint(0, BILLETES.length - 1)];
        if (!nums.includes(v) && !nums.some((n) => n + v === objetivo)) nums.push(v);
      }
      nums = shuffle(nums);
      const fila = el("div", "filaSprites");
      let elegido = null;
      let resuelto = false;
      nums.forEach((v, idx) => {
        const btn = el("button", "spriteBtn", `<span style="font-size:20px;font-family:'Baloo',sans-serif">$${v}</span>`);
        btn.addEventListener("click", async () => {
          if (resuelto || btn.disabled) return;
          if (elegido === null) {
            elegido = { idx, v, btn };
            btn.classList.add("elegido");
            return;
          }
          if (elegido.idx === idx) return;
          if (elegido.v + v === objetivo) {
            resuelto = true;
            btn.disabled = true;
            elegido.btn.disabled = true;
            btn.classList.add("anim-pop");
            elegido.btn.classList.add("anim-pop");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            const prevBtn = elegido.btn;   // capturar ANTES de resetear (bug real de suma_rapida)
            prevBtn.classList.remove("elegido");
            btn.style.animation = "sacudir .4s ease";
            prevBtn.style.animation = "sacudir .4s ease";
            setTimeout(() => { btn.style.animation = ""; prevBtn.style.animation = ""; }, 450);
            ctx.casi();
            elegido = null;
          }
        });
        fila.appendChild(btn);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ABSTRACTO O CONCRETO (14-jul-2026, 4° grado NAP Bimestre 1 "Ideas
   web": "clasificador de sustantivos abstractos vs. concretos"). Mismo
   patrón de clasificar 2 categorías que campo_ciudad. ── */
const ABSTRACTOS_BANCO = [
  { p: "Amor", tipo: "abstracto" }, { p: "Alegría", tipo: "abstracto" }, { p: "Libertad", tipo: "abstracto" },
  { p: "Amistad", tipo: "abstracto" },
  { p: "Mesa", tipo: "concreto" }, { p: "Perro", tipo: "concreto" }, { p: "Árbol", tipo: "concreto" },
  { p: "Pelota", tipo: "concreto" },
  // agregados 14-jul-2026 (banco ampliado de 8 a 10).
  { p: "Justicia", tipo: "abstracto" }, { p: "Silla", tipo: "concreto" },
];
GAMES.abstractos_concretos = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es abstracto o concreto?", "f");
      ctx.juego.innerHTML = "";
      let disp = ABSTRACTOS_BANCO.filter((x) => !usados.includes(x.p));
      if (!disp.length) { usados = []; disp = ABSTRACTOS_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.p);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto anim-pop",
        `<span style="font-size:36px;font-family:'Baloo',sans-serif">${item.p}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle(["abstracto", "concreto"]).forEach((tipo) => {
        const b = el("button", "spriteBtn", `<span style="font-size:20px;font-family:'Baloo',sans-serif">${tipo}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (tipo === item.tipo) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿DE QUÉ REGIÓN ES? (14-jul-2026, 4° grado NAP Bimestre 1 "Ideas web":
   "rompecabezas geográfico — encastrar provincias en el mapa nacional").
   Simplificado a trivia de región (Norte/Centro/Cuyo/Patagonia) — un mapa
   con las 24 provincias reales requiere un asset de geografía precisa que
   el motor no tiene (no es un juego nuevo, es un asset nuevo — ver informe). ── */
const PROVINCIAS_BANCO = [
  { p: "Salta", region: "Norte" }, { p: "Jujuy", region: "Norte" }, { p: "Misiones", region: "Norte" },
  { p: "Buenos Aires", region: "Centro" }, { p: "Córdoba", region: "Centro" }, { p: "Santa Fe", region: "Centro" },
  { p: "Mendoza", region: "Cuyo" }, { p: "San Juan", region: "Cuyo" },
  { p: "Chubut", region: "Patagonia" }, { p: "Santa Cruz", region: "Patagonia" },
];
GAMES.provincias_region = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    const REGIONES = ["Norte", "Centro", "Cuyo", "Patagonia"];
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿A qué región pertenece esta provincia?", "f");
      ctx.juego.innerHTML = "";
      let disp = PROVINCIAS_BANCO.filter((x) => !usados.includes(x.p));
      if (!disp.length) { usados = []; disp = PROVINCIAS_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.p);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:28px;font-family:'Baloo',sans-serif">${item.p}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle(REGIONES).forEach((r) => {
        const b = el("button", "spriteBtn", `<span style="font-size:18px;font-family:'Baloo',sans-serif">${r}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (r === item.region) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── AGUDA, GRAVE O ESDRÚJULA (14-jul-2026, 4° grado NAP Bimestre 2 "Ideas
   web": "clasificar palabras por acentuación en el tren correcto"). Mismo
   patrón de clasificar 3 categorías que partes_oracion. ── */
const ACENTUACION_BANCO = [
  { p: "Camión", tipo: "aguda" }, { p: "Café", tipo: "aguda" }, { p: "Jardín", tipo: "aguda" },
  { p: "Mesa", tipo: "grave" }, { p: "Lápiz", tipo: "grave" }, { p: "Árbol", tipo: "grave" },
  { p: "Música", tipo: "esdrújula" }, { p: "Teléfono", tipo: "esdrújula" }, { p: "Pájaro", tipo: "esdrújula" },
  { p: "Álbum", tipo: "grave" }, // agregado 14-jul-2026 (banco ampliado de 9 a 10)
  // ampliado 20-jul-2026 (de 10 a 24 — engrosar bancos nodales, docs/auditoria-dc-caba/)
  { p: "Reloj", tipo: "aguda" }, { p: "Corazón", tipo: "aguda" }, { p: "Compás", tipo: "aguda" },
  { p: "Sillón", tipo: "aguda" }, { p: "Feliz", tipo: "aguda" }, { p: "Canción", tipo: "aguda" },
  { p: "Azúcar", tipo: "grave" }, { p: "Difícil", tipo: "grave" }, { p: "Cárcel", tipo: "grave" },
  { p: "Útil", tipo: "grave" }, { p: "Goma", tipo: "grave" },
  { p: "Brújula", tipo: "esdrújula" }, { p: "Sábana", tipo: "esdrújula" }, { p: "Matemática", tipo: "esdrújula" },
  { p: "Relámpago", tipo: "esdrújula" }, { p: "Océano", tipo: "esdrújula" },
];
GAMES.acentuacion = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es aguda, grave o esdrújula?", "f");
      ctx.juego.innerHTML = "";
      let disp = ACENTUACION_BANCO.filter((x) => !usados.includes(x.p));
      if (!disp.length) { usados = []; disp = ACENTUACION_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.p);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto anim-pop",
        `<span style="font-size:36px;font-family:'Baloo',sans-serif">${item.p}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle(["aguda", "grave", "esdrújula"]).forEach((tipo) => {
        const b = el("button", "spriteBtn", `<span style="font-size:18px;font-family:'Baloo',sans-serif">${tipo}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (tipo === item.tipo) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── LA SÍLABA TÓNICA (3° grado — docs/auditoria-dc-caba/grado-3.md, gap #2: la
   acentuación es "el contenido estrella de Lengua 3°, con gamificables obvios
   (tocar la sílaba tónica), sin una sola actividad"). A diferencia de acentuacion
   (4°, que CLASIFICA la palabra dada), acá el chico IDENTIFICA dónde está la fuerza
   tocando la sílaba tónica entre las sílabas de la palabra — la base antes de
   clasificar. Al acertar se nombra el tipo (aguda/grave/esdrújula). Capa 0 C3: el
   error dice dónde está la fuerza y por qué es de ese tipo. ── */
const SILABA_TONICA_BANCO = [
  { s: ["ca", "mión"], t: 1, tipo: "aguda" }, { s: ["ca", "fé"], t: 1, tipo: "aguda" },
  { s: ["jar", "dín"], t: 1, tipo: "aguda" }, { s: ["re", "loj"], t: 1, tipo: "aguda" },
  { s: ["pa", "red"], t: 1, tipo: "aguda" },
  { s: ["me", "sa"], t: 0, tipo: "grave" }, { s: ["lá", "piz"], t: 0, tipo: "grave" },
  { s: ["ár", "bol"], t: 0, tipo: "grave" }, { s: ["pe", "rro"], t: 0, tipo: "grave" },
  { s: ["ven", "ta", "na"], t: 1, tipo: "grave" }, { s: ["cua", "der", "no"], t: 1, tipo: "grave" },
  { s: ["mú", "si", "ca"], t: 0, tipo: "esdrújula" }, { s: ["te", "lé", "fo", "no"], t: 1, tipo: "esdrújula" },
  { s: ["pá", "ja", "ro"], t: 0, tipo: "esdrújula" }, { s: ["brú", "ju", "la"], t: 0, tipo: "esdrújula" },
  { s: ["sá", "ba", "na"], t: 0, tipo: "esdrújula" },
];
GAMES.silaba_tonica = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const POS = { aguda: "la ÚLTIMA", grave: "la ANTEÚLTIMA", "esdrújula": "la ANTEPENÚLTIMA" };
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.consigna("Tocá la sílaba que suena MÁS FUERTE.");
      ctx.juego.innerHTML = "";
      let libres = SILABA_TONICA_BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!libres.length) { usados = []; libres = SILABA_TONICA_BANCO.map((_, i) => i); }
      const idx = libres[rint(0, libres.length - 1)]; usados.push(idx);
      const it = SILABA_TONICA_BANCO[idx];
      ctx.item("tonica#" + idx);
      const palabra = it.s.join("");
      const arriba = el("div", "tablero");
      const fila = el("div", "filaPalabras");
      fila.setAttribute("data-t", it.t);
      let resuelto = false;
      it.s.forEach((sil, i) => {
        const chip = el("button", "palabraChip", sil);
        chip.addEventListener("click", async () => {
          if (resuelto) return;
          if (i === it.t) {
            resuelto = true; chip.classList.add("tonica");
            ctx.bien(`¡Sí! «${palabra}» es ${it.tipo}.`);
            ronda++; await espera(1050);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else {
            chip.classList.add("casi-chip"); setTimeout(() => chip.classList.remove("casi-chip"), 450);
            ctx.casi(`En «${palabra}» la fuerza está en «${it.s[it.t]}» (${POS[it.tipo]}): es ${it.tipo}.`);
          }
        });
        fila.appendChild(chip);
      });
      arriba.appendChild(fila);
      ctx.juego.appendChild(arriba);
      const nota = el("div", "tonica-nota",
        "Aguda = fuerza en la última · Grave = en la anteúltima · Esdrújula = en la antepenúltima");
      ctx.juego.appendChild(el("div", "tablero")).appendChild(nota);
    };
    jugar();
  },
};

/* ── FOTOSÍNTESIS — EL INTRUSO (14-jul-2026, 4° grado NAP Bimestre 2
   "Ideas web": "simulador de fotosíntesis — colocar agua, sol, CO2 en una
   planta virtual"). Simplificado de simulación multi-paso a "odd one out"
   (mismo concepto que el juego `diferente` de las bandas mini/media, pero
   con contenido curricular real en vez de sprites decorativos del tema):
   tocar lo que la planta NO necesita entre 3 correctos + 1 intruso. ── */
const FOTOSINTESIS_NECESARIOS = ["💧", "☀️", "🌬️"];
const FOTOSINTESIS_INTRUSOS = ["🍖", "🪨", "🚗", "📱", "👟"];
GAMES.fotosintesis = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Cuál de estos NO necesita la planta para hacer la fotosíntesis?", "n");
      ctx.juego.innerHTML = "";
      let disp = FOTOSINTESIS_INTRUSOS.filter((x) => !usados.includes(x));
      if (!disp.length) { usados = []; disp = FOTOSINTESIS_INTRUSOS; }
      const intruso = disp[rint(0, disp.length - 1)];
      usados.push(intruso);
      const opciones = shuffle([...FOTOSINTESIS_NECESARIOS, intruso]);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      opciones.forEach((op) => {
        const b = el("button", "spriteBtn", `<span style="font-size:44px">${op}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op === intruso) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── LABORATORIO ELÉCTRICO (14-jul-2026, 4° grado NAP Bimestre 3 "Ideas
   web": "conectar cables a materiales para ver qué enciende una
   lamparita" — simplificado a clasificar, mismo patrón que
   conductor_aislante de 2° grado, banco de contenido nuevo).
   Consigna reescrita 15-jul-2026 (Pablo: "en lugar de esto enciende la
   lamparita o no, que diga este es material que conduce electricidad")
   — nombra el concepto curricular directo en vez de la metáfora. ── */
const ELECTRICO_BANCO = [
  { e: "🔑", cat: "conduce" }, { e: "🥄", cat: "conduce" }, { e: "🪙", cat: "conduce" }, { e: "🔩", cat: "conduce" },
  { e: "📖", cat: "noconduce" }, { e: "🧦", cat: "noconduce" }, { e: "🪵", cat: "noconduce" }, { e: "🎈", cat: "noconduce" },
  // agregados 14-jul-2026 (banco ampliado de 8 a 10).
  { e: "🥫", cat: "conduce" }, { e: "🎋", cat: "noconduce" },
];
GAMES.laboratorio_electrico = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Este material conduce electricidad?", "m");
      ctx.juego.innerHTML = "";
      let disp = ELECTRICO_BANCO.filter((x) => !usados.includes(x.e));
      if (!disp.length) { usados = []; disp = ELECTRICO_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.e);
      const arriba = el("div", "tablero");
      const cont = el("div", "spriteQuieto anim-pop", `<span style="font-size:80px">${item.e}</span>`);
      arriba.appendChild(cont);
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      [{ cat: "conduce", label: "⚡ Conduce" }, { cat: "noconduce", label: "🚫 No conduce" }].forEach(({ cat, label }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:17px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (cat === item.cat) {
            resuelto = true;
            cont.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── FRACCIONES EQUIVALENTES (14-jul-2026, 4° grado NAP Bimestre 3 "Ideas
   web": "equivalencias de fracciones — emparejar 2/4 con 1/2"). PRIMERA
   representación visual de fracciones del motor — no negociable mostrar
   solo el número (regla CPA del skill §4b/4c: matemática nueva necesita
   apoyo Pictórico, no solo símbolo). Barras divididas en segmentos, no
   pizza — más simple de dibujar en CSS puro y es la herramienta CPA
   estándar (Singapore Math "fraction bars"). Banco de distractores
   ESCRITO A MANO (no generado): con fracciones, un distractor generado al
   azar puede terminar siendo por coincidencia matemáticamente equivalente
   igual (ej. la "complementaria" de 1/2 es 1/2) — más seguro autorearlos. ── */
const FRACCIONES_BANCO = [
  { num: 1, den: 2, eq: { num: 2, den: 4 }, d1: { num: 1, den: 4 }, d2: { num: 3, den: 4 } },
  { num: 1, den: 3, eq: { num: 2, den: 6 }, d1: { num: 1, den: 6 }, d2: { num: 3, den: 6 } },
  { num: 2, den: 3, eq: { num: 4, den: 6 }, d1: { num: 3, den: 6 }, d2: { num: 5, den: 6 } },
  { num: 1, den: 4, eq: { num: 2, den: 8 }, d1: { num: 1, den: 8 }, d2: { num: 3, den: 8 } },
  { num: 3, den: 4, eq: { num: 6, den: 8 }, d1: { num: 5, den: 8 }, d2: { num: 7, den: 8 } },
  { num: 1, den: 5, eq: { num: 2, den: 10 }, d1: { num: 1, den: 10 }, d2: { num: 3, den: 10 } },
  { num: 2, den: 5, eq: { num: 4, den: 10 }, d1: { num: 3, den: 10 }, d2: { num: 5, den: 10 } },
  { num: 3, den: 5, eq: { num: 6, den: 10 }, d1: { num: 5, den: 10 }, d2: { num: 7, den: 10 } },
  { num: 4, den: 5, eq: { num: 8, den: 10 }, d1: { num: 7, den: 10 }, d2: { num: 9, den: 10 } },
  { num: 1, den: 6, eq: { num: 2, den: 12 }, d1: { num: 1, den: 12 }, d2: { num: 3, den: 12 } },
  { num: 5, den: 6, eq: { num: 10, den: 12 }, d1: { num: 9, den: 12 }, d2: { num: 11, den: 12 } },
  { num: 1, den: 2, eq: { num: 3, den: 6 }, d1: { num: 2, den: 6 }, d2: { num: 4, den: 6 } },
  { num: 1, den: 3, eq: { num: 3, den: 9 }, d1: { num: 2, den: 9 }, d2: { num: 4, den: 9 } },
  { num: 2, den: 3, eq: { num: 6, den: 9 }, d1: { num: 5, den: 9 }, d2: { num: 7, den: 9 } },
  { num: 1, den: 4, eq: { num: 3, den: 12 }, d1: { num: 2, den: 12 }, d2: { num: 4, den: 12 } },
  { num: 3, den: 4, eq: { num: 9, den: 12 }, d1: { num: 8, den: 12 }, d2: { num: 10, den: 12 } },
  { num: 1, den: 2, eq: { num: 4, den: 8 }, d1: { num: 3, den: 8 }, d2: { num: 5, den: 8 } },
  { num: 1, den: 3, eq: { num: 4, den: 12 }, d1: { num: 3, den: 12 }, d2: { num: 5, den: 12 } },
  { num: 2, den: 3, eq: { num: 8, den: 12 }, d1: { num: 7, den: 12 }, d2: { num: 9, den: 12 } },
  { num: 1, den: 2, eq: { num: 5, den: 10 }, d1: { num: 4, den: 10 }, d2: { num: 6, den: 10 } },
  { num: 1, den: 2, eq: { num: 6, den: 12 }, d1: { num: 5, den: 12 }, d2: { num: 7, den: 12 } },
  { num: 2, den: 6, eq: { num: 4, den: 12 }, d1: { num: 3, den: 12 }, d2: { num: 5, den: 12 } },
  { num: 3, den: 6, eq: { num: 6, den: 12 }, d1: { num: 5, den: 12 }, d2: { num: 7, den: 12 } },
  { num: 2, den: 4, eq: { num: 6, den: 12 }, d1: { num: 5, den: 12 }, d2: { num: 7, den: 12 } }
];
GAMES.fracciones_equivalentes = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    const barra = (num, den) => {
      const cont = el("div", "fraccionBarra");
      for (let i = 0; i < den; i++) cont.appendChild(el("div", "fraccionBarra__seg" + (i < num ? " lleno" : "")));
      return cont;
    };
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Cuál de estas barras muestra la misma fracción?", "f");
      ctx.juego.innerHTML = "";
      let disp = FRACCIONES_BANCO.filter((x) => !usados.includes(x.num + "/" + x.den));
      if (!disp.length) { usados = []; disp = FRACCIONES_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.num + "/" + item.den);
      const arriba = el("div", "tablero");
      arriba.appendChild(barra(item.num, item.den));
      ctx.juego.appendChild(arriba);
      const opciones = shuffle([item.eq, item.d1, item.d2]);
      const fila = el("div", "filaSprites fraccionesOpciones");
      let resuelto = false;
      opciones.forEach((op) => {
        const b = el("button", "spriteBtn fraccionBtn");
        b.appendChild(barra(op.num, op.den));
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op.num === item.eq.num && op.den === item.eq.den) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── SUMA EN COLUMNAS (15-jul-2026, 4° grado NAP Bimestre 1: "números hasta
   10.000-50.000... propiedades de suma y resta"). Reemplaza acá el `sumas`
   genérico (conteo de sprites, tope=10 fijo para TODOS los grados 1°-7°) —
   Pablo probándolo en vivo: "las sumas en 4° grado son de 4 a 5 cifras y
   parecen muy fáciles para esa edad". Contar iconitos no escala a 4-5
   cifras (nadie toca 12.345 sprites) — hace falta el algoritmo ESCRITO.
   Representación Pictórica no negociable (skill §2.3, Singapore Math CPA):
   columnas rotuladas con su potencia de 10 (U/D/C/UM/DM = ×1/×10/.../
   ×10.000, el eje curricular exacto del bimestre) y el acarreo se VE como
   insignia "+1" sobre la columna siguiente, nunca un cálculo invisible.
   Se resuelve de derecha a izquierda (unidades primero, como el algoritmo
   real) aunque el número se lea de izquierda a derecha. Andamiaje = botón
   "Ayuda" a pedido (tabla de dosificación skill §3, banda 8-9 años:
   "pista solo a pedido"), no automática. Cero fail states: un toque
   incorrecto sacude y deja reintentar la MISMA columna, sin límite. ── */
const SUMA_COL_NOMBRE = ["U", "D", "C", "UM", "DM"];
const SUMA_COL_LARGO = ["unidades", "decenas", "centenas", "unidades de mil", "decenas de mil"];
const SUMA_COL_POTENCIA = ["×1", "×10", "×100", "×1.000", "×10.000"];
// números en palabra (0-18, el resultado de sumar dos cifras + acarreo nunca
// pasa de 18) — para narrar la lección con audio grabado (generar_audio_
// consignas en actividades_web.py tiene las frases EXACTAS que arman con
// estas palabras, no se puede cambiar una lista sin regenerar la otra).
const NUM_PALABRA = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
  "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho"];
const SUMA_COL_CORTAS = ["Empezá por las unidades", "¿Y esta cuenta?", "Otra vez, por las unidades", "¿Y esta suma?"];
GAMES.suma_columnas = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let ronda = 0;
    // gutter: celda IGUAL en las 5 filas (ancho fijo) — el "+" de la fila B
    // vive ADENTRO de esta celda como cualquier otra, no como hermano extra
    // que desalinea el centrado del resto (bug real 15-jul-2026: Pablo
    // "los números de sumas no están alineados" — el "+" empujaba SOLO la
    // fila B unos px a la derecha del resto al centrarse cada fila sola).
    const gutter = (txt) => el("div", "sumaColGutter", txt || "");
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.juego.innerHTML = "";
      if (ronda === 0) {
        ctx.consigna('Sumá las dos cifras: empezá por las UNIDADES (a la derecha) y andá columna por columna. Si te trabás dos veces, te lo explico paso a paso.');
      } else {
        ctx.consigna(sacarDeBolsa(ctx, "sumacol", SUMA_COL_CORTAS));
      }
      // dificultad: últimas rondas van a 5 cifras (NAP: "hasta 10.000-50.000").
      const dif = (ronda + 1) / rondas;
      // rango configurable por cfg — 3° usa 3→4 cifras (hasta 10.000, gap #1 del DC
      // de 3°); 4° queda con el default 4→5 cifras. Sin cfg = comportamiento original.
      const cifrasMin = ctx.cfg.cifrasMin || 4;
      const cifrasMax = ctx.cfg.cifrasMax || 5;
      const cifras = dif <= 0.5 ? cifrasMin : cifrasMax;
      const piso = 10 ** (cifras - 1);
      const tope = cifras >= 5 ? 49999 : (10 ** cifras - 1);
      const a = rint(piso, tope);
      const b = rint(piso, tope);
      const suma = a + b;
      const ancho = Math.max(String(a).length, String(b).length, String(suma).length);
      const cifraEn = (n, i) => Math.floor(n / 10 ** i) % 10;   // i-ésima cifra desde la derecha (0=U)
      // precalcula acarreos: acarreo[i] = lo que se lleva DE la columna i A la i+1
      const acarreo = [];
      let c = 0;
      for (let i = 0; i < ancho; i++) {
        const total = cifraEn(a, i) + cifraEn(b, i) + c;
        c = total >= 10 ? 1 : 0;
        acarreo[i] = c;
      }
      const tablero = el("div", "tablero sumaColTablero");
      const encabezado = el("div", "sumaColGrid sumaColEncabezado");
      const filaAcarreos = el("div", "sumaColGrid sumaColAcarreos");
      const filaA = el("div", "sumaColGrid");
      const filaB = el("div", "sumaColGrid");
      const filaResultado = el("div", "sumaColGrid");
      encabezado.appendChild(gutter());
      filaAcarreos.appendChild(gutter());
      filaA.appendChild(gutter());
      filaB.appendChild(gutter("+"));
      filaResultado.appendChild(gutter());
      const acarreoBadges = [], slots = [], digitosA = [], digitosB = [];
      for (let i = ancho - 1; i >= 0; i--) {
        const col = el("div", "sumaColEncabezado__col",
          `<span class="sumaColEncabezado__nombre">${SUMA_COL_NOMBRE[i]}</span><span class="sumaColEncabezado__potencia">${SUMA_COL_POTENCIA[i]}</span>`);
        encabezado.appendChild(col);
        const badge = el("div", "sumaColAcarreo sumaColAcarreo--oculto", "+1");
        acarreoBadges[i] = badge;
        filaAcarreos.appendChild(badge);
        const digA = el("div", "sumaDigito" + (i >= String(a).length ? " sumaDigito--vacio" : ""),
          i < String(a).length ? String(cifraEn(a, i)) : "");
        digitosA[i] = digA;
        filaA.appendChild(digA);
        const digB = el("div", "sumaDigito" + (i >= String(b).length ? " sumaDigito--vacio" : ""),
          i < String(b).length ? String(cifraEn(b, i)) : "");
        digitosB[i] = digB;
        filaB.appendChild(digB);
        const slot = el("div", "sumaResultado__slot", "");
        slots[i] = slot;
        filaResultado.appendChild(slot);
      }
      tablero.appendChild(encabezado);
      tablero.appendChild(filaAcarreos);
      tablero.appendChild(filaA);
      tablero.appendChild(filaB);
      tablero.appendChild(el("div", "sumaColLinea"));
      tablero.appendChild(filaResultado);
      const leccionBox = el("div", "sumaColLeccion sumaColLeccion--oculto", "");
      tablero.appendChild(leccionBox);
      const btnAyuda = el("button", "btn suave sumaColAyuda", "💡 Ayuda");
      btnAyuda.type = "button";
      tablero.appendChild(btnAyuda);
      const keypad = el("div", "filaSprites sumaColKeypad");
      const botones = [];
      for (let d = 0; d <= 9; d++) {
        const btn = el("button", "spriteBtn sumaColDigitBtn", String(d));
        botones.push(btn);
        keypad.appendChild(btn);
      }
      tablero.appendChild(keypad);
      ctx.juego.appendChild(tablero);

      let activa = 0;   // índice de columna activa (0 = unidades, sube hacia la izquierda)
      let resuelto = false;
      let fallosCol = 0;   // se resetea al cambiar de columna o tras dar la lección
      const marcarActiva = () => {
        slots.forEach((s, i) => s.classList.toggle("activo", i === activa && !resuelto));
      };
      marcarActiva();
      const habilitarControles = (on) => {
        botones.forEach((b) => (b.disabled = !on));
        btnAyuda.disabled = !on;
      };
      const resolverColumna = async (digito) => {
        if (resuelto) return;
        fallosCol = 0;
        slots[activa].textContent = String(digito);
        slots[activa].classList.add("anim-pop");
        if (acarreo[activa] && activa + 1 < ancho) acarreoBadges[activa + 1].classList.remove("sumaColAcarreo--oculto");
        Sfx.tick(activa + 1);
        activa++;
        if (activa >= ancho) {
          resuelto = true;
          ctx.bien();
          ronda++;
          await espera(1100);
          if (ronda >= rondas) ctx.win();
          else jugar();
        } else {
          marcarActiva();
        }
      };
      // "Lección" (15-jul-2026, Pablo: si se equivoca 2 veces en la misma
      // columna, explicarle CÓMO se suma esa columna, con animación
      // marcando los números Y AUDIO — "el audio además de la explicación
      // visual le va a dar más tiempo de entender". Resalta cada dígito en
      // el orden en que se suman de verdad, con narración grabada (misma
      // voz argentina de siempre, NO speechSynthesis del navegador —
      // frases CHICAS y fijas encadenadas, no se puede pre-grabar
      // "3 + 6 = 9" para cada combinación posible de dos números).
      // decirYesperar: espera a que la frase TERMINE DE SONAR de verdad (no
      // una pausa fija a ojo) antes de seguir — si no hay audio (mute, sin
      // manifest, etc.) usa `pausaSinAudio` como respaldo para que el texto
      // solo también tenga tiempo de leerse.
      const decirYesperar = async (txt, pausaSinAudio) => {
        const sonó = await reproducirConsigna(txt);
        await espera(sonó ? 450 : pausaSinAudio);
      };
      const leccion = async (col) => {
        habilitarControles(false);
        const da = cifraEn(a, col), db = cifraEn(b, col), ac = col > 0 ? acarreo[col - 1] : 0;
        const total = da + db + ac;
        leccionBox.classList.remove("sumaColLeccion--oculto");
        leccionBox.textContent = "";
        // mismo texto que ctx.consigna pondría arriba, pero SIN pasar por
        // ella — así se puede esperar el audio real con decirYesperar en
        // vez de la pausa fija vieja (Pablo 15-jul-2026: quedaba una pausa
        // rara entre "vamos paso a paso" y "primero...").
        const intro = `Vamos paso a paso con las ${SUMA_COL_LARGO[col]}.`;
        $("#consignaTexto").innerHTML = intro;
        $("#consignaPista").style.display = "none";
        await decirYesperar(intro, 1200);
        digitosA[col].classList.add("sumaResaltado");
        leccionBox.textContent = `${da}`;
        await decirYesperar(`Primero, ${NUM_PALABRA[da]}.`, 1300);
        digitosB[col].classList.add("sumaResaltado");
        leccionBox.textContent = ac ? `${da} + ${db} + 1 (que llevábamos)` : `${da} + ${db}`;
        await decirYesperar(ac ? `Más ${NUM_PALABRA[db]}, y el uno que llevábamos.` : `Más ${NUM_PALABRA[db]}.`, 1800);
        leccionBox.textContent = `${da} + ${db}${ac ? " + 1" : ""} = ${total}`;
        await decirYesperar(`Son ${NUM_PALABRA[total]}.`, 1600);
        if (total >= 10) {
          leccionBox.textContent = `Anotamos el ${total % 10} y llevamos 1 a la próxima columna`;
          if (activa + 1 < ancho) acarreoBadges[activa + 1].classList.add("sumaResaltado");
          await decirYesperar(`Anotamos el ${NUM_PALABRA[total % 10]}.`, 1600);
          await decirYesperar("Y llevamos uno a la próxima columna.", 1800);
        } else {
          leccionBox.textContent = `Anotamos el ${total}`;
          await decirYesperar(`Anotamos el ${NUM_PALABRA[total]}.`, 1800);
        }
        digitosA[col].classList.remove("sumaResaltado");
        digitosB[col].classList.remove("sumaResaltado");
        if (activa + 1 < ancho) acarreoBadges[activa + 1].classList.remove("sumaResaltado");
        leccionBox.classList.add("sumaColLeccion--oculto");
        fallosCol = 0;
        ctx.consigna("Ahora probá vos: tocá el número que va en esta columna.");
        habilitarControles(true);
      };
      botones.forEach((btn, d) => {
        btn.addEventListener("click", () => {
          if (resuelto) return;
          const correcta = cifraEn(suma, activa);
          if (d === correcta) resolverColumna(d);
          else {
            btn.style.animation = "sacudir .4s ease";
            setTimeout(() => (btn.style.animation = ""), 450);
            ctx.casi();
            fallosCol++;
            if (fallosCol >= 2) leccion(activa);
          }
        });
      });
      btnAyuda.addEventListener("click", () => resolverColumna(cifraEn(suma, activa)));
    };
    jugar();
  },
};

/* ── RESTA CON PRÉSTAMO EN COLUMNA (3° grado — docs/auditoria-dc-caba/grado-3.md,
   gap #1/#3: el DC de 3° pide el algoritmo de resta con préstamo hasta 10.000 y no
   existía). Espeja el motor de suma_columnas (grilla alineada + keypad + Ayuda tras
   2 errores) pero restando: cuando una columna no alcanza, se pide prestado 1 a la
   izquierda (badge "−1" sobre esa columna). El dígito correcto de cada columna es la
   cifra de a−b. Rango por cfg (3°: 3→4 cifras). La Ayuda narra con TTS dinámico (no
   hay audio pre-grabado de resta como en suma). Capa 0: cada tap errado baja la
   estrella al primer intento (C2), la Ayuda explica el porqué (C3). ── */
const RESTA_COL_CORTAS = ["¿Y esta resta?", "Otra vez, por las unidades", "¿Y esta cuenta?", "Seguimos restando"];
GAMES.resta_columnas = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let ronda = 0;
    const gutter = (txt) => el("div", "sumaColGutter", txt || "");
    const cifraEn = (n, i) => Math.floor(n / 10 ** i) % 10;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.juego.innerHTML = "";
      ctx.consigna(ronda === 0
        ? "Restá columna por columna, empezá por las UNIDADES (a la derecha). Si no te alcanza, te prestás 1 de la izquierda."
        : sacarDeBolsa(ctx, "restacol", RESTA_COL_CORTAS));
      const cifrasMin = ctx.cfg.cifrasMin || 3;
      const cifrasMax = ctx.cfg.cifrasMax || 4;
      const dif = (ronda + 1) / rondas;
      const cifras = dif <= 0.5 ? cifrasMin : cifrasMax;
      const piso = 10 ** (cifras - 1);
      const tope = 10 ** cifras - 1;
      const a = rint(piso + 1, tope);
      const b = rint(piso, a - 1);            // minuendo > sustraendo → resultado positivo
      const resta = a - b;
      const ancho = String(a).length;
      // préstamo[i] = 1 si la columna i tuvo que pedir prestado a la de su izquierda.
      const prestamo = [];
      let pide = 0;
      for (let i = 0; i < ancho; i++) {
        const top = cifraEn(a, i) - pide;
        pide = top < cifraEn(b, i) ? 1 : 0;
        prestamo[i] = pide;
      }
      const tablero = el("div", "tablero sumaColTablero");
      const encabezado = el("div", "sumaColGrid sumaColEncabezado");
      const filaPrestamos = el("div", "sumaColGrid sumaColAcarreos");
      const filaA = el("div", "sumaColGrid");
      const filaB = el("div", "sumaColGrid");
      const filaResultado = el("div", "sumaColGrid");
      encabezado.appendChild(gutter());
      filaPrestamos.appendChild(gutter());
      filaA.appendChild(gutter());
      filaB.appendChild(gutter("−"));
      filaResultado.appendChild(gutter());
      const prestamoBadges = [], slots = [];
      for (let i = ancho - 1; i >= 0; i--) {
        encabezado.appendChild(el("div", "sumaColEncabezado__col",
          `<span class="sumaColEncabezado__nombre">${SUMA_COL_NOMBRE[i]}</span><span class="sumaColEncabezado__potencia">${SUMA_COL_POTENCIA[i]}</span>`));
        const badge = el("div", "sumaColAcarreo sumaColAcarreo--oculto", "−1");
        prestamoBadges[i] = badge;
        filaPrestamos.appendChild(badge);
        filaA.appendChild(el("div", "sumaDigito", String(cifraEn(a, i))));
        filaB.appendChild(el("div", "sumaDigito" + (i >= String(b).length ? " sumaDigito--vacio" : ""),
          i < String(b).length ? String(cifraEn(b, i)) : ""));
        const slot = el("div", "sumaResultado__slot", "");
        slots[i] = slot;
        filaResultado.appendChild(slot);
      }
      tablero.appendChild(encabezado);
      tablero.appendChild(filaPrestamos);
      tablero.appendChild(filaA);
      tablero.appendChild(filaB);
      tablero.appendChild(el("div", "sumaColLinea"));
      tablero.appendChild(filaResultado);
      const ayudaBox = el("div", "sumaColLeccion sumaColLeccion--oculto", "");
      tablero.appendChild(ayudaBox);
      const btnAyuda = el("button", "btn suave sumaColAyuda", "💡 Ayuda");
      btnAyuda.type = "button";
      tablero.appendChild(btnAyuda);
      const keypad = el("div", "filaSprites sumaColKeypad");
      const botones = [];
      for (let d = 0; d <= 9; d++) {
        const btn = el("button", "spriteBtn sumaColDigitBtn", String(d));
        botones.push(btn);
        keypad.appendChild(btn);
      }
      tablero.appendChild(keypad);
      ctx.juego.appendChild(tablero);

      let activa = 0, resuelto = false, fallosCol = 0;
      const correctaEn = (i) => cifraEn(resta, i);
      const marcarActiva = () => slots.forEach((s, i) => s.classList.toggle("activo", i === activa && !resuelto));
      marcarActiva();
      const mostrarAyuda = () => {
        const i = activa;
        const top = cifraEn(a, i) - (i > 0 && prestamo[i - 1] ? 1 : 0);
        const nombre = SUMA_COL_LARGO[i];
        const txt = top < cifraEn(b, i)
          ? `En las ${nombre}: a ${top} no le alcanza para restarle ${cifraEn(b, i)}, así que te prestás 1 (queda ${top + 10}). ${top + 10} − ${cifraEn(b, i)} = ${correctaEn(i)}.`
          : `En las ${nombre}: ${top} − ${cifraEn(b, i)} = ${correctaEn(i)}.`;
        ayudaBox.textContent = "💡 " + txt;
        ayudaBox.classList.remove("sumaColLeccion--oculto");
        reproducirConsigna(txt);
      };
      btnAyuda.addEventListener("click", mostrarAyuda);
      botones.forEach((btn, d) => {
        btn.addEventListener("click", async () => {
          if (resuelto) return;
          if (d !== correctaEn(activa)) {
            btn.style.animation = "sacudir .4s ease";
            setTimeout(() => (btn.style.animation = ""), 450);
            ctx.casi(); fallosCol++;
            if (fallosCol >= 2) mostrarAyuda();
            return;
          }
          fallosCol = 0;
          ayudaBox.classList.add("sumaColLeccion--oculto");
          slots[activa].textContent = String(d);
          slots[activa].classList.add("anim-pop");
          if (prestamo[activa] && activa + 1 < ancho) prestamoBadges[activa + 1].classList.remove("sumaColAcarreo--oculto");
          Sfx.tick(activa + 1);
          activa++;
          if (activa >= ancho) {
            resuelto = true;
            ctx.bien();
            ronda++;
            await espera(1100);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else marcarActiva();
        });
      });
    };
    jugar();
  },
};

/* ── AGUDO, RECTO U OBTUSO (14-jul-2026, 4° grado NAP Bimestre 4 "Ideas
   web": "transportador interactivo para medir ángulos de rampas de
   skate" — simplificado de medición libre con transportador a
   clasificación sobre un ángulo dibujado con CSS puro (dos líneas desde un
   vértice común, una fija y otra rotada). Grados curados a propósito, no
   al azar — un ángulo de 88° sería ambiguo a simple vista contra uno
   recto real (90°), así que cada categoría usa valores CLARAMENTE
   distinguibles. ── */
const ANGULOS_BANCO = [
  { grados: 12, tipo: "agudo" },
  { grados: 20, tipo: "agudo" },
  { grados: 25, tipo: "agudo" },
  { grados: 33, tipo: "agudo" },
  { grados: 40, tipo: "agudo" },
  { grados: 48, tipo: "agudo" },
  { grados: 55, tipo: "agudo" },
  { grados: 62, tipo: "agudo" },
  { grados: 70, tipo: "agudo" },
  { grados: 78, tipo: "agudo" },
  { grados: 85, tipo: "agudo" },
  { grados: 90, tipo: "recto" },
  { grados: 98, tipo: "obtuso" },
  { grados: 105, tipo: "obtuso" },
  { grados: 112, tipo: "obtuso" },
  { grados: 118, tipo: "obtuso" },
  { grados: 125, tipo: "obtuso" },
  { grados: 132, tipo: "obtuso" },
  { grados: 140, tipo: "obtuso" },
  { grados: 148, tipo: "obtuso" },
  { grados: 155, tipo: "obtuso" },
  { grados: 162, tipo: "obtuso" },
  { grados: 168, tipo: "obtuso" },
  { grados: 175, tipo: "obtuso" }
];
GAMES.angulos = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es agudo, recto u obtuso?", "m");
      ctx.juego.innerHTML = "";
      let disp = ANGULOS_BANCO.filter((x) => !usados.includes(x.grados));
      if (!disp.length) { usados = []; disp = ANGULOS_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.grados);
      const arriba = el("div", "tablero");
      const dibujo = el("div", "anguloDibujo");
      dibujo.appendChild(el("div", "anguloDibujo__base"));
      const lado = el("div", "anguloDibujo__lado");
      lado.style.transform = `rotate(-${item.grados}deg)`;
      dibujo.appendChild(lado);
      arriba.appendChild(dibujo);
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle(["agudo", "recto", "obtuso"]).forEach((tipo) => {
        const b = el("button", "spriteBtn", `<span style="font-size:18px;font-family:'Baloo',sans-serif">${tipo}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (tipo === item.tipo) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── LEER EL TRANSPORTADOR (M14 modo C, 5° — docs/auditoria-dc-caba/grado-5.md:
   "Lectura de transportador como modo C de M14: ¿mide 40° o 140°?"). En 4° el
   ángulo se CLASIFICA (agudo/recto/obtuso, GAMES.angulos); acá se MIDE leyendo el
   transportador de verdad — la mecánica nodal que la auditoría marcaba como
   trivia. Ataca la misconception #1 del transportador: leer la ESCALA EQUIVOCADA
   (θ vs 180−θ, el clásico "40 o 140"). Se dibuja el transportador con las DOS
   escalas y el lado de abajo apoyado en el 0 de la derecha → se lee la de afuera.
   Capa 0 C3: si eligen 180−θ, se nombra el error ("esa es la otra escala"). Los
   ángulos son múltiplos de 10 (lectura exacta) y evitan 90 (ahí las dos escalas
   coinciden y no hay nada que confundir). ── */
const TRANSPORTADOR_BANCO = [20, 30, 40, 50, 60, 70, 80, 100, 110, 120, 130, 140, 150, 160];
GAMES.transportador = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 8;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const P = (cx, cy, r, a) => [cx + r * Math.cos(a * Math.PI / 180), cy - r * Math.sin(a * Math.PI / 180)];
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.consigna("¿Cuántos grados mide el ángulo?");
      ctx.juego.innerHTML = "";
      let disp = TRANSPORTADOR_BANCO.filter((x) => !usados.includes(x));
      if (!disp.length) { usados = []; disp = TRANSPORTADOR_BANCO; }
      const th = disp[rint(0, disp.length - 1)]; usados.push(th);
      ctx.item("transportador#" + th);

      const cx = 175, cy = 185, R = 150;
      let s = '<svg viewBox="0 0 350 214" class="transp-svg">';
      // semicircunferencia + base
      let arc = "";
      for (let a = 0; a <= 180; a += 3) { const [x, y] = P(cx, cy, R, a); arc += (a ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1) + " "; }
      s += '<path d="' + arc + '" class="transp-arco"/>';
      s += '<line x1="' + (cx - R) + '" y1="' + cy + '" x2="' + (cx + R) + '" y2="' + cy + '" class="transp-arco"/>';
      // marcas + números de las DOS escalas (externa = a, interna = 180−a) cada 10°
      for (let a = 0; a <= 180; a += 10) {
        const [x1, y1] = P(cx, cy, R, a), [x2, y2] = P(cx, cy, R - 13, a);
        s += '<line x1="' + x1.toFixed(1) + '" y1="' + y1.toFixed(1) + '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) + '" class="transp-tick"/>';
        const [ox, oy] = P(cx, cy, R + 12, a), [ix, iy] = P(cx, cy, R - 26, a);
        s += '<text x="' + ox.toFixed(1) + '" y="' + (oy + 3).toFixed(1) + '" class="transp-num out">' + a + '</text>';
        s += '<text x="' + ix.toFixed(1) + '" y="' + (iy + 3).toFixed(1) + '" class="transp-num in">' + (180 - a) + '</text>';
      }
      // sector sombreado del ángulo (0 → th)
      let sec = "M " + cx + " " + cy + " ";
      for (let a = 0; a <= th; a += 3) { const [x, y] = P(cx, cy, R * 0.55, a); sec += "L " + x.toFixed(1) + " " + y.toFixed(1) + " "; }
      const [sxE, syE] = P(cx, cy, R * 0.55, th); sec += "L " + sxE.toFixed(1) + " " + syE.toFixed(1) + " Z";
      s += '<path d="' + sec + '" class="transp-sector"/>';
      // lados: base (0°, apoyado en la derecha) y móvil (th)
      const [bx, by] = P(cx, cy, R, 0), [mx, my] = P(cx, cy, R, th);
      s += '<line x1="' + cx + '" y1="' + cy + '" x2="' + bx + '" y2="' + by + '" class="transp-lado base"/>';
      s += '<line x1="' + cx + '" y1="' + cy + '" x2="' + mx.toFixed(1) + '" y2="' + my.toFixed(1) + '" class="transp-lado movil"/>';
      // resaltar las DOS lecturas posibles en la marca del lado móvil
      const [hox, hoy] = P(cx, cy, R + 12, th), [hix, hiy] = P(cx, cy, R - 26, th);
      s += '<circle cx="' + hox.toFixed(1) + '" cy="' + (hoy - 3).toFixed(1) + '" r="13" class="transp-halo"/>';
      s += '<circle cx="' + hix.toFixed(1) + '" cy="' + (hiy - 3).toFixed(1) + '" r="13" class="transp-halo"/>';
      s += '<circle cx="' + cx + '" cy="' + cy + '" r="4.5" class="transp-vert"/>';
      s += '</svg>';
      const arriba = el("div", "tablero transp-wrap"); arriba.innerHTML = s;
      ctx.juego.appendChild(arriba);

      // opciones: la correcta + la escala equivocada (180−th) + un error de ±1 marca
      const wrong = 180 - th;
      const tercero = [th + 10, th - 10, th + 20, th - 20].find((v) => v > 0 && v < 180 && v !== th && v !== wrong);
      const ops = [{ v: th, ok: true }, { v: wrong, escala: true }, { v: tercero }];
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(ops).forEach((o) => {
        const b = el("button", "op", o.v + "°");
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) {
            resuelto = true; b.classList.add("bien", "anim-pop"); ctx.bien();
            ronda++; await espera(850);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else if (o.escala) {
            b.classList.add("casi");
            ctx.casi("Esa es la OTRA escala. El lado de abajo apoya en el 0 de la derecha, así que se lee " + th + "°, no " + wrong + "°.");
          } else {
            b.classList.add("casi");
            ctx.casi("Casi. Contá las marcas de a 10 desde el 0 de la derecha.");
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿QUÉ HORA ES? (leer el reloj — docs/auditoria-dc-caba/: medida del tiempo,
   2°-3°, mecánica nodal que faltaba entera). Reloj analógico SVG real con dos
   punteros (el corto/grueso = hora, el largo/fino = minutos). Ataca las 2
   misconceptions clásicas: (1) redondear mal la hora — leer el puntero corto como
   el número más cercano cuando está entre dos (3:40 → "las 4"); (2) leer el
   puntero largo CRUDO en vez de ×5 (marca el 8 → "8" en vez de 40). nivel 1 (2°):
   en punto y y media. nivel 2 (3°): cuartos y de a 5/10. Capa 0 C2/C3: cada error
   baja la estrella al primer intento y nombra el error. ── */
GAMES.reloj = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 8;
    const nivel = ctx.cfg.nivel || 1;
    ctx.rondas(rondas);
    let ronda = 0, previas = [];
    const P = (cx, cy, r, a) => [cx + r * Math.cos(a * Math.PI / 180), cy - r * Math.sin(a * Math.PI / 180)];
    const fmt = (h, m) => h + ":" + String(m).padStart(2, "0");
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.consigna("¿Qué hora marca el reloj?");
      ctx.juego.innerHTML = "";
      const mins = nivel >= 2 ? [0, 10, 15, 20, 30, 40, 45, 50] : [0, 30];
      let H, M, key, guard = 0;
      do { H = rint(1, 12); M = mins[rint(0, mins.length - 1)]; key = fmt(H, M); guard++; }
      while (previas.includes(key) && guard < 30);
      previas.push(key); if (previas.length > 6) previas.shift();
      ctx.item("reloj#" + key);

      const cx = 150, cy = 150, R = 132;
      let s = '<svg viewBox="0 0 300 300" class="reloj-svg" data-hora="' + key + '">';
      s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + R + '" class="reloj-cara"/>';
      for (let i = 0; i < 60; i++) {
        const a = 90 - i * 6, larga = i % 5 === 0;
        const [x1, y1] = P(cx, cy, R - 4, a), [x2, y2] = P(cx, cy, R - (larga ? 16 : 9), a);
        s += '<line x1="' + x1.toFixed(1) + '" y1="' + y1.toFixed(1) + '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) + '" class="reloj-tick' + (larga ? " larga" : "") + '"/>';
      }
      for (let n = 1; n <= 12; n++) {
        const a = 90 - n * 30, [x, y] = P(cx, cy, R - 32, a);
        s += '<text x="' + x.toFixed(1) + '" y="' + (y + 8).toFixed(1) + '" class="reloj-num">' + n + '</text>';
      }
      const ah = 90 - ((H % 12) + M / 60) * 30, am = 90 - M * 6;
      const [hx, hy] = P(cx, cy, R * 0.52, ah), [mx, my] = P(cx, cy, R * 0.78, am);
      s += '<line x1="' + cx + '" y1="' + cy + '" x2="' + hx.toFixed(1) + '" y2="' + hy.toFixed(1) + '" class="reloj-hora"/>';
      s += '<line x1="' + cx + '" y1="' + cy + '" x2="' + mx.toFixed(1) + '" y2="' + my.toFixed(1) + '" class="reloj-min"/>';
      s += '<circle cx="' + cx + '" cy="' + cy + '" r="7" class="reloj-centro"/>';
      s += '</svg>';
      const arriba = el("div", "tablero reloj-wrap"); arriba.innerHTML = s;
      ctx.juego.appendChild(arriba);

      const correcto = fmt(H, M);
      const wrongHora = fmt(H === 12 ? 1 : H + 1, M);   // redondeó mal la hora (puntero corto)
      const crudo = M / 5;                               // leyó el puntero largo crudo (÷5)
      const wrongMin = fmt(H, crudo);                    // "3:08" en vez de 3:40
      const ops = [{ v: correcto, ok: true }];
      const add = (o) => { if (ops.length < 3 && !ops.some((x) => x.v === o.v)) ops.push(o); };
      if (wrongMin !== correcto) add({ v: wrongMin, min: true });
      add({ v: wrongHora, hora: true });
      let tries = 0;
      while (ops.length < 3 && tries++ < 30) {
        const v = fmt(rint(1, 12), mins[rint(0, mins.length - 1)]);
        if (!ops.some((x) => x.v === v)) add({ v: v });
      }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(ops).forEach((o) => {
        const b = el("button", "op reloj-op", o.v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.ok) {
            resuelto = true; b.classList.add("bien", "anim-pop"); ctx.bien();
            ronda++; await espera(850); if (ronda >= rondas) ctx.win(); else jugar();
          } else if (o.min) {
            b.classList.add("casi");
            ctx.casi("El puntero largo cuenta los minutos de a 5. Si marca el " + crudo + ", son " + M + " minutos.");
          } else if (o.hora) {
            b.classList.add("casi");
            ctx.casi("El puntero corto es la hora, y todavía no llegó al " + (H === 12 ? 1 : H + 1) + ". Son las " + H + ".");
          } else {
            b.classList.add("casi"); ctx.casi("Mirá bien los dos punteros: el corto es la hora, el largo los minutos.");
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ÁRBOL DE PROBABILIDAD (azar y combinatoria, 6°-7° — docs/auditoria-dc-caba/:
   nociones de probabilidad + diagrama de árbol + principio multiplicativo; faltaba
   entero). Dibuja el DIAGRAMA DE ÁRBOL de un experimento de 2 etapas (elegí A y B)
   y el chico lee de ahí. Dos modos: (1) contar los resultados posibles (principio
   multiplicativo a×b) y (2) probabilidad simple de una hoja (1 en a×b, con el
   camino resaltado). Ataca LA misconception: SUMAR (a+b) en vez de multiplicar. Los
   escenarios evitan 2×2 (ahí a+b=a×b y el distractor coincidiría con la respuesta).
   Capa 0 C3: el error se explica sobre las HOJAS del árbol. ── */
const ARBOL_ESCENAS = [
  { a: { t: "remera", op: ["roja", "azul", "verde"] }, b: { t: "gorra", op: ["negra", "blanca"] } },
  { a: { t: "sabor", op: ["chocolate", "frutilla", "limón"] }, b: { t: "cucurucho", op: ["simple", "doble"] } },
  { a: { t: "jugo", op: ["naranja", "manzana"] }, b: { t: "galleta", op: ["dulce", "salada", "de agua"] } },
  { a: { t: "entrada", op: ["empanada", "tarta"] }, b: { t: "postre", op: ["flan", "helado", "fruta"] } },
  { a: { t: "media", op: ["blanca", "negra", "a rayas"] }, b: { t: "zapatilla", op: ["roja", "azul", "verde"] } },
  { a: { t: "color", op: ["rojo", "verde", "azul", "amarillo"] }, b: { t: "moneda", op: ["cara", "cruz"] } },
];
GAMES.arbol_probabilidad = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 8;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.juego.innerHTML = "";
      const esc = ARBOL_ESCENAS[rint(0, ARBOL_ESCENAS.length - 1)];
      const A = esc.a.op, B = esc.b.op, a = A.length, b = B.length, total = a * b;
      const modo = rint(0, 1) === 0 ? "contar" : "prob";
      const hi = rint(0, a - 1), hj = rint(0, b - 1);   // hoja resaltada (modo prob)

      const W = 380, rowH = 30, topPad = 20;
      const Hsvg = topPad * 2 + total * rowH;
      const xr = 22, x1 = 132, x2 = 230;
      const yRoot = Hsvg / 2;
      let s = '<svg viewBox="0 0 ' + W + ' ' + Hsvg + '" class="arbol-svg" data-answer="'
        + (modo === "contar" ? total : "1 en " + total) + '" data-modo="' + modo + '">';
      s += '<circle cx="' + xr + '" cy="' + yRoot.toFixed(1) + '" r="6" class="arbol-nodo"/>';
      for (let i = 0; i < a; i++) {
        const yi = topPad + (Hsvg - topPad * 2) * (i + 0.5) / a;
        const on1 = (modo === "prob" && i === hi);
        s += '<line x1="' + xr + '" y1="' + yRoot.toFixed(1) + '" x2="' + x1 + '" y2="' + yi.toFixed(1) + '" class="arbol-rama' + (on1 ? " on" : "") + '"/>';
        s += '<circle cx="' + x1 + '" cy="' + yi.toFixed(1) + '" r="5" class="arbol-nodo"/>';
        s += '<text x="' + (x1 - 8) + '" y="' + (yi - 6).toFixed(1) + '" class="arbol-lbl a">' + A[i] + '</text>';
        for (let j = 0; j < b; j++) {
          const leafIdx = i * b + j;
          const yl = topPad + (Hsvg - topPad * 2) * (leafIdx + 0.5) / total;
          const on = (modo === "prob" && i === hi && j === hj);
          s += '<line x1="' + x1 + '" y1="' + yi.toFixed(1) + '" x2="' + x2 + '" y2="' + yl.toFixed(1) + '" class="arbol-rama' + (on ? " on" : "") + '"/>';
          s += '<circle cx="' + x2 + '" cy="' + yl.toFixed(1) + '" r="4" class="arbol-hoja' + (on ? " on" : "") + '"/>';
          s += '<text x="' + (x2 + 8) + '" y="' + (yl + 4).toFixed(1) + '" class="arbol-lbl leaf' + (on ? " on" : "") + '">' + A[i] + " + " + B[j] + '</text>';
        }
      }
      s += '</svg>';
      const arriba = el("div", "tablero arbol-wrap"); arriba.innerHTML = s;
      ctx.juego.appendChild(arriba);

      if (modo === "contar")
        ctx.consigna("¿Cuántas combinaciones distintas de " + esc.a.t + " y " + esc.b.t + " se pueden armar?");
      else
        ctx.consigna("Con los ojos cerrados, ¿qué chance hay de que salga «" + A[hi] + " + " + B[hj] + "»?");

      const ops = [];
      const add = (v, tag) => { if (ops.length < 3 && !ops.some((o) => o.v === v)) ops.push({ v: v, tag: tag }); };
      if (modo === "contar") {
        add(String(total), "ok"); add(String(a + b), "suma"); add(String(total + b), "mis"); add(String(a), "una");
      } else {
        add("1 en " + total, "ok"); add("1 en " + (a + b), "suma"); add("1 en " + a, "una"); add("1 en " + b, "otra");
      }
      const fila = el("div", "ops");
      let resuelto = false;
      shuffle(ops).forEach((o) => {
        const bt = el("button", "op arbol-op", o.v);
        bt.addEventListener("click", async () => {
          if (resuelto) return;
          if (o.tag === "ok") {
            resuelto = true; bt.classList.add("bien", "anim-pop"); ctx.bien();
            ronda++; await espera(850); if (ronda >= rondas) ctx.win(); else jugar();
          } else if (o.tag === "suma") {
            bt.classList.add("casi");
            ctx.casi(modo === "contar"
              ? "No se suma: por CADA " + esc.a.t + " (" + a + ") hay " + b + " de " + esc.b.t + ", así que son " + a + "×" + b + "=" + total + " (contá las hojas)."
              : "Mirá las HOJAS del árbol: hay " + total + " finales posibles, no " + (a + b) + ".");
          } else {
            bt.classList.add("casi");
            ctx.casi("Contá las HOJAS del árbol (las puntas de la derecha): son " + total + ".");
          }
        });
        fila.appendChild(bt);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── PREFIJOS — FORMÁ LA PALABRA NUEVA (14-jul-2026, 4° grado NAP
   Bimestre 4 "Ideas web": "arrastrar prefijos y sufijos para formar
   palabras nuevas"). Mismo patrón tap-en-orden que armar_palabra/
   prefijos_sufijos, SOLO prefijos (des-, in-, pre-, re-) — los sufijos
   diminutivos del NAP (-ito, -oso) casi siempre piden apócope (gato+ito=
   gatITO, no "gatoito"), un cambio ortográfico real que una concatenación
   simple de tap no puede representar sin mentir; se deja afuera a
   propósito en vez de simular mal la regla. Sin audio por palabra — a
   esta edad ya hay autonomía lectora consolidada (2°-3° grado), a
   diferencia de Sala 5/1° grado que sí la necesitaban. ── */
// Compartido por los juegos de "tocá en el orden correcto" (15-jul-2026,
// Pablo: barrido completo de consignas repetitivas) — el chico arma una
// secuencia DISTINTA cada ronda, pero la instrucción en sí es la misma
// acción siempre: "tocá en orden". Genérico a propósito, sin referirse a
// ningún contenido puntual (sirve igual para órganos, pasos, prefijos...).
const ORDEN_CORTAS = ["¿Y ahora, en orden?", "Tocá en orden otra vez", "¿Y este orden?", "De nuevo, en orden"];
GAMES.prefijos_sufijos = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    const BANCO = [
      { partes: ["DES", "ATAR"], resultado: "DESATAR" },
      { partes: ["IN", "ÚTIL"], resultado: "INÚTIL" },
      { partes: ["PRE", "HISTÓRICO"], resultado: "PREHISTÓRICO" },
      { partes: ["RE", "HACER"], resultado: "REHACER" },
      { partes: ["DES", "ARMAR"], resultado: "DESARMAR" },
    ];
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      if (ronda === 0) ctx.consigna("Tocá el prefijo y la palabra en orden para formar la palabra nueva");
      else ctx.consigna(sacarDeBolsa(ctx, "orden", ORDEN_CORTAS));
      ctx.juego.innerHTML = "";
      let disp = BANCO.filter((x) => !usados.includes(x.resultado));
      if (!disp.length) { usados = []; disp = BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.resultado);
      const tablero = el("div", "tablero armarPalabraTablero");
      const filaSlots = el("div", "armarPalabraSlots");
      const slots = item.partes.map(() => el("div", "armarPalabraSlot", ""));
      slots.forEach((s) => filaSlots.appendChild(s));
      tablero.appendChild(filaSlots);
      const filaPartes = el("div", "filaSprites");
      filaPartes.style.marginTop = "18px";
      let siguiente = 0;
      let resuelto = false;
      shuffle(item.partes.map((s, i) => ({ s, i }))).forEach(({ s, i }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:19px;font-family:'Baloo',sans-serif">${s}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto || b.disabled) return;
          if (i === siguiente) {
            b.disabled = true;
            b.classList.add("anim-brinco");
            slots[i].textContent = s;
            slots[i].classList.add("anim-pop");
            Sfx.tick(siguiente + 1);
            siguiente++;
            if (siguiente >= item.partes.length) {
              resuelto = true;
              ctx.bien();
              ronda++;
              await espera(1100);
              if (ronda >= rondas) ctx.win();
              else jugar();
            }
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        filaPartes.appendChild(b);
      });
      tablero.appendChild(filaPartes);
      ctx.juego.appendChild(tablero);
    };
    jugar();
  },
};

/* ── ¿VERDADERO O FALSO? — VIDA COLONIAL (14-jul-2026, 5° grado NAP
   Bimestre 1 "Ideas web": "trivia histórica de la vida colonial en Buenos
   Aires"). Mismo patrón de clasificar 2 categorías que campo_ciudad. ── */
const COLONIAL_BANCO = [
  { afirmacion: "El Cabildo era el gobierno de la ciudad en la época colonial", val: true },
  { afirmacion: "El contrabando estaba permitido libremente por España", val: false },
  { afirmacion: "La pulpería era una tienda donde se vendía de todo", val: true },
  { afirmacion: "Los criollos eran hijos de españoles nacidos en América", val: true },
  { afirmacion: "El monopolio permitía comerciar libremente con cualquier país", val: false },
  // agregados 14-jul-2026 (banco ampliado de 5 a 10).
  { afirmacion: "El Virreinato del Río de la Plata se creó en 1776", val: true },
  { afirmacion: "Los mestizos eran hijos de españoles e indígenas", val: true },
  { afirmacion: "Existió esclavitud africana durante la época colonial en el Río de la Plata", val: true },
  { afirmacion: "El Cabildo Abierto era una reunión secreta a la que nadie podía asistir", val: false },
  { afirmacion: "Durante la colonia, los indígenas y los criollos tenían los mismos derechos que los españoles peninsulares", val: false },
  // ampliado 20-jul-2026 (de 10 a 22 — engrosar bancos nodales, docs/auditoria-dc-caba/)
  { afirmacion: "Las carretas tiradas por bueyes eran un medio de transporte en la época colonial", val: true },
  { afirmacion: "En la colonia ya andaban autos por las calles", val: false },
  { afirmacion: "Los aguateros vendían agua por las calles de la ciudad", val: true },
  { afirmacion: "Los esclavos africanos trabajaban sin cobrar y sin libertad", val: true },
  { afirmacion: "En la época colonial las mujeres podían votar", val: false },
  { afirmacion: "La Iglesia tenía mucho poder e influencia durante la colonia", val: true },
  { afirmacion: "Las calles de la ciudad colonial eran de tierra, sin asfalto", val: true },
  { afirmacion: "En la colonia las casas tenían luz eléctrica", val: false },
  { afirmacion: "El mate ya se tomaba en la época colonial", val: true },
  { afirmacion: "La plaza principal era el centro de la vida de la ciudad colonial", val: true },
  { afirmacion: "El comercio con España estaba muy controlado por la Corona (monopolio)", val: true },
  { afirmacion: "Los caminos entre las ciudades coloniales estaban todos asfaltados", val: false },
];
GAMES.trivia_colonial = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es verdadero o falso?", "f");
      ctx.juego.innerHTML = "";
      let disp = COLONIAL_BANCO.filter((x) => !usados.includes(x.afirmacion));
      if (!disp.length) { usados = []; disp = COLONIAL_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.afirmacion);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:22px;font-family:'Baloo',sans-serif">${item.afirmacion}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle([{ v: true, label: "✅ Verdadero" }, { v: false, label: "❌ Falso" }]).forEach(({ v, label }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:19px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === item.val) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── EL CAMINO DIGESTIVO (14-jul-2026, 5° grado NAP Bimestre 1 "Ideas
   web": "arrastrar alimentos por los órganos correctos" — adaptado a
   tap-en-orden, mismo patrón que armar_palabra/prefijos_sufijos: tocar los
   órganos en el orden real del sistema digestivo. ── */
GAMES.camino_digestivo = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 4;
    ctx.rondas(rondas);
    const ORGANOS = ["Boca", "Esófago", "Estómago", "Intestino delgado", "Intestino grueso"];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      if (ronda === 0) ctx.consigna("Tocá los órganos en el orden correcto del camino digestivo");
      else ctx.consigna(sacarDeBolsa(ctx, "orden", ORDEN_CORTAS));
      ctx.juego.innerHTML = "";
      const tablero = el("div", "tablero armarPalabraTablero");
      const filaSlots = el("div", "armarPalabraSlots");
      const slots = ORGANOS.map(() => el("div", "armarPalabraSlot", ""));
      slots.forEach((s) => filaSlots.appendChild(s));
      tablero.appendChild(filaSlots);
      const filaOrganos = el("div", "filaSprites");
      filaOrganos.style.marginTop = "18px";
      let siguiente = 0;
      let resuelto = false;
      shuffle(ORGANOS.map((s, i) => ({ s, i }))).forEach(({ s, i }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:15px;font-family:'Baloo',sans-serif">${s}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto || b.disabled) return;
          if (i === siguiente) {
            b.disabled = true;
            b.classList.add("anim-brinco");
            slots[i].textContent = String(i + 1);
            slots[i].classList.add("anim-pop");
            Sfx.tick(siguiente + 1);
            siguiente++;
            if (siguiente >= ORGANOS.length) {
              resuelto = true;
              ctx.bien();
              ronda++;
              await espera(1100);
              if (ronda >= rondas) ctx.win();
              else jugar();
            }
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        filaOrganos.appendChild(b);
      });
      tablero.appendChild(filaOrganos);
      ctx.juego.appendChild(tablero);
    };
    jugar();
  },
};

/* ── FRACCIONES EQUIVALENTES — NIVEL 2 (14-jul-2026, 5° grado NAP
   Bimestre 2 "Ideas web": "calculadora de equivalencias con barras
   deslizantes — 2/3 = 4/6 = 6/9"). Mismo motor visual (barras CPA) que
   fracciones_equivalentes de 4° grado, banco más difícil (tercios/novenos/
   décimos en vez de medios/cuartos/octavos) — juego propio, no una
   extensión del banco del año anterior, para que cada año conserve su
   propio progreso de estrellas. ── */
const FRACCIONES_AVANZADO_BANCO = [
  { num: 1, den: 3, eq: { num: 3, den: 9 }, d1: { num: 2, den: 9 }, d2: { num: 4, den: 9 } },
  { num: 2, den: 3, eq: { num: 6, den: 9 }, d1: { num: 5, den: 9 }, d2: { num: 7, den: 9 } },
  { num: 1, den: 4, eq: { num: 3, den: 12 }, d1: { num: 2, den: 12 }, d2: { num: 4, den: 12 } },
  { num: 3, den: 4, eq: { num: 9, den: 12 }, d1: { num: 8, den: 12 }, d2: { num: 10, den: 12 } },
  { num: 1, den: 2, eq: { num: 3, den: 6 }, d1: { num: 2, den: 6 }, d2: { num: 4, den: 6 } },
  { num: 1, den: 2, eq: { num: 4, den: 8 }, d1: { num: 3, den: 8 }, d2: { num: 5, den: 8 } },
  { num: 2, den: 3, eq: { num: 8, den: 12 }, d1: { num: 7, den: 12 }, d2: { num: 9, den: 12 } },
  { num: 1, den: 3, eq: { num: 4, den: 12 }, d1: { num: 3, den: 12 }, d2: { num: 5, den: 12 } },
  { num: 2, den: 4, eq: { num: 6, den: 12 }, d1: { num: 5, den: 12 }, d2: { num: 7, den: 12 } },
  { num: 3, den: 5, eq: { num: 6, den: 10 }, d1: { num: 5, den: 10 }, d2: { num: 7, den: 10 } },
  { num: 2, den: 5, eq: { num: 4, den: 10 }, d1: { num: 3, den: 10 }, d2: { num: 5, den: 10 } },
  { num: 4, den: 5, eq: { num: 8, den: 10 }, d1: { num: 7, den: 10 }, d2: { num: 9, den: 10 } },
  { num: 1, den: 5, eq: { num: 2, den: 10 }, d1: { num: 1, den: 10 }, d2: { num: 3, den: 10 } },
  { num: 1, den: 6, eq: { num: 2, den: 12 }, d1: { num: 1, den: 12 }, d2: { num: 3, den: 12 } },
  { num: 5, den: 6, eq: { num: 10, den: 12 }, d1: { num: 9, den: 12 }, d2: { num: 11, den: 12 } },
  { num: 3, den: 4, eq: { num: 6, den: 8 }, d1: { num: 5, den: 8 }, d2: { num: 7, den: 8 } },
  { num: 1, den: 4, eq: { num: 2, den: 8 }, d1: { num: 1, den: 8 }, d2: { num: 3, den: 8 } },
  { num: 2, den: 3, eq: { num: 4, den: 6 }, d1: { num: 3, den: 6 }, d2: { num: 5, den: 6 } },
  { num: 1, den: 2, eq: { num: 5, den: 10 }, d1: { num: 4, den: 10 }, d2: { num: 6, den: 10 } },
  { num: 1, den: 2, eq: { num: 6, den: 12 }, d1: { num: 5, den: 12 }, d2: { num: 7, den: 12 } },
  { num: 1, den: 3, eq: { num: 2, den: 6 }, d1: { num: 1, den: 6 }, d2: { num: 3, den: 6 } },
  { num: 3, den: 6, eq: { num: 6, den: 12 }, d1: { num: 5, den: 12 }, d2: { num: 7, den: 12 } },
  { num: 2, den: 6, eq: { num: 4, den: 12 }, d1: { num: 3, den: 12 }, d2: { num: 5, den: 12 } },
  { num: 4, den: 6, eq: { num: 8, den: 12 }, d1: { num: 7, den: 12 }, d2: { num: 9, den: 12 } }
];
GAMES.fracciones_avanzado = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    const barra = (num, den) => {
      const cont = el("div", "fraccionBarra");
      for (let i = 0; i < den; i++) cont.appendChild(el("div", "fraccionBarra__seg" + (i < num ? " lleno" : "")));
      return cont;
    };
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Cuál de estas barras muestra la misma fracción?", "f");
      ctx.juego.innerHTML = "";
      let disp = FRACCIONES_AVANZADO_BANCO.filter((x) => !usados.includes(x.num + "/" + x.den));
      if (!disp.length) { usados = []; disp = FRACCIONES_AVANZADO_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.num + "/" + item.den);
      const arriba = el("div", "tablero");
      arriba.appendChild(barra(item.num, item.den));
      ctx.juego.appendChild(arriba);
      const opciones = shuffle([item.eq, item.d1, item.d2]);
      const fila = el("div", "filaSprites fraccionesOpciones");
      let resuelto = false;
      opciones.forEach((op) => {
        const b = el("button", "spriteBtn fraccionBtn");
        b.appendChild(barra(op.num, op.den));
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op.num === item.eq.num && op.den === item.eq.den) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── NÚCLEO DEL SUJETO O DEL PREDICADO — CONTRARRELOJ (14-jul-2026, 5°
   grado NAP Bimestre 2 "Ideas web": "velocidad de análisis sintáctico —
   núcleo del sujeto o del predicado"). SEGUNDA mecánica de timer del
   motor (la primera fue tablas_contrarreloj, 2° grado) — mismo guard de
   seguridad: el intervalo se auto-apaga si su nodo deja de estar
   conectado al documento (evita corromper Shell.fallos de otro juego si
   el jugador navega a mitad de ronda). ── */
const SINTACTICO_BANCO = [
  { oracion: "El <b>perro</b> ladra fuerte.", tipo: "sujeto" },
  { oracion: "La niña <b>corre</b> en el parque.", tipo: "predicado" },
  { oracion: "Los <b>chicos</b> juegan al fútbol.", tipo: "sujeto" },
  { oracion: "Mi mamá <b>cocina</b> todos los días.", tipo: "predicado" },
  { oracion: "El <b>sol</b> brilla en el cielo.", tipo: "sujeto" },
  { oracion: "El gato <b>duerme</b> en el sillón.", tipo: "predicado" },
  // agregados 14-jul-2026 (banco ampliado de 6 a 10).
  { oracion: "La <b>maestra</b> explica la lección.", tipo: "sujeto" },
  { oracion: "Los pájaros <b>cantan</b> en la mañana.", tipo: "predicado" },
  { oracion: "El <b>auto</b> rojo pasa rápido.", tipo: "sujeto" },
  { oracion: "Nosotros <b>estudiamos</b> para el examen.", tipo: "predicado" },
  // ampliado 20-jul-2026 (de 10 a 22 — engrosar bancos nodales, docs/auditoria-dc-caba/)
  { oracion: "El <b>maestro</b> corrige la tarea.", tipo: "sujeto" },
  { oracion: "Los niños <b>juegan</b> en el recreo.", tipo: "predicado" },
  { oracion: "La <b>abuela</b> teje una bufanda.", tipo: "sujeto" },
  { oracion: "El equipo <b>ganó</b> el partido.", tipo: "predicado" },
  { oracion: "Mi <b>hermana</b> toca el piano.", tipo: "sujeto" },
  { oracion: "El río <b>crece</b> con la lluvia.", tipo: "predicado" },
  { oracion: "Las <b>estrellas</b> brillan de noche.", tipo: "sujeto" },
  { oracion: "El bombero <b>apagó</b> el incendio.", tipo: "predicado" },
  { oracion: "El <b>viento</b> movía las hojas.", tipo: "sujeto" },
  { oracion: "Los turistas <b>sacaron</b> muchas fotos.", tipo: "predicado" },
  { oracion: "La <b>maestra</b> explicó el tema.", tipo: "sujeto" },
  { oracion: "El tren <b>llegó</b> tarde a la estación.", tipo: "predicado" },
];
GAMES.analisis_sintactico = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    const TIEMPO_MS = 6000;
    let usados = [];
    let ronda = 0;
    let intervalId = null;
    const jugar = () => {
      if (intervalId) { clearInterval(intervalId); intervalId = null; }
      ctx.ronda(ronda);
      ctx.consigna(ronda === 0 ? "Elegí rápido: ¿es núcleo del sujeto o del predicado?" : sacarDeBolsa(ctx, "rapido", RAPIDO_CORTAS));
      ctx.juego.innerHTML = "";
      let disp = SINTACTICO_BANCO.filter((x) => !usados.includes(x.oracion));
      if (!disp.length) { usados = []; disp = SINTACTICO_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.oracion);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:22px;font-family:'Baloo',sans-serif">${item.oracion}</span>`));
      ctx.juego.appendChild(arriba);
      const barraWrap = el("div", "barraTiempo");
      const barra = el("div", "barraTiempo__fill");
      barraWrap.appendChild(barra);
      ctx.juego.appendChild(barraWrap);
      let resuelto = false;
      const inicio = Date.now();
      intervalId = setInterval(() => {
        if (!barraWrap.isConnected) {
          clearInterval(intervalId);
          intervalId = null;
          return;
        }
        const restante = Math.max(0, 1 - (Date.now() - inicio) / TIEMPO_MS);
        barra.style.width = (restante * 100) + "%";
        if (restante <= 0 && !resuelto) {
          clearInterval(intervalId);
          intervalId = null;
          ctx.casi();
          jugar();
        }
      }, 100);
      const fila = el("div", "filaSprites");
      shuffle(["sujeto", "predicado"]).forEach((tipo) => {
        const b = el("button", "spriteBtn", `<span style="font-size:18px;font-family:'Baloo',sans-serif">Núcleo del ${tipo}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (tipo === item.tipo) {
            resuelto = true;
            if (intervalId) { clearInterval(intervalId); intervalId = null; }
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── SUJETO Y PREDICADO — DIVIDÍ LA ORACIÓN (docs/auditoria-dc-caba/: análisis
   sintáctico, hueco de Lengua nodal — grado-4.md lo marca ausente en 4°). A
   diferencia de analisis_sintactico (fluidez: el núcleo viene YA en negrita y se
   clasifica), acá el chico HACE el análisis: divide la oración tocando la primera
   palabra del PREDICADO (el verbo). Interacción por TAP, no drag de verdad — más
   robusto en mobile (mismo criterio que agrupar/campo_ciudad). Al acertar se pintan
   sujeto (azul) y predicado (verde). Capa 0 C3: el error dice si te quedaste en el
   sujeto o te pasaste ("buscá el verbo"). ── */
const SUJPRED_BANCO = [
  { suj: ["El", "perro"], pred: ["ladra", "fuerte."] },
  { suj: ["La", "niña", "pequeña"], pred: ["corre", "en", "el", "parque."] },
  { suj: ["Los", "chicos"], pred: ["juegan", "al", "fútbol."] },
  { suj: ["Mi", "mamá"], pred: ["cocina", "todos", "los", "días."] },
  { suj: ["El", "sol"], pred: ["brilla", "en", "el", "cielo."] },
  { suj: ["El", "gato", "negro"], pred: ["duerme", "en", "el", "sillón."] },
  { suj: ["La", "maestra"], pred: ["explica", "la", "lección."] },
  { suj: ["Los", "pájaros"], pred: ["cantan", "en", "la", "mañana."] },
  { suj: ["El", "auto", "rojo"], pred: ["pasa", "muy", "rápido."] },
  { suj: ["Nosotros"], pred: ["estudiamos", "para", "el", "examen."] },
  { suj: ["Mi", "hermano", "mayor"], pred: ["juega", "a", "la", "pelota."] },
  { suj: ["Las", "flores", "del", "jardín"], pred: ["crecen", "en", "primavera."] },
  { suj: ["El", "viento", "fuerte"], pred: ["mueve", "las", "hojas."] },
  { suj: ["Ana", "y", "Pedro"], pred: ["comen", "una", "pizza."] },
];
GAMES.sujeto_predicado = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 8;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.consigna("Tocá la primera palabra del PREDICADO (lo que hace el sujeto).");
      ctx.juego.innerHTML = "";
      let libres = SUJPRED_BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!libres.length) { usados = []; libres = SUJPRED_BANCO.map((_, i) => i); }
      const idx = libres[rint(0, libres.length - 1)];
      usados.push(idx);
      const item = SUJPRED_BANCO[idx];
      const palabras = item.suj.concat(item.pred);
      const corte = item.suj.length;
      ctx.item("sujpred#" + idx);

      const arriba = el("div", "tablero");
      const fila = el("div", "filaPalabras");
      fila.setAttribute("data-corte", corte);
      let resuelto = false;
      palabras.forEach((w, i) => {
        const chip = el("button", "palabraChip", w);
        chip.addEventListener("click", async () => {
          if (resuelto) return;
          if (i === corte) {
            resuelto = true;
            palabras.forEach((_, k) => fila.children[k].classList.add(k < corte ? "suj" : "pred"));
            ctx.bien();
            ronda++; await espera(1050);
            if (ronda >= rondas) ctx.win(); else jugar();
          } else if (i < corte) {
            chip.classList.add("casi-chip"); setTimeout(() => chip.classList.remove("casi-chip"), 450);
            ctx.casi("«" + w + "» todavía es parte del SUJETO (de quién hablamos). El predicado empieza en el verbo.");
          } else {
            chip.classList.add("casi-chip"); setTimeout(() => chip.classList.remove("casi-chip"), 450);
            ctx.casi("Eso ya está dentro del predicado, pero empieza ANTES: buscá el verbo (la acción).");
          }
        });
        fila.appendChild(chip);
      });
      arriba.appendChild(fila);
      ctx.juego.appendChild(arriba);
      const ley = el("div", "sujpred-leyenda",
        '<span class="suj-lbl">■ Sujeto: de quién hablamos</span><span class="pred-lbl">■ Predicado: lo que hace</span>');
      ctx.juego.appendChild(el("div", "tablero")).appendChild(ley);
    };
    jugar();
  },
};

/* ── PAGO EXACTO (14-jul-2026, 5° grado NAP Bimestre 3 "Ideas web":
   "simular pago con billetes/monedas argentinas reales — centavos
   incluidos"). Mismo patrón probado de cajero_automatico (3° grado, tocar
   2 que sumen el objetivo), con denominaciones que incluyen centavos —
   los valores se guardan en CENTAVOS (enteros) para no arrastrar errores
   de punto flotante, y se formatean a pesos recién al mostrar. ── */
function _formatoPesos(centavos) {
  return "$" + (centavos / 100).toFixed(2);
}
GAMES.pago_exacto = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    const MONEDAS = [25, 50, 100, 200, 500, 1000];   // $0.25, $0.50, $1, $2, $5, $10
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "Tocá las monedas que sumen el pago exacto", "n");
      ctx.juego.innerHTML = "";
      const idxA = rint(0, MONEDAS.length - 1);
      let idxB = rint(0, MONEDAS.length - 1);
      while (idxB === idxA) idxB = rint(0, MONEDAS.length - 1);
      const a = MONEDAS[idxA], b = MONEDAS[idxB];
      const objetivo = a + b;
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:30px;font-family:'Baloo',sans-serif">Pagá ${_formatoPesos(objetivo)}</span>`));
      ctx.juego.appendChild(arriba);
      let nums = [a, b];
      let guardas = 0;
      while (nums.length < 5 && guardas < 100) {
        guardas++;
        const v = MONEDAS[rint(0, MONEDAS.length - 1)];
        if (!nums.includes(v) && !nums.some((n) => n + v === objetivo)) nums.push(v);
      }
      nums = shuffle(nums);
      const fila = el("div", "filaSprites");
      let elegido = null;
      let resuelto = false;
      nums.forEach((v, idx) => {
        const btn = el("button", "spriteBtn", `<span style="font-size:18px;font-family:'Baloo',sans-serif">${_formatoPesos(v)}</span>`);
        btn.addEventListener("click", async () => {
          if (resuelto || btn.disabled) return;
          if (elegido === null) {
            elegido = { idx, v, btn };
            btn.classList.add("elegido");
            return;
          }
          if (elegido.idx === idx) return;
          if (elegido.v + v === objetivo) {
            resuelto = true;
            btn.disabled = true;
            elegido.btn.disabled = true;
            btn.classList.add("anim-pop");
            elegido.btn.classList.add("anim-pop");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            const prevBtn = elegido.btn;
            prevBtn.classList.remove("elegido");
            btn.style.animation = "sacudir .4s ease";
            prevBtn.style.animation = "sacudir .4s ease";
            setTimeout(() => { btn.style.animation = ""; prevBtn.style.animation = ""; }, 450);
            ctx.casi();
            elegido = null;
          }
        });
        fila.appendChild(btn);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿QUÉ SE PRODUCE EN ESTA REGIÓN? (14-jul-2026, 5° grado NAP Bimestre
   3 "Ideas web": "mapa interactivo de actividad económica por región" —
   simplificado a trivia, mismo criterio que provincias_region de 4°
   grado: un mapa económico interactivo real es un asset, no un juego). ── */
const ECONOMIA_BANCO = [
  { p: "Vino", region: "Cuyo" }, { p: "Ganado", region: "Pampeana" },
  { p: "Azúcar", region: "NOA" }, { p: "Yerba mate", region: "NEA" },
  { p: "Petróleo", region: "Patagonia" }, { p: "Trigo", region: "Pampeana" },
  // agregados 14-jul-2026 (banco ampliado de 6 a 10).
  { p: "Aceitunas", region: "Cuyo" }, { p: "Algodón", region: "NEA" },
  { p: "Lana", region: "Patagonia" }, { p: "Tabaco", region: "NOA" },
];
GAMES.actividad_economica = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    const REGIONES = ["Cuyo", "Pampeana", "NOA", "NEA", "Patagonia"];
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿En qué región se produce esto?", "n");
      ctx.juego.innerHTML = "";
      let disp = ECONOMIA_BANCO.filter((x) => !usados.includes(x.p));
      if (!disp.length) { usados = []; disp = ECONOMIA_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.p);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:28px;font-family:'Baloo',sans-serif">${item.p}</span>`));
      ctx.juego.appendChild(arriba);
      // 3 opciones: la correcta + 2 distractoras (nunca las 5 regiones juntas —
      // demasiadas opciones para el tamaño mínimo de blanco táctil)
      let opciones = [item.region];
      while (opciones.length < 3) {
        const r = REGIONES[rint(0, REGIONES.length - 1)];
        if (!opciones.includes(r)) opciones.push(r);
      }
      opciones = shuffle(opciones);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      opciones.forEach((r) => {
        const b = el("button", "spriteBtn", `<span style="font-size:18px;font-family:'Baloo',sans-serif">${r}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (r === item.region) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── PLANTA POTABILIZADORA (14-jul-2026, 5° grado NAP Bimestre 4 "Ideas
   web": "planta potabilizadora — ordenar los pasos de purificación").
   Mismo patrón tap-en-orden que camino_digestivo/armar_palabra. ── */
GAMES.planta_potabilizadora = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 4;
    ctx.rondas(rondas);
    const PASOS = ["Captación", "Filtración", "Desinfección", "Distribución"];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      if (ronda === 0) ctx.consigna("Tocá los pasos de la potabilización en el orden correcto");
      else ctx.consigna(sacarDeBolsa(ctx, "orden", ORDEN_CORTAS));
      ctx.juego.innerHTML = "";
      const tablero = el("div", "tablero armarPalabraTablero");
      const filaSlots = el("div", "armarPalabraSlots");
      const slots = PASOS.map(() => el("div", "armarPalabraSlot", ""));
      slots.forEach((s) => filaSlots.appendChild(s));
      tablero.appendChild(filaSlots);
      const filaPasos = el("div", "filaSprites");
      filaPasos.style.marginTop = "18px";
      let siguiente = 0;
      let resuelto = false;
      shuffle(PASOS.map((s, i) => ({ s, i }))).forEach(({ s, i }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:16px;font-family:'Baloo',sans-serif">${s}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto || b.disabled) return;
          if (i === siguiente) {
            b.disabled = true;
            b.classList.add("anim-brinco");
            slots[i].textContent = String(i + 1);
            slots[i].classList.add("anim-pop");
            Sfx.tick(siguiente + 1);
            siguiente++;
            if (siguiente >= PASOS.length) {
              resuelto = true;
              ctx.bien();
              ronda++;
              await espera(1100);
              if (ronda >= rondas) ctx.win();
              else jugar();
            }
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        filaPasos.appendChild(b);
      });
      tablero.appendChild(filaPasos);
      ctx.juego.appendChild(tablero);
    };
    jugar();
  },
};

/* ── DERECHOS Y CONSTITUCIÓN (14-jul-2026, 5° grado NAP Bimestre 4 "Ideas
   web": "trivia de Derechos del Niño y bases constitucionales"). Mismo
   patrón Verdadero/Falso que trivia_colonial. ── */
const DERECHOS_BANCO = [
  { afirmacion: "Todos los niños tienen derecho a la educación", val: true },
  { afirmacion: "La Constitución Argentina no protege ningún derecho", val: false },
  { afirmacion: "Argentina es una república federal y democrática", val: true },
  { afirmacion: "Los niños no tienen derecho a jugar ni a descansar", val: false },
  { afirmacion: "Todos los niños tienen derecho a la salud", val: true },
  // agregados 14-jul-2026 (banco ampliado de 5 a 10).
  { afirmacion: "La Convención sobre los Derechos del Niño protege a los chicos en todo el mundo", val: true },
  { afirmacion: "Los niños no tienen derecho a expresar su opinión", val: false },
  { afirmacion: "La Constitución Argentina garantiza la libertad de expresión", val: true },
  { afirmacion: "En Argentina, los derechos solo valen para los adultos, no para los niños", val: false },
  { afirmacion: "Los niños tienen derecho a la protección contra el maltrato", val: true },
];
GAMES.derechos_constitucion = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es verdadero o falso?", "f");
      ctx.juego.innerHTML = "";
      let disp = DERECHOS_BANCO.filter((x) => !usados.includes(x.afirmacion));
      if (!disp.length) { usados = []; disp = DERECHOS_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.afirmacion);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:22px;font-family:'Baloo',sans-serif">${item.afirmacion}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle([{ v: true, label: "✅ Verdadero" }, { v: false, label: "❌ Falso" }]).forEach(({ v, label }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:19px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === item.val) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿PARA QUÉ SIRVE ESTA PARTE? — LA CÉLULA (14-jul-2026, 6° grado NAP
   Bimestre 1 "Ideas web": "simulador de microscopio — enfocar y rotular
   partes de la célula" — simplificado de simulación de enfoque a
   matching parte→función, mismo patrón que planta_fruto/animal_comida). ── */
const CELULA_BANCO = [
  { parte: "Núcleo", correcta: "Controla las actividades de la célula", d1: "Fabrica proteínas", d2: "Le da forma a la célula" },
  { parte: "Membrana", correcta: "Protege y controla lo que entra y sale", d1: "Controla las actividades", d2: "Genera energía" },
  { parte: "Mitocondria", correcta: "Genera la energía de la célula", d1: "Protege a la célula", d2: "Guarda la información genética" },
  { parte: "Citoplasma", correcta: "Ocupa el espacio entre el núcleo y la membrana", d1: "Genera energía", d2: "Controla las actividades" },
  // agregados 14-jul-2026 (banco ampliado de 4 a 10 — Pablo: "agrandar el
  // banco de preguntas... preparar el terreno"). Distractores = función
  // REAL de otra parte del banco (confusión genuina), nunca al azar.
  { parte: "Ribosomas", correcta: "Fabrican las proteínas", d1: "Generan la energía de la célula", d2: "Controlan las actividades de la célula" },
  { parte: "Vacuola", correcta: "Almacena agua, nutrientes y desechos", d1: "Fabrica las proteínas", d2: "Protege y controla lo que entra y sale" },
  { parte: "Cloroplasto", correcta: "Realiza la fotosíntesis y produce el alimento", d1: "Genera la energía de la célula", d2: "Almacena agua y nutrientes" },
  { parte: "Pared celular", correcta: "Le da rigidez y protección extra a la célula vegetal", d1: "Protege y controla lo que entra y sale", d2: "Genera la energía de la célula" },
  { parte: "Aparato de Golgi", correcta: "Empaqueta y distribuye las proteínas", d1: "Fabrica las proteínas", d2: "Guarda la información genética" },
  { parte: "Retículo endoplasmático", correcta: "Transporta sustancias dentro de la célula", d1: "Ocupa el espacio entre el núcleo y la membrana", d2: "Genera la energía de la célula" },
];
GAMES.celula_partes = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 4;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Para qué sirve esta parte de la célula?", "f");
      ctx.juego.innerHTML = "";
      let disp = CELULA_BANCO.filter((x) => !usados.includes(x.parte));
      if (!disp.length) { usados = []; disp = CELULA_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.parte);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:30px;font-family:'Baloo',sans-serif">${item.parte}</span>`));
      ctx.juego.appendChild(arriba);
      const opciones = shuffle([item.correcta, item.d1, item.d2]);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      opciones.forEach((op) => {
        const b = el("button", "spriteBtn", `<span style="font-size:16px;font-family:'Baloo',sans-serif">${op}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op === item.correcta) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿HECHO U OPINIÓN? (14-jul-2026, 6° grado NAP Bimestre 1 "Ideas web":
   "cuestionario de hechos vs. opiniones en noticias"). Mismo patrón de
   clasificar 2 categorías que campo_ciudad. ── */
const HECHOS_OPINIONES_BANCO = [
  { texto: "Llovió 50 milímetros ayer en Buenos Aires", tipo: "hecho" },
  { texto: "El nuevo parque es hermoso", tipo: "opinion" },
  { texto: "El equipo ganó el partido 3 a 1", tipo: "hecho" },
  { texto: "Esa película fue aburrida", tipo: "opinion" },
  { texto: "La reunión empieza a las 10", tipo: "hecho" },
  { texto: "Creo que va a llover mañana", tipo: "opinion" },
  // agregados 14-jul-2026 (banco ampliado de 6 a 10).
  { texto: "El río Paraná es el más largo de Argentina", tipo: "hecho" },
  { texto: "La música de ese grupo es la mejor", tipo: "opinion" },
  { texto: "La reunión terminó a las 5 de la tarde", tipo: "hecho" },
  { texto: "Ese cuadro es feísimo", tipo: "opinion" },
];
GAMES.hechos_opiniones = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es un hecho o una opinión?", "f");
      ctx.juego.innerHTML = "";
      let disp = HECHOS_OPINIONES_BANCO.filter((x) => !usados.includes(x.texto));
      if (!disp.length) { usados = []; disp = HECHOS_OPINIONES_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.texto);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:22px;font-family:'Baloo',sans-serif">${item.texto}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle([{ v: "hecho", label: "Hecho" }, { v: "opinion", label: "Opinión" }]).forEach(({ v, label }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:19px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === item.tipo) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── SISTEMA NERVIOSO (14-jul-2026, 6° grado NAP Bimestre 2 "Ideas web":
   "simulador de reflejos — tiempo de reacción, explica el impulso
   nervioso" — simplificado a trivia de contenido. Medir milisegundos
   reales de reacción es una mecánica genuinamente nueva -stimulus→tap,
   sin "ronda" con respuesta correcta/incorrecta- que no encaja en el
   Shell de bien()/casi()/rondas existente; se prefirió construir sobre el
   patrón probado antes que forzar una mecánica a medio hacer). ── */
const NERVIOSO_BANCO = [
  { afirmacion: "El sistema nervioso central está formado por el cerebro y la médula espinal", val: true },
  { afirmacion: "Los reflejos son respuestas lentas que pensamos antes de actuar", val: false },
  { afirmacion: "Las neuronas transmiten información por impulsos eléctricos", val: true },
  { afirmacion: "El sistema nervioso periférico no cumple ninguna función", val: false },
  { afirmacion: "Un reflejo es una respuesta automática y rápida ante un estímulo", val: true },
  // agregados 14-jul-2026 (banco ampliado de 5 a 10).
  { afirmacion: "El cerebro controla el pensamiento, el movimiento y las emociones", val: true },
  { afirmacion: "Las neuronas se conectan entre sí a través de las sinapsis", val: true },
  { afirmacion: "El cerebelo se encarga del equilibrio y la coordinación de los movimientos", val: true },
  { afirmacion: "Todos los reflejos pasan primero por el cerebro antes de actuar", val: false },
  { afirmacion: "La médula espinal no cumple ninguna función en los reflejos", val: false },
];
GAMES.sistema_nervioso = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es verdadero o falso?", "f");
      ctx.juego.innerHTML = "";
      let disp = NERVIOSO_BANCO.filter((x) => !usados.includes(x.afirmacion));
      if (!disp.length) { usados = []; disp = NERVIOSO_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.afirmacion);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:20px;font-family:'Baloo',sans-serif">${item.afirmacion}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle([{ v: true, label: "✅ Verdadero" }, { v: false, label: "❌ Falso" }]).forEach(({ v, label }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:19px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === item.val) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── EL VIAJE DEL INMIGRANTE (14-jul-2026, 6° grado NAP Bimestre 2 "Ideas
   web": "viaje del inmigrante — mapa Génova → Hotel de Inmigrantes").
   Mismo patrón tap-en-orden que camino_digestivo/planta_potabilizadora. ── */
GAMES.viaje_inmigrante = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 4;
    ctx.rondas(rondas);
    const ETAPAS = ["Puerto de Génova", "Barco a Buenos Aires", "Hotel de Inmigrantes", "Nueva vida en Argentina"];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      if (ronda === 0) ctx.consigna("Tocá las etapas del viaje del inmigrante en el orden correcto");
      else ctx.consigna(sacarDeBolsa(ctx, "orden", ORDEN_CORTAS));
      ctx.juego.innerHTML = "";
      const tablero = el("div", "tablero armarPalabraTablero");
      const filaSlots = el("div", "armarPalabraSlots");
      const slots = ETAPAS.map(() => el("div", "armarPalabraSlot", ""));
      slots.forEach((s) => filaSlots.appendChild(s));
      tablero.appendChild(filaSlots);
      const filaEtapas = el("div", "filaSprites");
      filaEtapas.style.marginTop = "18px";
      let siguiente = 0;
      let resuelto = false;
      shuffle(ETAPAS.map((s, i) => ({ s, i }))).forEach(({ s, i }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:14px;font-family:'Baloo',sans-serif">${s}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto || b.disabled) return;
          if (i === siguiente) {
            b.disabled = true;
            b.classList.add("anim-brinco");
            slots[i].textContent = String(i + 1);
            slots[i].classList.add("anim-pop");
            Sfx.tick(siguiente + 1);
            siguiente++;
            if (siguiente >= ETAPAS.length) {
              resuelto = true;
              ctx.bien();
              ronda++;
              await espera(1100);
              if (ronda >= rondas) ctx.win();
              else jugar();
            }
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        filaEtapas.appendChild(b);
      });
      tablero.appendChild(filaEtapas);
      ctx.juego.appendChild(tablero);
    };
    jugar();
  },
};

/* ── FRACCIÓN DE UNA CANTIDAD (14-jul-2026, 6° grado NAP Bimestre 3
   "Ideas web": "balanza de fracciones — igualar peso con fracción mixta"
   — simplificado a cálculo directo de fracción de una cantidad, el
   contenido real detrás de "igualar el peso": 1/2 de 8 = 4). ── */
const FRACCION_CANTIDAD_BANCO = [
  { texto: "1/2 de 8", correcta: 4 },
  { texto: "1/4 de 12", correcta: 3 },
  { texto: "1/3 de 9", correcta: 3 },
  { texto: "3/4 de 8", correcta: 6 },
  { texto: "2/5 de 10", correcta: 4 },
  // agregados 14-jul-2026 (banco ampliado de 5 a 10).
  { texto: "1/5 de 15", correcta: 3 },
  { texto: "2/3 de 12", correcta: 8 },
  { texto: "3/5 de 20", correcta: 12 },
  { texto: "1/6 de 18", correcta: 3 },
  { texto: "5/6 de 12", correcta: 10 },
];
GAMES.fraccion_de_cantidad = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Cuánto es esta fracción de la cantidad?", "f");
      ctx.juego.innerHTML = "";
      let disp = FRACCION_CANTIDAD_BANCO.filter((x) => !usados.includes(x.texto));
      if (!disp.length) { usados = []; disp = FRACCION_CANTIDAD_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.texto);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:32px;font-family:'Baloo',sans-serif">${item.texto}</span>`));
      ctx.juego.appendChild(arriba);
      const opciones = new Set([item.correcta]);
      let guardas = 0;
      while (opciones.size < 3 && guardas < 50) {
        guardas++;
        const v = Math.max(1, item.correcta + rint(-3, 3));
        if (v !== item.correcta) opciones.add(v);
      }
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle([...opciones]).forEach((v) => {
        const b = el("button", "spriteBtn", `<span style="font-size:26px;font-family:'Baloo',sans-serif">${v}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === item.correcta) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── EL VOTO EN ARGENTINA (14-jul-2026, 6° grado NAP Bimestre 3 "Ideas
   web": "trivia de evolución del sufragio en Argentina"). Mismo patrón
   Verdadero/Falso que trivia_colonial. ── */
const SUFRAGIO_BANCO = [
  { afirmacion: "La Ley Sáenz Peña estableció el voto secreto y obligatorio", val: true },
  { afirmacion: "Antes de 1912 todos los hombres podían votar libremente y en secreto", val: false },
  { afirmacion: "Hipólito Yrigoyen fue elegido presidente en 1916 con la nueva ley", val: true },
  { afirmacion: "Las mujeres podían votar desde 1912", val: false },
  // agregados 14-jul-2026 (banco ampliado de 4 a 10). Hechos verificados:
  // Ley 13.010 (1947) y voto femenino real en 1951; "voto cantado" es el
  // término histórico correcto para el voto público pre-1912.
  { afirmacion: "El sufragio femenino en Argentina se logró en 1947, con la Ley 13.010", val: true },
  { afirmacion: "Antes de la Ley Sáenz Peña, el voto se llamaba \"voto cantado\" porque se decía en voz alta y no era secreto", val: true },
  { afirmacion: "Roque Sáenz Peña fue el presidente que impulsó la ley del voto secreto y obligatorio", val: true },
  { afirmacion: "La Ley Sáenz Peña de 1912 les dio el derecho a votar a las mujeres", val: false },
  { afirmacion: "El voto es obligatorio en Argentina desde la Ley Sáenz Peña de 1912", val: true },
  { afirmacion: "En Argentina votar es opcional: cada persona elige si quiere hacerlo", val: false },
];
GAMES.sufragio_argentina = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 4;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es verdadero o falso?", "f");
      ctx.juego.innerHTML = "";
      let disp = SUFRAGIO_BANCO.filter((x) => !usados.includes(x.afirmacion));
      if (!disp.length) { usados = []; disp = SUFRAGIO_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.afirmacion);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:20px;font-family:'Baloo',sans-serif">${item.afirmacion}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle([{ v: true, label: "✅ Verdadero" }, { v: false, label: "❌ Falso" }]).forEach(({ v, label }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:19px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === item.val) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿RENOVABLE O NO RENOVABLE? (14-jul-2026, 6° grado NAP Bimestre 4
   "Ideas web": "ciudad sustentable — distribuir fuentes de energía
   minimizando impacto" — simplificado a clasificar, mismo patrón que
   campo_ciudad/conductor_aislante). ── */
const ENERGIA_BANCO = [
  { e: "☀️", cat: "renovable" }, { e: "💨", cat: "renovable" }, { e: "💧", cat: "renovable" }, { e: "🌋", cat: "renovable" },
  { e: "⛽", cat: "no_renovable" }, { e: "⚫", cat: "no_renovable" }, { e: "☢️", cat: "no_renovable" },
  // agregados 14-jul-2026 (banco ampliado de 7 a 10).
  { e: "🌊", cat: "renovable" }, { e: "🌳", cat: "renovable" }, { e: "🛢️", cat: "no_renovable" },
];
GAMES.energia_renovable = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es una energía renovable o no renovable?", "n");
      ctx.juego.innerHTML = "";
      let disp = ENERGIA_BANCO.filter((x) => !usados.includes(x.e));
      if (!disp.length) { usados = []; disp = ENERGIA_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.e);
      const arriba = el("div", "tablero");
      const cont = el("div", "spriteQuieto anim-pop", `<span style="font-size:80px">${item.e}</span>`);
      arriba.appendChild(cont);
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      [{ cat: "renovable", label: "♻️ Renovable" }, { cat: "no_renovable", label: "🚫 No renovable" }].forEach(({ cat, label }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:17px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (cat === item.cat) {
            resuelto = true;
            cont.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿CUÁNTOS LADOS TIENE? (14-jul-2026, 6° grado NAP Bimestre 4 "Ideas
   web": "construir polígonos por nodos según ángulos/lados" —
   simplificado de construcción libre a reconocimiento: el motor no tiene
   una superficie de dibujo por nodos, y el contenido curricular real
   (relacionar el NOMBRE del polígono con su cantidad de lados) se puede
   verificar igual de bien con trivia). ── */
const POLIGONOS_BANCO = [
  { nombre: "Triángulo", lados: 3 }, { nombre: "Cuadrado", lados: 4 }, { nombre: "Pentágono", lados: 5 },
  { nombre: "Hexágono", lados: 6 }, { nombre: "Heptágono", lados: 7 }, { nombre: "Octágono", lados: 8 },
  // agregados 14-jul-2026 (banco ampliado de 6 a 10).
  { nombre: "Eneágono", lados: 9 }, { nombre: "Decágono", lados: 10 },
  { nombre: "Rectángulo", lados: 4 }, { nombre: "Rombo", lados: 4 },
];
GAMES.poligonos_lados = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Cuántos lados tiene esta figura?", "f");
      ctx.juego.innerHTML = "";
      let disp = POLIGONOS_BANCO.filter((x) => !usados.includes(x.nombre));
      if (!disp.length) { usados = []; disp = POLIGONOS_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.nombre);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:30px;font-family:'Baloo',sans-serif">${item.nombre}</span>`));
      ctx.juego.appendChild(arriba);
      const opciones = new Set([item.lados]);
      let guardas = 0;
      while (opciones.size < 3 && guardas < 50) {
        guardas++;
        const v = Math.max(3, item.lados + rint(-2, 2));
        if (v !== item.lados) opciones.add(v);
      }
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle([...opciones]).forEach((v) => {
        const b = el("button", "spriteBtn", `<span style="font-size:26px;font-family:'Baloo',sans-serif">${v}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === item.lados) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── TRADUCTOR ALGEBRAICO (14-jul-2026, 7° grado NAP Bimestre 1 "Ideas
   web": "traductor algebraico — emparejar oración con fórmula").
   Distractores por error de traducción REAL (agrupar mal, invertir la
   operación), nunca al azar. ── */
const ALGEBRA_BANCO = [
  { texto: "El doble de un número", correcta: "2x", d1: "x/2", d2: "x+2" },
  { texto: "El triple de un número", correcta: "3x", d1: "x+3", d2: "x/3" },
  { texto: "El doble más uno", correcta: "2x+1", d1: "2x-1", d2: "2(x+1)" },
  { texto: "La mitad de un número", correcta: "x/2", d1: "2x", d2: "x-2" },
  { texto: "El siguiente de un número", correcta: "x+1", d1: "x-1", d2: "2x" },
  { texto: "El triple menos dos", correcta: "3x-2", d1: "3x+2", d2: "3(x-2)" },
  // agregados 14-jul-2026 (banco ampliado de 6 a 10).
  { texto: "La mitad más dos", correcta: "x/2+2", d1: "x/2-2", d2: "(x+2)/2" },
  { texto: "El cuádruple de un número", correcta: "4x", d1: "x/4", d2: "x+4" },
  { texto: "El anterior de un número", correcta: "x-1", d1: "x+1", d2: "-x" },
  { texto: "El doble del siguiente de un número", correcta: "2(x+1)", d1: "2x+1", d2: "x+2" },
];
GAMES.traductor_algebraico = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "Elegí la fórmula que representa la frase", "f");
      ctx.juego.innerHTML = "";
      let disp = ALGEBRA_BANCO.filter((x) => !usados.includes(x.texto));
      if (!disp.length) { usados = []; disp = ALGEBRA_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.texto);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:24px;font-family:'Baloo',sans-serif">${item.texto}</span>`));
      ctx.juego.appendChild(arriba);
      const opciones = shuffle([item.correcta, item.d1, item.d2]);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      opciones.forEach((op) => {
        const b = el("button", "spriteBtn", `<span style="font-size:20px;font-family:'Baloo',sans-serif">${op}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op === item.correcta) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿TERRESTRE O GASEOSO? (14-jul-2026, 7° grado NAP Bimestre 1 "Ideas
   web": "simulador a escala del sistema solar — modificar órbitas" —
   simplificado a clasificar, mismo patrón que campo_ciudad/
   conductor_aislante: el motor no tiene mecánica de arrastre de órbitas
   ni escala física real, pero el contenido curricular — distinguir
   planetas terrestres de gaseosos — se verifica igual de bien así). ── */
// techo REAL de 8 (14-jul-2026): son los 8 planetas del sistema solar, ya
// están todos — agregar un 9° ítem obligaría a forzar una categoría
// incorrecta (Plutón no es limpiamente terrestre ni gaseoso) o inventar
// un cuerpo que no es un planeta. Mismo criterio que planta_fruto: techo
// honesto antes que contenido dudoso.
const PLANETAS_BANCO = [
  { nombre: "Mercurio", tipo: "terrestre" }, { nombre: "Venus", tipo: "terrestre" },
  { nombre: "Tierra", tipo: "terrestre" }, { nombre: "Marte", tipo: "terrestre" },
  { nombre: "Júpiter", tipo: "gaseoso" }, { nombre: "Saturno", tipo: "gaseoso" },
  { nombre: "Urano", tipo: "gaseoso" }, { nombre: "Neptuno", tipo: "gaseoso" },
];
GAMES.planetas_tipo = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es un planeta terrestre o gaseoso?", "m");
      ctx.juego.innerHTML = "";
      let disp = PLANETAS_BANCO.filter((x) => !usados.includes(x.nombre));
      if (!disp.length) { usados = []; disp = PLANETAS_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.nombre);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto anim-pop",
        `<span style="font-size:30px;font-family:'Baloo',sans-serif">${item.nombre}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      [{ v: "terrestre", label: "🪨 Terrestre" }, { v: "gaseoso", label: "💨 Gaseoso" }].forEach(({ v, label }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:18px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === item.tipo) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── LÍNEA DE TIEMPO: LA DEMOCRACIA (14-jul-2026, 7° grado NAP Bimestre 2
   "Ideas web": "línea de tiempo de la democracia — presidentes e hitos
   desde 1983"). Mismo patrón tap-en-orden que viaje_inmigrante. ── */
GAMES.linea_democracia = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 4;
    ctx.rondas(rondas);
    const ETAPAS = ["Golpe militar (1976)", "Guerra de Malvinas (1982)", "Recuperación de la democracia (1983)", "Juicio a las Juntas (1985)"];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      if (ronda === 0) ctx.consigna("Tocá los hechos históricos en el orden en que pasaron");
      else ctx.consigna(sacarDeBolsa(ctx, "orden", ORDEN_CORTAS));
      ctx.juego.innerHTML = "";
      const tablero = el("div", "tablero armarPalabraTablero");
      const filaSlots = el("div", "armarPalabraSlots");
      const slots = ETAPAS.map(() => el("div", "armarPalabraSlot", ""));
      slots.forEach((s) => filaSlots.appendChild(s));
      tablero.appendChild(filaSlots);
      const filaEtapas = el("div", "filaSprites");
      filaEtapas.style.marginTop = "18px";
      let siguiente = 0;
      let resuelto = false;
      shuffle(ETAPAS.map((s, i) => ({ s, i }))).forEach(({ s, i }) => {
        const b = el("button", "spriteBtn", `<span style="font-size:13px;font-family:'Baloo',sans-serif">${s}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto || b.disabled) return;
          if (i === siguiente) {
            b.disabled = true;
            b.classList.add("anim-brinco");
            slots[i].textContent = String(i + 1);
            slots[i].classList.add("anim-pop");
            Sfx.tick(siguiente + 1);
            siguiente++;
            if (siguiente >= ETAPAS.length) {
              resuelto = true;
              ctx.bien();
              ronda++;
              await espera(1100);
              if (ronda >= rondas) ctx.win();
              else jugar();
            }
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        filaEtapas.appendChild(b);
      });
      tablero.appendChild(filaEtapas);
      ctx.juego.appendChild(tablero);
    };
    jugar();
  },
};

/* ── APARATO REPRODUCTOR: FUNCIÓN (14-jul-2026, 7° grado NAP Bimestre 2
   "Ideas web": "diagrama interactivo de aparatos reproductores").
   Contenido de Educación Sexual Integral (ley 26.150, NAP obligatorio a
   esta edad) — registro estrictamente clínico/textual, sin imágenes,
   mismo patrón de matching que celula_partes. Distractores por
   confusión REAL (intercambiar el órgano equivalente del otro sexo, o
   con otro sistema del cuerpo), nunca al azar. ── */
const REPRODUCTOR_BANCO = [
  { parte: "Ovarios", correcta: "Producen los óvulos", d1: "Producen espermatozoides", d2: "Bombean la sangre" },
  { parte: "Testículos", correcta: "Producen los espermatozoides", d1: "Producen los óvulos", d2: "Filtran el aire" },
  { parte: "Útero", correcta: "Es donde se desarrolla el bebé", d1: "Es donde se producen los óvulos", d2: "Es donde se digieren los alimentos" },
  { parte: "Trompas de Falopio", correcta: "Conducen el óvulo hacia el útero", d1: "Producen espermatozoides", d2: "Almacenan la orina" },
  { parte: "Pene", correcta: "Órgano reproductor externo masculino", d1: "Órgano reproductor externo femenino", d2: "Glándula del crecimiento" },
  // agregados 14-jul-2026 (banco ampliado de 5 a 10). Mismo registro
  // clínico/textual, distractores por confusión real con otra parte del
  // banco (nunca al azar).
  { parte: "Vagina", correcta: "Canal de conexión con el exterior", d1: "Órgano donde se producen los óvulos", d2: "Órgano reproductor externo masculino" },
  { parte: "Glándula mamaria", correcta: "Produce leche para alimentar al bebé", d1: "Produce los óvulos", d2: "Produce los espermatozoides" },
  { parte: "Escroto", correcta: "Protege y regula la temperatura de los testículos", d1: "Produce los óvulos", d2: "Es donde se desarrolla el bebé" },
  { parte: "Cuello uterino", correcta: "Conecta el útero con la vagina", d1: "Produce los espermatozoides", d2: "Filtra la sangre" },
  { parte: "Placenta", correcta: "Nutre al bebé durante el embarazo", d1: "Protege a los testículos", d2: "Produce los óvulos" },
];
GAMES.sistema_reproductor = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Para qué sirve esta parte del aparato reproductor?", "f");
      ctx.juego.innerHTML = "";
      let disp = REPRODUCTOR_BANCO.filter((x) => !usados.includes(x.parte));
      if (!disp.length) { usados = []; disp = REPRODUCTOR_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.parte);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:26px;font-family:'Baloo',sans-serif">${item.parte}</span>`));
      ctx.juego.appendChild(arriba);
      const opciones = shuffle([item.correcta, item.d1, item.d2]);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      opciones.forEach((op) => {
        const b = el("button", "spriteBtn", `<span style="font-size:15px;font-family:'Baloo',sans-serif">${op}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op === item.correcta) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── MEDIA, MODA O MEDIANA (14-jul-2026, 7° grado NAP Bimestre 3 "Ideas
   web": "creador de gráficos dinámicos — datos → gráfico automático con
   promedio" — simplificado a calcular el promedio directo, el contenido
   real detrás de "gráfico con promedio"; el motor no arma gráficos
   dinámicos de barras arrastrables, pero el cálculo SÍ se verifica). ── */
const ESTADISTICA_BANCO = [
  { nums: [4, 4, 5, 6, 11], media: 6, moda: 4, mediana: 5 },
  { nums: [3, 3, 4, 9, 11], media: 6, moda: 3, mediana: 4 },
  { nums: [2, 3, 3, 7, 10], media: 5, moda: 3, mediana: 3 },
  { nums: [1, 1, 2, 7, 9], media: 4, moda: 1, mediana: 2 },
  { nums: [1, 1, 6, 6, 6], media: 4, moda: 6, mediana: 6 },
  { nums: [1, 3, 9, 11, 11], media: 7, moda: 11, mediana: 9 },
  { nums: [1, 3, 8, 8, 10], media: 6, moda: 8, mediana: 8 },
  { nums: [2, 2, 4, 5, 12], media: 5, moda: 2, mediana: 4 },
  { nums: [2, 2, 7, 8, 11], media: 6, moda: 2, mediana: 7 },
  { nums: [2, 4, 10, 12, 12], media: 8, moda: 12, mediana: 10 },
  { nums: [1, 1, 7, 9, 12], media: 6, moda: 1, mediana: 7 },
  { nums: [2, 3, 7, 9, 9], media: 6, moda: 9, mediana: 7 },
  { nums: [4, 6, 6, 8, 11], media: 7, moda: 6, mediana: 6 },
  { nums: [1, 6, 6, 6, 6], media: 5, moda: 6, mediana: 6 },
  { nums: [1, 6, 7, 8, 8], media: 6, moda: 8, mediana: 7 },
  { nums: [4, 6, 6, 9, 10], media: 7, moda: 6, mediana: 6 },
  { nums: [2, 2, 6, 7, 8], media: 5, moda: 2, mediana: 6 },
  { nums: [3, 3, 5, 9, 10], media: 6, moda: 3, mediana: 5 }
];
GAMES.estadistica_datos = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    // Estadística REAL (7° DC, docs/auditoria-dc-caba/): rota MEDIA / MODA /
    // MEDIANA, no solo el promedio. Los distractores son las OTRAS dos medidas
    // (el error típico: confundir una con otra) → C4 misconception.
    const MEDIDAS = [
      { k: "media",   q: "¿Cuál es el promedio (la media) de estos números?",
        m: "La media: sumá todos los números y dividí por la cantidad." },
      { k: "moda",    q: "¿Cuál es la moda (el número que más se repite)?",
        m: "La moda es el valor que aparece más veces en la lista." },
      { k: "mediana", q: "¿Cuál es la mediana? Ordenalos de menor a mayor y buscá el del medio.",
        m: "La mediana es el valor que queda justo en el medio cuando ordenás los números." },
    ];
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = ESTADISTICA_BANCO.filter((x) => !usados.includes(x.nums.join()));
      if (!disp.length) { usados = []; disp = ESTADISTICA_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.nums.join());
      const medida = MEDIDAS[rint(0, 2)];
      const correcta = item[medida.k];
      ctx.item("estadistica_" + medida.k);
      consignaVariada(ctx, ronda, medida.q, "n");
      ctx.juego.innerHTML = "";
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:26px;font-family:'Baloo',sans-serif">${item.nums.join(", ")}</span>`));
      ctx.juego.appendChild(arriba);
      const opciones = new Set([correcta]);
      [item.media, item.moda, item.mediana].forEach((v) => { if (opciones.size < 3) opciones.add(v); });
      let guardas = 0;
      while (opciones.size < 3 && guardas < 50) {
        guardas++;
        const v = Math.max(1, correcta + rint(-3, 3));
        if (v !== correcta) opciones.add(v);
      }
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle([...opciones]).forEach((v) => {
        const b = el("button", "spriteBtn", `<span style="font-size:26px;font-family:'Baloo',sans-serif">${v}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === correcta) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi(medida.m);
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── PRODUCTOR, CONSUMIDOR O DESCOMPONEDOR (14-jul-2026, 7° grado NAP
   Bimestre 3 "Ideas web": "simulador de red trófica — retirar un
   eslabón, ver el colapso" — simplificado a clasificar el rol de cada
   ser vivo, mismo patrón de 3 categorías que partes_oracion: el motor
   no tiene una red de nodos con propagación de colapso, pero el
   contenido curricular real — el ROL de cada eslabón — se verifica
   igual de bien clasificando). ── */
const RED_TROFICA_BANCO = [
  { e: "🌾 Pasto", rol: "productor" }, { e: "🌳 Árbol", rol: "productor" },
  { e: "🐇 Conejo", rol: "consumidor" }, { e: "🦁 León", rol: "consumidor" }, { e: "🦌 Ciervo", rol: "consumidor" },
  { e: "🍄 Hongo", rol: "descomponedor" }, { e: "🦠 Bacteria", rol: "descomponedor" },
  // agregados 14-jul-2026 (banco ampliado de 7 a 10).
  { e: "🌻 Girasol", rol: "productor" }, { e: "🐺 Lobo", rol: "consumidor" }, { e: "🪱 Lombriz", rol: "descomponedor" },
];
GAMES.red_trofica = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Es productor, consumidor o descomponedor?", "n");
      ctx.juego.innerHTML = "";
      let disp = RED_TROFICA_BANCO.filter((x) => !usados.includes(x.e));
      if (!disp.length) { usados = []; disp = RED_TROFICA_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.e);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto anim-pop",
        `<span style="font-size:26px;font-family:'Baloo',sans-serif">${item.e}</span>`));
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle(["productor", "consumidor", "descomponedor"]).forEach((rol) => {
        const b = el("button", "spriteBtn", `<span style="font-size:17px;font-family:'Baloo',sans-serif">${rol}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (rol === item.rol) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ÁREA DE LA HABITACIÓN (14-jul-2026, 7° grado NAP Bimestre 4 "Ideas
   web": "diseñador de planos virtual — arrastrar muebles/paredes, área/
   perímetro en vivo" — simplificado a calcular el área total de una
   figura compuesta por 2 rectángulos, el contenido curricular real
   ("figuras compuestas"); el motor no tiene arrastre libre de paredes
   con recálculo en vivo). Registro abstracto/textual a propósito — a
   los 12 años el propio informe (§ banda de edad) ya no pide andamiaje
   visual concreto, mismo criterio que trivia_colonial/sufragio_argentina. ── */
const AREA_BANCO = [
  { texto: "Rectángulo A: 4m × 3m.<br>Rectángulo B: 2m × 2m.", correcta: 16 },
  { texto: "Rectángulo A: 5m × 2m.<br>Rectángulo B: 3m × 3m.", correcta: 19 },
  { texto: "Rectángulo A: 6m × 2m.<br>Rectángulo B: 4m × 1m.", correcta: 16 },
  { texto: "Rectángulo A: 3m × 3m.<br>Rectángulo B: 2m × 4m.", correcta: 17 },
  { texto: "Rectángulo A: 7m × 2m.<br>Rectángulo B: 3m × 2m.", correcta: 20 },
  // agregados 14-jul-2026 (banco ampliado de 5 a 10).
  { texto: "Rectángulo A: 8m × 3m.<br>Rectángulo B: 2m × 5m.", correcta: 34 },
  { texto: "Rectángulo A: 4m × 4m.<br>Rectángulo B: 3m × 2m.", correcta: 22 },
  { texto: "Rectángulo A: 5m × 3m.<br>Rectángulo B: 4m × 2m.", correcta: 23 },
  { texto: "Rectángulo A: 6m × 3m.<br>Rectángulo B: 2m × 2m.", correcta: 22 },
  { texto: "Rectángulo A: 9m × 2m.<br>Rectángulo B: 3m × 3m.", correcta: 27 },
];
GAMES.area_perimetro = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Cuál es el área total de la habitación?", "f");
      ctx.juego.innerHTML = "";
      let disp = AREA_BANCO.filter((x) => !usados.includes(x.texto));
      if (!disp.length) { usados = []; disp = AREA_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.texto);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:19px;line-height:1.5;font-family:'Baloo',sans-serif">${item.texto}</span>`));
      ctx.juego.appendChild(arriba);
      const opciones = new Set([item.correcta]);
      let guardas = 0;
      while (opciones.size < 3 && guardas < 50) {
        guardas++;
        const v = Math.max(1, item.correcta + rint(-3, 3));
        if (v !== item.correcta) opciones.add(v);
      }
      const fila = el("div", "filaSprites");
      let resuelto = false;
      shuffle([...opciones]).forEach((v) => {
        const b = el("button", "spriteBtn", `<span style="font-size:22px;font-family:'Baloo',sans-serif">${v} m²</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === item.correcta) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ESCAPE ROOM DE EGRESO (14-jul-2026, 7° grado NAP Bimestre 4 "Ideas
   web": "escape room de egreso — integrando matemática, historia,
   gramática y biología del año" — simplificado a trivia mixta que
   recorre las 4 áreas del año, mismo patrón de matching que
   celula_partes: el motor no tiene una mecánica de "sala" con
   combinaciones/candados, pero el espíritu integrador — repasar
   contenido de TODO el año antes de egresar — se cumple igual
   recorriendo una pregunta de cada área por ronda). Consigna fija
   porque el contenido varía por pregunta (misma regla que celula_partes/
   fraccion_de_cantidad). ── */
const ESCAPE_ROOM_BANCO = [
  { texto: "¿Cuál es el mínimo común múltiplo de 4 y 6?", correcta: "12", d1: "24", d2: "10" },
  { texto: "¿En qué año volvió la democracia a la Argentina?", correcta: "1983", d1: "1976", d2: "1990" },
  { texto: "En \"El perro grande ladra fuerte\", ¿cuál es el sujeto?", correcta: "El perro grande", d1: "ladra fuerte", d2: "grande" },
  { texto: "Quemar un papel, ¿es un cambio físico o químico?", correcta: "Químico", d1: "Físico", d2: "Ninguno de los dos" },
  { texto: "Si más obreros hacen un trabajo, el tiempo necesario...", correcta: "Disminuye", d1: "Aumenta", d2: "Se mantiene igual" },
  { texto: "¿Cuál es el planeta más grande del sistema solar?", correcta: "Júpiter", d1: "Saturno", d2: "Tierra" },
  { texto: "¿Cuál de estos es un país de América Latina?", correcta: "Perú", d1: "Canadá", d2: "Portugal" },
  { texto: "¿Cuál de estas palabras lleva tilde?", correcta: "¿Cuándo?", d1: "Cuando", d2: "Cuanto" },
  // agregados 14-jul-2026 (banco ampliado de 8 a 10).
  { texto: "¿Cuál es la fórmula de 'el doble de un número'?", correcta: "2x", d1: "x/2", d2: "x+2" },
  { texto: "¿Qué gas liberan las plantas durante la fotosíntesis?", correcta: "Oxígeno", d1: "Dióxido de carbono", d2: "Nitrógeno" },
];
GAMES.escape_room_egreso = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "Elegí la respuesta correcta", "n");
      ctx.juego.innerHTML = "";
      let disp = ESCAPE_ROOM_BANCO.filter((x) => !usados.includes(x.texto));
      if (!disp.length) { usados = []; disp = ESCAPE_ROOM_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.texto);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:19px;font-family:'Baloo',sans-serif">${item.texto}</span>`));
      ctx.juego.appendChild(arriba);
      const opciones = shuffle([item.correcta, item.d1, item.d2]);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      opciones.forEach((op) => {
        const b = el("button", "spriteBtn", `<span style="font-size:17px;font-family:'Baloo',sans-serif">${op}</span>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (op === item.correcta) {
            resuelto = true;
            b.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(900);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── PROGRAMÁ EL CAMINO (14-jul-2026, prototipo de pensamiento
   computacional — idea de Pablo: "armar instrucciones, apretar play, ver
   la animación completa"). Primera mecánica del motor de "armar programa
   → ejecutar" — reusa el generador de laberintos YA VERIFICADO por BFS
   (mismo `_lab_json` que usa el laberinto normal, acá con un tamaño
   propio bien chico — `D.laberintosChicos`, 3-4 celdas — porque escribir
   la secuencia completa a mano en un laberinto de 9-12 celdas sería
   larguísimo). Estilo Logo/turtle graphics: el chico arma una lista de
   instrucciones (avanzar/girar) tocando botones, después mira la
   ejecución animada paso a paso. Sin loops/repetición todavía — es un
   prototipo para validar la mecánica antes de pensar en escalarla por
   edad (loops para años más grandes, menos instrucciones para más
   chicos). "Cero fail states": chocar contra una pared no termina la
   ronda, solo la reinicia — el programa armado queda igual para poder
   corregirlo con "Deshacer" en vez de reescribirlo entero. ── */
GAMES.programar_camino = {
  crear(ctx) {
    const labs = (D.laberintos_chicos || []).slice(0, 3);
    if (!labs.length) { ctx.rondas(0); ctx.win(); return; }
    ctx.rondas(labs.length);
    // Progresión de Programación por grado (docs/auditoria-dc-caba/): 1°-2°
    // SECUENCIA (F/L/R); desde 3° (edad≥8) el BUCLE (repetir ×N); desde 5°
    // (edad≥10) el CONDICIONAL "⏩ avanzar hasta la pared" (avanza MIENTRAS haya
    // camino) — los hitos secuencia→bucle→condicional del DC.
    const conBucle = ((D.edad | 0) >= 8);
    const conCondicional = ((D.edad | 0) >= 10);
    const ORDEN = ["E", "S", "W", "N"];
    const DELTA = { E: [1, 0], S: [0, 1], W: [-1, 0], N: [0, -1] };
    const DEG = { N: 0, E: 90, S: 180, W: 270 };
    const BIT = { N: 1, S: 2, E: 4, W: 8 };
    let nivel = 0;
    const arrancar = () => {
      ctx.ronda(nivel);
      ctx.consigna(conCondicional
        ? "Armá el programa: 🔁 repite y ⏩ avanza hasta la pared. Apretá Jugar."
        : conBucle
          ? "Armá el programa (usá 🔁 para repetir sin escribir tanto) y apretá Jugar"
          : "Armá el programa y apretá Jugar para ver el recorrido");
      ctx.juego.innerHTML = "";
      const lab = labs[nivel];
      const n = lab.n, C = 64, M = 10, S = n * C + M * 2;
      const NS = "http://www.w3.org/2000/svg";
      const svg = document.createElementNS(NS, "svg");
      svg.setAttribute("viewBox", `0 0 ${S} ${S}`);
      svg.setAttribute("class", "svgJuego lienzo");
      // laberinto CHICO (3-4 celdas): no hace falta que ocupe todo el ancho
      // como el laberinto normal — abajo hay 2 filas más de botones, y a
      // ancho completo la altura total no entraba en la pantalla (Pablo,
      // 14-jul-2026: "la de robótica no entra").
      svg.style.maxWidth = "230px";
      svg.style.margin = "0 auto";
      let d = "";
      const X = (x) => M + x * C, Y = (y) => M + y * C;
      for (let y = 0; y < n; y++)
        for (let x = 0; x < n; x++) {
          const b = lab.celdas[y][x];
          if (b & 1) d += `M${X(x)} ${Y(y)}h${C}`;
          if (b & 8) d += `M${X(x)} ${Y(y)}v${C}`;
          if (y === n - 1 && (b & 2)) d += `M${X(x)} ${Y(y + 1)}h${C}`;
          if (x === n - 1 && (b & 4)) d += `M${X(x + 1)} ${Y(y)}v${C}`;
        }
      const muros = document.createElementNS(NS, "path");
      muros.setAttribute("d", d);
      muros.setAttribute("stroke", D.paleta.ink);
      muros.setAttribute("stroke-width", 9);
      muros.setAttribute("stroke-linecap", "round");
      muros.setAttribute("fill", "none");
      const meta = document.createElementNS(NS, "text");
      meta.textContent = "⭐";
      meta.setAttribute("font-size", C * 0.62);
      meta.setAttribute("text-anchor", "middle");
      meta.setAttribute("x", X(n - 1) + C / 2);
      meta.setAttribute("y", Y(n - 1) + C * 0.72);
      const turtle = document.createElementNS(NS, "text");
      turtle.textContent = "▲";
      turtle.setAttribute("font-size", C * 0.6);
      turtle.setAttribute("text-anchor", "middle");
      turtle.setAttribute("fill", D.paleta.ac);
      turtle.style.transition = "transform .45s ease";
      turtle.style.transformOrigin = "center";
      turtle.style.transformBox = "fill-box";
      let cur = { x: 0, y: 0, dir: "E" };
      const ubicar = () => {
        turtle.setAttribute("x", X(cur.x) + C / 2);
        turtle.setAttribute("y", Y(cur.y) + C * 0.7);
        turtle.style.transform = `rotate(${DEG[cur.dir]}deg)`;
      };
      ubicar();
      svg.append(muros, meta, turtle);
      const tab = el("div", "tablero");
      tab.appendChild(svg);
      ctx.juego.appendChild(tab);

      const abierta = (x, y, dir) => !(lab.celdas[y][x] & BIT[dir]);

      let programa = [];   // items: { c: "F"|"L"|"R", n: veces }
      let jugando = false;
      const ICONOS = { F: "⬆️", L: "↩️", R: "↪️", H: "⏩" };
      const cola = el("div", "programaCola");
      const pintarCola = () => {
        cola.innerHTML = programa.length
          ? programa.map((p) => `<span class="programaChip">${ICONOS[p.c]}${p.n > 1 ? "×" + p.n : ""}</span>`).join("")
          : `<span class="programaVacio">Tocá los botones para armar tu programa</span>`;
      };
      pintarCola();
      ctx.juego.appendChild(cola);

      const filaInstr = el("div", "filaSprites");
      [["F", "⬆️ Avanzar"], ["L", "↩️ Girar izq."], ["R", "↪️ Girar der."]].forEach(([codigo, label]) => {
        const b = el("button", "spriteBtn", `<span style="font-size:15px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", () => {
          if (jugando) return;
          programa.push({ c: codigo, n: 1 });
          pintarCola();
        });
        filaInstr.appendChild(b);
      });
      if (conCondicional) {   // CONDICIONAL: ⏩ avanza MIENTRAS haya camino (hasta la pared)
        const bH = el("button", "spriteBtn", `<span style="font-size:15px;font-family:'Baloo',sans-serif">⏩ Hasta la pared</span>`);
        bH.addEventListener("click", () => {
          if (jugando) return;
          programa.push({ c: "H", n: 1 });
          pintarCola();
        });
        filaInstr.appendChild(bH);
      }
      if (conBucle) {   // BUCLE: 🔁 repite la ÚLTIMA instrucción una vez más (F → F×2 → F×3…)
        const bRep = el("button", "spriteBtn", `<span style="font-size:15px;font-family:'Baloo',sans-serif">🔁 Repetir</span>`);
        bRep.addEventListener("click", () => {
          if (jugando || !programa.length) return;
          const ult = programa[programa.length - 1];
          if (ult.n < 5) { ult.n++; pintarCola(); }
        });
        filaInstr.appendChild(bRep);
      }
      ctx.juego.appendChild(filaInstr);

      const filaAcciones = el("div", "filaSprites");
      filaAcciones.style.marginTop = "14px";
      const btnDeshacer = el("button", "btn suave", "⌫ Deshacer");
      btnDeshacer.addEventListener("click", () => {
        if (jugando) return;
        programa.pop();
        pintarCola();
      });
      const btnJugar = el("button", "btn verde", "▶️ ¡Jugar!");
      filaAcciones.append(btnDeshacer, btnJugar);
      ctx.juego.appendChild(filaAcciones);

      btnJugar.addEventListener("click", async () => {
        if (jugando || !programa.length) return;
        jugando = true;
        cur = { x: 0, y: 0, dir: "E" };
        ubicar();
        await espera(300);
        let choco = false;
        prog:
        for (const instr of programa) {
          for (let k = 0; k < instr.n; k++) {      // el BUCLE: repite la instrucción n veces
            await espera(500);
            if (instr.c === "L") cur.dir = ORDEN[(ORDEN.indexOf(cur.dir) + 3) % 4];
            else if (instr.c === "R") cur.dir = ORDEN[(ORDEN.indexOf(cur.dir) + 1) % 4];
            else if (instr.c === "F") {
              const [dx, dy] = DELTA[cur.dir];
              const nx = cur.x + dx, ny = cur.y + dy;
              if (nx < 0 || ny < 0 || nx >= n || ny >= n || !abierta(cur.x, cur.y, cur.dir)) {
                choco = true;
                ubicar();
                break prog;
              }
              cur = { x: nx, y: ny, dir: cur.dir };
            }
            else if (instr.c === "H") {   // CONDICIONAL: avanzar mientras haya camino (hasta la pared)
              let pasos = 0;
              while (abierta(cur.x, cur.y, cur.dir)) {
                const [dx, dy] = DELTA[cur.dir];
                const nx = cur.x + dx, ny = cur.y + dy;
                if (nx < 0 || ny < 0 || nx >= n || ny >= n) break;
                cur = { x: nx, y: ny, dir: cur.dir };
                ubicar();
                if (cur.x === n - 1 && cur.y === n - 1) break;   // llegó a la ⭐
                if (++pasos > n * n) break;                      // tope defensivo
                await espera(400);
              }
            }
            ubicar();
          }
        }
        jugando = false;
        if (choco) {
          turtle.style.animation = "sacudir .4s ease";
          setTimeout(() => (turtle.style.animation = ""), 450);
          ctx.casi();
          return;
        }
        if (cur.x === n - 1 && cur.y === n - 1) {
          ctx.bien();
          nivel++;
          await espera(700);
          if (nivel >= labs.length) ctx.win();
          else arrancar();
        } else {
          ctx.casi();
        }
      });
    };
    arrancar();
  },
};

GAMES.serie = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Qué número falta?", "m");
      ctx.juego.innerHTML = "";
      // sube la dificultad, pero sin un corte fijo en la mitad exacta (que
      // hacía adivinable CUÁNDO cambia el tipo de patrón): más probable +1
      // al principio, +2 hacia el final, con el medio genuinamente al azar.
      const progreso = rondas > 1 ? ronda / (rondas - 1) : 0;
      const paso = Math.random() < progreso ? 2 : 1;
      // tope (14-jul-2026, 1° grado NAP: "números del 1 al 30"): 16 reproduce
      // el rango histórico sin cfg.tope (12 con paso 1, 8 con paso 2 — la
      // cuenta de siempre), más alto solo si el juego lo pide.
      const tope = ctx.cfg.tope || 16;
      const desde = rint(1, Math.max(1, tope - 4 * paso));
      const seq = Array.from({ length: 5 }, (_, i) => desde + i * paso);
      const falta = rint(1, 4);
      const fila = el("div", "serieFila");
      let resuelto = false;
      seq.forEach((v, i) => {
        fila.appendChild(el("div", i === falta ? "hueco2" : "num", i === falta ? "?" : v));
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
      const ops = el("div", "ops");
      const distr = new Set([seq[falta]]);
      while (distr.size < 3) {
        const v = seq[falta] + rint(-3, 3);
        if (v >= 0) distr.add(v);
      }
      shuffle([...distr]).forEach((v) => {
        const b = el("button", "op", v);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (v === seq[falta]) {
            resuelto = true;
            const h = fila.children[falta];
            h.className = "num anim-pop";
            h.textContent = v;
            // la serie se "canta" en orden
            [...fila.children].forEach((d, i) => setTimeout(() => {
              d.classList.add("anim-brinco"); Sfx.tick(i + 1);
            }, i * 130));
            ctx.bien();
            ronda++;
            await espera(1100);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.classList.add("casi");
            setTimeout(() => b.classList.remove("casi"), 450);
            ctx.casi();
          }
        });
        ops.appendChild(b);
      });
      ctx.juego.appendChild(ops);
    };
    jugar();
  },
};

/* ── ESCUCHÁ Y REPETÍ — memoria auditiva/visual tipo Simon: la secuencia crece
   un color por nivel; un error nunca hace perder nada, solo repite la secuencia
   completa y deja reintentar (cero fail states). ── */
// Ampliado de 5 a 9 colores (15-jul-2026, Pablo: "6to y 7mo 9 botones en 3
// filas... 4 y 5to 2 filas de 4... 3ro 2 filas de 3... 2do 5 botones y 1ro 4").
const SIMON_COLORES = [
  { c: "#E25555", nota: 392 }, { c: "#4F86C6", nota: 330 }, { c: "#F2C94C", nota: 262 },
  { c: "#4CAF7D", nota: 440 }, { c: "#9B6BD6", nota: 494 }, { c: "#F2994A", nota: 349 },
  { c: "#E17DC2", nota: 294 }, { c: "#2FB6B6", nota: 523 }, { c: "#8BC34A", nota: 466 },
];
const SIMON_MIRA_CORTAS = ["Mirá bien…", "Prestá atención…", "Otra vez, mirá…"];
const SIMON_REPETI_CORTAS = ["Ahora repetí", "Tu turno, tocalos en orden", "¿Te acordás? Repetí"];
GAMES.simon = {
  crear(ctx) {
    const nColores = Math.min(ctx.cfg.colores || 4, SIMON_COLORES.length);
    const filas = Math.max(1, ctx.cfg.filas || 1);
    const rondas = ctx.cfg.rondas || 5;
    const colores = SIMON_COLORES.slice(0, nColores);
    ctx.rondas(rondas);
    const seq = [];
    let nivel = 0, entrada = [], reproduciendo = false, botones = [];

    const flash = (i, dur) => {
      const b = botones[i];
      b.style.filter = "brightness(1.55)"; b.style.transform = "scale(1.06)";
      Sfx._nota(colores[i].nota, 0, (dur || 320) / 1000, "triangle", 0.18);
      setTimeout(() => { b.style.filter = ""; b.style.transform = ""; }, dur || 320);
    };
    const reproducir = async () => {
      reproduciendo = true;
      // Pablo 15-jul-2026: "mira y escucha" se cortaba en seco — el mismo bug
      // ya arreglado en suma_columnas (reproducirConsigna() pausa el audio
      // anterior apenas arranca uno nuevo; acá el flash de la secuencia
      // empezaba a los 400ms fijos, sin esperar a que la frase realmente
      // terminara de sonar). Ahora se espera el audio real + una pausa de
      // respiro antes de arrancar la secuencia.
      const mira = nivel === 0 ? "Mirá y escuchá…" : sacarDeBolsa(ctx, "mira", SIMON_MIRA_CORTAS);
      $("#consignaTexto").innerHTML = mira;
      const sonó = await reproducirConsigna(mira);
      await espera(sonó ? 500 : 400);
      for (let i = 0; i < seq.length; i++) { flash(seq[i], 380); await espera(480); }
      reproduciendo = false;
      entrada = [];
      ctx.consigna(nivel === 0 ? "Ahora repetí vos, tocando en el mismo orden" : sacarDeBolsa(ctx, "repeti", SIMON_REPETI_CORTAS));
    };
    const construir = () => {
      ctx.juego.innerHTML = "";
      // grilla de `filas` filas × columnas (columnas = nColores/filas hacia
      // arriba) en vez de una sola fila que se apretaba con muchos botones —
      // filas=1 (default, 1°/2° grado) se ve exactamente igual que antes.
      const cols = Math.ceil(nColores / filas);
      const fila = el("div", "filaSprites");
      fila.style.cssText = `max-width:${Math.min(480, cols * 112)}px;margin:0 auto;display:grid;` +
        `grid-template-columns:repeat(${cols},1fr);gap:14px;justify-items:center`;
      const TAM = cols >= 5 ? 76 : cols === 4 ? 88 : 100;
      botones = colores.map((col, i) => {
        const b = el("button", "spriteBtn");
        b.style.cssText = `width:${TAM}px;height:${TAM}px;background:${col.c};border-radius:26px`;
        b.addEventListener("click", async () => {
          if (reproduciendo) return;
          flash(i, 220);
          entrada.push(i);
          const pos = entrada.length - 1;
          if (entrada[pos] !== seq[pos]) {
            ctx.casi();
            await espera(500);
            await reproducir();   // repasa la secuencia entera, sin penalizar
            return;
          }
          if (entrada.length === seq.length) {
            ctx.bien();
            nivel++;
            await espera(500);
            if (nivel >= rondas) { ctx.win(); return; }
            jugar();
          }
        });
        fila.appendChild(b);
        return b;
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    const jugar = async () => {
      ctx.ronda(nivel);
      seq.push(rint(0, nColores - 1));
      construir();
      await espera(300);
      await reproducir();
    };
    jugar();
  },
};

/* ── ¿DÓNDE VA? — clasificar: cada amigo va a la canasta de su igual (tap, sin
   drag — más robusto en mobile). ── */
GAMES.agrupar = {
  minP: 2,
  crear(ctx) {
    const canastas = Math.min(ctx.cfg.canastas || 2, P.length);
    const rondas = ctx.cfg.rondas || 6;
    const refs = sample(P, canastas);
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿A qué canasta va?", "n");
      ctx.juego.innerHTML = "";
      const item = refs[rint(0, canastas - 1)];
      const arriba = el("div", "tablero");
      const cont = el("div", "spriteQuieto anim-pop",
        `<img src="${item}" alt="" style="width:120px;height:120px">`);
      arriba.appendChild(cont);
      ctx.juego.appendChild(arriba);
      const fila = el("div", "filaSprites");
      let resuelto = false;
      refs.forEach((r) => {
        const b = el("button", "spriteBtn", `<div style="position:relative">
          <img src="${r}" alt="" style="width:96px;height:96px;opacity:.55">
          <div style="position:absolute;bottom:-6px;right:-6px;font-size:26px">🧺</div>
        </div>`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (r === item) {
            resuelto = true;
            cont.classList.add("anim-brinco");
            ctx.bien();
            ronda++;
            await espera(700);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        fila.appendChild(b);
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
    };
    jugar();
  },
};

/* ── ¿QUÉ FALTA? — atención y memoria a corto plazo: se muestran los amigos, se
   tapa uno y hay que reconocerlo entre las opciones (sin escribir/leer). ── */
const QUEFALTA_MIRA_CORTAS = ["Mirá otra vez…", "Fijate bien quiénes están…", "Prestá atención…"];
const QUEFALTA_QUIEN_CORTAS = ["¿Y ahora, quién falta?", "¿Quién no está?", "¿Quién se fue?"];
GAMES.quefalta = {
  minP: 3,
  crear(ctx) {
    const n = Math.min(ctx.cfg.items || 4, P.length);
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = async () => {
      ctx.ronda(ronda);
      const grupo = sample(P, n);
      const faltaIdx = rint(0, n - 1);
      const falta = grupo[faltaIdx];
      ctx.consigna(ronda === 0 ? "Mirá bien quiénes están…" : sacarDeBolsa(ctx, "mira", QUEFALTA_MIRA_CORTAS));
      ctx.juego.innerHTML = "";
      const fila = el("div", "filaSprites");
      const TAM = Math.min(120, Math.floor((Math.min(innerWidth, 1000) - 80) / n) - 12);
      const celdas = grupo.map((s) => {
        const d = el("div", "spriteQuieto", `<img src="${s}" alt="" style="width:${TAM}px;height:${TAM}px">`);
        fila.appendChild(d);
        return d;
      });
      ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
      await espera(2200);
      ctx.consigna(ronda === 0 ? "¿Quién se escondió?" : sacarDeBolsa(ctx, "quien", QUEFALTA_QUIEN_CORTAS));
      celdas[faltaIdx].innerHTML = `<div class="hueco" style="width:${TAM}px;height:${TAM}px">?</div>`;
      const ops = el("div", "ops");
      let resuelto = false;
      shuffle(grupo).forEach((s) => {
        const b = el("button", "spriteBtn", `<img src="${s}" alt="" style="width:78px;height:78px">`);
        b.addEventListener("click", async () => {
          if (resuelto) return;
          if (s === falta) {
            resuelto = true;
            celdas[faltaIdx].innerHTML = `<img src="${s}" alt="" style="width:${TAM}px;height:${TAM}px">`;
            celdas[faltaIdx].classList.add("anim-pop");
            ctx.bien();
            ronda++;
            await espera(800);
            if (ronda >= rondas) ctx.win();
            else jugar();
          } else {
            b.style.animation = "sacudir .4s ease";
            setTimeout(() => (b.style.animation = ""), 450);
            ctx.casi();
          }
        });
        ops.appendChild(b);
      });
      ctx.juego.appendChild(ops);
    };
    jugar();
  },
};

/* ── BINGO DE AMIGOS — escaneo visual, sin necesidad de leer: se pide un amigo
   por vez (con imagen de pista) y hay que encontrarlo en la grilla. ── */
const BINGO_CORTAS = ["¿Y ahora, a quién buscamos?", "Encontrá a:", "¿Dónde está:"];
GAMES.bingo = {
  minP: 4,
  crear(ctx) {
    const tam = Math.min(ctx.cfg.tam || 6, P.length);
    const cols = tam <= 4 ? 2 : 3;
    const items = sample(P, tam);
    const orden = shuffle(items);
    ctx.rondas(tam);
    let encontrados = 0, objetivo = orden[0];
    const gridInner = el("div");
    gridInner.style.cssText =
      `display:grid;grid-template-columns:repeat(${cols},1fr);gap:12px;max-width:${cols * 130}px;margin:0 auto`;
    items.forEach((s) => {
      const b = el("button", "spriteBtn", `<img src="${s}" alt="" style="width:96px;height:96px">`);
      b.addEventListener("click", async () => {
        if (b.dataset.ok) return;
        if (s === objetivo) {
          b.dataset.ok = "1";
          b.style.opacity = ".4";
          b.disabled = true;
          b.classList.add("anim-brinco");
          ctx.bien();
          encontrados++;
          ctx.ronda(encontrados);
          if (encontrados >= tam) { await espera(500); ctx.win(); return; }
          objetivo = orden[encontrados];
          ctx.consigna(sacarDeBolsa(ctx, "bingo", BINGO_CORTAS), objetivo);
        } else {
          b.style.animation = "sacudir .4s ease";
          setTimeout(() => (b.style.animation = ""), 450);
          ctx.casi();
        }
      });
      gridInner.appendChild(b);
    });
    ctx.consigna("Buscá a:", objetivo);
    ctx.juego.appendChild(el("div", "tablero")).appendChild(gridInner);
  },
};
