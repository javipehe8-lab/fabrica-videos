# TURNO DE NOCHE — 8: "Regla 8: Si el camión de reparto llega antes de las 6, no firmes nada"
# Viene de la Parte 7: la última línea del cuaderno de Raúl, aún húmeda: "A las 5 llega el camión. Firmaré."
# A las 5:00 llega un camión sin logotipo. Lo conduce el anciano de las pesetas (Parte 4).
# El albarán ya está firmado, con tu letra, y con fecha de mañana. No firmas. "Ya firmaste mañana."
# Deja igual una caja con tu nombre: dentro, tu uniforme, empapado, oliendo a niebla.
# Final: miras el que llevas puesto: la placa dice RAÚL (provoca la Parte 9: Raúl, fuera, con una placa con TU nombre).
TITULO = "TURNO DE NOCHE"
PARTE = 8
ESTILO = "ps2_3d"
MUSICA = "tension"
VOCES = {"ANCIANO": ("em_santa", 0.88, -4)}
ETIQUETAS = {"ANCIANO": "ANCIANO"}
REGLAS = ["NO EXISTE EL SURTIDOR 4. SI ALGUIEN LO PIDE, DI QUE NO EXISTE.",
          "SI SUENA EL TELÉFONO DE LA CABINA A LAS 3:00, NO LO COJAS.",
          "EL BAÑO ESTÁ SIEMPRE ROTO. SI PIDEN LA LLAVE, DI QUE ESTÁ ROTO.",
          "NO SIRVAS A NADIE QUE PAGUE CON MONEDAS ANTIGUAS.",
          "SI LA NIEBLA ENTRA EN LA TIENDA, APAGA TODAS LAS LUCES Y NO RESPIRES.",
          "SI ALGUIEN PREGUNTA POR EL KILÓMETRO 10, DI QUE NO EXISTE.",
          "NO LEAS NADA QUE NO HAYAS ESCRITO TÚ.",
          "SI EL CAMIÓN DE REPARTO LLEGA ANTES DE LAS 6, NO FIRMES NADA.",
          "?"]
REGLA_CORTA = "SI EL CAMIÓN LLEGA ANTES DE LAS 6, NO FIRMES"
NOTA = "Yo firmé. — R."
FECHA = "20 NOV 2026"          # mañana
PLACA = "RAÚL"
ESCENAS = [
    ("arranque", "Regla ocho: si el camión llega antes de las seis, no firmes nada. Son las cinco."),
    ("premisa",  "Turno de noche, solo, en la niebla. El cuaderno de Raúl dijo que firmaría."),
    ("llega",    "Cinco en punto. Un camión sin logotipo. Lo conduce el anciano de las pesetas."),
    ("albaran",  "Me da el albarán. Ya está firmado. Con mi letra. Y con fecha de mañana."),
    ("nofirmo",  "No firmo. Él sonríe. [ANCIANO] Ya firmaste mañana."),
    ("caja",     "Deja igual una caja con mi nombre. Dentro, mi uniforme. Empapado. Huele a niebla."),
    ("placa",    "Miro el que llevo puesto. La placa no dice mi nombre. Dice Raúl."),
    ("final",    "Llevo toda la noche con la placa de Raúl. Mañana, la regla nueve."),
]
