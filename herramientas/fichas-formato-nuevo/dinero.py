"""Monedas y billetes de euro en color, para las fichas de 1º-2º (petición de Miguel, 23-nov-2026).

Dibujos SENCILLOS con el color y el valor de los de verdad (no copias exactas: reproducir los billetes
tiene restricciones del BCE y para enseñar basta con color + número):
  1, 2, 5 céntimos → cobre · 10, 20, 50 céntimos → dorado
  1 € → centro plateado con aro dorado · 2 € → centro dorado con aro plateado
  billetes: 5 € gris verdoso · 10 € rojo · 20 € azul · 50 € naranja · 100 € verde
Moneda: viewBox 0 0 100 100 · Billete: viewBox 0 0 160 90 (los mismos marcos que los dibujos antiguos).
"""
import math

DEFS = ('<defs>'
        '<radialGradient id="dn-cobre" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#f7c49b"/><stop offset=".6" stop-color="#c8763a"/><stop offset="1" stop-color="#8f4a17"/></radialGradient>'
        '<radialGradient id="dn-oro" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#fff3b0"/><stop offset=".6" stop-color="#e2b52b"/><stop offset="1" stop-color="#a77d0c"/></radialGradient>'
        '<radialGradient id="dn-plata" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#c9d1db"/><stop offset="1" stop-color="#8592a3"/></radialGradient>'
        '</defs>')

BILLETE = {5: ('#c9d3c4', '#7d8f78', '#3f4d3c'), 10: ('#f6c1bb', '#d0584b', '#7a2219'),
           20: ('#bdd6f3', '#3f7fd6', '#163f7a'), 50: ('#fdd3a5', '#ec8a2c', '#8a4708'),
           100: ('#c6e8c3', '#4e9e4a', '#215421')}


def _estrellas(cx, cy, r, n=12, tam=7, color='#5b4a12'):
    o = []
    for k in range(n):
        a = 2 * math.pi * k / n
        o.append(f'<text x="{cx + r * math.sin(a):.1f}" y="{cy - r * math.cos(a) + tam * 0.36:.1f}" font-size="{tam}" '
                 f'text-anchor="middle" fill="{color}" font-family="sans-serif">★</text>')
    return ''.join(o)


def moneda(cent, attrs=' viewBox="0 0 100 100"'):
    """cent = valor en céntimos (1, 2, 5, 10, 20, 50, 100, 200)."""
    assert cent in (1, 2, 5, 10, 20, 50, 100, 200), cent
    if cent in (100, 200):
        aro, centro = ('dn-oro', 'dn-plata') if cent == 100 else ('dn-plata', 'dn-oro')
        cuerpo = (f'<circle cx="50" cy="50" r="46" fill="url(#{aro})" stroke="#6b5a1e" stroke-width="2"/>'
                  f'<circle cx="50" cy="50" r="31" fill="url(#{centro})" stroke="#6b6b6b" stroke-width="1.5"/>'
                  + _estrellas(50, 50, 38.5, tam=7, color='#4a3d10')
                  + f'<text x="50" y="57" font-size="22" font-weight="800" text-anchor="middle" fill="#1f2937" font-family="sans-serif">{cent // 100}€</text>'
                  '<text x="50" y="70" font-size="7" font-weight="700" text-anchor="middle" fill="#1f2937" font-family="sans-serif" letter-spacing="1">EURO</text>')
    else:
        g, borde, tinta = ('dn-cobre', '#7a3c10', '#4a230a') if cent < 10 else ('dn-oro', '#8a6a08', '#4a3a05')
        cuerpo = (f'<circle cx="50" cy="50" r="46" fill="url(#{g})" stroke="{borde}" stroke-width="2.5"/>'
                  f'<circle cx="50" cy="50" r="39" fill="none" stroke="{borde}" stroke-width="1" opacity=".55"/>'
                  + _estrellas(50, 50, 33, n=10, tam=6.5, color=tinta)
                  + f'<text x="50" y="58" font-size="28" font-weight="800" text-anchor="middle" fill="{tinta}" font-family="sans-serif">{cent}</text>'
                  f'<text x="50" y="71" font-size="8" font-weight="700" text-anchor="middle" fill="{tinta}" font-family="sans-serif" letter-spacing="1">CENT</text>')
    return f'<svg{attrs}>{DEFS}{cuerpo}</svg>'


def billete(valor, attrs=' viewBox="0 0 160 90"'):
    assert valor in BILLETE, valor
    claro, medio, oscuro = BILLETE[valor]
    gid = f'dn-b{valor}'
    return (f'<svg{attrs}><defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{claro}"/><stop offset="1" stop-color="{medio}"/></linearGradient></defs>'
            f'<rect x="2" y="2" width="156" height="86" rx="7" fill="url(#{gid})" stroke="{oscuro}" stroke-width="2"/>'
            f'<rect x="8" y="8" width="58" height="74" rx="5" fill="#ffffff" opacity=".55"/>'
            f'<path d="M86 72 V44 a18 18 0 0 1 36 0 V72" fill="none" stroke="{oscuro}" stroke-width="2" opacity=".45"/>'
            f'<path d="M96 72 V48 a8 8 0 0 1 16 0 V72" fill="none" stroke="{oscuro}" stroke-width="1.5" opacity=".35"/>'
            + _estrellas(139, 30, 11, tam=5, color='#f5d90a')
            + f'<text x="37" y="56" font-size="34" font-weight="800" text-anchor="middle" fill="{oscuro}" font-family="sans-serif">{valor}</text>'
            f'<text x="37" y="74" font-size="9" font-weight="700" text-anchor="middle" fill="{oscuro}" font-family="sans-serif" letter-spacing="2">EURO</text>'
            f'<text x="150" y="80" font-size="13" font-weight="800" text-anchor="end" fill="{oscuro}" font-family="sans-serif">{valor}</text>'
            '</svg>')
