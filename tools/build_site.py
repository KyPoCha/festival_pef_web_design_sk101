#!/usr/bin/env python3
"""Vygeneruje všechny stránky webu (složka web/) jako hotové HTML z data.json.

Použití:  python3 tools/build_site.py

Proč předgenerované stránky: obsah je v HTML hned, takže ho vidí validátor W3C, WAVE,
vyhledávače i AI agenti a web funguje i bez JavaScriptu. JavaScript (web/js/app.js) jen
přidává interaktivitu. Ke spuštění webu nic z toho není potřeba – stránky se jen otevřou.

Skript zapisuje: všechny stránky *.html, program/*.html, ucinkujici/*.html, sceny/*.html,
js/data.js, images/ (ilustrace přes tools/generate_images.py), sitemap.xml, robots.txt, llms.txt.
Ručně udržované zůstávají: css/style.css, js/app.js, fonts/, images/og/, images/favicon.svg.
Používá jen standardní knihovnu Pythonu.
"""
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
SITE = "https://tranzistor-festival.cz/"
D = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))

EV = {e["id"]: e for e in D["events"]}
PE = {p["id"]: p for p in D["performers"]}
VE = {v["id"]: v for v in D["venues"]}
TR = {t["id"]: t for t in D["tracks"]}
DA = {d["id"]: d for d in D["days"]}
TY = {t["id"]: t for t in D["eventTypes"]}
PT = {t["id"]: t for t in D["performerTypes"]}
LV = {t["id"]: t for t in D["levels"]}
LA = {t["id"]: t for t in D["languages"]}
F = D["festival"]
EVENTS_BY_PERFORMER = {}
for _e in sorted(D["events"], key=lambda e: e["start"]):
    for _pid in _e["performerIds"]:
        EVENTS_BY_PERFORMER.setdefault(_pid, []).append(_e)

# Ikony – stejné tvary jako ve skriptu webu (jedno místo pravdy: web/js/app.js)
_icons_js = re.search(r"var ICONS = \{(.*?)\n  \};", (WEB / "js" / "app.js").read_text(encoding="utf-8"), re.S).group(1)
ICONS = dict(re.findall(r"(\w+): '([^']+)'", _icons_js))


def icon(name, cls=""):
    c = f"icon {cls}".strip()
    return (f'<svg class="{c}" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false">'
            f'<path d="{ICONS[name]}"/></svg>')


def h(text):
    return escape(str(text), {'"': "&quot;"})


def norm(text):
    return "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c)).lower()


def plural(n, one, few, many):
    return one if n == 1 else (few if 2 <= n <= 4 else many)


def hm(iso):
    return iso[11:16]


def t(iso):
    return f'<time datetime="{iso}">{hm(iso)}</time>'


def date_cz(iso):
    y, m, d = iso[:10].split("-")
    return f'<time datetime="{iso[:10]}">{int(d)}. {int(m)}. {y}</time>'


# ---------------------------------------------------------------- adresy stránek
def event_path(e): return f"program/{e['slug']}.html"
def performer_path(p): return f"ucinkujici/{p['slug']}.html"
def venue_path(v): return f"sceny/{v['slug']}.html"


class Page:
    def __init__(self, path):
        self.path = path
        self.root = "../" * path.count("/")

    def url(self, target):
        return self.root + target


# ---------------------------------------------------------------- společné části
NAV = [("program.html", "Program", ("program", "event")), ("ucinkujici.html", "Účinkující", ("performers", "performer")),
       ("sceny.html", "Scény", ("venues", "venue")), ("prakticke-informace.html", "Praktické informace", ("practical",)),
       ("o-festivalu.html", "O festivalu", ("about",))]
TABS = [("index.html", "Úvod", "home", ("home",)), ("program.html", "Program", "program", ("program", "event")),
        ("ucinkujici.html", "Účinkující", "people", ("performers", "performer")), ("sceny.html", "Scény", "place", ("venues", "venue")),
        ("muj-program.html", "Můj plán", "star", ("my",))]


def header(pg, key):
    cur = ' aria-current="page"'
    links = "".join(f'<li><a href="{pg.url(href)}"{cur if key in keys else ""}>{label}</a></li>' for href, label, keys in NAV)
    return f'''<a class="skip-link" href="#obsah">Přeskočit na obsah</a>
<header class="site-header">
  <div class="site-header__bar container">
    <a class="logo" href="{pg.url("index.html")}"><span class="logo__mark" aria-hidden="true"></span>Tranzistor <span class="logo__year">2027</span></a>
    <a class="my-link" href="{pg.url("muj-program.html")}"{cur if key == "my" else ""}><span class="my-link__icon">{icon("star")}</span><span class="my-link__text">Můj program</span> <span class="badge" aria-hidden="true" data-my-count data-count="0">0</span><span class="visually-hidden" data-my-count-sr></span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="hlavni-menu">{icon("menu")}<span class="menu-toggle__text">Menu</span></button>
    <form class="search" action="{pg.url("hledani.html")}" method="get" role="search">
      <label for="hledat" class="visually-hidden">Hledat na webu</label>
      <input id="hledat" name="q" type="search" placeholder="Hledat účinkující, program, scény…" autocomplete="off">
      <button type="submit">{icon("search")}<span class="search__text">Hledat</span></button>
    </form>
  </div>
  <nav id="hlavni-menu" class="main-nav" aria-label="Hlavní navigace"><ul class="container">{links}</ul></nav>
</header>'''


def tab_bar(pg, key):
    items = []
    for href, label, ic, keys in TABS:
        badge = ('<span class="badge badge--corner" aria-hidden="true" data-my-count data-count="0">0</span>' if ic == "star" else "")
        sr = '<span class="visually-hidden" data-my-count-sr></span>' if ic == "star" else ""
        current = ' aria-current="page"' if key in keys else ""
        items.append(f'<li><a href="{pg.url(href)}"{current}><span class="tab-bar__icon">{icon(ic)}{badge}</span>'
                     f'<span class="tab-bar__label">{label}</span>{sr}</a></li>')
    return f'<nav class="tab-bar" aria-label="Rychlá navigace"><ul>{"".join(items)}</ul></nav>'


