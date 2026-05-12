# Guía de diseño · Academia Esparta

Última revisión: 13/05/2026 — refundición visual al sistema premium.

---

## 🎨 Sistema premium (web pública)

Coherente con el form de inscripción (`shadow.academiaesparta.es/inscripcion`).

### Tipografía

| Uso | Fuente | Peso |
|---|---|---|
| Titulares (h1, h2, h3 grandes) | **Fraunces** (serif) | 400 |
| Cuerpo, navs, badges, botones, labels | **Poppins** (sans) | 300, 400, 500, 600 |
| Frase italic destacada | Fraunces italic | 400 |
| Fichas de Primaria 1º-2º (material impreso, NO web) | **Edu SA Beginner** | 400-700 |

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,300..600,0..100&family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
```

### Paleta

| Variable | Valor | Uso |
|---|---|---|
| Fondo principal | `#064e3b` | Hero, Logopedia, Recursos |
| Fondo alterno | `#053a2c` | Stats, About, Psicología, Contact |
| Fondo footer | `#032519` | Más oscuro, solo footer |
| Texto blanco | `#ffffff` | Titulares serif |
| Texto cuerpo | `rgba(236,253,245,0.7)` | Párrafos sans |
| Acento brillante | `#4ade80` | Pulse dot, links, glows |
| Acento label | `rgba(167,243,208,0.85)` | Labels uppercase, hover sutil |
| Borde sutil | `rgba(74,222,128,0.18-0.25)` | Cards, pills, separadores |
| Glow ambient | `rgba(74,222,128,0.06-0.15)` | Auroras, backgrounds suaves |

### Componentes reutilizables

**Eyebrow pill** (label encima del título):
```html
<div class="ap-eyebrow">
  <span class="hp-pulse"></span>
  ETIQUETA · SEPARADOR · DETALLE
</div>
```
Borde verde sutil, fondo translúcido verde, texto uppercase letterspacing 0.22em, punto pulsante verde brillante a la izquierda.

**Título Fraunces**:
```css
font-family: 'Fraunces', serif;
font-weight: 400;
font-size: clamp(2rem, 4.5vw, 3.4rem);
letter-spacing: -0.025em;
line-height: 1.1;
color: #fff;
```

**CTA primary** (botón blanco redondo con glow):
```html
<a class="hp-cta-primary">Texto<svg>→</svg></a>
```
Background blanco, color emerald-900, padding 1rem 2.5rem, border-radius 9999px, glow verde conic-gradient animado alrededor.

**CTA ghost** (botón secundario translúcido):
```html
<a class="hp-cta-ghost">WhatsApp</a>
```
Borde blanco translúcido, fondo blanco 4% con blur.

**Aurora drifting** (fondo decorativo):
```html
<div class="hp-aurora hp-a1"></div>
<div class="hp-aurora hp-a2"></div>
<div class="hp-aurora hp-a3"></div>
```
Position absolute, blur 100px, mix-blend-mode screen, animación drift 24-30s.

### Ritmo de secciones

Para crear ritmo visual entre secciones contiguas, alternar:
- Sección A: `background: #064e3b` (más claro).
- Sección B: `background: #053a2c` (más oscuro).
- Sección C: `background: #064e3b`.

Padding `5rem 1.5rem` desktop, `4rem 1rem` mobile.

### Forzar `.reveal` visible (TRAMPA)

El sistema de scroll-reveal con `opacity: 0` puede dejar contenido invisible si el observer falla. **En cada sección premium SIEMPRE añadir**:
```css
.tu-seccion-premium .reveal {
  opacity: 1 !important;
  transform: none !important;
}
```

### Trampa — auroras y `#about > *`

El CSS legacy `#about > * { position: relative; z-index: 1 }` tiene ID-selector y sobreescribe el `position: absolute` de las auroras. Forzar con `!important`:
```css
.tu-seccion .aurora {
  position: absolute !important;
  z-index: 0 !important;
}
```

---

## 📄 Sistema de fichas imprimibles (NO web)

Las fichas (`/recursos/...`) y materiales (`material.html`) **NO usan el sistema premium**. Mantienen su propio estilo (Formato A/B/C según curso, B&N para imprimir). Ver `proyecto-web.md` en memoria para detalle.

---

## Histórico — paleta legacy (pre 13/05/2026)

Mantenida solo para referencia. NO usar en páginas nuevas.

| Variable | Valor | Uso original |
|---|---|---|
| `--primary` | `#0e9343` | Verde principal claro |
| `--primary-dark` | `#09834c` | Hover |
| `--primary-darker` | `#0a5233` | Fondos oscuros |
| `--accent` | `#f16565` | Acentos coral |
| `--light` | `#f5fdf7` | Fondo claro |

---

## Decisión 13/05/2026

Refundición visual completa de `index.html` + `quienes-somos.html` + `inscripcion.html` (redirección) al sistema premium.

**Motivo**: la web mezclaba 3 tipografías (Poppins, Nunito 800, cursivas) y paletas inconsistentes, lo cual desentonaba con el form de inscripción de calidad muy superior. Miguel quería que la web "pareciera super profesional y currada" para reflejar la calidad real del negocio.

**Resultado**: web → form → todo en mismo lenguaje visual editorial premium.
