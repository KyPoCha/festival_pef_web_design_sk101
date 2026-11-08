# Kontrolní list – iterace 2: UX návrh, prototyp a funkce

Kontroly provádí člověk z týmu. Ke každé zapište, kdo ji provedl, kdy a co zjistil. Strojové kontroly, které provedla AI (test v prohlížeči, kontrast, kontrolní skript dat), jsou v `docs/ai-usage/iteration-02.md`, kapitola 5; tento list je neopakuje.

## Přehled

| Kontrola | Kdo | Datum | Výsledek (v pořádku / nálezy) |
|---|---|---|---|
| K1 – Scénáře na vlastním telefonu | | | |
| K2 – Test s lidmi mimo tým | | | |
| K3 – Validátor HTML W3C | | | |
| K4 – Klávesnice a čtečka obrazovky | | | |
| K5 – Kontrast ověřený nástrojem | | | |
| K6 – Desktopové rozložení | | | |
| K7 – Texty, ilustrace a licence ikon | | | |
| K8 – Kontrolní skript a test | | | |
| K9 – Prezentace | | | |

---

## K1 – Scénáře na vlastním telefonu

**Postup:** Zkopírovat složku `prototype/` do telefonu nebo ji otevřít z počítače v režimu telefonu (vývojářské nástroje prohlížeče, šířka 360–390 px) a projít scénáře podle specifikace.

| Scénář | Očekávaný výsledek | Souhlasí? | Kde jsem váhal/a |
|---|---|---|---|
| S1 Večer na Nábřeží | Program → Sobota + Nábřeží → 6 položek → Šum a Signál → uložit → počet 1 v rohu hvězdičky | | |
| S2 Bezpečnost pro profesionálku | Hledání „malatova“ → řečnice, 2 vystoupení → uložit → téma Bezpečnost, sobota → workshop → Můj program ukáže kolizi | | |
| S3 Rodinná neděle | Neděle + Pro rodiny → 9 položek → dílna e057 (30 míst, rezervace, od 6 let) → zpět se zachovanými filtry → Praktické informace | | |
| S4 Právě teď | Úvod → „Vyzkoušet na sobotním večeru“ → na Nábřeží běží Šum a Signál | | |

**Nálezy:**

-

## K2 – Test s lidmi mimo tým

**Postup:** Dvěma až třem lidem, kteří prototyp neviděli, dát na telefonu úkol ze scénáře S1 a S3 (bez nápovědy, kam kliknout). Pozorovat a zapsat, kde zaváhali nebo se ztratili. Nevysvětlovat během úkolu.

| Účastník (bez jména) | Úkol | Splnil/a? | Čas | Kde zaváhal/a |
|---|---|---|---|---|
| | S1 | | | |
| | S3 | | | |
| | S1 | | | |

**Nálezy:**

-

## K3 – Validátor HTML W3C

**Postup:** Na https://validator.w3.org/nu/ zvolit „File upload“ a nahrát postupně všech 11 souborů HTML z `prototype/`. Zapsat počet chyb a varování. Validátor kontroluje zdrojový kód stránky; obsah, který doplní JavaScript, nekontroluje.

| Soubor | Chyby | Varování |
|---|---|---|
| index.html | | |
| program.html | | |
| udalost.html | | |
| ucinkujici.html | | |
| ucinkujici-detail.html | | |
| sceny.html | | |
| scena.html | | |
| muj-program.html | | |
| prakticke-informace.html | | |
| hledani.html | | |
| o-festivalu.html | | |

**Nálezy:**

-

## K4 – Klávesnice a čtečka obrazovky

**Postup:** Na počítači projít Program a Můj program jen klávesnicí (Tab, Shift+Tab, Enter, mezerník). Pak totéž se čtečkou obrazovky (VoiceOver: Cmd+F5 na Macu, NVDA na Windows).

| Co ověřit | Výsledek |
|---|---|
| Fokus je vždy vidět | |
| Filtry jdou ovládat bez myši | |
| Tlačítko uložit oznámí název položky a stav (stisknuto / nestisknuto) | |
| Po uložení čtečka přečte potvrzení „Přidáno do Mého programu“ | |
| Spodní lišta: každá položka má srozumitelný název, „Můj plán“ i počet uložených | |
| Upozornění na kolizi čtečka přečte | |

**Nálezy:**

-

## K5 – Kontrast ověřený nástrojem

**Postup:** AI spočítala kontrast výpočtem. Ověřte namátkou tři dvojice nástrojem, například https://webaim.org/resources/contrastchecker/.

| Dvojice | Barvy | Výpočet AI | Nástroj |
|---|---|---|---|
| Šedý text na kartě | #9ea6c0 na #121624 | 7,44 : 1 | |
| Zelený čas na kartě | #2ef2a6 na #121624 | 12,32 : 1 | |
| Tmavý text na štítku tématu | #0a0c13 na #ff7a93 | 7,87 : 1 | |

**Nálezy:**

-

## K6 – Desktopové rozložení

**Postup:** Otevřít prototyp na počítači v okně širokém aspoň 1280 px a projít všechny stránky. Zúžit okno postupně až na 360 px a sledovat, jestli se nic nepřekrývá a nevznikne vodorovný posuvník.

**Nálezy:**

-

## K7 – Texty, ilustrace a licence ikon

| Co ověřit | Výsledek |
|---|---|
| Nové texty v `data.json` (historie ročníků, popisy obrázků) dávají smysl | |
| Ilustrace scén a schéma areálu odpovídají popisu scén | |
| Ikony jsou podle Material Icons (Apache License 2.0) – uvést v dokumentaci | |
| Texty na stránkách prototypu (nadpisy, tlačítka, prázdné stavy) jsou srozumitelné | |

**Nálezy:**

-

## K8 – Kontrolní skript a test

| Datum | Kdo | `python3 tools/validate_data.py` | `tools/test_prototype.js` (návod v hlavičce souboru) |
|---|---|---|---|
| | | | |

**Nálezy:**

-

## K9 – Prezentace

| Co ověřit | Výsledek |
|---|---|
| Čísla a snímky obrazovky odpovídají aktuálnímu prototypu | |
| Snímek 9 a text mluvčího 4 popisují jen kontroly, které tým opravdu provedl | |
| Společná zkouška: celkový čas (limit 3–5 minut) | |
| Soubor `.odp` se otevře na počítači v učebně; záloha `.pdf` | |
| Prezentace je nahraná v Moodlu | |

**Nálezy:**

-
