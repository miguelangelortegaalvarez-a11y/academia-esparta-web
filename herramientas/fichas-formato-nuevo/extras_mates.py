"""Ejercicios NUEVOS para llenar la última página de las fichas de Mates (1º Primaria).

Solo se usan cuando la ficha ya pasa a dos páginas, y solo entra lo que cabe (pieza a pieza).
Cada ejercicio empieza con una fila resuelta de modelo («Mira cómo se hace»): ayuda visual para 1º-2º.
Todo lo que se imprime se comprueba aquí con assert (sumas sin llevadas, restas sin prestar, horas,
conteos…). Si un assert falla, la ficha NO se genera.
"""
import math
import random
from html import escape as E

DIAS = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
         'septiembre', 'octubre', 'noviembre', 'diciembre']
ORD = ['primero', 'segundo', 'tercero', 'cuarto', 'quinto', 'sexto', 'séptimo', 'octavo', 'noveno', 'décimo']


# ───────────────────────── piezas de dibujo ─────────────────────────
def cj(v=None, w=52):
    """Caja de respuesta; con valor = modelo resuelto (en verde)."""
    return f'<span class="xm-c{" ok" if v is not None else ""}" style="width:{w}px">{"" if v is None else E(str(v))}</span>'


def linea(v=None, w=170):
    return f'<span class="xm-l{" ok" if v is not None else ""}" style="width:{w}px">{"" if v is None else E(str(v))}</span>'


def fila(contenido, modelo=False):
    return f'<div class="xm-fila{" xm-mira" if modelo else ""}">{contenido}</div>'


def mira(contenido):
    return f'<div class="xm-mira-t">Mira cómo se hace:</div>{fila(contenido, True)}'


def op_vertical(a, b, signo, res=None):
    """Cuenta en columna (DU ± DU); res = resultado si es el modelo."""
    da, ua = divmod(a, 10); db, ub = divmod(b, 10)
    c = lambda x: f'<td>{x}</td>'
    if res is None:
        fr = '<tr class="r"><td></td><td><span class="xm-d"></span></td><td><span class="xm-d"></span></td></tr>'
    else:
        dr, ur = divmod(res, 10)
        fr = f'<tr class="r ok"><td></td>{c(dr if dr else "")}{c(ur)}</tr>'
    return (f'<table class="xm-op"><tr><td></td>{c(da if da else "")}{c(ua)}</tr>'
            f'<tr><td>{signo}</td>{c(db if db else "")}{c(ub)}</tr>{fr}</table>')


def reloj(h, corta=True):
    """Reloj en punto: larga al 12; corta a la hora h (si corta=False, solo la larga: para dibujarla)."""
    o = ['<svg class="xm-reloj" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="#fff" stroke="#1a1a1a" stroke-width="2.5"/>']
    for k in range(1, 13):
        a = math.radians(k * 30)
        o.append(f'<text x="{50 + 36 * math.sin(a):.1f}" y="{50 - 36 * math.cos(a) + 4.5:.1f}" text-anchor="middle" font-size="12" font-family="sans-serif">{k}</text>')
    o.append('<line x1="50" y1="50" x2="50" y2="18" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="round"/>')
    if corta:
        a = math.radians((h % 12) * 30)
        x, y = 50 + 22 * math.sin(a), 50 - 22 * math.cos(a)
        assert abs(math.hypot(x - 50, y - 50) - 22) < 1e-6
        o.append(f'<line x1="50" y1="50" x2="{x:.1f}" y2="{y:.1f}" stroke="#1a1a1a" stroke-width="4.5" stroke-linecap="round"/>')
    o.append('<circle cx="50" cy="50" r="3" fill="#1a1a1a"/></svg>')
    return ''.join(o)


def moneda(v):
    """Moneda (1 €, 2 €) o billete (5 €, 10 €) sencillos."""
    if v in (5, 10):
        return (f'<svg class="xm-bill" viewBox="0 0 90 50"><rect x="2" y="2" width="86" height="46" rx="5" fill="#fff" stroke="#1a1a1a" stroke-width="2"/>'
                f'<text x="45" y="20" text-anchor="middle" font-size="9" font-family="sans-serif" letter-spacing="2">EURO</text>'
                f'<text x="45" y="40" text-anchor="middle" font-size="18" font-weight="700" font-family="sans-serif">{v}</text></svg>')
    return (f'<svg class="xm-mon" viewBox="0 0 60 60"><circle cx="30" cy="30" r="27" fill="#fff" stroke="#1a1a1a" stroke-width="2"/>'
            f'<circle cx="30" cy="30" r="20" fill="none" stroke="#1a1a1a" stroke-width="1"/>'
            f'<text x="30" y="36" text-anchor="middle" font-size="17" font-weight="700" font-family="sans-serif">{v}€</text></svg>')


