import { chromium } from 'playwright-core';
const b=await chromium.launch({executablePath:process.argv[2]});
const p=await b.newPage({viewport:{width:900,height:1300},deviceScaleFactor:2});
await p.goto('http://localhost:8787/editor?key='+process.argv[3],{waitUntil:'networkidle'});
await p.waitForTimeout(1800);
const cv=await p.$('#cv'); const box=await cv.boundingBox();
await p.screenshot({path:'salida/editor_tel.png', clip:{x:box.x, y:box.y+box.height*0.93, width:box.width, height:box.height*0.07}});
console.log('ok');
await b.close();
