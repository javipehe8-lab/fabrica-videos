# Si oyes esto a las 3AM — 2: "El asiento de atrás"
# Conduces de noche y un coche te sigue dándote las largas sin parar. Cada vez que te ciega, cruje tu asiento de atrás.
# Giro: el conductor te grita que hay alguien detrás: las largas eran para que no te atacara… y acaba de dejar de darlas.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
VOCES = {"CONDUCTOR": ("em_santa", 1.15, -1)}
ETIQUETAS = {"CONDUCTOR": "EL OTRO CONDUCTOR"}
ESCENAS = [
    ("carretera",  "Son las tres. Conduces solo, y un coche no para de darte las largas."),
    ("largas",     "Te ciega. Una vez. Y otra. Y otra."),
    ("cruje",      "Y cada vez que te ciega… algo cruje en tu asiento de atrás."),
    ("paras",      "Asustado, frenas en el arcén. El otro coche para justo detrás."),
    ("conductor",  "Un hombre baja corriendo. [CONDUCTOR] ¡Sal del coche! ¡Hay alguien detrás!"),
    ("entiendes",  "Te daba las largas para que no te atacara. Y ya no las da."),
    ("retrovisor", "Miras el retrovisor. Ya no está agachado."),
    ("final",      "Si a las tres un coche te da las largas… mira atrás."),
]
