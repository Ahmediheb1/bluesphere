"""Risk score and ranking of NASA tests by environment.

The weighting comes from the BlueSphere team (version 1):
oxygen 30%, material 25%, ventilation 25%, thickness 10%, pressure 10%.

Each factor is a value from 0 (little risk) to 1 (highest risk). The score is the
weighted average, out of 100. It is a relative index to compare situations,
not a probability of fire, and not a certification.

Gravity does not change the score: it changes the confidence, because no PSI test
was run in lunar or Martian gravity.
"""

import math

import pandas as pd

EARTH_PRESSURE_KPA = 101.3
KPA_PER_PSI = 6.894757

# Default weights (in %), in display order
FACTORS = ["o2", "material", "ventilation", "thickness", "pressure"]
DEFAULT_WEIGHTS = {"o2": 30, "material": 25, "ventilation": 25, "thickness": 10, "pressure": 10}

# Oxygen factor bounds: 0 at the lowest O2 where a solid burned in our tests (14.2%, BASS-II),
# 1 from 35% (just above NASA's exploration atmosphere, 34%).
O2_LOW_PCT = 14.0
O2_HIGH_PCT = 35.0

# Ventilation: a bell curve peaking near 10 cm/s (NASA guide, 2015).
VENT_PEAK_CM_S = 10.0
VENT_FLOOR = 0.3   # still air: the fire weakens, but "it goes out by itself" is a misconception
VENT_WIDTH = 0.35  # width of the bell, in decades (log scale)

# Materials tested in our solid-fuel tests, with an expert value (version 1)
MATERIALS = {
    "sibal": 1.0,     # cotton and fiberglass fabric: burned in almost every test
    "pmma": 0.8,      # acrylic plastic: burns, and can reignite (Saffire-IV)
    "nomex": 0.5,     # mixed results: no ignition in Saffire-II
    "silicone": 0.2,  # no ignition in microgravity in Saffire-II, although it burns on Earth
}
DEFAULT_THICKNESS_MM = {"sibal": 0.37, "pmma": 6.35, "nomex": 0.37, "silicone": 0.37}
THICKNESS_CHOICES_MM = [0.1, 0.25, 0.37, 0.5, 1.0, 2.0, 6.35, 10.0, 12.7]

# Environments (the rover has the same atmosphere as the Moon base, per the challenge statement)
ENVIRONMENTS = {
    "iss": {"o2": 21.0, "pressure_kpa": 101.3, "flow": 10.0, "gravity": "micro"},
    "moon_base": {"o2": 30.0, "pressure_kpa": 70.3, "flow": 10.0, "gravity": "moon"},
    "moon_rover": {"o2": 30.0, "pressure_kpa": 70.3, "flow": 10.0, "gravity": "moon"},
    "mars_ship": {"o2": 34.0, "pressure_kpa": 56.5, "flow": 10.0, "gravity": "micro"},
}

# Cautious mode: margin added to the score when confidence is low
PRUDENT_MARGIN = 10


def material_category(material: str) -> str | None:
    m = str(material).lower()
    for key in MATERIALS:
        if key in m:
            return key
    return None


def _clamp(x: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, x))


def f_o2(o2_pct: float) -> float:
    return _clamp((o2_pct - O2_LOW_PCT) / (O2_HIGH_PCT - O2_LOW_PCT))


def f_ventilation(flow_cm_s: float) -> float:
    x = math.log10((max(flow_cm_s, 0.0) + 1.0) / (VENT_PEAK_CM_S + 1.0))
    return VENT_FLOOR + (1 - VENT_FLOOR) * math.exp(-(x ** 2) / (2 * VENT_WIDTH ** 2))


def f_thickness(thickness_mm: float) -> float:
    """The thinner the material, the more easily it burns: 1 at 0.1 mm, 0.2 at 10 mm and more."""
    return _clamp(1 - 0.8 * math.log10(max(thickness_mm, 0.01) / 0.1) / 2, 0.2, 1.0)


