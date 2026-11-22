#!/usr/bin/env python3
"""Genera la ficha de una letra de 1º de Primaria con el formato aprobado el 22-nov-2026.

Uso (desde la raíz del repo):
    python3 herramientas/fichas-letras/generar_ficha_letra.py m          # una letra
    python3 herramientas/fichas-letras/generar_ficha_letra.py m p s      # varias

Lee herramientas/fichas-letras/letras/<letra>.json y escribe:
    recursos/primaria/1/lengua/letras/<letra>.html          (página web, para Google y para verla)
    recursos/primaria/1/lengua/letras/letra-<letra>-1-primaria.pdf   (lo que imprimen los padres)

Diseño (aprobado por Miguel con la letra M): estilo de las fichas del Tutor, versión ligera de tinta,
6 páginas de fácil a difícil: presentación + rodear y contar · sílabas en pauta · palabras en pauta ·
junto sílabas · frases con caja de palabras · cuento con preguntas y dibujo. Letra Playwrite ES.

Dibujos que no existen como emoji (p. ej. la mesa): se escriben como [nombre] en el JSON y se
pintan con emoji-propios/<nombre>.svg. ¡Ojo!: comprobar que cada emoji ES esa cosa (🪑 es silla).

Después de generar: revisar el PDF a ojo y subir solo los ficheros de esa letra.
"""
import html, json, os, re, subprocess, sys, tempfile, shutil

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(RAIZ, 'recursos', 'primaria', '1', 'lengua', 'letras')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
REL = '../../../../../'          # de letras/ a la raíz del sitio
W = 673                          # ancho útil de la pauta (17,8 cm)
E = html.escape
T = 6                            # páginas


# ───────────────────────── piezas ─────────────────────────
def pauta(modelo='', gris=(), emoji='', vacia=False, hueco=150):
    """Pauta de 4 líneas: modelo en negrita verde, una copia en gris y puntos de inicio."""
    base = 52; h = base + 22
    o = [f'<svg class="pauta" viewBox="0 0 {W} {h}" width="{W}" height="{h}">',
         f'<line x1="0" y1="{base-49}" x2="{W}" y2="{base-49}" class="l-fina"/>',
         f'<line x1="0" y1="{base-20}" x2="{W}" y2="{base-20}" class="l-disc"/>',
         f'<line x1="0" y1="{base}" x2="{W}" y2="{base}" class="l-base"/>',
         f'<line x1="0" y1="{base+20}" x2="{W}" y2="{base+20}" class="l-fina"/>']
    x = 6
    if emoji:
        o.append(f'<text x="0" y="{base-2}" class="emo">{emoji}</text>'); x = 58
    if not vacia and modelo:
        o.append(f'<text x="{x}" y="{base}" class="pw modelo">{E(modelo)}</text>')
        for i, g in enumerate(gris):
            o.append(f'<text x="{x+hueco*(i+1)}" y="{base}" class="pw gris">{E(g)}</text>')
        k = len(gris) + 1
        while x + hueco*k + 30 <= W:
            o.append(f'<circle cx="{x+hueco*k+2}" cy="{base}" r="3.4" class="punto"/>'); k += 1
    o.append('</svg>'); return ''.join(o)


def mini_pauta(w, texto=''):
    base = 52; h = 74
    t = f'<text x="6" y="{base}" class="pw modelo" style="font-size:36px">{E(texto)}</text>' if texto else ''
    return (f'<svg class="mini-pauta" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<line x1="0" y1="{base-49}" x2="{w}" y2="{base-49}" class="l-fina"/><line x1="0" y1="{base-20}" x2="{w}" y2="{base-20}" class="l-disc"/>'
            f'<line x1="0" y1="{base}" x2="{w}" y2="{base}" class="l-base"/><line x1="0" y1="{base+20}" x2="{w}" y2="{base+20}" class="l-fina"/>{t}</svg>')


def cuenta(palabra, letra):
    return palabra.lower().count(letra.lower())


def rodea(palabra, letra):
    """Rodea cada aparición de la letra (vale para dígrafos: ll, ch, rr)."""
    n = len(letra); out = ''; i = 0
    while i < len(palabra):
        if palabra[i:i+n].lower() == letra.lower():
            out += f'<span class="circ">{E(palabra[i:i+n])}</span>'; i += n
        else:
            out += E(palabra[i]); i += 1
    return out


def verde(palabra, letra):
    return rodea(palabra, letra).replace('class="circ"', 'class="verde"')


