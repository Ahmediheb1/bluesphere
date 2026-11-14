"""Graphiques de BlueSphere (Altair).

Règles suivies : une couleur par type de combustible (3 au maximum sur un nuage de points),
le résultat de l'essai porté par le remplissage (plein = a brûlé, vide = éteint),
des lignes de repère discrètes, et les valeurs toujours lisibles dans le tableau.

L'Atlas a deux panneaux qui partagent l'axe de l'oxygène :
- à gauche, les essais en air immobile (0 cm/s : gouttes de FLEX, flammes de gaz d'ACME BRE) ;
- à droite, les essais avec un courant d'air (BASS-II, Saffire).
"""

import hashlib

import altair as alt
import pandas as pd

import data as d
from i18n import t
from style import colors

FUEL_ORDER = ["solid", "liquid", "gas"]
GRAVITY_ORDER = ["micro", "moon", "mars", "earth"]
O2_BAND_ORDER = ["o2_high", "o2_mid", "o2_low"]
HEIGHT = 520


def _axis(c: dict) -> dict:
    return dict(
        gridColor=c["grid"], domainColor=c["axis"], tickColor=c["axis"],
        labelColor=c["ink2"], titleColor=c["ink2"], labelFontSize=12, titleFontSize=13,
        titleFontWeight="normal",
    )


def _finish(chart, height: int = HEIGHT):
    c = colors()
    return (
        chart.properties(height=height, background=c["surface"],
                         padding={"left": 8, "right": 8, "top": 8, "bottom": 8})
        .configure_axis(**_axis(c))
        .configure_view(stroke=None)
    )


def _prepare(df: pd.DataFrame) -> pd.DataFrame:
    plot = df.dropna(subset=["o2_pct", "flow_cm_s"]).copy()
    plot["fuel_label"] = plot["fuel_state"].map(lambda f: t(f"fuel_{f}") if f in FUEL_ORDER else f)
    plot["outcome_label"] = plot["outcome"].map(lambda o: t(f"outcome_{o}"))
    plot["pressure_txt"] = plot["pressure_kpa"].map(lambda p: "—" if pd.isna(p) else f"{p:.0f}")
    plot["n_txt"] = plot["n_tests"].map(lambda n: "—" if pd.isna(n) else f"{n:.0f}")
    plot["is_still"] = plot["flow_max_cm_s"].fillna(plot["flow_cm_s"]).eq(0)
    return plot


def y_domain(df: pd.DataFrame) -> list[float]:
    """Le même axe d'oxygène pour les deux panneaux."""
    o2 = df["o2_pct"].dropna()
    low = float(o2.min()) if len(o2) else 21.0
    high = float(o2.max()) if len(o2) else 21.0
    return [min(12.0, low - 1.5), max(42.0, high + 2.0)]


def _fuel_scale(c: dict) -> alt.Scale:
    return alt.Scale(domain=[t(f"fuel_{f}") for f in FUEL_ORDER], range=[c[f] for f in FUEL_ORDER])


def _tooltip() -> list:
    return [
        alt.Tooltip("investigation:N", title=t("col_investigation")),
        alt.Tooltip("test_id:N", title=t("col_test")),
        alt.Tooltip("material:N", title=t("col_material")),
        alt.Tooltip("o2_pct:Q", title=t("col_o2"), format=".1f"),
        alt.Tooltip("flow_cm_s:Q", title=t("col_flow"), format=".1f"),
        alt.Tooltip("pressure_txt:N", title=t("col_pressure")),
        alt.Tooltip("outcome_label:N", title=t("col_outcome")),
        alt.Tooltip("outcome_detail:N", title=t("col_detail")),
        alt.Tooltip("n_txt:N", title=t("col_n_tests")),
    ]


def _points(plot: pd.DataFrame, x, y, c: dict):
    fuel = _fuel_scale(c)
    return alt.Chart(plot).mark_point(shape="circle", size=100, strokeWidth=2, opacity=1).encode(
        x=x, y=y,
        color=alt.Color("fuel_label:N", scale=fuel, legend=None),
        fill=alt.condition("datum.burned", alt.Fill("fuel_label:N", scale=fuel, legend=None),
                           alt.value(c["surface"])),
        tooltip=_tooltip(),
    )


