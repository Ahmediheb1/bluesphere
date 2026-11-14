"""Chargement des données de BlueSphere.

experiments.csv : un essai par ligne, avec les colonnes harmonisées ci-dessous.
investigations.csv : une ligne par expérience de la NASA (nom, numéro PSI, lien).

Les unités sont toujours les mêmes : oxygène en % du volume, pression en kPa,
vitesse de l'air en cm/s, épaisseur en mm.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent  # tous les fichiers sont à la racine du projet

EXPERIMENT_COLUMNS = [
    "investigation",     # nom court de l'expérience, ex. BASS-II
    "psi_id",            # numéro PSI, ex. PSI-25
    "test_id",           # identifiant de l'essai dans le tableau de PSI
    "material",          # matériau ou combustible
    "fuel_state",        # solid, liquid ou gas
    "geometry",          # forme de l'échantillon
    "thickness_mm",      # épaisseur
    "o2_pct",            # oxygène, % du volume
    "pressure_kpa",      # pression
    "flow_cm_s",         # vitesse de l'air (0 = air immobile)
    "flow_direction",    # concurrent, opposed ou quiescent
    "gravity",           # micro, moon, mars ou earth
    "outcome",           # burned, extinguished, no_ignition ou unknown
    "flow_min_cm_s",     # plus faible vitesse d'air notée pendant l'essai
    "flow_max_cm_s",     # plus forte vitesse d'air notée pendant l'essai
    "outcome_detail",    # le résultat en une phrase
    "spread_rate_mm_s",  # vitesse de propagation de la flamme
    "burn_time_s",       # durée de combustion
    "n_tests",           # nombre d'essais identiques regroupés sur la ligne (vide = inconnu)
    "co2_rise_pct",      # hausse du CO2 pendant l'essai (BASS-II)
    "co_rise_ppm",       # hausse du CO pendant l'essai (BASS-II)
    "notes",
]

NUMERIC = [
    "thickness_mm", "o2_pct", "pressure_kpa", "flow_cm_s", "flow_min_cm_s", "flow_max_cm_s",
    "spread_rate_mm_s", "burn_time_s", "n_tests", "co2_rise_pct", "co_rise_ppm",
]

PSI_URL = "https://psi.nasa.gov/physci/repo/data/investigations/{psi_id}"

# Base lunaire prévue (énoncé du défi) : 30 % d'oxygène ou plus, à 10,2 psi ou moins
MOON_BASE_O2_PCT = 30.0
MOON_BASE_PRESSURE_KPA = 70.3  # 10,2 psi
EARTH_AIR_O2_PCT = 21.0
# Guide NASA 2015 : minimum de la limite d'inflammabilité vers 10 cm/s,
# la vitesse typique de la ventilation d'un vaisseau
TYPICAL_VENTILATION_CM_S = 10.0


@st.cache_data
def _read_csv(path: str, mtime: float) -> pd.DataFrame:
    # mtime fait partie de la clé du cache : un fichier modifié est relu
    return pd.read_csv(path)


def _load(name: str) -> pd.DataFrame:
    path = DATA_DIR / name
    if not path.exists():
        return pd.DataFrame()
    return _read_csv(str(path), path.stat().st_mtime).copy()


def load_experiments() -> pd.DataFrame:
    df = _load("experiments.csv")
    for col in EXPERIMENT_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    for col in NUMERIC:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["gravity"] = df["gravity"].fillna("micro")
    df["outcome"] = df["outcome"].fillna("unknown")
    df["burned"] = df["outcome"].eq("burned")
    df["source_url"] = df["psi_id"].map(
        lambda p: PSI_URL.format(psi_id=p) if isinstance(p, str) else None
    )
    return df


def load_investigations() -> pd.DataFrame:
    return _load("investigations.csv")


def o2_band(o2_pct: float) -> str | None:
    """Bande d'oxygène utilisée par la carte des zones sans données."""
    if pd.isna(o2_pct):
        return None
    # 20,5 % : marge pour l'air normal, noté 20,9 % ou 21 % selon les tableaux
    if o2_pct < EARTH_AIR_O2_PCT - 0.5:
        return "o2_low"
    if o2_pct < MOON_BASE_O2_PCT:
        return "o2_mid"
    return "o2_high"
