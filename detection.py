"""Live fire detection (bonus): simulated cabin sensors and the team's detection rules."""

import streamlit as st

import charts
import sensors
from style import COLORS, page_header, section
from texts import t

STATUS_COLORS = {0: "#4CC38A", 1: COLORS["ember"], 2: "#F0605D"}


def clock(seconds: float) -> str:
    return f"{int(seconds) // 60}:{int(seconds) % 60:02d}"


page_header(t("det_title"), t("det_lead"))
st.warning(t("det_simulated"), icon=":material/science:")

left, right = st.columns([3, 2], vertical_alignment="bottom")
with left:
    scenario = st.pills(t("det_scenario"), list(sensors.SCENARIOS), default="pmma",
                        format_func=lambda k: t(f"det_sc_{k}"), key="det_scenario") or "pmma"
with right:
    cautious = st.toggle(t("det_cautious"), value=False, help=t("det_cautious_help"), key="det_cautious")
t_now = st.select_slider(t("det_time"), options=list(range(0, sensors.DURATION_S + 1, sensors.STEP_S)),
                         value=480, format_func=clock, key="det_time")

data = sensors.simulate(scenario)
det = sensors.detect(data, cautious)
row = det[det["t"] <= t_now].iloc[-1]
level = int(row["level"])

# The alert, and why
flagged = [s for s in sensors.SIGNALS if row[f"{s}_abnormal"]]
if level == 0:
    why = t("det_why_0")
else:
    reasons = [t("det_why_signal", name=t(f"det_sig_{s}"), x=f"{row[f'{s}_score']:.0f}") for s in flagged]
    why = t("det_why_prefix") + "; ".join(reasons) + ". " + t("det_why_fire" if level == 2 else "det_why_watch")
color = STATUS_COLORS[level]
st.markdown(
    f"<div style='border:1px solid {color}; border-radius:10px; padding:1rem 1.2rem; margin:0.6rem 0 1rem 0;'>"
    f"<div style='font-size:1.6rem; font-weight:650; font-stretch:112%; color:{color};'>{t(f'det_status_{level}')}</div>"
    f"<div style='color:{COLORS['ink2']}; margin-top:0.35rem; line-height:1.55;'>{why}</div></div>",
    unsafe_allow_html=True,
)

# When the alerts came
first_watch, first_fire = sensors.first_time(det, 1), sensors.first_time(det, 2)
fire = sensors.SCENARIOS[scenario]["fire"]


def when(value):
    if value is None:
        return t("det_none") if not fire else t("det_not_yet"), None
    shown = clock(value) if value <= t_now else t("det_not_yet")
    delta = t("det_after_ignition", s=int(value - sensors.IGNITION_S)) if fire and value <= t_now else None
    return shown, delta


m1, m2, m3 = st.columns(3)
m1.metric(t("det_ignition"), clock(sensors.IGNITION_S) if fire else t("det_none"))
v, d = when(first_watch)
m2.metric(t("det_first_alert"), v, d, delta_color="off")
v, d = when(first_fire)
m3.metric(t("det_confirmed"), v, d, delta_color="off")

# The four signals
events = []
if fire:
    events = [(sensors.IGNITION_S, t("det_ev_ignition")), (sensors.SCENARIOS[scenario]["vent_cut_s"], t("det_ev_cut"))]
grid = st.columns(2, gap="medium")
for i, s in enumerate(["co2", "co", "o2", "temp"]):
    with grid[i % 2]:
        st.altair_chart(charts.signal_chart(det, s, t_now, events, t(f"det_y_{s}"), sensors.DURATION_S), width="stretch")
st.caption(t("det_chart_caption"))

# Can we restart the ventilation?
section(t("det_restart_title"))
if not fire:
    st.markdown(t("det_restart_no_fire"))
else:
    checks = sensors.restart_checks(data, t_now, scenario)
    flame_out = dict((k, ok) for k, ok, _ in checks)["flame_out"]
    if not flame_out:
        st.markdown(f"**{t('det_restart_no')}**: {t('det_restart_wait')}")
    else:
        ok_all = all(ok for _, ok, _ in checks)
        st.markdown(f"**{t('det_restart_slow') if ok_all else t('det_restart_no')}**")
        for key, ok, value in checks:
            st.markdown(f"{'✅' if ok else '❌'} {t(f'det_check_{key}', v=value)}")
    st.caption(t("det_restart_note"))
    if st.button(t("nav_after")):
        st.switch_page("after.py")

with st.expander(t("det_method_title")):
    st.markdown(t("det_method_body"))
