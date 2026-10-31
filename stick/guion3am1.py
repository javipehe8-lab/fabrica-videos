# Si oyes esto a las 3AM — 1: "No bajes"
# Algo imita la voz de tu madre desde la cocina. Tu madre de verdad te escribe que no bajes.
# Giro: ahora la cosa llama a tu madre… con TU voz.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
VOCES = {"MAMA": ("ef_dora", 1.05, 0), "FALSA": ("em_santa", 1.1, 4)}
MONSTRUOS = {"FALSA"}
ETIQUETAS = {"MAMA": "MAMÁ", "FALSA": "¿TÚ?"}
ESCENAS = [
    ("llama",    "Son las tres de la mañana. Tu madre te llama desde la cocina. [MAMA] Cariño, baja un momento."),
    ("bajas",    "Bajas a oscuras. La luz de la cocina parpadea."),
    ("movil",    "Entonces vibra tu móvil. Es tu madre: no bajes. Yo también la he oído."),
    ("espalda",  "Desde la escalera la ves. De espaldas. Con la bata de tu madre."),
    ("cabeza",   "Y sin mover el cuerpo… gira la cabeza hacia ti."),
    ("subes",    "Subes corriendo y te encierras en el cuarto de tu madre."),
    ("abrazo",   "Está temblando. Es ella. La de verdad."),
    ("tuvoz",    "Pero abajo, la voz vuelve a llamar. [FALSA] Mamá, baja un momento."),
    ("final",    "Es tu voz. Y tu madre se levanta. Si a las tres te llaman desde la cocina… no bajes."),
]
