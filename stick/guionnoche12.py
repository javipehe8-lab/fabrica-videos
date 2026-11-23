# TURNO DE NOCHE — 12 (FINAL DE TEMPORADA): "Regla 12: Nunca devuelvas el saludo" (la escribo yo)
# Viene de la Parte 11: crucé el kilómetro 10; en la otra gasolinera tres empleados con mi uniforme me saludaban
# y en su mostrador había una hoja de reglas en blanco con "Regla 12:" escrito con mi letra.
# Les devuelvo el saludo y ya estoy detrás del mostrador, en el hueco que me guardaban. Entiendo que cada regla
# la escribió alguien justo después de perder: escribo la mía. A las siete entra el nuevo del turno de noche con su hoja:
# está escrita entera con mi letra. En la CAM 1 sale él solo ("¿Hola? ¿Hay alguien?").
# Final: ya solo salgo en la CAM 2, junto al surtidor 4, saludando (como en la Parte 1) -> provoca la temporada 2 (regla 13).
TITULO = "TURNO DE NOCHE"
PARTE = 12
ESTILO = "ps2_3d"
MUSICA = "caja"
VOCES = {"NUEVO": ("em_santa", 1.12, 5)}
ETIQUETAS = {"NUEVO": "EL NUEVO"}
REGLAS = ["NO EXISTE EL SURTIDOR 4. SI ALGUIEN LO PIDE, DI QUE NO EXISTE.",
          "SI SUENA EL TELÉFONO DE LA CABINA A LAS 3:00, NO LO COJAS.",
          "EL BAÑO ESTÁ SIEMPRE ROTO. SI PIDEN LA LLAVE, DI QUE ESTÁ ROTO.",
          "NO SIRVAS A NADIE QUE PAGUE CON MONEDAS ANTIGUAS.",
          "SI LA NIEBLA ENTRA EN LA TIENDA, APAGA TODAS LAS LUCES Y NO RESPIRES.",
          "SI ALGUIEN PREGUNTA POR EL KILÓMETRO 10, DI QUE NO EXISTE.",
          "NO LEAS NADA QUE NO HAYAS ESCRITO TÚ.",
          "SI EL CAMIÓN DE REPARTO LLEGA ANTES DE LAS 6, NO FIRMES NADA.",
          "SI VES A RAÚL, NO LE DEJES ENTRAR.",
          "LAS CÁMARAS VAN 10 SEGUNDOS POR DETRÁS. SI ALGUNA VA POR DELANTE, SAL POR LA PUERTA DE ATRÁS.",
          "NUNCA CRUCES EL KILÓMETRO 10.",
          "SI ALGUIEN CON TU UNIFORME TE SALUDA, NUNCA LE DEVUELVAS EL SALUDO.",
          "?"]
REGLA_CORTA = "NUNCA DEVUELVAS EL SALUDO"
# la hoja del nuevo: todas las reglas, con mi letra
LISTA = ["1. No existe el surtidor 4.", "2. No cojas la cabina a las 3.", "3. El baño está roto.", "4. Nada de monedas antiguas.",
         "5. Si entra la niebla, no respires.", "6. El km 10 no existe.", "7. No leas lo que no escribas.", "8. No firmes antes de las 6.",
         "9. No dejes entrar a Raúl.", "10. Vigila las cámaras.", "11. No cruces el km 10.", "12. Nunca devuelvas el saludo."]
REGLA_MANO = ["Regla 12:", "Nunca devuelvas", "el saludo."]
ESCENAS = [
    ("arranque", "Regla doce: nunca devuelvas el saludo. Esta noche lo devolví."),
    ("mano",     "Mi mano siguió saludando sola. Y ya estaba detrás del mostrador."),
    ("hoja",     "Delante, una hoja de reglas en blanco. Con mi letra: regla doce."),
    ("escribo",  "Cada regla la escribió alguien justo después de perder. Escribo la mía."),
    ("nuevo",    "A las siete se abre la puerta. Entra el nuevo, con su hoja."),
    ("lista",    "Su lista está escrita entera con mi letra. También la regla uno."),
    ("camara",   "En la cámara uno sale él solo. [NUEVO] ¿Hola? ¿Hay alguien?"),
    ("final",    "Ahora solo salgo en la cámara dos, saludando. Mañana, la regla trece."),
]
