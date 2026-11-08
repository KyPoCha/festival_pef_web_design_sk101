// Automatický test prototypu: všechny stránky na mobilu a desktopu, scénáře S1–S5 a varianty vzhledu.
// Vývojový nástroj týmu – web ho ke spuštění nepotřebuje.
//
// Spuštění (Node.js 18+, Google Chrome):
//   npm install --prefix /tmp/tranzistor-test playwright-core@1.48.2
//   NODE_PATH=/tmp/tranzistor-test/node_modules node tools/test_prototype.js [složka-webu] [složka-snímků]
// Výchozí složka webu je prototype/, snímky obrazovky se ukládají jen při zadání druhého argumentu.
// Jinou cestu k Chromu lze zadat proměnnou CHROME.
const { chromium } = require('playwright-core');
const path = require('path');
const ROOT = path.resolve(process.argv[2] || path.join(__dirname, '..', 'prototype'));
const SHOTS = process.argv[3] ? path.resolve(process.argv[3]) : null;
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const url = (p) => 'file://' + path.join(ROOT, p);
const PAGES = ['index.html', 'program.html', 'udalost.html?id=e052', 'ucinkujici.html', 'ucinkujici-detail.html?id=p022',
  'sceny.html', 'scena.html?id=v05', 'muj-program.html', 'prakticke-informace.html', 'hledani.html?q=malatova', 'o-festivalu.html'];
let failures = 0;
const ok = (cond, msg) => { console.log((cond ? 'PASS ' : 'FAIL ') + msg); if (!cond) failures++; };

