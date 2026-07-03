# Spec: Mejoras de catálogo y sitio CT3D — julio 2026

**Objetivo:** maximizar ventas del catálogo digital con productos y features nuevos que cumplan el principio rector del negocio: **100% automatizable — cero tiempo de preparación por producto o por venta; Pablo solo configura parámetros.**

**Base:** investigación de mercado (jul-2026) — 73 hallazgos de 23 fuentes (Etsy, Mercado Libre AR, Cults3D, competidores argentinos, plataformas de edición, tendencias 2026). Confianza indicada por hallazgo: ✅ = verificado con triple voto adversarial; 📄 = extraído de fuente primaria con cita textual, sin verificación cruzada (la fase de verificación se cortó por límite de sesión).

---

## 1. Hallazgos clave que fundamentan este spec

### El modelo de entrega de CT3D es una VENTAJA, no una carencia
- 📄 Corjl (la plataforma de edición líder para sellers de Etsy) está **cerrada a nuevos vendedores** — relanzamiento "New Corjl", solo lista de espera. Templett cuesta USD ~102/mes a volumen medio; Corjl USD ~87/mes.
- 📄 Canva (la alternativa barata) no protege el diseño: cualquiera con el link accede sin comprar; y con Canva el vendedor adjunta el link a mano en cada venta.
- 📄 La edición móvil de Corjl/Templett es "muy básica" — y el mercado hispano compra/edita desde el celular.
- 📄 El competidor argentino directo (Cocojolie) usa el mismo modelo que CT3D: entrega generada personalizada, sin self-edit.
- 📄 La mediana de creación de una invitación es 22 días antes del evento y el 20% se crea a menos de 7 días → la entrega instantánea generada le gana a cualquier flujo con fricción.
- **Conclusión:** no adoptar Corjl/Templett/Canva. La entrega generada automática es el diferencial a comunicar ("lo recibís listo en minutos, sin editar nada, directo al WhatsApp").

### Dónde está la plata en el mercado hispano
- 📄 Cocojolie (AR) cobra su **invitación web interactiva** USD 12.42 (baby shower) a USD 24.84 (15 años) — **2-3x más** que la video-invitación MP4 (USD 7.20). Features: fotos, mapa del evento, countdown, opciones de regalo y **RSVP por WhatsApp**.
- 📄 Los datos de RSVP digital (InviteDrop): 92% de aceptación, 25% responde en la primera hora, 44% agrega acompañantes (+1.2 invitados promedio) → el RSVP resuelve un dolor real del organizador.
- 📄 Competidores hispanos regalan video-invitaciones básicas gratis (invitajass) → **no competir en invitación suelta simple**; diferenciarse en el paquete completo automatizado.
- 📄 En ML Argentina, los imprimibles más vendidos de 2024 fueron **calendarios editables** (3 de los 5 tops del blog oficial de ML) — CT3D ya tiene motor de calendario.
- 📄 Las búsquedas long-tail de ML incluyen nichos adultos (cumpleaños 18/70, jubilación, despedidas, día del amigo) y cultura pop (Roblox, PSG) — hay demanda fuera de lo infantil.

### Libros infantiles personalizados: el producto premium del rubro
- 📄 Mercado global de USD 730M (2026) → USD 1.500M (2035). Wonderbly/Hooray Heroes venden a **USD 20-45 por libro**.
- 📄 La consistencia de personaje entre ilustraciones (el bloqueo técnico histórico) está resuelta en 2026 con imágenes de referencia — la misma técnica que ya usa el `ia_kit` de CT3D con la imagen maestra por tema.

### STL de fiesta: nicho menor, jugarlo como complemento
- ✅ Los best-sellers históricos de Cults3D son juguetes flexi print-in-place (35 de los top 50); **ningún** topper/medalla/trofeo/cortante en el top 50.
- ✅ El STL individual es ticket bajo: USD 2-4.70 típico; se monetiza por volumen y sets.
- ✅ La categoría cortantes tiene 86.900 archivos → demanda masiva pero saturación.
- ✅ Los títulos ganadores venden facilidad: "Print-in-Place", "No Supports", 3MF incluido, versiones XL.
- 📄 Cults3D paga 80% sin exclusividad → canal de distribución extra sin costo.
- 📄 Fotos de impresiones REALES (no renders) y medidas en el título son práctica estándar de fichas que convierten.
- **Conclusión:** el catálogo STL recién creado queda como complemento/upsell del kit, no como apuesta central. Sumar el canal Cults3D y mejorar fichas.

