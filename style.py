"""Look and feel of BlueSphere: colors, type, and the few custom blocks Streamlit does not provide.

Design notes
- The page is deep space navy, the color of the night side of an orbit.
- One memorable element: the blue sphere in the hero, the shape a flame takes in microgravity.
  Everything else stays quiet.
- Type: Archivo. Headlines use its expanded width, like the labels on flight hardware.
- Chart colors (solid, liquid, gas) were checked for color-blind readers against the panel color.
"""

import streamlit as st

COLORS = {
    "space": "#0A1222",    # page background
    "surface": "#111C30",  # panels and chart backgrounds
    "line": "#22314D",     # hairlines
    "ink": "#E6ECF5",      # main text
    "ink2": "#B4C0D6",     # secondary text
    "muted": "#7F8CA6",    # captions, axis labels
    "grid": "#1E2A42",
    "axis": "#2A3A58",
    "nodata": "#1E2A42",
    "data": "#3987e5",     # one-series charts
    "on_data": "#ffffff",
    "flame": "#4DA3FF",    # brand blue for links and accents
    "ember": "#F2A541",    # the no-data zone, used sparingly
    # One color per fuel type (identity, not rank). Validated against "surface".
    "solid": "#3987e5",
    "liquid": "#d95926",
    "gas": "#199e70",
}

FONT_URL = "https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap"
FONT = "Archivo"
# Charts draw text themselves: a sans-serif fallback keeps them clean before the web font loads
CHART_FONT = "Archivo, 'Source Sans 3', 'Source Sans Pro', system-ui, sans-serif"


def colors() -> dict:
    return COLORS


def page_header(title: str, lead: str | None = None) -> None:
    st.markdown(f"<h1 class='bs-title'>{title}</h1>", unsafe_allow_html=True)
    if lead:
        st.markdown(f"<p class='bs-lead'>{lead}</p>", unsafe_allow_html=True)


def section(title: str, lead: str | None = None) -> None:
    st.markdown(f"<h2 class='bs-section'>{title}</h2>", unsafe_allow_html=True)
    if lead:
        st.markdown(f"<p class='bs-section-lead'>{lead}</p>", unsafe_allow_html=True)


