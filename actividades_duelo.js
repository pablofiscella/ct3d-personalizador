/* ── DUELO ENTRE COMPAÑEROS ("el preguntados") ────────────────────────────────────────
   Dos chicos del mismo curso, las MISMAS 5 preguntas, por turnos.

   Pedido de Pablo (29-jul-2026) con tres decisiones suyas que le dan la forma:

   · POR TURNOS, no en tiempo real. Cada uno juega cuando puede. Coordinar a dos chicos de
     ocho años en el mismo minuto no pasa, así que no hay salas ni presencia: una partida es
     un archivo, igual que el progreso.
   · SIN CHAT. No hay un solo campo de texto libre en toda la pantalla. Lo único que viaja
     de una persona es el nombre del perfil, que ya existe en el cuaderno. Es una decisión
     de seguridad: son chicos de 6 a 12 y no vamos a administrar un canal entre menores.
   · SIN RANKING. Se muestra qué acertó cada uno y se los felicita a los dos. Los motores
     que miramos (ALEKS, DreamBox) evitan el ranking público a propósito: el riesgo es
     desmoralizar justo al que más necesita seguir jugando.

   DE DÓNDE SALEN LAS PREGUNTAS. Del mismo currículum que el chico estudia: las 2.868
   preguntas de mecánica `trivia` del catálogo, indexadas por grado en `CUR_DUELO_POR_GRADO`
   (lo emite gen_curriculum.py junto con los bancos, por referencia y no por copia). No se
   escribió un banco propio a propósito — sería una segunda fuente para el mismo contenido,
   que es justo el problema que ya nos costó caro con las categorías.

   Sólo entran las de opción múltiple. Los juegos de arrastrar, ordenar o clasificar no se
   pueden comparar entre dos chicos con un número de aciertos.

   POR QUÉ NO SUMA ESTRELLAS NI TELEMETRÍA. El duelo no llama a `ctx.bien()` / `ctx.casi()`
   como el resto. Acá el chico responde UNA vez, apurado y compitiendo: tomar eso como
   evidencia de dominio ensuciaría el motor adaptativo, que decide qué enseñarle después. Es
   un juego, no una evaluación.

   EL CÓDIGO ES DE LA PARTIDA, NUNCA DE UN CUADERNO. Si llevara el token, compartirlo sería
   repartir la puerta del cuaderno de un chico. Ver duelos.py.

   LÍMITE CONOCIDO: el que recibe el código necesita tener SU cuaderno para cargarlo. Un
   amigo sin cuaderno no puede jugar todavía. ── */

/* El pozo del grado, aplanado: [{q, ops, cat}]. `ops[0]` es la correcta —convención de
   juegoTriviaTexto y de todo el catálogo— y acá se conserva, porque el que baraja para
   mostrar es la pantalla, no el dato. */
function _dueloPozo(grado) {
  const porGrado = (typeof CUR_DUELO_POR_GRADO !== "undefined") ? CUR_DUELO_POR_GRADO : {};
  const pozo = [];
  (porGrado[grado] || []).forEach(([cat, banco]) => {
    (banco || []).forEach((it) => {
      // se descarta lo que no sea una pregunta cerrada de verdad: sin 2 opciones no hay
      // nada que elegir, y una pregunta rota en un duelo la ve el chico y su compañero
      if (it && it.q && Array.isArray(it.ops) && it.ops.length >= 2) {
        pozo.push({ q: it.q, ops: it.ops.slice(0, 4), ok: 0, cat: cat });
      }
    });
  });
  return pozo;
}

/* 5 preguntas al azar, sin repetir y repartidas entre materias cuando se puede: cinco de
   Lengua seguidas harían que el duelo dependa de qué le gusta a cada uno en vez de lo que
   estudiaron los dos. */
function _dueloElegir5(grado) {
  const pozo = _dueloPozo(grado);
  if (pozo.length < 5) return null;
  const porCat = {};
  shuffle(pozo.slice()).forEach((p) => { (porCat[p.cat] = porCat[p.cat] || []).push(p); });
  const cats = shuffle(Object.keys(porCat));
  const elegidas = [];
  // una vuelta tomando una de cada materia, y las que falten del resto
  for (let v = 0; elegidas.length < 5 && v < 5; v++) {
    cats.forEach((c) => {
      if (elegidas.length < 5 && porCat[c][v]) elegidas.push(porCat[c][v]);
    });
  }
  return elegidas.slice(0, 5);
}

