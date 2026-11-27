"""Bloques de base 10 en 3D (como el material de clase). Colores fijos: unidad verde, decena azul, centena roja.
Las unidades van como cubitos SUELTOS (con hueco), para que no parezcan una barra (Miguel, 27-nov-2026)."""
COL = {'u': ('#6dbb65', '#b4e2ad', '#3d8a37', '#2a6526'),
       'd': ('#5b9be0', '#a9cdf5', '#2f6fb5', '#1f4e8a'),
       'c': ('#e0665b', '#f5b4ad', '#b5382f', '#8a2a23')}

def svg(d=0, u=0, L=6):
    dx = dy = round(L / 2); H = 10 * L + dy; o = []; x = 0
    def cubo(px, py, k):
        f, t, l, s = COL[k]; w = '.7'
        return (f'<polygon points="{px},{py+dy} {px+dx},{py} {px+dx+L},{py} {px+L},{py+dy}" fill="{t}" stroke="{s}" stroke-width="{w}"/>'
                f'<polygon points="{px+L},{py+dy} {px+L+dx},{py} {px+L+dx},{py+L} {px+L},{py+L+dy}" fill="{l}" stroke="{s}" stroke-width="{w}"/>'
                f'<rect x="{px}" y="{py+dy}" width="{L}" height="{L}" fill="{f}" stroke="{s}" stroke-width="{w}"/>')
    for _ in range(d):                                   # decena: barra de 10 cubos pegados
        o += [cubo(x, j * L, 'd') for j in range(9, -1, -1)]; x += L + dx + 5
    if u:
        x += 6 if d else 0; paso = L + dx + 4            # unidades: cubitos sueltos, columnas de 5 desde abajo
        for k in range(u):
            c, f = divmod(k, 5); o.append(cubo(x + c * paso, H - dy - L - f * (L + dy + 4), 'u'))
        x += ((u - 1) // 5 + 1) * paso
    w = max(x, 1)
    return (f'<svg class="bloques" viewBox="-1 -1 {w + 2} {H + 2}" width="{w + 2}" height="{H + 2}" '
            f'role="img" aria-label="{d} decenas y {u} unidades">' + ''.join(o) + '</svg>')
