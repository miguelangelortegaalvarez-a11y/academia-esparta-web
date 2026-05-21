// 1. CONFIGURACIÓN DE LOS NIVELES
// Asegúrate de que los nombres de las imágenes coincidan con tus archivos en assets/items/
const niveles = [
    { img: "avion.png", correcta: "A", opciones: ["A", "E"] },
    { img: "elefante.png", correcta: "E", opciones: ["O", "E"] },
    { img: "isla.png", correcta: "I", opciones: ["I", "A"] },
    { img: "ojo.png", correcta: "O", opciones: ["U", "O"] },
    { img: "uva.png", correcta: "U", opciones: ["E", "U"] }
];

let indiceActual = 0;
let aciertos = 0;

// 2. ELEMENTOS DEL DOM (HTML)
const screenHome = document.getElementById('screen-home');
const screenGame = document.getElementById('screen-game');
const screenFinal = document.getElementById('screen-final');

const startBtn = document.getElementById('start-btn');
const retryBtn = document.getElementById('retry-btn');

const questionImg = document.getElementById('question-img');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');

const btn0 = document.getElementById('btn-0');
const btn1 = document.getElementById('btn-1');
const text0 = document.getElementById('text-0');
const text1 = document.getElementById('text-1');

// 3. LÓGICA DE INICIO
startBtn.addEventListener('click', () => {
    screenHome.classList.remove('is-active');
    screenGame.classList.add('is-active');
    cargarNivel();
});

// 4. CARGAR UN NIVEL
function cargarNivel() {
    const nivel = niveles[indiceActual];
    
    // Actualizar imagen
    questionImg.src = `./assets/items/${nivel.img}`;
    
    // Actualizar progreso
    const porcentaje = ((indiceActual + 1) / niveles.length) * 100;
    progressFill.style.width = `${porcentaje}%`;
    progressText.innerText = `${indiceActual + 1}/${niveles.length}`;

    // Cargar letras en los botones
    text0.innerText = nivel.opciones[0];
    text1.innerText = nivel.opciones[1];

    // Resetear colores de botones
    btn0.className = 'answer-btn';
    btn1.className = 'answer-btn';
    btn0.disabled = false;
    btn1.disabled = false;

    // Configurar clicks
    btn0.onclick = () => verificarRespuesta(nivel.opciones[0], btn0);
    btn1.onclick = () => verificarRespuesta(nivel.opciones[1], btn1);
}

// 5. VERIFICAR RESPUESTA
function verificarRespuesta(elegida, boton) {
    const correcta = niveles[indiceActual].correcta;
    
    // Bloquear botones para evitar doble click
    btn0.disabled = true;
    btn1.disabled = true;

    if (elegida === correcta) {
        boton.classList.add('correct');
        aciertos++;
        setTimeout(pasarSiguiente, 800);
    } else {
        boton.classList.add('wrong');
        // Si falla, le damos un segundo para ver el error y repetimos el nivel
        setTimeout(cargarNivel, 1000);
    }
}

// 6. PASAR DE NIVEL O FINALIZAR
function pasarSiguiente() {
    indiceActual++;
    
    if (indiceActual < niveles.length) {
        cargarNivel();
    } else {
        mostrarFinal();
    }
}

function mostrarFinal() {
    screenGame.classList.remove('is-active');
    screenFinal.classList.add('is-active');
    document.getElementById('final-correct').innerText = aciertos;
}

// 7. REINICIAR
retryBtn.addEventListener('click', () => {
    indiceActual = 0;
    aciertos = 0;
    screenFinal.classList.remove('is-active');
    screenHome.classList.add('is-active');
});
