"""Couleurs et petits éléments de mise en page.

Les couleurs des graphiques suivent une palette validée pour les daltoniens.
Il y a deux versions : une pour le thème sombre (par défaut), une pour le thème clair.
"""

import streamlit as st

PALETTE = {
    "dark": {
        "surface": "#1a1a19",
        "ink": "#f0efec",
        "ink2": "#c3c2b7",
        "muted": "#898781",
        "grid": "#2c2c2a",
        "axis": "#383835",
        "nodata": "#2c2c2a",
        "data": "#3987e5",
        "on_data": "#ffffff",
        # Une couleur par type de combustible (identité, pas un classement)
        "solid": "#3987e5",
        "liquid": "#d95926",
        "gas": "#199e70",
    },
    "light": {
        "surface": "#fcfcfb",
        "ink": "#0b0b0b",
        "ink2": "#52514e",
        "muted": "#898781",
        "grid": "#e1e0d9",
        "axis": "#c3c2b7",
        "nodata": "#f0efec",
        "data": "#2a78d6",
        "on_data": "#ffffff",
        "solid": "#2a78d6",
        "liquid": "#eb6834",
        "gas": "#1baf7a",
    },
}


def theme_type() -> str:
    """'dark' ou 'light'. Le thème de config.toml est sombre ; on s'y fie en premier,
    car le thème rapporté par le navigateur n'est pas fiable au premier affichage."""
    base = st.get_option("theme.base")
    if base in ("dark", "light"):
        return base
    theme = getattr(st.context, "theme", None)
    kind = getattr(theme, "type", None)
    if kind is None and isinstance(theme, dict):
        kind = theme.get("type")
    return "light" if kind == "light" else "dark"


def colors() -> dict:
    return PALETTE[theme_type()]


def page_header(title: str, lead: str | None = None) -> None:
    st.title(title)
    if lead:
        st.markdown(f"<p class='bs-lead'>{lead}</p>", unsafe_allow_html=True)


def inject_css() -> None:
    st.markdown(
        """
        <style>
        .bs-lead { font-size: 1.1rem; line-height: 1.55; opacity: 0.85; max-width: 46rem; }
        .bs-hero { font-size: 3.4rem !important; font-weight: 750; letter-spacing: -0.03em; line-height: 1.1; margin: 0.5rem 0 0.8rem 0; }
        .bs-hero span { color: #3987e5; }
        .bs-footer { font-size: 0.8rem; opacity: 0.6; margin-top: 3rem; }
        .bs-key { display: inline-flex; align-items: center; gap: 0.4rem; margin-right: 1.2rem; font-size: 0.9rem; }
        .bs-dot { width: 12px; height: 12px; border-radius: 50%; border: 2px solid currentColor; display: inline-block; }
        .bs-dot.filled { background: currentColor; }
        </style>
        """,
        unsafe_allow_html=True,
    )
