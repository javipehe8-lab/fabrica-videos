# Serie 3D: "TURNO DE NOCHE" (sustituye a El Sonriente desde el 13/11/2026)

Terror en 3D de pocos polígonos con look de PlayStation 2 (motor propio `stick/motor3d.py` + escenario `stick/turno3d.py`). Canal "Historias de las 3AM" a las **23:00**; versión inglesa **"NIGHT SHIFT"** para el canal inglés (Javi la sube a mano a las 00:30).

## Premisa (se dice en la primera frase de CADA episodio, con otras palabras)
"Trabajo solo, de noche, en una gasolinera perdida en la niebla. Hay una lista de reglas. Y cada noche descubro por qué."
- Narrador en **primera persona** (yo, el empleado nuevo; nunca se le ve la cara: casi siempre plano subjetivo, cámaras de seguridad o de espaldas).
- Lugar: Gasolinera **Kilómetro 9**, en una carretera nacional sin tráfico, con niebla todas las noches. Tienda con mostrador, caja, estanterías y nevera; marquesina con 3 surtidores; carretera; farola; cámaras de seguridad (CAM 1 tienda, CAM 2 surtidores, CAM 3 carretera).
- La lista: una hoja plastificada pegada junto a la caja, con reglas numeradas. Al pie, notas escritas a mano por el empleado anterior, **Raúl**, que desapareció.

## Formato de cada episodio (OBLIGATORIO)
1. **Un episodio = una regla.** Título: "Regla N: <la regla>". La regla se lee en pantalla (`hoja_reglas`) en las primeras escenas.
2. **Se entiende solo**: situación concreta → alguien o algo pone a prueba la regla → el narrador la cumple (o casi) → **giro lógico** que encaja con una pista que ya se vio (en la hoja, en una cámara, en algo que se dijo).
3. 8-9 escenas, **35-45 s**, frases de máx. ~12 palabras. 1-2 diálogos cortos como mucho (`VOCES`/`MONSTRUOS`/`ETIQUETAS` en el guion).
4. Escena `final`: tarjeta "REGLA N" + la regla + "MAÑANA: REGLA N+1". Narración final: "<frase de cierre>. Mañana, la regla <N+1>." (inglés: "Tomorrow, rule <N+1>.")
5. Sin gore. El miedo viene de lo que no encaja: algo que no debería estar, alguien que repite, una cámara que muestra otra cosa.
6. Misterio de fondo (avanza poco a poco, una pista cada 2-3 episodios, nunca obligatorio para entender el episodio): ¿qué le pasó a Raúl?, ¿quién escribió las reglas?, ¿por qué el kilómetro 9 no sale en los mapas?

## Técnica
- Archivos: `stick/guionnocheK.py`, `stick/guionnocheK_en.py` (mismos nombres de escena) y `stick/escenasnocheK.py`. `TITULO = "TURNO DE NOCHE"` (en inglés "NIGHT SHIFT"), `PARTE = K`, `ESTILO = "ps2_3d"`, `MUSICA` según el tono. Sin GANCHO ni ELECCION: la primera escena ya es un plano 3D inquietante con la voz desde el primer fotograma.
- Las escenas usan `turno3d.py`: `mundo(...)` construye toda la gasolinera (tienda + marquesina + surtidores + carretera) en una sola escena 3D; `cam_*` dan planos típicos (llegada, mostrador, ventana, CCTV); `cctv(img, cam, hora)` convierte un plano en imagen de cámara de seguridad; `hoja_reglas(...)` dibuja la hoja en primer plano; `empleado(...)` y `cliente(...)` son los personajes; `luces_base(...)` son las luces de la escena. Reutiliza `escenasnoche1.py` como modelo y añade piezas nuevas en `turno3d.py` (no en el episodio) si sirven para más episodios.
- `bash hacer_episodio.sh nocheK` → `videos/turno/Turno_de_Noche_K.mp4`; `bash hacer_episodio.sh nocheK en` → `videos/turno/en/Night_Shift_K.mp4`.
- Piezas añadidas en la Parte 2: `cabina(..., luz, vibra, colgado)` (vía `mundo(cabina_kw=...)`), `luz_cabina()`, `telefono()` del mostrador, `cam_cabina(cctv=True)` (CAM 3 apuntando a la cabina) y la constante `CABINA`.
- Texto en pantalla con `tr()` y su traducción en `EN` de `motor.py`.
- Registro: `publicaciones_turno.json`.

## Banco de reglas (usa la siguiente sin [HECHA]; marca [HECHA] al usarla)
1. [HECHA] **No existe el surtidor 4.** Si alguien lo pide, dile que no existe. — Un hombre empapado pide el 4; en la niebla aparece un cuarto surtidor. Le dices que no. En la CAM 2, junto al surtidor 4, alguien con tu uniforme saluda. Nota de Raúl al pie: "Yo le dije que sí."
2. [HECHA] **Si suena el teléfono de la cabina a las 3:00, no lo cojas.** — Suena y suena. Para, y suena el teléfono de la tienda: es tu voz desde la cabina, pidiendo que salgas porque "hay algo detrás de ti". En la CAM 1, detrás del mostrador, no hay nadie… salvo tú, de espaldas a la cámara, mirando la cabina. Pero tú estás en la cabina, en el reflejo del cristal. *Versión emitida (Parte 2): no la coges; llama al teléfono de la tienda (pantalla: CABINA KM 9) con tu propia voz: "Sal. Ya. Tienes algo detrás." En la CAM 1 no hay nadie; en la CAM 3, alguien con tu uniforme está en la cabina con el auricular, mirándote. Cierre: "Si hubiera salido, ahora estaría yo en esa cabina."*
3. **El baño está siempre roto.** Si alguien pide la llave, di que está roto. — Una niña pide la llave; dices que está roto. Desde dentro del baño cerrado con llave se oye a la misma niña pidiendo ayuda. Giro: la llave del baño, que tú tienes en el bolsillo, está mojada.
4. **No sirvas a nadie que pague con monedas antiguas.** — Un anciano paga con pesetas de 1986. Se las devuelves. Al mirar la fecha de la caja registradora: 1986.
5. **Si la niebla entra en la tienda, apaga todas las luces y no respires.** — La niebla pasa por debajo de la puerta; apagas; algo camina entre las estanterías. Al encender, todas las latas están giradas hacia ti.
6. **No le des indicaciones a nadie que pregunte por el kilómetro 10.** — Un coche familiar pregunta por el km 10. No lo hay. Media hora después, el mismo coche pasa otra vez. Y otra. Cada vez con una persona menos dentro.
7. **Si el camión de reparto llega antes de las 6, no firmes nada.** — El albarán ya tiene tu firma. Y la fecha de mañana.
8. **Las cámaras siempre van 10 segundos por detrás. Si alguna va por delante, sal por la puerta de atrás.** — La CAM 1 muestra a alguien entrando… y la puerta aún no se ha abierto.
9. **Si ves a Raúl, no le dejes entrar.** — Raúl, con su uniforme, golpea el cristal y dice que es un error, que le dejes explicarse. Llora. Al día siguiente, el encargado: "Raúl nunca existió. Ese uniforme es de tu talla."
10. **Si un cliente sabe tu nombre, no le digas el tuyo verdadero.** — Un hombre te llama por tu nombre. Le dices otro. Sonríe y escribe ese nombre en la hoja de reglas, al final: "Regla 11".

Cuando queden menos de 4 reglas sin hacer, añade 8 nuevas con las mismas condiciones (concretas, lógicas, con pista previa y giro), haciendo avanzar el misterio de Raúl y del kilómetro 9.
