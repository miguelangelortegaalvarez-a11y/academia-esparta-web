// ============================================================
// Camino Matemático — motor genérico + contenido por cursos
// El motor no sabe de operaciones: solo pide preguntas {prompt, correct, wrong}
// a un "reto". Añadir curso/reto = añadir datos en CURRICULUM.
// ============================================================

/** CONFIG **/
const GOAL = 10;          // preguntas por partida
const LEVEL_EVERY = 3;    // sube de nivel cada N aciertos
const FEEDBACK_MS = 1300; // tiempo que se ve el guerrero + icono

/** ASSETS **/
const ASSETS = {
  warrior: {
    idle:  "./assets/espartano/espartano-idle.png",
    power: "./assets/espartano/espartano-power.png",
    sad:   "./assets/espartano/espartano-sad.png",
  },
};

/** HELPERS NUMÉRICOS **/
function randInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
function shuffle2(a, b) { return Math.random() < 0.5 ? [a, b] : [b, a]; }

// Genera una respuesta incorrecta plausible y distinta de la correcta.
function wrongNear(correct, spread) {
  let w = correct;
  let guard = 0;
  while ((w === correct || w < 0) && guard++ < 50) {
    const d = randInt(-spread, spread);
    if (d === 0) continue;
    w = correct + d;
  }
  return w === correct ? correct + spread : w;
}

// ============================================================
// SONIDO (Web Audio, sin ficheros → cero peso)
// ============================================================
let audioCtx = null;
function ensureAudio() {
  try {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === "suspended") audioCtx.resume();
  } catch (e) { audioCtx = null; }
}
function beep(freq, start, dur, type = "sine", gain = 0.22) {
  if (!audioCtx) return;
  const o = audioCtx.createOscillator();
  const g = audioCtx.createGain();
  o.type = type;
  o.frequency.value = freq;
  o.connect(g); g.connect(audioCtx.destination);
  const t = audioCtx.currentTime + start;
  g.gain.setValueAtTime(0.0001, t);
  g.gain.exponentialRampToValueAtTime(gain, t + 0.02);
  g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  o.start(t); o.stop(t + dur + 0.03);
}
function playSound(kind) {
  ensureAudio();
  if (!audioCtx) return;
  if (kind === "correct")      { beep(660, 0, 0.12, "sine", 0.25); beep(880, 0.1, 0.16, "sine", 0.25); }
  else if (kind === "wrong")   { beep(196, 0, 0.24, "sawtooth", 0.16); }
  else if (kind === "win")     { [523, 659, 784, 1047].forEach((f, i) => beep(f, i * 0.13, 0.2, "triangle", 0.22)); }
}

// ============================================================
// GENERADORES DE PREGUNTAS (devuelven {prompt, correct, wrong})
// ============================================================

// — 1º —
function genSumaSinLlevar() {            // a + b, una cifra, resultado ≤ 9
  let a, b;
  do { a = randInt(1, 8); b = randInt(1, 8); } while (a + b > 9);
  const c = a + b;
  return { prompt: `${a} + ${b} = ?`, correct: c, wrong: wrongNear(c, 3) };
}
function genRestaSinLlevar() {           // a − b, resultado ≥ 0, una cifra
  const a = randInt(2, 9);
  const b = randInt(1, a);
  const c = a - b;
  return { prompt: `${a} − ${b} = ?`, correct: c, wrong: wrongNear(c, 3) };
}

// — 2º —
function genSumaLlevada() {              // DU + DU con llevada en unidades, ≤ 99
  let a, b;
  do { a = randInt(11, 79); b = randInt(11, 79); }
  while ((a % 10) + (b % 10) <= 9 || a + b > 99);
  const c = a + b;
  return { prompt: `${a} + ${b} = ?`, correct: c, wrong: wrongNear(c, 6) };
}
function genRestaPrestar() {             // DU − DU con préstamo en unidades
  let a, b;
  do { a = randInt(21, 98); b = randInt(11, a - 1); }
  while ((a % 10) >= (b % 10));          // unidad minuendo < unidad sustraendo → presta
  const c = a - b;
  return { prompt: `${a} − ${b} = ?`, correct: c, wrong: wrongNear(c, 6) };
}
function genTabla(n) {                   // tabla fija del n
  return () => {
    const b = randInt(1, 10);
    const c = n * b;
    return { prompt: `${n} × ${b} = ?`, correct: c, wrong: wrongNear(c, 6) };
  };
}
function genDoble() {                    // el doble de un número
  const a = randInt(2, 20);
  const c = a * 2;
  return { prompt: `El doble de ${a} = ?`, correct: c, wrong: wrongNear(c, 5) };
}

