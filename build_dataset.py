"""Construit data/experiments.csv à partir des tableaux d'essais de PSI (data/raw/).

Lancer :  py tools/build_dataset.py

Chaque ligne du résultat est un essai, ou un groupe d'essais identiques (colonne n_tests).
Les choix de lecture des tableaux bruts sont expliqués dans data/README.md.
"""

import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "experiments.csv"

COLUMNS = [
    "investigation", "psi_id", "test_id", "material", "fuel_state", "geometry", "thickness_mm",
    "o2_pct", "pressure_kpa", "flow_cm_s", "flow_min_cm_s", "flow_max_cm_s", "flow_direction",
    "gravity", "outcome", "outcome_detail", "spread_rate_mm_s", "burn_time_s", "n_tests",
    "co2_rise_pct", "co_rise_ppm", "notes",
]


def num(value):
    """Nombre, ou NaN si la cellule n'en contient pas un (none, OR, over, >500...)."""
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return np.nan


# ---------------------------------------------------------------- BASS-II (PSI-25)

def bass_flows(air: str) -> list[float]:
    """Vitesses d'air notées dans « Air display » (cm/s, le tunnel allait jusqu'à 40 cm/s).

    On retire : les parenthèses (valeurs du potentiomètre du ventilateur), et tout ce qui
    suit le mot « pot » (lectures du potentiomètre, pas des vitesses). « <1 » devient 0,5.
    """
    if not isinstance(air, str):
        return []
    s = air.lower().replace("<1", " 0.5 ")
    inside = " ".join(re.findall(r"\(([^)]*)\)", s))
    s = re.sub(r"\([^)]*\)", " ", s)
    s = re.sub(r"\bp(?:ots?|t)\b.*$", " ", s)       # tout ce qui suit « pot », « pots » ou « pt »

    def numbers(text: str) -> list[float]:
        return [float(x) for x in re.findall(r"\d+\.?\d*|\.\d+", text)]

    values = [v for v in numbers(s) if 0 <= v <= 40]
    if not values and "pot" not in inside:
        # Quelques lignes inversent : potentiomètre dehors, vitesses entre parenthèses (ex. O13a)
        values = [v for v in numbers(inside) if 0 <= v <= 40]
    return values


def bass_outcome(fan: str, air: str) -> tuple[str, str]:
    text = f"{fan} {air}".lower()
    if "no ign" in text:
        return "no_ignition", "pas d'allumage à aucun débit"
    if "blowoff" in text:
        return "extinguished", "flamme soufflée par un air trop rapide"
    if "would not stay lit" in text:
        return "extinguished", "la flamme ne restait pas allumée"
    if re.search(r"ext|extinguished|\bout\b", text):
        return "extinguished", "flamme éteinte en réduisant l'air"
    if re.search(r"\boff\b", text):
        return "unknown", "ventilateur coupé, résultat non noté"
    return "burned", "la flamme a brûlé aux débits notés"


def bass_material(text: str) -> tuple[str, str, float]:
    """(matériau, géométrie, épaisseur ou diamètre en mm)."""
    t = text.lower()
    if "sibal" in t:
        return "SIBAL (coton et fibre de verre)", "tissu", np.nan
    if "nomex" in t:
        return "Nomex", "tissu", np.nan
    if "candle" in t:
        return "Cire de bougie", "bougie", np.nan
    if "spherical" in t:
        return "PMMA", "sphère", np.nan
    if "rod" in t:
        inch = {"1/4": 6.35, "3/8": 9.53, "1/2": 12.7, "0.5": 12.7}
        diam = next((mm for k, mm in inch.items() if k in t), np.nan)
        color = "noir" if "black" in t or "blac" in t else "transparent"
        return f"PMMA {color}", "tige", diam
    micron = re.search(r"(\d+)\s*mic", t)
    if micron:
        return "PMMA", "film", float(micron.group(1)) / 1000
    mm = re.search(r"(\d*\.?\d+)\s*mm", t)
    thick = float(mm.group(1)) if mm else np.nan
    geometry = "film" if thick == thick and thick < 0.5 else "plaque"
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
        elif "soufflée" in detail:
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
            "notes": f"Air display : {r['Air display']} | Fan display : {r['Fan display']}",
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- Saffire (PSI-98, 99, 100)

