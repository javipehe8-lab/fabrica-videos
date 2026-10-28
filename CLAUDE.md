# Fábrica de vídeos – instrucciones de trabajo

Repositorio público con el motor de animación stickman, la serie "El Sonriente" y los vídeos terminados (`videos/`), que Metricool descarga por URL pública.

## Estructura
- `stick/motor.py`: lienzo, cámara, figuras (LEO, NORA, SOLDADO, DOCTOR, PACIENTE, SONRIENTE), poses, efectos y subtítulos.
- `stick/guionN.py` + `stick/escenasN.py`: episodio N (escenas = funciones `f(t, D, fi) -> (imagen, efectos)`, `ESCENA_FN`, `PAUSA`). Los episodios nuevos importan las piezas de `escenas.py` / `escenas2.py`.
- `stick/sonido.py`: música y efectos sincronizados por nombre de escena. Añade aquí los efectos de las escenas nuevas (bloque por episodio, con `os.environ.get("EP")` si un nombre se repite).
- `biblia.md`: personajes, reglas y resumen de cada episodio. Léela antes de escribir y actualízala después.
- `publicaciones.json`: registro de lo publicado (título, fecha, URL del vídeo).

## Gancho inicial (OBLIGATORIO desde la Parte 4)
Los datos de la Parte 1: solo el 44 % se quedó viendo (el 56 % deslizó). El arranque era lento. Cada guion (español e inglés) debe definir
`GANCHO = ("<escena más impactante del episodio>", <fracción 0-1 del momento más fuerte>, "LÍNEA 1\nLÍNEA 2")`: 1,2 s de impacto antes de la historia, con texto de máximo 2 líneas cortas (≤ 14 caracteres por línea) que plantee una pregunta o una amenaza. Ej.: `("gigante", 0.8, "SU HERMANA\nYA NO ERA ELLA")`. En `guionN_en.py` el texto va en inglés. Además, la primera frase narrada debe ser la más fuerte del episodio.

## Diálogos (MUY puntuales)
- Como máximo 1-2 frases de diálogo por episodio, de 2-6 palabras, solo en el pico de tensión (un grito, una amenaza, una pista). El vídeo tiene que seguir siendo frenético: nunca una conversación.
- Se escriben dentro del texto de la escena con el nombre entre corchetes: `"Leo la buscó en el bosque. [SONRIENTE] Leo… te puedo ver."`. Personajes con voz propia (distinta del narrador): LEO, NORA, DOCTOR, CARMEN, CORONEL, SOLDADO, SONRIENTE; cualquier otro nombre usa una voz genérica. En `guionN_en.py` van los mismos marcadores.
- Los subtítulos de cada personaje salen en su color (Nora lila, Leo rojo, Sonriente rojo intenso, resto azul).

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
