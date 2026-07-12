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

let D = null;            // data.json
let P = [];              // personajes (filenames)
const GAMES = {};        // registro de juegos

/* ── persistencia (estrellas + sonido) por token ── */
const Store = {
  key: "ct3d_act::" + location.pathname.replace(/\/$/, ""),
  data: { stars: {}, sound: true },
  load() {
    try { Object.assign(this.data, JSON.parse(localStorage.getItem(this.key) || "{}")); }
    catch (e) {}
  },
  save() { try { localStorage.setItem(this.key, JSON.stringify(this.data)); } catch (e) {} },
  stars(id) { return this.data.stars[id] || 0; },
  setStars(id, n) {
    if (n > this.stars(id)) { this.data.stars[id] = n; this.save(); }
  },
  total() { return Object.values(this.data.stars).reduce((a, b) => a + b, 0); },
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

/* ── shell de juego: consigna + progreso + festejo ── */
const Shell = {
  actual: null, fallos: 0, _rondas: 0,
  abrir(id) {
    const item = D.menu.find((m) => m.id === id);
    if (!item || !GAMES[id]) return;
    this.actual = id; this.fallos = 0;
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
    return {
      cfg: item.cfg || {}, D, P,
      juego: $("#juego"),
      consigna(txt, pistaSrc) {
        $("#consignaTexto").innerHTML = txt;
        const p = $("#consignaPista");
        if (pistaSrc) { p.src = pistaSrc; p.style.display = ""; }
        else p.style.display = "none";
      },
      rondas(n) {
        self._rondas = n;
        const pr = $("#progreso");
        pr.innerHTML = "";
        for (let i = 0; i < n; i++) pr.appendChild(el("i"));
        this.ronda(0);
      },
      ronda(i) {
        document.querySelectorAll("#progreso i").forEach((d, j) => {
          d.className = j < i ? "hecho" : (j === i ? "actual" : "");
        });
      },
      bien(txt) { Sfx.ok(); toast(txt || FRASES_BIEN[rint(0, FRASES_BIEN.length - 1)]); },
      casi() { self.fallos++; Sfx.casi(); },
      win(estrellas) {
        const e = estrellas !== undefined ? estrellas
          : (self.fallos === 0 ? 3 : (self.fallos <= 2 ? 2 : 1));
        Store.setStars(self.actual, e);
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
  $("#festejoTitulo").textContent = D.nombre ? `¡Muy bien, ${D.nombre}!` : "¡Muy bien!";
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

/* ── menú principal ── */
function pintarHeader() {
  $("#totalEstrellas").textContent = Store.total();
  $("#hdrNombre").textContent = D.nombre ? `¡Hola, ${D.nombre}!` : "¡Hola!";
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
  bienv.innerHTML = `<h1>${D.titulo}</h1><p>Elegí un juego y ganá estrellas ⭐</p>`;
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
  // precarga de personajes (los juegos los usan al instante)
  await Promise.all(P.map((src) => new Promise((res) => {
    const im = new Image(); im.onload = im.onerror = res; im.src = src;
  })));
  pintarHeader();
  pintarMenu();
  $("#cargando").remove();

  $("#btnAtras").addEventListener("click", () => { Sfx.pop(); pintarMenu(); });
  $("#btnSonido").addEventListener("click", () => {
    Sfx.on = !Sfx.on;
    Store.data.sound = Sfx.on; Store.save();
    $("#btnSonido").textContent = Sfx.on ? "🔊" : "🔇";
    if (Sfx.on) Sfx.pop();
  });
  $("#btnSeguir").addEventListener("click", () => { cerrarFestejo(); pintarMenu(); });
  $("#btnOtraVez").addEventListener("click", () => {
    const id = Shell.actual;
    cerrarFestejo();
    if (id) Shell.abrir(id);
  });
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
        const esc = S / r.width;
        return {
          x: Math.floor(((ev.clientX - r.left) * esc - M) / C),
          y: Math.floor(((ev.clientY - r.top) * esc - M) / C),
        };
      };
      // Seguimiento DIRECTO, celda por celda — pedido de Pablo: nada de
      // auto-resolver ni de rutear solo alrededor de las paredes. El dedo
      // tiene que recorrer de verdad el pasillo. Reporte real (Pablo, tramo
      // vertical largo): con un arrastre rápido el evento de puntero puede
      // "saltar" varias celdas de un salto (el muestreo no da abasto) — con
      // un solo paso por evento el personaje se quedaba atrás sin que se
      // notara, y al llegar abajo y doblar parecía que "una pared" lo
      // frenaba cuando en realidad todavía no había bajado del todo. Fix:
      // si el dedo saltó de largo pero en LÍNEA RECTA (mismo pasillo, sin
      // doblar), alcanza todo ese tramo de un saque — pero se frena en la
      // primera pared, y si el salto no es en línea recta (dx Y dy != 0,
      // cortaría una esquina) no se mueve nada: sigue exigiendo que el
      // dedo trace la esquina de verdad, no rutea solo.
      const seguir = (ev) => {
        const objetivo = celdaDePuntero(ev);
        const dx = objetivo.x - cur.x, dy = objetivo.y - cur.y;
        if (dx !== 0 && dy !== 0) return;   // no es un tramo recto: no corta esquinas
        const sx = Math.sign(dx), sy = Math.sign(dy);
        for (let i = 0, pasos = Math.abs(dx) + Math.abs(dy); i < pasos; i++) {
          if (!paso(sx, sy)) break;
        }
        if (cur.x === n - 1 && cur.y === n - 1) llegada();
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
        // agarrar = apoyar el dedo justo sobre el personaje (si no, un toque
        // cualquiera en el tablero no debería arrastrarlo desde ahí)
        const c = celdaDePuntero(ev);
        if (c.x !== cur.x || c.y !== cur.y) return;
        arrastrando = true; svg.setPointerCapture(ev.pointerId);
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
        // escala el canvas; acá el tope exacto midiendo la botonera real)
        requestAnimationFrame(() => {
          const libre = innerHeight - wrap.getBoundingClientRect().top
            - paleta.offsetHeight - botones.offsetHeight - 42;
          cv.style.maxHeight = Math.max(210, libre) + "px";
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
      a.download = (D.nombre ? D.nombre.toLowerCase() + "-" : "") + "dibujo.png";
      a.href = cv.toDataURL("image/png");
      a.click();
      toast("¡Guardado! 🖼️");
    });
    bListo.addEventListener("click", () => ctx.win(3));
  },
};

/* ── ¿CUÁNTOS HAY? — contá tocando: cada toque numera y suena (do-re-mi) ── */
GAMES.contar = {
  crear(ctx) {
    const max = ctx.cfg.max || 5, rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    // cantidades que suben de a poco (andamiaje)
    const cantidades = [];
    for (let i = 0; i < rondas; i++)
      cantidades.push(Math.min(max, Math.max(1, Math.round(1 + (max - 1) * i / (rondas - 1 || 1)))));
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.juego.innerHTML = "";
      const nBichos = cantidades[ronda];
      const objetivo = P[rint(0, Math.min(5, P.length - 1))];
      ctx.consigna(`¿Cuántos hay? ¡Tocalos para contarlos!`, objetivo);
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
      ctx.consigna("Uní los puntos en orden: 1, 2, 3…");
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
      ctx.consigna("Llevá a cada amigo hasta su sombra");
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
      ctx.consigna("¿Qué sigue? Seguí el patrón");
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
      ctx.consigna("Tocá el que es DISTINTO");
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
GAMES.tamano = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const grande = ronda % 2 === 0 || D.banda === "mini";  // mini: siempre "grande"
      ctx.consigna(grande ? "Tocá el MÁS GRANDE" : "Ahora tocá el MÁS CHICO");
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
GAMES.mas_menos = {
  crear(ctx) {
    const max = ctx.cfg.max || 6, rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      const buscaMas = D.banda === "mini" ? true : ronda % 2 === 0;
      ctx.consigna(buscaMas ? "¿Dónde hay MÁS? Tocá el grupo" : "¿Dónde hay MENOS? Tocá el grupo");
      ctx.juego.innerHTML = "";
      let a = rint(1, max), b = rint(1, max);
      while (a === b) b = rint(1, max);
      const [s1, s2] = sample(P, 2);
      const cont = el("div"); cont.id = "dosGrupos";
      let resuelto = false;
      [[a, s1], [b, s2]].forEach(([nCant, src], idx) => {
        const g = el("button", "grupo");
        for (let i = 0; i < nCant; i++) g.appendChild(el("img")).src = src;
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
          }
        });
        cont.appendChild(g);
      });
      ctx.juego.appendChild(cont);
    };
    jugar();
  },
};

/* ── LA SERIE — completá el número que falta (+1 o +2) ── */
GAMES.serie = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.consigna("¿Qué número falta?");
      ctx.juego.innerHTML = "";
      const paso = ronda < rondas / 2 ? 1 : 2;         // sube la dificultad
      const desde = rint(1, paso === 1 ? 12 : 8);
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
const SIMON_COLORES = [
  { c: "#E25555", nota: 392 }, { c: "#4F86C6", nota: 330 }, { c: "#F2C94C", nota: 262 },
  { c: "#4CAF7D", nota: 440 }, { c: "#9B6BD6", nota: 494 },
];
GAMES.simon = {
  crear(ctx) {
    const nColores = Math.min(ctx.cfg.colores || 4, SIMON_COLORES.length);
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
      ctx.consigna("Mirá y escuchá…");
      await espera(400);
      for (let i = 0; i < seq.length; i++) { flash(seq[i], 380); await espera(480); }
      reproduciendo = false;
      entrada = [];
      ctx.consigna("Ahora repetí vos, tocando en el mismo orden");
    };
    const construir = () => {
      ctx.juego.innerHTML = "";
      const fila = el("div", "filaSprites");
      fila.style.maxWidth = "480px";
      const TAM = nColores > 4 ? 84 : 100;
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
      ctx.consigna("¿A qué canasta va?");
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
      ctx.consigna("Mirá bien quiénes están…");
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
      ctx.consigna("¿Quién se escondió?");
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
          ctx.consigna("Buscá a:", objetivo);
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
