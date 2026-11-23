"""Ejercicios NUEVOS para la última página de las fichas de Mates de 2º (mismo sistema que extras_mates.py).

Siempre con fila resuelta de modelo y comprobados por código. Nivel de 2º:
sumas con llevada (DU+DU ≤ 99), restas con préstamo, tablas del 1 al 10, doble y mitad, números hasta 1000,
ordinales hasta el 20.º, reloj en punto y y media, monedas y billetes hasta 50 €, polígonos.
"""
import math
import random
from html import escape as E
import extras_mates as M
from extras_mates import cj, linea, fila, mira

ORD20 = M.ORD + ['undécimo', 'duodécimo', 'decimotercero', 'decimocuarto', 'decimoquinto', 'decimosexto',
                 'decimoséptimo', 'decimoctavo', 'decimonoveno', 'vigésimo']


def con_llevar(a, b): return (a % 10) + (b % 10) > 9 and a + b <= 99
def con_prestar(a, b): return a % 10 < b % 10 and a > b


def g_sumas2(r, n, ej, signos='+'):
    ops = []
    while len(ops) < 9:
        s = r.choice(signos)
        a, b = r.randint(13, 79), r.randint(12, 69)
        if s == '+' and not con_llevar(a, b): continue
        if s == '−':
            if a < b: a, b = b, a
            if not con_prestar(a, b): continue
        if (a, b, s) not in ops: ops.append((a, b, s))
    for a, b, s in ops:
        assert (s == '+' and con_llevar(a, b)) or (s == '−' and con_prestar(a, b))
    res = lambda a, b, s: a + b if s == '+' else a - b
    a, b, s = ops[0]
    p = [mira(M.op_vertical(a, b, s, res(a, b, s)))]
    p += [fila(''.join(M.op_vertical(*o) for o in ops[k:k+4])) for k in (1, 5)]
    t = {'+': 'Resuelve las sumas. ¡Recuerda la llevada!', '−': 'Resuelve las restas. ¡Recuerda pedir prestado!'}.get(signos, 'Resuelve. ¡Fíjate bien en el signo!')
    return [(ej(n, t), 'xm', p)]


def g_tablas(r, n, ej, tablas=range(2, 10)):
    ops = []
    while len(ops) < 9:
        a, b = r.choice(list(tablas)), r.randint(1, 10)
        if (a, b) not in ops: ops.append((a, b))
    for a, b in ops: assert 1 <= a <= 10 and 1 <= b <= 10
    it = lambda a, b, v=None: f'<span class="xm-par"><b class="xm-n">{a} × {b} =</b>{cj(v, 58)}</span>'
    p = [mira(it(*ops[0], ops[0][0] * ops[0][1]))]
    p += [fila(''.join(it(*o) for o in ops[k:k+4])) for k in (1, 5)]
    return [(ej(n, 'Calcula las multiplicaciones.'), 'xm', p)]


