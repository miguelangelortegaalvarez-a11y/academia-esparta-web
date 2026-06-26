# Web Pública Academia Esparta

Web estática de captación y recursos educativos gratuitos. Sin backend propio — push a `main` = producción inmediata.

**URL pública:** https://academiaesparta.es · GitHub Pages · rama `main`

---

## Estructura del proyecto

```
academia-esparta-web/
│
├── CLAUDE.md                               # Este archivo — referencia completa del proyecto
├── DISENO.md                               # Sistema visual premium (paleta, tipografía, componentes, trampas)
├── README.md                               # Descripción mínima del repo
├── CNAME                                   # academiaesparta.es
├── robots.txt
├── sitemap.xml                             # Generado automáticamente por CI en cada push
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
├── Logo.PNG / favicon.PNG / apple-touch-icon.png / og-image.jpg
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

## Stack

| Capa | Tecnología |
|---|---|
| Lenguaje | HTML5 / CSS3 / JS vanilla — sin build, sin npm |
| Fuentes web | Google Fonts: **Fraunces** (serif, títulos) + **Poppins** (sans, cuerpo) |
| Fuente fichas imprimibles | **Edu SA Beginner** (1º–2º Primaria) / **Poppins** (3º+) |
| Iconos | Font Awesome 6.4 (CDN) |
| Índice fichas | React 18 UMD inline en `materiales.html` (sin Node, sin build) |
| Analytics | Umami (snippet en 8 páginas principales) |
| SEO | canonical, OG, Twitter Cards, JSON-LD (ServiceType + BreadcrumbList), sitemap.xml, robots.txt |
| CI | GitHub Actions → regenera `sitemap.xml` automáticamente |

---

## Producción

| Recurso | Valor |
|---|---|
| URL pública | https://academiaesparta.es |
| Plataforma | GitHub Pages (rama `main`) |
| Repo | github.com/miguelangelortegaalvarez-a11y/academia-esparta-web |
| Dominio | Dondominio — CNAME apunta a GitHub Pages |
| Deploy | Push a `main` → publicado en segundos. Sin servidor, sin Docker |
| Sitemap | Auto-regenerado por CI en cada push con cambios `.html` |

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

## Sistema visual premium

Refundición del 13/05/2026. Documentación completa en `DISENO.md`.

**Páginas en sistema premium:** `index.html`, `quienes-somos.html`, `logopedia.html`, `psicologia.html`, `blog.html`, `404.html`, `juegos.html`.

**Páginas en paleta legacy** (verde claro `#0e9343`, pendiente migrar): `materiales.html`.

| Token | Valor | Uso |
|---|---|---|
| Fondo principal | `#064e3b` | Hero, secciones A |
| Fondo alterno | `#053a2c` | Secciones B |
| Fondo footer | `#032519` | Solo footer |
| Acento | `#4ade80` | Pulse, links, glows |
| Texto cuerpo | `rgba(236,253,245,0.7)` | Párrafos |

**Trampas conocidas:**
- Secciones con `.reveal` → siempre añadir `opacity: 1 !important` o el contenido queda invisible si falla el IntersectionObserver.
- CSS legacy `#about > *` sobreescribe `position: absolute` de auroras → forzar con `!important`.

---

## Normas fichas imprimibles

Template aprobado **26 abril 2026** — no variar tamaños ni márgenes.

- Papel A4. Márgenes nuevos (2026-05-24): laterales **3cm** / superior 2cm / inferior 1.5cm — `@page { margin: 2cm 3cm 1.5cm 3cm }`. La EPSON ET-2820 de Miguel cortaba con 2.5cm. Solo B&N para imprimir. **Fichas anteriores siguen con márgenes menores (2.5cm las primeras 50 fichas de 6º — tipologías, narrativa, poesía, teatro, discontinuos; 2.2cm hasta 5º) — pendiente migrar.**
- ⚠️ **Impresión Safari (norma 2026-06-14):** poner el margen vía `@page { margin: 2cm 3cm 1.5cm 3cm }` falla en Safari (recorta el borde derecho de las cajas: Safari no respeta `@page{margin}`). En fichas con cajas/bordes que llegan al borde (`.problema`, tablas, `.recuerda`) usar **`@page { margin: 0 }` + en `@media print` `body { max-width: 15cm !important; margin: 2cm auto 1.5cm !important }`** (margen vía body, que Safari sí respeta). Mismo aspecto en Chrome. **Aplicado a las 202 fichas de Mates Primaria (1º + 2º, commit e69e24f, 2026-06-14).** Queda Lengua (~620 fichas) como deuda.
- Fuente 1º–2º: **Edu SA Beginner**. Fuente 3º+: **Poppins**.
- Las fichas NO usan el sistema visual premium de la web.
- Ruta Lengua: `recursos/primaria/CURSO/lengua/BLOQUE/nombre-bloque-Xprimaria-serie-Y.html`
- Ruta Mates: `recursos/primaria/CURSO/matematicas/BLOQUE/SUB-BLOQUE/nombre-sub-bloque-Xprimaria-serie-Y.html`
- Cada serie = 6 fichas (gramática/lengua/mates) o 10 fichas (comprensión/velocidad).
- El sitemap las recoge automáticamente — no hay que tocar nada más.

---

## Estructura matemáticas Primaria

Acordado con Miguel el **2026-05-24** antes de arrancar 1º Primaria Mates.

**6 bloques raíz** (5 LOMLOE + problemas como bloque propio), todos al mismo nivel:

```
recursos/primaria/CURSO/matematicas/
├── numeros/        # numeración, decenas, ordinales, comparar, fracciones (3º+), decimales (4º+), %
├── operaciones/    # sumas, restas, multiplicación, división, cálculo mental, potencias (5º+)
├── medida/         # longitud, masa, capacidad, tiempo, dinero, superficie (3º+), volumen (5º+)
├── geometria/      # figuras planas, cuerpos, ángulos, simetría, perímetro, área (3º+), coordenadas (4º+)
├── estadistica/    # tablas, gráficos (barras, líneas, sectores), media (5º+), probabilidad (5º+)
└── problemas/      # bloque propio con sub-bloques por tipo (suma, resta, multi, división, mixtos, fracciones, geometría…)
```

**Sub-bloques anidados** dentro de cada bloque (mismo patrón que Bloque D Gramática de 5º/6º Lengua):
```
recursos/primaria/3/matematicas/operaciones/sumas-llevadas/
├── sumas-llevadas-3primaria-serie-1.html
├── sumas-llevadas-3primaria-serie-2.html
└── ... (hasta serie-6)
```

**Tamaño de serie:** **6 fichas siempre** (uniforme, sin excepciones). Mismo criterio que Bloque D Gramática de Lengua.

**Orden de cobertura:** curso a curso, 1º → 6º. Cerrar 1º Mates completo antes de pasar a 2º.

**Formato fichas Mates (validado 2026-05-25 con `ficha-1.html` de `numeros-hasta-99`):**
- **Solo ejercicios, sin página de teoría.** Las fichas de Mates van directas a la práctica (la teoría la explica el profe en clase). Diferencia clave respecto a Lengua, que sí lleva página 1 de teoría.
- **1 folio A4 obligatorio.** Validar con Chrome headless PDF antes de cerrar cada ficha (`reference-chrome-pdf-preview`).
- **Rellenar la página entera, sin huecos vacíos** (norma del 2026-05-28). Si queda corta: añadir ejercicios coherentes con el sub-bloque o agrandar cajas/padding/font-size. Validar siempre con PDF antes de cerrar.
- **4-7 ejercicios** equilibrados que cubren el folio sin apretarse ni dejar huecos.
- **Bloque "Recuerda" inicial opcional** (estilo banner con borde negro): permitido como excepción al "solo ejercicios" cuando el concepto del sub-bloque lo requiere para asociar (ej. equivalencias D↔U). Validado en `decenas-unidades/ficha-1.html`.
- **Número de fichas por sub-bloque ajustable** (norma del 2026-05-28): el ideal son 6, pero si el concepto en 1º no da para 6 fichas distintas, hacer 2-3 con misma estructura y números distintos (estilo Rubio/Santillana). NO inventar conceptos de 2º para rellenar. Ejemplo: `decenas-unidades` cerrado en 2 fichas.
- Plantilla base CSS: ver `recursos/primaria/1/matematicas/numeros/numeros-hasta-99/ficha-1.html`.

### Sub-bloques 1º Primaria — COMPLETO ✅ (71 fichas)

| Bloque | Sub-bloques | Fichas |
|---|---|---|
| `numeros` ✅ | numeros-hasta-99 (6 ✅) · decenas-unidades (2 ✅) · numeros-ordinales (2 ✅) · comparar-y-ordenar (2 ✅) | **12** |
| `operaciones` ✅ | sumas-sin-llevadas (8 ✅) · restas-sin-llevadas (8 ✅) · sumas-y-restas-mezcladas (4 ✅) | **20** |
| `medida` ✅ | longitud-peso-capacidad (3 ✅) · monedas-billetes (3 ✅) · el-reloj-en-punto (3 ✅) · dias-semana (3 ✅) · meses-del-ano (3 ✅) | **15** |
| `geometria` ✅ | figuras-planas (3 ✅) · cuerpos-geometricos (3 ✅) · lineas-y-situacion-espacial (3 ✅) | **9** |
| `estadistica` ✅ | tablas-simples (3 ✅) · pictogramas (3 ✅) | **6** |
| `problemas` ✅ | problemas-suma-sencillos (3 ✅) · problemas-resta-sencillos (3 ✅) · problemas-mixtos-basicos (3 ✅) | **9** |
| | **TOTAL 1º Mates COMPLETO ✅** | **71** |

> 1º Mates cerrado el **2026-05-28** con **71 fichas**. Cifra final aplicando la norma "ajustar fichas al material real disponible" (en 1º muchos conceptos no dan para 6 fichas distintas).
>
> **Norma crítica para problemas de 1º:** todas las sumas SIN llevadas (cada dígito sumado ≤9) y todas las restas SIN prestar (minuendo ≥ sustraendo en cada columna). Validar dígito a dígito antes de cerrar. Miguel detectó 25 operaciones con llevadas/prestar en la 1ª pasada y hubo que rehacer.

> En 2º+ la cantidad de sub-bloques crece porque entra multiplicación, división informal, fracciones, problemas de dos operaciones, sumas/restas con llevada, etc. 1º es el curso con menos sub-bloques de toda Primaria.

### Sub-bloques 2º Primaria — ACORDADO 2026-05-29 (EN MARCHA)

Árbol acordado con Miguel el 2026-05-29. Mismos 6 bloques que 1º. Serie = 6 fichas de referencia. **DIRECTRIZ 2º (Miguel):** hacer MÁS fichas que en 1º (las de 2º se usan más) y RELLENAR la página entera con apartados generosos. Ya alineado en `materiales.html`.

**Bloque `numeros` de 2º COMPLETO ✅ (21 fichas, cerrado 2026-05-29, en producción commit 57dce96):**
- `numeros-hasta-1000` (6): CDU · leer/escribir · formar+descomponer · descomponer · material base 10 · repaso
- `centenas-decenas-unidades` (3): equivalencias 1C=10D=100U, sumar/restar 10-100, valor posicional
- `comparar-y-ordenar` (3): signo >,<,= · ordenar · mayor/menor hasta 1000
- `pares-e-impares` (3) · `series-numericas` (3, de 2/5/10/50/100 asc-desc) · `numeros-ordinales` (3, 1º-20º)
- **⚠️ NUNCA usar `class="dato"` en celdas `<td>`** (la plantilla la usa en el header con `display:flex` → apila las celdas y rompe la tabla; usar clase propia).

| Bloque | Sub-bloques |
|---|---|
| `numeros` ✅ | numeros-hasta-1000 · centenas-decenas-unidades · comparar-y-ordenar · pares-e-impares · series-numericas · numeros-ordinales |
| `operaciones` | sumas-con-llevada · restas-con-llevada · sumas-y-restas-mezcladas · multiplicacion-concepto · tablas-de-multiplicar · doble-y-mitad |
| `medida` | longitud-metro-centimetro · peso-y-capacidad · el-reloj-horas-y-media · monedas-y-billetes · calendario |
| `geometria` | figuras-planas · cuerpos-geometricos · lineas-rectas-curvas-poligonales · simetria |
| `estadistica` | tablas-de-datos · graficos-de-barras · pictogramas |
| `problemas` | problemas-suma-con-llevada · problemas-resta-con-prestar · problemas-multiplicacion · problemas-dos-operaciones · problemas-mixtos |

**Estimación:** ~29 sub-bloques × 4-6 fichas ≈ 120-150 fichas.

**Diferencia clave vs 1º:** en 2º SÍ entran sumas/restas CON llevada y CON prestar. Se reutiliza el CSS `.problema` y los componentes de operaciones; solo cambian los números.

**Decisión pendiente** al llegar a `tablas-de-multiplicar`: ¿solo 2/5/10 o también 3/4? Preguntar a Miguel entonces.

**Bloque `operaciones` de 2º — EN MARCHA:**
- **`sumas-con-llevada` (4 fichas, en producción commit 2d1d1ec, 2026-05-29):** formato decidido por Miguel = **16 sumas verticales DU+DU por ficha, 4 por fila (rejilla 4×4), SIN explicaciones/Recuerda, con un círculo vacío sobre las decenas** para que el alumno anote la llevada. ficha-1 a ficha-4, números distintos. **Norma:** todas con llevada en unidades (U₁+U₂>9) y resultado ≤99 (una sola llevada U→D, sin acarreo a centenas). Generadas y verificadas dígito a dígito con script Python. CSS propio en `sumas-con-llevada/ficha-1.html` (clases `.sumas-grid`, `.op`, `.circ-fila`, `.circulo`, `.barra`).
- **`restas-con-llevada` (4 fichas, 2026-05-29):** clonado del formato de sumas pero **SIN el círculo arriba** (decisión de Miguel: las restas igual que las sumas pero sin círculo). 16 restas verticales DU−DU por ficha, rejilla 4×4, números distintos. **Norma:** todas CON prestar (unidad del minuendo < unidad del sustraendo) y decena del minuendo > la del sustraendo → resultado positivo de 1-2 cifras. Verificadas dígito a dígito con script Python. El `<div class="circ-fila">` eliminado del cuerpo (la regla CSS `.circulo`/`.circ-fila` queda sin usar, inofensiva).
- **⚠️ BUG corregido 2026-05-29:** el commit de sumas (2d1d1ec) subió las 4 fichas pero NO registró nada en `materiales.html` → la web no mostraba "Sumas con llevada" (sin entrada en `RECURSOS`, no aparece nada). Añadidas las entradas `matematicas|2|OPERACIONES|Sumas con llevada` y `…|Restas con llevada` (4 fichas cada una). **LECCIÓN: cada vez que se cierra un sub-bloque hay que registrar su entrada en `RECURSOS` de `materiales.html`, no solo subir las fichas.**

