# Kontrolní list – iterace 1: Projektová specifikace a datová základna

Kontroly provádí člověk z týmu. Ke každé zapište, kdo ji provedl, kdy a co zjistil. Nález zapište i tehdy, když je drobný – právě nálezy jsou důkazem, že kontrola proběhla.

## Přehled

| Kontrola | Kdo | Datum | Výsledek (v pořádku / nálezy) |
|---|---|---|---|
| K1 – Čtení specifikace | | | |
| K2 – Shoda se zadáním | | | |
| K3 – Vzorek textů v datech | | | |
| K4 – Jména účinkujících | | | |
| K5 – Údaje o skutečném místě | | | |
| K6 – Festival není kopií | | | |
| K7 – Průchod scénářů S1–S3 | | | |
| K8 – Kontrolní skript | | | |
| K9 – Prezentace | | | |

Strojové kontroly, které už provedla AI (konzistence dat, test skriptu vloženými chybami, shoda identifikátorů ve specifikaci s daty), jsou popsány v `docs/ai-usage/iteration-01.md`, kapitola 5. Tento list je nenahrazuje a neopakuje.

---

## K1 – Čtení specifikace

**Postup:** Přečíst celý `project-specification.md` od začátku do konce. U každé kapitoly si položit otázku: souhlasíme s tím a umíme to obhájit?

**Na co se zaměřit:** nepřirozené formulace, tvrzení, kterým nerozumíme, sliby, které web bez backendu nesplní (nákup vstupenek, rezervace workshopů).

**Nálezy:**

-

## K2 – Shoda se zadáním

**Postup:** Projít požadavky z Moodlu na první výstup a u každého najít místo ve specifikaci nebo v datech.

| Požadavek | Kde je splněn | Zkontrolováno |
|---|---|---|
| Identita festivalu v tabulce: název, ročník, lokalita, datumový rozsah, charakter, žánry nebo témata | kapitola 1 | ☐ |
| Účel webu: k čemu slouží, hlavní cíle, důležité akce uživatelů | kapitola 2 | ☐ |
| Cílové skupiny: potřeby, očekávání, informace a funkce | kapitola 3 | ☐ |
| Sitemap, hlavní navigace, vztahy mezi částmi, účel částí | kapitoly 4.1–4.4 | ☐ |
| Povinné části webu: úvod, program, účinkující (seznam a detail), scény, praktické informace, interaktivní části | kapitoly 4.1 a 4.5 | ☐ |
| Scénáře s typem uživatele, cílem, výchozí situací a očekávaným výsledkem | kapitola 5 | ☐ |
| Alespoň tři klíčové scénáře | S1–S3 | ☐ |
| Data: nejméně 3 dny, 2 scény, 60 účinkujících, 60 položek | `data.json`, kapitola 6 | ☐ |
| Entity: festival, scény, účinkující, položky programu | `data.json` | ☐ |
| Formát XML nebo JSON | `data.json` | ☐ |

**Nálezy:**

-

## K3 – Vzorek textů v datech

**Postup:** Přečíst medailonky a popisy u položek z níže uvedeného náhodného vzorku (15 účinkujících a 15 položek programu). Kdo chce, přečte víc.

**Na co se zaměřit:** gramatika a překlepy, věty bez smyslu, opakující se stavba vět, nevhodný nebo urážlivý obsah, rozpor mezi medailonkem a tím, v čem účinkující vystupuje.

**Vzorek účinkujících:**

| ID | Účinkující | V pořádku? | Poznámka |
|---|---|---|---|
| p007 | Sára Benešovská | | |
| p014 | Oisín Gallagher-Byrne | | |
| p015 | Marek Zdráhal | | |
| p019 | Dietrich Vogelsang | | |
| p022 | Kristýna Malátová | | |
| p025 | Rafael Monteverde | | |
| p032 | Krakowskie Smoki | | |
| p033 | Tatranskí Rysi | | |
| p039 | DJ Kernel Panic | | |
| p043 | Bitová Hloubka | | |
| p045 | Ráno v Serverovně | | |
| p046 | Katja Zimmerlin | | |
| p051 | Marie Kutálková | | |
| p060 | Johana Peřinová | | |
| p061 | Štěpán Louda | | |

**Vzorek položek programu:**

| ID | Položka programu | V pořádku? | Poznámka |
|---|---|---|---|
| e010 | Algoritmia: hudba psaná naživo | | |
| e012 | Tranzistor Cup: skupinová fáze | | |
| e021 | Retro noc s Pixel Babičkou | | |
| e025 | Data nelžou, grafy ano | | |
| e028 | Příběh pro hráče, který neposlouchá | | |
| e031 | Design systém, který přežil tři redesigny | | |
| e033 | Prompty, které fungují | | |
| e042 | Od víkendového prototypu k vydané hře | | |
| e047 | Soukromí je týmový sport | | |
| e052 | Šum a Signál | | |
| e057 | Rodinná dílna: světelný brouk | | |
| e061 | Otevřený hardware: plány pro všechny | | |
| e069 | Digitální klid: jak nevyhořet u obrazovky | | |
| e074 | Roboti, kteří se učí od lidí | | |
| e077 | Poslední Commit: závěrečný koncert | | |

