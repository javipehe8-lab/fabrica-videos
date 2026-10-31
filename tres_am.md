# Serie 2: "SI OYES ESTO A LAS 3AM"

Historias de terror **autoconclusivas** (cada vídeo empieza y acaba), en el mismo canal que El Sonriente. Se publica a las **19:00** (Europe/Madrid); El Sonriente sale a las 23:00.

## Qué tiene que tener cada historia (OBLIGATORIO)
1. **Una situación concreta y cotidiana a las 3 de la mañana**: un ruido, una llamada, un mensaje, alguien en la puerta… Nada abstracto ni "porque sí".
2. **Una lógica que se entienda a la primera**: el espectador tiene que poder explicar la historia en una frase. Si el giro necesita explicación, no vale.
3. **Una pista que el espectador ya tenía**: el giro da miedo porque encaja con algo que vio u oyó antes (la voz, el mensaje, la foto…). Nada de "y entonces apareció un monstruo".
4. **Narrada en segunda persona** ("Son las tres. Tu madre te llama desde la cocina."). El protagonista es `TU` (escenas3am1.py), sin nombre.
5. **Termina con la regla** que da título al vídeo: "Si a las tres te llaman desde la cocina… no bajes." en grande en pantalla + "SÍGUEME PARA MÁS".
6. **Nada de gore ni sangre**: el miedo viene de la idea, el silencio y el giro.

## Formato técnico
- Archivos: `stick/guion3amK.py` + `stick/escenas3amK.py` (K = número de la historia), efectos en `sonido.py` dentro de un bloque `if os.environ.get("EP") == "3amK": ... continue` (ver el de 3am1).
- `TITULO = "SI OYES ESTO A LAS 3AM"`, `PARTE = None`, SIN `GANCHO` ni `ELECCION`: la voz empieza en el primer fotograma, y el primer plano tiene que ser ya inquietante (ej.: el reloj con 3:00 en rojo, muy cerca).
- 8-9 escenas, **35-45 s**. Primera frase: la situación entera en una línea.
- Personajes propios con `VOCES = {"NOMBRE": (voz_kokoro, velocidad, semitonos)}`, `MONSTRUOS = {...}` (voz con eco/susurro y subtítulo rojo) y `ETIQUETAS = {"NOMBRE": "TEXTO DE LA ETIQUETA"}`. Ej.: la cosa que imita tu voz lleva la etiqueta "¿TÚ?". Máximo 1-2 frases de diálogo.
- Reutiliza piezas de `escenas3am1.py` (TU, MAMA, cuarto_casa, escalera_casa, puerta_cocina, movil_msg, reloj_3am, imitadora…) y de los episodios del Sonriente (iluminar, pasillo_h, lluvia, carretera…). Todo texto en pantalla con `tr()`.
- `bash hacer_episodio.sh 3amK` → `videos/3am/Si_Oyes_Esto_K.mp4`. URL: `https://raw.githubusercontent.com/javipehe8-lab/fabrica-videos/main/videos/3am/Si_Oyes_Esto_K.mp4`
- Registro: `publicaciones_3am.json`.

