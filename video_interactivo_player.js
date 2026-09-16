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
        voz.onended = voz.onerror = null;
        resolve();
      }
      // tope por si el audio no carga: nunca se traba el video esperando un "ended" que no llega
      var tope = setTimeout(fin, Math.max(5000, texto.length * 110));
      voz.onended = function () { clearTimeout(tope); setTimeout(fin, 250); };
      voz.onerror = function () { clearTimeout(tope); fin(); };
      if (voz.dataset.clave === clave && !voz.paused) return;   // ya está sonando (el arranque)
      voz.dataset.clave = clave;
      voz.src = "voz_" + clave + ".mp3";
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
  function pose(nombre) { carpiImg.src = "carpi_" + nombre + ".webp"; }

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
      b.className = "bicho " + (a.mov || "quieto");
      b.dataset.id = k;
      b.style.left = a.x + "%"; b.style.top = a.y + "%"; b.style.width = a.w + "%";
      b.setAttribute("aria-label", k);
      b.disabled = true;
      var im = document.createElement("img");
      im.src = a.img + ".webp"; im.alt = "";
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
      img.src = e.fondo + ".webp";
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

  function marcarBien(b) {
    b.classList.remove("brillo", "elegido");
    b.classList.add("bien");
    // AL FRENTE: el tilde va en la esquina del dibujo, y si otro objeto está delante —la silla
    // delante de la mesa— el chico toca bien y no ve nada. Lo encontró Pablo, 15-sep-2026.
    b.style.zIndex = "4";
    if (!b.querySelector(".tilde")) {
      var t = document.createElement("span"); t.className = "tilde"; t.textContent = "✓";
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
          btn.type = "button"; btn.className = "op"; btn.textContent = o.texto;
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
          btn.innerHTML = '<img alt="" src="' + g.icono + '.webp"><span></span><span class="adentro"></span>';
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
          mini.src = G.escenas[p.escena].animales[it.animal].img + ".webp"; mini.alt = "";
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

  var PASOS = { decir: pasoDecir, tocar: pasoTocar, elegir: pasoElegir, clasificar: pasoClasificar };

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
    telon.querySelector("h1").textContent = "¡Lo lograste!";
    $("telonTxt").textContent = "No todo lo que nada es pez.";
    var btn = $("empezar");
    btn.textContent = "↺ Ver de nuevo";
    btn.onclick = function () { location.reload(); };
    telon.hidden = false;
  }

  function correr(i) {
    if (i >= G.pasos.length) return terminar();
    var p = G.pasos[i];
    return PASOS[p.tipo](p, i).then(function () { return correr(i + 1); });
  }

  // Precarga liviana: imágenes y voces, así el cambio de escena no se nota.
  function precargar() {
    Object.keys(G.imagenes).forEach(function (k) { var im = new Image(); im.src = k + ".webp"; });
    Object.keys(G.voces).forEach(function (k) { var a = new Audio(); a.preload = "auto"; a.src = "voz_" + k + ".mp3"; });
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
      voz.src = "voz_" + primero.voz + ".mp3";
      var pr = voz.play();
      if (pr && pr.catch) pr.catch(function () {});
    }
    $("telon").hidden = true;
    correr(0);
  }, { once: true });
})();
