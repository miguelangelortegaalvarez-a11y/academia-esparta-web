# Web Pública Academia Esparta

Web estática de captación y recursos educativos gratuitos. Sin backend propio — push a `main` = producción inmediata.

**URL pública:** https://academiaesparta.es · GitHub Pages · rama `main`

---


## 🗂️ Qué se lee y cuándo (reorganización del 27-nov-2026)

Al abrir, **solo este fichero**. Lo de fichas se lee cuando Miguel pide algo de fichas, y **antes de afirmar un estado se comprueba en el código** (PDF que existen, git log), no en el recuerdo.

| Si Miguel pide… | Se lee antes |
|---|---|
| **Fichas en formato nuevo** (letras, conciencia, convertir 1º-2º, 3º-4º en Nunito, Leoni, interactivas con voz) | `.claude/contexto/formato-nuevo.md` |
| **Fichas de Mates** (cualquier curso, sub-bloques, recetas, asserts, validador) | `.claude/contexto/fichas-mates.md` |
| **Seguir con 6º de Mates** | `.claude/contexto/mates-6.md` (+ `fichas-mates.md`) |
| **Algo de lo hecho en Mates 1º-5º** (cómo se hizo un sub-bloque, sus niveles, un componente SVG) | `.claude/contexto/historico/mates-N.md` (buscar con grep, no leer entero) |
| **Rendimiento, fuentes, SRI, árbol completo de carpetas** | `.claude/contexto/web-tecnico.md` |
| **Diseño de páginas web** | `DISENO.md` |
| Blog, SEO, reseñas, deploy, juegos, privacidad… | Su memoria (índice `MEMORY.md`) |

🗄️ Lo viejo (no son pendientes): `.claude/contexto/historico/` — Mates 1º-5º, recuento de contenido publicado y roadmap antiguo. Copia de antes del cambio: tag `antes-reorganizar-27nov`.

---

## Estado de las fichas (comprobado el 27-nov-2026)

| Curso | Lengua | Mates | Formato |
|---|---|---|---|
| 1º | 92 | 71 | ✅ **Nuevo** (página + PDF, ligada Playwrite) |
| 2º | 130 | 131 | ✅ **Nuevo** (página + PDF, ligada más suave) |
| 3º | 79 | 198 | Piloto nuevo en **6** (Nunito); las otras 271 en formato antiguo — **aparcado** |
| 4º | 108 | 198 | Antiguo |
| 5º | 150 | 204 | Antiguo |
| 6º | 150 | 114 (19/34) | Antiguo — Mates **parado** desde el 27-sep |

Además: 1º ESO Mates solo álgebra (4 páginas) · blog con 9 artículos · servicios Logopedia, Psicología, Quiénes somos.

## Estructura (resumen; árbol completo en `web-tecnico.md`)

- Páginas premium en la raíz: `index.html`, `quienes-somos.html`, `logopedia.html`, `psicologia.html`, `blog.html` + artículos, `404.html`, `juegos.html`. `materiales.html` = índice React de fichas (paleta legacy).
- Fichas: `recursos/primaria/CURSO/{lengua,matematicas}/…` · índices estáticos por curso y asignatura en `recursos/primaria/CURSO/ASIGNATURA/index.html`.
- Herramientas del formato nuevo: `herramientas/{fichas-letras,fichas-conciencia,fichas-formato-nuevo,fichas-3-4}/`. Fuente ligada en `fuentes/`, mascota en `mascota/leoni/`.
- `juegos/` = piloto local SIN subir · `_pendiente/` = interactivos aparcados (públicos, con `Disallow` en robots).
- ⛔ No tocar `google690465498c577da0.html` (verificación de Search Console).

---

## Stack

| Capa | Tecnología |
|---|---|
| Lenguaje | HTML5 / CSS3 / JS vanilla — sin build, sin npm |
| Fuentes web | Google Fonts: **Fraunces** (serif, títulos) + **Poppins** (sans, cuerpo) |
| Fuente fichas imprimibles | **Playwrite ES** (1º–2º Primaria, ligada escolar, servida desde `fuentes/`, desde 22-nov-2026) / **Nunito** (3º-4º en formato nuevo, desde 23-nov-2026) / **Poppins** (resto de 3º+, formato antiguo) |
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
| Deploy | Push a `main` → publicado en segundos. Sin servidor, sin Docker. **`.nojekyll` en la raíz (2026-07-17, commit fddcb30): Pages ya NO procesa con Jekyll — el paso "Build with Jekyll" fallaba al crecer el sitio (~1.240 págs). Sirve estático directo (más rápido, sin ese fallo). EFECTO: `_pendiente/` ya se publica → blindado con `Disallow: /_pendiente/` en robots.txt. Diagnóstico de fallos de deploy y detalle: memoria `reference-deploy-web`.** |
| Sitemap | Regenerado por CI **por cron diario (05:00 UTC) + disparo manual** — NO en cada push (cambiado 2026-07-05: el doble-deploy topaba el límite de Pages de la cuenta; ver memoria `reference-deploy-web`) |

