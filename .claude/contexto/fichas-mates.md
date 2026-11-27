> Movido tal cual desde CLAUDE.md el 27-nov-2026 (reorganización). Copia anterior: tag `antes-reorganizar-27nov`.

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


## Recetas que se repiten (resumen; el detalle con ejemplos está en `historico/mates-N.md` y `mates-6.md`)

- **Números fijados y verificados por código** (asserts) ANTES de montar: llevadas/préstamos, divisiones (cociente, resto < divisor, prueba), conteos, áreas. En geometría, script por trig, nunca a ojo.
- **Script > agentes** cuando hay precisión (reloj, casita, gráficos, geometría, conteos de iconos). Agentes en paralelo solo para redactar sobre una ancla f1 hecha a mano; luego re-validar EN LOTE y con nombres de PDF únicos (se pisan).
- **Regalos (el validador no los ve):** el ejemplo del Recuerda no puede ser un ejercicio ni su resultado; una respuesta no puede salir impresa como dato en la ficha; un V/F no puede copiarse del Recuerda; los V/F y SÍ/NO no alternan; la correcta no cae siempre en el mismo sitio.
- **Atajos:** en jerarquía, la expresión debe dar distinto operando de izquierda a derecha; en «elige la operación», ni «una de cada» ni números que la delaten; en varios pasos, el resultado no puede salir con UNA operación entre dos datos.
- **Realismo:** leer cada enunciado preguntándose si la cantidad es creíble (clases ≤ 25, nada de ciudades que crecen un 55 %).
- **Problemas:** 4 por ficha (rejilla 2×2 en × y ÷), un solo marco, zona de operación con sitio real para la cuenta vertical; iconos elegidos mirando una hoja de contactos, no por índice.
- **B/N:** grises a ≥ 40-48 niveles entre sí; con más de 3 categorías, tramas; divisoria blanca entre sectores oscuros; nada de emojis que impriman mancha (⚠️, ⚖️, 🍰, 🛞).
- **Medir:** Chrome `--print-to-pdf --virtual-time-budget=4000`, ruta ABSOLUTA; `sips` mete marco negro (medir dentro de los píxeles claros); comprobar también desborde por la derecha (Chrome encoge la página y el llenado BAJA). Páginas con regex `/Type\s*/Page(?![s])`.
- **CSS:** `min-width:0` en hijos de grid; nada de flex en frases con texto suelto (se separan los trozos); `nowrap` en número+unidad y en fórmulas; antes de inventar una clase, mirar que no exista en el chasis.
