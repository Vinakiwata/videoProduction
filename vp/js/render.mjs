// Tool 08: tua trang trình chiếu tuần tự 0…total−1, chụp từng khung PNG và ghi liên tiếp ra stdout (image2pipe cho ffmpeg).
// Dùng: node render.mjs <spec.json>   spec: {url, width, height, total, chrome?}
// Trang có lỗi JS (vp.errors) → in lỗi ra stderr, thoát mã 3; không ghi thêm khung nào.
import { readFileSync } from 'node:fs';
import { openPage } from './cdp.mjs';

const spec = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const write = buf => new Promise(r => process.stdout.write(buf) ? r() : process.stdout.once('drain', r));
let page, code = 0;
try {
  page = await openPage(spec);
  for (let f = 0; f < spec.total; f++) {
    const n = await page.evaluate(`vp.seek(${f}).then(() => vp.errors.length)`);
    if (n || page.consoleMsgs.some(m => m.startsWith('exception'))) {
      const errs = await page.evaluate('vp.errors.slice()');
      console.error(`lỗi trang ở khung ${f}: ` + [...errs, ...page.consoleMsgs].join(' | '));
      code = 3; break;
    }
    await write(await page.shot());
    if (f % 150 === 0) process.stderr.write(`khung ${f}/${spec.total}\n`);
  }
} catch (err) {
  console.error(String(err && err.stack || err)); code = 1;
}
if (page) page.close();
process.stdout.end?.();
process.exitCode = code;
setTimeout(() => process.exit(code), 50);
