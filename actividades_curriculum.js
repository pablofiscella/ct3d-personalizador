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
