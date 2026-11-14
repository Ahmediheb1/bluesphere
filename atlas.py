"""Atlas d'inflammabilité : chaque essai de la NASA sur une seule carte."""

import streamlit as st

import charts
from data import load_experiments
from i18n import t
from style import colors, page_header

page_header(t("nav_atlas"), t("atlas_lead"))

df = load_experiments()
if df.empty or df["o2_pct"].isna().all():
    st.info(t("atlas_no_data"))
    st.stop()

# Filtres : une seule rangée, au-dessus de tout ce qu'ils filtrent
col1, col2 = st.columns([3, 2])
with col1:
    investigations = sorted(df["investigation"].dropna().unique())
    chosen = st.multiselect(t("atlas_filter_investigations"), investigations, default=investigations)
with col2:
    fuels = [f for f in charts.FUEL_ORDER if f in set(df["fuel_state"])]
    chosen_fuels = st.pills(
        t("atlas_filter_fuel"), fuels, selection_mode="multi", default=fuels,
        format_func=lambda f: t(f"fuel_{f}"),
    )

view = df[df["investigation"].isin(chosen) & df["fuel_state"].isin(chosen_fuels or [])]
plotted = view.dropna(subset=["o2_pct", "flow_cm_s"])

# Légende commune aux deux panneaux : la couleur du point = le combustible, le remplissage = le résultat
c = colors()
fuel_keys = "".join(
    f"<span class='bs-key' style='color:{c['ink2']}'>"
    f"<span class='bs-dot filled' style='color:{c[f]}'></span>{t(f'fuel_{f}')}</span>"
    for f in charts.FUEL_ORDER
)
st.markdown(
    fuel_keys
    + f"<span class='bs-key' style='color:{c['ink2']}'><span class='bs-dot filled'></span>{t('outcome_burned')}</span>"
    f"<span class='bs-key' style='color:{c['ink2']}'><span class='bs-dot'></span>"
    f"{t('outcome_extinguished')} / {t('outcome_no_ignition')}</span>"
    f"<span class='bs-key' style='color:{c['muted']}'>{t('atlas_n_shown', n=len(plotted))}</span>",
    unsafe_allow_html=True,
)

if plotted.empty:
    st.info(t("atlas_no_data"))
else:
    domain = charts.y_domain(plotted)
    left, right = st.columns([1, 3], gap="small")
    with left:
        st.altair_chart(charts.still_air_chart(view, domain), width="stretch")
    with right:
        st.altair_chart(charts.moving_air_chart(view, domain), width="stretch")
    st.caption(t("atlas_lead_2"))
    st.caption(t("atlas_ref_vent"))

# Zones sans données : calculées sur toutes les données, pas seulement le filtre
st.subheader(t("atlas_coverage_title"))
st.markdown(t("atlas_coverage_lead"))
st.altair_chart(charts.coverage_chart(df), width="stretch")
st.caption(t("atlas_coverage_note"))

# Le tableau : les mêmes valeurs, lisibles sans le graphique
with st.expander(t("atlas_table")):
    table = view[[
        "investigation", "test_id", "material", "fuel_state", "o2_pct",
        "pressure_kpa", "flow_cm_s", "outcome", "outcome_detail", "n_tests", "notes", "source_url",
    ]].copy()
    table["fuel_state"] = table["fuel_state"].map(lambda f: t(f"fuel_{f}") if f in charts.FUEL_ORDER else f)
    table["outcome"] = table["outcome"].map(lambda o: t(f"outcome_{o}"))
    st.dataframe(
        table,
        hide_index=True,
        column_config={
            "investigation": t("col_investigation"),
            "test_id": t("col_test"),
            "material": t("col_material"),
            "fuel_state": t("col_fuel"),
            "o2_pct": st.column_config.NumberColumn(t("col_o2"), format="%.1f"),
            "pressure_kpa": st.column_config.NumberColumn(t("col_pressure"), format="%.0f"),
            "flow_cm_s": st.column_config.NumberColumn(t("col_flow"), format="%.1f"),
            "outcome": t("col_outcome"),
            "outcome_detail": t("col_detail"),
            "n_tests": st.column_config.NumberColumn(t("col_n_tests"), format="%d"),
            "notes": t("col_notes"),
            "source_url": st.column_config.LinkColumn(t("col_source"), display_text="PSI"),
        },
    )
