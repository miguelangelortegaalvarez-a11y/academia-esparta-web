#!/usr/bin/env python3
"""Fichas de 3.º (y 4.º) en el formato nuevo: letra Nunito, interior verde claro, + PDF.

Piloto del 23-nov-2026 (6 fichas). El contenido es el de la ficha antigua, transcrito a mano
en FICHAS (abajo); solo se añade un «Mira cómo se hace» con un ejemplo NUEVO donde ayuda.
Misma dirección que la ficha antigua: la cabecera (title, description, canonical, OG, JSON-LD)
se conserva de la ficha antigua la PRIMERA vez y se guarda en cabeceras/<ruta>.json.

    python3 herramientas/fichas-3-4/generar.py            # todas las de FICHAS
    python3 herramientas/fichas-3-4/generar.py <ruta> ...  # solo esas
"""
import json, os, re, shutil, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..'))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CSS = open(os.path.join(AQUI, 'estilo.css'), encoding='utf8').read()
FUENTE = '<link rel="preconnect" href="https://fonts.googleapis.com" /><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin /><link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&amp;display=swap" rel="stylesheet" />'


# ───────────────────────── piezas ─────────────────────────
def ej(n, t):
    return f'<div class="ej"><span class="ej-n">{n}</span><span>{t}</span></div>'


def recuerda(html, t='Recuerda'):
    return f'<div class="recuerda"><div style="flex:1"><div class="rec-t">{t}</div>{html}</div></div>'


def lectura(titulo, parrafos):
    return f'<div class="lectura"><div class="lec-t">{titulo}</div>' + ''.join(f'<p>{p}</p>' for p in parrafos) + '</div>'


def preg(n, q, lineas=1, letras=None, opciones=None):
    h = f'<div class="preg">{ej(n, q)}'
    if opciones: h += '<div class="op3">' + ''.join(f'<span>{o}</span>' for o in opciones) + '</div>'
    if letras: h += ''.join(f'<div class="ln-l"><b>{l})</b><div class="ln"></div></div>' for l in letras)
    else: h += '<div class="ln"></div>' * lineas
    return h + '</div>'


def lista_cuadro(items, modelo=None):
    h = '<div class="lista">'
    if modelo:
        h += (f'<div class="lista-f ejm"><b></b><span class="fr">{modelo[0]} <span class="mira-t" style="margin-left:8px">Mira cómo se hace</span></span>'
              f'<span class="cuadro">{modelo[1]}</span></div>')
    h += ''.join(f'<div class="lista-f"><b>{"abcdefgh"[i]})</b><span class="fr">{t}</span><span class="cuadro"></span></div>' for i, t in enumerate(items))
    return h + '</div>'


def lista_frases(items):
    return '<div class="lista">' + ''.join(f'<div class="lista-f" style="font-size:17px;line-height:1.9"><b>{"abcdefgh"[i]})</b><span class="fr">{t}</span></div>' for i, t in enumerate(items)) + '</div>'


def texto(t):
    return f'<div class="texto-c">{t}</div>'


def copia(n):
    return '<div class="copia">' + '<div class="ln"></div>' * n + '</div>'


def pz(v, u):
    return f'<span class="pz"><b>{v}</b><i>{u}</i></span>'


def vop(a, b, sol=False):
    """Suma vertical de 3 cifras con circulitos para las llevadas."""
    A, B, r = f'{a:03d}', f'{b:03d}', f'{a+b:03d}'
    assert a + b < 1000
    cU = (int(A[2]) + int(B[2])) // 10
    cD = (int(A[1]) + int(B[1]) + cU) // 10
    ll = '<span></span>' + ''.join((f'<span class="ll v">{"1" if m else ""}</span>' if sol else '<span class="ll"><i></i></span>') for m in (cD, cU)) + '<span class="ll"></span>'
    return ('<div class="vg">' + ll + '<span></span>' + ''.join(f'<span>{d}</span>' for d in A)
            + '<span class="sg">+</span>' + ''.join(f'<span>{d}</span>' for d in B) + '<span class="br"></span>'
            + '<span></span>' + ''.join(f'<span class="r{" v" if sol else ""}">{d if sol else ""}</span>' for d in r) + '</div>')


