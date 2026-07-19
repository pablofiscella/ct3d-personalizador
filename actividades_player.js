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
  actual: null, fallos: 0, _rondas: 0, _nuevoLogro: false,
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
        if (!yaEstabaCompleto && todoCompleto()) self._nuevoLogro = true;
        pintarHeader();
        festejar(e);
      },
      confeti(n) { Confeti.tirar(n); },
    };
  },
};

function festejar(estrellas) {
  Sfx.fanfarria();
  Confeti.tirar(140);
  $("#festejoTitulo").textContent = Store.data.activeProfile ? `¡Muy bien, ${Store.data.activeProfile}!` : "¡Muy bien!";
  $("#festejoFrase").textContent = FRASES_FESTEJO[rint(0, FRASES_FESTEJO.length - 1)];
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

function pintarMenu() {
  Shell.actual = null;
  $("#btnAtras").classList.remove("ver");
  const stage = $("#stage");
  stage.innerHTML = "";
  const bienv = el("div", "", "");
  bienv.id = "bienvenida";
  bienv.innerHTML = `<h1>${D.titulo}</h1><p>Elegí un juego y ganá estrellas ⭐</p>
    <a id="pillLogro" class="${todoCompleto() ? "ver" : ""}" href="${certificadoUrl()}" target="_blank" rel="noopener">🏆 Ver mi diploma</a>`;
  stage.appendChild(bienv);
  const menu = el("div"); menu.id = "menu";
  D.menu.forEach((m, i) => {
    if (!GAMES[m.id]) return;
    if (P.length < (GAMES[m.id].minP || 0)) return;   // tema con pocos personajes
    const st = Store.stars(m.id);
    const c = el("button", "carta");
    // las cartas alternan emoji y personajes del tema para que el menú viva
    const conSprite = i % 3 === 1 && P[(i / 3 | 0) + 1];
    c.innerHTML = `
      <div class="icono">${conSprite ? `<img src="${P[(i / 3 | 0) + 1]}" alt="">` : m.icono}</div>
      <div class="nombre">${m.titulo}</div>
      <div class="mini-est">${st ? "⭐".repeat(st) : "&nbsp;"}</div>
      ${conSprite ? `<div class="chip">${m.icono}</div>` : ""}`;
    c.addEventListener("click", () => { Sfx.pop(); Shell.abrir(m.id); });
    menu.appendChild(c);
  });
  stage.appendChild(menu);
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

  $("#btnAtras").addEventListener("click", () => { Sfx.pop(); pintarMenu(); });
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
    cerrarFestejo(); pintarMenu();
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
GAMES.comprension_lectora = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 8;
    ctx.rondas(rondas);
    let ronda = 0, usados = [], pIdx = -1, qi = 0;
    const nuevoPasaje = () => {
      let disp = COMPRENSION_BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!disp.length) { usados = []; disp = COMPRENSION_BANCO.map((_, i) => i); }
      pIdx = disp[rint(0, disp.length - 1)]; usados.push(pIdx); qi = 0;
    };
    const render = () => {
      ctx.ronda(ronda);
      const pasaje = COMPRENSION_BANCO[pIdx];
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
];
GAMES.conectores = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 10;
    ctx.rondas(rondas);
    let usados = [], ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      let disp = CONECTORES_BANCO.map((_, i) => i).filter((i) => !usados.includes(i));
      if (!disp.length) { usados = []; disp = CONECTORES_BANCO.map((_, i) => i); }
      const idx = disp[rint(0, disp.length - 1)]; usados.push(idx);
      const it = CONECTORES_BANCO[idx];
      ctx.item("conector#" + idx);
      ctx.consigna("Completá: " + it.f);
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
  { num: 1, den: 2, eq: { num: 3, den: 6 }, d1: { num: 2, den: 6 }, d2: { num: 5, den: 6 } },
  { num: 1, den: 4, eq: { num: 2, den: 8 }, d1: { num: 3, den: 8 }, d2: { num: 6, den: 8 } },
  { num: 3, den: 4, eq: { num: 6, den: 8 }, d1: { num: 3, den: 8 }, d2: { num: 1, den: 8 } },
  { num: 1, den: 3, eq: { num: 2, den: 6 }, d1: { num: 1, den: 6 }, d2: { num: 4, den: 6 } },
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
      const cifras = dif <= 0.5 ? 4 : 5;
      const piso = cifras === 4 ? 1000 : 10000;
      const tope = cifras === 4 ? 9999 : 49999;
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

/* ── AGUDO, RECTO U OBTUSO (14-jul-2026, 4° grado NAP Bimestre 4 "Ideas
   web": "transportador interactivo para medir ángulos de rampas de
   skate" — simplificado de medición libre con transportador a
   clasificación sobre un ángulo dibujado con CSS puro (dos líneas desde un
   vértice común, una fija y otra rotada). Grados curados a propósito, no
   al azar — un ángulo de 88° sería ambiguo a simple vista contra uno
   recto real (90°), así que cada categoría usa valores CLARAMENTE
   distinguibles. ── */
const ANGULOS_BANCO = [
  { grados: 30, tipo: "agudo" }, { grados: 45, tipo: "agudo" }, { grados: 60, tipo: "agudo" },
  { grados: 90, tipo: "recto" },
  { grados: 120, tipo: "obtuso" }, { grados: 135, tipo: "obtuso" }, { grados: 150, tipo: "obtuso" },
  // agregados 14-jul-2026 (banco ampliado de 7 a 10).
  { grados: 90, tipo: "recto" }, { grados: 15, tipo: "agudo" }, { grados: 170, tipo: "obtuso" },
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
  { num: 2, den: 3, eq: { num: 4, den: 6 }, d1: { num: 3, den: 6 }, d2: { num: 5, den: 6 } },
  { num: 2, den: 3, eq: { num: 6, den: 9 }, d1: { num: 4, den: 9 }, d2: { num: 8, den: 9 } },
  { num: 1, den: 3, eq: { num: 3, den: 9 }, d1: { num: 2, den: 9 }, d2: { num: 5, den: 9 } },
  { num: 3, den: 5, eq: { num: 6, den: 10 }, d1: { num: 4, den: 10 }, d2: { num: 8, den: 10 } },
  { num: 2, den: 5, eq: { num: 4, den: 10 }, d1: { num: 3, den: 10 }, d2: { num: 7, den: 10 } },
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
  { texto: "4, 6, 8", correcta: 6 },
  { texto: "2, 4, 6, 8", correcta: 5 },
  { texto: "10, 20, 30", correcta: 20 },
  { texto: "3, 5, 7", correcta: 5 },
  { texto: "1, 2, 3, 4, 5", correcta: 3 },
  { texto: "6, 8, 10, 12", correcta: 9 },
  // agregados 14-jul-2026 (banco ampliado de 6 a 10).
  { texto: "5, 10, 15", correcta: 10 },
  { texto: "2, 4, 6", correcta: 4 },
  { texto: "8, 10, 12, 14", correcta: 11 },
  { texto: "9, 12, 15", correcta: 12 },
];
GAMES.estadistica_datos = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      consignaVariada(ctx, ronda, "¿Cuál es el promedio de estos números?", "n");
      ctx.juego.innerHTML = "";
      let disp = ESTADISTICA_BANCO.filter((x) => !usados.includes(x.texto));
      if (!disp.length) { usados = []; disp = ESTADISTICA_BANCO; }
      const item = disp[rint(0, disp.length - 1)];
      usados.push(item.texto);
      const arriba = el("div", "tablero");
      arriba.appendChild(el("div", "spriteQuieto",
        `<span style="font-size:26px;font-family:'Baloo',sans-serif">${item.texto}</span>`));
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
    const ORDEN = ["E", "S", "W", "N"];
    const DELTA = { E: [1, 0], S: [0, 1], W: [-1, 0], N: [0, -1] };
    const DEG = { N: 0, E: 90, S: 180, W: 270 };
    const BIT = { N: 1, S: 2, E: 4, W: 8 };
    let nivel = 0;
    const arrancar = () => {
      ctx.ronda(nivel);
      ctx.consigna("Armá el programa y apretá Jugar para ver el recorrido");
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

      let programa = [];
      let jugando = false;
      const ICONOS = { F: "⬆️", L: "↩️", R: "↪️" };
      const cola = el("div", "programaCola");
      const pintarCola = () => {
        cola.innerHTML = programa.length
          ? programa.map((p) => `<span class="programaChip">${ICONOS[p]}</span>`).join("")
          : `<span class="programaVacio">Tocá los botones para armar tu programa</span>`;
      };
      pintarCola();
      ctx.juego.appendChild(cola);

      const filaInstr = el("div", "filaSprites");
      [["F", "⬆️ Avanzar"], ["L", "↩️ Girar izq."], ["R", "↪️ Girar der."]].forEach(([codigo, label]) => {
        const b = el("button", "spriteBtn", `<span style="font-size:15px;font-family:'Baloo',sans-serif">${label}</span>`);
        b.addEventListener("click", () => {
          if (jugando) return;
          programa.push(codigo);
          pintarCola();
        });
        filaInstr.appendChild(b);
      });
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
        for (const instr of programa) {
          await espera(500);
          if (instr === "L") cur.dir = ORDEN[(ORDEN.indexOf(cur.dir) + 3) % 4];
          else if (instr === "R") cur.dir = ORDEN[(ORDEN.indexOf(cur.dir) + 1) % 4];
          else if (instr === "F") {
            const [dx, dy] = DELTA[cur.dir];
            const nx = cur.x + dx, ny = cur.y + dy;
            if (nx < 0 || ny < 0 || nx >= n || ny >= n || !abierta(cur.x, cur.y, cur.dir)) {
              choco = true;
              ubicar();
              break;
            }
            cur = { x: nx, y: ny, dir: cur.dir };
          }
          ubicar();
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
