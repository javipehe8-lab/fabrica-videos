# Si oyes esto a las 3AM — 16: "El taxi"
# A las tres vuelves a casa en taxi. El taxista no habla y, por el retrovisor, sus ojos no parpadean nunca.
# Pista: el número del taxi (117) está a la vista desde el primer plano, y al taxista le gotea agua de la gorra.
# Le mandas el número a tu amiga: "¿El 117? Se estrelló en el puente viejo en 1998". Y vais hacia el puente viejo.
# Frena junto a unas flores, donde la barandilla está rota. Por primera vez habla: "Hemos llegado. Bájate."
# Giro: tu puerta se abre sola y, abajo, en el fondo del río, brilla la luz verde de un taxi: el suyo.
# En una frase: un taxista muerto te lleva al puente donde se mató y quiere que te bajes justo donde él cayó.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "persecucion"
VOCES = {"TAXISTA": ("em_santa", 0.9, -3)}
MONSTRUOS = {"TAXISTA"}
ETIQUETAS = {"TAXISTA": "EL TAXISTA"}
ESCENAS = [
    ("taxi",      "Son las tres. Vas en taxi, y el taxista no parpadea."),
    ("ojos",      "Te mira por el retrovisor. Diez minutos. Ni una sola vez."),
    ("numero",    "Por si acaso, le escribes a tu amiga el número del taxi."),
    ("respuesta", "Contesta al momento. Ese taxi se estrelló hace treinta años."),
    ("puente",    "Miras fuera. No vais a tu casa. Vais al puente viejo."),
    ("flores",    "Frena junto a unas flores. Donde la barandilla está rota."),
    ("habla",     "Y por primera vez, habla. [TAXISTA] Hemos llegado. Bájate."),
    ("puerta",    "Tu puerta se abre sola. Abajo, en el río, brilla la luz de un taxi."),
    ("final",     "Si a las tres el taxista no parpadea… no te bajes donde él pare."),
]
