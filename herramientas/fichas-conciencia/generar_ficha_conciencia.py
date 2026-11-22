#!/usr/bin/env python3
"""Fichas de Conciencia fonológica de 1º de Primaria con el formato nuevo (página + PDF, 22-nov-2026).

Uso (desde la raíz del repo):
    python3 herramientas/fichas-conciencia/generar_ficha_conciencia.py reconocer-sonidos

Lee herramientas/fichas-conciencia/fichas/<nombre>.json y escribe, con la MISMA dirección de siempre:
    recursos/primaria/1/lengua/conciencia-fonologica/<nombre>.html
    recursos/primaria/1/lengua/conciencia-fonologica/<nombre>-1-primaria.pdf

Reutiliza el estilo de las letras (herramientas/fichas-letras/estilo.css) + extra.css de esta carpeta.
Cada tipo de página es una función de PAGINAS; el JSON dice qué páginas lleva la ficha y con qué datos.
Antes de generar se comprueba el contenido (cuentas de palabras, sílabas, palabras escondidas…).
Después: revisar el PDF a ojo.
"""
import html, json, os, re, subprocess, sys, tempfile, shutil

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(RAIZ, 'recursos', 'primaria', '1', 'lengua', 'conciencia-fonologica')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
REL = '../../../../../'
E = html.escape
LET = 'abcdefgh'
VOC = 'aeiouáéíóúü'


# ───────────────────────── utilidades ─────────────────────────
_T = str.maketrans('áéíóúü', 'aeiouu')
def pleg(t):
    return t.lower().translate(_T)


def palabras(frase):
    return re.findall(r"[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]+", frase)


def silabas(p):
    """Recuento de sílabas suficiente para palabras sencillas (núcleos vocálicos, diptongos con i/u átonas)."""
    p = p.lower()
    n, prev_v = 0, False
    for i, c in enumerate(p):
        v = c in VOC
        if v and not prev_v:
            n += 1
        elif v and prev_v:
            a, b = p[i - 1], c
            fuertes = 'aeoáéó'
            if (a in fuertes and b in fuertes) or (a in 'íú' or b in 'íú'):
                n += 1          # hiato
        prev_v = v
    return n


def bolas(n_total, pintadas=0):
    return '<span class="bolas">' + ''.join(
        f'<span class="bola{" on" if i < pintadas else ""}"></span>' for i in range(n_total)) + '</span>'


EJ = lambda n, t: f'<div class="ej"><span class="ej-n">{n}</span><span>{t}</span></div>'
MIRA = lambda c: f'<div class="mira"><div class="mira-t">Mira cómo se hace:</div>{c}</div><div class="ahora">Ahora tú:</div>'


# ───────────────────────── tipos de página ─────────────────────────
def p_contar(d, n):
    """Escucha la frase y pinta un círculo por cada palabra."""
    fila = lambda e, f, pint=0, let='': (
        f'<div class="cf">{let}<span class="emo-b">{e}</span><span class="pw cf-t">{E(f)}</span>{bolas(d["max"], pint)}</div>')
    ej = d['ejemplo']
    return (EJ(n, d['enunciado'])
            + MIRA(fila(ej[0], ej[1], len(palabras(ej[1]))))
            + ''.join(fila(e, f, 0, f'<span class="let">{LET[i]})</span>') for i, (e, f) in enumerate(d['filas']))
            + f'<p class="pista">{d["pista"]}</p>')


