#!/usr/bin/env python3
"""Cuentas «vivas» (28-nov-2026): mismo contenido, más alegres.

- D y U en color encima de las cuentas de dos cifras (D roja, U azul).
- Casillas del resultado teñidas del color de su columna.
- Números más grandes y separados; cuentas de una cifra en filas de 3.
- Un emoji delante de cada enunciado y «⭐ ¡Muy bien! 🏆» al final.

No cambia ningún número. Idempotente (si ya está aplicado, no repite).
Uso: python3 vivas.py ficha-1.html [ficha-2.html …]
"""
import re, sys

EMOJIS = ['🍎', '🚀', '🐠', '🎈', '🦁', '🍓', '🐢', '🌈', '🐝', '⚽']

CSS = """<style id="cuentas-vivas">
:root{--cd:#d64541;--cu:#2f6fd6;--cdf:#fdecec;--cuf:#eaf1fd}
.mz .columnas-grid{grid-template-columns:repeat(3,1fr)!important;row-gap:26px!important}
.mz .columnas-grid .cuenta{font-size:32px!important}.mz .columnas-grid .cuenta td{height:38px!important}
.ej-blq+.ej-blq{margin-top:20px!important}
.mz .columnas-grid-4{grid-template-columns:repeat(3,1fr)!important;row-gap:30px!important}
.mz .pagina-sumas,.mz .pagina-ops{grid-template-columns:repeat(3,1fr)!important;row-gap:8px!important}
.mz .pagina-sumas .cuenta,.mz .pagina-ops .cuenta{font-size:40px!important}
.mz .pagina-sumas .cuenta td,.mz .pagina-ops .cuenta td{width:42px!important;height:48px!important}
.mz .cuenta,.vv.xm-op{font:600 36px 'Nunito',sans-serif!important}
.mz .cuenta td,.vv.xm-op td{width:36px!important;height:44px!important}
.vv tr.cab td{font:800 17px 'Nunito',sans-serif!important;height:24px!important;border:0!important}
.vv .d{color:var(--cd)!important}.vv .u{color:var(--cu)!important}
.vv.xm-op tr:nth-child(2) td{border-bottom:0!important}
.vv tr.sig td{border-bottom:3px solid #1a1a1a!important}
.mz .cuenta .xm-d,.vv.xm-op .xm-d{width:32px!important;height:40px!important;margin-top:6px!important;border-radius:8px!important;border:1.5px solid var(--cu)!important;background:var(--cuf)}
.vv .xm-d.xd{border-color:var(--cd)!important;background:var(--cdf)}
.mz .horiz-fila,.mz .horiz-fila span{font-size:31px!important}
.mz .horiz-fila .caja{width:58px!important;height:46px!important;border-color:var(--cu)!important;background:var(--cuf)}
.mz .horiz-grid{row-gap:14px!important}
.ej-emo{font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;font-size:.8em;font-variation-settings:normal}
.mz .ej{gap:6px!important;letter-spacing:-.2px}
.fin.vv-fin{font-size:26px!important;display:flex;justify-content:center;align-items:center;gap:18px;margin-top:18px!important}
.fin.vv-fin .e{font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;font-size:34px}
.xm-fila{gap:12px 34px!important}
</style>"""


def tabla(m):
    t = m.group(0)
    if 'vv' in t.split('>', 1)[0]:
        return t
    t = t.replace('class="cuenta"', 'class="cuenta vv"', 1).replace('class="xm-op"', 'class="xm-op vv"', 1)
    filas = re.findall(r'<tr[^>]*>.*?</tr>', t, re.S)
    ncol = len(re.findall(r'<td', filas[-1]))
    dos = ncol == 3
    # cabecera D/U
    if dos:
        if 'class="cab"' in t:
            t = t.replace('<tr class="cab"><td></td><td>D</td><td>U</td></tr>',
                          '<tr class="cab"><td></td><td class="d">D</td><td class="u">U</td></tr>')
        else:
            t = re.sub(r'(<table[^>]*>)', r'\1<tr class="cab"><td></td><td class="d">D</td><td class="u">U</td></tr>', t, 1)
    # fila del signo (la que empieza por + o −) → clase sig
    t = re.sub(r'<tr>(<td>[+−\-]</td>)', r'<tr class="sig">\1', t)
    # casillas: la primera de una fila de 2 casillas es la D
    def fila(fm):
        f = fm.group(0)
        if f.count('class="xm-d"') == 2:
            f = f.replace('class="xm-d"', 'class="xm-d xd"', 1)
        return f
    t = re.sub(r'<tr[^>]*>.*?</tr>', fila, t, flags=re.S)
    return t


TABLAS = r'((?:\s*<table class="(?:cuenta|xm-op)">.*?</table>)+)'
# Menos cuentas (Miguel, 28-nov): cuántas se quedan en cada tipo de bloque
RECORTE = [
    (r'(<div class="columnas-grid">)', 3),      # una cifra: 6 → 3
    (r'(<div class="columnas-grid-4">)', 3),    # dos cifras: 4 → 3
    (r'(<div class="pagina-sumas">)', 9),       # hoja entera: 20 → 9 (3×3)
    (r'(<div class="pagina-ops">)', 9),
    (r'(<div class="xm-fila">)', 3),            # «Mira cómo se hace» + práctica: 4 → 3
]


def recortar(src):
    # práctica del «Mira cómo se hace»: si hay varias filas, solo la primera
    fila = r'<div class="xm-fila">(?:\s*<table class="xm-op">.*?</table>)+\s*</div>'
    src = re.sub(r'(' + fila + r')(?:\s*' + fila + r')+', r'\1', src, flags=re.S)
    for cab, n in RECORTE:
        def corta(m):
            tablas = re.findall(r'\s*<table class="(?:cuenta|xm-op)">.*?</table>', m.group(2), re.S)
            return m.group(1) + ''.join(tablas[:n])
        src = re.sub(cab + TABLAS, corta, src, flags=re.S)
    # horizontales: 6 → 4
    def horiz(m):
        filas = re.findall(r'\s*<div class="horiz-fila">.*?<div class="caja"></div></div>', m.group(2), re.S)
        return m.group(1) + ''.join(filas[:4])
    src = re.sub(r'(<div class="horiz-grid">)((?:\s*<div class="horiz-fila">.*?<div class="caja"></div></div>)+)', horiz, src, flags=re.S)
    return src


def aplicar(src):
    if 'id="cuentas-vivas"' in src:
        return src
    src = recortar(src)
    src = src.replace('</head>', CSS + '\n</head>', 1)
    src = re.sub(r'(<div class="ej-enunciado">)', r'\1<span class="ej-emo">✏️</span> ', src)
    src = re.sub(r'<table class="(?:cuenta|xm-op)">.*?</table>', tabla, src, flags=re.S)
    n = [0]
    def emo(m):
        e = EMOJIS[n[0] % len(EMOJIS)]; n[0] += 1
        return m.group(0) + f'<span class="ej-emo">{e}</span>'
    src = re.sub(r'<span class="ej-n">\d+</span>', emo, src)
    src = re.sub(r'<div class="fin([^"]*)">⭐ ¡Buen trabajo!</div>',
                 r'<div class="fin\1 vv-fin"><span class="e">⭐</span><span>¡Muy bien!</span><span class="e">🏆</span></div>', src)
    return src


if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = open(f, encoding='utf-8').read()
        nuevo = aplicar(s)
        if nuevo != s:
            open(f, 'w', encoding='utf-8').write(nuevo)
            print('ok', f)
        else:
            print('=', f)
