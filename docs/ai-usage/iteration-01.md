# Použití AI – iterace 1: Projektová specifikace a datová základna

| | |
|---|---|
| **Období** | 13. 10. 2026 |
| **Výstupy iterace** | `project-specification.md`, `data.json`, `tools/validate_data.py`, `docs/plan.md`, prezentace a texty pro mluvčí v `docs/presentation/iteration-01/` |
| **Odevzdání** | cvičení 2 |

Tento soubor popisuje jen to, co udělala a strojově zkontrolovala AI. Co udělal a zkontroloval tým, je v `docs/team-work-flow/iteration-01.md` a v kontrolním listu `docs/team-work-flow/controls/iteration-01.md`. Tvrzení „ověřili jsme pomocí AI“ se jako validace nepočítá.

## 1. Použité nástroje

| Nástroj | Verze / model | K čemu |
|---|---|---|
| Claude Code (rozšíření pro VS Code) | Claude Opus 5.5 | návrh konceptu, texty, data, kontrolní skript, plán projektu |
| Python | 3.10 (jen standardní knihovna) | kontrola konzistence dat, sestavení prezentace |
| Microsoft PowerPoint | pro macOS | otevření vygenerované prezentace a export do PDF kvůli vizuální kontrole |

## 2. K čemu byla AI použita

| Oblast | Co AI vytvořila |
|---|---|
| Koncept festivalu | název Tranzistor, slogan, lokalita, termín, pět scén, sedm témat, devět formátů programu |
| Specifikace | účel webu, pět cílových skupin, sitemap, navigace, vztahy mezi částmi, pět scénářů (tři klíčové) |
| Datová základna | 67 účinkujících (jména, charakteristiky, medailonky), 77 položek programu (názvy, popisy, štítky, časy), praktické informace (vstupenky, doprava, přístupnost, služby, časté dotazy, pravidla) |
| Nástroje | skript `tools/validate_data.py` pro kontrolu konzistence dat |
| Organizace | plán celého projektu v `docs/plan.md`, kontrolní list a seznam úkolů pro tým v `docs/team-work-flow/` |
| Prezentace | devět snímků v šabloně KIT (`tranzistor-iterace-01.odp`), skript `tools/build_presentation.py`, který je sestavuje, a texty pro čtyři mluvčí |

## 3. Zadání (prompty)

**Prompt 1** (v angličtině, s přiloženým úplným textem požadavků z Moodlu):

> Hi, we need to create a study project for the university. We have done something simmilar in the PEF_CZU_ZJ/festival. For now the main theme is tech festival. _[vložené zadání z Moodlu]_ Pls safe the how used AI to the folder docs for each itteration. For now let's plan (md in the docs as well) the whole project and after let's do the first itteration to submit pls.

**Prompt 2:**

> Ok, extract the TYM parts to docs/team-work-flow and control from the team parts from all md files to the docs/team-work-flow/controls and make it for each file itteration. Now it's first itteration. After that pls make a presentation for 4 people. YOu can use @16-9_blue_cze.odp as tempalte for presentation + for each the czech text presentation file. All in docs/presentation/itteration-n pls. After we will done all of that i want you to provide advisory review

AI si jako kontext přečetla dřívější projekt týmu ve složce `PEF_CZU_ZJ/festival` (specifikaci a strukturu dat hudebního festivalu). Z něj převzala pouze konvenci identifikátorů (`v…`, `p…`, `e…`) a jazyk výstupů. Koncept, obsah i formát dat jsou nové.

## 4. Rozhodnutí, která AI udělala sama

Zadání určilo pouze téma „tech festival“. Následující volby jsou návrhem AI a tým je má potvrdit, nebo změnit:

| Rozhodnutí | Zdůvodnění AI |
|---|---|
| Název Tranzistor, 3. ročník, Pražská tržnice, 4.–6. 6. 2027 | Krátký název srozumitelný česky i anglicky; reálné místo s halami a nábřežím odpovídá pěti scénám; termín je pátek až neděle. |
| Formát JSON místo XML | Web je čistě klientský a JSON lze v JavaScriptu použít bez převodu. |
| Pět scén a sedm témat místo minima dvou scén | Různorodý program dává smysl filtrům a osobnímu programu, které budou hlavními interaktivními funkcemi. |
| Odkazy v doméně `.example` | Vyhrazená doména, která nemůže patřit skutečnému subjektu. |
| Žádné obrázky v této verzi dat | Alternativní text má popisovat skutečný obrázek, a ty zatím neexistují. |
| Finalisté turnaje nejsou v datech uvedeni | Finále vzejde ze semifinále; u položky je uveden pouze komentátor. |
| Plán v angličtině, výstupy v češtině | Stejně jako v předchozím projektu týmu. |