// — 3º —
function genTablasMezcladas() {          // tablas del 2 al 9
  const a = randInt(2, 9), b = randInt(2, 10);
  const c = a * b;
  return { prompt: `${a} × ${b} = ?`, correct: c, wrong: wrongNear(c, 8) };
}
function genMultiUnaCifra() {            // DU × U
  const a = randInt(11, 99), b = randInt(2, 9);
  const c = a * b;
  return { prompt: `${a} × ${b} = ?`, correct: c, wrong: wrongNear(c, 14) };
}
function genDivisionExacta() {           // división exacta de una cifra
  const b = randInt(2, 9), q = randInt(2, 9);
  const a = b * q;
  return { prompt: `${a} : ${b} = ?`, correct: q, wrong: wrongNear(q, 4) };
}
function genSumaCentenas() {             // CDU + CDU
  const a = randInt(120, 880), b = randInt(110, 880);
  const c = a + b;
  return { prompt: `${a} + ${b} = ?`, correct: c, wrong: wrongNear(c, 40) };
}

// — SERIES NUMÉRICAS —
// Distractor típico de serie: el término anterior o un ±1 / ±paso plausible.
function wrongSerie(correct, paso) {
  const cands = [correct + paso, correct - paso, correct + 1, correct - 1]
    .filter((w) => w >= 0 && w !== correct);
  return cands[randInt(0, cands.length - 1)];
}
function genSerieAsc(paso, min, max) {   // ascendente: a, a+p, a+2p, a+3p, ?
  return () => {
    const start = randInt(min, max);
    const seq = [start, start + paso, start + 2 * paso, start + 3 * paso];
    const correct = start + 4 * paso;
    return { prompt: `${seq.join(", ")}, ?`, correct, wrong: wrongSerie(correct, paso) };
  };
}
function genSerieDesc(paso, min, max) {  // descendente: a, a−p, a−2p, a−3p, ?  (correct ≥ 0)
  return () => {
    let start;
    do { start = randInt(min, max); } while (start - 4 * paso < 0);
    const seq = [start, start - paso, start - 2 * paso, start - 3 * paso];
    const correct = start - 4 * paso;
    return { prompt: `${seq.join(", ")}, ?`, correct, wrong: wrongSerie(correct, paso) };
  };
}

// ============================================================
// CONTENIDO POR CURSOS  ←  para crecer, solo se edita esto
// ============================================================
const CURRICULUM = {
  "1": {
    nombre: "1º Primaria",
    temas: [
      { titulo: "Sumar sin llevar",  gen: genSumaSinLlevar },
      { titulo: "Restar sin llevar", gen: genRestaSinLlevar },
      { titulo: "Series de 2 en 2",  gen: genSerieAsc(2, 0, 10) },
    ],
  },
  "2": {
    nombre: "2º Primaria",
    temas: [
      { titulo: "Sumar con llevada",  gen: genSumaLlevada },
      { titulo: "Restar con prestar", gen: genRestaPrestar },
      { titulo: "Tabla del 2",        gen: genTabla(2) },
      { titulo: "Tabla del 5",        gen: genTabla(5) },
      { titulo: "Tabla del 10",       gen: genTabla(10) },
      { titulo: "El doble",           gen: genDoble },
      { titulo: "Series de 5 en 5",   gen: genSerieAsc(5, 0, 40) },
      { titulo: "Series de 10 en 10", gen: genSerieAsc(10, 0, 50) },
    ],
  },
  "3": {
    nombre: "3º Primaria",
    temas: [
      { titulo: "Tablas mezcladas",    gen: genTablasMezcladas },
      { titulo: "Multiplicar ×1 cifra", gen: genMultiUnaCifra },
      { titulo: "Dividir exacta",      gen: genDivisionExacta },
      { titulo: "Sumar centenas",      gen: genSumaCentenas },
      { titulo: "Series de 100 en 100", gen: genSerieAsc(100, 100, 500) },
      { titulo: "Series hacia atrás",  gen: genSerieDesc(10, 50, 90) },
    ],
  },
};

