# Project plan – Tranzistor festival website (team sk101)

Working document for the team. Deliverables are written in Czech; this plan and code comments are in English.
Source of requirements: the Moodle assignment "Požadavky na projekt a dílčí úkoly | prezenční".

## 1. What we are building

A client-side website for a fictional tech festival (**Tranzistor 2027**, Pražská tržnice, 4–6 June 2027), built up over six seminars and finished with a documented final submission. The grade depends on UX and information architecture, semantic and valid HTML, WCAG 2.0 AA, responsiveness, SEO/AEO, and on being able to explain how AI was used and how its output was verified.

Hard constraints:

- Plain HTML, CSS and JavaScript. No Node.js, build step, package manager, backend or database needed to run the site.
- All texts and images are AI-generated; the team answers for them.
- Outputs 1 and 2 (specification + data, UX design + prototype) are binding. Later changes are limited to roughly 15 % and each needs a reason that comes from validation, review or consultation.
- Presentations are 3–5 minutes and may only show material submitted before the seminar.

## 2. Roadmap

| # | Due | Deliverables | Status |
|---|---|---|---|
| 1 | Seminar 2 | `project-specification.md`, `data.json` | Submitted; data fixed to 1.1.0 in iteration 2 after feedback |
| 2 | Seminar 3 | `prototype/` (runs without install), `progress-02.md` | Submitted 2026-11-08 (commit 7142efb, `dist/sk101-iterace-02.zip`) |
| 3 | Seminar 4 | `web/` first working implementation, `progress-03.md` | Ready for submission (157 pre-rendered pages; tests 125 + 45 pass) |
| 4 | Seminar 5 | review-ready `web/`, `progress-04.md` | Not started |
| 5 | Seminar 6 | `review.md` for the project assigned to us | Not started |
| 6 | Final | `web/`, `documentation.md`, `review/received-review.md`, full folder structure | Not started |

Seminar dates are not in the assignment text – add them here once known.

## 3. Repository layout

```
/                              ← this is the "projekt/" folder from the assignment
├── project-specification.md   submitted (iteration 1, then final)
├── data.json                  submitted (iteration 1, then final)
├── prototype/                 submitted (iteration 2, then final); js/data.js and images/ are generated
├── web/                       submitted (iterations 3, 4, final)
│   ├── index.html …
│   ├── css/  js/  images/
├── documentation.md           submitted (final)
├── review/received-review.md  submitted (final)
├── progress-02.md … 04.md     submitted per iteration
├── docs/                      working files, not required by the assignment
│   ├── plan.md                this file
│   ├── ai-usage/iteration-0N.md          what the AI did and checked mechanically
│   ├── team-work-flow/iteration-0N.md    what the team must do, decide and record
│   ├── team-work-flow/controls/iteration-0N.md   manual control sheet
│   ├── presentation/iteration-0N/        slides (.odp, .pdf), slides.json, speaker texts, img/
│   └── design-picker/iteration-0N/       design voting page (published as an artifact with shared votes)
└── tools/                     dev-only scripts (Python stdlib); the site never depends on them
    ├── validate_data.py       data checks, incl. js/data.js and images in prototype/ and web/
    ├── build_web_data.py      data.json → <site>/js/data.js
    ├── generate_images.py     SVG illustrations and area map → <site>/images/
    ├── build_picker.py        design picker page with the prototype's styles scoped to phone previews
    ├── test_prototype.js      browser test (Node + playwright-core, dev only)
    ├── package_submission.py  zip of one iteration's deliverables
    └── build_presentation.py  builds the .odp from the KIT template and slides.json (text and screenshots)
```

## 4. Iterations

### Iteration 1 – specification and data (→ seminar 2)