def figura(nombre):
    f = {'triángulo': '<polygon points="30,6 56,52 4,52"/>', 'cuadrado': '<rect x="7" y="7" width="46" height="46"/>',
         'rectángulo': '<rect x="2" y="16" width="56" height="30"/>', 'círculo': '<circle cx="30" cy="30" r="25"/>'}[nombre]
    return f'<svg class="xm-fig" viewBox="0 0 60 60" fill="#fff" stroke="#1a1a1a" stroke-width="2.5">{f}</svg>'


LADOS = {'triángulo': 3, 'cuadrado': 4, 'rectángulo': 4, 'círculo': 0}


def dibujo(rotulo):
    return f'<div class="xm-dib"><div class="xm-dib-c"></div><div class="xm-dib-t">{rotulo}</div></div>'


# ───────────────────────── generadores por sub-bloque ─────────────────────────
def sin_llevar(a, b): return (a % 10) + (b % 10) <= 9 and a + b <= 99
def sin_prestar(a, b): return a % 10 >= b % 10 and a >= b


def g_sumas(r, n, ej, signos='+'):
    ops = []
    while len(ops) < 13:
        s = r.choice(signos)
        a, b = r.randint(11, 88), r.randint(10, 78)
        if s == '+' and not sin_llevar(a, b): continue
        if s == '−':
            if a < b: a, b = b, a
            if not sin_prestar(a, b) or a == b: continue
        if (a, b, s) in ops: continue
        ops.append((a, b, s))
    for a, b, s in ops:
        assert (s == '+' and sin_llevar(a, b)) or (s == '−' and sin_prestar(a, b))
    res = lambda a, b, s: a + b if s == '+' else a - b
    a, b, s = ops[0]
    piezas = [mira(op_vertical(a, b, s, res(a, b, s)))]
    resto = ops[1:]
    for k in range(0, len(resto), 4):
        piezas.append(fila(''.join(op_vertical(a, b, s) for a, b, s in resto[k:k+4])))
    t = {'+': 'Resuelve las sumas.', '−': 'Resuelve las restas.'}.get(signos, 'Resuelve. ¡Fíjate bien en el signo!')
    return [(ej(n, t), 'xm', piezas)]


def g_numeros(r, n, ej):
    ns = r.sample(range(12, 98), 7)
    p1 = [mira(cj(ns[0] - 1) + f'<b class="xm-n">{ns[0]}</b>' + cj(ns[0] + 1))]
    p1 += [fila(cj() + f'<b class="xm-n">{x}</b>' + cj()) for x in ns[1:]]
    out = [(ej(n, 'Escribe el número de antes y el de después.'), 'xm xm-2col', p1)]
    series = []
    for _ in range(4):
        ini = r.randint(10, 90)
        series.append(list(range(ini, ini + 6)))
    for s in series: assert all(b - a == 1 for a, b in zip(s, s[1:])) and s[-1] <= 99
    p2 = [mira(''.join(cj(x) for x in series[0]))]
    for s in series[1:]:
        hue = set(r.sample(range(1, 6), 3))
        p2.append(fila(''.join(cj() if i in hue else f'<span class="xm-c dado">{x}</span>' for i, x in enumerate(s))))
    out.append((ej(n + 1, 'Completa la serie.'), 'xm', p2))
    return out


def g_decenas(r, n, ej):
    ns = r.sample(range(11, 99), 9)
    du = lambda x: divmod(x, 10)
    p1 = [mira(f'<b class="xm-n">{ns[0]}</b> = ' + cj(du(ns[0])[0]) + ' D ' + cj(du(ns[0])[1]) + ' U')]
    p1 += [fila(f'<b class="xm-n">{x}</b> = ' + cj() + ' D ' + cj() + ' U') for x in ns[1:5]]
    out = [(ej(n, 'Escribe cuántas decenas (D) y unidades (U) tiene.'), 'xm xm-2col', p1)]
    p2 = [mira(f'{du(ns[5])[0]} D {du(ns[5])[1]} U = ' + cj(ns[5]))]
    p2 += [fila(f'{du(x)[0]} D {du(x)[1]} U = ' + cj()) for x in ns[6:]]
    for x in ns: d, u = du(x); assert 10 * d + u == x
    out.append((ej(n + 1, 'Escribe el número.'), 'xm xm-2col', p2))
    return out


