#!/usr/bin/env python3
"""(28-nov-2026) Objetos de la vida real (lata, pirámide de Egipto, dado, cucurucho, caja de zapatos,
pelota) con las ilustraciones de Gemini (img-fichas/objetos/*.png) en lugar del dibujo de línea.
Cambia el contenido del <svg viewBox="0 0 60 60"> que va justo antes de <span class="objeto-nombre">.
Uso: python3 objetos_img.py ficha.html …
"""
import re, sys
RUTA = '../../../../../../img-fichas/objetos/'
NOMBRES = {'lata': 'lata', 'pirámide de egipto': 'piramide-egipto', 'dado': 'dado',
           'cucurucho de helado': 'cucurucho', 'caja de zapatos': 'caja-zapatos', 'pelota': 'pelota'}


def aplicar(src):
    def cambia(m):
        nombre = m.group(3).strip().lower()
        img = NOMBRES.get(nombre)
        if not img: return m.group(0)
        return (f'{m.group(1)}<image href="{RUTA}{img}.png" x="-4" y="-4" width="68" height="68" '
                f'preserveAspectRatio="xMidYMid meet"/></svg>{m.group(2)}<span class="objeto-nombre">{m.group(3)}</span>')
    n = re.sub(r'(<svg viewBox="0 0 60 60"[^>]*>).*?</svg>(\s*)<span class="objeto-nombre">([^<]+)</span>', cambia, src, flags=re.S)
    if n != src and 'id="objetos-img"' not in n:
        n = n.replace('</head>', '<style id="objetos-img">.objeto-caja svg{zoom:1.6}.pagina .mz .objeto-nombre{font:700 16px "Nunito",sans-serif!important;font-variation-settings:normal!important;color:#333!important}</style>\n</head>', 1)
    return n


if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = open(f, encoding='utf-8').read(); n = aplicar(s)
        if n != s:
            open(f, 'w', encoding='utf-8').write(n); print('ok', f, n.count('img-fichas/objetos/'))
