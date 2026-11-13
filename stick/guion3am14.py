# Si oyes esto a las 3AM — 14: "El reflejo que tarda"
# A las tres, en el espejo del baño, tu reflejo parpadea un segundo tarde.
# Pista: todo lo que haces, él lo hace un segundo después (levantar la cara, la mano, acercarse): no te copia, te imita.
# Te acercas al espejo; tú te paras, él sigue acercándose y sonríe. Pega la mano al cristal: "Ahora te toca a ti".
# Giro: la luz parpadea y, cuando vuelve, estás dentro del espejo. Fuera, él, con tu cara, te sonríe y apaga la luz.
# En una frase: tu reflejo iba con retraso porque no era tu reflejo, y al acercarte te cambió el sitio.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "caja"
VOCES = {"REFLEJO": ("em_alex", 0.92, -2)}     # tu propia voz, más lenta y grave, con eco de monstruo
MONSTRUOS = {"REFLEJO"}
ETIQUETAS = {"REFLEJO": "¿TÚ?"}
ESCENAS = [
    ("reloj",   "Son las tres. En el espejo del baño, tu reflejo parpadea tarde."),
    ("agua",    "Te mojas la cara. Levantas la vista. Él tarda en levantarla."),
    ("mano",    "Levantas la mano. Uno… Y entonces la levanta él."),
    ("acercas", "No deberías, pero te acercas. Despacio. Él también."),
    ("sonrisa", "Tú te paras. Él sigue acercándose. Y sonríe."),
    ("voz",     "Pega la mano al cristal. [REFLEJO] Ahora te toca a ti."),
    ("luz",     "La luz parpadea. Cuando vuelve, estás dentro del espejo."),
    ("fuera",   "Fuera, alguien con tu cara te sonríe… y apaga la luz."),
    ("final",   "Si a las tres tu reflejo llega tarde… no te acerques."),
]