/* ── La cara de cada jugador ──────────────────────────────────────────────────────────
   Pablo (30-jul, viendo la página andando): "quizás poner algún ícono, por ejemplo el
   avatar".

   El avatar del cuaderno NO sirve acá: es un índice a las imágenes del TOKEN (`P[i]`, los
   personajes del grado), y la página del desafiado no tiene token — servirle el arte de
   otro cuaderno sería filtrar el material de un cliente.

   Así que la cara se DERIVA del nombre: misma persona, misma cara, en el cuaderno y en la
   página, sin guardar un dato nuevo y sin tocar el arte de nadie. Animales a propósito: no
   insinúan género ni tono de piel.

   ⚠ Esta función está DUPLICADA en duelo_publico.html (que es una página suelta, sin
   acceso a este archivo). Hay un test que corre las dos y falla si dejan de coincidir —
   si se separan, el mismo chico tendría dos caras distintas en las dos pantallas. */
const DUELO_CARAS = ["🦊", "🐼", "🦁", "🐨", "🐯", "🦉", "🐢", "🦋", "🐙", "🦄", "🐝", "🐳"];
function _dueloCara(nombre) {
  // minúsculas y sin espacios de más, igual que el motor para comparar nombres: si no,
  // "Sofi" y "sofi" —que para el duelo son la misma persona— tendrían caras distintas
  const n = String(nombre || "").trim().toLowerCase();
  let h = 0;
  for (let i = 0; i < n.length; i++) h = (h * 31 + n.charCodeAt(i)) >>> 0;
  return DUELO_CARAS[h % DUELO_CARAS.length];
}

function _dueloNombre() {
  try {
    const n = (Store.data && Store.data.activeProfile) || "";
    return String(n).trim().slice(0, 20) || "Alguien";
  } catch (e) { return "Alguien"; }
}

/* Estilos propios. Van inyectados y no en el CSS del cuaderno porque este archivo se sirve
   del repo y tiene que poder llegar solo a los links ya entregados. */
let _dueloCSSPuesto = false;
function _dueloCSS() {
  if (_dueloCSSPuesto) return;
  _dueloCSSPuesto = true;
  const s = document.createElement("style");
  s.textContent =
    ".duelo-caja{max-width:520px;margin:0 auto;text-align:center}" +
    ".duelo-caja p{font-size:17px;line-height:1.5;margin:12px 0}" +
    ".duelo-btn{display:block;width:100%;min-height:56px;margin:12px 0;padding:14px 18px;" +
    "border:0;border-radius:18px;background:var(--ac,#3D2FBF);color:#fff;font-family:inherit;" +
    "font-size:18px;font-weight:700;cursor:pointer}" +
    ".duelo-btn--2{background:transparent;color:var(--ac,#3D2FBF);" +
    "border:2px solid var(--ac,#3D2FBF)}" +
    ".duelo-pend{border:2px dashed color-mix(in srgb,var(--ac) 45%,transparent);" +
    "border-radius:16px;padding:12px 10px;margin:0 0 14px}" +
    ".duelo-pend-tit{margin:0 0 4px;font-weight:800;color:var(--ac)}" +
    ".duelo-codigo{font-family:ui-monospace,Menlo,monospace;font-size:44px;font-weight:700;" +
    "letter-spacing:.18em;margin:18px 0;padding:16px 10px;border-radius:18px;" +
    "background:color-mix(in srgb,var(--ac,#3D2FBF) 12%,transparent)}" +
    ".duelo-input{width:100%;box-sizing:border-box;text-align:center;font-size:34px;" +
    "font-family:ui-monospace,Menlo,monospace;letter-spacing:.16em;text-transform:uppercase;" +
    "padding:14px;border-radius:18px;border:2px solid var(--ac,#3D2FBF)}" +
    ".duelo-marcador{display:flex;gap:12px;justify-content:center;margin:20px 0}" +
    ".duelo-jug{flex:1;max-width:190px;padding:16px 10px;border-radius:18px;" +
    "background:color-mix(in srgb,var(--ac,#3D2FBF) 10%,transparent)}" +
    ".duelo-cara{font-size:42px;line-height:1;margin-bottom:8px}" +
    ".duelo-cara--hero{font-size:64px;margin:6px 0 10px}" +
    ".duelo-jug b{display:block;font-size:16px;margin-bottom:6px;word-break:break-word}" +
    ".duelo-jug span{font-size:34px;font-weight:700}" +
    ".duelo-aviso{font-size:15px;opacity:.75;margin-top:14px}";
  document.head.appendChild(s);
}

