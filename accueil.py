"""Accueil : le problème, les chiffres clés et par où commencer."""

import streamlit as st

import data as d
from data import load_experiments, load_investigations
from i18n import t

st.markdown("<div class='bs-hero'>Blue<span>Sphere</span></div>", unsafe_allow_html=True)
st.markdown(f"<p class='bs-lead'>{t('home_tagline')}</p>", unsafe_allow_html=True)

df = load_experiments()
inv = load_investigations()
if not df.empty and not inv.empty:
    n_tests = int(inv["n_tests"].sum())
    n_inv = len(inv)
    n_moon_o2 = int((df["o2_pct"] >= d.MOON_BASE_O2_PCT).sum())
    n_partial = int(df["gravity"].isin(["moon", "mars"]).sum())
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t("home_stat_tests"), f"{n_tests}")
    m2.metric(t("home_stat_investigations"), f"{n_inv}")
    m3.metric(t("home_stat_moon"), f"{n_moon_o2}")
    m4.metric(t("home_stat_partial"), f"{n_partial}")

st.subheader(t("home_why_title"))
st.markdown(t("home_why"))

st.subheader(t("home_messages_title"))
for i in range(1, 5):
    st.markdown(f"{i}. {t(f'home_msg_{i}')}")

st.subheader(t("home_start"))
st.page_link("atlas.py", label=t("home_go_atlas"), icon=":material/arrow_forward:")
st.page_link("classement.py", label=t("home_go_ranking"), icon=":material/arrow_forward:")
