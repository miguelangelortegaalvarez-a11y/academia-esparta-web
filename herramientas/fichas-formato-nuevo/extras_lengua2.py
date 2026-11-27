"""Ejercicios NUEVOS para llenar la última página de las fichas de Lengua de 2º (gramática y ortografía).

Igual que en Mates: solo entran si la ficha ya pasa a dos páginas y caben; empiezan con una fila resuelta
de modelo («Mira cómo se hace») y se escribe sobre pauta. Las listas de palabras están escritas a mano y
se comprueban con assert (reglas del plural, del femenino, parejas…). Se evitan las palabras que ya salen
en la propia ficha.
"""
import random
import re
from html import escape as E
from extras_mates import mira, fila, cj

MINI = ''          # pauta pequeña (la pone convertir.py)

# ── listas comprobadas ──
SINGULARES = ['pato', 'mesa', 'casa', 'flor', 'árbol', 'lápiz', 'pez', 'reloj', 'niña', 'perro', 'tren', 'luz',
              'camión', 'sol', 'nube', 'libro', 'ratón', 'nariz', 'papel', 'cuchara', 'avión', 'mar', 'silla', 'gato']
PLURAL_A_MANO = {'árbol': 'árboles', 'lápiz': 'lápices', 'pez': 'peces', 'reloj': 'relojes', 'tren': 'trenes',
                 'luz': 'luces', 'camión': 'camiones', 'sol': 'soles', 'ratón': 'ratones', 'nariz': 'narices',
                 'papel': 'papeles', 'avión': 'aviones', 'mar': 'mares', 'flor': 'flores'}


def plural(p):
    if p in PLURAL_A_MANO: return PLURAL_A_MANO[p]
    assert p[-1] in 'aeiou', p
    return p + 's'


FEMENINO = [('gato', 'gata'), ('niño', 'niña'), ('perro', 'perra'), ('abuelo', 'abuela'), ('conejo', 'coneja'),
            ('oso', 'osa'), ('león', 'leona'), ('profesor', 'profesora'), ('pato', 'pata'), ('tío', 'tía'),
            ('hermano', 'hermana'), ('cerdo', 'cerda'), ('mono', 'mona'), ('pintor', 'pintora'), ('lobo', 'loba'),
            ('señor', 'señora'), ('vecino', 'vecina'), ('primo', 'prima'), ('doctor', 'doctora'), ('zorro', 'zorra')]
for m_, f_ in FEMENINO:
    assert (m_.endswith('o') and f_ == m_[:-1] + 'a') or f_ == m_.replace('ó', 'o') + 'a', (m_, f_)

SINONIMOS = [('contento', 'alegre'), ('grande', 'enorme'), ('rápido', 'veloz'), ('bonito', 'precioso'),
             ('empezar', 'comenzar'), ('hablar', 'decir'), ('mirar', 'observar'), ('pequeño', 'chico'),
             ('listo', 'inteligente'), ('cansado', 'agotado'), ('feliz', 'dichoso'), ('regalo', 'obsequio'),
             ('cara', 'rostro'), ('enfadado', 'furioso'), ('caminar', 'andar'), ('miedo', 'susto')]
ANTONIMOS = [('alto', 'bajo'), ('frío', 'caliente'), ('día', 'noche'), ('abrir', 'cerrar'), ('rápido', 'lento'),
             ('lleno', 'vacío'), ('limpio', 'sucio'), ('alegre', 'triste'), ('dentro', 'fuera'), ('subir', 'bajar'),
             ('nuevo', 'viejo'), ('fuerte', 'débil'), ('mucho', 'poco'), ('encender', 'apagar'), ('cerca', 'lejos'),
             ('ganar', 'perder')]
for lst in (SINONIMOS, ANTONIMOS):
    assert len(set(a for a, b in lst)) == len(lst)

FRASES = ['el gato duerme en el sofá', 'mi hermana tiene una bici roja', 'hoy llueve mucho', 'los niños juegan en el patio',
          'mañana vamos al parque', 'el perro corre detrás de la pelota', 'me gusta leer cuentos', 'la abuela hace un pastel',
          'el sol sale por la mañana', 'en clase tenemos un pez', 'papá lleva gafas nuevas', 'el tren llega a las cinco']
for f_ in FRASES: assert f_ == f_.lower() and not f_.endswith('.')

CLASES = [('perro', 'nombre'), ('saltar', 'verbo'), ('azul', 'adjetivo'), ('mesa', 'nombre'), ('comer', 'verbo'),
          ('alto', 'adjetivo'), ('niño', 'nombre'), ('dormir', 'verbo'), ('feliz', 'adjetivo'), ('libro', 'nombre'),
          ('correr', 'verbo'), ('suave', 'adjetivo'), ('casa', 'nombre'), ('cantar', 'verbo'), ('rojo', 'adjetivo'),
          ('árbol', 'nombre'), ('nadar', 'verbo'), ('pequeño', 'adjetivo')]


