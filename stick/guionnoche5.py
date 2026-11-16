# TURNO DE NOCHE — 5: "Regla 5: Si la niebla entra en la tienda, apaga todas las luces y no respires"
# A las tres, la niebla se cuela por debajo de la puerta. Apagas todo y contienes el aire.
# Una silueta de niebla camina entre las estanterías y se para frente al mostrador. Con la voz de Raúl: "Tranquilo. Ya puedes respirar."
# No respiras. La niebla se va. Al encender, bajo la nota de Raúl en la hoja ("Yo respiré. — R."), alguien ha escrito en el vaho: "TÚ TODAVÍA NO."
# Pista del misterio: Raúl respiró, y la niebla se quedó con su voz.
TITULO = "TURNO DE NOCHE"
PARTE = 5
ESTILO = "ps2_3d"
MUSICA = "tension"
VOCES = {"RAUL": ("em_santa", 1.02, 3)}
ETIQUETAS = {"RAUL": "¿RAÚL?"}
REGLAS = ["NO EXISTE EL SURTIDOR 4. SI ALGUIEN LO PIDE, DI QUE NO EXISTE.",
          "SI SUENA EL TELÉFONO DE LA CABINA A LAS 3:00, NO LO COJAS.",
          "EL BAÑO ESTÁ SIEMPRE ROTO. SI PIDEN LA LLAVE, DI QUE ESTÁ ROTO.",
          "NO SIRVAS A NADIE QUE PAGUE CON MONEDAS ANTIGUAS.",
          "SI LA NIEBLA ENTRA EN LA TIENDA, APAGA TODAS LAS LUCES Y NO RESPIRES.",
          "?"]
ESCENAS = [
    ("llegada",  "Trabajo solo, de noche, en una gasolinera tragada por la niebla. Con reglas."),
    ("lista",    "Regla cinco: si entra la niebla, apágalo todo y no respires."),
    ("niebla",   "A las tres, la niebla empieza a colarse por debajo de la puerta."),
    ("apago",    "Apago todas las luces. Contengo el aire. Algo entra con ella."),
    ("voz",      "Se para frente al mostrador. Y me habla. [RAUL] Tranquilo. Ya puedes respirar."),
    ("aguanto",  "Es la voz de Raúl, el chico de antes. No respiro."),
    ("giro",     "Se va. Enciendo. Bajo la nota de Raúl, escrito en vaho: tú todavía no."),
    ("final",    "Raúl respiró. Ahora la niebla tiene su voz. Mañana, la regla seis."),
]
