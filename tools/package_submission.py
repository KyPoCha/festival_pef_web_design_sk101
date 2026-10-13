#!/usr/bin/env python3
"""Zabalí soubory k odevzdání jedné iterace do archivu ZIP a archiv ověří.

Použití:  python3 tools/package_submission.py 1

Výstup:   dist/sk101-iterace-01.zip, uvnitř jedna složka sk101-iterace-01/.
Do archivu jdou odevzdávané soubory iterace a soubory prezentace (.odp, .pptx,
.pdf) ze složky docs/presentation/iteration-0N/. Texty pro mluvčí se nebalí.
Skript používá jen standardní knihovnu. Při chybě končí návratovým kódem 1.
"""
import hashlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEAM = "sk101"

# Co se podle zadání odevzdává na konci které iterace (soubory i celé složky).
DELIVERABLES = {
    1: ["project-specification.md", "data.json"],
    2: ["prototype", "progress-02.md"],
    3: ["web", "progress-03.md"],
    4: ["web", "project-specification.md", "progress-04.md"],
    5: ["review.md"],
}
PRESENTATION_SUFFIXES = {".odp", ".pptx", ".ppt", ".pdf"}
JUNK = {".DS_Store", "Thumbs.db"}
PLACEHOLDER = re.compile(r"doplnit|_jméno_|TODO", re.IGNORECASE)

errors, warnings = [], []


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def collect(iteration):
    """Vrátí seznam dvojic (zdrojová cesta, cesta uvnitř složky v archivu)."""
    files = []
    for name in DELIVERABLES[iteration]:
        path = ROOT / name
        if path.is_dir():
            found = [p for p in sorted(path.rglob("*")) if p.is_file() and p.name not in JUNK]
            if not found:
                errors.append(f"složka {name}/ je prázdná")
            files += [(p, p.relative_to(ROOT).as_posix()) for p in found]
        elif path.is_file():
            files.append((path, name))
        else:
            errors.append(f"chybí odevzdávaný soubor: {name}")
    slides = ROOT / "docs" / "presentation" / f"iteration-{iteration:02d}"
    found = [p for p in sorted(slides.glob("*")) if p.suffix.lower() in PRESENTATION_SUFFIXES] if slides.is_dir() else []
    if not found:
        warnings.append(f"ve složce {slides.relative_to(ROOT)} není žádný soubor prezentace")
    files += [(p, p.name) for p in found]
    return files


def preflight(iteration, files):
    names = {inside for _, inside in files}
    if (ROOT / "data.json").is_file():
        result = subprocess.run([sys.executable, str(ROOT / "tools" / "validate_data.py")],
                                capture_output=True, text=True)
        last = (result.stdout.strip().splitlines() or ["bez výstupu"])[-1]
        print(f"Kontrola dat: {last}")
        if result.returncode != 0:
            errors.append("data.json neprošel kontrolním skriptem")

    for source, inside in files:
        if source.suffix == ".md":
            text = source.read_text(encoding="utf-8")
            for number, line in enumerate(text.splitlines(), 1):
                if PLACEHOLDER.search(line):
                    warnings.append(f"{inside}:{number} – nedoplněné místo: {line.strip()[:70]}")
            for ref in sorted(set(re.findall(r"`((?:docs|tools)/[^`]+)`", text))):
                warnings.append(f"{inside} odkazuje na soubor, který v archivu není: {ref}")
        if source.suffix == ".odp":
            with zipfile.ZipFile(source) as odp:
                content = odp.read("content.xml").decode("utf-8")
            if re.search(r">Mluvčí \d<", content):
                warnings.append(f"{inside} – v zápatí snímků jsou zástupná jména „Mluvčí 1–4“")

    decks = [s for s, _ in files if s.suffix.lower() in {".odp", ".pptx", ".ppt"}]
    for pdf in (s for s, _ in files if s.suffix.lower() == ".pdf" and s.parent.name.startswith("iteration-")):
        for deck in decks:
            if deck.stem == pdf.stem and deck.stat().st_mtime > pdf.stat().st_mtime:
                warnings.append(f"{pdf.name} je starší než {deck.name} – exportujte PDF znovu")
    if len(names) != len(files):
        errors.append("dva soubory by v archivu měly stejnou cestu")


def build(iteration, files):
    folder = f"{TEAM}-iterace-{iteration:02d}"
    target = ROOT / "dist" / f"{folder}.zip"
    target.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for source, inside in files:
            archive.write(source, f"{folder}/{inside}")
    return target, folder


def verify(target, folder, files):
    """Znovu otevře hotový archiv a porovná ho se zdrojovými soubory."""
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            errors.append("archiv je poškozený")
        listed = {i.filename: i for i in archive.infolist() if not i.is_dir()}
        expected = {f"{folder}/{inside}": source for source, inside in files}
        for name in sorted(set(listed) - set(expected)):
            errors.append(f"v archivu je soubor navíc: {name}")
        for name, source in expected.items():
            if name not in listed:
                errors.append(f"v archivu chybí: {name}")
            elif sha256(archive.read(name)) != sha256(source.read_bytes()):
                errors.append(f"obsah se liší od zdroje: {name}")
        for name in listed:
            if not name.startswith(f"{folder}/") or "__MACOSX" in name or Path(name).name in JUNK:
                errors.append(f"nežádoucí položka v archivu: {name}")
        print(f"\nArchiv: {target.relative_to(ROOT)}  ({target.stat().st_size / 1024:.0f} kB)")
        for name, info in sorted(listed.items()):
            print(f"  {info.file_size / 1024:8.1f} kB  {name}")


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) not in DELIVERABLES:
        raise SystemExit(__doc__)
    iteration = int(sys.argv[1])
    files = collect(iteration)
    preflight(iteration, files)
    if not errors:
        target, folder = build(iteration, files)
        verify(target, folder, files)
    print()
    for message in warnings:
        print(f"UPOZORNĚNÍ: {message}")
    for message in errors:
        print(f"CHYBA: {message}")
    print(f"Výsledek: {len(errors)} chyb, {len(warnings)} upozornění")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
