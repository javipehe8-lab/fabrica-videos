# REGLAS — 3: Metro, último tren. "Si el tren de las 2:40 para en el andén, no subas."
# Andrés, vigilante nocturno. A las 2:40 para un tren que no existe. Dentro, sentados, los desaparecidos de la línea.
# Al fondo, su hermano Dani, desaparecido hace cinco años, le guarda sitio. Andrés sube. El tren se va sin luces.
# Por la mañana, en el cartel de desaparecidos hay una cara nueva: la suya. Ficha: DESAPARECIDO.
TITULO = "REGLAS"
PARTE = None
ESTILO = "ps2_3d"
MUSICA = "tension"
VOCES = {"DANI": ("em_alex", 0.9, -4)}
MONSTRUOS = {"DANI"}
ETIQUETAS = {"DANI": "DANI"}
NOMBRE, OFICIO, FECHA = "Andrés M.", "Vigilante nocturno · Metro", "26/11/2026, 02:40"
REGLA = "Si el tren de las 2:40 para en el andén, no subas."
SELLO = "DESAPARECIDO"
ESCENAS = [
    ("arranque", "Regla uno: si el tren de las 2:40 para, no subas. Esta noche ha parado."),
    ("anden",    "Andrés es vigilante del metro. El último tren pasó a la una."),
    ("puertas",  "Las puertas se abren solas. Dentro, todos sentados. Nadie se mueve."),
    ("carteles", "Andrés los conoce. Son las caras del cartel de desaparecidos."),
    ("hermano",  "Al fondo está Dani, su hermano. Desapareció hace cinco años. [DANI] Te guardé sitio."),
    ("sube",     "Andrés no lo piensa. Sube. Las puertas se cierran."),
    ("camara",   "La cámara del andén ve irse el tren. Sin luces. Sin ruido."),
    ("final",    "Por la mañana, el cartel tenía una cara nueva. La de Andrés."),
]
