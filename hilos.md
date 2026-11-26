# Serie "HILOS MALDITOS" (prueba desde el 25/11/2026)

Historias de terror contadas como un post de un **foro propio del canal** (ficción: "h/relatos", logo HM). NO imitamos Reddit ni ninguna web real, NO usamos posts ni usuarios reales y NO usamos gameplay ni vídeos de otros: el fondo en bucle lo hace nuestro motor 3D. Así no hay reclamaciones de copyright ni "contenido reutilizado".

## Qué tiene que tener cada historia (OBLIGATORIO)
- Retorcida y **creíble**: algo que podría haber pasado de verdad o que suena a leyenda de pueblo/familia. Nada de monstruos genéricos. Ej.: "Mi abuela desapareció tres días. La que volvió me reconoce."
- Primera persona, tono de alguien que lo cuenta en internet, frases cortas (máx. ~14 palabras).
- **Gancho en el primer segundo**: el fotograma 0 ya enseña la imagen más inquietante (en el 1: la abuela en camisón en medio de la carretera) y la tarjeta del post está encima desde el principio. El título del post es la frase más fuerte.
- Detalles concretos que dan verosimilitud (fechas, kilómetros, objetos) y 2-3 pistas raras antes del giro.
- Termina con un **EDIT:** que lo empeora todo (tarjeta_edit) y "SÍGUEME PARA MÁS HILOS".
- 1-2 frases de diálogo como mucho (VOCES/EDGE_VOCES/MONSTRUOS/RADIOS).

## Formato técnico
- `stick/guionhiloK.py` (TITULO "HILOS MALDITOS", ESTILO "ps2_3d", SUBS_Y = 1060, SIN_SUBS = ("titulo",), POST = dict(...), EDIT, EDGE_NARRADOR según quien narra) + `stick/escenashiloK.py` con las piezas de `stick/hilos.py`.
- **Fondo distinto en cada vídeo** (OBLIGATORIO): `hilos.FONDOS` = carretera (de noche entre pinos), tunel (autovía con luces de sodio), pasillo (hotel infinito, números de puerta que suben), escalera (hueco de escalera visto desde arriba, girando y bajando). Ponlo en el guion como `FONDO = "<nombre>"` y NUNCA repitas el del episodio anterior; ve rotando y, cuando se hayan usado todos, crea uno nuevo en hilos.py (metro vacío, ascensor que no para, bosque con linterna, aparcamiento subterráneo…). Movimiento constante y simétrico, sin cortes: tiene que ser hipnótico. Llama al fondo con el tiempo GLOBAL (fi / FPS) para que el bucle no salte entre escenas.
- Sonidos: `sting()` y `boom()` largos eligen solos una variante distinta en cada vídeo (violines, sonido al revés, metal, glitch, susurro, coro, portazo, caída, campana, golpe metálico, cinta que se para). Además usa directamente las variantes que peguen con la historia (p. ej. `campana` en una historia de pueblo, `susurro` cuando alguien habla cerca).
- Duración 60-80 s, ~10 escenas. `bash hacer_episodio.sh hiloK` → `videos/hilos/Hilos_Malditos_K.mp4`.
- Título de YouTube: "<gancho corto> 😨 #shorts". Hashtags: #hilosmalditos #terror #historiasdeterror #historiasreales #miedo #creepy #shorts.

## Banco de ideas
1. [HECHA] La abuela que volvió del pinar.
2. Mi padre lleva 20 años llamando a casa a las 3:07 aunque vive con nosotros. Hoy no ha llamado.
3. Compramos una casa barata. En el desván hay fotos nuestras… de antes de que la viéramos.
4. Mi hermano gemelo murió al nacer. Mi madre sigue poniendo dos cepillos de dientes. Uno siempre está mojado.
5. El vigilabebés capta otra casa. Hoy, en esa casa, alguien ha dicho el nombre de mi hija.
6. En el pueblo de mi madre nadie sale el día de difuntos. Este año yo sí salí.
7. Mi novio habla dormido en un idioma que no existe. Mi abuela lo oyó una noche, lo entendió… y se fue de casa.
8. Hice de canguro. Me pidieron no abrir la habitación del fondo "porque duerme el otro niño". Solo tienen uno.
9. Mi madre me reconoce por teléfono, pero no cuando me ve. Dice que la que va a verla "lleva mi cara".
10. En el grupo de WhatsApp de la familia hay un número que nadie añadió. Manda fotos de nuestra casa. Desde dentro.
11. Llevo una semana despertándome con tierra bajo las uñas. Hoy he encontrado el agujero en el jardín. Tiene mi tamaño.

## Emitidos
- 1 · 26/11 21:00 · fondo carretera · «Mi abuela desapareció 3 días… y volvió DIFERENTE» (youtube.com/shorts/mSFDuuLoDZc)
