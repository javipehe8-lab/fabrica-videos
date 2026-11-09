# Si oyes esto a las 3AM — 10: "El ascensor"
# Tu edificio tiene doce plantas. A las tres, el ascensor para en la trece.
# Se abre a un pasillo igual que el tuyo: tu felpudo, tu número (12B)… y alguien de espaldas metiendo una llave en tu puerta.
# Pista: lleva una sudadera verde como la tuya y TU llavero verde (el pasillo, la puerta y la ropa: todo es tuyo).
# Sales para verle mejor. Se da la vuelta: tiene tu cara, con una sonrisa que tú nunca pones.
# Giro: no quería tu casa de la planta trece; quería que salieras. Entra en el ascensor y las puertas se cierran contigo fuera.
# En una frase: en la planta trece te espera otro tú, y en cuanto sales del ascensor, él vuelve a tu casa en tu lugar.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "tension"
VOCES = {"COPIA": ("em_alex", 0.95, -2)}      # tu propia voz, más lenta y grave, con eco de monstruo
MONSTRUOS = {"COPIA"}
ETIQUETAS = {"COPIA": "¿TÚ?"}
ESCENAS = [
    ("panel",    "Tu edificio tiene doce plantas. A las tres, el ascensor para en la trece."),
    ("abre",     "Se abren las puertas. Es un pasillo igual que el tuyo."),
    ("puerta",   "Tu felpudo. Tu número. Y alguien de espaldas frente a tu puerta."),
    ("llaves",   "Lleva una sudadera verde, como la tuya. Y tus llaves."),
    ("sales",    "Sales del ascensor para verle mejor. Se da la vuelta."),
    ("cara",     "Tiene tu cara. Pero tú nunca has sonreído así."),
    ("voz",      "[COPIA] Gracias. Ya vuelvo yo a casa."),
    ("cierra",   "Las puertas se cierran. Y tú te quedas en la trece."),
    ("final",    "Si a las tres el ascensor para en la trece… no salgas."),
]
