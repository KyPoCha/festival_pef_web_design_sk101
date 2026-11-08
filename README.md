# festival_pef_web_design_sk101

University project (PEF ČZU, team sk101): website for the fictional tech festival **Tranzistor 2027**.

| File | Purpose |
|---|---|
| [project-specification.md](project-specification.md) | Festival identity, purpose, target groups, information architecture, scenarios (Czech) |
| [data.json](data.json) | Data foundation: festival, days, stages, performers, programme, practical info (v1.1.0) |
| [prototype/](prototype/) | Clickable prototype – open `prototype/index.html`, no install needed |
| [progress-02.md](progress-02.md) | Iteration 2 report (Czech) |
| [docs/plan.md](docs/plan.md) | Plan for the whole project, iteration by iteration |
| [docs/ai-usage/](docs/ai-usage/) | AI usage log, one file per iteration |
| [docs/team-work-flow/](docs/team-work-flow/) | Team tasks and manual control sheets, one per iteration |
| [docs/presentation/](docs/presentation/) | Slides and speaker texts, one folder per iteration |
| [docs/design-picker/](docs/design-picker/) | Design voting page, one folder per iteration |
| [tools/validate_data.py](tools/validate_data.py) | Consistency check for `data.json` |
| [tools/build_presentation.py](tools/build_presentation.py) | Builds the `.odp` slides from the KIT template and `slides.json` |
| [tools/build_web_data.py](tools/build_web_data.py) | Writes `js/data.js` for the prototype or web from `data.json` |
| [tools/generate_images.py](tools/generate_images.py) | Generates the SVG illustrations and area map |
| [tools/build_picker.py](tools/build_picker.py) | Builds the design picker page |
| [tools/test_prototype.js](tools/test_prototype.js) | Browser test of pages and scenarios (instructions in the file header) |
| [tools/test_accessibility.js](tools/test_accessibility.js) | Accessibility audit: axe-core WCAG 2.2 AA, keyboard focus, reflow, reduced motion |
| [tools/package_submission.py](tools/package_submission.py) | Zips one iteration's deliverables for Moodle |

After editing `data.json`:

```sh
python3 tools/generate_images.py prototype
python3 tools/build_web_data.py prototype
python3 tools/validate_data.py
```
