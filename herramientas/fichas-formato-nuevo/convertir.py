#!/usr/bin/env python3
"""Pasa fichas antiguas de 1º y 2º de Primaria al formato nuevo (el de las letras, 22-nov-2026).

El CONTENIDO no se toca: mismos textos, mismas preguntas, mismo orden. Solo cambia el formato:
chasis de herramientas/fichas-letras/estilo.css (cabecera «Academia Esparta», Nombre/Fecha,
pie «Página X de Y»), todo en letra ligada Playwrite ES, + PDF con Chrome + botón de descarga.
Misma dirección que la ficha antigua.

Dos pasos (desde la raíz del repo):
    python3 herramientas/fichas-formato-nuevo/convertir.py extraer  recursos/primaria/1/lengua/comprension/b.html ...
    python3 herramientas/fichas-formato-nuevo/convertir.py generar  recursos/primaria/1/lengua/comprension/b.html ...
    python3 herramientas/fichas-formato-nuevo/convertir.py todo     <fichas>      (extraer si falta + generar)

«extraer» guarda el contenido de la ficha ANTIGUA en datos/<ruta>.json (solo si no existe:
una vez convertida, el HTML ya no es el antiguo). «generar» escribe la página y el PDF desde el JSON.
"""
import html, json, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chasis, extras_mates

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, 'datos')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CSS_BASE = os.path.join(RAIZ, 'herramientas', 'fichas-letras', 'estilo.css')
CSS_EXTRA = os.path.join(AQUI, 'extra.css')
W = 673
E = html.escape


def limpia(t):
    """Texto interior de la ficha antigua: espacios colapsados, se conservan <strong>/<b> y entidades."""
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def quita_emoji_inicial(t):
    return re.sub(r'^[^\wÁÉÍÓÚÑáéíóúñ¿¡<]+', '', t).strip()


# ───────────────────────── extraer (ficha antigua → dict) ─────────────────────────
def extraer_cabecera(s):
    head = s.split('</head>')[0]
    head = re.sub(r'<style>.*?</style>', '', head, flags=re.S)
    lineas = []
    for m in re.finditer(r'<(title|script)\b[^>]*>.*?</\1>|<(?:meta|link)\b[^>]*>', head, flags=re.S):
        x = m.group(0)
        if 'charset' in x or 'name="viewport"' in x: continue
        if 'fonts.googleapis' in x or 'fonts.gstatic' in x: continue
        lineas.append(x.strip())
    return lineas


def extraer(ruta):
    s = open(ruta, encoding='utf8').read()
    body = re.sub(r'<style>.*?</style>', '', s.split('</head>', 1)[1], flags=re.S)
    d = {'origen': os.path.relpath(ruta, RAIZ), 'cabecera': extraer_cabecera(s)}
    d['ref'] = limpia(re.search(r'class="ficha-ref">(.*?)</span>', body, re.S).group(1))
    if 'class="ej-block"' in body or '/matematicas/' in ruta:
        return chasis.extraer_chasis(s, d)
    d['titulos'] = [quita_emoji_inicial(limpia(re.sub(r'<span class="ej-n">.*?</span>', '', t)))
                    for t in re.findall(r'class="seccion-titulo">(.*?)</div>', body, re.S)]
    if 'pregunta-row' in body:                                   # comprension (V/F)
        d['plantilla'] = 'vf'
        d['emoji'] = limpia(re.search(r'class="texto-emoji">(.*?)</span>', body, re.S).group(1))
        d['texto'] = [limpia(x) for x in re.findall(r'class="texto-frase">(.*?)</span>', body, re.S)]
        d['vf'] = [limpia(x) for x in re.findall(r'class="pregunta-texto">(.*?)</span>', body, re.S)]
    elif 'pregunta-mc' in body:                                  # comprension-opciones
        d['plantilla'] = 'opciones'
        d['emoji'] = limpia(re.search(r'class="texto-emoji">(.*?)</span>', body, re.S).group(1))
        d['texto'] = [limpia(x) for x in re.findall(r'class="texto-frase">(.*?)</span>', body, re.S)]
        d['preguntas'] = []
        for blq in body.split('<div class="pregunta-mc">')[1:]:
            q = limpia(re.search(r'class="pregunta-enunciado">(.*?)</div>', blq, re.S).group(1))
            ops = [limpia(x) for x in re.findall(r'<span>(.*?)</span>', blq, re.S)]
            d['preguntas'].append([q, ops])
        d['rodea'] = [limpia(x) for x in re.findall(r'class="palabra-rodea">(.*?)</div>', body, re.S)]
    elif 'completa-frase' in body:                               # lectura-frase
        d['plantilla'] = 'lectura'
        par = re.search(r'class="texto-parrafo">(.*?)</p>', body, re.S).group(1)
        d['texto'] = [limpia(x) for x in re.split(r'<br\s*/?>', par) if limpia(x)]
        d['preguntas'] = [limpia(x) for x in re.findall(r'class="pregunta-texto">(.*?)</div>', body, re.S)]
        d['completa'] = [limpia(x) for x in re.findall(r'class="completa-frase">(.*?)</div>', body, re.S)]
    else:
        raise SystemExit(f'✗ {ruta}: plantilla desconocida')
    return d


