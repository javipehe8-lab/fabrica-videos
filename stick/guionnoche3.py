# TURNO DE NOCHE — 3: "Regla 3: El baño está siempre roto"
# Una niña empapada pide la llave del baño. Le dices que está roto y se va a la niebla.
# Desde dentro del baño cerrado, su misma voz: "Ábreme. Tengo frío." En la CAM 2 ella sigue fuera, mirando.
# Giro: la llave del baño, que no ha salido de tu bolsillo, está empapada. Pista: la nota de Raúl, "Está ocupado".
TITULO = "TURNO DE NOCHE"
PARTE = 3
ESTILO = "ps2_3d"
MUSICA = "caja"
VOCES = {"NIÑA": ("ef_dora", 1.0, 4)}
ETIQUETAS = {"NIÑA": "NIÑA"}
REGLAS = ["NO EXISTE EL SURTIDOR 4. SI ALGUIEN LO PIDE, DI QUE NO EXISTE.",
          "SI SUENA EL TELÉFONO DE LA CABINA A LAS 3:00, NO LO COJAS.",
          "EL BAÑO ESTÁ SIEMPRE ROTO. SI PIDEN LA LLAVE, DI QUE ESTÁ ROTO.",
          "?", "?"]
ESCENAS = [
    ("llegada",  "Trabajo solo, de noche, en una gasolinera en la niebla. Hay reglas."),
    ("lista",    "Regla tres: el baño siempre está roto. Raúl añadió: está ocupado."),
    ("nina",     "Pasadas las tres, entra una niña sola. Empapada."),
    ("pide",     "Me pide la llave del baño. Le digo que está roto. Se va."),
    ("puerta",   "Entonces, desde el baño cerrado con llave, oigo su voz. [NIÑA] Ábreme. Tengo frío."),
    ("camara",   "En la cámara dos, la niña sigue fuera. Mirándome."),
    ("giro",     "Saco la llave del bolsillo. Está empapada. Gotea, como ella."),
    ("final",    "Esa llave no ha salido de mi bolsillo en toda la noche. Mañana, la regla cuatro."),
]
