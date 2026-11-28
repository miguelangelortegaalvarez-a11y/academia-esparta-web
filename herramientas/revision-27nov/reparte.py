"""Reparte una ficha en páginas. Los ejercicios no se parten, salvo las REJILLAS de cuentas demasiado grandes,
que se parten por filas completas (el enunciado va con la primera fila)."""
import re, json, subprocess, sys, os
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'recursos', 'primaria')
REJ = r'<div class="(?:pagina-sumas|pagina-ops|columnas-grid|columnas-grid-4|horiz-grid)[^"]*">'
ITEM = r'<table class="cuenta">.*?</table>|<div class="horiz-fila">.*?</div>'
def _cdp(rel, js):
    open('/tmp/negritas/eval_rep.js', 'w').write(js); open('/tmp/negritas/l_rep.txt', 'w').write(rel)
    subprocess.run(['node', '/tmp/negritas/cdp_rep.mjs', RAIZ, '/tmp/negritas/l_rep.txt'], capture_output=True)
    return json.load(open('/tmp/negritas/res_rep.json'))[0]
JS = """(() => { const p=document.querySelector('.pagina'); const pt=p.getBoundingClientRect().top; const pie=p.querySelector('.pie');
  const limite = 1122.52 - (p.getBoundingClientRect().bottom - pie.getBoundingClientRect().top) - 6;
  const ro = p.querySelector('.rotulo'); const ini = ro.getBoundingClientRect().bottom - pt + parseFloat(getComputedStyle(ro).marginBottom);
  const bl=[...document.querySelectorAll('.pagina > .ej-blq, .pagina > .fin')].map(b=>{const cs=getComputedStyle(b);
     const g=b.querySelector('.pagina-sumas,.pagina-ops,.columnas-grid,.columnas-grid-4,.horiz-grid');
     return {h:Math.ceil(b.getBoundingClientRect().height+parseFloat(cs.marginTop)+parseFloat(cs.marginBottom)),
             cols: g ? getComputedStyle(g).gridTemplateColumns.split(' ').length : 0};});
  return {limite, ini, bl}; })()"""
def _medir(s, secs, cab, pie, bloques, ruta):
    tmp = s[:s.find(secs[0])] + cab + ''.join(bloques) + pie + s[s.rfind('</section>') + 10:]
    tmp = tmp.replace('</head>', '<style>.pagina{height:auto!important;min-height:0!important}</style></head>', 1)
    z = ruta.replace('.html', '-medir.html'); open(z, 'w').write(tmp)
    m = _cdp(os.path.relpath(z, RAIZ), JS); os.remove(z); return m
def _trocear(b, cols):
    g = re.search(REJ, b); ini = g.end()
    items = []; pos = ini
    for it in re.finditer(ITEM, b[ini:], re.S):
        if b[pos:ini + it.start()].strip(): break
        items.append(it.group(0)); pos = ini + it.end()
    if len(items) <= cols: return [b]
    pre, suf = b[:ini], b[pos:]
    pre_cont = re.sub(r'<div class="ej">.*?</div>|<div class="ej-enunciado">.*?</div>', '', pre, count=1, flags=re.S)
    filas = [items[i:i + cols] for i in range(0, len(items), cols)]
    return [{'pre': pre if k == 0 else pre_cont, 'items': f, 'suf': suf, 'id': id(b), 'k': k} for k, f in enumerate(filas)]
UNIR = False
def _unir_continuaciones(bloques):
    """--unir: un bloque sin enunciado (p. ej. las frases de un banco de palabras) es la
    continuación del anterior → se mete DENTRO del mismo ej-blq para que nunca se separen."""
    out = []
    for b in bloques:
        es_cont = (b.startswith('<div class="ej-blq">') and 'class="ej"' not in b and 'ej-enunciado' not in b
                   and 'recuerda' not in b and out and out[-1].startswith('<div class="ej-blq">'))
        if es_cont:
            prev = out[-1].rstrip(); cont = b.rstrip()
            interior = cont[len('<div class="ej-blq">'):cont.rfind('</div>')]
            out[-1] = prev[:prev.rfind('</div>')] + interior + '</div>'
        else:
            out.append(b)
    return out
