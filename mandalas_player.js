/* mandalas_player.js — app para pintar las mándalas en el navegador.
   Balde (flood-fill) sobre el line-art B/N; galería de 6; paleta; deshacer;
   guardar PNG; persistencia en localStorage (recargar NO pierde lo pintado). */
(function () {
  "use strict";
  var MANDALAS = window.MANDALAS || [];
  var el = function (t, cls) { var e = document.createElement(t); if (cls) e.className = cls; return e; };
  var $ = function (id) { return document.getElementById(id); };

  // paleta: clásicos infantiles + tonos cálidos + blanco (borrador)
  var COLORES = ["#E25555", "#F2984A", "#F7D154", "#8FC93A", "#3FA796", "#4F86C6",
    "#7C5CBF", "#E36FA0", "#8D6E63", "#3A3330", "#C8674E", "#6B7A4F", "#FFFFFF"];
  var estrellas = function (n) {
    var s = ""; for (var i = 0; i < 6; i++) s += i < n ? "★" : "☆"; return s;
  };
  var claveGuardado = function (idx) { return "mand:" + location.pathname + ":" + idx; };

  // ── galería ──
  function armarGaleria() {
    var grid = $("grid");
    MANDALAS.forEach(function (m, i) {
      var card = el("div", "card");
      var img = el("img"); img.src = m.src; img.alt = "Mándala " + (i + 1); img.loading = "lazy";
      var dif = el("div", "dif"); dif.textContent = (m.cat ? m.cat + " · " : "") + m.dif;
      var st = el("div", "stars"); st.textContent = estrellas(m.stars || (i + 1));
      card.append(img, st, dif);
      card.addEventListener("click", function () { abrirPintar(i); });
      grid.appendChild(card);
    });
  }

  // ── pintar ──
  var cv, cx, historia = [], color = COLORES[0], idxActual = 0, guardarTimer = null;

  function hexRgb(h) {
    h = h.replace("#", "");
    return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
  }

  function persistir() {
    clearTimeout(guardarTimer);
    guardarTimer = setTimeout(function () {
      try { localStorage.setItem(claveGuardado(idxActual), cv.toDataURL("image/png")); }
      catch (e) { /* cuota llena: ignorar */ }
    }, 400);
  }

  // flood-fill: pinta la región contigua clara; los trazos oscuros son frontera
  function balde(x0, y0) {
    var W = cv.width, H = cv.height;
    var img = cx.getImageData(0, 0, W, H), px = img.data;
    var at = function (x, y) { return (y * W + x) * 4; };
    var esLinea = function (i) { return px[i] < 90 && px[i + 1] < 90 && px[i + 2] < 90; };
    var i0 = at(x0, y0);
    if (esLinea(i0)) return false;
    var rgb = hexRgb(color), R = rgb[0], G = rgb[1], B = rgb[2];
    var r0 = px[i0], g0 = px[i0 + 1], b0 = px[i0 + 2];
    if (Math.abs(r0 - R) + Math.abs(g0 - G) + Math.abs(b0 - B) < 12) return false;
    var parecido = function (i) {
      return Math.abs(px[i] - r0) + Math.abs(px[i + 1] - g0) + Math.abs(px[i + 2] - b0) < 110;
    };
    if (historia.length >= 12) historia.shift();
    historia.push(cx.getImageData(0, 0, W, H));
    var pila = [[x0, y0]], visto = new Uint8Array(W * H);
    visto[y0 * W + x0] = 1;
    while (pila.length) {
      var p = pila.pop(), x = p[0], y = p[1], i = at(x, y);
      px[i] = R; px[i + 1] = G; px[i + 2] = B; px[i + 3] = 255;
      var vec = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]];
      for (var v = 0; v < 4; v++) {
        var nx = vec[v][0], ny = vec[v][1];
        if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;
        var k = ny * W + nx; if (visto[k]) continue;
        var ni = k * 4; if (esLinea(ni) || !parecido(ni)) continue;
        visto[k] = 1; pila.push([nx, ny]);
      }
    }
    cx.putImageData(img, 0, 0);
    persistir();
    return true;
  }

  function dibujarBase(cb) {
    var im = new Image();
    im.onload = function () {
      var maxW = Math.min(920, (cv.parentElement.clientWidth || 900) - 24);
      var esc = Math.min(1, maxW / im.width);
      cv.width = Math.round(im.width * esc);
      cv.height = Math.round(im.height * esc);
      cx.fillStyle = "#fff"; cx.fillRect(0, 0, cv.width, cv.height);
      cx.drawImage(im, 0, 0, cv.width, cv.height);
      if (cb) cb();
    };
    im.src = MANDALAS[idxActual].src;
  }

  function abrirPintar(idx) {
    idxActual = idx; historia = [];
    $("gallery").classList.add("off");
    $("paint").classList.add("on");
    dibujarBase(function () {
      // restaurar lo pintado si hay guardado para esta mándala
      var g = null;
      try { g = localStorage.getItem(claveGuardado(idx)); } catch (e) { }
      if (g) { var im = new Image(); im.onload = function () { cx.drawImage(im, 0, 0, cv.width, cv.height); }; im.src = g; }
    });
    window.scrollTo(0, 0);
  }

  function volverGaleria() {
    $("paint").classList.remove("on");
    $("gallery").classList.remove("off");
  }

  function armarPaleta() {
    var pal = $("palette");
    COLORES.forEach(function (c, i) {
      var b = el("button", "swatch" + (c === "#FFFFFF" ? " eraser" : "") + (i === 0 ? " on" : ""));
      b.style.background = c;
      b.addEventListener("click", function () {
        color = c;
        pal.querySelectorAll(".swatch").forEach(function (x) { x.classList.remove("on"); });
        b.classList.add("on");
      });
      pal.appendChild(b);
    });
  }

  function init() {
    var nom = window.NOMBRE || "";
    cv = $("lienzo"); cx = cv.getContext("2d", { willReadFrequently: true });
    armarGaleria();
    armarPaleta();

    cv.addEventListener("pointerdown", function (ev) {
      ev.preventDefault();
      var r = cv.getBoundingClientRect();
      var x = Math.round((ev.clientX - r.left) * (cv.width / r.width));
      var y = Math.round((ev.clientY - r.top) * (cv.height / r.height));
      if (x < 0 || y < 0 || x >= cv.width || y >= cv.height) return;
      balde(x, y);
    });
    $("volver").addEventListener("click", volverGaleria);
    $("undo").addEventListener("click", function () {
      var im = historia.pop(); if (im) { cx.putImageData(im, 0, 0); persistir(); }
    });
    $("limpiar").addEventListener("click", function () {
      historia = [];
      try { localStorage.removeItem(claveGuardado(idxActual)); } catch (e) { }
      dibujarBase();
    });
    $("guardar").addEventListener("click", function () {
      var a = document.createElement("a");
      a.download = (nom ? nom.toLowerCase() + "-" : "") + "mandala-" + (idxActual + 1) + ".png";
      a.href = cv.toDataURL("image/png"); a.click();
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
