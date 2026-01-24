/* ==========================================================
   CUENTO PIRATA MARIO — SCRIPT DEFINITIVO
   Autor: Academia Esparta
   Compatible iPad / Safari / Offline
   ========================================================== */

(() => {
  "use strict";

  /* =========================
     CONFIGURACIÓN
  ========================= */

  const FLOW = [1, 2, 3, 4, "interlude", 5, 6, 7, 8];

  const ASSETS = {
    bg: {
      1: "./assets/images/ESCENA_01_BIENVENIDA_MAPA.PNG",
      2: "./assets/images/ESCENA_02_PLAYA.PNG",
      3: "./assets/images/ESCENA_03_BOSQUE.PNG",
      4: "./assets/images/ESCENA_04_PUENTE.PNG",
      interlude: "./assets/images/ESCENA_04_PUENTE.PNG",
      5: "./assets/images/ESCENA_05_CUEVA.PNG",
      6: "./assets/images/ESCENA_06_MONTANA_COFRES.PNG",
      7: "./assets/images/ESCENA_07_MONTANA_SILABAS.PNG",
      8: "./assets/images/ESCENA_08_FINAL.PNG"
    },
    objects: {
      key: "./assets/objects/OBJ_LLAVE.PNG",
      chestClosed: "./assets/objects/COFRE_CERRADO.PNG",
      chestOpen: "./assets/objects/COFRE_ABIERTO.PNG"
    },
    audio: {
      bgm: "./assets/audio/MUSICA_PIRATAS_FONDO.mp3"
    }
  };

  const INSTRUCTIONS = {
    1: "",
    2: "Arrastra la letra correcta.",
    3: "Encuentra 5 llaves y arrástralas al cofre.",
    4: "Coloca cada objeto en su sitio.",
    interlude: "",
    5: "Observa, memoriza y coloca.",
    6: "Cuenta las monedas.",
    7: "Cuenta las sílabas.",
    8: ""
  };

  /* =========================
     HELPERS
  ========================= */

  const $ = s => document.querySelector(s);
  const $$ = s => Array.from(document.querySelectorAll(s));

  function show(el){ el && (el.hidden = false); }
  function hide(el){ el && (el.hidden = true); }

  function setInstruction(id){
    const el = $("#instruction");
    if(el) el.textContent = INSTRUCTIONS[id] || "";
  }

  function setBackground(id){
    const bg = $("#sceneBg");
    if(!bg) return;
    bg.style.backgroundImage = `url("${ASSETS.bg[id]}")`;
  }

  function activateScreen(id){
    $$(".screen").forEach(s => s.classList.remove("is-active"));
    const target = id === "interlude"
      ? $("#screen-interlude")
      : $(`#screen-${id}`);
    if(target) target.classList.add("is-active");
    setInstruction(id);
    setBackground(id);
  }

  let flowIndex = 0;
  function nextScreen(){
    flowIndex = Math.min(flowIndex + 1, FLOW.length - 1);
    activateScreen(FLOW[flowIndex]);
  }

  function restart(){
    flowIndex = 0;
    activateScreen(1);
    initScreen3(); // reinicia llaves
  }

  /* =========================
     MÚSICA
  ========================= */

  function setupMusic(){
    const bgm = $("#bgm");
    const btn = $("#btnMusic");
    if(!bgm) return;

    bgm.src = ASSETS.audio.bgm;
    bgm.loop = true;

    bgm.play().catch(() => {
      if(btn) btn.hidden = false;
    });

    btn && btn.addEventListener("click", () => {
      bgm.play().then(() => btn.hidden = true);
    });
  }

  /* =========================
     SCREEN 1
  ========================= */

  function initScreen1(){
    const btn = $("#btnStart");
    btn && btn.addEventListener("click", nextScreen);
  }

  /* =========================
     SCREEN 3 — LLAVES (ESTABLE)
  ========================= */

  function initScreen3(){
    const layer = $("#keysLayer");
    const chest = $("#chestDrop");
    const chestImg = $("#chestImg");
    const btnNext = $("#btnNext3");

    if(!layer || !chest) return;

    layer.innerHTML = "";
    let collected = 0;
    btnNext.disabled = true;

    for(let i=0;i<5;i++){
      const key = document.createElement("img");
      key.src = ASSETS.objects.key;
      key.className = "key-item";
      key.style.left = `${15 + i*12}%`;
      key.style.top = `${20 + (i%2)*20}%`;
      key.draggable = true;

      key.addEventListener("dragend", e => {
        const rect = chest.getBoundingClientRect();
        if(
          e.clientX > rect.left &&
          e.clientX < rect.right &&
          e.clientY > rect.top &&
          e.clientY < rect.bottom
        ){
          key.remove();
          collected++;
          if(collected === 5){
            chestImg.src = ASSETS.objects.chestOpen;
            btnNext.disabled = false;
          }
        }
      });

      layer.appendChild(key);
    }

    btnNext.addEventListener("click", nextScreen);
  }

  /* =========================
     SCREEN 4 — CLASIFICAR
     (AL COMPLETAR → INTERLUDE)
  ========================= */

  function initScreen4(){
    const btnNext = $("#btnNext4");
    btnNext && btnNext.addEventListener("click", () => {
      flowIndex = FLOW.indexOf("interlude");
      activateScreen("interlude");
    });
  }

  /* =========================
     INTERLUDE
  ========================= */

  function initInterlude(){
    const btn = $("#btnInterludeNext");
    btn && btn.addEventListener("click", nextScreen);
  }

  /* =========================
     SCREEN 8
  ========================= */

  function initScreen8(){
    const btn = $("#btnRestart");
    btn && btn.addEventListener("click", restart);
  }

  /* =========================
     BOOT
  ========================= */

  document.addEventListener("DOMContentLoaded", () => {
    setupMusic();
    initScreen1();
    initScreen3();
    initScreen4();
    initInterlude();
    initScreen8();
    activateScreen(1);
  });

})();
