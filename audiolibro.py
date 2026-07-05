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

KIT = os.path.dirname(os.path.abspath(__file__))
AUDIOLIBROS_DIR = os.environ.get(
    "CT3D_AUDIOLIBROS_DIR", os.path.join(KIT, "audiolibros"))
VIGENCIA_DIAS = 7300   # "para siempre" en la práctica (~20 años) — respalda Mis compras

_TTS_URL = "https://api.openai.com/v1/audio/speech"
_VOZ = "fable"
VOCES = {"fable": "Voz de cuentacuentos", "nova": "Voz femenina cálida",
         "onyx": "Voz masculina profunda"}
_INSTRUCCIONES = (
    "Sos una cuentacuentos humana y cariñosa narrando un cuento infantil para dormir, "
    "en español rioplatense (argentino) neutro. Leé con muchísima calidez y expresión: "
    "variá la entonación, hacé pausas naturales en las comas y los puntos, subí y bajá el "
    "tono según la emoción de cada frase (ternura, sorpresa, alegría), y sonreí al hablar. "
    "Ritmo pausado y dulce, NUNCA monótono ni robótico, como una maestra jardinera "
    "leyéndole a un nene en la cama.")

# ElevenLabs: voz por default del audiolibro (más natural que OpenAI). Lizy es una voz
# nativa en español pensada para cuentos infantiles. La key se lee de config.json.
_EL_URL = "https://api.elevenlabs.io/v1/text-to-speech"
_EL_VOICE = "rrErIO88ehxTnspOjKvf"   # Lizy
_EL_MODEL = "eleven_multilingual_v2"
_EL_SETTINGS = {"stability": 0.30, "similarity_boost": 0.80,
                "style": 0.48, "use_speaker_boost": True, "speed": 1.15}
_EL_KEY_CACHE = {}


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


def _tts_elevenlabs(texto, timeout=120):
    key = _elevenlabs_key()
    if not key:
        return None
    body = json.dumps({"text": texto, "model_id": _EL_MODEL,
                       "voice_settings": _EL_SETTINGS}).encode()
    req = urllib.request.Request(
        "%s/%s?output_format=mp3_44100_128" % (_EL_URL, _EL_VOICE),
        data=body, method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _tts_openai(api_key, texto, timeout=120, voz=None):
    v = voz if voz in VOCES else _VOZ
    body = json.dumps({"model": "gpt-4o-mini-tts", "voice": v, "input": texto,
                       "response_format": "mp3",
                       "instructions": _INSTRUCCIONES}).encode()
    req = urllib.request.Request(_TTS_URL, data=body, method="POST", headers={
        "Authorization": "Bearer " + api_key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def tts_mp3(api_key, texto, timeout=120, voz=None):
    """MP3 de la narración de `texto`. Por default usa ElevenLabs (voz Lizy, nativa
    español para cuentos); si el cliente eligió una voz OpenAI (fable/nova/onyx) usa
    esa; y si ElevenLabs falla, cae a OpenAI (fable) como respaldo automático."""
    v = (str(voz or "").strip().lower())
    if v not in VOCES:                    # default o 'lizy' → ElevenLabs
        try:
            mp3 = _tts_elevenlabs(texto, timeout)
            if mp3:
                return mp3
        except Exception as e:
            print("[tts] ElevenLabs falló (%s) — respaldo OpenAI" % e, flush=True)
        v = _VOZ
    return _tts_openai(api_key, texto, timeout, v)


def _textos_narracion(data, tema):
    """Texto a narrar por página (0..9): portada, dedicatoria, 7 de historia, fin."""
    import libro
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    dedic = (str(data.get("dedicatoria") or "").strip()) or \
        "Que nunca dejes de soñar, de jugar y de creer en vos."
    cuerpo = libro.cuento(data, tema, catalogo=True)
    return (["La gran aventura de %s. Un cuento personalizado." % nombre,
             "Este cuento pertenece a %s. %s" % (nombre, dedic)]
            + cuerpo
            + ["Fin. ¡Hasta la próxima aventura, %s!" % nombre])


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


def estado(token):
    """'listo' si el audiolibro ya está generado, 'generando' si está en curso,
    None si el token no existe."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{8,32}", token or ""):
        return None
    d = os.path.join(AUDIOLIBROS_DIR, token)
    if os.path.isfile(os.path.join(d, "manifest.json")):
        return "listo"
    if os.path.isfile(_marca_gen(token)):
        return "generando"
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
                f.write(tts_mp3(api_key, textos[i], voz=voz))
    finally:
        if ctx:
            ctx.__exit__(None, None, None)
    with open(os.path.join(d, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"tema": tema, "nombre": data.get("nombre", ""),
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
    titulo = "La gran aventura de %s — audiolibro" % (reg.get("nombre") or "")
    return """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>%(titulo)s</title><style>
* { margin:0; padding:0; box-sizing:border-box; }
html,body { height:100%%; }
body { background:#2a2438; font-family:system-ui,sans-serif; overflow:hidden;
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:14px; }
#flip img { border-radius:6px; }
.controles { display:flex; gap:14px; align-items:center; flex-shrink:0; }
button { background:#6B5BD2; color:#fff; border:0; border-radius:50%%; width:54px; height:54px;
  font-size:22px; cursor:pointer; } button.sec { background:#453a66; width:44px; height:44px; font-size:15px; }
.pag { color:#b8aede; font-size:14px; min-width:52px; text-align:center; }
</style></head><body>
<div id="flip"></div>
<div class="controles">
  <button class="sec" id="prev">⏮</button>
  <button id="play">▶</button>
  <button class="sec" id="next">⏭</button>
  <span class="pag" id="pag">1 / %(n)d</span>
  <span style="color:#b8aede;font-size:16px">🐢</span>
  <input type="range" id="vel" min="0.7" max="1.4" step="0.05" value="1"
         style="width:110px;accent-color:#6B5BD2">
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
var availH = Math.max(300, window.innerHeight - 130);
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
    narrando=false; play.textContent='▶'; err('tocá ▶ de nuevo ('+e.name+')'); });
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
pag.textContent='1 / '+N;
</script></body></html>""" % {"titulo": e(titulo), "token": e(token),
                              "base": e(base_url), "n": n,
                              "v": int(reg.get("creado", 0))}