def footer(pg):
    # oddělovač tisíců v češtině je (nezlomitelná) mezera
    loc = F["location"]
    price = {t["id"]: f'{t["priceCzk"]:,}'.replace(",", " ") for t in D["practical"]["tickets"]}
    return f'''<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-block">
      <h2 class="h-small">Tranzistor 2027</h2>
      <p><time datetime="{F["startDate"]}">4.</time>–<time datetime="{F["endDate"]}">6. června 2027</time></p>
      <address>{h(loc["name"])}<br>{h(loc["streetAddress"])}<br>{h(loc["postalCode"])} {h(loc["city"])}<br>
        <a href="mailto:{F["organizer"]["email"]}">{F["organizer"]["email"]}</a></address>
    </div>
    <nav aria-labelledby="pata-odkazy">
      <h2 id="pata-odkazy" class="h-small">Rychlé odkazy</h2>
      <ul>
        <li><a href="{pg.url("o-festivalu.html")}">O festivalu</a></li>
        <li><a href="{pg.url("prakticke-informace.html#vstupenky")}">Vstupenky</a></li>
        <li><a href="{pg.url("prakticke-informace.html#pristupnost")}">Přístupnost</a></li>
        <li><a href="{pg.url("prakticke-informace.html#caste-dotazy")}">Časté dotazy</a></li>
      </ul>
    </nav>
    <div class="footer-block">
      <h2 class="h-small">Vstupenky</h2>
      <p class="note">Třídenní vstupenka {price["tk01"]} Kč, studenti {price["tk02"]} Kč, děti do 12 let zdarma.</p>
      <p><a class="button button--accent button--small" href="{pg.url("prakticke-informace.html#vstupenky")}">Vybrat vstupenku</a></p>
    </div>
  </div>
</footer>'''


def breadcrumbs(pg, items):
    """items = [(href nebo None, text)]; poslední položka je aktuální stránka."""
    lis = "".join(f'<li><a href="{pg.url(href)}">{h(text)}</a></li>' for href, text in items[:-1])
    return (f'<nav class="breadcrumbs container" aria-label="Drobečková navigace"><ol>{lis}'
            f'<li aria-current="page">{h(items[-1][1])}</li></ol></nav>')


def breadcrumb_ld(pg, items):
    out = []
    for i, (href, text) in enumerate(items, 1):
        target = pg.path if href is None else href
        out.append({"@type": "ListItem", "position": i, "name": text, "item": SITE + ("" if target == "index.html" else target)})
    return {"@type": "BreadcrumbList", "itemListElement": out}


def festival_ref():
    return {"@type": "Festival", "@id": SITE + "#festival", "name": F["fullName"], "url": SITE}


def place_ld():
    loc = F["location"]
    return {"@type": "Place", "name": loc["name"],
            "address": {"@type": "PostalAddress", "streetAddress": loc["streetAddress"], "postalCode": loc["postalCode"],
                        "addressLocality": loc["city"], "addressCountry": loc["country"]}}


def performer_ld(p):
    kind = {"musician": "MusicGroup", "team": "SportsTeam", "collective": "PerformingGroup"}.get(p["type"], "Person")
    return {"@type": kind, "name": p["name"], "url": SITE + performer_path(p)}


