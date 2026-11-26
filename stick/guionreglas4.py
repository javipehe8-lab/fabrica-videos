# REGLAS — 4: Piscina municipal, cierre. "Después de cerrar, no mires el fondo de la piscina."
# Marta, socorrista. Al apagar las luces oye chapoteos y una niña pide socorro. Mira al fondo: hay una niña tumbada, mirándola.
# Podría estar viva: Marta salta. Abajo, la niña sonríe y le agarra el tobillo. La cámara ve una mano que sale y se hunde.
# Por la mañana la encuentran en el fondo, en el sitio de la niña. Ficha: FALLECIDA.
TITULO = "REGLAS"
PARTE = None
ESTILO = "ps2_3d"
MUSICA = "piano"
VOCES = {"NINA": ("ef_dora", 1.05, 2)}
MONSTRUOS = {"NINA"}
ETIQUETAS = {"NINA": "EL AGUA"}
NOMBRE, OFICIO, FECHA = "Marta L.", "Socorrista · Piscina municipal", "27/11/2026, 00:20"
REGLA = "Después de cerrar, no mires el fondo de la piscina."
SELLO = "FALLECIDA"
ESCENAS = [
    ("arranque", "Regla uno: tras cerrar, no mires el fondo de la piscina. Esta noche, el agua se mueve."),
    ("cierre",   "Marta es socorrista. Cierra la piscina municipal sola, a medianoche."),
    ("grito",    "Apaga la última luz y oye un chapoteo. [NINA] ¡Socorro! ¡Me ahogo!"),
    ("mira",     "Marta mira al fondo. Hay una niña tumbada. Con los ojos abiertos."),
    ("salta",    "Podría estar viva. Marta salta al agua sin pensarlo."),
    ("fondo",    "Abajo, la niña sonríe. Y la agarra del tobillo."),
    ("camara",   "La cámara solo ve agua quieta. Una mano sale. Y se hunde."),
    ("final",    "Por la mañana la encontraron en el fondo. En el sitio de la niña."),
]
