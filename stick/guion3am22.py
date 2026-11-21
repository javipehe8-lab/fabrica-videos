# Si oyes esto a las 3AM — 22: "La vecina de abajo"
# A las tres, algo arrastra muebles en tu techo. Vives en el último piso: encima solo está el desván.
# Pista: por la mañana la vecina de abajo subió a quejarse de que arrastras muebles cada noche, y en el pasillo hay
# arañazos en el suelo que van del armario hasta debajo de la trampilla del techo.
# El ruido se para encima de tu cama. La trampilla se abre sola; baja un brazo larguísimo y arrastra tu armario hasta
# debajo, sobre los mismos arañazos: así baja cada noche (eso es lo que oía la vecina). Asoma la cara, del revés.
# En una frase: lo que vive en tu desván baja cada noche usando tu armario de escalón; la vecina lo oía, tú no.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "piano"
VOCES = {"VECINA": ("ef_dora", 1.0, 0), "COSA": ("em_santa", 0.8, -5)}
MONSTRUOS = {"COSA"}
ETIQUETAS = {"VECINA": "LA VECINA DE ABAJO", "COSA": "EL DESVÁN"}
ESCENAS = [
    ("techo",    "Son las tres. Algo arrastra muebles en tu techo. Y vives en el último piso."),
    ("vecina",   "Esta mañana subió la vecina de abajo. [VECINA] ¡Deja de arrastrar muebles!"),
    ("solo",     "Pero vives solo. No has movido nada. Solo hay arañazos en el suelo."),
    ("encima",   "El ruido cruza el techo… y se para justo encima de tu cama."),
    ("trampilla", "Silencio. En el pasillo, la trampilla del techo se abre sola."),
    ("brazo",    "Baja un brazo larguísimo. Y arrastra tu armario hasta debajo."),
    ("aranazos", "Por los mismos arañazos. Así baja cada noche."),
    ("voz",      "Del hueco negro asoma una cara, del revés. [COSA] ¿Subes tú… o bajo yo?"),
    ("final",    "Si a las tres se arrastran muebles… no subas a mirar."),
]
