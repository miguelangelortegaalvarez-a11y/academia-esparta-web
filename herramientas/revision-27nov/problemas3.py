#!/usr/bin/env python3
"""Problemas en 3 columnas (28-nov-2026, idea de Miguel).

Antes: «Datos», «Operación» (cuadrícula de 9,6 × 2,4 cm) y «Solución» uno debajo de
otro; la operación es una suma de una línea y sobraba mucho hueco.
Ahora: Datos | Operación | Solución en columnas, título arriba y espacio para
escribir debajo (renglones en Datos y Solución; en Operación una cuenta en blanco con D/U, casillas,
círculo para el signo y resultado — la cuadrícula quedaba fea, Miguel 28-nov; dos en «dos pasos»).
«Rodea el signo» se queda como estaba. Cada problema queda en su bloque; después se pasa reparte.py para llenar páginas.
Idempotente. Uso: python3 problemas3.py ficha.html …
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alegres import COSAS

CSS = """<style id="problemas-3col">
:root{--cd:#d64541;--cu:#2f6fd6;--cdf:#fdecec;--cuf:#eaf1fd}
.pb-3col{display:grid;grid-template-columns:1fr auto 1fr;gap:26px;margin:4px 0 0 68px;align-items:start}
.pb-col{display:flex;flex-direction:column;gap:2px;min-width:0}
.pb-col .pb-l{width:auto!important}
.pb-renglones{height:3.2cm;background-image:repeating-linear-gradient(transparent 0 calc(1.1cm - 1.5px),#b9b09f calc(1.1cm - 1.5px) 1.1cm)}
.pb-ops{display:flex;gap:18px}
.pbc{border-collapse:collapse}
.pbc td{width:40px;height:40px;text-align:center;padding:0}
.pbc tr.cab td{font:800 16px 'Nunito',sans-serif;height:20px}
.pbc .cc{color:#2e8b57}.pbc .d{color:var(--cd)}.pbc .u{color:var(--cu)}
.pbc .c{display:inline-block;width:34px;height:36px;border:1.5px solid #cfc7b8;border-radius:6px;vertical-align:middle}
.pbc .c.s{border-radius:50%;width:30px;height:30px}
.pbc tr.sig td{border-bottom:2.5px solid #1a1a1a;padding-bottom:4px}
.pbc tr.res td{padding-top:5px}
.pbc .c.xc{border-color:#2e8b57;background:#e8f5ec}.pbc .c.xd{border-color:var(--cd);background:var(--cdf)}.pbc .c.xu{border-color:var(--cu);background:var(--cuf)}
.pb-ico.pb-dib{font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;font-size:44px;line-height:1;width:56px;text-align:center;flex-shrink:0}
.pb{padding-bottom:8px!important;padding-top:14px!important}
.pb-cab{margin-bottom:4px!important}
.ej-blq:has(.pbs)+.ej-blq:has(.pbs){margin-top:8px!important}
.fin.vv-fin{font-size:26px!important;display:flex;justify-content:center;align-items:center;gap:18px;margin-top:18px!important}
.fin.vv-fin .e{font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif;font-size:34px}
</style>"""

TRIO = (r'<div class="pb-fila"><span class="pb-l">Datos:</span><svg class="pb-pauta".*?</svg></div>'
        r'<div class="pb-fila pb-op"><span class="pb-l">Operación:</span><div class="pb-cuad"></div></div>'
        r'<div class="pb-fila"><span class="pb-l">Solución:</span><svg class="pb-pauta".*?</svg></div>')

# cuenta en blanco: D/U arriba, casillas para los dos números, círculo para el signo, raya y resultado
def cuenta(cdu, filas=2):
    """Cuenta en blanco: cabecera (D U o C D U), una fila de casillas por número (2, o 3 con tres sumandos), círculo del signo, raya y resultado.
    En 2º lleva centenas: hay números de 3 cifras y sumas que pasan de 100 (88 + 57)."""
    cols = ['c', 'd', 'u'] if cdu else ['d', 'u']
    cab = ''.join(f'<td class="{"cc" if k == "c" else k}">{k.upper()}</td>' for k in cols)
    fila = ''.join('<td><span class="c"></span></td>' for _ in cols)
    res = ''.join(f'<td><span class="c x{k}"></span></td>' for k in cols)
    return ('<table class="pbc"><tr class="cab"><td></td>' + cab + '</tr>'
            + ('<tr><td></td>' + fila + '</tr>') * (filas - 1) +
            '<tr class="sig"><td><span class="c s"></span></td>' + fila + '</tr>'
            '<tr class="res"><td></td>' + res + '</tr></table>')


def nuevo(n_ops, cdu=False, filas=2):
    col = lambda t, dentro: f'<div class="pb-col"><span class="pb-l">{t}</span>{dentro}</div>'
    return ('<div class="pb-3col">' + col('Datos:', '<div class="pb-renglones"></div>')
            + col('Operación:', '<div class="pb-ops">' + cuenta(cdu, filas) * n_ops + '</div>')
            + col('Solución:', '<div class="pb-renglones"></div>') + '</div>')


def separar(src):
    """Cada problema en su propio bloque (ej-blq), para que reparte.py pueda llenar páginas."""
    def uno(m):
        trozos = m.group(1).split('<div class="pb">')[1:]
        return ''.join('<div class="ej-blq"><div class="pbs"><div class="pb">' + t + '</div></div>' for t in trozos)
    return re.sub(r'<div class="ej-blq"><div class="pbs">(.*?)</div></div>(?=<footer|<div class="ej-blq">|<div class="fin)', uno, src, flags=re.S)


def dibujos(src):
    """Todos los problemas con dibujo a la izquierda (como los que ya lo tenían)."""
    def cab(m):
        c = m.group(0)
        if 'pb-ico' in c:
            return c
        em = re.search(r'<span class="pb-emo">([^<]*)</span>', c)
        if em:
            e = em.group(1); c = c.replace(em.group(0), '', 1)
        else:
            t = re.sub(r'<[^>]+>', '', c).lower()
            e = next((e for k, e in COSAS if k in t), None)
            if not e:
                return c
        return c.replace('<div class="pb-cab">', f'<div class="pb-cab"><span class="pb-ico pb-dib">{e}</span>', 1)
    return re.sub(r'<div class="pb-cab">.*?</span></div>', cab, src, flags=re.S)


def aplicar(src, ruta=''):
    if 'id="problemas-3col"' in src:
        return src
    # problemas de dos pasos: dos cuentas en blanco
    dos = 'dos-operaciones' in ruta
    cdu = ruta.startswith('2/') or '/2/' in ruta
    def trio(m):
        # números del enunciado de ESTE problema: con tres sumandos, la cuenta lleva tres filas
        t = src[src.rfind('<span class="pb-t">', 0, m.start()):m.start()]
        nums = re.findall(r'<strong>\d+</strong>', t)
        filas = 3 if (len(nums) == 3 and not dos) else 2
        return nuevo(2 if dos else 1, cdu, filas)
    n = re.sub(TRIO, trio, src, flags=re.S)
    if n == src:
        return src
    n = separar(n)
    n = dibujos(n)
    n = re.sub(r'<div class="fin([^"]*)">⭐ ¡Buen trabajo!</div>',
               r'<div class="fin\1 vv-fin"><span class="e">⭐</span><span>¡Muy bien!</span><span class="e">🏆</span></div>', n)
    return n.replace('</head>', CSS + '\n</head>', 1)


if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = open(f, encoding='utf-8').read()
        n = aplicar(s, f)
        if n != s:
            open(f, 'w', encoding='utf-8').write(n); print('ok', f)
        else:
            print('=', f)