---

## Sistema visual premium

Refundición del 13/05/2026. Documentación completa en `DISENO.md`.

**Páginas en sistema premium:** `index.html`, `quienes-somos.html`, `logopedia.html`, `psicologia.html`, `blog.html`, `404.html`, `juegos.html`.

**Páginas en paleta legacy** (verde claro `#0e9343`, pendiente migrar): `materiales.html`.

**Firma de autoría (2026-07-03, commit `3521de5`):** línea `Diseño y desarrollo por Miguel Ángel Ortega Álvarez` bajo el copyright del footer (centrada, uppercase, `letter-spacing:.16em`, tenue `rgba(236,253,245,0.3)`, inline en el `<p class="footer-credit">`). En las **13 páginas premium** con footer. Marca de identidad común a todas las webs de Miguel (nace de `moma`). Detalle en memoria `reference_firma_autoria`.

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
- ⚠️ **Impresión desde el MÓVIL (20-sep-2026):** al imprimir una ficha desde el iPhone sale «Página 1 de 2» con el pie en la segunda hoja. **No es un fallo de la ficha** — Safari de iOS ignora el `@page{margin:0}` y añade su margen (~1,27 cm/lado) más las bandas de encabezado y pie con la URL: ~8 cm de folio perdidos. **Se arregla bajando la *Escala* al 87-90 %** en el propio diálogo de impresión. Comprobado que **la f1 de 3º (en producción desde junio) se parte antes que las nuevas de 5º**, así que el criterio de llenado no está mal: el que cambia es el entorno de impresión. El validador (Chrome, `--no-pdf-header-footer`) no ve nada de esto. Pendiente sin decidir: si se quiere cubrir el caso «padres que imprimen desde el móvil», hay que recortar ~2,5 cm por ficha y eso afecta a las ~1.300 del sitio → tarea propia, no de un sub-bloque.
- ⚠️ **Ver fichas en el MÓVIL (26-sep-2026):** con `viewport width=device-width` el móvil maqueta la ficha a su ancho (≤500 px) y las filas que no se parten (operaciones, fracciones, tablas) **se salían por la derecha**: 41 de 66 fichas de 6º, hasta 102 px. En ordenador y tableta (≥820 px), 0. **Arreglo: `<meta name="viewport" content="width=820" />`** → el móvil maqueta a 820 px y encoge la ficha entera (vista de folio, se amplía con los dedos). La impresión no cambia. Aplicado a las 66 de 6º y al generador `/tmp/ocf/motor.py`. **Pendiente decidir: 1º-5º (y Lengua) siguen con `device-width`**; comprobar con `/tmp/scr/medir.py` (inyecta JS, mide lo que sobresale del body a un ancho dado).
- Fuente 1º–2º: **Playwrite ES** (cambio del 22-nov-2026, antes Edu SA Beginner; decisión de Miguel, la usa con alumnos de esas edades). Fuente 3º+: **Poppins**.
  - **Cómo se carga:** NO desde Google Fonts, sino desde `fuentes/playwrite-es.woff2` (licencia SIL OFL en `fuentes/OFL-playwrite-es.txt`) con un `@font-face` al principio del `<style>` de cada ficha, ruta relativa (`../` según profundidad) y **`size-adjust: 125%` en 1º y `115%` en 2º** (agranda solo esa letra; números/cajas/dibujos sin tocar). Copiarlo tal cual al crear fichas nuevas de 1º-2º.
  - **Es más ancha y tiene trazos altos y bajos:** (1) los títulos/filas en `display:flex` con texto + `<strong>` sueltos se desordenan si parten en dos líneas → envolver el texto en `<span class="txt-flex">` (regla `.txt-flex { flex: 1 1 auto; min-width: 0; }`); (2) los textos de varias líneas necesitan interlineado holgado → `line-height: 1.875` en 1º / `1.725` en 2º (bloque `interlineado-playwrite`).
  - **Folios:** Miguel acepta 2 folios si hay contenido real en el segundo. Las fichas que se pasaban por poco llevan `@media print { body { zoom: 0.85-0.97 } }` (bloque `ajuste-impresion`) para no dejar una hoja con solo el pie. Resultado al cambiar: 331 a 1 folio (153 con ajuste) + 93 a 2 folios.
