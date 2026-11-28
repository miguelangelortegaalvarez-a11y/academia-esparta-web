#!/usr/bin/env python3
"""(28-nov-2026) Escenas de «cuenta cuántos cuerpos hay» (1º f3 muñeco, 2º f3 juguetes) montadas con los
cuerpos de Gemini (img-fichas/cuerpos/). Los MISMOS cuerpos que tenía el dibujo de línea → la respuesta
no cambia. Cada pieza: (cuerpo, color, x centro, y de la base, ancho). Se apilan de abajo arriba.
"""
import re, sys
from PIL import Image
RAIZ_IMG = 'img-fichas/cuerpos/'
RUTA = '../../../../../../img-fichas/cuerpos/'
ESCENAS = {
    '1/matematicas/geometria/cuerpos-geometricos/ficha-3.html': ('0 0 280 210', 200, [
        ('cilindro', 'azul', 95, 200, 62), ('esfera', 'amarillo', 95, None, 52), ('cono', 'rojo', 95, None, 44),
        ('cubo', 'verde', 185, 200, 62), ('esfera', 'morado', 250, 200, 36)]),
    '2/matematicas/geometria/cuerpos-geometricos/ficha-3.html': ('0 0 260 210', 200, [
        ('prisma', 'naranja', 38, 200, 64), ('piramide', 'verde', 38, None, 52),
        ('cubo', 'azul', 128, 200, 50), ('cilindro', 'morado', 128, None, 40), ('esfera', 'amarillo', 128, None, 42), ('cono', 'rojo', 128, None, 34),
        ('cono', 'naranja', 202, 200, 44), ('esfera', 'rojo', 240, 200, 32)]),
}
SOLAPE = {'cilindro': .10, 'esfera': .14, 'cubo': .06, 'prisma': .08, 'piramide': .05, 'cono': .05}


def svg(vb, suelo, piezas):
    o = [f'<line x1="10" y1="{suelo}" x2="{vb.split()[2] and int(vb.split()[2]) - 10}" y2="{suelo}" stroke="#8a8a8a" stroke-width="2"/>']
    tope = {}
    for cu, col, x, base, w in piezas:
        im = Image.open(f'{RAIZ_IMG}{cu}-{col}.png'); h = w * im.height / im.width
        if base is None: base = tope[x]
        y = base - h
        o.append(f'<image href="{RUTA}{cu}-{col}.png" x="{x - w/2:.1f}" y="{y:.1f}" width="{w}" height="{h:.1f}"/>')
        tope[x] = y + h * SOLAPE[cu]
    return ''.join(o)


for rel, (vb, suelo, piezas) in ESCENAS.items():
    f = 'recursos/primaria/' + rel; s = open(f, encoding='utf-8').read()
    pat = re.compile(r'(<svg\b[^>]*viewBox="' + vb + r'"[^>]*>).*?</svg>', re.S)
    n, k = pat.subn(lambda m: m.group(1) + svg(vb, suelo, piezas) + '</svg>', s, count=1)
    assert k == 1, f
    open(f, 'w', encoding='utf-8').write(n); print('ok', rel)
