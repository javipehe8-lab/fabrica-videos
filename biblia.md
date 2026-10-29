# Biblia de la serie: EL SONRIENTE

Serie de terror paranormal en Shorts verticales (1080x1920), animada con stickmans. Cada episodio dura entre 60 y 80 segundos, tiene 14-16 escenas de 2-5 s, narrador masculino (voz `em_alex`) y termina en cliffhanger con "Parte N+1, muy pronto. Síguenme para no perdértela."

## Personajes
- **Leo**: protagonista, hermano mayor. Stickman con camiseta roja y gorra roja (`LEO`). Valiente pero impulsivo.
- **Nora**: hermana de Leo, lista, la que encuentra las soluciones. Camiseta y coleta moradas (`NORA`).
- **El Sonriente**: el enemigo. Stickman negro, alto, contorno lila brillante, ojos blancos y una sonrisa enorme de dientes (`SONRIENTE`, `enemy()` en escenas2). No se le puede matar, solo encerrar. Quien lo mira a los ojos cae dormido y no despierta.
- **Relleno** (sin nombre, sin arco propio): soldados con casco y fusil (`SOLDADO`), el doctor con bata y portapapeles (`DOCTOR`), pacientes (`PACIENTE`).

## Reglas del mundo
- Mirarlo a los ojos = no volver a despertar (salvo giro de guion).
- Las balas lo atraviesan como humo.
- Los espejos le hacen daño: verse a sí mismo lo destruye o lo encierra durante un tiempo.
- La luz del viejo faro de la costa (114 escalones) es la única cárcel conocida.

## Episodios publicados
1. **Parte 1 – "No lo mires a los ojos"**: aparece en la ventana de Leo, apagón, el ejército cierra el barrio, el doctor explica la regla de los ojos, Leo lo había mirado. Ataque nocturno: las balas no le hacen nada. Nora usa un espejo y el Sonriente estalla. Giro: en el espejo sigue sonriendo.
2. **Parte 2 – "La luz no fue suficiente"**: Nora encierra el espejo en una caja con tres candados, la caja golpea y se agrieta. Un libro antiguo dice que solo se le puede encerrar en la luz del faro. Convoy militar, la caja revienta, el Sonriente se lleva a los soldados. Huida por los 114 escalones, palanca atascada, Nora lo mira a los ojos para ganar tiempo, Leo enciende el faro y lo atrapa. Giro: Nora despierta en el hospital… sonriendo (poseída).

3. **Parte 3 – "Dentro de Nora"**: Nora vuelve a casa poseída: mira la pared durante horas y rompe todos los espejos. La radiografía del doctor muestra al Sonriente dentro de ella. Para sacarlo, Leo la mira a los ojos y cae en el mundo del Sonriente (gris, lleno de caras sonrientes flotando). Nora está atrapada en una jaula de luz; el Sonriente aparece gigante. Leo lo hace retroceder con tres destellos de linterna, rompe la jaula y huyen por la única puerta con luz. Despiertan a salvo en el hospital. Giro: esa noche el reflejo del doctor le sonríe (el doctor es el siguiente huésped).

4. **Parte 4 – "La grabación"** (misterio/pista): el doctor, mientras el Sonriente lo consume, se graba un mensaje y se encierra en la sala de rayos X tirando la llave. Leo encuentra una cinta VHS en su puerta ("PARA LEO Y NORA") y la ven en la vieja tele del salón. El doctor revela el origen: el hospital abandonado de Santa Brígida (en inglés, "Saint Brigid"), de donde en 1986 algo salió de la habitación 114. Nueva pista: 114, el mismo número que los escalones del faro. La imagen falla, al doctor se le ponen los ojos rojos y habla sin mover la boca; la tele no se apaga… y llevaba todo el rato desenchufada. Giro: una voz que no es la del doctor susurra "Os estoy esperando" y la cara del Sonriente llena la pantalla. Diálogos: DOCTOR "Sé de dónde salió", SONRIENTE "Os estoy esperando". Piezas nuevas en `escenas4.py`: tele CRT con imagen pegada (`tele_draw`, `pegar`, `feed_doctor`, `feed_estatico`), símbolo de radiación, fachada de Santa Brígida, puerta 114.

