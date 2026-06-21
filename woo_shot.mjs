import { chromium } from 'playwright-core';
const b=await chromium.launch({executablePath:process.argv[2]});
const p=await b.newPage({viewport:{width:1300,height:1400},deviceScaleFactor:2});
const errs=[];p.on('console',m=>{if(m.type()==='error')errs.push(m.text().slice(0,120))});
await p.goto('https://casatridimensional.com.ar/producto/kit-imprimible-de-cumpleanos-un-anito-salvaje-safari/',{waitUntil:'networkidle',timeout:45000});
await p.waitForTimeout(2000);
// llenar los campos con los mismos datos del editor
const fill=async(id,v)=>{const el=await p.$('#'+id); if(el){await el.fill(v);}};
await fill('ct3d_nombre','Tomás'); await fill('ct3d_fecha','Sábado 12 de julio');
await fill('ct3d_hora','16:00 hs'); await fill('ct3d_lugar','Salón Los Robles');
await fill('ct3d_direccion','Av. Siempreviva 742'); await fill('ct3d_telefono','11-5555-5555');
await p.waitForTimeout(2500); // que el preview se actualice
const img=await p.$('#ct3d-preview-img');
if(img){ await img.scrollIntoViewIfNeeded(); await img.screenshot({path:'salida/woo_preview.png'});
  const src=await img.getAttribute('src'); console.log('IMG src:', src?src.slice(0,90):'(sin src)'); }
else console.log('NO encontré #ct3d-preview-img');
console.log('errores consola:', errs.length?errs.slice(0,3):'ninguno');
await b.close();
