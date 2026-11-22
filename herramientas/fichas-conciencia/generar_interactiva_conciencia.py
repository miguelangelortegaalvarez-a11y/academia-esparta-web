#!/usr/bin/env python3
"""Interactiva de una ficha de Conciencia fonológica de 1º, desde el MISMO JSON que la ficha de papel.

Uso (desde la raíz del repo):
    python3 herramientas/fichas-conciencia/generar_interactiva_conciencia.py reconocer-sonidos          # sin gastar créditos
    python3 herramientas/fichas-conciencia/generar_interactiva_conciencia.py reconocer-sonidos --voz    # + audios de Sara que falten

Escribe recursos/primaria/1/lengua/conciencia-fonologica/<archivo>-interactiva.html (misma dirección que la antigua).

Un juego por cada página del papel, en el mismo orden. Todo se resuelve ESCUCHANDO y tocando dibujos
(los niños de estas fichas aún no leen). Reutiliza el aspecto y la infraestructura de las interactivas de
letras (Leoni, sonidos, felicitaciones, voz de Sara con su script; si falta un audio, voz del dispositivo).
Las felicitaciones, el saludo y el final usan los audios comunes que ya existen en letras/audio/comun/.
"""
import json, os, re, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', 'fichas-letras'))
import generar_interactiva_letra as GL          # noqa: E402  (solo definiciones; no genera nada al importarse)
from generar_ficha_conciencia import palabras, silabas, comprobar, SALIDA, REL, E   # noqa: E402

COLOR = '#0f766e'
CONSIGNA = {
    'contar': 'Escucha la frase y toca cuántas palabras tiene.',
    'largas': 'Escucha las dos palabras y toca el dibujo de la palabra más larga.',
    'escondidas': 'Escucha la palabra. Dentro se esconde otra: toca su dibujo.',
    'frases': 'Escucha las dos frases y toca la más larga.',
}
FINAL, SALUDO, ELOGIOS = GL.FINAL, GL.SALUDO, GL.ELOGIOS
COMUN = os.path.join(SALIDA, '..', 'letras', 'audio', 'comun')


def textos_voz(d):
    t = []
    for pg in d['paginas']:
        tp = pg['tipo']; t.append(CONSIGNA[tp])
        if tp == 'contar': t += [f for _, f in pg['filas']]
        if tp == 'largas': t += [f'{a[1]}... o... {b[1]}' for a, b in pg['filas']] + [x[1] for a, b in pg['filas'] for x in (a, b)]
        if tp == 'escondidas': t += [f['palabra'] for f in pg['filas']] + [f['escondida'] for f in pg['filas']]
        if tp == 'frases': t += [f'{a} ... {b}' for a, b in pg['filas']] + [x for a, b in pg['filas'] for x in (a, b)]
    return list(dict.fromkeys(x.strip() for x in t))


def audios(d, generar_faltan):
    A = d['archivo']; carpeta = os.path.join(SALIDA, 'audio', A); mapa = {}
    for texto in [FINAL, SALUDO] + ELOGIOS:
        f = os.path.join(COMUN, GL.nombre_audio(texto))
        if os.path.exists(f): mapa[texto] = f'../letras/audio/comun/{GL.nombre_audio(texto)}'
    for texto in textos_voz(d):
        f = os.path.join(carpeta, GL.nombre_audio(texto))
        if not os.path.exists(f) and generar_faltan:
            os.makedirs(carpeta, exist_ok=True)
            with tempfile.TemporaryDirectory() as tmp:
                wav = os.path.join(tmp, 'v.wav')
                r = subprocess.run(['python3', GL.GENERAR_VOZ, 'sara', texto, wav, '--pad', '0.1', '--seed', str(GL.SEMILLA)], capture_output=True, text=True)
                if r.returncode != 0 or not os.path.exists(wav):
                    print(f'   ✗ voz «{texto}»: {(r.stdout + r.stderr).strip()[-200:]}'); continue
                subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '64000', wav, f], check=True)
            print(f'   🔊 {texto}')
        if os.path.exists(f): mapa[texto] = f'audio/{A}/{GL.nombre_audio(texto)}'
    return mapa


