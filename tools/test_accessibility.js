// Kontrola přístupnosti webu: axe-core (WCAG 2.0, 2.1 a 2.2 úrovně A a AA + doporučené postupy),
// průchod klávesnicí (viditelný fokus, fokus nezakrytý lištami), reflow na 320 px a omezený pohyb.
// Vývojový nástroj týmu – web ho ke spuštění nepotřebuje. Náhrada za WAVE, který neumí soubory z disku.
//
// Spuštění (Node.js 18+, Google Chrome):
//   npm install --prefix /tmp/tranzistor-test playwright-core@1.48.2 axe-core@4.10.2
//   NODE_PATH=/tmp/tranzistor-test/node_modules node tools/test_accessibility.js [složka-webu]
const { chromium } = require('playwright-core');
const fs = require('fs'), path = require('path');
const AXE = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const ROOT = path.resolve(process.argv[2] || path.join(__dirname, '..', 'prototype'));
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const u = (p) => 'file://' + path.join(ROOT, p);
const PAGES = ['index.html', 'program.html', 'udalost.html?id=e052', 'ucinkujici.html', 'ucinkujici-detail.html?id=p022', 'sceny.html',
  'scena.html?id=v05', 'muj-program.html', 'prakticke-informace.html', 'hledani.html?q=malatova', 'hledani.html?q=xyz', 'o-festivalu.html'];
const SAVED = JSON.stringify(['e039', 'e043']);
let failures = 0;
const report = (ok, msg) => { console.log((ok ? 'PASS ' : 'FAIL ') + msg); if (!ok) failures++; };

(async () => {
  const b = await chromium.launch({ executablePath: CHROME });
  for (const vp of [{ n: 'mobil', width: 390 }, { n: 'desktop', width: 1280 }]) {
    const ctx = await b.newContext({ viewport: { width: vp.width, height: 844 }, reducedMotion: 'reduce' });
    const p = await ctx.newPage();
    await p.goto(u('index.html?ui=reset&cas=ted'));
    for (const pg of PAGES) {
      await p.evaluate((s) => localStorage.setItem('tranzistor:muj-program', s), SAVED);
      await p.goto(u(pg)); await p.waitForTimeout(150);
      await p.addScriptTag({ content: AXE });
      const res = await p.evaluate(async () => (await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] } })).violations);
      report(!res.length, vp.n + ' ' + pg + ' – axe bez porušení' + (res.length ? ': ' + res.map((v) => v.id + ' (' + v.nodes.length + ')').join(', ') : ''));
      // klávesnice: každý zastavený prvek má viditelný fokus a není schovaný pod lištou
      if (['program.html', 'muj-program.html', 'prakticke-informace.html', 'index.html'].includes(pg)) {
        const bad = new Set();
        for (let i = 0; i < 40; i++) {
          await p.keyboard.press('Tab');
          const r = await p.evaluate(() => {
            const el = document.activeElement; if (!el || el === document.body) return null;
            const target = el.matches('input[type="radio"]') ? el.nextElementSibling : el; // fokus čipu je vidět na štítku
            const cs = getComputedStyle(target), rect = target.getBoundingClientRect();
            const ring = (cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0) || cs.boxShadow !== 'none';
            const x = Math.min(Math.max(rect.left + rect.width / 2, 1), innerWidth - 1), y = Math.min(Math.max(rect.top + Math.min(rect.height / 2, 10), 1), innerHeight - 1);
            const hit = document.elementFromPoint(x, y);
            const covered = hit && !(target === hit || target.contains(hit) || hit.contains(target) || el.contains(hit));
            return { ring, covered, what: el.tagName.toLowerCase() + ' ' + (el.textContent || el.getAttribute('placeholder') || '').trim().slice(0, 30) };
          });
          if (r && !r.ring) bad.add('bez viditelného fokusu: ' + r.what);
          if (r && r.covered) bad.add('fokus zakrytý: ' + r.what);
        }
        report(!bad.size, vp.n + ' ' + pg + ' – klávesnice (40 kroků)' + (bad.size ? ': ' + [...bad].slice(0, 4).join('; ') : ''));
      }
    }
    await ctx.close();
  }
  const p = await (await b.newContext({ viewport: { width: 320, height: 640 } })).newPage();
  for (const pg of PAGES) {
    await p.goto(u(pg)); await p.waitForTimeout(80);
    const o = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    report(o <= 0, 'reflow 320 px – ' + pg + (o > 0 ? ' přetéká o ' + o + ' px' : ''));
  }
  const rm = await (await b.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' })).newPage();
  await rm.goto(u('index.html'));
  const running = await rm.evaluate(() => [...document.querySelectorAll('*')].filter((e) => getComputedStyle(e).animationName !== 'none').length);
  report(running === 0, 'omezený pohyb – při vypnutých animacích v systému neběží žádná animace (' + running + ')');
  await b.close();
  console.log(failures ? failures + ' FAILED' : 'ALL PASSED');
  process.exit(failures ? 1 : 0);
})();
