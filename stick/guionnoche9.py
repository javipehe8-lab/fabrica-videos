# TURNO DE NOCHE — 9: "Regla 9: Si ves a Raúl, no le dejes entrar"
# Viene de la Parte 8: llevo toda la noche con la placa de Raúl; fuera, en la niebla, alguien con mi uniforme miraba hacia la tienda.
# A las 3:00 Raúl golpea el cristal de la puerta, empapado y llorando: "Nos han cambiado. Déjame explicártelo."
# Su placa no dice Raúl: dice mi nombre (corrido por el agua). No abro. Deja de llorar de golpe y sonríe.
# Final: en la CAM 1, el que golpea el cristal desde fuera soy yo; dentro, detrás del mostrador, está él, mirando a la cámara
# (provoca la Parte 10: las cámaras ya no van por detrás).
TITULO = "TURNO DE NOCHE"
PARTE = 9
ESTILO = "ps2_3d"
MUSICA = "caja"
VOCES = {"RAUL": ("em_santa", 1.02, 3)}
ETIQUETAS = {"RAUL": "RAÚL"}
REGLAS = ["NO EXISTE EL SURTIDOR 4. SI ALGUIEN LO PIDE, DI QUE NO EXISTE.",
          "SI SUENA EL TELÉFONO DE LA CABINA A LAS 3:00, NO LO COJAS.",
          "EL BAÑO ESTÁ SIEMPRE ROTO. SI PIDEN LA LLAVE, DI QUE ESTÁ ROTO.",
          "NO SIRVAS A NADIE QUE PAGUE CON MONEDAS ANTIGUAS.",
          "SI LA NIEBLA ENTRA EN LA TIENDA, APAGA TODAS LAS LUCES Y NO RESPIRES.",
          "SI ALGUIEN PREGUNTA POR EL KILÓMETRO 10, DI QUE NO EXISTE.",
          "NO LEAS NADA QUE NO HAYAS ESCRITO TÚ.",
          "SI EL CAMIÓN DE REPARTO LLEGA ANTES DE LAS 6, NO FIRMES NADA.",
          "SI VES A RAÚL, NO LE DEJES ENTRAR.",
          "?"]
REGLA_CORTA = "SI VES A RAÚL, NO LE DEJES ENTRAR"
NOTA = "No soy yo. — R."
ESCENAS = [
    ("arranque", "Regla nueve: si ves a Raúl, no le dejes entrar. Está en la puerta."),
    ("premisa",  "Trabajo solo, de noche, en la niebla. Desde anoche llevo su placa."),
    ("golpes",   "Tres en punto. Raúl golpea el cristal. Empapado. Llorando."),
    ("habla",    "Me mira. [RAUL] Nos han cambiado. ¡Déjame explicártelo!"),
    ("placa",    "Su placa no dice Raúl. Dice mi nombre. Corrido por el agua."),
    ("noabro",   "No abro. Deja de llorar de golpe. Y sonríe."),
    ("cam1",     "Miro la cámara uno. Fuera, golpeando el cristal, estoy yo."),
    ("final",    "Y detrás del mostrador, mirando a la cámara, está él. Mañana, la regla diez."),
]
