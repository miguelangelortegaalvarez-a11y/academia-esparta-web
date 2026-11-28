#!/usr/bin/env python3
"""(28-nov-2026) Lengua 2º: misma letra que Mates 2º.

- .mz con zoom 1.12 (como Mates 2º): enunciados 23→26 px.
- Texto de los ejercicios más grande; nada de imprenta diminuta (10-12 px):
  números y letras de «Une» en Nunito (azul / rojo), opciones de «Rodea» y
  ejemplos del Recuerda en la ligada de la ficha.
- Carga Nunito de verdad (link de Google Fonts + font-variation-settings:normal).
Después: reparte.py --unir (el banco de palabras no se separa de sus frases).
Idempotente. Uso: python3 lengua2.py ficha.html …
"""
import re, sys

ZOOM = '--sin-zoom' not in sys.argv   # por defecto, misma letra que Mates (zoom 1.12)
LINK = ('<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@500;600;700;800'
        '&amp;display=swap" rel="stylesheet" />')

CSS = """<style id="lengua2-letra">
.mz .frase-item{font-size:18px!important;line-height:1.9!important}
.mz .match-item{font-size:18px!important;white-space:nowrap}
.mz .match-grid{gap:28px!important}
.mz .match-grid.largo .match-item{font-size:14px!important;gap:8px!important}
.mz .match-grid.largo{gap:16px!important}
.mz .match-grid.envuelve .match-col:last-child .match-item{white-space:normal!important}
.mz .frase-num,.mz .match-num,.mz .match-letter{font:800 16px 'Nunito',sans-serif!important;font-variation-settings:normal!important;color:#2f6fd6}
.mz .match-letter{color:#d64541}
.mz .match-blank{width:32px!important;height:26px!important;border-color:#2f6fd6!important;background:#eaf1fd;border-radius:6px}
.mz .opcion-group{font-family:inherit!important;font-size:17px!important}
.mz .opcion-chip{padding:1px 10px!important;border-radius:8px!important;margin:0 3px!important}
.mz .palabra-chip{font-size:17px!important;background:#fff6e6;border-color:#e39b2d!important}
.mz .recuerda-item .recuerda-def,.mz .recuerda-item .recuerda-tipo,.mz .recuerda-def,.mz .recuerda-tipo{font-size:16px!important;line-height:1.9!important}
.mz .recuerda-item .recuerda-ej,.mz .recuerda-ej{font-family:inherit!important;font-size:15px!important;font-style:normal!important;color:#333!important}
.mz .recuerda-titulo{font:800 13px 'Nunito',sans-serif!important;font-variation-settings:normal!important}
.mz .np{white-space:nowrap}
.xm-fila > .mini-pauta.larga{display:block;width:100%!important;height:74px!important}
.xm-fila:has(> .mini-pauta.larga){display:block!important;padding-right:0!important}
.v-pista{font-family:'Nunito',sans-serif!important;font-variation-settings:normal!important;font-size:14px!important;font-weight:600!important}
</style>"""


def marcar_largos(src):
    """«Une» con frases largas → letra algo menor para que cada frase quepa en una línea.
    Umbral orientativo: signos 2-6 se marcaron por MEDIDA (Chrome), no por longitud."""
    def g(m):
        cols = re.findall(r'<div class="match-col".*?(?=<div class="match-col"|$)', m.group(0), re.S)
        lmax = [max([len(re.sub(r'<[^>]+>|\s+', ' ', it).strip()) for it in re.findall(r'<div class="match-item">(.*?)</div>', c, re.S)] or [0]) for c in cols]
        if sum(lmax) > 70:
            return m.group(0).replace('<div class="match-grid"', '<div class="match-grid largo envuelve"', 1)
        return m.group(0).replace('<div class="match-grid"', '<div class="match-grid largo"', 1) if sum(lmax) > 55 else m.group(0)
    return re.sub(r'<div class="match-grid".*?(?=<div class="ej-blq"|<footer)', g, src, flags=re.S)


def aplicar(src):
    if 'id="lengua2-letra"' in src:   # ya aplicada: solo se actualiza el bloque de estilos
        src = re.sub(r'<style id="lengua2-letra">.*?</style>', lambda m: CSS, src, count=1, flags=re.S)
        return marcar_largos(src)
    if ZOOM: src = src.replace('.mz{zoom:1.0;', '.mz{zoom:1.12;', 1)
    if 'family=Nunito' not in src:
        src = src.replace('</title>', '</title>\n' + LINK, 1)
    # el hueco de escribir no salta solo a otra línea: va con la palabra de antes y el punto
    src = re.sub(r'([^\s<>]+ )(<svg class="mini-pauta pq".*?</svg>)([.,!?]?)',
                 r'<span class="np">\1\2\3</span>', src, flags=re.S)
    # la pauta larga ocupa todo el ancho (antes se quedaba en 170 px y centrada)
    src = src.replace('<svg class="mini-pauta larga" viewBox', '<svg class="mini-pauta larga" preserveAspectRatio="none" viewBox')
    return marcar_largos(src.replace('</head>', CSS + '\n</head>', 1))


if __name__ == '__main__':
    for f in [a for a in sys.argv[1:] if not a.startswith('--')]:
        s = open(f, encoding='utf-8').read()
        n = aplicar(s)
        if n != s:
            with open(f, 'w', encoding='utf-8') as w:
                w.write(n)
            print('ok', f)
