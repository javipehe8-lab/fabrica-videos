# TURNO DE NOCHE — 2: "Regla 2: Si suena el teléfono de la cabina a las 3:00, no lo cojas"
# La cabina suena a las 3:00. No la coges. Entonces suena el teléfono de la tienda: la pantalla dice CABINA.
# Es tu propia voz: "Sal. Tienes algo detrás." En la CAM 1 no hay nadie detrás de ti.
# Giro: en la CAM 3, alguien con tu uniforme está en la cabina, con el auricular, mirando la tienda. Quería que salieras.
TITULO = "TURNO DE NOCHE"
PARTE = 2
ESTILO = "ps2_3d"
MUSICA = "tension"
VOCES = {"YO": ("em_alex", 1.05, -2)}
ETIQUETAS = {"YO": "MI VOZ"}
REGLAS = ["NO EXISTE EL SURTIDOR 4. SI ALGUIEN LO PIDE, DI QUE NO EXISTE.",
          "SI SUENA EL TELÉFONO DE LA CABINA A LAS 3:00, NO LO COJAS.",
          "?", "?", "?"]
ESCENAS = [
    ("llegada",  "Trabajo solo, de noche, en una gasolinera que nadie encuentra. Con reglas."),
    ("lista",    "Regla dos: si suena la cabina a las tres, no la cojas."),
    ("suena",    "A las tres en punto suena la cabina. Doce veces. No me muevo."),
    ("tienda",   "Entonces suena el teléfono de la tienda. En la pantalla pone: cabina."),
    ("voz",      "Descuelgo. Es mi propia voz. [YO] Sal. Ya. Tienes algo detrás."),
    ("camara",   "Miro la cámara uno. Detrás de mí no hay nadie."),
    ("giro",     "En la cámara tres, alguien con mi uniforme sostiene el auricular. Mirándome."),
    ("final",    "Si hubiera salido, ahora estaría yo en esa cabina. Mañana, la regla tres."),
]
