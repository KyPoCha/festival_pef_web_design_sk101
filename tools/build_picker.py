#!/usr/bin/env python3
"""Sestaví stránku pro výběr vzhledu (docs/design-picker/iteration-0N/picker.html).

Použití:  python3 tools/build_picker.py 2                       (docs/design-picker/iteration-02)
          python3 tools/build_picker.py iteration-02-round-2    (jiná složka v docs/design-picker)

Náhledy na stránce používají skutečné styly prototypu (prototype/css/style.css).
Skript je přepíše tak, aby platily jen uvnitř náhledu telefonu (.proto) a aby
se rozložení řídilo šířkou náhledu, ne šířkou okna (@media → @container).
"""
import base64
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def scope_selector(sel):
    sel = sel.strip()
    sel = sel.replace(":root", ".proto")
    m = re.match(r'^(\[data-ui-[a-z]+="[^"]+"\])(.*)$', sel)
    if m:
        rest = m.group(2).strip()
        if rest in ("", "body"):
            return ".proto" + m.group(1)
        return ".proto" + m.group(1) + " " + rest
    if sel.startswith(".proto"):
        return sel
    if sel == "body" or sel.startswith("body "):
        return ".proto" + sel[4:]
    if sel.startswith(".js "):
        return ".proto.js " + sel[4:]
    if sel.startswith("*"):
        return ".proto " + sel
    return ".proto " + sel


def scope_rules(css):
    out = []
    for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        scoped = ", ".join(scope_selector(s) for s in selectors.split(","))
        out.append(f"{scoped} {{{body}}}")
    return "\n".join(out)


def top_level_blocks(css):
    """Rozdělí CSS na bloky nejvyšší úrovně: (prelude, obsah)."""
    pos = 0
    while True:
        start = css.find("{", pos)
        if start == -1:
            return
        depth, i = 1, start + 1
        while depth:
            depth += {"{": 1, "}": -1}.get(css[i], 0)
            i += 1
        yield css[pos:start].strip(), css[start + 1:i - 1]
        pos = i


def font_data_uri(match):
    path = ROOT / "prototype" / "fonts" / Path(match.group(1)).name
    return 'url("data:font/woff2;base64,' + base64.b64encode(path.read_bytes()).decode() + '")'


def scope(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    result = []
    for prelude, body in top_level_blocks(css):
        if prelude.startswith("@media"):
            query = prelude[len("@media"):].strip()
            at = "@container proto" if "width" in query else "@media"
            result.append(f"{at} {query} {{\n{scope_rules(body)}\n}}")
        elif prelude.startswith("@keyframes"):
            result.append(f"{prelude} {{{body}}}")
        elif prelude.startswith("@font-face"):
            # písmo vložené přímo do stránky, protože náhled nemůže načíst soubory z disku
            result.append("@font-face {" + re.sub(r'url\("([^"]+\.woff2)"\)', font_data_uri, body) + "}")
        else:
            result.append(scope_rules(prelude + "{" + body + "}"))
    return "\n".join(r for r in result if r.strip())


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    name = sys.argv[1]
    folder = ROOT / "docs" / "design-picker" / (f"iteration-{int(name):02d}" if name.isdigit() else name)
    template = (folder / "picker.template.html").read_text(encoding="utf-8")
    css = scope((ROOT / "prototype" / "css" / "style.css").read_text(encoding="utf-8"))
    # ikony náhledů jsou stejné jako v prototypu
    icons = re.search(r"var ICONS = \{.*?\n  \};", (ROOT / "prototype" / "js" / "app.js").read_text(encoding="utf-8"), re.S).group(0)
    out = folder / "picker.html"
    hero = base64.b64encode((ROOT / "prototype" / "images" / "festival" / "hero.svg").read_bytes()).decode()
    out.write_text(template.replace("/*PROTO_CSS*/", css).replace("/*ICONS_JS*/", icons).replace("/*HERO_SVG*/", hero), encoding="utf-8")
    print(f"{out.relative_to(ROOT)}: {out.stat().st_size // 1024} kB")


if __name__ == "__main__":
    main()
