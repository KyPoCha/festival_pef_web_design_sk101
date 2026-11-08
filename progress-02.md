# Progress 02 – UX návrh, prototyp a interaktivní funkce

| | |
|---|---|
| **Tým** | sk101 – Kyrylo Polishchuk, Daniel Šimůnek, Ngoc Tuan Nguyen, David Anderle |
| **Odevzdání** | cvičení 3 |
| **Odevzdávané soubory** | `prototype/` (spustitelný bez instalace), `progress-02.md`, prezentace (`.odp` a `.pdf`) |
| **Jak prototyp spustit** | Otevřít `prototype/index.html` v prohlížeči (dvojklikem, bez serveru a bez internetu). |

---

## 1. Co jsme od minula udělali

- Vytvořili jsme prototyp všech částí webu ze sitemapy: 11 stránek, mobilní i desktopové rozložení, skutečná data ze všech 77 položek programu.
- Navrhli a zprovoznili jsme šest interaktivních funkcí (kapitola 3).
- Doplnili jsme datovou základnu podle zpětné vazby a kontroly proti specifikaci (kapitola 5).
- Na sdílené stránce jsme hlasovali o čtyřech variantách vzhledu a zvolenou kombinaci zapracovali do prototypu (kapitola 4).

## 2. Prototyp

**Forma.** Prototyp je vibe-kódovaný základ webu v čistém HTML, CSS a JavaScriptu, bez knihoven a bez připojení k internetu. Data čte ze souboru `prototype/js/data.js`, který se strojově odvozuje z `data.json` (prohlížeč nedovolí stránce otevřené ze souboru načíst JSON přímo). Shodu obou souborů hlídá kontrolní skript.

**Stránky.** Úvod, Program, detail položky programu, Účinkující, detail účinkujícího, Scény se schématem areálu, detail scény, Můj program, Praktické informace, O festivalu a Výsledky hledání. Každá stránka má vlastní titulek a popis (`meta description`), detailní stránky si je nastavují podle zobrazené položky.

**Mobile-first.** Hlavní návrh je mobilní. Základní styly jsou psané pro telefon o šířce 360 px a širší rozložení se k nim přidává až pravidly od 600 px (dva sloupce karet) a od 900 px (vodorovné menu nahoře, filtry v postranním panelu, tři až čtyři sloupce, spodní lišta se skryje). Na mobilu je pět hlavních sekcí ve spodní liště v dosahu palce, filtry jsou sbalené a ovládací prvky mají nejméně 44 px na výšku.

**Navigace a hierarchie.** Logo vede na úvod, hlavní nabídka má pět sekcí, vyhledávání a Můj program jsou v záhlaví každé stránky. Všechny stránky kromě úvodní mají drobečkovou navigaci. Detail položky vede na účinkující a scénu a zpět; odkaz „Zpět na program“ vrací na program s původně nastavenými filtry.

## 3. Interaktivní funkce

| # | Funkce | Potřeba uživatele | Cílová skupina | Scénář | Stav |
|---|---|---|---|---|---|
| F1 | Filtr programu podle dne, scény, tématu, formátu, úrovně, jazyka a vhodnosti pro rodiny; filtry jsou v adrese stránky | Zúžit 77 položek na několik, které uživatele zajímají | všechny | S1, S2, S3 | hotovo |
| F2 | Můj program – uložení a odebrání položky, počet v záhlaví, uložení v prohlížeči bez registrace | Sestavit si vlastní plán návštěvy | A, B, D | S1, S2 | hotovo |
| F3 | Upozornění na časovou kolizi v Mém programu | Zjistit předem, že se dvě vybrané položky kryjí | A, B | S2 | hotovo |
| F4 | Vyhledávání účinkujících, programu a scén bez ohledu na diakritiku a velikost písmen, se stránkou výsledků | Najít něco podle útržku jména | všechny | S2, S5 | hotovo |
| F5 | „Právě teď na scénách“ podle aktuálního času; pro testování lze čas nasimulovat (`?cas=2027-06-05T19:45`) | Rozhodnout se na místě, kam jít | A, D | S4 | hotovo |
| F6 | Hledání, filtrování a řazení účinkujících | Projít 67 účinkujících podle typu a tématu | B | S2 | hotovo |