## 5. Jak byl výstup ověřen

### 5.1 Strojové kontroly

| Kontrola | Postup | Výsledek |
|---|---|---|
| Konzistence dat | `python3 tools/validate_data.py` – jedinečnost ID a slugů, platnost všech vazeb, kolize na scéně, kolize účinkujících, provozní doba, den v týdnu, časové pásmo, kapacity, minimální rozsah | 0 chyb, 0 upozornění |
| Spolehlivost kontrolního skriptu | Do kopie dat bylo postupně vloženo 14 různých chyb (překryv na scéně, dvojí obsazení účinkujícího, neexistující scéna, duplicitní ID, špatný den v týdnu, program po zavírací době, překročená kapacita, 59 položek místo 60 a další) | Skript odhalil všech 14 |
| Kalendář | Výpočet dne v týdnu pro 4.–6. 6. 2027 v Pythonu | pátek, sobota, neděle – souhlasí |
| Shoda specifikace s daty | Všech 25 identifikátorů uvedených ve specifikaci bylo vyhledáno v `data.json`; počty ve scénářích (6 položek na Nábřeží v sobotu, 9 rodinných položek v neděli, kolize e039 × e043, ceny vstupenek) byly přepočítány skriptem | Vše souhlasí |

Prezentace byla zkontrolována takto: vygenerovaný soubor `.odp` byl otevřen v aplikaci Microsoft PowerPoint, vyexportován do PDF a všech devět snímků bylo prohlédnuto (šablona se načetla, text nepřetéká a nezasahuje do zápatí). V LibreOffice soubor otevřen nebyl. Délka textů pro mluvčí byla spočítána: 512 slov, tedy asi 4 až 4,7 minuty.

Tyto kontroly ověřují strukturu a vnitřní soulad. Neověřují kvalitu textů, věcnou správnost ani vhodnost obsahu.

### 5.2 Ruční kontrola

Ruční kontroly provádí tým podle kontrolního listu `docs/team-work-flow/controls/iteration-01.md` (K1–K9). AI je neprovedla a nemůže je nahradit.

## 6. Co tým přijal, upravil a odmítl

Zapisuje tým do `docs/team-work-flow/iteration-01.md`, kapitoly 2 a 3.

## 7. Zjištěné limity a chyby

- **Jména.** AI neumí zaručit, že vymyšlené jméno nenosí skutečný člověk nebo kapela. Jména je nutné vyhledat ručně.
- **Údaje o skutečném místě.** Adresa, zastávka „Pražská tržnice“, stanice metra Vltavská a nádraží Praha-Holešovice jsou uvedeny z paměti modelu, nebyly ověřeny u zdroje. Čísla tramvajových linek AI záměrně neuvedla, protože se mění.
- **Rozmístění scén.** Zóny areálu (Severní hala, Pasáž, Nábřežní louka a další) jsou smyšlené a neodpovídají skutečnému plánu tržnice. V datech je to uvedeno v poznámce.
- **Ceny a kapacity** jsou odhad bez podkladu v reálných datech.
- **Styl textů.** Medailonky mají podobnou délku a stavbu vět, což může působit jednotvárně.
- **Úprava původního návrhu během práce.** V první verzi programu byla v pátečním panelu o AI ve škole italská řečnice, ačkoli panel probíhá česky. AI ji před vygenerováním dat nahradila českým lektorem. Turnaj měl původně tři týmy, s nimiž nevychází semifinále; AI doplnila čtvrtý.
- **Tvrzení o kontrole týmem.** První verze poznámky v datech uváděla, že texty „zkontroloval tým“, přestože kontrola ještě neproběhla. Formulace byla opravena na „za obsah odpovídá tým“.
- **Šablona prezentace.** V šabloně jsou obrázky pozadí jen na hlavních předlohách, ne na rozloženích, která snímky používají. PowerPoint si je doplní, u LibreOffice to AI ověřit nemohla. Proto je přiložen i export do PDF.
- **Délka textů pro mluvčí.** První verze textů měla 654 slov, což je pět až šest minut, tedy nad limit. AI je zkrátila na 512 slov.
- **Nepodložená tvrzení v textech pro mluvčí.** První verze uváděla, že kolizi ve scénáři S2 tým „nechal v datech záměrně“ a že jména a údaje o místě „jsme ověřovali sami“. Ani jedno neodpovídalo skutečnosti a AI formulace opravila.

Limity a chyby, které našel tým, se zapisují do `docs/team-work-flow/iteration-01.md`, kapitola 4.
