// =======================
// Camino Matemático — script.js (MODOS + PROGRESO + NIVELES)
// mode = "sumas" | "restas" | "multiplicaciones"
// =======================

/** CONFIG **/
const GOAL = 15;              // <-- Meta total de aciertos (cámbialo a 10 si quieres "prueba" corta)
const LEVEL_EVERY = 3;        // <-- Cada cuántos aciertos sube el nivel
const FEEDBACK_MS = 1500;     // <-- Tiempo que se ve el warrior + icono (ms)

/** ESTADO **/
let mode = null;              // "sumas" | "multiplicaciones"
let correctCount = 0;
let level = 1;
let wrongCount = 0;
let doneCount = 0; // ✅ preguntas hechas (acierto o fallo)

let selectedAnswer = null;
let locked = false;
let currentQ = null;

/** ASSETS **/
const ASSETS = {
  warrior: {
    idle: "./assets/warrior/warrior-idle.png.PNG",
    power: "./assets/warrior/warrior-power.png.PNG",
    sad: "./assets/warrior/warrior-sad.png.PNG",
  },
};

/** HELPERS **/
function $(id) { return document.getElementById(id); }

function showScreen(screens, name) {
  Object.values(screens).forEach((el) => el && el.classList.remove("is-active"));
  screens[name] && screens[name].classList.add("is-active");
}

