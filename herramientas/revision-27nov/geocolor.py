#!/usr/bin/env python3
"""(28-nov-2026) Figuras de geometría en color (antes línea negra sin relleno).
Los colores ROTAN figura a figura y NO dependen del tipo: si cada tipo tuviera su color,
el color daría la respuesta («Rodea los pentágonos» = rodea los morados; «Une figura y nombre»
por el color del Recuerda). Paleta: rojo, verde, azul, amarillo, morado, naranja, rosa.
Los puntos de los vértices (círculos pequeños rellenos de negro) no se tocan.
Solo cambia figuras con fill="none" stroke="#000"; las líneas abiertas no se rellenan.
Uso: python3 geocolor.py ficha.html …
"""
import re, sys

C = {  # relleno, borde
    'tri': ('#f7a39b', '#c0392b'), 'cua': ('#b4e2ad', '#3d8a37'), 'cir': ('#a9cdf5', '#2f6fb5'),
    'rec': ('#fde68a', '#b7791f'), 'pen': ('#d8b4fe', '#7e22ce'), 'hex': ('#fdba74', '#c2410c'),
    'otr': ('#f9a8d4', '#9d174d'),
}
NEG = re.compile(r'fill="none"(\s+)stroke="#000"')


ORDEN = ['tri', 'cua', 'cir', 'rec', 'pen', 'hex', 'otr']
_n = [0]


def _pinta(tag, clave):
    f, s = C[ORDEN[_n[0] % len(ORDEN)]]; _n[0] += 1
    t = NEG.sub(lambda m: f'fill="{f}"{m.group(1)}stroke="{s}"', tag, count=1)
    return t.replace('<polygon ', '<polygon class="geo" ', 1).replace('<rect ', '<rect class="geo" ', 1).replace('<circle ', '<circle class="geo" ', 1)


def _cara(cx, cy, t):
    """Carita (ojos + sonrisa) centrada en (cx, cy); t = tamaño de referencia."""
    e, r, p = t * .2, t * .1, t * .05
    return (f'<g class="cara" pointer-events="none">'
            f'<circle cx="{cx-e:.1f}" cy="{cy-e*.4:.1f}" r="{r:.1f}" fill="#fff" stroke="#333" stroke-width=".6"/>'
            f'<circle cx="{cx+e:.1f}" cy="{cy-e*.4:.1f}" r="{r:.1f}" fill="#fff" stroke="#333" stroke-width=".6"/>'
            f'<circle cx="{cx-e+p*.3:.1f}" cy="{cy-e*.35:.1f}" r="{p:.1f}" fill="#222"/>'
            f'<circle cx="{cx+e+p*.3:.1f}" cy="{cy-e*.35:.1f}" r="{p:.1f}" fill="#222"/>'
            f'<path d="M{cx-e*.8:.1f},{cy+e*.55:.1f} Q{cx:.1f},{cy+e*1.35:.1f} {cx+e*.8:.1f},{cy+e*.55:.1f}" '
            f'fill="none" stroke="#333" stroke-width="1.6" stroke-linecap="round"/></g>')


def _centro(tag):
    if tag.startswith('<polygon'):
        pts = [tuple(map(float, q.split(','))) for q in re.search(r'points="([^"]+)"', tag).group(1).split()]
        xs, ys = [a for a, _ in pts], [b for _, b in pts]
        cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
        if len(pts) == 3: cy = (max(ys) * 2 + min(ys)) / 3   # triángulo: la cara, abajo, donde hay sitio
        return cx, cy, min(max(xs) - min(xs), max(ys) - min(ys))
    if tag.startswith('<rect'):
        g = lambda k: float(re.search(rf'\b{k}="([\d.]+)"', tag).group(1))
        return g('x') + g('width') / 2, g('y') + g('height') / 2, min(g('width'), g('height'))
    g = lambda k: float(re.search(rf'\b{k}="([\d.]+)"', tag).group(1))
    return g('cx'), g('cy'), 2 * g('r')


def _poligono(m):
    tag = m.group(0)
    pts = re.search(r'points="([^"]+)"', tag).group(1).split()
    n = len(pts)
    if n == 3: return _pinta(tag, 'tri')
    if n == 5: return _pinta(tag, 'pen')
    if n == 6: return _pinta(tag, 'hex')
    if n == 4:
        xs = sorted({round(float(p.split(',')[0])) for p in pts}); ys = sorted({round(float(p.split(',')[1])) for p in pts})
        if len(xs) == 2 and len(ys) == 2:   # rectángulo alineado
            return _pinta(tag, 'cua' if abs((xs[1]-xs[0]) - (ys[1]-ys[0])) < 2 else 'rec')
    return _pinta(tag, 'otr')


def _rect(m):
    tag = m.group(0)
    w = float(re.search(r'width="([\d.]+)"', tag).group(1)); h = float(re.search(r'height="([\d.]+)"', tag).group(1))
    return _pinta(tag, 'cua' if abs(w - h) < 1.5 else 'rec')


def _circulo(m):
    tag = m.group(0)
    r = float(re.search(r'\br="([\d.]+)"', tag).group(1))
    return _pinta(tag, 'cir') if r >= 8 else tag


CARAS = '--caras' in sys.argv


def _figura(m):
    tag = m.group(0)
    if tag.startswith('<polygon'): t = _poligono(m)
    elif tag.startswith('<rect'): t = _rect(m)
    else: t = _circulo(m)
    if CARAS and 'class="geo"' in t:
        cx, cy, tam = _centro(tag)
        if tam >= 18: t += _cara(cx, cy, tam)
    return t


CSS = ('<style id="geocolor">.mz svg:has(.geo){zoom:1.4;overflow:visible}'
       '.geo{stroke-width:3px;stroke-linejoin:round;filter:drop-shadow(1.5px 2px 0 rgba(0,0,0,.16))}</style>')


def aplicar(src):
    _n[0] = 0
    i = src.index('<body'); cab, cuerpo = src[:i], src[i:]
    # figuras con el color en la etiqueta <svg> (fill="#fff" stroke="#1a1a1a") → pasarlo a la figura
    cuerpo = re.sub(r'(<svg class="xm-fig"[^>]*?) fill="#fff" stroke="#1a1a1a"([^>]*>)(<(?:polygon|rect|circle))',
                    r'\1\2\3 fill="none" stroke="#000"', cuerpo)
    # en orden de aparición, para que figuras seguidas tengan colores distintos
    cuerpo = re.sub(r'<(?:polygon|rect|circle) [^>]*fill="none"\s+stroke="#000"[^>]*>', _figura, cuerpo)
    # dibujos compuestos (casa, robot, mosaico: > 3 figuras en un mismo dibujo) → sin caritas
    cuerpo = re.sub(r'<svg\b.*?</svg>', lambda m: re.sub(r'<g class="cara".*?</g>', '', m.group(0), flags=re.S)
                    if m.group(0).count('class="geo"') > 3 else m.group(0), cuerpo, flags=re.S)
    if 'class="geo"' in cuerpo and 'id="geocolor"' not in cab:
        cab = cab.replace('</head>', CSS + '\n</head>', 1)
    return cab + cuerpo


if __name__ == '__main__':
    for f in [a for a in sys.argv[1:] if not a.startswith('--')]:
        s = open(f, encoding='utf-8').read(); n = aplicar(s)
        if n != s:
            with open(f, 'w', encoding='utf-8') as w: w.write(n)
            print('ok', f)