def construir(d):
    L, LM = d['letra'], d['mayus']
    chip = lambda s: f'<span class="chip">{E(s)}</span>'
    EJ = lambda n, t: f'<div class="ej"><span class="ej-n">{n}</span><span>{t}</span></div>'
    MIRA = lambda c: f'<div class="mira"><div class="mira-t">Mira cómo se hace:</div>{c}</div><div class="ahora">Ahora tú:</div>'

    def pagina(n, rotulo, cuerpo):
        return (f'<section class="pagina"><header class="banda"><div><div class="banda-t">Academia Esparta</div>'
                f'<div class="banda-lema">El esfuerzo de hoy es el éxito de mañana</div></div>'
                f'<div class="banda-d"><span class="pill">Lengua · La letra {E(L)}</span><span class="banda-c">1.º Primaria · Lengua</span></div></header>'
                f'<div class="datos"><span>Nombre: <i></i></span><span>Fecha: <i></i></span></div>'
                f'<div class="rotulo"><span>{rotulo}</span><b></b></div>{cuerpo}'
                f'<footer class="pie"><span>academiaesparta.es</span><span>Lengua · 1.º Primaria</span><span>Página {n} de {T}</span></footer></section>')

    P = []
    # 1 · Presentación + rodear y contar
    it = d['intro']
    intro = ('<div class="p1-intro"><div class="intro-arriba">'
             f'<div class="intro-let"><span>{E(LM)}</span><span>{E(L)}</span></div>'
             f'<div class="intro-der"><div class="intro-tit">Vamos a trabajar la <b>{E(L)}</b></div>'
             '<div class="intro-pal">' + ''.join(f'<span class="emo-b">{e}</span><span class="pw">{verde(p, L)}</span>' for e, p in it['palabras']) + '</div>'
             f'<div class="intro-suena">{it["suena"]}</div></div></div>'
             '<div class="intro-sil"><span class="intro-lee">Lee:</span>' + ''.join(f'<span class="chip chip-g">{E(s)}</span>' for s in d['silabas']) + '</div></div>')
    r = d['rodea']
    pal1 = [x for par in zip(r['minusculas'], r['mayusculas']) for x in par]
    cu = lambda e, p, n='': (f'<div class="cu-it"><span class="emo-b">{e}</span><span class="pw cu-pal">{p}</span>'
                             f'<span class="cu-fl">→</span><span class="cu-caja pw">{n}</span></div>')
    P.append(pagina(1, f'Conozco la {E(L)}', '<div class="p1">' + intro
        + f'<div class="p1-ej"><span class="p1-num">1</span><span>Rodea la <b>{E(LM)}</b> y la <b>{E(L)}</b> en cada palabra.<br>Escribe cuántas tiene.</span></div>'
        + MIRA('<div class="cu-grid">' + ''.join(cu(e, rodea(p, L), str(cuenta(p, L))) for e, p in r['ejemplos']) + '</div>')
        + '<div class="cu-grid">' + ''.join(cu(e, E(p)) for p, e in pal1) + '</div>'
        + f'<p class="pista">Fíjate bien: en algunas palabras no hay ninguna {E(L)}. Entonces escribe 0.</p></div>'))

    # 2 · Sílabas en pauta
    ps = d['pauta_silabas']
    P.append(pagina(2, 'Repaso las sílabas', EJ(2, 'Repasa la letra y las sílabas. Después escríbelas tú empezando en cada punto.')
        + MIRA(pauta(ps['ejemplo'][0], (ps['ejemplo'][0],), ps['ejemplo'][1], hueco=120))
        + ''.join(pauta(s, (s,), e, hueco=120) for s, e in ps['filas'])
        + f'<p class="pista">{ps["pista"]}</p>'))

    # 3 · Palabras en pauta
    pp = d['pauta_palabras']
    P.append(pagina(3, f'Palabras con {E(L)}', EJ(3, 'Repasa la palabra. Después escríbela tú empezando en cada punto.')
        + MIRA(pauta(pp['ejemplo'][0], (pp['ejemplo'][0],), pp['ejemplo'][1], hueco=165))
        + ''.join(pauta(p, (p,), e, hueco=165) for p, e in pp['filas'])))

    # 4 · Junto sílabas
    j = d['junta']
    fila = lambda e, ss, res='': (f'<div class="jun"><span class="emo-b">{e}</span><span class="jun-s">' + ' + '.join(chip(s) for s in ss)
                                  + '</span><span class="jun-eq">=</span>' + mini_pauta(250, res) + '</div>')
    P.append(pagina(4, 'Junto sílabas', EJ(4, 'Junta las sílabas y escribe la palabra.')
        + MIRA(fila(j['ejemplo'][0], j['ejemplo'][1], j['ejemplo'][2]))
        + ''.join(f'<div class="jun-l"><span class="let">{"abcdefgh"[i]})</span>' + fila(e, ss) + '</div>' for i, (e, ss) in enumerate(j['filas']))))

    # 5 · Frases
    f = d['frases']
    ej = f['ejemplo']
    P.append(pagina(5, 'Frases', EJ(5, 'Completa la frase. Usa las palabras de la caja.')
        + '<div class="banco"><div class="banco-t">Palabras para usar:</div><div class="banco-fila">'
        + ''.join(f'<span class="banco-it"><span class="banco-e">{e}</span><span class="pw">{E(b)}</span></span>' for b, e in f['banco']) + '</div></div>'
        + MIRA(f'<div class="fr"><span class="emo-b">{ej[0]}</span><span class="pw fr-t">{E(ej[1])} ' + mini_pauta(150, ej[2]) + f' {E(ej[3])}</span></div>')
        + ''.join(f'<div class="fr"><span class="let">{"abcdef"[i]})</span><span class="emo-b">{e}</span><span class="pw fr-t">{E(a)} {mini_pauta(170)}'
                  f'{(" " if not b.startswith(".") else "") + E(b)}</span></div>' for i, (e, a, _sol, b) in enumerate(f['filas']))))

    # 6 · Cuento + dibujo
    c = d['cuento']
    P.append(pagina(6, 'Leo y contesto', EJ(6, 'Lee el cuento.')
        + f'<div class="cuento pw"><span class="emo-b">{c["emoji"]}</span> ' + '<br>'.join(E(x) for x in c['lineas']) + '</div>'
        + '<div class="sub pw">Rodea la buena:</div>'
        + ''.join(f'<div class="pr pw"><span class="let">{"abcdef"[i]})</span><span class="pr-q">{E(q)}</span><span>{E(a)}</span><span class="bar">/</span><span>{E(b)}</span></div>'
                  for i, (q, a, b) in enumerate(c['preguntas']))
        + f'<div class="sub pw">Ahora rodea de <span class="rojo">rojo</span> todas las <span class="rojo">{E(L)}</span> del cuento.</div>'
        + EJ(7, f'Dibuja algo que tenga la <b>{E(L)}</b> y escribe su nombre.') + '<div class="dibuja" style="height:150px"></div>' + pauta(vacia=True)
        + '<div class="fin pw">⭐ ¡Muy bien! 🏆</div>'))
    return P


