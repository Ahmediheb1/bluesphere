"""Build experiments.csv from the PSI test tables (the PSI-*.csv files).

Run:  py build_dataset.py

Each output row is one test, or a group of identical tests (column n_tests).
How each raw table is read is explained in DATA.md.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent  # every file sits at the root of the project
RAW = ROOT
OUT = ROOT / "experiments.csv"

COLUMNS = [
    "investigation", "psi_id", "test_id", "material", "fuel_state", "geometry", "thickness_mm",
    "o2_pct", "pressure_kpa", "flow_cm_s", "flow_min_cm_s", "flow_max_cm_s", "flow_direction",
    "gravity", "outcome", "outcome_detail", "spread_rate_mm_s", "burn_time_s", "n_tests",
    "co2_rise_pct", "co_rise_ppm", "notes",
]


def num(value):
    """A number, or NaN if the cell does not hold one (none, OR, over, >500...)."""
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return np.nan


# ---------------------------------------------------------------- BASS-II (PSI-25)

def bass_flows(air: str) -> list[float]:
    """Air speeds written in "Air display" (cm/s; the tunnel went up to 40 cm/s).

    Removed: values in parentheses (fan potentiometer settings), and everything after the word
    "pot" (potentiometer readings, not speeds). "<1" becomes 0.5.
    """
    if not isinstance(air, str):
        return []
    s = air.lower().replace("<1", " 0.5 ")
    inside = " ".join(re.findall(r"\(([^)]*)\)", s))
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"\bp(?:ots?|t)\b.*$", " ", s)       # everything after "pot", "pots" or "pt"

    def numbers(text: str) -> list[float]:
        return [float(x) for x in re.findall(r"\d+\.?\d*|\.\d+", text)]

    values = [v for v in numbers(s) if 0 <= v <= 40]
    if not values and "pot" not in inside:
        # A few rows are reversed: potentiometer outside, speeds in parentheses (e.g. O13a)
        values = [v for v in numbers(inside) if 0 <= v <= 40]
    return values


def bass_outcome(fan: str, air: str) -> tuple[str, str]:
    text = f"{fan} {air}".lower()
    if "no ign" in text:
        return "no_ignition", "no ignition at any air speed"
    if "blowoff" in text:
        return "extinguished", "flame blown off by air that was too fast"
    if "would not stay lit" in text:
        return "extinguished", "the flame would not stay lit"
    if re.search(r"ext|extinguished|\bout\b", text):
        return "extinguished", "flame went out as the air was reduced"
    if re.search(r"\boff\b", text):
        return "unknown", "fan turned off, outcome not recorded"
    # No extinction word in the table: the flame is counted as burning at the listed air speeds
    return "burned", "the flame burned at the listed air speeds"


def bass_material(text: str) -> tuple[str, str, float]:
    """(material, geometry, thickness or diameter in mm)."""
    t = text.lower()
    if "sibal" in t:
        return "SIBAL (cotton and fiberglass)", "fabric", np.nan
    if "nomex" in t:
        return "Nomex", "fabric", np.nan
    if "candle" in t:
        return "Candle wax", "candle", np.nan
    if "spherical" in t:
        return "PMMA", "sphere", np.nan
    if "rod" in t:
        inch = {"1/4": 6.35, "3/8": 9.53, "1/2": 12.7, "0.5": 12.7}
        diam = next((mm for k, mm in inch.items() if k in t), np.nan)
        color = "Black" if "black" in t or "blac" in t else "Clear"
        return f"{color} PMMA", "rod", diam
    micron = re.search(r"(\d+)\s*mic", t)
    if micron:
        return "PMMA", "film", float(micron.group(1)) / 1000
    mm = re.search(r"(\d*\.?\d+)\s*mm", t)
    thick = float(mm.group(1)) if mm else np.nan
    geometry = "film" if thick == thick and thick < 0.5 else "slab"
    return "PMMA", geometry, thick


def build_bass() -> pd.DataFrame:
    raw = pd.read_csv(RAW / "PSI-25_BASS-II_experimental_table.csv", dtype=str)
    raw.columns = [c.strip() for c in raw.columns]
    rows = []
    for _, r in raw.iterrows():
        flows = bass_flows(r["Air display"])
        outcome, detail = bass_outcome(r["Fan display"], r["Air display"])
        material, geometry, thick = bass_material(r["Fuel Sample Material"])
        if not flows:
            x = np.nan
        elif "blown off" in detail:
            x = max(flows)
        else:
            x = min(flows)
        o2_i = num(r[[c for c in raw.columns if c.startswith("Calibrated") and "initial" in c][0]])
        co2 = num(r["Final CO2 % by vol"]) - num(r["Initial CO2 % by vol"])
        co = num(r["Final CO (ppm)"]) - num(r["Initial CO (ppm)"])
        rows.append({
            "investigation": "BASS-II", "psi_id": "PSI-25", "test_id": r["Test #"].strip(),
            "material": material, "fuel_state": "solid", "geometry": geometry, "thickness_mm": thick,
            "o2_pct": o2_i, "pressure_kpa": np.nan,
            "flow_cm_s": x,
            "flow_min_cm_s": min(flows) if flows else np.nan,
            "flow_max_cm_s": max(flows) if flows else np.nan,
            "flow_direction": "", "gravity": "micro",
            "outcome": outcome, "outcome_detail": detail,
            "spread_rate_mm_s": np.nan, "burn_time_s": np.nan, "n_tests": 1,
            "co2_rise_pct": co2 if co2 == co2 and -1 < co2 < 5 else np.nan,
            "co_rise_ppm": co if co == co and -50 < co < 2000 else np.nan,
            "notes": f"Air display: {r['Air display']} | Fan display: {r['Fan display']}",
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- Saffire (PSI-98, 99, 100)

def build_saffire() -> pd.DataFrame:
    rows = []
    base = {"fuel_state": "solid", "gravity": "micro", "pressure_kpa": np.nan, "n_tests": 1,
            "co2_rise_pct": np.nan, "co_rise_ppm": np.nan, "spread_rate_mm_s": np.nan}

    # Saffire-I: two large 94 x 40.6 cm SIBAL samples, air at 20 cm/s
    for test, o2, direction, burn in [("S1", 21.6, "concurrent", 420), ("S2", 21.5, "opposed", 70)]:
        rows.append({**base, "investigation": "Saffire-I", "psi_id": "PSI-98", "test_id": test,
                     "material": "SIBAL (cotton and fiberglass)", "geometry": "fabric", "thickness_mm": np.nan,
                     "o2_pct": o2, "flow_cm_s": 20, "flow_min_cm_s": 20, "flow_max_cm_s": 20,
                     "flow_direction": direction, "outcome": "burned",
                     "outcome_detail": f"burned for {burn} s", "burn_time_s": burn,
                     "notes": "94 x 40.6 cm sample"})

    # Saffire-II: nine 29 x 5 cm samples, air at 20 cm/s
    s2 = [
        ("2-1", "Silicone", "fabric", 0.27, 21.5, "concurrent", "no_ignition", "burn length ~0 (on Earth: burned completely)", np.nan, np.nan),
        ("2-2", "Silicone", "fabric", 0.61, 22.1, "concurrent", "no_ignition", "burn length ~0 (on Earth: 7.6 cm)", np.nan, np.nan),
        ("2-3", "Silicone", "fabric", 1.03, 22.1, "concurrent", "no_ignition", "burn length ~0 (on Earth: ~0)", np.nan, np.nan),
        ("2-4", "Silicone", "fabric", 0.37, 22.1, "opposed", "no_ignition", "burn length ~0 (on Earth: burned completely)", np.nan, np.nan),
        ("2-5", "SIBAL (cotton and fiberglass)", "fabric", 0.37, 22.1, "concurrent", "burned", "29 cm burned in 145 s", 2.1, 145),
        ("2-6", "SIBAL (cotton and fiberglass)", "fabric", 0.37, 22.1, "concurrent", "burned", "29 cm burned in 115 s", 2.6, 115),
        ("2-7a", "PMMA (5 cm part)", "slab", 0.85, 22.1, "concurrent", "burned", "PMMA fully consumed in 140 s", np.nan, 140),
        ("2-7b", "Nomex (24 cm part)", "fabric", 0.37, 22.1, "concurrent", "no_ignition", "Nomex did not ignite, even heated by the PMMA", np.nan, np.nan),
        ("2-8", "PMMA", "slab", np.nan, 22.05, "concurrent", "burned", "flame anchored at the base for 600 s", np.nan, 600),
        ("2-9", "PMMA", "slab", 10.0, 21.95, "concurrent", "burned", "flame anchored at the base for 900 s", np.nan, 900),
    ]
    for test, mat, geo, thick, o2, direction, outcome, detail, rate, burn in s2:
        rows.append({**base, "investigation": "Saffire-II", "psi_id": "PSI-99", "test_id": test,
                     "material": mat, "geometry": geo, "thickness_mm": thick, "o2_pct": o2,
                     "flow_cm_s": 20, "flow_min_cm_s": 20, "flow_max_cm_s": 20, "flow_direction": direction,
                     "outcome": outcome, "outcome_detail": detail, "spread_rate_mm_s": rate,
                     "burn_time_s": burn, "notes": "29 x 5 cm sample; O2 derived from the measured CO2"})

    # Saffire-III: the PSI table gives neither the oxygen nor the outcome
    for test, direction in [("S1", "concurrent"), ("S2", "opposed")]:
        rows.append({**base, "investigation": "Saffire-III", "psi_id": "PSI-100", "test_id": test,
                     "material": "SIBAL (cotton and fiberglass)", "geometry": "fabric", "thickness_mm": np.nan,
                     "o2_pct": np.nan, "flow_cm_s": 30, "flow_min_cm_s": 30, "flow_max_cm_s": 30,
                     "flow_direction": direction, "outcome": "unknown",
                     "outcome_detail": "oxygen and outcome missing from the PSI table", "burn_time_s": np.nan,
                     "notes": "94 x 40.6 cm sample"})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- FLEX (PSI-69)

def build_flex() -> pd.DataFrame:
    raw = pd.read_csv(RAW / "PSI-69_FLEX_grouped.csv")
    end_map = {"Extinction": ("extinguished", "flame went out before the droplet was gone"),
               "Completion": ("burned", "droplet burned completely"),
               "Disruption": ("burned", "droplet burst while burning")}
    rows = []
    for _, r in raw.iterrows():
        outcome, detail = end_map[r["test_end"]]
        diluent = []
        if r["co2_pct"] > 0:
            diluent.append(f"CO2 {r['co2_pct']:g}%")
        if r["he_pct"] > 0:
            diluent.append(f"helium {r['he_pct']:g}%")
        rows.append({
            "investigation": "FLEX", "psi_id": "PSI-69", "test_id": str(r["test_numbers"]),
            "material": r["fuel"], "fuel_state": "liquid", "geometry": "droplet", "thickness_mm": np.nan,
            "o2_pct": r["o2_pct"], "pressure_kpa": r["pressure_kpa"] if r["pressure_kpa"] > 0 else np.nan,
            "flow_cm_s": 0.0, "flow_min_cm_s": 0.0, "flow_max_cm_s": 0.0, "flow_direction": "quiescent",
            "gravity": "micro", "outcome": outcome, "outcome_detail": detail,
            "spread_rate_mm_s": np.nan, "burn_time_s": np.nan, "n_tests": int(r["n_tests"]),
            "co2_rise_pct": np.nan, "co_rise_ppm": np.nan,
            "notes": ("Dilution: " + ", ".join(diluent)) if diluent else "No dilution",
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- ACME BRE (PSI-20)

def build_bre() -> pd.DataFrame:
    raw = pd.read_csv(RAW / "PSI-20_ACME-BRE_experimental_table.csv", dtype=str)
    rows = []
    for _, r in raw.iterrows():
        levels = []
        for part in str(r["Oxygen Conc (percent)"]).split(";"):
            v = num(part.replace("%", ""))
            if v == v and v > 100:      # "3400%" and "2100%": typos for 34 and 21
                v = v / 100
            if v == v:
                levels.append(v)
        ignited = int(num(r["Flames Ignited"]))
        fuel = r["Fuel Bottle"].replace(" ", "")
        fuel = {"100%C2H4": "Ethylene", "50%C2H4": "Diluted ethylene (50%)", "100%CH4": "Methane"}.get(fuel, fuel)
        for v in levels:
            rows.append({
                "investigation": "ACME BRE", "psi_id": "PSI-20",
                "test_id": f"{r['Year']}-{r['Month']}-{r['Date']}",
                "material": fuel, "fuel_state": "gas", "geometry": f"{r['Burner Size (mm)']} mm burner",
                "thickness_mm": np.nan, "o2_pct": v, "pressure_kpa": np.nan,
                "flow_cm_s": 0.0, "flow_min_cm_s": 0.0, "flow_max_cm_s": 0.0, "flow_direction": "quiescent",
                "gravity": "micro",
                "outcome": "burned" if ignited > 0 else "no_ignition",
                "outcome_detail": f"{ignited} flames ignited that day" if ignited else "no flame ignited that day",
                "spread_rate_mm_s": np.nan, "burn_time_s": np.nan, "n_tests": np.nan,
                "co2_rise_pct": np.nan, "co_rise_ppm": np.nan,
                "notes": "Pressure varied but is not given in the PSI table",
            })
    return pd.DataFrame(rows)


def main() -> None:
    df = pd.concat([build_saffire(), build_bass(), build_flex(), build_bre()], ignore_index=True)
    df = df[COLUMNS]
    df.to_csv(OUT, index=False, float_format="%.4g")
    print(f"{len(df)} rows written to {OUT.relative_to(ROOT)}")
    print(df.groupby("investigation").agg(rows=("test_id", "size"), tests=("n_tests", "sum")))
    print(df["outcome"].value_counts())


if __name__ == "__main__":
    main()
