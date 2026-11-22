"""Piezas de las fichas 2-5 de Conciencia fonológica (rimas, sílabas, jugar con sílabas, sonidos).

Las palabras se escriben en el JSON separadas en sílabas con guiones («ma-ri-po-sa»): así las sílabas,
la sílaba tónica, la rima y los sonidos se calculan por código y se COMPRUEBAN antes de generar.

Tipos de página (campo «tipo» del JSON):
  silabas    → contar las sílabas de un dibujo (círculos)
  sino       → ¿riman? / ¿empiezan por el mismo sonido?  (SÍ / NO)
  elige      → modelo + 3 dibujos: rodea el que cumple el «criterio» (una sola respuesta buena)
  intruso    → 3 dibujos: tacha el que no cumple el «criterio»
  completa   → frase que acaba en rima: rodea el dibujo que la completa
Criterios: rima · empieza_silaba · termina_silaba · empieza_sonido · termina_sonido · encadena ·
           quitar (modelo + «quito») · juntar (sílabas en orden) · ordenar (sílabas desordenadas) · silabas_n (n)
"""
import html, re

E = html.escape
LET = 'abcdefgh'
_T = str.maketrans('áéíóúü', 'aeiouu')


def pleg(t): return t.lower().translate(_T)
def sil(w): return w.split('-')
def plano(w): return w.replace('-', '')


def tonica(w):
    s = sil(w)
    for i, x in enumerate(s):
        if re.search('[áéíóú]', x): return i
    p = plano(w)
    return len(s) - 2 if len(s) > 1 and p[-1] in 'aeiouns' else len(s) - 1


def rima(w):
    """Desde la vocal tónica hasta el final (ratón → ón, camión → ón, gato → ato)."""
    s = sil(w); x = s[tonica(w)]
    m = re.search('[áéíóú]', x)
    if not m:
        vs = [i for i, c in enumerate(x) if c in 'aeiou']
        i = vs[0]
        if len(vs) > 1 and x[i] in 'iu' and x[i + 1:i + 2] in ('a', 'e', 'o'): i = vs[1]
        k = i
    else:
        k = m.start()
    return pleg(x[k:] + ''.join(s[tonica(w) + 1:]))


def son_ini(w):
    p = pleg(plano(w))
    if p.startswith('h'): p = p[1:]
    for dg, f in (('ch', 'ch'), ('ll', 'y'), ('qu', 'k'), ('rr', 'r')):
        if p.startswith(dg): return f
    c, n = p[0], p[1:2]
    if c == 'c': return 'z' if n in ('e', 'i') else 'k'
    if c == 'g': return 'j' if n in ('e', 'i') else 'g'
    return {'v': 'b'}.get(c, c)


def son_fin(w): return pleg(plano(w))[-1]
def sil_ini(w): return pleg(sil(w)[0])
def sil_fin(w): return pleg(sil(w)[-1])


def cumple(crit, modelo, w):
    """¿La palabra w cumple el criterio respecto al modelo?"""
    if crit == 'rima': return rima(modelo) == rima(w)
    if crit == 'empieza_silaba': return sil_ini(modelo) == sil_ini(w)
    if crit == 'termina_silaba': return sil_fin(modelo) == sil_fin(w)
    if crit == 'empieza_sonido': return son_ini(modelo) == son_ini(w)
    if crit == 'termina_sonido': return son_fin(modelo) == son_fin(w)
    if crit == 'encadena': return sil_fin(modelo) == sil_ini(w)
    raise ValueError(crit)


def correcta(pg, f, w):
    """¿Es w la respuesta buena de la fila f (tipo elige)?"""
    c = pg['criterio']
    if c == 'quitar': return pleg(plano(f['m'][1])) == pleg(f['quito'].replace('-', '') + plano(w))
    if c in ('juntar', 'ordenar'): return pleg(''.join(sorted(f['silabas']))) == pleg(''.join(sorted(sil(w)))) and len(sil(w)) == len(f['silabas']) \
        and (c == 'ordenar' or pleg(''.join(f['silabas'])) == pleg(plano(w)))
    if c == 'silabas_n': return len(sil(w)) == f['n']
    return cumple(c, f['m'][1], w)


