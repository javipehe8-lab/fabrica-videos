# Serie 3D: "REGLAS" (sustituye a "Turno de noche" desde el 25/11/2026, a las 23:00)

Terror en 3D de pocos polígonos con look de PlayStation 2 (`stick/motor3d.py` + kit `stick/escenarios3d.py` + piezas de `stick/turno3d.py`). Historias **autoconclusivas**: cada noche, un sitio distinto, un trabajador distinto con nombre propio y una lista de reglas. **Alguien rompe una regla y paga un precio drástico e irreversible.**

## Por qué existe (datos del 23/11)
- "Turno de noche" con historia encadenada (Partes 6-10): la gente veía solo el 27-37 % del vídeo. Quien llega nuevo no entiende nada.
- Las historias que se entienden solas (3AM, Turno 1-5) se ven al 55-80 %.
- Javi quiere que esta serie se diferencie de "Si oyes esto a las 3AM": **final drástico**, no un consejo.

## En qué se DIFERENCIA de "Si oyes esto a las 3AM" (OBLIGATORIO)
| | Si oyes esto a las 3AM | REGLAS |
|---|---|---|
| Estilo | 2D stickman | 3D PS2 |
| Narrador | segunda persona ("tú") | **tercera persona, protagonista con nombre y oficio** ("Óscar es celador de noche…") |
| Lugar | tu casa, tu vida | **un trabajo nocturno o un sitio cerrado de noche**: hospital, hotel, metro, piscina, gasolinera, colegio, parking, morgue, centro comercial, faro, residencia, estación de esquí, barco… (cada noche uno distinto) |
| Final | la regla en grande, como consejo; el protagonista suele salvarse | **el protagonista rompe una regla (por un motivo humano y creíble) y lo pierde todo de forma irreversible**: desaparece, lo sustituyen, se queda atrapado, se convierte en lo que temía. Cierre con `ficha_final(...)`: ficha del trabajador con el sello DESAPARECIDO (o FALLECIDO / NO IDENTIFICADO / SUSTITUIDO según el caso) |

## Formato de cada episodio (OBLIGATORIO)
1. **Arranque (escena 1):** plano cercano y claro del sitio y de la amenaza (`aclarar(img)`), con `rotulo_regla(img, 1, "<la regla que se va a romper>")` encima desde el fotograma 0. Primera frase: la regla + la amenaza de esta noche. Ej.: "Regla uno: si llaman desde la 414, no vayas. Esta noche han llamado once veces."
2. **Escena 2: quién y dónde, en UNA frase, y ya pasando algo** ("Óscar es celador de noche. La 414 lleva un año vacía."). Nunca escenas de "presentación" lentas.
3. **El motivo para romperla tiene que ser humano** (la voz de su madre, un niño que llora, el miedo a perder el trabajo, la curiosidad, salvar a alguien). El espectador tiene que pensar "yo también lo haría".
4. **Escalada en 2-3 escenas** y **final drástico** en las dos últimas escenas: algo irreversible le pasa al protagonista, visto en el momento (plano cercano) y confirmado desde fuera (cámara de seguridad, otro trabajador, la mañana siguiente). Corte seco o fundido a negro con `negro(img, k)` y un sonido fuerte (monitor plano, puerta, golpe).
5. **Escena final:** `ficha_final(img, nombre, oficio, fecha_hora, regla_rota, p, t)`. Narración final, corta y seca, con la consecuencia (ej.: "A la noche siguiente, la 414 volvió a llamar. Con la voz de Óscar."). Sin "mañana, la regla…" (no hay continuidad).
6. 8 escenas, **35-45 s**, frases de máx. ~12 palabras. 1-2 diálogos cortos como mucho (`VOCES`, `MONSTRUOS`, `ETIQUETAS`).
7. Sin gore ni sangre: lo drástico es lo que le pasa, no cómo se ve.
8. Nunca repitas sitio ni tipo de final dos días seguidos. Apunta cada episodio en "Episodios emitidos".

