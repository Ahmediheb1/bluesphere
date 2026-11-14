"""Loading BlueSphere's data.

experiments.csv: one NASA test per row (or a group of identical tests), with harmonized columns.
investigations.csv: one row per NASA investigation (name, PSI number, number of tests, description).

Units are always the same: oxygen in % by volume, pressure in kPa, air speed in cm/s, thickness in mm.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent  # every file sits at the root of the project

EXPERIMENT_COLUMNS = [
    "investigation",     # short name of the investigation, e.g. BASS-II
    "psi_id",            # PSI number, e.g. PSI-25
    "test_id",           # test identifier in the PSI table
    "material",          # material or fuel
    "fuel_state",        # solid, liquid or gas
    "geometry",          # sample shape
    "thickness_mm",      # thickness
    "o2_pct",            # oxygen, % by volume
    "pressure_kpa",      # pressure
    "flow_cm_s",         # air speed (0 = still air)
    "flow_direction",    # concurrent, opposed or quiescent
    "gravity",           # micro, moon, mars or earth
    "outcome",           # burned, extinguished, no_ignition or unknown
    "flow_min_cm_s",     # lowest air speed recorded during the test
    "flow_max_cm_s",     # highest air speed recorded during the test
    "outcome_detail",    # the outcome in one sentence
    "spread_rate_mm_s",  # flame spread rate
    "burn_time_s",       # burning time
    "n_tests",           # number of identical tests grouped on the row (empty = unknown)
    "co2_rise_pct",      # CO2 rise during the test (BASS-II)
    "co_rise_ppm",       # CO rise during the test (BASS-II)
    "notes",
]

NUMERIC = [
    "thickness_mm", "o2_pct", "pressure_kpa", "flow_cm_s", "flow_min_cm_s", "flow_max_cm_s",
    "spread_rate_mm_s", "burn_time_s", "n_tests", "co2_rise_pct", "co_rise_ppm",
]

PSI_URL = "https://psi.nasa.gov/physci/repo/data/investigations/{psi_id}"

# Planned Moon base (challenge statement): 30% oxygen or more, at 10.2 psi or less
MOON_BASE_O2_PCT = 30.0
MOON_BASE_PRESSURE_KPA = 70.3  # 10.2 psi
EARTH_AIR_O2_PCT = 21.0
# NASA guide (2015): flames spread best around 10 cm/s, the typical speed of spacecraft ventilation
TYPICAL_VENTILATION_CM_S = 10.0


@st.cache_data
def _read_csv(path: str, mtime: float) -> pd.DataFrame:
    # mtime is part of the cache key, so an edited file is read again
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
    """Oxygen band used by the coverage map."""
    if pd.isna(o2_pct):
        return None
    # 20.5%: a margin for normal air, written 20.9% or 21% depending on the table
    if o2_pct < EARTH_AIR_O2_PCT - 0.5:
        return "o2_low"
    if o2_pct < MOON_BASE_O2_PCT:
        return "o2_mid"
    return "o2_high"
