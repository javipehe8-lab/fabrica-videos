# TURNO DE NOCHE — 1: "Regla 1: No existe el surtidor 4"
# Un hombre empapado pide el surtidor 4. En la niebla aparece un cuarto surtidor. Le dices que no existe.
# Giro: en la CAM 2, junto al surtidor 4, alguien con tu uniforme saluda. Al pie de la lista: "Yo le dije que sí. — Raúl".
TITULO = "TURNO DE NOCHE"
PARTE = 1
ESTILO = "ps2_3d"
MUSICA = "piano"
VOCES = {"HOMBRE": ("em_santa", 0.95, -3)}
ETIQUETAS = {"HOMBRE": "CLIENTE"}
REGLAS = ["NO EXISTE EL SURTIDOR 4. SI ALGUIEN LO PIDE, DI QUE NO EXISTE.",
          "?", "?", "?", "?"]
ESCENAS = [
    ("llegada",  "Trabajo solo, de noche, en una gasolinera perdida en la niebla. Y hay reglas."),
    ("lista",    "La primera dice: no existe el surtidor cuatro. Si alguien lo pide, di que no existe."),
    ("entra",    "A las tres y diecisiete entra un hombre empapado. [HOMBRE] ¿Me enciendes el cuatro?"),
    ("ventana",  "Miro fuera. Solo hay tres surtidores. Pero en la niebla… hay un cuarto."),
    ("niego",    "Le digo que no existe. No parpadea. Se da la vuelta y se va."),
    ("camara",   "En la cámara dos, junto al surtidor cuatro, hay alguien con mi uniforme. Saludando."),
    ("nota",     "Al final de la lista, alguien escribió a mano: yo le dije que sí."),
    ("final",    "Es la letra del que trabajaba aquí antes. Mañana, la regla dos."),
]