5. **Parte 5 – "Santa Brígida"** (exploración/persecución): Leo y Nora se cuelan de noche en el hospital abandonado con dos linternas. Pasillos con camillas oxidadas y sillas de ruedas, todas giradas hacia la misma puerta; una silla de ruedas rueda sola hacia ellos y huyen mientras algo sonríe en la oscuridad. En la tercera planta, la puerta 114 se abre sola: las paredes están cubiertas de dibujos infantiles del Sonriente, todos fechados en 1986… y el último es nuevo: Leo y Nora dibujados con ceras, con el Sonriente detrás. Pasos en el pasillo; se esconden bajo una cama y apagan las linternas; una luz barre el suelo buscándolos. Giro: no es el Sonriente, es una anciana (moño gris, bastón, linterna): la abuela Carmen. Diálogos: NORA "Leo… somos nosotros", CARMEN "Llevo cuarenta años esperándoos". Nueva figura `CARMEN` en `motor.py` (extras "bun" y "cane"). Piezas nuevas en `escenas5.py`: luz de linterna que oscurece la escena (`iluminar`, `linterna_mano`), pasillo de hospital de lado (`pasillo_h`), silla de ruedas, camilla, cama de hospital, dibujos con ceras (`stick_cera`, `dibujo`, `pared_dibujos`), sonrisa en la oscuridad (`ojos_oscuridad`).
   - Elección Parte 5 (para el arranque de la Parte 6): "¿Confían en la anciana?" A) SE QUEDAN CON ELLA (Carmen les cuenta su historia allí mismo, en la 114) · B) HUYEN DE ELLA (escapan del hospital, pero Carmen los alcanza fuera / en el coche y les demuestra que sobrevivió al Sonriente). Las dos llevan a la Parte 6 "La abuela Carmen".

## Arco de la temporada 1 (Partes 4-10) — SEGUIR ESTE PLAN
Objetivo: que la historia avance y descubra cosas nuevas. Historia SENCILLA: un único villano (el Sonriente); el coronel se ha eliminado del plan. NO repetir "el Sonriente se mete en otro personaje". La posesión ya se usó (Nora y doctor): no vuelve a usarse en lo que queda de temporada.
4. **La grabación**: el doctor, antes de perder el control, se graba un mensaje para Leo y Nora y se encierra a sí mismo en la sala de rayos X. En la grabación revela de dónde salió el Sonriente: un antiguo hospital abandonado, Santa Brígida, habitación 114. Giro: la grabación termina con una voz que no es la del doctor diciendo "os estoy esperando".
5. **Santa Brígida**: Leo y Nora entran en el hospital abandonado (pasillos, camillas, linterna). En la habitación 114 encuentran dibujos infantiles del Sonriente de 1986. Giro: alguien ya estaba allí, una anciana con linterna.
6. **La abuela Carmen** (nueva aliada fija, stickman con moño gris y bastón): sobrevivió al Sonriente de niña. Explica que se alimenta del miedo y que tiene un nombre verdadero; quien lo pronuncia dentro de la luz lo destruye. Giro: el doctor ha desaparecido de la sala de rayos X.
7. **El nombre** (misterio/pista): Carmen les enseña dónde buscar el nombre verdadero (el archivo del hospital, un expediente de 1986 con la ficha de un niño). Consiguen media pista: la primera letra o un apodo. El Sonriente se da cuenta de que lo están buscando. Giro: todos los dibujos de la 114 ahora tienen la cara tachada… menos el de Leo y Nora.
8. **La ciudad dormida** (persecución): el Sonriente se venga y duerme a toda la ciudad; calles llenas de gente dormida de pie. Solo Leo y Nora siguen despiertos (ya sobrevivieron a su mirada). Encuentran la otra mitad del nombre en un lugar inesperado (un columpio, una placa del hospital). Giro: Carmen no aparece en el punto de encuentro.
9. **El cebo** (trampa/rescate): el Sonriente se ha llevado a Carmen al faro como cebo. Leo y Nora suben los 114 escalones sabiendo que es una trampa. Giro: arriba, el Sonriente los espera con la cara de Carmen.
10. **FINAL DE TEMPORADA**: en el faro, dentro de la luz, Nora y Leo pronuncian su nombre verdadero. El Sonriente se convierte en un niño perdido de 1986 y desaparece en paz. La ciudad despierta. Giro de temporada 2: en otra ventana, en otra ciudad, algo nuevo empieza a sonreír.

## Reglas de variedad (siempre)
- Cada episodio debe tener al menos UNA cosa nueva: un lugar, un personaje, una pista o una regla del monstruo.
- Alterna el tipo de tensión: persecución, misterio/pista, trampa, rescate, traición. Nunca dos episodios seguidos del mismo tipo.
- El giro final no puede ser siempre una posesión ni una sonrisa en un espejo. Usa revelaciones, desapariciones, personajes que no son quien parecen y lugares nuevos.
- Un personaje de relleno puede tener una escena con frase, pero los protagonistas siguen siendo Leo y Nora.

## Para escribir el siguiente episodio
- Continúa justo donde acabó el anterior. Un problema, una escalada y un giro final.
- Frases cortas, de 1-2 líneas por escena. Primera frase con gancho fuerte.
- Reutiliza escenarios y piezas existentes (cuarto, hospital, calle, faro, sala de la lámpara, carretera, acantilado) y crea solo las escenas imprescindibles.
- Mantén la estética: fondos de degradado oscuros, tinte rojo y glitch en los sustos, subtítulos grandes con la palabra activa en amarillo.
- Después de escribir el episodio, añade aquí su resumen en "Episodios publicados".
