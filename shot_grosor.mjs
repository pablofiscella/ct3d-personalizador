import { chromium } from 'playwright-core';
const b=await chromium.launch({executablePath:process.argv[2]});
const p=await b.newPage({viewport:{width:900,height:1200},deviceScaleFactor:2});
await p.goto('http://localhost:8787/editor?key='+process.argv[3],{waitUntil:'networkidle'});
await p.waitForTimeout(1500);
// seleccionar el chip "Fecha"
await p.click('text=Fecha');
await p.waitForTimeout(300);
// poner grosor 700
await p.$eval('#wght', el=>{el.value=700; el.dispatchEvent(new Event('input'));});
await p.waitForTimeout(600);
const cv=await p.$('#cv');
const box=await cv.boundingBox();
await p.screenshot({path:'salida/grosor_700.png', clip:{x:box.x, y:box.y+box.height*0.45, width:box.width, height:box.height*0.20}});
console.log('listo');
await b.close();
