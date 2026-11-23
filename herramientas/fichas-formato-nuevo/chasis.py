"""Modo «chasis» (Mates y fichas con piezas propias): se respeta cada ejercicio por dentro
(sus medidas, sus dibujos SVG, sus alineaciones) y se cambia todo lo de alrededor."""
import re
from html.parser import HTMLParser

VACIOS = {'br', 'hr', 'img', 'input', 'meta', 'link', 'col', 'area', 'base', 'wbr', 'source'}


def trozos_primer_nivel(frag):
    """Divide un fragmento HTML en sus elementos de primer nivel (cadenas)."""
    lineas = frag.split('\n'); ini = [0]
    for l in lineas: ini.append(ini[-1] + len(l) + 1)
    off = lambda pos: ini[pos[0] - 1] + pos[1]

    class P(HTMLParser):
        def __init__(s):
            super().__init__(convert_charrefs=False); s.prof = 0; s.cortes = []; s.a = None
        def handle_starttag(s, tag, attrs):
            if tag in VACIOS:
                if s.prof == 0: s.cortes.append((off(s.getpos()), None))
                return
            if s.prof == 0: s.a = off(s.getpos())
            s.prof += 1
        def handle_startendtag(s, tag, attrs):
            if s.prof == 0: s.cortes.append((off(s.getpos()), None))
        def handle_endtag(s, tag):
            if tag in VACIOS: return
            s.prof -= 1
            if s.prof == 0:
                fin = frag.index('>', off(s.getpos())) + 1
                s.cortes.append((s.a, fin))
    p = P(); p.feed(frag); p.close()
    out = []
    for a, b in p.cortes:
        if b is None: continue
        out.append(frag[a:b])
    return out


QUITAR = re.compile(r'^\s*(html|body|\.wrapper|\.seccion-titulo.*|\.ej-n|\.topbar|\.back-btn|\.print-btn|\.header|\.academia-nombre|\.ficha-ref|\.datos-alumno|\.dato\b.*|\.separador|\.tipo-badge|\.footer.*|\*,.*|\.ej-enunciado.*|\.ej-block|\.num)\s*$')


def interlineado(css):
    """Más interlineado en las reglas de texto (las cuentas en columna no se tocan)."""
    texto = re.compile(r'recuerda|enunciado|frase|instr|titulo|info|vf|preg|prob|completar|ej-col|pasos|ejemplo')
    def lh(m):
        sel, cuerpo = m.group(1), m.group(2)
        if texto.search(sel):
            cuerpo = re.sub(r'line-height:\s*([\d.]+)', lambda x: 'line-height:' + (x.group(1) if float(x.group(1)) >= 1.75 else '1.75'), cuerpo)
        return sel + '{' + cuerpo + '}'
    css = re.sub(r'([^{}]+)\{([^}]*)\}', lh, css)
    return css


def espaciado(css):
    """Separaciones pequeñas (entre filas, cajas, elementos) casi al doble: el diseño antiguo iba apretado."""
    def px(v, m):
        n = float(v)
        return f'{max(8, round(n * m))}px' if 0 < n < 14 else f'{v}px'
    def regla(m):
        sel, cuerpo = m.group(1), m.group(2)
        if re.search(r'op-col|suma-col|dibujos-grupo|rec-op|cifra|celda', sel): return m.group(0)
        cuerpo = re.sub(r'(margin-bottom|row-gap):\s*([\d.]+)px', lambda x: f'{x.group(1)}:{px(x.group(2), 1.8)}', cuerpo)
        cuerpo = re.sub(r'(?<![-\w])gap:\s*([\d.]+)px', lambda x: f'gap:{px(x.group(1), 1.7)}', cuerpo)
        return sel + '{' + cuerpo + '}'
    return re.sub(r'([^{}]+)\{([^}]*)\}', regla, css)


