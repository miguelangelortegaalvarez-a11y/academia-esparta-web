// JavaScript for the interactive story of Mario el Pirata

// Names of the four zones and mapping to page IDs
const zoneNames = ['MAR', 'ISLA', 'PLAYA', 'MONTANA'];
const zoneToPage = {
    MAR: 'page2',
    ISLA: 'page3',
    PLAYA: 'page4',
    MONTANA: 'page5'
};

// Keep track of visited zones
const visitedZones = new Set();

// Current page ID
let currentPageId = 'page1';

// Audio elements
const pageAudio = document.getElementById('pageAudio');
const bgMusic = document.getElementById('bgMusic');

// Music toggle button
const musicToggle = document.getElementById('music-toggle');

// Utility: show a page with fade transition
function showPage(pageId) {
    const prevPageEl = document.querySelector('.page.active');
    if (prevPageEl) {
        prevPageEl.classList.remove('active');
        // pause any playing audio from previous page
        pageAudio.pause();
        pageAudio.currentTime = 0;
    }
    const nextPageEl = document.getElementById(pageId);
    currentPageId = pageId;
    nextPageEl.classList.add('active');
    // Reset control buttons
    resetControls(nextPageEl);
    // Render mini map if applicable
    if (['page2', 'page3', 'page4', 'page5'].includes(pageId)) {
        renderMiniMap(nextPageEl);
    }
    // Update next button text depending on page
    const nextBtn = nextPageEl.querySelector('.next-btn');
    if (nextBtn) {
        if (pageId === 'page10') {
            nextBtn.textContent = 'Volver a empezar';
        } else {
            nextBtn.textContent = 'Siguiente';
        }
    }
}

// Reset buttons on a given page: disable next; enable listen/read
function resetControls(pageEl) {
    const listenBtn = pageEl.querySelector('.listen-btn');
    const readBtn = pageEl.querySelector('.read-btn');
    const nextBtn = pageEl.querySelector('.next-btn');
    if (listenBtn) listenBtn.disabled = false;
    if (readBtn) readBtn.disabled = false;
    if (nextBtn) nextBtn.disabled = true;
}

// Play audio for the specified audio key (e.g., "P01")
function playAudio(pageKey) {
    const src = `./assets/audio/${pageKey}.MP3`;
    pageAudio.src = src;
    pageAudio.load();
    pageAudio.play().catch(() => {
        // Autoplay might be blocked until user gesture; ignore
    });
}

// Enable the next button for the current page
function enableNextButton() {
    // Find the currently active page to locate the corresponding Next button
    const pageEl = document.querySelector('.page.active');
    if (!pageEl) return;
    const nextBtn = pageEl.querySelector('.next-btn');
    if (nextBtn) {
        nextBtn.disabled = false;
        nextBtn.removeAttribute('disabled');
    }
}

// Render the mini map inside the given page element
function renderMiniMap(pageEl) {
    const miniMapContainer = pageEl.querySelector('.mini-map');
    // Clear previous mini map
    miniMapContainer.innerHTML = '';
    zoneNames.forEach(zone => {
        const btn = document.createElement('button');
        btn.classList.add('mini-zone');
        btn.textContent = zone;
        if (visitedZones.has(zone)) {
            btn.classList.add('visited');
        } else {
            btn.classList.add('active');
            btn.addEventListener('click', () => {
                openZone(zone);
            });
        }
        miniMapContainer.appendChild(btn);
    });
}

// Open a zone page based on its name
function openZone(zone) {
    // Mark as visited
    visitedZones.add(zone);
    const pageId = zoneToPage[zone];
    showPage(pageId);
}

// Determine and go to the next page when 'Siguiente' is clicked
function goToNext() {
    // If we are on a zone page (2-5)
    if (['page2','page3','page4','page5'].includes(currentPageId)) {
        // If not all zones visited, pick the first unvisited zone
        if (visitedZones.size < zoneNames.length) {
            const nextZone = zoneNames.find(z => !visitedZones.has(z));
            if (nextZone) {
                openZone(nextZone);
                return;
            }
        }
        // All zones visited -> go to transition page
        showPage('page6');
        return;
    }
    // Page1: if user presses next without choosing zone, pick first zone
    if (currentPageId === 'page1') {
        if (visitedZones.size < zoneNames.length) {
            const nextZone = zoneNames.find(z => !visitedZones.has(z));
            if (nextZone) {
                openZone(nextZone);
                return;
            }
        }
        showPage('page6');
        return;
    }
    // For pages 6-9: simply advance to next numeric page
    if (currentPageId.startsWith('page')) {
        const pageNumber = parseInt(currentPageId.replace('page', ''), 10);
        const nextPageNumber = pageNumber + 1;
        if (nextPageNumber <= 10) {
            showPage('page' + nextPageNumber);
        }
    }
}

// Restart the story: reset visited zones and go back to page 1
function restartStory() {
    visitedZones.clear();
    showPage('page1');
}

// Setup event listeners for page buttons and audio
function setupEventListeners() {
    // Direct listeners for main map zones
    document.querySelectorAll('.zone-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const zone = btn.getAttribute('data-zone');
            if (zone) openZone(zone);
        });
    });
    // Direct listeners for listen buttons
    document.querySelectorAll('.listen-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const pageKey = btn.getAttribute('data-page');
            if (pageKey) playAudio(pageKey);
        });
    });
    // Direct listeners for read buttons
    document.querySelectorAll('.read-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Enable the next button within the same controls container
            const controls = btn.closest('.controls');
            if (controls) {
                const nextBtn = controls.querySelector('.next-btn');
                if (nextBtn) {
                    nextBtn.disabled = false;
                    nextBtn.removeAttribute('disabled');
                }
            }
        });
    });
    // Direct listeners for next buttons
    document.querySelectorAll('.next-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (currentPageId === 'page10') {
                restartStory();
            } else {
                goToNext();
            }
        });
    });
    // PageAudio ended or error: enable next
    pageAudio.addEventListener('ended', enableNextButton);
    pageAudio.addEventListener('error', enableNextButton);
    // Music toggle
    musicToggle.addEventListener('click', () => {
        if (bgMusic.paused) {
            bgMusic.play().catch(() => {});
            musicToggle.textContent = '🔇';
        } else {
            bgMusic.pause();
            musicToggle.textContent = '🎵';
        }
    });
}

// Initialise the story when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    showPage('page1');
});
