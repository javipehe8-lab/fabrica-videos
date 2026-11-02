# Si oyes esto a las 3AM — 3: "Tu compañero de piso"
# A las tres llama a la puerta "tu compañero de piso": se ha dejado las llaves. Le escribes y te contesta desde su cama:
# no abras, lleva una semana imitándome. Pista: en el gancho de la entrada sus llaves NO están (las perdió hace una semana).
# Giro: la cerradura empieza a girar sola. Tenía llaves. Solo llamaba para saber si estabas despierto.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "piano"
VOCES = {"COMPI": ("em_santa", 1.05, -2)}
MONSTRUOS = {"COMPI"}
ETIQUETAS = {"COMPI": "¿TU COMPI?"}
ESCENAS = [
    ("timbre",    "Son las tres. Tu compañero de piso llama a la puerta. [COMPI] Abre, soy yo. Me dejé las llaves."),
    ("recibidor", "Es su voz. Y es verdad: sus llaves no están en el gancho."),
    ("movil",     "Le escribes. Contesta desde su cama: no abras. Lleva una semana imitándome."),
    ("cuarto",    "Su puerta está cerrada. Dentro brilla la luz de su móvil."),
    ("silencio",  "Fuera, el timbre deja de sonar. Pero nadie se va."),
    ("llavero",   "Y al otro lado de la puerta… suena un llavero."),
    ("cerradura", "La cerradura empieza a girar. Las llaves del gancho… las tenía eso."),
    ("asoma",     "No necesitaba que abrieras. Solo saber si estabas despierto."),
    ("final",     "Si a las tres alguien olvidó sus llaves… no abras."),
]