def generar(nombre, voz=False):
    d = json.load(open(os.path.join(AQUI, 'fichas', f'{nombre}.json'), encoding='utf8'))
    fallos = comprobar(d)
    if fallos:
        print(f'✗ {nombre}: no se genera'); [print('   -', x) for x in fallos]; return False
    A = d['archivo']
    pasos = []
    for pg in d['paginas']:
        p = {'tipo': pg['tipo'], 'titulo': pg['rotulo'], 'consigna': CONSIGNA[pg['tipo']]}
        if pg['tipo'] == 'contar':
            p['max'] = pg['max']; p['filas'] = [{'e': e, 'f': f, 'n': len(palabras(f))} for e, f in pg['filas']]
        elif pg['tipo'] == 'largas':
            p['filas'] = [{'a': a, 'b': b, 'larga': 0 if silabas(a[1]) > silabas(b[1]) else 1, 'voz': f'{a[1]}... o... {b[1]}'} for a, b in pg['filas']]
        elif pg['tipo'] == 'escondidas':
            p['filas'] = pg['filas']
        elif pg['tipo'] == 'frases':
            p['filas'] = [{'a': a, 'b': b, 'larga': 0 if len(palabras(a)) > len(palabras(b)) else 1, 'voz': f'{a} ... {b}',
                           'na': len(palabras(a)), 'nb': len(palabras(b))} for a, b in pg['filas']]
        pasos.append(p)
    titulo = d['titulo_corto'].split(' · ')[-1]
    datos = {'letra': '', 'silabas': [], 'archivo': A, 'pdf': f'{A}-1-primaria.pdf', 'pasos': pasos,
             'audio': audios(d, voz), 'final': FINAL, 'saludo': SALUDO, 'elogios': ELOGIOS, 'titulo': titulo,
             'num': d['titulo'].split(' · ')[0]}
    url = f'https://academiaesparta.es/recursos/primaria/1/lengua/conciencia-fonologica/{A}-interactiva.html'
    desc = (f'{d["titulo"].split(" · ")[0]} de conciencia fonológica interactiva para 1º de Primaria: {titulo.lower()}. '
            'Se juega escuchando y tocando, sin necesidad de saber leer · Gratis · Academia Esparta.')
    cab, js = GL.PLANTILLA.split('/* ── pasos ── */')[0], JS
    doc = cab + js
    for k, v in {'%%TITULO%%': E(f'{titulo} · Conciencia fonológica · Interactiva · 1º Primaria'), '%%DESC%%': E(desc),
                 '%%URL%%': url, '%%COLOR%%': COLOR, '%%REL%%': REL,
                 '%%DATOS%%': json.dumps(datos, ensure_ascii=False).replace('</', '<\\/')}.items():
        doc = doc.replace(k, v)
    doc = doc.replace('</style>', CSS + '</style>', 1)
    open(os.path.join(SALIDA, f'{A}-interactiva.html'), 'w', encoding='utf8').write(doc)
    tv = textos_voz(d)
    print(f'✓ {A}-interactiva.html ({sum(1 for t in tv if t in datos["audio"])} de {len(tv)} audios propios de Sara)')
    return True


