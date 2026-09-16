/* VIDEO INTERACTIVO — piloto (15-sep-2026).
 *
 * Pablo: "el video se pausa y hace una pregunta. El chico responde y si no contesta bien le puede
 * dar una pista. O seleccionar objetos según lo que le diga el video… que quede como un video
 * profesional y que el chico se sienta que es parte de él".
 *
 * Lo que hace que se sienta VIDEO y no página con botones:
 *  - la escena nunca está quieta: fondo con zoom lento, los animales nadan o respiran, y Carpi
 *    se mueve cuando habla y "espera" cuando le toca al chico;
 *  - lo que se toca está ADENTRO de la escena (el animal mismo), no en botones grises encima;
 *  - las pistas son de a poco y nunca hay un "perdiste": pista corta → se ilumina lo que tiene que
 *    mirar → Carpi se lo muestra.
 *
 * Todo sale de window.GUION (videos_interactivos/<pieza>/guion.json). Rutas RELATIVAS: la página
 * se sirve siempre bajo /vi/<pieza>/.
 */
(function () {
  "use strict";
  var G = window.GUION;
  var $ = function (id) { return document.getElementById(id); };
  var pantalla = $("pantalla"), bichosEl = $("bichos"), controles = $("controles");
  var carpiEl = $("carpi"), carpiImg = $("carpiImg"), subs = $("subs"), repetirBtn = $("repetir");
  var fondos = [$("fondoA"), $("fondoB")], fondoActivo = -1, escenaActual = null;
  var B = {};                     // id de animal -> botón en la escena
  var registro = [];              // lo que hizo el chico, paso por paso
  var consignaActual = null, bloqueado = false;

  // En un celular VERTICAL la escena mide unos 360x240: los botones de elegir y los grupos no
  // entran adentro sin tapar a los animales. Ahí van debajo de la escena; lo que se toca de la
  // escena —los animales— sigue adentro.
  var vertical = window.matchMedia("(max-width: 760px) and (orientation: portrait)");
  function dondeVanLosBotones() { return vertical.matches ? $("abajo") : controles; }

  // ── sonido: UNA sola voz reutilizada (iOS sólo deja sonar lo que arrancó con un toque) ──────
  var voz = new Audio();
  voz.preload = "auto";
  var actx = null;

  function esperar(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  // TODO lo que se baja lleva la versión de la pieza. Sin esto, el navegador que ya abrió el video
  // sigue usando el reproductor y las voces de la primera vez —se sirven con caché de horas y el
  // nombre nunca cambia—, y una mejora no llega nunca. El 15-sep-2026 eso dejó a Pablo con el
  // reproductor viejo y el guion nuevo, y el video se le trabó en la última pausa.
  function A(nombre) { return window.VI_V ? nombre + "?v=" + window.VI_V : nombre; }

  function hablar(clave) {
    var texto = (G.voces || {})[clave];
    if (!texto) return Promise.resolve();
    subs.textContent = texto;
    carpiEl.classList.add("charla");
    return new Promise(function (resolve) {
      var listo = false;
      function fin() {
        if (listo) return;
        listo = true;
        carpiEl.classList.remove("charla");
        voz.onended = voz.onerror = voz.onloadedmetadata = null;
        resolve();
      }
      // TOPE: por si el audio no carga, para no trabar el video esperando un "ended" que no llega.
      // Calculado por el largo del texto, CORTABA voces de verdad —siete de las dos piezas duraban
      // más que su tope (15-sep-2026)— y seguir de largo con la voz sonando es lo que Pablo oyó
      // como "se juntó": arranca la consigna siguiente encima de la que todavía habla. Ahora el
      // texto sólo da el piso de arranque y, apenas el audio dice cuánto dura, manda esa duración.
      var tope = setTimeout(fin, Math.max(9000, texto.length * 220));
      function porLaDuracion() {
        if (listo || !isFinite(voz.duration) || !voz.duration) return;
        clearTimeout(tope);
        tope = setTimeout(fin, (voz.duration - (voz.currentTime || 0)) * 1000 + 2500);
      }
      voz.onloadedmetadata = porLaDuracion;
      voz.onended = function () { clearTimeout(tope); setTimeout(fin, 400); };
      voz.onerror = function () { clearTimeout(tope); fin(); };
      if (voz.dataset.clave === clave && !voz.paused) { porLaDuracion(); return; }  // ya suena (el arranque)
      voz.dataset.clave = clave;
      voz.src = A("voz_" + clave + ".mp3");
      var p = voz.play();
      if (p && p.catch) p.catch(function () { /* sin permiso de audio: el tope avanza igual */ });
    });
  }

  function sonido(tipo) {
    if (!actx) return;
    var t = actx.currentTime;
    var notas = tipo === "bien" ? [660, 880] : tipo === "fin" ? [523, 659, 784, 1046] : [233, 185];
    notas.forEach(function (f, i) {
      var o = actx.createOscillator(), g = actx.createGain(), t0 = t + i * 0.11;
      o.type = tipo === "mal" ? "triangle" : "sine";
      o.frequency.value = f;
      g.gain.setValueAtTime(0.0001, t0);
      g.gain.exponentialRampToValueAtTime(tipo === "mal" ? 0.10 : 0.16, t0 + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.3);
      o.connect(g); g.connect(actx.destination);
      o.start(t0); o.stop(t0 + 0.34);
    });
  }

  // ── Carpi, la escena y los animales ────────────────────────────────────────────────────
  function pose(nombre) { carpiImg.src = A("carpi_" + nombre + ".webp"); }

  function confeti(cuantos) {
    var caja = $("confeti"), colores = ["#ffd23f", "#2fbf71", "#4cc9f0", "#ff7aa2", "#b388ff"];
    for (var i = 0; i < cuantos; i++) {
      var c = document.createElement("i");
      c.style.left = (Math.random() * 100) + "%";
      c.style.background = colores[i % colores.length];
      c.style.animationDelay = (Math.random() * 0.5) + "s";
      caja.appendChild(c);
      setTimeout(function (el) { el.remove(); }, 2400, c);
    }
  }

  function mostrarEscena(id) {
    if (escenaActual === id) return Promise.resolve();
    escenaActual = id;
    var e = G.escenas[id];
    var siguiente = fondoActivo === 0 ? 1 : 0;
    var img = fondos[siguiente];
    bichosEl.innerHTML = "";
    B = {};
    Object.keys(e.animales || {}).forEach(function (k) {
      var a = e.animales[k];
      var b = document.createElement("button");
      b.type = "button";
      // `estilo: "foto"`: con marco blanco y un poco torcida (`giro`, en grados), como fotos
      // sueltas sobre una mesa. Va con `mov: "ninguno"`, o la animación de respirar pisa el giro.
      // `decorado`: es parte del relato y no una opción —el tambero de «el tambero la ordeña»—.
      // Se ve siempre entero y nunca se toca; sin esto quedaba atenuado como una respuesta
      // descartada y el chico no lo veía cuando la voz lo nombraba.
      b.className = "bicho " + (a.mov || "quieto") + (a.estilo ? " " + a.estilo : "") +
                    (a.decorado ? " decorado" : "");
      if (a.giro) b.style.setProperty("--giro", a.giro + "deg");
      b.dataset.id = k;
      b.style.left = a.x + "%"; b.style.top = a.y + "%"; b.style.width = a.w + "%";
      b.setAttribute("aria-label", k);
      b.disabled = true;
      var im = document.createElement("img");
      im.src = A(a.img + ".webp"); im.alt = "";
      b.appendChild(im);
      bichosEl.appendChild(b);
      B[k] = b;
    });
    return new Promise(function (resolve) {
      // UNA sola vez: con la imagen ya en caché, `complete` da true Y además llega el onload, y la
      // segunda pasada le sacaba el .ver a la imagen que acababa de mostrar — la escena quedaba
      // en celeste liso (se vio en el recorrido automático del 15-sep-2026).
      var hecho = false;
      function cambiar() {
        if (hecho) return;
        hecho = true;
        img.onload = img.onerror = null;
        fondos.forEach(function (f, i) { f.classList.toggle("ver", i === siguiente); });
        fondoActivo = siguiente;
        setTimeout(resolve, 450);
      }
      img.onload = cambiar; img.onerror = cambiar;
      img.src = A(e.fondo + ".webp");
      if (img.complete && img.naturalWidth) cambiar();
      // Los que quedan chicos en la pantalla de verdad —no los que yo creo chicos— agrandan su
      // zona de toque. Se mide después de dibujar, porque depende del tamaño de la pantalla.
      setTimeout(function () {
        Object.keys(B).forEach(function (k) {
          var r = B[k].getBoundingClientRect();
          B[k].classList.toggle("chico", Math.min(r.width, r.height) < 56);
        });
      }, 500);
    });
  }

  // ¿DÓNDE SE APOYA EL TILDE? Pablo, 15-sep-2026: *"el check queda en el aire porque esa parte no
  // tiene imagen"*. Estaba colgado de la esquina de la CAJA del objeto, y los dibujos tienen aire
  // transparente alrededor: en la silla esa esquina no tenía nada, y en la moto —que ocupa sólo la
  // mitad de abajo de su caja— tampoco. Así que se mira el dibujo: se lo dibuja chiquito en un
  // lienzo, se busca dónde empieza y dónde termina de verdad, y se prueban las cuatro esquinas de
  // ESO. Gana la que más dibujo tenga debajo, con preferencia por arriba a la derecha para que
  // todos se parezcan. Se calcula una vez por dibujo.
  var puntos = {};
  function puntoDelTilde(im) {
    var clave = im.getAttribute("src");
    if (puntos[clave]) return puntos[clave];
    var punto = { x: 1, y: 0 };                        // por defecto, la esquina de la caja
    try {
      var nw = im.naturalWidth || 0, nh = im.naturalHeight || 0;
      if (!nw || !nh) return punto;                    // todavía no cargó: no se guarda
      var esc = 64 / Math.max(nw, nh);
      var cw = Math.max(1, Math.round(nw * esc)), ch = Math.max(1, Math.round(nh * esc));
      var lienzo = document.createElement("canvas");
      lienzo.width = cw; lienzo.height = ch;
      var cx = lienzo.getContext("2d");
      cx.drawImage(im, 0, 0, cw, ch);
      var d = cx.getImageData(0, 0, cw, ch).data;
      var lleno = function (x, y) { return d[(y * cw + x) * 4 + 3] > 40; };
      var x0 = cw, y0 = ch, x1 = 0, y1 = 0;
      for (var y = 0; y < ch; y++) {
        for (var x = 0; x < cw; x++) {
          if (!lleno(x, y)) continue;
          if (x < x0) x0 = x;
          if (x > x1) x1 = x;
          if (y < y0) y0 = y;
          if (y > y1) y1 = y;
        }
      }
      if (x1 < x0) return punto;                       // dibujo vacío
      // Cuánto dibujo taparía un tilde centrado en cada punto, de una pasada (suma acumulada).
      var S = new Int32Array((cw + 1) * (ch + 1));
      for (var yy = 0; yy < ch; yy++) {
        for (var xx = 0; xx < cw; xx++) {
          S[(yy + 1) * (cw + 1) + xx + 1] = (lleno(xx, yy) ? 1 : 0) + S[yy * (cw + 1) + xx + 1]
            + S[(yy + 1) * (cw + 1) + xx] - S[yy * (cw + 1) + xx];
        }
      }
      var lado = Math.max(2, Math.round(0.34 * cw));
      var mitad = Math.round(lado / 2);
      var tapa = function (px, py) {
        var a = Math.max(0, px - mitad), b = Math.min(cw, px + mitad);
        var c = Math.max(0, py - mitad), e = Math.min(ch, py + mitad);
        if (b <= a || e <= c) return 0;
        var suma = S[e * (cw + 1) + b] - S[c * (cw + 1) + b] - S[e * (cw + 1) + a] + S[c * (cw + 1) + a];
        return suma / (lado * lado);
      };
      // El tilde va COLGADO DEL BORDE, no en el medio ni en el vacío: se busca el punto del dibujo
      // donde tape más o menos la mitad, tirando hacia arriba a la derecha (que es donde el ojo lo
      // espera, y donde estuvo siempre en las piezas que ya andan).
      var dmin = -y1, dmax = x1, mejor = -1;
      for (var y2 = y0; y2 <= y1; y2++) {
        for (var x2 = x0; x2 <= x1; x2++) {
          if (!lleno(x2, y2)) continue;
          var hacia = dmax > dmin ? (x2 - y2 - dmin) / (dmax - dmin) : 0;
          var puntaje = (1 - Math.abs(tapa(x2, y2) - 0.55) * 2) + 0.6 * hacia;
          if (puntaje > mejor) { mejor = puntaje; punto = { x: x2 / cw, y: y2 / ch }; }
        }
      }
      puntos[clave] = punto;
    } catch (e) { /* sin lienzo: queda en la esquina de la caja */ }
    return punto;
  }

  function marcarBien(b) {
    b.classList.remove("brillo", "elegido");
    b.classList.add("bien");
    // AL FRENTE: el tilde va en el borde del dibujo, y si otro objeto está delante —la silla
    // delante de la mesa— el chico toca bien y no ve nada. Lo encontró Pablo, 15-sep-2026.
    b.style.zIndex = "4";
    if (!b.querySelector(".tilde")) {
      var t = document.createElement("span");
      t.className = "tilde";
      t.textContent = "✓";
      var p = puntoDelTilde(b.querySelector("img"));
      t.style.left = (p.x * 100) + "%";
      t.style.top = (p.y * 100) + "%";
      b.appendChild(t);
    }
  }
  function sacudir(el) { el.classList.remove("mal"); void el.offsetWidth; el.classList.add("mal"); }

  function festejo() {
    pose("festejando");
    carpiEl.classList.add("salto");
    confeti(18);
    sonido("bien");
    var n = 1 + Math.floor(Math.random() * 3);
    return hablar("festejo" + n).then(function () {
      carpiEl.classList.remove("salto");
      pose("hablando");
    });
  }

  function mostrarRepetir(clave) {
    consignaActual = clave;
    repetirBtn.classList.toggle("ver", !!clave);
  }
  repetirBtn.addEventListener("click", function () {
    if (!bloqueado && consignaActual) {
      bloqueado = true;
      hablar(consignaActual).then(function () { bloqueado = false; });
    }
  });

  // Si el chico no hace nada en 15 s, se le repite la consigna (una vez por silencio).
  function vigilarQuietud(clave) {
    var timer = null;
    function armar() {
      clearTimeout(timer);
      timer = setTimeout(function () {
        if (bloqueado) return armar();
        bloqueado = true;
        hablar(clave).then(function () { bloqueado = false; });
      }, 15000);
    }
    armar();
    return { tocar: armar, apagar: function () { clearTimeout(timer); } };
  }

  // ── los pasos ────────────────────────────────────────────────────────────────────────
  function pasoDecir(p) {
    return mostrarEscena(p.escena).then(function () {
      pose(p.pose || "hablando");
      if (p.pose === "festejando") { confeti(60); sonido("fin"); carpiEl.classList.add("salto"); }
      return hablar(p.voz);
    }).then(function () { carpiEl.classList.remove("salto"); });
  }

  function pasoTocar(p, indice) {
    // VARIANTES: si el paso trae varias, se sortea una. Pablo, 15-sep-2026: *"que sea aleatorio el
    // final porque siempre pregunta por la m"*. Un chico que lo repite tiene que encontrarse con
    // otra pregunta, o aprende la respuesta en vez del contenido.
    if (p.variantes && p.variantes.length) {
      var v = p.variantes[Math.floor(Math.random() * p.variantes.length)];
      p = Object.assign({}, p, v);
      window.KYDO_VI_VARIANTE = { paso: indice, correctos: p.correctos };
    }
    return mostrarEscena(p.escena).then(function () {
      var activos = p.solo || Object.keys(B);
      Object.keys(B).forEach(function (k) { B[k].classList.toggle("apagado", activos.indexOf(k) < 0); });
      pose("hablando");
      return hablar(p.consigna);
    }).then(function () {
      pose("esperando");
      mostrarRepetir(p.consigna);
      return new Promise(function (resolve) {
        var encontrados = {}, faltan = p.correctos.length, errores = 0, terminado = false;
        var quieto = vigilarQuietud(p.consigna);
        Object.keys(B).forEach(function (k) {
          var b = B[k];
          if (b.classList.contains("apagado")) return;
          b.disabled = false;
          b.onclick = function () {
            if (bloqueado || terminado) return;
            quieto.tocar();
            if (p.correctos.indexOf(k) >= 0) {
              if (encontrados[k]) return;
              encontrados[k] = true; faltan--;
              marcarBien(b); sonido("bien");
              if (faltan === 0) {
                terminado = true; quieto.apagar(); mostrarRepetir(null);
                Object.keys(B).forEach(function (j) { B[j].disabled = true; B[j].onclick = null; });
                registro.push({ paso: indice, tipo: "tocar", primer_intento: errores === 0, errores: errores });
                bloqueado = true;
                festejo().then(function () { return p.fin ? hablar(p.fin) : null; })
                  .then(function () {
                    bloqueado = false;
                    Object.keys(B).forEach(function (j) {
                      B[j].classList.remove("bien", "apagado");
                      B[j].style.zIndex = "";        // vuelven a su orden de dibujo
                    });
                    bichosEl.querySelectorAll(".tilde").forEach(function (t) { t.remove(); });
                    resolve();
                  });
              }
            } else {
              errores++;
              sacudir(b); sonido("mal");
              var nivel = Math.min(errores, p.pistas.length);
              if (nivel >= 2) {
                p.correctos.forEach(function (c) { if (!encontrados[c] && B[c]) B[c].classList.add("brillo"); });
              }
              bloqueado = true;
              pose("hablando");
              hablar(p.pistas[nivel - 1]).then(function () { bloqueado = false; pose("esperando"); });
            }
          };
        });
      });
    });
  }

  // ORDENAR (16-sep-2026, «Del campo a tu casa»). Pablo: *"sigamos con primero"*. La tarjeta del
  // cuaderno ordena FRASES —«La vaca da leche», «La leche va a la fábrica»— y un chico de 1.º
  // todavía no las lee. Acá se ordenan FOTOS de lo que acaba de ver en el video.
  //  - Cada acierto lleva su NÚMERO, no un tilde: lo que se aprende es el lugar en la secuencia.
  //  - Se equivoca → la escalera de siempre: pista corta, se ilumina LA QUE SIGUE, Carpi la dice.
  //  - Al completar, las fotos se acomodan solas en fila y en orden: es el momento en que el chico
  //    ve el viaje entero de una vez, que es lo que la pausa quería enseñar.
  function marcarNumero(b, n) {
    b.classList.remove("brillo");
    b.classList.add("bien");
    b.style.zIndex = "4";
    var t = document.createElement("span");
    t.className = "tilde numero";
    t.textContent = String(n);
    var pt = puntoDelTilde(b.querySelector("img"));
    t.style.left = (pt.x * 100) + "%";
    t.style.top = (pt.y * 100) + "%";
    b.appendChild(t);
  }

  function pasoOrdenar(p, indice) {
    return mostrarEscena(p.escena).then(function () {
      Object.keys(B).forEach(function (k) { B[k].classList.toggle("apagado", p.orden.indexOf(k) < 0); });
      pose("hablando");
      return hablar(p.consigna);
    }).then(function () {
      pose("esperando");
      mostrarRepetir(p.consigna);
      return new Promise(function (resolve) {
        var siguiente = 0, errores = 0, terminado = false;
        var quieto = vigilarQuietud(p.consigna);
        p.orden.forEach(function (k) {
          var b = B[k];
          if (!b) return;
          b.disabled = false;
          b.onclick = function () {
            if (bloqueado || terminado || b.classList.contains("bien")) return;
            quieto.tocar();
            if (k !== p.orden[siguiente]) {
              errores++;
              sacudir(b); sonido("mal");
              var nivel = Math.min(errores, p.pistas.length);
              if (nivel >= 2 && B[p.orden[siguiente]]) B[p.orden[siguiente]].classList.add("brillo");
              bloqueado = true;
              pose("hablando");
              hablar(p.pistas[nivel - 1]).then(function () { bloqueado = false; pose("esperando"); });
              return;
            }
            siguiente++;
            marcarNumero(b, siguiente);
            sonido("bien");
            Object.keys(B).forEach(function (j) { B[j].classList.remove("brillo"); });
            if (siguiente < p.orden.length) return;
            terminado = true; quieto.apagar(); mostrarRepetir(null);
            p.orden.forEach(function (j) { B[j].disabled = true; B[j].onclick = null; });
            registro.push({ paso: indice, tipo: "ordenar", primer_intento: errores === 0, errores: errores });
            bloqueado = true;
            // EN FILA: cada foto a su lugar, con la transición que ya tienen los objetos
            var n = p.orden.length, ancho = 90 / n;
            p.orden.forEach(function (j, i) {
              var c = B[j];
              c.classList.add("en-fila");              // las fotos se enderezan al acomodarse
              c.style.left = (5 + i * ancho + ancho * 0.06) + "%";
              c.style.top = (p.fila_y != null ? p.fila_y : 34) + "%";
              c.style.width = (ancho * 0.88) + "%";
            });
            festejo().then(function () { return p.fin ? hablar(p.fin) : null; })
              .then(function () {
                bloqueado = false;
                resolve();
              });
          };
        });
      });
    });
  }

  function pasoElegir(p, indice) {
    return mostrarEscena(p.escena).then(function () {
      // !! a propósito: toggle con un segundo argumento que no es booleano ALTERNA la clase
      Object.keys(B).forEach(function (k) { B[k].classList.toggle("apagado", !!(p.foco && k !== p.foco)); });
      if (p.foco && B[p.foco]) B[p.foco].classList.add("brillo");
      pose("hablando");
      return hablar(p.consigna);
    }).then(function () {
      pose("esperando");
      mostrarRepetir(p.consigna);
      return new Promise(function (resolve) {
        var errores = 0, terminado = false;
        var quieto = vigilarQuietud(p.consigna);
        var caja = document.createElement("div");
        caja.className = "opciones";
        function cerrar() {
          terminado = true; quieto.apagar(); mostrarRepetir(null);
          caja.remove();
          Object.keys(B).forEach(function (k) { B[k].classList.remove("brillo", "apagado"); });
          registro.push({ paso: indice, tipo: "elegir", primer_intento: errores === 0, errores: errores });
          resolve();
        }
        p.opciones.forEach(function (o) {
          var btn = document.createElement("button");
          btn.type = "button"; btn.className = "op";
          // CON DIBUJO, para 1.º: un chico que todavía no lee no puede elegir entre tres palabras.
          // El dibujo dice la opción y la voz la nombra en la consigna; la palabra queda abajo
          // para el que ya lee. Sin `icono`, el botón es el de siempre.
          if (o.icono) {
            var ic = document.createElement("img");
            ic.alt = ""; ic.src = A(o.icono + ".webp");
            btn.appendChild(ic);
            btn.classList.add("con_dibujo");
          }
          var palabra = document.createElement("span");
          palabra.textContent = o.texto;
          btn.appendChild(palabra);
          btn.onclick = function () {
            if (bloqueado || terminado) return;
            quieto.tocar();
            if (o.id === p.correcta) {
              btn.classList.add("bien");
              bloqueado = true;
              festejo().then(function () { bloqueado = false; cerrar(); });
            } else {
              errores++;
              sacudir(btn); sonido("mal");
              bloqueado = true;
              pose("hablando");
              var nivel = Math.min(errores, p.pistas.length);
              hablar(p.pistas[nivel - 1]).then(function () {
                bloqueado = false; pose("esperando");
                if (nivel >= p.pistas.length) cerrar();    // tercera pista: Carpi lo explica
              });
            }
          };
          caja.appendChild(btn);
        });
        dondeVanLosBotones().appendChild(caja);
      });
    });
  }

  function pasoClasificar(p, indice) {
    return mostrarEscena(p.escena).then(function () {
      var deLosItems = p.items.map(function (it) { return it.animal; });
      Object.keys(B).forEach(function (k) { B[k].classList.toggle("apagado", deLosItems.indexOf(k) < 0); });
      // Los que se clasifican se ACERCAN al centro de la escena: abajo está la barra de grupos, y
      // el pez nadando al fondo quedaba tapado por ella (recorrido automático, 15-sep-2026).
      Object.keys(p.acomodar || {}).forEach(function (k) {
        var pos = p.acomodar[k], b = B[k];
        if (!b) return;
        b.style.left = pos[0] + "%"; b.style.top = pos[1] + "%"; b.style.width = pos[2] + "%";
      });
      pose("hablando");
      return hablar(p.consigna);
    }).then(function () {
      pose("esperando");
      mostrarRepetir(p.consigna);
      return new Promise(function (resolve) {
        var barra = document.createElement("div"), G2 = {}, elegido = null, pendientes = p.items.length;
        var errores = {}, totalErrores = 0, terminado = false;
        var quieto = vigilarQuietud(p.consigna);
        barra.className = "grupos";
        p.grupos.forEach(function (g) {
          var btn = document.createElement("button");
          btn.type = "button"; btn.className = "grupo";
          btn.innerHTML = '<img alt="" src="' + A(g.icono + '.webp') + '"><span></span><span class="adentro"></span>';
          btn.querySelector("span").textContent = g.texto;
          btn.onclick = function () { soltarEn(g.id, btn); };
          barra.appendChild(btn);
          G2[g.id] = btn;
        });
        dondeVanLosBotones().appendChild(barra);

        p.items.forEach(function (it) {
          var b = B[it.animal];
          if (!b) return;
          b.disabled = false;
          b.onclick = function () {
            if (bloqueado || terminado) return;
            quieto.tocar();
            if (elegido) B[elegido.animal].classList.remove("elegido");
            elegido = it;
            b.classList.add("elegido");
            sonido("bien");
          };
        });

        function ubicar(it) {
          var b = B[it.animal];
          var mini = document.createElement("img");
          mini.src = A(G.escenas[p.escena].animales[it.animal].img + ".webp"); mini.alt = "";
          G2[it.grupo].querySelector(".adentro").appendChild(mini);
          b.classList.remove("elegido", "brillo");
          b.style.opacity = "0"; b.disabled = true; b.onclick = null;
          Object.keys(G2).forEach(function (k) { G2[k].classList.remove("brillo"); });
          pendientes--;
          elegido = null;
          if (pendientes === 0) {
            terminado = true; quieto.apagar(); mostrarRepetir(null);
            registro.push({ paso: indice, tipo: "clasificar", primer_intento: totalErrores === 0, errores: totalErrores });
            bloqueado = true;
            festejo().then(function () {
              bloqueado = false;
              barra.remove();
              var orig = G.escenas[p.escena].animales;
              Object.keys(B).forEach(function (k) {
                B[k].style.opacity = ""; B[k].classList.remove("apagado");
                B[k].style.left = orig[k].x + "%"; B[k].style.top = orig[k].y + "%"; B[k].style.width = orig[k].w + "%";
              });
              resolve();
            });
          }
        }

        function soltarEn(grupoId, btn) {
          if (bloqueado || terminado) return;
          quieto.tocar();
          if (!elegido) {                        // tocó un grupo sin elegir animal: se le muestran
            p.items.forEach(function (it) {
              var b = B[it.animal];
              if (b && !b.disabled) { b.classList.add("brillo"); setTimeout(function () { b.classList.remove("brillo"); }, 1200); }
            });
            return;
          }
          var it = elegido;
          if (it.grupo === grupoId) {
            sonido("bien");
            ubicar(it);
            return;
          }
          errores[it.animal] = (errores[it.animal] || 0) + 1;
          totalErrores++;
          sacudir(btn); sonido("mal");
          var n = errores[it.animal];
          if (n === 1) {
            bloqueado = true; pose("hablando");
            hablar(it.pista).then(function () { bloqueado = false; pose("esperando"); });
          } else if (n === 2) {
            G2[it.grupo].classList.add("brillo");      // segunda: se ilumina el grupo, sin repetir la pista
          } else {
            bloqueado = true; pose("hablando");
            G2[it.grupo].classList.add("brillo");
            hablar(p.va_aca).then(function () { bloqueado = false; pose("esperando"); ubicar(it); });
          }
        }
      });
    });
  }

  var PASOS = { decir: pasoDecir, tocar: pasoTocar, elegir: pasoElegir, clasificar: pasoClasificar,
                ordenar: pasoOrdenar };

  function guardar() {
    var datos = { pieza: G.pieza, saber: G.saber, fecha: new Date().toISOString(), pasos: registro };
    try { localStorage.setItem("kydo:vi:" + G.pieza, JSON.stringify(datos)); } catch (e) { /* sin storage */ }
    try { if (window.parent !== window) window.parent.postMessage({ tipo: "kydo-video-interactivo", datos: datos }, "*"); } catch (e) { /* nada */ }
    window.KYDO_VI_RESULTADO = datos;             // lo lee la prueba automática
  }

  function terminar() {
    guardar();
    subs.textContent = "";
    var telon = $("telon");
    // Sale del guion: escrito acá, las dos piezas terminaban diciendo "No todo lo que nada es pez",
    // que es el cierre del piloto y no tiene nada que ver con la de los sonidos.
    var cierre = G.cierre_pantalla || {};
    telon.querySelector("h1").textContent = cierre.titulo || "¡Lo lograste!";
    $("telonTxt").textContent = cierre.texto || "";
    var btn = $("empezar");
    btn.textContent = "↺ Ver de nuevo";
    btn.onclick = function () { location.reload(); };
    telon.hidden = false;
  }

  function correr(i) {
    if (i >= G.pasos.length) return terminar();
    var p = G.pasos[i];
    // UN RESPIRO ENTRE PAUSAS. Sin él, el cierre de una pausa y la consigna de la siguiente se
    // oyen como una sola frase larga —"como que se juntó con la sss", Pablo, 15-sep-2026—. En un
    // video de verdad hay un corte entre una cosa y la otra; acá el corte es este silencio.
    //
    // Y SI UN PASO SE ROMPE, el video sigue con el que viene. Un paso que falla dejaba la película
    // congelada para siempre —pantalla puesta, Carpi esperando y ni una palabra más—, que es lo
    // peor que puede pasarle a un chico que está jugando solo. Saltear una pausa se nota mucho
    // menos que quedarse clavado, y el error queda en la consola para que lo vea quien revisa.
    var paso;
    try {
      paso = PASOS[p.tipo](p, i);
    } catch (e) {
      paso = Promise.reject(e);
    }
    return paso.catch(function (e) {
      if (window.console) console.error("paso " + i + " (" + p.tipo + "):", e);
      window.KYDO_VI_PASO_ROTO = { paso: i, error: String(e && e.message || e) };
    }).then(function () { return esperar(700); })
      .then(function () { return correr(i + 1); });
  }

  // Precarga liviana: imágenes y voces, así el cambio de escena no se nota.
  function precargar() {
    Object.keys(G.imagenes).forEach(function (k) { var im = new Image(); im.src = A(k + ".webp"); });
    Object.keys(G.voces).forEach(function (k) { var a = new Audio(); a.preload = "auto"; a.src = A("voz_" + k + ".mp3"); });
  }

  pose("hablando");
  precargar();
  mostrarEscena(G.pasos[0].escena);
  $("empezar").addEventListener("click", function () {
    try {
      var AC = window.AudioContext || window.webkitAudioContext;
      if (AC && !actx) actx = new AC();
      if (actx && actx.state === "suspended") actx.resume();
    } catch (e) { actx = null; }
    // El primer audio arranca DENTRO del toque: es lo que destraba el sonido en iPhone.
    var primero = G.pasos[0];
    if (primero.tipo === "decir") {
      voz.dataset.clave = primero.voz;
      voz.src = A("voz_" + primero.voz + ".mp3");
      var pr = voz.play();
      if (pr && pr.catch) pr.catch(function () {});
    }
    $("telon").hidden = true;
    correr(0);
  }, { once: true });
})();