- **`sumas-y-restas-mezcladas` (4 fichas, 2026-06-01):** rejilla 4×4 de 16 operaciones DU±DU mezcladas (8 sumas con llevada + 8 restas con prestar, barajadas), sin círculo. Enunciado avisa "¡Fíjate bien en el signo!". Verificadas dígito a dígito. Registrado en `materiales.html`.
- **`multiplicacion-concepto` (6 fichas, 2026-06-01, commit 422cd5e):** primer contacto con la multiplicación, **visual y SIN tablas**. f1 suma de iguales↔multi · f2 grupos/veces (+dibujar grupos) · f3 filas×columnas (rejillas) · f4 conmutativa · f5 ×2/×1/×0 · f6 repaso. **Norma fijada:** siempre **veces × cantidad** + `.pista`/ejemplo resuelto para evitar ambigüedad de orden (la conmutativa no se ve hasta f4). CSS reusable: `.grupo`/`.punto`, `.grupo-vacio`, `.rejilla` (grid R×C), `.pista`, `.resp-fila.ejemplo`.
- **`tablas-de-multiplicar` (10 fichas, 2026-06-02, commit 8086ef4):** **Miguel decidió cubrir TODAS las tablas del 1 al 10** (no solo 2/5/10). 1 tabla por ficha + repaso, orden fácil→difícil: f1 (1 y 10) · f2→2 · f3→5 · f4→3 · f5→4 · f6→6 · f7→7 · f8→8 · f9→9 · f10 repaso. Cada ficha de tabla: Recuerda con TRUCO + completar la tabla + 8 cálculos desordenados + series (de N en N, ida/vuelta) + 2 problemas reales. Series en vez de descomposición en suma para no chocar con la convención veces×cantidad. Plantilla base: `tablas-de-multiplicar/ficha-1.html` (CSS `.tabla-mult`, `.serie`/`.cas`). f2-f10 generadas con script Python parametrizado (borrado tras generar). 1 folio A4 c/u validado (tablas 92-94% llenado, repaso 96%).

- **`doble-y-mitad` (5 fichas, 2026-06-09, commit 6e191cc):** **cierra el bloque `operaciones` de 2º.** f1 el doble (×2: sumar dos veces / ×2) · f2 la mitad (÷2, repartir en 2; solo los pares tienen mitad exacta, con cajas de reparto) · f3 doble y mitad juntos (operaciones contrarias, tabla nº→doble→mitad + completar el camino) · f4 6 problemas reales · f5 repaso página entera. Todas las mitades de números pares. CSS clonado del bloque (`.calc-grid`, `.resp-fila`, `.caja`, `.tabla-dm`, `.problema`). Validadas 1 folio A4 c/u con Chrome PDF + medición de llenado (footer al 99%). Registrado en `materiales.html`.

**BLOQUE `operaciones` DE 2º COMPLETO ✅** (33 fichas: sumas-con-llevada 4 + restas-con-llevada 4 + mezcladas 4 + multiplicacion-concepto 6 + tablas-de-multiplicar 10 + doble-y-mitad 5).

**Bloque `medida` de 2º — EN MARCHA:**
- **`longitud-metro-centimetro` (3 fichas, COMPLETO ✅, commit b4cb5e2, 2026-06-10):** metro/centímetro, 1 m = 100 cm. f1 elegir unidad (m/cm) + medir con **regla SVG** + medida lógica + conversión · f2 medir con regla + comparar >,<,= + ordenar menor→mayor + 2 problemas · f3 repaso (medir + equivalencias m↔cm + dibujar líneas con la regla + 2 problemas). **Regla SVG reusable:** viewBox 0 0 543 96, 33 px = 1 cm, objeto = `<rect>` gris desde x=24 (=0 cm); el largo del rect en px /33 da los cm. Verificar que cada objeto cae en marca exacta.
- **`peso-y-capacidad` (4 fichas, COMPLETO ✅, commit 14d4131, 2026-06-11):** f1 **el peso** (kilo/gramo, 1 kg = 1000 g) con **balanza SVG nueva** (platillos; el plato que baja pesa más) — elegir unidad + balanza + peso lógico + conversión · f2 **la capacidad** (el litro, 1 l = 2 medios litros) con **vaso SVG nuevo** (nivel de agua, polygon trapezoidal) — más/menos de 1 l + ordenar vasos por nivel + medio litro + 2 problemas · f3 **comparar y ordenar** (balanzas rodear el que pesa más + ordenar kg menos→más + vasos por nivel + signos > < = mezclando kg/l + ordenar l más→menos) · f4 **repaso** (elegir unidad kg/g/l + equivalencias 1kg=1000g / 1l=2 medios l + 4 problemas). Componentes SVG (balanza, vaso con nivel) aprobados por Miguel.
- **`el-reloj-horas-y-media` (4 fichas, COMPLETO ✅, commit 0bc2f8d, 2026-06-12):** reloj analógico SVG reutilizado de 1º (`el-reloj-en-punto`) con grosor correcto (**aguja hora gruesa-corta r=22, minutos fina-larga r=30**; coords con `punta(frac,r)`, frac=hora+0.5 para y media, larga al 6 = (50,80)). Concepto nuevo 2º: **y media** (larga al 6, corta entre dos números) y **cálculo ±media hora**. f1 explicativa (Recuerda + unir + escribir + dibujar + palabras→digital) · f2 práctica (+ rodear el reloj más tarde) · f3 aplicación (rutinas del día + ordenar por hora + media hora más tarde/antes) · f4 repaso. Generadas con scripts Python (`punta()` trig) borrados tras generar.
- **`monedas-y-billetes` (4 fichas, COMPLETO ✅, commit 351a5ab, 2026-06-12):** SVG dinero reutilizado de 1º (`monedas-billetes`) parametrizado por valor en `_lib.py` (`moneda_euro`/`moneda_cent`/`billete`/`mini_euro`/`mini_billete`), **billete 50€ nuevo**. f1 conocer y contar (valor de pieza + contar totales + comparar grupos + dibujar cantidad) · f2 contar carteras grandes 20/50€ + ¿quién tiene más? + unir grupo↔cantidad + problemas · f3 voy de compras (¿me llega? SÍ/NO + ¿cuánto falta? + dibujar pago justo) · f4 el cambio/la vuelta (devuelven = pago−cuesta) + 4 problemas. Sumas/restas en euros enteros (sin céntimos en los totales para no complicar). Scripts Python borrados tras generar.
- **`calendario` (4 fichas, COMPLETO ✅, commit 41bc493, 2026-06-12) — CIERRA el bloque `medida` de 2º.** En 1º eran sub-bloques separados `dias-semana`+`meses-del-ano`; en 2º van juntos con el avance clave de **leer un calendario mensual** (cuadrícula L-M-X-J-V-S-D generada en Python por `calendario(nombre, dias, primer_dia)`, con respuestas verificadas vía `dia_semana_de`). f1 días/meses + calendario de mayo + estación de cada mes + mes anterior/siguiente · f2 leer calendario de octubre (preguntas, domingos, fin de semana SÍ/NO, día anterior/siguiente) · f3 ayer/hoy/mañana + ¿cuántos días faltan? (resta) + equivalencias semana↔días + ordenar fechas · f4 repaso (calendario marzo) + 4 problemas. **Aprendizaje:** las fichas de calendario sin el componente cuadrícula quedan muy cortas → añadir siempre ≥4 ejercicios (días que faltan, equivalencias, ordenar) para llenar.

**Bloque `medida` de 2º COMPLETO ✅** (19 fichas): longitud-metro-centimetro (3) · peso-y-capacidad (4) · el-reloj-horas-y-media (4) · monedas-y-billetes (4) · calendario (4).

**Bloque `geometria` de 2º — EN MARCHA:**
- **`figuras-planas` (4 fichas, COMPLETO ✅, commit c964742, 2026-06-12):** avance clave de 2º = **polígonos, lados y vértices, pentágono y hexágono** (nuevos respecto a 1º). f1 Recuerda (6 tarjetas con vértices marcados con puntos; círculo = "NO es un polígono") + unir + contar lados/vértices + rodear pentágonos (mezclados con hexágonos ROTADOS para forzar contar lados) + V/F · f2 tabla nombre/lados/vértices + clasificar por nº de lados (banco) + dibujar polígonos de 3/4/5 lados + completar frases · f3 mundo real: unir objeto↔figura (señal, ventana, puerta, reloj, tuerca=hexágono — SVG nuevos) + **robot SVG compuesto** para contar figuras (2 triángulos, 1 cuadrado, 5 rectángulos, 5 círculos, 1 pentágono, 1 hexágono — verificado) + intruso (figuras rotadas) + continuar series dibujando · f4 repaso (nombrar con banco + unir nº lados + rodear solo polígonos + V/F + dibujar pentágono/hexágono con regla). **SVG pentágono/hexágono regulares reusables** (vértices sobre circunferencia r=24 centrada en viewBox 60×60; rotar con `transform="rotate(α 30 30)"`). Validadas 1 folio A4 (llenado 91-94%) con Chrome PDF + render PyObjC Quartz por página.
- **`cuerpos-geometricos` (4 fichas, COMPLETO ✅, 2026-06-12):** avance de 2º = **prisma y pirámide** (nuevos; SVG isométricos nuevos con aristas ocultas en discontinua) + **caras y vértices**. ⚠️ **Decisión de nivel (Miguel):** contar ARISTAS es de 3º — en 2º se presentan los 3 conceptos (cara/arista/vértice) pero la tabla solo pide contar caras y vértices; recuperar el conteo de aristas al hacer 3º. f1 Recuerda 6 cuerpos (4 de 1º + prisma/pirámide) + unir + rodear los que terminan en punta + completar + V/F · f2 Recuerda **cubo grande etiquetado** (CARA/ARISTA/VÉRTICE con flechas; "las líneas de puntitos también cuentan") + tabla caras/vértices (cubo 6/8, prisma 6/8, pirámide 5/5) + unir nº caras planas (cilindro 2, esfera 0, cono 1, cubo 6) + clasificar ruedan/no ruedan + V/F · f3 mundo real: unir objeto↔cuerpo (lata, pirámide Egipto, dado, cucurucho, caja zapatos, pelota — SVG objetos nuevos) + **escena de juguetes** (muñeco cono+esfera+cilindro+cubo, regalo prisma, pirámide juguete, cono tráfico, pelota → contar: 1/1/1/2 esferas/1/2 conos, verificado) + intruso + **adivinanzas** ("Tengo 6 caras iguales…") · f4 repaso (nombrar con banco + unir cuerpo↔figura plana de sus caras + rodear NO ruedan + V/F + dibujar objeto real de cada cuerpo). Llenados 91-94%.

