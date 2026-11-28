#!/usr/bin/env python3
"""Longitud, peso y capacidad de 1º (28-nov-2026): que se vean los objetos.

- Emoji grande en cada objeto (cajas de pareja, de ordenar y de unir).
- Las «líneas» hechas con ▬▬▬ pasan a barras dibujadas (mismo largo relativo).
- Arreglos de contenido (OK de Miguel): «BOTELLA VACÍA» regalaba la respuesta
  (se unía con «VACÍA») → «BOTELLA SIN AGUA»; «DEDAL» (no lo conocen) → «VASO».

Reloj en punto (mismo script, por la ruta): relojes para dibujar de 64 a 84 px (los de «Une», 78 → 62 para que quepa)
y las parejas de «Rodea el reloj más tarde» juntas en su recuadro con a) b).

Idempotente. Uso: python3 medida.py <ruta>/ficha-N.html …
"""
import re, sys

EMOJI = {
    'BICICLETA': '🚲', 'CAMIÓN': '🚚', 'COCHE': '🚗', 'ELEFANTE': '🐘', 'PERRO': '🐕',
    'RATÓN': '🐭', 'BAÑERA': '🛁', 'CUBO': '🪣', 'CUCHARA': '🥄', 'HORMIGA': '🐜',
    'LIBRO': '📕', 'PISCINA': '🏊', 'PLUMA': '🪶', 'TAZA': '☕', 'VASO': '🥛',
    'CASA': '🏠', 'EDIFICIO': '🏢', 'JIRAFA': '🦒', 'NIÑO': '🧒', 'PERSONA': '🧍',
    'SILLA': '🪑', 'BOTELLA': '🍾', 'BOTELLA SIN AGUA': '🍾', 'HOJA': '🍃',
    'MARIPOSA': '🦋', 'MELÓN': '🍈', 'OLLA': '🍲', 'PIANO': '🎹', 'GARRAFA': '🫙',
    'VACA': '🐄', 'SERPIENTE': '🐍',
}

CSS = """<style id="medida-dibujos">
.ob-emo{font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;font-size:34px;line-height:1;font-weight:400}
.pareja-caja.con-emo{gap:12px;min-height:52px!important}
.orden-nombre .ob-emo{font-size:24px;vertical-align:-4px;margin-right:6px}
.unir-tabla{grid-template-columns:225px 1fr 130px!important}
.unir-izq.con-emo{display:flex;align-items:center;gap:8px;white-space:nowrap;padding:6px 10px!important;width:max-content;min-width:100%}
.unir-izq.con-emo .ob-emo{font-size:26px}
.barra{display:inline-block;height:9px;border-radius:5px;background:var(--bosque)}
</style>"""


CSS_RELOJ = """<style id="reloj-grande">
.reloj-mini{width:84px!important;height:84px!important}
.reloj{width:62px!important;height:62px!important}
.ej-block{counter-reset:par}
.ej-block .pareja-fila{display:flex!important;justify-content:center;align-items:center;gap:56px;width:62%;margin:0 auto 8px!important;border:1.5px solid var(--borde,#cfc7b8);border-radius:12px;padding:3px 14px;position:relative}
.ej-block .pareja-fila .reloj-mini{width:64px!important;height:64px!important}
.ej-block .pareja-fila::before{counter-increment:par;content:counter(par,lower-alpha) ")";position:absolute;left:-30px;font-size:20px}
</style>"""


def aplicar_reloj(src):
    """Reloj en punto: relojes para dibujar más grandes y parejas juntas en su recuadro."""
    if 'id="reloj-grande"' in src:
        return src
    return src.replace('</head>', CSS_RELOJ + '\n</head>', 1)


def barra(n):
    return f'<span class="barra" style="width:{n * 22}px"></span>'


def aplicar(src):
    if 'id="medida-dibujos"' in src:
        return src
    src = src.replace('</head>', CSS + '\n</head>', 1)
    # contenido
    src = src.replace('<div class="unir-izq">BOTELLA VACÍA<', '<div class="unir-izq">BOTELLA SIN AGUA<')
    src = src.replace('<div class="pareja-caja">DEDAL<', '<div class="pareja-caja">VASO<')
    # emojis en los objetos
    def caja(m):
        clase, palabra = m.group(1), m.group(2)
        e = EMOJI.get(palabra)
        if not e:
            return m.group(0)
        emo = f'<span class="ob-emo">{e}</span>'
        if clase == 'orden-nombre':
            return f'<div class="orden-nombre">{emo}{palabra}<'
        return f'<div class="{clase} con-emo">{emo}<span>{palabra}</span><'
    src = re.sub(r'<div class="(pareja-caja|orden-nombre|unir-izq)">([A-ZÁÉÍÓÚÑ ]+)<', caja, src)
    # barras
    src = re.sub(r'<span class="long-linea">(▬+)</span>', lambda m: barra(len(m.group(1))), src)
    src = re.sub(r'<div class="orden-linea">(▬+)</div>', lambda m: barra(len(m.group(1))), src)
    return src


if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = open(f, encoding='utf-8').read()
        n = aplicar_reloj(s) if 'el-reloj' in f else aplicar(s)
        if n != s:
            open(f, 'w', encoding='utf-8').write(n)
            print('ok', f)
        else:
            print('=', f)
