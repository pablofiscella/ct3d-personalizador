"""Audiolibro web — el cuento personalizado NARRADO en una página interactiva:
la voz lee cada página (con el nombre del chico) y al terminar el clip la hoja
gira sola (efecto page-flip CSS). Link con token, igual que la invitación web.

Por pedido se genera en AUDIOLIBROS_DIR/<token>/: las 10 páginas como JPG, un
MP3 narrado por página (OpenAI TTS) y manifest.json. Vigencia 365 días.

API: crear(data, tema, client_tts) -> token · html(token, base_url) -> str
     archivo(token, nombre) -> (bytes, content_type) | None
"""
import html as html_mod
import io
import json
import os
import re
import secrets
import time
import urllib.request
import zlib

KIT = os.path.dirname(os.path.abspath(__file__))
AUDIOLIBROS_DIR = os.environ.get(
    "CT3D_AUDIOLIBROS_DIR", os.path.join(KIT, "audiolibros"))
VIGENCIA_DIAS = 7300   # "para siempre" en la práctica (~20 años) — respalda Mis compras

_TTS_URL = "https://api.openai.com/v1/audio/speech"
_VOZ = "sage"        # la voz del preset oficial "Bedtime Story" de openai.fm
VOCES = {"fable": "Voz de cuentacuentos", "nova": "Voz femenina cálida",
         "onyx": "Voz masculina profunda"}
# Estructura Affect/Tone/Pacing/... calcada de los presets oficiales "Bedtime
# Story" + "Serene" de openai.fm (así recomienda OpenAI usar `instructions`;
# en inglés siguen mejor). El acento rioplatense se ancla desde el TEXTO (voseo).
_INSTRUCCIONES = (
    "Affect: A warm, gentle female storyteller telling a bedtime story to a "
    "small child (2 to 6 years old), in Latin American Spanish from Argentina "
    "(Rioplatense accent).\n"
    "Tone: Soft, magical, loving and reassuring, like a mother reading a "
    "picture book at night; full of wonder, never loud or rushed.\n"
    "Pacing: Slow and unhurried, around 120 to 130 words per minute. Brief "
    "pause after every sentence; a longer, expectant pause before magical "
    "moments.\n"
    "Emotion: Tender warmth and quiet delight; gently playful in adventure "
    "moments, hushed and sleepy toward the end.\n"
    "Pronunciation: Clear, soft articulation with slightly elongated vowels. "
    "Argentine Spanish: pronounce 'll' and 'y' with the soft 'sh' sound, and "
    "read voseo forms ('mirá', 'tenés', 'dormite') naturally.\n"
    "Pauses: Gentle pauses at commas and ellipses; let final sentences trail "
    "off softly.")

# ElevenLabs: voz por default del audiolibro (más natural que OpenAI). Lizy es una voz
# nativa en español pensada para cuentos infantiles. La key se lee de config.json.
# MODELO: eleven_v3 con etiquetas de emoción ([whispers]/[excited]/[soft]) — elegido
# por Pablo en A/B contra multilingual_v2 (2026-07-06, muestra voz_v3_tags). Modo
# Natural (stability 0.5). OJO: los clones profesionales (PVC) aún NO están
# optimizados para v3 — si algún día clonamos locutora, evaluar volver a v2.
_EL_URL = "https://api.elevenlabs.io/v1/text-to-speech"
_EL_VOICE = "rrErIO88ehxTnspOjKvf"   # Lizy
_EL_MODEL = "eleven_v3"
_EL_SETTINGS = {"stability": 0.5}
_EL_KEY_CACHE = {}

# Etiquetas de emoción v3 automáticas y CONSERVADORAS (receta investigada:
# 1 etiqueta por página máximo, whitelist dulce, al inicio del segmento; las
# 2 páginas finales llevan el ritardando del cierre para dormir). Solo para la
# narración: jamás se renderizan en el libro.
_RE_SUSURRO = re.compile(r"susurr", re.IGNORECASE)


