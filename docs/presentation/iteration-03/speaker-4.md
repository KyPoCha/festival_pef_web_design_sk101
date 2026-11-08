# Mluvčí 4 – web pro vyhledávače a AI, testy a použití AI

| | |
|---|---|
| **Mluvčí** | David Anderle |
| **Snímky** | 8 a 9 |
| **Čas** | přibližně 70 sekund |
| **Přebírá slovo od** | mluvčího 3 |
| **Uzavírá prezentaci** | ano |

## Text

**Snímek 8 – Web pro vyhledávače a AI**

Každá stránka má vlastní titulek, popis a kanonickou adresu a při sdílení se zobrazí náhled, který vidíte vlevo. Ve stránkách jsou strukturovaná data JSON-LD: festival, položky programu, účinkující, scény a časté dotazy. Vyhledávač i nástroj AI z nich přečtou fakta, jako je čas a místo koncertu. Web má i mapu webu se 155 stránkami, soubor robots.txt a llms.txt se stručným popisem festivalu.

**Snímek 9 – Testy a použití AI**

Generátor stránek, metadata a úpravu stylů vytvořila AI v Claude Code. Ověřovali jsme to testem v prohlížeči: 125 kontrol na všech 157 stránkách včetně scénářů a stavu bez JavaScriptu, a 45 kontrol přístupnosti podle WCAG 2.2 AA. Testy odhalily tři chyby AI: převod stylů změnil vzhled 24 stránek, dvě stránky měly stejný titulek a bez JavaScriptu byla vidět nefunkční tlačítka. Všechny jsme opravili.

Děkujeme za pozornost.

## Možné otázky

**Jak víte, že strukturovaná data odpovídají stránce?**
Vznikají ze stejných dat jako viditelný obsah stránky. Test ověřuje, že jsou platný JSON; ověření nástroji vyhledávačů je v plánu na závěrečnou iteraci.

**Co testy nekontrolují?**
Validitu HTML podle W3C, chování se čtečkou obrazovky a použitelnost s lidmi. Validátor W3C je v plánu na iteraci 4.

**Proč llms.txt, když ho prý vyhledávače nečtou?**
Je to nepovinný doplněk s neprokázaným účinkem a stojí jen jeden krátký soubor. Hlavní jsou strukturovaná data, která podporu mají.
