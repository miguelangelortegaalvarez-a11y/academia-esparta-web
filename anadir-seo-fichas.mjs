// Añade <meta name="description"> + <link rel="canonical"> a todas las páginas
// de recursos/ que no los tengan. Idempotente (las que ya tienen description se
// saltan). Las fichas registradas en RECURSOS de materiales.html reciben una
// descripción rica (título + sub-bloque + curso); el resto, una derivada de su
// <title>. Ejecutar tras crear fichas nuevas:  node anadir-seo-fichas.mjs
import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { dirname, join, relative } from 'path';
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

const RECURSOS = extraerObjeto('RECURSOS');
const NOMBRE_ASIG = { lengua: 'Lengua', matematicas: 'Matemáticas' };

// ── Mapa ruta-de-fichero → descripción rica desde RECURSOS ──
const descPorRuta = new Map();
for (const [key, rec] of Object.entries(RECURSOS)) {
  const [asig, curso, , subBloque] = key.split('|');
  const asigNombre = NOMBRE_ASIG[asig] || asig;
  for (const f of rec.fichas) {
    const marco = `${subBloque} · ${asigNombre} ${curso}º Primaria`;
    descPorRuta.set(rec.ruta + f.archivo,
      `${f.titulo} — ficha ${f.num} de ${marco}. Gratis y lista para imprimir en A4 · Academia Esparta.`);
    if (f.interactiva) {
      descPorRuta.set(rec.ruta + f.interactiva,
        `${f.titulo} — ejercicio interactivo de ${marco}. Juega online gratis · Academia Esparta.`);
    }
  }
}

// ── Recorrer recursos/ ──
function* htmlsDe(dir) {
  for (const nombre of readdirSync(dir)) {
    const ruta = join(dir, nombre);
    if (statSync(ruta).isDirectory()) yield* htmlsDe(ruta);
    else if (nombre.endsWith('.html')) yield ruta;
  }
}

const esc = s => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const recorta = (s, max = 158) => (s.length <= max ? s : s.slice(0, max - 1).replace(/\s+\S*$/, '') + '…');

let anadidas = 0, saltadas = 0, ricas = 0, derivadas = 0;
const sinTitle = [];

for (const abs of htmlsDe(join(RAIZ, 'recursos'))) {
  const rel = relative(RAIZ, abs).split('\\').join('/');
  let contenido = readFileSync(abs, 'utf8');
  if (contenido.includes('name="description"')) { saltadas++; continue; }

  const mTitle = contenido.match(/<title>([^<]*)<\/title>/);
  if (!mTitle) { sinTitle.push(rel); continue; }

  let desc;
  if (descPorRuta.has(rel)) { desc = descPorRuta.get(rel); ricas++; }
  else { desc = `${mTitle[1].trim()} · Material educativo gratuito de Academia Esparta (Torremolinos).`; derivadas++; }

  const canonical = `${DOMINIO}/${rel}`;
  const inyeccion = `</title>\n  <meta name="description" content="${esc(recorta(desc))}">\n  <link rel="canonical" href="${canonical}">`;
  contenido = contenido.replace('</title>', inyeccion);
  writeFileSync(abs, contenido);
  anadidas++;
}

console.log(`✅ ${anadidas} páginas actualizadas (${ricas} con descripción rica de RECURSOS, ${derivadas} derivadas del <title>)`);
console.log(`↷ ${saltadas} ya tenían description (saltadas)`);
if (sinTitle.length) {
  console.log(`⚠️ Sin <title> — NO tocadas (${sinTitle.length}):`);
  sinTitle.forEach(r => console.log('  ', r));
}
