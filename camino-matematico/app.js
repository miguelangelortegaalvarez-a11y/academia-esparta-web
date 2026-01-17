/*
  Lógica de la actividad "Camino Matemático".

  Este script define un conjunto de pasos (preguntas) en un array para que
  sea sencillo modificar las operaciones sin alterar el código. Cada paso
  contiene el estado actual, el enunciado de la operación, un array de
  opciones, el índice de la respuesta correcta y el nuevo estado al acertar.

  El flujo básico es:
   - Mostrar progreso, estado y pregunta del paso actual.
   - Cuando el alumno toca una opción se valida si es correcta.
   - Si es correcta, se muestra feedback positivo y se avanza al siguiente paso
     tras una breve pausa; si es incorrecta, se muestra feedback negativo y
     se permite reintentar.
   - Al completar el último paso se muestra una pantalla final de meta.

  También se incluye un simple generador de tonos mediante la API Web Audio
  para reproducir sonidos de acierto/error si el sonido está activado.
*/

// Definición de preguntas para el camino
const questions = [
  {
    state: 'Empiezas en 5',
    question: '5 + 3 = ?',
    options: [8, 9],
    correctIndex: 0,
    newState: 8,
  },
  {
    state: 'Estás en 8',
    question: '8 − 2 = ?',
    options: [6, 5],
    correctIndex: 0,
    newState: 6,
  },
  {
    state: 'Estás en 6',
    question: '6 + 4 = ?',
    options: [10, 9],
    correctIndex: 0,
    newState: 10,
  },
  {
    state: 'Estás en 10',
    question: '10 − 3 = ?',
    options: [7, 6],
    correctIndex: 0,
    newState: 7,
  },
  {
    state: 'Estás en 7',
    question: '7 + 5 = ?',
    options: [12, 13],
    correctIndex: 0,
    newState: 12,
  },
  {
    state: 'Estás en 12',
    question: '12 − 4 = ?',
    options: [8, 9],
    correctIndex: 0,
    newState: 8,
  },
  {
    state: 'Estás en 8',
    question: '8 + 6 = ?',
    options: [14, 13],
    correctIndex: 0,
    newState: 14,
  },
  {
    state: 'Estás en 14',
    question: '14 − 5 = ?',
    options: [9, 10],
    correctIndex: 0,
    newState: 9,
  },
  {
    state: 'Estás en 9',
    question: '9 + 1 = ?',
    options: [10, 11],
    correctIndex: 0,
    newState: 10,
  },
  {
    state: 'Estás en 10',
    question: '10 + 5 = ?',
    options: [15, 14],
    correctIndex: 0,
    newState: 15,
  },
];

let currentStep = 0;
let soundEnabled = true;

// Imágenes de refuerzo que se mostrarán al alumno tras cada respuesta.
// Estas rutas apuntan a archivos en la carpeta `assets`. Cuando se
// acierta se elegirá aleatoriamente una de las imágenes de "clap", y
// cuando se falla una de "sad".
const successImages = ['clap1.png', 'clap2.png', 'clap3.png'];
const failureImages = ['sad1.png', 'sad2.png', 'sad3.png'];

// Variables de ayuda para mezclar las respuestas y saber cuál es la correcta
// `displayedOptions` contendrá las dos opciones en el orden en que se muestran
// `currentCorrectIndex` indica en qué posición de `displayedOptions` está la respuesta correcta
let displayedOptions = [];
let currentCorrectIndex = 0;

const motivationalMessages = [
  'Paso a paso lo consigo',
  'Hoy entreno mi mente',
  'Cada acierto me hace mejor',
];

// Selecciona una frase motivadora aleatoria
function setMotivational() {
  const msg =
    motivationalMessages[
      Math.floor(Math.random() * motivationalMessages.length)
    ];
  document.getElementById('motivational-text').textContent = msg;
}

// Carga el paso actual en la interfaz
function loadStep() {
  // Si hemos completado todas las preguntas, mostrar pantalla final
  if (currentStep >= questions.length) {
    showFinalScreen();
    return;
  }
  const q = questions[currentStep];
  document.getElementById('progress').textContent = `Paso ${
    currentStep + 1
  } de ${questions.length}`;
  document.getElementById('status').textContent = q.state;
  document.getElementById('question').textContent = q.question;
  document.getElementById('feedback').textContent = '';

  // Ocultar la pegatina de animal de la pregunta anterior (si existe)
  const sticker = document.getElementById('sticker');
  if (sticker) {
    sticker.classList.add('hidden');
  }

  // Alternar las opciones: en los pasos pares (índice 0, 2, 4...) la respuesta correcta
  // se muestra en la izquierda; en los pasos impares se muestra en la derecha.
  let order;
  if (currentStep % 2 === 0) {
    order = [0, 1];
  } else {
    order = [1, 0];
  }
  displayedOptions = order.map((i) => q.options[i]);
  currentCorrectIndex = order.indexOf(q.correctIndex);

  // Pintamos las opciones en los botones
  document.getElementById('optionA').textContent = displayedOptions[0];
  document.getElementById('optionB').textContent = displayedOptions[1];

  // Restablecer estilos y habilitar botones
  const buttons = document.querySelectorAll('.option-button');
  buttons.forEach((btn) => {
    btn.classList.remove('correct', 'incorrect');
    btn.disabled = false;
  });
}