def write_page(pg, *, key, title, description, main, crumbs=None, ld=None, og_type="website", main_class="container"):
    graph = list(ld or [])
    if crumbs:
        graph.append(breadcrumb_ld(pg, crumbs))
    jsonld = ""
    if graph:
        jsonld = ('<script type="application/ld+json">' +
                  json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/") + "</script>\n")
    canonical = SITE + ("" if pg.path == "index.html" else pg.path)
    html = f'''<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add('js')</script>
<title>{h(title)}</title>
<meta name="description" content="{h(description)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0b0e17">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Tranzistor 2027">
<meta property="og:locale" content="cs_CZ">
<meta property="og:title" content="{h(title)}">
<meta property="og:description" content="{h(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}images/og/tranzistor.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Tranzistor 2027 – festival technologií, her a digitální kultury, 4.–6. června 2027, Pražská tržnice">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pg.url("images/favicon.svg")}" type="image/svg+xml">
<link rel="stylesheet" href="{pg.url("css/style.css")}">
{jsonld}</head>
<body data-page="{key}" data-root="{pg.root}">
{header(pg, key)}
{breadcrumbs(pg, crumbs) if crumbs else ""}<main id="obsah" class="{main_class}">
{main}
</main>
{footer(pg)}
{tab_bar(pg, key)}
<div id="toast" class="toast" role="status" aria-live="polite"></div>
<script src="{pg.url("js/data.js")}"></script>
<script src="{pg.url("js/app.js")}"></script>
</body>
</html>
'''
    target = WEB / pg.path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    PAGES.append((pg.path, title))


PAGES = []
NOSCRIPT = '<noscript><p class="notice">Tato část stránky potřebuje zapnutý JavaScript.</p></noscript>'


# ---------------------------------------------------------------- komponenty
def save_button(e):
    return (f'<button type="button" class="save" data-save="{e["id"]}" aria-pressed="false">{icon("add")}'
            f'<span class="save__text">Do Mého programu</span><span class="visually-hidden">: {h(e["title"])}</span></button>')


def event_tags(e):
    tags = [f'<span class="tag tag--track tag--{e["trackId"]}">{h(TR[e["trackId"]]["name"])}</span>', f'<span class="tag">{h(TY[e["type"]]["label"])}</span>']
    if e["familyFriendly"]:
        tags.append('<span class="tag tag--family">Pro rodiny</span>')
    if e["registrationRequired"]:
        tags.append('<span class="tag tag--reg">Nutná rezervace</span>')
    return '<p class="tags">' + " ".join(tags) + "</p>"


def performer_names(e):
    return ", ".join(PE[i]["name"] for i in e["performerIds"])


def event_card(pg, e, heading="h4", show_day=False, data=False):
    attrs = ""
    if data:
        attrs = (f' data-den="{e["dayId"]}" data-scena="{e["venueId"]}" data-tema="{e["trackId"]}" data-format="{e["type"]}"'
                 f' data-uroven="{e["level"]}" data-jazyk="{e["language"] or "zadny"}" data-rodiny="{1 if e["familyFriendly"] else 0}"')
    day = h(DA[e["dayId"]]["label"]) + " · " if show_day else ""
    return (f'<li{attrs}><article class="card event-card event-card--{e["trackId"]}">'
            f'<p class="event-card__time">{icon("clock", "icon--time")}{t(e["start"])}<span>do {t(e["end"])}</span></p>'
            f'<div class="event-card__body"><{heading}><a href="{pg.url(event_path(e))}">{h(e["title"])}</a></{heading}>'
            f'<p class="event-card__where">{icon("place", "icon--inline")}{day}{h(VE[e["venueId"]]["name"])} · {h(performer_names(e))}</p>'
            f'{event_tags(e)}</div><div class="event-card__actions">{save_button(e)}</div></article></li>')


def event_row(pg, e, show_day=False):
    day = h(DA[e["dayId"]]["weekday"][:2]) + " " if show_day else ""
    return (f'<li><a class="event-row event-row--{e["trackId"]}" href="{pg.url(event_path(e))}"><span class="event-row__time">{day}{t(e["start"])}</span>'
            f'<span class="event-row__title">{h(e["title"])}</span><span class="event-row__where">{h(VE[e["venueId"]]["name"])} · {h(TY[e["type"]]["label"])}</span></a></li>')


def day_groups(pg, events, card):
    out = []
    for d in D["days"]:
        items = [e for e in events if e["dayId"] == d["id"]]
        if items:
            out.append(f'<section class="day-group" aria-labelledby="den-{d["id"]}"><h3 id="den-{d["id"]}">{h(d["label"])} <small>· {h(d["theme"])}</small></h3>'
                       f'<ol class="event-list">{"".join(card(e) for e in items)}</ol></section>')
    return "".join(out)


def performer_card(pg, p, heading="h3", data=False):
    attrs = ""
    if data:
        attrs = (f' data-jmeno="{h(norm(p["name"]))}" data-typ="{p["type"]}" data-temata="{" ".join(p["trackIds"])}"'
                 f' data-hvezda="{1 if p["headliner"] else 0}" data-razeni="{h(p["name"])}"')
    star = '<span class="tag tag--headliner person-card__star">Hvězda</span>' if p["headliner"] else ""
    return (f'<li class="card person-card"{attrs}><img src="{pg.url(p["image"]["src"])}" alt="" width="56" height="56" loading="lazy">'
            f'<div class="person-card__text"><{heading}><a href="{pg.url(performer_path(p))}">{h(p["name"])}</a></{heading}>'
            f'<p class="person-card__tagline">{h(p["tagline"])}</p><p class="person-card__meta">{h(PT[p["type"]]["label"])} · {h(D["countries"][p["country"]])}</p></div>{star}</li>')


def track_chip(pg, tr):
    n = sum(1 for e in D["events"] if e["trackId"] == tr["id"])
    return (f'<li><a class="track-chip track-chip--{tr["id"]}" href="{pg.url("program.html?tema=" + tr["id"])}">'
            f'<span class="track-chip__name">{h(tr["name"])}</span><span class="track-chip__count">{n}</span></a></li>')


def icon_list(items):
    out = []
    for ic, title, text in items:
        out.append(f'<li class="icon-list__item"><span class="icon-list__icon">{icon(ic)}</span><div>'
                   + (f'<h3 class="icon-list__title">{h(title)}</h3>' if title else "") + f"<p>{h(text)}</p></div></li>")
    return '<ul class="icon-list">' + "".join(out) + "</ul>"


def disclosure_icon():
    return f'<span class="disclosure__icon">{icon("expand", "disclosure__chevron")}</span>'


def sorted_events(events):
    order = {v["id"]: i for i, v in enumerate(D["venues"])}
    return sorted(events, key=lambda e: (e["start"], order[e["venueId"]]))


# ---------------------------------------------------------------- stránky
def build_home():
    pg = Page("index.html")
    stars = "".join(f'<li class="star-tile"><a href="{pg.url(performer_path(p))}"><img src="{pg.url(p["image"]["src"])}" alt="" width="112" height="112" loading="lazy">'
                    f'<span class="star-tile__name">{h(p["name"])}</span><span class="star-tile__tagline">{h(p["tagline"])}</span></a></li>'
                    for p in D["performers"] if p["headliner"])
    first_day = D["days"][0]
    first = sorted_events([e for e in D["events"] if e["dayId"] == first_day["id"]])[:4]
    days = "".join(f'<li><a class="day-card card" href="{pg.url("program.html?den=" + d["id"])}"><span class="day-card__date">{h(d["label"])}</span>'
                   f'<span class="day-card__theme">{h(d["theme"])}</span><span class="day-card__meta">{d["opens"]}–{d["closes"]} · '
                   f'{sum(1 for e in D["events"] if e["dayId"] == d["id"])} {plural(sum(1 for e in D["events"] if e["dayId"] == d["id"]), "položka", "položky", "položek")}</span></a></li>'
                   for d in D["days"])
    main = f'''<section class="hero full-bleed" aria-labelledby="nazev">
  <div class="hero__circuit" aria-hidden="true"></div>
  <div class="hero__inner container">
    <p class="hero__pill"><time datetime="{F["startDate"]}">4.</time>–<time datetime="{F["endDate"]}">6. 6. 2027</time> · Pražská tržnice, Praha 7</p>
    <h1 id="nazev">Tranzistor <span>2027</span></h1>
    <p class="hero__slogan">{h(F["slogan"])}</p>
    <p class="hero__facts">Festival technologií, her a digitální kultury</p>
    <ul class="hero__stats">
      <li><strong>{len(D["days"])}</strong> dny</li>
      <li><strong>{len(D["venues"])}</strong> scén</li>
      <li><strong>{len(D["events"])}</strong> položek programu</li>
    </ul>
    <p class="hero__actions"><a class="button button--accent" href="program.html">Prohlédnout program</a>
      <a class="button button--ghost" href="prakticke-informace.html#vstupenky">Vstupenky</a></p>
  </div>
</section>
<section class="section" aria-labelledby="ted-nadpis">
  <h2 id="ted-nadpis">Právě teď</h2>
  <div id="prave-ted">
    <div class="countdown card"><p class="countdown__label">Zahájení</p>
      <p class="countdown__value">{h(first_day["weekday"])} <time datetime="{first_day["date"]}T{first_day["opens"]}">4. 6. ve {first_day["opens"]}</time></p>
      <p>Během festivalu tu uvidíte, co na které scéně právě běží – <a href="?cas=2027-06-05T19:45">podívejte se, jak vypadá sobotní večer</a>.</p></div>
    <h3 class="subhead">Na úvod festivalu</h3>
    <ol class="event-rows">{"".join(event_row(pg, e, True) for e in first)}</ol>
  </div>
</section>
<section class="section" aria-labelledby="hvezdy-nadpis">
  <h2 id="hvezdy-nadpis">Hlavní hvězdy</h2>
  <ul class="star-strip">{stars}</ul>
  <p><a class="more-link" href="ucinkujici.html">Všech {len(D["performers"])} účinkujících →</a></p>
</section>
<section class="section" aria-labelledby="temata-nadpis">
  <h2 id="temata-nadpis">Vyberte si téma</h2>
  <ul class="track-chips">{"".join(track_chip(pg, tr) for tr in D["tracks"])}</ul>
</section>
<section class="section" aria-labelledby="dny-nadpis">
  <h2 id="dny-nadpis">Tři dny festivalu</h2>
  <ul class="day-cards">{days}</ul>
</section>
<section class="section card" aria-labelledby="info-nadpis">
  <h2 id="info-nadpis">Než vyrazíte</h2>
  <p>Vstupenky od 390 Kč, děti do 12 let zdarma. Tramvaj zastavuje přímo u vstupu, v areálu se neparkuje. Všechny scény jsou bezbariérové.</p>
  <p><a class="button" href="prakticke-informace.html">Praktické informace</a></p>
</section>'''
    prices = [t["priceCzk"] for t in D["practical"]["tickets"]]
    festival = {**festival_ref(), "description": "Festival technologií, her a digitální kultury", "startDate": F["startDate"], "endDate": F["endDate"],
                "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                "location": place_ld(), "image": SITE + "images/og/tranzistor.png",
                "performer": [performer_ld(p) for p in D["performers"] if p["headliner"]],
                "offers": {"@type": "AggregateOffer", "priceCurrency": "CZK", "lowPrice": min(prices), "highPrice": max(prices),
                           "url": SITE + "prakticke-informace.html#vstupenky", "availability": "https://schema.org/InStock"}}
    website = {"@type": "WebSite", "name": "Tranzistor 2027", "url": SITE,
               "potentialAction": {"@type": "SearchAction", "target": SITE + "hledani.html?q={search_term_string}", "query-input": "required name=search_term_string"}}
    write_page(pg, key="home", title="Tranzistor 2027 – festival technologií, her a digitální kultury",
               description="Tranzistor 2027: třídenní festival technologií, her a digitální kultury v Pražské tržnici, 4.–6. června 2027. Program, účinkující a praktické informace.",
               main=main, ld=[festival, website])


def build_program():
    pg = Page("program.html")
    opts = lambda items, label_key: "".join(f'<option value="{x["id"]}">{h(x[label_key])}</option>' for x in items)
    langs = "".join(f'<option value="{x["id"]}">{h(x["label"])}</option>' for x in D["languages"]) + '<option value="zadny">Bez mluveného slova (hudba)</option>'
    days = ('<label><input type="radio" name="den" value="" form="filtry" checked><span>Vše</span></label>' +
            "".join(f'<label><input type="radio" name="den" value="{d["id"]}" form="filtry"><span>{d["weekday"][:2].capitalize()} <small>{h(d["label"].split(" ", 1)[1])}</small>'
                    f'<span class="visually-hidden"> ({d["weekday"]})</span></span></label>' for d in D["days"]))
    events = sorted_events(D["events"])
    main = f'''<h1>Program</h1>
<p class="lead">{len(D["events"])} položek na pěti scénách. Vyberte si podle dne, scény nebo tématu a uložte si, co nechcete propásnout.</p>
<div class="with-sidebar">
  <details class="disclosure filters-panel" id="filtry-panel">
    <summary><span class="disclosure__label">Další filtry<span id="pocet-filtru"></span></span>{disclosure_icon()}</summary>
    <form class="filters" id="filtry" action="program.html" method="get">
      <label>Scéna<select name="scena"><option value="">Všechny scény</option>{opts(D["venues"], "name")}</select></label>
      <label>Téma<select name="tema"><option value="">Všechna témata</option>{opts(D["tracks"], "name")}</select></label>
      <label>Formát<select name="format"><option value="">Všechny formáty</option>{opts(D["eventTypes"], "label")}</select></label>
      <label>Úroveň<select name="uroven"><option value="">Všechny úrovně</option>{opts(D["levels"], "label")}</select></label>
      <label>Jazyk<select name="jazyk"><option value="">Všechny jazyky</option>{langs}</select></label>
      <label class="check"><input type="checkbox" name="rodiny" value="1"> Jen vhodné pro rodiny</label>
      <p><button class="button button--ghost button--small" type="reset">Zrušit filtry</button></p>
    </form>
  </details>
  <section aria-labelledby="vysledky-nadpis">
    <h2 id="vysledky-nadpis" class="visually-hidden">Výpis programu</h2>
    <fieldset class="day-switch"><legend class="visually-hidden">Den</legend><div class="chips" id="dny-volba">{days}</div></fieldset>
    <p id="pocet" class="result-count" role="status">Zobrazeno {len(events)} z {len(D["events"])} položek programu</p>
    <div id="vypis">{day_groups(pg, events, lambda e: event_card(pg, e, data=True))}</div>
    <div id="prazdny-program" class="card empty" hidden><p>Filtrům neodpovídá žádná položka.</p><p><button type="reset" form="filtry" class="button">Zrušit filtry</button></p></div>
  </section>
</div>'''
    write_page(pg, key="program", title="Program – Tranzistor 2027",
               description=f"Program festivalu Tranzistor 2027: {len(D['events'])} přednášek, workshopů, koncertů a turnajů na pěti scénách. Filtrujte podle dne, scény, tématu a úrovně.",
               main=main, crumbs=[("index.html", "Úvod"), (None, "Program")])


def build_event(e):
    pg = Page(event_path(e))
    v, d = VE[e["venueId"]], DA[e["dayId"]]
    parallel = [x for x in sorted_events(D["events"]) if x["id"] != e["id"] and x["start"] < e["end"] and e["start"] < x["end"]]
    lang = LA[e["language"]]["label"] if e["language"] else "Bez mluveného slova"
    capacity = f'{e["capacity"]} míst' if e["capacity"] else f'podle kapacity scény ({v["capacity"]})'
    reservation = "Nutná – " + D["practical"]["workshopRegistration"] if e["registrationRequired"] else "Není potřeba"
    performers = "".join(performer_card(pg, PE[i], "h3") for i in e["performerIds"])
    main = f'''<article id="detail">
<p><a class="back-link" href="{pg.url("program.html")}">← Zpět na program</a></p>
<header class="detail-head detail-head--{e["trackId"]}">{event_tags(e)}
  <h1>{h(e["title"])}</h1>
  <p class="detail-head__when">{icon("clock")}{h(d["label"])} · {t(e["start"])}–{t(e["end"])} <span class="detail-head__dur">({e["durationMinutes"]} min)</span></p>
  <p class="detail-head__where">{icon("place")}<a href="{pg.url(venue_path(v))}">{h(v["name"])}</a> · {h(v["zone"])}</p>
  <p class="detail-head__action">{save_button(e)}</p>
</header>
<p class="lead">{h(e["description"])}</p>
<dl class="meta-list"><dt>Scéna</dt><dd><a href="{pg.url(venue_path(v))}">{h(v["name"])}</a> – {h(v["kind"])}</dd>
  <dt>Formát</dt><dd>{h(TY[e["type"]]["label"])}</dd>
  <dt>Téma</dt><dd><a href="{pg.url("program.html?tema=" + e["trackId"])}">{h(TR[e["trackId"]]["name"])}</a></dd>
  <dt>Úroveň</dt><dd>{h(LV[e["level"]]["label"])}</dd>
  <dt>Jazyk</dt><dd>{h(lang)}</dd>
  <dt>Kapacita</dt><dd>{h(capacity)}</dd>
  <dt>Rezervace</dt><dd>{h(reservation)}</dd></dl>
<section aria-labelledby="kdo"><h2 id="kdo">{"Účinkující" if len(e["performerIds"]) > 1 else "Účinkuje"}</h2><ul class="grid grid--2">{performers}</ul></section>
<section aria-labelledby="soubezne"><h2 id="soubezne">Současně na jiných scénách</h2>
{('<ol class="event-rows">' + "".join(event_row(pg, x) for x in parallel) + "</ol>") if parallel else "<p>V tomto čase neběží nic dalšího.</p>"}</section>
</article>'''
    kind = {"concert": "MusicEvent", "livecoding": "MusicEvent", "workshop": "EducationEvent", "talk": "EducationEvent",
            "keynote": "EducationEvent", "panel": "EducationEvent", "tournament": "SportsEvent"}.get(e["type"], "Event")
    ld = {"@type": kind, "name": e["title"], "description": e["description"], "startDate": e["start"], "endDate": e["end"],
          "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
          "location": {"@type": "Place", "name": f'{v["name"]} – {F["location"]["name"]}', "address": place_ld()["address"]},
          "performer": [performer_ld(PE[i]) for i in e["performerIds"]], "superEvent": festival_ref(), "url": SITE + pg.path}
    if e["language"]:
        ld["inLanguage"] = e["language"]
    if e["capacity"]:
        ld["maximumAttendeeCapacity"] = e["capacity"]
    write_page(pg, key="event", title=f'{e["title"]} ({d["weekday"]} {hm(e["start"])}) – Tranzistor 2027', description=e["description"], main=main, og_type="article",
               crumbs=[("index.html", "Úvod"), ("program.html", "Program"), (None, e["title"])], ld=[ld])


def build_performers():
    pg = Page("ucinkujici.html")
    performers = sorted(D["performers"], key=lambda p: norm(p["name"]))
    main = f'''<h1>Účinkující</h1>
<p class="lead">Řečníci, lektoři, hudebníci, umělci a e-sportové týmy z {len(set(p["country"] for p in D["performers"]))} zemí.</p>
<details class="disclosure filters-panel" id="filtry-panel">
  <summary><span class="disclosure__label">Hledat, filtrovat a řadit<span id="pocet-filtru"></span></span>{disclosure_icon()}</summary>
  <form class="filters" id="filtry-ucinkujici" action="ucinkujici.html" method="get">
    <label>Jméno obsahuje<input type="text" name="jmeno" autocomplete="off"></label>
    <label>Typ<select name="typ"><option value="">Všechny typy</option>{"".join(f'<option value="{x["id"]}">{h(x["label"])}</option>' for x in D["performerTypes"])}</select></label>
    <label>Téma<select name="tema"><option value="">Všechna témata</option>{"".join(f'<option value="{x["id"]}">{h(x["name"])}</option>' for x in D["tracks"])}</select></label>
    <label>Řazení<select name="razeni"><option value="az">Podle jména A–Z</option><option value="za">Podle jména Z–A</option><option value="hvezdy">Hlavní hvězdy první</option></select></label>
  </form>
</details>
<p id="pocet" class="result-count" role="status">Zobrazeno {len(performers)} z {len(D["performers"])} účinkujících</p>
<ul id="vypis" class="person-list">{"".join(performer_card(pg, p, "h2", data=True) for p in performers)}</ul>
<p id="prazdni-ucinkujici" class="card empty" hidden>Nikdo neodpovídá zadání. Zkuste jiné jméno nebo zrušte filtry.</p>'''
    write_page(pg, key="performers", title="Účinkující – Tranzistor 2027",
               description=f"Všech {len(D['performers'])} účinkujících festivalu Tranzistor 2027: řečníci, lektoři, hudebníci, umělci a e-sportové týmy. Hledejte podle jména, typu a tématu.",
               main=main, crumbs=[("index.html", "Úvod"), (None, "Účinkující")])


def build_performer(p):
    pg = Page(performer_path(p))
    events = EVENTS_BY_PERFORMER.get(p["id"], [])
    tracks = " ".join(f'<span class="tag tag--track tag--{x}">{h(TR[x]["name"])}</span>' for x in p["trackIds"])
    main = f'''<article id="detail">
<div class="profile"><header class="profile__head"><img class="profile__photo" src="{pg.url(p["image"]["src"])}" alt="{h(p["image"]["alt"])}" width="160" height="160">
  <h1>{h(p["name"])}</h1><p class="lead">{h(p["tagline"])}</p>
  {'<p><span class="tag tag--headliner">Hlavní hvězda festivalu</span></p>' if p["headliner"] else ""}</header>
<div><dl class="meta-list"><dt>Typ</dt><dd>{h(PT[p["type"]]["label"])}</dd><dt>Země</dt><dd>{h(D["countries"][p["country"]])}</dd><dt>Témata</dt><dd>{tracks}</dd></dl>
<p>{h(p["bio"])}</p></div></div>
<section aria-labelledby="vystoupeni"><h2 id="vystoupeni">Vystoupení na festivalu ({len(events)})</h2>
<ol class="event-list">{"".join(event_card(pg, e, "h3", show_day=True) for e in events)}</ol></section>
<p><a class="back-link" href="{pg.url("ucinkujici.html")}">← Všichni účinkující</a></p>
</article>'''
    ld = {**performer_ld(p), "description": p["bio"], "image": SITE + p["image"]["src"],
          "performerIn": [{"@type": "Event", "name": e["title"], "startDate": e["start"], "url": SITE + event_path(e)} for e in events]}
    if ld["@type"] == "Person":
        ld["jobTitle"] = p["tagline"]
        ld["nationality"] = {"@type": "Country", "name": D["countries"][p["country"]]}
    write_page(pg, key="performer", title=f'{p["name"]} – Tranzistor 2027', description=f'{p["name"]} – {p["tagline"]}. {p["bio"]}', main=main,
               og_type="profile", crumbs=[("index.html", "Úvod"), ("ucinkujici.html", "Účinkující"), (None, p["name"])], ld=[ld])


def build_venues():
    pg = Page("sceny.html")
    cards = "".join(f'''<li class="card venue-card"><img src="{v["image"]["src"]}" alt="" width="800" height="450" loading="lazy">
  <h2><a href="{venue_path(v)}">{h(v["name"])}</a></h2><p>{h(v["kind"])} · {h(v["zone"])} · kapacita {v["capacity"]}</p>
  <p>{h(", ".join(v["focus"]))}</p><p data-now-venue="{v["id"]}"></p></li>''' for v in D["venues"])
    main = f'''<h1>Scény a areál</h1>
<p class="lead">Pět scén v jednom areálu – čtyři kryté a jedna venkovní u Vltavy.</p>
<section aria-labelledby="mapa-nadpis">
  <h2 id="mapa-nadpis">Schéma areálu</h2>
  <img class="map" src="{F["areaMap"]["src"]}" alt="{h(F["areaMap"]["alt"])}" width="800" height="560">
  <p>Hlavní vstup a tramvajová zastávka jsou na severovýchodě areálu. Textový popis scén najdete níže.</p>
</section>
<ul class="grid grid--3 section">{cards}</ul>'''
    write_page(pg, key="venues", title="Scény a areál – Tranzistor 2027",
               description="Pět scén festivalu Tranzistor 2027 v Pražské tržnici: schéma areálu, kapacity, zaměření a co právě běží.",
               main=main, crumbs=[("index.html", "Úvod"), (None, "Scény")],
               ld=[{**place_ld(), "@type": "Place", "hasMap": SITE + "sceny.html#mapa-nadpis",
                    "containsPlace": [{"@type": "EventVenue", "name": v["name"], "url": SITE + venue_path(v)} for v in D["venues"]]}])


def build_venue(v):
    pg = Page(venue_path(v))
    events = sorted_events([e for e in D["events"] if e["venueId"] == v["id"]])
    acc = v["accessibility"]
    main = f'''<article id="detail">
<h1>{h(v["name"])}</h1><p class="lead">{h(v["kind"])} · {h(v["zone"])}</p>
<img class="venue-hero" src="{pg.url(v["image"]["src"])}" alt="{h(v["image"]["alt"])}" width="800" height="450">
<p>{h(v["description"])}</p>
<dl class="meta-list"><dt>Kapacita</dt><dd>{v["capacity"]} osob</dd><dt>Prostor</dt><dd>{"krytý" if v["indoor"] else "venkovní"}</dd>
  <dt>Zaměření</dt><dd>{h(", ".join(v["focus"]))}</dd><dt>Vybavení</dt><dd>{h(", ".join(v["facilities"]))}</dd></dl>
<section aria-labelledby="pristupnost"><h2 id="pristupnost">Přístupnost</h2>{icon_list([
        ("accessible", "Bezbariérový přístup", "Ano" if acc["wheelchair"] else "Ne"),
        ("info", "Indukční smyčka", "Ano" if acc["hearingLoop"] else "Ne"),
        ("check", "", acc["note"])])}</section>
<section aria-labelledby="program-sceny"><h2 id="program-sceny">Program scény ({len(events)})</h2>{day_groups(pg, events, lambda e: event_card(pg, e))}</section>
</article>'''
    ld = {"@type": "EventVenue", "name": v["name"], "description": v["description"], "image": SITE + v["image"]["src"],
          "maximumAttendeeCapacity": v["capacity"], "containedInPlace": place_ld(), "url": SITE + pg.path,
          "event": [{"@type": "Event", "name": e["title"], "startDate": e["start"], "url": SITE + event_path(e)} for e in events]}
    write_page(pg, key="venue", title=f'{v["name"]} – Tranzistor 2027', description=f'{v["name"]} – {v["kind"]}. {v["description"]}', main=main,
               crumbs=[("index.html", "Úvod"), ("sceny.html", "Scény"), (None, v["name"])], ld=[ld])


def build_my():
    pg = Page("muj-program.html")
    main = f'''<h1>Můj program</h1>
<p class="lead">Položky, které jste si uložili. Program se ukládá jen v tomto prohlížeči, bez registrace.</p>
<div id="muj">{NOSCRIPT}</div>'''
    write_page(pg, key="my", title="Můj program – Tranzistor 2027",
               description="Váš osobní program festivalu Tranzistor 2027 uložený v tomto prohlížeči, s upozorněním na časové kolize.",
               main=main, crumbs=[("index.html", "Úvod"), (None, "Můj program")])


def build_practical():
    pg = Page("prakticke-informace.html")
    P = D["practical"]
    rows = []
    for tk in P["tickets"]:
        price = f'{tk["priceCzk"]:,} Kč'.replace(",", " ") if tk["priceCzk"] else "zdarma"
        valid = " · ".join(DA[x]["weekday"][:2] for x in tk["validDayIds"])
        rows.append(f'<tr><th scope="row">{h(tk["name"])}</th><td data-label="Cena" class="price">{price}</td><td data-label="Platí">{valid}</td><td class="ticket-desc">{h(tk["description"])}</td></tr>')
    loc = F["location"]
    service_icons = ["restaurant", "water", "card", "bag", "hospital", "face", "wifi"]
    faq = "".join(f'<details class="disclosure faq-item"><summary><span class="disclosure__label">{h(q["question"])}</span>{disclosure_icon()}</summary>'
                  f'<div class="disclosure__body"><p>{h(q["answer"])}</p></div></details>' for q in P["faq"])
    nav = [("vstupenky", "ticket", "Vstupenky"), ("doprava", "train", "Doprava"), ("pristupnost", "accessible", "Přístupnost"),
           ("sluzby", "cafe", "Služby"), ("pravidla", "info", "Pravidla"), ("caste-dotazy", "help", "Časté dotazy")]
    main = f'''<h1>Praktické informace</h1>
<nav aria-label="Obsah stránky" class="page-nav"><ul>{"".join(f'<li><a href="#{a}"><span class="page-nav__icon">{icon(i)}</span>{l}</a></li>' for a, i, l in nav)}</ul></nav>
<section id="vstupenky" aria-labelledby="h-vstupenky"><h2 id="h-vstupenky">Vstupenky</h2>
  <div class="table-wrap"><table class="data-table tickets"><caption class="visually-hidden">Ceny vstupenek</caption>
  <thead><tr><th scope="col">Vstupenka</th><th scope="col">Cena</th><th scope="col">Platí</th><th scope="col">Popis</th></tr></thead>
  <tbody>{"".join(rows)}</tbody></table></div>
  <p>{h(P["workshopRegistration"])}</p>
  <p><a class="button button--accent" href="{F["ticketShopUrl"]}">Koupit vstupenky</a></p></section>
<section id="doprava" aria-labelledby="h-doprava"><h2 id="h-doprava">Doprava</h2>
  <address>{h(loc["name"])}<br>{h(loc["streetAddress"])}<br>{h(loc["postalCode"])} {h(loc["city"])}</address>
  {icon_list([({"Kolo": "bike", "Auto": "car"}.get(x["mode"], "train"), x["mode"], x["description"]) for x in P["transport"]])}</section>
<section id="pristupnost" aria-labelledby="h-pristupnost"><h2 id="h-pristupnost">Přístupnost</h2>
  {icon_list([("accessible", "", a) for a in P["accessibility"]])}
  <p>Přístupnost jednotlivých scén najdete na stránce <a href="sceny.html">Scény</a>.</p></section>
<section id="sluzby" aria-labelledby="h-sluzby"><h2 id="h-sluzby">Služby v areálu</h2>
  {icon_list([(service_icons[i] if i < len(service_icons) else "info", s["name"], s["description"]) for i, s in enumerate(P["services"])])}</section>
<section id="pravidla" aria-labelledby="h-pravidla"><h2 id="h-pravidla">Pravidla</h2>{icon_list([("info", "", r) for r in P["rules"]])}</section>
<section id="caste-dotazy" class="faq" aria-labelledby="h-faq"><h2 id="h-faq">Časté dotazy</h2>{faq}</section>'''
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["question"],
                                                   "acceptedAnswer": {"@type": "Answer", "text": q["answer"]}} for q in P["faq"]]}
    write_page(pg, key="practical", title="Praktické informace – Tranzistor 2027",
               description="Vstupenky, doprava, přístupnost, služby v areálu, pravidla a časté dotazy k festivalu Tranzistor 2027.",
               main=main, crumbs=[("index.html", "Úvod"), (None, "Praktické informace")], ld=[faq_ld])


