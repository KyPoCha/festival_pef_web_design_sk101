#!/usr/bin/env python3
"""Sestaví prezentaci ve formátu ODP ze šablony KIT a z popisu snímků v JSON.

Použití:
    python3 tools/build_presentation.py 16-9_blue_cze.odp \
        docs/presentation/iteration-01/slides.json \
        docs/presentation/iteration-01/tranzistor-iterace-01.odp

Ze šablony se beze změny přebírají předlohy snímků, styly a obrázky (styles.xml,
media/). Skript generuje pouze content.xml. Používá jen standardní knihovnu.

Formát slides.json:
    {
      "footer": "text v zápatí",
      "speakers": ["Jméno 1", "Jméno 2", ...],
      "slides": [
        {"layout": "title", "title": "...", "subtitle": "...", "corner": "..."},
        {"layout": "content", "speaker": 1, "title": "...", "items": [...]},
        {"layout": "two", "speaker": 2, "title": "...", "left": [...], "right": [...]}
      ]
    }
Položka seznamu je řetězec (odrážka), {"sub": "..."} (odrážka druhé úrovně)
nebo {"h": "..."} (mezititulek bez odrážky). **Text** mezi hvězdičkami je tučný.
"""
import json
import re
import sys
import zipfile
from xml.sax.saxutils import escape

BLUE = "#005490"
PT = 1 / 72  # palce na bod

NAMESPACES = (
    'xmlns:dom="http://www.w3.org/2001/xml-events" '
    'xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" '
    'xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" '
    'xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0" '
    'xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" '
    'xmlns:smil="urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0" '
    'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
    'xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" '
    'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
    'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
    'xmlns:xlink="http://www.w3.org/1999/xlink" '
    'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" office:version="1.4"'
)

# Předlohy a rozměry zástupných rámců převzaté ze šablony 16-9_blue_cze.odp.
MASTER_TITLE = ("Master1-Layout1-cust-Úvodní-stránka-prezentace", "Master1-PPL1")
MASTER_CONTENT = ("Master2-Layout2-cust-Nadpis-a-obsah", "Master2-PPL2")
MASTER_TWO = ("Master2-Layout4-cust-Dva-obsahy", "Master2-PPL4")

styles = {}  # název stylu -> XML


def frame_style(valign, halign="left", shrink=False):
    name = f"tzF-{valign}-{halign}{'-fit' if shrink else ''}"
    fit = ' style:shrink-to-fit="true"' if shrink else ""
    styles[name] = (
        f'<style:style style:family="presentation" style:name="{name}">'
        '<style:graphic-properties fo:wrap-option="wrap" fo:padding-top="0.05in" fo:padding-bottom="0.05in" '
        f'fo:padding-left="0.1in" fo:padding-right="0.1in" draw:textarea-vertical-align="{valign}" '
        f'draw:textarea-horizontal-align="{halign}" draw:fill="none" draw:stroke="none" '
        f'draw:auto-grow-width="false" draw:auto-grow-height="false"{fit}/>'
        '<style:paragraph-properties style:font-independent-line-spacing="true" style:writing-mode="lr-tb"/>'
        "</style:style>"
    )
    return name


def para_style(align="left", left=0.0, indent=0.0, top=0.0):
    name = f"tzP-{align}-{round(left * 1000)}-{round(-indent * 1000)}-{round(top * 1000)}"
    styles[name] = (
        f'<style:style style:family="paragraph" style:name="{name}">'
        f'<style:paragraph-properties fo:line-height="100%" fo:text-align="{align}" '
        f'fo:margin-left="{left}in" fo:margin-right="0in" fo:text-indent="{indent}in" '
        f'fo:margin-top="{top}in" fo:margin-bottom="0in" style:writing-mode="lr-tb"/>'
        "</style:style>"
    )
    return name


def text_style(points, color="#000000", bold=False):
    name = f"tzT-{points}-{color[1:]}{'-b' if bold else ''}"
    size = f"{points * PT:.5f}in"
    weight = "bold" if bold else "normal"
    styles[name] = (
        f'<style:style style:family="text" style:name="{name}">'
        f'<style:text-properties fo:color="{color}" fo:font-family="Calibri" fo:font-size="{size}" '
        f'style:font-size-asian="{size}" style:font-size-complex="{size}" fo:language="cs" fo:country="CZ" '
        f'fo:font-style="normal" fo:font-weight="{weight}" style:font-weight-asian="{weight}" '
        f'style:font-weight-complex="{weight}" style:text-underline-style="none" style:letter-kerning="true"/>'
        "</style:style>"
    )
    return name


