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
function reproducirConsigna(txt) {
  if (vozActual) { vozActual.pause(); vozActual = null; }
  if (!Sfx.on) return;
  const archivo = AudioManifest[txt];
  if (!archivo) return;
  vozActual = new Audio(archivo);
  vozActual.play().catch(() => {});   // autoplay bloqueado hasta el primer toque: no rompe nada
}

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
        reproducirConsigna(txt);
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
  $("#perfilInput").select();
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
        // escala X e Y por separado: el tablero no siempre renderiza
        // perfectamente cuadrado (el CSS lo cap a un alto máximo), y usar
        // una sola escala (basada solo en el ancho) para las dos corría el
        // cálculo del eje vertical — "el cursor siempre queda más abajo
        // del ícono para que llegue ahí" era exactamente este bug.
        const escX = S / r.width, escY = S / r.height;
        return {
          x: Math.floor(((ev.clientX - r.left) * escX - M) / C),
          y: Math.floor(((ev.clientY - r.top) * escY - M) / C),
        };
      };
      // El BFS (dobla esquinas solo, aunque el mouse apunte lejos en línea
      // general) resultó ser MÁS de lo que hacía falta: "si voy a donde
      // quiero hace todo el camino" — no debe rutear alrededor de una
      // pared, tiene que seguir literalmente la línea del mouse y frenarse
      // ahí si esa línea cruza una pared. Bresenham en cuadrícula: la
      // secuencia de pasos ortogonales (nunca diagonales — los pasillos no
      // conectan en diagonal) que sigue la línea recta real entre dos
      // celdas, tolerando el temblor natural de una mano sin rutear.
      const pasosLinea = (x0, y0, x1, y1) => {
        const pasos = [];
        let x = x0, y = y0;
        const adx = Math.abs(x1 - x0), ady = Math.abs(y1 - y0);
        const sx = x1 > x0 ? 1 : -1, sy = y1 > y0 ? 1 : -1;
        let err = adx - ady;
        while (x !== x1 || y !== y1) {
          const e2 = 2 * err;
          if (e2 > -ady && x !== x1) { err -= ady; x += sx; pasos.push([sx, 0]); }
          else if (e2 < adx && y !== y1) { err += adx; y += sy; pasos.push([0, sy]); }
          else break;
        }
        return pasos;
      };
      let llegando = false;   // guard: dos eventos de puntero casi simultáneos
      // llegando a la meta no deben disparar llegada() dos veces (corrompía
      // "nivel" y rompía el nivel siguiente — bug real visto en pruebas)
      const seguir = (ev) => {
        if (llegando) return;
        // getCoalescedEvents: el navegador agrupa varios movimientos reales
        // del mouse/dedo en un solo evento "pointermove" por rendimiento —
        // sin esto solo veíamos el ÚLTIMO punto de cada tanda, perdiendo
        // pasos intermedios (sentía "poco sensible", y en una esquina
        // rápida el personaje se quedaba atrás del mouse sin reconectar).
        // Con los eventos agrupados seguimos el trazo real punto a punto.
        const eventos = (ev.getCoalescedEvents && ev.getCoalescedEvents().length)
          ? ev.getCoalescedEvents() : [ev];
        for (const e of eventos) {
          const objetivo = celdaDePuntero(e);
          if (objetivo.x < 0 || objetivo.y < 0 || objetivo.x >= n || objetivo.y >= n) continue;
          for (const [dx, dy] of pasosLinea(cur.x, cur.y, objetivo.x, objetivo.y)) {
            if (!paso(dx, dy)) break;
          }
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
        // agarrar = apoyar el dedo cerca del personaje (con margen de una
        // celda: un dedo real nunca apoya pixel-perfecto arriba de él) —
        // un toque cualquiera lejos, en otra parte del tablero, no debería
        // arrastrarlo desde ahí.
        const c = celdaDePuntero(ev);
        if (Math.abs(c.x - cur.x) > 1 || Math.abs(c.y - cur.y) > 1) return;
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
      a.download = (Store.data.activeProfile ? Store.data.activeProfile.toLowerCase() + "-" : "") + "dibujo.png";
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
      // mini: siempre "grande" (más simple); el resto: al azar de verdad —
      // alternar por paridad de ronda hacía que, jugado dos veces, ya se
      // supiera sin mirar que la ronda 2 siempre pedía "el más chico".
      const grande = D.banda === "mini" || rint(0, 1) === 0;
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
      // mini: siempre "más" (más simple); el resto: al azar de verdad — igual
      // bug que en tamano, alternar por paridad se aprendía de memoria.
      const buscaMas = D.banda === "mini" || rint(0, 1) === 0;
      ctx.consigna(buscaMas ? "¿Dónde hay MÁS? Tocá el grupo" : "¿Dónde hay MENOS? Tocá el grupo");
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
      ctx.consigna("Escuchá la palabra y elegí cuántas partes tiene");
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
      ctx.consigna("Escuchá la palabra y tocá las sílabas en orden para armarla");
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
      ctx.consigna("Tocá las letras en orden del abecedario");
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
      ctx.consigna("Tocá dos burbujas que sumen 10");
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
      ctx.consigna("¿Es del campo o de la ciudad?");
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
];
GAMES.planta_fruto = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.consigna("¿Qué fruto da esta planta?");
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

/* ── ¿DE QUÉ MATERIAL ES? — trivia (14-jul-2026, 1° grado NAP Bimestre 4
   "Ideas web": "trivia de materiales — ¿vidrio, madera o metal para una
   ventana?"). Opciones de TEXTO (no emoji — no hay glifo distintivo por
   material sin ambigüedad con los objetos del banco). ── */
const MATERIALES_BANCO = [
  { obj: "🪟", material: "Vidrio" }, { obj: "🍷", material: "Vidrio" },
  { obj: "🪑", material: "Madera" }, { obj: "🚪", material: "Madera" },
  { obj: "🔔", material: "Metal" }, { obj: "🥄", material: "Metal" },
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
      ctx.consigna("¿De qué material es?");
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
      ctx.consigna("¿Es un sustantivo común o propio?");
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
      ctx.consigna("Tocá dos números que sumen el número redondo");
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
      ctx.consigna("¿Qué multiplicación es esta suma?");
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
];
GAMES.conductor_aislante = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.consigna("¿Se calienta rápido o no?");
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
];
GAMES.familia_palabras = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 5;
    ctx.rondas(rondas);
    let usados = [];
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.consigna("¿Qué palabra es de la misma familia?");
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
      ctx.consigna("¿Se ve de día, de noche o en ambos?");
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
      ctx.consigna("Elegí rápido: ¿cuánto es?");
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

GAMES.serie = {
  crear(ctx) {
    const rondas = ctx.cfg.rondas || 6;
    ctx.rondas(rondas);
    let ronda = 0;
    const jugar = () => {
      ctx.ronda(ronda);
      ctx.consigna("¿Qué número falta?");
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
