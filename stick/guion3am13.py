# Si oyes esto a las 3AM — 13: "El vecino de enfrente"
# Cada noche a las tres el vecino de enfrente te saluda desde su ventana y tú le devuelves el saludo.
# Pista: cada noche que le saludas, él está un poco más pegado al cristal (se va acercando gracias a tu saludo).
# Hoy su ventana está vacía, con la luz encendida. Tu móvil abre solo la cámara frontal y hace una foto: detrás de tu
# hombro está él, saludando. Giro: "Gracias por invitarme": devolver el saludo era dejarle pasar.
# En una frase: le devolviste el saludo al vecino de enfrente cada noche… y cada saludo lo acercó, hasta tu cuarto.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "piano"
VOCES = {"VECINO": ("em_santa", 0.82, -4)}
MONSTRUOS = {"VECINO"}
ETIQUETAS = {"VECINO": "¿EL VECINO?"}
ESCENAS = [
    ("ventana",   "Son las tres. El vecino de enfrente te saluda desde su ventana."),
    ("devuelves", "Como cada noche, tú le devuelves el saludo."),
    ("cerca",     "Y cada noche, está un poco más pegado al cristal."),
    ("vacia",     "Hoy su ventana está vacía. Con la luz encendida."),
    ("movil",     "Tu móvil vibra. La cámara frontal se abre sola."),
    ("clic",      "Clic. Una foto. Tu cara… y algo detrás de tu hombro."),
    ("detras",    "Es él. En tu cuarto. Saludándote."),
    ("voz",       "Te susurra en la nuca. [VECINO] Gracias por invitarme."),
    ("final",     "Si a las tres alguien te saluda… no le devuelvas el saludo."),
]
