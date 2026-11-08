# Progress 03 – první funkční implementace webu

|                         |                                                                                    |
| ----------------------- | ---------------------------------------------------------------------------------- |
| **Tým**                 | sk101 – Kyrylo Polishchuk, Daniel Šimůnek, Ngoc Tuan Nguyen, David Anderle         |
| **Odevzdání**           | cvičení 4                                                                          |
| **Odevzdávané soubory** | `web/` (spustitelný bez instalace), `progress-03.md`, prezentace (`.odp` a `.pdf`) |
| **Jak web spustit**     | Otevřít `web/index.html` v prohlížeči (dvojklikem, bez serveru a bez internetu).   |

---

## 1. Co jsme od minula udělali

- Z prototypu jsme udělali web ve složce `web/`: 157 stránek s obsahem přímo v HTML, z toho 77 stránek položek programu, 67 stránek účinkujících a 5 stránek scén.
- Všechny funkce z prototypu fungují i na webu (kapitola 2.3).
- Prošli jsme aktuální doporučení a trendy v UX a designu a zapsali, co jsme uplatnili (kapitola 3).
- Web jsme připravili pro vyhledávače a nástroje umělé inteligence: titulky, popisy, kanonické adresy, náhledy pro sdílení, strukturovaná data, mapa webu (kapitola 4).
- Zopakovali jsme automatické testy a test přístupnosti na novém webu (kapitola 5).

## 2. Co je implementováno

### 2.1 Stránky

| Stránka             | Adresa                          | Obsah                                                                                       |
| ------------------- | ------------------------------- | ------------------------------------------------------------------------------------------- |
| Úvod                | `index.html`                    | odpočet do zahájení, později „Právě teď a za chvíli“, hlavní hvězdy, témata, dny, vstupenky |
| Program             | `program.html`                  | všech 77 položek po dnech, přepínač dnů, další filtry                                       |
| Detail položky      | `program/<název>.html` (77×)    | čas, scéna, formát, téma, úroveň, jazyk, popis, účinkující, rezervace, souběžný program     |
| Účinkující          | `ucinkujici.html`               | 67 účinkujících, hledání, filtr podle typu a tématu, řazení                                 |
| Detail účinkujícího | `ucinkujici/<jméno>.html` (67×) | medailonek, země, témata, vystoupení s časem a scénou                                       |
| Scény               | `sceny.html`                    | schéma areálu, pět scén, co na scéně právě běží                                             |
| Detail scény        | `sceny/<název>.html` (5×)       | vybavení, přístupnost, program scény po dnech                                               |
| Můj program         | `muj-program.html`              | uložené položky po dnech, upozornění na kolize                                              |
| Praktické informace | `prakticke-informace.html`      | vstupenky, doprava, přístupnost, služby, pravidla, časté dotazy                             |
| O festivalu         | `o-festivalu.html`              | charakter festivalu, témata, historie ročníků, pořadatel, kontakt                           |
| Výsledky hledání    | `hledani.html?q=…`              | výsledky ve skupinách účinkující, program, scény                                            |

### 2.2 Navigace a rozložení

- **Mobile-first.** Základní styly platí pro telefon (360 px), širší rozložení se přidává od 600 px a 900 px. Na telefonu je pět hlavních sekcí ve spodní liště; od 900 px je menu nahoře, filtry v postranním panelu a obsah ve více sloupcích.
- **Hlavní navigace** je na všech stránkách stejná: logo, hledání a Můj program v záhlaví, sekce ve spodní liště nebo v menu, drobečková navigace na všech stránkách kromě úvodu, zápatí s kontaktem a odkazy.
- **Vzhled** je ten, který jsme zvolili v iteraci 2: tmavý vzhled Kyber, dlaždice programu, textové tlačítko „Do Mého programu“, ikony ve stylu Material Icons, nadpisové písmo Chakra Petch a společná pravidla pro karty, skládací bloky, seznamy a tabulky.

### 2.3 Interaktivní funkce

| #   | Funkce                                                                                                                | Scénář     | Stav   |
| --- | --------------------------------------------------------------------------------------------------------------------- | ---------- | ------ |
| F1  | Filtr programu podle dne, scény, tématu, formátu, úrovně, jazyka a vhodnosti pro rodiny; filtry jsou v adrese stránky | S1, S2, S3 | hotovo |
| F2  | Můj program – uložení, odebrání s možností „Vrátit“, počet v záhlaví a ve spodní liště, uložení v prohlížeči          | S1, S2     | hotovo |
| F3  | Upozornění na časovou kolizi v Mém programu                                                                           | S2         | hotovo |
| F4  | Vyhledávání bez ohledu na diakritiku a velikost písmen se stránkou výsledků                                           | S2, S5     | hotovo |
| F5  | „Právě teď na scénách“ podle aktuálního času; čas lze pro test nasimulovat (`?cas=2027-06-05T19:45`)                  | S4         | hotovo |
| F6  | Hledání, filtrování a řazení účinkujících                                                                             | S2         | hotovo |