def repartir(rel):
    ruta = os.path.join(RAIZ, rel); s = open(ruta).read()
    secs = re.findall(r'<section class="pagina">.*?</section>', s, re.S)
    cab = re.match(r'(<section class="pagina">.*?<div class="rotulo">.*?</div>)', secs[0], re.S).group(1)
    pie = re.search(r'(<footer class="pie">.*?</footer></section>)', secs[0], re.S).group(1)
    bloques = []
    for sec in secs:
        cuerpo = sec[len(re.match(r'<section class="pagina">.*?<div class="rotulo">.*?</div>', sec, re.S).group(0)):]
        cuerpo = cuerpo[:cuerpo.rfind('<footer class="pie">')]
        bloques += re.findall(r'<div class="ej-blq">.*?(?=<div class="ej-blq">|<div class="fin|$)|<div class="fin[^"]*">.*?</div>', cuerpo, re.S)
    if UNIR: bloques = _unir_continuaciones(bloques)
    m = _medir(s, secs, cab, pie, bloques, ruta); cap = m['limite'] - m['ini'] - 6
    # piezas: bloques enteros o filas de una rejilla grande
    piezas = []
    for b, info in zip(bloques, m['bl']):
        if info['cols'] and info['h'] > cap * 0.45 and re.search(REJ, b): piezas += _trocear(b, info['cols'])
        else: piezas.append(b)
    html = lambda p: p if isinstance(p, str) else p['pre'] + ''.join(p['items']) + p['suf']
    m2 = _medir(s, secs, cab, pie, [html(p) for p in piezas], ruta); hs = [x['h'] for x in m2['bl']]
    # una fila suelta ocupa: su alto medido; al juntarse se ahorra el margen del bloque (~30 px)
    pags = [[]]; y = 0
    for i, (p, h) in enumerate(zip(piezas, hs)):
        cont = not isinstance(p, str) and p['k'] > 0 and pags[-1] and not isinstance(pags[-1][-1], str) and pags[-1][-1]['id'] == p['id']
        h_ef = h - 30 if cont else h
        solo_enun = isinstance(p, str) and 'ej-enunciado' in p and 'ej-blq' in p and not re.search(REJ, p)
        sig_h = hs[i + 1] if solo_enun and i + 1 < len(hs) else 0
        if y + h_ef + sig_h > cap and pags[-1]: pags.append([]); y = 0; h_ef = h
        pags[-1].append(p); y += h_ef
    if len(pags) > 1 and len(pags[-1]) == 1 and isinstance(pags[-1][0], str) and pags[-1][0].startswith('<div class="fin'):
        pags[-2].append(pags[-1][0].replace('<div class="fin', '<div class="fin fin-justo', 1)); pags.pop()
        if 'fin-justo{' not in s: s = s.replace('</head>', '<style>.fin.fin-justo{margin-top:0!important;line-height:1.15}</style>\n</head>', 1)
    # juntar filas seguidas del mismo ejercicio dentro de una página
    def unir(pg):
        out = []
        for p in pg:
            if out and not isinstance(p, str) and not isinstance(out[-1], str) and out[-1]['id'] == p['id']:
                out[-1] = dict(out[-1], items=out[-1]['items'] + p['items'])
            else: out.append(p)
        return [html(p) for p in out]
    T = len(pags)
    nuevas = [cab + ''.join(unir(p)) + re.sub(r'Página \d+ de \d+', f'Página {i+1} de {T}', pie) for i, p in enumerate(pags)]
    open(ruta, 'w').write(s[:s.find(secs[0])] + ''.join(nuevas) + s[s.rfind('</section>') + 10:])
    return len(secs), T
if __name__ == '__main__':
    args = sys.argv[1:]
    if '--unir' in args: UNIR = True; args.remove('--unir')
    for rel in args: print(rel, repartir(rel))
