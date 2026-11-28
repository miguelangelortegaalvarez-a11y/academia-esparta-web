#!/usr/bin/env python3
"""(28-nov-2026) Líneas sueltas de las fichas de líneas (1º-2º) en COLOR y más gruesas.
Cada dibujo (<svg>) toma un color que ROTA. NO se rellena nada (fill="none" se queda): rellenar las
cerradas daría la respuesta de «abierta o cerrada». Los puntos negros (vértices / puntos de unir) se
quedan oscuros. Los trazos finos de ayuda (≤1.2) no se engordan.
Uso: python3 lineas_color.py ficha.html …
"""
import re, sys
COL = ['#d64541', '#2f6fd6', '#2e8b57', '#d4881c', '#7e22ce', '#c2410c']


def aplicar(src):
    i = src.index('<body'); cab, cuerpo = src[:i], src[i:]; n = [0]
    def svg(m):
        d = m.group(2)
        if 'stroke="#000"' not in d and 'stroke="#1a1a1a"' not in d: return m.group(0)
        c = COL[n[0] % len(COL)]; n[0] += 1
        def gros(t):
            w = float(t.group(1)); return f'stroke-width="{w * 1.5 if w > 1.2 else w:g}"'
        d = re.sub(r'stroke="(?:#000|#1a1a1a)"', f'stroke="{c}"', d)
        d = re.sub(r'stroke-width="([\d.]+)"', gros, d)
        d = re.sub(r'(<(?:line|path|polyline|polygon)\b(?![^>]*stroke-linecap))', r'\1 stroke-linecap="round"', d)
        return m.group(1) + d + m.group(3)
    cuerpo = re.sub(r'(<svg\b[^>]*>)(.*?)(</svg>)', svg, cuerpo, flags=re.S)
    return cab + cuerpo


if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = open(f, encoding='utf-8').read(); n = aplicar(s)
        if n != s: open(f, 'w', encoding='utf-8').write(n); print('ok', f.split('primaria/')[-1])