// Genera un tono simple usando la Web Audio API
function playTone(frequency, duration) {
  if (!soundEnabled) return;
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    const context = new AudioCtx();
    const oscillator = context.createOscillator();
    const gainNode = context.createGain();
    oscillator.type = 'sine';
    oscillator.frequency.value = frequency;
    oscillator.connect(gainNode);
    gainNode.connect(context.destination);
    oscillator.start();
    // atenuar el volumen suavemente
    gainNode.gain.setValueAtTime(1, context.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, context.currentTime + duration);
    oscillator.stop(context.currentTime + duration);
  } catch (e) {
    // Algunas versiones antiguas de Safari pueden fallar; en ese caso
    // simplemente ignoramos el sonido.
    console.warn('No se pudo reproducir el sonido: ', e);
  }
}

function playCorrectSound() {
  // tono más alto y breve
  playTone(600, 0.2);
}

function playIncorrectSound() {
  // tono más bajo y un poco más largo
  playTone(200, 0.3);
}

// Manejador para las respuestas del alumno
function handleAnswer(index) {
  const q = questions[currentStep];
  const buttons = [
    document.getElementById('optionA'),
    document.getElementById('optionB'),
  ];
  // Comparamos contra currentCorrectIndex calculado en loadStep
  if (index === currentCorrectIndex) {
    // Respuesta correcta
    buttons[index].classList.add('correct');
    document.getElementById('feedback').textContent = `¡Correcto! Avanzas a ${
      q.newState
    }.`;
    // Mostrar un animal aplaudiendo
    const sticker = document.getElementById('sticker');
    const stickerImg = document.getElementById('sticker-img');
    if (sticker && stickerImg) {
      const imgName =
        successImages[Math.floor(Math.random() * successImages.length)];
      stickerImg.src = 'assets/' + imgName;
      sticker.classList.remove('hidden');
    }
    playCorrectSound();
    // Desactivar botones para evitar pulsaciones múltiples
    buttons.forEach((btn) => {
      btn.disabled = true;
    });
    // Avanzar al siguiente paso tras un breve retraso
    setTimeout(() => {
      currentStep += 1;
      loadStep();
    }, 1000);
  } else {
    // Respuesta incorrecta
    buttons[index].classList.add('incorrect');
    document.getElementById('feedback').textContent = 'No es ese. Inténtalo otra vez.';
    // Mostrar un animal triste
    const sticker = document.getElementById('sticker');
    const stickerImg = document.getElementById('sticker-img');
    if (sticker && stickerImg) {
      const imgName =
        failureImages[Math.floor(Math.random() * failureImages.length)];
      stickerImg.src = 'assets/' + imgName;
      sticker.classList.remove('hidden');
    }
    playIncorrectSound();
    // Eliminar el color rojo después de un momento para permitir reintento
    setTimeout(() => {
      buttons[index].classList.remove('incorrect');
    }, 800);
  }
}

// Mostrar la pantalla final y ocultar el juego
function showFinalScreen() {
  document.getElementById('game-container').classList.add('hidden');
  const finalScreen = document.getElementById('final-screen');
  document.getElementById('final-message').innerHTML =
    '¡Has llegado a 15! <br />¡Enhorabuena!';
  // Mostrar un emoji grande como trofeo. Utilizamos <span> con rol decorativo.
  const emojiContainer = document.getElementById('final-emoji');
  if (emojiContainer) {
    emojiContainer.textContent = '🎉🥳';
  }
  // Reproducir un sonido de celebración (subida de tonos)
  playFinalSound();
  finalScreen.classList.remove('hidden');
}

// Sonido especial para la pantalla final. Reproduce dos tonos en sucesión.
function playFinalSound() {
  if (!soundEnabled) return;
  // Primer tono
  playTone(600, 0.3);
  setTimeout(() => {
    playTone(800, 0.4);
  }, 300);
}

// Reiniciar el juego desde el paso 0
function restart() {
  currentStep = 0;
  document.getElementById('final-screen').classList.add('hidden');
  document.getElementById('game-container').classList.remove('hidden');
  loadStep();
}

// Asignar eventos a los botones
document.getElementById('optionA').addEventListener('click', () => handleAnswer(0));
document.getElementById('optionB').addEventListener('click', () => handleAnswer(1));
document.getElementById('restart').addEventListener('click', restart);
document.getElementById('restart-final').addEventListener('click', restart);

// Alternar el sonido y actualizar el icono del botón
document.getElementById('toggle-sound').addEventListener('click', () => {
  soundEnabled = !soundEnabled;
  document.getElementById('toggle-sound').textContent = soundEnabled ? '🔈' : '🔇';
});

// Inicializar la frase motivadora y el primer paso
setMotivational();
loadStep();