import { chromium } from 'playwright-core';
const b=await chromium.launch({executablePath:process.argv[2]});
const p=await b.newPage({viewport:{width:1300,height:1000},deviceScaleFactor:1.5});
const errs=[];p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});p.on('pageerror',e=>errs.push('PE:'+e.message));
await p.goto('http://localhost:8787/editor?key='+process.argv[3],{waitUntil:'networkidle'});
await p.waitForTimeout(1500);
await p.screenshot({path:'salida/editor_shot.png',fullPage:true});
console.log('errores:',errs.length?errs:'ninguno');
await b.close();
