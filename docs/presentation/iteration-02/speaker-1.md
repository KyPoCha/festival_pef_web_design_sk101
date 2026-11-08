# Mluvčí 1 – co jsme udělali a oprava dat

| | |
|---|---|
| **Mluvčí** | Kyrylo Polishchuk |
| **Snímky** | 1 až 3 |
| **Čas** | přibližně 65 sekund |
| **Předává slovo** | mluvčímu 2 |

## Text

**Snímek 1 – titulní**

Dobrý den, jsme tým sk101 a ukážeme prototyp webu festivalu Tranzistor.

**Snímek 2 – Co jsme od minula udělali**

Od minula jsme vytvořili prototyp celého webu: jedenáct stránek podle sitemapy, pro mobil i desktop, se všemi 77 položkami programu. Zprovoznili jsme šest interaktivních funkcí. Opravili jsme datovou základnu a o vzhledu jsme hlasovali.

**Snímek 3 – Co chybělo v datové základně**

Ke kontrole dat jsme dostali zpětnou vazbu, že v nich něco chybí. Porovnali jsme data se zadáním a se specifikací a našli pět mezer. Hlavní byly obrázky, které zadání vyžaduje, dále schéma areálu a historie ročníků, které specifikace slibuje. Doplnili jsme je ve verzi 1.1. Kontrolní skript teď hlídá i tato pravidla: na starých datech hlásí 83 chyb, na nových žádnou.

Jak prototyp vypadá, ukáže Daniel Šimůnek.

## Možné otázky

**Nezměnili jste specifikaci víc, než je povoleno?**
Ne. Doplnili jsme jen chybějící pole; rozsah dat, identifikátory, program, scénáře i struktura webu zůstaly. Každá změna je ve specifikaci v kapitole 8 i s důvodem.

**Odkud jsou obrázky?**
Vytvořila je AI jako vektorové kresby. Portréty účinkujících jsou abstraktní monogramy, aby nepředstíraly skutečné lidi.

**Proč nejsou data načtená přímo z data.json?**
Prohlížeč nedovolí stránce otevřené ze souboru data.json načíst. Proto z něj skript vytvoří stejná data jako JavaScript a kontrolní skript hlídá, že se shodují.
