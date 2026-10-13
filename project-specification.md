# Projektová specifikace – Tranzistor 2027

|                     |                                 |
| ------------------- | ------------------------------- |
| **Tým**             | sk101                           |
| **Členové**         | _doplnit jména čtyř členů týmu_ |
| **Verze dokumentu** | 1.0                             |
| **Datová základna** | `data.json`, verze 1.0.0        |

Festival, všichni účinkující i program jsou fiktivní. Texty v této specifikaci a v datové základně byly vygenerovány AI, za výsledek odpovídá tým (viz kapitola 7).

---

## 1. Identita festivalu

| Položka                 | Hodnota                                                                                                                                                                                                                                  |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Název**               | Tranzistor – festival technologií, her a digitální kultury                                                                                                                                                                               |
| **Slogan**              | Zapoj se.                                                                                                                                                                                                                                |
| **Ročník**              | 3. ročník (první ročník proběhl v roce 2025)                                                                                                                                                                                             |
| **Lokalita**            | Pražská tržnice, Bubenské nábřeží 306/13, 170 00 Praha 7 – Holešovice                                                                                                                                                                    |
| **Datumový rozsah**     | pátek 4. 6. – neděle 6. 6. 2027 (3 dny)                                                                                                                                                                                                  |
| **Charakter festivalu** | Multižánrový městský festival: přes den odborné přednášky, praktické workshopy a herní turnaj, večer elektronická hudba a audiovizuální show. Pět scén v jednom areálu, čtyři kryté a jedna venkovní. Očekávaná návštěvnost 12 000 lidí. |
| **Hlavní témata**       | AI a data · Web a vývoj · Hardware a robotika · Bezpečnost a soukromí · Hry a e-sport · Digitální umění a hudba · Technologie a společnost                                                                                               |
| **Formáty programu**    | hlavní přednáška, přednáška, panelová diskuse, workshop, koncert, live coding, performance, turnaj, herna a show                                                                                                                         |
| **Jazyk webu**          | čeština                                                                                                                                                                                                                                  |

Tranzistor není kopií existujícího festivalu. Kombinuje prvky technologické konference, maker festivalu, herní akce a hudebního festivalu, které se běžně konají odděleně. Právě proto potřebuje web, který pomůže návštěvníkovi vybrat si z velmi různorodého programu.

### Scény

| ID  | Scéna         | Typ                             | Kapacita | Zaměření                                      |
| --- | ------------- | ------------------------------- | -------- | --------------------------------------------- |
| v01 | **Mainframe** | hlavní sál (krytý)              | 1 800    | hlavní přednášky, panely, večerní koncerty    |
| v02 | **Terminal**  | přednáškový sál (krytý)         | 450      | odborné přednášky a diskuse                   |
| v03 | **Sandbox**   | workshopová dílna (krytá)       | 60       | praktické workshopy s rezervací               |
| v04 | **Arcade**    | herní a e-sportová zóna (krytá) | 350      | turnaj Tranzistor Cup, nezávislé hry, retro   |
| v05 | **Nábřeží**   | venkovní scéna u Vltavy         | 2 500    | koncerty, live coding, performance (do 22:00) |

---

## 2. Účel webu

### K čemu web slouží

Web je hlavním informačním zdrojem festivalu před akcí i během ní. Program má 77 položek na pěti scénách, které často běží souběžně, a oslovuje velmi odlišné publikum – od vývojářů po rodiny s dětmi. Web má návštěvníkovi umožnit rychle najít to, co je pro něj relevantní, a sestavit si z toho vlastní plán.

### Hlavní cíle

1. **Orientace v programu** – umožnit zúžit 77 položek podle dne, scény, tématu, formátu, úrovně a jazyka na několik relevantních.
2. **Plánování návštěvy** – dát uživateli nástroj, kterým si sestaví osobní program a včas odhalí časové kolize.
3. **Představení účinkujících** – u každého z 67 účinkujících ukázat, kdo to je, kdy a kde vystupuje.
4. **Praktická příprava** – na jednom místě odpovědět na otázky „kolik to stojí, jak se tam dostanu, je to bezbariérové, můžu vzít děti“.
5. **Podpora na místě** – na mobilu rychle ukázat, co právě běží a co začne za chvíli.
6. **Dohledatelnost** – obsah strukturovat tak, aby mu rozuměly vyhledávače i AI asistenti (sémantické HTML, metadata, strukturovaná data).

