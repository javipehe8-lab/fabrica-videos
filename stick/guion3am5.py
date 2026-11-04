# Si oyes esto a las 3AM — 5: "El perro te lame la mano"
# A las tres bajas la mano de la cama y tu perro, que duerme debajo, te la lame para calmarte.
# Pista: bajo la cama, en la oscuridad, se ven unos dedos largos y pálidos junto a "tu perro".
# Oyes gotear en el baño: tu perro está tumbado en la ducha, sin respirar, y en el espejo pone
# "LOS HUMANOS TAMBIÉN SABEN LAMER". Giro: lo que te lamía la mano no era tu perro… y sale de debajo de tu cama.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "caja"
VOCES = {"COSA": ("em_santa", 0.92, -3)}
MONSTRUOS = {"COSA"}
ETIQUETAS = {"COSA": "¿TU PERRO?"}
ESCENAS = [
    ("cama",      "Son las tres. Bajas la mano de la cama… y tu perro te la lame."),
    ("siempre",   "Duerme ahí debajo. Cuando tienes miedo, te lame. Y te calmas."),
    ("gotea",     "Pero en el baño algo gotea. Plic. Plic. Plic."),
    ("pasillo",   "Te levantas. La luz del baño parpadea."),
    ("ducha",     "Tu perro está tumbado en la ducha. Frío. No respira."),
    ("espejo",    "En el espejo empañado hay algo escrito. [COSA] Los humanos también saben lamer."),
    ("entiendes", "Lo que te lamía la mano… no era tu perro."),
    ("sale",      "Y ahora, en tu cuarto, sale de debajo de la cama."),
    ("final",     "Si a las tres algo te lame la mano… no la bajes."),
]
