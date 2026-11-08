# Mluvčí 1 – co jsme udělali a předgenerované stránky

| | |
|---|---|
| **Mluvčí** | Kyrylo Polishchuk |
| **Snímky** | 1 až 3 |
| **Čas** | přibližně 65 sekund |
| **Předává slovo** | mluvčímu 2 |

## Text

**Snímek 1 – titulní**

Dobrý den, jsme tým sk101 a ukážeme první funkční verzi webu festivalu Tranzistor.

**Snímek 2 – Co jsme od minula udělali**

Z prototypu jsme udělali web: 157 stránek, které mají obsah přímo v HTML. Všech šest interaktivních funkcí z prototypu funguje i tady. Prošli jsme aktuální doporučení a trendy v UX a designu, připravili web pro vyhledávače a nástroje umělé inteligence a zopakovali všechny testy.

**Snímek 3 – Z prototypu web: předgenerované stránky**

Prototyp měl pro každý typ detailu jednu šablonu, například detail položky programu s parametrem id v adrese, a obsah do ní doplňoval JavaScript. Na webu má každá položka programu, každý účinkující i každá scéna vlastní stránku s čitelnou adresou, třeba program/sum-a-signal.html. Obsah tak přečte vyhledávač i nástroj AI a zobrazí se i bez JavaScriptu – to je obrázek vlevo. Stránky vytváří náš skript z data.json, web ale dál běží po otevření ze souboru, bez serveru.

Jaká doporučení z UX jsme použili, řekne Daniel Šimůnek.

## Možné otázky

**Nepotřebuje web teď build nebo server?**
Ne. Skript stránky jen jednou vytvoří a ty jsou ve složce web. Web se otevře dvojklikem na index.html. Skript je potřeba jen po změně dat.

**Změnili jste kvůli tomu specifikaci?**
Jen adresy detailních stránek v sitemapě. Změna je ve specifikaci ve verzi 1.2 v kapitole 8 i s důvodem. Stránky, obsah, scénáře a data se nezměnily.

**Co bez JavaScriptu nefunguje?**
Filtry, Můj program, hledání a blok Právě teď. Celý program, detaily a praktické informace jsou ale vidět. Ovládání, které by bez JavaScriptu nic nedělalo, se bez něj nezobrazuje.