### Důležité akce uživatelů

| Akce                                                                                       | Kde na webu                                                                                                       |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| Filtrovat program podle dne, scény, tématu, formátu, úrovně, jazyka a vhodnosti pro rodiny | Program                                                                                                           |
| Uložit položku programu do osobního plánu a zase ji odebrat                                | Program, detail položky, detail účinkujícího                                                                      |
| Zkontrolovat osobní plán a vyřešit časové kolize                                           | Můj program                                                                                                       |
| Vyhledat účinkujícího, položku programu nebo scénu podle části názvu                       | vyhledávací pole v záhlaví, stránka výsledků                                                                      |
| Zobrazit detail účinkujícího včetně všech jeho vystoupení                                  | Účinkující                                                                                                        |
| Zjistit, co na které scéně právě běží                                                      | Úvod, Scény                                                                                                       |
| Najít cenu vstupenky, dopravu a informace o přístupnosti                                   | Praktické informace                                                                                               |
| Přejít k nákupu vstupenky                                                                  | výzva k akci na úvodní stránce a v praktických informacích (nákup je v projektu pouze naznačen, web nemá backend) |

---

## 3. Cílové skupiny

| Skupina                                                                                                 | Potřeby                                                                                                             | Očekávání                                                                     | Informace a funkce na webu                                                                                                    |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **A. Technologičtí nadšenci a studenti** (18–30 let, hlavně mobil)                                      | Projít celý program, vybrat si napříč tématy, nepřijít o nic zajímavého, ušetřit.                                   | Rychlý přehled, moderní ovládání, funguje i na pomalém připojení.             | Filtr programu, Můj program s upozorněním na kolize, studentská vstupenka, „Právě teď“.                                       |
| **B. Profesionálové z oboru** (vývojáři, designéři, bezpečnostní specialisté; 25–45 let, často desktop) | Najít odborné přednášky ve svém oboru a na své úrovni, ověřit si, kdo přednáší, obhájit účast před zaměstnavatelem. | Přesné a úplné údaje: téma, úroveň, jazyk, délka, medailonek řečníka.         | Filtr podle tématu, úrovně a jazyka, detail účinkujícího se všemi vystoupeními, vyhledávání podle jména.                      |
| **C. Rodiny s dětmi a školní skupiny** (rodiče 30–45 let, učitelé)                                      | Zjistit, co je vhodné pro děti, kolik to stojí, jak se dostat na místo a jestli je potřeba rezervace.               | Srozumitelný jazyk bez žargonu, jasné odpovědi, jistota bezpečného prostředí. | Označení „vhodné pro rodiny“, přehled rodinné neděle, kapacita a rezervace workshopů, vstupenky, doprava, dětský koutek, FAQ. |
| **D. Večerní návštěvníci – fanoušci hudby a her** (18–35 let, mobil)                                    | Vědět, kdo hraje večer, kdy začíná hlavní koncert a kdy je turnaj.                                                  | Program podle scény a času, minimum kroků.                                    | Filtr podle scény a formátu, detail scény s programem, večerní vstupenka.                                                     |
| **E. Návštěvníci se specifickými potřebami** (prolíná se všemi skupinami)                               | Ověřit bezbariérovost, tlumočení, klidovou místnost; ovládat web klávesnicí nebo čtečkou obrazovky.                 | Konkrétní informace u každé scény, ne obecné prohlášení.                      | Přístupnost u každé scény, sekce Přístupnost v praktických informacích, web splňující WCAG AA.                                |

Vedlejší skupinou jsou média a partneři, kteří hledají základní údaje o festivalu a kontakt na pořadatele (stránka O festivalu).

---

## 4. Informační architektura

### 4.1 Struktura webu (sitemap)

```
Úvod (index.html)
├── Program (program.html)
│   └── Detail položky programu (udalost.html?id=…)
├── Účinkující (ucinkujici.html)
│   └── Detail účinkujícího (ucinkujici-detail.html?id=…)
├── Scény (sceny.html)
│   └── Detail scény (scena.html?id=…)
├── Můj program (muj-program.html)
├── Praktické informace (prakticke-informace.html)
│   ├── #vstupenky
│   ├── #doprava
│   ├── #pristupnost
│   ├── #sluzby
│   ├── #pravidla
│   └── #caste-dotazy
├── O festivalu (o-festivalu.html)
└── Výsledky vyhledávání (hledani.html?q=…)
```

