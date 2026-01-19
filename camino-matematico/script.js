// =======================
// Camino Matemático - script.js
// MODOS: SUMAS/RESTAS y MULTIPLICACIONES
// Nivel visible + sube cada 3 aciertos
// =======================

let selectedAnswer = null;
let locked = false;

let correctCount = 0;
const GOAL = 10;

let level = 1;            // Nivel actual
let streak = 0;           // Aciertos seguidos para subir nivel (cada 3)
let mode = null;          // "sumasrestas" | "multiplicaciones"

let currentQ = null;      // pregunta actual

// Assets (tus nombres actuales con doble extensión)
const ASSETS = {
  warrior: {
    idle: "./assets/warrior/warrior-idle.png.PNG",
    power: "./assets/warrior/warrior-power.png.PNG",
    sad: "./assets/warrior/warrior-sad.png.PNG",
  },
};

function $(id) { return document.getElementById(id); }

function showScreen(screens, name) {
  Object.values(screens).forEach((el) => el && el.classList.remove("is-active"));
  screens[name] && screens[name].classList.add("is-active");
}

function setWarrior(warriorImg, state) {
  if (!warriorImg) return;
  warriorImg.src =
    state === "power" ? ASSETS.warrior.power :
    state === "sad" ? ASSETS.warrior.sad :
    ASSETS.warrior.idle;
}

function hideFeedback(iconCorrect, iconWrong) {
  if (iconCorrect) iconCorrect.style.display = "none";
  if (iconWrong) iconWrong.style.display = "none";
}

function showFeedback(iconCorrect, iconWrong, type) {
  hideFeedback(iconCorrect, iconWrong);
  if (type === "correct" && iconCorrect) iconCorrect.style.display = "block";
  if (type === "wrong" && iconWrong) iconWrong.style.display = "block";
}

function resetSelectionUI(answerButtons) {
  selectedAnswer = null;
  answerButtons.forEach((btn) => btn.classList.remove("is-selected"));
}

function updateProgress(ctx) {
  const pct = Math.min(100, (correctCount / GOAL) * 100);
  if (ctx.progressFill) ctx.progressFill.style.width = pct + "%";
  if (ctx.progressText) ctx.progressText.textContent = `${correctCount}/${GOAL}`;
}

function updateLevelUI(ctx) {
  if (ctx.levelText) ctx.levelText.textContent = `Nivel ${level}`;
}

// =======================
// Generadores por modo + nivel
// =======================

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function makeQuestionSumasRestas() {
  // Nivel 1: 0..10
  // Cada nivel sube el rango 5 puntos (ajustable)
  const MAX = 10 + (level - 1) * 5;
  const MIN = 0;

  const op = Math.random() < 0.5 ? "+" : "-";

  let a = randInt(MIN, MAX);
  let b = randInt(MIN, MAX);

  // Evitar negativos en restas
  if (op === "-" && b > a) [a, b] = [b, a];

  const correct = op === "+" ? a + b : a - b;

  // Wrong cercano y no negativo
  let wrong = correct;
  while (wrong === correct || wrong < 0) {
    const delta = randInt(-3, 3);
    if (delta === 0) continue;
    wrong = correct + delta;
  }

  return { text: `${a} ${op} ${b} = ?`, correct, wrong };
}

function makeQuestionMultiplicaciones() {
  // Nivel 1: factores 0..5
  // Cada nivel sube el factor máximo 2 puntos (ajustable)
  const MAX = 5 + (level - 1) * 2;
  const MIN = 0;

  const a = randInt(MIN, MAX);
  const b = randInt(MIN, MAX);

  const correct = a * b;

  let wrong = correct;
  while (wrong === correct || wrong < 0) {
    const delta = randInt(-5, 5);
    if (delta === 0) continue;
    wrong = correct + delta;
  }

  return { text: `${a} × ${b} = ?`, correct, wrong };
}

function makeQuestionByMode() {
  if (mode === "multiplicaciones") return makeQuestionMultiplicaciones();
  return makeQuestionSumasRestas(); // por defecto sumas/restas
}

function currentQuestion() {
  if (!currentQ) currentQ = makeQuestionByMode();
  return currentQ;
}

// =======================
// Flujo de juego
// =======================

