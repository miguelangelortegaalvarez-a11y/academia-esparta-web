#!/usr/bin/env python3
"""Genera la ficha INTERACTIVA de una letra de 1º a partir del mismo JSON que la ficha de papel.

Uso (desde la raíz del repo):
    python3 herramientas/fichas-letras/generar_interactiva_letra.py m          # una letra (sin gastar créditos)
    python3 herramientas/fichas-letras/generar_interactiva_letra.py m --voz    # genera los audios de Sara que falten (ElevenLabs)
    python3 herramientas/fichas-letras/generar_interactiva_letra.py --todas    # las 29

Escribe recursos/primaria/1/lengua/letras/<archivo>-interactiva.html (misma dirección que la antigua).

Seis pasos, uno detrás de otro y sin teclado (se juega tocando): conozco la letra · toca la letra ·
¿qué sílaba falta? · junto sílabas · completa la frase · el cuento. Voz del dispositivo (🔊) si hay voz
en español; si no la hay, los botones de voz no salen y la ficha se hace igual.
El color de cada letra es el de su pieza en materiales.html (mismo orden y misma paleta).
"""
import hashlib, html, json, os, re, subprocess, sys, tempfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(RAIZ, 'recursos', 'primaria', '1', 'lengua', 'letras')
REL = '../../../../../'
E = html.escape

# Mismo orden y paleta que las piezas de materiales.html (vocales primero, luego el orden de clase)
ORDEN = ['a', 'e', 'i', 'o', 'u', 'm', 'p', 's', 'd', 't', 'n', 'l', 'r', 'f', 'c', 'b', 'v', 'g', 'j',
         'll', 'ch', 'z', 'nie', 'h', 'q', 'y', 'ge', 'ce', 'rr']
COLORES = ['#15803d', '#c2410c', '#be123c', '#1d4ed8', '#7c3aed']
# Voz: la misma que Redes Sociales (Sara, ElevenLabs), con SU script. La clave la lee ese script del Llavero.
GENERAR_VOZ = os.path.expanduser('~/Desktop/Redes Sociales/Identidad/voces/generar-voz.py')
SEMILLA = 7

# Instrucciones habladas: COMUNES a todas las letras (no nombran la letra) → se generan una sola vez en audio/comun/
CONSIGNAS = [
    'Mira la letra. Toca los dibujos para oír las palabras, y toca las sílabas. Después, pídele a tu profe que te diga cómo suena esta letra.',
    'Toca todas las letras iguales a estas dos que encuentres en cada palabra. Si una palabra no tiene ninguna, toca el botón: no tiene.',
    'Mira el dibujo y escucha la palabra. Después, toca la sílaba que falta.',
    'Mira el dibujo y toca las sílabas en orden para formar la palabra.',
    'Escucha la frase y toca la palabra que falta.',
    'Escucha el cuento. Después, toca la respuesta buena de cada pregunta.',
]
FINAL = '¡Muy bien! ¡Lo has conseguido!'
# Felicitación al acabar cada ejercicio (comunes, se elige una al azar): pedido por Miguel el 22-nov-2026
SALUDO = '¡Hola! Soy Leoni. ¡Vamos a aprender!'
ELOGIOS = ['¡Muy bien!', '¡Genial! Lo has hecho fenomenal.', '¡Qué bien lo haces!', '¡Eres un campeón!',
           '¡Sigue así, lo estás haciendo genial!', '¡Bravo! ¡Muy bien hecho!']

# El paso 2 sí nombra la letra (decidido por Miguel el 22-nov-2026): «Toca todas las eme…». Una frase por letra.
NOMBRES = {'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u', 'm': 'eme', 'p': 'pe', 's': 'ese', 'd': 'de', 't': 'te',
           'n': 'ene', 'l': 'ele', 'r': 'erre', 'f': 'efe', 'c': 'ce', 'b': 'be', 'v': 'uve', 'g': 'ge', 'j': 'jota',
           'll': 'elle', 'ch': 'che', 'z': 'zeta', 'nie': 'eñe', 'h': 'hache', 'q': 'cu', 'y': 'i griega', 'ge': 'ge',
           'ce': 'ce', 'rr': 'erre doble'}
def consigna_toca(A):
    if A == 'rr': return 'Toca todas las erres dobles. Si una palabra no tiene ninguna, toca: no tiene.'
    return f'Toca todas las {NOMBRES[A]}. Si una palabra no tiene ninguna, toca: no tiene.'
def consignas_de(A):
    c = list(CONSIGNAS); c[1] = consigna_toca(A); return c

# «¿Cómo suena?»: sin audio (decisión de Miguel, 22-nov-2026: lo explica el profe). Solo se enseña escrito.
SE_ALARGAN = {'a', 'e', 'i', 'o', 'u', 'm', 'n', 'ñ', 'l', 's', 'f', 'z', 'j', 'r', 'rr', 'y'}
def como_suena(d):
    A, L = d.get('archivo', d['letra']), d['letra']
    if A == 'h': return 'h', 'La h es muda: no suena. 🤫'
    if A in ('ce', 'ge', 'q'): return ' · '.join(d['silabas']), 'Tu profe te va a decir cómo suena. ¡Repítelo tú también!'
    if L in SE_ALARGAN: return (L * 4 if len(L) == 1 else L * 3), 'Tu profe te va a decir cómo suena. ¡Repítelo tú también!'
    return ' · '.join([L] * 3), 'Tu profe te va a decir cómo suena. ¡Repítelo tú también!'


ESP_VER = {'ll': 'Ll ll', 'ch': 'Ch ch', 'rr': 'rr', 'ce': 'ce ci', 'ge': 'ge gi'}
def album():
    """Las 29 casillas del álbum de pegatinas: letra, dibujo (el primero de su presentación) y enlace."""
    out = []
    for A in ORDEN:
        f = os.path.join(AQUI, 'letras', f'{A}.json')
        if not os.path.exists(f): continue
        d = json.load(open(f, encoding='utf8'))
        out.append({'a': A, 'ver': ESP_VER.get(A, d['mayus'] + d['letra']), 'emo': d['intro']['palabras'][0][0]})
    return out


def frase_completa(a, w, b):
    if w == '...' and b == '.': return f'{a}...'
    return f"{a} {w}{'' if b.startswith('.') else ' '}{b}"


def textos_voz(d):
    """Todo lo que la interactiva puede decir en voz alta (mismas cadenas que usa el JS)."""
    t = [consigna_toca(d.get('archivo', d['letra']))] + [w for _, w in d['intro']['palabras']] + d['silabas']
    for trozo in d['pauta_silabas']['pista'].split('·'):
        t.append(re.match(r'\s*(\S+)\s+(\S+)\s+de\s+(\S+)', trozo).group(3))
    t += [''.join(ss) for _, ss in d['junta']['filas']]
    for _, a, w, b in d['frases']['filas']:
        t += [frase_completa(a, '...', b), frase_completa(a, w, b)]
    c = d['cuento']; t.append(' '.join(c['lineas']))
    t += [q for q, _, _ in c['preguntas']]
    return list(dict.fromkeys(x.strip() for x in t if x.strip()))


def nombre_audio(texto):
    return hashlib.md5(texto.encode('utf8')).hexdigest()[:10] + '.m4a'