def build_saffire() -> pd.DataFrame:
    rows = []
    base = {"fuel_state": "solid", "gravity": "micro", "pressure_kpa": np.nan, "n_tests": 1,
            "co2_rise_pct": np.nan, "co_rise_ppm": np.nan, "spread_rate_mm_s": np.nan}

    # Saffire-I : deux grands échantillons de SIBAL de 94 x 40,6 cm, air à 20 cm/s
    for test, o2, direction, burn in [("S1", 21.6, "concurrent", 420), ("S2", 21.5, "opposed", 70)]:
        rows.append({**base, "investigation": "Saffire-I", "psi_id": "PSI-98", "test_id": test,
                     "material": "SIBAL (coton et fibre de verre)", "geometry": "tissu", "thickness_mm": np.nan,
                     "o2_pct": o2, "flow_cm_s": 20, "flow_min_cm_s": 20, "flow_max_cm_s": 20,
                     "flow_direction": direction, "outcome": "burned",
                     "outcome_detail": f"a brûlé pendant {burn} s", "burn_time_s": burn,
                     "notes": "Échantillon de 94 x 40,6 cm"})

    # Saffire-II : neuf échantillons de 29 x 5 cm, air à 20 cm/s
    s2 = [
        ("2-1", "Silicone", "tissu", 0.27, 21.5, "concurrent", "no_ignition", "longueur brûlée ~0 (sur Terre : brûlé en entier)", np.nan, np.nan),
        ("2-2", "Silicone", "tissu", 0.61, 22.1, "concurrent", "no_ignition", "longueur brûlée ~0 (sur Terre : 7,6 cm)", np.nan, np.nan),
        ("2-3", "Silicone", "tissu", 1.03, 22.1, "concurrent", "no_ignition", "longueur brûlée ~0 (sur Terre : ~0)", np.nan, np.nan),
        ("2-4", "Silicone", "tissu", 0.37, 22.1, "opposed", "no_ignition", "longueur brûlée ~0 (sur Terre : brûlé en entier)", np.nan, np.nan),
        ("2-5", "SIBAL (coton et fibre de verre)", "tissu", 0.37, 22.1, "concurrent", "burned", "29 cm brûlés en 145 s", 2.1, 145),
        ("2-6", "SIBAL (coton et fibre de verre)", "tissu", 0.37, 22.1, "concurrent", "burned", "29 cm brûlés en 115 s", 2.6, 115),
        ("2-7a", "PMMA (partie de 5 cm)", "plaque", 0.85, 22.1, "concurrent", "burned", "PMMA entièrement consumé en 140 s", np.nan, 140),
        ("2-7b", "Nomex (partie de 24 cm)", "tissu", 0.37, 22.1, "concurrent", "no_ignition", "Nomex non allumé, même chauffé par le PMMA", np.nan, np.nan),
        ("2-8", "PMMA", "plaque", np.nan, 22.05, "concurrent", "burned", "flamme ancrée à la base pendant 600 s", np.nan, 600),
        ("2-9", "PMMA", "plaque", 10.0, 21.95, "concurrent", "burned", "flamme ancrée à la base pendant 900 s", np.nan, 900),
    ]
    for test, mat, geo, thick, o2, direction, outcome, detail, rate, burn in s2:
        rows.append({**base, "investigation": "Saffire-II", "psi_id": "PSI-99", "test_id": test,
                     "material": mat, "geometry": geo, "thickness_mm": thick, "o2_pct": o2,
                     "flow_cm_s": 20, "flow_min_cm_s": 20, "flow_max_cm_s": 20, "flow_direction": direction,
                     "outcome": outcome, "outcome_detail": detail, "spread_rate_mm_s": rate,
                     "burn_time_s": burn, "notes": "Échantillon de 29 x 5 cm ; O2 déduit du CO2 mesuré"})

    # Saffire-III : le tableau de PSI ne donne ni l'oxygène ni le résultat
    for test, direction in [("S1", "concurrent"), ("S2", "opposed")]:
        rows.append({**base, "investigation": "Saffire-III", "psi_id": "PSI-100", "test_id": test,
                     "material": "SIBAL (coton et fibre de verre)", "geometry": "tissu", "thickness_mm": np.nan,
                     "o2_pct": np.nan, "flow_cm_s": 30, "flow_min_cm_s": 30, "flow_max_cm_s": 30,
                     "flow_direction": direction, "outcome": "unknown",
                     "outcome_detail": "oxygène et résultat absents du tableau de PSI", "burn_time_s": np.nan,
                     "notes": "Échantillon de 94 x 40,6 cm"})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- FLEX (PSI-69)

