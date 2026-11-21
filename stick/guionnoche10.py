# TURNO DE NOCHE — 10: "Regla 10: Las cámaras van 10 segundos por detrás. Si alguna va por delante, sal por la puerta de atrás"
# Viene de la Parte 9: en la CAM 1, el que golpeaba el cristal desde fuera era yo; dentro, detrás del mostrador, estaba Raúl.
# A las 4:10 la CAM 1 va diez segundos por delante: en la pantalla la niebla entra por la puerta (aquí sigue cerrada),
# se para detrás de mí y me pone las manos en los hombros. Noto frío en la nuca y la voz de Raúl: "Te toca."
# Huyo por la puerta de atrás; en la pantalla me quedo, y la niebla me lleva (una parte de mí se queda en las cámaras).
# Final: detrás de la gasolinera, en la niebla, hay un cartel que no estaba: KILÓMETRO 10 (provoca la Parte 11).
TITULO = "TURNO DE NOCHE"
PARTE = 10
ESTILO = "ps2_3d"
MUSICA = "persecucion"
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
          "?"]
REGLA_CORTA = "SI UNA CÁMARA VA POR DELANTE, SAL POR LA PUERTA DE ATRÁS"
NOTA = "Yo esperé los diez segundos. — R."
ESCENAS = [
    ("arranque", "Regla diez: las cámaras van diez segundos tarde. Esta noche, una va adelantada."),
    ("premisa",  "Trabajo solo, de noche, en la niebla. Anoche, las cámaras me pusieron fuera."),
    ("reloj",    "Cuatro y diez. La cámara uno va diez segundos por delante."),
    ("entra",    "En la pantalla, la niebla entra por la puerta. Aquí, sigue cerrada."),
    ("detras",   "En la pantalla, se para detrás de mí. Me pone las manos encima."),
    ("nuca",     "Frío en la nuca. Y su voz, al oído: [RAUL] Te toca."),
    ("huyo",     "Huyo por la puerta de atrás. En la pantalla, me quedo. Y me lleva."),
    ("final",    "Fuera hay un cartel que no estaba: kilómetro diez. Mañana, la regla once."),
]