def rej(a, b):
    celdas = ('<span class="s"></span>' + '<span class="ll"></span>' * 4 + '<span class="s"></span>' + '<span></span>' * 4
              + '<span class="s">+</span>' + '<span></span>' * 4 + '<span class="s"></span>' + '<span class="res"></span>' * 4)
    return f'<div class="col-it"><span class="col-t">{a} + {b}</span><div class="rej">{celdas}</div></div>'


def cifras(n):
    return [int(c) for c in str(n).replace('.', '')]


def miles(n):
    return f'{n:,}'.replace(',', '.')


# ───────────────────────── contenido de cada ficha ─────────────────────────
def f_idea(titulo, parrafos, preguntas):
    return lambda L: (f'<div class="instr"><img src="{L}leyendo.webp" alt="">Lee con atención el texto.</div>'
                      + lectura(titulo, parrafos) + '<div style="height:8px"></div>'
                      + ''.join(preg(k, *p) if isinstance(p, tuple) else preg(k, **p) for k, p in enumerate(preguntas, 1))
                      + FIN_STATIC)


FIN = '<div class="fin-b"><img src="{L}pulgar.webp" alt="">¡Buen trabajo!</div>'
FIN_STATIC = '<div class="fin-b" style="position:static"><img src="{L}pulgar.webp" alt="">¡Buen trabajo!</div>'


def mates_numeros(L):
    fila = lambda n: f'<tr><td>{n}</td><td></td><td></td><td></td><td></td></tr>'
    formar = [(4, 2, 6, 3), (7, 0, 5, 1), (5, 8, 0, 9)]
    f2 = ''.join('<div class="form-f">' + f'{pz(a,"UM")}<span class="op">+</span>{pz(b,"C")}<span class="op">+</span>{pz(c,"D")}<span class="op">+</span>{pz(d,"U")}<span class="op">=</span><span class="resp"></span></div>' for a, b, c, d in formar)
    f3 = ''.join(f'<div class="desc-f"><span class="desc-n">{n}</span><span class="op">=</span>' + '<span class="op">+</span>'.join(['<span class="resp"></span>'] * 4) + '</div>' for n in ('3.847', '6.520', '4.906'))
    serie = ['1.000', '2.000', '', '4.000', '', '6.000', '', '8.000', '', '10.000']
    s4 = '<span class="s-fl">›</span>'.join(f'<div class="s-it"><span class="s-c{" dado" if v else ""}">{v}</span></div>' for v in serie)
    # comprobaciones de los ejemplos nuevos
    assert cifras(1352) == [1, 3, 5, 2] and 3000 + 100 + 40 + 2 == 3142 and 2000 + 700 + 30 + 5 == 2735
    rec = lambda n, a: (f'<div class="rec-it"><div class="rec-n">{n}</div><div class="rec-l">'
                        + ' + '.join(f'<b>{d}</b> {u}' for d, u in zip(cifras(n), ('UM', 'C', 'D', 'U'))) + f'<br>{a}</div></div>')
    return (recuerda('<div class="rec-cols">' + rec('3.582', '3.000 + 500 + 80 + 2') + rec('4.090', '4.000 + 0 + 90 + 0') + rec('6.005', '6.000 + 0 + 0 + 5')
                     + '</div><div class="ord">El orden de las cifras: <span>UM</span>›<span>C</span>›<span>D</span>›<span>U</span> &nbsp;·&nbsp; 1 UM = 1.000 U</div>')
            + ej(1, 'Descompón cada número en unidades de millar, centenas, decenas y unidades.')
            + '<table class="tabla"><tr><th>Número</th><th>UM<small>unidades de millar</small></th><th>C<small>centenas</small></th><th>D<small>decenas</small></th><th>U<small>unidades</small></th></tr>'
            + '<tr class="ejm"><td>1.352 <span class="mira-t">Mira</span></td><td>1</td><td>3</td><td>5</td><td>2</td></tr>'
            + ''.join(fila(n) for n in ('2.461', '5.738', '7.090', '3.604', '8.205')) + '</table>'
            + ej(2, 'Escribe el número que se forma.')
            + f'<div class="form"><div class="form-f ejm">{pz(3,"UM")}<span class="op">+</span>{pz(1,"C")}<span class="op">+</span>{pz(4,"D")}<span class="op">+</span>{pz(2,"U")}<span class="op">=</span><span class="resp">3.142</span><span class="mira-t" style="margin-left:6px">Mira cómo se hace</span></div>{f2}</div>'
            + ej(3, 'Descompón cada número en una suma.')
            + '<div class="form"><div class="desc-f ejm"><span class="desc-n">2.735</span><span class="op">=</span><span class="resp">2.000</span><span class="op">+</span><span class="resp">700</span><span class="op">+</span><span class="resp">30</span><span class="op">+</span><span class="resp">5</span></div>' + f3 + '</div>'
            + f'<div class="ej"><span class="ej-n">4</span><span>Completa la serie contando de 1.000 en 1.000.</span><span class="fin-in"><img src="{L}pulgar.webp" alt="">¡Buen trabajo!</span></div>'
            + f'<div class="serie">{s4}</div>')


