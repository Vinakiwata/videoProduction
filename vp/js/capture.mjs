// Chụp khung trang trình chiếu bằng Chrome headless qua CDP (Node ≥ 22, không cần thư viện ngoài).
// Dùng: node capture.mjs <spec.json>
// spec: {url, out_dir, frames:[...], width, height, chrome?, port?, measure?: bool, prefix?: "f"}
// In ra stdout một JSON: {frames:[{frame, shot, file, issues}], errors:[...], console:[...]}
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const spec = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const W = spec.width || 1920, H = spec.height || 1080, port = spec.port || 9333 + Math.floor(Math.random() * 500);
const profile = mkdtempSync(join(tmpdir(), 'vp-chrome-'));
const chrome = spawn(spec.chrome || 'google-chrome', ['--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
  '--allow-file-access-from-files', '--mute-audio', '--disable-background-networking', '--disable-component-update', '--no-first-run', '--disable-sync', '--force-color-profile=srgb', '--font-render-hinting=none',
  `--user-data-dir=${profile}`, `--remote-debugging-port=${port}`, `--window-size=${W},${H}`, 'about:blank'],
  { stdio: 'ignore' });
const done = code => { try { chrome.kill('SIGKILL'); } catch {} try { rmSync(profile, { recursive: true, force: true }); } catch {} process.exit(code); };
const sleep = ms => new Promise(r => setTimeout(r, ms));

let list = null;
for (let i = 0; i < 60 && !list; i++) {
  await sleep(150);
  try { list = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); } catch {}
}
if (!list) { console.error('không mở được Chrome'); done(2); }
const ws = new WebSocket(list.find(t => t.type === 'page').webSocketDebuggerUrl);
let id = 0; const pend = {}; const consoleMsgs = [];
ws.onmessage = e => {
  const m = JSON.parse(e.data);
  if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; }
  else if (m.method === 'Runtime.exceptionThrown') consoleMsgs.push('exception: ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
  else if (m.method === 'Runtime.consoleAPICalled' && ['error', 'warning'].includes(m.params.type))
    consoleMsgs.push(m.params.type + ': ' + m.params.args.map(a => a.value ?? a.description).join(' '));
  else if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') consoleMsgs.push('log: ' + m.params.entry.text + ' ' + (m.params.entry.url || ''));
};
await new Promise(r => ws.onopen = r);
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async expr => {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.result.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description || r.result.exceptionDetails.text);
  return r.result.result.value;
};

try {
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 1, mobile: false });
  await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable');
  await send('Page.navigate', { url: spec.url });
  let ok = false;
  for (let i = 0; i < 100 && !ok; i++) { await sleep(100); try { ok = await evaluate('!!(window.vp && window.vp.ready)'); } catch {} }
  if (!ok) throw new Error('trang không tạo window.vp');
  await evaluate('vp.ready.then(() => true)');
  mkdirSync(spec.out_dir, { recursive: true });
  const out = [];
  for (const f of spec.frames) {
    const r = await evaluate(`vp.seek(${f}).then(r => ({...r, issues: ${spec.measure ? 'vp.measure()' : '[]'}}))`);
    const shot = await send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: W, height: H, scale: 1 } });
    const file = join(spec.out_dir, `${spec.prefix || 'f'}${String(f).padStart(5, '0')}.png`);
    writeFileSync(file, Buffer.from(shot.result.data, 'base64'));
    out.push({ frame: r.frame, shot: r.shot, file, issues: r.issues });
  }
  const errors = await evaluate('vp.errors.slice()');
  const fonts = await evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/[\"']/g, '') + ' ' + f.weight)");
  process.stdout.write(JSON.stringify({ frames: out, errors, console: consoleMsgs, fonts }));
  ws.close(); done(0);
} catch (err) {
  console.error(String(err && err.stack || err)); if (consoleMsgs.length) console.error(consoleMsgs.join('\n'));
  done(1);
}