def inject_css() -> None:
    c = COLORS
    st.markdown(
        f"""
        <style>
        @import url('{FONT_URL}');

        html, body, .stApp, .stMarkdown, .stCaption, button, input, textarea, select, label {{
            font-family: '{FONT}', system-ui, sans-serif;
        }}
        .stApp {{ background: {c['space']}; }}
        [data-testid="stDecoration"] {{ display: none; }}
        .block-container {{ max-width: 1180px; padding-top: 3.2rem; padding-bottom: 4rem; }}

        h1, h2, h3, .bs-title, .bs-section, .bs-wordmark {{
            font-family: '{FONT}', system-ui, sans-serif !important;
            font-stretch: 118%;
            letter-spacing: -0.01em;
        }}
        .bs-title {{ font-size: 2.6rem; font-weight: 650; line-height: 1.1; margin: 0 0 0.6rem 0; color: {c['ink']}; }}
        .bs-lead {{ font-size: 1.15rem; line-height: 1.6; color: {c['ink2']}; max-width: 44rem; margin-bottom: 1.6rem; }}
        .bs-section {{ font-size: 1.6rem; font-weight: 600; margin: 3.2rem 0 0.4rem 0; color: {c['ink']}; }}
        .bs-section-lead {{ color: {c['ink2']}; max-width: 44rem; line-height: 1.6; margin-bottom: 1.2rem; }}
        a {{ color: {c['flame']}; }}

        /* Hero */
        .bs-wordmark {{ font-size: 1.05rem; font-weight: 700; font-stretch: 125%; color: {c['flame']}; margin: 0 0 1.4rem 0; }}
        .bs-headline {{
            font-family: '{FONT}', system-ui, sans-serif; font-stretch: 112%;
            font-size: clamp(2.2rem, 4.2vw, 3.4rem); font-weight: 650; line-height: 1.06;
            letter-spacing: -0.02em; color: {c['ink']}; margin: 0 0 1.4rem 0; max-width: 19ch;
        }}
        .bs-hero-text {{ font-size: 1.18rem; line-height: 1.6; color: {c['ink2']}; max-width: 34rem; margin: 0 0 1.8rem 0; }}
        .bs-sphere-wrap {{ display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 380px; }}
        .bs-sphere {{
            width: min(300px, 70vw); aspect-ratio: 1; border-radius: 50%;
            background:
                radial-gradient(circle at 50% 54%, rgba(255, 196, 120, 0.85) 0 4%, rgba(255, 150, 70, 0.25) 9%, rgba(255, 150, 70, 0) 15%),
                radial-gradient(circle at 50% 50%, rgba(10, 18, 34, 0.0) 0 38%, rgba(77, 163, 255, 0.10) 48%,
                                rgba(110, 182, 255, 0.95) 60%, rgba(77, 163, 255, 0.45) 66%, rgba(77, 163, 255, 0) 76%);
            box-shadow: 0 0 90px 14px rgba(77, 163, 255, 0.22), inset 0 0 60px rgba(77, 163, 255, 0.18);
            animation: bs-ignite 2.4s ease-out both;
        }}
        .bs-sphere-caption {{ margin-top: 1.4rem; font-size: 0.88rem; color: {c['muted']}; text-align: center; max-width: 22rem; line-height: 1.5; }}
        @keyframes bs-ignite {{
            0% {{ opacity: 0; transform: scale(0.82); filter: blur(6px); }}
            60% {{ opacity: 1; filter: blur(0); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}
        @media (prefers-reduced-motion: reduce) {{ .bs-sphere {{ animation: none; }} }}

        /* Key numbers: a quiet row, separated by hairlines */
        .bs-stats {{ display: grid; grid-template-columns: repeat(4, 1fr); border-top: 1px solid {c['line']}; border-bottom: 1px solid {c['line']}; margin: 1rem 0 0.5rem 0; }}
        .bs-stat {{ padding: 1.2rem 1.2rem 1.1rem 0; }}
        .bs-stat + .bs-stat {{ padding-left: 1.2rem; border-left: 1px solid {c['line']}; }}
        .bs-stat-value {{ font-size: 2.1rem; font-weight: 600; font-stretch: 112%; color: {c['ink']}; line-height: 1.1; font-variant-numeric: tabular-nums; }}
        .bs-stat-label {{ font-size: 0.92rem; color: {c['ink2']}; margin-top: 0.35rem; line-height: 1.4; }}
        @media (max-width: 720px) {{
            .bs-stats {{ grid-template-columns: repeat(2, 1fr); }}
            .bs-stat:nth-child(3) {{ padding-left: 0; border-left: none; }}
        }}

        /* Oxygen ruler */
        .bs-ruler {{ background: {c['surface']}; border: 1px solid {c['line']}; border-radius: 10px; padding: 1.2rem 1.2rem 0.6rem 1.2rem; }}
        .bs-ruler svg {{ width: 100%; height: auto; display: block; }}
        .bs-ruler-note {{ font-size: 0.9rem; color: {c['muted']}; margin-top: 0.6rem; line-height: 1.5; }}

        /* Modules: a list, not a grid of identical cards */
        .bs-module {{ padding: 0.9rem 0 0.4rem 0; }}
        .bs-module h3 {{ font-size: 1.25rem; font-weight: 600; margin: 0 0 0.3rem 0; color: {c['ink']}; }}
        .bs-module p {{ color: {c['ink2']}; margin: 0; line-height: 1.55; max-width: 44rem; }}
        .bs-tag {{ display: inline-block; font-size: 0.78rem; color: {c['ember']}; border: 1px solid {c['ember']}; border-radius: 999px; padding: 0.05rem 0.55rem; margin-left: 0.6rem; vertical-align: middle; font-stretch: 100%; }}

        /* History: a real sequence, so it gets years */
        .bs-timeline {{ display: grid; grid-template-columns: 5.5rem 1fr; row-gap: 0.9rem; column-gap: 1rem; max-width: 46rem; }}
        .bs-year {{ font-weight: 650; font-stretch: 118%; color: {c['flame']}; font-variant-numeric: tabular-nums; }}
        .bs-event {{ color: {c['ink2']}; line-height: 1.55; }}

        .bs-footer {{ font-size: 0.85rem; color: {c['muted']}; margin-top: 4rem; padding-top: 1.2rem; border-top: 1px solid {c['line']}; max-width: 60rem; line-height: 1.6; }}

        /* Atlas legend */
        .bs-key {{ display: inline-flex; align-items: center; gap: 0.4rem; margin-right: 1.2rem; font-size: 0.92rem; }}
        .bs-dot {{ width: 12px; height: 12px; border-radius: 50%; border: 2px solid currentColor; display: inline-block; }}
        .bs-dot.filled {{ background: currentColor; }}

        /* Streamlit pieces, tuned to the palette */
        [data-testid="stMetric"] {{ background: {c['surface']}; border: 1px solid {c['line']}; border-radius: 10px; padding: 0.9rem 1rem; }}
        [data-testid="stExpander"] details {{ border-color: {c['line']}; border-radius: 10px; }}
        [data-testid="stVegaLiteChart"] {{ border-radius: 10px; overflow: hidden; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def oxygen_ruler(solid_min: float, solid_max: float, other_min: float, other_max: float,
                 earth: float = 21.0, moon: float = 30.0, exploration: float = 34.0) -> str:
    """An SVG scale of oxygen levels: where NASA tested solids in microgravity, and where the Moon base will live."""
    c = COLORS
    lo, hi, left, right = 10.0, 40.0, 30.0, 970.0

    def x(v: float) -> float:
        return left + (min(max(v, lo), hi) - lo) / (hi - lo) * (right - left)

    ticks = "".join(
        f"<line x1='{x(v):.1f}' y1='132' x2='{x(v):.1f}' y2='138' stroke='{c['axis']}' />"
        f"<text x='{x(v):.1f}' y='156' fill='{c['muted']}' font-size='13' text-anchor='middle'>{v:.0f}%</text>"
        for v in range(10, 41, 5)
    )
    return f"""
<div class="bs-ruler" role="img" aria-label="Oxygen levels: solids were tested in microgravity from {solid_min:.1f}% to {solid_max:.1f}%; the Moon base will likely have {moon:.0f}% or more.">
<svg viewBox="0 0 1000 168" xmlns="http://www.w3.org/2000/svg" font-family="Archivo, sans-serif">
  <defs>
    <pattern id="bs-hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="8" stroke="{c['ember']}" stroke-width="2" stroke-opacity="0.55" />
    </pattern>
  </defs>
  <rect x="{x(moon):.1f}" y="70" width="{x(hi) - x(moon):.1f}" height="30" fill="url(#bs-hatch)" rx="4" />
  <text x="{(x(moon) + x(hi)) / 2:.1f}" y="90" fill="{c['ember']}" font-size="14" font-weight="600" text-anchor="middle"
        paint-order="stroke" stroke="{c['surface']}" stroke-width="5">No solid tested here</text>
  <rect x="{x(solid_min):.1f}" y="70" width="{x(solid_max) - x(solid_min):.1f}" height="30" fill="{c['data']}" rx="4" />
  <text x="{(x(solid_min) + x(solid_max)) / 2:.1f}" y="90" fill="#ffffff" font-size="14" font-weight="600" text-anchor="middle">Solids tested</text>
  <line x1="{x(other_min):.1f}" y1="112" x2="{x(other_max):.1f}" y2="112" stroke="{c['ink2']}" stroke-width="2" stroke-dasharray="5 5" />
  <text x="{x(other_max):.1f}" y="126" fill="{c['muted']}" font-size="12.5" text-anchor="end">Gas flames and fuel droplets</text>
  <line x1="{x(earth):.1f}" y1="30" x2="{x(earth):.1f}" y2="132" stroke="{c['ink2']}" stroke-width="1.5" />
  <text x="{x(earth) - 6:.1f}" y="26" fill="{c['ink2']}" font-size="13.5" text-anchor="end">Earth's air, {earth:.0f}%</text>
  <line x1="{x(moon):.1f}" y1="30" x2="{x(moon):.1f}" y2="132" stroke="{c['ember']}" stroke-width="2" />
  <text x="{x(moon) + 6:.1f}" y="26" fill="{c['ember']}" font-size="13.5" font-weight="600">Moon base, {moon:.0f}% or more</text>
  <line x1="{x(exploration):.1f}" y1="48" x2="{x(exploration):.1f}" y2="132" stroke="{c['muted']}" stroke-width="1" stroke-dasharray="3 3" />
  <text x="{x(exploration) + 6:.1f}" y="46" fill="{c['muted']}" font-size="12.5">NASA exploration atmosphere, {exploration:.0f}%</text>
  <line x1="{left}" y1="132" x2="{right}" y2="132" stroke="{c['axis']}" />
  {ticks}
</svg>
</div>
"""
