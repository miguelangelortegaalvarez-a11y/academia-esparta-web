#!/usr/bin/env python3
"""Fichas de 1º más alegres (28-nov-2026): solo emojis, el contenido no se toca.

- Un emoji delante de cada enunciado, según el tema del bloque.
- En los problemas, el emoji de lo que se cuenta (bombones 🍬, patos 🦆…).
- En las lecturas finales, un dibujo junto al texto (como el burro de comprensión).
- «⭐ ¡Muy bien! 🏆» al final, donde ya había «⭐ ¡Buen trabajo!» (no se añade: pisaría el pie).

Solo actúa en fichas con 2 emojis o menos (las sosas). Idempotente.
Uso: python3 alegres.py ficha.html [...]
"""
import re, sys

EMO = re.compile('[\U0001F300-\U0001FAFF☀-➿⭐]')

TEMAS = [  # (trozo de la ruta, emojis por orden de ejercicio)
    ('monedas', ['🪙', '💶', '🐷', '🛒', '🍦', '🎁']),
    ('dias-semana', ['📅', '🌞', '🎒', '🌙', '🎉', '🛝']),
    ('meses', ['📅', '🎂', '🌸', '☀️', '🍂', '❄️']),
    ('reloj', ['⏰', '🌞', '🥪', '🛁', '🌙', '🛏️']),
    ('longitud-peso', ['📏', '⚖️', '🥛', '🐘', '🐜', '🦒']),
    ('geometria', ['🔷', '🔺', '🟢', '🎁', '⚽', '🧊']),
    ('comparar', ['🐊', '🦒', '🐭', '🐘', '⚖️', '🏁']),
    ('ordinales', ['🏁', '🥇', '🚂', '🏆', '🎈', '🐢']),
    ('decenas', ['🧱', '📦', '🍎', '🚀', '🎈', '🐠']),
    ('numeros', ['🔢', '🐞', '🎈', '🍎', '🚀', '🐠']),
    ('lengua', ['📖', '✏️', '🦉', '🌈', '🐝', '⭐']),
]
DEFECTO = ['🍎', '🚀', '🐠', '🎈', '🦁', '🍓']

COSAS = [  # palabra del problema → emoji (la primera que aparezca)
    ('céntimo', '🪙'), ('bombon', '🍬'), ('caramelo', '🍬'), ('chuche', '🍭'), ('tomate', '🍅'), ('cromo', '🃏'),
    ('galleta', '🍪'), ('donut', '🍩'), ('manzana', '🍎'), ('plátano', '🍌'), ('flor', '🌸'),
    ('pez', '🐟'), ('peces', '🐟'), ('pato', '🦆'), ('gallina', '🐔'), ('oveja', '🐑'), ('pájaro', '🐦'),
    ('globo', '🎈'), ('pegatina', '⭐'), ('moneda', '🪙'), ('céntimo', '🪙'), ('lápi', '✏️'),
    ('pelota', '⚽'), ('libro', '📚'), ('cuento', '📖'), ('coche', '🚗'), ('autobús', '🚌'),
    ('hoja', '🍃'), ('niño', '🧒'),
]

LECTURAS = {'1': '🐱', '2': '🐶', '3': '👦', '4': '🐄', '5': '🌳',
            '6': '👨‍🍳', '7': '🚆', '8': '📚', '9': '🧺', '10': '🎵'}

CSS = """<style id="fichas-alegres">
.ej-emo,.pb-emo{font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;font-size:.8em;font-variation-settings:normal;font-style:normal}
.pb-emo{margin-right:8px;font-size:1.25em!important;vertical-align:-3px}
.fin.vv-fin{font-size:26px!important;display:flex;justify-content:center;align-items:center;gap:18px;margin-top:18px!important}
.fin.vv-fin .e{font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;font-size:34px}
.cuento.con-emo{display:flex;gap:14px;align-items:flex-start}
.cuento.con-emo .emo-b{font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;font-size:46px;width:58px;margin-top:8px;text-align:center;flex-shrink:0;line-height:1}
</style>"""

FIN = '<div class="fin pw vv-fin"><span class="e">⭐</span><span>¡Muy bien!</span><span class="e">🏆</span></div>'


def emojis_cuerpo(src):
    b = src.split('<body', 1)[1]
    b = re.sub(r'<div class="topbar">.*?</div>', '', b, flags=re.S).replace('💡', '')
    return len(EMO.findall(re.sub(r'<[^>]+>', ' ', b)))


def aplicar(src, ruta, forzar=False):
    if 'id="fichas-alegres"' in src or 'id="cuentas-vivas"' in src:
        return src
    if emojis_cuerpo(src) > 2 and not forzar:
        return src
    src = src.replace('</head>', CSS + '\n</head>', 1)
    lista = next((l for k, l in TEMAS if k in ruta), DEFECTO)
    n = [0]
    def emo(m):
        e = lista[n[0] % len(lista)]; n[0] += 1
        return m.group(0) + f'<span class="ej-emo">{e}</span>'
    src = re.sub(r'<span class="ej-n">\d+</span>', emo, src)
    # problemas
    def pb(m):
        t = m.group(2).lower()
        e = next((e for k, e in COSAS if k in t), '🤔')
        return m.group(1) + f'<span class="pb-emo">{e}</span>' + m.group(2)
    src = re.sub(r'(<span class="pb-t">)(.*?</span>)', pb, src, flags=re.S)
    # lecturas finales
    m = re.search(r'lectura-frase/(\d+)\.html$', ruta)
    if m and m.group(1) in LECTURAS:
        src = src.replace('<div class="cuento pw lect"><div>',
                          f'<div class="cuento pw lect con-emo"><span class="emo-b">{LECTURAS[m.group(1)]}</span><div>', 1)
    # final
    # (solo donde ya había final: añadirlo donde no lo hay pisa el pie)
    src = re.sub(r'<div class="fin[^"]*">⭐ ¡Buen trabajo!</div>', FIN, src)
    return src


if __name__ == '__main__':
    forzar = '--forzar' in sys.argv  # también en fichas que ya tienen dibujos (monedas)
    for f in [a for a in sys.argv[1:] if a != '--forzar']:
        s = open(f, encoding='utf-8').read()
        nuevo = aplicar(s, f, forzar)
        if nuevo != s:
            open(f, 'w', encoding='utf-8').write(nuevo)
            print('ok', f)
        else:
            print('=', f)
