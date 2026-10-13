# festival_pef_web_design_sk101

University project (PEF ČZU, team sk101): website for the fictional tech festival **Tranzistor 2027**.

| File | Purpose |
|---|---|
| [project-specification.md](project-specification.md) | Festival identity, purpose, target groups, information architecture, scenarios (Czech) |
| [data.json](data.json) | Data foundation: festival, days, stages, performers, programme, practical info |
| [docs/plan.md](docs/plan.md) | Plan for the whole project, iteration by iteration |
| [docs/ai-usage/](docs/ai-usage/) | AI usage log, one file per iteration |
| [docs/team-work-flow/](docs/team-work-flow/) | Team tasks and manual control sheets, one per iteration |
| [docs/presentation/](docs/presentation/) | Slides and speaker texts, one folder per iteration |
| [tools/validate_data.py](tools/validate_data.py) | Consistency check for `data.json` |
| [tools/build_presentation.py](tools/build_presentation.py) | Builds the `.odp` slides from the KIT template and `slides.json` |

Check the data after every edit:

```sh
python3 tools/validate_data.py
```
