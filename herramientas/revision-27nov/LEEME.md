# Herramientas de la revisión del 27-nov-2026

- `cuentas.py` — pasa las cuentas de 1º (suma-col, op-col, ej-col-mini, horizontales, series…) a **Nunito, mismo tamaño, una casilla por cifra**. `aplicar(html)`.
- `reparte.py` — vuelve a repartir una ficha en páginas midiendo con Chrome: no parte ejercicios salvo las rejillas grandes de cuentas (por filas completas); el «¡Buen trabajo!» suelto se pega a la página anterior. Usa `cdp.mjs` (copiar a `/tmp/negritas/cdp_rep.mjs` cambiando `eval.js`→`eval_rep.js` y `res.json`→`res_rep.json`).
- `bloques.py` — bloques de base 10 en 3D (U verde suelta, D azul, C roja).
- `cdp.mjs` — Chrome headless por CDP: carga una lista de fichas y ejecuta `/tmp/negritas/eval.js` en cada una.

Después de tocar una ficha: regenerar su PDF con Chrome (`--headless --no-pdf-header-footer --virtual-time-budget=8000`) y comprobar páginas y pie.