function setWarrior(img, state) {
  if (!img) return;
  img.src =
    state === "power" ? ASSETS.warrior.power :
    state === "sad" ? ASSETS.warrior.sad :
    ASSETS.warrior.idle;
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

function clamp(n, a, b) { return Math.max(a, Math.min(b, n)); }

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function shuffle2(a, b) {
  return Math.random() < 0.5 ? [a, b] : [b, a];
}

/** NIVEL Y DIFICULTAD **/
function computeLevelFromScore(score) {
  return 1 + Math.floor(score / LEVEL_EVERY);
}

function updateLevelUI(ctx) {
  level = computeLevelFromScore(correctCount);
  if (ctx.levelText) ctx.levelText.textContent = `Nivel ${level}`;
}

function updateProgressUI(ctx) {
  const pct = Math.min(100, (doneCount / GOAL) * 100);
  if (ctx.progressFill) ctx.progressFill.style.width = pct + "%";
  if (ctx.progressText) ctx.progressText.textContent = `${doneCount}/${GOAL}`;

  // Dorado cuando completa
  if (ctx.progressFill && ctx.progressFill.parentElement) {
    if (doneCount >= GOAL) ctx.progressFill.parentElement.classList.add("complete");
    else ctx.progressFill.parentElement.classList.remove("complete");
  }
}

/** GENERADOR DE PREGUNTAS **/
function makeQuestionSumasRestas(level) {
  // SOLO SUMAS
  // Números de una sola cifra (0–9)
  // Resultado máximo: 18

  let a = randInt(0, 9);
  let b = randInt(0, 9);

  // Forzar que la suma no pase de 18
  while (a + b > 18) {
    a = randInt(0, 9);
    b = randInt(0, 9);
  }

  const correct = a + b;

  let wrong = correct;
  while (wrong === correct || wrong < 0 || wrong > 18) {
    const delta = randInt(-3, 3);
    if (delta === 0) continue;
    wrong = correct + delta;
  }

  return {
    a,
    b,
    op: "+",
    correct,
    wrong
  };
}
function makeQuestionRestas(level) {
  // RESTAS simples
  // Un solo dígito
  // Resultado SIEMPRE entre 0 y 9

  let a = randInt(0, 9);
  let b = randInt(0, 9);

  // Asegurar:
  // - a >= b (no negativos)
  // - resultado < 10
  while (a < b || (a - b) >= 10) {
    a = randInt(0, 9);
    b = randInt(0, 9);
  }

  const correct = a - b;

  let wrong = correct;
  while (wrong === correct || wrong < 0 || wrong >= 10) {
    const delta = randInt(-3, 3);
    if (delta === 0) continue;
    wrong = correct + delta;
  }

  return {
    a,
    b,
    op: "−",
    correct,
    wrong
  };
}
function makeQuestionMultiplicaciones(level) {
  // Tablas: nivel 1 (0-5), nivel 2 (0-7), nivel 3 (0-9), nivel 4 (0-10), etc.
  const max = clamp(5 + (level - 1) * 2, 5, 12);
  const a = randInt(0, max);
  const b = randInt(0, max);
  const op = "×";
  const correct = a * b;

  let wrong = correct;
  while (wrong === correct || wrong < 0) {
    const delta = randInt(-10, 10);
    if (delta === 0) continue;
    wrong = correct + delta;
  }

  return { a, b, op, correct, wrong };
}
function makeQuestionTabla(n) {
  // Tabla fija: n × b (b de 0 a 10)
  const a = n;
  const b = randInt(0, 10);
  const op = "×";
  const correct = a * b;

  let wrong = correct;
  while (wrong === correct || wrong < 0) {
    const delta = randInt(-10, 10);
    if (delta === 0) continue;
    wrong = correct + delta;
  }

  return { a, b, op, correct, wrong };
}

function makeQuestionMultiMix() {
  // Mezcladas: tablas del 2 al 9, multiplicador 0 a 10
  const a = randInt(2, 9);
  const b = randInt(0, 10);
  const op = "×";
  const correct = a * b;

  let wrong = correct;
  while (wrong === correct || wrong < 0) {
    const delta = randInt(-10, 10);
    if (delta === 0) continue;
    wrong = correct + delta;
  }

  return { a, b, op, correct, wrong };
}
function makeQuestion() {
  // Multiplicaciones por tabla fija (2–9)
  if (mode === "tabla2") return makeQuestionTabla(2);
  if (mode === "tabla3") return makeQuestionTabla(3);
  if (mode === "tabla4") return makeQuestionTabla(4);
  if (mode === "tabla5") return makeQuestionTabla(5);
  if (mode === "tabla6") return makeQuestionTabla(6);
  if (mode === "tabla7") return makeQuestionTabla(7);
  if (mode === "tabla8") return makeQuestionTabla(8);
  if (mode === "tabla9") return makeQuestionTabla(9);

  // Multiplicaciones mezcladas (tablas 2–9)
  if (mode === "multi_mix") return makeQuestionMultiMix();

  // Modos ya existentes
  if (mode === "multiplicaciones") return makeQuestionMultiplicaciones(level); // (si lo sigues usando)
  if (mode === "restas") return makeQuestionRestas(level);

  // Por defecto: sumas
  return makeQuestionSumasRestas(level);
}

/** CARGAR PREGUNTA **/
function loadQuestion(ctx) {
  locked = false;
  currentQ = null;

  resetSelectionUI(ctx.answerButtons);
  hideFeedback(ctx.iconCorrect, ctx.iconWrong);
  setWarrior(ctx.warriorImg, "idle");

  updateLevelUI(ctx);

  currentQ = makeQuestion();

  if (ctx.questionEl) {
    ctx.questionEl.textContent = `${currentQ.a} ${currentQ.op} ${currentQ.b} = ?`;
  }

  const [optA, optB] = shuffle2(String(currentQ.correct), String(currentQ.wrong));

  if (ctx.answerButtons[0]) ctx.answerButtons[0].dataset.value = optA;
  if (ctx.answerButtons[1]) ctx.answerButtons[1].dataset.value = optB;

  if (ctx.answerAText) ctx.answerAText.textContent = optA;
  if (ctx.answerBText) ctx.answerBText.textContent = optB;

  updateProgressUI(ctx);
}

/** CHECK **/
function checkAnswer(ctx) {
  if (locked) return;
  if (selectedAnswer === null) return;

  locked = true;

  const ok = Number(selectedAnswer) === Number(currentQ.correct);
    doneCount += 1;       // ✅ una pregunta hecha (acierto o fallo)

  if (ok) {
    correctCount += 1;
    updateLevelUI(ctx);
    updateProgressUI(ctx);

    setWarrior(ctx.warriorImg, "power");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "correct");

    // ✅ Fin tras 15 preguntas (aciertos + fallos)
if (doneCount >= GOAL) {
  setTimeout(() => {
    updateFinalStats(ctx);
    showScreen(ctx.screens, "final");
  }, FEEDBACK_MS);
  return;
}
  } else {
    wrongCount += 1;
    setWarrior(ctx.warriorImg, "sad");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "wrong");
  }

  setTimeout(() => {
    loadQuestion(ctx);
  }, FEEDBACK_MS);
}
function updateFinalStats(ctx) {
  if (ctx.finalCorrect) ctx.finalCorrect.textContent = String(correctCount);
  if (ctx.finalWrong) ctx.finalWrong.textContent = String(wrongCount);
}
/** RESET DE PARTIDA **/
function resetRun(ctx) {
  correctCount = 0;
  level = 1;
  wrongCount = 0;
    doneCount = 0;
    if (ctx.finalCorrect) ctx.finalCorrect.textContent = "0";
  if (ctx.finalWrong) ctx.finalWrong.textContent = "0";
  locked = false;
  selectedAnswer = null;
  currentQ = null;

  updateLevelUI(ctx);
  updateProgressUI(ctx);
  hideFeedback(ctx.iconCorrect, ctx.iconWrong);
  setWarrior(ctx.warriorImg, "idle");
  resetSelectionUI(ctx.answerButtons);

  // quitar dorado si estaba
  if (ctx.progressFill && ctx.progressFill.parentElement) {
    ctx.progressFill.parentElement.classList.remove("complete");
  }
}

