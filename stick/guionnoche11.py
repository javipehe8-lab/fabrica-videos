# TURNO DE NOCHE — 11: "Regla 11: Nunca cruces el kilómetro 10"
# Viene de la Parte 10: huí por la puerta de atrás y, en la niebla, había un cartel que no estaba: KILÓMETRO 10.
# Lo cruzo. Detrás, mi gasolinera se apaga entera. Al otro lado hay otra gasolinera idéntica (rótulo: KILÓMETRO 10 · 24H).
# Detrás de su mostrador, tres empleados con mi uniforme (el anciano de las pesetas, Raúl y uno sin cara) me saludan a la vez,
# como en la CAM 2 de la Parte 1. Raúl: "Pasa. Te guardamos el sitio." En su monitor hay cuatro detrás del mostrador: el cuarto soy yo.
# Final: en su mostrador, una hoja de reglas en blanco; arriba, con mi letra, "Regla 12:" y el bolígrafo aún caliente (provoca la Parte 12).
TITULO = "TURNO DE NOCHE"
PARTE = 11
ESTILO = "ps2_3d"
MUSICA = "piano"
VOCES = {"RAUL": ("em_santa", 1.02, 3)}
ETIQUETAS = {"RAUL": "RAÚL"}
REGLAS = ["NO EXISTE EL SURTIDOR 4. SI ALGUIEN LO PIDE, DI QUE NO EXISTE.",
          "SI SUENA EL TELÉFONO DE LA CABINA A LAS 3:00, NO LO COJAS.",
          "EL BAÑO ESTÁ SIEMPRE ROTO. SI PIDEN LA LLAVE, DI QUE ESTÁ ROTO.",
          "NO SIRVAS A NADIE QUE PAGUE CON MONEDAS ANTIGUAS.",
          "SI LA NIEBLA ENTRA EN LA TIENDA, APAGA TODAS LAS LUCES Y NO RESPIRES.",
          "SI ALGUIEN PREGUNTA POR EL KILÓMETRO 10, DI QUE NO EXISTE.",
          "NO LEAS NADA QUE NO HAYAS ESCRITO TÚ.",
          "SI EL CAMIÓN DE REPARTO LLEGA ANTES DE LAS 6, NO FIRMES NADA.",
          "SI VES A RAÚL, NO LE DEJES ENTRAR.",
          "LAS CÁMARAS VAN 10 SEGUNDOS POR DETRÁS. SI ALGUNA VA POR DELANTE, SAL POR LA PUERTA DE ATRÁS.",
          "NUNCA CRUCES EL KILÓMETRO 10.",
          "?"]
REGLA_CORTA = "NUNCA CRUCES EL KILÓMETRO 10"
ESCENAS = [
    ("arranque", "Regla once: nunca cruces el kilómetro diez. Esta noche lo he cruzado."),
    ("cruzo",    "Paso el cartel. A mi espalda, mi gasolinera se apaga entera."),
    ("otra",     "Huí por la puerta de atrás. Y aquí hay otra gasolinera: kilómetro diez."),
    ("dentro",   "Detrás del mostrador hay tres empleados. Todos llevan mi uniforme."),
    ("saludo",   "Me saludan a la vez. [RAUL] Pasa. Te guardamos el sitio."),
    ("monitor",  "En su monitor hay cuatro detrás del mostrador. El cuarto soy yo."),
    ("hoja",     "En su mostrador, una hoja de reglas en blanco. Con mi letra: regla doce."),
    ("final",    "Y el bolígrafo todavía está caliente. Mañana, la regla doce."),
]
