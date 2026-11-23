# RULES — 1: Hospital, 4th floor. "If room 414 calls, don't go."
TITULO = "RULES"
PARTE = None
ESTILO = "ps2_3d"
MUSICA = "caja"
VOCES = {"MADRE": ("af_bella", 0.88, -2), "OSCAR": ("am_puck", 0.95, 0)}
MONSTRUOS = {"MADRE", "OSCAR"}
ETIQUETAS = {"MADRE": "414", "OSCAR": "414"}
NOMBRE, OFICIO, FECHA = "Oscar M.", "Night orderly · 4th floor", "11/25/2026, 3:12 AM"
REGLA = "If room 414 calls, don't go."
ESCENAS = [
    ("arranque", "Rule one: if room 414 calls, don't go. Tonight it has called eleven times."),
    ("panel",    "Oscar is the night orderly. Room 414 has been empty for a year."),
    ("voz",      "On the twelfth call, the intercom speaks. [MADRE] Oscar… it hurts."),
    ("camina",   "It's his mother's voice. She died in that room. Oscar goes."),
    ("cama",     "Someone is in the bed. Covered up to the face."),
    ("cara",     "He pulls back the sheet. It's him. And it opens its eyes."),
    ("puerta",   "The door slams shut. The monitor beeps once. Long."),
    ("final",    "The next night, room 414 called again. [OSCAR] Help me."),
]
