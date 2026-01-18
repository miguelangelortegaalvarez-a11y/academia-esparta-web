// =======================
// Configuración del juego
// =======================

const QUESTIONS = [
  { a: 3, b: 2, op: "+", correct: 5, wrong: 6 },
  { a: 7, b: 4, op: "-", correct: 3, wrong: 2 },
  { a: 6, b: 1, op: "+", correct: 7, wrong: 8 },
  { a: 9, b: 5, op: "-", correct: 4, wrong: 6 },
];

let currentIndex = 0;

// Energía: empieza en 0, sube +10 por acierto, max 100, no baja nunca.
let energy = 0;

// Estado de pantalla
const screens = {
  home: document.getElementById("screen-home"),
  game: document.getElementById("screen-game"),
  final: document.getElementById("screen-final"),
};

// Botones (IDs reales del index.html)
const btnHomeNext = document.getElementById("home-next");
const btnCheck = document.getElementById("btn-check");
const btnNext = document.getElementById("btn-next");
const btnFinalRetry = document.getElementById("final-retry");

// Elementos de juego
const warriorImg = document.getElementById("warrior");
const answerButtons = Array.from(document.querySelectorAll(".answer-btn"));
const answerAText = document.getElementById("answer-a-text");
const answerBText = document.getElementById("answer-b-text");

// Feedback (en tu HTML hay 2 iconos separados)
const iconCorrect = document.getElementById("icon-correct");
const iconWrong = document.getElementById("icon-wrong");

// Energía UI (tus elementos reales del HTML)
const energyText = document.getElementById("energy-text");
const energyFillImg = document.getElementById("energy-fill"); // <img> que vamos a recortar con clipPath

// Rutas assets (EN MAYÚSCULAS .PNG según tus carpetas)
const ASSETS = {
  warrior: {
    idle: "./assets/warrior/warrior-idle.png.PNG",
    power: "./assets/warrior/warrior-power.png.PNG",
    sad: "./assets/warrior/warrior-sad.png.PNG",
  },
};

// Selección y bloqueo
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
  if (iconCorrect) iconCorrect.style.display = "none";
  if (iconWrong) iconWrong.style.display = "none";

  if (!type) return;

  if (type === "correct" && iconCorrect) iconCorrect.style.display = "block";
  if (type === "wrong" && iconWrong) iconWrong.style.display = "block";
}

function setEnergy(newValue) {
  energy = Math.max(0, Math.min(100, newValue));
  updateEnergyUI();
}

function updateEnergyUI() {
  if (energyText) energyText.textContent = String(energy);

  // Recorte horizontal del <img> según porcentaje (clip-path)
  if (energyFillImg) {
    const p = Math.max(0, Math.min(100, energy));
    energyFillImg.style.clipPath = `inset(0 ${100 - p}% 0 0)`;
  }
}

function resetSelectionUI() {
  selectedAnswer = null;
  answerButtons.forEach((btn) => btn.classList.remove("is-selected"));
}

// =======================
// Lógica de preguntas
// =======================

function currentQuestion() {
  return QUESTIONS[currentIndex % QUESTIONS.length];
}

function loadQuestion() {
  locked = false;
  resetSelectionUI();
  showFeedback(null);
  setWarrior("idle");

  // Ocultar botón siguiente (solo debe salir tras comprobar)
  if (btnNext) btnNext.style.display = "none";

  const q = currentQuestion();

  // Generar texto de la pregunta
  const questionEl = document.getElementById("question");
  if (questionEl) questionEl.textContent = `${q.a} ${q.op} ${q.b} = ?`;

  // Aleatorizar posición de correct/wrong
  const options = [q.correct, q.wrong].sort(() => Math.random() - 0.5);

  // Asignar valores a botones
  answerButtons[0].dataset.value = String(options[0]);
  answerButtons[1].dataset.value = String(options[1]);
  answerAText.textContent = String(options[0]);
  answerBText.textContent = String(options[1]);
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
    setEnergy(energy + 10);
  } else {
    setWarrior("sad");
    showFeedback("wrong");
  }

  // Mostrar botón siguiente tras comprobar
  if (btnNext) btnNext.style.display = "block";

  // Si energía llega a 100 -> pantalla final
  if (energy >= 100) {
    setTimeout(() => {
      showScreen("final");
    }, 400);
  }
}

function goNextQuestion() {
  if (!locked) return; // solo después de comprobar
  if (energy >= 100) return;

  currentIndex += 1;
  loadQuestion();
}

// =======================
// Eventos
// =======================

if (btnHomeNext) {
  btnHomeNext.addEventListener("click", () => {
    showScreen("game");
    setEnergy(0);
    currentIndex = 0;
    loadQuestion();
  });
}

answerButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (locked) return;
    selectedAnswer = btn.dataset.value || null;

    answerButtons.forEach((b) => b.classList.remove("is-selected"));
    btn.classList.add("is-selected");
  });
});

if (btnCheck) {
  btnCheck.addEventListener("click", () => {
    checkAnswer();
  });
}

if (btnNext) {
  btnNext.addEventListener("click", () => {
    goNextQuestion();
  });
}

if (btnFinalRetry) {
  btnFinalRetry.addEventListener("click", () => {
    setEnergy(0);
    currentIndex = 0;
    showFeedback(null);
    setWarrior("idle");
    showScreen("home");
    resetSelectionUI();
    if (btnNext) btnNext.style.display = "none";
  });
}

// =======================
// Inicio
// =======================

showScreen("home");
setEnergy(0);
setWarrior("idle");
showFeedback(null);
if (btnNext) btnNext.style.display = "none";
