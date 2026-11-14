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
