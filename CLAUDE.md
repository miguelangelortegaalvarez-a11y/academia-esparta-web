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
│   │   └── 6/lengua/     # EN MARCHA ⬅ (Lectura CERRADA 7/7, Gramática D 4/8)
│   │                     # Área Lectura 7/7 ✅:
│   │                     #   - tipologias-textuales (10 fichas)
│   │                     #   - textos-literarios-narrativa (10 fichas)
│   │                     #   - textos-literarios-poesia (10 fichas)
│   │                     #   - textos-literarios-teatro (10 fichas)
│   │                     #   - textos-discontinuos (10 fichas)
│   │                     #   - intencion-autor-subtexto (10 fichas, márgenes 3cm)
│   │                     #   - resumen-y-esquema-avanzado (10 fichas, márgenes 3cm)
│   │                     # Área Gramática D 4/8:
│   │                     #   - analisis-sintactico-sn-sv (10 fichas, márgenes 3cm) ✅
│   │                     #   - oracion-compuesta-coordinadas (10 fichas, márgenes 3cm) ✅
│   │                     #   - oracion-compuesta-subordinadas (10 fichas, márgenes 3cm) ✅
│   │                     #   - verbo-avanzado (10 fichas, márgenes 3cm) ✅
│   │                     # Siguiente: Gramática D — Léxico (cultismos y prefijos griegos/latinos)
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
- Ruta: `recursos/primaria/CURSO/lengua/BLOQUE/nombre-bloque-Xprimaria-serie-Y.html`
- Cada serie = 6 fichas (gramática/lengua) o 10 fichas (comprensión/velocidad).
- El sitemap las recoge automáticamente — no hay que tocar nada más.

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
- **6º Primaria Lengua — EN MARCHA ⬅** (arrancado 2026-05-23):
  - Área Lectura 7/7 ✅ CERRADA (2026-05-24):
    - `tipologias-textuales` (10 fichas) ✅
    - `textos-literarios-narrativa` (10 fichas) ✅
    - `textos-literarios-poesia` (10 fichas) ✅
    - `textos-literarios-teatro` (10 fichas) ✅
    - `textos-discontinuos` (10 fichas) ✅
    - `intencion-autor-subtexto` (10 fichas) ✅ (márgenes 3cm)
    - `resumen-y-esquema-avanzado` (10 fichas) ✅ (márgenes 3cm)
  - Bloque D Gramática 4/8:
    - `analisis-sintactico-sn-sv` (10 fichas) ✅ (márgenes 3cm, cerrado 2026-05-24)
    - `oracion-compuesta-coordinadas` (10 fichas) ✅ (márgenes 3cm, cerrado 2026-05-24)
    - `oracion-compuesta-subordinadas` (10 fichas) ✅ (márgenes 3cm, cerrado 2026-05-24)
    - `verbo-avanzado` (10 fichas) ✅ (márgenes 3cm, cerrado 2026-05-24)
  - Estructura prevista: 7 sub-bloques Lectura + 8 Gramática = 150 fichas
  - Sub-bloques Gramática D pendientes (4): Léxico (cultismos, prefijos griegos/latinos) · Polisemia/homonimia/paronimia · Ortografía avanzada · Puntuación nivel ESO
- **1º ESO Matemáticas** — solo álgebra (4 páginas)
- **Total:** ~709 fichas indexadas en sitemap

### Blog (`/blog.html`)
- 4 artículos publicados:
  - `como-elegir-academia-torremolinos.html`
  - `como-ayudar-comprension-lectora-primaria.html`
  - `tecnicas-de-estudio-primaria.html` (publicado 2026-05-23)
  - `como-trabajar-ortografia-primaria.html` (publicado 2026-05-24, con 7 enlaces a fichas)

### Páginas de servicio
- Logopedia · Psicología · Quiénes somos — en sistema premium, con JSON-LD

---

## Roadmap

### Prioridad alta — orden acordado con Miguel (2026-05-24)

1. **Acabar 6º Primaria Lengua** — Área Lectura CERRADA 7/7 ✅. Bloque D Gramática 4/8 ✅. **Quedan 4 sub-bloques de Gramática D** (~40 fichas a 10/sub-bloque): Léxico (cultismos, prefijos griegos/latinos) · Polisemia/homonimia/paronimia · Ortografía avanzada · Puntuación nivel ESO. Patrón: 10 fichas por sub-bloque, dificultad progresiva ⭐→⭐⭐⭐⭐, registro en `materiales.html` con clave `'lengua|6|D|Nombre'`. **Márgenes @page 3cm laterales**. **Siguiente sub-bloque: Léxico (cultismos y prefijos griegos/latinos).**

2. **Enlazar fichas desde el blog** — los 3 artículos publicados no apuntan a fichas concretas. Añadir enlaces internos contextuales desde cada artículo hacia fichas relevantes. Palanca SEO de alto retorno sin contenido nuevo.

3. **Matemáticas Primaria** — empezar a cubrir el área de Mates. Miguel adelantó que **la organización será diferente** a Lengua. NO arrancar hasta acordar la estructura con él (probablemente bloques tipo operaciones, números, geometría, medida, problemas).

### Prioridad media — más adelante

4. **Más artículos de blog SEO** — "Cómo preparar la EBAU en Andalucía", "Qué hacer si tu hijo no aprueba matemáticas", "El paso de Primaria a la ESO". Ideas ya listadas. Después de prioridad 2.

5. **ESO completa** — 1º ESO tiene solo álgebra. Cubrir resto de matemáticas 1º ESO, luego 2º, 3º, 4º. La estructura `recursos/1-eso/`, `recursos/2-eso/`... ya sigue el mismo patrón.

6. **Migrar `materiales.html` al sistema premium** — sigue con la paleta legacy verde claro. No es urgente pero rompe coherencia visual.

### Prioridad baja — cuando recursos y materiales estén completos

7. **Juegos interactivos** — todo está en `_pendiente/`. Retomar cuando Primaria + ESO estén cubiertos. Cablear `operaciones/`, `mates-iniciales/`, `lectoescritura/` al menos en `juegos.html`.

8. **Bachillerato** — crear `recursos/1-bachillerato/` y `recursos/2-bachillerato/` con fichas de las asignaturas principales.

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

**Frase trigger:** _"Seguimos con las fichas"_ o _"Vamos con [bloque] de [Nº Primaria]"_ → ir directo al roadmap, sin preguntar.
