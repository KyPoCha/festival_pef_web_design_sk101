// Automatický test webu (složka web/): stránky na mobilu a desktopu, scénáře S1–S5, funkce bez JavaScriptu,
// metadata a strukturovaná data, odkazy na všech stránkách. Vývojový nástroj týmu – web ho ke spuštění nepotřebuje.
//
// Spuštění (Node.js 18+, Google Chrome):
//   npm install --prefix /tmp/tranzistor-test playwright-core@1.48.2
//   NODE_PATH=/tmp/tranzistor-test/node_modules node tools/test_web.js [složka-webu]
// Jinou cestu k Chromu lze zadat proměnnou CHROME.
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(process.argv[2] || path.join(__dirname, '..', 'web'));
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const url = (p) => 'file://' + path.join(ROOT, p);
const PAGES = ['index.html', 'program.html', 'program/sum-a-signal.html', 'ucinkujici.html', 'ucinkujici/kristyna-malatova.html',
  'sceny.html', 'sceny/nabrezi.html', 'muj-program.html', 'prakticke-informace.html', 'hledani.html?q=malatova', 'o-festivalu.html'];
let failures = 0;
const ok = (cond, msg) => { console.log((cond ? 'PASS ' : 'FAIL ') + msg); if (!cond) failures++; };

