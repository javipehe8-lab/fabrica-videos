# Subir a YouTube desde el Chrome de Javi (sustituye a Metricool desde el 14/11/2026)

Metricool gratis solo deja 20 publicaciones al mes, y se agotaron. Ahora los vídeos se suben **directamente a YouTube Studio** con Claude en Chrome (el Chrome de Javi, con la sesión de YouTube abierta en el canal "Historias de las 3AM"), y se programan con el programador del propio YouTube.

- Las tareas que **fabrican** vídeos (Turno de noche, Si oyes esto a las 3AM) ya NO usan Metricool: al terminar, añaden el vídeo a `cola_youtube.json` con `"estado": "pendiente"` (serie, parte, video, titulo, descripcion) y hacen commit y push.
- La tarea de **subida** (cada día a las 17:47; necesita el ordenador de Javi encendido con la app de Claude y Chrome abiertos) sube todo lo pendiente. Si un día el ordenador está apagado, no pasa nada: al día siguiente sube lo atrasado y lo reparte en los siguientes días libres.

## Cómo asignar fecha a cada vídeo pendiente
- Hora fija por serie: `cola_youtube.json["horas"]` (3am → 19:00, turno → 23:00, hora de España).
- Cada serie publica como mucho un vídeo al día. Para cada serie, en orden de parte, el primer día libre a partir de hoy (si la hora de hoy ya pasó o falta menos de 1 hora, desde mañana), sin repetir un día que ya tenga un vídeo "programado" de esa serie en la cola.

## Procedimiento en Chrome (probado el 14/11/2026)
Carga las herramientas de Claude en Chrome en UNA llamada a ToolSearch (tabs_context_mcp, tabs_create_mcp, tabs_close_mcp, navigate, computer, find, javascript_tool, browser_batch). Luego:
1. `tabs_context_mcp` (createIfEmpty) → abre una pestaña nueva → `https://studio.youtube.com`. Comprueba en una captura que el canal es "Historias de las 3AM". Si pide iniciar sesión, PARA y avisa a Javi (nunca escribas contraseñas).
2. Para cada vídeo pendiente:
   a. Con `javascript_tool`, descarga el vídeo y mételo en el diálogo de subida (no hace falta tenerlo en el ordenador):
      ```js
      const r = await fetch('https://raw.githubusercontent.com/javipehe8-lab/fabrica-videos/main/<video>');
      window.__v = await r.blob();
      document.querySelector('#upload-icon').click();
      await new Promise(r => setTimeout(r, 2500));
      const inp = document.querySelector('input[type=file]');
      const dt = new DataTransfer(); dt.items.add(new File([window.__v], '<nombre>.mp4', {type: 'video/mp4'}));
      inp.files = dt.files; inp.dispatchEvent(new Event('change', {bubbles: true}));
      'ok ' + window.__v.size
      ```
   b. Título: clic en el cuadro del título, `ctrl+a` y escribe el título. Descripción: clic en el cuadro de descripción y escríbela. Clic en una zona vacía para cerrar las sugerencias de hashtags.
   c. `find` "radio 'No, no está creado para niños'" → `scroll_to` + clic. OBLIGATORIO.
   d. "Siguiente" tres veces (esperando ~2 s entre clics) hasta "Visibilidad".
   e. Abre "Programar". Clic en la fecha → elige el día en el calendario. Clic en la hora → `ctrl+a` → escribe "HH:MM" → Enter. **Comprueba con zoom que fecha y hora son las correctas** antes de seguir (a veces la hora se queda en 0:00: repítelo).
   f. Pulsa "Programar". En el diálogo "Se ha programado la publicación" anota el enlace (youtube.com/shorts/…) y ciérralo.
   g. En `cola_youtube.json` pon ese vídeo a `"estado": "programado"`, con `"fecha"` y `"url"`.
3. Si algo no responde tras 2-3 intentos, no insistas: deja el vídeo como pendiente y sigue con el siguiente. Cierra las pestañas que abriste.
4. Haz commit y push de `cola_youtube.json` (desde la nube) y avisa a Javi con la lista de lo programado (título, fecha y enlace).

Coordenadas orientativas del diálogo en la ventana de Javi (1568x653): "Siguiente"/"Programar" ≈ (1118, 585); apartado "Programar" ≈ (833, 477); fecha ≈ (517, 405); hora ≈ (642, 405). Si la ventana cambia de tamaño, guíate por una captura.

El primer comentario NO se puede programar desde Studio (solo se puede comentar tras publicar): de momento se omite.
