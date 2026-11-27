import { spawn } from 'child_process'; import fs from 'fs'; import path from 'path';
const root = process.argv[2]; const files = fs.readFileSync(process.argv[3],'utf8').trim().split('\n');
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', ['--headless=new','--remote-debugging-port=9333','--user-data-dir=/tmp/negritas/prof','--no-first-run','about:blank'], {stdio:'ignore'});
await new Promise(r=>setTimeout(r,2500));
const list = await (await fetch('http://127.0.0.1:9333/json')).json();
const ws = new WebSocket(list.find(t=>t.type==='page').webSocketDebuggerUrl);
await new Promise(r=>ws.onopen=r);
let id=0; const pend={}; const waiters=[];
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; } if (m.method==='Page.loadEventFired') waiters.splice(0).forEach(f=>f()); };
const send=(method,params={})=>new Promise(r=>{const i=++id; pend[i]=r; ws.send(JSON.stringify({id:i,method,params}));});
await send('Page.enable');
const fn = fs.readFileSync('/tmp/negritas/eval.js','utf8');
const out=[];
for (const f of files) {
  const loaded = new Promise(r=>waiters.push(r));
  await send('Page.navigate',{url:'file://'+path.resolve(root,f)}); await loaded;
  await send('Runtime.evaluate',{expression:'document.fonts.ready',awaitPromise:true});
  const r = await send('Runtime.evaluate',{expression:fn,returnByValue:true});
  out.push({f, ...r.result.result.value});
}
fs.writeFileSync('/tmp/negritas/res.json', JSON.stringify(out,null,0));
ws.close(); chrome.kill(); process.exit(0);