def _references(ys: alt.Scale, c: dict):
    """Bande de la base lunaire (30 % et plus) et ligne de l'air (21 %)."""
    moon = alt.Chart(pd.DataFrame({"y0": [d.MOON_BASE_O2_PCT], "y1": [ys.domain[1]]})).mark_rect(
        color=c["ink"], opacity=0.07
    ).encode(y=alt.Y("y0:Q", scale=ys), y2="y1:Q")
    air = alt.Chart(pd.DataFrame({"y": [d.EARTH_AIR_O2_PCT]})).mark_rule(
        color=c["muted"], strokeWidth=1
    ).encode(y=alt.Y("y:Q", scale=ys))
    return moon, air


def _jitter(key: str) -> float:
    """Décalage horizontal stable (entre -0,5 et 0,5) pour séparer les points en air immobile."""
    return int(hashlib.md5(key.encode()).hexdigest()[:6], 16) / 0xFFFFFF - 0.5


def still_air_chart(df: pd.DataFrame, domain: list[float]):
    """Panneau de gauche : essais en air immobile (0 cm/s)."""
    c = colors()
    plot = _prepare(df)
    plot = plot[plot["is_still"]].copy()
    ys = alt.Scale(domain=domain, nice=False, zero=False)
    y = alt.Y("o2_pct:Q", title=t("atlas_y"), scale=ys, axis=alt.Axis(tickMinStep=5))
    moon, air = _references(ys, c)
    if plot.empty:
        return _finish(alt.layer(moon, air))
    plot["jitter"] = [_jitter(f"{a}|{b}|{i}") for i, (a, b) in
                      enumerate(zip(plot["investigation"], plot["test_id"]))]
    order = [i for i in ["FLEX", "ACME BRE"] if i in set(plot["investigation"])]
    order += sorted(set(plot["investigation"]) - set(order))
    x = alt.X("investigation:N", sort=order, title=t("atlas_still_air_title"),
              axis=alt.Axis(labelAngle=0, domain=False, ticks=False, labelPadding=6),
              scale=alt.Scale(paddingInner=0.3, paddingOuter=0.2))
    pts = _points(plot, x, y, c).encode(
        xOffset=alt.XOffset("jitter:Q", scale=alt.Scale(domain=[-0.65, 0.65]))
    )
    return _finish(alt.layer(moon, air, pts))


def moving_air_chart(df: pd.DataFrame, domain: list[float]):
    """Panneau de droite : essais avec un courant d'air."""
    c = colors()
    plot = _prepare(df)
    plot = plot[~plot["is_still"]].copy()
    ys = alt.Scale(domain=domain, nice=False, zero=False)
    x_max = max(30.0, float(plot["flow_max_cm_s"].max() if len(plot) else 0) * 1.04)
    xs = alt.Scale(domain=[-1, x_max], nice=False, zero=False)
    x = alt.X("flow_cm_s:Q", title=t("atlas_x"), scale=xs,
              axis=alt.Axis(values=list(range(0, int(x_max) + 1, 5)), grid=False))
    y = alt.Y("o2_pct:Q", title=None, scale=ys, axis=alt.Axis(tickMinStep=5))

    moon, air = _references(ys, c)
    moon_label = alt.Chart(pd.DataFrame({"x": [x_max], "y": [domain[1]]})).mark_text(
        align="right", baseline="top", dx=-6, dy=6, color=c["ink2"], fontSize=12
    ).encode(x=alt.X("x:Q", scale=xs), y=alt.Y("y:Q", scale=ys), text=alt.value(t("atlas_ref_moon")))
    air_label = alt.Chart(pd.DataFrame({"x": [x_max], "y": [d.EARTH_AIR_O2_PCT]})).mark_text(
        align="right", baseline="bottom", dx=-6, dy=-4, color=c["ink2"], fontSize=12
    ).encode(x=alt.X("x:Q", scale=xs), y=alt.Y("y:Q", scale=ys), text=alt.value(t("atlas_ref_air")))
    vent = alt.Chart(pd.DataFrame({"x": [d.TYPICAL_VENTILATION_CM_S]})).mark_rule(
        color=c["muted"], strokeWidth=1
    ).encode(x=alt.X("x:Q", scale=xs))
    vent_label = alt.Chart(pd.DataFrame({"x": [d.TYPICAL_VENTILATION_CM_S], "y": [domain[0]]})).mark_text(
        align="left", baseline="bottom", dx=6, dy=-6, color=c["ink2"], fontSize=12
    ).encode(x=alt.X("x:Q", scale=xs), y=alt.Y("y:Q", scale=ys), text=alt.value(t("atlas_ref_vent_short")))

    if plot.empty:
        return _finish(alt.layer(moon, air, vent, moon_label, air_label, vent_label))

    # Plage de vitesses d'air parcourue pendant un même essai (BASS-II)
    ranges = plot[plot["flow_max_cm_s"] > plot["flow_min_cm_s"]]
    segments = alt.Chart(ranges).mark_rule(strokeWidth=2, opacity=0.3).encode(
        x=alt.X("flow_min_cm_s:Q", scale=xs), x2="flow_max_cm_s:Q", y=alt.Y("o2_pct:Q", scale=ys),
        color=alt.Color("fuel_label:N", scale=_fuel_scale(c), legend=None),
    )
    pts = _points(plot, x, y, c)
    layers = [moon, air, vent, segments, pts, moon_label, air_label, vent_label]

    # Le message clé : aucun essai avec un courant d'air dans l'atmosphère de la base lunaire
    if not (plot["o2_pct"] >= d.MOON_BASE_O2_PCT).any():
        mid = (d.MOON_BASE_O2_PCT + domain[1]) / 2
        layers.append(alt.Chart(pd.DataFrame({"x": [x_max / 2], "y": [mid]})).mark_text(
            align="center", baseline="middle", color=c["ink"], fontSize=15, fontWeight="bold"
        ).encode(x=alt.X("x:Q", scale=xs), y=alt.Y("y:Q", scale=ys), text=alt.value(t("atlas_moon_gap"))))
    return _finish(alt.layer(*layers))


