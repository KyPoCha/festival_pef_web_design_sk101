#!/usr/bin/env python3
"""Vygeneruje ilustrace SVG, na které odkazuje data.json, do složky webu.

Použití:  python3 tools/generate_images.py prototype
          python3 tools/generate_images.py web

Ilustrace jsou vektorové kresby zapsané jako kód (napsala je AI), ne fotografie.
Portréty účinkujících jsou abstraktní: monogram na pozadí v barvě hlavního
tématu a vzor „plošného spoje“ odvozený z identifikátoru, takže je každý jiný
a při opakovaném spuštění vychází stejně. Schéma areálu se kreslí podle poloh
scén v data.json (venues[].mapPosition). Používá jen standardní knihovnu.
"""
import hashlib
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
# Paleta odpovídá zvolenému vzhledu Kyber (iterace 2).
NAVY, NAVY_2, YELLOW, PAPER = "#0b0e17", "#141a2c", "#2ef2a6", "#111625"
INK, MUTED, TRACE = "#edf0f7", "#9ea6c0", "#1f3346"
# Stejné barvy témat používá css/style.css (--track-t01 … --track-t07).
TRACK_COLORS = {
    "t01": "#6d28d9", "t02": "#0369a1", "t03": "#b45309", "t04": "#b91c1c",
    "t05": "#15803d", "t06": "#be185d", "t07": "#0f766e",
}
FONT = "font-family=\"'Segoe UI', Roboto, Helvetica, Arial, sans-serif\""


