#!/usr/bin/env python3
"""Odvodí z data.json soubor js/data.js pro web nebo prototyp.

Použití:  python3 tools/build_web_data.py prototype
          python3 tools/build_web_data.py web

Prohlížeč nedovolí stránce otevřené ze souborového systému (file://) načíst
data.json přes fetch(). Proto se stejná data uloží jako JavaScript:
    window.TRANZISTOR_DATA = { … obsah data.json … };
Obsah se nemění, jen se obalí. Shodu s data.json ověřuje tools/validate_data.py.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "window.TRANZISTOR_DATA = "


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    site = ROOT / sys.argv[1]
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    target = site / "js" / "data.js"
    target.parent.mkdir(parents=True, exist_ok=True)
    header = "/* Vygenerováno z data.json skriptem tools/build_web_data.py – needitujte ručně. */\n"
    target.write_text(header + PREFIX + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"{target.relative_to(ROOT)}: {target.stat().st_size // 1024} kB")


if __name__ == "__main__":
    main()
