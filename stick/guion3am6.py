# Si oyes esto a las 3AM — 6: "El vigilabebés"
# A las tres, por el vigilabebés de tu cuarto, alguien le canta una nana a tu hermano pequeño. En casa solo estáis tú y él.
# Pulsas el botón de hablar y preguntas quién es: la nana se calla. Corres a su cuarto y en el pasillo algo frío te roza (pista).
# Tu hermano duerme solo. Entonces el aparato de la cuna habla: "Shhh… ya se ha ido". La voz sale del aparato de TU cuarto:
# se cruzó contigo en el pasillo y ahora está en tu cama. Y como contestaste, sabe que estás despierto.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "piano"
ESTILO = "ps2"
VOCES = {"COSA": ("ef_dora", 0.82, -2)}
MONSTRUOS = {"COSA"}
ETIQUETAS = {"COSA": "¿QUIÉN CANTA?"}
ESCENAS = [
    ("vigila",    "Son las tres. Por el vigilabebés, alguien le canta una nana a tu hermano."),
    ("solos",     "Pero en casa solo estáis tú y él."),
    ("contestas", "Pulsas el botón y preguntas quién es. La nana se calla."),
    ("pasillo",   "Corres a su cuarto. En el pasillo, algo frío te roza."),
    ("cuna",      "Tu hermano duerme. Solo. La ventana, cerrada."),
    ("suena",     "Y el aparato de la cuna vuelve a sonar. [COSA] Shhh… ya se ha ido."),
    ("entiendes", "Esa voz sale del otro aparato. El de tu cuarto."),
    ("tucama",    "Se ha cruzado contigo. Y sabe que estás despierto."),
    ("final",     "Si a las tres alguien canta en el vigilabebés… no contestes."),
]
