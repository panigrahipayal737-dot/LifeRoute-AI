import streamlit as st
from backend import emergency_db

st.set_page_config(page_title="Traffic Preemption Controller", page_icon="🚦", layout="wide")

st.markdown('''
<style>
    .stApp { background: radial-gradient(circle at 15% 15%, #0a1128 0%, #050814 100%) !important; color: #f8fafc !important; }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #070e24 0%, #0a1738 50%, #040918 100%) !important; border-right: 1.5px solid rgba(56, 189, 248, 0.3) !important; }
    section[data-testid="stSidebar"] a { background: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-radius: 10px !important; padding: 9px 14px !important; margin: 4px 0 !important; font-weight: 700 !important; color: #cbd5e1 !important; }
    section[data-testid="stSidebar"] a[aria-current="page"] { background: linear-gradient(90deg, rgba(2, 132, 199, 0.5), rgba(59, 130, 246, 0.5)) !important; border: 1.5px solid #38bdf8 !important; color: #ffffff !important; }
    [data-testid="stSidebarNav"] > div:first-child { display: none !important; }
</style>
''', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('''
    <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%); border: 2px solid #38bdf8; border-radius: 14px; padding: 16px 12px; text-align: center; margin-top: -30px; margin-bottom: 22px; box-shadow: 0 0 25px rgba(56, 189, 248, 0.35);">
        <div style="font-size: 32px; margin-bottom: 4px;">🚨</div>
        <div style="font-size: 21px; font-weight: 900; letter-spacing: -0.5px; background: linear-gradient(90deg, #38bdf8, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            PulseRoute AI
        </div>
        <div style="display: inline-block; background: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e; color: #4ade80; border-radius: 12px; padding: 3px 10px; font-size: 10px; font-weight: 800; margin-top: 6px;">
            ● SURAT V2X CORRIDOR ACTIVE
        </div>
        <div style="font-size: 10.5px; color: #94a3b8; font-weight: 600; margin-top: 5px;">
            108 Smart Transit Preemption Hub
        </div>
    </div>
    ''', unsafe_allow_html=True)

inc = emergency_db.get_latest_incident()
is_active = inc.get("PreemptionActive", True)

token_str = str(inc.get("Token", "#SOS-2013"))
origin_str = str(inc.get("Origin", "Majura Gate Chauraha (Central Surat)"))
hosp_str = str(inc.get("Hospital", "SMIMER Medical College & Apex ER (Umarwada)"))
fleet_str = str(inc.get("Fleet", "GJ-01-EA-108 (ALS)"))
pilot_str = str(inc.get("Pilot", "Ramesh Kumar (+91 98765 43210)"))
corridor_str = str(inc.get("Corridor", "EAST Lane")).upper()
radar_str = str(inc.get("Radar", "450m"))

status_badge = "PREEMPTION ARMED 🚨" if is_active else "STANDBY CYCLIC MODE"

header_html = (
    '<div style="background: linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border: 1.5px solid rgba(56,189,248,0.4); border-radius:14px; padding:18px 24px; display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">'
    '<div><div style="font-size: 20px; font-weight: 900; color: #38bdf8; display:flex; align-items:center; gap:8px;"><span>🚦</span> 4-WAY V2X TRAFFIC PREEMPTION CONTROLLER</div>'
    '<div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Live Intersection Preemption Synchronized With Dispatch Bus</div></div>'
    '<div style="background:rgba(34,197,94,0.2); color:#4ade80; border:1.5px solid #22c55e; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:900;">' + status_badge + '</div></div>'
)
st.markdown(header_html, unsafe_allow_html=True)

if is_active:
    corr_html = (
        '<div style="background: linear-gradient(135deg, rgba(6,78,59,0.45) 0%, rgba(15,23,42,0.85) 100%); border: 1.5px solid #10b981; border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;">'
        '<div style="font-size: 15px; font-weight: 900; color: #34d399; margin-bottom: 8px;">🚨 LIVE EMERGENCY CORRIDOR ENGAGED: ' + token_str + '</div>'
        '<div style="font-size: 13px; color: #e2e8f0; line-height: 1.8;">'
        '<div>📍 <strong>ORIGIN:</strong> <span style="color:#facc15; font-weight:800;">' + origin_str + '</span></div>'
        '<div>🎯 <strong>DESTINATION:</strong> <span style="color:#38bdf8; font-weight:800;">' + hosp_str + '</span></div>'
        '<div>🚑 <strong>AMBULANCE:</strong> ' + fleet_str + ' | <strong>DRIVER:</strong> ' + pilot_str + '</div>'
        '<div>🚦 <strong>PREEMPTION SIGNAL LOCK:</strong> <span style="color:#4ade80; font-weight:900;">' + corridor_str + ' (GREEN WAVE ACTIVE 🟢)</span> | <strong>RADAR:</strong> ' + radar_str + '</div>'
        '</div></div>'
    )
    st.markdown(corr_html, unsafe_allow_html=True)
else:
    st.info("No active emergency preemption detected. Traffic signals operating in standard cyclic rotation.")

st.markdown("### 🚦 Live 4-Way Junction Signal State Machine")

c1, c2, c3 = st.columns(3)

is_n = ("NORTH" in corridor_str) and is_active
txt_n = "🟢 FORCED GREEN WAVE (LOCKED)" if is_n else "STANDARD CYCLIC"
col_n = "#4ade80" if is_n else "#cbd5e1"
bg_n = "background: rgba(6,78,59,0.55); border: 1.5px solid #22c55e;" if is_n else "background: rgba(15,23,42,0.7); border: 1px solid rgba(255,255,255,0.08);"

is_s = ("SOUTH" in corridor_str) and is_active
txt_s = "🟢 FORCED GREEN WAVE (LOCKED)" if is_s else "STANDARD CYCLIC"
col_s = "#4ade80" if is_s else "#cbd5e1"
bg_s = "background: rgba(6,78,59,0.55); border: 1.5px solid #22c55e;" if is_s else "background: rgba(15,23,42,0.7); border: 1px solid rgba(255,255,255,0.08);"

is_e = ("EAST" in corridor_str) and is_active
txt_e = "🟢 FORCED GREEN WAVE (LOCKED)" if is_e else "STANDARD CYCLIC"
col_e = "#4ade80" if is_e else "#cbd5e1"
bg_e = "background: rgba(6,78,59,0.55); border: 1.5px solid #22c55e;" if is_e else "background: rgba(15,23,42,0.7); border: 1px solid rgba(255,255,255,0.08);"

with c1:
    st.markdown('<div style="' + bg_n + ' border-radius:12px; padding:16px; text-align:center;"><div style="font-size:11px; color:#94a3b8; font-weight:700;">JUNCTION POLE #1</div><div style="font-size:16px; font-weight:800; color:#fff; margin:6px 0;">NORTH APPROACH</div><div style="color:' + col_n + '; font-weight:800;">' + txt_n + '</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div style="' + bg_s + ' border-radius:12px; padding:16px; text-align:center;"><div style="font-size:11px; color:#94a3b8; font-weight:700;">JUNCTION POLE #2</div><div style="font-size:16px; font-weight:800; color:#fff; margin:6px 0;">SOUTH APPROACH</div><div style="color:' + col_s + '; font-weight:800;">' + txt_s + '</div></div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div style="' + bg_e + ' border-radius:12px; padding:16px; text-align:center;"><div style="font-size:11px; color:#94a3b8; font-weight:700;">JUNCTION POLE #3</div><div style="font-size:16px; font-weight:800; color:#fff; margin:6px 0;">EAST APPROACH</div><div style="color:' + col_e + '; font-weight:800;">' + txt_e + '</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
with b1:
    if st.button("🚨 Lock Green Corridor & Broadcast Signal Override", use_container_width=True, type="primary"):
        inc["PreemptionActive"] = True
        emergency_db.update_incident_status(token_str, "Active (En-Route)")
        st.success("Signal Override Locked!")
        st.rerun()
with b2:
    if st.button("🔄 Revert to Automated Cyclic Phasing", use_container_width=True):
        emergency_db.update_incident_status(token_str, "Resolved (Handed Over)")
        st.warning("Corridor cleared.")
        st.rerun()
