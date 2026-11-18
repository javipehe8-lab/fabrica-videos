# TURNO DE NOCHE — 7: "Regla 7: No leas nada que no hayas escrito tú"
# Viene de la Parte 6: la niña te dio el cuaderno de Raúl, con tu nombre en la última página.
# Lo lees igual. Cada página cuenta tus noches aquí (el surtidor 4, la cabina, la niña, las pesetas, la niebla)... fechadas en 1986.
# Mientras lees, se escribe una línea nueva, con la letra de Raúl: "No mires la cámara uno". La miras: en la CAM 1 no estás leyendo; estás escribiendo.
# Final: la última línea, aún húmeda: "A las 5 llega el camión. Firmaré." (provoca la Parte 8)
TITULO = "TURNO DE NOCHE"
PARTE = 7
ESTILO = "ps2_3d"
MUSICA = "piano"
VOCES = {"RAUL": ("em_santa", 1.02, 3)}
ETIQUETAS = {"RAUL": "¿RAÚL?"}
REGLAS = ["NO EXISTE EL SURTIDOR 4. SI ALGUIEN LO PIDE, DI QUE NO EXISTE.",
          "SI SUENA EL TELÉFONO DE LA CABINA A LAS 3:00, NO LO COJAS.",
          "EL BAÑO ESTÁ SIEMPRE ROTO. SI PIDEN LA LLAVE, DI QUE ESTÁ ROTO.",
          "NO SIRVAS A NADIE QUE PAGUE CON MONEDAS ANTIGUAS.",
          "SI LA NIEBLA ENTRA EN LA TIENDA, APAGA TODAS LAS LUCES Y NO RESPIRES.",
          "SI ALGUIEN PREGUNTA POR EL KILÓMETRO 10, DI QUE NO EXISTE.",
          "NO LEAS NADA QUE NO HAYAS ESCRITO TÚ.",
          "?"]
REGLA_CORTA = "NO LEAS NADA QUE NO HAYAS ESCRITO TÚ"
# lo que pone en el cuaderno (con la letra de Raúl)
NOCHES = [("12 NOV 1986", "Pidió el surtidor 4. Dije que no."),
          ("13 NOV 1986", "3:00. Sonó la cabina. No la cogí."),
          ("14 NOV 1986", "La niña quería la llave."),
          ("15 NOV 1986", "Pesetas. No le cobré."),
          ("16 NOV 1986", "Entró la niebla. No respiré.")]
HOY = "18 NOV 1986"
PAG_HOY = ["3:12. Lo abro igual.", "Estoy leyendo esta línea.", "3:14. No mires la cámara uno."]
PAG_FIN = ["Miré la cámara.", "A las 5 llega el camión.", "Firmaré."]
ESCENAS = [
    ("arranque", "Regla siete: no leas nada que no hayas escrito tú. Y estoy leyendo."),
    ("premisa",  "Turno de noche, solo, en la niebla. Anoche me dieron el cuaderno de Raúl."),
    ("abro",     "La regla dice que no lo lea. Lo abro igual."),
    ("noches",   "Son mis noches aquí, una a una. Escritas en mil novecientos ochenta y seis."),
    ("sola",     "Mientras leo, se escribe otra línea. [RAUL] No mires la cámara uno."),
    ("cam",      "La miro. En la cámara uno no estoy leyendo. Estoy escribiendo."),
    ("giro",     "Última línea, aún húmeda: a las cinco llega el camión. Firmaré."),
    ("final",    "Yo no he firmado nada. Todavía. Mañana, la regla ocho."),
]