def comprobar(d):
    """Que el contenido tenga sentido antes de generar (no sustituye a revisar el PDF a ojo)."""
    L = d['letra'].lower(); fallos = []
    r = d['rodea']
    if not all(p == p.lower() for p, _ in r['minusculas']): fallos.append('rodea.minusculas: hay alguna palabra con mayúsculas')
    if not all(p == p.upper() for p, _ in r['mayusculas']): fallos.append('rodea.mayusculas: hay alguna palabra con minúsculas')
    todas = r['minusculas'] + r['mayusculas']
    if not any(cuenta(p, L) == 0 for p, _ in todas): fallos.append('rodea: pon alguna palabra SIN la letra (para que se fijen)')
    if not any(cuenta(p, L) >= 2 for p, _ in todas): fallos.append('rodea: conviene alguna palabra con la letra dos veces')
    for p, _ in d['pauta_palabras']['filas'] + [d['pauta_palabras']['ejemplo']]:
        if L not in p.lower(): fallos.append(f'pauta_palabras: «{p}» no lleva la {L}')
    for e, ss in d['junta']['filas']:
        if L not in ''.join(ss).lower(): fallos.append(f'junta: «{"".join(ss)}» no lleva la {L}')
    banco = [b for b, _ in d['frases']['banco']]
    for _, _, sol, _ in d['frases']['filas']:
        if sol not in banco: fallos.append(f'frases: la solución «{sol}» no está en la caja de palabras')
    if len(set(banco)) != len(banco): fallos.append('frases: palabra repetida en la caja')
    for e in re.findall(r'\[([a-z-]+)\]', json.dumps(d, ensure_ascii=False)):
        if not os.path.exists(os.path.join(RAIZ, 'emoji-propios', e + '.svg')):
            fallos.append(f'falta el dibujo emoji-propios/{e}.svg')
    def pares(x):  # [palabra, emoji] o [emoji, palabra, ...] en cualquier sitio del JSON
        if isinstance(x, list):
            if len(x) >= 2 and all(isinstance(y, str) for y in x[:2]): yield x
            for y in x: yield from pares(y)
        elif isinstance(x, dict):
            for y in x.values(): yield from pares(y)
    for par in pares(d):
        if '🪑' in par[:2] and any('mesa' in s.lower() for s in par if isinstance(s, str)):
            fallos.append('🪑 es una SILLA, no una mesa: usa [mesa]')
    for s in ([d['pauta_silabas']['pista']] if 'pista' in d.get('pauta_silabas', {}) else []):
        if re.search(r'🪑\s*\w+ de mesa', s): fallos.append('pista: 🪑 es una SILLA, no una mesa: usa [mesa]')
    return fallos


