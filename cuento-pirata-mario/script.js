/* ==========================================================
   CUENTO PIRATA MARIO — Juego educativo 4 años (SPA)
   - Sin frameworks. Offline. GitHub Pages.
   - 8 pantallas + interlude.
   - Música única en loop (autoplay con fallback).
   - Robusto ante assets faltantes.
   - Interacción táctil (iPad): drag por Pointer Events + fallback por tap.

   Autor: Academia Esparta
   ========================================================== */

(() => {
  "use strict";

  /* =========================
     CONFIG
  ========================= */

  const ASSETS = {
    bg: {
      1: "./assets/images/ESCENA_01_BIENVENIDA_MAPA.PNG",
      2: "./assets/images/ESCENA_02_PLAYA.PNG",
      3: "./assets/images/ESCENA_03_BOSQUE.PNG",
      4: "./assets/images/ESCENA_04_PUENTE.PNG",
      // Interlude usa el mismo fondo que la 4 (puedes cambiarlo si quieres)
      interlude: "./assets/images/ESCENA_04_PUENTE.PNG",
      5: "./assets/images/ESCENA_05_CUEVA.PNG",
      6: "./assets/images/ESCENA_06_MONTANA_COFRES.PNG",
      7: "./assets/images/ESCENA_07_MONTANA_SILABAS.PNG",
      8: "./assets/images/ESCENA_08_FINAL.PNG",
    },
    objects: {
      telescope: "./assets/objects/OBJ_CATALEJO.PNG",
      sword: "./assets/objects/OBJ_ESPADA.PNG",
      flag: "./assets/objects/OBJ_BANDERA_PIRATA.PNG",
      cannon: "./assets/objects/CANON_PIRATA.PNG",
      ball: "./assets/objects/OBJ_PELOTA.PNG",
      plush: "./assets/objects/OBJ_PELUCHE.PNG",
      key: "./assets/objects/OBJ_LLAVE.PNG",
      chestClosed: "./assets/objects/COFRE_CERRADO.PNG",
      chestOpen: "./assets/objects/COFRE_ABIERTO.PNG",
      coin: "./assets/objects/MONEDA_ORO.PNG",
    },
   audio: {
  bgm: "./assets/audio/MUSICA_PIRATAS_FONDO.mp3",
  intro1: "./assets/audio/INTRO_PANTALLA1.mp3",
},
  };

  const INSTRUCTIONS = {
    1: "",
    2: "Mira bien: falta la primera letra. Pulsa la letra correcta.",
    3: "Encuentra 5 llaves y púlsalas.",
    4: "Arrastra los objetos PIRATAS hacia los niños piratas.",
    interlude: "",
    5: "Mira el orden. Memoriza… y colócalo igual.",
    6: "Arrastra monedas a cada cofre: 3, 5 y 6.",
    7: "Cuenta las sílabas y elige la opción correcta.",
    8: "",
  };

  const SETTINGS = {
    memoryPreviewMs: 2500,
    fadeMs: 350,
    keyCount: 5,
    coinsTargets: [3, 5, 6],
     bgmVolume: 0.18,          // volumen normal música
voiceVolume: 1.0,         // volumen voz/instrucciones
duckBgmWhileVoice: 0.06,  // música mientras habla la voz

    // Actividad 1
    letters: [
      { id: "w1", solution: "M" }, // MAPA
      { id: "w2", solution: "P" }, // PIRATA
      { id: "w3", solution: "T" }, // TESORO
      { id: "w4", solution: "B" }, // BARCO
      { id: "w5", solution: "I" }, // ISLA
      { id: "w6", solution: "C" }, // COFRE
      { id: "w7", solution: "B" }, // BANDERA
    ],

    // Actividad 7
    syllables: [
      { word: "MAPA", answer: 2 },
      { word: "PIRATA", answer: 3 },
      { word: "TESORO", answer: 3 },
    ],

    // Actividad 4 (clasificar)
    classify: {
      pirates: ["telescope", "sword", "flag", "cannon"],
      explorers: ["ball", "plush"],
    },

    // Actividad 5 (memoria)
    memoryOrder: ["telescope", "sword", "flag"],
  };

  /* =========================
     HELPERS (DOM)
  ========================= */

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  function clamp(n, min, max) {
    return Math.max(min, Math.min(max, n));
  }

  function safeText(el, text) {
    if (!el) return;
    el.textContent = text ?? "";
  }

  function show(el) {
    if (!el) return;
    el.hidden = false;
  }

  function hide(el) {
    if (!el) return;
    el.hidden = true;
  }
function playOneShot(url, onEnd) {
  const a = new Audio(url);
   // Volumen de audios de instrucciones/intro (0.0 a 1.0)
a.volume = 1.0; // máximo
  a.preload = "auto";
  a.playsInline = true;

  a.addEventListener("ended", () => onEnd?.(), { once: true });
  a.addEventListener("error", () => {
    reportMissing(url);
    onEnd?.(); // si falla el audio, desbloqueamos igualmente
  }, { once: true });

  // iOS: solo reproduce tras gesto del usuario (click/tap)
  a.play().catch(() => {
    // si iOS bloquea por algún motivo, desbloqueamos igualmente
    onEnd?.();
  });

  return a;
}
  function disable(btn, state) {
    if (!btn) return;
    btn.disabled = !!state;
  }

  function toast(msg, ms = 900) {
    const t = $("#toast");
    if (!t) return;
    t.hidden = false;
    t.textContent = msg;
    clearTimeout(toast._tm);
    toast._tm = setTimeout(() => {
      t.hidden = true;
      t.textContent = "";
    }, ms);
  }

  function bigCheck(ms = 700) {
    const el = $("#bigCheck");
    if (!el) return;
    el.hidden = false;
    clearTimeout(bigCheck._tm);
    bigCheck._tm = setTimeout(() => (el.hidden = true), ms);
  }

  function reportMissing(url) {
    const fb = $("#assetFallback");
    if (!fb) return;
    fb.hidden = false;
    fb.textContent = `FALTA RECURSO: ${url}`;
    console.error("FALTA RECURSO:", url);
  }

  /* =========================
     ASSET FALLBACKS
  ========================= */

  function setBgWithFallback(bgEl, url) {
    if (!bgEl) return;

    const img = new Image();
    img.onload = () => {
      bgEl.style.backgroundImage = `url("${url}")`;
    };
    img.onerror = () => {
      reportMissing(url);
      bgEl.style.backgroundImage = "none";
      bgEl.style.background = "linear-gradient(135deg, #0b1220, #12324a)";
    };
    img.src = url;
  }

  function imgEl(src, alt) {
    const img = document.createElement("img");
    img.src = src;
    img.alt = alt || "";
    img.draggable = false;
    img.addEventListener("error", () => {
      reportMissing(src);
      img.src =
        "data:image/svg+xml;charset=utf-8," +
        encodeURIComponent(
          `<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160">
            <rect width="100%" height="100%" fill="#ddd"/>
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#666" font-size="14">IMG</text>
          </svg>`
        );
    });
    return img;
  }

  /* =========================
     POINTER DRAG (iPad-friendly)
     IMPORTANTE:
     - NO movemos el elemento si solo “toca y suelta”.
     - Solo empezamos drag si se desplaza > umbral.
  ========================= */

  class PointerDrag {
    constructor() {
      this.active = null;   // drag en curso
      this.pending = null;  // toque inicial (aún no drag)
      this.onDrop = null;
      this.thresholdPx = 8; // umbral para considerar “arrastre real”
    }

    makeDraggable(el, opts = {}) {
      el.style.touchAction = "none";
      el.dataset.pd = "1";
      el._pdOpts = opts;

      el.addEventListener("pointerdown", (e) => {
        if (e.button !== undefined && e.button !== 0) return;
        e.preventDefault();

        const rect = el.getBoundingClientRect();
        const originParent = el.parentElement;
        const originNextSibling = el.nextSibling;

        this.pending = {
          el,
          pointerId: e.pointerId,
          startX: e.clientX,
          startY: e.clientY,
          offsetX: e.clientX - rect.left,
          offsetY: e.clientY - rect.top,
          originParent,
          originNextSibling,
          originRect: rect,
          bounds: opts.bounds || null,
          revert: opts.revert || null,
        };

        el.setPointerCapture(e.pointerId);
      });

      el.addEventListener("pointermove", (e) => {
        if (this.active && this.active.pointerId === e.pointerId) {
          e.preventDefault();
          this._moveActive(e);
          return;
        }

        if (!this.pending || this.pending.pointerId !== e.pointerId) return;

        const dx = e.clientX - this.pending.startX;
        const dy = e.clientY - this.pending.startY;
        const dist = Math.hypot(dx, dy);

        if (dist < this.thresholdPx) return; // aún es “toque”, no drag

        // Activamos drag real
        this._activateDrag(e);
      });

      el.addEventListener("pointerup", (e) => {
        if (this.active && this.active.pointerId === e.pointerId) {
          e.preventDefault();
          this._finishDrag(e);
          return;
        }

        // Si estaba en pending y NO llegó a drag => NO mover nada
        if (this.pending && this.pending.pointerId === e.pointerId) {
          // click normal (no arrastre)
          this.pending = null;
          try { el.releasePointerCapture(e.pointerId); } catch {}
        }
      });

      el.addEventListener("pointercancel", (e) => {
        if (this.active && this.active.pointerId === e.pointerId) {
          this.revertActive();
          this.active = null;
        }
        this.pending = null;
      });
    }

    _activateDrag(e) {
      const p = this.pending;
      if (!p) return;

      const { el, originRect } = p;

      el.classList.add("is-dragging");
      el.style.position = "absolute";
      el.style.left = `${originRect.left}px`;
      el.style.top = `${originRect.top}px`;
      el.style.width = `${originRect.width}px`;
      el.style.height = `${originRect.height}px`;
      el.style.zIndex = "9999";

      document.body.appendChild(el);

      this.active = p;
      this.pending = null;

      this._moveActive(e);
    }

    _moveActive(e) {
      const a = this.active;
      if (!a) return;

      const { el, offsetX, offsetY, bounds } = a;

      let x = e.clientX - offsetX;
      let y = e.clientY - offsetY;

      if (bounds) {
        const b = bounds.getBoundingClientRect();
        const w = el.getBoundingClientRect().width;
        const h = el.getBoundingClientRect().height;
        x = clamp(x, b.left, b.right - w);
        y = clamp(y, b.top, b.bottom - h);
      }

      el.style.left = `${x}px`;
      el.style.top = `${y}px`;
    }

    _finishDrag(e) {
  const a = this.active;
  if (!a) return;

  const { el } = a;
  el.classList.remove("is-dragging");

  // detectar dropZone bajo el dedo (ignorando el propio elemento)
  el.style.pointerEvents = "none";
  const dropTarget = document.elementFromPoint(e.clientX, e.clientY);
  el.style.pointerEvents = "";
  const dropZone = dropTarget?.closest?.(
    ".slot-drop, .dropzone, .drop-chest, .chest-drop"
  );

  try {
    if (typeof this.onDrop === "function") {
      this.onDrop(dropZone, el);
    } else {
      this.revertActive();
    }
  } finally {
    // SEGURIDAD TOTAL: si el elemento sigue colgando en <body>, vuelve SIEMPRE
    if (el.parentElement === document.body) {
      this.revertActive();
    }

    try { el.releasePointerCapture(e.pointerId); } catch {}
    this.active = null;
  }
}

    revertActive() {
      const a = this.active;
      if (!a) return;

      const { el, originParent, originNextSibling, revert } = a;

      if (typeof revert === "function") {
        revert(el);
        return;
      }

      el.style.position = "";
      el.style.left = "";
      el.style.top = "";
      el.style.width = "";
      el.style.height = "";
      el.style.zIndex = "";

      if (originNextSibling) originParent.insertBefore(el, originNextSibling);
      else originParent.appendChild(el);
    }
  }

  /* =========================
     GAME STATE
  ========================= */

  const state = {
    screen: 1,
    lettersDone: new Set(),
    keysDropped: 0,
    classifyDone: 0,
    memPlaced: [],
    coins: { 3: 0, 5: 0, 6: 0 },
    syllablesDone: new Set(),
  };

  /* =========================
     SCREEN NAVIGATION
  ========================= */

  const FLOW = [1, 2, 3, 4, "interlude", 5, 6, 7, 8];

  function setInstruction(screenKey) {
    safeText($("#instruction"), INSTRUCTIONS[screenKey] || "");
  }

  function setBackground(screenKey) {
    const bgEl = $("#sceneBg");
    const url = ASSETS.bg[screenKey];
    if (!url) return;
    setBgWithFallback(bgEl, url);
  }

  function getScreenEl(key) {
    if (typeof key === "number") return $(`#screen-${key}`);
    return $(`#screen-${key}`);
  }

  function switchScreen(nextKey) {
    const current = $(".screen.is-active");
    const target = getScreenEl(nextKey);

    if (!target) {
      console.warn("Pantalla no encontrada:", nextKey, "→ screen-1");
      const fallback = getScreenEl(1);
      if (fallback) fallback.classList.add("is-active");
      return;
    }

    if (current && current === target) {
      target.classList.add("is-active");
      target.classList.remove("is-leaving");
      state.screen = nextKey;
      setInstruction(nextKey);
      setBackground(nextKey);
      onEnterScreen(nextKey);
      return;
    }

    if (current) {
      current.classList.add("is-leaving");
      setTimeout(() => current.classList.remove("is-active", "is-leaving"), SETTINGS.fadeMs);
    }

    target.classList.add("is-active");
    state.screen = nextKey;

    setInstruction(nextKey);
    setBackground(nextKey);
    onEnterScreen(nextKey);
  }

  function nextScreen() {
    const idx = FLOW.indexOf(state.screen);
    const nextKey = FLOW[Math.min(FLOW.length - 1, idx + 1)];
    switchScreen(nextKey);
  }

  function restartGame() {
    state.screen = 1;
    state.lettersDone.clear();
    state.keysDropped = 0;
    state.classifyDone = 0;
    state.memPlaced = [];
    state.coins = { 3: 0, 5: 0, 6: 0 };
    state.syllablesDone.clear();

    resetUIAll();
    switchScreen(1);
  }

  /* =========================
     MUSIC
  ========================= */

  function setupMusic() {
    const bgm = $("#bgm");
    const btn = $("#btnMusic");
    if (!bgm) return;

    bgm.src = ASSETS.audio.bgm;
    bgm.loop = true;
     bgm.volume = SETTINGS.bgmVolume;
// Volumen de música de fondo (0.0 a 1.0)
    const tryAutoplay = () => {
      bgm.play().then(() => {
        if (btn) btn.hidden = true;
      }).catch(() => {
        if (btn) btn.hidden = false;
      });
    };

    tryAutoplay();

    if (btn) {
      btn.addEventListener("click", () => {
        bgm.play().then(() => (btn.hidden = true)).catch(() => toast("Toca de nuevo para activar música"));
      });
    }

    const firstGesture = () => tryAutoplay();
    window.addEventListener("pointerdown", firstGesture, { once: true });
    window.addEventListener("touchstart", firstGesture, { once: true, passive: true });
  }
function playVoice(src) {
  const bgm = $("#bgm");
  if (!bgm) return;

  const voice = new Audio(src);
  voice.volume = SETTINGS.voiceVolume;

  const originalVolume = bgm.volume;

  // Baja la música mientras habla la voz
  bgm.volume = SETTINGS.duckBgmWhileVoice;

  voice.addEventListener("ended", () => {
    bgm.volume = originalVolume;
  });

  voice.addEventListener("error", () => {
    bgm.volume = originalVolume;
    console.warn("Error al reproducir voz:", src);
  });

  voice.play().catch(() => {
    bgm.volume = originalVolume;
  });
}
  /* =========================
     SCREEN 1
  ========================= */

  function initScreen1() {
  const btnPlay = $("#btnStart");     // VAMOS A JUGAR
  const btnListen = $("#btnListen1"); // ESCUCHAR
  if (!btnPlay || !btnListen) return;

  // Al cargar: NO se puede empezar
  disable(btnPlay, true);

  let listened = false;
  let playing = false;

  btnListen.addEventListener("click", () => {
    if (playing) return;

    playing = true;
    disable(btnListen, true); // evita doble tap

    playOneShot(ASSETS.audio.intro1, () => {
      listened = true;
      playing = false;

      // Habilita empezar
      disable(btnPlay, false);

      // Vuelve a permitir escuchar si quieres (opcional)
      disable(btnListen, false);
    });
  });

  btnPlay.addEventListener("click", () => {
    if (!listened) return; // seguridad
    switchScreen(2);
  });
}

  /* =========================
     SCREEN 2 — LETTERS
  ========================= */

  const drag2 = new PointerDrag();

  function initScreen2() {
    const root = $("#screen-2");
    if (!root) return;

    const btnNext = $("#btnNext2");
    disable(btnNext, true);

    const chips = $$(".chip-drag", root);

    drag2.onDrop = (dropZone, draggedEl) => {
      const letter = draggedEl?.dataset?.letter;
      const targetId = draggedEl?.dataset?.target;

      const slot = dropZone?.closest?.(".slot-drop");
      const slotId = slot?.dataset?.slot;

      if (!slot || !slotId) {
        drag2.revertActive();
        return;
      }

      if (slotId !== targetId) {
        toast("Prueba en su palabra");
        drag2.revertActive();
        return;
      }

      const row = root.querySelector(`.letter-row[data-id="${slotId}"]`);
      const solution = row?.dataset?.solution;

      if (!solution) {
        drag2.revertActive();
        return;
      }

      if (letter === solution) {
        state.lettersDone.add(slotId);
        slot.textContent = letter;
        slot.classList.add("is-correct");

        chips
          .filter(c => c.dataset.target === slotId)
          .forEach(c => {
            c.disabled = true;
            c.classList.add("is-disabled");
          });

        drag2.revertActive();
        bigCheck();

        if (state.lettersDone.size >= SETTINGS.letters.length) {
          disable(btnNext, false);
        }
      } else {
        toast("Esa no… prueba la otra");
        drag2.revertActive();
      }
    };

    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        if (chip.disabled) return;

        const letter = chip.dataset.letter;
        const targetId = chip.dataset.target;
        const row = root.querySelector(`.letter-row[data-id="${targetId}"]`);
        const solution = row?.dataset?.solution;
        const slot = root.querySelector(`.slot-drop[data-slot="${targetId}"]`);
        if (!slot) return;

        if (letter === solution) {
          state.lettersDone.add(targetId);
          slot.textContent = letter;
          slot.classList.add("is-correct");

          chips
            .filter(c => c.dataset.target === targetId)
            .forEach(c => {
              c.disabled = true;
              c.classList.add("is-disabled");
            });

          bigCheck();
          if (state.lettersDone.size >= SETTINGS.letters.length) disable(btnNext, false);
        } else {
          toast("Prueba la otra");
        }
      });

      drag2.makeDraggable(chip, { bounds: root });
    });

    if (btnNext) btnNext.addEventListener("click", nextScreen);
  }

  function resetScreen2() {
    const root = $("#screen-2");
    if (!root) return;

    state.lettersDone.clear();

    $$(".slot-drop", root).forEach((slot) => {
      slot.textContent = "_";
      slot.classList.remove("is-correct");
    });

    $$(".chip-drag", root).forEach((c) => {
      c.disabled = false;
      c.classList.remove("is-disabled");
      c.style.position = "";
      c.style.left = "";
      c.style.top = "";
      c.style.width = "";
      c.style.height = "";
      c.style.zIndex = "";
    });

    disable($("#btnNext2"), true);
  }

  /* =========================
     SCREEN 3 — KEYS
  ========================= */

  const drag3 = new PointerDrag();

  function buildScreen3() {
    const root = $("#screen-3");
    if (!root) return;

    const keysLayer = $("#keysLayer");
    const chestDrop = $("#chestDrop");
    const chestImg = $("#chestImg");
    const btnNext = $("#btnNext3");

    if (!keysLayer || !chestDrop) return;

    disable(btnNext, true);
    state.keysDropped = 0;

    keysLayer.innerHTML = "";

    for (let i = 0; i < SETTINGS.keyCount; i++) {
      const k = document.createElement("button");
      k.type = "button";
      k.className = "key-item";
      k.setAttribute("aria-label", "Llave");
      k.dataset.key = String(i + 1);

      const img = imgEl(ASSETS.objects.key, "Llave");
      img.classList.add("key-img");
      k.appendChild(img);

      k.style.position = "absolute";
      k.style.left = `${10 + (i * 14) + (i % 2) * 8}%`;
      k.style.top = `${18 + (i * 10) % 55}%`;

      keysLayer.appendChild(k);

      k.addEventListener("click", () => {
        if (k.classList.contains("is-dropped")) return;
        k.classList.add("is-dropped");
        k.style.opacity = "0.25";
        k.style.pointerEvents = "none";
        state.keysDropped++;
        bigCheck();
        if (state.keysDropped >= SETTINGS.keyCount) {
          if (chestImg) chestImg.src = ASSETS.objects.chestOpen;
          disable(btnNext, false);
        }
      });

      drag3.makeDraggable(k, { bounds: root });
    }

    drag3.onDrop = (dropZone, draggedEl) => {
      const dz = dropZone?.closest?.(".chest-drop");
      if (!dz || dz !== chestDrop) {
        drag3.revertActive();
        return;
      }

      if (draggedEl.classList.contains("is-dropped")) {
        drag3.revertActive();
        return;
      }

      draggedEl.classList.add("is-dropped");
      draggedEl.style.opacity = "0.15";
      draggedEl.style.pointerEvents = "none";

      drag3.revertActive();

      state.keysDropped++;
      bigCheck();

      if (state.keysDropped >= SETTINGS.keyCount) {
        if (chestImg) chestImg.src = ASSETS.objects.chestOpen;
        disable(btnNext, false);
      }
    };

    if (btnNext) btnNext.onclick = nextScreen;

    if (chestImg) {
      chestImg.src = ASSETS.objects.chestClosed;
      chestImg.addEventListener("error", () => {
        reportMissing(ASSETS.objects.chestClosed);
      });
    }
  }

  function resetScreen3() {
    state.keysDropped = 0;
    disable($("#btnNext3"), true);
    const chestImg = $("#chestImg");
    if (chestImg) chestImg.src = ASSETS.objects.chestClosed;
  }

  /* =========================
     SCREEN 4 — CLASSIFY (-> INTERLUDE al completar)
  ========================= */

  const drag4 = new PointerDrag();

  function buildScreen4() {
    const root = $("#screen-4");
    if (!root) return;

    const tray = $("#objectsTray");
    const dropPirates = $("#dropPirates");
    const dropExplorers = $("#dropExplorers");
    const btnNext = $("#btnNext4");

    if (!tray || !dropPirates || !dropExplorers) return;

    disable(btnNext, true);
    state.classifyDone = 0;

    tray.innerHTML = "";

    const items = [
      { key: "telescope", group: "pirates", label: "Catalejo" },
      { key: "sword", group: "pirates", label: "Espada" },
      { key: "flag", group: "pirates", label: "Bandera pirata" },
      { key: "cannon", group: "pirates", label: "Cañón" },
      { key: "ball", group: "explorers", label: "Pelota" },
      { key: "plush", group: "explorers", label: "Peluche" },
    ];

    const total = items.length;

    function placeClassify(el, zone) {
      el.classList.add("is-placed");
      el.style.pointerEvents = "none";
      el.style.opacity = "0.2";

      zone.classList.add("is-hit");
      setTimeout(() => zone.classList.remove("is-hit"), 250);

      state.classifyDone++;
      bigCheck();

      if (state.classifyDone >= total) {
        // En lugar de “continuar” aquí, saltamos a interlude
        disable(btnNext, false);
        setTimeout(() => switchScreen("interlude"), 450);
      }
    }

    items.forEach((it) => {
      const card = document.createElement("button");
      card.type = "button";
      card.className = "obj-card";
      card.dataset.group = it.group;
      card.dataset.key = it.key;
      card.setAttribute("aria-label", it.label);

      const img = imgEl(ASSETS.objects[it.key], it.label);
      img.classList.add("obj-img");
      card.appendChild(img);

      card.addEventListener("click", () => {
        if (card.classList.contains("is-placed")) return;
        const correctZone = it.group === "pirates" ? dropPirates : dropExplorers;
        placeClassify(card, correctZone);
      });

      tray.appendChild(card);
      drag4.makeDraggable(card, { bounds: root });
    });

    drag4.onDrop = (dropZone, draggedEl) => {
      const dz = dropZone?.closest?.(".dropzone");
      if (!dz) {
        drag4.revertActive();
        return;
      }

      const group = draggedEl.dataset.group;
      const correct =
        (group === "pirates" && dz === dropPirates) ||
        (group === "explorers" && dz === dropExplorers);

      if (!correct) {
        toast("Ese no va ahí");
        drag4.revertActive();
        return;
      }

      drag4.revertActive();
      placeClassify(draggedEl, dz);
    };

    if (btnNext) btnNext.onclick = () => switchScreen("interlude");
  }

  function resetScreen4() {
    state.classifyDone = 0;
    disable($("#btnNext4"), true);
  }

  /* =========================
     INTERLUDE
  ========================= */

  function initInterlude() {
    const btn = $("#interludeContinue");
    if (btn) btn.addEventListener("click", () => switchScreen(5));
  }

  /* =========================
     SCREEN 5 — MEMORY
  ========================= */

  const drag5 = new PointerDrag();

  function buildScreen5() {
    const root = $("#screen-5");
    if (!root) return;

    const preview = $("#memoryPreview");
    const bank = $("#memoryBank");
    const btnNext = $("#btnNext5");

    if (!preview || !bank) return;

    disable(btnNext, true);

    // Preview
    preview.innerHTML = "";
    SETTINGS.memoryOrder.forEach((k) => {
      const wrap = document.createElement("div");
      wrap.className = "mem-preview-item";
      wrap.appendChild(imgEl(ASSETS.objects[k], k));
      preview.appendChild(wrap);
    });

    show(preview);
    setTimeout(() => {
      hide(preview);
      startMemoryRound();
    }, SETTINGS.memoryPreviewMs);

    function startMemoryRound() {
      state.memPlaced = [];

      $$(".mem-slot", root).forEach((s) => {
        s.classList.remove("is-filled");
        s.innerHTML = s.dataset.memslot;
      });

      const keys = [...SETTINGS.memoryOrder];
      shuffle(keys);

      bank.innerHTML = "";
      keys.forEach((k) => {
        const item = document.createElement("button");
        item.type = "button";
        item.className = "mem-item";
        item.dataset.key = k;
        item.setAttribute("aria-label", k);
        item.appendChild(imgEl(ASSETS.objects[k], k));

        item.addEventListener("click", () => {
          if (item.classList.contains("is-used")) return;
          const nextSlot = $$(".mem-slot", root).find(s => !s.classList.contains("is-filled"));
          if (!nextSlot) return;
          tryPlaceMemory(item, nextSlot);
        });

        bank.appendChild(item);
        drag5.makeDraggable(item, { bounds: root });
      });

      drag5.onDrop = (dropZone, draggedEl) => {
        const slot = dropZone?.closest?.(".mem-slot");
        if (!slot) {
          drag5.revertActive();
          return;
        }
        if (slot.classList.contains("is-filled")) {
          toast("Ese hueco ya está");
          drag5.revertActive();
          return;
        }
        drag5.revertActive();
        tryPlaceMemory(draggedEl, slot);
      };
    }

    function tryPlaceMemory(item, slot) {
      const slotNum = Number(slot.dataset.memslot);
      const correctKey = SETTINGS.memoryOrder[slotNum - 1];
      const chosen = item.dataset.key;

      if (chosen !== correctKey) {
        toast("No era ese… prueba otro");
        return;
      }

      slot.classList.add("is-filled");
      slot.textContent = "";
      slot.appendChild(imgEl(ASSETS.objects[chosen], chosen));

      item.classList.add("is-used");
      item.style.opacity = "0.2";
      item.style.pointerEvents = "none";

      state.memPlaced.push({ slot: slotNum, key: chosen });
      bigCheck();

      if (state.memPlaced.length >= 3) disable(btnNext, false);
    }

    if (btnNext) btnNext.onclick = nextScreen;
  }

  function resetScreen5() {
    state.memPlaced = [];
    disable($("#btnNext5"), true);
  }

  /* =========================
     SCREEN 6 — COINS
  ========================= */

  const drag6 = new PointerDrag();

  function buildScreen6() {
    const root = $("#screen-6");
    if (!root) return;

    state.coins = { 3: 0, 5: 0, 6: 0 };
    disable($("#btnNext6"), true);

    const bank = $("#coinsBank");
    const chests = $$(".count-chest", root);

    if (!bank || !chests.length) return;

    bank.innerHTML = "";
    const totalNeeded = SETTINGS.coinsTargets.reduce((a, b) => a + b, 0);
    const totalCoins = totalNeeded + 6;

    for (let i = 0; i < totalCoins; i++) {
      const c = document.createElement("button");
      c.type = "button";
      c.className = "coin-item";
      c.dataset.coin = String(i + 1);
      c.setAttribute("aria-label", "Moneda");
      c.appendChild(imgEl(ASSETS.objects.coin, "Moneda"));
      bank.appendChild(c);

      c.addEventListener("click", () => {
        if (c.classList.contains("is-used")) return;
        $$(".coin-item", bank).forEach(x => x.classList.remove("is-selected"));
        c.classList.add("is-selected");
        toast("Ahora toca un cofre (3, 5 o 6)");
      });

      drag6.makeDraggable(c, { bounds: root });
    }

    chests.forEach((ch) => {
      ch.addEventListener("click", () => {
        const selected = $(".coin-item.is-selected", bank);
        if (!selected || selected.classList.contains("is-used")) return;
        const target = Number(ch.dataset.target);
        placeCoin(selected, target);
      });
    });

    drag6.onDrop = (dropZone, draggedEl) => {
      const dz = dropZone?.closest?.(".drop-chest");
      if (!dz) {
        drag6.revertActive();
        return;
      }
      const target = Number(dz.dataset.coinchest);
      drag6.revertActive();
      placeCoin(draggedEl, target);
    };

    function placeCoin(coinEl, target) {
      if (coinEl.classList.contains("is-used")) return;

      if (state.coins[target] >= target) {
        toast("Ese cofre ya está completo");
        return;
      }

      coinEl.classList.remove("is-selected");
      coinEl.classList.add("is-used");
      coinEl.style.opacity = "0.2";
      coinEl.style.pointerEvents = "none";

      state.coins[target]++;

      chests.forEach((ch) => {
        const t = Number(ch.dataset.target);
        const st = ch.querySelector(".count-status");
        if (st) st.textContent = `${state.coins[t]} / ${t}`;
      });

      bigCheck();

      if (SETTINGS.coinsTargets.every((t) => state.coins[t] === t)) {
        disable($("#btnNext6"), false);
      }
    }

    const btn = $("#btnNext6");
    if (btn) btn.onclick = nextScreen;
  }

  function resetScreen6() {
    state.coins = { 3: 0, 5: 0, 6: 0 };
    disable($("#btnNext6"), true);
  }

  /* =========================
     SCREEN 7 — SYLLABLES
  ========================= */

  function initScreen7() {
    const root = $("#screen-7");
    if (!root) return;

    const btn = $("#btnNext7");
    disable(btn, true);

    const rows = $$(".syll-row", root);
    rows.forEach((row) => {
      const word = row.dataset.word;
      const answer = Number(row.dataset.answer);
      const opts = $$(".btn-option", row);
      const res = $(".syll-result", row);

      opts.forEach((b) => {
        b.addEventListener("click", () => {
          const pick = Number(b.dataset.pick);
          opts.forEach(o => o.classList.remove("is-picked"));
          b.classList.add("is-picked");

          if (pick === answer) {
            safeText(res, "✓");
            res.classList.add("is-correct");
            state.syllablesDone.add(word);
            bigCheck();
          } else {
            safeText(res, "—");
            res.classList.remove("is-correct");
            state.syllablesDone.delete(word);
            toast("Cuenta otra vez");
          }

          if (state.syllablesDone.size >= SETTINGS.syllables.length) {
            disable(btn, false);
          }
        });
      });
    });

    if (btn) btn.addEventListener("click", nextScreen);
  }

  function resetScreen7() {
    state.syllablesDone.clear();
    disable($("#btnNext7"), true);
    const root = $("#screen-7");
    if (!root) return;

    $$(".syll-row", root).forEach((row) => {
      $$(".btn-option", row).forEach(b => b.classList.remove("is-picked"));
      const res = $(".syll-result", row);
      if (res) {
        res.textContent = "—";
        res.classList.remove("is-correct");
      }
    });
  }

  /* =========================
     SCREEN 8 — FINAL
  ========================= */

  function initScreen8() {
    const btn = $("#btnRestart");
    if (btn) btn.addEventListener("click", restartGame);
  }

  /* =========================
     ENTER HOOKS (reconstrucción dinámica)
  ========================= */

  let built3 = false, built4 = false, built5 = false, built6 = false;

  function onEnterScreen(key) {
    const fb = $("#assetFallback");
    if (fb) fb.hidden = true;

    if (key === 3) { buildScreen3(); built3 = true; }
    if (key === 4) { buildScreen4(); built4 = true; }
    if (key === 5) { buildScreen5(); built5 = true; }
    if (key === 6) { buildScreen6(); built6 = true; }
  }

  /* =========================
     RESET UI
  ========================= */

  function resetUIAll() {
    resetScreen2();
    resetScreen3();
    resetScreen4();
    resetScreen5();
    resetScreen6();
    resetScreen7();
  }

  /* =========================
     SHUFFLE
  ========================= */

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = (Math.random() * (i + 1)) | 0;
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  /* =========================
     BOOT
  ========================= */

  function boot() {
    setupMusic();

    initScreen1();
    initScreen2();
    initInterlude();
    initScreen7();
    initScreen8();

    setInstruction(1);
    setBackground(1);
    switchScreen(1);
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
