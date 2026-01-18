// =======================
// Camino Matemático - script.js
// Auto-comprobar al pulsar número (sin botón "Comprobar")
// =======================

const QUESTIONS = [
  { a: 3, b: 2, op: "+", correct: 5, wrong: 6 },
  { a: 7, b: 4, op: "-", correct: 3, wrong: 2 },
  { a: 6, b: 1, op: "+", correct: 7, wrong: 8 },
  { a: 9, b: 5, op: "-", correct: 4, wrong: 6 },
];

let currentIndex = 0;
let energy = 0; // lo dejamos por si luego vuelves a la barra
let locked = false;

const ASSETS = {
  warrior: {
    idle: "./assets/warrior/warrior-idle.png.PNG",
    power: "./assets/warrior/warrior-power.png.PNG",
    sad: "./assets/warrior/warrior-sad.png.PNG",
  },
};

function $(id) {
  return document.getElementById(id);
}

function showScreen(screens, name) {
  Object.values(screens).forEach((el) => el && el.classList.remove("is-active"));
  screens[name] && screens[name].classList.add("is-active");
}

function setWarrior(warriorImg, state) {
  if (!warriorImg) return;
  if (state === "idle") warriorImg.src = ASSETS.warrior.idle;
  if (state === "power") warriorImg.src = ASSETS.warrior.power;
  if (state === "sad") warriorImg.src = ASSETS.warrior.sad;
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

function clamp(n, a, b) {
  return Math.max(a, Math.min(b, n));
}

function currentQuestion() {
  return QUESTIONS[currentIndex % QUESTIONS.length];
}

function loadQuestion(ctx) {
  locked = false;
  hideFeedback(ctx.iconCorrect, ctx.iconWrong);
  setWarrior(ctx.warriorImg, "idle");

  const q = currentQuestion();

  if (ctx.questionEl) {
    ctx.questionEl.textContent = `${q.a} ${q.op} ${q.b} = ?`;
  }

  // Aleatoriza posición correcta/incorrecta
  const options = [q.correct, q.wrong].sort(() => Math.random() - 0.5);

  if (ctx.answerButtons[0]) ctx.answerButtons[0].dataset.value = String(options[0]);
  if (ctx.answerButtons[1]) ctx.answerButtons[1].dataset.value = String(options[1]);

  if (ctx.answerAText) ctx.answerAText.textContent = String(options[0]);
  if (ctx.answerBText) ctx.answerBText.textContent = String(options[1]);

  // Limpia selección visual
  ctx.answerButtons.forEach((b) => b.classList.remove("is-selected"));
}

function checkAnswerAndAdvance(ctx, selectedValue) {
  if (locked) return;
  locked = true;

  const q = currentQuestion();
  const isCorrect = Number(selectedValue) === Number(q.correct);

  if (isCorrect) {
    setWarrior(ctx.warriorImg, "power");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "correct");
    energy = clamp(energy + 10, 0, 100);
  } else {
    setWarrior(ctx.warriorImg, "sad");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "wrong");
  }

  // Si llega a 100 => final
  if (energy >= 100) {
    setTimeout(() => showScreen(ctx.screens, "final"), 650);
    return;
  }

  // Siguiente pregunta automático
  setTimeout(() => {
    currentIndex += 1;
    loadQuestion(ctx);
  }, 700);
}

function init() {
  const screens = {
    home: $("screen-home"),
    game: $("screen-game"),
    final: $("screen-final"),
  };

  const btnHomeNext = $("home-next");
  const btnFinalRetry = $("final-retry");

  const warriorImg = $("warrior");
  const questionEl = $("question");

  const answerButtons = Array.from(document.querySelectorAll(".answer-btn"));
  const answerAText = $("answer-a-text");
  const answerBText = $("answer-b-text");

  const iconCorrect = $("icon-correct");
  const iconWrong = $("icon-wrong");

  const ctx = {
    screens,
    warriorImg,
    questionEl,
    answerButtons,
    answerAText,
    answerBText,
    iconCorrect,
    iconWrong,
  };

  // Estado inicial
  energy = 0;
  currentIndex = 0;
  locked = false;

  setWarrior(warriorImg, "idle");
  hideFeedback(iconCorrect, iconWrong);
  showScreen(screens, "home");

  // HOME -> GAME
  if (btnHomeNext) {
    btnHomeNext.addEventListener("click", () => {
      energy = 0;
      currentIndex = 0;
      locked = false;

      showScreen(screens, "game");
      loadQuestion(ctx);
    });
  }

  // Click en respuestas = seleccionar + comprobar automáticamente
  answerButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (locked) return;

      const val = btn.dataset.value;
      if (val == null) return;

      // Marca visual selección
      answerButtons.forEach((b) => b.classList.remove("is-selected"));
      btn.classList.add("is-selected");

      // Auto-check
      checkAnswerAndAdvance(ctx, val);
    });
  });

  // FINAL -> HOME
  if (btnFinalRetry) {
    btnFinalRetry.addEventListener("click", () => {
      energy = 0;
      currentIndex = 0;
      locked = false;

      hideFeedback(iconCorrect, iconWrong);
      setWarrior(warriorImg, "idle");
      answerButtons.forEach((b) => b.classList.remove("is-selected"));
      showScreen(screens, "home");
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  try {
    init();
  } catch (e) {
    console.error("Error iniciando el juego:", e);
  }
});
