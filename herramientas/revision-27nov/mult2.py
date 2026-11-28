#!/usr/bin/env python3
"""(28-nov-2026) Multiplicación de 2º al aspecto «vivo» de las cuentas.

- Carga Nunito de verdad (link de Google Fonts): antes se pedía 'Nunito' sin
  cargarla y salía Helvetica.
- Números de las multiplicaciones en Nunito grande; el × en rojo.
- Casillas de respuesta teñidas de azul; resultado final en verde.
- Tablas con título de color.
- Puntitos negros de grupos y rejillas → emoji del ejercicio; los grupos pasan
  a «recipientes» (cuenco de color).
El contenido (números, enunciados) no cambia. Idempotente.
Uso: python3 mult2.py ficha.html …
"""
import re, sys

LINK = ('<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@500;600;700;800'
        '&amp;display=swap" rel="stylesheet" />')

CSS = """<style id="mult-viva">
:root{--mr:#d64541;--ma:#2f6fd6;--maf:#eaf1fd;--mv:#2e8b57;--mvf:#e8f6ee;--mo:#e39b2d;--mof:#fff6e6}
.mz .reng,.mz .resp-fila,.mz .rec-op,.xm-n,.mz .reng *,.mz .resp-fila *,.mz .rec-op *,.xm-n *{font-family:'Nunito',sans-serif!important;font-variation-settings:normal!important}
.mz .reng,.mz .resp-fila,.mz .rec-op,.xm-n{font-weight:700!important}
.mz .reng{font-size:21px!important;gap:10px!important}
.mz .reng .op{min-width:92px!important}
.mz .resp-fila,.mz .resp-fila .lead,.mz .resp-fila .sep{font-size:21px!important}
.mz .resp-fila .lead.frase{font-size:17px!important;font-weight:600!important}
.mz .resp-fila .sep{color:#1a1a1a}
.mz .calc-grid.una-col,.mz .dos-col.una-col{grid-template-columns:1fr!important}
.mz .rejillas-fila .resp-fila{flex-wrap:nowrap!important;gap:8px!important}
.mz .rejillas-fila .resp-fila,.mz .rejillas-fila .resp-fila .sep{font-size:18px!important}
.mz .serie{gap:6px!important}
.mz .serie .et{flex-basis:100%;font:800 15px 'Nunito',sans-serif!important;font-variation-settings:normal!important;min-width:0!important}
.mz .cas{width:38px!important;height:32px!important;font:700 18px 'Nunito',sans-serif!important;font-variation-settings:normal!important;border-color:var(--ma)!important;background:var(--maf)}
.mz .cas.dada{background:#fff!important;border-color:var(--mv)!important;color:var(--mv)}
.mz .serie .fl{font-size:14px!important;color:#999}
.mz .rec-op{font-size:20px!important}
.xm-n{font-size:22px!important}
.xm-par{margin-right:6px!important;gap:8px!important}
.xm-fila{gap:12px 14px!important;flex-wrap:nowrap!important}
.xm-c:not(.ok){width:50px!important}
.mx,.mz .rec-op .x{color:var(--mr)!important;font-weight:800!important}
.mz .caja{height:30px!important;width:46px!important;border:1.6px solid var(--ma)!important;background:var(--maf);border-radius:7px!important;vertical-align:middle}
.mz .caja.res{width:54px!important;border-color:var(--mv)!important;background:var(--mvf)}
.xm-c:not(.ok){border-color:var(--ma)!important;background:var(--maf)}
.xm-c.ok{font:700 24px 'Nunito',sans-serif!important;color:var(--mv)!important}
.mz .tabla-mult.una-col{grid-template-columns:auto!important}
.mz .tabla-mult{border:2px solid var(--mo)!important;background:#fffdf8;padding:8px 18px 10px!important;gap:7px!important}
.mz .tabla-mult .titulo{font:800 17px 'Nunito',sans-serif!important;font-variation-settings:normal!important;color:#fff;background:var(--mo);border:0!important;border-radius:7px;padding:3px 0!important;margin-bottom:4px!important}
.mz .tablas-fila{gap:44px!important;flex-wrap:nowrap!important}
.mz .grupo,.mz .grupo-vacio{border:2px solid var(--mo)!important;background:var(--mof);border-radius:6px 6px 20px 20px!important}
.mz .grupo-vacio{border-style:dashed!important}
.mz .rejilla{border:2px solid var(--mo)!important;background:var(--mof)}
.v-emo{font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;font-size:19px;line-height:1;display:inline-block;width:22px;text-align:center;font-variation-settings:normal}
.mz .rejillas-fila:has(> .rejilla + .resp-fila),.mz .rejillas-fila:has(> .rejilla + div > .resp-fila){display:grid!important;grid-template-columns:auto auto;justify-content:start;align-items:center;gap:14px 18px!important}
.mz .rejillas-fila > .rejilla{justify-self:start}
.mz .rejillas-fila .caja{width:42px!important}
.mz .rejillas-fila .caja.res{width:50px!important}
.mz .rejilla .v-emo{font-size:16px;width:19px}
</style>"""