def g_ordinales(r, n, ej):
    emo = ['🚗', '🐟', '🎈', '⭐', '🍎']
    p = []
    for k, e in enumerate(r.sample(emo, 4)):
        pos = r.randint(1, 7)
        celdas = ''.join(f'<span class="xm-emo{" circ" if (k == 0 and i == pos - 1) else ""}">{e}</span>' for i in range(7))
        t = f'<span class="xm-ord">el {ORD[pos-1]}</span>'
        p.append(mira(t + celdas) if k == 0 else fila(t + celdas))
    out = [(ej(n, 'Empieza por la izquierda y rodea el que te dicen.'), 'xm', p)]
    ns = r.sample(range(1, 11), 5)
    p2 = [mira(f'<b class="xm-n">{ns[0]}.º</b> → ' + linea(ORD[ns[0]-1]))]
    p2 += [fila(f'<b class="xm-n">{x}.º</b> → ' + linea()) for x in ns[1:]]
    out.append((ej(n + 1, 'Escribe el nombre.'), 'xm xm-2col', p2))
    return out


def g_comparar(r, n, ej):
    pares = []
    while len(pares) < 9:
        a = r.randint(10, 99); b = a if len(pares) in (3,) else r.randint(10, 99)
        if (a, b) not in pares: pares.append((a, b))
    sig = lambda a, b: '>' if a > b else '<' if a < b else '='
    par = lambda a, b, v=None: f'<span class="xm-par"><b class="xm-n">{a}</b>{cj(v, 44)}<b class="xm-n">{b}</b></span>'
    p = [mira(par(*pares[0], sig(*pares[0])))]
    for k in range(1, 9, 2): p.append(fila(par(*pares[k]) + par(*pares[k+1])))
    out = [(ej(n, 'Escribe &gt;, &lt; o =.'), 'xm', p)]
    grupos = [r.sample(range(10, 99), 4) for _ in range(3)]
    p2 = [mira(' '.join(f'<b class="xm-n">{x}</b>' for x in grupos[0]) + ' → ' + ''.join(cj(x) for x in sorted(grupos[0])))]
    p2 += [fila(' '.join(f'<b class="xm-n">{x}</b>' for x in g) + ' → ' + ''.join(cj() for _ in g)) for g in grupos[1:]]
    out.append((ej(n + 1, 'Ordena de menor a mayor.'), 'xm', p2))
    return out


def g_reloj(r, n, ej):
    hs = r.sample(range(1, 13), 12)
    it = lambda h, v=None: f'<span class="xm-rel">{reloj(h)}{cj(v, 82)}</span>'
    p = [mira(it(hs[0], f'{hs[0]}:00'))]
    p += [fila(''.join(it(h) for h in hs[1:5])), fila(''.join(it(h) for h in hs[5:9]))]
    out = [(ej(n, 'Escribe la hora.'), 'xm', p)]
    it2 = lambda h: f'<span class="xm-rel">{reloj(h, corta=False)}<span class="xm-c dado" style="width:82px">{h}:00</span></span>'
    out.append((ej(n + 1, 'Dibuja la aguja corta (la de la hora).'), 'xm', [fila(''.join(it2(h) for h in hs[9:12] + hs[1:2]))]))
    return out


def g_monedas(r, n, ej):
    grupos = []
    while len(grupos) < 5:
        g = [r.choice([1, 2, 2, 1, 5]) for _ in range(r.randint(2, 4))]
        if sum(g) <= 10 and sorted(g) not in [sorted(x) for x in grupos]: grupos.append(g)
    it = lambda g, v=None: ''.join(moneda(x) for x in g) + ' = ' + cj(v) + ' €'
    p = [mira(it(grupos[0], sum(grupos[0])))] + [fila(it(g)) for g in grupos[1:]]
    for g in grupos: assert sum(g) <= 10
    return [(ej(n, 'Cuenta cuánto dinero hay.'), 'xm', p)]


def g_lista(lista, nombre):
    def g(r, n, ej):
        idx = (r.sample(range(len(lista)), len(lista)) * 2)[:8]   # la semana solo tiene 7 días
        sig = lambda i: lista[(i + 1) % len(lista)]
        ant = lambda i: lista[i - 1]
        assert all(lista.index(sig(i)) == (i + 1) % len(lista) for i in idx)
        p = [mira(f'Después de <b class="xm-w">{lista[idx[0]]}</b> va: ' + linea(sig(idx[0])))]
        p += [fila(f'Después de <b class="xm-w">{lista[i]}</b> va: ' + linea()) for i in idx[1:4]]
        out = [(ej(n, f'Escribe el {nombre} que va <b>después</b>.'), 'xm', p)]
        p2 = [mira(f'Antes de <b class="xm-w">{lista[idx[4]]}</b> va: ' + linea(ant(idx[4])))]
        p2 += [fila(f'Antes de <b class="xm-w">{lista[i]}</b> va: ' + linea()) for i in idx[5:8]]
        out.append((ej(n + 1, f'Escribe el {nombre} que va <b>antes</b>.'), 'xm', p2))
        return out
    return g