def p_largas(d, n):
    """Rodea la palabra más larga (la que tarda más en decirse)."""
    par = lambda a, b, marca=None, let='': (
        f'<div class="lc">{let}' + ''.join(
            f'<span class="lc-it{" circ-b" if marca == k else ""}"><span class="emo-g">{e}</span><span class="pw lc-p">{E(p)}</span></span>'
            + ('<span class="lc-o">o</span>' if k == 0 else '') for k, (e, p) in enumerate((a, b))) + '</div>')
    ej = d['ejemplo']
    larga = lambda a, b: 0 if silabas(a[1]) > silabas(b[1]) else 1
    out = (EJ(n, d['enunciado'])
           + MIRA(par(ej[0], ej[1], larga(ej[0], ej[1])))
           + '<div class="lc-grid">' + ''.join(par(a, b, None, f'<span class="let">{LET[i]})</span>') for i, (a, b) in enumerate(d['filas'])) + '</div>'
           + f'<p class="pista">{d["pista"]}</p>')
    if d.get('dibuja'):
        out += (EJ(n + 1, d['dibuja']) + '<div class="dib2"><div><div class="dib2-t pw">nombre corto</div><div class="dibuja"></div></div>'
                '<div><div class="dib2-t pw">nombre largo</div><div class="dibuja"></div></div></div>')
    return out


def p_escondidas(d, n):
    """Dentro de una palabra larga se esconde otra: rodea su dibujo."""
    fila = lambda e, p, ops, marca=None, let='': (
        f'<div class="esc">{let}<span class="esc-c"><span class="emo-g">{e}</span><span class="pw esc-p">{E(p)}</span></span><span class="esc-fl">→</span>'
        + ''.join(f'<span class="esc-op{" circ-b" if marca == o else ""}">{o}</span>' for o in ops) + '</div>')
    ej = d['ejemplo']
    return (EJ(n, d['enunciado'])
            + MIRA(fila(ej['emoji'], ej['palabra'], ej['opciones'], ej['opciones'][ej['buena']]))
            + ''.join(fila(f['emoji'], f['palabra'], f['opciones'], None, f'<span class="let">{LET[i]})</span>') for i, f in enumerate(d['filas']))
            + f'<p class="pista">{d["pista"]}</p>')


def p_frases(d, n):
    """Rodea la frase más larga y pinta un círculo por cada palabra."""
    def par(a, b, ej=False, let=''):
        larga = 0 if len(palabras(a)) > len(palabras(b)) else 1
        return (f'<div class="fl">{let}<div class="fl-col">' + ''.join(
            f'<div class="fl-it"><span class="pw fl-t{" circ-r" if ej and k == larga else ""}">{E(f)}</span>'
            f'{bolas(d["max"], len(palabras(f)) if ej else 0)}</div>' for k, f in enumerate((a, b))) + '</div></div>')
    ej = d['ejemplo']
    out = (EJ(n, d['enunciado']) + MIRA(par(ej[0], ej[1], True))
           + ''.join(par(a, b, False, f'<span class="let">{LET[i]})</span>') for i, (a, b) in enumerate(d['filas'])))
    if d.get('inventa'):
        iv = d['inventa']
        out += (EJ(n + 1, iv['enunciado']) + f'<div class="inv"><span class="inv-e">{iv["emoji"]}</span>'
                f'<div class="inv-d"><div class="inv-t pw">Mi frase tiene:</div>{bolas(d["max"])}</div></div>')
    return out


PAGINAS = {'contar': p_contar, 'largas': p_largas, 'escondidas': p_escondidas, 'frases': p_frases}
import fonologia as FO   # noqa: E402  fichas 2-5: rimas, sílabas, jugar con sílabas, sonidos
PAGINAS.update(FO.PAGINAS)