def svg(width, height, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" role="img" aria-label="{escape(label)}">{body}</svg>\n')


def rng(seed):
    """Deterministický zdroj čísel 0–255 z textu."""
    data = hashlib.sha256(seed.encode()).digest()
    while True:
        for byte in data:
            yield byte
        data = hashlib.sha256(data).digest()


def initials(name):
    words = [w for w in name.replace("-", " ").split() if w[0].isalpha()]
    return "".join(w[0] for w in words[:2]).upper()


def performer(p):
    color = TRACK_COLORS[p["trackIds"][0]]
    r = rng(p["id"])
    traces = []
    for _ in range(5):
        x = 20 + next(r) % 200
        y = 20 + next(r) % 200
        dx = (next(r) % 120) - 60
        dy = (next(r) % 120) - 60
        traces.append(
            f'<path d="M{x} {y} h{dx} v{dy}" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="5" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{x + dx}" cy="{y + dy}" r="8" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="4"/>')
    ring = YELLOW if p.get("headliner") else "#ffffff"
    body = (
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{color}"/>'
        f'<stop offset="1" stop-color="{NAVY}"/></linearGradient></defs>'
        f'<rect width="240" height="240" fill="url(#g)"/>{"".join(traces)}'
        f'<circle cx="120" cy="120" r="70" fill="{NAVY}" fill-opacity=".55" stroke="{ring}" stroke-width="5"/>'
        f'<text x="120" y="140" text-anchor="middle" font-size="58" font-weight="700" fill="#fff" {FONT}>'
        f'{escape(initials(p["name"]))}</text>'
    )
    return svg(240, 240, body, p["image"]["alt"])


def hero(f):
    traces = []
    r = rng("hero")
    for i in range(14):
        y = 40 + i * 40
        x = next(r) % 300
        length = 200 + next(r) % 500
        traces.append(f'<path d="M{x} {y} h{length} l30 30 h{next(r) % 200 + 80}" fill="none" stroke="{TRACE}" '
                      f'stroke-width="4"/><circle cx="{x}" cy="{y}" r="7" fill="{NAVY}" stroke="{TRACE}" stroke-width="4"/>')
    body = (
        f'<rect width="1200" height="600" fill="{NAVY}"/>{"".join(traces)}'
        f'<g transform="translate(860 300)">'
        f'<circle r="170" fill="{NAVY_2}" stroke="{YELLOW}" stroke-width="10"/>'
        f'<path d="M-60 -110 V110" stroke="#fff" stroke-width="14" stroke-linecap="round"/>'
        f'<path d="M-200 0 H-60" stroke="#fff" stroke-width="14" stroke-linecap="round"/>'
        f'<path d="M-60 -50 L60 -130 V-230" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M-60 50 L60 130 V230" fill="none" stroke="{YELLOW}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M30 92 L66 133 L14 140 Z" fill="{YELLOW}"/>'
        f'</g>'
        f'<circle cx="160" cy="470" r="60" fill="none" stroke="{YELLOW}" stroke-width="6" stroke-dasharray="14 12"/>'
    )
    return svg(1200, 600, body, f["image"]["alt"])


def area_map(data):
    f, venues = data["festival"], data["venues"]
    width, height = 800, 560
    halls = []
    for v in venues:
        x = v["mapPosition"]["x"] / 100 * width
        y = v["mapPosition"]["y"] / 100 * height
        w, h = (230, 110) if v["indoor"] else (250, 84)
        fill = "#1a2135" if v["indoor"] else "#123326"
        halls.append(
            f'<g><rect x="{x - w / 2:.0f}" y="{y - h / 2:.0f}" width="{w}" height="{h}" rx="10" fill="{fill}" '
            f'stroke="{YELLOW}" stroke-width="3"/>'
            f'<text x="{x:.0f}" y="{y - 2:.0f}" text-anchor="middle" font-size="32" font-weight="700" fill="{INK}" {FONT}>'
            f'{escape(v["name"])}</text>'
            f'<text x="{x:.0f}" y="{y + 30:.0f}" text-anchor="middle" font-size="21" fill="{MUTED}" {FONT}>'
            f'{escape(v["zone"])}</text></g>')
    body = (
        f'<rect width="{width}" height="{height}" fill="{PAPER}"/>'
        f'<path d="M0 470 C200 440 420 520 800 500 V560 H0 Z" fill="#17405a"/>'
        f'<text x="640" y="540" font-size="20" font-style="italic" fill="#7ddcff" {FONT}>Vltava</text>'
        f'<rect x="40" y="40" width="720" height="420" rx="18" fill="none" stroke="#3a4360" stroke-width="3" stroke-dasharray="10 8"/>'
        f'{"".join(halls)}'
        f'<g><rect x="672" y="20" width="116" height="42" rx="21" fill="{YELLOW}"/>'
        f'<text x="730" y="48" text-anchor="middle" font-size="21" font-weight="700" fill="{NAVY}" {FONT}>Vstup</text></g>'
        f'<g><circle cx="740" cy="100" r="18" fill="{YELLOW}" stroke="{NAVY}" stroke-width="3"/>'
        f'<text x="740" y="106" text-anchor="middle" font-size="16" font-weight="700" fill="{NAVY}" {FONT}>T</text>'
        f'<text x="740" y="146" text-anchor="middle" font-size="19" fill="{MUTED}" {FONT}>Tramvaj</text></g>'
    )
    return svg(width, height, body, f["areaMap"]["alt"])


def scene_mainframe():
    seats = "".join(f'<rect x="{80 + c * 52}" y="{330 + r * 34}" width="40" height="20" rx="6" fill="#2b3a7a"/>'
                    for r in range(3) for c in range(13))
    return (f'<rect width="800" height="450" fill="{NAVY}"/>'
            f'<rect x="150" y="50" width="500" height="200" rx="8" fill="{NAVY_2}" stroke="{YELLOW}" stroke-width="6"/>'
            f'<path d="M200 200 l80 -70 60 40 90 -100 80 60 90 -40" fill="none" stroke="{YELLOW}" stroke-width="8" stroke-linejoin="round"/>'
            f'<rect x="100" y="270" width="600" height="40" fill="#3b4a8f"/>'
            f'<circle cx="400" cy="250" r="16" fill="#fff"/><rect x="388" y="266" width="24" height="10" fill="#fff"/>{seats}')


def scene_terminal():
    rows = "".join(f'<rect x="{60 + r * 30}" y="{230 + r * 50}" width="{680 - r * 60}" height="34" rx="6" fill="#232b45"/>'
                   for r in range(4))
    return (f'<rect width="800" height="450" fill="{PAPER}"/>'
            f'<rect x="240" y="40" width="320" height="150" rx="8" fill="{NAVY}" stroke="#2a3350" stroke-width="3"/>'
            f'<path d="M280 90 h120 M280 120 h200 M280 150 h160" stroke="{YELLOW}" stroke-width="10" stroke-linecap="round"/>'
            f'<rect x="590" y="120" width="60" height="90" rx="6" fill="#0369a1"/>{rows}')


def scene_sandbox():
    return (f'<rect width="800" height="450" fill="#17140f"/>'
            f'<rect x="60" y="250" width="680" height="30" fill="#8a5a2b"/><rect x="90" y="280" width="20" height="140" fill="#8a5a2b"/>'
            f'<rect x="690" y="280" width="20" height="140" fill="#8a5a2b"/>'
            f'<rect x="120" y="170" width="220" height="80" rx="6" fill="#15803d"/>'
            f'<path d="M140 190 h60 v30 h50 M220 190 v40 M260 200 h60" stroke="{YELLOW}" stroke-width="6" fill="none"/>'
            f'<rect x="420" y="140" width="220" height="110" rx="8" fill="{NAVY_2}" stroke="#2a3350" stroke-width="3"/><rect x="400" y="245" width="260" height="10" fill="#3a4360"/>'
            f'<path d="M450 175 h100 M450 200 h150 M450 225 h80" stroke="#9ccbe8" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M330 120 l60 120" stroke="#8a93ad" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="M388 236 l8 14" stroke="#d33" stroke-width="6"/>')


def scene_arcade():
    cabinets = "".join(
        f'<g transform="translate({90 + i * 170} 150)"><rect width="120" height="260" rx="10" fill="{c}"/>'
        f'<rect x="15" y="25" width="90" height="80" rx="6" fill="{NAVY}"/>'
        f'<circle cx="35" cy="140" r="10" fill="{YELLOW}"/><circle cx="70" cy="140" r="10" fill="#fff"/></g>'
        for i, c in enumerate(["#15803d", "#be185d", "#0369a1", "#b45309"]))
    return (f'<rect width="800" height="450" fill="{NAVY}"/>'
            f'<rect x="200" y="30" width="400" height="90" rx="8" fill="{NAVY_2}" stroke="{YELLOW}" stroke-width="5"/>'
            f'<path d="M240 90 h40 v-30 h40 v30 h40 v-30" stroke="{YELLOW}" stroke-width="8" fill="none"/>{cabinets}')


def scene_nabrezi():
    return (f'<rect width="800" height="450" fill="#101528"/>'
            f'<circle cx="640" cy="90" r="46" fill="{YELLOW}"/>'
            f'<path d="M0 300 C200 270 500 320 800 290 V450 H0 Z" fill="#3f7a3a"/>'
            f'<path d="M0 380 C250 360 520 410 800 380 V450 H0 Z" fill="#4c86b3"/>'
            f'<path d="M220 300 L300 160 H500 L580 300 Z" fill="{NAVY}" stroke="#fff" stroke-width="4"/>'
            f'<path d="M300 160 L400 110 L500 160" fill="none" stroke="#fff" stroke-width="4"/>'
            f'<path d="M330 200 l40 60 M470 200 l-40 60" stroke="{YELLOW}" stroke-width="6" stroke-linecap="round"/>')


SCENES = {"mainframe": scene_mainframe, "terminal": scene_terminal, "sandbox": scene_sandbox,
          "arcade": scene_arcade, "nabrezi": scene_nabrezi}


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    site = ROOT / sys.argv[1]
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    written = {}
    f = data["festival"]
    written[f["image"]["src"]] = hero(f)
    written[f["areaMap"]["src"]] = area_map(data)
    for v in data["venues"]:
        written[v["image"]["src"]] = svg(800, 450, SCENES[v["slug"]](), v["image"]["alt"])
    for p in data["performers"]:
        written[p["image"]["src"]] = performer(p)
    for src, content in written.items():
        target = site / src
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    print(f"{site.relative_to(ROOT)}/images: {len(written)} souborů")


if __name__ == "__main__":
    main()