// ============================================================
// ESTADO
// ============================================================
let retoActual = null;   // función generadora del reto elegido
let correctCount = 0, wrongCount = 0, doneCount = 0, level = 1, streak = 0;
let selectedAnswer = null, locked = false, currentQ = null;

const WALK_START = 14, WALK_END = 82;   // % de avance del guerrero por el camino

const $ = (id) => document.getElementById(id);

function showScreen(screens, name) {
  Object.values(screens).forEach((el) => el && el.classList.remove("is-active"));
  if (screens[name]) screens[name].classList.add("is-active");
}

function setWarrior(img, state) {
  if (!img) return;
  img.src = state === "power" ? ASSETS.warrior.power
          : state === "sad"   ? ASSETS.warrior.sad
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

function updateLevelUI(ctx) {
  level = 1 + Math.floor(correctCount / LEVEL_EVERY);
  if (ctx.levelText) ctx.levelText.textContent = `Nivel ${level}`;
}
function updateProgressUI(ctx) {
  const pct = Math.min(100, (doneCount / GOAL) * 100);
  if (ctx.progressFill) ctx.progressFill.style.width = pct + "%";
  if (ctx.progressText) ctx.progressText.textContent = `${doneCount}/${GOAL}`;
  if (ctx.progressFill && ctx.progressFill.parentElement) {
    ctx.progressFill.parentElement.classList.toggle("complete", doneCount >= GOAL);
  }
}

// El guerrero avanza por el camino según aciertos
function updateWalk(ctx) {
  if (!ctx.warriorWrap) return;
  const pos = WALK_START + (correctCount / GOAL) * (WALK_END - WALK_START);
  ctx.warriorWrap.style.left = pos + "%";
}

// Racha de aciertos
function showStreak(ctx) {
  if (!ctx.streakEl) return;
  if (streak >= 2) {
    ctx.streakEl.textContent = `🔥 ¡${streak} seguidas!`;
    ctx.streakEl.classList.add("show");
  } else {
    hideStreak(ctx);
  }
}
function hideStreak(ctx) {
  if (ctx.streakEl) ctx.streakEl.classList.remove("show");
}

// Estrellas finales según aciertos
function starsFor(correct) {
  if (correct >= 9) return 3;
  if (correct >= 7) return 2;
  if (correct >= 4) return 1;
  return 0;
}
function renderStars(ctx) {
  if (!ctx.starsEl) return;
  const n = starsFor(correctCount);
  ctx.starsEl.innerHTML = "";
  for (let i = 0; i < 3; i++) {
    const s = document.createElement("span");
    s.className = "star" + (i < n ? " on" : "");
    s.textContent = "★";
    ctx.starsEl.appendChild(s);
  }
}

// Reinicia la animación de reacción del guerrero
function animarGuerrero(ctx, clase) {
  const img = ctx.warriorImg;
  if (!img) return;
  img.classList.remove("is-correct", "is-wrong");
  void img.offsetWidth;          // fuerza reflow para reproducir de nuevo
  img.classList.add(clase);
}

function loadQuestion(ctx) {
  locked = false;
  resetSelectionUI(ctx.answerButtons);
  hideFeedback(ctx.iconCorrect, ctx.iconWrong);
  setWarrior(ctx.warriorImg, "idle");
  if (ctx.warriorImg) ctx.warriorImg.classList.remove("is-correct", "is-wrong");
  updateLevelUI(ctx);

  currentQ = retoActual();
  if (ctx.questionEl) ctx.questionEl.textContent = currentQ.prompt;

  const [optA, optB] = shuffle2(String(currentQ.correct), String(currentQ.wrong));
  if (ctx.answerButtons[0]) ctx.answerButtons[0].dataset.value = optA;
  if (ctx.answerButtons[1]) ctx.answerButtons[1].dataset.value = optB;
  if (ctx.answerAText) ctx.answerAText.textContent = optA;
  if (ctx.answerBText) ctx.answerBText.textContent = optB;

  updateProgressUI(ctx);
}

function checkAnswer(ctx) {
  if (locked || selectedAnswer === null || !currentQ) return;
  locked = true;

  const ok = Number(selectedAnswer) === Number(currentQ.correct);
  doneCount += 1;

  if (ok) {
    correctCount += 1;
    streak += 1;
    updateLevelUI(ctx);
    setWarrior(ctx.warriorImg, "power");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "correct");
    animarGuerrero(ctx, "is-correct");
    updateWalk(ctx);
    showStreak(ctx);
    playSound("correct");
  } else {
    wrongCount += 1;
    streak = 0;
    setWarrior(ctx.warriorImg, "sad");
    showFeedback(ctx.iconCorrect, ctx.iconWrong, "wrong");
    animarGuerrero(ctx, "is-wrong");
    hideStreak(ctx);
    playSound("wrong");
  }
  updateProgressUI(ctx);

  if (doneCount >= GOAL) {
    setTimeout(() => {
      updateFinalStats(ctx);
      renderStars(ctx);
      playSound("win");
      showScreen(ctx.screens, "final");
    }, FEEDBACK_MS);
    return;
  }
  setTimeout(() => loadQuestion(ctx), FEEDBACK_MS);
}

