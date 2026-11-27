> Movido tal cual desde CLAUDE.md el 27-nov-2026 (reorganización). Copia anterior: tag `antes-reorganizar-27nov`.

## Estructura del proyecto

```
academia-esparta-web/
│
├── CLAUDE.md                               # Este archivo — referencia completa del proyecto
├── DISENO.md                               # Sistema visual premium (paleta, tipografía, componentes, trampas)
├── README.md                               # Descripción mínima del repo
├── CNAME                                   # academiaesparta.es
├── robots.txt
├── sitemap.xml                             # Generado por CI (cron diario 05:00 UTC + manual; NO en cada push desde 2026-07-05)
├── .github/workflows/sitemap.yml          # CI: regenera sitemap cuando cambia cualquier .html
│
│  ── Páginas principales ──
├── index.html                              # Home — sistema visual premium
├── quienes-somos.html                      # Equipo
├── logopedia.html                          # Servicio Logopedia (Rocío)
├── psicologia.html                         # Servicio Psicología
├── materiales.html                         # Hub público de fichas imprimibles (índice React inline)
├── blog.html                               # Hub blog SEO "Guías para padres" — diseño editorial con fotos (rediseño 2026-06-15)
├── blog-img/                               # Fotos de portada del blog (Pexels, self-hosted): mates, ortografia, estudio, lectura, academia, ebau
├── inscripcion.html                        # Redirige → shadow.academiaesparta.es/inscripcion
├── juegos.html                             # "Próximamente" — interactivos aparcados
├── 404.html                                # Página de error (sistema premium)
├── como-elegir-academia-torremolinos.html  # Artículo SEO nº1
├── como-preparar-la-ebau-andalucia.html    # Artículo SEO EBAU/Bachillerato (2026-06-15)
├── google690465498c577da0.html             # Verificación Google Search Console (no tocar)
│
│  ── Recursos (fichas imprimibles SEO) ──
├── recursos/
│   ├── primaria/
│   │   ├── 1/lengua/     # letras(58), comprension(24), comprension-opciones(24),
│   │   │                 # conciencia-fonologica(11), lectura-frase(10) — COMPLETO ✅
│   │   ├── 2/lengua/     # 12 bloques × ~10 fichas — COMPLETO ✅
│   │   ├── 3/lengua/     # 12 bloques × 6 fichas — COMPLETO ✅
│   │   ├── 4/lengua/     # 14 bloques completos (6-10 fichas c/u) — COMPLETO ✅
│   │   ├── 5/lengua/     # COMPLETO ✅ (cerrado 2026-05-23)
│   │   │                 # Área Lectura: 7 bloques × 10 fichas
│   │   │                 # Bloque D Gramática 8/8: analisis-morfologico, verbos-irregulares, oracion-simple, campos-semanticos, connotacion-y-denotacion, acentuacion-completa, tildes-diacriticas, puntuacion-avanzada
│   │   └── 6/lengua/     # COMPLETO ✅ (cerrado 2026-05-24) — 150 fichas
│   │                     # Área Lectura 7/7 ✅:
│   │                     #   - tipologias-textuales (10 fichas)
│   │                     #   - textos-literarios-narrativa (10 fichas)
│   │                     #   - textos-literarios-poesia (10 fichas)
│   │                     #   - textos-literarios-teatro (10 fichas)
│   │                     #   - textos-discontinuos (10 fichas)
│   │                     #   - intencion-autor-subtexto (10 fichas, márgenes 3cm)
│   │                     #   - resumen-y-esquema-avanzado (10 fichas, márgenes 3cm)
│   │                     # Área Gramática D 8/8 ✅:
│   │                     #   - analisis-sintactico-sn-sv (10 fichas, márgenes 3cm)
│   │                     #   - oracion-compuesta-coordinadas (10 fichas, márgenes 3cm)
│   │                     #   - oracion-compuesta-subordinadas (10 fichas, márgenes 3cm)
│   │                     #   - verbo-avanzado (10 fichas, márgenes 3cm)
│   │                     #   - lexico-cultismos-prefijos (10 fichas, márgenes 3cm)
│   │                     #   - polisemia-homonimia-paronimia (10 fichas, márgenes 3cm)
│   │                     #   - ortografia-avanzada (10 fichas, márgenes 3cm)
│   │                     #   - puntuacion-nivel-eso (10 fichas, márgenes 3cm)
│   │   ├── 1/matematicas/      # 1º Mates COMPLETO ✅ (cerrado 2026-05-28, 71 fichas)
│   │   │                       # 6 bloques: numeros (12) + operaciones (20) + medida (15) + geometria (9) + estadistica (6) + problemas (9)
│   │   ├── [2-6]/matematicas/  # Pendiente · Estructura acordada 2026-05-24 — ver sección "Estructura matemáticas Primaria"
│   └── 1-eso/
│       └── matematicas/algebra/  # 4 páginas (apuntes, imprimibles, interactivo, index)
│                                 # Resto de 1º ESO sin cubrir
│
│  ── Imágenes ──
├── favicon.PNG / apple-touch-icon.png / og-image.jpg   # favicon = logo real (columnas + «academia ESPARTA»). El templo genérico Logo.PNG se borró el 22-nov-2026: no usar
├── hero.jpg / quienes-somos.jpg / primaria.jpg / secundaria.jpg / bachiller.jpg
└── julio.jpg / miguel.jpg        # Fotos equipo (todas en uso)
│
│  ── Juegos de contenido propio (PILOTO en local, SIN SUBIR — ver memoria project-juegos-interactivos) ──
├── juegos/
│   └── camino-matematico/    # Piloto reconstruido 2026-06-17: motor por cursos + imágenes optimizadas (32MB→1.6MB) + dinamismo
│                             # NO trackeado, NO enlazado en juegos.html. Original en _pendiente/ intacto.
│
│  ── Interactivos aparcados (no tocar hasta acabar recursos) ──
└── _pendiente/
    ├── camino-ingles/
    ├── camino-letras/
    ├── camino-matematico/
    ├── cuento-pirata-mario/
    ├── operaciones/
    ├── mates-iniciales/
    ├── lectoescritura/
    ├── primero/
    ├── entrenamiento-esparta.html
    ├── entrenamiento-division.html
    └── lectura-comprensiva.html
```

