"""BlueSphere: an AI-powered fire safety copilot built on NASA microgravity combustion data.

Run locally:  py -m streamlit run app.py
"""

import streamlit as st

from style import inject_css
from texts import t

st.set_page_config(page_title="BlueSphere", page_icon="🔵", layout="wide", initial_sidebar_state="collapsed")
inject_css()

pages = [
    st.Page("home.py", title=t("nav_home"), icon=":material/public:", default=True),
    st.Page("atlas.py", title=t("nav_atlas"), icon=":material/scatter_plot:", url_path="atlas"),
    st.Page("ranking.py", title=t("nav_ranking"), icon=":material/leaderboard:", url_path="ranking"),
    st.Page("assistant.py", title=t("nav_assistant"), icon=":material/smart_toy:", url_path="assistant"),
    st.Page("detection.py", title=t("nav_detection"), icon=":material/sensors:", url_path="detection"),
    st.Page("after.py", title=t("nav_after"), icon=":material/local_fire_department:", url_path="after-the-fire"),
    st.Page("sources.py", title=t("nav_sources"), icon=":material/menu_book:", url_path="sources"),
]
st.navigation(pages, position="top").run()
st.markdown(f"<p class='bs-footer'>{t('footer')}</p>", unsafe_allow_html=True)
