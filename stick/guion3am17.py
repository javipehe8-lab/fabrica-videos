# Si oyes esto a las 3AM — 17: "Las escaleras de más"
# Cada noche bajas a por agua contando los trece escalones a oscuras. Hoy cuentas catorce, y el último está blando.
# Pista: la cuenta (once, doce, trece…) sale en pantalla desde el principio, y en el escalón blando se notan unas vértebras.
# Enciendes el móvil: el "escalón" es alguien tumbado boca abajo al pie de la escalera, con la cara girada hacia ti.
# Subes corriendo y te tapas. Desde la escalera, algo cuenta los escalones al subir: "Once. Doce. Trece."
# Giro: silencio… y junto a tu cama, un susurro: "Catorce". El escalón de más ahora está al lado de tu cama.
# En una frase: lo que se hacía pasar por un escalón te ha notado al pisarlo y sube contando hasta tu cama.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "tension"
VOCES = {"COSA": ("em_santa", 0.85, -4)}
MONSTRUOS = {"COSA"}
ETIQUETAS = {"COSA": "EL ESCALÓN 14"}
ESCENAS = [
    ("reloj",    "Son las tres. Bajas a oscuras, y tu escalera tiene un escalón de más."),
    ("trece",    "Siempre son trece. Los cuentas sin mirar."),
    ("catorce",  "Pero hoy, después del trece, tu pie sigue bajando. Catorce."),
    ("blando",   "Y el catorce está blando. Y caliente."),
    ("respira",  "Entonces, bajo tu pie… el escalón respira."),
    ("movil",    "Enciendes el móvil. No es un escalón. Es alguien tumbado."),
    ("subes",    "Subes corriendo y te tapas hasta la cabeza."),
    ("cuenta",   "Y en la escalera, algo empieza a contar. [COSA] Once. Doce. Trece."),
    ("final",    "Silencio. Y junto a tu cama… [COSA] Catorce. [NARRADOR] Si a las tres hay un escalón de más… no lo pises."),
]
