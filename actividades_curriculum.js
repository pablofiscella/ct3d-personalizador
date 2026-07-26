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
    "q": "Un cuadrado apoyado en una punta, ¿deja de ser cuadrado?",
    "ops": [
      "No, sigue siendo cuadrado",
      "Sí, pasa a ser rombo",
      "Sí, pasa a ser triángulo"
    ],
    "m": "Girar la figura no la cambia: sigue teniendo 4 lados iguales y ángulos rectos."
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
  "m": "Fijate en qué columna sumás: unidades con unidades, dieces con dieces, cienes con cienes. Da {ok}."
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

/* 6° · Clasificá pronombres — pronombres_clasif
   DC: Pronombres personales, posesivos y demostrativos
   Fuente: docs/auditoria-dc-caba/grado-6.md · L6 */
const CUR_PRONOMBRES_CLASIF_BANCO = [
  {
    "it": "ELLA llegó temprano.",
    "cat": "personal",
    "m": "«Ella» reemplaza a una persona: es personal."
  },
  {
    "it": "Ese libro es MÍO.",
    "cat": "posesivo",
    "m": "«Mío» indica de quién es: posesivo."
  },
  {
    "it": "ESTE me gusta más.",
    "cat": "demostrativo",
    "m": "«Este» señala cuál: demostrativo."
  },
  {
    "it": "NOSOTROS vamos al club.",
    "cat": "personal",
    "m": "«Nosotros» son personas: personal."
  },
  {
    "it": "La bici es TUYA.",
    "cat": "posesivo",
    "m": "«Tuya» dice de quién es: posesivo."
  },
  {
    "it": "AQUELLOS quedaron lejos.",
    "cat": "demostrativo",
    "m": "«Aquellos» señalan cuáles y dónde: demostrativo."
  },
  {
    "it": "YO no fui.",
    "cat": "personal",
    "m": "«Yo» es la persona que habla: personal."
  },
  {
    "it": "El error fue NUESTRO.",
    "cat": "posesivo",
    "m": "«Nuestro» indica pertenencia: posesivo."
  },
  {
    "it": "ESA es la respuesta.",
    "cat": "demostrativo",
    "m": "«Esa» señala cuál: demostrativo."
  },
  {
    "it": "USTEDES llegaron primero.",
    "cat": "personal",
    "m": "«Ustedes» son personas: personal."
  },
  {
    "it": "Los zapatos son SUYOS.",
    "cat": "posesivo",
    "m": "«Suyos» dice de quién: posesivo."
  },
  {
    "it": "ESTOS están rotos.",
    "cat": "demostrativo",
    "m": "«Estos» señalan cuáles: demostrativo."
  },
  {
    "it": "ÉL me lo contó.",
    "cat": "personal",
    "m": "«Él» reemplaza a una persona."
  },
  {
    "it": "La culpa no es MÍA.",
    "cat": "posesivo",
    "m": "«Mía» indica de quién: posesivo."
  }
];
GAMES.pronombres_clasif = juegoClasificar(CUR_PRONOMBRES_CLASIF_BANCO, "¿Qué clase de pronombre es el resaltado?", [{"cat": "personal", "label": "🙋 Personal"}, {"cat": "posesivo", "label": "🔑 Posesivo"}, {"cat": "demostrativo", "label": "👉 Demostrativo"}], "pronombres");

/* 6° · ¿Fuente confiable? — fuente_confiable
   DC: Evaluar la confiabilidad de las fuentes de información
   Fuente: docs/auditoria-dc-caba/grado-6.md · L4 */