Web má nejvýše tři úrovně. Každá stránka druhé a třetí úrovně má drobečkovou navigaci (například _Úvod › Účinkující › Kristýna Malátová_).

### 4.2 Hlavní navigace

| Prvek                   | Obsah                                                                                                                                   |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Záhlaví**             | logo (odkaz na Úvod) · Program · Účinkující · Scény · Praktické informace · Můj program (s počtem uložených položek) · vyhledávací pole |
| **Mobilní zobrazení**   | logo, vyhledávání a Můj program zůstávají viditelné, ostatní položky jsou ve sbalitelné nabídce                                         |
| **Drobečková navigace** | na všech stránkách kromě úvodní                                                                                                         |
| **Zápatí**              | O festivalu · Vstupenky · Přístupnost · Časté dotazy · kontakt na pořadatele · sociální sítě                                            |
| **Kontextové odkazy**   | položka programu ↔ účinkující ↔ scéna (viz 4.3)                                                                                         |

Pořadí položek odpovídá nejčastějším úkolům: nejdřív „co a kdy“ (Program), potom „kdo“ (Účinkující), „kde“ (Scény) a „jak“ (Praktické informace).

### 4.3 Vztahy mezi hlavními částmi

```
   Den ◄──── 1 ──── Položka programu ──── 1 ────► Scéna
                      │            │
                    1 │            │ 1..5
                      ▼            ▼
                    Téma ◄────── Účinkující
                          1..n

   Můj program ──── 0..n ────► Položka programu   (uloženo v prohlížeči uživatele)
   Vstupenka   ──── 1..3 ────► Den
```

- **Položka programu** má právě jeden den, jednu scénu, jedno téma a jeden formát a jednoho až pět účinkujících. Z jejího detailu vedou odkazy na všechny tyto entity.
- **Účinkující** má jedno až čtyři vystoupení. Detail účinkujícího je všechna vypisuje s časem a scénou.
- **Scéna** zobrazuje svůj program po dnech a informace o přístupnosti.
- **Můj program** je výběr položek programu uložený v prohlížeči (bez registrace). Položku lze přidat z programu, z detailu položky i z detailu účinkujícího.
- **Praktické informace** odkazují na scény (přístupnost, rezervace workshopů ve scéně Sandbox) a na dny (platnost vstupenek).
- **Vyhledávání** prohledává účinkující, položky programu a scény a výsledky zobrazuje ve skupinách podle typu.

### 4.4 Účel jednotlivých částí

| Část                        | Účel                                                     | Hlavní obsah                                                                                                                                                                                               |
| --------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Úvod**                    | Představit festival a nasměrovat uživatele k jeho úkolu. | Název, termín, místo, krátké představení, hlavní hvězdy, blok „Právě teď / Nejbližší program“, rozcestník podle témat, vstupenky.                                                                          |
| **Program**                 | Umožnit najít relevantní položky a uložit si je.         | Seznam položek po dnech v časovém pořadí, filtry (den, scéna, téma, formát, úroveň, jazyk, vhodné pro rodiny), tlačítko pro uložení. Stav filtrů je v adrese stránky, aby šel sdílet a přežil návrat zpět. |
| **Detail položky programu** | Dát úplnou informaci o jedné položce.                    | Název, čas, scéna, formát, téma, úroveň, jazyk, popis, účinkující, kapacita a rezervace, uložení do Mého programu, souběžný program na jiných scénách.                                                     |
| **Účinkující**              | Přehled všech 67 účinkujících.                           | Karty se jménem, typem, zemí a tématem; filtr podle typu a tématu, řazení podle abecedy.                                                                                                                   |
| **Detail účinkujícího**     | Představit účinkujícího a jeho vystoupení.               | Medailonek, země, témata, seznam vystoupení s časem a scénou, uložení do Mého programu.                                                                                                                    |
| **Scény**                   | Orientace v areálu.                                      | Přehled pěti scén, schéma areálu, kapacita, zaměření, co na scéně právě běží.                                                                                                                              |
| **Detail scény**            | Program a vybavení jedné scény.                          | Popis, kapacita, vybavení, přístupnost, program scény po dnech.                                                                                                                                            |
| **Můj program**             | Osobní plán návštěvy.                                    | Uložené položky po dnech v časovém pořadí, upozornění na časové kolize, odebrání položky, prázdný stav s odkazem do programu.                                                                              |
| **Praktické informace**     | Odpovědět na organizační otázky.                         | Vstupenky a ceny, doprava, přístupnost, služby v areálu, pravidla, časté dotazy.                                                                                                                           |
| **O festivalu**             | Kontext a kontakt.                                       | Charakter festivalu, témata, historie ročníků, pořadatel, kontakt.                                                                                                                                         |
| **Výsledky vyhledávání**    | Najít obsah podle části názvu.                           | Výsledky ve skupinách (účinkující, program, scény), počet výsledků, stav „nic nenalezeno“ s návrhem dalšího postupu.                                                                                       |

