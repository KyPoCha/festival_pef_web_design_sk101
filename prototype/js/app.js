/* Tranzistor 2027 – web festivalu
   Jeden skript pro všechny stránky. Data čte z window.TRANZISTOR_DATA (js/data.js,
   odvozeno z data.json), takže web funguje i po otevření ze souborového systému.
   Klasický skript bez modulů: <script type="module"> prohlížeč z file:// nenačte. */
(function () {
  'use strict';

  var D = window.TRANZISTOR_DATA;
  var STORE_KEY = 'tranzistor:muj-program';
  var UI_KEY = 'tranzistor:ui';
  var NOW_KEY = 'tranzistor:cas';
  var LAST_PROGRAM_KEY = 'tranzistor:posledni-program';
  var TZ = '+02:00';

  // ---------------------------------------------------------------- indexy
  function index(list) {
    var map = {};
    list.forEach(function (item) { map[item.id] = item; });
    return map;
  }
  var EV = index(D.events), PE = index(D.performers), VE = index(D.venues), TR = index(D.tracks),
      DA = index(D.days), TY = index(D.eventTypes), PT = index(D.performerTypes), LV = index(D.levels),
      LA = index(D.languages);
  var eventsByPerformer = {};
  D.events.forEach(function (e) {
    e.performerIds.forEach(function (pid) { (eventsByPerformer[pid] = eventsByPerformer[pid] || []).push(e); });
  });

  // ---------------------------------------------------------------- pomocné funkce
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function params() { return new URLSearchParams(window.location.search); }
  function norm(s) {
    return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
  }
  function hm(iso) { return iso.slice(11, 16); }
  function time(iso) { return '<time datetime="' + esc(iso) + '">' + hm(iso) + '</time>'; }
  function dateCz(iso) {
    var d = iso.slice(0, 10).split('-');
    return '<time datetime="' + d.join('-') + '">' + Number(d[2]) + '. ' + Number(d[1]) + '. ' + d[0] + '</time>';
  }
  function ms(iso) { return new Date(iso).getTime(); }
  function overlaps(a, b) { return ms(a.start) < ms(b.end) && ms(b.start) < ms(a.end); }
  function byStart(a, b) { return ms(a.start) - ms(b.start) || a.venueId.localeCompare(b.venueId); }
  function names(ids) { return ids.map(function (id) { return PE[id].name; }).join(', '); }
  function pluralCz(n, one, few, many) { return n === 1 ? one : (n >= 2 && n <= 4 ? few : many); }
  function langLabel(e) { return e.language ? LA[e.language].label : 'Bez mluveného slova'; }
  function storage(kind) {
    try { return window[kind]; } catch (err) { return null; }
  }
  function read(kind, key, fallback) {
    try { var v = storage(kind).getItem(key); return v == null ? fallback : JSON.parse(v); } catch (err) { return fallback; }
  }
  function write(kind, key, value) {
    try { storage(kind).setItem(key, JSON.stringify(value)); } catch (err) { /* soukromé okno apod. */ }
  }

  // ---------------------------------------------------------------- ikony
  // Tvary ikon podle Material Icons (Google, Apache License 2.0), vložené jako inline SVG.
  var ICONS = {
    home: 'M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z',
    program: 'M17 10H7v2h10v-2zm2-7h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zm-5-5H7v2h7v-2z',
    people: 'M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z',
    place: 'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z',
    star: 'M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z',
    add: 'M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z',
    check: 'M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z',
    menu: 'M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z',
    search: 'M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z',
    warning: 'M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z',
    expand: 'M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z',
    remove: 'M19 13H5v-2h14v2z',
    undo: 'M12.5 8c-2.65 0-5.05.99-6.9 2.6L2 7v9h9l-3.62-3.62c1.39-1.16 3.16-1.88 5.12-1.88 3.54 0 6.55 2.31 7.6 5.5l2.37-.78C21.08 11.03 17.15 8 12.5 8z',
    ticket: 'M22 10V6c0-1.11-.9-2-2-2H4c-1.1 0-1.99.89-1.99 2v4c1.1 0 1.99.9 1.99 2s-.89 2-2 2v4c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2v-4c-1.1 0-2-.9-2-2s.9-2 2-2zm-9 7.5h-2v-2h2v2zm0-4.5h-2v-2h2v2zm0-4.5h-2v-2h2v2z',
    train: 'M12 2c-4 0-8 .5-8 4v9.5C4 17.43 5.57 19 7.5 19L6 20.5v.5h2.23l2-2H14l2 2h2v-.5L16.5 19c1.93 0 3.5-1.57 3.5-3.5V6c0-3.5-3.58-4-8-4zM7.5 17c-.83 0-1.5-.67-1.5-1.5S6.67 14 7.5 14s1.5.67 1.5 1.5S8.33 17 7.5 17zm3.5-7H6V6h5v4zm2 0V6h5v4h-5zm3.5 7c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z',
    accessible: 'M12 4c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm7 7v-2c-1.54.02-3.08-.75-4.08-1.85l-1.29-1.43c-.17-.19-.38-.34-.61-.45-.01 0-.01-.01-.02-.01H13c-.35-.2-.75-.3-1.19-.26C10.76 5.09 10 6.01 10 7.07V13c0 1.1.9 2 2 2h5v5h2v-5.5c0-1.1-.9-2-2-2h-3v-3.45c1.29 1.07 3.25 1.94 5 1.95zm-6.17 5c-.41 1.16-1.52 2-2.83 2-1.66 0-3-1.34-3-3 0-1.31.84-2.41 2-2.83V12.1c-2.28.46-4 2.48-4 4.9 0 2.76 2.24 5 5 5 2.42 0 4.44-1.72 4.9-4h-2.07z',
    cafe: 'M20 3H4v10c0 2.21 1.79 4 4 4h6c2.21 0 4-1.79 4-4v-3h2c1.11 0 2-.9 2-2V5c0-1.11-.89-2-2-2zm0 5h-2V5h2v3zM4 19h16v2H4z',
    info: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z',
    help: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z',
    restaurant: 'M11 9H9V2H7v7H5V2H3v7c0 2.12 1.66 3.84 3.75 3.97V22h2.5v-9.03C11.34 12.84 13 11.12 13 9V2h-2v7zm5-3v8h2.5v8H21V2c-2.76 0-5 2.24-5 4z',
    water: 'M3 2l2.01 18.23C5.13 21.23 5.97 22 7 22h10c1.03 0 1.87-.77 1.99-1.77L21 2H3zm9 17c-1.66 0-3-1.34-3-3 0-2 3-5.4 3-5.4s3 3.4 3 5.4c0 1.66-1.34 3-3 3zm6.33-11H5.67l-.44-4h13.53l-.43 4z',
    card: 'M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z',
    bag: 'M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z',
    hospital: 'M19 3H5c-1.1 0-1.99.9-1.99 2L3 19c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-1 11h-4v4h-4v-4H6v-4h4V6h4v4h4v4z',
    face: 'M9 11.75c-.69 0-1.25.56-1.25 1.25s.56 1.25 1.25 1.25 1.25-.56 1.25-1.25-.56-1.25-1.25-1.25zm6 0c-.69 0-1.25.56-1.25 1.25s.56 1.25 1.25 1.25 1.25-.56 1.25-1.25-.56-1.25-1.25-1.25zM12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8 0-.29.02-.58.05-.86 2.36-1.05 4.23-2.98 5.21-5.37C11.07 8.33 14.05 10 17.42 10c.78 0 1.53-.09 2.25-.26.21.71.33 1.47.33 2.26 0 4.41-3.59 8-8 8z',
    wifi: 'M1 9l2 2c4.97-4.97 13.03-4.97 18 0l2-2C16.93 2.93 7.08 2.93 1 9zm8 8l3 3 3-3c-1.65-1.66-4.34-1.66-6 0zm-4-4l2 2c2.76-2.76 7.24-2.76 10 0l2-2C15.14 9.14 8.87 9.14 5 13z',
    bike: 'M15.5 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM5 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5zm5.8-10l2.4-2.4.8.8c1.3 1.3 3 2.1 5.1 2.1V9c-1.5 0-2.7-.6-3.6-1.5l-1.9-1.9c-.5-.4-1-.6-1.6-.6s-1.1.2-1.4.6L7.8 8.4c-.4.4-.6.9-.6 1.4 0 .6.2 1.1.6 1.4L11 14v5h2v-6.2l-2.2-2.3zM19 12c-2.8 0-5 2.2-5 5s2.2 5 5 5 5-2.2 5-5-2.2-5-5-5zm0 8.5c-1.9 0-3.5-1.6-3.5-3.5s1.6-3.5 3.5-3.5 3.5 1.6 3.5 3.5-1.6 3.5-3.5 3.5z',
    car: 'M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z',
    clock: 'M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z'
  };
  function icon(name, cls) {
    return '<svg class="icon' + (cls ? ' ' + cls : '') + '" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"><path d="' + ICONS[name] + '"/></svg>';
  }

  // ---------------------------------------------------------------- varianty vzhledu (pro výběr návrhu)
  // ?ui=theme:kyber,nav:bottom,card:tile,save:star – volba se pamatuje v prohlížeči.
  // Výchozí kombinace podle hlasování týmu (iterace 2): Kyber, spodní lišta, dlaždice, textové tlačítko.
  // Kolo 2 (komponenty a animace): výchozí jsou doporučení, o kterých tým rozhoduje na druhé stránce pro výběr.
  var UI_DEFAULTS = { theme: 'kyber', nav: 'bottom', card: 'tile', save: 'text',
    alert: 'panel', toast: 'undo', pagenav: 'chips', faq: 'cards', services: 'cards', motion: 'subtle', accent: 'green', hero: 'circuit' };
  var UI_ALLOWED = { theme: ['signal', 'kyber', 'papir'], nav: ['top', 'bottom'], card: ['timeline', 'tile', 'compact'], save: ['text', 'star'],
    alert: ['panel', 'strip', 'inline'], toast: ['undo', 'pulse', 'quiet'], pagenav: ['chips', 'tiles', 'tabs'], faq: ['cards', 'plus', 'plain'],
    services: ['cards', 'list', 'plain'], motion: ['subtle', 'lively', 'none'], accent: ['green', 'cyan', 'amber'], hero: ['transistor', 'circuit', 'type'] };
  function applyUi() {
    var ui = Object.assign({}, UI_DEFAULTS, read('localStorage', UI_KEY, {}));
    var fromUrl = params().get('ui');
    if (fromUrl) {
      if (fromUrl === 'reset') ui = Object.assign({}, UI_DEFAULTS);
      fromUrl.split(',').forEach(function (pair) {
        var kv = pair.split(':');
        if (UI_ALLOWED[kv[0]] && UI_ALLOWED[kv[0]].indexOf(kv[1]) !== -1) ui[kv[0]] = kv[1];
      });
      write('localStorage', UI_KEY, ui);
    }
    Object.keys(ui).forEach(function (k) { document.documentElement.setAttribute('data-ui-' + k, ui[k]); });
    return ui;
  }
  var UI = applyUi();

  // ---------------------------------------------------------------- čas („Právě teď“)
  // ?cas=2027-06-05T19:45 nasimuluje čas festivalu (pražský čas); ?cas=ted vrátí skutečný.
  function currentTime() {
    var p = params().get('cas');
    if (p === 'ted') { try { storage('sessionStorage').removeItem(NOW_KEY); } catch (err) { /* */ } }
    else if (p && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(p)) write('sessionStorage', NOW_KEY, p);
    var sim = p === 'ted' ? null : read('sessionStorage', NOW_KEY, null);
    return sim ? { ms: ms(sim + ':00' + TZ), simulated: sim } : { ms: Date.now(), simulated: null };
  }
  var NOW = currentTime();
  function simLabel(sim) {
    var day = D.days.filter(function (d) { return d.date === sim.slice(0, 10); })[0];
    return (day ? day.weekday : sim.slice(0, 10)) + ' ' + sim.slice(11, 16);
  }

  // ---------------------------------------------------------------- Můj program
  function saved() { return read('localStorage', STORE_KEY, []).filter(function (id) { return EV[id]; }); }
  function isSaved(id) { return saved().indexOf(id) !== -1; }
  function setSaved(list) { write('localStorage', STORE_KEY, list); updateBadge(); }
  function toggleSaved(id) {
    var list = saved(), i = list.indexOf(id);
    if (i === -1) list.push(id); else list.splice(i, 1);
    setSaved(list);
    return i === -1;
  }
  function updateBadge() {
    var n = saved().length;
    $$('[data-my-count]').forEach(function (b) { b.textContent = n; b.setAttribute('data-count', n); });
    // čtečka obrazovky slyší „Můj plán, 2 uložené položky“ – odznak sám je skrytý
    $$('[data-my-count-sr]').forEach(function (s) { s.textContent = ', ' + n + ' ' + pluralCz(n, 'uložená položka', 'uložené položky', 'uložených položek'); });
    $$('[data-my-count-label]').forEach(function (b) {
      b.textContent = n + ' ' + pluralCz(n, 'uložená položka', 'uložené položky', 'uložených položek');
    });
  }
  function conflictsOf(list) {
    var pairs = [];
    for (var i = 0; i < list.length; i++) {
      for (var j = i + 1; j < list.length; j++) {
        if (overlaps(list[i], list[j])) pairs.push([list[i], list[j]]);
      }
    }
    return pairs;
  }

  var toastTimer = null;
  function announce(text, undoId) {
    var t = $('#toast');
    if (!t) return;
    var withUndo = undoId && UI.toast === 'undo';
    t.innerHTML = (UI.toast === 'quiet' ? '' : icon(undoId && !isSaved(undoId) ? 'remove' : 'check', 'toast__icon')) +
      '<span class="toast__text">' + esc(text) + '</span> ' +
      (withUndo ? '<button type="button" class="toast__undo" data-undo="' + undoId + '">' + icon('undo') + 'Vrátit</button>' : '');
    t.classList.remove('is-shown');
    void t.offsetWidth; // znovu spustí animaci vyjetí
    t.classList.add('is-shown');
    if (UI.toast === 'pulse') {
      $$('[data-my-count]').forEach(function (b) { b.classList.remove('is-bumping'); void b.offsetWidth; b.classList.add('is-bumping'); });
    }
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.classList.remove('is-shown'); t.innerHTML = ''; }, withUndo ? 6000 : 3500);
  }

  // ---------------------------------------------------------------- komponenty
  function saveButton(e) {
    var on = isSaved(e.id);
    var label = UI.card === 'compact' && document.body.dataset.page !== 'event'
      ? '<span aria-hidden="true">' + (on ? '★' : '☆') + '</span><span class="visually-hidden">' + (on ? 'Uloženo' : 'Uložit') + '</span>'
      : UI.save === 'star'
      ? '<span aria-hidden="true">' + (on ? '★' : '☆') + '</span> <span class="save__text">' + (on ? 'Uloženo' : 'Uložit') + '</span>'
      : icon(on ? 'check' : 'add') + '<span class="save__text">' + (on ? 'V Mém programu' : 'Do Mého programu') + '</span>';
    return '<button type="button" class="save" data-save="' + e.id + '" aria-pressed="' + on + '">' + label +
      '<span class="visually-hidden">: ' + esc(e.title) + '</span></button>';
  }
  // Společné komponenty: seznam s ikonami (karty) a skládací blok (disclosure)
  function iconList(items) {
    return '<ul class="icon-list">' + items.map(function (it) {
      return '<li class="icon-list__item"><span class="icon-list__icon">' + icon(it.icon) + '</span><div>' +
        (it.title ? '<h3 class="icon-list__title">' + esc(it.title) + '</h3>' : '') + '<p>' + esc(it.text) + '</p></div></li>';
    }).join('') + '</ul>';
  }
  function disclosureIcon() { return '<span class="disclosure__icon">' + icon('expand', 'disclosure__chevron') + icon('add', 'disclosure__plus') + icon('remove', 'disclosure__minus') + '</span>'; }
  function trackChip(t) {
    var n = D.events.filter(function (e) { return e.trackId === t.id; }).length;
    return '<li><a class="track-chip track-chip--' + t.id + '" href="program.html?tema=' + t.id + '">' +
      '<span class="track-chip__name">' + esc(t.name) + '</span><span class="track-chip__count">' + n + '</span></a></li>';
  }
  function trackTag(id) { return '<span class="tag tag--track tag--' + id + '">' + esc(TR[id].name) + '</span>'; }
  function eventTags(e) {
    var t = [trackTag(e.trackId), '<span class="tag">' + esc(TY[e.type].label) + '</span>'];
    if (e.familyFriendly) t.push('<span class="tag tag--family">Pro rodiny</span>');
    if (e.registrationRequired) t.push('<span class="tag tag--reg">Nutná rezervace</span>');
    return '<p class="tags">' + t.join(' ') + '</p>';
  }
  function eventCard(e, opts) {
    opts = opts || {};
    var heading = opts.heading || 'h4';
    return '<li><article class="card event-card event-card--' + e.trackId + (opts.conflict ? ' is-conflict' : '') + '">' +
      '<p class="event-card__time">' + icon('clock', 'icon--time') + time(e.start) + '<span>do ' + time(e.end) + '</span></p>' +
      '<div class="event-card__body">' +
        '<' + heading + '><a href="udalost.html?id=' + e.id + '">' + esc(e.title) + '</a></' + heading + '>' +
        '<p class="event-card__where">' + icon('place', 'icon--inline') + (opts.showDay ? esc(DA[e.dayId].label) + ' · ' : '') + esc(VE[e.venueId].name) +
          ' · ' + esc(names(e.performerIds)) + '</p>' +
        eventTags(e) +
        (opts.clashWith ? '<p class="clash-note">' + icon('warning') + 'Kryje se s: ' + opts.clashWith.map(function (x) { return esc(x.title); }).join(', ') + '</p>' : '') +
      '</div>' +
      '<div class="event-card__actions">' + saveButton(e) + '</div>' +
    '</article></li>';
  }
  function performerCard(p, heading) {
    heading = heading || 'h3';
    return '<li class="card person-card">' +
      '<img src="' + esc(p.image.src) + '" alt="" width="56" height="56" loading="lazy">' +
      '<div class="person-card__text"><' + heading + '><a href="ucinkujici-detail.html?id=' + p.id + '">' + esc(p.name) + '</a></' + heading + '>' +
      '<p class="person-card__tagline">' + esc(p.tagline) + '</p>' +
      '<p class="person-card__meta">' + esc(PT[p.type].label) + ' · ' + esc(D.countries[p.country]) + '</p></div>' +
      (p.headliner ? '<span class="tag tag--headliner person-card__star">Hvězda</span>' : '') + '</li>';
  }
  // Hlavní hvězda pro vodorovný pás na úvodní stránce
  function starTile(p) {
    return '<li class="star-tile"><a href="ucinkujici-detail.html?id=' + p.id + '">' +
      '<img src="' + esc(p.image.src) + '" alt="" width="112" height="112" loading="lazy">' +
      '<span class="star-tile__name">' + esc(p.name) + '</span><span class="star-tile__tagline">' + esc(p.tagline) + '</span></a></li>';
  }
  // Kompaktní řádek položky programu (souběžný program, nejbližší program)
  function eventRow(e, showDay) {
    return '<li><a class="event-row event-row--' + e.trackId + '" href="udalost.html?id=' + e.id + '">' +
      '<span class="event-row__time">' + (showDay ? esc(DA[e.dayId].weekday.slice(0, 2)) + ' ' : '') + time(e.start) + '</span>' +
      '<span class="event-row__title">' + esc(e.title) + '</span>' +
      '<span class="event-row__where">' + esc(VE[e.venueId].name) + ' · ' + esc(TY[e.type].label) + '</span></a></li>';
  }
  function groupByDay(list, render) {
    return D.days.map(function (d) {
      var items = list.filter(function (e) { return e.dayId === d.id; });
      if (!items.length) return '';
      return '<section class="day-group" aria-labelledby="den-' + d.id + '"><h3 id="den-' + d.id + '">' + esc(d.label) +
        ' <small>· ' + esc(d.theme) + '</small></h3><ol class="event-list">' + items.map(render).join('') + '</ol></section>';
    }).join('');
  }
  function setTitle(text) { document.title = text + ' – Tranzistor 2027'; }
  function setDescription(text) {
    var m = $('meta[name="description"]');
    if (m) m.setAttribute('content', text);
  }
  function crumb(text) { var c = $('[data-crumb]'); if (c) c.textContent = text; }
  function notFound(main, what, back) {
    main.innerHTML = '<h1>' + esc(what) + ' nenalezen(a)</h1><p>Odkaz je neplatný nebo zastaralý.</p>' +
      '<p><a class="button" href="' + back.href + '">' + esc(back.text) + '</a></p>';
  }

  // „Právě teď“ – co na scéně běží a co následuje
  function nowAndNext(venueId) {
    var list = D.events.filter(function (e) { return e.venueId === venueId; }).sort(byStart);
    var now = list.filter(function (e) { return ms(e.start) <= NOW.ms && NOW.ms < ms(e.end); })[0] || null;
    var next = list.filter(function (e) { return ms(e.start) > NOW.ms; })[0] || null;
    return { now: now, next: next };
  }
  function nowItem(v) {
    var nn = nowAndNext(v.id);
    var line = function (label, e) {
      return '<p><span class="now-label">' + label + '</span><br>' + (e
        ? time(e.start) + '–' + time(e.end) + ' <a href="udalost.html?id=' + e.id + '">' + esc(e.title) + '</a>'
        : '—') + '</p>';
    };
    return '<li class="card now-item"><h3><a href="scena.html?id=' + v.id + '">' + esc(v.name) + '</a></h3>' +
      line('Právě teď', nn.now) + line('Následuje', nn.next) + '</li>';
  }
  function simBar() {
    if (!NOW.simulated) return;
    var bar = document.createElement('div');
    bar.className = 'sim-bar';
    bar.innerHTML = '<div class="container"><span>Program zobrazujeme k času <strong>' + esc(simLabel(NOW.simulated)) +
      '</strong></span><a href="?cas=ted">Zobrazit aktuální čas</a></div>';
    $('.site-header').appendChild(bar); // uvnitř záhlaví, aby byl obsah v orientačním bodu
  }

  // ---------------------------------------------------------------- stránky
  var pages = {};

  function heroCircuit() {
    var el = $('.hero__circuit');
    if (!el) return;
    var paths = '', dots = '';
    for (var i = 0; i < 9; i++) {
      var y = 40 + i * 62, x = (i * 97) % 260, w = 300 + (i * 131) % 420;
      var d = 'M' + x + ' ' + y + ' h' + w + ' l36 36 h' + (120 + (i * 53) % 260);
      paths += '<path class="trace" d="' + d + '"/><path class="pulse" style="animation-delay:' + (i * 0.7).toFixed(1) + 's" d="' + d + '"/>';
      dots += '<circle cx="' + x + '" cy="' + y + '" r="6"/>';
    }
    el.innerHTML = '<svg viewBox="0 0 1200 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">' + paths + dots + '</svg>';
  }

  pages.home = function () {
    heroCircuit();
    var start = ms(D.days[0].date + 'T' + D.days[0].opens + ':00' + TZ);
    var end = ms(D.days[D.days.length - 1].date + 'T' + D.days[D.days.length - 1].closes + ':00' + TZ);
    var box = $('#prave-ted');
    var intro;
    $$('[data-stat]').forEach(function (el) {
      el.textContent = { days: D.days.length, venues: D.venues.length, events: D.events.length, performers: D.performers.length }[el.getAttribute('data-stat')];
    });
    if (NOW.ms < start) {
      var left = start - NOW.ms, days = Math.floor(left / 86400000), hours = Math.floor(left % 86400000 / 3600000);
      var first = D.events.filter(function (e) { return e.dayId === D.days[0].id; }).sort(byStart).slice(0, 4);
      box.innerHTML = '<div class="countdown card"><p class="countdown__label">Do zahájení zbývá</p>' +
        '<p class="countdown__value"><strong>' + days + '</strong> ' + pluralCz(days, 'den', 'dny', 'dní') +
        ' <strong>' + hours + '</strong> ' + pluralCz(hours, 'hodina', 'hodiny', 'hodin') + '</p>' +
        '<p>Brány se otevírají v ' + esc(D.days[0].weekday) + ' ' + esc(D.days[0].label.replace(/^\S+ /, '')) + ' ve ' + esc(D.days[0].opens) + '. ' +
        'Během festivalu tu uvidíte, co na které scéně právě běží – <a href="?cas=2027-06-05T19:45">podívejte se, jak vypadá sobotní večer</a>.</p></div>' +
        '<h3 class="subhead">Na úvod festivalu</h3><ol class="event-rows">' + first.map(function (e) { return eventRow(e, true); }).join('') + '</ol>';
    } else if (NOW.ms > end) {
      box.innerHTML = '<p>Letošní ročník skončil. Děkujeme, že jste byli s námi.</p>';
    } else {
      box.innerHTML = '<p>Program na všech scénách k času <strong>' + esc(NOW.simulated ? simLabel(NOW.simulated) : 'teď') + '</strong>.</p>' +
        '<ul class="now-list grid grid--3">' + D.venues.map(nowItem).join('') + '</ul>';
    }

    $('#hvezdy').innerHTML = D.performers.filter(function (p) { return p.headliner; }).map(starTile).join('');
    $('#temata').innerHTML = D.tracks.map(trackChip).join('');
    $('#dny').innerHTML = D.days.map(function (d) {
      var n = D.events.filter(function (e) { return e.dayId === d.id; }).length;
      return '<li><a class="day-card card" href="program.html?den=' + d.id + '">' +
        '<span class="day-card__date">' + esc(d.label) + '</span><span class="day-card__theme">' + esc(d.theme) + '</span>' +
        '<span class="day-card__meta">' + esc(d.opens) + '–' + esc(d.closes) + ' · ' + n + ' ' + pluralCz(n, 'položka', 'položky', 'položek') + '</span></a></li>';
    }).join('');
  };

  pages.program = function () {
    var form = $('#filtry');
    var fields = ['den', 'scena', 'tema', 'format', 'uroven', 'jazyk'];
    var sources = { scena: D.venues, tema: D.tracks, format: D.eventTypes, uroven: D.levels };
    Object.keys(sources).forEach(function (name) {
      var sel = form.elements[name];
      sources[name].forEach(function (item) {
        sel.insertAdjacentHTML('beforeend', '<option value="' + item.id + '">' + esc(item.name || item.label) + '</option>');
      });
    });
    D.languages.forEach(function (l) {
      form.elements.jazyk.insertAdjacentHTML('beforeend', '<option value="' + l.id + '">' + esc(l.label) + '</option>');
    });
    form.elements.jazyk.insertAdjacentHTML('beforeend', '<option value="zadny">Bez mluveného slova (hudba)</option>');
    $('#dny-volba').innerHTML = '<label><input type="radio" name="den" value="" form="filtry"><span>Vše</span></label>' +
      D.days.map(function (d) {
        return '<label><input type="radio" name="den" value="' + d.id + '" form="filtry"><span>' + esc(d.weekday.charAt(0).toUpperCase() + d.weekday.slice(1, 2)) +
          ' <small>' + esc(d.label.replace(/^\S+ /, '')) + '</small><span class="visually-hidden"> (' + esc(d.weekday) + ')</span></span></label>';
      }).join('');

    var p = params();
    fields.forEach(function (f) {
      var v = p.get(f) || '';
      if (f === 'den') $$('input[name="den"]').forEach(function (r) { r.checked = r.value === v; });
      else if (form.elements[f]) form.elements[f].value = v;
    });
    form.elements.rodiny.checked = p.get('rodiny') === '1';

    var wide = window.matchMedia('(min-width: 900px)');
    var panel = $('#filtry-panel');
    function syncPanel() { if (wide.matches) panel.open = true; }
    syncPanel();
    if (wide.addEventListener) wide.addEventListener('change', syncPanel);

    function state() {
      var s = {};
      fields.forEach(function (f) {
        var v = f === 'den' ? (($('input[name="den"]:checked') || {}).value || '') : form.elements[f].value;
        if (v) s[f] = v;
      });
      if (form.elements.rodiny.checked) s.rodiny = '1';
      return s;
    }
    function render() {
      var s = state();
      var list = D.events.filter(function (e) {
        return (!s.den || e.dayId === s.den) && (!s.scena || e.venueId === s.scena) &&
          (!s.tema || e.trackId === s.tema) && (!s.format || e.type === s.format) &&
          (!s.uroven || e.level === s.uroven) &&
          (!s.jazyk || (s.jazyk === 'zadny' ? e.language === null : e.language === s.jazyk)) &&
          (!s.rodiny || e.familyFriendly);
      }).sort(byStart);
      var active = Object.keys(s).filter(function (k) { return k !== 'den'; }).length;
      $('#pocet-filtru').textContent = active ? ' (' + active + ' ' + pluralCz(active, 'aktivní', 'aktivní', 'aktivních') + ')' : '';
      $('#pocet').textContent = 'Zobrazeno ' + list.length + ' z ' + D.events.length + ' položek programu';
      $('#vypis').innerHTML = list.length
        ? groupByDay(list, function (e) { return eventCard(e); })
        : '<div class="card empty"><p>Filtrům neodpovídá žádná položka.</p><p><button type="reset" form="filtry" class="button">Zrušit filtry</button></p></div>';
      var query = new URLSearchParams(s).toString();
      var url = 'program.html' + (query ? '?' + query : '');
      window.history.replaceState(null, '', url);
      write('sessionStorage', LAST_PROGRAM_KEY, url);
    }
    form.addEventListener('change', render);
    $('#dny-volba').addEventListener('change', render);
    form.addEventListener('submit', function (ev) { ev.preventDefault(); render(); });
    form.addEventListener('reset', function () { setTimeout(function () { $$('input[name="den"]')[0].checked = true; render(); }, 0); });
    render();
  };

  pages.event = function () {
    var e = EV[params().get('id')];
    var main = $('#obsah');
    if (!e) { notFound(main, 'Položka programu', { href: 'program.html', text: 'Zpět na program' }); return; }
    var v = VE[e.venueId], d = DA[e.dayId];
    setTitle(e.title);
    setDescription(e.description);
    crumb(e.title);
    var parallel = D.events.filter(function (x) { return x.id !== e.id && overlaps(x, e); }).sort(byStart);
    var back = read('sessionStorage', LAST_PROGRAM_KEY, 'program.html');
    $('#detail').innerHTML =
      '<p><a class="back-link" href="' + esc(back) + '">← Zpět na program</a></p>' +
      '<header class="detail-head detail-head--' + e.trackId + '">' + eventTags(e) +
        '<h1>' + esc(e.title) + '</h1>' +
        '<p class="detail-head__when">' + icon('clock') + esc(d.label) + ' · ' + time(e.start) + '–' + time(e.end) + ' <span class="detail-head__dur">(' + e.durationMinutes + ' min)</span></p>' +
        '<p class="detail-head__where">' + icon('place') + '<a href="scena.html?id=' + v.id + '">' + esc(v.name) + '</a> · ' + esc(v.zone) + '</p>' +
        '<p class="detail-head__action">' + saveButton(e) + '</p>' +
      '</header>' +
      '<p class="lead">' + esc(e.description) + '</p>' +
      '<dl class="meta-list">' +
        '<dt>Scéna</dt><dd><a href="scena.html?id=' + v.id + '">' + esc(v.name) + '</a> – ' + esc(v.kind) + '</dd>' +
        '<dt>Formát</dt><dd>' + esc(TY[e.type].label) + '</dd>' +
        '<dt>Téma</dt><dd><a href="program.html?tema=' + e.trackId + '">' + esc(TR[e.trackId].name) + '</a></dd>' +
        '<dt>Úroveň</dt><dd>' + esc(LV[e.level].label) + '</dd>' +
        '<dt>Jazyk</dt><dd>' + esc(langLabel(e)) + '</dd>' +
        '<dt>Kapacita</dt><dd>' + (e.capacity ? e.capacity + ' míst' : 'podle kapacity scény (' + v.capacity + ')') + '</dd>' +
        '<dt>Rezervace</dt><dd>' + (e.registrationRequired ? 'Nutná – ' + esc(D.practical.workshopRegistration) : 'Není potřeba') + '</dd>' +
      '</dl>' +
      '<section aria-labelledby="kdo"><h2 id="kdo">' + (e.performerIds.length > 1 ? 'Účinkující' : 'Účinkuje') + '</h2>' +
        '<ul class="grid grid--2">' + e.performerIds.map(function (id) { return performerCard(PE[id], 'h3'); }).join('') + '</ul></section>' +
      '<section aria-labelledby="soubezne"><h2 id="soubezne">Současně na jiných scénách</h2>' +
        (parallel.length ? '<ol class="event-rows">' + parallel.map(function (x) { return eventRow(x); }).join('') + '</ol>'
          : '<p>V tomto čase neběží nic dalšího.</p>') + '</section>';
  };

  pages.performers = function () {
    var form = $('#filtry-ucinkujici');
    D.performerTypes.forEach(function (t) {
      form.elements.typ.insertAdjacentHTML('beforeend', '<option value="' + t.id + '">' + esc(t.label) + '</option>');
    });
    D.tracks.forEach(function (t) {
      form.elements.tema.insertAdjacentHTML('beforeend', '<option value="' + t.id + '">' + esc(t.name) + '</option>');
    });
    var p = params();
    ['jmeno', 'typ', 'tema', 'razeni'].forEach(function (f) { if (p.get(f)) form.elements[f].value = p.get(f); });
    var wide = window.matchMedia('(min-width: 900px)');
    var panel = $('#filtry-panel');
    if (wide.matches || p.toString()) panel.open = true;
    function render() {
      var active = ['jmeno', 'typ', 'tema'].filter(function (f) { return form.elements[f].value; }).length;
      $('#pocet-filtru').textContent = active ? ' (' + active + ' ' + pluralCz(active, 'aktivní', 'aktivní', 'aktivních') + ')' : '';
      var q = norm(form.elements.jmeno.value), typ = form.elements.typ.value, tema = form.elements.tema.value,
          razeni = form.elements.razeni.value;
      var list = D.performers.filter(function (x) {
        return (!q || norm(x.name).indexOf(q) !== -1) && (!typ || x.type === typ) && (!tema || x.trackIds.indexOf(tema) !== -1);
      });
      list.sort(function (a, b) {
        if (razeni === 'hvezdy' && a.headliner !== b.headliner) return a.headliner ? -1 : 1;
        var c = a.name.localeCompare(b.name, 'cs');
        return razeni === 'za' ? -c : c;
      });
      $('#pocet').textContent = 'Zobrazeno ' + list.length + ' z ' + D.performers.length + ' účinkujících';
      $('#vypis').innerHTML = list.length ? list.map(function (x) { return performerCard(x, 'h2'); }).join('')
        : '<li class="card empty">Nikdo neodpovídá zadání. Zkuste jiné jméno nebo zrušte filtry.</li>';
      var s = {};
      ['jmeno', 'typ', 'tema', 'razeni'].forEach(function (f) { if (form.elements[f].value) s[f] = form.elements[f].value; });
      if (s.razeni === 'az') delete s.razeni;
      var query = new URLSearchParams(s).toString();
      window.history.replaceState(null, '', 'ucinkujici.html' + (query ? '?' + query : ''));
    }
    form.addEventListener('input', render);
    form.addEventListener('submit', function (ev) { ev.preventDefault(); render(); });
    form.addEventListener('reset', function () { setTimeout(render, 0); });
    render();
  };

  pages.performer = function () {
    var p = PE[params().get('id')];
    var main = $('#obsah');
    if (!p) { notFound(main, 'Účinkující', { href: 'ucinkujici.html', text: 'Zpět na účinkující' }); return; }
    setTitle(p.name);
    setDescription(p.name + ' – ' + p.tagline + '. ' + p.bio);
    crumb(p.name);
    var list = (eventsByPerformer[p.id] || []).slice().sort(byStart);
    $('#detail').innerHTML =
      '<div class="profile"><header class="profile__head"><img class="profile__photo" src="' + esc(p.image.src) + '" alt="' + esc(p.image.alt) + '" width="160" height="160">' +
      '<h1>' + esc(p.name) + '</h1><p class="lead">' + esc(p.tagline) + '</p>' +
      (p.headliner ? '<p><span class="tag tag--headliner">Hlavní hvězda festivalu</span></p>' : '') + '</header><div>' +
      '<dl class="meta-list"><dt>Typ</dt><dd>' + esc(PT[p.type].label) + '</dd><dt>Země</dt><dd>' + esc(D.countries[p.country]) + '</dd>' +
      '<dt>Témata</dt><dd>' + p.trackIds.map(trackTag).join(' ') + '</dd></dl>' +
      '<p>' + esc(p.bio) + '</p></div></div>' +
      '<section aria-labelledby="vystoupeni"><h2 id="vystoupeni">Vystoupení na festivalu (' + list.length + ')</h2>' +
      '<ol class="event-list">' + list.map(function (e) { return eventCard(e, { heading: 'h3', showDay: true }); }).join('') + '</ol></section>' +
      '<p><a class="back-link" href="ucinkujici.html">← Všichni účinkující</a></p>';
  };

  pages.venues = function () {
    var f = D.festival;
    $('#mapa').innerHTML = '<img class="map" src="' + esc(f.areaMap.src) + '" alt="' + esc(f.areaMap.alt) + '" width="800" height="560">';
    $('#sceny').innerHTML = D.venues.map(function (v) {
      var nn = nowAndNext(v.id);
      var cur = nn.now ? 'Právě teď: <a href="udalost.html?id=' + nn.now.id + '">' + esc(nn.now.title) + '</a>'
        : (nn.next ? 'Další: ' + esc(DA[nn.next.dayId].label) + ' ' + time(nn.next.start) + ' <a href="udalost.html?id=' + nn.next.id + '">' + esc(nn.next.title) + '</a>' : '');
      return '<li class="card venue-card"><img src="' + esc(v.image.src) + '" alt="" width="800" height="450" loading="lazy">' +
        '<h2><a href="scena.html?id=' + v.id + '">' + esc(v.name) + '</a></h2>' +
        '<p>' + esc(v.kind) + ' · ' + esc(v.zone) + ' · kapacita ' + v.capacity + '</p>' +
        '<p>' + esc(v.focus.join(', ')) + '</p><p>' + cur + '</p></li>';
    }).join('');
  };

  pages.venue = function () {
    var v = VE[params().get('id')];
    var main = $('#obsah');
    if (!v) { notFound(main, 'Scéna', { href: 'sceny.html', text: 'Zpět na scény' }); return; }
    setTitle(v.name);
    setDescription(v.name + ' – ' + v.kind + '. ' + v.description);
    crumb(v.name);
    var list = D.events.filter(function (e) { return e.venueId === v.id; }).sort(byStart);
    $('#detail').innerHTML =
      '<h1>' + esc(v.name) + '</h1><p class="lead">' + esc(v.kind) + ' · ' + esc(v.zone) + '</p>' +
      '<img class="venue-hero" src="' + esc(v.image.src) + '" alt="' + esc(v.image.alt) + '" width="800" height="450">' +
      '<p>' + esc(v.description) + '</p>' +
      '<dl class="meta-list"><dt>Kapacita</dt><dd>' + v.capacity + ' osob</dd><dt>Prostor</dt><dd>' + (v.indoor ? 'krytý' : 'venkovní') + '</dd>' +
      '<dt>Zaměření</dt><dd>' + esc(v.focus.join(', ')) + '</dd><dt>Vybavení</dt><dd>' + esc(v.facilities.join(', ')) + '</dd></dl>' +
      '<section aria-labelledby="pristupnost"><h2 id="pristupnost">Přístupnost</h2>' + iconList([
        { icon: 'accessible', title: 'Bezbariérový přístup', text: v.accessibility.wheelchair ? 'Ano' : 'Ne' },
        { icon: 'info', title: 'Indukční smyčka', text: v.accessibility.hearingLoop ? 'Ano' : 'Ne' },
        { icon: 'check', text: v.accessibility.note }]) + '</section>' +
      '<section aria-labelledby="program-sceny"><h2 id="program-sceny">Program scény (' + list.length + ')</h2>' +
        groupByDay(list, function (e) { return eventCard(e); }) + '</section>';
  };

  // Upozornění na časové kolize ve třech variantách (ui alert: panel | strip | inline)
  function overlapText(pr) {
    var from = ms(pr[0].start) > ms(pr[1].start) ? pr[0].start : pr[1].start;
    var to = ms(pr[0].end) < ms(pr[1].end) ? pr[0].end : pr[1].end;
    return { from: from, to: to, minutes: Math.round((ms(to) - ms(from)) / 60000) };
  }
  function conflictAlert(pairs) {
    if (!pairs.length) return '';
    var title = pairs.length + ' ' + pluralCz(pairs.length, 'časová kolize', 'časové kolize', 'časových kolizí');
    var items = pairs.map(function (pr) {
      var o = overlapText(pr);
      return '<li class="clash"><span class="clash__time">' + esc(DA[pr[0].dayId].weekday.slice(0, 2)) + ' ' + time(o.from) + '–' + time(o.to) +
        ' <span class="clash__len">(' + o.minutes + ' min)</span></span>' +
        '<a href="udalost.html?id=' + pr[0].id + '">' + esc(pr[0].title) + '</a><span class="clash__vs">kryje se s</span>' +
        '<a href="udalost.html?id=' + pr[1].id + '">' + esc(pr[1].title) + '</a></li>';
    }).join('');
    var advice = 'Jednu z položek odeberte, nebo počítejte s přesunem mezi scénami.';
    if (UI.alert === 'strip') {
      return '<details class="notice conflict-strip" role="alert"><summary>' + icon('warning') + '<span>' + title + '</span><span class="conflict-strip__more">Zobrazit</span></summary>' +
        '<ul class="clashes">' + items + '</ul><p>' + advice + '</p></details>';
    }
    if (UI.alert === 'inline') {
      return '<p class="notice conflict-line" role="alert">' + icon('warning') + '<span><strong>' + title + '.</strong> Kolidující položky jsou níže označené červeně.' +
        '<span class="visually-hidden"> ' + pairs.map(function (pr) { return pr[0].title + ' a ' + pr[1].title; }).join('; ') + '.</span></span></p>';
    }
    return '<section class="notice conflict-panel" role="alert" aria-labelledby="kolize-nadpis"><div class="conflict-panel__head">' +
      '<span class="conflict-panel__icon">' + icon('warning') + '</span><div><h2 id="kolize-nadpis">' + title + '</h2><p>' + advice + '</p></div></div>' +
      '<ul class="clashes">' + items + '</ul></section>';
  }

  pages.my = function () {
    var box = $('#muj');
    function render() {
      var list = saved().map(function (id) { return EV[id]; }).sort(byStart);
      if (!list.length) {
        box.innerHTML = '<div class="card empty"><span class="empty__icon">' + icon('star') + '</span><h2>Zatím tu nic není</h2>' +
          '<p>V programu si položky uložíte tlačítkem „' + (UI.save === 'star' ? 'Uložit' : 'Do Mého programu') + '“. Uvidíte je tu podle dnů a upozorníme vás, když se dvě kryjí.</p>' +
          '<p><a class="button" href="program.html">Přejít na program</a></p></div>';
        return;
      }
      var pairs = conflictsOf(list);
      var inConflict = {}, clashWith = {};
      pairs.forEach(function (pr) {
        inConflict[pr[0].id] = inConflict[pr[1].id] = true;
        (clashWith[pr[0].id] = clashWith[pr[0].id] || []).push(pr[1]);
        (clashWith[pr[1].id] = clashWith[pr[1].id] || []).push(pr[0]);
      });
      box.innerHTML = '<p data-my-count-label></p>' + conflictAlert(pairs) +
        groupByDay(list, function (e) { return eventCard(e, { conflict: inConflict[e.id], clashWith: clashWith[e.id] }); }) +
        '<p><button type="button" class="button button--ghost" id="smazat-vse">Odebrat vše</button></p>';
      updateBadge();
      $('#smazat-vse').addEventListener('click', function () {
        if (window.confirm('Opravdu odebrat všechny položky z Mého programu?')) { setSaved([]); render(); announce('Můj program je prázdný.'); }
      });
    }
    document.addEventListener('tranzistor:saved', render);
    render();
  };

  pages.practical = function () {
    var P = D.practical;
    $('#vstupenky-obsah').innerHTML = '<div class="table-wrap"><table class="data-table tickets"><caption class="visually-hidden">Ceny vstupenek</caption>' +
      '<thead><tr><th scope="col">Vstupenka</th><th scope="col">Cena</th><th scope="col">Platí</th><th scope="col">Popis</th></tr></thead><tbody>' +
      P.tickets.map(function (t) {
        var valid = t.validDayIds.map(function (id) { return DA[id].weekday.slice(0, 2); }).join(' · ');
        return '<tr><th scope="row">' + esc(t.name) + '</th><td data-label="Cena" class="price">' + (t.priceCzk ? t.priceCzk.toLocaleString('cs-CZ') + ' Kč' : 'zdarma') +
          '</td><td data-label="Platí">' + esc(valid) + '</td><td class="ticket-desc">' + esc(t.description) + '</td></tr>';
      }).join('') + '</tbody></table></div>' +
      '<p>' + esc(P.workshopRegistration) + '</p>' +
      '<p><a class="button button--accent" href="' + esc(D.festival.ticketShopUrl) + '">Koupit vstupenky</a></p>';
    $('#doprava-obsah').innerHTML = '<address>' + esc(D.festival.location.name) + '<br>' + esc(D.festival.location.streetAddress) +
      '<br>' + esc(D.festival.location.postalCode) + ' ' + esc(D.festival.location.city) + '</address>' +
      iconList(P.transport.map(function (t) {
        return { icon: { 'Kolo': 'bike', 'Auto': 'car' }[t.mode] || 'train', title: t.mode, text: t.description };
      }));
    $('#pristupnost-obsah').innerHTML = iconList(P.accessibility.map(function (a) { return { icon: 'accessible', text: a }; })) +
      '<p>Přístupnost jednotlivých scén najdete na stránce <a href="sceny.html">Scény</a>.</p>';
    var SERVICE_ICONS = ['restaurant', 'water', 'card', 'bag', 'hospital', 'face', 'wifi'];
    $('#sluzby-obsah').innerHTML = iconList(P.services.map(function (s, i) { return { icon: SERVICE_ICONS[i] || 'info', title: s.name, text: s.description }; }));
    $('#pravidla-obsah').innerHTML = iconList(P.rules.map(function (r) { return { icon: 'info', text: r }; }));
    $('#caste-dotazy-obsah').innerHTML = P.faq.map(function (f) {
      return '<details class="disclosure faq-item"><summary><span class="disclosure__label">' + esc(f.question) + '</span>' + disclosureIcon() + '</summary>' +
        '<div class="disclosure__body"><p>' + esc(f.answer) + '</p></div></details>';
    }).join('');

    // zvýraznění sekce, ve které se čtenář nachází (navigace po stránce)
    var links = $$('.page-nav a');
    if (links.length && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          links.forEach(function (a) {
            if (a.getAttribute('href') === '#' + en.target.id) {
              a.setAttribute('aria-current', 'location');
              var row = a.closest('ul');
              if (row && row.scrollWidth > row.clientWidth) row.scrollTo({ left: a.parentNode.offsetLeft - 16, behavior: 'smooth' });
            } else a.removeAttribute('aria-current');
          });
        });
      }, { rootMargin: '-35% 0px -60% 0px' });
      links.forEach(function (a) { var s = $(a.getAttribute('href')); if (s) io.observe(s); });
    }
  };

  pages.search = function () {
    var q = params().get('q') || '';
    var input = $('#hledat');
    if (input) input.value = q;
    var nq = norm(q);
    var out = $('#vysledky');
    if (!nq) { out.innerHTML = '<p>Zadejte hledaný výraz do pole v záhlaví, například <a href="hledani.html?q=malatova">malatova</a>.</p>'; return; }
    setTitle('Hledání: ' + q);
    function hits(text) { return norm(text).indexOf(nq) !== -1; }
    function mark(text) {
      var n = norm(text), i = n.indexOf(nq);
      if (i === -1) return esc(text);
      // normalizace NFD + odstranění diakritiky zachovává délku řetězce pro běžné české znaky
      return esc(text.slice(0, i)) + '<mark>' + esc(text.slice(i, i + nq.length)) + '</mark>' + esc(text.slice(i + nq.length));
    }
    var people = D.performers.filter(function (p) { return hits(p.name) || hits(p.tagline) || hits(p.bio); })
      .sort(function (a, b) { return (hits(b.name) - hits(a.name)) || a.name.localeCompare(b.name, 'cs'); });
    var events = D.events.filter(function (e) {
      return hits(e.title) || hits(e.description) || hits(e.tags.join(' ')) || hits(names(e.performerIds));
    }).sort(function (a, b) { return (hits(b.title) - hits(a.title)) || byStart(a, b); });
    var venues = D.venues.filter(function (v) { return hits(v.name) || hits(v.kind) || hits(v.description); });
    var total = people.length + events.length + venues.length;
    var html = '<p role="status" class="result-count">Pro „' + esc(q) + '“ ' + pluralCz(total, 'nalezen', 'nalezeny', 'nalezeno') + ' ' +
      total + ' ' + pluralCz(total, 'výsledek', 'výsledky', 'výsledků') + '.</p>';
    if (!total) {
      html += '<div class="card empty"><p>Nic jsme nenašli. Zkontrolujte překlep, zkuste kratší slovo nebo projděte <a href="program.html">celý program</a>.</p></div>';
    }
    function group(title, id, list, render) {
      if (!list.length) return '';
      return '<section class="results-group" aria-labelledby="' + id + '"><h2 id="' + id + '">' + title + ' <small>(' + list.length + ')</small></h2>' +
        '<ul class="results-list">' + list.map(render).join('') + '</ul></section>';
    }
    html += group('Účinkující', 'vysledky-ucinkujici', people, function (p) {
      return '<li class="card"><a href="ucinkujici-detail.html?id=' + p.id + '">' + mark(p.name) + '</a><p>' + mark(p.tagline) + '</p></li>';
    });
    html += group('Program', 'vysledky-program', events, function (e) {
      return '<li class="card"><a href="udalost.html?id=' + e.id + '">' + mark(e.title) + '</a><p>' + esc(DA[e.dayId].label) + ' ' +
        time(e.start) + ' · ' + esc(VE[e.venueId].name) + ' · ' + mark(names(e.performerIds)) + '</p></li>';
    });
    html += group('Scény', 'vysledky-sceny', venues, function (v) {
      return '<li class="card"><a href="scena.html?id=' + v.id + '">' + mark(v.name) + '</a><p>' + esc(v.kind) + '</p></li>';
    });
    out.innerHTML = html;
  };

  pages.about = function () {
    var f = D.festival;
    $('#o-festivalu-obsah').innerHTML =
      '<p class="lead">' + esc(f.description) + '</p><p>' + esc(f.character) + '</p>' +
      '<h2>Témata</h2><ul class="track-chips">' + D.tracks.map(trackChip).join('') + '</ul>' +
      '<h2>Historie ročníků</h2><div class="table-wrap"><table class="data-table"><caption class="visually-hidden">Přehled ročníků festivalu</caption>' +
      '<thead><tr><th scope="col">Ročník</th><th scope="col">Termín</th><th scope="col">Návštěvnost</th><th scope="col">Scény</th><th scope="col">Shrnutí</th></tr></thead><tbody>' +
      f.history.map(function (h) {
        return '<tr><th scope="row">' + h.edition + '. ročník (' + h.year + ')</th><td data-label="Termín">' + dateCz(h.startDate) + ' – ' + dateCz(h.endDate) + '</td><td data-label="Návštěvnost">' +
          h.attendance.toLocaleString('cs-CZ') + '</td><td data-label="Scény">' + h.venueCount + '</td><td class="data-table__wide">' + esc(h.summary) + '</td></tr>';
      }).join('') +
      '<tr><th scope="row">' + f.edition + '. ročník (' + f.year + ')</th><td data-label="Termín">' + dateCz(f.startDate) + ' – ' + dateCz(f.endDate) +
      '</td><td data-label="Návštěvnost">očekáváme ' + f.expectedAttendance.toLocaleString('cs-CZ') + '</td><td data-label="Scény">' + D.venues.length + '</td><td class="data-table__wide">Letošní ročník.</td></tr>' +
      '</tbody></table></div>' +
      '<h2>Pořadatel a kontakt</h2><address class="card">' + esc(f.organizer.name) + '<br>' +
      'Obecné dotazy: <a href="mailto:' + esc(f.organizer.email) + '">' + esc(f.organizer.email) + '</a><br>' +
      'Média: <a href="mailto:' + esc(f.organizer.pressEmail) + '">' + esc(f.organizer.pressEmail) + '</a></address>';
  };

  // ---------------------------------------------------------------- společné chování
  function initHeader() {
    document.documentElement.classList.add('js');
    var toggle = $('.menu-toggle'), nav = $('#hlavni-menu');
    if (toggle && nav) {
      toggle.addEventListener('click', function () {
        var open = toggle.getAttribute('aria-expanded') !== 'true';
        toggle.setAttribute('aria-expanded', String(open));
        nav.classList.toggle('is-open', open);
      });
    }
    // spodní lišta pro variantu nav:bottom vzniká z hlavní navigace, aby odkazy byly na jednom místě
    if (nav) {
      var current = $('a[aria-current="page"]', nav);
      var bar = document.createElement('nav');
      bar.className = 'tab-bar';
      bar.setAttribute('aria-label', 'Rychlá navigace');
      var items = [['index.html', 'Úvod', 'home'], ['program.html', 'Program', 'program'], ['ucinkujici.html', 'Účinkující', 'people'],
        ['sceny.html', 'Scény', 'place'], ['muj-program.html', 'Můj plán', 'star']];
      bar.innerHTML = '<ul>' + items.map(function (it) {
        var here = (current && current.getAttribute('href') === it[0]) || (it[0] === 'index.html' && document.body.dataset.page === 'home');
        var badge = it[0] === 'muj-program.html' ? '<span class="badge badge--corner" aria-hidden="true" data-my-count data-count="0">0</span>' : '';
        return '<li><a href="' + it[0] + '"' + (here ? ' aria-current="page"' : '') + '><span class="tab-bar__icon">' + icon(it[2]) + badge + '</span>' +
          '<span class="tab-bar__label">' + it[1] + '</span>' + (badge ? '<span class="visually-hidden" data-my-count-sr></span>' : '') + '</a></li>';
      }).join('') + '</ul>';
      document.body.appendChild(bar);
    }
    $$('[data-icon]').forEach(function (el) { el.insertAdjacentHTML('afterbegin', icon(el.getAttribute('data-icon'))); });
    var toast = document.createElement('div');
    toast.id = 'toast';
    toast.className = 'toast';
    toast.setAttribute('role', 'status');
    document.body.appendChild(toast);

    document.addEventListener('click', function (ev) {
      var u = ev.target.closest('[data-undo]');
      if (u) {
        var ue = EV[u.getAttribute('data-undo')];
        var back = toggleSaved(ue.id);
        $$('[data-save="' + ue.id + '"]').forEach(function (btn) { btn.outerHTML = saveButton(ue); });
        announce((back ? 'Vráceno do Mého programu: ' : 'Odebráno z Mého programu: ') + ue.title);
        document.dispatchEvent(new CustomEvent('tranzistor:saved'));
        return;
      }
      var b = ev.target.closest('[data-save]');
      if (!b) return;
      var e = EV[b.getAttribute('data-save')];
      var added = toggleSaved(e.id);
      $$('[data-save="' + e.id + '"]').forEach(function (btn) { btn.outerHTML = saveButton(e); });
      var again = $('[data-save="' + e.id + '"]');
      if (again && document.body.dataset.page !== 'my') again.focus();
      announce((added ? 'Přidáno do Mého programu: ' : 'Odebráno z Mého programu: ') + e.title, e.id);
      document.dispatchEvent(new CustomEvent('tranzistor:saved'));
    });
    updateBadge();
    simBar();
  }

  if (!D) {
    document.body.insertAdjacentHTML('afterbegin', '<p class="notice">Data festivalu se nepodařilo načíst. Zkuste stránku obnovit.</p>');
    return;
  }
  initHeader();
  var page = pages[document.body.dataset.page];
  if (page) page();
})();