MALOS = {'✖️', '✖', '⭐', '🚀', '➕'}   # no sirven como «cosas que se cuentan»


def x_rojo(m):
    return m.group(1) + m.group(2).replace('×', '<span class="mx">×</span>') + m.group(3)


def aplicar(src):
    if 'id="mult-viva"' in src:
        return src
    if 'family=Nunito' not in src:
        src = src.replace('</title>', '</title>\n' + LINK, 1)
    src = src.replace('</head>', CSS + '\n</head>', 1)
    # × en rojo dentro de los números (no en enunciados ni pistas)
    src = re.sub(r'(<span class="(?:op|lead|sep)"[^>]*>)([^<]*)(</span>)', x_rojo, src)
    src = re.sub(r'(<b class="xm-n">)([^<]*)(</b>)', x_rojo, src)
    src = re.sub(r'(<div class="resp-fila ejemplo">.*?<b>)([^<]*)(</b>)', x_rojo, src)
    # rejillas de cuentas con dos casillas por fila → una sola columna
    partes = re.split(r'(<div class="(?:calc-grid|dos-col)">)', src)
    for i in range(1, len(partes), 2):
        tramo = re.split(r'<div class="ej|<footer', partes[i + 1])[0]
        if any(f.count('<div class="caja') >= 2 for f in tramo.split('<div class="resp-fila')):
            partes[i] = partes[i].replace('">', ' una-col">')
    src = ''.join(partes)
    # frases largas en .lead → más pequeñas
    src = re.sub(r'<span class="lead"([^>]*)>([^<]*[a-záéíóúñ¿?]{3}[^<]*)</span>',
                 r'<span class="lead frase"\1>\2</span>', src)
    # dos tablas en la misma fila → cada una en una columna, del 1 al 10
    if src.count('class="tabla-mult"') == 2:
        def ordena(m):
            r = re.findall(r'<div class="reng">.*?<div class="caja"></div></div>', m.group(0), re.S)
            r.sort(key=lambda x: int(re.search(r'(\d+)\s*=', re.sub('<[^>]+>', '', x)).group(1)))
            return '\n        '.join(r) + '\n'
        src = re.sub(r'(?:<div class="reng">.*?<div class="caja"></div></div>\s*)+', ordena, src, flags=re.S)
        src = src.replace('class="tabla-mult"', 'class="tabla-mult una-col"')
    # puntitos → emoji del ejercicio (Recuerda: manzana)
    trozos = re.split(r'(<div class="ej-blq">)', src)
    emo = '🍎'
    out = []
    for t in trozos:
        m = re.search(r'<span class="ej-emo">([^<]+)</span>', t)
        e = emo if 'recuerda' in t and not m else (m.group(1) if m else emo)
        if e in MALOS:
            e = '🍎'
        out.append(t.replace('<div class="v-punto"></div>', f'<span class="v-emo">{e}</span>'))
    src = ''.join(out)
    # los emojis ya no son puntos: solo las frases que DESCRIBEN el dibujo
    src = src.replace('Los puntos en ', 'Las cosas en ')
    src = src.replace('cuántos puntos hay en cada grupo', 'cuántas cosas hay en cada grupo')
    return src


if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = open(f, encoding='utf-8').read()
        n = aplicar(s)
        if n != s:
            with open(f, 'w', encoding='utf-8') as w:
                w.write(n)
            print('ok', f)
