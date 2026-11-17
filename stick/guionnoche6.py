# TURNO DE NOCHE — 6: "Regla 6: Si alguien pregunta por el kilómetro 10, di que no existe"
# Viene de la Parte 5: la niebla escribió en el vaho "TÚ TODAVÍA NO".
# A la una para un coche familiar con cuatro dentro; el padre pregunta por el kilómetro 10. Le dices que no existe.
# Vuelve cada media hora, cada vez con uno menos. A las 2:30 solo queda la niña, atrás; el asiento del conductor, vacío.
# Baja la ventanilla y te da un cuaderno mojado: es el de Raúl, y en la última página está escrito tu nombre.
TITULO = "TURNO DE NOCHE"
PARTE = 6
ESTILO = "ps2_3d"
MUSICA = "caja"
VOCES = {"PADRE": ("em_santa", 0.95, -3), "NIÑA": ("ef_dora", 1.0, 4)}
ETIQUETAS = {"PADRE": "PADRE", "NIÑA": "NIÑA"}
REGLAS = ["NO EXISTE EL SURTIDOR 4. SI ALGUIEN LO PIDE, DI QUE NO EXISTE.",
          "SI SUENA EL TELÉFONO DE LA CABINA A LAS 3:00, NO LO COJAS.",
          "EL BAÑO ESTÁ SIEMPRE ROTO. SI PIDEN LA LLAVE, DI QUE ESTÁ ROTO.",
          "NO SIRVAS A NADIE QUE PAGUE CON MONEDAS ANTIGUAS.",
          "SI LA NIEBLA ENTRA EN LA TIENDA, APAGA TODAS LAS LUCES Y NO RESPIRES.",
          "SI ALGUIEN PREGUNTA POR EL KILÓMETRO 10, DI QUE NO EXISTE.",
          "?"]
REGLA_CORTA = "SI PREGUNTAN POR EL KM 10, DI QUE NO EXISTE"
ESCENAS = [
    ("arranque", "Regla seis: el kilómetro diez no existe. Esta noche, cuatro veces."),
    ("premisa",  "Turno de noche, solo, en la niebla. Anoche me escribió: tú todavía no."),
    ("coche",    "A la una para un coche. Cuatro dentro. [PADRE] ¿Por dónde al kilómetro diez?"),
    ("niego",    "Le digo que no existe. Sonríe. Se va despacio."),
    ("vuelve",   "Vuelve cada media hora. Mismo coche. Cada vez, uno menos."),
    ("nina",     "A las dos y media, solo la niña. [NIÑA] Raúl dice que es tuyo."),
    ("giro",     "Es el cuaderno de Raúl. En la última página, mi nombre."),
    ("final",    "Raúl escribió mi nombre antes de conocerme. Mañana, la regla siete."),
]
