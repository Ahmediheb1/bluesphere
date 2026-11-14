# BlueSphere 🔵

**NASA Space Apps Challenge 2026 · Défi « Flame in Freefall » · Équipe BlueSphere (Sherbrooke)**

BlueSphere est un copilote de sécurité incendie alimenté par l'IA. Il transforme des décennies d'expériences de la NASA sur le feu en microgravité en réponses claires, pour protéger les astronautes sur la Lune et sur Mars.

*BlueSphere is an AI-powered fire safety copilot that turns decades of NASA microgravity combustion experiments into clear answers to keep astronauts safe on the Moon and Mars.*

## Ce que fait l'application

- **Atlas d'inflammabilité** : 764 essais réels de 8 expériences de la NASA (BASS-II, Saffire I à III, FLEX, FLEX-2, ACME BRE, CFI-G) réunis sur une seule carte, oxygène en fonction de la vitesse de l'air.
- **Les zones sans données** : ce que la NASA n'a pas encore testé, à commencer par l'atmosphère de la future base lunaire (30 % d'O₂ ou plus, à 10,2 psi ou moins) en gravité lunaire.
- Application bilingue (français et anglais) : `?lang=fr` ou `?lang=en` dans le lien.

## Lancer en local

```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Pour reconstruire le tableau de données à partir des fichiers bruts de PSI :

```bash
py tools/build_dataset.py
```

## Données

Toutes les données viennent du dépôt [Physical Sciences Informatics (PSI)](https://psi.nasa.gov/physci/repo/) de la NASA, sous licence CC0. Les tableaux d'essais bruts sont dans `data/raw/`, et la façon de les lire est expliquée dans [data/README.md](data/README.md).

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

BlueSphere a été construit avec l'aide de Claude (Anthropic) pour le code, l'analyse des tableaux et la rédaction. Les données, elles, viennent toutes de la NASA. L'assistant de l'application utilise aussi Claude et répond seulement à partir des documents de la NASA.

## Licence

Code sous licence MIT. Données de la NASA : CC0.
