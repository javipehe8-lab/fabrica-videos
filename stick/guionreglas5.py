# REGLAS — 5: Almacén de paquetería en Black Friday. "Si sale un paquete con tu dirección, no lo abras."
# Diego, mozo de almacén, turno doble. Por la cinta llega una caja con su nombre y su dirección; dentro se oye a su hija.
# La abre: la caja no tiene fondo y unas manitas tiran de él. La cámara solo ve la caja, cerrada, siguiendo por la cinta.
# Por la mañana su mujer firma un paquete en casa: pesa lo que un hombre. Ficha: DESAPARECIDO.
TITULO = "REGLAS"
PARTE = None
ESTILO = "ps2_3d"
MUSICA = "caja"
VOCES = {"HIJA": ("ef_dora", 1.05, 3)}
MONSTRUOS = {"HIJA"}
ETIQUETAS = {"HIJA": "LA CAJA"}
NOMBRE, OFICIO, FECHA = "Diego R.", "Mozo de almacén · Paquetería", "28/11/2026, 03:10"
REGLA = "Si sale un paquete con tu dirección, no lo abras."
SELLO = "DESAPARECIDO"
ESCENAS = [
    ("arranque", "Regla uno: si sale un paquete con tu dirección, no lo abras. Esta noche ha salido."),
    ("turno",    "Diego es mozo de almacén. Turno doble de Black Friday."),
    ("etiqueta", "A las tres llega una caja por la cinta. Con su dirección."),
    ("voz",      "Dentro se oye a su hija. [HIJA] Papá, sácame."),
    ("abre",     "Su hija duerme en casa. Pero es su voz. Diego la abre."),
    ("dentro",   "La caja no tiene fondo. Unas manitas lo agarran. Y tiran."),
    ("camara",   "La cámara ve la caja seguir por la cinta. Diego ya no está."),
    ("final",    "Por la mañana, su mujer firmó un paquete. Pesaba lo que un hombre."),
]
