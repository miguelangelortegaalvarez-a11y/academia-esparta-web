// =======================
// Configuracion del juego
// =======================

const QUESTIONS = [
  // Mantengo preguntas simples por defecto.
  // Luego las cambiamos por las tuyas (sumas/restas por niveles).
  { a: 3, b: 2, op: "+", correct: 5, wrong: 6 },
  { a: 7, b: 4, op: "-", correct: 3, wrong: 2 },
  { a: 6, b: 1, op: "+", correct: 7, wrong: 8 },
  { a: 9, b: 5, op: "-", correct: 4, wrong: 6 },
];

let currentIndex = 0;

// Energia: empieza en 0, sube +10 por acierto, max 100, no baja nunca.
let energy = 0;

// Estado de pantalla
const screens = {
  home: document.getElementById("screen-home"),
  game: document.getElementById("screen-game"),
  final: document.getElementById("screen-final"),
};

// Botones
const btnHomeNext = document.getElementById("btn-home-next");
const btnCheck = document.getElementById("btn-check");
const btnRetry = document.getElementById("btn-retry");

// Elementos de juego
const warriorImg = document.getElementById("warrior");
const feedbackIcon = document.getElementById("feedback-icon");
const answerButtons = Array.from(document.querySelectorAll(".answer-btn"));

// Rutas assets (fijas)
const ASSETS = {
  warrior: {
    idle: "./assets/warrior/warrior-idle.png",
    power: "./assets/warrior/warrior-power.png",
    sad: "./assets/warrior/warrior-sad.png",
  },
  icons: {
    correct: "./assets/ui/icons/icon-correct.png",
    wrong: "./assets/ui/icons/icon-wrong.png",
  },
};

// Para seleccionar una respuesta
let selectedAnswer = null;
let locked = false;

// =======================
// Helpers UI
// =======================

function showScreen(name) {
  Object.values(screens).forEach((el) => el.classList.remove("is-active"));
  screens[name].classList.add("is-active");
}

function setWarrior(state) {
  if (state === "idle") warriorImg.src = ASSETS.warrior.idle;
  if (state === "power") warriorImg.src = ASSETS.warrior.power;
  if (state === "sad") warriorImg.src = ASSETS.warrior.sad;
}

function showFeedback(type) {
  // type: "correct" | "wrong" | null
  if (!type) {
    feedbackIcon.hidden = true;
    feedbackIcon.src = "";
    return;
  }
  feedbackIcon.hidden = false;
  feedbackIcon.src = type === "correct" ? ASSETS.icons.correct : ASSETS.icons.wrong;
}

function setEnergy(newValue) {
  energy = Math.max(0, Math.min(100, newValue));
  updateEnergyUI();
}

function updateEnergyUI() {
  // El relleno es un DIV con overflow hidden que contiene la imagen del fill.
  // Ajustamos el ancho en porcentaje.
  const fillContainer = document.querySelector(".energy-fill");
  if (fillContainer) fillContainer.style.width = `${energy}%`;
}

function resetSelectionUI() {
  selectedAnswer = null;
  answerButtons.forEach((btn) => btn.classList.remove("is-selected"));
}

// =======================
// Logica de preguntas
// =======================

function currentQuestion() {
  return QUESTIONS[currentIndex % QUESTIONS.length];
}

function loadQuestion() {
  locked = false;
  resetSelectionUI();
  showFeedback(null);
  setWarrior("idle");

  const q = currentQuestion();

  // Asignar valores a los dos botones (data-answer 1 y 2).
  // Aleatorizamos posicion de correct/wrong.
  const options = [q.correct, q.wrong].sort(() => Math.random() - 0.5);

  // Guardamos la respuesta correcta real en cada boton
  answerButtons[0].dataset.value = String(options[0]);
  answerButtons[1].dataset.value = String(options[1]);

  // Importante: tu index usa una imagen como boton.
  // El numero no se ve porque no hay texto.
  // De momento, el juego funciona aunque no se vea el numero.
  // En el siguiente paso lo hacemos visible con CSS + un overlay de texto.
}

function checkAnswer() {
  if (locked) return;
  if (selectedAnswer === null) return;

  locked = true;
  const q = currentQuestion();
  const isCorrect = Number(selectedAnswer) === Number(q.correct);

  if (isCorrect) {
    setWarrior("power");
    showFeedback("correct");
    setEnergy(energy + 10); // no baja, max 100
  } else {
    setWarrior("sad");
    showFeedback("wrong");
  }

  // Si energia llega a 100 -> pantalla final
  if (energy >= 100) {
    // pequeña pausa visual
    setTimeout(() => {
      showScreen("final");
    }, 400);
    return;
  }

  // Pasar a siguiente pregunta tras una pausa
  setTimeout(() => {
    currentIndex += 1;
    loadQuestion();
  }, 700);
}

// =======================
// Eventos
// =======================

btnHomeNext.addEventListener("click", () => {
  showScreen("game");
  setEnergy(0);
  currentIndex = 0;
  loadQuestion();
});

answerButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (locked) return;
    // Guardar seleccion
    selectedAnswer = btn.dataset.value || null;

    // UI seleccion
    answerButtons.forEach((b) => b.classList.remove("is-selected"));
    btn.classList.add("is-selected");
  });
});

btnCheck.addEventListener("click", () => {
  checkAnswer();
});

btnRetry.addEventListener("click", () => {
  // Reiniciar juego
  setEnergy(0);
  currentIndex = 0;
  showScreen("home");
  setWarrior("idle");
  showFeedback(null);
  resetSelectionUI();
});

// =======================
// Inicio
// =======================

showScreen("home");
setEnergy(0);
setWarrior("idle");
showFeedback(null);