def f_pressure(pressure_kpa: float) -> float:
    """At the same oxygen percentage, lower pressure means fewer oxygen molecules."""
    return _clamp(pressure_kpa / EARTH_PRESSURE_KPA)


def factor_values(o2: float, material: str, flow: float, thickness_mm: float, pressure_kpa: float) -> dict:
    return {
        "o2": f_o2(o2),
        "material": MATERIALS[material],
        "ventilation": f_ventilation(flow),
        "thickness": f_thickness(thickness_mm),
        "pressure": f_pressure(pressure_kpa),
    }


def score(values: dict, weights: dict) -> tuple[float, dict]:
    """Score out of 100, and each factor's share (in points) for the chart."""
    total = sum(weights.values()) or 1
    parts = {k: 100 * weights[k] * values[k] / total for k in FACTORS}
    maxima = {k: 100 * weights[k] / total for k in FACTORS}
    return sum(parts.values()), {"parts": parts, "max": maxima}


def level(points: float) -> str:
    if points >= 80:
        return "very_high"
    if points >= 60:
        return "high"
    if points >= 40:
        return "moderate"
    return "low"


def o2_partial_pressure_kpa(o2_pct: float, pressure_kpa: float) -> float:
    return o2_pct / 100 * pressure_kpa


def _similarity(diff: float, scale: float) -> float:
    return max(0.05, 1 - abs(diff) / scale)


def rank_tests(tests: pd.DataFrame, env: dict, material: str, thickness_mm: float, weights: dict) -> pd.DataFrame:
    """Rank NASA solid-fuel tests from closest to farthest from the chosen environment.

    The match is a weighted geometric mean (same weights as the score): a single large gap,
    for example 8 points of oxygen, is enough to push a test away.
    Pressure is missing from the BASS-II and Saffire tables: we use the station's (101.3 kPa).
    """
    solid = tests[tests["fuel_state"].eq("solid") & tests["o2_pct"].notna()].copy()
    if solid.empty:
        return solid
    solid["category"] = solid["material"].map(material_category)
    solid["pressure_used"] = solid["pressure_kpa"].fillna(EARTH_PRESSURE_KPA)
    solid["pressure_assumed"] = solid["pressure_kpa"].isna()
    total = sum(weights.values()) or 1

    def proximity(row) -> float:
        sims = {
            "o2": _similarity(row["o2_pct"] - env["o2"], 10),
            "material": 1.0 if row["category"] == material else 0.25,
            "ventilation": _similarity(
                math.log10((row["flow_cm_s"] if pd.notna(row["flow_cm_s"]) else 0) + 1) - math.log10(env["flow"] + 1),
                math.log10(41),
            ),
            "thickness": 0.5 if pd.isna(row["thickness_mm"]) else _similarity(
                math.log10(row["thickness_mm"]) - math.log10(thickness_mm), 2
            ),
            "pressure": _similarity(row["pressure_used"] - env["pressure_kpa"], 50),
        }
        return math.exp(sum(weights[k] * math.log(sims[k]) for k in FACTORS) / total)

    solid["proximity"] = solid.apply(proximity, axis=1)
    solid["o2_gap"] = solid["o2_pct"] - env["o2"]
    return solid.sort_values("proximity", ascending=False)


def confidence(best_proximity: float | None, gravity: str) -> tuple[str, str]:
    """Confidence level and its reason (a text key)."""
    if best_proximity is None:
        data_level, reason = "low", "conf_reason_no_test"
    elif best_proximity >= 0.8:
        data_level, reason = "high", "conf_reason_close"
    elif best_proximity >= 0.6:
        data_level, reason = "medium", "conf_reason_some"
    else:
        data_level, reason = "low", "conf_reason_far"
    if gravity in ("moon", "mars"):
        return "low", "conf_reason_gravity"
    if gravity == "earth" and data_level == "high":
        return "medium", "conf_reason_earth"
    return data_level, reason