def coverage_table(df: pd.DataFrame) -> pd.DataFrame:
    """Nombre de conditions testées par bande d'oxygène et par gravité, cases vides comprises."""
    counts = (
        df.assign(band=df["o2_pct"].map(d.o2_band))
        .dropna(subset=["band"])
        .groupby(["band", "gravity"]).size()
    )
    rows = []
    for band in O2_BAND_ORDER:
        for grav in GRAVITY_ORDER:
            rows.append({"band": band, "gravity": grav, "n": int(counts.get((band, grav), 0))})
    return pd.DataFrame(rows)


def coverage_chart(df: pd.DataFrame):
    """Carte des zones sans données : une case par (oxygène, gravité)."""
    c = colors()
    cov = coverage_table(df)
    cov["band_label"] = cov["band"].map(t)
    cov["grav_label"] = cov["gravity"].map(lambda g: t(f"grav_{g}"))
    cov["has_data"] = cov["n"] > 0
    cov["label"] = cov.apply(lambda r: str(r["n"]) if r["n"] else t("atlas_coverage_none"), axis=1)
    cov["is_moon_base"] = (cov["band"] == "o2_high") & (cov["gravity"] == "moon")

    x = alt.X("grav_label:N", sort=[t(f"grav_{g}") for g in GRAVITY_ORDER], title=None,
              axis=alt.Axis(orient="top", labelAngle=0, domain=False, ticks=False, labelPadding=8))
    y = alt.Y("band_label:N", sort=[t(b) for b in O2_BAND_ORDER], title=None,
              axis=alt.Axis(domain=False, ticks=False, labelPadding=8))

    cells = alt.Chart(cov).mark_rect(cornerRadius=4, stroke=c["surface"], strokeWidth=3).encode(
        x=x, y=y,
        color=alt.condition("datum.has_data", alt.value(c["data"]), alt.value(c["nodata"])),
        tooltip=[
            alt.Tooltip("band_label:N", title=t("col_o2")),
            alt.Tooltip("grav_label:N", title=" "),
            alt.Tooltip("n:Q", title=t("atlas_conditions")),
        ],
    )
    # Contour de la case de la base lunaire (30 % et plus, gravité lunaire)
    ring = alt.Chart(cov[cov["is_moon_base"]]).mark_rect(
        cornerRadius=4, fillOpacity=0, stroke=c["ink"], strokeWidth=2
    ).encode(x=x, y=y)
    text = alt.Chart(cov).mark_text(fontSize=13).encode(
        x=x, y=y, text="label:N",
        color=alt.condition("datum.has_data", alt.value(c["on_data"]), alt.value(c["muted"])),
    )
    return (
        alt.layer(cells, ring, text)
        .properties(height=210, background=c["surface"],
                    padding={"left": 8, "right": 8, "top": 8, "bottom": 8})
        .configure_axis(labelColor=c["ink2"], labelFontSize=12, grid=False)
        .configure_view(stroke=None)
    )
