# Mluvčí 2 – doporučení a trendy v UX, od mobilu k desktopu

| | |
|---|---|
| **Mluvčí** | Daniel Šimůnek |
| **Snímky** | 4 a 5 |
| **Čas** | přibližně 70 sekund |
| **Přebírá slovo od** | mluvčího 1 |
| **Předává slovo** | mluvčímu 3 |

## Text

**Snímek 4 – Doporučení a trendy v UX**

Vlevo jsou doporučení, která jsme našli, vpravo jak jsou na webu. Podle WCAG 2.2 nesmí fokus zajet pod přilepené lišty, proto se stránka při pohybu tabulátorem posouvá. Navigace je dole v dosahu palce. Místo okna „Opravdu odebrat?“ ukážeme tlačítko Vrátit, jak doporučuje Nielsen Norman Group. U tmavého vzhledu jsme kontrast spočítali, nejnižší je 7,4 ku 1. Animace běží jen tehdy, když je uživatel v systému nevypnul. A obsah je v HTML bez knihoven, aby se web načítal rychle.

**Snímek 5 – Od mobilu k desktopu**

Web je navržený od telefonu o šířce 360 pixelů. Na mobilu je spodní lišta a sbalené filtry. Na desktopu je menu nahoře, filtry v panelu vlevo a karty ve dvou sloupcích. Vzhled je ten, který jsme si zvolili minule.

Jak se na webu projdou scénáře, ukáže Ngoc Tuan Nguyen.

## Možné otázky

**Odkud ta doporučení jsou?**
Hlavně z W3C, web.dev a Nielsen Norman Group; ke každému bodu je v progress-03.md odkaz na zdroj. Přehledy trendů od agentur jsme brali jen tam, kde se shodovalo více zdrojů.

**Které trendy jste nepoužili?**
Personalizaci pomocí AI a hlasové ovládání, protože by potřebovaly server a web musí běžet jen v prohlížeči. A průhledné skleněné vrstvy, protože snižují kontrast textu.

**Jak víte, že je web rychlý?**
Zatím jen z toho, jak je postavený: žádné knihovny ani externí zdroje, obrázky mají rozměry a načítají se postupně. Měření Lighthousem je v plánu na iteraci 4.
