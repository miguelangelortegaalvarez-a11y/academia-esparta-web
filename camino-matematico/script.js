// =======================
// Camino Matemático - script.js
// MODO INFINITO + PROGRESIÓN
// =======================

// Estado global
let selectedAnswer = null;
let locked = false;
let correctCount = 0;
let level = 1;
let streak = 0;
let currentQ = null;

// Assets
const ASSETS = {
  warrior: {
    idle: "./assets/warrior/warrior-idle.png.PNG",
    power: "./assets/warrior/warrior-power.png.PNG",
    sad: "./assets/warrior/warrior-sad.png.PNG",
  },
};

// Utilidades
function $(id) {
  return document.getElementById(id);
}

function showScreen(screens, name) {
  Object.values(screens).forEach((el) =>
    el && el.classList.remove("is-active")
  );
  screens[name] && screens[name].classList.add("is-active");
}

function setWarrior(img, state) {
  if (!img) return;
  img.src =
    state === "power"
      ? ASSETS.warrior.power
      : state === "sad"
      ? ASSETS.warrior.sad
      : ASSETS.warrior.idle;
}

function hideFeedback(ok, wrong) {
  if (ok) ok.style.display = "none";
  if (wrong) wrong.style.display = "none";
}

function showFeedback(ok, wrong, type) {
  hideFeedback(ok, wrong);
  if (type === "correct" && ok) ok.style.display = "block";
  if (type === "wrong" && wrong) wrong.style.display = "block";
}

function resetSelection(btns) {
  selectedAnswer = null;
  btns.forEach((b) => b.classList.remove("is-selected"));
}

// =======================
// GENERADOR DE EJERCICIOS
// =======================
function makeQuestion() {
  let max;

  if (level === 1) max = 5;
  else if (level === 2) max = 10;
  else if (level === 3) max = 20;
  else max = 50;

  const op = Math.random() < 0.5 ? "+" : "-";

  let a = Math.floor(Math.random() * (max + 1));
  let b = Math.floor(Math.random() * (max + 1));

  if (op === "-" && b > a) [a, b] = [b, a];

  const correct = op === "+" ? a + b : a - b;

  let wrong = correct;
  while (wrong === correct || wrong < 0) {
    wrong = correct + (Math.floor(Math.random() * 7) - 3);
  }

  return { a, b, op, correct, wrong };
}

// =======================
// CARGA DE PREGUNTA
// =======================
function loadQuestion(ctx) {
  locked = false;
  resetSelection(ctx.answerButtons);
  hideFeedback(ctx.iconCorrect, ctx.iconWrong);
  setWarrior(ctx.warriorImg, "idle");

  currentQ = makeQuestion();

  ctx.questionEl.textContent = `${currentQ.a} ${currentQ.op} ${currentQ.b} = ?`;

  const options = [currentQ.correct, currentQ.wrong].sort(
    () => Math.random() - 0.5
  );

  ctx.answerButtons[0].dataset.value = options[0];
  ctx.answerButtons[1].dataset.value = options[1];

  ctx.answerAText.textContent = options[0];
  ctx.answerBText.textContent = options[1];

  ctx.progressText.textContent = `Aciertos: ${correctCount}`;
  ctx.levelText.textContent = `Nivel ${level}`;
}

// =======================
// COMPROBAR RESPUESTA
// =======================
function checkAnswer(ctx) {
  if (locked || selectedAnswer === null) return;
  locked = true;

  const isCorrect = Number(selectedAnswer) === currentQ.correct;

  if (isCorrect) {
    correctCount++;
    streak++;

    setWarrior(ctx.warriorImg, "power");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "correct");

    // Subida de nivel cada 3 aciertos seguidos
    if (streak === 3) {
      level++;
      streak = 0;
    }
  } else {
    streak = 0;
    setWarrior(ctx.warriorImg, "sad");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "wrong");
  }

  setTimeout(() => loadQuestion(ctx), 1800);
}

// =======================
// INIT
// =======================
function init() {
  const ctx = {
    screens: {
      home: $("screen-home"),
      game: $("screen-game"),
    },
    warriorImg: $("warrior"),
    questionEl: $("question"),
    answerButtons: Array.from(document.querySelectorAll(".answer-btn")),
    answerAText: $("answer-a-text"),
    answerBText: $("answer-b-text"),
    iconCorrect: $("icon-correct"),
    iconWrong: $("icon-wrong"),
    progressText: $("progress-text"),
    levelText: $("level-text"),
  };

  $("home-next").onclick = () => {
    correctCount = 0;
    level = 1;
    streak = 0;
    currentQ = null;

    showScreen(ctx.screens, "game");
    loadQuestion(ctx);
  };

  ctx.answerButtons.forEach((btn) => {
    btn.onclick = () => {
      if (locked) return;
      ctx.answerButtons.forEach((b) =>
        b.classList.remove("is-selected")
      );
      btn.classList.add("is-selected");
      selectedAnswer = btn.dataset.value;
    };
  });

  $("btn-check").onclick = () => checkAnswer(ctx);

  showScreen(ctx.screens, "home");
}

document.addEventListener("DOMContentLoaded", init);