def build_search():
    pg = Page("hledani.html")
    write_page(pg, key="search", title="Výsledky hledání – Tranzistor 2027", description="Výsledky vyhledávání na webu festivalu Tranzistor 2027.",
               main=f'<h1>Výsledky hledání</h1>\n<div id="vysledky">{NOSCRIPT}</div>', crumbs=[("index.html", "Úvod"), (None, "Hledání")])


def build_about():
    pg = Page("o-festivalu.html")
    rows = "".join(f'<tr><th scope="row">{x["edition"]}. ročník ({x["year"]})</th><td data-label="Termín">{date_cz(x["startDate"])} – {date_cz(x["endDate"])}</td>'
                   f'<td data-label="Návštěvnost">{x["attendance"]:,}</td><td data-label="Scény">{x["venueCount"]}</td><td class="data-table__wide">{h(x["summary"])}</td></tr>'.replace(",", " ")
                   for x in F["history"])
    rows += (f'<tr><th scope="row">{F["edition"]}. ročník ({F["year"]})</th><td data-label="Termín">{date_cz(F["startDate"])} – {date_cz(F["endDate"])}</td>'
             f'<td data-label="Návštěvnost">očekáváme {F["expectedAttendance"]:,}</td><td data-label="Scény">{len(D["venues"])}</td><td class="data-table__wide">Letošní ročník.</td></tr>').replace(",", " ")
    org = F["organizer"]
    main = f'''<h1>O festivalu</h1>
<p class="lead">{h(F["description"])}</p><p>{h(F["character"])}</p>
<h2>Témata</h2><ul class="track-chips">{"".join(track_chip(pg, tr) for tr in D["tracks"])}</ul>
<h2>Historie ročníků</h2><div class="table-wrap"><table class="data-table"><caption class="visually-hidden">Přehled ročníků festivalu</caption>
<thead><tr><th scope="col">Ročník</th><th scope="col">Termín</th><th scope="col">Návštěvnost</th><th scope="col">Scény</th><th scope="col">Shrnutí</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>Pořadatel a kontakt</h2><address class="card">{h(org["name"])}<br>Obecné dotazy: <a href="mailto:{org["email"]}">{org["email"]}</a><br>
Média: <a href="mailto:{org["pressEmail"]}">{org["pressEmail"]}</a></address>'''
    ld = {"@type": "Organization", "name": org["name"], "email": org["email"], "url": SITE,
          "contactPoint": [{"@type": "ContactPoint", "contactType": "media", "email": org["pressEmail"]}]}
    write_page(pg, key="about", title="O festivalu – Tranzistor 2027",
               description="Tranzistor je festival technologií, her a digitální kultury. Témata, historie ročníků, pořadatel a kontakt.",
               main=main, crumbs=[("index.html", "Úvod"), (None, "O festivalu")], ld=[ld, {**festival_ref(), "description": F["description"],
                                                                                           "startDate": F["startDate"], "endDate": F["endDate"], "location": place_ld()}])