CSS = r'''
    .nav-paso { display:flex; justify-content:space-between; align-items:center; margin-top:20px; padding-top:12px; border-top:2px dashed color-mix(in srgb, var(--c) 18%, #fff); }
    .nav-b { font:600 .9rem 'Poppins'; color:#64748b; background:none; border:none; cursor:pointer; padding:.35rem .6rem; border-radius:10px; }
    .nav-b:hover { color:var(--c); background:color-mix(in srgb, var(--c) 8%, #fff); }
    .dibujo-g { font-size:5rem; line-height:1.1; display:inline-block; animation:bota 2s ease-in-out infinite; }
    .adulto-t { font-family:'Playwrite ES',cursive; font-size:1.25rem; color:#64748b; margin:6px 0 16px; }
    .num-op { display:flex; gap:12px; justify-content:center; flex-wrap:wrap; }
    .num-op .op { font-family:'Poppins'; font-weight:800; display:flex; flex-direction:column; align-items:center; gap:6px; min-width:96px; padding:10px 14px; }
    .num-op .op i { display:flex; gap:4px; } .num-op .op i b { width:13px; height:13px; border-radius:50%; background:var(--c); }
    .num-op .op.bien i b { background:#fff; }
    .pareja { display:flex; gap:16px; justify-content:center; align-items:stretch; flex-wrap:wrap; }
    .carta { position:relative; background:#fff; border:4px solid color-mix(in srgb, var(--c) 22%, #fff); border-radius:24px; padding:14px 22px 10px;
             min-width:170px; cursor:pointer; text-align:center; box-shadow:0 6px 0 color-mix(in srgb, var(--c) 22%, #fff); transition:transform .15s; }
    .carta:hover { transform:translateY(-3px); border-color:var(--c); }
    .carta .e { font-size:4.4rem; line-height:1.15; display:block; }
    .carta .w { font-family:'Playwrite ES',cursive; font-size:1.2rem; color:#64748b; }
    .carta .oir { position:absolute; top:6px; right:6px; border:none; background:color-mix(in srgb, var(--c) 14%, #fff); border-radius:50%; width:34px; height:34px; cursor:pointer; font-size:1rem; }
    .carta.bien { background:#ecfdf5; border-color:var(--ok); box-shadow:0 6px 0 #166534; animation:pop .35s; }
    .carta.mal { animation:tiembla .4s; border-color:var(--mal); }
    .carta.fr { min-width:280px; max-width:340px; padding:18px 22px; }
    .carta.fr .w { font-size:1.4rem; color:#334155; }
    .o { align-self:center; font:700 1rem 'Poppins'; color:#94a3b8; }
    .esc-op .op { font-family:'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif; font-size:3.2rem; padding:10px 18px; }
    .bolitas { display:flex; gap:6px; justify-content:center; margin-top:8px; } .bolitas b { width:16px; height:16px; border-radius:50%; background:var(--ok); animation:pop .35s backwards; }
'''

