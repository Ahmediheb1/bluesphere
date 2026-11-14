# BlueSphere 🔵

**NASA Space Apps Challenge 2026, "Flame in Freefall" challenge. Team BlueSphere, Sherbrooke, Canada.**

**Live app: https://bluesphere.streamlit.app**

BlueSphere is an AI-powered fire safety copilot. It turns decades of NASA microgravity combustion experiments into clear answers to keep astronauts safe on the Moon and Mars.

## The problem

NASA has run hundreds of fire experiments in orbit. The results are public in NASA's Physical Sciences Informatics (PSI) repository, but they are hard to find, harder to compare, and even harder to interpret. Meanwhile, the future Moon base and pressurized rovers will likely run at 30% oxygen or more, at 10.2 psi or less, to shorten the preparation before moonwalks. More oxygen means more fire risk.

## The key finding

In these PSI tables, solid materials, the materials habitats are made of, were tested in microgravity between 13.6% and 22.2% oxygen only, and no test was run in lunar or Martian gravity. The Moon base will be built where NASA has no fire data yet. BlueSphere shows this gap, and becomes more cautious inside it.

## What the app does

- **Flammability atlas**: 764 real tests from 8 NASA investigations (BASS-II, Saffire I to III, FLEX, FLEX-2, ACME BRE, CFI-G) on a single map, oxygen against air speed, plus a coverage map of the conditions no test has covered yet.
- **Ranking by environment**: space station, Moon base, lunar rover, ship to Mars, or a custom environment. A risk score from 0 to 100 with the team's expert weighting (oxygen 30%, material 25%, ventilation 25%, thickness 10%, pressure 10%), the closest NASA tests, and a confidence that drops where data is missing (cautious mode).
- **AI assistant**: answers questions about fire in space using only facts from NASA sources (`knowledge.py`), cites each source, and says "I don't know" when the information is missing. It runs on Claude Sonnet 5.5; the API key stays in the Streamlit secrets, never in this repository.
- **After the fire**: why the danger continues once the flame is out (Saffire-IV reignition, Mir, hidden flamelets), with every point sourced, and a checklist before restarting the ventilation.
- **Live fire detection** (demo, simulated data): four cabin sensors (CO2, CO, O2, temperature) replay a fire timed on Saffire-IV and V. The team's rules: CO2 gives the alert, CO confirms it, and the speed of change matters more than the value. A cautious mode alerts earlier in no-data zones, and the demo ends with "Can we restart the ventilation?".

## Run it locally

```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

To rebuild the data table from the raw PSI files:

```bash
py build_dataset.py
```

The assistant needs a Claude API key. On Streamlit Community Cloud, add `ANTHROPIC_API_KEY` under the app's Settings > Secrets. Never put the key in a file of this repository.

## Project files

Every file sits at the root of the repository, except the theme (`.streamlit/config.toml`).

| File | Role |
| --- | --- |
| `app.py` | Entry point: page setup and navigation |
| `home.py`, `atlas.py`, `ranking.py`, `assistant.py`, `detection.py`, `after.py`, `sources.py` | The pages of the app |
| `texts.py` | Every piece of text shown in the app |
| `data.py`, `charts.py`, `style.py` | Data loading, charts, look and feel |
| `risk.py` | The risk score, the confidence, and the ranking of tests |
| `knowledge.py` | The assistant's knowledge base: NASA facts and their sources |
| `sensors.py` | The simulated cabin sensors and the detection rules of the demo |
| `experiments.csv`, `investigations.csv` | The harmonized data used by the app |
| `PSI-*.csv` | The raw NASA test tables |
| `build_dataset.py` | Builds `experiments.csv` from the raw tables |
| `DATA.md` | How each NASA table is read |

## Data

All data comes from NASA's [Physical Sciences Informatics (PSI)](https://psi.nasa.gov/physci/repo/) repository, under a CC0 license. The raw test tables are the `PSI-*.csv` files, and the way they are read is explained in [DATA.md](DATA.md).

| Investigation | PSI | DOI |
| --- | --- | --- |
| BASS-II | [PSI-25](https://psi.nasa.gov/physci/repo/data/investigations/PSI-25) | [10.60555/4qc4-de67](https://doi.org/10.60555/4qc4-de67) |
| Saffire-I | [PSI-98](https://psi.nasa.gov/physci/repo/data/investigations/PSI-98) | [10.60555/0t15-1z43](https://doi.org/10.60555/0t15-1z43) |
| Saffire-II | [PSI-99](https://psi.nasa.gov/physci/repo/data/investigations/PSI-99) | [10.60555/2chp-m469](https://doi.org/10.60555/2chp-m469) |
| Saffire-III | [PSI-100](https://psi.nasa.gov/physci/repo/data/investigations/PSI-100) | [10.60555/040q-4h36](https://doi.org/10.60555/040q-4h36) |
| FLEX | [PSI-69](https://psi.nasa.gov/physci/repo/data/investigations/PSI-69) | [10.60555/mbq8-0451](https://doi.org/10.60555/mbq8-0451) |
| FLEX-2 | [PSI-68](https://psi.nasa.gov/physci/repo/data/investigations/PSI-68) | [10.60555/byp8-h018](https://doi.org/10.60555/byp8-h018) |
| ACME BRE | [PSI-20](https://psi.nasa.gov/physci/repo/data/investigations/PSI-20) | [10.60555/vb93-3y72](https://doi.org/10.60555/vb93-3y72) |
| CFI-G | [PSI-159](https://psi.nasa.gov/physci/repo/data/investigations/PSI-159) | [10.60555/cyt1-kh64](https://doi.org/10.60555/cyt1-kh64) |

The other sources (NASA papers on Saffire, NASA's 2015 guide to combustion science, NASA's exploration atmosphere) are listed on the app's Sources page.

## Use of AI

*Statement required by the NASA Space Apps rules.*

Claude (Anthropic) took part in writing the code with the BlueSphere team. The app's assistant runs on Claude, through an API key. The ideas, the Moon base scenario, the scientific choices and the risk analysis come from the BlueSphere team.

## License

Code under the MIT license. NASA data: CC0.