## Técnica
- Archivos: `stick/guionreglasK.py`, `stick/guionreglasK_en.py` (mismos nombres de escena) y `stick/escenasreglasK.py`. `TITULO = "REGLAS"` (inglés "RULES"), `PARTE = None`, `ESTILO = "ps2_3d"`, `MUSICA` según el tono. Sin GANCHO ni ELECCION.
- Kit `escenarios3d.py`: `escena()`, `habitacion(...)`, `pasillo(... puertas, luces_on)` (devuelve las luces), `puerta(...)`, `fluorescente(...)`, `cama(...)`, `monitor_constantes(...)`, `interfono(...)`, `panel_llamadas(img, …)`, `ascensor(...)`, `negro(img, k)`, `ficha_final(..., sello="DESAPARECIDO")` (el sello cambia: SUSTITUIDA, FALLECIDA…). Hotel: `vestibulo(...)`, `mostrador`, `claveros`, `timbre`, `lampara_mesa`, `pasillo_hotel(...)`, `libro_reservas(img, …)`. Además, de `turno3d.py`: `cctv(img, n, hora)`, `aclarar`, `rotulo_regla`, `etiquetas`, `hoja_reglas`, personajes `cliente`, `nina`, `anciano`, `figura_niebla`, y de `motor3d.py`: `humano(...)`. Si un sitio nuevo necesita piezas (taquillas, piscina, vagón de metro, mostrador de hotel…), añádelas a `escenarios3d.py` para que sirvan a otros episodios. Modelo completo: `escenasreglas1.py`.
- `bash hacer_episodio.sh reglasK` → `videos/reglas/Reglas_K.mp4`; con `en` → `videos/reglas/en/Rules_K.mp4`.
- Título de YouTube: "<La regla, corta> 😱 #shorts" (sin "Parte N"; ej.: "Si llaman desde la 414, no vayas 😱 #shorts"). Descripción: el oficio + la regla + una pregunta ("¿Tú habrías ido?") + hashtags (#reglas #terror #historiasdeterror #miedo #ps2 #creepy #animacion #shorts).
- Registro: entrada en `cola_youtube.json` con `"serie": "reglas"` (hora 23:00).

## Banco de ideas (usa la primera sin [HECHA]; marca [HECHA] al usarla; añade 8 más cuando queden menos de 4)
1. [HECHA] **Hospital, planta 4 — Óscar, celador.** "Si llaman desde la 414, no vayas." La 414 lleva un año vacía; por el interfono habla su madre, que murió allí. Va. En la cama, tapado, está él mismo. La puerta se cierra; monitor plano. Ficha: DESAPARECIDO. A la noche siguiente la 414 llama con la voz de Óscar.
2. [HECHA] **Hotel — Lucía, recepcionista de noche.** "No des nunca la llave de la habitación 0." Un huésped empapado insiste en que reservó la 0. Ella mira el libro: la reserva está, a su nombre, para esta noche. Le da la llave para comprobarlo… la cámara del pasillo la ve entrar a ella en la 0. Ficha: SUSTITUIDA (a la mañana, en recepción, hay otra Lucía que sonríe demasiado).
3. **Metro, último tren — Andrés, vigilante.** "Si el tren de las 2:40 para en el andén, no subas." El tren abre las puertas; dentro, sentados, todos los que desaparecieron en esa línea. Su hermano, desaparecido hace 5 años, le hace sitio. Sube. Ficha: DESAPARECIDO. En el cartel de la estación, su foto entre los "Se busca".
4. **Piscina municipal — Marta, socorrista de cierre.** "Después de cerrar, no mires el fondo de la piscina." Oye chapoteos, alguien pide ayuda; salta. Desde fuera, la cámara solo ve el agua quieta… y una mano que sale, la de Marta, y vuelve a hundirse.
5. **Residencia de ancianos — Iván, auxiliar.** "Si la señora de la 9 dice tu nombre, sal de la habitación." Ella lo dice, él se queda a calmarla. Por la mañana, en la cama de la 9 hay un anciano con su cara.
6. **Parking subterráneo — Sara, guardia de seguridad.** "Si ves un coche en la plaza 13, no te acerques." Hay uno, con las luces dadas y alguien dentro llorando. Abre la puerta: el que llora es su padre muerto. Ficha: FALLECIDA (encontrada dentro del coche, plaza 13, con el motor apagado desde 1998).
7. **Morgue — Raúl, forense de guardia.** "Si una cámara frigorífica está abierta, ciérrala sin mirar el nombre." Mira: el nombre de la etiqueta es el suyo. La puerta se cierra detrás de él.
8. **Centro comercial — Nerea, limpiadora.** "Si los maniquíes están mirando a otro sitio, apaga la luz y vete." Se queda a terminar. Al encender, uno más en el escaparate. Lleva su uniforme.
9. **Estación de esquí, cabina de remontes — Pablo, operario.** "No pongas en marcha el telesilla después de medianoche." Una cabina baja ocupada. Arranca para ayudar. La cámara ve subir la cabina… con Pablo dentro, saludando.
10. **Colegio, vigilante nocturno — Tomás.** "Si oyes recreo, no salgas al patio." Risas de niños; sale a buscarlos. Por la mañana, en la foto de clase colgada en el pasillo, hay un adulto nuevo al fondo.

## Episodios emitidos
1. (25/11) Hospital, Óscar, la 414. Final: lo sustituye la cosa de la cama; la 414 llama con su voz. Sello DESAPARECIDO.
2. (26/11) Hotel, Lucía, la habitación 0. Un huésped empapado pide la 0 y la reserva está a nombre de Lucía; le da la llave y la cámara la ve entrar a ella.
   Final: por la mañana hay otra Lucía en recepción que sonríe sin parpadear; la de verdad pide ayuda desde la 0. Sello SUSTITUIDA.
