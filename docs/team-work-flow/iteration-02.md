# Úkoly týmu – iterace 2: UX návrh, prototyp a funkce

Odevzdání: cvičení 3. Kontroly jsou v samostatném listu [controls/iteration-02.md](controls/iteration-02.md).

## 1. Doplnit údaje

- [ ] `progress-02.md`, kapitola 4 – proč jsme u barevného směru a karty programu nepřijali doporučení AI
- [ ] `progress-02.md`, kapitola 7 – shrnutí ruční kontroly podle kontrolního listu
- [ ] `progress-02.md`, kapitola 8 – co tým přijal, upravil a odmítl (z tabulky v kapitole 3 tohoto souboru)
- [ ] snímek 9 prezentace a `docs/presentation/iteration-02/speaker-4.md` – místa označená [doplnit]

## 2. Hlasování o vzhledu

Zatím je uložený jeden hlas (Kyber, spodní lišta, dlaždice, textové tlačítko). Prototyp tuto kombinaci používá jako výchozí.

- [ ] sdílet stránku pro výběr vzhledu s ostatními členy (menu Share na stránce; bez sdílení ji neotevřou)
- [ ] ostatní členové hlasují nebo kombinaci potvrdí
- [ ] pokud tým rozhodne jinak, napsat výsledek do chatu – výchozí kombinace se změní na jednom místě (`UI_DEFAULTS` v `prototype/js/app.js`)

## 3. Potvrdit rozhodnutí, která udělala AI

| Rozhodnutí AI | Potvrzeno / změněno | Poznámka |
|---|---|---|
| Co v `data.json` chybělo (obrázky, schéma, historie, kontakt pro média, témata panelistů) | | Odpovídá to zpětné vazbě, kterou jsme dostali? |
| Ilustrace jako SVG kresby, portréty jako abstraktní monogramy | | Alternativa: portréty z generátoru obrázků v iteraci 4 |
| Data pro web v `prototype/js/data.js` odvozená skriptem | | |
| Ikony podle Material Icons (Apache License 2.0) | | |
| Rezervace workshopů – zatím nefunkční | | Nasimulovat v prohlížeči, nebo napsat „rezervace na místě“? |
| Adresy stránek ve tvaru `udalost.html?id=…` | | Rozhodnout ve 3. iteraci spolu se SEO |

## 4. Co jsme přijali, upravili a odmítli

| Výstup AI | Přijato / upraveno / odmítnuto | Co přesně a proč |
|---|---|---|
| Doporučený barevný směr Signál | odmítnuto – zvolen Kyber | _doplnit proč_ |
| Doporučená karta Časová osa | odmítnuto – zvolena Dlaždice | _doplnit proč_ |
| Doporučená spodní lišta | přijato | |
| Doporučené textové tlačítko uložit | přijato | |
| Znakové ikony ve spodní liště | odmítnuto – nahrazeny ikonami ve stylu Material, počet v rohu ikony | poznámka z hlasování |
| Oprava `data.json` | | |
| Prototyp – struktura stránek a funkce | | |
| Posouzení prototypu člena týmu | | |
| Prezentace a texty pro mluvčí | | |

## 5. Limity a chyby AI, které jsme našli sami

Limity, které uvedla sama AI, jsou v `docs/ai-usage/iteration-02.md`, kapitola 7. Sem patří jen to, co našel tým.

- _doplnit_

## 6. Prototyp člena týmu

- [ ] probrat s autorem posouzení v `progress-02.md`, kapitola 6 (co jsme převzali a proč zbytek ne)
- [ ] jeho složka `web/` se zatím neodevzdává; `web/` je výstupem iterace 3 a vznikne z `prototype/`

## 7. Prezentace

- [ ] každý si přečte svůj text v `docs/presentation/iteration-02/speaker-N.md`
- [ ] společná zkouška se stopkami – limit 3 až 5 minut
- [ ] na cvičení mít prototyp otevřený v prohlížeči pro případ dotazu (`prototype/index.html`)

## 8. Odevzdání

- [ ] `python3 tools/validate_data.py` – 0 chyb
- [ ] `python3 tools/package_submission.py 2` – archiv s prototypem, `progress-02.md`, `data.json`, specifikací a prezentací
- [ ] nahrát archiv do Moodlu před cvičením
- [ ] uložit práci do repozitáře přes pull request (větev `main` je chráněná)
