// =======================
// Camino Matemático - script.js (estable en iPad / sin btn-next)
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

// Estado interacción
let selectedAnswer = null;
let locked = false;

// Assets (ojo: según tus capturas, los warrior tienen doble extensión .png.PNG)
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

function updateEnergyUI(energyText, energyFillImg, value) {
  if (energyText) energyText.textContent = String(value);

  // Con tu CSS actual, lo más robusto es controlar el ancho del propio <img>
  // (va dentro de un contenedor con overflow hidden)
  if (energyFillImg) {
    energyFillImg.style.width = `${value}%`;
  }
}

function currentQuestion() {
  return QUESTIONS[currentIndex % QUESTIONS.length];
}

function resetSelectionUI(answerButtons) {
  selectedAnswer = null;
  answerButtons.forEach((btn) => btn.classList.remove("is-selected"));
}

function loadQuestion(ctx) {
  locked = false;
  resetSelectionUI(ctx.answerButtons);
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
}

function checkAnswer(ctx) {
  if (locked) return;
  if (selectedAnswer === null) return;

  locked = true;

  const q = currentQuestion();
  const isCorrect = Number(selectedAnswer) === Number(q.correct);

  if (isCorrect) {
    setWarrior(ctx.warriorImg, "power");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "correct");
    energy = clamp(energy + 10, 0, 100);
    updateEnergyUI(ctx.energyText, ctx.energyFillImg, energy);
  } else {
    setWarrior(ctx.warriorImg, "sad");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "wrong");
  }

  // Si llega a 100 => final
  if (energy >= 100) {
    setTimeout(() => showScreen(ctx.screens, "final"), 600);
    return;
  }

  // Pasar a la siguiente pregunta automáticamente (sin botón extra)
  setTimeout(() => {
    currentIndex += 1;
    loadQuestion(ctx);
  }, 700);
}

function init() {
  // Pantallas
  const screens = {
    home: $("screen-home"),
    game: $("screen-game"),
    final: $("screen-final"),
  };

  // Botones
  const btnHomeNext = $("home-next");
  const btnCheck = $("btn-check");
  const btnFinalRetry = $("final-retry");

  // Juego
  const warriorImg = $("warrior");
  const questionEl = $("question");

  const answerButtons = Array.from(document.querySelectorAll(".answer-btn"));
  const answerAText = $("answer-a-text");
  const answerBText = $("answer-b-text");

  const iconCorrect = $("icon-correct");
  const iconWrong = $("icon-wrong");

  const energyText = $("energy-text");
  const energyFillImg = $("energy-fill");

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
    energyText,
    energyFillImg,
  };

  // Estado inicial
  energy = 0;
  currentIndex = 0;
  updateEnergyUI(energyText, energyFillImg, energy);
  setWarrior(warriorImg, "idle");
  hideFeedback(iconCorrect, iconWrong);
  showScreen(screens, "home");

  // HOME -> GAME
  if (btnHomeNext) {
    btnHomeNext.addEventListener("click", () => {
      showScreen(screens, "game");
      energy = 0;
      currentIndex = 0;
      updateEnergyUI(energyText, energyFillImg, energy);
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

  // FINAL -> HOME
  if (btnFinalRetry) {
    btnFinalRetry.addEventListener("click", () => {
      energy = 0;
      currentIndex = 0;
      locked = false;
      selectedAnswer = null;

      updateEnergyUI(energyText, energyFillImg, energy);
      hideFeedback(iconCorrect, iconWrong);
      setWarrior(warriorImg, "idle");
      resetSelectionUI(answerButtons);
      showScreen(screens, "home");
    });
  }
}

// Arranque seguro (iPad/Safari)
document.addEventListener("DOMContentLoaded", () => {
  try {
    init();
  } catch (e) {
    console.error("Error iniciando el juego:", e);
  }
});