def _libres(lst, html, clave=lambda x: x):
    """Quita lo que ya sale en la ficha (para no repetir ni regalar respuestas)."""
    t = re.sub(r'<[^>]+>', ' ', html).lower()
    return [x for x in lst if not re.search(r'\b' + re.escape(clave(x).lower()) + r'\b', t)]


def _pares(r, n, ej, html, lista, titulo):
    """Modelo + dos bloques de 3 parejas, cada uno completo (si solo cabe uno, sigue teniendo solución)."""
    ps = r.sample(_libres(lista, html, lambda x: x[0]), 7)
    modelo = mira(f'<span class="xm-w">{E(ps[0][0])}</span> → <span class="xm-ok">{E(ps[0][1])}</span>')
    bloques = []
    for k, grupo in enumerate((ps[1:4], ps[4:7])):
        der = grupo[:]
        while der == grupo: r.shuffle(der)
        letras = 'ABC' if k == 0 else 'DEF'
        filas = ''.join(f'<div class="xm-une"><span class="xm-w">{3*k+i+1}. {E(a)}</span>{cj(w=40)}'
                        f'<span class="xm-w">{letras[i]}. {E(der[i][1])}</span></div>' for i, (a, _) in enumerate(grupo))
        assert sorted(b for _, b in grupo) == sorted(b for _, b in der)
        bloques.append(f'<div class="xm-unes">{filas}</div>')
    return [(ej(n, titulo), 'xm', [modelo] + bloques)]


def _pp(w, ok=None):
    """Casilla «palabra arriba, pauta debajo» (Miguel, 27-nov-2026). Con ok = el modelo, escrito en verde sobre la pauta."""
    pz = MINI.replace('<svg class="mini-pauta"', '<svg class="mini-pauta" preserveAspectRatio="none"', 1)
    if ok is None: return fila(f'<span class="xm-w">{w}</span>{pz}')
    return mira(f'<span class="xm-w">{w}</span><div class="xm-pz">{pz}<span class="xm-ok">{ok}</span></div>')


def g_plural(r, n, ej, html):
    ws = r.sample(_libres(SINGULARES, html), 7)
    p = [_pp(E(ws[0]), E(plural(ws[0])))] + [_pp(E(w)) for w in ws[1:]]
    return [(ej(n, 'Escribe el <b>plural</b>.'), 'xm xm-2col xm-pp', p)]


def g_femenino(r, n, ej, html):
    ws = r.sample(_libres(FEMENINO, html, lambda x: x[0]), 7)
    p = [_pp(E(ws[0][0]), E(ws[0][1]))] + [_pp(E(m_)) for m_, _ in ws[1:]]
    return [(ej(n, 'Escribe el <b>femenino</b>.'), 'xm xm-2col xm-pp', p)]


def g_signos(r, n, ej, html):
    fs = r.sample(_libres(FRASES, html), 4)
    p = [mira(f'<span class="xm-fr">{E(fs[0])}</span> → <span class="xm-ok">{E(fs[0][0].upper() + fs[0][1:])}.</span>')]
    p += [fila(f'<span class="xm-fr">{E(f_)}</span>') + fila(MINI.replace('class="mini-pauta"', 'class="mini-pauta larga"')) for f_ in fs[1:]]
    return [(ej(n, 'Escribe la frase bien: con <b>mayúscula</b> al principio y <b>punto</b> al final.'), 'xm', p)]


def g_clases(r, n, ej, html):
    ws = r.sample(_libres(CLASES, html, lambda x: x[0]), 7)
    p = [_pp(E(ws[0][0]), ws[0][1])] + [_pp(E(w)) for w, _ in ws[1:]]
    return [(ej(n, '¿Es un <b>nombre</b>, un <b>adjetivo</b> o un <b>verbo</b>? Escríbelo.'), 'xm xm-2col xm-pp', p)]


GEN = {
    'singular-plural': g_plural, 'masculino-femenino': g_femenino, 'signos-puntuacion': g_signos,
    'nombre-adjetivo-verbo': g_clases,
    'sinonimos': lambda r, n, ej, h: _pares(r, n, ej, h, SINONIMOS, 'Une cada palabra con su <b>sinónimo</b>. Escribe la letra.'),
    'antonimos': lambda r, n, ej, h: _pares(r, n, ej, h, ANTONIMOS, 'Une cada palabra con su <b>antónimo</b>. Escribe la letra.'),
}

LECTURA = {'lectura-fluida', 'inferencias-simples', 'idea-principal', 'secuencia-temporal',
           'comprension-instrucciones', 'vocabulario-en-contexto'}


def extras(d, n, ej, mini):
    global MINI
    MINI = mini
    sub = d['origen'].split('/')[-2]
    gen = GEN.get(sub)
    if not gen: return []
    return gen(random.Random(d['origen']), n, ej, ''.join(d['bloques']))