def page_style(color):
    name = f"tzPage-{color[1:]}"
    styles[name] = (
        f'<style:style style:family="drawing-page" style:name="{name}">'
        f'<style:drawing-page-properties draw:fill="solid" draw:fill-color="{color}" draw:opacity="100%" '
        'presentation:visibility="visible" draw:background-size="border" '
        'presentation:background-objects-visible="true" presentation:background-visible="true" '
        'presentation:display-header="false" presentation:display-footer="false" '
        'presentation:display-page-number="false" presentation:display-date-time="false"/>'
        "</style:style>"
    )
    return name


LIST_STYLE = "tzList"
styles[LIST_STYLE] = (
    f'<text:list-style style:name="{LIST_STYLE}">'
    + "".join(
        f'<text:list-level-style-bullet text:level="{level}" text:bullet-char="•">'
        f'<style:list-level-properties text:space-before="{before}in" text:min-label-width="{label}in"/>'
        '<style:text-properties fo:font-family="Arial" style:font-family-generic="swiss" fo:font-size="100%"/>'
        "</text:list-level-style-bullet>"
        for level, before, label in ((1, 0, 0.3), (2, 0.3, 0.25))
    )
    + "</text:list-style>"
)

next_id = [1000]


def new_id():
    next_id[0] += 1
    return f"id{next_id[0]}"


def spans(text, points, color="#000000", bold=False):
    """Převede text s **tučnými** úseky na posloupnost text:span."""
    out = []
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if part:
            style = text_style(points, color, bold or i % 2 == 1)
            out.append(f'<text:span text:style-name="{style}">{escape(part)}</text:span>')
    return "".join(out)


def frame(cls, name, x, y, w, h, style, inner, placeholder="false"):
    return (
        f'<draw:frame draw:id="{new_id()}" presentation:style-name="{style}" draw:name="{escape(name)}" '
        f'svg:x="{x}in" svg:y="{y}in" svg:width="{w}in" svg:height="{h}in" '
        f'presentation:class="{cls}" presentation:placeholder="{placeholder}">'
        f"<draw:text-box>{inner}</draw:text-box><svg:title/><svg:desc/></draw:frame>"
    )


def paragraph(text, points, align="left", color="#000000", bold=False, top=0.0):
    return f'<text:p text:style-name="{para_style(align, top=top)}">{spans(text, points, color, bold)}</text:p>'


def body(items, points):
    """Sestaví obsah textového rámce ze seznamu položek."""
    sub_points = points - 3
    out = []
    for n, item in enumerate(items):
        gap = 0.0 if n == 0 else round(points * PT * 0.42, 4)
        if isinstance(item, dict) and "h" in item:
            out.append(paragraph(item["h"], points + 1, color=BLUE, bold=True, top=gap * 1.5))
        elif isinstance(item, dict) and "sub" in item:
            p = (f'<text:p text:style-name="{para_style("left", 0.55, -0.25, round(gap * 0.5, 4))}">'
                 f'{spans(item["sub"], sub_points)}</text:p>')
            out.append(f'<text:list text:style-name="{LIST_STYLE}"><text:list-item>'
                       f'<text:list text:style-name="{LIST_STYLE}"><text:list-item>{p}</text:list-item></text:list>'
                       "</text:list-item></text:list>")
        else:
            p = f'<text:p text:style-name="{para_style("left", 0.3, -0.3, gap)}">{spans(item, points)}</text:p>'
            out.append(f'<text:list text:style-name="{LIST_STYLE}"><text:list-item>{p}</text:list-item></text:list>')
    return "".join(out)