def _etiqueta_pagina(texto, pos=None, total=None):
    """Devuelve el texto con SU etiqueta v3 (una sola). pos/total permiten el
    cierre para dormir: anteúltima página [slows down], última [whispers]."""
    t = texto
    low = t.lower()
    if _RE_SUSURRO.search(low) and "“" in t:
        return t.replace("“", "[whispers] “", 1)
    if pos is not None and total:
        if pos == total - 1:                      # última: casi un susurro
            return "[whispers] " + t
        if pos == total - 2:                      # anteúltima: bajar el ritmo
            return "[slows down] " + t
        if pos == 0:                              # tapa: bienvenida cálida
            return "[warmly] " + t
    if low.count("¡") >= 2 or "sorpresa!" in low:
        return "[excited] " + t
    if "se durmió" in low or "a dormir" in low or "buenas noches" in low:
        return "[slows down] " + t
    if t.lstrip().startswith("¿") or "¿y si" in low:
        return "[curious] " + t
    return t


def _elevenlabs_key():
    if "k" in _EL_KEY_CACHE:
        return _EL_KEY_CACHE["k"]
    k = (os.environ.get("ELEVENLABS_API_KEY") or "").strip()
    if not k:
        for p in (os.path.join(KIT, "config.json"), "/opt/ct3d/backend/config.json"):
            try:
                k = (json.load(open(p)).get("elevenlabs_api_key") or "").strip()
                if k:
                    break
            except Exception:
                pass
    _EL_KEY_CACHE["k"] = k
    return k


def _tts_elevenlabs(texto, timeout=120, seed=None):
    key = _elevenlabs_key()
    if not key:
        return None
    payload = {"text": texto, "model_id": _EL_MODEL,
               "voice_settings": _EL_SETTINGS}
    if seed is not None:
        payload["seed"] = int(seed) % (2 ** 31)
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        "%s/%s?output_format=mp3_44100_128" % (_EL_URL, _EL_VOICE),
        data=body, method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _dur_mp3_128(b):
    """Duración aprox (s) de un mp3 CBR 128 kbps: bytes * 8 / 128000."""
    return len(b) / 16000.0


def _duracion_ok(texto, mp3):
    """QA de ritmo (receta: cuentos infantiles ~125 palabras/min). Una toma
    apurada o cortada se detecta por duración fuera de rango — se reintenta."""
    palabras = max(1, len(re.findall(r"\w+", texto)))
    esperado = palabras / 125.0 * 60.0
    dur = _dur_mp3_128(mp3)
    return esperado * 0.55 <= dur <= esperado * 1.9


