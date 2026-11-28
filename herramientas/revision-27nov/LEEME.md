# Herramientas de la revisión del 27-nov-2026

- `cuentas.py` — pasa las cuentas de 1º (suma-col, op-col, ej-col-mini, horizontales, series…) a **Nunito, mismo tamaño, una casilla por cifra**. `aplicar(html)`.
- `reparte.py` — vuelve a repartir una ficha en páginas midiendo con Chrome: no parte ejercicios salvo las rejillas grandes de cuentas (por filas completas); el «¡Buen trabajo!» suelto se pega a la página anterior. Usa `cdp.mjs` (copiar a `/tmp/negritas/cdp_rep.mjs` cambiando `eval.js`→`eval_rep.js` y `res.json`→`res_rep.json`).
- `bloques.py` — bloques de base 10 en 3D (U verde suelta, D azul, C roja).
- `vivas.py` — (28-nov) cuentas «vivas» en las 20 fichas de operaciones de 1º: D roja / U azul encima, casillas teñidas, números grandes, 3 por fila, emoji en cada enunciado, «⭐ ¡Muy bien! 🏆», y MENOS cuentas (una cifra 6→3, horizontales 6→4, dos cifras 4→3, práctica del «Mira cómo se hace» solo una fila de 3, hojas enteras 20→9). Idempotente.
- `alegres.py` — (28-nov) emojis en las fichas de 1º que tenían ≤2 (91: Lengua comprensión/opciones/lecturas + Mates números/geometría/medida/problemas): emoji por tema en cada enunciado, emoji de lo que se cuenta en cada problema, dibujo junto al texto en las lecturas, «⭐ ¡Muy bien! 🏆» donde había «¡Buen trabajo!» (no se añade donde no había: pisa el pie). Si un enunciado se parte por el emoji y empuja contra el pie, quitarle el emoji (pasó en figuras-planas f3 ej3 y reloj f2 ej4).
- `medida.py` — (28-nov) medida de 1º: longitud-peso-capacidad con emoji en cada objeto + barras dibujadas en vez de ▬▬▬ + «BOTELLA VACÍA»→«BOTELLA SIN AGUA» (regalaba la respuesta) y «DEDAL»→«VASO»; reloj con relojes de dibujar 64→84 px (los de «Une» 78→62) y parejas de «más tarde» en recuadro a) b). `alegres.py --forzar` para fichas con dibujos (monedas). Si algo pisa el pie: `<style id="fin-compacto">` o quitar el emoji del enunciado que se parte.
- `cdp.mjs` — Chrome headless por CDP: carga una lista de fichas y ejecuta `/tmp/negritas/eval.js` en cada una.

Después de tocar una ficha: regenerar su PDF con Chrome (`--headless --no-pdf-header-footer --virtual-time-budget=8000`) y comprobar páginas y pie.
