#!/usr/bin/env python3
"""Cuentas «vivas» de 2º (28-nov-2026): sumas/restas con llevada y mezcladas.

Las cuentas de 2º van en bloques <div class="op"> (círculo de la llevada, filas
de cifras y barra). Se pasan al formato de 1º (vivas.py): tabla con D roja / U
azul encima, números Nunito grandes, casillas del resultado teñidas, y el círculo
de la llevada encima de la D. Menos cuentas: 16 → 9 (3 por fila). Emoji en el
enunciado y «⭐ ¡Muy bien! 🏆». Los números no cambian. Idempotente.
Uso: python3 vivas2.py ficha.html …
"""
import re, sys

EMOJIS = ['🍎', '🚀', '🐠', '🎈', '🦁', '🍓']

CSS = """<style id="cuentas-vivas2">
:root{--cd:#d64541;--cu:#2f6fd6;--cdf:#fdecec;--cuf:#eaf1fd}
.sumas-grid{grid-template-columns:repeat(3,1fr)!important;row-gap:56px!important}
.sumas-grid:has(.lleva){row-gap:16px!important}
.cuenta.vv{border-collapse:collapse;font:500 40px 'Nunito',sans-serif;margin:0 auto}
.cuenta.vv td{width:42px;height:48px;text-align:center;padding:0;vertical-align:middle}
.cuenta.vv tr.cab td{font:800 18px 'Nunito',sans-serif;height:24px}
.cuenta.vv tr.lleva td{height:34px}
.cuenta.vv .circulo{display:inline-block;width:26px;height:26px;border:1.5px solid var(--cd);border-radius:50%;background:#fff}
.cuenta.vv .d{color:var(--cd)}.cuenta.vv .u{color:var(--cu)}
.cuenta.vv tr.sig td{border-bottom:3px solid #1a1a1a}
.cuenta.vv .xm-d{display:inline-block;width:34px;height:42px;margin-top:6px;border-radius:8px;border:1.5px solid var(--cu);background:var(--cuf)}
.cuenta.vv .xm-d.xd{border-color:var(--cd);background:var(--cdf)}
.ej-emo{font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;font-size:.8em;font-variation-settings:normal}
.fin.vv-fin{font-size:26px!important;display:flex;justify-content:center;align-items:center;gap:18px;margin-top:18px!important}
.fin.vv-fin .e{font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;font-size:34px}
</style>"""

OP = r'<div class="op">(.*?<div class="barra"></div></div>)</div>'


def tabla(o):
    filas = re.findall(r'<div class="fila">(.*?)</div>', o, re.S)
    a = re.findall(r'<span>(\d)</span>', filas[0])
    b = re.findall(r'<span>(\d)</span>', filas[1])
    sig = re.search(r'class="signo">([^<]*)<', filas[1]).group(1)
    lleva = '<tr class="lleva"><td></td><td><span class="circulo"></span></td><td></td></tr>' if 'circ-fila' in o else ''
    return ('<table class="cuenta vv">' + lleva +
            '<tr class="cab"><td></td><td class="d">D</td><td class="u">U</td></tr>'
            f'<tr><td></td><td>{a[0]}</td><td>{a[1]}</td></tr>'
            f'<tr class="sig"><td>{sig}</td><td>{b[0]}</td><td>{b[1]}</td></tr>'
            '<tr><td></td><td><span class="xm-d xd"></span></td><td><span class="xm-d"></span></td></tr></table>')


def aplicar(src):
    if 'id="cuentas-vivas2"' in src:
        return src
    src = src.replace('</head>', CSS + '\n</head>', 1)
    def rejilla(m):
        ops = re.findall(OP, m.group(2), re.S)[:9]
        return m.group(1) + ''.join(tabla(o) for o in ops)
    src = re.sub(r'(<div class="sumas-grid">)((?:<div class="op">.*?<div class="barra"></div></div></div>)+)', rejilla, src, flags=re.S)
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
        n = aplicar(s)
        if n != s:
            open(f, 'w', encoding='utf-8').write(n); print('ok', f)
        else:
            print('=', f)
