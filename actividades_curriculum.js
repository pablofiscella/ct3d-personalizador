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