def comprobar_extraccion(d, ruta):
    """Que no se haya perdido nada al leer la ficha antigua."""
    s = open(ruta, encoding='utf8').read()
    f = []
    n = lambda c: s.count(f'class="{c}"')
    if d['plantilla'] == 'vf':
        if len(d['texto']) != n('texto-frase') or len(d['vf']) != n('pregunta-row'): f.append('faltan frases o V/F')
    if d['plantilla'] == 'opciones':
        if len(d['preguntas']) != n('pregunta-mc'): f.append('faltan preguntas')
        if sum(len(o) for _, o in d['preguntas']) != n('opcion'): f.append('faltan opciones')
        if len(d['rodea']) != n('palabra-rodea'): f.append('faltan palabras de rodear')
    if d['plantilla'] == 'lectura':
        if len(d['preguntas']) != n('pregunta-item') or len(d['completa']) != n('completa-item'): f.append('faltan preguntas/completa')
    if d['plantilla'] == 'chasis':
        sin = lambda x: re.sub(r'\s+', '', re.sub(r'<[^>]+>', '', x))
        mid = re.split(r'<hr class="separador"\s*/?>', re.sub(r'<style>.*?</style>', '', s, flags=re.S), 1)[1]
        mid = mid[:mid.rindex('<div class="footer">')]
        if sin(mid) != sin(d['badge'] + ''.join(d['bloques'])): f.append('se ha perdido texto al trocear')
        return f
    if not d['texto']: f.append('sin texto')
    return f


# ───────────────────────── piezas del formato nuevo ─────────────────────────
def pauta_vacia(w=W):
    base = 52; h = 74
    return (f'<svg class="pauta" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="none">'
            f'<line x1="0" y1="{base-49}" x2="{w}" y2="{base-49}" class="l-fina"/><line x1="0" y1="{base-20}" x2="{w}" y2="{base-20}" class="l-disc"/>'
            f'<line x1="0" y1="{base}" x2="{w}" y2="{base}" class="l-base"/><line x1="0" y1="{base+20}" x2="{w}" y2="{base+20}" class="l-fina"/></svg>')


def mini_pauta(w):
    base = 52; h = 74
    return (f'<svg class="mini-pauta" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<line x1="0" y1="{base-49}" x2="{w}" y2="{base-49}" class="l-fina"/><line x1="0" y1="{base-20}" x2="{w}" y2="{base-20}" class="l-disc"/>'
            f'<line x1="0" y1="{base}" x2="{w}" y2="{base}" class="l-base"/><line x1="0" y1="{base+20}" x2="{w}" y2="{base+20}" class="l-fina"/></svg>')