def footer_frames(deck, slide):
    speakers = deck.get("speakers", [])
    number = slide.get("speaker")
    who = speakers[number - 1] if number and number <= len(speakers) else ""
    page_number = (
        f'<text:p text:style-name="{para_style("center")}"><text:span text:style-name="{text_style(16, "#ffffff")}">'
        '<text:page-number style:num-format="1" text:fixed="false">1</text:page-number></text:span></text:p>'
    )
    return (
        frame("outline", "Zápatí – text", 3.11003, 5.17497, 4.17361, 0.23611, frame_style("middle"),
              paragraph(deck.get("footer", ""), 13, color="#ffffff", bold=True))
        + frame("outline", "Zápatí – mluvčí", 3.10938, 5.41146, 4.17361, 0.21354, frame_style("middle"),
                paragraph(who, 11, color="#ffffff", bold=True))
        + frame("page-number", "Číslo snímku", 8.37489, 5.25372, 1.1138, 0.30035,
                frame_style("middle", "center"), page_number)
    )


def slide_title(slide):
    return frame("title", "Nadpis", 0.5, 0.21379, 9, 0.70874, frame_style("middle", "center", shrink=True),
                 paragraph(slide["title"], slide.get("titleSize", 30), "center", BLUE, bold=True))


def build_slide(deck, slide, index):
    layout = slide["layout"]
    if layout == "title":
        master, ppl = MASTER_TITLE
        page = page_style(BLUE)
        inner = (
            frame("title", "Nadpis", 0.75, 3.08812, 8.5, 0.82686, frame_style("bottom", "center"),
                  paragraph(slide["title"], 40, "center", "#ffffff", bold=True))
            + frame("subtitle", "Podnadpis", 1.0, 3.91465, 8.0, 0.78782, frame_style("top", "center"),
                    paragraph(slide.get("subtitle", ""), 22, "center", "#ffffff", bold=True))
            + frame("outline", "Tým", 5.78749, 4.8206, 4.01736, 0.64974, frame_style("bottom"),
                    paragraph(slide.get("corner", ""), 16, "right", "#ffffff", bold=True))
        )
    elif layout == "content":
        master, ppl = MASTER_CONTENT
        page = page_style("#ffffff")
        inner = (
            slide_title(slide)
            + frame("outline", "Obsah", 0.5, 1.00128, 9, 3.7012, frame_style("top", shrink=True),
                    body(slide["items"], slide.get("size", 20)))
            + footer_frames(deck, slide)
        )
    elif layout == "two":
        master, ppl = MASTER_TWO
        page = page_style("#ffffff")
        size = slide.get("size", 16)
        inner = (
            slide_title(slide)
            + frame("outline", "Obsah vlevo", 0.5, 1.00128, 4.41667, 3.7012, frame_style("top", shrink=True),
                    body(slide["left"], size))
            + frame("outline", "Obsah vpravo", 5.08333, 1.00128, 4.41667, 3.7012, frame_style("top", shrink=True),
                    body(slide["right"], size))
            + footer_frames(deck, slide)
        )
    else:
        raise SystemExit(f"Neznámé rozložení snímku: {layout}")
    return (
        f'<draw:page draw:name="Snimek{index}" draw:style-name="{page}" draw:master-page-name="{master}" '
        f'presentation:presentation-page-layout-name="{ppl}" draw:id="Slide-{index}">{inner}</draw:page>'
    )


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    template, source, output = sys.argv[1:]
    with open(source, encoding="utf-8") as f:
        deck = json.load(f)

    pages = "".join(build_slide(deck, slide, n) for n, slide in enumerate(deck["slides"], 1))
    content = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f"<office:document-content {NAMESPACES}>"
        f'<office:automatic-styles>{"".join(styles.values())}</office:automatic-styles>'
        f"<office:body><office:presentation>{pages}<presentation:settings/></office:presentation></office:body>"
        "</office:document-content>"
    )

    with zipfile.ZipFile(template) as src, zipfile.ZipFile(output, "w") as dst:
        # mimetype musí být první položkou archivu a nesmí být komprimovaný
        dst.writestr(zipfile.ZipInfo("mimetype"), src.read("mimetype"), zipfile.ZIP_STORED)
        for info in src.infolist():
            if info.filename == "mimetype" or info.filename.startswith("Thumbnails/"):
                continue
            data = src.read(info.filename)
            if info.filename == "content.xml":
                data = content.encode("utf-8")
            elif info.filename == "META-INF/manifest.xml":
                data = re.sub(rb'<manifest:file-entry manifest:full-path="Thumbnails/[^>]*/>', b"", data)
            dst.writestr(info.filename, data, zipfile.ZIP_DEFLATED)
    print(f"{output}: {len(deck['slides'])} snímků")


if __name__ == "__main__":
    main()