def cabecera(d):
    L, LM = d['letra'], d['mayus']
    url = f'https://academiaesparta.es/recursos/primaria/1/lengua/letras/{L}.html'
    titulo = f'Ficha Letra {LM} · 1º Primaria'
    desc = d['descripcion']
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "LearningResource", "name": f"Letra {LM} · Ficha de la letra", "description": desc, "url": url,
         "learningResourceType": "worksheet", "educationalLevel": "1º de Primaria", "about": "Lectura · Aprendizaje de letras",
         "inLanguage": "es", "isAccessibleForFree": True, "isFamilyFriendly": True, "educationalUse": "assignment",
         "publisher": {"@type": "EducationalOrganization", "name": "Academia Esparta", "url": "https://academiaesparta.es/"},
         "typicalAgeRange": "6-7"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://academiaesparta.es/"},
            {"@type": "ListItem", "position": 2, "name": "Materiales", "item": "https://academiaesparta.es/materiales.html"},
            {"@type": "ListItem", "position": 3, "name": "Fichas de Lengua de 1º de Primaria", "item": "https://academiaesparta.es/recursos/primaria/1/lengua/"},
            {"@type": "ListItem", "position": 4, "name": f"Letra {LM}", "item": url}]}]}
    return (f'  <title>{E(titulo)}</title>\n  <meta name="description" content="{E(desc)}">\n  <link rel="canonical" href="{url}">\n'
            f'  <meta property="og:type" content="article">\n  <meta property="og:site_name" content="Academia Esparta">\n'
            f'  <meta property="og:title" content="Letra {E(LM)} · Ficha de la letra · Lengua 1º Primaria">\n'
            f'  <meta property="og:description" content="{E(desc)}">\n  <meta property="og:url" content="{url}">\n'
            f'  <meta property="og:image" content="https://academiaesparta.es/og-image.jpg">\n'
            f'  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')


def generar(letra):
    d = json.load(open(os.path.join(AQUI, 'letras', f'{letra}.json'), encoding='utf8'))
    fallos = comprobar(d)
    if fallos:
        print(f'✗ {letra}: no se genera'); [print('   -', x) for x in fallos]; return False
    L = d['letra']; pdf = f'letra-{L}-1-primaria.pdf'
    css = open(os.path.join(AQUI, 'estilo.css'), encoding='utf8').read()
    doc = ('<!DOCTYPE html>\n<html lang="es">\n<head>\n  <meta charset="UTF-8" />\n  <meta name="viewport" content="width=820" />\n'
           + cabecera(d) + f'  <style>{css}</style>\n</head>\n<body>\n'
           f'<div class="topbar"><a class="back-btn" href="{REL}materiales.html">← Volver</a>'
           f'<a class="pdf-btn" href="{pdf}" target="_blank" rel="noopener" data-umami-event="pdf-letra">📄 Descargar PDF para imprimir</a></div>\n'
           + ''.join(construir(d)) + '\n</body>\n</html>\n')
    # dibujos propios: [nombre] → emoji-propios/nombre.svg
    doc = re.sub(r'<text x="([0-9.]+)" y="([0-9.]+)" class="emo">\[([a-z-]+)\]</text>',
                 lambda m: f'<image href="{REL}emoji-propios/{m.group(3)}.svg" x="{m.group(1)}" y="{float(m.group(2))-36}" width="44" height="44"/>', doc)
    doc = re.sub(r'\[([a-z-]+)\]', lambda m: f'<img class="emo-img" src="{REL}emoji-propios/{m.group(1)}.svg" alt="{m.group(1)}">', doc)
    ruta = os.path.join(SALIDA, f'{L}.html')
    open(ruta, 'w', encoding='utf8').write(doc)
    ud = tempfile.mkdtemp()
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=8000',
                    '--allow-file-access-from-files', f'--user-data-dir={ud}', f'--print-to-pdf={os.path.join(SALIDA, pdf)}',
                    'file://' + ruta], capture_output=True)
    shutil.rmtree(ud, ignore_errors=True)
    n = len(re.findall(rb'/Type\s*/Page(?!s)', open(os.path.join(SALIDA, pdf), 'rb').read()))
    print(f'✓ {letra}: {L}.html + {pdf} ({n} páginas{"" if n == T else " — ¡OJO, se esperaban " + str(T) + "!"})')
    return n == T


if __name__ == '__main__':
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    ok = all([generar(x) for x in sys.argv[1:]])
    sys.exit(0 if ok else 1)