- **`simetria` (4 fichas, COMPLETO ✅, 2026-06-12) — generadas con 4 AGENTES EN PARALELO** (decisión de Miguel: "todas de una vez, un agente por ficha"). Sub-bloque NUEVO en 2º (no existía en 1º). f1 introducción (Recuerda eje/espejo + ¿es simétrica? SÍ/NO + ¿eje bien trazado? ✓/✗ + V/F) · f2 **"dibuja la otra mitad"** — 6 cuadrículas pixel-art con eje vertical discontinuo (celdas 16px, rejilla #bbb, mitad izquierda en trazo grueso tocando el eje; figuras: pedestal, escalera, casa, flecha, abeto, cohete) · f3 ejes/letras/figuras (trazar eje + letras simétricas A-H-M-O vs F-L-R-S + figuras con eje + 2 espejos en cuadrícula + V/F) · f4 repaso (SÍ/NO nuevos + trazar ejes + 2 espejos + V/F + **"inventa TU figura simétrica"** en cuadrícula grande vacía).
- **`lineas-rectas-curvas-poligonales` (4 fichas, COMPLETO ✅, 2026-06-12) — también con agentes en paralelo. CIERRA el bloque `geometria` de 2º.** Avance de 2º: la **línea poligonal** (trozos rectos, abierta/cerrada). ⚠️ Nivel acotado por Miguel ("cuidado con el nivel"): SIN paralelas/secantes/perpendiculares (3º). f1 introducción (Recuerda 4 tipos + unir + rodear poligonales + ABIERTA/CERRADA + V/F) · f2 práctica (tabla marcar X recta/curva/poligonal + contar trozos rectos con vértices punteados + rodear cerradas/tachar abiertas + dibujar con regla) · f3 mundo real (**escena los 3 caminos al cole** A recta/B curva/C poligonal + el más corto + poligonal cerrada↔polígono que forma + **unir puntos numerados con regla** rombo/casa + V/F) · f4 repaso (nombrar con banco + clasificar abiertas/cerradas por letras + contar trozos + V/F + camino poligonal de 4 trozos SALIDA→META).

**BLOQUE `geometria` DE 2º COMPLETO ✅** (16 fichas: figuras-planas 4 + cuerpos-geometricos 4 + lineas 4 + simetria 4).

**Bloque `estadistica` de 2º COMPLETO ✅ (12 fichas, cerrado 2026-06-13):** generado con el patrón de agentes en paralelo / script parametrizado (validación PDF/llenado en lote con `/tmp/validar_ficha.py`, Chrome headless + PyObjC Quartz + PIL; ⚠️ "llenado" = **extensión VERTICAL** del contenido, no densidad de tinta — rango sano 88-99%).
- **`tablas-de-datos` (4 fichas, COMPLETO ✅, commit 8772b68, 2026-06-12):** avances de 2º = **recuento con palotes** + **tabla de doble entrada** + preguntas con suma/llevada y resta/prestar. **Componente SVG palotes nuevo reusable** (`.palote5` grupo de 5 con el quinto cruzado, `.palote1` suelto, `.recuento`). f1 recuento con palotes (Recuerda 1/3/5/7 + mosaico 18 mascotas 7/6/5 + leer palotes 12/8/4/10 + preguntas + V/F) · f2 leer/completar tablas con números grandes (cuentos 24/17/31/9: 24+17, 31−9; granja 15/12/8/20 + ordenar + V/F) · f3 **tabla de doble entrada** (Recuerda con celda cruzada resaltada + recreo niños/niñas + columna TOTAL + bocadillos 2ºA/2ºB con operaciones) · f4 repaso página entera (palotes frutas 6/4/3/3 + doble entrada granjas con TOTAL + ordenar + V/F).
- **`graficos-de-barras` (4 fichas, COMPLETO ✅, 2026-06-13):** avance estrella de estadística en 2º. **Componente SVG nuevo reusable: gráfico de barras vertical** — viewBox `0 0 320 196`, rejilla `#bbb` cada 20px (1 unidad), eje 0-8, barra = `rect` con `y=170−20·v`/`height=20·v` fill `#d6d6d6`, etiquetas y=186; **variante vacía** con columnas guía punteadas (`stroke-dasharray 4,3`) para que el alumno dibuje. Escala SIEMPRE 1 cuadrado = 1 (la escala de 2 en 2 es de 3º). f1 leer (Recuerda + mini-gráfico helados + mascotas 7/5/3/6) · f2 dibujar barras desde tabla (frutas 6/4/7/3 + deportes 8/5/2) · f3 leer/comparar/calcular (libros por día 4/6/2/5/8 + operaciones + ordenar 5 puestos) · f4 repaso (leer helados 5/7/8/4 + dibujar flores 6/8/5 + V/F).
- **`pictogramas` (4 fichas, COMPLETO ✅, commit d096d94, 2026-06-13) — CIERRA el bloque `estadistica` de 2º.** Escala 1 dibujo = 1 (la escala de 2 en 2 es de 3º, igual criterio que gráficos de barras). Reutiliza los SVG de 1º (frutas manzana/plátano/pera, mascotas perro/gato/pez, transportes coche/bici/avión/barco). Avance de 2º: números hasta 9, preguntas con suma/resta, columna **TOTAL**, **4 categorías** y ordenar 4 puestos. f1 frutas intro (Recuerda + leer/completar + responder + dibujar) · f2 mascotas (perro 7/gato 5/pez 9, tabla con TOTAL + dibujar + ordenar MENOS→MÁS) · f3 transportes 4 cat (coche 8/bici 6/avión 3/barco 5, comparar + V/F 5 + ordenar MÁS→MENOS 4 puestos) · f4 repaso. **Generadas con `/tmp/gen_pictogramas.py`** (script parametrizado, borrado tras generar — garantiza el conteo exacto de iconos por fila; mejor que agentes para fichas con mucha repetición de SVG idénticos).
- ⚠️ Lección validación: pasar SIEMPRE ruta absoluta a `validar_ficha.py` — con ruta relativa y CWD cambiado, Chrome genera un PDF de error (ERR_FILE_NOT_FOUND) que mide ~37% y confunde.

**Bloque `estadistica` DE 2º COMPLETO ✅** (12 fichas: tablas-de-datos 4 + graficos-de-barras 4 + pictogramas 4).

**Bloque `problemas` de 2º COMPLETO ✅ (30 fichas, cerrado 2026-06-14) — ÚLTIMO bloque de 2º. Serie = 6 fichas.**
- **`problemas-suma-con-llevada` (6 fichas, COMPLETO ✅, commit ca3f3e2, 2026-06-13) — abre el bloque.** Generadas con **6 agentes en paralelo (1 por ficha)** de fácil→difícil (método que pidió Miguel para este sub-bloque). Reusan `ficha-1` como plantilla (componente `.problema` con zona OPERACIÓN + SOLUCIÓN, clonado de 1º). f1 2 sumandos DU+DU ≤99 + Recuerda + dibujos · f2 refuerzo · f3 ≤99 números altos (6 problemas, sin Recuerda, los últimos sin icono `grid-template-columns:1fr`) · f4 **tres sumandos** ≤99 · f5 resultado **pasa de 100** (llevada a centenas, avisada en Recuerda) · f6 repaso mezcla (6 problemas). **Números fijados por mí y verificados dígito a dígito** (llevada en unidades garantizada); los agentes solo redactan enunciados + montan HTML. ⚠️ **Nivel 2º:** la llevada doble (a centenas) solo aparece en f5/f6 y SIEMPRE avisada en Recuerda.
- **`problemas-resta-con-prestar` (6 fichas, COMPLETO ✅, 2026-06-13).** Mismo método (6 agentes en paralelo, 1/ficha, fácil→difícil, que pidió Miguel). **Números fijados por mí y verificados dígito a dígito con script Python: TODAS prestan en unidades (U del minuendo < U del sustraendo) y resultado positivo.** f1 DU−DU básico + Recuerda + dibujos · f2 refuerzo · f3 números altos hasta 99 (6 problemas, sin Recuerda) · f4 **comparación** (¿cuántos más?/¿cuánto falta? → también se resuelve restando) · f5 **restar a números de 3 cifras** (minuendo >100, préstamo único en U, resultado de 3 cifras; avanzado pero adaptado a 2º, SIN doble préstamo) · f6 repaso mezcla (6 problemas, 1 sin icono). Registrado en `materiales.html` (entrada `matematicas|2|PROBLEMAS|Problemas de resta con prestar`).
- ⚠️ **LECCIÓN llenado/impresión (2026-06-13):** las fichas de `.problema` a 90-99% de llenado (medido en Chrome headless `validar_ficha.py`) **se van a 2 páginas POR POCO al imprimir en Safari/diálogo de impresión** (mete su propio margen; Chrome headless NO lo reproduce, dice 1 página). Corregido TODO el bloque (suma+resta, 12 fichas) bajando `.problemas gap 13→9`, `.problema padding 9px→6px`, `.zona min-height 60→54` → llenado **~85-92% con aire bajo el footer**. **NORMA mates problemas: apuntar a 85-92%, NO 95-99%.** El "OK hasta 99%" del validador es engañoso para impresión real.

- **`problemas-multiplicacion` (6 fichas, COMPLETO ✅, 2026-06-14).** ficha-1 hecha a mano (ancla + sirvió para diagnosticar el arreglo de impresión Safari). f1 grupos iguales (Recuerda "veces × cantidad") · f2 más grupos · f3 filas×columnas (Recuerda) · f4 doble/triple (Recuerda) · f5 productos mayores (7x4..4x8) · f6 repaso. Convención "veces × cantidad", productos de tablas 1-10.
- **`problemas-dos-operaciones` (6 fichas, COMPLETO ✅, 2026-06-14).** Problemas de DOS pasos SOLO suma/resta (combinar con multiplicación es 3º). Zona OPERACIÓN ampliada `min-height:78px` para las dos cuentas. f1 intro nº bajos (Recuerda 2 pasos) · f2-f5 progresión (dos sumas/restas, comparar, nº mayores) · f6 repaso. Internamente las fichas se titulan "dos pasos"; el subBloque en materiales.html es "Problemas de dos operaciones".
- **`problemas-mixtos` (6 fichas, COMPLETO ✅, 2026-06-14) — CIERRA 2º.** Mezcla **suma + resta + multiplicación** (decisión de Miguel: repaso total de 2º). ⚠️ Los enunciados NO revelan la operación (el alumno decide); f1 Recuerda con palabras pista. f6 = repaso final de 2º.
- **MÉTODO (2026-06-14):** las 17 fichas que faltaban (mult 2-6 + dos-op 1-6 + mixtos 1-6) se generaron con un **WORKFLOW de 17 agentes en paralelo, 1 ficha por agente** (Miguel: "¿te ves capaz de lanzar 17 agentes...?"). Números fijados y verificados por mí en el script; cada agente clona la plantilla corregida, redacta enunciados, elige iconos y ajusta el llenado. Validación EN LOTE (las 17 a 1 página + arreglo de impresión presente + muestra visual). Las 3 keys registradas en RECURSOS de `materiales.html`. Commit 59f53fc.
- ⚠️ **ARREGLO IMPRESIÓN SAFARI (2026-06-14):** Miguel reportó que al imprimir "desbordaba por la derecha y no se veía la línea del rectángulo". El CSS era idéntico en las 13 fichas y en Chrome salían perfectas → bug de Safari, que NO respeta `@page{margin}` (pone el body a ancho de A4 y recorta el borde derecho al meter su propio margen). **FIX: `@page{ size:A4 portrait; margin:0 }` + en `@media print` `body{ max-width:15cm !important; margin:2cm auto 1.5cm !important }`** (margen vía body; mismo aspecto en Chrome, verificado por Miguel en Safari). Aplicado primero a las 30 fichas de problemas de 2º (commit d466664 las 12 de suma+resta; las 18 nuevas ya nacieron con el fix) y luego, tras barrido, a **las 172 restantes de Mates Primaria** (commit e69e24f) → **las 202 fichas de Mates Primaria ya migradas**. ⚠️ **DEUDA: solo queda Lengua (~620 fichas) con `@page margin:3cm` → mismo recorte potencial en Safari. NO migrado (trabajo grande, distintas plantillas/anchos).**

**Arrancar por:** ~~`numeros`~~ ✅ (21) → ~~`operaciones`~~ ✅ (33) → ~~`medida`~~ ✅ (19) → ~~`geometria`~~ ✅ (16) → ~~`estadistica`~~ ✅ (12) → ~~`problemas`~~ ✅ (30: suma 6 + resta 6 + multiplicacion 6 + dos-operaciones 6 + mixtos 6). **2º MATES COMPLETO ✅ (131 fichas, 2026-06-14).**

### Sub-bloques 3º Primaria — ACORDADO 2026-06-15 (EN MARCHA)

Árbol acordado con Miguel el 2026-06-15. Mismos 6 bloques. Serie = 6 fichas. **⚠️ 3º usa fuente Poppins** (no Edu SA Beginner, que es solo 1º-2º). Plantilla base: `recursos/primaria/3/matematicas/numeros/numeros-hasta-10000/ficha-1.html` (clonada de la de 2º, fuente cambiada a Poppins, arreglo impresión Safari incluido). back-btn = 6 niveles `../../../../../../materiales.html`.

**Decisiones de NIVEL (Miguel):** decimales → **aplazados a 4º** (en 3º NO) · fracciones → **concepto + sumar/restar mismo denominador** · división → **una cifra, exacta Y con resto** (división por dos cifras es 4º).

| Bloque | Sub-bloques |
|---|---|
| `numeros` ✅ | numeros-hasta-10000 ✅ · valor-posicional-y-descomposicion ✅ · comparar-y-ordenar ✅ · numeros-romanos ✅ · las-fracciones ✅ · sumar-y-restar-fracciones ✅ |
| `operaciones` ✅ | sumas-y-restas-llevando ✅ · multiplicacion-por-una-cifra ✅ · multiplicacion-por-dos-cifras ✅ · propiedades-y-calculo-mental ✅ · la-division-concepto-y-reparto ✅ · division-por-una-cifra ✅ |
| `medida` ✅ | longitud-km-m-cm-mm ✅ · masa-kilo-gramo ✅ · capacidad-litro-mililitro ✅ · el-reloj-y-los-minutos ✅ · el-dinero-euros-y-centimos ✅ · superficie ✅ |
| `geometria` ⏳ EN MARCHA | rectas-paralelas-secantes-perpendiculares ✅ · los-angulos ✅ · poligonos-y-triangulos ⏳ SIGUIENTE · circunferencia-y-circulo · el-perimetro |
| `estadistica` | tablas-de-datos · graficos-de-barras · pictogramas · graficos-lineales · probabilidad |
| `problemas` | problemas-suma-y-resta · problemas-multiplicacion · problemas-division · problemas-dos-operaciones · problemas-mixtos |

**Bloque `numeros` de 3º — EN MARCHA:**
- **`numeros-hasta-10000` COMPLETO ✅ (6 fichas, cerrado 2026-06-15, commits 6b84320/88ebe68/5f050fc):** f1 UM·C·D·U (descomponer en tabla, formar, descomponer en suma, serie de 1.000 en 1.000) · f2 leer y escribir números (cifra↔letra, unir lecturas, ¿qué número es?) · f3 formar y descomponer · f4 descomponer con ceros + ¿qué número soy? (adivinanzas + inventa tú) · f5 el millar y equivalencias (1 UM=10 C=100 D=1.000 U) · f6 repaso (mayor/menor, ordenar, series, anterior/posterior). f1 a mano (ancla); f2-f6 con **5 agentes en paralelo (1/ficha), números fijados por mí** (agentes solo redactan+montan clonando f1). 1 folio A4 c/u (92-95%). Registradas en RECURSOS de materiales.html. ⚠️ Reparto: `numeros-hasta-10000` cubre leer/escribir/formar/descomponer/equivalencias/series; el **valor posicional puro** y **comparar/ordenar formal** van en sus sub-bloques propios para no duplicar.

- **`valor-posicional-y-descomposicion` COMPLETO ✅ (6 fichas, cerrado 2026-06-15, commit 54f9e79):** sub-bloque del **valor posicional puro** (cuánto vale cada cifra según su posición, sin duplicar el "5 C" de numeros-hasta-10000). f1 el valor de cada cifra (cifra marcada con recuadro `.cm` + tabla valor por posición + descomp. en suma + misma cifra distinto valor) · f2 práctica sin Recuerda (cifra marcada + cifra que ocupa cada posición + rodear cifra pedida + V/F) · f3 descomponer y componer (número→suma y suma→número + unir + completar sumando) · f4 **descomposición multiplicativa** (3×1.000 + 5×100 + 8×10 + 2×1; concepto nuevo de 3º, con Recuerda) · f5 el cero (valor 0, no se escribe en la suma) + adivinanzas "¿qué número soy?" + inventa tú · f6 repaso. f1 a mano (ancla); f2-f6 con **5 agentes en paralelo (1/ficha), números fijados y verificados por mí** (agentes solo redactan+montan clonando f1). 1 folio A4 c/u (82-91%; hubo que comprimir f3/f4/f5 que salieron a 98%/2-páginas — bajar alturas de caja+gaps). Registradas en RECURSOS de materiales.html. Clase nueva reusable `.cm` (cifra marcada con recuadro gris).

- **`comparar-y-ordenar` COMPLETO ✅ (6 fichas, cerrado 2026-06-15, commit 5d52ee4):** sub-bloque 3 de numeros. f1 el signo >,<,= (Recuerda "el signo abierto mira al mayor / el pico al menor" + comparar de izda a dcha + parejas + rodear mayor/menor + V/F) · f2 práctica sin Recuerda (signo + **completar la cifra que falta** para que sean iguales / para que la desigualdad sea verdadera + rodear mayor de cada trío) · f3 **ordenar** menor→mayor y mayor→menor (bancos desordenados + secuencia de cajas con < o > + numerar puesto 1-4) · f4 **anterior/posterior** (tabla) + **intercalar** un nº entre dos + completar series de 1 en 1 (cruzando millares) · f5 **la recta numérica** (completar de 100 en 100 y de 10 en 10) + **formar el mayor/menor nº con unas cifras** + ¿entre qué millares? · f6 repaso. f1 a mano (ancla) + f5 a mano (lleva la recta, componente nuevo); f2/f3/f4/f6 con **4 agentes en paralelo (1/ficha), números fijados y verificados por mí**. ⚠️ **LECCIÓN SAFARI (commit 1578b1e, confirmada por Miguel):** salieron a 85-89% de llenado y 5 de 6 se iban a **2 páginas al imprimir en Safari**. Causa: los agentes (y yo en f5) habíamos inflado el AIRE VERTICAL (ej-block 30px, cajas altas) para llegar al 85-89% — espacio en blanco, no contenido; Safari mete su propio margen y desborda. El umbral de fallo está en **~85% Chrome-medido** (f4 a 85.6% aguantaba, f2 a 85.7% no). Fix: recortar gaps/alturas de las 6 a **78-82%**. **NORMA para fichas full-page de 3º (Poppins): apuntar a 78-82%, NO a 85-89%. No rellenar el folio inflando espacios en blanco — solo con contenido real.** Registradas en RECURSOS de materiales.html. Clases nuevas reusables: `.recta-num`/`.rn-puntos`/`.rn-pt` (recta numérica con ticks), `.cifras-banco`/`.dig`/`.caja-num` (formar nº con cifras), `.orden-banco`/`.orden-secuencia` (ordenar), `.ap-tabla` (anterior/posterior), `.cifra-box` (hueco de una cifra dentro de un número).

- **`numeros-romanos` COMPLETO ✅ (6 fichas, cerrado 2026-06-17, commit 97be83d):** sub-bloque 4 de numeros. Alcance acordado con Miguel: **los 7 símbolos completos (I·V·X·L·C·D·M) + reglas de suma/resta, hasta el 1.000, con siglos y relojes.** f1 conoce los 7 símbolos (tabla `.simbolos` + reglas suma/resta + leer/escribir 1-20) · f2 la regla de la resta a fondo (IV·IX·XL·XC·CD·CM + "rodea el bien escrito" IIII vs IV) · f3 hasta el 100 (decenas combinadas + ordenar menor→mayor) · f4 centenas y hasta 1.000 (C·D·M, números grandes 444=CDXLIV, 999=CMXCIX) · f5 aplicación en la vida real (siglos, reyes Carlos III/Felipe VI, reloj romano, ordenar siglos) · f6 repaso (mezcla + Año MM=2000). f1 a mano (ancla); f2-f6 con **5 agentes en paralelo (1/ficha), todas las conversiones romanas fijadas y verificadas por mí** (agentes solo redactan+montan clonando f1). Todo texto, **sin SVG**. Clases nuevas reusables: `.simbolos`/`.sim-cel` (tabla de símbolos), `.conv-lista`/`.conv-item`/`.caja` (cifra↔romano), `.banco`/`.orden-cajas`/`.caja-o` (ordenar), `.par-lista`/`.par-item` (rodear el correcto). ⚠️ **LECCIÓN VALIDADOR (2026-06-17):** el `validar_ficha.py` recreado medía INESTABLE (misma ficha 81% u 87% según si Poppins cargaba por red antes del render). **FIX: añadir `--virtual-time-budget=4000` al Chrome headless** → espera a las fuentes y mide determinista (siempre con Poppins, el caso real de impresión). Con la medida estable, los agentes habían quedado altos (inflando `.ej-block margin-bottom` hasta 22px = aire, justo lo prohibido) → normalizadas a los gaps base de f1, llenado final **75-82%** (f3/f4/f5 a 75-76% del lado seguro, f1/f2/f6 78-82%). 1 folio A4 c/u.

- **`las-fracciones` COMPLETO ✅ (6 fichas, cerrado 2026-06-17, commit 6e197db):** sub-bloque 5 de numeros. **Concepto de fracción, SIN operar** (sumar/restar va en el sub-bloque siguiente). f1 ¿qué es una fracción? (Recuerda con tarta ¼ + numerador/denominador + escribir fracción de barra coloreada + colorear + unir lectura + completar) · f2 leer y escribir (mini-Recuerda con nombres /2 medios…/10 décimos + frac↔palabra en ambos sentidos + unir) · f3 representar (colorear en **tartas** y barras + escribir la fracción de figuras coloreadas + "divide tú la barra con la regla" + V/F) · f4 la fracción de una cantidad sencilla (1/2 de 8 con puntos a rodear + 1/3 de 9, 1/4 de 12… + 3 problemas + V/F) · f5 comparar igual denominador (con barras + signo >,<,= + la unidad n/n=1 + ordenar) · f6 repaso. f1 a mano (ancla) + **f3 a mano** (lleva el componente círculo/tarta nuevo); f2/f4/f5/f6 con **4 agentes en paralelo (1/ficha), números fijados y verificados por mí**. **Componentes nuevos reusables:** `.barra-frac`/`.celda`/`.celda.on` (barra dividida, celdas coloreadas), `.frac` (fracción escrita num/línea/den), `.frac-caja` (huecos num/den para rellenar), `.barra-entera` (barra sin dividir), y **tarta SVG** (círculo r=27 en viewBox 64 dividido en N sectores con radios + M coloreados `#cfcfcf`; generador `/tmp/gen_circulos.py` con `punto(a)=(32+27·sin a, 32−27·cos a)`, sector = `M32,32 L p(a0) A27,27 0 large 1 p(a1) Z`). Validador estable con `--virtual-time-budget=4000`; llenado final 78-84% (f1 81.5, f2 83.5, f3 82.7, f4 83.8, f5 78.3, f6 80.7).

- **`sumar-y-restar-fracciones` COMPLETO ✅ (6 fichas, cerrado 2026-06-20, commit be272ab) — CIERRA el bloque `numeros` de 3º.** Nivel acordado: sumar/restar con el **MISMO denominador**. f1 sumar (Recuerda con barras 1/5+2/5=3/5 + sumar mirando partes coloreadas + calcular + completar numerador + V/F) · f2 sumar práctica (calcular + **tres sumandos** + completar + 1 problema) · f3 restar (Recuerda con barras 4/5−1/5=3/5 + tachar celdas + calcular + completar + V/F) · f4 restar práctica (calcular + **"¿cuánto falta para llegar?"** + completar + 1 problema) · f5 sumar/restar mezclado + **la unidad n/n=1** (Recuerda 5/5=8/8=3/3=1 + fíjate en el signo + completar para llegar a 1 + problema 2 apartados) · f6 repaso (calcular + completar + 4 problemas reales). **Norma de nivel respetada:** todas las sumas dan resultado ≤ denominador (o =1 cuando el tema lo pide en f5), todas las restas positivas, denominador SIEMPRE constante — verificado operación a operación. f1 a mano (ancla); f2-f6 con **4 agentes en paralelo (1/ficha), números fijados y verificados por mí**. Reusa los componentes de `las-fracciones` (`.frac`, `.frac-caja` con variante `.fijo` para denominador dado, `.barra-frac`/`.celda.on`, `.prob`). Validador con `--virtual-time-budget=4000`: 1 folio A4 c/u, llenado 79-82% (f1 82.1, f2 81.8, f3 81.9, f4 79.7, f5 80.0, f6 79.2). Registradas en RECURSOS de materiales.html.

**BLOQUE `numeros` DE 3º COMPLETO ✅** (36 fichas: numeros-hasta-10000 6 + valor-posicional-y-descomposicion 6 + comparar-y-ordenar 6 + numeros-romanos 6 + las-fracciones 6 + sumar-y-restar-fracciones 6).

**Bloque `operaciones` de 3º — EN MARCHA:**
- **`sumas-y-restas-llevando` COMPLETO ✅ (6 fichas, cerrado 2026-06-20, commit 9dcdd59) — abre el bloque `operaciones` de 3º.** Repaso/consolidación de sumas y restas llevando con números hasta 4 cifras (≤9999). f1 sumas 3 cifras (8 verticales colocadas + 6 cuadrículas "coloca y resuelve" — **2 ejercicios, sin tercero**, decisión de Miguel: nada de "rodear las bien resueltas") · f2 sumas 4 cifras + **tres sumandos** (Ej2 verticales de 3 sumandos) · f3 restas 3 cifras (prestar) · f4 restas 4 cifras + **la prueba de la resta** (Ej2 resta→prueba sumando, diferencia+sustraendo=minuendo) · f5 sumas y restas **mezcladas** (¡fíjate en el signo!) · f6 repaso (mezcla 3/4 cifras) + 3 problemas reales (componente `.problema`). f1 a mano (ancla); f2-f6 con **5 agentes en paralelo (1/ficha), números fijados y verificados por mí dígito a dígito** (todas las sumas con llevada, todas las restas con préstamo y positivas). Validador `--virtual-time-budget=4000`: 1 folio A4 c/u, **llenado 78-82%** (f1 79.2, f2 81.9, f3 78.3, f4 82.0, f5 79.2, f6 79.2). **Componentes nuevos reusables:** `.op`/`.sumas-grid`/`.fila`/`.barra` (operación vertical en rejilla — para 4 cifras: `grid-template-columns: 22px 24px 24px 24px 24px` + barra `grid-column: 2/6`, clase `.op4`), `.coloca-grid`/`.coloca-item`/`.rejilla`/`.cel`/`.res`/`.sig` (cuadrícula vacía para colocar y operar), `.rec-op`/`.lleva` (operación de muestra resuelta en el Recuerda con las llevadas arriba). Registradas en RECURSOS de materiales.html.

- **`multiplicacion-por-una-cifra` COMPLETO ✅ (6 fichas, cerrado 2026-06-21, commit 08f2ba7) — segundo sub-bloque de `operaciones` de 3º.** Multiplicar número de 2-3 cifras × 1 cifra. f1 DU×U **sin llevar** (ancla, Recuerda con 32×3=96) · f2 DU×U **con llevada** (la llevada anotada arriba en el Recuerda, 27×3=81) · f3 **CDU×U** (3 cifras × 1 cifra, resultados de 3 cifras, 124×3=372) · f4 **números con ceros** (terminados en 0: 40×6; con cero intermedio: 203×3 — la llevada cae sobre el 0) · f5 **"coloca y multiplica"** (12 cuadrículas vacías, mezcla DU/CDU, SIN Recuerda) · f6 **repaso + 3 problemas** reales (componente `.problema`: 24×3, 45×2, 125×4). **Números verificados dígito a dígito por mí** (todas las "con llevada" generan llevada en unidades; resultados de 3 cifras en CDU). f1 a mano (ancla); f2-f6 con **5 agentes en paralelo (1/ficha)**, los agentes solo clonan f1 + montan con mis números. **Reutiliza el CSS de `sumas-y-restas-llevando` SIN cambios** (`.op`/`.sumas-grid`/`.fila`/`.barra` con signo `×` en vez de `+`; el factor se alinea a la derecha y el multiplicador bajo las unidades — col 4 del grid de 4; `.coloca-grid`/`.rejilla` para cuadrículas; `.rec-op`/`.lleva` para la llevada de muestra). 1 folio A4 c/u. ⚠️ **Validador recreado esta sesión** (`/tmp/validar_ficha.py` con Quartz + `--virtual-time-budget=4000`): **satura a "92.9%" para todas** porque mide la posición del footer (casi constante), NO el % de llenado vertical real — sirve para confirmar **1 folio sí/no** pero NO da resolución fina; la verificación de densidad/alineación se hizo por **render visual** (Quartz PDF→PNG con `/tmp/pdf2png.py`). El llenado visual real ronda 75-78% (lado seguro Safari). Registradas en RECURSOS de materiales.html.

- **`multiplicacion-por-dos-cifras` COMPLETO ✅ (6 fichas, cerrado 2026-06-21, commit 1c40c24) — tercer sub-bloque de `operaciones` de 3º.** Alcance acordado con Miguel: **DU×DU primero, luego CDU×DU** (3 cifras × 2 cifras). f1 **DU×DU sin llevar** (ancla, Recuerda 23×12=276 con los dos productos parciales y notas laterales ← 23×2 / ← 23×1 decena) · f2 **DU×DU con llevada** (37×24=888) · f3 **CDU×DU** (213×12=2556) · f4 **con ceros** (cero intermedio/terminado en 0: 203×13=2639) · f5 **"coloca y multiplica"** (12 cuadrículas vacías, mezcla DU/CDU, SIN Recuerda) · f6 **repaso + 3 problemas** reales (componente `.problema`, zona OPERACIÓN min-height:78px para los dos renglones: 24×13, 32×15, 125×12). **Números verificados dígito a dígito por mí** (f1 sin acarreo en los productos parciales ni en la suma; f2+ con llevada). f1 a mano (ancla); f2-f6 con **5 agentes en paralelo (1/ficha)**, los agentes solo clonan f1 + montan con mis números. **Componente NUEVO reusable: operación de dos productos parciales** — `.op .barra { height: 94px }` reserva el espacio en blanco para que el alumno escriba pp1 + pp2 + barra + resultado; `.ops-grid` (3 columnas) en vez de `.sumas-grid`; el grid `.op .fila` es de 5 columnas `22px + 4×24px` (signo + UM C D U): multiplicando DU ocupa D,U / CDU ocupa C,D,U / multiplicador DU bajo las unidades. **Recuerda con dos renglones:** `.rec-op .fila` de 5 cols (signo+C+D+U+nota) para resultados de 3 cifras; **para f3/f4 (CDU×DU, resultado 4 cifras) se amplía a 6 cols** (signo+UM+C+D+U+nota) y `.rec-op .barra` a `grid-column: 2/6`; el segundo producto parcial va corrido un lugar a la izquierda (hueco en U) con `.nota` "← N × 1 (decena)". Cuadrícula `.coloca-grid`/`.rejilla` de f1 ampliada a **5 filas** (multiplicando, ×multiplicador, pp1, +pp2, resultado). 1 folio A4 c/u (validador satura a 92.9% = solo confirma 1-folio sí/no; densidad verificada por render visual `/tmp/pdf2png.py`). Registradas en RECURSOS de materiales.html.

- **`propiedades-y-calculo-mental` COMPLETO ✅ (6 fichas, cerrado 2026-06-21, commit 412ee86) — cuarto sub-bloque de `operaciones` de 3º.** **Decisión de nivel (Miguel): la propiedad distributiva se APLAZA a 4º** (en 3º solo conmutativa, asociativa, neutro). Sub-bloque **conceptual** (no más operaciones verticales) → librería de componentes nueva. f1 **propiedad conmutativa** (ancla: suma y multiplicación, el orden no cambia el resultado; ⚠️ NO en la resta) · f2 **propiedad asociativa de la suma** (agrupar como quiera; agrupar primero los que suman 10) · f3 **elemento neutro** (+0, ×1) + **×0** + **×10 y ×100** (añadir ceros) · f4 **cálculo mental I** (sumar/restar decenas y centenas completas + truco del 9: +10 −1) · f5 **cálculo mental II** (dobles y mitades, descomponer para sumar 25+13=25+10+3, ×20/×200) · f6 **repaso + 3 problemas** (componente `.prob` ligero: enunciado + caja resultado). Números fijados y verificados por mí (cajas vacías). f1 a mano (ancla) + f2-f6 con **5 agentes en paralelo (1/ficha)**. **Componentes nuevos reusables** (todos en el `<style>` de f1, los agentes lo clonan entero): `.hueco`/`.hueco.ancha` (caja cuadrada/ancha para escribir un número), `.igs`/`.ig` (igualdades en rejilla 2 col; variante `.igs.una` 1 col para caminos largos tipo "35+9=35+10−1=☐"), `.dosf`/`.par`/`.l` (calcula de las dos formas), `.une`/`.col`/`.chip` (unir dos columnas con flecha, sin línea guía), `.vf-lista`/`.vf`/`.op`/`.opt`/`.o` (verdadero/falso con cajas V·F), `.rec-ej`/`.rl` (ejemplo resuelto en el Recuerda), `.prob-lista`/`.prob`/`.res` (problema mental: texto + caja resultado). Validador con `--virtual-time-budget=4000`: 1 folio A4 c/u (satura a 92.9% = solo confirma 1-folio sí/no; densidad verificada por render visual `/tmp/pdf2png.py`, todas con buen aire bajo el footer). Registradas en RECURSOS de materiales.html.

- **`la-division-concepto-y-reparto` COMPLETO ✅ (6 fichas, cerrado 2026-06-21, commit c2b6f46) — quinto sub-bloque de `operaciones` de 3º.** **El CONCEPTO de división, SIN el algoritmo de la casita** (la casita va en el siguiente sub-bloque). Miguel avisó de que la división "siempre te ha costado colocarla bien" → aquí **TODO va en horizontal** (`12 ÷ 3 = 4`), cero alineación vertical de cifras, así que no hay riesgo. f1 **dividir es repartir** (ancla: reparto visual con puntos en cajas + términos dividendo/divisor/cociente) · f2 **dividir es agrupar** (¿cuántos grupos de N caben? grupos hechos + rodear grupos en fila de puntos) · f3 **× y ÷ inversas** (familias de operaciones + usar la multiplicación para dividir + unir × con su ÷ de la misma familia) · f4 **los términos y la prueba** (identificar dividendo/divisor/cociente + comprobar con cociente×divisor=dividendo) · f5 **la división con resto** (reparto que sobra: cociente y resto, con puntos sobrantes fuera de las cajas + rodear las exactas) · f6 **repaso + 3 problemas** reales (componente `.problema` reusado de multiplicacion-por-una-cifra). **Hecha A MANO entera (NO agentes), una a una**, por la sensibilidad de la división que avisó Miguel — todas las operaciones verificadas dígito a dígito (exactas en f1-f4 y f6-ej1; restos controlados en f5 y f6-ej2: divisor×cociente+resto=dividendo). **Componentes nuevos reusables:** `.reparto`/`.caja-r`/`.caja-r.dibuja`/`.pt` (cajas de reparto con puntos negros; variante dashed para que el alumno dibuje), `.rep-fila`/`.etiq`/`.div-op` (fila reparto+división horizontal), `.fila-pts` (puntos sueltos en línea para rodear grupos, f2), `.sobran`/`.lbl` (puntos sobrantes = resto, f5), `.familias`/`.fam`/`.fop` (familias de 4 operaciones ×/÷, f3), `.porque`/`.p1`/`.pq` (usar × para dividir, f3), `.terminos`/`.grande`/`.et` (división etiquetada con términos), `.term-lista`/`.term-item`/`.sub` + `.prueba-lista`/`.prueba-item`/`.pr` (términos y prueba, f4), `.exactas` (chips para rodear, f5), `.divs`/`.div1` (rejilla de divisiones; variante `.div1.resto` font menor para "= ☐ y resto ☐"). Validador `--virtual-time-budget=4000`: las 6 a 1 folio A4 (satura a 92.9% = solo confirma 1-folio sí/no; densidad verificada por render visual `/tmp/pdf2png.py`; f5/f6 con algo más de aire abajo, del lado seguro Safari). Registradas en RECURSOS de materiales.html (el currículum ya listaba el sub-bloque).

- **`division-por-una-cifra` COMPLETO ✅ (6 fichas, cerrado 2026-06-21) — sexto sub-bloque, CIERRA `operaciones` de 3º. = LA CASITA** (algoritmo con la llave). Miguel avisó de que cuesta maquetar → se hizo con cabeza: f1 a mano como ANCLA + validación visual antes de seguir, y **f2-f6 a mano una a una** (NO agentes; la casita resuelta del Recuerda es distinta en cada ficha y hay que alinearla). **Nivel acordado (Miguel, AskUserQuestion): completo CON "coger dos cifras" (1ª cifra del dividendo < divisor), exactas y con resto, SIN cero en el cociente** (eso → 4º). Progresión: f1 **DU÷U exacta** (1ª cifra ≥ divisor; Recuerda casita 96÷4=24 + método divido·multiplico·resto·bajo) · f2 **DU÷U con resto** (59÷4=14 r3; "el resto siempre menor que el divisor") · f3 **CDU÷U exacta** (936÷3=312) · f4 **CDU÷U con resto** (947÷4=236 r3) · f5 **"coger dos cifras"** (128÷4=32; 1<4 → se cogen 12; las dos primeras cifras del dividendo resaltadas en gris en el Recuerda) · f6 **repaso (3 casitas mezcla) + 3 problemas** reales (componente `.problema` con zona OPERACIÓN min-height:70px para la casita). **Las 73 divisiones (f2-f6) fijadas y verificadas dígito a dígito con script Python** (`/tmp/verif_div.py`: cociente, resto, prueba c·v+r=d, sin cero en cociente, regla 1ª cifra ≥/<, resto<divisor → 0 fallos). **Maquetación de la casita (componente nuevo reusable, la parte difícil que salió limpia):** dos columnas en flex — la "llave" se forma con `border-right` de `.izq` (vertical, recorre dividendo + zona de restas) + `border-top` de `.coc`/`.cociente` (horizontal, bajo el divisor). **Casita VACÍA** (ejercicios): `.casita`/`.izq`/`.dvd` (dividendo, letter-spacing 7-8px)/`.zona` (blanco para restas, min-height 72px DU / 86-88px CDU)/`.der`/`.dvs` (divisor)/`.coc` (hueco cociente). **Casita RESUELTA** (Recuerda): `.rec-casita` + `.cres` grid de celdas fijas (`.cres.c2` = `15px 26px 26px` para 2 cifras, `.cres.c3` = `14px 24px 24px 24px` para 3 cifras), clases de celda `.sg` (signo −), `.ln` (línea de resta = border-bottom), `.gris` (cifra bajada), `.resto`/`.cog` (resto / cifras cogidas resaltadas). `.pasos`/`.nb` (pasos numerados en círculo negro) en el Recuerda. `.divs`/`.div1` reusados para el ejercicio horizontal "= ☐ y resto ☐" (`.rt`). Validador `--virtual-time-budget=4000`: las 6 a 1 folio A4, casitas alineadas verificadas por render visual `/tmp/pdf2png.py` (Quartz PDF→PNG); buen aire bajo el footer (lado seguro Safari). Registradas en RECURSOS de materiales.html.

**BLOQUE `operaciones` DE 3º COMPLETO ✅** (36 fichas: sumas-y-restas-llevando 6 + multiplicacion-por-una-cifra 6 + multiplicacion-por-dos-cifras 6 + propiedades-y-calculo-mental 6 + la-division-concepto-y-reparto 6 + division-por-una-cifra 6).

**Bloque `medida` de 3º COMPLETO ✅** (6 sub-bloques × 6 fichas = 36):
- **`longitud-km-m-cm-mm` COMPLETO ✅ (6 fichas, cerrado 2026-06-22, commit a9b1d39) — abre el bloque `medida` de 3º.** Nivel acordado con Miguel (AskUserQuestion): **solo km, m, cm, mm** (sin la escalera hm/dam/dm) y **conversiones enteras sin decimales** (decimales→4º). f1 introducción (4 unidades + equivalencias 1km=1000m / 1m=100cm / 1cm=10mm / 1m=1000mm + elegir unidad + completar equivalencias + ordenar mayor→menor + medir con regla en cm + medida lógica) · f2 convertir (km→m ×1000, m→cm ×100, cm→mm ×10, m→mm ×1000 + al revés) · f3 comparar y ordenar (signo >,<,= pasando a misma unidad + rodear la mayor + ordenar menor→mayor + V/F) · f4 sumar y restar longitudes (misma unidad) + 2 problemas · f5 6 problemas de longitud (rejilla 2×3, componente `.problema`) · f6 repaso. f1 a mano (ancla) + f2-f6 con **5 agentes en paralelo (1/ficha), números fijados y verificados por mí**. Reusa la **regla SVG de 2º** (33px=1cm, objeto rect desde x=24) y el `.problema` de operaciones 3º. Validador `--virtual-time-budget=4000`: 1 folio A4 c/u. Reusables de 2º: regla SVG (33px=1cm), balanza, vaso con nivel, reloj analógico, SVG dinero.
- **`masa-kilo-gramo` COMPLETO ✅ (6 fichas, cerrado 2026-06-23, commit 9a2896e) — segundo sub-bloque de `medida` de 3º.** Nivel acordado con Miguel (AskUserQuestion): **kg, g + medio/cuarto kilo** (1 kg=1000 g, ½ kg=500 g, ¼ kg=250 g), **conversiones enteras sin decimales** (sin tonelada ni mg → eso a 4º). f1 introducción (Recuerda kg/g + ½/¼ kg + balanza "el plato que baja pesa más" + elegir unidad + equivalencias + 3 balanzas rodear el que pesa más + masa lógica) · f2 convertir (kg→g ×1000, g→kg ÷1000, ½/¼ kg en g + 2 problemas) · f3 comparar y ordenar (signo >,<,= pasando a misma unidad + rodear la mayor + ordenar menor→mayor + V/F) · f4 sumar y restar masas (en g y en kg, misma unidad) + 2 problemas · f5 6 problemas de masa (rejilla 2×3, `.problema`) · f6 repaso (unidad + equivalencias + signo + balanzas + 2 problemas). f1 a mano (ancla) + f2-f6 con **5 agentes en paralelo (1/ficha), números fijados y verificados por mí**. **Reusa la balanza SVG de 2º** (`peso-y-capacidad`, viewBox 0 0 240 150; el plato que baja = más pesado; 2 orientaciones: izq-baja brazo `48,62→192,26` / der-baja brazo `48,26→192,62`; etiqueta del plato bajo y=66-82, del alto y=30-46) + el `.problema`. ⚠️ **LECCIÓN LLENADO 2026-06-23:** las fichas full-page sin balanzas/Recuerda grande (f2/f4/f5/f6 = solo eq-grid + 2 problemas) salieron CORTAS (~52-67% en PDF print real medido con `sips` PDF→PNG); el screenshot de pantalla con `--window-size` ENGAÑA (modo print cambia el body a max-width:15cm). Medir el llenado real = render del PDF en modo print (`--print-to-pdf` + `sips -s format png`), NO el screenshot de viewport. f6 (repaso) salió a 52% → densificada con un Ej de 3 balanzas → ~68%. ⚠️ **CORRECCIÓN 2026-06-23 (Miguel): el ~57% NO vale — las fichas a media página le parecen vacías ("llegan solo a mitad de página, mucho espacio").** El "~57% es el estándar" que creí ver en longitud quedó DESMENTIDO. **NUEVO CRITERIO de llenado para full-page 3º: ~78-85% en PDF print real, densificando con ESPACIO DE TRABAJO real (cajas `.caja-sm` grandes ≈54×36, zonas `.problema .zona` min-height ≈104px + `.problemas gap` 14px + enunciado 13.5px, más ítems reales por ejercicio), NUNCA con aire/gaps vacíos.** ✅ **masa REAJUSTADA a este criterio el 2026-06-23** (mismo set CSS que capacidad: caja-sm 54×36, zonas 104px, gap 14px, enunciado 13.5px, f2 con 6 ítems/ejercicio) → f2 83% · f3 77% · f4 83% · f5 75% · f6 88%, todas 1 folio. Reusables de 2º: regla SVG (33px=1cm), balanza, vaso con nivel, reloj analógico, SVG dinero.
- **`capacidad-litro-mililitro` COMPLETO ✅ (6 fichas, cerrado 2026-06-23) — tercer sub-bloque de `medida` de 3º.** Nivel acordado con Miguel (AskUserQuestion): **l, ml + medio/cuarto litro** (1 l=1000 ml, ½ l=500 ml, ¼ l=250 ml), **conversiones enteras sin decimales** (sin dl/cl → 4º). Simétrico a masa. f1 introducción (Recuerda l/ml + ½/¼ l + vaso "el más lleno tiene más capacidad" + elegir unidad + equivalencias + 3 vasos rodear el más lleno/tachar el menos + capacidad lógica) · f2 convertir · f3 comparar y ordenar · f4 sumar y restar (ml y l) · f5 6 problemas · f6 repaso (con 3 vasos). f1 a mano (ancla) + f2-f6 con 5 agentes/1 ficha, números fijados y verificados por mí. **Reusa el vaso SVG con nivel de 2º** (`peso-y-capacidad`: trapecio `path M12,8 L52,8 L47,86 L17,86 Z`; nivel = `polygon` desde la superficie —y MENOR = más lleno— hasta la base y=84 + `line` de superficie; ancho a una altura y: izq `12+5·(y-8)/78`, der `52−…`; niveles usados: lleno y≈14, medio y≈42, poco y≈66). **Llenado: nació corto como masa (f2 60%, f5 57%) y se densificó al NUEVO criterio** (cajas 54×36, zonas 104px, f2 con 6 ítems/ejercicio) → f1 83% · f2 83% · f3 77% · f4 83% · f5 75% · f6 85%. Reusables de 2º: regla SVG (33px=1cm), balanza, vaso con nivel, reloj analógico, SVG dinero.
- **`el-reloj-y-los-minutos` COMPLETO ✅ (6 fichas, cerrado 2026-06-24, commit a6540cf) — cuarto sub-bloque de `medida` de 3º.** Nivel "Estándar 3º" acordado con Miguel (AskUserQuestion): minutos de 5 en 5 + cuartos + «y»/«menos» + 1 h=60 min + reloj de 24 h + tiempo transcurrido sencillo + problemas (minuto a minuto fino y duraciones complejas → 4º). f1 leer minutos de 5 en 5 (la minutera, cada nº=5 min; correspondencia + leer 6 relojes + dibujar 6) · f2 los cuartos (en punto/y cuarto/y media/menos cuarto; rodear + completar + dibujar) · f3 «y»/«menos» (hasta la media «y», pasada la media la hora siguiente «menos»; palabras + unir + rodear y/menos + escribir con «menos») · f4 1 h=60 min + 24 h (conversión h↔min + 12h↔24h + mañana/tarde/noche + relojes "de la tarde"→24h) · f5 el tiempo que pasa (transcurrido sencillo + ¿qué hora será? + 4 problemas) · f6 repaso (leer + dibujar + conversión + 4 problemas). **Generadas con script Python `gen.py` + `reloj.py` (NO agentes)** por la sensibilidad de las agujas — igual criterio que la división. **Reloj SVG nuevo parametrizado para 3º** (clona el de 2º `el-reloj-horas-y-media`, viewBox 0 0 100 100, círculo r=46): `punta(frac,r)` con trig (frac en vueltas, 0=12 en punto) coloca la minutera (r=30, sw 2.5) en CUALQUIER minuto y la horaria (r=22, sw 4) avanzando proporcional `(h%12+m/60)/12`; opción `marcas=True` pinta 00/05/.../55 en gris (Recuerda de f1). Geometría verificada contra 2º (media→(50,80); 2:30→(71.3,44.3)). Todas las conversiones/horas verificadas por mí. Validador `validar.py` (Chrome `--print-to-pdf` + `--virtual-time-budget=4000` + sips PNG): ⚠️ **BUG corregido — contar páginas con regex `/Type\s*/Page(?![s])`**, no `count("/Type /Page")` (matchea `/Type /Pages` raíz → siempre marcaba 2 páginas falsas). 1 folio A4 c/u, llenado 78.5-84.3%. Registradas en RECURSOS de materiales.html (el currículum ya listaba el sub-bloque). Reusables de 2º: regla SVG (33px=1cm), balanza, vaso con nivel, reloj analógico, SVG dinero.
- **`el-dinero-euros-y-centimos` COMPLETO ✅ (6 fichas, cerrado 2026-06-24) — quinto sub-bloque de `medida` de 3º.** Nivel acordado con Miguel (AskUserQuestion): **estándar 3º CON coma** (1 €=100 cént, leer/escribir precios con coma tipo 3,75 €, descomponer € y cént, comparar) + **operaciones completas** (sumar/restar precios con céntimos —con llevada/préstamo de céntimos—, el cambio/la vuelta, precio × cantidad pequeña). El dinero es la puerta a la coma aunque los decimales "puros" sigan en 4º. f1 conocer monedas/billetes + 1€=100cént + leer/descomponer precios con coma (Recuerda) + palabras→precio (ojo a los ceros: 3,05 €) · f2 leer/escribir precios (palabras↔cifras, precio→palabras, €→céntimos, unir precio↔descomposición) · f3 comparar y ordenar (signo >,<,= entre precios + rodear mayor de tríos + ordenar menor→mayor y mayor→menor + V/F) · f4 sumar y restar precios (6 sumas + 6 restas en horizontal con caja resultado + 2 problemas) · f5 voy de compras (el cambio = pago−cuesta + precio × cantidad: 3 panes a 0,80 € + 2 problemas) · f6 repaso (palabras→precio + comparar + €→céntimos + 4 problemas). **f1 a mano (ancla) + f2-f6 con 5 agentes en paralelo (1/ficha); TODOS los precios/operaciones fijados y verificados por mí** (sumas con llevada de céntimos 70+50=120→1,20; restas con préstamo 6,20−2,70=3,50; cambios y precio×cantidad exactos). **f2-f6 son texto + cajas + `.problema`, SIN SVG** (solo la f1 lleva los SVG de dinero) → los agentes solo clonan el CSS de f1 + pegan un bloque de CSS extra que les doy + montan los enunciados. **SVG dinero reusado de 2º (`monedas-y-billetes`):** moneda céntimo (círculo r=47 + estrellas + nº + "CENT"), moneda euro (doble círculo r=47/34 + 12 estrellas + "2€"+"EURO"), billete (rect + nº esquinas + "EURO" + nº grande + 7 estrellas); mini versiones solo círculo/rect + nº. **Clases nuevas reusables** (en el CSS extra): `.caja-precio` (hueco ancho para un precio), `.escribir-linea`/`.ln` (línea para escribir con palabras), `.eq-grid` (equivalencias con cajas), `.une`/`.une-col`/`.une-chip` (unir 2 columnas), `.signo-grid`/`.signo-item`/`.caja-s` (comparar con signo), `.trio-fila` (rodear mayor de un trío), `.orden-banco`/`.orden-secuencia`/`.caja-o` (ordenar), `.vf-lista`/`.vf-item` (V/F con pills), `.calc-grid`/`.calc-item`/`.res` (calcular horizontal con caja resultado), `.cambio-item` (el cambio y precio×cantidad), `.desc-grid`/`.desc-item` (descomponer precio; OJO: los textos sueltos en flex se parten → envolverlos en `<span class="lbl">` con `white-space:nowrap;flex-shrink:0`). Validador recreado `/tmp/validar_ficha.py` (Chrome `--print-to-pdf` + `--virtual-time-budget=4000` + sips PNG + PIL mide última fila con tinta; cuenta páginas con regex `/Type\s*/Page(?![s])`): 1 folio A4 c/u, llenado **78.9-88.2%** (f1 88.2 — alto pero el % lo dispara la tinta del footer/monedas; verificado visualmente con aire real). ⚠️ f3 nació a 85.5% con el footer pegado → bajada a 83.7% recortando gaps (a >85% Chrome-medido riesgo de 2 páginas en Safari). Registradas en RECURSOS de materiales.html. Reusables de 2º: regla SVG (33px=1cm), balanza, vaso con nivel, reloj analógico, SVG dinero.
- **`superficie` COMPLETO ✅ (6 fichas, cerrado 2026-06-24) — sexto sub-bloque, CIERRA el bloque `medida` de 3º.** Nivel acordado con Miguel (AskUserQuestion): **estándar 3º** — concepto de superficie (la región de dentro de una figura) + **medir CONTANDO cuadrados-unidad** + comparar superficies por conteo + distinguir superficie de contorno de forma intuitiva. **SIN cm²/m² formales ni fórmulas** (eso → 4º), igual que aplazamos decimales/distributiva. f1 ¿qué es la superficie? + contar cuadraditos (Recuerda + 3 ejercicios: contar figuras flotantes, contar coloreados sobre cuadrícula, rodear la de más) · f2 medir (contar figuras flotantes, coloreados, cubrir por filas, rodear más/tachar menos, figura grande) · f3 comparar (contar+signo >,<,= en parejas, rodear más en trío, ordenar 1-4) · f4 superficie vs contorno (Recuerda: superficie=dentro/contorno=borde; contar, misma superficie distinta forma, rodear correcto, V/F) · f5 construir (colorear figuras de N cuadraditos, dos figuras distintas de la misma superficie, copiar/ampliar; cuadrículas vacías grandes 6-7 cols × 5 filas) · f6 repaso (contar, comparar, ordenar, construir). **MÉTODO: f1 a mano (ancla, define el CSS del componente nuevo) + f2-f6 con SCRIPT Python `gen_superficie.py`** (NO agentes) — el conteo exacto de cuadrados ES lo que se evalúa, así que generar los grids desde ASCII y verificar las áreas por código (función `area()`) es más fiable que dibujar SVG/divs a mano (mismo criterio que pictogramas/reloj/división). El script clona el `<head>`/CSS de f1 e inyecta CSS extra (V/F, opciones); las 43 figuras verificadas por código antes de cerrar. **Componente nuevo reusable: cuadrícula de cuadraditos = rejilla CSS de `<div>`** (NO SVG): `.cuad` (grid, `grid-template-columns:repeat(N,22px)`, gap 0) con celdas `.c` (cuadrado-unidad 22px, borde gris #9a9a9a), `.c.on` (coloreado: fondo #cfcfcf + borde #333 = parte de la figura), `.c.hidden` (placeholder invisible que mantiene la posición en la rejilla para figuras irregulares flotantes tipo L/cruz/escalera). Dos representaciones: (A) figura flotante = solo `.on` + `.hidden`; (B) figura sobre cuadrícula visible = `.c` (vacías visibles) + `.c.on` (coloreadas a contar). Más clases: `.figs-fila`/`.fig-item`/`.fig-label`/`.fig-resp` (figuras en fila con caja de respuesta), `.comp-par`/`.comp-fig`/`.comp-vs` (comparar reutilizada: caja de conteo bajo cada figura + caja de signo en medio), `.vf-item`/`.vf-pill` (V/F), `.opt-fila`/`.opt-pill` (rodear opción correcta), `.unidad-uno` (cuadradito inline en el Recuerda). Validador `validar_ficha.py` (Chrome `--print-to-pdf` + `--virtual-time-budget=4000` + sips PNG + PIL última fila con tinta; páginas con regex `/Type\s*/Page(?![s])`): 1 folio A4 c/u, llenado **77.6-86.8%** (f1 86.8 · f2 85.0 · f3 84.1 · f4 85.3 · f5 81.5 · f6 77.6). ⚠️ Lección viva: las cuadrículas vacías de construcción (f5) nacen a media página (59%) — densificar con cuadrículas GRANDES (espacio de trabajo real, 6-7 cols × 5-6 filas) + un ejercicio más, NUNCA con aire (criterio Miguel). Registradas en RECURSOS de materiales.html. Reusables de 2º: regla SVG (33px=1cm), balanza, vaso con nivel, reloj analógico, SVG dinero.

**Bloque `geometria` de 3º — EN MARCHA:**
- **`rectas-paralelas-secantes-perpendiculares` COMPLETO ✅ (6 fichas, cerrado 2026-06-26, commit f841233) — ABRE el bloque `geometria` de 3º.** Nivel "Estándar 3º" acordado con Miguel (AskUserQuestion): **recta/semirrecta/segmento (concepto) + paralelas, secantes y perpendiculares** (posición de dos rectas) + reconocer el **ángulo recto con la escuadra** de forma intuitiva. **SIN medir ángulos en grados** (eso → sub-bloque siguiente `los-angulos`). En 2º `lineas-rectas-curvas-poligonales` ya había acotado "paralelas/secantes/perpendiculares → 3º". f1 recta/semirrecta/segmento (Recuerda 3 tarjetas + unir dibujo↔nombre + nombrar + V/F + dibujar con regla en cajas con puntos A/B/P/M) · f2 **paralelas** ("nunca se cortan", vías del tren; ¿paralelas? SÍ/NO + geoplano "dibuja la paralela" + rodear objetos + V/F) · f3 **secantes** ("se cortan en un punto"; clasificar secante/paralela + marcar el punto de corte + geoplano + objetos) · f4 **perpendiculares** ("secantes especiales = ángulo recto, esquina del folio, cuadradito"; ¿perpendiculares? SÍ/NO + dibujar el cuadradito + geoplano + objetos) · f5 mezcla las tres (tabla resumen + clasificar 4 pares + objetos con opciones + geoplano + V/F) · f6 repaso (nombrar recta/semi/segmento + clasificar + geoplano + objetos + completar frases). **MÉTODO: f1 a mano (ancla, define todo el CSS + los SVG) + f2-f6 con SCRIPT Python `/tmp/gen_rectas.py`** (NO agentes) — geometría de precisión (paralelas exactas, perpendiculares a 90°) → script más fiable que agentes, mismo criterio que reloj/superficie/división. El script clona el `<head>`/CSS de f1 e inyecta CSS extra. **Componentes nuevos reusables:** (1) **marker de flecha SVG global** `<marker id="fl">` en un `<svg width=0>` al inicio del body, referenciado por todos los SVG con `marker-start/end="url(#fl)"`; (2) **recta/semirrecta/segmento** (viewBox 0 0 150 42, y=21: recta=línea con flecha en las dos puntas; semirrecta=`<circle>` + línea con 1 flecha; segmento=línea + 2 circles); (3) **par de rectas** `par(tipo, ad, recto)` (viewBox 0 0 120 96, función `clip(cx,cy,ad)` intersección línea-rectángulo [8,112]×[8,88] → rectas que llegan al borde; `par`=2 paralelas desplazadas perp `sep=17`; `sec`=dos líneas por el centro a `ad` y `ad+52`; `perp`=`ad` y `ad+90` + cuadradito del ángulo recto `M p0 L p1 L p2` con `L=11`); (4) **geoplano** `geoplano(cols,rows,rectas,paso=22)` (cuadrícula de puntos `<circle r=2 #777>` + recta dada gruesa con flechas → el alumno traza la paralela/perpendicular/secante contando cuadritos); (5) **objetos mundo real** `obj(nombre)` SVG B&N (via=vías paralelas, escalera=paralelas, tijera/aspa=secantes, ventana/cruz=perpendiculares). Clases CSS: `.rsvg`, `.par-svg`, `.rec-cards`/`.rec-card`, `.une`/`.une-col`/`.une-it`/`.chip`, `.nombrar`/`.nom-it`/`.ln`, `.vf-lista`/`.vf-item`/`.vf-pill`, `.dibujar`/`.dib-item`/`.dib-caja`/`.pt-d`/`.pl`, `.clasif`/`.clasif-it`, `.par-fila`/`.par-it`, `.geo-fila`/`.geo-it`/`.geo-svg`, `.sino`/`.op`, `.resumen`/`.col`, `.obj-fila`/`.obj-it`/`.objsvg`. ⚠️ **Validación:** el `/tmp/validar_ficha.py` recreado mide la última fila con tinta sobre la altura del PNG → **satura ~91-96% cuando el footer está abajo** (f1 92.6, f2 91.4, f3 93.5, f4 96.2 — todas 1 folio con AIRE visual real). El número alto NO es malo si el render visual muestra aire bajo el footer; lo que mata es 2-páginas en el validador. f5 nació a 2 páginas (Ej1 con 6 pares en 2 filas) → recortado a 4 pares = 1 folio. f6 nació corta (69.5%) → densificada a 84.2% con 3er geoplano + ejercicio de objetos (NUNCA con aire, criterio Miguel). Verificación final por **render visual de las 6** (`/tmp/pdf2png.py`). Registradas en RECURSOS de materiales.html (key `matematicas|3|GEOMETRIA|Rectas: paralelas, secantes y perpendiculares`). Reusables de 2º: regla SVG (33px=1cm), balanza, vaso con nivel, reloj analógico, SVG dinero.
- **`los-angulos` COMPLETO ✅ (6 fichas, cerrado 2026-06-26, commit 16ab618) — segundo sub-bloque de `geometria` de 3º.** Nivel "Estándar 3º" acordado con Miguel (AskUserQuestion): **concepto de ángulo (vértice + lados) + clasificar RECTO / AGUDO / OBTUSO / LLANO** comparando "a ojo" con el ángulo recto de la escuadra. **SIN transportador ni medir en grados** (eso → 4º, igual que aplazamos decimales/cm²/distributiva). f1 ¿qué es un ángulo? (Recuerda: ángulo etiquetado vértice/lados/abertura + ángulo recto con cuadradito; marcar el vértice + ¿es recto? SÍ/NO + contar ángulos de figuras + dibujar) · f2 **agudo** ("más cerrado que el recto"; ¿agudo? SÍ/NO + rodear agudos + ordenar del más cerrado al más abierto + dibujar) · f3 **obtuso** ("más abierto que el recto"; ¿obtuso? SÍ/NO + rodear obtusos + clasificar agudo/recto/obtuso + dibujar) · f4 **clasificar** (Recuerda tabla 4 tipos incl. **llano** = línea recta/media vuelta; nombrar 8 ángulos + V/F + dibujar) · f5 **mundo real** (las **agujas del reloj** en punto forman ángulos: 1=agudo, 3=recto, 5=obtuso; **porciones de tarta** = sectores; V/F + dibujar) · f6 repaso (nombrar 8 + rodear el recto + relojes 2/3/4 + completar frases). **MÉTODO: las 6 con SCRIPT Python `/tmp/gen_angulos.py`** (NO agentes) — geometría por trig (igual criterio que el reloj). Clona el `<head>`/CSS de la f1 de rectas + inyecta CSS de ángulos. **Componentes nuevos reusables:** (1) **ángulo** `angulo(abertura, base=0, marca='arco'|'recto'|'none', r=40)` — viewBox 0 0 110 104, vértice (55,56), `pt(ang,r)` con `-sin` (ángulo positivo abre hacia arriba); marca `arco`=polyline de 18 segmentos, `recto`=cuadradito `M q1 L c L q2`; variante CSS `.ang-svg.mini` (62×58) para los Recuerda comparativos; (2) **reloj** `reloj(h)` — círculo r=40 + 12 puntos + minutera al 12 + horaria a `h·30°`; las agujas en punto dan ángulos exactos (1→30° agudo, 3→90° recto, 5→150° obtuso); (3) **sector/porción de tarta** `sector(abertura, base)` — polígono con vértice en el centro + borde curvo por polyline (relleno gris). Clases CSS: `.ang-svg`/`.ang-svg.mini`, `.reloj-svg`, `.sector-svg`, `.ang-fila`/`.ang-it`/`.et`/`.ln`, `.sino`/`.op`, `.resumen`/`.col` (tabla 4 tipos), + reusadas de rectas (`.recuerda`, `.vf-lista`, `.dibujar`/`.dib-caja`/`.pt-d`). ⚠️ **Llenado:** los ángulos SVG nacieron grandes (104×98) → f2/f3 a 2 páginas + f1 al 98%. Fix: `.ang-svg` a **90×86**, `.dib-caja` a 80, ángulos `.mini` en los Recuerda comparativos, recortar el 5º ángulo de f2/f3 Ej2 → todas 1 folio (f1 92.6, f2 85.6, f3 85.9, f4 87.9, f5 79.5, f6 85.3; f6 densificada con 2ª fila de ángulos). ⚠️ Fix `VÉRTICE` se cortaba por la izquierda del viewBox (text-anchor="end" en x negativo) → `text-anchor` por defecto en x=2. Registradas en RECURSOS de materiales.html (key `matematicas|3|GEOMETRIA|Los ángulos`). **Siguiente sub-bloque: `poligonos-y-triangulos`** (nivel a acordar con Miguel al arrancar). Reusables de 2º: regla SVG (33px=1cm), balanza, vaso con nivel, reloj analógico, SVG dinero.

---

## Contenido publicado

### Fichas imprimibles (`/recursos/`)
- **1º Primaria Lengua** — 5 bloques, ~131 fichas ✅
- **2º Primaria Lengua** — 12 bloques, ~111 fichas ✅
- **3º Primaria Lengua** — 12 bloques, ~73 fichas ✅
- **4º Primaria Lengua** — 14 bloques, ~102 fichas ✅
- **5º Primaria Lengua — COMPLETO ✅** (cerrado 2026-05-23):
  - Área Lectura — 7 bloques × 10 fichas = 70 fichas (cerrada 2026-05-22)
  - Bloque D Gramática — 8 sub-bloques × 10 fichas = 80 fichas: analisis-morfologico, verbos-irregulares, oracion-simple, campos-semanticos, connotacion-y-denotacion, acentuacion-completa, tildes-diacriticas, puntuacion-avanzada
- **6º Primaria Lengua — COMPLETO ✅** (cerrado 2026-05-24, 150 fichas):
  - Área Lectura 7/7 ✅ (cerrada 2026-05-24):
    - `tipologias-textuales` (10 fichas)
    - `textos-literarios-narrativa` (10 fichas)
    - `textos-literarios-poesia` (10 fichas)
    - `textos-literarios-teatro` (10 fichas)
    - `textos-discontinuos` (10 fichas)
    - `intencion-autor-subtexto` (10 fichas, márgenes 3cm)
    - `resumen-y-esquema-avanzado` (10 fichas, márgenes 3cm)
  - Bloque D Gramática 8/8 ✅ (cerrado 2026-05-24, todo con márgenes 3cm):
    - `analisis-sintactico-sn-sv` (10 fichas)
    - `oracion-compuesta-coordinadas` (10 fichas)
    - `oracion-compuesta-subordinadas` (10 fichas)
    - `verbo-avanzado` (10 fichas)
    - `lexico-cultismos-prefijos` (10 fichas)
    - `polisemia-homonimia-paronimia` (10 fichas)
    - `ortografia-avanzada` (10 fichas)
    - `puntuacion-nivel-eso` (10 fichas)
- **1º Primaria Matemáticas — COMPLETO ✅** (cerrado 2026-05-28, 71 fichas):
  - `numeros` (12): numeros-hasta-99 (6) + decenas-unidades (2) + numeros-ordinales (2) + comparar-y-ordenar (2)
  - `operaciones` (20): sumas-sin-llevadas (8) + restas-sin-llevadas (8) + sumas-y-restas-mezcladas (4)
  - `medida` (15): longitud-peso-capacidad (3) + monedas-billetes (3) + el-reloj-en-punto (3) + dias-semana (3) + meses-del-ano (3)
  - `geometria` (9): figuras-planas (3) + cuerpos-geometricos (3) + lineas-y-situacion-espacial (3)
  - `estadistica` (6): tablas-simples (3) + pictogramas (3)
  - `problemas` (9): problemas-suma-sencillos (3) + problemas-resta-sencillos (3) + problemas-mixtos-basicos (3)
- **2º Primaria Matemáticas — COMPLETO ✅** (cerrado 2026-06-14, 131 fichas):
  - `numeros` (21) + `operaciones` (33) + `medida` (19) + `geometria` (16) + `estadistica` (12) + `problemas` (30) — detalle en sección "Estructura matemáticas Primaria"
- **3º Primaria Matemáticas — EN MARCHA** (arrancado 2026-06-15, fuente Poppins):
  - **Bloque `numeros` COMPLETO ✅ (36 fichas)**: `numeros-hasta-10000` (6) ✅ + `valor-posicional-y-descomposicion` (6) ✅ + `comparar-y-ordenar` (6) ✅ + `numeros-romanos` (6) ✅ + `las-fracciones` (6) ✅ + `sumar-y-restar-fracciones` (6) ✅
  - **Bloque `operaciones` COMPLETO ✅ (36 fichas)**: `sumas-y-restas-llevando` (6) ✅ (commit 9dcdd59) + `multiplicacion-por-una-cifra` (6) ✅ (commit 08f2ba7) + `multiplicacion-por-dos-cifras` (6) ✅ (commit 1c40c24) + `propiedades-y-calculo-mental` (6) ✅ (commit 412ee86 — conmutativa, asociativa, neutro/×0/×10/×100, cálculo mental; distributiva→4º) + `la-division-concepto-y-reparto` (6) ✅ (commit c2b6f46 — CONCEPTO de división sin casita, todo horizontal; hecha a mano una a una) + `division-por-una-cifra` (6) ✅ (cerrado 2026-06-21 — LA CASITA: DU/CDU exacta y con resto + "coger dos cifras", sin cero en cociente; f1 ancla a mano + f2-f6 a mano una a una, 73 divisiones verificadas con script)
  - **Bloque `medida` COMPLETO ✅ (36 fichas, cerrado 2026-06-24)**: `longitud-km-m-cm-mm` (6) ✅ (commit a9b1d39, cerrado 2026-06-22 — solo km/m/cm/mm, conversiones enteras sin decimales; f1 a mano + f2-f6 con 5 agentes/1 ficha; reusa regla SVG de 2º + `.problema`) + `masa-kilo-gramo` (6) ✅ (commit 9a2896e, cerrado 2026-06-23 — kg/g + ½ kg=500g/¼ kg=250g; reusa balanza SVG de 2º; llenado reajustado al nuevo criterio 75-88%) + `capacidad-litro-mililitro` (6) ✅ (cerrado 2026-06-23 — l/ml + ½ l=500ml/¼ l=250ml, conversiones enteras; f1 a mano + f2-f6 con 5 agentes/1 ficha; reusa vaso SVG con nivel de 2º + `.problema`; densificada al nuevo criterio de llenado 75-85%) + `el-reloj-y-los-minutos` (6) ✅ (commit a6540cf, cerrado 2026-06-24 — estándar 3º: minutos de 5 en 5 + cuartos + «y»/«menos» + 1h=60min + 24h + tiempo transcurrido; reloj SVG nuevo con agujas por trig, minutera en cualquier minuto; generadas con script Python, NO agentes; 78-84%) + `el-dinero-euros-y-centimos` (6) ✅ (cerrado 2026-06-24 — estándar 3º CON coma: 1€=100cént, leer/escribir/descomponer precios con coma 3,75 €, comparar, sumar/restar precios con llevada/préstamo de céntimos, el cambio, precio×cantidad; f1 a mano + f2-f6 con 5 agentes/1 ficha, precios verificados por mí; reusa SVG dinero de 2º; 78-88%) + `superficie` (6) ✅ (cerrado 2026-06-24 — estándar 3º: concepto + medir contando cuadrados-unidad + comparar + superficie vs contorno; SIN cm²/m² ni fórmulas →4º; componente nuevo = cuadrícula de divs CSS `.cuad`/`.c`/`.on`/`.hidden`; f1 a mano + f2-f6 con script Python `gen_superficie.py`, áreas verificadas por código; 77-87%) — **bloque medida CERRADO**
  - **Bloque `geometria` EN MARCHA** (arrancado 2026-06-26): `rectas-paralelas-secantes-perpendiculares` (6) ✅ (commit f841233 — recta/semirrecta/segmento + paralelas/secantes/perpendiculares, ángulo recto intuitivo; SIN grados →`los-angulos`; f1 a mano + f2-f6 con script Python `gen_rectas.py`, componentes nuevos: marker flecha SVG, par de rectas con clip línea-rectángulo, geoplano de puntos) + `los-angulos` (6) ✅ (commit 16ab618 — concepto vértice/lados + clasificar recto/agudo/obtuso/llano comparando con el recto; SIN transportador ni grados →4º; las 6 con script Python `gen_angulos.py` por trig; componentes nuevos: ángulo SVG con arco/cuadradito, reloj con agujas, sector de tarta). **Siguiente: `poligonos-y-triangulos`** · luego circunferencia-y-circulo · el-perimetro
- **1º ESO Matemáticas** — solo álgebra (4 páginas)
- **Total:** ~975 fichas indexadas en sitemap

### Blog (`/blog.html`)
- **Índice rediseñado el 2026-06-15** (commits a31b003 + 362804d): fuera las portadas de emoji → diseño editorial con **fotos reales** (Pexels, uso comercial, self-hosted en `blog-img/` para no depender del CDN ni añadir cookies), **artículo destacado a doble ancho** con imagen de fondo y **color por categoría** (var `--cat` + `--img` por tarjeta). El **destacado es `como-elegir-academia-torremolinos`** (color **jade `#4fc3a1`** — el coral daba sensación de alerta), no Mates. Portadas `aspect-ratio:16/9` (las fotos verticales se recortan en el hero ancho → para el destacado mejor horizontal). Degradado verde sutil sobre cada foto. La de Lectura: niño de espaldas, NO identificable (norma de Miguel: fotos de niños sin cara identificable). El artículo `elegir-academia` se reescribió en clave de metodología propia y tono NO competitivo (ver memoria `project-posicionamiento-academia`).
- 6 artículos publicados, casi todos con enlaces internos a fichas:
  - `como-elegir-academia-torremolinos.html` (DESTACADO del blog; reescrito 2026-06-15: 7 claves en tono positivo "buena señal" + sección "Cómo trabajamos en Esparta"; enlaza a psicología, materiales y otros artículos)
  - `como-ayudar-comprension-lectora-primaria.html` (11 enlaces a fichas)
  - `tecnicas-de-estudio-primaria.html` (5 enlaces a fichas)
  - `como-trabajar-ortografia-primaria.html` (9 enlaces a fichas)
  - `como-ayudar-matematicas-primaria.html` (2026-06-04, commit 9ca66b7, 18 enlaces a fichas de mates 1º-2º — primer artículo de mates; 3 pilares número/cálculo/problemas; enlaza a psicología por discalculia)
  - `como-preparar-la-ebau-andalucia.html` (2026-06-15 — guía estratégica de Bachillerato: nota 60/40, dos fases Acceso/Admisión, ponderaciones, plan de preparación; enlaza a psicología por gestión de nervios; CTA a inscripción. Sin enlaces a fichas: no hay material de ese nivel. Datos estables; el detalle de asignaturas/fechas se consulta cada año en el Distrito Único Andaluz)

### Páginas de servicio
- Logopedia · Psicología · Quiénes somos — en sistema premium, con JSON-LD

---

## Roadmap

### Prioridad alta — orden acordado con Miguel (2026-05-24)

1. **1º Primaria Matemáticas COMPLETO ✅** (cerrado 2026-05-28, **71 fichas**) — estructura acordada con Miguel el 2026-05-24 (detalle completo en sección "Estructura matemáticas Primaria"). 6 bloques (5 LOMLOE + problemas), sub-bloques anidados. Cifra final aplicando la norma "ajustar fichas al material real" (en 1º muchos conceptos no dan para 6 fichas distintas).
   - **Bloque `numeros` COMPLETO ✅** (12 fichas, cerrado 2026-05-28): `numeros-hasta-99` (6) + `decenas-unidades` (2) + `numeros-ordinales` (2) + `comparar-y-ordenar` (2). Patrón en sub-bloques de 2 fichas: ficha-1 con "Recuerda" + ejemplos, ficha-2 solo ejercicios + variación.
   - **Bloque `operaciones` EN MARCHA — `sumas-sin-llevadas` COMPLETO ✅** (8 fichas, cerrado 2026-05-28): ficha-1 con Recuerda (3 ejemplos: una cifra vertical, dos cifras vertical, una cifra horizontal) + sumas básicas + serie 1-10. ficha-2 unir suma↔resultado + serie 11-20. ficha-3 sumas con dibujos (●★▲■) + serie 20-30. ficha-4 descomponer + serie 10-100 de 10 en 10. ficha-5 el doble + serie 40-50. ficha-6 tres sumandos + serie 50-60. ficha-7 y ficha-8 página entera con 20 sumas DU+DU en rejilla 5×4 (fuente 22px, gap 38px) — estilo cuadernillo Rubio.
   - **`restas-sin-llevadas` COMPLETO ✅** (8 fichas, cerrado 2026-05-28): clonadas del patrón de `sumas-sin-llevadas` («cógelo como imagen y lo imitas con restas todo de un tirón»). ficha-1 introducción + Recuerda (7−3, 47−23 D U, 8−5 horizontal). ficha-2 unir resta↔resultado. ficha-3 con dibujos (segundo grupo = se quitan). ficha-4 **completar restas** `7−☐=5` (en lugar de «descomponer al revés»: más natural para 1º). ficha-5 **la mitad** (en lugar de el doble): 2→1, 4→2, 6→3, 8→4, 20→10, 40→20. ficha-6 **restas encadenadas en horizontal** `9−2−1=☐` (no en columna: confunde a 1º). ficha-7 y ficha-8 página entera 20 restas DU−DU (con minuendo≥sustraendo dígito a dígito en cada columna).
   - **`sumas-y-restas-mezcladas` COMPLETO ✅** (4 fichas, cerrado 2026-05-28): sustituye al previsto `calculo-mental` por ser más productivo en 1º. ficha-1 introducción + Recuerda (3 mini-ejemplos: suma vertical, resta vertical, mezcladas horizontal) + ejercicios discriminación de signo (6 columna 1 cifra, 8 horizontal 1 cifra, 4 columna 2 cifras, todo alternando + y −). ficha-2/3/4 página entera con 20 operaciones DU±DU mezcladas en rejilla 5×4 (10 sumas + 10 restas, todo sin llevadas / sin prestar verificado), mismo font/gap que ficha-7/8 de los dos sub-bloques previos.
   - **Bloque `operaciones` COMPLETO ✅** (20 fichas).
   - **Bloque `medida` COMPLETO ✅** (17 fichas, cerrado 2026-05-28). 5 sub-bloques:
     - **`longitud-peso-capacidad`** (3 fichas): ficha-1 explicación con Recuerda (3 conceptos: longitud, peso, capacidad) + 4 ejercicios (rodear más largo con líneas ▬, más pesado con palabras ELEFANTE/HORMIGA…, más capacidad BAÑERA/VASO…, ordenar 3 tamaños). ficha-2 conceptos opuestos (más corto, más ligero, menos capacidad, ordenar por altura). ficha-3 repaso mixto (unir objeto↔adjetivo, completar frases con ligera/pesada / larga/corta / más/menos, ordenar líneas por longitud y objetos por capacidad).
     - **`monedas-billetes`** (3 fichas): **primer sub-bloque con dibujos SVG inline** — decisión de Miguel: en este tema concreto sí entran dibujos porque el niño debe reconocer el objeto real (no leer "1€" al lado de "1€"). 3 plantillas SVG propias B&N: moneda céntimo (círculo + 10 estrellas UE + número grande + "CENT"), moneda euro (círculo + anillo bicolor + 12 estrellas + número + "EURO"), billete (rectángulo redondeado + número en esquinas + "EURO" centrado + 7 estrellas abajo). ficha-1 explicativa con Recuerda + 4 ejercicios. ficha-2 ejercicios variados. ficha-3 ¿me llega? SÍ/NO + dibujar libre las monedas necesarias. Uniones SIN líneas guía (el alumno traza la flecha libre).
     - **`el-reloj-en-punto`** (3 fichas): segundo sub-bloque con SVG inline. Plantilla reloj analógico B&N: círculo r=46 + 12 números + aguja larga al 12 (en punto) + aguja corta con coordenadas precalculadas por hora. Caja digital con Courier New (look LCD). ficha-1 Recuerda + 4 ejercicios. ficha-2 con comparar "más tarde". ficha-3 repaso con actividades cotidianas en formato 24h (Comida 14:00, Cena 21:00 — decisión Miguel por realismo cultural).
     - **`dias-semana`** (3 fichas): sin SVG, todo texto. ficha-1 Recuerda (tira 7 días, sábado/domingo en gris claro) + 5 ejercicios (numerar 1-7, completar huecos, rodear fin de semana, frases, tabla ayer/hoy/mañana). ficha-2 sin Recuerda (unir día↔posición ordinal, mini calendario 4×7 con preguntas, continuar serie cruzando semana, problemas mañana/ayer/dentro de N días). ficha-3 repaso (tachar intruso, calendario+rodear miércoles, ordenar los 7 días desde banco, preguntas con suma 7+7).
     - **`meses-del-ano`** (3 fichas, carpeta sin ñ por compatibilidad de URLs): sin SVG. Estructura mimética a `dias-semana` adaptada a 12 elementos. ficha-1 Recuerda con grid 6×2 de los 12 meses + 4 ejercicios (numerar 1-12, completar huecos, rodear meses de verano, frases). ficha-2 sin Recuerda (unir mes↔posición ordinal, continuar serie, asociar celebración↔mes Navidad/Halloween/Vuelta al cole/Reyes, preguntas). ficha-3 repaso (intruso con lunes/otoño/tarde/año, tabla mes anterior/este/siguiente, ordenar los 12 desde banco, preguntas).
   - **Aprendizaje 2026-05-28:** Miguel rechazó un ejercicio `12+12=___ meses (dos años)` en `meses-del-ano/ficha-2` por forzado. Norma: en preguntas finales evitar agregaciones artificiales (sumar dos unidades de tiempo para forzar una operación); preferir preguntas con sentido real ("¿en qué mes empiezan las vacaciones?").
   - **Bloque `geometria` COMPLETO ✅** (9 fichas, cerrado 2026-05-28). Tres sub-bloques:
     - **`figuras-planas`** (3): 4 figuras canónicas (triángulo/cuadrado/rectángulo/círculo) con SVG simple. ficha-1 Recuerda + 4 ejercicios. ficha-2 contar mosaico, asociar figura↔objeto, series, intruso. ficha-3 casita SVG + dibujar + V/F + nombrar. **Norma:** uniones figura↔texto sin caja contenedora; píldoras solo en el texto. Dejar ~100-150px de aire bajo el footer (Safari mete sus márgenes y se va a 2 páginas).
     - **`cuerpos-geometricos`** (3, con SVG 3D): 4 cuerpos (cubo/esfera/cilindro/cono). Plantillas SVG isométricas B&N: cubo (3 polígonos), esfera (círculo+elipse meridiana), cilindro (elipse+líneas+arcos), cono (líneas+arcos con base dashed). ficha-1 Recuerda + unir nombre + unir nº caras planas (6/0/2/1) + rodear. ficha-2 contar mosaico, asociar cuerpo↔objeto cotidiano (dado/lata/gorro/pelota), rodear los que ruedan (esfera/cilindro/cono), asociar cuerpo↔figura plana (cubo↔cuadrado / cilindro↔rectángulo / cono↔triángulo / esfera↔círculo). ficha-3 muñeco compuesto + nombrar + V/F + dibujar libre.
     - **`lineas-y-situacion-espacial`** (3): líneas (recta/curva/abierta/cerrada) + posición (dentro/fuera, encima/debajo, izq/medio/dcha). ficha-1 Recuerda + 4 ejercicios sobre líneas. ficha-2 mini-escenas con caja/pelota, pecera/pez, mesa/casa/árbol + escena grande con V/F. ficha-3 nombrar líneas + escena habitación (cama+gato+zapato+mesilla+lámpara+alfombra+pelota) con completar 6 frases + dibujar 4 + V/F mixto.
   - **Bloque `estadistica` COMPLETO ✅** (6 fichas, cerrado 2026-05-28). Dos sub-bloques:
     - **`tablas-simples`** (3): ficha-1 figuras + Recuerda + contar→tabla. ficha-2 frutas + TOTAL + ordenar MENOS→MÁS. ficha-3 estuche + V/F + ordenar MÁS→MENOS (4 puestos). Tablas HTML reales (`border-collapse`, `th` gris).
     - **`pictogramas`** (3): ficha-1 frutas + Recuerda + leyenda "cada 🍎=1" + leer/responder/dibujar. ficha-2 mascotas (perro/gato/pez SVG nuevos) + TOTAL + ordenar MENOS→MÁS (3 puestos). ficha-3 transportes (coche/bici/avión/barco SVG nuevos, **4 categorías** vs 3) + V/F + ordenar MÁS→MENOS (4 puestos).
   - **Bloque `problemas` COMPLETO ✅** (9 fichas, cerrado 2026-05-28). Tres sub-bloques × 3 fichas. Patrón: **ficha-1** Recuerda + 5 problemas con dibujo · **ficha-2** 5 problemas (3 con dibujo + 2 sin) · **ficha-3** 6 problemas solo texto. Componente `.problema` reusable con caja border + grid `40px 1fr` cuando lleva icono. Caja "OPERACIÓN" (dashed) + caja "SOLUCIÓN" con línea para frase. **Mixtos añade caja `.signo-elegir`** (label SIGNO + "+ o −") antes de OPERACIÓN.
     - **`problemas-suma-sencillos`** (3): caramelos, niños, coches, pegatinas, galletas (f1) · lápices, pelotas, libros, flores, peces (f2) · cromos, plátanos, bus, monedas, ovejas, cuentos (f3 — 6 problemas).
     - **`problemas-resta-sencillos`** (3): Recuerda con palabras pista (quita/da/vuelan/comen/gasta) + manzanas/pájaros/caramelos/globos/monedas (f1) · peces/galletas/cromos/coches/niños (f2) · pegatinas/hojas/clase/céntimos/gallinas/donuts (f3).
     - **`problemas-mixtos-basicos`** (3): Recuerda con **tabla 2 cols de palabras pista** (`+ regalan/llegan/compran/más/en total/ponen` · `− quedan/se van/comen/dan/pierden/vuelan/gastan`) + alternancia suma/resta + casilla SIGNO obligatoria en los 3 fichas.
   - **NORMA CRÍTICA validada 2026-05-28 (problemas 1º):** todas las sumas SIN llevadas y todas las restas SIN prestar. Miguel detectó 25 operaciones con llevadas/prestar en la 1ª pasada — hubo que rehacerlas. Validar dígito a dígito antes de cerrar cada ficha.
   - **Índice web:** `materiales.html` ya alineado para 1º Mates con la estructura de 6 bloques (commit `ec68965`, 2026-05-28). 2º–6º Mates en `materiales.html` siguen con la estructura antigua de 5 bloques — actualizar al arrancar cada curso.
   - **Hero compacto en `materiales.html`** (2026-05-28): el hero ocupaba toda la pantalla y los padres tenían que hacer scroll para ver las tarjetas Lengua/Mates. Reducido (`padding 7.5rem→2rem`, h1 más pequeño, quitados `<p>` descriptivo y 4 `<span class="hero-tag">`, app-wrap padding-top 2.5rem→1.5rem). Las tarjetas aparecen ahora en el viewport inicial sin scroll.
   - **1º MATES COMPLETO ✅** (2026-05-28, 71 fichas). **2º MATES COMPLETO ✅** (2026-06-14, 131 fichas). **3º MATES EN MARCHA** (arrancado 2026-06-15): árbol acordado + **bloque `numeros` COMPLETO ✅ (36 fichas)** + **bloque `operaciones` COMPLETO ✅ (36 fichas)**: `sumas-y-restas-llevando` ✅ (6, 9dcdd59) + `multiplicacion-por-una-cifra` ✅ (6, 08f2ba7) + `multiplicacion-por-dos-cifras` ✅ (6, 1c40c24) + `propiedades-y-calculo-mental` ✅ (6, 412ee86) + `la-division-concepto-y-reparto` ✅ (6, c2b6f46) + `division-por-una-cifra` ✅ (6, cerrado 2026-06-21 — la casita). **Bloque `medida` COMPLETO ✅ (36 fichas, cerrado 2026-06-24):** `longitud-km-m-cm-mm` ✅ (6, a9b1d39) + `masa-kilo-gramo` ✅ (6, 9a2896e) + `capacidad-litro-mililitro` ✅ (6) + `el-reloj-y-los-minutos` ✅ (6, a6540cf) + `el-dinero-euros-y-centimos` ✅ (6) + `superficie` ✅ (6, cerrado 2026-06-24 — concepto + contar cuadrados-unidad + comparar + superficie vs contorno; sin cm²/m² ni fórmulas →4º). **Bloque `geometria` EN MARCHA** (arrancado 2026-06-26): `rectas-paralelas-secantes-perpendiculares` ✅ (6, commit f841233) + `los-angulos` ✅ (6, commit 16ab618 — concepto + clasificar recto/agudo/obtuso/llano; SIN grados →4º; script Python `gen_angulos.py` por trig). **Siguiente sub-bloque: `poligonos-y-triangulos`** (ver sección "Sub-bloques 3º Primaria"). 3º usa **Poppins**.

2. **Más artículos de blog SEO** — "Cómo preparar la EBAU en Andalucía", "Qué hacer si tu hijo no aprueba matemáticas", "El paso de Primaria a la ESO". Ideas ya listadas. Después de prioridad 1.

### Prioridad media — más adelante

3. **ESO completa** — 1º ESO tiene solo álgebra. Cubrir resto de matemáticas 1º ESO, luego 2º, 3º, 4º. La estructura `recursos/1-eso/`, `recursos/2-eso/`... ya sigue el mismo patrón.

4. **Migrar `materiales.html` al sistema premium** — sigue con la paleta legacy verde claro. No es urgente pero rompe coherencia visual.

### Prioridad baja — cuando recursos y materiales estén completos

5. **Juegos interactivos** — EN MARCHA (Miguel lo adelantó al roadmap el 2026-06-17). Decisión: **portal de juegos de contenido propio** en `juegos.html` (hoy "Próximamente"), **solo Camino Matemático + Camino Inglés** (resto de `_pendiente/` descartado para esto). **Piloto del Camino Matemático HECHO en `juegos/camino-matematico/`** — motor genérico + contenido por cursos (`CURRICULUM`, añadir reto = 1 línea), home 2 pasos, imágenes optimizadas 32MB→1.6MB, dinamismo (guerrero avanza + animaciones + sonido Web Audio sin peso + racha + estrellas), aritmética validada. **EN LOCAL, SIN SUBIR** (sin commit, sin enlazar). Detalle completo y siguientes pasos (clonar al Inglés, montar el portal) en memoria `project-juegos-interactivos`.

6. **Bachillerato** — crear `recursos/1-bachillerato/` y `recursos/2-bachillerato/` con fichas de las asignaturas principales.

### Lo que NO haría aún

| Idea | Por qué no |
|---|---|
| Build step / framework JS | Sin beneficio real para contenido estático. Rompe la simplicidad del deploy. |
| CMS / panel de admin | El flujo actual (editar HTML + push) es más rápido y sin dependencias. |
| Backend propio en esta web | La inscripción ya va al dashboard Shadow. No hay necesidad. |
| Materiales privados de alumnos en este repo | Se eliminaron. Si se retoma, crear estructura nueva ESO/Bach cuando llegue el momento. |

---

## Seguridad en commits — OBLIGATORIO

Antes de cualquier `git commit`:

1. Ejecutar `git status` y mostrar qué archivos van a entrar.
2. **Solo commitear lo que se haya trabajado en la sesión actual.** Nunca `git add -A` ni `git add .` — siempre `git add <rutas-específicas>`. Si aparece un archivo "modified" que no se ha tocado en la conversación (CI, hooks, autoformat, IDE…), **parar y preguntar a Miguel** — no entra en el commit.
3. Escanear en busca de: datos personales de alumnos, teléfonos, emails privados, URLs con credenciales.
4. Nunca commitear material privado de alumnos con nombres reales sin `noindex,nofollow`.
5. Solo hacer el commit tras confirmación explícita del usuario.
6. Tras el commit, ejecutar `git show --stat HEAD` para verificar que el contenido es exactamente el esperado (sobre todo si hubo `pull --rebase` previo).

---

## Proyectos hermanos (ecosistema Esparta)

| Carpeta | Qué es | URL |
|---|---|---|
| `~/Desktop/dashboard-shadow-academia-esparta/` | Dashboard interno — Supabase + React | shadow.academiaesparta.es |
| `~/Desktop/consulta-asistida-ia/mavego-app/` | App clínica Mavego (proyecto externo) | mavego-dev.academiaesparta.es |
| `~/Desktop/Activos/supabase-shadow-setup/` | SQL fundacional del dashboard | — |
| `~/Desktop/Activos/n8n-organization/` | Workflows n8n del ecosistema | — |

---

## Cuando vuelvas a este proyecto

1. Abre esta carpeta (`~/Desktop/academia-esparta-web/`).
2. Lee este `CLAUDE.md` — tienes la estructura completa, el estado y el roadmap.
3. Lee `DISENO.md` si vas a tocar páginas web (sistema premium, trampas CSS).
4. El siguiente paso siempre está en **Roadmap › Prioridad alta**.
5. Para añadir fichas: sigue la ruta `recursos/primaria/CURSO/lengua/BLOQUE/` y el template del 26 abr 2026.
6. Push a `main` → publicado. El sitemap se regenera solo.
7. Los interactivos están en `_pendiente/` — no tocar hasta que Primaria + ESO estén completos.
8. La memoria de Claude (`~/.claude/projects/...`) se carga automáticamente al abrir esta carpeta.

**Frase trigger:** _"Seguimos con las fichas"_, _"Vamos con [bloque] de [Nº Primaria]"_, _"Seguimos con mates"_ o _"Vamos con [bloque] de mates de [Nº Primaria]"_ → ir directo al roadmap, sin preguntar.
