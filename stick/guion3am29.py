# Si oyes esto a las 3AM — 29: "El altavoz inteligente"
# A las tres, el altavoz de tu mesilla se ilumina y obedece una orden que nadie le dio: desactiva la alarma de la puerta.
# Vives solo y dormías. Le preguntas quién se lo ordenó y te pone la grabación: es TU voz… y de fondo, alguien ronca.
# Pista: en el primer plano, la ventana de encima del altavoz está entreabierta (la cortina se mueve) y, pegada al cristal,
# casi invisible, hay una cara pálida. Cuando te despiertas ya no está.
# Giro: los ronquidos son tuyos; lo que habló con tu voz estaba en tu ventana, junto al altavoz. Abajo la puerta hace clic,
# suben pasos, se abre tu puerta y, con tu voz: "Apaga la luz". El altavoz obedece.
# En una frase: algo que imita tu voz usó tu altavoz para desactivar la alarma y entrar a por ti.
TITULO = "SI OYES ESTO A LAS 3AM"
PARTE = None
MUSICA = "piano"
VOCES = {"ALTAVOZ": ("ef_dora", 1.0, 0), "COPIA": ("em_santa", 0.85, -3)}
RADIOS = {"ALTAVOZ"}                      # voz por el altavoz
MONSTRUOS = {"COPIA"}                     # tu voz… pero no eres tú
ETIQUETAS = {"ALTAVOZ": "EL ALTAVOZ", "COPIA": "¿TÚ?"}
ESCENAS = [
    ("luz",       "Son las tres. Tu altavoz se enciende solo, como si alguien le hablara."),
    ("orden",     "[ALTAVOZ] De acuerdo. Desactivando la alarma de la puerta."),
    ("solo",      "Te despiertas. Vives solo. Nadie le ha dicho nada."),
    ("preguntas", "Le preguntas quién le dio la orden. Y te pone la grabación."),
    ("voz",       "Es tu voz… {susurro} Y de fondo, muy cerca, alguien ronca."),
    ("ronca",     "Esos ronquidos son tuyos. Lo que habló estaba en tu ventana."),
    ("clic",      "Abajo, la puerta de la calle hace clic. Pasos en la escalera."),
    ("apaga",     "Tu puerta se abre despacio. [COPIA] Apaga la luz."),
    ("final",     "Si a las tres tu altavoz obedece a alguien… no preguntes a quién."),
]