### Temáticas y estacionalidad 2026
- 📄 **Mundial de fútbol 2026** = LA oportunidad estacional del año para Argentina.
- 📄 Tendencias infantiles: Bluey (2-4 años), Toy Story 5 (estreno jun-2026), safari vigente para primer año ("Wild One").
- 📄 Formatos por edad/hito venden: "Winter ONEderland" (1 año), "Oh TWOdles" (2 años) — dos de los top 10 de Etsy.
- 📄 Baby shower 2026: osito ("we can bearly wait") y nubes ya están en el catálogo CT3D y aparecen en las tendencias; faltan abeja, bosque encantado, vaquero/a, flores ("baby in bloom"), y paletas tierra además del pastel.
- 📄 Los personajes licenciados (Mickey, Toy Story) dominan ventas en Etsy **pese al riesgo legal** — CT3D mantiene la política de equivalentes genéricos (perros cartoon estilo Bluey, juguetes espaciales estilo Toy Story) sin marcas.
- 📄 Refrescar títulos por año/temporada ("Calendario 2027", "edición Mundial") sostiene ventas.

### Modelos de catálogo que escalan
- 📄 La tienda #1 de Etsy en la categoría (MintyPaperieShop: 329.000 ventas, ~USD 8,9 de ticket promedio) escala por **catálogo masivo de variantes** (4.879 listings) — exactamente lo que un motor generativo produce gratis.
- 📄 El modelo alternativo (marrygrams: 189 listings, 2.000 ventas/mes) es curación de alta rotación. CT3D puede hacer ambos: catálogo ancho generado + destacados curados.

---

## 2. Productos nuevos (orden de prioridad)

### P1a — Invitación web interactiva con RSVP por WhatsApp
**Qué es:** una página web personalizada por evento (no un PDF): arte del tema + nombre/edad + fecha + countdown regresivo + mapa (link a Google Maps) + botón "Confirmar asistencia" que abre WhatsApp con mensaje precargado hacia el organizador. El comprador la comparte por WhatsApp como link.

**Por qué:** es el formato que el competidor argentino cobra 2-3x más que cualquier otro (USD 12-25). El RSVP resuelve el dolor real nº1 del organizador (saber cuántos vienen). Nadie más lo tiene automatizado de punta a punta.

**Automatización:** 100%. Es una plantilla HTML servida por la tienda Flask con los mismos datos que ya pide el kit (nombre/edad/fecha/hora/lugar) + assets del tema. Cero trabajo por venta. La página vive en `casatridimensional.com.ar/invitacion/<token>` con vigencia de N meses.

**Alcance técnico:** template Jinja en la tienda + tabla de invitaciones (token, datos, tema, vencimiento) + contador de confirmaciones visible para el comprador (página "admin" con su token). El RSVP por WhatsApp es un link `wa.me/<tel-organizador>?text=...` — sin backend de mensajería propio.

**Precio sugerido:** $8.000-12.000 ARS (vs kit $9.500). Bundle "Kit + Invitación interactiva" con descuento.

### P1b — Cuento infantil personalizado ilustrado (producto premium)
**Qué es:** libro PDF de 12-16 páginas: "La gran aventura de {NOMBRE}" con el personaje del tema como coprotagonista. Texto por plantilla (escrito una vez por temática, con nombre/edad intercalados), ilustraciones generadas por `ia_kit` (gpt-image-2) usando la imagen maestra del tema como referencia de consistencia, armado Pillow → PDF.

**Por qué:** el producto de mayor valor percibido del rubro (USD 20-45 afuera). Diferencial total en el mercado hispano. Reusa el 90% de infraestructura existente (jobs async, aprobación, generación con referencia).

**Automatización:** 100% por venta (generación async ~10-20 min, entrega por link al estar listo — el flujo de jobs IA ya existe). Preparación por temática: 1 plantilla de historia (una vez, la escribe la IA de texto y Pablo aprueba desde el panel — mismo patrón que el panel IA actual).

**Precio sugerido:** $15.000-25.000 ARS digital. Variante física por impresión bajo demanda queda para fase posterior.

**Riesgo a validar primero:** consistencia real del personaje a lo largo de 15 ilustraciones con gpt-image-2 — hacer un smoke test de 1 cuento completo antes de construir el producto entero.

### P1c — Calendario como producto estrella estacional
**Qué es:** el motor de calendario ya existe (editor visual incluido). Falta productizarlo como lo que ML dice que más se vende: producto "Calendario 2027 personalizado" destacado, refrescado cada año, con variantes por temática.

**Automatización:** ya está hecha — es trabajo de catálogo: crear los productos por tema, título con el año, y un cron anual que genere la campaña del año siguiente (agosto-septiembre es temporada de compra de calendarios del año próximo).

### P2a — Segmentación por edad/hito
**Qué es:** variantes de título/copy de los productos existentes por edad: "Safari — Primer añito (Wild One)", "Dos años — Oh, TWOdles", etc. El motor ya personaliza por edad; esto es exponerlo como productos/landing distintos para capturar long-tail SEO ("kit imprimible primer añito safari").

**Automatización:** 100% — son filas nuevas de producto (`KIT-SAFARI-1ANITO`) con el mismo motor. Generables por script.

