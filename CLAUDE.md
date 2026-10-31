# Fábrica de vídeos – instrucciones de trabajo

Repositorio público con el motor de animación stickman, la serie "El Sonriente" y los vídeos terminados (`videos/`), que Metricool descarga por URL pública.

## Estructura
- `stick/motor.py`: lienzo, cámara, figuras (LEO, NORA, SOLDADO, DOCTOR, PACIENTE, SONRIENTE), poses, efectos y subtítulos.
- `stick/guionN.py` + `stick/escenasN.py`: episodio N (escenas = funciones `f(t, D, fi) -> (imagen, efectos)`, `ESCENA_FN`, `PAUSA`). Los episodios nuevos importan las piezas de `escenas.py` / `escenas2.py`.
- `stick/sonido.py`: música y efectos sincronizados por nombre de escena. Añade aquí los efectos de las escenas nuevas (bloque por episodio, con `os.environ.get("EP")` si un nombre se repite).
- `biblia.md`: personajes, reglas y resumen de cada episodio. Léela antes de escribir y actualízala después.
- `publicaciones.json`: registro de lo publicado (título, fecha, URL del vídeo).
- `tres_am.md`: SEGUNDA SERIE "Si oyes esto a las 3AM" (historias autoconclusivas, 19:00). Tiene sus propias reglas y su banco de historias; las reglas de GANCHO, ELECCION y biblia de este archivo son solo para El Sonriente.

## Gancho inicial (OBLIGATORIO desde la Parte 4)
Los datos de la Parte 1: solo el 44 % se quedó viendo (el 56 % deslizó). El arranque era lento. Cada guion (español e inglés) debe definir
`GANCHO = ("<escena más impactante del episodio>", <fracción 0-1 del momento más fuerte>, "LÍNEA 1\nLÍNEA 2")`: 1,2 s de impacto antes de la historia, con texto de máximo 2 líneas cortas (≤ 14 caracteres por línea) que plantee una pregunta o una amenaza. Ej.: `("gigante", 0.8, "SU HERMANA\nYA NO ERA ELLA")`. En `guionN_en.py` el texto va en inglés. Además, la primera frase narrada debe ser la más fuerte del episodio.

## Cada episodio debe entenderse SOLO (datos del 29/10)
La Parte 1 tiene ~1.000 visitas; las Partes 2-4, 20-30 cada una. YouTube enseña cada Short a gente que NO ha visto las partes anteriores: si no entiende de qué va, desliza.
- La primera frase narrada (tras el GANCHO) presenta la premisa en una línea, sin depender de lo anterior. Ej.: "Un monstruo que sonríe duerme para siempre a quien lo mira a los ojos. Leo y Nora lo han visto."
- No empieces con "Después de lo que pasó…" ni con referencias que exijan haber visto la parte anterior.
- Título: gancho autónomo primero; "(Parte N)" siempre al final.

## Duración: 35-45 s (OBLIGATORIO, datos del 31/10)
Partes 3-5: la gente se queda 39-42 s de media, dure el vídeo 1:10 o 1:18; solo vieron ~55 % de cada vídeo y YouTube dejó de recomendarlos. Por eso:
- 8-9 escenas como máximo (incluida "final"), 2-5 s cada una; vídeo total de 35-45 s (con gancho y tarjeta). Comprueba la duración del MP4 con ffprobe: si pasa de 48 s, recorta texto o escenas y vuelve a renderizar.
- Estructura: gancho → premisa en una línea → un problema → un susto → un giro → tarjeta A/B. Una sola idea por episodio; si un punto del arco no cabe, se reparte en dos episodios.
- Frases de narración aún más cortas (máx. ~12 palabras por escena).

## Diálogos (MUY puntuales)
- Como máximo 1-2 frases de diálogo por episodio, de 2-6 palabras, solo en el pico de tensión (un grito, una amenaza, una pista). El vídeo tiene que seguir siendo frenético: nunca una conversación.
- Se escriben dentro del texto de la escena con el nombre entre corchetes: `"Leo la buscó en el bosque. [SONRIENTE] Leo… te puedo ver."`. Personajes con voz propia (distinta del narrador): LEO, NORA, DOCTOR, CARMEN, CORONEL, SOLDADO, SONRIENTE; cualquier otro nombre usa una voz genérica. En `guionN_en.py` van los mismos marcadores.
- Los subtítulos de cada personaje salen en su color (Nora lila, Leo rojo, Sonriente rojo intenso, resto azul) con una etiqueta encima con su nombre (automático).

