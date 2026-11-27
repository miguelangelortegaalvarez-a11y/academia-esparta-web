"""Cuentas de 1º con un mismo formato de número (Miguel, 27-nov-2026): NUNITO, mismo tamaño, una casilla por cifra."""
import re
FUENTE = '<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@500;600&amp;display=swap" rel="stylesheet" />'
NUM = "500 28px 'Nunito',sans-serif"
CSS = f"""<style id="cuentas-iguales">
.mz .columnas-grid,.mz .columnas-grid-4{{display:grid;justify-items:center;align-items:start;gap:10px 6px}}
.mz .columnas-grid{{grid-template-columns:repeat(6,1fr)}}
.mz .pagina-sumas,.mz .pagina-ops{{row-gap:18px!important;align-items:start}}.mz .columnas-grid-4{{grid-template-columns:repeat(4,1fr)}}
.mz .cuenta,.xm-op{{border-collapse:collapse;font:{NUM};margin:0 auto}}
.mz .cuenta td,.xm-op td{{width:24px;height:35px;text-align:center;padding:0;vertical-align:middle}}
.mz .cuenta tr.sig td,.xm-op tr:nth-child(2) td{{border-bottom:2.5px solid #1a1a1a}}
.mz .cuenta tr.cab td{{font:600 14px 'Nunito',sans-serif;color:var(--gris);height:20px}}
.mz .cuenta tr.ok td,.xm-op tr.ok td{{color:#2e8b57;font-weight:600}}
.mz .cuenta .xm-d,.xm-op .xm-d{{display:inline-block;width:23px;height:32px;border:1.5px solid var(--bosque);border-radius:6px;margin-top:3px}}
.mz .horiz-fila,.mz .horiz-fila span,.mz .ej-horiz-mini{{font:{NUM}!important}}
.mz .horiz-fila{{gap:10px!important;align-items:center}}
.mz .horiz-fila .caja{{width:52px!important;height:44px!important;border-radius:8px}}
.mz .serie-num,.mz .xm-c{{font:{NUM}!important}}
.mz .recuerda-ejemplos{{align-items:start}}
.mz .unir-suma,.mz .unir-resultado,.mz .descomp-fila,.mz .descomp-num,.mz .doble-fila,.mz .doble-num,.mz .enc-fila{{font:{NUM}!important}}
.mz .unir-suma,.mz .unir-resultado{{padding:2px 0!important;border-width:1.5px!important;border-radius:8px!important}}
.mz .descomp-num,.mz .doble-num{{height:42px!important;border-width:1.5px!important;border-radius:8px!important}}
.mz .enc-fila .caja,.mz .descomp-fila .caja,.mz .doble-fila .caja{{height:42px!important;border-radius:8px!important}}
.ej-blq > .xm .xm-op{{zoom:var(--zoom-mz,1.12)}}
.ej-blq > .ej{{zoom:1.12}}
.xm:has(.xm-op){{display:grid;grid-template-columns:auto 1fr;align-items:end;column-gap:18px}}
.xm:has(.xm-op) > .xm-mira-t{{grid-column:1/-1}}
.xm:has(.xm-op) > .xm-fila{{display:flex;flex-wrap:wrap;gap:6px 4px;align-items:flex-start}}
.xm:has(.xm-op) > .xm-fila:not(.xm-mira) + .xm-fila{{grid-column:1/-1}}
.mz .recuerda{{padding-top:6px;padding-bottom:6px}}
</style>"""
def _td(x, n): return ''.join(f'<td>{c}</td>' for c in x.rjust(n)).replace('<td> </td>', '<td></td>')
def tabla(nums, sig, cab=None, res=None):
    n = max(len(x) for x in nums + ([res] if res else []))
    h = '<table class="cuenta">'
    if cab: h += f'<tr class="cab"><td></td>{_td(cab, n)}</tr>'
    h += ''.join(f'<tr><td></td>{_td(x, n)}</tr>' for x in nums[:-1])
    h += f'<tr class="sig"><td>{sig}</td>{_td(nums[-1], n)}</tr>'
    h += (f'<tr class="ok"><td></td>{_td(res, n)}</tr>' if res else '<tr><td></td>' + '<td><span class="xm-d"></span></td>' * n + '</tr>') + '</table>'
    return h
def _col(m):
    b = m.group(0)
    filas = [x.replace(' ', '') for x in re.findall(r'<div>\s*([\d ]+)\s*</div>', b)]
    sig, ult = re.search(r'<span[^>]*>([+−-])</span><span>([\d ]+)</span>', b).groups()
    return tabla(filas + [ult.replace(' ', '')], sig)
def _mini(m):
    b = m.group(0)
    cab = re.search(r'<div class="cab">([^<]+)</div>', b)
    filas = [x.replace(' ', '') for x in re.findall(r'<div>\s*([\d ]+)\s*</div>', b)]
    sig, ult = re.search(r'<span[^>]*>([+−-])</span><span>([\d ]+)</span>', b).groups()
    res = re.search(r'<div class="barra">\s*([\d ]+)\s*</div>', b).group(1).replace(' ', '')
    return tabla(filas + [ult.replace(' ', '')], sig, cab.group(1).replace(' ', '') if cab else None, res)
def aplicar(s):
    if 'id="cuentas-iguales"' in s: return s
    s = re.sub(r'<div class="(?:suma-col|op-col)[^"]*">(?:<div>[\d ]+</div>)+<div class="lin"><span class="sg">.</span><span>[\d ]+</span></div><div class="barra">&nbsp;</div></div>', _col, s)
    s = re.sub(r'<div class="ej-col-mini">.*?<div class="barra">[^<]*</div>\s*</div>', _mini, s, flags=re.S)
    s = s.replace('</head>', FUENTE + '\n' + CSS + '\n</head>', 1)
    return s
