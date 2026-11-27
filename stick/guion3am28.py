# Si oyes esto a las 3AM — 28: "La palabra secreta"
# Tu familia tiene una palabra secreta por si algo imita vuestras voces. A las tres tu hermana te llama llorando desde
# el portal: se ha dejado las llaves. Le pides la palabra y la dice bien. Vas al telefonillo a abrir.
# Pista: el armario de tu cuarto está entreabierto en la primera escena… y también aquella noche en que elegisteis la
# palabra, susurrando en tu cama (el recuerdo).
# Giro: tu hermana te escribe desde su cama, al otro lado de la pared: esa palabra solo se dijo una vez, en tu cuarto.
# La llamada nunca vino del portal: en la rendija del armario brilla un móvil. "Vale. Te espero en tu cuarto."
# En una frase: lo que vive en tu armario oyó la palabra y la usó para que le abrieras.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "caja"
VOCES = {"HERMANA": ("ef_dora", 0.9, -2)}
MONSTRUOS = {"HERMANA"}
ETIQUETAS = {"HERMANA": "¿TU HERMANA?"}
ESCENAS = [
    ("llamada",  "Son las tres. Tu hermana te llama llorando desde el portal."),
    ("llaves",   "[HERMANA] Ábreme, porfa. Me he dejado las llaves."),
    ("palabra",  "En tu familia hay una palabra secreta. Por si algo imita vuestras voces."),
    ("pides",    "Se la pides. Ella la dice sin dudar. Es la correcta."),
    ("abrir",    "Vas al telefonillo. Tu dedo, sobre el botón de abrir."),
    ("mensaje",  "Entonces te escribe tu hermana. Desde su cama, al otro lado de la pared."),
    ("armario",  "Esa palabra solo la dijisteis una vez. Susurrando. En tu cuarto."),
    ("susurro",  "En el móvil, el llanto se para. [HERMANA] Vale. Te espero en tu cuarto."),
    ("final",    "Si a las tres alguien sabe vuestra palabra secreta… no abras."),
]