def problema(html_p, mini_pauta):
    """Un problema antiguo (.problema) → formato nuevo: enunciado + Datos + Operación + Solución, sin cuadro."""
    ico = re.search(r'<div class="problema-icono">\s*(<svg.*?</svg>)', html_p, re.S)
    num = re.search(r'class="problema-num">(.*?)</span>', html_p, re.S).group(1).strip()
    txt = re.search(r'class="problema-enunciado">(.*?)</span>\s*</div>', html_p, re.S).group(1).strip()
    signo = 'signo-elegir' in html_p
    fila = lambda l, c: f'<div class="pb-fila"><span class="pb-l">{l}</span>{c}</div>'
    return ('<div class="pb">'
            f'<div class="pb-cab">{"<span class=pb-ico>" + ico.group(1) + "</span>" if ico else ""}'
            f'<span class="pb-n">{num}</span><span class="pb-t">{txt}</span></div>'
            + (fila('Rodea el signo:', '<span class="pb-signos"><span>+</span><span>−</span></span>') if signo else '')
            + fila('Datos:', mini_pauta)
            + '<div class="pb-fila pb-op"><span class="pb-l">Operación:</span><div class="pb-cuad"></div></div>'
            + fila('Solución:', mini_pauta)
            + '</div>')


def css_util(css):
    """Del CSS antiguo, solo las reglas de los ejercicios (fuera página, cabecera, pie, impresión)."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out = []; i = 0
    while i < len(css):
        j = css.find('{', i)
        if j < 0: break
        sel = css[i:j].strip()
        if sel.startswith('@'):                              # @media, @page, @font-face → fuera (bloque entero)
            prof = 0; k = j
            while True:
                if css[k] == '{': prof += 1
                elif css[k] == '}':
                    prof -= 1
                    if prof == 0: break
                k += 1
            i = k + 1; continue
        k = css.find('}', j)
        cuerpo = css[j+1:k]
        sels = [x for x in sel.split(',') if not QUITAR.match(x)]
        if sels: out.append(','.join('.mz ' + x.strip() for x in sels) + '{' + cuerpo.strip() + '}')
        i = k + 1
    css = '\n'.join(out)
    css = css.replace("'Playwrite ES'", "'PW-ficha'")
    css = re.sub(r'solid #000\b', 'solid var(--bosque)', css)
    return css


def extraer_chasis(s, d):
    st = '\n'.join(re.findall(r'<style>(.*?)</style>', s, re.S))
    m = re.search(r"@font-face\s*\{[^}]*size-adjust:\s*([\d.]+)%", st)
    d['size_adjust'] = float(m.group(1)) if m else 100
    d['css'] = css_util(st)
    body = re.sub(r'<style>.*?</style>', '', s.split('</head>', 1)[1], flags=re.S)
    mid = re.split(r'<hr class="separador"\s*/?>', body, 1)[1]
    mid = mid[:mid.rindex('<div class="footer">')]
    if mid.lstrip().startswith('<div class="wrapper">'):
        mid = mid.lstrip()[len('<div class="wrapper">'):]
    bl = trozos_primer_nivel(mid)
    tb = re.search(r'class="texto-box"[^>]*>(.*?)</div>', mid, re.S)
    if tb:
        frases = re.split(r'<br\s*/?>|</p>', tb.group(1))
        d['texto'] = [re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x)).strip() for x in frases if re.sub(r'<[^>]+>|\s', '', x)]
    d['badge'] = ''
    d['bloques'] = []
    for b in bl:
        if 'class="tipo-badge"' in b[:60]:
            d['badge'] = re.sub(r'<[^>]+>', '', b).strip(); continue
        d['bloques'].append(b.strip())
    d['plantilla'] = 'chasis'
    return d


def enunciado(b, ej):
    """<div class="ej-enunciado"><span class="num">3.</span> Texto</div> → enunciado del formato nuevo."""
    def r(m):
        n = re.sub(r'\D', '', m.group(1)) or ''
        return ej(n, m.group(2).strip())
    b = re.sub(r'<div class="ej-enunciado">\s*<span class="num">(.*?)</span>(.*?)</div>', r, b, flags=re.S)
    # 2º: <div class="seccion-titulo"><span class="ej-n">1</span> 📖 Lee el texto.</div>
    def r2(m):
        txt = re.sub(r'^\s*<span class="txt-flex">(.*)</span>\s*$', r'\1', m.group(2).strip(), flags=re.S)
        txt = re.sub(r'^[^\wÁÉÍÓÚÑáéíóúñ¿¡<]+', '', txt.strip())
        return ej(m.group(1).strip(), txt)
    return re.sub(r'<div class="seccion-titulo">\s*<span class="ej-n">(.*?)</span>(.*?)</div>', r2, b, flags=re.S)


PAUTA = ''


# Dibujos de línea antiguos → emoji (decisión de Miguel, 23-nov-2026: «esos dibujos no los quiero»).
# Clave = huella del SVG antiguo (sin width/height/class/style). Relojes, monedas y figuras NO se tocan.
DIBUJO_A_EMOJI = {
    '9491ad': '🍎', 'a1ce94': '🍎', 'a63cd3': '🍎', 'f8c9c2': '🍌', '856f6f': '🍐', '841b47': '🍐', 'c7cbeb': '🍇', 'dbdb23': '🍇',
    'dfe98f': '🐶', '295129': '🐶', '698919': '🐶', '060410': '🐱', 'f968c1': '🐱', '3f6866': '🐱', 'afebb7': '🐟', 'b4df33': '🐟',
    'df8889': '🚗', 'e4c55d': '🚗', '9b25ac': '🚲', '313770': '🚲', 'a6005d': '🚲', 'a40f8a': '✈️', 'b34351': '⛵',
    '5b28c5': '✏️', '8526f6': '✏️', 'ac5c45': '✏️', '2a22ec': '📘', '110cd2': 'GOMA', '656014': 'SACAPUNTAS',
    'd7ec3e': '🃏', 'c0b506': '🍪', '8714fa': '🧒', '0846eb': '🧒', '760346': '🪙', 'f623f3': '⭐', 'd68aa2': '🌸',
    '4af2a9': '🍬', '42d7f4': '🍬', '8e34cc': '🎈', '56ca9e': '🐦', '21b656': '⚽',
}
PROPIOS = {   # objetos sin emoji: dibujo propio en color, estilo emoji
    'GOMA': '<g transform="rotate(-18 30 30)"><rect x="8" y="20" width="44" height="22" rx="5" fill="#f9a8d4" stroke="#9d174d" stroke-width="2"/>'
            '<rect x="30" y="20" width="22" height="22" rx="4" fill="#60a5fa" stroke="#1e3a8a" stroke-width="2"/></g>',
    'SACAPUNTAS': '<rect x="12" y="16" width="36" height="30" rx="5" fill="#fbbf24" stroke="#92400e" stroke-width="2"/>'
                  '<circle cx="30" cy="31" r="8" fill="#fff" stroke="#92400e" stroke-width="2"/><circle cx="30" cy="31" r="3" fill="#374151"/>'
                  '<rect x="40" y="22" width="6" height="18" rx="2" fill="#d1d5db" stroke="#6b7280" stroke-width="1.5"/>',
}

# Mates 2º: dibujos de los problemas → emoji (elegidos leyendo cada enunciado)
DIBUJO_A_EMOJI.update({
    'f4ade3': '🃏', 'd643e2': '🃏', '9ad17e': '🃏', 'c975ea': '🚌', 'f5f3c2': '💶', '7bfbb9': '💶', 'c56652': '💶', '271c07': '💶',
    'a3d8ff': '💶', 'a10f82': '💶', 'ccc453': '💶', '01c096': '💶', 'bbc21c': '💶', '2c8543': '🐷', '2d8f5f': '✏️',
    '33fa95': '🧒', '590dd9': '🧒', '61b7f5': '🧒', '9dd122': '🎯', 'f88cb8': '⭐', '3f1baa': '🎯', '38c784': '⭐',
    '5a88ad': '🎈', '65ae0a': '🎈', 'ee89b3': '🎈', '3a745d': '🎈', '973df8': '🎈', 'b8a3ac': '📖', 'dd998a': '📚', '8199ea': '📚',
    '3dff8f': '🌸', 'a574ab': '🍎', 'f727ce': '⚽', '226b55': '⚽', 'a5cbfe': '⚽', 'e90294': '📮', '022818': '🪑', 'd0b66e': '🪑',
    'ff0d41': '🪑', '912a12': '🪑', '79b5c6': '🪑', '48b628': '🧦', 'a003c6': '🍬', '0a9164': '🍬', 'abad1b': '🖍️', 'ef3721': '🖍️',
    '0421ee': '🧁', '2ced50': '🧁', '742dba': '🥚', '7c5a99': '🥬', '38fcc6': '🍫', '04239b': '🧱', '08b297': '🥛', '936893': '⚽',
    '3cce30': '🍪',
})


def huella(svg):
    import hashlib
    k = re.sub(r'\s+', ' ', re.sub(r'(width|height|class|style)="[^"]*"', '', svg)).strip()
    return hashlib.md5(k.encode()).hexdigest()[:6]


def a_dinero(html):
    """Monedas y billetes antiguos (dibujo de línea) → en color (dinero.py), leyendo su valor."""
    import dinero
    def r(m):
        attrs, cuerpo = m.group(1), m.group(2)
        cls = re.search(r'class="([^"]+)"', attrs)
        if not cls or not re.search(r'moneda-svg|billete-svg', cls.group(1)): return m.group(0)
        txt = ' '.join(re.findall(r'>([^<>]+)</text>', cuerpo))
        if 'billete' in cls.group(1):
            v = int(re.search(r'\d+', txt).group(0)); return dinero.billete(v, attrs)
        e = re.search(r'(\d+)\s*€', txt)
        cent = int(e.group(1)) * 100 if e else int(re.search(r'(\d+)\s*CENT', txt).group(1))
        return dinero.moneda(cent, attrs)
    return re.sub(r'<svg(\b[^>]*)>(.*?)</svg>', r, html, flags=re.S)


def a_emoji(html):
    html = a_dinero(html)
    def r(m):
        e = DIBUJO_A_EMOJI.get(huella(m.group(0)))
        if not e: return m.group(0)
        attrs = m.group(1)
        if e in PROPIOS:
            return f'<svg{attrs}>{PROPIOS[e]}</svg>'
        return (f'<svg{attrs}><text x="30" y="51" font-size="54" text-anchor="middle" '
                f'font-family="Apple Color Emoji,Segoe UI Emoji,Noto Color Emoji,sans-serif">{e}</text></svg>')
    return re.sub(r'<svg(\b[^>]*)>.*?</svg>', r, html, flags=re.S)


_NUEVAS = None


def clases_nuevas():
    """Clases del formato nuevo (letras + extra.css): si una ficha antigua usa el mismo nombre, choca."""
    global _NUEVAS
    if _NUEVAS is None:
        import os
        aqui = os.path.dirname(os.path.abspath(__file__))
        css = open(os.path.join(aqui, '..', 'fichas-letras', 'estilo.css')).read() + open(os.path.join(aqui, 'extra.css')).read()
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
        css = re.sub(r'(?:(?<=\})|^)\s*\.mz [^{]*\{[^}]*\}', '', css, flags=re.M)      # reglas para los ejercicios antiguos: no son clases «nuevas»
        _NUEVAS = set(re.findall(r'\.([a-zA-Z][\w-]*)', re.sub(r'url\([^)]*\)', '', css)))
        _NUEVAS -= {'mz'}               # el envoltorio de los ejercicios antiguos no es una clase «nueva»
    return _NUEVAS


def sin_choques_html(h):
    """Renombra (v-<nombre>) las clases antiguas que se llaman igual que una del formato nuevo."""
    N = clases_nuevas()
    return re.sub(r'class="([^"]+)"', lambda m: 'class="' + ' '.join(('v-' + c) if c in N else c for c in m.group(1).split()) + '"', h)


def sin_choques_css(css):
    for c in clases_nuevas():
        css = re.sub(r'\.' + re.escape(c) + r'(?![\w-])', '.v-' + c, css) if ('.' + c) in css else css
    return css


PAUTA_ENTERA = ''
MINI = ''


def a_pauta(html):
    """2º: escribir sobre pauta de 4 líneas como en 1º. Líneas largas → pauta entera; huecos de frase → pauta pequeña."""
    html = re.sub(r'<div class="(respuesta-linea|escribir-linea|reflexion-linea)"[^>]*>\s*</div>', lambda m: PAUTA_ENTERA, html)
    pq = MINI.replace('class="mini-pauta"', 'class="mini-pauta pq"')
    html = re.sub(r'<span class="(?:v-)?hueco"[^>]*>\s*</span>', lambda m: pq, html)
    html = re.sub(r'<div class="conector-hueco"[^>]*>\s*</div>', lambda m: pq, html)
    return html


def proteger_ej(b):
    """Renombra las clases antiguas que chocan, sin tocar los enunciados ya convertidos al formato nuevo."""
    trozos = re.split(r'(<div class="ej"><span class="ej-n">.*?</span><span>.*?</span></div>)', b, flags=re.S)
    return ''.join(t if t.startswith('<div class="ej">') else sin_choques_html(t) for t in trozos)


def partible(b):
    """Bloque cuyos hijos son ≥3 piezas iguales (preguntas, frases…) → (clase, [hijos]). Si no, None."""
    m = re.match(r'<div class="([^"]+)">(.*)</div>$', b.strip(), re.S)
    if not m or re.search(r'recuerda|opcion', m.group(1)): return None   # una pregunta con opciones nunca se parte
    hijos = [h for h in trozos_primer_nivel(m.group(2))]
    cls = [re.match(r'<\w+ class="([^"]+)"', h) for h in hijos]
    if len(hijos) < 3 or not all(cls) or len(set(c.group(1) for c in cls)) != 1: return None
    if re.sub(r'\s|<[^>]+>', '', ''.join(hijos)) != re.sub(r'\s|<[^>]+>', '', m.group(2)): return None   # no perder texto suelto
    return m.group(1), hijos


def ejercicios_chasis(d, ej):
    """Cada bloque de primer nivel es una pieza; un enunciado suelto va pegado al bloque siguiente;
    las listas de problemas se pueden repartir problema a problema."""
    bl = [enunciado(a_emoji(b), ej) for b in d['bloques']]          # primero los enunciados (usan ej-n)
    bl = [proteger_ej(b) for b in bl]
    if '/primaria/2/' in d['origen']: bl = [a_pauta(b) for b in bl]
    o = []; k = 0; defs = ''
    while k < len(bl):
        b = bl[k]
        if b.startswith('<div class="ej">') and k + 1 < len(bl):      # enunciado suelto + su rejilla
            lista = partible(bl[k+1])
            if lista:                                                   # lista larga: se reparte pieza a pieza
                o.append((b, 'mz ' + lista[0], lista[1])); k += 2; continue
            o.append(('', 'mz', [b + bl[k+1]])); k += 2; continue
        m = re.match(r'<div class="(problemas)">(.*)</div>$', b, re.S)
        if m:
            hijos = trozos_primer_nivel(m.group(2))
            if all(re.match(r'<div class="problema[ "]', h) for h in hijos):
                o.append(('', 'pbs', [problema(h, PAUTA) for h in hijos])); k += 1; continue
            o.append(('', 'mz ' + m.group(1), hijos)); k += 1; continue
        if b.startswith('<svg') and 'width="0"' in b[:80]:            # definiciones de dibujos: una vez, al principio
            defs += b; k += 1; continue
        o.append(('', 'mz', [b])); k += 1
    if defs and o:
        cab, cls, pz = o[0]; o[0] = (cab, cls, [defs + pz[0]] + pz[1:])
    return o


def css_ficha(d, rel_raiz):
    """CSS propio de la ficha: su letra (con el size-adjust que tenía), sus reglas y la escala."""
    return (f"@font-face{{font-family:'PW-ficha';src:url('{rel_raiz}fuentes/playwrite-es.woff2') format('woff2');"
            f"font-weight:100 400;font-display:swap;size-adjust:{d.get('size_adjust', 100)}%}}"
            ".mz{zoom:1.12;font-family:'PW-ficha',cursive}.mz .ej{font-family:'Playwrite ES',cursive}"
            + espaciado(interlineado(sin_choques_css(d['css']))))
