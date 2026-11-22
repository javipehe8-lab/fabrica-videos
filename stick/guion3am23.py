# Si oyes esto a las 3AM — 23: "Los golpes en la pared"
# Tu hermano y tú os dais las buenas noches con tres golpes en la pared que separa vuestros cuartos.
# A las tres suenan tres golpes; contestas. Por la mañana tu hermano vuelve: durmió en casa de un amigo.
# Su cuarto estaba vacío… y algo pálido, de pie contra la pared, era quien llamaba.
# Giro: la noche siguiente los tres golpes ya no vienen de la pared, sino de dentro de tu armario: le contestaste, ahora sabe dónde estás.
# En una frase: le devolviste los golpes a algo que no era tu hermano, y ahora llama desde dentro de tu cuarto.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "caja"
VOCES = {"HERMANO": ("em_alex", 1.1, 3), "COSA": ("em_santa", 0.85, -4)}
MONSTRUOS = {"COSA"}
ETIQUETAS = {"HERMANO": "TU HERMANO", "COSA": "¿TU HERMANO?"}
ESCENAS = [
    ("golpes",    "Son las tres. Suenan tres golpes en la pared de tu cuarto."),
    ("senal",     "Es vuestra señal. Así os dais las buenas noches tu hermano y tú."),
    ("contestas", "Sonríes. Contestas con tres golpes… y te duermes."),
    ("manana",    "Por la mañana, tu hermano vuelve con la mochila. [HERMANO] Dormí en casa de Dani."),
    ("vacio",     "Su cuarto estuvo vacío toda la noche. Entonces… ¿quién llamó?"),
    ("noche",     "Esa noche, a las tres, vuelven los tres golpes."),
    ("armario",   "Pero no vienen de la pared. Vienen de dentro de tu armario."),
    ("toca",      "La puerta se abre un dedo. [COSA] Ahora te toca a ti."),
    ("final",     "Si a las tres llaman a la pared… no devuelvas los golpes."),
]
