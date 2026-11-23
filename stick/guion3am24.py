# Si oyes esto a las 3AM — 24: "La foto de la puerta"
# Tu timbre con cámara te avisó a las tres: alguien en tu puerta. En la grabación, una figura pálida mira fijo al objetivo
# sin moverse: 3:00, 3:10, 3:30, 3:47. A las 3:48 el porche está vacío y tu puerta, abierta. Miras la hora del móvil: 3:48.
# Giro: no se fue, acaba de entrar. Sube la escalera y abre tu cuarto: "Te vi mirándome" (por eso miraba a la cámara).
# En una frase: estabas viendo la grabación justo cuando él dejó de mirar a la cámara para entrar en tu casa.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "tension"
VOCES = {"VISITA": ("em_santa", 0.85, -4)}
MONSTRUOS = {"VISITA"}
ETIQUETAS = {"VISITA": "EL DE LA PUERTA"}
ESCENAS = [
    ("aviso",    "Tu timbre con cámara te avisó a las tres: hay alguien en tu puerta."),
    ("video",    "Abres el vídeo. Alguien mira fijo a la cámara. No llama."),
    ("rapido",   "Lo adelantas. Las tres y diez. Las tres y media. No se mueve."),
    ("cuarenta", "Las tres y cuarenta y siete. Sigue ahí, mirándote."),
    ("abierta",  "Las tres y cuarenta y ocho. Ya no está. Tu puerta está abierta."),
    ("hora",     "Miras la hora del móvil. Son las tres y cuarenta y ocho."),
    ("escalera", "No se fue. Entró. Y algo sube despacio por la escalera."),
    ("cuarto",   "La puerta de tu cuarto se abre. [VISITA] Te vi mirándome."),
    ("final",    "Si a las tres hay alguien en tu timbre… no mires a qué hora se fue."),
]