function _dueloCaja(ctx) {
  ctx.juego.innerHTML = "";
  const caja = el("div", "duelo-caja");
  ctx.juego.appendChild(caja);
  return caja;
}

/* ── las 5 preguntas ──
   `alTerminar(aciertos)`. Una sola oportunidad por pregunta: en un duelo, poder reintentar
   hasta acertar haría que los dos terminen siempre 5 de 5 y el resultado no diga nada. Se
   muestra cuál era la correcta, que es lo que deja algo aprendido. */
function _dueloJugar(ctx, preguntas, alTerminar) {
  let i = 0, aciertos = 0;
  ctx.rondas(preguntas.length);
  const paso = () => {
    ctx.ronda(i);
    const p = preguntas[i];
    const correcta = p.ops[p.ok || 0];
    ctx.consigna(p.q);
    ctx.juego.innerHTML = "";
    const fila = el("div", "opsTexto");
    let resuelto = false;
    shuffle(p.ops.slice()).forEach((op) => {
      const b = el("button", "op-texto", op);
      b.addEventListener("click", async () => {
        if (resuelto) return;
        resuelto = true;
        if (op === correcta) {
          aciertos++;
          b.classList.add("bien", "anim-pop");
          Sfx.ok();
        } else {
          b.classList.add("casi");
          Sfx.casi();
          // se marca la correcta: perder la pregunta y encima no saber cuál era es la
          // única forma de que el duelo no enseñe nada
          Array.from(fila.children).forEach((x) => {
            if (x.textContent === correcta) x.classList.add("bien");
          });
        }
        await espera(op === correcta ? 800 : 1500);
        i++;
        if (i >= preguntas.length) alTerminar(aciertos); else paso();
      });
      fila.appendChild(b);
    });
    ctx.juego.appendChild(el("div", "tablero")).appendChild(fila);
  };
  paso();
}

/* ── el marcador final ──
   Los dos números, sin ganador declarado ni tabla de posiciones (decisión de Pablo). Si
   todavía no jugó el compañero, se muestra el código para que lo siga compartiendo. */
function _dueloResultado(ctx, duelo, codigo) {
  const caja = _dueloCaja(ctx);
  const jug = duelo.jugadores || [];
  const total = (duelo.preguntas || []).length || 5;
  let marcador = '<div class="duelo-marcador">';
  jug.forEach((j) => {
    marcador += `<div class="duelo-jug"><div class="duelo-cara">${_dueloCara(j.nombre)}</div>` +
                `<b>${_dueloEscapar(j.nombre)}</b>` +
                `<span>${j.aciertos}</span><div>de ${total}</div></div>`;
  });
  marcador += "</div>";

  if (jug.length < 2) {
    caja.innerHTML =
      "<h2>¡Listo! 🎉</h2>" + marcador +
      "<p>Ahora pasale este código a un compañero para que juegue las mismas preguntas. " +
      "Si lo cerrás, lo volvés a encontrar acá adentro.</p>" +
      `<div class="duelo-codigo">${codigo}</div>`;
    caja.appendChild(_dueloBotonCompartir(codigo));
  } else {
    // se felicita a los dos, siempre. El que sacó menos es justo el que tiene que volver.
    const iguales = jug[0].aciertos === jug[1].aciertos;
    caja.innerHTML =
      `<h2>${iguales ? "¡Empataron! 🤝" : "¡Terminó el duelo! 🎉"}</h2>` + marcador +
      "<p>" + (iguales ? "Los dos igual de afilados." : "¡Muy bien los dos!") + "</p>";
  }
  const volver = el("button", "duelo-btn duelo-btn--2", "Volver a las actividades");
  volver.title = "El código queda guardado: podés compartirlo después desde el duelo.";
  volver.addEventListener("click", () => { Sfx.pop(); volverMenu(); });
  caja.appendChild(volver);
}

