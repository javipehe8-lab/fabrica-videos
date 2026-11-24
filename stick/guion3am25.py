# Si oyes esto a las 3AM — 25: "El silencio"
# A las tres todos los ruidos de la casa se apagan de golpe (la nevera, el reloj, los coches). Tu madre te escribe desde
# su cuarto: "No respires fuerte. Está escuchando". Tu móvil VIBRA al recibirlo (pista). Algo recorre el pasillo y se
# para en cada puerta, escuchando. Se para en la tuya; te tapas la boca. Le escribes: "Está en mi puerta".
# Giro: ella contesta y, en el silencio, tu móvil vibra otra vez. El mensaje dice "QUITA LA VIBRACIÓN". La puerta se abre.
# En una frase: algo caza por el oído, y el aviso de tu madre es el ruido que le dice dónde estás.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "piano"
VOCES = {"COSA": ("em_santa", 0.8, -5)}
MONSTRUOS = {"COSA"}
ETIQUETAS = {"COSA": "LO QUE ESCUCHA"}
ESCENAS = [
    ("reloj",    "A las tres, todos los ruidos de tu casa se apagan de golpe."),
    ("nada",     "La nevera. El reloj de la cocina. Los coches. Nada suena."),
    ("mensaje",  "Tu móvil vibra. Tu madre, desde su cuarto: no respires fuerte. Está escuchando."),
    ("pasillo",  "Algo camina por el pasillo. Se para en cada puerta. Escucha."),
    ("puerta",   "Se para en la tuya. Te tapas la boca. No respiras."),
    ("escribes", "Le escribes a tu madre, temblando: está en mi puerta."),
    ("vibra",    "Ella contesta. En el silencio, tu móvil vibra: quita la vibración."),
    ("abre",     "La puerta se abre despacio. [COSA] Te he oído."),
    ("final",    "Si a las tres todo se calla… cállate tú también."),
]