## Banco de historias (usa la primera que no esté hecha; marca [HECHA] al usarla)
1. [HECHA] **No bajes** — Tu madre te llama desde la cocina; tu madre real te escribe "no bajes, yo también la he oído". Giro: la cosa ahora la llama a ella… con TU voz.
2. **El asiento de atrás** — Conduces de noche; un coche te sigue dándote las largas sin parar. Paras asustado y el conductor grita: "¡Hay alguien en tu asiento de atrás!". Las largas eran para que no te atacara. Regla: si un coche te da las largas a las 3… mira atrás.
3. **Tu compañero de piso** — Llaman al timbre: "Abre, soy yo, me he dejado las llaves". Es la voz de tu compañero. Le escribes y te contesta desde su cama: "No abras. Lleva una semana imitándome". Giro: el pomo empieza a girar solo; tenía llaves. Regla: si a las 3 alguien olvidó sus llaves… no abras.
4. **La mirilla** — En un hotel oyes pasos; por la mirilla todo está rojo. Por la mañana la recepcionista: "El de la habitación de enfrente tiene los ojos rojos". Lo rojo era su ojo, mirándote. Regla: si a las 3 tu mirilla está roja… no mires.
5. **El perro te lame la mano** — Tu perro duerme bajo la cama y te lame la mano cada vez que tienes miedo. A las 3 oyes gotear en el baño; vas y tu perro está muerto en la ducha, con una nota en el espejo: "Los humanos también saben lamer". Regla: si a las 3 algo te lame la mano… no la bajes.
6. **El vigilabebés** — Por el vigilabebés oyes a alguien cantándole una nana a tu hermano pequeño. En casa solo estáis tú y él. Corres y está dormido, solo. El vigilabebés vuelve a sonar: "Shhh… ya se ha ido". Ahora la voz está en tu cuarto. Regla: si a las 3 alguien canta en el vigilabebés… no contestes.
7. **La estatua del payaso** — Haces de canguro; un payaso de tamaño real en una esquina te da mal rollo. Llamas a los padres para preguntar si puedes taparlo: "Nosotros no tenemos ninguna estatua. Coge a los niños y sal". Regla: si a las 3 ves algo que no debería estar ahí… no le des la espalda.
8. **Tu número te llama** — Te llama tu propio número. Tu voz susurra: "No te levantes. Hay alguien debajo de la cama". Giro: debajo de la cama… también suena un móvil. Regla: si a las 3 te llamas tú… haz caso.
9. **Las huellas en la nieve** — Nieva toda la noche. A las 3 ves huellas que llegan hasta tu puerta. Ninguna se va. Giro: la puerta está cerrada desde dentro. Regla: si a las 3 hay huellas que solo vienen… no busques quién.
10. **El ascensor** — Tu edificio tiene 12 plantas. A las 3 el ascensor para en la 13. Se abre: un pasillo igual que el tuyo, con alguien en tu puerta esperando. Se da la vuelta: eres tú. Regla: si a las 3 el ascensor para en la 13… no salgas.
11. **El mensaje de tu amigo** — Tu mejor amigo te escribe a las 3: "Abre, tengo frío". Lo enterraron ayer. Giro: el doble check azul aparece… en un mensaje que tú no has enviado: "Ya bajo". Regla: si a las 3 te escribe quien no puede… no leas.
12. **El flash** — Se va la luz; usas el flash del móvil para hacer fotos y ver el cuarto. En cada foto, una figura está un poco más cerca de tu cama. En la última, la foto la ha hecho ella. Regla: si a las 3 se va la luz… no hagas fotos.
13. **El vecino de enfrente** — Cada noche, a las 3, el vecino de enfrente te saluda desde su ventana. Hoy su ventana está vacía. Tu móvil hace una foto sola con la cámara frontal: está detrás de ti, saludando. Regla: si a las 3 alguien te saluda… no le devuelvas el saludo.
14. **El reflejo que tarda** — En el espejo del baño, tu reflejo parpadea un segundo tarde. Te acercas. El reflejo sonríe; tú no. Regla: si a las 3 tu reflejo llega tarde… no te acerques.
15. **La radio del abuelo** — La radio vieja se enciende sola cada noche a las 3 y da el parte del tiempo. Hoy da un aviso: "Se busca a un hombre en la calle de [tu calle]. Está en el número 7". Tú vives en el 7. Regla: si a las 3 se enciende la radio… escucha la dirección.
16. **El taxi** — Pides un taxi a las 3. El conductor no habla; por el retrovisor sus ojos no parpadean. Le escribes a tu amiga la matrícula. Responde: "Ese taxi se estrelló en 1998". Regla: si a las 3 el taxista no parpadea… no te bajes donde él pare.
17. **Las escaleras de más** — Cada noche bajas 13 escalones a la cocina. Hoy cuentas 14. Y el último está blando. Regla: si a las 3 hay un escalón de más… no lo pises.
18. **El niño del columpio** — Desde tu ventana ves un niño columpiándose solo en el parque a las 3. Llamas a la policía; cuando cuelgas, el columpio sigue moviéndose… y el niño está en tu jardín. Regla: si a las 3 ves a un niño solo… no llames a nadie.
19. **La llamada de la abuela** — Tu abuela con alzhéimer te llama: "Hay un hombre en mi cocina que dice ser tu padre". Tu padre está a tu lado, dormido en el sofá… ¿o no? Giro: tu padre abre los ojos y dice: "Cuelga". Regla: si a las 3 llama la abuela… créetela.
20. **El GPS** — Tu GPS te dice a las 3: "Gire a la derecha" hacia un camino de tierra que no existe en el mapa. No giras. El GPS repite, cada vez más rápido. Por el retrovisor, unas luces giran por ese camino detrás de ti. Regla: si a las 3 el GPS insiste… no gires.
21. **El grupo de clase** — A las 3 alguien escribe en el grupo de clase: "¿Quién está despierto?". Contestas tú. Te escribe por privado: "Ya lo sé. Te veo". Tu webcam tiene la luz encendida. Regla: si a las 3 preguntan quién está despierto… no contestes.
22. **La vecina de abajo** — La vecina de abajo sube a quejarse: "Deja de arrastrar muebles a las 3". Vives solo y no has movido nada. Esa noche, a las 3, el ruido empieza… en tu techo. Vives en el último piso. Regla: si a las 3 se arrastran muebles… no subas a mirar.
23. **Los golpes en la pared** — Tu hermano y tú os dais las buenas noches con tres golpes en la pared. A las 3 suenan tres golpes. Contestas. Por la mañana: tu hermano dormía en casa de un amigo. Esa noche los golpes vienen de dentro de tu armario. Regla: si a las 3 llaman a la pared… no devuelvas los golpes.
24. **La foto de la puerta** — Tu cámara del timbre graba a alguien de pie en la puerta, mirando al objetivo sin moverse. Desde las 3 hasta las 3:47. A las 3:48 la cámara graba la puerta abierta. Regla: si a las 3 hay alguien en tu timbre… no mires a qué hora se fue.
25. **El silencio** — A las 3 todos los ruidos de la casa paran: la nevera, el reloj, los coches. Tu madre te escribe desde su cuarto: "No respires fuerte. Está escuchando". Regla: si a las 3 todo se calla… cállate tú también.

Cuando quedan menos de 5 historias sin hacer, añade 10 nuevas al banco siguiendo las mismas reglas (situación concreta + pista previa + giro lógico + regla final).
