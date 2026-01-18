// =======================
// Camino Matemático (Guerrero)
// Compatible con assets en .PNG (MAYUSCULAS)
// y con tu index.html actual (IDs correctos)
// =======================

// 10 pasos exactos (1º Primaria, sin llevadas, hasta 15)
// correct = respuesta correcta, wrong = incorrecta
const QUESTIONS = [
  { stateText: "Empiezas en 5", questionText: "5 + 3 = ?", correct: 8,  wrong: 9  },
  { stateText: "Estás en 8",    questionText: "8 − 2 = ?", correct: 6,  wrong: 5  },
  { stateText: "Estás en 6",    questionText: "6 + 4 = ?", correct: 10, wrong: 9  },
  { stateText: "Estás en 10",   questionText: "10 − 3 = ?", correct: 7,  wrong: 6  },
  { stateText: "Estás en 7",    questionText: "7 + 5 = ?", correct: 12, wrong: 13 },
  { stateText: "Estás en 12",   questionText: "12 − 4 = ?", correct: 8,  wrong: 9  },
  { stateText: "Estás en 8",    questionText: "8 + 6 = ?", correct: 14, wrong: 13 },
  { stateText: "Estás en 14",   questionText: "14 − 5 = ?", correct: 9,  wrong: 10 },
  { stateText: "Estás en 9",    questionText: "9 + 1 = ?", correct: 10, wrong: 11 },
  { stateText: "Estás en 10",   questionText: "10 + 5 = ?", correct: 15, wrong: 14 },
];

// Energía: empieza en 0, sube +10 por acierto, max 100, no baja
let energy = 0;

// Paso actual (0..9)
let currentIndex = 0;

// Selección del alumno
let selectedValue = null;
let locked = false;

// =======================
// Rutas de assets (.PNG)
// =======================
const ASSETS = {
  warrior: {
    idle: "./assets/warrior/warrior-idle.PNG",
    power: "./assets/warrior/warrior-power.PNG",
    sad: "./assets/warrior/warrior-sad.PNG",
  },
};

// =======================
// Elementos DOM (IDs de tu index.html)
// =======================
const screens = {
  home: document.getElementById("screen-home"),
  game: document.getElementById("screen-game"),
  final: document.getElementById("screen-final"),
};

const btnHomeNext = document.getElementById("home-next");
const btnCheck = document.getElementById("btn-check");
const btnRetry = document.getElementById("final-retry");

const warriorImg = document.getElementById("warrior");

const questionEl = document.getElementById("question");
const answerButtons = Array.from(document.querySelectorAll(".answer-btn"));
const answerAText = document.getElementById("answer-a-text");
const answerBText = document.getElementById("answer-b-text");

const iconCorrect = document.getElementById("icon-correct");
const iconWrong = document.getElementById("icon-wrong");

const energyFillImg = document.getElementById("energy-fill");
const energyTextEl = document.getElementById("energy-text");

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

function showFeedback(type) {
  // type: "correct" | "wrong" | null
  if (!iconCorrect || !iconWrong) return;

  if (!type) {
    iconCorrect.style.display = "none";
    iconWrong.style.display = "none";
    return;
  }

  if (type === "correct") {
    iconCorrect.style.display = "block";
    iconWrong.style.display = "none";
  } else {
    iconCorrect.style.display = "none";
    iconWrong.style.display = "block";
  }
}

function setEnergy(newValue) {
  energy = Math.max(0, Math.min(100, newValue));
  updateEnergyUI();
}

function updateEnergyUI() {
  if (energyTextEl) energyTextEl.textContent = String(energy);

  // Relleno por escala horizontal (0..1)
  if (energyFillImg) {
    energyFillImg.style.transformOrigin = "left center";
    energyFillImg.style.transform = `scaleX(${energy / 100})`;
  }
}

function resetSelectionUI() {
  selectedValue = null;
  answerButtons.forEach((btn) => btn.classList.remove("is-selected"));
}

function disableCheck(disabled) {
  if (!btnCheck) return;
  btnCheck.disabled = !!disabled;
  btnCheck.style.opacity = disabled ? "0.6" : "1";
}

// =======================
// Lógica del juego
// =======================
function loadStep() {
  locked = false;
  resetSelectionUI();
  showFeedback(null);
  setWarrior("idle");
  disableCheck(true);

  const step = QUESTIONS[currentIndex];

  // Pregunta en panel (incluye estado + operación)
  if (questionEl) {
    questionEl.textContent = `${step.stateText} · ${step.questionText}`;
  }

  // Alternar posición correcta izquierda/derecha (sin que el niño se lo aprenda)
  // Alterna por paso: pares izquierda, impares derecha
  const correctOnLeft = currentIndex % 2 === 0;

  const leftValue = correctOnLeft ? step.correct : step.wrong;
  const rightValue = correctOnLeft ? step.wrong : step.correct;

  // Guardar valores en botones
  if (answerButtons[0]) answerButtons[0].dataset.value = String(leftValue);
  if (answerButtons[1]) answerButtons[1].dataset.value = String(rightValue);

  if (answerAText) answerAText.textContent = String(leftValue);
  if (answerBText) answerBText.textContent = String(rightValue);
}

function isCorrectSelection() {
  const step = QUESTIONS[currentIndex];
  return Number(selectedValue) === Number(step.correct);
}

function goFinal() {
  showScreen("final");
}

function goNextStep() {
  currentIndex += 1;
  if (currentIndex >= QUESTIONS.length) {
    goFinal();
  } else {
    loadStep();
  }
}

function checkAnswer() {
  if (locked) return;
  if (selectedValue === null) return;

  locked = true;
  disableCheck(true);

  if (isCorrectSelection()) {
    // Acierto
    setWarrior("power");
    showFeedback("correct");
    setEnergy(energy + 10);

    // Avanza automáticamente
    setTimeout(() => {
      goNextStep();
    }, 700);
  } else {
    // Fallo
    setWarrior("sad");
    showFeedback("wrong");

    // No avanza; permite reintentar
    setTimeout(() => {
      locked = false;
      setWarrior("idle");
      disableCheck(false);
    }, 700);
  }
}

// =======================
// Eventos
// =======================
if (btnHomeNext) {
  btnHomeNext.addEventListener("click", () => {
    showScreen("game");
    currentIndex = 0;
    setEnergy(0);
    loadStep();
  });
}

answerButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (locked) return;

    selectedValue = btn.dataset.value || null;

    // UI selección
    answerButtons.forEach((b) => b.classList.remove("is-selected"));
    btn.classList.add("is-selected");

    // Ahora sí se puede comprobar
    disableCheck(false);
  });
});

if (btnCheck) {
  btnCheck.addEventListener("click", () => {
    checkAnswer();
  });
}

if (btnRetry) {
  btnRetry.addEventListener("click", () => {
    // Reiniciar
    currentIndex = 0;
    setEnergy(0);
    showFeedback(null);
    setWarrior("idle");
    showScreen("home");
  });
}

// =======================
// Inicio
// =======================
showScreen("home");
setEnergy(0);
setWarrior("idle");
showFeedback(null);
disableCheck(true);
