/* ==========================================================
   CUENTO PIRATA MARIO — Juego educativo 4 años (SPA)
   - Sin frameworks. Offline. GitHub Pages.
   - 8 pantallas lineales.
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
      bgm: "./assets/audio/MUSICA_PIRATAS_FONDO.MP3",
    },
  };

  const INSTRUCTIONS = {
    1: "",
    2: "Mira bien: falta la primera letra. Arrastra la correcta.",
    3: "Encuentra 5 llaves y arrástralas al cofre.",
    4: "Arrastra los objetos PIRATAS hacia los niños piratas.",
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
    letters: [
      { id: "w1", solution: "M", rest: "APA" },
      { id: "w2", solution: "P", rest: "IRATA" },
      { id: "w3", solution: "T", rest: "ESORO" },
    ],
    syllables: [
      { word: "MAPA", answer: 2 },
      { word: "PIRATA", answer: 3 },
      { word: "TESORO", answer: 3 },
    ],
    classify: {
      pirates: ["telescope", "sword", "flag", "cannon"],
      explorers: ["ball", "plush"],
    },
    memoryOrder: ["telescope", "sword", "flag"],
  };

  /* =========================
     HELPERS (DOM)
  ========================= */
function reportMissing(url) {
  const fb = document.getElementById("assetFallback");
  if (!fb) return;
  fb.hidden = false;
  fb.textContent = `FALTA RECURSO: ${url}`;
  console.error("FALTA RECURSO:", url);
}
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

  /* =========================
     ASSET FALLBACKS
  ========================= */

  function setBgWithFallback(bgEl, url) {
    if (!bgEl) return;

    // Preload to detect errors
    const img = new Image();
    img.onload = () => {
      bgEl.style.backgroundImage = `url("${url}")`;
    };
    img.onerror = () => {
      bgEl.style.backgroundImage = "none";
      show($("#assetFallback"));
      // Minimal fallback gradient
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
     - Works on touch + mouse
     - We keep it simple & robust
  ========================= */

  class PointerDrag {
    constructor() {
      this.active = null; // { el, startX, startY, offsetX, offsetY, originRect, originParent, originNextSibling }
      this.onDrop = null; // callback(dropTarget, draggedEl)
    }

    makeDraggable(el, opts = {}) {
      // opts: { data?: any, bounds?: HTMLElement, revert?: () => void }
      el.style.touchAction = "none";
      el.dataset.pd = "1";
      el._pdOpts = opts;

      el.addEventListener("pointerdown", (e) => {
        if (e.button !== undefined && e.button !== 0) return; // only left click if mouse
        e.preventDefault();

        const rect = el.getBoundingClientRect();
        const parentRect = el.parentElement.getBoundingClientRect();

        // Save origin to allow revert
        const originParent = el.parentElement;
        const originNextSibling = el.nextSibling;

        // Move to body overlay (so it can float above)
        const ghost = el;
        ghost.classList.add("is-dragging");
        ghost.style.position = "absolute";
        ghost.style.left = `${rect.left}px`;
        ghost.style.top = `${rect.top}px`;
        ghost.style.width = `${rect.width}px`;
        ghost.style.height = `${rect.height}px`;
        ghost.style.zIndex = "9999";

        document.body.appendChild(ghost);

        this.active = {
          el: ghost,
          pointerId: e.pointerId,
          offsetX: e.clientX - rect.left,
          offsetY: e.clientY - rect.top,
          originParent,
          originNextSibling,
          originRect: rect,
          bounds: opts.bounds || null,
          revert: opts.revert || null,
        };

        ghost.setPointerCapture(e.pointerId);
      });

      el.addEventListener("pointermove", (e) => {
        if (!this.active || this.active.pointerId !== e.pointerId) return;
        e.preventDefault();

        const { el: ghost, offsetX, offsetY, bounds } = this.active;
        let x = e.clientX - offsetX;
        let y = e.clientY - offsetY;

        if (bounds) {
          const b = bounds.getBoundingClientRect();
          const w = ghost.getBoundingClientRect().width;
          const h = ghost.getBoundingClientRect().height;
          x = clamp(x, b.left, b.right - w);
          y = clamp(y, b.top, b.bottom - h);
        }

        ghost.style.left = `${x}px`;
        ghost.style.top = `${y}px`;
      });

      el.addEventListener("pointerup", (e) => {
        if (!this.active || this.active.pointerId !== e.pointerId) return;
        e.preventDefault();

        const { el: ghost } = this.active;
        ghost.classList.remove("is-dragging");

        // Detect drop target under pointer
        const dropTarget = document.elementFromPoint(e.clientX, e.clientY);
        const dropZone = dropTarget?.closest?.(".slot-drop, .dropzone, .drop-chest, .chest-drop");

        if (typeof this.onDrop === "function") {
          this.onDrop(dropZone, ghost);
        } else {
          this.revertActive(); // fallback
        }

        ghost.releasePointerCapture(e.pointerId);
        this.active = null;
      });

      el.addEventListener("pointercancel", () => {
        if (!this.active) return;
        this.revertActive();
        this.active = null;
      });
    }

    revertActive() {
      if (!this.active) return;
      const { el, originParent, originNextSibling, revert } = this.active;

      // If custom revert exists
      if (typeof revert === "function") {
        revert(el);
        return;
      }

      // Default revert: back to origin parent
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
    // Screen 2
    lettersDone: new Set(), // w1,w2,w3
    // Screen 3
    keysDropped: 0,
    // Screen 4
    classifyDone: 0,
    // Screen 5
    memPlaced: [], // [{slot:1, key:'telescope'}...]
    // Screen 6
    coins: { 3: 0, 5: 0, 6: 0 },
    // Screen 7
    syllablesDone: new Set(), // word
  };

  /* =========================
     SCREEN NAVIGATION
  ========================= */

  function setInstruction(screenNum) {
    safeText($("#instruction"), INSTRUCTIONS[screenNum] || "");
  }

  function setBackground(screenNum) {
    const bgEl = $("#sceneBg");
    setBgWithFallback(bgEl, ASSETS.bg[screenNum]);
  }

  function switchScreen(next) {
    const current = $(`.screen.is-active`);
    const target = $(`#screen-${next}`);
    if (!target) return;

    // Fade out current
    if (current) {
      current.classList.add("is-leaving");
      setTimeout(() => {
        current.classList.remove("is-active", "is-leaving");
      }, SETTINGS.fadeMs);
    }

    // Fade in target
    target.classList.add("is-active");
    state.screen = next;

    setInstruction(next);
    setBackground(next);

    // Run per-screen "enter" hooks
    onEnterScreen(next);
  }

  function nextScreen() {
    const next = Math.min(8, state.screen + 1);
    switchScreen(next);
  }

  function restartGame() {
    // Reset state
    state.screen = 1;
    state.lettersDone.clear();
    state.keysDropped = 0;
    state.classifyDone = 0;
    state.memPlaced = [];
    state.coins = { 3: 0, 5: 0, 6: 0 };
    state.syllablesDone.clear();

    // Reset UI by re-initting screens
    resetUIAll();
    switchScreen(1);
  }

  /* =========================
     MUSIC (single track)
  ========================= */

  function setupMusic() {
    const bgm = $("#bgm");
    const btn = $("#btnMusic");

    if (!bgm) return;

    // Ensure correct src
    bgm.src = ASSETS.audio.bgm;
    bgm.loop = true;

    const tryAutoplay = () => {
      bgm.play().then(() => {
        // ok
        if (btn) btn.hidden = true;
      }).catch(() => {
        // blocked
        if (btn) btn.hidden = false;
      });
    };

    // Try at load
    tryAutoplay();

    // Button fallback
    if (btn) {
      btn.addEventListener("click", () => {
        bgm.play().then(() => {
          btn.hidden = true;
        }).catch(() => {
          toast("Toca de nuevo para activar música");
        });
      });
    }

    // If user touches anywhere, try again (helpful on iOS)
    const firstGesture = () => {
      tryAutoplay();
      window.removeEventListener("pointerdown", firstGesture);
      window.removeEventListener("touchstart", firstGesture);
    };
    window.addEventListener("pointerdown", firstGesture, { once: true });
    window.addEventListener("touchstart", firstGesture, { once: true, passive: true });
  }

  /* =========================
     SCREEN 1 — START
  ========================= */

  function initScreen1() {
    const btn = $("#btnStart");
    if (btn) btn.addEventListener("click", () => switchScreen(2));
  }

  /* =========================
     SCREEN 2 — LETTERS
     Spec: drag chip letter to slot (w1,w2,w3)
  ========================= */

  const drag2 = new PointerDrag();

  function initScreen2() {
    const root = $("#screen-2");
    if (!root) return;

    const btnNext = $("#btnNext2");
    disable(btnNext, true);

    // Make chips draggable
    const chips = $$(".chip-drag", root);

    // Drop handler
    drag2.onDrop = (dropZone, draggedEl) => {
      const letter = draggedEl?.dataset?.letter;
      const targetId = draggedEl?.dataset?.target; // w1, w2, w3

      const slot = dropZone?.closest?.(".slot-drop");
      const slotId = slot?.dataset?.slot;

      // If not dropping into a slot, revert
      if (!slot || !slotId) {
        drag2.revertActive();
        return;
      }

      // Must match its intended target row
      if (slotId !== targetId) {
        toast("Prueba en su palabra");
        drag2.revertActive();
        return;
      }

      // Check solution
      const row = root.querySelector(`.letter-row[data-id="${slotId}"]`);
      const solution = row?.dataset?.solution;

      if (!solution) {
        drag2.revertActive();
        return;
      }

      if (letter === solution) {
        // Success: lock word
        state.lettersDone.add(slotId);
        slot.textContent = letter;
        slot.classList.add("is-correct");

        // Disable both chips for that target
        chips
          .filter(c => c.dataset.target === slotId)
          .forEach(c => {
            c.disabled = true;
            c.classList.add("is-disabled");
          });

        // Remove dragged element safely back to its tray (revert styling)
        drag2.revertActive();
        bigCheck();

        if (state.lettersDone.size >= 3) {
          disable(btnNext, false);
        }
      } else {
        toast("Esa no… prueba la otra");
        drag2.revertActive();
      }
    };

    chips.forEach((chip) => {
      // Fallback tap: if chip tapped, try to place automatically
      chip.addEventListener("click", () => {
        const letter = chip.dataset.letter;
        const targetId = chip.dataset.target;
        const row = root.querySelector(`.letter-row[data-id="${targetId}"]`);
        const solution = row?.dataset?.solution;
        const slot = root.querySelector(`.slot-drop[data-slot="${targetId}"]`);
        if (!slot || chip.disabled) return;

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
          if (state.lettersDone.size >= 3) disable(btnNext, false);
        } else {
          toast("Prueba la otra");
        }
      });

      drag2.makeDraggable(chip, {
        bounds: root,
      });
    });

    if (btnNext) btnNext.addEventListener("click", nextScreen);
  }

  function resetScreen2() {
    const root = $("#screen-2");
    if (!root) return;
    state.lettersDone.clear();

    // reset slots
    $$(".slot-drop", root).forEach((slot) => {
      slot.textContent = "_";
      slot.classList.remove("is-correct");
    });

    // reset chips
    $$(".chip-drag", root).forEach((c) => {
      c.disabled = false;
      c.classList.remove("is-disabled");
      // ensure chip is in its original container if moved
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
     SCREEN 3 — KEYS to CHEST
  ========================= */

  const drag3 = new PointerDrag();

  function initScreen3() {
    const root = $("#screen-3");
    if (!root) return;

    const keysLayer = $("#keysLayer");
    const chestDrop = $("#chestDrop");
    const chestImg = $("#chestImg");
    const btnNext = $("#btnNext3");

    disable(btnNext, true);
    state.keysDropped = 0;

    // Build 5 keys (if not already)
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

      // Random-ish placement (JS only; CSS should allow absolute positioning)
      k.style.position = "absolute";
      k.style.left = `${10 + (i * 14) + (i % 2) * 8}%`;
      k.style.top = `${20 + (i * 10) % 50}%`;

      keysLayer.appendChild(k);

      // Tap fallback: counts as drop
      k.addEventListener("click", () => {
        if (k.classList.contains("is-dropped")) return;
        k.classList.add("is-dropped");
        k.style.opacity = "0.35";
        state.keysDropped++;
        bigCheck();
        if (state.keysDropped >= SETTINGS.keyCount) {
          // open chest + enable
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
      // Hide key once dropped
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

    if (btnNext) btnNext.addEventListener("click", nextScreen);

    // Ensure chest image fallback
    if (chestImg) {
      chestImg.addEventListener("error", () => {
        chestImg.src = ASSETS.objects.chestClosed; // try again, then svg fallback via browser
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
     SCREEN 4 — CLASSIFY
  ========================= */

  const drag4 = new PointerDrag();

  function initScreen4() {
    const root = $("#screen-4");
    if (!root) return;

    const tray = $("#objectsTray");
    const dropPirates = $("#dropPirates");
    const dropExplorers = $("#dropExplorers");
    const btnNext = $("#btnNext4");

    disable(btnNext, true);
    state.classifyDone = 0;

    // Build objects
    tray.innerHTML = "";

    const items = [
      { key: "telescope", group: "pirates", label: "Catalejo" },
      { key: "sword", group: "pirates", label: "Espada" },
      { key: "flag", group: "pirates", label: "Bandera pirata" },
      { key: "cannon", group: "pirates", label: "Cañón" },
      { key: "ball", group: "explorers", label: "Pelota" },
      { key: "plush", group: "explorers", label: "Peluche" },
    ];

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

      // Tap fallback: send to correct zone automatically
      card.addEventListener("click", () => {
        if (card.classList.contains("is-placed")) return;
        const correctZone = it.group === "pirates" ? dropPirates : dropExplorers;
        placeClassify(card, correctZone);
      });

      tray.appendChild(card);
      drag4.makeDraggable(card, { bounds: root });
    });

    function placeClassify(el, zone) {
      el.classList.add("is-placed");
      el.style.pointerEvents = "none";
      el.style.opacity = "0.25";
      zone.classList.add("is-hit");
      setTimeout(() => zone.classList.remove("is-hit"), 250);

      state.classifyDone++;
      bigCheck();

      if (state.classifyDone >= items.length) {
        disable(btnNext, false);
      }
    }

    drag4.onDrop = (dropZone, draggedEl) => {
      const dz = dropZone?.closest?.(".dropzone");
      if (!dz) {
        drag4.revertActive();
        return;
      }

      const group = draggedEl.dataset.group;
      const isPiratesZone = dz === dropPirates;
      const isExplZone = dz === dropExplorers;

      const correct =
        (group === "pirates" && isPiratesZone) ||
        (group === "explorers" && isExplZone);

      if (!correct) {
        toast("Ese no va ahí");
        drag4.revertActive();
        return;
      }

      // Correct
      drag4.revertActive();
      placeClassify(draggedEl, dz);
    };

    if (btnNext) btnNext.addEventListener("click", nextScreen);
  }

  function resetScreen4() {
    state.classifyDone = 0;
    disable($("#btnNext4"), true);
  }

  /* =========================
     SCREEN 5 — MEMORY ORDER
  ========================= */

  const drag5 = new PointerDrag();

  function initScreen5() {
    const root = $("#screen-5");
    if (!root) return;

    const preview = $("#memoryPreview");
    const bank = $("#memoryBank");
    const btnNext = $("#btnNext5");
    disable(btnNext, true);

    // Build preview sequence
    preview.innerHTML = "";
    SETTINGS.memoryOrder.forEach((k) => {
      const wrap = document.createElement("div");
      wrap.className = "mem-preview-item";
      wrap.appendChild(imgEl(ASSETS.objects[k], k));
      preview.appendChild(wrap);
    });

    // Show preview, then hide
    hide(preview);
    show(preview);
    setTimeout(() => {
      hide(preview);
      startMemoryRound();
    }, SETTINGS.memoryPreviewMs);

    function startMemoryRound() {
      // Reset slots
      state.memPlaced = [];
      $$(".mem-slot", root).forEach((s) => {
        s.classList.remove("is-filled");
        s.dataset.filled = "";
        s.textContent = s.getAttribute("aria-label")?.includes("1") ? "1"
          : s.getAttribute("aria-label")?.includes("2") ? "2" : "3";
      });

      // Build bank shuffled
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

        // Tap fallback: place to next empty slot
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
        bigCheck(350); // small feedback anyway
        return;
      }

      // Fill slot visually
      slot.classList.add("is-filled");
      slot.textContent = "";
      slot.appendChild(imgEl(ASSETS.objects[chosen], chosen));

      item.classList.add("is-used");
      item.style.opacity = "0.2";
      item.style.pointerEvents = "none";

      state.memPlaced.push({ slot: slotNum, key: chosen });
      bigCheck();

      if (state.memPlaced.length >= 3) {
        disable(btnNext, false);
      }
    }

    if (btnNext) {
      btnNext.addEventListener("click", () => {
        // Spec says auto; but we keep button too. Auto can be added later.
        nextScreen();
      });
    }
  }

  function resetScreen5() {
    state.memPlaced = [];
    disable($("#btnNext5"), true);
  }

  /* =========================
     SCREEN 6 — COINS COUNTS
  ========================= */

  const drag6 = new PointerDrag();

  function initScreen6() {
    const root = $("#screen-6");
    if (!root) return;

    state.coins = { 3: 0, 5: 0, 6: 0 };
    disable($("#btnNext6"), true);

    const bank = $("#coinsBank");
    const chests = $$(".count-chest", root);
    const statusEls = $$(".count-status", root);

    // Build coins bank: create enough coins (3+5+6 + extras for comfort)
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

      // Tap fallback: do nothing (coins need drag). But allow tap to select then tap chest.
      c.addEventListener("click", () => {
        if (c.classList.contains("is-used")) return;
        $$(".coin-item", bank).forEach(x => x.classList.remove("is-selected"));
        c.classList.add("is-selected");
        toast("Ahora toca un cofre (3, 5 o 6)");
      });

      drag6.makeDraggable(c, { bounds: root });
    }

    // Tap-to-drop fallback: tap a chest if a coin is selected
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

      // If already full, reject
      if (state.coins[target] >= target) {
        toast("Ese cofre ya está completo");
        return;
      }

      coinEl.classList.remove("is-selected");
      coinEl.classList.add("is-used");
      coinEl.style.opacity = "0.2";
      coinEl.style.pointerEvents = "none";

      state.coins[target]++;

      // Update status text
      updateCoinStatuses();

      bigCheck();

      // Check completion: exact match for all
      if (isCoinsComplete()) {
        disable($("#btnNext6"), false);
      }
    }

    function updateCoinStatuses() {
      chests.forEach((ch) => {
        const target = Number(ch.dataset.target);
        const st = ch.querySelector(".count-status");
        if (st) st.textContent = `${state.coins[target]} / ${target}`;
      });
    }

    function isCoinsComplete() {
      return SETTINGS.coinsTargets.every((t) => state.coins[t] === t);
    }

    // Continue button (we keep explicit control)
    const btn = $("#btnNext6");
    if (btn) btn.addEventListener("click", nextScreen);
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

    state.syllablesDone.clear();
    disable($("#btnNext7"), true);

    const rows = $$(".syll-row", root);
    rows.forEach((row) => {
      const word = row.dataset.word;
      const answer = Number(row.dataset.answer);
      const opts = $$(".btn-option", row);
      const res = $(".syll-result", row);

      opts.forEach((btn) => {
        btn.addEventListener("click", () => {
          const pick = Number(btn.dataset.pick);

          // Mark selection UI
          opts.forEach(o => o.classList.remove("is-picked"));
          btn.classList.add("is-picked");

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
            disable($("#btnNext7"), false);
          }
        });
      });
    });

    const btn = $("#btnNext7");
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
     SCREEN ENTER HOOKS
  ========================= */

  function onEnterScreen(n) {
    // Hide global fallback message after first success (optional)
    const fb = $("#assetFallback");
    if (fb) fb.hidden = true;

    // Per-screen init (idempotent-ish)
    // Note: We initialize once at load; here we can refresh dynamic content if needed.
    if (n === 3) {
      // Ensure chest image uses correct file
      const chestImg = $("#chestImg");
      if (chestImg) chestImg.src = ASSETS.objects.chestClosed;
    }
  }

  /* =========================
     RESET UI
  ========================= */

  function resetUIAll() {
    // Screen 2
    resetScreen2();

    // Screen 3: full rebuild will happen when visiting screen 3; just reset counters
    resetScreen3();

    // Screen 4
    resetScreen4();

    // Screen 5
    resetScreen5();

    // Screen 6
    resetScreen6();

    // Screen 7
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
    // init music first (so it can try autoplay)
    setupMusic();

    // init static buttons
    initScreen1();
    initScreen2();
    initScreen3();
    initScreen4();
    initScreen5();
    initScreen6();
    initScreen7();
    initScreen8();

    // start on screen 1
    setInstruction(1);
    setBackground(1);
    switchScreen(1);
  }

  document.addEventListener("DOMContentLoaded", boot);
})();