(async () => {
  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  for (const vp of [{ name: 'mobil', width: 360, height: 780 }, { name: 'desktop', width: 1280, height: 860 }]) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 1 });
    for (const p of PAGES) {
      const page = await ctx.newPage();
      const errors = [];
      page.on('pageerror', (e) => errors.push(e.message));
      page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
      await page.goto(url(p));
      await page.waitForTimeout(150);
      const r = await page.evaluate(() => {
        const ids = [...document.querySelectorAll('[id]')].map((e) => e.id);
        const dup = ids.filter((id, i) => ids.indexOf(id) !== i);
        const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter((h) => h.offsetParent !== null || h.closest('.visually-hidden') || h.classList.contains('visually-hidden')).map((h) => +h.tagName[1]);
        let jump = null; for (let i = 1; i < hs.length; i++) if (hs[i] - hs[i - 1] > 1) { jump = hs[i - 1] + '→' + hs[i]; break; }
        const imgs = [...document.images].filter((i) => i.complete && i.naturalWidth === 0).map((i) => i.getAttribute('src'));
        const h1 = document.querySelectorAll('h1').length;
        return { overflow: document.documentElement.scrollWidth - window.innerWidth, dup, jump, imgs, h1, title: document.title };
      });
      const label = vp.name + ' ' + p;
      ok(!errors.length, label + ' – bez chyb v konzoli' + (errors.length ? ': ' + errors.join(' | ') : ''));
      ok(r.overflow <= 0, label + ' – bez vodorovného přetečení (' + r.overflow + ' px)');
      ok(!r.dup.length, label + ' – unikátní id' + (r.dup.length ? ': ' + r.dup.join(',') : ''));
      ok(r.h1 === 1, label + ' – právě jeden h1 (' + r.h1 + ')');
      ok(!r.jump, label + ' – nadpisy bez přeskočené úrovně' + (r.jump ? ' (' + r.jump + ')' : ''));
      ok(!r.imgs.length, label + ' – obrázky se načetly' + (r.imgs.length ? ': ' + r.imgs.join(',') : ''));
      const shot = p.replace(/[?=&]/g, '_').replace('.html', '');
      if (SHOTS) await page.screenshot({ path: path.join(SHOTS, vp.name + '-' + shot + '.png'), fullPage: false });
      await page.close();
    }
    await ctx.close();
  }

  // ---------------- scénáře na mobilu
  const ctx = await browser.newContext({ viewport: { width: 360, height: 780 } });
  const page = await ctx.newPage();
  page.on('pageerror', (e) => { console.log('FAIL pageerror ' + e.message); failures++; });

  // S1
  await page.goto(url('program.html'));
  await page.click('#filtry-panel > summary');
  await page.click('label:has(input[name="den"][value="d2"])');
  await page.selectOption('select[name="scena"]', 'v05');
  const s1count = await page.textContent('#pocet');
  ok(/Zobrazeno 6 z 77/.test(s1count), 'S1 filtr sobota + Nábřeží: ' + s1count);
  ok(page.url().includes('den=d2') && page.url().includes('scena=v05'), 'S1 filtry jsou v adrese: ' + page.url().split('?')[1]);
  await page.click('a[href="udalost.html?id=e052"]');
  ok((await page.textContent('h1')).includes('Šum a Signál'), 'S1 detail koncertu Šum a Signál');
  await page.click('button[data-save="e052"]');
  ok((await page.getAttribute('button[data-save="e052"]', 'aria-pressed')) === 'true', 'S1 tlačítko uložit má aria-pressed=true');
  ok((await page.textContent('#toast')).includes('Přidáno'), 'S1 potvrzení o uložení (role=status)');
  ok((await page.textContent('.my-link [data-my-count]')) === '1', 'S1 počítadlo v záhlaví = 1');
  const back = await page.getAttribute('.back-link', 'href');
  ok(back.includes('den=d2') && back.includes('scena=v05'), 'S1/S3 odkaz zpět zachová filtry: ' + back);
  await page.goto(url('muj-program.html'));
  await page.reload();
  ok(await page.isVisible('a[href="udalost.html?id=e052"]'), 'S1 koncert je v Mém programu i po znovunačtení');

  // S2
  await page.goto(url('index.html'));
  await page.fill('#hledat', 'malatova');
  await page.press('#hledat', 'Enter');
  await page.waitForLoadState();
  ok(await page.isVisible('a[href="ucinkujici-detail.html?id=p022"]'), 'S2 hledání „malatova“ najde Kristýnu Malátovou');
  await page.click('a[href="ucinkujici-detail.html?id=p022"]');
  const appearances = await page.$$eval('#vystoupeni ~ ol .event-card', (n) => n.length);
  ok(appearances === 2, 'S2 detail řečnice uvádí 2 vystoupení (' + appearances + ')');
  await page.click('button[data-save="e043"]');
  await page.click('button[data-save="e047"]');
  await page.goto(url('program.html?den=d2&tema=t04'));
  ok(/Zobrazeno 4 z 77/.test(await page.textContent('#pocet')), 'S2 sobota + Bezpečnost: 4 položky');
  await page.click('button[data-save="e039"]');
  await page.goto(url('muj-program.html'));
  const notice = await page.textContent('.notice');
  ok(notice.includes('Capture the Flag') && notice.includes('Jak jsem se nabourala'), 'S2 upozornění na kolizi e039 × e043');
  ok(await page.isVisible('.is-conflict'), 'S2 kolizní karty jsou zvýrazněné');
  await page.click('button[data-save="e043"]');
  await page.waitForTimeout(100);
  ok(!(await page.isVisible('.notice')), 'S2 po odebrání přednášky upozornění zmizí');

  // S3
  await page.goto(url('program.html?den=d3&rodiny=1'));
  ok(/Zobrazeno 9 z 77/.test(await page.textContent('#pocet')), 'S3 neděle + pro rodiny: 9 položek');
  await page.click('a[href="udalost.html?id=e057"]');
  const det = await page.textContent('#detail');
  ok(det.includes('30 míst') && det.includes('Nutná') && det.includes('od 6 let'), 'S3 dílna: kapacita 30, rezervace, od 6 let');
  ok((await page.getAttribute('.back-link', 'href')).includes('rodiny=1'), 'S3 návrat do programu se zachovanými filtry');
  await page.goto(url('prakticke-informace.html'));
  const prak = await page.textContent('main');
  ok(prak.replace(/\u00a0/g, ' ').includes('1 490 Kč') && prak.includes('zdarma') && prak.includes('neparkuje'), 'S3 ceny, vstup dětí zdarma, doprava');

  // S4
  await page.goto(url('index.html?cas=2027-06-05T19:45'));
  const ted = await page.textContent('#prave-ted');
  ok(ted.includes('Šum a Signál') && ted.includes('Lumen Field') === false || ted.includes('Šum a Signál'), 'S4 sobota 19:45: na Nábřeží běží Šum a Signál');
  ok(await page.isVisible('.sim-bar'), 'S4 ukázkový čas je viditelně označen');
  await page.goto(url('index.html?cas=ted'));
  ok(!(await page.isVisible('.sim-bar')), 'S4 návrat ke skutečnému času');

  // S5
  await page.goto(url('hledani.html?q=tiskaren'));
  const s5 = await page.textContent('#vysledky');
  ok(s5.includes('Orchestr Rozbitých Tiskáren') && (await page.isVisible('a[href="udalost.html?id=e022"]')), 'S5 „tiskaren“ najde orchestr i jeho vystoupení');
  await page.goto(url('hledani.html?q=xyzneexistuje'));
  ok((await page.textContent('#vysledky')).includes('Nic jsme nenašli'), 'S5 prázdný výsledek má srozumitelnou zprávu');

  // klávesnice a menu
  await page.goto(url('program.html'));
  await page.keyboard.press('Tab');
  ok((await page.evaluate(() => document.activeElement.className)) === 'skip-link', 'Klávesnice: první Tab je odkaz Přeskočit na obsah');
  ok(!(await page.isVisible('#hlavni-menu')), 'Mobil: hlavní menu je sbalené');
  ok(await page.isVisible('.tab-bar'), 'Mobil: spodní lišta je výchozí (volba týmu)');
  ok((await page.$$eval('.tab-bar svg.icon', (n) => n.length)) === 5, 'Mobil: spodní lišta má 5 ikon SVG');
  ok((await page.textContent('.tab-bar .badge')) === '3' && (await page.isVisible('.tab-bar .badge')), 'Mobil: odznak ve spodní liště ukazuje 3 uložené položky');
  await page.evaluate(() => localStorage.removeItem('tranzistor:muj-program'));
  await page.reload();
  ok(!(await page.isVisible('.tab-bar .badge')), 'Mobil: odznak s nulou je skrytý');
  await page.click('.menu-toggle');
  ok(await page.isVisible('#hlavni-menu a[href="sceny.html"]'), 'Mobil: tlačítko Menu menu rozbalí');
  ok((await page.getAttribute('.menu-toggle', 'aria-expanded')) === 'true', 'Mobil: aria-expanded se přepne');

  // varianty vzhledu (kolo 1 a kolo 2)
  const VARIANTS = [
    'theme:kyber,nav:bottom,card:tile,save:star',
    'theme:papir,nav:top,card:compact,save:text',
    'alert:strip,toast:pulse,pagenav:tiles,faq:plus,services:list,motion:lively,accent:cyan,hero:type',
    'alert:inline,toast:quiet,pagenav:tabs,faq:plain,services:plain,motion:none,accent:amber,hero:transistor',
  ];
  for (const v of VARIANTS) {
    await page.goto(url('index.html?ui=reset'));
    await page.evaluate(() => localStorage.setItem('tranzistor:muj-program', JSON.stringify(['e039', 'e043'])));
    for (const pg of ['program.html?den=d2&scena=v05', 'muj-program.html', 'prakticke-informace.html', 'index.html']) {
      await page.goto(url(pg + (pg.includes('?') ? '&' : '?') + 'ui=' + v));
      await page.waitForTimeout(80);
      const attrs = await page.evaluate((keys) => keys.map((k) => document.documentElement.getAttribute('data-ui-' + k)).join(','), v.split(',').map((x) => x.split(':')[0]));
      if (pg === 'index.html') ok(attrs === v.split(',').map((x) => x.split(':')[1]).join(','), 'Varianta ' + v + ' se použije');
      const ov = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      ok(ov <= 0, 'Varianta ' + v.slice(0, 40) + '… ' + pg + ' bez přetečení (' + ov + ' px)');
      if (pg === 'muj-program.html') {
        const n = await page.textContent('.notice');
        ok(n.includes('Capture the Flag') && n.includes('nabourala'), 'Varianta ' + v.slice(0, 20) + '… upozornění na kolizi obsahuje obě položky');
      }
    }
    if (v.includes('nav:bottom')) ok(await page.isVisible('.tab-bar'), 'Varianta nav:bottom zobrazí spodní lištu');
    if (SHOTS) await page.screenshot({ path: path.join(SHOTS, 'varianta-' + v.split(',')[0].split(':')[1] + '.png') });
  }
  // potvrzení s možností vrátit
  await page.goto(url('program.html?ui=reset&den=d1'));
  await page.evaluate(() => localStorage.removeItem('tranzistor:muj-program'));
  await page.reload();
  await page.click('button[data-save="e001"]');
  ok(await page.isVisible('#toast .toast__undo'), 'Potvrzení po uložení nabízí Vrátit');
  await page.click('#toast .toast__undo');
  ok((await page.getAttribute('button[data-save="e001"]', 'aria-pressed')) === 'false', 'Vrátit uložení zruší');
  await page.goto(url('index.html?ui=reset'));
  await browser.close();
  console.log(failures ? failures + ' FAILED' : 'ALL PASSED');
  process.exit(failures ? 1 : 0);
})();