function _dueloEscapar(t) {
  const d = document.createElement("div");
  d.textContent = String(t == null ? "" : t);
  return d.innerHTML;
}

/* Lo que se comparte es un LINK, no el código suelto.

   Pablo (30-jul): "¿pero cómo se entera otro compañero?". Con el código pelado, el que lo
   recibía necesitaba tener SU cuaderno para cargarlo — el desafío sólo podía viajar entre
   dos chicos que ya habían comprado. `/reto/<codigo>` se abre sin nada.

   El código igual se muestra grande y se puede copiar: la mitad de los desafíos se van a
   pasar dictándolos en el recreo, que es justo para lo que está elegido el alfabeto. */
/* ── LOS DUELOS QUE EL CHICO YA CREÓ ───────────────────────────────────────────
   Pablo, 31-jul-2026: *"cuando un chico juega, ¿cómo le pasa el token al amigo? El que se
   puso a jugar primero no tiene ningún número que compartir"*.

   Reproducido en el navegador, el circuito era: toca "Empezar un duelo" → contesta las 5 →
   recién ahí aparece el código → toca "Volver a las actividades" → **el código desaparece
   para siempre**. No se guardaba en ninguna parte. Si no lo compartía en ese mismo momento
   —y un chico de nueve años cierra la pantalla— la partida quedaba huérfana en el servidor
   30 días, con sus 5 respuestas adentro, y el compañero no se enteraba nunca.

   Se guardan en el PERFIL del chico, no en el token: el cuaderno lo pueden usar dos
   hermanos y el duelo es de quien lo jugó. Tope de 3 y sólo el código y la fecha — no hace
   falta guardar las preguntas, que ya están en el servidor. ── */
const DUELOS_GUARDADOS = 3;

function _dueloMios() {
  try {
    const p = Store._perfil();
    return (p && Array.isArray(p.du)) ? p.du : [];
  } catch (e) { return []; }
}

function _dueloRecordar(codigo) {
  try {
    const p = Store._perfil(); if (!p) return;
    p.du = [{ c: codigo, ts: Date.now() }]
      .concat((p.du || []).filter((d) => d && d.c !== codigo))
      .slice(0, DUELOS_GUARDADOS);
    Store.save();
  } catch (e) { /* sin guardar, el duelo igual se jugó */ }
}

function _dueloOlvidar(codigo) {
  try {
    const p = Store._perfil(); if (!p) return;
    p.du = (p.du || []).filter((d) => d && d.c !== codigo);
    Store.save();
  } catch (e) { /* idem */ }
}

function _dueloLink(codigo) {
  return location.origin + "/reto/" + codigo;
}

function _dueloBotonCompartir(codigo) {
  const cont = el("div");
  const link = _dueloLink(codigo);
  const msg = "¡Te desafío! Tocá acá y jugá las mismas 5 preguntas: " + link;
  const wa = el("button", "duelo-btn", "Compartir por WhatsApp");
  wa.addEventListener("click", () => {
    Sfx.pop();
    window.open("https://wa.me/?text=" + encodeURIComponent(msg), "_blank", "noopener");
  });
  cont.appendChild(wa);
  // `navigator.share` abre el menú del sistema (WhatsApp, mensajes, mail…) y en el celular
  // del adulto —que es por donde va a viajar esto— es el camino natural. Sólo si existe.
  if (navigator.share) {
    const compartir = el("button", "duelo-btn duelo-btn--2", "Compartir de otra forma");
    compartir.addEventListener("click", () => {
      Sfx.pop();
      navigator.share({ text: msg }).catch(() => {});
    });
    cont.appendChild(compartir);
  }
  const copiar = el("button", "duelo-btn duelo-btn--2", "Copiar el link");
  copiar.addEventListener("click", async () => {
    Sfx.pop();
    try {
      await navigator.clipboard.writeText(link);
      toast("¡Link copiado!");
    } catch (e) {
      // sin permiso de portapapeles el código igual está en pantalla, grande y dictable
      toast("Copiá el código de la pantalla 🙂");
    }
  });
  cont.appendChild(copiar);
  return cont;
}

/* Un solo lugar para hablar con el motor. Si la red falla, el chico se entera con una
   frase y un botón, nunca con una pantalla trabada. */
