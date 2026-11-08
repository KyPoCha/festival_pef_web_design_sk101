# Použití AI – iterace 3: první funkční implementace

| | |
|---|---|
| **Období** | 8. 11. 2026 |
| **Výstupy iterace** | `web/`, `progress-03.md`, `project-specification.md` 1.2, nástroje `tools/build_site.py` a `tools/test_web.js`, úprava `tools/test_accessibility.js` |
| **Odevzdání** | cvičení 4 |

Tento soubor popisuje jen to, co udělala a strojově zkontrolovala AI. Co udělal a zkontroloval tým, zapisuje tým.

## 1. Použité nástroje

| Nástroj | Verze / model | K čemu |
|---|---|---|
| Claude Code (rozšíření pro VS Code) | Claude Opus 5.5 | generátor stránek, úprava stylů a skriptu, testy, rešerše, dokumenty |
| Vyhledávání na webu v Claude Code | – | rešerše doporučení a trendů v UX a designu |
| Python | 3.9 (jen standardní knihovna) | generování stránek, `js/data.js` a ilustrací, kontrola dat |
| Google Chrome + playwright-core | 1.48.2 (jen pro test, není součástí projektu) | test webu, test přístupnosti, snímky obrazovky, vykreslení obrázku pro sdílení |
| axe-core | 4.10.2 (jen pro test) | automatický audit přístupnosti |

## 2. K čemu byla AI použita

| Oblast | Co AI vytvořila |
|---|---|
| Generátor stránek | `tools/build_site.py`: z `data.json` vytvoří 157 stránek (11 hlavních, 77 položek programu, 67 účinkujících, 5 scén) se společným záhlavím, spodní lištou, drobečkovou navigací a zápatím |
| SEO a AEO | titulek, popis, kanonická adresa, Open Graph a Twitter karta na každé stránce; JSON-LD (Festival, WebSite, MusicEvent, EducationEvent, SportsEvent, Event, Person, MusicGroup, SportsTeam, PerformingGroup, EventVenue, Place, FAQPage, Organization, BreadcrumbList); `sitemap.xml`, `robots.txt`, `llms.txt` |
| Styly | převod stylů prototypu na jeden vzhled bez variant (`web/css/style.css`) se zachováním váhy pravidel |
| Skript webu | `web/js/app.js`: funkce z prototypu nad předgenerovaným obsahem – filtry skrývají hotové karty, Můj program, kolize, hledání, „Právě teď“, odpočet, „Vrátit“, zpětný odkaz s filtry |
| Obrázky | obrázek pro sdílení 1200 × 630 px (PNG vykreslený v prohlížeči), ikona webu (SVG) |
| Testy | `tools/test_web.js` (157 stránek, metadata, odkazy, scénáře, stav bez JavaScriptu); `tools/test_accessibility.js` umí testovat `web/` |
| Rešerše | vyhledání aktuálních doporučení a trendů v UX a designu, výběr zdrojů, porovnání s webem |
| Dokumenty | `progress-03.md`, specifikace 1.2 (nové adresy detailů, spodní lišta, obnovená kapitola 8), plán |

## 3. Rozhodnutí, která AI navrhla

| Rozhodnutí | Zdůvodnění AI | Stav |
|---|---|---|
| Předgenerované stránky místo šablony s `?id=` | Obsah v HTML je čitelný pro vyhledávače a nástroje AI a zobrazí se bez JavaScriptu; web přitom dál běží ze souboru bez serveru | schválil uživatel |
| Adresy podle `slug` z `data.json` | Čitelné a stabilní; slugy jsou v datech jedinečné a kontroluje je skript | – |
| Data pro funkce dál v `js/data.js` na každé stránce | Můj program, hledání a „Právě teď“ potřebují data o všech položkách; `fetch()` ze souboru nefunguje | – |
| Titulek detailu položky s dnem a časem | Řeší shodu titulku vystoupení sólového umělce s titulkem jeho profilu | – |
| `hledani.html` a `muj-program.html` mimo mapu webu, hledání zakázané v `robots.txt` | Nemají vlastní obsah, jen výsledek akce uživatele | – |
| Třída `js` nastavená skriptem v `<head>` | Ovládání, které bez JavaScriptu nic nedělá, se bez něj nezobrazí, a se skriptem se neobjeví až se zpožděním | – |

## 4. Jak byl výstup ověřen

| Kontrola | Postup | Výsledek |
|---|---|---|
| Web | `tools/test_web.js` v Chrome: všech 157 stránek (odkazy, obrázky, metadata, JSON-LD, jedinečné titulky), 11 stránek × 2 šířky, scénáře S1–S5, stav bez JavaScriptu, filtr účinkujících, „Vrátit“, odkaz přeskočit na obsah, menu | 125 kontrol, všechny prošly |
| Přístupnost | `tools/test_accessibility.js` na `web/`: axe-core WCAG 2.0/2.1/2.2 A a AA (12 stránek a stavů × 2 šířky), klávesnice, šířka 320 px, omezený pohyb | 45 kontrol, všechny prošly |
| Shoda vzhledu s prototypem | snímky všech stránek prototypu a webu na 360 a 1280 px porovnány po pixelech | shodné až na drobné rozdíly ve vyhlazení písma |
| Data | `python3 tools/validate_data.py` včetně shody `web/js/data.js` s `data.json` | 0 chyb |
| Rešerše | každé doporučení v `progress-03.md` má odkaz na zdroj; tvrzení, která uváděl jen jeden zdroj nebo jen reklamní text (např. procenta úspory energie v tmavém režimu), nebyla převzata | – |

Strojové kontroly neověřují validitu HTML podle W3C, chování se skutečnou čtečkou obrazovky ani použitelnost s lidmi. Validátor W3C (vnu.jar) se nepodařilo spustit, protože stažení a spuštění programu z internetu nebylo v tomto prostředí povoleno.

## 5. Zjištěné limity a chyby

- **Změna vzhledu při převodu stylů.** První převod stylů bez variant změnil vzhled 24 stránek, protože pravidla zvoleného vzhledu ztratila váhu (specificitu). Odhalilo to porovnání snímků po pixelech; opraveno nahrazením atributu varianty selektorem `:root`.
- **Duplicitní titulky.** Detail vystoupení sólového umělce měl stejný titulek jako jeho profil. Odhalil to test; titulek detailu teď obsahuje den a čas.
- **Chybný test.** Test čekal u filtru účinkujících 6 výsledků místo skutečných 5. Chyba byla v testu, ne na webu.
- **Ovládání bez funkce.** Bez JavaScriptu byly vidět filtry a tlačítka uložit, která nic nedělala. Odhaleno kontrolou stránek bez JavaScriptu; opraveno a přidáno do testu.
- **Neověřené číslo v návrhu textu.** Do návrhu `progress-03.md` AI napsala, že web je o 30 % menší, aniž by to změřila; dále chybně uvedla barvu pozadí a že web nabízí rezervaci na místě. Před předáním opraveno podle skutečných souborů (styly 58 kB → 49 kB, pozadí #090b12, detail workshopu odkazuje na rezervaci na webu, která zatím chybí).
- **Chybějící kapitola specifikace.** Kapitola 8 specifikace (změny oproti verzi 1.0), na kterou odkazují `progress-02.md` a prezentace iterace 2, nebyla v odevzdané verzi souboru. Obnovena ve verzi 1.2.