### 4.5 Interaktivní části (předběžně)

Podrobný návrh bude součástí druhého výstupu. Ze scénářů v kapitole 5 vyplývají tyto funkce:

1. filtrování programu podle více kritérií současně,
2. Můj program s detekcí časových kolizí (uložení v prohlížeči),
3. vyhledávání bez ohledu na diakritiku a velikost písmen,
4. kontextový blok „Právě teď / Nejbližší program“ podle aktuálního času,
5. filtrování a řazení seznamu účinkujících.

---

## 5. Uživatelské scénáře

Scénáře S1–S3 jsou **klíčové**. Budou použity při prototypování, implementaci a ověřování. Scénáře S4 a S5 jsou doplňkové. U každého scénáře jsou uvedeny konkrétní položky z `data.json`, na kterých lze průchod ověřit.

### S1 – Večer na Nábřeží (klíčový)

|                        |                                                                                                                                                                                                                                                   |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Typ uživatele**      | Večerní návštěvník, fanoušek hudby (skupina D), mobilní telefon.                                                                                                                                                                                  |
| **Cíl**                | Zjistit, kdo v sobotu večer hraje na scéně Nábřeží, a uložit si vybraný koncert do svého programu.                                                                                                                                                |
| **Výchozí situace**    | Sobota odpoledne, uživatel jede tramvají na festival. Web otevírá poprvé na úvodní stránce. Nezná jména účinkujících ani rozložení scén.                                                                                                          |
| **Průchod**            | Úvod → Program → filtr _Den: Sobota_ a _Scéna: Nábřeží_ → seznam položek v časovém pořadí → detail koncertu _Šum a Signál_ → _Přidat do Mého programu_ → Můj program.                                                                             |
| **Očekávaný výsledek** | Uživatel vidí pouze šest sobotních položek scény Nábřeží seřazených podle času (14:00–22:00). Po uložení dostane potvrzení a počet položek u odkazu Můj program se zvýší. Koncert je v Mém programu i po zavření a opětovném otevření prohlížeče. |
| **Data pro ověření**   | e036, e040, e046, e050, e052 (Šum a Signál, 19:30–20:30), e054                                                                                                                                                                                    |

### S2 – Bezpečnost pro profesionálku (klíčový)

|                        |                                                                                                                                                                                                                                                                                                                        |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Typ uživatele**      | Vývojářka se zájmem o bezpečnost (skupina B), desktop, týden před festivalem.                                                                                                                                                                                                                                          |
| **Cíl**                | Sestavit si sobotní plán z tématu Bezpečnost a soukromí a zjistit více o řečnici, o které slyšela.                                                                                                                                                                                                                     |
| **Výchozí situace**    | Pamatuje si příjmení „Malátová“. Neví, kdy a kde řečnice vystupuje ani jaký další program se tématu věnuje.                                                                                                                                                                                                            |
| **Průchod**            | Vyhledávací pole → „malatova“ (bez diakritiky) → výsledky → detail účinkující Kristýny Malátové → uložení obou jejích vystoupení → Program → filtr _Téma: Bezpečnost a soukromí_ a _Den: Sobota_ → uložení workshopu _Capture the Flag pro začátečníky_ → Můj program → upozornění na kolizi → odebrání jedné položky. |
| **Očekávaný výsledek** | Vyhledávání najde účinkující i bez diakritiky. Detail účinkující uvádí medailonek a obě vystoupení s časem a scénou. Můj program řadí položky podle času a viditelně označí, že workshop (15:00–17:00, Sandbox) se překrývá s přednáškou (16:30–17:15, Mainframe). Po odebrání jedné z položek upozornění zmizí.       |
| **Data pro ověření**   | p022; e043 a e047 (vystoupení řečnice); e035, e039, e043, e047 (sobotní program tématu); kolize e039 × e043                                                                                                                                                                                                            |

