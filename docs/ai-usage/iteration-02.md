# Použití AI – iterace 2: UX návrh, prototyp a funkce

| | |
|---|---|
| **Období** | 8. 11. 2026 |
| **Výstupy iterace** | `prototype/`, `progress-02.md`, `data.json` 1.1.0, `project-specification.md` 1.1, stránka pro výběr vzhledu (`docs/design-picker/iteration-02/`), prezentace a texty pro mluvčí (`docs/presentation/iteration-02/`), nástroje `tools/build_web_data.py`, `tools/generate_images.py`, `tools/build_picker.py`, `tools/test_prototype.js` |
| **Odevzdání** | cvičení 3 |

Tento soubor popisuje jen to, co udělala a strojově zkontrolovala AI. Co udělal a zkontroloval tým, je v `docs/team-work-flow/iteration-02.md` a v kontrolním listu `docs/team-work-flow/controls/iteration-02.md`.

## 1. Použité nástroje

| Nástroj | Verze / model | K čemu |
|---|---|---|
| Claude Code (rozšíření pro VS Code) | Claude Opus 5.5 | prototyp, oprava dat, ilustrace, stránka pro výběr vzhledu, testy, dokumenty |
| Python | 3.9 (jen standardní knihovna) | kontrola dat, odvození `js/data.js`, generování ilustrací, sestavení prezentace a stránky pro výběr |
| Google Chrome + playwright-core | 1.48.2 (jen pro test, není součástí projektu) | automatický test prototypu, snímky obrazovky |
| Microsoft PowerPoint | pro macOS | otevření prezentace a export do PDF kvůli kontrole |
| Artifact na claude.ai | – | sdílená stránka pro hlasování o vzhledu |

## 2. K čemu byla AI použita

| Oblast | Co AI vytvořila |
|---|---|
| Oprava dat | nalezení pěti mezer v `data.json` porovnáním se zadáním a specifikací; doplnění obrázků, schématu areálu, historie, kontaktu pro média, odkazu na vstupenky a témat tří panelistů; verze 1.1.0 |
| Kontrolní skript | nová pravidla: obrázky, poloha scén, historie ročníků, shoda témat účinkujícího s jeho vystoupeními, shoda `js/data.js` s `data.json`, existence souborů obrázků |
| Prototyp | 11 stránek, jeden soubor stylů, jeden skript; filtry, Můj program, kolize, vyhledávání, „Právě teď“, filtr účinkujících; přepínání variant vzhledu |
| Ilustrace | 74 souborů SVG: úvodní ilustrace, schéma areálu kreslené z dat, 5 scén, 67 abstraktních portrétů s monogramem |
| Posouzení prototypu člena týmu | otevření v prohlížeči, porovnání se zadáním a s daty, seznam převzatých a nepřevzatých prvků |
| Stránka pro výběr vzhledu | 4 rozhodnutí, 10 variant s živými náhledy, sdílené hlasování, souhrn |
| Úprava vzhledu po hlasování | ikony SVG ve stylu Material Icons, počet v rohu ikony, dotažený tmavý vzhled, ilustrace v nové paletě |
| Druhé kolo výběru vzhledu | stránka s 8 rozhodnutími o komponentách a pohybu (24 variant s živými náhledy), varianty v prototypu, po rozhodnutí sjednocení do společných pravidel pro karty, skládací bloky, seznamy, tabulky a fakta v detailu |
| Kontrola přístupnosti | skript `tools/test_accessibility.js` (axe-core, klávesnice, reflow, omezený pohyb), opravy: zakrytý fokus, fokus pole hledání, název odznaku pro čtečku, duplicitní orientační body, kontrast animovaného úvodu |
| Odstranění zmínek o projektu | texty o studijním projektu, prototypu a fiktivních odkazech odstraněny z webu; adresy festivalu v doméně tranzistor-festival.cz (ověřeno, že není registrovaná) |
| Redesign po kontrole stránek na telefonu | nadpisové písmo Chakra Petch (OFL, uložené lokálně), nový úvod, přepínač dnů v programu, záhlaví detailu, kompaktní seznamy účinkujících a souběžného programu, vstupenky jako karty na telefonu, dvousloupcový desktop |
| Dokumenty | `progress-02.md`, změny ve specifikaci, plán, prezentace, texty pro mluvčí, kontrolní list |

## 3. Rozhodnutí, která AI udělala sama

