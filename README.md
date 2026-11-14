# BlueSphere 🔵

**NASA Space Apps Challenge 2026 · Défi « Flame in Freefall » · Équipe BlueSphere (Sherbrooke)**

BlueSphere est un copilote de sécurité incendie alimenté par l'IA. Il transforme des décennies d'expériences de la NASA sur le feu en microgravité en réponses claires, pour protéger les astronautes sur la Lune et sur Mars.

*BlueSphere is an AI-powered fire safety copilot that turns decades of NASA microgravity combustion experiments into clear answers to keep astronauts safe on the Moon and Mars.*

## Ce que fait l'application

- **Atlas d'inflammabilité** : 764 essais réels de 8 expériences de la NASA (BASS-II, Saffire I à III, FLEX, FLEX-2, ACME BRE, CFI-G) réunis sur une seule carte, oxygène en fonction de la vitesse de l'air.
- **Les zones sans données** : ce que la NASA n'a pas encore testé, à commencer par l'atmosphère de la future base lunaire (30 % d'O₂ ou plus, à 10,2 psi ou moins) en gravité lunaire.
- **Classement selon l'environnement** : station spatiale, base lunaire, rover lunaire, vaisseau vers Mars ou environnement personnalisé. Un score de risque de 0 à 100 avec la pondération de l'équipe (oxygène 30 %, matériau 25 %, ventilation 25 %, épaisseur 10 %, pression 10 %), les essais de la NASA les plus proches, et une confiance qui baisse là où les données manquent (mode prudent).
- **Assistant d'IA** : il répond aux questions sur le feu dans l'espace seulement avec des faits tirés de sources de la NASA (`knowledge.py`), cite chaque source et dit « je ne sais pas » quand l'information manque. Modèle Claude Sonnet 5.5 ; la clé de l'API reste dans les secrets de Streamlit, jamais sur GitHub.
- Application bilingue (français et anglais) : `?lang=fr` ou `?lang=en` dans le lien.

## Lancer en local

```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Pour reconstruire le tableau de données à partir des fichiers bruts de PSI :

```bash
py build_dataset.py
```

## Fichiers du projet

Tous les fichiers sont à la racine du dépôt, sauf le thème (`.streamlit/config.toml`).

| Fichier | Rôle |
| --- | --- |
| `app.py` | Point d'entrée : langue, menu et pages |
| `accueil.py`, `atlas.py`, `classement.py`, `assistant.py`, `sources.py` | Les pages de l'application |
| `i18n.py` | Tous les textes, en français et en anglais |
| `data.py`, `charts.py`, `style.py` | Lecture des données, graphiques, couleurs |
| `risk.py` | Le score de risque, la confiance et le classement des essais |
| `knowledge.py` | La base de connaissances de l'assistant : les faits de la NASA et leurs sources |
| `experiments.csv`, `investigations.csv` | Les données harmonisées utilisées par l'application |
| `PSI-*.csv` | Les tableaux d'essais bruts de la NASA |
| `build_dataset.py` | Construit `experiments.csv` à partir des tableaux bruts |
| `DATA.md` | Comment chaque tableau de la NASA est lu |

## Données

Toutes les données viennent du dépôt [Physical Sciences Informatics (PSI)](https://psi.nasa.gov/physci/repo/) de la NASA, sous licence CC0. Les tableaux d'essais bruts sont les fichiers `PSI-*.csv`, et la façon de les lire est expliquée dans [DATA.md](DATA.md).

| Expérience | PSI |
| --- | --- |
| BASS-II (DOI 10.60555/4qc4-de67) | [PSI-25](https://psi.nasa.gov/physci/repo/data/investigations/PSI-25) |
| Saffire-I | [PSI-98](https://psi.nasa.gov/physci/repo/data/investigations/PSI-98) |
| Saffire-II | [PSI-99](https://psi.nasa.gov/physci/repo/data/investigations/PSI-99) |
| Saffire-III | [PSI-100](https://psi.nasa.gov/physci/repo/data/investigations/PSI-100) |
| FLEX | [PSI-69](https://psi.nasa.gov/physci/repo/data/investigations/PSI-69) |
| FLEX-2 | [PSI-68](https://psi.nasa.gov/physci/repo/data/investigations/PSI-68) |
| ACME BRE | [PSI-20](https://psi.nasa.gov/physci/repo/data/investigations/PSI-20) |
| CFI-G | [PSI-159](https://psi.nasa.gov/physci/repo/data/investigations/PSI-159) |

Les autres sources (articles de la NASA sur Saffire, guide de la NASA sur la combustion, 2015) sont listées dans la page « Sources et méthode » de l'application.

## Usage de l'IA

*Déclaration demandée par le règlement de NASA Space Apps.*

Claude (Anthropic) a participé à l'écriture du code avec l'équipe BlueSphere. L'assistant de l'application fonctionne avec Claude, grâce à une clé d'API. Les idées, le scénario de la base lunaire, les choix scientifiques et l'analyse du risque viennent de l'équipe BlueSphere.

*Use of AI (required by the NASA Space Apps rules): Claude (Anthropic) took part in writing the code with the BlueSphere team. The app's assistant runs on Claude, through an API key. The ideas, the Moon base scenario, the scientific choices and the risk analysis come from the BlueSphere team.*

## Licence

Code sous licence MIT. Données de la NASA : CC0.
