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


QUITAR = re.compile(r'^\s*(html|body|\.topbar|\.back-btn|\.print-btn|\.header|\.academia-nombre|\.ficha-ref|\.datos-alumno|\.dato\b.*|\.separador|\.tipo-badge|\.footer.*|\*,.*|\.ej-enunciado.*|\.ej-block|\.num)\s*$')


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
    bl = trozos_primer_nivel(mid)
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
    return re.sub(r'<div class="ej-enunciado">\s*<span class="num">(.*?)</span>(.*?)</div>', r, b, flags=re.S)


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


def ejercicios_chasis(d, ej):
    """Cada bloque de primer nivel es una pieza; un enunciado suelto va pegado al bloque siguiente;
    las listas de problemas se pueden repartir problema a problema."""
    bl = [enunciado(a_emoji(b), ej) for b in d['bloques']]
    o = []; k = 0; defs = ''
    while k < len(bl):
        b = bl[k]
        if b.startswith('<div class="ej">') and k + 1 < len(bl):      # enunciado suelto + su rejilla
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
            + espaciado(interlineado(d['css'])))
