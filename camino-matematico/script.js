// =======================
// Camino Matemático - script.js (adaptado a tus IDs y .PNG)
// =======================

// Preguntas demo (luego las cambiamos por niveles)
const QUESTIONS = [
  { a: 3, b: 2, op: "+", correct: 5, wrong: 6 },
  { a: 7, b: 4, op: "-", correct: 3, wrong: 2 },
  { a: 6, b: 1, op: "+", correct: 7, wrong: 8 },
  { a: 9, b: 5, op: "-", correct: 4, wrong: 6 },
];

let currentIndex = 0;
let energy = 0; // 0..100

// =======================
// DOM (IDs reales de tu index)
// =======================

const screens = {
  home: document.getElementById("screen-home"),
  game: document.getElementById("screen-game"),
  final: document.getElementById("screen-final"),
};

// Botones reales
const btnHomeNext = document.getElementById("home-next");
const btnCheck = document.getElementById("btn-check");
const btnNext = document.getElementById("btn-next");       // el flotante (si lo quieres usar)
const btnFinalRetry = document.getElementById("final-retry");

// Elementos juego
const warriorImg = document.getElementById("warrior");
const questionEl = document.getElementById("question");

const answerButtons = Array.from(document.querySelectorAll(".answer-btn"));
const answerAText = document.getElementById("answer-a-text");
const answerBText = document.getElementById("answer-b-text");

const iconCorrect = document.getElementById("icon-correct");
const iconWrong = document.getElementById("icon-wrong");

const energyText = document.getElementById("energy-text");
const energyFillImg = document.getElementById("energy-fill"); // <img> del fill

// =======================
// Rutas assets (según tus capturas: muchos acaban en .PNG)
// =======================

const ASSETS = {
  warrior: {
    idle: "./assets/warrior/warrior-idle.png.PNG",
    power: "./assets/warrior/warrior-power.png.PNG",
    sad: "./assets/warrior/warrior-sad.png.PNG",
  },
};

// =======================
// Estado interacción
// =======================

let selectedAnswer = null;
let locked = false;

// =======================
// Helpers UI
// =======================

function showScreen(name) {
  Object.values(screens).forEach((el) => el && el.classList.remove("is-active"));
  screens[name] && screens[name].classList.add("is-active");
}

function setWarrior(state) {
  if (!warriorImg) return;
  if (state === "idle") warriorImg.src = ASSETS.warrior.idle;
  if (state === "power") warriorImg.src = ASSETS.warrior.power;
  if (state === "sad") warriorImg.src = ASSETS.warrior.sad;
}

function hideFeedback() {
  if (iconCorrect) iconCorrect.style.display = "none";
  if (iconWrong) iconWrong.style.display = "none";
}

function showFeedback(type) {
  // type: "correct" | "wrong"
  hideFeedback();
  if (type === "correct" && iconCorrect) iconCorrect.style.display = "block";
  if (type === "wrong" && iconWrong) iconWrong.style.display = "block";
}

function setEnergy(newValue) {
  energy = Math.max(0, Math.min(100, newValue));
  updateEnergyUI();
}

function updateEnergyUI() {
  // Texto
  if (energyText) energyText.textContent = String(energy);

  // Relleno: como es una IMAGEN, usamos clip-path para simular el progreso
  // (0% = invisible, 100% = completa)
  if (energyFillImg) {
    const p = energy / 100;
    energyFillImg.style.clipPath = `inset(0 ${100 - p * 100}% 0 0)`;
    energyFillImg.style.webkitClipPath = `inset(0 ${100 - p * 100}% 0 0)`;
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
  hideFeedback();
  setWarrior("idle");

  const q = currentQuestion();

  if (questionEl) {
    questionEl.textContent = `${q.a} ${q.op} ${q.b} = ?`;
  }

  // Aleatoriza posición correcta/incorrecta
  const options = [q.correct, q.wrong].sort(() => Math.random() - 0.5);

  if (answerButtons[0]) answerButtons[0].dataset.value = String(options[0]);
  if (answerButtons[1]) answerButtons[1].dataset.value = String(options[1]);

  if (answerAText) answerAText.textContent = String(options[0]);
  if (answerBText) answerBText.textContent = String(options[1]);

  // Oculta botón "Siguiente" flotante hasta que se compruebe (si lo usas)
  if (btnNext) btnNext.style.display = "none";
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

  // Si quieres usar el botón flotante "Siguiente"
  if (btnNext) btnNext.style.display = "block";

  // Si llega a 100 => final
  if (energy >= 100) {
    setTimeout(() => showScreen("final"), 500);
  }
}

function goNextQuestion() {
  if (!locked) return; // solo después de comprobar
  currentIndex += 1;
  loadQuestion();
}

// =======================
// Eventos
// =======================

function wireEvents() {
  // HOME -> GAME
  if (btnHomeNext) {
    btnHomeNext.addEventListener("click", () => {
      showScreen("game");
      setEnergy(0);
      currentIndex = 0;
      loadQuestion();
    });
  }

  // Selección respuestas
  answerButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (locked) return;
      selectedAnswer = btn.dataset.value || null;

      answerButtons.forEach((b) => b.classList.remove("is-selected"));
      btn.classList.add("is-selected");
    });
  });

  // Comprobar
  if (btnCheck) {
    btnCheck.addEventListener("click", () => checkAnswer());
  }

  // Botón flotante siguiente (si existe)
  if (btnNext) {
    btnNext.addEventListener("click", () => goNextQuestion());
  }

  // FINAL -> HOME (reinicio)
  if (btnFinalRetry) {
    btnFinalRetry.addEventListener("click", () => {
      setEnergy(0);
      currentIndex = 0;
      hideFeedback();
      setWarrior("idle");
      resetSelectionUI();
      showScreen("home");
    });
  }
}

// =======================
// Inicio seguro (evita que un null rompa todo)
// =======================

(function init() {
  try {
    wireEvents();
    showScreen("home");
    setEnergy(0);
    setWarrior("idle");
    hideFeedback();
  } catch (e) {
    // Si algo falla, al menos lo vemos en consola
    console.error("Error iniciando el juego:", e);
  }
})();
