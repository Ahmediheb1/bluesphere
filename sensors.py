"""Live detection demo (bonus module): simulated cabin sensors and the team's detection rules.

The data is SIMULATED, and the page says so. Its timing follows what NASA measured or modeled
during the Saffire-IV and V fires in Cygnus:
- far from the fire, CO2 starts rising about 50 s after ignition, and CO rises more slowly
  (Fortenberry et al., 2021);
- at the far sensor, CO2 reached 1.4 times its starting value with SIBAL fabric and 2.8 times
  with PMMA (Brooker and Niehaus, 2022);
- oxygen barely moves: 21.7% to 21.5% during Saffire-I (Ferkul et al., 2017);
- the smoke eater did not remove CO in a noticeable way (Fortenberry et al., 2021).
Other amplitudes (CO, cabin temperature) are illustrative choices for the demo. All four readings
come from one cabin sensor away from the fire, like the far sensor in Saffire.

The team's detection rules:
1. CO2 gives the alert, CO confirms it.
2. The speed of change matters more than the value: learn the habitat's normal behavior,
   then flag changes much faster than normal.
3. Combine the four signals (temperature, O2, CO2, CO) rather than trust one.
No absolute threshold is invented: a signal is abnormal when its rate of change is many times
larger than its own normal fluctuations, learned at the start of the run.
"""

import numpy as np
import pandas as pd

STEP_S = 5            # one reading every 5 seconds
DURATION_S = 900      # 15 minutes
IGNITION_S = 120      # the fire starts at 2 minutes
LEARN_S = 90          # the normal behavior is learned over the first 90 seconds
WINDOW_S = 30         # rates are measured over 30 seconds
PERSIST = 2           # a signal must be abnormal 2 readings in a row
K_NORMAL = 5.0        # "many times its normal fluctuations"
K_CAUTIOUS = 3.5      # cautious mode (no-data zone): the alert comes earlier

SIGNALS = ["co2", "co", "o2", "temp"]

SCENARIOS = {
    # CO2 peak from Brooker and Niehaus (2022); the rest is illustrative
    "pmma": {"fire": True, "co2_peak": 2.8, "co_peak": 9.0, "temp_peak": 2.0, "o2_drop": 0.2, "vent_cut_s": 420},
    "sibal": {"fire": True, "co2_peak": 1.4, "co_peak": 4.0, "temp_peak": 1.0, "o2_drop": 0.1, "vent_cut_s": 420},
    "exercise": {"fire": False},
}


def _logistic(t: np.ndarray, start: float, rise_s: float) -> np.ndarray:
    """0 before `start`, then an S-curve that reaches about 1 after `rise_s` seconds."""
    x = (t - start - rise_s / 2) / (rise_s / 8)
    return np.where(t < start, 0.0, 1 / (1 + np.exp(-x)))


def simulate(scenario: str, seed: int = 7) -> pd.DataFrame:
    """Readings every 5 s at a cabin sensor: CO2 and CO as multiples of their starting level, O2 in %, temperature in °C."""
    p = SCENARIOS[scenario]
    rng = np.random.default_rng(seed)
    t = np.arange(0, DURATION_S + STEP_S, STEP_S, dtype=float)
    n = len(t)
    co2 = 1 + rng.normal(0, 0.004, n)
    co = 1 + rng.normal(0, 0.03, n)
    o2 = 21.0 + rng.normal(0, 0.008, n)
    temp = 22.0 + rng.normal(0, 0.06, n)

    if p["fire"]:
        # CO2 reaches the far sensor about 50 s after ignition, then rises as the cabin mixes (about 6 minutes)
        co2 += (p["co2_peak"] - 1) * _logistic(t, IGNITION_S + 50, 360)
        # CO rises later and more slowly
        co += (p["co_peak"] - 1) * _logistic(t, IGNITION_S + 110, 420)
        o2 -= p["o2_drop"] * _logistic(t, IGNITION_S + 50, 360)
        # Away from the fire, the cabin warms only a little; it cools slowly once the flame is out
        heat = _logistic(t, IGNITION_S + 60, 300)
        out = t >= p["vent_cut_s"] + 30
        cooling = np.exp(-(t - (p["vent_cut_s"] + 30)) / 400)
        temp += p["temp_peak"] * np.where(out, heat * cooling, heat)
    else:
        # A crew member exercising: CO2 creeps up slowly, nothing else moves
        co2 += 0.25 * np.clip((t - IGNITION_S) / 600, 0, 1)
        o2 -= 0.02 * np.clip((t - IGNITION_S) / 600, 0, 1)

    return pd.DataFrame({"t": t, "co2": co2, "co": co, "o2": o2, "temp": temp})


def detect(df: pd.DataFrame, cautious: bool = False) -> pd.DataFrame:
    """Add, for each reading, how abnormal each signal is and the alert level (0 normal, 1 watch, 2 fire)."""
    k = K_CAUTIOUS if cautious else K_NORMAL
    lag = WINDOW_S // STEP_S
    out = df.copy()
    learn = out["t"] <= LEARN_S
    for s in SIGNALS:
        rate = (out[s] - out[s].shift(lag)) / WINDOW_S
        if s == "o2":
            rate = -rate  # for oxygen, a drop is the warning sign
        base = rate[learn & rate.notna()]
        spread = max(float(base.std()), 1e-9)
        score = ((rate - float(base.mean())) / spread).fillna(0)
        hot = score > k
        out[f"{s}_score"] = score
        out[f"{s}_abnormal"] = hot & hot.shift(1, fill_value=False)  # 2 readings in a row
    others = out[["co2_abnormal", "o2_abnormal", "temp_abnormal"]].any(axis=1)
    fire = out["co_abnormal"] & others
    watch = out[[f"{s}_abnormal" for s in SIGNALS]].any(axis=1)
    out["level"] = np.where(fire, 2, np.where(watch, 1, 0))
    # Once confirmed, a fire stays confirmed until the crew clears it
    out["level"] = out["level"].cummax().where(out["level"].cummax() == 2, out["level"])
    return out


def first_time(det: pd.DataFrame, level: int) -> float | None:
    hits = det.loc[det["level"] >= level, "t"]
    return float(hits.iloc[0]) if len(hits) else None


def restart_checks(df: pd.DataFrame, t_now: float, scenario: str) -> list[tuple[str, bool, str]]:
    """The 'can we restart the ventilation?' checks at time t_now: (check, passed, value)."""
    p = SCENARIOS[scenario]
    now = df[df["t"] <= t_now]
    last = now.iloc[-1]
    recent = now.tail(WINDOW_S // STEP_S + 1)
    co_rising = recent["co"].iloc[-1] - recent["co"].iloc[0] > 0.05
    out_s = (p.get("vent_cut_s", 0) + 30) if p["fire"] else None
    flame_out = p["fire"] and t_now >= out_s
    return [
        ("co_normal", bool(last["co"] < 1.5 and not co_rising), f"{last['co']:.1f}"),
        ("co2_normal", bool(last["co2"] < 1.1), f"{last['co2']:.2f}"),
        ("temp_normal", bool(last["temp"] - 22.0 < 0.3), f"{last['temp'] - 22.0:+.1f}"),
        ("flame_out", bool(flame_out or not p["fire"]), ""),
    ]
