# Fábrica de vídeos – instrucciones de trabajo

Repositorio público con el motor de animación stickman, la serie "El Sonriente" y los vídeos terminados (`videos/`), que Metricool descarga por URL pública.

## Estructura
- `stick/motor.py`: lienzo, cámara, figuras (LEO, NORA, SOLDADO, DOCTOR, PACIENTE, SONRIENTE), poses, efectos y subtítulos.
- `stick/guionN.py` + `stick/escenasN.py`: episodio N (escenas = funciones `f(t, D, fi) -> (imagen, efectos)`, `ESCENA_FN`, `PAUSA`). Los episodios nuevos importan las piezas de `escenas.py` / `escenas2.py`.
- `stick/sonido.py`: música y efectos sincronizados por nombre de escena. Añade aquí los efectos de las escenas nuevas (bloque por episodio, con `os.environ.get("EP")` si un nombre se repite).
- `biblia.md`: personajes, reglas y resumen de cada episodio. Léela antes de escribir y actualízala después.
- `publicaciones.json`: registro de lo publicado (título, fecha, URL del vídeo).

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
- Metricool: marca del canal inglés (ver `publicaciones_en.json` → `blogId`), a las 00:30 Europe/Madrid del día siguiente (18:30-19:30 en la costa este de EE. UU.). Mismos ajustes: short, public, madeForKids false, FILM_ANIMATION, título en inglés con " #shorts", hashtags en inglés (#horror #scarystories #creepy #animation #stickman #shorts #thegrinner) y primer comentario en inglés.
- URL: `https://raw.githubusercontent.com/javipehe8-lab/fabrica-videos/main/videos/en/The_Grinner_PartN.mp4`.
