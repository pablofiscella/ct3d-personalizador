// aventura_player.js — lector de "Elegí tu aventura": muestra el nodo actual (imagen +
// texto + opciones) y navega el grafo inyectado por el servidor (window.AVENTURA_*).
// El progreso se guarda en localStorage por token (la URL) para sobrevivir un refresh.
(function () {
  "use strict";
  var NODOS = window.AVENTURA_NODOS || {};
  var INICIO = window.AVENTURA_INICIO;
  var KEY = "ct3d_aventura:" + location.pathname;
  var AKEY = "ct3d_aventura_audio:" + location.pathname;

  var $escena = document.getElementById("escena");
  var $texto = document.getElementById("texto");
  var $opciones = document.getElementById("opciones");
  var $final = document.getElementById("final-badge");
  var $reiniciar = document.getElementById("reiniciar");
  var $audio = document.getElementById("audio");
  var $audioToggle = document.getElementById("audio-toggle");

  function guardar(nid) {
    try { localStorage.setItem(KEY, nid); } catch (e) {}
  }
  function cargar() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  // Narración por nodo (opcional): si el token todavía no tiene audio generado
  // (aventura_audio.py), el pedido da 404 y el cuento se lee igual, en silencio —
  // degradación silenciosa a propósito, nunca un error visible para el chico.
  function audioActivo() {
    try { return localStorage.getItem(AKEY) !== "0"; } catch (e) { return true; }
  }
  function marcarAudioToggle() {
    $audioToggle.textContent = audioActivo() ? "🔊" : "🔇";
  }
  var actualNid = null;
  function narrar(nid) {
    $audio.pause();
    if (!audioActivo()) return;
    $audio.src = nid + ".mp3";
    $audio.play().catch(function () {});
  }
  $audioToggle.onclick = function () {
    var on = !audioActivo();
    try { localStorage.setItem(AKEY, on ? "1" : "0"); } catch (e) {}
    marcarAudioToggle();
    if (on) { narrar(actualNid); } else { $audio.pause(); }
  };
  marcarAudioToggle();

  function mostrar(nid) {
    if (!NODOS[nid]) nid = INICIO;
    var nodo = NODOS[nid];
    actualNid = nid;
    $escena.src = nodo.imagen;
    $texto.textContent = nodo.texto;
    narrar(nid);
    $opciones.innerHTML = "";
    if (nodo.final) {
      $final.style.display = "block";
      $reiniciar.style.display = "block";
    } else {
      $final.style.display = "none";
      $reiniciar.style.display = "none";
      (nodo.opciones || []).forEach(function (op) {
        var b = document.createElement("button");
        b.className = "btn ac op";
        b.textContent = op.texto;
        b.onclick = function () {
          guardar(op.next);
          mostrar(op.next);
          window.scrollTo({ top: 0, behavior: "smooth" });
        };
        $opciones.appendChild(b);
      });
    }
    guardar(nid);
  }

  $reiniciar.onclick = function () { mostrar(INICIO); };

  mostrar(cargar() || INICIO);
})();