- Las fichas NO usan el sistema visual premium de la web.
- Ruta Lengua: `recursos/primaria/CURSO/lengua/BLOQUE/nombre-bloque-Xprimaria-serie-Y.html`
- Ruta Mates: `recursos/primaria/CURSO/matematicas/BLOQUE/SUB-BLOQUE/nombre-sub-bloque-Xprimaria-serie-Y.html`
- Cada serie = 6 fichas (gramática/lengua/mates) o 10 fichas (comprensión/velocidad).
- El sitemap las recoge automáticamente — no hay que tocar nada más.
- **Al cerrar un sub-bloque (norma ampliada 2026-07-03):** además de registrar la entrada en `RECURSOS` de `materiales.html`, ejecutar **`node generar-indices-recursos.mjs`** → regenera los índices estáticos `recursos/primaria/CURSO/ASIGNATURA/index.html` (páginas rastreables por curso+asignatura con enlaces `<a>` a todas las fichas; los robots de IA no ejecutan el React de materiales.html, así que sin estos índices el catálogo es invisible para ellos). El script valida que cada enlace exista en disco. **Ese mismo script regenera también `buscador-fichas.json`** (datos del buscador de fichas de la home, `#buscador-fichas`, desde 22-nov-2026): hay que commitearlo junto con los índices. Después ejecutar **`node anadir-seo-fichas.mjs`** → añade meta description (rica, desde RECURSOS) + canonical a las fichas nuevas que no la tengan (idempotente; hecho en masa a las 1.155 páginas el 2026-07-03).

---


## Formato nuevo de fichas (desde 22-nov-2026) — resumen

**Detalle, herramientas y normas de Miguel: `.claude/contexto/formato-nuevo.md` (leerlo antes de tocar fichas).**

- Cada ficha = página web (misma dirección de siempre) + **PDF generado con Chrome** + botón «📄 Descargar PDF para imprimir». Se acaban las peleas de 1 folio / Safari / iPhone.
- Estilo: cabecera blanca «Academia Esparta» en verde + lema + pastilla, cajas ligeras de tinta, en color, «Mira cómo se hace». 1º-2º en **ligada Playwrite ES**; 3º-4º en **Nunito** con el interior rediseñado (Recuerda verde claro, bordes finos).
- **El contenido NO se toca: se cambia el formato.** Más aire; si no cabe, a 2 páginas, y la última se rellena con ejercicios NUEVOS con modelo.
- ⛔ Interactivas SOLO en letras y conciencia fonológica de 1º.
- Método: muestra por plantilla → OK de Miguel → bloque → revisar las miniaturas de TODAS las páginas → subir.
- **Revisión de Miguel (27-28 nov 2026), 1º-2º:** marco común con el Tutor; enunciado ≥12 px de lo de debajo; ejemplos sin recuadro; bloques base 10 en 3D. **28-nov, «que no sean sosas»:** cuentas «vivas» (D roja / U azul, Nunito grande, casillas en color, MENOS cuentas) en operaciones de 1º y 2º; emojis en todas las fichas sosas de 1º y 2º + «⭐ ¡Muy bien! 🏆»; medida de 1º con dibujos; **problemas 1º-2º en columnas Datos | Operación | Solución con cuenta en blanco**. Herramientas: `herramientas/revision-27nov/` (LEEME). **28-nov tarde:** multiplicación y doble-mitad de 2º vivas (`mult2.py`) + Nunito cargada de verdad en 51 fichas (antes salía Helvetica). **Siguiente:** Lengua 2º; luego 3º. Detalle en la memoria `project_revision_fichas_27nov`.

---

## Roadmap

### Prioridad alta
1. **Formato nuevo en 3º** — 271 fichas aparcadas. Propuesta sin decidir: «repintado» por programa con muestra variada de 5-6 fichas, Lengua primero. Luego 4º.
2. **6º de Mates** — 15 sub-bloques sin hacer. Decidir con Miguel si se sigue y en qué formato (`mates-6.md`).

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

1. Este fichero + la tabla «Qué se lee y cuándo». Nada más hasta que Miguel pida algo.
2. Antes de decir que algo está hecho o pendiente, comprobarlo en el código (PDF, git log), no en el recuerdo.
3. Push a `main` = producción. Sitemap por cron diario.
4. **Regla de mantenimiento:** cuando algo se resuelve o cambia, se SUSTITUYE el párrafo viejo (no se añade otro). Lo terminado sale de aquí y va a su cajón o a `historico/`. Las reglas y recetas no se quitan.

**Frase trigger:** _"Seguimos con las fichas"_ / _"Seguimos con mates"_ → leer el cajón que toque (tabla de arriba) y el roadmap.