def cortar_lista(wav, n):
    """Corta un WAV con n sílabas dichas en lista por los silencios. Devuelve n trozos (listas de muestras) o None."""
    import wave, struct
    w = wave.open(wav); N = w.getnframes(); sr = w.getframerate()
    x = struct.unpack('<%dh' % N, w.readframes(N)); win = int(sr * 0.01)
    env = [max(abs(v) for v in x[i:i + win]) for i in range(0, N, win)]; thr = max(env) * 0.06
    segs, on = [], False
    for i, e in enumerate(env):
        if e > thr and not on: on, st = True, i
        elif e <= thr and on and all(v <= thr for v in env[i:i + 6]): on = False; segs.append((st, i))
    if on: segs.append((st, len(env)))
    segs = [g for g in segs if g[1] - g[0] > 8]
    if len(segs) != n: return None, sr
    pad = [0] * int(sr * 0.08)
    return [pad + list(x[max(0, a - 3) * win:min(N, (b + 4) * win)]) + pad for a, b in segs], sr


def audios_silabas(d, A, carpeta, generar_faltan):
    """Las sílabas sueltas las alarga («maaa»): se dicen en lista («ma, me, mi, mo, mu, ma.»), se cortan
    por los silencios y se tira la última, que es la que se alarga. Decidido por Miguel el 22-nov-2026."""
    import wave, struct
    sil = list(dict.fromkeys(d['silabas']))
    falta = [x for x in sil if not os.path.exists(os.path.join(carpeta, nombre_audio(x)))]
    if falta and generar_faltan:
        os.makedirs(carpeta, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            wav = os.path.join(tmp, 'lista.wav'); trozos = None
            for sep in (', ', '... '):   # si van muy pegadas (pasó con la ñ), se repite con pausas más largas
                texto = sep.join(sil + [sil[0]]) + '.'
                r = subprocess.run(['python3', GENERAR_VOZ, 'sara', texto, wav, '--pad', '0.1', '--seed', str(SEMILLA)], capture_output=True, text=True)
                trozos, sr = cortar_lista(wav, len(sil) + 1) if os.path.exists(wav) else (None, 0)
                if trozos: break
            if not trozos: print(f'   ✗ sílabas: no salen {len(sil) + 1} trozos al cortar «{texto}» → se quedan con la voz del dispositivo')
            else:
                for x, t in zip(sil, trozos):
                    tw = os.path.join(tmp, 's.wav'); o = wave.open(tw, 'w'); o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr)
                    o.writeframes(struct.pack('<%dh' % len(t), *t)); o.close()
                    subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '64000', tw, os.path.join(carpeta, nombre_audio(x))], check=True)
                print(f'   🔊 sílabas: {", ".join(sil)}')
    return {x: f'audio/{A}/{nombre_audio(x)}' for x in sil if os.path.exists(os.path.join(carpeta, nombre_audio(x)))}


def audios(d, A, generar_faltan):
    """Devuelve {texto: ruta relativa} de los audios que existen; genera los que falten si se pide."""
    carpeta = os.path.join(SALIDA, 'audio', A)
    mapa = audios_silabas(d, A, carpeta, generar_faltan)
    comun = os.path.join(SALIDA, 'audio', 'comun')
    for texto in [x for i, x in enumerate(CONSIGNAS) if i != 1] + [FINAL, SALUDO] + ELOGIOS:
        f = os.path.join(comun, nombre_audio(texto))
        if not os.path.exists(f) and generar_faltan:
            os.makedirs(comun, exist_ok=True)
            with tempfile.TemporaryDirectory() as tmp:
                wav = os.path.join(tmp, 'v.wav')
                subprocess.run(['python3', GENERAR_VOZ, 'sara', texto, wav, '--pad', '0.1', '--seed', str(SEMILLA)], capture_output=True, text=True)
                if os.path.exists(wav): subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '64000', wav, f], check=True); print(f'   🔊 (común) {texto}')
        if os.path.exists(f): mapa[texto] = f'audio/comun/{nombre_audio(texto)}'
    for texto in textos_voz(d):
        if texto in d['silabas']: continue
        f = os.path.join(carpeta, nombre_audio(texto))
        if not os.path.exists(f) and generar_faltan:
            os.makedirs(carpeta, exist_ok=True)
            with tempfile.TemporaryDirectory() as tmp:
                wav = os.path.join(tmp, 'v.wav')
                r = subprocess.run(['python3', GENERAR_VOZ, 'sara', texto, wav, '--pad', '0.1', '--seed', str(SEMILLA)], capture_output=True, text=True)
                if r.returncode != 0 or not os.path.exists(wav):
                    print(f'   ✗ voz «{texto}»: {(r.stdout + r.stderr).strip()[-200:]}'); continue
                subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '64000', wav, f], check=True)
            print(f'   🔊 {texto}')
        if os.path.exists(f): mapa[texto] = f'audio/{A}/{nombre_audio(texto)}'
    return mapa


def sin_tilde(t):
    return t.translate(str.maketrans('áéíóúüÁÉÍÓÚÜ', 'aeiouuAEIOUU')).lower()


def comprobar(d):
    fallos = []
    c = d['cuento']; b = c.get('buenas', [])
    if len(b) != len(c['preguntas']): fallos.append('cuento: falta «buenas» (la respuesta buena de cada pregunta)')
    else:
        for (q, x, y), r in zip(c['preguntas'], b):
            if r not in (x, y): fallos.append(f'cuento: «{r}» no es una de las opciones de «{q}»')
    if len(d['pauta_silabas']['pista'].split('·')) < 3: fallos.append('pista: hacen falta al menos 3 «sílaba de palabra»')
    for trozo in d['pauta_silabas']['pista'].split('·'):
        m = re.match(r'\s*(\S+)\s+(\S+)\s+de\s+(\S+)', trozo)
        if not m: fallos.append(f'pista: no entiendo «{trozo.strip()}»'); continue
        if sin_tilde(m.group(2)) not in sin_tilde(m.group(3)): fallos.append(f'pista: «{m.group(3)}» no contiene «{m.group(2)}»')
    return fallos


def generar(archivo, voz=False):
    d = json.load(open(os.path.join(AQUI, 'letras', f'{archivo}.json'), encoding='utf8'))
    A = d.get('archivo', d['letra'])
    fallos = comprobar(d)
    if fallos:
        print(f'✗ {A}: no se genera'); [print('   -', x) for x in fallos]; return False
    color = COLORES[ORDEN.index(A) % len(COLORES)]
    L, LM = d['letra'], d['mayus']
    nombre = d.get('nombre', L)
    titulo_letra = d.get('titulo', f'Letra {LM}').replace('Ficha ', '').replace(' · 1º Primaria', '')
    sil = []
    for trozo in d['pauta_silabas']['pista'].split('·'):
        e, s, w = re.match(r'\s*(\S+)\s+(\S+)\s+de\s+(\S+)', trozo).groups()
        i = sin_tilde(w).index(sin_tilde(s))   # posición de la sílaba en la palabra, sin mirar tildes (árbol, lápiz, río…)
        sil.append({'e': e, 's': s, 'w': w, 'ini': i, 'fin': i + len(s)})
    datos = {
        'letra': L, 'mayus': LM, 'nombre': nombre, 'archivo': A,
        'intro': d['intro'], 'silabas': d['silabas'],
        'toca': [[p, e] for p, e in d['rodea']['minusculas']] + [[p, e] for p, e in d['rodea']['mayusculas']],
        'sil': sil, 'junta': d['junta']['filas'],
        'banco': d['frases']['banco'], 'frases': d['frases']['filas'],
        'cuento': d['cuento'],
        'pdf': f'letra-{A}-1-primaria.pdf', 'ver': f'{A}.html',
        'audio': audios(d, A, voz),
        'consignas': consignas_de(A), 'final': FINAL, 'saludo': SALUDO, 'elogios': ELOGIOS, 'album': album(), 'suena': como_suena(d),
    }
    url = f'https://academiaesparta.es/recursos/primaria/1/lengua/letras/{A}-interactiva.html'
    desc = (f'{titulo_letra} interactiva para 1º de Primaria: conoce la letra, tócala en palabras, sílabas, '
            f'junta sílabas, frases y un cuento. Se juega tocando, con voz · Gratis · Academia Esparta.')
    doc = PLANTILLA
    for k, v in {
        '%%TITULO%%': E(f'{titulo_letra} · Interactiva · 1º Primaria'), '%%DESC%%': E(desc), '%%URL%%': url,
        '%%COLOR%%': color, '%%REL%%': REL, '%%DATOS%%': json.dumps(datos, ensure_ascii=False).replace('</', '<\\/'),
        '%%NOMBRE%%': E(nombre), '%%TITULOLETRA%%': E(titulo_letra),
    }.items():
        doc = doc.replace(k, v)
    open(os.path.join(SALIDA, f'{A}-interactiva.html'), 'w', encoding='utf8').write(doc)
    print(f'✓ {A}-interactiva.html ({len(datos["audio"])} de {len(textos_voz(d)) + len(CONSIGNAS) + len(ELOGIOS) + 1} audios de Sara)')
    return True