- [x] Festival identity, purpose, target groups, information architecture, five scenarios (three key ones)
- [x] `data.json`: 3 days, 5 stages, 67 performers, 77 programme items, 7 tracks, practical info
- [x] `tools/validate_data.py` – consistency checker, itself tested with 14 injected errors
- [x] AI log: `docs/ai-usage/iteration-01.md`
- [x] Presentation: nine slides in the KIT template plus a Czech text per speaker, `docs/presentation/iteration-01/`
- [x] Team task list and manual control sheet, `docs/team-work-flow/`
- [ ] **Team:** everything in `docs/team-work-flow/iteration-01.md` and `docs/team-work-flow/controls/iteration-01.md`

Presentation at seminar 2 (about 4.5 min, limit is 3–5):

| Speaker | Slides | Topic |
|---|---|---|
| 1 | 1–3 | Festival and purpose of the site |
| 2 | 4–5 | Target groups, information architecture |
| 3 | 6–7 | Key scenarios S1 and S2 |
| 4 | 8–9 | Data, AI use and verification |

Rebuild after editing `slides.json`: `python3 tools/build_presentation.py 16-9_blue_cze.odp docs/presentation/iteration-01/slides.json docs/presentation/iteration-01/tranzistor-iterace-01.odp`. The presentation file must be uploaded to Moodle before the seminar.

### Iteration 2 – UX design and prototype (→ seminar 3)

