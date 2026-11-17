# NIGHT SHIFT — 6: "Rule 6: If anyone asks about mile 10, say it doesn't exist"
TITULO = "NIGHT SHIFT"
PARTE = 6
ESTILO = "ps2_3d"
MUSICA = "caja"
VOCES = {"PADRE": ("am_fenrir", 0.95, -2), "NIÑA": ("af_bella", 1.0, 3)}
ETIQUETAS = {"PADRE": "FATHER", "NIÑA": "GIRL"}
REGLAS = ["THERE IS NO PUMP 4. IF ANYONE ASKS FOR IT, SAY IT DOESN'T EXIST.",
          "IF THE PAY PHONE RINGS AT 3:00, DON'T ANSWER IT.",
          "THE RESTROOM IS ALWAYS BROKEN. IF ANYONE ASKS FOR THE KEY, SAY IT'S BROKEN.",
          "DON'T SERVE ANYONE WHO PAYS WITH OLD COINS.",
          "IF THE FOG GETS INSIDE THE STORE, TURN OFF EVERY LIGHT AND DON'T BREATHE.",
          "IF ANYONE ASKS ABOUT MILE 10, SAY IT DOESN'T EXIST.",
          "?"]
REGLA_CORTA = "IF THEY ASK ABOUT MILE 10, SAY IT DOESN'T EXIST"
ESCENAS = [
    ("arranque", "Rule six: mile ten doesn't exist. Tonight, four times."),
    ("premisa",  "Night shift, alone, in the fog. Last night it wrote me: not you. Not yet."),
    ("coche",    "At one, a car pulls in. Four inside. [PADRE] Which way to mile ten?"),
    ("niego",    "I tell him it doesn't exist. He smiles. He drives off slowly."),
    ("vuelve",   "Every half hour, it comes back. Same car. One less each time."),
    ("nina",     "At two thirty, just the girl. [NIÑA] Raul says this is yours."),
    ("giro",     "It's Raul's notebook. On the last page, my name."),
    ("final",    "Raul wrote my name before he ever met me. Tomorrow, rule seven."),
]
