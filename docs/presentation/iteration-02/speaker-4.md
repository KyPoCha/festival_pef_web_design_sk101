# Mluvčí 4 – interaktivní funkce, použití AI a ověření

| | |
|---|---|
| **Mluvčí** | David Anderle |
| **Snímky** | 8 a 9 |
| **Čas** | přibližně 70 sekund |
| **Přebírá slovo od** | mluvčího 3 |
| **Uzavírá prezentaci** | ano |


## Text

**Snímek 8 – Interaktivní funkce**

Prototyp má šest interaktivních funkcí a každá řeší konkrétní potřebu. Filtr programu zúží 77 položek na několik. Můj program slouží jako osobní plán bez registrace a upozorní na kolize. Vyhledávání najde jméno i bez diakritiky. Blok Právě teď ukáže, co běží na scénách, a účinkující jdou filtrovat a řadit.

**Snímek 9 – Použití AI a ověření**

Prototyp, ilustrace i doplnění dat vytvořila AI v Claude Code. Ověřovali jsme to automatickým testem v prohlížeči: 190 kontrol na mobilu i desktopu včetně všech scénářů. Test odhalil například, že záhlaví na telefonu přetékalo; to jsme opravili. Data hlídá kontrolní skript. Ručně jsme web zkontrolovali nástrojem WAVE, který dal hodnocení deset z deseti, a prošli jsme ho na vlastních telefonech.

Děkujeme za pozornost.

## Možné otázky

**Co přesně test kontroluje?**
Chyby v konzoli, vodorovné přetečení, jedinečná id, jeden nadpis h1, pořadí nadpisů, načtení obrázků, průchod scénářů, ovládání klávesnicí a menu.

**Co test nekontroluje?**
Validitu HTML podle W3C, chování se čtečkou obrazovky a použitelnost s lidmi. To kontrolujeme ručně.

**Jaké chyby udělala AI?**
Záhlaví přetékalo o 67 pixelů, v tmavém vzhledu zmizely barvy témat a jedna úprava kódu rozbila skript na všech stránkách. Vše odhalil test nebo snímky obrazovky.
