// =======================
// Camino Inglés — script.js
// AM / IS / ARE
// =======================


// ========================
// Banco de ejercicios INGLÉS (10–11 años)
// Tipos mezclados: AM/IS/ARE, HAVE/HAS, DO/DOES, PAST (was/were), PREPOSITIONS, PLURALS
// ========================

const QUESTIONS = [
  // 1) AM / IS / ARE
  { type: "am_is_are", prompt: "I ___ hungry.", correct: "am", wrong: "is" },
  { type: "am_is_are", prompt: "She ___ at home.", correct: "is", wrong: "are" },
  { type: "am_is_are", prompt: "They ___ friends.", correct: "are", wrong: "is" },

  // 2) HAVE / HAS
  { type: "have_has", prompt: "He ___ a new bike.", correct: "has", wrong: "have" },
  { type: "have_has", prompt: "We ___ two dogs.", correct: "have", wrong: "has" },

  // 3) DO / DOES (present simple questions)
  { type: "do_does", prompt: "___ you like pizza?", correct: "Do", wrong: "Does" },
  { type: "do_does", prompt: "___ she play tennis?", correct: "Does", wrong: "Do" },

  // 4) WAS / WERE (past of to be)
  { type: "was_were", prompt: "I ___ tired yesterday.", correct: "was", wrong: "were" },
  { type: "was_were", prompt: "They ___ at the park.", correct: "were", wrong: "was" },

  // 5) PREPOSITIONS (in / on / at)
  { type: "prepositions", prompt: "My birthday is ___ July.", correct: "in", wrong: "on" },
  { type: "prepositions", prompt: "The book is ___ the table.", correct: "on", wrong: "in" },
  { type: "prepositions", prompt: "We meet ___ 5 o'clock.", correct: "at", wrong: "in" },

  // 6) PLURALS (s / es)
  { type: "plurals", prompt: "One box, two ___.", correct: "boxes", wrong: "boxs" },
  { type: "plurals", prompt: "One baby, two ___.", correct: "babies", wrong: "babys" },
];
// Pool de preguntas (para que no se repitan)
let questionPool = [];

// Mezclar array (Fisher-Yates)
function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

// Obtener siguiente pregunta sin repetir
function getNextQuestion() {
  if (questionPool.length === 0) {
    questionPool = shuffle([...QUESTIONS]);
  }
  return questionPool.pop();
}

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

  currentQ = getNextQuestion();

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
      setTimeout(() => loadQuestion(ctx), 1500);
    }
  } else {
    setWarrior(ctx.warriorImg, "sad");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "wrong");
    setTimeout(() => loadQuestion(ctx), 1500);
  }

  
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
