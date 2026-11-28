// Mở Chrome headless và một trang qua giao thức DevTools (Node ≥ 22, không cần thư viện ngoài).
// Dùng chung cho capture.mjs (Tool 07) và render.mjs (Tool 08).
import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

export const sleep = ms => new Promise(r => setTimeout(r, ms));

export async function openPage({ url, width = 1920, height = 1080, chrome = 'google-chrome', port }) {
  port = port || 9333 + Math.floor(Math.random() * 500);
  const profile = mkdtempSync(join(tmpdir(), 'vp-chrome-'));
  const proc = spawn(chrome, ['--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
    '--allow-file-access-from-files', '--mute-audio', '--disable-background-networking', '--disable-component-update', '--no-first-run',
    '--disable-sync', '--force-color-profile=srgb', '--font-render-hinting=none',
    `--user-data-dir=${profile}`, `--remote-debugging-port=${port}`, `--window-size=${width},${height}`, 'about:blank'], { stdio: 'ignore' });
  const close = () => { try { proc.kill('SIGKILL'); } catch {} try { rmSync(profile, { recursive: true, force: true }); } catch {} };
  let list = null;
  for (let i = 0; i < 60 && !list; i++) { await sleep(150); try { list = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); } catch {} }
  if (!list) { close(); throw new Error('không mở được Chrome'); }
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
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false });
  await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable');
  await send('Page.navigate', { url });
  let ok = false;
  for (let i = 0; i < 100 && !ok; i++) { await sleep(100); try { ok = await evaluate('!!(window.vp && window.vp.ready)'); } catch {} }
  if (!ok) { close(); throw new Error('trang không tạo window.vp' + (consoleMsgs.length ? '\n' + consoleMsgs.join('\n') : '')); }
  await evaluate('vp.ready.then(() => true)');
  const shot = async () => Buffer.from((await send('Page.captureScreenshot',
    { format: 'png', clip: { x: 0, y: 0, width, height, scale: 1 } })).result.data, 'base64');
  return { send, evaluate, shot, consoleMsgs, close: () => { try { ws.close(); } catch {} close(); } };
}
