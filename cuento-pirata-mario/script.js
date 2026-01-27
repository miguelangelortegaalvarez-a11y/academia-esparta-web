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

  const VERSION = "2147";
  const withV = (url) =>
    (url ? `${url}${url.includes("?") ? "&" : "?"}v=${VERSION}` : url);

  /* =========================
     CONFIG
  ========================= */

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
      map: "./assets/objects/MAPA.PNG", // ✅ NUEVO
      chestClosed: "./assets/objects/COFRE_CERRADO.PNG",
      chestOpen: "./assets/objects/COFRE_ABIERTO.PNG",
      coin: "./assets/objects/MONEDA_ORO.PNG",
    },
    audio: {
      bgm: "./assets/audio/MUSICA_PIRATAS_FONDO.mp3",
      intro1: "./assets/audio/INTRO_PANTALLA1.mp3",
      interlude1: "./assets/audio/INTERLUDE_MOTIVACION.mp3",

      // ✅ NUEVOS audios de pista (puedes cambiar nombres/rutas)
      clue_sword: "./assets/audio/PISTA_ESPADA.mp3",
      clue_telescope: "./assets/audio/PISTA_CATALEJO.mp3",
      clue_flag: "./assets/audio/PISTA_BANDERA.mp3",
      clue_map: "./assets/audio/PISTA_MAPA.mp3",
      clue_key: "./assets/audio/PISTA_LLAVE.mp3",
    },
  };

  const INSTRUCTIONS = {
    1: "",
    2: "Mira bien: falta la primera letra. Pulsa la letra correcta.",
    3: "Encuentra 5 llaves y púlsalas.",
    4: "Pulsa solo los 4 objetos piratas.",
    interlude: "",
    5: "Pulsa ESCUCHAR y toca el objeto correcto.",
    6: "Arrastra monedas a cada cofre: 3, 5 y 6.",
    7: "Cuenta las sílabas y elige la opción correcta.",
    8: "",
  };

  const SETTINGS = {
    fadeMs: 350,
    keyCount: 5,
    coinsTargets: [3, 5, 6],

    bgmVolume: 0.18,
    voiceVolume: 1.0,
    duckBgmWhileVoice: 0.06,

    // Actividad 1
    letters: [
      { id: "w1", solution: "M" },
      { id: "w2", solution: "P" },
      { id: "w3", solution: "T" },
      { id: "w4", solution: "B" },
      { id: "w5", solution: "I" },
      { id: "w6", solution: "C" },
      { id: "w7", solution: "B" },
    ],

    // Actividad 7
    syllables: [
      { word: "MAPA", answer: 2 },
      { word: "PIRATA", answer: 3 },
      { word: "TESORO", answer: 3 },
    ],

    // Actividad 4 (tocar objetos piratas)
    classify: {
      pirates: ["telescope", "sword", "flag", "cannon"],
      explorers: ["ball", "plush"],
    },

    // ✅ NUEVA Actividad 5 (Escucha y encuentra)
    findObject: {
      // 5 rondas
      pool: ["sword", "telescope", "flag", "map", "key"],
      // 5 objetos en pantalla (usamos los mismos 5 para no añadir más imágenes)
      grid: ["sword", "telescope", "flag", "map", "key"],
      labels: {
        sword: "ESPADA",
        telescope: "CATALEJO",
        flag: "BANDERA",
        map: "MAPA",
        key: "LLAVE",
      },
      // Texto muy simple por si quieres también mostrarlo en pantalla (opcional)
      cluesText: {
        sword: "Busca la espada del pirata.",
        telescope: "Busca el catalejo para mirar lejos.",
        flag: "Busca la bandera pirata.",
        map: "Busca el mapa del tesoro.",
        key: "Busca la llave para abrir el cofre.",
      },
      // Mapeo a audios
      cluesAudio: {
        sword: ASSETS.audio.clue_sword,
        telescope: ASSETS.audio.clue_telescope,
        flag: ASSETS.audio.clue_flag,
        map: ASSETS.audio.clue_map,
        key: ASSETS.audio.clue_key,
      },
    },
  };

  // =========================
  // MOTIVACIÓN (INTERLUDE)
  // =========================
  const INTERLUDE_MOTIVATION_TEXT = "¡Bien, piratas! Lo estáis haciendo genial.";

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
  ========================= */

  class PointerDrag {
    constructor() {
      this.active = null;
      this.pending = null;
      this.onDrop = null;
      this.thresholdPx = 8;
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

        if (dist < this.thresholdPx) return;

        this._activateDrag(e);
      });

      el.addEventListener("pointerup", (e) => {
        if (this.active && this.active.pointerId === e.pointerId) {
          e.preventDefault();
          this._finishDrag(e);
          return;
        }

        if (this.pending && this.pending.pointerId === e.pointerId) {
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
    coins: { 3: 0, 5: 0, 6: 0 },
    syllablesDone: new Set(),

    // ✅ NUEVO estado pantalla 5
    find: {
      queue: [],
      current: null,
      solved: new Set(),
      lock: false,
    },
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
    setBgWithFallback(bgEl, withV(url));
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
    state.coins = { 3: 0, 5: 0, 6: 0 };
    state.syllablesDone.clear();

    state.find.queue = [];
    state.find.current = null;
    state.find.solved.clear();
    state.find.lock = false;

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

    // ✅ ocultamos el botón siempre (no quieres “activarla” manualmente)
    if (btn) btn.hidden = true;

    bgm.src = withV(ASSETS.audio.bgm);
    bgm.loop = true;
    bgm.volume = SETTINGS.bgmVolume;

    const tryAutoplay = () => {
      bgm.play().catch(() => {
        // iOS/Safari bloqueará hasta un gesto: lo resolvemos con firstGesture
      });
    };

    tryAutoplay();

    // En el primer toque/click arrancamos si estaba bloqueada
    const firstGesture = () => tryAutoplay();
    window.addEventListener("pointerdown", firstGesture, { once: true });
    window.addEventListener("touchstart", firstGesture, { once: true, passive: true });
  }

  function playVoice(src) {
    const bgm = $("#bgm");
    const voice = new Audio(withV(src));
    voice.volume = SETTINGS.voiceVolume;

    if (!bgm) {
      return voice.play();
    }

    const originalVolume = bgm.volume;
    bgm.volume = SETTINGS.duckBgmWhileVoice;

    return new Promise((resolve, reject) => {
      const restore = () => {
        bgm.volume = originalVolume;
      };

      voice.addEventListener("ended", () => {
        restore();
        resolve();
      });

      voice.addEventListener("error", () => {
        restore();
        console.warn("Error al reproducir voz:", src);
        reject(new Error("voice error"));
      });

      voice.play().catch((err) => {
        restore();
        reject(err);
      });
    });
  }

  /* =========================
     SCREEN 1
  ========================= */

  function initScreen1() {
    const btnPlay = $("#btnStart");
    const btnListen = $("#btnListen1");
    if (!btnPlay || !btnListen) return;

    disable(btnPlay, true);

    let listened = false;
    let playing = false;

    btnListen.addEventListener("click", () => {
      if (playing) return;

      playing = true;
      disable(btnListen, true);

      playVoice(ASSETS.audio.intro1)
        .then(() => {
          listened = true;
          disable(btnPlay, false);
          disable(btnListen, false);
          bigCheck();
        })
        .catch(() => {
          listened = true;
          disable(btnPlay, false);
          disable(btnListen, false);
          toast("No se pudo reproducir la voz");
        })
        .finally(() => {
          playing = false;
        });
    });

    btnPlay.addEventListener("click", () => {
      if (!listened) return;
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

      const img = imgEl(withV(ASSETS.objects.key), "Llave");
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
          if (chestImg) chestImg.src = withV(ASSETS.objects.chestOpen);
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
        if (chestImg) chestImg.src = withV(ASSETS.objects.chestOpen);
        disable(btnNext, false);
      }
    };

    if (btnNext) btnNext.onclick = nextScreen;

    if (chestImg) {
      chestImg.src = withV(ASSETS.objects.chestClosed);
      chestImg.addEventListener("error", () => {
        reportMissing(ASSETS.objects.chestClosed);
      });
    }
  }

  function resetScreen3() {
    state.keysDropped = 0;
    disable($("#btnNext3"), true);
    const chestImg = $("#chestImg");
    if (chestImg) chestImg.src = withV(ASSETS.objects.chestClosed);
  }

  /* =========================
     SCREEN 4 — PIRATE TAP
  ========================= */

  function buildScreen4() {
    const root = $("#screen-4");
    if (!root) return;

    const layer = $("#pirateTapLayer");
    const btnNext = $("#btnNext4");

    if (!layer || !btnNext) return;

    disable(btnNext, true);
    layer.innerHTML = "";

    state.classifyDone = 0;

    const pirateKeys = SETTINGS.classify?.pirates || ["telescope", "sword", "flag", "cannon"];
    const decoys = SETTINGS.classify?.explorers || ["ball", "plush"];

    const items = [
      ...pirateKeys.map((k) => ({ key: k, isPirate: true })),
      ...decoys.map((k) => ({ key: k, isPirate: false })),
    ];
function resetScreen4() {
  state.classifyDone = 0;
  disable($("#btnNext4"), true);
  const layer = $("#pirateTapLayer");
  if (layer) layer.innerHTML = "";
}
    const NAME_MAP = {
      telescope: "CATALEJO",
      sword: "ESPADA",
      flag: "BANDERA",
      cannon: "CAÑÓN",
      ball: "PELOTA",
      plush: "PELUCHE",
    };

    // mezcla para variar
    shuffle(items);

    items.forEach((it) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "pirate-tap-item";
      b.dataset.key = it.key;
      b.dataset.pirate = it.isPirate ? "1" : "0";
      b.setAttribute("aria-label", (NAME_MAP[it.key] || it.key).toUpperCase());

      const img = imgEl(withV(ASSETS.objects[it.key]), it.key);
      img.classList.add("pirate-tap-img");

      const label = document.createElement("div");
      label.className = "pirate-tap-label";
      label.textContent = (NAME_MAP[it.key] || it.key).toUpperCase();

      b.appendChild(img);
      b.appendChild(label);

      b.addEventListener("click", () => {
        if (b.classList.contains("is-picked")) return;

        const isPirate = b.dataset.pirate === "1";
        if (!isPirate) {
          toast("Ese no es de piratas");
          b.classList.add("is-wrong");
          setTimeout(() => b.classList.remove("is-wrong"), 250);
          return;
        }

        b.classList.add("is-picked");
        b.style.opacity = "0.18";
        b.style.pointerEvents = "none";
        state.classifyDone++;
        bigCheck();

        if (state.classifyDone >= pirateKeys.length) {
          disable(btnNext, false);
        }
      });

      layer.appendChild(b);
    });

    btnNext.onclick = () => switchScreen("interlude");
  }

  function resetScreen4() {
    state.classifyDone = 0;
    disable($("#btnNext4"), true);
    const layer = $("#pirateTapLayer");
    if (layer) layer.innerHTML = "";
  }

  /* =========================
     INTERLUDE
  ========================= */

  function initInterlude() {
    const btnContinue = $("#interludeContinue");
    const btnListen = $("#btnListenInterlude");
    const topRight = $("#interludeMotivation");
    safeText(topRight, INTERLUDE_MOTIVATION_TEXT);

    if (btnContinue) {
      btnContinue.addEventListener("click", () => switchScreen(5));
    }

    if (btnListen) {
      let playing = false;

      btnListen.addEventListener("click", () => {
        if (playing) return;
        playing = true;
        disable(btnListen, true);

        playVoice(ASSETS.audio.interlude1)
          .catch(() => {
            toast("No se pudo reproducir la voz");
          })
          .finally(() => {
            disable(btnListen, false);
            playing = false;
          });
      });
    }
  }

  /* =========================
     SCREEN 5 — ESCUCHA Y ENCUENTRA (NUEVO)
  ========================= */

  function buildScreen5() {
    const root = $("#screen-5");
    if (!root) return;

    const area = $("#memoryArea");   // reutilizamos el contenedor del index
    const btnNext = $("#btnNext5");
    if (!area || !btnNext) return;

    disable(btnNext, true);

    // Construimos UI interna sin tocar el index
    area.innerHTML = `
      <div class="find-wrap" aria-label="Escucha y encuentra">
        <div class="find-top">
          <button id="btnFindListen" class="btn btn-secondary btn-big" type="button">ESCUCHAR</button>
          <div id="findRoundText" class="find-round" aria-live="polite"></div>
        </div>
        <div id="findGrid" class="find-grid" role="group" aria-label="Objetos para elegir"></div>
      </div>
    `;

    const btnListen = $("#btnFindListen", area);
    const roundText = $("#findRoundText", area);
    const grid = $("#findGrid", area);

    // Inicializa cola aleatoria de 5 rondas
    state.find.queue = [...SETTINGS.findObject.pool];
    shuffle(state.find.queue);
    state.find.current = null;
    state.find.solved = new Set();
    state.find.lock = false;

    // Render grid (5 objetos visibles siempre)
    grid.innerHTML = "";
    SETTINGS.findObject.grid.forEach((k) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "find-item";
      b.dataset.key = k;
      b.setAttribute("aria-label", SETTINGS.findObject.labels[k] || k);

      const img = imgEl(withV(ASSETS.objects[k]), SETTINGS.findObject.labels[k] || k);
      img.classList.add("find-img");

      const label = document.createElement("div");
      label.className = "find-label";
      label.textContent = (SETTINGS.findObject.labels[k] || k).toUpperCase();

      b.appendChild(img);
      b.appendChild(label);

      b.addEventListener("click", () => {
        if (state.find.lock) return;
        if (state.find.solved.has(k)) return;

        const target = state.find.current;
        if (!target) {
          toast("Pulsa ESCUCHAR primero");
          return;
        }

        if (k !== target) {
          toast("Ese no… prueba otro");
          b.classList.add("is-wrong");
          setTimeout(() => b.classList.remove("is-wrong"), 220);
          return;
        }

        // ✅ ACIERTO
        state.find.solved.add(k);
        bigCheck();

        // ilumina y bloquea ese objeto
        b.classList.add("is-found");
        b.style.pointerEvents = "none";
        b.style.opacity = "1";
        // un “brillo” inline para que se note incluso sin CSS nuevo
        b.style.filter = "drop-shadow(0 0 14px rgba(255,215,90,0.75))";
        b.style.outline = "3px solid rgba(255,215,90,0.8)";
        b.style.outlineOffset = "6px";
        b.style.borderRadius = "14px";

        // “no se puede volver a escuchar” (en la práctica: avanzamos ronda y cambiamos objetivo)
        state.find.current = null;
        safeText(roundText, "¡Bien! ✅");

        if (state.find.solved.size >= SETTINGS.findObject.pool.length) {
          disable(btnNext, false);
          safeText(roundText, "¡Perfecto! Ya puedes CONTINUAR.");
          disable(btnListen, true);
          return;
        }

        // siguiente ronda
        setTimeout(() => {
          startNextRound();
        }, 450);
      });

      grid.appendChild(b);
    });

    function startNextRound() {
      if (state.find.lock) return;

      // Busca el siguiente objetivo que no esté resuelto
      let next = null;
      while (state.find.queue.length) {
        const cand = state.find.queue.shift();
        if (!state.find.solved.has(cand)) {
          next = cand;
          break;
        }
      }
      // si por lo que sea se vació, reconstruimos con los que falten
      if (!next) {
        const remaining = SETTINGS.findObject.pool.filter(x => !state.find.solved.has(x));
        shuffle(remaining);
        next = remaining[0] || null;
      }

      state.find.current = next;

      const done = state.find.solved.size;
      const total = SETTINGS.findObject.pool.length;
      safeText(roundText, `Ronda ${done + 1} / ${total}`);
      disable(btnListen, false);
    }

    // ESCUCHAR: reproduce pista del objetivo
    if (btnListen) {
      let playing = false;
      btnListen.addEventListener("click", () => {
        if (state.find.lock) return;
        if (playing) return;

        // si no hay ronda activa, la arrancamos
        if (!state.find.current) startNextRound();

        const target = state.find.current;
        if (!target) return;

        const src = SETTINGS.findObject.cluesAudio[target];
        if (!src) {
          toast("No hay audio de pista");
          return;
        }

        playing = true;
        disable(btnListen, true);

        playVoice(src)
          .catch(() => toast("No se pudo reproducir la voz"))
          .finally(() => {
            playing = false;
            // si aún no se ha acertado esa ronda, permitimos volver a escuchar
            if (state.find.current) disable(btnListen, false);
          });
      });
    }

    // Arranca primera ronda automáticamente (sin escuchar)
    startNextRound();

    // CONTINUAR
    btnNext.onclick = nextScreen;
  }

  function resetScreen5() {
    disable($("#btnNext5"), true);
    state.find.queue = [];
    state.find.current = null;
    state.find.solved.clear();
    state.find.lock = false;

    const area = $("#memoryArea");
    if (area) area.innerHTML = "";
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
      c.appendChild(imgEl(withV(ASSETS.objects.coin), "Moneda"));
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
     ENTER HOOKS
  ========================= */

  function onEnterScreen(key) {
    const fb = $("#assetFallback");
    if (fb) fb.hidden = true;

    if (key === 3) buildScreen3();
    if (key === 4) buildScreen4();
    if (key === 5) buildScreen5(); // ✅ ahora es “Escucha y encuentra”
    if (key === 6) buildScreen6();
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