def ej(n, t):
    return f'<div class="ej"><span class="ej-n">{n}</span><span>{t}</span></div>'


def info(d):
    """Curso, asignatura, bloque y etiqueta, sacados de la ruta y de la referencia antigua."""
    partes = d['origen'].split('/')          # recursos/primaria/1/lengua/<bloque>/<archivo>
    curso, asig = partes[2], partes[3]
    trozos = [x.strip() for x in d['ref'].split('·')]
    bloque = trozos[2] if len(trozos) > 2 else ''
    etiqueta = ' · '.join(trozos[3:])
    if d.get('plantilla') == 'chasis' and d.get('badge'):
        etiqueta = re.sub(r'^[^\wÁÉÍÓÚÑáéíóúñ¿¡]+', '', d['badge'])
    return curso, asig, bloque, etiqueta


def ejercicios(d):
    if d['plantilla'] == 'chasis':
        chasis.PAUTA = re.sub(r' width="\d+" height="\d+"', '', pauta_vacia().replace('class="pauta"', 'class="pb-pauta"'))
        return chasis.ejercicios_chasis(d, ej)
    return ejercicios_texto(d)


def ejercicios_texto(d):
    """Lista de ejercicios: cabecera + clase de la lista + piezas. Una pieza nunca se parte;
    una lista sí puede seguir en la página siguiente (pieza a pieza)."""
    T = d['titulos']
    texto_box = ('<div class="cuento pw lect">' + (f'<span class="emo-b">{d["emoji"]}</span>' if d.get('emoji') else '')
                 + '<div>' + '<br>'.join(d['texto']) + '</div></div>')
    o = [(ej(1, T[0]), 'txt-w', [texto_box])]
    if d['plantilla'] == 'vf':
        o.append((ej(2, T[1]), 'vf-lista', [
            f'<div class="vf-it pw"><span class="let">{i+1}.</span><span class="vf-t">{q}</span>'
            f'<span class="vf-c">V</span><span class="vf-c">F</span></div>' for i, q in enumerate(d['vf'])]))
    elif d['plantilla'] == 'opciones':
        o.append((ej(2, T[1]), 'mc-lista', [
            f'<div class="mc-it pw"><div class="mc-q">{q}</div><div class="mc-ops">'
            + ''.join(f'<span class="mc-op"><span class="mc-o"></span>{x}</span>' for x in ops) + '</div></div>'
            for q, ops in d['preguntas']]))
        o.append((ej(3, T[2]), 'rod-w', ['<div class="rod-lista">' + ''.join(f'<span class="rod-p pw">{x}</span>' for x in d['rodea']) + '</div>']))
    elif d['plantilla'] == 'lectura':
        o.append((ej(2, T[1]), 'pr-lista', [
            f'<div class="pa-it"><div class="pa-q pw">{q}</div>{pauta_vacia()}</div>' for q in d['preguntas']]))
        o.append((ej(3, T[2]), 'co-lista', [
            '<div class="co-it pw">' + q.replace('<span class="hueco"></span>', mini_pauta(170)) + '</div>' for q in d['completa']]))
    return o


# ───────────── ejercicios nuevos para llenar la 2.ª página (sacados del propio texto) ─────────────
import random
_TIL = str.maketrans('áéíóúüÁÉÍÓÚÜ', 'aeiouuAEIOUU')


def texto_plano(t):
    return html.unescape(re.sub(r'<[^>]+>', '', t)).strip()