**Nálezy:**

-

## K4 – Jména účinkujících

**Postup:** Každé jméno vyhledat ve vyhledávači. Hledáme shodu se skutečnou veřejně známou osobou, kapelou, firmou nebo značkou ve stejném oboru. Při shodě jméno v `data.json` změnit (pole `name`, `slug` a `website`) a spustit kontrolní skript.

Běžné jméno, které nosí i soukromé osoby, nevadí. Vadí shoda s někým, s kým by si čtenář fiktivního účinkujícího mohl splést.

| ID | Jméno | Typ | Shoda nalezena? |
|---|---|---|---|
| p001 | Elena Havránková | Řečník / řečnice | |
| p002 | Tomasz Wieliczko | Řečník / řečnice | |
| p003 | Ngozi Adebayo-Lindqvist | Řečník / řečnice | |
| p004 | Vojtěch Skřivan | Řečník / řečnice | |
| p005 | Mirela Dragomir | Řečník / řečnice | |
| p006 | Kenji Moriwaki | Řečník / řečnice | |
| p007 | Sára Benešovská | Řečník / řečnice | |
| p008 | Jonáš Vrbata | Řečník / řečnice | |
| p009 | Ingrid Solheim | Řečník / řečnice | |
| p010 | Radim Koutecký | Řečník / řečnice | |
| p011 | Lucía Ferrandis | Řečník / řečnice | |
| p012 | Patrik Hruboň | Řečník / řečnice | |
| p013 | Daniela Štorková | Řečník / řečnice | |
| p014 | Oisín Gallagher-Byrne | Řečník / řečnice | |
| p015 | Marek Zdráhal | Řečník / řečnice | |
| p016 | Barbora Kolmanová | Řečník / řečnice | |
| p017 | Matteo Calvaresi | Řečník / řečnice | |
| p018 | Hana Šimůnková | Řečník / řečnice | |
| p019 | Dietrich Vogelsang | Řečník / řečnice | |
| p020 | Aigerim Nurlanova | Řečník / řečnice | |
| p021 | Ondřej Pazdera | Řečník / řečnice | |
| p022 | Kristýna Malátová | Řečník / řečnice | |
| p023 | Lars Hedenskog | Řečník / řečnice | |
| p024 | Zuzana Križanová | Řečník / řečnice | |
| p025 | Rafael Monteverde | Řečník / řečnice | |
| p026 | Petr Luňáček | Lektor / lektorka | |
| p027 | Studio Mlha | Kolektiv / studio | |
| p028 | Tereza Vaňousová | Řečník / řečnice | |
| p029 | Yuki Tanabe-Hart | Řečník / řečnice | |
| p030 | Stříbrní Lvi | E-sportový tým | |
| p031 | Team Nordwind | E-sportový tým | |
| p032 | Krakowskie Smoki | E-sportový tým | |
| p033 | Tatranskí Rysi | E-sportový tým | |
| p034 | Pixel Babička | Moderátor / moderátorka | |
| p035 | Adam Řezníček | Moderátor / moderátorka | |
| p036 | Kolektiv Osmibit | Kolektiv / studio | |
| p037 | Neonová Sova | Hudební projekt | |
| p038 | Algoritmia | Hudební projekt | |
| p039 | DJ Kernel Panic | Hudební projekt | |
| p040 | Modulární Morava | Hudební projekt | |
| p041 | Lumen Field | Hudební projekt | |
| p042 | Šum a Signál | Hudební projekt | |
| p043 | Bitová Hloubka | Hudební projekt | |
| p044 | Voltage Sisters | Hudební projekt | |
| p045 | Ráno v Serverovně | Hudební projekt | |
| p046 | Katja Zimmerlin | Umělec / umělkyně | |
| p047 | Filip Dostálek | Umělec / umělkyně | |
| p048 | Orchestr Rozbitých Tiskáren | Hudební projekt | |
| p049 | Sine Qua Nonet | Hudební projekt | |
| p050 | Glitch Babylon | Hudební projekt | |
| p051 | Marie Kutálková | Umělec / umělkyně | |
| p052 | Subnet Mask | Hudební projekt | |
| p053 | Poslední Commit | Hudební projekt | |
| p054 | Magdaléna Jirsová | Moderátor / moderátorka | |
| p055 | Bohumil Trnavský | Řečník / řečnice | |
| p056 | Chiara Bellandi | Řečník / řečnice | |
| p057 | Viktor Hlaváčik | Řečník / řečnice | |
| p058 | Simona Rybářová | Řečník / řečnice | |
| p059 | Emre Kahraman | Řečník / řečnice | |
| p060 | Johana Peřinová | Řečník / řečnice | |
| p061 | Štěpán Louda | Řečník / řečnice | |
| p062 | Dílna Pájka | Kolektiv / studio | |
| p063 | Alžběta Nováčková | Lektor / lektorka | |
| p064 | Jakub Tesařík | Lektor / lektorka | |
| p065 | Wanjiru Kamau-Stein | Lektor / lektorka | |
| p066 | Robin Vacula | Lektor / lektorka | |
| p067 | Nikola Šafránková | Lektor / lektorka | |

