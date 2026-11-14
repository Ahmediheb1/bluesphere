"""BlueSphere charts (Altair).

Rules: one color per fuel type (3 at most on a scatter plot), the test outcome carried by the fill
(filled = burned, hollow = went out), quiet reference lines, and every value also readable in a table.

The atlas has two panels that share the oxygen axis:
- left, tests in still air (0 cm/s: FLEX droplets, ACME BRE gas flames);
- right, tests with an air flow (BASS-II, Saffire).
"""

import hashlib

import altair as alt
import pandas as pd

import data as d
from style import CHART_FONT, colors
from texts import t

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


def _finish(chart, height: int = HEIGHT, top: int = 12):
    c = colors()
    return (
        chart.properties(height=height, background=c["surface"],
                         padding={"left": 12, "right": 12, "top": top, "bottom": 8})
        .configure(font=CHART_FONT)
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
    """The same oxygen axis for both panels."""
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
    """The Moon base band (30% and more) and the air line (21%)."""
    moon = alt.Chart(pd.DataFrame({"y0": [d.MOON_BASE_O2_PCT], "y1": [ys.domain[1]]})).mark_rect(
        color=c["ink"], opacity=0.07
    ).encode(y=alt.Y("y0:Q", scale=ys), y2="y1:Q")
    air = alt.Chart(pd.DataFrame({"y": [d.EARTH_AIR_O2_PCT]})).mark_rule(
        color=c["muted"], strokeWidth=1
    ).encode(y=alt.Y("y:Q", scale=ys))
    return moon, air


def _jitter(key: str) -> float:
    """A stable horizontal offset (between -0.5 and 0.5) to spread out points in still air."""
    return int(hashlib.md5(key.encode()).hexdigest()[:6], 16) / 0xFFFFFF - 0.5


def still_air_chart(df: pd.DataFrame, domain: list[float]):
    """Left panel: tests in still air (0 cm/s)."""
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
    """Right panel: tests with an air flow."""
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

    # Range of air speeds covered during a single test (BASS-II)
    ranges = plot[plot["flow_max_cm_s"] > plot["flow_min_cm_s"]]
    segments = alt.Chart(ranges).mark_rule(strokeWidth=2, opacity=0.3).encode(
        x=alt.X("flow_min_cm_s:Q", scale=xs), x2="flow_max_cm_s:Q", y=alt.Y("o2_pct:Q", scale=ys),
        color=alt.Color("fuel_label:N", scale=_fuel_scale(c), legend=None),
    )
    pts = _points(plot, x, y, c)
    layers = [moon, air, vent, segments, pts, moon_label, air_label, vent_label]

    # The key message: no test with an air flow in the Moon base atmosphere
    if not (plot["o2_pct"] >= d.MOON_BASE_O2_PCT).any():
        mid = (d.MOON_BASE_O2_PCT + domain[1]) / 2
        layers.append(alt.Chart(pd.DataFrame({"x": [x_max / 2], "y": [mid]})).mark_text(
            align="center", baseline="middle", color=c["ink"], fontSize=15, fontWeight="bold"
        ).encode(x=alt.X("x:Q", scale=xs), y=alt.Y("y:Q", scale=ys), text=alt.value(t("atlas_moon_gap"))))
    return _finish(alt.layer(*layers))


def coverage_table(df: pd.DataFrame) -> pd.DataFrame:
    """Number of tested conditions by oxygen band and gravity, empty cells included."""
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
    """Coverage map: one cell per (oxygen, gravity)."""
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
    # Outline of the Moon base cell (30% and more, lunar gravity)
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
                    padding={"left": 12, "right": 12, "top": 12, "bottom": 8})
        .configure(font=CHART_FONT)
        .configure_axis(labelColor=c["ink2"], labelFontSize=12, grid=False)
        .configure_view(stroke=None)
    )


# --- Ranking by environment ------------------------------------------------------------------