JS = r'''/* ── voz en cola: cada frase espera a que termine la anterior (audio de Sara o voz del dispositivo) ── */
let colaVoz = [], turno = 0;
function pararVoz() { turno++; colaVoz = []; if (sonando) { sonando.onended = null; sonando.pause(); sonando = null; } if (window.speechSynthesis) speechSynthesis.cancel(); habla(false); }
function di(texto, enCola) { if (!sonido || !texto) return; texto = texto.trim();
  const libre = !sonando && !(window.speechSynthesis && speechSynthesis.speaking);
  if (!enCola) pararVoz(); colaVoz.push(texto); if (!enCola || libre) sigVoz(); }
function sigVoz() { if (sonando || (window.speechSynthesis && speechSynthesis.speaking)) return;
  const t = colaVoz.shift(); if (t == null) return; const mio = ++turno;
  const fin = () => { if (mio !== turno) return; sonando = null; habla(false); setTimeout(() => { if (mio === turno) sigVoz(); }, 300); };
  if (D.audio[t]) { const a = new Audio(D.audio[t]); sonando = a; a.onplaying = () => habla(true); a.onended = fin; a.onerror = fin; a.play().catch(fin); }
  else if (vozEs) { const u = new SpeechSynthesisUtterance(t); u.voice = vozEs; u.lang = vozEs.lang; u.rate = .85; u.onstart = () => habla(true); u.onend = u.onerror = fin; speechSynthesis.speak(u); }
  else fin(); }

/* ── pasos (conciencia fonológica) ── */
const P = D.pasos;
const app = $('#app'), prog = $('#progreso');
P.forEach(() => prog.appendChild(el('i')));
let actual = -1;
function pintaProgreso() { [...prog.children].forEach((x, i) => { x.className = i < actual ? 'hecho' : i === actual ? 'ahora' : ''; }); }
function tarjeta(n) {
  const t = el('section', 'paso'), c = el('div', 'tarjeta');
  c.innerHTML = `<div class="titulo"><b>${n + 1}</b><h2>${esc(P[n].titulo)}</h2></div><p class="consigna">${esc(P[n].consigna)} <button class="voz rep" type="button">🔊 Repetir</button></p>`;
  c.querySelector('.rep').onclick = () => di(P[n].consigna);
  const cuerpo = el('div'); c.appendChild(cuerpo);
  const sig = el('button', 'siguiente', n === P.length - 1 ? '¡Terminar! 🏆' : '¡Siguiente! ➜'); sig.type = 'button'; c.appendChild(sig);
  sig.onclick = () => ir(n + 1);
  const nav = el('div', 'nav-paso', (n > 0 ? '<button class="nav-b atras" type="button">← Atrás</button>' : '<span></span>') + '<button class="nav-b saltar" type="button">' + (n === P.length - 1 ? 'Saltar al final →' : 'Saltar →') + '</button>'); c.appendChild(nav);
  if (n > 0) nav.querySelector('.atras').onclick = () => ir(n - 1);
  nav.querySelector('.saltar').onclick = () => ir(n + 1);
  t.appendChild(c); app.appendChild(t);
  return { t, cuerpo, listo: () => { felicita(); setTimeout(() => { sig.classList.add('ver'); sig.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 1600); } };
}
let ultimoElogio = -1;
function felicita() {
  let i; do { i = Math.floor(Math.random() * D.elogios.length); } while (i === ultimoElogio && D.elogios.length > 1); ultimoElogio = i;
  const txt = D.elogios[i]; tono([[660, 0, .12], [880, .12, .12], [1175, .24, .3]]); confeti(40); di(txt, true); caraTemporal('celebrando', 1700, 'salta');
  const c = $('#cartel'); c.innerHTML = `<span class="estrella">⭐</span>${esc(txt)}`; c.classList.add('ver');
  clearTimeout(felicita.t); felicita.t = setTimeout(() => c.classList.remove('ver'), 1800);
}
mascota.style.display = 'none';
const pasos = [], CONSTRUYE = [];
function ir(n, cola) {
  document.querySelectorAll('.paso').forEach(p => p.classList.remove('activo'));
  actual = n; pintaProgreso();
  if (n >= P.length) { mascota.style.display = 'none'; $('#final').classList.add('activo'); fanfarria(); confeti(); setTimeout(() => di(D.final), 700); }
  else { if (pasos[n]) pasos[n].t.remove(); pasos[n] = CONSTRUYE[n](); pasos[n].t.classList.add('activo'); (matchMedia('(max-width:1200px)').matches ? pasos[n].t.querySelector('.tarjeta') : document.body).appendChild(mascota);
         mascota.style.display = ''; di(P[n].consigna, cola); if (pasos[n].alEntrar) pasos[n].alEntrar(); }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
const sacude = b => { b.classList.remove('mal'); void b.offsetWidth; b.classList.add('mal'); mal(); };
function rondas(p, filas, pintar) {
  let k = 0; const orden = mezcla(filas); const caja = el('div', 'reto'); p.cuerpo.appendChild(caja);
  const sigue = () => setTimeout(() => { k++; k < orden.length ? uno() : (caja.innerHTML = '<div class="dibujo-g">🎉</div><p class="palabra">¡Todas!</p>', p.listo()); }, 1500);
  const uno = () => { const v = pintar(caja, orden[k], `<p class="cuenta-reto">${k + 1} de ${orden.length}</p>`, sigue); if (k > 0) di(v, true); return v; };
  const primera = uno(); p.alEntrar = () => di(primera, true);
}

/* portada */
const portada = el('section', 'paso activo');
portada.innerHTML = `<div class="tarjeta portada"><div class="portada-leo"><img src="${REL}mascota/leoni/frente.webp" alt="Leoni, la mascota de Academia Esparta"><span class="bocadillo">¡Hola! Soy Leoni</span></div>
  <div class="letrota" style="font-size:min(24vw,6rem)">👂</div><h1>${esc(D.titulo)}</h1><p>${P.length} juegos cortos. Escucha bien y toca. ¡No hace falta saber leer!</p>
  <button class="grande" type="button">¡Empezar! 🚀</button></div>`;
portada.querySelector('.grande').onclick = () => { di(D.saludo); ir(0, true); };
app.appendChild(portada);

P.forEach((pg, n) => { CONSTRUYE[n] = () => { const p = tarjeta(n);
  if (pg.tipo === 'contar') rondas(p, pg.filas, (caja, r, pie, sigue) => {
    caja.innerHTML = `<div class="dibujo-g">${emo(r.e)}</div><div class="adulto-t">${esc(r.f)} <button class="voz auto" type="button">🔊</button></div><div class="num-op"></div>${pie}`;
    caja.querySelector('.auto').onclick = () => di(r.f);
    const ops = caja.querySelector('.num-op');
    for (let v = 1; v <= pg.max; v++) { const b = el('button', 'op', `${v}<i>${'<b></b>'.repeat(v)}</i>`); b.type = 'button';
      b.onclick = () => { if (v === r.n) { b.classList.add('bien'); bien(); ops.querySelectorAll('.op').forEach(x => x.disabled = true); di(r.f); sigue(); } else sacude(b); };
      ops.appendChild(b); } return r.f; });
  if (pg.tipo === 'largas') rondas(p, pg.filas, (caja, r, pie, sigue) => {
    const carta = (x, i) => `<div class="carta" data-i="${i}"><button class="oir" type="button" data-w="${esc(x[1])}">🔊</button><span class="e">${emo(x[0])}</span><span class="w">${esc(x[1])}</span></div>`;
    caja.innerHTML = `<div class="pareja">${carta(r.a, 0)}<span class="o">o</span>${carta(r.b, 1)}</div><p><button class="voz auto" type="button">🔊 Escuchar las dos</button></p>${pie}`;
    caja.querySelector('.auto').onclick = () => di(r.voz);
    caja.querySelectorAll('.oir').forEach(b => b.onclick = ev => { ev.stopPropagation(); di(b.dataset.w); });
    let hecho = false;
    caja.querySelectorAll('.carta').forEach(c => c.onclick = () => { if (hecho) return;
      if (+c.dataset.i === r.larga) { hecho = true; c.classList.add('bien'); bien(); di(c.querySelector('.oir').dataset.w); sigue(); } else sacude(c); }); return r.voz; });
  if (pg.tipo === 'escondidas') rondas(p, pg.filas, (caja, r, pie, sigue) => {
    caja.innerHTML = `<div class="dibujo-g">${emo(r.emoji)}</div><div class="adulto-t">${esc(r.palabra)} <button class="voz auto" type="button">🔊</button></div><div class="opciones esc-op"></div>${pie}`;
    caja.querySelector('.auto').onclick = () => di(r.palabra);
    const ops = caja.querySelector('.opciones');
    mezcla(r.opciones.map((o, i) => [o, i])).forEach(([o, i]) => { const b = el('button', 'op', emo(o)); b.type = 'button';
      b.onclick = () => { if (i === r.buena) { b.classList.add('bien'); bien(); ops.querySelectorAll('.op').forEach(x => x.disabled = true); di(r.escondida); sigue(); } else sacude(b); };
      ops.appendChild(b); }); return r.palabra; });
  if (pg.tipo === 'frases') rondas(p, pg.filas, (caja, r, pie, sigue) => {
    const carta = (f, i) => `<div class="carta fr" data-i="${i}"><button class="oir" type="button" data-w="${esc(f)}">🔊</button><span class="w">${esc(f)}</span><div class="bolitas"></div></div>`;
    caja.innerHTML = `<div class="pareja">${carta(r.a, 0)}<span class="o">o</span>${carta(r.b, 1)}</div><p><button class="voz auto" type="button">🔊 Escuchar las dos</button></p>${pie}`;
    caja.querySelector('.auto').onclick = () => di(r.voz);
    caja.querySelectorAll('.oir').forEach(b => b.onclick = ev => { ev.stopPropagation(); di(b.dataset.w); });
    let hecho = false;
    caja.querySelectorAll('.carta').forEach(c => c.onclick = () => { if (hecho) return;
      if (+c.dataset.i === r.larga) { hecho = true; c.classList.add('bien'); bien();
        caja.querySelectorAll('.carta').forEach(x => { const nn = +x.dataset.i ? r.nb : r.na; x.querySelector('.bolitas').innerHTML = Array.from({ length: nn }, (_, j) => `<b style="animation-delay:${j * .12}s"></b>`).join(''); });
        di(c.querySelector('.oir').dataset.w); sigue(); } else sacude(c); }); return r.voz; });
  return p; }; });

/* final */
const fin = el('section', 'paso'); fin.id = 'final';
fin.innerHTML = `<div class="tarjeta final"><img class="leo-fin" src="${REL}mascota/leoni/celebrando.webp" alt=""><h2>¡Lo has conseguido!</h2><p>Has escuchado muy bien. ¡Eres un campeón!</p>
  <div class="estrellas"><span>⭐</span><span style="animation-delay:.2s">⭐</span><span style="animation-delay:.4s">⭐</span></div>
  <div class="acciones"><a class="lleno" href="${D.pdf}" target="_blank" rel="noopener">📄 Ficha para imprimir</a><button type="button" id="otra-vez">↺ Jugar otra vez</button><a href="${REL}materiales.html">Más fichas</a></div></div>`;
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
    sys.exit(0 if all([generar(x, voz) for x in args]) else 1)
