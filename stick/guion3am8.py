# Si oyes esto a las 3AM — 8: "Tu número te llama"
# A las tres te llama tu propio número. Es tu voz, susurrando: "No te levantes. Hay alguien debajo de la cama".
# Pista: mientras hablas, bajo la cama brilla una lucecita azul (una pantalla) que se apaga justo cuando cuelgas.
# Crees que es una broma (alguien ha copiado tu número) y, sin bajar de la cama, devuelves la llamada para pillarlo.
# Giro: debajo de tu cama empieza a sonar un móvil. Una mano pálida lo coge y oyes tu voz por el teléfono… y desde abajo.
# Lo que te llamaba está ahí debajo, esperando a que pongas un pie en el suelo. Regla: si te llamas tú… haz caso.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "tension"
VOCES = {"VOZ": ("em_alex", 1.0, -1)}       # tu misma voz (la del narrador), con eco de monstruo
MONSTRUOS = {"VOZ"}
ETIQUETAS = {"VOZ": "¿TÚ?"}
ESCENAS = [
    ("entrante",  "Son las tres. Te está llamando tu propio número."),
    ("contestas", "Contestas. Es tu voz, susurrando. [VOZ] No te levantes. Hay alguien debajo."),
    ("broma",     "Una broma. Alguien ha copiado tu número. Cuelgas."),
    ("devuelves", "Sin bajar de la cama, devuelves la llamada. Para pillarlo."),
    ("suena",     "Da tono… y debajo de tu cama empieza a sonar un móvil."),
    ("coge",      "Una mano pálida lo coge. Y oyes tu voz por el móvil… y desde abajo."),
    ("abajo",     "[VOZ] Te he dicho que no te levantes."),
    ("espera",    "Lo que te llamaba está ahí debajo. Esperando a que bajes un pie."),
    ("final",     "Si a las tres te llamas tú… haz caso."),
]