def score_parts_chart(parts: dict, maxima: dict, order: list[str]):
    """Points added by each factor, on a track that shows the most it can add."""
    c = colors()
    rows = pd.DataFrame({
        "factor": [t(f"f_{k}") for k in order],
        "points": [round(parts[k], 1) for k in order],
        "max": [round(maxima[k], 1) for k in order],
    })
    rows["label"] = rows.apply(lambda r: f"{r['points']:.0f} / {r['max']:.0f}", axis=1)
    y = alt.Y("factor:N", sort=list(rows["factor"]), title=None, axis=alt.Axis(labelLimit=160))
    x_scale = alt.Scale(domain=[0, max(rows["max"].max(), 1)])
    track = alt.Chart(rows).mark_bar(color=c["nodata"], cornerRadiusEnd=4, height=18).encode(
        y=y, x=alt.X("max:Q", scale=x_scale, title=t("points")),
        tooltip=[alt.Tooltip("factor:N", title=" "), alt.Tooltip("max:Q", title=t("points_max"), format=".0f")],
    )
    bars = alt.Chart(rows).mark_bar(color=c["data"], cornerRadiusEnd=4, height=18).encode(
        y=y, x=alt.X("points:Q", scale=x_scale),
        tooltip=[alt.Tooltip("factor:N", title=" "), alt.Tooltip("points:Q", title=t("points"), format=".1f"),
                 alt.Tooltip("max:Q", title=t("points_max"), format=".0f")],
    )
    labels = alt.Chart(rows).mark_text(align="left", dx=6, color=c["ink2"], fontSize=12).encode(
        y=y, x=alt.X("max:Q", scale=x_scale), text="label:N",
    )
    return _finish(track + bars + labels, height=210)


def env_ranking_chart(rows: pd.DataFrame, selected: str):
    """Score of each environment with the same material, from riskiest to least risky."""
    c = colors()
    rows = rows.sort_values("score", ascending=False).copy()
    rows["is_selected"] = rows["key"].eq(selected)
    rows["label"] = rows["score"].map(lambda s: f"{s:.0f}")
    y = alt.Y("name:N", sort=list(rows["name"]), title=None, axis=alt.Axis(labelLimit=220))
    x_scale = alt.Scale(domain=[0, 100])
    bars = alt.Chart(rows).mark_bar(cornerRadiusEnd=4, height=18).encode(
        y=y,
        x=alt.X("score:Q", scale=x_scale, title=t("metric_score")),
        color=alt.condition("datum.is_selected", alt.value(c["data"]), alt.value(c["muted"])),
        tooltip=[alt.Tooltip("name:N", title=t("rank_env")), alt.Tooltip("score:Q", title=t("metric_score"), format=".0f"),
                 alt.Tooltip("gravity_label:N", title=t("rank_gravity"))],
    )
    labels = alt.Chart(rows).mark_text(align="left", dx=6, color=c["ink2"], fontSize=12).encode(
        y=y, x=alt.X("score:Q", scale=x_scale), text="label:N",
    )
    return _finish(bars + labels, height=40 * len(rows) + 40)


# --- Live detection ---------------------------------------------------------------------------

def signal_chart(det: pd.DataFrame, signal: str, t_now: float, events: list[tuple[float, str]], y_title: str,
                 x_max: float):
    """One sensor signal up to the current time; readings flagged as abnormal are shown in orange."""
    c = colors()
    now = det[det["t"] <= t_now].copy()
    now["value"] = now[signal]
    now["abnormal"] = now[f"{signal}_abnormal"]
    xs = alt.Scale(domain=[0, x_max], nice=False)
    ys = alt.Scale(zero=False, nice=True)
    x = alt.X("t:Q", scale=xs, title=t("det_x"), axis=alt.Axis(values=list(range(0, int(x_max) + 1, 120)), grid=False))
    line = alt.Chart(now).mark_line(color=c["data"], strokeWidth=2).encode(
        x=x, y=alt.Y("value:Q", scale=ys, title=y_title),
        tooltip=[alt.Tooltip("t:Q", title=t("det_x")), alt.Tooltip("value:Q", title=y_title, format=".3g")],
    )
    flagged = alt.Chart(now[now["abnormal"]]).mark_circle(color=c["ember"], size=36, opacity=1).encode(
        x=x, y=alt.Y("value:Q", scale=ys),
    )
    shown = [(when, label) for when, label in events if when <= t_now]
    layers = [line, flagged]
    if shown:
        ev = pd.DataFrame(shown, columns=["t", "label"])
        layers.append(alt.Chart(ev).mark_rule(color=c["muted"], strokeDash=[4, 4]).encode(x=x))
        # Event names sit just above the plot, so they never cover the data or the axis title.
        layers.append(alt.Chart(ev).mark_text(align="left", baseline="bottom", dx=4, dy=-3, color=c["ink2"], fontSize=11)
                      .encode(x=x, y=alt.value(0), text="label:N"))
    return _finish(alt.layer(*layers), height=200, top=24)