PLANTILLA = r'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>%%TITULO%%</title>
  <meta name="description" content="%%DESC%%">
  <link rel="canonical" href="%%URL%%">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Academia Esparta">
  <meta property="og:title" content="%%TITULO%%">
  <meta property="og:description" content="%%DESC%%">
  <meta property="og:url" content="%%URL%%">
  <meta property="og:image" content="https://academiaesparta.es/og-image.jpg">
  <meta name="theme-color" content="%%COLOR%%">
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet" />
  <style>
    @font-face { font-family:'Playwrite ES'; src:url('%%REL%%fuentes/playwrite-es.woff2') format('woff2'); font-display:swap; }
    :root { --c:%%COLOR%%; --ok:#16a34a; --mal:#dc2626; --oro:#f59e0b; }
    * { box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
    html, body { margin:0; min-height:100%; }
    body { font-family:'Poppins',system-ui,sans-serif; color:#1e293b; overflow-x:hidden;
           background:radial-gradient(circle at 15% 10%, color-mix(in srgb, var(--c) 22%, #fff) 0, transparent 45%),
                      radial-gradient(circle at 85% 90%, color-mix(in srgb, var(--oro) 25%, #fff) 0, transparent 45%),
                      color-mix(in srgb, var(--c) 9%, #fffdf6); }
    .pw { font-family:'Playwrite ES',cursive; }
    /* burbujas del fondo */
    .burbujas { position:fixed; inset:0; pointer-events:none; z-index:0; overflow:hidden; }
    .burbujas span { position:absolute; bottom:-120px; border-radius:50%; opacity:.18; animation:sube linear infinite; }
    @keyframes sube { to { transform:translateY(-120vh) rotate(360deg); } }
    /* barra de arriba */
    .barra { position:sticky; top:0; z-index:5; display:flex; align-items:center; gap:10px; padding:10px 16px;
             background:color-mix(in srgb, #fff 82%, transparent); backdrop-filter:blur(10px); border-bottom:1px solid color-mix(in srgb, var(--c) 20%, #fff); }
    .barra a, .barra button { font:600 .82rem 'Poppins',sans-serif; color:var(--c); text-decoration:none; background:#fff; border:2px solid color-mix(in srgb, var(--c) 30%, #fff);
             border-radius:999px; padding:.4rem .85rem; cursor:pointer; white-space:nowrap; }
    .barra .marca { font-weight:800; color:#064e3b; margin-right:auto; font-size:.95rem; }
    .progreso { display:flex; gap:6px; justify-content:center; padding:14px 0 4px; position:relative; z-index:1; }
    .progreso i { width:34px; height:8px; border-radius:99px; background:color-mix(in srgb, var(--c) 18%, #fff); transition:background .3s, transform .3s; }
    .progreso i.hecho { background:var(--c); }
    .progreso i.ahora { background:var(--oro); transform:scaleY(1.4); }
    main { position:relative; z-index:1; max-width:780px; margin:0 auto; padding:10px 16px 60px; }
    .paso { display:none; animation:entra .45s cubic-bezier(.34,1.56,.64,1); }
    .paso.activo { display:block; }
    @keyframes entra { from { opacity:0; transform:translateY(24px) scale(.97); } }
    .tarjeta { background:#fff; border-radius:28px; padding:24px 22px 26px; box-shadow:0 10px 0 color-mix(in srgb, var(--c) 25%, #fff), 0 22px 40px -18px rgba(0,0,0,.25);
               border:3px solid color-mix(in srgb, var(--c) 18%, #fff); }
    .titulo { display:flex; align-items:center; gap:12px; margin:0 0 6px; }
    .titulo b { flex:none; width:42px; height:42px; border-radius:50%; background:var(--c); color:#fff; display:grid; place-items:center; font-size:1.2rem; }
    .titulo h2 { margin:0; font-size:1.25rem; color:#0f172a; }
    .consigna { margin:0 0 18px 54px; color:#475569; font-size:.95rem; }
    .voz { border:none; background:color-mix(in srgb, var(--c) 14%, #fff); color:var(--c); border-radius:999px; font:700 .85rem 'Poppins'; padding:.35rem .8rem; cursor:pointer; }
    .voz:hover { background:var(--c); color:#fff; }
    body.sin-voz .voz { display:none; }
    .siguiente { display:none; margin:22px auto 0; font:800 1.15rem 'Poppins'; color:#fff; background:var(--oro); border:none; border-radius:999px;
                 padding:.8rem 2.2rem; cursor:pointer; box-shadow:0 6px 0 #b45309; animation:late 1.2s ease-in-out infinite; }
    .siguiente.ver { display:block; }
    .siguiente:active { transform:translateY(4px); box-shadow:0 2px 0 #b45309; }
    @keyframes late { 50% { transform:scale(1.06); } }
    .emo { font-size:2rem; line-height:1; }
    .emo img, img.emo-img { width:1em; height:1em; vertical-align:-.12em; }
    /* bienvenida */
    .portada { text-align:center; padding:28px 10px 10px; }
    .portada .letrota { font-family:'Playwrite ES',cursive; font-size:min(34vw,9rem); color:var(--c); line-height:1.2;
                        display:inline-block; animation:bota 1.6s ease-in-out infinite; text-shadow:0 8px 0 color-mix(in srgb, var(--c) 22%, #fff); }
    @keyframes bota { 50% { transform:translateY(-14px) rotate(-3deg); } }
    .portada h1 { margin:6px 0 4px; font-size:1.6rem; color:#0f172a; }
    .portada p { margin:0 0 22px; color:#475569; }
    .grande { font:800 1.35rem 'Poppins'; color:#fff; background:var(--c); border:none; border-radius:999px; padding:.95rem 2.6rem; cursor:pointer;
              box-shadow:0 7px 0 color-mix(in srgb, var(--c) 60%, #000); }
    .grande:active { transform:translateY(5px); box-shadow:0 2px 0 color-mix(in srgb, var(--c) 60%, #000); }
    /* paso 1 */
    .conozco { display:flex; gap:22px; align-items:center; flex-wrap:wrap; justify-content:center; }
    .par-letras { font-family:'Playwrite ES',cursive; font-size:5.2rem; color:var(--c); line-height:1.25; display:flex; gap:14px; }
    .par-letras span { background:color-mix(in srgb, var(--c) 9%, #fff); border-radius:22px; padding:0 18px; border:3px dashed color-mix(in srgb, var(--c) 35%, #fff); }
    .pal-intro { display:flex; flex-direction:column; gap:10px; }
    .pal-btn { display:flex; align-items:center; gap:12px; background:#fff; border:3px solid color-mix(in srgb, var(--c) 20%, #fff); border-radius:18px;
               padding:8px 16px; cursor:pointer; font-size:1.7rem; transition:transform .15s; }
    .pal-btn:hover { transform:scale(1.04); border-color:var(--c); }
    .pal-btn .v { color:var(--c); font-weight:700; }
    .suena { text-align:center; color:#334155; margin:18px 0 10px; font-size:1rem; }
    .chips { display:flex; gap:10px; justify-content:center; flex-wrap:wrap; }
    .chip { font-family:'Playwrite ES',cursive; font-size:1.7rem; min-width:76px; padding:8px 14px 12px; border-radius:16px; cursor:pointer; background:#fff;
            border:3px solid color-mix(in srgb, var(--c) 25%, #fff); color:#0f172a; transition:transform .15s, background .15s; }
    .chip:hover { transform:translateY(-3px); border-color:var(--c); }
    .chip.toque { background:var(--c); color:#fff; animation:pop .35s; }
    .como-suena { margin:18px auto 14px; max-width:460px; text-align:center; background:#fffbeb; border:3px dashed var(--oro); border-radius:22px; padding:12px 16px 14px; }
    .como-suena h3 { margin:0; font-size:1.05rem; color:#92400e; }
    .como-suena .muestra { font-family:'Playwrite ES',cursive; font-size:3rem; color:var(--c); line-height:1.5; letter-spacing:.06em; }
    .como-suena p { margin:0; color:#78350f; font-weight:600; font-size:.95rem; }
    /* paso 2 */
    .toca-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(270px,1fr)); gap:12px; }
    .toca-it { display:flex; align-items:center; gap:10px; background:color-mix(in srgb, var(--c) 5%, #fff); border-radius:18px; padding:8px 10px;
               border:2px solid color-mix(in srgb, var(--c) 15%, #fff); transition:background .3s, border-color .3s; }
    .toca-it.listo { background:#ecfdf5; border-color:#86efac; }
    .letras { display:flex; flex-wrap:nowrap; gap:1px; flex:1; min-width:0; }
    .lt { font:600 1.4rem 'Poppins'; min-width:26px; height:46px; border:none; background:transparent; border-radius:12px; cursor:pointer; color:#0f172a; padding:0 4px; }
    .lt.min { font-family:'Playwrite ES',cursive; font-weight:400; font-size:1.55rem; }
    .lt:hover { background:color-mix(in srgb, var(--c) 12%, #fff); }
    .lt.bien { background:var(--ok); color:#fff; animation:pop .35s; }
    .lt.mal { animation:tiembla .4s; color:var(--mal); }
    .ninguna { font:700 .72rem 'Poppins'; border:2px dashed #94a3b8; background:#fff; color:#475569; border-radius:10px; padding:4px 7px; cursor:pointer; }
    .ninguna.bien { background:var(--ok); color:#fff; border-color:var(--ok); }
    .ninguna.mal { animation:tiembla .4s; border-color:var(--mal); color:var(--mal); }
    .marcador { font:800 .9rem 'Poppins'; color:var(--c); white-space:nowrap; }
    /* pasos 3-5 */
    .reto { text-align:center; }
    .reto .dibujo { font-size:4.6rem; line-height:1.1; display:inline-block; animation:bota 2s ease-in-out infinite; }
    .reto .dibujo img { width:1em; height:1em; }
    .reto .palabra { font-family:'Playwrite ES',cursive; font-size:2.6rem; margin:8px 0 18px; letter-spacing:.02em; }
    .hueco { display:inline-block; min-width:2.2em; border-bottom:4px solid var(--c); color:var(--c); margin:0 2px; }
    .hueco.lleno { border-color:var(--ok); color:var(--ok); animation:pop .35s; }
    .opciones { display:flex; gap:12px; justify-content:center; flex-wrap:wrap; }
    .op { font-family:'Playwrite ES',cursive; font-size:1.8rem; min-width:84px; padding:8px 16px 14px; border-radius:18px; cursor:pointer; background:#fff;
          border:3px solid color-mix(in srgb, var(--c) 25%, #fff); box-shadow:0 5px 0 color-mix(in srgb, var(--c) 25%, #fff); color:#0f172a; }
    .op:hover { border-color:var(--c); }
    .op.bien { background:var(--ok); border-color:var(--ok); color:#fff; box-shadow:0 5px 0 #166534; animation:pop .35s; }
    .op.mal { animation:tiembla .4s; border-color:var(--mal); color:var(--mal); }
    .op.usada { opacity:.25; pointer-events:none; }
    .cuenta-reto { color:#64748b; font:700 .85rem 'Poppins'; margin-top:16px; }
    .huecos-junta { display:flex; gap:8px; justify-content:center; margin:6px 0 18px; min-height:62px; }
    .huecos-junta span { font-family:'Playwrite ES',cursive; font-size:2rem; min-width:72px; padding:4px 10px 10px; border-bottom:4px solid color-mix(in srgb, var(--c) 40%, #fff); }
    .huecos-junta span.lleno { border-color:var(--ok); color:var(--ok); animation:pop .35s; }
    .frase { font-family:'Playwrite ES',cursive; font-size:1.65rem; line-height:2.1; margin:4px 0 18px; }
    /* paso 6 */
    .cuento { font-family:'Playwrite ES',cursive; font-size:1.45rem; line-height:2.05; background:color-mix(in srgb, var(--c) 6%, #fff);
              border-radius:20px; padding:14px 20px; border:3px dashed color-mix(in srgb, var(--c) 30%, #fff); margin-bottom:16px; }
    .preg { margin:14px 0; }
    .preg p { margin:0 0 8px; font-weight:700; font-size:1.05rem; }
    .preg .opciones { justify-content:flex-start; }
    .preg .op { font-size:1.35rem; min-width:0; }
    /* final */
    .final { text-align:center; padding:20px 0 6px; }
    .final .copa { font-size:5.5rem; display:inline-block; animation:bota 1.4s ease-in-out infinite; }
    .final h2 { font-size:2rem; margin:6px 0; color:var(--c); }
    .estrellas { font-size:2.6rem; letter-spacing:.2em; margin:6px 0 18px; }
    .estrellas span { display:inline-block; animation:pop .5s backwards; }
    .acciones { display:flex; gap:10px; justify-content:center; flex-wrap:wrap; }
    .acciones a, .acciones button { font:700 1rem 'Poppins'; text-decoration:none; border-radius:999px; padding:.7rem 1.4rem; cursor:pointer; border:3px solid var(--c); color:var(--c); background:#fff; }
    .acciones .lleno { background:var(--c); color:#fff; }
    /* Leoni, la mascota (22-nov-2026): asomado a la esquina de arriba a la derecha de la tarjeta */
    .tarjeta { position:relative; }
    /* Leoni de pie en el lateral izquierdo, fuera de la tarjeta y fijo al bajar (decidido por Miguel el 22-nov-2026) */
    .mascota { position:fixed; left:max(12px, calc(50% - 390px - 215px)); top:46%; transform:translateY(-50%); width:190px; z-index:4; pointer-events:none; transform-origin:50% 100%; }
    .mascota img { width:100%; height:auto; display:block; filter:drop-shadow(0 8px 8px rgba(0,0,0,.18)); animation:respira 3s ease-in-out infinite; transition:opacity .11s; }
    .mascota.habla img { animation:asiente .5s ease-in-out infinite; }
    @keyframes asiente { 0%,100% { transform:rotate(0) translateY(0); } 50% { transform:rotate(-2.5deg) translateY(-3px); } }
    @keyframes respira { 50% { transform:translateY(-3px) rotate(-1deg); } }
    .mascota.salta img { animation:salta .6s cubic-bezier(.3,1.6,.5,1); }
    @keyframes salta { 30% { transform:translateY(-26px) rotate(-6deg); } 60% { transform:translateY(0) scale(1.06,.94); } }
    .mascota.uy img { animation:uy .5s; }
    @keyframes uy { 25% { transform:rotate(-7deg); } 75% { transform:rotate(7deg); } }
    .portada { position:relative; }
    .portada-leo { display:flex; align-items:flex-end; justify-content:center; gap:6px; margin-bottom:4px; }
    .portada-leo img { width:min(30vw,150px); height:auto; animation:bota 1.8s ease-in-out infinite; filter:drop-shadow(0 10px 10px rgba(0,0,0,.18)); }
    .bocadillo { position:relative; background:#fff; border:3px solid var(--c); border-radius:20px; padding:8px 14px; font:800 1.05rem 'Poppins'; color:var(--c); margin-bottom:90px; white-space:nowrap; }
    .bocadillo::after { content:''; position:absolute; left:-12px; bottom:14px; border:9px solid transparent; border-right-color:var(--c); border-left:0; }
    .final .leo-fin { width:150px; height:auto; display:block; margin:0 auto -6px; animation:bota 1.4s ease-in-out infinite; }
    @media (max-width:1200px) { .mascota { left:8px; top:auto; bottom:4px; transform:none; width:96px; } main { padding-bottom:190px; } }
    @media (max-width:560px) { .mascota { width:78px; } main { padding-bottom:160px; } }
    /* piezas que vuelan */
    .volando { position:fixed; z-index:14; margin:0; pointer-events:none; transition:transform .45s cubic-bezier(.5,0,.3,1.25), opacity .45s; }
    .huecos-junta.unidas { animation:unidas .6s cubic-bezier(.34,1.56,.64,1); }
    .huecos-junta.unidas span { margin:0 -4px; transition:margin .3s; }
    @keyframes unidas { 40% { transform:scale(1.15); } }
    /* álbum de pegatinas */
    .pegatina-nueva { font-size:5rem; display:inline-block; animation:pega 1s cubic-bezier(.34,1.56,.64,1) .4s backwards; filter:drop-shadow(0 6px 0 rgba(0,0,0,.12)); }
    @keyframes pega { 0% { transform:scale(3) rotate(-30deg); opacity:0; } 100% { transform:scale(1) rotate(0); opacity:1; } }
    .album { margin:20px auto 6px; max-width:640px; background:#fffbeb; border:3px solid #fcd34d; border-radius:22px; padding:12px 12px 16px; }
    .album h3 { margin:2px 0 10px; color:#92400e; font-size:1.05rem; }
    .album-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(64px,1fr)); gap:8px; }
    .casilla { aspect-ratio:1; border-radius:14px; background:#fff; border:2px dashed #e5c07b; display:flex; flex-direction:column; align-items:center; justify-content:center; text-decoration:none; color:#a16207; font-size:.72rem; font-weight:700; }
    .casilla .e { font-size:1.6rem; line-height:1.1; filter:grayscale(1) opacity(.25); }
    .casilla.tiene { border:2px solid var(--oro); box-shadow:0 3px 0 #fcd34d; }
    .casilla.tiene .e { filter:none; }
    .casilla.esta { animation:pop .6s 1.2s backwards; outline:3px solid var(--c); }
    .portada .album-link { display:inline-block; margin-top:14px; font:700 .9rem 'Poppins'; color:#92400e; background:#fffbeb; border:2px solid #fcd34d; border-radius:999px; padding:.35rem .9rem; text-decoration:none; cursor:pointer; }
    @media (max-width:560px) { .mascota { width:78px; } }
    .cartel { position:fixed; left:50%; top:42%; z-index:15; transform:translate(-50%,-50%) scale(.6); opacity:0; pointer-events:none;
              background:#fff; border:4px solid var(--oro); border-radius:28px; padding:18px 30px; text-align:center; box-shadow:0 18px 40px -10px rgba(0,0,0,.35);
              font:800 1.6rem 'Poppins'; color:var(--c); max-width:90vw; transition:transform .35s cubic-bezier(.34,1.56,.64,1), opacity .25s; }
    .cartel .estrella { display:block; font-size:3.2rem; animation:pop .6s; }
    .cartel.ver { transform:translate(-50%,-50%) scale(1); opacity:1; }
    .confeti { position:fixed; top:-20px; width:10px; height:16px; z-index:20; pointer-events:none; animation:cae linear forwards; }
    @keyframes cae { to { transform:translateY(110vh) rotate(720deg); } }
    @keyframes pop { 0% { transform:scale(.7); } 60% { transform:scale(1.18); } 100% { transform:scale(1); } }
    @keyframes tiembla { 20%,60% { transform:translateX(-6px); } 40%,80% { transform:translateX(6px); } }
    @media (max-width:560px) {
      .barra .marca { display:none; }
      .par-letras { font-size:3.8rem; } .reto .palabra { font-size:2.1rem; } .frase { font-size:1.35rem; }
      .tarjeta { padding:18px 14px 22px; border-radius:22px; } .consigna { margin-left:0; }
    }
    @media (prefers-reduced-motion:reduce) { *, *::before, *::after { animation:none !important; transition:none !important; } .burbujas { display:none; } }
  </style>
</head>
<body>
<div class="burbujas" aria-hidden="true"></div>
<div class="barra">
  <span class="marca">Academia Esparta</span>
  <a href="%%REL%%materiales.html">← Volver</a>
  <a id="btn-pdf" href="#" target="_blank" rel="noopener" data-umami-event="pdf-desde-interactiva">📄 Para imprimir</a>
  <button id="btn-sonido" type="button" aria-label="Sonido">🔔</button>
</div>
<div class="progreso" id="progreso" aria-hidden="true"></div>
<main id="app"></main>
<div class="cartel" id="cartel" aria-live="polite"></div>
<div class="mascota" id="mascota" aria-hidden="true"><img id="leo" src="%%REL%%mascota/leoni/contento.webp" alt=""></div>

<script>
const D = %%DATOS%%;
const REL = '%%REL%%';
const $ = s => document.querySelector(s);
const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
const esc = t => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const emo = e => { const m = /^\[([a-z-]+)\]$/.exec(e || ''); return m ? `<img class="emo-img" src="${REL}emoji-propios/${m[1]}.svg" alt="${m[1]}">` : esc(e || ''); };
const mezcla = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const frase = (a, w, b) => (w === '...' && b === '.') ? `${a}...` : `${a} ${w}${b.startsWith('.') ? '' : ' '}${b}`;
const plegar = t => t.normalize('NFD').replace(/[́̈]/g, '').normalize('NFC').toLowerCase(); // á→a, ü→u, la ñ se queda
$('#btn-pdf').href = D.pdf;

/* ── burbujas ── */
(() => { const b = $('.burbujas'); const cols = ['var(--c)', 'var(--oro)', '#38bdf8', '#f472b6'];
  for (let i = 0; i < 14; i++) { const s = el('span'); const t = 30 + Math.random() * 90;
    Object.assign(s.style, { left: Math.random() * 100 + '%', width: t + 'px', height: t + 'px', background: cols[i % 4],
      animationDuration: 14 + Math.random() * 16 + 's', animationDelay: -Math.random() * 20 + 's' }); b.appendChild(s); } })();

/* ── sonidos (Web Audio, sin ficheros) ── */
let sonido = true, ac = null;
$('#btn-sonido').onclick = () => { sonido = !sonido; $('#btn-sonido').textContent = sonido ? '🔔' : '🔕'; };
function tono(notas) {
  if (!sonido) return;
  try { ac = ac || new (window.AudioContext || window.webkitAudioContext)();
    notas.forEach(([f, t, d]) => { const o = ac.createOscillator(), g = ac.createGain(); o.type = 'triangle'; o.frequency.value = f;
      g.gain.setValueAtTime(.0001, ac.currentTime + t); g.gain.exponentialRampToValueAtTime(.22, ac.currentTime + t + .02);
      g.gain.exponentialRampToValueAtTime(.0001, ac.currentTime + t + d); o.connect(g).connect(ac.destination); o.start(ac.currentTime + t); o.stop(ac.currentTime + t + d + .05); });
  } catch (e) {}
}
const mascota = document.getElementById('mascota'), leo = document.getElementById('leo');
const CARAS = {}; ['contento', 'celebrando', 'uy', 'pulgar'].forEach(c => { const i = new Image(); i.src = REL + 'mascota/leoni/' + c + '.webp'; CARAS[c] = i.src; });
let hablando = false, caraFija = null;
function cara(c) { if (!leo || !CARAS[c] || leo.src === CARAS[c]) return; leo.style.opacity = '0';
  clearTimeout(cara.t); cara.t = setTimeout(() => { leo.src = CARAS[c]; leo.style.opacity = '1'; }, 110); }
function caraTemporal(c, ms, mov) { caraFija = c; cara(c); if (mov) { mascota.classList.remove('salta', 'uy'); void mascota.offsetWidth; mascota.classList.add(mov); }
  clearTimeout(caraTemporal.t); caraTemporal.t = setTimeout(() => { caraFija = null; mascota.classList.remove('salta', 'uy'); cara('contento'); }, ms); }
function habla(si) { hablando = si; if (mascota) mascota.classList.toggle('habla', si); }
const bien = () => { tono([[660, 0, .12], [990, .1, .2]]); caraTemporal('pulgar', 800, 'salta'); };
const mal = () => { tono([[220, 0, .18]]); caraTemporal('uy', 900, 'uy'); };
function suena(a) { a.addEventListener('playing', () => habla(true)); ['ended', 'pause', 'error'].forEach(ev => a.addEventListener(ev, () => habla(false))); a.play().catch(() => habla(false)); }
const fanfarria = () => tono([[523, 0, .15], [659, .15, .15], [784, .3, .15], [1047, .45, .4]]);

/* ── voz del dispositivo ── */
let vozEs = null;
function cargaVoces() { const v = (window.speechSynthesis ? speechSynthesis.getVoices() : []);
  vozEs = v.find(x => /^es[-_]ES/i.test(x.lang)) || v.find(x => /^es/i.test(x.lang)) || null;
  document.body.classList.toggle('sin-voz', !vozEs && !Object.keys(D.audio).length); }
if (window.speechSynthesis) { cargaVoces(); speechSynthesis.onvoiceschanged = cargaVoces; } else document.body.classList.add('sin-voz');
let sonando = null;
function di(texto, cola) { if (!sonido) return; texto = texto.trim();
  if (D.audio[texto]) { const a = new Audio(D.audio[texto]);
    if (cola && sonando && !sonando.paused && !sonando.ended) { sonando.onended = () => { sonando = a; suena(a); }; return; }
    if (sonando) { sonando.onended = null; sonando.pause(); } if (window.speechSynthesis) speechSynthesis.cancel(); sonando = a; suena(a); return; }
  if (!vozEs) return; speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(texto); u.voice = vozEs; u.lang = vozEs.lang; u.rate = .85; u.onstart = () => habla(true); u.onend = u.onerror = () => habla(false); speechSynthesis.speak(u); }

/* ── confeti ── */
function confeti(n = 90) { const cols = ['#f59e0b', '#16a34a', '#2563eb', '#db2777', '#7c3aed', '#f97316'];
  for (let i = 0; i < n; i++) { const c = el('div', 'confeti'); Object.assign(c.style, { left: Math.random() * 100 + 'vw', background: cols[i % cols.length],
    animationDuration: 1.8 + Math.random() * 1.8 + 's', animationDelay: Math.random() * .6 + 's', borderRadius: i % 3 ? '2px' : '50%' });
    document.body.appendChild(c); setTimeout(() => c.remove(), 4500); } }

/* ── pasos ── */
const PASOS = ['Conozco la letra', 'Toca la letra', '¿Qué sílaba falta?', 'Junto sílabas', 'Completa la frase', 'Leo el cuento'];
const app = $('#app'), prog = $('#progreso');
PASOS.forEach(() => prog.appendChild(el('i')));
let actual = -1;
function pintaProgreso() { [...prog.children].forEach((x, i) => { x.className = i < actual ? 'hecho' : i === actual ? 'ahora' : ''; }); }
function tarjeta(n, consigna, vozTexto) {
  const t = el('section', 'paso'), c = el('div', 'tarjeta');
  c.innerHTML = `<div class="titulo"><b>${n + 1}</b><h2>${PASOS[n]}</h2></div><p class="consigna">${consigna} <button class="voz rep" type="button">🔊 Repetir</button>${vozTexto ? ' <button class="voz cue" type="button">📖 Escuchar el cuento</button>' : ''}</p>`;
  c.querySelector('.rep').onclick = () => di(D.consignas[n]);
  if (vozTexto) c.querySelector('.cue').onclick = () => di(vozTexto);
  const cuerpo = el('div'); c.appendChild(cuerpo);
  const sig = el('button', 'siguiente', n === PASOS.length - 1 ? '¡Terminar! 🏆' : '¡Siguiente! ➜'); sig.type = 'button'; c.appendChild(sig);
  sig.onclick = () => ir(n + 1);
  t.appendChild(c); app.appendChild(t);
  return { t, cuerpo, listo: () => { felicita(); setTimeout(() => { sig.classList.add('ver'); sig.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 1600); } };
}
const quieto = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
function vuela(desde, hasta, alLlegar) {
  if (quieto || !desde.getBoundingClientRect) { alLlegar(); return; }
  const a = desde.getBoundingClientRect(), b = hasta.getBoundingClientRect();
  const c = desde.cloneNode(true); c.classList.add('volando'); c.classList.remove('mal');
  Object.assign(c.style, { left: a.left + 'px', top: a.top + 'px', width: a.width + 'px', height: a.height + 'px' });
  document.body.appendChild(c); desde.style.visibility = 'hidden';
  requestAnimationFrame(() => requestAnimationFrame(() => {
    const dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
    c.style.transform = `translate(${dx}px, ${dy}px) scale(.8)`; c.style.opacity = '.2'; }));
  setTimeout(() => { c.remove(); alLlegar(); }, 470);
}
let ultimoElogio = -1;
function felicita() {
  let i; do { i = Math.floor(Math.random() * D.elogios.length); } while (i === ultimoElogio && D.elogios.length > 1); ultimoElogio = i;
  const txt = D.elogios[i]; tono([[660, 0, .12], [880, .12, .12], [1175, .24, .3]]); confeti(40); di(txt, true); caraTemporal('celebrando', 1700, 'salta');
  const c = $('#cartel'); c.innerHTML = `<span class="estrella">⭐</span>${esc(txt)}`; c.classList.add('ver');
  clearTimeout(felicita.t); felicita.t = setTimeout(() => c.classList.remove('ver'), 1800);
}
mascota.style.display = 'none';
const pasos = [];
function ir(n, cola) {
  document.querySelectorAll('.paso').forEach(p => p.classList.remove('activo'));
  actual = n; pintaProgreso();
  if (n >= PASOS.length) { mascota.style.display = 'none'; albumGuardar(D.archivo); $('#final .album-hueco').innerHTML = albumHtml(D.archivo); $('#final').classList.add('activo'); fanfarria(); confeti(); setTimeout(() => di(D.final), 700); }
  else { pasos[n].t.classList.add('activo'); mascota.style.display = ''; di(D.consignas[n], cola); if (pasos[n].alEntrar) pasos[n].alEntrar(); }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* álbum de pegatinas (se guarda en este navegador) */
const CLAVE_ALBUM = 'esparta-album-letras';
function albumLeer() { try { return JSON.parse(localStorage.getItem(CLAVE_ALBUM) || '[]'); } catch (e) { return []; } }
function albumGuardar(a) { try { const l = albumLeer(); if (!l.includes(a)) { l.push(a); localStorage.setItem(CLAVE_ALBUM, JSON.stringify(l)); } } catch (e) {} }
function albumHtml(nueva) { const l = albumLeer();
  return `<div class="album"><h3>📒 Mi álbum de letras · ${l.length} de ${D.album.length}</h3><div class="album-grid">` +
    D.album.map(x => `<a class="casilla${l.includes(x.a) ? ' tiene' : ''}${x.a === nueva ? ' esta' : ''}" href="${x.a}-interactiva.html" title="Letra ${esc(x.ver)}"><span class="e">${emo(x.emo)}</span>${esc(x.ver)}</a>`).join('') + '</div></div>'; }

/* portada */
const portada = el('section', 'paso activo');
portada.innerHTML = `<div class="tarjeta portada"><div class="portada-leo"><img src="${REL}mascota/leoni/frente.webp" alt="Leoni, la mascota de Academia Esparta"><span class="bocadillo">¡Hola! Soy Leoni</span></div><div class="letrota">${esc(D.mayus.charAt(0) + D.mayus.slice(1).toLowerCase())} ${esc(D.letra)}</div>
  <h1>Vamos a aprender la ${esc(D.nombre)}</h1><p>Seis juegos cortos. ¡Termínalos y gana la pegatina de esta letra!</p>
  <button class="grande" type="button">¡Empezar! 🚀</button>${albumLeer().length ? `<br><span class="album-link">📒 Mi álbum: ${albumLeer().length} de ${D.album.length} pegatinas</span>` : ''}</div>`;
portada.querySelector('.grande').onclick = () => { di(D.saludo); ir(0, true); };
app.appendChild(portada);

/* 1 · conozco la letra */
(() => { const p = tarjeta(0, 'Mira la letra. Toca los dibujos para oír las palabras y toca las sílabas.', null);
  const pal = D.intro.palabras.map(([e, w]) => `<button class="pal-btn" type="button" data-w="${esc(w)}"><span class="emo">${emo(e)}</span><span class="pw">${marcaLetra(w)}</span></button>`).join('');
  p.cuerpo.innerHTML = `<div class="conozco"><div class="par-letras"><span>${esc(D.mayus.charAt(0) + D.mayus.slice(1).toLowerCase())}</span><span>${esc(D.letra)}</span></div><div class="pal-intro">${pal}</div></div>
    <div class="como-suena"><h3>¿Cómo suena la ${esc(D.nombre.replace(/\s*\(.*\)/, ''))}?</h3><div class="muestra">${esc(D.suena[0])}</div><p>${esc(D.suena[1])}</p></div><div class="chips">${D.silabas.map(s => `<button class="chip" type="button">${esc(s)}</button>`).join('')}</div>`;
  const vistos = new Set();
  const comprueba = () => { if (vistos.size >= D.intro.palabras.length + Math.min(3, D.silabas.length)) p.listo(); };
  p.cuerpo.querySelectorAll('.pal-btn').forEach(b => b.onclick = () => { di(b.dataset.w); b.style.borderColor = 'var(--ok)'; vistos.add('p' + b.dataset.w); comprueba(); });
  p.cuerpo.querySelectorAll('.chip').forEach(b => b.onclick = () => { di(b.textContent); b.classList.remove('toque'); void b.offsetWidth; b.classList.add('toque'); vistos.add('s' + b.textContent); comprueba(); });
  const ayuda = el('p', 'cuenta-reto', 'Toca las dos palabras y por lo menos tres sílabas.'); p.cuerpo.appendChild(ayuda);
  pasos.push(p); })();

function marcaLetra(w) { const L = plegar(D.letra), n = D.letra.length; let o = '', i = 0;
  while (i < w.length) { if (plegar(w.substr(i, n)) === L) { o += `<span class="v">${esc(w.substr(i, n))}</span>`; i += n; } else { o += esc(w[i]); i++; } } return o; }

/* 2 · toca la letra */
(() => { const p = tarjeta(1, `Toca todas las <b class="pw" style="color:var(--c);font-size:1.3em">${esc(D.mayus.charAt(0) + D.mayus.slice(1).toLowerCase())}</b> y <b class="pw" style="color:var(--c);font-size:1.3em">${esc(D.letra)}</b> de cada palabra. Si una palabra no tiene ninguna, toca «No tiene».`, null);
  const L = plegar(D.letra), n = D.letra.length; let faltan = 0;
  const grid = el('div', 'toca-grid'); p.cuerpo.appendChild(grid);
  const marc = el('p', 'cuenta-reto'); p.cuerpo.appendChild(marc);
  const items = mezcla(D.toca);
  let palabrasHechas = 0;
  items.forEach(([w, e]) => {
    const it = el('div', 'toca-it'); it.innerHTML = `<span class="emo">${emo(e)}</span>`;
    const ls = el('div', 'letras'); it.appendChild(ls);
    const esMayus = w === w.toUpperCase();
    let i = 0, tiene = 0;
    while (i < w.length) { const trozo = plegar(w.substr(i, n)) === L ? w.substr(i, n) : w[i]; const es = plegar(trozo) === L && trozo.length === n;
      const b = el('button', 'lt' + (esMayus ? '' : ' min'), esc(trozo)); b.type = 'button'; if (es) tiene++;
      b.onclick = () => { if (b.classList.contains('bien')) return;
        if (es) { b.classList.add('bien'); bien(); quedan--; if (quedan === 0) hecha(); }
        else { b.classList.remove('mal'); void b.offsetWidth; b.classList.add('mal'); mal(); } };
      ls.appendChild(b); i += trozo.length; }
    let quedan = tiene; faltan += tiene ? 1 : 1;
    const hecha = () => { it.classList.add('listo'); palabrasHechas++; marcador(); if (palabrasHechas === items.length) p.listo(); };
    const ning = el('button', 'ninguna', 'No tiene'); ning.type = 'button';
    ning.onclick = () => { if (it.classList.contains('listo')) return;
      if (!tiene) { ning.classList.add('bien'); bien(); hecha(); } else { ning.classList.remove('mal'); void ning.offsetWidth; ning.classList.add('mal'); mal(); } };
    it.appendChild(ning); grid.appendChild(it);
  });
  const marcador = () => marc.textContent = `Palabras terminadas: ${palabrasHechas} de ${items.length}`; marcador();
  pasos.push(p); })();

/* 3 · ¿qué sílaba falta? */
(() => { const p = tarjeta(2, 'Mira el dibujo y escucha la palabra. Después, toca la sílaba que falta.', null);
  const rondas = mezcla(D.sil); let k = 0;
  const caja = el('div', 'reto'); p.cuerpo.appendChild(caja);
  function ronda() {
    const r = rondas[k];
    const antes = r.w.slice(0, r.ini), despues = r.w.slice(r.fin);
    caja.innerHTML = `<div class="dibujo">${emo(r.e)}</div><div class="palabra">${esc(antes)}<span class="hueco">&nbsp;</span>${esc(despues)}
      <button class="voz" type="button" title="Escuchar">🔊</button></div><div class="opciones"></div><p class="cuenta-reto">${k + 1} de ${rondas.length}</p>`;
    caja.querySelector('.voz').onclick = () => di(r.w);
    if (k > 0) di(r.w);
    const ops = caja.querySelector('.opciones');
    mezcla([...new Set(D.silabas.concat(r.s))]).forEach(s => { const b = el('button', 'op', esc(s)); b.type = 'button';
      b.onclick = () => { if (s === r.s) { b.classList.add('bien'); const h = caja.querySelector('.hueco'); bien(); vuela(b, h, () => { h.textContent = r.w.slice(r.ini, r.fin); h.classList.add('lleno'); }); di(r.w);
          ops.querySelectorAll('.op').forEach(x => x.disabled = true);
          setTimeout(() => { k++; k < rondas.length ? ronda() : (caja.innerHTML = '<div class="dibujo">🎉</div><p class="palabra">¡Todas!</p>', p.listo()); }, 1100); }
        else { b.classList.remove('mal'); void b.offsetWidth; b.classList.add('mal'); mal(); } };
      ops.appendChild(b); });
  }
  ronda(); p.alEntrar = () => di(rondas[0].w, true); pasos.push(p); })();

/* 4 · junto sílabas */
(() => { const p = tarjeta(3, 'Mira el dibujo y toca las sílabas en orden para formar la palabra.', null);
  const rondas = mezcla(D.junta); let k = 0;
  const caja = el('div', 'reto'); p.cuerpo.appendChild(caja);
  function ronda() {
    const [e, ss] = rondas[k]; let pos = 0;
    caja.innerHTML = `<div class="dibujo">${emo(e)}</div><div class="huecos-junta">${ss.map(() => '<span>&nbsp;</span>').join('')}</div><div class="opciones"></div><p class="cuenta-reto">${k + 1} de ${rondas.length}</p>`;
    const huecos = caja.querySelectorAll('.huecos-junta span'), ops = caja.querySelector('.opciones');
    let piezas = ss.map((s, i) => ({ s, i })); do { piezas = mezcla(piezas); } while (ss.length > 1 && piezas.every((x, i) => x.i === i));
    piezas.forEach(({ s }) => { const b = el('button', 'op', esc(s)); b.type = 'button';
      b.onclick = () => { if (s === ss[pos]) { const hh = huecos[pos]; pos++; bien(); vuela(b, hh, () => { hh.textContent = s; hh.classList.add('lleno'); b.classList.add('usada'); b.style.visibility = ''; });
          if (pos === ss.length) { setTimeout(() => caja.querySelector('.huecos-junta').classList.add('unidas'), 520); di(ss.join('')); setTimeout(() => { k++; k < rondas.length ? ronda() : (caja.innerHTML = '<div class="dibujo">🎉</div><p class="palabra">¡Muy bien!</p>', p.listo()); }, 1200); } }
        else { b.classList.remove('mal'); void b.offsetWidth; b.classList.add('mal'); mal(); } };
      ops.appendChild(b); });
  }
  ronda(); pasos.push(p); })();

/* 5 · completa la frase */
(() => { const p = tarjeta(4, 'Escucha la frase y toca la palabra que falta.', null);
  const rondas = mezcla(D.frases); let k = 0;
  const caja = el('div', 'reto'); p.cuerpo.appendChild(caja);
  function ronda() {
    const [e, a, sol, b] = rondas[k];
    const tras = (b.startsWith('.') ? '' : ' ') + esc(b);
    caja.innerHTML = `<div class="dibujo">${emo(e)}</div><div class="frase">${esc(a)} <span class="hueco">&nbsp;</span>${tras}
      <button class="voz" type="button" title="Escuchar">🔊</button></div><div class="opciones"></div><p class="cuenta-reto">${k + 1} de ${rondas.length}</p>`;
    caja.querySelector('.voz').onclick = () => di(frase(a, '...', b));
    if (k > 0) di(frase(a, '...', b));
    const ops = caja.querySelector('.opciones');
    mezcla(D.banco).forEach(([w, ew]) => { const bt = el('button', 'op', `<span style="font-size:.8em">${emo(ew)}</span> ${esc(w)}`); bt.type = 'button';
      bt.onclick = () => { if (w === sol) { bt.classList.add('bien'); const h = caja.querySelector('.hueco'); bien(); vuela(bt, h, () => { h.textContent = w; h.classList.add('lleno'); }); di(frase(a, w, b));
          ops.querySelectorAll('.op').forEach(x => x.disabled = true);
          setTimeout(() => { k++; k < rondas.length ? ronda() : (caja.innerHTML = '<div class="dibujo">🎉</div><p class="palabra">¡Fenomenal!</p>', p.listo()); }, 1500); }
        else { bt.classList.remove('mal'); void bt.offsetWidth; bt.classList.add('mal'); mal(); } };
      ops.appendChild(bt); });
  }
  ronda(); p.alEntrar = () => { const [, a, , b] = rondas[0]; di(frase(a, '...', b), true); }; pasos.push(p); })();

/* 6 · el cuento */
(() => { const c = D.cuento;
  const p = tarjeta(5, 'Escucha el cuento. Después, toca la respuesta buena de cada pregunta.', c.lineas.join(' '));
  p.cuerpo.innerHTML = `<div class="cuento"><span class="emo">${emo(c.emoji)}</span> ${c.lineas.map(esc).join('<br>')}</div>`;
  let ok = 0;
  c.preguntas.forEach(([q, a, b], i) => {
    const pr = el('div', 'preg'); pr.innerHTML = `<p>${i + 1}. ${esc(q)} <button class="voz" type="button" title="Escuchar">🔊</button></p><div class="opciones"></div>`;
    pr.querySelector('.voz').onclick = () => di(q);
    const ops = pr.querySelector('.opciones');
    const buena = c.buenas[i];
    [a, b].forEach(x => { const bt = el('button', 'op', esc(x)); bt.type = 'button';
      bt.onclick = () => { if (x === buena) { bt.classList.add('bien'); bien(); ops.querySelectorAll('.op').forEach(y => y.disabled = true); ok++; if (ok === c.preguntas.length) p.listo(); }
        else { bt.classList.remove('mal'); void bt.offsetWidth; bt.classList.add('mal'); mal(); } };
      ops.appendChild(bt); });
    p.cuerpo.appendChild(pr); });
  pasos.push(p); })();


/* final */
const fin = el('section', 'paso'); fin.id = 'final';
const pegMia = (D.album.find(x => x.a === D.archivo) || {}).emo || '⭐';
fin.innerHTML = `<div class="tarjeta final"><img class="leo-fin" src="${REL}mascota/leoni/celebrando.webp" alt=""><h2>¡Lo has conseguido!</h2><p>Has ganado la pegatina de la ${esc(D.nombre)}:</p>
  <div class="pegatina-nueva">${emo(pegMia)}</div><div class="album-hueco"></div>
  <div class="acciones"><a class="lleno" href="${D.pdf}" target="_blank" rel="noopener">📄 Ficha para imprimir</a><button type="button" id="otra-vez">↺ Jugar otra vez</button><a href="${REL}materiales.html">Más letras</a></div></div>`;
app.appendChild(fin);
$('#otra-vez').onclick = () => location.reload();
</script>
</body>
</html>
'''

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args: print(__doc__); sys.exit(1)
    voz = '--voz' in args; args = [a for a in args if a != '--voz']
    if args == ['--todas']: args = ORDEN
    ok = all([generar(x, voz) for x in args])
    sys.exit(0 if ok else 1)