async function _dueloPedir(url, opciones) {
  const r = await fetch(url, opciones);
  const j = await r.json().catch(() => ({}));
  if (!r.ok || !j.ok) throw new Error((j && j.error) || "no se pudo");
  return j;
}

function _dueloError(ctx, texto, reintentar) {
  const caja = _dueloCaja(ctx);
  caja.innerHTML = `<h2>Uy 😅</h2><p>${_dueloEscapar(texto)}</p>`;
  const b = el("button", "duelo-btn", "Probar de nuevo");
  b.addEventListener("click", () => { Sfx.pop(); reintentar(); });
  caja.appendChild(b);
  const v = el("button", "duelo-btn duelo-btn--2", "Volver a las actividades");
  v.addEventListener("click", () => { Sfx.pop(); volverMenu(); });
  caja.appendChild(v);
}

GAMES.duelo = {
  crear(ctx) {
    _dueloCSS();
    const grado = Math.max(1, Math.min(7, gradoDelChico()));

    const inicio = () => {
      ctx.consigna("Jugá las mismas 5 preguntas que un compañero.");
      const caja = _dueloCaja(ctx);
      caja.innerHTML =
        `<div class="duelo-cara duelo-cara--hero">${_dueloCara(_dueloNombre())}</div>` +
        "<h2>Duelo con un compañero</h2>" +
        "<p>Cinco preguntas de tu grado. Vos jugás ahora y tu compañero juega " +
        "cuando pueda, con las mismas preguntas.</p>";

      // Los duelos que ya creó van PRIMERO: es lo único accionable de esta pantalla —
      // hay un compañero esperando del otro lado — y era justamente lo que no existía.
      _dueloMios().forEach((d) => {
        const fila = el("div", "duelo-pend");
        fila.innerHTML = '<p class="duelo-pend-tit">Tu duelo, esperando a un compañero</p>' +
          `<div class="duelo-codigo">${_dueloEscapar(d.c)}</div>`;
        const compartir = _dueloBotonCompartir(d.c);
        fila.appendChild(compartir);
        const ver = el("button", "duelo-btn duelo-btn--2", "Ver si ya jugó");
        ver.addEventListener("click", async () => {
          Sfx.pop();
          try {
            const j = await _dueloPedir("/duelo/" + d.c, {});
            if ((j.duelo.jugadores || []).length >= 2) _dueloOlvidar(d.c);
            _dueloResultado(ctx, j.duelo, d.c);
          } catch (e) {
            // 404 = la partida venció (30 días) o se borró: sacarla en vez de dejarle
            // un código muerto en pantalla para siempre
            _dueloOlvidar(d.c);
            _dueloError(ctx, "Ese duelo ya no está disponible.", inicio);
          }
        });
        fila.appendChild(ver);
        caja.appendChild(fila);
        // y si el compañero YA jugó, que se entere sin tener que tocar nada
        _dueloPedir("/duelo/" + d.c, {}).then((j) => {
          const otros = (j.duelo.jugadores || []).length;
          if (otros >= 2 && fila.isConnected) {
            fila.querySelector(".duelo-pend-tit").textContent = "¡Ya jugó tu compañero!";
            ver.textContent = "Ver el resultado";
            compartir.remove();   // ya no hay a quién invitar: el duelo está cerrado
          }
        }).catch(() => {
          // La partida ya no existe (venció a los 30 días, o se borró). Se saca sola en vez
          // de esperar a que el chico toque un código muerto para enterarse.
          _dueloOlvidar(d.c);
          fila.remove();
        });
      });

      const bCrear = el("button", "duelo-btn", "Empezar un duelo");
      bCrear.addEventListener("click", () => { Sfx.pop(); crear(); });
      caja.appendChild(bCrear);
      const bUnir = el("button", "duelo-btn duelo-btn--2", "Tengo un código");
      bUnir.addEventListener("click", () => { Sfx.pop(); unirse(); });
      caja.appendChild(bUnir);
    };

    const crear = () => {
      const preguntas = _dueloElegir5(grado);
      if (!preguntas) {
        return _dueloError(ctx, "Todavía no hay preguntas de duelo para tu grado.", inicio);
      }
      _dueloJugar(ctx, preguntas, async (aciertos) => {
        const caja = _dueloCaja(ctx);
        caja.innerHTML = "<h2>Guardando tu duelo…</h2>";
        try {
          const j = await _dueloPedir("/duelo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ grado: grado, preguntas: preguntas,
                                   nombre: _dueloNombre(), aciertos: aciertos }),
          });
          _dueloRecordar(j.codigo);   // para poder compartirlo después, no sólo ahora
          _dueloResultado(ctx, j.duelo, j.codigo);
        } catch (e) {
          // el chico ya jugó: lo que se perdió es el código, no su partida
          _dueloError(ctx, "No pudimos guardar el duelo. Fijate que tengas internet.",
                      inicio);
        }
      });
    };

    const unirse = () => {
      ctx.consigna("Escribí el código que te pasaron.");
      const caja = _dueloCaja(ctx);
      caja.innerHTML = "<h2>Tengo un código</h2>";
      const inp = el("input", "duelo-input");
      inp.maxLength = 5;
      inp.autocapitalize = "characters";
      inp.setAttribute("aria-label", "Código del duelo");
      // el alfabeto de duelos.py: sin vocales (para no formar palabras) ni 0/O/1/I/L, que
      // se confunden al dictarlo. Se filtra al tipear para que no puedan escribir algo
      // que el motor va a rechazar igual.
      inp.addEventListener("input", () => {
        inp.value = inp.value.toUpperCase().replace(/[^23456789BCDFGHJKMNPQRSTVWXYZ]/g, "");
      });
      caja.appendChild(inp);
      const b = el("button", "duelo-btn", "Jugar");
      b.addEventListener("click", async () => {
        Sfx.pop();
        const cod = inp.value.trim();
        if (cod.length !== 5) return toast("El código tiene 5 caracteres");
        caja.innerHTML = "<h2>Buscando el duelo…</h2>";
        let duelo;
        try {
          duelo = (await _dueloPedir("/duelo/" + cod, {})).duelo;
        } catch (e) {
          return _dueloError(ctx, "No encontramos ese código. Revisalo con tu compañero.",
                             unirse);
        }
        if ((duelo.jugadores || []).length >= 2) {
          return _dueloResultado(ctx, duelo, cod);   // ya jugaron los dos: sólo mirar
        }
        _dueloJugar(ctx, duelo.preguntas, async (aciertos) => {
          const c2 = _dueloCaja(ctx);
          c2.innerHTML = "<h2>Guardando…</h2>";
          try {
            const j = await _dueloPedir("/duelo/" + cod + "/jugue", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ nombre: _dueloNombre(), aciertos: aciertos }),
            });
            _dueloResultado(ctx, j.duelo, cod);
          } catch (e) {
            _dueloError(ctx, "No pudimos guardar tu resultado. Fijate que tengas internet.",
                        inicio);
          }
        });
      });
      caja.appendChild(b);
      const v = el("button", "duelo-btn duelo-btn--2", "Volver");
      v.addEventListener("click", () => { Sfx.pop(); inicio(); });
      caja.appendChild(v);
      setTimeout(() => inp.focus(), 60);
    };

    inicio();
  },
};

