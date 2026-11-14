"""Score de risque et classement des essais de la NASA selon l'environnement.

La pondération vient de l'équipe BlueSphere (version 1) :
oxygène 30 %, matériau 25 %, ventilation 25 %, épaisseur 10 %, pression 10 %.

Chaque facteur est une valeur de 0 (peu de risque) à 1 (risque maximal).
Le score est la moyenne pondérée, sur 100. C'est un indice relatif pour comparer
des situations, pas une probabilité d'incendie, et pas une certification.

La gravité ne change pas le score : elle change la confiance, parce qu'aucun essai
de PSI n'a été fait en gravité lunaire ou martienne.
"""

import math

import pandas as pd

EARTH_PRESSURE_KPA = 101.3
KPA_PER_PSI = 6.894757

# Poids par défaut (en %), dans l'ordre d'affichage
FACTORS = ["o2", "material", "ventilation", "thickness", "pressure"]
DEFAULT_WEIGHTS = {"o2": 30, "material": 25, "ventilation": 25, "thickness": 10, "pressure": 10}

# Bornes du facteur oxygène : 0 au plus bas O2 où un solide a brûlé dans nos essais (14,2 %, BASS-II),
# 1 à partir de 35 % (au-delà de l'atmosphère d'exploration de la NASA, 34 %).
O2_LOW_PCT = 14.0
O2_HIGH_PCT = 35.0

# Ventilation : courbe en cloche, sommet vers 10 cm/s (guide de la NASA, 2015).
VENT_PEAK_CM_S = 10.0
VENT_FLOOR = 0.3   # air immobile : le feu faiblit, mais « il s'éteint tout seul » est une idée fausse
VENT_WIDTH = 0.35  # largeur de la cloche, en décades (échelle logarithmique)

# Matériaux testés dans nos essais solides, avec une valeur d'expert (version 1)
MATERIALS = {
    "sibal": 1.0,     # tissu coton et fibre de verre : a brûlé dans presque tous les essais
    "pmma": 0.8,      # plastique acrylique : brûle, et peut se rallumer (Saffire-IV)
    "nomex": 0.5,     # résultats partagés : pas d'allumage dans Saffire-II
    "silicone": 0.2,  # aucun allumage en microgravité dans Saffire-II, alors qu'il brûle sur Terre
}
DEFAULT_THICKNESS_MM = {"sibal": 0.37, "pmma": 6.35, "nomex": 0.37, "silicone": 0.37}
THICKNESS_CHOICES_MM = [0.1, 0.25, 0.37, 0.5, 1.0, 2.0, 6.35, 10.0, 12.7]

# Environnements (le rover a la même atmosphère que la base lunaire, selon l'énoncé du défi)
ENVIRONMENTS = {
    "iss": {"o2": 21.0, "pressure_kpa": 101.3, "flow": 10.0, "gravity": "micro"},
    "moon_base": {"o2": 30.0, "pressure_kpa": 70.3, "flow": 10.0, "gravity": "moon"},
    "moon_rover": {"o2": 30.0, "pressure_kpa": 70.3, "flow": 10.0, "gravity": "moon"},
    "mars_ship": {"o2": 34.0, "pressure_kpa": 56.5, "flow": 10.0, "gravity": "micro"},
}

# Mode prudent : marge ajoutée au score quand la confiance est faible
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
    """Plus le matériau est mince, plus il brûle facilement : 1 à 0,1 mm, 0,2 à 10 mm et plus."""
    return _clamp(1 - 0.8 * math.log10(max(thickness_mm, 0.01) / 0.1) / 2, 0.2, 1.0)


def f_pressure(pressure_kpa: float) -> float:
    """À oxygène égal, une pression plus basse donne un peu moins de molécules d'oxygène."""
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
    """Score sur 100, et la part de chaque facteur (en points) pour le graphique."""
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
    """Classe les essais solides de la NASA du plus proche au plus éloigné de l'environnement choisi.

    La proximité est une moyenne géométrique pondérée (mêmes poids que le score) :
    un seul grand écart, par exemple 8 points d'oxygène, suffit à éloigner un essai.
    La pression manque dans les tableaux de BASS-II et de Saffire : on prend celle de la Station (101,3 kPa).
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
    """Niveau de confiance et sa raison (clé de texte)."""
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
