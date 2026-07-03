// Genera los índices estáticos de fichas por curso+asignatura a partir de los
// datos de materiales.html (ASIGNATURAS + RECURSOS). Ejecutar tras registrar
// un sub-bloque nuevo en RECURSOS:  node generar-indices-recursos.mjs
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const RAIZ = dirname(fileURLToPath(import.meta.url));
const DOMINIO = 'https://academiaesparta.es';
const html = readFileSync(join(RAIZ, 'materiales.html'), 'utf8');

function extraerObjeto(nombre) {
  const inicio = html.indexOf(`const ${nombre} = {`);
  if (inicio < 0) throw new Error(`${nombre} no encontrado en materiales.html`);
  const desde = html.indexOf('{', inicio);
  let depth = 0, fin = -1;
  for (let i = desde; i < html.length; i++) {
    if (html[i] === '{') depth++;
    else if (html[i] === '}') { depth--; if (depth === 0) { fin = i; break; } }
  }
  return eval('(' + html.slice(desde, fin + 1) + ')');
}

const ASIGNATURAS = extraerObjeto('ASIGNATURAS');
const RECURSOS = extraerObjeto('RECURSOS');

const NOMBRE_ASIG = { lengua: 'Lengua', matematicas: 'Matemáticas' };
const GUIAS_BLOG = {
  matematicas: [{ href: '/como-ayudar-matematicas-primaria.html', texto: 'Cómo ayudar a tu hijo con las matemáticas en Primaria' }],
  lengua: [
    { href: '/como-ayudar-comprension-lectora-primaria.html', texto: 'Cómo mejorar la comprensión lectora en Primaria' },
    { href: '/como-trabajar-ortografia-primaria.html', texto: 'Cómo trabajar la ortografía en Primaria' },
  ],
};

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// ── Qué páginas existen: (asig, curso) con al menos un sub-bloque en RECURSOS ──
const paginas = new Map();
for (const key of Object.keys(RECURSOS)) {
  const [asig, curso] = key.split('|');
  paginas.set(`${asig}|${curso}`, true);
}

const enlacesGenerados = [];
const avisos = [];