def build_meta_files():
    urls = "".join(f"  <url><loc>{SITE}{'' if p == 'index.html' else p}</loc></url>\n" for p, _ in PAGES if p not in ("hledani.html", "muj-program.html"))
    (WEB / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n', encoding="utf-8")
    (WEB / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /hledani.html\n\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8")
    top = "\n".join(f"- [{h_title}]({SITE}{'' if p == 'index.html' else p})" for p, h_title in PAGES if "/" not in p and p not in ("hledani.html", "muj-program.html"))
    days = "\n".join(f"- {d['label']} ({d['weekday']}): {d['opens']}–{d['closes']}, {d['theme']}" for d in D["days"])
    (WEB / "llms.txt").write_text(f"""# Tranzistor 2027

> {F["fullName"]}. {F["description"]}

- Termín: {F["startDate"]} až {F["endDate"]} (pátek až neděle)
- Místo: {F["location"]["name"]}, {F["location"]["streetAddress"]}, {F["location"]["postalCode"]} {F["location"]["city"]}
- Rozsah: {len(D["venues"])} scén, {len(D["events"])} položek programu, {len(D["performers"])} účinkujících
- Kontakt: {F["organizer"]["email"]}

## Dny
{days}

## Hlavní stránky
{top}

## Data
- Kompletní program, účinkující a scény jsou na stránkách v sekcích program/, ucinkujici/ a sceny/; seznam všech adres je v {SITE}sitemap.xml
""", encoding="utf-8")


def main():
    if not (WEB / "js" / "app.js").is_file() or not (WEB / "css" / "style.css").is_file():
        raise SystemExit("Chybí web/js/app.js nebo web/css/style.css.")
    for old in list(WEB.glob("*.html")) + [WEB / "program", WEB / "ucinkujici", WEB / "sceny"]:
        if old.is_dir():
            shutil.rmtree(old)
        elif old.exists():
            old.unlink()
    build_home(); build_program(); build_performers(); build_venues(); build_my(); build_practical(); build_search(); build_about()
    for e in D["events"]:
        build_event(e)
    for p in D["performers"]:
        build_performer(p)
    for v in D["venues"]:
        build_venue(v)
    build_meta_files()
    for tool in ("build_web_data.py", "generate_images.py"):
        subprocess.run([sys.executable, str(ROOT / "tools" / tool), "web"], check=True)
    print(f"web/: {len(PAGES)} stránek")


if __name__ == "__main__":
    main()
