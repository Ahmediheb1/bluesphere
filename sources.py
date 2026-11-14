"""Sources et méthode : d'où vient chaque chiffre, et comment l'IA est utilisée."""

import streamlit as st

from data import PSI_URL, load_investigations
from i18n import get_lang, t
from style import page_header

page_header(t("nav_sources"), t("sources_lead"))

lang = get_lang()

inv = load_investigations()
if not inv.empty:
    st.subheader("NASA PSI")
    for _, row in inv.iterrows():
        url = PSI_URL.format(psi_id=row["psi_id"])
        desc = row["desc_fr"] if lang == "fr" else row["desc_en"]
        st.markdown(f"- **[{row['investigation']} ({row['psi_id']})]({url})** : {desc}")

st.subheader("Articles" if lang == "fr" else "Papers")
PAPERS = [
    ("Ferkul et al., 2017, Results of Large-Scale Spacecraft Flammability Tests (NASA)",
     "https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf"),
    ("Fortenberry et al., 2021, Combustion Products from Saffire-IV and Saffire-V (ICES)",
     "https://ttu-ir.tdl.org/items/13a0b598-7e79-4d08-9d42-1fd220ad8803"),
    ("Brooker et Niehaus, 2022, Model Development of Large-Scale Spacecraft Fires during Saffire-IV (NASA)",
     "https://ntrs.nasa.gov/citations/20220002714"),
    ("Brooker et al., 2015, Modeling and Analysis of Realistic Fire Scenarios in Spacecraft (NASA)",
     "https://ntrs.nasa.gov/api/citations/20150021283/downloads/20150021283.pdf"),
    ("Olson et al., 2009, Flame spread over thin fuels in actual and simulated microgravity, Combustion and Flame",
     "https://doi.org/10.1016/j.combustflame.2009.01.015"),
    ("Greenberg et al., 1999, Microgravity combustion diagnostics: the path to the ISS, Meas. Sci. Technol.",
     "https://iopscience.iop.org/0957-0233/10/10/301"),
    ("Abercromby et al., 2022, NASA DCS Strategic Plan: exploration atmosphere 8.2 psia / 34% O2 (NASA)",
     "https://ntrs.nasa.gov/api/citations/20220005709/downloads/AsMA%202022%20-%20Abercromby%20-%20DCS%20Strategic%20Plan%20v2.pdf"),
    ("Norcross et al., 2013, Effects of the 8 psia / 32% O2 Atmosphere on the Human in the Spaceflight Environment (NASA TM)",
     "https://ntrs.nasa.gov/citations/20130013505"),
    ("Ross et al., combustion experiments on Mir (NASA SP-4225)", None),
]
for title, url in PAPERS:
    st.markdown(f"- [{title}]({url})" if url else f"- {title}")

st.subheader("NASA")
RESOURCES = [
    ("A Researcher's Guide to: Combustion Science (2015)",
     "https://www.nasa.gov/missions/station/a-researchers-guide-to-combustion-science/"),
    ("NASA Glenn, Combustion Science",
     "https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/"),
    ("Space Apps 2026, Flame in Freefall",
     "https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/"),
    ("NASA history: 25 years ago, fire aboard space station Mir",
     "https://www.nasa.gov/history/25-years-ago-fire-aboard-space-station-mir/"),
]
for title, url in RESOURCES:
    st.markdown(f"- [{title}]({url})")

st.subheader(t("sources_ai_title"))
st.markdown(t("sources_ai"))
