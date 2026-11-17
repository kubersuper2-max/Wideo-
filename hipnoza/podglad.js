// Zrzuty pojedynczych klatek: node podglad.js <katalog> <h|v> t1 t2 ...
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [out, lay, ...ts] = process.argv.slice(2);
  const V = lay === 'v';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: V ? { width: 1080, height: 1920 } : { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + path.resolve(__dirname, 'scena.html') + '#static' + (V ? 'v' : 'h'));
  await p.evaluate(() => document.fonts.ready);
  for (const t of ts.map(Number)) { await p.evaluate(t => render(t), t); await p.screenshot({ path: `${out}/${lay}_${t}.png` }); }
  await b.close();
})();