def g_figuras(r, n, ej):
    fs = list(LADOS)
    orden = r.sample(fs, 4) + r.sample(fs, 4)
    it = lambda f, v=None: f'<span class="xm-figit">{figura(f)}{linea(v, 140)}</span>'
    p = [mira(it(orden[0], orden[0])), fila(''.join(it(f) for f in orden[1:4]))]
    out = [(ej(n, 'Escribe el nombre de cada figura.'), 'xm', p)]
    it2 = lambda f, v=None: f'<span class="xm-figit">{figura(f)}{cj(v)} lados</span>'
    p2 = [mira(it2(orden[4], LADOS[orden[4]])), fila(''.join(it2(f) for f in orden[5:8]))]
    out.append((ej(n + 1, '¿Cuántos lados tiene?'), 'xm', p2))
    return out


def g_dibujos(pares, texto):
    def g(r, n, ej):
        return [(ej(n, texto), 'xm', [fila(dibujo(a) + dibujo(b)) for a, b in pares])]
    return g


def g_tabla(r, n, ej):
    sims = ['★', '▲', '●', '■']
    piezas = []
    for k in range(2):
        cuenta = {s: r.randint(2, 8) for s in sims[:3]}
        while len(set(cuenta.values())) < 3: cuenta = {s: r.randint(2, 8) for s in sims[:3]}
        todos = [s for s, c in cuenta.items() for _ in range(c)]; r.shuffle(todos)
        assert all(todos.count(s) == c for s, c in cuenta.items())
        mosaico = '<div class="xm-mos">' + ' '.join(todos) + '</div>'
        tabla = '<table class="xm-tab"><tr>' + ''.join(f'<th>{s}</th>' for s in cuenta) + '</tr><tr>' + ''.join(
            f'<td>{cj(c if k == 0 and i == 0 else None, 46)}</td>' for i, (s, c) in enumerate(cuenta.items())) + '</tr></table>'
        piezas.append(fila(mosaico + tabla))
    return [(ej(n, 'Cuenta cada dibujo y escribe cuántos hay en la tabla. (El primero ya está.)'), 'xm', piezas)]


def g_picto(r, n, ej):
    frutas = [('🍎', 'manzanas'), ('🍌', 'plátanos'), ('🍐', 'peras')]
    c = r.sample(range(2, 8), 3)
    filas = ''.join(f'<tr><td class="xm-pn">{nom}</td><td class="xm-pe">{e * k}</td></tr>' for (e, nom), k in zip(frutas, c))
    mas = frutas[c.index(max(c))][1]
    assert c.count(max(c)) == 1
    pz = [fila(f'<table class="xm-pic">{filas}</table>')       # una sola pieza: el pictograma con sus preguntas
          + fila(f'¿Cuántas {frutas[0][1]} hay? ' + cj()) + fila(f'¿Cuántos {frutas[1][1]} hay? ' + cj())
          + fila('¿De qué fruta hay <b>más</b>? ' + linea(w=190))]
    return [(ej(n, 'Mira el pictograma (cada dibujo es 1) y contesta.'), 'xm', pz)]


PROB = {
    '+': [('🍬', '{nom} tiene <strong>{a}</strong> caramelos y le dan <strong>{b}</strong> más. ¿Cuántos caramelos tiene ahora?', 'caramelos'),
          ('🎈', 'En la fiesta hay <strong>{a}</strong> globos y traen <strong>{b}</strong> más. ¿Cuántos globos hay en total?', 'globos'),
          ('📚', 'En la estantería hay <strong>{a}</strong> libros y {nom} pone <strong>{b}</strong> más. ¿Cuántos libros hay ahora?', 'libros')],
    '−': [('🍪', 'En el plato hay <strong>{a}</strong> galletas y {nom} se come <strong>{b}</strong>. ¿Cuántas galletas quedan?', 'galletas'),
          ('🐦', 'En el árbol hay <strong>{a}</strong> pájaros y se van <strong>{b}</strong>. ¿Cuántos pájaros quedan?', 'pájaros'),
          ('🖍️', '{nom} tiene <strong>{a}</strong> ceras y regala <strong>{b}</strong>. ¿Cuántas ceras le quedan?', 'ceras')]}
