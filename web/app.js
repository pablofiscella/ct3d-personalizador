/* Preview en vivo — replica el render de Pillow usando el MISMO spec.json.
   Canvas a resolucion real (1500x2100) mostrado escalado por CSS. */

let SPEC = null;
const IMAGES = {};

async function loadSpec() {
  SPEC = await (await fetch('spec.json?v=' + Date.now())).json();
}

function fontInfo(file) { return (SPEC.fonts && SPEC.fonts[file]) || { family: 'sans-serif', weight: 400 }; }
function rgb(c) { return `rgb(${c[0]},${c[1]},${c[2]})`; }

async function loadFonts() {
  const jobs = [];
  for (const [file, info] of Object.entries(SPEC.fonts || {})) {
    const desc = info.variable ? {} : { weight: String(info.weight || 400) };
    const ff = new FontFace(info.family, `url(fonts/${file})`, desc);
    jobs.push(ff.load().then(f => document.fonts.add(f)).catch(e => console.warn('font fail', file, e)));
  }
  await Promise.all(jobs);
  try { await document.fonts.ready; } catch (e) {}
}

async function loadImages() {
  const jobs = SPEC.art.map(layer => new Promise(res => {
    const im = new Image();
    im.onload = () => { IMAGES[layer.file] = im; res(); };
    im.onerror = () => { console.warn('img fail', layer.file); res(); };
    im.src = 'recortes/' + layer.file;
  }));
  await Promise.all(jobs);
}

function fitFont(ctx, text, family, weight, size, maxw) {
  let s = size;
  for (; s > 10; s -= 2) {
    ctx.font = `${weight} ${s}px "${family}"`;
    if (ctx.measureText(text).width <= maxw) return s;
  }
  return s;
}

function render(canvas, data) {
  const [W, H] = SPEC.size;
  canvas.width = W; canvas.height = H;
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = rgb(SPEC.bg);
  ctx.fillRect(0, 0, W, H);

  for (const layer of SPEC.art) {
    const im = IMAGES[layer.file];
    if (!im) continue;
    const tw = W * layer.w;
    const th = im.height * (tw / im.width);
    const px = W * layer.x, py = H * layer.y;
    const h = layer.anchor[0], v = layer.anchor[1];
    const ox = h === 'l' ? 0 : h === 'r' ? tw : tw / 2;
    const oy = v === 't' ? 0 : v === 'b' ? th : th / 2;
    ctx.drawImage(im, px - ox, py - oy, tw, th);
  }

  for (const fld of SPEC.text) {
    const text = fld.tpl.replace(/\{(\w+)\}/g, (m, k) => (data[k] != null ? data[k] : ''));
    if (!text.trim()) continue;
    const fi = fontInfo(fld.font);
    const weight = fld.wght || fi.weight || 400;
    const maxw = W * (fld.maxw || 0.9);
    const size = fitFont(ctx, text, fi.family, weight, fld.size, maxw);
    ctx.font = `${weight} ${size}px "${fi.family}"`;
    ctx.fillStyle = rgb(fld.color);
    ctx.textAlign = fld.anchor[0] === 'l' ? 'left' : fld.anchor[0] === 'r' ? 'right' : 'center';
    ctx.textBaseline = fld.anchor[1] === 't' ? 'top' : fld.anchor[1] === 'b' ? 'alphabetic' : 'middle';
    ctx.fillText(text, W * fld.x, H * fld.y);
  }
}

function currentData() {
  const d = {};
  for (const f of SPEC.form) {
    const el = document.getElementById('in_' + f.var);
    d[f.var] = el ? el.value : f.default;
  }
  return d;
}

function buildForm() {
  const form = document.getElementById('form');
  for (const f of SPEC.form) {
    const wrap = document.createElement('label');
    wrap.className = 'field';
    wrap.innerHTML = `<span>${f.label}</span>`;
    const inp = document.createElement('input');
    inp.id = 'in_' + f.var;
    inp.type = 'text';
    inp.value = f.default;
    inp.maxLength = 40;
    inp.addEventListener('input', update);
    wrap.appendChild(inp);
    form.appendChild(wrap);
  }
}

let canvas;
function update() { render(canvas, currentData()); }

function downloadPreview() {
  const a = document.createElement('a');
  a.download = 'vista_previa.png';
  a.href = canvas.toDataURL('image/png');
  a.click();
}

(async function init() {
  canvas = document.getElementById('preview');
  document.getElementById('status').textContent = 'Cargando…';
  await loadSpec();
  buildForm();
  await loadFonts();
  await loadImages();
  update();
  document.getElementById('status').textContent = '';
  document.getElementById('btnDownload').addEventListener('click', downloadPreview);
})();