def mates_sumas(L):
    sumas = [(247, 168), (356, 275), (489, 134), (528, 196), (374, 247), (615, 287), (463, 158), (729, 195)]
    coloca = [(345, 287), (176, 459), (638, 254), (467, 158), (384, 276), (529, 263)]
    for a, b in sumas + coloca: assert (a % 10 + b % 10) >= 10 or (a // 10 % 10 + b // 10 % 10) >= 10, (a, b)
    return (recuerda('<div class="rec-wrap"><div class="rec-p">Coloca las cifras bien alineadas: <b>U bajo U, D bajo D y C bajo C</b>. '
                     'Suma empezando por las <b>unidades</b>. Cuando una columna <b>pasa de 9</b>, escribes la última cifra y <b>te llevas 1</b> a la columna siguiente: '
                     'apúntalo en el circulito de arriba.</div>' f'<div class="rec-op">{vop(368, 275, True)}</div></div>')
            + ej(1, 'Resuelve estas sumas. No olvides las cifras que te llevas.')
            + '<div class="ops">' + ''.join(f'<div class="vop">{vop(a, b)}</div>' for a, b in sumas) + '</div>'
            + ej(2, 'Coloca cada suma en la cuadrícula y resuélvela.')
            + '<div class="col">' + ''.join(rej(a, b) for a, b in coloca) + '</div>' + FIN)


def orto1(L):
    return (recuerda('<div class="rec-p">Se escribe <b>mayúscula</b> al inicio de oración, después de punto y en los nombres propios.<br>'
                     'El <b>punto</b> va al final de una oración. La siguiente empieza con mayúscula.</div>')
            + ej(1, 'Rodea las letras que deberían ser mayúsculas.')
            + texto('ayer fui al parque con mi amiga laura. hacía mucho sol y los niños jugaban. mi perro toby corría muy rápido. después fuimos a casa de mis abuelos en málaga. fue un día genial.')
            + ej(2, 'Escribe <span class="verde">M</span> (mayúscula) o <span class="verde">m</span> (minúscula) según corresponda.')
            + lista_cuadro(['El nombre de mi ciudad:', 'La primera palabra de una frase:', 'El día de la semana (lunes):',
                            'El nombre de una persona (carlos):', 'La palabra después de una coma:'], ('El nombre de un río (ebro)', 'M'))
            + ej(3, 'Copia el texto colocando los puntos y las mayúsculas donde faltan.')
            + texto('el lunes llegó un niño nuevo al colegio se llama pablo viene de barcelona le gusta el fútbol y los videojuegos todos le dieron la bienvenida')
            + copia(3) + FIN)


def orto2(L):
    sig = lambda s, t: f'<span class="sig-it"><b>{s}</b>{t}</span>'
    return (recuerda('<div class="sigs">' + sig('.', 'termina la oración') + sig(',', 'pausa o lista') + sig('¿ ?', 'pregunta') + sig('¡ !', 'exclamación') + '</div>')
            + ej(1, 'Escribe el signo de puntuación que falta al final.')
            + lista_cuadro(['¿Cuántos años tienes', '¡Qué día tan bonito', 'Mañana tengo un examen de matemáticas',
                            '¿Dónde has puesto mis llaves', '¡Gol', 'El gato duerme en el sofá'], ('¿Vienes al parque', '?'))
            + ej(2, 'Añade comas para separar los elementos de la lista.')
            + lista_frases(['En mi mochila hay un libro un cuaderno un estuche y una botella.',
                            'Me gustan el fútbol la natación el baloncesto y el tenis.',
                            'Compré manzanas naranjas plátanos y uvas en el mercado.'])
            + ej(3, 'Puntúa correctamente este texto.')
            + texto('Hoy en el recreo paula me preguntó qué te pasa estás triste yo le respondí no me duele la cabeza ella dijo vaya qué mala suerte luego me trajo un vaso de agua')
            + copia(3) + FIN)


FICHAS = {
    'recursos/primaria/3/lengua/idea-principal/lectura-1.html': ('Lengua', 'Idea principal', 'Idea principal y secundarias', f_idea('Las abejas', [
        'Las abejas son insectos imprescindibles para la naturaleza. Viven en colonias de miles de individuos organizadas dentro de una colmena. Cada abeja tiene una misión: la reina pone huevos, las obreras recogen néctar y cuidan la colmena, y los zánganos se reproducen con la reina.',
        'Su papel más importante es la polinización: al volar de flor en flor en busca de alimento, transportan el polen y permiten que las plantas se reproduzcan. Sin las abejas, muchos cultivos y especies vegetales desaparecerían.'],
        [('¿Cuál es la idea principal del texto?', 2), {'q': 'Escribe dos ideas secundarias del texto.', 'letras': 'ab'},
         ('Escribe un título adecuado para este texto basándote en su idea principal.', 1),
         {'q': '¿Dónde aparece la idea principal: al principio, en el medio o al final del texto?', 'opciones': ['al principio', 'en el medio', 'al final']}])),
    'recursos/primaria/3/lengua/idea-principal/lectura-2.html': ('Lengua', 'Idea principal', 'Idea principal y secundarias', f_idea('La tortuga marina', [
        'La tortuga marina es uno de los animales más antiguos de nuestro planeta. Su cuerpo está protegido por un caparazón duro y aplanado que le permite deslizarse con facilidad por el agua. Sus aletas delanteras son largas y poderosas, perfectas para recorrer largas distancias en el océano.',
        'Estas tortugas pasan casi toda su vida en el mar. Sin embargo, cada cierto tiempo las hembras salen a tierra firme para poner sus huevos en la arena de las playas, siempre regresando a la misma orilla donde ellas nacieron.'],
        [('¿Cuál es la idea principal del texto?', 2), {'q': 'Escribe dos ideas secundarias del texto.', 'letras': 'ab'},
         ('Escribe un título para este texto que resuma su idea principal.', 1),
         ('¿Por qué crees que las ideas secundarias son importantes en este texto?', 2)])),
    'recursos/primaria/3/lengua/ortografia/ficha-1.html': ('Lengua', 'Ortografía', 'Mayúsculas y punto', orto1),
    'recursos/primaria/3/lengua/ortografia/ficha-2.html': ('Lengua', 'Ortografía', 'Signos de puntuación', orto2),
    'recursos/primaria/3/matematicas/numeros/numeros-hasta-10000/ficha-1.html': ('Matemáticas', 'Números hasta 10.000', 'Unidades de millar (UM · C · D · U)', mates_numeros),
    'recursos/primaria/3/matematicas/operaciones/sumas-y-restas-llevando/ficha-1.html': ('Matemáticas', 'Sumas y restas llevando', 'Sumas llevando · 3 cifras', mates_sumas),
}

EXTRA = """
.preg .ej{font-size:16px}
.sigs{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.sig-it{background:#fff;border:1px solid var(--linea);border-radius:10px;padding:5px 8px;font-size:13px;white-space:nowrap;display:flex;align-items:center;gap:8px}
.sig-it b{font-size:22px;color:var(--verde);font-weight:800;min-width:24px;text-align:center}
.fin-in{margin-left:auto;display:flex;align-items:center;gap:6px;font-size:14px;font-weight:700;color:var(--verde);margin-top:-14px}.fin-in img{height:46px}
"""


# ───────────────────────── montaje ─────────────────────────
def cabecera(rel):
    jd = os.path.join(AQUI, 'cabeceras', os.path.splitext(rel)[0] + '.json')
    if os.path.exists(jd): return json.load(open(jd, encoding='utf8'))
    s = open(os.path.join(RAIZ, rel), encoding='utf8').read()
    assert 'class="pagina"' not in s, f'{rel} ya está convertida y no hay cabecera guardada'
    head = re.sub(r'<style>.*?</style>', '', s.split('</head>')[0], flags=re.S)
    lineas = []
    for m in re.finditer(r'<(title|script)\b[^>]*>.*?</\1>|<(?:meta|link)\b[^>]*>', head, flags=re.S):
        x = m.group(0)
        if 'charset' in x or 'name="viewport"' in x or 'fonts.googleapis' in x or 'fonts.gstatic' in x: continue
        lineas.append(x.strip())
    os.makedirs(os.path.dirname(jd), exist_ok=True)
    json.dump(lineas, open(jd, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    return lineas


def nombre_pdf(rel):
    p = rel.split('/')
    return f'{p[-2]}-{os.path.splitext(p[-1])[0]}-{p[2]}-primaria.pdf'


def generar(rel):
    asig, pill, rot, cuerpo = FICHAS[rel]
    curso = rel.split('/')[2]
    REL = '../' * rel.count('/')
    L = REL + 'mascota/leoni/'
    html_c = cuerpo(L).replace('{L}', L)
    nom = nombre_pdf(rel)
    doc = ('<!DOCTYPE html>\n<html lang="es">\n<head>\n  <meta charset="UTF-8" />\n  <meta name="viewport" content="width=820" />\n'
           + ''.join('  ' + x + '\n' for x in cabecera(rel)) + '  ' + FUENTE + '\n'
           f'  <style>{CSS}{EXTRA}</style>\n</head>\n<body>\n'
           f'<div class="topbar"><a class="back-btn" href="{REL}materiales.html">← Volver</a>'
           f'<a class="pdf-btn" href="{nom}" target="_blank" rel="noopener" data-umami-event="pdf-ficha">📄 Descargar PDF para imprimir</a></div>\n'
           f'<section class="pagina"><header class="banda"><div><div class="banda-t">Academia Esparta</div><div class="banda-lema">El esfuerzo de hoy es el éxito de mañana</div></div>'
           f'<div class="banda-d"><span class="pill">{asig} · {pill}</span><span class="banda-c">{curso}.º Primaria · {asig}</span></div></header>'
           f'<div class="datos"><span>Nombre: <i></i></span><span>Fecha: <i></i></span></div>'
           f'<div class="rotulo"><span>{rot}</span><b></b></div>{html_c}'
           f'<footer class="pie"><span>academiaesparta.es</span><span>{asig} · {curso}.º Primaria</span><span>Página 1 de 1</span></footer></section>\n'
           '</body>\n</html>\n')
    destino = os.path.join(RAIZ, rel)
    open(destino, 'w', encoding='utf8').write(doc)
    ud = tempfile.mkdtemp()
    pdf = os.path.join(os.path.dirname(destino), nom)
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=10000',
                    '--allow-file-access-from-files', f'--user-data-dir={ud}', f'--print-to-pdf={pdf}', 'file://' + destino], capture_output=True)
    shutil.rmtree(ud, ignore_errors=True)
    n = len(re.findall(rb'/Type\s*/Page(?!s)', open(pdf, 'rb').read()))
    print(f'{"✓" if n == 1 else "✗"} {rel} → {nom} ({n} pág.)')
    return n == 1


if __name__ == '__main__':
    rutas = sys.argv[1:] or list(FICHAS)
    ok = all([generar(r) for r in rutas])
    sys.exit(0 if ok else 1)