Odkaz „Zpět na program“ na detailu položky vrací na program s filtry, které byly naposledy nastavené.

## 3. Aktuální doporučení a trendy v UX a designu a jak jsme je uplatnili

Zdroje jsme hledali v listopadu 2026. Přednost mají standardy a primární zdroje (W3C, web.dev, Nielsen Norman Group); přehledy trendů od agentur a nástrojů jsou názory, proto z nich bereme jen to, na čem se shoduje více zdrojů.

| Doporučení nebo trend                                                                                                                           | Zdroj                                                                                                                                              | Jak je to na webu                                                                                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **WCAG 2.2 AA** – nová kritéria: fokus nesmí být schovaný pod přilepenými lištami (2.4.11), cíle dotyku aspoň 24 × 24 px (2.5.8)                | [W3C: What's New in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)                                                         | Stránka se při pohybu tabulátorem posouvá tak, aby fokus nezajel pod záhlaví ani spodní lištu; ovládací prvky mají aspoň 44 px na výšku. Ověřeno testem (kapitola 5).                                                                    |
| **Přístupnost jako zákonný požadavek** – Evropský akt o přístupnosti platí od 28. 6. 2025 a odkazuje na normu EN 301 549 (ta vychází z WCAG)    | [CookieYes: European Accessibility Act](https://www.cookieyes.com/blog/european-accessibility-act/)                                                | Festival prodává vstupenky spotřebitelům v EU, proto bereme WCAG AA jako povinnost, ne jako bonus.                                                                                                                                       |
| **Navigace v dosahu palce** – na telefonu 3–5 hlavních cílů ve spodní liště                                                                     | [UX Planet: Bottom tab bar navigation best practices](https://uxplanet.org/bottom-tab-bar-navigation-design-best-practices-48d46a3b0c36)           | Spodní lišta s pěti sekcemi a ikonami s popisky; počet uložených položek v rohu ikony.                                                                                                                                                   |
| **Předvídatelné vzory místo efektů** – návrat k vzorům, které uživatelé znají; design podle cíle uživatele                                      | [raw.studio: UI and UX Design Trends for 2026](https://raw.studio/blog/ui-and-ux-design-trends-for-2026-what-founders-and-designers-need-to-know/) | Drobečková navigace, karty, skládací filtry, tabulka cen; žádné neobvyklé ovládání.                                                                                                                                                      |
| **Tmavý vzhled** – stále populární, ale potřebuje vlastní práci s kontrastem, ne jen převrácení barev                                           | [UX Design Institute: How to design for dark mode](https://www.uxdesigninstitute.com/blog/dark-mode/)                                              | Pozadí není čistě černé (#090b12), zelený akcent; kontrast všech 23 dvojic barev ověřen výpočtem (nejnižší 7,4 : 1).                                                                                                                     |
| **Výrazná nadpisová typografie**                                                                                                                | [B12: Top website UX/UI trends 2026](https://www.b12.io/resource-center/website-basics/top-website-ux-ui-trends-to-expect-in-2026.html)            | Nadpisy písmem Chakra Petch, text systémovým písmem kvůli čitelnosti a rychlosti.                                                                                                                                                        |
| **Pohyb s ohledem na uživatele** – respektovat systémové nastavení „omezit pohyb“, neodstraňovat zpětnou vazbu                                  | [Tatiana Mac: prefers-reduced-motion](https://www.tatianamac.com/posts/prefers-reduced-motion)                                                     | Jemné animace (karty, potvrzení, obvod v úvodu) běží jen bez omezení pohybu; jinak se stav změní okamžitě, bez animace.                                                                                                                  |
| **„Vrátit“ místo potvrzovacího dialogu** – heuristika kontrola a svoboda uživatele                                                              | [Nielsen Norman Group: User Control and Freedom](https://www.nngroup.com/articles/user-control-and-freedom/)                                       | Po odebrání položky z Mého programu se zobrazí oznámení s tlačítkem „Vrátit“; žádné okno „Opravdu?“.                                                                                                                                     |
| **Progressive enhancement** – základní obsah je už v HTML, JavaScript jen přidává funkce                                                        | [Progressive Enhancement Best Practices](https://mgifford.github.io/ACCESSIBILITY.md/examples/PROGRESSIVE_ENHANCEMENT_BEST_PRACTICES.html)         | Všech 157 stránek je předgenerovaných; bez JavaScriptu je vidět celý program, detaily i ceny. Ovládání, které bez JavaScriptu nefunguje (filtry, uložení), se bez něj nezobrazuje.                                                       |
| **Rychlost (Core Web Vitals)** – LCP ≤ 2,5 s, INP ≤ 200 ms, CLS ≤ 0,1                                                                           | [web.dev: Core Web Vitals thresholds](https://web.dev/articles/defining-core-web-vitals-thresholds)                                                | Žádné knihovny ani externí zdroje; všechny obrázky mají rozměry (stránka neposkakuje), obrázky mimo první obrazovku se načítají až při posunutí, písmo se zobrazí hned (`font-display: swap`). Měření Lighthousem plánujeme v iteraci 4. |
| **Strukturovaná data pro vyhledávače a AI (AEO)** – JSON-LD je nejlépe podložený postup; `llms.txt` je nepovinný doplněk s neprokázaným účinkem | [DEV: llms.txt and GEO in 2026](https://dev.to/mbdev/llmstxt-and-geo-in-2026-how-to-get-your-site-cited-by-ai-search-4352)                         | JSON-LD na všech stránkách, `llms.txt` jako stručné shrnutí festivalu (kapitola 4).                                                                                                                                                      |

**Trendy, které web nepřebírá:** personalizace pomocí AI a hlasové ovládání by potřebovaly server nebo službu třetí strany, web ale musí běžet jen v prohlížeči. Průhledné „skleněné“ vrstvy (glassmorphism) snižují kontrast textu na pozadí, což je u tmavého vzhledu riziko pro WCAG AA.

## 4. Co se proti prototypu změnilo a proč

| Změna                                                                                                                                                                                                                                                                                                                      | Proč                                                                                                                                                                |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Předgenerované stránky.** Prototyp měl jednu šablonu pro každý typ detailu (`udalost.html?id=e001`) a obsah doplňoval JavaScript. Web má pro každou položku, účinkujícího a scénu vlastní soubor HTML, který z `data.json` vytváří náš generátor stránek (skript v Pythonu, je v repozitáři týmu, do odevzdání nepatří). | Obsah je v HTML: přečte ho vyhledávač i nástroj AI a zobrazí se i bez JavaScriptu. Ke spuštění webu skript potřeba není, jen k jeho přegenerování po změně dat.     |
| **Čitelné adresy** – `program/sum-a-signal.html`, `ucinkujici/kristyna-malatova.html`, `sceny/nabrezi.html`                                                                                                                                                                                                                | Adresa říká, co na stránce je, a dá se sdílet. Změna je zapsaná ve specifikaci (verze 1.2, kapitola 8).                                                             |
| **Metadata každé stránky** – vlastní titulek a popis, kanonická adresa, náhled pro sdílení (Open Graph, obrázek 1200 × 630 px)                                                                                                                                                                                             | Titulky detailů obsahují den a čas (např. „Šum a Signál (pátek 19:30) – Tranzistor 2027“), takže je každý titulek jedinečný a srozumitelný i ve výsledcích hledání. |
| **Strukturovaná data JSON-LD** – festival, web s vyhledáváním, položky programu (koncert, vzdělávací akce, sportovní akce), účinkující (osoba, skupina, tým), scény, časté dotazy, pořadatel, drobečková navigace                                                                                                          | Odpovídají viditelnému obsahu stránky, aby vyhledávač i AI dostaly fakta ve strojově čitelné podobě.                                                                |
| **`sitemap.xml`, `robots.txt`, `llms.txt`**                                                                                                                                                                                                                                                                                | Mapa webu obsahuje 155 stránek; výsledky hledání a Můj program v ní nejsou, protože nemají vlastní obsah.                                                           |
| **Bez přepínání variant vzhledu** – parametr `?ui=` a varianty, o kterých jsme hlasovali, jsou z webu odstraněné; ve stylech zůstal jen zvolený vzhled                                                                                                                                                                     | Soubor stylů má 49 kB místo 58 kB a obsahuje jen pravidla, která web používá. Snímky všech stránek před změnou a po ní jsme porovnali po pixelech; vypadají stejně. |
| **Ovládání závislé na JavaScriptu se bez něj nezobrazuje**                                                                                                                                                                                                                                                                 | Bez JavaScriptu by filtry a tlačítka uložit nic nedělaly.                                                                                                           |

Funkce, obsah stránek, scénáře a datová základna se proti prototypu nezměnily.

## 5. Co jsme ověřovali a jak

**Strojově (provedla AI):**

| Kontrola                                               | Postup                                                                                                                                                                                                  | Výsledek             |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| Všech 157 stránek                                      | Testovací skript projde každý soubor: existují všechny místní odkazy a obrázky, každá stránka má popis, kanonickou adresu, Open Graph, viewport a jazyk, JSON-LD je platný JSON, titulky jsou jedinečné | prošlo               |
| Hlavní stránky na mobilu (360 px) a desktopu (1280 px) | 11 stránek × 2 šířky v Chrome: chyby v konzoli, vodorovné přetečení, jedinečná `id`, jeden `h1`, nadpisy bez přeskočené úrovně, načtení obrázků                                                         | bez chyb             |
| Scénáře S1 až S5                                       | Test prochází scénáře klikáním: filtry, uložení, opětovné načtení, kolize, odebrání a „Vrátit“, zpětný odkaz s filtry, simulovaný čas, hledání bez diakritiky, prázdný výsledek                         | všechny kroky prošly |
| Bez JavaScriptu                                        | Program obsahuje všech 77 položek, detail položky a profil účinkujícího mají celý obsah, praktické informace mají ceny; filtry a tlačítka uložit se nezobrazují                                         | prošlo               |
| Přístupnost – automatický audit                        | axe-core podle WCAG 2.0, 2.1 a 2.2 na úrovni A a AA, 12 stránek a stavů na mobilu i desktopu                                                                                                            | bez porušení         |
| Přístupnost – klávesnice                               | Průchod tabulátorem po 40 krocích na čtyřech stránkách: viditelný fokus, fokus není schovaný pod lištami                                                                                                | prošlo               |
| Přístupnost – zvětšení a pohyb                         | Šířka 320 px bez vodorovného posouvání; při omezeném pohybu neběží žádná animace                                                                                                                        | prošlo               |
| Shoda vzhledu s prototypem                             | Snímky všech stránek prototypu a webu porovnány po pixelech po odstranění variant ze stylů                                                                                                              | shodné               |
| Data                                                   | Kontrolní skript dat včetně shody `web/js/data.js` s `data.json` a existence obrázků                                                                                                                    | 0 chyb               |

Test webu má 125 kontrol, test přístupnosti 45 kontrol; všechny prošly. Strojové kontroly nenahrazují validátor HTML W3C, vyzkoušení se skutečnou čtečkou obrazovky ani průchod scénářů lidmi.

## 6. Použití AI a ověření výstupů

| K čemu                                                                    | Nástroj                                            | Jak ověřeno                                                                             |
| ------------------------------------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Skript, který generuje stránky, metadata, JSON-LD, mapu webu a `llms.txt` | Claude Code                                        | Test všech 157 stránek, scénářů a přístupnosti (kapitola 5)                             |
| Úprava stylů a skriptu z prototypu pro web                                | Claude Code                                        | Porovnání snímků po pixelech s prototypem, opakované testy                              |
| Obrázek pro sdílení (1200 × 630 px) a ikona webu                          | Claude Code (vykresleno v prohlížeči z HTML a SVG) | Prohlédnut                                                                              |
| Rešerše doporučení a trendů v UX                                          | Claude Code s vyhledáváním na webu                 | Ke každému bodu je odkaz na zdroj; tvrzení z jediného reklamního zdroje jsme nepřevzali |
| Úprava specifikace a dokumentů                                            | Claude Code                                        | Přečteno týmem                                                                          |

**Chyby, které AI udělala a test odhalil:**

- První převod stylů bez variant změnil vzhled 24 stránek, protože se změnila váha (specificita) pravidel. Odhalilo to porovnání snímků; opraveno tak, že pravidla zvoleného vzhledu si původní váhu ponechala.
- Detail položky a profil účinkujícího měly u několika vystoupení sólových umělců stejný titulek („Šum a Signál – Tranzistor 2027“). Odhalil to test jedinečnosti titulků; titulek detailu teď obsahuje den a čas.
- Filtry a tlačítka uložit byla vidět i bez JavaScriptu, kde nic nedělala. Odhaleno při kontrole stránek bez JavaScriptu; opraveno a přidáno do testu.

## 7. Známá omezení a další kroky

- Validace HTML validátorem W3C proběhne v iteraci 4.
- Výsledky hledání a Můj program se bez JavaScriptu nezobrazí (stránka to oznámí); obě funkce pracují s daty v prohlížeči.
- Každá stránka načítá celou datovou základnu (`js/data.js`, 100 kB), kterou potřebují funkce Můj program, hledání a „Právě teď“. Velikost ověříme měřením Lighthousem v iteraci 4.
- Ilustrace účinkujících jsou abstraktní monogramy, ne portréty.
- Rezervace workshopů není funkční: detail workshopu uvádí, že je potřeba si místo rezervovat na webu, rezervační formulář ale chybí.
- Strukturovaná data jsme zatím ověřili jen jako platný JSON; ověření nástroji vyhledávačů patří do iterace 6.
