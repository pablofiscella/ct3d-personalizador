/* ══ Player del rompecabezas interactivo — Casatridimensional ══
   Un solo archivo, vanilla JS, rutas RELATIVAS (vive bajo /armar/<token>/).
   Contrato: data.json trae paleta + puzzles (imágenes del tema) + bordes de
   piezas YA GENERADOS en Python (la misma receta de knobs Bézier del
   rompecabezas imprimible) — acá solo se dibujan y se arrastran.
   Principios (los del cuaderno interactivo): targets ≥76px, drag con imán,
   cero fail states (una pieza mal soltada queda donde está, nunca castiga),
   feedback inmediato, festejo corto, sin timers. */
"use strict";

const $ = (s) => document.querySelector(s);
const el = (tag, cls, html) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html !== undefined) e.innerHTML = html;
  return e;
};
const rint = (a, b) => a + Math.floor(Math.random() * (b - a + 1));

let D = null;              // data.json
const ESC = 0.9;           // escala del knob (idéntica a rompecabezas._dibujar_cortes)

/* ── persistencia (estrellas + progreso + sonido) por token ── */
const Store = {
  key: "ct3d_rompe::" + location.pathname.replace(/\/$/, ""),
  data: { stars: {}, prog: {}, sound: true },
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
  pop() { this._nota(900 + Math.random() * 300, 0, 0.07, "square", 0.06); },
  tick(i) { this._nota(523 * Math.pow(2, (i % 8) / 12 * 2), 0, 0.12, "triangle", 0.13); },
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

const FRASES_FESTEJO = [
  "¡Pieza por pieza lo lograste!", "¡Qué bien miraste cada forma!",
  "¡Lo armaste vos!", "¡Sos de no rendirte!", "¡Cuánta paciencia le pusiste!",
];

function toast(txt) {
  const t = $("#toast");
  t.textContent = txt;
  t.classList.remove("ver");
  void t.offsetWidth;
  t.classList.add("ver");
}

function festejar(estrellas, alCerrar) {
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
  Festejo.alCerrar = alCerrar || null;
}
const Festejo = { alCerrar: null };
function cerrarFestejo() { $("#festejo").classList.remove("ver"); }

/* ── pantallas ── */
function pintarHeader() {
  $("#totalEstrellas").textContent = Store.total();
  $("#hdrNombre").textContent = D.nombre ? `¡Hola, ${D.nombre}!` : "¡Hola!";
  $("#hdrSub").textContent = `${D.tema_nombre} · Casatridimensional`;
  const av = $("#avatar"), mf = $("#mascoFestejo");
  if (D.masco) {
    av.innerHTML = ""; av.appendChild(el("img")).src = D.masco;
    mf.innerHTML = ""; const m = el("img", "masco"); m.src = D.masco; mf.appendChild(m);
  } else {
    av.textContent = "🧩";
    mf.innerHTML = ""; mf.appendChild(el("div", "mascoEmoji", "🧩"));
  }
}

function estrellitas(n) {
  return n ? "⭐".repeat(n) : "";
}

function starsPuzzle(pi) {
  return D.targets.reduce((a, t) => a + Store.stars(pi + "|" + t), 0);
}

function pintarMenu() {
  Juego.cerrar();
  $("#btnAtras").classList.remove("ver");
  const stage = $("#stage");
  stage.className = ""; stage.innerHTML = "";
  const bienv = el("div", "", `<h1>${D.titulo}</h1><p>Elegí una foto, armala y ganá estrellas ⭐</p>`);
  bienv.id = "bienvenida";
  stage.appendChild(bienv);
  const menu = el("div"); menu.id = "menu";
  D.puzzles.forEach((p, i) => {
    const c = el("button", "carta", `
      <div class="foto"><img src="${p.thumb}" alt="" loading="lazy"></div>
      <div class="nombre">Rompecabezas ${i + 1}</div>
      <div class="mini-est">${estrellitas(Math.min(3, Math.round(starsPuzzle(i) / D.targets.length)))}</div>`);
    c.addEventListener("click", () => { Sfx.pop(); pintarNiveles(i); });
    menu.appendChild(c);
  });
  stage.appendChild(menu);
  Pantalla.actual = "menu";
}

function pintarNiveles(pi) {
  Juego.cerrar();
  $("#btnAtras").classList.add("ver");
  const stage = $("#stage");
  stage.className = ""; stage.innerHTML = "";
  const p = D.puzzles[pi];
  const cont = el("div"); cont.id = "niveles";
  cont.appendChild(el("div", "foto", `<img src="${p.thumb}" alt="">`));
  cont.appendChild(el("h2", "", "¿De cuántas piezas lo armás?"));
  const btns = el("div"); btns.id = "nivelBtns";
  D.targets.forEach((t) => {
    const b = el("button", "nivelBtn", `
      <div class="n">${t}</div><div class="t">piezas</div>
      <div class="est">${estrellitas(Store.stars(pi + "|" + t))}</div>`);
    b.addEventListener("click", () => { Sfx.pop(); jugar(pi, t); });
    btns.appendChild(b);
  });
  cont.appendChild(btns);
  stage.appendChild(cont);
  Pantalla.actual = "niveles";
  Pantalla.puzzle = pi;
}

const Pantalla = { actual: "menu", puzzle: 0 };

/* ── el juego ─────────────────────────────────────────────────────────────
   Todo en UN canvas: tablero (con fantasma de la imagen + contornos de las
   piezas, como la página-bandeja del imprimible) + piezas sueltas alrededor.
   Cada pieza es un Path2D recortado de la imagen; el drag es pointer events
   y al soltar cerca de su lugar, imán + POP. */
const Juego = {
  activo: false, pi: 0, target: 0,
  img: null, puz: null, cols: 0, filas: 0, bordes: null,
  piezas: [], z: [],            // z = orden de dibujado (índices de piezas sueltas)
  cv: null, cx: null, cssW: 0, cssH: 0,
  bx: 0, by: 0, bw: 0, bh: 0, s: 1,
  drag: null, espiar: false, listo: false,

  abrir(pi, target) {
    this.cerrar();
    this.activo = true; this.listo = false;
    this.pi = pi; this.target = target;
    this.puz = D.puzzles[pi];
    const [c, f] = this.puz.grillas[String(target)].split("x").map(Number);
    this.cols = c; this.filas = f;
    this.bordes = D.bordes[this.puz.grillas[String(target)]];

    $("#btnAtras").classList.add("ver");
    const stage = $("#stage");
    stage.className = "jugando"; stage.innerHTML = "";
    const j = el("div"); j.id = "juego";
    j.innerHTML = `
      <canvas id="lienzo"></canvas>
      <div id="barraJuego">
        <div class="estado"><span id="puestas">0</span> / ${target} piezas</div>
        <button class="btn suave" id="btnEspiar">🖼️ Espiar</button>
        <button class="btn suave" id="btnMezclar">🔀 Mezclar</button>
      </div>`;
    stage.appendChild(j);
    Pantalla.actual = "juego";
    Pantalla.puzzle = pi;

    this.cv = $("#lienzo"); this.cx = this.cv.getContext("2d");
    this.cv.addEventListener("pointerdown", (e) => this.abajo(e));
    this.cv.addEventListener("pointermove", (e) => this.mueve(e));
    this.cv.addEventListener("pointerup", (e) => this.suelta(e));
    this.cv.addEventListener("pointercancel", (e) => this.suelta(e));
    const esp = $("#btnEspiar");
    const espiarOn = (e) => { e.preventDefault(); this.espiar = true; this.dibujar(); };
    const espiarOff = () => { if (this.espiar) { this.espiar = false; this.dibujar(); } };
    esp.addEventListener("pointerdown", espiarOn);
    esp.addEventListener("pointerup", espiarOff);
    esp.addEventListener("pointerleave", espiarOff);
    $("#btnMezclar").addEventListener("click", () => { Sfx.pop(); this.esparcir(); this.dibujar(); });

    this.img = new Image();
    this.img.onload = () => {
      this.armar();
      $("#cargando").style.display = "none";
      this.dibujar();
    };
    this.img.src = this.puz.img;
  },

  cerrar() {
    this.activo = false; this.drag = null; this.piezas = []; this.z = [];
  },

  /* geometría: polilínea del contorno de la pieza (ci,fi) en px de imagen.
     Mapeo IDÉNTICO a rompecabezas._dibujar_cortes (px a lo largo del borde,
     py perpendicular escalado por la celda × ESC). */
  poliPieza(ci, fi) {
    const cw = this.puz.w / this.cols, ch = this.puz.h / this.filas;
    const H = this.bordes.h, V = this.bordes.v;
    const pts = [];
    if (fi === 0) { pts.push([ci * cw, 0], [(ci + 1) * cw, 0]); }
    else for (const [px, py] of H[fi - 1][ci]) pts.push([ci * cw + px * cw, fi * ch + py * ch * ESC]);
    if (ci === this.cols - 1) { pts.push([this.puz.w, (fi + 1) * ch]); }
    else for (const [px, py] of V[ci][fi]) pts.push([(ci + 1) * cw + py * cw * ESC, fi * ch + px * ch]);
    if (fi === this.filas - 1) { pts.push([ci * cw, this.puz.h]); }
    else { const e = H[fi][ci]; for (let k = e.length - 1; k >= 0; k--) { const [px, py] = e[k]; pts.push([ci * cw + px * cw, (fi + 1) * ch + py * ch * ESC]); } }
    if (ci !== 0) { const e = V[ci - 1][fi]; for (let k = e.length - 1; k >= 0; k--) { const [px, py] = e[k]; pts.push([ci * cw + py * cw * ESC, fi * ch + px * ch]); } }
    return pts;
  },

  armar() {
    // layout del canvas: tablero + zona de piezas (abajo o al costado)
    const contW = $("#juego").clientWidth;
    const top = this.cv.getBoundingClientRect().top;
    const contH = Math.max(360, innerHeight - top - 86);
    this.cssW = contW; this.cssH = contH;
    const dpr = Math.min(2.5, devicePixelRatio || 1);
    this.cv.width = Math.round(contW * dpr); this.cv.height = Math.round(contH * dpr);
    this.cv.style.height = contH + "px";
    this.cx.setTransform(dpr, 0, 0, dpr, 0, 0);

    const lado = contW / contH > 1.15;   // apaisado: piezas a la derecha
    const zona = lado ? { x: 8, y: 8, w: contW * 0.62 - 16, h: contH - 16 }
                      : { x: 8, y: 8, w: contW - 16, h: contH * 0.62 - 16 };
    this.s = Math.min(zona.w / this.puz.w, zona.h / this.puz.h);
    this.bw = this.puz.w * this.s; this.bh = this.puz.h * this.s;
    this.bx = zona.x + (zona.w - this.bw) / 2;
    this.by = zona.y + (zona.h - this.bh) / 2;
    this.bandeja = lado
      ? { x: contW * 0.62, y: 8, w: contW * 0.38 - 12, h: contH - 16 }
      : { x: 8, y: contH * 0.62, w: contW - 16, h: contH * 0.38 - 12 };

    const puestas = new Set((Store.data.prog[this.pk()] || []));
    const armadas = this.piezas.length > 0;
    const previas = this.piezas;
    this.piezas = []; this.z = [];
    for (let fi = 0; fi < this.filas; fi++)
      for (let ci = 0; ci < this.cols; ci++) {
        const i = fi * this.cols + ci;
        const poly = this.poliPieza(ci, fi).map(([x, y]) => [this.bx + x * this.s, this.by + y * this.s]);
        const path = new Path2D();
        poly.forEach(([x, y], k) => k ? path.lineTo(x, y) : path.moveTo(x, y));
        path.closePath();
        const cx = this.bx + (ci + 0.5) * (this.bw / this.cols);
        const cy = this.by + (fi + 0.5) * (this.bh / this.filas);
        const p = { i, ci, fi, poly, path, cx, cy, dx: 0, dy: 0,
                    placed: armadas ? previas[i].placed : puestas.has(i),
                    fx: armadas ? previas[i].fx : Math.random(),
                    fy: armadas ? previas[i].fy : Math.random() };
        this.piezas.push(p);
      }
    for (const p of this.piezas)
      if (!p.placed) { if (armadas) this.posiciona(p); this.z.push(p.i); }
    if (!armadas) this.esparcir();
    this.actualizaEstado();
  },

  pk() { return this.pi + "|" + this.target; },

  posiciona(p) {
    // ubica la pieza suelta según su fracción guardada dentro de la bandeja
    const mw = (this.bw / this.cols) * 0.55, mh = (this.bh / this.filas) * 0.55;
    const tx = this.bandeja.x + mw + p.fx * Math.max(1, this.bandeja.w - 2 * mw);
    const ty = this.bandeja.y + mh + p.fy * Math.max(1, this.bandeja.h - 2 * mh);
    p.dx = tx - p.cx; p.dy = ty - p.cy;
  },

  esparcir() {
    // reparto en grilla mezclada + jitter: cubre toda la bandeja sin que las
    // piezas caigan todas apiladas en el medio (puro random las amontonaba)
    const sueltas = this.piezas.filter((p) => !p.placed);
    if (!sueltas.length) return;
    const ct = Math.max(1, Math.round(Math.sqrt(
      sueltas.length * this.bandeja.w / Math.max(1, this.bandeja.h))));
    const ft = Math.ceil(sueltas.length / ct);
    const slots = [...Array(ct * ft).keys()];
    for (let i = slots.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [slots[i], slots[j]] = [slots[j], slots[i]];
    }
    sueltas.forEach((p, k) => {
      p.fx = (slots[k] % ct + 0.5 + (Math.random() - 0.5) * 0.6) / ct;
      p.fy = (Math.floor(slots[k] / ct) + 0.5 + (Math.random() - 0.5) * 0.6) / ft;
      this.posiciona(p);
    });
  },

  actualizaEstado() {
    const n = this.piezas.filter((p) => p.placed).length;
    const e = $("#puestas");
    if (e) e.textContent = n;
  },

  dibujar() {
    if (!this.activo || !this.piezas.length) return;
    const c = this.cx;
    c.clearRect(0, 0, this.cssW, this.cssH);
    // tablero (card + fantasma + contornos = la "bandeja" del imprimible)
    c.save();
    c.fillStyle = D.paleta.card;
    const r = 18, x = this.bx - 12, y = this.by - 12, w = this.bw + 24, h = this.bh + 24;
    c.beginPath();
    if (c.roundRect) c.roundRect(x, y, w, h, r); else c.rect(x, y, w, h);
    c.fill();
    c.strokeStyle = D.paleta.soft; c.lineWidth = 3; c.stroke();
    c.restore();
    const completo = this.piezas.every((p) => p.placed);
    c.save();
    c.globalAlpha = this.espiar ? 0.85 : (completo ? 0 : 0.16);
    c.drawImage(this.img, this.bx, this.by, this.bw, this.bh);
    c.restore();
    if (!completo) {
      c.save();
      c.strokeStyle = D.paleta.ink; c.globalAlpha = 0.18; c.lineWidth = 1.5;
      for (const p of this.piezas) if (!p.placed) c.stroke(p.path);
      c.restore();
    }
    // piezas puestas (encajadas, sin offset)
    for (const p of this.piezas) if (p.placed) this.dibujarPieza(p, false);
    // piezas sueltas en orden z (la arrastrada, última)
    for (const i of this.z) {
      const p = this.piezas[i];
      if (!p.placed) this.dibujarPieza(p, this.drag && this.drag.p === p);
    }
  },

  dibujarPieza(p, alzada) {
    const c = this.cx;
    c.save();
    c.translate(p.dx, p.dy);
    if (alzada) {
      c.save();
      c.shadowColor = "rgba(0,0,0,.32)"; c.shadowBlur = 16; c.shadowOffsetY = 7;
      c.fillStyle = "#fff"; c.fill(p.path);
      c.restore();
    }
    c.save();
    c.clip(p.path);
    c.drawImage(this.img, this.bx, this.by, this.bw, this.bh);
    c.restore();
    if (!p.placed) {
      c.strokeStyle = alzada ? "#FFFFFF" : "rgba(255,255,255,.75)";
      c.lineWidth = alzada ? 3 : 2;
      c.stroke(p.path);
    }
    c.restore();
  },

  xy(e) {
    const r = this.cv.getBoundingClientRect();
    return [e.clientX - r.left, e.clientY - r.top];
  },

  abajo(e) {
    if (!this.listoParaJugar()) return;
    const [x, y] = this.xy(e);
    for (let k = this.z.length - 1; k >= 0; k--) {
      const p = this.piezas[this.z[k]];
      if (p.placed) continue;
      if (dentro(p.poly, x - p.dx, y - p.dy)) {
        this.drag = { p, ox: x - p.dx, oy: y - p.dy };
        this.z.splice(k, 1); this.z.push(p.i);   // al frente
        this.cv.setPointerCapture(e.pointerId);
        Sfx.pop();
        this.dibujar();
        return;
      }
    }
  },

  mueve(e) {
    if (!this.drag) return;
    const [x, y] = this.xy(e);
    const p = this.drag.p;
    p.dx = x - this.drag.ox; p.dy = y - this.drag.oy;
    this.dibujar();
  },

  suelta(e) {
    if (!this.drag) return;
    const p = this.drag.p;
    this.drag = null;
    const cwCss = this.bw / this.cols, chCss = this.bh / this.filas;
    const iman = Math.max(26, 0.32 * Math.min(cwCss, chCss));
    if (Math.hypot(p.dx, p.dy) < iman) {
      p.dx = 0; p.dy = 0; p.placed = true;
      this.z = this.z.filter((i) => i !== p.i);
      Sfx.ok();
      const puestos = this.piezas.filter((q) => q.placed).map((q) => q.i);
      Store.data.prog[this.pk()] = puestos; Store.save();
      this.actualizaEstado();
      if (this.piezas.every((q) => q.placed)) return this.gano();
    } else {
      // cero fail state: queda donde la soltó (clampeada adentro del canvas)
      const mx = this.bw / this.cols / 2, my = this.bh / this.filas / 2;
      p.dx = Math.min(Math.max(p.dx, -p.cx + mx), this.cssW - p.cx - mx);
      p.dy = Math.min(Math.max(p.dy, -p.cy + my), this.cssH - p.cy - my);
      p.fx = Math.min(1, Math.max(0, (p.cx + p.dx - this.bandeja.x) / Math.max(1, this.bandeja.w)));
      p.fy = Math.min(1, Math.max(0, (p.cy + p.dy - this.bandeja.y) / Math.max(1, this.bandeja.h)));
    }
    this.dibujar();
  },

  listoParaJugar() { return this.activo && this.piezas.length && this.img.complete; },

  gano() {
    delete Store.data.prog[this.pk()]; Store.save();
    Store.setStars(this.pk(), 3);
    pintarHeader();
    this.dibujar();                       // la imagen completa, sin cortes
    const pi = this.pi, target = this.target;
    setTimeout(() => festejar(3, () => {
      const sig = D.targets[D.targets.indexOf(target) + 1];
      if (sig) jugar(pi, sig);
      else pintarMenu();
    }), 650);
  },

  redimensionar() {
    if (!this.activo || !this.piezas.length) return;
    this.armar();
    this.dibujar();
  },
};

function dentro(poly, x, y) {
  let c = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
    if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c;
  }
  return c;
}

