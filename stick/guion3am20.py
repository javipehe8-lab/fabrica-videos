# Si oyes esto a las 3AM — 20: "El GPS"
# A las tres conduces solo por una carretera de bosque y el GPS te dice que gires a la derecha,
# hacia un camino de tierra que no sale en el mapa (la línea de la ruta se mete en un hueco gris).
# Pista: desde el primer plano hay un coche detrás de ti, siempre a la misma distancia (sus faros en el retrovisor).
# No giras. El GPS insiste cada vez más rápido. El coche de detrás pone el intermitente y gira por el camino.
# Sus luces se meten entre los árboles y se apagan de golpe. El GPS, tranquilo: "Ruta completada".
# Giro: un kilómetro después, otro camino de tierra a la derecha, y el GPS vuelve a marcar el giro.
# En una frase: el GPS necesitaba que alguien girara por ese camino; giró el de detrás… y ahora vuelve a por ti.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "persecucion"
VOCES = {"GPS": ("ef_dora", 1.0, 0)}
RADIOS = {"GPS"}                          # voz por el altavoz del GPS
ETIQUETAS = {"GPS": "EL GPS"}
ESCENAS = [
    ("gps",      "Son las tres. Conduces solo, y el GPS te dice que gires."),
    ("camino",   "A la derecha hay un camino de tierra. En el mapa, nada."),
    ("detras",   "No giras. Detrás, un coche te sigue desde hace kilómetros."),
    ("insiste",  "El GPS se acelera. [GPS] Gire a la derecha. Gire. Gire."),
    ("gira",     "Por el retrovisor, el coche de detrás pone el intermitente. Y gira."),
    ("apagan",   "Sus luces se meten entre los árboles. Y se apagan de golpe."),
    ("completa", "El GPS se calla. Y luego, tranquilo: [GPS] Ruta completada."),
    ("otra",     "Un kilómetro después, otro camino de tierra. El GPS vuelve a marcarlo."),
    ("final",    "Si a las tres el GPS insiste… no gires."),
]