Zadání vyžaduje alespoň tři funkce. Jádrem jsou F1 až F4, které pokrývají všechny tři klíčové scénáře.

## 4. Návrhová rozhodnutí a výběr variant

Prototyp umí přepínat čtyři rozhodnutí o vzhledu (parametr `?ui=` v adrese, volba se pamatuje). O variantách jsme hlasovali na samostatné stránce, která je ukazuje jako živé náhledy na šířce telefonu.

| Rozhodnutí | Varianty | Doporučení AI | Zvoleno |
|---|---|---|---|
| Barevný směr | A Signál (světlý obsah, tmavomodré záhlaví) · B Kyber (tmavý, z prototypu člena týmu) · C Papír (černobílý kontrastní) | A – čitelnost venku na slunci | **B Kyber** |
| Navigace na mobilu | A Menu nahoře · B Spodní lišta (z prototypu člena týmu) | B – sekce v dosahu palce | **B Spodní lišta** |
| Karta položky programu | A Časová osa · B Dlaždice · C Kompaktní řádek | A – čas se čte jako první | **B Dlaždice** |
| Tlačítko uložit | A Text „Do Mého programu“ · B Hvězdička | A – srozumitelné pro nového návštěvníka | **A Text** |

U barevného směru a karty programu jsme doporučení AI nepřijali. Tmavý vzhled je dnes moderní a na mnoha zařízeních výchozí; všichni v týmu ho sami používáme jako výchozí. Riziko horší čitelnosti tmavého vzhledu, na které AI upozorňovala, jsme ověřili výpočtem kontrastu (kapitola 6).

Zvolená kombinace je v prototypu výchozí; ostatní varianty zůstávají dostupné přes `?ui=` pro srovnání. Podle poznámky z hlasování jsme navíc:

- nahradili znakové ikony ve spodní liště a v záhlaví ikonami SVG ve stylu Material Icons (tvary z Material Icons, Apache License 2.0),
- přesunuli počet uložených položek do pravého horního rohu ikony hvězdičky; při nule se nezobrazuje,
- dotáhli tmavý vzhled: jemná mřížka v pozadí, čas položek neproporcionálním písmem s ikonou hodin, místo s ikonou špendlíku, ilustrace a schéma areálu překreslené do stejné palety.

Po rozhodnutí jsme prošli všechny stránky na šířce telefonu a upravili, co bylo zbytečně dlouhé nebo těžko čitelné:

- **Nadpisové písmo** Chakra Petch (SIL Open Font License 1.1) je uložené ve složce prototypu, takže funguje bez internetu; text zůstává v systémovém písmu.
- **Úvod** se zkrátil zhruba na polovinu: odpočet do zahájení s prvními položkami programu místo prázdných karet scén, hlavní hvězdy ve vodorovném pásu, témata jako kompaktní dlaždice se počtem položek, dny jako tři řádky.
- **Program** má nad výpisem přepínač dnů (Vše · Pá · So · Ne), který zůstává při posouvání nahoře; ostatní filtry jsou ve sbaleném panelu „Další filtry“.
- **Detail položky** začíná výrazným záhlavím s časem, místem a tlačítkem uložit; souběžný program je v kompaktních řádcích.
- **Účinkující** jsou v kompaktním seznamu (stránka je o 40 % kratší), profil má vycentrované záhlaví s portrétem.
- **Vstupenky** se na telefonu zobrazují jako karty místo úzké tabulky se čtyřmi sloupci; na širším displeji zůstává tabulka.
- **Desktop** využívá šířku: dlaždice programu a řádky ve dvou sloupcích.