# ───────────────────────── papel ─────────────────────────
def it(e, w, cls=''):
    return f'<span class="itd{(" " + cls) if cls else ""}"><span class="itd-e">{e}</span><span class="itd-w pw">{E(plano(w))}</span></span>'


def bolas(n_total, pintadas=0):
    return '<span class="bolas">' + ''.join(f'<span class="bola{" on" if i < pintadas else ""}"></span>' for i in range(n_total)) + '</span>'


EJ = lambda n, t: f'<div class="ej"><span class="ej-n">{n}</span><span>{t}</span></div>'
MIRA = lambda c: f'<div class="mira"><div class="mira-t">Mira cómo se hace:</div>{c}</div><div class="ahora">Ahora tú:</div>'
let = lambda i: f'<span class="let">{LET[i]})</span>'
pista = lambda d: f'<p class="pista">{d["pista"]}</p>' if d.get('pista') else ''


def p_silabas(d, n):
    fila = lambda e, w, pint=0, l='': f'<div class="cf">{l}<span class="emo-b">{e}</span><span class="pw cf-t">{E(plano(w))}</span>{bolas(d["max"], pint)}</div>'
    e, w = d['ejemplo']
    return (EJ(n, d['enunciado']) + MIRA(fila(e, w, len(sil(w)))) + ''.join(fila(e, w, 0, let(i)) for i, (e, w) in enumerate(d['filas'])) + pista(d))


def p_sino(d, n):
    def fila(a, b, marca=None, l=''):
        si = cumple(d['criterio'], a[1], b[1])
        pill = lambda t, ok: f'<span class="op-p{" circ-b" if marca and ok else ""}">{t}</span>'
        return (f'<div class="sn">{l}{it(*a)}<span class="sn-y">y</span>{it(*b)}<span class="sn-p">{pill("SÍ", si)}{pill("NO", not si)}</span></div>')
    a, b = d['ejemplo']
    return EJ(n, d['enunciado']) + MIRA(fila(a, b, True)) + ''.join(fila(a, b, None, let(i)) for i, (a, b) in enumerate(d['filas'])) + pista(d)


def modelo_html(pg, f):
    c = pg['criterio']
    if c in ('juntar', 'ordenar'):
        return '<span class="md-sil">' + ' · '.join(f'<span class="chip">{E(s)}</span>' for s in f['silabas']) + '</span>'
    if c == 'silabas_n':
        return f'<span class="md-n">{bolas(f["n"], f["n"])}</span>'
    if c == 'quitar':
        return f'<span class="md-q">{it(*f["m"])}<span class="md-sin pw">sin <b>{E(f["quito"].replace("-", ""))}</b></span></span>'
    return it(*f['m'], 'md')


def p_elige(d, n):
    def fila(f, marca=False, l=''):
        return (f'<div class="el">{l}<span class="el-m">{modelo_html(d, f)}</span><span class="esc-fl">→</span>'
                + ''.join(it(e, w, 'circ-b' if marca and i == f['buena'] else '') for i, (e, w) in enumerate(f['op'])) + '</div>')
    return EJ(n, d['enunciado']) + MIRA(fila(d['ejemplo'], True)) + ''.join(fila(f, False, let(i)) for i, f in enumerate(d['filas'])) + pista(d)


def intruso_de(pg, trio):
    ws = [w for _, w in trio]
    malos = [i for i in range(3) if not any(cumple(pg['criterio'], ws[i], ws[j]) for j in range(3) if j != i)]
    return malos


def p_intruso(d, n):
    def fila(trio, marca=False, l=''):
        x = intruso_de(d, trio)[0] if marca else None
        return f'<div class="el in">{l}' + ''.join(it(e, w, 'tacha' if i == x else '') for i, (e, w) in enumerate(trio)) + '</div>'
    return EJ(n, d['enunciado']) + MIRA(fila(d['ejemplo'], True)) + ''.join(fila(t, False, let(i)) for i, t in enumerate(d['filas'])) + pista(d)