def frases_para_ordenar(d, n=2):
    """Frases del texto de 4 a 7 palabras, con las palabras desordenadas (nunca en el orden bueno)."""
    out = []
    for f in d['texto']:
        for fr in re.split(r'(?<=[.!?])\s+', texto_plano(f)):
            pal = fr.rstrip('.!?').split()
            if 4 <= len(pal) <= 7 and fr not in [x[0] for x in out]:
                rnd = random.Random(fr)
                mez = pal[:]
                while mez == pal or mez[0] == pal[0]:
                    rnd.shuffle(mez)
                out.append((fr, mez))
    # repartidas por el texto: no las dos primeras
    if len(out) > n:
        paso = len(out) / n
        out = [out[int(k * paso + paso / 2)] for k in range(n)]
    return out[:n]


def letra_de(d):
    m = re.search(r'Letra ([A-ZÑ]{1,2})\b', d['ref'])
    return m.group(1).lower() if m else None


def palabras_con(d, L):
    vistas = []
    for f in d['texto']:
        for p in re.findall(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+', texto_plano(f)):
            if L in p.lower().translate(_TIL) and p.lower() not in [v.lower() for v in vistas]:
                vistas.append(p)
    return vistas


def extras(d, n0):
    """Ejercicios nuevos, numerados a continuación (n0 = nº del primero)."""
    o = []; n = n0
    fr = frases_para_ordenar(d)
    if fr:
        o.append((ej(n, 'Ordena las palabras y escribe la frase.'), 'or-lista', [
            '<div class="or-it"><div class="or-chips">' + ''.join(f'<span class="chip pw or-c">{E(w)}</span>' for w in mez)
            + f'</div>{pauta_vacia()}</div>' for _, mez in fr])); n += 1
    L = letra_de(d)
    if L and len(palabras_con(d, L)) >= 3:
        o.append((ej(n, f'Escribe tres palabras del texto que tengan la <b>{E(L)}</b>.'), 'pc-w', [pauta_vacia() + pauta_vacia()])); n += 1
    return o, n


def dibuja(n, alto, texto='Dibuja lo que pasa en el texto.'):
    return (ej(n, texto), 'dib-w', [f'<div class="dibuja" style="height:{int(alto)}px"></div>'])


def solo_modelo(pz):
    """Un ejercicio nuevo que se ha quedado solo con su fila de modelo no sirve: fuera entero."""
    return len(pz) == 1 and 'xm-mira-t' in pz[0]


def caja(cls):
    """Contenedor de una lista: «mz problemas» = escala de Mates + la clase antigua dentro."""
    if cls.startswith('mz '):
        return f'<div class="mz"><div class="{cls[3:]}">', '</div></div>'
    return f'<div class="{cls}">', '</div>'


def montar(trozos):
    """trozos = [(nº ejercicio, con_cabecera, [piezas])] → HTML de una página."""
    return ''.join(f'<div class="ej-blq">{cab if con else ""}{caja(cls)[0]}{"".join(piezas)}{caja(cls)[1]}</div>'
                   for cab, cls, con, piezas in trozos)


MEDIR_JS = """<script>window.addEventListener('load',()=>{document.fonts.ready.then(()=>{
const pg=document.querySelector('.pagina'),P=pg.getBoundingClientRect().top;
const u=[...document.querySelectorAll('[data-u]')].map(e=>{const r=e.getBoundingClientRect();return [e.dataset.u,r.top-P,r.bottom-P]});
const lim=pg.getBoundingClientRect().right-pg.offsetWidth/21*1.6+2;let des=0;
pg.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>0&&r.right>lim)des=Math.max(des,r.right-lim)});
const pie=document.querySelector('.pie').offsetHeight, fin=document.querySelector('.fin').getBoundingClientRect();
const pre=document.createElement('pre');pre.id='alturas';pre.textContent=JSON.stringify({u,des,pie,fin:fin.height+26,cm:pg.offsetWidth/21});
document.body.appendChild(pre);});});</script>"""


def paginar(d, doc_medida, carpeta):
    """Mide con Chrome cada pieza y reparte en páginas llenando cada una."""
    prueba = os.path.join(carpeta, '.mide.html')
    open(prueba, 'w', encoding='utf8').write(doc_medida)
    ud = tempfile.mkdtemp()
    r = subprocess.run([CHROME, '--headless', '--disable-gpu', '--virtual-time-budget=8000', '--allow-file-access-from-files',
                        f'--user-data-dir={ud}', '--window-size=1000,4000', '--dump-dom', 'file://' + prueba], capture_output=True, text=True)
    shutil.rmtree(ud, ignore_errors=True); os.remove(prueba)
    m = json.loads(html.unescape(re.search(r'<pre id="alturas">(.*?)</pre>', r.stdout, re.S).group(1)))
    cm = m['cm']
    u = m['u']                                    # [id, top, bottom] en orden de documento
    alto = []
    for k, (uid, top, bot) in enumerate(u):
        sig = u[k+1][1] if k + 1 < len(u) else bot + 30
        alto.append((uid, sig - top))
    y0 = u[0][1]
    limite = 29.7 * cm - 0.8 * cm - m['pie'] - 30
    paginas, libres, actual, y = [], [], [], y0
    for k, (uid, h) in enumerate(alto):
        extra = alto[k+1][1] if uid.startswith('c') and k + 1 < len(alto) else 0   # cabecera pegada a su 1.ª pieza
        if actual and y + h + extra > limite:
            paginas.append(actual); libres.append(limite - y); actual, y = [], y0
        actual.append(uid); y += h
    paginas.append(actual); libres.append(limite - y)
    DESBORDE[0] = m['des']
    return paginas, libres, m['fin']


def pagina(d, n, T, contenido):
    curso, asig, bloque, etiqueta = info(d)
    A = 'Lengua' if asig == 'lengua' else 'Matemáticas'
    return (f'<section class="pagina"><header class="banda"><div><div class="banda-t">Academia Esparta</div>'
            f'<div class="banda-lema">El esfuerzo de hoy es el éxito de mañana</div></div>'
            f'<div class="banda-d"><span class="pill">{A} · {E(bloque)}</span><span class="banda-c">{curso}.º Primaria · {A}</span></div></header>'
            f'<div class="datos"><span>Nombre: <i></i></span><span>Fecha: <i></i></span></div>'
            f'<div class="rotulo"><span>{E(etiqueta)}</span><b></b></div>{contenido}'
            + ('<div class="fin pw">⭐ ¡Buen trabajo!</div>' if n == T and FIN[0] else '') +
            f'<footer class="pie"><span>academiaesparta.es</span><span>{A} · {curso}.º Primaria</span><span>Página {n} de {T}</span></footer></section>')


def nombre_pdf(d):
    partes = d['origen'].split('/')
    base = os.path.splitext(partes[-1])[0].replace('_opciones', '')
    return f'{partes[-2]}-{base}-{partes[2]}-primaria.pdf'


def pdf(html_ruta, pdf_ruta):
    ud = tempfile.mkdtemp()
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=8000',
                    '--allow-file-access-from-files', f'--user-data-dir={ud}', f'--print-to-pdf={pdf_ruta}',
                    'file://' + html_ruta], capture_output=True)
    shutil.rmtree(ud, ignore_errors=True)
    return len(re.findall(rb'/Type\s*/Page(?!s)', open(pdf_ruta, 'rb').read()))


