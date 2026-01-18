// =======================
// Camino Matemático - script.js (SIN barra energía)
// =======================

// Preguntas demo (luego cambiamos por niveles / por tu banco de ejercicios)
const QUESTIONS = [
  { a: 3, b: 2, op: "+", correct: 5, wrong: 6 },
  { a: 7, b: 4, op: "-", correct: 3, wrong: 2 },
  { a: 6, b: 1, op: "+", correct: 7, wrong: 8 },
  { a: 9, b: 5, op: "-", correct: 4, wrong: 6 },
];

let currentIndex = 0;
let selectedAnswer = null;
let locked = false;
let correctCount = 0;
const GOAL = 10;
let currentQ = null; // pregunta actualpaso
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

function makeQuestion() {
  // Config simple: sumas y restas sin negativos (Infantil/Primaria)
  const ops = ["+", "-"];
  const op = ops[Math.floor(Math.random() * ops.length)];

  let a = 0, b = 0, correct = 0;

  if (op === "+") {
    a = 1 + Math.floor(Math.random() * 9);  // 1..9
    b = 1 + Math.floor(Math.random() * 9);  // 1..9
    correct = a + b;
  } else {
    a = 1 + Math.floor(Math.random() * 9);  // 1..9
    b = 1 + Math.floor(Math.random() * 9);  // 1..9
    if (b > a) [a, b] = [b, a];             // evita negativos
    correct = a - b;
  }

  // wrong: cercano pero distinto (y >=0)
  let wrong = correct;
  while (wrong === correct) {
    const delta = 1 + Math.floor(Math.random() * 3); // 1..3
    wrong = Math.random() < 0.5 ? correct + delta : Math.max(0, correct - delta);
  }

  return { a, b, op, correct, wrong };
}

function currentQuestion() {
  // Si no hay pregunta, crea una
  if (!currentQ) currentQ = makeQuestion();
  return currentQ;
}
function updateProgress(ctx) {
  const pct = Math.min(100, (correctCount / GOAL) * 100);
  if (ctx.progressFill) ctx.progressFill.style.width = pct + "%";
  if (ctx.progressText) ctx.progressText.textContent = `${correctCount}/${GOAL}`;
}
function loadQuestion(ctx) {
  locked = false;
  resetSelectionUI(ctx.answerButtons);
  hideFeedback(ctx.iconCorrect, ctx.iconWrong);
  setWarrior(ctx.warriorImg, "idle");

  const q = currentQuestion();
  if (ctx.questionEl) ctx.questionEl.textContent = `${q.a} ${q.op} ${q.b} = ?`;

  // Alterna de forma impredecible izquierda/derecha
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
  // ✅ SUMA PROGRESO SOLO AL ACERTAR
  correctCount += 1;
  updateProgress(ctx);

  // ✅ SI LLEGA A 10 → FINAL
  if (correctCount >= GOAL) {
    // Barra en dorado
    if (ctx.progressFill && ctx.progressFill.parentElement) {
      ctx.progressFill.parentElement.classList.add("complete");
    }

    showScreen(ctx.screens, "final");
    return; // ⛔️ IMPORTANTÍSIMO: corta aquí
  }

  setWarrior(ctx.warriorImg, "power");
  showFeedback(ctx.iconCorrect, ctx.iconWrong, "correct");

} else {
  // ❌ NO SUMA, ❌ NO RESTA
  setWarrior(ctx.warriorImg, "sad");
  showFeedback(ctx.iconCorrect, ctx.iconWrong, "wrong");
}

  // Tras un momento, siguiente pregunta (o fin si quieres por nº de aciertos)
  setTimeout(() => {
    currentIndex += 1;
    loadQuestion(ctx);
  }, 3000);
}

function init() {
  const screens = {
    home: $("screen-home"),
    game: $("screen-game"),
    final: $("screen-final"),
  };

  const btnHomeNext = $("home-next");
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
  const ctx = {
    screens,
    btnHomeNext,
    btnCheck,
    btnFinalRetry,
    warriorImg,
    questionEl,
    answerButtons,
    answerAText,
    answerBText,
    iconCorrect,
    iconWrong,
    progressFill,
    progressText,
  };

  // Estado inicial
  currentIndex = 0;
  locked = false;
  selectedAnswer = null;

  setWarrior(warriorImg, "idle");
  hideFeedback(iconCorrect, iconWrong);
  showScreen(screens, "home");

  // HOME -> GAME
  if (btnHomeNext) {
    btnHomeNext.addEventListener("click", () => {
    currentIndex = 0;
correctCount = 0;
locked = false;
selectedAnswer = null;

updateProgress(ctx);

if (ctx.progressFill && ctx.progressFill.parentElement) {
  ctx.progressFill.parentElement.classList.remove("complete");
}

showScreen(screens, "game");
loadQuestion(ctx);
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
    btnCheck.addEventListener("click", () => checkAnswer(ctx));
  }

  // FINAL -> HOME (si luego decides usar final, lo conectamos por regla)
  if (btnFinalRetry) {
    btnFinalRetry.addEventListener("click", () => {
      currentIndex = 0;
      locked = false;
      selectedAnswer = null;

      hideFeedback(iconCorrect, iconWrong);
      setWarrior(warriorImg, "idle");
      resetSelectionUI(answerButtons);
      showScreen(screens, "home");
    });
  }
}

// Arranque seguro
document.addEventListener("DOMContentLoaded", () => {
  try { init(); }
  catch (e) { console.error("Error iniciando el juego:", e); }
});