Ve druhém kole jsme na stránce pro výběr rozhodli o komponentách a pohybu. Ve všech osmi bodech jsme zvolili variantu A: upozornění na kolizi jako panel s ikonou, potvrzení uložení s možností „Vrátit“, navigaci po stránce Praktické informace jako čipy s ikonami, které zvýrazní právě čtenou část, časté dotazy jako karty se šipkou, služby jako karty s ikonami, jemné animace (vypnuté, pokud je uživatel v systému vypnul), neonovou zelenou a živý obvod v úvodu.

Zvolené styly jsme pak sjednotili do **společných pravidel pro celý web**:

- **karty** mají jednotné zaoblení a okraj,
- **skládací bloky** (filtry programu, filtry účinkujících, časté dotazy) vypadají a chovají se stejně – karta se šipkou, která se při otevření otočí,
- **seznamy** (služby, doprava, přístupnost, pravidla, přístupnost scény) jsou karty s ikonou,
- **tabulky** (vstupenky, historie ročníků) mají jeden styl a na telefonu se skládají do karet,
- **fakta v detailu** položky, účinkujícího a scény jsou v jednotném rámečku s oddělenými řádky.

Z textů webu jsme odstranili zmínky o studijním projektu a fiktivních odkazech; web, e-maily a odkaz na vstupenky festivalu používají doménu tranzistor-festival.cz.

## 5. Oprava datové základny

Po cvičení 2 jsme dostali zpětnou vazbu, že v `data.json` něco chybí. Porovnali jsme data se zadáním a se slibami ve specifikaci a našli pět mezer:

| Chybělo | Proč je to problém | Co jsme doplnili |
|---|---|---|
| Obrázky | Zadání vyžaduje obrázky vytvořené AI; výpisy a detaily je potřebují | `image` (cesta a alternativní text) u festivalu, 5 scén a 67 účinkujících |
| Schéma areálu | Specifikace slibuje schéma na stránce Scény | `festival.areaMap` a `mapPosition` u každé scény |
| Historie ročníků | Specifikace slibuje historii na stránce O festivalu | `festival.history` se dvěma předchozími ročníky |
| Kontakt pro média, odkaz na vstupenky | Média jsou vedlejší cílovou skupinou; úvod má výzvu k nákupu | `organizer.pressEmail`, `festival.ticketShopUrl` |
| Témata tří panelistů | Filtr účinkujících podle tématu by je u jejich panelu nenašel | téma Technologie a společnost u tří účinkujících |

Kontrolní skript jsme rozšířili o nová pravidla (obrázky, schéma, historie, shoda témat účinkujícího a jeho vystoupení, shoda `js/data.js` s `data.json`). Na původních datech 1.0.0 hlásí 83 chyb, na nových 0. Rozsah dat, identifikátory a program se nezměnily; změny jsou zapsané ve specifikaci v kapitole 8.

## 6. Co jsme ověřovali a jak

**Strojově (provedla AI):**

