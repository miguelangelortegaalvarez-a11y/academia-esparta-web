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
├── blog.html                               # Hub blog SEO — "Guías para padres"
├── inscripcion.html                        # Redirige → shadow.academiaesparta.es/inscripcion
├── juegos.html                             # "Próximamente" — interactivos aparcados
├── 404.html                                # Página de error (sistema premium)
├── como-elegir-academia-torremolinos.html  # Artículo SEO nº1
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
│   │   ├── [1-6]/matematicas/  # Estructura acordada 2026-05-24 — ver sección "Estructura matemáticas Primaria"
│   │   │                       # 6 bloques: numeros, operaciones, medida, geometria, estadistica, problemas
│   │   │                       # Sub-bloques anidados · 6 fichas/serie · empieza por 1º (120 fichas previstas)
│   └── 1-eso/
│       └── matematicas/algebra/  # 4 páginas (apuntes, imprimibles, interactivo, index)
│                                 # Resto de 1º ESO sin cubrir
│
│  ── Imágenes ──
├── Logo.PNG / favicon.PNG / apple-touch-icon.png / og-image.jpg
├── hero.jpg / quienes-somos.jpg / primaria.jpg / secundaria.jpg / bachiller.jpg
└── julio.jpg / miguel.jpg        # Fotos equipo (todas en uso)
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

### Sub-bloques 1º Primaria (120 fichas)

| Bloque | Sub-bloques (fichas estimadas) | Fichas |
|---|---|---|
| `numeros` ✅ | numeros-hasta-99 (6 ✅) · decenas-unidades (2 ✅) · numeros-ordinales (2 ✅) · comparar-y-ordenar (2 ✅) | **12** |
| `operaciones` ✅ | sumas-sin-llevadas (8 ✅) · restas-sin-llevadas (8 ✅) · sumas-y-restas-mezcladas (4 ✅) | **20** |
| `medida` 🟡 | longitud-peso-capacidad (3 ✅) · monedas-billetes (3 ✅) · el-reloj-en-punto (3 ✅) · dias-semana · meses-año | ~15-25 |
| `geometria` | figuras-planas · cuerpos-geometricos · lineas-y-situacion-espacial | ~10-18 |
| `estadistica` | tablas-simples · pictogramas | ~6-12 |
| `problemas` | problemas-suma-sencillos · problemas-resta-sencillos · problemas-mixtos-basicos | ~12-18 |
| | **Total 1º Mates (rango realista)** | **~75-110 fichas** |

> Total revisado a la baja el 2026-05-28 tras la norma "ajustar fichas al material real disponible". Antes se estimaba 120, pero en 1º muchos conceptos no dan para 6 fichas distintas. La cifra final saldrá según vayamos cerrando cada sub-bloque.

> En 2º+ la cantidad de sub-bloques crece porque entra multiplicación, división informal, fracciones, problemas de dos operaciones, etc. 1º es el curso con menos sub-bloques de toda Primaria.

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
- **1º ESO Matemáticas** — solo álgebra (4 páginas)
- **Total:** ~749 fichas indexadas en sitemap

### Blog (`/blog.html`)
- 4 artículos publicados, todos con enlaces internos a fichas (2026-05-24):
  - `como-elegir-academia-torremolinos.html` (sin enlaces — artículo comercial puro)
  - `como-ayudar-comprension-lectora-primaria.html` (11 enlaces a fichas)
  - `tecnicas-de-estudio-primaria.html` (5 enlaces a fichas)
  - `como-trabajar-ortografia-primaria.html` (9 enlaces a fichas)

### Páginas de servicio
- Logopedia · Psicología · Quiénes somos — en sistema premium, con JSON-LD

---

## Roadmap

### Prioridad alta — orden acordado con Miguel (2026-05-24)

