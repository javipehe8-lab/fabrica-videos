# Si oyes esto a las 3AM — 15: "La radio del abuelo"
# Cada noche a las tres, la vieja radio del abuelo se enciende sola y da el parte del tiempo. Hoy da un aviso:
# "Se busca a un hombre. Calle del Olmo, siete." Es tu casa, y vives solo.
# Pista: desde el primer plano del cuarto hay un "perchero" en el rincón, con un abrigo gris y un sombrero.
# La radio da la descripción: "Abrigo gris y sombrero. Está escuchando la radio."
# Giro: tú no tienes perchero. La radio se calla y el sombrero gira despacio hacia ti.
# En una frase: la radio te avisaba de que el hombre que buscan llevaba toda la noche quieto en tu cuarto.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "piano"
VOCES = {"LOCUTOR": ("em_alex", 1.0, -2)}
RADIOS = {"LOCUTOR"}                      # voz filtrada como por un altavoz viejo (voz.py)
ETIQUETAS = {"LOCUTOR": "RADIO"}
ESCENAS = [
    ("radio",    "Cada noche a las tres, la radio del abuelo se enciende sola."),
    ("tiempo",   "Siempre da el tiempo. Tú te duermes escuchándola. Hoy no."),
    ("aviso",    "Hoy da un aviso. [LOCUTOR] Se busca a un hombre. Calle del Olmo, siete."),
    ("casa",     "Calle del Olmo, siete. Es tu casa. Y vives solo."),
    ("abrigo",   "[LOCUTOR] Lleva abrigo gris y sombrero. Está escuchando la radio."),
    ("rincon",   "Abrigo gris y sombrero. Como el del perchero del rincón."),
    ("perchero", "Pero tú… no tienes perchero."),
    ("gira",     "La radio se calla. Y el sombrero, despacio, gira hacia ti."),
    ("final",    "Si a las tres se enciende la radio… escucha la dirección."),
]