- [x] Find and fix what was missing in `data.json` (images, area map, edition history, press contact, ticket link, panellists' tracks) → 1.1.0; spec 1.1 with change log in chapter 8
- [x] Validator extended (83 errors on 1.0.0, 0 on 1.1.0)
- [x] Teammate's own prototype (Downloads) reviewed: bottom bar and dark theme adopted as variants; `fetch` from `file://` shows only 16/77 items, so not adopted
- [x] `prototype/`: 11 pages, mobile-first, F1–F6 working, design variants via `?ui=`
- [x] Design picker published, vote saved: Kyber · bottom bar · tiles · text button → now the default; Material-style SVG icons and corner badge from the vote note
- [x] Browser test 168/168, Kyber contrast ≥ 7.4:1, `progress-02.md`, AI log, slides + speaker texts
- [ ] **Team:** everything in `docs/team-work-flow/iteration-02.md` and `controls/iteration-02.md`; other members vote or confirm on the picker (share it first)

Presentation at seminar 3 (about 4 min):

| Speaker | Slides | Topic |
|---|---|---|
| 1 | 1–3 | What we did, the data fix |
| 2 | 4–5 | Mobile-first prototype, design decision |
| 3 | 6–7 | Scenarios S1 and S2 in the prototype |
| 4 | 8–9 | Interactive features, AI use and verification |

Rebuild: `python3 tools/generate_images.py prototype && python3 tools/build_web_data.py prototype` after any data change; `python3 tools/build_picker.py 2` after CSS changes; `python3 tools/package_submission.py 2` for the Moodle zip.

### Iteration 3 – first implementation (→ seminar 4)

- Home page, at least one other distinct page, working main navigation, mobile-first responsive layout, working interactive features, semantic HTML.
- Research current UX and design best practices and record what was applied – this is a required chapter of `progress-03.md`.
- `progress-03.md`: what is implemented, best practices and how they were applied, what changed against the prototype and why, tests performed, AI use.
- [x] `web/` generated by `python3 tools/build_site.py` (157 pages, metadata, JSON-LD, sitemap, robots, llms.txt, OG image)
- [x] Tests: `tools/test_web.js` (125 checks), `tools/test_accessibility.js` (45 checks), data validator 0 errors
- [x] `progress-03.md`, AI log `docs/ai-usage/iteration-03.md`, spec 1.2 (detail URLs, bottom bar, chapter 8 restored)
- [ ] W3C HTML validator (vnu.jar download was blocked in the AI environment; run it or validator.w3.org by hand)
- [x] Presentation for seminar 4 (`docs/presentation/iteration-03/`, 9 slides, 4 speaker texts) and `dist/sk101-iterace-03.zip`

Rebuild after any change to `data.json`, `tools/build_site.py` or the CSS/JS: `python3 tools/build_site.py` (also regenerates `web/js/data.js` and images).

### Iteration 4 – review-ready version (→ seminar 5)

- All main sections present, scenarios S1–S3 can be completed, search field and results page, usable on mobile and desktop, complete content, no known blocking bugs.
- AI-generated images for performers and stages, with alt text; image path and alt text added to `data.json`.
- Checks: W3C HTML validator, WCAG AA contrast and keyboard pass, screen-reader smoke test, no horizontal overflow from 320 px up, Lighthouse.
- `progress-04.md`: current state, known shortcomings, what was tested and how, AI use.
- Hand `web/` and `project-specification.md` to the reviewing team.

### Iteration 5 – cross-review of another team (→ seminar 6)

- Walk two of their key scenarios.
- Two formal methods: heuristic evaluation (Nielsen's ten heuristics) and cognitive walkthrough; add a WCAG 2.0 AA checklist pass.
- Every finding: severity (critical / significant / minor), how it was found, reasoning, proposed fix. Each finding reproduced by a team member – AI may suggest findings, it does not confirm them.
- `review.md`: methodology and list of findings. Presentation: method, top 3–5 findings.

### Iteration 6 – final submission

- Apply the review we received; record each comment in the cross-review table (accepted / rejected with reasoning).
- SEO and AEO/GEO: research current practice, then implement – per-page `<title>` and description, Open Graph, JSON-LD (`Festival`, `Event`, `Person`/`MusicGroup`, `Place`, `FAQPage`, `BreadcrumbList`) that matches visible content, `sitemap.xml`, `robots.txt`, possibly `llms.txt`.
- `documentation.md`: project evolution and changes, cross-review table, workflow, AI use with representative prompts and a critical assessment.
- Final folder structure exactly as the assignment prescribes.

## 5. Planned interactive features

| # | Feature | User need | Scenario |
|---|---|---|---|
| F1 | Programme filter by day, stage, track, format, level, language, family-friendly; state kept in the URL | Narrow 77 items down to the few that matter | S1, S2, S3 |
| F2 | My programme – save and remove items, stored in `localStorage`, counter in the navigation | Build a personal plan without an account | S1, S2 |
| F3 | Time-conflict detection in My programme | Notice overlapping items before the festival, not on the spot | S2 |
| F4 | Search across performers, programme and stages, ignoring diacritics and case, with a results page | Find something from a half-remembered name | S2, S5 |
| F5 | "Now and next" block per stage, driven by the current time, with a simulated clock for testing | Decide where to go while on site | S4 |
| F6 | Performer list filter and sort | Browse 67 performers by type and track | S2 |

The assignment requires at least three; F1–F4 are the core, F5 and F6 follow if time allows.

## 6. Technical decisions

| # | Decision | Reason |
|---|---|---|
| D1 | Vanilla HTML, CSS, JavaScript; no framework, no build | Required by the assignment |
| D2 | `data.json` is the single source of truth; `<site>/js/data.js` is generated from it by `tools/build_web_data.py` and checked for equality | `fetch()` of a local JSON file fails when the site is opened via `file://`; the assignment allows a JS-friendly copy if it is derivable and consistent |
| D3 | Prototype: one template per detail type with `?id=`. Web (from iteration 3): every page is pre-rendered by `tools/build_site.py` to `program/<slug>.html`, `ucinkujici/<slug>.html`, `sceny/<slug>.html` | Content in HTML for search engines, AI crawlers and no-JS visitors; the site still runs from the file system without a server – the script is only needed to regenerate |
| D4 | Filters live in the URL query string; saved items live in `localStorage` | Filters survive Back and can be shared; the personal plan survives a browser restart |
| D5 | Stable IDs (`e001`, `p001`, `v01`) plus readable slugs | IDs never change; slugs are available for readable URLs |
| D6 | Site language is Czech; identifiers and code comments are English | Czech audience; conventional code style |
| D7 | Prototype: design variants switch with `?ui=`. Web: only the chosen look, CSS flattened (former variant rules keep their specificity via `:root`) | Variants were for deciding; the web carries only the decision |
| D8 | Classic `<script>` files, no ES modules | Browsers refuse module scripts from `file://` |
| D9 | Icons are inline SVG with Material Icons shapes (Apache License 2.0) | No icon font or network needed; matches the team's request for MUI-like icons |

Resolved in iteration 3: pre-generated static pages (chosen by Kyrylo on 2026-11-08). The URL scheme change is in section 7 and in spec chapter 8.

## 7. Change log against outputs 1 and 2

Every change to the specification or data after seminar 2 goes here, with the validation, review or consultation that caused it. This table feeds the "Vývoj projektu a změny" chapter of `documentation.md`.

| Date | What changed | Why | Triggered by |
|---|---|---|---|
| 2026-11-08 | `data.json` 1.1.0: images, area map, edition history, press contact, ticket link, tracks of three panellists | Spec promised these on pages; assignment requires AI images | Feedback after seminar 2 ("something is missing in data.json"), check of data against spec |
| 2026-11-08 | Spec 1.1: data model rows and consistency rules updated, chapter 8 added | Follows the data change | Same |
| 2026-11-08 | Mobile navigation moves to a bottom bar (spec 4.2 updated in 1.2) | Team vote on the design picker | Team vote |
| 2026-11-08 | Spec 1.2: detail pages get their own files with readable URLs instead of `?id=` (spec 4.1); chapter 8 restored (it was missing from the iteration 2 commit although progress-02 and the slides refer to it) | Content in HTML for SEO/AEO and no-JS visitors | Iteration 3 assignment, decision D3 |

## 8. Verification approach

"We checked it with AI" does not count as validation. For every iteration:

- **Data** – `python3 tools/validate_data.py` must report 0 errors after any edit.
- **Scenarios** – a team member walks S1–S3 by hand on a phone and on desktop and notes the result.
- **HTML and accessibility** – W3C validator, keyboard-only pass, contrast check, screen-reader smoke test.
- **AI text and images** – read by a human; factual claims about real places checked against a primary source.
- **Record** – what was accepted, changed and rejected goes into the AI log for that iteration.

## 9. Per-iteration records

Each iteration leaves four things in `docs/`, all in Czech so they can be pasted into `progress-0N.md` and `documentation.md`:

| File | Written by | Content |
|---|---|---|
| `ai-usage/iteration-0N.md` | AI | Tools, what AI produced, mechanical checks, limits and errors of its own output (no prompts) |
| `team-work-flow/iteration-0N.md` | Team | Data to fill in, AI decisions to confirm, accepted / changed / rejected, errors the team found, submission steps |
| `team-work-flow/controls/iteration-0N.md` | Team | Manual controls with procedure, who, when, result |
| `presentation/iteration-0N/` | AI drafts, team finalises | Slides and one text file per speaker |

The AI never fills in the team's files with results, and never claims a manual check on the team's behalf.

## 10. Risks

| Risk | Mitigation |
|---|---|
| A generated name matches a real person or band | Manual search of performer names before submission; rename on a hit |
| Real-world facts (address, transit) are wrong | Check against the venue's and the transit operator's own websites |
| Scope creep beyond the 15 % limit | Section 7 change log; new ideas go into F5/F6 or are dropped |
| JS-rendered detail pages hurt SEO/AEO scoring | Resolved: pre-rendered pages (D3) |
| Site breaks when opened from the file system | D2; test by double-clicking `index.html` on every iteration |
| Accessibility left to the end | Semantic HTML and keyboard support from the prototype onward |

## 11. Team

Roster and responsibilities are in `docs/team-work-flow/README.md`.