### S3 – Rodinná neděle (klíčový)

|                        |                                                                                                                                                                                                                                                                                                                                                            |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Typ uživatele**      | Rodič dvou dětí ve věku 7 a 11 let (skupina C), mobilní telefon, večer doma. Na festivalu nikdy nebyl.                                                                                                                                                                                                                                                     |
| **Cíl**                | Rozhodnout se, zda v neděli s dětmi přijet: co je pro děti vhodné, zda je potřeba rezervace, kolik to bude stát a jak se na místo dostat.                                                                                                                                                                                                                  |
| **Výchozí situace**    | Uživatel přichází na úvodní stránku z odkazu od známých. Technologickým pojmům nerozumí a neví, že neděle je rodinný den.                                                                                                                                                                                                                                  |
| **Průchod**            | Úvod → Program → filtr _Den: Neděle_ a _Vhodné pro rodiny_ → detail _Rodinná dílna: světelný brouk_ → odkaz na scénu Sandbox → Praktické informace → Vstupenky → Doprava → Služby (dětský koutek).                                                                                                                                                         |
| **Očekávaný výsledek** | Uživatel do tří minut zjistí: které nedělní položky jsou vhodné pro děti (9 položek), že dílna je pro děti od 6 let, má 30 míst a vyžaduje rezervaci, že rodinná nedělní vstupenka stojí 1 490 Kč a děti do 12 let mají vstup zdarma, že u vstupu staví tramvaj a v areálu se neparkuje. Při návratu z detailu zpět do programu zůstanou filtry nastavené. |
| **Data pro ověření**   | e057 (dílna), dalších osm nedělních položek s `familyFriendly: true`; vstupenky tk05 a tk06; scéna v03                                                                                                                                                                                                                                                     |

### S4 – Co běží právě teď (doplňkový)

|                        |                                                                                                                                                                                                                |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Typ uživatele**      | Návštěvník v areálu (skupiny A a D), mobilní telefon, pomalé připojení.                                                                                                                                        |
| **Cíl**                | Zjistit, co právě běží a co začne v nejbližší hodině, a vybrat si, kam jít.                                                                                                                                    |
| **Výchozí situace**    | Skončila přednáška, uživatel stojí v hale a má hodinu volna. Otevře úvodní stránku webu.                                                                                                                       |
| **Očekávaný výsledek** | Úvodní stránka bez dalšího klikání ukáže pro každou scénu aktuální a následující položku s časem. Mimo dny festivalu blok zobrazí nejbližší program a datum zahájení. Pro účely testování lze čas nasimulovat. |

### S5 – Pamatuji si jen kousek názvu (doplňkový)

|                        |                                                                                                                                                                                                                                             |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Typ uživatele**      | Kdokoli; uživatel, kterému o vystoupení někdo vyprávěl.                                                                                                                                                                                     |
| **Cíl**                | Najít vystoupení, ze kterého si pamatuje jen slovo „tiskáren“.                                                                                                                                                                              |
| **Výchozí situace**    | Uživatel je na libovolné stránce webu a nezná název účinkujícího, den ani scénu.                                                                                                                                                            |
| **Očekávaný výsledek** | Po zadání „tiskaren“ stránka výsledků zobrazí účinkujícího _Orchestr Rozbitých Tiskáren_ a jeho vystoupení (e022), rozdělené do skupin podle typu výsledku. Při dotazu bez výsledků se zobrazí srozumitelná zpráva a odkaz na celý program. |

---

## 6. Datová základna (`data.json`)

### Formát

Zvolili jsme **JSON**: web je čistě klientský a JSON lze v JavaScriptu použít bez převodu. Soubor pro web (`web/js/data.js`) bude z `data.json` odvozen strojově, aby web fungoval i po otevření ze souborového systému bez serveru.

### Rozsah

| Entita           | Počet | Minimum ze zadání |
| ---------------- | ----- | ----------------- |
| Dny              | 3     | 3                 |
| Scény            | 5     | 2                 |
| Účinkující       | 67    | 60                |
| Položky programu | 77    | 60                |
| Témata           | 7     | –                 |
| Typy vstupenek   | 6     | –                 |