function jugar(pi, target) {
  cerrarFestejo();
  Juego.abrir(pi, target);
}

/* ── arranque ── */
async function boot() {
  Store.load();
  Sfx.on = Store.data.sound !== false;
  $("#btnSonido").textContent = Sfx.on ? "🔊" : "🔇";
  try {
    D = await (await fetch("data.json")).json();
  } catch (e) {
    $("#cargando").innerHTML = "<div class='fx' style='font-size:22px'>No pudimos cargar 😕<br>Probá recargar la página.</div>";
    return;
  }
  const root = document.documentElement.style;
  for (const [k, v] of Object.entries({ bg: "--bg", card: "--card", ink: "--ink",
    ac: "--ac", ac2: "--ac2", soft: "--soft", star: "--star" }))
    root.setProperty(v, D.paleta[k]);
  Confeti.init();
  pintarHeader();
  pintarMenu();
  $("#cargando").style.display = "none";

  $("#btnAtras").addEventListener("click", () => {
    Sfx.pop();
    if (Pantalla.actual === "juego") pintarNiveles(Pantalla.puzzle);
    else pintarMenu();
  });
  $("#btnSonido").addEventListener("click", () => {
    Sfx.on = !Sfx.on;
    Store.data.sound = Sfx.on; Store.save();
    $("#btnSonido").textContent = Sfx.on ? "🔊" : "🔇";
    if (Sfx.on) Sfx.ok();
  });
  $("#btnOtraVez").addEventListener("click", () => {
    cerrarFestejo();
    delete Store.data.prog[Juego.pk()]; Store.save();
    jugar(Juego.pi, Juego.target);
  });
  $("#btnSeguir").addEventListener("click", () => {
    cerrarFestejo();
    if (Festejo.alCerrar) Festejo.alCerrar();
  });
  addEventListener("resize", () => Juego.redimensionar());
}

boot();
