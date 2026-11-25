# HILOS MALDITOS — 1: "Mi abuela desapareció tres días. La que volvió me reconoce."
# Formato (ver hilos.md): un "post" de un foro propio del canal (ficción), narrado en primera persona sobre un fondo
# en bucle hecho con el motor 3D (aquí: carretera de noche entre pinos). 60-90 s.
TITULO = "HILOS MALDITOS"
PARTE = None
ESTILO = "ps2_3d"
MUSICA = "piano"
SUBS_Y = 1060                     # subtítulos en el centro, grandes (formato "historia de foro")
SIN_SUBS = ("titulo",)            # en el arranque el título se lee en la tarjeta del post
EDGE_NARRADOR = "es-ES-XimenaNeural"
VOCES = {"ABUELA": ("ef_dora", 0.82, -3), "LLAMADA": ("ef_dora", 0.86, -2)}
EDGE_VOCES = {"ABUELA": "es-MX-DaliaNeural", "LLAMADA": "es-ES-ElviraNeural"}
MONSTRUOS = {"ABUELA"}
RADIOS = {"LLAMADA"}
ETIQUETAS = {"ABUELA": "LA ABUELA", "LLAMADA": "MÓVIL DE LA ABUELA"}

POST = dict(
    usuario="nieta_del_pinar", hace="hace 4 h", sub="relatos",
    titulo="Mi abuela desapareció tres días. La que volvió me reconoce.",
    votos="2,4 mil", comentarios="318",
)
EDIT = "EDIT: mi madre ha ido al pinar. No contesta. La abuela está poniendo la mesa para cinco."

ESCENAS = [
    ("titulo",    "Mi abuela desapareció tres días. La que volvió me reconoce. Y eso es lo que me da miedo."),
    ("alzheimer", "Mi abuela tiene alzhéimer. Hace un año que no sabe quién soy. Me llama señorita."),
    ("noche",     "En agosto salió de casa de madrugada, en camisón. La buscó medio pueblo. Nada."),
    ("pinar",     "Al tercer día la encontraron sentada en el pinar, a veinte kilómetros. Sin un rasguño. Con las zapatillas limpias."),
    ("coche",     "En el coche me cogió la mano y dijo mi nombre. Mi nombre completo. Con su voz de antes."),
    ("mesa",      "Desde entonces no olvida nada. Cocina sin mirar las recetas. Pero pone la mesa para cinco. Y somos cuatro."),
    ("puerta",    "Anoche me desperté a las tres. Estaba de pie en mi puerta, sonriendo. [ABUELA] Tú también vas a venir al pinar."),
    ("movil",     "Hoy ha sonado su móvil viejo. Estaba en un cajón, sin batería desde agosto."),
    ("llamada",   "Era su voz. Lloraba. [LLAMADA] Hija, sigo en el pinar. ¿Quién duerme en mi cama?"),
    ("final",     "Edit: mi madre ha ido al pinar. No contesta. La abuela está poniendo la mesa para cinco."),
]
