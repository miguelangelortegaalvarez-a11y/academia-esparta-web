#!/usr/bin/env python3
"""(28-nov-2026) Material de base 10 de 2º en 3D y en color, como en 1º (bloques.py):
centena = placa roja (10×10), decena = barra azul (10 cubos), unidad = cubito verde.
Sustituye los dibujos planos de línea (placa 30×30 con trama p100, barra 7×30 con p10,
cuadradito 8×8) que hay en la leyenda y en «Cuenta el material». Idempotente.
Uso: python3 bloques2.py ficha.html …
"""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from bloques import COL

L = 5                       # lado de un cubito (px)
DX = DY = 3                 # profundidad 3D


def _cubo(px, py, k, w='.6'):
    f, t, l, s = COL[k]
    return (f'<polygon points="{px},{py+DY} {px+DX},{py} {px+DX+L},{py} {px+L},{py+DY}" fill="{t}" stroke="{s}" stroke-width="{w}"/>'
            f'<polygon points="{px+L},{py+DY} {px+L+DX},{py} {px+L+DX},{py+L} {px+L},{py+L+DY}" fill="{l}" stroke="{s}" stroke-width="{w}"/>'
            f'<rect x="{px}" y="{py+DY}" width="{L}" height="{L}" fill="{f}" stroke="{s}" stroke-width="{w}"/>')


def _svg(cuerpo, w, h, etiqueta):
    return (f'<svg class="b10" viewBox="-1 -1 {w+2} {h+2}" width="{w+2}" height="{h+2}" role="img" '
            f'aria-label="{etiqueta}">{cuerpo}</svg>')


def unidad():
    return _svg(_cubo(0, 0, 'u'), L + DX, L + DY, '1 unidad')


def decena():
    return _svg(''.join(_cubo(0, j * L, 'd') for j in range(9, -1, -1)), L + DX, 10 * L + DY, '1 decena')


def centena():
    f, t, l, s = COL['c']; S = 10 * L
    o = [f'<polygon points="0,{DY} {DX},0 {DX+S},0 {S},{DY}" fill="{t}" stroke="{s}" stroke-width=".7"/>',
         f'<polygon points="{S},{DY} {S+DX},0 {S+DX},{S} {S},{S+DY}" fill="{l}" stroke="{s}" stroke-width=".7"/>',
         f'<rect x="0" y="{DY}" width="{S}" height="{S}" fill="{f}" stroke="{s}" stroke-width=".8"/>']
    for k in range(1, 10):   # cuadrícula de la placa
        o.append(f'<line x1="{k*L}" y1="{DY}" x2="{k*L}" y2="{DY+S}" stroke="{s}" stroke-width=".45"/>')
        o.append(f'<line x1="0" y1="{DY+k*L}" x2="{S}" y2="{DY+k*L}" stroke="{s}" stroke-width=".45"/>')
    return _svg(''.join(o), S + DX, S + DY, '1 centena')


PLACA = re.compile(r'<svg width="30" height="30"><rect[^>]*fill="url\(#p100\)"[^>]*/></svg>')
BARRA = re.compile(r'<svg width="7" height="30"><rect[^>]*fill="url\(#p10\)"[^>]*/></svg>')
CUBO = re.compile(r'<svg width="8" height="8"><rect[^>]*fill="none"[^>]*/></svg>')
CSS = ('<style id="bloques2">.mz .mat-grupo{gap:5px!important;align-items:flex-end}'
       '.mz .material-fila{align-items:center!important}.mz .leyenda{align-items:center!important}.mz .ley-item{display:flex;align-items:center;gap:6px}</style>')


def aplicar(src):
    n = PLACA.sub(centena(), src)
    n = BARRA.sub(decena(), n)
    n = CUBO.sub(unidad(), n)
    if n != src and 'id="bloques2"' not in n:
        n = n.replace('</head>', CSS + '\n</head>', 1)
    return n


if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = open(f, encoding='utf-8').read(); n = aplicar(s)
        if n != s:
            with open(f, 'w', encoding='utf-8') as w: w.write(n)
            print('ok', f)