MIDE = '<style>@media print{.pagina{height:auto!important;min-height:0!important;overflow:visible!important}}</style>'


FIN = [True]
DESBORDE = [0]
ZOOM = [1.12]


def generar(ruta):
    for z in (1.12, 1.0, 0.9, 0.8):
        ZOOM[0] = z
        r = generar_una(ruta)
        if r != 'desborda': return r
    print(f'✗ {ruta}: se sale por la derecha incluso al 80 %'); return False


def generar_una(ruta):
    rel = os.path.relpath(os.path.abspath(ruta), RAIZ)
    jd = os.path.join(DATOS, os.path.splitext(rel)[0] + '.json')
    d = json.load(open(jd, encoding='utf8'))
    prof = rel.count('/')                  # recursos/primaria/1/lengua/bloque/x.html → 5
    REL = '../' * prof
    css = open(CSS_BASE, encoding='utf8').read().replace('../../../../../fuentes/', REL + 'fuentes/')
    css += open(CSS_EXTRA, encoding='utf8').read()
    if d['plantilla'] == 'chasis': css += chasis.css_ficha(d, REL).replace('.mz{zoom:1.12;', '.mz{zoom:%s;' % ZOOM[0])
    nom = nombre_pdf(d)
    destino = os.path.join(RAIZ, rel)
    carpeta = os.path.dirname(destino)
    EJ = ejercicios(d)

    def documento(paginas_html, extra_head=''):
        T = len(paginas_html)
        return ('<!DOCTYPE html>\n<html lang="es">\n<head>\n  <meta charset="UTF-8" />\n  <meta name="viewport" content="width=820" />\n'
                + ''.join('  ' + x + '\n' for x in d['cabecera']) + f'  <style>{css}</style>{extra_head}\n</head>\n<body>\n'
                f'<div class="topbar"><a class="back-btn" href="{REL}materiales.html">← Volver</a>'
                f'<a class="pdf-btn" href="{nom}" target="_blank" rel="noopener" data-umami-event="pdf-ficha">📄 Descargar PDF para imprimir</a></div>\n'
                + ''.join(pagina(d, k+1, T, h) for k, h in enumerate(paginas_html)) + '\n</body>\n</html>\n')

    # 1) medir: todo en una página alta, cada cabecera y cada pieza marcadas
    marcado = ''.join(f'<div class="ej-blq"><div data-u="c{e}">{cab}</div><div class="{cls}">'
                      + ''.join(f'<div data-u="p{e}_{k}">{x}</div>' for k, x in enumerate(piezas)) + '</div></div>'
                      for e, (cab, cls, piezas) in enumerate(EJ))
    def medir(EJ):
        marcado = ''.join(f'<div class="ej-blq"><div data-u="c{e}">{cab}</div>{caja(cls)[0]}'
                          + ''.join(f'<div data-u="p{e}_{k}">{x}</div>' for k, x in enumerate(piezas)) + caja(cls)[1] + '</div>'
                          for e, (cab, cls, piezas) in enumerate(EJ))
        return paginar(d, documento([marcado], MIDE + MEDIR_JS), carpeta)

    FIN[0] = True
    nbase = len(EJ)
    reparto, libres, alto_fin = medir(EJ)
    if DESBORDE[0] > 1 and d['plantilla'] == 'chasis' and ZOOM[0] > 0.8: return 'desborda'
    if len(reparto) > 1:                                   # pasa a dos páginas: llenamos la última
        base = len(reparto)
        nbase = len(EJ)                                    # ejercicios de la ficha antigua (no se tocan)
        if d['plantilla'] == 'chasis':
            ultimo = max([int(x) for x in re.findall(r'<span class="ej-n">(\d+)</span>', ''.join(''.join(p) for _, _, p in EJ))] or [len(EJ)])
            d['_problemas'] = ''.join(''.join(p) for _, _, p in EJ).count('<div class="pb">')
            nuevos = extras_mates.extras(d, ultimo + 1, ej, chasis.PAUTA)
            n = ultimo + 1 + len(nuevos)
        else:
            nuevos, n = extras(d, len(EJ) + 1)
        if nuevos:
            r2, l2, _ = medir(EJ + nuevos)
            if len(r2) > base:                             # lo que no cabe, fuera (pieza a pieza)
                r2, l2 = r2[:base], l2[:base]
                usados = {u for p in r2 for u in p}
                nuevos2 = []
                for e, (cab, cls, piezas) in enumerate(nuevos, start=len(EJ)):
                    pz = [x for k, x in enumerate(piezas) if f'p{e}_{k}' in usados]
                    if pz and not solo_modelo(pz): nuevos2.append((cab, cls, pz))
                nuevos = nuevos2
                n = len(EJ) + len(nuevos) + 1
            EJ = EJ + nuevos
            reparto, libres, alto_fin = medir(EJ)
        hueco = libres[-1] - alto_fin - 70                 # 70 ≈ enunciado + márgenes
        if hueco >= 150 and d['plantilla'] != 'chasis':
            EJ = EJ + [dibuja(n, min(hueco, 420))]
            reparto, libres, alto_fin = medir(EJ)
        while len(reparto) > base and len(EJ) > nbase:      # lo nuevo nunca añade páginas: se quita pieza a pieza
            cab, cls, pz = EJ[-1]
            EJ = EJ[:-1] + ([(cab, cls, pz[:-1])] if len(pz) > 1 and not solo_modelo(pz[:-1]) else [])
            reparto, libres, alto_fin = medir(EJ)
    while True:
        FIN[0] = libres[-1] >= alto_fin
        # 2) montar cada página con sus piezas
        htmls = []
        for ids in reparto:
            trozos = []
            for uid in ids:
                if uid.startswith('c'): continue
                e, k = map(int, uid[1:].split('_'))
                cab, cls, piezas = EJ[e]
                if trozos and trozos[-1][4] == e:
                    trozos[-1][3].append(piezas[k])
                else:
                    trozos.append([cab, cls, ('c%d' % e) in ids, [piezas[k]], e])
            htmls.append(montar([t[:4] for t in trozos]))
        T = len(htmls)
        doc = documento(htmls)
        # 3) comprobar que nada se sale (sin el recorte del chasis)
        prueba = os.path.join(carpeta, '.mide.html')
        open(prueba, 'w', encoding='utf8').write(doc.replace('</head>', MIDE + '</head>'))
        n = pdf(prueba, os.path.join(tempfile.gettempdir(), 'mide.pdf')); os.remove(prueba)
        if n == T: break
        if len(EJ) > nbase:                                 # quitamos una pieza de lo nuevo y otra vez
            cab, cls, pz = EJ[-1]
            EJ = EJ[:-1] + ([(cab, cls, pz[:-1])] if len(pz) > 1 and not solo_modelo(pz[:-1]) else [])
            reparto, libres, alto_fin = medir(EJ); continue
        print(f'✗ {rel}: el reparto no cabe ({n} folios para {T} páginas) — NO se escribe'); return False
    open(destino, 'w', encoding='utf8').write(doc)
    n = pdf(destino, os.path.join(carpeta, nom))
    print(f'{"✓" if n == T else "✗"} {rel} → {nom} ({n} pág.{"" if ZOOM[0] == 1.12 else ", escala " + str(ZOOM[0])}: ' + ' | '.join(','.join(x for x in ids if x[0] == 'p') for ids in reparto) + ')')
    return n == T


def guardar_extraccion(ruta):
    rel = os.path.relpath(os.path.abspath(ruta), RAIZ)
    jd = os.path.join(DATOS, os.path.splitext(rel)[0] + '.json')
    if os.path.exists(jd): return True
    d = extraer(ruta)
    f = comprobar_extraccion(d, ruta)
    if f: print(f'✗ {rel}:', '; '.join(f)); return False
    os.makedirs(os.path.dirname(jd), exist_ok=True)
    json.dump(d, open(jd, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3: print(__doc__); sys.exit(1)
    orden, fichas = sys.argv[1], sys.argv[2:]
    ok = True
    if orden in ('extraer', 'todo'): ok = all([guardar_extraccion(f) for f in fichas])
    def seguro(f):
        try: return generar(f)
        except Exception as e: print(f'✗ {f}: {type(e).__name__}: {e}'); return False
    if ok and orden in ('generar', 'todo'): ok = all([seguro(f) for f in fichas])
    sys.exit(0 if ok else 1)
