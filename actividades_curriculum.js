/* Actividades del catálogo CURRICULAR — GENERADO por gen_curriculum.py.
   No editar a mano: la fuente es actividades_curriculum.py (una actividad = una
   entrada de datos, con el contenido del DC y el documento del que salió).
   Se carga DESPUÉS de player.js porque registra sobre GAMES. */

/* 1° · ¿De qué está hecho? — objeto_material
   DC: Los objetos y los materiales: de qué está hecho, qué propiedad lo hace servir para eso
   Fuente: docs/auditoria-dc-caba/grado-1.md · C4 */
const CUR_OBJETO_MATERIAL_BANCO = [
  {
    "q": "¿De qué material es una ventana?",
    "ops": [
      "Vidrio",
      "Madera",
      "Tela"
    ],
    "m": "La ventana es de vidrio: deja pasar la luz y por eso se ve a través."
  },
  {
    "q": "¿De qué material es un buzo de invierno?",
    "ops": [
      "Lana",
      "Vidrio",
      "Metal"
    ],
    "m": "El buzo es de lana: abriga porque no deja escapar el calor del cuerpo."
  },
  {
    "q": "¿De qué material es una cuchara para revolver la sopa caliente?",
    "ops": [
      "Madera",
      "Papel",
      "Tela"
    ],
    "m": "De madera: no se calienta tanto como el metal y no se moja como el papel."
  },
  {
    "q": "¿Por qué las botellas son de plástico o vidrio y no de papel?",
    "ops": [
      "Porque el papel se moja y se rompe",
      "Porque el papel es caro",
      "Porque el papel es pesado"
    ],
    "m": "El papel absorbe el agua y se deshace: no sirve para guardar líquidos."
  },
  {
    "q": "Dos vasos iguales: uno se cayó y se rompió en pedazos. ¿De qué era?",
    "ops": [
      "De vidrio",
      "De plástico",
      "De goma"
    ],
    "m": "El vidrio es frágil: se rompe al golpearse. El plástico y la goma no."
  },
  {
    "q": "¿Qué propiedad tiene que tener un paraguas?",
    "ops": [
      "Que no deje pasar el agua",
      "Que sea transparente",
      "Que sea pesado"
    ],
    "m": "El paraguas tiene que ser impermeable: que el agua no lo atraviese."
  },
  {
    "q": "¿De qué material es una llave?",
    "ops": [
      "Metal",
      "Cartón",
      "Lana"
    ],
    "m": "De metal: es duro y resistente, no se dobla al girarlo en la cerradura."
  },
  {
    "q": "¿Por qué las ollas tienen el mango de plástico o madera?",
    "ops": [
      "Para no quemarse la mano",
      "Para que sean más lindas",
      "Para que pesen menos"
    ],
    "m": "El metal pasa el calor muy rápido; el plástico y la madera no, así que el mango no quema."
  },
  {
    "q": "¿Qué material se estira y vuelve a su forma?",
    "ops": [
      "La goma",
      "El vidrio",
      "La piedra"
    ],
    "m": "La goma es elástica: se estira y vuelve. El vidrio y la piedra no."
  },
  {
    "q": "¿De qué material es un globo?",
    "ops": [
      "Goma",
      "Papel",
      "Metal"
    ],
    "m": "De goma: se estira cuando entra el aire sin romperse."
  },
  {
    "q": "¿Por qué los libros son de papel y no de tela?",
    "ops": [
      "Porque en el papel se puede escribir e imprimir bien",
      "Porque el papel abriga",
      "Porque el papel no se moja"
    ],
    "m": "En el papel la tinta queda nítida; en la tela se correría."
  },
  {
    "q": "¿Qué material dejaría pasar la luz?",
    "ops": [
      "El vidrio",
      "La madera",
      "El metal"
    ],
    "m": "El vidrio es transparente: deja pasar la luz. La madera y el metal no."
  },
  {
    "q": "¿De qué material conviene una bolsa para llevar cosas pesadas?",
    "ops": [
      "Tela gruesa",
      "Papel de servilleta",
      "Papel de diario"
    ],
    "m": "La tela gruesa resiste el peso; los papeles finos se rompen."
  },
  {
    "q": "¿Por qué las sillas de plaza suelen ser de metal o plástico?",
    "ops": [
      "Porque aguantan la lluvia y el sol",
      "Porque son transparentes",
      "Porque son blandas"
    ],
    "m": "Están a la intemperie: el metal y el plástico resisten el agua; el cartón se arruinaría."
  }
];
GAMES.objeto_material = juegoTriviaTexto(CUR_OBJETO_MATERIAL_BANCO, "Elegí la respuesta correcta.", "objeto_mat");

/* 2° · ¿Tiene luz propia? — luz_propia
   DC: Fuentes lumínicas vs. objetos que no emiten luz. Tres categorías: emite / refleja / no se ve sin luz
   Fuente: docs/auditoria-dc-caba/grado-2.md · C2 */
const CUR_LUZ_PROPIA_BANCO = [
  {
    "q": "El Sol, ¿tiene luz propia o refleja?",
    "ops": [
      "Tiene luz propia",
      "Refleja la luz",
      "No se ve sin luz"
    ],
    "m": "El Sol es una estrella: produce su propia luz."
  },
  {
    "q": "La Luna, ¿tiene luz propia o refleja?",
    "ops": [
      "Refleja la luz del Sol",
      "Tiene luz propia",
      "No se ve nunca"
    ],
    "m": "La Luna no produce luz: se ve porque el Sol la ilumina y ella refleja."
  },
  {
    "q": "Un espejo en una pieza a oscuras, ¿se ve?",
    "ops": [
      "No, porque no tiene luz propia",
      "Sí, porque brilla solo",
      "Sí, porque tiene luz adentro"
    ],
    "m": "El espejo refleja la luz que le llega; sin luz no refleja nada."
  },
  {
    "q": "Una vela encendida…",
    "ops": [
      "Tiene luz propia",
      "Refleja la luz del Sol",
      "No se ve sin luz"
    ],
    "m": "La llama produce luz: es una fuente lumínica."
  },
  {
    "q": "Una lamparita apagada, ¿tiene luz propia?",
    "ops": [
      "No, sólo cuando está encendida",
      "Sí, siempre",
      "Sí, porque es de vidrio"
    ],
    "m": "La lamparita es fuente de luz sólo cuando está encendida."
  },
  {
    "q": "Una luciérnaga…",
    "ops": [
      "Tiene luz propia",
      "Refleja la luz",
      "No se ve de noche"
    ],
    "m": "La luciérnaga produce su propia luz: es un ser vivo luminoso."
  },
  {
    "q": "Un cartel reflectante en la ruta, de noche…",
    "ops": [
      "Refleja la luz de los autos",
      "Tiene luz propia",
      "No se ve nunca"
    ],
    "m": "No produce luz: devuelve la de los faros, por eso se ve tanto."
  },
  {
    "q": "La pantalla del celular encendida…",
    "ops": [
      "Tiene luz propia",
      "Refleja la luz del ambiente",
      "No se ve en la oscuridad"
    ],
    "m": "La pantalla emite su propia luz; por eso se ve a oscuras."
  },
  {
    "q": "Una manzana arriba de la mesa, de noche y sin luz…",
    "ops": [
      "No se ve, porque no tiene luz propia",
      "Se ve igual",
      "Tiene luz propia"
    ],
    "m": "La manzana sólo se ve cuando algo la ilumina."
  },
  {
    "q": "Las estrellas del cielo…",
    "ops": [
      "Tienen luz propia",
      "Reflejan la luz de la Luna",
      "No se ven nunca"
    ],
    "m": "Cada estrella produce su propia luz, como el Sol."
  },
  {
    "q": "El fuego de una fogata…",
    "ops": [
      "Tiene luz propia",
      "Refleja la luz",
      "No calienta"
    ],
    "m": "El fuego produce luz y calor: es una fuente lumínica."
  },
  {
    "q": "Un vidrio de ventana de día, ¿por qué se ve?",
    "ops": [
      "Porque el Sol lo ilumina",
      "Porque tiene luz propia",
      "Porque es de metal"
    ],
    "m": "El vidrio no emite luz: lo vemos porque la luz del Sol lo atraviesa e ilumina."
  },
  {
    "q": "Una linterna prendida…",
    "ops": [
      "Tiene luz propia",
      "Refleja la luz de la Luna",
      "No se ve de noche"
    ],
    "m": "La linterna produce luz: por eso sirve para alumbrar."
  },
  {
    "q": "El agua de una pileta con sol, ¿brilla porque tiene luz propia?",
    "ops": [
      "No, refleja la luz del Sol",
      "Sí, tiene luz propia",
      "Sí, porque está fría"
    ],
    "m": "El agua refleja la luz del Sol; no la produce."
  }
];
GAMES.luz_propia = juegoTriviaTexto(CUR_LUZ_PROPIA_BANCO, "Elegí la respuesta correcta.", "luz_propia");

/* 3° · ¿Se respeta el derecho? — derechos_escenarios
   DC: Derechos de niños y niñas, también en entornos digitales; diálogo y consenso frente al conflicto
   Fuente: docs/auditoria-dc-caba/grado-3.md · C10 */
const CUR_DERECHOS_ESCENARIOS_BANCO = [
  {
    "q": "En la escuela dejan a un chico afuera del juego por cómo habla. ¿Qué derecho no se respeta?",
    "ops": [
      "A no ser discriminado",
      "A tener juguetes nuevos",
      "A elegir la maestra"
    ],
    "m": "Excluir a alguien por cómo habla, cómo es o de dónde viene es discriminación."
  },
  {
    "q": "Una nena de 8 años trabaja todo el día y no va a la escuela. ¿Qué derecho no se respeta?",
    "ops": [
      "A la educación",
      "A tener una mascota",
      "A mirar televisión"
    ],
    "m": "Todos los chicos tienen derecho a ir a la escuela; el trabajo infantil lo impide."
  },
  {
    "q": "Un chico se enferma y lo atienden en el hospital sin pagar. ¿Qué derecho se está cumpliendo?",
    "ops": [
      "A la salud",
      "A la vivienda",
      "Al juego"
    ],
    "m": "La atención de la salud es un derecho, no un favor."
  },
  {
    "q": "En el recreo nadie deja jugar a los más chicos. ¿Qué está en juego?",
    "ops": [
      "El derecho al juego",
      "El derecho a la vivienda",
      "El derecho a votar"
    ],
    "m": "Jugar es un derecho de la infancia, no un premio."
  },
  {
    "q": "Alguien sube a internet una foto tuya sin permiso. ¿Qué derecho no se respeta?",
    "ops": [
      "A la privacidad, también en internet",
      "A tener celular propio",
      "A jugar en línea"
    ],
    "m": "Los derechos valen igual en el mundo digital: tu imagen es tuya."
  },
  {
    "q": "Dos chicos se pelean por una pelota. ¿Cuál es la mejor salida?",
    "ops": [
      "Hablar y acordar turnos",
      "Que gane el más fuerte",
      "Esconder la pelota"
    ],
    "m": "El diálogo y el acuerdo resuelven el conflicto; la fuerza sólo lo tapa."
  },
  {
    "q": "En una reunión de grado no dejan opinar a los chicos. ¿Qué derecho no se respeta?",
    "ops": [
      "A ser escuchado",
      "A llegar tarde",
      "A no ir a la escuela"
    ],
    "m": "Los chicos tienen derecho a dar su opinión sobre lo que les afecta."
  },
  {
    "q": "Un chico no tiene dónde vivir. ¿Qué derecho no se está cumpliendo?",
    "ops": [
      "A una vivienda digna",
      "A tener bicicleta",
      "A elegir la comida"
    ],
    "m": "Una vivienda digna es un derecho básico."
  },
  {
    "q": "Todos los chicos del grado tienen nombre y documento. ¿Qué derecho es?",
    "ops": [
      "A la identidad",
      "Al deporte",
      "A la tecnología"
    ],
    "m": "Tener nombre, apellido y documento es el derecho a la identidad."
  },
  {
    "q": "Un chico en silla de ruedas no puede entrar porque hay escalones. ¿Qué falta?",
    "ops": [
      "Que el lugar sea accesible para todos",
      "Que se quede en casa",
      "Que lo carguen siempre"
    ],
    "m": "Los espacios tienen que ser accesibles: es parte de la igualdad de derechos."
  },
  {
    "q": "En un grupo de chat se burlan de un compañero todos los días. ¿Qué hay que hacer?",
    "ops": [
      "Contarle a una persona adulta de confianza",
      "Sumarse para no quedar afuera",
      "Hacer de cuenta que no pasa"
    ],
    "m": "El hostigamiento también existe en lo digital; hay que pedir ayuda a una persona adulta."
  },
  {
    "q": "Una familia habla otro idioma en casa. ¿Eso está bien?",
    "ops": [
      "Sí, es parte de su identidad y cultura",
      "No, hay que hablar sólo uno",
      "Sólo si viven en otro país"
    ],
    "m": "Respetar la lengua y la cultura de cada familia es un derecho."
  },
  {
    "q": "En la escuela dan de comer a quien lo necesita. ¿Qué derecho se cumple?",
    "ops": [
      "A la alimentación",
      "A la propiedad",
      "Al trabajo"
    ],
    "m": "Alimentarse bien es un derecho, y la escuela ayuda a garantizarlo."
  },
  {
    "q": "Un chico quiere jugar al fútbol y le dicen que es sólo para varones. ¿Qué pasa ahí?",
    "ops": [
      "Se lo discrimina: el deporte es para todos",
      "Está bien, es la regla",
      "Tiene que elegir otro juego"
    ],
    "m": "Limitar una actividad por el género es discriminación."
  }
];
GAMES.derechos_escenarios = juegoTriviaTexto(CUR_DERECHOS_ESCENARIOS_BANCO, "Elegí la respuesta correcta.", "derechos_e");

/* 1° · ¿Sólido o líquido? — solido_liquido
   DC: Los materiales y sus estados: sólido y líquido; casos límite
   Fuente: docs/auditoria-dc-caba/grado-1.md · C3 */
const CUR_SOLIDO_LIQUIDO_BANCO = [
  {
    "it": "Piedra",
    "cat": "solido",
    "m": "La piedra tiene forma propia: es sólida."
  },
  {
    "it": "Agua",
    "cat": "liquido",
    "m": "El agua toma la forma del recipiente: es líquida."
  },
  {
    "it": "Leche",
    "cat": "liquido",
    "m": "La leche se vuelca y toma la forma del vaso: líquida."
  },
  {
    "it": "Madera",
    "cat": "solido",
    "m": "La madera mantiene su forma: es sólida."
  },
  {
    "it": "Hielo",
    "cat": "solido",
    "m": "Ojo: el hielo es agua SÓLIDA. Tiene forma propia, no se vuelca."
  },
  {
    "it": "Miel",
    "cat": "liquido",
    "m": "La miel es espesa, pero se vuelca y toma la forma del frasco: es líquida."
  },
  {
    "it": "Harina",
    "cat": "solido",
    "m": "La harina parece que se vuelca, pero son muchos granitos sólidos."
  },
  {
    "it": "Aceite",
    "cat": "liquido",
    "m": "El aceite se vuelca y toma la forma: líquido."
  },
  {
    "it": "Vidrio",
    "cat": "solido",
    "m": "El vidrio tiene forma propia: es sólido."
  },
  {
    "it": "Jugo",
    "cat": "liquido",
    "m": "El jugo toma la forma del vaso: líquido."
  },
  {
    "it": "Arena",
    "cat": "solido",
    "m": "La arena se derrama, pero cada granito es sólido."
  },
  {
    "it": "Goma de borrar",
    "cat": "solido",
    "m": "Tiene forma propia: sólida."
  },
  {
    "it": "Champú",
    "cat": "liquido",
    "m": "Es espeso pero se vuelca: líquido."
  },
  {
    "it": "Cubito de caldo",
    "cat": "solido",
    "m": "Tiene forma propia: es sólido."
  }
];
GAMES.solido_liquido = juegoClasificar(CUR_SOLIDO_LIQUIDO_BANCO, "¿Es sólido o líquido?", [{"cat": "solido", "label": "🧊 Sólido"}, {"cat": "liquido", "label": "💧 Líquido"}], "solido_liq");

/* 3° · El viaje del alimento — circuito_alimento
   DC: Circuito productivo: de la fase agraria a la comercial
   Fuente: docs/auditoria-dc-caba/grado-3.md · C3 */
const CUR_CIRCUITO_ALIMENTO_BANCO = [
  {
    "items": [
      "La vaca da leche en el tambo",
      "Un camión lleva la leche a la fábrica",
      "En la fábrica hacen el queso",
      "El queso llega al supermercado"
    ]
  },
  {
    "items": [
      "Se siembra el trigo",
      "Se cosecha el trigo",
      "En el molino lo hacen harina",
      "La panadería hace el pan"
    ]
  },
  {
    "items": [
      "Se plantan las papas",
      "Se sacan las papas de la tierra",
      "Se lavan y se embolsan",
      "Se venden en la verdulería"
    ]
  },
  {
    "items": [
      "La oveja da lana",
      "Se esquila la oveja",
      "Se hila la lana",
      "Se teje el pulóver"
    ]
  },
  {
    "items": [
      "Se juntan las uvas",
      "Se llevan a la bodega",
      "Se hace el jugo",
      "Se vende embotellado"
    ]
  },
  {
    "items": [
      "El árbol da naranjas",
      "Se cosechan las naranjas",
      "En la fábrica hacen el jugo",
      "El jugo llega al kiosco"
    ]
  },
  {
    "items": [
      "Se cría la gallina",
      "Se juntan los huevos",
      "Se guardan en maples",
      "Se venden en el almacén"
    ]
  },
  {
    "items": [
      "Se corta el árbol",
      "Se lleva el tronco al aserradero",
      "Se hacen las tablas",
      "Se arma la silla"
    ]
  },
  {
    "items": [
      "Se cultiva el algodón",
      "Se cosecha el algodón",
      "Se hila y se teje la tela",
      "Se cose la remera"
    ]
  }
];
GAMES.circuito_alimento = juegoOrdenar(CUR_CIRCUITO_ALIMENTO_BANCO, "Ordená el recorrido: ¿qué pasa primero? Tocá en orden.", "Pensá el camino desde donde se produce hasta que llega a tu casa.", "circuito_a");

/* 1° · ¿Pelos, plumas o escamas? — animales_cobertura
   DC: Características de los animales: cobertura del cuerpo
   Fuente: docs/auditoria-dc-caba/grado-1.md · C1 */
const CUR_ANIMALES_COBERTURA_BANCO = [
  {
    "it": "Perro",
    "cat": "pelos",
    "m": "El perro tiene el cuerpo cubierto de pelos."
  },
  {
    "it": "Gallina",
    "cat": "plumas",
    "m": "La gallina tiene plumas, como todas las aves."
  },
  {
    "it": "Pez",
    "cat": "escamas",
    "m": "El pez tiene escamas que le cubren el cuerpo."
  },
  {
    "it": "Gato",
    "cat": "pelos",
    "m": "El gato está cubierto de pelos."
  },
  {
    "it": "Murciélago",
    "cat": "pelos",
    "m": "Ojo: vuela, pero NO es un ave. Tiene pelos, no plumas."
  },
  {
    "it": "Pingüino",
    "cat": "plumas",
    "m": "Ojo: no vuela, pero es un ave. Tiene plumas."
  },
  {
    "it": "Serpiente",
    "cat": "escamas",
    "m": "La serpiente está cubierta de escamas."
  },
  {
    "it": "Caballo",
    "cat": "pelos",
    "m": "El caballo tiene pelo en todo el cuerpo."
  },
  {
    "it": "Loro",
    "cat": "plumas",
    "m": "El loro es un ave: tiene plumas."
  },
  {
    "it": "Lagartija",
    "cat": "escamas",
    "m": "La lagartija tiene escamas."
  },
  {
    "it": "Vaca",
    "cat": "pelos",
    "m": "La vaca tiene el cuerpo cubierto de pelos."
  },
  {
    "it": "Pato",
    "cat": "plumas",
    "m": "El pato es un ave: tiene plumas."
  },
  {
    "it": "Tiburón",
    "cat": "escamas",
    "m": "El tiburón es un pez: tiene escamas."
  },
  {
    "it": "Ballena",
    "cat": "pelos",
    "m": "Ojo: vive en el mar, pero NO es un pez. Tiene pelos, muy poquitos."
  },
  {
    "it": "Oveja",
    "cat": "pelos",
    "m": "La lana de la oveja es pelo."
  },
  {
    "it": "Cocodrilo",
    "cat": "escamas",
    "m": "El cocodrilo tiene escamas duras."
  }
];
GAMES.animales_cobertura = juegoClasificar(CUR_ANIMALES_COBERTURA_BANCO, "¿Con qué está cubierto el cuerpo?", [{"cat": "pelos", "label": "🐻 Pelos"}, {"cat": "plumas", "label": "🦜 Plumas"}, {"cat": "escamas", "label": "🐟 Escamas"}], "animales_c");

/* 1° · ¿Antes, hoy o en los dos? — antes_y_hoy
   DC: Cambios y continuidades a lo largo del tiempo. La CONTINUIDAD es el contenido que una dicotomía antes/hoy no puede enseñar
   Fuente: docs/auditoria-dc-caba/grado-1.md · C6 */
const CUR_ANTES_Y_HOY_BANCO = [
  {
    "it": "El pan",
    "cat": "ambos",
    "m": "Se comía antes y se come hoy: es una continuidad."
  },
  {
    "it": "El celular",
    "cat": "hoy",
    "m": "El celular es de ahora; antes no existía."
  },
  {
    "it": "La carreta con caballos",
    "cat": "antes",
    "m": "Antes se viajaba en carreta; hoy ya casi no se usa."
  },
  {
    "it": "Los juegos con pelota",
    "cat": "ambos",
    "m": "Los chicos jugaban con pelota antes y siguen jugando hoy."
  },
  {
    "it": "La computadora",
    "cat": "hoy",
    "m": "Es un invento reciente."
  },
  {
    "it": "Las velas para alumbrar",
    "cat": "antes",
    "m": "Antes se alumbraba con velas; hoy usamos luz eléctrica."
  },
  {
    "it": "La escuela",
    "cat": "ambos",
    "m": "Había escuelas antes y hay hoy."
  },
  {
    "it": "Los anillos y collares",
    "cat": "ambos",
    "m": "La gente usaba adornos antes y los usa hoy."
  },
  {
    "it": "La heladera",
    "cat": "hoy",
    "m": "Antes se guardaba la comida con hielo, no había heladera eléctrica."
  },
  {
    "it": "La pluma para escribir",
    "cat": "antes",
    "m": "Antes se escribía con pluma y tintero."
  },
  {
    "it": "La familia",
    "cat": "ambos",
    "m": "Siempre hubo familias, aunque cambiaron."
  },
  {
    "it": "El televisor",
    "cat": "hoy",
    "m": "La tele es un invento del siglo pasado."
  },
  {
    "it": "Cocinar con leña",
    "cat": "antes",
    "m": "Antes se cocinaba con leña; hoy casi siempre con gas o electricidad."
  },
  {
    "it": "Los cuentos",
    "cat": "ambos",
    "m": "Se contaban cuentos antes y hoy también."
  }
];
GAMES.antes_y_hoy = juegoClasificar(CUR_ANTES_Y_HOY_BANCO, "¿Esto era de antes, es de ahora, o hay en los dos?", [{"cat": "antes", "label": "🕰️ Sólo antes"}, {"cat": "hoy", "label": "📱 Sólo hoy"}, {"cat": "ambos", "label": "🔁 En los dos"}], "antes_y_ho");

/* 2° · La linterna mágica — linterna_magica
   DC: Materiales opacos, traslúcidos y transparentes — el eje de ciencias del grado
   Fuente: docs/auditoria-dc-caba/grado-2.md · C1 */
const CUR_LINTERNA_MAGICA_BANCO = [
  {
    "it": "Una puerta de madera",
    "cat": "opaco",
    "m": "La madera no deja pasar nada de luz."
  },
  {
    "it": "El vidrio de la ventana",
    "cat": "transparente",
    "m": "Se ve nítido a través: es transparente."
  },
  {
    "it": "Papel manteca",
    "cat": "translucido",
    "m": "Ojo: pasa luz pero NO se ve nítido. Traslúcido no es lo mismo que transparente."
  },
  {
    "it": "Una pared",
    "cat": "opaco",
    "m": "La pared no deja pasar luz."
  },
  {
    "it": "Una bolsa de nylon fina",
    "cat": "translucido",
    "m": "Pasa luz pero las formas se ven borrosas."
  },
  {
    "it": "Una botella de agua limpia",
    "cat": "transparente",
    "m": "Se ve con nitidez lo que hay detrás."
  },
  {
    "it": "Un libro",
    "cat": "opaco",
    "m": "El libro tapa la luz por completo."
  },
  {
    "it": "Vidrio esmerilado del baño",
    "cat": "translucido",
    "m": "Deja pasar la luz pero no se distinguen las formas."
  },
  {
    "it": "Los anteojos",
    "cat": "transparente",
    "m": "Se ve nítido a través del cristal."
  },
  {
    "it": "Una remera",
    "cat": "opaco",
    "m": "La tela no deja pasar la luz."
  },
  {
    "it": "Una hoja de papel blanca",
    "cat": "translucido",
    "m": "Con la linterna atrás se ve el resplandor, pero no las formas."
  },
  {
    "it": "El agua de un vaso",
    "cat": "transparente",
    "m": "Se ve a través del agua limpia."
  },
  {
    "it": "Una cortina gruesa",
    "cat": "opaco",
    "m": "Está hecha para que no pase la luz."
  },
  {
    "it": "Papel celofán de color",
    "cat": "translucido",
    "m": "Pasa luz teñida, pero no se ve con nitidez."
  }
];
GAMES.linterna_magica = juegoClasificar(CUR_LINTERNA_MAGICA_BANCO, "Si le ponés la linterna atrás, ¿qué pasa con la luz?", [{"cat": "opaco", "label": "⬛ No pasa"}, {"cat": "translucido", "label": "🌫️ Pasa borroso"}, {"cat": "transparente", "label": "🪟 Se ve nítido"}], "linterna_m");

/* 2° · ¿Artesanal o industrial? — artesanal_industrial
   DC: Producción artesanal vs. industrial. El criterio es la TÉCNICA y la ESCALA, no si hay o no personas trabajando
   Fuente: docs/auditoria-dc-caba/grado-2.md · C4 */
const CUR_ARTESANAL_INDUSTRIAL_BANCO = [
  {
    "it": "Una señora teje un pulóver a mano",
    "cat": "artesanal",
    "m": "Lo hace una persona, de a uno y con sus manos: artesanal."
  },
  {
    "it": "Una fábrica hace 5.000 pulóveres por día",
    "cat": "industrial",
    "m": "Muchísimas unidades iguales con máquinas: industrial."
  },
  {
    "it": "Un panadero amasa el pan en el horno del barrio",
    "cat": "artesanal",
    "m": "De a poco y a mano: artesanal."
  },
  {
    "it": "Una máquina llena mil botellas por hora",
    "cat": "industrial",
    "m": "La escala y la máquina lo hacen industrial."
  },
  {
    "it": "Una persona controla una máquina que corta mil chapas",
    "cat": "industrial",
    "m": "Ojo: que haya una persona NO lo hace artesanal. Manda la máquina y la escala."
  },
  {
    "it": "Un alfarero hace una vasija en su torno",
    "cat": "artesanal",
    "m": "Una pieza por vez, hecha por una persona."
  },
  {
    "it": "Se imprimen 10.000 cuadernos iguales",
    "cat": "industrial",
    "m": "Producción en serie: industrial."
  },
  {
    "it": "Una artesana pinta cada mate distinto",
    "cat": "artesanal",
    "m": "Cada pieza es única: artesanal."
  },
  {
    "it": "Una línea de montaje arma autos",
    "cat": "industrial",
    "m": "Máquinas y gran escala: industrial."
  },
  {
    "it": "Un zapatero arregla zapatos en su taller",
    "cat": "artesanal",
    "m": "Trabajo manual, de a uno."
  },
  {
    "it": "Una máquina embolsa fideos sin parar",
    "cat": "industrial",
    "m": "Producción en serie con máquinas."
  },
  {
    "it": "Una señora hace dulce en su cocina",
    "cat": "artesanal",
    "m": "En casa, en poca cantidad: artesanal."
  },
  {
    "it": "Una fábrica hace mil frascos de dulce iguales",
    "cat": "industrial",
    "m": "El mismo producto, pero a escala industrial."
  },
  {
    "it": "Un carpintero hace una mesa por encargo",
    "cat": "artesanal",
    "m": "Una pieza, hecha a medida."
  }
];
GAMES.artesanal_industrial = juegoClasificar(CUR_ARTESANAL_INDUSTRIAL_BANCO, "¿Cómo se produce esto?", [{"cat": "artesanal", "label": "🤲 Artesanal"}, {"cat": "industrial", "label": "🏭 Industrial"}], "artesanal_");

/* 2° · ¿Ayer, hoy o mañana? — tiempo_verbo
   DC: Presente, pasado y futuro. Sin adverbio, lo decide la desinencia del verbo
   Fuente: docs/auditoria-dc-caba/grado-2.md · L13 */
const CUR_TIEMPO_VERBO_BANCO = [
  {
    "it": "Ayer jugamos en la plaza.",
    "cat": "ayer",
    "m": "«Jugamos» ya pasó."
  },
  {
    "it": "Mañana iremos al museo.",
    "cat": "manana",
    "m": "«Iremos» todavía no pasó."
  },
  {
    "it": "Hoy leo un cuento.",
    "cat": "hoy",
    "m": "«Leo» está pasando ahora."
  },
  {
    "it": "Comí una manzana.",
    "cat": "ayer",
    "m": "«Comí» ya terminó: es pasado."
  },
  {
    "it": "Cantaremos en el acto.",
    "cat": "manana",
    "m": "«Cantaremos» es futuro."
  },
  {
    "it": "Corro por el patio.",
    "cat": "hoy",
    "m": "«Corro» es presente."
  },
  {
    "it": "Pintaba un dibujo.",
    "cat": "ayer",
    "m": "«Pintaba» es pasado."
  },
  {
    "it": "Vamos a la escuela todos los días.",
    "cat": "hoy",
    "m": "«Vamos» es presente: algo que pasa habitualmente."
  },
  {
    "it": "Visitaré a mi abuela.",
    "cat": "manana",
    "m": "«Visitaré» es futuro."
  },
  {
    "it": "Escribimos una carta la semana pasada.",
    "cat": "ayer",
    "m": "«Escribimos» con «la semana pasada» es pasado."
  },
  {
    "it": "El perro duerme en la alfombra.",
    "cat": "hoy",
    "m": "«Duerme» es presente."
  },
  {
    "it": "Traeré la pelota.",
    "cat": "manana",
    "m": "«Traeré» es futuro."
  },
  {
    "it": "Se rompió el vaso.",
    "cat": "ayer",
    "m": "«Se rompió» ya ocurrió."
  },
  {
    "it": "Estudiaremos para la prueba.",
    "cat": "manana",
    "m": "«Estudiaremos» es futuro."
  },
  {
    "it": "Ella baila muy bien.",
    "cat": "hoy",
    "m": "«Baila» es presente."
  }
];
GAMES.tiempo_verbo = juegoClasificar(CUR_TIEMPO_VERBO_BANCO, "¿Cuándo pasa lo que dice la oración?", [{"cat": "ayer", "label": "⬅️ Ayer"}, {"cat": "hoy", "label": "📍 Hoy"}, {"cat": "manana", "label": "➡️ Mañana"}], "tiempo_ver");

/* 2° · ¿Qué texto es? — tipos_de_texto
   DC: Tipos textuales: instrucciones, invitaciones, publicidades y señalética
   Fuente: docs/auditoria-dc-caba/grado-2.md · L10 */
const CUR_TIPOS_DE_TEXTO_BANCO = [
  {
    "it": "«Mezclar la harina con el agua y amasar.»",
    "cat": "receta",
    "m": "Dice pasos para cocinar: es una receta."
  },
  {
    "it": "«¡Te espero el sábado a las 4 en mi casa!»",
    "cat": "invitacion",
    "m": "Invita a alguien a un evento."
  },
  {
    "it": "«¡Gran liquidación! Todo al 50%.»",
    "cat": "aviso",
    "m": "Quiere vender algo: es un aviso."
  },
  {
    "it": "«Ingredientes: 2 huevos, 1 taza de leche.»",
    "cat": "receta",
    "m": "La lista de ingredientes es parte de la receta."
  },
  {
    "it": "«Cumplo 8 años. ¡Vení a festejar!»",
    "cat": "invitacion",
    "m": "Invita al cumpleaños."
  },
  {
    "it": "«Se busca perro perdido. Llamar al 4444-5555.»",
    "cat": "aviso",
    "m": "Avisa algo al público."
  },
  {
    "it": "«Hornear 20 minutos a fuego medio.»",
    "cat": "receta",
    "m": "Es una instrucción de cocina."
  },
  {
    "it": "«Fiesta de fin de año. Salón de la escuela, 18 hs.»",
    "cat": "invitacion",
    "m": "Invita a un evento con lugar y horario."
  },
  {
    "it": "«Cuidado: piso mojado.»",
    "cat": "aviso",
    "m": "Avisa algo para prevenir: es un cartel de aviso."
  },
  {
    "it": "«Batir las claras a nieve.»",
    "cat": "receta",
    "m": "Es un paso de la receta."
  },
  {
    "it": "«Los esperamos en el acto del 25 de Mayo.»",
    "cat": "invitacion",
    "m": "Convoca a un acto."
  },
  {
    "it": "«Clases de guitarra. Consultá horarios.»",
    "cat": "aviso",
    "m": "Ofrece un servicio: aviso."
  },
  {
    "it": "«Dejar enfriar antes de servir.»",
    "cat": "receta",
    "m": "Instrucción de cocina."
  },
  {
    "it": "«Prohibido pisar el césped.»",
    "cat": "aviso",
    "m": "Es un cartel de aviso."
  }
];
GAMES.tipos_de_texto = juegoClasificar(CUR_TIPOS_DE_TEXTO_BANCO, "¿Qué clase de texto es este?", [{"cat": "receta", "label": "🍳 Receta"}, {"cat": "invitacion", "label": "🎉 Invitación"}, {"cat": "aviso", "label": "📢 Aviso"}], "tipos_de_t");

/* 2° · Ordená los pasos — ordenar_pasos
   DC: Orden lógico de las acciones en un texto instructivo
   Fuente: docs/auditoria-dc-caba/grado-2.md · L9 */
const CUR_ORDENAR_PASOS_BANCO = [
  {
    "items": [
      "Juntar los ingredientes",
      "Mezclar todo en un bol",
      "Poner la mezcla en el horno",
      "Servir la torta"
    ]
  },
  {
    "items": [
      "Poner la pava con agua",
      "Esperar a que hierva",
      "Poner la yerba en el mate",
      "Cebar el mate"
    ]
  },
  {
    "items": [
      "Sacar los útiles de la mochila",
      "Escribir la fecha",
      "Hacer la tarea",
      "Guardar todo otra vez"
    ]
  },
  {
    "items": [
      "Elegir la semilla",
      "Poner tierra en la maceta",
      "Enterrar la semilla",
      "Regar todos los días"
    ]
  },
  {
    "items": [
      "Sacar la ropa sucia",
      "Ponerla en el lavarropas",
      "Colgarla al sol",
      "Doblarla y guardarla"
    ]
  },
  {
    "items": [
      "Untar el pan con manteca",
      "Poner el queso encima",
      "Cerrar el sándwich",
      "Cortarlo por la mitad"
    ]
  },
  {
    "items": [
      "Ponerse las medias",
      "Ponerse las zapatillas",
      "Atarse los cordones"
    ]
  },
  {
    "items": [
      "Abrir el libro",
      "Leer el cuento",
      "Cerrar el libro",
      "Contarle a alguien de qué se trataba"
    ]
  },
  {
    "items": [
      "Mojarse las manos",
      "Ponerse jabón",
      "Enjuagarse",
      "Secarse con la toalla"
    ]
  },
  {
    "items": [
      "Comprar los globos",
      "Inflarlos",
      "Colgarlos en la pared",
      "Sacarle una foto a la decoración"
    ]
  }
];
GAMES.ordenar_pasos = juegoOrdenar(CUR_ORDENAR_PASOS_BANCO, "Ordená los pasos: ¿qué se hace primero? Tocá en orden.", "Pensá qué tiene que estar listo antes de poder hacer lo siguiente.", "ordenar_pa");

/* 3° · Frío y calor — estados_tres
   DC: Estados de la materia. El estado GASEOSO es lo nuevo del grado
   Fuente: docs/auditoria-dc-caba/grado-3.md · C1 */
const CUR_ESTADOS_TRES_BANCO = [
  {
    "it": "Una piedra",
    "cat": "solido",
    "m": "Tiene forma propia: sólido."
  },
  {
    "it": "El agua del vaso",
    "cat": "liquido",
    "m": "Toma la forma del vaso: líquido."
  },
  {
    "it": "El aire",
    "cat": "gaseoso",
    "m": "El aire es un gas: ocupa todo el espacio."
  },
  {
    "it": "El vapor de la pava",
    "cat": "gaseoso",
    "m": "El vapor es agua en estado gaseoso."
  },
  {
    "it": "Un cubito de hielo",
    "cat": "solido",
    "m": "El hielo es agua sólida."
  },
  {
    "it": "El humo",
    "cat": "gaseoso",
    "m": "El humo se dispersa por el aire: gaseoso."
  },
  {
    "it": "La leche",
    "cat": "liquido",
    "m": "Se vuelca y toma la forma: líquida."
  },
  {
    "it": "El gas de la garrafa",
    "cat": "gaseoso",
    "m": "Es un gas, por eso se llama así."
  },
  {
    "it": "Una cuchara de metal",
    "cat": "solido",
    "m": "Tiene forma propia."
  },
  {
    "it": "El aceite",
    "cat": "liquido",
    "m": "Toma la forma del recipiente."
  },
  {
    "it": "Las burbujas de la gaseosa",
    "cat": "gaseoso",
    "m": "Adentro de la burbuja hay gas."
  },
  {
    "it": "La arena",
    "cat": "solido",
    "m": "Cada granito es sólido."
  },
  {
    "it": "El jugo",
    "cat": "liquido",
    "m": "Es líquido: toma la forma del vaso."
  },
  {
    "it": "El vaho que sale de la boca en invierno",
    "cat": "gaseoso",
    "m": "Es vapor de agua: estado gaseoso."
  }
];
GAMES.estados_tres = juegoClasificar(CUR_ESTADOS_TRES_BANCO, "¿En qué estado está?", [{"cat": "solido", "label": "🧊 Sólido"}, {"cat": "liquido", "label": "💧 Líquido"}, {"cat": "gaseoso", "label": "☁️ Gaseoso"}], "estados_tr");

/* 3° · Línea de tiempo — linea_siglo_xx
   DC: Impacto de las nuevas tecnologías; línea de tiempo
   Fuente: docs/auditoria-dc-caba/grado-3.md · C7 */
const CUR_LINEA_SIGLO_XX_BANCO = [
  {
    "items": [
      "La carreta tirada por caballos",
      "El tren a vapor",
      "El auto",
      "El avión"
    ]
  },
  {
    "items": [
      "La carta en papel",
      "El telégrafo",
      "El teléfono de casa",
      "El celular"
    ]
  },
  {
    "items": [
      "La vela",
      "El farol a querosén",
      "La lamparita eléctrica",
      "La luz LED"
    ]
  },
  {
    "items": [
      "El diario de papel",
      "La radio",
      "La televisión",
      "Internet"
    ]
  },
  {
    "items": [
      "Lavar la ropa en el río",
      "El lavadero con tabla",
      "El lavarropas a manija",
      "El lavarropas automático"
    ]
  },
  {
    "items": [
      "Guardar comida con hielo",
      "La heladera eléctrica",
      "El freezer"
    ]
  },
  {
    "items": [
      "Escribir con pluma y tintero",
      "La máquina de escribir",
      "La computadora"
    ]
  },
  {
    "items": [
      "La fotografía en blanco y negro",
      "La foto a color",
      "La foto digital"
    ]
  },
  {
    "items": [
      "El fuego a leña",
      "La cocina a gas",
      "El microondas"
    ]
  }
];
GAMES.linea_siglo_xx = juegoOrdenar(CUR_LINEA_SIGLO_XX_BANCO, "Ordená del más ANTIGUO al más nuevo. Tocá en orden.", "Pensá qué se inventó primero: lo más viejo va al principio.", "linea_sigl");

/* 2° · ¿Qué cuenta lo resuelve? — que_cuenta_resuelve
   DC: Elegir la operación que resuelve el problema. Rediseñada: era clasificar en 2 cajas y se acertaba el 50% por moneda
   Fuente: docs/auditoria-dc-caba/grado-2.md · M9 */
const CUR_QUE_CUENTA_RESUELVE_BANCO = [
  {
    "q": "Hay 4 paquetes con 6 caramelos cada uno. ¿Cuántos caramelos hay?",
    "ops": [
      "6 + 6 + 6 + 6",
      "6 + 4",
      "6 − 4"
    ],
    "m": "Son 4 grupos iguales de 6: se suma 6 cuatro veces."
  },
  {
    "q": "Tenía 20 figuritas y regalé 8. ¿Cuántas me quedan?",
    "ops": [
      "20 − 8",
      "20 + 8",
      "8 − 20"
    ],
    "m": "Si regalás, tenés menos: hay que restar."
  },
  {
    "q": "Junté 15 tapitas y después 12 más. ¿Cuántas tengo?",
    "ops": [
      "15 + 12",
      "15 − 12",
      "15 + 2"
    ],
    "m": "Se juntan las dos cantidades: se suma."
  },
  {
    "q": "Hay 3 mesas con 5 sillas cada una. ¿Cuántas sillas hay?",
    "ops": [
      "5 + 5 + 5",
      "5 + 3",
      "5 − 3"
    ],
    "m": "Son 3 grupos iguales de 5."
  },
  {
    "q": "En el micro había 30 personas y bajaron 12. ¿Cuántas quedaron?",
    "ops": [
      "30 − 12",
      "30 + 12",
      "12 − 30"
    ],
    "m": "Si bajan, quedan menos: se resta."
  },
  {
    "q": "Compré 2 cajas de 10 lápices. ¿Cuántos lápices compré?",
    "ops": [
      "10 + 10",
      "10 + 2",
      "10 − 2"
    ],
    "m": "Dos grupos iguales de 10."
  },
  {
    "q": "Tenía 45 y me dieron 20 más. ¿Cuántos tengo?",
    "ops": [
      "45 + 20",
      "45 − 20",
      "20 − 45"
    ],
    "m": "Si te dan más, se suma."
  },
  {
    "q": "Había 100 globos y se pincharon 25. ¿Cuántos quedan?",
    "ops": [
      "100 − 25",
      "100 + 25",
      "25 − 100"
    ],
    "m": "Se pierden globos: se resta."
  },
  {
    "q": "Cada bolsa trae 4 manzanas. Compré 5 bolsas. ¿Cuántas manzanas?",
    "ops": [
      "4 + 4 + 4 + 4 + 4",
      "4 + 5",
      "5 − 4"
    ],
    "m": "Cinco grupos iguales de 4."
  },
  {
    "q": "Leí 18 páginas ayer y 22 hoy. ¿Cuántas leí?",
    "ops": [
      "18 + 22",
      "22 − 18",
      "18 − 22"
    ],
    "m": "Se juntan las dos cantidades."
  },
  {
    "q": "Tenía 60 pesos y gasté 35. ¿Cuánto me queda?",
    "ops": [
      "60 − 35",
      "60 + 35",
      "35 − 60"
    ],
    "m": "Si gastás, te queda menos."
  },
  {
    "q": "Hay 6 cajas con 2 pelotas cada una. ¿Cuántas pelotas?",
    "ops": [
      "2 + 2 + 2 + 2 + 2 + 2",
      "6 + 2",
      "6 − 2"
    ],
    "m": "Seis grupos iguales de 2."
  },
  {
    "q": "En el estante hay 40 libros y agrego 15. ¿Cuántos hay?",
    "ops": [
      "40 + 15",
      "40 − 15",
      "15 − 40"
    ],
    "m": "Se agregan: se suma."
  },
  {
    "q": "Salieron 8 de los 25 alumnos. ¿Cuántos quedaron en el aula?",
    "ops": [
      "25 − 8",
      "25 + 8",
      "8 + 8"
    ],
    "m": "Si salen, quedan menos."
  }
];
GAMES.que_cuenta_resuelve = juegoTriviaTexto(CUR_QUE_CUENTA_RESUELVE_BANCO, "¿Con qué cuenta se resuelve?", "que_cuenta");

/* 2° · Adiviná mi figura — adivina_figura
   DC: Figuras geométricas por sus características: lados, vértices y ángulos rectos. Las figuras se reconocen aunque estén rotadas
   Fuente: docs/auditoria-dc-caba/grado-2.md · M15 */
const CUR_ADIVINA_FIGURA_BANCO = [
  {
    "q": "Tengo 3 lados y 3 vértices. ¿Qué soy?",
    "ops": [
      "Un triángulo",
      "Un cuadrado",
      "Un círculo"
    ],
    "m": "Tri- significa tres: el triángulo tiene 3 lados."
  },
  {
    "q": "Tengo 4 lados iguales y 4 esquinas rectas. ¿Qué soy?",
    "ops": [
      "Un cuadrado",
      "Un rectángulo",
      "Un triángulo"
    ],
    "m": "El cuadrado tiene los 4 lados iguales; el rectángulo no."
  },
  {
    "q": "No tengo ningún lado recto ni esquinas. ¿Qué soy?",
    "ops": [
      "Un círculo",
      "Un cuadrado",
      "Un triángulo"
    ],
    "m": "El círculo es una curva cerrada: no tiene lados."
  },
  {
    "q": "Tengo 4 lados y 4 esquinas rectas, pero dos lados son más largos. ¿Qué soy?",
    "ops": [
      "Un rectángulo",
      "Un cuadrado",
      "Un rombo"
    ],
    "m": "El rectángulo tiene los lados iguales de a pares."
  },
  {
    "q": "Tengo 4 lados iguales pero estoy inclinado, sin esquinas rectas. ¿Qué soy?",
    "ops": [
      "Un rombo",
      "Un cuadrado",
      "Un círculo"
    ],
    "m": "El rombo tiene 4 lados iguales pero sus ángulos no son rectos."
  },
  {
    "q": "Aunque me den vuelta y quede apoyado en una punta, sigo teniendo 3 lados. ¿Qué soy?",
    "ops": [
      "Un triángulo",
      "Un cuadrado",
      "Un rectángulo"
    ],
    "m": "Girar una figura no le cambia la cantidad de lados."
  },
  {
    "q": "¿Cuántos vértices tiene un cuadrado?",
    "ops": [
      "4",
      "3",
      "6"
    ],
    "m": "Los vértices son las esquinas: el cuadrado tiene 4."
  },
  {
    "q": "¿Cuántos lados tiene un rectángulo?",
    "ops": [
      "4",
      "3",
      "5"
    ],
    "m": "El rectángulo tiene 4 lados."
  },
  {
    "q": "Tengo 5 lados. ¿Qué soy?",
    "ops": [
      "Un pentágono",
      "Un cuadrado",
      "Un triángulo"
    ],
    "m": "Penta- significa cinco: el pentágono tiene 5 lados."
  },
  {
    "q": "¿Qué figura rueda porque no tiene esquinas?",
    "ops": [
      "El círculo",
      "El cuadrado",
      "El triángulo"
    ],
    "m": "Sin esquinas ni lados rectos, el círculo rueda."
  },
  {
    "q": "Tengo 6 lados. ¿Qué soy?",
    "ops": [
      "Un hexágono",
      "Un pentágono",
      "Un cuadrado"
    ],
    "m": "Hexa- significa seis."
  },
  {
    "q": "¿En qué se diferencian un cuadrado y un rombo?",
    "ops": [
      "El cuadrado tiene los ángulos rectos",
      "El rombo tiene más lados",
      "El cuadrado no se puede girar"
    ],
    "m": "Los dos tienen 4 lados iguales; sólo el cuadrado tiene ángulos rectos."
  },
  {
    "q": "¿Cuántas esquinas rectas tiene un triángulo cualquiera?",
    "ops": [
      "Puede no tener ninguna",
      "Siempre 3",
      "Siempre 1"
    ],
    "m": "Hay triángulos sin ningún ángulo recto."
  },
  {
    "q": "¿Qué tienen en común el cuadrado y el rectángulo?",
    "ops": [
      "Los dos tienen 4 lados y 4 ángulos rectos",
      "Los dos tienen los 4 lados iguales",
      "Los dos ruedan"
    ],
    "m": "Ambos tienen 4 lados y 4 ángulos rectos; se diferencian en los lados."
  }
];
GAMES.adivina_figura = juegoTriviaTexto(CUR_ADIVINA_FIGURA_BANCO, "¿Qué figura es?", "adivina_fi");

/* 1° · Del campo a tu casa — campo_a_casa
   DC: De dónde vienen las cosas que usamos: procesos hasta llegar a casa
   Fuente: docs/auditoria-dc-caba/grado-1.md · C5 */
const CUR_CAMPO_A_CASA_BANCO = [
  {
    "items": [
      "La gallina pone el huevo",
      "Se juntan los huevos",
      "Se llevan al negocio",
      "Los comemos en casa"
    ]
  },
  {
    "items": [
      "Crece la planta de tomate",
      "Se juntan los tomates",
      "Se venden en la verdulería",
      "Hacemos la ensalada"
    ]
  },
  {
    "items": [
      "La vaca da leche",
      "La leche va a la fábrica",
      "Llega al supermercado",
      "La tomamos en casa"
    ]
  },
  {
    "items": [
      "Se planta la semilla de trigo",
      "Crece la planta",
      "Se hace harina",
      "Se hace el pan"
    ]
  },
  {
    "items": [
      "El árbol da manzanas",
      "Se juntan las manzanas",
      "Van al mercado",
      "Las comemos"
    ]
  },
  {
    "items": [
      "La oveja da lana",
      "Se hace el hilo",
      "Se teje la bufanda",
      "La usamos en invierno"
    ]
  },
  {
    "items": [
      "Se planta la papa",
      "Se saca de la tierra",
      "Se lava",
      "Se cocina en casa"
    ]
  },
  {
    "items": [
      "La abeja hace la miel",
      "Se saca del panal",
      "Se envasa en frascos",
      "La comemos con tostadas"
    ]
  }
];
GAMES.campo_a_casa = juegoOrdenar(CUR_CAMPO_A_CASA_BANCO, "Ordená cómo llega a tu casa. Tocá en orden.", "Empezá por dónde nace o se produce, y terminá en tu casa.", "campo_a_ca");

/* 2° · Cálculo redondo — calculo_redondo
   DC: Sumar y restar 1, 10 y 100 a números de tres cifras. Reemplaza sumas/restas, que operaban hasta 10 (contenido de 1°)
   Fuente: docs/auditoria-dc-caba/grado-2.md · M4 */
const CUR_CALCULO_REDONDO_PLANTILLA = {
  "q": "{a} + {b}",
  "vars": {
    "a": {
      "rango": [
        110,
        880
      ],
      "paso": 10
    },
    "b": {
      "opciones": [
        1,
        10,
        100
      ]
    }
  },
  "ok": "a + b",
  "distractores": [
    "a + b*10",
    "a + b/10",
    "a - b"
  ],
  "tope": 1000,
  "m": "Fijate en qué columna sumás: unidades con unidades, decenas con decenas, centenas con centenas. Da {ok}."
};
GAMES.calculo_redondo = juegoParametrico(CUR_CALCULO_REDONDO_PLANTILLA, "¿Cuánto da?", "calculo_re");

/* 2° · ¿Cuánto falta para llegar? — forma_redondo
   DC: Sumas que dan 100 y 1.000 — complementos, nodal del grado
   Fuente: docs/auditoria-dc-caba/grado-2.md · M3 */
const CUR_FORMA_REDONDO_PLANTILLA = {
  "q": "{a} + ___ = {objetivo}",
  "vars": {
    "a": {
      "rango": [
        5,
        95
      ],
      "paso": 5
    },
    "objetivo": {
      "opciones": [
        100,
        500,
        1000
      ]
    }
  },
  "ok": "objetivo - a",
  "distractores": [
    "100 - a",
    "objetivo - a - 10",
    "objetivo - a + 10"
  ],
  "tope": 1000,
  "m": "Pensá cuánto le falta a {a} para llegar. La respuesta es {ok}."
};
GAMES.forma_redondo = juegoParametrico(CUR_FORMA_REDONDO_PLANTILLA, "¿Cuánto falta?", "forma_redo");

/* 7° · Derechos en el trabajo — derechos_trabajo
   DC: Derechos laborales y sociales; el trabajo en la Argentina contemporánea
   Fuente: docs/auditoria-dc-caba/grado-7.md · S */
const CUR_DERECHOS_TRABAJO_BANCO = [
  {
    "q": "¿Qué son las vacaciones pagas?",
    "ops": [
      "Días de descanso que se cobran igual",
      "Días que se descuentan del sueldo",
      "Un premio que da la empresa si quiere"
    ],
    "m": "Son un derecho: descansar sin perder el sueldo."
  },
  {
    "q": "¿Puede una empresa hacer trabajar a un chico de 12 años?",
    "ops": [
      "No, el trabajo infantil está prohibido",
      "Sí, si él quiere",
      "Sí, si le pagan bien"
    ],
    "m": "El trabajo infantil está prohibido por ley: los chicos tienen que estudiar y jugar."
  },
  {
    "q": "¿Qué es el aguinaldo?",
    "ops": [
      "Medio sueldo extra que se paga dos veces al año",
      "Un préstamo del empleador",
      "Una propina"
    ],
    "m": "Es un derecho: se cobra en junio y en diciembre."
  },
  {
    "q": "Trabajar «en negro» significa…",
    "ops": [
      "Sin estar registrado, y por eso sin derechos",
      "De noche",
      "En una fábrica"
    ],
    "m": "Sin registro no hay obra social, aportes ni indemnización: por eso importa."
  },
  {
    "q": "¿Para qué sirve un sindicato?",
    "ops": [
      "Para que los trabajadores negocien juntos sus condiciones",
      "Para cobrar impuestos",
      "Para contratar gente"
    ],
    "m": "Juntos tienen más fuerza para negociar que uno solo."
  },
  {
    "q": "¿Qué es la jornada laboral?",
    "ops": [
      "La cantidad de horas que se puede trabajar por día",
      "El día que se cobra",
      "El nombre del jefe"
    ],
    "m": "Está limitada por ley justamente para proteger la salud."
  },
  {
    "q": "Una mujer embarazada, ¿puede ser despedida por estar embarazada?",
    "ops": [
      "No, está protegida por ley",
      "Sí, si la empresa lo decide",
      "Sí, siempre"
    ],
    "m": "La ley protege especialmente la maternidad en el trabajo."
  },
  {
    "q": "¿Qué pasa si alguien se accidenta trabajando?",
    "ops": [
      "Tiene derecho a atención y cobertura",
      "Se arregla solo",
      "Pierde el trabajo"
    ],
    "m": "Los accidentes de trabajo tienen cobertura obligatoria."
  },
  {
    "q": "¿A igual tarea, tienen que cobrar igual un varón y una mujer?",
    "ops": [
      "Sí, es un derecho",
      "No, depende de la empresa",
      "Sólo si tienen la misma edad"
    ],
    "m": "«Igual remuneración por igual tarea» es un principio del derecho laboral."
  },
  {
    "q": "¿Qué es una obra social?",
    "ops": [
      "La cobertura de salud que corresponde por estar registrado",
      "Un banco",
      "Una escuela"
    ],
    "m": "Va ligada al trabajo registrado: otra razón por la que el registro importa."
  },
  {
    "q": "¿Se puede obligar a alguien a trabajar sin descanso semanal?",
    "ops": [
      "No, el descanso semanal es un derecho",
      "Sí, si hay mucho trabajo",
      "Sí, si le pagan extra"
    ],
    "m": "El descanso está protegido por ley, no es negociable."
  },
  {
    "q": "¿Qué es una indemnización por despido?",
    "ops": [
      "Un pago que corresponde si te despiden sin causa",
      "Una multa al trabajador",
      "Un adelanto de sueldo"
    ],
    "m": "Compensa la pérdida del trabajo cuando no hubo culpa del trabajador."
  },
  {
    "q": "¿Por qué existe el salario mínimo?",
    "ops": [
      "Para que ningún sueldo quede por debajo de lo necesario para vivir",
      "Para que nadie gane mucho",
      "Para cobrar impuestos"
    ],
    "m": "Es un piso: protege a quien tiene menos poder de negociación."
  },
  {
    "q": "¿Quién controla que se cumplan los derechos laborales?",
    "ops": [
      "El Estado, además de los sindicatos",
      "Nadie",
      "Sólo las empresas"
    ],
    "m": "El Estado inspecciona y los sindicatos reclaman: los dos."
  }
];
GAMES.derechos_trabajo = juegoTriviaTexto(CUR_DERECHOS_TRABAJO_BANCO, "Elegí la respuesta correcta.", "derechos_t");

/* 1° · ¿Con cuál empieza? — suena_igual
   DC: Correspondencia entre sonido y letra al inicio de la palabra
   Fuente: docs/auditoria-dc-caba/grado-1.md · L */
const CUR_SUENA_IGUAL_BANCO = [
  {
    "q": "🍎 MANZANA empieza con…",
    "ops": [
      "M",
      "N",
      "S"
    ],
    "m": "MA-: empieza con M."
  },
  {
    "q": "🐱 GATO empieza con…",
    "ops": [
      "G",
      "J",
      "C"
    ],
    "m": "GA-: empieza con G."
  },
  {
    "q": "☀️ SOL empieza con…",
    "ops": [
      "S",
      "C",
      "Z"
    ],
    "m": "SOL empieza con S."
  },
  {
    "q": "🐟 PEZ empieza con…",
    "ops": [
      "P",
      "B",
      "F"
    ],
    "m": "PEZ empieza con P."
  },
  {
    "q": "🌙 LUNA empieza con…",
    "ops": [
      "L",
      "N",
      "R"
    ],
    "m": "LU-: empieza con L."
  },
  {
    "q": "🏠 CASA empieza con…",
    "ops": [
      "C",
      "K",
      "Q"
    ],
    "m": "CASA empieza con C."
  },
  {
    "q": "🐘 ELEFANTE empieza con…",
    "ops": [
      "E",
      "A",
      "I"
    ],
    "m": "E-lefante: con E."
  },
  {
    "q": "🌻 FLOR empieza con…",
    "ops": [
      "F",
      "V",
      "B"
    ],
    "m": "FLOR empieza con F."
  },
  {
    "q": "🚗 AUTO empieza con…",
    "ops": [
      "A",
      "O",
      "E"
    ],
    "m": "AU-: empieza con A."
  },
  {
    "q": "🐝 ABEJA empieza con…",
    "ops": [
      "A",
      "E",
      "O"
    ],
    "m": "ABEJA empieza con A."
  },
  {
    "q": "🍌 BANANA empieza con…",
    "ops": [
      "B",
      "P",
      "D"
    ],
    "m": "BA-: empieza con B."
  },
  {
    "q": "🥛 LECHE empieza con…",
    "ops": [
      "L",
      "Ll",
      "N"
    ],
    "m": "LE-: empieza con L."
  },
  {
    "q": "🐭 RATÓN empieza con…",
    "ops": [
      "R",
      "D",
      "L"
    ],
    "m": "RA-: empieza con R."
  },
  {
    "q": "🧦 MEDIA empieza con…",
    "ops": [
      "M",
      "N",
      "B"
    ],
    "m": "ME-: empieza con M."
  }
];
GAMES.suena_igual = juegoTriviaTexto(CUR_SUENA_IGUAL_BANCO, "¿Con qué letra empieza?", "suena_igua");

/* 1° · ¿Cuántos quedan? — mas_o_menos_1
   DC: Restar cantidades pequeñas en situaciones de quitar
   Fuente: docs/auditoria-dc-caba/grado-1.md · M */
const CUR_MAS_O_MENOS_1_PLANTILLA = {
  "q": "Tenías {a} y se fueron {b}. ¿Cuántos quedan?",
  "vars": {
    "a": {
      "rango": [
        4,
        20
      ],
      "paso": 1
    },
    "b": {
      "rango": [
        1,
        9
      ],
      "paso": 1
    }
  },
  "ok": "a - b",
  "distractores": [
    "a + b",
    "a - b + 1",
    "a - b - 1"
  ],
  "tope": 20,
  "m": "Si se van, hay que restar: quedan {ok}."
};
GAMES.mas_o_menos_1 = juegoParametrico(CUR_MAS_O_MENOS_1_PLANTILLA, "¿Cuánto queda?", "mas_o_meno");

/* 4° · ¿Quién come a quién? — cadena_alimentaria
   DC: Relaciones alimentarias entre los seres vivos
   Fuente: docs/auditoria-dc-caba/grado-4.md · N */
const CUR_CADENA_ALIMENTARIA_BANCO = [
  {
    "it": "El pasto",
    "cat": "productor",
    "m": "Las plantas fabrican su alimento: son productoras."
  },
  {
    "it": "La vaca",
    "cat": "herbivoro",
    "m": "La vaca come pasto: herbívora."
  },
  {
    "it": "El puma",
    "cat": "carnivoro",
    "m": "El puma come otros animales: carnívoro."
  },
  {
    "it": "El árbol",
    "cat": "productor",
    "m": "Fabrica su alimento con la luz del sol."
  },
  {
    "it": "El conejo",
    "cat": "herbivoro",
    "m": "Come plantas: herbívoro."
  },
  {
    "it": "El zorro",
    "cat": "carnivoro",
    "m": "Caza otros animales."
  },
  {
    "it": "El helecho",
    "cat": "productor",
    "m": "Es una planta: productora."
  },
  {
    "it": "La oveja",
    "cat": "herbivoro",
    "m": "Come pasto."
  },
  {
    "it": "El águila",
    "cat": "carnivoro",
    "m": "Caza otros animales."
  },
  {
    "it": "El alga",
    "cat": "productor",
    "m": "Fabrica su alimento en el agua con la luz."
  },
  {
    "it": "La oruga",
    "cat": "herbivoro",
    "m": "Come hojas."
  },
  {
    "it": "La araña",
    "cat": "carnivoro",
    "m": "Come insectos: es carnívora."
  },
  {
    "it": "El yuyo",
    "cat": "productor",
    "m": "Es una planta."
  },
  {
    "it": "El caballo",
    "cat": "herbivoro",
    "m": "Come pasto y avena."
  }
];
GAMES.cadena_alimentaria = juegoClasificar(CUR_CADENA_ALIMENTARIA_BANCO, "¿Qué lugar ocupa en la cadena?", [{"cat": "productor", "label": "🌱 Produce"}, {"cat": "herbivoro", "label": "🐰 Come plantas"}, {"cat": "carnivoro", "label": "🦊 Come animales"}], "cadena_ali");

/* 4° · ¿Quién se ocupa? — gobierno_argentina
   DC: Organización del gobierno; niveles municipal, provincial y nacional
   Fuente: docs/auditoria-dc-caba/grado-4.md · S */
const CUR_GOBIERNO_ARGENTINA_BANCO = [
  {
    "q": "¿Quién se ocupa de la recolección de basura de tu barrio?",
    "ops": [
      "El municipio",
      "El gobierno nacional",
      "Ningún gobierno"
    ],
    "m": "Lo cercano —basura, alumbrado, plazas— lo resuelve el municipio."
  },
  {
    "q": "¿Quién dirige una provincia?",
    "ops": [
      "El gobernador o la gobernadora",
      "El intendente",
      "El presidente"
    ],
    "m": "Municipio → intendente; provincia → gobernador; país → presidente."
  },
  {
    "q": "¿Quién es la máxima autoridad del país?",
    "ops": [
      "El presidente o la presidenta",
      "El gobernador",
      "El intendente"
    ],
    "m": "El presidente encabeza el gobierno nacional."
  },
  {
    "q": "¿Quiénes hacen las leyes nacionales?",
    "ops": [
      "Los diputados y senadores",
      "Los jueces",
      "Los intendentes"
    ],
    "m": "El Congreso —diputados y senadores— hace las leyes."
  },
  {
    "q": "¿Quién se ocupa de que se cumplan las leyes y juzga?",
    "ops": [
      "Los jueces",
      "Los senadores",
      "El intendente"
    ],
    "m": "Ese es el Poder Judicial."
  },
  {
    "q": "¿Cada cuánto se vota para presidente en Argentina?",
    "ops": [
      "Cada 4 años",
      "Cada año",
      "Cada 10 años"
    ],
    "m": "El mandato presidencial dura 4 años."
  },
  {
    "q": "¿Quién puede votar en Argentina?",
    "ops": [
      "Las personas desde los 16 años",
      "Sólo los mayores de 30",
      "Sólo quienes trabajan"
    ],
    "m": "Desde los 16 se puede votar; desde los 18 es obligatorio."
  },
  {
    "q": "¿Cuántos poderes tiene el gobierno?",
    "ops": [
      "Tres: Ejecutivo, Legislativo y Judicial",
      "Uno solo",
      "Dos"
    ],
    "m": "Se dividen para que ninguno tenga todo el poder."
  },
  {
    "q": "Si se rompe una calle de tu barrio, ¿a quién le corresponde?",
    "ops": [
      "Al municipio",
      "Al presidente",
      "A los jueces"
    ],
    "m": "El mantenimiento del barrio es municipal."
  },
  {
    "q": "¿Qué es la Constitución?",
    "ops": [
      "La ley más importante del país",
      "Un libro de historia",
      "El nombre del Congreso"
    ],
    "m": "Todas las demás leyes tienen que respetarla."
  },
  {
    "q": "¿Quién dirige un municipio?",
    "ops": [
      "El intendente o la intendenta",
      "El gobernador",
      "Un juez"
    ],
    "m": "El intendente gobierna el municipio."
  },
  {
    "q": "¿Las provincias pueden tener sus propias leyes?",
    "ops": [
      "Sí, además de las nacionales",
      "No, ninguna",
      "Sólo la provincia de Buenos Aires"
    ],
    "m": "Cada provincia tiene su constitución y sus leyes, dentro de la nacional."
  },
  {
    "q": "¿Para qué sirve votar?",
    "ops": [
      "Para elegir a quienes nos gobiernan",
      "Para pagar impuestos",
      "Para elegir el feriado"
    ],
    "m": "Es la forma en que el pueblo elige a sus representantes."
  },
  {
    "q": "¿Qué significa que Argentina sea una república?",
    "ops": [
      "Que gobiernan representantes elegidos por el pueblo",
      "Que hay un rey",
      "Que no hay gobierno"
    ],
    "m": "En una república el poder se elige y se divide, no se hereda."
  }
];
GAMES.gobierno_argentina = juegoTriviaTexto(CUR_GOBIERNO_ARGENTINA_BANCO, "Elegí la respuesta correcta.", "gobierno_a");

/* 5° · ¿Qué clase de palabra es? — clases_palabra_5
   DC: Clases de palabras: sustantivo, adjetivo y verbo en contexto
   Fuente: docs/auditoria-dc-caba/grado-5.md · L */
const CUR_CLASES_PALABRA_5_BANCO = [
  {
    "it": "El PERRO corre rápido.",
    "cat": "sust",
    "m": "«Perro» nombra: sustantivo."
  },
  {
    "it": "El perro CORRE rápido.",
    "cat": "verbo",
    "m": "«Corre» es la acción: verbo."
  },
  {
    "it": "El perro NEGRO ladra.",
    "cat": "adj",
    "m": "«Negro» describe al perro: adjetivo."
  },
  {
    "it": "La CASA es grande.",
    "cat": "sust",
    "m": "«Casa» nombra una cosa."
  },
  {
    "it": "La casa es GRANDE.",
    "cat": "adj",
    "m": "«Grande» describe la casa."
  },
  {
    "it": "Ana CANTA en el coro.",
    "cat": "verbo",
    "m": "«Canta» es lo que hace."
  },
  {
    "it": "Comí una manzana JUGOSA.",
    "cat": "adj",
    "m": "«Jugosa» describe la manzana."
  },
  {
    "it": "COMÍ una manzana.",
    "cat": "verbo",
    "m": "«Comí» es la acción."
  },
  {
    "it": "El MAESTRO explicó el tema.",
    "cat": "sust",
    "m": "«Maestro» nombra a alguien."
  },
  {
    "it": "Un día LLUVIOSO.",
    "cat": "adj",
    "m": "«Lluvioso» describe el día."
  },
  {
    "it": "Los chicos SALTARON la soga.",
    "cat": "verbo",
    "m": "«Saltaron» es la acción."
  },
  {
    "it": "La CIUDAD tiene muchas plazas.",
    "cat": "sust",
    "m": "«Ciudad» nombra un lugar."
  },
  {
    "it": "Un problema DIFÍCIL.",
    "cat": "adj",
    "m": "«Difícil» describe el problema."
  },
  {
    "it": "El río CRECIÓ con la lluvia.",
    "cat": "verbo",
    "m": "«Creció» es lo que pasó."
  }
];
GAMES.clases_palabra_5 = juegoClasificar(CUR_CLASES_PALABRA_5_BANCO, "¿Qué clase de palabra es la resaltada?", [{"cat": "sust", "label": "🏷️ Sustantivo"}, {"cat": "adj", "label": "🎨 Adjetivo"}, {"cat": "verbo", "label": "🏃 Verbo"}], "clases_pal");

/* 5° · ¿De qué sistema es? — aparatos_cuerpo
   DC: Sistemas del cuerpo humano y sus órganos
   Fuente: docs/auditoria-dc-caba/grado-5.md · N */
const CUR_APARATOS_CUERPO_BANCO = [
  {
    "it": "El estómago",
    "cat": "digestivo",
    "m": "Ahí se sigue digiriendo la comida."
  },
  {
    "it": "Los pulmones",
    "cat": "respiratorio",
    "m": "Ahí entra y sale el aire."
  },
  {
    "it": "El corazón",
    "cat": "circulatorio",
    "m": "Bombea la sangre al cuerpo."
  },
  {
    "it": "El intestino delgado",
    "cat": "digestivo",
    "m": "Ahí se absorben los nutrientes."
  },
  {
    "it": "La tráquea",
    "cat": "respiratorio",
    "m": "Lleva el aire hacia los pulmones."
  },
  {
    "it": "Las venas",
    "cat": "circulatorio",
    "m": "Llevan la sangre de vuelta al corazón."
  },
  {
    "it": "El esófago",
    "cat": "digestivo",
    "m": "Lleva la comida de la boca al estómago."
  },
  {
    "it": "Los bronquios",
    "cat": "respiratorio",
    "m": "Reparten el aire dentro del pulmón."
  },
  {
    "it": "Las arterias",
    "cat": "circulatorio",
    "m": "Llevan la sangre desde el corazón."
  },
  {
    "it": "El hígado",
    "cat": "digestivo",
    "m": "Produce la bilis, que ayuda a digerir."
  },
  {
    "it": "La nariz",
    "cat": "respiratorio",
    "m": "Por ahí entra el aire y se filtra."
  },
  {
    "it": "La sangre",
    "cat": "circulatorio",
    "m": "Es lo que circula llevando oxígeno."
  },
  {
    "it": "El intestino grueso",
    "cat": "digestivo",
    "m": "Absorbe el agua que queda."
  },
  {
    "it": "El diafragma",
    "cat": "respiratorio",
    "m": "Es el músculo que te hace respirar."
  }
];
GAMES.aparatos_cuerpo = juegoClasificar(CUR_APARATOS_CUERPO_BANCO, "¿A qué sistema del cuerpo pertenece?", [{"cat": "digestivo", "label": "🍽️ Digestivo"}, {"cat": "respiratorio", "label": "🫁 Respiratorio"}, {"cat": "circulatorio", "label": "🫀 Circulatorio"}], "aparatos_c");

/* 6° · Recursos de nuestro país — recursos_argentina
   DC: Recursos naturales de la Argentina y actividades económicas asociadas
   Fuente: docs/auditoria-dc-caba/grado-6.md · S */
const CUR_RECURSOS_ARGENTINA_BANCO = [
  {
    "q": "¿Qué se produce sobre todo en la región pampeana?",
    "ops": [
      "Cereales y ganado",
      "Petróleo",
      "Azúcar"
    ],
    "m": "La llanura pampeana tiene los mejores suelos para agricultura y ganadería."
  },
  {
    "q": "¿Qué recurso se extrae en Neuquén (Vaca Muerta)?",
    "ops": [
      "Petróleo y gas",
      "Oro",
      "Algodón"
    ],
    "m": "Vaca Muerta es un yacimiento de petróleo y gas no convencional."
  },
  {
    "q": "¿Qué es un recurso NO renovable?",
    "ops": [
      "Uno que se agota, como el petróleo",
      "Uno que se repone solo",
      "Uno que no sirve"
    ],
    "m": "El petróleo tardó millones de años en formarse: no se repone."
  },
  {
    "q": "¿Qué se cultiva principalmente en Tucumán?",
    "ops": [
      "Caña de azúcar",
      "Trigo",
      "Vid"
    ],
    "m": "Tucumán es la principal provincia azucarera."
  },
  {
    "q": "¿Y en Mendoza?",
    "ops": [
      "Vid, para hacer vino",
      "Yerba mate",
      "Algodón"
    ],
    "m": "Mendoza es la principal provincia vitivinícola."
  },
  {
    "q": "¿De dónde viene la yerba mate?",
    "ops": [
      "De Misiones y Corrientes",
      "De la Patagonia",
      "De Buenos Aires"
    ],
    "m": "Necesita clima subtropical: se cultiva en el noreste."
  },
  {
    "q": "¿Qué es la pesca de altura?",
    "ops": [
      "La que se hace mar adentro con barcos grandes",
      "La que se hace desde la orilla",
      "La pesca en ríos"
    ],
    "m": "Se hace lejos de la costa, con embarcaciones preparadas."
  },
  {
    "q": "¿Qué energía se obtiene de una represa?",
    "ops": [
      "Hidroeléctrica",
      "Solar",
      "Eólica"
    ],
    "m": "Hidro = agua: la fuerza del agua mueve las turbinas."
  },
  {
    "q": "¿Dónde hay más parques eólicos en Argentina?",
    "ops": [
      "En la Patagonia, por el viento",
      "En el noreste",
      "En las sierras"
    ],
    "m": "La Patagonia tiene vientos fuertes y constantes."
  },
  {
    "q": "¿Qué actividad predomina en la Patagonia además del petróleo?",
    "ops": [
      "La cría de ovejas",
      "El cultivo de caña",
      "La yerba mate"
    ],
    "m": "La meseta patagónica se usa sobre todo para ganadería ovina."
  },
  {
    "q": "¿Qué problema trae usar mal un recurso natural?",
    "ops": [
      "Se puede agotar o contaminar",
      "Ninguno",
      "Se multiplica"
    ],
    "m": "El uso sin cuidado agota el recurso y daña el ambiente."
  },
  {
    "q": "¿Qué es la minería a cielo abierto?",
    "ops": [
      "Extraer minerales removiendo la superficie",
      "Buscar minerales en el mar",
      "Sembrar minerales"
    ],
    "m": "Se remueve gran cantidad de suelo; por eso genera debate ambiental."
  },
  {
    "q": "¿Qué región produce la mayor parte de la soja?",
    "ops": [
      "La pampeana y parte del norte",
      "La Patagonia",
      "Cuyo"
    ],
    "m": "La soja se expandió desde la pampa hacia el norte."
  },
  {
    "q": "¿Qué significa que un recurso sea renovable?",
    "ops": [
      "Que se repone si se usa con cuidado",
      "Que nunca se acaba pase lo que pase",
      "Que es artificial"
    ],
    "m": "Renovable no significa infinito: se repone SI se usa bien."
  }
];
GAMES.recursos_argentina = juegoTriviaTexto(CUR_RECURSOS_ARGENTINA_BANCO, "Elegí la respuesta correcta.", "recursos_a");

/* 7° · Recursos del poema — recursos_poema
   DC: Recursos literarios: comparación, metáfora, personificación, hipérbole
   Fuente: docs/auditoria-dc-caba/grado-7.md · L */
const CUR_RECURSOS_POEMA_BANCO = [
  {
    "q": "«Sus ojos son dos luceros»",
    "ops": [
      "Metáfora",
      "Comparación",
      "Hipérbole"
    ],
    "m": "Dice que SON, sin usar «como»: metáfora."
  },
  {
    "q": "«Sus ojos brillan COMO luceros»",
    "ops": [
      "Comparación",
      "Metáfora",
      "Hipérbole"
    ],
    "m": "Usa «como»: es una comparación."
  },
  {
    "q": "«El viento susurraba entre los árboles»",
    "ops": [
      "Personificación",
      "Comparación",
      "Hipérbole"
    ],
    "m": "Le da al viento algo humano (susurrar): personificación."
  },
  {
    "q": "«Te lo dije un millón de veces»",
    "ops": [
      "Hipérbole",
      "Metáfora",
      "Comparación"
    ],
    "m": "Exagera a propósito: hipérbole."
  },
  {
    "q": "«La luna sonríe en el cielo»",
    "ops": [
      "Personificación",
      "Comparación",
      "Hipérbole"
    ],
    "m": "Sonreír es humano: personificación."
  },
  {
    "q": "«Sus manos eran de hielo»",
    "ops": [
      "Metáfora",
      "Comparación",
      "Personificación"
    ],
    "m": "Dice que ERAN, sin «como»: metáfora."
  },
  {
    "q": "«Corría como el viento»",
    "ops": [
      "Comparación",
      "Metáfora",
      "Hipérbole"
    ],
    "m": "El «como» marca la comparación."
  },
  {
    "q": "«Tengo un hambre que me muero»",
    "ops": [
      "Hipérbole",
      "Metáfora",
      "Comparación"
    ],
    "m": "Exageración evidente: hipérbole."
  },
  {
    "q": "«Las olas acariciaban la orilla»",
    "ops": [
      "Personificación",
      "Hipérbole",
      "Comparación"
    ],
    "m": "Acariciar es humano: personificación."
  },
  {
    "q": "«Tus cabellos son oro»",
    "ops": [
      "Metáfora",
      "Comparación",
      "Personificación"
    ],
    "m": "Identifica una cosa con otra sin «como»."
  },
  {
    "q": "«Duerme como un tronco»",
    "ops": [
      "Comparación",
      "Metáfora",
      "Personificación"
    ],
    "m": "Con «como»: comparación."
  },
  {
    "q": "«El reloj devoraba los minutos»",
    "ops": [
      "Personificación",
      "Comparación",
      "Hipérbole"
    ],
    "m": "Devorar es propio de un ser vivo: personificación."
  },
  {
    "q": "«Esperé una eternidad»",
    "ops": [
      "Hipérbole",
      "Metáfora",
      "Comparación"
    ],
    "m": "Exagera el tiempo: hipérbole."
  },
  {
    "q": "«La vida es un viaje»",
    "ops": [
      "Metáfora",
      "Comparación",
      "Hipérbole"
    ],
    "m": "Identifica la vida con un viaje, sin «como»: metáfora."
  }
];
GAMES.recursos_poema = juegoTriviaTexto(CUR_RECURSOS_POEMA_BANCO, "¿Qué recurso usa?", "recursos_p");

/* 4° · El agua cambia — estados_agua_4
   DC: Cambios de estado del agua y el ciclo del agua
   Fuente: docs/auditoria-dc-caba/grado-4.md · N */
const CUR_ESTADOS_AGUA_4_BANCO = [
  {
    "q": "El agua del charco desaparece con el sol. ¿Qué pasó?",
    "ops": [
      "Se evaporó: pasó a vapor",
      "Se la tomó la tierra entera",
      "Desapareció"
    ],
    "m": "El calor la hace pasar a estado gaseoso: se evapora."
  },
  {
    "q": "¿Cómo se llama cuando el vapor vuelve a ser líquido?",
    "ops": [
      "Condensación",
      "Evaporación",
      "Congelación"
    ],
    "m": "Condensación: el vapor se enfría y vuelve a líquido, como en el vidrio."
  },
  {
    "q": "El agua en el freezer se hace hielo. ¿Cómo se llama?",
    "ops": [
      "Solidificación",
      "Evaporación",
      "Condensación"
    ],
    "m": "Pasa de líquido a sólido: se solidifica."
  },
  {
    "q": "¿A qué temperatura hierve el agua?",
    "ops": [
      "100 °C",
      "50 °C",
      "0 °C"
    ],
    "m": "A 100 °C hierve; a 0 °C se congela."
  },
  {
    "q": "¿A qué temperatura se congela el agua?",
    "ops": [
      "0 °C",
      "100 °C",
      "-50 °C"
    ],
    "m": "A 0 °C pasa a hielo."
  },
  {
    "q": "Las gotas en el vidrio frío de un vaso, ¿de dónde salen?",
    "ops": [
      "Del vapor del aire que se condensó",
      "Del agua de adentro que se escapó",
      "De la nada"
    ],
    "m": "El aire tiene vapor; al tocar el vidrio frío se condensa."
  },
  {
    "q": "¿Qué forma las nubes?",
    "ops": [
      "Vapor de agua que se condensó en gotitas",
      "Humo",
      "Aire caliente"
    ],
    "m": "El vapor sube, se enfría y se condensa: eso son las nubes."
  },
  {
    "q": "¿Por qué llueve?",
    "ops": [
      "Las gotitas de la nube se juntan y pesan demasiado",
      "Alguien tira agua",
      "El sol la empuja"
    ],
    "m": "Al juntarse, las gotas pesan y caen."
  },
  {
    "q": "El hielo se derrite. ¿Cómo se llama ese cambio?",
    "ops": [
      "Fusión",
      "Evaporación",
      "Condensación"
    ],
    "m": "Fusión: de sólido a líquido."
  },
  {
    "q": "¿El agua se gasta cuando se evapora?",
    "ops": [
      "No, cambia de estado y vuelve con la lluvia",
      "Sí, desaparece",
      "Sí, se convierte en aire"
    ],
    "m": "El ciclo del agua es un circuito: no se pierde, circula."
  },
  {
    "q": "La ropa se seca al sol porque…",
    "ops": [
      "El agua se evapora",
      "El sol se la toma",
      "El viento la empuja"
    ],
    "m": "El calor evapora el agua de la tela."
  },
  {
    "q": "¿Qué pasa con el agua del mar cuando se evapora?",
    "ops": [
      "Sube el agua y la sal queda",
      "Sube también la sal",
      "No se evapora"
    ],
    "m": "Sólo el agua se evapora: por eso la lluvia es dulce."
  },
  {
    "q": "¿En qué estado está el agua en una nube?",
    "ops": [
      "Líquido, en gotitas muy chiquitas",
      "Gaseoso siempre",
      "Sólido"
    ],
    "m": "La nube ya es agua condensada: gotitas suspendidas."
  },
  {
    "q": "¿El vapor de agua se ve?",
    "ops": [
      "No, es invisible; lo que se ve ya son gotitas",
      "Sí, es el humo blanco",
      "Sí, siempre"
    ],
    "m": "El «vaho» blanco de la pava ya es agua condensada, no vapor puro."
  }
];
GAMES.estados_agua_4 = juegoTriviaTexto(CUR_ESTADOS_AGUA_4_BANCO, "Elegí la respuesta correcta.", "estados_ag");

/* 7° · La población argentina — poblacion_argentina
   DC: Población: distribución, migraciones y condiciones de vida
   Fuente: docs/auditoria-dc-caba/grado-7.md · S */
const CUR_POBLACION_ARGENTINA_BANCO = [
  {
    "q": "¿Dónde vive la mayoría de la población argentina?",
    "ops": [
      "En ciudades",
      "En el campo",
      "En la montaña"
    ],
    "m": "Argentina es un país muy urbanizado: más del 90% vive en ciudades."
  },
  {
    "q": "¿Qué es una migración interna?",
    "ops": [
      "Mudarse de una provincia a otra dentro del país",
      "Irse a otro país",
      "Venir de otro país"
    ],
    "m": "Interna = dentro del mismo país."
  },
  {
    "q": "¿Por qué mucha gente migró del campo a la ciudad?",
    "ops": [
      "Buscando trabajo y servicios",
      "Porque les gustaba el ruido",
      "Porque se lo ordenaron"
    ],
    "m": "La industria y los servicios se concentraron en las ciudades."
  },
  {
    "q": "A fines del siglo XIX llegaron muchos inmigrantes. ¿De dónde, sobre todo?",
    "ops": [
      "De Europa, en especial Italia y España",
      "De Asia",
      "De Oceanía"
    ],
    "m": "La inmigración europea masiva cambió la sociedad argentina."
  },
  {
    "q": "¿Qué es la densidad de población?",
    "ops": [
      "Cuánta gente vive por kilómetro cuadrado",
      "Cuánta gente hay en total",
      "Cuánto mide el país"
    ],
    "m": "Relaciona la cantidad de gente con el espacio."
  },
  {
    "q": "¿Qué provincia concentra más población?",
    "ops": [
      "Buenos Aires",
      "La Rioja",
      "Santa Cruz"
    ],
    "m": "Buenos Aires y el AMBA concentran alrededor de un tercio del país."
  },
  {
    "q": "¿Cómo es la Patagonia en cuanto a población?",
    "ops": [
      "Muy poco poblada",
      "La más poblada",
      "Igual que Buenos Aires"
    ],
    "m": "Mucho territorio y poca gente: baja densidad."
  },
  {
    "q": "Hoy, ¿de dónde vienen la mayoría de los inmigrantes?",
    "ops": [
      "De países vecinos, como Paraguay y Bolivia",
      "De Europa",
      "De Estados Unidos"
    ],
    "m": "La inmigración limítrofe es la principal en las últimas décadas."
  },
  {
    "q": "¿Qué derechos tiene una persona migrante en Argentina?",
    "ops": [
      "Los mismos derechos: salud, educación y trabajo",
      "Ninguno",
      "Sólo a trabajar"
    ],
    "m": "La ley reconoce a la migración como un derecho humano."
  },
  {
    "q": "¿Qué es el éxodo rural?",
    "ops": [
      "La salida de gente del campo hacia las ciudades",
      "Un viaje de vacaciones",
      "La llegada de gente al campo"
    ],
    "m": "Es el movimiento del campo a la ciudad."
  },
  {
    "q": "¿Qué significa que la población esté «envejecida»?",
    "ops": [
      "Que hay más proporción de personas mayores",
      "Que la gente vive poco",
      "Que nacen más chicos"
    ],
    "m": "Pasa cuando bajan los nacimientos y sube la esperanza de vida."
  },
  {
    "q": "¿Qué es un censo?",
    "ops": [
      "El conteo oficial de toda la población",
      "Una elección",
      "Un impuesto"
    ],
    "m": "Sirve para saber cuánta gente hay y cómo vive, y planificar."
  },
  {
    "q": "¿Por qué importa saber cómo se distribuye la población?",
    "ops": [
      "Para planificar escuelas, hospitales y transporte",
      "Para nada",
      "Sólo por curiosidad"
    ],
    "m": "Sin ese dato no se puede planificar dónde hacen falta servicios."
  },
  {
    "q": "Las villas y asentamientos muestran…",
    "ops": [
      "Un problema de acceso a la vivienda",
      "Que sobra lugar",
      "Que la gente prefiere vivir así"
    ],
    "m": "Reflejan desigualdad en el acceso a la vivienda, no una elección."
  }
];
GAMES.poblacion_argentina = juegoTriviaTexto(CUR_POBLACION_ARGENTINA_BANCO, "Elegí la respuesta correcta.", "poblacion_");

/* 7° · Vivir en democracia — democracia_argentina
   DC: La democracia argentina: derechos, participación y memoria
   Fuente: docs/auditoria-dc-caba/grado-7.md · S */
const CUR_DEMOCRACIA_ARGENTINA_BANCO = [
  {
    "q": "¿Qué es una democracia?",
    "ops": [
      "Un sistema donde el pueblo elige a sus gobernantes",
      "Un sistema donde manda una sola persona",
      "Un sistema sin leyes"
    ],
    "m": "El poder viene del voto de la gente y se renueva."
  },
  {
    "q": "¿Qué se elige en una elección legislativa?",
    "ops": [
      "Diputados y senadores",
      "El presidente",
      "Los jueces"
    ],
    "m": "El Poder Legislativo se renueva por partes, no todo junto."
  },
  {
    "q": "¿Qué pasó durante la última dictadura (1976-1983)?",
    "ops": [
      "Se violaron los derechos humanos y hubo desaparecidos",
      "Hubo elecciones normales",
      "No pasó nada especial"
    ],
    "m": "Fue un gobierno de facto: sin elecciones y con graves violaciones a los derechos humanos."
  },
  {
    "q": "¿Qué se recuerda el 24 de marzo?",
    "ops": [
      "El Día de la Memoria por la Verdad y la Justicia",
      "El día de la independencia",
      "El día del trabajador"
    ],
    "m": "Recuerda el golpe de 1976 y a sus víctimas."
  },
  {
    "q": "¿Quiénes son las Madres y Abuelas de Plaza de Mayo?",
    "ops": [
      "Familiares que reclaman por los desaparecidos",
      "Un partido político",
      "Un club"
    ],
    "m": "Buscan a sus hijos y nietos desde la dictadura hasta hoy."
  },
  {
    "q": "¿Qué significa que el voto sea SECRETO?",
    "ops": [
      "Que nadie puede saber a quién votaste",
      "Que no se cuenta",
      "Que se vota a escondidas del Estado"
    ],
    "m": "Protege tu libertad: nadie puede presionarte por tu voto."
  },
  {
    "q": "Además de votar, ¿cómo se puede participar?",
    "ops": [
      "En centros de estudiantes, asambleas, organizaciones",
      "Sólo votando",
      "No se puede de otra forma"
    ],
    "m": "La democracia no se agota en el voto: la participación es cotidiana."
  },
  {
    "q": "¿Puede un gobierno democrático suspender la Constitución?",
    "ops": [
      "No, tiene que respetarla",
      "Sí, cuando quiera",
      "Sí, si gana con muchos votos"
    ],
    "m": "El límite de todo gobierno es la Constitución."
  },
  {
    "q": "¿Qué es la libertad de expresión?",
    "ops": [
      "Poder opinar sin ser perseguido por eso",
      "Poder decir mentiras sin consecuencias",
      "Poder insultar"
    ],
    "m": "Es un derecho que protege la crítica, incluso al gobierno."
  },
  {
    "q": "¿Qué es el voto obligatorio?",
    "ops": [
      "Que a partir de los 18 hay deber de votar",
      "Que hay que votar a un partido fijo",
      "Que se vota dos veces"
    ],
    "m": "Desde los 16 se puede votar; desde los 18 es un deber."
  },
  {
    "q": "¿Para qué sirve que haya varios partidos políticos?",
    "ops": [
      "Para que haya opciones distintas para elegir",
      "Para confundir",
      "Para que gane siempre el mismo"
    ],
    "m": "El pluralismo es parte de lo que hace democrática a una elección."
  },
  {
    "q": "¿Por qué el voto es obligatorio en la Argentina?",
    "ops": [
      "Porque votar es un derecho y también un deber cívico",
      "Porque lo decide cada provincia",
      "Porque hay pocos votantes"
    ],
    "m": "Desde 1912 el voto es universal, secreto y obligatorio."
  },
  {
    "q": "¿Los derechos humanos se pueden perder?",
    "ops": [
      "No, se tienen por ser persona",
      "Sí, si te portás mal",
      "Sí, si no votás"
    ],
    "m": "Son inalienables: no dependen de portarse bien ni de un gobierno."
  },
  {
    "q": "¿Qué pasa si un gobierno no respeta la ley?",
    "ops": [
      "La Justicia puede controlarlo y limitarlo",
      "No pasa nada",
      "Se disuelve el país"
    ],
    "m": "La división de poderes existe justamente para eso."
  }
];
GAMES.democracia_argentina = juegoTriviaTexto(CUR_DEMOCRACIA_ARGENTINA_BANCO, "Elegí la respuesta correcta.", "democracia");

/* 4° · Modelador de paisaje — erosion_4
   DC: Erosión, transporte y depósito
   Fuente: docs/auditoria-dc-caba/grado-4.md · N1 */
const CUR_EROSION_4_BANCO = [
  {
    "it": "El viento sopla contra la roca del cerro y le va sacando polvo",
    "cat": "erosion",
    "m": "El viento le saca material a la roca: la desgasta."
  },
  {
    "it": "El río arrastra piedritas durante kilómetros",
    "cat": "transporte",
    "m": "Las piedritas están viajando: el río las lleva de un lugar a otro."
  },
  {
    "it": "En la desembocadura del río se forma un banco de arena",
    "cat": "deposito",
    "m": "El material terminó su viaje y se quedó ahí."
  },
  {
    "it": "El hielo del glaciar raspa la piedra por donde pasa",
    "cat": "erosion",
    "m": "El glaciar raspa: le saca material a la roca."
  },
  {
    "it": "Después de la creciente queda barro nuevo en la orilla",
    "cat": "deposito",
    "m": "El barro venía viajando en el agua y quedó donde el agua perdió fuerza."
  },
  {
    "it": "El agua de lluvia va abriendo un surco en la ladera",
    "cat": "erosion",
    "m": "Para abrir el surco el agua tuvo que sacarle tierra a la ladera."
  },
  {
    "it": "Las olas empujan la arena a lo largo de la playa",
    "cat": "transporte",
    "m": "La arena se está moviendo de un lugar a otro de la playa."
  },
  {
    "it": "Al pie del cerro hay un montón de piedras sueltas",
    "cat": "deposito",
    "m": "Las piedras se soltaron arriba, cayeron y ahí terminaron. Cuidado: el desgaste pasó ARRIBA; lo que ves al pie es dónde quedaron."
  },
  {
    "it": "El viento levanta arena del médano y la lleva lejos",
    "cat": "transporte",
    "m": "La arena va en el aire, viajando."
  },
  {
    "it": "La raíz del árbol parte la roca en dos",
    "cat": "erosion",
    "m": "La raíz rompe la roca: también es desgaste, aunque lo haga un ser vivo."
  },
  {
    "it": "En el fondo del lago se van juntando capas de limo",
    "cat": "deposito",
    "m": "El limo llegó con el agua y se quedó en el fondo, capa sobre capa."
  },
  {
    "it": "Un alud baja piedras y tierra por la ladera",
    "cat": "transporte",
    "m": "Todo ese material está bajando: está viajando, todavía no llegó."
  },
  {
    "it": "La sal del mar va carcomiendo el acantilado",
    "cat": "erosion",
    "m": "El acantilado pierde material: se desgasta."
  },
  {
    "it": "Cuando baja la creciente, el valle queda con tierra nueva y fértil",
    "cat": "deposito",
    "m": "Esa tierra vino de más arriba y quedó en el valle. Por eso los valles de río son buenos para sembrar."
  },
  {
    "it": "El agua se congela dentro de una grieta y la agranda",
    "cat": "erosion",
    "m": "Al congelarse el agua ocupa más lugar y rompe la roca desde adentro."
  },
  {
    "it": "El camión de la cantera lleva las piedras a la ciudad",
    "cat": "transporte",
    "m": "También es transporte, pero lo hace una persona y no la naturaleza: el material igual está viajando."
  }
];
GAMES.erosion_4 = juegoClasificar(CUR_EROSION_4_BANCO, "¿Qué está pasando con el material?", [{"cat": "erosion", "label": "🪨 Se desgasta"}, {"cat": "transporte", "label": "🌊 Viaja"}, {"cat": "deposito", "label": "🏖️ Se queda"}], "erosion_4");

/* 4° · Placas en movimiento — placas_4
   DC: Tectónica de placas; bordes activos; formación del relieve
   Fuente: docs/auditoria-dc-caba/grado-4.md · N2 */
const CUR_PLACAS_4_BANCO = [
  {
    "q": "¿Sobre qué apoya la corteza de la Tierra?",
    "ops": [
      "Sobre placas que se mueven muy despacio",
      "Sobre una sola cáscara quieta",
      "Sobre agua"
    ],
    "m": "La corteza está partida en placas y todas se mueven, aunque tan despacio que no lo sentimos."
  },
  {
    "q": "¿Qué pasa cuando dos placas chocan de frente?",
    "ops": [
      "Se levantan montañas",
      "Se hace un agujero",
      "No pasa nada"
    ],
    "m": "El choque arruga la corteza hacia arriba: así se formó la cordillera de los Andes."
  },
  {
    "q": "¿Por qué la Argentina tiene los Andes justo en el oeste?",
    "ops": [
      "Porque ahí choca la placa del océano con la de América del Sur",
      "Porque el viento apiló tierra",
      "Porque el río la levantó"
    ],
    "m": "El borde entre las dos placas pasa por el oeste: por eso la montaña está de ese lado y no en el medio del país."
  },
  {
    "q": "¿Qué es un terremoto?",
    "ops": [
      "El temblor cuando las placas se traban y se sueltan de golpe",
      "Un pozo que se abre solo",
      "Lluvia muy fuerte"
    ],
    "m": "Las placas empujan, se traban y cuando se sueltan liberan la energía de golpe: eso es el temblor."
  },
  {
    "q": "¿Dónde hay más terremotos y volcanes?",
    "ops": [
      "En los bordes de las placas",
      "En el medio de las placas",
      "En todos lados por igual"
    ],
    "m": "En el medio de una placa casi no pasa nada; la acción está en los bordes."
  },
  {
    "q": "¿Qué sale por un volcán?",
    "ops": [
      "Roca derretida que viene de abajo de la corteza",
      "Agua caliente del mar",
      "Aire comprimido"
    ],
    "m": "El magma es roca fundida que estaba debajo y encuentra una salida."
  },
  {
    "q": "¿Las placas se mueven rápido?",
    "ops": [
      "Unos pocos centímetros por año",
      "Varios metros por día",
      "A la velocidad de un auto"
    ],
    "m": "Se mueven más o menos lo que te crecen las uñas en un año. Por eso hacen falta millones de años para levantar una montaña."
  },
  {
    "q": "Si una montaña se está levantando, ¿por qué no crece sin parar?",
    "ops": [
      "Porque la erosión la desgasta al mismo tiempo",
      "Porque las placas se cansan",
      "Porque llega hasta las nubes y frena"
    ],
    "m": "Mientras el choque la empuja hacia arriba, el agua y el viento la desgastan: las dos cosas pasan a la vez."
  },
  {
    "q": "¿Qué pasa cuando dos placas se SEPARAN?",
    "ops": [
      "Sube material de abajo y se hace corteza nueva",
      "Queda un vacío",
      "Se juntan de nuevo enseguida"
    ],
    "m": "Por la grieta sube magma que se enfría y forma corteza nueva."
  },
  {
    "q": "En el medio de la llanura pampeana casi no tiembla. ¿Por qué?",
    "ops": [
      "Porque está lejos del borde de la placa",
      "Porque el suelo es blando",
      "Porque es una zona baja"
    ],
    "m": "La Pampa está en el medio de la placa; los bordes activos quedan lejos."
  },
  {
    "q": "¿Se puede saber el día exacto en que va a haber un terremoto?",
    "ops": [
      "No, sólo se sabe qué zonas son riesgosas",
      "Sí, con una semana de aviso",
      "Sí, los volcanes avisan siempre"
    ],
    "m": "Se conocen las zonas de riesgo y se construye preparado, pero la fecha exacta no se puede predecir."
  },
  {
    "q": "¿Cómo se llama el relieve alto y plano, como una mesa?",
    "ops": [
      "Meseta",
      "Llanura",
      "Cordillera"
    ],
    "m": "La meseta es alta como la montaña pero plana arriba, como una mesa."
  },
  {
    "q": "Encuentran fósiles marinos en lo alto de los Andes. ¿Qué explica eso?",
    "ops": [
      "Ese lugar estuvo bajo el mar y las placas lo levantaron",
      "Alguien los subió",
      "Los peces subieron nadando"
    ],
    "m": "El choque de placas levantó fondo marino hasta la altura de la montaña."
  },
  {
    "q": "¿Qué es el epicentro de un terremoto?",
    "ops": [
      "El punto de la superficie justo arriba de donde se soltó la placa",
      "El lugar donde más casas hay",
      "El centro de la Tierra"
    ],
    "m": "Es dónde se siente más fuerte, porque queda justo encima del origen."
  }
];
GAMES.placas_4 = juegoTriviaTexto(CUR_PLACAS_4_BANCO, "¿Qué pasa cuando la Tierra se mueve?", "placas_4");

/* 4° · Huellas del tiempo — fosiles_4
   DC: Fósiles; escala de tiempo geológico frente a la humana
   Fuente: docs/auditoria-dc-caba/grado-4.md · N3 */
const CUR_FOSILES_4_BANCO = [
  {
    "items": [
      "Capa de abajo: caracoles de mar",
      "Capa del medio: hojas de helecho",
      "Capa de arriba: huella de ave"
    ]
  },
  {
    "items": [
      "Aparecen los primeros seres vivos en el mar",
      "Aparecen los peces",
      "Aparecen los dinosaurios",
      "Aparecen los seres humanos"
    ]
  },
  {
    "items": [
      "Capa de arena del fondo del mar",
      "Capa de barro de laguna",
      "Capa de tierra con raíces",
      "El pasto de hoy"
    ]
  },
  {
    "items": [
      "Se extinguen los dinosaurios",
      "Aparecen los primeros mamíferos grandes",
      "Aparecen los seres humanos",
      "Se inventa la escritura"
    ]
  },
  {
    "items": [
      "Un animal muere y queda tapado por barro",
      "El barro se endurece y se hace roca",
      "El agua y el viento gastan la roca de arriba",
      "Alguien encuentra el fósil"
    ]
  },
  {
    "items": [
      "Capa con fósiles de trilobites",
      "Capa con fósiles de dinosaurio",
      "Capa con fósiles de gliptodonte"
    ]
  },
  {
    "items": [
      "Se forma la Tierra",
      "Aparece la vida en el mar",
      "La vida sale del agua a la tierra firme",
      "Aparecen las flores"
    ]
  },
  {
    "items": [
      "Vivían los gliptodontes en la Pampa",
      "Llegaron los primeros pueblos a América",
      "Se fundó Buenos Aires por segunda vez",
      "Nacieron tus abuelos"
    ]
  },
  {
    "items": [
      "Un tronco queda enterrado en ceniza volcánica",
      "La madera se reemplaza por mineral",
      "Queda un tronco de piedra"
    ]
  },
  {
    "items": [
      "Capa de abajo: peces",
      "Capa: anfibios",
      "Capa: reptiles",
      "Capa de arriba: mamíferos"
    ]
  },
  {
    "items": [
      "La huella se marca en el barro blando",
      "El sol seca el barro y la huella queda dura",
      "Otra capa la tapa y la protege",
      "Millones de años después se descubre"
    ]
  },
  {
    "items": [
      "Los dinosaurios caminaban por la Patagonia",
      "Se extinguieron los dinosaurios",
      "Aparecieron los primeros seres humanos"
    ]
  }
];
GAMES.fosiles_4 = juegoOrdenar(CUR_FOSILES_4_BANCO, "Ordená del MÁS ANTIGUO al MÁS NUEVO. Tocá en orden.", "En las capas de roca, lo de abajo se depositó primero: es lo más viejo.", "fosiles_4");

/* 4° · Armá el movimiento — movimiento_cuerpo_4
   DC: Sistema osteo-artro-muscular: huesos, músculos y articulaciones
   Fuente: docs/auditoria-dc-caba/grado-4.md · N4 */
const CUR_MOVIMIENTO_CUERPO_4_BANCO = [
  {
    "q": "¿Qué hace un músculo para mover un hueso?",
    "ops": [
      "Se acorta y TIRA del hueso",
      "Empuja el hueso",
      "Le da aire al hueso"
    ],
    "m": "El músculo sólo puede tirar, nunca empujar. Por eso los músculos trabajan de a pares: uno tira para un lado y el otro para el otro."
  },
  {
    "q": "Para estirar el brazo después de doblarlo, ¿qué pasa?",
    "ops": [
      "Tira el músculo del otro lado del brazo",
      "El mismo músculo empuja al revés",
      "El hueso vuelve solo"
    ],
    "m": "El bíceps dobla y el tríceps estira. Como el músculo sólo tira, hace falta uno de cada lado."
  },
  {
    "q": "¿Qué es una articulación?",
    "ops": [
      "El lugar donde se unen dos huesos y pueden moverse",
      "Un músculo redondo",
      "La punta del hueso"
    ],
    "m": "Es la unión que permite el movimiento: sin articulaciones el esqueleto sería una sola pieza rígida."
  },
  {
    "q": "¿Por qué el codo se dobla para un solo lado?",
    "ops": [
      "Porque es una articulación tipo bisagra",
      "Porque el hueso es corto",
      "Porque el músculo es débil"
    ],
    "m": "El codo es una bisagra, como la de una puerta. El hombro en cambio gira para todos lados."
  },
  {
    "q": "¿Qué une el músculo al hueso?",
    "ops": [
      "El tendón",
      "La piel",
      "La sangre"
    ],
    "m": "El tendón es la cuerda que transmite el tirón del músculo al hueso."
  },
  {
    "q": "¿Para qué sirven las costillas?",
    "ops": [
      "Protegen el corazón y los pulmones",
      "Ayudan a caminar",
      "Sostienen la cabeza"
    ],
    "m": "El esqueleto también protege, no sólo sostiene: costillas y cráneo son armaduras."
  },
  {
    "q": "¿El esqueleto está vivo?",
    "ops": [
      "Sí, los huesos crecen y se reparan solos",
      "No, es como una piedra",
      "Sólo de chico"
    ],
    "m": "Por eso un hueso roto se suelda: está vivo y se repara."
  },
  {
    "q": "Un insecto tiene el esqueleto por fuera. ¿Qué ventaja tiene el nuestro por dentro?",
    "ops": [
      "Puede crecer con nosotros sin cambiarlo",
      "Es más duro",
      "Pesa más"
    ],
    "m": "El insecto tiene que largar el caparazón para crecer; nuestro hueso crece con nosotros."
  },
  {
    "q": "¿Qué protege el cráneo?",
    "ops": [
      "El cerebro",
      "El corazón",
      "El estómago"
    ],
    "m": "El cráneo es una caja de hueso alrededor del cerebro."
  },
  {
    "q": "¿Los músculos se mueven solos o los manda algo?",
    "ops": [
      "El cerebro les manda la orden por los nervios",
      "Se mueven solos",
      "Los mueve la sangre"
    ],
    "m": "Sin la orden del cerebro no hay movimiento: por eso hablamos de sistema osteo-artro-muscular Y nervioso trabajando juntos."
  },
  {
    "q": "¿Qué hay entre los huesos de una articulación para que no se rocen?",
    "ops": [
      "Cartílago, más blando que el hueso",
      "Nada, se tocan directo",
      "Otro hueso chiquito"
    ],
    "m": "El cartílago amortigua y evita que hueso contra hueso se gaste."
  },
  {
    "q": "El corazón también es un músculo. ¿Qué tiene de distinto?",
    "ops": [
      "Trabaja sin que se lo mandemos",
      "No se mueve",
      "Está pegado a un hueso"
    ],
    "m": "Hay músculos que movemos a voluntad y otros, como el corazón, que trabajan solos toda la vida."
  },
  {
    "q": "Si el bíceps se acorta, ¿qué hace el brazo?",
    "ops": [
      "Se dobla",
      "Se estira",
      "Se queda igual"
    ],
    "m": "Al acortarse tira del antebrazo hacia arriba: el brazo se dobla."
  },
  {
    "q": "¿Por qué la columna está hecha de muchos huesitos y no de uno solo?",
    "ops": [
      "Para poder doblarse y girar",
      "Porque uno solo sería muy caro",
      "Para pesar menos"
    ],
    "m": "Las vértebras dan una espalda firme pero flexible: un solo hueso largo no dejaría agacharse."
  },
  {
    "q": "¿Qué pasa con un músculo que no se usa nunca?",
    "ops": [
      "Se debilita y se achica",
      "Se pone más fuerte",
      "Se convierte en hueso"
    ],
    "m": "El músculo responde al uso: se fortalece si trabaja y se atrofia si no."
  },
  {
    "q": "Al levantar una mochila pesada, ¿qué conviene?",
    "ops": [
      "Doblar las rodillas y usar las piernas",
      "Doblar la espalda",
      "Levantarla de golpe"
    ],
    "m": "Las piernas tienen los músculos más fuertes; la espalda doblada concentra el esfuerzo en la columna."
  }
];
GAMES.movimiento_cuerpo_4 = juegoTriviaTexto(CUR_MOVIMIENTO_CUERPO_4_BANCO, "¿Cómo se mueve el cuerpo?", "movimiento");

/* 4° · Laboratorio de imanes — imanes_4
   DC: Magnetismo: dos polos, atracción y repulsión; electrostática
   Fuente: docs/auditoria-dc-caba/grado-4.md · N5 */
const CUR_IMANES_4_BANCO = [
  {
    "q": "Acercás el polo norte de un imán al polo norte de otro. ¿Qué pasa?",
    "ops": [
      "Se rechazan",
      "Se pegan",
      "No pasa nada"
    ],
    "m": "Polos iguales se rechazan; polos distintos se atraen."
  },
  {
    "q": "Acercás el polo norte al polo sur. ¿Qué pasa?",
    "ops": [
      "Se pegan",
      "Se rechazan",
      "El imán se apaga"
    ],
    "m": "Distintos se atraen: norte con sur."
  },
  {
    "q": "Partís un imán al medio. ¿Qué queda?",
    "ops": [
      "Dos imanes, cada uno con sus dos polos",
      "Un imán norte y un imán sur",
      "Dos pedazos sin fuerza"
    ],
    "m": "Nunca se puede tener un polo solo: por chiquito que sea el pedazo, siempre tiene norte Y sur."
  },
  {
    "q": "¿A cuál de estos atrae un imán?",
    "ops": [
      "Un clavo de hierro",
      "Una cuchara de plástico",
      "Una moneda de aluminio"
    ],
    "m": "El imán atrae hierro, níquel y cobalto. No atrae todos los metales."
  },
  {
    "q": "¿El imán atrae al oro y al aluminio?",
    "ops": [
      "No, aunque sean metales",
      "Sí, atrae todos los metales",
      "Sólo si están calientes"
    ],
    "m": "Error común: pensar que 'metal = lo atrae el imán'. Sólo algunos metales."
  },
  {
    "q": "Ponés una hoja de papel entre el imán y el clavo. ¿Qué pasa?",
    "ops": [
      "Lo atrae igual, a través del papel",
      "Deja de atraerlo",
      "El papel se imanta"
    ],
    "m": "La fuerza del imán atraviesa materiales que no son magnéticos."
  },
  {
    "q": "Alejás el imán del clavo. ¿Qué pasa con la fuerza?",
    "ops": [
      "Se hace más débil",
      "Se hace más fuerte",
      "Queda igual"
    ],
    "m": "La fuerza magnética se debilita rápido con la distancia."
  },
  {
    "q": "Frotás una regla de plástico con lana y la acercás a papelitos. ¿Qué pasa?",
    "ops": [
      "Los papelitos suben pegados a la regla",
      "No pasa nada",
      "Los papelitos se mojan"
    ],
    "m": "Al frotarla queda cargada: eso es electricidad estática, no magnetismo."
  },
  {
    "q": "Esa regla frotada, ¿atrae también un clavo de hierro?",
    "ops": [
      "Puede atraer cosas livianas, sea o no de hierro",
      "Sólo hierro, como el imán",
      "Nada, sólo papel"
    ],
    "m": "Diferencia clave: el imán elige el material; la carga estática atrae cualquier cosa liviana."
  },
  {
    "q": "Después de un rato la regla frotada deja de atraer. ¿Y el imán?",
    "ops": [
      "El imán sigue funcionando",
      "También se apaga",
      "El imán se apaga primero"
    ],
    "m": "La carga estática se pierde; el imán mantiene su fuerza."
  },
  {
    "q": "¿Por qué la aguja de una brújula siempre apunta al norte?",
    "ops": [
      "Porque la Tierra se comporta como un imán gigante",
      "Porque el norte está más alto",
      "Porque el sol la empuja"
    ],
    "m": "La Tierra tiene su propio campo magnético y la aguja se alinea con él."
  },
  {
    "q": "Pasás un imán muchas veces por un clavo, siempre en el mismo sentido. ¿Qué pasa?",
    "ops": [
      "El clavo queda imantado un rato",
      "El clavo se rompe",
      "El imán pierde el norte"
    ],
    "m": "El hierro se puede imantar por contacto: es imán temporal."
  },
  {
    "q": "Dos imanes se rechazan. ¿Qué tenés que hacer para que se peguen?",
    "ops": [
      "Dar vuelta uno de los dos",
      "Apretarlos más fuerte",
      "Calentarlos"
    ],
    "m": "Al darlo vuelta enfrentás polos distintos y se atraen."
  },
  {
    "q": "¿La fuerza del imán necesita que se toquen las cosas?",
    "ops": [
      "No, actúa a distancia",
      "Sí, siempre",
      "Sólo bajo el agua"
    ],
    "m": "Es una fuerza a distancia: se nota antes de que se toquen."
  },
  {
    "q": "Acercás un imán a un montón de arena de la playa. ¿Qué puede pasar?",
    "ops": [
      "Se le pegan granitos oscuros con hierro",
      "Se pega toda la arena",
      "No se pega nada nunca"
    ],
    "m": "Parte de la arena tiene granos de hierro: el imán los separa del resto."
  },
  {
    "q": "¿Se puede blindar un imán para que no atraiga?",
    "ops": [
      "Sí, tapándolo con una chapa de hierro",
      "No, es imposible",
      "Sí, con una hoja de papel"
    ],
    "m": "El hierro desvía las líneas del campo y protege lo que está detrás; el papel no hace nada."
  }
];
GAMES.imanes_4 = juegoTriviaTexto(CUR_IMANES_4_BANCO, "Antes de probar: ¿qué va a pasar?", "imanes_4");

/* 4° · Objeto o material — objeto_material_4
   DC: Natural y artificial; objeto no es material; propiedades y usos
   Fuente: docs/auditoria-dc-caba/grado-4.md · N7 */
const CUR_OBJETO_MATERIAL_4_BANCO = [
  {
    "it": "La madera",
    "cat": "natural",
    "m": "Se saca del árbol tal como está: es un material natural."
  },
  {
    "it": "El vidrio",
    "cat": "transformado",
    "m": "El vidrio no se junta: se fabrica fundiendo arena a muchísima temperatura. La arena es natural, el vidrio no."
  },
  {
    "it": "La silla",
    "cat": "objeto",
    "m": "La silla no es un material: es un objeto HECHO de materiales (madera, metal, tela)."
  },
  {
    "it": "El algodón",
    "cat": "natural",
    "m": "Sale de la planta de algodón."
  },
  {
    "it": "El papel",
    "cat": "transformado",
    "m": "Se fabrica a partir de la madera del árbol."
  },
  {
    "it": "El martillo",
    "cat": "objeto",
    "m": "Es un objeto. Sus materiales son el hierro y la madera."
  },
  {
    "it": "La lana",
    "cat": "natural",
    "m": "Se esquila de la oveja."
  },
  {
    "it": "El plástico",
    "cat": "transformado",
    "m": "Se fabrica a partir del petróleo."
  },
  {
    "it": "La piedra",
    "cat": "natural",
    "m": "Está en la naturaleza y se usa tal cual."
  },
  {
    "it": "El cuaderno",
    "cat": "objeto",
    "m": "Es un objeto de papel y cartón."
  },
  {
    "it": "El acero",
    "cat": "transformado",
    "m": "Se fabrica a partir del hierro más un poco de carbono."
  },
  {
    "it": "El agua",
    "cat": "natural",
    "m": "Es un material natural."
  },
  {
    "it": "El cuero",
    "cat": "natural",
    "m": "Sale del animal, aunque después se curta para conservarlo."
  },
  {
    "it": "La botella",
    "cat": "objeto",
    "m": "Es un objeto. Puede ser DE vidrio o DE plástico: el mismo objeto con materiales distintos."
  },
  {
    "it": "El cemento",
    "cat": "transformado",
    "m": "Se fabrica calcinando piedra caliza."
  },
  {
    "it": "La arena",
    "cat": "natural",
    "m": "Está en la naturaleza; con ella se fabrica el vidrio."
  },
  {
    "it": "El ladrillo",
    "cat": "transformado",
    "m": "Se fabrica cocinando arcilla en un horno."
  },
  {
    "it": "La cuchara",
    "cat": "objeto",
    "m": "Objeto. Puede ser de metal, de madera o de plástico."
  }
];
GAMES.objeto_material_4 = juegoClasificar(CUR_OBJETO_MATERIAL_4_BANCO, "¿De dónde sale este material?", [{"cat": "natural", "label": "🌿 Se saca de la naturaleza"}, {"cat": "transformado", "label": "🔥 Se fabrica a partir de otro"}, {"cat": "objeto", "label": "🔧 No es material: es un objeto"}], "objeto_mat");

/* 4° · El cielo de Buenos Aires — cielo_4
   DC: Movimiento diario del Sol; día y noche; sombras y estaciones
   Fuente: docs/auditoria-dc-caba/grado-4.md · N8 */
const CUR_CIELO_4_BANCO = [
  {
    "q": "¿Por qué hay día y noche?",
    "ops": [
      "Porque la Tierra gira sobre sí misma",
      "Porque la Luna tapa el Sol",
      "Porque el Sol se apaga"
    ],
    "m": "La Luna NO tiene nada que ver con el día y la noche: es el giro de la Tierra sobre su eje, una vuelta cada 24 horas."
  },
  {
    "q": "¿Por dónde aparece el Sol a la mañana?",
    "ops": [
      "Por el este",
      "Por el oeste",
      "Por el norte"
    ],
    "m": "Sale por el este y se pone por el oeste, todos los días del año."
  },
  {
    "q": "¿En qué momento del día la sombra es más corta?",
    "ops": [
      "Al mediodía",
      "A la mañana temprano",
      "Al atardecer"
    ],
    "m": "Cuanto más alto está el Sol, más corta es la sombra. Al mediodía está en su punto más alto."
  },
  {
    "q": "A la tarde, ¿hacia dónde se alarga tu sombra?",
    "ops": [
      "Hacia el este, del lado contrario al Sol",
      "Hacia el oeste, hacia el Sol",
      "Siempre hacia el sur"
    ],
    "m": "La sombra siempre cae del lado opuesto al Sol. Si el Sol está al oeste, la sombra va al este."
  },
  {
    "q": "¿Por qué en verano hace más calor?",
    "ops": [
      "Porque los rayos del Sol llegan más derechos y el día es más largo",
      "Porque la Tierra está más cerca del Sol",
      "Porque el Sol crece"
    ],
    "m": "No es la distancia: es la inclinación del eje de la Tierra. Los rayos llegan más derechos y calientan más."
  },
  {
    "q": "¿Cuándo es el día más largo del año en Buenos Aires?",
    "ops": [
      "En diciembre",
      "En junio",
      "En marzo"
    ],
    "m": "En el hemisferio sur el día más largo es en diciembre, al empezar el verano. En Europa es al revés."
  },
  {
    "q": "En junio en Buenos Aires, ¿qué pasa?",
    "ops": [
      "Es invierno y el día es corto",
      "Es verano y el día es largo",
      "Es primavera"
    ],
    "m": "Cuando en Europa es verano, acá es invierno: los hemisferios están al revés."
  },
  {
    "q": "¿Cuánto tarda la Tierra en dar una vuelta alrededor del Sol?",
    "ops": [
      "Un año",
      "Un día",
      "Un mes"
    ],
    "m": "Sobre sí misma: un día. Alrededor del Sol: un año."
  },
  {
    "q": "¿La Luna tiene luz propia?",
    "ops": [
      "No, refleja la luz del Sol",
      "Sí, es una estrella chiquita",
      "Sí, de noche se prende"
    ],
    "m": "La Luna sólo refleja: por eso cambia de forma según cómo le pega el Sol."
  },
  {
    "q": "Si a la mañana tu sombra apunta al oeste, ¿dónde está el Sol?",
    "ops": [
      "En el este",
      "En el oeste",
      "Arriba de todo"
    ],
    "m": "La sombra apunta al lado contrario del Sol. Sirve para orientarse sin brújula."
  },
  {
    "q": "¿Por qué parece que el Sol se mueve por el cielo?",
    "ops": [
      "Porque la que se mueve es la Tierra",
      "Porque el Sol da vueltas alrededor nuestro",
      "Porque las nubes lo empujan"
    ],
    "m": "Nos movemos nosotros: el Sol se ve moverse igual que se ven pasar los árboles desde el auto."
  },
  {
    "q": "En verano el Sol al mediodía está más alto que en invierno. ¿Y la sombra?",
    "ops": [
      "Más corta en verano",
      "Más larga en verano",
      "Igual todo el año"
    ],
    "m": "Sol más alto, sombra más corta. Por eso el largo de la sombra al mediodía sirve para saber la época del año."
  },
  {
    "q": "¿Las estrellas están sólo de noche?",
    "ops": [
      "Están siempre, pero de día no se ven por la luz del Sol",
      "Se prenden a la noche",
      "Se van a otro lado"
    ],
    "m": "Siguen ahí: la luz del Sol es tan fuerte que las tapa."
  },
  {
    "q": "¿Qué es el mediodía solar?",
    "ops": [
      "El momento en que el Sol está en su punto más alto",
      "Las 12 en punto del reloj siempre",
      "Cuando empieza a hacer calor"
    ],
    "m": "No coincide exacto con las 12 del reloj: el reloj usa husos horarios."
  },
  {
    "q": "En el hemisferio sur, al mediodía el Sol se ve hacia…",
    "ops": [
      "El norte",
      "El sur",
      "El este"
    ],
    "m": "Acá el Sol al mediodía queda hacia el norte; en Europa queda hacia el sur."
  },
  {
    "q": "¿Por qué el eje de la Tierra causa las estaciones?",
    "ops": [
      "Porque está inclinado y cada hemisferio recibe el Sol más derecho por turnos",
      "Porque la órbita es un cuadrado",
      "Porque el eje se dobla en verano"
    ],
    "m": "La inclinación es fija: lo que cambia es qué hemisferio queda apuntando al Sol en cada parte del año."
  }
];
GAMES.cielo_4 = juegoTriviaTexto(CUR_CIELO_4_BANCO, "Mirá el cielo y pensá.", "cielo_4");

/* 4° · ¿Qué clase de palabra? — clases_palabra_4
   DC: Sustantivos propios y comunes; adjetivos calificativos y gentilicios
   Fuente: docs/auditoria-dc-caba/grado-4.md · L4 */
const CUR_CLASES_PALABRA_4_BANCO = [
  {
    "it": "perro",
    "cat": "comun",
    "m": "Nombra a cualquier perro, no a uno solo."
  },
  {
    "it": "Rosario",
    "cat": "propio",
    "m": "Es el nombre de UNA ciudad en particular: va con mayúscula."
  },
  {
    "it": "veloz",
    "cat": "adjetivo",
    "m": "Dice CÓMO es algo."
  },
  {
    "it": "alegría",
    "cat": "comun",
    "m": "Trampa clásica: aunque nombre un sentimiento y no algo que se toca, sigue siendo un sustantivo."
  },
  {
    "it": "cordobés",
    "cat": "adjetivo",
    "m": "Gentilicio: dice de dónde es alguien, así que califica. Va con minúscula, a diferencia de Córdoba."
  },
  {
    "it": "Paraná",
    "cat": "propio",
    "m": "Nombre de un río en particular."
  },
  {
    "it": "mesa",
    "cat": "comun",
    "m": "Nombra a cualquier mesa."
  },
  {
    "it": "oscuro",
    "cat": "adjetivo",
    "m": "Dice cómo es."
  },
  {
    "it": "Malena",
    "cat": "propio",
    "m": "Nombre de una persona."
  },
  {
    "it": "valentía",
    "cat": "comun",
    "m": "Sustantivo abstracto: no se toca, pero nombra."
  },
  {
    "it": "argentino",
    "cat": "adjetivo",
    "m": "Gentilicio, con minúscula. Distinto de Argentina, que es el país."
  },
  {
    "it": "ciudad",
    "cat": "comun",
    "m": "Nombra cualquier ciudad."
  },
  {
    "it": "enorme",
    "cat": "adjetivo",
    "m": "Dice el tamaño: califica."
  },
  {
    "it": "Belgrano",
    "cat": "propio",
    "m": "Apellido de una persona."
  },
  {
    "it": "tristeza",
    "cat": "comun",
    "m": "Nombra un sentimiento: sustantivo."
  },
  {
    "it": "amarillo",
    "cat": "adjetivo",
    "m": "Dice el color: califica."
  },
  {
    "it": "escuela",
    "cat": "comun",
    "m": "Nombra cualquier escuela."
  },
  {
    "it": "Aconcagua",
    "cat": "propio",
    "m": "El nombre de UN cerro."
  },
  {
    "it": "salteño",
    "cat": "adjetivo",
    "m": "Gentilicio: de Salta."
  },
  {
    "it": "libertad",
    "cat": "comun",
    "m": "Abstracto pero sustantivo: nombra una idea."
  }
];
GAMES.clases_palabra_4 = juegoClasificar(CUR_CLASES_PALABRA_4_BANCO, "¿Qué clase de palabra es?", [{"cat": "comun", "label": "📦 Sustantivo común"}, {"cat": "propio", "label": "🅰️ Sustantivo propio"}, {"cat": "adjetivo", "label": "🎨 Adjetivo"}], "clases_pal");

/* 4° · Máquina del tiempo verbal — tiempos_verbales_4
   DC: Presente, pretérito perfecto simple e imperfecto; narrar en pasado
   Fuente: docs/auditoria-dc-caba/grado-4.md · L5 */
const CUR_TIEMPOS_VERBALES_4_BANCO = [
  {
    "q": "Todos los veranos ___ a la casa de la abuela.",
    "ops": [
      "íbamos",
      "fuimos",
      "vamos"
    ],
    "m": "'Todos los veranos' marca algo repetido en el pasado: va el imperfecto (íbamos)."
  },
  {
    "q": "Ese día ___ a la casa de la abuela y comimos torta.",
    "ops": [
      "fuimos",
      "íbamos",
      "vamos"
    ],
    "m": "'Ese día' marca una vez sola y terminada: perfecto simple (fuimos)."
  },
  {
    "q": "Mientras ___ , sonó el timbre.",
    "ops": [
      "dormía",
      "dormí",
      "duermo"
    ],
    "m": "Lo que estaba pasando de fondo va en imperfecto; lo que interrumpe, en perfecto simple."
  },
  {
    "q": "Mientras dormía, ___ el timbre.",
    "ops": [
      "sonó",
      "sonaba",
      "suena"
    ],
    "m": "El hecho puntual que corta la escena va en perfecto simple."
  },
  {
    "q": "La casa ___ vieja y ___ un jardín enorme.",
    "ops": [
      "era / tenía",
      "fue / tuvo",
      "es / tiene"
    ],
    "m": "Para DESCRIBIR cómo eran las cosas en el relato se usa el imperfecto."
  },
  {
    "q": "De repente, la puerta ___ .",
    "ops": [
      "se abrió",
      "se abría",
      "se abre"
    ],
    "m": "'De repente' pide un hecho puntual: perfecto simple."
  },
  {
    "q": "Cuando era chico, ___ al fútbol todos los sábados.",
    "ops": [
      "jugaba",
      "jugué",
      "juego"
    ],
    "m": "Costumbre del pasado: imperfecto."
  },
  {
    "q": "El sábado pasado ___ dos goles.",
    "ops": [
      "hice",
      "hacía",
      "hago"
    ],
    "m": "Un sábado concreto y terminado: perfecto simple."
  },
  {
    "q": "¿Cuál de estas frases está en presente?",
    "ops": [
      "Corro hasta la esquina",
      "Corrí hasta la esquina",
      "Corría hasta la esquina"
    ],
    "m": "El presente cuenta lo que pasa ahora."
  },
  {
    "q": "Para contar un cuento que ya pasó, ¿qué conviene?",
    "ops": [
      "Mantener el pasado sin saltar al presente",
      "Ir cambiando de presente a pasado",
      "Usar siempre el presente"
    ],
    "m": "El DC lo pide así: narrar en pasado sin fluctuaciones que confundan al lector."
  },
  {
    "q": "Ayer ___ la tarea y después ___ un rato.",
    "ops": [
      "terminé / jugué",
      "terminaba / jugaba",
      "termino / juego"
    ],
    "m": "Dos hechos puntuales y terminados, uno detrás del otro: perfecto simple."
  },
  {
    "q": "Antes la plaza ___ una calesita.",
    "ops": [
      "tenía",
      "tuvo",
      "tiene"
    ],
    "m": "'Antes' describe cómo era la plaza en ese tiempo: imperfecto."
  },
  {
    "q": "El lobo ___ y ___ la puerta de un soplido.",
    "ops": [
      "llegó / tiró",
      "llegaba / tiraba",
      "llega / tira"
    ],
    "m": "La acción que hace avanzar el cuento va en perfecto simple."
  },
  {
    "q": "Llovía y hacía frío. ¿Para qué sirven esos verbos en el relato?",
    "ops": [
      "Para describir la escena",
      "Para contar qué pasó",
      "Para terminar el cuento"
    ],
    "m": "El imperfecto pinta el decorado; el perfecto simple mueve la acción."
  },
  {
    "q": "¿Cuál es pretérito perfecto simple?",
    "ops": [
      "cantó",
      "cantaba",
      "canta"
    ],
    "m": "'Cantó' es una acción terminada en un momento concreto."
  },
  {
    "q": "Todos los días el sol ___ por el este.",
    "ops": [
      "sale",
      "salió",
      "salía"
    ],
    "m": "Algo que pasa siempre se cuenta en presente."
  }
];
GAMES.tiempos_verbales_4 = juegoTriviaTexto(CUR_TIEMPOS_VERBALES_4_BANCO, "¿Qué verbo completa bien la historia?", "tiempos_ve");

/* 4° · La palabra que abarca — hiperonimos_4
   DC: Cohesión léxica: hiperónimos, hipónimos y sinonimia
   Fuente: docs/auditoria-dc-caba/grado-4.md · L7 */
const CUR_HIPERONIMOS_4_BANCO = [
  {
    "q": "¿Qué palabra incluye a 'rosa', 'clavel' y 'jazmín'?",
    "ops": [
      "flor",
      "planta",
      "perfume"
    ],
    "m": "'Planta' también las incluye, pero 'flor' es la más precisa: son todas flores."
  },
  {
    "q": "¿Qué palabra incluye a 'hornero', 'cóndor' y 'gorrión'?",
    "ops": [
      "ave",
      "animal",
      "pluma"
    ],
    "m": "'Animal' es verdadero, pero menos preciso: todos son AVES."
  },
  {
    "q": "¿Cuál es un tipo de 'herramienta'?",
    "ops": [
      "martillo",
      "taller",
      "arreglar"
    ],
    "m": "El martillo es una clase de herramienta: es su hipónimo."
  },
  {
    "q": "¿Qué palabra incluye a 'guitarra', 'piano' y 'violín'?",
    "ops": [
      "instrumento musical",
      "música",
      "concierto"
    ],
    "m": "Son todos instrumentos; 'música' es lo que producen, no lo que son."
  },
  {
    "q": "En un texto sobre el hornero, ¿con qué palabra podés reemplazarlo para no repetir?",
    "ops": [
      "el ave",
      "la casa",
      "el barro"
    ],
    "m": "Usar el hiperónimo evita repetir y mantiene el texto unido: eso es cohesión léxica."
  },
  {
    "q": "¿Cuál es sinónimo de 'veloz'?",
    "ops": [
      "rápido",
      "lento",
      "fuerte"
    ],
    "m": "Sinónimos: dos palabras distintas con el mismo significado."
  },
  {
    "q": "¿Cuál es sinónimo de 'contento'?",
    "ops": [
      "alegre",
      "cansado",
      "enojado"
    ],
    "m": "Alegre y contento significan lo mismo."
  },
  {
    "q": "¿Qué palabra incluye a 'remera', 'pantalón' y 'campera'?",
    "ops": [
      "ropa",
      "tela",
      "placard"
    ],
    "m": "Son prendas de ropa. 'Tela' es de qué están hechas."
  },
  {
    "q": "¿Cuál es un tipo de 'vehículo'?",
    "ops": [
      "colectivo",
      "calle",
      "viajar"
    ],
    "m": "El colectivo es una clase de vehículo."
  },
  {
    "q": "¿Qué palabra incluye a 'manzana', 'pera' y 'durazno'?",
    "ops": [
      "fruta",
      "comida",
      "árbol"
    ],
    "m": "'Comida' es cierto pero muy general: la palabra justa es 'fruta'."
  },
  {
    "q": "¿Cuál es sinónimo de 'empezar'?",
    "ops": [
      "comenzar",
      "terminar",
      "seguir"
    ],
    "m": "Empezar y comenzar son sinónimos."
  },
  {
    "q": "¿Cuál NO es un tipo de 'mueble'?",
    "ops": [
      "ventana",
      "silla",
      "mesa"
    ],
    "m": "La ventana es parte de la casa, no un mueble."
  },
  {
    "q": "¿Qué palabra incluye a 'triángulo', 'cuadrado' y 'círculo'?",
    "ops": [
      "figura",
      "dibujo",
      "regla"
    ],
    "m": "Son figuras geométricas."
  },
  {
    "q": "¿Cuál es sinónimo de 'enorme'?",
    "ops": [
      "gigante",
      "chiquito",
      "angosto"
    ],
    "m": "Gigante y enorme dicen lo mismo."
  },
  {
    "q": "¿Cuál NO es un tipo de 'ave'?",
    "ops": [
      "murciélago",
      "pingüino",
      "avestruz"
    ],
    "m": "El murciélago vuela pero es un mamífero. El pingüino no vuela y sí es un ave."
  },
  {
    "q": "¿Qué palabra incluye a 'lápiz', 'goma' y 'regla'?",
    "ops": [
      "útiles escolares",
      "mochila",
      "escuela"
    ],
    "m": "La mochila los guarda; no son tipos de mochila."
  },
  {
    "q": "¿Cuál es sinónimo de 'hermoso'?",
    "ops": [
      "bello",
      "feo",
      "nuevo"
    ],
    "m": "Bello y hermoso significan lo mismo."
  },
  {
    "q": "¿Qué palabra incluye a 'lluvia', 'granizo' y 'nieve'?",
    "ops": [
      "precipitación",
      "agua",
      "invierno"
    ],
    "m": "Las tres son formas en que cae el agua del cielo: precipitaciones."
  },
  {
    "q": "En 'Compré una mascota. El perro es negro', ¿qué relación hay?",
    "ops": [
      "'Perro' es un tipo de 'mascota'",
      "Son sinónimos",
      "No tienen relación"
    ],
    "m": "Se pasa del hiperónimo (mascota) al hipónimo (perro): así se encadena un texto."
  },
  {
    "q": "¿Cuál es sinónimo de 'silencioso'?",
    "ops": [
      "callado",
      "ruidoso",
      "brillante"
    ],
    "m": "Callado y silencioso significan lo mismo."
  }
];
GAMES.hiperonimos_4 = juegoTriviaTexto(CUR_HIPERONIMOS_4_BANCO, "Pensá qué palabra incluye a la otra.", "hiperonimo");

/* 4° · ¿Ola u hola? — homofonos_4
   DC: Homófonos heterógrafos
   Fuente: docs/auditoria-dc-caba/grado-4.md · L8 */
const CUR_HOMOFONOS_4_BANCO = [
  {
    "q": "___ , ¿cómo andás?",
    "ops": [
      "Hola",
      "Ola",
      "Olla"
    ],
    "m": "El saludo lleva H: hola. La 'ola' es la del mar."
  },
  {
    "q": "Nos tapó una ___ enorme en la playa.",
    "ops": [
      "ola",
      "hola",
      "holla"
    ],
    "m": "La del mar es 'ola', sin H."
  },
  {
    "q": "Puso los fideos en la ___ .",
    "ops": [
      "olla",
      "hoya",
      "ola"
    ],
    "m": "La de cocinar es 'olla', con doble L."
  },
  {
    "q": "Ayer ___ mucha gente en la plaza.",
    "ops": [
      "hubo",
      "uvo",
      "huvo"
    ],
    "m": "Del verbo haber: 'hubo', con H y con B."
  },
  {
    "q": "Se comió un racimo de ___ .",
    "ops": [
      "uvas",
      "hubas",
      "huvas"
    ],
    "m": "La fruta va sin H: uvas."
  },
  {
    "q": "El agua pasa por ese ___ de plástico.",
    "ops": [
      "tubo",
      "tuvo",
      "thubo"
    ],
    "m": "El caño es 'tubo', con B."
  },
  {
    "q": "Ella ___ que irse temprano.",
    "ops": [
      "tuvo",
      "tubo",
      "thuvo"
    ],
    "m": "Del verbo tener: 'tuvo', con V."
  },
  {
    "q": "Fuimos a ___ la película.",
    "ops": [
      "ver",
      "haber",
      "a ver"
    ],
    "m": "'Ver' es mirar. 'Haber' es el verbo auxiliar."
  },
  {
    "q": "Tiene que ___ una explicación.",
    "ops": [
      "haber",
      "a ver",
      "ver"
    ],
    "m": "Acá el verbo es haber: tiene que haber."
  },
  {
    "q": "Le dieron un premio por su ___ .",
    "ops": [
      "valor",
      "balor",
      "vallor"
    ],
    "m": "Valor va con V."
  },
  {
    "q": "Se ___ el pelo todas las mañanas.",
    "ops": [
      "ata",
      "hata",
      "atta"
    ],
    "m": "Del verbo atar, sin H."
  },
  {
    "q": "El pájaro tiene un ___ largo.",
    "ops": [
      "pico",
      "picco",
      "phico"
    ],
    "m": "Pico se escribe con C."
  },
  {
    "q": "Vamos a ___ la mesa para comer.",
    "ops": [
      "poner",
      "ponner",
      "pooner"
    ],
    "m": "Una sola N."
  },
  {
    "q": "El equipo ___ el partido.",
    "ops": [
      "ganó",
      "gano",
      "gannó"
    ],
    "m": "'Ganó' con tilde es pasado; 'gano' sin tilde es presente."
  },
  {
    "q": "Yo ___ todos los domingos.",
    "ops": [
      "gano",
      "ganó",
      "gané"
    ],
    "m": "Sin tilde y en presente: yo gano."
  },
  {
    "q": "Se cayó y se hizo un ___ en la rodilla.",
    "ops": [
      "raspón",
      "rraspón",
      "rasspón"
    ],
    "m": "Una sola R al principio, aunque suene fuerte."
  },
  {
    "q": "El pan estaba muy ___ .",
    "ops": [
      "rico",
      "rrico",
      "hrico"
    ],
    "m": "La R al principio de palabra ya suena fuerte: no se duplica."
  },
  {
    "q": "Le regaló un ramo de flores ___ .",
    "ops": [
      "bellas",
      "vellas",
      "veyas"
    ],
    "m": "'Bellas' es hermosas, con B. 'Vellas' no existe con ese sentido."
  },
  {
    "q": "Se fue ___ la esquina.",
    "ops": [
      "hasta",
      "asta",
      "hastta"
    ],
    "m": "'Hasta' con H es el límite; el 'asta' sin H es el palo de la bandera."
  },
  {
    "q": "Izaron la bandera en el ___ .",
    "ops": [
      "asta",
      "hasta",
      "azta"
    ],
    "m": "El palo de la bandera es 'asta', sin H."
  }
];
GAMES.homofonos_4 = juegoTriviaTexto(CUR_HOMOFONOS_4_BANCO, "Suenan igual pero se escriben distinto. ¿Cuál va?", "homofonos_");

/* 4° · Completá lo que falta — grupos_ortograficos_4
   DC: Regularidades ortográficas: hue-, bue-, bur-, bus-, -aje, -bilidad
   Fuente: docs/auditoria-dc-caba/grado-4.md · L9 */
const CUR_GRUPOS_ORTOGRAFICOS_4_BANCO = [
  {
    "q": "___ vo (el del gallinero)",
    "ops": [
      "hue",
      "ue",
      "bue"
    ],
    "m": "Las palabras que empiezan con el sonido 'ue' llevan H adelante: huevo."
  },
  {
    "q": "___ so (del esqueleto)",
    "ops": [
      "hue",
      "ue",
      "gue"
    ],
    "m": "Hueso, con H."
  },
  {
    "q": "___ lla (la marca del pie)",
    "ops": [
      "hue",
      "ue",
      "bue"
    ],
    "m": "Huella, con H."
  },
  {
    "q": "___ rta (donde se plantan verduras)",
    "ops": [
      "hue",
      "ue",
      "bur"
    ],
    "m": "Huerta, con H."
  },
  {
    "q": "___ no (lo contrario de malo)",
    "ops": [
      "bue",
      "vue",
      "hue"
    ],
    "m": "Bueno va con B."
  },
  {
    "q": "___ y (el animal que ara el campo)",
    "ops": [
      "bue",
      "vue",
      "hue"
    ],
    "m": "Buey, con B."
  },
  {
    "q": "___ rro (el animal de carga)",
    "ops": [
      "bu",
      "vu",
      "hu"
    ],
    "m": "Burro va con B, como casi todas las que empiezan con bur-."
  },
  {
    "q": "___ buja (la de jabón)",
    "ops": [
      "bur",
      "vur",
      "hur"
    ],
    "m": "Burbuja, con B."
  },
  {
    "q": "___ car (lo que hacés cuando perdés algo)",
    "ops": [
      "bus",
      "vus",
      "hus"
    ],
    "m": "Buscar va con B, como bus-."
  },
  {
    "q": "___ to (la escultura de la cabeza)",
    "ops": [
      "bus",
      "vus",
      "hus"
    ],
    "m": "Busto, con B."
  },
  {
    "q": "gar___ (el lugar donde entra el auto)",
    "ops": [
      "aje",
      "age",
      "aches"
    ],
    "m": "Las palabras terminadas en el sonido 'aje' van con J: garaje."
  },
  {
    "q": "vi___ (lo que hacés cuando salís de viaje)",
    "ops": [
      "aje",
      "age",
      "aye"
    ],
    "m": "Viaje, con J."
  },
  {
    "q": "person___ (el del cuento)",
    "ops": [
      "aje",
      "age",
      "aye"
    ],
    "m": "Personaje, con J."
  },
  {
    "q": "equip___ (las valijas del viaje)",
    "ops": [
      "aje",
      "age",
      "aches"
    ],
    "m": "Equipaje, con J."
  },
  {
    "q": "mens___ (lo que mandás por el celular)",
    "ops": [
      "aje",
      "age",
      "aye"
    ],
    "m": "Mensaje, con J."
  },
  {
    "q": "posi___ (cuando algo se puede hacer)",
    "ops": [
      "bilidad",
      "vilidad",
      "billidad"
    ],
    "m": "Las palabras terminadas en -bilidad van con B: posibilidad."
  },
  {
    "q": "amá___ (cuando alguien es agradable)",
    "ops": [
      "bilidad",
      "vilidad",
      "billidad"
    ],
    "m": "Amabilidad, con B."
  },
  {
    "q": "responsa___ (hacerse cargo)",
    "ops": [
      "bilidad",
      "vilidad",
      "billidad"
    ],
    "m": "Responsabilidad, con B."
  },
  {
    "q": "¿Cuál es la excepción de -bilidad, que va con V?",
    "ops": [
      "movilidad",
      "posibilidad",
      "amabilidad"
    ],
    "m": "Movilidad y civilidad son las excepciones: vienen de móvil y civil."
  },
  {
    "q": "___ lga (cuando los trabajadores paran)",
    "ops": [
      "hue",
      "ue",
      "bue"
    ],
    "m": "Huelga, con H."
  },
  {
    "q": "___ sped (el que viene de visita)",
    "ops": [
      "hué",
      "ué",
      "bué"
    ],
    "m": "Huésped, con H."
  },
  {
    "q": "sal___ (lo que hacés al despedirte)",
    "ops": [
      "udo",
      "hudo",
      "uddo"
    ],
    "m": "Saludo no lleva H: la regla del 'hue' vale sólo cuando ESE sonido arranca la palabra."
  }
];
GAMES.grupos_ortograficos_4 = juegoTriviaTexto(CUR_GRUPOS_ORTOGRAFICOS_4_BANCO, "¿Con qué se completa la palabra?", "grupos_ort");

/* 4° · ¿Mito, leyenda o los dos? — mito_leyenda_4
   DC: Mitos y leyendas: estructura, semejanzas y diferencias
   Fuente: docs/auditoria-dc-caba/grado-4.md · L11 */
const CUR_MITO_LEYENDA_4_BANCO = [
  {
    "it": "Explica cómo se creó el mundo",
    "cat": "mito",
    "m": "El mito explica los orígenes: el mundo, los dioses, el ser humano."
  },
  {
    "it": "Cuenta por qué el ceibo tiene flores rojas",
    "cat": "leyenda",
    "m": "La leyenda explica algo concreto y cercano: una planta, un cerro, un río."
  },
  {
    "it": "Los personajes son dioses",
    "cat": "mito",
    "m": "En el mito actúan dioses y fuerzas de la naturaleza."
  },
  {
    "it": "Ocurre en un lugar que se puede señalar en el mapa",
    "cat": "leyenda",
    "m": "La leyenda se ancla a un lugar real; el mito pasa en un tiempo anterior al mundo tal como lo conocemos."
  },
  {
    "it": "Se transmitió de boca en boca durante generaciones",
    "cat": "ambos",
    "m": "Los dos son relatos de tradición oral: nadie los escribió primero."
  },
  {
    "it": "Pasa en un tiempo anterior al mundo actual",
    "cat": "mito",
    "m": "El mito ocurre 'antes de que todo fuera como es'."
  },
  {
    "it": "Un personaje se transforma en planta o en animal",
    "cat": "ambos",
    "m": "La transformación aparece en los dos: en el mito explica el origen del mundo, en la leyenda explica algo puntual del paisaje."
  },
  {
    "it": "La historia de la yerba mate y la luna",
    "cat": "leyenda",
    "m": "Explica el origen de una planta concreta del Litoral."
  },
  {
    "it": "Explica de dónde vino el fuego para los seres humanos",
    "cat": "mito",
    "m": "Es un relato de origen: por qué existe algo fundamental."
  },
  {
    "it": "La gente del lugar lo cuenta como si hubiera pasado de verdad",
    "cat": "ambos",
    "m": "Los dos se cuentan como verdaderos dentro de la comunidad."
  },
  {
    "it": "Tiene un héroe que fundó un pueblo entero",
    "cat": "mito",
    "m": "Los mitos fundacionales explican el origen de un pueblo."
  },
  {
    "it": "Cuenta por qué el Iguazú tiene esa garganta",
    "cat": "leyenda",
    "m": "Explica un accidente geográfico que existe y se puede visitar."
  },
  {
    "it": "Aparecen personajes con poderes que las personas no tienen",
    "cat": "ambos",
    "m": "Lo sobrenatural está en los dos: dioses en el mito, seres mágicos en la leyenda."
  },
  {
    "it": "Explica por qué hay día y noche",
    "cat": "mito",
    "m": "Un fenómeno del universo entero: eso es materia de mito."
  },
  {
    "it": "El Pombero cuida los montes de noche",
    "cat": "leyenda",
    "m": "Personaje de una región concreta: es leyenda."
  },
  {
    "it": "Explica el origen del maíz para todo un pueblo",
    "cat": "mito",
    "m": "El origen de lo que sostiene a un pueblo entero es un relato mítico."
  },
  {
    "it": "La historia del cardenal y su copete rojo",
    "cat": "leyenda",
    "m": "Explica el rasgo de un pájaro concreto."
  },
  {
    "it": "Empieza contando cómo eran las cosas antes",
    "cat": "ambos",
    "m": "Los dos arrancan con una situación inicial que después cambia."
  },
  {
    "it": "Cuenta cómo los dioses castigaron a los seres humanos",
    "cat": "mito",
    "m": "Dioses que intervienen en el destino de la humanidad: mito."
  },
  {
    "it": "Explica por qué el ombú no sirve para hacer leña",
    "cat": "leyenda",
    "m": "Un detalle concreto de un árbol de la Pampa."
  }
];
GAMES.mito_leyenda_4 = juegoClasificar(CUR_MITO_LEYENDA_4_BANCO, "¿De qué tipo de relato es este rasgo?", [{"cat": "mito", "label": "⚡ Mito"}, {"cat": "leyenda", "label": "🌿 Leyenda"}, {"cat": "ambos", "label": "🤝 Los dos"}], "mito_leyen");

/* 4° · Detective del paratexto — paratexto_4
   DC: Índice, glosario, títulos y epígrafes; su relación con el contenido
   Fuente: docs/auditoria-dc-caba/grado-4.md · L12 */
const CUR_PARATEXTO_4_BANCO = [
  {
    "q": "Querés saber en qué página está el capítulo de los volcanes. ¿Dónde mirás?",
    "ops": [
      "El índice",
      "El glosario",
      "La contratapa"
    ],
    "m": "El índice dice qué hay y en qué página."
  },
  {
    "q": "No entendés la palabra 'sedimento'. ¿Dónde la buscás?",
    "ops": [
      "El glosario",
      "El índice",
      "El título"
    ],
    "m": "El glosario explica las palabras difíciles del libro."
  },
  {
    "q": "¿Para qué sirve el epígrafe de una foto?",
    "ops": [
      "Explica qué se ve en la foto",
      "Dice el precio del libro",
      "Numera la página"
    ],
    "m": "El epígrafe es el textito al pie de la imagen: dice qué estás mirando."
  },
  {
    "q": "¿Qué te adelanta el título de un capítulo?",
    "ops": [
      "De qué va a tratar",
      "Cuántas páginas tiene",
      "Quién lo imprimió"
    ],
    "m": "El título anticipa el tema: leerlo antes ayuda a entender mejor."
  },
  {
    "q": "Querés saber de qué trata el libro antes de comprarlo. ¿Qué mirás?",
    "ops": [
      "La contratapa",
      "El glosario",
      "El número de página"
    ],
    "m": "La contratapa resume el libro para el que todavía no lo leyó."
  },
  {
    "q": "¿Dónde está el nombre del autor?",
    "ops": [
      "En la tapa",
      "En el glosario",
      "En el índice"
    ],
    "m": "La tapa lleva título y autor."
  },
  {
    "q": "En un libro de Naturales, ¿qué es un subtítulo?",
    "ops": [
      "Un título más chico que divide el capítulo en partes",
      "El nombre del autor",
      "Una palabra difícil"
    ],
    "m": "Los subtítulos organizan el capítulo por dentro."
  },
  {
    "q": "¿Cómo está ordenado el glosario, casi siempre?",
    "ops": [
      "Alfabéticamente",
      "Por página",
      "Por tamaño de palabra"
    ],
    "m": "Como un diccionario: por eso se encuentra rápido."
  },
  {
    "q": "¿El índice va siempre al final del libro?",
    "ops": [
      "Puede ir al principio o al final",
      "Siempre al final",
      "Siempre al principio"
    ],
    "m": "Depende del libro: conviene fijarse en los dos lugares."
  },
  {
    "q": "Ves un recuadro de color al costado del texto. ¿Qué suele traer?",
    "ops": [
      "Un dato extra sobre el tema",
      "El índice",
      "El nombre de la imprenta"
    ],
    "m": "Los recuadros suman información aparte del texto principal."
  },
  {
    "q": "¿Qué información te da el número de página?",
    "ops": [
      "Dónde estás dentro del libro",
      "De qué trata la página",
      "Quién la escribió"
    ],
    "m": "Es lo que hace que el índice sirva."
  },
  {
    "q": "Antes de leer un capítulo, ¿qué conviene mirar primero?",
    "ops": [
      "Título, subtítulos e imágenes",
      "Sólo la última página",
      "Nada, leer directo"
    ],
    "m": "Explorar el paratexto antes de leer ayuda a entender mucho más."
  },
  {
    "q": "Un mapa con una referencia de colores al costado. ¿Cómo se llama esa referencia?",
    "ops": [
      "Las referencias o la leyenda del mapa",
      "El glosario",
      "El epígrafe"
    ],
    "m": "Las referencias explican qué significa cada color o símbolo."
  },
  {
    "q": "Buscás quién publicó el libro y en qué año. ¿Dónde está?",
    "ops": [
      "En las primeras páginas, con los datos de edición",
      "En el glosario",
      "En el epígrafe"
    ],
    "m": "Esos datos permiten saber si la información está actualizada."
  }
];
GAMES.paratexto_4 = juegoTriviaTexto(CUR_PARATEXTO_4_BANCO, "¿Dónde lo buscás en el libro?", "paratexto_");

/* 4° · ¿Para qué se escribió? — proposito_texto_4
   DC: Propósito comunicativo: informar, narrar, describir, indicar, argumentar
   Fuente: docs/auditoria-dc-caba/grado-4.md · L13 */
const CUR_PROPOSITO_TEXTO_4_BANCO = [
  {
    "q": "«Mezclá la harina con el agua. Amasá 10 minutos. Dejá descansar.»",
    "ops": [
      "Indicar cómo hacer algo",
      "Contar una historia",
      "Convencer"
    ],
    "m": "Verbos que mandan y pasos numerados: es un instructivo."
  },
  {
    "q": "«El hornero construye su nido con barro y pasto seco.»",
    "ops": [
      "Informar",
      "Convencer",
      "Contar una historia"
    ],
    "m": "Da un dato de la realidad, sin opinión ni personajes."
  },
  {
    "q": "«Era alto, flaco, de barba blanca y ojos muy chiquitos.»",
    "ops": [
      "Describir",
      "Indicar cómo hacer algo",
      "Convencer"
    ],
    "m": "Dice cómo es alguien: descripción."
  },
  {
    "q": "«Esa mañana Julián se despertó tarde y salió corriendo.»",
    "ops": [
      "Contar una historia",
      "Informar",
      "Convencer"
    ],
    "m": "Hay un personaje y hechos que se suceden: es una narración."
  },
  {
    "q": "«Hay que cuidar el agua: sin ella no hay vida posible.»",
    "ops": [
      "Convencer",
      "Informar",
      "Describir"
    ],
    "m": "Defiende una postura y da razones: es argumentativo."
  },
  {
    "q": "«Apretá el botón rojo y esperá tres segundos.»",
    "ops": [
      "Indicar cómo hacer algo",
      "Describir",
      "Informar"
    ],
    "m": "Instrucción: dice qué hacer paso a paso."
  },
  {
    "q": "«La Argentina tiene 24 jurisdicciones.»",
    "ops": [
      "Informar",
      "Convencer",
      "Contar una historia"
    ],
    "m": "Es un dato verificable, sin opinión."
  },
  {
    "q": "«El aula era grande, con ventanales que daban al patio.»",
    "ops": [
      "Describir",
      "Contar una historia",
      "Indicar"
    ],
    "m": "Pinta cómo es un lugar."
  },
  {
    "q": "«Creemos que la escuela debería tener más horas de música.»",
    "ops": [
      "Convencer",
      "Informar",
      "Describir"
    ],
    "m": "Es una opinión que busca que estés de acuerdo."
  },
  {
    "q": "«Primero cortá el papel. Después pegalo en el cartón.»",
    "ops": [
      "Indicar cómo hacer algo",
      "Contar una historia",
      "Informar"
    ],
    "m": "Pasos en orden: instructivo."
  },
  {
    "q": "«Ayer se inauguró la plaza nueva del barrio.»",
    "ops": [
      "Informar",
      "Convencer",
      "Indicar"
    ],
    "m": "Comunica un hecho ocurrido, sin personajes ni opinión: es una noticia."
  },
  {
    "q": "«Cuando llegó a la plaza, Lucía encontró a su perro esperándola.»",
    "ops": [
      "Contar una historia",
      "Informar",
      "Describir"
    ],
    "m": "Hay personaje y sucesos encadenados: narración."
  },
  {
    "q": "«El ombú no es un árbol: es una hierba gigante.»",
    "ops": [
      "Informar",
      "Convencer",
      "Contar una historia"
    ],
    "m": "Aporta un dato, aunque sorprenda."
  },
  {
    "q": "«Los chicos necesitan más recreo y acá te explico por qué.»",
    "ops": [
      "Convencer",
      "Informar",
      "Describir"
    ],
    "m": "Anuncia que va a dar razones para sostener una postura."
  },
  {
    "q": "«Tenía el pelo colorado y una campera azul enorme.»",
    "ops": [
      "Describir",
      "Contar una historia",
      "Convencer"
    ],
    "m": "Sólo dice cómo es: no pasa nada todavía."
  },
  {
    "q": "Un cartel que dice «No pisar el césped». ¿Para qué está?",
    "ops": [
      "Indicar qué hacer",
      "Contar una historia",
      "Describir el césped"
    ],
    "m": "Da una instrucción."
  },
  {
    "q": "«La ballena franca austral visita la Península Valdés cada año.»",
    "ops": [
      "Informar",
      "Convencer",
      "Indicar"
    ],
    "m": "Dato de la realidad."
  },
  {
    "q": "«Es el mejor libro que leí en mi vida, tenés que leerlo.»",
    "ops": [
      "Convencer",
      "Informar",
      "Describir"
    ],
    "m": "Opinión + recomendación: busca que hagas algo."
  }
];
GAMES.proposito_texto_4 = juegoTriviaTexto(CUR_PROPOSITO_TEXTO_4_BANCO, "¿Para qué escribieron este texto?", "proposito_");

/* 4° · ¡Boom! La historieta — historieta_4
   DC: La historieta: onomatopeyas y aspectos gráficos
   Fuente: docs/auditoria-dc-caba/grado-4.md · L16 */
const CUR_HISTORIETA_4_BANCO = [
  {
    "q": "Un vaso se cae al piso. ¿Qué onomatopeya va?",
    "ops": [
      "¡CRASH!",
      "¡SPLASH!",
      "¡ZZZZ!"
    ],
    "m": "Crash es la rotura. Splash es el agua y zzz es dormir."
  },
  {
    "q": "Alguien duerme profundamente. ¿Qué va?",
    "ops": [
      "ZZZZZ",
      "BOOM",
      "TOC TOC"
    ],
    "m": "Las zetas representan el ronquido."
  },
  {
    "q": "Golpean la puerta. ¿Qué va?",
    "ops": [
      "TOC TOC",
      "MUAC",
      "GLUP"
    ],
    "m": "Toc toc es el golpeteo de nudillos."
  },
  {
    "q": "El personaje se asusta y traga saliva. ¿Qué va?",
    "ops": [
      "GLUP",
      "PLAF",
      "RING"
    ],
    "m": "Glup marca el susto."
  },
  {
    "q": "¿Qué es un globo de diálogo?",
    "ops": [
      "El espacio donde va lo que dice el personaje",
      "El dibujo del fondo",
      "El título de la historieta"
    ],
    "m": "El globo contiene las palabras y su rabito señala quién habla."
  },
  {
    "q": "El globo tiene el borde de nubecitas. ¿Qué significa?",
    "ops": [
      "El personaje lo está pensando, no lo dice",
      "Está gritando",
      "Está durmiendo"
    ],
    "m": "Globo de nubecitas = pensamiento. Se ve, pero los otros personajes no lo escuchan."
  },
  {
    "q": "El globo tiene el borde en picos y la letra enorme. ¿Qué significa?",
    "ops": [
      "El personaje grita",
      "El personaje susurra",
      "El personaje piensa"
    ],
    "m": "Picos y letra grande son grito: la forma del globo también dice cosas."
  },
  {
    "q": "¿Cómo se llama cada cuadrito de la historieta?",
    "ops": [
      "Viñeta",
      "Globo",
      "Epígrafe"
    ],
    "m": "La viñeta es el cuadro; la historieta es la seguidilla de viñetas."
  },
  {
    "q": "Unas rayitas atrás de un personaje que corre. ¿Qué indican?",
    "ops": [
      "Que se está moviendo rápido",
      "Que hace frío",
      "Que está enojado"
    ],
    "m": "Se llaman líneas cinéticas: dibujan el movimiento."
  },
  {
    "q": "¿En qué orden se leen las viñetas?",
    "ops": [
      "De izquierda a derecha y de arriba abajo",
      "De derecha a izquierda",
      "En cualquier orden"
    ],
    "m": "Igual que el texto: si se leen desordenadas, la historia no se entiende."
  },
  {
    "q": "Una explosión en la historieta. ¿Qué va?",
    "ops": [
      "¡BOOM!",
      "¡GLUP!",
      "¡MUAC!"
    ],
    "m": "Boom es el estallido."
  },
  {
    "q": "Un beso. ¿Qué va?",
    "ops": [
      "MUAC",
      "CRASH",
      "TOC TOC"
    ],
    "m": "Muac es el sonido del beso."
  },
  {
    "q": "El personaje tiene una lamparita dibujada sobre la cabeza. ¿Qué quiere decir?",
    "ops": [
      "Se le ocurrió una idea",
      "Tiene calor",
      "Está triste"
    ],
    "m": "Es una convención gráfica: la lamparita es la idea."
  },
  {
    "q": "¿Para qué sirve el cartel rectangular arriba de la viñeta?",
    "ops": [
      "Lo cuenta el narrador, no un personaje",
      "Es un grito",
      "Es un pensamiento"
    ],
    "m": "El cartel es la voz del narrador: ubica el tiempo o el lugar."
  }
];
GAMES.historieta_4 = juegoTriviaTexto(CUR_HISTORIETA_4_BANCO, "¿Cómo se cuenta en una historieta?", "historieta");

/* 4° · América antes de 1492 — america_1492_4
   DC: Incas y aztecas; tributos y tecnologías; cultivos americanos
   Fuente: docs/auditoria-dc-caba/grado-4.md · S2 */
const CUR_AMERICA_1492_4_BANCO = [
  {
    "q": "¿Dónde vivían los incas?",
    "ops": [
      "En la cordillera de los Andes",
      "En la selva del Amazonas",
      "En el norte de México"
    ],
    "m": "El imperio inca iba por los Andes, desde Colombia hasta el norte argentino."
  },
  {
    "q": "¿Dónde vivían los aztecas?",
    "ops": [
      "En el centro de México",
      "En la Patagonia",
      "En Perú"
    ],
    "m": "Su capital, Tenochtitlán, estaba donde hoy está la Ciudad de México."
  },
  {
    "q": "¿Qué era el tributo?",
    "ops": [
      "Lo que los pueblos dominados tenían que entregar al imperio",
      "Una fiesta religiosa",
      "Un tipo de casa"
    ],
    "m": "Entregaban alimentos, tejidos o trabajo: así se sostenía el imperio."
  },
  {
    "q": "¿Para qué construían terrazas en la montaña los incas?",
    "ops": [
      "Para poder cultivar en la ladera empinada",
      "Para vivir arriba",
      "Para defenderse"
    ],
    "m": "Los andenes son escalones de tierra plana: sin ellos la lluvia se llevaría la tierra ladera abajo."
  },
  {
    "q": "¿Cuál de estos alimentos es originario de América?",
    "ops": [
      "La papa",
      "El trigo",
      "El arroz"
    ],
    "m": "Papa, maíz, tomate, cacao, poroto y zapallo son americanos. El trigo llegó de Europa."
  },
  {
    "q": "¿Y el chocolate?",
    "ops": [
      "Viene del cacao, que es americano",
      "Vino de Europa",
      "Vino de África"
    ],
    "m": "El cacao lo usaban los aztecas como bebida y hasta como moneda."
  },
  {
    "q": "¿Qué era el quipu?",
    "ops": [
      "Un sistema de cuerdas con nudos para llevar cuentas",
      "Un instrumento musical",
      "Un tipo de casa"
    ],
    "m": "Los incas registraban cantidades con nudos: era su forma de anotar."
  },
  {
    "q": "¿Cómo se comunicaban a lo largo del imperio inca?",
    "ops": [
      "Con chasquis que corrían por caminos de postas",
      "Con caballos",
      "Con barcos"
    ],
    "m": "Los chasquis se pasaban el mensaje corriendo. No había caballos en América antes de la llegada de los europeos."
  },
  {
    "q": "¿Había caballos en América antes de 1492?",
    "ops": [
      "No, los trajeron los europeos",
      "Sí, muchos",
      "Sí, pero eran salvajes"
    ],
    "m": "Ni caballos ni vacas ni ovejas: todos llegaron después."
  },
  {
    "q": "¿Qué animal usaban los incas para cargar cosas?",
    "ops": [
      "La llama",
      "El caballo",
      "El burro"
    ],
    "m": "La llama era su animal de carga; también daba lana."
  },
  {
    "q": "¿Los incas y los aztecas eran el mismo pueblo?",
    "ops": [
      "No, vivían lejos y eran distintos",
      "Sí, con dos nombres",
      "Sí, eran vecinos"
    ],
    "m": "Los separaban miles de kilómetros y no se conocían entre sí."
  },
  {
    "q": "¿Qué pueblos vivían en lo que hoy es la Argentina?",
    "ops": [
      "Diaguitas, guaraníes, tehuelches y muchos más",
      "Sólo los incas",
      "Ninguno"
    ],
    "m": "Había muchos pueblos distintos, con lenguas y modos de vida propios."
  },
  {
    "q": "Los aztecas hicieron chinampas en el lago. ¿Qué eran?",
    "ops": [
      "Islas artificiales para cultivar",
      "Barcos de guerra",
      "Templos flotantes"
    ],
    "m": "Ganaban tierra de cultivo sobre el agua: una solución de ingeniería."
  },
  {
    "q": "¿Qué construcciones levantaron estos pueblos?",
    "ops": [
      "Ciudades de piedra con templos y caminos",
      "Sólo casas de paja",
      "Nada permanente"
    ],
    "m": "Machu Picchu y Tenochtitlán muestran ciudades planificadas."
  },
  {
    "q": "¿Cómo trabajaban la tierra en el imperio inca?",
    "ops": [
      "Por turnos, y parte de la cosecha iba al Estado",
      "Cada uno para sí, sin entregar nada",
      "No cultivaban"
    ],
    "m": "El trabajo por turnos (la mita) era una obligación con el imperio."
  },
  {
    "q": "El maíz era central para estos pueblos. ¿Por qué?",
    "ops": [
      "Porque crecía bien y alimentaba a mucha gente",
      "Porque era decorativo",
      "Porque era muy caro"
    ],
    "m": "Un cultivo que rinde mucho permite que crezcan ciudades grandes."
  }
];
GAMES.america_1492_4 = juegoTriviaTexto(CUR_AMERICA_1492_4_BANCO, "¿Qué sabés de los pueblos de América?", "america_14");

/* 4° · La sociedad colonial — sociedad_colonial_4
   DC: Sectores de la sociedad colonial: derechos y obligaciones
   Fuente: docs/auditoria-dc-caba/grado-4.md · S4 */
const CUR_SOCIEDAD_COLONIAL_4_BANCO = [
  {
    "q": "¿Quiénes tenían más derechos en la sociedad colonial?",
    "ops": [
      "Los españoles venidos de España",
      "Los indígenas",
      "Los africanos esclavizados"
    ],
    "m": "Los peninsulares ocupaban los cargos más altos; los criollos, hijos de españoles nacidos acá, quedaban un escalón abajo."
  },
  {
    "q": "¿Quiénes eran los criollos?",
    "ops": [
      "Hijos de españoles nacidos en América",
      "Los que venían de España",
      "Los pueblos originarios"
    ],
    "m": "Eran ricos y educados, pero no podían acceder a los cargos más altos: ese enojo pesó en 1810."
  },
  {
    "q": "¿Qué era la encomienda?",
    "ops": [
      "Un grupo de indígenas obligados a trabajar para un español",
      "Un paquete que llegaba de España",
      "Una fiesta religiosa"
    ],
    "m": "El español recibía el trabajo y el tributo de esos indígenas a cambio de 'protegerlos' y evangelizarlos."
  },
  {
    "q": "Los indígenas bajo encomienda, ¿eran esclavos?",
    "ops": [
      "No: legalmente eran libres, pero estaban obligados a trabajar y pagar tributo",
      "Sí, exactamente lo mismo",
      "No, eran totalmente libres"
    ],
    "m": "Diferencia importante: la ley los declaraba libres y vasallos del rey, pero les imponía trabajo y tributo obligatorios."
  },
  {
    "q": "¿Cuál era la situación legal de las personas africanas esclavizadas?",
    "ops": [
      "Eran tratadas como propiedad y se las podía comprar y vender",
      "Eran trabajadoras con sueldo",
      "Eran dueñas de la tierra"
    ],
    "m": "La esclavitud era una condición legal distinta de la de los indígenas: se heredaba y la persona era considerada propiedad de otra."
  },
  {
    "q": "¿Qué trabajos hacían las personas esclavizadas en Buenos Aires?",
    "ops": [
      "Oficios en la ciudad y tareas domésticas",
      "Sólo trabajo en minas",
      "Ninguno"
    ],
    "m": "En Buenos Aires eran panaderos, changadores, lavanderas, artesanos: buena parte de la vida de la ciudad dependía de ese trabajo."
  },
  {
    "q": "¿Quién gobernaba el Virreinato en nombre del rey?",
    "ops": [
      "El virrey",
      "El cabildo",
      "El obispo"
    ],
    "m": "'Virrey' quiere decir justamente eso: el que está en lugar del rey."
  },
  {
    "q": "¿Qué era el Cabildo?",
    "ops": [
      "El gobierno de la ciudad",
      "La iglesia principal",
      "El puerto"
    ],
    "m": "Se ocupaba de lo cotidiano: precios, limpieza, seguridad."
  },
  {
    "q": "¿Podían las mujeres de la colonia estudiar en la universidad?",
    "ops": [
      "No, les estaba vedado",
      "Sí, todas",
      "Sí, sólo las criollas"
    ],
    "m": "El acceso al estudio y a los cargos estaba cerrado para las mujeres."
  },
  {
    "q": "¿Qué tenían que pagar los indígenas de encomienda?",
    "ops": [
      "Un tributo, en productos o en trabajo",
      "Nada",
      "Sólo impuestos a la iglesia"
    ],
    "m": "El tributo era la obligación central que pesaba sobre ellos."
  },
  {
    "q": "¿Todos los que vivían en la colonia tenían los mismos derechos?",
    "ops": [
      "No: los derechos dependían del grupo al que pertenecías",
      "Sí, eran todos iguales ante la ley",
      "Sí, salvo los niños"
    ],
    "m": "Era una sociedad de estamentos: el lugar de nacimiento y el origen definían qué podías hacer."
  },
  {
    "q": "¿Qué era la mita?",
    "ops": [
      "Un turno de trabajo obligatorio, sobre todo en las minas",
      "Una comida típica",
      "Un impuesto al comercio"
    ],
    "m": "Los pueblos andinos debían turnos de trabajo; en las minas de Potosí fue durísimo."
  },
  {
    "q": "¿De dónde salía la plata que enriqueció a España?",
    "ops": [
      "De las minas de Potosí",
      "De los ríos de la Pampa",
      "De Buenos Aires"
    ],
    "m": "Potosí, en el Alto Perú, fue la mina de plata más grande del mundo."
  },
  {
    "q": "¿Por qué Buenos Aires era importante para la corona?",
    "ops": [
      "Por su puerto: por ahí salía y entraba el comercio",
      "Por sus minas",
      "Por sus montañas"
    ],
    "m": "El puerto la volvió clave, sobre todo desde 1776 con el Virreinato del Río de la Plata."
  }
];
GAMES.sociedad_colonial_4 = juegoTriviaTexto(CUR_SOCIEDAD_COLONIAL_4_BANCO, "¿Cómo era la vida en la colonia?", "sociedad_c");

/* 4° · Ambientes argentinos — ambientes_4
   DC: Ambientes: montaña, llanura y meseta
   Fuente: docs/auditoria-dc-caba/grado-4.md · S5 */
const CUR_AMBIENTES_4_BANCO = [
  {
    "it": "Terreno muy alto, empinado y con picos nevados",
    "cat": "montana",
    "m": "Alto y con pendiente fuerte: montaña."
  },
  {
    "it": "Terreno bajo y plano hasta donde llega la vista",
    "cat": "llanura",
    "m": "Bajo y plano: llanura."
  },
  {
    "it": "Terreno alto pero plano arriba, cortado por barrancas",
    "cat": "meseta",
    "m": "Este es el que se confunde: es ALTO como la montaña pero PLANO arriba, como una mesa."
  },
  {
    "it": "La región donde se siembra trigo y soja en Buenos Aires",
    "cat": "llanura",
    "m": "La llanura pampeana: suelo plano y fértil."
  },
  {
    "it": "El Aconcagua y sus alrededores",
    "cat": "montana",
    "m": "El cerro más alto de América está en la cordillera."
  },
  {
    "it": "La Patagonia extraandina, con escalones de piedra y viento",
    "cat": "meseta",
    "m": "La meseta patagónica baja hacia el mar en escalones."
  },
  {
    "it": "Zona donde el agua de lluvia baja rápido y forma torrentes",
    "cat": "montana",
    "m": "La pendiente fuerte hace que el agua corra rápido."
  },
  {
    "it": "Campo llano donde el río serpentea despacio",
    "cat": "llanura",
    "m": "Sin pendiente el río se mueve lento y hace curvas."
  },
  {
    "it": "Superficie alta y pareja arriba, con bordes cortados a pique",
    "cat": "meseta",
    "m": "Arriba plano, bordes abruptos: meseta."
  },
  {
    "it": "Lugar donde se cría ganado ovino con mucho viento y poca lluvia",
    "cat": "meseta",
    "m": "La meseta patagónica: seca, ventosa, buena para la oveja."
  },
  {
    "it": "Terreno donde hay que hacer terrazas para poder cultivar",
    "cat": "montana",
    "m": "En la ladera empinada hay que aterrazar para que la tierra no se lave."
  },
  {
    "it": "Zona de esteros y campos anegados del Litoral",
    "cat": "llanura",
    "m": "Terreno bajo y plano donde el agua se queda."
  },
  {
    "it": "Región donde están las minas y los valles entre cerros",
    "cat": "montana",
    "m": "Los valles de montaña se forman entre cordones."
  },
  {
    "it": "Territorio parejo que permite trazar rutas rectas por kilómetros",
    "cat": "llanura",
    "m": "Sin obstáculos, la ruta va derecho."
  },
  {
    "it": "Terreno escalonado que termina en un acantilado sobre el mar",
    "cat": "meseta",
    "m": "Así llega la meseta patagónica a la costa."
  }
];
GAMES.ambientes_4 = juegoClasificar(CUR_AMBIENTES_4_BANCO, "¿Qué tipo de relieve es?", [{"cat": "montana", "label": "⛰️ Montaña"}, {"cat": "llanura", "label": "🌾 Llanura"}, {"cat": "meseta", "label": "🪨 Meseta"}], "ambientes_");

/* 4° · ¿Urbano, rural o periurbano? — urbano_rural_4
   DC: Espacios urbanos, rurales y periurbanos; articulación y servicios
   Fuente: docs/auditoria-dc-caba/grado-4.md · S6 */
const CUR_URBANO_RURAL_4_BANCO = [
  {
    "it": "Edificios altos, subte y mucha gente por metro cuadrado",
    "cat": "urbano",
    "m": "Población concentrada y servicios: ciudad."
  },
  {
    "it": "Campo de soja de 200 hectáreas",
    "cat": "rural",
    "m": "Mucha superficie y poca gente: espacio rural."
  },
  {
    "it": "Quintas de verdura que abastecen a la ciudad de al lado",
    "cat": "periurbano",
    "m": "El cinturón que rodea la ciudad y la alimenta: ni campo abierto ni ciudad."
  },
  {
    "it": "Barrio con veredas, semáforos y colectivos cada cinco minutos",
    "cat": "urbano",
    "m": "Servicios urbanos completos."
  },
  {
    "it": "Tambo con 300 vacas lecheras",
    "cat": "rural",
    "m": "Producción agropecuaria en el campo."
  },
  {
    "it": "Zona de galpones y depósitos entre la ruta y el último barrio",
    "cat": "periurbano",
    "m": "El borde recibe lo que la ciudad no quiere adentro: depósitos, logística, plantas."
  },
  {
    "it": "Pueblo de 400 habitantes rodeado de sembrados",
    "cat": "rural",
    "m": "Poca gente y actividad ligada al campo."
  },
  {
    "it": "Avenida con locales, oficinas y estacionamiento medido",
    "cat": "urbano",
    "m": "Comercio y servicios densos."
  },
  {
    "it": "Viveros y criaderos de pollos a 20 minutos del centro",
    "cat": "periurbano",
    "m": "Actividad de campo pero pegada a la ciudad, que es su cliente."
  },
  {
    "it": "Estancia con casco, molino y alambrados",
    "cat": "rural",
    "m": "Establecimiento agropecuario."
  },
  {
    "it": "Hospital grande al que llega gente de toda la zona",
    "cat": "urbano",
    "m": "La ciudad concentra los servicios que usa también el campo de alrededor: por eso están articulados."
  },
  {
    "it": "Barrio nuevo construido donde antes había quintas",
    "cat": "periurbano",
    "m": "El borde se va corriendo: lo que era quinta hoy es barrio."
  },
  {
    "it": "Silos y acopio de granos al costado de la ruta",
    "cat": "rural",
    "m": "Infraestructura de la producción agrícola."
  },
  {
    "it": "Plaza con juegos, rodeada de edificios de departamentos",
    "cat": "urbano",
    "m": "Espacio público de la ciudad."
  },
  {
    "it": "Basural y planta de tratamiento en las afueras",
    "cat": "periurbano",
    "m": "La ciudad manda al borde lo que produce y no puede alojar."
  }
];
GAMES.urbano_rural_4 = juegoClasificar(CUR_URBANO_RURAL_4_BANCO, "¿Qué tipo de espacio es?", [{"cat": "urbano", "label": "🏙️ Urbano"}, {"cat": "rural", "label": "🚜 Rural"}, {"cat": "periurbano", "label": "🌱 El borde"}], "urbano_rur");

/* 4° · Mecanismos y energía — mecanismos_4
   DC: Bielas, manivelas y levas; conversiones de energía; motor, transmisión y efector
   Fuente: docs/auditoria-dc-caba/grado-4.md · T2 */
const CUR_MECANISMOS_4_BANCO = [
  {
    "q": "Un motor, ¿crea la energía que usa la máquina?",
    "ops": [
      "No: la transforma de una forma a otra",
      "Sí, la fabrica",
      "Sí, la saca del aire"
    ],
    "m": "Este es EL error del tema. La energía no se crea ni se destruye: el motor la transforma (eléctrica → movimiento, por ejemplo)."
  },
  {
    "q": "¿Para qué sirve una manivela?",
    "ops": [
      "Para hacer girar algo con la mano",
      "Para frenar",
      "Para medir"
    ],
    "m": "La manivela convierte tu fuerza en giro."
  },
  {
    "q": "¿Qué hace una biela?",
    "ops": [
      "Convierte el giro en un movimiento de ida y vuelta",
      "Multiplica la velocidad",
      "Enfría el motor"
    ],
    "m": "Biela y manivela juntas pasan de circular a alternativo (ida y vuelta) y al revés."
  },
  {
    "q": "El pedal de la bicicleta gira y la rueda gira. ¿Qué tipo de movimiento es?",
    "ops": [
      "Circular en los dos",
      "Alternativo",
      "Rectilíneo"
    ],
    "m": "Los dos giran: la cadena transmite el movimiento circular."
  },
  {
    "q": "¿Qué hace una leva?",
    "ops": [
      "Convierte el giro en un empuje hacia arriba y abajo",
      "Frena el eje",
      "Genera electricidad"
    ],
    "m": "La leva es una rueda de forma irregular: al girar, levanta y suelta una pieza. Así se mueven los muñecos de los juguetes a cuerda."
  },
  {
    "q": "En una licuadora, ¿cuál es el efector?",
    "ops": [
      "La cuchilla que corta",
      "El cable",
      "El motor"
    ],
    "m": "El efector es la parte que hace el trabajo final. El motor da la energía, la transmisión la lleva y el efector actúa."
  },
  {
    "q": "En un ventilador, ¿cuál es la transmisión?",
    "ops": [
      "El eje que une el motor con las paletas",
      "El enchufe",
      "Las paletas"
    ],
    "m": "La transmisión lleva el movimiento del motor al efector."
  },
  {
    "q": "Una linterna a pilas: ¿qué transformación hace?",
    "ops": [
      "De energía química a luz",
      "De luz a movimiento",
      "De sonido a luz"
    ],
    "m": "La pila guarda energía química y la lámpara la vuelve luz (y algo de calor)."
  },
  {
    "q": "Un molino de viento: ¿qué transformación hace?",
    "ops": [
      "De movimiento del aire a movimiento del eje",
      "De luz a movimiento",
      "De sonido a electricidad"
    ],
    "m": "El viento empuja las aspas y hace girar el eje."
  },
  {
    "q": "¿Para qué sirve una polea?",
    "ops": [
      "Para levantar peso con menos esfuerzo o cambiar la dirección de la fuerza",
      "Para generar energía",
      "Para medir el peso"
    ],
    "m": "La polea no crea fuerza: la redirige o la reparte."
  },
  {
    "q": "Dos engranajes: uno grande y uno chico. Si gira el grande, el chico…",
    "ops": [
      "Gira más rápido",
      "Gira más lento",
      "Gira igual"
    ],
    "m": "El chico da más vueltas en el mismo tiempo: menos fuerza, más velocidad."
  },
  {
    "q": "¿Qué transformación hace una plancha?",
    "ops": [
      "De electricidad a calor",
      "De calor a electricidad",
      "De movimiento a luz"
    ],
    "m": "La resistencia convierte la electricidad en calor."
  },
  {
    "q": "En una máquina, ¿de dónde sale la energía del motor?",
    "ops": [
      "De una fuente externa: enchufe, pila, combustible",
      "Del propio motor",
      "Del movimiento que produce"
    ],
    "m": "Sin fuente no hay movimiento: el motor solo no genera nada."
  },
  {
    "q": "Un juguete a cuerda: ¿dónde está guardada la energía?",
    "ops": [
      "En el resorte tensado",
      "En las ruedas",
      "En el color"
    ],
    "m": "Al dar cuerda guardás energía en el resorte y después se libera."
  }
];
GAMES.mecanismos_4 = juegoTriviaTexto(CUR_MECANISMOS_4_BANCO, "¿Cómo funciona la máquina?", "mecanismos");

/* 4° · Detectives digitales — fuentes_digitales_4
   DC: IA en aplicaciones cotidianas; confiabilidad y procedencia de las fuentes
   Fuente: docs/auditoria-dc-caba/grado-4.md · T3 */
const CUR_FUENTES_DIGITALES_4_BANCO = [
  {
    "it": "Una noticia publicada por un diario que firma quién la escribió",
    "cat": "confiable",
    "m": "Tiene autor y responsable: se puede reclamar si está mal."
  },
  {
    "it": "Un video donde una persona famosa dice algo rarísimo, sin fuente",
    "cat": "dudoso",
    "m": "Hoy se puede generar un video falso de cualquiera. Sin fuente, desconfiar."
  },
  {
    "it": "Una foto muy linda de un paisaje, sin ningún dato",
    "cat": "faltadato",
    "m": "Puede ser una foto real o generada. Con sólo mirarla no alcanza: habría que buscar de dónde salió."
  },
  {
    "it": "Una página de un museo nacional explicando su colección",
    "cat": "confiable",
    "m": "Institución conocida y responsable de lo que publica."
  },
  {
    "it": "Un mensaje reenviado que dice «pasalo a 10 contactos o pasa algo malo»",
    "cat": "dudoso",
    "m": "La urgencia y la cadena son señales clásicas de engaño."
  },
  {
    "it": "Un texto que te dio un asistente de IA, sin decir de dónde lo sacó",
    "cat": "faltadato",
    "m": "Puede estar bien o puede estar inventado. Hay que verificarlo en otra fuente antes de usarlo."
  },
  {
    "it": "Un artículo de enciclopedia con la lista de fuentes al final",
    "cat": "confiable",
    "m": "Se puede ir a chequear de dónde sacó cada dato."
  },
  {
    "it": "Una cuenta creada ayer que promete regalar celulares",
    "cat": "dudoso",
    "m": "Cuenta nueva + promesa demasiado buena = estafa casi segura."
  },
  {
    "it": "Un gráfico sin decir quién hizo la medición ni cuándo",
    "cat": "faltadato",
    "m": "Un gráfico parece serio, pero sin fuente ni fecha no se puede evaluar."
  },
  {
    "it": "El sitio oficial del gobierno de la Ciudad con los horarios de vacunación",
    "cat": "confiable",
    "m": "Fuente oficial del tema que consultás."
  },
  {
    "it": "Una foto de un animal que nunca existió, presentada como real",
    "cat": "dudoso",
    "m": "Si no coincide con nada conocido, conviene buscar en más de un lugar."
  },
  {
    "it": "Un audio de alguien de tu familia pidiéndote plata con urgencia",
    "cat": "dudoso",
    "m": "Se puede imitar una voz con IA. Ante una urgencia con plata, cortar y llamar vos a esa persona."
  },
  {
    "it": "Una receta de cocina de un canal con miles de comentarios",
    "cat": "faltadato",
    "m": "Que sea popular no la hace correcta: los comentarios no son una fuente."
  },
  {
    "it": "Un libro de texto de la escuela",
    "cat": "confiable",
    "m": "Pasó por autores, editorial y revisión."
  },
  {
    "it": "Una imagen donde alguien tiene seis dedos en una mano",
    "cat": "dudoso",
    "m": "Los errores en manos y textos son pistas de imagen generada, aunque cada vez menos."
  },
  {
    "it": "Un dato que te repitieron dos amigos distintos",
    "cat": "faltadato",
    "m": "Que dos personas lo repitan no lo hace cierto: puede que los dos lo hayan leído del mismo lugar equivocado."
  }
];
GAMES.fuentes_digitales_4 = juegoClasificar(CUR_FUENTES_DIGITALES_4_BANCO, "¿Se puede confiar en esto?", [{"cat": "confiable", "label": "✅ Se puede confiar"}, {"cat": "dudoso", "label": "⚠️ Desconfiar"}, {"cat": "faltadato", "label": "🤷 No alcanza para saber"}], "fuentes_di");

/* 4° · Separá en origen — residuos_4
   DC: Ed. Ambiental: corrientes de residuos, separación en origen, compostaje
   Fuente: docs/auditoria-dc-caba/grado-4.md · X1 */
const CUR_RESIDUOS_4_BANCO = [
  {
    "it": "Botella de plástico vacía y enjuagada",
    "cat": "reciclable",
    "m": "Limpia y seca, el plástico se recicla."
  },
  {
    "it": "Cáscara de banana",
    "cat": "organico",
    "m": "Va al compost: se transforma en tierra."
  },
  {
    "it": "Pila usada",
    "cat": "especial",
    "m": "Contamina muchísima agua. Va a un punto de recepción especial, nunca al cesto común."
  },
  {
    "it": "Servilleta usada con grasa",
    "cat": "basura",
    "m": "El papel sucio de grasa ya no se puede reciclar."
  },
  {
    "it": "Hoja de cuaderno escrita",
    "cat": "reciclable",
    "m": "El papel escrito se recicla igual."
  },
  {
    "it": "Restos de yerba del mate",
    "cat": "organico",
    "m": "Excelente para el compost."
  },
  {
    "it": "Lata de tomate enjuagada",
    "cat": "reciclable",
    "m": "El metal se recicla muchas veces sin perder calidad."
  },
  {
    "it": "Botella de aceite sin lavar",
    "cat": "basura",
    "m": "Trampa del tema: el plástico se recicla, pero SUCIO de aceite arruina el lote entero. Enjuagada sí, así no."
  },
  {
    "it": "Cáscara de huevo",
    "cat": "organico",
    "m": "Va al compost; conviene molerla."
  },
  {
    "it": "Tubo fluorescente quemado",
    "cat": "especial",
    "m": "Tiene mercurio: recepción diferenciada."
  },
  {
    "it": "Diario viejo",
    "cat": "reciclable",
    "m": "Papel limpio y seco."
  },
  {
    "it": "Restos de comida cocida",
    "cat": "organico",
    "m": "Va al compost, aunque conviene evitar carne y lácteos en el de casa."
  },
  {
    "it": "Envoltorio metalizado de golosina",
    "cat": "basura",
    "m": "Mezcla plástico y aluminio pegados: hoy no se puede separar."
  },
  {
    "it": "Frasco de vidrio enjuagado",
    "cat": "reciclable",
    "m": "El vidrio se recicla infinitas veces."
  },
  {
    "it": "Celular roto",
    "cat": "especial",
    "m": "Los aparatos electrónicos van a puntos de residuos electrónicos."
  },
  {
    "it": "Hojas secas del patio",
    "cat": "organico",
    "m": "Son la parte 'marrón' del compost, la que da carbono."
  },
  {
    "it": "Cartón de una caja",
    "cat": "reciclable",
    "m": "Plegado ocupa menos y se recicla."
  },
  {
    "it": "Medicamento vencido",
    "cat": "especial",
    "m": "Se devuelve a la farmacia: tirado contamina el agua."
  }
];
GAMES.residuos_4 = juegoClasificar(CUR_RESIDUOS_4_BANCO, "¿En qué cesto va?", [{"cat": "reciclable", "label": "♻️ Reciclable"}, {"cat": "organico", "label": "🍌 Orgánico"}, {"cat": "basura", "label": "🗑️ Basura"}, {"cat": "especial", "label": "☣️ Especial"}], "residuos_4");

/* 4° · ¿Necesidad o deseo? — necesidad_deseo_4
   DC: Ed. Financiera: necesidades y deseos; ahorro = ingreso − gasto
   Fuente: docs/auditoria-dc-caba/grado-4.md · X2 */
const CUR_NECESIDAD_DESEO_4_BANCO = [
  {
    "it": "Comer todos los días",
    "cat": "necesidad",
    "m": "Sin comida no se vive: es una necesidad básica."
  },
  {
    "it": "La última consola de videojuegos",
    "cat": "deseo",
    "m": "Se puede vivir sin ella."
  },
  {
    "it": "Una computadora",
    "cat": "depende",
    "m": "Para quien estudia o trabaja con ella es una necesidad; para quien sólo la quiere para jugar, un deseo."
  },
  {
    "it": "Tener dónde dormir bajo techo",
    "cat": "necesidad",
    "m": "La vivienda es una necesidad básica."
  },
  {
    "it": "Una remera de la marca que está de moda",
    "cat": "deseo",
    "m": "Necesitás ropa; necesitar ESA marca es otra cosa."
  },
  {
    "it": "Un par de zapatillas",
    "cat": "depende",
    "m": "Si no tenés ninguna, es necesidad. Si es el quinto par, es deseo."
  },
  {
    "it": "Ir al médico cuando estás enfermo",
    "cat": "necesidad",
    "m": "La salud es una necesidad."
  },
  {
    "it": "Salir a jugar con amigos",
    "cat": "necesidad",
    "m": "Jugar y estar con otros no es un lujo: es parte de crecer sano. Es un derecho de los chicos."
  },
  {
    "it": "Un celular con la mejor cámara del mercado",
    "cat": "deseo",
    "m": "Comunicarte puede ser necesario; tener el mejor modelo no."
  },
  {
    "it": "Agua potable",
    "cat": "necesidad",
    "m": "Necesidad básica."
  },
  {
    "it": "Ir al cine el fin de semana",
    "cat": "deseo",
    "m": "Es lindo y vale la pena planificarlo, pero no es imprescindible."
  },
  {
    "it": "Un abrigo en invierno",
    "cat": "necesidad",
    "m": "Protegerse del frío es una necesidad."
  },
  {
    "it": "Un instrumento musical",
    "cat": "depende",
    "m": "Para quien estudia música es una herramienta; para quien lo quiere probar un rato, un deseo."
  },
  {
    "it": "Ahorrar un poco de lo que te dan cada semana",
    "cat": "necesidad",
    "m": "No es un gasto: es lo que te permite después comprar lo que querés sin pedir prestado. Ahorro = lo que entra menos lo que gastás."
  },
  {
    "it": "Ir a la escuela",
    "cat": "necesidad",
    "m": "Educarse es una necesidad y un derecho."
  },
  {
    "it": "Comprar figuritas todos los días",
    "cat": "deseo",
    "m": "Gasto chico y repetido: sumado en el mes suele ser más de lo que parece."
  }
];
GAMES.necesidad_deseo_4 = juegoClasificar(CUR_NECESIDAD_DESEO_4_BANCO, "¿Qué es para vos?", [{"cat": "necesidad", "label": "🥖 Necesidad"}, {"cat": "deseo", "label": "🎁 Deseo"}, {"cat": "depende", "label": "🤔 Depende de la situación"}], "necesidad_");

/* 4° · Semáforo de la convivencia — convivencia_4
   DC: ESI: diálogo ante burlas y exclusiones; a quiénes acudir; huella digital
   Fuente: docs/auditoria-dc-caba/grado-4.md · X3 */
const CUR_CONVIVENCIA_4_BANCO = [
  {
    "q": "Si alguien te molesta seguido y no sabés qué hacer, ¿qué conviene?",
    "ops": [
      "Contarle a un adulto de confianza",
      "Guardártelo",
      "Devolver la agresión"
    ],
    "m": "Pedir ayuda no es acusar: es lo que corta la situación."
  },
  {
    "q": "¿Quiénes pueden ser adultos de confianza en la escuela?",
    "ops": [
      "La maestra, la directora, el preceptor",
      "Sólo la familia",
      "Nadie"
    ],
    "m": "En la escuela también hay adultos a cargo de cuidarte."
  },
  {
    "q": "Ves que a un compañero lo dejan afuera de todos los juegos. ¿Eso es?",
    "ops": [
      "Exclusión, y afecta a esa persona",
      "Algo normal",
      "Un problema sólo suyo"
    ],
    "m": "Dejar afuera sistemáticamente también es una forma de maltrato, aunque nadie grite ni pegue."
  },
  {
    "q": "¿Qué es la huella digital?",
    "ops": [
      "El rastro que dejan tus mensajes y fotos en internet",
      "La marca del dedo en la pantalla",
      "Un virus"
    ],
    "m": "Lo que subís puede quedar aunque lo borres: otros pueden haberlo guardado."
  },
  {
    "q": "Alguien te manda una foto de otro compañero para burlarse. ¿Qué conviene?",
    "ops": [
      "No reenviarla y contarle a un adulto",
      "Reenviarla a los amigos",
      "Contestar con otra foto"
    ],
    "m": "Reenviar hace más grande el daño y también te involucra a vos."
  },
  {
    "q": "¿Está bien que alguien te pida datos personales por un juego online?",
    "ops": [
      "No, y conviene avisarle a un adulto",
      "Sí, si el juego es conocido",
      "Sí, si te lo pide un jugador amable"
    ],
    "m": "Dirección, escuela y teléfono no se comparten con desconocidos."
  },
  {
    "q": "Un chiste que hace reír a todos menos a la persona de la que se ríen, ¿qué es?",
    "ops": [
      "Una burla",
      "Un chiste sin importancia",
      "Un juego"
    ],
    "m": "La señal es cómo se siente esa persona, no cuántos se rieron."
  },
  {
    "q": "¿Todos los chicos tienen derecho a jugar y a ser escuchados?",
    "ops": [
      "Sí, son derechos de todos los chicos",
      "Sólo los que se portan bien",
      "Sólo los más grandes"
    ],
    "m": "Los derechos de niñas y niños no se ganan portándose bien: se tienen."
  },
  {
    "q": "Si contás algo que te preocupa y el primer adulto no te escucha, ¿qué hacés?",
    "ops": [
      "Buscás a otro adulto de confianza",
      "No lo contás más",
      "Te enojás y listo"
    ],
    "m": "Insistir con otra persona es parte de pedir ayuda."
  },
  {
    "q": "¿Qué significa que algo publicado en internet es difícil de borrar?",
    "ops": [
      "Que alguien pudo copiarlo antes de que lo borraras",
      "Que la app cobra por borrarlo",
      "Que se borra solo al año"
    ],
    "m": "Por eso conviene pensar antes de subir, más que borrar después."
  },
  {
    "q": "Ver una situación de maltrato y no decir nada, ¿ayuda?",
    "ops": [
      "No: el silencio deja que siga",
      "Sí, evita problemas",
      "Es lo mismo"
    ],
    "m": "No hace falta enfrentarse a nadie: alcanza con avisarle a un adulto."
  },
  {
    "q": "¿Se puede estar en desacuerdo con un compañero sin pelear?",
    "ops": [
      "Sí, se puede decir lo que pensás sin agredir",
      "No, siempre termina en pelea",
      "Sólo si el otro cede"
    ],
    "m": "Discutir ideas está bien; lastimar a la persona no."
  }
];
GAMES.convivencia_4 = juegoTriviaTexto(CUR_CONVIVENCIA_4_BANCO, "Pensemos juntos.", "convivenci");

/* 4° · Armá el número — valor_posicional_4
   DC: Valor posicional; composición y descomposición aditiva y multiplicativa
   Fuente: docs/auditoria-dc-caba/grado-4.md · M2 */
const CUR_VALOR_POSICIONAL_4_BANCO = [
  {
    "q": "¿Cómo se escribe treinta y cuatro mil quinientos siete?",
    "ops": [
      "34.507",
      "34.000.507",
      "340.507"
    ],
    "m": "Error clásico: escribir tal como se dice, pegando 34.000 y 507. Treinta y cuatro mil son 34.000 y el 507 ocupa las tres últimas cifras: 34.507."
  },
  {
    "q": "¿Cómo se escribe ocho mil cuarenta?",
    "ops": [
      "8.040",
      "8.400",
      "80.040"
    ],
    "m": "Cuarenta son 40: van en las decenas. El cero del medio guarda el lugar de las centenas."
  },
  {
    "q": "¿Cuánto vale el 7 en 47.192?",
    "ops": [
      "7.000",
      "700",
      "7"
    ],
    "m": "Está en la posición de los miles: vale 7.000."
  },
  {
    "q": "¿Cuánto vale el 3 en 35.208?",
    "ops": [
      "30.000",
      "3.000",
      "300"
    ],
    "m": "Es la primera cifra de un número de 5: son decenas de mil."
  },
  {
    "q": "20.000 + 6.000 + 300 + 40 + 5 = ",
    "ops": [
      "26.345",
      "26.045",
      "20.345"
    ],
    "m": "Cada sumando ocupa su posición: 2-6-3-4-5."
  },
  {
    "q": "¿Cómo se descompone 50.403?",
    "ops": [
      "50.000 + 400 + 3",
      "50.000 + 40 + 3",
      "5.000 + 400 + 3"
    ],
    "m": "El 4 está en las centenas (400) y hay un cero en las decenas."
  },
  {
    "q": "¿Qué número es 6 × 10.000 + 2 × 100 + 9?",
    "ops": [
      "60.209",
      "62.009",
      "60.029"
    ],
    "m": "Descomposición multiplicativa: 60.000 + 200 + 9."
  },
  {
    "q": "¿Cuál es el número que sigue a 39.999?",
    "ops": [
      "40.000",
      "39.9910",
      "310.000"
    ],
    "m": "Se llenan todas las posiciones y sube la siguiente."
  },
  {
    "q": "¿Cuál es mayor: 9.876 o 10.234?",
    "ops": [
      "10.234",
      "9.876",
      "Son iguales"
    ],
    "m": "Tiene más cifras: 5 contra 4. Más cifras siempre es mayor."
  },
  {
    "q": "¿Cuál es mayor: 45.100 o 45.010?",
    "ops": [
      "45.100",
      "45.010",
      "Son iguales"
    ],
    "m": "Con la misma cantidad de cifras se comparan de izquierda a derecha: en las centenas hay 1 contra 0."
  },
  {
    "q": "Si a 7.000 le sumo 10 veces 100, ¿cuánto da?",
    "ops": [
      "8.000",
      "7.100",
      "7.010"
    ],
    "m": "10 × 100 = 1.000. Así que 7.000 + 1.000 = 8.000."
  },
  {
    "q": "¿Cuántas decenas hay en 3.500?",
    "ops": [
      "350",
      "35",
      "3.500"
    ],
    "m": "Cada decena son 10: 3.500 ÷ 10 = 350 decenas."
  },
  {
    "q": "¿Cómo se escribe cien mil?",
    "ops": [
      "100.000",
      "10.000",
      "1.000.000"
    ],
    "m": "Cien mil tiene 6 cifras: un 1 y cinco ceros."
  },
  {
    "q": "¿Qué número es 4 × 1.000 + 7 × 10?",
    "ops": [
      "4.070",
      "4.700",
      "4.007"
    ],
    "m": "7 × 10 = 70: van en las decenas."
  },
  {
    "q": "En 82.361, ¿qué cifra ocupa el lugar de las centenas?",
    "ops": [
      "El 3",
      "El 6",
      "El 2"
    ],
    "m": "Contando de derecha a izquierda: 1 unidades, 6 decenas, 3 centenas."
  },
  {
    "q": "¿Cómo se escribe setenta mil ocho?",
    "ops": [
      "70.008",
      "70.800",
      "7.008"
    ],
    "m": "Setenta mil son 70.000 y el 8 va en las unidades: hay que rellenar con ceros el medio."
  }
];
GAMES.valor_posicional_4 = juegoTriviaTexto(CUR_VALOR_POSICIONAL_4_BANCO, "¿Qué número es?", "valor_posi");

/* 4° · Resta con canje — resta_canje_4
   DC: Algoritmo de resta analizado en rangos de 10.000 y 100.000
   Fuente: docs/auditoria-dc-caba/grado-4.md · M4 */
GAMES.resta_canje_4 = { crear(ctx) { return GAMES.resta_columnas.crear(ctx); } };

/* 4° · ¿Se arma el triángulo? — triangulos_4
   DC: Construcción de triángulos dados los lados; clasificación; desigualdad triangular
   Fuente: docs/auditoria-dc-caba/grado-4.md · M13 */
const CUR_TRIANGULOS_4_BANCO = [
  {
    "it": "3 cm, 3 cm y 3 cm",
    "cat": "equilatero",
    "m": "Los tres lados iguales: equilátero."
  },
  {
    "it": "5 cm, 5 cm y 8 cm",
    "cat": "isosceles",
    "m": "Dos iguales y uno distinto. Y se arma: 5 + 5 = 10, que es más que 8."
  },
  {
    "it": "4 cm, 6 cm y 9 cm",
    "cat": "escaleno",
    "m": "Los tres distintos, y SÍ se arma: 4 + 6 = 10, más que 9. Por poco, pero alcanza."
  },
  {
    "it": "4 cm, 5 cm y 9 cm",
    "cat": "nose",
    "m": "Acá NO: 4 + 5 = 9, justo igual al lado largo. Las varillas quedan estiradas en línea recta y no cierran. Tienen que SUPERAR al lado largo."
  },
  {
    "it": "2 cm, 3 cm y 7 cm",
    "cat": "nose",
    "m": "2 + 3 = 5, muy poco para llegar a 7: no se tocan."
  },
  {
    "it": "6 cm, 6 cm y 6 cm",
    "cat": "equilatero",
    "m": "Los tres iguales."
  },
  {
    "it": "7 cm, 7 cm y 10 cm",
    "cat": "isosceles",
    "m": "Dos iguales; 7 + 7 = 14 supera a 10, así que cierra."
  },
  {
    "it": "3 cm, 4 cm y 5 cm",
    "cat": "escaleno",
    "m": "Los tres distintos; 3 + 4 = 7 supera a 5."
  },
  {
    "it": "1 cm, 2 cm y 3 cm",
    "cat": "nose",
    "m": "1 + 2 = 3, igual al largo: queda una línea, no un triángulo."
  },
  {
    "it": "8 cm, 8 cm y 3 cm",
    "cat": "isosceles",
    "m": "Dos lados de 8 y uno de 3: cierra sin problema."
  },
  {
    "it": "5 cm, 12 cm y 13 cm",
    "cat": "escaleno",
    "m": "Los tres distintos; 5 + 12 = 17 supera a 13."
  },
  {
    "it": "2 cm, 2 cm y 5 cm",
    "cat": "nose",
    "m": "2 + 2 = 4, no llega a 5. Aunque haya dos lados iguales, no se arma."
  },
  {
    "it": "10 cm, 10 cm y 10 cm",
    "cat": "equilatero",
    "m": "Los tres iguales."
  },
  {
    "it": "9 cm, 9 cm y 4 cm",
    "cat": "isosceles",
    "m": "Dos iguales de 9 y uno corto: cierra."
  },
  {
    "it": "6 cm, 7 cm y 8 cm",
    "cat": "escaleno",
    "m": "Los tres distintos; 6 + 7 = 13 supera a 8."
  },
  {
    "it": "3 cm, 3 cm y 7 cm",
    "cat": "nose",
    "m": "3 + 3 = 6, no alcanza para 7."
  },
  {
    "it": "4 cm, 4 cm y 4 cm",
    "cat": "equilatero",
    "m": "Los tres iguales."
  },
  {
    "it": "5 cm, 9 cm y 5 cm",
    "cat": "isosceles",
    "m": "Ojo al orden: los iguales son el primero y el tercero. 5 + 5 = 10 supera a 9."
  },
  {
    "it": "7 cm, 8 cm y 13 cm",
    "cat": "escaleno",
    "m": "Los tres distintos; 7 + 8 = 15 supera a 13."
  },
  {
    "it": "5 cm, 5 cm y 10 cm",
    "cat": "nose",
    "m": "5 + 5 = 10, exactamente el lado largo: queda plano. Hace falta SUPERARLO."
  }
];
GAMES.triangulos_4 = juegoClasificar(CUR_TRIANGULOS_4_BANCO, "Con estas tres varillas, ¿qué triángulo sale?", [{"cat": "equilatero", "label": "🔺 Los 3 lados iguales"}, {"cat": "isosceles", "label": "🔻 2 lados iguales"}, {"cat": "escaleno", "label": "📐 Los 3 distintos"}, {"cat": "nose", "label": "🚫 No se arma"}], "triangulos");

/* 4° · Caras y cuerpos — cuerpos_caras_4
   DC: Cubos y prismas: caras y figuras; circunferencia y círculo
   Fuente: docs/auditoria-dc-caba/grado-4.md · M14 */
const CUR_CUERPOS_CARAS_4_BANCO = [
  {
    "q": "¿Cuántas caras tiene un cubo?",
    "ops": [
      "6",
      "4",
      "8"
    ],
    "m": "Seis caras, todas cuadrados iguales."
  },
  {
    "q": "¿Qué figura son las caras de un cubo?",
    "ops": [
      "Cuadrados",
      "Triángulos",
      "Rectángulos distintos"
    ],
    "m": "Todas cuadradas y del mismo tamaño."
  },
  {
    "q": "¿Cuántas aristas tiene un cubo?",
    "ops": [
      "12",
      "6",
      "8"
    ],
    "m": "Las aristas son los bordes donde se juntan dos caras: 12."
  },
  {
    "q": "¿Cuántos vértices tiene un cubo?",
    "ops": [
      "8",
      "6",
      "12"
    ],
    "m": "Los vértices son las puntas: 8."
  },
  {
    "q": "Una caja de zapatos, ¿qué cuerpo es?",
    "ops": [
      "Un prisma rectangular",
      "Un cubo",
      "Una pirámide"
    ],
    "m": "Tiene 6 caras rectangulares, pero no todas iguales: por eso no es cubo."
  },
  {
    "q": "¿Qué caras tiene un prisma de base triangular?",
    "ops": [
      "2 triángulos y 3 rectángulos",
      "5 triángulos",
      "3 triángulos y 2 rectángulos"
    ],
    "m": "Las dos bases son triángulos y los costados, rectángulos."
  },
  {
    "q": "¿Cuántas caras tiene una pirámide de base cuadrada?",
    "ops": [
      "5",
      "4",
      "6"
    ],
    "m": "La base cuadrada más 4 triángulos que suben a la punta."
  },
  {
    "q": "¿Cuál es la diferencia entre circunferencia y círculo?",
    "ops": [
      "La circunferencia es la línea; el círculo, la línea con lo de adentro",
      "Son lo mismo",
      "El círculo es más grande"
    ],
    "m": "La circunferencia es el borde; el círculo incluye toda la superficie."
  },
  {
    "q": "¿Qué es el radio de una circunferencia?",
    "ops": [
      "La distancia del centro al borde",
      "La distancia de borde a borde",
      "La línea de afuera"
    ],
    "m": "El diámetro va de borde a borde pasando por el centro y mide el doble del radio."
  },
  {
    "q": "Si el radio mide 3 cm, ¿cuánto mide el diámetro?",
    "ops": [
      "6 cm",
      "3 cm",
      "1,5 cm"
    ],
    "m": "El diámetro es siempre el doble del radio."
  },
  {
    "q": "¿Qué cuerpo tiene una sola cara curva y ninguna plana?",
    "ops": [
      "La esfera",
      "El cilindro",
      "El cono"
    ],
    "m": "La esfera es toda curva. El cilindro tiene dos círculos planos."
  },
  {
    "q": "¿Qué caras tiene un cilindro?",
    "ops": [
      "Dos círculos y una superficie curva",
      "Sólo círculos",
      "Seis rectángulos"
    ],
    "m": "Si lo desarmás, el costado desplegado es un rectángulo."
  },
  {
    "q": "¿Todos los prismas tienen las dos bases iguales?",
    "ops": [
      "Sí, iguales y paralelas",
      "No, siempre distintas",
      "Sólo el cubo"
    ],
    "m": "Esa es la definición de prisma."
  },
  {
    "q": "Si desarmás un cubo y lo aplanás, ¿qué obtenés?",
    "ops": [
      "Seis cuadrados unidos",
      "Un cuadrado grande",
      "Cuatro triángulos"
    ],
    "m": "Se llama desarrollo: las 6 caras estiradas sobre el papel."
  }
];
GAMES.cuerpos_caras_4 = juegoTriviaTexto(CUR_CUERPOS_CARAS_4_BANCO, "Pensá el cuerpo por dentro y por fuera.", "cuerpos_ca");

/* 4° · Emparejar medidas — equivalencias_medida_4
   DC: Equivalencias km-m-cm-mm; kg-g-tonelada
   Fuente: docs/auditoria-dc-caba/grado-4.md · M16 */
const CUR_EQUIVALENCIAS_MEDIDA_4_BANCO = [
  {
    "q": "1 metro = ",
    "ops": [
      "100 cm",
      "10 cm",
      "1.000 cm"
    ],
    "m": "Un metro tiene 100 centímetros."
  },
  {
    "q": "1 kilómetro = ",
    "ops": [
      "1.000 m",
      "100 m",
      "10.000 m"
    ],
    "m": "'Kilo' quiere decir mil."
  },
  {
    "q": "1 centímetro = ",
    "ops": [
      "10 mm",
      "100 mm",
      "1.000 mm"
    ],
    "m": "Un centímetro tiene 10 milímetros: mirá la regla."
  },
  {
    "q": "1 kilogramo = ",
    "ops": [
      "1.000 g",
      "100 g",
      "10.000 g"
    ],
    "m": "Kilo es mil: 1.000 gramos."
  },
  {
    "q": "1 tonelada = ",
    "ops": [
      "1.000 kg",
      "100 kg",
      "10.000 kg"
    ],
    "m": "Una tonelada son mil kilos: más o menos un auto chico."
  },
  {
    "q": "250 cm = ",
    "ops": [
      "2,5 m",
      "25 m",
      "0,25 m"
    ],
    "m": "Cada 100 cm es 1 m: 250 cm son 2 m y medio."
  },
  {
    "q": "3.000 m = ",
    "ops": [
      "3 km",
      "30 km",
      "300 km"
    ],
    "m": "Cada 1.000 m es 1 km."
  },
  {
    "q": "500 g = ",
    "ops": [
      "medio kilo",
      "5 kilos",
      "50 kilos"
    ],
    "m": "La mitad de 1.000 g."
  },
  {
    "q": "1.500 g = ",
    "ops": [
      "1 kg y 500 g",
      "15 kg",
      "150 kg"
    ],
    "m": "Mil gramos son 1 kg y sobran 500 g."
  },
  {
    "q": "¿Qué es más largo: 1.200 m o 1 km?",
    "ops": [
      "1.200 m",
      "1 km",
      "Son iguales"
    ],
    "m": "1 km son 1.000 m, así que 1.200 m es más."
  },
  {
    "q": "¿Qué pesa más: 2.000 g o 3 kg?",
    "ops": [
      "3 kg",
      "2.000 g",
      "Son iguales"
    ],
    "m": "2.000 g son 2 kg, menos que 3 kg. Hay que pasar todo a la misma unidad antes de comparar."
  },
  {
    "q": "45 mm = ",
    "ops": [
      "4,5 cm",
      "45 cm",
      "0,45 cm"
    ],
    "m": "Cada 10 mm es 1 cm."
  },
  {
    "q": "¿Con qué unidad conviene medir el largo de un lápiz?",
    "ops": [
      "Centímetros",
      "Kilómetros",
      "Toneladas"
    ],
    "m": "Elegir la unidad adecuada evita números incómodos."
  },
  {
    "q": "¿Con qué unidad conviene medir la distancia entre dos ciudades?",
    "ops": [
      "Kilómetros",
      "Milímetros",
      "Gramos"
    ],
    "m": "En milímetros el número sería enorme."
  },
  {
    "q": "¿Con qué unidad conviene pesar un camión cargado?",
    "ops": [
      "Toneladas",
      "Gramos",
      "Milímetros"
    ],
    "m": "Para pesos muy grandes, la tonelada."
  },
  {
    "q": "2 m y 30 cm = ",
    "ops": [
      "230 cm",
      "23 cm",
      "2.030 cm"
    ],
    "m": "2 m son 200 cm, más 30 cm: 230 cm."
  },
  {
    "q": "¿Cuántos gramos son 2 kg y medio?",
    "ops": [
      "2.500 g",
      "250 g",
      "25.000 g"
    ],
    "m": "2.000 g más 500 g."
  },
  {
    "q": "Media tonelada = ",
    "ops": [
      "500 kg",
      "50 kg",
      "5.000 kg"
    ],
    "m": "La mitad de 1.000 kg."
  },
  {
    "q": "¿Qué mide más: 90 cm o 1 m?",
    "ops": [
      "1 m",
      "90 cm",
      "Son iguales"
    ],
    "m": "1 m son 100 cm, más que 90."
  },
  {
    "q": "7,5 km = ",
    "ops": [
      "7.500 m",
      "750 m",
      "75 m"
    ],
    "m": "7 km son 7.000 m y el medio kilómetro son 500 m."
  }
];
GAMES.equivalencias_medida_4 = juegoTriviaTexto(CUR_EQUIVALENCIAS_MEDIDA_4_BANCO, "¿Cuánto es lo mismo?", "equivalenc");

/* 5° · Cazador de recursos — recursos_poeticos_5
   DC: Personificación, comparación y metáfora
   Fuente: docs/auditoria-dc-caba/grado-5.md · L2 */
const CUR_RECURSOS_POETICOS_5_BANCO = [
  {
    "it": "«La luna me miraba desde el techo»",
    "cat": "personificacion",
    "m": "Mirar es algo que hacen las personas: se lo presta a la luna."
  },
  {
    "it": "«Sus ojos son como dos faroles»",
    "cat": "comparacion",
    "m": "Dice 'como': compara dos cosas sin decir que sean la misma."
  },
  {
    "it": "«Sus ojos son dos faroles»",
    "cat": "metafora",
    "m": "Sin el 'como', la reemplaza directamente: eso es metáfora."
  },
  {
    "it": "«El viento aullaba toda la noche»",
    "cat": "personificacion",
    "m": "Aullar es de un animal o una persona; se lo da al viento."
  },
  {
    "it": "«Corre tan rápido como el agua»",
    "cat": "comparacion",
    "m": "El 'tan… como' marca la comparación."
  },
  {
    "it": "«Tu risa es una campana»",
    "cat": "metafora",
    "m": "No dice que se PAREZCA a una campana: dice que ES una campana."
  },
  {
    "it": "«Las estrellas bailaban en el cielo»",
    "cat": "personificacion",
    "m": "Bailar es acción humana."
  },
  {
    "it": "«Blanca como la nieve»",
    "cat": "comparacion",
    "m": "El 'como' compara el color con la nieve."
  },
  {
    "it": "«La ciudad es una selva de cemento»",
    "cat": "metafora",
    "m": "Reemplaza la ciudad por la selva, sin comparar."
  },
  {
    "it": "«El reloj se quejaba en la pared»",
    "cat": "personificacion",
    "m": "Quejarse es de alguien que siente."
  },
  {
    "it": "«Es más lento que una tortuga»",
    "cat": "comparacion",
    "m": "'Más… que' compara."
  },
  {
    "it": "«El otoño es una carta amarilla»",
    "cat": "metafora",
    "m": "Sustituye una cosa por otra."
  },
  {
    "it": "«Las hojas susurraban un secreto»",
    "cat": "personificacion",
    "m": "Susurrar un secreto lo hace alguien que habla."
  },
  {
    "it": "«Duro como una piedra»",
    "cat": "comparacion",
    "m": "'Como' otra vez: comparación."
  },
  {
    "it": "«Sus manos eran dos pájaros nerviosos»",
    "cat": "metafora",
    "m": "Las manos SON pájaros: reemplazo, no comparación."
  },
  {
    "it": "«El sol se despertó temprano»",
    "cat": "personificacion",
    "m": "Despertarse es de un ser vivo."
  },
  {
    "it": "«Tan callado como un ratón»",
    "cat": "comparacion",
    "m": "El 'tan… como' es la marca."
  },
  {
    "it": "«La noche es un manto negro»",
    "cat": "metafora",
    "m": "La noche ES el manto, sin 'como'."
  }
];
GAMES.recursos_poeticos_5 = juegoClasificar(CUR_RECURSOS_POETICOS_5_BANCO, "¿Qué recurso usó el poeta?", [{"cat": "personificacion", "label": "🌙 Personificación"}, {"cat": "comparacion", "label": "⚖️ Comparación"}, {"cat": "metafora", "label": "🔮 Metáfora"}], "recursos_p");

/* 5° · Verbos en tres cajas — verbos_clases_5
   DC: Verbos de acción, de estado y psicológicos
   Fuente: docs/auditoria-dc-caba/grado-5.md · L3 */
const CUR_VERBOS_CLASES_5_BANCO = [
  {
    "it": "correr",
    "cat": "accion",
    "m": "Se hace con el cuerpo y se ve."
  },
  {
    "it": "ser",
    "cat": "estado",
    "m": "No indica acción: dice cómo se está o se es."
  },
  {
    "it": "pensar",
    "cat": "psicologico",
    "m": "Pasa adentro de la cabeza: es un proceso mental."
  },
  {
    "it": "saltar",
    "cat": "accion",
    "m": "Acción visible."
  },
  {
    "it": "estar",
    "cat": "estado",
    "m": "Verbo de estado por excelencia."
  },
  {
    "it": "querer",
    "cat": "psicologico",
    "m": "Es un sentimiento, no una acción."
  },
  {
    "it": "escribir",
    "cat": "accion",
    "m": "Se hace y se ve."
  },
  {
    "it": "parecer",
    "cat": "estado",
    "m": "Indica un estado o una apariencia."
  },
  {
    "it": "odiar",
    "cat": "psicologico",
    "m": "Sentimiento."
  },
  {
    "it": "cocinar",
    "cat": "accion",
    "m": "Acción."
  },
  {
    "it": "permanecer",
    "cat": "estado",
    "m": "Seguir en un estado."
  },
  {
    "it": "recordar",
    "cat": "psicologico",
    "m": "Proceso mental."
  },
  {
    "it": "nadar",
    "cat": "accion",
    "m": "Acción del cuerpo."
  },
  {
    "it": "resultar",
    "cat": "estado",
    "m": "Verbo copulativo: une con un estado."
  },
  {
    "it": "imaginar",
    "cat": "psicologico",
    "m": "Pasa en la mente."
  },
  {
    "it": "construir",
    "cat": "accion",
    "m": "Acción."
  },
  {
    "it": "temer",
    "cat": "psicologico",
    "m": "Sentimiento de miedo."
  },
  {
    "it": "quedar",
    "cat": "estado",
    "m": "Indica el estado en que algo queda."
  },
  {
    "it": "gritar",
    "cat": "accion",
    "m": "Acción, se oye."
  },
  {
    "it": "creer",
    "cat": "psicologico",
    "m": "Actividad de la mente."
  },
  {
    "it": "seguir",
    "cat": "estado",
    "m": "Ojo: cuando dice 'sigue enojado' es de estado. Si fuera 'sigue al perro' sería de acción: el contexto decide."
  },
  {
    "it": "extrañar",
    "cat": "psicologico",
    "m": "Sentimiento."
  }
];
GAMES.verbos_clases_5 = juegoClasificar(CUR_VERBOS_CLASES_5_BANCO, "¿Qué tipo de verbo es?", [{"cat": "accion", "label": "🏃 De acción"}, {"cat": "estado", "label": "🪑 De estado"}, {"cat": "psicologico", "label": "💭 Psicológico"}], "verbos_cla");

/* 5° · ¿Objeto directo o indirecto? — od_oi_5
   DC: Objeto directo e indirecto; prueba de sustitución por lo/le
   Fuente: docs/auditoria-dc-caba/grado-5.md · L4 */
const CUR_OD_OI_5_BANCO = [
  {
    "q": "Ana compró **un libro**. ¿Qué es 'un libro'?",
    "ops": [
      "Objeto directo",
      "Objeto indirecto",
      "Sujeto"
    ],
    "m": "Probá reemplazarlo: 'Ana LO compró'. Si entra lo/la, es directo."
  },
  {
    "q": "Ana le dio el libro **a su hermano**. ¿Qué es 'a su hermano'?",
    "ops": [
      "Objeto indirecto",
      "Objeto directo",
      "Sujeto"
    ],
    "m": "'Ana LE dio el libro'. Si entra le/les, es indirecto."
  },
  {
    "q": "Escribí **una carta**. ¿Qué es?",
    "ops": [
      "Objeto directo",
      "Objeto indirecto",
      "Predicado"
    ],
    "m": "'La escribí': entra 'la', así que es directo."
  },
  {
    "q": "Le conté el chiste **a Julia**. ¿Qué es 'a Julia'?",
    "ops": [
      "Objeto indirecto",
      "Objeto directo",
      "Sujeto"
    ],
    "m": "'LE conté el chiste': indirecto."
  },
  {
    "q": "Vi **a Julia** en la plaza. ¿Qué es 'a Julia'?",
    "ops": [
      "Objeto directo",
      "Objeto indirecto",
      "Sujeto"
    ],
    "m": "Trampa clásica: lleva 'a' pero es DIRECTO, porque se dice 'LA vi'. La 'a' aparece cuando el objeto directo es una persona."
  },
  {
    "q": "Regalamos flores **a la maestra**. ¿Qué es?",
    "ops": [
      "Objeto indirecto",
      "Objeto directo",
      "Circunstancial"
    ],
    "m": "'LE regalamos flores': indirecto."
  },
  {
    "q": "El perro mordió **la pelota**. ¿Qué es 'la pelota'?",
    "ops": [
      "Objeto directo",
      "Objeto indirecto",
      "Sujeto"
    ],
    "m": "'LA mordió': directo."
  },
  {
    "q": "Mandé un mensaje **a mis primos**. ¿Qué es?",
    "ops": [
      "Objeto indirecto",
      "Objeto directo",
      "Sujeto"
    ],
    "m": "'LES mandé un mensaje': indirecto."
  },
  {
    "q": "Compré **pan** para la cena. ¿Qué es 'pan'?",
    "ops": [
      "Objeto directo",
      "Objeto indirecto",
      "Circunstancial"
    ],
    "m": "'LO compré': directo."
  },
  {
    "q": "En 'Le presté la bici a Tomás', ¿cuál es el objeto directo?",
    "ops": [
      "la bici",
      "a Tomás",
      "Le"
    ],
    "m": "'La presté': el directo es la bici. 'A Tomás' es el indirecto."
  },
  {
    "q": "¿Con qué pronombres se reemplaza el objeto directo?",
    "ops": [
      "lo, la, los, las",
      "le, les",
      "me, te"
    ],
    "m": "Es la prueba más rápida para distinguirlos."
  },
  {
    "q": "¿Y el objeto indirecto?",
    "ops": [
      "le, les",
      "lo, la",
      "el, la"
    ],
    "m": "Le/les es la marca del indirecto."
  },
  {
    "q": "Explicó **la lección** a los chicos. ¿Qué es 'la lección'?",
    "ops": [
      "Objeto directo",
      "Objeto indirecto",
      "Sujeto"
    ],
    "m": "'LA explicó': directo."
  },
  {
    "q": "Cociné **una torta** para vos. ¿Qué es 'una torta'?",
    "ops": [
      "Objeto directo",
      "Objeto indirecto",
      "Sujeto"
    ],
    "m": "'LA cociné': directo."
  },
  {
    "q": "Pedí un favor **a mi vecina**. ¿Qué es 'a mi vecina'?",
    "ops": [
      "Objeto indirecto",
      "Objeto directo",
      "Circunstancial"
    ],
    "m": "'LE pedí un favor': indirecto."
  },
  {
    "q": "Saludé **a los abuelos**. ¿Qué es?",
    "ops": [
      "Objeto directo",
      "Objeto indirecto",
      "Sujeto"
    ],
    "m": "Otra vez la 'a' con personas: 'LOS saludé', así que es directo."
  },
  {
    "q": "El objeto directo, ¿de qué verbo depende?",
    "ops": [
      "Del verbo principal del predicado",
      "Del sujeto",
      "De ninguno"
    ],
    "m": "Los dos objetos completan al verbo, por eso se llaman complementos."
  },
  {
    "q": "Trajimos **los cuadernos**. ¿Qué es?",
    "ops": [
      "Objeto directo",
      "Objeto indirecto",
      "Sujeto"
    ],
    "m": "'LOS trajimos': directo."
  },
  {
    "q": "Contale la novedad **a tu mamá**. ¿Qué es?",
    "ops": [
      "Objeto indirecto",
      "Objeto directo",
      "Sujeto"
    ],
    "m": "'ContaLE la novedad': indirecto."
  },
  {
    "q": "Rompieron **la ventana**. ¿Qué es?",
    "ops": [
      "Objeto directo",
      "Objeto indirecto",
      "Sujeto"
    ],
    "m": "'LA rompieron': directo."
  }
];
GAMES.od_oi_5 = juegoTriviaTexto(CUR_OD_OI_5_BANCO, "Mirá la parte destacada de la oración.", "od_oi_5");

/* 5° · Grados del adjetivo — grados_adjetivo_5
   DC: Comparativo y superlativo
   Fuente: docs/auditoria-dc-caba/grado-5.md · L5 */
const CUR_GRADOS_ADJETIVO_5_BANCO = [
  {
    "q": "Juan es alto. Pedro es MÁS alto. ¿Qué grado es 'más alto'?",
    "ops": [
      "Comparativo",
      "Superlativo",
      "Positivo"
    ],
    "m": "El comparativo pone dos cosas una al lado de la otra."
  },
  {
    "q": "Pedro es EL MÁS alto de todos. ¿Qué grado es?",
    "ops": [
      "Superlativo",
      "Comparativo",
      "Positivo"
    ],
    "m": "El superlativo lo pone arriba de todo el grupo."
  },
  {
    "q": "El comparativo de 'bueno' es…",
    "ops": [
      "mejor",
      "más bueno",
      "buenísimo"
    ],
    "m": "'Bueno' tiene comparativo propio: mejor. 'Más bueno' suena raro."
  },
  {
    "q": "El comparativo de 'malo' es…",
    "ops": [
      "peor",
      "más malo",
      "malísimo"
    ],
    "m": "Igual que bueno/mejor: malo/peor."
  },
  {
    "q": "El comparativo de 'grande' es…",
    "ops": [
      "mayor",
      "más grandoso",
      "grandote"
    ],
    "m": "Grande tiene mayor, aunque también se usa 'más grande'."
  },
  {
    "q": "El comparativo de 'pequeño' es…",
    "ops": [
      "menor",
      "más pequeñito",
      "pequeñísimo"
    ],
    "m": "Pequeño/menor, como grande/mayor."
  },
  {
    "q": "¿Cuál es el superlativo de 'rápido' con el sufijo -ísimo?",
    "ops": [
      "rapidísimo",
      "más rápido",
      "muy rápido"
    ],
    "m": "El sufijo -ísimo arma el superlativo en una sola palabra."
  },
  {
    "q": "El superlativo de 'fácil' es…",
    "ops": [
      "facilísimo",
      "más fácil",
      "fácilmente"
    ],
    "m": "Se le agrega -ísimo."
  },
  {
    "q": "«Este libro es TAN largo COMO el otro». ¿Qué compara?",
    "ops": [
      "Que son iguales",
      "Que uno es más largo",
      "Que uno es el más largo"
    ],
    "m": "'Tan… como' es el comparativo de igualdad."
  },
  {
    "q": "«Este libro es MENOS largo QUE el otro». ¿Qué compara?",
    "ops": [
      "Que este tiene menos",
      "Que son iguales",
      "Que este es el más largo"
    ],
    "m": "'Menos… que' es el comparativo de inferioridad."
  },
  {
    "q": "El superlativo de 'feliz' es…",
    "ops": [
      "felicísimo",
      "más feliz",
      "felizmente"
    ],
    "m": "Con -ísimo; ojo que la z cambia a c."
  },
  {
    "q": "«Es la casa MÁS linda DEL barrio». ¿Qué grado es?",
    "ops": [
      "Superlativo",
      "Comparativo",
      "Positivo"
    ],
    "m": "'El más… de' señala el tope del grupo: superlativo."
  },
  {
    "q": "«La casa es linda». ¿Qué grado es?",
    "ops": [
      "Positivo",
      "Comparativo",
      "Superlativo"
    ],
    "m": "El grado positivo es el adjetivo solo, sin comparar."
  },
  {
    "q": "El superlativo de 'antiguo' es…",
    "ops": [
      "antiquísimo",
      "más antiguo",
      "antigüedad"
    ],
    "m": "Antiquísimo: la palabra cambia un poco al agregar -ísimo."
  },
  {
    "q": "«Sos MÁS alto QUE yo». ¿Qué tipo de comparativo es?",
    "ops": [
      "De superioridad",
      "De igualdad",
      "De inferioridad"
    ],
    "m": "'Más… que' marca superioridad."
  },
  {
    "q": "El superlativo de 'bueno' con -ísimo es…",
    "ops": [
      "buenísimo",
      "mejorísimo",
      "más bueno"
    ],
    "m": "'Buenísimo' existe; 'mejorísimo' no."
  }
];
GAMES.grados_adjetivo_5 = juegoTriviaTexto(CUR_GRADOS_ADJETIVO_5_BANCO, "¿Cómo se dice?", "grados_adj");

/* 5° · Futuro o condicional — futuro_condicional_5
   DC: Futuro y condicional; perífrasis 'voy a + infinitivo'
   Fuente: docs/auditoria-dc-caba/grado-5.md · L6 */
const CUR_FUTURO_CONDICIONAL_5_BANCO = [
  {
    "q": "Mañana ___ al club.",
    "ops": [
      "iré",
      "iría",
      "iba"
    ],
    "m": "'Mañana' es futuro seguro: iré."
  },
  {
    "q": "Si tuviera tiempo, ___ al club.",
    "ops": [
      "iría",
      "iré",
      "fui"
    ],
    "m": "'Si tuviera' plantea algo hipotético: pide el condicional."
  },
  {
    "q": "El año que viene ___ quinto grado.",
    "ops": [
      "terminaré",
      "terminaría",
      "terminaba"
    ],
    "m": "Hecho futuro concreto: futuro."
  },
  {
    "q": "Yo que vos, ___ con la maestra.",
    "ops": [
      "hablaría",
      "hablaré",
      "hablé"
    ],
    "m": "'Yo que vos' da un consejo: condicional."
  },
  {
    "q": "¿___ pasarme la goma, por favor?",
    "ops": [
      "Podrías",
      "Podrás",
      "Pudiste"
    ],
    "m": "El condicional también sirve para pedir con cortesía. 'Podrás' suena a orden."
  },
  {
    "q": "El sábado ___ el partido.",
    "ops": [
      "jugaremos",
      "jugaríamos",
      "jugábamos"
    ],
    "m": "Fecha concreta a futuro."
  },
  {
    "q": "Me dijo que ___ más tarde.",
    "ops": [
      "llegaría",
      "llegará",
      "llegó"
    ],
    "m": "Es un futuro visto desde el pasado: se usa el condicional."
  },
  {
    "q": "«Voy a estudiar esta tarde» es…",
    "ops": [
      "Una forma de hablar del futuro",
      "Pasado",
      "Condicional"
    ],
    "m": "La perífrasis 'voy a + infinitivo' expresa futuro; se usa muchísimo al hablar."
  },
  {
    "q": "Con esta lluvia, ___ que suspenden el acto.",
    "ops": [
      "diría",
      "diré",
      "dije"
    ],
    "m": "Es una suposición: condicional."
  },
  {
    "q": "En dos horas ___ la película.",
    "ops": [
      "empezará",
      "empezaría",
      "empezaba"
    ],
    "m": "Futuro cierto."
  },
  {
    "q": "¿Cuál es el futuro de 'hacer'?",
    "ops": [
      "haré",
      "haría",
      "hacía"
    ],
    "m": "Hacer es irregular: haré, harás, hará."
  },
  {
    "q": "¿Cuál es el condicional de 'poder'?",
    "ops": [
      "podría",
      "podré",
      "pude"
    ],
    "m": "Podría, podrías, podría."
  },
  {
    "q": "Nos ___ encantado ir, pero no pudimos.",
    "ops": [
      "habría",
      "habrá",
      "hubo"
    ],
    "m": "Habla de algo que no pasó: condicional."
  },
  {
    "q": "¿Cuál es el futuro de 'tener'?",
    "ops": [
      "tendré",
      "tendría",
      "tenía"
    ],
    "m": "Tener es irregular: tendré."
  },
  {
    "q": "Seguro que ya ___ en casa.",
    "ops": [
      "estará",
      "estaría",
      "estuvo"
    ],
    "m": "El futuro también sirve para suponer algo del presente: 'ya estará en casa'."
  },
  {
    "q": "Prometió que ___ el libro.",
    "ops": [
      "devolvería",
      "devolverá",
      "devolvió"
    ],
    "m": "Lo prometió en pasado, así que el futuro de ese momento es condicional."
  },
  {
    "q": "Cuando sea grande ___ veterinaria.",
    "ops": [
      "seré",
      "sería",
      "era"
    ],
    "m": "Plan a futuro: futuro."
  },
  {
    "q": "¿___ un poco de agua? Tengo mucha sed.",
    "ops": [
      "Tendrías",
      "Tendrás",
      "Tuviste"
    ],
    "m": "Pedido cortés: condicional."
  },
  {
    "q": "El lunes ___ los resultados.",
    "ops": [
      "conoceremos",
      "conoceríamos",
      "conocíamos"
    ],
    "m": "Día concreto a futuro."
  },
  {
    "q": "Me ___ quedar, pero tengo que irme.",
    "ops": [
      "gustaría",
      "gustará",
      "gustó"
    ],
    "m": "Deseo que no se cumple: condicional."
  }
];
GAMES.futuro_condicional_5 = juegoTriviaTexto(CUR_FUTURO_CONDICIONAL_5_BANCO, "¿Cuál completa mejor la frase?", "futuro_con");

/* 5° · Vaya, valla o baya — homofonos_5
   DC: Homófonos heterógrafos: ay/hay, casar/cazar, vaya/valla/baya
   Fuente: docs/auditoria-dc-caba/grado-5.md · L7 */
const CUR_HOMOFONOS_5_BANCO = [
  {
    "q": "Ojalá ___ todo bien en la prueba.",
    "ops": [
      "vaya",
      "valla",
      "baya"
    ],
    "m": "'Vaya' es del verbo ir. La 'valla' es una cerca y la 'baya' es un fruto."
  },
  {
    "q": "Saltó la ___ del terreno.",
    "ops": [
      "valla",
      "vaya",
      "baya"
    ],
    "m": "La cerca es 'valla', con doble L."
  },
  {
    "q": "El arándano es una ___ .",
    "ops": [
      "baya",
      "valla",
      "vaya"
    ],
    "m": "La fruta chiquita y carnosa es la 'baya', con B."
  },
  {
    "q": "___ , me golpeé el codo.",
    "ops": [
      "Ay",
      "Hay",
      "Ahí"
    ],
    "m": "El quejido es '¡Ay!'. 'Hay' es del verbo haber y 'ahí' es el lugar."
  },
  {
    "q": "___ tres sillas libres.",
    "ops": [
      "Hay",
      "Ay",
      "Ahí"
    ],
    "m": "Del verbo haber: hay."
  },
  {
    "q": "Dejalo ___ , sobre la mesa.",
    "ops": [
      "ahí",
      "hay",
      "ay"
    ],
    "m": "Indica lugar: ahí, con tilde."
  },
  {
    "q": "Se van a ___ en diciembre.",
    "ops": [
      "casar",
      "cazar",
      "cansar"
    ],
    "m": "Formar pareja es 'casar', con S. 'Cazar' con Z es perseguir animales."
  },
  {
    "q": "Salieron a ___ en el monte.",
    "ops": [
      "cazar",
      "casar",
      "calzar"
    ],
    "m": "Perseguir animales: cazar, con Z."
  },
  {
    "q": "El equipo ___ ganando.",
    "ops": [
      "va",
      "vah",
      "bá"
    ],
    "m": "Del verbo ir: va."
  },
  {
    "q": "Le regaló un ramo de flores muy ___ .",
    "ops": [
      "bellas",
      "vellas",
      "veyas"
    ],
    "m": "'Bellas' es hermosas, con B."
  },
  {
    "q": "El bebé tiene mucho ___ en la cabeza.",
    "ops": [
      "vello",
      "bello",
      "veyo"
    ],
    "m": "El pelito fino es 'vello', con V. 'Bello' con B es hermoso."
  },
  {
    "q": "Es un paisaje muy ___ .",
    "ops": [
      "bello",
      "vello",
      "veyo"
    ],
    "m": "Hermoso es 'bello', con B."
  },
  {
    "q": "Saltó la ___ del jardín.",
    "ops": [
      "valla",
      "vaya",
      "baya"
    ],
    "m": "La valla es la cerca; vaya es del verbo ir; la baya es un fruto."
  },
  {
    "q": "Espero que ___ llegado bien.",
    "ops": [
      "haya",
      "halla",
      "aya"
    ],
    "m": "'Haya' es del verbo haber. 'Halla' es de hallar (encontrar)."
  },
  {
    "q": "El que busca, ___ .",
    "ops": [
      "halla",
      "haya",
      "aya"
    ],
    "m": "De hallar: encontrar."
  },
  {
    "q": "Le dieron un ___ por su trabajo.",
    "ops": [
      "premio",
      "premmio",
      "prehmio"
    ],
    "m": "Premio, con una sola M."
  },
  {
    "q": "Puso los platos ___ la mesa.",
    "ops": [
      "sobre",
      "sobrre",
      "zobre"
    ],
    "m": "Sobre, con B."
  },
  {
    "q": "Ese ___ tiene mucha agua.",
    "ops": [
      "pozo",
      "poso",
      "posso"
    ],
    "m": "El agujero con agua es 'pozo', con Z. 'Poso' es lo que queda en el fondo."
  },
  {
    "q": "Quedó un ___ de café en la taza.",
    "ops": [
      "poso",
      "pozo",
      "posso"
    ],
    "m": "Lo que se deposita abajo es el 'poso', con S."
  },
  {
    "q": "___ tú a saber qué pasó.",
    "ops": [
      "Vaya",
      "Valla",
      "Baya"
    ],
    "m": "Otra vez del verbo ir: vaya."
  },
  {
    "q": "El campo estaba cercado con una ___ de madera.",
    "ops": [
      "valla",
      "vaya",
      "baya"
    ],
    "m": "La cerca: valla."
  },
  {
    "q": "Comimos ___ silvestres en la montaña.",
    "ops": [
      "bayas",
      "vallas",
      "vayas"
    ],
    "m": "Las frutas: bayas."
  }
];
GAMES.homofonos_5 = juegoTriviaTexto(CUR_HOMOFONOS_5_BANCO, "Suenan igual. ¿Cuál va acá?", "homofonos_");

/* 5° · Tilde diacrítica — acentuacion_5
   DC: Acentuación general, tilde diacrítica y adverbios en -mente
   Fuente: docs/auditoria-dc-caba/grado-5.md · L8 */
const CUR_ACENTUACION_5_BANCO = [
  {
    "q": "¿___ hora es?",
    "ops": [
      "Qué",
      "Que",
      "Qué o que, da igual"
    ],
    "m": "En pregunta lleva tilde: qué."
  },
  {
    "q": "Me dijo ___ venía tarde.",
    "ops": [
      "que",
      "qué",
      "qué o que, da igual"
    ],
    "m": "Acá no pregunta ni exclama: va sin tilde."
  },
  {
    "q": "___ es mi hermano.",
    "ops": [
      "Él",
      "El",
      "Èl"
    ],
    "m": "El pronombre (la persona) lleva tilde: él. El artículo (el perro) no."
  },
  {
    "q": "Abrí ___ cajón.",
    "ops": [
      "el",
      "él",
      "èl"
    ],
    "m": "Acá 'el' es artículo, va sin tilde."
  },
  {
    "q": "Ese libro es para ___ .",
    "ops": [
      "mí",
      "mi",
      "mî"
    ],
    "m": "El pronombre lleva tilde: mí."
  },
  {
    "q": "___ mochila es azul.",
    "ops": [
      "Mi",
      "Mí",
      "Mî"
    ],
    "m": "'Mi mochila' es posesivo: sin tilde."
  },
  {
    "q": "Yo no ___ nada de eso.",
    "ops": [
      "sé",
      "se",
      "sê"
    ],
    "m": "Del verbo saber lleva tilde: sé."
  },
  {
    "q": "___ lava las manos antes de comer.",
    "ops": [
      "Se",
      "Sé",
      "Sê"
    ],
    "m": "El pronombre 'se' va sin tilde."
  },
  {
    "q": "¿Querés ___ o café?",
    "ops": [
      "té",
      "te",
      "tê"
    ],
    "m": "La infusión lleva tilde: té."
  },
  {
    "q": "___ espero en la puerta.",
    "ops": [
      "Te",
      "Té",
      "Tê"
    ],
    "m": "El pronombre 'te' no lleva tilde."
  },
  {
    "q": "No sé ___ hacer.",
    "ops": [
      "qué",
      "que",
      "qué o que, da igual"
    ],
    "m": "Es una pregunta indirecta: igual lleva tilde."
  },
  {
    "q": "___ mucho más de lo que parece.",
    "ops": [
      "Sé",
      "Se",
      "Sê"
    ],
    "m": "Del verbo saber: sé."
  },
  {
    "q": "¿___ viene a buscarte?",
    "ops": [
      "Quién",
      "Quien",
      "Quièn"
    ],
    "m": "En pregunta, quién lleva tilde."
  },
  {
    "q": "El chico ___ vino ayer es mi primo.",
    "ops": [
      "que",
      "qué",
      "quê"
    ],
    "m": "No pregunta: sin tilde."
  },
  {
    "q": "¿___ vivís?",
    "ops": [
      "Dónde",
      "Donde",
      "Dônde"
    ],
    "m": "Pregunta: dónde con tilde."
  },
  {
    "q": "La casa ___ vivo es amarilla.",
    "ops": [
      "donde",
      "dónde",
      "dônde"
    ],
    "m": "Sin pregunta: sin tilde."
  },
  {
    "q": "¿___ llegaste tarde?",
    "ops": [
      "Por qué",
      "Porque",
      "Porqué"
    ],
    "m": "Al preguntar va separado y con tilde: por qué."
  },
  {
    "q": "Llegué tarde ___ perdí el colectivo.",
    "ops": [
      "porque",
      "por qué",
      "por que"
    ],
    "m": "Al responder va junto y sin tilde: porque."
  },
  {
    "q": "El adverbio de 'rápida' es…",
    "ops": [
      "rápidamente",
      "rapidamente",
      "rápidamentè"
    ],
    "m": "Los adverbios en -mente conservan la tilde del adjetivo original."
  },
  {
    "q": "El adverbio de 'fácil' es…",
    "ops": [
      "fácilmente",
      "facilmente",
      "fàcilmente"
    ],
    "m": "Fácil lleva tilde, así que fácilmente también."
  },
  {
    "q": "El adverbio de 'lento' es…",
    "ops": [
      "lentamente",
      "léntamente",
      "lentaménte"
    ],
    "m": "'Lento' no lleva tilde, así que lentamente tampoco."
  },
  {
    "q": "'Cántaro' es una palabra…",
    "ops": [
      "Esdrújula",
      "Grave",
      "Aguda"
    ],
    "m": "La fuerza está en la antepenúltima sílaba: CÁN-ta-ro. Todas las esdrújulas llevan tilde."
  },
  {
    "q": "'Ratón' es una palabra…",
    "ops": [
      "Aguda",
      "Grave",
      "Esdrújula"
    ],
    "m": "La fuerza está en la última: ra-TÓN. Lleva tilde por terminar en N."
  },
  {
    "q": "'Árbol' es una palabra…",
    "ops": [
      "Grave",
      "Aguda",
      "Esdrújula"
    ],
    "m": "ÁR-bol: la fuerza en la anteúltima. Lleva tilde porque NO termina en n, s ni vocal."
  }
];
GAMES.acentuacion_5 = juegoTriviaTexto(CUR_ACENTUACION_5_BANCO, "¿Lleva tilde o no?", "acentuacio");

/* 5° · Prefijos poderosos — prefijos_5
   DC: Prefijos in-, des-, micro-, sub-, anti-
   Fuente: docs/auditoria-dc-caba/grado-5.md · L9 */
const CUR_PREFIJOS_5_BANCO = [
  {
    "q": "'Incompleto' significa…",
    "ops": [
      "Que no está completo",
      "Muy completo",
      "Completo de nuevo"
    ],
    "m": "El prefijo in- niega."
  },
  {
    "q": "'Deshacer' significa…",
    "ops": [
      "Hacer al revés",
      "Hacer mucho",
      "Hacer después"
    ],
    "m": "Des- invierte la acción."
  },
  {
    "q": "'Microscopio' sirve para ver cosas…",
    "ops": [
      "Muy chiquitas",
      "Muy lejanas",
      "Muy grandes"
    ],
    "m": "Micro- quiere decir pequeño."
  },
  {
    "q": "'Submarino' significa…",
    "ops": [
      "Debajo del mar",
      "Sobre el mar",
      "Contra el mar"
    ],
    "m": "Sub- es debajo."
  },
  {
    "q": "'Antivirus' es algo que…",
    "ops": [
      "Actúa contra los virus",
      "Ayuda a los virus",
      "Es un virus chiquito"
    ],
    "m": "Anti- es contra."
  },
  {
    "q": "'Injusto' significa…",
    "ops": [
      "Que no es justo",
      "Muy justo",
      "Justo otra vez"
    ],
    "m": "In- niega."
  },
  {
    "q": "'Desarmar' significa…",
    "ops": [
      "Sacar las partes de algo armado",
      "Armar mejor",
      "Armar de nuevo"
    ],
    "m": "Des- deshace la acción de armar."
  },
  {
    "q": "'Subsuelo' es…",
    "ops": [
      "Lo que está debajo del suelo",
      "El suelo de arriba",
      "Un suelo chiquito"
    ],
    "m": "Sub- otra vez: debajo."
  },
  {
    "q": "'Antibiótico' actúa…",
    "ops": [
      "Contra bacterias que enferman",
      "A favor de las bacterias",
      "Debajo de la piel"
    ],
    "m": "Anti- es contra; bio es vida."
  },
  {
    "q": "'Microondas' usa ondas…",
    "ops": [
      "Muy chiquitas",
      "Muy grandes",
      "De agua"
    ],
    "m": "Micro- es pequeño."
  },
  {
    "q": "En 'insecto', ¿el 'in-' es un prefijo que niega?",
    "ops": [
      "No, es parte de la palabra",
      "Sí, significa 'no secto'",
      "Sí, significa 'muy secto'"
    ],
    "m": "Trampa importante: no todo lo que empieza con 'in' lleva prefijo. 'Secto' no existe. Si al sacar el prefijo no queda una palabra real, no era prefijo."
  },
  {
    "q": "En 'destino', ¿el 'des-' es un prefijo?",
    "ops": [
      "No, es parte de la palabra",
      "Sí, es 'no tino'",
      "Sí, es 'tino al revés'"
    ],
    "m": "Misma trampa: 'tino' existe pero destino no significa 'lo contrario de tino'. El prefijo tiene que cambiar el significado de forma previsible."
  },
  {
    "q": "'Desordenado' significa…",
    "ops": [
      "Que no tiene orden",
      "Muy ordenado",
      "Ordenado de nuevo"
    ],
    "m": "Des- niega el orden."
  },
  {
    "q": "'Imposible' significa…",
    "ops": [
      "Que no se puede",
      "Que se puede mucho",
      "Que se puede después"
    ],
    "m": "In- se transforma en im- antes de p: imposible, impaciente."
  },
  {
    "q": "'Subrayar' significa…",
    "ops": [
      "Hacer una raya debajo",
      "Rayar mucho",
      "Rayar contra algo"
    ],
    "m": "Sub- es debajo; rayar es hacer la raya."
  },
  {
    "q": "'Antiaéreo' significa…",
    "ops": [
      "Contra lo que viene por el aire",
      "Que vuela mucho",
      "Debajo del aire"
    ],
    "m": "Anti- es contra."
  },
  {
    "q": "'Incapaz' significa…",
    "ops": [
      "Que no es capaz",
      "Muy capaz",
      "Capaz otra vez"
    ],
    "m": "In- niega."
  },
  {
    "q": "'Descongelar' significa…",
    "ops": [
      "Sacar el congelamiento",
      "Congelar más",
      "Congelar de nuevo"
    ],
    "m": "Des- invierte la acción."
  },
  {
    "q": "'Microbio' es un ser vivo…",
    "ops": [
      "Tan chico que no se ve a simple vista",
      "Enorme",
      "Que vive debajo del agua"
    ],
    "m": "Micro- pequeño, bio vida."
  },
  {
    "q": "En 'independiente', ¿qué niega el prefijo?",
    "ops": [
      "Que dependa de otro",
      "Que sea diente",
      "Que esté debajo"
    ],
    "m": "In- + dependiente: que no depende."
  }
];
GAMES.prefijos_5 = juegoTriviaTexto(CUR_PREFIJOS_5_BANCO, "¿Qué significa la palabra?", "prefijos_5");

/* 5° · Una palabra, varios sentidos — polisemia_5
   DC: Polisemia; la acepción según el contexto
   Fuente: docs/auditoria-dc-caba/grado-5.md · L10 */
const CUR_POLISEMIA_5_BANCO = [
  {
    "q": "«Se lastimó la HOJA del cuchillo». ¿Qué es la hoja?",
    "ops": [
      "La parte que corta",
      "La de un árbol",
      "La del cuaderno"
    ],
    "m": "La misma palabra nombra cosas distintas según el contexto."
  },
  {
    "q": "«Junté una HOJA seca del patio».",
    "ops": [
      "La de un árbol",
      "La que corta",
      "La del libro"
    ],
    "m": "Acá manda 'seca' y 'del patio'."
  },
  {
    "q": "«Me duele la MUÑECA de tanto escribir».",
    "ops": [
      "La articulación del brazo",
      "El juguete",
      "Un adorno"
    ],
    "m": "'Me duele' y 'de escribir' definen el sentido."
  },
  {
    "q": "«Le regalaron una MUÑECA de trapo».",
    "ops": [
      "El juguete",
      "La articulación",
      "Una herramienta"
    ],
    "m": "'De trapo' resuelve la ambigüedad."
  },
  {
    "q": "«El BANCO me cobró comisión».",
    "ops": [
      "La entidad donde está la plata",
      "El asiento de la plaza",
      "Un banco de peces"
    ],
    "m": "'Me cobró comisión' sólo tiene sentido con la entidad."
  },
  {
    "q": "«Nos sentamos en un BANCO de la plaza».",
    "ops": [
      "El asiento",
      "La entidad financiera",
      "Un banco de arena"
    ],
    "m": "'Nos sentamos' define el sentido."
  },
  {
    "q": "«La SIERRA cortó la madera».",
    "ops": [
      "La herramienta",
      "La cadena de montañas",
      "Un tipo de tela"
    ],
    "m": "'Cortó la madera': herramienta."
  },
  {
    "q": "«Fuimos de campamento a la SIERRA».",
    "ops": [
      "La zona de montañas",
      "La herramienta",
      "Un río"
    ],
    "m": "'De campamento a la…': el lugar."
  },
  {
    "q": "«El GATO del auto está en el baúl».",
    "ops": [
      "La herramienta para levantar el auto",
      "El animal",
      "Un juego"
    ],
    "m": "'Del auto' y 'en el baúl' lo definen."
  },
  {
    "q": "«El GATO maulló toda la noche».",
    "ops": [
      "El animal",
      "La herramienta",
      "Un baile"
    ],
    "m": "'Maulló': el animal."
  },
  {
    "q": "«Me puse el saco porque hacía frío».",
    "ops": [
      "La prenda de abrigo",
      "La bolsa grande",
      "Un golpe"
    ],
    "m": "'Me puse' y 'frío': la prenda."
  },
  {
    "q": "«Cargó un SACO de papas».",
    "ops": [
      "La bolsa grande",
      "La prenda",
      "Un mueble"
    ],
    "m": "'De papas': la bolsa."
  },
  {
    "q": "«La PLANTA baja del edificio».",
    "ops": [
      "El piso",
      "El vegetal",
      "La fábrica"
    ],
    "m": "'Del edificio': el piso."
  },
  {
    "q": "«Regué la PLANTA del balcón».",
    "ops": [
      "El vegetal",
      "El piso",
      "La fábrica"
    ],
    "m": "'Regué': el vegetal."
  },
  {
    "q": "«Trabaja en una PLANTA automotriz».",
    "ops": [
      "Una fábrica",
      "El vegetal",
      "El piso de abajo"
    ],
    "m": "Tercera acepción: la fábrica."
  },
  {
    "q": "«Perdió la LLAVE de casa».",
    "ops": [
      "La de abrir la puerta",
      "La del agua",
      "Una llave de lucha"
    ],
    "m": "'De casa': la de la puerta."
  },
  {
    "q": "«Cerrá la LLAVE del agua».",
    "ops": [
      "El grifo",
      "La de la puerta",
      "Una llave inglesa"
    ],
    "m": "'Del agua': la canilla."
  },
  {
    "q": "¿Qué es una palabra polisémica?",
    "ops": [
      "Una que tiene varios significados",
      "Una que suena igual que otra",
      "Una muy larga"
    ],
    "m": "Polisemia: muchos sentidos en UNA misma palabra. Distinto de los homófonos, que se escriben distinto."
  }
];
GAMES.polisemia_5 = juegoTriviaTexto(CUR_POLISEMIA_5_BANCO, "¿Qué significa acá?", "polisemia_");

/* 5° · Arquitecto de textos — estructura_textos_5
   DC: Estructura de la carta y el mail, la entrevista y la noticia
   Fuente: docs/auditoria-dc-caba/grado-5.md · L11 */
const CUR_ESTRUCTURA_TEXTOS_5_BANCO = [
  {
    "items": [
      "Asunto: Pedido de permiso",
      "Estimada directora:",
      "Le escribo para pedirle permiso para la salida.",
      "Saludos cordiales, Martina"
    ]
  },
  {
    "items": [
      "Buenos Aires, 12 de mayo",
      "Querida abuela:",
      "Te cuento que empecé quinto grado.",
      "Te mando un beso, Nico"
    ]
  },
  {
    "items": [
      "Título: Hallaron un fósil en la Patagonia",
      "Bajada: Tiene 70 millones de años",
      "El equipo encontró los restos el martes.",
      "Epígrafe: Los científicos junto al hallazgo"
    ]
  },
  {
    "items": [
      "Presentación del entrevistado",
      "Primera pregunta",
      "Respuesta",
      "Despedida y agradecimiento"
    ]
  },
  {
    "items": [
      "Asunto: Consulta por el taller",
      "Hola, buen día:",
      "Quería saber si quedan lugares.",
      "Muchas gracias, Lucía"
    ]
  },
  {
    "items": [
      "Título de la noticia",
      "Bajada que amplía el título",
      "Cuerpo con los detalles"
    ]
  },
  {
    "items": [
      "Rosario, 3 de agosto",
      "Estimado señor Pérez:",
      "Me dirijo a usted por el aviso del diario.",
      "Atentamente, Ana Gómez"
    ]
  },
  {
    "items": [
      "Se presenta a quién se va a entrevistar",
      "Se hacen las preguntas",
      "Se cierra con un agradecimiento"
    ]
  },
  {
    "items": [
      "Asunto del mail",
      "Saludo inicial",
      "Cuerpo del mensaje",
      "Despedida y firma"
    ]
  },
  {
    "items": [
      "Qué pasó",
      "Dónde pasó",
      "Cuándo pasó",
      "Por qué pasó"
    ]
  },
  {
    "items": [
      "Lugar y fecha",
      "Destinatario",
      "Cuerpo de la carta",
      "Firma"
    ]
  },
  {
    "items": [
      "Encabezado con el nombre del entrevistado",
      "Pregunta sobre su trabajo",
      "Respuesta del entrevistado",
      "Pregunta final",
      "Cierre"
    ]
  }
];
GAMES.estructura_textos_5 = juegoOrdenar(CUR_ESTRUCTURA_TEXTOS_5_BANCO, "Ordená las partes del texto. Tocá en orden.", "Cada tipo de texto tiene sus partes y siempre van en el mismo orden.", "estructura");

/* 5° · Dos puntos y raya — dos_puntos_5
   DC: Dos puntos en el discurso directo; voz del narrador frente al diálogo
   Fuente: docs/auditoria-dc-caba/grado-5.md · L12 */
const CUR_DOS_PUNTOS_5_BANCO = [
  {
    "q": "¿Cuál está bien puntuada?",
    "ops": [
      "Ana dijo: —Ya llego.",
      "Ana dijo —Ya llego.",
      "Ana dijo, —Ya llego."
    ],
    "m": "Los dos puntos anuncian que empieza la voz del personaje; la raya la abre."
  },
  {
    "q": "¿Para qué sirven los dos puntos en el diálogo?",
    "ops": [
      "Anuncian que va a hablar el personaje",
      "Terminan la oración",
      "Separan el sujeto del verbo"
    ],
    "m": "Avisan que lo que viene es textual."
  },
  {
    "q": "¿Qué signo abre lo que dice el personaje?",
    "ops": [
      "La raya de diálogo (—)",
      "El guion corto (-)",
      "El paréntesis"
    ],
    "m": "Es una raya larga, distinta del guion de 'físico-química'."
  },
  {
    "q": "«—¿Venís? —preguntó Juan.» ¿Qué hace la segunda raya?",
    "ops": [
      "Abre la voz del narrador",
      "Cierra la pregunta",
      "Marca una pausa"
    ],
    "m": "Cuando el narrador se mete en el medio, también va con raya."
  },
  {
    "q": "En «—Vamos —dijo ella—, se hace tarde», ¿qué está entre rayas?",
    "ops": [
      "Lo que cuenta el narrador",
      "Lo que dice el personaje",
      "Un pensamiento"
    ],
    "m": "El personaje dice 'Vamos, se hace tarde'; 'dijo ella' es el narrador."
  },
  {
    "q": "¿La raya de diálogo lleva espacio antes de lo que dice el personaje?",
    "ops": [
      "No, va pegada a la palabra",
      "Sí, siempre",
      "Sólo si es pregunta"
    ],
    "m": "—Hola, no — Hola."
  },
  {
    "q": "¿Cuál está bien?",
    "ops": [
      "El maestro anunció: —Mañana hay prueba.",
      "El maestro anunció. —Mañana hay prueba.",
      "El maestro anunció; —Mañana hay prueba."
    ],
    "m": "Después del verbo de decir van dos puntos."
  },
  {
    "q": "Los dos puntos también sirven para…",
    "ops": [
      "Introducir una enumeración",
      "Terminar un párrafo",
      "Separar palabras"
    ],
    "m": "«Traje tres cosas: pan, queso y fruta»."
  },
  {
    "q": "«Compré: manzanas, peras y uvas». ¿Está bien?",
    "ops": [
      "Sí, los dos puntos anuncian la lista",
      "No, va punto y coma",
      "No, va coma"
    ],
    "m": "Anuncian la enumeración que viene."
  },
  {
    "q": "¿Cómo se marca que habla OTRO personaje?",
    "ops": [
      "Se empieza un renglón nuevo con raya",
      "Se usa coma",
      "Se pone entre paréntesis"
    ],
    "m": "Cada intervención va en su renglón: así se sabe quién habla sin que lo aclaren."
  },
  {
    "q": "En «—Tengo hambre —dijo Pedro.», ¿quién dice 'Tengo hambre'?",
    "ops": [
      "Pedro",
      "El narrador",
      "No se sabe"
    ],
    "m": "Lo que va después de la raya inicial es del personaje."
  },
  {
    "q": "¿Cuál NO es una función de los dos puntos?",
    "ops": [
      "Separar el sujeto del predicado",
      "Anunciar un diálogo",
      "Anunciar una enumeración"
    ],
    "m": "Entre sujeto y predicado no va ningún signo."
  },
  {
    "q": "«Estimada directora:» — ¿por qué lleva dos puntos?",
    "ops": [
      "Porque después del saludo de una carta van dos puntos",
      "Porque es una pregunta",
      "Porque hay una lista"
    ],
    "m": "En cartas y mails, el saludo inicial cierra con dos puntos."
  },
  {
    "q": "«—No sé —respondió—. Preguntale a él.» El punto después de la raya, ¿de qué es?",
    "ops": [
      "Cierra lo que dijo el narrador",
      "Cierra la pregunta",
      "Está de más"
    ],
    "m": "El narrador terminó su aclaración y ahí sigue hablando el personaje."
  },
  {
    "q": "¿La raya de diálogo se usa también en la carta?",
    "ops": [
      "No, sólo cuando hay personajes hablando",
      "Sí, siempre",
      "Sólo al final"
    ],
    "m": "La carta tiene una sola voz: la de quien escribe."
  },
  {
    "q": "¿Qué diferencia hay entre la voz del narrador y la del personaje?",
    "ops": [
      "El narrador cuenta; el personaje habla y va con raya",
      "Son lo mismo",
      "El narrador siempre va con raya"
    ],
    "m": "Distinguirlas es lo que hace que se entienda un cuento con diálogos."
  }
];
GAMES.dos_puntos_5 = juegoTriviaTexto(CUR_DOS_PUNTOS_5_BANCO, "¿Cómo se puntúa el diálogo?", "dos_puntos");

/* 5° · ¿Opinión o argumento? — opinion_argumento_5
   DC: Textos argumentativos: notas de opinión y publicidades
   Fuente: docs/auditoria-dc-caba/grado-5.md · L13 */
const CUR_OPINION_ARGUMENTO_5_BANCO = [
  {
    "it": "«La escuela tiene 320 alumnos»",
    "cat": "hecho",
    "m": "Se puede verificar: contás y listo."
  },
  {
    "it": "«La escuela es la mejor del barrio»",
    "cat": "opinion",
    "m": "Es una valoración: alguien puede pensar distinto y no está mintiendo."
  },
  {
    "it": "«La escuela es la mejor del barrio porque tiene la biblioteca más grande»",
    "cat": "argumento",
    "m": "Es una opinión MÁS una razón que la sostiene. Ese 'porque' es la clave."
  },
  {
    "it": "«El recreo dura 20 minutos»",
    "cat": "hecho",
    "m": "Se mide con el reloj."
  },
  {
    "it": "«El recreo es demasiado corto»",
    "cat": "opinion",
    "m": "Valoración."
  },
  {
    "it": "«El recreo debería ser más largo, porque después del almuerzo cuesta concentrarse»",
    "cat": "argumento",
    "m": "Postura + razón."
  },
  {
    "it": "«Ayer llovió 30 milímetros»",
    "cat": "hecho",
    "m": "Dato medible."
  },
  {
    "it": "«Los días de lluvia son horribles»",
    "cat": "opinion",
    "m": "A alguien pueden gustarle."
  },
  {
    "it": "«Conviene salir con paraguas, ya que el pronóstico da 80% de lluvia»",
    "cat": "argumento",
    "m": "Recomienda algo y da el motivo."
  },
  {
    "it": "«Este celular tiene 128 GB de memoria»",
    "cat": "hecho",
    "m": "Dato del producto, verificable."
  },
  {
    "it": "«Este celular es el mejor del mercado»",
    "cat": "opinion",
    "m": "Frase típica de publicidad: suena a dato pero es valoración."
  },
  {
    "it": "«Elegí este celular: es el único con garantía de 3 años»",
    "cat": "argumento",
    "m": "Da una razón concreta y comprobable para la recomendación."
  },
  {
    "it": "«El museo abre de martes a domingo»",
    "cat": "hecho",
    "m": "Se chequea en la cartelera."
  },
  {
    "it": "«El museo es aburrido»",
    "cat": "opinion",
    "m": "Valoración personal."
  },
  {
    "it": "«Vale la pena ir al museo, porque la muestra se va en dos semanas»",
    "cat": "argumento",
    "m": "Recomendación con razón."
  },
  {
    "it": "«El Aconcagua mide 6.960 metros»",
    "cat": "hecho",
    "m": "Dato geográfico."
  },
  {
    "it": "«Hay que cuidar el agua porque es un recurso que no se repone solo»",
    "cat": "argumento",
    "m": "Postura + razón."
  },
  {
    "it": "«El verano es la mejor estación»",
    "cat": "opinion",
    "m": "Gustos."
  },
  {
    "it": "«La biblioteca tiene 4.000 libros»",
    "cat": "hecho",
    "m": "Se cuenta."
  },
  {
    "it": "«Leé más: los que leen entienden mejor las consignas»",
    "cat": "argumento",
    "m": "Consejo sostenido en una razón."
  }
];
GAMES.opinion_argumento_5 = juegoClasificar(CUR_OPINION_ARGUMENTO_5_BANCO, "¿Qué tipo de enunciado es?", [{"cat": "hecho", "label": "📅 Hecho"}, {"cat": "opinion", "label": "💭 Opinión"}, {"cat": "argumento", "label": "🧩 Argumento"}], "opinion_ar");

/* 5° · Traductor romano — romanos_5
   DC: Sistema romano: diferencias con el decimal (posicionalidad, el cero)
   Fuente: docs/auditoria-dc-caba/grado-5.md · M2 */
const CUR_ROMANOS_5_BANCO = [
  {
    "q": "¿Cuánto vale V?",
    "ops": [
      "5",
      "4",
      "10"
    ],
    "m": "Las letras base: I=1, V=5, X=10, L=50, C=100, D=500, M=1000."
  },
  {
    "q": "¿Cuánto vale XV?",
    "ops": [
      "15",
      "5",
      "51"
    ],
    "m": "X (10) + V (5). Cuando la letra menor va DESPUÉS, se suma."
  },
  {
    "q": "¿Cuánto vale IX?",
    "ops": [
      "9",
      "11",
      "10"
    ],
    "m": "La I ADELANTE de la X resta: 10 − 1 = 9. Ésa es la regla sustractiva."
  },
  {
    "q": "¿Cuánto vale XI?",
    "ops": [
      "11",
      "9",
      "10"
    ],
    "m": "Ahora la I va después: se suma. XI = 11, IX = 9. El orden cambia todo."
  },
  {
    "q": "¿Cuánto vale XL?",
    "ops": [
      "40",
      "60",
      "410"
    ],
    "m": "X delante de L resta: 50 − 10 = 40."
  },
  {
    "q": "¿Cuánto vale LX?",
    "ops": [
      "60",
      "40",
      "510"
    ],
    "m": "Ahora se suma: 50 + 10."
  },
  {
    "q": "¿Cuánto vale CM?",
    "ops": [
      "900",
      "1100",
      "100000"
    ],
    "m": "C delante de M resta: 1000 − 100 = 900."
  },
  {
    "q": "¿Cuánto vale MC?",
    "ops": [
      "1100",
      "900",
      "1000100"
    ],
    "m": "Se suma: 1000 + 100."
  },
  {
    "q": "¿Cómo se escribe 14?",
    "ops": [
      "XIV",
      "XIIII",
      "VIX"
    ],
    "m": "10 + 4, y el 4 es IV. No se repite una letra más de tres veces."
  },
  {
    "q": "¿Cómo se escribe 2026?",
    "ops": [
      "MMXXVI",
      "MMXXVV",
      "MXXVI"
    ],
    "m": "1000+1000+10+10+5+1."
  },
  {
    "q": "¿Cuánto vale XXIX?",
    "ops": [
      "29",
      "31",
      "21"
    ],
    "m": "XX (20) + IX (9)."
  },
  {
    "q": "¿Cómo se escribe 90?",
    "ops": [
      "XC",
      "LXXXX",
      "CX"
    ],
    "m": "100 − 10. No se escriben cuatro X seguidas."
  },
  {
    "q": "¿Cuál es la diferencia más grande con nuestro sistema?",
    "ops": [
      "El romano no tiene cero",
      "El romano usa más números",
      "El romano se lee al revés"
    ],
    "m": "No hay símbolo para el cero, y por eso tampoco hay valor posicional: en 'XX' las dos equis valen lo mismo, en '22' los dos doses no."
  },
  {
    "q": "En el número 55, ¿los dos cincos valen lo mismo?",
    "ops": [
      "No: uno vale 50 y el otro 5",
      "Sí, los dos valen 5",
      "Sí, los dos valen 50"
    ],
    "m": "Eso es el valor posicional, y el sistema romano no lo tiene."
  },
  {
    "q": "¿Cuánto vale MMXIV?",
    "ops": [
      "2014",
      "2016",
      "2024"
    ],
    "m": "2000 + 10 + 4."
  },
  {
    "q": "¿Se puede escribir el cero en números romanos?",
    "ops": [
      "No existe símbolo para el cero",
      "Sí, es la O",
      "Sí, es la N"
    ],
    "m": "Es la gran limitación del sistema: sin cero, hacer cuentas escritas es durísimo."
  },
  {
    "q": "¿Cuánto vale XLIV?",
    "ops": [
      "44",
      "56",
      "64"
    ],
    "m": "XL (40) + IV (4)."
  },
  {
    "q": "¿Cómo se escribe 400?",
    "ops": [
      "CD",
      "CCCC",
      "DC"
    ],
    "m": "500 − 100. DC sería 600."
  }
];
GAMES.romanos_5 = juegoTriviaTexto(CUR_ROMANOS_5_BANCO, "¿Cuánto vale?", "romanos_5");

/* 5° · Misiones de varios pasos — problemas_pasos_5
   DC: Problemas de varios pasos con las cuatro operaciones
   Fuente: docs/auditoria-dc-caba/grado-5.md · M3 */
const CUR_PROBLEMAS_PASOS_5_PLANTILLA = {
  "q": "En el club hay {b} grupos de {a} chicos cada uno. Si se van {c}, ¿cuántos quedan?",
  "vars": {
    "a": {
      "rango": [
        6,
        24
      ],
      "paso": 1
    },
    "b": {
      "opciones": [
        3,
        4,
        5,
        6,
        7
      ]
    },
    "c": {
      "rango": [
        2,
        17
      ],
      "paso": 1
    }
  },
  "ok": "a * b - c",
  "distractores": [
    "a * b + c",
    "a * b",
    "a + b - c"
  ],
  "tope": 1000,
  "m": "Son DOS pasos: primero cuántos hay en total ({a} × {b}) y recién después restás los que se van. Da {ok}."
};
GAMES.problemas_pasos_5 = juegoParametrico(CUR_PROBLEMAS_PASOS_5_PLANTILLA, "Resolvé el problema.", "problemas_");

/* 5° · Combinador de conjuntos — combinatoria_5
   DC: Combinatoria; pasaje a la escritura multiplicativa
   Fuente: docs/auditoria-dc-caba/grado-5.md · M4 */
const CUR_COMBINATORIA_5_PLANTILLA = {
  "q": "Tenés {a} remeras y {b} pantalones. ¿Cuántos conjuntos distintos podés armar?",
  "vars": {
    "a": {
      "rango": [
        2,
        9
      ],
      "paso": 1
    },
    "b": {
      "rango": [
        2,
        9
      ],
      "paso": 1
    }
  },
  "ok": "a * b",
  "distractores": [
    "a + b",
    "a * b - a",
    "a * b + b"
  ],
  "tope": 200,
  "m": "Cada remera se puede combinar con TODOS los pantalones, así que se multiplica: {a} × {b} = {ok}. El error típico es sumar."
};
GAMES.combinatoria_5 = juegoParametrico(CUR_COMBINATORIA_5_PLANTILLA, "¿Cuántas combinaciones distintas salen?", "combinator");

/* 5° · La cuenta escondida — cuenta_escondida_5
   DC: Relación c×d+r=D con r<d; análisis del resto
   Fuente: docs/auditoria-dc-caba/grado-5.md · M5 */
const CUR_CUENTA_ESCONDIDA_5_PLANTILLA = {
  "q": "Una división da cociente {c}, divisor {d} y resto {r}. ¿Cuál era el dividendo?",
  "vars": {
    "c": {
      "rango": [
        4,
        60
      ],
      "paso": 1
    },
    "d": {
      "opciones": [
        7,
        8,
        9,
        11,
        12
      ]
    },
    "r": {
      "opciones": [
        1,
        2,
        3,
        4,
        5
      ]
    }
  },
  "ok": "c * d + r",
  "distractores": [
    "c * d",
    "c * d - r",
    "c + d + r"
  ],
  "tope": 1000,
  "m": "La regla es dividendo = cociente × divisor + resto. Sin sumar el resto te falta. Da {ok}."
};
GAMES.cuenta_escondida_5 = juegoParametrico(CUR_CUENTA_ESCONDIDA_5_PLANTILLA, "Reconstruí el dividendo.", "cuenta_esc");

/* 5° · Cazamúltiplos — divisibilidad_5
   DC: Divisibilidad: múltiplos, divisores y descomposición multiplicativa
   Fuente: docs/auditoria-dc-caba/grado-5.md · M6 */
const CUR_DIVISIBILIDAD_5_BANCO = [
  {
    "q": "¿Cuál de estos es múltiplo de 5?",
    "ops": [
      "45",
      "42",
      "48"
    ],
    "m": "Los múltiplos de 5 terminan en 0 o en 5."
  },
  {
    "q": "¿Cuál NO es múltiplo de 2?",
    "ops": [
      "37",
      "36",
      "38"
    ],
    "m": "Los múltiplos de 2 terminan en cifra par."
  },
  {
    "q": "¿Cuál es múltiplo de 10?",
    "ops": [
      "70",
      "75",
      "77"
    ],
    "m": "Terminan en 0."
  },
  {
    "q": "¿Cuál es múltiplo de 3?",
    "ops": [
      "27",
      "26",
      "28"
    ],
    "m": "Sumá sus cifras: 2+7=9, que es múltiplo de 3. Ése es el truco."
  },
  {
    "q": "¿Es 24 múltiplo de 6?",
    "ops": [
      "Sí, porque 6×4=24",
      "No",
      "Sólo si se divide por 2"
    ],
    "m": "Un número es múltiplo de otro si lo contiene una cantidad exacta de veces."
  },
  {
    "q": "¿Cuáles son los divisores de 12?",
    "ops": [
      "1, 2, 3, 4, 6 y 12",
      "1, 2, 3 y 12",
      "2, 4 y 6"
    ],
    "m": "Divisores son los que dividen SIN resto. El 1 y el propio número siempre están."
  },
  {
    "q": "¿Cuántos divisores tiene el 7?",
    "ops": [
      "Dos: 1 y 7",
      "Uno: el 7",
      "Tres: 1, 3 y 7"
    ],
    "m": "Los que tienen sólo dos divisores se llaman primos."
  },
  {
    "q": "¿Cuál es el mayor divisor común de 12 y 18?",
    "ops": [
      "6",
      "12",
      "3"
    ],
    "m": "6 divide a los dos y es el más grande que lo hace."
  },
  {
    "q": "¿El 1 es primo?",
    "ops": [
      "No, tiene un solo divisor",
      "Sí, es el primero",
      "Sí, porque es impar"
    ],
    "m": "Para ser primo hacen falta DOS divisores distintos, y el 1 sólo tiene uno."
  },
  {
    "q": "¿Cuál es múltiplo de 4?",
    "ops": [
      "36",
      "34",
      "38"
    ],
    "m": "4 × 9 = 36."
  },
  {
    "q": "¿Qué número es múltiplo de 2 Y de 3 a la vez?",
    "ops": [
      "18",
      "15",
      "16"
    ],
    "m": "18 es par y sus cifras suman 9. Es múltiplo de 6."
  },
  {
    "q": "24 = 4 × 6. ¿Qué otra descomposición sirve?",
    "ops": [
      "2 × 12",
      "5 × 5",
      "3 × 9"
    ],
    "m": "Un número se puede descomponer de varias formas multiplicativas."
  },
  {
    "q": "¿Es 9 divisor de 45?",
    "ops": [
      "Sí, 45 ÷ 9 = 5 exacto",
      "No",
      "Sólo si se suma 5"
    ],
    "m": "Divide sin dejar resto: es divisor."
  },
  {
    "q": "¿Cuál es el menor múltiplo común de 4 y 6?",
    "ops": [
      "12",
      "24",
      "10"
    ],
    "m": "Los de 4: 4, 8, 12… Los de 6: 6, 12… El primero que comparten es 12."
  },
  {
    "q": "El 0, ¿es múltiplo de 5?",
    "ops": [
      "Sí, porque 5×0=0",
      "No, es demasiado chico",
      "Sólo del 1"
    ],
    "m": "El 0 es múltiplo de todos, porque cualquier número por cero da cero."
  },
  {
    "q": "¿Cuál de estos es múltiplo de 9?",
    "ops": [
      "54",
      "52",
      "56"
    ],
    "m": "5+4=9. El truco de sumar las cifras también sirve para el 9."
  },
  {
    "q": "Si 8 es divisor de 40, entonces 40 es…",
    "ops": [
      "Múltiplo de 8",
      "Divisor de 8",
      "Primo"
    ],
    "m": "Son las dos caras de la misma relación: 8 divide a 40, 40 es múltiplo de 8."
  },
  {
    "q": "¿Cuál tiene MÁS divisores?",
    "ops": [
      "24",
      "23",
      "29"
    ],
    "m": "23 y 29 son primos: sólo dos divisores cada uno. 24 tiene ocho."
  }
];
GAMES.divisibilidad_5 = juegoTriviaTexto(CUR_DIVISIBILIDAD_5_BANCO, "Pensá en múltiplos y divisores.", "divisibili");

/* 5° · Reconstruí el entero — reconstruir_entero_5
   DC: Reconstrucción de la unidad; fracción de un número natural
   Fuente: docs/auditoria-dc-caba/grado-5.md · M9 */
const CUR_RECONSTRUIR_ENTERO_5_PLANTILLA = {
  "q": "Si 1/{d} de una colección son {p} figuritas, ¿cuántas hay en total?",
  "vars": {
    "d": {
      "opciones": [
        2,
        3,
        4,
        5,
        6,
        8,
        10
      ]
    },
    "p": {
      "rango": [
        3,
        40
      ],
      "paso": 1
    }
  },
  "ok": "p * d",
  "distractores": [
    "p + d",
    "p * d - p",
    "p * d + p"
  ],
  "tope": 500,
  "m": "Si {p} es UNA de las {d} partes iguales, el total tiene {d} veces esa parte: {p} × {d} = {ok}. El error típico es sumar en vez de multiplicar."
};
GAMES.reconstruir_entero_5 = juegoParametrico(CUR_RECONSTRUIR_ENTERO_5_PLANTILLA, "Si conocés la parte, ¿cuál es el total?", "reconstrui");

/* 5° · ¿Proporcional o no? — proporcionalidad_5
   DC: Proporcionalidad directa; distinguir lo proporcional de lo que no lo es
   Fuente: docs/auditoria-dc-caba/grado-5.md · M13 */
const CUR_PROPORCIONALIDAD_5_BANCO = [
  {
    "it": "1 kg de pan cuesta $2.000. ¿Cuánto cuestan 3 kg?",
    "cat": "si",
    "m": "El triple de kilos, el triple de precio: es proporcional."
  },
  {
    "it": "Un chico de 8 años mide 1,30 m. ¿Cuánto mide a los 16?",
    "cat": "no",
    "m": "El doble de edad NO da el doble de altura. Crecer no es proporcional."
  },
  {
    "it": "Un auto tarda 2 horas en llegar. ¿Cuánto tardan 2 autos?",
    "cat": "no",
    "m": "Tardan lo mismo: el tiempo no depende de cuántos autos vayan."
  },
  {
    "it": "3 lápices cuestan $900. ¿Cuánto cuestan 6?",
    "cat": "si",
    "m": "El doble de lápices, el doble de precio."
  },
  {
    "it": "Una canilla llena el tanque en 20 min. ¿Y dos canillas iguales?",
    "cat": "no",
    "m": "Tardan la MITAD, no el doble: cuando una crece y la otra baja, no es proporcionalidad directa."
  },
  {
    "it": "Un libro cuesta $8.000. ¿Cuánto cuestan 4 libros?",
    "cat": "si",
    "m": "Cuatro veces más."
  },
  {
    "it": "Con 2 huevos salen 12 panqueques. ¿Con 4 huevos?",
    "cat": "si",
    "m": "El doble de ingredientes, el doble de panqueques."
  },
  {
    "it": "Juan tiene 10 años y su hermana 5. ¿Cuántos tendrá ella cuando él tenga 20?",
    "cat": "no",
    "m": "Tendrá 15, no 10: la diferencia de edad se mantiene, no se duplica."
  },
  {
    "it": "Una remera cuesta $10.000. ¿Cuánto cuestan 3?",
    "cat": "nosesabe",
    "m": "Si hay promo 3×2 no son $30.000. Sin saber si hay descuento por cantidad, no se puede afirmar."
  },
  {
    "it": "1 hora de trabajo se paga $5.000. ¿Y 10 horas?",
    "cat": "nosesabe",
    "m": "Las horas extra suelen pagarse distinto. Con el dato que hay, no alcanza."
  },
  {
    "it": "4 entradas cuestan $12.000. ¿Cuánto cuesta 1?",
    "cat": "si",
    "m": "$3.000 cada una: el valor unitario."
  },
  {
    "it": "Un tren tarda 3 h a 80 km/h. ¿Cuánto tarda a 160 km/h?",
    "cat": "no",
    "m": "Tarda la mitad. Al doble de velocidad, la mitad de tiempo."
  },
  {
    "it": "2 metros de tela cuestan $6.000. ¿Y 5 metros?",
    "cat": "si",
    "m": "$3.000 el metro por 5."
  },
  {
    "it": "Una pizza alcanza para 4 chicos. ¿Cuántas para 12?",
    "cat": "si",
    "m": "El triple de chicos, el triple de pizzas."
  },
  {
    "it": "Con 20 años de edad pesás 60 kg. ¿Cuánto a los 40?",
    "cat": "no",
    "m": "El peso no se duplica con la edad."
  },
  {
    "it": "El taxi cobra $3.000 de bajada de bandera más $500 por km. ¿El doble de km cuesta el doble?",
    "cat": "no",
    "m": "No, porque la bajada de bandera se paga UNA vez. Cuando hay un valor fijo, la relación deja de ser proporcional."
  },
  {
    "it": "Un envío pesa 2 kg y sale $4.000. ¿Cuánto sale uno de 8 kg?",
    "cat": "nosesabe",
    "m": "Muchos envíos cobran por franjas de peso, no por kilo exacto."
  },
  {
    "it": "6 alfajores cuestan $4.800. ¿Cuánto cuestan 3?",
    "cat": "si",
    "m": "La mitad de alfajores, la mitad de precio: $2.400."
  }
];
GAMES.proporcionalidad_5 = juegoClasificar(CUR_PROPORCIONALIDAD_5_BANCO, "¿La relación es proporcional?", [{"cat": "si", "label": "✅ Sí, proporcional"}, {"cat": "no", "label": "❌ No lo es"}, {"cat": "nosesabe", "label": "🤷 No alcanza el dato"}], "proporcion");

/* 5° · Perímetro y baldosas — perimetro_area_5
   DC: Fórmulas de perímetro; área con unidades no convencionales
   Fuente: docs/auditoria-dc-caba/grado-5.md · M15 */
const CUR_PERIMETRO_AREA_5_PLANTILLA = {
  "q": "Un rectángulo mide {a} cm de largo y {b} cm de ancho. ¿Cuál es su perímetro?",
  "vars": {
    "a": {
      "rango": [
        4,
        25
      ],
      "paso": 1
    },
    "b": {
      "rango": [
        2,
        18
      ],
      "paso": 1
    }
  },
  "ok": "2 * (a + b)",
  "distractores": [
    "a * b",
    "a + b",
    "2 * a + b"
  ],
  "tope": 200,
  "m": "El perímetro es el contorno: se recorren los cuatro lados, 2 × ({a} + {b}) = {ok}. Si multiplicaste, calculaste el ÁREA, que es lo que entra adentro."
};
GAMES.perimetro_area_5 = juegoParametrico(CUR_PERIMETRO_AREA_5_PLANTILLA, "¿Cuánto mide el contorno?", "perimetro_");

/* 5° · Encuesta y gráfico — graficos_5
   DC: Tablas de frecuencias; gráficos de barras y circulares
   Fuente: docs/auditoria-dc-caba/grado-5.md · M16 */
const CUR_GRAFICOS_5_BANCO = [
  {
    "q": "En una encuesta: fútbol 12, básquet 7, vóley 5. ¿Cuántos contestaron?",
    "ops": [
      "24",
      "12",
      "19"
    ],
    "m": "Se suman todas las frecuencias: 12+7+5."
  },
  {
    "q": "Con esos datos, ¿cuál es el deporte más elegido?",
    "ops": [
      "Fútbol",
      "Básquet",
      "Vóley"
    ],
    "m": "El de mayor frecuencia."
  },
  {
    "q": "¿Qué es la frecuencia en una tabla?",
    "ops": [
      "Cuántas veces se repite cada respuesta",
      "El total de encuestados",
      "El nombre de la categoría"
    ],
    "m": "Es el conteo de cada opción."
  },
  {
    "q": "En un gráfico de barras, ¿qué representa la altura?",
    "ops": [
      "La frecuencia de esa categoría",
      "El nombre",
      "El total"
    ],
    "m": "Barra más alta, categoría más elegida."
  },
  {
    "q": "Perro 10, gato 10, pez 4. ¿Qué se puede decir?",
    "ops": [
      "Perro y gato empatan",
      "Gana el perro",
      "Gana el pez"
    ],
    "m": "Frecuencias iguales: empate."
  },
  {
    "q": "¿Para qué sirve un gráfico circular (de torta)?",
    "ops": [
      "Para ver qué parte del total es cada categoría",
      "Para ver cómo cambia algo en el tiempo",
      "Para contar de a uno"
    ],
    "m": "La torta muestra partes de un total; las barras comparan cantidades."
  },
  {
    "q": "Si una categoría se lleva la mitad de la torta, ¿qué significa?",
    "ops": [
      "La eligió la mitad de la gente",
      "La eligieron 2 personas",
      "Es la que menos votos tuvo"
    ],
    "m": "Media torta = 50% del total."
  },
  {
    "q": "Verano 15, invierno 5, otoño 5, primavera 5. ¿Cuántos contestaron?",
    "ops": [
      "30",
      "15",
      "20"
    ],
    "m": "15+5+5+5."
  },
  {
    "q": "Con esos datos, ¿qué fracción eligió verano?",
    "ops": [
      "La mitad",
      "Un cuarto",
      "Un tercio"
    ],
    "m": "15 de 30 es la mitad."
  },
  {
    "q": "¿Qué hay que poner SIEMPRE en un gráfico?",
    "ops": [
      "El título y qué mide cada eje",
      "Sólo los colores",
      "El nombre de quien lo hizo"
    ],
    "m": "Sin título ni referencias, el gráfico no se puede interpretar."
  },
  {
    "q": "Un gráfico de barras muestra 8, 6 y 6. ¿Cuál es el total?",
    "ops": [
      "20",
      "8",
      "14"
    ],
    "m": "Se suman todas las barras."
  },
  {
    "q": "Si en la encuesta hay 25 chicos y 10 eligieron pizza, ¿cuántos NO la eligieron?",
    "ops": [
      "15",
      "10",
      "25"
    ],
    "m": "25 − 10."
  },
  {
    "q": "¿Se puede concluir algo de toda la escuela con una encuesta a 5 chicos?",
    "ops": [
      "No, son muy pocos",
      "Sí, siempre",
      "Sí, si son de distintos grados"
    ],
    "m": "Con una muestra muy chica la conclusión no es confiable."
  },
  {
    "q": "En una tabla, ¿qué va en la primera columna?",
    "ops": [
      "Las categorías",
      "Las frecuencias",
      "Los totales"
    ],
    "m": "Primero qué se midió, después cuántos."
  },
  {
    "q": "Chocolate 9, frutilla 6, limón 3. ¿Cuántos MÁS eligieron chocolate que limón?",
    "ops": [
      "6",
      "3",
      "12"
    ],
    "m": "9 − 3 = 6. 'Cuántos más' es una resta, no una suma."
  },
  {
    "q": "¿Cuándo conviene un gráfico de barras y no una torta?",
    "ops": [
      "Cuando querés comparar cantidades entre sí",
      "Cuando hay una sola categoría",
      "Cuando los datos son texto"
    ],
    "m": "Las barras comparan mejor; la torta muestra proporciones del total."
  }
];
GAMES.graficos_5 = juegoTriviaTexto(CUR_GRAFICOS_5_BANCO, "Leé la tabla y decidí.", "graficos_5");

/* 5° · El ciclo del agua — ciclo_agua_5
   DC: Ciclo hidrológico como modelo; los tres estados en los subsistemas
   Fuente: docs/auditoria-dc-caba/grado-5.md · N1 */
const CUR_CICLO_AGUA_5_BANCO = [
  {
    "items": [
      "El sol calienta el agua del mar",
      "El agua se evapora y sube",
      "Arriba se enfría y forma nubes",
      "Cae como lluvia"
    ]
  },
  {
    "items": [
      "Llueve sobre la montaña",
      "El agua baja por el arroyo",
      "El arroyo desemboca en el río",
      "El río llega al mar"
    ]
  },
  {
    "items": [
      "El agua se filtra en la tierra",
      "Queda guardada bajo el suelo",
      "Se saca con una bomba",
      "Llega a la canilla"
    ]
  },
  {
    "items": [
      "Nieva en la cordillera",
      "La nieve se acumula todo el invierno",
      "En primavera se derrite",
      "El deshielo alimenta el río"
    ]
  },
  {
    "items": [
      "El agua del charco se evapora",
      "El vapor sube al aire",
      "Se condensa en gotitas",
      "Se forma la nube"
    ]
  },
  {
    "items": [
      "La planta toma agua por la raíz",
      "El agua sube por el tallo",
      "Sale por las hojas como vapor"
    ]
  },
  {
    "items": [
      "Cae granizo",
      "El granizo se derrite en el suelo",
      "El agua corre hacia el arroyo"
    ]
  },
  {
    "items": [
      "El vapor de la olla toca la tapa fría",
      "Se forman gotas en la tapa",
      "Las gotas caen de nuevo a la olla"
    ]
  },
  {
    "items": [
      "El río deja el agua en el lago",
      "El sol la evapora",
      "Se forma la nube sobre el lago",
      "Vuelve a llover sobre el lago"
    ]
  },
  {
    "items": [
      "Sale el sol sobre el pasto mojado",
      "El rocío se evapora",
      "El aire se lleva el vapor"
    ]
  },
  {
    "items": [
      "El agua de lluvia entra a la alcantarilla",
      "Va por los caños hasta la planta",
      "Se limpia en la planta",
      "Vuelve al río"
    ]
  },
  {
    "items": [
      "El hielo del glaciar se derrite",
      "El agua líquida corre ladera abajo",
      "Se junta en la laguna"
    ]
  }
];
GAMES.ciclo_agua_5 = juegoOrdenar(CUR_CICLO_AGUA_5_BANCO, "Ordená el recorrido del agua. Tocá en orden.", "Seguí el agua: de dónde sale, por dónde pasa y a dónde vuelve.", "ciclo_agua");

/* 5° · Homogénea o heterogénea — mezclas_5
   DC: Mezclas y su clasificación
   Fuente: docs/auditoria-dc-caba/grado-5.md · N2 */
const CUR_MEZCLAS_5_BANCO = [
  {
    "it": "Agua con sal disuelta",
    "cat": "homogenea",
    "m": "La sal sigue ahí, pero no se distinguen los componentes: es homogénea. Que no se vea NO quiere decir que no sea mezcla."
  },
  {
    "it": "Ensalada de lechuga y tomate",
    "cat": "heterogenea",
    "m": "Se ve cada parte por separado."
  },
  {
    "it": "Agua destilada",
    "cat": "nomezcla",
    "m": "Es agua pura, un solo componente: no hay nada mezclado."
  },
  {
    "it": "Agua con aceite",
    "cat": "heterogenea",
    "m": "Se ven las dos capas."
  },
  {
    "it": "Aire",
    "cat": "homogenea",
    "m": "Es una mezcla de gases que no se distinguen a simple vista."
  },
  {
    "it": "Un vaso de agua con arena en el fondo",
    "cat": "heterogenea",
    "m": "Se ve la arena separada."
  },
  {
    "it": "Oro puro de 24 quilates",
    "cat": "nomezcla",
    "m": "Un solo material, sin nada agregado."
  },
  {
    "it": "Café con leche bien revuelto",
    "cat": "homogenea",
    "m": "Queda un solo color parejo."
  },
  {
    "it": "Granola con frutas secas",
    "cat": "heterogenea",
    "m": "Se distingue cada ingrediente."
  },
  {
    "it": "Agua con azúcar disuelta",
    "cat": "homogenea",
    "m": "El azúcar está pero no se ve."
  },
  {
    "it": "Un vaso de agua mineral sin gas",
    "cat": "homogenea",
    "m": "Tiene minerales disueltos: es mezcla, aunque parezca agua sola."
  },
  {
    "it": "Un trozo de hierro",
    "cat": "nomezcla",
    "m": "Un solo material."
  },
  {
    "it": "Sopa de verduras con trozos",
    "cat": "heterogenea",
    "m": "Se ven los pedazos."
  },
  {
    "it": "Vinagre",
    "cat": "homogenea",
    "m": "Es ácido acético disuelto en agua: no se distinguen."
  },
  {
    "it": "Arena de la playa con caracoles",
    "cat": "heterogenea",
    "m": "Se ven los componentes."
  },
  {
    "it": "Un cubito de hielo",
    "cat": "nomezcla",
    "m": "Es agua sólida: un solo material en otro estado."
  },
  {
    "it": "Leche chocolatada",
    "cat": "homogenea",
    "m": "Bien mezclada queda pareja."
  },
  {
    "it": "Gaseosa con burbujas",
    "cat": "heterogenea",
    "m": "Se ven las burbujas de gas separadas del líquido."
  }
];
GAMES.mezclas_5 = juegoClasificar(CUR_MEZCLAS_5_BANCO, "¿Qué tipo de mezcla es?", [{"cat": "homogenea", "label": "🥛 Homogénea"}, {"cat": "heterogenea", "label": "🥗 Heterogénea"}, {"cat": "nomezcla", "label": "🚫 No es mezcla"}], "mezclas_5");

/* 5° · Laboratorio de disolución — disolucion_5
   DC: Modelo de partículas; factores: tamaño, temperatura y agitación
   Fuente: docs/auditoria-dc-caba/grado-5.md · N3 */
const CUR_DISOLUCION_5_BANCO = [
  {
    "q": "Mismo vaso, misma agua: azúcar en polvo o en terrón. ¿Cuál se disuelve antes?",
    "ops": [
      "El polvo",
      "El terrón",
      "Los dos igual"
    ],
    "m": "En polvo hay más superficie en contacto con el agua."
  },
  {
    "q": "Misma azúcar, misma cantidad: agua fría o caliente. ¿Cuál se disuelve antes?",
    "ops": [
      "La caliente",
      "La fría",
      "Igual"
    ],
    "m": "Con más temperatura las partículas se mueven más rápido."
  },
  {
    "q": "Dos vasos iguales: uno se revuelve y el otro no. ¿Cuál se disuelve antes?",
    "ops": [
      "El que se revuelve",
      "El que no",
      "Igual"
    ],
    "m": "Agitar acerca agua nueva al sólido todo el tiempo."
  },
  {
    "q": "Cuando el azúcar se disuelve, ¿qué le pasa?",
    "ops": [
      "Sus partículas se separan y se meten entre las del agua",
      "Desaparece",
      "Se convierte en agua"
    ],
    "m": "Sigue estando: por eso el agua queda dulce y pesa más."
  },
  {
    "q": "Si disolvés 10 g de sal en 100 g de agua, ¿cuánto pesa la mezcla?",
    "ops": [
      "110 g",
      "100 g",
      "10 g"
    ],
    "m": "La materia no se pierde al disolverse."
  },
  {
    "q": "¿Se puede recuperar la sal del agua salada?",
    "ops": [
      "Sí, dejando evaporar el agua",
      "No, ya no existe",
      "Sí, colando con un filtro"
    ],
    "m": "La sal queda; el filtro no sirve porque las partículas son muy chicas."
  },
  {
    "q": "¿Por qué el filtro NO separa el agua salada?",
    "ops": [
      "Porque las partículas de sal son más chicas que los poros",
      "Porque la sal desapareció",
      "Porque el filtro se moja"
    ],
    "m": "Filtrar sirve para mezclas heterogéneas, no para lo disuelto."
  },
  {
    "q": "¿Qué pasa si seguís agregando azúcar a un vaso de agua?",
    "ops": [
      "Llega un punto en que no se disuelve más",
      "Se disuelve infinitamente",
      "El agua se evapora"
    ],
    "m": "Ahí la solución está saturada."
  },
  {
    "q": "Si calentás una solución saturada, ¿se puede disolver más?",
    "ops": [
      "Sí, en general sí",
      "No, nunca",
      "Sólo si la enfriás"
    ],
    "m": "Más temperatura, más capacidad de disolver."
  },
  {
    "q": "El café instantáneo se disuelve más rápido que los granos. ¿Por qué?",
    "ops": [
      "Porque está molido muy fino",
      "Porque es más dulce",
      "Porque tiene más agua"
    ],
    "m": "Otra vez el tamaño: más finito, más superficie."
  },
  {
    "q": "Para comparar si el agua caliente disuelve mejor, ¿qué NO hay que cambiar?",
    "ops": [
      "La cantidad de azúcar y de agua",
      "La temperatura",
      "Nada, se cambia todo"
    ],
    "m": "Ésta es la idea clave: para saber qué causa qué, se cambia UN factor por vez y todo lo demás queda igual."
  },
  {
    "q": "Si un vaso está caliente Y se revuelve, y el otro está frío y quieto, ¿qué se aprende?",
    "ops": [
      "Nada seguro: cambiaron dos cosas a la vez",
      "Que la temperatura es lo que importa",
      "Que revolver es lo que importa"
    ],
    "m": "Con dos factores cambiados no se puede saber cuál fue el responsable."
  },
  {
    "q": "El aceite en agua, ¿se disuelve?",
    "ops": [
      "No, forma dos capas",
      "Sí, si revolvés mucho",
      "Sí, si lo calentás"
    ],
    "m": "No todos los materiales se disuelven en agua."
  },
  {
    "q": "¿Qué es el soluto?",
    "ops": [
      "Lo que se disuelve",
      "El líquido que disuelve",
      "La mezcla entera"
    ],
    "m": "El azúcar es el soluto; el agua, el solvente."
  },
  {
    "q": "¿Y el solvente?",
    "ops": [
      "El que disuelve, casi siempre el agua",
      "Lo que se disuelve",
      "El recipiente"
    ],
    "m": "El agua es el solvente más común: se la llama solvente universal."
  },
  {
    "q": "¿La sal disuelta se ve con lupa?",
    "ops": [
      "No, sus partículas son demasiado chicas",
      "Sí, se ven los granitos",
      "Sí, si el agua está fría"
    ],
    "m": "Por eso la mezcla es homogénea."
  },
  {
    "q": "Si el azúcar se hunde y queda en el fondo sin revolver, ¿está disuelta?",
    "ops": [
      "No, todavía se ve separada",
      "Sí, ya está",
      "Sí, porque tocó el agua"
    ],
    "m": "Mientras se vea el sólido, no está disuelta."
  },
  {
    "q": "¿Por qué el agua fría del mar tiene sal igual?",
    "ops": [
      "Porque la sal se disuelve también en frío, sólo que más lento",
      "Porque el mar no tiene sal en invierno",
      "Porque el frío crea sal"
    ],
    "m": "La temperatura cambia la VELOCIDAD y la cantidad máxima, no el hecho de que se disuelva."
  }
];
GAMES.disolucion_5 = juegoTriviaTexto(CUR_DISOLUCION_5_BANCO, "Antes de probar: ¿qué va a pasar?", "disolucion");

/* 5° · El plato saludable — plato_gapa_5
   DC: Guías alimentarias; etiquetado frontal
   Fuente: docs/auditoria-dc-caba/grado-5.md · N4 */
const CUR_PLATO_GAPA_5_BANCO = [
  {
    "it": "Manzana",
    "cat": "verduras",
    "m": "Fruta: es el grupo más grande del plato."
  },
  {
    "it": "Arroz",
    "cat": "cereales",
    "m": "Cereal."
  },
  {
    "it": "Huevo",
    "cat": "proteinas",
    "m": "Aporta proteínas."
  },
  {
    "it": "Gaseosa",
    "cat": "opcional",
    "m": "Mucha azúcar y ningún nutriente: consumo ocasional."
  },
  {
    "it": "Brócoli",
    "cat": "verduras",
    "m": "Verdura."
  },
  {
    "it": "Lentejas",
    "cat": "cereales",
    "m": "Las legumbres van con los cereales en la guía argentina."
  },
  {
    "it": "Yogur",
    "cat": "proteinas",
    "m": "Lácteo."
  },
  {
    "it": "Alfajor",
    "cat": "opcional",
    "m": "Azúcar y grasas: ocasional."
  },
  {
    "it": "Zanahoria",
    "cat": "verduras",
    "m": "Verdura."
  },
  {
    "it": "Fideos",
    "cat": "cereales",
    "m": "Derivado del trigo."
  },
  {
    "it": "Pollo",
    "cat": "proteinas",
    "m": "Carne."
  },
  {
    "it": "Papas fritas de paquete",
    "cat": "opcional",
    "m": "Mucha sal y grasa."
  },
  {
    "it": "Naranja",
    "cat": "verduras",
    "m": "Fruta."
  },
  {
    "it": "Pan integral",
    "cat": "cereales",
    "m": "Cereal."
  },
  {
    "it": "Queso",
    "cat": "proteinas",
    "m": "Lácteo."
  },
  {
    "it": "Caramelos",
    "cat": "opcional",
    "m": "Azúcar pura."
  },
  {
    "it": "Espinaca",
    "cat": "verduras",
    "m": "Verdura de hoja."
  },
  {
    "it": "Porotos",
    "cat": "cereales",
    "m": "Legumbre."
  },
  {
    "it": "Pescado",
    "cat": "proteinas",
    "m": "Carne."
  },
  {
    "it": "Un sello negro que dice EXCESO EN AZÚCARES",
    "cat": "opcional",
    "m": "El etiquetado frontal avisa de un vistazo: si tiene sellos negros, es de consumo ocasional."
  }
];
GAMES.plato_gapa_5 = juegoClasificar(CUR_PLATO_GAPA_5_BANCO, "¿A qué grupo pertenece?", [{"cat": "verduras", "label": "🥦 Verduras y frutas"}, {"cat": "cereales", "label": "🍞 Cereales y legumbres"}, {"cat": "proteinas", "label": "🥚 Carnes, huevos y lácteos"}, {"cat": "opcional", "label": "🍬 Opcionales, de consumo ocasional"}], "plato_gapa");

/* 5° · Luz y materiales — luz_materiales_5
   DC: Opaco, traslúcido y transparente; propagación rectilínea; reflexión
   Fuente: docs/auditoria-dc-caba/grado-5.md · N6 */
const CUR_LUZ_MATERIALES_5_BANCO = [
  {
    "it": "El vidrio de la ventana",
    "cat": "transparente",
    "m": "Pasa la luz y se ve nítido del otro lado."
  },
  {
    "it": "Una hoja de papel de calcar",
    "cat": "traslucido",
    "m": "Pasa luz pero las formas se ven borrosas."
  },
  {
    "it": "Un ladrillo",
    "cat": "opaco",
    "m": "No pasa nada de luz: hace sombra."
  },
  {
    "it": "El agua limpia de un vaso",
    "cat": "transparente",
    "m": "Se ve a través."
  },
  {
    "it": "Una bolsa de plástico blanca",
    "cat": "traslucido",
    "m": "Se ve el resplandor pero no la forma."
  },
  {
    "it": "Una puerta de madera",
    "cat": "opaco",
    "m": "Bloquea la luz."
  },
  {
    "it": "El celofán transparente",
    "cat": "transparente",
    "m": "Se ve a través, aunque tenga color."
  },
  {
    "it": "Un vidrio esmerilado del baño",
    "cat": "traslucido",
    "m": "Justamente por eso se usa: pasa luz pero no se ve."
  },
  {
    "it": "Una cuchara de metal",
    "cat": "opaco",
    "m": "No pasa luz; además refleja."
  },
  {
    "it": "Un vaso de vidrio limpio",
    "cat": "transparente",
    "m": "Se ve a través."
  },
  {
    "it": "Una tela de gasa fina",
    "cat": "traslucido",
    "m": "Pasa algo de luz, difusa."
  },
  {
    "it": "Tu mano",
    "cat": "opaco",
    "m": "Con una linterna fuerte se ve rojiza, pero no deja ver del otro lado."
  },
  {
    "it": "El aire",
    "cat": "transparente",
    "m": "Por eso vemos a lo lejos."
  },
  {
    "it": "Un vidrio empañado",
    "cat": "traslucido",
    "m": "Las gotitas dispersan la luz."
  },
  {
    "it": "Una piedra",
    "cat": "opaco",
    "m": "No pasa luz."
  },
  {
    "it": "Papel manteca",
    "cat": "traslucido",
    "m": "Pasa luz difusa."
  },
  {
    "it": "Una lámina de aluminio",
    "cat": "opaco",
    "m": "No pasa nada y refleja bastante."
  },
  {
    "it": "Agua con mucho barro",
    "cat": "opaco",
    "m": "El agua sola es transparente, pero con barro deja de serlo: depende de la mezcla, no sólo del material."
  }
];
GAMES.luz_materiales_5 = juegoClasificar(CUR_LUZ_MATERIALES_5_BANCO, "Si le apuntás con una linterna, ¿qué pasa?", [{"cat": "transparente", "label": "🪟 Deja pasar y se ve"}, {"cat": "traslucido", "label": "🌫️ Pasa luz, no se ve bien"}, {"cat": "opaco", "label": "🧱 No pasa nada"}], "luz_materi");

/* 5° · El sonido — sonido_5
   DC: El sonido como vibración; no se propaga en el vacío; volumen, altura y timbre
   Fuente: docs/auditoria-dc-caba/grado-5.md · N7 */
const CUR_SONIDO_5_BANCO = [
  {
    "q": "¿Qué produce el sonido?",
    "ops": [
      "Algo que vibra",
      "Algo que brilla",
      "Algo caliente"
    ],
    "m": "Toda fuente de sonido vibra: la cuerda, el parlante, tus cuerdas vocales."
  },
  {
    "q": "¿Se escucha un sonido en el espacio, donde no hay aire?",
    "ops": [
      "No, el sonido necesita un medio",
      "Sí, más fuerte",
      "Sí, pero más agudo"
    ],
    "m": "El sonido necesita partículas para viajar. En el vacío no hay nada que vibre: por eso las explosiones del espacio en las películas son mentira."
  },
  {
    "q": "¿En cuál viaja MÁS RÁPIDO el sonido?",
    "ops": [
      "En el metal",
      "En el aire",
      "En el vacío"
    ],
    "m": "Cuanto más juntas están las partículas, más rápido se transmite."
  },
  {
    "q": "Si golpeás un tambor más fuerte, ¿qué cambia?",
    "ops": [
      "El volumen",
      "La altura",
      "El timbre"
    ],
    "m": "Más energía, más volumen. Sigue siendo la misma nota."
  },
  {
    "q": "Una cuerda más finita y tensa suena…",
    "ops": [
      "Más aguda",
      "Más grave",
      "Más fuerte"
    ],
    "m": "Vibra más rápido: sonido más agudo."
  },
  {
    "q": "Una cuerda gruesa y floja suena…",
    "ops": [
      "Más grave",
      "Más aguda",
      "Más bajo"
    ],
    "m": "Vibra más lento: más grave."
  },
  {
    "q": "La misma nota en un piano y en una guitarra se distingue por…",
    "ops": [
      "El timbre",
      "El volumen",
      "La altura"
    ],
    "m": "El timbre es el 'color' del sonido: por eso reconocés una voz."
  },
  {
    "q": "¿Qué es el eco?",
    "ops": [
      "El sonido que rebota y vuelve",
      "Un sonido más agudo",
      "Un sonido sin fuente"
    ],
    "m": "El sonido se refleja en una superficie y vuelve con retraso."
  },
  {
    "q": "¿Por qué el trueno se escucha DESPUÉS del relámpago?",
    "ops": [
      "Porque la luz viaja mucho más rápido que el sonido",
      "Porque se producen en momentos distintos",
      "Porque el sonido baja del cielo"
    ],
    "m": "Los dos pasan a la vez; la luz llega casi al instante y el sonido tarda."
  },
  {
    "q": "Si ponés la mano en la garganta mientras hablás, ¿qué sentís?",
    "ops": [
      "Vibración",
      "Calor",
      "Nada"
    ],
    "m": "Son las cuerdas vocales vibrando."
  },
  {
    "q": "¿El sonido viaja bajo el agua?",
    "ops": [
      "Sí, y más rápido que en el aire",
      "No",
      "Sólo si hay burbujas"
    ],
    "m": "Por eso las ballenas se comunican a kilómetros."
  },
  {
    "q": "Un sonido muy fuerte y sostenido, ¿puede dañar el oído?",
    "ops": [
      "Sí, conviene bajar el volumen",
      "No, el oído se acostumbra",
      "Sólo si es agudo"
    ],
    "m": "El daño por volumen alto no se recupera."
  },
  {
    "q": "¿Qué mide la altura de un sonido?",
    "ops": [
      "Si es agudo o grave",
      "Si es fuerte o débil",
      "De qué instrumento viene"
    ],
    "m": "Altura = agudo/grave. No confundir con volumen."
  },
  {
    "q": "Si el parlante deja de vibrar, ¿qué pasa?",
    "ops": [
      "Deja de haber sonido",
      "El sonido sigue un rato",
      "El sonido se hace agudo"
    ],
    "m": "Sin vibración no hay sonido."
  },
  {
    "q": "¿Por qué en una sala vacía se escucha más eco?",
    "ops": [
      "Porque no hay muebles ni cortinas que absorban el sonido",
      "Porque hay más aire",
      "Porque hace más frío"
    ],
    "m": "Las superficies blandas absorben; las duras reflejan."
  },
  {
    "q": "Una flauta y un violín tocando la misma nota, ¿qué comparten?",
    "ops": [
      "La altura",
      "El timbre",
      "Nada"
    ],
    "m": "La misma nota es la misma altura; lo que cambia es el timbre."
  },
  {
    "q": "¿Se puede ver el sonido?",
    "ops": [
      "No, pero se pueden ver sus efectos, como el agua que vibra",
      "Sí, es de color azul",
      "Sí, con una linterna"
    ],
    "m": "Poner arroz sobre un parlante deja ver la vibración."
  },
  {
    "q": "El sonido, ¿es una onda?",
    "ops": [
      "Sí, una onda que viaja por el medio",
      "No, es una partícula",
      "Sí, pero sólo en el agua"
    ],
    "m": "Viaja como onda, empujando las partículas del medio."
  }
];
GAMES.sonido_5 = juegoTriviaTexto(CUR_SONIDO_5_BANCO, "Pensá cómo viaja el sonido.", "sonido_5");

/* 5° · ¿Causa interna o externa? — causas_revolucion_5
   DC: Crisis del orden colonial: circunstancias internas y externas; multicausalidad
   Fuente: docs/auditoria-dc-caba/grado-5.md · S2 */
const CUR_CAUSAS_REVOLUCION_5_BANCO = [
  {
    "it": "Napoleón invade España y toma prisionero al rey Fernando VII",
    "cat": "externa",
    "m": "Pasó en Europa y dejó al virreinato sin rey a quien obedecer."
  },
  {
    "it": "Los criollos no podían ocupar los cargos más altos",
    "cat": "interna",
    "m": "Un malestar de acá, acumulado durante años."
  },
  {
    "it": "Las Invasiones Inglesas de 1806 y 1807",
    "cat": "interna",
    "m": "Pasaron acá y dejaron algo decisivo: milicias criollas armadas y la certeza de que se podían defender solos."
  },
  {
    "it": "La Revolución Francesa de 1789",
    "cat": "antecedente",
    "m": "Difundió ideas de libertad e igualdad, pero pasó veinte años antes y lejos: preparó el clima, no desató la Revolución."
  },
  {
    "it": "El monopolio comercial con España molestaba a los comerciantes locales",
    "cat": "interna",
    "m": "Sólo se podía comerciar con España, y acá querían comerciar con todos."
  },
  {
    "it": "La independencia de Estados Unidos en 1776",
    "cat": "antecedente",
    "m": "Mostró que una colonia podía independizarse, pero no fue la causa directa de lo que pasó acá."
  },
  {
    "it": "La Junta de Sevilla, que gobernaba en nombre del rey, cae en 1810",
    "cat": "externa",
    "m": "Ésta es la noticia que llega en mayo de 1810 y precipita todo."
  },
  {
    "it": "El virrey Cisneros no había sido elegido por los vecinos de Buenos Aires",
    "cat": "interna",
    "m": "Sin rey, se discutía de dónde venía su autoridad."
  },
  {
    "it": "Los criollos habían ganado prestigio militar defendiendo la ciudad",
    "cat": "interna",
    "m": "Consecuencia directa de las Invasiones Inglesas."
  },
  {
    "it": "Las ideas de la Ilustración sobre el origen del poder",
    "cat": "antecedente",
    "m": "Dieron argumentos a los que discutían en el Cabildo, pero circulaban desde mucho antes."
  },
  {
    "it": "España queda ocupada por tropas francesas",
    "cat": "externa",
    "m": "El vacío de poder en España es lo que abre la puerta."
  },
  {
    "it": "Buenos Aires había crecido como puerto y quería decidir su comercio",
    "cat": "interna",
    "m": "Intereses económicos locales."
  },
  {
    "it": "Inglaterra necesitaba mercados nuevos para vender sus productos",
    "cat": "externa",
    "m": "Presión desde afuera a favor de abrir el comercio."
  },
  {
    "it": "La creación del Virreinato del Río de la Plata en 1776",
    "cat": "antecedente",
    "m": "Le dio importancia a Buenos Aires y preparó el terreno, pero fue 34 años antes."
  },
  {
    "it": "El descontento por los impuestos que se pagaban a España",
    "cat": "interna",
    "m": "Malestar económico local."
  },
  {
    "it": "El rey de España ya no podía gobernar sus colonias",
    "cat": "externa",
    "m": "Sin rey efectivo, la pregunta era quién manda acá."
  }
];
GAMES.causas_revolucion_5 = juegoClasificar(CUR_CAUSAS_REVOLUCION_5_BANCO, "Para la Revolución de Mayo, ¿qué tipo de causa es?", [{"cat": "interna", "label": "🏠 Interna"}, {"cat": "externa", "label": "🌎 Externa"}, {"cat": "antecedente", "label": "🕰️ Antecedente, no causa directa"}], "causas_rev");

/* 5° · El debate de Mayo — debate_mayo_5
   DC: El debate entre Moreno y Saavedra
   Fuente: docs/auditoria-dc-caba/grado-5.md · S3 */
const CUR_DEBATE_MAYO_5_BANCO = [
  {
    "it": "Quería cambios profundos y rápidos",
    "cat": "moreno",
    "m": "Moreno empujaba por transformar en poco tiempo."
  },
  {
    "it": "Prefería avanzar con prudencia, sin apurar",
    "cat": "saavedra",
    "m": "Saavedra temía que ir muy rápido rompiera todo."
  },
  {
    "it": "Estaba a favor de la Primera Junta",
    "cat": "ambos",
    "m": "Los dos formaron parte de la Junta: discutían el CÓMO, no si había que hacerlo."
  },
  {
    "it": "Escribía en La Gazeta para difundir las ideas de la Revolución",
    "cat": "moreno",
    "m": "Moreno fundó el primer periódico oficial."
  },
  {
    "it": "Era militar y jefe del regimiento de Patricios",
    "cat": "saavedra",
    "m": "Su prestigio venía de las Invasiones Inglesas."
  },
  {
    "it": "Quería que el gobierno quedara en manos de los criollos y no del virrey",
    "cat": "ambos",
    "m": "En esto no había discusión entre ellos."
  },
  {
    "it": "Impulsó el Plan de Operaciones, con medidas duras contra los opositores",
    "cat": "moreno",
    "m": "Su postura era la más radical."
  },
  {
    "it": "Apoyaba incorporar a los diputados del interior a la Junta",
    "cat": "saavedra",
    "m": "Ésa fue la diferencia concreta que terminó de separarlos: la Junta Grande."
  },
  {
    "it": "Participó de los sucesos de la Semana de Mayo de 1810",
    "cat": "ambos",
    "m": "Los dos estuvieron ahí."
  },
  {
    "it": "Fue secretario de la Primera Junta",
    "cat": "moreno",
    "m": "Moreno fue secretario; Saavedra, presidente."
  },
  {
    "it": "Fue presidente de la Primera Junta",
    "cat": "saavedra",
    "m": "Saavedra la presidió."
  },
  {
    "it": "Quería terminar con el monopolio comercial español",
    "cat": "ambos",
    "m": "Abrir el comercio era un punto compartido."
  },
  {
    "it": "Murió en alta mar camino a Inglaterra, en 1811",
    "cat": "moreno",
    "m": "Se lo envió en misión diplomática y murió durante el viaje."
  },
  {
    "it": "Pensaba que el interior tenía que tener voz en el gobierno",
    "cat": "saavedra",
    "m": "Buenos Aires sola o con las provincias: ése era el fondo del debate."
  },
  {
    "it": "Defendía que el poder ya no venía del rey sino del pueblo",
    "cat": "ambos",
    "m": "Es la idea que sostiene toda la Revolución; discrepaban en cómo aplicarla."
  }
];
GAMES.debate_mayo_5 = juegoClasificar(CUR_DEBATE_MAYO_5_BANCO, "¿De quién era esta postura?", [{"cat": "moreno", "label": "📜 Moreno"}, {"cat": "saavedra", "label": "🎖️ Saavedra"}, {"cat": "ambos", "label": "🤝 Coincidían los dos"}], "debate_may");

/* 5° · La Asamblea del año XIII — asamblea_xiii_5
   DC: Asamblea del año XIII: libertad de vientres, moneda y símbolos
   Fuente: docs/auditoria-dc-caba/grado-5.md · S4 */
const CUR_ASAMBLEA_XIII_5_BANCO = [
  {
    "q": "¿En qué año se reunió la Asamblea del Año XIII?",
    "ops": [
      "1813",
      "1810",
      "1816"
    ],
    "m": "Por eso se la llama 'del año XIII'."
  },
  {
    "q": "¿Qué fue la libertad de vientres?",
    "ops": [
      "Los hijos de esclavas nacían libres",
      "Se liberó a todas las personas esclavizadas",
      "Se prohibió trabajar de noche"
    ],
    "m": "Importante: NO abolió la esclavitud. Los que ya eran esclavos seguían siéndolo; sólo los que nacían desde entonces eran libres."
  },
  {
    "q": "¿La Asamblea abolió la esclavitud?",
    "ops": [
      "No, sólo liberó a los que nacían desde 1813",
      "Sí, a todos",
      "No hizo nada al respecto"
    ],
    "m": "La abolición completa llegó recién décadas después."
  },
  {
    "q": "¿Qué símbolo patrio aprobó la Asamblea?",
    "ops": [
      "El Himno Nacional",
      "La escarapela",
      "El Cabildo"
    ],
    "m": "Aprobó el Himno y mandó acuñar la primera moneda patria."
  },
  {
    "q": "¿Qué tenía de nuevo la primera moneda patria?",
    "ops": [
      "No llevaba la cara del rey de España",
      "Era de papel",
      "Valía más que la española"
    ],
    "m": "Llevaba el escudo: era una declaración de que ya no se dependía del rey."
  },
  {
    "q": "¿Qué otro símbolo se aprobó en esa época?",
    "ops": [
      "El Escudo Nacional",
      "La bandera de Belgrano en 1812",
      "El Cabildo abierto"
    ],
    "m": "La bandera es de 1812, un año antes; el escudo sale de la Asamblea."
  },
  {
    "q": "¿Qué eliminó la Asamblea sobre los pueblos originarios?",
    "ops": [
      "El tributo, la mita y la encomienda",
      "Sus tierras",
      "Su idioma"
    ],
    "m": "Eliminó las obligaciones de trabajo forzado heredadas de la colonia."
  },
  {
    "q": "¿Qué pasó con los títulos de nobleza?",
    "ops": [
      "Se eliminaron",
      "Se mantuvieron",
      "Se crearon nuevos"
    ],
    "m": "Se buscaba una sociedad sin privilegios de nacimiento."
  },
  {
    "q": "¿La Asamblea declaró la independencia?",
    "ops": [
      "No, eso pasó en 1816 en Tucumán",
      "Sí, en 1813",
      "Sí, pero en secreto"
    ],
    "m": "Es una confusión muy común: la Asamblea tomó muchas medidas pero no declaró la independencia."
  },
  {
    "q": "¿Qué instrumento de tortura prohibió la Asamblea?",
    "ops": [
      "Los instrumentos de tortura en los juicios",
      "Las armas de fuego",
      "Los látigos del campo"
    ],
    "m": "Mandó quemarlos en la plaza pública."
  },
  {
    "q": "¿Quién compuso la música del Himno?",
    "ops": [
      "Blas Parera",
      "Vicente López y Planes",
      "Juan Bautista Alberdi"
    ],
    "m": "La letra es de Vicente López y Planes; la música, de Blas Parera."
  },
  {
    "q": "¿Por qué se dice que la Asamblea fue 'soberana'?",
    "ops": [
      "Porque decidía sin depender del rey de España",
      "Porque la presidía un rey",
      "Porque era secreta"
    ],
    "m": "Soberanía es decidir por sí misma."
  },
  {
    "q": "¿Qué buscaba la Asamblea al crear símbolos propios?",
    "ops": [
      "Mostrar que se estaba formando un país nuevo",
      "Copiar a España",
      "Vender más monedas"
    ],
    "m": "Los símbolos construyen identidad."
  },
  {
    "q": "La libertad de vientres, ¿alcanzó para terminar con la esclavitud?",
    "ops": [
      "No, fue un paso pero quedó incompleto",
      "Sí, de inmediato",
      "No cambió nada"
    ],
    "m": "Fue un avance real y, al mismo tiempo, insuficiente: las dos cosas son ciertas."
  },
  {
    "q": "¿Dónde funcionó la Asamblea?",
    "ops": [
      "En Buenos Aires",
      "En Tucumán",
      "En Córdoba"
    ],
    "m": "En Buenos Aires; el Congreso de 1816 sí fue en Tucumán."
  }
];
GAMES.asamblea_xiii_5 = juegoTriviaTexto(CUR_ASAMBLEA_XIII_5_BANCO, "¿Qué decidió la Asamblea?", "asamblea_x");

/* 5° · Próceres y gestas — proceres_5
   DC: Gesta sanmartiniana; Belgrano; Güemes
   Fuente: docs/auditoria-dc-caba/grado-5.md · S5 */
const CUR_PROCERES_5_BANCO = [
  {
    "q": "Antes de ser militar, Belgrano se había recibido de…",
    "ops": [
      "Abogado",
      "Médico",
      "Ingeniero"
    ],
    "m": "Estudió leyes en España; lo de militar vino después y por necesidad."
  },
  {
    "q": "¿Qué cargo económico tuvo Belgrano antes de 1810?",
    "ops": [
      "Secretario del Consulado de Comercio",
      "Virrey",
      "Jefe de la aduana"
    ],
    "m": "Desde ahí impulsó la agricultura, las escuelas y el comercio."
  },
  {
    "q": "¿Qué hizo Belgrano con el dinero del premio que le dieron por sus victorias?",
    "ops": [
      "Lo donó para construir cuatro escuelas",
      "Compró tierras",
      "Lo repartió entre sus soldados"
    ],
    "m": "Donó los 40.000 pesos para escuelas."
  },
  {
    "q": "¿Qué fue el Éxodo Jujeño?",
    "ops": [
      "La población se fue y quemó todo para no dejarle nada al enemigo",
      "Una fiesta popular",
      "Una migración por el hambre"
    ],
    "m": "Belgrano ordenó la retirada; la gente se llevó o destruyó todo."
  },
  {
    "q": "¿Qué hizo Güemes en el norte?",
    "ops": [
      "Frenó a los realistas con la guerra de guerrillas",
      "Cruzó los Andes",
      "Firmó la independencia"
    ],
    "m": "Con los gauchos salteños contuvo las invasiones desde el norte y protegió la retaguardia de San Martín."
  },
  {
    "q": "¿Por qué la guerra de Güemes se llama 'guerra gaucha'?",
    "ops": [
      "Porque la hacían gauchos con tácticas de emboscada",
      "Porque se peleaba en la ciudad",
      "Porque no hubo combates"
    ],
    "m": "Conocían el terreno y atacaban por sorpresa."
  },
  {
    "q": "¿Para qué cruzó San Martín los Andes?",
    "ops": [
      "Para liberar Chile y desde ahí atacar Perú por mar",
      "Para conquistar Chile",
      "Para huir del enemigo"
    ],
    "m": "Era un plan estratégico: Perú era el centro del poder realista y por tierra era inalcanzable."
  },
  {
    "q": "¿Quién ayudó a organizar el cruce desde Cuyo?",
    "ops": [
      "Todo el pueblo cuyano y Remedios de Escalada con las damas mendocinas",
      "Sólo el ejército",
      "Los ingleses"
    ],
    "m": "Las mujeres de Mendoza cosieron las banderas y aportaron sus joyas."
  },
  {
    "q": "¿Qué fue el Combate de San Lorenzo?",
    "ops": [
      "El bautismo de fuego de los Granaderos",
      "Una batalla naval",
      "El cruce de los Andes"
    ],
    "m": "Ahí San Martín estrenó el regimiento que había creado."
  },
  {
    "q": "¿Quién creó la bandera y en qué año?",
    "ops": [
      "Belgrano, en 1812",
      "San Martín, en 1816",
      "Güemes, en 1810"
    ],
    "m": "La enarboló a orillas del Paraná, en Rosario."
  },
  {
    "q": "¿Qué batallas ganó Belgrano en el norte?",
    "ops": [
      "Tucumán y Salta",
      "Chacabuco y Maipú",
      "San Lorenzo"
    ],
    "m": "Chacabuco y Maipú son de San Martín, en Chile."
  },
  {
    "q": "¿Belgrano quería ser militar?",
    "ops": [
      "No, aceptó el mando porque hacía falta",
      "Sí, desde chico",
      "Sí, se formó como militar en España"
    ],
    "m": "Era abogado y economista; asumió el mando sin formación militar."
  },
  {
    "q": "¿Cómo murió Belgrano?",
    "ops": [
      "Enfermo y pobre, en 1820",
      "En combate",
      "En el exilio"
    ],
    "m": "Murió el 20 de junio de 1820, en la mayor pobreza."
  },
  {
    "q": "¿Dónde pasó San Martín sus últimos años?",
    "ops": [
      "En Francia",
      "En Chile",
      "En Perú"
    ],
    "m": "Se fue a Europa y murió en Boulogne-sur-Mer en 1850."
  },
  {
    "q": "¿Qué tenían en común Belgrano, San Martín y Güemes?",
    "ops": [
      "Los tres pusieron su propio patrimonio al servicio de la causa",
      "Los tres eran militares de carrera",
      "Los tres nacieron en Buenos Aires"
    ],
    "m": "Belgrano era abogado y Güemes nació en Salta: lo que compartieron fue el compromiso, no el origen ni la profesión."
  },
  {
    "q": "¿Por qué era importante el norte que defendía Güemes?",
    "ops": [
      "Era la puerta de entrada de los ejércitos realistas",
      "Tenía las minas de oro",
      "Era la capital"
    ],
    "m": "Si caía el norte, quedaba abierto el camino a Buenos Aires."
  }
];
GAMES.proceres_5 = juegoTriviaTexto(CUR_PROCERES_5_BANCO, "¿Quién fue y qué hizo?", "proceres_5");

/* 5° · El mapa de América — mapa_america_5
   DC: Mapa político de América; subcontinentes, límites y escalas
   Fuente: docs/auditoria-dc-caba/grado-5.md · S7 */
const CUR_MAPA_AMERICA_5_BANCO = [
  {
    "q": "¿En qué subcontinente está la Argentina?",
    "ops": [
      "América del Sur",
      "América Central",
      "América del Norte"
    ],
    "m": "América se divide en del Norte, Central y del Sur."
  },
  {
    "q": "¿Cuántos países limitan con la Argentina?",
    "ops": [
      "Cinco",
      "Tres",
      "Siete"
    ],
    "m": "Chile, Bolivia, Paraguay, Brasil y Uruguay."
  },
  {
    "q": "¿Con qué país tiene la Argentina el límite más largo?",
    "ops": [
      "Chile",
      "Brasil",
      "Bolivia"
    ],
    "m": "Toda la cordillera de los Andes es el límite con Chile."
  },
  {
    "q": "¿Qué cordillera recorre el oeste de América del Sur?",
    "ops": [
      "Los Andes",
      "Los Alpes",
      "Las Rocosas"
    ],
    "m": "Los Andes van desde Venezuela hasta Tierra del Fuego."
  },
  {
    "q": "¿En qué subcontinente está México?",
    "ops": [
      "América del Norte",
      "América Central",
      "América del Sur"
    ],
    "m": "México está en América del Norte, junto con Estados Unidos y Canadá."
  },
  {
    "q": "¿Cuál de estos está en América Central?",
    "ops": [
      "Costa Rica",
      "Ecuador",
      "Paraguay"
    ],
    "m": "América Central es la franja angosta entre México y Colombia."
  },
  {
    "q": "¿Qué océano baña la costa argentina?",
    "ops": [
      "El Atlántico",
      "El Pacífico",
      "El Índico"
    ],
    "m": "El Pacífico baña la costa chilena, del otro lado de los Andes."
  },
  {
    "q": "¿Qué país sudamericano NO tiene salida al mar, además de Bolivia?",
    "ops": [
      "Paraguay",
      "Perú",
      "Uruguay"
    ],
    "m": "Bolivia y Paraguay son los dos países mediterráneos de Sudamérica."
  },
  {
    "q": "¿Para qué sirve la escala de un mapa?",
    "ops": [
      "Para saber a cuánto equivale en la realidad cada centímetro del mapa",
      "Para saber los colores",
      "Para ubicar el norte"
    ],
    "m": "Sin escala no se puede calcular una distancia real."
  },
  {
    "q": "Si la escala dice 1:1.000.000, ¿qué significa?",
    "ops": [
      "1 cm del mapa es 1.000.000 cm reales (10 km)",
      "El mapa mide un millón de cm",
      "Hay un millón de ciudades"
    ],
    "m": "Se lee 'uno en un millón'."
  },
  {
    "q": "¿Qué muestran las referencias de un mapa?",
    "ops": [
      "Qué significa cada color y cada símbolo",
      "La fecha",
      "El nombre del autor"
    ],
    "m": "Sin referencias el mapa no se puede leer."
  },
  {
    "q": "¿Cuál es el país más extenso de América del Sur?",
    "ops": [
      "Brasil",
      "Argentina",
      "Perú"
    ],
    "m": "Brasil es el más grande; la Argentina es el segundo."
  },
  {
    "q": "¿Qué diferencia hay entre un mapa político y uno físico?",
    "ops": [
      "El político muestra países; el físico, el relieve",
      "Son lo mismo",
      "El político es más grande"
    ],
    "m": "Uno muestra fronteras, el otro montañas y ríos."
  },
  {
    "q": "¿Qué país limita con la Argentina sólo al noreste?",
    "ops": [
      "Brasil",
      "Chile",
      "Bolivia"
    ],
    "m": "Brasil limita con Misiones y Corrientes."
  },
  {
    "q": "¿Cuál es la capital de Uruguay?",
    "ops": [
      "Montevideo",
      "Asunción",
      "Santiago"
    ],
    "m": "Asunción es de Paraguay y Santiago de Chile."
  },
  {
    "q": "¿Qué río forma buena parte del límite con Uruguay?",
    "ops": [
      "El río Uruguay",
      "El Paraná",
      "El Colorado"
    ],
    "m": "Por eso el país se llama así."
  },
  {
    "q": "¿Dónde está el punto más alto de América?",
    "ops": [
      "En la Argentina: el Aconcagua",
      "En Brasil",
      "En México"
    ],
    "m": "El Aconcagua, en Mendoza, con casi 6.961 metros."
  },
  {
    "q": "En un planisferio, ¿hacia dónde queda el sur?",
    "ops": [
      "Abajo, según la convención más usada",
      "Arriba",
      "A la derecha"
    ],
    "m": "Es una convención: hay mapas invertidos, y no están mal."
  },
  {
    "q": "¿Cuántos países tiene América del Sur?",
    "ops": [
      "Doce países independientes",
      "Cinco",
      "Veinte"
    ],
    "m": "Doce, más la Guayana Francesa que es territorio de Francia."
  },
  {
    "q": "¿Qué es un límite natural?",
    "ops": [
      "Un río o una montaña que separa dos países",
      "Una línea recta trazada",
      "Un muro"
    ],
    "m": "Los Andes con Chile y el río Uruguay son límites naturales."
  }
];
GAMES.mapa_america_5 = juegoTriviaTexto(CUR_MAPA_AMERICA_5_BANCO, "Ubicate en el mapa.", "mapa_ameri");

/* 5° · La caja de la variable — variables_5
   DC: Variables: declaración, asignación, contar y sumar
   Fuente: docs/auditoria-dc-caba/grado-5.md · T1 */
const CUR_VARIABLES_5_BANCO = [
  {
    "q": "La caja PUNTOS está vacía. Usás el bloque «guardar 5 en PUNTOS». ¿Qué tiene?",
    "ops": [
      "5",
      "0",
      "Nada"
    ],
    "m": "Guardar pone un valor adentro de la caja."
  },
  {
    "q": "PUNTOS tiene 5. Usás «sumar 3 a PUNTOS». ¿Qué tiene ahora?",
    "ops": [
      "8",
      "3",
      "5"
    ],
    "m": "Sumar cambia lo que había: 5 + 3."
  },
  {
    "q": "PUNTOS tiene 8. Usás «guardar 2 en PUNTOS». ¿Qué tiene?",
    "ops": [
      "2",
      "10",
      "8"
    ],
    "m": "Guardar PISA lo que había. Sumar acumula; guardar reemplaza."
  },
  {
    "q": "VIDAS tiene 3. Usás «restar 1 a VIDAS» dos veces. ¿Qué tiene?",
    "ops": [
      "1",
      "2",
      "3"
    ],
    "m": "3 − 1 − 1."
  },
  {
    "q": "¿Para qué sirve una variable?",
    "ops": [
      "Para guardar un dato y usarlo después",
      "Para dibujar",
      "Para borrar el programa"
    ],
    "m": "Es una caja con nombre donde el programa deja algo."
  },
  {
    "q": "MONEDAS tiene 0. Repetís 4 veces «sumar 2 a MONEDAS». ¿Qué tiene?",
    "ops": [
      "8",
      "2",
      "4"
    ],
    "m": "Se suma 2 cuatro veces: 0+2+2+2+2."
  },
  {
    "q": "Tenés dos cajas: A con 5 y B con 9. Hacés «guardar A en B». ¿Qué tiene B?",
    "ops": [
      "5",
      "9",
      "14"
    ],
    "m": "B toma el valor de A. Lo que tenía B se pierde."
  },
  {
    "q": "En ese mismo caso, ¿qué queda en A?",
    "ops": [
      "5, no cambió",
      "9",
      "Nada"
    ],
    "m": "Copiar de A a B no vacía A."
  },
  {
    "q": "Querés intercambiar lo que hay en A y en B. ¿Alcanza con «guardar A en B» y «guardar B en A»?",
    "ops": [
      "No, se pierde uno de los dos valores",
      "Sí, queda intercambiado",
      "Sí, si se hace rápido"
    ],
    "m": "Al pisar B se pierde su valor original. Hace falta una tercera caja temporal: es el clásico problema del intercambio."
  },
  {
    "q": "¿Qué nombre le conviene a una variable?",
    "ops": [
      "Uno que diga qué guarda, como PUNTAJE",
      "Cualquiera, como x1",
      "El más corto posible"
    ],
    "m": "Un buen nombre hace que el programa se entienda solo."
  },
  {
    "q": "TIEMPO tiene 10. Usás «restar 1 a TIEMPO» dentro de un repetir 10 veces. ¿En cuánto termina?",
    "ops": [
      "0",
      "10",
      "1"
    ],
    "m": "Se resta 1 diez veces."
  },
  {
    "q": "Si nunca guardás nada en una caja, ¿qué tiene?",
    "ops": [
      "Nada, está vacía",
      "Un número al azar",
      "Siempre 1"
    ],
    "m": "Por eso conviene darle un valor inicial antes de usarla."
  },
  {
    "q": "Para contar cuántas veces pasa algo, ¿qué usás?",
    "ops": [
      "Una variable que suma 1 cada vez",
      "Un dibujo",
      "Un sonido"
    ],
    "m": "Se llama contador."
  },
  {
    "q": "PUNTOS tiene 7. «sumar PUNTOS a PUNTOS». ¿Qué queda?",
    "ops": [
      "14",
      "7",
      "0"
    ],
    "m": "Se suma a sí misma: 7 + 7."
  },
  {
    "q": "¿Se puede cambiar el valor de una variable muchas veces?",
    "ops": [
      "Sí, para eso sirve",
      "No, una sola vez",
      "Sólo dos veces"
    ],
    "m": "Justamente por eso se llama variable."
  },
  {
    "q": "En un juego, el marcador que sube al juntar monedas, ¿qué es?",
    "ops": [
      "Una variable",
      "Un dibujo fijo",
      "Un sonido"
    ],
    "m": "Guarda un valor que va cambiando."
  },
  {
    "q": "VIDAS tiene 1. «restar 1 a VIDAS». ¿Qué conviene hacer después?",
    "ops": [
      "Preguntar si llegó a 0 y terminar el juego",
      "Sumar 10",
      "Nada"
    ],
    "m": "Las variables se combinan con condicionales para decidir qué pasa."
  },
  {
    "q": "¿Dos cajas pueden llamarse igual?",
    "ops": [
      "No, el programa no sabría cuál es cuál",
      "Sí, siempre",
      "Sí, si guardan lo mismo"
    ],
    "m": "El nombre es lo que las identifica."
  }
];
GAMES.variables_5 = juegoTriviaTexto(CUR_VARIABLES_5_BANCO, "¿Qué queda guardado en la caja?", "variables_");

/* 5° · Si el sensor detecta… — sensores_5
   DC: Entrada y salida; sensores y actuadores; sistemas temporizados
   Fuente: docs/auditoria-dc-caba/grado-5.md · T3 */
const CUR_SENSORES_5_BANCO = [
  {
    "q": "¿Qué hace un sensor?",
    "ops": [
      "Detecta algo del ambiente",
      "Mueve una pieza",
      "Guarda información"
    ],
    "m": "El sensor es la ENTRADA: mide o detecta."
  },
  {
    "q": "¿Qué hace un actuador?",
    "ops": [
      "Realiza una acción, como mover o encender",
      "Detecta la temperatura",
      "Guarda datos"
    ],
    "m": "El actuador es la SALIDA: hace algo en el mundo."
  },
  {
    "q": "En una puerta automática, ¿cuál es el sensor?",
    "ops": [
      "El detector de movimiento",
      "El motor que la abre",
      "El vidrio"
    ],
    "m": "Detecta que te acercás."
  },
  {
    "q": "Y en esa puerta, ¿cuál es el actuador?",
    "ops": [
      "El motor que la abre",
      "El detector",
      "La alarma"
    ],
    "m": "El motor ejecuta la acción."
  },
  {
    "q": "Una luz de patio se prende cuando oscurece. ¿Qué sensor usa?",
    "ops": [
      "Uno de luz",
      "Uno de temperatura",
      "Uno de humedad"
    ],
    "m": "Mide cuánta luz hay."
  },
  {
    "q": "Un riego automático se prende si la tierra está seca. ¿Qué sensor usa?",
    "ops": [
      "Uno de humedad",
      "Uno de luz",
      "Uno de sonido"
    ],
    "m": "Mide cuánta agua tiene la tierra."
  },
  {
    "q": "«SI hace más de 26 grados, ENTONCES prender el ventilador». ¿Qué es esto?",
    "ops": [
      "Una regla con condición",
      "Un sensor",
      "Un actuador"
    ],
    "m": "El sistema decide según lo que mide."
  },
  {
    "q": "Si el sensor de temperatura marca 22 grados con esa regla, ¿qué pasa?",
    "ops": [
      "No se prende el ventilador",
      "Se prende",
      "Se apaga la luz"
    ],
    "m": "22 no es más que 26: la condición no se cumple."
  },
  {
    "q": "Un riego temporizado riega todos los días a las 7. ¿Qué necesita?",
    "ops": [
      "Un reloj, no un sensor de humedad",
      "Un sensor de luz",
      "Un sensor de sonido"
    ],
    "m": "Un sistema temporizado actúa por tiempo, no por lo que detecta."
  },
  {
    "q": "¿Qué problema tiene regar por horario y no por humedad?",
    "ops": [
      "Riega igual aunque haya llovido",
      "No riega nunca",
      "Gasta menos agua"
    ],
    "m": "Por eso a veces conviene combinar reloj y sensor."
  },
  {
    "q": "El termostato de una estufa, ¿qué hace?",
    "ops": [
      "Mide la temperatura y apaga o prende para mantenerla",
      "Sólo calienta",
      "Sólo mide"
    ],
    "m": "Combina sensor y actuador en un mismo sistema."
  },
  {
    "q": "En un semáforo con botón para peatones, ¿qué es el botón?",
    "ops": [
      "Una entrada del sistema",
      "Un actuador",
      "Una salida"
    ],
    "m": "Es la señal que entra al sistema."
  },
  {
    "q": "«SI se detecta humo, ENTONCES sonar la alarma». ¿Cuál es la salida?",
    "ops": [
      "La alarma que suena",
      "El humo",
      "El detector"
    ],
    "m": "La alarma es el actuador."
  },
  {
    "q": "Una regla con DOS condiciones: «si está oscuro Y hay movimiento, prender la luz». Si está oscuro pero nadie pasa…",
    "ops": [
      "No se prende",
      "Se prende igual",
      "Se prende a la mitad"
    ],
    "m": "Con 'Y' se tienen que cumplir las dos."
  },
  {
    "q": "¿El celular tiene sensores?",
    "ops": [
      "Sí, muchos: luz, movimiento, huella",
      "No, ninguno",
      "Sólo la cámara"
    ],
    "m": "Por eso la pantalla se gira sola y baja el brillo de noche."
  },
  {
    "q": "Un ascensor que frena en el piso indicado, ¿cómo sabe dónde está?",
    "ops": [
      "Con sensores de posición",
      "Adivinando",
      "Con un reloj"
    ],
    "m": "Necesita medir dónde está para decidir cuándo frenar."
  }
];
GAMES.sensores_5 = juegoTriviaTexto(CUR_SENSORES_5_BANCO, "¿Qué hace el sistema?", "sensores_5");

/* 5° · ¿Es phishing? — phishing_5
   DC: Phishing; datos personales; identidad digital
   Fuente: docs/auditoria-dc-caba/grado-5.md · T4 */
const CUR_PHISHING_5_BANCO = [
  {
    "it": "«¡GANASTE UN CELULAR! Entrá acá y poné tus datos»",
    "cat": "trampa",
    "m": "Premio que no jugaste + urgencia + pide datos: las tres señales juntas."
  },
  {
    "it": "Un mail de tu escuela desde la dirección de siempre, con la circular del mes",
    "cat": "seguro",
    "m": "Remitente conocido y contenido esperable."
  },
  {
    "it": "Un mensaje de un amigo pidiéndote plata con mucha urgencia",
    "cat": "verificar",
    "m": "Pudieron hackearle la cuenta. Llamalo por otro medio antes de hacer nada."
  },
  {
    "it": "«Tu cuenta será cerrada en 24 horas si no confirmás tu contraseña»",
    "cat": "trampa",
    "m": "Ninguna empresa seria pide la contraseña por mail. La urgencia es para que no pienses."
  },
  {
    "it": "Un compañero te pide por chat en qué barrio vivís para juntarse a estudiar",
    "cat": "verificar",
    "m": "El barrio se puede decir; la dirección exacta, no. Y conviene chequear con un adulto que sea realmente él."
  },
  {
    "it": "«Hola, soy del banco. Pasame el código que te llegó por SMS»",
    "cat": "trampa",
    "m": "El código es de un solo uso y NUNCA se comparte: el banco jamás lo pide."
  },
  {
    "it": "Una notificación de la app de la escuela dentro de la propia app",
    "cat": "seguro",
    "m": "Viene de adentro de la app oficial."
  },
  {
    "it": "«Mirá este video» con un link raro, de alguien que no te escribe nunca",
    "cat": "trampa",
    "m": "Link inesperado de un contacto inactivo: clásico."
  },
  {
    "it": "Un mail de una tienda donde compraste, con el número de tu pedido",
    "cat": "seguro",
    "m": "Tiene un dato que sólo ellos y vos conocen."
  },
  {
    "it": "Un mail que dice ser de una tienda pero el remitente termina en «.info»",
    "cat": "trampa",
    "m": "El dominio del remitente es la pista más fuerte: miralo siempre."
  },
  {
    "it": "Un juego online te pide el nombre de tu escuela para «armar equipos»",
    "cat": "trampa",
    "m": "Un juego no necesita saber a qué escuela vas. Eso es dato personal."
  },
  {
    "it": "Alguien que decís conocer te escribe desde un número nuevo",
    "cat": "verificar",
    "m": "Puede ser real o puede ser alguien haciéndose pasar. Chequealo por el número viejo."
  },
  {
    "it": "«Tu paquete no pudo entregarse, pagá $500 acá» y no encargaste nada",
    "cat": "trampa",
    "m": "Si no esperabas ningún paquete, es estafa."
  },
  {
    "it": "El profe te comparte un documento desde el mail de la escuela",
    "cat": "seguro",
    "m": "Fuente conocida y esperable."
  },
  {
    "it": "Un mail de «soporté técnico» con faltas de ortografía",
    "cat": "trampa",
    "m": "Los errores son una señal, aunque cada vez menos: hay estafas bien escritas."
  },
  {
    "it": "Una encuesta que promete un descuento y pide tu DNI y tu dirección",
    "cat": "trampa",
    "m": "Ninguna encuesta necesita tu DNI."
  },
  {
    "it": "Un mail de tu club avisando el cambio de horario, con el logo de siempre",
    "cat": "verificar",
    "m": "El logo se copia fácil. Si algo cambia, confirmalo por el canal habitual."
  },
  {
    "it": "«Te mando el link de la reunión de mañana», del grupo de la escuela",
    "cat": "seguro",
    "m": "Esperable y del grupo conocido."
  },
  {
    "it": "Alguien que conociste jugando te pide una foto tuya",
    "cat": "trampa",
    "m": "No se mandan fotos a desconocidos, por más amable que sea. Contale a un adulto."
  },
  {
    "it": "Un mensaje que dice «reenviá esto a 10 contactos o tendrás mala suerte»",
    "cat": "trampa",
    "m": "Cadena: no se reenvía."
  },
  {
    "it": "Un mail del banco de tus padres que llega a TU casilla",
    "cat": "verificar",
    "m": "Raro que le escriban a tu mail. Mostráselo a ellos antes de tocar nada."
  },
  {
    "it": "Una app que pide permiso para usar el micrófono siendo una calculadora",
    "cat": "trampa",
    "m": "Si el permiso no tiene nada que ver con lo que hace la app, desconfiá."
  }
];
GAMES.phishing_5 = juegoClasificar(CUR_PHISHING_5_BANCO, "¿Qué harías con este mensaje?", [{"cat": "seguro", "label": "✅ Es seguro"}, {"cat": "trampa", "label": "🚨 Es trampa"}, {"cat": "verificar", "label": "🔍 Verificar antes"}], "phishing_5");

/* 5° · Presupuesto del proyecto — presupuesto_5
   DC: Ed. Financiera: ingreso y gasto, necesario y prescindible, ahorro y deuda
   Fuente: docs/auditoria-dc-caba/grado-5.md · T5 */
const CUR_PRESUPUESTO_5_BANCO = [
  {
    "it": "Lo que se junta en la rifa",
    "cat": "ingreso",
    "m": "Entra plata al proyecto."
  },
  {
    "it": "El micro que los lleva",
    "cat": "necesario",
    "m": "Sin transporte no hay viaje."
  },
  {
    "it": "Remeras personalizadas con el nombre de cada uno",
    "cat": "prescindible",
    "m": "Está buenísimo, pero el viaje se hace igual sin ellas."
  },
  {
    "it": "La venta de pastelitos en el acto",
    "cat": "ingreso",
    "m": "Entra plata."
  },
  {
    "it": "El alojamiento",
    "cat": "necesario",
    "m": "Hay que dormir en algún lado."
  },
  {
    "it": "Un fotógrafo profesional para todo el viaje",
    "cat": "prescindible",
    "m": "Con los celulares alcanza si el presupuesto está justo."
  },
  {
    "it": "Lo que aporta cada familia por mes",
    "cat": "ingreso",
    "m": "Es la cuota que entra."
  },
  {
    "it": "Las comidas",
    "cat": "necesario",
    "m": "Comer no es opcional."
  },
  {
    "it": "Souvenirs para todos",
    "cat": "prescindible",
    "m": "Es lo primero que se recorta si falta plata."
  },
  {
    "it": "El seguro del viaje",
    "cat": "necesario",
    "m": "Parece un gasto evitable pero no lo es: si pasa algo, cubre."
  },
  {
    "it": "Una fiesta extra la última noche",
    "cat": "prescindible",
    "m": "Lindo, no imprescindible."
  },
  {
    "it": "La donación de un comercio del barrio",
    "cat": "ingreso",
    "m": "Entra plata sin que nadie la ponga del bolsillo."
  },
  {
    "it": "Las entradas al parque que van a visitar",
    "cat": "necesario",
    "m": "Es la actividad principal del viaje."
  },
  {
    "it": "Globos y decoración para la despedida",
    "cat": "prescindible",
    "m": "Recortable."
  },
  {
    "it": "Lo que sobró del año pasado",
    "cat": "ingreso",
    "m": "Es plata disponible."
  },
  {
    "it": "Un botiquín de primeros auxilios",
    "cat": "necesario",
    "m": "Barato y no se discute."
  }
];
GAMES.presupuesto_5 = juegoClasificar(CUR_PRESUPUESTO_5_BANCO, "Para el viaje de egresados, ¿qué es cada cosa?", [{"cat": "ingreso", "label": "💵 Ingreso"}, {"cat": "necesario", "label": "✅ Gasto necesario"}, {"cat": "prescindible", "label": "🎈 Gasto prescindible"}], "presupuest");

/* 3° · Cajero de miles — cajero_miles_3
   DC: Valor posicional; composición aditiva de números de 4 cifras
   Fuente: docs/auditoria-dc-caba/grado-3.md · M3 */
const CUR_CAJERO_MILES_3_PIEZAS = {
  "piezas": [
    10,
    50,
    100,
    500,
    1000
  ],
  "cuantas": 2,
  "unidad": "$",
  "m": "Fijate cuánto te falta para llegar y buscá un billete de ese valor."
};
GAMES.cajero_miles_3 = juegoManipular(CUR_CAJERO_MILES_3_PIEZAS, "Tocá los billetes que sumen el monto exacto.", "cajero_mil");

/* 3° · Parejas que dan 1.000 — parejas_mil_3
   DC: Repertorio de sumas que dan 1.000 y 10.000
   Fuente: docs/auditoria-dc-caba/grado-3.md · M7 */
const CUR_PAREJAS_MIL_3_PIEZAS = {
  "piezas": [
    100,
    200,
    300,
    400,
    500,
    600,
    700,
    800,
    900
  ],
  "cuantas": 2,
  "unidad": "",
  "m": "Pensá cuánto le falta al primero para llegar al total."
};
GAMES.parejas_mil_3 = juegoManipular(CUR_PAREJAS_MIL_3_PIEZAS, "Tocá los dos números que juntos den el total.", "parejas_mi");

/* 3° · Ponele la tilde — tilde_pasado_3
   DC: Tildación del pretérito perfecto simple; reglas de acentuación
   Fuente: docs/auditoria-dc-caba/grado-3.md · L2 */
const CUR_TILDE_PASADO_3_BANCO = [
  {
    "q": "Ayer Ana ___ la carta.",
    "ops": [
      "mandó",
      "mando",
      "mándo"
    ],
    "m": "En pasado, la fuerza va en la última sílaba y termina en vocal: lleva tilde."
  },
  {
    "q": "Yo ___ el equipo todos los días.",
    "ops": [
      "mando",
      "mandó",
      "mándo"
    ],
    "m": "En presente la fuerza va en la anteúltima: sin tilde."
  },
  {
    "q": "El nene ___ la pelota.",
    "ops": [
      "pateó",
      "pateo",
      "páteo"
    ],
    "m": "Pasado terminado en vocal: con tilde."
  },
  {
    "q": "Todos los días yo ___ un rato.",
    "ops": [
      "camino",
      "caminó",
      "camínó"
    ],
    "m": "Presente: sin tilde."
  },
  {
    "q": "Anoche ___ mucho.",
    "ops": [
      "llovió",
      "llovio",
      "llóvio"
    ],
    "m": "Pasado con tilde en la última."
  },
  {
    "q": "La maestra ___ el cuento.",
    "ops": [
      "leyó",
      "leyo",
      "léyo"
    ],
    "m": "Pasado: leyó."
  },
  {
    "q": "Yo ___ todos los libros de la serie.",
    "ops": [
      "leo",
      "leó",
      "léo"
    ],
    "m": "Presente sin tilde."
  },
  {
    "q": "El perro ___ toda la noche.",
    "ops": [
      "ladró",
      "ladro",
      "ládro"
    ],
    "m": "Pasado con tilde."
  },
  {
    "q": "Mi hermano ___ la ventana sin querer.",
    "ops": [
      "rompió",
      "rompio",
      "rómpio"
    ],
    "m": "Pasado terminado en vocal: tilde."
  },
  {
    "q": "Ella ___ la respuesta correcta.",
    "ops": [
      "eligió",
      "eligio",
      "elígio"
    ],
    "m": "Pasado con tilde."
  },
  {
    "q": "¿Quién ___ la puerta?",
    "ops": [
      "cerró",
      "cerro",
      "cérro"
    ],
    "m": "Ojo: 'cerro' sin tilde es la montaña. 'Cerró' con tilde es el verbo."
  },
  {
    "q": "Subimos a ese ___ el verano pasado.",
    "ops": [
      "cerro",
      "cerró",
      "cérro"
    ],
    "m": "Acá es la montaña: sin tilde."
  },
  {
    "q": "El médico ___ un remedio.",
    "ops": [
      "recetó",
      "receto",
      "récéto"
    ],
    "m": "Pasado con tilde."
  },
  {
    "q": "'Médico' es una palabra…",
    "ops": [
      "Esdrújula",
      "Grave",
      "Aguda"
    ],
    "m": "La fuerza en la antepenúltima: MÉ-di-co. Todas las esdrújulas llevan tilde."
  }
];
GAMES.tilde_pasado_3 = juegoTriviaTexto(CUR_TILDE_PASADO_3_BANCO, "¿Cuál está bien escrita?", "tilde_pasa");

/* 3° · Armá el diálogo — dialogo_signos_3
   DC: Raya de diálogo; signos de pregunta y exclamación
   Fuente: docs/auditoria-dc-caba/grado-3.md · L5 */
const CUR_DIALOGO_SIGNOS_3_BANCO = [
  {
    "q": "¿Qué signo abre lo que dice un personaje?",
    "ops": [
      "La raya (—)",
      "El guion corto (-)",
      "El paréntesis"
    ],
    "m": "Es una raya larga, distinta del guion de 'físico-química'."
  },
  {
    "q": "¿Cuántos signos de pregunta lleva una pregunta en español?",
    "ops": [
      "Dos: uno al principio y otro al final",
      "Uno, al final",
      "Uno, al principio"
    ],
    "m": "En español se abre y se cierra: ¿Venís?"
  },
  {
    "q": "¿Y una exclamación?",
    "ops": [
      "Dos: ¡ y !",
      "Uno al final",
      "Ninguno"
    ],
    "m": "Igual que la pregunta: ¡Qué lindo!"
  },
  {
    "q": "¿Cuál está bien escrita?",
    "ops": [
      "¿Venís al parque?",
      "Venís al parque?",
      "¿Venís al parque"
    ],
    "m": "Se abre y se cierra."
  },
  {
    "q": "Cuando habla otro personaje, ¿qué se hace?",
    "ops": [
      "Se empieza un renglón nuevo con su raya",
      "Se sigue en el mismo renglón",
      "Se usa coma"
    ],
    "m": "Cada voz en su renglón: así se sabe quién habla."
  },
  {
    "q": "«—Hola —dijo Ana.» ¿Qué es 'dijo Ana'?",
    "ops": [
      "Lo que cuenta el narrador",
      "Lo que dice Ana",
      "Un error"
    ],
    "m": "Cuando el narrador se mete, también va con raya."
  },
  {
    "q": "La raya de diálogo, ¿lleva espacio antes de la palabra?",
    "ops": [
      "No, va pegada",
      "Sí, siempre",
      "Sólo si es pregunta"
    ],
    "m": "—Hola, no — Hola."
  },
  {
    "q": "¿Cuál está bien?",
    "ops": [
      "¡Qué frío hace!",
      "Que frío hace!",
      "¡Que frío hace"
    ],
    "m": "Se abre y se cierra la exclamación."
  },
  {
    "q": "En un diálogo, ¿para qué sirve la raya?",
    "ops": [
      "Para marcar que habla un personaje",
      "Para separar palabras",
      "Para terminar la oración"
    ],
    "m": "Es la marca de que empieza una voz."
  },
  {
    "q": "«¿Cómo estás?» ¿Quién habla acá?",
    "ops": [
      "Un personaje, porque es una pregunta directa",
      "El narrador",
      "Nadie"
    ],
    "m": "Las preguntas directas son de los personajes."
  },
  {
    "q": "¿Qué signo va al final de «Qué calor»?",
    "ops": [
      "Exclamación",
      "Pregunta",
      "Punto y coma"
    ],
    "m": "Expresa una emoción: exclamación."
  },
  {
    "q": "¿Se puede escribir un diálogo sin rayas?",
    "ops": [
      "Se puede, pero cuesta saber quién habla",
      "No, es obligatorio",
      "Sí, y se entiende igual"
    ],
    "m": "Las rayas están justamente para que se entienda quién dice qué."
  }
];
GAMES.dialogo_signos_3 = juegoTriviaTexto(CUR_DIALOGO_SIGNOS_3_BANCO, "¿Cómo se escribe lo que dicen?", "dialogo_si");

/* 3° · Detrás del telón — teatro_3
   DC: Teatro: actos y escenas; parlamentos y didascalias
   Fuente: docs/auditoria-dc-caba/grado-3.md · L6 */
const CUR_TEATRO_3_BANCO = [
  {
    "it": "«ANA: ¡No lo puedo creer!»",
    "cat": "parlamento",
    "m": "Lo que dice un personaje, con su nombre adelante."
  },
  {
    "it": "«(Entra corriendo y cierra la puerta.)»",
    "cat": "didascalia",
    "m": "Va entre paréntesis: indica al actor qué hacer. No se dice en voz alta."
  },
  {
    "it": "El ACTO",
    "cat": "parte",
    "m": "Cada gran bloque de la obra."
  },
  {
    "it": "«LUIS: ¿Vos qué opinás?»",
    "cat": "parlamento",
    "m": "Habla un personaje."
  },
  {
    "it": "«(Se apagan las luces.)»",
    "cat": "didascalia",
    "m": "Indicación de escena."
  },
  {
    "it": "La ESCENA",
    "cat": "parte",
    "m": "Cada parte de un acto, según quién está."
  },
  {
    "it": "«NARRADORA: Todo empezó una mañana.»",
    "cat": "parlamento",
    "m": "También es un personaje que habla."
  },
  {
    "it": "«(Con voz temblorosa.)»",
    "cat": "didascalia",
    "m": "Dice CÓMO decirlo: es para el actor."
  },
  {
    "it": "El TELÓN",
    "cat": "parte",
    "m": "Marca el comienzo y el final."
  },
  {
    "it": "«PEDRO: Yo me quedo acá.»",
    "cat": "parlamento",
    "m": "Un personaje habla."
  },
  {
    "it": "«(Silencio largo.)»",
    "cat": "didascalia",
    "m": "Indicación, no se dice."
  },
  {
    "it": "El REPARTO",
    "cat": "parte",
    "m": "La lista de personajes al principio."
  },
  {
    "it": "«(Señala la ventana.)»",
    "cat": "didascalia",
    "m": "Qué hace el actor."
  },
  {
    "it": "«ANA: Mirá eso.»",
    "cat": "parlamento",
    "m": "Lo que se dice en voz alta."
  }
];
GAMES.teatro_3 = juegoClasificar(CUR_TEATRO_3_BANCO, "En una obra de teatro, ¿qué es esto?", [{"cat": "parlamento", "label": "🗣️ Parlamento"}, {"cat": "didascalia", "label": "📋 Didascalia"}, {"cat": "parte", "label": "🎬 Parte de la obra"}], "teatro_3");

/* 3° · ¿Qué globo va? — globos_3
   DC: Historieta: tipos de globo y onomatopeyas
   Fuente: docs/auditoria-dc-caba/grado-3.md · L7 */
const CUR_GLOBOS_3_BANCO = [
  {
    "it": "«Hola, ¿cómo andás?»",
    "cat": "habla",
    "m": "Se lo dice a otro: globo normal."
  },
  {
    "it": "«Ojalá no se dé cuenta…» (nadie más lo escucha)",
    "cat": "piensa",
    "m": "Sólo lo sabe el lector: globo de nubecitas."
  },
  {
    "it": "«¡CUIDADOOO!»",
    "cat": "grita",
    "m": "Globo con picos y letra grande."
  },
  {
    "it": "«¿Vos también venís?»",
    "cat": "habla",
    "m": "Le pregunta a alguien."
  },
  {
    "it": "«Qué raro todo esto» (para sí mismo)",
    "cat": "piensa",
    "m": "Pensamiento."
  },
  {
    "it": "«¡BASTA!»",
    "cat": "grita",
    "m": "Grito."
  },
  {
    "it": "«Pasame el vaso, por favor.»",
    "cat": "habla",
    "m": "Habla normal."
  },
  {
    "it": "«Si le digo la verdad se va a enojar» (no lo dice)",
    "cat": "piensa",
    "m": "Nadie más lo escucha."
  },
  {
    "it": "«¡SOCORRO!»",
    "cat": "grita",
    "m": "Grito de auxilio."
  },
  {
    "it": "«Buen día, señora.»",
    "cat": "habla",
    "m": "Saludo dicho en voz alta."
  },
  {
    "it": "«Ojalá llueva» (mirando el cielo, en silencio)",
    "cat": "piensa",
    "m": "Deseo pensado."
  },
  {
    "it": "«¡NO PUEDE SER!»",
    "cat": "grita",
    "m": "Exclamación fuerte."
  },
  {
    "it": "«Te espero afuera.»",
    "cat": "habla",
    "m": "Se lo dice a alguien."
  },
  {
    "it": "«Qué hambre tengo» (sin decirlo)",
    "cat": "piensa",
    "m": "Pensamiento."
  }
];
GAMES.globos_3 = juegoClasificar(CUR_GLOBOS_3_BANCO, "¿Qué tipo de globo corresponde?", [{"cat": "habla", "label": "💬 Habla"}, {"cat": "piensa", "label": "💭 Piensa"}, {"cat": "grita", "label": "💥 Grita"}], "globos_3");

/* 3° · Versos y estrofas — poema_3
   DC: Poema: estrofas y versos; lenguaje figurado
   Fuente: docs/auditoria-dc-caba/grado-3.md · L8 */
const CUR_POEMA_3_BANCO = [
  {
    "q": "¿Qué es un verso?",
    "ops": [
      "Cada renglón del poema",
      "Cada bloque",
      "El título"
    ],
    "m": "El verso es una línea."
  },
  {
    "q": "¿Y una estrofa?",
    "ops": [
      "Un grupo de versos separado por un espacio",
      "Un renglón",
      "La última palabra"
    ],
    "m": "Las estrofas se separan con un renglón en blanco."
  },
  {
    "q": "Un poema de 8 renglones en 2 bloques tiene…",
    "ops": [
      "8 versos y 2 estrofas",
      "2 versos y 8 estrofas",
      "8 estrofas"
    ],
    "m": "Renglones = versos; bloques = estrofas."
  },
  {
    "q": "¿Qué es la rima?",
    "ops": [
      "Que los finales de los versos suenen parecido",
      "Que empiecen igual",
      "Que sean largos"
    ],
    "m": "La rima está al final del verso."
  },
  {
    "q": "'Luna' rima con…",
    "ops": [
      "cuna",
      "lunes",
      "lupa"
    ],
    "m": "Coinciden desde la vocal fuerte: u-na."
  },
  {
    "q": "«El viento canta entre los árboles». ¿Qué recurso es?",
    "ops": [
      "Personificación",
      "Rima",
      "Comparación"
    ],
    "m": "Cantar lo hacen las personas: se lo presta al viento."
  },
  {
    "q": "«Sus ojos son como el mar». ¿Qué recurso es?",
    "ops": [
      "Comparación",
      "Personificación",
      "Rima"
    ],
    "m": "El 'como' marca la comparación."
  },
  {
    "q": "¿Los poemas tienen que rimar siempre?",
    "ops": [
      "No, hay poemas sin rima",
      "Sí, siempre",
      "Sólo los largos"
    ],
    "m": "El verso libre no rima y sigue siendo poema."
  },
  {
    "q": "'Mar' rima con…",
    "ops": [
      "cantar",
      "mesa",
      "marzo"
    ],
    "m": "Coinciden en -ar."
  },
  {
    "q": "«La noche se puso su vestido de estrellas». ¿Qué es?",
    "ops": [
      "Lenguaje figurado",
      "Un dato real",
      "Una instrucción"
    ],
    "m": "La noche no se viste: se dice de un modo poético."
  },
  {
    "q": "¿Dónde va el título del poema?",
    "ops": [
      "Arriba de todo, antes de los versos",
      "Al final",
      "En el medio"
    ],
    "m": "Encabeza el poema."
  },
  {
    "q": "¿Cómo se sabe dónde termina una estrofa?",
    "ops": [
      "Por el renglón en blanco",
      "Por el punto",
      "Por la rima"
    ],
    "m": "El espacio separa las estrofas."
  }
];
GAMES.poema_3 = juegoTriviaTexto(CUR_POEMA_3_BANCO, "Mirá cómo está armado el poema.", "poema_3");

/* 3° · El conector justo — conectores_3
   DC: Conectores adversativos y continuativos; cohesión
   Fuente: docs/auditoria-dc-caba/grado-3.md · L10 */
const CUR_CONECTORES_3_BANCO = [
  {
    "q": "Quería salir, ___ estaba lloviendo.",
    "ops": [
      "pero",
      "y",
      "porque"
    ],
    "m": "Hay un obstáculo: va un conector que se opone."
  },
  {
    "q": "Estudió mucho, ___ le fue bien.",
    "ops": [
      "así que",
      "pero",
      "aunque"
    ],
    "m": "Lo segundo es consecuencia de lo primero."
  },
  {
    "q": "No fui ___ me sentía mal.",
    "ops": [
      "porque",
      "pero",
      "sin embargo"
    ],
    "m": "Da la causa."
  },
  {
    "q": "Compró pan ___ leche.",
    "ops": [
      "y",
      "pero",
      "aunque"
    ],
    "m": "Simplemente suma."
  },
  {
    "q": "Es caro; ___ , vale la pena.",
    "ops": [
      "sin embargo",
      "además",
      "porque"
    ],
    "m": "Se opone a lo anterior."
  },
  {
    "q": "Llegó tarde, ___ no lo dejaron entrar.",
    "ops": [
      "por eso",
      "aunque",
      "pero"
    ],
    "m": "Marca la consecuencia."
  },
  {
    "q": "Me gusta el mar ___ no sé nadar.",
    "ops": [
      "aunque",
      "porque",
      "así que"
    ],
    "m": "Admite algo que va en contra."
  },
  {
    "q": "Terminó la tarea; ___ , ordenó su cuarto.",
    "ops": [
      "además",
      "pero",
      "porque"
    ],
    "m": "Agrega otra cosa que hizo."
  },
  {
    "q": "Estaba cansado, ___ siguió jugando.",
    "ops": [
      "igual",
      "porque",
      "así que"
    ],
    "m": "Va en contra de lo esperado."
  },
  {
    "q": "Primero mezclá; ___ , amasá.",
    "ops": [
      "después",
      "pero",
      "porque"
    ],
    "m": "Marca el orden en el tiempo."
  },
  {
    "q": "No estudió ___ aprobó igual.",
    "ops": [
      "pero",
      "porque",
      "así que"
    ],
    "m": "Contraste: pasó lo contrario de lo esperado."
  },
  {
    "q": "¿Qué agrega un conector como «pero»?",
    "ops": [
      "Una idea que va en contra de la anterior",
      "Dos ideas que se suman",
      "Una explicación de lo anterior"
    ],
    "m": "Pero, sin embargo y aunque oponen; y, además y también suman."
  }
];
GAMES.conectores_3 = juegoTriviaTexto(CUR_CONECTORES_3_BANCO, "¿Qué palabra une mejor las dos partes?", "conectores");

/* 3° · Fábrica de palabras — derivadas_3
   DC: Sufijos derivativos; prefijos y sufijos frecuentes
   Fuente: docs/auditoria-dc-caba/grado-3.md · L13 */
const CUR_DERIVADAS_3_BANCO = [
  {
    "q": "El que trabaja el pan es el…",
    "ops": [
      "panadero",
      "panoso",
      "panal"
    ],
    "m": "El sufijo -ero nombra al que hace algo."
  },
  {
    "q": "El lugar donde se hace el pan es la…",
    "ops": [
      "panadería",
      "panera",
      "panal"
    ],
    "m": "El sufijo -ería nombra el lugar."
  },
  {
    "q": "Un zapato chiquito es un…",
    "ops": [
      "zapatito",
      "zapatón",
      "zapatero"
    ],
    "m": "-ito hace el diminutivo."
  },
  {
    "q": "Un zapato grande es un…",
    "ops": [
      "zapatón",
      "zapatito",
      "zapatilla"
    ],
    "m": "-ón hace el aumentativo."
  },
  {
    "q": "El que arregla zapatos es el…",
    "ops": [
      "zapatero",
      "zapatón",
      "zapatazo"
    ],
    "m": "-ero: el que trabaja con eso."
  },
  {
    "q": "El lugar donde se venden libros es la…",
    "ops": [
      "librería",
      "librito",
      "librero"
    ],
    "m": "-ería: el lugar."
  },
  {
    "q": "Una casa muy grande es un…",
    "ops": [
      "caserón",
      "casita",
      "casero"
    ],
    "m": "-ón aumentativo."
  },
  {
    "q": "Una flor chiquita es una…",
    "ops": [
      "florcita",
      "florón",
      "florero"
    ],
    "m": "-cita diminutivo."
  },
  {
    "q": "El que vende carne es el…",
    "ops": [
      "carnicero",
      "carnoso",
      "carnaval"
    ],
    "m": "-ero, el oficio."
  },
  {
    "q": "¿Cuál NO es de la familia de 'mar'?",
    "ops": [
      "martes",
      "marino",
      "marinero"
    ],
    "m": "Martes no tiene nada que ver: se parece pero no comparte la raíz."
  },
  {
    "q": "¿Cuál NO es de la familia de 'pan'?",
    "ops": [
      "pantalón",
      "panadero",
      "panera"
    ],
    "m": "Pantalón no viene de pan, aunque empiece igual."
  },
  {
    "q": "Todas las palabras de una familia comparten…",
    "ops": [
      "La raíz",
      "La última letra",
      "La cantidad de sílabas"
    ],
    "m": "La raíz es la parte que se repite y lleva el significado."
  }
];
GAMES.derivadas_3 = juegoTriviaTexto(CUR_DERIVADAS_3_BANCO, "¿Qué palabra sale de esta?", "derivadas_");

/* 3° · ¿Hiato o diptongo? — hiato_diptongo_3
   DC: Segmentación en sílabas con hiatos y diptongos
   Fuente: docs/auditoria-dc-caba/grado-3.md · L14 */
const CUR_HIATO_DIPTONGO_3_BANCO = [
  {
    "q": "«aire» se separa…",
    "ops": [
      "ai-re",
      "a-i-re",
      "air-e"
    ],
    "m": "Las dos vocales van juntas en la misma sílaba: es un diptongo."
  },
  {
    "q": "«maestro» se separa…",
    "ops": [
      "ma-es-tro",
      "maes-tro",
      "ma-estro"
    ],
    "m": "A y E son dos vocales fuertes: se separan. Eso es un hiato."
  },
  {
    "q": "«peine» se separa…",
    "ops": [
      "pei-ne",
      "pe-i-ne",
      "pein-e"
    ],
    "m": "E + I forman diptongo."
  },
  {
    "q": "«leo» se separa…",
    "ops": [
      "le-o",
      "leo",
      "l-eo"
    ],
    "m": "E y O son fuertes: hiato."
  },
  {
    "q": "¿Qué es un diptongo?",
    "ops": [
      "Dos vocales en la misma sílaba",
      "Dos vocales en sílabas distintas",
      "Dos consonantes"
    ],
    "m": "Van juntas."
  },
  {
    "q": "¿Y un hiato?",
    "ops": [
      "Dos vocales en sílabas distintas",
      "Dos vocales juntas",
      "Una vocal sola"
    ],
    "m": "Se separan."
  },
  {
    "q": "«ciudad» se separa…",
    "ops": [
      "ciu-dad",
      "ci-u-dad",
      "ciud-ad"
    ],
    "m": "I + U son dos débiles: forman diptongo."
  },
  {
    "q": "«teatro» se separa…",
    "ops": [
      "te-a-tro",
      "tea-tro",
      "teat-ro"
    ],
    "m": "E y A son fuertes: hiato."
  },
  {
    "q": "«cuaderno» se separa…",
    "ops": [
      "cua-der-no",
      "cu-a-der-no",
      "cuad-er-no"
    ],
    "m": "U + A forman diptongo."
  },
  {
    "q": "¿Cuántas sílabas tiene «aire»?",
    "ops": [
      "2",
      "3",
      "1"
    ],
    "m": "ai-re: dos."
  },
  {
    "q": "¿Cuántas sílabas tiene «maestro»?",
    "ops": [
      "3",
      "2",
      "4"
    ],
    "m": "ma-es-tro: tres, porque hay hiato."
  },
  {
    "q": "Las vocales fuertes son…",
    "ops": [
      "a, e, o",
      "i, u",
      "todas"
    ],
    "m": "Dos fuertes juntas siempre se separan."
  }
];
GAMES.hiato_diptongo_3 = juegoTriviaTexto(CUR_HIATO_DIPTONGO_3_BANCO, "¿Cómo se separa en sílabas?", "hiato_dipt");

/* 3° · Inicio, desarrollo y cierre — estructura_cuento_3
   DC: Estructura narrativa; relaciones temporales y causales
   Fuente: docs/auditoria-dc-caba/grado-3.md · L16 */
const CUR_ESTRUCTURA_CUENTO_3_BANCO = [
  {
    "items": [
      "Sofía vivía cerca del río",
      "Un día el río creció",
      "Los vecinos la ayudaron a mudarse"
    ]
  },
  {
    "items": [
      "El zorro tenía hambre",
      "Vio unas uvas muy altas",
      "Saltó y saltó sin alcanzarlas",
      "Se fue diciendo que estaban verdes"
    ]
  },
  {
    "items": [
      "Era el primer día de clases",
      "Nico se olvidó la mochila",
      "Su hermana se la llevó a la escuela"
    ]
  },
  {
    "items": [
      "Había una vez un pueblo sin agua",
      "Cavaron un pozo muy hondo",
      "Encontraron agua y hubo fiesta"
    ]
  },
  {
    "items": [
      "La ballena nadaba tranquila",
      "Quedó atrapada en una red",
      "Unos pescadores la liberaron"
    ]
  },
  {
    "items": [
      "Tomás quería aprender a andar en bici",
      "Se caía todo el tiempo",
      "Su abuelo lo ayudó",
      "Al final pudo solo"
    ]
  },
  {
    "items": [
      "El árbol del patio estaba seco",
      "Los chicos lo regaron todo el verano",
      "En primavera dio flores"
    ]
  },
  {
    "items": [
      "Ana encontró un perro perdido",
      "Buscó al dueño por el barrio",
      "Lo encontró gracias a un cartel"
    ]
  },
  {
    "items": [
      "Empezó la tormenta",
      "Se cortó la luz en todo el barrio",
      "Cenaron a la luz de las velas"
    ]
  },
  {
    "items": [
      "El circo llegó al pueblo",
      "Se rompió la carpa antes de la función",
      "Todos ayudaron a arreglarla",
      "La función salió igual"
    ]
  }
];
GAMES.estructura_cuento_3 = juegoOrdenar(CUR_ESTRUCTURA_CUENTO_3_BANCO, "Ordená la historia. Tocá en orden.", "Todo cuento empieza presentando, después pasa algo, y al final se resuelve.", "estructura");

/* 3° · ¿Cambió el material? — cambios_material_3
   DC: Cambios de forma y de estado frente a transformaciones
   Fuente: docs/auditoria-dc-caba/grado-3.md · C2 */
const CUR_CAMBIOS_MATERIAL_3_BANCO = [
  {
    "it": "Arrugar una hoja de papel",
    "cat": "forma",
    "m": "Sigue siendo papel."
  },
  {
    "it": "Derretir un cubito de hielo",
    "cat": "estado",
    "m": "Sigue siendo agua, pero líquida."
  },
  {
    "it": "Quemar un papel",
    "cat": "otro",
    "m": "Queda ceniza: ya no se puede volver atrás."
  },
  {
    "it": "Cortar una madera en dos",
    "cat": "forma",
    "m": "Sigue siendo madera."
  },
  {
    "it": "Hervir agua hasta que se evapora",
    "cat": "estado",
    "m": "Agua en gas."
  },
  {
    "it": "Cocinar un huevo",
    "cat": "otro",
    "m": "El huevo cocido no vuelve a ser crudo."
  },
  {
    "it": "Doblar un alambre",
    "cat": "forma",
    "m": "Sigue siendo alambre."
  },
  {
    "it": "Congelar agua",
    "cat": "estado",
    "m": "Agua sólida."
  },
  {
    "it": "Hacer pan con harina y levadura",
    "cat": "otro",
    "m": "La fermentación hace un material nuevo."
  },
  {
    "it": "Estirar un chicle",
    "cat": "forma",
    "m": "El mismo chicle, otra forma."
  },
  {
    "it": "Derretir chocolate",
    "cat": "estado",
    "m": "Al enfriarse vuelve a ser chocolate sólido."
  },
  {
    "it": "Oxidarse un clavo con la lluvia",
    "cat": "otro",
    "m": "El óxido es un material distinto del hierro."
  },
  {
    "it": "Romper un vaso",
    "cat": "forma",
    "m": "Sigue siendo vidrio."
  },
  {
    "it": "Que se pudra una fruta",
    "cat": "otro",
    "m": "Ya no vuelve atrás."
  }
];
GAMES.cambios_material_3 = juegoClasificar(CUR_CAMBIOS_MATERIAL_3_BANCO, "¿Qué cambió acá?", [{"cat": "forma", "label": "✋ Sólo la forma"}, {"cat": "estado", "label": "🧊 El estado"}, {"cat": "otro", "label": "🔥 Se transformó en otra cosa"}], "cambios_ma");

/* 3° · Constelaciones del sur — constelaciones_3
   DC: Constelaciones como figuras; el giro del cielo
   Fuente: docs/auditoria-dc-caba/grado-3.md · C6 */
const CUR_CONSTELACIONES_3_BANCO = [
  {
    "q": "¿Qué es una constelación?",
    "ops": [
      "Un dibujo que inventamos uniendo estrellas",
      "Un grupo de estrellas pegadas",
      "Un planeta"
    ],
    "m": "Las estrellas están lejísimos entre sí: la figura la inventamos nosotros."
  },
  {
    "q": "¿Las estrellas de una constelación están cerca entre sí?",
    "ops": [
      "No, sólo se ven juntas desde acá",
      "Sí, están pegadas",
      "Sí, se tocan"
    ],
    "m": "Pueden estar a distancias muy distintas."
  },
  {
    "q": "¿Qué constelación se ve desde el sur y sirve para orientarse?",
    "ops": [
      "La Cruz del Sur",
      "La Osa Mayor",
      "El Carro"
    ],
    "m": "Su brazo más largo apunta hacia el sur."
  },
  {
    "q": "¿Cuántas estrellas principales tiene la Cruz del Sur?",
    "ops": [
      "Cuatro",
      "Tres",
      "Siete"
    ],
    "m": "Forman una cruz."
  },
  {
    "q": "Las Tres Marías son parte de…",
    "ops": [
      "Orión",
      "la Cruz del Sur",
      "la Luna"
    ],
    "m": "Son el cinturón de Orión."
  },
  {
    "q": "¿Por qué las constelaciones parecen girar en el cielo?",
    "ops": [
      "Porque la Tierra gira",
      "Porque las estrellas se mueven rápido",
      "Porque las empuja el viento"
    ],
    "m": "Lo mismo que hace salir y ponerse al Sol."
  },
  {
    "q": "¿Se ven las mismas constelaciones todo el año?",
    "ops": [
      "No, cambian según la época",
      "Sí, siempre las mismas",
      "Sólo en invierno"
    ],
    "m": "Al girar la Tierra alrededor del Sol miramos hacia otro lado del cielo."
  },
  {
    "q": "¿En qué momento se ven las estrellas?",
    "ops": [
      "De noche, cuando no está la luz del Sol",
      "De día",
      "Sólo en verano"
    ],
    "m": "De día siguen ahí, pero el Sol las tapa."
  },
  {
    "q": "¿Pueblos distintos ven las mismas figuras?",
    "ops": [
      "No, cada cultura inventó las suyas",
      "Sí, todas iguales",
      "Sólo dos culturas"
    ],
    "m": "Los pueblos originarios de acá veían otras figuras, como el Ñandú."
  },
  {
    "q": "¿Las constelaciones tienen siempre la misma forma?",
    "ops": [
      "Sí, durante toda una vida humana",
      "No, cambian cada mes",
      "Cambian cada noche"
    ],
    "m": "Cambian, pero tan despacio que hacen falta miles de años."
  },
  {
    "q": "¿Para qué usaban las constelaciones los navegantes?",
    "ops": [
      "Para orientarse en el mar",
      "Para saber la temperatura",
      "Para pescar"
    ],
    "m": "Sin GPS, el cielo era el mapa."
  },
  {
    "q": "¿Qué es una estrella?",
    "ops": [
      "Una bola enorme de gas que produce luz propia",
      "Una piedra que brilla",
      "Un planeta lejano"
    ],
    "m": "El Sol es la estrella más cercana."
  }
];
GAMES.constelaciones_3 = juegoTriviaTexto(CUR_CONSTELACIONES_3_BANCO, "Mirá el cielo del sur.", "constelaci");

/* 3° · Antes y ahora — plaza_mayo_3
   DC: Cambios y permanencias; patrimonio; inmigración
   Fuente: docs/auditoria-dc-caba/grado-3.md · C8 */
const CUR_PLAZA_MAYO_3_BANCO = [
  {
    "it": "El Cabildo sigue en la Plaza de Mayo",
    "cat": "permanece",
    "m": "Está desde la época colonial: es patrimonio."
  },
  {
    "it": "Antes se andaba en carro y ahora en subte",
    "cat": "cambio",
    "m": "El transporte cambió por completo."
  },
  {
    "it": "La plaza sigue siendo el lugar donde la gente se junta",
    "cat": "permanece",
    "m": "Cambió alrededor, pero su función es la misma."
  },
  {
    "it": "Antes las calles eran de tierra",
    "cat": "cambio",
    "m": "Hoy están asfaltadas."
  },
  {
    "it": "La Catedral sigue frente a la plaza",
    "cat": "permanece",
    "m": "Sigue en el mismo lugar."
  },
  {
    "it": "Antes se alumbraba con faroles de gas",
    "cat": "cambio",
    "m": "Hoy es luz eléctrica."
  },
  {
    "it": "La Casa Rosada sigue siendo la sede del gobierno",
    "cat": "permanece",
    "m": "Su función no cambió."
  },
  {
    "it": "Antes el agua se traía en carros aguateros",
    "cat": "cambio",
    "m": "Hoy llega por cañerías."
  },
  {
    "it": "Muchas familias del barrio vinieron de otros países",
    "cat": "cambio",
    "m": "La inmigración cambió la población de la ciudad."
  },
  {
    "it": "El Riachuelo sigue siendo el límite sur de la ciudad",
    "cat": "permanece",
    "m": "El límite es el mismo."
  },
  {
    "it": "Antes no existían los edificios altos",
    "cat": "cambio",
    "m": "La ciudad creció hacia arriba."
  },
  {
    "it": "Se sigue festejando el 25 de Mayo en la plaza",
    "cat": "permanece",
    "m": "La costumbre se mantiene."
  }
];
GAMES.plaza_mayo_3 = juegoClasificar(CUR_PLAZA_MAYO_3_BANCO, "En la ciudad, ¿esto cambió o sigue igual?", [{"cat": "cambio", "label": "🔄 Cambió"}, {"cat": "permanece", "label": "🏛️ Sigue igual"}], "plaza_mayo");

/* 3° · El viaje del alimento — viaje_alimento_3
   DC: Transformación del alimento en el organismo; alimentación equilibrada
   Fuente: docs/auditoria-dc-caba/grado-3.md · C9 */
const CUR_VIAJE_ALIMENTO_3_BANCO = [
  {
    "items": [
      "El bocado entra por la boca",
      "Baja por el esófago",
      "Llega al estómago",
      "Pasa al intestino"
    ]
  },
  {
    "items": [
      "Los dientes cortan la comida",
      "La saliva la ablanda",
      "Se traga el bocado"
    ]
  },
  {
    "items": [
      "En el intestino delgado pasan los nutrientes a la sangre",
      "Lo que no sirve sigue al intestino grueso",
      "Se elimina del cuerpo"
    ]
  },
  {
    "items": [
      "Se siembra el trigo",
      "Se cosecha",
      "Se muele para hacer harina",
      "Se hornea el pan"
    ]
  },
  {
    "items": [
      "La vaca da leche",
      "La leche va a la fábrica",
      "Se hace el yogur",
      "Llega al supermercado"
    ]
  },
  {
    "items": [
      "Elegís qué comer",
      "Masticás bien",
      "El cuerpo aprovecha los nutrientes"
    ]
  },
  {
    "items": [
      "Se lava la fruta",
      "Se come",
      "El cuerpo toma sus vitaminas"
    ]
  },
  {
    "items": [
      "El alimento entra",
      "Se transforma en partes chiquitas",
      "Pasa a la sangre",
      "Llega a todas las células"
    ]
  }
];
GAMES.viaje_alimento_3 = juegoOrdenar(CUR_VIAJE_ALIMENTO_3_BANCO, "Ordená el recorrido del alimento. Tocá en orden.", "Seguí el bocado desde que entra hasta que el cuerpo aprovecha lo que sirve.", "viaje_alim");

/* 3° · Mil más, mil menos — mil_mas_menos_3
   DC: Relaciones mil y cien más y menos; doble, triple y mitad
   Fuente: docs/auditoria-dc-caba/grado-3.md · M4 */
const CUR_MIL_MAS_MENOS_3_PLANTILLA = {
  "q": "{a} + {b}",
  "vars": {
    "a": {
      "rango": [
        1200,
        8800
      ],
      "paso": 100
    },
    "b": {
      "opciones": [
        100,
        1000
      ]
    }
  },
  "ok": "a + b",
  "distractores": [
    "a + b*10",
    "a + b/10",
    "a - b"
  ],
  "tope": 10000,
  "m": "Fijate en qué columna sumás: las centenas con las centenas, los miles con los miles. Da {ok}."
};
GAMES.mil_mas_menos_3 = juegoParametrico(CUR_MIL_MAS_MENOS_3_PLANTILLA, "¿Cuánto da?", "mil_mas_me");

/* 3° · Rayo ×10 ×100 ×1.000 — rayo_por_diez_3
   DC: Repertorio multiplicativo por la unidad seguida de ceros
   Fuente: docs/auditoria-dc-caba/grado-3.md · M9 */
const CUR_RAYO_POR_DIEZ_3_PLANTILLA = {
  "q": "{a} × {b}",
  "vars": {
    "a": {
      "rango": [
        2,
        9
      ],
      "paso": 1
    },
    "b": {
      "opciones": [
        10,
        100,
        1000
      ]
    }
  },
  "ok": "a * b",
  "distractores": [
    "a * b * 10",
    "a * b / 10",
    "a + b"
  ],
  "tope": 10000,
  "m": "Multiplicar por 10 agrega UN cero, por 100 dos y por 1.000 tres. Da {ok}."
};
GAMES.rayo_por_diez_3 = juegoParametrico(CUR_RAYO_POR_DIEZ_3_PLANTILLA, "Rápido: ¿cuánto da?", "rayo_por_d");

/* 3° · Multiplicación en partes — multi_partes_3
   DC: Algoritmos intermedios y multiplicación por una cifra
   Fuente: docs/auditoria-dc-caba/grado-3.md · M10 */
const CUR_MULTI_PARTES_3_PLANTILLA = {
  "q": "{a} × {b}",
  "vars": {
    "a": {
      "rango": [
        12,
        48
      ],
      "paso": 1
    },
    "b": {
      "rango": [
        3,
        9
      ],
      "paso": 1
    }
  },
  "ok": "a * b",
  "distractores": [
    "a * b - a",
    "a * b + a",
    "a + b"
  ],
  "tope": 500,
  "m": "Partilo: multiplicá primero las decenas y después las unidades, y sumá. Da {ok}."
};
GAMES.multi_partes_3 = juegoParametrico(CUR_MULTI_PARTES_3_PLANTILLA, "¿Cuánto da?", "multi_part");

/* 3° · Bandeja de huevos — bandeja_huevos_3
   DC: Organizaciones rectangulares; series proporcionales
   Fuente: docs/auditoria-dc-caba/grado-3.md · M12 */
const CUR_BANDEJA_HUEVOS_3_BANCO = [
  {
    "q": "Una bandeja de 3 filas con 4 huevos cada una tiene…",
    "ops": [
      "12 huevos",
      "7 huevos",
      "34 huevos"
    ],
    "m": "Se multiplica: 3 × 4. Contar de a uno también da 12, pero tarda más."
  },
  {
    "q": "Una caja de 5 filas de 6 alfajores tiene…",
    "ops": [
      "30",
      "11",
      "56"
    ],
    "m": "5 × 6 = 30."
  },
  {
    "q": "Si 1 bandeja trae 12 huevos, 3 bandejas traen…",
    "ops": [
      "36",
      "15",
      "24"
    ],
    "m": "12 × 3."
  },
  {
    "q": "Si 2 paquetes traen 10 figuritas, 4 paquetes traen…",
    "ops": [
      "20",
      "14",
      "40"
    ],
    "m": "Cada paquete trae 5; 4 × 5 = 20."
  },
  {
    "q": "Una grilla de 4 por 4 tiene…",
    "ops": [
      "16",
      "8",
      "44"
    ],
    "m": "4 × 4."
  },
  {
    "q": "6 filas de 3 sillas son…",
    "ops": [
      "18",
      "9",
      "63"
    ],
    "m": "6 × 3."
  },
  {
    "q": "¿Por qué conviene multiplicar y no contar de a uno?",
    "ops": [
      "Porque es más rápido y no te perdés",
      "Porque da otro resultado",
      "Porque es más difícil"
    ],
    "m": "Da lo mismo, pero multiplicar es el atajo."
  },
  {
    "q": "Si 3 cajas traen 24 chocolates, 1 caja trae…",
    "ops": [
      "8",
      "21",
      "27"
    ],
    "m": "24 ÷ 3."
  },
  {
    "q": "Una bandeja de 2 filas de 9 tiene lo mismo que…",
    "ops": [
      "9 filas de 2",
      "2 filas de 2",
      "9 filas de 9"
    ],
    "m": "2 × 9 y 9 × 2 dan lo mismo: cambia la forma, no la cantidad."
  },
  {
    "q": "5 bolsas con 4 manzanas cada una: ¿cuántas manzanas?",
    "ops": [
      "20",
      "9",
      "54"
    ],
    "m": "5 × 4."
  },
  {
    "q": "Si 1 auto lleva 4 chicos, 6 autos llevan…",
    "ops": [
      "24",
      "10",
      "46"
    ],
    "m": "6 × 4."
  },
  {
    "q": "Una plancha de 7 filas de 2 galletitas tiene…",
    "ops": [
      "14",
      "9",
      "72"
    ],
    "m": "7 × 2."
  }
];
GAMES.bandeja_huevos_3 = juegoTriviaTexto(CUR_BANDEJA_HUEVOS_3_BANCO, "Contá sin contar de a uno.", "bandeja_hu");

/* 3° · Ubicate en la cuadrícula — cuadricula_3
   DC: Orientación en cuadrícula con casilleros y vocabulario
   Fuente: docs/auditoria-dc-caba/grado-3.md · M14 */
const CUR_CUADRICULA_3_BANCO = [
  {
    "q": "En una cuadrícula, ¿cómo se nombra un casillero?",
    "ops": [
      "Con la letra de la columna y el número de la fila",
      "Sólo con el número",
      "Con dos letras"
    ],
    "m": "Primero la columna (letra), después la fila (número): C4."
  },
  {
    "q": "El casillero C4 está en…",
    "ops": [
      "Columna C, fila 4",
      "Fila C, columna 4",
      "Casillero 34"
    ],
    "m": "La letra siempre es la columna."
  },
  {
    "q": "¿Es lo mismo C4 que 4C?",
    "ops": [
      "No, el orden importa",
      "Sí, es lo mismo",
      "Sólo si es cuadrada"
    ],
    "m": "Se escribe siempre columna y después fila."
  },
  {
    "q": "Si estoy en B2 y me muevo una a la derecha, llego a…",
    "ops": [
      "C2",
      "B3",
      "A2"
    ],
    "m": "A la derecha cambia la letra."
  },
  {
    "q": "Si estoy en B2 y bajo una, llego a…",
    "ops": [
      "B3",
      "C2",
      "B1"
    ],
    "m": "Bajar cambia el número."
  },
  {
    "q": "Si estoy en D5 y subo dos, llego a…",
    "ops": [
      "D3",
      "D7",
      "B5"
    ],
    "m": "Subir resta al número."
  },
  {
    "q": "¿Cuántos casilleros tiene una cuadrícula de 4 columnas y 3 filas?",
    "ops": [
      "12",
      "7",
      "43"
    ],
    "m": "4 × 3."
  },
  {
    "q": "En un mapa, ¿para qué sirve la cuadrícula?",
    "ops": [
      "Para encontrar rápido un lugar",
      "Para saber la distancia",
      "Para pintar"
    ],
    "m": "El índice te da el casillero y vas directo."
  },
  {
    "q": "Si estoy en A1 y me muevo dos a la derecha y una abajo, llego a…",
    "ops": [
      "C2",
      "B3",
      "C1"
    ],
    "m": "Dos letras a la derecha: A→B→C. Una abajo: 1→2."
  },
  {
    "q": "El casillero de más arriba y más a la izquierda suele ser…",
    "ops": [
      "A1",
      "Z9",
      "1A"
    ],
    "m": "Primera columna, primera fila."
  },
  {
    "q": "Si algo está en F1 y otra cosa en F6, están…",
    "ops": [
      "En la misma columna",
      "En la misma fila",
      "En el mismo casillero"
    ],
    "m": "Comparten la letra: misma columna."
  },
  {
    "q": "Si algo está en B3 y otra cosa en E3, están…",
    "ops": [
      "En la misma fila",
      "En la misma columna",
      "Pegados"
    ],
    "m": "Comparten el número: misma fila."
  }
];
GAMES.cuadricula_3 = juegoTriviaTexto(CUR_CUADRICULA_3_BANCO, "Leé la cuadrícula.", "cuadricula");

/* 3° · Detective de figuras — figuras_3
   DC: Rombo y paralelogramo; vértices, lados y diagonales
   Fuente: docs/auditoria-dc-caba/grado-3.md · M15 */
const CUR_FIGURAS_3_BANCO = [
  {
    "q": "¿Cuántos lados tiene un cuadrilátero?",
    "ops": [
      "4",
      "3",
      "5"
    ],
    "m": "'Cuadri' es cuatro.",
    "dib": "cuadrilatero"
  },
  {
    "q": "Una figura con los 4 lados iguales pero sin ángulos rectos es un…",
    "ops": [
      "Rombo",
      "Cuadrado",
      "Rectángulo"
    ],
    "m": "El rombo tiene los lados iguales pero está 'aplastado'.",
    "dib": "rombo"
  },
  {
    "q": "Un cuadrado apoyado en una punta, ¿sigue siendo cuadrado?",
    "ops": [
      "Sí, girarlo no lo cambia",
      "No, es un rombo",
      "No, es un triángulo"
    ],
    "m": "La figura no cambia por girarla. Sigue teniendo 4 lados iguales y 4 ángulos rectos.",
    "dib": "rombo"
  },
  {
    "q": "¿Qué es un vértice?",
    "ops": [
      "Cada punta donde se juntan dos lados",
      "Cada lado",
      "El centro"
    ],
    "m": "Los vértices son las esquinas.",
    "dib": "vertice"
  },
  {
    "q": "¿Cuántos vértices tiene un triángulo?",
    "ops": [
      "3",
      "4",
      "1"
    ],
    "m": "Tres lados, tres vértices.",
    "dib": "triangulo"
  },
  {
    "q": "¿Qué es una diagonal?",
    "ops": [
      "La línea que une dos vértices no vecinos",
      "Cualquier lado",
      "El borde de afuera"
    ],
    "m": "Va de esquina a esquina cruzando la figura.",
    "dib": "diagonal"
  },
  {
    "q": "¿Cuántas diagonales tiene un cuadrado?",
    "ops": [
      "2",
      "4",
      "1"
    ],
    "m": "Une las dos parejas de vértices opuestos.",
    "dib": "diagonales"
  },
  {
    "q": "Un paralelogramo tiene los lados opuestos…",
    "ops": [
      "Paralelos y del mismo largo",
      "Todos iguales",
      "Perpendiculares"
    ],
    "m": "Los de enfrente son paralelos e iguales.",
    "dib": "paralelogramo"
  },
  {
    "q": "¿El rectángulo es un paralelogramo?",
    "ops": [
      "Sí, sus lados opuestos son paralelos",
      "No",
      "Sólo si es cuadrado"
    ],
    "m": "Cumple la condición, así que sí.",
    "dib": "rectangulo"
  },
  {
    "q": "¿Cuántos lados tiene un pentágono?",
    "ops": [
      "5",
      "6",
      "4"
    ],
    "m": "Penta es cinco.",
    "dib": "pentagono"
  },
  {
    "q": "Un triángulo con los 3 lados iguales se llama…",
    "ops": [
      "Equilátero",
      "Isósceles",
      "Escaleno"
    ],
    "m": "Equi es igual.",
    "dib": "triangulo"
  },
  {
    "q": "¿Qué figura no tiene vértices?",
    "ops": [
      "El círculo",
      "El cuadrado",
      "El triángulo"
    ],
    "m": "No tiene esquinas: su borde es una curva.",
    "dib": "circulo"
  }
];
GAMES.figuras_3 = juegoTriviaTexto(CUR_FIGURAS_3_BANCO, "Mirá bien la figura.", "figuras_3");

/* 3° · Medí como experto — medir_3
   DC: m, cm y mm; litro; gramo y kilo; estimación; medios y cuartos
   Fuente: docs/auditoria-dc-caba/grado-3.md · M18 */
const CUR_MEDIR_3_BANCO = [
  {
    "q": "¿Con qué medirías el largo de tu banco?",
    "ops": [
      "Centímetros",
      "Kilómetros",
      "Litros"
    ],
    "m": "El centímetro es la unidad cómoda para algo de esa escala."
  },
  {
    "q": "¿Y la distancia entre dos ciudades?",
    "ops": [
      "Kilómetros",
      "Milímetros",
      "Gramos"
    ],
    "m": "En milímetros el número sería enorme."
  },
  {
    "q": "¿Con qué medirías el agua de una botella?",
    "ops": [
      "Litros",
      "Metros",
      "Kilos"
    ],
    "m": "Los líquidos se miden en litros."
  },
  {
    "q": "1 litro son…",
    "ops": [
      "1.000 ml",
      "100 ml",
      "10 ml"
    ],
    "m": "Mil mililitros entran en un litro."
  },
  {
    "q": "1 centímetro son…",
    "ops": [
      "10 mm",
      "100 mm",
      "1 mm"
    ],
    "m": "Diez milímetros. Miralo en la regla."
  },
  {
    "q": "1 kilo son…",
    "ops": [
      "1.000 g",
      "100 g",
      "10 g"
    ],
    "m": "Kilo es mil."
  },
  {
    "q": "Medio litro es…",
    "ops": [
      "500 ml",
      "50 ml",
      "5 ml"
    ],
    "m": "La mitad de 1.000."
  },
  {
    "q": "Un cuarto de kilo es…",
    "ops": [
      "250 g",
      "400 g",
      "25 g"
    ],
    "m": "1.000 dividido 4."
  },
  {
    "q": "¿Cuánto pesa más o menos una manzana?",
    "ops": [
      "200 gramos",
      "2 kilos",
      "20 kilos"
    ],
    "m": "Estimar es acostumbrarse a los órdenes de magnitud."
  },
  {
    "q": "¿Cuánto mide más o menos una puerta?",
    "ops": [
      "2 metros",
      "2 centímetros",
      "2 kilómetros"
    ],
    "m": "Un poco más alta que una persona."
  },
  {
    "q": "Tres cuartos de litro son…",
    "ops": [
      "750 ml",
      "300 ml",
      "34 ml"
    ],
    "m": "Tres partes de cuatro: 250 × 3."
  },
  {
    "q": "¿Qué es más largo, 90 cm o 1 m?",
    "ops": [
      "1 m",
      "90 cm",
      "Son iguales"
    ],
    "m": "1 m son 100 cm."
  }
];
GAMES.medir_3 = juegoTriviaTexto(CUR_MEDIR_3_BANCO, "¿Con qué se mide y cuánto da?", "medir_3");

/* 3° · Cazador de bugs — bugs_3
   DC: Depuración: encontrar el bloque que falla
   Fuente: docs/auditoria-dc-caba/grado-3.md · T2 */
const CUR_BUGS_3_BANCO = [
  {
    "q": "El robot tenía que avanzar 3 y avanzó 4. ¿Qué pasó?",
    "ops": [
      "Hay un bloque 'avanzar' de más",
      "Falta un bloque",
      "Giró mal"
    ],
    "m": "Depurar es encontrar QUÉ bloque sobra o falta, no borrar todo."
  },
  {
    "q": "El robot tenía que girar a la derecha y giró a la izquierda.",
    "ops": [
      "El bloque de giro está al revés",
      "Falta avanzar",
      "Sobra un repetir"
    ],
    "m": "El bloque equivocado está identificado: se reemplaza ése."
  },
  {
    "q": "Si el programa sale mal, ¿qué conviene hacer primero?",
    "ops": [
      "Leerlo paso a paso",
      "Borrar todo y empezar de nuevo",
      "Agregar más bloques"
    ],
    "m": "Leerlo te dice dónde se desvía; borrar todo te hace repetir el error."
  },
  {
    "q": "¿Cómo se llama buscar y arreglar el error de un programa?",
    "ops": [
      "Depurar",
      "Compilar",
      "Ejecutar"
    ],
    "m": "Depurar, o 'debuggear'."
  },
  {
    "q": "El robot llega al lugar correcto pero mirando para otro lado.",
    "ops": [
      "Falta o sobra un giro al final",
      "Faltan avanzar",
      "Está bien igual"
    ],
    "m": "La posición está bien y la orientación no: el problema es un giro."
  },
  {
    "q": "«repetir 3 veces: avanzar» hace que el robot…",
    "ops": [
      "Avance 3 casilleros",
      "Avance 1",
      "Gire 3 veces"
    ],
    "m": "El bloque de adentro se ejecuta 3 veces."
  },
  {
    "q": "Si tenías «avanzar, avanzar, avanzar, avanzar», ¿cómo lo hacés más corto?",
    "ops": [
      "repetir 4 veces: avanzar",
      "avanzar 4",
      "borrar tres"
    ],
    "m": "Para eso está el bloque repetir."
  },
  {
    "q": "El robot choca contra la pared en el paso 2. ¿Dónde mirás?",
    "ops": [
      "En los bloques 1 y 2",
      "En el último bloque",
      "En todos por igual"
    ],
    "m": "El error está donde se desvió, no después."
  },
  {
    "q": "¿Un programa con un bug siempre falla de entrada?",
    "ops": [
      "No, a veces falla más adelante",
      "Sí, siempre",
      "Nunca falla"
    ],
    "m": "Por eso conviene probarlo paso a paso."
  },
  {
    "q": "¿Sirve probar el programa con los ojos antes de darle play?",
    "ops": [
      "Sí, se llama anticipar",
      "No, hay que ejecutarlo",
      "Sólo si es largo"
    ],
    "m": "Leer y anticipar lo que va a pasar es parte de programar."
  },
  {
    "q": "Al robot le falta llegar UN casillero. ¿Qué hacés?",
    "ops": [
      "Agregar un bloque avanzar",
      "Borrar todo",
      "Cambiar un giro"
    ],
    "m": "Un error chico se arregla con un cambio chico."
  },
  {
    "q": "¿Un bug es culpa de la computadora?",
    "ops": [
      "No, la computadora hace lo que le pediste",
      "Sí, se equivoca sola",
      "A veces"
    ],
    "m": "Hace exactamente lo que dice el programa: si sale mal, el programa lo dice mal."
  }
];
GAMES.bugs_3 = juegoTriviaTexto(CUR_BUGS_3_BANCO, "El programa sale mal. ¿Dónde está el error?", "bugs_3");

/* 3° · La variable contadora — contador_3
   DC: Variables: contar y acumular
   Fuente: docs/auditoria-dc-caba/grado-3.md · T3 */
const CUR_CONTADOR_3_BANCO = [
  {
    "q": "PUNTOS empieza en 0 y sumás 1 tres veces. ¿Cuánto vale?",
    "ops": [
      "3",
      "1",
      "0"
    ],
    "m": "Cada vez se acumula: 0+1+1+1."
  },
  {
    "q": "¿Para qué sirve una variable?",
    "ops": [
      "Para guardar un dato y usarlo después",
      "Para dibujar",
      "Para borrar"
    ],
    "m": "Es una caja con nombre."
  },
  {
    "q": "¿Qué es un contador?",
    "ops": [
      "Una variable que suma 1 cada vez que pasa algo",
      "Un dibujo",
      "Un bloque de giro"
    ],
    "m": "Sirve para contar cuántas veces ocurrió algo."
  },
  {
    "q": "MONEDAS vale 5. Sumás 2. ¿Cuánto vale?",
    "ops": [
      "7",
      "2",
      "52"
    ],
    "m": "Se acumula sobre lo que había."
  },
  {
    "q": "MONEDAS vale 5. GUARDÁS 2. ¿Cuánto vale?",
    "ops": [
      "2",
      "7",
      "5"
    ],
    "m": "Guardar PISA lo que había. Sumar acumula. Es la confusión más común."
  },
  {
    "q": "VIDAS vale 3 y le restás 1 dos veces. ¿Cuánto vale?",
    "ops": [
      "1",
      "2",
      "3"
    ],
    "m": "3−1−1."
  },
  {
    "q": "Si nunca guardaste nada en una variable, ¿qué tiene?",
    "ops": [
      "Nada, está vacía",
      "Siempre 1",
      "Un número al azar"
    ],
    "m": "Por eso conviene darle un valor inicial."
  },
  {
    "q": "¿Qué nombre le conviene a una variable?",
    "ops": [
      "Uno que diga qué guarda, como PUNTAJE",
      "Cualquiera",
      "El más corto"
    ],
    "m": "Un buen nombre hace que el programa se entienda solo."
  },
  {
    "q": "En un juego, el marcador que sube al juntar monedas es…",
    "ops": [
      "Una variable",
      "Un dibujo fijo",
      "Un sonido"
    ],
    "m": "Guarda un valor que cambia."
  },
  {
    "q": "PUNTOS vale 4. «repetir 3 veces: sumar 2 a PUNTOS». ¿Cuánto queda?",
    "ops": [
      "10",
      "6",
      "24"
    ],
    "m": "4 + 2 + 2 + 2."
  },
  {
    "q": "¿Se puede cambiar el valor de una variable muchas veces?",
    "ops": [
      "Sí, para eso sirve",
      "No, una sola vez",
      "Sólo dos"
    ],
    "m": "Por eso se llama variable."
  },
  {
    "q": "VIDAS llega a 0. ¿Qué conviene hacer?",
    "ops": [
      "Preguntar si llegó a 0 y terminar el juego",
      "Sumar 10",
      "Nada"
    ],
    "m": "Las variables se combinan con preguntas para decidir qué pasa."
  }
];
GAMES.contador_3 = juegoTriviaTexto(CUR_CONTADOR_3_BANCO, "¿Qué queda guardado?", "contador_3");

/* 3° · Mundo digital — mundo_digital_3
   DC: Dispositivos digitales y su uso cotidiano
   Fuente: docs/auditoria-dc-caba/grado-3.md · T4 */
const CUR_MUNDO_DIGITAL_3_BANCO = [
  {
    "q": "¿Qué hace el teclado?",
    "ops": [
      "Entra información",
      "Muestra información",
      "Guarda archivos"
    ],
    "m": "Es un dispositivo de ENTRADA."
  },
  {
    "q": "¿Y la pantalla?",
    "ops": [
      "Muestra información",
      "Entra información",
      "Calcula"
    ],
    "m": "Es de SALIDA."
  },
  {
    "q": "¿El micrófono es de entrada o de salida?",
    "ops": [
      "Entrada",
      "Salida",
      "Ninguna"
    ],
    "m": "Toma el sonido y lo mete a la máquina."
  },
  {
    "q": "¿Y el parlante?",
    "ops": [
      "Salida",
      "Entrada",
      "Las dos"
    ],
    "m": "Saca el sonido."
  },
  {
    "q": "¿Dónde quedan guardados los archivos?",
    "ops": [
      "En la memoria del dispositivo",
      "En la pantalla",
      "En el teclado"
    ],
    "m": "La memoria es donde se guarda."
  },
  {
    "q": "¿Qué necesitás para mandar un mensaje a otra ciudad?",
    "ops": [
      "Conexión a internet",
      "Sólo el teclado",
      "Una impresora"
    ],
    "m": "Internet conecta los dispositivos entre sí."
  },
  {
    "q": "La pantalla táctil del celular es…",
    "ops": [
      "Entrada y salida a la vez",
      "Sólo entrada",
      "Sólo salida"
    ],
    "m": "Muestra y también recibe tus toques."
  },
  {
    "q": "¿Una tablet y una computadora hacen cosas parecidas?",
    "ops": [
      "Sí, las dos procesan información",
      "No, nada que ver",
      "Sólo la computadora sirve"
    ],
    "m": "Cambian el tamaño y la forma, no la idea."
  },
  {
    "q": "¿Qué pasa si apagás el dispositivo sin guardar?",
    "ops": [
      "Podés perder lo que estabas haciendo",
      "No pasa nada",
      "Se guarda solo siempre"
    ],
    "m": "Por eso conviene guardar cada tanto."
  },
  {
    "q": "¿Un programa y un archivo son lo mismo?",
    "ops": [
      "No: el programa hace cosas, el archivo guarda datos",
      "Sí",
      "El archivo hace cosas"
    ],
    "m": "El programa es la herramienta; el archivo, lo que hacés con ella."
  },
  {
    "q": "¿La computadora piensa?",
    "ops": [
      "No, ejecuta lo que alguien programó",
      "Sí, decide sola",
      "A veces"
    ],
    "m": "Hace exactamente lo que le indicaron."
  },
  {
    "q": "¿Para qué sirve una contraseña?",
    "ops": [
      "Para que sólo vos entres a lo tuyo",
      "Para que ande más rápido",
      "Para guardar archivos"
    ],
    "m": "Protege lo que es tuyo."
  }
];
GAMES.mundo_digital_3 = juegoTriviaTexto(CUR_MUNDO_DIGITAL_3_BANCO, "¿Para qué sirve?", "mundo_digi");

/* 3° · ¿Con qué se mueve? — con_que_se_mueve_3
   DC: Fuentes de energía y mecanismos simples
   Fuente: docs/auditoria-dc-caba/grado-3.md · T5 */
const CUR_CON_QUE_SE_MUEVE_3_BANCO = [
  {
    "q": "¿Con qué se mueve una bicicleta?",
    "ops": [
      "Con la fuerza de las piernas",
      "Con electricidad",
      "Con nafta"
    ],
    "m": "La energía la ponés vos."
  },
  {
    "q": "¿Y un auto?",
    "ops": [
      "Con combustible o electricidad",
      "Con el viento",
      "Con agua"
    ],
    "m": "Necesita una fuente de energía externa."
  },
  {
    "q": "¿Con qué se mueve un molino de viento?",
    "ops": [
      "Con el viento",
      "Con una pila",
      "Con el sol"
    ],
    "m": "El aire empuja las aspas."
  },
  {
    "q": "¿Qué hace una polea?",
    "ops": [
      "Ayuda a subir cosas con menos esfuerzo",
      "Genera energía",
      "Enfría"
    ],
    "m": "No crea fuerza: la redirige."
  },
  {
    "q": "¿Y una rueda?",
    "ops": [
      "Hace más fácil mover cosas pesadas",
      "Genera electricidad",
      "Frena"
    ],
    "m": "Reduce el rozamiento."
  },
  {
    "q": "Una linterna a pilas convierte…",
    "ops": [
      "Energía de la pila en luz",
      "Luz en energía",
      "Sonido en luz"
    ],
    "m": "Transforma, no crea."
  },
  {
    "q": "¿De dónde sale la energía de un panel solar?",
    "ops": [
      "Del sol",
      "Del viento",
      "Del agua"
    ],
    "m": "Convierte la luz en electricidad."
  },
  {
    "q": "¿Qué hace una palanca?",
    "ops": [
      "Permite mover algo pesado con menos fuerza",
      "Genera calor",
      "Guarda energía"
    ],
    "m": "Es una máquina simple."
  },
  {
    "q": "Un juguete a cuerda guarda la energía en…",
    "ops": [
      "Un resorte",
      "Una pila",
      "El color"
    ],
    "m": "Al dar cuerda tensás el resorte."
  },
  {
    "q": "¿La energía se puede crear de la nada?",
    "ops": [
      "No, sólo se transforma",
      "Sí, en los motores",
      "Sí, con imanes"
    ],
    "m": "Siempre viene de algún lado."
  },
  {
    "q": "¿Qué mueve a un barco a vela?",
    "ops": [
      "El viento",
      "Un motor",
      "Las olas"
    ],
    "m": "El viento empuja la vela."
  },
  {
    "q": "¿Para qué sirven los engranajes?",
    "ops": [
      "Para transmitir el movimiento",
      "Para frenar siempre",
      "Para generar energía"
    ],
    "m": "Pasan el giro de una pieza a otra."
  }
];
GAMES.con_que_se_mueve_3 = juegoTriviaTexto(CUR_CON_QUE_SE_MUEVE_3_BANCO, "¿De dónde saca la energía?", "con_que_se");

/* 3° · Detectives de señales — senales_3
   DC: Señales y su forma; educación vial
   Fuente: docs/auditoria-dc-caba/grado-3.md · T6 */
const CUR_SENALES_3_BANCO = [
  {
    "it": "PARE, octogonal y roja",
    "cat": "obliga",
    "m": "Es la única con ocho lados, para reconocerla aun tapada por la nieve o de espaldas."
  },
  {
    "it": "Prohibido estacionar",
    "cat": "prohibe",
    "m": "Círculo rojo: prohíbe."
  },
  {
    "it": "Curva peligrosa a la derecha",
    "cat": "avisa",
    "m": "Triángulo o rombo amarillo: avisa de un peligro."
  },
  {
    "it": "Contramano",
    "cat": "prohibe",
    "m": "No se puede pasar."
  },
  {
    "it": "Senda peatonal adelante",
    "cat": "avisa",
    "m": "Avisa qué viene."
  },
  {
    "it": "Velocidad máxima 40",
    "cat": "obliga",
    "m": "Obliga a no pasar de ahí."
  },
  {
    "it": "Prohibido girar a la izquierda",
    "cat": "prohibe",
    "m": "Prohibición."
  },
  {
    "it": "Escuela cerca",
    "cat": "avisa",
    "m": "Advierte para que bajes la velocidad."
  },
  {
    "it": "Sentido obligatorio hacia la derecha",
    "cat": "obliga",
    "m": "Indica por dónde hay que ir."
  },
  {
    "it": "Prohibido el paso de bicicletas",
    "cat": "prohibe",
    "m": "Prohibición."
  },
  {
    "it": "Cruce de trenes adelante",
    "cat": "avisa",
    "m": "Advertencia."
  },
  {
    "it": "Camino resbaladizo",
    "cat": "avisa",
    "m": "Avisa de un riesgo."
  },
  {
    "it": "Uso obligatorio del casco",
    "cat": "obliga",
    "m": "Obliga a algo."
  },
  {
    "it": "Prohibido tocar bocina",
    "cat": "prohibe",
    "m": "Prohibición."
  }
];
GAMES.senales_3 = juegoClasificar(CUR_SENALES_3_BANCO, "¿Qué tipo de señal es?", [{"cat": "prohibe", "label": "🚫 Prohíbe"}, {"cat": "obliga", "label": "🔵 Obliga"}, {"cat": "avisa", "label": "⚠️ Avisa"}], "senales_3");

/* 3° · ¿Confiable o sospechoso? — confiable_3
   DC: Confiabilidad de la información digital
   Fuente: docs/auditoria-dc-caba/grado-3.md · T7 */
const CUR_CONFIABLE_3_BANCO = [
  {
    "it": "Un libro de la biblioteca de la escuela",
    "cat": "confiar",
    "m": "Pasó por autores y revisión."
  },
  {
    "it": "«¡Ganaste un premio! Poné tus datos acá»",
    "cat": "sospechar",
    "m": "Premio que no jugaste y te pide datos: trampa."
  },
  {
    "it": "Alguien que no conocés te escribe por un juego",
    "cat": "preguntar",
    "m": "Ante un desconocido, siempre avisale a un adulto."
  },
  {
    "it": "La página del gobierno con los horarios de un museo",
    "cat": "confiar",
    "m": "Fuente oficial del tema."
  },
  {
    "it": "«Reenviá esto a 10 amigos o tendrás mala suerte»",
    "cat": "sospechar",
    "m": "Las cadenas no se reenvían."
  },
  {
    "it": "Un video que dice que los tiburones vuelan",
    "cat": "sospechar",
    "m": "Si contradice todo lo que sabés, verificá."
  },
  {
    "it": "Un mail que dice ser de tu escuela pero con faltas de ortografía",
    "cat": "preguntar",
    "m": "Mostráselo a un adulto antes de tocar nada."
  },
  {
    "it": "Una enciclopedia con la lista de fuentes al final",
    "cat": "confiar",
    "m": "Se puede ir a chequear de dónde sacó los datos."
  },
  {
    "it": "Un juego que te pide el nombre de tu escuela",
    "cat": "sospechar",
    "m": "Un juego no necesita saber eso: es dato personal."
  },
  {
    "it": "Una foto increíble sin decir de dónde salió",
    "cat": "preguntar",
    "m": "Puede ser real o armada: hay que buscar la fuente."
  },
  {
    "it": "El sitio del club al que vas, con el horario de siempre",
    "cat": "confiar",
    "m": "Fuente conocida y esperable."
  },
  {
    "it": "«Pasame una foto tuya» de alguien que conociste jugando",
    "cat": "sospechar",
    "m": "No se mandan fotos a desconocidos. Contale a un adulto."
  },
  {
    "it": "Un dato que te repitieron dos compañeros",
    "cat": "preguntar",
    "m": "Que dos lo repitan no lo hace cierto: pudieron leerlo del mismo lugar."
  },
  {
    "it": "Una noticia del diario que firma quién la escribió",
    "cat": "confiar",
    "m": "Tiene un responsable."
  }
];
GAMES.confiable_3 = juegoClasificar(CUR_CONFIABLE_3_BANCO, "¿Qué harías con esto?", [{"cat": "confiar", "label": "✅ Se puede confiar"}, {"cat": "sospechar", "label": "🚨 Sospechar"}, {"cat": "preguntar", "label": "🙋 Preguntarle a un adulto"}], "confiable_");

/* 3° · ¿Va al compost? — compost_3
   DC: Ed. Ambiental: separación de residuos y compostaje
   Fuente: docs/auditoria-dc-caba/grado-3.md · T8 */
const CUR_COMPOST_3_BANCO = [
  {
    "it": "Cáscara de banana",
    "cat": "compost",
    "m": "Se transforma en tierra."
  },
  {
    "it": "Botella de plástico enjuagada",
    "cat": "reciclable",
    "m": "Limpia se recicla."
  },
  {
    "it": "Servilleta usada con grasa",
    "cat": "basura",
    "m": "El papel sucio de grasa ya no se recicla."
  },
  {
    "it": "Yerba usada",
    "cat": "compost",
    "m": "Excelente para el compost."
  },
  {
    "it": "Diario viejo",
    "cat": "reciclable",
    "m": "Papel limpio y seco."
  },
  {
    "it": "Hojas secas del patio",
    "cat": "compost",
    "m": "La parte 'marrón' del compost."
  },
  {
    "it": "Lata enjuagada",
    "cat": "reciclable",
    "m": "El metal se recicla muchas veces."
  },
  {
    "it": "Envoltorio metalizado de golosina",
    "cat": "basura",
    "m": "Mezcla plástico y aluminio pegados: no se pueden separar."
  },
  {
    "it": "Cáscara de huevo",
    "cat": "compost",
    "m": "Al compost, mejor molida."
  },
  {
    "it": "Frasco de vidrio",
    "cat": "reciclable",
    "m": "El vidrio se recicla siempre."
  },
  {
    "it": "Restos de verdura",
    "cat": "compost",
    "m": "Al compost."
  },
  {
    "it": "Cartón de una caja",
    "cat": "reciclable",
    "m": "Plegado ocupa menos."
  },
  {
    "it": "Un chicle masticado",
    "cat": "basura",
    "m": "No se composta ni se recicla."
  },
  {
    "it": "¿Qué se obtiene del compost?",
    "cat": "compost",
    "m": "Tierra fértil: lo que era basura vuelve a servir."
  }
];
GAMES.compost_3 = juegoClasificar(CUR_COMPOST_3_BANCO, "¿Dónde va este residuo?", [{"cat": "compost", "label": "🍂 Al compost"}, {"cat": "reciclable", "label": "♻️ Reciclable"}, {"cat": "basura", "label": "🗑️ Basura"}], "compost_3");

/* 2° · Constructor de sílabas — silabas_2
   DC: Sílabas y dígrafos; construcción de palabras
   Fuente: docs/auditoria-dc-caba/grado-2.md · L1 */
const CUR_SILABAS_2_BANCO = [
  {
    "q": "«lluvia»",
    "ops": [
      "2",
      "1",
      "3"
    ],
    "m": "llu-via: la ll no se separa."
  },
  {
    "q": "«chocolate»",
    "ops": [
      "4",
      "3",
      "5"
    ],
    "m": "cho-co-la-te. La CH es un solo sonido."
  },
  {
    "q": "«llave»",
    "ops": [
      "2",
      "3",
      "1"
    ],
    "m": "lla-ve. La LL es un solo sonido."
  },
  {
    "q": "«perro»",
    "ops": [
      "2",
      "3",
      "1"
    ],
    "m": "pe-rro. La RR es un solo sonido."
  },
  {
    "q": "«guitarra»",
    "ops": [
      "3",
      "4",
      "2"
    ],
    "m": "gui-ta-rra."
  },
  {
    "q": "«queso»",
    "ops": [
      "2",
      "3",
      "1"
    ],
    "m": "que-so. La QU suena como una K."
  },
  {
    "q": "«carretilla»",
    "ops": [
      "4",
      "3",
      "5"
    ],
    "m": "ca-rre-ti-lla: ni la rr ni la ll se parten."
  },
  {
    "q": "«cuchara»",
    "ops": [
      "3",
      "2",
      "4"
    ],
    "m": "cu-cha-ra: la ch es una sola letra y no se parte."
  },
  {
    "q": "«escuela»",
    "ops": [
      "3",
      "4",
      "2"
    ],
    "m": "es-cue-la."
  },
  {
    "q": "«chancho»",
    "ops": [
      "2",
      "3",
      "4"
    ],
    "m": "chan-cho: dos CH, dos sílabas."
  },
  {
    "q": "¿Qué letras van SIEMPRE juntas y suenan como una sola?",
    "ops": [
      "ch, ll, rr, qu",
      "b, v",
      "m, n"
    ],
    "m": "Se llaman dígrafos: dos letras, un sonido."
  },
  {
    "q": "«pollito»",
    "ops": [
      "3",
      "2",
      "4"
    ],
    "m": "po-lli-to: la ll va entera en su sílaba."
  }
];
GAMES.silabas_2 = juegoTriviaTexto(CUR_SILABAS_2_BANCO, "¿Cuántas sílabas tiene?", "silabas_2");

/* 2° · Una letra cambia todo — pares_minimos_2
   DC: Grafías que cambian el significado de la palabra
   Fuente: docs/auditoria-dc-caba/grado-2.md · L3 */
const CUR_PARES_MINIMOS_2_BANCO = [
  {
    "q": "El animal que da leche es la…",
    "ops": [
      "vaca",
      "baca",
      "waca"
    ],
    "m": "Vaca con V."
  },
  {
    "q": "Lo que se pone arriba del auto es la…",
    "ops": [
      "baca",
      "vaca",
      "waca"
    ],
    "m": "La parrilla del techo es 'baca', con B."
  },
  {
    "q": "Lo que usás para peinarte es el…",
    "ops": [
      "peine",
      "peune",
      "peene"
    ],
    "m": "Peine."
  },
  {
    "q": "El que corta el pelo es el…",
    "ops": [
      "peluquero",
      "peluqero",
      "pelukero"
    ],
    "m": "Con QU."
  },
  {
    "q": "Lo que tomás cuando tenés sed es el…",
    "ops": [
      "vaso",
      "baso",
      "bazo"
    ],
    "m": "Vaso con V. El 'bazo' es un órgano."
  },
  {
    "q": "Ir de un lado a otro es…",
    "ops": [
      "caminar",
      "kaminar",
      "qaminar"
    ],
    "m": "Con C."
  },
  {
    "q": "La casa de las abejas es la…",
    "ops": [
      "colmena",
      "kolmena",
      "qolmena"
    ],
    "m": "Con C."
  },
  {
    "q": "El animal que ladra es el…",
    "ops": [
      "perro",
      "pero",
      "perrro"
    ],
    "m": "Con doble R. 'Pero' con una sola es otra palabra."
  },
  {
    "q": "Lo que decís cuando querés objetar: «me gusta, ___ es caro»",
    "ops": [
      "pero",
      "perro",
      "peró"
    ],
    "m": "Acá va con una sola R."
  },
  {
    "q": "El pelo de la oveja es la…",
    "ops": [
      "lana",
      "llana",
      "laná"
    ],
    "m": "Lana, con L simple."
  },
  {
    "q": "Lo que se usa para abrir la puerta es la…",
    "ops": [
      "llave",
      "lave",
      "yave"
    ],
    "m": "Con LL."
  },
  {
    "q": "Lo que hacés con la ropa sucia: la…",
    "ops": [
      "lavás",
      "llavás",
      "labás"
    ],
    "m": "Lavar con V y L simple."
  }
];
GAMES.pares_minimos_2 = juegoTriviaTexto(CUR_PARES_MINIMOS_2_BANCO, "¿Cuál corresponde?", "pares_mini");

/* 2° · mb, nv y la hache — mb_nv_h_2
   DC: Reglas ortográficas de mb, nv y h
   Fuente: docs/auditoria-dc-caba/grado-2.md · L4 */
const CUR_MB_NV_H_2_BANCO = [
  {
    "q": "Persona: ho___re",
    "ops": [
      "mb",
      "nb",
      "mv"
    ],
    "m": "Antes de B siempre va M: hombre."
  },
  {
    "q": "Se come: ta___or",
    "ops": [
      "mb",
      "nb",
      "mv"
    ],
    "m": "Tambor: M antes de B."
  },
  {
    "q": "Lo contrario de verano: i___ierno",
    "ops": [
      "nv",
      "mv",
      "nb"
    ],
    "m": "Antes de V siempre va N: invierno."
  },
  {
    "q": "Lo que mandás por correo: e___iar",
    "ops": [
      "nv",
      "mv",
      "nb"
    ],
    "m": "Enviar: N antes de V."
  },
  {
    "q": "¿Qué letra va SIEMPRE antes de la B?",
    "ops": [
      "M",
      "N",
      "Ninguna"
    ],
    "m": "Regla sin excepciones: mb."
  },
  {
    "q": "¿Y antes de la V?",
    "ops": [
      "N",
      "M",
      "Ninguna"
    ],
    "m": "Regla sin excepciones: nv."
  },
  {
    "q": "El saludo: ___ola",
    "ops": [
      "h",
      "sin nada",
      "j"
    ],
    "m": "Hola lleva H, aunque no suene."
  },
  {
    "q": "Del gallinero: ___uevo",
    "ops": [
      "h",
      "sin nada",
      "g"
    ],
    "m": "Las palabras que empiezan con el sonido UE llevan H."
  },
  {
    "q": "Del esqueleto: ___ueso",
    "ops": [
      "h",
      "sin nada",
      "g"
    ],
    "m": "Hueso, con H."
  },
  {
    "q": "Del verbo haber: ___ay tres sillas",
    "ops": [
      "h",
      "sin nada",
      "j"
    ],
    "m": "Hay con H."
  },
  {
    "q": "La H, ¿suena?",
    "ops": [
      "No, es muda",
      "Sí, como la J",
      "A veces"
    ],
    "m": "No se oye, pero hay que escribirla."
  },
  {
    "q": "Lo que hacés con las manos: ___acer",
    "ops": [
      "h",
      "sin nada",
      "j"
    ],
    "m": "Hacer con H."
  }
];
GAMES.mb_nv_h_2 = juegoTriviaTexto(CUR_MB_NV_H_2_BANCO, "¿Cómo se escribe?", "mb_nv_h_2");

/* 2° · La sílaba fuerte — acentuacion_2
   DC: Acentuación: agudas, graves y esdrújulas
   Fuente: docs/auditoria-dc-caba/grado-2.md · L5 */
const CUR_ACENTUACION_2_BANCO = [
  {
    "q": "En «ventana», ¿cuál suena más fuerte?",
    "ops": [
      "ta",
      "ven",
      "na"
    ],
    "m": "ven-TA-na. Decila despacio en voz alta."
  },
  {
    "q": "En «camión», ¿cuál suena más fuerte?",
    "ops": [
      "mión",
      "ca",
      "mí"
    ],
    "m": "ca-MIÓN: la última."
  },
  {
    "q": "En «árbol», ¿cuál suena más fuerte?",
    "ops": [
      "ár",
      "bol",
      "bo"
    ],
    "m": "ÁR-bol: la anteúltima."
  },
  {
    "q": "«camión» es una palabra…",
    "ops": [
      "Aguda",
      "Grave",
      "Esdrújula"
    ],
    "m": "La fuerza en la última: aguda."
  },
  {
    "q": "«árbol» es una palabra…",
    "ops": [
      "Grave",
      "Aguda",
      "Esdrújula"
    ],
    "m": "La fuerza en la anteúltima: grave."
  },
  {
    "q": "«pájaro» es una palabra…",
    "ops": [
      "Esdrújula",
      "Grave",
      "Aguda"
    ],
    "m": "PÁ-ja-ro: la antepenúltima."
  },
  {
    "q": "Todas las esdrújulas…",
    "ops": [
      "Llevan tilde siempre",
      "Nunca llevan tilde",
      "A veces"
    ],
    "m": "Es la regla más fácil de todas."
  },
  {
    "q": "En «lápiz», ¿cuál suena más fuerte?",
    "ops": [
      "lá",
      "piz",
      "pi"
    ],
    "m": "LÁ-piz."
  },
  {
    "q": "En «reloj», ¿cuál suena más fuerte?",
    "ops": [
      "loj",
      "re",
      "lo"
    ],
    "m": "re-LOJ: aguda."
  },
  {
    "q": "«mesa» es una palabra…",
    "ops": [
      "Grave",
      "Aguda",
      "Esdrújula"
    ],
    "m": "ME-sa: grave."
  },
  {
    "q": "«música» es una palabra…",
    "ops": [
      "Esdrújula",
      "Grave",
      "Aguda"
    ],
    "m": "MÚ-si-ca: esdrújula, con tilde."
  },
  {
    "q": "¿Cómo se busca la sílaba fuerte?",
    "ops": [
      "Diciendo la palabra despacio en voz alta",
      "Contando las letras",
      "Mirando la primera letra"
    ],
    "m": "Es un sonido: hay que escucharlo."
  }
];
GAMES.acentuacion_2 = juegoTriviaTexto(CUR_ACENTUACION_2_BANCO, "¿Dónde suena más fuerte?", "acentuacio");

/* 2° · Signos y mayúsculas — signos_2
   DC: Signos de pregunta y exclamación; coma; punto y mayúscula
   Fuente: docs/auditoria-dc-caba/grado-2.md · L6 */
const CUR_SIGNOS_2_BANCO = [
  {
    "q": "Una pregunta se escribe…",
    "ops": [
      "¿Venís?",
      "Venís?",
      "¿Venís"
    ],
    "m": "En español se abre Y se cierra."
  },
  {
    "q": "Una exclamación se escribe…",
    "ops": [
      "¡Qué lindo!",
      "Qué lindo!",
      "¡Qué lindo"
    ],
    "m": "La exclamación también se abre y se cierra."
  },
  {
    "q": "¿Qué lleva una pregunta escrita en castellano?",
    "ops": [
      "Signo de apertura y de cierre",
      "Sólo el de cierre",
      "Sólo un punto"
    ],
    "m": "En castellano la pregunta se abre con ¿ y se cierra con ?."
  },
  {
    "q": "«compré pan, leche ___ fruta»",
    "ops": [
      "y",
      "coma",
      "punto"
    ],
    "m": "En una enumeración, la última va con Y."
  },
  {
    "q": "«compré pan___ leche y fruta»",
    "ops": [
      "coma",
      ", y",
      "punto"
    ],
    "m": "Entre los elementos va coma."
  },
  {
    "q": "¿Qué signo termina una oración que cuenta algo?",
    "ops": [
      "El punto",
      "La coma",
      "La pregunta"
    ],
    "m": "El punto cierra la idea."
  },
  {
    "q": "¿Los nombres de persona llevan mayúscula?",
    "ops": [
      "Sí, siempre",
      "No",
      "Sólo al empezar"
    ],
    "m": "Son nombres propios."
  },
  {
    "q": "¿Y los días de la semana?",
    "ops": [
      "No, van con minúscula",
      "Sí",
      "Sólo lunes"
    ],
    "m": "Trampa clásica: lunes, martes y los meses van con minúscula."
  },
  {
    "q": "«mi perro se llama ___»",
    "ops": [
      "Rocco",
      "rocco",
      "ROCCO"
    ],
    "m": "Nombre propio: mayúscula inicial."
  },
  {
    "q": "¿Cómo se escribe la oración completa?",
    "ops": [
      "Hoy es lunes.",
      "hoy es Lunes.",
      "Hoy es Lunes"
    ],
    "m": "Mayúscula al empezar, lunes con minúscula, punto al final."
  },
  {
    "q": "¿Para qué sirve la coma en una lista?",
    "ops": [
      "Para separar los elementos",
      "Para terminar",
      "Para preguntar"
    ],
    "m": "Separa sin cerrar la oración."
  },
  {
    "q": "«qué hora es» le falta…",
    "ops": [
      "Los signos de pregunta",
      "Una coma",
      "Nada"
    ],
    "m": "Es una pregunta: ¿Qué hora es?"
  }
];
GAMES.signos_2 = juegoTriviaTexto(CUR_SIGNOS_2_BANCO, "¿Cómo se escribe bien?", "signos_2");

/* 2° · Separá las palabras — separar_palabras_2
   DC: Separación de palabras en la escritura
   Fuente: docs/auditoria-dc-caba/grado-2.md · L19 */
const CUR_SEPARAR_PALABRAS_2_BANCO = [
  {
    "q": "¿«mi mamá» o «mimamá»?",
    "ops": [
      "mi mamá",
      "mimamá",
      "mi-mamá"
    ],
    "m": "Son dos palabras."
  },
  {
    "q": "¿«se lo dije» o «selo dije»?",
    "ops": [
      "se lo dije",
      "selo dije",
      "se lodije"
    ],
    "m": "Tres palabras separadas."
  },
  {
    "q": "¿«por favor» o «porfavor»?",
    "ops": [
      "por favor",
      "porfavor",
      "por-favor"
    ],
    "m": "Dos palabras."
  },
  {
    "q": "¿«en seguida» o «ense guida»?",
    "ops": [
      "en seguida",
      "enseguida",
      "ense guida"
    ],
    "m": "Las dos primeras existen, pero 'ense guida' no."
  },
  {
    "q": "¿«a veces» o «aveces»?",
    "ops": [
      "a veces",
      "aveces",
      "ha veces"
    ],
    "m": "Dos palabras."
  },
  {
    "q": "¿«de repente» o «derepente»?",
    "ops": [
      "de repente",
      "derepente",
      "dere pente"
    ],
    "m": "Dos palabras."
  },
  {
    "q": "¿«me gusta» o «megusta»?",
    "ops": [
      "me gusta",
      "megusta",
      "me-gusta"
    ],
    "m": "Dos palabras."
  },
  {
    "q": "¿«te lo doy» o «telo doy»?",
    "ops": [
      "te lo doy",
      "telo doy",
      "te lodoy"
    ],
    "m": "Tres palabras."
  },
  {
    "q": "¿«sin embargo» o «sinembargo»?",
    "ops": [
      "sin embargo",
      "sinembargo",
      "sin-embargo"
    ],
    "m": "Dos palabras."
  },
  {
    "q": "¿«tal vez» o «talvez»?",
    "ops": [
      "tal vez",
      "talvez",
      "tal-vez"
    ],
    "m": "Dos palabras."
  },
  {
    "q": "«Miamigo» está mal escrito. ¿Por qué?",
    "ops": [
      "Son dos palabras: mi amigo",
      "Le falta una tilde",
      "Va con mayúscula"
    ],
    "m": "«Mi» y «amigo» son dos palabras y van separadas."
  },
  {
    "q": "¿«lo hice» o «lohice»?",
    "ops": [
      "lo hice",
      "lohice",
      "lo-hice"
    ],
    "m": "Dos palabras."
  }
];
GAMES.separar_palabras_2 = juegoTriviaTexto(CUR_SEPARAR_PALABRAS_2_BANCO, "¿Cuál está bien separado?", "separar_pa");

/* 2° · Ordená el relato — ordenar_relato_2
   DC: Secuencia narrativa con y sin conectores
   Fuente: docs/auditoria-dc-caba/grado-2.md · L8 */
const CUR_ORDENAR_RELATO_2_BANCO = [
  {
    "items": [
      "Ana se despertó",
      "Se lavó los dientes",
      "Salió para la escuela"
    ]
  },
  {
    "items": [
      "Llovió toda la noche",
      "Se llenó de agua la vereda",
      "Los chicos saltaron los charcos"
    ]
  },
  {
    "items": [
      "Plantaron la semilla",
      "La regaron todos los días",
      "Salió un brote"
    ]
  },
  {
    "items": [
      "El gato tenía hambre",
      "Maulló en la cocina",
      "Le dieron de comer"
    ]
  },
  {
    "items": [
      "Sonó el timbre",
      "Los chicos salieron al patio",
      "Empezó el recreo"
    ]
  },
  {
    "items": [
      "Juntaron los ingredientes",
      "Mezclaron todo",
      "Lo pusieron en el horno",
      "Comieron la torta"
    ]
  },
  {
    "items": [
      "Se rompió la pelota",
      "Fueron a comprar otra",
      "Siguieron jugando"
    ]
  },
  {
    "items": [
      "Llegó el verano",
      "Fueron a la playa",
      "Se metieron al mar"
    ]
  },
  {
    "items": [
      "Nico se cayó de la bici",
      "Se lastimó la rodilla",
      "Le pusieron una curita"
    ]
  },
  {
    "items": [
      "Compraron entradas",
      "Entraron al cine",
      "Empezó la película"
    ]
  }
];
GAMES.ordenar_relato_2 = juegoOrdenar(CUR_ORDENAR_RELATO_2_BANCO, "Ordená la historia. Tocá en orden.", "Pensá qué tuvo que pasar primero para que pase lo siguiente.", "ordenar_re");

/* 2° · Buscá el dato — buscar_dato_2
   DC: Localizar información en un texto o etiqueta
   Fuente: docs/auditoria-dc-caba/grado-2.md · L11 */
const CUR_BUSCAR_DATO_2_BANCO = [
  {
    "q": "«Fiesta de Lucía. Sábado 8, a las 16 h.» ¿Qué día es?",
    "ops": [
      "Sábado 8",
      "Lucía",
      "16 h"
    ],
    "m": "El día es lo que sigue a la fecha."
  },
  {
    "q": "Con ese mismo texto: ¿a qué hora empieza?",
    "ops": [
      "16 h",
      "Sábado",
      "8"
    ],
    "m": "La hora lleva la 'h'."
  },
  {
    "q": "«Galletitas. Contenido: 200 g.» ¿Cuánto trae?",
    "ops": [
      "200 g",
      "Galletitas",
      "g"
    ],
    "m": "El contenido está en gramos."
  },
  {
    "q": "«Vence: 12/2026.» ¿Qué dice esa fecha?",
    "ops": [
      "Hasta cuándo se puede consumir",
      "Cuándo se fabricó",
      "El precio"
    ],
    "m": "El vencimiento."
  },
  {
    "q": "«Jarabe. Tomar 1 cucharada cada 8 horas.» ¿Cada cuánto se toma?",
    "ops": [
      "Cada 8 horas",
      "1 cucharada",
      "Jarabe"
    ],
    "m": "La frecuencia."
  },
  {
    "q": "Con ese mismo texto: ¿cuánto se toma por vez?",
    "ops": [
      "1 cucharada",
      "8 horas",
      "Todo el frasco"
    ],
    "m": "La cantidad por toma."
  },
  {
    "q": "«Museo. Martes a domingo de 10 a 18.» ¿Abre los lunes?",
    "ops": [
      "No",
      "Sí",
      "Sólo a la mañana"
    ],
    "m": "Dice martes a domingo: el lunes queda afuera."
  },
  {
    "q": "«Se busca perro. Contacto: 4444-5555.» ¿A qué número llamás?",
    "ops": [
      "4444-5555",
      "Perro",
      "Se busca"
    ],
    "m": "El teléfono de contacto."
  },
  {
    "q": "«Cine. Función: 20:30. Sala 3.» ¿En qué sala es?",
    "ops": [
      "Sala 3",
      "20:30",
      "Cine"
    ],
    "m": "La sala."
  },
  {
    "q": "«Leche. Mantener refrigerada.» ¿Dónde hay que guardarla?",
    "ops": [
      "En la heladera",
      "En el placard",
      "Al sol"
    ],
    "m": "Refrigerada es en frío."
  },
  {
    "q": "Para encontrar un dato rápido, ¿qué conviene?",
    "ops": [
      "Buscar la palabra clave de la pregunta",
      "Leer todo de nuevo",
      "Adivinar"
    ],
    "m": "Si preguntan la hora, buscás el número con 'h'."
  },
  {
    "q": "«Taller de dibujo. Cupo: 15 chicos.» ¿Cuántos entran?",
    "ops": [
      "15",
      "Dibujo",
      "Cupo"
    ],
    "m": "El cupo es la cantidad."
  }
];
GAMES.buscar_dato_2 = juegoTriviaTexto(CUR_BUSCAR_DATO_2_BANCO, "Leé y buscá la información.", "buscar_dat");

/* 2° · El conector justo — conectores_2
   DC: Conectores y/e/ni, o/u y temporales
   Fuente: docs/auditoria-dc-caba/grado-2.md · L12 */
const CUR_CONECTORES_2_BANCO = [
  {
    "q": "Compré pan ___ leche.",
    "ops": [
      "y",
      "o",
      "ni"
    ],
    "m": "Suma las dos cosas."
  },
  {
    "q": "¿Querés agua ___ jugo?",
    "ops": [
      "o",
      "y",
      "ni"
    ],
    "m": "Da a elegir entre dos."
  },
  {
    "q": "No vino Ana ___ Luis.",
    "ops": [
      "ni",
      "y",
      "o"
    ],
    "m": "Niega las dos."
  },
  {
    "q": "Padres ___ hijos.",
    "ops": [
      "e",
      "y",
      "o"
    ],
    "m": "Antes de una palabra que empieza con I o HI, la «Y» se cambia por «E»."
  },
  {
    "q": "Uno ___ otro.",
    "ops": [
      "u",
      "o",
      "y"
    ],
    "m": "Antes de una palabra que empieza con O, la O se cambia por U."
  },
  {
    "q": "Primero me lavo los dientes ___ me acuesto.",
    "ops": [
      "y después",
      "o",
      "ni"
    ],
    "m": "Marca el orden en el tiempo."
  },
  {
    "q": "Estudió mucho ___ le fue bien.",
    "ops": [
      "y por eso",
      "o",
      "ni"
    ],
    "m": "Lo segundo es consecuencia."
  },
  {
    "q": "Aguja ___ hilo.",
    "ops": [
      "e",
      "y",
      "u"
    ],
    "m": "Antes de HI va E."
  },
  {
    "q": "Siete ___ ocho.",
    "ops": [
      "u",
      "o",
      "y"
    ],
    "m": "Antes de O va U."
  },
  {
    "q": "Me lavé las manos ___ comí.",
    "ops": [
      "y luego",
      "o",
      "ni"
    ],
    "m": "Orden temporal."
  },
  {
    "q": "No me gusta el brócoli ___ la espinaca.",
    "ops": [
      "ni",
      "y",
      "o"
    ],
    "m": "Niega las dos."
  },
  {
    "q": "¿Para qué sirven los conectores?",
    "ops": [
      "Para unir ideas",
      "Para separar sílabas",
      "Para poner tildes"
    ],
    "m": "Enganchan las partes de lo que decís."
  }
];
GAMES.conectores_2 = juegoTriviaTexto(CUR_CONECTORES_2_BANCO, "¿Qué palabra une mejor?", "conectores");

/* 2° · Escribilo bien — dictado_2
   DC: Escritura correcta de palabras frecuentes
   Fuente: docs/auditoria-dc-caba/grado-2.md · L15 */
const CUR_DICTADO_2_BANCO = [
  {
    "q": "El día que viene después del lunes.",
    "ops": [
      "martes",
      "marte",
      "martez"
    ],
    "m": "Martes."
  },
  {
    "q": "Lo que usás para escribir.",
    "ops": [
      "lápiz",
      "lapiz",
      "lápis"
    ],
    "m": "Lápiz con Z y con tilde."
  },
  {
    "q": "Donde vas a aprender.",
    "ops": [
      "escuela",
      "escuala",
      "eskuela"
    ],
    "m": "Con C."
  },
  {
    "q": "El lugar donde vivís.",
    "ops": [
      "casa",
      "caza",
      "cassa"
    ],
    "m": "Casa con S. 'Caza' con Z es perseguir animales."
  },
  {
    "q": "Lo que hacés con un libro.",
    "ops": [
      "leer",
      "leher",
      "ler"
    ],
    "m": "Leer, sin H."
  },
  {
    "q": "La estación más fría.",
    "ops": [
      "invierno",
      "imbierno",
      "inbierno"
    ],
    "m": "Invierno: N antes de V."
  },
  {
    "q": "Lo que tomás en el desayuno.",
    "ops": [
      "leche",
      "lechhe",
      "leshe"
    ],
    "m": "Leche."
  },
  {
    "q": "Tu mamá y tu papá son tus…",
    "ops": [
      "padres",
      "padrez",
      "padrés"
    ],
    "m": "Padres."
  },
  {
    "q": "El animal que vuela y hace miel.",
    "ops": [
      "abeja",
      "aveja",
      "habeja"
    ],
    "m": "Abeja con B y sin H."
  },
  {
    "q": "Lo que ves cuando mirás para arriba.",
    "ops": [
      "cielo",
      "sielo",
      "zielo"
    ],
    "m": "Con C."
  },
  {
    "q": "El número después del nueve.",
    "ops": [
      "diez",
      "dies",
      "diéz"
    ],
    "m": "Diez con Z."
  },
  {
    "q": "Lo que hacés cuando tenés sueño.",
    "ops": [
      "dormir",
      "dormis",
      "dorrmir"
    ],
    "m": "Dormir."
  }
];
GAMES.dictado_2 = juegoTriviaTexto(CUR_DICTADO_2_BANCO, "¿Cuál está bien escrita?", "dictado_2");

/* 2° · ¿Qué quiere decir? — vocabulario_2
   DC: Ampliación de vocabulario en contexto
   Fuente: docs/auditoria-dc-caba/grado-2.md · L17 */
const CUR_VOCABULARIO_2_BANCO = [
  {
    "q": "«El nene estaba PENSATIVO.» Estaba…",
    "ops": [
      "Pensando en algo",
      "Corriendo",
      "Enojado"
    ],
    "m": "Viene de 'pensar'."
  },
  {
    "q": "«La sopa estaba TIBIA.» Estaba…",
    "ops": [
      "Ni fría ni caliente",
      "Hirviendo",
      "Congelada"
    ],
    "m": "Tibio es el punto del medio."
  },
  {
    "q": "«El perro es MANSO.» Es…",
    "ops": [
      "Tranquilo y no ataca",
      "Muy grande",
      "Peligroso"
    ],
    "m": "Manso es lo contrario de bravo."
  },
  {
    "q": "«Caminaba con SIGILO.» Caminaba…",
    "ops": [
      "Sin hacer ruido",
      "Corriendo",
      "Cantando"
    ],
    "m": "Con sigilo es en silencio."
  },
  {
    "q": "«La casa era AMPLIA.» Era…",
    "ops": [
      "Grande y espaciosa",
      "Chiquita",
      "Vieja"
    ],
    "m": "Amplia es que sobra lugar."
  },
  {
    "q": "«Estaba EXHAUSTO.» Estaba…",
    "ops": [
      "Muy cansado",
      "Contento",
      "Con hambre"
    ],
    "m": "Exhausto es sin fuerzas."
  },
  {
    "q": "«Le respondió con FRANQUEZA.» Respondió…",
    "ops": [
      "Con la verdad",
      "Con mentiras",
      "Sin hablar"
    ],
    "m": "Franqueza es sinceridad."
  },
  {
    "q": "«El agua estaba CRISTALINA.» Estaba…",
    "ops": [
      "Muy transparente",
      "Sucia",
      "Caliente"
    ],
    "m": "Como el cristal: se ve a través."
  },
  {
    "q": "«Tenía una sonrisa PÍCARA.» Era…",
    "ops": [
      "Traviesa",
      "Triste",
      "Enojada"
    ],
    "m": "Pícaro es travieso."
  },
  {
    "q": "«El camino era SINUOSO.» Tenía…",
    "ops": [
      "Muchas curvas",
      "Piedras",
      "Barro"
    ],
    "m": "Sinuoso es lleno de vueltas."
  },
  {
    "q": "«Habló en voz QUEDA.» Habló…",
    "ops": [
      "Bajito",
      "A los gritos",
      "Rápido"
    ],
    "m": "Voz queda es suave."
  },
  {
    "q": "Si no sabés qué quiere decir una palabra, ¿qué hacés?",
    "ops": [
      "Mirás el resto de la oración",
      "La salteás",
      "Te enojás"
    ],
    "m": "El contexto casi siempre te da una pista."
  }
];
GAMES.vocabulario_2 = juegoTriviaTexto(CUR_VOCABULARIO_2_BANCO, "¿Qué significa esta palabra?", "vocabulari");

/* 2° · El bucle — bucle_2
   DC: Repetir: contar repeticiones frente a contar bloques
   Fuente: docs/auditoria-dc-caba/grado-2.md · T2 */
const CUR_BUCLE_2_BANCO = [
  {
    "q": "«repetir 3 veces: avanzar». ¿Cuántos casilleros avanza?",
    "ops": [
      "3",
      "1",
      "0"
    ],
    "m": "El bloque de adentro se hace 3 veces."
  },
  {
    "q": "«repetir 4 veces: avanzar, girar». ¿Cuántas veces gira?",
    "ops": [
      "4",
      "1",
      "8"
    ],
    "m": "Todo lo de adentro se repite: gira 4 veces."
  },
  {
    "q": "En «repetir 4 veces: avanzar, girar», ¿cuántos BLOQUES hay adentro?",
    "ops": [
      "2",
      "4",
      "8"
    ],
    "m": "Ojo: 2 bloques que se hacen 4 veces. No es lo mismo contar bloques que repeticiones."
  },
  {
    "q": "«avanzar, avanzar, avanzar» se puede escribir como…",
    "ops": [
      "repetir 3 veces: avanzar",
      "repetir 1 vez: avanzar",
      "avanzar 3"
    ],
    "m": "El bucle acorta lo repetido."
  },
  {
    "q": "¿Para qué sirve el bloque repetir?",
    "ops": [
      "Para no copiar lo mismo muchas veces",
      "Para que ande más rápido",
      "Para borrar"
    ],
    "m": "Hace el programa más corto y claro."
  },
  {
    "q": "«repetir 2 veces: avanzar, avanzar». ¿Cuánto avanza en total?",
    "ops": [
      "4",
      "2",
      "1"
    ],
    "m": "2 avances × 2 repeticiones."
  },
  {
    "q": "Si el robot tiene que dar la vuelta a un cuadrado, ¿cuántas veces repite?",
    "ops": [
      "4",
      "1",
      "2"
    ],
    "m": "Un cuadrado tiene 4 lados."
  },
  {
    "q": "«repetir 5 veces: saltar». ¿Cuántos saltos?",
    "ops": [
      "5",
      "1",
      "10"
    ],
    "m": "Cinco."
  },
  {
    "q": "¿Se puede poner un repetir adentro de otro repetir?",
    "ops": [
      "Sí",
      "No",
      "Sólo dos veces"
    ],
    "m": "Se llama bucle anidado."
  },
  {
    "q": "«repetir 3 veces: avanzar» y después «avanzar». ¿Cuánto avanzó?",
    "ops": [
      "4",
      "3",
      "1"
    ],
    "m": "3 del bucle más 1 suelto."
  },
  {
    "q": "Si te equivocaste en el número de repeticiones, ¿qué cambiás?",
    "ops": [
      "Sólo el número",
      "Todo el programa",
      "Los bloques de adentro"
    ],
    "m": "Un cambio chico arregla un error chico."
  },
  {
    "q": "¿El bucle cambia lo que hace el programa?",
    "ops": [
      "No, sólo lo escribe más corto",
      "Sí, hace otra cosa",
      "Lo hace más lento"
    ],
    "m": "El resultado es el mismo."
  }
];
GAMES.bucle_2 = juegoTriviaTexto(CUR_BUCLE_2_BANCO, "¿Qué hace el programa?", "bucle_2");

/* 2° · Si pasa esto… — condicional_2
   DC: Condicionales simples
   Fuente: docs/auditoria-dc-caba/grado-2.md · T3 */
const CUR_CONDICIONAL_2_BANCO = [
  {
    "q": "«SI hay pared, ENTONCES girar». Hay pared. ¿Qué hace?",
    "ops": [
      "Gira",
      "Avanza",
      "Nada"
    ],
    "m": "Se cumple la condición."
  },
  {
    "q": "Con esa misma regla: NO hay pared. ¿Qué hace?",
    "ops": [
      "No gira",
      "Gira",
      "Se apaga"
    ],
    "m": "Si la condición no se cumple, no hace la acción."
  },
  {
    "q": "«SI está oscuro, ENTONCES prender la luz». Es de día. ¿Qué pasa?",
    "ops": [
      "No se prende",
      "Se prende",
      "Se apaga"
    ],
    "m": "No está oscuro."
  },
  {
    "q": "¿Qué parte de la regla es «SI hay pared»?",
    "ops": [
      "La condición",
      "La acción",
      "El resultado"
    ],
    "m": "Es lo que se pregunta."
  },
  {
    "q": "¿Y «ENTONCES girar»?",
    "ops": [
      "La acción",
      "La condición",
      "El error"
    ],
    "m": "Es lo que se hace si se cumple."
  },
  {
    "q": "«SI hay moneda, ENTONCES sumar 1 punto». Pasa por 3 monedas. ¿Cuántos puntos?",
    "ops": [
      "3",
      "1",
      "0"
    ],
    "m": "La regla se aplica cada vez."
  },
  {
    "q": "«SI llueve, ENTONCES llevar paraguas». No llueve. ¿Lleva paraguas?",
    "ops": [
      "No",
      "Sí",
      "A veces"
    ],
    "m": "La condición manda."
  },
  {
    "q": "¿Se puede tener dos condiciones juntas?",
    "ops": [
      "Sí, con un Y",
      "No",
      "Sólo con un O"
    ],
    "m": "«SI está oscuro Y hay movimiento»."
  },
  {
    "q": "«SI está oscuro Y hay alguien, prender». Está oscuro pero no hay nadie.",
    "ops": [
      "No prende",
      "Prende",
      "Prende a la mitad"
    ],
    "m": "Con Y tienen que cumplirse las dos."
  },
  {
    "q": "¿Para qué sirve un condicional?",
    "ops": [
      "Para que el programa decida",
      "Para repetir",
      "Para borrar"
    ],
    "m": "Permite que actúe distinto según lo que pasa."
  },
  {
    "q": "«SI toca el borde, ENTONCES rebotar». Está en el medio. ¿Rebota?",
    "ops": [
      "No",
      "Sí",
      "Se detiene"
    ],
    "m": "No tocó el borde."
  },
  {
    "q": "En un juego, «si las vidas llegan a 0, terminar» es…",
    "ops": [
      "Un condicional",
      "Un bucle",
      "Una variable"
    ],
    "m": "Decide según una condición."
  }
];
GAMES.condicional_2 = juegoTriviaTexto(CUR_CONDICIONAL_2_BANCO, "¿Qué hace el robot?", "condiciona");

/* 2° · Entra y sale — entrada_salida_2
   DC: Dispositivos de entrada y de salida
   Fuente: docs/auditoria-dc-caba/grado-2.md · T4 */
const CUR_ENTRADA_SALIDA_2_BANCO = [
  {
    "it": "El teclado",
    "cat": "entrada",
    "m": "Vos escribís y la información entra."
  },
  {
    "it": "La pantalla",
    "cat": "salida",
    "m": "Te muestra lo que la máquina tiene para decir."
  },
  {
    "it": "El micrófono",
    "cat": "entrada",
    "m": "Toma el sonido y lo mete."
  },
  {
    "it": "El parlante",
    "cat": "salida",
    "m": "Saca el sonido."
  },
  {
    "it": "El mouse",
    "cat": "entrada",
    "m": "Le decís dónde hacer clic."
  },
  {
    "it": "La impresora",
    "cat": "salida",
    "m": "Saca la información en papel."
  },
  {
    "it": "La cámara",
    "cat": "entrada",
    "m": "Captura la imagen."
  },
  {
    "it": "Los auriculares",
    "cat": "salida",
    "m": "Sacan el sonido, sólo para vos."
  },
  {
    "it": "El botón de un ascensor",
    "cat": "entrada",
    "m": "Le pedís algo al sistema."
  },
  {
    "it": "La luz del piso en el ascensor",
    "cat": "salida",
    "m": "Te informa dónde está."
  },
  {
    "it": "El lector de huella",
    "cat": "entrada",
    "m": "Lee tu dedo."
  },
  {
    "it": "La vibración del celular",
    "cat": "salida",
    "m": "Te avisa algo."
  }
];
GAMES.entrada_salida_2 = juegoClasificar(CUR_ENTRADA_SALIDA_2_BANCO, "¿Entra o sale información?", [{"cat": "entrada", "label": "➡️ Entra"}, {"cat": "salida", "label": "⬅️ Sale"}], "entrada_sa");

/* 2° · Parejas que dan 100 — parejas_cien_2
   DC: Repertorio de sumas que dan 100, 500 y 1.000
   Fuente: docs/auditoria-dc-caba/grado-2.md · M3 */
const CUR_PAREJAS_CIEN_2_PIEZAS = {
  "piezas": [
    10,
    20,
    30,
    40,
    50,
    60,
    70,
    80,
    90
  ],
  "cuantas": 2,
  "unidad": "",
  "m": "Pensá cuánto le falta al primero para llegar al total."
};
GAMES.parejas_cien_2 = juegoManipular(CUR_PAREJAS_CIEN_2_PIEZAS, "Tocá los dos números que juntos den el total.", "parejas_ci");

/* 2° · Reparto justo — reparto_2
   DC: Reparto exacto, con resto y partición
   Fuente: docs/auditoria-dc-caba/grado-2.md · M12 */
const CUR_REPARTO_2_BANCO = [
  {
    "q": "12 galletitas entre 4 chicos: a cada uno le tocan…",
    "ops": [
      "3",
      "4",
      "8"
    ],
    "m": "12 repartido en 4 partes iguales."
  },
  {
    "q": "10 figuritas entre 2: a cada uno…",
    "ops": [
      "5",
      "2",
      "8"
    ],
    "m": "La mitad."
  },
  {
    "q": "9 caramelos entre 3: a cada uno…",
    "ops": [
      "3",
      "6",
      "1"
    ],
    "m": "9 en 3 partes."
  },
  {
    "q": "7 alfajores entre 2: a cada uno 3, y…",
    "ops": [
      "sobra 1",
      "sobran 2",
      "no sobra nada"
    ],
    "m": "3 y 3 son 6: queda 1 sin repartir."
  },
  {
    "q": "11 chicos en autos de 4. ¿Cuántos autos hacen falta?",
    "ops": [
      "3",
      "2",
      "4"
    ],
    "m": "En 2 autos entran 8 y quedan 3 a pie. Hace falta un tercero."
  },
  {
    "q": "20 flores en floreros de 5: ¿cuántos floreros?",
    "ops": [
      "4",
      "5",
      "15"
    ],
    "m": "Acá se pregunta cuántos grupos, no cuánto le toca a cada uno."
  },
  {
    "q": "8 chocolates entre 4: a cada uno…",
    "ops": [
      "2",
      "4",
      "12"
    ],
    "m": "8 en 4 partes."
  },
  {
    "q": "15 lápices entre 5: a cada uno…",
    "ops": [
      "3",
      "5",
      "10"
    ],
    "m": "15 en 5 partes."
  },
  {
    "q": "Si sobran caramelos, ¿el reparto está mal?",
    "ops": [
      "No, a veces sobra",
      "Sí, siempre da justo",
      "Hay que tirarlos"
    ],
    "m": "Lo que sobra se llama resto, y es parte del resultado."
  },
  {
    "q": "6 globos entre 4 chicos: a cada uno 1, y…",
    "ops": [
      "sobran 2",
      "sobra 1",
      "no sobra"
    ],
    "m": "4 repartidos, quedan 2."
  },
  {
    "q": "18 stickers entre 3: a cada uno…",
    "ops": [
      "6",
      "3",
      "15"
    ],
    "m": "18 en 3 partes."
  },
  {
    "q": "¿Repartir es lo mismo que sumar?",
    "ops": [
      "No, es partir en grupos iguales",
      "Sí",
      "Sólo a veces"
    ],
    "m": "Repartir es lo contrario de juntar."
  }
];
GAMES.reparto_2 = juegoTriviaTexto(CUR_REPARTO_2_BANCO, "¿Cuánto le toca a cada uno?", "reparto_2");

/* 2° · Los dobles — dobles_2
   DC: Dobles y mitades
   Fuente: docs/auditoria-dc-caba/grado-2.md · M13 */
const CUR_DOBLES_2_PLANTILLA = {
  "q": "El doble de {a}",
  "vars": {
    "a": {
      "rango": [
        3,
        60
      ],
      "paso": 1
    }
  },
  "ok": "a * 2",
  "distractores": [
    "a + 2",
    "a * 2 + 1",
    "a * 2 - 1"
  ],
  "tope": 200,
  "m": "El doble es sumarlo consigo mismo: {a} + {a}. Da {ok}."
};
GAMES.dobles_2 = juegoParametrico(CUR_DOBLES_2_PLANTILLA, "¿Cuánto es el doble?", "dobles_2");

/* 2° · ¿Dónde está? — posiciones_2
   DC: Posiciones, trayectos y puntos de vista
   Fuente: docs/auditoria-dc-caba/grado-2.md · M14 */
const CUR_POSICIONES_2_BANCO = [
  {
    "q": "Si el gato está ARRIBA de la mesa, la mesa está…",
    "ops": [
      "Debajo del gato",
      "Arriba del gato",
      "Al lado"
    ],
    "m": "Es la misma relación mirada al revés."
  },
  {
    "q": "Si camino hacia adelante y me doy vuelta, ahora voy…",
    "ops": [
      "Hacia atrás",
      "Hacia adelante",
      "Hacia arriba"
    ],
    "m": "Darse vuelta invierte el sentido."
  },
  {
    "q": "La puerta está a MI derecha. Si me doy vuelta, queda a mi…",
    "ops": [
      "Izquierda",
      "Derecha",
      "Espalda"
    ],
    "m": "Al girar, se invierten los lados."
  },
  {
    "q": "Si estoy ENTRE Ana y Luis, ¿cuántos hay a cada lado?",
    "ops": [
      "Uno de cada lado",
      "Los dos de un lado",
      "Ninguno"
    ],
    "m": "Estar entre es tener uno a cada lado."
  },
  {
    "q": "Vista desde ARRIBA, una pelota se ve…",
    "ops": [
      "Como un círculo",
      "Como un cuadrado",
      "Como un triángulo"
    ],
    "m": "Desde arriba se ve el contorno redondo."
  },
  {
    "q": "Vista desde arriba, una caja se ve…",
    "ops": [
      "Como un rectángulo",
      "Como un círculo",
      "Como un triángulo"
    ],
    "m": "Se ve la tapa."
  },
  {
    "q": "Si voy 2 pasos adelante y 1 atrás, avancé…",
    "ops": [
      "1 paso",
      "3 pasos",
      "0"
    ],
    "m": "2 − 1."
  },
  {
    "q": "Lo que está CERCA de mí, ¿está cerca de todos?",
    "ops": [
      "No, depende de dónde esté cada uno",
      "Sí, siempre",
      "Sólo en el aula"
    ],
    "m": "Cerca y lejos dependen de quién mira."
  },
  {
    "q": "Si el perro está DELANTE del auto y yo miro desde el otro lado, lo veo…",
    "ops": [
      "Detrás del auto",
      "Delante",
      "Arriba"
    ],
    "m": "El punto de vista cambia lo que ves."
  },
  {
    "q": "Para ir de A a B pasando por C, primero voy…",
    "ops": [
      "De A a C",
      "De A a B",
      "De C a B"
    ],
    "m": "El trayecto respeta el orden pedido."
  },
  {
    "q": "Si algo está DEBAJO de la silla, la silla está…",
    "ops": [
      "Encima",
      "Debajo",
      "Al lado"
    ],
    "m": "Relación inversa."
  },
  {
    "q": "Mi izquierda y la izquierda de alguien que me mira de frente…",
    "ops": [
      "Están cambiadas",
      "Son la misma",
      "No existen"
    ],
    "m": "Por eso conviene decir 'a mi izquierda' o 'a tu izquierda'."
  }
];
GAMES.posiciones_2 = juegoTriviaTexto(CUR_POSICIONES_2_BANCO, "Ubicate en el espacio.", "posiciones");

/* 2° · Medí con la regla — medir_regla_2
   DC: Medición con regla; elección de unidad
   Fuente: docs/auditoria-dc-caba/grado-2.md · M16 */
const CUR_MEDIR_REGLA_2_BANCO = [
  {
    "q": "Para medir algo con la regla, ¿dónde apoyás la punta?",
    "ops": [
      "En el 0",
      "En el 1",
      "Donde caiga"
    ],
    "m": "Si empezás en el 1, todas las medidas te dan mal."
  },
  {
    "q": "Apoyaste en el 2 y el objeto llega al 9. ¿Cuánto mide?",
    "ops": [
      "7 cm",
      "9 cm",
      "11 cm"
    ],
    "m": "9 − 2. Éste es EL error de medir: leer el número final sin restar."
  },
  {
    "q": "Apoyaste en el 0 y llega al 12. ¿Cuánto mide?",
    "ops": [
      "12 cm",
      "11 cm",
      "13 cm"
    ],
    "m": "Desde el 0 se lee directo."
  },
  {
    "q": "¿Con qué medirías tu lápiz?",
    "ops": [
      "Centímetros",
      "Kilómetros",
      "Litros"
    ],
    "m": "El centímetro es la unidad cómoda."
  },
  {
    "q": "¿Y el largo de la escuela?",
    "ops": [
      "Metros",
      "Milímetros",
      "Gramos"
    ],
    "m": "En milímetros el número sería enorme."
  },
  {
    "q": "1 metro son…",
    "ops": [
      "100 cm",
      "10 cm",
      "1.000 cm"
    ],
    "m": "Cien centímetros."
  },
  {
    "q": "Los numeritos chiquitos entre dos centímetros son…",
    "ops": [
      "Milímetros",
      "Metros",
      "Kilos"
    ],
    "m": "Diez milímetros por centímetro."
  },
  {
    "q": "Si medís torcido, la medida…",
    "ops": [
      "Da más de lo que es",
      "Da igual",
      "Da menos"
    ],
    "m": "Hay que apoyar la regla derecha, al lado del objeto."
  },
  {
    "q": "¿Se puede medir con un lápiz en vez de una regla?",
    "ops": [
      "Sí, pero cada lápiz mide distinto",
      "No, nunca",
      "Sí, y da igual"
    ],
    "m": "Por eso existen las unidades: para que todos midan lo mismo."
  },
  {
    "q": "¿Qué es más largo: 50 cm o medio metro?",
    "ops": [
      "Son iguales",
      "50 cm",
      "Medio metro"
    ],
    "m": "Medio metro son 50 cm."
  },
  {
    "q": "¿Con qué medirías el ancho de una moneda?",
    "ops": [
      "Milímetros",
      "Metros",
      "Kilómetros"
    ],
    "m": "Es muy chiquita."
  },
  {
    "q": "Antes de medir, ¿conviene estimar?",
    "ops": [
      "Sí, te avisa si el resultado tiene sentido",
      "No, hace perder tiempo",
      "Sólo si es grande"
    ],
    "m": "Si estimaste 10 cm y te da 80, algo hiciste mal."
  }
];
GAMES.medir_regla_2 = juegoTriviaTexto(CUR_MEDIR_REGLA_2_BANCO, "¿Cómo se mide bien?", "medir_regl");

/* 2° · ¿De qué grupo es? — animales_2
   DC: Clasificación de animales; casos que rompen el estereotipo
   Fuente: docs/auditoria-dc-caba/grado-2.md · C3 */
const CUR_ANIMALES_2_BANCO = [
  {
    "it": "El hornero",
    "cat": "ave",
    "m": "Tiene plumas y pico: es ave."
  },
  {
    "it": "El perro",
    "cat": "mamifero",
    "m": "Tiene pelo y toma leche de su mamá."
  },
  {
    "it": "El salmón",
    "cat": "pez",
    "m": "Vive en el agua y respira por branquias."
  },
  {
    "it": "El pingüino",
    "cat": "ave",
    "m": "No vuela, pero tiene plumas y pico: es ave."
  },
  {
    "it": "El murciélago",
    "cat": "mamifero",
    "m": "Vuela, pero tiene pelo y toma leche: es mamífero, no ave."
  },
  {
    "it": "El delfín",
    "cat": "mamifero",
    "m": "Vive en el mar pero respira aire y toma leche: mamífero."
  },
  {
    "it": "El avestruz",
    "cat": "ave",
    "m": "No vuela y es ave igual."
  },
  {
    "it": "El tiburón",
    "cat": "pez",
    "m": "Respira por branquias."
  },
  {
    "it": "El gato",
    "cat": "mamifero",
    "m": "Pelo y leche."
  },
  {
    "it": "La ballena",
    "cat": "mamifero",
    "m": "Es el animal más grande y es mamífero."
  },
  {
    "it": "El loro",
    "cat": "ave",
    "m": "Plumas y pico."
  },
  {
    "it": "La trucha",
    "cat": "pez",
    "m": "Vive en el río, con branquias."
  },
  {
    "it": "El caballo",
    "cat": "mamifero",
    "m": "Pelo y leche."
  },
  {
    "it": "El cóndor",
    "cat": "ave",
    "m": "El ave más grande de los Andes."
  }
];
GAMES.animales_2 = juegoClasificar(CUR_ANIMALES_2_BANCO, "¿A qué grupo pertenece este animal?", [{"cat": "ave", "label": "🐦 Ave"}, {"cat": "mamifero", "label": "🐕 Mamífero"}, {"cat": "pez", "label": "🐟 Pez"}], "animales_2");

/* 2° · ¿De dónde viene el agua? — agua_2
   DC: El recorrido del agua hasta la canilla
   Fuente: docs/auditoria-dc-caba/grado-2.md · C5 */
const CUR_AGUA_2_BANCO = [
  {
    "items": [
      "Se saca agua del río",
      "Se limpia en la planta",
      "Va por los caños",
      "Sale por la canilla"
    ]
  },
  {
    "items": [
      "Llueve sobre la montaña",
      "El agua baja al río",
      "El río llega a la ciudad"
    ]
  },
  {
    "items": [
      "El agua sucia va por el desagüe",
      "Se trata en una planta",
      "Vuelve limpia al río"
    ]
  },
  {
    "items": [
      "Se junta el agua en un tanque",
      "Baja por los caños del edificio",
      "Llega al departamento"
    ]
  },
  {
    "items": [
      "Se abre la canilla",
      "Sale el agua",
      "Se cierra la canilla para no desperdiciar"
    ]
  },
  {
    "items": [
      "El agua se filtra en la tierra",
      "Queda bajo el suelo",
      "Se saca con una bomba"
    ]
  },
  {
    "items": [
      "El sol evapora el agua",
      "Se forma la nube",
      "Vuelve a llover"
    ]
  },
  {
    "items": [
      "Se llena el vaso",
      "Se toma el agua",
      "Se lava el vaso"
    ]
  }
];
GAMES.agua_2 = juegoOrdenar(CUR_AGUA_2_BANCO, "Ordená el recorrido del agua. Tocá en orden.", "El agua no aparece en la canilla: hace un camino largo antes.", "agua_2");

/* 2° · ¿Se contagia? — salud_2
   DC: Enfermedades contagiosas y no contagiosas; prevención
   Fuente: docs/auditoria-dc-caba/grado-2.md · C6 */
const CUR_SALUD_2_BANCO = [
  {
    "it": "La gripe",
    "cat": "contagia",
    "m": "Se pasa por el aire al toser o estornudar."
  },
  {
    "it": "La celiaquía",
    "cat": "nocontagia",
    "m": "No se contagia de ninguna manera. Se nace con esa condición."
  },
  {
    "it": "La varicela",
    "cat": "contagia",
    "m": "Muy contagiosa entre chicos."
  },
  {
    "it": "La diabetes",
    "cat": "nocontagia",
    "m": "No se pega. Compartir el mate con alguien que tiene diabetes no contagia nada."
  },
  {
    "it": "Los piojos",
    "cat": "contagia",
    "m": "Se pasan de cabeza a cabeza."
  },
  {
    "it": "El asma",
    "cat": "nocontagia",
    "m": "No se contagia."
  },
  {
    "it": "Un resfrío",
    "cat": "contagia",
    "m": "Por el aire y las manos."
  },
  {
    "it": "Una pierna quebrada",
    "cat": "nocontagia",
    "m": "Es un accidente, no se pega."
  },
  {
    "it": "La conjuntivitis",
    "cat": "contagia",
    "m": "Por tocarse los ojos y después algo."
  },
  {
    "it": "Usar anteojos",
    "cat": "nocontagia",
    "m": "Ver poco no se contagia."
  },
  {
    "it": "Una caries",
    "cat": "nocontagia",
    "m": "Se produce por lo que comés y no lavarte."
  },
  {
    "it": "Lavarse las manos ayuda a evitar…",
    "cat": "contagia",
    "m": "Es la mejor forma de cortar el contagio."
  }
];
GAMES.salud_2 = juegoClasificar(CUR_SALUD_2_BANCO, "¿Esto se contagia o no?", [{"cat": "contagia", "label": "🦠 Se contagia"}, {"cat": "nocontagia", "label": "🚫 No se contagia"}], "salud_2");

/* 2° · De la semilla a la planta — plantas_2
   DC: Necesidades de las plantas; el ciclo de la planta
   Fuente: docs/auditoria-dc-caba/grado-2.md · C8 */
const CUR_PLANTAS_2_BANCO = [
  {
    "items": [
      "La semilla",
      "El brote",
      "La planta con hojas",
      "La flor"
    ]
  },
  {
    "items": [
      "Se planta la semilla",
      "Se riega",
      "Sale el brote"
    ]
  },
  {
    "items": [
      "La flor se abre",
      "Aparece el fruto",
      "Adentro hay semillas nuevas"
    ]
  },
  {
    "items": [
      "La raíz toma agua de la tierra",
      "El agua sube por el tallo",
      "Llega a las hojas"
    ]
  },
  {
    "items": [
      "Sale el sol",
      "La planta recibe luz",
      "Fabrica su alimento"
    ]
  },
  {
    "items": [
      "Se seca la planta",
      "Cae la semilla al suelo",
      "Nace una planta nueva"
    ]
  },
  {
    "items": [
      "Se prepara la tierra",
      "Se pone la semilla",
      "Se tapa con tierra",
      "Se riega"
    ]
  },
  {
    "items": [
      "La planta es chiquita",
      "Crece",
      "Da flores"
    ]
  }
];
GAMES.plantas_2 = juegoOrdenar(CUR_PLANTAS_2_BANCO, "Ordená lo que le pasa a la planta. Tocá en orden.", "Todo empieza por la semilla y termina dando semillas nuevas.", "plantas_2");

/* 2° · ¿Dónde va? — residuos_2
   DC: Separación de residuos y reciclado
   Fuente: docs/auditoria-dc-caba/grado-2.md · X1 */
const CUR_RESIDUOS_2_BANCO = [
  {
    "it": "Una botella de plástico enjuagada",
    "cat": "reciclable",
    "m": "Limpia se recicla."
  },
  {
    "it": "Una servilleta sucia de comida",
    "cat": "basura",
    "m": "Es papel, pero sucio de grasa ya no se puede reciclar. Ése es EL error."
  },
  {
    "it": "Una hoja de cuaderno escrita",
    "cat": "reciclable",
    "m": "El papel escrito se recicla."
  },
  {
    "it": "Un envoltorio de golosina",
    "cat": "basura",
    "m": "Mezcla materiales pegados."
  },
  {
    "it": "Una lata enjuagada",
    "cat": "reciclable",
    "m": "El metal se recicla muchas veces."
  },
  {
    "it": "Un chicle masticado",
    "cat": "basura",
    "m": "No se recicla."
  },
  {
    "it": "Un frasco de vidrio",
    "cat": "reciclable",
    "m": "El vidrio se recicla siempre."
  },
  {
    "it": "Una caja de cartón",
    "cat": "reciclable",
    "m": "Plegada ocupa menos."
  },
  {
    "it": "Un pañuelo de papel usado",
    "cat": "basura",
    "m": "Papel sucio: basura."
  },
  {
    "it": "Una botella con restos de aceite",
    "cat": "basura",
    "m": "Sin enjuagar arruina todo el lote de reciclado."
  },
  {
    "it": "Un diario viejo",
    "cat": "reciclable",
    "m": "Papel limpio y seco."
  },
  {
    "it": "Antes de tirar un envase, conviene…",
    "cat": "reciclable",
    "m": "Enjuagarlo: así sí se puede reciclar."
  }
];
GAMES.residuos_2 = juegoClasificar(CUR_RESIDUOS_2_BANCO, "¿En qué cesto va?", [{"cat": "reciclable", "label": "♻️ Reciclable"}, {"cat": "basura", "label": "🗑️ Basura"}], "residuos_2");

/* 2° · ¿Cómo me alimento? — plato_2
   DC: Alimentación equilibrada; etiquetado frontal
   Fuente: docs/auditoria-dc-caba/grado-2.md · X2 */
const CUR_PLATO_2_BANCO = [
  {
    "it": "Frutas",
    "cat": "todos",
    "m": "Cuanto más variadas, mejor."
  },
  {
    "it": "Gaseosa",
    "cat": "aveces",
    "m": "Mucha azúcar y ningún nutriente."
  },
  {
    "it": "Verduras",
    "cat": "todos",
    "m": "La mitad del plato."
  },
  {
    "it": "Golosinas",
    "cat": "aveces",
    "m": "De vez en cuando, no prohibidas."
  },
  {
    "it": "Agua",
    "cat": "todos",
    "m": "Es la mejor bebida."
  },
  {
    "it": "Papas fritas de paquete",
    "cat": "aveces",
    "m": "Mucha sal y grasa."
  },
  {
    "it": "Pan y cereales",
    "cat": "todos",
    "m": "Dan energía."
  },
  {
    "it": "Un alimento con varios sellos negros",
    "cat": "aveces",
    "m": "Los sellos avisan de un vistazo: no lo prohíben, dicen que sea ocasional."
  },
  {
    "it": "Leche o yogur",
    "cat": "todos",
    "m": "Aportan calcio."
  },
  {
    "it": "Alfajor",
    "cat": "aveces",
    "m": "Azúcar y grasas."
  },
  {
    "it": "Huevo",
    "cat": "todos",
    "m": "Aporta proteínas."
  },
  {
    "it": "Jugo en polvo con azúcar",
    "cat": "aveces",
    "m": "Mejor agua o fruta exprimida."
  }
];
GAMES.plato_2 = juegoClasificar(CUR_PLATO_2_BANCO, "¿Cada cuánto conviene comerlo?", [{"cat": "todos", "label": "🥦 Todos los días"}, {"cat": "aveces", "label": "🍬 De vez en cuando"}], "plato_2");

/* 2° · En la calle — vial_2
   DC: Educación vial; señales y semáforo
   Fuente: docs/auditoria-dc-caba/grado-2.md · X3 */
const CUR_VIAL_2_BANCO = [
  {
    "q": "El semáforo del peatón está en rojo y no viene ningún auto. ¿Qué hacés?",
    "ops": [
      "Esperar igual",
      "Cruzar rápido",
      "Cruzar por el medio"
    ],
    "m": "La regla no depende de si mirás o no: puede aparecer un auto que no viste."
  },
  {
    "q": "¿Por dónde se cruza la calle?",
    "ops": [
      "Por la senda peatonal",
      "Por donde sea",
      "Por el medio de la cuadra"
    ],
    "m": "La senda es donde el auto espera que cruces."
  },
  {
    "q": "¿Qué avisa una señal triangular con borde rojo?",
    "ops": [
      "Un peligro adelante",
      "Una prohibición",
      "Un lugar para estacionar"
    ],
    "m": "El triángulo siempre avisa peligro; el círculo rojo prohíbe."
  },
  {
    "q": "¿De qué lado de la vereda se camina?",
    "ops": [
      "Por la vereda, lejos del cordón",
      "Por la calle",
      "Por el cordón"
    ],
    "m": "La vereda es del peatón."
  },
  {
    "q": "En el auto, ¿dónde van los chicos?",
    "ops": [
      "Atrás y con cinturón",
      "Adelante",
      "En la falda de alguien"
    ],
    "m": "Atrás y siempre con cinturón o sillita."
  },
  {
    "q": "En bici, ¿qué hay que usar?",
    "ops": [
      "Casco",
      "Nada",
      "Auriculares"
    ],
    "m": "El casco protege la cabeza."
  },
  {
    "q": "El semáforo en amarillo significa…",
    "ops": [
      "Precaución, va a cambiar",
      "Apurate a cruzar",
      "Podés cruzar"
    ],
    "m": "Avisa que va a ponerse en rojo."
  },
  {
    "q": "Si viene una ambulancia con sirena, los autos…",
    "ops": [
      "Le dejan paso",
      "Siguen igual",
      "Aceleran"
    ],
    "m": "Tiene prioridad."
  },
  {
    "q": "¿Qué forma tienen las señales que PROHÍBEN algo?",
    "ops": [
      "Redondas con borde rojo",
      "Cuadradas verdes",
      "Triangulares azules"
    ],
    "m": "El círculo con borde rojo prohíbe."
  },
  {
    "q": "Si el semáforo de los autos está en verde, para el peatón está…",
    "ops": [
      "En rojo",
      "También en verde",
      "En amarillo"
    ],
    "m": "Cuando los autos avanzan, el peatón espera."
  },
  {
    "q": "El cartel PARE le indica al conductor…",
    "ops": [
      "Que frene por completo",
      "Que baje la velocidad",
      "Que acelere"
    ],
    "m": "Es una parada total."
  },
  {
    "q": "Cruzar mirando el celular…",
    "ops": [
      "Es peligroso, no ves lo que viene",
      "Está bien si es rápido",
      "No pasa nada"
    ],
    "m": "Cruzar pide atención completa."
  }
];
GAMES.vial_2 = juegoTriviaTexto(CUR_VIAL_2_BANCO, "¿Qué corresponde hacer?", "vial_2");

/* 2° · Entre todos — convivencia_2
   DC: Acuerdos de convivencia y cuidado
   Fuente: docs/auditoria-dc-caba/grado-2.md · X4 */
const CUR_CONVIVENCIA_2_BANCO = [
  {
    "q": "Dos compañeros quieren el mismo juguete. ¿Qué conviene?",
    "ops": [
      "Turnarse",
      "Que lo tenga el más fuerte",
      "Esconderlo"
    ],
    "m": "Turnarse es un acuerdo que sirve para los dos."
  },
  {
    "q": "Si alguien te molesta seguido, ¿qué hacés?",
    "ops": [
      "Se lo contás a un adulto",
      "Te lo guardás",
      "Le pegás"
    ],
    "m": "Pedir ayuda es lo que corta la situación."
  },
  {
    "q": "Un compañero se queda solo en el recreo. ¿Qué podés hacer?",
    "ops": [
      "Invitarlo a jugar",
      "Ignorarlo",
      "Reírte"
    ],
    "m": "Incluir cuesta poco y cambia el día."
  },
  {
    "q": "¿Para qué sirven los acuerdos del aula?",
    "ops": [
      "Para que todos puedan estar bien",
      "Para castigar",
      "Para que mande uno"
    ],
    "m": "Son reglas que se acuerdan entre todos."
  },
  {
    "q": "Si rompés algo sin querer, ¿qué conviene?",
    "ops": [
      "Avisar",
      "Esconderlo",
      "Culpar a otro"
    ],
    "m": "Avisar es hacerse cargo."
  },
  {
    "q": "Cuando alguien está hablando, ¿qué se hace?",
    "ops": [
      "Se escucha y se espera el turno",
      "Se habla más fuerte",
      "Se interrumpe"
    ],
    "m": "Escuchar es parte de conversar."
  },
  {
    "q": "Un chiste del que se ríen todos menos uno es…",
    "ops": [
      "Una burla",
      "Un chiste sin importancia",
      "Divertido"
    ],
    "m": "Lo que importa es cómo se siente esa persona."
  },
  {
    "q": "¿Está bien pedir perdón?",
    "ops": [
      "Sí, es hacerse cargo",
      "No, es de débiles",
      "Sólo si te obligan"
    ],
    "m": "Reconocer el error es lo que repara."
  },
  {
    "q": "Si no estás de acuerdo con alguien, ¿qué hacés?",
    "ops": [
      "Decís lo que pensás sin agredir",
      "Te enojás",
      "No decís nada nunca"
    ],
    "m": "Se pueden discutir las ideas sin lastimar a la persona."
  },
  {
    "q": "¿Todos tienen que jugar a lo mismo?",
    "ops": [
      "No, cada uno puede elegir",
      "Sí",
      "Sólo los grandes eligen"
    ],
    "m": "Respetar lo que le gusta a cada uno."
  },
  {
    "q": "Si ves que alguien necesita ayuda, ¿qué podés hacer?",
    "ops": [
      "Ofrecer ayuda o avisar a un adulto",
      "Nada",
      "Reírte"
    ],
    "m": "No hace falta resolverlo solo: avisar ya ayuda."
  },
  {
    "q": "Cuidar los materiales del aula es…",
    "ops": [
      "Cuidar lo de todos",
      "Perder tiempo",
      "Cosa de la maestra"
    ],
    "m": "Son de uso compartido."
  }
];
GAMES.convivencia_2 = juegoTriviaTexto(CUR_CONVIVENCIA_2_BANCO, "¿Qué conviene hacer?", "convivenci");

/* 1° · Contá las sílabas — silabas_1
   DC: Contar y armar sílabas
   Fuente: docs/auditoria-dc-caba/grado-1.md · L3 */
const CUR_SILABAS_1_BANCO = [
  {
    "q": "«sol»",
    "ops": [
      "1",
      "2",
      "3"
    ],
    "m": "Una sola palma: sol."
  },
  {
    "q": "«casa»",
    "ops": [
      "2",
      "1",
      "3"
    ],
    "m": "ca-sa: dos palmas."
  },
  {
    "q": "«pelota»",
    "ops": [
      "3",
      "2",
      "4"
    ],
    "m": "pe-lo-ta: tres."
  },
  {
    "q": "«mariposa»",
    "ops": [
      "4",
      "3",
      "5"
    ],
    "m": "ma-ri-po-sa: cuatro."
  },
  {
    "q": "«pan»",
    "ops": [
      "1",
      "2",
      "3"
    ],
    "m": "Una."
  },
  {
    "q": "«gato»",
    "ops": [
      "2",
      "1",
      "3"
    ],
    "m": "ga-to."
  },
  {
    "q": "«zapato»",
    "ops": [
      "3",
      "2",
      "4"
    ],
    "m": "za-pa-to."
  },
  {
    "q": "«flor»",
    "ops": [
      "1",
      "2",
      "3"
    ],
    "m": "Una sola."
  },
  {
    "q": "«ventana»",
    "ops": [
      "3",
      "2",
      "4"
    ],
    "m": "ven-ta-na."
  },
  {
    "q": "«sol» y «pan», ¿tienen la misma cantidad?",
    "ops": [
      "Sí, una cada una",
      "No",
      "Sol tiene más"
    ],
    "m": "Las dos son de una sílaba."
  },
  {
    "q": "«mesa»",
    "ops": [
      "2",
      "1",
      "3"
    ],
    "m": "me-sa."
  },
  {
    "q": "«caramelo»",
    "ops": [
      "4",
      "3",
      "5"
    ],
    "m": "ca-ra-me-lo."
  }
];
GAMES.silabas_1 = juegoTriviaTexto(CUR_SILABAS_1_BANCO, "¿Cuántas sílabas tiene? Contalas con palmas.", "silabas_1");

/* 1° · Parejas de letras — parejas_letras_1
   DC: Mayúscula y minúscula de la misma letra
   Fuente: docs/auditoria-dc-caba/grado-1.md · L5 */
const CUR_PAREJAS_LETRAS_1_BANCO = [
  {
    "q": "A",
    "ops": [
      "a",
      "e",
      "o"
    ],
    "m": "La A mayúscula y la a minúscula son la misma letra: la A."
  },
  {
    "q": "M",
    "ops": [
      "m",
      "n",
      "w"
    ],
    "m": "«M» mayúscula y «m» minúscula son la misma letra."
  },
  {
    "q": "S",
    "ops": [
      "s",
      "z",
      "c"
    ],
    "m": "«S» mayúscula y «s» minúscula son la misma letra."
  },
  {
    "q": "P",
    "ops": [
      "p",
      "q",
      "b"
    ],
    "m": "«P» mayúscula y «p» minúscula son la misma letra."
  },
  {
    "q": "E",
    "ops": [
      "e",
      "a",
      "i"
    ],
    "m": "«E» mayúscula y «e» minúscula son la misma letra."
  },
  {
    "q": "L",
    "ops": [
      "l",
      "i",
      "t"
    ],
    "m": "«L» mayúscula y «l» minúscula son la misma letra."
  },
  {
    "q": "T",
    "ops": [
      "t",
      "f",
      "l"
    ],
    "m": "«T» mayúscula y «t» minúscula son la misma letra."
  },
  {
    "q": "O",
    "ops": [
      "o",
      "c",
      "a"
    ],
    "m": "«O» mayúscula y «o» minúscula son la misma letra."
  },
  {
    "q": "D",
    "ops": [
      "d",
      "b",
      "p"
    ],
    "m": "«D» mayúscula y «d» minúscula son la misma letra. Ojo que la «b» y la «d» se parecen mucho."
  },
  {
    "q": "B",
    "ops": [
      "b",
      "d",
      "p"
    ],
    "m": "«B» mayúscula y «b» minúscula son la misma letra."
  },
  {
    "q": "R",
    "ops": [
      "r",
      "n",
      "m"
    ],
    "m": "«R» mayúscula y «r» minúscula son la misma letra."
  },
  {
    "q": "N",
    "ops": [
      "n",
      "m",
      "u"
    ],
    "m": "«N» mayúscula y «n» minúscula son la misma letra."
  }
];
GAMES.parejas_letras_1 = juegoTriviaTexto(CUR_PAREJAS_LETRAS_1_BANCO, "¿Cuál es la misma letra en minúscula (la chiquita)?", "parejas_le");

/* 1° · Despegá las palabras — despegar_palabras_1
   DC: Separación de palabras en la oración
   Fuente: docs/auditoria-dc-caba/grado-1.md · L6 */
const CUR_DESPEGAR_PALABRAS_1_BANCO = [
  {
    "q": "«el gato duerme»",
    "ops": [
      "3",
      "2",
      "4"
    ],
    "m": "el / gato / duerme."
  },
  {
    "q": "«mi mamá canta»",
    "ops": [
      "3",
      "2",
      "4"
    ],
    "m": "mi / mamá / canta."
  },
  {
    "q": "«hay sol»",
    "ops": [
      "2",
      "1",
      "3"
    ],
    "m": "hay / sol."
  },
  {
    "q": "«la nena come pan»",
    "ops": [
      "4",
      "3",
      "5"
    ],
    "m": "la / nena / come / pan."
  },
  {
    "q": "«corro»",
    "ops": [
      "1",
      "2",
      "3"
    ],
    "m": "Una sola palabra."
  },
  {
    "q": "«el perro ladra»",
    "ops": [
      "3",
      "2",
      "4"
    ],
    "m": "el / perro / ladra."
  },
  {
    "q": "«vamos a jugar»",
    "ops": [
      "3",
      "2",
      "4"
    ],
    "m": "vamos / a / jugar. La 'a' también cuenta."
  },
  {
    "q": "«llueve mucho»",
    "ops": [
      "2",
      "1",
      "3"
    ],
    "m": "llueve / mucho."
  },
  {
    "q": "«me gusta el helado»",
    "ops": [
      "4",
      "3",
      "5"
    ],
    "m": "me / gusta / el / helado."
  },
  {
    "q": "¿Cómo se sabe dónde termina una palabra?",
    "ops": [
      "Por el espacio en blanco",
      "Por el tamaño",
      "Por la primera letra"
    ],
    "m": "El espacio separa una palabra de la otra."
  },
  {
    "q": "«la casa es grande»",
    "ops": [
      "4",
      "3",
      "5"
    ],
    "m": "la / casa / es / grande."
  },
  {
    "q": "«sí»",
    "ops": [
      "1",
      "2",
      "3"
    ],
    "m": "Una."
  }
];
GAMES.despegar_palabras_1 = juegoTriviaTexto(CUR_DESPEGAR_PALABRAS_1_BANCO, "¿Cuántas palabras hay?", "despegar_p");

/* 1° · Mayúscula y punto — mayuscula_punto_1
   DC: Mayúscula inicial y punto final
   Fuente: docs/auditoria-dc-caba/grado-1.md · L7 */
const CUR_MAYUSCULA_PUNTO_1_BANCO = [
  {
    "q": "¿Con qué empieza una oración?",
    "ops": [
      "Con mayúscula",
      "Con minúscula",
      "Con un número"
    ],
    "m": "La primera letra va grande."
  },
  {
    "q": "¿Con qué termina?",
    "ops": [
      "Con un punto",
      "Con una coma",
      "Con nada"
    ],
    "m": "El punto cierra la idea."
  },
  {
    "q": "¿Cuál está bien?",
    "ops": [
      "El gato duerme.",
      "el gato duerme.",
      "El gato duerme"
    ],
    "m": "Mayúscula al empezar y punto al final."
  },
  {
    "q": "¿Cuál está bien escrita?",
    "ops": [
      "Hoy llueve.",
      "hoy llueve",
      "Hoy llueve"
    ],
    "m": "Las dos cosas: mayúscula y punto."
  },
  {
    "q": "Los nombres de personas, ¿cómo van?",
    "ops": [
      "Con mayúscula",
      "Con minúscula",
      "Con punto"
    ],
    "m": "Ana, Luis, Sofía: siempre con mayúscula."
  },
  {
    "q": "«mi hermana se llama ___»",
    "ops": [
      "Ana",
      "ana",
      "ANA"
    ],
    "m": "Nombre propio."
  },
  {
    "q": "Después de un punto, la palabra que sigue va…",
    "ops": [
      "Con mayúscula",
      "Con minúscula",
      "Igual"
    ],
    "m": "Empieza una oración nueva."
  },
  {
    "q": "¿Cuál de estas está bien?",
    "ops": [
      "Vamos al parque.",
      "vamos al parque.",
      "Vamos al parque"
    ],
    "m": "Mayúscula y punto."
  },
  {
    "q": "¿La palabra «perro» lleva mayúscula?",
    "ops": [
      "No, salvo que empiece la oración",
      "Sí, siempre",
      "Nunca"
    ],
    "m": "Es un nombre común."
  },
  {
    "q": "¿Y el nombre de tu ciudad?",
    "ops": [
      "Sí, con mayúscula",
      "No",
      "A veces"
    ],
    "m": "Es un nombre propio."
  },
  {
    "q": "¿Cuántos puntos lleva una oración?",
    "ops": [
      "Uno, al final",
      "Varios",
      "Ninguno"
    ],
    "m": "Uno cierra la oración."
  },
  {
    "q": "Y de estas, ¿cuál está bien?",
    "ops": [
      "Me gusta el sol.",
      "me gusta el sol",
      "Me gusta el sol"
    ],
    "m": "Mayúscula y punto."
  }
];
GAMES.mayuscula_punto_1 = juegoTriviaTexto(CUR_MAYUSCULA_PUNTO_1_BANCO, "¿Cómo se escribe bien?", "mayuscula_");

/* 1° · Leé y encontrá — leer_encontrar_1
   DC: Decodificación: leer sin apoyo de audio
   Fuente: docs/auditoria-dc-caba/grado-1.md · L8 */
const CUR_LEER_ENCONTRAR_1_BANCO = [
  {
    "q": "¿Cuál dice «casa»?",
    "ops": [
      "casa",
      "cosa",
      "caza"
    ],
    "m": "ca-sa."
  },
  {
    "q": "¿Cuál dice «pato»?",
    "ops": [
      "pato",
      "gato",
      "pata"
    ],
    "m": "pa-to."
  },
  {
    "q": "¿Cuál dice «sol»?",
    "ops": [
      "sol",
      "sal",
      "sil"
    ],
    "m": "sol."
  },
  {
    "q": "¿Cuál dice «mesa»?",
    "ops": [
      "mesa",
      "misa",
      "masa"
    ],
    "m": "me-sa."
  },
  {
    "q": "¿Cuál dice «pelota»?",
    "ops": [
      "pelota",
      "paleta",
      "pileta"
    ],
    "m": "pe-lo-ta."
  },
  {
    "q": "¿Cuál dice «mamá»?",
    "ops": [
      "mamá",
      "mano",
      "mapa"
    ],
    "m": "ma-má."
  },
  {
    "q": "¿Cuál dice «perro»?",
    "ops": [
      "perro",
      "pero",
      "parro"
    ],
    "m": "pe-rro, con dos R."
  },
  {
    "q": "¿Cuál dice «luna»?",
    "ops": [
      "luna",
      "lupa",
      "lana"
    ],
    "m": "lu-na."
  },
  {
    "q": "¿Cuál dice «flor»?",
    "ops": [
      "flor",
      "flan",
      "fror"
    ],
    "m": "flor."
  },
  {
    "q": "¿Cuál dice «nene»?",
    "ops": [
      "nene",
      "nena",
      "nube"
    ],
    "m": "ne-ne."
  },
  {
    "q": "¿Cuál dice «pan»?",
    "ops": [
      "pan",
      "pon",
      "pin"
    ],
    "m": "pan."
  },
  {
    "q": "¿Cuál dice «gato»?",
    "ops": [
      "gato",
      "pato",
      "gota"
    ],
    "m": "ga-to."
  }
];
GAMES.leer_encontrar_1 = juegoTriviaTexto(CUR_LEER_ENCONTRAR_1_BANCO, "Leé y elegí.", "leer_encon");

/* 1° · Leo y respondo — leo_respondo_1
   DC: Comprensión de textos breves
   Fuente: docs/auditoria-dc-caba/grado-1.md · L9 */
const CUR_LEO_RESPONDO_1_BANCO = [
  {
    "q": "«El gato duerme en la cama.» ¿Dónde duerme?",
    "ops": [
      "En la cama",
      "En el patio",
      "En la silla"
    ],
    "m": "Lo dice el texto."
  },
  {
    "q": "«Ana come una manzana.» ¿Qué come?",
    "ops": [
      "Una manzana",
      "Una pera",
      "Pan"
    ],
    "m": "Está escrito."
  },
  {
    "q": "«Llueve y Luis abre el paraguas.» ¿Por qué lo abre?",
    "ops": [
      "Porque llueve",
      "Porque hace calor",
      "Porque es de noche"
    ],
    "m": "Lo primero explica lo segundo."
  },
  {
    "q": "«El perro corre en la plaza.» ¿Quién corre?",
    "ops": [
      "El perro",
      "El nene",
      "La plaza"
    ],
    "m": "El que hace la acción."
  },
  {
    "q": "«Sofía riega la planta todos los días.» ¿Cada cuánto?",
    "ops": [
      "Todos los días",
      "Una vez",
      "Nunca"
    ],
    "m": "Lo dice el texto."
  },
  {
    "q": "«Hace frío. Nico se pone la campera.» ¿Por qué se la pone?",
    "ops": [
      "Porque hace frío",
      "Porque llueve",
      "Porque va a dormir"
    ],
    "m": "La causa está en la primera oración."
  },
  {
    "q": "«La maestra lee un cuento.» ¿Qué lee?",
    "ops": [
      "Un cuento",
      "Un diario",
      "Una carta"
    ],
    "m": "Está escrito."
  },
  {
    "q": "«El sol brilla y los chicos juegan.» ¿Cómo está el día?",
    "ops": [
      "Soleado",
      "Lluvioso",
      "Nublado"
    ],
    "m": "Si el sol brilla, está soleado."
  },
  {
    "q": "«Papá cocina fideos.» ¿Quién cocina?",
    "ops": [
      "Papá",
      "Mamá",
      "El nene"
    ],
    "m": "El que hace la acción."
  },
  {
    "q": "«El bebé llora porque tiene hambre.» ¿Por qué llora?",
    "ops": [
      "Tiene hambre",
      "Tiene sueño",
      "Tiene frío"
    ],
    "m": "El 'porque' te da la razón."
  },
  {
    "q": "«Vamos a la playa en verano.» ¿Cuándo van?",
    "ops": [
      "En verano",
      "En invierno",
      "Nunca"
    ],
    "m": "Está escrito."
  },
  {
    "q": "«El pájaro hace su nido en el árbol.» ¿Dónde lo hace?",
    "ops": [
      "En el árbol",
      "En el suelo",
      "En la casa"
    ],
    "m": "Está escrito."
  }
];
GAMES.leo_respondo_1 = juegoTriviaTexto(CUR_LEO_RESPONDO_1_BANCO, "Leé y contestá.", "leo_respon");

/* 1° · Ordená el cuento — ordenar_cuento_1
   DC: Secuencia narrativa
   Fuente: docs/auditoria-dc-caba/grado-1.md · L10 */
const CUR_ORDENAR_CUENTO_1_BANCO = [
  {
    "items": [
      "El nene se despierta",
      "Desayuna",
      "Va a la escuela"
    ]
  },
  {
    "items": [
      "Plantan la semilla",
      "La riegan",
      "Nace la flor"
    ]
  },
  {
    "items": [
      "El gato tiene hambre",
      "Maúlla",
      "Le dan comida"
    ]
  },
  {
    "items": [
      "Se ensucia las manos",
      "Se las lava",
      "Quedan limpias"
    ]
  },
  {
    "items": [
      "Empieza a llover",
      "Abren el paraguas",
      "Se mojan menos"
    ]
  },
  {
    "items": [
      "Juntan los ingredientes",
      "Hacen la torta",
      "La comen"
    ]
  },
  {
    "items": [
      "Se rompe el juguete",
      "Lo arreglan",
      "Vuelven a jugar"
    ]
  },
  {
    "items": [
      "Sale el sol",
      "Los chicos van a la plaza",
      "Juegan a la pelota"
    ]
  },
  {
    "items": [
      "El perro se pierde",
      "Lo buscan",
      "Lo encuentran"
    ]
  },
  {
    "items": [
      "Se hace de noche",
      "El nene se acuesta",
      "Se duerme"
    ]
  }
];
GAMES.ordenar_cuento_1 = juegoOrdenar(CUR_ORDENAR_CUENTO_1_BANCO, "Ordená lo que pasó. Tocá en orden.", "Pensá qué pasó primero de todo.", "ordenar_cu");

/* 1° · El, la, los, las — articulos_1
   DC: Artículos y concordancia
   Fuente: docs/auditoria-dc-caba/grado-1.md · L13 */
const CUR_ARTICULOS_1_BANCO = [
  {
    "q": "___ gato",
    "ops": [
      "el",
      "la",
      "las"
    ],
    "m": "Gato es uno y masculino: el."
  },
  {
    "q": "___ casa",
    "ops": [
      "la",
      "el",
      "los"
    ],
    "m": "Casa es una y femenina: la."
  },
  {
    "q": "___ gatos",
    "ops": [
      "los",
      "el",
      "la"
    ],
    "m": "Son varios y masculinos: los."
  },
  {
    "q": "___ casas",
    "ops": [
      "las",
      "la",
      "el"
    ],
    "m": "Son varias y femeninas: las."
  },
  {
    "q": "___ sol",
    "ops": [
      "el",
      "la",
      "las"
    ],
    "m": "El sol."
  },
  {
    "q": "___ luna",
    "ops": [
      "la",
      "el",
      "los"
    ],
    "m": "La luna."
  },
  {
    "q": "___ nenes",
    "ops": [
      "los",
      "el",
      "las"
    ],
    "m": "Varios."
  },
  {
    "q": "___ flores",
    "ops": [
      "las",
      "la",
      "el"
    ],
    "m": "Varias y femeninas."
  },
  {
    "q": "___ pan",
    "ops": [
      "el",
      "la",
      "los"
    ],
    "m": "El pan."
  },
  {
    "q": "___ mesa",
    "ops": [
      "la",
      "el",
      "los"
    ],
    "m": "La mesa."
  },
  {
    "q": "___ perros",
    "ops": [
      "los",
      "la",
      "el"
    ],
    "m": "Varios."
  },
  {
    "q": "___ manos",
    "ops": [
      "las",
      "los",
      "el"
    ],
    "m": "Manos es femenino: las manos."
  }
];
GAMES.articulos_1 = juegoTriviaTexto(CUR_ARTICULOS_1_BANCO, "¿Qué palabrita va adelante?", "articulos_");

/* 1° · El kiosco — kiosco_1
   DC: Componer una cantidad con monedas
   Fuente: docs/auditoria-dc-caba/grado-1.md · M3 */
const CUR_KIOSCO_1_PIEZAS = {
  "piezas": [
    1,
    2,
    5,
    10,
    20,
    50
  ],
  "cuantas": 2,
  "unidad": "$",
  "m": "Fijate cuánto te falta y buscá una moneda de ese valor."
};
GAMES.kiosco_1 = juegoManipular(CUR_KIOSCO_1_PIEZAS, "Tocá las monedas que suman el precio.", "kiosco_1");

/* 1° · Parejas que suman 10 — parejas_diez_1
   DC: Repertorio de sumas que dan 10 y 100
   Fuente: docs/auditoria-dc-caba/grado-1.md · M5 */
const CUR_PAREJAS_DIEZ_1_PIEZAS = {
  "piezas": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9
  ],
  "cuantas": 2,
  "unidad": "",
  "m": "Contá con los dedos cuánto le falta al primero."
};
GAMES.parejas_diez_1 = juegoManipular(CUR_PAREJAS_DIEZ_1_PIEZAS, "Tocá los dos números que suman el total.", "parejas_di");

/* 1° · Armá el cálculo — armar_calculo_1
   DC: Componer el cálculo que resuelve el problema
   Fuente: docs/auditoria-dc-caba/grado-1.md · M8 */
const CUR_ARMAR_CALCULO_1_BANCO = [
  {
    "q": "Tenía 5 figuritas y le dieron 3. ¿Qué cuenta hacés?",
    "ops": [
      "5 + 3",
      "5 − 3",
      "3 − 5"
    ],
    "m": "Le dieron más: se suma."
  },
  {
    "q": "Tenía 8 caramelos y comió 2. ¿Qué cuenta?",
    "ops": [
      "8 − 2",
      "8 + 2",
      "2 − 8"
    ],
    "m": "Comió: se quita."
  },
  {
    "q": "Hay 4 nenes y llegan 2 más. ¿Qué cuenta?",
    "ops": [
      "4 + 2",
      "4 − 2",
      "2 − 4"
    ],
    "m": "Llegan más: se suma."
  },
  {
    "q": "Tenía 10 globos y se le escaparon 3. ¿Qué cuenta?",
    "ops": [
      "10 − 3",
      "10 + 3",
      "3 − 10"
    ],
    "m": "Se escaparon: se resta."
  },
  {
    "q": "Junté 6 piedritas y después 4 más. ¿Qué cuenta?",
    "ops": [
      "6 + 4",
      "6 − 4",
      "4 − 6"
    ],
    "m": "Junté más."
  },
  {
    "q": "En el colectivo había 9 y bajaron 5. ¿Qué cuenta?",
    "ops": [
      "9 − 5",
      "9 + 5",
      "5 − 9"
    ],
    "m": "Bajaron: quedan menos."
  },
  {
    "q": "Tenía 7 y ahora tiene 10. ¿Cuántos le dieron?",
    "ops": [
      "10 − 7",
      "10 + 7",
      "7 − 10"
    ],
    "m": "Para saber cuánto se agregó, se resta."
  },
  {
    "q": "Hay 3 en una caja y 5 en otra. ¿Cuántos hay?",
    "ops": [
      "3 + 5",
      "5 − 3",
      "3 − 5"
    ],
    "m": "Se juntan las dos cajas."
  },
  {
    "q": "Tenía 12 y regaló 4. ¿Qué cuenta?",
    "ops": [
      "12 − 4",
      "12 + 4",
      "4 − 12"
    ],
    "m": "Regaló: se va."
  },
  {
    "q": "«Le dieron», «llegaron», «juntó» son palabras de…",
    "ops": [
      "Sumar",
      "Restar",
      "Ninguna"
    ],
    "m": "Todas indican que hay más."
  },
  {
    "q": "«Comió», «perdió», «bajaron» son palabras de…",
    "ops": [
      "Restar",
      "Sumar",
      "Ninguna"
    ],
    "m": "Todas indican que hay menos."
  },
  {
    "q": "Tenía 6, le dieron 2 y perdió 1. ¿Cuántas cuentas hacés?",
    "ops": [
      "Dos",
      "Una",
      "Ninguna"
    ],
    "m": "Primero sumás y después restás."
  }
];
GAMES.armar_calculo_1 = juegoTriviaTexto(CUR_ARMAR_CALCULO_1_BANCO, "¿Qué cuenta resuelve el problema?", "armar_calc");

/* 1° · ¿Dónde está? — donde_esta_1
   DC: Ubicación espacial: arriba, abajo, entre
   Fuente: docs/auditoria-dc-caba/grado-1.md · M10 */
const CUR_DONDE_ESTA_1_BANCO = [
  {
    "q": "El pájaro vuela ___ del árbol.",
    "ops": [
      "arriba",
      "abajo",
      "adentro"
    ],
    "m": "Los pájaros vuelan por encima."
  },
  {
    "q": "El pez nada ___ del agua.",
    "ops": [
      "adentro",
      "arriba",
      "atrás"
    ],
    "m": "En el agua."
  },
  {
    "q": "Si estoy ENTRE dos amigos, tengo…",
    "ops": [
      "Uno a cada lado",
      "Los dos adelante",
      "Ninguno"
    ],
    "m": "Entre es en el medio."
  },
  {
    "q": "El techo está ___ de la casa.",
    "ops": [
      "arriba",
      "abajo",
      "al lado"
    ],
    "m": "En lo alto."
  },
  {
    "q": "El piso está ___ de nuestros pies.",
    "ops": [
      "abajo",
      "arriba",
      "adelante"
    ],
    "m": "Lo pisamos."
  },
  {
    "q": "Si el gato está DEBAJO de la mesa, la mesa está…",
    "ops": [
      "Arriba del gato",
      "Debajo",
      "Al lado"
    ],
    "m": "Es la misma relación al revés."
  },
  {
    "q": "La puerta está ___ de la pared.",
    "ops": [
      "en el medio",
      "arriba",
      "abajo"
    ],
    "m": "Está en la pared."
  },
  {
    "q": "Si camino ADELANTE, dejo la puerta…",
    "ops": [
      "Atrás",
      "Adelante",
      "Arriba"
    ],
    "m": "Lo que pasás queda atrás."
  },
  {
    "q": "El sol está ___ de las nubes cuando el cielo está limpio.",
    "ops": [
      "arriba",
      "abajo",
      "adentro"
    ],
    "m": "Muy arriba."
  },
  {
    "q": "Las raíces están ___ de la tierra.",
    "ops": [
      "abajo",
      "arriba",
      "al lado"
    ],
    "m": "Bajo tierra."
  },
  {
    "q": "Si pongo un libro SOBRE otro, el de abajo queda…",
    "ops": [
      "Debajo",
      "Arriba",
      "Al lado"
    ],
    "m": "Uno tapa al otro."
  },
  {
    "q": "Estar CERCA es lo contrario de…",
    "ops": [
      "Lejos",
      "Arriba",
      "Adentro"
    ],
    "m": "Cerca y lejos son opuestos."
  }
];
GAMES.donde_esta_1 = juegoTriviaTexto(CUR_DONDE_ESTA_1_BANCO, "Mirá dónde está cada cosa.", "donde_esta");

/* 1° · Detective de figuras — figuras_1
   DC: Figuras: lados y vértices
   Fuente: docs/auditoria-dc-caba/grado-1.md · M11 */
const CUR_FIGURAS_1_BANCO = [
  {
    "q": "¿Cuántos lados tiene un triángulo?",
    "ops": [
      "3",
      "4",
      "5"
    ],
    "m": "Tri es tres.",
    "dib": "triangulo"
  },
  {
    "q": "¿Y un cuadrado?",
    "ops": [
      "4",
      "3",
      "5"
    ],
    "m": "Cuatro lados iguales.",
    "dib": "cuadrado"
  },
  {
    "q": "¿Cuántas puntas tiene un triángulo?",
    "ops": [
      "3",
      "4",
      "2"
    ],
    "m": "Tantas puntas como lados.",
    "dib": "triangulo"
  },
  {
    "q": "¿Cuántos lados tiene un círculo?",
    "ops": [
      "Ninguno, es todo curvo",
      "4",
      "1"
    ],
    "m": "No tiene lados rectos ni puntas.",
    "dib": "circulo"
  },
  {
    "q": "Un cuadrado tiene los cuatro lados…",
    "ops": [
      "Iguales",
      "Distintos",
      "Curvos"
    ],
    "m": "Todos del mismo largo.",
    "dib": "cuadrado"
  },
  {
    "q": "Un rectángulo tiene…",
    "ops": [
      "4 lados, dos largos y dos cortos",
      "3 lados",
      "Ninguno"
    ],
    "m": "Los de enfrente son iguales.",
    "dib": "rectangulo"
  },
  {
    "q": "¿Cuántas puntas tiene un cuadrado?",
    "ops": [
      "4",
      "3",
      "5"
    ],
    "m": "Cuatro esquinas.",
    "dib": "cuadrado"
  },
  {
    "q": "Un cuadrado apoyado en una punta, ¿sigue siendo cuadrado?",
    "ops": [
      "Sí",
      "No, es un triángulo",
      "No, es un círculo"
    ],
    "m": "Girarlo no lo cambia.",
    "dib": "rombo"
  },
  {
    "q": "La rueda tiene forma de…",
    "ops": [
      "Círculo",
      "Cuadrado",
      "Triángulo"
    ],
    "m": "Es redonda.",
    "dib": "rueda"
  },
  {
    "q": "¿Qué figura tiene la puerta?",
    "ops": [
      "Rectángulo",
      "Círculo",
      "Triángulo"
    ],
    "m": "Cuatro lados, dos largos y dos cortos.",
    "dib": "puerta"
  },
  {
    "q": "¿Cuántos lados tiene esta figura si tiene 5 puntas?",
    "ops": [
      "5",
      "4",
      "6"
    ],
    "m": "Tantos lados como puntas.",
    "dib": "pentagono"
  },
  {
    "q": "El techo de una casita dibujada suele ser un…",
    "ops": [
      "Triángulo",
      "Círculo",
      "Cuadrado"
    ],
    "m": "Tres lados.",
    "dib": "casita"
  }
];
GAMES.figuras_1 = juegoTriviaTexto(CUR_FIGURAS_1_BANCO, "Contá los lados y las puntas.", "figuras_1");

/* 1° · Caras y cuerpos — cuerpos_1
   DC: Cuerpos geométricos y objetos cotidianos
   Fuente: docs/auditoria-dc-caba/grado-1.md · M12 */
const CUR_CUERPOS_1_BANCO = [
  {
    "q": "Un dado tiene forma de…",
    "ops": [
      "Cubo",
      "Esfera",
      "Cono"
    ],
    "m": "Seis caras cuadradas."
  },
  {
    "q": "Una pelota tiene forma de…",
    "ops": [
      "Esfera",
      "Cubo",
      "Cilindro"
    ],
    "m": "Es toda redonda."
  },
  {
    "q": "Una lata de tomate tiene forma de…",
    "ops": [
      "Cilindro",
      "Cubo",
      "Esfera"
    ],
    "m": "Dos tapas redondas y el costado curvo."
  },
  {
    "q": "Un cucurucho de helado tiene forma de…",
    "ops": [
      "Cono",
      "Cubo",
      "Cilindro"
    ],
    "m": "Termina en punta."
  },
  {
    "q": "¿Cuántas caras tiene un cubo?",
    "ops": [
      "6",
      "4",
      "8"
    ],
    "m": "Seis, todas cuadradas."
  },
  {
    "q": "¿Qué cuerpo rueda?",
    "ops": [
      "La esfera",
      "El cubo",
      "La caja"
    ],
    "m": "Todo redondo: rueda para cualquier lado."
  },
  {
    "q": "¿Qué cuerpo NO rueda?",
    "ops": [
      "El cubo",
      "La pelota",
      "La lata"
    ],
    "m": "Tiene caras planas: se queda quieto."
  },
  {
    "q": "Una caja de zapatos tiene forma de…",
    "ops": [
      "Prisma",
      "Esfera",
      "Cono"
    ],
    "m": "Como un cubo pero estirado."
  },
  {
    "q": "Las caras del cubo son…",
    "ops": [
      "Cuadrados",
      "Círculos",
      "Triángulos"
    ],
    "m": "Seis cuadrados iguales."
  },
  {
    "q": "La lata, ¿rueda?",
    "ops": [
      "Sí, para un solo lado",
      "No",
      "Sí, para todos lados"
    ],
    "m": "Rueda de costado, pero apoyada en la tapa no."
  },
  {
    "q": "¿Qué se puede apilar mejor?",
    "ops": [
      "Los cubos",
      "Las pelotas",
      "Los conos"
    ],
    "m": "Las caras planas se apoyan."
  },
  {
    "q": "La Luna se parece a…",
    "ops": [
      "Una esfera",
      "Un cubo",
      "Un cono"
    ],
    "m": "Es redonda."
  }
];
GAMES.cuerpos_1 = juegoTriviaTexto(CUR_CUERPOS_1_BANCO, "¿A qué se parece?", "cuerpos_1");

/* 1° · Medí con clips — medir_clips_1
   DC: Medición con unidades no convencionales
   Fuente: docs/auditoria-dc-caba/grado-1.md · M13 */
const CUR_MEDIR_CLIPS_1_BANCO = [
  {
    "q": "Un lápiz entra 5 veces en la mesa. La mesa mide…",
    "ops": [
      "5 lápices",
      "5 cm",
      "1 lápiz"
    ],
    "m": "Se mide en la unidad que usaste."
  },
  {
    "q": "Si medís con clips chiquitos, ¿te dan más o menos que con clips grandes?",
    "ops": [
      "Más",
      "Menos",
      "Igual"
    ],
    "m": "Cuanto más chica la unidad, más veces entra."
  },
  {
    "q": "El banco mide 8 manos. Con manos más grandes daría…",
    "ops": [
      "Menos manos",
      "Más manos",
      "Lo mismo"
    ],
    "m": "Cada mano cubre más."
  },
  {
    "q": "¿Por qué conviene usar siempre la misma unidad?",
    "ops": [
      "Para poder comparar",
      "Para que sea más rápido",
      "Para que quede lindo"
    ],
    "m": "Si cada uno mide con su mano, nadie se entiende."
  },
  {
    "q": "Para medir, ¿los clips tienen que estar…?",
    "ops": [
      "Uno pegado al otro, sin huecos",
      "Separados",
      "Encimados"
    ],
    "m": "Sin huecos ni superposiciones."
  },
  {
    "q": "Si el libro mide 4 clips y el cuaderno 6, ¿cuál es más largo?",
    "ops": [
      "El cuaderno",
      "El libro",
      "Son iguales"
    ],
    "m": "Más clips, más largo."
  },
  {
    "q": "Empezaste a medir desde la mitad del objeto. La medida…",
    "ops": [
      "Va a dar mal",
      "Va a dar bien",
      "Da igual"
    ],
    "m": "Hay que empezar desde la punta."
  },
  {
    "q": "¿Qué unidad conviene para medir el aula?",
    "ops": [
      "Pasos",
      "Clips",
      "Botones"
    ],
    "m": "Para algo grande, una unidad grande."
  },
  {
    "q": "¿Y para medir una goma?",
    "ops": [
      "Clips",
      "Pasos",
      "Baldosas"
    ],
    "m": "Para algo chico, una unidad chica."
  },
  {
    "q": "Dos chicos midieron la misma mesa y les dio distinto. ¿Por qué?",
    "ops": [
      "Usaron unidades distintas",
      "La mesa cambió",
      "Uno se equivocó seguro"
    ],
    "m": "Con unidades distintas, números distintos."
  },
  {
    "q": "La puerta mide 6 baldosas y la ventana 3. La puerta es…",
    "ops": [
      "El doble de larga",
      "Más corta",
      "Igual"
    ],
    "m": "6 es el doble de 3."
  },
  {
    "q": "¿Se puede medir con el pie?",
    "ops": [
      "Sí, pero cada pie es distinto",
      "No",
      "Sí, y todos dan igual"
    ],
    "m": "Por eso después se inventaron el metro y el centímetro."
  }
];
GAMES.medir_clips_1 = juegoTriviaTexto(CUR_MEDIR_CLIPS_1_BANCO, "¿Cuánto mide?", "medir_clip");

/* 1° · El calendario — calendario_1
   DC: Días, semanas y meses
   Fuente: docs/auditoria-dc-caba/grado-1.md · M14 */
const CUR_CALENDARIO_1_BANCO = [
  {
    "q": "¿Cuántos días tiene una semana?",
    "ops": [
      "7",
      "5",
      "10"
    ],
    "m": "Siete."
  },
  {
    "q": "¿Qué día viene después del lunes?",
    "ops": [
      "Martes",
      "Domingo",
      "Viernes"
    ],
    "m": "Lunes, martes, miércoles…"
  },
  {
    "q": "¿Qué día viene antes del sábado?",
    "ops": [
      "Viernes",
      "Domingo",
      "Lunes"
    ],
    "m": "Viernes, sábado, domingo."
  },
  {
    "q": "¿Cuántos meses tiene el año?",
    "ops": [
      "12",
      "10",
      "7"
    ],
    "m": "Doce."
  },
  {
    "q": "¿Cuál es el primer mes del año?",
    "ops": [
      "Enero",
      "Diciembre",
      "Marzo"
    ],
    "m": "Enero abre el año."
  },
  {
    "q": "¿Y el último?",
    "ops": [
      "Diciembre",
      "Enero",
      "Noviembre"
    ],
    "m": "Diciembre lo cierra."
  },
  {
    "q": "¿Qué días no se va a la escuela?",
    "ops": [
      "Sábado y domingo",
      "Lunes y martes",
      "Ninguno"
    ],
    "m": "El fin de semana."
  },
  {
    "q": "Si hoy es miércoles, mañana es…",
    "ops": [
      "Jueves",
      "Martes",
      "Viernes"
    ],
    "m": "El que sigue."
  },
  {
    "q": "Si hoy es martes, ayer fue…",
    "ops": [
      "Lunes",
      "Miércoles",
      "Domingo"
    ],
    "m": "El anterior."
  },
  {
    "q": "¿En qué mes empiezan las clases en Argentina?",
    "ops": [
      "Marzo",
      "Enero",
      "Julio"
    ],
    "m": "Después del verano."
  },
  {
    "q": "Si tu cumpleaños es el 8 y hoy es 5, ¿cuántos días faltan?",
    "ops": [
      "3",
      "5",
      "8"
    ],
    "m": "8 − 5."
  },
  {
    "q": "¿Cuántas semanas tiene más o menos un mes?",
    "ops": [
      "4",
      "2",
      "10"
    ],
    "m": "Cuatro semanas de 7 días son 28."
  }
];
GAMES.calendario_1 = juegoTriviaTexto(CUR_CALENDARIO_1_BANCO, "Mirá el calendario.", "calendario");

/* 1° · Cuidarnos — cuidarnos_1
   DC: Cuidado del cuerpo; a quién acudir
   Fuente: docs/auditoria-dc-caba/grado-1.md · C8 */
const CUR_CUIDARNOS_1_BANCO = [
  {
    "q": "Antes de comer conviene…",
    "ops": [
      "Lavarse las manos",
      "Correr",
      "Mirar la tele"
    ],
    "m": "Las manos traen microbios que no se ven."
  },
  {
    "q": "Si te sentís mal, ¿a quién le avisás?",
    "ops": [
      "A un adulto de confianza",
      "A nadie",
      "Al que pase"
    ],
    "m": "Contarlo es lo que te ayuda."
  },
  {
    "q": "¿Cuántas veces por día conviene lavarse los dientes?",
    "ops": [
      "Después de cada comida",
      "Una vez por semana",
      "Nunca"
    ],
    "m": "Sobre todo antes de dormir."
  },
  {
    "q": "Jugar sin parar todo el día es…",
    "ops": [
      "Demasiado: también hay que descansar",
      "Perfecto",
      "Obligatorio"
    ],
    "m": "Jugar está buenísimo, y dormir también hace falta."
  },
  {
    "q": "¿Cuántas horas conviene dormir a tu edad?",
    "ops": [
      "Unas 10",
      "3",
      "20"
    ],
    "m": "Dormir es cuando el cuerpo crece y descansa."
  },
  {
    "q": "Si te lastimás en el recreo, ¿qué hacés?",
    "ops": [
      "Avisás a la maestra",
      "Seguís jugando",
      "Te escondés"
    ],
    "m": "Un adulto puede curarte."
  },
  {
    "q": "¿Para qué sirve tomar agua?",
    "ops": [
      "El cuerpo la necesita todo el día",
      "Sólo si hace calor",
      "Para nada"
    ],
    "m": "Es lo que más conviene tomar."
  },
  {
    "q": "Si alguien te toca y no te gusta, ¿qué hacés?",
    "ops": [
      "Decís que no y avisás a un adulto",
      "Te callás",
      "Te vas sin decir nada"
    ],
    "m": "Tu cuerpo es tuyo. Decir que no está bien, y contarlo también."
  },
  {
    "q": "¿Quién puede ayudarte en la escuela?",
    "ops": [
      "La maestra o la directora",
      "Nadie",
      "Sólo tu mamá"
    ],
    "m": "Hay adultos a cargo de cuidarte ahí también."
  },
  {
    "q": "¿Hay que hacer actividad física?",
    "ops": [
      "Sí, jugar y moverse hace bien",
      "No",
      "Sólo los grandes"
    ],
    "m": "Correr y saltar también es cuidarse."
  },
  {
    "q": "Si un compañero se lastima, ¿qué hacés?",
    "ops": [
      "Avisás a un adulto",
      "Te reís",
      "No hacés nada"
    ],
    "m": "Avisar ya es ayudar."
  },
  {
    "q": "¿Para qué sirve ir al médico si no estás enfermo?",
    "ops": [
      "Para controlar que estés bien",
      "Para nada",
      "Sólo para las vacunas"
    ],
    "m": "El control evita problemas."
  }
];
GAMES.cuidarnos_1 = juegoTriviaTexto(CUR_CUIDARNOS_1_BANCO, "¿Qué conviene hacer?", "cuidarnos_");

/* 1° · Pasos en orden — pasos_orden_1
   DC: Secuencia de pasos y detección del intruso
   Fuente: docs/auditoria-dc-caba/grado-1.md · T2 */
const CUR_PASOS_ORDEN_1_BANCO = [
  {
    "items": [
      "Agarrar el vaso",
      "Servir el agua",
      "Tomar"
    ]
  },
  {
    "items": [
      "Sacar el pan",
      "Untar la manteca",
      "Comer"
    ]
  },
  {
    "items": [
      "Ponerse las medias",
      "Ponerse las zapatillas",
      "Atarse los cordones"
    ]
  },
  {
    "items": [
      "Abrir la mochila",
      "Sacar el cuaderno",
      "Escribir"
    ]
  },
  {
    "items": [
      "Mojarse las manos",
      "Poner jabón",
      "Enjuagarse",
      "Secarse"
    ]
  },
  {
    "items": [
      "Prender la luz",
      "Buscar el libro",
      "Leer"
    ]
  },
  {
    "items": [
      "Ponerse el pijama",
      "Lavarse los dientes",
      "Acostarse"
    ]
  },
  {
    "items": [
      "Juntar los juguetes",
      "Guardarlos en la caja",
      "Cerrar la caja"
    ]
  },
  {
    "items": [
      "Sacar la basura de casa",
      "Llevarla al contenedor",
      "Volver"
    ]
  },
  {
    "items": [
      "Regar la planta",
      "Esperar unos días",
      "Ver el brote"
    ]
  }
];
GAMES.pasos_orden_1 = juegoOrdenar(CUR_PASOS_ORDEN_1_BANCO, "Ordená los pasos. Tocá en orden.", "Pensá qué hay que hacer primero para poder seguir.", "pasos_orde");

/* 1° · Herramientas y oficios — oficios_1
   DC: Herramientas, tareas y oficios
   Fuente: docs/auditoria-dc-caba/grado-1.md · T3 */
const CUR_OFICIOS_1_BANCO = [
  {
    "q": "El martillo lo usa…",
    "ops": [
      "La carpintera",
      "La cocinera",
      "El médico"
    ],
    "m": "Sirve para clavar la madera."
  },
  {
    "q": "El estetoscopio lo usa…",
    "ops": [
      "El médico",
      "El panadero",
      "La maestra"
    ],
    "m": "Sirve para escuchar el corazón."
  },
  {
    "q": "La cuchara de madera la usa…",
    "ops": [
      "El cocinero",
      "La electricista",
      "El chofer"
    ],
    "m": "Para revolver la comida."
  },
  {
    "q": "La tijera de podar la usa…",
    "ops": [
      "La jardinera",
      "La panadera",
      "El piloto"
    ],
    "m": "Para cortar las ramas."
  },
  {
    "q": "El volante lo usa…",
    "ops": [
      "La chofer",
      "La médica",
      "El carpintero"
    ],
    "m": "Para manejar."
  },
  {
    "q": "El pincel lo usa…",
    "ops": [
      "El pintor",
      "El plomero",
      "La cocinera"
    ],
    "m": "Para pintar."
  },
  {
    "q": "La llave inglesa la usa…",
    "ops": [
      "La plomera",
      "La maestra",
      "El panadero"
    ],
    "m": "Para ajustar los caños."
  },
  {
    "q": "El horno lo usa…",
    "ops": [
      "La panadera",
      "La jardinera",
      "El chofer"
    ],
    "m": "Para hornear el pan."
  },
  {
    "q": "El pizarrón lo usa…",
    "ops": [
      "El maestro",
      "El plomero",
      "La chofer"
    ],
    "m": "Para enseñar."
  },
  {
    "q": "¿Un oficio es sólo para varones o sólo para mujeres?",
    "ops": [
      "Para cualquiera",
      "Para varones",
      "Para mujeres"
    ],
    "m": "Cualquier persona puede hacer cualquier oficio."
  },
  {
    "q": "La regla y el metro los usa…",
    "ops": [
      "La albañila",
      "La cocinera",
      "El médico"
    ],
    "m": "Para medir antes de construir."
  },
  {
    "q": "¿Para qué sirve una herramienta?",
    "ops": [
      "Para hacer más fácil un trabajo",
      "Para jugar",
      "Para decorar"
    ],
    "m": "Ayuda a hacer algo que sin ella costaría mucho."
  }
];
GAMES.oficios_1 = juegoTriviaTexto(CUR_OFICIOS_1_BANCO, "¿Quién usa esto?", "oficios_1");

/* 1° · Separá los residuos — residuos_1
   DC: Separación de residuos
   Fuente: docs/auditoria-dc-caba/grado-1.md · T4 */
const CUR_RESIDUOS_1_BANCO = [
  {
    "it": "Una botella de plástico vacía",
    "cat": "reciclable",
    "m": "Limpia se recicla."
  },
  {
    "it": "Una servilleta usada",
    "cat": "basura",
    "m": "Es papel, pero sucio no se recicla."
  },
  {
    "it": "Una hoja de papel",
    "cat": "reciclable",
    "m": "El papel limpio se recicla."
  },
  {
    "it": "Un envoltorio de caramelo",
    "cat": "basura",
    "m": "No se puede reciclar."
  },
  {
    "it": "Una lata",
    "cat": "reciclable",
    "m": "El metal se recicla."
  },
  {
    "it": "Una cáscara de banana",
    "cat": "basura",
    "m": "No va con los reciclables. Si hay compost, va ahí."
  },
  {
    "it": "Una caja de cartón",
    "cat": "reciclable",
    "m": "El cartón se recicla."
  },
  {
    "it": "Un chicle masticado",
    "cat": "basura",
    "m": "A la basura."
  },
  {
    "it": "Un frasco de vidrio",
    "cat": "reciclable",
    "m": "El vidrio se recicla."
  },
  {
    "it": "Un pañuelo de papel usado",
    "cat": "basura",
    "m": "Papel sucio."
  },
  {
    "it": "Un diario viejo",
    "cat": "reciclable",
    "m": "Papel limpio."
  },
  {
    "it": "Antes de tirar una botella, conviene…",
    "cat": "reciclable",
    "m": "Enjuagarla: así sí se recicla."
  }
];
GAMES.residuos_1 = juegoClasificar(CUR_RESIDUOS_1_BANCO, "¿Dónde va?", [{"cat": "reciclable", "label": "♻️ Reciclable"}, {"cat": "basura", "label": "🗑️ Basura"}], "residuos_1");

/* 1° · Antes y ahora — antes_ahora_1
   DC: Objetos de la misma función en distintas épocas
   Fuente: docs/auditoria-dc-caba/grado-1.md · T5 */
const CUR_ANTES_AHORA_1_BANCO = [
  {
    "q": "Hoy mandamos un audio. Antes se mandaba…",
    "ops": [
      "Una carta",
      "Un dibujo",
      "Nada"
    ],
    "m": "Las dos sirven para lo mismo: mandar un mensaje lejos."
  },
  {
    "q": "Hoy usamos la heladera. Antes se usaba…",
    "ops": [
      "Una fresquera con hielo",
      "Un horno",
      "Una radio"
    ],
    "m": "Las dos sirven para conservar la comida fría."
  },
  {
    "q": "Hoy escuchamos música en el celular. Antes, en…",
    "ops": [
      "Un tocadiscos",
      "Una lámpara",
      "Un reloj"
    ],
    "m": "Las dos reproducen música."
  },
  {
    "q": "Hoy escribimos en la computadora. Antes, con…",
    "ops": [
      "Una máquina de escribir",
      "Un martillo",
      "Una plancha"
    ],
    "m": "Las dos sirven para escribir."
  },
  {
    "q": "Hoy usamos el lavarropas. Antes se lavaba…",
    "ops": [
      "A mano, en la pileta",
      "En el horno",
      "Con la escoba"
    ],
    "m": "La misma tarea, distinto modo."
  },
  {
    "q": "Hoy sacamos fotos con el celular. Antes, con…",
    "ops": [
      "Una cámara con rollo",
      "Un espejo",
      "Un cuaderno"
    ],
    "m": "Las dos capturan imágenes."
  },
  {
    "q": "Hoy vemos la hora en el celular. Antes, en…",
    "ops": [
      "Un reloj de pared",
      "Una radio",
      "Un libro"
    ],
    "m": "Las dos dan la hora."
  },
  {
    "q": "¿Qué tienen en común el teléfono de antes y el celular?",
    "ops": [
      "Los dos sirven para hablar a distancia",
      "El tamaño",
      "El color"
    ],
    "m": "Lo que importa es para qué SIRVE, no cómo se ve."
  },
  {
    "q": "Hoy hay luz eléctrica. Antes se alumbraba con…",
    "ops": [
      "Velas o faroles",
      "Espejos",
      "Ventanas"
    ],
    "m": "Las dos dan luz."
  },
  {
    "q": "Hoy vamos en auto. Antes se iba…",
    "ops": [
      "En carro con caballos",
      "Volando",
      "En subte"
    ],
    "m": "Las dos sirven para transportarse."
  },
  {
    "q": "¿Por qué cambian los objetos con el tiempo?",
    "ops": [
      "Porque se inventan cosas mejores",
      "Porque se rompen",
      "Porque se aburren"
    ],
    "m": "La tecnología va cambiando."
  },
  {
    "q": "El abanico y el ventilador sirven para…",
    "ops": [
      "Lo mismo: dar aire",
      "Cosas distintas",
      "Nada"
    ],
    "m": "Misma función, distinta época."
  }
];
GAMES.antes_ahora_1 = juegoTriviaTexto(CUR_ANTES_AHORA_1_BANCO, "¿Con qué se hacía antes?", "antes_ahor");

/* 1° · Íconos y datos — iconos_1
   DC: Íconos digitales; datos que se comparten y que se protegen
   Fuente: docs/auditoria-dc-caba/grado-1.md · T6 */
const CUR_ICONOS_1_BANCO = [
  {
    "q": "El dibujito de una lupa sirve para…",
    "ops": [
      "Buscar",
      "Borrar",
      "Guardar"
    ],
    "m": "La lupa es buscar."
  },
  {
    "q": "El dibujito de una casita sirve para…",
    "ops": [
      "Volver al inicio",
      "Cerrar",
      "Imprimir"
    ],
    "m": "La casita es el inicio."
  },
  {
    "q": "El dibujito de un tacho de basura sirve para…",
    "ops": [
      "Borrar",
      "Guardar",
      "Buscar"
    ],
    "m": "Es eliminar."
  },
  {
    "q": "El dibujito de un disquete o una flechita hacia abajo sirve para…",
    "ops": [
      "Guardar o descargar",
      "Borrar",
      "Salir"
    ],
    "m": "Guarda lo que hiciste."
  },
  {
    "q": "La X en una esquina sirve para…",
    "ops": [
      "Cerrar",
      "Abrir",
      "Guardar"
    ],
    "m": "Cierra la ventana."
  },
  {
    "q": "Tu nombre completo y tu dirección son…",
    "ops": [
      "Datos que se protegen",
      "Datos para compartir con cualquiera",
      "No son datos"
    ],
    "m": "No se le dan a desconocidos."
  },
  {
    "q": "¿Le darías tu dirección a alguien que conociste en un juego?",
    "ops": [
      "No, y le aviso a un adulto",
      "Sí",
      "Sí, si es simpático"
    ],
    "m": "Los datos personales no se comparten."
  },
  {
    "q": "Tu color favorito, ¿es un dato que se protege?",
    "ops": [
      "No, ese se puede contar",
      "Sí",
      "Nunca se cuenta nada"
    ],
    "m": "No todos los datos son privados."
  },
  {
    "q": "¿Para qué sirve una contraseña?",
    "ops": [
      "Para que sólo vos entres",
      "Para que ande más rápido",
      "Para nada"
    ],
    "m": "Protege lo tuyo."
  },
  {
    "q": "¿Le contarías tu contraseña a un compañero?",
    "ops": [
      "No, es sólo tuya",
      "Sí",
      "Sí, si es tu amigo"
    ],
    "m": "La contraseña no se comparte."
  },
  {
    "q": "Si aparece algo raro en la pantalla, ¿qué hacés?",
    "ops": [
      "Le avisás a un adulto",
      "Tocás todo",
      "Lo cerrás sin decir nada"
    ],
    "m": "Un adulto sabe qué hacer."
  },
  {
    "q": "Una foto tuya, ¿la subirías sin preguntar?",
    "ops": [
      "No, primero le pregunto a un adulto",
      "Sí",
      "Sí, si sale linda"
    ],
    "m": "Lo que se sube puede quedar."
  }
];
GAMES.iconos_1 = juegoTriviaTexto(CUR_ICONOS_1_BANCO, "¿Qué significa?", "iconos_1");

/* 1° · ¿Cómo se siente? — emociones_1
   DC: Reconocimiento de emociones
   Fuente: docs/auditoria-dc-caba/grado-1.md · T7 */
const CUR_EMOCIONES_1_BANCO = [
  {
    "it": "Le regalaron lo que quería",
    "cat": "alegria",
    "m": "Se siente contento."
  },
  {
    "it": "Se le perdió su juguete preferido",
    "cat": "tristeza",
    "m": "Perder algo querido pone triste."
  },
  {
    "it": "Le rompieron el dibujo a propósito",
    "cat": "enojo",
    "m": "Es normal enojarse."
  },
  {
    "it": "Escuchó un ruido fuerte de noche",
    "cat": "miedo",
    "m": "El miedo avisa que estés atento."
  },
  {
    "it": "Ganó el partido con sus amigos",
    "cat": "alegria",
    "m": "Alegría compartida."
  },
  {
    "it": "Se mudó su mejor amigo",
    "cat": "tristeza",
    "m": "Extrañar da tristeza."
  },
  {
    "it": "Le sacaron la merienda sin pedirle",
    "cat": "enojo",
    "m": "Enoja que no te respeten."
  },
  {
    "it": "Se perdió por un momento en el supermercado",
    "cat": "miedo",
    "m": "Da miedo."
  },
  {
    "it": "Le salió bien algo que le costaba",
    "cat": "alegria",
    "m": "Orgullo y alegría."
  },
  {
    "it": "Nadie lo invitó a jugar",
    "cat": "tristeza",
    "m": "Quedar afuera pone triste."
  },
  {
    "it": "Le tocó esperar mucho y nadie le explicó",
    "cat": "enojo",
    "m": "La espera sin explicación enoja."
  },
  {
    "it": "Tiene que hablar delante de todos",
    "cat": "miedo",
    "m": "Los nervios también son miedo."
  },
  {
    "it": "Abrazó a alguien que extrañaba",
    "cat": "alegria",
    "m": "Reencontrarse alegra."
  },
  {
    "it": "Se lastimó y le dolió",
    "cat": "tristeza",
    "m": "El dolor también da ganas de llorar."
  },
  {
    "it": "¿Está mal sentir enojo o miedo?",
    "cat": "enojo",
    "m": "Ninguna emoción está mal. Lo que importa es qué hacés con ella."
  },
  {
    "it": "Vio una película con una escena muy oscura",
    "cat": "miedo",
    "m": "Es normal asustarse."
  }
];
GAMES.emociones_1 = juegoClasificar(CUR_EMOCIONES_1_BANCO, "¿Cómo se siente en esta situación?", [{"cat": "alegria", "label": "😀 Alegría"}, {"cat": "tristeza", "label": "😢 Tristeza"}, {"cat": "enojo", "label": "😠 Enojo"}, {"cat": "miedo", "label": "😨 Miedo"}], "emociones_");

/* 1° · Armá el plato — plato_1
   DC: Grupos de alimentos
   Fuente: docs/auditoria-dc-caba/grado-1.md · T8 */
const CUR_PLATO_1_BANCO = [
  {
    "it": "Manzana",
    "cat": "frutas",
    "m": "Fruta."
  },
  {
    "it": "Pan",
    "cat": "cereales",
    "m": "Del trigo."
  },
  {
    "it": "Huevo",
    "cat": "proteinas",
    "m": "Aporta proteínas."
  },
  {
    "it": "Zanahoria",
    "cat": "frutas",
    "m": "Verdura."
  },
  {
    "it": "Arroz",
    "cat": "cereales",
    "m": "Cereal."
  },
  {
    "it": "Queso",
    "cat": "proteinas",
    "m": "Lácteo."
  },
  {
    "it": "Banana",
    "cat": "frutas",
    "m": "Fruta."
  },
  {
    "it": "Papa",
    "cat": "cereales",
    "m": "Aunque salga de la tierra, la papa llena como el pan: va con los cereales."
  },
  {
    "it": "Pollo",
    "cat": "proteinas",
    "m": "Carne."
  },
  {
    "it": "Tomate",
    "cat": "frutas",
    "m": "Verdura."
  },
  {
    "it": "Fideos",
    "cat": "cereales",
    "m": "Del trigo."
  },
  {
    "it": "Leche",
    "cat": "proteinas",
    "m": "Lácteo."
  },
  {
    "it": "Naranja",
    "cat": "frutas",
    "m": "Fruta."
  },
  {
    "it": "Lentejas",
    "cat": "cereales",
    "m": "Las legumbres van con los cereales."
  }
];
GAMES.plato_1 = juegoClasificar(CUR_PLATO_1_BANCO, "¿De qué grupo es?", [{"cat": "frutas", "label": "🍎 Frutas y verduras"}, {"cat": "cereales", "label": "🍞 Cereales y papa"}, {"cat": "proteinas", "label": "🥚 Carnes y lácteos"}], "plato_1");

/* 1° · ¿Cruzo o espero? — vial_1
   DC: Educación vial
   Fuente: docs/auditoria-dc-caba/grado-1.md · T9 */
const CUR_VIAL_1_BANCO = [
  {
    "q": "El semáforo del peatón está en rojo. ¿Qué hacés?",
    "ops": [
      "Esperar",
      "Cruzar rápido",
      "Cruzar mirando"
    ],
    "m": "Rojo es esperar, siempre."
  },
  {
    "q": "Está en rojo pero no viene ningún auto. ¿Qué hacés?",
    "ops": [
      "Esperar igual",
      "Cruzar",
      "Cruzar corriendo"
    ],
    "m": "Puede aparecer un auto que no viste. La regla no cambia."
  },
  {
    "q": "¿Por dónde se cruza?",
    "ops": [
      "Por la senda peatonal",
      "Por el medio de la cuadra",
      "Por donde sea"
    ],
    "m": "Es donde el auto espera que cruces."
  },
  {
    "q": "Antes de cruzar, ¿qué hacés?",
    "ops": [
      "Mirar para los dos lados",
      "Correr",
      "Cerrar los ojos"
    ],
    "m": "Los autos vienen de los dos sentidos."
  },
  {
    "q": "¿Se cruza solo o de la mano de un adulto?",
    "ops": [
      "De la mano de un adulto",
      "Solo",
      "Corriendo"
    ],
    "m": "A tu edad, siempre con un grande."
  },
  {
    "q": "¿Por dónde caminás?",
    "ops": [
      "Por la vereda",
      "Por la calle",
      "Por el cordón"
    ],
    "m": "La vereda es del peatón."
  },
  {
    "q": "En el auto vas…",
    "ops": [
      "Atrás y con cinturón",
      "Adelante",
      "Parado"
    ],
    "m": "Atrás y siempre atado."
  },
  {
    "q": "¿Se puede jugar a la pelota en la calle?",
    "ops": [
      "No",
      "Sí",
      "Sí, si hay pocos autos"
    ],
    "m": "La calle es de los vehículos."
  },
  {
    "q": "El semáforo en verde para el peatón significa…",
    "ops": [
      "Podés cruzar mirando",
      "Esperar",
      "Correr"
    ],
    "m": "Verde es cruzar, pero mirando igual."
  },
  {
    "q": "Si se te cae algo en la calle, ¿qué hacés?",
    "ops": [
      "Le avisás a un adulto",
      "Vas corriendo a buscarlo",
      "Lo dejás y no decís nada"
    ],
    "m": "Nunca salgas solo a la calle a buscar algo."
  },
  {
    "q": "En bici, ¿qué usás en la cabeza?",
    "ops": [
      "Casco",
      "Gorra",
      "Nada"
    ],
    "m": "El casco protege."
  },
  {
    "q": "Al bajar del auto, ¿por qué puerta salís?",
    "ops": [
      "Por la de la vereda",
      "Por la de la calle",
      "Por cualquiera"
    ],
    "m": "Del lado de la calle pasan los autos."
  }
];
GAMES.vial_1 = juegoTriviaTexto(CUR_VIAL_1_BANCO, "¿Qué hacés?", "vial_1");

/* 1° · Armá la planta — planta_partes_1
   DC: Partes de la planta y su función
   Fuente: docs/auditoria-dc-caba/grado-1.md · C2 */
const CUR_PLANTA_PARTES_1_BANCO = [
  {
    "q": "¿Qué parte de la planta toma el agua de la tierra?",
    "ops": [
      "La raíz",
      "La hoja",
      "La flor"
    ],
    "m": "La raíz está abajo, en la tierra, y chupa el agua."
  },
  {
    "q": "¿Qué parte sostiene la planta y lleva el agua para arriba?",
    "ops": [
      "El tallo",
      "La raíz",
      "El fruto"
    ],
    "m": "El tallo es como una cañita por donde sube el agua."
  },
  {
    "q": "¿En qué parte la planta fabrica su alimento?",
    "ops": [
      "Las hojas",
      "La raíz",
      "El tallo"
    ],
    "m": "Las hojas usan la luz del sol para eso."
  },
  {
    "q": "¿Qué parte se abre de colores para atraer insectos?",
    "ops": [
      "La flor",
      "La raíz",
      "El tallo"
    ],
    "m": "La flor llama a los insectos que la ayudan."
  },
  {
    "q": "¿Dónde están las semillas?",
    "ops": [
      "Adentro del fruto",
      "En la raíz",
      "En el tallo"
    ],
    "m": "El fruto guarda las semillas."
  },
  {
    "q": "Si le cortás las raíces a una planta, ¿qué pasa?",
    "ops": [
      "No puede tomar agua",
      "Crece más",
      "No pasa nada"
    ],
    "m": "Sin raíz no llega el agua."
  },
  {
    "q": "Si la ponés en un lugar totalmente oscuro, ¿qué pasa?",
    "ops": [
      "No puede fabricar su alimento",
      "Crece igual",
      "Se pone verde"
    ],
    "m": "Las hojas necesitan luz."
  },
  {
    "q": "¿Qué necesita una planta para vivir?",
    "ops": [
      "Agua, luz, aire y tierra",
      "Sólo agua",
      "Sólo luz"
    ],
    "m": "Las cuatro cosas."
  },
  {
    "q": "La zanahoria que comemos es…",
    "ops": [
      "Una raíz",
      "Un fruto",
      "Una flor"
    ],
    "m": "Es la raíz de la planta."
  },
  {
    "q": "La lechuga que comemos es…",
    "ops": [
      "Hojas",
      "Raíz",
      "Fruto"
    ],
    "m": "Son las hojas."
  },
  {
    "q": "El tomate que comemos es…",
    "ops": [
      "Un fruto",
      "Una raíz",
      "Una hoja"
    ],
    "m": "Tiene semillas adentro: es fruto."
  },
  {
    "q": "¿De dónde sale una planta nueva?",
    "ops": [
      "De una semilla",
      "De una hoja suelta",
      "De la nada"
    ],
    "m": "La semilla trae adentro la planta chiquita."
  }
];
GAMES.planta_partes_1 = juegoTriviaTexto(CUR_PLANTA_PARTES_1_BANCO, "¿Para qué sirve cada parte?", "planta_par");

/* 1° · Mi cuerpo y las etapas — cuerpo_etapas_1
   DC: Partes del cuerpo; etapas de la vida
   Fuente: docs/auditoria-dc-caba/grado-1.md · C7 */
const CUR_CUERPO_ETAPAS_1_BANCO = [
  {
    "q": "¿Con qué parte del cuerpo agarrás las cosas?",
    "ops": [
      "Las manos",
      "Los pies",
      "La cabeza"
    ],
    "m": "Las manos, con los dedos."
  },
  {
    "q": "¿Con qué parte caminás?",
    "ops": [
      "Las piernas",
      "Los brazos",
      "La espalda"
    ],
    "m": "Las piernas."
  },
  {
    "q": "¿Dónde está el codo?",
    "ops": [
      "En el medio del brazo",
      "En la pierna",
      "En la mano"
    ],
    "m": "Donde el brazo se dobla."
  },
  {
    "q": "¿Dónde está la rodilla?",
    "ops": [
      "En el medio de la pierna",
      "En el brazo",
      "En el cuello"
    ],
    "m": "Donde la pierna se dobla."
  },
  {
    "q": "¿Qué une la cabeza con el resto del cuerpo?",
    "ops": [
      "El cuello",
      "El codo",
      "La rodilla"
    ],
    "m": "El cuello."
  },
  {
    "q": "¿Cuál es la primera etapa de la vida?",
    "ops": [
      "Bebé",
      "Niño",
      "Adulto"
    ],
    "m": "Todos empezamos siendo bebés."
  },
  {
    "q": "¿Qué viene después de ser bebé?",
    "ops": [
      "Niño",
      "Adulto",
      "Anciano"
    ],
    "m": "Niño o niña."
  },
  {
    "q": "¿Y después de niño?",
    "ops": [
      "Adolescente",
      "Bebé",
      "Anciano"
    ],
    "m": "La adolescencia."
  },
  {
    "q": "Ordenadas de menor a mayor, las etapas son…",
    "ops": [
      "Bebé, niño, adolescente, adulto, anciano",
      "Niño, bebé, adulto",
      "Adulto, niño, bebé"
    ],
    "m": "Siempre en ese orden."
  },
  {
    "q": "¿Un bebé puede caminar solo?",
    "ops": [
      "No todavía, aprende de más grande",
      "Sí, desde que nace",
      "Nunca"
    ],
    "m": "Cada etapa trae cosas nuevas que se pueden hacer."
  },
  {
    "q": "¿Tu cuerpo es igual al de todos?",
    "ops": [
      "No, cada cuerpo es distinto",
      "Sí, todos iguales",
      "Sólo el de los grandes cambia"
    ],
    "m": "Somos parecidos y a la vez distintos."
  },
  {
    "q": "¿Con qué partes sentís el mundo?",
    "ops": [
      "Los ojos, los oídos, la nariz, la lengua y la piel",
      "Sólo los ojos",
      "Sólo las manos"
    ],
    "m": "Son los cinco sentidos."
  }
];
GAMES.cuerpo_etapas_1 = juegoTriviaTexto(CUR_CUERPO_ETAPAS_1_BANCO, "Mirá tu cuerpo y cómo cambia.", "cuerpo_eta");

/* 4° · Capitales y regiones — capitales_4
   DC: División político-administrativa: las 24 jurisdicciones, sus capitales y las 5 regiones
   Fuente: docs/auditoria-dc-caba/grado-4.md · S8 */
const CUR_CAPITALES_4_BANCO = [
  {
    "q": "La capital de Salta es…",
    "ops": [
      "Salta",
      "Jujuy",
      "Tucumán"
    ],
    "m": "Varias provincias tienen su capital con el mismo nombre."
  },
  {
    "q": "La capital de Córdoba es…",
    "ops": [
      "Córdoba",
      "Río Cuarto",
      "Villa María"
    ],
    "m": "Mismo nombre."
  },
  {
    "q": "La capital de Santa Fe es…",
    "ops": [
      "Santa Fe",
      "Rosario",
      "Rafaela"
    ],
    "m": "Ojo: Rosario es más grande, pero la capital es Santa Fe."
  },
  {
    "q": "La capital de Buenos Aires (la provincia) es…",
    "ops": [
      "La Plata",
      "Buenos Aires",
      "Mar del Plata"
    ],
    "m": "La Plata. La Ciudad de Buenos Aires es una jurisdicción aparte."
  },
  {
    "q": "La capital de Mendoza es…",
    "ops": [
      "Mendoza",
      "San Rafael",
      "Malargüe"
    ],
    "m": "Mismo nombre."
  },
  {
    "q": "La capital de Entre Ríos es…",
    "ops": [
      "Paraná",
      "Concordia",
      "Gualeguaychú"
    ],
    "m": "Paraná."
  },
  {
    "q": "La capital de Chubut es…",
    "ops": [
      "Rawson",
      "Trelew",
      "Comodoro Rivadavia"
    ],
    "m": "Rawson, aunque Comodoro sea más grande."
  },
  {
    "q": "La capital de Neuquén es…",
    "ops": [
      "Neuquén",
      "Zapala",
      "San Martín de los Andes"
    ],
    "m": "Mismo nombre."
  },
  {
    "q": "La capital de Misiones es…",
    "ops": [
      "Posadas",
      "Iguazú",
      "Oberá"
    ],
    "m": "Posadas."
  },
  {
    "q": "La capital de Tucumán es…",
    "ops": [
      "San Miguel de Tucumán",
      "Tafí",
      "Concepción"
    ],
    "m": "San Miguel de Tucumán."
  },
  {
    "q": "¿Cuántas jurisdicciones tiene la Argentina?",
    "ops": [
      "24",
      "23",
      "25"
    ],
    "m": "23 provincias más la Ciudad Autónoma de Buenos Aires."
  },
  {
    "q": "¿Cuáles son las cinco regiones?",
    "ops": [
      "NOA, NEA, Cuyo, Centro-Pampeana y Patagonia",
      "Norte, Sur, Este y Oeste",
      "Sólo tres: norte, centro y sur"
    ],
    "m": "Se agrupan por geografía y economía."
  },
  {
    "q": "Salta y Jujuy son del…",
    "ops": [
      "NOA",
      "NEA",
      "Cuyo"
    ],
    "m": "Noroeste argentino."
  },
  {
    "q": "Misiones y Corrientes son del…",
    "ops": [
      "NEA",
      "NOA",
      "Patagonia"
    ],
    "m": "Noreste argentino."
  },
  {
    "q": "Mendoza, San Juan y San Luis son de…",
    "ops": [
      "Cuyo",
      "NOA",
      "Patagonia"
    ],
    "m": "Cuyo."
  },
  {
    "q": "Neuquén, Río Negro, Chubut y Santa Cruz son de…",
    "ops": [
      "Patagonia",
      "Cuyo",
      "NEA"
    ],
    "m": "Patagonia."
  },
  {
    "q": "Córdoba, Santa Fe y Buenos Aires son de…",
    "ops": [
      "Centro-Pampeana",
      "Cuyo",
      "NOA"
    ],
    "m": "La región Centro-Pampeana."
  },
  {
    "q": "La capital de San Juan es…",
    "ops": [
      "San Juan",
      "Jáchal",
      "Caucete"
    ],
    "m": "Mismo nombre."
  },
  {
    "q": "La capital de Corrientes es…",
    "ops": [
      "Corrientes",
      "Goya",
      "Mercedes"
    ],
    "m": "Mismo nombre."
  },
  {
    "q": "La capital de Santiago del Estero es…",
    "ops": [
      "Santiago del Estero",
      "La Banda",
      "Termas"
    ],
    "m": "Mismo nombre."
  },
  {
    "q": "La capital de Formosa es…",
    "ops": [
      "Formosa",
      "Clorinda",
      "Pirané"
    ],
    "m": "Mismo nombre."
  },
  {
    "q": "La capital de Tierra del Fuego es…",
    "ops": [
      "Ushuaia",
      "Río Grande",
      "Tolhuin"
    ],
    "m": "Ushuaia, la ciudad más austral."
  },
  {
    "q": "La capital de La Pampa es…",
    "ops": [
      "Santa Rosa",
      "General Pico",
      "Toay"
    ],
    "m": "Santa Rosa."
  },
  {
    "q": "La capital de Catamarca es…",
    "ops": [
      "San Fernando del Valle de Catamarca",
      "Andalgalá",
      "Belén"
    ],
    "m": "Su nombre completo es largo."
  }
];
GAMES.capitales_4 = juegoTriviaTexto(CUR_CAPITALES_4_BANCO, "¿Cuál es la capital?", "capitales_");

/* 5° · La recta del millón — recta_millon_5
   DC: Lectura, escritura y orden en el rango del millón
   Fuente: docs/auditoria-dc-caba/grado-5.md · M1 */
const CUR_RECTA_MILLON_5_BANCO = [
  {
    "q": "¿Cómo se escribe un millón?",
    "ops": [
      "1.000.000",
      "100.000",
      "10.000"
    ],
    "m": "Un 1 y seis ceros."
  },
  {
    "q": "¿Cuántas cifras tiene un millón?",
    "ops": [
      "7",
      "6",
      "8"
    ],
    "m": "Una más que cien mil."
  },
  {
    "q": "¿Cuál es mayor: 999.999 o 1.000.000?",
    "ops": [
      "1.000.000",
      "999.999",
      "Son iguales"
    ],
    "m": "Siete cifras contra seis."
  },
  {
    "q": "¿Qué número sigue a 999.999?",
    "ops": [
      "1.000.000",
      "999.9910",
      "1.000.0"
    ],
    "m": "Se llenan todas las posiciones y sube la siguiente."
  },
  {
    "q": "¿Cómo se escribe trescientos cuarenta y dos mil quinientos?",
    "ops": [
      "342.500",
      "3.425.000",
      "342.000.500"
    ],
    "m": "Trescientos cuarenta y dos mil son 342.000, más 500."
  },
  {
    "q": "¿Cuánto vale el 7 en 7.250.000?",
    "ops": [
      "7.000.000",
      "700.000",
      "70.000"
    ],
    "m": "Es la primera cifra de un número de 7: son millones."
  },
  {
    "q": "¿Cuál es mayor: 1.250.000 o 1.205.000?",
    "ops": [
      "1.250.000",
      "1.205.000",
      "Son iguales"
    ],
    "m": "Se compara de izquierda a derecha: 5 contra 0 en la misma posición."
  },
  {
    "q": "En una recta de 0 a 1.000.000, el 500.000 está…",
    "ops": [
      "Justo en el medio",
      "Cerca del cero",
      "Cerca del millón"
    ],
    "m": "Es la mitad."
  },
  {
    "q": "¿Y el 250.000?",
    "ops": [
      "En el primer cuarto",
      "En el medio",
      "Cerca del millón"
    ],
    "m": "Un cuarto de un millón."
  },
  {
    "q": "Medio millón se escribe…",
    "ops": [
      "500.000",
      "50.000",
      "5.000.000"
    ],
    "m": "La mitad de 1.000.000."
  },
  {
    "q": "¿Cuántos cien mil entran en un millón?",
    "ops": [
      "10",
      "100",
      "1.000"
    ],
    "m": "Diez veces cien mil."
  },
  {
    "q": "¿Cómo se lee 4.080.000?",
    "ops": [
      "Cuatro millones ochenta mil",
      "Cuatro millones ocho mil",
      "Cuarenta y ocho mil"
    ],
    "m": "El cero después del 4 guarda el lugar de los cientos de mil."
  },
  {
    "q": "¿Cuál está entre 300.000 y 400.000?",
    "ops": [
      "350.000",
      "250.000",
      "450.000"
    ],
    "m": "Está en el medio de los dos."
  },
  {
    "q": "Dos millones y medio se escribe…",
    "ops": [
      "2.500.000",
      "2.050.000",
      "25.000.000"
    ],
    "m": "Dos millones más medio millón."
  }
];
GAMES.recta_millon_5 = juegoTriviaTexto(CUR_RECTA_MILLON_5_BANCO, "Ubicá el número.", "recta_mill");

/* 5° · ¿Se arma el cuerpo? — geometria_5
   DC: Desigualdad triangular; suma de ángulos; desarrollos planos
   Fuente: docs/auditoria-dc-caba/grado-5.md · M14 */
const CUR_GEOMETRIA_5_BANCO = [
  {
    "q": "Con varillas de 4, 6 y 9 cm, ¿se arma un triángulo?",
    "ops": [
      "Sí",
      "No",
      "Depende"
    ],
    "m": "4 + 6 = 10, que supera a 9. Se arma, por poco."
  },
  {
    "q": "¿Y con 4, 5 y 9?",
    "ops": [
      "No",
      "Sí",
      "Depende"
    ],
    "m": "4 + 5 = 9, justo igual al largo: queda una línea recta, no cierra."
  },
  {
    "q": "La regla para saberlo es…",
    "ops": [
      "Los dos lados cortos tienen que SUPERAR al largo",
      "Los tres lados tienen que ser iguales",
      "Da lo mismo"
    ],
    "m": "Si suman igual o menos, no cierra."
  },
  {
    "q": "¿Cuánto suman los tres ángulos de un triángulo?",
    "ops": [
      "180°",
      "90°",
      "360°"
    ],
    "m": "Siempre 180, sea el triángulo que sea."
  },
  {
    "q": "Si dos ángulos miden 60° y 70°, el tercero mide…",
    "ops": [
      "50°",
      "60°",
      "70°"
    ],
    "m": "180 − 60 − 70."
  },
  {
    "q": "¿Puede un triángulo tener dos ángulos rectos?",
    "ops": [
      "No, ya sumarían 180",
      "Sí",
      "Siempre"
    ],
    "m": "90 + 90 = 180 y no quedaría nada para el tercero."
  },
  {
    "q": "¿Cuántos desarrollos planos distintos tiene un cubo?",
    "ops": [
      "11",
      "6",
      "1"
    ],
    "m": "Hay once formas de aplanarlo que no son la misma girada."
  },
  {
    "q": "El desarrollo de un cilindro tiene…",
    "ops": [
      "Dos círculos y un rectángulo",
      "Seis cuadrados",
      "Tres triángulos"
    ],
    "m": "Las dos tapas y el costado desplegado."
  },
  {
    "q": "El desarrollo de una pirámide de base cuadrada tiene…",
    "ops": [
      "Un cuadrado y cuatro triángulos",
      "Seis cuadrados",
      "Dos círculos"
    ],
    "m": "La base más las caras que suben."
  },
  {
    "q": "¿Todos los desarrollos de seis cuadrados arman un cubo?",
    "ops": [
      "No, depende de cómo estén unidos",
      "Sí, siempre",
      "Nunca"
    ],
    "m": "Tienen que poder plegarse sin superponerse."
  },
  {
    "q": "Un triángulo con los tres lados iguales tiene sus ángulos de…",
    "ops": [
      "60° cada uno",
      "90°",
      "45°"
    ],
    "m": "180 dividido 3."
  },
  {
    "q": "Con varillas de 5, 5 y 10, ¿se arma?",
    "ops": [
      "No",
      "Sí",
      "Sólo si se estiran"
    ],
    "m": "5 + 5 = 10, exactamente el largo: queda plano."
  }
];
GAMES.geometria_5 = juegoTriviaTexto(CUR_GEOMETRIA_5_BANCO, "Pensá la figura antes de armarla.", "geometria_");

/* 5° · Fases y eclipses — eclipses_5
   DC: Fases de la Luna; los eclipses como sombras
   Fuente: docs/auditoria-dc-caba/grado-5.md · N8 */
const CUR_ECLIPSES_5_BANCO = [
  {
    "q": "¿Por qué la Luna cambia de forma?",
    "ops": [
      "Porque vemos distinta parte de su mitad iluminada",
      "Porque la tapa la sombra de la Tierra",
      "Porque cambia de tamaño"
    ],
    "m": "Ésta es LA confusión del tema: la sombra de la Tierra sólo actúa en un eclipse."
  },
  {
    "q": "¿Cuánta parte de la Luna está siempre iluminada por el Sol?",
    "ops": [
      "La mitad",
      "Toda",
      "Ninguna"
    ],
    "m": "La mitad que le da la cara al Sol, siempre."
  },
  {
    "q": "En luna NUEVA, ¿qué vemos?",
    "ops": [
      "Casi nada: la parte iluminada está del otro lado",
      "Toda la Luna",
      "Media Luna"
    ],
    "m": "La cara que vemos está a oscuras."
  },
  {
    "q": "En luna LLENA, ¿qué vemos?",
    "ops": [
      "Toda la cara iluminada",
      "Nada",
      "La mitad"
    ],
    "m": "El Sol le da de frente desde nuestra perspectiva."
  },
  {
    "q": "¿Cuánto tarda la Luna en pasar por todas sus fases?",
    "ops": [
      "Un mes aproximadamente",
      "Un día",
      "Un año"
    ],
    "m": "Por eso el mes se llama así."
  },
  {
    "q": "¿Qué es un eclipse de Luna?",
    "ops": [
      "La Tierra se pone entre el Sol y la Luna y le hace sombra",
      "La Luna tapa al Sol",
      "La Luna se apaga"
    ],
    "m": "Ahí sí actúa la sombra de la Tierra."
  },
  {
    "q": "¿Y un eclipse de Sol?",
    "ops": [
      "La Luna se pone entre el Sol y la Tierra",
      "La Tierra tapa al Sol",
      "El Sol se apaga"
    ],
    "m": "La Luna nos tapa el Sol."
  },
  {
    "q": "¿Los eclipses pasan todos los meses?",
    "ops": [
      "No, son poco frecuentes",
      "Sí, cada mes",
      "Sí, cada semana"
    ],
    "m": "La órbita de la Luna está inclinada: casi siempre pasa por arriba o por abajo."
  },
  {
    "q": "¿Por qué no hay un eclipse de Sol todos los meses?",
    "ops": [
      "Porque la órbita de la Luna está inclinada",
      "Porque la Luna se apaga",
      "Porque el Sol cambia de lugar"
    ],
    "m": "Casi siempre la sombra pasa por arriba o por debajo de la Tierra."
  },
  {
    "q": "¿Se puede mirar un eclipse de Sol a ojo desnudo?",
    "ops": [
      "No, daña la vista",
      "Sí, sin problema",
      "Sí, si es corto"
    ],
    "m": "Hacen falta filtros especiales."
  },
  {
    "q": "Entre luna nueva y luna llena, la Luna está…",
    "ops": [
      "Creciendo",
      "Menguando",
      "Igual"
    ],
    "m": "Cada vez vemos más parte iluminada."
  },
  {
    "q": "¿Por qué siempre vemos la misma cara de la Luna?",
    "ops": [
      "Porque gira sobre sí misma en el mismo tiempo que tarda en dar la vuelta a la Tierra",
      "Porque no gira",
      "Porque está quieta"
    ],
    "m": "Los dos giros están sincronizados."
  }
];
GAMES.eclipses_5 = juegoTriviaTexto(CUR_ECLIPSES_5_BANCO, "Mirá el Sol, la Tierra y la Luna.", "eclipses_5");

/* 5° · ¿Unitario o federal? — unitario_federal_5
   DC: Unitarios y federales; la Constitución de 1853 como acuerdo
   Fuente: docs/auditoria-dc-caba/grado-5.md · S6 */
const CUR_UNITARIO_FEDERAL_5_BANCO = [
  {
    "it": "El gobierno debe decidir todo desde Buenos Aires",
    "cat": "unitario",
    "m": "Un solo centro de poder: eso es unitario."
  },
  {
    "it": "Cada provincia debe manejar sus propios asuntos",
    "cat": "federal",
    "m": "Poder repartido entre las provincias."
  },
  {
    "it": "Las provincias se gobiernan solas PERO hay un gobierno nacional",
    "cat": "acuerdo",
    "m": "La Constitución de 1853 tomó algo de cada postura."
  },
  {
    "it": "Las rentas de la aduana son para toda la Nación",
    "cat": "unitario",
    "m": "Concentrar los recursos en el centro."
  },
  {
    "it": "Cada provincia debe quedarse con lo que produce",
    "cat": "federal",
    "m": "Autonomía económica provincial."
  },
  {
    "it": "Hay una Constitución que está por encima de todos",
    "cat": "acuerdo",
    "m": "Nadie, ni el gobierno, está por encima de la ley."
  },
  {
    "it": "Una sola ley igual para todo el país",
    "cat": "unitario",
    "m": "Uniformidad desde el centro."
  },
  {
    "it": "Cada provincia dicta su propia constitución",
    "cat": "federal",
    "m": "Y esto quedó en la Constitución nacional."
  },
  {
    "it": "El país se organiza en provincias con gobierno propio y uno nacional",
    "cat": "acuerdo",
    "m": "Es el artículo 1: forma representativa, republicana y federal."
  },
  {
    "it": "Buenos Aires debe conducir al resto del país",
    "cat": "unitario",
    "m": "Centralismo."
  },
  {
    "it": "Los caudillos de cada provincia representan a su gente",
    "cat": "federal",
    "m": "Voces locales frente al centro."
  },
  {
    "it": "Se elige presidente, diputados y senadores",
    "cat": "acuerdo",
    "m": "El Senado representa a las provincias por igual: eso es lo federal del acuerdo."
  },
  {
    "it": "Los diputados se eligen según cuánta gente tiene cada provincia",
    "cat": "acuerdo",
    "m": "Diputados por población y senadores por provincia: las dos lógicas conviven."
  },
  {
    "it": "El interior no tiene por qué obedecer a Buenos Aires",
    "cat": "federal",
    "m": "Autonomía."
  }
];
GAMES.unitario_federal_5 = juegoClasificar(CUR_UNITARIO_FEDERAL_5_BANCO, "¿De qué postura es esta idea?", [{"cat": "unitario", "label": "🏛️ Unitario"}, {"cat": "federal", "label": "🌎 Federal"}, {"cat": "acuerdo", "label": "🤝 Quedó en la Constitución"}], "unitario_f");

/* 5° · Clasificador de recursos — recursos_5
   DC: Recursos forestales, mineros y panorámicos; su valorización
   Fuente: docs/auditoria-dc-caba/grado-5.md · S8 */
const CUR_RECURSOS_5_BANCO = [
  {
    "it": "Los bosques de la Patagonia para hacer madera",
    "cat": "forestal",
    "m": "Se aprovecha el árbol."
  },
  {
    "it": "La plata de las minas de Potosí",
    "cat": "minero",
    "m": "Se extrae del suelo."
  },
  {
    "it": "El paisaje del Perito Moreno que atrae turistas",
    "cat": "panoramico",
    "m": "Su valor está en mirarlo, no en extraerlo."
  },
  {
    "it": "El quebracho del Chaco para hacer durmientes",
    "cat": "forestal",
    "m": "Madera."
  },
  {
    "it": "El litio del norte argentino",
    "cat": "minero",
    "m": "Mineral que se extrae."
  },
  {
    "it": "Las Cataratas del Iguazú",
    "cat": "panoramico",
    "m": "Recurso turístico."
  },
  {
    "it": "Los pinos plantados para hacer papel",
    "cat": "forestal",
    "m": "Se usan para pasta de papel."
  },
  {
    "it": "El petróleo de Vaca Muerta",
    "cat": "minero",
    "m": "Se extrae del subsuelo."
  },
  {
    "it": "Los cerros de Jujuy con sus colores",
    "cat": "panoramico",
    "m": "Atraen visitantes."
  },
  {
    "it": "El mismo bosque: se puede talar o se puede visitar",
    "cat": "panoramico",
    "m": "Un MISMO lugar puede tener dos usos distintos, y a veces no compatibles."
  },
  {
    "it": "El mismo cerro: se puede minar o se puede recorrer",
    "cat": "panoramico",
    "m": "La valorización depende de qué decide hacer la sociedad con él."
  },
  {
    "it": "La sal de las Salinas Grandes",
    "cat": "minero",
    "m": "Se extrae."
  },
  {
    "it": "El bosque de arrayanes protegido como parque",
    "cat": "panoramico",
    "m": "Se decidió valorarlo por su paisaje y no por su madera."
  },
  {
    "it": "La yerba mate de las plantaciones de Misiones",
    "cat": "forestal",
    "m": "Es un cultivo de origen vegetal."
  }
];
GAMES.recursos_5 = juegoClasificar(CUR_RECURSOS_5_BANCO, "¿Qué tipo de recurso es?", [{"cat": "forestal", "label": "🌲 Forestal"}, {"cat": "minero", "label": "⛏️ Minero"}, {"cat": "panoramico", "label": "🏞️ Panorámico"}], "recursos_5");

/* 5° · Club de lectura — club_lectura_5
   DC: Inferencias; correferencia; información relevante en textos de varios géneros
   Fuente: docs/auditoria-dc-caba/grado-5.md · L1 */
const CUR_CLUB_LECTURA_5_BANCO = [
  {
    "q": "«Martín miró el reloj y salió corriendo sin terminar el desayuno.» ¿Qué se puede deducir?",
    "ops": [
      "Estaba llegando tarde",
      "No tenía hambre",
      "El reloj estaba roto"
    ],
    "m": "No lo dice, pero mirar el reloj y correr lo sugiere. Eso es inferir."
  },
  {
    "q": "«La casa estaba a oscuras y el buzón rebalsaba de cartas.» ¿Qué se deduce?",
    "ops": [
      "Hacía tiempo que no había nadie",
      "Se cortó la luz",
      "El cartero se equivocó"
    ],
    "m": "Las dos pistas juntas apuntan a lo mismo."
  },
  {
    "q": "«Ana abrió el paraguas apenas salió.» ¿Cómo estaba el día?",
    "ops": [
      "Llovía",
      "Hacía sol",
      "Nevaba"
    ],
    "m": "El paraguas lo dice sin decirlo."
  },
  {
    "q": "«El perro movía la cola y saltaba en la puerta.» ¿Cómo estaba?",
    "ops": [
      "Contento",
      "Asustado",
      "Enfermo"
    ],
    "m": "Son señales de alegría."
  },
  {
    "q": "«Cuando la vio entrar, cerró el cuaderno de golpe.» ¿Qué sugiere?",
    "ops": [
      "No quería que ella viera lo que escribía",
      "Que había terminado",
      "Que tenía frío"
    ],
    "m": "El «de golpe» es la pista."
  },
  {
    "q": "«El hornero construye su nido con barro. El ave trabaja durante semanas.» ¿A quién se refiere «el ave»?",
    "ops": [
      "Al hornero",
      "Al barro",
      "A otra ave"
    ],
    "m": "Es la misma cosa nombrada de otra manera: eso es correferencia."
  },
  {
    "q": "«Lucía le prestó el libro a Sofía. Ella lo devolvió al día siguiente.» ¿Quién devolvió?",
    "ops": [
      "Sofía",
      "Lucía",
      "El libro"
    ],
    "m": "«Ella» retoma a la última mencionada que puede devolver."
  },
  {
    "q": "«Se apagaron las luces y el público empezó a aplaudir.» ¿Dónde están?",
    "ops": [
      "En un teatro o cine",
      "En una casa",
      "En la calle"
    ],
    "m": "El público y las luces lo ubican."
  },
  {
    "q": "«El equipo volvió al vestuario en silencio, con la cabeza baja.» ¿Qué pasó?",
    "ops": [
      "Perdieron",
      "Ganaron",
      "Se suspendió"
    ],
    "m": "El lenguaje del cuerpo lo cuenta."
  },
  {
    "q": "«Puso tres platos en la mesa aunque eran cuatro en la casa.» ¿Qué se deduce?",
    "ops": [
      "Alguien no iba a comer",
      "Se olvidó de contar",
      "Sobraban platos"
    ],
    "m": "El «aunque» marca que la diferencia importa."
  },
  {
    "q": "«La torta estaba intacta y las velas sin encender.» ¿Qué se deduce?",
    "ops": [
      "La fiesta todavía no había empezado",
      "Ya se habían ido",
      "Nadie quería torta"
    ],
    "m": "Las dos pistas apuntan a antes del festejo."
  },
  {
    "q": "En un texto, ¿para qué sirve reemplazar una palabra por otra que significa lo mismo?",
    "ops": [
      "Para no repetir y que el texto se lea mejor",
      "Para confundir",
      "Para hacerlo más largo"
    ],
    "m": "Es lo que mantiene el texto unido."
  },
  {
    "q": "«Guardó el abrigo en el placard: no lo necesitaría por meses.» ¿En qué época estamos?",
    "ops": [
      "Empezando el verano",
      "Empezando el invierno",
      "En otoño"
    ],
    "m": "Guardar el abrigo por meses sugiere que viene el calor."
  },
  {
    "q": "¿Qué es inferir?",
    "ops": [
      "Deducir algo que el texto no dice pero deja entender",
      "Copiar lo que dice el texto",
      "Inventar cualquier cosa"
    ],
    "m": "Se apoya en pistas del texto, no en la imaginación."
  }
];
GAMES.club_lectura_5 = juegoTriviaTexto(CUR_CLUB_LECTURA_5_BANCO, "Leé y respondé.", "club_lectu");

/* 6° · Números gigantes — numeros_gigantes_6
   DC: Lectura, orden y valor posicional sin restricción de rango
   Fuente: docs/auditoria-dc-caba/grado-6.md · M1 */
const CUR_NUMEROS_GIGANTES_6_PLANTILLA = {
  "q": "¿Qué número es {a} millones {b} mil {c}?",
  "vars": {
    "a": {
      "rango": [
        2,
        89
      ],
      "paso": 1
    },
    "b": {
      "rango": [
        1,
        999
      ],
      "paso": 1
    },
    "c": {
      "rango": [
        1,
        999
      ],
      "paso": 1
    }
  },
  "ok": "a * 1000000 + b * 1000 + c",
  "distractores": [
    "a * 1000 + b * 1000 + c",
    "a * 1000000 + b * 100 + c",
    "a * 100000 + b * 1000 + c"
  ],
  "tope": 100000000,
  "m": "Cada clase ocupa TRES lugares. Si los miles son {b}, hay que completar con ceros hasta llenarlos. Da {ok}."
};
GAMES.numeros_gigantes_6 = juegoParametrico(CUR_NUMEROS_GIGANTES_6_PLANTILLA, "Escribí el número.", "numeros_gi");

/* 6° · Armá el cálculo — jerarquia_6
   DC: Operaciones combinadas y jerarquía; uso del paréntesis
   Fuente: docs/auditoria-dc-caba/grado-6.md · M4 */
const CUR_JERARQUIA_6_PLANTILLA = {
  "q": "{a} + {b} × {c}",
  "vars": {
    "a": {
      "rango": [
        3,
        60
      ],
      "paso": 1
    },
    "b": {
      "rango": [
        2,
        12
      ],
      "paso": 1
    },
    "c": {
      "rango": [
        2,
        12
      ],
      "paso": 1
    }
  },
  "ok": "a + b * c",
  "distractores": [
    "(a + b) * c",
    "a + b + c",
    "a * b + c"
  ],
  "tope": 1000,
  "m": "Sin paréntesis, la multiplicación va PRIMERO: {b} × {c}, y a eso le sumás {a}. Da {ok}. Si resolvés de izquierda a derecha te da otra cosa."
};
GAMES.jerarquia_6 = juegoParametrico(CUR_JERARQUIA_6_PLANTILLA, "Respetá el orden de las operaciones.", "jerarquia_");

/* 6° · Reconstruí la división — reconstruir_division_6
   DC: Relación c×d+r=D con r<d; restos posibles e imposibles
   Fuente: docs/auditoria-dc-caba/grado-6.md · M5 */
const CUR_RECONSTRUIR_DIVISION_6_PLANTILLA = {
  "q": "Una división da cociente {a} y resto {c}, con divisor {b}. ¿Cuál era el dividendo?",
  "vars": {
    "a": {
      "rango": [
        4,
        40
      ],
      "paso": 1
    },
    "b": {
      "rango": [
        5,
        12
      ],
      "paso": 1
    },
    "c": {
      "rango": [
        1,
        4
      ],
      "paso": 1
    }
  },
  "ok": "a * b + c",
  "distractores": [
    "a * b",
    "a * b - c",
    "a + b + c"
  ],
  "tope": 600,
  "m": "El resto es lo que sobró, así que se SUMA: {a} × {b} + {c} = {ok}. Si te olvidás del resto, te falta {c}."
};
GAMES.reconstruir_division_6 = juegoParametrico(CUR_RECONSTRUIR_DIVISION_6_PLANTILLA, "Encontrá el dividendo.", "reconstrui");

/* 6° · Podio de permutaciones — permutaciones_6
   DC: Combinatoria: permutaciones; combinación de dos conjuntos
   Fuente: docs/auditoria-dc-caba/grado-6.md · M6 */
const CUR_PERMUTACIONES_6_PLANTILLA = {
  "q": "Corren {a} chicos. ¿De cuántas formas distintas pueden quedar el 1° y el 2° puesto?",
  "vars": {
    "a": {
      "rango": [
        4,
        25
      ],
      "paso": 1
    }
  },
  "ok": "a * (a - 1)",
  "distractores": [
    "a * a",
    "a + a",
    "a * (a - 2)"
  ],
  "tope": 1000,
  "m": "Para el 1° hay {a} candidatos; para el 2°, uno MENOS, porque el que salió primero ya no puede repetir. Da {ok}. Multiplicar {a} × {a} es el error típico: cuenta al mismo chico dos veces."
};
GAMES.permutaciones_6 = juegoParametrico(CUR_PERMUTACIONES_6_PLANTILLA, "¿De cuántas formas distintas?", "permutacio");

/* 6° · Fracción de una cantidad — fraccion_cantidad_6
   DC: Fracción de un natural con numerador distinto de 1, sin tope de rango
   Fuente: docs/auditoria-dc-caba/grado-6.md · M7 */
const CUR_FRACCION_CANTIDAD_6_PLANTILLA = {
  "q": "¿Cuánto es {n}/{d} de {a}?",
  "vars": {
    "d": {
      "opciones": [
        4,
        5,
        6,
        8,
        10
      ]
    },
    "n": {
      "opciones": [
        2,
        3
      ]
    },
    "a": {
      "rango": [
        120,
        960
      ],
      "paso": 120
    }
  },
  "ok": "a * n / d",
  "distractores": [
    "a / d",
    "a * n",
    "a - a / d"
  ],
  "tope": 2000,
  "m": "Primero cuánto vale UNA parte: {a} ÷ {d}. Después multiplicás por {n}. Da {ok}. Quedarse en la división es el error más común."
};
GAMES.fraccion_cantidad_6 = juegoParametrico(CUR_FRACCION_CANTIDAD_6_PLANTILLA, "¿Cuánto es esa parte?", "fraccion_c");

/* 6° · Porcentaje de una cantidad — porcentaje_cantidad_6
   DC: Cálculo del porcentaje de una cantidad
   Fuente: docs/auditoria-dc-caba/grado-6.md · M13b */
const CUR_PORCENTAJE_CANTIDAD_6_PLANTILLA = {
  "q": "¿Cuánto es el {p}% de {a}?",
  "vars": {
    "p": {
      "opciones": [
        10,
        15,
        20,
        25,
        30,
        40,
        50,
        60,
        75
      ]
    },
    "a": {
      "rango": [
        200,
        9800
      ],
      "paso": 200
    }
  },
  "ok": "a * p / 100",
  "distractores": [
    "a * p / 1000",
    "a - a * p / 100",
    "a / 10"
  ],
  "tope": 10000,
  "m": "El {p}% es {p} de cada 100: {a} × {p} ÷ 100 = {ok}. Ojo con dos errores — correr mal la coma, y calcular lo que QUEDA en vez de lo que se saca."
};
GAMES.porcentaje_cantidad_6 = juegoParametrico(CUR_PORCENTAJE_CANTIDAD_6_PLANTILLA, "Sacá el porcentaje.", "porcentaje");

/* 6° · La tienda de descuentos — descuentos_6
   DC: Descuentos y aumentos; elegir la oferta conveniente
   Fuente: docs/auditoria-dc-caba/grado-6.md · M13 */
const CUR_DESCUENTOS_6_PLANTILLA = {
  "q": "Una campera sale ${a} y tiene {p}% de descuento. ¿Cuánto pagás?",
  "vars": {
    "p": {
      "opciones": [
        10,
        20,
        25,
        30,
        40,
        50
      ]
    },
    "a": {
      "rango": [
        2000,
        40000
      ],
      "paso": 500
    }
  },
  "ok": "a - a * p / 100",
  "distractores": [
    "a * p / 100",
    "a + a * p / 100",
    "a - p"
  ],
  "tope": 50000,
  "m": "El {p}% de ${a} es el descuento, no el precio final: hay que RESTARLO. Pagás ${ok}. Contestar el descuento en vez del precio es el error clásico."
};
GAMES.descuentos_6 = juegoParametrico(CUR_DESCUENTOS_6_PLANTILLA, "¿Cuánto pagás al final?", "descuentos");

/* 6° · Proporcionalidad aplicada — proporcionalidad_6
   DC: Proporcionalidad directa; escalas; constante de proporcionalidad
   Fuente: docs/auditoria-dc-caba/grado-6.md · M14 */
const CUR_PROPORCIONALIDAD_6_PLANTILLA = {
  "q": "Si {a} alfajores cuestan ${b}, ¿cuánto cuestan {c} alfajores?",
  "vars": {
    "a": {
      "opciones": [
        2,
        3,
        4,
        5,
        6
      ]
    },
    "b": {
      "rango": [
        600,
        3600
      ],
      "paso": 300
    },
    "c": {
      "rango": [
        7,
        20
      ],
      "paso": 1
    }
  },
  "ok": "b * c / a",
  "distractores": [
    "b * c",
    "b + c",
    "b * a"
  ],
  "tope": 100000,
  "m": "Primero cuánto sale UNO: ${b} ÷ {a}. Después multiplicás por {c}. Da ${ok}. Multiplicar el precio total por {c} es el error típico."
};
GAMES.proporcionalidad_6 = juegoParametrico(CUR_PROPORCIONALIDAD_6_PLANTILLA, "Mantené la proporción.", "proporcion");

/* 6° · Resolvé el problema — problemas_varios_pasos_6
   DC: Problemas de varios pasos; decidir qué operación resuelve
   Fuente: docs/auditoria-dc-caba/grado-6.md · Mprob */
const CUR_PROBLEMAS_VARIOS_PASOS_6_PLANTILLA = {
  "q": "Un micro lleva {a} filas de {b} asientos. Si {c} asientos están rotos, ¿cuántos quedan para usar?",
  "vars": {
    "a": {
      "rango": [
        8,
        30
      ],
      "paso": 1
    },
    "b": {
      "opciones": [
        2,
        3,
        4,
        5
      ]
    },
    "c": {
      "rango": [
        3,
        25
      ],
      "paso": 1
    }
  },
  "ok": "a * b - c",
  "distractores": [
    "a * b + c",
    "a * b",
    "a + b - c"
  ],
  "tope": 200,
  "m": "Son DOS pasos: primero el total ({a} × {b}) y recién después restás los {c} rotos. Da {ok}. Quedarse en el total es el error más común."
};
GAMES.problemas_varios_pasos_6 = juegoParametrico(CUR_PROBLEMAS_VARIOS_PASOS_6_PLANTILLA, "Leé bien y resolvé.", "problemas_");

/* 6° · Criba de primos — primos_6
   DC: Primos y compuestos; múltiplos y divisores comunes
   Fuente: docs/auditoria-dc-caba/grado-6.md · M2 */
const CUR_PRIMOS_6_BANCO = [
  {
    "q": "¿Cuál de estos es primo?",
    "ops": [
      "17",
      "21",
      "27"
    ],
    "m": "21 = 3 × 7 y 27 = 3 × 9. El 17 no sale de ninguna multiplicación de dos números menores."
  },
  {
    "q": "¿Cuál de estos NO es primo?",
    "ops": [
      "51",
      "53",
      "59"
    ],
    "m": "51 = 3 × 17. Que termine en 1 no lo hace primo: hay que probar los divisores."
  },
  {
    "q": "¿Por qué el 1 no es primo?",
    "ops": [
      "Porque tiene un solo divisor",
      "Porque es impar",
      "Porque es muy chico"
    ],
    "m": "Para ser primo hacen falta DOS divisores distintos, y el 1 sólo se divide por 1."
  },
  {
    "q": "¿Cuál es el único primo par?",
    "ops": [
      "El 2",
      "El 4",
      "Ninguno"
    ],
    "m": "Todos los otros pares se dividen por 2, así que tienen un tercer divisor."
  },
  {
    "q": "¿Cuántos divisores tiene un número primo?",
    "ops": [
      "Exactamente dos",
      "Uno solo",
      "Depende del número"
    ],
    "m": "Siempre dos: el 1 y él mismo. Ni más ni menos."
  },
  {
    "q": "¿Cuál de estos es compuesto?",
    "ops": [
      "91",
      "89",
      "97"
    ],
    "m": "91 = 7 × 13. Los otros dos son primos, aunque no se note a simple vista."
  },
  {
    "q": "¿Cuál es el máximo común divisor de 12 y 18?",
    "ops": [
      "6",
      "3",
      "36"
    ],
    "m": "Los divisores comunes son 1, 2, 3 y 6. El MAYOR de ellos es 6. 36 es el múltiplo, no el divisor."
  },
  {
    "q": "¿Cuál es el mínimo común múltiplo de 4 y 6?",
    "ops": [
      "12",
      "24",
      "10"
    ],
    "m": "Los múltiplos comunes son 12, 24, 36… El MENOR es 12. 24 también es común, pero no es el mínimo."
  },
  {
    "q": "¿Cuántos números primos hay entre 1 y 10?",
    "ops": [
      "Cuatro: 2, 3, 5 y 7",
      "Cinco, contando el 1",
      "Tres: 3, 5 y 7"
    ],
    "m": "El 1 no cuenta y el 2 sí, aunque sea par."
  },
  {
    "q": "El 15 y el 28, ¿tienen algún divisor común además del 1?",
    "ops": [
      "No, ninguno",
      "Sí, el 3",
      "Sí, el 5"
    ],
    "m": "15 = 3 × 5 y 28 = 2 × 2 × 7. No comparten ningún factor: se llaman coprimos."
  },
  {
    "q": "¿Cómo se descompone 30 en factores primos?",
    "ops": [
      "2 × 3 × 5",
      "5 × 6",
      "2 × 15"
    ],
    "m": "Hay que llegar hasta que TODOS los factores sean primos. 6 y 15 todavía se pueden partir."
  },
  {
    "q": "¿Es 1 divisor de todos los números?",
    "ops": [
      "Sí, de todos",
      "Sólo de los impares",
      "No, de ninguno"
    ],
    "m": "Cualquier número dividido 1 da él mismo, sin resto."
  },
  {
    "q": "¿Cuál de estos es múltiplo de 7 y de 3 a la vez?",
    "ops": [
      "42",
      "35",
      "27"
    ],
    "m": "42 = 7 × 6 = 3 × 14. Los otros dos son múltiplos de uno solo de los dos."
  },
  {
    "q": "Si un número termina en 5, ¿puede ser primo?",
    "ops": [
      "Sólo el 5 mismo",
      "Sí, muchos",
      "No, nunca"
    ],
    "m": "Todos los que terminan en 5 se dividen por 5; el único que zafa es el propio 5."
  },
  {
    "q": "¿Cuántos divisores tiene el 16?",
    "ops": [
      "Cinco: 1, 2, 4, 8 y 16",
      "Cuatro: 1, 2, 8 y 16",
      "Dos: 1 y 16"
    ],
    "m": "No hay que olvidarse del 4, que es 16 ÷ 4. Los divisores van de a pares salvo la raíz."
  },
  {
    "q": "¿Qué significa que 24 sea múltiplo de 8?",
    "ops": [
      "Que 24 contiene a 8 una cantidad exacta de veces",
      "Que 8 es más grande",
      "Que 24 y 8 son primos"
    ],
    "m": "24 ÷ 8 = 3 sin resto. Múltiplo y divisor son las dos caras de lo mismo."
  }
];
GAMES.primos_6 = juegoTriviaTexto(CUR_PRIMOS_6_BANCO, "Pensá en cuántos divisores tiene.", "primos_6");

/* 6° · Detector de divisibilidad — divisibilidad_criterios_6
   DC: Criterios de divisibilidad por 2, 5 y 10
   Fuente: docs/auditoria-dc-caba/grado-6.md · M3 */
const CUR_DIVISIBILIDAD_CRITERIOS_6_BANCO = [
  {
    "it": "48",
    "cat": "dos",
    "m": "Termina en 8, que es par: por 2. No termina en 0 ni 5."
  },
  {
    "it": "35",
    "cat": "cinco",
    "m": "Termina en 5: por 5. Pero 5 es impar, así que por 2 no."
  },
  {
    "it": "70",
    "cat": "diez",
    "m": "Termina en 0: por 2, por 5 y por 10, las tres."
  },
  {
    "it": "27",
    "cat": "ninguno",
    "m": "Impar y no termina en 0 ni 5: por ninguno de los tres."
  },
  {
    "it": "156",
    "cat": "dos",
    "m": "Termina en 6, par. Mirá SIEMPRE la última cifra, no el número entero."
  },
  {
    "it": "205",
    "cat": "cinco",
    "m": "Termina en 5: por 5 sí, por 2 no."
  },
  {
    "it": "340",
    "cat": "diez",
    "m": "Termina en 0: las tres a la vez."
  },
  {
    "it": "119",
    "cat": "ninguno",
    "m": "Impar y no termina en 0 ni 5."
  },
  {
    "it": "94",
    "cat": "dos",
    "m": "Termina en 4: par."
  },
  {
    "it": "1.005",
    "cat": "cinco",
    "m": "Termina en 5. Que sea grande no cambia el criterio."
  },
  {
    "it": "1.200",
    "cat": "diez",
    "m": "Termina en 0, así que entra en las tres."
  },
  {
    "it": "83",
    "cat": "ninguno",
    "m": "Impar, no termina en 0 ni 5."
  },
  {
    "it": "62",
    "cat": "dos",
    "m": "Par, y no termina en 0 ni 5."
  },
  {
    "it": "455",
    "cat": "cinco",
    "m": "Termina en 5: por 5. Impar, así que por 2 no."
  },
  {
    "it": "890",
    "cat": "diez",
    "m": "Termina en 0: las tres."
  },
  {
    "it": "247",
    "cat": "ninguno",
    "m": "Impar y no termina en 0 ni 5."
  },
  {
    "it": "308",
    "cat": "dos",
    "m": "Termina en 8: par."
  },
  {
    "it": "75",
    "cat": "cinco",
    "m": "Termina en 5, pero es impar: sólo por 5."
  },
  {
    "it": "560",
    "cat": "diez",
    "m": "Termina en 0: las tres."
  },
  {
    "it": "391",
    "cat": "ninguno",
    "m": "Impar y no termina en 0 ni 5."
  }
];
GAMES.divisibilidad_criterios_6 = juegoClasificar(CUR_DIVISIBILIDAD_CRITERIOS_6_BANCO, "Mirá la última cifra: ¿por cuál se divide?", [{"cat": "dos", "label": "2️⃣ Sólo por 2"}, {"cat": "cinco", "label": "5️⃣ Sólo por 5"}, {"cat": "diez", "label": "🔟 Por 2, 5 y 10"}, {"cat": "ninguno", "label": "🚫 Por ninguno"}], "divisibili");

/* 6° · Fracciones equivalentes — fracciones_equivalentes_6
   DC: Equivalencia de fracciones: amplificar y simplificar
   Fuente: docs/auditoria-dc-caba/grado-6.md · M7b */
const CUR_FRACCIONES_EQUIVALENTES_6_BANCO = [
  {
    "q": "¿Cuál es equivalente a 1/2?",
    "ops": [
      "3/6",
      "2/3",
      "1/4"
    ],
    "m": "1/2 amplificada por 3 da 3/6. En 2/3 se sumó 1 a cada lado, y eso SÍ cambia el valor."
  },
  {
    "q": "¿Cuál es equivalente a 2/3?",
    "ops": [
      "8/12",
      "3/4",
      "4/9"
    ],
    "m": "2/3 × 4/4 = 8/12. En 4/9 se multiplicó arriba por 2 y abajo por 3: distinto factor, distinto valor."
  },
  {
    "q": "Simplificá 6/8 al mínimo.",
    "ops": [
      "3/4",
      "2/4",
      "6/8 ya está"
    ],
    "m": "Se dividen los dos por 2. 2/4 todavía se puede seguir simplificando."
  },
  {
    "q": "Simplificá 15/25 al mínimo.",
    "ops": [
      "3/5",
      "5/5",
      "15/5"
    ],
    "m": "Los dos se dividen por 5. Hay que dividir ARRIBA y ABAJO, no sólo uno."
  },
  {
    "q": "¿Cuál es equivalente a 3/4?",
    "ops": [
      "9/12",
      "4/5",
      "6/12"
    ],
    "m": "3/4 × 3/3 = 9/12. 6/12 es la mitad, no tres cuartos."
  },
  {
    "q": "Si a 2/5 le multiplico arriba y abajo por 4, ¿qué obtengo?",
    "ops": [
      "8/20",
      "8/5",
      "2/20"
    ],
    "m": "Hay que multiplicar los DOS. Tocar uno solo cambia el valor de la fracción."
  },
  {
    "q": "¿4/6 y 2/3 valen lo mismo?",
    "ops": [
      "Sí, 4/6 simplificada da 2/3",
      "No, 4/6 es mayor",
      "No, 2/3 es mayor"
    ],
    "m": "Dividís arriba y abajo por 2 y llegás a la misma fracción."
  },
  {
    "q": "¿Cuál NO es equivalente a 1/3?",
    "ops": [
      "2/9",
      "2/6",
      "5/15"
    ],
    "m": "2/6 y 5/15 salen de amplificar 1/3. En 2/9 el de arriba se duplicó y el de abajo se triplicó."
  },
  {
    "q": "Simplificá 12/18 al mínimo.",
    "ops": [
      "2/3",
      "6/9",
      "4/6"
    ],
    "m": "Hay que dividir por 6, el máximo común divisor. 6/9 y 4/6 todavía se pueden seguir."
  },
  {
    "q": "¿Cuánto vale 5/5?",
    "ops": [
      "1 entero",
      "5",
      "1/5"
    ],
    "m": "Cuando arriba y abajo son iguales, están todas las partes: es el entero completo."
  },
  {
    "q": "¿Cuál es equivalente a 10/20?",
    "ops": [
      "1/2",
      "10/2",
      "1/20"
    ],
    "m": "Los dos se dividen por 10. Es la mitad."
  },
  {
    "q": "¿Por qué 3/6 y 1/2 son la misma cantidad?",
    "ops": [
      "Porque 3/6 se simplifica dividiendo por 3",
      "Porque 3 y 6 son parecidos",
      "Porque las dos tienen números chicos"
    ],
    "m": "Dos fracciones son equivalentes cuando una sale de la otra multiplicando o dividiendo los dos términos."
  },
  {
    "q": "¿Cuál es equivalente a 7/10?",
    "ops": [
      "70/100",
      "7/100",
      "17/20"
    ],
    "m": "Se amplificó por 10 arriba y abajo. 7/100 sólo movió el de abajo."
  },
  {
    "q": "Simplificá 20/30 al mínimo.",
    "ops": [
      "2/3",
      "10/15",
      "20/3"
    ],
    "m": "Se dividen por 10. 10/15 todavía se puede dividir por 5."
  },
  {
    "q": "¿Se puede simplificar 7/9?",
    "ops": [
      "No, no tienen divisores comunes",
      "Sí, da 1/3",
      "Sí, da 7/3"
    ],
    "m": "7 es primo y no divide a 9: la fracción ya está en su mínima expresión."
  },
  {
    "q": "¿Cuál de estas es MAYOR: 3/4 o 5/8?",
    "ops": [
      "3/4",
      "5/8",
      "Son iguales"
    ],
    "m": "Llevalas al mismo denominador: 3/4 = 6/8, y 6/8 es más que 5/8. El de arriba más grande no gana solo."
  }
];
GAMES.fracciones_equivalentes_6 = juegoTriviaTexto(CUR_FRACCIONES_EQUIVALENTES_6_BANCO, "Buscá la que vale lo mismo.", "fracciones");

/* 6° · Zoom en la recta — densidad_recta_6
   DC: Densidad y orden de fracciones y decimales en la recta numérica
   Fuente: docs/auditoria-dc-caba/grado-6.md · M8 */
const CUR_DENSIDAD_RECTA_6_BANCO = [
  {
    "q": "¿Qué número está entre 0,3 y 0,4?",
    "ops": [
      "0,35",
      "0,5",
      "0,25"
    ],
    "m": "Agregando un decimal más aparecen números en el medio: 0,35 cae justo entre los dos."
  },
  {
    "q": "¿Cuántos números hay entre 1,2 y 1,3?",
    "ops": [
      "Infinitos",
      "Ninguno",
      "Nueve"
    ],
    "m": "Siempre podés agregar un decimal más y encontrar otro. Eso se llama densidad."
  },
  {
    "q": "¿Qué número está entre 1/2 y 1?",
    "ops": [
      "3/4",
      "1/4",
      "2/2"
    ],
    "m": "3/4 es más que la mitad y menos que el entero. 2/2 ES el entero."
  },
  {
    "q": "¿Cuál es MAYOR: 0,7 o 0,65?",
    "ops": [
      "0,7",
      "0,65",
      "Son iguales"
    ],
    "m": "0,7 es 0,70. Que 65 tenga más cifras no lo hace más grande."
  },
  {
    "q": "¿Cuál es MENOR: 0,5 o 0,45?",
    "ops": [
      "0,45",
      "0,5",
      "Son iguales"
    ],
    "m": "0,5 es 0,50, y 45 centésimos es menos que 50 centésimos."
  },
  {
    "q": "¿Qué fracción está entre 0 y 1/2?",
    "ops": [
      "1/4",
      "3/4",
      "2/3"
    ],
    "m": "1/4 es la mitad de la mitad. Las otras dos pasan de 1/2."
  },
  {
    "q": "Ordenados de menor a mayor: 0,8 · 0,08 · 0,88",
    "ops": [
      "0,08 · 0,8 · 0,88",
      "0,8 · 0,08 · 0,88",
      "0,08 · 0,88 · 0,8"
    ],
    "m": "0,08 son 8 centésimos, mucho menos que 0,8 que son 8 décimos."
  },
  {
    "q": "¿Cuál es MAYOR: 2/3 o 3/5?",
    "ops": [
      "2/3",
      "3/5",
      "Son iguales"
    ],
    "m": "Al mismo denominador: 10/15 contra 9/15. Gana 2/3, por poco."
  },
  {
    "q": "¿Qué número está justo entre 2 y 3?",
    "ops": [
      "2,5",
      "2,05",
      "3,5"
    ],
    "m": "2,5 es dos y medio. 2,05 está casi pegado al 2."
  },
  {
    "q": "¿0,5 y 1/2 son el mismo punto de la recta?",
    "ops": [
      "Sí, el mismo",
      "No, 0,5 es menor",
      "No, 1/2 es menor"
    ],
    "m": "Son dos escrituras de la misma cantidad: la mitad del entero."
  },
  {
    "q": "¿Qué número está entre 0,99 y 1?",
    "ops": [
      "0,995",
      "0,9",
      "1,1"
    ],
    "m": "Aunque parezcan pegados, siempre entra otro en el medio."
  },
  {
    "q": "¿Cuál es MAYOR: 1,4 o 1,40?",
    "ops": [
      "Son iguales",
      "1,40",
      "1,4"
    ],
    "m": "El cero final no agrega valor: 1,4 = 1,40 = 1,400."
  },
  {
    "q": "¿Dónde cae 7/2 en la recta?",
    "ops": [
      "Entre 3 y 4",
      "Entre 7 y 8",
      "Entre 1 y 2"
    ],
    "m": "7/2 es 3 enteros y medio. Cuando el de arriba es más grande, la fracción pasa del 1."
  },
  {
    "q": "¿Cuál es MENOR: 3/8 o 1/2?",
    "ops": [
      "3/8",
      "1/2",
      "Son iguales"
    ],
    "m": "1/2 son 4/8. Con el mismo denominador se ve enseguida."
  },
  {
    "q": "¿Qué número está entre 5,1 y 5,2?",
    "ops": [
      "5,15",
      "5,01",
      "5,21"
    ],
    "m": "Hay que mirar el segundo decimal: 5,15 cae justo en el medio."
  }
];
GAMES.densidad_recta_6 = juegoTriviaTexto(CUR_DENSIDAD_RECTA_6_BANCO, "Ubicá el número entre los otros dos.", "densidad_r");

/* 6° · Suma y resta de fracciones — suma_fracciones_6
   DC: Suma y resta con distinto denominador
   Fuente: docs/auditoria-dc-caba/grado-6.md · M8b */
const CUR_SUMA_FRACCIONES_6_BANCO = [
  {
    "q": "1/2 + 1/3 =",
    "ops": [
      "5/6",
      "2/5",
      "2/6"
    ],
    "m": "No se suman los de abajo. Llevá las dos a sextos: 3/6 + 2/6 = 5/6."
  },
  {
    "q": "1/4 + 1/4 =",
    "ops": [
      "2/4",
      "2/8",
      "1/8"
    ],
    "m": "Con el mismo denominador se suman sólo los de arriba: el tamaño de la parte no cambia."
  },
  {
    "q": "3/4 − 1/2 =",
    "ops": [
      "1/4",
      "2/2",
      "2/4"
    ],
    "m": "1/2 son 2/4. Entonces 3/4 − 2/4 = 1/4."
  },
  {
    "q": "1/3 + 1/6 =",
    "ops": [
      "1/2",
      "2/9",
      "2/6"
    ],
    "m": "1/3 son 2/6. Entonces 2/6 + 1/6 = 3/6, que simplificado es 1/2."
  },
  {
    "q": "¿Por qué 1/2 + 1/3 NO es 2/5?",
    "ops": [
      "Porque los de abajo no se suman",
      "Porque 2/5 es muy chico",
      "Porque hay que restar"
    ],
    "m": "El de abajo dice el TAMAÑO de la parte. Sumarlos achica las partes en vez de juntarlas."
  },
  {
    "q": "2/5 + 1/5 =",
    "ops": [
      "3/5",
      "3/10",
      "2/10"
    ],
    "m": "Mismo denominador: se suman los de arriba y abajo queda igual."
  },
  {
    "q": "1/2 − 1/4 =",
    "ops": [
      "1/4",
      "0/2",
      "1/2"
    ],
    "m": "1/2 son 2/4. Entonces 2/4 − 1/4 = 1/4."
  },
  {
    "q": "Para sumar 1/3 + 1/4, ¿qué denominador común conviene?",
    "ops": [
      "12",
      "7",
      "34"
    ],
    "m": "12 es el mínimo común múltiplo de 3 y 4. Sumar los denominadores no sirve."
  },
  {
    "q": "1/3 + 1/4 =",
    "ops": [
      "7/12",
      "2/7",
      "2/12"
    ],
    "m": "4/12 + 3/12 = 7/12. Sumar arriba y abajo da 2/7, que es MENOS que 1/3 solo."
  },
  {
    "q": "5/6 − 1/3 =",
    "ops": [
      "1/2",
      "4/3",
      "4/6"
    ],
    "m": "1/3 son 2/6. Entonces 5/6 − 2/6 = 3/6 = 1/2."
  },
  {
    "q": "1/2 + 1/2 =",
    "ops": [
      "1 entero",
      "2/4",
      "1/4"
    ],
    "m": "Dos mitades arman el entero. 2/4 es la mitad, no el entero."
  },
  {
    "q": "3/8 + 1/8 =",
    "ops": [
      "1/2",
      "4/16",
      "3/16"
    ],
    "m": "4/8 simplificado es 1/2. El denominador no se toca."
  },
  {
    "q": "2/3 − 1/6 =",
    "ops": [
      "1/2",
      "1/3",
      "1/6"
    ],
    "m": "2/3 son 4/6. Entonces 4/6 − 1/6 = 3/6 = 1/2."
  },
  {
    "q": "Al sumar dos fracciones con el mismo denominador, ¿qué pasa con el de abajo?",
    "ops": [
      "Queda igual",
      "Se suma",
      "Se multiplica"
    ],
    "m": "El de abajo dice en cuántas partes está cortado el entero, y eso no cambia por juntar partes."
  },
  {
    "q": "1/4 + 2/3 =",
    "ops": [
      "11/12",
      "3/7",
      "3/12"
    ],
    "m": "3/12 + 8/12 = 11/12. Casi un entero."
  },
  {
    "q": "¿Cuánto le falta a 3/4 para llegar al entero?",
    "ops": [
      "1/4",
      "1/2",
      "4/4"
    ],
    "m": "El entero es 4/4. Si ya tenés 3/4, falta una parte de cuatro."
  }
];
GAMES.suma_fracciones_6 = juegoTriviaTexto(CUR_SUMA_FRACCIONES_6_BANCO, "Igualá los de abajo antes de sumar.", "suma_fracc");

/* 6° · Parejas que dan 1 — fraccion_inversa_6
   DC: Fracción inversa: el producto de una fracción por su inversa da 1
   Fuente: docs/auditoria-dc-caba/grado-6.md · M9 */
const CUR_FRACCION_INVERSA_6_BANCO = [
  {
    "q": "¿Cuál es la inversa de 2/3?",
    "ops": [
      "3/2",
      "2/3",
      "1/3"
    ],
    "m": "Se dan vuelta los dos términos. 2/3 × 3/2 = 6/6 = 1."
  },
  {
    "q": "¿Cuál es la inversa de 5?",
    "ops": [
      "1/5",
      "5/1",
      "−5"
    ],
    "m": "5 es 5/1; dado vuelta queda 1/5. Y 5 × 1/5 = 1."
  },
  {
    "q": "¿Cuánto da 3/4 × 4/3?",
    "ops": [
      "1",
      "12/12 y algo más",
      "7/7"
    ],
    "m": "Arriba y abajo queda 12: 12/12 es el entero."
  },
  {
    "q": "¿Cuál es la inversa de 1/7?",
    "ops": [
      "7",
      "1/7",
      "7/7"
    ],
    "m": "1/7 dado vuelta es 7/1, que es 7."
  },
  {
    "q": "¿Qué número NO tiene inversa?",
    "ops": [
      "El 0",
      "El 1",
      "El 10"
    ],
    "m": "Habría que dividir por cero, y eso no se puede hacer."
  },
  {
    "q": "¿Cuál es la inversa de 1?",
    "ops": [
      "1",
      "0",
      "−1"
    ],
    "m": "1 es 1/1; dado vuelta sigue siendo 1/1."
  },
  {
    "q": "Si multiplico 7/9 por su inversa, ¿qué obtengo?",
    "ops": [
      "1",
      "0",
      "7/9"
    ],
    "m": "Siempre 1: para eso está definida la inversa."
  },
  {
    "q": "¿Cuál es la inversa de 9/4?",
    "ops": [
      "4/9",
      "9/4",
      "4/4"
    ],
    "m": "Se dan vuelta los dos términos, no sólo uno."
  },
  {
    "q": "¿Por qué la inversa de una fracción se llama así?",
    "ops": [
      "Porque invierte el lugar del numerador y el denominador",
      "Porque le cambia el signo",
      "Porque la hace más chica"
    ],
    "m": "Invertir es dar vuelta, no cambiar el signo."
  },
  {
    "q": "¿Cuánto da 1/2 × 2?",
    "ops": [
      "1",
      "1/2",
      "4"
    ],
    "m": "2 es la inversa de 1/2, así que el producto es el entero."
  },
  {
    "q": "¿Cuál es la inversa de 10/3?",
    "ops": [
      "3/10",
      "10/3",
      "3/3"
    ],
    "m": "Dada vuelta: el 10 baja y el 3 sube."
  },
  {
    "q": "Dividir por 2 es lo mismo que multiplicar por…",
    "ops": [
      "1/2",
      "2",
      "1/4"
    ],
    "m": "Dividir por un número es multiplicar por su inversa. Por eso 8 ÷ 2 = 8 × 1/2 = 4."
  },
  {
    "q": "¿Cuánto da 6/5 × 5/6?",
    "ops": [
      "1",
      "30/30 menos 1",
      "11/11"
    ],
    "m": "30/30, que es el entero completo."
  },
  {
    "q": "¿La inversa de una fracción menor que 1 es mayor o menor que 1?",
    "ops": [
      "Mayor que 1",
      "Menor que 1",
      "Siempre igual a 1"
    ],
    "m": "Si el de arriba era el chico, al dar vuelta pasa a ser el grande."
  }
];
GAMES.fraccion_inversa_6 = juegoTriviaTexto(CUR_FRACCION_INVERSA_6_BANCO, "Buscá la que da 1 al multiplicar.", "fraccion_i");

/* 6° · Área fraccionaria — area_fraccionaria_6
   DC: Multiplicación de fracciones interpretada como área
   Fuente: docs/auditoria-dc-caba/grado-6.md · M10 */
const CUR_AREA_FRACCIONARIA_6_BANCO = [
  {
    "q": "1/2 × 1/2 =",
    "ops": [
      "1/4",
      "1",
      "2/4"
    ],
    "m": "Es la mitad de la mitad, o sea un cuarto. Multiplicar fracciones ACHICA."
  },
  {
    "q": "1/2 × 1/3 =",
    "ops": [
      "1/6",
      "2/5",
      "1/5"
    ],
    "m": "Se multiplican arriba con arriba y abajo con abajo: 1×1 sobre 2×3."
  },
  {
    "q": "2/3 × 3/4 =",
    "ops": [
      "1/2",
      "5/7",
      "6/7"
    ],
    "m": "6/12, que simplificado es 1/2. Los de abajo se multiplican, no se suman."
  },
  {
    "q": "Si un patio mide 1/2 de la cuadra y pinto 1/3 del patio, ¿qué parte de la cuadra pinté?",
    "ops": [
      "1/6",
      "1/5",
      "2/3"
    ],
    "m": "Una parte de una parte: 1/2 × 1/3 = 1/6."
  },
  {
    "q": "¿Multiplicar por 1/2 agranda o achica?",
    "ops": [
      "Achica: es quedarse con la mitad",
      "Agranda: siempre que se multiplica crece",
      "No cambia nada"
    ],
    "m": "Con los enteros multiplicar agranda, pero con fracciones menores que 1 pasa al revés."
  },
  {
    "q": "3/4 × 1/2 =",
    "ops": [
      "3/8",
      "4/6",
      "3/6"
    ],
    "m": "3×1 = 3 arriba y 4×2 = 8 abajo."
  },
  {
    "q": "1/4 × 4 =",
    "ops": [
      "1",
      "1/16",
      "4/4 menos 1"
    ],
    "m": "Cuatro cuartos arman el entero."
  },
  {
    "q": "2/5 × 1/2 =",
    "ops": [
      "1/5",
      "3/7",
      "2/10 y algo más"
    ],
    "m": "2/10, que simplificado es 1/5. Es la mitad de dos quintos."
  },
  {
    "q": "En una cuadrícula de 4×5, pinto 3 filas de 2 columnas. ¿Qué parte pinté?",
    "ops": [
      "6/20",
      "5/9",
      "6/9"
    ],
    "m": "6 casilleros pintados de 20 en total. Ésa es la idea de área."
  },
  {
    "q": "¿Cómo se multiplican dos fracciones?",
    "ops": [
      "Arriba con arriba y abajo con abajo",
      "Buscando denominador común",
      "Dando vuelta la segunda y sumando"
    ],
    "m": "El denominador común hace falta para SUMAR, no para multiplicar."
  },
  {
    "q": "1/3 × 1/3 =",
    "ops": [
      "1/9",
      "2/6",
      "1/6"
    ],
    "m": "Un tercio de un tercio: el entero queda cortado en nueve."
  },
  {
    "q": "5/6 × 1 =",
    "ops": [
      "5/6",
      "5/12",
      "1"
    ],
    "m": "Multiplicar por el entero no cambia nada."
  },
  {
    "q": "3/5 × 5/3 =",
    "ops": [
      "1",
      "15/8",
      "8/8 menos algo"
    ],
    "m": "Son inversas: 15/15 es el entero."
  },
  {
    "q": "1/2 de 3/4 de una torta es…",
    "ops": [
      "3/8 de la torta",
      "3/6 de la torta",
      "1/4 de la torta"
    ],
    "m": "«De» es multiplicar: 1/2 × 3/4 = 3/8."
  }
];
GAMES.area_fraccionaria_6 = juegoTriviaTexto(CUR_AREA_FRACCIONARIA_6_BANCO, "Pensá la multiplicación como un pedazo de un pedazo.", "area_fracc");

/* 6° · Corredor de la coma — corredor_coma_6
   DC: Multiplicar y dividir por la unidad seguida de ceros; valor posicional decimal
   Fuente: docs/auditoria-dc-caba/grado-6.md · M11 */
const CUR_CORREDOR_COMA_6_BANCO = [
  {
    "q": "3,5 × 10 =",
    "ops": [
      "35",
      "3,50",
      "0,35"
    ],
    "m": "Un cero, un lugar a la DERECHA. Agregar un cero al final no cambia el valor."
  },
  {
    "q": "4,2 × 100 =",
    "ops": [
      "420",
      "42",
      "4,200"
    ],
    "m": "Dos ceros, dos lugares. Mover uno solo es el error más común."
  },
  {
    "q": "7 ÷ 10 =",
    "ops": [
      "0,7",
      "70",
      "0,07"
    ],
    "m": "Al dividir la coma va a la IZQUIERDA: el número se achica."
  },
  {
    "q": "0,8 × 1.000 =",
    "ops": [
      "800",
      "80",
      "8"
    ],
    "m": "Tres ceros, tres lugares a la derecha."
  },
  {
    "q": "56 ÷ 100 =",
    "ops": [
      "0,56",
      "5,6",
      "0,056"
    ],
    "m": "Dos lugares a la izquierda: 56 → 5,6 → 0,56."
  },
  {
    "q": "0,05 × 100 =",
    "ops": [
      "5",
      "0,5",
      "500"
    ],
    "m": "Dos lugares a la derecha: 0,05 → 0,5 → 5."
  },
  {
    "q": "¿Cuántos lugares se corre la coma al multiplicar por 1.000?",
    "ops": [
      "Tres",
      "Uno",
      "Cuatro"
    ],
    "m": "Tantos como ceros tenga el número: 1.000 tiene tres."
  },
  {
    "q": "1,25 × 10 =",
    "ops": [
      "12,5",
      "1,250",
      "125"
    ],
    "m": "Un lugar a la derecha, no dos."
  },
  {
    "q": "En 3,47, ¿qué vale la cifra 4?",
    "ops": [
      "4 décimos",
      "4 centésimos",
      "4 unidades"
    ],
    "m": "El primer lugar después de la coma son los décimos."
  },
  {
    "q": "En 0,209, ¿qué vale el 9?",
    "ops": [
      "9 milésimos",
      "9 centésimos",
      "9 décimos"
    ],
    "m": "Después de la coma van décimos, centésimos y milésimos, en ese orden."
  },
  {
    "q": "9,6 ÷ 10 =",
    "ops": [
      "0,96",
      "96",
      "9,06"
    ],
    "m": "Un lugar a la izquierda."
  },
  {
    "q": "0,4 × 10 =",
    "ops": [
      "4",
      "0,40",
      "40"
    ],
    "m": "Cuatro décimos por diez arma el entero 4."
  },
  {
    "q": "¿Es lo mismo 2,5 que 2,50?",
    "ops": [
      "Sí, el cero final no agrega valor",
      "No, 2,50 es mayor",
      "No, 2,5 es mayor"
    ],
    "m": "Después de la coma, los ceros al final no cambian la cantidad."
  },
  {
    "q": "120 ÷ 1.000 =",
    "ops": [
      "0,12",
      "1,2",
      "0,012"
    ],
    "m": "Tres lugares a la izquierda: 120 → 12 → 1,2 → 0,12."
  },
  {
    "q": "0,003 × 1.000 =",
    "ops": [
      "3",
      "0,3",
      "30"
    ],
    "m": "Tres lugares a la derecha vuelven a armar el entero."
  },
  {
    "q": "¿Qué es mayor: 0,4 o 0,40?",
    "ops": [
      "Son iguales",
      "0,40",
      "0,4"
    ],
    "m": "4 décimos y 40 centésimos son la misma cantidad."
  }
];
GAMES.corredor_coma_6 = juegoTriviaTexto(CUR_CORREDOR_COMA_6_BANCO, "Movés la coma tantos lugares como ceros.", "corredor_c");

/* 6° · Multiplicar con coma — multiplicar_coma_6
   DC: Multiplicación de decimales; cociente decimal
   Fuente: docs/auditoria-dc-caba/grado-6.md · M12 */
const CUR_MULTIPLICAR_COMA_6_BANCO = [
  {
    "q": "2,5 × 4 =",
    "ops": [
      "10",
      "8",
      "12,5"
    ],
    "m": "2,5 es 2 y medio: cuatro veces dos y medio son 10. Si te da 8, ignoraste el medio."
  },
  {
    "q": "3 ÷ 4 =",
    "ops": [
      "0,75",
      "1,33",
      "0,7"
    ],
    "m": "Tres repartido en cuatro da menos que uno. 1,33 sale de dividir al revés."
  },
  {
    "q": "0,5 × 6 =",
    "ops": [
      "3",
      "30",
      "0,30"
    ],
    "m": "Medio por seis es la mitad de seis."
  },
  {
    "q": "1,2 × 3 =",
    "ops": [
      "3,6",
      "36",
      "3,06"
    ],
    "m": "Un factor con un decimal da un resultado con un decimal."
  },
  {
    "q": "0,2 × 0,3 =",
    "ops": [
      "0,06",
      "0,6",
      "0,5"
    ],
    "m": "Un decimal más otro decimal son DOS decimales en el resultado. Y multiplicar decimales achica."
  },
  {
    "q": "1 ÷ 2 =",
    "ops": [
      "0,5",
      "2",
      "0,2"
    ],
    "m": "Un entero repartido entre dos es la mitad."
  },
  {
    "q": "2,5 × 2 =",
    "ops": [
      "5",
      "4,10",
      "4"
    ],
    "m": "Dos veces dos y medio son cinco."
  },
  {
    "q": "¿Cuántos decimales tiene el resultado de 1,5 × 2,5?",
    "ops": [
      "Dos",
      "Uno",
      "Ninguno"
    ],
    "m": "Se suman los decimales de los dos factores: uno más uno."
  },
  {
    "q": "7 ÷ 2 =",
    "ops": [
      "3,5",
      "3",
      "0,35"
    ],
    "m": "Sobra 1, que repartido entre 2 da 0,5. Quedarse en 3 es truncar el resto."
  },
  {
    "q": "0,1 × 0,1 =",
    "ops": [
      "0,01",
      "0,1",
      "1"
    ],
    "m": "Un décimo de un décimo es un centésimo. Multiplicar por menos de 1 achica."
  },
  {
    "q": "4,5 × 2 =",
    "ops": [
      "9",
      "8,10",
      "8"
    ],
    "m": "Cuatro y medio dos veces son nueve."
  },
  {
    "q": "1 ÷ 4 =",
    "ops": [
      "0,25",
      "4",
      "0,4"
    ],
    "m": "Un cuarto escrito con coma es 0,25."
  },
  {
    "q": "0,25 × 4 =",
    "ops": [
      "1",
      "0,100",
      "0,1"
    ],
    "m": "Cuatro cuartos arman el entero."
  },
  {
    "q": "6 ÷ 5 =",
    "ops": [
      "1,2",
      "1,1",
      "0,83"
    ],
    "m": "Da un poco más que uno, porque 6 es más que 5. 0,83 sale de dividir al revés."
  },
  {
    "q": "3,2 × 10 ÷ 4 =",
    "ops": [
      "8",
      "0,8",
      "80"
    ],
    "m": "Primero 32, después repartido en cuatro."
  },
  {
    "q": "¿Multiplicar por 0,5 es lo mismo que…?",
    "ops": [
      "Dividir por 2",
      "Multiplicar por 2",
      "Restar 2"
    ],
    "m": "0,5 es la mitad, así que multiplicar por 0,5 parte al medio."
  }
];
GAMES.multiplicar_coma_6 = juegoTriviaTexto(CUR_MULTIPLICAR_COMA_6_BANCO, "Contá los decimales antes de contestar.", "multiplica");

/* 6° · Cuadriláteros y ángulos — cuadrilateros_6
   DC: Mediatriz; paralelogramos; suma de ángulos interiores de un cuadrilátero
   Fuente: docs/auditoria-dc-caba/grado-6.md · M15a */
const CUR_CUADRILATEROS_6_BANCO = [
  {
    "q": "¿Cuánto suman los ángulos interiores de un cuadrilátero?",
    "ops": [
      "360°",
      "180°",
      "90°"
    ],
    "m": "180° es el triángulo. Un cuadrilátero se parte en DOS triángulos: 180 × 2.",
    "dib": "cuadrilatero"
  },
  {
    "q": "Tres ángulos de un cuadrilátero miden 90°, 90° y 100°. ¿Cuánto mide el cuarto?",
    "ops": [
      "80°",
      "90°",
      "100°"
    ],
    "m": "Los cuatro suman 360°: 360 − 280 = 80.",
    "dib": "cuadrilatero"
  },
  {
    "q": "¿Qué es la mediatriz de un segmento?",
    "ops": [
      "La perpendicular que pasa por su punto medio",
      "Cualquier recta que lo corta",
      "La recta paralela al segmento"
    ],
    "m": "Tiene que cumplir las DOS cosas: pasar por el medio y ser perpendicular.",
    "dib": "mediatriz"
  },
  {
    "q": "¿Qué tienen en común todos los paralelogramos?",
    "ops": [
      "Los lados opuestos son paralelos e iguales",
      "Los cuatro lados son iguales",
      "Todos los ángulos son rectos"
    ],
    "m": "Los lados iguales son del rombo y los ángulos rectos del rectángulo: son casos particulares.",
    "dib": "paralelogramo"
  },
  {
    "q": "¿El cuadrado es un rectángulo?",
    "ops": [
      "Sí, es un rectángulo con los 4 lados iguales",
      "No, son figuras distintas",
      "Sólo si está inclinado"
    ],
    "m": "Rectángulo significa cuatro ángulos rectos, y el cuadrado los tiene.",
    "dib": "rectangulo"
  },
  {
    "q": "¿Cuántos pares de lados paralelos tiene un trapecio?",
    "ops": [
      "Uno",
      "Dos",
      "Ninguno"
    ],
    "m": "Con dos pares sería un paralelogramo.",
    "dib": "trapecio"
  },
  {
    "q": "¿Cómo son las diagonales de un rombo?",
    "ops": [
      "Perpendiculares entre sí",
      "Iguales entre sí",
      "Paralelas"
    ],
    "m": "Se cortan formando ángulo recto. Iguales son las del rectángulo.",
    "dib": "rombo"
  },
  {
    "q": "En un paralelogramo, dos ángulos consecutivos suman…",
    "ops": [
      "180°",
      "90°",
      "360°"
    ],
    "m": "Son suplementarios, porque los lados opuestos son paralelos.",
    "dib": "paralelogramo"
  },
  {
    "q": "¿Todo rombo es un cuadrado?",
    "ops": [
      "No, sólo si además tiene ángulos rectos",
      "Sí, siempre",
      "No, nunca"
    ],
    "m": "El rombo tiene los cuatro lados iguales, pero puede estar aplastado.",
    "dib": "rombo"
  },
  {
    "q": "¿Qué figura tiene los 4 lados iguales Y los 4 ángulos rectos?",
    "ops": [
      "El cuadrado",
      "El rombo",
      "El rectángulo"
    ],
    "m": "El rombo cumple lo de los lados y el rectángulo lo de los ángulos; el cuadrado, las dos.",
    "dib": "cuadrado"
  },
  {
    "q": "Un cuadrilátero tiene ángulos de 60°, 120° y 60°. El cuarto mide…",
    "ops": [
      "120°",
      "60°",
      "90°"
    ],
    "m": "360 − 240 = 120. Es un paralelogramo.",
    "dib": "cuadrilatero"
  },
  {
    "q": "¿Cuántas diagonales tiene un cuadrilátero?",
    "ops": [
      "Dos",
      "Cuatro",
      "Una"
    ],
    "m": "Cada vértice se une con el opuesto: dos uniones en total.",
    "dib": "diagonales"
  },
  {
    "q": "¿Las diagonales de un rectángulo son iguales?",
    "ops": [
      "Sí, siempre",
      "No, nunca",
      "Sólo si es un cuadrado"
    ],
    "m": "En cualquier rectángulo las dos diagonales miden lo mismo.",
    "dib": "diagonal"
  },
  {
    "q": "Los puntos de la mediatriz de un segmento están…",
    "ops": [
      "A la misma distancia de los dos extremos",
      "Más cerca de un extremo",
      "Siempre fuera del segmento"
    ],
    "m": "Esa propiedad es lo que la hace útil para construir figuras.",
    "dib": "mediatriz"
  },
  {
    "q": "¿Un trapecio es un paralelogramo?",
    "ops": [
      "No, tiene un solo par de lados paralelos",
      "Sí, siempre",
      "Sólo si es isósceles"
    ],
    "m": "El paralelogramo necesita los DOS pares paralelos.",
    "dib": "trapecio"
  }
];
GAMES.cuadrilateros_6 = juegoTriviaTexto(CUR_CUADRILATEROS_6_BANCO, "Mirá los lados, los ángulos y las diagonales.", "cuadrilate");

/* 6° · Cuerpos y desarrollos — desarrollos_6
   DC: Desarrollo plano de prismas, cilindros y conos; elementos de los cuerpos
   Fuente: docs/auditoria-dc-caba/grado-6.md · M15b */
const CUR_DESARROLLOS_6_BANCO = [
  {
    "q": "El desarrollo de un cilindro está formado por…",
    "ops": [
      "Un rectángulo y dos círculos",
      "Dos rectángulos y un círculo",
      "Un triángulo y un círculo"
    ],
    "m": "La cara curva desenrollada es un rectángulo; las tapas, dos círculos."
  },
  {
    "q": "El desarrollo de un cono está formado por…",
    "ops": [
      "Un sector de círculo y un círculo",
      "Un triángulo y un círculo",
      "Dos triángulos"
    ],
    "m": "La cara curva no es un triángulo: desplegada queda como una porción de círculo."
  },
  {
    "q": "¿Cuántas caras tiene un cubo?",
    "ops": [
      "Seis",
      "Cuatro",
      "Ocho"
    ],
    "m": "Ocho son los vértices, no las caras."
  },
  {
    "q": "¿Cuántas aristas tiene un cubo?",
    "ops": [
      "Doce",
      "Seis",
      "Ocho"
    ],
    "m": "Cuatro arriba, cuatro abajo y cuatro verticales."
  },
  {
    "q": "¿Cuántos vértices tiene un cubo?",
    "ops": [
      "Ocho",
      "Seis",
      "Doce"
    ],
    "m": "Cuatro en la cara de arriba y cuatro en la de abajo."
  },
  {
    "q": "El desarrollo de un prisma de base triangular tiene…",
    "ops": [
      "Tres rectángulos y dos triángulos",
      "Dos rectángulos y tres triángulos",
      "Seis rectángulos"
    ],
    "m": "Un rectángulo por cada lado de la base, y las dos bases triangulares."
  },
  {
    "q": "¿Qué cuerpo NO tiene ninguna cara plana?",
    "ops": [
      "La esfera",
      "El cilindro",
      "El cono"
    ],
    "m": "El cilindro tiene dos tapas y el cono una; la esfera no tiene ninguna."
  },
  {
    "q": "¿Qué es una arista?",
    "ops": [
      "La línea donde se juntan dos caras",
      "El punto donde se juntan tres caras",
      "La superficie de una cara"
    ],
    "m": "El punto es el vértice; la arista es la línea."
  },
  {
    "q": "Una pirámide de base cuadrada tiene…",
    "ops": [
      "Cinco caras",
      "Cuatro caras",
      "Seis caras"
    ],
    "m": "Las cuatro triangulares más la base."
  },
  {
    "q": "¿Cuántas caras tiene un prisma de base pentagonal?",
    "ops": [
      "Siete",
      "Cinco",
      "Diez"
    ],
    "m": "Cinco laterales más las dos bases."
  },
  {
    "q": "Si desarmo una caja de zapatos y la apoyo, obtengo…",
    "ops": [
      "Seis rectángulos",
      "Cuatro rectángulos",
      "Un rectángulo grande"
    ],
    "m": "Una cara por cada lado de la caja: tapa, base y los cuatro costados."
  },
  {
    "q": "¿Qué diferencia a un prisma de una pirámide?",
    "ops": [
      "El prisma tiene dos bases iguales; la pirámide, una sola y termina en punta",
      "El prisma siempre es más alto",
      "La pirámide no tiene caras planas"
    ],
    "m": "Lo que manda son las bases, no el tamaño."
  },
  {
    "q": "La cara curva del cilindro, desenrollada, ¿qué figura da?",
    "ops": [
      "Un rectángulo",
      "Un círculo",
      "Un triángulo"
    ],
    "m": "Un lado del rectángulo es la altura y el otro, el contorno del círculo."
  },
  {
    "q": "¿Cuántas aristas tiene una pirámide de base cuadrada?",
    "ops": [
      "Ocho",
      "Cuatro",
      "Doce"
    ],
    "m": "Las cuatro de la base más las cuatro que suben al vértice."
  }
];
GAMES.desarrollos_6 = juegoTriviaTexto(CUR_DESARROLLOS_6_BANCO, "Imaginá la figura plegada.", "desarrollo");

/* 6° · Mismo área, otro borde — area_perimetro_6
   DC: Independencia entre área y perímetro; fórmulas; equivalencias m²↔cm²
   Fuente: docs/auditoria-dc-caba/grado-6.md · M16 */
const CUR_AREA_PERIMETRO_6_BANCO = [
  {
    "q": "Un rectángulo de 2×6 y otro de 3×4: ¿qué tienen igual?",
    "ops": [
      "El área: los dos 12",
      "El perímetro",
      "Todo"
    ],
    "m": "Área 12 los dos, pero los perímetros son 16 y 14. Se puede tener la misma área con distinto borde."
  },
  {
    "q": "¿Cuál es el área de un rectángulo de 7 cm × 4 cm?",
    "ops": [
      "28 cm²",
      "22 cm²",
      "11 cm²"
    ],
    "m": "Área es multiplicar los lados. 22 es el perímetro."
  },
  {
    "q": "¿Cuál es el perímetro de un rectángulo de 7 cm × 4 cm?",
    "ops": [
      "22 cm",
      "28 cm",
      "11 cm"
    ],
    "m": "Perímetro es sumar los cuatro lados: 7+4+7+4. 28 es el área."
  },
  {
    "q": "Si duplico los dos lados de un cuadrado, el área…",
    "ops": [
      "Se multiplica por 4",
      "Se duplica",
      "No cambia"
    ],
    "m": "Se multiplican los dos lados, así que el factor 2 entra dos veces."
  },
  {
    "q": "¿Cuánto es 1 m² en cm²?",
    "ops": [
      "10.000 cm²",
      "100 cm²",
      "1.000 cm²"
    ],
    "m": "Un metro son 100 cm, y el cuadrado mide 100 × 100."
  },
  {
    "q": "¿Cuál es el área de un cuadrado de 9 cm de lado?",
    "ops": [
      "81 cm²",
      "36 cm²",
      "18 cm²"
    ],
    "m": "Lado por lado. 36 es el perímetro."
  },
  {
    "q": "Dos figuras con el mismo perímetro, ¿tienen la misma área?",
    "ops": [
      "No necesariamente",
      "Sí, siempre",
      "Sólo si son rectángulos"
    ],
    "m": "Con perímetro 16 podés tener un 4×4 (área 16) o un 2×6 (área 12)."
  },
  {
    "q": "¿En qué unidad se mide un área?",
    "ops": [
      "En unidades cuadradas, como cm²",
      "En cm",
      "En cm³"
    ],
    "m": "El cm mide largo y el cm³ mide volumen; la superficie va en cuadradas."
  },
  {
    "q": "El área de un triángulo es…",
    "ops": [
      "Base por altura dividido 2",
      "Base por altura",
      "Base más altura"
    ],
    "m": "El triángulo es la mitad del rectángulo que lo contiene."
  },
  {
    "q": "Un terreno de 20 m × 15 m tiene un área de…",
    "ops": [
      "300 m²",
      "70 m²",
      "35 m²"
    ],
    "m": "70 es el perímetro, o sea el alambrado."
  },
  {
    "q": "Para saber cuánto alambre necesito para cercar, calculo…",
    "ops": [
      "El perímetro",
      "El área",
      "El volumen"
    ],
    "m": "El alambre va por el borde."
  },
  {
    "q": "Para saber cuánto pasto necesito para cubrir, calculo…",
    "ops": [
      "El área",
      "El perímetro",
      "La diagonal"
    ],
    "m": "El pasto cubre la superficie, no el borde."
  },
  {
    "q": "¿Cuánto es 3 m² en cm²?",
    "ops": [
      "30.000 cm²",
      "300 cm²",
      "3.000 cm²"
    ],
    "m": "Cada m² son 10.000 cm²."
  },
  {
    "q": "Un rectángulo de 1×12 y otro de 3×4 tienen la misma área. ¿Cuál tiene MÁS perímetro?",
    "ops": [
      "El de 1×12",
      "El de 3×4",
      "Los dos igual"
    ],
    "m": "26 contra 14: cuanto más alargada es la figura, más borde tiene para la misma superficie."
  }
];
GAMES.area_perimetro_6 = juegoTriviaTexto(CUR_AREA_PERIMETRO_6_BANCO, "Área y perímetro no van de la mano.", "area_perim");

/* 6° · La moda de la encuesta — moda_encuesta_6
   DC: Frecuencia absoluta y relativa; gráficos; moda
   Fuente: docs/auditoria-dc-caba/grado-6.md · M17 */
const CUR_MODA_ENCUESTA_6_BANCO = [
  {
    "q": "En 3-5-5-7-9, ¿cuál es la moda?",
    "ops": [
      "5",
      "9",
      "29"
    ],
    "m": "La moda es el que más se repite, no el más grande ni la suma."
  },
  {
    "q": "¿Qué es la frecuencia absoluta?",
    "ops": [
      "Cuántas veces aparece un dato",
      "El porcentaje que representa",
      "El dato más grande"
    ],
    "m": "Es un conteo, un número entero de veces."
  },
  {
    "q": "¿Qué es la frecuencia relativa?",
    "ops": [
      "La parte del total que representa ese dato",
      "La cantidad de veces que aparece",
      "La suma de todos los datos"
    ],
    "m": "Se expresa como fracción o porcentaje del total."
  },
  {
    "q": "De 20 chicos, 8 eligieron fútbol. ¿Cuál es su frecuencia relativa?",
    "ops": [
      "40%",
      "8%",
      "20%"
    ],
    "m": "8 de 20 es 8/20, que es 40 de cada 100."
  },
  {
    "q": "En 2-2-3-3-4, ¿cuál es la moda?",
    "ops": [
      "Hay dos modas: 2 y 3",
      "4",
      "3"
    ],
    "m": "Cuando dos datos empatan en cantidad de apariciones, la distribución tiene dos modas."
  },
  {
    "q": "En un gráfico de barras, ¿qué representa la barra MÁS ALTA?",
    "ops": [
      "La categoría con más casos",
      "El promedio",
      "El total"
    ],
    "m": "La altura de cada barra es su frecuencia."
  },
  {
    "q": "¿Cuál es la moda de 1-2-3-4-5?",
    "ops": [
      "No hay moda: ninguno se repite",
      "5",
      "3"
    ],
    "m": "Si todos aparecen una sola vez, no hay dato que se destaque."
  },
  {
    "q": "Si sumo todas las frecuencias absolutas de una encuesta, obtengo…",
    "ops": [
      "La cantidad total de encuestados",
      "La moda",
      "El 100 siempre"
    ],
    "m": "Cada persona se cuenta una vez, así que el total son las personas."
  },
  {
    "q": "Si sumo todas las frecuencias relativas, obtengo…",
    "ops": [
      "El 100%",
      "La moda",
      "La cantidad de encuestados"
    ],
    "m": "Las partes de un total siempre completan el entero."
  },
  {
    "q": "En una encuesta de 50 personas, la frecuencia relativa de una opción es 20%. ¿Cuántas la eligieron?",
    "ops": [
      "10",
      "20",
      "5"
    ],
    "m": "El 20% de 50 es 10. El 20 es el porcentaje, no la cantidad."
  },
  {
    "q": "En un gráfico circular, ¿qué representa el círculo entero?",
    "ops": [
      "El 100% de los encuestados",
      "El valor más alto",
      "La cantidad de preguntas"
    ],
    "m": "Cada porción es una parte de ese total."
  },
  {
    "q": "En 7-7-7-2-9, ¿cuál es la moda?",
    "ops": [
      "7",
      "9",
      "2"
    ],
    "m": "Aparece tres veces; los otros, una."
  },
  {
    "q": "¿La moda tiene que ser el número más grande?",
    "ops": [
      "No, es el que más se repite",
      "Sí, siempre",
      "Sólo si hay empate"
    ],
    "m": "Confundirla con el máximo es el error clásico del tema."
  },
  {
    "q": "De 40 chicos, 10 eligieron pizza. ¿Qué fracción del total es?",
    "ops": [
      "1/4",
      "1/10",
      "1/40"
    ],
    "m": "10 de 40 se simplifica a 1 de cada 4."
  }
];
GAMES.moda_encuesta_6 = juegoTriviaTexto(CUR_MODA_ENCUESTA_6_BANCO, "Leé la tabla antes de contestar.", "moda_encue");

/* 6° · ¿Seguro, posible o imposible? — probabilidad_6
   DC: Sucesos seguros, posibles e imposibles
   Fuente: docs/auditoria-dc-caba/grado-6.md · M18 */
const CUR_PROBABILIDAD_6_BANCO = [
  {
    "it": "Tirar un dado y sacar un número menor que 7",
    "cat": "seguro",
    "m": "El dado tiene 1, 2, 3, 4, 5 y 6: todos son menores que 7."
  },
  {
    "it": "Tirar un dado y sacar un 3",
    "cat": "posible",
    "m": "El 3 está en el dado, pero no sale siempre."
  },
  {
    "it": "Tirar un dado y sacar un 8",
    "cat": "imposible",
    "m": "El dado no tiene 8: no puede pasar nunca."
  },
  {
    "it": "Sacar una bolita roja de una bolsa con 5 rojas",
    "cat": "seguro",
    "m": "Todas son rojas, así que cualquiera que saques lo es."
  },
  {
    "it": "Sacar una bolita roja de una bolsa con 3 rojas y 3 azules",
    "cat": "posible",
    "m": "Puede salir roja o azul: depende de la suerte."
  },
  {
    "it": "Sacar una bolita verde de una bolsa con sólo rojas y azules",
    "cat": "imposible",
    "m": "No hay ninguna verde en la bolsa."
  },
  {
    "it": "Que mañana el sol salga por el este",
    "cat": "seguro",
    "m": "Pasa todos los días, sin excepción."
  },
  {
    "it": "Que mañana llueva en Buenos Aires",
    "cat": "posible",
    "m": "Algunos días llueve y otros no."
  },
  {
    "it": "Que en enero nieve en Buenos Aires",
    "cat": "imposible",
    "m": "Enero es pleno verano en el hemisferio sur."
  },
  {
    "it": "Tirar una moneda y que salga cara o ceca",
    "cat": "seguro",
    "m": "No hay una tercera posibilidad."
  },
  {
    "it": "Tirar una moneda y que salga cara",
    "cat": "posible",
    "m": "Hay una chance de dos."
  },
  {
    "it": "Tirar una moneda y que quede parada de canto",
    "cat": "imposible",
    "m": "En este juego sólo se consideran cara y ceca."
  },
  {
    "it": "Que un mes tenga 30 o 31 días",
    "cat": "posible",
    "m": "Febrero tiene 28 o 29, así que no es seguro."
  },
  {
    "it": "Que después del lunes venga el martes",
    "cat": "seguro",
    "m": "El orden de los días no cambia."
  },
  {
    "it": "Sacar un 7 de un mazo de cartas españolas",
    "cat": "posible",
    "m": "Hay cuatro sietes en el mazo, pero también hay muchas otras cartas."
  },
  {
    "it": "Sacar una carta de un mazo vacío",
    "cat": "imposible",
    "m": "Si no hay cartas, no se puede sacar ninguna."
  },
  {
    "it": "Que en un grupo de 40 chicos dos cumplan años el mismo mes",
    "cat": "seguro",
    "m": "Los meses son 12: con 40 chicos, por fuerza se repite alguno."
  },
  {
    "it": "Que en un grupo de 40 chicos dos cumplan el mismo DÍA",
    "cat": "posible",
    "m": "Es muy probable, pero no está garantizado."
  }
];
GAMES.probabilidad_6 = juegoClasificar(CUR_PROBABILIDAD_6_BANCO, "¿Qué chance tiene de pasar?", [{"cat": "seguro", "label": "✅ Seguro"}, {"cat": "posible", "label": "🤔 Posible"}, {"cat": "imposible", "label": "🚫 Imposible"}], "probabilid");

/* 6° · Leé y respondé — comprension_lectora_6
   DC: Comprensión lectora: literal, inferencial y predictiva
   Fuente: docs/auditoria-dc-caba/grado-6.md · L0 */
const CUR_COMPRENSION_LECTORA_6_BANCO = [
  {
    "q": "«El aula quedó en silencio cuando la directora entró sin golpear.» ¿Qué se deduce?",
    "ops": [
      "Que pasaba algo serio",
      "Que la directora era simpática",
      "Que los chicos estaban solos"
    ],
    "m": "Dos pistas juntas: el silencio repentino y entrar sin golpear."
  },
  {
    "q": "«Guardó el paraguas mojado y prendió la estufa.» ¿Cómo estaba el día?",
    "ops": [
      "Frío y lluvioso",
      "Caluroso",
      "Ventoso pero seco"
    ],
    "m": "El paraguas mojado da la lluvia; la estufa, el frío."
  },
  {
    "q": "«Tomás revisó la mochila tres veces antes de salir.» ¿Qué muestra?",
    "ops": [
      "Que estaba nervioso o inseguro",
      "Que la mochila estaba rota",
      "Que tenía mucho tiempo"
    ],
    "m": "Repetir una acción de control es la pista de la ansiedad."
  },
  {
    "q": "«El equipo entrenó todo el verano. La final es el sábado.» ¿Qué es probable que pase?",
    "ops": [
      "Que lleguen preparados a la final",
      "Que suspendan el partido",
      "Que dejen de entrenar"
    ],
    "m": "Predecir es continuar la línea que el texto ya trazó."
  },
  {
    "q": "«La panadería tenía las persianas bajas un martes a las diez.» ¿Qué se deduce?",
    "ops": [
      "Que ese día no abrió",
      "Que ya había cerrado por la tarde",
      "Que estaba llena de gente"
    ],
    "m": "Un martes a las diez es horario comercial: la persiana baja es lo raro."
  },
  {
    "q": "«Le devolvió el libro sin mirarlo a los ojos.» ¿Qué sugiere?",
    "ops": [
      "Que estaba incómodo o avergonzado",
      "Que tenía apuro",
      "Que no leyó el libro"
    ],
    "m": "Esquivar la mirada es el detalle que el texto elige contar."
  },
  {
    "q": "En un texto, ¿qué es la idea principal?",
    "ops": [
      "Lo más importante que quiere decir",
      "El primer renglón siempre",
      "El dato más curioso"
    ],
    "m": "Puede estar en cualquier parte del texto, no necesariamente al principio."
  },
  {
    "q": "«Se escuchó el timbre y todos guardaron los útiles.» ¿Qué momento es?",
    "ops": [
      "El final de la clase",
      "El comienzo del día",
      "El recreo largo"
    ],
    "m": "Guardar los útiles marca el cierre, no el comienzo."
  },
  {
    "q": "«El perro no ladró cuando entró el hombre.» ¿Qué se puede deducir?",
    "ops": [
      "Que el perro lo conocía",
      "Que el perro estaba enfermo",
      "Que el hombre era silencioso"
    ],
    "m": "Lo que NO pasa también es una pista: el silencio del perro es el dato."
  },
  {
    "q": "«Después de tres días sin dormir, Vera se equivocó en la suma más fácil.» ¿Por qué se equivocó?",
    "ops": [
      "Por el cansancio",
      "Porque no sabía sumar",
      "Porque la suma era difícil"
    ],
    "m": "El texto pone la causa antes del efecto: hay que unirlas."
  },
  {
    "q": "«Las valijas estaban en la puerta y el taxi esperaba.» ¿Qué va a pasar?",
    "ops": [
      "Alguien se va de viaje",
      "Alguien acaba de llegar",
      "Se mudan a la casa de al lado"
    ],
    "m": "Las valijas en la puerta con el taxi afuera apuntan a la salida, no a la llegada."
  },
  {
    "q": "¿Qué diferencia hay entre lo que el texto DICE y lo que se DEDUCE?",
    "ops": [
      "Lo que dice está escrito; lo que se deduce se arma con las pistas",
      "Son lo mismo",
      "Lo que se deduce se inventa libremente"
    ],
    "m": "Inferir no es inventar: la deducción tiene que apoyarse en algo del texto."
  },
  {
    "q": "«El pan estaba duro y la leche cortada.» ¿Qué se deduce?",
    "ops": [
      "Hacía días que nadie estaba en la casa",
      "Recién habían hecho las compras",
      "La heladera andaba bien"
    ],
    "m": "Dos alimentos vencidos a la vez apuntan al tiempo transcurrido."
  },
  {
    "q": "«Aunque le habían dicho que no, Julia volvió a intentarlo.» ¿Cómo es Julia?",
    "ops": [
      "Perseverante",
      "Distraída",
      "Obediente"
    ],
    "m": "El «aunque» marca que actuó EN CONTRA de lo que le dijeron."
  },
  {
    "q": "«El profesor bajó la nota a toda la clase menos a dos.» ¿Qué se deduce de esos dos?",
    "ops": [
      "Que hicieron algo distinto del resto",
      "Que faltaron ese día",
      "Que eran los más callados"
    ],
    "m": "La excepción se explica por una diferencia, y el texto la señala sin nombrarla."
  },
  {
    "q": "«La cancha estaba vacía y el marcador seguía encendido.» ¿Qué pasó?",
    "ops": [
      "El partido acababa de terminar",
      "El partido no había empezado",
      "Se cortó la luz"
    ],
    "m": "El marcador encendido indica que hubo partido; la cancha vacía, que ya terminó."
  },
  {
    "q": "«Se puso el abrigo más grueso y buscó los guantes.» ¿En qué estación estamos?",
    "ops": [
      "Invierno",
      "Verano",
      "Primavera"
    ],
    "m": "El abrigo grueso más los guantes acumulan la pista del frío intenso."
  },
  {
    "q": "«Nadie contestó el teléfono, ni la primera ni la quinta vez.» ¿Qué sugiere la insistencia?",
    "ops": [
      "Que quien llamaba estaba preocupado",
      "Que el teléfono estaba roto",
      "Que era una llamada equivocada"
    ],
    "m": "Llamar cinco veces es la pista de la urgencia de quien llama."
  }
];
GAMES.comprension_lectora_6 = juegoTriviaTexto(CUR_COMPRENSION_LECTORA_6_BANCO, "Leé con atención y pensá qué se deduce.", "comprensio");

/* 6° · Idea principal y cuadro sinóptico — idea_principal_6
   DC: Técnicas de estudio: idea central y jerarquización de la información
   Fuente: docs/auditoria-dc-caba/grado-6.md · L0b */
const CUR_IDEA_PRINCIPAL_6_BANCO = [
  {
    "q": "«Los pingüinos son aves que no vuelan. Nadan muy bien y viven en colonias. El emperador es el más grande.» ¿Cuál es la idea principal?",
    "ops": [
      "Los pingüinos son aves que no vuelan pero nadan muy bien",
      "El emperador es el pingüino más grande",
      "Los pingüinos viven en colonias"
    ],
    "m": "Las otras dos son detalles que dependen de la primera."
  },
  {
    "q": "¿Cómo se reconoce una idea secundaria?",
    "ops": [
      "Amplía o ejemplifica a la principal",
      "Siempre va al final",
      "Es la oración más larga"
    ],
    "m": "Lo que manda es la función, no el lugar ni el largo."
  },
  {
    "q": "En un cuadro sinóptico, ¿qué va a la izquierda?",
    "ops": [
      "El concepto más general",
      "Los ejemplos",
      "Los detalles"
    ],
    "m": "El cuadro se lee de lo general a lo particular."
  },
  {
    "q": "«El agua puede estar sólida, líquida o gaseosa.» Para un cuadro sinóptico, ¿qué es «sólida»?",
    "ops": [
      "Una subdivisión de «estados del agua»",
      "El concepto general",
      "Un ejemplo sin relación"
    ],
    "m": "Es una de las ramas que se abren del concepto principal."
  },
  {
    "q": "¿Para qué sirve subrayar al estudiar?",
    "ops": [
      "Para quedarse con lo que después hay que repasar",
      "Para que la carpeta quede linda",
      "Para marcar lo que no se entiende"
    ],
    "m": "Si subrayás todo, no subrayaste nada: la técnica es elegir."
  },
  {
    "q": "«Muchos animales migran. Las ballenas recorren miles de kilómetros. Las golondrinas cruzan continentes.» ¿Cuál es la idea principal?",
    "ops": [
      "Muchos animales migran",
      "Las ballenas recorren miles de kilómetros",
      "Las golondrinas cruzan continentes"
    ],
    "m": "Las otras dos son ejemplos de la primera."
  },
  {
    "q": "¿Qué es un resumen?",
    "ops": [
      "El texto reducido conservando las ideas principales",
      "Las partes que más gustaron",
      "Una opinión sobre el texto"
    ],
    "m": "Un resumen no agrega opinión ni elige por gusto."
  },
  {
    "q": "Si un párrafo habla de las causas de la lluvia, su idea principal es…",
    "ops": [
      "Por qué llueve",
      "Cuándo llueve más",
      "Cuánto llueve"
    ],
    "m": "La idea principal responde a la pregunta que el párrafo se hace."
  },
  {
    "q": "En un texto de estudio, ¿qué suelen indicar los subtítulos?",
    "ops": [
      "Los grandes temas en que se divide",
      "Las palabras difíciles",
      "Las opiniones del autor"
    ],
    "m": "Los subtítulos son el esqueleto del texto: sirven para armar el cuadro."
  },
  {
    "q": "¿Qué diferencia hay entre resumir y copiar?",
    "ops": [
      "Resumir exige decidir qué es importante",
      "Ninguna, es lo mismo",
      "Copiar lleva más tiempo"
    ],
    "m": "Copiar no obliga a entender; resumir sí."
  },
  {
    "q": "«El sistema solar tiene ocho planetas. Cuatro son rocosos y cuatro gaseosos.» ¿Cómo se jerarquiza?",
    "ops": [
      "Sistema solar → planetas → rocosos y gaseosos",
      "Rocosos → gaseosos → sistema solar",
      "Planetas → sistema solar → ocho"
    ],
    "m": "Siempre de lo que contiene a lo contenido."
  },
  {
    "q": "¿Qué palabras suelen anunciar una idea principal?",
    "ops": [
      "«Lo importante es», «en síntesis»",
      "«Por ejemplo», «como»",
      "«Además», «también»"
    ],
    "m": "«Por ejemplo» y «además» anuncian lo secundario, no lo central."
  },
  {
    "q": "Si sacás una idea secundaria del texto, ¿qué pasa?",
    "ops": [
      "El texto se entiende igual, con menos detalle",
      "El texto pierde el sentido",
      "El texto se vuelve más importante"
    ],
    "m": "Ésa es justamente la prueba para distinguirla de la principal."
  },
  {
    "q": "¿Un cuadro sinóptico sirve para…?",
    "ops": [
      "Ver de un vistazo cómo se organiza un tema",
      "Escribir el texto completo con letra chica",
      "Guardar las opiniones propias"
    ],
    "m": "Si copiás todo el texto adentro del cuadro, dejás de ver la estructura."
  }
];
GAMES.idea_principal_6 = juegoTriviaTexto(CUR_IDEA_PRINCIPAL_6_BANCO, "Separá lo central de lo que acompaña.", "idea_princ");

/* 6° · Anatomía de la noticia — noticia_partes_6
   DC: Partes de la noticia; la crónica periodística
   Fuente: docs/auditoria-dc-caba/grado-6.md · L1 */
const CUR_NOTICIA_PARTES_6_BANCO = [
  {
    "q": "¿Qué es el copete de una noticia?",
    "ops": [
      "El párrafo que resume lo esencial antes del cuerpo",
      "El título más grande",
      "La foto con su texto"
    ],
    "m": "Va entre el título y el cuerpo, y adelanta lo principal."
  },
  {
    "q": "¿Qué es la volanta?",
    "ops": [
      "La línea chica que va ARRIBA del título",
      "La línea que va abajo del título",
      "El nombre del periodista"
    ],
    "m": "Ubica el tema; el que va abajo del título es el subtítulo o bajada."
  },
  {
    "q": "¿Qué es el epígrafe?",
    "ops": [
      "El texto que explica una foto",
      "El título de la sección",
      "La firma del autor"
    ],
    "m": "Siempre acompaña a una imagen."
  },
  {
    "q": "¿Qué preguntas debe responder una buena noticia?",
    "ops": [
      "Qué, quién, cuándo, dónde, cómo y por qué",
      "Sólo qué y quién",
      "Cuándo y cuánto cuesta"
    ],
    "m": "Son las seis preguntas básicas del periodismo."
  },
  {
    "q": "¿Qué es la pirámide invertida?",
    "ops": [
      "Poner lo más importante al principio",
      "Poner lo más importante al final",
      "Escribir en orden cronológico"
    ],
    "m": "Si el lector abandona a la mitad, ya se enteró de lo esencial."
  },
  {
    "q": "¿En qué se diferencia la crónica de la noticia?",
    "ops": [
      "La crónica narra los hechos en orden y con más detalle",
      "La crónica es más corta",
      "La crónica no lleva título"
    ],
    "m": "La crónica recupera el orden temporal que la noticia rompe."
  },
  {
    "q": "En una noticia, ¿qué es el cuerpo?",
    "ops": [
      "El desarrollo con los detalles y las declaraciones",
      "El resumen inicial",
      "El título"
    ],
    "m": "Va después del copete y amplía lo ya anunciado."
  },
  {
    "q": "¿Qué es una fuente en periodismo?",
    "ops": [
      "De dónde salió la información",
      "El tipo de letra",
      "El lugar del hecho"
    ],
    "m": "Una noticia sin fuente no se puede verificar."
  },
  {
    "q": "«Tres heridos en un choque en Avenida Rivadavia» es…",
    "ops": [
      "Un título",
      "Un epígrafe",
      "Una volanta"
    ],
    "m": "Sintetiza el hecho en una línea: es la función del título."
  },
  {
    "q": "¿La noticia debe incluir la opinión del periodista?",
    "ops": [
      "No, para eso está la columna de opinión",
      "Sí, siempre",
      "Sólo si el hecho es grave"
    ],
    "m": "La noticia informa; opinar es otro género con su propio lugar."
  },
  {
    "q": "¿Qué diferencia hay entre un hecho y una opinión?",
    "ops": [
      "El hecho se puede verificar; la opinión, no",
      "El hecho es más largo",
      "La opinión siempre es falsa"
    ],
    "m": "Una opinión puede estar bien fundada y seguir siendo opinión."
  },
  {
    "q": "¿Para qué sirve una declaración entre comillas en una noticia?",
    "ops": [
      "Para reproducir textualmente lo que alguien dijo",
      "Para marcar que es mentira",
      "Para destacar una palabra difícil"
    ],
    "m": "Las comillas indican que ésas son las palabras exactas de la fuente."
  },
  {
    "q": "¿Qué es el lead o entrada de una noticia?",
    "ops": [
      "El arranque que concentra lo más importante",
      "El cierre con la conclusión",
      "El listado de fuentes"
    ],
    "m": "Es lo primero que se lee después del título."
  },
  {
    "q": "Si una noticia no dice CUÁNDO ocurrió el hecho, ¿qué le falta?",
    "ops": [
      "Una de las seis preguntas básicas",
      "El epígrafe",
      "La volanta"
    ],
    "m": "Sin el cuándo, el lector no puede ubicar el hecho en el tiempo."
  }
];
GAMES.noticia_partes_6 = juegoTriviaTexto(CUR_NOTICIA_PARTES_6_BANCO, "¿Qué parte de la noticia es?", "noticia_pa");

/* 6° · Resolvé el caso — relato_policial_6
   DC: Relato policial: enigma, pistas, hipótesis y resolución
   Fuente: docs/auditoria-dc-caba/grado-6.md · L2 */
const CUR_RELATO_POLICIAL_6_BANCO = [
  {
    "it": "Apareció la vitrina vacía y la puerta sin forzar",
    "cat": "enigma",
    "m": "Plantea el misterio que hay que resolver: es el arranque."
  },
  {
    "it": "En el piso había una huella de zapato mojada",
    "cat": "pista",
    "m": "Es un dato observable que el detective recoge."
  },
  {
    "it": "«Tal vez el ladrón tenía la llave», pensó el detective",
    "cat": "hipotesis",
    "m": "Es una explicación posible todavía sin confirmar."
  },
  {
    "it": "Era el sereno: sólo él tenía copia de la llave",
    "cat": "resolucion",
    "m": "Cierra el caso y explica todas las pistas."
  },
  {
    "it": "El cuadro desapareció durante la noche",
    "cat": "enigma",
    "m": "El hecho a explicar, sin explicación todavía."
  },
  {
    "it": "El reloj de la sala estaba parado a las 3:15",
    "cat": "pista",
    "m": "Un detalle concreto que después va a servir."
  },
  {
    "it": "«Si el reloj se paró, alguien lo tocó», supuso",
    "cat": "hipotesis",
    "m": "Deduce a partir de la pista, pero todavía no lo probó."
  },
  {
    "it": "Confesó que había parado el reloj para fingir la hora",
    "cat": "resolucion",
    "m": "La confirmación de la hipótesis cierra el relato."
  },
  {
    "it": "Nadie escuchó nada, aunque la ventana estaba rota",
    "cat": "enigma",
    "m": "La contradicción es lo que arma el misterio."
  },
  {
    "it": "Los vidrios estaban del lado de AFUERA",
    "cat": "pista",
    "m": "Un dato que cambia todo, pero todavía hay que interpretarlo."
  },
  {
    "it": "«Si los vidrios cayeron afuera, la rompieron desde adentro»",
    "cat": "hipotesis",
    "m": "Razonamiento a partir de la pista, todavía por comprobar."
  },
  {
    "it": "El robo fue simulado por el propio dueño",
    "cat": "resolucion",
    "m": "Explica el enigma y le da sentido a cada pista."
  },
  {
    "it": "La caja fuerte estaba abierta sin marcas de violencia",
    "cat": "enigma",
    "m": "Presenta el hecho extraño."
  },
  {
    "it": "En la agenda figuraba la combinación anotada",
    "cat": "pista",
    "m": "Dato objetivo que aparece durante la investigación."
  },
  {
    "it": "«Quien la abrió conocía la combinación», dedujo",
    "cat": "hipotesis",
    "m": "Una explicación tentativa que reduce los sospechosos."
  },
  {
    "it": "La secretaria había visto la agenda esa mañana",
    "cat": "resolucion",
    "m": "El dato final que cierra la cadena."
  },
  {
    "it": "El perro guardián no ladró en toda la noche",
    "cat": "pista",
    "m": "Lo que NO pasó también es una pista."
  },
  {
    "it": "«El ladrón era alguien conocido por el perro»",
    "cat": "hipotesis",
    "m": "Interpreta la pista del silencio."
  }
];
GAMES.relato_policial_6 = juegoClasificar(CUR_RELATO_POLICIAL_6_BANCO, "¿Qué parte del relato policial es?", [{"cat": "enigma", "label": "❓ Enigma"}, {"cat": "pista", "label": "🔍 Pista"}, {"cat": "hipotesis", "label": "💭 Hipótesis"}, {"cat": "resolucion", "label": "✅ Resolución"}], "relato_pol");

/* 6° · Bestiario de la ciencia ficción — ciencia_ficcion_6
   DC: Ciencia ficción: robot, androide, cyborg, científico
   Fuente: docs/auditoria-dc-caba/grado-6.md · L3 */
const CUR_CIENCIA_FICCION_6_BANCO = [
  {
    "q": "¿Qué es un robot?",
    "ops": [
      "Una máquina que hace tareas, sin forma humana necesariamente",
      "Una máquina con forma humana siempre",
      "Una persona con partes de máquina"
    ],
    "m": "La forma humana es lo propio del androide, no del robot en general."
  },
  {
    "q": "¿Qué es un androide?",
    "ops": [
      "Un robot con apariencia humana",
      "Un humano con piezas mecánicas",
      "Un programa sin cuerpo"
    ],
    "m": "«Andro-» viene de hombre: lo que lo define es parecerse a una persona."
  },
  {
    "q": "¿Qué es un cyborg?",
    "ops": [
      "Un ser vivo con partes mecánicas incorporadas",
      "Una máquina con forma humana",
      "Un robot que se programa solo"
    ],
    "m": "Empieza siendo un ser vivo. El androide, en cambio, es máquina desde el principio."
  },
  {
    "q": "¿Qué rol suele tener el científico en la ciencia ficción?",
    "ops": [
      "Crear el invento que desata el conflicto",
      "Ser siempre el villano",
      "Narrar la historia desde afuera"
    ],
    "m": "Puede ser héroe o villano; lo que no falla es que su invento mueve la trama."
  },
  {
    "q": "¿Qué caracteriza a la ciencia ficción?",
    "ops": [
      "Imagina un futuro posible a partir de la ciencia",
      "Cuenta hechos históricos reales",
      "Usa magia y hechizos"
    ],
    "m": "La magia es de la fantasía; la ciencia ficción se apoya en lo científicamente imaginable."
  },
  {
    "q": "¿En qué se diferencia la ciencia ficción de la fantasía?",
    "ops": [
      "La ciencia ficción explica lo raro con ciencia; la fantasía, no lo explica",
      "La fantasía siempre pasa en el futuro",
      "No hay diferencia"
    ],
    "m": "Un viaje en nave es ciencia ficción; uno en alfombra voladora, fantasía."
  },
  {
    "q": "Un personaje que perdió un brazo y lleva uno biónico es…",
    "ops": [
      "Un cyborg",
      "Un androide",
      "Un robot"
    ],
    "m": "Sigue siendo una persona con una parte mecánica."
  },
  {
    "q": "Una aspiradora que limpia sola es…",
    "ops": [
      "Un robot",
      "Un androide",
      "Un cyborg"
    ],
    "m": "Hace una tarea sin ayuda y no tiene forma humana."
  },
  {
    "q": "¿Qué es una distopía?",
    "ops": [
      "Un futuro imaginado que salió mal",
      "Un futuro perfecto",
      "Un pasado inventado"
    ],
    "m": "Es lo contrario de la utopía."
  },
  {
    "q": "En la ciencia ficción, ¿qué suele preguntarse sobre los androides?",
    "ops": [
      "Si pueden pensar y sentir como las personas",
      "Cuánto pesan",
      "De qué color son"
    ],
    "m": "El conflicto del género es qué los separa de nosotros."
  },
  {
    "q": "¿Qué es la inteligencia artificial en un relato de ciencia ficción?",
    "ops": [
      "Una máquina capaz de decidir por su cuenta",
      "Una computadora muy rápida",
      "Un robot con forma humana"
    ],
    "m": "Lo que la define es decidir, no la velocidad ni la forma."
  },
  {
    "q": "«La nave llegó a un planeta con dos soles.» ¿A qué género pertenece?",
    "ops": [
      "Ciencia ficción",
      "Policial",
      "Crónica periodística"
    ],
    "m": "Viaje espacial y mundo imaginado son marcas del género."
  },
  {
    "q": "¿Un robot puede ser también un androide?",
    "ops": [
      "Sí, si tiene apariencia humana",
      "No, nunca",
      "Sólo si es un cyborg"
    ],
    "m": "Androide es un tipo de robot, no algo distinto."
  },
  {
    "q": "¿Qué elemento NO es típico de la ciencia ficción?",
    "ops": [
      "Un hechizo que resucita a un rey",
      "Un viaje en el tiempo",
      "Una colonia en Marte"
    ],
    "m": "El hechizo pertenece a la fantasía: no busca explicación científica."
  }
];
GAMES.ciencia_ficcion_6 = juegoTriviaTexto(CUR_CIENCIA_FICCION_6_BANCO, "¿Quién es quién en la ciencia ficción?", "ciencia_fi");

/* 6° · ¿Fuente confiable? — fuente_confiable_6
   DC: Evaluación de fuentes; hecho verificable vs opinión fundamentada
   Fuente: docs/auditoria-dc-caba/grado-6.md · L4 */
const CUR_FUENTE_CONFIABLE_6_BANCO = [
  {
    "q": "Para un trabajo sobre vacunas, ¿qué fuente es más confiable?",
    "ops": [
      "La página del Ministerio de Salud",
      "Un video de alguien opinando",
      "Un comentario en una red social"
    ],
    "m": "El organismo oficial responde por lo que publica; un comentario, no."
  },
  {
    "q": "¿Qué indica el dominio .gob o .gov?",
    "ops": [
      "Que es un sitio de un organismo del Estado",
      "Que es una empresa",
      "Que es un blog personal"
    ],
    "m": "No garantiza que sea perfecto, pero sí quién se hace responsable."
  },
  {
    "q": "¿Qué suele indicar el dominio .edu?",
    "ops": [
      "Que es una institución educativa",
      "Que es una tienda",
      "Que es una organización sin fines de lucro"
    ],
    "m": "Sin fines de lucro es .org; la tienda suele ser .com."
  },
  {
    "q": "Una página sin fecha ni autor, ¿es confiable?",
    "ops": [
      "Menos confiable: no se sabe quién ni cuándo lo escribió",
      "Sí, si está bien escrita",
      "Sí, si aparece primera en el buscador"
    ],
    "m": "Aparecer primero mide popularidad, no veracidad."
  },
  {
    "q": "¿Qué es un hecho verificable?",
    "ops": [
      "Algo que se puede comprobar con datos",
      "Algo que mucha gente cree",
      "Algo que suena razonable"
    ],
    "m": "Que muchos lo crean no lo vuelve comprobable."
  },
  {
    "q": "«El agua hierve a 100 °C al nivel del mar.» Es…",
    "ops": [
      "Un hecho verificable",
      "Una opinión",
      "Una exageración"
    ],
    "m": "Se puede medir y cualquiera obtiene el mismo resultado."
  },
  {
    "q": "«Este es el mejor libro que se escribió.» Es…",
    "ops": [
      "Una opinión",
      "Un hecho verificable",
      "Un dato estadístico"
    ],
    "m": "«Mejor» depende de quién juzgue: no hay medición posible."
  },
  {
    "q": "¿Qué es una opinión fundamentada?",
    "ops": [
      "Una opinión que se apoya en datos y razones",
      "Una opinión que dice mucha gente",
      "Cualquier opinión escrita con seguridad"
    ],
    "m": "Sigue siendo opinión, pero se puede discutir sobre las razones que da."
  },
  {
    "q": "Si dos fuentes se contradicen, ¿qué conviene hacer?",
    "ops": [
      "Buscar una tercera y ver quién respalda cada dato",
      "Elegir la más corta",
      "Quedarse con la primera que se encontró"
    ],
    "m": "Contrastar es el único modo de decidir con criterio."
  },
  {
    "q": "Un titular que promete «lo que nadie te contó» suele ser señal de…",
    "ops": [
      "Que busca el clic más que informar",
      "Que tiene información exclusiva",
      "Que la fuente es oficial"
    ],
    "m": "El clickbait apela a la curiosidad, no a la evidencia."
  },
  {
    "q": "¿Por qué importa la FECHA de una fuente?",
    "ops": [
      "Porque la información puede haber quedado vieja",
      "Porque las páginas viejas son más confiables",
      "No importa"
    ],
    "m": "En ciencia y actualidad, un dato de hace diez años puede estar superado."
  },
  {
    "q": "Una enciclopedia que cualquiera puede editar…",
    "ops": [
      "Sirve para empezar, pero conviene chequear sus fuentes",
      "No sirve para nada",
      "Es la fuente más confiable que existe"
    ],
    "m": "Suele citar de dónde saca cada dato: ahí está lo verificable."
  },
  {
    "q": "«Nueve de cada diez dentistas lo recomiendan», dice una publicidad. ¿Qué falta?",
    "ops": [
      "Saber quién hizo el estudio y a cuántos preguntó",
      "Nada, es un dato claro",
      "El precio del producto"
    ],
    "m": "Un número sin fuente ni método parece un dato pero no se puede verificar."
  },
  {
    "q": "¿Qué es citar una fuente?",
    "ops": [
      "Decir de dónde se sacó la información",
      "Copiar el texto entero",
      "Poner un link cualquiera"
    ],
    "m": "Citar permite que otro vaya a chequearlo."
  },
  {
    "q": "Un sitio .com, ¿es necesariamente poco confiable?",
    "ops": [
      "No, pero conviene ver quién está detrás",
      "Sí, siempre",
      "No, los .com son los más confiables"
    ],
    "m": "Muchos diarios serios son .com: el dominio orienta, no decide solo."
  }
];
GAMES.fuente_confiable_6 = juegoTriviaTexto(CUR_FUENTE_CONFIABLE_6_BANCO, "¿De cuál te fiarías más?", "fuente_con");

/* 6° · Del directo al indirecto — directo_indirecto_6
   DC: Discurso directo e indirecto; biografía y autobiografía
   Fuente: docs/auditoria-dc-caba/grado-6.md · L5 */
const CUR_DIRECTO_INDIRECTO_6_BANCO = [
  {
    "q": "«Tengo hambre», dijo Ana. En indirecto:",
    "ops": [
      "Ana dijo que tenía hambre",
      "Ana dijo que tengo hambre",
      "Ana dijo: tenía hambre"
    ],
    "m": "Cambian la persona (tengo → tenía) y hay que agregar «que»."
  },
  {
    "q": "«Voy a llegar tarde», avisó Luis. En indirecto:",
    "ops": [
      "Luis avisó que iba a llegar tarde",
      "Luis avisó que voy a llegar tarde",
      "Luis avisó: iba a llegar tarde"
    ],
    "m": "El verbo pasa al pasado y la persona cambia de primera a tercera."
  },
  {
    "q": "¿Qué marca gráfica es propia del discurso directo?",
    "ops": [
      "Las comillas o la raya de diálogo",
      "El paréntesis",
      "El punto y coma"
    ],
    "m": "Sirven para mostrar que ésas son las palabras exactas."
  },
  {
    "q": "Marta dijo que estaba cansada. En directo:",
    "ops": [
      "«Estoy cansada», dijo Marta",
      "«Estaba cansada», dijo Marta",
      "Marta: estaba cansada"
    ],
    "m": "Al volver a directo, el verbo recupera el presente de quien habló."
  },
  {
    "q": "¿Qué es una autobiografía?",
    "ops": [
      "El relato de la propia vida, escrito por uno mismo",
      "El relato de la vida de otro",
      "Una novela inventada"
    ],
    "m": "«Auto-» significa uno mismo."
  },
  {
    "q": "¿Qué es una biografía?",
    "ops": [
      "El relato de la vida de otra persona",
      "El relato de la propia vida",
      "Un diario íntimo"
    ],
    "m": "Está escrita en tercera persona, sobre alguien más."
  },
  {
    "q": "¿En qué persona gramatical se escribe una autobiografía?",
    "ops": [
      "Primera",
      "Tercera",
      "Segunda"
    ],
    "m": "El que escribe es el protagonista: «yo nací…»."
  },
  {
    "q": "«¿Venís mañana?», preguntó Sol. En indirecto:",
    "ops": [
      "Sol preguntó si iba mañana",
      "Sol preguntó que venís mañana",
      "Sol preguntó: venías mañana"
    ],
    "m": "Las preguntas pasan a indirecto con «si», no con «que»."
  },
  {
    "q": "«Ayer estuve acá», dijo. En indirecto, «ayer» se transforma en…",
    "ops": [
      "El día anterior",
      "Mañana",
      "Hoy"
    ],
    "m": "Los marcadores de tiempo también se corren, no sólo los verbos."
  },
  {
    "q": "En indirecto, «acá» suele transformarse en…",
    "ops": [
      "Allá o ahí",
      "Acá igual",
      "Adentro"
    ],
    "m": "Cambia el punto de vista: ya no habla desde el mismo lugar."
  },
  {
    "q": "«Cerrá la puerta», ordenó. En indirecto:",
    "ops": [
      "Ordenó que cerrara la puerta",
      "Ordenó que cerrá la puerta",
      "Ordenó: cerrara la puerta"
    ],
    "m": "La orden pasa al subjuntivo del pasado."
  },
  {
    "q": "¿Qué verbo NO sirve para introducir discurso indirecto?",
    "ops": [
      "Correr",
      "Afirmar",
      "Preguntar"
    ],
    "m": "Hace falta un verbo de decir o pensar."
  },
  {
    "q": "«Mi hermano nació en 1998» aparece en un texto sobre otra persona. Es…",
    "ops": [
      "Una biografía",
      "Una autobiografía",
      "Una noticia"
    ],
    "m": "Habla de alguien más, no del propio autor."
  },
  {
    "q": "¿Qué se conserva EXACTAMENTE en el discurso directo?",
    "ops": [
      "Las palabras tal como se dijeron",
      "Sólo la idea general",
      "El tiempo verbal del narrador"
    ],
    "m": "Por eso lleva comillas: nada se reformula."
  },
  {
    "q": "«Estoy leyendo», dijo Juan. En indirecto:",
    "ops": [
      "Juan dijo que estaba leyendo",
      "Juan dijo que estoy leyendo",
      "Juan dijo estaba leyendo"
    ],
    "m": "Cambia la persona y el tiempo, y hace falta el «que»."
  }
];
GAMES.directo_indirecto_6 = juegoTriviaTexto(CUR_DIRECTO_INDIRECTO_6_BANCO, "Pasá lo que dijo a lo que se cuenta.", "directo_in");

/* 6° · Clasificá pronombres — pronombres_6
   DC: Pronombres personales, posesivos, demostrativos e indefinidos
   Fuente: docs/auditoria-dc-caba/grado-6.md · L6 */
const CUR_PRONOMBRES_6_BANCO = [
  {
    "it": "yo",
    "cat": "personal",
    "m": "Nombra a quien habla: es personal."
  },
  {
    "it": "mío",
    "cat": "posesivo",
    "m": "Indica de quién es algo."
  },
  {
    "it": "este",
    "cat": "demostrativo",
    "m": "Señala algo por su distancia: cerca."
  },
  {
    "it": "alguien",
    "cat": "indefinido",
    "m": "No precisa quién: por eso es indefinido."
  },
  {
    "it": "nosotros",
    "cat": "personal",
    "m": "Nombra a un grupo que incluye al que habla."
  },
  {
    "it": "tuyo",
    "cat": "posesivo",
    "m": "Marca la pertenencia a la segunda persona."
  },
  {
    "it": "aquel",
    "cat": "demostrativo",
    "m": "Señala algo lejano."
  },
  {
    "it": "nadie",
    "cat": "indefinido",
    "m": "Habla de una cantidad sin precisar: ninguno."
  },
  {
    "it": "ella",
    "cat": "personal",
    "m": "Reemplaza a una tercera persona."
  },
  {
    "it": "nuestro",
    "cat": "posesivo",
    "m": "Pertenece a un grupo que incluye al que habla."
  },
  {
    "it": "ese",
    "cat": "demostrativo",
    "m": "Señala algo a distancia media."
  },
  {
    "it": "algunos",
    "cat": "indefinido",
    "m": "No dice cuántos ni cuáles."
  },
  {
    "it": "vos",
    "cat": "personal",
    "m": "Nombra a quien escucha."
  },
  {
    "it": "suyo",
    "cat": "posesivo",
    "m": "Pertenencia de la tercera persona."
  },
  {
    "it": "esta",
    "cat": "demostrativo",
    "m": "Señala algo cercano, en femenino."
  },
  {
    "it": "ninguno",
    "cat": "indefinido",
    "m": "Cantidad imprecisa: cero, sin decir quién."
  },
  {
    "it": "ustedes",
    "cat": "personal",
    "m": "Nombra a varios oyentes."
  },
  {
    "it": "mía",
    "cat": "posesivo",
    "m": "Pertenencia de la primera persona, en femenino."
  },
  {
    "it": "aquellos",
    "cat": "demostrativo",
    "m": "Señala varios elementos lejanos."
  },
  {
    "it": "todos",
    "cat": "indefinido",
    "m": "Cantidad global, sin identificar a cada uno."
  }
];
GAMES.pronombres_6 = juegoClasificar(CUR_PRONOMBRES_6_BANCO, "¿Qué tipo de pronombre es?", [{"cat": "personal", "label": "🙋 Personal"}, {"cat": "posesivo", "label": "🔒 Posesivo"}, {"cat": "demostrativo", "label": "👉 Demostrativo"}, {"cat": "indefinido", "label": "❔ Indefinido"}], "pronombres");

/* 6° · Radiografía de la oración — sintagma_6
   DC: Sintagma nominal y verbal; núcleo, especificador y modificadores
   Fuente: docs/auditoria-dc-caba/grado-6.md · L7a */
const CUR_SINTAGMA_6_BANCO = [
  {
    "q": "En «el perro negro», ¿cuál es el núcleo?",
    "ops": [
      "perro",
      "el",
      "negro"
    ],
    "m": "El sustantivo es el núcleo; «el» y «negro» lo acompañan."
  },
  {
    "q": "En «el perro negro», ¿qué función cumple «el»?",
    "ops": [
      "Especificador (artículo)",
      "Núcleo",
      "Modificador directo"
    ],
    "m": "Los artículos especifican de cuál se habla."
  },
  {
    "q": "En «una casa muy grande», ¿cuál es el núcleo?",
    "ops": [
      "casa",
      "grande",
      "una"
    ],
    "m": "Sacá «casa» y no queda de qué se habla."
  },
  {
    "q": "¿Qué es un modificador directo?",
    "ops": [
      "Un adjetivo que acompaña al núcleo sin nexo",
      "Un adjetivo unido por preposición",
      "Otro sustantivo aclarando entre comas"
    ],
    "m": "Si hay preposición, es indirecto; si hay comas, es aposición."
  },
  {
    "q": "En «la casa de madera», «de madera» es…",
    "ops": [
      "Modificador indirecto",
      "Modificador directo",
      "Núcleo"
    ],
    "m": "Va unido por la preposición «de»: por eso es indirecto."
  },
  {
    "q": "En «Buenos Aires, la capital, creció mucho», «la capital» es…",
    "ops": [
      "Una aposición",
      "Un modificador directo",
      "El núcleo"
    ],
    "m": "Va entre comas y podría reemplazar al núcleo: es aposición."
  },
  {
    "q": "En «los chicos corrieron rápido», ¿cuál es el núcleo del predicado?",
    "ops": [
      "corrieron",
      "chicos",
      "rápido"
    ],
    "m": "El núcleo del predicado siempre es el verbo."
  },
  {
    "q": "¿Qué es un sintagma nominal?",
    "ops": [
      "Un grupo de palabras cuyo núcleo es un sustantivo",
      "Un grupo cuyo núcleo es un verbo",
      "Una oración completa"
    ],
    "m": "Si el núcleo es un verbo, es un sintagma verbal."
  },
  {
    "q": "En «mi mejor amiga», ¿cuál es el núcleo?",
    "ops": [
      "amiga",
      "mi",
      "mejor"
    ],
    "m": "Los otros dos dicen algo SOBRE la amiga."
  },
  {
    "q": "En «el gato duerme en el sillón», ¿cuál es el sujeto?",
    "ops": [
      "el gato",
      "duerme",
      "en el sillón"
    ],
    "m": "Preguntale al verbo: ¿quién duerme?"
  },
  {
    "q": "¿Puede una oración tener sujeto sin que aparezca escrito?",
    "ops": [
      "Sí, se llama sujeto tácito",
      "No, nunca",
      "Sólo en las preguntas"
    ],
    "m": "En «Corrimos toda la tarde», el sujeto «nosotros» está sobreentendido."
  },
  {
    "q": "En «una tarde de lluvia», ¿cuál es el núcleo?",
    "ops": [
      "tarde",
      "lluvia",
      "una"
    ],
    "m": "«De lluvia» modifica a «tarde», así que «tarde» manda."
  },
  {
    "q": "¿Cuántos núcleos puede tener un sujeto?",
    "ops": [
      "Uno o más de uno",
      "Siempre uno solo",
      "Siempre dos"
    ],
    "m": "En «Ana y Juan llegaron» hay dos: el sujeto es compuesto."
  },
  {
    "q": "En «el libro rojo de tapa dura», ¿cuántos modificadores tiene el núcleo?",
    "ops": [
      "Dos: «rojo» y «de tapa dura»",
      "Uno solo",
      "Ninguno"
    ],
    "m": "Uno es directo y el otro indirecto, pero los dos modifican a «libro»."
  },
  {
    "q": "¿Qué pasa si sacás el núcleo de un sintagma?",
    "ops": [
      "La construcción se rompe",
      "No cambia nada",
      "Queda más clara"
    ],
    "m": "Ésa es justamente la prueba para encontrarlo."
  }
];
GAMES.sintagma_6 = juegoTriviaTexto(CUR_SINTAGMA_6_BANCO, "Encontrá el núcleo y lo que lo acompaña.", "sintagma_6");

/* 6° · OD, OI y transitividad — od_oi_6
   DC: Objeto directo e indirecto; complementos vs adjuntos; verbos transitivos
   Fuente: docs/auditoria-dc-caba/grado-6.md · L7b */
const CUR_OD_OI_6_BANCO = [
  {
    "q": "En «Ana compró un libro», ¿cuál es el objeto directo?",
    "ops": [
      "un libro",
      "Ana",
      "compró"
    ],
    "m": "Se reemplaza por LO: «Ana LO compró»."
  },
  {
    "q": "En «Le di el regalo a mi hermana», ¿cuál es el objeto indirecto?",
    "ops": [
      "a mi hermana",
      "el regalo",
      "Le di"
    ],
    "m": "Se reemplaza por LE. El regalo es el OD."
  },
  {
    "q": "«Juan corre en la plaza.» ¿Tiene objeto directo?",
    "ops": [
      "No, correr es intransitivo",
      "Sí, «en la plaza»",
      "Sí, «Juan»"
    ],
    "m": "Correr no admite OD: lo que sigue es un circunstancial de lugar."
  },
  {
    "q": "¿Qué es un verbo transitivo?",
    "ops": [
      "El que necesita un objeto directo",
      "El que nunca lleva objeto",
      "El que se conjuga en pasado"
    ],
    "m": "«Comprar» pide qué: sin objeto la oración queda colgada."
  },
  {
    "q": "¿Cuál de estos verbos es intransitivo?",
    "ops": [
      "nacer",
      "comprar",
      "leer"
    ],
    "m": "«Nacer» no admite objeto directo: nadie nace algo."
  },
  {
    "q": "En «Corrimos en el parque», «en el parque» es…",
    "ops": [
      "Un adjunto de lugar",
      "Un objeto directo",
      "Un objeto indirecto"
    ],
    "m": "Se puede sacar y la oración sigue en pie: por eso es adjunto, no complemento."
  },
  {
    "q": "¿Cómo se distingue un complemento de un adjunto?",
    "ops": [
      "El complemento no se puede sacar sin que la oración quede incompleta",
      "El adjunto siempre va al final",
      "El complemento siempre lleva preposición"
    ],
    "m": "El adjunto agrega información circunstancial; el complemento es exigido por el verbo."
  },
  {
    "q": "En «Le escribí una carta a Pedro», ¿cuál es el OD?",
    "ops": [
      "una carta",
      "a Pedro",
      "Le"
    ],
    "m": "Se reemplaza por LA: «se LA escribí»."
  },
  {
    "q": "En «Vimos la película ayer», ¿qué es «ayer»?",
    "ops": [
      "Un adjunto de tiempo",
      "El objeto directo",
      "El objeto indirecto"
    ],
    "m": "El OD es «la película»; «ayer» se puede sacar sin romper nada."
  },
  {
    "q": "«Juan durmió» es una oración con verbo…",
    "ops": [
      "Intransitivo",
      "Transitivo",
      "Copulativo"
    ],
    "m": "«Dormir» no admite objeto directo."
  },
  {
    "q": "En «Regalé flores a mi mamá», ¿cuál es el OI?",
    "ops": [
      "a mi mamá",
      "flores",
      "Regalé"
    ],
    "m": "Es quien recibe la acción: se reemplaza por LE."
  },
  {
    "q": "¿Puede una oración tener OD y OI a la vez?",
    "ops": [
      "Sí, es muy frecuente",
      "No, nunca",
      "Sólo en preguntas"
    ],
    "m": "«Le di el libro a Ana» tiene los dos."
  },
  {
    "q": "En «Ana LO vio», ¿qué reemplaza «lo»?",
    "ops": [
      "El objeto directo",
      "El sujeto",
      "El objeto indirecto"
    ],
    "m": "LO y LA son las marcas del directo."
  },
  {
    "q": "¿Qué pregunta se le hace al verbo para encontrar el OD?",
    "ops": [
      "¿Qué? o ¿a quién?",
      "¿Para quién?",
      "¿Cuándo?"
    ],
    "m": "«¿Para quién?» apunta al indirecto y «¿cuándo?» a un adjunto."
  },
  {
    "q": "En «El tren llegó a Retiro», «a Retiro» es…",
    "ops": [
      "Un adjunto de lugar",
      "Un objeto indirecto",
      "Un objeto directo"
    ],
    "m": "Que lleve «a» no la vuelve objeto indirecto: acá indica destino."
  }
];
GAMES.od_oi_6 = juegoTriviaTexto(CUR_OD_OI_6_BANCO, "Preguntale al verbo qué y a quién.", "od_oi_6");

/* 6° · Conectores en acción — conectores_6
   DC: Conectores temporales, locativos, causales-consecutivos y de síntesis
   Fuente: docs/auditoria-dc-caba/grado-6.md · L8 */
const CUR_CONECTORES_6_BANCO = [
  {
    "it": "después",
    "cat": "temporal",
    "m": "Ordena dos hechos en el tiempo."
  },
  {
    "it": "porque",
    "cat": "causal",
    "m": "Introduce la causa de lo anterior."
  },
  {
    "it": "allí",
    "cat": "locativo",
    "m": "Ubica en el espacio."
  },
  {
    "it": "en resumen",
    "cat": "sintesis",
    "m": "Cierra recogiendo lo dicho."
  },
  {
    "it": "mientras tanto",
    "cat": "temporal",
    "m": "Marca simultaneidad."
  },
  {
    "it": "por lo tanto",
    "cat": "causal",
    "m": "Introduce la consecuencia."
  },
  {
    "it": "más adelante",
    "cat": "locativo",
    "m": "Señala un punto del espacio hacia delante."
  },
  {
    "it": "en síntesis",
    "cat": "sintesis",
    "m": "Anuncia el cierre de lo desarrollado."
  },
  {
    "it": "antes",
    "cat": "temporal",
    "m": "Indica anterioridad."
  },
  {
    "it": "por eso",
    "cat": "causal",
    "m": "Presenta lo que se sigue de lo anterior."
  },
  {
    "it": "debajo",
    "cat": "locativo",
    "m": "Indica posición en el espacio."
  },
  {
    "it": "para concluir",
    "cat": "sintesis",
    "m": "Cierra el texto."
  },
  {
    "it": "finalmente",
    "cat": "temporal",
    "m": "Marca el último hecho de la serie."
  },
  {
    "it": "ya que",
    "cat": "causal",
    "m": "Introduce el motivo."
  },
  {
    "it": "enfrente",
    "cat": "locativo",
    "m": "Ubica algo respecto de otra cosa."
  },
  {
    "it": "en conclusión",
    "cat": "sintesis",
    "m": "Anuncia el balance final."
  },
  {
    "it": "luego",
    "cat": "temporal",
    "m": "Ordena en el tiempo lo que sigue."
  },
  {
    "it": "así que",
    "cat": "causal",
    "m": "Presenta la consecuencia."
  },
  {
    "it": "alrededor",
    "cat": "locativo",
    "m": "Ubica en el entorno de algo."
  },
  {
    "it": "en pocas palabras",
    "cat": "sintesis",
    "m": "Resume lo desarrollado."
  }
];
GAMES.conectores_6 = juegoClasificar(CUR_CONECTORES_6_BANCO, "¿Qué relación arma este conector?", [{"cat": "temporal", "label": "⏱️ Temporal"}, {"cat": "causal", "label": "➡️ Causa o consecuencia"}, {"cat": "locativo", "label": "📍 De lugar"}, {"cat": "sintesis", "label": "📌 De síntesis"}], "conectores");

/* 6° · Basta de repetir — cohesion_6
   DC: Cohesión léxica: sinónimo, hiperónimo y referencia pronominal
   Fuente: docs/auditoria-dc-caba/grado-6.md · L9 */
const CUR_COHESION_6_BANCO = [
  {
    "q": "«Compré un perro. El perro es marrón.» ¿Cómo evitar la repetición?",
    "ops": [
      "El animal es marrón",
      "Perro es marrón",
      "Un perro es marrón"
    ],
    "m": "«Animal» es un hiperónimo: una palabra más general que abarca a «perro»."
  },
  {
    "q": "¿Qué es un hiperónimo?",
    "ops": [
      "Una palabra más general que incluye a otra",
      "Un sinónimo exacto",
      "Una palabra más específica"
    ],
    "m": "«Flor» es hiperónimo de «rosa»; «rosa» es hipónimo de «flor»."
  },
  {
    "q": "«Vino Sofía. Sofía trajo la torta.» El mejor reemplazo es…",
    "ops": [
      "Ella trajo la torta",
      "La chica Sofía trajo la torta",
      "Sofía ella trajo la torta"
    ],
    "m": "El pronombre personal evita repetir el nombre."
  },
  {
    "q": "¿Qué es un sinónimo?",
    "ops": [
      "Una palabra con significado parecido",
      "Una palabra con significado opuesto",
      "Una palabra más general"
    ],
    "m": "El opuesto es el antónimo; la más general, el hiperónimo."
  },
  {
    "q": "Un hiperónimo de «rosa», «margarita» y «tulipán» es…",
    "ops": [
      "flor",
      "planta hermosa",
      "jardín"
    ],
    "m": "El jardín es el lugar, no la categoría de esas tres."
  },
  {
    "q": "«El auto quedó en el taller. El vehículo estaba roto.» ¿Qué recurso se usó?",
    "ops": [
      "Un hiperónimo",
      "Un pronombre",
      "Una repetición"
    ],
    "m": "«Vehículo» es más general que «auto»."
  },
  {
    "q": "«Juan y Ana llegaron. Ellos traían regalos.» ¿A quiénes se refiere «ellos»?",
    "ops": [
      "A Juan y Ana",
      "Sólo a Juan",
      "A los regalos"
    ],
    "m": "El pronombre retoma lo nombrado justo antes."
  },
  {
    "q": "¿Por qué es un problema repetir siempre la misma palabra?",
    "ops": [
      "Hace el texto pesado y monótono",
      "Es un error de ortografía",
      "Alarga demasiado el texto"
    ],
    "m": "No es un error de escritura, es un problema de calidad del texto."
  },
  {
    "q": "Un sinónimo de «rápido» es…",
    "ops": [
      "veloz",
      "lento",
      "movimiento"
    ],
    "m": "«Lento» es el antónimo."
  },
  {
    "q": "«Compré manzanas y peras. Las frutas estaban frescas.» ¿Qué es «frutas»?",
    "ops": [
      "Un hiperónimo de las dos",
      "Un sinónimo de manzana",
      "Un pronombre"
    ],
    "m": "Abarca a las dos en una sola palabra."
  },
  {
    "q": "Si un pronombre no queda claro a quién se refiere, el texto…",
    "ops": [
      "Se vuelve ambiguo",
      "Queda más elegante",
      "Se acorta"
    ],
    "m": "La referencia tiene que poder rastrearse sin dudas."
  },
  {
    "q": "«El profesor explicó el tema. El docente dio ejemplos.» ¿Qué recurso se usó?",
    "ops": [
      "Un sinónimo",
      "Un pronombre",
      "Un hiperónimo"
    ],
    "m": "«Docente» y «profesor» significan prácticamente lo mismo."
  },
  {
    "q": "¿Qué es la elipsis en un texto?",
    "ops": [
      "Omitir una palabra que ya se entiende",
      "Repetirla para insistir",
      "Cambiarla por su opuesto"
    ],
    "m": "En «Ana estudia y (Ana) trabaja», el segundo sujeto se omite."
  },
  {
    "q": "Un hiperónimo de «martillo», «pinza» y «destornillador» es…",
    "ops": [
      "herramienta",
      "ferretería",
      "trabajo"
    ],
    "m": "La ferretería es el lugar donde se venden, no la categoría."
  }
];
GAMES.cohesion_6 = juegoTriviaTexto(CUR_COHESION_6_BANCO, "Buscá el mejor reemplazo.", "cohesion_6");

/* 6° · Sonidos del poema — recursos_poeticos_6
   DC: Aliteración, onomatopeya, personificación, comparación e hipérbole
   Fuente: docs/auditoria-dc-caba/grado-6.md · L10 */
const CUR_RECURSOS_POETICOS_6_BANCO = [
  {
    "q": "«El silbo de los silbos silbaba en la sierra.» ¿Qué recurso es?",
    "ops": [
      "Aliteración",
      "Onomatopeya",
      "Hipérbole"
    ],
    "m": "Repite el mismo sonido varias veces para armar un efecto sonoro."
  },
  {
    "q": "«El reloj hacía tic-tac toda la noche.» ¿Qué recurso es?",
    "ops": [
      "Onomatopeya",
      "Aliteración",
      "Comparación"
    ],
    "m": "La palabra imita directamente el sonido real."
  },
  {
    "q": "«El viento acariciaba las hojas.» ¿Qué recurso es?",
    "ops": [
      "Personificación",
      "Comparación",
      "Onomatopeya"
    ],
    "m": "Le da al viento una acción humana: acariciar."
  },
  {
    "q": "«Sus ojos eran como dos faroles.» ¿Qué recurso es?",
    "ops": [
      "Comparación",
      "Personificación",
      "Hipérbole"
    ],
    "m": "El «como» es la marca de la comparación."
  },
  {
    "q": "«Te lo dije un millón de veces.» ¿Qué recurso es?",
    "ops": [
      "Hipérbole",
      "Comparación",
      "Aliteración"
    ],
    "m": "Exagera a propósito para dar énfasis."
  },
  {
    "q": "¿Qué diferencia hay entre comparación y metáfora?",
    "ops": [
      "La comparación usa «como»; la metáfora, no",
      "La metáfora es más larga",
      "No hay diferencia"
    ],
    "m": "«Sus ojos son faroles» es metáfora; «como faroles», comparación."
  },
  {
    "q": "«La luna me miraba desde la ventana.» ¿Qué recurso es?",
    "ops": [
      "Personificación",
      "Hipérbole",
      "Onomatopeya"
    ],
    "m": "Mirar es una acción de un ser vivo."
  },
  {
    "q": "«¡Zas! cayó el vaso.» ¿Qué recurso es?",
    "ops": [
      "Onomatopeya",
      "Aliteración",
      "Personificación"
    ],
    "m": "Reproduce con letras el ruido del golpe."
  },
  {
    "q": "«Tres tristes tigres tragaban trigo.» ¿Qué recurso es?",
    "ops": [
      "Aliteración",
      "Onomatopeya",
      "Comparación"
    ],
    "m": "Se repite la «tr» en casi todas las palabras."
  },
  {
    "q": "«Lloré un océano.» ¿Qué recurso es?",
    "ops": [
      "Hipérbole",
      "Comparación",
      "Personificación"
    ],
    "m": "Exagera muchísimo la cantidad para expresar la intensidad."
  },
  {
    "q": "«Duerme como un tronco.» ¿Qué recurso es?",
    "ops": [
      "Comparación",
      "Metáfora",
      "Hipérbole"
    ],
    "m": "Con «como» explícito, es comparación."
  },
  {
    "q": "«Las nubes lloraban sobre el pueblo.» ¿Qué recurso es?",
    "ops": [
      "Personificación",
      "Onomatopeya",
      "Aliteración"
    ],
    "m": "Llorar es propio de las personas."
  },
  {
    "q": "¿Para qué sirven los recursos poéticos?",
    "ops": [
      "Para producir un efecto en quien lee",
      "Para hacer el texto más largo",
      "Para respetar la ortografía"
    ],
    "m": "Buscan una sensación, no cumplir una regla."
  },
  {
    "q": "«Su risa era música.» ¿Qué recurso es?",
    "ops": [
      "Metáfora",
      "Comparación",
      "Onomatopeya"
    ],
    "m": "Identifica una cosa con otra sin usar «como»."
  },
  {
    "q": "«Miau, miau», se escuchó detrás de la puerta. ¿Qué recurso es?",
    "ops": [
      "Onomatopeya",
      "Personificación",
      "Hipérbole"
    ],
    "m": "Imita el sonido del gato con letras."
  }
];
GAMES.recursos_poeticos_6 = juegoTriviaTexto(CUR_RECURSOS_POETICOS_6_BANCO, "¿Qué recurso usó el poeta?", "recursos_p");

/* 6° · Conjugá el verbo — conjugacion_6
   DC: Conjugación del modo indicativo; imperfecto vs perfecto simple
   Fuente: docs/auditoria-dc-caba/grado-6.md · L11 */
const CUR_CONJUGACION_6_BANCO = [
  {
    "q": "«Todos los veranos ___ a la playa.» ¿Qué forma va?",
    "ops": [
      "íbamos",
      "fuimos",
      "iremos"
    ],
    "m": "«Todos los veranos» marca una costumbre repetida: eso pide imperfecto."
  },
  {
    "q": "«Ayer ___ al cine.» ¿Qué forma va?",
    "ops": [
      "fui",
      "iba",
      "iré"
    ],
    "m": "Un hecho puntual y terminado pide perfecto simple."
  },
  {
    "q": "«Mientras yo ___, sonó el timbre.» ¿Qué forma va?",
    "ops": [
      "cocinaba",
      "cociné",
      "cocinaré"
    ],
    "m": "La acción que estaba en curso va en imperfecto; la que la interrumpe, en perfecto simple."
  },
  {
    "q": "¿Qué expresa el pretérito imperfecto?",
    "ops": [
      "Una acción que duraba o se repetía en el pasado",
      "Una acción terminada en un momento preciso",
      "Una acción futura"
    ],
    "m": "No marca el final de la acción: la muestra transcurriendo."
  },
  {
    "q": "¿Qué expresa el pretérito perfecto simple?",
    "ops": [
      "Una acción del pasado ya terminada",
      "Una costumbre del pasado",
      "Una acción que sigue pasando"
    ],
    "m": "Cierra la acción: pasó y se acabó."
  },
  {
    "q": "«Cuando era chico, ___ mucho al fútbol.»",
    "ops": [
      "jugaba",
      "jugué",
      "jugaría"
    ],
    "m": "«Cuando era chico» abre un período, no un instante."
  },
  {
    "q": "«El año pasado ___ la escuela primaria.»",
    "ops": [
      "terminé",
      "terminaba",
      "termino"
    ],
    "m": "Terminar es un hecho puntual con fecha."
  },
  {
    "q": "¿En qué tiempo está «habré llegado»?",
    "ops": [
      "Futuro perfecto",
      "Futuro simple",
      "Pretérito perfecto"
    ],
    "m": "Habla de algo que estará terminado en un momento futuro."
  },
  {
    "q": "¿En qué tiempo está «he estudiado»?",
    "ops": [
      "Pretérito perfecto compuesto",
      "Pretérito perfecto simple",
      "Pretérito imperfecto"
    ],
    "m": "Se arma con «haber» más el participio."
  },
  {
    "q": "«Todos los días ___ el mismo colectivo.» (en pasado)",
    "ops": [
      "tomaba",
      "tomé",
      "tomaré"
    ],
    "m": "«Todos los días» marca repetición: imperfecto."
  },
  {
    "q": "«De pronto ___ un ruido fuerte.»",
    "ops": [
      "se escuchó",
      "se escuchaba",
      "se escuchará"
    ],
    "m": "«De pronto» marca un hecho puntual."
  },
  {
    "q": "¿Cuál es el infinitivo de «tuvimos»?",
    "ops": [
      "tener",
      "tuvir",
      "tenir"
    ],
    "m": "Es un verbo irregular: la raíz cambia pero el infinitivo es «tener»."
  },
  {
    "q": "¿Cuántos modos verbales hay en español?",
    "ops": [
      "Tres: indicativo, subjuntivo e imperativo",
      "Dos",
      "Cinco"
    ],
    "m": "El indicativo informa, el subjuntivo expresa deseo o duda, el imperativo ordena."
  },
  {
    "q": "¿Qué expresa el modo indicativo?",
    "ops": [
      "Hechos que se presentan como reales",
      "Deseos y dudas",
      "Órdenes"
    ],
    "m": "Los deseos van en subjuntivo y las órdenes en imperativo."
  },
  {
    "q": "«Nosotros ___ la tarea antes de salir.» (pasado terminado)",
    "ops": [
      "hicimos",
      "hacíamos",
      "haremos"
    ],
    "m": "«Antes de salir» cierra la acción: perfecto simple."
  }
];
GAMES.conjugacion_6 = juegoTriviaTexto(CUR_CONJUGACION_6_BANCO, "Elegí el tiempo que pide la oración.", "conjugacio");

/* 6° · Tildes rebeldes — tildes_6
   DC: Acentuación completa: reglas generales, tilde diacrítica, -mente e hiato
   Fuente: docs/auditoria-dc-caba/grado-6.md · L12a */
const CUR_TILDES_6_BANCO = [
  {
    "q": "¿Cómo se escribe el vehículo grande de pasajeros?",
    "ops": [
      "camión",
      "camion",
      "cámion"
    ],
    "m": "Aguda terminada en n: lleva tilde."
  },
  {
    "q": "¿Cómo se escribe el útil con el que se dibuja?",
    "ops": [
      "lápiz",
      "lapiz",
      "lapíz"
    ],
    "m": "Grave terminada en z: lleva tilde porque no termina en n, s ni vocal."
  },
  {
    "q": "¿Cómo se escribe el adverbio de «fácil»?",
    "ops": [
      "fácilmente",
      "facilmente",
      "facílmente"
    ],
    "m": "Los adverbios en -mente conservan la tilde del adjetivo: fácil → fácilmente."
  },
  {
    "q": "«___ querés un café?» ¿Qué va?",
    "ops": [
      "¿Vos",
      "Vós",
      "Bos"
    ],
    "m": "«Vos» es monosílabo: no lleva tilde."
  },
  {
    "q": "«No sé ___ decir.» ¿Qué va?",
    "ops": [
      "qué",
      "que",
      "qué que"
    ],
    "m": "En pregunta indirecta, «qué» lleva tilde diacrítica."
  },
  {
    "q": "«Quiero ___ vengas.» ¿Qué va?",
    "ops": [
      "que",
      "qué",
      "qué que"
    ],
    "m": "Acá «que» es un nexo, no una pregunta: sin tilde."
  },
  {
    "q": "«___ tomo el café solo.» ¿Qué va?",
    "ops": [
      "Yo",
      "Yó",
      "Ió"
    ],
    "m": "Monosílabo sin necesidad de diacrítica: no lleva tilde."
  },
  {
    "q": "«Dame ___ libro a mí.» ¿Qué va?",
    "ops": [
      "el",
      "él",
      "êl"
    ],
    "m": "Artículo: sin tilde. «Él» con tilde es el pronombre."
  },
  {
    "q": "«___ llegó tarde.» ¿Qué va?",
    "ops": [
      "Él",
      "El",
      "Ell"
    ],
    "m": "Acá es el pronombre: lleva tilde diacrítica para distinguirlo del artículo."
  },
  {
    "q": "«Quiero ___ té, no café.» ¿Qué va?",
    "ops": [
      "un",
      "ún",
      "uno"
    ],
    "m": "Monosílabo átono: no lleva tilde."
  },
  {
    "q": "¿Cómo se escribe el ave nocturna de ojos grandes?",
    "ops": [
      "búho",
      "buho",
      "buhó"
    ],
    "m": "Hiato con vocal cerrada tónica: lleva tilde aunque haya una h en el medio."
  },
  {
    "q": "¿Cómo se escribe ese nombre de mujer?",
    "ops": [
      "María",
      "Maria",
      "Mária"
    ],
    "m": "La i tónica junto a otra vocal forma hiato y lleva tilde."
  },
  {
    "q": "¿Cómo se escribe el adverbio de «rápido»?",
    "ops": [
      "rápidamente",
      "rapidamente",
      "rapídamente"
    ],
    "m": "«Rápido» lleva tilde, así que «rápidamente» también."
  },
  {
    "q": "¿Cómo se escribe el plural de «examen»?",
    "ops": [
      "exámenes",
      "examenes",
      "examénes"
    ],
    "m": "«Examen» es grave sin tilde, pero el plural es esdrújula y sí la lleva."
  },
  {
    "q": "¿Cómo se escribe el cofre para guardar ropa?",
    "ops": [
      "baúl",
      "baul",
      "bául"
    ],
    "m": "La u tónica en hiato lleva tilde siempre."
  },
  {
    "q": "«___ vas a venir?» ¿Qué va?",
    "ops": [
      "¿Cuándo",
      "¿Cuando",
      "¿Quando"
    ],
    "m": "En pregunta, los interrogativos llevan tilde."
  },
  {
    "q": "«Vino ___ terminó de trabajar.» ¿Qué va?",
    "ops": [
      "cuando",
      "cuándo",
      "quando"
    ],
    "m": "Acá no pregunta nada: es un conector de tiempo, sin tilde."
  },
  {
    "q": "¿Cómo se escribe el número 16?",
    "ops": [
      "dieciséis",
      "dieciseis",
      "diecíseis"
    ],
    "m": "Aguda terminada en s: lleva tilde."
  }
];
GAMES.tildes_6 = juegoTriviaTexto(CUR_TILDES_6_BANCO, "¿Lleva tilde o no?", "tildes_6");

/* 6° · Puntuación fina — puntuacion_6
   DC: Coma, punto, paréntesis, comillas y puntos suspensivos
   Fuente: docs/auditoria-dc-caba/grado-6.md · L12b */
const CUR_PUNTUACION_6_BANCO = [
  {
    "q": "«Compré pan___ leche y queso.» ¿Qué signo va?",
    "ops": [
      "coma",
      "punto",
      "dos puntos"
    ],
    "m": "La coma separa los elementos de una enumeración."
  },
  {
    "q": "«Mi abuela ___la que vive en Salta___ vino de visita.» ¿Qué signos van?",
    "ops": [
      "comas o paréntesis",
      "comillas",
      "puntos suspensivos"
    ],
    "m": "La aclaración va entre comas o paréntesis, no entre comillas."
  },
  {
    "q": "«Y entonces pasó lo peor___» ¿Qué signo deja la frase en suspenso?",
    "ops": [
      "puntos suspensivos",
      "punto final",
      "dos puntos"
    ],
    "m": "Los suspensivos dejan algo sin decir a propósito."
  },
  {
    "q": "¿Para qué sirven las comillas?",
    "ops": [
      "Para citar palabras textuales de alguien",
      "Para separar una enumeración",
      "Para cerrar una idea"
    ],
    "m": "Marcan que ésas son las palabras exactas de otro."
  },
  {
    "q": "«Ana, ___ traés el mapa?» En una frase donde llamás a alguien, ¿qué la separa?",
    "ops": [
      "Una coma antes del nombre",
      "Dos puntos",
      "Un punto"
    ],
    "m": "El vocativo —a quién le hablás— siempre va entre comas."
  },
  {
    "q": "¿Cuándo se usan los dos puntos?",
    "ops": [
      "Antes de una enumeración o una cita",
      "Para separar palabras de una lista",
      "Al final de un párrafo"
    ],
    "m": "Anuncian que viene algo: la lista o las palabras citadas."
  },
  {
    "q": "¿Qué diferencia hay entre punto y seguido y punto y aparte?",
    "ops": [
      "El punto y aparte cambia de párrafo",
      "El punto y seguido cierra el texto",
      "Son lo mismo"
    ],
    "m": "El punto y seguido continúa en el mismo párrafo."
  },
  {
    "q": "¿Para qué sirve el paréntesis?",
    "ops": [
      "Para agregar un dato secundario",
      "Para citar textualmente",
      "Para separar una enumeración"
    ],
    "m": "Lo que va adentro se puede sacar sin romper la oración."
  },
  {
    "q": "«No vino ___ estaba enfermo.» ¿Qué signo va antes de la explicación?",
    "ops": [
      "dos puntos",
      "punto",
      "signo de pregunta"
    ],
    "m": "Los dos puntos anuncian la causa que viene después."
  },
  {
    "q": "«¿Vas a venir___» ¿Con qué se cierra una pregunta en español?",
    "ops": [
      "Con signo de interrogación de cierre",
      "Con punto",
      "Sólo con el de apertura"
    ],
    "m": "En español las preguntas se abren y se cierran."
  },
  {
    "q": "¿Se pone coma entre el sujeto y el verbo?",
    "ops": [
      "No, nunca",
      "Sí, siempre",
      "Sólo si el sujeto es largo"
    ],
    "m": "«Los chicos, juegan» está mal: nada separa al sujeto de su verbo."
  },
  {
    "q": "«Pedro dijo: ___Ya llego___» ¿Qué signos encierran lo que dijo?",
    "ops": [
      "comillas",
      "paréntesis",
      "puntos suspensivos"
    ],
    "m": "Las palabras textuales van entre comillas."
  },
  {
    "q": "¿Cuándo se usa el punto y coma?",
    "ops": [
      "Para separar partes de una oración que ya tienen comas",
      "Para cerrar el texto",
      "Para abrir una cita"
    ],
    "m": "Marca una pausa más fuerte que la coma pero menos que el punto."
  },
  {
    "q": "«Vinieron Ana, Luis y Sol___» ¿Qué signo cierra la oración?",
    "ops": [
      "punto",
      "coma",
      "dos puntos"
    ],
    "m": "Termina la idea completa: va punto."
  },
  {
    "q": "En una enumeración, ¿va coma antes del «y» final?",
    "ops": [
      "No, en español no se pone",
      "Sí, siempre",
      "Sólo si son más de cinco"
    ],
    "m": "«Pan, leche y queso»: el «y» reemplaza a la última coma."
  }
];
GAMES.puntuacion_6 = juegoTriviaTexto(CUR_PUNTUACION_6_BANCO, "¿Qué signo va acá?", "puntuacion");

/* 6° · Armá la red del ecosistema — red_ecosistema_6
   DC: Autótrofos y heterótrofos; el ecosistema como sistema abierto
   Fuente: docs/auditoria-dc-caba/grado-6.md · N1 */
const CUR_RED_ECOSISTEMA_6_BANCO = [
  {
    "q": "¿Qué es un organismo autótrofo?",
    "ops": [
      "El que fabrica su propio alimento",
      "El que come plantas",
      "El que descompone restos"
    ],
    "m": "«Auto» es por sí mismo y «trofo» es alimento."
  },
  {
    "q": "¿Cuál de estos es autótrofo?",
    "ops": [
      "El helecho",
      "El hongo",
      "La lombriz"
    ],
    "m": "Los hongos no hacen fotosíntesis: absorben materia ya elaborada."
  },
  {
    "q": "¿De dónde sacan la energía las plantas?",
    "ops": [
      "De la luz del sol",
      "Del suelo",
      "Del agua de lluvia"
    ],
    "m": "Del suelo y del agua toman materiales, pero la ENERGÍA viene del sol."
  },
  {
    "q": "¿Por qué se dice que un ecosistema es un sistema ABIERTO?",
    "ops": [
      "Porque intercambia materia y energía con el afuera",
      "Porque no tiene límites definidos",
      "Porque cualquiera puede entrar"
    ],
    "m": "Entra energía del sol y salen calor y materia: no está aislado."
  },
  {
    "q": "¿Qué pasa si desaparecen todos los productores de un ecosistema?",
    "ops": [
      "Se corta la entrada de energía y colapsa toda la red",
      "Sólo se afectan los herbívoros",
      "No pasa nada, se reacomoda"
    ],
    "m": "Los productores son la puerta de entrada de la energía a la red."
  },
  {
    "q": "¿Qué es una red alimentaria?",
    "ops": [
      "El conjunto de cadenas alimentarias entrelazadas de un ecosistema",
      "Una sola cadena de tres eslabones",
      "El lugar donde comen los animales"
    ],
    "m": "Una cadena es una línea; la red muestra que casi todos comen de varios."
  },
  {
    "q": "En una cadena, ¿hacia dónde va la flecha?",
    "ops": [
      "Hacia quien recibe la energía, o sea quien come",
      "Hacia quien es comido",
      "En los dos sentidos"
    ],
    "m": "La flecha indica el sentido en que fluye la energía."
  },
  {
    "q": "¿Qué le pasa a la energía a medida que sube por la cadena?",
    "ops": [
      "Se va perdiendo en cada eslabón",
      "Se multiplica",
      "Se mantiene igual"
    ],
    "m": "Por eso hay muchas más plantas que grandes carnívoros."
  },
  {
    "q": "¿Los hongos son plantas?",
    "ops": [
      "No, forman un reino aparte",
      "Sí, son plantas sin clorofila",
      "Sí, porque no se mueven"
    ],
    "m": "No hacen fotosíntesis, y por eso no son plantas aunque no se muevan."
  },
  {
    "q": "¿Qué es la fotosíntesis?",
    "ops": [
      "El proceso por el que la planta fabrica alimento con la luz",
      "La respiración de la planta",
      "La forma en que la planta toma agua"
    ],
    "m": "Fabricar alimento y respirar son procesos distintos: la planta hace los dos."
  },
  {
    "q": "En un acuario cerrado herméticamente, ¿qué falta para que sea un sistema abierto?",
    "ops": [
      "El intercambio de materia con el exterior",
      "Los peces",
      "El agua"
    ],
    "m": "Si nada entra ni sale, deja de ser abierto y no se sostiene."
  },
  {
    "q": "¿Qué organismo devuelve al suelo los nutrientes de los restos?",
    "ops": [
      "Los descomponedores",
      "Los productores",
      "Los carnívoros"
    ],
    "m": "Sin ellos los nutrientes quedarían atrapados en la materia muerta."
  },
  {
    "q": "El fitoplancton del mar, ¿qué papel cumple?",
    "ops": [
      "Es productor: hace fotosíntesis",
      "Es consumidor",
      "Es descomponedor"
    ],
    "m": "Es la base de casi toda la red alimentaria marina."
  },
  {
    "q": "¿Un ecosistema incluye sólo a los seres vivos?",
    "ops": [
      "No, también el agua, el suelo, el aire y la temperatura",
      "Sí, sólo los seres vivos",
      "Sólo los animales"
    ],
    "m": "Los factores no vivos son parte del ecosistema y condicionan quién puede vivir ahí."
  },
  {
    "q": "¿La ciudad es un ecosistema?",
    "ops": [
      "Sí, un ecosistema antrópico",
      "No, porque la hicieron las personas",
      "Sólo las plazas lo son"
    ],
    "m": "Tiene seres vivos, factores no vivos y flujo de materia y energía; lo particular es que lo modela la actividad humana."
  }
];
GAMES.red_ecosistema_6 = juegoTriviaTexto(CUR_RED_ECOSISTEMA_6_BANCO, "Pensá quién fabrica su alimento y quién lo toma de otro.", "red_ecosis");

/* 6° · Roles y niveles — roles_niveles_6
   DC: Productores, consumidores y descomponedores; especie, población y comunidad
   Fuente: docs/auditoria-dc-caba/grado-6.md · N2 */
const CUR_ROLES_NIVELES_6_BANCO = [
  {
    "it": "El pasto de la pampa",
    "cat": "productor",
    "m": "Hace fotosíntesis: fabrica su alimento."
  },
  {
    "it": "La vaca",
    "cat": "consumidor",
    "m": "Come pasto: obtiene la energía de otro ser vivo."
  },
  {
    "it": "El hongo que crece en un tronco caído",
    "cat": "descomponedor",
    "m": "Descompone la materia muerta y devuelve los nutrientes al suelo."
  },
  {
    "it": "El ombú",
    "cat": "productor",
    "m": "Es un árbol: produce su propio alimento."
  },
  {
    "it": "El puma",
    "cat": "consumidor",
    "m": "Carnívoro: consumidor de segundo o tercer orden."
  },
  {
    "it": "Las bacterias del suelo",
    "cat": "descomponedor",
    "m": "Junto con los hongos cierran el ciclo de la materia."
  },
  {
    "it": "El fitoplancton",
    "cat": "productor",
    "m": "Microscópico, pero hace fotosíntesis."
  },
  {
    "it": "El hornero",
    "cat": "consumidor",
    "m": "Come insectos: obtiene energía de otros seres vivos."
  },
  {
    "it": "La lombriz que come hojas en descomposición",
    "cat": "descomponedor",
    "m": "Fragmenta la materia muerta y la devuelve al suelo."
  },
  {
    "it": "El junco del delta",
    "cat": "productor",
    "m": "Planta acuática que hace fotosíntesis."
  },
  {
    "it": "El carpincho",
    "cat": "consumidor",
    "m": "Herbívoro: consumidor de primer orden."
  },
  {
    "it": "El moho del pan",
    "cat": "descomponedor",
    "m": "Un hongo que se alimenta de materia ya elaborada."
  },
  {
    "it": "El alga verde de la laguna",
    "cat": "productor",
    "m": "Tiene clorofila: produce."
  },
  {
    "it": "El zorro gris",
    "cat": "consumidor",
    "m": "Come otros animales y también frutos."
  },
  {
    "it": "El carancho que come restos",
    "cat": "consumidor",
    "m": "Es carroñero, pero sigue siendo consumidor: no descompone la materia a nivel químico."
  },
  {
    "it": "El trébol",
    "cat": "productor",
    "m": "Planta: base de la cadena."
  },
  {
    "it": "La mulita",
    "cat": "consumidor",
    "m": "Come insectos y raíces."
  },
  {
    "it": "Las bacterias que actúan sobre un animal muerto",
    "cat": "descomponedor",
    "m": "Transforman la materia orgánica en nutrientes disponibles."
  }
];
GAMES.roles_niveles_6 = juegoClasificar(CUR_ROLES_NIVELES_6_BANCO, "¿Qué papel cumple en la red?", [{"cat": "productor", "label": "🌱 Productor"}, {"cat": "consumidor", "label": "🦌 Consumidor"}, {"cat": "descomponedor", "label": "🍄 Descomponedor"}], "roles_nive");

/* 6° · Ecorregiones de Buenos Aires — ecorregiones_6
   DC: Pampa, Espinal, Delta e islas: ambientes y especies
   Fuente: docs/auditoria-dc-caba/grado-6.md · N3 */
const CUR_ECORREGIONES_6_BANCO = [
  {
    "it": "Pastizal sin árboles hasta donde llega la vista",
    "cat": "pampa",
    "m": "El pastizal abierto es la marca de la pampa."
  },
  {
    "it": "Bosque bajo de ñandubay y algarrobo",
    "cat": "espinal",
    "m": "El espinal es un bosque de árboles bajos y espinosos."
  },
  {
    "it": "Islas bajas que se inundan con la marea",
    "cat": "delta",
    "m": "El delta se define por el agua que entra y sale."
  },
  {
    "it": "El venado de las pampas",
    "cat": "pampa",
    "m": "Su nombre lo dice: es del pastizal."
  },
  {
    "it": "El caldén",
    "cat": "espinal",
    "m": "Árbol característico del bosque de espinal."
  },
  {
    "it": "El junco y el ceibo",
    "cat": "delta",
    "m": "Plantas de ribera y humedal."
  },
  {
    "it": "El ñandú",
    "cat": "pampa",
    "m": "Ave corredora del pastizal abierto."
  },
  {
    "it": "Suelo con espinillos y talas",
    "cat": "espinal",
    "m": "Los árboles espinosos son la firma del espinal."
  },
  {
    "it": "El carpincho entre los camalotes",
    "cat": "delta",
    "m": "Vive asociado al agua y a la vegetación flotante."
  },
  {
    "it": "La vizcacha en su vizcachera",
    "cat": "pampa",
    "m": "Cava sus cuevas en el suelo del pastizal."
  },
  {
    "it": "Algarrobo blanco dando sombra a un pastizal ralo",
    "cat": "espinal",
    "m": "Es la transición entre el bosque y el pastizal."
  },
  {
    "it": "El ciervo de los pantanos",
    "cat": "delta",
    "m": "Vive en humedales: su nombre lo indica."
  },
  {
    "it": "El chimango sobrevolando el campo abierto",
    "cat": "pampa",
    "m": "Ave de campos abiertos y cultivos."
  },
  {
    "it": "Bosque abierto de tala en las barrancas",
    "cat": "espinal",
    "m": "El talar es una formación típica del espinal bonaerense."
  },
  {
    "it": "El lobito de río",
    "cat": "delta",
    "m": "Necesita cursos de agua para vivir."
  },
  {
    "it": "Suelo profundo y fértil, ideal para la agricultura",
    "cat": "pampa",
    "m": "Justamente por ese suelo la pampa se transformó tanto."
  },
  {
    "it": "El ñandubay resistiendo la sequía",
    "cat": "espinal",
    "m": "Los árboles del espinal toleran suelos pobres y sequía."
  },
  {
    "it": "Sauces y alisos en la orilla del río",
    "cat": "delta",
    "m": "Vegetación de ribera del sistema deltaico."
  }
];
GAMES.ecorregiones_6 = juegoClasificar(CUR_ECORREGIONES_6_BANCO, "¿De qué ambiente es?", [{"cat": "pampa", "label": "🌾 Pampa"}, {"cat": "espinal", "label": "🌳 Espinal"}, {"cat": "delta", "label": "🏝️ Delta e islas"}], "ecorregion");

/* 6° · Línea de la vida y la pubertad — pubertad_6
   DC: Etapas de la vida; pubertad y hormonas; variabilidad individual (ESI)
   Fuente: docs/auditoria-dc-caba/grado-6.md · N4 */
const CUR_PUBERTAD_6_BANCO = [
  {
    "q": "¿Qué es la pubertad?",
    "ops": [
      "La etapa de cambios que prepara al cuerpo para la reproducción",
      "El momento en que se termina de crecer",
      "Una enfermedad pasajera"
    ],
    "m": "Es una etapa normal del desarrollo, no un problema de salud."
  },
  {
    "q": "¿Qué son las hormonas?",
    "ops": [
      "Sustancias que el cuerpo produce y que ordenan los cambios",
      "Células de la sangre",
      "Alimentos que hay que consumir"
    ],
    "m": "Viajan por la sangre y funcionan como mensajeros químicos."
  },
  {
    "q": "¿Todos los chicos empiezan la pubertad a la misma edad?",
    "ops": [
      "No, cada persona tiene su ritmo",
      "Sí, todos a los 12",
      "Sí, todas las nenas a los 10 y todos los varones a los 13"
    ],
    "m": "La variabilidad es lo normal: empezar antes o después no es mejor ni peor."
  },
  {
    "q": "¿Cuáles son las etapas de la vida en orden?",
    "ops": [
      "Infancia, pubertad, adolescencia, adultez, vejez",
      "Infancia, adolescencia, pubertad, adultez, vejez",
      "Pubertad, infancia, adolescencia, adultez, vejez"
    ],
    "m": "La pubertad es el comienzo biológico de la adolescencia, no viene después."
  },
  {
    "q": "¿Qué diferencia hay entre pubertad y adolescencia?",
    "ops": [
      "La pubertad son los cambios del cuerpo; la adolescencia incluye lo emocional y social",
      "Son exactamente lo mismo",
      "La adolescencia viene antes"
    ],
    "m": "Una es biológica; la otra es más amplia y dura más tiempo."
  },
  {
    "q": "¿Es normal transpirar más durante la pubertad?",
    "ops": [
      "Sí, las glándulas trabajan más",
      "No, indica una enfermedad",
      "Sólo en verano"
    ],
    "m": "Es uno de los cambios esperables de esta etapa."
  },
  {
    "q": "Durante la pubertad, ¿el cuerpo crece a un ritmo parejo?",
    "ops": [
      "No, hay un estirón y algunas partes crecen antes que otras",
      "Sí, todo al mismo tiempo",
      "No crece, sólo cambia por dentro"
    ],
    "m": "Que las manos o los pies crezcan primero es habitual y transitorio."
  },
  {
    "q": "¿Los cambios de la pubertad son sólo físicos?",
    "ops": [
      "No, también hay cambios emocionales",
      "Sí, sólo físicos",
      "Sólo emocionales"
    ],
    "m": "Sentir las emociones más intensas es parte esperable del proceso."
  },
  {
    "q": "¿Qué órgano coordina la producción de hormonas en la pubertad?",
    "ops": [
      "La hipófisis, en el cerebro",
      "El corazón",
      "El hígado"
    ],
    "m": "Da la señal que pone en marcha los cambios."
  },
  {
    "q": "Si alguien empieza la pubertad después que sus compañeros, ¿qué significa?",
    "ops": [
      "Que tiene su propio ritmo, y es normal",
      "Que algo anda mal",
      "Que va a ser más bajo"
    ],
    "m": "El momento de inicio no determina cómo va a ser el cuerpo adulto."
  },
  {
    "q": "¿Por qué en la pubertad puede aparecer acné?",
    "ops": [
      "Porque las glándulas de la piel producen más grasa",
      "Por comer chocolate",
      "Por no dormir"
    ],
    "m": "El cambio hormonal actúa sobre las glándulas de la piel."
  },
  {
    "q": "¿Cambia la voz sólo en los varones?",
    "ops": [
      "Cambia en todas las personas, más notoriamente en los varones",
      "Sólo en los varones",
      "En nadie"
    ],
    "m": "La laringe crece en todos; en los varones el cambio se nota más."
  },
  {
    "q": "¿A quién conviene consultarle las dudas sobre estos cambios?",
    "ops": [
      "A un adulto de confianza o a un profesional de la salud",
      "A nadie, hay que resolverlo solo",
      "Sólo a los amigos"
    ],
    "m": "Preguntar es parte del cuidado del propio cuerpo."
  },
  {
    "q": "¿La pubertad termina el crecimiento?",
    "ops": [
      "No, el crecimiento sigue un tiempo después",
      "Sí, ahí se deja de crecer",
      "Sí, y también de cambiar"
    ],
    "m": "El cuerpo sigue desarrollándose durante la adolescencia."
  }
];
GAMES.pubertad_6 = juegoTriviaTexto(CUR_PUBERTAD_6_BANCO, "Pensá en los cambios y en su tiempo.", "pubertad_6");

/* 6° · El ciclo menstrual y los mitos — ciclo_menstrual_6
   DC: Ovulación y menstruación; refutación de creencias erróneas (ESI)
   Fuente: docs/auditoria-dc-caba/grado-6.md · N5 */
const CUR_CICLO_MENSTRUAL_6_BANCO = [
  {
    "q": "¿Qué es la menstruación?",
    "ops": [
      "La eliminación del revestimiento del útero cuando no hubo embarazo",
      "Una pérdida de sangre por una herida",
      "Una enfermedad"
    ],
    "m": "Es un proceso normal y esperable del aparato reproductor."
  },
  {
    "q": "¿Qué es la ovulación?",
    "ops": [
      "La liberación de un óvulo por parte del ovario",
      "El día que empieza la menstruación",
      "El final del ciclo"
    ],
    "m": "Ocurre aproximadamente en la mitad del ciclo, no cuando empieza el sangrado."
  },
  {
    "q": "¿Cuánto dura en promedio un ciclo menstrual?",
    "ops": [
      "Alrededor de 28 días, con variaciones",
      "Exactamente 30 días",
      "Una semana"
    ],
    "m": "El promedio es 28, pero ciclos de 21 a 35 días también son normales."
  },
  {
    "q": "¿Los primeros ciclos suelen ser regulares?",
    "ops": [
      "No, tardan un tiempo en regularizarse",
      "Sí, desde el primero",
      "Nunca se regularizan"
    ],
    "m": "Es esperable que al principio los intervalos varíen."
  },
  {
    "q": "¿Se puede hacer deporte durante la menstruación?",
    "ops": [
      "Sí, no hay ninguna razón para no hacerlo",
      "No, hay que hacer reposo",
      "Sólo caminar despacio"
    ],
    "m": "Es un mito: la actividad física no está contraindicada."
  },
  {
    "q": "¿Se puede bañar una persona durante la menstruación?",
    "ops": [
      "Sí, y además es recomendable",
      "No, hace mal",
      "Sólo con agua fría"
    ],
    "m": "La higiene es parte del cuidado, no algo a evitar."
  },
  {
    "q": "¿Menstruar es sinónimo de estar enferma?",
    "ops": [
      "No, es un proceso normal del cuerpo",
      "Sí, por eso duele",
      "Sólo si hay molestias"
    ],
    "m": "Puede haber molestias y aun así tratarse de un proceso completamente normal."
  },
  {
    "q": "Si el ciclo dura 28 días, ¿aproximadamente cuándo ocurre la ovulación?",
    "ops": [
      "Cerca del día 14",
      "El día 1",
      "El día 28"
    ],
    "m": "Alrededor de la mitad del ciclo; el día 1 es el del comienzo del sangrado."
  },
  {
    "q": "¿La menstruación es lo mismo que la ovulación?",
    "ops": [
      "No, son dos momentos distintos del mismo ciclo",
      "Sí, es lo mismo",
      "La ovulación viene después del sangrado siempre"
    ],
    "m": "Confundirlas es el error más frecuente del tema."
  },
  {
    "q": "¿Qué órgano libera el óvulo?",
    "ops": [
      "El ovario",
      "El útero",
      "La vagina"
    ],
    "m": "El útero es donde se implantaría el embrión; el óvulo sale del ovario."
  },
  {
    "q": "¿Todas las personas menstrúan a la misma edad por primera vez?",
    "ops": [
      "No, varía mucho de una persona a otra",
      "Sí, a los 12",
      "Sí, a los 10"
    ],
    "m": "El rango normal es amplio y depende de cada cuerpo."
  },
  {
    "q": "¿Es cierto que no hay que lavarse el pelo durante la menstruación?",
    "ops": [
      "No, es un mito sin ninguna base",
      "Sí, hace mal",
      "Sólo el primer día"
    ],
    "m": "No existe ningún mecanismo por el cual eso pudiera afectar al cuerpo."
  },
  {
    "q": "¿Qué se puede hacer si hay molestias durante la menstruación?",
    "ops": [
      "Consultar a un adulto de confianza o a un profesional de la salud",
      "Aguantar en silencio",
      "Dejar de comer"
    ],
    "m": "Las molestias fuertes merecen consulta, no resignación."
  },
  {
    "q": "¿Qué pasa con el óvulo si no es fecundado?",
    "ops": [
      "Se elimina junto con el revestimiento del útero",
      "Se queda esperando al mes siguiente",
      "Se transforma en otra célula"
    ],
    "m": "Ese es justamente el contenido de la menstruación."
  }
];
GAMES.ciclo_menstrual_6 = juegoTriviaTexto(CUR_CICLO_MENSTRUAL_6_BANCO, "Separá lo que es cierto de lo que se dice.", "ciclo_mens");

/* 6° · Del cigoto al feto — cigoto_feto_6
   DC: Fecundación; cigoto, embrión y feto; métodos anticonceptivos e ITS (ESI)
   Fuente: docs/auditoria-dc-caba/grado-6.md · N6 */
const CUR_CIGOTO_FETO_6_BANCO = [
  {
    "q": "¿Qué es la fecundación?",
    "ops": [
      "La unión de un óvulo y un espermatozoide",
      "La llegada del óvulo al útero",
      "El comienzo de la menstruación"
    ],
    "m": "De esa unión se forma una única célula: el cigoto."
  },
  {
    "q": "¿Cómo se llama la célula que resulta de la fecundación?",
    "ops": [
      "Cigoto",
      "Embrión",
      "Feto"
    ],
    "m": "Embrión y feto son etapas posteriores, con más desarrollo."
  },
  {
    "q": "¿En qué orden van las etapas?",
    "ops": [
      "Cigoto, embrión, feto",
      "Embrión, cigoto, feto",
      "Feto, embrión, cigoto"
    ],
    "m": "Va de la célula única al organismo ya formado."
  },
  {
    "q": "¿Dónde ocurre habitualmente la fecundación?",
    "ops": [
      "En la trompa de Falopio",
      "En el útero",
      "En el ovario"
    ],
    "m": "El cigoto después viaja hasta el útero para implantarse."
  },
  {
    "q": "¿Qué es la implantación?",
    "ops": [
      "Cuando el embrión se fija en la pared del útero",
      "Cuando el óvulo sale del ovario",
      "Cuando nace el bebé"
    ],
    "m": "Es lo que permite que el embarazo continúe."
  },
  {
    "q": "¿Para qué sirve la placenta?",
    "ops": [
      "Para intercambiar nutrientes y oxígeno con el feto",
      "Para proteger de los golpes solamente",
      "Para producir hormonas únicamente"
    ],
    "m": "Es el órgano de intercambio entre la persona gestante y el feto."
  },
  {
    "q": "¿Qué es un método anticonceptivo?",
    "ops": [
      "Un método para evitar un embarazo",
      "Un tratamiento médico",
      "Una forma de acelerar el desarrollo"
    ],
    "m": "Su función es prevenir el embarazo, no tratar una enfermedad."
  },
  {
    "q": "¿Qué método previene el embarazo Y las infecciones de transmisión sexual?",
    "ops": [
      "El preservativo",
      "Las pastillas anticonceptivas",
      "Ninguno"
    ],
    "m": "Es el único que actúa como barrera contra las dos cosas."
  },
  {
    "q": "¿Qué son las ITS?",
    "ops": [
      "Infecciones que se transmiten en las relaciones sexuales",
      "Enfermedades hereditarias",
      "Alergias de la piel"
    ],
    "m": "Se transmiten de una persona a otra; no se heredan."
  },
  {
    "q": "¿Aproximadamente cuánto dura un embarazo?",
    "ops": [
      "Alrededor de 9 meses",
      "6 meses",
      "12 meses"
    ],
    "m": "Unas 40 semanas contadas desde la última menstruación."
  },
  {
    "q": "¿A partir de qué momento se habla de feto?",
    "ops": [
      "Cuando ya están formados los órganos principales",
      "Desde la fecundación",
      "Recién al nacer"
    ],
    "m": "Antes de eso, mientras se están formando, se lo llama embrión."
  },
  {
    "q": "¿Las pastillas anticonceptivas protegen de las ITS?",
    "ops": [
      "No, sólo previenen el embarazo",
      "Sí, de todas",
      "Sí, de algunas"
    ],
    "m": "Confundir esto es un riesgo real: hace falta el preservativo."
  },
  {
    "q": "¿Con quién conviene hablar sobre estos temas?",
    "ops": [
      "Con un adulto de confianza o un profesional de la salud",
      "Con nadie",
      "Sólo buscando en internet"
    ],
    "m": "La información confiable viene de fuentes que se puedan preguntar y repreguntar."
  },
  {
    "q": "¿Cuántas células tiene el cigoto?",
    "ops": [
      "Una",
      "Dos",
      "Miles"
    ],
    "m": "Es una sola célula que después empieza a dividirse."
  }
];
GAMES.cigoto_feto_6 = juegoTriviaTexto(CUR_CIGOTO_FETO_6_BANCO, "Seguí el desarrollo y sus nombres.", "cigoto_fet");

/* 6° · Estados, partículas y calor — particulas_calor_6
   DC: Modelo de partículas; el calor en tránsito; equilibrio térmico
   Fuente: docs/auditoria-dc-caba/grado-6.md · N7 */
const CUR_PARTICULAS_CALOR_6_BANCO = [
  {
    "q": "Según el modelo de partículas, ¿qué diferencia a un sólido de un líquido?",
    "ops": [
      "En el sólido las partículas están ordenadas y casi fijas",
      "El sólido no tiene partículas",
      "En el sólido las partículas son más grandes"
    ],
    "m": "Las partículas son las mismas: lo que cambia es cómo se mueven y qué tan juntas están."
  },
  {
    "q": "Al calentar un cuerpo, ¿qué les pasa a sus partículas?",
    "ops": [
      "Se mueven más rápido",
      "Se agrandan",
      "Se multiplican"
    ],
    "m": "Las partículas no cambian de tamaño ni de cantidad: cambia su movimiento."
  },
  {
    "q": "¿Qué es el calor?",
    "ops": [
      "Energía que se transfiere de un cuerpo más caliente a uno más frío",
      "Una sustancia que tienen los cuerpos calientes",
      "Lo mismo que la temperatura"
    ],
    "m": "El calor está en tránsito: un cuerpo no «tiene» calor, lo transfiere."
  },
  {
    "q": "¿Qué es el equilibrio térmico?",
    "ops": [
      "Cuando dos cuerpos en contacto llegan a la misma temperatura",
      "Cuando un cuerpo deja de tener partículas",
      "Cuando el calor desaparece"
    ],
    "m": "A partir de ahí ya no hay transferencia neta de energía."
  },
  {
    "q": "Si ponés una cuchara fría en agua caliente, ¿qué pasa?",
    "ops": [
      "El calor va del agua a la cuchara",
      "El frío va de la cuchara al agua",
      "No pasa nada"
    ],
    "m": "El frío no se transmite: lo que se transfiere es siempre energía, de lo caliente a lo frío."
  },
  {
    "q": "¿En qué estado están las partículas más separadas?",
    "ops": [
      "Gaseoso",
      "Sólido",
      "Líquido"
    ],
    "m": "Por eso un gas ocupa todo el recipiente."
  },
  {
    "q": "¿Por qué un líquido toma la forma del recipiente?",
    "ops": [
      "Porque sus partículas pueden deslizarse unas sobre otras",
      "Porque no tiene partículas",
      "Porque las partículas se estiran"
    ],
    "m": "Están juntas pero no fijas: pueden moverse."
  },
  {
    "q": "¿Qué es la temperatura?",
    "ops": [
      "Una medida de cuánto se agitan las partículas",
      "La cantidad de calor que tiene un cuerpo",
      "El peso del cuerpo"
    ],
    "m": "Es una medida del movimiento promedio, no una cantidad de sustancia."
  },
  {
    "q": "Una pava de agua a 90 °C y una taza a 90 °C, ¿tienen la misma temperatura?",
    "ops": [
      "Sí, la misma temperatura, aunque distinta energía total",
      "No, la pava está más caliente",
      "No, la taza está más caliente"
    ],
    "m": "La temperatura es la misma; lo que difiere es cuánta energía total contiene cada una."
  },
  {
    "q": "¿Qué es la fusión?",
    "ops": [
      "El pasaje de sólido a líquido",
      "El pasaje de líquido a gas",
      "El pasaje de gas a líquido"
    ],
    "m": "De líquido a gas es la vaporización; de gas a líquido, la condensación."
  },
  {
    "q": "¿Por qué se empañan los vidrios en invierno?",
    "ops": [
      "El vapor del aire se condensa al tocar el vidrio frío",
      "El vidrio pierde partículas",
      "El agua atraviesa el vidrio"
    ],
    "m": "Al enfriarse, el vapor pasa a líquido y se deposita."
  },
  {
    "q": "Si dejás una gaseosa fría afuera, ¿qué ocurre?",
    "ops": [
      "Recibe calor del ambiente hasta igualar su temperatura",
      "Le pasa frío al ambiente",
      "Nada, se mantiene fría"
    ],
    "m": "Siempre fluye energía hacia el cuerpo más frío, hasta el equilibrio."
  },
  {
    "q": "Al enfriar un gas lo suficiente, ¿qué pasa?",
    "ops": [
      "Sus partículas se juntan y puede pasar a líquido",
      "Sus partículas se achican",
      "Desaparecen las partículas"
    ],
    "m": "Al perder energía, el movimiento disminuye y las partículas se acercan."
  },
  {
    "q": "¿El calor y la temperatura son lo mismo?",
    "ops": [
      "No: el calor es energía en tránsito y la temperatura, una medida",
      "Sí, son sinónimos",
      "Sí, sólo cambian las unidades"
    ],
    "m": "Confundirlos es el error clásico del tema."
  }
];
GAMES.particulas_calor_6 = juegoTriviaTexto(CUR_PARTICULAS_CALOR_6_BANCO, "Pensá qué hacen las partículas.", "particulas");

/* 6° · Elegí el material térmico — material_termico_6
   DC: Conductividad térmica, dilatación y usos de los materiales
   Fuente: docs/auditoria-dc-caba/grado-6.md · N8 */
const CUR_MATERIAL_TERMICO_6_BANCO = [
  {
    "q": "¿De qué conviene que sea el mango de una sartén?",
    "ops": [
      "De un material aislante, como plástico o madera",
      "De metal, para que se caliente parejo",
      "De vidrio fino"
    ],
    "m": "El aislante frena el paso del calor y protege la mano."
  },
  {
    "q": "¿De qué conviene que sea el fondo de una olla?",
    "ops": [
      "De metal, buen conductor",
      "De madera",
      "De corcho"
    ],
    "m": "Ahí sí querés que el calor pase rápido al alimento."
  },
  {
    "q": "¿Por qué la ropa de invierno abriga?",
    "ops": [
      "Porque atrapa aire y frena la salida del calor del cuerpo",
      "Porque produce calor",
      "Porque atrae el calor del ambiente"
    ],
    "m": "La ropa no genera calor: reduce la pérdida del que produce el cuerpo."
  },
  {
    "q": "¿Cuál de estos es mejor conductor del calor?",
    "ops": [
      "El cobre",
      "La lana",
      "El telgopor"
    ],
    "m": "Los metales son los mejores conductores; la lana y el telgopor, aislantes."
  },
  {
    "q": "¿Por qué las conservadoras son de telgopor?",
    "ops": [
      "Porque es aislante y frena la entrada de calor",
      "Porque es liviano nada más",
      "Porque enfría el contenido"
    ],
    "m": "No enfría: sólo demora el calentamiento de lo que hay adentro."
  },
  {
    "q": "¿Qué es la dilatación térmica?",
    "ops": [
      "El aumento de tamaño de un cuerpo al calentarse",
      "La pérdida de calor",
      "El cambio de estado"
    ],
    "m": "Al aumentar el movimiento, las partículas ocupan un poco más de espacio."
  },
  {
    "q": "¿Por qué las vías del tren tienen pequeñas separaciones?",
    "ops": [
      "Para dejar lugar a la dilatación con el calor",
      "Para ahorrar material",
      "Para que pase el agua"
    ],
    "m": "Sin esa junta, el riel se deformaría al dilatarse."
  },
  {
    "q": "¿Por qué un piso de cerámica se siente más frío que uno de madera a la misma temperatura?",
    "ops": [
      "Porque la cerámica conduce mejor y te saca calor más rápido",
      "Porque la cerámica está más fría",
      "Porque la madera produce calor"
    ],
    "m": "Los dos están a la misma temperatura: lo que cambia es la velocidad con que te sacan calor."
  },
  {
    "q": "¿Para qué sirve el mango de madera de un atizador?",
    "ops": [
      "Para aislar la mano del calor del metal",
      "Para que pese menos",
      "Para que se vea mejor"
    ],
    "m": "La madera conduce mal el calor: por eso protege."
  },
  {
    "q": "¿Un termo mantiene el café caliente porque…?",
    "ops": [
      "Frena el intercambio de calor con el afuera",
      "Produce calor",
      "Aumenta la temperatura del café"
    ],
    "m": "Un termo también mantiene frío lo frío: no genera nada, aísla."
  },
  {
    "q": "¿Qué material conviene para el asa de una plancha?",
    "ops": [
      "Plástico resistente al calor",
      "Aluminio",
      "Hierro"
    ],
    "m": "Los metales conducen y quemarían la mano."
  },
  {
    "q": "¿Por qué en verano conviene ropa clara?",
    "ops": [
      "Porque refleja más la radiación del sol",
      "Porque es más liviana siempre",
      "Porque conduce mejor el calor"
    ],
    "m": "El color oscuro absorbe más radiación y se calienta más."
  },
  {
    "q": "El aire quieto, ¿es conductor o aislante?",
    "ops": [
      "Aislante",
      "Conductor",
      "Ninguna de las dos"
    ],
    "m": "Por eso las prendas que atrapan aire, como el polar, abrigan tanto."
  },
  {
    "q": "¿Por qué un puente lleva juntas de dilatación?",
    "ops": [
      "Porque el material se expande con el calor y se contrae con el frío",
      "Porque el material se gasta",
      "Para que el puente se mueva con el viento"
    ],
    "m": "Es el mismo principio que en las vías del tren."
  }
];
GAMES.material_termico_6 = juegoTriviaTexto(CUR_MATERIAL_TERMICO_6_BANCO, "¿Qué material conviene?", "material_t");

/* 6° · Del geocentrismo al heliocentrismo — heliocentrismo_6
   DC: Modelos geo y heliocéntrico; el sistema solar y sus escalas
   Fuente: docs/auditoria-dc-caba/grado-6.md · N9 */
const CUR_HELIOCENTRISMO_6_BANCO = [
  {
    "q": "¿Qué sostiene el modelo geocéntrico?",
    "ops": [
      "Que la Tierra está en el centro y todo gira a su alrededor",
      "Que el Sol está en el centro",
      "Que no hay centro"
    ],
    "m": "«Geo» es Tierra: el nombre lo dice."
  },
  {
    "q": "¿Qué sostiene el modelo heliocéntrico?",
    "ops": [
      "Que el Sol está en el centro y los planetas giran alrededor",
      "Que la Tierra está en el centro",
      "Que la Luna está en el centro"
    ],
    "m": "«Helio» es Sol."
  },
  {
    "q": "¿Por qué se abandonó el modelo geocéntrico?",
    "ops": [
      "Porque el heliocéntrico explicaba mejor las observaciones",
      "Porque lo prohibieron",
      "Porque era más difícil de calcular"
    ],
    "m": "En ciencia un modelo se reemplaza cuando otro explica más y mejor."
  },
  {
    "q": "¿Cuántos planetas tiene el sistema solar?",
    "ops": [
      "Ocho",
      "Nueve",
      "Siete"
    ],
    "m": "Plutón dejó de considerarse planeta en 2006: pasó a planeta enano."
  },
  {
    "q": "¿Cuál es el orden correcto de los cuatro primeros planetas?",
    "ops": [
      "Mercurio, Venus, Tierra, Marte",
      "Venus, Mercurio, Tierra, Marte",
      "Mercurio, Tierra, Venus, Marte"
    ],
    "m": "Mercurio es el más cercano al Sol."
  },
  {
    "q": "¿Cuál es el planeta más grande del sistema solar?",
    "ops": [
      "Júpiter",
      "Saturno",
      "La Tierra"
    ],
    "m": "Saturno es el segundo; la Tierra es muchísimo más chica que los dos."
  },
  {
    "q": "¿Cuál es el planeta más caliente?",
    "ops": [
      "Venus",
      "Mercurio",
      "Marte"
    ],
    "m": "Mercurio está más cerca del Sol, pero la atmósfera densa de Venus atrapa el calor."
  },
  {
    "q": "¿Qué diferencia a los planetas rocosos de los gaseosos?",
    "ops": [
      "Los rocosos son más chicos y tienen superficie sólida",
      "Los gaseosos están más cerca del Sol",
      "Los rocosos no tienen atmósfera"
    ],
    "m": "Los cuatro interiores son rocosos; los cuatro exteriores, gigantes gaseosos."
  },
  {
    "q": "¿Qué observación de Galileo apoyó el heliocentrismo?",
    "ops": [
      "Que Júpiter tiene lunas girando a su alrededor",
      "Que la Luna tiene cráteres",
      "Que el Sol es amarillo"
    ],
    "m": "Si algo giraba alrededor de Júpiter, no todo giraba alrededor de la Tierra."
  },
  {
    "q": "¿Qué es una órbita?",
    "ops": [
      "El recorrido de un cuerpo alrededor de otro",
      "La distancia al Sol",
      "El giro sobre su propio eje"
    ],
    "m": "El giro sobre el eje es la rotación; la órbita es la traslación."
  },
  {
    "q": "¿Qué causa el día y la noche?",
    "ops": [
      "La rotación de la Tierra sobre su eje",
      "La traslación alrededor del Sol",
      "La órbita de la Luna"
    ],
    "m": "La traslación produce el año y las estaciones, no el día."
  },
  {
    "q": "¿Por qué desde la Tierra parece que el Sol se mueve?",
    "ops": [
      "Porque la que se mueve es la Tierra",
      "Porque el Sol gira alrededor nuestro",
      "Porque la atmósfera lo desplaza"
    ],
    "m": "Es un movimiento aparente: fue lo que sostuvo al geocentrismo tanto tiempo."
  },
  {
    "q": "En una maqueta a escala del sistema solar, ¿qué suele ser lo más difícil de representar?",
    "ops": [
      "Las distancias, porque son enormes comparadas con los tamaños",
      "Los colores",
      "La cantidad de planetas"
    ],
    "m": "Si respetás el tamaño de los planetas, las distancias no entran en el aula."
  },
  {
    "q": "¿Qué es un planeta enano como Plutón?",
    "ops": [
      "Un cuerpo que orbita el Sol pero no despejó su órbita",
      "Un planeta muy chico y nada más",
      "Una luna grande"
    ],
    "m": "El criterio no es sólo el tamaño: incluye haber limpiado su zona orbital."
  },
  {
    "q": "¿La Luna es un planeta?",
    "ops": [
      "No, es un satélite natural de la Tierra",
      "Sí, el más chico",
      "Sí, porque gira alrededor del Sol"
    ],
    "m": "Un planeta orbita directamente al Sol; la Luna orbita a la Tierra."
  }
];
GAMES.heliocentrismo_6 = juegoTriviaTexto(CUR_HELIOCENTRISMO_6_BANCO, "¿Qué modelo explica mejor lo que se observa?", "heliocentr");

/* 6° · Tiempo vs. clima — tiempo_clima_6
   DC: Variables meteorológicas; diferencia entre tiempo y clima
   Fuente: docs/auditoria-dc-caba/grado-6.md · N10a */
const CUR_TIEMPO_CLIMA_6_BANCO = [
  {
    "it": "Hoy hay 28 grados y está despejado",
    "cat": "tiempo",
    "m": "Describe el estado de la atmósfera AHORA."
  },
  {
    "it": "En Ushuaia los inviernos son largos y fríos",
    "cat": "clima",
    "m": "Es una característica sostenida a lo largo de los años."
  },
  {
    "it": "Mañana se esperan tormentas por la tarde",
    "cat": "tiempo",
    "m": "Es un pronóstico de corto plazo."
  },
  {
    "it": "El noroeste argentino es una zona árida",
    "cat": "clima",
    "m": "Describe el patrón general de la región."
  },
  {
    "it": "Ahora está lloviznando en Palermo",
    "cat": "tiempo",
    "m": "Es lo que pasa en este momento y en un lugar puntual."
  },
  {
    "it": "En la selva misionera llueve mucho todo el año",
    "cat": "clima",
    "m": "Es el promedio de precipitaciones de muchos años."
  },
  {
    "it": "El viento sopla a 40 km/h desde el sur",
    "cat": "tiempo",
    "m": "Una medición del momento."
  },
  {
    "it": "Buenos Aires tiene clima templado húmedo",
    "cat": "clima",
    "m": "Una clasificación basada en décadas de registros."
  },
  {
    "it": "Esta noche la temperatura baja a 4 grados",
    "cat": "tiempo",
    "m": "Un dato puntual del pronóstico."
  },
  {
    "it": "La Patagonia es ventosa durante todo el año",
    "cat": "clima",
    "m": "Una característica permanente de la región."
  },
  {
    "it": "Hay 85% de humedad en este momento",
    "cat": "tiempo",
    "m": "Es una variable meteorológica medida ahora."
  },
  {
    "it": "En la Puna la amplitud térmica diaria es muy grande",
    "cat": "clima",
    "m": "Es un rasgo estable de esa región, no de un día."
  },
  {
    "it": "Cayó granizo esta mañana en Mar del Plata",
    "cat": "tiempo",
    "m": "Un evento puntual."
  },
  {
    "it": "El promedio de lluvias anuales de la pampa es de 900 mm",
    "cat": "clima",
    "m": "Un promedio de largo plazo."
  },
  {
    "it": "El cielo está parcialmente nublado",
    "cat": "tiempo",
    "m": "Describe la nubosidad de este momento."
  },
  {
    "it": "En el sur del país nieva todos los inviernos",
    "cat": "clima",
    "m": "Un patrón que se repite año tras año."
  }
];
GAMES.tiempo_clima_6 = juegoClasificar(CUR_TIEMPO_CLIMA_6_BANCO, "¿Habla del tiempo de hoy o del clima del lugar?", [{"cat": "tiempo", "label": "🌦️ Tiempo"}, {"cat": "clima", "label": "🗓️ Clima"}], "tiempo_cli");

/* 6° · Efecto invernadero — efecto_invernadero_6
   DC: Gases de efecto invernadero; procesos directos e indirectos; mitigación
   Fuente: docs/auditoria-dc-caba/grado-6.md · N10b */
const CUR_EFECTO_INVERNADERO_6_BANCO = [
  {
    "q": "¿Qué es el efecto invernadero?",
    "ops": [
      "La retención de calor por gases de la atmósfera",
      "Un agujero en la atmósfera",
      "El calor directo del sol"
    ],
    "m": "El agujero de ozono es otro problema distinto: conviene no mezclarlos."
  },
  {
    "q": "¿El efecto invernadero es en sí mismo algo malo?",
    "ops": [
      "No, es natural y necesario; el problema es su aumento",
      "Sí, siempre fue dañino",
      "No existe"
    ],
    "m": "Sin él la Tierra sería demasiado fría para la vida como la conocemos."
  },
  {
    "q": "¿Cuál de estos es un gas de efecto invernadero?",
    "ops": [
      "El dióxido de carbono",
      "El nitrógeno",
      "El argón"
    ],
    "m": "El nitrógeno es el gas más abundante del aire, pero no retiene calor así."
  },
  {
    "q": "¿Qué actividad libera más dióxido de carbono?",
    "ops": [
      "Quemar combustibles fósiles",
      "Plantar árboles",
      "Usar energía solar"
    ],
    "m": "Los árboles y la energía solar van en el sentido contrario."
  },
  {
    "q": "¿Qué es el metano?",
    "ops": [
      "Un gas de efecto invernadero muy potente",
      "Un gas inofensivo",
      "Un tipo de contaminación del agua"
    ],
    "m": "Se libera en la ganadería, los rellenos sanitarios y la extracción de gas."
  },
  {
    "q": "Usar el colectivo en vez del auto particular es una medida de…",
    "ops": [
      "Mitigación",
      "Adaptación",
      "Ninguna de las dos"
    ],
    "m": "Mitigar es reducir las emisiones; adaptarse es prepararse para los efectos."
  },
  {
    "q": "¿Qué diferencia hay entre mitigación y adaptación?",
    "ops": [
      "Mitigar reduce las causas; adaptarse prepara para las consecuencias",
      "Son lo mismo",
      "Mitigar es sólo plantar árboles"
    ],
    "m": "Construir defensas contra inundaciones es adaptación, no mitigación."
  },
  {
    "q": "¿Cuál es una fuente de energía renovable?",
    "ops": [
      "La energía eólica",
      "El carbón",
      "El petróleo"
    ],
    "m": "El viento no se agota; el carbón y el petróleo sí."
  },
  {
    "q": "¿Por qué los bosques ayudan contra el cambio climático?",
    "ops": [
      "Porque absorben dióxido de carbono al crecer",
      "Porque dan sombra",
      "Porque producen metano"
    ],
    "m": "Funcionan como sumideros de carbono."
  },
  {
    "q": "Comprar productos de cerca en vez de importados, ¿ayuda?",
    "ops": [
      "Sí, porque reduce las emisiones del transporte",
      "No, es indistinto",
      "Sí, pero sólo por el precio"
    ],
    "m": "Es una emisión indirecta: no la ves, pero está en el traslado."
  },
  {
    "q": "¿Qué es una emisión indirecta?",
    "ops": [
      "La que se produce en otro lugar por algo que consumimos acá",
      "La que sale del caño de escape",
      "La que no se puede medir"
    ],
    "m": "La electricidad que usás genera emisiones en la central donde se produjo."
  },
  {
    "q": "¿La energía nuclear emite dióxido de carbono al generar electricidad?",
    "ops": [
      "No en la generación, aunque tiene otros problemas",
      "Sí, muchísimo",
      "Sí, más que el carbón"
    ],
    "m": "Su discusión pasa por los residuos y la seguridad, no por el CO₂."
  },
  {
    "q": "Separar los residuos, ¿en qué ayuda?",
    "ops": [
      "Permite reciclar y reduce lo que se entierra y genera metano",
      "No ayuda en nada",
      "Sólo mejora el aspecto de la ciudad"
    ],
    "m": "Los rellenos sanitarios son una fuente importante de metano."
  },
  {
    "q": "¿Qué significa que un proceso libere GEI de forma directa?",
    "ops": [
      "Que la emisión ocurre en el propio proceso",
      "Que la emisión ocurre en otro país",
      "Que no se puede evitar"
    ],
    "m": "Quemar nafta en el auto es directo; la nafta que se usó para traerte la comida, indirecto."
  }
];
GAMES.efecto_invernadero_6 = juegoTriviaTexto(CUR_EFECTO_INVERNADERO_6_BANCO, "Pensá qué gases y de dónde vienen.", "efecto_inv");

/* 6° · Línea de tiempo 1862-1930 — linea_tiempo_1862_1930_6
   DC: Unificación 1862, federalización 1880, Ley 1420, Sáenz Peña 1912, 1916, 1930
   Fuente: docs/auditoria-dc-caba/grado-6.md · S1 */
const CUR_LINEA_TIEMPO_1862_1930_6_BANCO = [
  {
    "items": [
      "Mitre asume la presidencia del país unificado (1862)",
      "Se sanciona la Ley 1420 de educación común (1884)",
      "Se sanciona la Ley Sáenz Peña (1912)",
      "Yrigoyen asume la presidencia (1916)"
    ]
  },
  {
    "items": [
      "Presidencia de Sarmiento (1868)",
      "Federalización de Buenos Aires (1880)",
      "Primera Guerra Mundial (1914-1918)",
      "Golpe de Estado contra Yrigoyen (1930)"
    ]
  },
  {
    "items": [
      "Presidencia de Avellaneda (1874)",
      "Ley 1420 de educación común (1884)",
      "Ley Sáenz Peña de voto secreto (1912)",
      "Crisis económica mundial (1929)"
    ]
  },
  {
    "items": [
      "Unificación nacional bajo Mitre (1862)",
      "Campaña militar sobre los territorios indígenas (1879)",
      "Llegada masiva de inmigrantes ultramarinos (1890-1914)",
      "Primer gobierno radical (1916)"
    ]
  },
  {
    "items": [
      "Buenos Aires se convierte en capital federal (1880)",
      "Se organiza el modelo agroexportador (1880-1900)",
      "Estalla la Primera Guerra Mundial (1914)",
      "Crack de la Bolsa de Nueva York (1929)"
    ]
  },
  {
    "items": [
      "Presidencia de Mitre (1862)",
      "Presidencia de Sarmiento (1868)",
      "Presidencia de Avellaneda (1874)",
      "Presidencia de Roca (1880)"
    ]
  },
  {
    "items": [
      "Ley 1420 de educación común (1884)",
      "Censo nacional que muestra el peso de la inmigración (1895)",
      "Ley Sáenz Peña (1912)",
      "Golpe de 1930"
    ]
  },
  {
    "items": [
      "Se extiende la red ferroviaria hacia el puerto (1870-1890)",
      "Auge de las exportaciones de carne y cereal (1900)",
      "Primera Guerra Mundial interrumpe el comercio (1914)",
      "La crisis del '29 golpea a las exportaciones (1930)"
    ]
  },
  {
    "items": [
      "Sanción de la Ley Sáenz Peña (1912)",
      "Primera elección con voto secreto y obligatorio (1916)",
      "Segundo gobierno de Yrigoyen (1928)",
      "Interrupción del orden constitucional (1930)"
    ]
  },
  {
    "items": [
      "Federalización de Buenos Aires (1880)",
      "Ley 1420 (1884)",
      "Censo de 1895",
      "Ley Sáenz Peña (1912)"
    ]
  }
];
GAMES.linea_tiempo_1862_1930_6 = juegoOrdenar(CUR_LINEA_TIEMPO_1862_1930_6_BANCO, "Ordená del hecho MÁS ANTIGUO al más nuevo. Tocá en orden.", "Anclate en las fechas que ya sabés y ubicá el resto alrededor.", "linea_tiem");

/* 6° · ¿1ª o 2ª Revolución Industrial? — revolucion_industrial_6
   DC: Vapor vs petróleo y electricidad; países centrales y periféricos
   Fuente: docs/auditoria-dc-caba/grado-6.md · S2 */
const CUR_REVOLUCION_INDUSTRIAL_6_BANCO = [
  {
    "it": "La máquina de vapor",
    "cat": "primera",
    "m": "Es la energía que define la primera etapa."
  },
  {
    "it": "El motor de combustión interna",
    "cat": "segunda",
    "m": "Funciona con derivados del petróleo: segunda etapa."
  },
  {
    "it": "El carbón como combustible principal",
    "cat": "primera",
    "m": "Alimentaba las máquinas de vapor."
  },
  {
    "it": "La electricidad en las fábricas",
    "cat": "segunda",
    "m": "Permitió mover máquinas sin correas ni calderas."
  },
  {
    "it": "La industria textil mecanizada",
    "cat": "primera",
    "m": "Fue el primer sector en industrializarse."
  },
  {
    "it": "La producción en serie del automóvil",
    "cat": "segunda",
    "m": "La línea de montaje pertenece a la segunda etapa."
  },
  {
    "it": "El ferrocarril a vapor",
    "cat": "primera",
    "m": "Transformó el transporte usando la misma tecnología del vapor."
  },
  {
    "it": "La industria química y del acero a gran escala",
    "cat": "segunda",
    "m": "Sectores característicos de la segunda revolución."
  },
  {
    "it": "El telar mecánico",
    "cat": "primera",
    "m": "Reemplazó el trabajo manual en el textil."
  },
  {
    "it": "El teléfono y el telégrafo eléctrico",
    "cat": "segunda",
    "m": "Las comunicaciones eléctricas son de la segunda etapa."
  },
  {
    "it": "Inglaterra como potencia industrial dominante",
    "cat": "primera",
    "m": "Lideró la primera etapa casi en soledad."
  },
  {
    "it": "Estados Unidos y Alemania disputando el liderazgo",
    "cat": "segunda",
    "m": "En la segunda etapa aparecen nuevas potencias."
  },
  {
    "it": "La lámpara eléctrica en las ciudades",
    "cat": "segunda",
    "m": "Cambió la vida urbana y los horarios de trabajo."
  },
  {
    "it": "Las primeras fábricas con chimeneas humeantes",
    "cat": "primera",
    "m": "El humo del carbón es la imagen de la primera etapa."
  },
  {
    "it": "La Argentina exportando cereales a los países industriales",
    "cat": "segunda",
    "m": "Se integra al mercado mundial como país periférico durante esta etapa."
  },
  {
    "it": "El barco a vapor cruzando el Atlántico",
    "cat": "primera",
    "m": "Aplicó al transporte marítimo la tecnología del vapor."
  }
];
GAMES.revolucion_industrial_6 = juegoClasificar(CUR_REVOLUCION_INDUSTRIAL_6_BANCO, "¿De qué etapa es?", [{"cat": "primera", "label": "🚂 1ª (vapor)"}, {"cat": "segunda", "label": "💡 2ª (electricidad)"}], "revolucion");

/* 6° · Estado y agroexportación — estado_agroexportacion_6
   DC: Mitre, Sarmiento y Avellaneda; modelo agroexportador; ferrocarril y puerto
   Fuente: docs/auditoria-dc-caba/grado-6.md · S3 */
const CUR_ESTADO_AGROEXPORTACION_6_BANCO = [
  {
    "q": "¿Qué exportaba principalmente la Argentina del modelo agroexportador?",
    "ops": [
      "Cereales, carne y lana",
      "Máquinas y automóviles",
      "Petróleo refinado"
    ],
    "m": "Se exportaban materias primas y se importaban manufacturas."
  },
  {
    "q": "¿Por qué la red ferroviaria tenía forma de abanico hacia Buenos Aires?",
    "ops": [
      "Porque estaba pensada para llevar la producción al puerto",
      "Porque el terreno lo imponía",
      "Porque unía las provincias entre sí"
    ],
    "m": "El diseño respondía a la exportación, no a conectar el interior entre sí."
  },
  {
    "q": "¿Qué presidente impulsó fuertemente la educación pública?",
    "ops": [
      "Sarmiento",
      "Mitre",
      "Avellaneda"
    ],
    "m": "Su gestión fundó escuelas y escuelas normales en todo el país."
  },
  {
    "q": "¿Qué fue la federalización de Buenos Aires en 1880?",
    "ops": [
      "Convertir la ciudad en capital del país, separada de la provincia",
      "Darle más poder a la provincia de Buenos Aires",
      "Trasladar la capital a otra ciudad"
    ],
    "m": "Resolvió un conflicto que venía desde 1852 sobre quién controlaba la ciudad y su puerto."
  },
  {
    "q": "¿Qué fue la Ley 1420 de 1884?",
    "ops": [
      "La ley de educación común, gratuita y obligatoria",
      "La ley de inmigración",
      "La ley del voto secreto"
    ],
    "m": "Fue una de las bases del Estado moderno y de la integración de los inmigrantes."
  },
  {
    "q": "¿Qué papel cumplía el puerto de Buenos Aires en ese modelo?",
    "ops": [
      "Era la salida de las exportaciones y la entrada de las importaciones",
      "Era sólo un puerto militar",
      "No tenía importancia económica"
    ],
    "m": "Todo el sistema de transporte se organizó en función de ese punto."
  },
  {
    "q": "¿Quiénes financiaron en buena parte los ferrocarriles argentinos?",
    "ops": [
      "Capitales británicos",
      "El Estado argentino en soledad",
      "Cooperativas de productores"
    ],
    "m": "Esa inversión extranjera es parte de la relación con los países centrales."
  },
  {
    "q": "En el reparto internacional de esa época, la Argentina era…",
    "ops": [
      "Un país periférico proveedor de materias primas",
      "Un país central industrializado",
      "Un país aislado del comercio"
    ],
    "m": "Centrales eran los industrializados que compraban esas materias primas."
  },
  {
    "q": "¿Qué fue el frigorífico para la exportación de carne?",
    "ops": [
      "La tecnología que permitió mandar carne enfriada a Europa",
      "Un tipo de barco",
      "Una raza de ganado"
    ],
    "m": "Sin frío, la carne no podía cruzar el Atlántico."
  },
  {
    "q": "El alambrado de los campos, ¿qué cambió?",
    "ops": [
      "Delimitó la propiedad y permitió mejorar el ganado",
      "Sólo sirvió para marcar caminos",
      "No tuvo efecto económico"
    ],
    "m": "Separar los rodeos hizo posible seleccionar y mejorar las razas."
  },
  {
    "q": "¿Qué presidencia se ubica entre las de Sarmiento y Roca?",
    "ops": [
      "La de Avellaneda",
      "La de Mitre",
      "La de Yrigoyen"
    ],
    "m": "El orden es Mitre, Sarmiento, Avellaneda y después Roca."
  },
  {
    "q": "¿Qué significa que un país exporte materias primas e importe manufacturas?",
    "ops": [
      "Que vende productos poco elaborados y compra los elaborados",
      "Que vende y compra lo mismo",
      "Que no comercia con nadie"
    ],
    "m": "Esa asimetría es la que define la posición periférica en el comercio mundial."
  },
  {
    "q": "¿Qué cambió el telégrafo para el comercio de la época?",
    "ops": [
      "Permitió conocer los precios de Europa casi al instante",
      "Sirvió sólo para uso militar",
      "No influyó en el comercio"
    ],
    "m": "La información rápida modificó cómo se compraba y vendía."
  },
  {
    "q": "El crecimiento de esa economía, ¿llegó por igual a todo el país?",
    "ops": [
      "No: se concentró en la región pampeana y el litoral",
      "Sí, a todas las provincias por igual",
      "Sólo llegó al noroeste"
    ],
    "m": "Las economías regionales quedaron en una posición muy distinta."
  }
];
GAMES.estado_agroexportacion_6 = juegoTriviaTexto(CUR_ESTADO_AGROEXPORTACION_6_BANCO, "Pensá cómo se armó el país y de qué vivía.", "estado_agr");

/* 6° · Inmigración: censos y conventillo — inmigracion_censos_6
   DC: Inmigración ultramarina; lectura de censos; conventillo; Ley 1420
   Fuente: docs/auditoria-dc-caba/grado-6.md · S4 */
const CUR_INMIGRACION_CENSOS_6_BANCO = [
  {
    "q": "¿De qué países llegaba la mayor parte de los inmigrantes ultramarinos?",
    "ops": [
      "Italia y España",
      "Alemania y Francia",
      "Inglaterra y Portugal"
    ],
    "m": "Hubo inmigración de muchos orígenes, pero esos dos fueron con diferencia los mayores."
  },
  {
    "q": "¿Qué era un conventillo?",
    "ops": [
      "Una casa grande subdividida donde muchas familias compartían patio y servicios",
      "Un edificio de departamentos modernos",
      "Un hotel para turistas"
    ],
    "m": "Una pieza por familia y todo lo demás compartido."
  },
  {
    "q": "¿Por qué emigraba tanta gente de Europa en esa época?",
    "ops": [
      "Por pobreza, falta de tierra y guerras",
      "Por turismo",
      "Porque el gobierno europeo los expulsaba a todos"
    ],
    "m": "Casi siempre había una combinación de causas económicas y políticas."
  },
  {
    "q": "¿Para qué sirve un censo?",
    "ops": [
      "Para contar y describir a la población en un momento dado",
      "Para cobrar impuestos únicamente",
      "Para elegir autoridades"
    ],
    "m": "Da una foto de cuánta gente hay y cómo vive."
  },
  {
    "q": "Si un censo muestra que el 30% de los habitantes de una ciudad nació en el extranjero, ¿qué indica?",
    "ops": [
      "Que la inmigración tuvo un peso enorme en esa población",
      "Que la ciudad era muy chica",
      "Que casi nadie emigraba"
    ],
    "m": "Es exactamente el tipo de dato que revelaron los censos de 1895 y 1914."
  },
  {
    "q": "¿Qué papel cumplió la escuela pública con los hijos de inmigrantes?",
    "ops": [
      "Enseñar el idioma y una historia común",
      "Separarlos del resto",
      "Enviarlos de vuelta a sus países"
    ],
    "m": "La Ley 1420 fue una herramienta central de integración."
  },
  {
    "q": "¿Qué era el Hotel de Inmigrantes?",
    "ops": [
      "El lugar donde los recién llegados se alojaban unos días al desembarcar",
      "Un hotel de lujo del puerto",
      "Una escuela para adultos"
    ],
    "m": "Ofrecía alojamiento, comida y ayuda para conseguir trabajo."
  },
  {
    "q": "¿Todos los inmigrantes se quedaron definitivamente?",
    "ops": [
      "No, muchos volvieron o venían por temporadas",
      "Sí, todos se quedaron",
      "Casi ninguno se quedó"
    ],
    "m": "Los «golondrina» venían para la cosecha y volvían."
  },
  {
    "q": "¿Qué huellas dejó la inmigración en el habla del Río de la Plata?",
    "ops": [
      "Palabras y modismos, sobre todo del italiano",
      "Ninguna",
      "Sólo nombres propios"
    ],
    "m": "El lunfardo tomó mucho vocabulario de los dialectos italianos."
  },
  {
    "q": "En un conventillo, ¿cómo eran las condiciones sanitarias?",
    "ops": [
      "Precarias, con baños compartidos y hacinamiento",
      "Muy buenas, con baño en cada pieza",
      "No había gente viviendo ahí"
    ],
    "m": "El hacinamiento facilitaba la propagación de enfermedades."
  },
  {
    "q": "¿Qué actividad concentró a muchos inmigrantes en la ciudad?",
    "ops": [
      "El trabajo en talleres, comercios y el puerto",
      "La minería",
      "La pesca de altura"
    ],
    "m": "Los que se quedaron en la ciudad se emplearon sobre todo ahí."
  },
  {
    "q": "Si comparás dos censos de distintas décadas, ¿qué podés ver?",
    "ops": [
      "Cómo cambió la población en ese período",
      "Sólo cuánta gente había hoy",
      "El resultado de una elección"
    ],
    "m": "Comparar es lo que convierte un dato aislado en una tendencia."
  },
  {
    "q": "¿La llegada de inmigrantes generó tensiones sociales?",
    "ops": [
      "Sí, hubo conflictos laborales y también rechazo de algunos sectores",
      "No, fue un proceso sin conflictos",
      "Sólo hubo conflictos entre inmigrantes"
    ],
    "m": "Fue un proceso de integración real, y por eso también tuvo tensiones."
  },
  {
    "q": "¿Qué prometía a los inmigrantes la Constitución de 1853?",
    "ops": [
      "Los mismos derechos civiles que a los ciudadanos argentinos",
      "Tierra gratis garantizada para todos",
      "El voto inmediato"
    ],
    "m": "Los derechos civiles no son lo mismo que los políticos: votar requería la ciudadanía."
  }
];
GAMES.inmigracion_censos_6 = juegoTriviaTexto(CUR_INMIGRACION_CENSOS_6_BANCO, "Leé los datos y pensá cómo se vivía.", "inmigracio");

/* 6° · El voto antes y después — voto_6
   DC: Ley Sáenz Peña 1912; gobiernos radicales; golpe de 1930
   Fuente: docs/auditoria-dc-caba/grado-6.md · S5 */
const CUR_VOTO_6_BANCO = [
  {
    "q": "¿Qué estableció la Ley Sáenz Peña de 1912?",
    "ops": [
      "Voto secreto, obligatorio y universal masculino",
      "Voto para todas las personas adultas",
      "El fin de las elecciones"
    ],
    "m": "Fue un avance real Y siguió excluyendo a las mujeres: las dos cosas son ciertas."
  },
  {
    "q": "¿Las mujeres podían votar después de la Ley Sáenz Peña?",
    "ops": [
      "No, recién pudieron desde 1947",
      "Sí, desde 1912",
      "Sí, pero sólo en algunas provincias"
    ],
    "m": "El voto femenino llegó con la Ley 13.010, mucho después."
  },
  {
    "q": "Antes de 1912, ¿cómo se votaba?",
    "ops": [
      "A viva voz y sin secreto, lo que facilitaba la presión",
      "Con boleta secreta",
      "Por correo"
    ],
    "m": "Sin secreto, quien tenía poder podía controlar y presionar el voto."
  },
  {
    "q": "¿Qué significa que el voto sea secreto?",
    "ops": [
      "Que nadie puede saber a quién votaste",
      "Que no se cuentan los votos",
      "Que se vota sin decir el nombre propio"
    ],
    "m": "Es lo que protege al votante de las presiones."
  },
  {
    "q": "¿Qué significa que el voto sea obligatorio?",
    "ops": [
      "Que las personas habilitadas tienen el deber de votar",
      "Que hay que votar a un candidato determinado",
      "Que se vota todos los años"
    ],
    "m": "Obliga a participar, no a elegir una opción en particular."
  },
  {
    "q": "¿Quién ganó la primera elección presidencial con la nueva ley, en 1916?",
    "ops": [
      "Hipólito Yrigoyen",
      "Julio Roca",
      "Marcelo T. de Alvear"
    ],
    "m": "Alvear gobernó después, entre los dos mandatos de Yrigoyen."
  },
  {
    "q": "¿Qué pasó en 1930?",
    "ops": [
      "Un golpe de Estado interrumpió el orden constitucional",
      "Se amplió el voto a las mujeres",
      "Terminó la Primera Guerra"
    ],
    "m": "Fue el primer golpe de Estado del siglo XX en la Argentina."
  },
  {
    "q": "¿Qué es el fraude electoral?",
    "ops": [
      "Manipular una elección para alterar el resultado",
      "Votar en blanco",
      "No presentarse a votar"
    ],
    "m": "Fue una práctica extendida antes de 1912 y volvió después de 1930."
  },
  {
    "q": "¿Qué significa «universal» en el sufragio de 1912?",
    "ops": [
      "Universal masculino: todos los varones nativos mayores de edad",
      "Todas las personas adultas del país",
      "Todos los habitantes, incluidos los extranjeros"
    ],
    "m": "El nombre suena más amplio de lo que fue: es importante nombrar lo que quedó afuera."
  },
  {
    "q": "¿Los inmigrantes que no se habían nacionalizado podían votar?",
    "ops": [
      "No, hacía falta la ciudadanía",
      "Sí, todos",
      "Sí, tras cinco años"
    ],
    "m": "Es una de las razones por las que mucha población quedó fuera del sistema político."
  },
  {
    "q": "El padrón electoral servía para…",
    "ops": [
      "Registrar quiénes estaban habilitados para votar",
      "Contar los votos",
      "Elegir a los candidatos"
    ],
    "m": "Se armó a partir del registro militar de los varones."
  },
  {
    "q": "¿Qué se buscaba con el voto secreto y obligatorio?",
    "ops": [
      "Que la elección reflejara mejor la voluntad de la gente",
      "Que votara menos gente",
      "Que el gobierno eligiera a los candidatos"
    ],
    "m": "Reducir la presión y ampliar la participación eran los dos objetivos."
  },
  {
    "q": "Después de 1930, ¿qué pasó con las elecciones?",
    "ops": [
      "Hubo un período con fraude sistemático",
      "Se mantuvieron completamente limpias",
      "Dejaron de hacerse elecciones"
    ],
    "m": "Hubo elecciones, pero con prácticas fraudulentas conocidas."
  }
];
GAMES.voto_6 = juegoTriviaTexto(CUR_VOTO_6_BANCO, "Pensá quién podía votar y cómo.", "voto_6");

/* 6° · La Gran Guerra y la crisis del '29 — gran_guerra_crisis_6
   DC: Primera Guerra Mundial; crisis de 1929 y su impacto en la Argentina
   Fuente: docs/auditoria-dc-caba/grado-6.md · S6 */
const CUR_GRAN_GUERRA_CRISIS_6_BANCO = [
  {
    "q": "¿Entre qué años ocurrió la Primera Guerra Mundial?",
    "ops": [
      "1914-1918",
      "1939-1945",
      "1929-1933"
    ],
    "m": "1939-1945 es la Segunda; 1929 es la crisis económica."
  },
  {
    "q": "¿Qué postura tomó la Argentina durante la Primera Guerra Mundial?",
    "ops": [
      "Se mantuvo neutral",
      "Participó junto a los Aliados",
      "Participó junto a las Potencias Centrales"
    ],
    "m": "La neutralidad no la aisló de los efectos económicos."
  },
  {
    "q": "¿Cómo afectó la guerra al comercio argentino?",
    "ops": [
      "Se interrumpieron importaciones y bajó el comercio con Europa",
      "No tuvo ningún efecto",
      "Aumentaron las importaciones"
    ],
    "m": "Al faltar productos importados, algunas industrias locales empezaron a producirlos."
  },
  {
    "q": "¿Qué fue la crisis de 1929?",
    "ops": [
      "Una crisis económica mundial que empezó con la caída de la Bolsa de Nueva York",
      "Una guerra",
      "Una epidemia"
    ],
    "m": "Se conoce como el crack del '29 y derivó en la Gran Depresión."
  },
  {
    "q": "¿Cómo golpeó la crisis del '29 a la Argentina?",
    "ops": [
      "Cayeron los precios y la demanda de sus exportaciones",
      "Aumentaron las exportaciones",
      "No la afectó"
    ],
    "m": "Un país que vive de exportar materias primas queda muy expuesto a la demanda externa."
  },
  {
    "q": "¿Qué es la sustitución de importaciones?",
    "ops": [
      "Producir localmente lo que antes se compraba afuera",
      "Dejar de exportar",
      "Importar más productos"
    ],
    "m": "Se aceleró justamente cuando el comercio internacional se interrumpió."
  },
  {
    "q": "¿Qué relación hay entre la crisis del '29 y el golpe de 1930 en la Argentina?",
    "ops": [
      "La crisis agravó el descontento, aunque no fue su única causa",
      "La crisis causó el golpe por sí sola",
      "No hubo ninguna relación"
    ],
    "m": "Los procesos históricos suelen tener varias causas: conviene no reducirlo a una."
  },
  {
    "q": "¿Qué fue el Tratado de Versalles?",
    "ops": [
      "El acuerdo que cerró la Primera Guerra Mundial",
      "Un tratado comercial entre Argentina e Inglaterra",
      "El fin de la crisis del '29"
    ],
    "m": "Impuso duras condiciones a Alemania, con consecuencias que llegarían después."
  },
  {
    "q": "Durante la crisis, ¿qué pasó con el desempleo en el mundo?",
    "ops": [
      "Creció fuertemente",
      "Bajó",
      "Se mantuvo igual"
    ],
    "m": "La caída de la producción dejó a millones de personas sin trabajo."
  },
  {
    "q": "¿Por qué se dice que la economía argentina era vulnerable?",
    "ops": [
      "Porque dependía de pocos productos y de pocos compradores",
      "Porque no tenía recursos naturales",
      "Porque no tenía puertos"
    ],
    "m": "Depender de pocos mercados amplifica cualquier sacudón externo."
  },
  {
    "q": "¿Qué fue la Gran Depresión?",
    "ops": [
      "El largo período de crisis económica que siguió al crack de 1929",
      "Una batalla de la Primera Guerra",
      "Una crisis política argentina"
    ],
    "m": "Se extendió durante buena parte de la década del '30."
  },
  {
    "q": "La guerra en Europa, ¿favoreció en algo a la industria local argentina?",
    "ops": [
      "Sí, al faltar productos importados hubo que fabricarlos acá",
      "No, la perjudicó por completo",
      "No hubo ningún efecto"
    ],
    "m": "Fue un impulso limitado y por necesidad, no una política industrial planificada."
  },
  {
    "q": "¿Qué es una causa externa de un proceso histórico?",
    "ops": [
      "La que se origina fuera del país y lo afecta",
      "La que ocurre dentro del país",
      "La que no se puede comprobar"
    ],
    "m": "La crisis del '29 es externa; el descontento acumulado acá es interno."
  }
];
GAMES.gran_guerra_crisis_6 = juegoTriviaTexto(CUR_GRAN_GUERRA_CRISIS_6_BANCO, "Seguí la cadena de causas y consecuencias.", "gran_guerr");

/* 6° · Mercosur y la energía que viaja — mercosur_energia_6
   DC: Integración regional; grandes instalaciones de energía
   Fuente: docs/auditoria-dc-caba/grado-6.md · S7 */
const CUR_MERCOSUR_ENERGIA_6_BANCO = [
  {
    "q": "¿Qué es el Mercosur?",
    "ops": [
      "Un bloque de integración económica de países sudamericanos",
      "Una alianza militar",
      "Una empresa de energía"
    ],
    "m": "Su objetivo central es comercial y económico."
  },
  {
    "q": "¿Cuáles fueron los cuatro países fundadores del Mercosur?",
    "ops": [
      "Argentina, Brasil, Uruguay y Paraguay",
      "Argentina, Chile, Perú y Brasil",
      "Argentina, Brasil, Bolivia y Chile"
    ],
    "m": "Chile y Bolivia participan como asociados, no como fundadores."
  },
  {
    "q": "¿En qué año se firmó el Tratado de Asunción, que creó el Mercosur?",
    "ops": [
      "1991",
      "1980",
      "2001"
    ],
    "m": "Fue a comienzos de los años noventa."
  },
  {
    "q": "¿Qué ventaja busca un bloque de integración?",
    "ops": [
      "Comerciar entre sus miembros con menos trabas",
      "Cerrar las fronteras",
      "Unificar los gobiernos"
    ],
    "m": "Integrarse no significa dejar de ser países independientes."
  },
  {
    "q": "¿Qué es la represa de Yacyretá?",
    "ops": [
      "Una central hidroeléctrica compartida entre Argentina y Paraguay",
      "Una central nuclear",
      "Un puerto de exportación"
    ],
    "m": "Es un ejemplo de obra binacional de generación de energía."
  },
  {
    "q": "¿Qué es Salto Grande?",
    "ops": [
      "Una represa hidroeléctrica compartida con Uruguay",
      "Una central térmica en Buenos Aires",
      "Un parque eólico patagónico"
    ],
    "m": "Otra obra binacional, esta vez sobre el río Uruguay."
  },
  {
    "q": "¿Cómo llega la electricidad desde una represa hasta las ciudades?",
    "ops": [
      "Por líneas de alta tensión",
      "En camiones",
      "Por caños subterráneos de gas"
    ],
    "m": "El sistema interconectado nacional transporta la energía a distancia."
  },
  {
    "q": "¿Qué tipo de energía genera una represa hidroeléctrica?",
    "ops": [
      "Energía eléctrica a partir de la fuerza del agua",
      "Energía a partir del carbón",
      "Energía solar"
    ],
    "m": "Aprovecha el movimiento del agua para mover las turbinas."
  },
  {
    "q": "¿Dónde se ubican los principales parques eólicos argentinos?",
    "ops": [
      "En la Patagonia y el sur bonaerense",
      "En la selva misionera",
      "En el centro de la ciudad de Buenos Aires"
    ],
    "m": "Se instalan donde el viento es fuerte y constante."
  },
  {
    "q": "¿Qué es una central nuclear?",
    "ops": [
      "Una instalación que genera electricidad a partir de la fisión del átomo",
      "Una represa muy grande",
      "Un tipo de parque solar"
    ],
    "m": "La Argentina tiene tres: Atucha I, Atucha II y Embalse."
  },
  {
    "q": "¿Una obra binacional es…?",
    "ops": [
      "Una obra construida y administrada por dos países",
      "Una obra de una empresa privada",
      "Una obra que cruza dos provincias"
    ],
    "m": "Requiere un acuerdo entre los dos Estados."
  },
  {
    "q": "¿Por qué conviene integrarse regionalmente en materia de energía?",
    "ops": [
      "Porque las obras son muy caras y compartir recursos las hace posibles",
      "Porque así se consume menos",
      "Porque lo exige el Mercosur"
    ],
    "m": "Además permite compensar picos de demanda entre países."
  },
  {
    "q": "¿Qué es un país asociado del Mercosur?",
    "ops": [
      "Uno que participa con acuerdos parciales, sin ser miembro pleno",
      "Uno que fundó el bloque",
      "Uno que se retiró"
    ],
    "m": "Tiene beneficios comerciales pero no todas las obligaciones del miembro pleno."
  }
];
GAMES.mercosur_energia_6 = juegoTriviaTexto(CUR_MERCOSUR_ENERGIA_6_BANCO, "Pensá en la región y en cómo llega la energía.", "mercosur_e");

/* 6° · Demografía en gráficos — demografia_6
   DC: Natalidad, mortalidad y esperanza de vida; censos y su lectura
   Fuente: docs/auditoria-dc-caba/grado-6.md · S8a */
const CUR_DEMOGRAFIA_6_BANCO = [
  {
    "q": "¿Qué mide la tasa de natalidad?",
    "ops": [
      "Los nacimientos por cada mil habitantes en un año",
      "Las muertes por cada mil habitantes",
      "Cuántos años vive la gente"
    ],
    "m": "Cada tasa mide una cosa distinta: conviene no mezclarlas."
  },
  {
    "q": "¿Qué mide la tasa de mortalidad?",
    "ops": [
      "Las muertes por cada mil habitantes en un año",
      "Los nacimientos",
      "La cantidad de migrantes"
    ],
    "m": "Junto con la natalidad determina el crecimiento natural."
  },
  {
    "q": "¿Qué es la esperanza de vida?",
    "ops": [
      "El promedio de años que se espera que viva una persona",
      "La edad máxima que alcanza alguien",
      "La edad de jubilación"
    ],
    "m": "Es un promedio estadístico, no un límite individual."
  },
  {
    "q": "¿Qué es el crecimiento vegetativo?",
    "ops": [
      "La diferencia entre nacimientos y defunciones",
      "La cantidad de inmigrantes",
      "El total de habitantes"
    ],
    "m": "No incluye las migraciones: sólo nacimientos y muertes."
  },
  {
    "q": "Si en un país nacen más personas de las que mueren, el crecimiento vegetativo es…",
    "ops": [
      "Positivo",
      "Negativo",
      "Nulo"
    ],
    "m": "Sería negativo si murieran más de las que nacen."
  },
  {
    "q": "¿Qué muestra una pirámide de población?",
    "ops": [
      "Cómo se reparte la población por edad y sexo",
      "Dónde vive la gente",
      "Cuánto gana cada persona"
    ],
    "m": "Su forma resume la estructura demográfica de un país."
  },
  {
    "q": "Una pirámide con base ancha indica…",
    "ops": [
      "Una población joven, con alta natalidad",
      "Una población envejecida",
      "Que hay pocos habitantes"
    ],
    "m": "La base son los grupos de menor edad."
  },
  {
    "q": "¿Qué es la tasa de mortalidad infantil?",
    "ops": [
      "Cuántos bebés mueren antes del año por cada mil nacidos",
      "Cuántos chicos hay en el país",
      "Cuánto vive un adulto"
    ],
    "m": "Es uno de los indicadores más usados para medir las condiciones de vida."
  },
  {
    "q": "¿Cada cuánto se realiza el censo nacional en la Argentina?",
    "ops": [
      "Aproximadamente cada diez años",
      "Todos los años",
      "Cada cinco años"
    ],
    "m": "Esa periodicidad permite comparar décadas."
  },
  {
    "q": "Si la esperanza de vida aumenta, ¿qué suele pasar con la pirámide?",
    "ops": [
      "Se ensancha en la parte de arriba",
      "Se ensancha en la base",
      "No cambia"
    ],
    "m": "Más personas llegan a edades avanzadas."
  },
  {
    "q": "Si un país tiene más adultos mayores que chicos, ¿qué se espera?",
    "ops": [
      "Que necesite más servicios de salud",
      "Que suba la natalidad",
      "Que baje la esperanza de vida"
    ],
    "m": "La estructura por edades cambia lo que hay que planificar."
  },
  {
    "q": "En la Argentina, ¿cómo se distribuye la población?",
    "ops": [
      "De manera muy desigual, concentrada en pocas áreas urbanas",
      "De manera pareja en todo el territorio",
      "Sobre todo en zonas rurales"
    ],
    "m": "El área metropolitana de Buenos Aires concentra una parte enorme del total."
  },
  {
    "q": "Si un gráfico de líneas muestra la población subiendo año a año, ¿qué indica?",
    "ops": [
      "Que la población crece",
      "Que la población se mantiene",
      "Que la población baja"
    ],
    "m": "Una línea ascendente en el tiempo representa crecimiento."
  }
];
GAMES.demografia_6 = juegoTriviaTexto(CUR_DEMOGRAFIA_6_BANCO, "¿Qué mide cada indicador?", "demografia");

/* 6° · Escalas ambientales — escalas_ambientales_6
   DC: Escala local, regional y global; mitigación del riesgo
   Fuente: docs/auditoria-dc-caba/grado-6.md · S8b */
const CUR_ESCALAS_AMBIENTALES_6_BANCO = [
  {
    "it": "Basura acumulada en la esquina del barrio",
    "cat": "local",
    "m": "Afecta a quienes viven en ese lugar puntual."
  },
  {
    "it": "Contaminación de la cuenca Matanza-Riachuelo",
    "cat": "regional",
    "m": "Involucra a varios municipios y a toda una cuenca."
  },
  {
    "it": "Aumento de la temperatura media del planeta",
    "cat": "global",
    "m": "Ningún país lo resuelve por su cuenta."
  },
  {
    "it": "Un árbol caído que corta una calle",
    "cat": "local",
    "m": "Afecta a una manzana."
  },
  {
    "it": "Sequía prolongada en la región pampeana",
    "cat": "regional",
    "m": "Abarca varias provincias, pero no todo el planeta."
  },
  {
    "it": "Pérdida de biodiversidad en todo el mundo",
    "cat": "global",
    "m": "Es un proceso planetario."
  },
  {
    "it": "Ruido de una obra en construcción",
    "cat": "local",
    "m": "Molesta a los vecinos inmediatos."
  },
  {
    "it": "Deforestación del Gran Chaco",
    "cat": "regional",
    "m": "Se extiende por varias provincias y países vecinos."
  },
  {
    "it": "Acidificación de los océanos",
    "cat": "global",
    "m": "Afecta a todos los mares del planeta."
  },
  {
    "it": "Una plaza sin desagües que se inunda",
    "cat": "local",
    "m": "Un problema puntual de infraestructura barrial."
  },
  {
    "it": "Contaminación del río Paraná por vertidos industriales",
    "cat": "regional",
    "m": "Recorre varias provincias aguas abajo."
  },
  {
    "it": "Reducción de la capa de ozono",
    "cat": "global",
    "m": "Se abordó con un acuerdo internacional, el Protocolo de Montreal."
  },
  {
    "it": "Un basural a cielo abierto en las afueras del pueblo",
    "cat": "local",
    "m": "Afecta principalmente a esa localidad."
  },
  {
    "it": "Incendios en el delta del Paraná",
    "cat": "regional",
    "m": "Su humo llega a varias provincias."
  },
  {
    "it": "Aumento del nivel del mar",
    "cat": "global",
    "m": "Es consecuencia de procesos planetarios."
  },
  {
    "it": "Falta de arbolado en una avenida",
    "cat": "local",
    "m": "Se resuelve con una intervención en ese lugar."
  },
  {
    "it": "Retroceso de los glaciares patagónicos",
    "cat": "regional",
    "m": "Es un efecto regional de un proceso global."
  },
  {
    "it": "Emisiones mundiales de gases de efecto invernadero",
    "cat": "global",
    "m": "Se miden y se negocian a escala planetaria."
  }
];
GAMES.escalas_ambientales_6 = juegoClasificar(CUR_ESCALAS_AMBIENTALES_6_BANCO, "¿A qué escala ocurre este problema?", [{"cat": "local", "label": "🏘️ Local"}, {"cat": "regional", "label": "🗺️ Regional"}, {"cat": "global", "label": "🌎 Global"}], "escalas_am");

/* 6° · Mi Buenos Aires querido — buenos_aires_6
   DC: Patrimonio porteño: tango, fileteado, Obelisco, subte A, Reserva, Mataderos
   Fuente: docs/auditoria-dc-caba/grado-6.md · S9 */
const CUR_BUENOS_AIRES_6_BANCO = [
  {
    "q": "¿En qué año se inauguró el Obelisco?",
    "ops": [
      "1936",
      "1910",
      "1950"
    ],
    "m": "Se levantó para los 400 años de la primera fundación de la ciudad."
  },
  {
    "q": "¿Qué línea de subte fue la primera de Buenos Aires y de Sudamérica?",
    "ops": [
      "La línea A, en 1913",
      "La línea B, en 1930",
      "La línea D, en 1937"
    ],
    "m": "Fue la primera de toda Sudamérica."
  },
  {
    "q": "¿Qué reconocimiento recibió el tango de la UNESCO?",
    "ops": [
      "Patrimonio Cultural Inmaterial de la Humanidad",
      "Maravilla del mundo moderno",
      "Monumento histórico nacional"
    ],
    "m": "Inmaterial porque es una práctica viva, no un edificio."
  },
  {
    "q": "¿Qué es el fileteado porteño?",
    "ops": [
      "Un estilo de pintura decorativa típico de la ciudad",
      "Un baile",
      "Un tipo de comida"
    ],
    "m": "También fue declarado patrimonio inmaterial por la UNESCO."
  },
  {
    "q": "¿Qué es la Reserva Ecológica Costanera Sur?",
    "ops": [
      "Un área natural protegida junto al Río de la Plata",
      "Un parque de diversiones",
      "Un museo al aire libre"
    ],
    "m": "Se formó sobre terrenos ganados al río y se protegió en 1986."
  },
  {
    "q": "¿Qué se celebra en la Feria de Mataderos?",
    "ops": [
      "Las tradiciones criollas: música, danzas y destrezas",
      "El carnaval veneciano",
      "La cultura inmigrante europea"
    ],
    "m": "Es un espacio de cultura tradicional argentina en plena ciudad."
  },
  {
    "q": "¿Qué barrio porteño se asocia históricamente con el tango y el conventillo?",
    "ops": [
      "La Boca",
      "Palermo",
      "Belgrano"
    ],
    "m": "Fue zona portuaria y de gran presencia inmigrante."
  },
  {
    "q": "¿Qué es el patrimonio cultural INMATERIAL?",
    "ops": [
      "Las prácticas, saberes y expresiones que se transmiten entre personas",
      "Los edificios antiguos",
      "Las obras de arte de los museos"
    ],
    "m": "Lo material son objetos y edificios; lo inmaterial, prácticas vivas."
  },
  {
    "q": "¿Qué avenida cruza el Obelisco?",
    "ops": [
      "La 9 de Julio",
      "Rivadavia",
      "Corrientes"
    ],
    "m": "Corrientes también pasa por ahí, pero el Obelisco está sobre la 9 de Julio."
  },
  {
    "q": "¿Por qué el subte A tenía coches de madera hasta hace pocos años?",
    "ops": [
      "Porque eran los originales, conservados por su valor histórico",
      "Porque no había dinero para cambiarlos",
      "Porque la madera es más segura"
    ],
    "m": "Fueron declarados monumento histórico nacional."
  },
  {
    "q": "¿Qué caracteriza al fileteado como estilo?",
    "ops": [
      "Líneas curvas, colores fuertes, flores y frases populares",
      "Figuras geométricas en blanco y negro",
      "Fotografías retocadas"
    ],
    "m": "Nació decorando carros y colectivos de la ciudad."
  },
  {
    "q": "¿Cómo se formó el terreno de la Reserva Ecológica?",
    "ops": [
      "Con rellenos sobre el río que después se naturalizaron",
      "Fue siempre una isla natural",
      "Se construyó como parque planificado"
    ],
    "m": "La naturaleza colonizó un terreno de origen artificial."
  },
  {
    "q": "¿Qué es un monumento histórico nacional?",
    "ops": [
      "Un bien protegido por su valor para la historia del país",
      "Cualquier edificio antiguo",
      "Una estatua en una plaza"
    ],
    "m": "La protección la establece una declaración oficial, no la antigüedad sola."
  }
];
GAMES.buenos_aires_6 = juegoTriviaTexto(CUR_BUENOS_AIRES_6_BANCO, "Reconocé el patrimonio de la ciudad.", "buenos_air");

/* 6° · Elegí el instrumento — instrumentos_medida_6
   DC: Tecnología: instrumento y escala de medida; sensor→procesamiento→display
   Fuente: docs/auditoria-dc-caba/grado-6.md · T1 */
const CUR_INSTRUMENTOS_MEDIDA_6_BANCO = [
  {
    "q": "¿Con qué se mide la masa de una manzana?",
    "ops": [
      "Balanza",
      "Termómetro",
      "Cronómetro"
    ],
    "m": "El termómetro mide temperatura y el cronómetro, tiempo."
  },
  {
    "q": "¿Con qué se mide la temperatura del ambiente?",
    "ops": [
      "Termómetro",
      "Barómetro",
      "Anemómetro"
    ],
    "m": "El barómetro mide presión y el anemómetro, velocidad del viento."
  },
  {
    "q": "¿Con qué se mide la velocidad del viento?",
    "ops": [
      "Anemómetro",
      "Higrómetro",
      "Pluviómetro"
    ],
    "m": "El higrómetro mide humedad y el pluviómetro, lluvia acumulada."
  },
  {
    "q": "¿Con qué se mide la humedad del aire?",
    "ops": [
      "Higrómetro",
      "Termómetro",
      "Balanza"
    ],
    "m": "Cada variable meteorológica tiene su instrumento."
  },
  {
    "q": "Para medir el largo de un lápiz, ¿qué escala conviene?",
    "ops": [
      "Una regla en centímetros y milímetros",
      "Un metro de obra",
      "Un odómetro de auto"
    ],
    "m": "El instrumento tiene que tener la precisión adecuada al objeto."
  },
  {
    "q": "«Un lápiz mide 17 kilómetros.» ¿Qué está mal?",
    "ops": [
      "La unidad: debería ser centímetros",
      "El número",
      "El instrumento usado"
    ],
    "m": "Detectar una medida absurda es parte de saber medir."
  },
  {
    "q": "En un sistema de medición automática, ¿qué hace el sensor?",
    "ops": [
      "Capta la magnitud física y la convierte en una señal",
      "Muestra el resultado en pantalla",
      "Guarda los datos"
    ],
    "m": "Mostrar es la función del display, no del sensor."
  },
  {
    "q": "En ese mismo sistema, ¿qué hace el display?",
    "ops": [
      "Muestra el resultado ya procesado",
      "Capta la magnitud",
      "Realiza los cálculos"
    ],
    "m": "El orden es sensor, procesamiento y display."
  },
  {
    "q": "¿Cuál es el orden correcto de un sistema de medición automático?",
    "ops": [
      "Sensor, procesamiento, display",
      "Display, sensor, procesamiento",
      "Procesamiento, sensor, display"
    ],
    "m": "Primero se capta, después se procesa y al final se muestra."
  },
  {
    "q": "¿Qué es la precisión de un instrumento?",
    "ops": [
      "La menor diferencia que es capaz de distinguir",
      "El valor más alto que puede medir",
      "Su tamaño"
    ],
    "m": "El valor máximo es el alcance o rango, no la precisión."
  },
  {
    "q": "¿Con qué se mide la lluvia caída?",
    "ops": [
      "Pluviómetro",
      "Anemómetro",
      "Balanza"
    ],
    "m": "Mide la altura de agua acumulada en milímetros."
  },
  {
    "q": "Para pesar un camión, ¿qué instrumento se usa?",
    "ops": [
      "Una balanza de gran alcance, como la de una báscula",
      "Una balanza de cocina",
      "Una regla"
    ],
    "m": "Si el alcance no llega, la medición es imposible aunque el instrumento sea preciso."
  },
  {
    "q": "¿Con qué se mide un intervalo de tiempo corto?",
    "ops": [
      "Cronómetro",
      "Calendario",
      "Termómetro"
    ],
    "m": "El calendario sirve para días, no para segundos."
  },
  {
    "q": "¿Por qué conviene repetir una medición varias veces?",
    "ops": [
      "Para reducir el efecto de los errores",
      "Para gastar más tiempo",
      "Porque el instrumento se desgasta"
    ],
    "m": "Promediar varias mediciones da un resultado más confiable."
  }
];
GAMES.instrumentos_medida_6 = juegoTriviaTexto(CUR_INSTRUMENTOS_MEDIDA_6_BANCO, "¿Con qué se mide y en qué escala?", "instrument");

/* 6° · ¿Secuencial o condicional? — secuencial_condicional_6
   DC: Tecnología: algoritmos no lineales; comparación de algoritmos
   Fuente: docs/auditoria-dc-caba/grado-6.md · T2 */
const CUR_SECUENCIAL_CONDICIONAL_6_BANCO = [
  {
    "q": "¿Qué es un algoritmo secuencial?",
    "ops": [
      "Uno que ejecuta los pasos siempre en el mismo orden",
      "Uno que toma decisiones",
      "Uno que repite pasos"
    ],
    "m": "Si toma decisiones ya no es puramente secuencial."
  },
  {
    "q": "¿Qué agrega un bloque SI a un programa?",
    "ops": [
      "La posibilidad de hacer cosas distintas según una condición",
      "Más velocidad",
      "Más pasos siempre"
    ],
    "m": "Es lo que convierte al algoritmo en no lineal."
  },
  {
    "q": "«Si llueve, llevá paraguas; si no, llevá gorra.» ¿Qué estructura es?",
    "ops": [
      "Condicional",
      "Secuencial",
      "Repetitiva"
    ],
    "m": "Hay dos caminos posibles según una condición."
  },
  {
    "q": "«Ponete las medias, después las zapatillas, después atá los cordones.» ¿Qué estructura es?",
    "ops": [
      "Secuencial",
      "Condicional",
      "Repetitiva"
    ],
    "m": "Los pasos van siempre en el mismo orden, sin decidir nada."
  },
  {
    "q": "¿Qué es un bucle o repetición?",
    "ops": [
      "Una estructura que repite pasos varias veces",
      "Una estructura que decide entre dos caminos",
      "Un error del programa"
    ],
    "m": "Repetir y decidir son estructuras distintas."
  },
  {
    "q": "«Repetí 4 veces: avanzá 10 y girá 90°.» ¿Qué dibuja?",
    "ops": [
      "Un cuadrado",
      "Un triángulo",
      "Un círculo"
    ],
    "m": "Cuatro lados iguales con giros de 90° cierran un cuadrado."
  },
  {
    "q": "Para dibujar un triángulo equilátero repitiendo, ¿cuánto hay que girar?",
    "ops": [
      "120°",
      "90°",
      "60°"
    ],
    "m": "Los giros exteriores tienen que sumar 360°: 360 ÷ 3 = 120."
  },
  {
    "q": "Si dos programas hacen lo mismo, ¿cuál conviene?",
    "ops": [
      "El que usa menos pasos y se entiende mejor",
      "El más largo",
      "El que tiene más bloques distintos"
    ],
    "m": "Comparar algoritmos es parte del contenido: no alcanza con que funcione."
  },
  {
    "q": "«Si el sensor detecta luz, encendé el motor.» Si no hay luz, ¿qué pasa?",
    "ops": [
      "No se enciende el motor",
      "Se enciende igual",
      "El programa se rompe"
    ],
    "m": "Sin la parte «si no», simplemente no se ejecuta esa acción."
  },
  {
    "q": "¿Qué es una condición en programación?",
    "ops": [
      "Una pregunta que se responde con verdadero o falso",
      "Un paso que siempre se ejecuta",
      "El final del programa"
    ],
    "m": "Según esa respuesta, el programa toma un camino u otro."
  },
  {
    "q": "«Avanzá hasta que toques la pared.» ¿Qué estructura combina?",
    "ops": [
      "Repetición con una condición",
      "Sólo secuencia",
      "Sólo condición"
    ],
    "m": "Repite avanzar mientras la condición no se cumpla."
  },
  {
    "q": "¿Por qué conviene usar un bucle en vez de repetir el mismo bloque 20 veces?",
    "ops": [
      "Porque el programa queda más corto y fácil de cambiar",
      "Porque se ejecuta más rápido siempre",
      "Porque ocupa más memoria"
    ],
    "m": "Si hay que cambiar el paso, con el bucle se cambia en un solo lugar."
  },
  {
    "q": "«Si el número es par, sumá 1; si no, restá 1.» ¿Cuántos caminos tiene?",
    "ops": [
      "Dos",
      "Uno",
      "Ninguno"
    ],
    "m": "El «si no» abre el segundo camino."
  },
  {
    "q": "Un programa que siempre hace exactamente lo mismo, ¿puede reaccionar al entorno?",
    "ops": [
      "No, para eso necesita condicionales",
      "Sí, siempre",
      "Sólo si es muy largo"
    ],
    "m": "Reaccionar significa decidir según lo que pasa afuera."
  }
];
GAMES.secuencial_condicional_6 = juegoTriviaTexto(CUR_SECUENCIAL_CONDICIONAL_6_BANCO, "Pensá si el programa siempre hace lo mismo.", "secuencial");

/* 6° · Bloques ↔ código — bloques_codigo_6
   DC: Tecnología: programación en bloques y su relación con el código
   Fuente: docs/auditoria-dc-caba/grado-6.md · T3 */
const CUR_BLOQUES_CODIGO_6_BANCO = [
  {
    "q": "El bloque «repetir 10 veces» equivale en código a…",
    "ops": [
      "Un bucle for",
      "Un condicional if",
      "Una variable"
    ],
    "m": "El if decide; el for repite una cantidad conocida de veces."
  },
  {
    "q": "El bloque «si… entonces» equivale en código a…",
    "ops": [
      "Un if",
      "Un for",
      "Un print"
    ],
    "m": "El if evalúa una condición."
  },
  {
    "q": "El bloque «decir Hola» equivale a…",
    "ops": [
      "Una instrucción de salida, como print",
      "Una variable",
      "Un condicional"
    ],
    "m": "Mostrar algo en pantalla es una salida."
  },
  {
    "q": "¿Qué es una variable en programación?",
    "ops": [
      "Un espacio con nombre donde se guarda un valor",
      "Un bloque que repite",
      "Un error del programa"
    ],
    "m": "Se le puede cambiar el valor durante la ejecución: por eso es variable."
  },
  {
    "q": "¿Cuál es la ventaja de programar en bloques?",
    "ops": [
      "No se puede escribir mal la sintaxis",
      "Es más rápido de ejecutar",
      "Permite hacer más cosas que el código"
    ],
    "m": "El código escrito permite MÁS cosas; los bloques evitan los errores de tipeo."
  },
  {
    "q": "¿Los bloques y el código hacen cosas distintas?",
    "ops": [
      "No, expresan las mismas ideas de dos formas",
      "Sí, son incompatibles",
      "Sí, el código no tiene bucles"
    ],
    "m": "Cambia la forma de escribirlo, no lo que se puede expresar."
  },
  {
    "q": "En «x = 5», ¿qué se está haciendo?",
    "ops": [
      "Guardando el valor 5 en la variable x",
      "Comparando x con 5",
      "Repitiendo 5 veces"
    ],
    "m": "El signo = asigna; para comparar se usa otro símbolo."
  },
  {
    "q": "El bloque «esperar 2 segundos» sirve para…",
    "ops": [
      "Pausar el programa un momento",
      "Repetir 2 veces",
      "Guardar el número 2"
    ],
    "m": "Es una pausa, no una repetición."
  },
  {
    "q": "¿Para qué sirve agrupar bloques en un procedimiento?",
    "ops": [
      "Para reusar la misma secuencia sin repetirla",
      "Para que el programa corra más rápido",
      "Para esconder los errores"
    ],
    "m": "Si hay que cambiarla, se cambia en un solo lugar."
  },
  {
    "q": "Si un programa da un resultado incorrecto, ¿qué hay que hacer?",
    "ops": [
      "Depurarlo: buscar dónde falla la lógica",
      "Empezar de cero siempre",
      "Agregar más bloques"
    ],
    "m": "Depurar es leer el programa paso a paso hasta encontrar el error."
  },
  {
    "q": "¿Qué es la sintaxis de un lenguaje de programación?",
    "ops": [
      "Las reglas de escritura que el lenguaje exige",
      "La velocidad del programa",
      "La cantidad de líneas"
    ],
    "m": "Si no se respeta, el programa ni siquiera arranca."
  },
  {
    "q": "«mover 10 pasos» dentro de «repetir 4 veces» hace que el objeto…",
    "ops": [
      "Avance 40 pasos en total",
      "Avance 10 pasos",
      "No se mueva"
    ],
    "m": "El bloque de adentro se ejecuta una vez por repetición."
  },
  {
    "q": "¿Qué significa anidar bloques?",
    "ops": [
      "Poner una estructura adentro de otra",
      "Ponerlas una al lado de la otra",
      "Borrar una estructura"
    ],
    "m": "Un if adentro de un for es un ejemplo de anidamiento."
  },
  {
    "q": "¿Para qué sirve comentar un programa?",
    "ops": [
      "Para explicar qué hace cada parte a quien lo lea después",
      "Para que se ejecute más rápido",
      "Para agregar funciones"
    ],
    "m": "Los comentarios no se ejecutan: son para las personas."
  }
];
GAMES.bloques_codigo_6 = juegoTriviaTexto(CUR_BLOQUES_CODIGO_6_BANCO, "¿Qué hace esta instrucción?", "bloques_co");

/* 6° · Las 5 etapas del diseño — etapas_diseno_6
   DC: Tecnología: empatizar, definir, idear, prototipar y evaluar
   Fuente: docs/auditoria-dc-caba/grado-6.md · T4 */
const CUR_ETAPAS_DISENO_6_BANCO = [
  {
    "items": [
      "Preguntarles a los chicos qué les molesta del patio",
      "Escribir el problema en una sola frase",
      "Hacer una lluvia de ideas de soluciones",
      "Armar una maqueta de cartón",
      "Probarla en el recreo y anotar qué falló"
    ]
  },
  {
    "items": [
      "Observar cómo usan la mochila los compañeros",
      "Definir que el problema es el peso mal repartido",
      "Proponer varias formas de repartirlo",
      "Construir un modelo con materiales simples",
      "Pedirle a alguien que la use y dé su opinión"
    ]
  },
  {
    "items": [
      "Entrevistar a los vecinos sobre la plaza",
      "Delimitar qué se va a resolver",
      "Dibujar tres propuestas distintas",
      "Hacer un prototipo a escala",
      "Evaluar cuál funciona mejor"
    ]
  },
  {
    "items": [
      "Ponerse en el lugar de quien va a usar el objeto",
      "Formular el problema con precisión",
      "Generar la mayor cantidad de ideas posible",
      "Materializar la idea elegida",
      "Poner a prueba el resultado"
    ]
  },
  {
    "items": [
      "Escuchar a quien tiene la necesidad",
      "Acotar el problema a algo resoluble",
      "Buscar muchas alternativas sin descartar",
      "Construir una primera versión rápida",
      "Medir si resolvió lo que se buscaba"
    ]
  },
  {
    "items": [
      "Registrar cómo se usa hoy el bebedero de la escuela",
      "Definir que se desperdicia agua",
      "Pensar formas de evitar el desperdicio",
      "Armar un prototipo con una botella",
      "Probarlo una semana y comparar el consumo"
    ]
  },
  {
    "items": [
      "Averiguar por qué se traba la puerta del aula",
      "Enunciar el problema concreto",
      "Idear tres mecanismos distintos",
      "Construir el que parece más simple",
      "Verificar si la puerta ya no se traba"
    ]
  },
  {
    "items": [
      "Conversar con el bibliotecario sobre los libros perdidos",
      "Definir que falta un sistema de registro",
      "Proponer varias formas de registrarlos",
      "Hacer una versión de prueba en papel",
      "Usarla un mes y ver si funcionó"
    ]
  },
  {
    "items": [
      "Mirar cómo se forma la fila del comedor",
      "Precisar dónde se genera la demora",
      "Imaginar distintos recorridos posibles",
      "Marcar uno en el piso como prueba",
      "Cronometrar si la fila avanza más rápido"
    ]
  }
];
GAMES.etapas_diseno_6 = juegoOrdenar(CUR_ETAPAS_DISENO_6_BANCO, "Ordená el proceso de diseño. Tocá en orden.", "Primero se entiende el problema; recién al final se evalúa la solución.", "etapas_dis");

/* 6° · Sensores y control reactivo — sensores_6
   DC: Tecnología: control reactivo; sensores analógicos y digitales; autoría e IA
   Fuente: docs/auditoria-dc-caba/grado-6.md · T5 */
const CUR_SENSORES_6_BANCO = [
  {
    "q": "¿Qué diferencia hay entre un sensor digital y uno analógico?",
    "ops": [
      "El digital da dos estados y el analógico muchos valores",
      "El digital es más rápido",
      "El analógico no necesita corriente"
    ],
    "m": "Un pulsador dice sí o no; uno de temperatura da toda una escala."
  },
  {
    "q": "En un control reactivo, ¿qué pasa si falla el sensor?",
    "ops": [
      "El sistema decide a ciegas",
      "Se apaga solo",
      "El actuador lo reemplaza"
    ],
    "m": "Sin la entrada, la decisión se toma sin la información que hacía falta."
  },
  {
    "q": "«Si la humedad de la tierra baja, activá el riego.» ¿Qué tipo de control es?",
    "ops": [
      "Reactivo: responde a lo que mide",
      "Manual",
      "Sin control"
    ],
    "m": "El sistema reacciona a una medición, sin que nadie intervenga."
  },
  {
    "q": "¿Cuál es la diferencia entre un sensor digital y uno analógico?",
    "ops": [
      "El digital entrega dos estados; el analógico, un rango de valores",
      "El digital es más nuevo",
      "El analógico no funciona con electricidad"
    ],
    "m": "Un pulsador es digital: apretado o no. Un termómetro entrega un rango."
  },
  {
    "q": "Un botón de encendido, ¿es un sensor digital o analógico?",
    "ops": [
      "Digital: sólo tiene dos estados",
      "Analógico",
      "Ninguno de los dos"
    ],
    "m": "Apretado o suelto: no hay valores intermedios."
  },
  {
    "q": "Un sensor de temperatura que entrega valores de 0 a 50 °C es…",
    "ops": [
      "Analógico",
      "Digital",
      "Un actuador"
    ],
    "m": "Entrega un rango continuo de valores, no dos estados."
  },
  {
    "q": "En un invernadero automático, ¿qué sería el actuador?",
    "ops": [
      "El motor que abre la ventana",
      "El sensor de temperatura",
      "La pantalla que muestra los datos"
    ],
    "m": "El actuador es el que produce el cambio físico."
  },
  {
    "q": "¿Qué es la realimentación en un sistema de control?",
    "ops": [
      "Volver a medir para ajustar la acción",
      "Cargar la batería",
      "Reiniciar el sistema"
    ],
    "m": "El resultado de la acción vuelve a entrar como información."
  },
  {
    "q": "¿Por qué hay que señalar cuando un contenido fue generado con inteligencia artificial?",
    "ops": [
      "Para que quien lo lea sepa cómo se produjo",
      "Porque siempre está mal",
      "Porque es obligatorio por ley en todos lados"
    ],
    "m": "La autoría es información relevante para evaluar un contenido."
  },
  {
    "q": "Si una IA genera un texto con un dato falso, ¿de quién es la responsabilidad de chequearlo?",
    "ops": [
      "De quien lo publica o lo usa",
      "De nadie",
      "Sólo de la empresa que la creó"
    ],
    "m": "Usar una herramienta no traslada la responsabilidad sobre lo que se publica."
  },
  {
    "q": "Un sensor de luz que enciende el alumbrado al anochecer, ¿qué controla?",
    "ops": [
      "Un sistema reactivo de iluminación",
      "Un sistema manual",
      "Nada, es un display"
    ],
    "m": "Mide la luz ambiente y actúa en consecuencia."
  },
  {
    "q": "¿Qué necesita un sistema para ser reactivo?",
    "ops": [
      "Sensor, lógica de decisión y actuador",
      "Sólo un sensor",
      "Sólo un motor"
    ],
    "m": "Sin la parte que decide, el sensor y el motor no se coordinan."
  },
  {
    "q": "«Si la puerta está abierta más de 30 segundos, sonar la alarma.» ¿Qué mide el sensor?",
    "ops": [
      "Si la puerta está abierta o cerrada",
      "El volumen de la alarma",
      "La temperatura"
    ],
    "m": "Es un sensor digital de dos estados, combinado con un tiempo."
  },
  {
    "q": "¿Puede un sistema reactivo funcionar sin condicionales?",
    "ops": [
      "No, necesita decidir según lo que mide",
      "Sí, siempre",
      "Sólo si es muy simple"
    ],
    "m": "Reaccionar es exactamente lo que hace un condicional."
  }
];
GAMES.sensores_6 = juegoTriviaTexto(CUR_SENSORES_6_BANCO, "Pensá qué detecta y qué hace el sistema.", "sensores_6");

/* 6° · Chat seguro — chat_seguro_6
   DC: Transversal ESI + Educación Digital: grooming como delito; cómo actuar
   Fuente: docs/auditoria-dc-caba/grado-6.md · Tr1 */
const CUR_CHAT_SEGURO_6_BANCO = [
  {
    "q": "Alguien que no conocés te escribe y dice ser de tu edad. ¿Qué conviene?",
    "ops": [
      "No aceptar y contarle a un adulto de confianza",
      "Contestarle para ver quién es",
      "Bloquearlo y no decir nada"
    ],
    "m": "Bloquear está bien, pero avisarle a un adulto es lo que suma protección."
  },
  {
    "q": "Un adulto te pide por chat que no le cuentes a nadie que hablan. ¿Qué significa?",
    "ops": [
      "Es una señal de alarma: hay que contarlo enseguida",
      "Que quiere respetar tu privacidad",
      "Que es normal entre amigos"
    ],
    "m": "Pedir secreto frente a los adultos que te cuidan es la señal más clara."
  },
  {
    "q": "¿Qué es el grooming?",
    "ops": [
      "Cuando un adulto contacta a un chico por internet para dañarlo",
      "Un juego en línea",
      "Un tipo de virus informático"
    ],
    "m": "En la Argentina es un delito previsto en el Código Penal."
  },
  {
    "q": "¿Está bien mandar fotos íntimas aunque te las pida alguien conocido?",
    "ops": [
      "No, nunca; y si te presionan hay que contarlo",
      "Sí, si es alguien conocido",
      "Sí, si prometen borrarla"
    ],
    "m": "Una vez enviada, la imagen deja de estar bajo tu control."
  },
  {
    "q": "Si un compañero comparte una foto tuya sin permiso, ¿qué hacés?",
    "ops": [
      "Avisarle a un adulto y guardar la evidencia",
      "Compartir una de él",
      "No hacer nada"
    ],
    "m": "Responder con lo mismo agrega un problema en vez de resolverlo."
  },
  {
    "q": "¿Por qué conviene tener el perfil privado?",
    "ops": [
      "Porque sólo ven tus cosas quienes vos aceptás",
      "Porque así tenés más seguidores",
      "Porque la app anda más rápido"
    ],
    "m": "Reduce cuánta información sobre vos queda al alcance de desconocidos."
  },
  {
    "q": "Alguien te dice que si no le contestás le va a pasar algo malo. ¿Qué es eso?",
    "ops": [
      "Una forma de manipulación: hay que contarlo",
      "Una preocupación genuina",
      "Una broma sin importancia"
    ],
    "m": "Generar culpa para que no cortes el contacto es una técnica conocida."
  },
  {
    "q": "¿Qué información NO conviene publicar?",
    "ops": [
      "Dirección, escuela y horarios",
      "Tu color favorito",
      "Una película que te gustó"
    ],
    "m": "Los datos que permiten ubicarte físicamente son los sensibles."
  },
  {
    "q": "¿Cómo tiene que ser una contraseña segura?",
    "ops": [
      "Larga, con letras, números y símbolos, y no compartida",
      "Tu fecha de nacimiento",
      "La misma para todas las cuentas"
    ],
    "m": "Repetir la contraseña hace que un solo robo abra todas tus cuentas."
  },
  {
    "q": "Si algo en internet te hace sentir incómodo, ¿qué es lo primero?",
    "ops": [
      "Contárselo a un adulto de confianza",
      "Resolverlo solo",
      "Seguir la conversación para entender"
    ],
    "m": "No es tu responsabilidad resolverlo solo: para eso están los adultos."
  },
  {
    "q": "¿Es tu culpa si un adulto te contactó y te engañó?",
    "ops": [
      "No, la responsabilidad es siempre del adulto",
      "Sí, por aceptar la solicitud",
      "Depende de qué le contestaste"
    ],
    "m": "Esto es importante: la culpa nunca es del chico, y no hablar por vergüenza es lo que el adulto busca."
  },
  {
    "q": "¿Está bien aceptar como contacto a alguien que no conocés?",
    "ops": [
      "No, aunque diga tener tu edad",
      "Sí, si tienen amigos en común",
      "Sí, si dice ser de tu barrio"
    ],
    "m": "En internet la edad que alguien dice tener no se puede comprobar."
  },
  {
    "q": "Un desconocido te ofrece regalos o dinero por chat. ¿Qué hacés?",
    "ops": [
      "No aceptar y avisarle a un adulto",
      "Aceptar si es poco",
      "Preguntarle por qué"
    ],
    "m": "El regalo suele ser la forma de crear una deuda y sostener el contacto."
  },
  {
    "q": "¿Qué significa que algo publicado en internet deja huella?",
    "ops": [
      "Que puede quedar aunque lo borres",
      "Que se borra solo",
      "Que nadie lo puede ver"
    ],
    "m": "Otros pueden haberlo guardado antes de que lo borres."
  }
];
GAMES.chat_seguro_6 = juegoTriviaTexto(CUR_CHAT_SEGURO_6_BANCO, "¿Qué conviene hacer en esta situación?", "chat_segur");

/* 6° · Mitos, ITS y tipos de violencia — its_violencia_6
   DC: Transversal ESI: vías de transmisión y prevención de ITS; tipos de violencia
   Fuente: docs/auditoria-dc-caba/grado-6.md · Tr2 */
const CUR_ITS_VIOLENCIA_6_BANCO = [
  {
    "q": "¿Qué significa ITS?",
    "ops": [
      "Infección de transmisión sexual",
      "Infección de tipo severo",
      "Enfermedad hereditaria"
    ],
    "m": "Se transmiten entre personas; no se heredan."
  },
  {
    "q": "¿El VIH se transmite por compartir el mate?",
    "ops": [
      "No, la saliva no transmite VIH",
      "Sí, siempre",
      "Sí, a veces"
    ],
    "m": "Es uno de los mitos más extendidos y sostiene la discriminación."
  },
  {
    "q": "¿El VIH se transmite por abrazar a una persona que lo tiene?",
    "ops": [
      "No, el contacto cotidiano no lo transmite",
      "Sí",
      "Sólo si hay sudor"
    ],
    "m": "Ni abrazos, ni besos, ni compartir el baño o la vajilla."
  },
  {
    "q": "¿Cuál es el método más efectivo para prevenir las ITS?",
    "ops": [
      "El preservativo",
      "Las pastillas anticonceptivas",
      "Ninguno"
    ],
    "m": "Es el único que funciona como barrera contra las infecciones."
  },
  {
    "q": "¿Se puede tener una ITS sin síntomas?",
    "ops": [
      "Sí, por eso los controles médicos son importantes",
      "No, siempre hay síntomas",
      "Sólo en los adultos mayores"
    ],
    "m": "Muchas cursan sin señales visibles durante mucho tiempo."
  },
  {
    "q": "¿Qué es la violencia física?",
    "ops": [
      "La que daña el cuerpo con golpes o empujones",
      "La que se ejerce con palabras",
      "La que controla el dinero"
    ],
    "m": "Cada tipo de violencia tiene su forma; nombrarlas ayuda a reconocerlas."
  },
  {
    "q": "¿Qué es la violencia psicológica?",
    "ops": [
      "Humillar, amenazar o descalificar de manera sostenida",
      "Sólo los golpes",
      "Sólo el control del dinero"
    ],
    "m": "No deja marcas visibles, y por eso a veces cuesta reconocerla."
  },
  {
    "q": "¿Qué es la violencia simbólica?",
    "ops": [
      "Mensajes e imágenes que naturalizan la desigualdad",
      "Una discusión fuerte",
      "Un golpe accidental"
    ],
    "m": "Circula en publicidades, chistes y frases repetidas."
  },
  {
    "q": "Si un compañero se burla todos los días de otro, ¿qué es?",
    "ops": [
      "Una forma de violencia, y hay que contarlo",
      "Una broma sin importancia",
      "Un problema entre ellos dos"
    ],
    "m": "La repetición sostenida es lo que la convierte en hostigamiento."
  },
  {
    "q": "¿Qué es el consentimiento?",
    "ops": [
      "Estar de acuerdo de manera libre, y poder cambiar de opinión",
      "Aceptar porque te insistieron",
      "No decir nada"
    ],
    "m": "El silencio no es consentimiento, y aceptar bajo presión tampoco."
  },
  {
    "q": "¿Dónde se puede consultar sobre salud sexual en la Argentina?",
    "ops": [
      "En un centro de salud, de forma gratuita y confidencial",
      "En ningún lado",
      "Sólo en clínicas privadas"
    ],
    "m": "La atención en el sistema público es gratuita y confidencial."
  },
  {
    "q": "Si alguien te toca sin tu permiso, ¿qué hacés?",
    "ops": [
      "Decir que no y contárselo a un adulto de confianza",
      "Callarte para no hacer lío",
      "Esperar a ver si se repite"
    ],
    "m": "Tu cuerpo es tuyo, y avisar es siempre lo correcto."
  },
  {
    "q": "¿Existe una ITS que se cure sola sin tratamiento?",
    "ops": [
      "No conviene asumirlo: hay que consultar siempre",
      "Sí, todas se curan solas",
      "Sí, la mayoría"
    ],
    "m": "Algunas se curan con tratamiento y otras se controlan; ninguna conviene dejar librada al azar."
  },
  {
    "q": "¿Qué hace la vacuna contra el VPH?",
    "ops": [
      "Previene infecciones que pueden causar cáncer",
      "Cura una infección ya presente",
      "Reemplaza al preservativo"
    ],
    "m": "Está en el calendario nacional y es gratuita."
  }
];
GAMES.its_violencia_6 = juegoTriviaTexto(CUR_ITS_VIOLENCIA_6_BANCO, "Distinguí lo que es cierto de lo que se dice.", "its_violen");

/* 6° · Los tres poderes y la ley — tres_poderes_6
   DC: Transversal FEC: división de poderes; sanción de las leyes; sufragio
   Fuente: docs/auditoria-dc-caba/grado-6.md · Tr3 */
const CUR_TRES_PODERES_6_BANCO = [
  {
    "it": "Sancionar una ley nueva",
    "cat": "legislativo",
    "m": "Hacer las leyes es la función del Congreso."
  },
  {
    "it": "Reglamentar y hacer cumplir una ley ya sancionada",
    "cat": "ejecutivo",
    "m": "El Ejecutivo administra y ejecuta lo que la ley establece."
  },
  {
    "it": "Resolver un juicio entre dos personas",
    "cat": "judicial",
    "m": "Juzgar y aplicar la ley a un caso concreto es del Poder Judicial."
  },
  {
    "it": "Debatir un proyecto en la Cámara de Diputados",
    "cat": "legislativo",
    "m": "Diputados y Senadores integran el Congreso."
  },
  {
    "it": "Nombrar a los ministros del gabinete",
    "cat": "ejecutivo",
    "m": "El Presidente encabeza el Poder Ejecutivo."
  },
  {
    "it": "Declarar que una ley es inconstitucional",
    "cat": "judicial",
    "m": "El control de constitucionalidad lo ejerce la Justicia."
  },
  {
    "it": "Aprobar el presupuesto nacional",
    "cat": "legislativo",
    "m": "El Congreso lo discute y lo aprueba."
  },
  {
    "it": "Vetar total o parcialmente una ley",
    "cat": "ejecutivo",
    "m": "Es una facultad del Presidente dentro del proceso de sanción."
  },
  {
    "it": "Dictar una sentencia",
    "cat": "judicial",
    "m": "Es el acto por el cual un juez resuelve un caso."
  },
  {
    "it": "Discutir el proyecto en el Senado",
    "cat": "legislativo",
    "m": "El Senado es la otra cámara del Congreso."
  },
  {
    "it": "Conducir la administración del país",
    "cat": "ejecutivo",
    "m": "Es la función central del Poder Ejecutivo."
  },
  {
    "it": "Integrar la Corte Suprema de Justicia",
    "cat": "judicial",
    "m": "Es el máximo tribunal del país."
  },
  {
    "it": "Modificar una ley existente",
    "cat": "legislativo",
    "m": "Sólo el Congreso puede cambiar una ley."
  },
  {
    "it": "Promulgar una ley aprobada por el Congreso",
    "cat": "ejecutivo",
    "m": "Es el paso final para que la ley entre en vigencia."
  },
  {
    "it": "Investigar si alguien cometió un delito, a cargo de un fiscal",
    "cat": "judicial",
    "m": "La investigación penal forma parte del ámbito judicial."
  },
  {
    "it": "Tratar un proyecto en comisión antes de votarlo",
    "cat": "legislativo",
    "m": "Las comisiones son parte del trabajo del Congreso."
  }
];
GAMES.tres_poderes_6 = juegoClasificar(CUR_TRES_PODERES_6_BANCO, "¿Qué poder hace esto?", [{"cat": "legislativo", "label": "🏛️ Legislativo"}, {"cat": "ejecutivo", "label": "🏢 Ejecutivo"}, {"cat": "judicial", "label": "⚖️ Judicial"}], "tres_poder");

/* 6° · Billetera virtual y presupuesto — presupuesto_6
   DC: Transversal Educación Financiera: medios de pago, seguridad y presupuesto
   Fuente: docs/auditoria-dc-caba/grado-6.md · Tr4 */
const CUR_PRESUPUESTO_6_BANCO = [
  {
    "q": "Si tu presupuesto destina 50% a gastos fijos y 30% a variables, ¿cuánto queda para ahorro?",
    "ops": [
      "20%",
      "30%",
      "10%"
    ],
    "m": "El total siempre es 100%: 100 − 50 − 30 = 20."
  },
  {
    "q": "¿Qué es un gasto fijo?",
    "ops": [
      "El que se repite igual todos los meses",
      "El que cambia según el mes",
      "El que se hace una sola vez"
    ],
    "m": "El alquiler es fijo; la salida del fin de semana, variable."
  },
  {
    "q": "Alguien te escribe diciendo que ganaste un premio y te pide tu clave. ¿Qué es?",
    "ops": [
      "Una estafa: nunca se comparte la clave",
      "Un premio real",
      "Un aviso del banco"
    ],
    "m": "Ninguna entidad legítima pide la clave por mensaje."
  },
  {
    "q": "¿Qué es un código de seguridad de un solo uso?",
    "ops": [
      "Un código que confirma una operación y no se comparte con nadie",
      "Tu contraseña habitual",
      "El número de tu documento"
    ],
    "m": "Pedírtelo por teléfono o chat es la señal de estafa más frecuente."
  },
  {
    "q": "¿Qué diferencia hay entre débito y crédito?",
    "ops": [
      "El débito descuenta al instante; el crédito, después",
      "Son exactamente lo mismo",
      "El débito siempre cobra interés"
    ],
    "m": "Con crédito estás usando plata que todavía no pagaste."
  },
  {
    "q": "Si pagás en cuotas «sin interés», ¿siempre pagás lo mismo?",
    "ops": [
      "Conviene comparar: a veces el precio de contado es menor",
      "Sí, siempre es igual",
      "No, siempre es más caro"
    ],
    "m": "El «sin interés» a veces ya está incluido en el precio de lista."
  },
  {
    "q": "¿Qué es ahorrar?",
    "ops": [
      "Guardar una parte de lo que entra para después",
      "Gastar menos de lo que se puede",
      "No comprar nunca nada"
    ],
    "m": "No es privarse de todo: es apartar una parte de forma planificada."
  },
  {
    "q": "Si gastás más de lo que entra, ¿qué pasa?",
    "ops": [
      "Te endeudás",
      "Ahorrás",
      "No pasa nada"
    ],
    "m": "La diferencia sale de algún lado: de ahorros previos o de deuda."
  },
  {
    "q": "¿Conviene usar la misma clave para el banco y para las redes?",
    "ops": [
      "No, si roban una quedan expuestas todas",
      "Sí, es más fácil de recordar",
      "Sí, si es larga"
    ],
    "m": "Repetir claves multiplica el daño de un solo robo."
  },
  {
    "q": "En un presupuesto, ¿qué son los ingresos?",
    "ops": [
      "La plata que entra",
      "La plata que sale",
      "Lo que se ahorra"
    ],
    "m": "Los egresos son lo que sale."
  },
  {
    "q": "Si tenés $10.000 y destinás el 20% al ahorro, ¿cuánto ahorrás?",
    "ops": [
      "$2.000",
      "$200",
      "$8.000"
    ],
    "m": "El 20% de 10.000 es 2.000. $8.000 es lo que queda para gastar."
  },
  {
    "q": "Un link que llega por mensaje y pide iniciar sesión en el banco, ¿qué conviene hacer?",
    "ops": [
      "No entrar y abrir la app oficial por separado",
      "Entrar y verificar",
      "Reenviarlo para consultar"
    ],
    "m": "Los links falsos imitan la página real: siempre conviene entrar por la vía propia."
  },
  {
    "q": "¿Qué es una transferencia?",
    "ops": [
      "El envío de dinero de una cuenta a otra",
      "Un tipo de préstamo",
      "Un descuento en una compra"
    ],
    "m": "Una vez hecha, revertirla no es automático: conviene verificar antes."
  },
  {
    "q": "Si querés comprar algo que cuesta más de lo que tenés, ¿qué opción es más sana?",
    "ops": [
      "Planificar un ahorro mensual hasta juntarlo",
      "Pedirlo prestado sin plan",
      "Comprarlo igual en muchas cuotas"
    ],
    "m": "Endeudarse sin plan es lo que convierte una compra en un problema."
  }
];
GAMES.presupuesto_6 = juegoTriviaTexto(CUR_PRESUPUESTO_6_BANCO, "Cuidá la plata y los datos.", "presupuest");

/* 6° · Economía circular y el Riachuelo — economia_circular_6
   DC: Transversal Educación Ambiental: economía lineal vs circular; cuenca del Riachuelo
   Fuente: docs/auditoria-dc-caba/grado-6.md · Tr5 */
const CUR_ECONOMIA_CIRCULAR_6_BANCO = [
  {
    "it": "Comprar una botella, usarla una vez y tirarla",
    "cat": "lineal",
    "m": "Extraer, usar y descartar: el modelo lineal."
  },
  {
    "it": "Devolver el envase para que lo vuelvan a llenar",
    "cat": "circular",
    "m": "El material vuelve al circuito en vez de convertirse en residuo."
  },
  {
    "it": "Reparar el celular en vez de cambiarlo",
    "cat": "circular",
    "m": "Alargar la vida útil es una estrategia circular."
  },
  {
    "it": "Diseñar un producto para que dure poco a propósito",
    "cat": "lineal",
    "m": "La obsolescencia programada acelera el descarte."
  },
  {
    "it": "Compostar los restos de comida",
    "cat": "circular",
    "m": "La materia orgánica vuelve al suelo como nutriente."
  },
  {
    "it": "Enterrar toda la basura sin separar",
    "cat": "lineal",
    "m": "Todo termina como residuo, y además genera metano."
  },
  {
    "it": "Fabricar remeras con hilo de botellas recicladas",
    "cat": "circular",
    "m": "Un residuo se convierte en materia prima."
  },
  {
    "it": "Cambiar de electrodoméstico cada dos años porque sale más barato que arreglarlo",
    "cat": "lineal",
    "m": "El diseño que impide reparar empuja al modelo lineal."
  },
  {
    "it": "Donar la ropa que ya no usás",
    "cat": "circular",
    "m": "Extiende la vida útil de la prenda."
  },
  {
    "it": "Usar vasos descartables en una fiesta",
    "cat": "lineal",
    "m": "Un solo uso y al residuo."
  },
  {
    "it": "Recuperar metales de aparatos electrónicos viejos",
    "cat": "circular",
    "m": "Evita extraer material nuevo de la naturaleza."
  },
  {
    "it": "Verter efluentes industriales sin tratar al río",
    "cat": "lineal",
    "m": "Es el tipo de práctica que contaminó la cuenca Matanza-Riachuelo."
  },
  {
    "it": "Tratar los efluentes antes de devolver el agua al río",
    "cat": "circular",
    "m": "El agua vuelve al ciclo en condiciones de ser reutilizada."
  },
  {
    "it": "Comprar a granel con envase propio",
    "cat": "circular",
    "m": "Evita generar un envase nuevo en cada compra."
  },
  {
    "it": "Reemplazar el teléfono porque salió un modelo nuevo",
    "cat": "lineal",
    "m": "El descarte no responde a una falla sino al recambio."
  },
  {
    "it": "Recuperar la ribera del Riachuelo y sanear la cuenca",
    "cat": "circular",
    "m": "Restaurar el ambiente para que vuelva a cumplir sus funciones."
  }
];
GAMES.economia_circular_6 = juegoClasificar(CUR_ECONOMIA_CIRCULAR_6_BANCO, "¿Es economía lineal o circular?", [{"cat": "lineal", "label": "➡️ Lineal"}, {"cat": "circular", "label": "🔄 Circular"}], "economia_c");

/* 7° · Potencias y raíces — potencias_7
   DC: Potenciación y raíz cuadrada; reversibilidad entre las dos
   Fuente: docs/auditoria-dc-caba/grado-7.md · M1 */
const CUR_POTENCIAS_7_PLANTILLA = {
  "q": "¿Cuánto es {a} al cuadrado?",
  "vars": {
    "a": {
      "rango": [
        2,
        30
      ],
      "paso": 1
    }
  },
  "ok": "a * a",
  "distractores": [
    "a * 2",
    "a * a - a",
    "a * a + a"
  ],
  "tope": 1000,
  "m": "Al cuadrado es {a} × {a} = {ok}. Multiplicar por 2 da otra cosa: el exponente dice cuántas VECES se repite el número como factor."
};
GAMES.potencias_7 = juegoParametrico(CUR_POTENCIAS_7_PLANTILLA, "Calculá la potencia.", "potencias_");

/* 7° · Expresión objetivo — expresion_objetivo_7
   DC: Cálculos combinados; jerarquía; propiedades de las operaciones
   Fuente: docs/auditoria-dc-caba/grado-7.md · M4 */
const CUR_EXPRESION_OBJETIVO_7_PLANTILLA = {
  "q": "({a} + {b}) × {c}",
  "vars": {
    "a": {
      "rango": [
        2,
        40
      ],
      "paso": 1
    },
    "b": {
      "rango": [
        2,
        40
      ],
      "paso": 1
    },
    "c": {
      "rango": [
        2,
        12
      ],
      "paso": 1
    }
  },
  "ok": "(a + b) * c",
  "distractores": [
    "a + b * c",
    "a + b + c",
    "a * b * c"
  ],
  "tope": 1000,
  "m": "El paréntesis manda: primero {a} + {b}, y ese resultado por {c}. Da {ok}. Sin el paréntesis la multiplicación iría primero y daría otra cosa."
};
GAMES.expresion_objetivo_7 = juegoParametrico(CUR_EXPRESION_OBJETIVO_7_PLANTILLA, "Resolvé respetando el paréntesis.", "expresion_");

/* 7° · Problemas de varios pasos — problemas_pasos_7
   DC: Problemas de varios pasos; tratamiento de la información del enunciado
   Fuente: docs/auditoria-dc-caba/grado-7.md · M5b */
const CUR_PROBLEMAS_PASOS_7_PLANTILLA = {
  "q": "Una librería compra {b} cajas de {a} cuadernos. Si vende {c} cuadernos, ¿cuántos le quedan?",
  "vars": {
    "a": {
      "rango": [
        10,
        60
      ],
      "paso": 1
    },
    "b": {
      "opciones": [
        3,
        4,
        5,
        6,
        8
      ]
    },
    "c": {
      "rango": [
        12,
        90
      ],
      "paso": 1
    }
  },
  "ok": "a * b - c",
  "distractores": [
    "a * b",
    "a * b + c",
    "a + b - c"
  ],
  "tope": 500,
  "m": "Dos pasos: primero cuántos entraron ({a} × {b}) y recién después restás los {c} vendidos. Da {ok}. Contestar el total es el error más común."
};
GAMES.problemas_pasos_7 = juegoParametrico(CUR_PROBLEMAS_PASOS_7_PLANTILLA, "Leé el enunciado y resolvé.", "problemas_");

/* 7° · Razón y porcentaje — razon_porcentaje_7
   DC: Razón; uso de los racionales para expresar porcentajes
   Fuente: docs/auditoria-dc-caba/grado-7.md · M8 */
const CUR_RAZON_PORCENTAJE_7_PLANTILLA = {
  "q": "En un club de {a} chicos, el {p}% juega al fútbol. ¿Cuántos son?",
  "vars": {
    "a": {
      "rango": [
        10,
        150
      ],
      "paso": 10
    },
    "p": {
      "opciones": [
        10,
        20,
        50
      ]
    }
  },
  "ok": "a * p / 100",
  "distractores": [
    "a * p / 10",
    "a - a * p / 100",
    "a + p"
  ],
  "tope": 2000,
  "m": "El {p}% son {p} de cada 100: {a} × {p} ÷ 100 = {ok}. Ojo con correr mal la coma y con contestar los que NO juegan."
};
GAMES.razon_porcentaje_7 = juegoParametrico(CUR_RAZON_PORCENTAJE_7_PLANTILLA, "¿Cuántos son?", "razon_porc");

/* 7° · Proporcionalidad inversa — proporcionalidad_inversa_7
   DC: Proporcionalidad inversa; distinguirla de la directa
   Fuente: docs/auditoria-dc-caba/grado-7.md · M10 */
const CUR_PROPORCIONALIDAD_INVERSA_7_PLANTILLA = {
  "q": "Un trabajo lleva {a} días-persona. Si lo hacen {b} personas, ¿cuántos días tardan?",
  "vars": {
    "a": {
      "rango": [
        12,
        96
      ],
      "paso": 12
    },
    "b": {
      "opciones": [
        2,
        3,
        4,
        6
      ]
    }
  },
  "ok": "a / b",
  "distractores": [
    "a * b",
    "a - b",
    "a / 2"
  ],
  "tope": 200,
  "m": "Si son más personas, tardan MENOS: hay que dividir. {a} ÷ {b} = {ok} días. Multiplicar sería tratarla como proporcionalidad directa."
};
GAMES.proporcionalidad_inversa_7 = juegoParametrico(CUR_PROPORCIONALIDAD_INVERSA_7_PLANTILLA, "Más gente, menos días.", "proporcion");

/* 7° · Áreas del paralelogramo — areas_7
   DC: Área de paralelogramo, trapecio y romboide; perímetro y área del círculo
   Fuente: docs/auditoria-dc-caba/grado-7.md · M11 */
const CUR_AREAS_7_PLANTILLA = {
  "q": "Un paralelogramo tiene base {a} cm y altura {b} cm. ¿Cuál es su área?",
  "vars": {
    "a": {
      "rango": [
        3,
        24
      ],
      "paso": 1
    },
    "b": {
      "rango": [
        2,
        18
      ],
      "paso": 1
    }
  },
  "ok": "a * b",
  "distractores": [
    "2 * (a + b)",
    "a * b / 2",
    "a + b"
  ],
  "tope": 600,
  "m": "Área es base × altura: {a} × {b} = {ok} cm². Sumar los lados da el perímetro, y dividir por 2 da el triángulo."
};
GAMES.areas_7 = juegoParametrico(CUR_AREAS_7_PLANTILLA, "Calculá el área.", "areas_7");

/* 7° · Número y sistema de numeración — numeracion_7
   DC: Valor posicional, descomposición polinómica y sistema sexagesimal
   Fuente: docs/auditoria-dc-caba/grado-7.md · M0 */
const CUR_NUMERACION_7_BANCO = [
  {
    "q": "En 4.708, ¿cuánto vale el 7?",
    "ops": [
      "700",
      "70",
      "7"
    ],
    "m": "Está en el lugar de las centenas: vale 7 × 100."
  },
  {
    "q": "En 25.031, ¿cuánto vale el 5?",
    "ops": [
      "5.000",
      "500",
      "50"
    ],
    "m": "Ocupa el lugar de las unidades de mil."
  },
  {
    "q": "¿Cómo se descompone 3.406?",
    "ops": [
      "3×1.000 + 4×100 + 0×10 + 6",
      "3×100 + 4×10 + 6",
      "34×100 + 6"
    ],
    "m": "Cada cifra se multiplica por la potencia de 10 de su lugar."
  },
  {
    "q": "¿Cuál es la descomposición polinómica de 250?",
    "ops": [
      "2×10² + 5×10¹ + 0",
      "2×10 + 5",
      "25×10"
    ],
    "m": "Polinómica quiere decir con potencias de 10, no cualquier forma de escribirlo."
  },
  {
    "q": "¿Cuántos minutos hay en 2 horas y 15 minutos?",
    "ops": [
      "135",
      "215",
      "75"
    ],
    "m": "Cada hora son 60 minutos: 2 × 60 + 15. El sistema sexagesimal no es decimal."
  },
  {
    "q": "¿Cuántos segundos hay en 3 minutos?",
    "ops": [
      "180",
      "300",
      "30"
    ],
    "m": "Cada minuto tiene 60 segundos, no 100."
  },
  {
    "q": "¿Cuánto es 90 minutos en horas y minutos?",
    "ops": [
      "1 hora y 30 minutos",
      "9 horas",
      "1 hora y 9 minutos"
    ],
    "m": "60 forman una hora y sobran 30."
  },
  {
    "q": "En el número 8.888, ¿las cuatro cifras valen lo mismo?",
    "ops": [
      "No: valen 8.000, 800, 80 y 8",
      "Sí, todas valen 8",
      "Sí, porque son iguales"
    ],
    "m": "Ésa es la idea de valor posicional: la misma cifra vale distinto según el lugar."
  },
  {
    "q": "¿Cuál es mayor: 10² o 2¹⁰?",
    "ops": [
      "2¹⁰, que es 1.024",
      "10², que es 100",
      "Son iguales"
    ],
    "m": "10² = 100 y 2¹⁰ = 1.024. El exponente pesa más de lo que parece."
  },
  {
    "q": "¿Cuánto es 10⁴?",
    "ops": [
      "10.000",
      "40",
      "1.000"
    ],
    "m": "El exponente cuenta los ceros: 10⁴ es un 1 con cuatro ceros."
  },
  {
    "q": "¿Cuántos grados tiene un ángulo de 1 hora en un reloj analógico?",
    "ops": [
      "30°",
      "60°",
      "12°"
    ],
    "m": "360° repartidos en 12 horas: 360 ÷ 12."
  },
  {
    "q": "¿Cuánto es 1 hora y 45 minutos en minutos?",
    "ops": [
      "105",
      "145",
      "60"
    ],
    "m": "60 + 45. Pegar los números como si fuera decimal es el error clásico."
  },
  {
    "q": "¿Qué representa el 0 en el número 507?",
    "ops": [
      "Que no hay decenas",
      "Que el número vale menos",
      "Nada, se puede sacar"
    ],
    "m": "Sacarlo daría 57: el cero guarda el lugar."
  },
  {
    "q": "¿Cuál de estos números es mayor?",
    "ops": [
      "1.000.000",
      "999.999",
      "100.000"
    ],
    "m": "Contá las cifras primero: siete gana contra seis."
  },
  {
    "q": "¿Cuántas horas son 210 minutos?",
    "ops": [
      "3 horas y 30 minutos",
      "2 horas y 10 minutos",
      "21 horas"
    ],
    "m": "210 ÷ 60 da 3 y sobran 30."
  },
  {
    "q": "En 7,25 ¿cuánto vale el 2?",
    "ops": [
      "2 décimos",
      "2 centésimos",
      "2 unidades"
    ],
    "m": "El primer lugar después de la coma son los décimos."
  }
];
GAMES.numeracion_7 = juegoTriviaTexto(CUR_NUMERACION_7_BANCO, "Pensá cuánto vale cada cifra.", "numeracion");

/* 7° · Tribunal de divisibilidad — divisibilidad_7
   DC: Criterios de divisibilidad por 3, 4, 6, 8 y 9
   Fuente: docs/auditoria-dc-caba/grado-7.md · M2 */
const CUR_DIVISIBILIDAD_7_BANCO = [
  {
    "q": "¿Cuál es el criterio de divisibilidad por 3?",
    "ops": [
      "Que la suma de sus cifras sea múltiplo de 3",
      "Que termine en 3",
      "Que sea impar"
    ],
    "m": "Terminar en 3 no dice nada: 13 no es múltiplo de 3."
  },
  {
    "q": "¿Es 234 divisible por 3?",
    "ops": [
      "Sí: 2+3+4 = 9",
      "No",
      "Sólo por 2"
    ],
    "m": "9 es múltiplo de 3, así que 234 también lo es."
  },
  {
    "q": "¿Cuál es el criterio por 9?",
    "ops": [
      "Que la suma de sus cifras sea múltiplo de 9",
      "Que termine en 9",
      "Que sea múltiplo de 3 y de 6"
    ],
    "m": "Es el mismo mecanismo que el de 3, pero exigiendo múltiplo de 9."
  },
  {
    "q": "¿Es 4.518 divisible por 9?",
    "ops": [
      "Sí: 4+5+1+8 = 18",
      "No",
      "Sólo por 3"
    ],
    "m": "18 es múltiplo de 9. Todo múltiplo de 9 es además múltiplo de 3."
  },
  {
    "q": "¿Cuál es el criterio por 4?",
    "ops": [
      "Que las dos últimas cifras formen un múltiplo de 4",
      "Que sea par",
      "Que termine en 4"
    ],
    "m": "Ser par no alcanza: 14 es par y no es múltiplo de 4."
  },
  {
    "q": "¿Es 1.316 divisible por 4?",
    "ops": [
      "Sí: 16 es múltiplo de 4",
      "No",
      "Sólo por 2"
    ],
    "m": "Alcanza con mirar las dos últimas cifras."
  },
  {
    "q": "¿Cuál es el criterio por 6?",
    "ops": [
      "Que sea divisible por 2 Y por 3 a la vez",
      "Que termine en 6",
      "Que sea divisible por 3 solamente"
    ],
    "m": "6 = 2 × 3, así que tiene que cumplir los dos criterios."
  },
  {
    "q": "¿Es 132 divisible por 6?",
    "ops": [
      "Sí: es par y 1+3+2 = 6",
      "No",
      "Sólo por 2"
    ],
    "m": "Cumple los dos criterios a la vez."
  },
  {
    "q": "¿Es 246 divisible por 4?",
    "ops": [
      "No: 46 no es múltiplo de 4",
      "Sí, porque es par",
      "Sí, porque 2+4+6 = 12"
    ],
    "m": "La suma de cifras sirve para 3 y 9, no para 4."
  },
  {
    "q": "¿Cuál es el criterio por 8?",
    "ops": [
      "Que las tres últimas cifras formen un múltiplo de 8",
      "Que sea múltiplo de 4 y de 2",
      "Que termine en 8"
    ],
    "m": "Ser múltiplo de 4 no alcanza: 12 es múltiplo de 4 y no de 8."
  },
  {
    "q": "Si un número es divisible por 9, ¿es divisible por 3?",
    "ops": [
      "Sí, siempre",
      "No, nunca",
      "Sólo si es par"
    ],
    "m": "Todo múltiplo de 9 lo es de 3, porque 9 contiene al 3."
  },
  {
    "q": "Si un número es divisible por 3, ¿es divisible por 9?",
    "ops": [
      "No necesariamente",
      "Sí, siempre",
      "Sólo si es impar"
    ],
    "m": "12 es múltiplo de 3 y no de 9. La implicación va en un solo sentido."
  },
  {
    "q": "¿Es 720 divisible por 8?",
    "ops": [
      "Sí: 720 ÷ 8 = 90",
      "No",
      "Sólo por 4"
    ],
    "m": "Las tres últimas cifras son 720, que es múltiplo de 8."
  },
  {
    "q": "¿Por qué sirve conocer los criterios?",
    "ops": [
      "Para simplificar fracciones y factorizar sin hacer la división",
      "Para sumar más rápido",
      "Para escribir números grandes"
    ],
    "m": "Es la herramienta que hace rápida la simplificación."
  },
  {
    "q": "¿Es 555 divisible por 3?",
    "ops": [
      "Sí: 5+5+5 = 15",
      "No, es impar",
      "Sólo por 5"
    ],
    "m": "La paridad no tiene nada que ver con el criterio del 3."
  }
];
GAMES.divisibilidad_7 = juegoTriviaTexto(CUR_DIVISIBILIDAD_7_BANCO, "Aplicá el criterio, no dividas.", "divisibili");

/* 7° · Múltiplo y divisor común — mcm_dcm_7
   DC: Mínimo común múltiplo y divisor común mayor en problemas
   Fuente: docs/auditoria-dc-caba/grado-7.md · M3 */
const CUR_MCM_DCM_7_BANCO = [
  {
    "q": "¿Cuál es el mcm de 6 y 8?",
    "ops": [
      "24",
      "48",
      "2"
    ],
    "m": "48 también es múltiplo común, pero el MÍNIMO es 24. El 2 es el divisor."
  },
  {
    "q": "¿Cuál es el DCM de 12 y 18?",
    "ops": [
      "6",
      "36",
      "3"
    ],
    "m": "36 es el mcm. Entre los divisores comunes (1, 2, 3, 6) el mayor es 6."
  },
  {
    "q": "El mcm de dos números, ¿es mayor o menor que ellos?",
    "ops": [
      "Mayor o igual",
      "Siempre menor",
      "Siempre igual al más chico"
    ],
    "m": "Es un múltiplo, así que nunca puede ser más chico."
  },
  {
    "q": "El DCM de dos números, ¿es mayor o menor que ellos?",
    "ops": [
      "Menor o igual",
      "Siempre mayor",
      "Siempre 1"
    ],
    "m": "Es un divisor: nunca supera al más chico de los dos."
  },
  {
    "q": "Dos colectivos salen cada 12 y cada 18 minutos. ¿Cada cuánto coinciden?",
    "ops": [
      "Cada 36 minutos (mcm)",
      "Cada 6 minutos (DCM)",
      "Cada 30 minutos"
    ],
    "m": "«Coincidir» pide el momento común: eso es un múltiplo, no un divisor."
  },
  {
    "q": "Quiero cortar cintas de 24 y 36 cm en trozos iguales lo más largos posible. ¿Cuánto miden?",
    "ops": [
      "12 cm (DCM)",
      "72 cm (mcm)",
      "6 cm"
    ],
    "m": "«Repartir en partes iguales lo más grandes posible» pide el divisor común mayor."
  },
  {
    "q": "¿Cuál es el mcm de 4 y 5?",
    "ops": [
      "20",
      "9",
      "1"
    ],
    "m": "Como no comparten factores, el mcm es el producto."
  },
  {
    "q": "¿Cuál es el DCM de 7 y 9?",
    "ops": [
      "1",
      "63",
      "7"
    ],
    "m": "No comparten ningún factor: se llaman coprimos y su DCM es 1."
  },
  {
    "q": "¿Cuál es el mcm de 3 y 12?",
    "ops": [
      "12",
      "36",
      "3"
    ],
    "m": "Cuando uno es múltiplo del otro, el mcm es el mayor."
  },
  {
    "q": "¿Cuál es el DCM de 5 y 20?",
    "ops": [
      "5",
      "20",
      "1"
    ],
    "m": "Cuando uno divide al otro, el DCM es el menor."
  },
  {
    "q": "¿Para qué sirve el mcm al sumar fracciones?",
    "ops": [
      "Para encontrar el denominador común más chico",
      "Para simplificar",
      "Para invertir la fracción"
    ],
    "m": "Simplificar usa el DCM; el común denominador usa el mcm."
  },
  {
    "q": "¿Para qué sirve el DCM al simplificar una fracción?",
    "ops": [
      "Para llevarla de una vez a su mínima expresión",
      "Para agrandarla",
      "Para sumarla"
    ],
    "m": "Dividiendo por el DCM llegás en un solo paso a la mínima expresión."
  },
  {
    "q": "¿Cuál es el mcm de 2, 3 y 4?",
    "ops": [
      "12",
      "24",
      "6"
    ],
    "m": "12 es múltiplo de los tres, y es el más chico que lo cumple."
  },
  {
    "q": "Dos luces parpadean cada 6 y cada 10 segundos. ¿Cada cuánto coinciden?",
    "ops": [
      "Cada 30 segundos",
      "Cada 60 segundos",
      "Cada 2 segundos"
    ],
    "m": "El mcm de 6 y 10 es 30; 60 también es común pero no es el mínimo."
  }
];
GAMES.mcm_dcm_7 = juegoTriviaTexto(CUR_MCM_DCM_7_BANCO, "¿Te piden un múltiplo o un divisor?", "mcm_dcm_7");

/* 7° · Multiplicar y dividir fracciones — multiplicar_fracciones_7
   DC: Multiplicación y división de fracciones; la fracción inversa
   Fuente: docs/auditoria-dc-caba/grado-7.md · M5 */
const CUR_MULTIPLICAR_FRACCIONES_7_BANCO = [
  {
    "q": "2/3 × 3/5 =",
    "ops": [
      "2/5",
      "5/8",
      "6/8"
    ],
    "m": "6/15, que simplificado es 2/5. Los denominadores se multiplican, no se suman."
  },
  {
    "q": "1/2 ÷ 1/4 =",
    "ops": [
      "2",
      "1/8",
      "1/2"
    ],
    "m": "Es 1/2 × 4/1 = 4/2 = 2. Preguntate cuántos cuartos entran en un medio."
  },
  {
    "q": "3/4 ÷ 1/2 =",
    "ops": [
      "3/2",
      "3/8",
      "1/2"
    ],
    "m": "3/4 × 2/1 = 6/4 = 3/2. Multiplicar en vez de invertir da 3/8."
  },
  {
    "q": "Para dividir por 2/5 hay que multiplicar por…",
    "ops": [
      "5/2",
      "2/5",
      "1/5"
    ],
    "m": "La inversa se obtiene dando vuelta los dos términos."
  },
  {
    "q": "1/3 × 6 =",
    "ops": [
      "2",
      "18",
      "1/18"
    ],
    "m": "6/3 = 2. Un tercio de seis."
  },
  {
    "q": "¿Dividir por 1/2 agranda o achica?",
    "ops": [
      "Agranda: da el doble",
      "Achica: da la mitad",
      "No cambia"
    ],
    "m": "Preguntate cuántas mitades entran: en 3 entran 6."
  },
  {
    "q": "5/6 × 2/5 =",
    "ops": [
      "1/3",
      "7/11",
      "10/11"
    ],
    "m": "10/30, que simplificado es 1/3."
  },
  {
    "q": "2 ÷ 1/4 =",
    "ops": [
      "8",
      "1/2",
      "2/4"
    ],
    "m": "¿Cuántos cuartos entran en 2? Ocho."
  },
  {
    "q": "¿Cuánto da 4/7 × 7/4?",
    "ops": [
      "1",
      "28/28 y algo",
      "8/11"
    ],
    "m": "Son inversas: el producto siempre es el entero."
  },
  {
    "q": "3/5 ÷ 3 =",
    "ops": [
      "1/5",
      "9/5",
      "3/15 y no se puede simplificar"
    ],
    "m": "3 es 3/1, así que se multiplica por 1/3: 3/15 = 1/5."
  },
  {
    "q": "¿Cómo se dividen dos fracciones?",
    "ops": [
      "Se multiplica por la inversa de la segunda",
      "Se dividen arriba y abajo",
      "Se busca denominador común"
    ],
    "m": "Dividir por 1/4 es multiplicar por 4: por eso se da vuelta la segunda."
  },
  {
    "q": "1/2 × 1/2 × 1/2 =",
    "ops": [
      "1/8",
      "3/6",
      "1/6"
    ],
    "m": "Cada mitad parte de nuevo: 2 × 2 × 2 = 8 partes."
  },
  {
    "q": "¿Cuál es la inversa de 1/6?",
    "ops": [
      "6",
      "1/6",
      "6/6"
    ],
    "m": "1/6 dado vuelta es 6/1, que es 6."
  },
  {
    "q": "6 ÷ 2/3 =",
    "ops": [
      "9",
      "4",
      "12/3 sin simplificar"
    ],
    "m": "6 × 3/2 = 18/2 = 9. En 6 entran nueve dos tercios."
  }
];
GAMES.multiplicar_fracciones_7 = juegoTriviaTexto(CUR_MULTIPLICAR_FRACCIONES_7_BANCO, "Para dividir, multiplicá por la inversa.", "multiplica");

/* 7° · Decimales y el período escondido — decimales_periodo_7
   DC: Multiplicación y división de decimales; expresiones periódicas
   Fuente: docs/auditoria-dc-caba/grado-7.md · M6 */
const CUR_DECIMALES_PERIODO_7_BANCO = [
  {
    "q": "1 ÷ 3 =",
    "ops": [
      "0,333… (periódica)",
      "0,3 exacto",
      "3"
    ],
    "m": "El 3 se repite para siempre: es una expresión periódica."
  },
  {
    "q": "3 ÷ 8 =",
    "ops": [
      "0,375 (exacta)",
      "0,38 periódica",
      "2,6"
    ],
    "m": "El denominador 8 sólo tiene factores 2: por eso la división corta."
  },
  {
    "q": "¿Qué es una expresión decimal periódica?",
    "ops": [
      "Una en la que un grupo de cifras se repite sin fin",
      "Una que tiene muchos decimales",
      "Una que termina en cero"
    ],
    "m": "Tener muchos decimales no alcanza: lo que define es la repetición."
  },
  {
    "q": "2 ÷ 3 =",
    "ops": [
      "0,666…",
      "0,66 exacto",
      "0,23"
    ],
    "m": "El 6 se repite indefinidamente."
  },
  {
    "q": "¿Cuál de estas es exacta?",
    "ops": [
      "3 ÷ 8",
      "1 ÷ 6",
      "5 ÷ 9"
    ],
    "m": "3 ÷ 8 = 0,375 y ahí termina. Las otras dos tienen período."
  },
  {
    "q": "1 ÷ 6 =",
    "ops": [
      "0,1666…",
      "0,16 exacto",
      "0,6"
    ],
    "m": "El 6 se repite después del 1: el período no siempre arranca al principio."
  },
  {
    "q": "0,4 × 0,5 =",
    "ops": [
      "0,2",
      "2",
      "0,9"
    ],
    "m": "Dos decimales en total, y multiplicar por menos de 1 achica."
  },
  {
    "q": "1,2 ÷ 0,4 =",
    "ops": [
      "3",
      "0,3",
      "4,8"
    ],
    "m": "¿Cuántas veces entra 0,4 en 1,2? Tres."
  },
  {
    "q": "¿Cuánto es 2,5 ÷ 100?",
    "ops": [
      "0,025",
      "0,25",
      "250"
    ],
    "m": "Dos lugares a la izquierda."
  },
  {
    "q": "¿Cuánto es 0,07 × 1.000?",
    "ops": [
      "70",
      "7",
      "700"
    ],
    "m": "Tres lugares a la derecha: 0,07 → 0,7 → 7 → 70."
  },
  {
    "q": "¿Toda fracción se puede escribir como decimal?",
    "ops": [
      "Sí, exacto o periódico",
      "No, algunas no se pueden",
      "Sólo las que dan exacto"
    ],
    "m": "Siempre pasa una de las dos cosas."
  },
  {
    "q": "¿Cuál es el período de 0,4545…?",
    "ops": [
      "45",
      "4",
      "0,45"
    ],
    "m": "El período es el grupo de cifras que se repite."
  },
  {
    "q": "1 ÷ 7 =",
    "ops": [
      "0,142857… (periódica)",
      "0,14 exacta",
      "7"
    ],
    "m": "El período de 1/7 tiene seis cifras que se repiten."
  },
  {
    "q": "0,3 × 0,3 =",
    "ops": [
      "0,09",
      "0,6",
      "0,9"
    ],
    "m": "Un decimal más un decimal dan dos decimales en el resultado."
  }
];
GAMES.decimales_periodo_7 = juegoTriviaTexto(CUR_DECIMALES_PERIODO_7_BANCO, "¿Se corta o se repite?", "decimales_");

/* 7° · Zoom infinito — densidad_7
   DC: Densidad de los racionales; orden con reglas distintas de los naturales
   Fuente: docs/auditoria-dc-caba/grado-7.md · M7 */
const CUR_DENSIDAD_7_BANCO = [
  {
    "q": "¿Qué número está entre 1/2 y 3/4?",
    "ops": [
      "5/8",
      "1/4",
      "4/4"
    ],
    "m": "A octavos: 4/8, 5/8 y 6/8. El 5/8 cae justo en el medio."
  },
  {
    "q": "¿Cuántos racionales hay entre 0 y 1?",
    "ops": [
      "Infinitos",
      "Cien",
      "Ninguno"
    ],
    "m": "Ésa es la propiedad de densidad."
  },
  {
    "q": "Entre 3 y 4, ¿hay algún NATURAL?",
    "ops": [
      "No, ninguno",
      "Sí, uno",
      "Infinitos"
    ],
    "m": "Los naturales son discretos: 3 y 4 son consecutivos. Los racionales no funcionan así."
  },
  {
    "q": "¿Cuál es MAYOR: 3/7 o 4/9?",
    "ops": [
      "4/9",
      "3/7",
      "Son iguales"
    ],
    "m": "A denominador 63: 27/63 contra 28/63. Gana 4/9 por poco."
  },
  {
    "q": "¿Cómo se busca un número entre dos fracciones?",
    "ops": [
      "Se las lleva a un denominador común más grande",
      "Se suman los numeradores",
      "Se restan"
    ],
    "m": "Ampliando aparecen lugares intermedios que antes no se veían."
  },
  {
    "q": "¿Qué número está entre 0,25 y 0,26?",
    "ops": [
      "0,255",
      "0,3",
      "0,2"
    ],
    "m": "Agregando un decimal más siempre aparece uno en el medio."
  },
  {
    "q": "¿Cuál es MENOR: 5/8 o 2/3?",
    "ops": [
      "5/8",
      "2/3",
      "Son iguales"
    ],
    "m": "A denominador 24: 15/24 contra 16/24."
  },
  {
    "q": "Con los naturales, ¿cuál sigue después del 7?",
    "ops": [
      "El 8",
      "El 7,5",
      "Hay infinitos"
    ],
    "m": "Entre naturales hay un siguiente; entre racionales no existe «el siguiente»."
  },
  {
    "q": "¿Cuál es MAYOR: 0,8 o 4/5?",
    "ops": [
      "Son iguales",
      "0,8",
      "4/5"
    ],
    "m": "4/5 es exactamente 0,8: son dos escrituras del mismo número."
  },
  {
    "q": "¿Qué fracción está entre 1/3 y 1/2?",
    "ops": [
      "5/12",
      "1/4",
      "2/3"
    ],
    "m": "A doceavos: 4/12 y 6/12; el 5/12 queda justo en el medio."
  },
  {
    "q": "¿Un número con más cifras decimales es siempre mayor?",
    "ops": [
      "No: 0,25 es menor que 0,3",
      "Sí, siempre",
      "Sólo si empieza con 0"
    ],
    "m": "Hay que comparar lugar por lugar desde la izquierda."
  },
  {
    "q": "¿Cuántos números hay entre 0,999 y 1?",
    "ops": [
      "Infinitos",
      "Uno",
      "Ninguno"
    ],
    "m": "Aunque parezcan pegados, siempre se puede agregar un decimal más."
  },
  {
    "q": "Ordenados de menor a mayor: 2/5 · 1/2 · 3/8",
    "ops": [
      "3/8 · 2/5 · 1/2",
      "2/5 · 3/8 · 1/2",
      "1/2 · 2/5 · 3/8"
    ],
    "m": "A cuarentavos: 15/40, 16/40 y 20/40."
  },
  {
    "q": "¿Cuál está entre 2 y 2,1?",
    "ops": [
      "2,05",
      "2,5",
      "1,95"
    ],
    "m": "Hay que mirar el segundo decimal."
  }
];
GAMES.densidad_7 = juegoTriviaTexto(CUR_DENSIDAD_7_BANCO, "Siempre entra otro en el medio.", "densidad_7");

/* 7° · Proporcionalidad en el plano — proporcionalidad_grafico_7
   DC: Representación cartesiana de la proporcionalidad directa
   Fuente: docs/auditoria-dc-caba/grado-7.md · M9 */
const CUR_PROPORCIONALIDAD_GRAFICO_7_BANCO = [
  {
    "q": "¿Cómo se ve en el plano una proporcionalidad directa?",
    "ops": [
      "Una recta que pasa por el origen",
      "Una curva",
      "Una recta que corta el eje arriba del cero"
    ],
    "m": "Si no pasa por el (0,0), hay un valor fijo de arranque y ya no es proporcional."
  },
  {
    "q": "Si 1 kg cuesta $500, ¿cuánto cuestan 4 kg?",
    "ops": [
      "$2.000",
      "$504",
      "$125"
    ],
    "m": "La constante es 500: se multiplica."
  },
  {
    "q": "¿Qué es la constante de proporcionalidad?",
    "ops": [
      "El número por el que se multiplica siempre",
      "El punto de partida",
      "El valor más alto de la tabla"
    ],
    "m": "Es lo que se mantiene al dividir cada par de valores."
  },
  {
    "q": "En una tabla proporcional, si divido cada y por su x, ¿qué obtengo?",
    "ops": [
      "Siempre el mismo número",
      "Números distintos",
      "Cero"
    ],
    "m": "Ése es el test para saber si una tabla es proporcional."
  },
  {
    "q": "Un remís cobra $1.000 de bajada más $200 por km. ¿Es proporcional?",
    "ops": [
      "No: hay un costo fijo de arranque",
      "Sí, siempre",
      "Sí, porque crece"
    ],
    "m": "Con 0 km ya se pagan $1.000, así que la recta no pasa por el origen."
  },
  {
    "q": "¿Qué eje suele llevar la variable que uno elige?",
    "ops": [
      "El horizontal (x)",
      "El vertical (y)",
      "Cualquiera"
    ],
    "m": "En y va la que depende de la otra."
  },
  {
    "q": "Si 3 lápices cuestan $600, ¿cuál es la constante?",
    "ops": [
      "200",
      "600",
      "3"
    ],
    "m": "Es el precio de UNO: 600 ÷ 3."
  },
  {
    "q": "Una tabla da (2, 6), (4, 12) y (5, 16). ¿Es proporcional?",
    "ops": [
      "No: 16 ÷ 5 no da 3",
      "Sí, siempre crece",
      "Sí, porque los dos suben"
    ],
    "m": "Crecer no alcanza: el cociente tiene que ser SIEMPRE el mismo."
  },
  {
    "q": "Una tabla da (1, 4), (3, 12) y (5, 20). ¿Es proporcional?",
    "ops": [
      "Sí: la constante es 4",
      "No",
      "Sólo en los dos primeros pares"
    ],
    "m": "4 ÷ 1, 12 ÷ 3 y 20 ÷ 5 dan todos 4."
  },
  {
    "q": "En una proporcionalidad, si x se duplica, ¿qué pasa con y?",
    "ops": [
      "Se duplica",
      "Se mantiene",
      "Se reduce a la mitad"
    ],
    "m": "Reducirse a la mitad sería una proporcionalidad inversa."
  },
  {
    "q": "¿Qué punto siempre pertenece a una proporcionalidad directa?",
    "ops": [
      "El (0, 0)",
      "El (1, 1)",
      "El (0, 1)"
    ],
    "m": "Si no hay cantidad, no hay costo: por eso arranca en el origen."
  },
  {
    "q": "Un gráfico de proporcionalidad inversa se ve como…",
    "ops": [
      "Una curva que baja y nunca toca los ejes",
      "Una recta por el origen",
      "Una línea horizontal"
    ],
    "m": "El producto se mantiene constante, así que la curva se acerca a los ejes sin tocarlos."
  },
  {
    "q": "Si la constante es 2,5 y x vale 6, ¿cuánto vale y?",
    "ops": [
      "15",
      "8,5",
      "2,4"
    ],
    "m": "y = constante × x."
  }
];
GAMES.proporcionalidad_grafico_7 = juegoTriviaTexto(CUR_PROPORCIONALIDAD_GRAFICO_7_BANCO, "Mirá si pasa por el origen.", "proporcion");

/* 7° · ¿Moda, mediana o media? — media_mediana_moda_7
   DC: Moda, mediana y media; cuál es pertinente según la situación
   Fuente: docs/auditoria-dc-caba/grado-7.md · M12 */
const CUR_MEDIA_MEDIANA_MODA_7_BANCO = [
  {
    "q": "¿Cuál es la media de 2, 4, 6 y 8?",
    "ops": [
      "5",
      "6",
      "4"
    ],
    "m": "Se suman (20) y se divide por la cantidad (4)."
  },
  {
    "q": "¿Cuál es la mediana de 3, 5, 7, 9 y 11?",
    "ops": [
      "7",
      "5",
      "35"
    ],
    "m": "Ordenados, es el valor del medio."
  },
  {
    "q": "¿Cuál es la moda de 4, 4, 5, 7 y 9?",
    "ops": [
      "4",
      "5",
      "9"
    ],
    "m": "Es el que más se repite, no el más grande ni el del medio."
  },
  {
    "q": "Sueldos de 1.000, 1.100, 1.200 y 20.000. ¿Qué medida representa mejor?",
    "ops": [
      "La mediana, porque el 20.000 desvía la media",
      "La media, siempre es la mejor",
      "La moda"
    ],
    "m": "La media daría 5.825, un número que no describe a casi nadie del grupo."
  },
  {
    "q": "¿Cómo se calcula la mediana con una cantidad PAR de datos?",
    "ops": [
      "Es el promedio de los dos del medio",
      "Es el mayor de los dos del medio",
      "No se puede calcular"
    ],
    "m": "Con cantidad par no hay un único valor central."
  },
  {
    "q": "¿Cuál es la mediana de 2, 4, 6 y 10?",
    "ops": [
      "5",
      "6",
      "4"
    ],
    "m": "Los del medio son 4 y 6: su promedio es 5."
  },
  {
    "q": "¿Qué medida usarías para saber el talle de calzado más vendido?",
    "ops": [
      "La moda",
      "La media",
      "La mediana"
    ],
    "m": "Un talle promedio de 39,4 no existe como producto."
  },
  {
    "q": "¿Qué es un valor atípico o extremo?",
    "ops": [
      "Un dato muy alejado del resto",
      "El dato que más se repite",
      "El del medio"
    ],
    "m": "Es el que puede distorsionar la media."
  },
  {
    "q": "¿Cuál es la media de 10, 10, 10 y 30?",
    "ops": [
      "15",
      "10",
      "30"
    ],
    "m": "60 ÷ 4 = 15, aunque tres de los cuatro datos valgan 10."
  },
  {
    "q": "En ese mismo grupo (10, 10, 10 y 30), ¿cuál es la mediana?",
    "ops": [
      "10",
      "15",
      "20"
    ],
    "m": "Los dos del medio son 10 y 10: la mediana resiste al extremo."
  },
  {
    "q": "¿Puede una distribución tener más de una moda?",
    "ops": [
      "Sí, si hay empate en cantidad de apariciones",
      "No, nunca",
      "Sólo si hay 3 datos"
    ],
    "m": "Se la llama bimodal cuando hay dos."
  },
  {
    "q": "¿Qué medida NO cambia si le agrego un dato altísimo?",
    "ops": [
      "La moda, casi siempre",
      "La media",
      "El total"
    ],
    "m": "La media es la más sensible a los extremos."
  },
  {
    "q": "¿Cuál es la media de 5, 5, 5 y 5?",
    "ops": [
      "5",
      "20",
      "0"
    ],
    "m": "Si todos los datos son iguales, la media es ese valor."
  },
  {
    "q": "Para informar «el argentino promedio», ¿qué se usa?",
    "ops": [
      "Depende: con datos muy dispares conviene la mediana",
      "Siempre la media",
      "Siempre la moda"
    ],
    "m": "Elegir la medida pertinente ES el contenido del tema."
  }
];
GAMES.media_mediana_moda_7 = juegoTriviaTexto(CUR_MEDIA_MEDIANA_MODA_7_BANCO, "Elegí la medida que mejor representa.", "media_medi");

/* 7° · Árbol de la probabilidad — probabilidad_arbol_7
   DC: Diagramas de árbol; equiprobabilidad; casos favorables y posibles
   Fuente: docs/auditoria-dc-caba/grado-7.md · M13 */
const CUR_PROBABILIDAD_ARBOL_7_BANCO = [
  {
    "q": "Al tirar dos monedas, ¿cuántos resultados posibles hay?",
    "ops": [
      "Cuatro",
      "Tres",
      "Dos"
    ],
    "m": "Cara-cara, cara-ceca, ceca-cara y ceca-ceca. Las dos del medio son distintas."
  },
  {
    "q": "¿Cuál es la probabilidad de sacar dos caras con dos monedas?",
    "ops": [
      "1 de 4",
      "1 de 2",
      "1 de 3"
    ],
    "m": "Un caso favorable sobre cuatro posibles."
  },
  {
    "q": "Al tirar un dado, ¿cuál es la probabilidad de sacar par?",
    "ops": [
      "3 de 6",
      "2 de 6",
      "1 de 6"
    ],
    "m": "Los favorables son 2, 4 y 6."
  },
  {
    "q": "¿Qué significa que dos resultados sean equiprobables?",
    "ops": [
      "Que tienen la misma chance",
      "Que son seguros",
      "Que son imposibles"
    ],
    "m": "En un dado no cargado, las seis caras lo son."
  },
  {
    "q": "Al tirar dos dados, ¿cuántos resultados posibles hay?",
    "ops": [
      "36",
      "12",
      "6"
    ],
    "m": "Seis del primero por seis del segundo."
  },
  {
    "q": "Al tirar dos dados, ¿qué suma es la MÁS probable?",
    "ops": [
      "7",
      "2",
      "12"
    ],
    "m": "El 7 se puede armar de seis maneras; el 2 y el 12, de una sola cada uno."
  },
  {
    "q": "¿Para qué sirve un diagrama de árbol?",
    "ops": [
      "Para listar ordenadamente todos los casos posibles",
      "Para calcular la media",
      "Para ordenar de mayor a menor"
    ],
    "m": "Cada rama es una posibilidad y ninguna se pierde."
  },
  {
    "q": "¿Cuál es la probabilidad de un suceso imposible?",
    "ops": [
      "0",
      "1",
      "1/2"
    ],
    "m": "Cero casos favorables sobre los posibles."
  },
  {
    "q": "¿Cuál es la probabilidad de un suceso seguro?",
    "ops": [
      "1",
      "0",
      "100"
    ],
    "m": "Todos los casos posibles son favorables: la razón da 1, o sea el 100%."
  },
  {
    "q": "Si tiro una moneda 5 veces y sale cara las 5, ¿qué chance tiene la sexta?",
    "ops": [
      "La misma: 1 de 2",
      "Más chance de ceca",
      "Más chance de cara"
    ],
    "m": "La moneda no tiene memoria. Ésta es la falacia del jugador."
  },
  {
    "q": "En una bolsa con 3 rojas y 7 azules, ¿qué probabilidad hay de sacar roja?",
    "ops": [
      "3 de 10",
      "3 de 7",
      "1 de 3"
    ],
    "m": "Favorables sobre el TOTAL, no sobre las otras."
  },
  {
    "q": "¿Puede una probabilidad ser mayor que 1?",
    "ops": [
      "No, nunca",
      "Sí, si hay muchos casos",
      "Sí, si el suceso es seguro"
    ],
    "m": "Los favorables nunca superan a los posibles."
  },
  {
    "q": "Con tres monedas, ¿cuántos resultados posibles hay?",
    "ops": [
      "8",
      "6",
      "3"
    ],
    "m": "2 × 2 × 2: cada moneda duplica las ramas del árbol."
  },
  {
    "q": "¿Cuál es la probabilidad de sacar un número mayor que 4 en un dado?",
    "ops": [
      "2 de 6",
      "3 de 6",
      "4 de 6"
    ],
    "m": "Sólo el 5 y el 6. El 4 no cuenta porque pide MAYOR que 4."
  }
];
GAMES.probabilidad_arbol_7 = juegoTriviaTexto(CUR_PROBABILIDAD_ARBOL_7_BANCO, "Contá los casos favorables y los posibles.", "probabilid");

/* 7° · Traductor algebraico — traductor_algebraico_7
   DC: Expresiones con y sin letras; traducir un enunciado a una expresión
   Fuente: docs/auditoria-dc-caba/grado-7.md · M14 */
const CUR_TRADUCTOR_ALGEBRAICO_7_BANCO = [
  {
    "q": "«El doble de un número» se escribe…",
    "ops": [
      "2x",
      "x²",
      "x+2"
    ],
    "m": "x² es el cuadrado y x+2 es «dos más»."
  },
  {
    "q": "«El doble de un número aumentado en 1» se escribe…",
    "ops": [
      "2(x+1)",
      "2x+1",
      "2x−1"
    ],
    "m": "Primero se aumenta y DESPUÉS se duplica: por eso va el paréntesis."
  },
  {
    "q": "«El doble de un número, aumentado en 1» se escribe…",
    "ops": [
      "2x+1",
      "2(x+1)",
      "x+2"
    ],
    "m": "Acá la coma cambia el orden: primero el doble, después el +1."
  },
  {
    "q": "«La mitad de un número» se escribe…",
    "ops": [
      "x/2",
      "2x",
      "x−2"
    ],
    "m": "Dividir por 2 es tomar la mitad."
  },
  {
    "q": "«La mitad de la suma de un número y 2» se escribe…",
    "ops": [
      "(x+2)/2",
      "x/2+2",
      "x+2/2"
    ],
    "m": "Se suma primero, y todo eso se divide."
  },
  {
    "q": "«El cuadrado de un número» se escribe…",
    "ops": [
      "x²",
      "2x",
      "√x"
    ],
    "m": "2x es el doble; la raíz es la operación inversa."
  },
  {
    "q": "«Un número disminuido en 5» se escribe…",
    "ops": [
      "x−5",
      "5−x",
      "x/5"
    ],
    "m": "El orden importa: 5−x sería «5 disminuido en el número»."
  },
  {
    "q": "«El triple de un número menos 4» se escribe…",
    "ops": [
      "3x−4",
      "3(x−4)",
      "x−12"
    ],
    "m": "Sin paréntesis, el triple se aplica sólo al número."
  },
  {
    "q": "«El siguiente de un número» se escribe…",
    "ops": [
      "x+1",
      "x−1",
      "2x"
    ],
    "m": "El anterior sería x−1."
  },
  {
    "q": "«La suma de dos números consecutivos» se escribe…",
    "ops": [
      "x + (x+1)",
      "2x",
      "x + 2"
    ],
    "m": "El consecutivo de x es x+1."
  },
  {
    "q": "Si x = 5, ¿cuánto vale 2(x+3)?",
    "ops": [
      "16",
      "13",
      "10"
    ],
    "m": "Primero el paréntesis: 5+3 = 8, y 8 × 2 = 16."
  },
  {
    "q": "Si x = 5, ¿cuánto vale 2x+3?",
    "ops": [
      "13",
      "16",
      "10"
    ],
    "m": "Acá el 2 multiplica sólo a x: 10+3."
  },
  {
    "q": "«El área de un cuadrado de lado L» se escribe…",
    "ops": [
      "L²",
      "4L",
      "2L"
    ],
    "m": "4L sería el perímetro."
  },
  {
    "q": "«Un número par cualquiera» se escribe…",
    "ops": [
      "2n",
      "n+2",
      "n²"
    ],
    "m": "Todo par es el doble de algún entero."
  }
];
GAMES.traductor_algebraico_7 = juegoTriviaTexto(CUR_TRADUCTOR_ALGEBRAICO_7_BANCO, "Pasá la frase a una expresión.", "traductor_");

/* 7° · ¿Fantástico, maravilloso o terror? — subgeneros_7
   DC: Los subgéneros narrativos como clave de lectura
   Fuente: docs/auditoria-dc-caba/grado-7.md · L1 */
const CUR_SUBGENEROS_7_BANCO = [
  {
    "it": "Una puerta común aparece de golpe donde antes había una pared, y nadie entiende por qué",
    "cat": "fantastico",
    "m": "Lo insólito irrumpe en un mundo normal y queda sin explicación."
  },
  {
    "it": "En el reino, las hadas conceden deseos desde hace siglos",
    "cat": "maravilloso",
    "m": "La magia es parte de las reglas de ese mundo: nadie se asombra."
  },
  {
    "it": "Los pasos se acercan por el pasillo oscuro y ella contiene la respiración",
    "cat": "terror",
    "m": "El objetivo del texto es producir miedo."
  },
  {
    "it": "El protagonista descubre que su reflejo se mueve un segundo tarde",
    "cat": "fantastico",
    "m": "Un hecho imposible dentro de una vida cotidiana."
  },
  {
    "it": "El príncipe consulta al dragón, que como todos los dragones habla",
    "cat": "maravilloso",
    "m": "El dragón parlante es normal en ese mundo."
  },
  {
    "it": "La casa lleva años vacía y sin embargo alguien enciende la luz del sótano",
    "cat": "terror",
    "m": "Construye tensión y amenaza."
  },
  {
    "it": "Recibe una carta escrita por él mismo, fechada la semana que viene",
    "cat": "fantastico",
    "m": "Lo imposible ocurre en un mundo por lo demás normal."
  },
  {
    "it": "La bruja del bosque prepara pociones desde antes de que naciera la abuela",
    "cat": "maravilloso",
    "m": "El mundo entero funciona con magia."
  },
  {
    "it": "Cada noche a las tres se escuchan uñas rascando la puerta",
    "cat": "terror",
    "m": "Todo el relato está armado para asustar."
  },
  {
    "it": "El hombre empieza a olvidar palabras, y las palabras desaparecen del diccionario",
    "cat": "fantastico",
    "m": "La irrupción de lo inexplicable en lo cotidiano."
  },
  {
    "it": "El caballero recibe la espada encantada de manos del anciano sabio",
    "cat": "maravilloso",
    "m": "Objetos mágicos aceptados como parte del mundo."
  },
  {
    "it": "El espejo del baño devuelve una habitación que no es la suya",
    "cat": "terror",
    "m": "El detalle busca inquietar y anticipar la amenaza."
  },
  {
    "it": "Un pueblo entero amanece sin recordar el día anterior, y la vida sigue igual",
    "cat": "fantastico",
    "m": "El hecho imposible no se explica ni se resuelve."
  },
  {
    "it": "Los tres deseos se piden en voz alta y el genio los concede",
    "cat": "maravilloso",
    "m": "El genio y los deseos son reglas del mundo del cuento."
  },
  {
    "it": "Alguien había estado durmiendo en su cama mientras ella no estaba",
    "cat": "terror",
    "m": "La amenaza es lo que organiza el relato."
  },
  {
    "it": "El gato de la casa empieza a contestar preguntas y la familia se aterra",
    "cat": "fantastico",
    "m": "Que la familia se asuste marca que NO es normal en ese mundo."
  }
];
GAMES.subgeneros_7 = juegoClasificar(CUR_SUBGENEROS_7_BANCO, "¿A qué subgénero pertenece?", [{"cat": "fantastico", "label": "🌀 Fantástico"}, {"cat": "maravilloso", "label": "🧚 Maravilloso"}, {"cat": "terror", "label": "🕯️ Terror"}], "subgeneros");

/* 7° · ¿Qué narrador habla? — narrador_7
   DC: Tipos de narrador; voces que se alternan
   Fuente: docs/auditoria-dc-caba/grado-7.md · L2 */
const CUR_NARRADOR_7_BANCO = [
  {
    "q": "«Caminé hasta la esquina y esperé.» ¿Qué narrador es?",
    "ops": [
      "Primera persona (protagonista)",
      "Tercera persona omnisciente",
      "Segunda persona"
    ],
    "m": "El «yo» que además protagoniza la acción."
  },
  {
    "q": "«Ana caminó hasta la esquina y esperó.» ¿Qué narrador es?",
    "ops": [
      "Tercera persona",
      "Primera persona",
      "Narrador testigo"
    ],
    "m": "Habla de ella desde afuera."
  },
  {
    "q": "¿Qué caracteriza al narrador omnisciente?",
    "ops": [
      "Sabe lo que piensan y sienten todos los personajes",
      "Sólo cuenta lo que ve",
      "Es uno de los personajes"
    ],
    "m": "«Omni» es todo: lo sabe todo, incluso lo que nadie dijo."
  },
  {
    "q": "¿Qué es un narrador testigo?",
    "ops": [
      "Un personaje que cuenta lo que le pasa a OTRO",
      "El protagonista contando su historia",
      "Alguien que lo sabe todo"
    ],
    "m": "Está adentro de la historia pero no es el que la protagoniza."
  },
  {
    "q": "«Ana caminó hasta la esquina. No sabía que la estaban esperando.» ¿Qué narrador es?",
    "ops": [
      "Omnisciente",
      "Testigo",
      "Protagonista"
    ],
    "m": "Sabe algo que la propia Ana ignora."
  },
  {
    "q": "El narrador, ¿es lo mismo que el autor?",
    "ops": [
      "No: es una voz que el autor construye",
      "Sí, siempre",
      "Sólo en primera persona"
    ],
    "m": "Un autor puede escribir en la voz de alguien muy distinto de él."
  },
  {
    "q": "«Esperé en la esquina» pasado a tercera persona es…",
    "ops": [
      "Esperó en la esquina",
      "Espero en la esquina",
      "Esperaba yo en la esquina"
    ],
    "m": "Cambia la persona del verbo, no el tiempo."
  },
  {
    "q": "«Marcos abrió la puerta» pasado a primera persona es…",
    "ops": [
      "Abrí la puerta",
      "Abre la puerta",
      "Marcos abrió la puerta"
    ],
    "m": "El personaje pasa a contar en su propia voz."
  },
  {
    "q": "¿Puede un relato alternar narradores?",
    "ops": [
      "Sí, y es un recurso muy usado",
      "No, nunca",
      "Sólo en poesía"
    ],
    "m": "Cambiar de voz sirve para dar distintos puntos de vista del mismo hecho."
  },
  {
    "q": "«Yo vi cómo Julián rompía el vidrio.» ¿Qué narrador es?",
    "ops": [
      "Testigo",
      "Protagonista",
      "Omnisciente"
    ],
    "m": "Es un yo, pero el que actúa es Julián."
  },
  {
    "q": "Un narrador en primera persona, ¿puede equivocarse?",
    "ops": [
      "Sí, sólo sabe lo que él percibe",
      "No, siempre dice la verdad",
      "Sólo si es un personaje malo"
    ],
    "m": "Ésa es la gracia del narrador no confiable."
  },
  {
    "q": "¿Qué punto de vista da más información al lector?",
    "ops": [
      "El omnisciente",
      "El protagonista",
      "El testigo"
    ],
    "m": "Accede a lo que piensan todos, no sólo a lo que uno ve."
  },
  {
    "q": "«Sentí que el corazón me latía fuerte.» ¿Podría contarlo un narrador en tercera?",
    "ops": [
      "Sí, si es omnisciente",
      "No, nunca",
      "Sólo si es testigo"
    ],
    "m": "Un testigo no puede saber lo que otro siente por dentro."
  },
  {
    "q": "En una autobiografía, ¿qué narrador se usa?",
    "ops": [
      "Primera persona",
      "Tercera persona",
      "Omnisciente"
    ],
    "m": "El que escribe cuenta su propia vida."
  }
];
GAMES.narrador_7 = juegoTriviaTexto(CUR_NARRADOR_7_BANCO, "¿Quién está contando?", "narrador_7");

/* 7° · Tres modos, un verbo — modos_verbales_7
   DC: Modos indicativo, subjuntivo e imperativo
   Fuente: docs/auditoria-dc-caba/grado-7.md · L3 */
const CUR_MODOS_VERBALES_7_BANCO = [
  {
    "it": "Mañana llueve en toda la provincia",
    "cat": "indicativo",
    "m": "Presenta el hecho como real: informa."
  },
  {
    "it": "Ojalá llueva mañana",
    "cat": "subjuntivo",
    "m": "«Ojalá» dispara el subjuntivo: expresa un deseo."
  },
  {
    "it": "Cerrá la ventana",
    "cat": "imperativo",
    "m": "Da una orden directa."
  },
  {
    "it": "Los chicos estudian todos los días",
    "cat": "indicativo",
    "m": "Enuncia un hecho."
  },
  {
    "it": "Quiero que estudies más",
    "cat": "subjuntivo",
    "m": "El verbo de deseo obliga al subjuntivo en la subordinada."
  },
  {
    "it": "Estudiá para la prueba",
    "cat": "imperativo",
    "m": "Le ordena a alguien."
  },
  {
    "it": "Ayer fuimos al cine",
    "cat": "indicativo",
    "m": "Cuenta algo que pasó."
  },
  {
    "it": "Quizás vayamos al cine",
    "cat": "subjuntivo",
    "m": "«Quizás» marca duda: subjuntivo."
  },
  {
    "it": "Vení al cine con nosotros",
    "cat": "imperativo",
    "m": "Es una invitación en forma de orden."
  },
  {
    "it": "El tren llega a las siete",
    "cat": "indicativo",
    "m": "Informa un hecho."
  },
  {
    "it": "Espero que el tren llegue a horario",
    "cat": "subjuntivo",
    "m": "«Espero que» expresa deseo y arrastra el subjuntivo."
  },
  {
    "it": "Esperá el tren en el andén",
    "cat": "imperativo",
    "m": "Indica qué hacer."
  },
  {
    "it": "Ella canta en el coro",
    "cat": "indicativo",
    "m": "Presenta el hecho como real."
  },
  {
    "it": "Ojalá cante en el coro este año",
    "cat": "subjuntivo",
    "m": "Deseo sobre algo que todavía no pasó."
  },
  {
    "it": "Cantá más fuerte",
    "cat": "imperativo",
    "m": "Orden directa a la segunda persona."
  },
  {
    "it": "No creo que sea tan difícil",
    "cat": "subjuntivo",
    "m": "La negación de «creer» expresa duda: subjuntivo."
  },
  {
    "it": "Creo que es bastante difícil",
    "cat": "indicativo",
    "m": "Afirmar una creencia sí va en indicativo."
  },
  {
    "it": "Prestá atención al cartel",
    "cat": "imperativo",
    "m": "Manda hacer algo."
  }
];
GAMES.modos_verbales_7 = juegoClasificar(CUR_MODOS_VERBALES_7_BANCO, "¿Qué modo verbal es?", [{"cat": "indicativo", "label": "📢 Indicativo"}, {"cat": "subjuntivo", "label": "🌫️ Subjuntivo"}, {"cat": "imperativo", "label": "❗ Imperativo"}], "modos_verb");

/* 7° · Clasificador de sustantivos — sustantivos_7
   DC: Individual/colectivo, abstracto/concreto, contable/incontable
   Fuente: docs/auditoria-dc-caba/grado-7.md · L4 */
const CUR_SUSTANTIVOS_7_BANCO = [
  {
    "q": "«Rebaño» es un sustantivo…",
    "ops": [
      "Colectivo",
      "Individual",
      "Abstracto"
    ],
    "m": "En singular nombra a un conjunto de ovejas."
  },
  {
    "q": "«Oveja» es un sustantivo…",
    "ops": [
      "Individual",
      "Colectivo",
      "Incontable"
    ],
    "m": "En singular nombra a una sola."
  },
  {
    "q": "«Libertad» es un sustantivo…",
    "ops": [
      "Abstracto",
      "Concreto",
      "Colectivo"
    ],
    "m": "No se puede percibir con los sentidos."
  },
  {
    "q": "«Mesa» es un sustantivo…",
    "ops": [
      "Concreto",
      "Abstracto",
      "Colectivo"
    ],
    "m": "Se puede ver y tocar."
  },
  {
    "q": "«Agua» es un sustantivo…",
    "ops": [
      "Incontable",
      "Contable",
      "Colectivo"
    ],
    "m": "No se dice «dos aguas» sin agregar una medida: dos VASOS de agua."
  },
  {
    "q": "«Silla» es un sustantivo…",
    "ops": [
      "Contable",
      "Incontable",
      "Abstracto"
    ],
    "m": "Se puede contar de a una."
  },
  {
    "q": "«Arboleda» es un sustantivo…",
    "ops": [
      "Colectivo",
      "Individual",
      "Abstracto"
    ],
    "m": "Nombra a un conjunto de árboles."
  },
  {
    "q": "«Alegría» es un sustantivo…",
    "ops": [
      "Abstracto",
      "Concreto",
      "Contable"
    ],
    "m": "Es un sentimiento: no se toca."
  },
  {
    "q": "¿Qué caracteriza a un sustantivo colectivo?",
    "ops": [
      "Que en SINGULAR nombra a un conjunto",
      "Que va siempre en plural",
      "Que nombra ideas"
    ],
    "m": "«Enjambre» es singular y nombra a muchas abejas."
  },
  {
    "q": "«Arena» es un sustantivo…",
    "ops": [
      "Incontable",
      "Contable",
      "Colectivo"
    ],
    "m": "Se mide, no se cuenta: un kilo de arena."
  },
  {
    "q": "«Manada» es colectivo de…",
    "ops": [
      "Lobos u otros animales",
      "Árboles",
      "Barcos"
    ],
    "m": "De árboles sería arboleda; de barcos, flota."
  },
  {
    "q": "Un sustantivo, ¿puede ser concreto y contable a la vez?",
    "ops": [
      "Sí: «silla» es las dos cosas",
      "No, son excluyentes",
      "Sólo si es colectivo"
    ],
    "m": "Los ejes de clasificación son independientes entre sí."
  },
  {
    "q": "«Flota» es colectivo de…",
    "ops": [
      "Barcos",
      "Ovejas",
      "Estrellas"
    ],
    "m": "De ovejas es rebaño; de estrellas, constelación."
  },
  {
    "q": "«Justicia» es un sustantivo…",
    "ops": [
      "Abstracto",
      "Concreto",
      "Contable"
    ],
    "m": "Nombra un concepto, no un objeto."
  },
  {
    "q": "«Coraje» es un sustantivo…",
    "ops": [
      "Abstracto e incontable",
      "Concreto",
      "Colectivo"
    ],
    "m": "No se toca ni se cuenta de a uno."
  }
];
GAMES.sustantivos_7 = juegoTriviaTexto(CUR_SUSTANTIVOS_7_BANCO, "¿Qué tipo de sustantivo es?", "sustantivo");

/* 7° · ¿Quién es el sujeto? — sujeto_7
   DC: Sujeto expreso y tácito; oraciones impersonales
   Fuente: docs/auditoria-dc-caba/grado-7.md · L5 */
const CUR_SUJETO_7_BANCO = [
  {
    "q": "En «Los chicos juegan en el patio», ¿cuál es el sujeto?",
    "ops": [
      "Los chicos",
      "juegan",
      "en el patio"
    ],
    "m": "¿Quiénes juegan? Los chicos."
  },
  {
    "q": "En «Llegamos temprano», ¿cuál es el sujeto?",
    "ops": [
      "Nosotros, tácito",
      "temprano",
      "No tiene sujeto"
    ],
    "m": "No está escrito, pero la terminación del verbo lo indica: es tácito."
  },
  {
    "q": "¿Qué es un sujeto tácito?",
    "ops": [
      "Uno que no está escrito pero se sobreentiende",
      "Uno que no existe",
      "El que va al final"
    ],
    "m": "El que no existe es el de las impersonales, que es distinto."
  },
  {
    "q": "«Hay tres libros en la mesa». ¿Cuál es el sujeto?",
    "ops": [
      "No tiene: es impersonal",
      "Tres libros",
      "La mesa"
    ],
    "m": "«Haber» impersonal no lleva sujeto. Por eso siempre va en singular: «hay», nunca «han» tres libros."
  },
  {
    "q": "«Hace mucho calor». ¿Cuál es el sujeto?",
    "ops": [
      "No tiene: es impersonal",
      "Mucho calor",
      "Está tácito"
    ],
    "m": "Los verbos de fenómeno meteorológico son impersonales."
  },
  {
    "q": "«Llueve desde ayer». ¿Cuál es el sujeto?",
    "ops": [
      "No tiene: es impersonal",
      "La lluvia, tácito",
      "Desde ayer"
    ],
    "m": "No hay nadie que llueva: el verbo funciona solo."
  },
  {
    "q": "En «Ana y Luis cocinaron», ¿cómo es el sujeto?",
    "ops": [
      "Compuesto: tiene dos núcleos",
      "Simple",
      "Tácito"
    ],
    "m": "Dos núcleos coordinados por «y»."
  },
  {
    "q": "¿Cómo se encuentra el sujeto de una oración?",
    "ops": [
      "Preguntándole al verbo quién o qué",
      "Buscando la primera palabra",
      "Buscando el sustantivo más largo"
    ],
    "m": "El sujeto no siempre va primero."
  },
  {
    "q": "En «Ayer llegó el paquete», ¿cuál es el sujeto?",
    "ops": [
      "El paquete",
      "Ayer",
      "Llegó"
    ],
    "m": "Aunque vaya al final, es lo que responde a «¿qué llegó?»."
  },
  {
    "q": "«Se vive bien en esta ciudad». ¿Qué tipo de oración es?",
    "ops": [
      "Impersonal",
      "De sujeto tácito",
      "De sujeto compuesto"
    ],
    "m": "No se dice quién vive: es una impersonal con «se»."
  },
  {
    "q": "¿Por qué «Habían muchas personas» está mal?",
    "ops": [
      "Porque «haber» impersonal va siempre en singular: «Había»",
      "Porque falta el sujeto",
      "No está mal"
    ],
    "m": "«Muchas personas» no es el sujeto, así que no arrastra el plural."
  },
  {
    "q": "En «El profesor de música llegó tarde», ¿cuál es el NÚCLEO del sujeto?",
    "ops": [
      "profesor",
      "música",
      "El"
    ],
    "m": "«De música» sólo modifica a «profesor»."
  },
  {
    "q": "«Estudiamos toda la tarde». El sujeto es…",
    "ops": [
      "Nosotros, tácito",
      "Toda la tarde",
      "Inexistente"
    ],
    "m": "La desinencia del verbo indica quién."
  },
  {
    "q": "¿Puede una oración tener sujeto y no verbo?",
    "ops": [
      "No: sin verbo no hay oración bimembre",
      "Sí, siempre",
      "Sólo en preguntas"
    ],
    "m": "El verbo es el núcleo del predicado y no puede faltar."
  }
];
GAMES.sujeto_7 = juegoTriviaTexto(CUR_SUJETO_7_BANCO, "Preguntale al verbo quién.", "sujeto_7");

/* 7° · Metáfora o sinécdoque — metafora_sinecdoque_7
   DC: Metáfora y sinécdoque; el yo poético no es el autor
   Fuente: docs/auditoria-dc-caba/grado-7.md · L6 */
const CUR_METAFORA_SINECDOQUE_7_BANCO = [
  {
    "q": "«Sus cabellos son oro.» ¿Qué recurso es?",
    "ops": [
      "Metáfora",
      "Sinécdoque",
      "Comparación"
    ],
    "m": "Sustituye por semejanza y sin usar «como»."
  },
  {
    "q": "«Necesitamos brazos para la cosecha.» ¿Qué recurso es?",
    "ops": [
      "Sinécdoque",
      "Metáfora",
      "Hipérbole"
    ],
    "m": "Nombra la parte (los brazos) para referirse al todo (los trabajadores)."
  },
  {
    "q": "¿Qué es una sinécdoque?",
    "ops": [
      "Nombrar el todo por la parte, o la parte por el todo",
      "Comparar dos cosas con «como»",
      "Exagerar a propósito"
    ],
    "m": "Lo que la define es la relación de pertenencia, no el parecido."
  },
  {
    "q": "«Tiene cien cabezas de ganado.» ¿Qué recurso es?",
    "ops": [
      "Sinécdoque",
      "Metáfora",
      "Personificación"
    ],
    "m": "La cabeza está por el animal entero."
  },
  {
    "q": "«La ciudad dormía.» ¿Qué recurso es?",
    "ops": [
      "Personificación",
      "Sinécdoque",
      "Metáfora"
    ],
    "m": "Le atribuye a la ciudad una acción de ser vivo."
  },
  {
    "q": "¿Qué es el yo poético?",
    "ops": [
      "La voz que habla en el poema, que no es el autor",
      "El autor del poema",
      "El lector"
    ],
    "m": "Un autor puede escribir un poema en la voz de otra persona."
  },
  {
    "q": "«Me compré un Picasso.» ¿Qué recurso es?",
    "ops": [
      "Metonimia o sinécdoque: el autor por la obra",
      "Metáfora",
      "Comparación"
    ],
    "m": "Se nombra al creador para referirse a lo creado."
  },
  {
    "q": "«El otoño de la vida» se refiere a…",
    "ops": [
      "La vejez, por metáfora",
      "Una estación del año",
      "Una comparación"
    ],
    "m": "Traslada el sentido del ciclo natural a la vida de una persona."
  },
  {
    "q": "«Sus ojos brillan como estrellas.» ¿Qué recurso es?",
    "ops": [
      "Comparación",
      "Metáfora",
      "Sinécdoque"
    ],
    "m": "El «como» está explícito: comparación, no metáfora."
  },
  {
    "q": "¿En qué se diferencian metáfora y comparación?",
    "ops": [
      "La comparación usa un nexo como «como»; la metáfora sustituye directamente",
      "La metáfora es más larga",
      "No se diferencian"
    ],
    "m": "El nexo es la marca visible."
  },
  {
    "q": "«Se ganan el pan trabajando.» ¿Qué recurso es?",
    "ops": [
      "Sinécdoque: el pan por todo el alimento",
      "Metáfora",
      "Hipérbole"
    ],
    "m": "Una parte del sustento nombra al sustento entero."
  },
  {
    "q": "«El poeta dice que está triste.» ¿A quién le corresponde esa tristeza?",
    "ops": [
      "Al yo poético, no necesariamente al autor",
      "Siempre al autor",
      "Al lector"
    ],
    "m": "Confundir yo poético con autor es el error clásico del tema."
  },
  {
    "q": "«Río de gente» es…",
    "ops": [
      "Una metáfora",
      "Una sinécdoque",
      "Una personificación"
    ],
    "m": "El río sustituye a la multitud por semejanza en cómo se mueve."
  },
  {
    "q": "«Tres velas cruzaron el horizonte.» ¿Qué recurso es?",
    "ops": [
      "Sinécdoque: las velas por los barcos",
      "Metáfora",
      "Comparación"
    ],
    "m": "La parte visible nombra al todo."
  }
];
GAMES.metafora_sinecdoque_7 = juegoTriviaTexto(CUR_METAFORA_SINECDOQUE_7_BANCO, "¿Qué recurso se está usando?", "metafora_s");

/* 7° · Hecho, opinión o argumento — hecho_opinion_argumento_7
   DC: Distinguir hecho verificable, opinión y argumento
   Fuente: docs/auditoria-dc-caba/grado-7.md · L7 */
const CUR_HECHO_OPINION_ARGUMENTO_7_BANCO = [
  {
    "it": "El agua hierve a 100 °C al nivel del mar",
    "cat": "hecho",
    "m": "Se puede medir y cualquiera obtiene el mismo resultado."
  },
  {
    "it": "El invierno es la peor estación del año",
    "cat": "opinion",
    "m": "«Peor» depende de quién juzgue: no hay medición posible."
  },
  {
    "it": "Conviene abrigarse en invierno porque el frío baja las defensas",
    "cat": "argumento",
    "m": "Sostiene una postura con una razón."
  },
  {
    "it": "La Argentina limita con cinco países",
    "cat": "hecho",
    "m": "Se verifica mirando un mapa."
  },
  {
    "it": "El fútbol es el deporte más lindo",
    "cat": "opinion",
    "m": "Un juicio de gusto, sin criterio verificable."
  },
  {
    "it": "Hay que hacer deporte porque mejora la salud cardiovascular",
    "cat": "argumento",
    "m": "Da la razón que fundamenta la postura."
  },
  {
    "it": "El censo de 2022 registró 46 millones de habitantes",
    "cat": "hecho",
    "m": "Es un dato con fuente que se puede consultar."
  },
  {
    "it": "Los libros son mejores que las películas",
    "cat": "opinion",
    "m": "No hay forma de medir «mejor» acá."
  },
  {
    "it": "Leer amplía el vocabulario, y por eso conviene hacerlo",
    "cat": "argumento",
    "m": "Encadena un motivo con una recomendación."
  },
  {
    "it": "El Aconcagua mide 6.960 metros",
    "cat": "hecho",
    "m": "Es una medición comprobable."
  },
  {
    "it": "Las vacaciones de invierno deberían ser más largas",
    "cat": "opinion",
    "m": "Expresa un deseo sin fundamentarlo."
  },
  {
    "it": "Las vacaciones deberían ser más largas porque el segundo cuatrimestre es el más cargado",
    "cat": "argumento",
    "m": "La misma postura, ahora con una razón que la sostiene."
  },
  {
    "it": "El agua se congela a 0 °C",
    "cat": "hecho",
    "m": "Dato verificable."
  },
  {
    "it": "La música de antes era mejor",
    "cat": "opinion",
    "m": "No hay criterio objetivo para compararlas."
  },
  {
    "it": "Conviene separar los residuos porque reduce lo que se entierra",
    "cat": "argumento",
    "m": "Postura más razón: argumento."
  },
  {
    "it": "La Ley 1420 se sancionó en 1884",
    "cat": "hecho",
    "m": "Se puede consultar."
  },
  {
    "it": "Este es el mejor libro que leí",
    "cat": "opinion",
    "m": "Es un juicio personal."
  },
  {
    "it": "El transporte público conviene porque mueve más gente con menos emisiones",
    "cat": "argumento",
    "m": "Da el motivo que respalda la conclusión."
  }
];
GAMES.hecho_opinion_argumento_7 = juegoClasificar(CUR_HECHO_OPINION_ARGUMENTO_7_BANCO, "¿Se puede verificar, es un juicio, o lo fundamenta?", [{"cat": "hecho", "label": "📋 Hecho"}, {"cat": "opinion", "label": "💭 Opinión"}, {"cat": "argumento", "label": "🧩 Argumento"}], "hecho_opin");

/* 7° · Recursos del argumentador — recursos_argumentador_7
   DC: Cita de autoridad, ejemplificación, contraejemplo y generalización
   Fuente: docs/auditoria-dc-caba/grado-7.md · L8 */
const CUR_RECURSOS_ARGUMENTADOR_7_BANCO = [
  {
    "it": "«Según la Organización Mundial de la Salud, dormir menos de 8 horas afecta la memoria»",
    "cat": "autoridad",
    "m": "Se apoya en una institución reconocida."
  },
  {
    "it": "«Por ejemplo, en Rosario el carril exclusivo bajó los tiempos de viaje»",
    "cat": "ejemplo",
    "m": "Ilustra la afirmación con un caso concreto."
  },
  {
    "it": "«Se dice que todos los adolescentes duermen poco, pero mi hermana duerme nueve horas»",
    "cat": "contraejemplo",
    "m": "Un solo caso alcanza para refutar un «todos»."
  },
  {
    "it": "«Los chicos de hoy no leen»",
    "cat": "generalizacion",
    "m": "Extiende a todos algo observado en algunos; es el recurso más frágil."
  },
  {
    "it": "«El doctor Favaloro sostenía que la prevención salva más vidas que la cirugía»",
    "cat": "autoridad",
    "m": "Cita a un especialista reconocido."
  },
  {
    "it": "«Pensemos en el caso de Bariloche, donde el turismo cambió la economía»",
    "cat": "ejemplo",
    "m": "Un caso particular que ilustra la idea."
  },
  {
    "it": "«Dicen que ningún gato nada, pero el gato de Bengala sí lo hace»",
    "cat": "contraejemplo",
    "m": "Refuta una afirmación absoluta con un caso."
  },
  {
    "it": "«Siempre que llueve, el tránsito colapsa»",
    "cat": "generalizacion",
    "m": "El «siempre» es lo que la vuelve generalización."
  },
  {
    "it": "«El informe del CONICET indica que la sequía redujo la cosecha»",
    "cat": "autoridad",
    "m": "Respalda con una institución científica."
  },
  {
    "it": "«Mirá lo que pasó en Rosario con el ordenamiento del centro»",
    "cat": "ejemplo",
    "m": "Un caso concreto para apoyar la postura."
  },
  {
    "it": "«Aseguran que ninguna ave no vuela; el pingüino los desmiente»",
    "cat": "contraejemplo",
    "m": "Un caso que rompe la regla enunciada."
  },
  {
    "it": "«Toda la gente joven prefiere los videos a los libros»",
    "cat": "generalizacion",
    "m": "Un «toda» sin datos que lo respalden."
  },
  {
    "it": "«Como explica la Sociedad Argentina de Pediatría, el calendario de vacunas es gratuito»",
    "cat": "autoridad",
    "m": "Apela al saber de una entidad especializada."
  },
  {
    "it": "«Un caso claro es el del reciclaje en San Isidro»",
    "cat": "ejemplo",
    "m": "Ilustra con una experiencia concreta."
  },
  {
    "it": "«Se afirma que nadie usa el efectivo, pero en las ferias se usa todo el tiempo»",
    "cat": "contraejemplo",
    "m": "Desarma el «nadie» con un contraejemplo."
  },
  {
    "it": "«Los docentes están todos de acuerdo con la medida»",
    "cat": "generalizacion",
    "m": "Atribuye a un grupo entero una postura sin medirla."
  }
];
GAMES.recursos_argumentador_7 = juegoClasificar(CUR_RECURSOS_ARGUMENTADOR_7_BANCO, "¿Qué recurso está usando para convencer?", [{"cat": "autoridad", "label": "🎓 Cita de autoridad"}, {"cat": "ejemplo", "label": "📌 Ejemplificación"}, {"cat": "contraejemplo", "label": "🚫 Contraejemplo"}, {"cat": "generalizacion", "label": "🌐 Generalización"}], "recursos_a");

/* 7° · Detector de persuasión — persuasion_7
   DC: Recursos de persuasión de la publicidad; verbal y visual
   Fuente: docs/auditoria-dc-caba/grado-7.md · L9 */
const CUR_PERSUASION_7_BANCO = [
  {
    "q": "«¡Última oportunidad! Sólo por hoy.» ¿Qué recurso usa?",
    "ops": [
      "Urgencia artificial",
      "Cita de autoridad",
      "Dato verificable"
    ],
    "m": "Apura la decisión para que no la pienses."
  },
  {
    "q": "«9 de cada 10 dentistas lo recomiendan.» ¿Qué recurso usa?",
    "ops": [
      "Apelación a la autoridad, sin fuente",
      "Un dato verificable",
      "Una comparación"
    ],
    "m": "Parece un dato, pero no dice quién midió ni a cuántos preguntó."
  },
  {
    "q": "Un famoso usando el producto apela a…",
    "ops": [
      "La identificación con alguien admirado",
      "Un argumento lógico",
      "Una prueba científica"
    ],
    "m": "No dice nada sobre el producto: transfiere el prestigio de la persona."
  },
  {
    "q": "«Con esta bebida vas a tener más amigos.» ¿Qué promete?",
    "ops": [
      "Un beneficio que el producto no puede dar",
      "Una característica real",
      "Un dato del envase"
    ],
    "m": "La promesa exagerada asocia el producto con algo que no depende de él."
  },
  {
    "q": "¿Cuál es la función principal de una publicidad?",
    "ops": [
      "Convencer de hacer algo",
      "Informar sin intención",
      "Enseñar un contenido"
    ],
    "m": "Aunque informe de paso, su objetivo es persuadir."
  },
  {
    "q": "«Vos te lo merecés» apela a…",
    "ops": [
      "Las emociones del que mira",
      "La razón",
      "Un dato objetivo"
    ],
    "m": "Habla del deseo, no del producto."
  },
  {
    "q": "El uso de colores brillantes y música alegre es un recurso…",
    "ops": [
      "Visual y sonoro, no verbal",
      "Verbal",
      "Argumentativo"
    ],
    "m": "La persuasión no está sólo en las palabras."
  },
  {
    "q": "«El líder del mercado» es…",
    "ops": [
      "Un argumento de popularidad",
      "Un dato técnico",
      "Un contraejemplo"
    ],
    "m": "Que muchos lo compren no dice que sea mejor."
  },
  {
    "q": "La letra chica en una publicidad suele contener…",
    "ops": [
      "Las condiciones que limitan la promesa",
      "El precio real",
      "El nombre del autor"
    ],
    "m": "Ahí aparece lo que la promesa grande omite."
  },
  {
    "q": "«Antes y después» en una publicidad de un producto de belleza es…",
    "ops": [
      "Una comparación armada para convencer",
      "Una prueba científica",
      "Un dato verificable"
    ],
    "m": "La iluminación y la pose pueden explicar la diferencia."
  },
  {
    "q": "¿Qué es un eslogan?",
    "ops": [
      "Una frase corta y pegadiza que resume la marca",
      "El precio",
      "El nombre del producto"
    ],
    "m": "Está diseñado para que lo recuerdes sin esfuerzo."
  },
  {
    "q": "«Gratis» en letras grandes con «con la compra de dos» abajo es…",
    "ops": [
      "Una promesa que la condición limita",
      "Una oferta sin condiciones",
      "Un error de imprenta"
    ],
    "m": "Leer la condición completa es parte de leer una publicidad."
  },
  {
    "q": "¿Qué diferencia hay entre publicidad y propaganda?",
    "ops": [
      "La publicidad vende productos; la propaganda difunde ideas",
      "Son sinónimos",
      "La propaganda es más corta"
    ],
    "m": "Una campaña de vacunación es propaganda, no publicidad."
  },
  {
    "q": "Ante una publicidad, ¿qué conviene preguntarse?",
    "ops": [
      "Quién la paga y qué quiere que yo haga",
      "Si me gusta la música",
      "Cuánto dura"
    ],
    "m": "Identificar el emisor y su intención es la clave de la lectura crítica."
  }
];
GAMES.persuasion_7 = juegoTriviaTexto(CUR_PERSUASION_7_BANCO, "¿Con qué te quiere convencer?", "persuasion");

/* 7° · De la noticia a la crónica — cronica_7
   DC: La crónica policial; discurso directo e indirecto
   Fuente: docs/auditoria-dc-caba/grado-7.md · L10 */
const CUR_CRONICA_7_BANCO = [
  {
    "q": "¿Cuál es la diferencia central entre noticia y crónica?",
    "ops": [
      "La crónica narra en orden temporal; la noticia arranca por lo más importante",
      "La crónica es más corta",
      "La noticia no lleva título"
    ],
    "m": "La noticia usa pirámide invertida; la crónica recupera la secuencia."
  },
  {
    "q": "¿Qué diferencia a una crónica de una noticia?",
    "ops": [
      "La crónica narra el hecho en orden y con detalle",
      "La crónica es más corta",
      "La noticia lleva opinión"
    ],
    "m": "La noticia informa lo esencial; la crónica cuenta cómo pasó."
  },
  {
    "q": "«El testigo dijo: “Vi todo desde la ventana”.» ¿Qué tipo de discurso es?",
    "ops": [
      "Directo",
      "Indirecto",
      "Ninguno"
    ],
    "m": "Las comillas reproducen las palabras exactas."
  },
  {
    "q": "«El testigo dijo que había visto todo desde la ventana.» ¿Qué tipo es?",
    "ops": [
      "Indirecto",
      "Directo",
      "Mixto"
    ],
    "m": "Aparece el «que» y el verbo se corre al pasado."
  },
  {
    "q": "¿Qué aporta una cita textual en una crónica?",
    "ops": [
      "La voz del protagonista sin intermediarios",
      "Más extensión",
      "Una opinión del cronista"
    ],
    "m": "Le da al lector el testimonio directo."
  },
  {
    "q": "Una crónica, ¿puede tener descripciones y clima?",
    "ops": [
      "Sí, es parte de su recurso narrativo",
      "No, sólo datos",
      "Sólo si es de deportes"
    ],
    "m": "La crónica está más cerca de la narración que la noticia."
  },
  {
    "q": "En una crónica policial, ¿qué NO corresponde?",
    "ops": [
      "Condenar de antemano a un sospechoso",
      "Reconstruir los hechos",
      "Citar a los testigos"
    ],
    "m": "Hasta que haya sentencia, se informa sin dar por probado."
  },
  {
    "q": "¿Qué es el copete?",
    "ops": [
      "El párrafo inicial que resume lo esencial",
      "El título",
      "El cierre"
    ],
    "m": "Va entre el título y el cuerpo."
  },
  {
    "q": "«“Salí corriendo”, contó la vecina» pasado a indirecto:",
    "ops": [
      "La vecina contó que había salido corriendo",
      "La vecina contó que salí corriendo",
      "La vecina: salí corriendo"
    ],
    "m": "Cambian la persona y el tiempo del verbo."
  },
  {
    "q": "¿Qué preguntas debe responder una crónica completa?",
    "ops": [
      "Qué, quién, cuándo, dónde, cómo y por qué",
      "Sólo qué y cuándo",
      "Cuánto y dónde"
    ],
    "m": "Son las mismas seis preguntas del periodismo."
  },
  {
    "q": "En periodismo, ¿qué es contrastar fuentes?",
    "ops": [
      "Chequear el dato con más de un testimonio",
      "Elegir la fuente más rápida",
      "Copiar de otro medio"
    ],
    "m": "Una sola fuente puede estar equivocada o interesada."
  },
  {
    "q": "¿Qué diferencia una crónica de un cuento?",
    "ops": [
      "La crónica narra hechos reales verificables",
      "El cuento es más largo",
      "No hay diferencia"
    ],
    "m": "Las dos narran, pero una se compromete con la verdad de los hechos."
  },
  {
    "q": "El orden «pasó A, después B, después C» corresponde a…",
    "ops": [
      "Una crónica",
      "Una noticia",
      "Un aviso"
    ],
    "m": "La noticia rompería ese orden para empezar por lo más importante."
  },
  {
    "q": "¿Para qué sirve el epígrafe de una foto?",
    "ops": [
      "Para explicar qué se ve y dónde fue",
      "Para poner el título",
      "Para firmar la nota"
    ],
    "m": "Una foto sin epígrafe puede leerse mal."
  }
];
GAMES.cronica_7 = juegoTriviaTexto(CUR_CRONICA_7_BANCO, "Pensá el orden y la voz del relato.", "cronica_7");

/* 7° · Armá tu historieta — historieta_7
   DC: Historieta: viñeta, globo, onomatopeya y guion
   Fuente: docs/auditoria-dc-caba/grado-7.md · L11 */
const CUR_HISTORIETA_7_BANCO = [
  {
    "q": "¿Qué es una viñeta?",
    "ops": [
      "Cada cuadro de la historieta",
      "El globo de diálogo",
      "El texto del narrador"
    ],
    "m": "Es la unidad mínima: dentro va la escena."
  },
  {
    "q": "¿Qué es un globo o bocadillo?",
    "ops": [
      "El espacio donde va lo que dice o piensa un personaje",
      "El cuadro de la historieta",
      "El sonido dibujado"
    ],
    "m": "Su forma indica si el personaje habla, piensa o grita."
  },
  {
    "q": "Un globo con el borde en forma de nube indica…",
    "ops": [
      "Que el personaje piensa, no habla",
      "Que grita",
      "Que susurra"
    ],
    "m": "La forma del globo es información, no decoración."
  },
  {
    "q": "Un globo con bordes en punta indica…",
    "ops": [
      "Grito o enojo",
      "Pensamiento",
      "Susurro"
    ],
    "m": "El dibujo del globo transmite el tono."
  },
  {
    "q": "¿Qué es una onomatopeya en la historieta?",
    "ops": [
      "Una palabra que representa un sonido",
      "El texto del narrador",
      "El nombre del autor"
    ],
    "m": "«CRASH», «BOOM» y «PUM» son las más típicas."
  },
  {
    "q": "¿Qué es el cartucho o cartela?",
    "ops": [
      "El recuadro con la voz del narrador",
      "El globo de diálogo",
      "El título de la historieta"
    ],
    "m": "Suele indicar el tiempo o el lugar: «Mientras tanto…»."
  },
  {
    "q": "¿Qué es el guion de una historieta?",
    "ops": [
      "El texto que describe qué pasa en cada viñeta y qué se dice",
      "El dibujo terminado",
      "El título"
    ],
    "m": "Es lo que se escribe antes de dibujar."
  },
  {
    "q": "¿En qué orden se leen las viñetas en español?",
    "ops": [
      "De izquierda a derecha y de arriba abajo",
      "De derecha a izquierda",
      "En cualquier orden"
    ],
    "m": "El manga japonés se lee al revés, y por eso desorienta al principio."
  },
  {
    "q": "Las líneas cinéticas (rayitas de movimiento) sirven para…",
    "ops": [
      "Mostrar que algo se mueve",
      "Decorar el cuadro",
      "Marcar el final"
    ],
    "m": "Con una imagen fija hay que dibujar el movimiento."
  },
  {
    "q": "¿Qué pasa entre una viñeta y la siguiente?",
    "ops": [
      "El lector completa lo que no se muestra",
      "No pasa nada",
      "Se repite la escena"
    ],
    "m": "Ese espacio en blanco es parte del lenguaje: el lector lo llena."
  },
  {
    "q": "Mafalda es una historieta creada por…",
    "ops": [
      "Quino",
      "Fontanarrosa",
      "Caloi"
    ],
    "m": "Fontanarrosa creó Inodoro Pereyra y Caloi, a Clemente."
  },
  {
    "q": "Clemente es un personaje creado por…",
    "ops": [
      "Caloi",
      "Quino",
      "Quirino Cristiani"
    ],
    "m": "Caloi lo publicó durante décadas en el diario Clarín."
  },
  {
    "q": "¿Puede una historieta contar algo sin ninguna palabra?",
    "ops": [
      "Sí, se llama historieta muda",
      "No, siempre lleva texto",
      "Sólo si es de humor"
    ],
    "m": "La secuencia de imágenes alcanza para narrar."
  },
  {
    "q": "¿Qué es una tira cómica?",
    "ops": [
      "Una historieta corta, de pocas viñetas",
      "Una historieta muda",
      "El guion sin dibujar"
    ],
    "m": "Suele resolverse en tres o cuatro viñetas."
  }
];
GAMES.historieta_7 = juegoTriviaTexto(CUR_HISTORIETA_7_BANCO, "Reconocé los elementos del lenguaje de la historieta.", "historieta");

/* 7° · Corregí el error — ambiguedad_7
   DC: Problemas usuales del uso; ambigüedad sintáctica
   Fuente: docs/auditoria-dc-caba/grado-7.md · L12 */
const CUR_AMBIGUEDAD_7_BANCO = [
  {
    "q": "«Vi a Juan corriendo por la plaza.» ¿Por qué es ambigua?",
    "ops": [
      "No se sabe quién corría",
      "Falta el verbo",
      "Está mal el tiempo verbal"
    ],
    "m": "El gerundio puede referirse a Juan o al que mira."
  },
  {
    "q": "«El perro de mi hermano que ladra mucho.» ¿Qué es ambiguo?",
    "ops": [
      "No se sabe si ladra el perro o el hermano",
      "El posesivo",
      "Nada, está bien"
    ],
    "m": "El relativo puede engancharse con cualquiera de los dos."
  },
  {
    "q": "¿Cómo se dice correctamente?",
    "ops": [
      "El decimoprimer piso",
      "El onceavo piso",
      "El once piso"
    ],
    "m": "«Onceavo» es una fracción (1/11), no un ordinal."
  },
  {
    "q": "«Habían muchas personas» debería ser…",
    "ops": [
      "Había muchas personas",
      "Habían mucha gente",
      "Han habido muchas personas"
    ],
    "m": "«Haber» impersonal va siempre en singular."
  },
  {
    "q": "«Detrás mío» debería decirse…",
    "ops": [
      "Detrás de mí",
      "Detrás mía",
      "Atrás mío"
    ],
    "m": "Los adverbios de lugar no admiten posesivo."
  },
  {
    "q": "«Se los dije a los chicos» debería ser…",
    "ops": [
      "Se lo dije a los chicos",
      "Se les dije a los chicos",
      "Está bien así"
    ],
    "m": "Lo dicho es UNA cosa: va «lo». El plural ya está en «se», que reemplaza a «les». «Se los dije» es un error muy común."
  },
  {
    "q": "«Le dije a mis primos» debería ser…",
    "ops": [
      "Les dije a mis primos",
      "Le dije a mi primos",
      "Lo dije a mis primos"
    ],
    "m": "El pronombre tiene que concordar en número con el objeto indirecto."
  },
  {
    "q": "«El mismo» usado como pronombre («llegó el paquete y abrí el mismo») es…",
    "ops": [
      "Un uso desaconsejado: mejor «lo abrí»",
      "Correcto siempre",
      "Un error de ortografía"
    ],
    "m": "«El mismo» funciona como adjetivo, no como sustituto del pronombre."
  },
  {
    "q": "«Media hora» o «medio hora»: ¿cuál va?",
    "ops": [
      "Media hora",
      "Medio hora",
      "Las dos"
    ],
    "m": "Concuerda con «hora», que es femenino."
  },
  {
    "q": "«Vendieron los libros a los alumnos usados.» ¿Qué pasa?",
    "ops": [
      "El adjetivo quedó lejos y parece referirse a los alumnos",
      "Falta un verbo",
      "Está bien"
    ],
    "m": "El orden de las palabras cambia el sentido: «los libros usados»."
  },
  {
    "q": "«Ayer me encontré con Ana y su hermana. Ella tenía puesto un abrigo rojo.» ¿Qué falla?",
    "ops": [
      "No se sabe a cuál de las dos se refiere «ella»",
      "El tiempo verbal",
      "El adjetivo"
    ],
    "m": "La referencia pronominal quedó ambigua."
  },
  {
    "q": "«Contra más estudio, mejor me va» debería ser…",
    "ops": [
      "Cuanto más estudio, mejor me va",
      "Contra más estudio, mejor",
      "Mientras más estudio, contra mejor"
    ],
    "m": "«Contra más» no es una forma correcta."
  },
  {
    "q": "«Se alquila departamento para señorita amueblado.» ¿Qué pasa?",
    "ops": [
      "El adjetivo quedó separado de lo que califica",
      "Falta el precio",
      "Está bien"
    ],
    "m": "Debería ser «departamento amueblado para señorita»."
  },
  {
    "q": "¿Cómo se evita la ambigüedad?",
    "ops": [
      "Reordenando la frase o repitiendo el sustantivo",
      "Alargando la oración",
      "Agregando comas al azar"
    ],
    "m": "Poner cada modificador cerca de lo que modifica resuelve casi todo."
  }
];
GAMES.ambiguedad_7 = juegoTriviaTexto(CUR_AMBIGUEDAD_7_BANCO, "Encontrá el problema de la frase.", "ambiguedad");

/* 7° · Análisis sintáctico completo — analisis_sintactico_7
   DC: Sujeto y predicado, núcleos, modificadores, OD, OI y predicativo
   Fuente: docs/auditoria-dc-caba/grado-7.md · L13 */
const CUR_ANALISIS_SINTACTICO_7_BANCO = [
  {
    "q": "En «Los alumnos entregaron la tarea», ¿cuál es el OD?",
    "ops": [
      "la tarea",
      "Los alumnos",
      "entregaron"
    ],
    "m": "Se reemplaza por LA: «la entregaron»."
  },
  {
    "q": "En «Le entregué la tarea al profesor», ¿cuál es el OI?",
    "ops": [
      "al profesor",
      "la tarea",
      "Le entregué"
    ],
    "m": "Es quien recibe: se reemplaza por LE."
  },
  {
    "q": "En «Mi hermano es médico», ¿qué función cumple «médico»?",
    "ops": [
      "Predicativo subjetivo obligatorio",
      "Objeto directo",
      "Adjunto"
    ],
    "m": "Con verbos copulativos (ser, estar, parecer) no hay OD: hay predicativo."
  },
  {
    "q": "¿Qué verbos son copulativos?",
    "ops": [
      "Ser, estar y parecer",
      "Comer, correr y saltar",
      "Haber y hacer"
    ],
    "m": "No expresan acción: unen el sujeto con su característica."
  },
  {
    "q": "En «El agua está fría», ¿qué es «fría»?",
    "ops": [
      "Predicativo subjetivo obligatorio",
      "Modificador directo",
      "Objeto directo"
    ],
    "m": "Con «estar» la palabra que sigue describe al sujeto."
  },
  {
    "q": "En «la casa grande de la esquina», ¿qué es «de la esquina»?",
    "ops": [
      "Modificador indirecto",
      "Modificador directo",
      "Aposición"
    ],
    "m": "Va con preposición: por eso es indirecto."
  },
  {
    "q": "En «Buenos Aires, la capital, es enorme», ¿qué es «la capital»?",
    "ops": [
      "Aposición",
      "Modificador directo",
      "Predicativo"
    ],
    "m": "Va entre comas y podría ocupar el lugar del núcleo."
  },
  {
    "q": "¿Cuál es el núcleo del predicado?",
    "ops": [
      "Siempre el verbo",
      "El sustantivo",
      "El adjetivo"
    ],
    "m": "Sin verbo no hay predicado."
  },
  {
    "q": "En «Ana llegó cansada», ¿qué es «cansada»?",
    "ops": [
      "Predicativo subjetivo no obligatorio",
      "Objeto directo",
      "Modificador directo"
    ],
    "m": "No es obligatorio —«Ana llegó» funciona sola— pero describe al sujeto."
  },
  {
    "q": "¿Cómo se prueba que algo es OD?",
    "ops": [
      "Reemplazándolo por LO o LA",
      "Reemplazándolo por LE",
      "Sacándolo de la oración"
    ],
    "m": "LE es la marca del indirecto."
  },
  {
    "q": "En «Corrimos por el parque», ¿qué es «por el parque»?",
    "ops": [
      "Un adjunto o circunstancial de lugar",
      "Objeto directo",
      "Predicativo"
    ],
    "m": "Se puede sacar y la oración sigue en pie."
  },
  {
    "q": "En «Trajeron flores para mi mamá», ¿cuál es el OI?",
    "ops": [
      "para mi mamá",
      "flores",
      "Trajeron"
    ],
    "m": "Es el destinatario de la acción."
  },
  {
    "q": "¿Por dónde conviene empezar un análisis sintáctico?",
    "ops": [
      "Por el verbo",
      "Por la primera palabra",
      "Por el final"
    ],
    "m": "El verbo organiza todo: a partir de él se pregunta quién y qué."
  },
  {
    "q": "En «Los tres perros del vecino ladraron», ¿cuál es el núcleo del sujeto?",
    "ops": [
      "perros",
      "vecino",
      "tres"
    ],
    "m": "Los otros lo acompañan: «tres» y «del vecino» modifican a «perros»."
  },
  {
    "q": "En «Le compré un regalo», ¿qué falta explicitar?",
    "ops": [
      "El objeto indirecto: a quién",
      "El objeto directo",
      "El sujeto"
    ],
    "m": "El «le» anticipa un OI que la oración no nombra."
  }
];
GAMES.analisis_sintactico_7 = juegoTriviaTexto(CUR_ANALISIS_SINTACTICO_7_BANCO, "Identificá la función de cada parte.", "analisis_s");

/* 7° · Cazador de errores — ortografia_7
   DC: Tildación; reglas de b/v, g/j y h; homófonos
   Fuente: docs/auditoria-dc-caba/grado-7.md · L14 */
const CUR_ORTOGRAFIA_7_BANCO = [
  {
    "q": "«Espero que ___ suerte.» ¿Qué va?",
    "ops": [
      "haya",
      "halla",
      "aya"
    ],
    "m": "«Haya» es del verbo haber; «halla» es de hallar, encontrar."
  },
  {
    "q": "«Ojalá ___ la salida.» ¿Qué va?",
    "ops": [
      "halle",
      "haya",
      "aye"
    ],
    "m": "Acá sí es encontrar: viene de hallar."
  },
  {
    "q": "«Ya está ___ el trabajo.» ¿Qué va?",
    "ops": [
      "hecho",
      "echo",
      "hexo"
    ],
    "m": "«Hecho» viene de hacer; «echo» de echar, tirar."
  },
  {
    "q": "«Yo ___ sal a la comida.» ¿Qué va?",
    "ops": [
      "echo",
      "hecho",
      "hecho de"
    ],
    "m": "Echar es agregar o tirar: va sin h."
  },
  {
    "q": "¿Cómo se escribe el condicional del verbo haber?",
    "ops": [
      "hubiera",
      "ubiera",
      "huviera"
    ],
    "m": "Del verbo haber: lleva h y v."
  },
  {
    "q": "¿Cómo se escribe el pretérito de «estar»?",
    "ops": [
      "estuvo",
      "estubo",
      "hestuvo"
    ],
    "m": "Los pretéritos de andar, estar y tener llevan v: anduvo, estuvo, tuvo."
  },
  {
    "q": "¿Cómo se escribe el infinitivo de «dirijo»?",
    "ops": [
      "dirigir",
      "diriguir",
      "dirijir"
    ],
    "m": "Los verbos terminados en -gir van con g."
  },
  {
    "q": "¿Cómo se escribe el pretérito de «decir» en plural?",
    "ops": [
      "dijeron",
      "digeron",
      "dijieron"
    ],
    "m": "Del verbo decir: la j se mantiene en el pretérito."
  },
  {
    "q": "¿Cómo se escribe «agotadísimo» con x?",
    "ops": [
      "exhausto",
      "exausto",
      "eshausto"
    ],
    "m": "Lleva h intercalada después del prefijo ex-."
  },
  {
    "q": "¿Cómo se escribe lo que no está permitido?",
    "ops": [
      "prohibido",
      "proibido",
      "proivido"
    ],
    "m": "Lleva h intercalada y b."
  },
  {
    "q": "«Se cayó del árbol» o «se calló del árbol»: ¿cuál corresponde?",
    "ops": [
      "Se cayó, de caer",
      "Se calló, de callar",
      "Las dos"
    ],
    "m": "«Callar» es dejar de hablar: no aplica a un árbol."
  },
  {
    "q": "¿Cómo se escribe la expresión que anuncia que vas a mirar algo?",
    "ops": [
      "a ver qué pasa",
      "haber qué pasa",
      "aver qué pasa"
    ],
    "m": "«A ver» es preposición más verbo ver; «haber» es el infinitivo."
  },
  {
    "q": "¿Cómo se escribe la proporción de cada cien?",
    "ops": [
      "porcentaje",
      "porsentaje",
      "porcentage"
    ],
    "m": "Las palabras terminadas en -aje van con j."
  },
  {
    "q": "¿Cómo se escribe el sustantivo derivado de «conducir»?",
    "ops": [
      "conducción",
      "conduczión",
      "conduxión"
    ],
    "m": "Los sustantivos terminados en -ción derivados de verbos en -cir llevan cc."
  },
  {
    "q": "«Sí, quiero» o «si, quiero»: ¿cuál va?",
    "ops": [
      "Sí, con tilde",
      "Si, sin tilde",
      "Da igual"
    ],
    "m": "El «sí» afirmativo lleva tilde diacrítica; el condicional no."
  },
  {
    "q": "¿Cómo se escribe lo contrario de fracaso?",
    "ops": [
      "éxito",
      "exito",
      "écsito"
    ],
    "m": "Es esdrújula: lleva tilde siempre."
  }
];
GAMES.ortografia_7 = juegoTriviaTexto(CUR_ORTOGRAFIA_7_BANCO, "¿Cuál está bien escrita?", "ortografia");

/* 7° · Leé y deducí — leer_deducir_7
   DC: Comprensión de texto largo con inferencia e intención del autor
   Fuente: docs/auditoria-dc-caba/grado-7.md · L15 */
const CUR_LEER_DEDUCIR_7_BANCO = [
  {
    "q": "«La fábrica cerró en 1998. Diez años después, la mitad del pueblo se había ido.» ¿Qué se deduce?",
    "ops": [
      "El cierre provocó la emigración",
      "La gente se fue por el clima",
      "El pueblo creció"
    ],
    "m": "El texto pone los dos hechos juntos: la relación es lo que hay que inferir."
  },
  {
    "q": "«El autor dedica tres páginas a los riesgos y dos líneas a los beneficios.» ¿Qué revela?",
    "ops": [
      "Que su postura es crítica",
      "Que es neutral",
      "Que está a favor"
    ],
    "m": "Cuánto espacio le da a cada cosa muestra su intención."
  },
  {
    "q": "«Aunque el informe reconoce avances, insiste en que son insuficientes.» ¿Cuál es la postura?",
    "ops": [
      "Crítica, con reconocimiento parcial",
      "Totalmente favorable",
      "Totalmente indiferente"
    ],
    "m": "El «aunque» concede algo antes de sostener lo principal."
  },
  {
    "q": "Si un texto usa «lamentablemente» y «afortunadamente», ¿qué muestra?",
    "ops": [
      "Que el autor valora lo que cuenta",
      "Que es un texto científico neutral",
      "Que hay un error de estilo"
    ],
    "m": "Los adverbios valorativos delatan la subjetividad del emisor."
  },
  {
    "q": "«Los datos no permiten concluir todavía.» ¿Qué actitud expresa el autor?",
    "ops": [
      "Prudencia ante la evidencia",
      "Certeza total",
      "Rechazo del tema"
    ],
    "m": "El «todavía» deja abierta la posibilidad de una conclusión futura."
  },
  {
    "q": "¿Qué es la intención del autor?",
    "ops": [
      "Para qué escribió el texto",
      "Cuánto tardó en escribirlo",
      "De qué trata"
    ],
    "m": "«De qué trata» es el tema; la intención es informar, convencer, emocionar…"
  },
  {
    "q": "Un texto que enumera ventajas y desventajas sin cerrar, ¿qué busca?",
    "ops": [
      "Que el lector se forme su propia opinión",
      "Convencer de una postura",
      "Divertir"
    ],
    "m": "Presentar las dos caras sin conclusión es una decisión del autor."
  },
  {
    "q": "«El proyecto costó tres veces lo presupuestado y se entregó con dos años de atraso.» ¿Qué se deduce?",
    "ops": [
      "Hubo problemas serios de gestión",
      "Fue un éxito rotundo",
      "El presupuesto era generoso"
    ],
    "m": "Los dos datos apuntan en la misma dirección."
  },
  {
    "q": "«Nadie de los consultados quiso dar su nombre.» ¿Qué sugiere?",
    "ops": [
      "Que temían alguna consecuencia",
      "Que eran tímidos",
      "Que no sabían del tema"
    ],
    "m": "El anonimato colectivo apunta a un riesgo compartido."
  },
  {
    "q": "Si un texto cita sólo a quienes están de acuerdo con él, ¿qué falla?",
    "ops": [
      "No contrasta posturas: es parcial",
      "Es demasiado largo",
      "Le falta título"
    ],
    "m": "Elegir las fuentes es también una forma de argumentar."
  },
  {
    "q": "«Las clases se suspendieron por el temporal. Las pruebas se pasaron a la semana siguiente.» ¿Qué relación hay?",
    "ops": [
      "Causa y consecuencia",
      "Contraste",
      "Ninguna"
    ],
    "m": "Lo segundo se explica por lo primero, aunque no haya un conector que lo diga."
  },
  {
    "q": "¿Qué diferencia hay entre lo que un texto DICE y lo que SUGIERE?",
    "ops": [
      "Lo que sugiere se deduce de las pistas, no está escrito",
      "Son lo mismo",
      "Lo que sugiere es siempre falso"
    ],
    "m": "Inferir es apoyarse en el texto, no inventar."
  },
  {
    "q": "«Un informe encargado por la propia empresa concluye que no hubo contaminación.» ¿Qué conviene notar?",
    "ops": [
      "Quién lo encargó puede afectar la conclusión",
      "Que es definitivo",
      "Que no importa el emisor"
    ],
    "m": "Identificar al emisor y su interés es parte de leer críticamente."
  },
  {
    "q": "Un párrafo que empieza con «Sin embargo» anuncia…",
    "ops": [
      "Que viene algo que contrasta con lo anterior",
      "Un ejemplo",
      "Una conclusión"
    ],
    "m": "El conector avisa la relación antes de que la leas."
  }
];
GAMES.leer_deducir_7 = juegoTriviaTexto(CUR_LEER_DEDUCIR_7_BANCO, "Leé el texto y pensá qué quiso decir.", "leer_deduc");

/* 7° · Vocabulario en inglés — ingles_vocabulario_7
   DC: Inglés: campos léxicos de 7°
   Fuente: docs/auditoria-dc-caba/grado-7.md · IN1 */
const CUR_INGLES_VOCABULARIO_7_BANCO = [
  {
    "q": "«Library» significa…",
    "ops": [
      "Biblioteca",
      "Librería",
      "Libro"
    ],
    "m": "Es un falso amigo: la librería es «bookshop» o «bookstore»."
  },
  {
    "q": "«Actually» significa…",
    "ops": [
      "En realidad",
      "Actualmente",
      "Activamente"
    ],
    "m": "Otro falso amigo: «actualmente» se dice «currently»."
  },
  {
    "q": "«Embarrassed» significa…",
    "ops": [
      "Avergonzado",
      "Embarazada",
      "Enojado"
    ],
    "m": "Falso amigo clásico: embarazada es «pregnant»."
  },
  {
    "q": "«Weather» significa…",
    "ops": [
      "El tiempo atmosférico",
      "El tiempo del reloj",
      "El clima de un país"
    ],
    "m": "El tiempo del reloj es «time»; el clima de una región, «climate»."
  },
  {
    "q": "«To attend» significa…",
    "ops": [
      "Asistir a",
      "Atender a alguien",
      "Esperar"
    ],
    "m": "Atender a un cliente es «to serve»."
  },
  {
    "q": "«Carpet» significa…",
    "ops": [
      "Alfombra",
      "Carpeta",
      "Cartera"
    ],
    "m": "Carpeta es «folder»."
  },
  {
    "q": "«Exit» significa…",
    "ops": [
      "Salida",
      "Éxito",
      "Extra"
    ],
    "m": "Éxito es «success»."
  },
  {
    "q": "«Homework» significa…",
    "ops": [
      "Tarea escolar",
      "Trabajo en casa",
      "Casa de trabajo"
    ],
    "m": "Se refiere específicamente a la tarea de la escuela."
  },
  {
    "q": "«Neighbour» significa…",
    "ops": [
      "Vecino",
      "Ni uno ni otro",
      "Sobrino"
    ],
    "m": "Sobrino es «nephew»."
  },
  {
    "q": "«To realize» significa…",
    "ops": [
      "Darse cuenta",
      "Realizar una tarea",
      "Alquilar"
    ],
    "m": "Realizar una tarea es «to carry out» o «to do»."
  },
  {
    "q": "«Notice» significa…",
    "ops": [
      "Aviso o notar",
      "Noticia",
      "Nota escolar"
    ],
    "m": "Noticia es «news»; la nota escolar, «mark» o «grade»."
  },
  {
    "q": "«Sensible» significa…",
    "ops": [
      "Sensato",
      "Sensible",
      "Simple"
    ],
    "m": "Sensible se dice «sensitive»."
  },
  {
    "q": "«To support» significa…",
    "ops": [
      "Apoyar",
      "Soportar algo molesto",
      "Suponer"
    ],
    "m": "Soportar algo molesto es «to put up with»."
  },
  {
    "q": "«Grocery store» es…",
    "ops": [
      "Un almacén de comida",
      "Una tienda de ropa",
      "Una ferretería"
    ],
    "m": "«Grocery» son los comestibles."
  },
  {
    "q": "«Journey» significa…",
    "ops": [
      "Viaje",
      "Jornada laboral",
      "Diario"
    ],
    "m": "La jornada es «working day»; el diario, «newspaper»."
  }
];
GAMES.ingles_vocabulario_7 = juegoTriviaTexto(CUR_INGLES_VOCABULARIO_7_BANCO, "¿Qué significa?", "ingles_voc");

/* 7° · Verbos en inglés — ingles_verbos_7
   DC: Inglés: present simple, past simple y verbos irregulares
   Fuente: docs/auditoria-dc-caba/grado-7.md · IN2 */
const CUR_INGLES_VERBOS_7_BANCO = [
  {
    "q": "«She ___ to school every day.»",
    "ops": [
      "goes",
      "go",
      "gone"
    ],
    "m": "Tercera persona del singular en present simple: lleva -es."
  },
  {
    "q": "«They ___ football on Sundays.»",
    "ops": [
      "play",
      "plays",
      "played"
    ],
    "m": "«They» es plural: el verbo va sin -s."
  },
  {
    "q": "«I ___ to the cinema yesterday.»",
    "ops": [
      "went",
      "go",
      "goes"
    ],
    "m": "«Yesterday» pide past simple, y «go» es irregular: went."
  },
  {
    "q": "«We ___ pizza last night.»",
    "ops": [
      "ate",
      "eat",
      "eaten"
    ],
    "m": "Past simple de «eat» es «ate»; «eaten» es el participio."
  },
  {
    "q": "¿Cuál es el past simple de «buy»?",
    "ops": [
      "bought",
      "buyed",
      "buied"
    ],
    "m": "Es irregular: no lleva -ed."
  },
  {
    "q": "¿Cuál es el past simple de «work»?",
    "ops": [
      "worked",
      "wrought",
      "workt"
    ],
    "m": "Es regular: se le agrega -ed."
  },
  {
    "q": "«He ___ TV every evening.»",
    "ops": [
      "watches",
      "watch",
      "watched"
    ],
    "m": "Los verbos terminados en -ch agregan -es en tercera persona."
  },
  {
    "q": "«Did you ___ the film?»",
    "ops": [
      "see",
      "saw",
      "seen"
    ],
    "m": "Después de «did» el verbo va en infinitivo, sin marca de pasado."
  },
  {
    "q": "«She ___ not like coffee.»",
    "ops": [
      "does",
      "do",
      "did"
    ],
    "m": "Tercera persona en presente: el auxiliar es «does»."
  },
  {
    "q": "¿Cuál es el past simple de «have»?",
    "ops": [
      "had",
      "haved",
      "has"
    ],
    "m": "Es irregular."
  },
  {
    "q": "«They ___ in Buenos Aires in 2010.»",
    "ops": [
      "lived",
      "live",
      "living"
    ],
    "m": "Una fecha del pasado pide past simple; «live» es regular."
  },
  {
    "q": "¿Cuál es el past simple de «make»?",
    "ops": [
      "made",
      "maked",
      "make"
    ],
    "m": "Es irregular."
  },
  {
    "q": "«I ___ my homework every day.»",
    "ops": [
      "do",
      "does",
      "did"
    ],
    "m": "«I» no lleva -s en present simple."
  },
  {
    "q": "¿Cuál es el past simple de «take»?",
    "ops": [
      "took",
      "taked",
      "taken"
    ],
    "m": "Irregular. «Taken» es el participio."
  },
  {
    "q": "«She ___ born in 2012.»",
    "ops": [
      "was",
      "were",
      "is"
    ],
    "m": "Tercera persona del singular en pasado del verbo «to be»."
  }
];
GAMES.ingles_verbos_7 = juegoTriviaTexto(CUR_INGLES_VERBOS_7_BANCO, "Elegí la forma correcta.", "ingles_ver");

/* 7° · Leé en inglés — ingles_lectura_7
   DC: Inglés: comprensión lectora en lengua extranjera
   Fuente: docs/auditoria-dc-caba/grado-7.md · IN3 */
const CUR_INGLES_LECTURA_7_BANCO = [
  {
    "q": "«Tom wakes up at 7. He has breakfast and takes the bus to school.» ¿Cómo va a la escuela?",
    "ops": [
      "En colectivo",
      "Caminando",
      "En bicicleta"
    ],
    "m": "«Takes the bus» es toma el colectivo."
  },
  {
    "q": "«The museum is closed on Mondays.» ¿Cuándo NO se puede visitar?",
    "ops": [
      "Los lunes",
      "Los domingos",
      "Todos los días"
    ],
    "m": "«Closed» es cerrado; «Mondays» son los lunes."
  },
  {
    "q": "«Anna is afraid of dogs.» ¿Qué le pasa a Anna?",
    "ops": [
      "Les tiene miedo a los perros",
      "Le gustan los perros",
      "Tiene un perro"
    ],
    "m": "«Afraid of» significa tener miedo de algo."
  },
  {
    "q": "«It was raining, so we stayed at home.» ¿Por qué se quedaron en casa?",
    "ops": [
      "Porque llovía",
      "Porque hacía calor",
      "Porque estaban cansados"
    ],
    "m": "«So» introduce la consecuencia de lo anterior."
  },
  {
    "q": "«The shop opens at 9 and closes at 6.» ¿Cuántas horas está abierto?",
    "ops": [
      "Nueve",
      "Seis",
      "Tres"
    ],
    "m": "De 9 a 18 hay nueve horas."
  },
  {
    "q": "«My sister doesn't eat meat.» ¿Qué se deduce?",
    "ops": [
      "Probablemente es vegetariana",
      "Le encanta la carne",
      "Come carne los domingos"
    ],
    "m": "«Doesn't eat» es no come."
  },
  {
    "q": "«Please, do not feed the animals.» ¿Qué pide el cartel?",
    "ops": [
      "Que no les des de comer a los animales",
      "Que les des de comer",
      "Que no toques a los animales"
    ],
    "m": "«Feed» es alimentar."
  },
  {
    "q": "«She has lived in Córdoba since 2015.» ¿Sigue viviendo ahí?",
    "ops": [
      "Sí, desde 2015 hasta ahora",
      "No, se mudó en 2015",
      "Vivió sólo un año"
    ],
    "m": "«Since» marca el comienzo de algo que continúa."
  },
  {
    "q": "«Turn left at the corner and then go straight.» ¿Qué te están dando?",
    "ops": [
      "Indicaciones para llegar a un lugar",
      "Una receta",
      "Una advertencia"
    ],
    "m": "«Turn left» y «go straight» son instrucciones de dirección."
  },
  {
    "q": "«The test was easier than I expected.» ¿Cómo resultó la prueba?",
    "ops": [
      "Más fácil de lo que pensaba",
      "Más difícil",
      "Igual que siempre"
    ],
    "m": "«Easier than» es más fácil que."
  },
  {
    "q": "«We're going to travel next summer.» ¿Cuándo viajan?",
    "ops": [
      "El verano que viene",
      "El verano pasado",
      "Ahora mismo"
    ],
    "m": "«Next» es próximo; «last» sería pasado."
  },
  {
    "q": "«He couldn't come because he was ill.» ¿Por qué no vino?",
    "ops": [
      "Porque estaba enfermo",
      "Porque no quiso",
      "Porque llegó tarde"
    ],
    "m": "«Ill» significa enfermo."
  },
  {
    "q": "«There are no tickets left.» ¿Qué significa?",
    "ops": [
      "Se agotaron las entradas",
      "Quedan entradas a la izquierda",
      "Las entradas son gratis"
    ],
    "m": "«Left» acá es lo que queda, no la izquierda."
  },
  {
    "q": "Si no entendés una palabra de un texto en inglés, ¿qué conviene?",
    "ops": [
      "Deducirla por el contexto y seguir leyendo",
      "Frenar hasta buscarla",
      "Abandonar el texto"
    ],
    "m": "La comprensión global no exige entender cada palabra."
  }
];
GAMES.ingles_lectura_7 = juegoTriviaTexto(CUR_INGLES_LECTURA_7_BANCO, "Leé el texto corto y respondé.", "ingles_lec");

/* 7° · Constructor de redes tróficas — redes_troficas_7
   DC: Cadenas y redes tróficas; roles en el ecosistema
   Fuente: docs/auditoria-dc-caba/grado-7.md · CN1 */
const CUR_REDES_TROFICAS_7_BANCO = [
  {
    "it": "El fitoplancton del océano",
    "cat": "productor",
    "m": "Hace fotosíntesis: es la base de casi toda la red marina."
  },
  {
    "it": "La anchoíta que se alimenta de plancton",
    "cat": "consumidor",
    "m": "Consumidor de primer orden."
  },
  {
    "it": "Las bacterias que degradan un pez muerto",
    "cat": "descomponedor",
    "m": "Devuelven los nutrientes al agua."
  },
  {
    "it": "El alga marina",
    "cat": "productor",
    "m": "Tiene clorofila y produce su alimento."
  },
  {
    "it": "El lobo marino que come peces",
    "cat": "consumidor",
    "m": "Obtiene la energía de otros seres vivos."
  },
  {
    "it": "Los hongos del suelo del bosque",
    "cat": "descomponedor",
    "m": "Transforman la materia muerta en nutrientes disponibles."
  },
  {
    "it": "El pastizal de la pampa",
    "cat": "productor",
    "m": "Convierte luz en materia orgánica."
  },
  {
    "it": "El zorro que caza roedores",
    "cat": "consumidor",
    "m": "Consumidor de segundo o tercer orden."
  },
  {
    "it": "Las lombrices que procesan hojarasca",
    "cat": "descomponedor",
    "m": "Fragmentan la materia muerta y la incorporan al suelo."
  },
  {
    "it": "El musgo sobre la roca húmeda",
    "cat": "productor",
    "m": "Es una planta: hace fotosíntesis."
  },
  {
    "it": "El puma",
    "cat": "consumidor",
    "m": "Depredador tope: sigue siendo consumidor."
  },
  {
    "it": "El moho sobre la fruta olvidada",
    "cat": "descomponedor",
    "m": "Un hongo que se alimenta de materia ya elaborada."
  },
  {
    "it": "La cianobacteria fotosintética",
    "cat": "productor",
    "m": "Aunque sea bacteria, hace fotosíntesis: produce."
  },
  {
    "it": "El carancho que come animales muertos",
    "cat": "consumidor",
    "m": "Es carroñero, pero no descompone la materia químicamente."
  },
  {
    "it": "Las bacterias que fijan nitrógeno en las raíces",
    "cat": "descomponedor",
    "m": "Participan del reciclado de materia en el suelo."
  },
  {
    "it": "El helecho del sotobosque",
    "cat": "productor",
    "m": "Planta con clorofila."
  }
];
GAMES.redes_troficas_7 = juegoClasificar(CUR_REDES_TROFICAS_7_BANCO, "¿Qué rol cumple en la red?", [{"cat": "productor", "label": "🌱 Productor"}, {"cat": "consumidor", "label": "🦊 Consumidor"}, {"cat": "descomponedor", "label": "🍄 Descomponedor"}], "redes_trof");

/* 7° · Flujo de energía y reciclaje — flujo_energia_7
   DC: Flujo de energía; la energía disminuye en cada nivel trófico
   Fuente: docs/auditoria-dc-caba/grado-7.md · CN2 */
const CUR_FLUJO_ENERGIA_7_BANCO = [
  {
    "q": "¿De dónde entra la energía a casi todos los ecosistemas?",
    "ops": [
      "Del Sol, por la fotosíntesis",
      "Del suelo",
      "De los descomponedores"
    ],
    "m": "Del suelo se toman nutrientes, no energía."
  },
  {
    "q": "¿Qué le pasa a la energía al pasar de un nivel al siguiente?",
    "ops": [
      "Se pierde una gran parte como calor",
      "Se multiplica",
      "Se mantiene igual"
    ],
    "m": "Sólo una fracción chica llega al nivel de arriba."
  },
  {
    "q": "¿Por qué hay muchas más plantas que grandes carnívoros?",
    "ops": [
      "Porque la energía disponible se achica en cada nivel",
      "Porque los carnívoros comen poco",
      "Por el clima"
    ],
    "m": "La pirámide de energía explica la pirámide de números."
  },
  {
    "q": "¿La materia también se pierde en cada nivel?",
    "ops": [
      "No: la materia se recicla gracias a los descomponedores",
      "Sí, igual que la energía",
      "Sí, más que la energía"
    ],
    "m": "Ésa es la diferencia clave: la energía FLUYE, la materia CICLA."
  },
  {
    "q": "¿Hacia dónde apuntan las flechas de una cadena alimentaria?",
    "ops": [
      "Hacia el que come",
      "Hacia el que es comido",
      "Hacia los dos lados"
    ],
    "m": "Indican el sentido en que fluye la energía."
  },
  {
    "q": "¿Qué pasaría si desaparecieran todos los descomponedores?",
    "ops": [
      "Los nutrientes quedarían atrapados en la materia muerta",
      "No pasaría nada",
      "Habría más energía disponible"
    ],
    "m": "El ciclo de la materia se cortaría."
  },
  {
    "q": "¿Aproximadamente cuánta energía pasa de un nivel al siguiente?",
    "ops": [
      "Alrededor del 10%",
      "Casi el 100%",
      "Alrededor del 90%"
    ],
    "m": "El resto se usa en respirar, moverse y se disipa como calor."
  },
  {
    "q": "¿Qué es un nivel trófico?",
    "ops": [
      "El escalón que ocupa un ser vivo en la cadena",
      "Un tipo de ecosistema",
      "Una especie"
    ],
    "m": "Productores, consumidores de primer orden, de segundo…"
  },
  {
    "q": "¿Puede un animal ocupar más de un nivel trófico?",
    "ops": [
      "Sí, si come plantas y animales",
      "No, nunca",
      "Sólo los descomponedores"
    ],
    "m": "Los omnívoros son el ejemplo típico."
  },
  {
    "q": "¿Por qué las cadenas alimentarias suelen tener pocos eslabones?",
    "ops": [
      "Porque la energía se agota",
      "Porque no hay suficientes especies",
      "Por el tamaño de los animales"
    ],
    "m": "Después de cuatro o cinco niveles ya casi no queda energía."
  },
  {
    "q": "¿Es correcto decir que la energía «se gasta»?",
    "ops": [
      "Se transforma y se degrada como calor, no desaparece",
      "Sí, desaparece",
      "No, se conserva intacta"
    ],
    "m": "La energía se conserva, pero se degrada a formas menos útiles."
  },
  {
    "q": "Los descomponedores, ¿aportan energía a los niveles superiores?",
    "ops": [
      "Aportan materia; la energía ya se degradó",
      "Sí, devuelven toda la energía",
      "No hacen nada"
    ],
    "m": "Cierran el ciclo de la materia, no el de la energía."
  },
  {
    "q": "En una pirámide de energía, ¿dónde está el escalón más ancho?",
    "ops": [
      "En la base, con los productores",
      "En la punta",
      "En el medio"
    ],
    "m": "Es donde hay más energía disponible."
  },
  {
    "q": "¿Qué diferencia hay entre cadena y red trófica?",
    "ops": [
      "La red muestra que cada especie come de varias fuentes",
      "Son sinónimos",
      "La cadena es más grande"
    ],
    "m": "La red es más realista: casi ningún animal come una sola cosa."
  }
];
GAMES.flujo_energia_7 = juegoTriviaTexto(CUR_FLUJO_ENERGIA_7_BANCO, "Seguí la energía por la cadena.", "flujo_ener");

/* 7° · Sucesión ecológica — sucesion_ecologica_7
   DC: Sucesión tras un disturbio; efecto en cascada de una especie
   Fuente: docs/auditoria-dc-caba/grado-7.md · CN3 */
const CUR_SUCESION_ECOLOGICA_7_BANCO = [
  {
    "q": "¿Qué es una sucesión ecológica?",
    "ops": [
      "El cambio ordenado de las comunidades de un lugar a lo largo del tiempo",
      "La migración de una especie",
      "Una cadena alimentaria"
    ],
    "m": "No es un cambio al azar: sigue etapas reconocibles."
  },
  {
    "q": "Después de un incendio, ¿qué aparece primero?",
    "ops": [
      "Pastos y hierbas de crecimiento rápido",
      "Árboles grandes",
      "Los grandes mamíferos"
    ],
    "m": "Las especies pioneras son las que colonizan primero."
  },
  {
    "q": "¿Qué son las especies pioneras?",
    "ops": [
      "Las primeras en colonizar un ambiente alterado",
      "Las que llegan al final",
      "Las más grandes"
    ],
    "m": "Toleran condiciones duras y preparan el suelo para las siguientes."
  },
  {
    "q": "¿Qué es la comunidad clímax?",
    "ops": [
      "La etapa final y estable de la sucesión",
      "La primera etapa",
      "El momento del incendio"
    ],
    "m": "Es la comunidad que se mantiene si no hay nuevos disturbios."
  },
  {
    "q": "Si se elimina al depredador tope de un ecosistema, ¿qué suele pasar?",
    "ops": [
      "Sus presas se multiplican y afectan al resto",
      "No cambia nada",
      "Se extingue todo"
    ],
    "m": "Eso es un efecto en cascada: el impacto se propaga por la red."
  },
  {
    "q": "¿Qué es una especie exótica invasora?",
    "ops": [
      "Una traída de otro lugar que se expande y desplaza a las nativas",
      "Una especie muy rara",
      "Una que está en peligro"
    ],
    "m": "Sin sus depredadores naturales, puede crecer sin control."
  },
  {
    "q": "El castor introducido en Tierra del Fuego es un ejemplo de…",
    "ops": [
      "Especie invasora que transformó el ambiente",
      "Especie pionera nativa",
      "Comunidad clímax"
    ],
    "m": "Sus diques inundaron bosques que no se regeneran."
  },
  {
    "q": "¿Qué es un disturbio ecológico?",
    "ops": [
      "Un evento que altera la comunidad, como un incendio o una tala",
      "Un cambio de estación",
      "La llegada de la noche"
    ],
    "m": "Puede ser natural o provocado por la actividad humana."
  },
  {
    "q": "¿La sucesión ocurre siempre a la misma velocidad?",
    "ops": [
      "No: depende del clima, el suelo y el disturbio",
      "Sí, siempre igual",
      "Sólo en los bosques"
    ],
    "m": "Un bosque puede tardar décadas; un pastizal, pocos años."
  },
  {
    "q": "¿Qué es la sucesión primaria?",
    "ops": [
      "La que empieza donde no había suelo, como en una roca desnuda",
      "La que sigue a un incendio",
      "La más rápida"
    ],
    "m": "La que empieza con suelo ya formado es secundaria y va más rápido."
  },
  {
    "q": "¿Por qué la biodiversidad aumenta durante la sucesión?",
    "ops": [
      "Porque cada etapa crea condiciones para nuevas especies",
      "Porque llegan más animales de golpe",
      "No aumenta"
    ],
    "m": "Las pioneras modifican el ambiente y lo hacen habitable para otras."
  },
  {
    "q": "¿Qué pasa si se introduce una especie sin depredadores naturales?",
    "ops": [
      "Puede crecer sin control y desplazar a las nativas",
      "Se extingue rápido",
      "Se equilibra sola"
    ],
    "m": "Es lo que convierte a una exótica en invasora."
  },
  {
    "q": "Un pastizal que se abandona y con los años se llena de arbustos y árboles muestra…",
    "ops": [
      "Una sucesión secundaria",
      "Una sucesión primaria",
      "Un disturbio"
    ],
    "m": "El suelo ya estaba: por eso avanza relativamente rápido."
  },
  {
    "q": "¿Los seres vivos modifican el ambiente donde viven?",
    "ops": [
      "Sí, y eso es motor de la sucesión",
      "No, sólo se adaptan",
      "Sólo las plantas"
    ],
    "m": "Las pioneras generan suelo y sombra, y así cambian las condiciones."
  }
];
GAMES.sucesion_ecologica_7 = juegoTriviaTexto(CUR_SUCESION_ECOLOGICA_7_BANCO, "Pensá cómo se recupera un ambiente.", "sucesion_e");

/* 7° · Camino del estímulo — sistema_nervioso_7
   DC: Sentidos y sistema nervioso; central y periférico; efectos del alcohol
   Fuente: docs/auditoria-dc-caba/grado-7.md · CN4 */
const CUR_SISTEMA_NERVIOSO_7_BANCO = [
  {
    "q": "¿Cuál es el orden correcto del camino del estímulo?",
    "ops": [
      "Receptor → nervio → centro nervioso → nervio → efector",
      "Efector → receptor → centro",
      "Centro → receptor → efector"
    ],
    "m": "Primero se capta, después se procesa y al final se responde."
  },
  {
    "q": "¿Qué órganos forman el sistema nervioso CENTRAL?",
    "ops": [
      "El encéfalo y la médula espinal",
      "Los nervios de los brazos",
      "Los órganos de los sentidos"
    ],
    "m": "Los nervios que salen de ahí forman el periférico."
  },
  {
    "q": "¿Qué es una neurona?",
    "ops": [
      "La célula que transmite el impulso nervioso",
      "Un órgano del cerebro",
      "Un tipo de músculo"
    ],
    "m": "Es la unidad funcional del sistema nervioso."
  },
  {
    "q": "¿Qué es un acto reflejo?",
    "ops": [
      "Una respuesta rápida que se resuelve en la médula",
      "Una decisión pensada",
      "Un movimiento voluntario"
    ],
    "m": "No pasa por el cerebro: por eso es tan rápido."
  },
  {
    "q": "Sacar la mano de algo caliente antes de darse cuenta es…",
    "ops": [
      "Un acto reflejo",
      "Un acto voluntario",
      "Un error del sistema"
    ],
    "m": "La médula responde antes de que el cerebro procese el dolor."
  },
  {
    "q": "¿Qué es un receptor?",
    "ops": [
      "La estructura que capta el estímulo",
      "El músculo que responde",
      "El nervio que transmite"
    ],
    "m": "Están en los órganos de los sentidos y en la piel."
  },
  {
    "q": "¿Qué es un efector?",
    "ops": [
      "El músculo o la glándula que ejecuta la respuesta",
      "El que capta el estímulo",
      "El centro nervioso"
    ],
    "m": "Es el que produce el movimiento o la secreción."
  },
  {
    "q": "¿Cómo afecta el alcohol al sistema nervioso?",
    "ops": [
      "Lo deprime: enlentece los reflejos y el juicio",
      "Lo estimula y mejora los reflejos",
      "No lo afecta"
    ],
    "m": "La sensación inicial de desinhibición engaña: es un depresor."
  },
  {
    "q": "¿Por qué el alcohol y conducir son incompatibles?",
    "ops": [
      "Porque alarga el tiempo de reacción",
      "Porque da sueño solamente",
      "Porque afecta la vista nada más"
    ],
    "m": "Unos décimos de segundo más de reacción son metros de más de frenado."
  },
  {
    "q": "¿Qué es la sinapsis?",
    "ops": [
      "La conexión por la que pasa el impulso entre neuronas",
      "El núcleo de la neurona",
      "Un tipo de nervio"
    ],
    "m": "Es donde se transmite la señal de una neurona a la siguiente."
  },
  {
    "q": "¿Qué parte del encéfalo coordina el equilibrio y los movimientos finos?",
    "ops": [
      "El cerebelo",
      "El bulbo raquídeo",
      "La médula espinal"
    ],
    "m": "El bulbo controla funciones automáticas como respirar."
  },
  {
    "q": "¿Qué controla el bulbo raquídeo?",
    "ops": [
      "Funciones automáticas como respirar y el latido",
      "El pensamiento",
      "El equilibrio"
    ],
    "m": "Por eso es una zona vital."
  },
  {
    "q": "¿El sistema nervioso trabaja solo o con otros sistemas?",
    "ops": [
      "Con otros, sobre todo con el endocrino",
      "Solo, siempre",
      "Sólo con el muscular"
    ],
    "m": "Nervioso y endocrino coordinan juntos el funcionamiento del cuerpo."
  },
  {
    "q": "¿Qué pasa con el tiempo de reacción cuando alguien está cansado?",
    "ops": [
      "Se alarga",
      "Se acorta",
      "No cambia"
    ],
    "m": "El cansancio afecta al sistema nervioso igual que otras sustancias."
  }
];
GAMES.sistema_nervioso_7 = juegoTriviaTexto(CUR_SISTEMA_NERVIOSO_7_BANCO, "Seguí el recorrido del estímulo a la respuesta.", "sistema_ne");

/* 7° · Barreras y defensas — inmune_7
   DC: Defensa inespecífica y específica; respuesta primaria y secundaria
   Fuente: docs/auditoria-dc-caba/grado-7.md · CN5 */
const CUR_INMUNE_7_BANCO = [
  {
    "q": "¿Cuál es la primera barrera de defensa del cuerpo?",
    "ops": [
      "La piel y las mucosas",
      "Los anticuerpos",
      "Los linfocitos"
    ],
    "m": "Es una barrera física: impide la entrada."
  },
  {
    "q": "¿Qué es una defensa INESPECÍFICA?",
    "ops": [
      "La que actúa igual contra cualquier invasor",
      "La que ataca a uno solo",
      "La que da la vacuna"
    ],
    "m": "La piel, la fiebre y la inflamación no distinguen de qué microbio se trata."
  },
  {
    "q": "¿Qué es una defensa ESPECÍFICA?",
    "ops": [
      "La que reconoce y ataca a un invasor puntual",
      "La barrera de la piel",
      "La fiebre"
    ],
    "m": "Los anticuerpos se fabrican a medida de cada antígeno."
  },
  {
    "q": "¿Qué es un anticuerpo?",
    "ops": [
      "Una proteína que reconoce a un invasor específico",
      "Un tipo de virus",
      "Una célula de la piel"
    ],
    "m": "Se produce después del contacto con el antígeno."
  },
  {
    "q": "¿Por qué la segunda vez que aparece el mismo microbio la respuesta es más rápida?",
    "ops": [
      "Porque hay células de memoria",
      "Porque el microbio es más débil",
      "Porque la piel se hizo más gruesa"
    ],
    "m": "Ésa es la base de cómo funcionan las vacunas."
  },
  {
    "q": "¿Para qué sirve la fiebre?",
    "ops": [
      "Dificulta la reproducción de los microbios",
      "Es sólo un síntoma inútil",
      "Enfría el cuerpo"
    ],
    "m": "Es parte de la respuesta, aunque haya que controlarla si sube demasiado."
  },
  {
    "q": "¿Qué es la inflamación?",
    "ops": [
      "Una respuesta que lleva más defensas a la zona afectada",
      "Una infección",
      "Un daño permanente"
    ],
    "m": "El enrojecimiento y el calor vienen del aumento de la circulación."
  },
  {
    "q": "¿Los antibióticos sirven contra los virus?",
    "ops": [
      "No: actúan sobre las bacterias",
      "Sí, contra todos",
      "Sí, si la dosis es alta"
    ],
    "m": "Tomarlos de más favorece la resistencia bacteriana."
  },
  {
    "q": "¿Qué es un antígeno?",
    "ops": [
      "Una sustancia que el cuerpo reconoce como extraña",
      "Un anticuerpo",
      "Un tipo de glóbulo rojo"
    ],
    "m": "Es lo que dispara la respuesta específica."
  },
  {
    "q": "¿Qué células producen los anticuerpos?",
    "ops": [
      "Los linfocitos",
      "Los glóbulos rojos",
      "Las plaquetas"
    ],
    "m": "Los glóbulos rojos transportan oxígeno; las plaquetas coagulan."
  },
  {
    "q": "El moco de las vías respiratorias, ¿qué función cumple?",
    "ops": [
      "Atrapa partículas y microbios antes de que entren",
      "Sólo molesta",
      "Transporta oxígeno"
    ],
    "m": "Es parte de las barreras inespecíficas."
  },
  {
    "q": "¿Por qué la respuesta secundaria es más intensa?",
    "ops": [
      "Porque el sistema ya reconoce al invasor y reacciona antes",
      "Porque el cuerpo está más débil",
      "Porque hay más microbios"
    ],
    "m": "Las células de memoria acortan el tiempo de reacción."
  },
  {
    "q": "El ácido del estómago, ¿es una defensa?",
    "ops": [
      "Sí, inespecífica: destruye muchos microbios que se tragan",
      "No, sólo digiere",
      "Sólo si hay fiebre"
    ],
    "m": "Es una barrera química."
  },
  {
    "q": "¿Qué es la inmunidad?",
    "ops": [
      "La capacidad de defenderse de un agente al que ya se enfrentó",
      "No enfermarse nunca",
      "Tener fiebre alta"
    ],
    "m": "Se puede adquirir por haber cursado la enfermedad o por vacunación."
  }
];
GAMES.inmune_7 = juegoTriviaTexto(CUR_INMUNE_7_BANCO, "¿Cómo se defiende el cuerpo?", "inmune_7");

/* 7° · Cómo actúa una vacuna — vacunas_7
   DC: Acción de las vacunas; calendario; protección colectiva
   Fuente: docs/auditoria-dc-caba/grado-7.md · CN6 */
const CUR_VACUNAS_7_BANCO = [
  {
    "q": "¿Qué hace una vacuna?",
    "ops": [
      "Entrena al sistema inmune sin producir la enfermedad",
      "Mata a los microbios que ya están",
      "Cura una infección en curso"
    ],
    "m": "Es preventiva: se da ANTES de enfermarse."
  },
  {
    "q": "¿Qué contiene una vacuna?",
    "ops": [
      "El microbio inactivado o una parte de él",
      "Antibióticos",
      "El microbio activo y completo"
    ],
    "m": "Alcanza con que el sistema reconozca al antígeno."
  },
  {
    "q": "¿Por qué algunas vacunas necesitan refuerzos?",
    "ops": [
      "Porque la memoria inmunitaria se va debilitando",
      "Porque la primera dosis falla",
      "Porque el microbio se hace más fuerte"
    ],
    "m": "El refuerzo vuelve a activar las células de memoria."
  },
  {
    "q": "¿Qué es la inmunidad de rebaño o protección colectiva?",
    "ops": [
      "Cuando hay tantos vacunados que el microbio casi no circula",
      "Cuando se vacuna a los animales",
      "Cuando nadie se enferma nunca"
    ],
    "m": "Protege también a quien no puede vacunarse por razones médicas."
  },
  {
    "q": "En la Argentina, las vacunas del calendario son…",
    "ops": [
      "Gratuitas y obligatorias",
      "Pagas",
      "Optativas y pagas"
    ],
    "m": "Es una política de salud pública, no una decisión individual."
  },
  {
    "q": "¿Una vacuna puede darle la enfermedad a la persona?",
    "ops": [
      "No: el microbio está inactivado o incompleto",
      "Sí, siempre",
      "Sí, si es la primera dosis"
    ],
    "m": "Puede haber molestias leves, que no son la enfermedad."
  },
  {
    "q": "¿Por qué se erradicó la viruela?",
    "ops": [
      "Por una campaña mundial de vacunación",
      "Porque el virus mutó",
      "Por casualidad"
    ],
    "m": "Es el único caso de erradicación completa de una enfermedad humana."
  },
  {
    "q": "¿Contra qué protege la vacuna triple viral?",
    "ops": [
      "Sarampión, rubéola y paperas",
      "Gripe, covid y neumonía",
      "Tétanos, difteria y tos convulsa"
    ],
    "m": "La triple bacteriana es la del tétanos, la difteria y la tos convulsa."
  },
  {
    "q": "¿Por qué hay que vacunarse contra la gripe todos los años?",
    "ops": [
      "Porque el virus cambia y la vacuna se actualiza",
      "Porque la vacuna es de mala calidad",
      "Porque el cuerpo la rechaza"
    ],
    "m": "Cada año se prepara con las cepas que se esperan circulando."
  },
  {
    "q": "¿A qué edad se dan la mayoría de las vacunas del calendario?",
    "ops": [
      "Durante los primeros años de vida",
      "Recién en la adultez",
      "Sólo en la adolescencia"
    ],
    "m": "Aunque hay dosis en la adolescencia y en la adultez también."
  },
  {
    "q": "Si alguien no puede vacunarse por una enfermedad, ¿cómo se protege?",
    "ops": [
      "Con la protección colectiva de los que sí se vacunan",
      "No se puede proteger",
      "Tomando antibióticos"
    ],
    "m": "Por eso vacunarse es también un acto de cuidado hacia otros."
  },
  {
    "q": "¿Qué diferencia hay entre vacuna y antibiótico?",
    "ops": [
      "La vacuna previene; el antibiótico trata una infección bacteriana",
      "Son lo mismo",
      "El antibiótico previene y la vacuna cura"
    ],
    "m": "Una actúa antes; el otro, cuando la infección ya está."
  },
  {
    "q": "La vacuna contra el VPH se da…",
    "ops": [
      "En la adolescencia, a todos",
      "Sólo a las mujeres adultas",
      "Al nacer"
    ],
    "m": "Está en el calendario nacional a los 11 años, para todos."
  },
  {
    "q": "¿Qué pasa si baja mucho la cobertura de vacunación de una población?",
    "ops": [
      "Pueden reaparecer enfermedades que estaban controladas",
      "No pasa nada",
      "Mejora la inmunidad natural"
    ],
    "m": "El sarampión volvió a brotar en varios países por esa razón."
  }
];
GAMES.vacunas_7 = juegoTriviaTexto(CUR_VACUNAS_7_BANCO, "Pensá qué hace la vacuna en el cuerpo.", "vacunas_7");

/* 7° · Transformá la energía — transformar_energia_7
   DC: Transformación, conservación y degradación de la energía
   Fuente: docs/auditoria-dc-caba/grado-7.md · CN7 */
const CUR_TRANSFORMAR_ENERGIA_7_BANCO = [
  {
    "q": "En una lamparita, la energía eléctrica se transforma en…",
    "ops": [
      "Luz y calor",
      "Sólo luz",
      "Sólo movimiento"
    ],
    "m": "Parte siempre se degrada como calor: por eso se calienta."
  },
  {
    "q": "En un ventilador, la energía eléctrica se transforma en…",
    "ops": [
      "Movimiento y algo de calor",
      "Sólo luz",
      "Sólo sonido"
    ],
    "m": "El motor convierte electricidad en energía mecánica."
  },
  {
    "q": "¿Qué dice el principio de conservación de la energía?",
    "ops": [
      "No se crea ni se destruye: se transforma",
      "Se gasta y desaparece",
      "Se multiplica al usarla"
    ],
    "m": "Lo que cambia es la FORMA, no la cantidad total."
  },
  {
    "q": "¿Qué significa que la energía se DEGRADA?",
    "ops": [
      "Que se convierte en formas menos aprovechables, como calor disperso",
      "Que desaparece",
      "Que se contamina"
    ],
    "m": "Se conserva la cantidad, pero se pierde la calidad."
  },
  {
    "q": "En una represa hidroeléctrica, ¿qué transformación ocurre?",
    "ops": [
      "Energía del movimiento del agua en energía eléctrica",
      "Energía química en luz",
      "Calor en sonido"
    ],
    "m": "El agua mueve las turbinas, y las turbinas los generadores."
  },
  {
    "q": "En un panel solar, ¿qué se transforma?",
    "ops": [
      "La energía de la radiación solar en eléctrica",
      "Calor en movimiento",
      "Movimiento en luz"
    ],
    "m": "El efecto fotovoltaico convierte luz en corriente."
  },
  {
    "q": "Al comer, ¿qué transformación hace el cuerpo?",
    "ops": [
      "Energía química del alimento en movimiento y calor",
      "Luz en energía química",
      "Sonido en movimiento"
    ],
    "m": "Por eso el cuerpo se calienta al hacer ejercicio."
  },
  {
    "q": "¿Por qué ninguna máquina es 100% eficiente?",
    "ops": [
      "Porque siempre se pierde energía como calor",
      "Porque están mal diseñadas",
      "Porque se rompen"
    ],
    "m": "La degradación es inevitable, no un defecto de fabricación."
  },
  {
    "q": "En una estufa eléctrica, ¿la transformación es eficiente?",
    "ops": [
      "Sí, porque lo que se busca ES el calor",
      "No, se pierde todo",
      "Sólo en invierno"
    ],
    "m": "Cuando el calor es el objetivo, no cuenta como pérdida."
  },
  {
    "q": "En una central térmica, ¿qué transformaciones hay?",
    "ops": [
      "Química → calor → movimiento → eléctrica",
      "Eléctrica → química",
      "Sólo calor → eléctrica"
    ],
    "m": "Se quema combustible, el vapor mueve la turbina y ésta el generador."
  },
  {
    "q": "¿La energía de una pila se acaba?",
    "ops": [
      "Se transforma hasta que los reactivos se agotan",
      "Desaparece sin más",
      "Se recicla sola"
    ],
    "m": "La cantidad se conserva; lo que se agota es la sustancia que la almacena."
  },
  {
    "q": "En un molino eólico, ¿qué se transforma?",
    "ops": [
      "Energía del viento en eléctrica",
      "Calor en movimiento",
      "Luz en calor"
    ],
    "m": "El viento mueve las palas y éstas el generador."
  },
  {
    "q": "Al frenar un auto, ¿adónde va la energía del movimiento?",
    "ops": [
      "Se transforma en calor en los frenos",
      "Desaparece",
      "Vuelve al motor"
    ],
    "m": "Por eso los frenos se calientan tanto."
  },
  {
    "q": "¿Se puede recuperar toda la energía degradada como calor disperso?",
    "ops": [
      "No, en la práctica no",
      "Sí, con la máquina adecuada",
      "Sí, siempre"
    ],
    "m": "Ésa es la diferencia entre conservación y degradación."
  }
];
GAMES.transformar_energia_7 = juegoTriviaTexto(CUR_TRANSFORMAR_ENERGIA_7_BANCO, "¿En qué se transforma?", "transforma");

/* 7° · ¿Química o física? — quimica_fisica_7
   DC: Transformaciones químicas y físicas; reactivos y productos; combustión
   Fuente: docs/auditoria-dc-caba/grado-7.md · CN8 */
const CUR_QUIMICA_FISICA_7_BANCO = [
  {
    "it": "El hielo se derrite",
    "cat": "fisica",
    "m": "Sigue siendo agua: sólo cambió de estado."
  },
  {
    "it": "Un papel se quema",
    "cat": "quimica",
    "m": "Aparecen sustancias nuevas: cenizas y gases. No hay vuelta atrás."
  },
  {
    "it": "El agua hierve",
    "cat": "fisica",
    "m": "El vapor sigue siendo agua."
  },
  {
    "it": "Un clavo se oxida",
    "cat": "quimica",
    "m": "El hierro se combina con el oxígeno y forma óxido, otra sustancia."
  },
  {
    "it": "Se rompe un vaso",
    "cat": "fisica",
    "m": "Cambió la forma, no el vidrio."
  },
  {
    "it": "La leche se corta",
    "cat": "quimica",
    "m": "Las proteínas se transforman: ya no es leche."
  },
  {
    "it": "Se disuelve azúcar en agua",
    "cat": "fisica",
    "m": "El azúcar sigue ahí: se puede recuperar evaporando el agua."
  },
  {
    "it": "Se hornea una torta",
    "cat": "quimica",
    "m": "Los ingredientes reaccionan y forman algo nuevo."
  },
  {
    "it": "Se corta una madera con serrucho",
    "cat": "fisica",
    "m": "Sigue siendo madera, en trozos más chicos."
  },
  {
    "it": "Una fruta se pudre",
    "cat": "quimica",
    "m": "Los microorganismos transforman su materia."
  },
  {
    "it": "Un alambre de cobre se dobla",
    "cat": "fisica",
    "m": "Cambió la forma; el cobre es el mismo."
  },
  {
    "it": "Se enciende una vela y la cera arde",
    "cat": "quimica",
    "m": "La combustión produce dióxido de carbono y agua."
  },
  {
    "it": "Se evapora el agua de un charco",
    "cat": "fisica",
    "m": "Cambio de estado, no de sustancia."
  },
  {
    "it": "Se agrega vinagre al bicarbonato y burbujea",
    "cat": "quimica",
    "m": "El gas que sale es una sustancia nueva."
  },
  {
    "it": "Se muele café en grano",
    "cat": "fisica",
    "m": "El polvo sigue siendo café."
  },
  {
    "it": "Una manzana cortada se pone marrón",
    "cat": "quimica",
    "m": "Se oxida al contacto con el aire."
  }
];
GAMES.quimica_fisica_7 = juegoClasificar(CUR_QUIMICA_FISICA_7_BANCO, "¿Cambió la sustancia o sólo su forma?", [{"cat": "fisica", "label": "🧊 Física"}, {"cat": "quimica", "label": "🔥 Química"}], "quimica_fi");

/* 7° · Día, noche, estaciones y fases — movimientos_tierra_7
   DC: Rotación y traslación; eje inclinado; fases lunares
   Fuente: docs/auditoria-dc-caba/grado-7.md · CN9 */
const CUR_MOVIMIENTOS_TIERRA_7_BANCO = [
  {
    "q": "¿Qué produce el día y la noche?",
    "ops": [
      "La rotación de la Tierra",
      "La traslación alrededor del Sol",
      "El movimiento de la Luna"
    ],
    "m": "La rotación dura 24 horas; la traslación, un año."
  },
  {
    "q": "¿Qué produce las estaciones del año?",
    "ops": [
      "La inclinación del eje terrestre durante la traslación",
      "La distancia al Sol",
      "La rotación"
    ],
    "m": "Éste es EL error del tema: la distancia casi no influye. De hecho la Tierra está más cerca del Sol en enero, que es verano acá y invierno en el norte."
  },
  {
    "q": "Cuando es verano en la Argentina, en Europa es…",
    "ops": [
      "Invierno",
      "Verano también",
      "Otoño"
    ],
    "m": "Los hemisferios reciben la luz con distinta inclinación al mismo tiempo."
  },
  {
    "q": "¿Cuánto tarda la Tierra en dar una vuelta sobre su eje?",
    "ops": [
      "24 horas",
      "365 días",
      "28 días"
    ],
    "m": "365 días es la traslación."
  },
  {
    "q": "¿Cuánto tarda la Luna en dar una vuelta alrededor de la Tierra?",
    "ops": [
      "Alrededor de 28 días",
      "24 horas",
      "365 días"
    ],
    "m": "Por eso el ciclo de las fases dura aproximadamente un mes."
  },
  {
    "q": "¿Por qué vemos siempre la misma cara de la Luna?",
    "ops": [
      "Porque tarda lo mismo en rotar que en girar alrededor de la Tierra",
      "Porque no rota",
      "Porque está muy lejos"
    ],
    "m": "Se llama rotación sincrónica."
  },
  {
    "q": "¿Por qué la Luna cambia de forma?",
    "ops": [
      "Porque vemos distinta parte de su mitad iluminada",
      "Porque la sombra de la Tierra la tapa",
      "Porque cambia de tamaño"
    ],
    "m": "La sombra de la Tierra sólo actúa en un eclipse de Luna, que es otra cosa."
  },
  {
    "q": "En el solsticio de verano, ¿qué pasa?",
    "ops": [
      "Es el día más largo del año en ese hemisferio",
      "El día y la noche duran igual",
      "Es el día más corto"
    ],
    "m": "En el equinoccio duran igual."
  },
  {
    "q": "¿Qué es un equinoccio?",
    "ops": [
      "El día en que la noche y el día duran lo mismo",
      "El día más largo",
      "El día más corto"
    ],
    "m": "Ocurre dos veces al año, en marzo y en septiembre."
  },
  {
    "q": "¿En qué orden van las fases de la Luna?",
    "ops": [
      "Nueva, creciente, llena, menguante",
      "Llena, nueva, creciente, menguante",
      "Creciente, nueva, menguante, llena"
    ],
    "m": "El ciclo empieza cuando no la vemos y vuelve a empezar."
  },
  {
    "q": "¿Cuánta parte de la Luna está iluminada por el Sol en cualquier momento?",
    "ops": [
      "Siempre la mitad",
      "Toda",
      "Depende de la fase"
    ],
    "m": "Lo que cambia es cuánto de esa mitad vemos desde acá."
  },
  {
    "q": "Si el eje de la Tierra no estuviera inclinado, ¿qué pasaría?",
    "ops": [
      "No habría estaciones marcadas",
      "No habría día y noche",
      "El año duraría menos"
    ],
    "m": "La inclinación es lo que hace que la luz llegue distinta según la época."
  },
  {
    "q": "¿Qué es un año bisiesto y por qué existe?",
    "ops": [
      "Porque la traslación tarda un poco más de 365 días",
      "Porque la Luna cambia",
      "Porque el calendario está mal"
    ],
    "m": "Cada cuatro años se acumula casi un día entero."
  },
  {
    "q": "¿El Sol se mueve alrededor de la Tierra?",
    "ops": [
      "No: es un movimiento aparente por la rotación terrestre",
      "Sí, una vez por día",
      "Sí, una vez por año"
    ],
    "m": "Ese movimiento aparente sostuvo al geocentrismo durante siglos."
  }
];
GAMES.movimientos_tierra_7 = juegoTriviaTexto(CUR_MOVIMIENTOS_TIERRA_7_BANCO, "Pensá qué movimiento produce cada cosa.", "movimiento");

/* 7° · Eclipses y el universo — eclipses_universo_7
   DC: Eclipses; escalas; modelo actual del universo y exoplanetas
   Fuente: docs/auditoria-dc-caba/grado-7.md · CN10 */
const CUR_ECLIPSES_UNIVERSO_7_BANCO = [
  {
    "q": "En un eclipse de SOL, ¿qué tapa a qué?",
    "ops": [
      "La Luna tapa al Sol",
      "La Tierra tapa al Sol",
      "El Sol tapa a la Luna"
    ],
    "m": "La Luna se interpone entre el Sol y nosotros."
  },
  {
    "q": "En un eclipse de LUNA, ¿qué pasa?",
    "ops": [
      "La sombra de la Tierra cae sobre la Luna",
      "La Luna tapa al Sol",
      "La Luna se apaga"
    ],
    "m": "La Tierra queda en el medio."
  },
  {
    "q": "¿Por qué la Luna, siendo chiquita, puede tapar al Sol?",
    "ops": [
      "Porque el Sol es 400 veces más grande pero está 400 veces más lejos",
      "Porque la Luna crece",
      "Porque el Sol se achica"
    ],
    "m": "Es una coincidencia de escalas que hace posible el eclipse total."
  },
  {
    "q": "¿Por qué no hay un eclipse cada mes?",
    "ops": [
      "Porque la órbita de la Luna está inclinada respecto de la de la Tierra",
      "Porque la Luna se aleja",
      "Porque el Sol se mueve"
    ],
    "m": "Sólo se alinean en ciertos momentos del año."
  },
  {
    "q": "¿Se puede mirar un eclipse de Sol a ojo desnudo?",
    "ops": [
      "No: daña la vista de forma permanente",
      "Sí, si es corto",
      "Sí, con anteojos de sol comunes"
    ],
    "m": "Hacen falta filtros especiales certificados."
  },
  {
    "q": "¿Qué es la Vía Láctea?",
    "ops": [
      "La galaxia donde está el Sol",
      "Un cúmulo de planetas",
      "Otra galaxia lejana"
    ],
    "m": "El Sol es una de sus cientos de miles de millones de estrellas."
  },
  {
    "q": "¿Dónde está el Sol dentro de la Vía Láctea?",
    "ops": [
      "En un brazo, lejos del centro",
      "En el centro exacto",
      "Fuera de la galaxia"
    ],
    "m": "Está a unos 26.000 años luz del centro."
  },
  {
    "q": "¿Qué es un año luz?",
    "ops": [
      "La distancia que recorre la luz en un año",
      "El tiempo que tarda la luz en llegar",
      "Un año en otro planeta"
    ],
    "m": "Es una unidad de DISTANCIA, no de tiempo."
  },
  {
    "q": "¿Qué es un exoplaneta?",
    "ops": [
      "Un planeta que orbita otra estrella",
      "Un planeta muy grande",
      "Un planeta sin atmósfera"
    ],
    "m": "Ya se confirmaron miles."
  },
  {
    "q": "¿Qué es el Big Bang según el modelo actual?",
    "ops": [
      "El estado inicial denso y caliente del que el universo se expande",
      "Una explosión en el espacio vacío",
      "El fin del universo"
    ],
    "m": "No fue una explosión EN el espacio: el espacio mismo se expande."
  },
  {
    "q": "¿El universo se está expandiendo?",
    "ops": [
      "Sí, y la expansión se acelera",
      "No, es estático",
      "Se está contrayendo"
    ],
    "m": "Se observa por el corrimiento al rojo de las galaxias lejanas."
  },
  {
    "q": "Cuando mirás una estrella muy lejana, ¿qué estás viendo?",
    "ops": [
      "Cómo era hace mucho tiempo, porque la luz tardó en llegar",
      "Cómo es ahora mismo",
      "Un reflejo del Sol"
    ],
    "m": "Mirar lejos es mirar al pasado."
  },
  {
    "q": "¿Cuánto tarda la luz del Sol en llegar a la Tierra?",
    "ops": [
      "Unos 8 minutos",
      "Un segundo",
      "Un año"
    ],
    "m": "Por eso vemos al Sol como era hace ocho minutos."
  },
  {
    "q": "¿Qué es una galaxia?",
    "ops": [
      "Un conjunto enorme de estrellas, gas y polvo ligados por la gravedad",
      "Un sistema de planetas",
      "Una nube de gas sin estrellas"
    ],
    "m": "Un sistema de planetas alrededor de una estrella es un sistema planetario."
  }
];
GAMES.eclipses_universo_7 = juegoTriviaTexto(CUR_ECLIPSES_UNIVERSO_7_BANCO, "Pensá en las escalas y en las sombras.", "eclipses_u");

/* 7° · Sistema reproductor — reproductor_7
   DC: Anatomía y función del sistema reproductor (ESI)
   Fuente: docs/auditoria-dc-caba/grado-7.md · CN11 */
const CUR_REPRODUCTOR_7_BANCO = [
  {
    "q": "¿Qué órgano produce los óvulos?",
    "ops": [
      "El ovario",
      "El útero",
      "La trompa de Falopio"
    ],
    "m": "El útero es donde se implantaría el embrión."
  },
  {
    "q": "¿Qué órganos producen los espermatozoides?",
    "ops": [
      "Los testículos",
      "La próstata",
      "La uretra"
    ],
    "m": "La próstata aporta parte del líquido seminal, no las células."
  },
  {
    "q": "¿Cuál es la función del útero?",
    "ops": [
      "Alojar y nutrir al embrión durante el embarazo",
      "Producir óvulos",
      "Transportar la orina"
    ],
    "m": "Producir óvulos es función del ovario."
  },
  {
    "q": "¿Qué función cumplen los ovarios?",
    "ops": [
      "Producen óvulos y hormonas",
      "Transportan el óvulo",
      "Alojan al embrión"
    ],
    "m": "El transporte es de las trompas; el embarazo ocurre en el útero."
  },
  {
    "q": "¿Qué es la menarca?",
    "ops": [
      "La primera menstruación",
      "El fin del ciclo menstrual",
      "La primera ovulación de la vida"
    ],
    "m": "Marca el inicio de los ciclos, aunque al principio sean irregulares."
  },
  {
    "q": "¿Qué hormonas participan del ciclo menstrual?",
    "ops": [
      "Estrógenos y progesterona",
      "Insulina y adrenalina",
      "Tiroxina y cortisol"
    ],
    "m": "Son hormonas sexuales producidas principalmente en los ovarios."
  },
  {
    "q": "¿Qué es la vulva?",
    "ops": [
      "El conjunto de los órganos genitales externos",
      "El útero",
      "La vagina"
    ],
    "m": "La vagina es un conducto interno: no son sinónimos."
  },
  {
    "q": "¿Cuál es la función del escroto?",
    "ops": [
      "Mantener los testículos a una temperatura menor que la del cuerpo",
      "Producir hormonas",
      "Almacenar orina"
    ],
    "m": "Los espermatozoides necesitan algunos grados menos para formarse bien."
  },
  {
    "q": "¿Qué es la pubertad desde el punto de vista del aparato reproductor?",
    "ops": [
      "El momento en que empieza a ser funcional",
      "El fin del desarrollo",
      "Una enfermedad"
    ],
    "m": "Es una etapa normal del desarrollo."
  },
  {
    "q": "¿Qué produce la próstata?",
    "ops": [
      "Parte del líquido seminal",
      "Los espermatozoides",
      "Las hormonas femeninas"
    ],
    "m": "Los espermatozoides se producen en los testículos."
  },
  {
    "q": "¿Los sistemas reproductores funcionan aislados del resto del cuerpo?",
    "ops": [
      "No: están regulados por el sistema endocrino",
      "Sí, funcionan solos",
      "Sólo dependen del nervioso"
    ],
    "m": "Las hormonas coordinan su funcionamiento."
  },
  {
    "q": "¿Por qué importa usar los nombres correctos de las partes del cuerpo?",
    "ops": [
      "Porque permite pedir ayuda y cuidarse con precisión",
      "Porque queda mejor",
      "No importa"
    ],
    "m": "Es una de las razones por las que la ESI insiste en nombrar bien."
  },
  {
    "q": "¿Qué son las trompas de Falopio?",
    "ops": [
      "Los conductos que unen los ovarios con el útero",
      "Glándulas hormonales",
      "Parte de la vejiga"
    ],
    "m": "Por ahí viaja el óvulo."
  },
  {
    "q": "¿A quién conviene consultarle dudas sobre salud sexual?",
    "ops": [
      "A un profesional de la salud o un adulto de confianza",
      "A nadie",
      "Sólo a internet"
    ],
    "m": "En los centros de salud la consulta es gratuita y confidencial."
  }
];
GAMES.reproductor_7 = juegoTriviaTexto(CUR_REPRODUCTOR_7_BANCO, "Reconocé cada órgano y su función.", "reproducto");

/* 7° · Línea de tiempo del siglo XX — linea_siglo_xx_7
   DC: 1930, sustitución de importaciones, peronismo, 1976, Malvinas, 1983
   Fuente: docs/auditoria-dc-caba/grado-7.md · CS1 */
const CUR_LINEA_SIGLO_XX_7_BANCO = [
  {
    "items": [
      "Golpe de Estado de 1930",
      "Primera presidencia de Perón (1946)",
      "Golpe de Estado de 1976",
      "Vuelta de la democracia (1983)"
    ]
  },
  {
    "items": [
      "Crisis mundial de 1929",
      "Comienza la sustitución de importaciones (1930s)",
      "Voto femenino en la Argentina (1947)",
      "Primera elección con voto de mujeres (1951)"
    ]
  },
  {
    "items": [
      "Golpe de 1930",
      "Golpe de 1955",
      "Golpe de 1976",
      "Elecciones de 1983"
    ]
  },
  {
    "items": [
      "Segunda Guerra Mundial (1939-1945)",
      "Creación de las Naciones Unidas (1945)",
      "Guerra de Malvinas (1982)",
      "Juicio a las Juntas (1985)"
    ]
  },
  {
    "items": [
      "Ley Sáenz Peña (1912)",
      "Golpe de 1930",
      "Primera presidencia de Perón (1946)",
      "Golpe de 1976"
    ]
  },
  {
    "items": [
      "Sustitución de importaciones (década de 1930)",
      "Voto femenino (1947)",
      "Guerra de Malvinas (1982)",
      "Reforma de la Constitución (1994)"
    ]
  },
  {
    "items": [
      "Golpe de Estado de 1976",
      "Guerra de Malvinas (1982)",
      "Vuelta de la democracia (1983)",
      "Juicio a las Juntas (1985)"
    ]
  },
  {
    "items": [
      "Fin de la Segunda Guerra Mundial (1945)",
      "Comienzo de la Guerra Fría (fines de los 40)",
      "Caída del Muro de Berlín (1989)",
      "Reforma constitucional argentina (1994)"
    ]
  },
  {
    "items": [
      "Primera presidencia de Perón (1946)",
      "Voto femenino (1947)",
      "Golpe de 1955",
      "Golpe de 1976"
    ]
  },
  {
    "items": [
      "Guerra de Malvinas (1982)",
      "Vuelta de la democracia (1983)",
      "Juicio a las Juntas (1985)",
      "Reforma constitucional (1994)"
    ]
  }
];
GAMES.linea_siglo_xx_7 = juegoOrdenar(CUR_LINEA_SIGLO_XX_7_BANCO, "Ordená del hecho MÁS ANTIGUO al más nuevo. Tocá en orden.", "Anclate en las fechas que ya sabés y ubicá el resto alrededor.", "linea_sigl");

/* 7° · Bandos: Segunda Guerra y Guerra Fría — bandos_siglo_xx_7
   DC: Aliados y Eje; el mundo bipolar de la Guerra Fría
   Fuente: docs/auditoria-dc-caba/grado-7.md · CS2 */
const CUR_BANDOS_SIGLO_XX_7_BANCO = [
  {
    "it": "La alianza entre Alemania, Italia y Japón",
    "cat": "segunda_guerra",
    "m": "Eran las potencias del Eje."
  },
  {
    "it": "El Muro de Berlín",
    "cat": "guerra_fria",
    "m": "Se levantó en 1961 y dividió la ciudad hasta 1989."
  },
  {
    "it": "El desembarco en Normandía",
    "cat": "segunda_guerra",
    "m": "Operación aliada de 1944."
  },
  {
    "it": "La carrera espacial entre Estados Unidos y la URSS",
    "cat": "guerra_fria",
    "m": "La competencia se dio en la ciencia y la tecnología, no en el campo de batalla."
  },
  {
    "it": "El Holocausto",
    "cat": "segunda_guerra",
    "m": "El exterminio sistemático perpetrado por el régimen nazi."
  },
  {
    "it": "La OTAN y el Pacto de Varsovia",
    "cat": "guerra_fria",
    "m": "Las dos alianzas militares del mundo bipolar."
  },
  {
    "it": "El bombardeo de Hiroshima y Nagasaki",
    "cat": "segunda_guerra",
    "m": "Agosto de 1945, al final del conflicto."
  },
  {
    "it": "La crisis de los misiles en Cuba",
    "cat": "guerra_fria",
    "m": "1962: el momento de mayor tensión nuclear."
  },
  {
    "it": "La invasión de Polonia en 1939",
    "cat": "segunda_guerra",
    "m": "El hecho que dio inicio a la guerra en Europa."
  },
  {
    "it": "La caída del Muro en 1989",
    "cat": "guerra_fria",
    "m": "Marca simbólicamente el final de la Guerra Fría."
  },
  {
    "it": "La alianza entre Estados Unidos, el Reino Unido y la URSS",
    "cat": "segunda_guerra",
    "m": "Eran los Aliados: pelearon juntos y después quedaron enfrentados."
  },
  {
    "it": "La división del mundo en dos bloques ideológicos",
    "cat": "guerra_fria",
    "m": "Capitalismo y comunismo como modelos en disputa."
  },
  {
    "it": "La creación de las Naciones Unidas en 1945",
    "cat": "segunda_guerra",
    "m": "Nació al terminar el conflicto, para evitar otro igual."
  },
  {
    "it": "La llegada del hombre a la Luna en 1969",
    "cat": "guerra_fria",
    "m": "Fue un hito de la carrera espacial entre las dos potencias."
  },
  {
    "it": "El juicio de Núremberg",
    "cat": "segunda_guerra",
    "m": "Juzgó los crímenes del régimen nazi al terminar la guerra."
  },
  {
    "it": "El apoyo de las potencias a distintos bandos en conflictos de otros países",
    "cat": "guerra_fria",
    "m": "Los enfrentamientos eran indirectos: por eso «fría»."
  }
];
GAMES.bandos_siglo_xx_7 = juegoClasificar(CUR_BANDOS_SIGLO_XX_7_BANCO, "¿De qué conflicto es este elemento?", [{"cat": "segunda_guerra", "label": "⚔️ Segunda Guerra"}, {"cat": "guerra_fria", "label": "❄️ Guerra Fría"}], "bandos_sig");

/* 7° · ¿Democracia o dictadura? — democracia_dictadura_7
   DC: Alternancia de democracias y dictaduras; terrorismo de Estado; DDHH
   Fuente: docs/auditoria-dc-caba/grado-7.md · CS3 */
const CUR_DEMOCRACIA_DICTADURA_7_BANCO = [
  {
    "q": "¿Qué caracteriza a un gobierno democrático?",
    "ops": [
      "Se elige por el voto y tiene límites y controles",
      "Gobierna una sola persona sin control",
      "No hay elecciones"
    ],
    "m": "No alcanza con votar: también hacen falta división de poderes y libertades."
  },
  {
    "q": "¿Qué es un golpe de Estado?",
    "ops": [
      "La toma del poder por fuera de la Constitución",
      "Una elección adelantada",
      "Un cambio de ministro"
    ],
    "m": "Interrumpe el orden constitucional por la fuerza."
  },
  {
    "q": "¿Cuántos golpes de Estado hubo en la Argentina en el siglo XX?",
    "ops": [
      "Seis: 1930, 1943, 1955, 1962, 1966 y 1976",
      "Uno solo, en 1976",
      "Ninguno"
    ],
    "m": "La alternancia entre gobiernos elegidos y de facto marcó buena parte del siglo."
  },
  {
    "q": "¿En qué año volvió la democracia a la Argentina?",
    "ops": [
      "1983",
      "1976",
      "1994"
    ],
    "m": "Desde entonces no se interrumpió el orden constitucional."
  },
  {
    "q": "¿Qué es el terrorismo de Estado?",
    "ops": [
      "Cuando el propio Estado usa su aparato para perseguir y reprimir ilegalmente",
      "Un ataque contra el Estado",
      "Una protesta social"
    ],
    "m": "Lo grave es que quien debía proteger los derechos fue el que los violó."
  },
  {
    "q": "¿Qué fue un centro clandestino de detención?",
    "ops": [
      "Un lugar secreto donde se detenía a personas al margen de la ley",
      "Una cárcel común",
      "Un cuartel militar cualquiera"
    ],
    "m": "Clandestino significa que su existencia se negaba oficialmente."
  },
  {
    "q": "¿Qué es una desaparición forzada?",
    "ops": [
      "Cuando el Estado detiene a alguien y niega tenerlo o dar información",
      "Cuando alguien se muda sin avisar",
      "Una detención con orden judicial"
    ],
    "m": "La negación es parte del delito: deja a la familia sin ninguna vía legal."
  },
  {
    "q": "¿Qué son las Abuelas de Plaza de Mayo?",
    "ops": [
      "Una organización que busca a los nietos apropiados durante la dictadura",
      "Un partido político",
      "Un organismo del gobierno"
    ],
    "m": "Fue una de las apropiaciones sistemáticas de bebés que la Justicia comprobó."
  },
  {
    "q": "¿Qué fue la CONADEP?",
    "ops": [
      "La comisión que investigó las desapariciones y publicó el informe «Nunca Más»",
      "Un tribunal militar",
      "Un partido político"
    ],
    "m": "Se creó en 1983 y su informe fue prueba en los juicios."
  },
  {
    "q": "¿Qué fue el Juicio a las Juntas de 1985?",
    "ops": [
      "El juicio civil a los responsables de la dictadura",
      "Un juicio militar interno",
      "Una comisión investigadora"
    ],
    "m": "Fue excepcional en el mundo: un tribunal civil juzgando a los jefes de un régimen anterior."
  },
  {
    "q": "¿Qué se conmemora el 24 de marzo?",
    "ops": [
      "El Día Nacional de la Memoria por la Verdad y la Justicia",
      "El Día de la Independencia",
      "La vuelta de la democracia"
    ],
    "m": "Recuerda el golpe de 1976. Es feriado inamovible por ley."
  },
  {
    "q": "¿Qué son los derechos humanos?",
    "ops": [
      "Derechos que toda persona tiene por el solo hecho de serlo",
      "Derechos que otorga cada gobierno",
      "Derechos que se compran"
    ],
    "m": "No dependen de la nacionalidad ni de quién gobierne."
  },
  {
    "q": "¿Qué pasa con la libertad de prensa en una dictadura?",
    "ops": [
      "Se restringe o se censura",
      "Se amplía",
      "No cambia"
    ],
    "m": "Controlar la información es una de las primeras medidas."
  },
  {
    "q": "¿Por qué se dice que la memoria es una construcción colectiva?",
    "ops": [
      "Porque recordar lo que pasó ayuda a que no vuelva a pasar",
      "Porque es obligatoria",
      "Porque la decide el gobierno"
    ],
    "m": "Ésa es la razón de los espacios y las fechas de memoria."
  },
  {
    "q": "¿Los delitos de lesa humanidad prescriben?",
    "ops": [
      "No: se pueden juzgar sin límite de tiempo",
      "Sí, a los diez años",
      "Sí, a los veinte años"
    ],
    "m": "La imprescriptibilidad es lo que permitió reabrir los juicios años después."
  }
];
GAMES.democracia_dictadura_7 = juegoTriviaTexto(CUR_DEMOCRACIA_DICTADURA_7_BANCO, "Pensá quién ejerce el poder y con qué límites.", "democracia");

/* 7° · Cadena productiva y regiones — cadena_productiva_7
   DC: Encadenamientos agroindustriales; producciones por región
   Fuente: docs/auditoria-dc-caba/grado-7.md · CS4 */
const CUR_CADENA_PRODUCTIVA_7_BANCO = [
  {
    "q": "¿Cuál es el orden de una cadena productiva?",
    "ops": [
      "Materia prima → industrialización → distribución → consumo",
      "Consumo → industrialización → materia prima",
      "Distribución → materia prima → consumo"
    ],
    "m": "Siempre va de lo que se extrae a lo que se consume."
  },
  {
    "q": "¿Qué es el valor agregado?",
    "ops": [
      "Lo que se suma al producto en cada etapa de elaboración",
      "El precio de la materia prima",
      "El costo del transporte"
    ],
    "m": "Por eso exportar harina rinde más que exportar trigo."
  },
  {
    "q": "¿En qué región argentina se produce principalmente la yerba mate?",
    "ops": [
      "Misiones y Corrientes",
      "La Patagonia",
      "Cuyo"
    ],
    "m": "Necesita el clima subtropical del noreste."
  },
  {
    "q": "¿Qué se produce principalmente en Cuyo?",
    "ops": [
      "Vid y vino",
      "Yerba mate",
      "Algodón"
    ],
    "m": "Mendoza y San Juan concentran la vitivinicultura."
  },
  {
    "q": "¿Qué producción caracteriza al Alto Valle de Río Negro y Neuquén?",
    "ops": [
      "Manzanas y peras",
      "Caña de azúcar",
      "Yerba mate"
    ],
    "m": "La fruticultura de pepita es su actividad emblemática."
  },
  {
    "q": "¿Dónde se concentra la producción de caña de azúcar?",
    "ops": [
      "Tucumán y el noroeste",
      "La Patagonia",
      "La pampa húmeda"
    ],
    "m": "Necesita clima cálido y húmedo."
  },
  {
    "q": "¿Qué se produce principalmente en la región pampeana?",
    "ops": [
      "Cereales, oleaginosas y ganado",
      "Petróleo",
      "Yerba mate"
    ],
    "m": "Su suelo fértil y su clima templado la hacen el corazón agrícola."
  },
  {
    "q": "¿Qué es un circuito productivo agroindustrial?",
    "ops": [
      "El conjunto de etapas que van del campo a la industria y al consumidor",
      "Sólo la etapa del campo",
      "Sólo la venta"
    ],
    "m": "Incluye a todos los actores, no sólo al productor."
  },
  {
    "q": "¿Por qué conviene industrializar la materia prima antes de exportarla?",
    "ops": [
      "Porque se vende más caro y genera más trabajo local",
      "Porque pesa menos",
      "Porque es más fácil"
    ],
    "m": "El valor agregado queda en el país en vez de irse afuera."
  },
  {
    "q": "¿Qué región produce lana y carne ovina?",
    "ops": [
      "La Patagonia",
      "El noreste",
      "Cuyo"
    ],
    "m": "Las estepas patagónicas son aptas para el ovino."
  },
  {
    "q": "¿Qué es la etapa de comercialización?",
    "ops": [
      "Cuando el producto llega al consumidor",
      "Cuando se cosecha",
      "Cuando se industrializa"
    ],
    "m": "Es la última etapa del circuito."
  },
  {
    "q": "El algodón se produce principalmente en…",
    "ops": [
      "Chaco y Santiago del Estero",
      "La Patagonia",
      "Cuyo"
    ],
    "m": "Es un cultivo del norte argentino."
  },
  {
    "q": "¿Qué actores intervienen en un circuito productivo?",
    "ops": [
      "Productores, industriales, transportistas y comerciantes",
      "Sólo los productores",
      "Sólo el Estado"
    ],
    "m": "Cada uno se queda con una parte del valor final."
  },
  {
    "q": "¿Qué región concentra la actividad petrolera?",
    "ops": [
      "Patagonia y Cuyo",
      "El noreste",
      "La pampa húmeda"
    ],
    "m": "Neuquén, Chubut, Santa Cruz y Mendoza son las principales."
  }
];
GAMES.cadena_productiva_7 = juegoTriviaTexto(CUR_CADENA_PRODUCTIVA_7_BANCO, "Seguí el recorrido de la producción.", "cadena_pro");

/* 7° · Flujos migratorios — migraciones_7
   DC: Migraciones forzadas y voluntarias; áreas expulsoras y receptoras
   Fuente: docs/auditoria-dc-caba/grado-7.md · CS5 */
const CUR_MIGRACIONES_7_BANCO = [
  {
    "it": "Una ingeniera se muda a otro país porque le ofrecieron un mejor puesto",
    "cat": "voluntaria",
    "m": "Elige entre dos opciones posibles."
  },
  {
    "it": "Una familia huye de una zona en guerra",
    "cat": "forzada",
    "m": "Quedarse pondría en riesgo su vida."
  },
  {
    "it": "Un joven emigra porque en su región no hay trabajo desde hace años",
    "cat": "mixta",
    "m": "Formalmente elige, pero la falta de alternativas lo empuja."
  },
  {
    "it": "Un estudiante se va a cursar un posgrado al exterior",
    "cat": "voluntaria",
    "m": "Es una decisión tomada entre opciones reales."
  },
  {
    "it": "Una comunidad tiene que abandonar su pueblo por una inundación",
    "cat": "forzada",
    "m": "El desastre ambiental no deja alternativa."
  },
  {
    "it": "Una familia deja el campo porque la mecanización eliminó su trabajo",
    "cat": "mixta",
    "m": "La causa económica estructural condiciona la decisión."
  },
  {
    "it": "Alguien se muda a otra provincia porque le gusta el clima",
    "cat": "voluntaria",
    "m": "Motivo personal, sin presión externa."
  },
  {
    "it": "Personas perseguidas por su religión piden refugio en otro país",
    "cat": "forzada",
    "m": "El derecho al asilo existe justamente para estos casos."
  },
  {
    "it": "Una persona emigra porque en su país la inflación se comió su salario",
    "cat": "mixta",
    "m": "La crisis económica reduce el margen de elección."
  },
  {
    "it": "Un músico se instala en otra ciudad para desarrollar su carrera",
    "cat": "voluntaria",
    "m": "Decisión profesional entre alternativas."
  },
  {
    "it": "Una población es desplazada por la construcción de una represa",
    "cat": "forzada",
    "m": "El desplazamiento lo impone una obra, no la persona."
  },
  {
    "it": "Una familia se muda buscando escuelas y hospitales que en su zona no hay",
    "cat": "mixta",
    "m": "La falta de servicios básicos empuja la decisión."
  },
  {
    "it": "Una pareja se muda al exterior para estar cerca de sus hijos",
    "cat": "voluntaria",
    "m": "Motivo familiar, con opción de quedarse."
  },
  {
    "it": "Personas escapan de un régimen que las persigue por su opinión política",
    "cat": "forzada",
    "m": "El exilio político es una migración forzada."
  },
  {
    "it": "Un trabajador rural viaja cada año a otra provincia para la cosecha",
    "cat": "mixta",
    "m": "La migración estacional responde a la necesidad de trabajo."
  },
  {
    "it": "Alguien se muda a otra ciudad porque le ofrecieron una beca",
    "cat": "voluntaria",
    "m": "Una oportunidad que se elige tomar."
  }
];
GAMES.migraciones_7 = juegoClasificar(CUR_MIGRACIONES_7_BANCO, "¿La persona eligió irse o tuvo que hacerlo?", [{"cat": "voluntaria", "label": "🎒 Voluntaria"}, {"cat": "forzada", "label": "⚠️ Forzada"}, {"cat": "mixta", "label": "🔀 Mixta"}], "migracione");

/* 7° · Espacios de memoria porteños — espacios_memoria_7
   DC: Parque de la Memoria, ex ESMA, Museo del Holocausto, Museo Malvinas
   Fuente: docs/auditoria-dc-caba/grado-7.md · CS6 */
const CUR_ESPACIOS_MEMORIA_7_BANCO = [
  {
    "q": "¿Qué es el Parque de la Memoria?",
    "ops": [
      "Un espacio con un monumento que lleva los nombres de las víctimas del terrorismo de Estado",
      "Un parque de juegos",
      "Un museo de historia natural"
    ],
    "m": "Está sobre la costanera, frente al Río de la Plata."
  },
  {
    "q": "¿Qué funcionó en el predio de la ex ESMA durante la dictadura?",
    "ops": [
      "Un centro clandestino de detención",
      "Una escuela pública",
      "Un hospital"
    ],
    "m": "Hoy es el Espacio Memoria y Derechos Humanos."
  },
  {
    "q": "¿Qué recuerda el Museo del Holocausto de Buenos Aires?",
    "ops": [
      "El exterminio del pueblo judío durante la Segunda Guerra",
      "La Guerra de Malvinas",
      "La independencia argentina"
    ],
    "m": "Muchos sobrevivientes se radicaron en la Argentina."
  },
  {
    "q": "¿A qué está dedicado el Museo Malvinas e Islas del Atlántico Sur?",
    "ops": [
      "A la historia de las islas y al conflicto de 1982",
      "A la fauna marina solamente",
      "A la dictadura"
    ],
    "m": "Funciona en el mismo predio de la ex ESMA."
  },
  {
    "q": "¿Qué es la Casa Ana Frank de Buenos Aires?",
    "ops": [
      "Un centro educativo sobre el Holocausto y los derechos humanos",
      "La casa donde vivió Ana Frank",
      "Un archivo de la dictadura"
    ],
    "m": "Ana Frank nunca vivió en la Argentina: es una réplica con fines educativos."
  },
  {
    "q": "¿Para qué sirve un espacio de memoria?",
    "ops": [
      "Para que las nuevas generaciones conozcan lo que pasó",
      "Para atraer turistas",
      "Para guardar objetos antiguos"
    ],
    "m": "Su función es pedagógica y de reparación."
  },
  {
    "q": "¿Qué son los pañuelos blancos pintados en la Plaza de Mayo?",
    "ops": [
      "El símbolo de las Madres y Abuelas que reclaman por sus hijos y nietos",
      "Una decoración",
      "Un homenaje a los inmigrantes"
    ],
    "m": "Las Madres empezaron a rondar la plaza en 1977."
  },
  {
    "q": "¿Qué se conmemora el 2 de abril?",
    "ops": [
      "El Día del Veterano y de los Caídos en la Guerra de Malvinas",
      "La vuelta de la democracia",
      "El golpe de 1976"
    ],
    "m": "Recuerda el desembarco de 1982."
  },
  {
    "q": "¿Por qué se preservan los edificios donde ocurrieron los hechos?",
    "ops": [
      "Porque son prueba material y espacio de transmisión",
      "Porque son antiguos",
      "Porque no se pueden demoler"
    ],
    "m": "Sirvieron como evidencia en los juicios."
  },
  {
    "q": "¿Qué hacen las Abuelas de Plaza de Mayo?",
    "ops": [
      "Buscan a los nietos apropiados y les restituyen su identidad",
      "Administran museos",
      "Organizan actos escolares"
    ],
    "m": "Ya se restituyó la identidad de más de un centenar de personas."
  },
  {
    "q": "¿Qué es el derecho a la identidad?",
    "ops": [
      "El derecho a conocer el propio origen y llevar el nombre verdadero",
      "El derecho a votar",
      "El derecho a la educación"
    ],
    "m": "Está reconocido en la Convención sobre los Derechos del Niño."
  },
  {
    "q": "¿Qué significa «Nunca Más»?",
    "ops": [
      "El compromiso de que el terrorismo de Estado no se repita",
      "El nombre de un museo",
      "Una consigna partidaria"
    ],
    "m": "Es el título del informe de la CONADEP y se volvió una consigna común."
  },
  {
    "q": "Los espacios de memoria, ¿son sólo sobre la dictadura argentina?",
    "ops": [
      "No: también hay sobre el Holocausto y Malvinas",
      "Sí, sólo sobre la dictadura",
      "Sólo sobre Malvinas"
    ],
    "m": "Cada uno preserva la memoria de un proceso distinto."
  },
  {
    "q": "¿Qué es una marca territorial de memoria?",
    "ops": [
      "Una señal en el lugar donde ocurrió un hecho, para recordarlo",
      "Un cartel de tránsito",
      "Una placa de obra"
    ],
    "m": "Convierte un punto de la ciudad en un espacio de transmisión."
  }
];
GAMES.espacios_memoria_7 = juegoTriviaTexto(CUR_ESPACIOS_MEMORIA_7_BANCO, "¿Qué recuerda cada espacio?", "espacios_m");

/* 7° · Mi primera billetera — billetera_7
   DC: Sociales/FEC: ahorro, deuda e inversión; medios de pago; interés simple
   Fuente: docs/auditoria-dc-caba/grado-7.md · CS7 */
const CUR_BILLETERA_7_BANCO = [
  {
    "it": "Guardar $5.000 por mes en una caja de ahorro",
    "cat": "ahorro",
    "m": "Se aparta plata sin comprometerla ni arriesgarla."
  },
  {
    "it": "Comprar un celular en 12 cuotas con tarjeta de crédito",
    "cat": "deuda",
    "m": "Se usa plata que todavía no se tiene."
  },
  {
    "it": "Poner el dinero en un plazo fijo que paga interés",
    "cat": "inversion",
    "m": "Se busca que el dinero genere un rendimiento."
  },
  {
    "it": "Juntar plata en una alcancía para las vacaciones",
    "cat": "ahorro",
    "m": "Guardar con un objetivo, sin riesgo ni rendimiento."
  },
  {
    "it": "Pedir un préstamo al banco",
    "cat": "deuda",
    "m": "Hay que devolverlo con intereses."
  },
  {
    "it": "Comprar herramientas para trabajar con ellas",
    "cat": "inversion",
    "m": "Se espera que generen ingresos futuros."
  },
  {
    "it": "Dejar el sueldo en la cuenta sin tocarlo",
    "cat": "ahorro",
    "m": "Es ahorro, aunque no genere rendimiento."
  },
  {
    "it": "Pagar el mínimo del resumen de la tarjeta",
    "cat": "deuda",
    "m": "Lo que no se paga sigue generando intereses: es la deuda más cara."
  },
  {
    "it": "Comprar un curso para conseguir un mejor trabajo",
    "cat": "inversion",
    "m": "Se invierte en la propia formación."
  },
  {
    "it": "Apartar una parte del sueldo apenas cobra",
    "cat": "ahorro",
    "m": "Ahorrar primero y gastar después es la estrategia recomendada."
  },
  {
    "it": "Financiar el supermercado en cuotas",
    "cat": "deuda",
    "m": "Endeudarse por consumo corriente es lo más riesgoso."
  },
  {
    "it": "Comprar una máquina para producir y vender",
    "cat": "inversion",
    "m": "Se espera recuperar lo invertido y generar ganancia."
  },
  {
    "it": "Guardar plata para una emergencia",
    "cat": "ahorro",
    "m": "El fondo de emergencia es la primera recomendación financiera."
  },
  {
    "it": "Comprar ahora y pagar el mes que viene",
    "cat": "deuda",
    "m": "Aunque no haya interés, se compromete el ingreso futuro."
  },
  {
    "it": "Aportar a un fondo que rinde a lo largo del tiempo",
    "cat": "inversion",
    "m": "Busca rendimiento, y por eso también tiene riesgo."
  },
  {
    "it": "Tener el dinero disponible en la billetera virtual sin gastarlo",
    "cat": "ahorro",
    "m": "Está guardado y disponible."
  }
];
GAMES.billetera_7 = juegoClasificar(CUR_BILLETERA_7_BANCO, "¿Esto es ahorro, deuda o inversión?", [{"cat": "ahorro", "label": "🐖 Ahorro"}, {"cat": "deuda", "label": "📉 Deuda"}, {"cat": "inversion", "label": "📈 Inversión"}], "billetera_");

/* 7° · Puerto Madero y el arte urbano — puerto_madero_7
   DC: Refuncionalización urbana; murales, grafitis e intervenciones
   Fuente: docs/auditoria-dc-caba/grado-7.md · CS8 */
const CUR_PUERTO_MADERO_7_BANCO = [
  {
    "q": "¿Qué era Puerto Madero antes de su transformación?",
    "ops": [
      "Una zona portuaria en desuso con depósitos abandonados",
      "Un barrio residencial",
      "Un parque"
    ],
    "m": "El puerto quedó obsoleto cuando cambiaron los barcos y las cargas."
  },
  {
    "q": "¿Qué significa refuncionalizar un espacio?",
    "ops": [
      "Darle un uso nuevo conservando parte de lo construido",
      "Demolerlo todo",
      "Dejarlo como estaba"
    ],
    "m": "Los docks de ladrillo se convirtieron en oficinas y restaurantes."
  },
  {
    "q": "¿Qué es la gentrificación?",
    "ops": [
      "Cuando un barrio se renueva y sube tanto de precio que desplaza a sus vecinos",
      "La construcción de plazas",
      "La demolición de edificios viejos"
    ],
    "m": "Es la contracara habitual de una refuncionalización exitosa."
  },
  {
    "q": "¿Qué diferencia hay entre un mural y un grafiti?",
    "ops": [
      "El mural suele ser una obra planificada y autorizada",
      "El grafiti siempre es más grande",
      "No hay diferencia"
    ],
    "m": "El grafiti nació como práctica espontánea y muchas veces no autorizada."
  },
  {
    "q": "¿Qué es una intervención urbana?",
    "ops": [
      "Una acción artística que transforma temporalmente un espacio público",
      "Una obra de construcción",
      "Un corte de calle"
    ],
    "m": "Busca hacer pensar sobre el espacio, no sólo decorarlo."
  },
  {
    "q": "¿Por qué se conservaron las grúas del puerto?",
    "ops": [
      "Porque son patrimonio industrial y cuentan la historia del lugar",
      "Porque todavía funcionan",
      "Porque son muy pesadas"
    ],
    "m": "Preservar marcas del uso anterior es parte de la refuncionalización."
  },
  {
    "q": "¿Qué es el patrimonio industrial?",
    "ops": [
      "Construcciones y máquinas que testimonian la actividad productiva del pasado",
      "Las fábricas actuales",
      "Los museos de arte"
    ],
    "m": "Galpones, silos y grúas entran en esa categoría."
  },
  {
    "q": "¿Qué barrio porteño es conocido por sus murales de gran escala?",
    "ops": [
      "Villa Urquiza, entre otros",
      "Puerto Madero",
      "Recoleta"
    ],
    "m": "También La Boca y Barracas tienen una tradición muralista fuerte."
  },
  {
    "q": "¿Puede el arte urbano transformar la percepción de un barrio?",
    "ops": [
      "Sí, cambia cómo lo ven vecinos y visitantes",
      "No, es sólo decoración",
      "Sólo si lo hace el gobierno"
    ],
    "m": "Hay barrios que se volvieron circuitos turísticos por sus murales."
  },
  {
    "q": "¿Qué se construyó en los antiguos diques de Puerto Madero?",
    "ops": [
      "Oficinas, viviendas y espacios gastronómicos",
      "Fábricas nuevas",
      "Un puerto más grande"
    ],
    "m": "Es hoy uno de los barrios más caros de la ciudad."
  },
  {
    "q": "¿Qué es la Reserva Ecológica que está junto a Puerto Madero?",
    "ops": [
      "Un área natural formada sobre terrenos ganados al río",
      "Un parque diseñado desde cero",
      "Una isla natural"
    ],
    "m": "La naturaleza colonizó un relleno de origen artificial."
  },
  {
    "q": "¿Por qué las ciudades refuncionalizan zonas en desuso?",
    "ops": [
      "Porque aprovechan infraestructura que ya existe",
      "Porque es más barato demoler",
      "Porque lo exige la ley"
    ],
    "m": "Reutilizar suele costar menos que urbanizar desde cero."
  },
  {
    "q": "¿El arte urbano puede tener contenido político o social?",
    "ops": [
      "Sí, muchas veces es su razón de ser",
      "No, es sólo estético",
      "Sólo si lo encarga el Estado"
    ],
    "m": "Muchos murales denuncian o reivindican algo."
  },
  {
    "q": "¿Quiénes suelen quedar afuera de una renovación urbana?",
    "ops": [
      "Los vecinos de menores ingresos, por el aumento de los precios",
      "Los turistas",
      "Los comerciantes"
    ],
    "m": "Por eso la gentrificación es un tema de discusión pública."
  }
];
GAMES.puerto_madero_7 = juegoTriviaTexto(CUR_PUERTO_MADERO_7_BANCO, "Pensá cómo cambia la ciudad.", "puerto_mad");

/* 7° · La comunicación en el tiempo — comunicacion_tiempo_7
   DC: Avance de las tecnologías de comunicación; la historieta argentina
   Fuente: docs/auditoria-dc-caba/grado-7.md · CS9 */
const CUR_COMUNICACION_TIEMPO_7_BANCO = [
  {
    "items": [
      "La carta en papel",
      "El telégrafo",
      "El teléfono fijo",
      "El teléfono celular"
    ]
  },
  {
    "items": [
      "La imprenta de tipos móviles",
      "El diario impreso",
      "La radio",
      "La televisión"
    ]
  },
  {
    "items": [
      "El telégrafo",
      "El teléfono",
      "La radio",
      "Internet"
    ]
  },
  {
    "items": [
      "El diario en papel",
      "La radio a válvulas",
      "La televisión en blanco y negro",
      "La televisión en color"
    ]
  },
  {
    "items": [
      "La señal de humo",
      "La paloma mensajera",
      "El telégrafo",
      "El correo electrónico"
    ]
  },
  {
    "items": [
      "El disco de vinilo",
      "El casete",
      "El CD",
      "La música en streaming"
    ]
  },
  {
    "items": [
      "La máquina de escribir",
      "La computadora personal",
      "El teléfono inteligente",
      "El asistente con inteligencia artificial"
    ]
  },
  {
    "items": [
      "El cine mudo",
      "El cine sonoro",
      "La televisión",
      "Las plataformas de video"
    ]
  },
  {
    "items": [
      "El correo postal",
      "El fax",
      "El correo electrónico",
      "La mensajería instantánea"
    ]
  },
  {
    "items": [
      "La radio a galena",
      "La televisión abierta",
      "El cable",
      "El streaming"
    ]
  }
];
GAMES.comunicacion_tiempo_7 = juegoOrdenar(CUR_COMUNICACION_TIEMPO_7_BANCO, "Ordená del MÁS ANTIGUO al más nuevo. Tocá en orden.", "Cada tecnología nueva no borra a la anterior: convive con ella un tiempo.", "comunicaci");

/* 7° · Fuentes: ¿sustentable o no? — fuentes_sustentables_7
   DC: Tecnología: energía tradicional y alternativa; sobreexplotación
   Fuente: docs/auditoria-dc-caba/grado-7.md · T1 */
const CUR_FUENTES_SUSTENTABLES_7_BANCO = [
  {
    "it": "La energía solar",
    "cat": "renovable",
    "m": "El Sol no se agota en escala humana."
  },
  {
    "it": "El petróleo",
    "cat": "no_renovable",
    "m": "Tardó millones de años en formarse."
  },
  {
    "it": "La energía eólica",
    "cat": "renovable",
    "m": "El viento se renueva permanentemente."
  },
  {
    "it": "El carbón mineral",
    "cat": "no_renovable",
    "m": "Es un combustible fósil."
  },
  {
    "it": "La energía hidroeléctrica",
    "cat": "renovable",
    "m": "El ciclo del agua la repone, aunque la represa tenga impacto ambiental."
  },
  {
    "it": "El gas natural",
    "cat": "no_renovable",
    "m": "Otro combustible fósil."
  },
  {
    "it": "La energía geotérmica",
    "cat": "renovable",
    "m": "Aprovecha el calor del interior de la Tierra."
  },
  {
    "it": "El uranio de las centrales nucleares",
    "cat": "no_renovable",
    "m": "Es un mineral que se extrae y se agota, aunque no emita CO₂ al generar."
  },
  {
    "it": "La biomasa de residuos agrícolas",
    "cat": "renovable",
    "m": "Se repone con cada cosecha."
  },
  {
    "it": "El fuel oil de una central térmica",
    "cat": "no_renovable",
    "m": "Deriva del petróleo."
  },
  {
    "it": "La energía mareomotriz",
    "cat": "renovable",
    "m": "Aprovecha el movimiento de las mareas."
  },
  {
    "it": "El litio de las baterías",
    "cat": "no_renovable",
    "m": "Se extrae de salares y su explotación tiene fuerte impacto sobre el agua."
  },
  {
    "it": "Los paneles fotovoltaicos de un techo",
    "cat": "renovable",
    "m": "Convierten radiación solar, que no se agota."
  },
  {
    "it": "El gasoil de un generador",
    "cat": "no_renovable",
    "m": "Derivado del petróleo."
  },
  {
    "it": "Un parque eólico patagónico",
    "cat": "renovable",
    "m": "El viento del sur es constante y aprovechable."
  },
  {
    "it": "El carbón de una usina eléctrica",
    "cat": "no_renovable",
    "m": "Es la fuente fósil de mayor emisión por unidad de energía."
  }
];
GAMES.fuentes_sustentables_7 = juegoClasificar(CUR_FUENTES_SUSTENTABLES_7_BANCO, "¿La fuente se agota o se renueva?", [{"cat": "renovable", "label": "🌞 Renovable"}, {"cat": "no_renovable", "label": "🛢️ No renovable"}], "fuentes_su");

/* 7° · De la central al enchufe — central_enchufe_7
   DC: Tecnología: generación, transporte y distribución de la energía
   Fuente: docs/auditoria-dc-caba/grado-7.md · T2 */
const CUR_CENTRAL_ENCHUFE_7_BANCO = [
  {
    "q": "¿Cuál es el orden correcto del sistema eléctrico?",
    "ops": [
      "Generación → transporte → distribución → consumo",
      "Distribución → generación → consumo",
      "Consumo → transporte → generación"
    ],
    "m": "Primero se genera, después se lleva y al final se reparte."
  },
  {
    "q": "¿Por qué la electricidad se transporta en alta tensión?",
    "ops": [
      "Para perder menos energía en el camino",
      "Porque es más barato el cable",
      "Porque llega más rápido"
    ],
    "m": "A mayor tensión, menor corriente y menores pérdidas por calor."
  },
  {
    "q": "¿Qué hace un transformador?",
    "ops": [
      "Cambia el nivel de tensión",
      "Genera electricidad",
      "Almacena energía"
    ],
    "m": "Sube la tensión para transportar y la baja para distribuir."
  },
  {
    "q": "¿Qué es Yacyretá?",
    "ops": [
      "Una central hidroeléctrica binacional con Paraguay",
      "Una central nuclear",
      "Un parque solar"
    ],
    "m": "Es una de las mayores obras hidroeléctricas del país."
  },
  {
    "q": "¿Qué son Atucha y Embalse?",
    "ops": [
      "Centrales nucleares argentinas",
      "Represas",
      "Parques eólicos"
    ],
    "m": "La Argentina tiene tres centrales nucleares en operación."
  },
  {
    "q": "¿Qué es una central térmica?",
    "ops": [
      "Una que quema combustible para producir vapor y mover turbinas",
      "Una que usa el viento",
      "Una que usa el Sol"
    ],
    "m": "Es la que más aporta al sistema argentino."
  },
  {
    "q": "¿Qué diferencia hay entre generación centralizada y distribuida?",
    "ops": [
      "La distribuida produce cerca de donde se consume, en muchos puntos chicos",
      "La distribuida es más grande",
      "Son lo mismo"
    ],
    "m": "Los paneles en el techo de una casa son generación distribuida."
  },
  {
    "q": "¿Qué ventaja tiene la generación distribuida?",
    "ops": [
      "Reduce las pérdidas del transporte",
      "Genera más energía total",
      "No necesita mantenimiento"
    ],
    "m": "Si se consume donde se genera, no hay que transportarla."
  },
  {
    "q": "¿Qué es el sistema interconectado nacional?",
    "ops": [
      "La red que une generadoras y consumidores de todo el país",
      "Una central en particular",
      "El cableado de una ciudad"
    ],
    "m": "Permite compensar la demanda entre regiones."
  },
  {
    "q": "¿Por qué se producen cortes de luz en verano?",
    "ops": [
      "Porque la demanda supera la capacidad de la red",
      "Porque hace calor en los cables solamente",
      "Porque falta combustible"
    ],
    "m": "El pico de aire acondicionado sobrecarga la distribución."
  },
  {
    "q": "¿Qué mide un medidor eléctrico domiciliario?",
    "ops": [
      "La energía consumida, en kilovatios-hora",
      "La tensión de la línea",
      "La cantidad de aparatos"
    ],
    "m": "El kWh es una unidad de energía, no de potencia."
  },
  {
    "q": "¿Qué es la potencia de un artefacto?",
    "ops": [
      "La energía que consume por unidad de tiempo",
      "El total que consumió",
      "Su tamaño"
    ],
    "m": "Se mide en vatios; la energía, en vatios por hora."
  },
  {
    "q": "¿Un artefacto en stand-by consume energía?",
    "ops": [
      "Sí, poco pero constante",
      "No, nada",
      "Sólo si está encendido"
    ],
    "m": "Sumado en todos los aparatos y todo el año, no es despreciable."
  },
  {
    "q": "¿Para qué sirve la etiqueta de eficiencia energética?",
    "ops": [
      "Para comparar cuánto consume cada aparato",
      "Para saber el precio",
      "Para saber la garantía"
    ],
    "m": "Un aparato clase A consume mucho menos que uno clase G para lo mismo."
  }
];
GAMES.central_enchufe_7 = juegoTriviaTexto(CUR_CENTRAL_ENCHUFE_7_BANCO, "Seguí el camino de la electricidad.", "central_en");

/* 7° · Nodos, enlaces y capas de la red — capas_red_7
   DC: Tecnología: nodos y enlaces; infraestructura, plataforma y servicio; IoT
   Fuente: docs/auditoria-dc-caba/grado-7.md · T3 */
const CUR_CAPAS_RED_7_BANCO = [
  {
    "q": "¿Qué es un nodo en una red?",
    "ops": [
      "Un punto que se conecta con otros",
      "El cable que los une",
      "El centro de la red"
    ],
    "m": "El cable es el enlace; el nodo es el punto."
  },
  {
    "q": "¿Qué pasa si se corta un enlace en una red bien diseñada?",
    "ops": [
      "La información busca otro camino",
      "Se cae toda la red",
      "Se pierde para siempre"
    ],
    "m": "La redundancia de caminos es lo que hace robusta a internet."
  },
  {
    "q": "¿Internet tiene un centro que la controla?",
    "ops": [
      "No: es una red de redes descentralizada",
      "Sí, un servidor central",
      "Sí, un país"
    ],
    "m": "Ese diseño la hace muy difícil de apagar por completo."
  },
  {
    "q": "¿Qué es la capa de infraestructura?",
    "ops": [
      "Los cables, antenas y servidores físicos",
      "Las aplicaciones",
      "Los usuarios"
    ],
    "m": "Es lo material: sin eso no hay red."
  },
  {
    "q": "¿Qué es la capa de servicios o aplicaciones?",
    "ops": [
      "Lo que el usuario usa: buscadores, redes sociales, mensajería",
      "Los cables submarinos",
      "Los routers"
    ],
    "m": "Es la capa visible, montada sobre la infraestructura."
  },
  {
    "q": "¿Qué son los cables submarinos?",
    "ops": [
      "La infraestructura física que conecta continentes",
      "Cables de electricidad",
      "Antenas flotantes"
    ],
    "m": "La mayor parte del tráfico internacional viaja por ahí, no por satélite."
  },
  {
    "q": "¿Qué significa IoT o internet de las cosas?",
    "ops": [
      "Que objetos cotidianos se conectan a la red y envían datos",
      "Que hay más páginas web",
      "Que internet es más rápida"
    ],
    "m": "Una heladera o un reloj conectados son ejemplos."
  },
  {
    "q": "¿Qué es una dirección IP?",
    "ops": [
      "El número que identifica a un dispositivo en la red",
      "El nombre de una página",
      "La velocidad de la conexión"
    ],
    "m": "El nombre de la página es el dominio, que se traduce a una IP."
  },
  {
    "q": "¿Qué hace un router?",
    "ops": [
      "Decide por qué camino enviar los datos",
      "Genera la señal de internet",
      "Almacena las páginas"
    ],
    "m": "Enruta: de ahí su nombre."
  },
  {
    "q": "¿Qué es un servidor?",
    "ops": [
      "Una computadora que provee datos o servicios a otras",
      "Un cable",
      "Un usuario"
    ],
    "m": "Cuando abrís una página, tu dispositivo se la pide a un servidor."
  },
  {
    "q": "¿Los datos viajan enteros por un mismo camino?",
    "ops": [
      "No: se dividen en paquetes que pueden ir por rutas distintas",
      "Sí, siempre juntos",
      "Sólo los videos se dividen"
    ],
    "m": "Se reensamblan al llegar. Ése es el principio de la conmutación de paquetes."
  },
  {
    "q": "¿Qué riesgo trae el IoT?",
    "ops": [
      "Que dispositivos poco protegidos expongan datos",
      "Que la red sea más lenta",
      "Ninguno"
    ],
    "m": "Muchos vienen con contraseñas de fábrica que nadie cambia."
  },
  {
    "q": "¿Qué es el ancho de banda?",
    "ops": [
      "Cuántos datos pueden pasar por unidad de tiempo",
      "La distancia al servidor",
      "El tamaño del cable"
    ],
    "m": "Es lo que limita cuántas cosas podés hacer a la vez."
  },
  {
    "q": "Si una red tiene un solo camino entre dos nodos, ¿qué problema hay?",
    "ops": [
      "Si se corta, quedan incomunicados",
      "Es más rápida",
      "No hay problema"
    ],
    "m": "Por eso las redes reales tienen caminos alternativos."
  }
];
GAMES.capas_red_7 = juegoTriviaTexto(CUR_CAPAS_RED_7_BANCO, "Pensá cómo está armada internet.", "capas_red_");

/* 7° · Evento, acción y paralelismo — eventos_paralelismo_7
   DC: Tecnología: algoritmos no lineales, eventos y tareas en paralelo
   Fuente: docs/auditoria-dc-caba/grado-7.md · T4 */
const CUR_EVENTOS_PARALELISMO_7_BANCO = [
  {
    "q": "¿Qué es un evento en programación?",
    "ops": [
      "Algo que ocurre y dispara una acción",
      "Una variable",
      "Un error"
    ],
    "m": "«Al presionar una tecla» o «al tocar un objeto» son eventos."
  },
  {
    "q": "«Al presionar la bandera verde, mover 10 pasos.» ¿Qué es «al presionar»?",
    "ops": [
      "El evento",
      "La acción",
      "La condición"
    ],
    "m": "La acción es mover; el evento es lo que la dispara."
  },
  {
    "q": "¿Qué significa que dos personajes se muevan en paralelo?",
    "ops": [
      "Que sus programas se ejecutan al mismo tiempo",
      "Que uno espera al otro",
      "Que se mueven en línea recta"
    ],
    "m": "Cada uno corre su propia secuencia simultáneamente."
  },
  {
    "q": "¿Qué diferencia hay entre secuencial y paralelo?",
    "ops": [
      "En secuencial una cosa espera a la anterior; en paralelo van juntas",
      "El paralelo es más lento",
      "Son lo mismo"
    ],
    "m": "El paralelismo permite que varias cosas pasen a la vez."
  },
  {
    "q": "«Si toca el borde, rebotar.» ¿Qué estructura es?",
    "ops": [
      "Un condicional dentro de un bucle",
      "Una secuencia simple",
      "Un evento"
    ],
    "m": "Se evalúa la condición continuamente mientras el programa corre."
  },
  {
    "q": "¿Qué es un mensaje o «broadcast» entre objetos?",
    "ops": [
      "Una señal que un objeto envía y otros escuchan",
      "Un texto en pantalla",
      "Un error"
    ],
    "m": "Sirve para coordinar varios personajes sin que se toquen."
  },
  {
    "q": "Si dos programas modifican la misma variable a la vez, ¿qué puede pasar?",
    "ops": [
      "Un resultado inesperado",
      "Nada, siempre funciona",
      "El programa se acelera"
    ],
    "m": "Es uno de los problemas clásicos de la programación en paralelo."
  },
  {
    "q": "«Al recibir el mensaje “empezar”, mostrar el personaje.» ¿Qué es el mensaje?",
    "ops": [
      "El evento que dispara la acción",
      "La acción",
      "Una variable"
    ],
    "m": "El mensaje funciona como disparador."
  },
  {
    "q": "¿Un algoritmo con condicionales es lineal?",
    "ops": [
      "No: puede tomar caminos distintos",
      "Sí, siempre",
      "Sólo si tiene un condicional"
    ],
    "m": "El condicional es lo que lo vuelve no lineal."
  },
  {
    "q": "¿Para qué sirve un bucle «por siempre»?",
    "ops": [
      "Para que el programa esté atento todo el tiempo",
      "Para que termine antes",
      "Para contar"
    ],
    "m": "Se usa para chequear condiciones continuamente."
  },
  {
    "q": "¿Qué es depurar un programa?",
    "ops": [
      "Buscar y corregir sus errores",
      "Borrarlo",
      "Hacerlo más corto"
    ],
    "m": "Requiere leerlo paso a paso, no adivinar."
  },
  {
    "q": "Si dos programas paralelos terminan en distinto momento, ¿qué conviene?",
    "ops": [
      "Sincronizarlos con un mensaje o una espera",
      "Dejarlos así",
      "Volverlos secuenciales siempre"
    ],
    "m": "La sincronización es lo que evita resultados impredecibles."
  },
  {
    "q": "¿Un evento puede disparar varias acciones?",
    "ops": [
      "Sí, en distintos objetos a la vez",
      "No, sólo una",
      "Sólo dos"
    ],
    "m": "Ése es el uso típico del mensaje: uno avisa y muchos reaccionan."
  },
  {
    "q": "¿Qué ventaja tiene programar por eventos?",
    "ops": [
      "El programa responde a lo que pasa, sin adivinar el orden",
      "Es más corto siempre",
      "Corre más rápido"
    ],
    "m": "No hace falta prever de antemano en qué orden va a actuar el usuario."
  }
];
GAMES.eventos_paralelismo_7 = juegoTriviaTexto(CUR_EVENTOS_PARALELISMO_7_BANCO, "Pensá qué dispara cada acción.", "eventos_pa");

/* 7° · El dataset sesgado — dataset_sesgado_7
   DC: Tecnología: sesgo algorítmico; datos de entrenamiento; privacidad
   Fuente: docs/auditoria-dc-caba/grado-7.md · T5 */
const CUR_DATASET_SESGADO_7_BANCO = [
  {
    "q": "¿De dónde aprende un sistema de inteligencia artificial?",
    "ops": [
      "De los datos con los que lo entrenaron",
      "De internet en vivo siempre",
      "De nada: lo programan todo a mano"
    ],
    "m": "Los datos de entrenamiento determinan lo que puede reconocer."
  },
  {
    "q": "Un sistema entrenado sólo con fotos de perros, ¿reconoce gatos?",
    "ops": [
      "No, nunca los vio",
      "Sí, igual",
      "Sí, si son parecidos"
    ],
    "m": "Un modelo no puede reconocer lo que no estaba en sus datos."
  },
  {
    "q": "¿Qué es el sesgo algorítmico?",
    "ops": [
      "Cuando un sistema reproduce o amplifica desigualdades de sus datos",
      "Un error de programación",
      "Una falla del hardware"
    ],
    "m": "No es un bug: el sistema hace exactamente lo que aprendió."
  },
  {
    "q": "Si un sistema de selección de personal se entrena con currículums de una empresa que históricamente contrató varones, ¿qué pasa?",
    "ops": [
      "Tiende a favorecer currículums de varones",
      "Corrige la desigualdad solo",
      "No pasa nada"
    ],
    "m": "Aprende el patrón histórico y lo repite hacia adelante."
  },
  {
    "q": "¿Cómo se reduce un sesgo en los datos?",
    "ops": [
      "Revisando y equilibrando el conjunto de entrenamiento",
      "Usando una computadora más potente",
      "Agregando más datos iguales"
    ],
    "m": "Más datos del mismo tipo refuerzan el sesgo en vez de corregirlo."
  },
  {
    "q": "¿Una IA puede equivocarse con seguridad aparente?",
    "ops": [
      "Sí, puede dar una respuesta falsa con tono convincente",
      "No, siempre avisa",
      "Sólo si está rota"
    ],
    "m": "Por eso hay que verificar lo que produce."
  },
  {
    "q": "¿De quién es la responsabilidad si se publica algo falso generado por IA?",
    "ops": [
      "De quien lo publica",
      "De la IA",
      "De nadie"
    ],
    "m": "Usar una herramienta no traslada la responsabilidad."
  },
  {
    "q": "¿Qué son los datos personales?",
    "ops": [
      "Información que permite identificar a una persona",
      "Cualquier archivo",
      "Sólo el DNI"
    ],
    "m": "Nombre, dirección, foto, ubicación y hábitos entran ahí."
  },
  {
    "q": "Cuando una app pide acceso a tus contactos sin necesitarlo, ¿qué conviene?",
    "ops": [
      "No dárselo: pedí sólo lo necesario",
      "Dárselo siempre",
      "Desinstalar todas las apps"
    ],
    "m": "Cada permiso de más es información tuya circulando."
  },
  {
    "q": "¿Por qué muchos servicios digitales son gratis?",
    "ops": [
      "Porque su modelo de negocio usa los datos de los usuarios",
      "Porque son solidarios",
      "Porque no cuestan nada de hacer"
    ],
    "m": "La publicidad segmentada se paga con datos."
  },
  {
    "q": "¿Qué es entrenar un modelo?",
    "ops": [
      "Ajustarlo mostrándole muchos ejemplos",
      "Escribir sus reglas a mano",
      "Instalarlo"
    ],
    "m": "El modelo ajusta sus parámetros a partir de los ejemplos."
  },
  {
    "q": "Un sistema de reconocimiento facial que falla más con ciertos tonos de piel muestra…",
    "ops": [
      "Un sesgo en los datos de entrenamiento",
      "Un problema de la cámara",
      "Un error del usuario"
    ],
    "m": "Es un caso real y documentado de sesgo algorítmico."
  },
  {
    "q": "¿Conviene revisar lo que genera una IA antes de usarlo?",
    "ops": [
      "Sí, siempre",
      "No, si suena bien",
      "Sólo si es muy largo"
    ],
    "m": "Suena bien y ser correcto son dos cosas distintas."
  },
  {
    "q": "¿Qué significa que un dataset esté desbalanceado?",
    "ops": [
      "Que algunos casos están muy sobrerrepresentados y otros casi ausentes",
      "Que tiene pocos datos",
      "Que está desordenado"
    ],
    "m": "El modelo va a funcionar bien sólo con lo que vio mucho."
  }
];
GAMES.dataset_sesgado_7 = juegoTriviaTexto(CUR_DATASET_SESGADO_7_BANCO, "Pensá con qué datos aprendió el sistema.", "dataset_se");

/* 7° · De la máquina a la industria 4.0 — industria_40_7
   DC: Tecnología: sistemas de producción; configuración por el usuario
   Fuente: docs/auditoria-dc-caba/grado-7.md · T6 */
const CUR_INDUSTRIA_40_7_BANCO = [
  {
    "q": "¿Qué caracteriza a la producción artesanal?",
    "ops": [
      "Cada pieza la hace una persona y sale distinta",
      "Miles de piezas iguales por día",
      "Máquinas conectadas entre sí"
    ],
    "m": "El artesano controla todo el proceso."
  },
  {
    "q": "¿Qué introdujo la producción en serie?",
    "ops": [
      "Muchas unidades idénticas con división del trabajo",
      "Piezas únicas",
      "Máquinas que deciden solas"
    ],
    "m": "Cada operario hace una parte del proceso."
  },
  {
    "q": "¿Qué caracteriza a la industria 4.0?",
    "ops": [
      "Máquinas conectadas que intercambian datos y se ajustan",
      "Producción totalmente manual",
      "Producción en serie sin computadoras"
    ],
    "m": "Combina sensores, conectividad y análisis de datos."
  },
  {
    "q": "¿Qué es la personalización masiva?",
    "ops": [
      "Producir a gran escala pero adaptado a cada cliente",
      "Hacer todo igual",
      "Producir de a una pieza a mano"
    ],
    "m": "Es lo que la flexibilidad de la industria 4.0 hace posible."
  },
  {
    "q": "¿Qué papel cumplen los sensores en una fábrica 4.0?",
    "ops": [
      "Recogen datos del proceso en tiempo real",
      "Mueven las piezas",
      "Reemplazan a los operarios"
    ],
    "m": "Los datos permiten anticipar fallas y ajustar la producción."
  },
  {
    "q": "¿Qué es el mantenimiento predictivo?",
    "ops": [
      "Reparar antes de que la máquina falle, según los datos",
      "Reparar cuando se rompe",
      "No reparar nunca"
    ],
    "m": "Se anticipa a la falla en vez de reaccionar a ella."
  },
  {
    "q": "¿La automatización elimina todo el trabajo humano?",
    "ops": [
      "No: cambia qué tareas hacen las personas",
      "Sí, elimina todos los puestos",
      "No cambia nada"
    ],
    "m": "Aparecen tareas de supervisión, mantenimiento y análisis de datos."
  },
  {
    "q": "¿Qué es un producto configurable por el usuario?",
    "ops": [
      "Uno que el comprador ajusta a su necesidad antes de fabricarse",
      "Uno que viene en un solo modelo",
      "Uno hecho a mano"
    ],
    "m": "Elegir color, medidas o funciones antes de producirlo."
  },
  {
    "q": "¿Qué es un gemelo digital?",
    "ops": [
      "Una réplica virtual de una máquina o proceso para simularlo",
      "Una copia de seguridad",
      "Un robot idéntico"
    ],
    "m": "Permite probar cambios sin tocar la línea real."
  },
  {
    "q": "¿Qué necesita una máquina para integrarse a la industria 4.0?",
    "ops": [
      "Sensores y conectividad",
      "Ser más grande",
      "Ser más rápida"
    ],
    "m": "Sin datos ni conexión no puede integrarse al sistema."
  },
  {
    "q": "La impresión 3D en la industria permite…",
    "ops": [
      "Fabricar piezas únicas sin moldes",
      "Producir sólo en serie",
      "Reemplazar el diseño"
    ],
    "m": "Baja mucho el costo de hacer una sola pieza."
  },
  {
    "q": "¿Qué significa producción flexible?",
    "ops": [
      "Que la misma línea puede cambiar de producto rápidamente",
      "Que se produce despacio",
      "Que se produce a mano"
    ],
    "m": "La rigidez era el límite de la producción en serie clásica."
  },
  {
    "q": "¿Qué desafío social trae la automatización?",
    "ops": [
      "Que hace falta formar a las personas para las nuevas tareas",
      "Que baja la calidad",
      "Ninguno"
    ],
    "m": "El desplazamiento de puestos es real y requiere política pública."
  },
  {
    "q": "¿Qué es la trazabilidad de un producto?",
    "ops": [
      "Poder seguir su recorrido desde el origen hasta el consumidor",
      "Su precio final",
      "Su diseño"
    ],
    "m": "Los sistemas conectados la hacen posible en tiempo real."
  }
];
GAMES.industria_40_7 = juegoTriviaTexto(CUR_INDUSTRIA_40_7_BANCO, "Pensá cómo cambió el modo de producir.", "industria_");

/* 7° · Anticoncepción y prevención — anticoncepcion_7
   DC: Transversal ESI: métodos; ITS y VIH; el preservativo como doble prevención
   Fuente: docs/auditoria-dc-caba/grado-7.md · X1 */
const CUR_ANTICONCEPCION_7_BANCO = [
  {
    "q": "¿Qué método anticonceptivo es de larga duración?",
    "ops": [
      "El DIU",
      "El preservativo",
      "La anticoncepción de emergencia"
    ],
    "m": "El DIU se coloca y dura años; los otros son de uso puntual."
  },
  {
    "q": "Las pastillas anticonceptivas, ¿protegen de las ITS?",
    "ops": [
      "No: sólo previenen el embarazo",
      "Sí, de todas",
      "Sí, de algunas"
    ],
    "m": "Confundir esto es un riesgo real."
  },
  {
    "q": "¿Qué significa doble protección?",
    "ops": [
      "Usar preservativo más otro método anticonceptivo",
      "Usar dos preservativos",
      "Tomar dos pastillas"
    ],
    "m": "Usar dos preservativos a la vez es contraproducente: se rompen."
  },
  {
    "q": "¿Cómo se transmite el VIH?",
    "ops": [
      "Por relaciones sexuales sin protección, sangre y de madre a hijo",
      "Por saliva y abrazos",
      "Por compartir el baño"
    ],
    "m": "El contacto cotidiano NO lo transmite."
  },
  {
    "q": "¿El VIH y el sida son lo mismo?",
    "ops": [
      "No: el VIH es el virus y el sida es la etapa avanzada",
      "Sí, son sinónimos",
      "El sida es el virus y el VIH la enfermedad"
    ],
    "m": "Con tratamiento se puede vivir con VIH sin llegar nunca al sida."
  },
  {
    "q": "En la Argentina, ¿los métodos anticonceptivos en el sistema público son…?",
    "ops": [
      "Gratuitos",
      "Pagos",
      "Sólo para mayores de 21"
    ],
    "m": "La ley garantiza el acceso gratuito y la consulta confidencial."
  },
  {
    "q": "¿Desde qué edad se puede consultar sobre salud sexual sin autorización?",
    "ops": [
      "Desde los 13 años, por ley",
      "Recién a los 18",
      "Nunca sin un adulto"
    ],
    "m": "La ley reconoce autonomía progresiva en el cuidado de la salud."
  },
  {
    "q": "¿Qué es la anticoncepción de emergencia?",
    "ops": [
      "Un método para después de una relación sin protección, no de uso habitual",
      "Una pastilla de uso diario",
      "Un método que previene ITS"
    ],
    "m": "No reemplaza a un método regular ni protege de infecciones."
  },
  {
    "q": "¿Qué es el VPH?",
    "ops": [
      "Un virus de transmisión sexual muy frecuente",
      "Una bacteria del agua",
      "Una enfermedad hereditaria"
    ],
    "m": "Algunos tipos pueden derivar en cáncer; hay vacuna gratuita."
  },
  {
    "q": "¿Un test de VIH es confidencial?",
    "ops": [
      "Sí, y además es gratuito en el sistema público",
      "No, se informa a la familia",
      "Sólo si sos mayor de edad"
    ],
    "m": "La confidencialidad está protegida por ley."
  },
  {
    "q": "¿Cuál de estos NO es un método anticonceptivo?",
    "ops": [
      "Retirarse antes de eyacular",
      "El implante subdérmico",
      "El DIU"
    ],
    "m": "Retirarse antes no es un método: el riesgo de embarazo sigue existiendo."
  },
  {
    "q": "¿El preservativo tiene fecha de vencimiento?",
    "ops": [
      "Sí, y hay que revisarla antes de usarlo",
      "No",
      "Sólo si está abierto"
    ],
    "m": "También importa cómo se guardó: el calor lo daña."
  },
  {
    "q": "¿A quién se le puede consultar sobre estos temas?",
    "ops": [
      "A un profesional de la salud o un adulto de confianza",
      "A nadie",
      "Sólo a los amigos"
    ],
    "m": "La información confiable viene de fuentes que se pueden repreguntar."
  },
  {
    "q": "¿La ESI es obligatoria en las escuelas argentinas?",
    "ops": [
      "Sí, por la Ley 26.150",
      "No, es optativa",
      "Sólo en secundaria"
    ],
    "m": "Rige desde 2006 en todos los niveles."
  }
];
GAMES.anticoncepcion_7 = juegoTriviaTexto(CUR_ANTICONCEPCION_7_BANCO, "¿Qué previene cada método?", "anticoncep");

/* 7° · Señales de alerta en línea — alerta_en_linea_7
   DC: Transversal ESI + Digital: grooming como delito; qué hacer y dónde reportar
   Fuente: docs/auditoria-dc-caba/grado-7.md · X2 */
const CUR_ALERTA_EN_LINEA_7_BANCO = [
  {
    "q": "Un adulto que conociste en línea te pide que no le cuentes a nadie. ¿Qué es?",
    "ops": [
      "Una señal de alarma: hay que contarlo enseguida",
      "Una muestra de confianza",
      "Algo normal"
    ],
    "m": "El pedido de secreto frente a los adultos que te cuidan es la señal más clara."
  },
  {
    "q": "¿Cuál es una señal de alerta en un chat?",
    "ops": [
      "Que te pida guardar el secreto",
      "Que te mande un sticker",
      "Que escriba con faltas de ortografía"
    ],
    "m": "Pedir secreto es la señal más típica: te separa de los adultos que te cuidan."
  },
  {
    "q": "¿Dónde se puede denunciar en la Argentina?",
    "ops": [
      "En la línea 137 o en la fiscalía especializada",
      "En ningún lado",
      "Sólo en la escuela"
    ],
    "m": "Hay organismos del Estado dedicados específicamente a esto."
  },
  {
    "q": "Si alguien te presiona para que le mandes fotos íntimas, ¿qué hacés?",
    "ops": [
      "No mandarlas y contárselo a un adulto de confianza",
      "Mandarlas para que te deje en paz",
      "Bloquear y no decir nada"
    ],
    "m": "Ceder no termina la presión: la aumenta."
  },
  {
    "q": "Si ya mandaste una foto y te amenazan con difundirla, ¿qué hacés?",
    "ops": [
      "Contarlo enseguida: no es tu culpa y hay cómo ayudarte",
      "Pagar lo que piden",
      "Callarte por vergüenza"
    ],
    "m": "El silencio por vergüenza es exactamente lo que busca quien extorsiona."
  },
  {
    "q": "¿De quién es la responsabilidad si un adulto engaña a un menor?",
    "ops": [
      "Siempre del adulto",
      "Del menor por haber aceptado",
      "De los dos por igual"
    ],
    "m": "Esto es importante: la culpa nunca es del chico."
  },
  {
    "q": "Si alguien te incomoda por chat, ¿qué conviene hacer primero?",
    "ops": [
      "Contarle a un adulto de confianza y no borrar los mensajes",
      "Bloquear y borrar todo",
      "Contestarle para que pare"
    ],
    "m": "Los mensajes son la prueba: borrarlos deja la denuncia sin respaldo."
  },
  {
    "q": "¿Para qué sirve tener el perfil privado?",
    "ops": [
      "Para que sólo vean tus cosas quienes vos aceptás",
      "Para tener más seguidores",
      "Para que la app ande mejor"
    ],
    "m": "Reduce cuánta información tuya queda al alcance de desconocidos."
  },
  {
    "q": "¿Qué es el ciberacoso o ciberbullying?",
    "ops": [
      "Hostigamiento sostenido a alguien por medios digitales",
      "Una discusión aislada",
      "Un comentario negativo"
    ],
    "m": "Lo que lo define es la repetición y la intención de dañar."
  },
  {
    "q": "Si ves que hostigan a un compañero en un grupo, ¿qué conviene?",
    "ops": [
      "No reenviar y avisarle a un adulto",
      "Sumarte para no quedar afuera",
      "Ignorarlo"
    ],
    "m": "Reenviar amplifica el daño: quien reenvía también participa."
  },
  {
    "q": "¿Qué hacer antes de aceptar una solicitud de alguien que no conocés?",
    "ops": [
      "No aceptarla",
      "Aceptarla y ver qué pasa",
      "Preguntarle quién es"
    ],
    "m": "Un perfil se puede falsificar entero, incluida la foto y la edad."
  },
  {
    "q": "¿Sirve guardar capturas de una conversación que te preocupa?",
    "ops": [
      "Sí: son evidencia para la denuncia",
      "No, hay que borrar todo",
      "Sólo si es muy grave"
    ],
    "m": "Conservar la evidencia ayuda a la investigación."
  },
  {
    "q": "¿Qué es la huella digital?",
    "ops": [
      "El rastro que dejan tus publicaciones y actividad en línea",
      "Tu contraseña",
      "Tu dirección IP nada más"
    ],
    "m": "Puede quedar aunque borres el contenido original."
  },
  {
    "q": "Alguien desconocido te ofrece regalos o dinero por chat. ¿Qué es?",
    "ops": [
      "Una señal de alerta: hay que contarlo",
      "Una oportunidad",
      "Algo sin importancia"
    ],
    "m": "El regalo suele usarse para crear una deuda y sostener el contacto."
  }
];
GAMES.alerta_en_linea_7 = juegoTriviaTexto(CUR_ALERTA_EN_LINEA_7_BANCO, "¿Qué conviene hacer?", "alerta_en_");

/* 7° · Los nuevos derechos del 94 — derechos_94_7
   DC: Transversal FEC: reforma de 1994; ambiente, consumidor y datos personales
   Fuente: docs/auditoria-dc-caba/grado-7.md · X3 */
const CUR_DERECHOS_94_7_BANCO = [
  {
    "q": "¿En qué año se reformó por última vez la Constitución Nacional?",
    "ops": [
      "1994",
      "1853",
      "1983"
    ],
    "m": "1853 es la original; 1983 es la vuelta de la democracia."
  },
  {
    "q": "¿Qué derecho incorporó el artículo 41 de la Constitución?",
    "ops": [
      "El derecho a un ambiente sano",
      "El derecho al voto",
      "El derecho a la propiedad"
    ],
    "m": "También establece la obligación de recomponer el daño ambiental."
  },
  {
    "q": "¿Qué protege el artículo 42?",
    "ops": [
      "Los derechos de consumidores y usuarios",
      "El ambiente",
      "La libertad de prensa"
    ],
    "m": "Incluye información adecuada, trato digno y libertad de elección."
  },
  {
    "q": "¿Qué es el hábeas data?",
    "ops": [
      "El derecho a saber qué datos tuyos tiene alguien y a corregirlos",
      "El derecho a la libertad física",
      "Un impuesto"
    ],
    "m": "El que protege la libertad física es el hábeas corpus."
  },
  {
    "q": "¿Qué es el amparo?",
    "ops": [
      "Una acción judicial rápida para proteger un derecho vulnerado",
      "Un impuesto",
      "Una elección"
    ],
    "m": "Sirve cuando no hay otro camino legal más idóneo."
  },
  {
    "q": "¿Qué son los derechos de primera generación?",
    "ops": [
      "Los civiles y políticos, como votar o expresarse",
      "Los ambientales",
      "Los del consumidor"
    ],
    "m": "Son los más antiguos, ligados a la libertad individual."
  },
  {
    "q": "¿Qué son los derechos de segunda generación?",
    "ops": [
      "Los sociales, económicos y culturales, como salud y educación",
      "Los ambientales",
      "Los civiles"
    ],
    "m": "Aparecen con el Estado de bienestar."
  },
  {
    "q": "¿Qué son los derechos de tercera generación?",
    "ops": [
      "Los colectivos, como el ambiente sano y el patrimonio",
      "Los civiles",
      "Los políticos"
    ],
    "m": "Son de titularidad colectiva: le pertenecen a la comunidad."
  },
  {
    "q": "Los tratados de derechos humanos incorporados en 1994 tienen…",
    "ops": [
      "Jerarquía constitucional",
      "Menos valor que una ley común",
      "Valor sólo simbólico"
    ],
    "m": "Están al mismo nivel que la Constitución."
  },
  {
    "q": "¿Qué reconoce la Constitución sobre los pueblos indígenas desde 1994?",
    "ops": [
      "Su preexistencia étnica y cultural y sus derechos sobre las tierras",
      "Nada",
      "Sólo su historia"
    ],
    "m": "Es el artículo 75, inciso 17."
  },
  {
    "q": "Si una empresa te vende algo defectuoso, ¿qué derecho te ampara?",
    "ops": [
      "El de consumidor, del artículo 42",
      "El de ambiente sano",
      "El hábeas data"
    ],
    "m": "Incluye el derecho a la reparación."
  },
  {
    "q": "Si una empresa guarda datos tuyos que son incorrectos, ¿qué podés hacer?",
    "ops": [
      "Pedir que los corrijan mediante el hábeas data",
      "Nada",
      "Presentar un amparo ambiental"
    ],
    "m": "El derecho incluye acceder, rectificar y suprimir."
  },
  {
    "q": "¿Qué figuras de participación ciudadana incorporó la reforma?",
    "ops": [
      "La iniciativa popular y la consulta popular",
      "El voto obligatorio",
      "El servicio militar"
    ],
    "m": "Permiten a la ciudadanía proponer leyes y ser consultada."
  },
  {
    "q": "Una fábrica contamina un río del barrio. ¿Qué derecho se vulnera?",
    "ops": [
      "El derecho a un ambiente sano",
      "El derecho al voto",
      "El derecho de propiedad"
    ],
    "m": "Y el que contamina tiene obligación de recomponer."
  }
];
GAMES.derechos_94_7 = juegoTriviaTexto(CUR_DERECHOS_94_7_BANCO, "¿Qué derecho está en juego?", "derechos_9");

/* 7° · El gobierno de la Ciudad — gobierno_ciudad_7
   DC: Transversal FEC: división de poderes en CABA; Legislatura; comunas
   Fuente: docs/auditoria-dc-caba/grado-7.md · X4 */
const CUR_GOBIERNO_CIUDAD_7_BANCO = [
  {
    "q": "¿Desde cuándo la Ciudad de Buenos Aires es autónoma?",
    "ops": [
      "Desde la reforma constitucional de 1994",
      "Desde 1880",
      "Desde 1853"
    ],
    "m": "En 1880 fue federalizada, pero la autonomía llegó recién en 1994."
  },
  {
    "q": "¿Cómo se llama el poder legislativo de la Ciudad?",
    "ops": [
      "La Legislatura",
      "El Congreso",
      "El Concejo Deliberante"
    ],
    "m": "El Congreso es nacional; el Concejo Deliberante es de los municipios."
  },
  {
    "q": "¿Quién encabeza el poder ejecutivo de la Ciudad?",
    "ops": [
      "El Jefe o Jefa de Gobierno",
      "El intendente",
      "El gobernador"
    ],
    "m": "Se elige por voto directo cada cuatro años."
  },
  {
    "q": "¿En cuántas comunas está dividida la Ciudad?",
    "ops": [
      "Quince",
      "Cuarenta y ocho",
      "Cinco"
    ],
    "m": "Cuarenta y ocho son los barrios, que se agrupan en las quince comunas."
  },
  {
    "q": "¿Qué es una comuna?",
    "ops": [
      "Una unidad de gestión descentralizada con autoridades elegidas",
      "Un barrio",
      "Una escuela"
    ],
    "m": "Cada una tiene una Junta Comunal de siete miembros elegidos por voto."
  },
  {
    "q": "¿Cuántos legisladores tiene la Legislatura porteña?",
    "ops": [
      "Sesenta",
      "Treinta",
      "Cien"
    ],
    "m": "Se renueva por mitades cada dos años."
  },
  {
    "q": "¿Qué hace el Poder Judicial de la Ciudad?",
    "ops": [
      "Resuelve conflictos aplicando las leyes porteñas",
      "Sanciona leyes",
      "Administra la Ciudad"
    ],
    "m": "Cada poder tiene su función y no invade la de los otros."
  },
  {
    "q": "¿La Ciudad tiene su propia Constitución?",
    "ops": [
      "Sí, desde 1996",
      "No, se rige sólo por la Nacional",
      "Sólo un estatuto"
    ],
    "m": "Es consecuencia de la autonomía reconocida en 1994."
  },
  {
    "q": "¿Qué es el presupuesto participativo?",
    "ops": [
      "Un mecanismo para que los vecinos decidan parte del gasto público",
      "El sueldo de los legisladores",
      "Un impuesto"
    ],
    "m": "Es una forma de participación ciudadana directa."
  },
  {
    "q": "¿Quién controla el gasto del gobierno porteño?",
    "ops": [
      "La Auditoría General de la Ciudad",
      "La Legislatura sola",
      "El Jefe de Gobierno"
    ],
    "m": "Los organismos de control son parte del sistema de pesos y contrapesos."
  },
  {
    "q": "¿Para qué sirve la división de poderes?",
    "ops": [
      "Para que ninguno concentre todo el poder",
      "Para que haya más empleados",
      "Para hacer más rápido el trámite"
    ],
    "m": "Cada poder controla a los otros dos."
  },
  {
    "q": "¿A partir de qué edad se puede votar en la Argentina?",
    "ops": [
      "Desde los 16, de manera optativa",
      "Recién a los 18",
      "Desde los 21"
    ],
    "m": "Desde 2012 el voto es optativo entre los 16 y los 17 años."
  },
  {
    "q": "¿Qué es el Defensor del Pueblo?",
    "ops": [
      "Un organismo que defiende los derechos de los habitantes frente al Estado",
      "Un juez",
      "Un legislador"
    ],
    "m": "Actúa con independencia de los tres poderes."
  },
  {
    "q": "Si querés reclamar por una plaza rota de tu barrio, ¿adónde vas primero?",
    "ops": [
      "A la Junta Comunal de tu comuna",
      "Al Congreso Nacional",
      "A la Corte Suprema"
    ],
    "m": "Las comunas existen justamente para acercar la gestión al vecino."
  }
];
GAMES.gobierno_ciudad_7 = juegoTriviaTexto(CUR_GOBIERNO_CIUDAD_7_BANCO, "¿Quién hace qué en la Ciudad?", "gobierno_c");

/* 7° · Presupuesto con inflación — presupuesto_inflacion_7
   DC: Transversal Financiera: presupuesto, inflación e interés simple
   Fuente: docs/auditoria-dc-caba/grado-7.md · X5 */
const CUR_PRESUPUESTO_INFLACION_7_PLANTILLA = {
  "q": "Una zapatilla cuesta ${a} y en el mes aumenta un {p}%. ¿Cuánto va a costar?",
  "vars": {
    "a": {
      "rango": [
        5000,
        60000
      ],
      "paso": 500
    },
    "p": {
      "opciones": [
        10,
        20,
        25,
        50
      ]
    }
  },
  "ok": "a + a * p / 100",
  "distractores": [
    "a * p / 100",
    "a - a * p / 100",
    "a + p"
  ],
  "tope": 200000,
  "m": "El aumento es ${a} × {p} ÷ 100, y hay que SUMARLO al precio. Queda ${ok}. Contestar sólo el aumento es el error más común."
};
GAMES.presupuesto_inflacion_7 = juegoParametrico(CUR_PRESUPUESTO_INFLACION_7_PLANTILLA, "¿Cuánto va a costar después del aumento?", "presupuest");

/* 7° · Matriz energética y transición — matriz_energetica_7
   DC: Transversal Ambiental: transición energética; mitigación y adaptación
   Fuente: docs/auditoria-dc-caba/grado-7.md · X6 */
const CUR_MATRIZ_ENERGETICA_7_BANCO = [
  {
    "q": "¿Qué es la matriz energética de un país?",
    "ops": [
      "La proporción de cada fuente en el total que consume",
      "La cantidad total de energía",
      "El precio de la energía"
    ],
    "m": "Muestra de qué depende ese país para funcionar."
  },
  {
    "q": "Reemplazar una central a carbón por un parque eólico es una medida de…",
    "ops": [
      "Mitigación",
      "Adaptación",
      "Ninguna de las dos"
    ],
    "m": "Reduce las emisiones, o sea la causa del problema."
  },
  {
    "q": "Construir defensas contra inundaciones es una medida de…",
    "ops": [
      "Adaptación",
      "Mitigación",
      "Ninguna de las dos"
    ],
    "m": "No reduce emisiones: prepara para las consecuencias."
  },
  {
    "q": "¿Qué es la transición energética?",
    "ops": [
      "El pasaje de una matriz basada en fósiles a una con más renovables",
      "Consumir menos energía nada más",
      "Cerrar todas las centrales"
    ],
    "m": "Es un proceso gradual, no un apagón."
  },
  {
    "q": "¿Qué fuente domina hoy la matriz energética argentina?",
    "ops": [
      "El gas natural",
      "La energía solar",
      "La nuclear"
    ],
    "m": "Los fósiles siguen siendo la mayor parte, con el gas a la cabeza."
  },
  {
    "q": "¿Qué es el Acuerdo de París?",
    "ops": [
      "Un acuerdo internacional para limitar el calentamiento global",
      "Un tratado comercial",
      "Un acuerdo militar"
    ],
    "m": "Se firmó en 2015 y cada país presenta sus propias metas."
  },
  {
    "q": "Plantar árboles en una ciudad es sobre todo una medida de…",
    "ops": [
      "Las dos: absorbe CO₂ y baja la temperatura urbana",
      "Sólo mitigación",
      "Sólo adaptación"
    ],
    "m": "Algunas medidas cumplen las dos funciones a la vez."
  },
  {
    "q": "¿Por qué es difícil almacenar energía solar y eólica?",
    "ops": [
      "Porque no se generan de manera constante",
      "Porque son muy caras",
      "Porque contaminan"
    ],
    "m": "La intermitencia es su principal desafío técnico."
  },
  {
    "q": "¿La energía nuclear emite gases de efecto invernadero al generar?",
    "ops": [
      "Prácticamente no, aunque tiene otros problemas",
      "Sí, más que el carbón",
      "Sí, igual que el gas"
    ],
    "m": "Su discusión pasa por los residuos y la seguridad."
  },
  {
    "q": "Mejorar la aislación de las casas es una medida de…",
    "ops": [
      "Mitigación: se necesita menos energía para climatizar",
      "Sólo adaptación",
      "Ninguna"
    ],
    "m": "Menos consumo es menos emisión."
  },
  {
    "q": "¿Qué es la eficiencia energética?",
    "ops": [
      "Obtener el mismo servicio usando menos energía",
      "Consumir menos aunque se viva peor",
      "Producir más energía"
    ],
    "m": "Es la forma más barata de reducir emisiones."
  },
  {
    "q": "Cambiar los cultivos por variedades resistentes a la sequía es…",
    "ops": [
      "Adaptación",
      "Mitigación",
      "Eficiencia"
    ],
    "m": "Prepara la producción para condiciones que ya están cambiando."
  },
  {
    "q": "¿Qué es Vaca Muerta?",
    "ops": [
      "Una formación de hidrocarburos no convencionales en Neuquén",
      "Un parque eólico",
      "Una central nuclear"
    ],
    "m": "Es central en el debate sobre la matriz energética argentina."
  },
  {
    "q": "¿Se puede hacer sólo mitigación y no adaptación?",
    "ops": [
      "No: parte del cambio ya está en curso y hay que adaptarse igual",
      "Sí, alcanza con mitigar",
      "Sí, la adaptación es opcional"
    ],
    "m": "Aun con emisiones cero, los efectos acumulados siguen."
  }
];
GAMES.matriz_energetica_7 = juegoTriviaTexto(CUR_MATRIZ_ENERGETICA_7_BANCO, "¿Reduce las causas o prepara para las consecuencias?", "matriz_ene");

/* 7° · ¿Quién es la fuente? — fuente_licencias_7
   DC: Transversal Digital: autoría incluida la de IA; desinformación; licencias
   Fuente: docs/auditoria-dc-caba/grado-7.md · X7 */
const CUR_FUENTE_LICENCIAS_7_BANCO = [
  {
    "q": "¿Qué es una fake news?",
    "ops": [
      "Información falsa presentada como noticia",
      "Una noticia vieja",
      "Una noticia de otro país"
    ],
    "m": "Imita el formato de una noticia para parecer creíble."
  },
  {
    "q": "Antes de reenviar algo que te llegó, ¿qué conviene hacer?",
    "ops": [
      "Verificar la fuente y la fecha",
      "Reenviarlo rápido",
      "Reenviarlo sólo a amigos"
    ],
    "m": "Reenviar sin verificar es lo que hace circular la desinformación."
  },
  {
    "q": "¿Qué es una imagen sacada de contexto?",
    "ops": [
      "Una foto real usada para ilustrar un hecho distinto",
      "Una foto falsa",
      "Una foto con mala calidad"
    ],
    "m": "Es una de las formas más comunes y difíciles de detectar."
  },
  {
    "q": "¿Qué es una licencia Creative Commons?",
    "ops": [
      "Un permiso que el autor da para reusar su obra con ciertas condiciones",
      "Una prohibición total",
      "Un impuesto"
    ],
    "m": "Hay variantes: algunas exigen atribución, otras prohíben el uso comercial."
  },
  {
    "q": "Si una obra no dice nada sobre su licencia, ¿se puede usar libremente?",
    "ops": [
      "No: por defecto los derechos están reservados",
      "Sí, si no dice nada es libre",
      "Sí, si es de internet"
    ],
    "m": "El derecho de autor no hace falta declararlo para existir."
  },
  {
    "q": "¿Qué es el dominio público?",
    "ops": [
      "Obras cuyos derechos de autor ya vencieron y se pueden usar libremente",
      "Cualquier cosa que esté en internet",
      "Las obras del Estado"
    ],
    "m": "En la Argentina son 70 años después de la muerte del autor."
  },
  {
    "q": "¿Qué significa «atribución» en una licencia?",
    "ops": [
      "Que hay que citar al autor original",
      "Que no se puede usar",
      "Que hay que pagar"
    ],
    "m": "Es la condición más común de las licencias libres."
  },
  {
    "q": "Un texto generado por IA, ¿se puede publicar como propio?",
    "ops": [
      "Conviene aclararlo: la autoría es información relevante",
      "Sí, sin decir nada",
      "No se puede publicar nunca"
    ],
    "m": "Transparentar cómo se produjo es parte de la honestidad intelectual."
  },
  {
    "q": "¿Qué es un deepfake?",
    "ops": [
      "Un video o audio falso generado con IA que imita a una persona real",
      "Un video de mala calidad",
      "Una película animada"
    ],
    "m": "Cada vez son más difíciles de distinguir a simple vista."
  },
  {
    "q": "Si un titular te genera mucha indignación de golpe, ¿qué conviene?",
    "ops": [
      "Sospechar y verificar antes de compartir",
      "Compartirlo enseguida",
      "Confiar en la emoción"
    ],
    "m": "La desinformación se diseña para provocar reacción inmediata."
  },
  {
    "q": "¿Qué es una fuente primaria?",
    "ops": [
      "El documento o testimonio original",
      "Un resumen de otro",
      "Una opinión"
    ],
    "m": "Ir a la fuente primaria evita el teléfono descompuesto."
  },
  {
    "q": "¿Sirve buscar la misma noticia en otros medios?",
    "ops": [
      "Sí, contrastar es la mejor verificación",
      "No, siempre dicen lo mismo",
      "Sólo si es internacional"
    ],
    "m": "Si nadie más la publica, conviene desconfiar."
  },
  {
    "q": "¿Se puede usar una foto de internet en un trabajo escolar?",
    "ops": [
      "Sí, citando la fuente y respetando su licencia",
      "Sí, sin más",
      "No, nunca"
    ],
    "m": "Citar es lo mínimo, y algunas licencias piden más."
  },
  {
    "q": "¿Qué es la búsqueda inversa de imágenes?",
    "ops": [
      "Buscar dónde apareció antes una foto para ver su contexto original",
      "Buscar imágenes por color",
      "Ampliar una imagen"
    ],
    "m": "Es la herramienta más útil para detectar fotos fuera de contexto."
  }
];
GAMES.fuente_licencias_7 = juegoTriviaTexto(CUR_FUENTE_LICENCIAS_7_BANCO, "Antes de compartir, verificá.", "fuente_lic");

/* 7° · ¿Consumo o consumismo? — consumo_consumismo_7
   DC: Transversal Consumos: consumo problemático; apuestas online; estafas
   Fuente: docs/auditoria-dc-caba/grado-7.md · X8 */
const CUR_CONSUMO_CONSUMISMO_7_BANCO = [
  {
    "it": "Comprar zapatillas nuevas porque las viejas están rotas",
    "cat": "necesario",
    "m": "Cubre una necesidad concreta."
  },
  {
    "it": "Comprar el mismo modelo de siempre pero de otro color, sólo porque salió",
    "cat": "consumismo",
    "m": "No hay necesidad: la impulsa el recambio permanente."
  },
  {
    "it": "Apostar plata en línea todas las semanas y esconderlo",
    "cat": "problematico",
    "m": "El ocultamiento es una de las señales de alerta más claras."
  },
  {
    "it": "Comprar los útiles al empezar las clases",
    "cat": "necesario",
    "m": "Responde a una necesidad real."
  },
  {
    "it": "Cambiar el celular cada seis meses porque salió uno nuevo",
    "cat": "consumismo",
    "m": "El recambio no responde a una falla del anterior."
  },
  {
    "it": "No poder dejar de jugar aunque se pierda plata que hace falta",
    "cat": "problematico",
    "m": "La pérdida de control es lo que lo define."
  },
  {
    "it": "Comprar comida para la semana",
    "cat": "necesario",
    "m": "Es consumo básico y planificado."
  },
  {
    "it": "Comprar algo sólo porque estaba en oferta y después no usarlo",
    "cat": "consumismo",
    "m": "La oferta creó el deseo, no la necesidad."
  },
  {
    "it": "Pasar tantas horas en un juego que se abandonan la escuela y los amigos",
    "cat": "problematico",
    "m": "Cuando afecta otras áreas de la vida, es problemático."
  },
  {
    "it": "Comprar un abrigo antes del invierno",
    "cat": "necesario",
    "m": "Previsión de una necesidad real."
  },
  {
    "it": "Comprar por impulso cada vez que se entra a una app de compras",
    "cat": "consumismo",
    "m": "El diseño de la app empuja la compra impulsiva."
  },
  {
    "it": "Pedir prestado para seguir apostando",
    "cat": "problematico",
    "m": "Endeudarse para sostener la conducta es una señal grave."
  },
  {
    "it": "Reponer un producto de limpieza que se terminó",
    "cat": "necesario",
    "m": "Consumo de reposición."
  },
  {
    "it": "Comprar la ropa que usa un influencer para parecerse a él",
    "cat": "consumismo",
    "m": "La compra busca pertenencia, no utilidad."
  },
  {
    "it": "Sentir angustia si no se puede entrar a apostar",
    "cat": "problematico",
    "m": "La angustia por la abstinencia es un indicador claro."
  },
  {
    "it": "Comprar los remedios recetados",
    "cat": "necesario",
    "m": "Es una necesidad de salud."
  },
  {
    "it": "Comprar algo sólo porque queda poco stock",
    "cat": "consumismo",
    "m": "La escasez artificial es un recurso de venta muy usado."
  },
  {
    "it": "Ocultarle a la familia cuánto se gasta en un juego",
    "cat": "problematico",
    "m": "El ocultamiento acompaña casi siempre al consumo problemático."
  }
];
GAMES.consumo_consumismo_7 = juegoClasificar(CUR_CONSUMO_CONSUMISMO_7_BANCO, "¿Cubre una necesidad o responde a un impulso?", [{"cat": "necesario", "label": "✅ Consumo necesario"}, {"cat": "consumismo", "label": "🌀 Consumismo"}, {"cat": "problematico", "label": "⚠️ Consumo problemático"}], "consumo_co");

/* Pozo de preguntas del DUELO, por grado — generado junto con los bancos.
   Referencias a los arrays de arriba, no copias. Lo consume actividades_duelo.js. */
const CUR_DUELO_POR_GRADO = {
  1: [["cdm", CUR_OBJETO_MATERIAL_BANCO], ["lengua", CUR_SUENA_IGUAL_BANCO], ["lengua", CUR_SILABAS_1_BANCO], ["lengua", CUR_PAREJAS_LETRAS_1_BANCO], ["lengua", CUR_DESPEGAR_PALABRAS_1_BANCO], ["lengua", CUR_MAYUSCULA_PUNTO_1_BANCO], ["lengua", CUR_LEER_ENCONTRAR_1_BANCO], ["lengua", CUR_LEO_RESPONDO_1_BANCO], ["lengua", CUR_ARTICULOS_1_BANCO], ["matematica", CUR_ARMAR_CALCULO_1_BANCO], ["matematica", CUR_DONDE_ESTA_1_BANCO], ["matematica", CUR_FIGURAS_1_BANCO], ["matematica", CUR_CUERPOS_1_BANCO], ["matematica", CUR_MEDIR_CLIPS_1_BANCO], ["matematica", CUR_CALENDARIO_1_BANCO], ["cdm", CUR_CUIDARNOS_1_BANCO], ["logica", CUR_OFICIOS_1_BANCO], ["logica", CUR_ANTES_AHORA_1_BANCO], ["logica", CUR_ICONOS_1_BANCO], ["logica", CUR_VIAL_1_BANCO], ["cdm", CUR_PLANTA_PARTES_1_BANCO], ["cdm", CUR_CUERPO_ETAPAS_1_BANCO]],
  2: [["cdm", CUR_LUZ_PROPIA_BANCO], ["matematica", CUR_QUE_CUENTA_RESUELVE_BANCO], ["matematica", CUR_ADIVINA_FIGURA_BANCO], ["lengua", CUR_SILABAS_2_BANCO], ["lengua", CUR_PARES_MINIMOS_2_BANCO], ["lengua", CUR_MB_NV_H_2_BANCO], ["lengua", CUR_ACENTUACION_2_BANCO], ["lengua", CUR_SIGNOS_2_BANCO], ["lengua", CUR_SEPARAR_PALABRAS_2_BANCO], ["lengua", CUR_BUSCAR_DATO_2_BANCO], ["lengua", CUR_CONECTORES_2_BANCO], ["lengua", CUR_DICTADO_2_BANCO], ["lengua", CUR_VOCABULARIO_2_BANCO], ["logica", CUR_BUCLE_2_BANCO], ["logica", CUR_CONDICIONAL_2_BANCO], ["matematica", CUR_REPARTO_2_BANCO], ["matematica", CUR_POSICIONES_2_BANCO], ["matematica", CUR_MEDIR_REGLA_2_BANCO], ["cdm", CUR_VIAL_2_BANCO], ["cdm", CUR_CONVIVENCIA_2_BANCO]],
  3: [["cdm", CUR_DERECHOS_ESCENARIOS_BANCO], ["lengua", CUR_TILDE_PASADO_3_BANCO], ["lengua", CUR_DIALOGO_SIGNOS_3_BANCO], ["lengua", CUR_POEMA_3_BANCO], ["lengua", CUR_CONECTORES_3_BANCO], ["lengua", CUR_DERIVADAS_3_BANCO], ["lengua", CUR_HIATO_DIPTONGO_3_BANCO], ["cdm", CUR_CONSTELACIONES_3_BANCO], ["matematica", CUR_BANDEJA_HUEVOS_3_BANCO], ["matematica", CUR_CUADRICULA_3_BANCO], ["matematica", CUR_FIGURAS_3_BANCO], ["matematica", CUR_MEDIR_3_BANCO], ["logica", CUR_BUGS_3_BANCO], ["logica", CUR_CONTADOR_3_BANCO], ["logica", CUR_MUNDO_DIGITAL_3_BANCO], ["logica", CUR_CON_QUE_SE_MUEVE_3_BANCO]],
  4: [["sociales", CUR_GOBIERNO_ARGENTINA_BANCO], ["naturales", CUR_ESTADOS_AGUA_4_BANCO], ["naturales", CUR_PLACAS_4_BANCO], ["naturales", CUR_MOVIMIENTO_CUERPO_4_BANCO], ["naturales", CUR_IMANES_4_BANCO], ["naturales", CUR_CIELO_4_BANCO], ["lengua", CUR_TIEMPOS_VERBALES_4_BANCO], ["lengua", CUR_HIPERONIMOS_4_BANCO], ["lengua", CUR_HOMOFONOS_4_BANCO], ["lengua", CUR_GRUPOS_ORTOGRAFICOS_4_BANCO], ["lengua", CUR_PARATEXTO_4_BANCO], ["lengua", CUR_PROPOSITO_TEXTO_4_BANCO], ["lengua", CUR_HISTORIETA_4_BANCO], ["sociales", CUR_AMERICA_1492_4_BANCO], ["sociales", CUR_SOCIEDAD_COLONIAL_4_BANCO], ["naturales", CUR_MECANISMOS_4_BANCO], ["sociales", CUR_CONVIVENCIA_4_BANCO], ["matematica", CUR_VALOR_POSICIONAL_4_BANCO], ["matematica", CUR_CUERPOS_CARAS_4_BANCO], ["matematica", CUR_EQUIVALENCIAS_MEDIDA_4_BANCO], ["sociales", CUR_CAPITALES_4_BANCO]],
  5: [["lengua", CUR_OD_OI_5_BANCO], ["lengua", CUR_GRADOS_ADJETIVO_5_BANCO], ["lengua", CUR_FUTURO_CONDICIONAL_5_BANCO], ["lengua", CUR_HOMOFONOS_5_BANCO], ["lengua", CUR_ACENTUACION_5_BANCO], ["lengua", CUR_PREFIJOS_5_BANCO], ["lengua", CUR_POLISEMIA_5_BANCO], ["lengua", CUR_DOS_PUNTOS_5_BANCO], ["matematica", CUR_ROMANOS_5_BANCO], ["matematica", CUR_DIVISIBILIDAD_5_BANCO], ["matematica", CUR_GRAFICOS_5_BANCO], ["naturales", CUR_DISOLUCION_5_BANCO], ["naturales", CUR_SONIDO_5_BANCO], ["sociales", CUR_ASAMBLEA_XIII_5_BANCO], ["sociales", CUR_PROCERES_5_BANCO], ["sociales", CUR_MAPA_AMERICA_5_BANCO], ["logica", CUR_VARIABLES_5_BANCO], ["logica", CUR_SENSORES_5_BANCO], ["matematica", CUR_RECTA_MILLON_5_BANCO], ["matematica", CUR_GEOMETRIA_5_BANCO], ["naturales", CUR_ECLIPSES_5_BANCO], ["lengua", CUR_CLUB_LECTURA_5_BANCO]],
  6: [["sociales", CUR_RECURSOS_ARGENTINA_BANCO], ["matematica", CUR_PRIMOS_6_BANCO], ["matematica", CUR_FRACCIONES_EQUIVALENTES_6_BANCO], ["matematica", CUR_DENSIDAD_RECTA_6_BANCO], ["matematica", CUR_SUMA_FRACCIONES_6_BANCO], ["matematica", CUR_FRACCION_INVERSA_6_BANCO], ["matematica", CUR_AREA_FRACCIONARIA_6_BANCO], ["matematica", CUR_CORREDOR_COMA_6_BANCO], ["matematica", CUR_MULTIPLICAR_COMA_6_BANCO], ["matematica", CUR_CUADRILATEROS_6_BANCO], ["matematica", CUR_DESARROLLOS_6_BANCO], ["matematica", CUR_AREA_PERIMETRO_6_BANCO], ["matematica", CUR_MODA_ENCUESTA_6_BANCO], ["lengua", CUR_COMPRENSION_LECTORA_6_BANCO], ["lengua", CUR_IDEA_PRINCIPAL_6_BANCO], ["lengua", CUR_NOTICIA_PARTES_6_BANCO], ["lengua", CUR_CIENCIA_FICCION_6_BANCO], ["lengua", CUR_FUENTE_CONFIABLE_6_BANCO], ["lengua", CUR_DIRECTO_INDIRECTO_6_BANCO], ["lengua", CUR_SINTAGMA_6_BANCO], ["lengua", CUR_OD_OI_6_BANCO], ["lengua", CUR_COHESION_6_BANCO], ["lengua", CUR_RECURSOS_POETICOS_6_BANCO], ["lengua", CUR_CONJUGACION_6_BANCO], ["lengua", CUR_TILDES_6_BANCO], ["lengua", CUR_PUNTUACION_6_BANCO], ["naturales", CUR_RED_ECOSISTEMA_6_BANCO], ["naturales", CUR_PUBERTAD_6_BANCO], ["naturales", CUR_CICLO_MENSTRUAL_6_BANCO], ["naturales", CUR_CIGOTO_FETO_6_BANCO], ["naturales", CUR_PARTICULAS_CALOR_6_BANCO], ["naturales", CUR_MATERIAL_TERMICO_6_BANCO], ["naturales", CUR_HELIOCENTRISMO_6_BANCO], ["naturales", CUR_EFECTO_INVERNADERO_6_BANCO], ["sociales", CUR_ESTADO_AGROEXPORTACION_6_BANCO], ["sociales", CUR_INMIGRACION_CENSOS_6_BANCO], ["sociales", CUR_VOTO_6_BANCO], ["sociales", CUR_GRAN_GUERRA_CRISIS_6_BANCO], ["sociales", CUR_MERCOSUR_ENERGIA_6_BANCO], ["sociales", CUR_DEMOGRAFIA_6_BANCO], ["sociales", CUR_BUENOS_AIRES_6_BANCO], ["naturales", CUR_INSTRUMENTOS_MEDIDA_6_BANCO], ["logica", CUR_SECUENCIAL_CONDICIONAL_6_BANCO], ["logica", CUR_BLOQUES_CODIGO_6_BANCO], ["logica", CUR_SENSORES_6_BANCO], ["sociales", CUR_CHAT_SEGURO_6_BANCO], ["naturales", CUR_ITS_VIOLENCIA_6_BANCO], ["matematica", CUR_PRESUPUESTO_6_BANCO]],
  7: [["sociales", CUR_DERECHOS_TRABAJO_BANCO], ["lengua", CUR_RECURSOS_POEMA_BANCO], ["sociales", CUR_POBLACION_ARGENTINA_BANCO], ["sociales", CUR_DEMOCRACIA_ARGENTINA_BANCO], ["matematica", CUR_NUMERACION_7_BANCO], ["matematica", CUR_DIVISIBILIDAD_7_BANCO], ["matematica", CUR_MCM_DCM_7_BANCO], ["matematica", CUR_MULTIPLICAR_FRACCIONES_7_BANCO], ["matematica", CUR_DECIMALES_PERIODO_7_BANCO], ["matematica", CUR_DENSIDAD_7_BANCO], ["matematica", CUR_PROPORCIONALIDAD_GRAFICO_7_BANCO], ["matematica", CUR_MEDIA_MEDIANA_MODA_7_BANCO], ["matematica", CUR_PROBABILIDAD_ARBOL_7_BANCO], ["matematica", CUR_TRADUCTOR_ALGEBRAICO_7_BANCO], ["lengua", CUR_NARRADOR_7_BANCO], ["lengua", CUR_SUSTANTIVOS_7_BANCO], ["lengua", CUR_SUJETO_7_BANCO], ["lengua", CUR_METAFORA_SINECDOQUE_7_BANCO], ["lengua", CUR_PERSUASION_7_BANCO], ["lengua", CUR_CRONICA_7_BANCO], ["lengua", CUR_HISTORIETA_7_BANCO], ["lengua", CUR_AMBIGUEDAD_7_BANCO], ["lengua", CUR_ANALISIS_SINTACTICO_7_BANCO], ["lengua", CUR_ORTOGRAFIA_7_BANCO], ["lengua", CUR_LEER_DEDUCIR_7_BANCO], ["lengua", CUR_INGLES_VOCABULARIO_7_BANCO], ["lengua", CUR_INGLES_VERBOS_7_BANCO], ["lengua", CUR_INGLES_LECTURA_7_BANCO], ["naturales", CUR_FLUJO_ENERGIA_7_BANCO], ["naturales", CUR_SUCESION_ECOLOGICA_7_BANCO], ["naturales", CUR_SISTEMA_NERVIOSO_7_BANCO], ["naturales", CUR_INMUNE_7_BANCO], ["naturales", CUR_VACUNAS_7_BANCO], ["naturales", CUR_TRANSFORMAR_ENERGIA_7_BANCO], ["naturales", CUR_MOVIMIENTOS_TIERRA_7_BANCO], ["naturales", CUR_ECLIPSES_UNIVERSO_7_BANCO], ["naturales", CUR_REPRODUCTOR_7_BANCO], ["sociales", CUR_DEMOCRACIA_DICTADURA_7_BANCO], ["sociales", CUR_CADENA_PRODUCTIVA_7_BANCO], ["sociales", CUR_ESPACIOS_MEMORIA_7_BANCO], ["sociales", CUR_PUERTO_MADERO_7_BANCO], ["naturales", CUR_CENTRAL_ENCHUFE_7_BANCO], ["logica", CUR_CAPAS_RED_7_BANCO], ["logica", CUR_EVENTOS_PARALELISMO_7_BANCO], ["logica", CUR_DATASET_SESGADO_7_BANCO], ["logica", CUR_INDUSTRIA_40_7_BANCO], ["naturales", CUR_ANTICONCEPCION_7_BANCO], ["sociales", CUR_ALERTA_EN_LINEA_7_BANCO], ["sociales", CUR_DERECHOS_94_7_BANCO], ["sociales", CUR_GOBIERNO_CIUDAD_7_BANCO], ["naturales", CUR_MATRIZ_ENERGETICA_7_BANCO], ["logica", CUR_FUENTE_LICENCIAS_7_BANCO]],
};
