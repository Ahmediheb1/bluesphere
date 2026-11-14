"""After the fire (module 4): why the danger continues once the flame is out."""

import streamlit as st

from knowledge import SOURCES
from style import COLORS, page_header, section
from texts import STRINGS, t


SHORT_NAMES = {
    "S2": "NASA guide to combustion science, 2015",
    "S5": "Fortenberry et al., 2021",
    "S6": "Brooker and Niehaus, NASA, 2022",
    "S8": "Olson et al., NASA Glenn, 2009",
    "S9": "Ross et al., NASA SP-4225",
}


def source_link(key: str) -> str:
    if not key:
        return ""
    title, url = SOURCES[key]
    short = SHORT_NAMES.get(key, title)
    return f"<a href='{url}' target='_blank'>{short}</a>" if url else short


def phase_strip(phases: list) -> str:
    """The phases of a cabin fire as a horizontal sequence; the last one is the danger."""
    c = COLORS
    n = len(phases)
    cells = []
    for i, (name, text, src) in enumerate(phases):
        last = i == n - 1
        color = c["ember"] if last else c["flame"]
        cells.append(
            f"<div class='bs-phase{' bs-phase-last' if last else ''}'>"
            f"<div class='bs-phase-dot' style='background:{color}'></div>"
            f"<div class='bs-phase-name' style='color:{color if last else c['ink']}'>{name}</div>"
            f"<div class='bs-phase-text'>{text}</div>"
            f"<div class='bs-phase-src'>{source_link(src)}</div></div>"
        )
    return (
        "<style>"
        f".bs-phases {{ display: grid; grid-template-columns: repeat({n}, 1fr); gap: 0; position: relative; margin: 0.6rem 0 0.4rem 0; }}"
        f".bs-phases::before {{ content: ''; position: absolute; left: 6px; right: 6px; top: 6px; height: 2px; background: {c['line']}; }}"
        ".bs-phase { position: relative; padding-right: 1.2rem; }"
        ".bs-phase-dot { width: 14px; height: 14px; border-radius: 50%; position: relative; z-index: 1; }"
        f".bs-phase-last .bs-phase-dot {{ box-shadow: 0 0 0 5px rgba(242, 165, 65, 0.18); }}"
        ".bs-phase-name { font-weight: 650; font-stretch: 112%; margin: 0.8rem 0 0.35rem 0; font-size: 1.02rem; }"
        f".bs-phase-text {{ color: {c['ink2']}; font-size: 0.95rem; line-height: 1.5; }}"
        f".bs-phase-src {{ font-size: 0.82rem; color: {c['muted']}; margin-top: 0.45rem; }}"
        "@media (max-width: 820px) { .bs-phases { grid-template-columns: 1fr; row-gap: 1.2rem; } .bs-phases::before { display: none; } }"
        "</style>"
        "<div class='bs-phases'>" + "".join(cells) + "</div>"
    )


page_header(t("after_title"), t("after_lead"))

section(t("after_timeline_title"), t("after_timeline_lead"))
st.markdown(phase_strip(STRINGS["after_phases"]), unsafe_allow_html=True)

section(t("after_findings_title"))
for title, where, text, src in STRINGS["after_findings"]:
    st.markdown(
        f"<div class='bs-finding'><h3>{title}</h3>"
        f"<p class='bs-finding-where'>{where}</p>"
        f"<p>{text}</p>"
        f"<p class='bs-finding-src'>{t('after_source')}: {source_link(src)}</p></div>",
        unsafe_allow_html=True,
    )

section(t("after_check_title"), t("after_check_lead"))
for check, why, src in STRINGS["after_checks"]:
    st.markdown(
        f"<div class='bs-check'><span class='bs-check-box'></span><div>"
        f"<p class='bs-check-title'>{check}</p>"
        f"<p class='bs-check-why'>{why} {source_link(src)}</p></div></div>",
        unsafe_allow_html=True,
    )

st.markdown(
    f"<div class='bs-moon-note'><h3>{t('after_moon_title')}</h3><p>{t('after_moon')}</p></div>",
    unsafe_allow_html=True,
)
if st.button(t("after_ask"), type="primary"):
    st.switch_page("assistant.py")