def g_doble(r, n, ej):
    ns = r.sample([x for x in range(2, 50, 2)], 8)
    for x in ns: assert x % 2 == 0 and 2 * x <= 100
    p = [mira(f'<b class="xm-n">{ns[0]}</b> → doble ' + cj(2 * ns[0]) + ' mitad ' + cj(ns[0] // 2))]
    p += [fila(f'<b class="xm-n">{x}</b> → doble ' + cj() + ' mitad ' + cj()) for x in ns[1:5]]
    return [(ej(n, 'Escribe el doble y la mitad.'), 'xm xm-2col', p)]


def g_numeros1000(r, n, ej):
    ns = r.sample(range(101, 999), 5)
    for x in ns: assert 100 < x < 999
    p = [mira(cj(ns[0] - 1, 70) + f'<b class="xm-n">{ns[0]}</b>' + cj(ns[0] + 1, 70))]
    p += [fila(cj(w=70) + f'<b class="xm-n">{x}</b>' + cj(w=70)) for x in ns[1:]]
    out = [(ej(n, 'Escribe el número de antes y el de después.'), 'xm xm-2col', p)]
    cs = r.sample(range(101, 999), 5)
    cdu = lambda x: (x // 100, x // 10 % 10, x % 10)
    p2 = [mira(f'<b class="xm-n">{cs[0]}</b> = ' + cj(cdu(cs[0])[0]) + ' C ' + cj(cdu(cs[0])[1]) + ' D ' + cj(cdu(cs[0])[2]) + ' U')]
    p2 += [fila(f'<b class="xm-n">{x}</b> = ' + cj() + ' C ' + cj() + ' D ' + cj() + ' U') for x in cs[1:]]
    for x in cs: c, d, u = cdu(x); assert 100 * c + 10 * d + u == x
    out.append((ej(n + 1, 'Escribe las centenas (C), decenas (D) y unidades (U).'), 'xm', p2))
    return out


def g_comparar1000(r, n, ej):
    pares = [(r.randint(100, 999), r.randint(100, 999)) for _ in range(9)]
    pares[4] = (pares[4][0], pares[4][0])
    sig = lambda a, b: '>' if a > b else '<' if a < b else '='
    par = lambda a, b, v=None: f'<span class="xm-par"><b class="xm-n">{a}</b>{cj(v, 44)}<b class="xm-n">{b}</b></span>'
    p = [mira(par(*pares[0], sig(*pares[0])))] + [fila(par(*pares[k]) + par(*pares[k+1])) for k in range(1, 9, 2)]
    return [(ej(n, 'Escribe &gt;, &lt; o =.'), 'xm', p)]


def g_pares(r, n, ej):
    ns = r.sample(range(10, 999), 9)
    it = lambda x, v=None: f'<span class="xm-par"><b class="xm-n">{x}</b> → {linea(v, 110)}</span>'
    p = [mira(it(ns[0], 'par' if ns[0] % 2 == 0 else 'impar'))] + [fila(it(ns[k]) + it(ns[k+1])) for k in range(1, 9, 2)]
    return [(ej(n, '¿Es <b>par</b> o <b>impar</b>? Escríbelo.'), 'xm', p)]


def g_series(r, n, ej):
    p = []
    for k in range(5):
        paso = r.choice([2, 5, 10, 100, 50])
        ini = r.randint(1, 30) * paso if paso < 50 else r.randint(1, 4) * paso
        baja = k % 2 == 1
        s = [ini + paso * 6 - paso * i if baja else ini + paso * i for i in range(7)]
        assert all(abs(b - a) == paso for a, b in zip(s, s[1:])) and min(s) >= 0 and max(s) <= 1000
        if k == 0:
            p.append(mira(f'<span class="xm-ord">de {paso} en {paso}</span>' + ''.join(cj(x, 58) for x in s)))
        else:
            hue = set(r.sample(range(2, 7), 3))
            p.append(fila(f'<span class="xm-ord">de {paso} en {paso}</span>' + ''.join(cj(w=58) if i in hue else f'<span class="xm-c dado" style="width:58px">{x}</span>' for i, x in enumerate(s))))
    return [(ej(n, 'Completa la serie.'), 'xm', p)]


def g_ordinales2(r, n, ej):
    ns = r.sample(range(1, 21), 7)
    p = [mira(f'<b class="xm-n">{ns[0]}.º</b> → ' + linea(ORD20[ns[0]-1], 190))]
    p += [fila(f'<b class="xm-n">{x}.º</b> → ' + linea(w=190)) for x in ns[1:]]
    return [(ej(n, 'Escribe el nombre del ordinal.'), 'xm xm-2col', p)]


def reloj2(h, media):
    """Reloj en punto o y media (la corta avanza media hora hacia la siguiente)."""
    s = M.reloj(h, corta=False)
    if media:
        s = s.replace('x2="50" y2="18"', 'x2="50" y2="82"')
    a = math.radians(((h % 12) + (0.5 if media else 0)) * 30)
    x, y = 50 + 22 * math.sin(a), 50 - 22 * math.cos(a)
    return s.replace('<circle cx="50" cy="50" r="3"', f'<line x1="50" y1="50" x2="{x:.1f}" y2="{y:.1f}" stroke="#1a1a1a" stroke-width="4.5" stroke-linecap="round"/><circle cx="50" cy="50" r="3"')


def g_reloj2(r, n, ej):
    hs = [(h, m) for h in r.sample(range(1, 13), 9) for m in [r.random() < 0.5]][:9]
    txt = lambda h, m: f'{h}:{"30" if m else "00"}'
    it = lambda h, m, v=None: f'<span class="xm-rel">{reloj2(h, m)}{cj(v, 82)}</span>'
    p = [mira(it(*hs[0], txt(*hs[0])))] + [fila(''.join(it(*x) for x in hs[k:k+4])) for k in (1, 5)]
    return [(ej(n, 'Escribe la hora (en punto o y media).'), 'xm', p)]


def g_monedas2(r, n, ej):
    import dinero
    pieza = lambda v: dinero.billete(v, ' class="xm-bill" viewBox="0 0 160 90"') if v >= 5 else dinero.moneda(v * 100, ' class="xm-mon" viewBox="0 0 100 100"')
    grupos = []
    while len(grupos) < 5:
        g = sorted([r.choice([1, 2, 5, 10, 20, 50]) for _ in range(r.randint(2, 4))], reverse=True)
        if sum(g) <= 99 and g not in grupos: grupos.append(g)
    it = lambda g, v=None: ''.join(pieza(x) for x in g) + ' = ' + cj(v, 60) + ' €'
    p = [mira(it(grupos[0], sum(grupos[0])))] + [fila(it(g)) for g in grupos[1:]]
    return [(ej(n, 'Cuenta cuánto dinero hay.'), 'xm', p)]


POLI = {'triángulo': 3, 'cuadrado': 4, 'rectángulo': 4, 'pentágono': 5, 'hexágono': 6}


def poligono(nombre):
    if nombre in ('triángulo', 'cuadrado', 'rectángulo'): return M.figura(nombre)
    k = POLI[nombre]
    pts = ' '.join(f'{30 + 25 * math.sin(2 * math.pi * i / k):.1f},{31 - 25 * math.cos(2 * math.pi * i / k):.1f}' for i in range(k))
    return f'<svg class="xm-fig" viewBox="0 0 60 60" fill="#fff" stroke="#1a1a1a" stroke-width="2.5"><polygon points="{pts}"/></svg>'


def g_poligonos(r, n, ej):
    fs = r.sample(list(POLI), 5) + r.sample(list(POLI), 3)
    it = lambda f, v=None, w=None: f'<span class="xm-figit">{poligono(f)}{cj(v)} lados</span>'
    p = [mira(it(fs[0], POLI[fs[0]])), fila(''.join(it(f) for f in fs[1:4])), fila(''.join(it(f) for f in fs[4:8]))]
    return [(ej(n, '¿Cuántos lados tiene cada polígono?'), 'xm', p)]


PROB2 = {
    '+': [('🍬', '{nom} tiene <strong>{a}</strong> caramelos y le regalan <strong>{b}</strong>. ¿Cuántos tiene ahora?'),
          ('📚', 'En la biblioteca hay <strong>{a}</strong> cuentos y llegan <strong>{b}</strong> más. ¿Cuántos cuentos hay?'),
          ('🎈', 'Para la fiesta hay <strong>{a}</strong> globos rojos y <strong>{b}</strong> azules. ¿Cuántos globos hay en total?')],
    '−': [('🍪', 'En la caja hay <strong>{a}</strong> galletas y se comen <strong>{b}</strong>. ¿Cuántas quedan?'),
          ('🃏', '{nom} tiene <strong>{a}</strong> cromos y regala <strong>{b}</strong>. ¿Cuántos le quedan?'),
          ('🐦', 'En el parque hay <strong>{a}</strong> palomas y se van <strong>{b}</strong>. ¿Cuántas quedan?')],
    '×': [('🧁', 'Hay <strong>{a}</strong> bandejas con <strong>{b}</strong> magdalenas cada una. ¿Cuántas magdalenas hay?'),
          ('🪑', 'En la clase hay <strong>{a}</strong> filas de <strong>{b}</strong> sillas. ¿Cuántas sillas hay?'),
          ('⚽', 'Hay <strong>{a}</strong> cajas y en cada caja hay <strong>{b}</strong> pelotas. ¿Cuántas pelotas hay?')]}


def g_problemas2(signos, pauta, elegir=False):
    def g(r, n, ej, inicio=0):
        pz = []; usados = set()
        for k in range(3):
            s = r.choice(signos)
            emo, t = r.choice([x for x in PROB2[s] if x[1] not in usados]); usados.add(t)
            while True:
                if s == '×': a, b = r.randint(2, 9), r.randint(2, 9); break
                a, b = r.randint(13, 79), r.randint(12, 59)
                if s == '+' and con_llevar(a, b): break
                if s == '−' and a > b and con_prestar(a, b): break
            fl = lambda l, c: f'<div class="pb-fila"><span class="pb-l">{l}</span>{c}</div>'
            pz.append('<div class="pb">'
                      f'<div class="pb-cab"><span class="pb-ico pb-emo">{emo}</span><span class="pb-n">{inicio + k + 1}.</span><span class="pb-t">{t.format(a=a, b=b, nom=r.choice(M.NOMBRES))}</span></div>'
                      + (fl('Rodea el signo:', '<span class="pb-signos"><span>+</span><span>−</span><span>×</span></span>') if elegir else '')
                      + fl('Datos:', pauta) + '<div class="pb-fila pb-op"><span class="pb-l">Operación:</span><div class="pb-cuad"></div></div>'
                      + fl('Solución:', pauta) + '</div>')
        return [('<div class="ej"><span>Más problemas para practicar:</span></div>', 'pbs', pz)]
    return g


GEN2 = {
    'numeros-hasta-1000': g_numeros1000, 'centenas-decenas-unidades': g_numeros1000, 'comparar-y-ordenar': g_comparar1000,
    'pares-e-impares': g_pares, 'series-numericas': g_series, 'numeros-ordinales': g_ordinales2,
    'sumas-con-llevada': lambda r, n, ej: g_sumas2(r, n, ej, '+'), 'restas-con-llevada': lambda r, n, ej: g_sumas2(r, n, ej, '−'),
    'sumas-y-restas-mezcladas': lambda r, n, ej: g_sumas2(r, n, ej, '+−'),
    'multiplicacion-concepto': lambda r, n, ej: g_tablas(r, n, ej, (2, 5, 10)), 'tablas-de-multiplicar': g_tablas, 'doble-y-mitad': g_doble,
    'el-reloj-horas-y-media': g_reloj2, 'monedas-y-billetes': g_monedas2,
    'calendario': M.g_lista(M.MESES, 'mes'),
    'figuras-planas': g_poligonos,
    'cuerpos-geometricos': M.g_dibujos([('algo con forma de <b>prisma</b>', 'algo con forma de <b>pirámide</b>'),
                                        ('algo con forma de <b>cilindro</b>', 'algo con forma de <b>esfera</b>')], 'Dibuja una cosa de casa o del cole con esta forma.'),
    'lineas-rectas-curvas-poligonales': M.g_dibujos([('una línea <b>poligonal abierta</b>', 'una línea <b>poligonal cerrada</b>'),
                                                     ('una línea <b>recta</b>', 'una línea <b>curva</b>')], 'Dibuja con la regla.'),
    'simetria': M.g_dibujos([('una cosa <b>simétrica</b>', 'otra cosa <b>simétrica</b>')], 'Dibuja y traza su eje de simetría.'),
    'tablas-de-datos': M.g_tabla, 'pictogramas': M.g_picto,
}


def extras(d, n, ej, pauta):
    sub = d['origen'].split('/')[-2]
    gen = GEN2.get(sub)
    if sub == 'problemas-suma-con-llevada': gen = g_problemas2('+', pauta)
    if sub == 'problemas-resta-con-prestar': gen = g_problemas2('−', pauta)
    if sub == 'problemas-multiplicacion': gen = g_problemas2('×', pauta)
    if sub == 'problemas-mixtos': gen = g_problemas2('+−×', pauta, True)          # dos-operaciones: sin extras (serían de un paso)
    if not gen: return []
    r = random.Random(d['origen'])
    if sub == 'tablas-de-multiplicar':                    # cada ficha, solo su tabla (f10 = repaso de todas)
        import re as _re
        k = int(_re.search(r'ficha-(\d+)', d['origen']).group(1))
        tab = {1: (1, 10), 2: (2,), 3: (5,), 4: (3,), 5: (4,), 6: (6,), 7: (7,), 8: (8,), 9: (9,)}.get(k, tuple(range(2, 11)))
        return g_tablas(r, n, ej, tab)
    return gen(r, n, ej, inicio=d.get('_problemas', 0)) if sub.startswith('problemas-') else gen(r, n, ej)
