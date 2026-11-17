// Renderuje scena.html klatka po klatce do MP4 (kilka przeglądarek równolegle)
// node render.js <katalog> <h|v>
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path'), fs = require('fs');
const FPS = 30, WORKERS = +(process.env.WORKERS || 4);
const outDir = process.argv[2] || path.join(__dirname, 'build');
const lay = process.argv[3] || 'h', V = lay === 'v';
const VIEW = V ? { width: 1080, height: 1920 } : { width: 1920, height: 1080 };
const URL = 'file://' + path.resolve(__dirname, 'scena.html') + '#static' + lay;
fs.mkdirSync(outDir, { recursive: true });

async function worker(id, from, to) {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: VIEW });
  p.on('pageerror', e => console.error('ERR', e.message));
  await p.goto(URL);
  await p.evaluate(() => document.fonts.ready);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', path.join(outDir, `${lay}_seg${id}.mp4`)], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = from; f < to; f++) {
    await p.evaluate(t => render(t), f / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 94 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((f - from) % 300 === 0) console.log(`${lay} worker ${id}: ${f - from}/${to - from}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
}
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto(URL); const dur = await p.evaluate(() => DURATION); await b.close();
  const total = Math.round(dur * FPS), per = Math.ceil(total / WORKERS);
  await Promise.all([...Array(WORKERS).keys()].map(i => worker(i, i * per, Math.min(total, (i + 1) * per))));
  fs.writeFileSync(path.join(outDir, `${lay}_list.txt`), [...Array(WORKERS).keys()].map(i => `file '${lay}_seg${i}.mp4'`).join('\n'));
  console.log('done', lay, total, 'frames');
})();