def _tts_openai(api_key, texto, timeout=120, voz=None):
    v = voz if voz in VOCES else _VOZ
    # las etiquetas v3 de ElevenLabs no existen acá: se leerían en voz alta
    texto = re.sub(r"\[[a-z][a-z ]*\]\s*", "", texto)
    body = json.dumps({"model": "gpt-4o-mini-tts", "voice": v, "input": texto,
                       "response_format": "mp3",
                       "instructions": _INSTRUCCIONES}).encode()
    req = urllib.request.Request(_TTS_URL, data=body, method="POST", headers={
        "Authorization": "Bearer " + api_key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def tts_mp3(api_key, texto, timeout=120, voz=None, seed=None):
    """MP3 de la narración de `texto`. Por default usa ElevenLabs (Lizy sobre
    eleven_v3); si el cliente eligió una voz OpenAI usa esa; y si ElevenLabs
    falla, cae a OpenAI como respaldo automático. Con `seed` (fijo por libro)
    mantiene la consistencia entre páginas (v3 no tiene request stitching) y
    reintenta con seed+1 si la toma sale con ritmo raro (QA de duración)."""
    v = (str(voz or "").strip().lower())
    if v not in VOCES:                    # default o 'lizy' → ElevenLabs
        base = seed if seed is not None else 4242
        for intento in range(3):
            try:
                mp3 = _tts_elevenlabs(texto, timeout, seed=base + intento)
                if mp3 and _duracion_ok(texto, mp3):
                    return mp3
                if mp3 and intento == 2:  # 3 tomas raras: devolver la última
                    return mp3
            except Exception as e:
                print("[tts] ElevenLabs falló (%s)" % e, flush=True)
                break
        v = _VOZ
    return _tts_openai(api_key, texto, timeout, v)


def _titulo_libro(data):
    """Título del libro: el de la HISTORIA elegida (catálogo), con fallback al
    clásico del libro de kit."""
    from libro_historias import TITULOS
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    t = TITULOS.get(str(data.get("historia") or "").strip().lower())
    return ("%s — el cuento de %s" % (t, nombre)) if t \
        else "La gran aventura de %s" % nombre


def _textos_narracion(data, tema):
    """Texto a narrar por página (0..9): portada, dedicatoria, 7 de historia, fin."""
    import libro
    from libro_historias import TITULOS
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    dedic = (str(data.get("dedicatoria") or "").strip()) or \
        "Que nunca dejes de soñar, de jugar y de creer en vos."
    t = TITULOS.get(str(data.get("historia") or "").strip().lower())
    tapa = ("“%s”. Un cuento de %s." % (t, nombre)) if t \
        else "La gran aventura de %s. Un cuento personalizado." % nombre
    cuerpo = libro.cuento(data, tema, catalogo=True)
    textos = ([tapa,
               "Este cuento pertenece a %s. %s" % (nombre, dedic)]
              + cuerpo
              + ["Fin. ¡Hasta la próxima aventura, %s!" % nombre])
    # etiquetas v3 por posición (tapa cálida, cierre para dormir en las últimas)
    n = len(textos)
    return [_etiqueta_pagina(tx, pos=i, total=n) for i, tx in enumerate(textos)]


def _marca_gen(token):
    return os.path.join(AUDIOLIBROS_DIR, token, ".generando")


def marcar_generando(token):
    """Reserva el token y lo marca 'en generación', para que el visor muestre un
    cartel de espera mientras el worker crea páginas + narración (~1-2 min)."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,32}", token or ""):
        return
    os.makedirs(os.path.join(AUDIOLIBROS_DIR, token), exist_ok=True)
    with open(_marca_gen(token), "w") as f:
        f.write("1")


def _quitar_generando(token):
    try:
        os.remove(_marca_gen(token))
    except OSError:
        pass


def _marca_error(token):
    return os.path.join(AUDIOLIBROS_DIR, token, ".error")


def marcar_error(token, motivo=""):
    """La generación falló definitivamente: saca el '.generando' (para que el
    visor NO quede en 'grabándose' eterno) y deja un '.error' con el motivo, así
    el visor muestra un cartel amable y queda registro para el vendedor."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,32}", token or ""):
        return
    os.makedirs(os.path.join(AUDIOLIBROS_DIR, token), exist_ok=True)
    _quitar_generando(token)
    try:
        with open(_marca_error(token), "w", encoding="utf-8") as f:
            f.write(str(motivo)[:500])
    except OSError:
        pass


def estado(token):
    """'listo' si el audiolibro ya está generado, 'generando' si está en curso,
    'error' si la generación falló, None si el token no existe."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,32}", token or ""):
        return None
    d = os.path.join(AUDIOLIBROS_DIR, token)
    if os.path.isfile(os.path.join(d, "manifest.json")):
        return "listo"
    if os.path.isfile(_marca_gen(token)):
        return "generando"
    if os.path.isfile(_marca_error(token)):
        return "error"
    return None


def crear(data, tema, api_key, escenas_dir=None, progress=None, token=None):
    voz = (str(data.get("voz") or "").strip().lower()) or None
    """Genera páginas JPG + narración MP3 + manifest. Devuelve el token del link.
    Si se pasa `token` (válido), lo usa como link estable del visor — así la tienda
    puede mostrar la URL /al/<token> apenas arranca la compra, antes de que termine
    la generación. Si no, genera uno nuevo."""
    import libro
    if not (token and re.fullmatch(r"[A-Za-z0-9_-]{8,32}", token)):
        token = secrets.token_urlsafe(12)
    d = os.path.join(AUDIOLIBROS_DIR, token)
    os.makedirs(d, exist_ok=True)
    textos = _textos_narracion(data, tema)
    ctx = libro.usar_escenas_dir(escenas_dir) if escenas_dir else \
          libro.usar_genero(data.get("genero"))
    try:
        if ctx:
            ctx.__enter__()
        total = libro.total_paginas(tema, data.get("edad"), data.get("historia"), catalogo=True)
        for i in range(total):
            if progress:
                progress("Página %d de %d…" % (i + 1, total))
            img = libro.pagina_libro(i, data, tema, catalogo=True).convert("RGB")
            img.resize((img.width * 2 // 3, img.height * 2 // 3)).save(
                os.path.join(d, "pag_%02d.jpg" % i), quality=86)
            with open(os.path.join(d, "pag_%02d.mp3" % i), "wb") as f:
                f.write(tts_mp3(api_key, textos[i], voz=voz,
                                seed=zlib.crc32(token.encode())))
    finally:
        if ctx:
            ctx.__exit__(None, None, None)
    with open(os.path.join(d, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"tema": tema, "nombre": data.get("nombre", ""),
                   "titulo": _titulo_libro(data),
                   "paginas": total, "creado": int(time.time())},
                  f, ensure_ascii=False)
    _quitar_generando(token)
    _limpiar_vencidos()
    return token


def _cargar(token):
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,32}", token or ""):
        return None
    p = os.path.join(AUDIOLIBROS_DIR, token, "manifest.json")
    if not os.path.isfile(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def archivo(token, nombre):
    """(bytes, content_type) de un asset del audiolibro, o None."""
    if not _cargar(token) or not re.fullmatch(r"pag_\d{2}\.(jpg|mp3)", nombre or ""):
        return None
    p = os.path.join(AUDIOLIBROS_DIR, token, nombre)
    if not os.path.isfile(p):
        return None
    ct = "image/jpeg" if nombre.endswith(".jpg") else "audio/mpeg"
    with open(p, "rb") as f:
        return f.read(), ct


def _limpiar_vencidos():
    import shutil
    limite = time.time() - VIGENCIA_DIAS * 86400
    try:
        for fn in os.listdir(AUDIOLIBROS_DIR):
            p = os.path.join(AUDIOLIBROS_DIR, fn)
            if os.path.isdir(p) and os.path.getmtime(p) < limite:
                shutil.rmtree(p, ignore_errors=True)
    except OSError:
        pass


def html(token, base_url=""):
    """El visor: página a pantalla completa, narración y page-flip automático."""
    reg = _cargar(token)
    if not reg:
        return None
    e = html_mod.escape
    n = int(reg.get("paginas", 10))
    titulo = (reg.get("titulo") or
              "La gran aventura de %s" % (reg.get("nombre") or "")) + " — audiolibro"
    return """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>%(titulo)s</title><style>
* { margin:0; padding:0; box-sizing:border-box; }
html,body { height:100%%; }
body { background:#2a2438; font-family:system-ui,sans-serif; overflow:hidden;
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; padding:6px 0; }
#flip img { border-radius:6px; }
.controles { display:flex; gap:10px; align-items:center; justify-content:center;
  flex-wrap:wrap; flex-shrink:0; max-width:96vw; }
.velrow { gap:8px; }
.velrow input[type=range] { width:140px; accent-color:#6B5BD2; }
button { background:#6B5BD2; color:#fff; border:0; border-radius:50%%; width:52px; height:52px;
  font-size:22px; cursor:pointer; flex:0 0 auto; line-height:1; }
button.sec { background:#453a66; width:44px; height:44px; font-size:16px; }
.pag { color:#b8aede; font-size:14px; min-width:52px; text-align:center; }
body.tv .controles, body.tv #diag { display:none; }
@media (max-width:520px){
  button { width:46px; height:46px; font-size:19px; }
  button.sec { width:40px; height:40px; font-size:14px; }
  .controles { gap:8px; } .velrow input[type=range] { width:130px; }
}
</style></head><body>
<div id="flip"></div>
<div class="controles">
  <button class="sec" id="reinicio" title="Volver al principio">↺</button>
  <button class="sec" id="prev">⏮</button>
  <button id="play">▶</button>
  <button class="sec" id="next">⏭</button>
  <span class="pag" id="pag">1 / %(n)d</span>
  <button class="sec" id="fs" title="Pantalla completa">⛶</button>
  <button class="sec" id="cast" title="Ver en la tele (Chromecast)">📺</button>
</div>
<div class="controles velrow">
  <span style="color:#b8aede;font-size:16px">🐢</span>
  <input type="range" id="vel" min="0.7" max="1.4" step="0.05" value="1">
  <span style="color:#b8aede;font-size:16px">🐇</span>
  <span class="pag" id="velval" style="min-width:38px">1.0x</span>
</div>
<div id="diag" style="color:#e0b0b0;font-size:12px;min-height:16px"></div>
<audio id="audio" preload="auto"></audio>
<script src="https://unpkg.com/page-flip@2.0.7/dist/js/page-flip.browser.js"></script>
<script>
var N=%(n)d, base="%(base)s/al/%(token)s/", V="?v=%(v)d";
var audio=document.getElementById('audio'), play=document.getElementById('play'),
    pag=document.getElementById('pag'), vel=document.getElementById('vel'),
    diag=document.getElementById('diag');
var narrando=false, actual=0;
function pad(x){return ('0'+x).slice(-2);}
function err(m){ diag.textContent=m; }
audio.addEventListener('error', function(){ err('audio error: no se pudo cargar el clip'); });
var availH = Math.max(280, window.innerHeight - 180);
var h = availH, w = Math.round(h * 827 / 1169);
if (w > window.innerWidth * 0.94) { w = Math.round(window.innerWidth * 0.94); h = Math.round(w * 1169 / 827); }
var flip=null;
try {
  flip = new St.PageFlip(document.getElementById('flip'), {
    width: w, height: h, size: 'fixed',
    usePortrait: true, showCover: true, maxShadowOpacity: 0.65,
    mobileScrollSupport: false, flippingTime: 850 });
  var urls=[]; for(var k=0;k<N;k++) urls.push(base+'pag_'+pad(k)+'.jpg'+V);
  // Página en blanco extra como CONTRATAPA del FIN: con cantidad impar, la librería
  // recicla el canvas de la hoja anterior durante la transición (se veía la página
  // vieja hasta que terminaba el giro). El blanco se genera acá, sin pedir nada.
  var cv=document.createElement('canvas'); cv.width=827; cv.height=1169;
  var cx=cv.getContext('2d'); cx.fillStyle='#FDF7EE'; cx.fillRect(0,0,827,1169);
  urls.push(cv.toDataURL('image/jpeg', 0.7));
  flip.loadFromImages(urls);
  flip.on('flip', function(e){
    if (e.data >= N) { pag.textContent=N+' / '+N; return; }
    actual=e.data; mostrarPag();
    if(narrando) narrarVisibles(); });
} catch(ex) { err('visor: '+ex.message); }
// En pantalla ancha la librería muestra DOBLE página (pliego): hay que narrar
// las dos hojas visibles antes de girar — si no, se salteaba una (bug fútbol pág 1).
var cola = [];
function visibles(){
  var esPliego = flip && flip.getOrientation && flip.getOrientation() === 'landscape';
  if (esPliego && actual > 0 && actual + 1 < N) return [actual, actual + 1];
  return [actual];
}
function mostrarPag(){
  var v = visibles();
  pag.textContent = (v.length === 2 ? (v[0]+1)+'-'+(v[1]+1) : (v[0]+1)) + ' / ' + N;
}
function narrarVisibles(){
  cola = visibles().slice();
  reproducir(cola.shift());
}
function reproducir(i){
  audio.src = base+'pag_'+pad(i)+'.mp3'+V;
  audio.load();
  // load() resetea playbackRate → defaultPlaybackRate manda para las páginas siguientes
  audio.defaultPlaybackRate = parseFloat(vel.value);
  audio.playbackRate = parseFloat(vel.value);
  var p = audio.play();
  if (p && p.catch) p.catch(function(e){
    narrando=false; play.textContent='▶'; err('tocá ▶ de nuevo ('+e.name+')');
    document.body.classList.remove('tv'); });   // modo TV sin autoplay: mostrar controles
}
audio.addEventListener('ended', function(){
  if (!narrando) return;
  if (cola.length) { reproducir(cola.shift()); return; }  // la otra hoja del pliego
  var ultimaVisible = visibles()[visibles().length - 1];
  if (ultimaVisible < N-1) { if(flip){ flip.flipNext(); } else { actual++; narrarVisibles(); } }
  else { narrando=false; play.textContent='▶'; }
});
var velval=document.getElementById('velval');
vel.oninput = function(){
  audio.defaultPlaybackRate = parseFloat(vel.value);
  audio.playbackRate = parseFloat(vel.value);
  velval.textContent = parseFloat(vel.value).toFixed(2).replace(/0$/,'')+'x';
};
play.onclick = function(){
  if (narrando) { narrando=false; audio.pause(); play.textContent='▶'; return; }
  narrando=true; play.textContent='⏸'; err('');
  narrarVisibles();
};
document.getElementById('prev').onclick = function(){ if(flip) flip.flipPrev(); };
document.getElementById('next').onclick = function(){ if(flip) flip.flipNext(); };
document.getElementById('reinicio').onclick = function(){
  narrando=false; audio.pause(); play.textContent='▶'; err('');
  actual=0;
  if(flip){ try{ flip.turnToPage(0); }catch(ex){ } }
  mostrarPag();
};
// ── pantalla completa (⛶) — se oculta donde no existe (iPhone) ──
var fsBtn=document.getElementById('fs');
if (document.documentElement.requestFullscreen) {
  fsBtn.onclick=function(){
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen().catch(function(){});
  };
} else { fsBtn.style.display='none'; }
// ── transmitir a la tele (📺): mismo selector de Chromecast que el menú de
// Chrome, vía Presentation API. En la tele el libro abre en modo TV (?tv=1):
// sin controles y narrando solo. Se oculta donde no está soportado (iOS). ──
var castBtn=document.getElementById('cast');
var tvUrl=location.origin+location.pathname.replace(/\\/+$/,'')+'?tv=1';
if (window.PresentationRequest) {
  try {
    var preq=new PresentationRequest([tvUrl]);
    if (navigator.presentation) navigator.presentation.defaultRequest=preq;
    castBtn.onclick=function(){
      err('buscando Chromecast…');
      preq.start().then(function(conn){
        err('');
        conn.addEventListener('close', function(){ err('se cerró la transmisión'); });
        conn.addEventListener('terminate', function(){ err('se cerró la transmisión'); });
      }).catch(function(e2){
        if (e2.name==='NotAllowedError') { err(''); return; }   // el usuario cerró el selector
        err('No se pudo transmitir (' + e2.name + ': ' + (e2.message || '') +
            ') — probá con Transmitir… del menú de Chrome');
      });
    };
  } catch(ex3){ castBtn.style.display='none'; }
} else { castBtn.style.display='none'; }
// ── modo TV (receptor Chromecast / ?tv=1): narración automática ──
if (/[?&]tv=1/.test(location.search)) {
  document.body.classList.add('tv');
  setTimeout(function(){ if (!narrando) play.onclick(); }, 1200);
}
pag.textContent='1 / '+N;
</script></body></html>""" % {"titulo": e(titulo), "token": e(token),
                              "base": e(base_url), "n": n,
                              "v": int(reg.get("creado", 0))}