Program podle dnů: pátek 24, sobota 31, neděle 22 položek. Podle scény: Mainframe 20, Terminal 20, Sandbox 10, Arcade 12, Nábřeží 15. Účinkující pocházejí z 19 zemí; 18 položek je označeno jako vhodné pro rodiny a 10 workshopů vyžaduje rezervaci.

### Entity a vazby

| Klíč v JSON                                                        | Entita              | Identifikátor             | Hlavní atributy                                                                                            | Vazby                                                                           |
| ------------------------------------------------------------------ | ------------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| `festival`                                                         | Festival            | `tranzistor-2027`         | název, slogan, ročník, termín, charakter, popis, adresa, pořadatel                                         | –                                                                               |
| `days`                                                             | Den                 | `d1`–`d3`                 | datum, den v týdnu, provozní doba, téma dne                                                                | –                                                                               |
| `venues`                                                           | Scéna               | `v01`–`v05`               | název, typ, kapacita, zóna areálu, vybavení, přístupnost                                                   | –                                                                               |
| `tracks`                                                           | Téma                | `t01`–`t07`               | název, popis                                                                                               | –                                                                               |
| `performers`                                                       | Účinkující          | `p001`–`p067`             | jméno, typ, země, charakteristika, medailonek, hlavní hvězda                                               | `trackIds` → témata                                                             |
| `events`                                                           | Položka programu    | `e001`–`e077`             | název, formát, začátek, konec, délka, jazyk, úroveň, popis, štítky, vhodné pro rodiny, rezervace, kapacita | `dayId` → den, `venueId` → scéna, `trackId` → téma, `performerIds` → účinkující |
| `practical`                                                        | Praktické informace | `tk01`–`tk06` u vstupenek | vstupenky, doprava, přístupnost, služby, časté dotazy, pravidla                                            | `validDayIds` → dny                                                             |
| `eventTypes`, `performerTypes`, `levels`, `languages`, `countries` | Číselníky           | kód                       | český popisek                                                                                              | odkazují na ně `events` a `performers`                                          |

Účinkující a položky programu mají navíc pole `slug` (čitelný identifikátor bez diakritiky) pro budoucí adresy stránek. Časy jsou ve formátu ISO 8601 s časovým pásmem (`2027-06-05T19:30:00+02:00`).

Obrázky účinkujících a scén budou vygenerovány AI v implementační fázi. Do dat pak přibude pouze cesta k souboru a alternativní text; stávající údaje se tím nemění.

### Pravidla konzistence

Vazby jsou jednoznačné a jsou strojově kontrolovány skriptem:

- všechny identifikátory a slugy jsou jedinečné,
- každá vazba odkazuje na existující entitu,
- každý účinkující má alespoň jednu položku programu a každá položka alespoň jednoho účinkujícího,
- na jedné scéně se žádné dvě položky časově nepřekrývají,
- žádný účinkující nevystupuje na dvou místech současně,
- každá položka leží v provozní době svého dne a datum odpovídá dni,
- den v týdnu odpovídá datu a časové pásmo odpovídá letnímu času v Praze,
- kapacita workshopu nepřesahuje kapacitu scény,
- program venkovní scény končí nejpozději ve 22:00.

---

## 7. Použití AI a ověření

| K čemu byla AI použita                                                                            | Nástroj                   | Jak byl výstup ověřen                                                                                                                                            |
| ------------------------------------------------------------------------------------------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Návrh konceptu festivalu, scén a témat                                                            | Claude Code (Claude Opus) | Ruční kontrola týmem proti zadání – viz níže.                                                                                                                    |
| Návrh cílových skupin, informační architektury a scénářů                                          | Claude Code (Claude Opus) | Strojově: všech 25 identifikátorů a všechny počty uvedené ve scénářích byly skriptem porovnány s `data.json` a souhlasí. Ruční průchod scénářů týmem – viz níže. |
| Vygenerování obsahu `data.json` (jména, medailonky, názvy a popisy programu, praktické informace) | Claude Code (Claude Opus) | Strojově skriptem (0 chyb). Skript sám byl ověřen 14 záměrně vloženými chybami a všechny odhalil. Ruční kontrola textů týmem – viz níže.                         |

**Zjištěné limity AI:** AI neumí zaručit, že vymyšlené jméno nenosí skutečný člověk, a údaje o reálném místě uvádí z paměti bez ověření. Časovou konzistenci programu AI navrhla správně, spolehnout se na to ale nedá, proto ji kontroluje skript, ne další dotaz na AI.