/* ── La entrada en el menú ──
   Se inyecta desde el navegador y no desde data.json a propósito: el menú queda CONGELADO
   en el token el día de la compra, así que un cuaderno ya entregado nunca vería un juego
   nuevo. Mismo criterio que las actividades que suma el padre.

   Cae en "Extras" solo: `Adapt.categoria()` devuelve "logica" para lo que no está en el
   grafo de saberes, y esa categoría se muestra con el título "Extras". Es el lugar correcto
   —no es una actividad del Diseño Curricular— y además `logica` está excluida del plan
   adaptativo y del panel de padres, que es justo lo que queremos: el duelo no mide.

   Sólo en la línea ESCOLAR: es un juego entre compañeros de un mismo grado, y los cuadernos
   de cumpleaños no tienen grado ni curso. ── */
function sumarDueloDeCompaneros() {
  try {
    if (!D || !D.escolar_on) return;
    const ya = (D.menu || []).some((m) => (typeof m === "string" ? m : m.id) === "duelo");
    if (ya) return;
    if (_dueloPozo(Math.max(1, Math.min(7, gradoDelChico()))).length < 5) return;
    D.menu.push({ id: "duelo", titulo: "Duelo con un compañero", icono: "🆚",
                  cfg: {}, nivel: 1 });
  } catch (e) { /* sin duelo, el cuaderno de siempre */ }
}
