# Mluvčí 4 – data, použití AI a ověření

| | |
|---|---|
| **Snímky** | 8 a 9 |
| **Čas** | přibližně 70 sekund |
| **Přebírá slovo od** | mluvčího 3 |
| **Uzavírá prezentaci** | ano |

> **Před prezentací doplnit** místa označená _[doplnit]_ podle skutečných výsledků z `docs/team-work-flow/controls/iteration-01.md`. Neříkejte nic, co tým opravdu neudělal.

## Text

**Snímek 8 – Datová základna**

Data jsou v jednom souboru JSON, který klientský web použije bez převodu. Obsahuje festival, dny, scény, témata, účinkující, položky programu a praktické informace.

Každá položka programu odkazuje identifikátorem na svůj den, scénu, téma a účinkující. Rozsah je nad požadovaným minimem.

**Snímek 9 – Použití AI a ověření**

Použili jsme Claude Code. AI navrhla koncept, cílové skupiny, architekturu a scénáře a vygenerovala texty v datech.

Ověřovali jsme třemi způsoby. Kontrolní skript hlídá vazby a to, že se na scéně nic nepřekrývá a nikdo nevystupuje na dvou místech zároveň. Samotný skript jsme otestovali čtrnácti záměrně vloženými chybami a našel všechny. A ručně: _[doplnit – co jsme prověřili a co jsme našli]_.

Z návrhů AI jsme upravili nebo odmítli _[doplnit – konkrétní příklady]_.

Hlavní limit: AI neumí zaručit, že vymyšlené jméno nenosí skutečný člověk, a údaje o skutečném místě uvádí z paměti.

Děkujeme za pozornost.

## Možné otázky

**Co přesně kontrolní skript ověřuje?**
Jedinečnost identifikátorů, platnost všech vazeb, překryvy na scéně, dvojí obsazení účinkujícího, provozní dobu, den v týdnu, časové pásmo, kapacity workshopů a minimální rozsah ze zadání.

**Proč nestačí zeptat se AI, jestli jsou data v pořádku?**
AI může potvrdit i chybná data. Skript dává pokaždé stejný výsledek a jeho spolehlivost jsme změřili na záměrně vložených chybách.

**Jaké chyby AI udělala?**
V prvním návrhu byla v panelu vedeném česky italská řečnice a turnaj měl tři týmy, se kterými nevychází semifinále. Obojí bylo opraveno před vygenerováním dat. _[doplnit chyby, které našel tým]_

**Proč JSON, a ne XML?**
Zadání JSON dovoluje a pro klientský web je přímočařejší. Pro web z něj strojově odvodíme soubor pro JavaScript, aby stránky fungovaly i po otevření ze souborového systému.

**Kolik z dat je dílem AI a kolik týmu?**
Texty vygenerovala AI. Tým odpovídá za výběr, kontrolu a úpravy: _[doplnit podle tabulky přijato / upraveno / odmítnuto]_.
