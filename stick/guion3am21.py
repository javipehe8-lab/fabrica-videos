# Si oyes esto a las 3AM — 21: "El grupo de clase"
# A las tres, en el grupo de clase, un número que nadie tiene guardado pregunta: "¿Quién está despierto?".
# Pista: desde el primer plano del cuarto, tu portátil está abierto en la mesa, apuntando a tu cama (con su lucecita).
# Contestas "Yo". Por privado: "Ya lo sé. Te veo." La luz de la webcam está encendida, y te llega una foto tuya en la cama.
# Cierras el portátil de golpe. Giro: llega otra foto… de ti cerrándolo, hecha desde la esquina del techo de tu cuarto.
# En una frase: algo preguntó quién estaba despierto para saber a quién mirar; contestaste… y ya no necesita la webcam.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "tension"
VOCES = {"DESCONOCIDO": ("em_santa", 0.85, -4)}
MONSTRUOS = {"DESCONOCIDO"}
ETIQUETAS = {"DESCONOCIDO": "¿QUIÉN?"}
ESCENAS = [
    ("grupo",     "Son las tres. En el grupo de clase alguien pregunta: ¿quién está despierto?"),
    ("nadie",     "Nadie contesta. Y ese número no lo tiene guardado nadie."),
    ("portatil",  "Tu portátil sigue abierto en la mesa. Mirando a tu cama."),
    ("contestas", "Por curiosidad, contestas: yo."),
    ("privado",   "Al segundo, te escribe por privado. [DESCONOCIDO] Ya lo sé. Te veo."),
    ("luz",       "Miras el portátil. La luz de la cámara está encendida."),
    ("foto",      "Te llega una foto. Eres tú, en la cama, mirando el móvil."),
    ("esquina",   "Cierras el portátil de golpe. Llega otra foto: tú, cerrándolo."),
    ("final",     "Hecha desde la esquina del techo. Si a las tres preguntan quién está despierto… no contestes."),
]