1. **1º Primaria Matemáticas** — estructura acordada con Miguel el 2026-05-24 (detalle completo en sección "Estructura matemáticas Primaria"). 6 bloques (5 LOMLOE + problemas), sub-bloques anidados, **6 fichas/serie**, curso a curso 1º→6º. **Total 1º Mates: 120 fichas**.
   - **Bloque `numeros` COMPLETO ✅** (12 fichas, cerrado 2026-05-28): `numeros-hasta-99` (6) + `decenas-unidades` (2) + `numeros-ordinales` (2) + `comparar-y-ordenar` (2). Patrón en sub-bloques de 2 fichas: ficha-1 con "Recuerda" + ejemplos, ficha-2 solo ejercicios + variación.
   - **Bloque `operaciones` EN MARCHA — `sumas-sin-llevadas` COMPLETO ✅** (8 fichas, cerrado 2026-05-28): ficha-1 con Recuerda (3 ejemplos: una cifra vertical, dos cifras vertical, una cifra horizontal) + sumas básicas + serie 1-10. ficha-2 unir suma↔resultado + serie 11-20. ficha-3 sumas con dibujos (●★▲■) + serie 20-30. ficha-4 descomponer + serie 10-100 de 10 en 10. ficha-5 el doble + serie 40-50. ficha-6 tres sumandos + serie 50-60. ficha-7 y ficha-8 página entera con 20 sumas DU+DU en rejilla 5×4 (fuente 22px, gap 38px) — estilo cuadernillo Rubio.
   - **`restas-sin-llevadas` COMPLETO ✅** (8 fichas, cerrado 2026-05-28): clonadas del patrón de `sumas-sin-llevadas` («cógelo como imagen y lo imitas con restas todo de un tirón»). ficha-1 introducción + Recuerda (7−3, 47−23 D U, 8−5 horizontal). ficha-2 unir resta↔resultado. ficha-3 con dibujos (segundo grupo = se quitan). ficha-4 **completar restas** `7−☐=5` (en lugar de «descomponer al revés»: más natural para 1º). ficha-5 **la mitad** (en lugar de el doble): 2→1, 4→2, 6→3, 8→4, 20→10, 40→20. ficha-6 **restas encadenadas en horizontal** `9−2−1=☐` (no en columna: confunde a 1º). ficha-7 y ficha-8 página entera 20 restas DU−DU (con minuendo≥sustraendo dígito a dígito en cada columna).
   - **`sumas-y-restas-mezcladas` COMPLETO ✅** (4 fichas, cerrado 2026-05-28): sustituye al previsto `calculo-mental` por ser más productivo en 1º. ficha-1 introducción + Recuerda (3 mini-ejemplos: suma vertical, resta vertical, mezcladas horizontal) + ejercicios discriminación de signo (6 columna 1 cifra, 8 horizontal 1 cifra, 4 columna 2 cifras, todo alternando + y −). ficha-2/3/4 página entera con 20 operaciones DU±DU mezcladas en rejilla 5×4 (10 sumas + 10 restas, todo sin llevadas / sin prestar verificado), mismo font/gap que ficha-7/8 de los dos sub-bloques previos.
   - **Bloque `operaciones` COMPLETO ✅** (20 fichas).
   - **Bloque `medida` EN MARCHA — `longitud-peso-capacidad` COMPLETO ✅** (3 fichas, cerrado 2026-05-28): ficha-1 explicación con Recuerda (3 conceptos: longitud, peso, capacidad) + 4 ejercicios (rodear más largo con líneas ▬, más pesado con palabras ELEFANTE/HORMIGA…, más capacidad BAÑERA/VASO…, ordenar 3 tamaños). ficha-2 conceptos opuestos (más corto, más ligero, menos capacidad, ordenar por altura). ficha-3 repaso mixto (unir objeto↔adjetivo, completar frases con ligera/pesada / larga/corta / más/menos, ordenar líneas por longitud y objetos por capacidad).
   - **`monedas-billetes` COMPLETO ✅** (3 fichas, cerrado 2026-05-28): **primer sub-bloque con dibujos SVG inline** — decisión de Miguel: en este tema concreto sí entran dibujos porque el niño debe reconocer el objeto real (no leer "1€" al lado de "1€"). 3 plantillas SVG propias B&N: **moneda céntimo** (círculo + 10 estrellas UE + número grande + "CENT"), **moneda euro** (círculo + anillo bicolor + 12 estrellas + número + "EURO"), **billete** (rectángulo redondeado + número en esquinas + "EURO" centrado + 7 estrellas abajo). ficha-1 explicativa: Recuerda (céntimos/euros/billetes, 100c=1€) + 4 ejercicios (unir moneda↔valor **sin líneas guía** para que el niño dibuje flechas libres, escribir valor debajo, rodear monedas/tachar billetes, contar monedas iguales). ficha-2 ejercicios (unir más variado, contar monedas iguales 4×1€/3×2€/etc, comparar mayor valor en parejas mixtas, sumar monedas distintas). ficha-3 ejercicios (cuenta total con billete+monedas, **¿me llega? rodear SÍ/NO** en 4 escenarios, dibujar libre las monedas/billetes necesarios para 3€/7€/15€). Tamaño SVG ajustado para que entre en 1 folio: moneda 46px / billete 74×42px (ficha-1) y 44px / 70×40px (ficha-2).
   - **`el-reloj-en-punto` COMPLETO ✅** (3 fichas, cerrado 2026-05-28): segundo sub-bloque con SVG inline. **Plantilla reloj analógico** B&N: círculo r=46 + 12 números en posiciones precalculadas (radio ~40, ángulo 30° por hora) + centro como punto + aguja larga vertical hacia arriba (siempre al 12, "en punto") + aguja corta apuntando a la hora con `<line>` desde centro (50,50) a punta calculada. Coordenadas aguja corta por hora: 12→(50,28), 1/2→(68,36), 3→(68,50), 4/5→(68,64), 6→(50,72), 7/8→(32,64), 9→(32,50), 10/11→(32,36). Junto al reloj analógico, **caja digital** con borde + fuente Courier New (estilo display LCD): `.digital` (24px) y `.digital-mini` (18px). ficha-1 explicativa: Recuerda (2 agujas: corta=HORA, larga=MINUTOS; larga al 12 = "en punto"; H:00 en digital) + 4 ejercicios (unir analógico↔digital sin líneas guía, escribir hora digital de 4 relojes, dibujar la aguja corta para 4 horas dadas). ficha-2 ejercicios (unir, escribir, dibujar — variando horas; ej 4 **comparar más tarde** rodeando el reloj de hora mayor en 2 parejas). ficha-3 repaso: dibujar aguja para 4 **actividades cotidianas** (Desayuno 8:00, Recreo 11:00, Comida **14:00**, Cena **21:00** — formato 24h para realismo cultural, el alumno deduce que la aguja sigue apuntando al 2 y al 9), ordenar 4 relojes del más temprano al más tarde (caja con hueco), escribir 3 horas en palabras (`5:00 → las cinco en punto`), completar 2 frases sobre las agujas. Siguiente sub-bloque: `dias-semana`.
   - **Índice web:** `materiales.html` ya alineado para 1º Mates con la estructura de 6 bloques (commit `ec68965`, 2026-05-28). 2º–6º Mates en `materiales.html` siguen con la estructura antigua de 5 bloques — actualizar al arrancar cada curso.

2. **Más artículos de blog SEO** — "Cómo preparar la EBAU en Andalucía", "Qué hacer si tu hijo no aprueba matemáticas", "El paso de Primaria a la ESO". Ideas ya listadas. Después de prioridad 1.

### Prioridad media — más adelante

3. **ESO completa** — 1º ESO tiene solo álgebra. Cubrir resto de matemáticas 1º ESO, luego 2º, 3º, 4º. La estructura `recursos/1-eso/`, `recursos/2-eso/`... ya sigue el mismo patrón.

4. **Migrar `materiales.html` al sistema premium** — sigue con la paleta legacy verde claro. No es urgente pero rompe coherencia visual.

### Prioridad baja — cuando recursos y materiales estén completos

5. **Juegos interactivos** — todo está en `_pendiente/`. Retomar cuando Primaria + ESO estén cubiertos. Cablear `operaciones/`, `mates-iniciales/`, `lectoescritura/` al menos en `juegos.html`.

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
