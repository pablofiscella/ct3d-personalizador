// aventura_player.js — lector de "Elegí tu aventura": muestra el nodo actual (imagen +
// texto + opciones) y navega el grafo inyectado por el servidor (window.AVENTURA_*).
// El progreso se guarda en localStorage por token (la URL) para sobrevivir un refresh.
(function () {
  "use strict";
  var NODOS = window.AVENTURA_NODOS || {};
  var INICIO = window.AVENTURA_INICIO;
  var KEY = "ct3d_aventura:" + location.pathname;

  var $escena = document.getElementById("escena");
  var $texto = document.getElementById("texto");
  var $opciones = document.getElementById("opciones");
  var $final = document.getElementById("final-badge");
  var $reiniciar = document.getElementById("reiniciar");

  function guardar(nid) {
    try { localStorage.setItem(KEY, nid); } catch (e) {}
  }
  function cargar() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function mostrar(nid) {
    if (!NODOS[nid]) nid = INICIO;
    var nodo = NODOS[nid];
    $escena.src = nodo.imagen;
    $texto.textContent = nodo.texto;
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
