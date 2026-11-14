"""Textes de l'application en français et en anglais.

Chaque texte a une clé. On l'affiche avec t("cle").
La langue vient, dans l'ordre : du choix de l'utilisateur, du lien (?lang=fr ou ?lang=en),
puis de la langue du navigateur. Par défaut : anglais.
"""

import streamlit as st

LANGS = {"fr": "Français", "en": "English"}

STRINGS = {
    # Navigation
    "nav_home": {"fr": "Accueil", "en": "Home"},
    "nav_atlas": {"fr": "Atlas d'inflammabilité", "en": "Flammability atlas"},
    "nav_ranking": {"fr": "Classement", "en": "Ranking"},
    "nav_assistant": {"fr": "Assistant", "en": "Assistant"},
    "nav_after": {"fr": "Après le feu", "en": "After the fire"},
    "nav_detection": {"fr": "Détection en direct", "en": "Live detection"},
    "nav_sources": {"fr": "Sources et méthode", "en": "Sources and method"},
    "lang_label": {"fr": "Langue", "en": "Language"},

    # Accueil
    "home_tagline": {
        "fr": "Copilote de sécurité incendie alimenté par l'IA. Il transforme des décennies "
              "d'expériences de la NASA sur le feu en microgravité en réponses claires, "
              "pour protéger les astronautes sur la Lune et sur Mars.",
        "en": "An AI-powered fire safety copilot. It turns decades of NASA microgravity "
              "combustion experiments into clear answers to keep astronauts safe "
              "on the Moon and Mars.",
    },
    "home_why_title": {"fr": "Pourquoi c'est urgent", "en": "Why it matters now"},
    "home_why": {
        "fr": "Dans l'espace, une flamme ne monte pas : sans gravité, l'air chaud ne s'élève plus "
              "et la flamme devient une sphère bleue qui dépend de la diffusion de l'oxygène. "
              "La future base lunaire aura probablement 30 % d'oxygène ou plus, à 10,2 psi ou moins, "
              "pour faciliter les sorties en scaphandre. C'est plus de 40 % d'oxygène en plus que sur Terre.",
        "en": "In space, a flame does not rise: without gravity, hot gases no longer float upward, "
              "and the flame becomes a blue sphere fed by the diffusion of oxygen. "
              "The planned Moon base will likely have 30% oxygen or more, at 10.2 psi or less, "
              "to make spacesuit excursions easier. That is a 40% increase in oxygen over Earth's air.",
    },
    "home_messages_title": {"fr": "Ce que BlueSphere montre", "en": "What BlueSphere shows"},
    "home_msg_1": {
        "fr": "Sur la base lunaire, plus d'oxygène veut dire plus de risque de feu.",
        "en": "On the Moon base, more oxygen means a higher fire risk.",
    },
    "home_msg_2": {
        "fr": "Ce qu'on sait, et surtout ce qu'on ne sait pas encore : les expériences dont la NASA a besoin.",
        "en": "What we know, and above all what we don't know yet: the experiments NASA still needs.",
    },
    "home_msg_3": {
        "fr": "BlueSphere sait ce qu'il ne sait pas : dans les zones sans données, il devient plus prudent.",
        "en": "BlueSphere knows what it doesn't know: where data is missing, it becomes more cautious.",
    },
    "home_msg_4": {
        "fr": "Le danger ne s'arrête pas quand la flamme s'éteint : la NASA l'a vu en orbite.",
        "en": "The danger does not end when the flame goes out: NASA saw it in orbit.",
    },
    "home_stat_tests": {"fr": "Essais réels de la NASA", "en": "Real NASA tests"},
    "home_stat_investigations": {"fr": "Expériences", "en": "Investigations"},
    "home_stat_moon": {"fr": "Conditions testées à 30 % d'O₂ ou plus", "en": "Conditions tested at 30% O₂ or more"},
    "home_stat_partial": {"fr": "Essais en gravité lunaire", "en": "Tests in lunar gravity"},
    "home_start": {"fr": "Par où commencer", "en": "Where to start"},
    "home_go_atlas": {
        "fr": "Ouvrir l'Atlas : chaque essai de la NASA sur une seule carte.",
        "en": "Open the Atlas: every NASA test on a single map.",
    },
    "home_go_ranking": {
        "fr": "Ouvrir le Classement : le risque selon l'environnement, et les essais de la NASA les plus proches.",
        "en": "Open the Ranking: the risk for each environment, and the closest NASA tests.",
    },

    # Atlas
    "atlas_lead": {
        "fr": "Chaque point est un essai réel de la NASA en microgravité. "
              "Point plein : la flamme a brûlé. Point vide : elle s'est éteinte ou n'a pas pris.",
        "en": "Each point is a real NASA test in microgravity. "
              "Filled point: the flame burned. Hollow point: it went out or never caught.",
    },
    "atlas_filter_investigations": {"fr": "Expériences", "en": "Investigations"},
    "atlas_filter_fuel": {"fr": "Combustible", "en": "Fuel"},
    "atlas_x": {"fr": "Vitesse de l'air (cm/s)", "en": "Air flow speed (cm/s)"},
    "atlas_y": {"fr": "Oxygène (% en volume)", "en": "Oxygen (% by volume)"},
    "atlas_ref_air": {"fr": "Air : 21 %", "en": "Air: 21%"},
    "atlas_ref_moon": {"fr": "Base lunaire : 30 % ou plus", "en": "Moon base: 30% or more"},
    "atlas_ref_vent": {
        "fr": "Repères : l'air de la Terre et de l'ISS contient 21 % d'oxygène. La base lunaire en aura 30 % ou plus. "
              "Vers 10 cm/s, la vitesse typique de la ventilation d'un vaisseau, les flammes se propagent le mieux "
              "et brûlent avec le moins d'oxygène (guide de la NASA, 2015).",
        "en": "Reference lines: Earth and ISS air holds 21% oxygen. The Moon base will hold 30% or more. "
              "Around 10 cm/s, the typical speed of spacecraft ventilation, flames spread fastest "
              "and burn with the least oxygen (NASA guide, 2015).",
    },
    "atlas_no_data": {
        "fr": "Les tableaux d'essais de PSI sont en cours d'intégration.",
        "en": "The PSI test tables are being integrated.",
    },
    "atlas_still_air": {"fr": "air immobile", "en": "still air"},
    "atlas_still_air_title": {"fr": "Air immobile (0 cm/s)", "en": "Still air (0 cm/s)"},
    "atlas_ref_vent_short": {"fr": "ventilation typique (~10 cm/s)", "en": "typical ventilation (~10 cm/s)"},
    "atlas_moon_gap": {
        "fr": "Aucun essai avec courant d'air dans l'atmosphère de la base lunaire",
        "en": "No test with airflow in the Moon base atmosphere",
    },
    "atlas_conditions": {"fr": "Conditions testées", "en": "Tested conditions"},
    "atlas_coverage_note": {
        "fr": "Le contour marque la case de la base lunaire. CFI-G (flammes inversées) et FLEX-2 (plages seulement) "
              "ne sont pas comptés : leur oxygène n'est pas celui de l'air ambiant, ou PSI ne détaille pas leurs essais.",
        "en": "The outline marks the Moon base cell. CFI-G (inverse flames) and FLEX-2 (ranges only) are not counted: "
              "their oxygen is not the ambient air's, or PSI does not list their individual tests.",
    },
    "atlas_lead_2": {
        "fr": "Les traits montrent la plage de vitesses d'air parcourue pendant un même essai de BASS-II. "
              "Les points qui se chevauchaient sont légèrement écartés. Passez la souris sur un point pour voir l'essai.",
        "en": "Lines show the range of air speeds covered during a single BASS-II test. "
              "Overlapping points are spread slightly apart. Hover over a point to see the test.",
    },
    "atlas_coverage_title": {"fr": "Les zones sans données", "en": "Where data is missing"},
    "atlas_coverage_lead": {
        "fr": "Nombre de conditions testées (un essai, ou un groupe d'essais identiques) selon l'oxygène et la gravité. "
              "Une case vide est une question à laquelle aucune expérience de PSI ne répond encore.",
        "en": "Number of tested conditions (one test, or a group of identical tests) by oxygen level and gravity. "
              "An empty cell is a question no PSI investigation answers yet.",
    },
    "atlas_coverage_none": {"fr": "aucune donnée", "en": "no data"},
    "atlas_table": {"fr": "Voir les données", "en": "View the data"},
    "atlas_n_shown": {"fr": "{n} essais affichés", "en": "{n} tests shown"},

    # Combustibles et résultats
    "fuel_solid": {"fr": "Solide", "en": "Solid"},
    "fuel_liquid": {"fr": "Liquide", "en": "Liquid"},
    "fuel_gas": {"fr": "Gaz", "en": "Gas"},
    "outcome_burned": {"fr": "A brûlé", "en": "Burned"},
    "outcome_extinguished": {"fr": "S'est éteinte", "en": "Went out"},
    "outcome_no_ignition": {"fr": "N'a pas pris", "en": "Did not ignite"},
    "outcome_unknown": {"fr": "Inconnu", "en": "Unknown"},

    # Gravité et bandes d'oxygène
    "grav_micro": {"fr": "Microgravité", "en": "Microgravity"},
    "grav_moon": {"fr": "Lune (1/6 g)", "en": "Moon (1/6 g)"},
    "grav_mars": {"fr": "Mars (3/8 g)", "en": "Mars (3/8 g)"},
    "grav_earth": {"fr": "Terre (1 g)", "en": "Earth (1 g)"},
    "o2_low": {"fr": "Sous l'air (< 21 %)", "en": "Below air (< 21%)"},
    "o2_mid": {"fr": "De l'air à 30 %", "en": "Air to 30%"},
    "o2_high": {"fr": "30 % et plus", "en": "30% and more"},

    # Colonnes du tableau
    "col_investigation": {"fr": "Expérience", "en": "Investigation"},
    "col_test": {"fr": "Essai", "en": "Test"},
    "col_material": {"fr": "Matériau", "en": "Material"},
    "col_fuel": {"fr": "Combustible", "en": "Fuel"},
    "col_o2": {"fr": "O₂ (%)", "en": "O₂ (%)"},
    "col_pressure": {"fr": "Pression (kPa)", "en": "Pressure (kPa)"},
    "col_flow": {"fr": "Air (cm/s)", "en": "Air flow (cm/s)"},
    "col_outcome": {"fr": "Résultat", "en": "Outcome"},
    "col_source": {"fr": "Source", "en": "Source"},
    "col_detail": {"fr": "Détail", "en": "Detail"},
    "col_n_tests": {"fr": "Essais", "en": "Tests"},
    "col_notes": {"fr": "Notes du tableau PSI", "en": "PSI table notes"},

    # Pages à venir
    "coming_soon": {"fr": "Cette partie arrive bientôt.", "en": "This part is coming soon."},

    # Sources
    "sources_lead": {
        "fr": "Toutes les données viennent du dépôt Physical Sciences Informatics (PSI) de la NASA. "
              "Chaque chiffre de l'application renvoie à sa source.",
        "en": "All data comes from NASA's Physical Sciences Informatics (PSI) repository. "
              "Every number in the app points to its source.",
    },
    "sources_ai_title": {"fr": "Usage de l'IA", "en": "Use of AI"},
    "sources_ai": {
        "fr": "Déclaration demandée par le règlement de NASA Space Apps. Claude (Anthropic) a participé à l'écriture du code avec l'équipe BlueSphere. L'assistant de l'application fonctionne avec Claude, grâce à une clé d'API. Les idées, le scénario de la base lunaire, les choix scientifiques et l'analyse du risque viennent de l'équipe BlueSphere.",
        "en": "Statement required by the NASA Space Apps rules. Claude (Anthropic) took part in writing the code with the BlueSphere team. The app's assistant runs on Claude, through an API key. The ideas, the Moon base scenario, the scientific choices and the risk analysis come from the BlueSphere team.",
    },
    # Classement selon l'environnement (module 2)
    "rank_title": {"fr": "Classement selon l'environnement", "en": "Ranking by environment"},
    "rank_lead": {
        "fr": "Choisis un environnement et un matériau. BlueSphere calcule un score de risque avec la pondération "
              "de l'équipe, puis classe les essais de la NASA les plus proches : ce qu'on sait, et ce qu'on ne sait pas encore.",
        "en": "Pick an environment and a material. BlueSphere computes a risk score with the team's weighting, "
              "then ranks the closest NASA tests: what we know, and what we don't know yet.",
    },
    "rank_env": {"fr": "Environnement", "en": "Environment"},
    "env_iss": {"fr": "Station spatiale (ISS)", "en": "Space station (ISS)"},
    "env_moon_base": {"fr": "Base lunaire", "en": "Moon base"},
    "env_moon_rover": {"fr": "Rover lunaire pressurisé", "en": "Pressurized lunar rover"},
    "env_mars_ship": {"fr": "Vaisseau vers Mars", "en": "Ship to Mars"},
    "env_custom": {"fr": "Personnalisé", "en": "Custom"},
    "env_note_iss": {
        "fr": "Air comme sur Terre : 21 % d'O₂ à 14,7 psi (101,3 kPa). Ventilation typique d'un vaisseau : environ 10 cm/s (guide de la NASA, 2015). Microgravité.",
        "en": "Earth-like air: 21% O₂ at 14.7 psi (101.3 kPa). Typical spacecraft ventilation: about 10 cm/s (NASA guide, 2015). Microgravity.",
    },
    "env_note_moon_base": {
        "fr": "Énoncé du défi : 30 % d'O₂ ou plus, à 10,2 psi (70,3 kPa) ou moins, pour raccourcir la préparation avant les sorties. Gravité lunaire. Ventilation supposée à 10 cm/s.",
        "en": "Challenge statement: 30% O₂ or more, at 10.2 psi (70.3 kPa) or less, to shorten the preparation before moonwalks. Lunar gravity. Ventilation assumed at 10 cm/s.",
    },
    "env_note_moon_rover": {
        "fr": "Même atmosphère que la base lunaire, selon l'énoncé du défi. Gravité lunaire. Petit volume : les gaz d'un feu s'y accumulent plus vite.",
        "en": "Same atmosphere as the Moon base, according to the challenge statement. Lunar gravity. Small volume: fire gases build up faster.",
    },
    "env_note_mars_ship": {
        "fr": "Hypothèse : l'atmosphère d'exploration recommandée par la NASA pour les véhicules avec des sorties fréquentes, 34 % d'O₂ à 8,2 psi (56,5 kPa). Microgravité pendant le voyage.",
        "en": "Assumption: the exploration atmosphere NASA recommends for vehicles with frequent spacewalks, 34% O₂ at 8.2 psi (56.5 kPa). Microgravity during the trip.",
    },
    "env_note_custom": {
        "fr": "Règle toi-même l'oxygène, la pression, la ventilation et la gravité.",
        "en": "Set the oxygen, pressure, ventilation and gravity yourself.",
    },
    "rank_material": {"fr": "Matériau", "en": "Material"},
    "mat_sibal": {"fr": "Tissu SIBAL (coton et fibre de verre)", "en": "SIBAL fabric (cotton and fiberglass)"},
    "mat_pmma": {"fr": "Plastique PMMA (acrylique)", "en": "PMMA plastic (acrylic)"},
    "mat_nomex": {"fr": "Tissu Nomex (résistant au feu)", "en": "Nomex fabric (fire-resistant)"},
    "mat_silicone": {"fr": "Silicone", "en": "Silicone"},
    "mat_evidence": {
        "fr": "Essais de la NASA avec ce matériau : {burned} ont brûlé sur {n}.",
        "en": "NASA tests with this material: {burned} burned out of {n}.",
    },
    "rank_thickness": {"fr": "Épaisseur (mm)", "en": "Thickness (mm)"},
    "rank_o2": {"fr": "Oxygène (% du volume)", "en": "Oxygen (% by volume)"},
    "rank_pressure": {"fr": "Pression (kPa)", "en": "Pressure (kPa)"},
    "rank_flow": {"fr": "Ventilation (cm/s)", "en": "Ventilation (cm/s)"},
    "rank_gravity": {"fr": "Gravité", "en": "Gravity"},
    "metric_score": {"fr": "Score de risque", "en": "Risk score"},
    "metric_confidence": {"fr": "Confiance", "en": "Confidence"},
    "metric_ppo2": {"fr": "O₂ à respirer (pression partielle)", "en": "Breathable O₂ (partial pressure)"},
    "ppo2_value": {"fr": "{kpa} kPa ({psi} psi)", "en": "{kpa} kPa ({psi} psi)"},
    "ppo2_earth": {
        "fr": "Sur Terre : 21,3 kPa (3,09 psi). Même O₂ à respirer ne veut pas dire même risque de feu : c'est le % d'oxygène qui compte le plus.",
        "en": "On Earth: 21.3 kPa (3.09 psi). The same breathable O₂ does not mean the same fire risk: the oxygen percentage matters most.",
    },
    "score_of": {"fr": "{s} sur 100", "en": "{s} out of 100"},
    "level_low": {"fr": "🟢 Faible", "en": "🟢 Low"},
    "level_moderate": {"fr": "🟡 Modéré", "en": "🟡 Moderate"},
    "level_high": {"fr": "🟠 Élevé", "en": "🟠 High"},
    "level_very_high": {"fr": "🔴 Très élevé", "en": "🔴 Very high"},
    "conf_high": {"fr": "Élevée", "en": "High"},
    "conf_medium": {"fr": "Moyenne", "en": "Medium"},
    "conf_low": {"fr": "Faible", "en": "Low"},
    "conf_reason_close": {"fr": "Des essais de la NASA très proches existent.", "en": "Very close NASA tests exist."},
    "conf_reason_some": {"fr": "Les essais de la NASA les plus proches sont assez éloignés.", "en": "The closest NASA tests are fairly far."},
    "conf_reason_far": {"fr": "Aucun essai de la NASA n'est proche de cet environnement.", "en": "No NASA test is close to this environment."},
    "conf_reason_no_test": {"fr": "Aucun essai de la NASA ne peut être comparé.", "en": "No NASA test can be compared."},
    "conf_reason_gravity": {
        "fr": "Aucun essai de PSI n'a été fait en gravité lunaire ou martienne.",
        "en": "No PSI test was run in lunar or Martian gravity.",
    },
    "conf_reason_earth": {"fr": "Nos essais sont en microgravité, pas sur Terre.", "en": "Our tests are in microgravity, not on Earth."},
    "prudent_mode": {
        "fr": "🛡️ **Mode prudent.** Cet environnement est dans une zone sans données. BlueSphere sait ce qu'il ne sait pas : il ajoute une marge de {m} points. Score prudent : **{sp} sur 100** (au lieu de {s}).",
        "en": "🛡️ **Cautious mode.** This environment is in a no-data zone. BlueSphere knows what it doesn't know: it adds a {m}-point margin. Cautious score: **{sp} out of 100** (instead of {s}).",
    },
    "o2_gap_note": {
        "fr": "Aucun matériau solide n'a été testé au-dessus de {max} % d'O₂ dans ces essais de la NASA. Cet environnement en a {o2} %.",
        "en": "No solid material was tested above {max}% O₂ in these NASA tests. This environment has {o2}%.",
    },
    "rank_parts_title": {"fr": "D'où vient le score", "en": "Where the score comes from"},
    "rank_parts_caption": {
        "fr": "Chaque barre montre les points apportés par un facteur. La bande claire montre le maximum possible avec sa pondération.",
        "en": "Each bar shows the points a factor adds. The light track shows the most it can add with its weight.",
    },
    "rank_envs_title": {"fr": "Les environnements classés, avec ce matériau", "en": "Environments ranked, with this material"},
    "rank_envs_caption": {
        "fr": "Score sans la marge du mode prudent. Même matériau et même épaisseur partout.",
        "en": "Score without the cautious-mode margin. Same material and thickness everywhere.",
    },
    "f_o2": {"fr": "Oxygène", "en": "Oxygen"},
    "f_material": {"fr": "Matériau", "en": "Material"},
    "f_ventilation": {"fr": "Ventilation", "en": "Ventilation"},
    "f_thickness": {"fr": "Épaisseur", "en": "Thickness"},
    "f_pressure": {"fr": "Pression", "en": "Pressure"},
    "points": {"fr": "Points", "en": "Points"},
    "points_max": {"fr": "Maximum possible", "en": "Most possible"},
    "rank_tests_title": {"fr": "Les essais de la NASA les plus proches", "en": "The closest NASA tests"},
    "rank_best": {
        "fr": "L'essai le plus proche, {inv} {test}, ressemble à {p} % à cet environnement. Résultat : {outcome}.",
        "en": "The closest test, {inv} {test}, is a {p}% match for this environment. Outcome: {outcome}.",
    },
    "rank_tests_caption": {
        "fr": "Proximité : ressemblance avec l'environnement choisi, avec les mêmes poids que le score. Un seul grand écart, par exemple 8 points d'oxygène, suffit à éloigner un essai. La pression manque dans les tableaux de BASS-II et de Saffire : on prend celle de la Station (101,3 kPa).",
        "en": "Match: how much a test looks like the chosen environment, with the same weights as the score. One large gap, for example 8 points of oxygen, is enough to push a test away. Pressure is missing from the BASS-II and Saffire tables: we use the station's (101.3 kPa).",
    },
    "col_proximity": {"fr": "Proximité", "en": "Match"},
    "col_thickness": {"fr": "Épaisseur (mm)", "en": "Thickness (mm)"},
    "col_o2_gap": {"fr": "Écart d'O₂ (points)", "en": "O₂ gap (points)"},
    "weights_title": {"fr": "Ajuster la pondération (version 1 de l'équipe BlueSphere)", "en": "Adjust the weighting (BlueSphere team, version 1)"},
    "weights_note": {
        "fr": "Pondération d'expert de l'équipe BlueSphere. Total actuel : {n} %. Les poids sont toujours remis sur 100.",
        "en": "Expert weighting from the BlueSphere team. Current total: {n}%. Weights are always rescaled to 100.",
    },
    "weights_reset": {"fr": "Revenir à la pondération de l'équipe", "en": "Back to the team's weighting"},
    "method_title": {"fr": "Comment le score est calculé", "en": "How the score is computed"},
    "method_body": {
        "fr": "Chaque facteur vaut de 0 (peu de risque) à 1 (risque maximal). Le score est leur moyenne pondérée, sur 100.\n\n"
              "- **Oxygène** : 0 à 14 % (le plus bas O₂ où un solide a brûlé dans nos essais : 14,2 %, BASS-II), 1 à partir de 35 %, en ligne droite entre les deux.\n"
              "- **Matériau** : valeur d'expert, version 1, appuyée sur les essais : SIBAL 1 ; PMMA 0,8 ; Nomex 0,5 (pas d'allumage dans Saffire-II) ; silicone 0,2 (aucun allumage en microgravité dans Saffire-II, alors qu'il brûle sur Terre).\n"
              "- **Ventilation** : courbe en cloche, avec son sommet vers 10 cm/s, la vitesse typique de la ventilation d'un vaisseau, où les flammes se propagent le mieux (guide de la NASA, 2015). En air immobile, le facteur ne tombe pas à 0 : selon ce guide, « un feu s'éteint si on coupe la ventilation » est une idée fausse.\n"
              "- **Épaisseur** : 1 à 0,1 mm, puis de moins en moins jusqu'à 0,2 à 10 mm et plus. Un matériau mince brûle plus facilement.\n"
              "- **Pression** : la pression divisée par celle de la Terre. À oxygène égal, une pression plus basse donne moins de molécules d'oxygène.\n"
              "- **Gravité** : elle ne change pas le score, mais la confiance. Aucun essai de PSI n'a été fait en gravité lunaire ou martienne.\n\n"
              "**Limites** : c'est un indice pour comparer des situations, pas une probabilité d'incendie. BlueSphere est un outil d'aide à la décision, il ne certifie pas un habitat. "
              "Le sens de l'air n'est pas encore pris en compte : dans Saffire-I, le même tissu a brûlé 420 secondes avec l'air dans le sens de la flamme, contre 70 secondes à contre-courant.",
        "en": "Each factor goes from 0 (little risk) to 1 (highest risk). The score is their weighted average, out of 100.\n\n"
              "- **Oxygen**: 0 at 14% (the lowest O₂ where a solid burned in our tests: 14.2%, BASS-II), 1 from 35%, in a straight line in between.\n"
              "- **Material**: expert value, version 1, backed by the tests: SIBAL 1; PMMA 0.8; Nomex 0.5 (no ignition in Saffire-II); silicone 0.2 (no ignition in microgravity in Saffire-II, while it burns on Earth).\n"
              "- **Ventilation**: a bell curve peaking near 10 cm/s, the typical speed of spacecraft ventilation, where flames spread best (NASA guide, 2015). In still air the factor does not drop to 0: according to that guide, \"a fire goes out if you shut off the ventilation\" is a misconception.\n"
              "- **Thickness**: 1 at 0.1 mm, then less and less down to 0.2 at 10 mm and more. Thin materials burn more easily.\n"
              "- **Pressure**: the pressure divided by Earth's. At the same oxygen percentage, lower pressure means fewer oxygen molecules.\n"
              "- **Gravity**: it does not change the score, but the confidence. No PSI test was run in lunar or Martian gravity.\n\n"
              "**Limits**: this is an index to compare situations, not a probability of fire. BlueSphere is a decision-support tool; it does not certify a habitat. "
              "Air direction is not taken into account yet: in Saffire-I, the same fabric burned 420 seconds with the air flowing with the flame, against 70 seconds against it.",
    },
    "method_sources": {"fr": "Sources des environnements et des règles", "en": "Sources for the environments and rules"},

    # Assistant d'IA (module 3)
    "assistant_title": {"fr": "Assistant d'IA", "en": "AI assistant"},
    "assistant_lead": {
        "fr": "Pose une question sur le feu dans l'espace. L'assistant répond seulement avec des sources de la NASA, cite chacune, et dit « je ne sais pas » quand l'information manque.",
        "en": "Ask a question about fire in space. The assistant answers only with NASA sources, cites each one, and says \"I don't know\" when the information is missing.",
    },
    "assistant_disclaimer": {
        "fr": "Réponses générées par l'IA (Claude, d'Anthropic) à partir de sources de la NASA. Vérifie toujours la source citée. Outil d'aide à la décision, pas une certification.",
        "en": "Answers generated by AI (Claude, by Anthropic) from NASA sources. Always check the cited source. A decision-support tool, not a certification.",
    },
    "assistant_no_key": {
        "fr": "L'assistant sera actif dès que la clé de l'API Claude sera ajoutée dans les secrets de Streamlit.",
        "en": "The assistant will be active as soon as the Claude API key is added to the Streamlit secrets.",
    },
    "assistant_examples": {"fr": "Exemples de questions", "en": "Example questions"},
    "assistant_example_1": {"fr": "Un feu s'éteint-il si on coupe la ventilation ?", "en": "Does a fire go out if you shut off the ventilation?"},
    "assistant_example_2": {"fr": "Pourquoi 30 % d'oxygène sur la base lunaire est-il dangereux ?", "en": "Why is 30% oxygen on the Moon base dangerous?"},
    "assistant_example_3": {"fr": "Quel gaz révèle un feu en premier ?", "en": "Which gas reveals a fire first?"},
    "assistant_example_4": {"fr": "Que sait-on du feu en gravité lunaire ?", "en": "What do we know about fire in lunar gravity?"},
    "assistant_input": {"fr": "Ta question sur le feu dans l'espace…", "en": "Your question about fire in space…"},
    "assistant_sources": {"fr": "Sources citées", "en": "Cited sources"},
    "assistant_limit": {
        "fr": "Tu as posé {n} questions : c'est la limite pour cette visite. Merci !",
        "en": "You asked {n} questions: that is the limit for this visit. Thank you!",
    },
    "assistant_daily_limit": {
        "fr": "L'assistant a atteint sa limite de questions pour aujourd'hui. Reviens demain !",
        "en": "The assistant has reached its question limit for today. Come back tomorrow!",
    },
    "assistant_error": {
        "fr": "L'assistant n'a pas pu répondre. Réessaie dans un moment.",
        "en": "The assistant could not answer. Try again in a moment.",
    },
    "assistant_remaining": {"fr": "Questions restantes pour cette visite : {n}", "en": "Questions left for this visit: {n}"},
    "assistant_clear": {"fr": "Effacer la conversation", "en": "Clear the conversation"},
    "home_go_assistant": {
        "fr": "Demander à l'assistant : des réponses tirées des sources de la NASA, avec leurs références.",
        "en": "Ask the assistant: answers drawn from NASA sources, with their references.",
    },

    "footer": {
        "fr": "BlueSphere · NASA Space Apps Challenge 2026 · Défi « Flame in Freefall » · Données : NASA PSI",
        "en": "BlueSphere · NASA Space Apps Challenge 2026 · \"Flame in Freefall\" challenge · Data: NASA PSI",
    },
}


def _default_lang() -> str:
    """Langue du lien, sinon du navigateur, sinon anglais."""
    param = st.query_params.get("lang")
    if param in LANGS:
        return param
    locale = getattr(st.context, "locale", None) or ""
    return "fr" if str(locale).lower().startswith("fr") else "en"


def get_lang() -> str:
    if "lang" not in st.session_state:
        st.session_state["lang"] = _default_lang()
    return st.session_state["lang"]


def t(key: str, **kwargs) -> str:
    """Renvoie le texte de la clé dans la langue choisie."""
    text = STRINGS[key][get_lang()]
    return text.format(**kwargs) if kwargs else text


def language_selector() -> str:
    """Le choix de langue, en haut de la barre latérale."""
    get_lang()
    st.sidebar.segmented_control(
        t("lang_label"),
        options=list(LANGS),
        format_func=lambda code: LANGS[code],
        key="lang",
        required=True,
    )
    return st.session_state["lang"]