# ───────────────────────── comprobaciones ─────────────────────────
def comprobar(d):
    f = []
    for pg in d['paginas']:
        t = pg['tipo']
        if t in FO.PAGINAS:
            f += FO.comprobar(pg); continue
        if t == 'contar':
            ns = [len(palabras(fr)) for _, fr in pg['filas']]
            if max(ns + [len(palabras(pg['ejemplo'][1]))]) > pg['max']: f.append('contar: alguna frase tiene más palabras que círculos')
            if len(set(ns)) < 3: f.append(f'contar: poca variedad de longitudes {ns}')
            if any(b - a == 1 for a, b in zip(ns, ns[1:])) and ns == sorted(ns): f.append('contar: van en orden creciente, se adivina')
            if len(palabras(pg['ejemplo'][1])) in ns[:1]: f.append('contar: la primera frase tiene las mismas palabras que el ejemplo')
            for _, fr in pg['filas']:
                if re.search(r"\b(al|del)\b", fr, re.I): f.append(f'contar: «{fr}» lleva al/del (contracción, confunde)')
        if t == 'largas':
            lados = []
            for a, b in pg['filas'] + [pg['ejemplo']]:
                sa, sb = silabas(a[1]), silabas(b[1])
                if abs(sa - sb) < 2: f.append(f'largas: «{a[1]}» ({sa}) y «{b[1]}» ({sb}) se parecen demasiado en largo')
            for a, b in pg['filas']:
                lados.append(0 if silabas(a[1]) > silabas(b[1]) else 1)
            if len(set(lados)) == 1: f.append('largas: la larga cae siempre en el mismo lado')
            if 'trampa' in pg:   # índices de filas donde la cosa grande tiene el nombre corto
                if len(pg['trampa']) < len(pg['filas']) // 2: f.append('largas: pocas filas donde lo grande tiene nombre corto')
        if t == 'escondidas':
            for fl in pg['filas'] + [pg['ejemplo']]:
                esc = fl['escondida']
                if pleg(esc) not in pleg(fl['palabra']): f.append(f'escondidas: «{esc}» no está dentro de «{fl["palabra"]}»')
                if len(fl['opciones']) != 3: f.append(f'escondidas: «{fl["palabra"]}» necesita 3 opciones')
                if fl['opciones'][fl['buena']] != fl['opcion_buena_emoji']: f.append(f'escondidas: la buena de «{fl["palabra"]}» no cuadra')
            buenas = [fl['buena'] for fl in pg['filas']]
            if len(set(buenas)) == 1: f.append('escondidas: la buena está siempre en la misma posición')
        if t == 'frases':
            lados = []
            for a, b in pg['filas'] + [pg['ejemplo']]:
                na, nb = len(palabras(a)), len(palabras(b))
                if na == nb: f.append(f'frases: «{a}» y «{b}» tienen las mismas palabras')
                if max(na, nb) > pg['max']: f.append('frases: más palabras que círculos')
            lados = [0 if len(palabras(a)) > len(palabras(b)) else 1 for a, b in pg['filas']]
            if len(set(lados)) == 1: f.append('frases: la larga va siempre en el mismo sitio')
    return f


# ───────────────────────── página y documento ─────────────────────────
def documento(d):
    T = len(d['paginas'])
    def pagina(i, rotulo, cuerpo):
        return (f'<section class="pagina"><header class="banda"><div><div class="banda-t">Academia Esparta</div>'
                f'<div class="banda-lema">El esfuerzo de hoy es el éxito de mañana</div></div>'
                f'<div class="banda-d"><span class="pill">Lengua · Conciencia fonológica</span><span class="banda-c">1.º Primaria · Lengua</span></div></header>'
                f'<div class="datos"><span>Nombre: <i></i></span><span>Fecha: <i></i></span></div>'
                f'<div class="rotulo"><span>{E(rotulo)}</span><b></b></div>{cuerpo}'
                f'<footer class="pie"><span>academiaesparta.es</span><span>Lengua · 1.º Primaria</span><span>Página {i} de {T}</span></footer></section>')
    out, n = [], 1
    for i, pg in enumerate(d['paginas'], 1):
        cuerpo = PAGINAS[pg['tipo']](pg, n)
        n += 1 + (1 if pg.get('dibuja') or pg.get('inventa') else 0)
        if i == 1 and d.get('adulto'):
            cuerpo = f'<div class="adulto">{d["adulto"]}</div>' + cuerpo
        if i == T and d.get('fin', True):
            cuerpo += '<div class="fin pw">⭐ ¡Muy bien! 🏆</div>'
        out.append(pagina(i, pg['rotulo'], cuerpo))
    return out