const CUR_FUENTE_CONFIABLE_BANCO = [
  {
    "q": "Para un trabajo sobre el sistema solar, ¿cuál es más confiable?",
    "ops": [
      "La página de un observatorio astronómico",
      "Un video de alguien opinando",
      "Un comentario en una red social"
    ],
    "m": "Un observatorio produce el conocimiento; una opinión suelta no lo respalda."
  },
  {
    "q": "Encontrás dos páginas con datos distintos. ¿Qué hacés?",
    "ops": [
      "Buscar una tercera fuente para comparar",
      "Elegir la que más te guste",
      "Copiar las dos sin decir nada"
    ],
    "m": "Contrastar fuentes es lo que permite decidir cuál es más confiable."
  },
  {
    "q": "Una página no dice quién la escribió ni cuándo. ¿Eso importa?",
    "ops": [
      "Sí, no poder saber quién lo dice le resta confianza",
      "No, si está en internet es verdad",
      "Sólo importa si tiene fotos"
    ],
    "m": "Autor y fecha son dos señales básicas de confiabilidad."
  },
  {
    "q": "Para saber cuándo es un feriado, ¿cuál conviene?",
    "ops": [
      "Una página oficial del gobierno",
      "Un chat de amigos",
      "Un blog personal"
    ],
    "m": "Los feriados los fija el Estado: la fuente oficial es la que manda."
  },
  {
    "q": "Un texto dice «los científicos afirman» pero no dice cuáles. ¿Qué le falta?",
    "ops": [
      "Decir de dónde saca esa información",
      "Más adjetivos",
      "Ser más largo"
    ],
    "m": "Sin la fuente concreta, «los científicos dicen» no se puede verificar."
  },
  {
    "q": "Para un dato sobre la salud, ¿cuál elegirías?",
    "ops": [
      "La página de un hospital o del Ministerio de Salud",
      "Una publicidad de un producto",
      "Un video de humor"
    ],
    "m": "La publicidad quiere venderte algo: no es una fuente neutral."
  },
  {
    "q": "¿Qué significa que una página termine en .gob.ar?",
    "ops": [
      "Que es de un organismo del Estado argentino",
      "Que es de una empresa",
      "Que es un blog"
    ],
    "m": "El .gob.ar identifica sitios oficiales del Estado."
  },
  {
    "q": "Una noticia de hace 10 años sobre tecnología, ¿sirve hoy?",
    "ops": [
      "Hay que revisar si sigue vigente",
      "Sí, siempre",
      "No, nada viejo sirve"
    ],
    "m": "La fecha importa según el tema: en tecnología, mucho."
  },
  {
    "q": "Alguien muy famoso opina sobre medicina sin ser médico. ¿Es confiable?",
    "ops": [
      "No, ser famoso no lo hace experto",
      "Sí, porque lo conoce todo el mundo",
      "Sí, si tiene muchos seguidores"
    ],
    "m": "La autoridad tiene que ser sobre EL TEMA, no fama en general."
  },
  {
    "q": "Para una biografía de San Martín, ¿cuál es mejor?",
    "ops": [
      "Un libro de historia o un museo histórico",
      "Una película de acción",
      "Un meme"
    ],
    "m": "La película puede inventar; el museo y el libro de historia investigan."
  },
  {
    "q": "¿Por qué conviene mirar más de una fuente?",
    "ops": [
      "Porque cada una puede tener errores o su punto de vista",
      "Porque así el trabajo es más largo",
      "No conviene, es perder tiempo"
    ],
    "m": "Comparar es lo que te permite darte cuenta de un error o un sesgo."
  },
  {
    "q": "Un sitio lleno de mayúsculas y signos («¡¡¡INCREÍBLE!!!»), ¿qué señal da?",
    "ops": [
      "Que busca impactar más que informar",
      "Que es muy serio",
      "Que tiene mucha información"
    ],
    "m": "El tono exagerado suele acompañar información poco cuidada."
  },
  {
    "q": "Wikipedia, ¿sirve?",
    "ops": [
      "Como punto de partida, revisando sus fuentes al final",
      "No sirve nunca",
      "Sí, y no hace falta revisar nada"
    ],
    "m": "Cualquiera puede editarla, pero cita fuentes: ahí está lo verificable."
  },
  {
    "q": "¿Qué hacés si un dato te parece raro?",
    "ops": [
      "Lo verificás en otra fuente antes de usarlo",
      "Lo usás igual",
      "Lo borrás del trabajo"
    ],
    "m": "Verificar es exactamente lo que hace confiable a un trabajo."
  }
];
GAMES.fuente_confiable = juegoTriviaTexto(CUR_FUENTE_CONFIABLE_BANCO, "¿Cuál conviene usar para un trabajo de la escuela?", "fuente_con");

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

/* 6° · Conectores en acción — conectores_6
   DC: Conectores temporales, causales y consecutivos
   Fuente: docs/auditoria-dc-caba/grado-6.md · L8 */
