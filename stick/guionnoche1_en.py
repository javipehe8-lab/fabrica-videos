# NIGHT SHIFT — 1: "Rule 1: There is no pump 4"
TITULO = "NIGHT SHIFT"
PARTE = 1
ESTILO = "ps2_3d"
MUSICA = "piano"
VOCES = {"HOMBRE": ("am_adam", 0.95, -3)}
ETIQUETAS = {"HOMBRE": "CUSTOMER"}
REGLAS = ["THERE IS NO PUMP 4. IF ANYONE ASKS FOR IT, SAY IT DOESN'T EXIST.",
          "?", "?", "?", "?"]
ESCENAS = [
    ("llegada",  "I work alone, nights, at a gas station lost in the fog. And there are rules."),
    ("lista",    "Rule one: there is no pump four. If anyone asks for it, say it doesn't exist."),
    ("entra",    "At three seventeen, a soaking wet man walks in. [HOMBRE] Can you turn on pump four?"),
    ("ventana",  "I look outside. There are only three pumps. But in the fog… there's a fourth."),
    ("niego",    "I tell him it doesn't exist. He doesn't blink. He turns and leaves."),
    ("camara",   "On camera two, next to pump four, someone in my uniform is waving."),
    ("nota",     "At the bottom of the list, someone wrote by hand: I told him yes."),
    ("final",    "It's the handwriting of the guy who worked here before me. Tomorrow, rule two."),
]
