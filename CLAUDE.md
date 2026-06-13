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

**Hecho:**
- **Reseñas Google 63 → 64** en 5 sitios (index.html: chip hero, contador `data-target`, label rating, chip rotativo JS; + `como-elegir-academia-torremolinos.html`).
- **153 botones "← Volver" rotos (404) arreglados** — eran error de plantilla (mal número de `../`): Lengua necesita 5 niveles `../../../../../materiales.html`, Mates 6 niveles `../../../../../../materiales.html`. Verificar SIEMPRE al crear plantilla nueva.
- **Índice `conciencia-fonologica`** reescrito: 8 cards inventadas → 5 fichas reales.
- **Rendimiento:** imágenes recomprimidas con `sips` (~1,5 MB ahorrados: hero 914→359 KB, Logo 371→98 KB, etc.) + `preload`/`fetchpriority` del hero + `preconnect` a fuentes. El hero es **background-image CSS** (por eso disparaba el LCP).
- **`aggregateRating` 4,9 · 64** en JSON-LD (estrellas Google). Caveat: Google puede no mostrar estrellas de reseñas autodeclaradas sin widget.
- Meta description en `inscripcion.html`.

**Foto técnica:** HTTPS ✅, SEO 100/100, 0 enlaces/recursos rotos, todas las imágenes con `alt`, Umami **sin cookies** (no necesita banner RGPD), web pública **sin `<form>`** (inscripción → `shadow.academiaesparta.es`, contacto por WhatsApp).

**Pendiente (rendimiento):** aligerar fuentes (3 familias) + Font Awesome (con cuidado, no romper diseño); WebP (falta cwebp/imagemagick en la máquina); cabeceras de seguridad 0/4 (GitHub Pages no las permite → opcional Cloudflare delante, no urgente).

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

**Bloque `problemas` de 2º — EN MARCHA (ÚLTIMO bloque de 2º). Serie = 6 fichas (Miguel, 2026-06-13).**
- **`problemas-suma-con-llevada` (6 fichas, COMPLETO ✅, commit ca3f3e2, 2026-06-13) — abre el bloque.** Generadas con **6 agentes en paralelo (1 por ficha)** de fácil→difícil (método que pidió Miguel para este sub-bloque). Reusan `ficha-1` como plantilla (componente `.problema` con zona OPERACIÓN + SOLUCIÓN, clonado de 1º). f1 2 sumandos DU+DU ≤99 + Recuerda + dibujos · f2 refuerzo · f3 ≤99 números altos (6 problemas, sin Recuerda, los últimos sin icono `grid-template-columns:1fr`) · f4 **tres sumandos** ≤99 · f5 resultado **pasa de 100** (llevada a centenas, avisada en Recuerda) · f6 repaso mezcla (6 problemas). **Números fijados por mí y verificados dígito a dígito** (llevada en unidades garantizada); los agentes solo redactan enunciados + montan HTML. ⚠️ **Nivel 2º:** la llevada doble (a centenas) solo aparece en f5/f6 y SIEMPRE avisada en Recuerda.
- **`problemas-resta-con-prestar` (6 fichas, COMPLETO ✅, 2026-06-13).** Mismo método (6 agentes en paralelo, 1/ficha, fácil→difícil, que pidió Miguel). **Números fijados por mí y verificados dígito a dígito con script Python: TODAS prestan en unidades (U del minuendo < U del sustraendo) y resultado positivo.** f1 DU−DU básico + Recuerda + dibujos · f2 refuerzo · f3 números altos hasta 99 (6 problemas, sin Recuerda) · f4 **comparación** (¿cuántos más?/¿cuánto falta? → también se resuelve restando) · f5 **restar a números de 3 cifras** (minuendo >100, préstamo único en U, resultado de 3 cifras; avanzado pero adaptado a 2º, SIN doble préstamo) · f6 repaso mezcla (6 problemas, 1 sin icono). Registrado en `materiales.html` (entrada `matematicas|2|PROBLEMAS|Problemas de resta con prestar`).
- ⚠️ **LECCIÓN llenado/impresión (2026-06-13):** las fichas de `.problema` a 90-99% de llenado (medido en Chrome headless `validar_ficha.py`) **se van a 2 páginas POR POCO al imprimir en Safari/diálogo de impresión** (mete su propio margen; Chrome headless NO lo reproduce, dice 1 página). Corregido TODO el bloque (suma+resta, 12 fichas) bajando `.problemas gap 13→9`, `.problema padding 9px→6px`, `.zona min-height 60→54` → llenado **~85-92% con aire bajo el footer**. **NORMA mates problemas: apuntar a 85-92%, NO 95-99%.** El "OK hasta 99%" del validador es engañoso para impresión real.

**Arrancar por:** ~~`numeros`~~ ✅ (21) → ~~`operaciones`~~ ✅ (33) → ~~`medida`~~ ✅ (19) → ~~`geometria`~~ ✅ (16) → ~~`estadistica`~~ ✅ (12) → **`problemas` EN MARCHA: ~~suma-con-llevada~~ ✅ (6) → ~~resta-con-prestar~~ ✅ (6) → multiplicacion · dos-operaciones · mixtos.**

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
- **1º ESO Matemáticas** — solo álgebra (4 páginas)
- **Total:** ~820 fichas indexadas en sitemap

### Blog (`/blog.html`)
- 5 artículos publicados, casi todos con enlaces internos a fichas:
  - `como-elegir-academia-torremolinos.html` (sin enlaces — artículo comercial puro)
  - `como-ayudar-comprension-lectora-primaria.html` (11 enlaces a fichas)
  - `tecnicas-de-estudio-primaria.html` (5 enlaces a fichas)
  - `como-trabajar-ortografia-primaria.html` (9 enlaces a fichas)
  - `como-ayudar-matematicas-primaria.html` (2026-06-04, commit 9ca66b7, 18 enlaces a fichas de mates 1º-2º — primer artículo de mates; 3 pilares número/cálculo/problemas; enlaza a psicología por discalculia)

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
   - **1º MATES COMPLETO ✅** (2026-05-28, 71 fichas totales: 12+20+15+9+6+9). **Siguiente:** arrancar **2º Primaria Matemáticas**. Estructura mismos 6 bloques pero los sub-bloques crecen (multiplicación, división informal, fracciones básicas, problemas con dos operaciones, sumas/restas CON llevada/prestar, números hasta 1000). Actualizar primero el árbol de 2º en `materiales.html` (sigue con la estructura antigua de 5 bloques).

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