---


## Estado técnico / auditoría web (2026-06-02)

Auditoría profunda + optimizaciones (3 commits: `ee102d0`, `0bdfdfe`, `326c1d0`). Detalle en memoria `project-web-auditoria-optimizacion`.

> **⚠️ FIX CRÍTICO 2026-06-15 (commit a31b003):** el hash SRI de Font Awesome estaba MAL en las 13 páginas (`sha512-p1HgFeAX…`). Con SRI estricto, eso **bloqueaba TODOS los iconos de Font Awesome en toda la web, en todos los navegadores y en producción** (footer redes, mapa, teléfono, flechas "Leer guía"…) — pasó desapercibido porque casi todos los iconos llevan texto al lado. Corregido al hash bueno de FA 6.4.0: `sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw==` (mantiene SRI). **Lección:** si no se ven iconos FA, comprobar el hash SRI contra el fichero que sirve cdnjs (`openssl dgst -sha512 -binary all.min.css | openssl base64 -A`). Los SVG/CSS escritos a mano (botón WhatsApp, pulse-dot) NO dependen de FA y siempre se vieron.

**Hecho:**
- **Reseñas Google 63 → 64** en 5 sitios (index.html: chip hero, contador `data-target`, label rating, chip rotativo JS; + `como-elegir-academia-torremolinos.html`).
- **153 botones "← Volver" rotos (404) arreglados** — eran error de plantilla (mal número de `../`): Lengua necesita 5 niveles `../../../../../materiales.html`, Mates 6 niveles `../../../../../../materiales.html`. Verificar SIEMPRE al crear plantilla nueva.
- **Índice `conciencia-fonologica`** reescrito: 8 cards inventadas → 5 fichas reales.
- **Rendimiento:** imágenes recomprimidas con `sips` (~1,5 MB ahorrados: hero 914→359 KB, Logo 371→98 KB, etc.) + `preload`/`fetchpriority` del hero + `preconnect` a fuentes. El hero es **background-image CSS** (por eso disparaba el LCP).
- **`aggregateRating` 4,9 · 64** en JSON-LD (estrellas Google). Caveat: Google puede no mostrar estrellas de reseñas autodeclaradas sin widget.
- Meta description en `inscripcion.html`.

**Foto técnica:** HTTPS ✅, SEO 100/100, 0 enlaces/recursos rotos, todas las imágenes con `alt`, Umami **sin cookies** (no necesita banner RGPD), web pública **sin `<form>`** (inscripción → `shadow.academiaesparta.es`, contacto por WhatsApp).

**Fuentes — optimización invisible HECHA (2026-06-22, commits b1aaad1 + 6bce16e):** auditoría profunda (2 workflows con verificación adversarial + medición woff2 real). Hallazgo: **8 familias** en el sitio (Fraunces, Poppins, Nunito, Montserrat, Open Sans, Edu SA Beginner, Bebas Neue, Roboto Mono). Matiz clave: el navegador solo descarga el woff2 de un peso/familia que algún elemento PINTA → lo cargado-no-usado no se baja (recortarlo es cosmético). Aplicado, **0 cambio visual** (validado píxel a píxel): (1) Fraunces sin el eje `SOFT` inútil (0 usos en las 1039 páginas) → woff2 **221→124 KB, -97 KB/página** en las 15 premium; (2) Nunito muerta fuera de index; (3) `preconnect` a `fonts.gstatic` en **1037 páginas** (premium + fichas, -100-300 ms). Las fichas ya estaban tipográficamente ajustadas. **DECISIÓN Miguel: NO cambiar las letras** (descartado unificar/sustituir fuentes). NO tocadas por esa norma: `.rating-big` (Poppins 900 sintetizado), Roboto Mono en 2 fichas 6º, Bebas Neue en 3 de 1º ESO.

**Pendiente (rendimiento):** Font Awesome (carga la librería completa por ~15 iconos — subset/SVG inline, con cuidado de no romper diseño); WebP (falta cwebp/imagemagick en la máquina); cabeceras de seguridad 0/4 (GitHub Pages no las permite → opcional Cloudflare delante, no urgente).

---

