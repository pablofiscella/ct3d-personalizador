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
