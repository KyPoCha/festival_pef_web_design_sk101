# Úkoly týmu – iterace 1: Projektová specifikace a datová základna

Odevzdání: cvičení 2. Kontroly jsou v samostatném listu [controls/iteration-01.md](controls/iteration-01.md).

## 1. Doplnit údaje

- [x] jména čtyř členů do záhlaví `project-specification.md`
- [x] jména do tabulky v [README.md](README.md)
- [x] odpovědnosti členů do tabulky v [README.md](README.md)
- [x] jména mluvčích do `docs/presentation/iteration-01/slides.json` (pole `speakers`) a znovu sestavit prezentaci, nebo je přepsat přímo v zápatí snímků
- [x] jména v předávacích větách v souborech `speaker-1.md` až `speaker-3.md`

## 2. Potvrdit rozhodnutí, která udělala AI

Zadání určilo jen téma „tech festival“. Tyto volby navrhla AI sama. Po cvičení 2 budou závazné, proto je teď buď potvrďte, nebo změňte.

| Rozhodnutí AI                                                 | Potvrzeno / změněno | Poznámka |
| ------------------------------------------------------------- | ------------------- | -------- |
| Název Tranzistor, slogan „Zapoj se.“                          |                     |          |
| 3. ročník, termín 4.–6. 6. 2027                               |                     |          |
| Místo: Pražská tržnice, Praha 7                               |                     |          |
| Pět scén: Mainframe, Terminal, Sandbox, Arcade, Nábřeží       |                     |          |
| Sedm témat a devět formátů programu                           |                     |          |
| Formát dat JSON                                               |                     |          |
| Názvy stránek a adresy v sitemapě (např. `udalost.html?id=…`) |                     |          |
| Ceny vstupenek a kapacity scén                                |                     |          |
| Odkazy v doméně `.example`                                    |                     |          |
| Data zatím bez obrázků                                        |                     |          |

## 3. Co jsme přijali, upravili a odmítli

Na tuto otázku se vyučující ptá při každé prezentaci. Odpověď „přijali jsme všechno“ je slabá; zapište konkrétní úpravy.

| Výstup AI                     | Přijato / upraveno / odmítnuto | Co přesně a proč |
| ----------------------------- | ------------------------------ | ---------------- |
| Koncept a název festivalu     |                                |                  |
| Cílové skupiny                |                                |                  |
| Informační architektura       |                                |                  |
| Uživatelské scénáře           |                                |                  |
| Data – účinkující             |                                |                  |
| Data – program                |                                |                  |
| Data – praktické informace    |                                |                  |
| Prezentace a texty pro mluvčí |                                |                  |

## 4. Limity a chyby AI, které jsme našli sami

Limity, které o svém výstupu uvedla sama AI, jsou v `docs/ai-usage/iteration-01.md`, kapitola 7. Sem patří jen to, co našel tým.

## 5. Přenést výsledky do odevzdávaných souborů

Po dokončení kontrol:

- [ ] snímek 9 prezentace – upravit bod „Ruční kontrola týmem“, pokud některá kontrola neproběhla
- [ ] po každé úpravě `data.json` spustit `python3 tools/validate_data.py` (musí hlásit 0 chyb)
- [ ] po úpravě specifikace nebo dat zkontrolovat, že čísla na snímcích stále platí

## 6. Prezentace

- [ ] rozdělit role mluvčích 1–4
- [ ] každý si přečte svůj text a odpovědi na možné otázky
- [ ] společná zkouška se stopkami – limit je 3 až 5 minut
- [ ] ověřit, že se soubor `.odp` v učebně otevře správně; záloha je `.pdf`