/** INIT **/
function init() {
  const ctx = {
    screens: {
      home: $("screen-home"),
      game: $("screen-game"),
      final: $("screen-final"),
    },
    warriorImg: $("warrior"),
    questionEl: $("question"),
    levelText: $("level-text"),

    answerButtons: Array.from(document.querySelectorAll(".answer-btn")),
    answerAText: $("answer-a-text"),
    answerBText: $("answer-b-text"),

    iconCorrect: $("icon-correct"),
    iconWrong: $("icon-wrong"),

    progressFill: $("progress-fill"),
    progressText: $("progress-text"),
    finalCorrect: $("final-correct"),
    finalWrong: $("final-wrong"),

    // Botones HOME
// Botones HOME
btnModeSumas: $("home-mode-sumas"),
btnModeRestas: $("home-mode-restas"),

btnModeTabla2: $("home-mode-tabla2"),
btnModeTabla3: $("home-mode-tabla3"),
btnModeTabla4: $("home-mode-tabla4"),
btnModeTabla5: $("home-mode-tabla5"),
btnModeTabla6: $("home-mode-tabla6"),
btnModeTabla7: $("home-mode-tabla7"),
btnModeTabla8: $("home-mode-tabla8"),
btnModeTabla9: $("home-mode-tabla9"),

btnModeMultiMix: $("home-mode-multi-mix"),

    // Botones comunes
    btnRetry: $("final-retry"),
  };

  // Estado inicial
  mode = null;
  resetRun(ctx);
  showScreen(ctx.screens, "home");

   // HOME -> GAME (Sumas)
if (ctx.btnModeSumas) {
  ctx.btnModeSumas.addEventListener("click", () => {
    mode = "sumas";
    resetRun(ctx);
    showScreen(ctx.screens, "game");
    loadQuestion(ctx);
  });
}
// HOME -> GAME (Restas)
if (ctx.btnModeRestas) {
  ctx.btnModeRestas.addEventListener("click", () => {
    mode = "restas";
    resetRun(ctx);
    showScreen(ctx.screens, "game");
    loadQuestion(ctx);
  });
}
  
  // HOME -> GAME (Multiplicaciones)
  if (ctx.btnModeMultiplicaciones) {
    ctx.btnModeMultiplicaciones.addEventListener("click", () => {
      mode = "multiplicaciones";
      resetRun(ctx);
      showScreen(ctx.screens, "game");
      loadQuestion(ctx);
    });
  }
// Selección respuestas (auto-resuelve al tocar)
ctx.answerButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (locked) return;

    ctx.answerButtons.forEach((b) => b.classList.remove("is-selected"));
    btn.classList.add("is-selected");
    selectedAnswer = btn.dataset.value ?? null;

    // ✅ Resolver automáticamente al tocar
    checkAnswer(ctx);
  });
});


  // FINAL -> HOME
  if (ctx.btnRetry) {
    ctx.btnRetry.addEventListener("click", () => {
      mode = null;
      resetRun(ctx);
      showScreen(ctx.screens, "home");
    });
  }
}

document.addEventListener("DOMContentLoaded", () => {
  try { init(); }
  catch (e) { console.error("Error iniciando el juego:", e); }
});