const CUR_CONECTORES_6_BANCO = [
  {
    "q": "Estudió mucho ___ aprobó el examen.",
    "ops": [
      "por lo tanto",
      "aunque",
      "mientras"
    ],
    "m": "Estudiar es la causa y aprobar la consecuencia: «por lo tanto»."
  },
  {
    "q": "No fue a la plaza ___ estaba lloviendo.",
    "ops": [
      "porque",
      "por lo tanto",
      "además"
    ],
    "m": "«Porque» introduce la causa."
  },
  {
    "q": "Primero hervimos el agua; ___ agregamos los fideos.",
    "ops": [
      "después",
      "porque",
      "sin embargo"
    ],
    "m": "Es una secuencia en el tiempo: «después»."
  },
  {
    "q": "Es caro; ___ , vale la pena.",
    "ops": [
      "sin embargo",
      "porque",
      "entonces"
    ],
    "m": "Marca oposición: «sin embargo»."
  },
  {
    "q": "Llegó tarde ___ perdió el colectivo.",
    "ops": [
      "porque",
      "aunque",
      "además"
    ],
    "m": "Explica la causa de llegar tarde."
  },
  {
    "q": "Terminó la tarea; ___ salió a jugar.",
    "ops": [
      "entonces",
      "aunque",
      "porque"
    ],
    "m": "Consecuencia en el tiempo: «entonces»."
  },
  {
    "q": "Me gusta el mar ___ no sé nadar.",
    "ops": [
      "aunque",
      "porque",
      "por eso"
    ],
    "m": "«Aunque» marca una concesión: algo que no impide lo otro."
  },
  {
    "q": "Estaba cansado; ___ , siguió trabajando.",
    "ops": [
      "no obstante",
      "porque",
      "así que"
    ],
    "m": "Marca oposición, como «sin embargo»."
  },
  {
    "q": "Juntamos los ingredientes; ___ , mezclamos todo.",
    "ops": [
      "luego",
      "porque",
      "aunque"
    ],
    "m": "Secuencia temporal."
  },
  {
    "q": "Hacía calor, ___ abrimos las ventanas.",
    "ops": [
      "así que",
      "aunque",
      "sin embargo"
    ],
    "m": "«Así que» introduce la consecuencia."
  },
  {
    "q": "Le gusta leer; ___ , escribe muy bien.",
    "ops": [
      "además",
      "pero",
      "porque"
    ],
    "m": "«Además» suma información en la misma dirección."
  },
  {
    "q": "No entrenó ___ perdió el partido.",
    "ops": [
      "por eso",
      "aunque",
      "sin embargo"
    ],
    "m": "Causa y consecuencia: «por eso»."
  },
  {
    "q": "Vinieron todos, ___ Ana, que estaba enferma.",
    "ops": [
      "excepto",
      "porque",
      "entonces"
    ],
    "m": "«Excepto» marca la excepción."
  },
  {
    "q": "___ terminó de llover, salió el arcoíris.",
    "ops": [
      "Cuando",
      "Porque",
      "Aunque"
    ],
    "m": "Ubica el momento: conector temporal."
  }
];
GAMES.conectores_6 = juegoTriviaTexto(CUR_CONECTORES_6_BANCO, "¿Qué conector completa mejor?", "conectores");

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
    "q": "¿En qué año volvió la democracia a la Argentina?",
    "ops": [
      "1983",
      "1810",
      "2001"
    ],
    "m": "En 1983, después de la última dictadura militar."
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
    "q": "¿Qué significa «Nunca Más»?",
    "ops": [
      "El compromiso de que no se repita el terrorismo de Estado",
      "Que no haya elecciones",
      "Que no se hable del pasado"
    ],
    "m": "Da nombre al informe de la CONADEP y sintetiza ese compromiso."
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
const CUR_RESTA_CANJE_4_PLANTILLA = {
  "q": "{a} − {b}",
  "vars": {
    "a": {
      "rango": [
        1200,
        9800
      ],
      "paso": 1
    },
    "b": {
      "rango": [
        150,
        990
      ],
      "paso": 1
    }
  },
  "ok": "a - b",
  "distractores": [
    "a - b + 10",
    "a - b - 10",
    "a - b + 100"
  ],
  "tope": 10000,
  "m": "Cuando en una columna no alcanza, se pide 10 prestado a la de al lado Y esa columna queda con uno menos. Da {ok}."
};
GAMES.resta_canje_4 = juegoParametrico(CUR_RESTA_CANJE_4_PLANTILLA, "¿Cuánto da?", "resta_canj");

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
    "q": "Se ___ el pelo todas las mañanas.",
    "ops": [
      "ata",
      "hata",
      "haya"
    ],
    "m": "Del verbo atar, sin H."
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
    "q": "¿Cuál de estos es primo?",
    "ops": [
      "13",
      "15",
      "21"
    ],
    "m": "13 sólo se divide por 1 y por 13. Los otros dos tienen más divisores."
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
