#!/usr/bin/env python3
"""(28-nov-2026) Cuerpos geométricos dibujados con Gemini (img-fichas/cuerpos/<cuerpo>-<color>.png,
36 imágenes: 6 cuerpos × 6 colores, con carita) en lugar de los dibujos de línea negra.

Se cambia el CONTENIDO de cada <svg viewBox="0 0 60 60"> que sea un cuerpo suelto por un <image>,
así el sitio y el tamaño en la ficha no cambian. El color ROTA (no depende del cuerpo: no da pistas).
NO se tocan:
  · los ejercicios de contar caras / aristas / vértices (las aristas escondidas en discontinua
    hacen falta y la imagen no las tiene);
  · los objetos de la vida real (dado, lata, caja de zapatos, pelota…) ni las escenas grandes.
Uso: python3 cuerpos_img.py ficha.html …
"""
import re, sys, collections

COLORES = ['rojo', 'verde', 'azul', 'amarillo', 'morado', 'naranja']
RUTA = '../../../../../../img-fichas/cuerpos/'
NO_TOCAR = re.compile(r'arista|vértice|vertice|puntitos', re.I)


def tipo(dentro):
    tags = []
    for t in re.finditer(r'<(polygon|rect|circle|ellipse|path|line|polyline)\b([^>]*)>', dentro):
        if 'dasharray' in t.group(2): continue
        if t.group(1) == 'circle' and 'fill="#000"' in t.group(2): tags.append('punto'); continue
        tags.append(t.group(1))
    firma = ' '.join(sorted(tags))
    if firma == 'polygon polygon rect':
        r = re.search(r'<rect\b[^>]*width="([\d.]+)"[^>]*height="([\d.]+)"', dentro)
        return 'cubo' if r and abs(float(r.group(1)) - float(r.group(2))) < 1.5 else 'prisma'
    return {'circle ellipse': 'esfera', 'ellipse line line path': 'cilindro',
            'line line path': 'cono', 'line line line polyline': 'piramide',
            'line line line polyline polyline': 'piramide'}.get(firma)


def aplicar(src):
    i = src.index('<body'); cab, cuerpo = src[:i], src[i:]
    n = [0]
    bloques = re.split(r'(?=<div class="ej-blq">)', cuerpo)
    for k, b in enumerate(bloques):
        if NO_TOCAR.search(re.sub(r'<[^>]+>', ' ', b)): continue
        def cambia(m):
            abre, dentro = m.group(1), m.group(2)
            if 'viewBox="0 0 60 60"' not in abre: return m.group(0)
            t = tipo(dentro)
            if not t: return m.group(0)
            col = COLORES[n[0] % 6]; n[0] += 1
            return (abre.replace('<svg ', '<svg data-cuerpo="1" ', 1) +
                    f'<image href="{RUTA}{t}-{col}.png" x="0" y="0" width="60" height="60" '
                    f'preserveAspectRatio="xMidYMid meet"><title>{t}</title></image></svg>')
        bloques[k] = re.sub(r'(<svg\b[^>]*>)(.*?)</svg>', cambia, b, flags=re.S)
    cuerpo = ''.join(bloques)
    if 'data-cuerpo="1"' in cuerpo and 'id="cuerpos-img"' not in cab:
        cab = cab.replace('</head>', '<style id="cuerpos-img">.mz svg[data-cuerpo]{zoom:1.45;overflow:visible}</style>\n</head>', 1)
    return cab + cuerpo


if __name__ == '__main__':
    tot = collections.Counter()
    for f in sys.argv[1:]:
        s = open(f, encoding='utf-8').read(); n = aplicar(s)
        if n != s:
            with open(f, 'w', encoding='utf-8') as w: w.write(n)
            c = collections.Counter(re.findall(r'<title>(\w+)</title></image>', n)); tot += c
            print('ok', f.split('primaria/')[-1], dict(c))
    print('total', dict(tot))
