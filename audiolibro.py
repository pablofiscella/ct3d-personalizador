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
VIGENCIA_DIAS = 365

_TTS_URL = "https://api.openai.com/v1/audio/speech"
_VOZ = "nova"
VOCES = {"nova": "Voz femenina cálida", "onyx": "Voz masculina profunda",
         "fable": "Voz de cuentacuentos"}
_INSTRUCCIONES = ("Narradora cálida de cuentos infantiles, en español rioplatense, "
                  "ritmo pausado y expresivo, como leyéndole a un chico antes de dormir.")


def tts_mp3(api_key, texto, timeout=120, voz=None):
    """MP3 de la narración de `texto` (OpenAI TTS)."""
    v = voz if voz in VOCES else _VOZ
    body = json.dumps({"model": "gpt-4o-mini-tts", "voice": v, "input": texto,
                       "response_format": "mp3",
                       "instructions": _INSTRUCCIONES}).encode()
    req = urllib.request.Request(_TTS_URL, data=body, method="POST", headers={
        "Authorization": "Bearer " + api_key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _textos_narracion(data, tema):
    """Texto a narrar por página (0..9): portada, dedicatoria, 7 de historia, fin."""
    import libro
    nombre = (str(data.get("nombre") or "").strip()) or "Alex"
    dedic = (str(data.get("dedicatoria") or "").strip()) or \
        "Que nunca dejes de soñar, de jugar y de creer en vos."
    cuerpo = libro.cuento(data, tema)
    return (["La gran aventura de %s. Un cuento personalizado." % nombre,
             "Este cuento pertenece a %s. %s" % (nombre, dedic)]
            + cuerpo
            + ["Fin. ¡Hasta la próxima aventura, %s!" % nombre])


def crear(data, tema, api_key, escenas_dir=None, progress=None):
    voz = (str(data.get("voz") or "").strip().lower()) or None
    """Genera páginas JPG + narración MP3 + manifest. Devuelve el token del link."""
    import libro
    token = secrets.token_urlsafe(12)
    d = os.path.join(AUDIOLIBROS_DIR, token)
    os.makedirs(d, exist_ok=True)
    textos = _textos_narracion(data, tema)
    ctx = libro.usar_escenas_dir(escenas_dir) if escenas_dir else \
          libro.usar_genero(data.get("genero"))
    try:
        if ctx:
            ctx.__enter__()
        for i in range(libro.TOTAL_PAGINAS):
            if progress:
                progress("Página %d de %d…" % (i + 1, libro.TOTAL_PAGINAS))
            img = libro.pagina_libro(i, data, tema).convert("RGB")
            img.resize((img.width * 2 // 3, img.height * 2 // 3)).save(
                os.path.join(d, "pag_%02d.jpg" % i), quality=86)
            with open(os.path.join(d, "pag_%02d.mp3" % i), "wb") as f:
                f.write(tts_mp3(api_key, textos[i], voz=voz))
    finally:
        if ctx:
            ctx.__exit__(None, None, None)
    with open(os.path.join(d, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"tema": tema, "nombre": data.get("nombre", ""),
                   "paginas": libro.TOTAL_PAGINAS, "creado": int(time.time())},
                  f, ensure_ascii=False)
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
  <select id="vel" style="background:#453a66;color:#fff;border:0;border-radius:8px;padding:8px">
    <option value="0.8">🐢 lenta</option><option value="1" selected>normal</option>
    <option value="1.25">🐇 rápida</option></select>
</div>
<div id="diag" style="color:#e0b0b0;font-size:12px;min-height:16px"></div>
<audio id="audio" preload="auto"></audio>
<script src="https://unpkg.com/page-flip@2.0.7/dist/js/page-flip.browser.js"></script>
<script>
var N=%(n)d, base="%(base)s/al/%(token)s/";
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
  var urls=[]; for(var k=0;k<N;k++) urls.push(base+'pag_'+pad(k)+'.jpg');
  flip.loadFromImages(urls);
  flip.on('flip', function(e){ actual=e.data; pag.textContent=(actual+1)+' / '+N;
    if(narrando) reproducir(actual); });
} catch(ex) { err('visor: '+ex.message); }
function reproducir(i){
  actual=i; pag.textContent=(i+1)+' / '+N;
  audio.src = base+'pag_'+pad(i)+'.mp3';
  audio.playbackRate = parseFloat(vel.value);
  audio.load();
  var p = audio.play();
  if (p && p.catch) p.catch(function(e){
    narrando=false; play.textContent='▶'; err('tocá ▶ de nuevo ('+e.name+')'); });
}
audio.addEventListener('ended', function(){
  if (!narrando) return;
  if (actual < N-1) { if(flip){ flip.flipNext(); } else { reproducir(actual+1); } }
  else { narrando=false; play.textContent='▶'; }
});
vel.onchange = function(){ audio.playbackRate = parseFloat(vel.value); };
play.onclick = function(){
  if (narrando) { narrando=false; audio.pause(); play.textContent='▶'; return; }
  narrando=true; play.textContent='⏸'; err('');
  reproducir(actual);
};
document.getElementById('prev').onclick = function(){ if(flip) flip.flipPrev(); };
document.getElementById('next').onclick = function(){ if(flip) flip.flipNext(); };
pag.textContent='1 / '+N;
</script></body></html>""" % {"titulo": e(titulo), "token": e(token),
                              "base": e(base_url), "n": n}
