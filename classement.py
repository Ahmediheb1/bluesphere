"""Classement selon l'environnement (module 2) : score de risque, confiance, et essais de la NASA les plus proches."""

import pandas as pd
import streamlit as st

import charts
import risk
from data import load_experiments, material_label
from i18n import get_lang, t
from style import page_header

ENV_KEYS = list(risk.ENVIRONMENTS) + ["custom"]
GRAVITIES = ["micro", "moon", "mars", "earth"]
ENV_SOURCES = [
    ("Space Apps 2026, Flame in Freefall", "https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/"),
    ("NASA, A Researcher's Guide to Combustion Science (2015)",
     "https://www.nasa.gov/missions/station/a-researchers-guide-to-combustion-science/"),
    ("Abercromby et al., NASA, 2022 : 8,2 psia / 34 % O₂",
     "https://ntrs.nasa.gov/api/citations/20220005709/downloads/AsMA%202022%20-%20Abercromby%20-%20DCS%20Strategic%20Plan%20v2.pdf"),
    ("Ferkul et al., 2017, Saffire-I et II (NASA)", "https://ntrs.nasa.gov/api/citations/20170008805/downloads/20170008805.pdf"),
    ("BASS-II (PSI-25)", "https://psi.nasa.gov/physci/repo/data/investigations/PSI-25"),
]


def num(x: float, digits: int = 1) -> str:
    """Nombre avec la virgule en français."""
    text = f"{x:.{digits}f}"
    return text.replace(".", ",") if get_lang() == "fr" else text


page_header(t("rank_title"), t("rank_lead"))
df = load_experiments()

# Les poids de l'équipe, gardés d'une page à l'autre ; les curseurs sont plus bas, dans un volet
for key, value in risk.DEFAULT_WEIGHTS.items():
    st.session_state.setdefault(f"w_{key}", value)

# 1. Les choix : environnement, matériau, épaisseur
env_key = st.pills(
    t("rank_env"), ENV_KEYS, default="moon_base", format_func=lambda k: t(f"env_{k}"), key="rank_env"
) or "moon_base"
col_mat, col_thick = st.columns(2, gap="large")
with col_mat:
    material = st.selectbox(t("rank_material"), list(risk.MATERIALS), format_func=lambda k: t(f"mat_{k}"),
                            key="rank_material")
with col_thick:
    thickness = st.select_slider(t("rank_thickness"), options=risk.THICKNESS_CHOICES_MM,
                                 value=risk.DEFAULT_THICKNESS_MM[material], key=f"rank_thick_{material}",
                                 format_func=lambda v: num(v, 2).rstrip("0").rstrip(",."))

if env_key == "custom":
    a, b, c, d = st.columns(4)
    env = {
        "o2": a.slider(t("rank_o2"), 14.0, 40.0, 30.0, 0.5, format="%.1f", key="custom_o2"),
        "pressure_kpa": b.slider(t("rank_pressure"), 30.0, 105.0, 70.3, 0.1, format="%.1f", key="custom_p"),
        "flow": c.slider(t("rank_flow"), 0.0, 40.0, 10.0, 0.5, format="%.1f", key="custom_flow"),
        "gravity": d.selectbox(t("rank_gravity"), GRAVITIES, index=1, format_func=lambda g: t(f"grav_{g}"),
                               key="custom_g"),
    }
else:
    env = risk.ENVIRONMENTS[env_key]
st.caption(t(f"env_note_{env_key}"))

# Ce que disent les essais de la NASA sur ce matériau
solid = df[df["fuel_state"].eq("solid")].copy()
solid["category"] = solid["material"].map(risk.material_category)
same = solid[solid["category"].eq(material)]
st.caption(t("mat_evidence", burned=int(same["outcome"].eq("burned").sum()), n=len(same)))

# 2. Le calcul
weights = {k: st.session_state[f"w_{k}"] for k in risk.FACTORS}
if sum(weights.values()) == 0:
    weights = dict(risk.DEFAULT_WEIGHTS)
values = risk.factor_values(env["o2"], material, env["flow"], thickness, env["pressure_kpa"])
points, detail = risk.score(values, weights)
ranked = risk.rank_tests(df, env, material, thickness, weights)
best = float(ranked["proximity"].iloc[0]) if not ranked.empty else None
conf, reason = risk.confidence(best, env["gravity"])
prudent = conf == "low"
final = min(100.0, points + risk.PRUDENT_MARGIN) if prudent else points

# 3. Les résultats
m1, m2, m3 = st.columns(3)
with m1:
    st.metric(t("metric_score"), t("score_of", s=f"{final:.0f}"))
    st.caption(t(f"level_{risk.level(final)}"))