NOMBRES = ['Lucas', 'Noa', 'Hugo', 'Sara', 'Leo', 'Vega']


def g_problemas(signos, pauta, signo_elegir=False):
    def g(r, n, ej, inicio=0):
        pz = []
        usados = set()
        for k in range(3):
            s = r.choice(signos)
            emo, t, _ = r.choice([x for x in PROB[s] if x[1] not in usados]); usados.add(t)
            while True:                                    # nivel de 1º: hasta 19, sin llevar ni prestar
                a, b = r.randint(10, 18), r.randint(2, 8)
                if s == '+' and sin_llevar(a, b) and a + b <= 19: break
                if s == '−' and a > b and sin_prestar(a, b) and a - b >= 2: break
            assert a <= 19 and ((s == '+' and sin_llevar(a, b) and a + b <= 19) or (s == '−' and sin_prestar(a, b)))
            txt = t.format(a=a, b=b, nom=r.choice(NOMBRES))
            fl = lambda l, c: f'<div class="pb-fila"><span class="pb-l">{l}</span>{c}</div>'
            pz.append('<div class="pb">'
                      f'<div class="pb-cab"><span class="pb-ico pb-emo">{emo}</span><span class="pb-n">{inicio + k + 1}.</span><span class="pb-t">{txt}</span></div>'
                      + (fl('Rodea el signo:', '<span class="pb-signos"><span>+</span><span>−</span></span>') if signo_elegir else '')
                      + fl('Datos:', pauta) + '<div class="pb-fila pb-op"><span class="pb-l">Operación:</span><div class="pb-cuad"></div></div>'
                      + fl('Solución:', pauta) + '</div>')
        return [('<div class="ej"><span>Más problemas para practicar:</span></div>', 'pbs', pz)]
    return g


GEN1 = {
    'numeros-hasta-99': g_numeros, 'decenas-unidades': g_decenas, 'numeros-ordinales': g_ordinales,
    'comparar-y-ordenar': g_comparar,
    'sumas-sin-llevadas': lambda r, n, ej: g_sumas(r, n, ej, '+'),
    'restas-sin-llevadas': lambda r, n, ej: g_sumas(r, n, ej, '−'),
    'sumas-y-restas-mezcladas': lambda r, n, ej: g_sumas(r, n, ej, '+−'),
    'longitud-peso-capacidad': g_dibujos([('una cosa <b>larga</b>', 'una cosa <b>corta</b>'), ('una cosa que <b>pesa mucho</b>', 'una cosa que <b>pesa poco</b>'),
                                          ('algo que <b>cabe mucha</b> agua', 'algo que <b>cabe poca</b> agua')], 'Dibuja.'),
    'monedas-billetes': g_monedas, 'el-reloj-en-punto': g_reloj,
    'dias-semana': g_lista(DIAS, 'día'), 'meses-del-ano': g_lista(MESES, 'mes'),
    'figuras-planas': g_figuras,
    'cuerpos-geometricos': g_dibujos([('algo con forma de <b>cubo</b>', 'algo con forma de <b>esfera</b>'),
                                      ('algo con forma de <b>cilindro</b>', 'algo con forma de <b>cono</b>')], 'Dibuja una cosa de casa o del cole con esta forma.'),
    'lineas-y-situacion-espacial': g_dibujos([('una línea <b>recta</b>', 'una línea <b>curva</b>'), ('una línea <b>abierta</b>', 'una línea <b>cerrada</b>'),
                                              ('un sol <b>encima</b> de una casa', 'una pelota <b>debajo</b> de una mesa')], 'Dibuja.'),
    'tablas-simples': g_tabla, 'pictogramas': g_picto,
}


def extras(d, n, ej, pauta):
    sub = d['origen'].split('/')[-2]
    curso = d['origen'].split('/')[2]
    if curso != '1': return []
    gen = GEN1.get(sub)
    if sub == 'problemas-suma-sencillos': gen = g_problemas('+', pauta)
    if sub == 'problemas-resta-sencillos': gen = g_problemas('−', pauta)
    if sub == 'problemas-mixtos-basicos': gen = g_problemas('+−', pauta, True)
    if not gen: return []
    r = random.Random(d['origen'])
    if sub.startswith('problemas-'):
        return gen(r, n, ej, inicio=d.get('_problemas', 0))
    return gen(r, n, ej)
