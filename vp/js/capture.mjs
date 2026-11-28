// Chụp khung trang trình chiếu bằng Chrome headless qua CDP (Node ≥ 22, không cần thư viện ngoài).
// Dùng: node capture.mjs <spec.json>
// spec: {url, out_dir, frames:[...], width, height, chrome?, port?, measure?: bool, prefix?: "f"}
// In ra stdout một JSON: {frames:[{frame, shot, file, issues}], errors:[...], console:[...], fonts:[...]}
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { openPage } from './cdp.mjs';

const spec = JSON.parse(readFileSync(process.argv[2], 'utf8'));
let page;
try {
  page = await openPage(spec);
  mkdirSync(spec.out_dir, { recursive: true });
  const out = [];
  for (const f of spec.frames) {
    const r = await page.evaluate(`vp.seek(${f}).then(r => ({...r, issues: ${spec.measure ? 'vp.measure()' : '[]'}}))`);
    const file = join(spec.out_dir, `${spec.prefix || 'f'}${String(f).padStart(5, '0')}.png`);
    writeFileSync(file, await page.shot());
    out.push({ frame: r.frame, shot: r.shot, file, issues: r.issues });
  }
  const errors = await page.evaluate('vp.errors.slice()');
  const fonts = await page.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/[\"']/g, '') + ' ' + f.weight)");
  process.stdout.write(JSON.stringify({ frames: out, errors, console: page.consoleMsgs, fonts }));
  page.close(); process.exit(0);
} catch (err) {
  console.error(String(err && err.stack || err)); if (page && page.consoleMsgs.length) console.error(page.consoleMsgs.join('\n'));
  if (page) page.close(); process.exit(1);
}
