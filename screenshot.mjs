import { chromium } from 'playwright-core';
const exe = process.argv[2];
const name = process.argv[3] || 'Tomás';
const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1200, height: 1400 }, deviceScaleFactor: 2 });
const errs = [];
page.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
page.on('pageerror', e => errs.push('PAGEERROR: '+e.message));
await page.goto('http://localhost:8099/index.html', { waitUntil: 'networkidle' });
await page.waitForTimeout(1200);
// cambiar el nombre para probar el live-update
await page.fill('#in_nombre', name);
await page.fill('#in_lugar', 'Jardín La Pradera');
await page.waitForTimeout(600);
await page.screenshot({ path: 'salida/preview_full.png', fullPage: true });
const c = await page.$('#preview');
await c.screenshot({ path: 'salida/preview_canvas.png' });
console.log('errores consola:', errs.length ? errs : 'ninguno');
await browser.close();
