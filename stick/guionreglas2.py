# REGLAS — 2: Hotel, recepción de noche. "Nunca des la llave de la habitación 0."
# Lucía, recepcionista. Un huésped empapado dice que reservó la 0. En el libro, la reserva está a nombre de Lucía.
# Él tiembla de frío y ella le da la llave. La cámara del pasillo la ve entrar A ELLA en la 0.
# Por la mañana, en recepción hay una Lucía que sonríe demasiado. Ficha: SUSTITUIDA. La de verdad pide ayuda desde la 0.
TITULO = "REGLAS"
PARTE = None
ESTILO = "ps2_3d"
MUSICA = "piano"
VOCES = {"HUESPED": ("em_santa", 0.9, -7), "LUCIA": ("ef_dora", 0.95, -3)}
MONSTRUOS = {"HUESPED", "LUCIA"}
ETIQUETAS = {"HUESPED": "HUÉSPED", "LUCIA": "HAB. 0"}
NOMBRE, OFICIO, FECHA = "Lucía F.", "Recepcionista de noche · Hotel", "25/11/2026, 03:14"
REGLA = "Nunca des la llave de la habitación 0."
SELLO = "SUSTITUIDA"
ESCENAS = [
    ("arranque", "Regla uno: nunca des la llave de la habitación 0. Esta noche, alguien la pide."),
    ("entra",    "Lucía es recepcionista de noche. El hotel no tiene habitación 0."),
    ("pide",     "A las tres entra un hombre empapado. [HUESPED] Reservé la cero."),
    ("libro",    "Lucía mira el libro. La reserva existe. Pone su nombre."),
    ("llave",    "Él tiembla de frío. Lucía no se atreve a echarlo. Le da la llave."),
    ("camara",   "En la cámara del pasillo, quien entra en la 0 es Lucía."),
    ("manana",   "Por la mañana, Lucía sigue en recepción. Sonríe sin parpadear."),
    ("final",    "La de verdad sigue en la 0. [LUCIA] Que alguien me abra."),
]