// ---------- statická kontrola všech stránek: odkazy, obrázky, metadata, JSON-LD
function allHtml(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((d) => d.isDirectory() ? allHtml(path.join(dir, d.name)) : d.name.endsWith('.html') ? [path.join(dir, d.name)] : []);
}
const files = allHtml(ROOT);
let broken = [], missingMeta = [], badLd = [];
for (const file of files) {
  const html = fs.readFileSync(file, 'utf8');
  const rel = path.relative(ROOT, file);
  for (const m of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    const target = m[1];
    if (/^(https?:|mailto:|#|\?|data:)/.test(target)) continue;
    const clean = target.split('#')[0].split('?')[0];
    if (clean && !fs.existsSync(path.resolve(path.dirname(file), clean))) broken.push(rel + ' → ' + target);
  }
  for (const need of ['<meta name="description"', '<link rel="canonical"', 'property="og:title"', 'property="og:image"', 'name="viewport"', '<html lang="cs">']) {
    if (!html.includes(need)) missingMeta.push(rel + ' bez ' + need);
  }
  for (const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try { JSON.parse(m[1]); } catch (e) { badLd.push(rel); }
  }
}
ok(files.length === 157, 'vygenerováno 157 stránek (' + files.length + ')');
ok(!broken.length, 'všechny místní odkazy a obrázky existují' + (broken.length ? ': ' + broken.slice(0, 5).join(', ') : ''));
ok(!missingMeta.length, 'každá stránka má popis, kanonickou adresu, Open Graph, viewport a jazyk' + (missingMeta.length ? ': ' + missingMeta.slice(0, 5).join(', ') : ''));
ok(!badLd.length, 'strukturovaná data (JSON-LD) jsou platný JSON' + (badLd.length ? ': ' + badLd.slice(0, 5).join(', ') : ''));
const titles = files.map((f) => (fs.readFileSync(f, 'utf8').match(/<title>([^<]+)<\/title>/) || [])[1]);
ok(new Set(titles).size === titles.length, 'každá stránka má jiný titulek');

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });

  // ---------- stránky na mobilu a desktopu
  for (const vp of [{ name: 'mobil', width: 360, height: 780 }, { name: 'desktop', width: 1280, height: 860 }]) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    for (const p of PAGES) {
      const page = await ctx.newPage();
      const errors = [];
      page.on('pageerror', (e) => errors.push(e.message));
      page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
      await page.goto(url(p));
      await page.waitForTimeout(150);
      const r = await page.evaluate(() => {
        const ids = [...document.querySelectorAll('[id]')].map((e) => e.id);
        const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map((h) => +h.tagName[1]);
        let jump = null; for (let i = 1; i < hs.length; i++) if (hs[i] - hs[i - 1] > 1) { jump = hs[i - 1] + '→' + hs[i]; break; }
        return { overflow: document.documentElement.scrollWidth - window.innerWidth, dup: ids.filter((id, i) => ids.indexOf(id) !== i),
          jump, imgs: [...document.images].filter((i) => i.complete && i.naturalWidth === 0).map((i) => i.getAttribute('src')),
          h1: document.querySelectorAll('h1').length };
      });
      const label = vp.name + ' ' + p;
      ok(!errors.length, label + ' – bez chyb v konzoli' + (errors.length ? ': ' + errors.join(' | ') : ''));
      ok(r.overflow <= 0, label + ' – bez vodorovného přetečení (' + r.overflow + ' px)');
      ok(!r.dup.length && r.h1 === 1 && !r.jump, label + ' – unikátní id, jeden h1, nadpisy bez přeskoku' + (r.dup.length || r.jump ? ' ' + r.dup.join(',') + ' ' + r.jump : ''));
      ok(!r.imgs.length, label + ' – obrázky se načetly' + (r.imgs.length ? ': ' + r.imgs.join(',') : ''));
      await page.close();
    }
    await ctx.close();
  }

  // ---------- obsah bez JavaScriptu (předgenerované stránky)
  const nojs = await (await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } })).newPage();
  await nojs.goto(url('program.html'));
  ok((await nojs.$$eval('#vypis .event-card', (n) => n.length)) === 77, 'bez JavaScriptu: program obsahuje všech 77 položek');
  ok(await nojs.evaluate(() => ['.filters-panel', '.day-switch', '.save'].every((s) => document.querySelector(s).offsetParent === null)),
    'bez JavaScriptu: filtry a tlačítka uložit se nezobrazují');
  await nojs.goto(url('program/sum-a-signal.html'));
  ok((await nojs.textContent('h1')).includes('Šum a Signál') && (await nojs.textContent('main')).includes('19:30'), 'bez JavaScriptu: detail položky má název i čas');
  await nojs.goto(url('ucinkujici/kristyna-malatova.html'));
  ok((await nojs.$$eval('#vystoupeni ~ ol .event-card', (n) => n.length)) === 2, 'bez JavaScriptu: profil řečnice uvádí 2 vystoupení');
  await nojs.goto(url('prakticke-informace.html'));
  ok((await nojs.textContent('main')).replace(/ /g, ' ').includes('1 490 Kč'), 'bez JavaScriptu: praktické informace včetně cen');

  // ---------- scénáře na mobilu
  const ctx = await browser.newContext({ viewport: { width: 360, height: 780 } });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => { console.log('FAIL pageerror ' + e.message); failures++; });

  // S1
  await page.goto(url('program.html'));
  await page.click('label:has(input[name="den"][value="d2"])');
  await page.click('#filtry-panel > summary');
  await page.selectOption('select[name="scena"]', 'v05');
  ok(/Zobrazeno 6 z 77/.test(await page.textContent('#pocet')), 'S1 filtr sobota + Nábřeží: ' + await page.textContent('#pocet'));
  ok(page.url().includes('den=d2') && page.url().includes('scena=v05'), 'S1 filtry jsou v adrese');
  await page.click('a[href="program/sum-a-signal.html"]');
  ok((await page.textContent('h1')).includes('Šum a Signál'), 'S1 detail koncertu Šum a Signál');
  await page.click('button[data-save="e052"]');
  ok((await page.getAttribute('button[data-save="e052"]', 'aria-pressed')) === 'true', 'S1 tlačítko uložit má aria-pressed=true');
  ok((await page.textContent('#toast')).includes('Přidáno'), 'S1 potvrzení o uložení');
  ok((await page.textContent('.tab-bar [data-my-count]')) === '1', 'S1 počet ve spodní liště = 1');
  const back = await page.getAttribute('.back-link', 'href');
  ok(back.includes('den=d2') && back.includes('scena=v05'), 'S1/S3 odkaz zpět zachová filtry: ' + back);
  await page.goto(url('muj-program.html'));
  await page.reload();
  ok(await page.isVisible('a[href="program/sum-a-signal.html"]'), 'S1 koncert je v Mém programu i po znovunačtení');

  // S2
  await page.goto(url('index.html'));
  await page.fill('#hledat', 'malatova');
  await page.press('#hledat', 'Enter');
  await page.waitForLoadState();
  ok(await page.isVisible('a[href="ucinkujici/kristyna-malatova.html"]'), 'S2 hledání „malatova“ najde řečnici');
  await page.click('a[href="ucinkujici/kristyna-malatova.html"]');
  await page.click('button[data-save="e043"]');
  await page.click('button[data-save="e047"]');
  await page.goto(url('program.html?den=d2&tema=t04'));
  ok(/Zobrazeno 4 z 77/.test(await page.textContent('#pocet')), 'S2 sobota + Bezpečnost: 4 položky');
  await page.click('button[data-save="e039"]');
  await page.goto(url('muj-program.html'));
  const notice = await page.textContent('.notice');
  ok(notice.includes('Capture the Flag') && notice.includes('nabourala'), 'S2 upozornění na kolizi e039 × e043');
  ok(await page.isVisible('.is-conflict'), 'S2 kolizní karty jsou zvýrazněné');
  await page.click('button[data-save="e043"]');
  await page.waitForTimeout(100);
  ok(!(await page.isVisible('.notice')), 'S2 po odebrání přednášky upozornění zmizí');

  // S3
  await page.goto(url('program.html?den=d3&rodiny=1'));
  ok(/Zobrazeno 9 z 77/.test(await page.textContent('#pocet')), 'S3 neděle + pro rodiny: 9 položek');
  await page.click('a[href="program/rodinna-dilna-svetelny-brouk.html"]');
  const det = await page.textContent('#detail');
  ok(det.includes('30 míst') && det.includes('Nutná') && det.includes('od 6 let'), 'S3 dílna: kapacita 30, rezervace, od 6 let');
  ok((await page.getAttribute('.back-link', 'href')).includes('rodiny=1'), 'S3 návrat do programu se zachovanými filtry');

  // S4
  await page.goto(url('index.html?cas=2027-06-05T19:45'));
  ok((await page.textContent('#prave-ted')).includes('Šum a Signál'), 'S4 sobota 19:45: na Nábřeží běží Šum a Signál');
  ok(await page.isVisible('.sim-bar'), 'S4 zobrazený čas je viditelně označen');
  await page.goto(url('index.html?cas=ted'));
  ok(!(await page.isVisible('.sim-bar')), 'S4 návrat ke skutečnému času');

  // S5
  await page.goto(url('hledani.html?q=tiskaren'));
  ok((await page.textContent('#vysledky')).includes('Orchestr Rozbitých Tiskáren') && await page.isVisible('a[href^="program/orchestr-rozbitych-tiskaren"]'), 'S5 „tiskaren“ najde orchestr i vystoupení');
  await page.goto(url('hledani.html?q=xyzneexistuje'));
  ok((await page.textContent('#vysledky')).includes('Nic jsme nenašli'), 'S5 prázdný výsledek má srozumitelnou zprávu');

  // účinkující: filtr a řazení
  await page.goto(url('ucinkujici.html?tema=t04&razeni=za'));
  const names = await page.$$eval('#vypis > li:not([hidden]) h2', (n) => n.map((x) => x.textContent));
  ok(names.length === 5 && names[0].localeCompare(names[names.length - 1], 'cs') > 0, 'filtr účinkujících: téma Bezpečnost (5), řazení Z–A: ' + names.join(', '));

  // potvrzení s Vrátit, menu a klávesnice
  await page.goto(url('program.html?den=d1'));
  await page.evaluate(() => localStorage.removeItem('tranzistor:muj-program'));
  await page.reload();
  await page.click('button[data-save="e001"]');
  ok(await page.isVisible('#toast .toast__undo'), 'potvrzení nabízí Vrátit');
  await page.click('#toast .toast__undo');
  ok((await page.getAttribute('button[data-save="e001"]', 'aria-pressed')) === 'false', 'Vrátit uložení zruší');
  await page.goto(url('program.html'));
  await page.keyboard.press('Tab');
  ok((await page.evaluate(() => document.activeElement.className)) === 'skip-link', 'první Tab je odkaz Přeskočit na obsah');
  ok(!(await page.isVisible('#hlavni-menu')) && await page.isVisible('.tab-bar'), 'mobil: menu sbalené, spodní lišta viditelná');
  await page.click('.menu-toggle');
  ok(await page.isVisible('#hlavni-menu a[href="sceny.html"]') && (await page.getAttribute('.menu-toggle', 'aria-expanded')) === 'true', 'tlačítko Menu menu rozbalí');

  await browser.close();
  console.log(failures ? failures + ' FAILED' : 'ALL PASSED');
  process.exit(failures ? 1 : 0);
})();
