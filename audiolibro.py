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
_INSTRUCCIONES = ("Narradora cálida de cuentos infantiles, en español rioplatense, "
                  "ritmo pausado y expresivo, como leyéndole a un chico antes de dormir.")


def tts_mp3(api_key, texto, timeout=120):
    """MP3 de la narración de `texto` (OpenAI TTS)."""
    body = json.dumps({"model": "gpt-4o-mini-tts", "voice": _VOZ, "input": texto,
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
                f.write(tts_mp3(api_key, textos[i]))
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
body { background:#2a2438; font-family:system-ui,sans-serif; min-height:100vh;
  display:flex; flex-direction:column; align-items:center; justify-content:center; }
.escenario { perspective:1600px; width:min(92vw, 62vh); }
.hoja { width:100%%; border-radius:12px; box-shadow:0 18px 60px rgba(0,0,0,.5);
  display:block; transform-origin:left center; backface-visibility:hidden; }
.girando { animation:curl .9s cubic-bezier(.4,.1,.3,1); }
@keyframes curl {
  0%%   { transform:rotateY(0) skewY(0); border-radius:12px; filter:brightness(1); }
  35%%  { transform:rotateY(-24deg) skewY(-1.5deg); border-top-right-radius:70px;
          border-bottom-right-radius:40px; filter:brightness(.92);
          box-shadow:-30px 18px 50px rgba(0,0,0,.45); }
  60%%  { transform:rotateY(-10deg) skewY(-.5deg); border-top-right-radius:26px;
          filter:brightness(.97); }
  100%% { transform:rotateY(0) skewY(0); border-radius:12px; filter:brightness(1); }
}
.controles { display:flex; gap:14px; margin-top:18px; align-items:center; }
button { background:#6B5BD2; color:#fff; border:0; border-radius:50%%; width:56px; height:56px;
  font-size:22px; cursor:pointer; } button.sec { background:#453a66; width:46px; height:46px; font-size:16px; }
.pag { color:#b8aede; font-size:14px; min-width:52px; text-align:center; }
</style></head><body>
<div class="escenario"><img id="hoja" class="hoja" src="%(base)s/al/%(token)s/pag_00.jpg"></div>
<div class="controles">
  <button class="sec" id="prev">⏮</button>
  <button id="play">▶</button>
  <button class="sec" id="next">⏭</button>
  <span class="pag" id="pag">1 / %(n)d</span>
</div>
<audio id="audio" preload="auto"></audio>
<script>
var N=%(n)d, i=0, base="%(base)s/al/%(token)s/";
var hoja=document.getElementById('hoja'), audio=document.getElementById('audio');
var play=document.getElementById('play'), pag=document.getElementById('pag');
function pad(x){return ('0'+x).slice(-2);}
function cargar(k, auto){
  i=Math.max(0, Math.min(N-1, k));
  hoja.classList.remove('girando'); void hoja.offsetWidth; hoja.classList.add('girando');
  setTimeout(function(){ hoja.src=base+'pag_'+pad(i)+'.jpg'; }, 380);
  audio.src=base+'pag_'+pad(i)+'.mp3';
  pag.textContent=(i+1)+' / '+N;
  if(auto){ audio.play(); play.textContent='⏸'; }
}
audio.onended=function(){ if(i<N-1){ cargar(i+1, true); } else { play.textContent='▶'; } };
play.onclick=function(){
  if(audio.paused){ if(!audio.src) cargar(0,true); else audio.play(); play.textContent='⏸'; }
  else { audio.pause(); play.textContent='▶'; }
};
document.getElementById('prev').onclick=function(){ cargar(i-1, !audio.paused); };
document.getElementById('next').onclick=function(){ cargar(i+1, !audio.paused); };
cargar(0, false);
</script></body></html>""" % {"titulo": e(titulo), "token": e(token),
                              "base": e(base_url), "n": n}
