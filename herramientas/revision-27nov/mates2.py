#!/usr/bin/env python3
"""(28-nov-2026) Mates 2º (números, geometría, medida, estadística, problemas): letra y números.

Paso 1 (fijo, en el HTML):
  - carga Nunito de verdad (link + font-variation-settings:normal en lo que la usa);
  - C / D / U en color, como en las cuentas (C verde, D roja, U azul) — solo en números,
    menos ordinales (allí A B C… son letras de una fila);
  - «⭐ ¡Buen trabajo!» → «⭐ ¡Muy bien! 🏆», igual que el resto.
Paso 2 (medido con Chrome, `--medir`): cada pieza con letra < 15 px sube a 15 px; las piezas que
  solo llevan números (345, 4 + 5, 1 m = 100 cm…) pasan a Nunito 700. Se escribe en
  <style id="mates2-auto">, que se rehace entero cada vez (idempotente).
Después: reparte.py (sin --unir) y regenerar el PDF.
Uso: python3 mates2.py [--medir] ficha.html …   (rutas desde la raíz del repo)
"""
import json, os, re, subprocess, sys

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'recursos', 'primaria')
LINK = ('<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@500;600;700;800'
        '&amp;display=swap" rel="stylesheet" />')
CSS = """<style id="mates2-fijo">
.m2l-c,.m2l-d,.m2l-u{font:800 1.3em 'Nunito',sans-serif;font-variation-settings:normal}
.m2l-c{color:#2e8b57}.m2l-d{color:#d64541}.m2l-u{color:#2f6fd6}
</style>"""
FIN_MB = '<div class="fin pw vv-fin"><span class="e">⭐</span><span>¡Muy bien!</span><span class="e">🏆</span></div>'

JS = r"""(() => {
  const MIN = 15, out = {};
  const NUM = /^[\d\s.,:+\-−×x÷=<>()€%/]+(?:\s?(?:cm|m|kg|g|l|€|h))?$/i;
  const sel = el => {
    const cls = [...el.classList].filter(c => !/^(pw|mz)$/.test(c));
    if (cls.length) return '.' + cls[0];
    const p = el.parentElement; if (!p) return null;
    const pc = [...p.classList].filter(c => !/^(pw|mz)$/.test(c));
    if (pc.length) return '.' + pc[0] + ' > ' + el.tagName.toLowerCase();
    let a = p.parentElement;
    while (a && !a.classList.length) a = a.parentElement;
    return a ? '.' + a.classList[0] + ' ' + el.tagName.toLowerCase() : null;
  };
  document.querySelectorAll('.pagina').forEach(pg => {
    const w = document.createTreeWalker(pg, NodeFilter.SHOW_TEXT); let t;
    while ((t = w.nextNode())) {
      const s = t.textContent.trim(); if (!s) continue;
      const el = t.parentElement;
      if (el.closest('.banda,.pie,.datos,.rotulo,.topbar,svg,.cuenta,.ej-n,.ej-emo,.e,.m2l-c,.m2l-d,.m2l-u')) continue;
      const k = sel(el); if (!k) continue;
      const cs = getComputedStyle(el), z = el.currentCSSZoom || 1;
      const px = parseFloat(cs.fontSize) * z;
      const o = out[k] || (out[k] = {min: 99, zoom: z, num: true, n: 0});
      o.min = Math.min(o.min, px); o.zoom = z; o.n++;
      if (!NUM.test(s)) o.num = false;
    }
  });
  return {sel: out};
})()"""


def fijo(src, ruta):
    if 'id="mates2-fijo"' not in src:
        if 'family=Nunito' not in src:
            src = src.replace('</title>', '</title>\n' + LINK, 1)
        src = src.replace('</head>', CSS + '\n</head>', 1)
    if '/numeros/' in ruta and 'ordinales' not in ruta and 'class="m2l-' not in src:
        cuerpo_i = src.index('<body')
        cab, cuerpo = src[:cuerpo_i], src[cuerpo_i:]
        cuerpo = re.sub(r'>(\s*\d*\s*)([CDU])(\s*)<',
                        lambda m: f'>{m.group(1)}<b class="m2l-{m.group(2).lower()}">{m.group(2)}</b>{m.group(3)}<', cuerpo)
        src = cab + cuerpo
    src = re.sub(r'<div class="fin pw">\s*⭐\s*¡Buen trabajo!\s*</div>', FIN_MB, src)
    return src


def medir(rutas):
    os.makedirs('/tmp/negritas', exist_ok=True)
    open('/tmp/negritas/eval.js', 'w').write(JS)
    lista = [os.path.relpath(os.path.abspath(r), RAIZ) for r in rutas]
    open('/tmp/negritas/l_m2.txt', 'w').write('\n'.join(lista))
    subprocess.run(['node', '/tmp/negritas/cdp.mjs', RAIZ, '/tmp/negritas/l_m2.txt'], check=True)
    return {os.path.abspath(os.path.join(RAIZ, x['f'])): x['sel'] for x in json.load(open('/tmp/negritas/res.json'))}


def auto_css(sels):
    reglas = []
    for k, o in sorted(sels.items()):
        partes = []
        if o['num']:   # Nunito a igual tamaño se ve más pequeña que la ligada → +15 %
            partes.append(f"font-size:{round(max(15, o['min'] * 1.15) / o['zoom'], 1)}px!important")
        elif o['min'] < 14.9:
            partes.append(f"font-size:{round(15 / o['zoom'], 1)}px!important")
        if o['num']:
            partes.append("font-family:'Nunito',sans-serif!important;font-weight:700!important;font-variation-settings:normal!important")
        if partes:
            reglas.append(f".pagina {k}{{{';'.join(partes)}}}")
    return '<style id="mates2-auto">\n' + '\n'.join(reglas) + '\n</style>'


if __name__ == '__main__':
    args = sys.argv[1:]
    hacer_medida = '--medir' in args
    rutas = [a for a in args if not a.startswith('--')]
    for f in rutas:
        s = open(f, encoding='utf-8').read(); n = fijo(s, f)
        if n != s:
            with open(f, 'w', encoding='utf-8') as w: w.write(n)
    if hacer_medida:
        for f in rutas:   # se mide SIN el bloque automático anterior
            s = open(f, encoding='utf-8').read()
            n = re.sub(r'<style id="mates2-auto">.*?</style>\n?', '', s, flags=re.S)
            if n != s:
                with open(f, 'w', encoding='utf-8') as w: w.write(n)
        m = medir(rutas)
        for f in rutas:
            s = open(f, encoding='utf-8').read()
            css = auto_css(m.get(os.path.abspath(f), {}))
            s = s.replace('</head>', css + '\n</head>', 1)
            with open(f, 'w', encoding='utf-8') as w: w.write(s)
        print('medidas', len(m))