| Kontrola | Postup | Výsledek |
|---|---|---|
| Kontrast barev vzhledu Kyber | Výpočet poměru kontrastu podle WCAG pro 23 dvojic barev textu a pozadí (text, odkazy, štítky, tlačítka, upozornění, spodní lišta) | všechny vyhovují AA, nejnižší poměr 7,4 : 1 |
| Všechny stránky na mobilu (360 px) a desktopu (1280 px) | Automatický test v prohlížeči Chrome (vlastní skript): chyby v konzoli, vodorovné přetečení, jedinečná `id`, právě jeden `h1`, nadpisy bez přeskočené úrovně, načtení obrázků | 11 stránek × 2 šířky, bez chyb |
| Scénáře S1 až S5 | Stejný test prochází scénáře klikáním: filtry, uložení, opětovné načtení, kolize, odebrání, zpětný odkaz s filtry, simulovaný čas, hledání bez diakritiky, prázdný výsledek | všechny kroky prošly |
| Klávesnice a menu | První Tab vede na „Přeskočit na obsah“; tlačítko Menu přepíná `aria-expanded` | prošlo |
| Spodní lišta | Je výchozí na mobilu, má 5 ikon, počet uložených ukazuje v rohu ikony a při nule ho skryje | prošlo |
| Varianty vzhledu | Každá kombinace se použije a nezpůsobí přetečení na mobilu | prošlo |
| Data | Kontrolní skript dat včetně shody `js/data.js` a existence obrázků | 0 chyb |
| Přístupnost – automatický audit | axe-core (stejný typ nástroje jako WAVE nebo Lighthouse) podle WCAG 2.0, 2.1 a 2.2 na úrovni A a AA: 12 stránek a stavů na mobilu i desktopu | bez porušení; nalezené drobnosti (duplicitní názvy orientačních bodů, pruh s časem mimo orientační body) opraveny |
| Přístupnost – klávesnice | Průchod tabulátorem po 40 krocích na čtyřech stránkách: každý prvek má viditelný fokus a fokus není schovaný pod přilepenými lištami (WCAG 2.2, 2.4.11) | prošlo po opravě – původně fokus zajížděl pod spodní lištu a pole hledání mělo jen změnu barvy okraje |
| Přístupnost – zvětšení a pohyb | Zobrazení na šířce 320 px (odpovídá zvětšení 400 %) bez vodorovného posouvání; při vypnutých animacích v systému neběží žádná animace | prošlo |
| Přístupnost – čtečka obrazovky (strojově) | Názvy a stavy ovládacích prvků z přístupnostního stromu prohlížeče, např. „Můj plán, 2 uložené položky“, „V Mém programu: Capture the Flag pro začátečníky, stisknuto“ | v pořádku po opravě – počet u hvězdičky se dřív četl jako „1Můj plán“ |
| Kontrast animovaného úvodu | Výpočet nejhoršího případu, kdy svítící puls obvodu projde za textem | původně 1,28 : 1; obvod je za textem ztlumený, nejhorší případ teď 5,8 : 1 |

Test scénářů a vzhledu má 190 kontrol, test přístupnosti 45 kontrol; všechny prošly. Strojové kontroly nenahrazují vyzkoušení se skutečnou čtečkou obrazovky ani validátor HTML W3C; to je součástí ruční kontroly.

**Ručně (tým):** web jsme zkontrolovali nástrojem WAVE (hodnocení 10 z 10) a prošli jsme ho na vlastních telefonech.

## 7. Použití AI a ověření výstupů

| K čemu | Nástroj | Jak ověřeno |
|---|---|---|
| Prototyp (HTML, CSS, JavaScript) | Claude Code | Automatický test v prohlížeči (kapitola 6) a prohlédnutí snímků obrazovky na mobilu i desktopu |
| Ilustrace (SVG) a schéma areálu | Claude Code, vlastní skript, který ilustrace kreslí z dat | Kontrolní skript ověřuje existenci souborů; vzhled prohlédnut na snímcích |
| Doplnění datové základny | Claude Code | Rozšířený kontrolní skript: 83 chyb na staré verzi, 0 na nové |
| Stránka pro výběr variant | Claude Code | Otevřena na šířce telefonu i desktopu, výběr varianty vyzkoušen, uložený hlas přečten zpět ze sdíleného úložiště |
| Úprava vzhledu podle hlasování | Claude Code | Výpočet kontrastu, opakovaný test v prohlížeči, prohlédnutí snímků obrazovky |

**Chyby, které AI udělala a test odhalil:** záhlaví na telefonu přetékalo o 67 px (logo, „Můj program“ a Menu se nevešly vedle sebe); ve variantě Kyber ztratily štítky témat barvu; v kompaktní kartě bylo tlačítko uložit příliš široké. Vše bylo opraveno a test zopakován.


## 8. Známá omezení

- Rezervace workshopů není v prototypu funkční; tým rozhodne, zda ji nasimulovat, nebo uvést rezervaci na místě.
- Obsah detailních stránek vykresluje JavaScript, což je slabší pro vyhledávače; řešíme ve 3. iteraci spolu se SEO.
- Ilustrace účinkujících jsou abstraktní monogramy, ne portréty.
- Můj program je uložený jen v jednom prohlížeči.