| Rozhodnutí | Zdůvodnění AI |
|---|---|
| Co v datech chybělo | Zpětná vazba neříkala co. AI porovnala pole v `data.json` s tím, co specifikace slibuje zobrazit, a s požadavkem zadání na obrázky od AI. |
| Ilustrace jako SVG napsané kódem | V prostředí nebyl dostupný generátor obrázků. Vektorová kresba je malá, ostrá a funguje bez internetu. Portréty jsou abstraktní, aby nepředstíraly skutečné lidi. |
| Data pro web v `js/data.js` | Prohlížeč nedovolí stránce otevřené ze souboru načíst `data.json` přes `fetch()`; prototyp člena týmu kvůli tomu zobrazoval jen část dat. |
| Klasický skript místo modulů | `<script type="module">` se ze souboru také nenačte. |
| Stránky skládané z jedné šablony | Záhlaví a zápatí jsou na 11 stránkách stejné. Výsledkem jsou obyčejné statické soubory HTML. |
| Ikony podle Material Icons | Uživatel chtěl ikony „podobné MUI“. Tvary jsou z Material Icons (Apache License 2.0), vložené jako SVG, bez knihovny a bez internetu. |

## 4. Jak byl výstup ověřen

| Kontrola | Postup | Výsledek |
|---|---|---|
| Data | `python3 tools/validate_data.py` | 0 chyb; na původních datech 1.0.0 hlásí 83 chyb |
| Prototyp | `tools/test_prototype.js` v Chrome: 11 stránek × 2 šířky, scénáře S1–S5, klávesnice, menu, spodní lišta, varianty | 190 kontrol, všechny prošly; přístupnost 45 kontrol, všechny prošly |
| Kontrast tmavého vzhledu | výpočet podle WCAG pro 23 dvojic barev | vše AA, nejnižší 7,4 : 1 |
| Vzhled | prohlédnutí snímků obrazovky na mobilu (360 a 390 px) a desktopu (1280 px) | nálezy opraveny, viz kapitola 7 |
| Prototyp člena týmu | otevřen ze souboru v Chrome, spočítány zobrazené položky, porovnána ID s daty | `fetch` selže, zobrazí 16 ze 77 položek a 20 ze 67 účinkujících; ID souhlasí |
| Stránka pro výběr | otevřena lokálně na šířce telefonu i desktopu, výběr vyzkoušen; po zveřejnění přečten uložený hlas ze sdíleného úložiště | funguje, jeden uložený hlas |
| Prezentace | otevřena v PowerPointu, export do PDF, prohlédnuto všech 9 snímků | text nepřetéká, obrázky jsou vložené |

Strojové kontroly neověřují validitu HTML podle W3C, chování se čtečkou obrazovky ani použitelnost s lidmi. To je v kontrolním listu týmu.

## 5. Co tým přijal, upravil a odmítl

Zapisuje tým do `docs/team-work-flow/iteration-02.md`. Z hlasování je zřejmé, že u barevného směru a karty programu tým doporučení AI nepřijal (AI doporučila Signál a časovou osu, zvolen byl Kyber a dlaždice).

## 6. Zjištěné limity a chyby

- **Přetečení záhlaví.** První verze záhlaví se na telefonu o šířce 360 px nevešla o 67 px. Odhalil to test, opraveno zkrácením „Můj program“ na ikonu s počtem.
- **Chyba z příkazové řádky.** Při jedné úpravě skriptu shell nahradil část kódu (`$(…)`), skript přestal fungovat na všech stránkách. Odhalil to test (chyba v konzoli), opraveno.
- **Ztracené barvy témat.** Ve variantě Kyber přebilo obecné pravidlo barvy štítků témat. Odhaleno na snímku obrazovky.
- **Chybný test.** Test čekal skrytý odznak s nulou v okamžiku, kdy byly uložené tři položky. Chyba byla v testu, ne v prototypu.
- **Nepodložené tvrzení o prototypu člena týmu.** AI nejprve uživateli napsala, že záložní data v jeho prototypu mají špatná ID. Porovnáním s `data.json` se ukázalo, že ID souhlasí; skutečným problémem je jen neúplná kopie dat. Do dokumentů se chybné tvrzení nedostalo.
- **Vymyšlené zdůvodnění týmu.** Při psaní `progress-02.md` AI doplnila důvody, proč tým zvolil Kyber a dlaždice, ačkoli je tým neuvedl. Opraveno na místo k doplnění.
- **Ilustrace nejsou portréty.** Abstraktní monogramy nesplní očekávání fotografií účinkujících; pro finální web by tým mohl vygenerovat portréty generátorem obrázků.
- **Obsah vykreslovaný skriptem.** Detailní stránky plní JavaScript, což je slabší pro vyhledávače. Řešení patří do iterace 3 spolu se SEO.

Limity a chyby, které našel tým, se zapisují do `docs/team-work-flow/iteration-02.md`, kapitola 4.
