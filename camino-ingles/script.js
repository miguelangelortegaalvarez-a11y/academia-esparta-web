// =======================
// Camino Inglés — script.js
// AM / IS / ARE
// =======================

// Banco de preguntas INGLÉS
const QUESTIONS = [
  { prompt: "I ___ happy.", correct: "am", wrong: "is" },
  { prompt: "He ___ my brother.", correct: "is", wrong: "are" },
  { prompt: "They ___ at school.", correct: "are", wrong: "is" },
  { prompt: "She ___ a teacher.", correct: "is", wrong: "am" },
  { prompt: "We ___ friends.", correct: "are", wrong: "is" },
  { prompt: "I ___ ready.", correct: "am", wrong: "are" },
  { prompt: "He ___ tall.", correct: "is", wrong: "am" },
  { prompt: "They ___ happy.", correct: "are", wrong: "is" },
];

let currentQ = null;
let selectedAnswer = null;
let locked = false;
let correctCount = 0;
const GOAL = 10;

// Assets
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

function resetSelectionUI(btns) {
  selectedAnswer = null;
  btns.forEach((b) => b.classList.remove("is-selected"));
}

function randomQuestion() {
  return QUESTIONS[Math.floor(Math.random() * QUESTIONS.length)];
}

function loadQuestion(ctx) {
  locked = false;
  resetSelectionUI(ctx.answerButtons);
  hideFeedback(ctx.iconCorrect, ctx.iconWrong);
  setWarrior(ctx.warriorImg, "idle");

  currentQ = randomQuestion();

  if (ctx.questionEl)
    ctx.questionEl.textContent = currentQ.prompt;

  const options = [currentQ.correct, currentQ.wrong].sort(
    () => Math.random() - 0.5
  );

  ctx.answerButtons[0].dataset.value = options[0];
  ctx.answerButtons[1].dataset.value = options[1];

  ctx.answerAText.textContent = options[0];
  ctx.answerBText.textContent = options[1];

  updateProgress(ctx);
}

function updateProgress(ctx) {
  const pct = Math.min(100, (correctCount / GOAL) * 100);
  ctx.progressFill.style.width = pct + "%";
  ctx.progressText.textContent = `${correctCount}/${GOAL}`;
}

function checkAnswer(ctx) {
  if (locked || selectedAnswer === null) return;
  locked = true;

  const ok = selectedAnswer === currentQ.correct;

  if (ok) {
    correctCount++;
    setWarrior(ctx.warriorImg, "power");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "correct");

    if (correctCount >= GOAL) {
      ctx.progressFill.parentElement.classList.add("complete");
      showScreen(ctx.screens, "final");
      return;
    }
  } else {
    setWarrior(ctx.warriorImg, "sad");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "wrong");
  }

  setTimeout(() => loadQuestion(ctx), 1500);
}

function init() {
  const ctx = {
    screens: {
      home: $("screen-home"),
      game: $("screen-game"),
      final: $("screen-final"),
    },
    warriorImg: $("warrior"),
    questionEl: $("question"),
    answerButtons: Array.from(document.querySelectorAll(".answer-btn")),
    answerAText: $("answer-a-text"),
    answerBText: $("answer-b-text"),
    iconCorrect: $("icon-correct"),
    iconWrong: $("icon-wrong"),
    progressFill: $("progress-fill"),
    progressText: $("progress-text"),
  };

  $("home-next").onclick = () => {
    correctCount = 0;
    ctx.progressFill.parentElement.classList.remove("complete");
    showScreen(ctx.screens, "game");
    loadQuestion(ctx);
  };

  ctx.answerButtons.forEach((btn) => {
    btn.onclick = () => {
      if (locked) return;
      ctx.answerButtons.forEach((b) => b.classList.remove("is-selected"));
      btn.classList.add("is-selected");
      selectedAnswer = btn.dataset.value;
    };
  });

  $("btn-check").onclick = () => checkAnswer(ctx);

  $("final-retry").onclick = () => {
    correctCount = 0;
    showScreen(ctx.screens, "home");
  };

  showScreen(ctx.screens, "home");
}

document.addEventListener("DOMContentLoaded", init);