## Final con elección (desde la Parte 5)
- Cada guion termina con una tarjeta para votar: define `ELECCION = ("PREGUNTA CORTA\nEN 2 LÍNEAS", "OPCIÓN A", "OPCIÓN B")` (opciones de 2-4 palabras; en `guionN_en.py`, en inglés). La escena "final" se sustituye sola por la tarjeta; su texto narrado debe ser: "¿<pregunta>? ¿A o B? Coméntalo. Mañana lo verás." (en inglés: "…? A or B? Tell me in the comments. Find out tomorrow.").
- Las dos opciones tienen que ser dos caminos creíbles hacia el siguiente punto del "Arco de la temporada" (no deben romper el arco).
- Al empezar el episodio siguiente: si el anterior tenía ELECCION, elige la opción AL AZAR con `python3 -c "import random; print(random.choice('AB'))"` (da igual lo que vote la gente), apúntala en biblia.md ("Elección Parte N: salió X") y haz que el episodio arranque siguiendo esa opción. NUNCA digas en el vídeo ni en la descripción que "ganó la mayoría".
- Primer comentario (firstCommentText) de un episodio con elección: "¿A o B? 👇 Mañana lo descubres."

## Calidad visual
- `CALIDAD=hd` (por defecto) activa el contorno de los personajes, sombras de contacto, brillo en la cabeza, contraste y bloom. No lo desactives.

## Hacer un episodio
1. `bash setup.sh` (descarga Piper y Kokoro; unos 400 MB, una vez por sesión).
2. Escribe `stick/guionN.py` y `stick/escenasN.py`, y añade los efectos en `sonido.py`.
3. `cd stick && EP=N python3.13 voz.py vozN && EP=N AT=0.7 python3.13 render.py vozN outN --preview` → MIRA `outN/preview.png` y corrige encuadres, personajes tapados por subtítulos (zona y > 1300) y elementos fuera de cuadro.
4. `bash hacer_episodio.sh N` → `videos/El_Sonriente_ParteN.mp4` (tiene que pesar menos de 95 MB).
5. Comprueba 4-6 fotogramas con ffmpeg antes de publicar.

## Publicar (Metricool)
- Marca: blogId `7684641`, zona horaria `Europe/Madrid`. Red: YouTube (Short).
- URL del vídeo: `https://raw.githubusercontent.com/javipehe8-lab/fabrica-videos/main/videos/El_Sonriente_ParteN.mp4` (haz commit y push antes).
- SIEMPRE: `type: "short"`, `privacy: "public"`, `madeForKids: false`, `category: "FILM_ANIMATION"`, título con " #shorts", descripción con hashtags y `firstCommentText` con una pregunta para los comentarios.
- Hora por defecto: 23:00 Europe/Madrid del mismo día.
- Añade la publicación a `publicaciones.json` y haz commit.

## Versión en inglés ("The Grinner")
- Misma animación, texto traducido: `stick/guionN_en.py` con los MISMOS nombres de escena que `guionN.py`. Serie: "THE GRINNER", el Sonriente = "the Grinner". Traduce de forma natural (inglés de EE. UU.), no literal; mantén las frases cortas.
- Los textos fijos de pantalla se traducen con `tr()` de `motor.py`. Si una escena nueva dibuja texto, envuélvelo en `tr("...")` y añade la traducción al diccionario `EN`.
- `bash hacer_episodio.sh N en` → `videos/en/The_Grinner_PartN.mp4` (voz `am_onyx`, inglés de EE. UU.).
- Canal: "The Grinner Files". NO se publica por Metricool (el plan gratuito solo tiene una marca): Javi lo sube a mano cada día desde la app de YouTube, programado a las 00:30 Europe/Madrid. Prepárale el vídeo y los textos en inglés: título con " #shorts", descripción + hashtags (#horror #scarystories #creepy #animation #stickman #shorts #thegrinner), primer comentario, y recuérdale: Short, público, "No, no es para niños".
- URL: `https://raw.githubusercontent.com/javipehe8-lab/fabrica-videos/main/videos/en/The_Grinner_PartN.mp4`.

## Subir a GitHub (vídeos grandes)
- Haz un commit por vídeo (no metas dos MP4 en el mismo push) y empuja con `git -c http.postBuffer=524288000 push origin HEAD:main`. Si falla con "remote end hung up", repite una vez y comprueba con `git fetch origin main && git log -1 origin/main`.
