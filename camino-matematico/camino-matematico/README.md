# Camino Matemático – Academia Esparta

Esta carpeta contiene una actividad web para que alumnos de 1.º de Primaria practiquen sumas y restas sin llevadas. El juego reproduce un **camino** de diez pasos en el que el alumno debe resolver operaciones sencillas. Al tocar una respuesta, recibe **feedback inmediato** y solo avanza si acierta. Cuando completa el último paso, aparece una pantalla de “¡Meta conseguida!” con un refuerzo positivo. El diseño está pensado para usarse en iPad y otros dispositivos táctiles: botones grandes, tipografía legible y contraste alto siguiendo las recomendaciones de accesibilidad (áreas táctiles de al menos 44 × 44 px o 48 dp【638008952038423†L188-L239】).

## Estructura de la carpeta

```
camino-matematico/
│  index.html      → página principal de la actividad
│  styles.css      → estilos CSS (personaliza `--esparta-green` aquí)
│  app.js          → lógica en JavaScript con las preguntas y el feedback
│  README.md       → este documento
└── assets/        → carpeta opcional para imágenes o logotipos
```

### Archivos clave

- **`index.html`**: contiene la estructura del juego, cabecera fija, contenedor de preguntas y botones de control. No necesita ningún servidor; basta con abrirlo en un navegador.
- **`styles.css`**: define los colores y estilos. El color corporativo se controla mediante la variable CSS `--esparta-green`. Modifica ese valor si conoces el color exacto de Academia Esparta.
- **`app.js`**: implementa el conjunto de preguntas en un array, gestiona el avance entre pasos, muestra feedback inmediato y reproduce un pequeño tono cuando el sonido está activado. La lógica está comentada para facilitar modificaciones.
- **`assets/`**: puedes añadir aquí el logotipo de tu academia u otras imágenes. En esta versión no hay imágenes predeterminadas para mantener el paquete ligero.

## Cómo publicar en GitHub Pages

1. **Ubica la carpeta en tu repositorio.** Copia la carpeta `camino-matematico` completa dentro de tu repositorio de GitHub. Dependiendo de cómo tengas configurada la publicación de GitHub Pages puedes:
   - **Publicar desde la raíz (`/`).** Coloca `camino-matematico` en la raíz del repositorio. Luego, en _Settings → Pages_, selecciona la rama principal (`main` o `master`) y la carpeta raíz para GitHub Pages.
   - **Publicar desde `/docs`.** Si tu proyecto usa la carpeta `docs` para GitHub Pages, coloca `camino-matematico` dentro de `docs` y elige esa carpeta como fuente.

2. **Haz _commit_ y _push_.** Sube los cambios a GitHub. Asegúrate de que los archivos `index.html`, `styles.css` y `app.js` estén incluidos.

3. **Activa GitHub Pages.** En la configuración del repositorio (_Settings → Pages_) selecciona la rama y la carpeta donde se encuentra la actividad. Guarda los cambios. GitHub generará el sitio automáticamente en unos segundos.

4. **Comprueba la URL final.** Si tu dominio es `www.academiaesparta.es` configurado como _Custom Domain_ en GitHub Pages, la actividad estará disponible en:

```
https://www.academiaesparta.es/camino-matematico/
```

Puedes probarlo localmente abriendo `index.html` en tu navegador; el comportamiento será el mismo que en GitHub Pages.

## Personalización y ampliaciones

- **Cambiar o añadir preguntas.** El array `questions` en `app.js` define cada paso. Cada objeto incluye el estado actual (`state`), el enunciado (`question`), las dos opciones (`options`), la posición de la respuesta correcta (`correctIndex`) y el valor del nuevo estado (`newState`). Puedes ajustar, añadir o eliminar pasos modificando este array.
- **Colores y tipografía.** Para adaptar el estilo a tu marca, cambia la variable `--esparta-green` en `styles.css`. El resto de colores (aciertos en verde y errores en rojo) también se definen ahí.
- **Sonidos.** La actividad reproduce un tono agudo en los aciertos y grave en los errores mediante la API Web Audio. El botón con el icono de altavoz (`🔈/🔇`) permite activar o desactivar el sonido. Si prefieres silenciar por defecto, cambia la variable `soundEnabled` a `false` al principio de `app.js`.
- **Modo hasta 10** (opcional). Si quieres reducir el rango máximo de resultados (por ejemplo, para trabajar solo operaciones que no superen 10), modifica la secuencia de preguntas acorde a tus necesidades. El juego no utiliza un backend ni bases de datos; todo está en el lado del cliente.

¡Disfruta del juego y adapta este recurso a tus alumnos según lo necesites!