def p_completa(d, n):
    def fila(f, marca=False, l=''):
        return (f'<div class="cp">{l}<span class="emo-b">{f["e"]}</span><span class="pw cp-t">{E(f["frase"])}</span><span class="cp-op">'
                + ''.join(it(e, w, 'circ-b' if marca and i == f['buena'] else '') for i, (e, w) in enumerate(f['op'])) + '</span></div>')
    return EJ(n, d['enunciado']) + MIRA(fila(d['ejemplo'], True)) + ''.join(fila(f, False, let(i)) for i, f in enumerate(d['filas'])) + pista(d)


PAGINAS = {'silabas': p_silabas, 'sino': p_sino, 'elige': p_elige, 'intruso': p_intruso, 'completa': p_completa}


# ───────────────────────── comprobaciones ─────────────────────────
def alterna(xs):
    return len(xs) >= 4 and all(xs[i] != xs[i + 1] for i in range(len(xs) - 1))


def comprobar(pg):
    t, f = pg['tipo'], []
    if t == 'silabas':
        ns = [len(sil(w)) for _, w in pg['filas']]
        if max(ns) > pg['max']: f.append('silabas: más sílabas que círculos')
        if len(set(ns)) < 3: f.append(f'silabas: poca variedad {ns}')
    if t == 'sino':
        r = []
        for a, b in [pg['ejemplo']] + pg['filas']:
            si = cumple(pg['criterio'], a[1], b[1]); r.append(si)
            if pg['criterio'] == 'empieza_sonido' and si and sil_ini(a[1]) == sil_ini(b[1]):
                f.append(f'sino: «{plano(a[1])}» y «{plano(b[1])}» comparten la sílaba entera (se acierta por la sílaba, no por el sonido)')
        r = r[1:]
        if len(set(r)) == 1: f.append('sino: todas las respuestas son iguales')
        if alterna(r): f.append(f'sino: SÍ y NO alternan, se adivina {r}')
    if t == 'elige':
        bs = []
        for fl in [pg['ejemplo']] + pg['filas']:
            ok = [i for i, (_, w) in enumerate(fl['op']) if correcta(pg, fl, w)]
            nom = plano(fl['m'][1]) if 'm' in fl else '·'.join(fl.get('silabas', [])) or str(fl.get('n'))
            if ok != [fl['buena']]: f.append(f'elige: en «{nom}» las buenas son {ok}, se esperaba [{fl["buena"]}]')
            if pg['criterio'] == 'ordenar' and pleg(''.join(fl['silabas'])) == pleg(plano(fl['op'][fl['buena']][1])):
                f.append(f'elige/ordenar: «{nom}» ya está en orden')
            if pg['criterio'] == 'empieza_sonido':
                for i in ok:
                    if sil_ini(fl['m'][1]) == sil_ini(fl['op'][i][1]): f.append(f'elige: «{nom}» comparte la sílaba entera con la buena')
            if pg['criterio'] == 'termina_silaba':
                for i in ok:
                    pass
            bs.append(fl['buena'])
        if len(set(bs[1:])) == 1: f.append('elige: la buena está siempre en la misma posición')
    if t == 'intruso':
        xs = []
        for trio in [pg['ejemplo']] + pg['filas']:
            m = intruso_de(pg, trio)
            if len(m) != 1: f.append(f'intruso: en {[plano(w) for _, w in trio]} hay {len(m)} intrusos')
            xs.append(m[0] if m else -1)
            if pg['criterio'] == 'empieza_sonido':
                buenos = [w for i, (_, w) in enumerate(trio) if m and i != m[0]]
                if len(buenos) == 2 and sil_ini(buenos[0]) == sil_ini(buenos[1]): f.append(f'intruso: {buenos} comparten la sílaba entera')
        if len(set(xs[1:])) == 1: f.append('intruso: siempre en la misma posición')
    if t == 'completa':
        bs = []
        for fl in [pg['ejemplo']] + pg['filas']:
            ok = [i for i, (_, w) in enumerate(fl['op']) if rima(fl['clave']) == rima(w)]
            if ok != [fl['buena']]: f.append(f'completa: «{fl["frase"]}» buenas {ok}, se esperaba [{fl["buena"]}]')
            bs.append(fl['buena'])
        if len(set(bs[1:])) == 1: f.append('completa: la buena siempre en la misma posición')
    return f
