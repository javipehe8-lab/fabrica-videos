# REGLAS — 1: Hospital, planta 4. "Si llaman desde la 414, no vayas."
# Óscar, celador de noche. La 414 lleva un año vacía. Por el interfono habla su madre, que murió allí. Va.
# En la cama, tapado, está él mismo. La puerta se cierra; monitor plano. Ficha: DESAPARECIDO.
# A la noche siguiente la 414 vuelve a llamar, con la voz de Óscar.
TITULO = "REGLAS"
PARTE = None
ESTILO = "ps2_3d"
MUSICA = "caja"
VOCES = {"MADRE": ("ef_dora", 0.88, -2), "OSCAR": ("em_santa", 0.95, 0)}
MONSTRUOS = {"MADRE", "OSCAR"}
ETIQUETAS = {"MADRE": "414", "OSCAR": "414"}
NOMBRE, OFICIO, FECHA = "Óscar M.", "Celador de noche · Planta 4", "25/11/2026, 03:12"
REGLA = "Si llaman desde la 414, no vayas."
ESCENAS = [
    ("arranque", "Regla uno: si llaman desde la 414, no vayas. Esta noche han llamado once veces."),
    ("panel",    "Óscar es celador de noche. La 414 lleva un año vacía."),
    ("voz",      "A la duodécima llamada, el interfono habla. [MADRE] Óscar… me duele."),
    ("camina",   "Es la voz de su madre. Murió en esa habitación. Óscar va."),
    ("cama",     "Dentro hay alguien en la cama. Tapado hasta la cara."),
    ("cara",     "Destapa la sábana. Es él. Y abre los ojos."),
    ("puerta",   "La puerta se cierra. El monitor pita una sola vez. Largo."),
    ("final",    "A la noche siguiente, la 414 volvió a llamar. [OSCAR] Ayúdame."),
]
