# Si oyes esto a las 3AM — 19: "La llamada de la abuela"
# A las tres te llama tu abuela, la que tiene alzhéimer: "Hay un hombre en mi cocina. Dice que es tu padre".
# Imposible: tu padre está dormido a tu lado, en el sofá (con el mismo jersey mostaza que el hombre de la cocina).
# Pista: papá siempre ronca, y esta noche no hace ningún ruido. La abuela insiste: él dice que el de tu sofá no respira.
# Lo miras: su pecho no se mueve. Y sin moverse, "tu padre" abre los ojos: "Cuelga".
# En una frase: el de la cocina era tu padre de verdad; el que duerme a tu lado no, y la abuela tenía razón.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "piano"
VOCES = {"ABUELA": ("ef_dora", 0.92, -1), "PADRE": ("em_santa", 0.9, -3)}
RADIOS = {"ABUELA"}          # por el teléfono
MONSTRUOS = {"PADRE"}
ETIQUETAS = {"ABUELA": "LA ABUELA", "PADRE": "¿PAPÁ?"}
ESCENAS = [
    ("llama",   "Son las tres. Te llama tu abuela, la que tiene alzhéimer."),
    ("susurra", "Susurra. [ABUELA] Hay un hombre en mi cocina. Dice que es tu padre."),
    ("sofa",    "Imposible. Tu padre está dormido a tu lado, en el sofá."),
    ("ronca",   "Qué raro. Papá siempre ronca. Esta noche no hace ningún ruido."),
    ("insiste", "La abuela insiste. Él dice que el de tu sofá… no respira."),
    ("pecho",   "Lo miras. Su pecho no se mueve. Nada."),
    ("ojos",    "Y sin moverse, tu padre abre los ojos. [PADRE] Cuelga."),
    ("final",   "La llamada se corta. Si a las tres llama la abuela… créetela."),
]