def cabecera(d):
    url = f'https://academiaesparta.es/recursos/primaria/1/lengua/conciencia-fonologica/{d["archivo"]}.html'
    desc = d['descripcion']
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "LearningResource", "name": d['titulo_corto'], "description": desc, "url": url,
         "learningResourceType": "worksheet", "educationalLevel": "1º de Primaria", "about": "Lectura · Conciencia fonológica",
         "inLanguage": "es", "isAccessibleForFree": True, "isFamilyFriendly": True, "educationalUse": "assignment",
         "publisher": {"@type": "EducationalOrganization", "name": "Academia Esparta", "url": "https://academiaesparta.es/"},
         "typicalAgeRange": "6-7"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://academiaesparta.es/"},
            {"@type": "ListItem", "position": 2, "name": "Materiales", "item": "https://academiaesparta.es/materiales.html"},
            {"@type": "ListItem", "position": 3, "name": "Fichas de Lengua de 1º de Primaria", "item": "https://academiaesparta.es/recursos/primaria/1/lengua/"},
            {"@type": "ListItem", "position": 4, "name": d['titulo_corto'], "item": url}]}]}
    return (f'  <title>{E(d["titulo"])}</title>\n  <meta name="description" content="{E(desc)}">\n  <link rel="canonical" href="{url}">\n'
            f'  <meta property="og:type" content="article">\n  <meta property="og:site_name" content="Academia Esparta">\n'
            f'  <meta property="og:title" content="{E(d["titulo"])}">\n'
            f'  <meta property="og:description" content="{E(desc)}">\n  <meta property="og:url" content="{url}">\n'
            f'  <meta property="og:image" content="https://academiaesparta.es/og-image.jpg">\n'
            f'  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')


def generar(nombre):
    d = json.load(open(os.path.join(AQUI, 'fichas', f'{nombre}.json'), encoding='utf8'))
    fallos = comprobar(d)
    if fallos:
        print(f'✗ {nombre}: no se genera'); [print('   -', x) for x in fallos]; return False
    A = d['archivo']; pdf = f'{A}-1-primaria.pdf'
    css = (open(os.path.join(RAIZ, 'herramientas', 'fichas-letras', 'estilo.css'), encoding='utf8').read()
           + open(os.path.join(AQUI, 'extra.css'), encoding='utf8').read())
    doc = ('<!DOCTYPE html>\n<html lang="es">\n<head>\n  <meta charset="UTF-8" />\n  <meta name="viewport" content="width=820" />\n'
           + cabecera(d) + f'  <style>{css}</style>\n</head>\n<body>\n'
           f'<div class="topbar"><a class="back-btn" href="{REL}materiales.html">← Volver</a>'
           f'<a class="pdf-btn" href="{pdf}" target="_blank" rel="noopener" data-umami-event="pdf-conciencia">📄 Descargar PDF para imprimir</a></div>\n'
           + ''.join(documento(d)) + '\n</body>\n</html>\n')
    ruta = os.path.join(SALIDA, f'{A}.html')
    open(ruta, 'w', encoding='utf8').write(doc)
    ud = tempfile.mkdtemp()
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=8000',
                    '--allow-file-access-from-files', f'--user-data-dir={ud}', f'--print-to-pdf={os.path.join(SALIDA, pdf)}',
                    'file://' + ruta], capture_output=True)
    shutil.rmtree(ud, ignore_errors=True)
    n = len(re.findall(rb'/Type\s*/Page(?!s)', open(os.path.join(SALIDA, pdf), 'rb').read()))
    T = len(d['paginas'])
    print(f'✓ {nombre}: {A}.html + {pdf} ({n} páginas{"" if n == T else " — ¡OJO, se esperaban " + str(T) + "!"})')
    return n == T


if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    sys.exit(0 if all([generar(x) for x in sys.argv[1:]]) else 1)
