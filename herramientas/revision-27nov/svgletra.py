#!/usr/bin/env python3
"""(28-nov-2026) Letra legible DENTRO de los dibujos (SVG) de Mates 1º-2º.

1. Agranda los dibujos pequeños que llevan números que el niño tiene que leer:
   relojes (.reloj, .reloj-mini) y balanzas (viewBox 0 0 240 150).
2. Mide con Chrome la letra de cada <svg> con <text> y multiplica sus font-size para que lo más
   pequeño llegue a MIN px (tope ×1.35). No se tocan: monedas/billetes (las ★ son adorno),
   emojis (ya son grandes) ni los dibujos donde la letra ya es legible.
Idempotente: guarda el tamaño original en data-fs0 y recalcula desde él.
Uso: python3 svgletra.py ficha.html …   (rutas desde la raíz del repo)
"""
import json, os, re, subprocess, sys

MIN = 14.0
TOPE = 1.35   # más, y los números del reloj se amontonan / los nombres de la balanza se montan
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'recursos', 'primaria')
CSS = ('<style id="svgletra">.mz svg.reloj{width:104px!important;height:104px!important}'
       '.mz svg.reloj-mini{width:92px!important;height:92px!important}'
       '.mz svg[viewBox="0 0 543 96"]{overflow:visible}.mz .regla-fila > svg{flex:1 1 0;min-width:0}'
       '.mz .tarde-celda svg.reloj-mini{width:76px!important;height:76px!important}</style>')
SALTAR = re.compile(r'class="(?:[^"]*\b)?(?:moneda|billete|mini-moneda|mini-billete|xm-mon|xm-bill)')

JS = r"""(() => { const out=[];
  document.querySelectorAll('.pagina svg').forEach(s => {
    const ts=[...s.querySelectorAll('text')]; if(!ts.length) return;
    const px=ts.map(t=>t.getBoundingClientRect().height).filter(h=>h>0);
    out.push(px.length ? Math.min(...px) : 0); });
  return {min: out}; })()"""


def css(src):
    src = re.sub(r'<style id="svgletra">.*?</style>\n?', '', src, flags=re.S)
    src = src.replace('</head>', CSS + '\n</head>', 1)
    return src


def svgs_con_texto(cuerpo):
    return [m for m in re.finditer(r'<svg\b[^>]*>.*?</svg>', cuerpo, re.S) if '<text' in m.group(0)]


def escalar(svg, f):
    def fs(m):
        orig = m.group(3) or m.group(2)
        nuevo = round(float(orig) * f, 1)
        return f'{m.group(1)}font-size="{nuevo:g}" data-fs0="{orig}"'
    return re.sub(r'(\s)font-size="([\d.]+)"(?: data-fs0="([\d.]+)")?', fs, svg)


def medir(rutas):
    open('/tmp/negritas/eval.js', 'w').write(JS)
    open('/tmp/negritas/l_svg.txt', 'w').write('\n'.join(os.path.relpath(os.path.abspath(r), RAIZ) for r in rutas))
    subprocess.run(['node', '/tmp/negritas/cdp.mjs', RAIZ, '/tmp/negritas/l_svg.txt'], check=True)
    return {os.path.abspath(os.path.join(RAIZ, x['f'])): x['min'] for x in json.load(open('/tmp/negritas/res.json'))}


if __name__ == '__main__':
    rutas = sys.argv[1:]
    for f in rutas:                                   # 1) tamaños + volver al font-size original
        s = open(f, encoding='utf-8').read()
        s = re.sub(r'font-size="[\d.]+" data-fs0="([\d.]+)"', r'font-size="\1"', css(s))
        open(f, 'w', encoding='utf-8').write(s)
    m = medir(rutas)                                  # 2) medir con el tamaño nuevo
    for f in rutas:
        s = open(f, encoding='utf-8').read(); i = s.index('<body')
        cab, cuerpo = s[:i], s[i:]
        mins = m.get(os.path.abspath(f), [])
        piezas, pos, cambios = [], 0, 0
        for k, sv in enumerate(svgs_con_texto(cuerpo)):
            t = sv.group(0); px = mins[k] if k < len(mins) else 0
            if 0 < px < MIN - .5 and not SALTAR.search(t[:200]):
                t = escalar(t, min(TOPE, MIN / px)); cambios += 1
            piezas.append(cuerpo[pos:sv.start()] + t); pos = sv.end()
        cuerpo = ''.join(piezas) + cuerpo[pos:]
        open(f, 'w', encoding='utf-8').write(cab + cuerpo)
        if cambios: print(f.split('primaria/')[-1], cambios, 'dibujos')
