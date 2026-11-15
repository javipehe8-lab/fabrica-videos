# TURNO DE NOCHE — 4: "Regla 4: No sirvas a nadie que pague con monedas antiguas"
# Un anciano, seco pese a la niebla, paga un paquete de tabaco con pesetas de 1986. La caja marca 15/11/2026.
# Le devuelves las monedas (casi: las has tocado para leer la fecha). Él: "El otro chico sí me cobró."
# En la CAM 2, alguien con tu uniforme (Raúl) le abre la puerta de un coche viejo. La caja se abre sola: solo pesetas.
# Giro: la pantalla de la caja ya no marca 2026. Marca 15/11/1986. Pista: la fecha que se vio en "monedas".
TITULO = "TURNO DE NOCHE"
PARTE = 4
ESTILO = "ps2_3d"
MUSICA = "piano"
VOCES = {"ANCIANO": ("em_santa", 0.88, -4)}
ETIQUETAS = {"ANCIANO": "ANCIANO"}
REGLAS = ["NO EXISTE EL SURTIDOR 4. SI ALGUIEN LO PIDE, DI QUE NO EXISTE.",
          "SI SUENA EL TELÉFONO DE LA CABINA A LAS 3:00, NO LO COJAS.",
          "EL BAÑO ESTÁ SIEMPRE ROTO. SI PIDEN LA LLAVE, DI QUE ESTÁ ROTO.",
          "NO SIRVAS A NADIE QUE PAGUE CON MONEDAS ANTIGUAS.",
          "?"]
ESCENAS = [
    ("llegada",  "Cada noche vigilo, solo, una gasolinera en la niebla. Y obedezco reglas."),
    ("lista",    "Regla cuatro: no sirvas a nadie que pague con monedas antiguas."),
    ("anciano",  "Pasadas las tres entra un anciano. Sin coche. Y seco."),
    ("monedas",  "Pide tabaco. Paga con pesetas. Del año ochenta y seis."),
    ("niego",    "Se las devuelvo. No le cobro. [ANCIANO] El otro chico sí me cobró."),
    ("camara",   "En la cámara dos, alguien con mi uniforme le abre la puerta."),
    ("giro",     "Entonces la caja se abre sola. Dentro ya no hay euros. Solo pesetas."),
    ("final",    "Y la fecha de la pantalla ya no es la de hoy. Mañana, la regla cinco."),
]
