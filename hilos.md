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
- Fondos en bucle de `hilos.py`: `carretera()` (conducir de noche entre pinos). Para variar, añade otros fondos (escalera sin fin, pasillo, metro…) en hilos.py.
- Duración 60-80 s, ~10 escenas. `bash hacer_episodio.sh hiloK` → `videos/hilos/Hilos_Malditos_K.mp4`.
- Título de YouTube: "<gancho corto> 😨 #shorts". Hashtags: #hilosmalditos #terror #historiasdeterror #historiasreales #miedo #creepy #shorts.

## Banco de ideas
1. [HECHA] La abuela que volvió del pinar.
2. Mi padre lleva 20 años llamando a casa a las 3:07 aunque vive con nosotros. Hoy no ha llamado.
3. Compramos una casa barata. En el desván hay fotos nuestras… de antes de que la viéramos.
4. Mi hermano gemelo murió al nacer. Mi madre sigue poniendo dos cepillos de dientes. Uno siempre está mojado.
5. El vigilabebés capta otra casa. Hoy, en esa casa, alguien ha dicho el nombre de mi hija.
6. En el pueblo de mi madre nadie sale el día de difuntos. Este año yo sí salí.

## Emitidos