def build_flex() -> pd.DataFrame:
    raw = pd.read_csv(RAW / "PSI-69_FLEX_grouped.csv")
    end_map = {"Extinction": ("extinguished", "flamme éteinte avant la fin de la goutte"),
               "Completion": ("burned", "goutte entièrement brûlée"),
               "Disruption": ("burned", "goutte éclatée en brûlant")}
    rows = []
    for _, r in raw.iterrows():
        outcome, detail = end_map[r["test_end"]]
        diluent = []
        if r["co2_pct"] > 0:
            diluent.append(f"CO2 {r['co2_pct']:g} %")
        if r["he_pct"] > 0:
            diluent.append(f"hélium {r['he_pct']:g} %")
        fuel = {"Methanol": "Méthanol", "Heptane": "Heptane"}.get(r["fuel"], r["fuel"])
        rows.append({
            "investigation": "FLEX", "psi_id": "PSI-69", "test_id": str(r["test_numbers"]),
            "material": fuel, "fuel_state": "liquid", "geometry": "goutte", "thickness_mm": np.nan,
            "o2_pct": r["o2_pct"], "pressure_kpa": r["pressure_kpa"] if r["pressure_kpa"] > 0 else np.nan,
            "flow_cm_s": 0.0, "flow_min_cm_s": 0.0, "flow_max_cm_s": 0.0, "flow_direction": "quiescent",
            "gravity": "micro", "outcome": outcome, "outcome_detail": detail,
            "spread_rate_mm_s": np.nan, "burn_time_s": np.nan, "n_tests": int(r["n_tests"]),
            "co2_rise_pct": np.nan, "co_rise_ppm": np.nan,
            "notes": ("Dilution : " + ", ".join(diluent)) if diluent else "Sans dilution",
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
            if v == v and v > 100:      # « 3400% » et « 2100% » : fautes de frappe pour 34 et 21
                v = v / 100
            if v == v:
                levels.append(v)
        ignited = int(num(r["Flames Ignited"]))
        fuel = r["Fuel Bottle"].replace(" ", "")
        fuel = {"100%C2H4": "Éthylène", "50%C2H4": "Éthylène dilué (50 %)", "100%CH4": "Méthane"}.get(fuel, fuel)
        for v in levels:
            rows.append({
                "investigation": "ACME BRE", "psi_id": "PSI-20",
                "test_id": f"{r['Year']}-{r['Month']}-{r['Date']}",
                "material": fuel, "fuel_state": "gas", "geometry": f"brûleur de {r['Burner Size (mm)']} mm",
                "thickness_mm": np.nan, "o2_pct": v, "pressure_kpa": np.nan,
                "flow_cm_s": 0.0, "flow_min_cm_s": 0.0, "flow_max_cm_s": 0.0, "flow_direction": "quiescent",
                "gravity": "micro",
                "outcome": "burned" if ignited > 0 else "no_ignition",
                "outcome_detail": f"{ignited} flammes allumées ce jour-là" if ignited else "aucune flamme allumée ce jour-là",
                "spread_rate_mm_s": np.nan, "burn_time_s": np.nan, "n_tests": np.nan,
                "co2_rise_pct": np.nan, "co_rise_ppm": np.nan,
                "notes": "Pression variée mais non indiquée dans le tableau de PSI",
            })
    return pd.DataFrame(rows)


def main() -> None:
    df = pd.concat([build_saffire(), build_bass(), build_flex(), build_bre()], ignore_index=True)
    df = df[COLUMNS]
    df.to_csv(OUT, index=False, float_format="%.4g")
    print(f"{len(df)} lignes écrites dans {OUT.relative_to(ROOT)}")
    print(df.groupby("investigation").agg(lignes=("test_id", "size"), essais=("n_tests", "sum")))
    print(df["outcome"].value_counts())


if __name__ == "__main__":
    main()