### P2b — Temáticas nuevas de tendencia (todas con arte generable por `ia_kit`)
1. **Fútbol/Mundial 2026** — la oportunidad del año en Argentina. Genérico (sin escudos ni marcas).
2. **Perritos cartoon** (estilo Bluey genérico) — franja 2-4 años.
3. **Juguetes espaciales** (estilo Toy Story genérico) — colgarse del estreno jun-2026.
4. **Baby shower:** abeja ("una dulzura en camino"), bosque encantado, vaquero/a, flores; variantes de paleta tierra además del pastel.

**Automatización:** el pipeline de alta de temática ya existe (panel + `ia_kit` genera el arte). Cada tema nuevo habilita TODO el catálogo (kit + 15 tipos + 5 STL + interactiva + cuento) de una.

### P2c — Video-invitación WhatsApp (tier de entrada)
**Qué es:** MP4 animado de 15-30s con el arte del tema + nombre + datos, para mandar por WhatsApp. Es el tier barato (USD ~7 en la competencia) que alimenta el funnel hacia el kit completo y la interactiva.

**Automatización:** 100% — animación programática (Pillow/ffmpeg: zoom/pan de assets + texto animado, música libre). NO usar IA de video por venta (costo/latencia); plantilla de animación por código, assets por tema.

---

## 3. Mejoras del sitio (tienda Flask)

### S1 — Bundles con descuento (mayor impacto/esfuerzo)
"Fiesta completa": Kit imprimible + Pack Cumple 3D + Invitación interactiva a precio paquete. La investigación muestra que las tiendas top monetizan por volumen/bundle. Implementación: tipo de producto "bundle" que referencia otros tipos, un solo checkout, genera todo junto.

### S2 — Fichas de producto (patrón de los que venden)
- **STL:** fotos de impresiones reales (pedirle a Pablo 1 sesión de fotos de las piezas impresas — única tarea manual, se hace una vez), medidas en el título ("Medalla 60mm"), copy "sin soportes / lista para imprimir", y visor 3D interactivo en el browser (three.js STLLoader — los STL ya están generados).
- **Todos:** título long-tail con ocasión+edad+temática; galería "qué incluye" (ya existe); sello "Entrega automática en minutos" como diferencial vs edición manual.

### S3 — SEO long-tail programático
Landing por combinación temática × edad × ocasión generadas del catálogo (ej. `/kit-imprimible/safari/primer-anito`). El contenido sale del motor (previews + copy por plantilla). Las búsquedas de ML muestran demanda long-tail fuerte (nichos adultos incluidos — evaluar temáticas 18/30/40 años, jubilación, despedida como fase posterior).

### S4 — Estacionalidad automatizada
Cron de temporada: agosto → destacar calendarios del año siguiente; mayo-jun 2026 → banner Mundial + Toy-Story-like; fechas patrias/día del niño. Definir el calendario comercial una vez; el sistema rota banners/destacados solo.

### S5 — Canal Cults3D para los STL
Subir el catálogo STL (versión genérica "NOMBRE" o piezas sin texto) a Cults3D con 80% de payout, sin exclusividad, como canal de descubrimiento + link a la tienda para la versión personalizada. Los modelos gratis estacionales (cortante navideño gratis) como imán de tráfico — táctica confirmada del marketplace.

---

## 4. Qué NO hacer (decisiones explícitas)
1. **No** adoptar Corjl/Templett/Canva — cerrado/caro/inseguro respectivamente; la entrega generada es mejor y ya está construida.
2. **No** competir en invitación digital suelta básica — hay quien la regala; venderla solo como parte de bundles o tier de entrada al funnel.
3. **No** usar personajes/marcas licenciadas (Bluey/Toy Story/Mickey reales) — riesgo legal explícito; siempre equivalentes genéricos propios.
4. **No** apostar el crecimiento al STL de fiesta — nicho menor confirmado; es complemento y upsell.
5. **No** IA de video por venta en la video-invitación — costo y latencia; animación por código.
6. **Etsy en inglés: postergado** — el modelo encaja (la fricción de Canva/Corjl es real y Corjl está cerrado), pero exige localizar todo el catálogo y soporte en inglés; reevaluar cuando P1 esté rindiendo.

## 5. Roadmap sugerido
| Fase | Qué | Por qué primero |
|---|---|---|
| 1 (ya) | Activar catálogo STL oculto (precios) + S2 fichas STL | Ya está construido, solo falta encender |
| 2 | P1a Invitación interactiva + S1 bundles | Mayor precio/margen validado localmente, 100% con stack actual |
| 3 | P1c Calendarios 2027 (agosto) + P2b temática Mundial | Ventanas estacionales con fecha límite |
| 4 | P1b Cuento personalizado (smoke test primero) | Producto premium, mayor upside, algo más de obra |
| 5 | P2a segmentación edad + S3 SEO + P2c video-invitación | Volumen long-tail sobre lo ya construido |

## 6. Criterio de éxito
Cada ítem cumple: (a) cero minutos de Pablo por venta; (b) alta por temática = solo parámetros/aprobación en panel; (c) precio y formato respaldados por al menos un hallazgo de la investigación citado arriba.