for (const pagKey of paginas.keys()) {
  const [asig, curso] = pagKey.split('|');
  const cur = ASIGNATURAS[asig].curriculum[curso];
  const asigNombre = NOMBRE_ASIG[asig];
  const cursoLargo = `${curso}º de Primaria`;
  const urlDir = `/recursos/primaria/${curso}/${asig}/`;
  const canonical = DOMINIO + urlDir;

  // Bloques con contenido real
  let totalFichas = 0, subConFichas = 0, subTotales = 0;
  const bloquesHtml = [];
  const nombresBloques = [];
  for (const [bloqueKey, bloque] of Object.entries(cur.bloques)) {
    subTotales += bloque.subBloques.length;
    const subs = [];
    for (const sb of bloque.subBloques) {
      const rec = RECURSOS[`${asig}|${curso}|${bloqueKey}|${sb}`];
      if (!rec) continue;
      subConFichas++;
      totalFichas += rec.fichas.length;
      const items = rec.fichas.map(f => {
        const href = '/' + rec.ruta + f.archivo;
        enlacesGenerados.push(href);
        let extra = '';
        if (f.interactiva) {
          const hrefInt = '/' + rec.ruta + f.interactiva;
          enlacesGenerados.push(hrefInt);
          extra = ` <a class="int" href="${hrefInt}">interactiva</a>`;
        }
        return `        <li><a href="${href}">Ficha ${f.num} · ${esc(f.titulo)}</a> <span class="nivel">${esc(f.nivel)}</span>${extra}</li>`;
      }).join('\n');
      subs.push(`      <h3>${esc(sb)} <span class="n">· ${rec.fichas.length} fichas</span></h3>\n      <ul class="fichas">\n${items}\n      </ul>`);
    }
    if (subs.length) {
      nombresBloques.push(bloque.nombre.toLowerCase());
      bloquesHtml.push(`    <section class="bloque">\n      <h2>${bloque.icono} ${esc(bloque.nombre)}</h2>\n${subs.join('\n')}\n    </section>`);
    }
  }

  // Enlaces a otros índices (mismo asig otros cursos + otra asignatura mismo curso)
  const otros = [];
  for (const c of Object.keys(ASIGNATURAS[asig].curriculum)) {
    if (c !== curso && paginas.has(`${asig}|${c}`)) {
      otros.push(`<a class="pill" href="/recursos/primaria/${c}/${asig}/">${asigNombre} ${c}º</a>`);
    }
  }
  for (const otraAsig of Object.keys(ASIGNATURAS)) {
    if (otraAsig !== asig && paginas.has(`${otraAsig}|${curso}`)) {
      otros.push(`<a class="pill" href="/recursos/primaria/${curso}/${otraAsig}/">${NOMBRE_ASIG[otraAsig]} ${curso}º</a>`);
    }
  }

  const guias = (GUIAS_BLOG[asig] || []).map(g => `<li><a href="${g.href}">${g.texto}</a></li>`).join('\n          ');
  const parcial = subConFichas < subTotales
    ? `\n    <p class="parcial">📌 Estamos completando este curso: publicamos fichas nuevas cada semana. Aquí tienes todo lo ya disponible.</p>` : '';

  const titulo = `Fichas de ${asigNombre} de ${cursoLargo} para imprimir (gratis) | Academia Esparta`;
  const descripcion = `${totalFichas} fichas de ${asigNombre} de ${cursoLargo} gratis y listas para imprimir en A4: ${nombresBloques.join(', ')}. Elaboradas por Academia Esparta (Torremolinos) según el currículo LOMLOE. Sin registro.`;

  const jsonld = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Inicio', item: DOMINIO + '/' },
          { '@type': 'ListItem', position: 2, name: 'Materiales', item: DOMINIO + '/materiales.html' },
          { '@type': 'ListItem', position: 3, name: `Fichas de ${asigNombre} ${cursoLargo}`, item: canonical },
        ],
      },
      {
        '@type': 'CollectionPage',
        name: titulo,
        description: descripcion,
        url: canonical,
        inLanguage: 'es',
        publisher: {
          '@type': 'EducationalOrganization',
          name: 'Academia Esparta',
          url: DOMINIO + '/',
        },
      },
    ],
  };

  const pagina = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${esc(titulo)}</title>
  <meta name="description" content="${esc(descripcion)}">
  <link rel="canonical" href="${canonical}">
  <meta property="og:title" content="${esc(titulo)}">
  <meta property="og:description" content="${esc(descripcion)}">
  <meta property="og:url" content="${canonical}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="${DOMINIO}/og-image.jpg">
  <link rel="icon" type="image/png" href="/favicon.PNG">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet">
  <script type="application/ld+json">${JSON.stringify(jsonld)}</script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Poppins', sans-serif; color: #22302a; background: #fff; line-height: 1.6; }
    a { color: #0e9343; }
    .site-header { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: .85rem 1.4rem; border-bottom: 1px solid #e6eee9; }
    .site-header .logo { font-weight: 800; color: #064e3b; text-decoration: none; font-size: 1rem; }
    .site-header nav { display: flex; gap: 1rem; font-size: .85rem; }
    main { max-width: 900px; margin: 0 auto; padding: 1.6rem 1.4rem 3rem; }
    .breadcrumb { font-size: .78rem; color: #6b7f75; margin-bottom: 1.1rem; }
    .breadcrumb a { color: #6b7f75; }
    h1 { font-size: 1.65rem; color: #064e3b; line-height: 1.25; }
    .lead { margin: .7rem 0 .4rem; color: #4b5f56; font-size: .95rem; max-width: 62ch; }
    .badges { margin: .8rem 0 .4rem; display: flex; flex-wrap: wrap; gap: .45rem; }
    .badge { background: #e7f6ec; color: #0b7a37; font-weight: 700; padding: .18rem .7rem; border-radius: 999px; font-size: .78rem; }
    .parcial { margin-top: .9rem; font-size: .85rem; color: #4b5f56; background: #fbf7ea; border: 1px solid #efe3bc; border-radius: 10px; padding: .6rem .9rem; }
    section.bloque { margin: 2rem 0 0; }
    h2 { font-size: 1.18rem; color: #064e3b; border-bottom: 2px solid #d9eadf; padding-bottom: .35rem; }
    h3 { font-size: .95rem; margin: 1.05rem 0 .4rem; color: #22302a; }
    h3 .n { color: #6b7f75; font-weight: 600; font-size: .78rem; }
    ul.fichas { list-style: none; display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: .3rem 1.1rem; }
    ul.fichas li { font-size: .86rem; }
    ul.fichas a { text-decoration: none; font-weight: 600; }
    ul.fichas a:hover { text-decoration: underline; }
    .nivel { color: #8aa094; font-size: .7rem; white-space: nowrap; }
    a.int { font-size: .74rem; font-weight: 600; background: #eef7f1; border-radius: 6px; padding: 0 .4rem; text-decoration: none; }
    .otros { margin-top: 2.2rem; }
    .otros h2 { border: none; padding: 0; margin-bottom: .6rem; }
    .pills { display: flex; flex-wrap: wrap; gap: .5rem; }
    .pill { border: 1.5px solid #bcdcc8; border-radius: 999px; padding: .3rem .9rem; font-size: .84rem; font-weight: 600; text-decoration: none; }
    .pill:hover { background: #e7f6ec; }
    .cta { background: #f2faf5; border: 1px solid #d7ecdf; border-radius: 14px; padding: 1.15rem 1.3rem; margin-top: 2.2rem; font-size: .9rem; }
    .cta h2 { border: none; padding: 0; font-size: 1.05rem; margin-bottom: .4rem; }
    .cta ul { margin: .5rem 0 0 1.2rem; }
    footer { border-top: 1px solid #e6eee9; padding: 1.3rem; text-align: center; color: #7d8f86; font-size: .78rem; }
    footer a { color: #7d8f86; }
  </style>
  <!-- Umami Analytics -->
  <script defer src="https://umami.academiaesparta.es/script.js" data-website-id="625f0531-51c5-4ff4-bee3-c06c04ac3905"></script>
</head>
<body>

  <header class="site-header">
    <a class="logo" href="/">Academia Esparta</a>
    <nav>
      <a href="/materiales.html">Todos los materiales</a>
      <a href="/blog.html">Guías para padres</a>
    </nav>
  </header>

  <main>
    <div class="breadcrumb"><a href="/">Inicio</a> › <a href="/materiales.html">Materiales</a> › Fichas de ${asigNombre} ${cursoLargo}</div>

    <h1>Fichas de ${asigNombre} de ${cursoLargo} para imprimir</h1>
    <p class="lead">${totalFichas} fichas gratuitas de ${asigNombre} de ${cursoLargo}, elaboradas por el equipo de Academia Esparta y organizadas por bloques del currículo LOMLOE. Listas para imprimir en A4 en blanco y negro. Sin registro y sin correo: abre la ficha e imprímela.</p>
    <div class="badges"><span class="badge">${totalFichas} fichas</span><span class="badge">Gratis</span><span class="badge">A4 · blanco y negro</span><span class="badge">LOMLOE</span></div>${parcial}

${bloquesHtml.join('\n')}

    <section class="otros">
      <h2>Más fichas gratuitas</h2>
      <div class="pills">
        ${otros.join('\n        ')}
        <a class="pill" href="/materiales.html">📚 Ver todo el catálogo</a>
      </div>
    </section>

    <section class="cta">
      <h2>¿Quién hace estas fichas?</h2>
      <p>Somos <a href="/">Academia Esparta</a>, una academia de refuerzo escolar en Torremolinos (Málaga). Estas fichas son las mismas que usamos cada tarde con nuestros alumnos, y las publicamos gratis para que cualquier familia pueda usarlas en casa. Si quieres sacarles más partido, te lo contamos en nuestras guías:</p>
      <ul>
          ${guias}
      </ul>
    </section>
  </main>

  <footer>
    © Academia Esparta · C/ Rafael Quintana Rosado 8, Torremolinos (Málaga) · <a href="/">academiaesparta.es</a> · <a href="/materiales.html">Materiales</a> · <a href="/blog.html">Blog</a>
  </footer>

</body>
</html>
`;

  const dirSalida = join(RAIZ, 'recursos', 'primaria', curso, asig);
  if (!existsSync(dirSalida)) { avisos.push(`⚠️ no existe el directorio ${dirSalida}`); continue; }
  writeFileSync(join(dirSalida, 'index.html'), pagina);
  console.log(`✅ ${urlDir}index.html — ${totalFichas} fichas, ${subConFichas}/${subTotales} sub-bloques`);
}

// ── Validación: cada enlace generado debe existir en disco ──
const rotos = enlacesGenerados.filter(href => !existsSync(join(RAIZ, href.slice(1))));
console.log(`\nEnlaces a fichas generados: ${enlacesGenerados.length}`);
if (rotos.length) {
  console.log(`❌ ROTOS (${rotos.length}):`);
  rotos.forEach(r => console.log('  ', r));
  process.exitCode = 1;
} else {
  console.log('✅ Todos los enlaces existen en disco.');
}
avisos.forEach(a => console.log(a));