with m2:
    st.metric(t("metric_confidence"), t(f"conf_{conf}"))
    st.caption(t(reason))
with m3:
    ppo2 = risk.o2_partial_pressure_kpa(env["o2"], env["pressure_kpa"])
    st.metric(t("metric_ppo2"), t("ppo2_value", kpa=num(ppo2), psi=num(ppo2 / risk.KPA_PER_PSI, 2)))
    st.caption(t("ppo2_earth"))

if prudent:
    st.info(t("prudent_mode", m=risk.PRUDENT_MARGIN, sp=f"{final:.0f}", s=f"{points:.0f}"))

max_solid_o2 = solid["o2_pct"].max()
if pd.notna(max_solid_o2) and env["o2"] > max_solid_o2 + 0.5:
    st.warning(t("o2_gap_note", max=num(max_solid_o2), o2=num(env["o2"])), icon=":material/visibility_off:")

left, right = st.columns(2, gap="large")
with left:
    st.subheader(t("rank_parts_title"))
    st.altair_chart(charts.score_parts_chart(detail["parts"], detail["max"], risk.FACTORS), width="stretch")
    st.caption(t("rank_parts_caption"))
with right:
    st.subheader(t("rank_envs_title"))
    rows = []
    for key in risk.ENVIRONMENTS:
        e = risk.ENVIRONMENTS[key]
        s, _ = risk.score(risk.factor_values(e["o2"], material, e["flow"], thickness, e["pressure_kpa"]), weights)
        rows.append({"key": key, "name": t(f"env_{key}"), "score": s, "gravity_label": t(f"grav_{e['gravity']}")})
    if env_key == "custom":
        rows.append({"key": "custom", "name": t("env_custom"), "score": points,
                     "gravity_label": t(f"grav_{env['gravity']}")})
    st.altair_chart(charts.env_ranking_chart(pd.DataFrame(rows), env_key), width="stretch")
    st.caption(t("rank_envs_caption"))

# 4. Ce qu'on sait : les essais les plus proches
st.subheader(t("rank_tests_title"))
if ranked.empty:
    st.info(t("conf_reason_no_test"))
else:
    top = ranked.head(8).copy()
    first = top.iloc[0]
    st.markdown(t("rank_best", inv=first["investigation"], test=first["test_id"], p=f"{100 * first['proximity']:.0f}",
                  outcome=t(f"outcome_{first['outcome']}").lower()))
    top["outcome"] = top["outcome"].map(lambda o: t(f"outcome_{o}"))
    top["proximity_pct"] = (100 * top["proximity"]).round().astype(int)
    top["material"] = top["material"].map(lambda m: material_label(m, get_lang()))
    top["thickness_txt"] = top["thickness_mm"].map(lambda v: "—" if pd.isna(v) else num(v, 2))
    st.dataframe(
        top[["proximity_pct", "investigation", "test_id", "material", "thickness_txt", "o2_pct", "o2_gap", "flow_cm_s",
             "outcome", "source_url"]],
        hide_index=True,
        column_config={
            "proximity_pct": st.column_config.ProgressColumn(t("col_proximity"), min_value=0, max_value=100,
                                                             format="%d %%"),
            "investigation": t("col_investigation"),
            "test_id": t("col_test"),
            "material": t("col_material"),
            "thickness_txt": t("col_thickness"),
            "o2_pct": st.column_config.NumberColumn(t("col_o2"), format="%.1f"),
            "o2_gap": st.column_config.NumberColumn(t("col_o2_gap"), format="%+.1f"),
            "flow_cm_s": st.column_config.NumberColumn(t("col_flow"), format="%.1f"),
            "outcome": t("col_outcome"),
            "source_url": st.column_config.LinkColumn(t("col_source"), display_text="PSI"),
        },
    )
    st.caption(t("rank_tests_caption"))

# 5. La pondération et la méthode
with st.expander(t("weights_title")):
    def reset_weights():
        for k, v in risk.DEFAULT_WEIGHTS.items():
            st.session_state[f"w_{k}"] = v

    cols = st.columns(len(risk.FACTORS))
    for col, key in zip(cols, risk.FACTORS):
        col.slider(t(f"f_{key}"), 0, 50, step=5, key=f"w_{key}")
    st.caption(t("weights_note", n=sum(st.session_state[f"w_{k}"] for k in risk.FACTORS)))
    st.button(t("weights_reset"), on_click=reset_weights)

with st.expander(t("method_title")):
    st.markdown(t("method_body"))
    st.markdown(f"**{t('method_sources')}**")
    st.markdown("\n".join(f"- [{name}]({url})" for name, url in ENV_SOURCES))