**Nálezy a provedené změny:**

-

## K5 – Údaje o skutečném místě

**Postup:** Každé tvrzení ověřit na webu provozovatele areálu nebo dopravce (Pražská tržnice, DPP, PID, České dráhy), ne dotazem na AI. Zapsat zdroj.

| Tvrzení v datech a ve specifikaci | Zdroj | Platí? |
|---|---|---|
| Adresa areálu: Bubenské nábřeží 306/13, 170 00 Praha 7 – Holešovice | | |
| Tramvajová zastávka se jmenuje „Pražská tržnice“ a je u vstupu do areálu | | |
| Nejbližší metro je Vltavská na lince C, pěšky asi 8 minut | | |
| Nádraží Praha-Holešovice je jednu stanici metra od Vltavské, pěšky asi 20 minut | | |
| Zeměpisné souřadnice 50,0995 s. š., 14,4447 v. d. odpovídají areálu | | |
| 4. 6. 2027 je pátek | | |
| V areálu je nábřeží a venkovní plocha, kde by mohla stát venkovní scéna | | |

**Nálezy:**

-

## K6 – Festival není kopií existující akce

**Postup:** Vyhledat „Tranzistor festival“ a podobné názvy. Porovnat koncept s festivaly, které známe (technologické konference, maker festivaly, herní akce, festivaly světla a digitálního umění).

**Otázky:** Existuje akce se stejným názvem? Existuje akce, která má stejné místo, termín i skladbu programu?

**Nálezy:**

-

## K7 – Průchod scénářů S1–S3 nad daty

**Postup:** Otevřít `data.json` v editoru a ručně vyhledat údaje, které scénář slibuje. Nespoléhat na čísla ve specifikaci.

| Scénář | Co ověřit | Očekávaná hodnota | Souhlasí? |
|---|---|---|---|
| S1 | počet sobotních položek (`dayId: d2`) na scéně Nábřeží (`venueId: v05`) | 6 | |
| S1 | čas první a poslední položky | 14:00 a konec ve 22:00 | |
| S1 | koncert Šum a Signál | e052, 19:30–20:30 | |
| S2 | vystoupení Kristýny Malátové (p022) | e043 a e047 | |
| S2 | sobotní položky tématu Bezpečnost a soukromí (`trackId: t04`) | e035, e039, e043, e047 | |
| S2 | časy workshopu e039 a přednášky e043 se překrývají | 15:00–17:00 a 16:30–17:15 | |
| S3 | nedělní položky (`dayId: d3`) s `familyFriendly: true` | 9 | |
| S3 | dílna e057: kapacita, rezervace, věk | 30 míst, rezervace nutná, od 6 let | |
| S3 | cena rodinné nedělní vstupenky a vstup dětí | 1 490 Kč, do 12 let zdarma | |
| S3 | doprava: tramvaj u vstupu, v areálu se neparkuje | podle `practical.transport` | |

**Otázka navíc:** Dává scénář smysl jako situace skutečného člověka? Chybí v něm krok, který by uživatel musel udělat?

**Nálezy:**

-

## K8 – Kontrolní skript

**Postup:** Spustit `python3 tools/validate_data.py` na vlastním počítači, po každé úpravě dat znovu.

| Datum | Kdo | Výstup skriptu (počet chyb a upozornění) |
|---|---|---|
| | | |

Kdo chce ověřit, že skript opravdu něco hlídá: v kopii `data.json` změnit u jedné položky `venueId` na neexistující hodnotu a spustit skript na kopii. Musí ohlásit chybu.

**Nálezy:**

-

## K9 – Prezentace

| Co ověřit | Výsledek |
|---|---|
| Čísla na snímcích souhlasí s aktuální verzí specifikace a dat | |
| Snímek 9 a text mluvčího 4 popisují jen kontroly, které tým opravdu provedl | |
| Společná zkouška: celkový čas (limit 3–5 minut) | |
| Soubor `.odp` se otevře a zobrazí správně na počítači, ze kterého se bude promítat | |
| Soubor prezentace je nahrán v Moodlu | |

**Nálezy:**

-