function loadQuestion(ctx) {
  locked = false;
  resetSelectionUI(ctx.answerButtons);
  hideFeedback(ctx.iconCorrect, ctx.iconWrong);
  setWarrior(ctx.warriorImg, "idle");

  updateLevelUI(ctx);

  const q = currentQuestion();
  if (ctx.questionEl) ctx.questionEl.textContent = q.text;

  const options = [q.correct, q.wrong].sort(() => Math.random() - 0.5);

  if (ctx.answerButtons[0]) ctx.answerButtons[0].dataset.value = String(options[0]);
  if (ctx.answerButtons[1]) ctx.answerButtons[1].dataset.value = String(options[1]);

  if (ctx.answerAText) ctx.answerAText.textContent = String(options[0]);
  if (ctx.answerBText) ctx.answerBText.textContent = String(options[1]);

  updateProgress(ctx);
}

function checkAnswer(ctx) {
  if (locked) return;
  if (selectedAnswer === null) return;

  locked = true;
  const q = currentQuestion();
  const isCorrect = Number(selectedAnswer) === Number(q.correct);

  if (isCorrect) {
    correctCount += 1;
    streak += 1;

    // Subir nivel cada 3 aciertos
    if (streak >= 3) {
      level += 1;
      streak = 0;
    }

    updateProgress(ctx);
    updateLevelUI(ctx);

    setWarrior(ctx.warriorImg, "power");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "correct");

    if (correctCount >= GOAL) {
      if (ctx.progressFill && ctx.progressFill.parentElement) {
        ctx.progressFill.parentElement.classList.add("complete");
      }
      showScreen(ctx.screens, "final");
      return;
    }
  } else {
    // Fallo: NO sumamos aciertos, reiniciamos racha
    streak = 0;

    setWarrior(ctx.warriorImg, "sad");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "wrong");
  }

  // Siguiente pregunta
  setTimeout(() => {
    currentQ = null;
    loadQuestion(ctx);
  }, 2000);
}

function startGame(ctx, newMode) {
  mode = newMode;

  correctCount = 0;
  level = 1;
  streak = 0;
  locked = false;
  selectedAnswer = null;
  currentQ = null;

  updateProgress(ctx);
  updateLevelUI(ctx);

  if (ctx.progressFill && ctx.progressFill.parentElement) {
    ctx.progressFill.parentElement.classList.remove("complete");
  }

  showScreen(ctx.screens, "game");
  loadQuestion(ctx);
}

function init() {
  const screens = {
    home: $("screen-home"),
    game: $("screen-game"),
    final: $("screen-final"),
  };

  // BOTONES HOME (los nuevos)
  const btnModeSumasRestas = $("home-mode-sumasrestas");
  const btnModeMultiplicaciones = $("home-mode-multiplicaciones");

  const btnCheck = $("btn-check");
  const btnFinalRetry = $("final-retry");

  const warriorImg = $("warrior");
  const questionEl = $("question");

  const answerButtons = Array.from(document.querySelectorAll(".answer-btn"));
  const answerAText = $("answer-a-text");
  const answerBText = $("answer-b-text");

  const iconCorrect = $("icon-correct");
  const iconWrong = $("icon-wrong");

  const progressFill = $("progress-fill");
  const progressText = $("progress-text");

  // NIVEL (nuevo)
  const levelText = $("level-text");

  const ctx = {
    screens,
    warriorImg,
    questionEl,
    answerButtons,
    answerAText,
    answerBText,
    iconCorrect,
    iconWrong,
    progressFill,
    progressText,
    levelText,
  };

  // Estado inicial
  locked = false;
  selectedAnswer = null;
  correctCount = 0;
  level = 1;
  streak = 0;
  mode = null;
  currentQ = null;

  setWarrior(warriorImg, "idle");
  hideFeedback(iconCorrect, iconWrong);
  updateProgress(ctx);
  updateLevelUI(ctx);
  showScreen(screens, "home");

  // HOME -> GAME por modo
  if (btnModeSumasRestas) {
    btnModeSumasRestas.addEventListener("click", () => startGame(ctx, "sumasrestas"));
  }
  if (btnModeMultiplicaciones) {
    btnModeMultiplicaciones.addEventListener("click", () => startGame(ctx, "multiplicaciones"));
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
    btnCheck.addEventListener("click", () => checkAnswer(ctx));
  }

  // FINAL -> HOME
  if (btnFinalRetry) {
    btnFinalRetry.addEventListener("click", () => {
      locked = false;
      selectedAnswer = null;
      currentQ = null;

      hideFeedback(iconCorrect, iconWrong);
      setWarrior(warriorImg, "idle");
      resetSelectionUI(answerButtons);

      showScreen(screens, "home");
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  try { init(); }
  catch (e) { console.error("Error iniciando el juego:", e); }
});
