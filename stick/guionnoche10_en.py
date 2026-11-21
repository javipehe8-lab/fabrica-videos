# NIGHT SHIFT — 10: "Rule 10: The cameras run 10 seconds behind. If one runs ahead, leave by the back door"
TITULO = "NIGHT SHIFT"
PARTE = 10
ESTILO = "ps2_3d"
MUSICA = "persecucion"
VOCES = {"RAUL": ("am_puck", 1.0, 1)}
ETIQUETAS = {"RAUL": "RAUL"}
REGLAS = ["THERE IS NO PUMP 4. IF ANYONE ASKS FOR IT, SAY IT DOESN'T EXIST.",
          "IF THE PAY PHONE RINGS AT 3:00, DON'T ANSWER IT.",
          "THE RESTROOM IS ALWAYS BROKEN. IF ANYONE ASKS FOR THE KEY, SAY IT'S BROKEN.",
          "DON'T SERVE ANYONE WHO PAYS WITH OLD COINS.",
          "IF THE FOG GETS INSIDE THE STORE, TURN OFF EVERY LIGHT AND DON'T BREATHE.",
          "IF ANYONE ASKS ABOUT MILE 10, SAY IT DOESN'T EXIST.",
          "DON'T READ ANYTHING YOU DIDN'T WRITE.",
          "IF THE DELIVERY TRUCK COMES BEFORE 6, DON'T SIGN ANYTHING.",
          "IF YOU SEE RAUL, DON'T LET HIM IN.",
          "THE CAMERAS RUN 10 SECONDS BEHIND. IF ONE RUNS AHEAD, LEAVE BY THE BACK DOOR.",
          "?"]
REGLA_CORTA = "IF A CAMERA RUNS AHEAD, LEAVE BY THE BACK DOOR"
NOTA = "I waited the ten seconds. — R."
ESCENAS = [
    ("arranque", "Rule ten: the cameras run ten seconds behind. Tonight, one is running ahead."),
    ("premisa",  "I work alone, at night, in the fog. Last night, the cameras put me outside."),
    ("reloj",    "Four ten. Camera one is ten seconds ahead of me."),
    ("entra",    "On the screen, the fog comes in the door. Here, it's still shut."),
    ("detras",   "On the screen, it stops right behind me. It puts its hands on me."),
    ("nuca",     "Cold on my neck. And his voice, in my ear: [RAUL] Your turn."),
    ("huyo",     "I run out the back door. On the screen, I stay. And it takes me."),
    ("final",    "Out back, there's a sign that wasn't there: Mile 10. Tomorrow, rule eleven."),
]
