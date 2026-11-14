"""Overview: the problem, the key finding, and where to go next."""

import streamlit as st

import data as d
from style import oxygen_ruler, section
from texts import STRINGS, t

df = d.load_experiments()
inv = d.load_investigations()

# Hero: the message on the left, the blue sphere on the right
left, right = st.columns([1.35, 1], gap="large", vertical_alignment="center")
with left:
    st.markdown(
        f"<p class='bs-wordmark'>{t('home_wordmark')}</p>"
        f"<h1 class='bs-headline'>{t('home_headline')}</h1>"
        f"<p class='bs-hero-text'>{t('home_intro')}</p>",
        unsafe_allow_html=True,
    )
    b1, b2, b3 = st.columns([1.1, 1.25, 1.2])
    if b1.button(t("home_cta_atlas"), type="primary", width="stretch"):
        st.switch_page("atlas.py")
    if b2.button(t("home_cta_ranking"), width="stretch"):
        st.switch_page("ranking.py")
    if b3.button(t("home_cta_assistant"), width="stretch"):
        st.switch_page("assistant.py")
with right:
    st.markdown(
        "<div class='bs-sphere-wrap' aria-hidden='true'><div class='bs-sphere'></div>"
        f"<p class='bs-sphere-caption'>{t('home_sphere_caption')}</p></div>",
        unsafe_allow_html=True,
    )

# The key finding: solids were never tested at Moon-base oxygen in these tables
solids = df[df["fuel_state"].eq("solid")]["o2_pct"].dropna()
others = df[~df["fuel_state"].eq("solid")]["o2_pct"].dropna()
if len(solids) and len(others):
    section(t("home_gap_title"), t("home_gap_lead", lo=f"{solids.min():.1f}", hi=f"{solids.max():.1f}"))
    st.markdown(oxygen_ruler(solids.min(), solids.max(), others.min(), others.max()), unsafe_allow_html=True)
    st.markdown(f"<p class='bs-ruler-note'>{t('home_gap_note')}</p>", unsafe_allow_html=True)

    stats = [
        (f"{int(inv['n_tests'].sum())}", t("home_stat_tests")),
        (f"{len(inv)}", t("home_stat_investigations")),
        (f"{int(df['gravity'].isin(['moon', 'mars']).sum())}", t("home_stat_gravity")),
        (f"{solids.max():.1f}%", t("home_stat_solid")),
    ]
    st.markdown(
        "<div class='bs-stats'>"
        + "".join(f"<div class='bs-stat'><div class='bs-stat-value'>{v}</div><div class='bs-stat-label'>{label}</div></div>"
                  for v, label in stats)
        + "</div>",
        unsafe_allow_html=True,
    )

# The modules, as a list with one action each
section(t("home_modules_title"))
modules = [
    ("atlas", "atlas.py", False),
    ("ranking", "ranking.py", False),
    ("assistant", "assistant.py", False),
    ("detection", "detection.py", False),
    ("after", "after.py", False),
]
for key, page, in_progress in modules:
    text_col, action_col = st.columns([5, 1], vertical_alignment="center")
    tag = f"<span class='bs-tag'>{t('home_in_progress')}</span>" if in_progress else ""
    text_col.markdown(
        f"<div class='bs-module'><h3>{t(f'home_mod_{key}_title')}{tag}</h3><p>{t(f'home_mod_{key}')}</p></div>",
        unsafe_allow_html=True,
    )
    if page and action_col.button(t("home_open"), key=f"open_{key}", width="stretch"):
        st.switch_page(page)

# Why it matters: a short history, in order
section(t("home_history_title"))
st.markdown(
    "<div class='bs-timeline'>"
    + "".join(f"<div class='bs-year'>{year}</div><div class='bs-event'>{event}</div>"
              for year, event in STRINGS["home_history"])
    + "</div>",
    unsafe_allow_html=True,
)
