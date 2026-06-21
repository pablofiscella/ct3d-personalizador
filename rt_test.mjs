import { chromium } from 'playwright-core';
const b=await chromium.launch({executablePath:process.argv[2]});
const p=await b.newPage();
p.on('pageerror',e=>console.log('PAGEERROR',e.message));
await p.goto('http://localhost:8787/editor?key='+process.argv[3],{waitUntil:'networkidle'});
await p.waitForTimeout(2000);
// mover el telefono a y=0.95, x=0.40 vía la API interna del editor
const set=await p.evaluate(()=>{
  select('rsvp'); sel.x=0.40; sel.y=0.95; sel.size=50; draw();
  return {x:sel.x,y:sel.y,size:sel.size};
});
console.log('seteado en editor:', JSON.stringify(set));
await p.click('#save');
await p.waitForTimeout(800);
await b.close();