function updateFinalStats(ctx) {
  if (ctx.finalCorrect) ctx.finalCorrect.textContent = String(correctCount);
  if (ctx.finalWrong)   ctx.finalWrong.textContent   = String(wrongCount);
}

function resetRun(ctx) {
  correctCount = wrongCount = doneCount = 0;
  level = 1;
  streak = 0;
  locked = false;
  selectedAnswer = null;
  currentQ = null;
  updateLevelUI(ctx);
  updateProgressUI(ctx);
  updateWalk(ctx);
  hideStreak(ctx);
  hideFeedback(ctx.iconCorrect, ctx.iconWrong);
  setWarrior(ctx.warriorImg, "idle");
  if (ctx.warriorImg) ctx.warriorImg.classList.remove("is-correct", "is-wrong");
  if (ctx.starsEl) ctx.starsEl.innerHTML = "";
  resetSelectionUI(ctx.answerButtons);
}

function startReto(ctx, gen) {
  retoActual = gen;
  resetRun(ctx);
  showScreen(ctx.screens, "game");
  loadQuestion(ctx);
}

// ============================================================
// NAVEGACIÓN: home (cursos) → temas → juego
// ============================================================
function renderCursos(ctx) {
  ctx.cursoList.innerHTML = "";
  Object.entries(CURRICULUM).forEach(([key, curso]) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "menu-btn";
    btn.textContent = curso.nombre;
    btn.addEventListener("click", () => openCurso(ctx, key));
    ctx.cursoList.appendChild(btn);
  });
}

function openCurso(ctx, key) {
  const curso = CURRICULUM[key];
  if (!curso) return;
  ctx.temasTitle.textContent = curso.nombre;
  ctx.temaList.innerHTML = "";
  curso.temas.forEach((tema) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "menu-btn";
    btn.textContent = tema.titulo;
    btn.addEventListener("click", () => startReto(ctx, tema.gen));
    ctx.temaList.appendChild(btn);
  });
  showScreen(ctx.screens, "temas");
}

// ============================================================
// INIT
// ============================================================
function init() {
  const ctx = {
    screens: { home: $("screen-home"), temas: $("screen-temas"), game: $("screen-game"), final: $("screen-final") },
    cursoList: $("curso-list"),
    temaList: $("tema-list"),
    temasTitle: $("temas-title"),
    warriorImg: $("warrior"),
    warriorWrap: $("warrior-wrap"),
    streakEl: $("streak"),
    starsEl: $("stars"),
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
  };

  renderCursos(ctx);
  resetRun(ctx);
  showScreen(ctx.screens, "home");

  // Respuestas (auto-resuelve al tocar)
  ctx.answerButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      ensureAudio();          // desbloquea el sonido en el primer toque
      if (locked) return;
      ctx.answerButtons.forEach((b) => b.classList.remove("is-selected"));
      btn.classList.add("is-selected");
      selectedAnswer = btn.dataset.value ?? null;
      checkAnswer(ctx);
    });
  });

  // Navegación atrás
  $("temas-back") && $("temas-back").addEventListener("click", () => showScreen(ctx.screens, "home"));
  $("game-back")  && $("game-back").addEventListener("click", () => showScreen(ctx.screens, "temas"));

  // Final
  $("final-retry") && $("final-retry").addEventListener("click", () => startReto(ctx, retoActual));
  $("final-menu")  && $("final-menu").addEventListener("click",  () => showScreen(ctx.screens, "temas"));
}

document.addEventListener("DOMContentLoaded", () => {
  try { init(); } catch (e) { console.error("Error iniciando el juego:", e); }
});
