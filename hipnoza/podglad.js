const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const out = process.argv[2]; const times = process.argv.slice(3).map(Number);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('console', m => console.log('console:', m.text())); p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + path.resolve(__dirname, 'scena.html') + '#static');
  await p.evaluate(() => document.fonts.ready);
  for (const t of times) { await p.evaluate(t => render(t), t); await p.screenshot({ path: `${out}/t${t}.png` }); }
  await b.close();
})();
