"""BlueSphere : copilote de sécurité incendie pour l'exploration spatiale.

NASA Space Apps Challenge 2026, défi « Flame in Freefall ».
Lancer en local :  py -m streamlit run app.py
"""

import streamlit as st

from i18n import language_selector, t
from style import inject_css

st.set_page_config(page_title="BlueSphere", page_icon="🔵", layout="wide")
inject_css()
language_selector()

pages = [
    st.Page("accueil.py", title=t("nav_home"), icon=":material/public:", default=True),
    st.Page("atlas.py", title=t("nav_atlas"), icon=":material/scatter_plot:", url_path="atlas"),
    st.Page("classement.py", title=t("nav_ranking"), icon=":material/leaderboard:", url_path="ranking"),
    st.Page("assistant.py", title=t("nav_assistant"), icon=":material/smart_toy:", url_path="assistant"),
    st.Page("sources.py", title=t("nav_sources"), icon=":material/menu_book:", url_path="sources"),
]

st.navigation(pages).run()

st.markdown(f"<p class='bs-footer'>{t('footer')}</p>", unsafe_allow_html=True)
