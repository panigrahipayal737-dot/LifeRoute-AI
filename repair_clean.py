import os
import glob
import py_compile

print(">>> STARTING ZERO-ERROR CLEAN REWRITE...")

os.makedirs("pages", exist_ok=True)
os.makedirs("backend", exist_ok=True)

# 1. TRAFFIC CONTROL PAGE (pages/1_🚦_Traffic_Control.py)
traffic_py = """import streamlit as st
from backend import emergency_db

st.set_page_config(page_title="Traffic Preemption Controller", page_icon="🚦", layout="wide")

st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0a1128 0%, #050814 100%) !important;
        color: #f8fafc !important;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070e24 0%, #0a1738 50%, #040918 100%) !important;
        border-right: 1.5px solid rgba(56, 189, 248, 0.3) !important;
    }
    section[data-testid="stSidebar"] a {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 9px 14px !important;
        margin: 4px 0 !important;
        font-weight: 700 !important;
        color: #cbd5e1 !important;
    }
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background: linear-gradient(90deg, rgba(2, 132, 199, 0.5), rgba(59, 130, 246, 0.5)) !important;
        border: 1.5px solid #38bdf8 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebarNav"] > div:first-child {
        display: none !important;
    }
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

st.markdown(f'''
<div style="background: linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border: 1.5px solid rgba(56,189,248,0.4); border-radius:14px; padding:18px 24px; display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
    <div>
        <div style="font-size: 20px; font-weight: 900; color: #38bdf8; display:flex; align-items:center; gap:8px;">
            <span>🚦</span> 4-WAY V2X TRAFFIC PREEMPTION CONTROLLER
        </div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Live Intersection Preemption Synchronized With Dispatch Bus</div>
    </div>
    <div style="background:rgba(34,197,94,0.2); color:#4ade80; border:1.5px solid #22c55e; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:900;">
        {status_badge}
    </div>
</div>
''', unsafe_allow_html=True)

if is_active:
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, rgba(6,78,59,0.45) 0%, rgba(15,23,42,0.85) 100%); border: 1.5px solid #10b981; border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;">
        <div style="font-size: 15px; font-weight: 900; color: #34d399; margin-bottom: 8px;">
            🚨 LIVE EMERGENCY CORRIDOR ENGAGED: {token_str}
        </div>
        <div style="font-size: 13px; color: #e2e8f0; line-height: 1.8;">
            <div>📍 <strong>ORIGIN (KAHAN SE NIKLI):</strong> <span style="color:#facc15; font-weight:800;">{origin_str}</span></div>
            <div>🎯 <strong>DESTINATION (KAHAN JAYEGI):</strong> <span style="color:#38bdf8; font-weight:800;">{hosp_str}</span></div>
            <div>🚑 <strong>AMBULANCE:</strong> {fleet_str} | <strong>DRIVER:</strong> {pilot_str}</div>
            <div>🚦 <strong>PREEMPTION SIGNAL LOCK:</strong> <span style="color:#4ade80; font-weight:900;">{corridor_str} (GREEN WAVE ACTIVE 🟢)</span> | <strong>RADAR:</strong> {radar_str}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
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
    st.markdown(f'''<div style="{bg_n} border-radius:12px; padding:16px; text-align:center;"><div style="font-size:11px; color:#94a3b8; font-weight:700;">JUNCTION POLE #1</div><div style="font-size:16px; font-weight:800; color:#fff; margin:6px 0;">NORTH APPROACH</div><div style="color:{col_n}; font-weight:800;">{txt_n}</div></div>''', unsafe_allow_html=True)

with c2:
    st.markdown(f'''<div style="{bg_s} border-radius:12px; padding:16px; text-align:center;"><div style="font-size:11px; color:#94a3b8; font-weight:700;">JUNCTION POLE #2</div><div style="font-size:16px; font-weight:800; color:#fff; margin:6px 0;">SOUTH APPROACH</div><div style="color:{col_s}; font-weight:800;">{txt_s}</div></div>''', unsafe_allow_html=True)

with c3:
    st.markdown(f'''<div style="{bg_e} border-radius:12px; padding:16px; text-align:center;"><div style="font-size:11px; color:#94a3b8; font-weight:700;">JUNCTION POLE #3</div><div style="font-size:16px; font-weight:800; color:#fff; margin:6px 0;">EAST APPROACH</div><div style="color:{col_e}; font-weight:800;">{txt_e}</div></div>''', unsafe_allow_html=True)

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
"""

# 2. POLICE CAD ROOM (pages/3_👮_Police_Control_Room.py)
police_py = """import streamlit as st
from backend import emergency_db

st.set_page_config(page_title="Police CAD Room", page_icon="👮", layout="wide")

st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0a1128 0%, #050814 100%) !important;
        color: #f8fafc !important;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070e24 0%, #0a1738 50%, #040918 100%) !important;
        border-right: 1.5px solid rgba(56, 189, 248, 0.3) !important;
    }
    section[data-testid="stSidebar"] a {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 9px 14px !important;
        margin: 4px 0 !important;
        font-weight: 700 !important;
        color: #cbd5e1 !important;
    }
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background: linear-gradient(90deg, rgba(2, 132, 199, 0.5), rgba(59, 130, 246, 0.5)) !important;
        border: 1.5px solid #38bdf8 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebarNav"] > div:first-child {
        display: none !important;
    }
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
eta_str = str(inc.get("ETA", "3.7 mins"))
radar_str = str(inc.get("Radar", "450m"))

st.markdown(f'''
<div style="background: linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border: 1.5px solid rgba(56,189,248,0.4); border-radius:14px; padding:18px 24px; display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
    <div>
        <div style="font-size: 20px; font-weight: 900; color: #38bdf8; display:flex; align-items:center; gap:8px;">
            <span>👮</span> SURAT TRAFFIC POLICE V2X ENFORCEMENT & CAD ROOM
        </div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Live Corridor Preemption Tracking & Obstruction Surveillance</div>
    </div>
    <div style="background:rgba(225,29,72,0.2); color:#fda4af; border:1.5px solid #f43f5e; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:900;">
        POLICE CAD DESK
    </div>
</div>
''', unsafe_allow_html=True)

if is_active:
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, rgba(15,23,42,0.92) 0%, rgba(2,132,199,0.25) 100%); border: 1.5px solid #0284c7; border-radius: 12px; padding: 18px 22px; margin-bottom: 20px;">
        <div style="font-size: 16px; font-weight: 900; color: #38bdf8; margin-bottom: 12px;">
            🚓 ACTIVE V2X POLICE ESCORT: {token_str}
        </div>
        <div style="font-size: 13.5px; color: #e2e8f0; line-height: 2.0;">
            <div>📍 <strong>DISPATCH ORIGIN (KAHAN SE NIKLI):</strong> <span style="color:#facc15; font-weight:800;">{origin_str}</span></div>
            <div>🎯 <strong>TARGET DESTINATION (KAHAN JAYEGI):</strong> <span style="color:#38bdf8; font-weight:800;">{hosp_str}</span></div>
            <div>🚑 <strong>FLEET UNIT:</strong> {fleet_str} | <strong>PILOT:</strong> {pilot_str}</div>
            <div>🚦 <strong>CLEARED GREEN LANE:</strong> <span style="color:#4ade80; font-weight:800;">{corridor_str} (PREEMPTION ACTIVE 🟢)</span></div>
            <div>⏱️ <strong>ESTIMATED TIME TO ARRIVAL (ETA):</strong> {eta_str} | <strong>RADAR RANGE:</strong> {radar_str}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.info("All Surat junction corridors operating normally. No active emergency preemption requests.")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🚔 Interceptor Dispatch Status")
    st.success(f"Patrol Car assigned to {corridor_str} for clearing transit obstacles.")
with col2:
    st.markdown("#### 🛑 Manual Override")
    if st.button("Mark Route Cleared / Deactivate Police Escort", use_container_width=True):
        emergency_db.update_incident_status(token_str, "Resolved (Handed Over)")
        st.success("Escort deactivated.")
        st.rerun()
"""

# 3. CITIZEN ALERTS / BROADCAST PORTAL
citizen_py = """import streamlit as st
from backend import emergency_db

st.set_page_config(page_title="Citizen Broadcast Portal", page_icon="📢", layout="wide")

st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0a1128 0%, #050814 100%) !important;
        color: #f8fafc !important;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070e24 0%, #0a1738 50%, #040918 100%) !important;
        border-right: 1.5px solid rgba(56, 189, 248, 0.3) !important;
    }
    section[data-testid="stSidebar"] a {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 9px 14px !important;
        margin: 4px 0 !important;
        font-weight: 700 !important;
        color: #cbd5e1 !important;
    }
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background: linear-gradient(90deg, rgba(2, 132, 199, 0.5), rgba(59, 130, 246, 0.5)) !important;
        border: 1.5px solid #38bdf8 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebarNav"] > div:first-child {
        display: none !important;
    }
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
corridor_str = str(inc.get("Corridor", "EAST Lane")).upper()
eta_str = str(inc.get("ETA", "3.7 mins"))
fleet_str = str(inc.get("Fleet", "GJ-01-EA-108 (ALS)"))

st.markdown(f'''
<div style="background: linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border: 1.5px solid rgba(245,158,11,0.4); border-radius:14px; padding:18px 24px; display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
    <div>
        <div style="font-size: 20px; font-weight: 900; color: #f59e0b; display:flex; align-items:center; gap:8px;">
            <span>📢</span> SURAT CITIZEN EMERGENCY BROADCAST PORTAL
        </div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Public Advisory & Emergency Vehicle Right-Of-Way Notices</div>
    </div>
    <div style="background:rgba(245,158,11,0.2); color:#fbbf24; border:1.5px solid #f59e0b; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:900;">
        PUBLIC BROADCAST
    </div>
</div>
''', unsafe_allow_html=True)

if is_active:
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, rgba(225,29,72,0.25) 0%, rgba(15,23,42,0.85) 100%); border: 1.5px solid #f43f5e; border-radius: 12px; padding: 16px 20px; margin-bottom: 20px;">
        <div style="font-size: 15px; font-weight: 900; color: #fda4af;">🚨 URGENT: EMERGENCY AMBULANCE TRANSIT IN PROGRESS ({token_str})</div>
        <div style="font-size: 13px; color: #e2e8f0; margin-top: 6px; line-height: 1.8;">
            Priority green wave corridor active between <strong>{origin_str}</strong> and <strong>{hosp_str}</strong>.<br>
            Citizens on <strong>{corridor_str}</strong> are requested to keep left lane clear for Ambulance ({fleet_str}). ETA: ~{eta_str}.
        </div>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.success("Standard City Traffic Phase: No active emergency corridor disruptions in Surat.")
"""

# 4. HOSPITAL ADMIN DESK (Password Protected)
hosp_py = """import streamlit as st
import pandas as pd
from backend import emergency_db

st.set_page_config(page_title="Hospital Emergency & Admin Command", page_icon="🏥", layout="wide")

st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0a1128 0%, #050814 100%) !important;
        color: #f8fafc !important;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070e24 0%, #0a1738 50%, #040918 100%) !important;
        border-right: 1.5px solid rgba(56, 189, 248, 0.3) !important;
    }
    section[data-testid="stSidebar"] a {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 9px 14px !important;
        margin: 4px 0 !important;
        font-weight: 700 !important;
        color: #cbd5e1 !important;
    }
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background: linear-gradient(90deg, rgba(2, 132, 199, 0.5), rgba(59, 130, 246, 0.5)) !important;
        border: 1.5px solid #38bdf8 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebarNav"] > div:first-child {
        display: none !important;
    }
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

if "hospital_admin_logged_in" not in st.session_state:
    st.session_state["hospital_admin_logged_in"] = False

if not st.session_state["hospital_admin_logged_in"]:
    st.markdown('''
    <div style="background: linear-gradient(135deg, rgba(15,23,42,0.92) 0%, rgba(2,132,199,0.2) 100%); border: 1.5px solid #38bdf8; border-radius: 14px; padding: 26px; max-width: 520px; margin: 50px auto 20px auto; text-align: center; box-shadow: 0 0 30px rgba(56,189,248,0.25);">
        <div style="font-size: 34px; margin-bottom: 8px;">🔒</div>
        <div style="font-size: 19px; font-weight: 900; color: #38bdf8; margin-bottom: 6px;">HOSPITAL ADMIN PORTAL LOCKED</div>
        <div style="font-size: 12px; color: #94a3b8;">Restricted Area: Only Authorized Chief Medical Officers & ER Admins Allowed</div>
    </div>
    ''', unsafe_allow_html=True)

    col_a, col_mid, col_b = st.columns([1, 1.4, 1])
    with col_mid:
        entered_pass = st.text_input("Enter Hospital Admin Access Key:", type="password", key="hosp_admin_pwd")
        c_btn1, c_btn2 = st.columns([1.2, 1])
        with c_btn1:
            if st.button("🔓 Authenticate & Unlock Desk", use_container_width=True, type="primary"):
                if entered_pass == "admin108":
                    st.session_state["hospital_admin_logged_in"] = True
                    st.success("Access Granted!")
                    st.rerun()
                else:
                    st.error("❌ Invalid Access Key!")
        with c_btn2:
            st.caption("Default Key: `admin108`")
    st.stop()

col_head_l, col_head_r = st.columns([5, 1])
with col_head_r:
    if st.button("🔒 Logout Admin", use_container_width=True):
        st.session_state["hospital_admin_logged_in"] = False
        st.rerun()

records = emergency_db.load_db()
latest = records[0]

st.markdown('''
<div style="background: linear-gradient(135deg, rgba(14,165,233,0.15) 0%, rgba(99,102,241,0.2) 100%); border: 1.5px solid rgba(56,189,248,0.4); border-radius: 14px; padding: 18px 24px; display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
    <div>
        <div style="font-size: 20px; font-weight: 900; color: #f8fafc; display:flex; align-items:center; gap:8px;">
            <span>📄</span> HOSPITAL EMERGENCY INTAKE & CLINICAL HANDOVER DESK
        </div>
        <div style="font-size: 11.5px; color: #94a3b8; margin-top: 4px;">Real-Time Patient Telemetry • 1-Click Handover Sheet • ICU Bed & Cath-Lab Staging</div>
    </div>
    <div style="background: linear-gradient(135deg, rgba(244,63,94,0.25), rgba(225,29,72,0.4)); color:#fda4af; border:1.5px solid #f43f5e; padding:6px 14px; border-radius:20px; font-size:11px; font-weight:900;">
        ICU TRAUMA BAY ONLINE
    </div>
</div>
''', unsafe_allow_html=True)

tab_hospital, tab_admin, tab_family = st.tabs([
    "🏥 Hospital ER Command & Bed Reservation",
    "📊 Incident Database & Audit Records",
    "📲 Family Clinical Handover & WhatsApp Dispatch"
])

with tab_hospital:
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, rgba(6,78,59,0.45) 0%, rgba(15,23,42,0.85) 100%); border: 1.5px solid #059669; border-radius: 8px; padding: 12px 18px; color: #34d399; font-weight: 700; font-size: 13px; margin-bottom: 18px;">
        🚨 INCOMING AMBULANCE PRE-ALERT: {latest.get("Fleet", "GJ-01-EA-108 (ALS)")} (ETA: ~{latest.get("ETA", "3.7 mins")}) • ORIGIN: {latest.get("Origin", "Majura Gate")}
    </div>
    ''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'''
        <div style="background: linear-gradient(145deg, rgba(15,23,42,0.85), rgba(30,58,138,0.3)); border: 1.5px solid #38bdf8; border-radius: 14px; padding: 18px; min-height: 195px;">
            <div style="font-size:10.5px; font-weight:800; text-transform:uppercase; color:#38bdf8; margin-bottom:8px;">PATIENT DOSSIER</div>
            <div style="font-size: 22px; font-weight: 900; color: #f8fafc; margin-bottom: 6px;">{latest.get("Patient", "Pooja Sharma")}</div>
            <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.6;">
                <strong>Age:</strong> {latest.get("Age", "28")} years<br>
                <strong>Blood Group:</strong> <span style="color:#f43f5e; font-weight:800;">{latest.get("BloodGroup", "B+")}</span><br>
                <span style="color:#f87171; font-weight:600; font-size:11.5px;">{latest.get("Condition", "Severe Trauma")}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''
        <div style="background: linear-gradient(145deg, rgba(15,23,42,0.85), rgba(6,78,59,0.35)); border: 1.5px solid #22c55e; border-radius: 14px; padding: 18px; min-height: 195px;">
            <div style="font-size:10.5px; font-weight:800; text-transform:uppercase; color:#4ade80; margin-bottom:8px;">LIVE ICU TELEMETRY (ESP32 V2X LINK)</div>
            <div style="display:flex; justify-content:space-around; text-align:center; margin-top:16px;">
                <div>
                    <div style="font-size: 10px; font-weight: 800; color: #94a3b8;">PULSE</div>
                    <div style="font-size: 24px; font-weight: 900; color: #22c55e;">{latest.get("Pulse", "108 BPM")}</div>
                </div>
                <div>
                    <div style="font-size: 10px; font-weight: 800; color: #94a3b8;">SpO2</div>
                    <div style="font-size: 24px; font-weight: 900; color: #38bdf8;">{latest.get("SpO2", "96%")}</div>
                </div>
                <div>
                    <div style="font-size: 10px; font-weight: 800; color: #94a3b8;">BP</div>
                    <div style="font-size: 24px; font-weight: 900; color: #facc15;">{latest.get("BP", "130/85")}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''
        <div style="background: linear-gradient(145deg, rgba(15,23,42,0.85), rgba(120,53,15,0.3)); border: 1.5px solid #f59e0b; border-radius: 14px; padding: 18px; min-height: 195px;">
            <div style="font-size:10.5px; font-weight:800; text-transform:uppercase; color:#fbbf24; margin-bottom:8px;">STAGED FACILITY & DOCTOR</div>
            <div style="font-size: 13.5px; font-weight: 800; color: #38bdf8; margin-bottom: 4px;">{latest.get("Hospital", "SMIMER Medical College")}</div>
            <div style="font-size: 12px; color: #e2e8f0; margin-top: 4px;">👨‍⚕️ <strong>{latest.get("Doctor", "Dr. Specialist")}</strong></div>
            <div style="font-size: 11px; color: #94a3b8;">Corridor: {latest.get("Corridor", "EAST Lane")}</div>
            <div style="margin-top: 8px; font-size: 13px; font-weight: 800; color: #22c55e;">
                Reserved: {latest.get("Bed", "TRAUMA-BAY #02")}
            </div>
        </div>
        ''', unsafe_allow_html=True)

with tab_admin:
    st.markdown("### 🗄️ Master Incident Records")
    st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)

with tab_family:
    slip = f"""================================================================================
PULSEROUTE AI • 108 EMERGENCY CLINICAL HANDOVER SLIP
================================================================================
Token Ref         : {latest.get("Token", "#SOS-2013")}
Time Dispatched   : {latest.get("Time", "14:20:00")}
Patient Name      : {latest.get("Patient", "Pooja Sharma")} ({latest.get("Age", "28")}y) | Blood: {latest.get("BloodGroup", "B+")}
Condition         : {latest.get("Condition", "Severe Trauma")}
Telemetry Vitals  : Pulse: {latest.get("Pulse", "108 BPM")} | SpO2: {latest.get("SpO2", "96%")} | BP: {latest.get("BP", "130/85")}
Pickup Origin     : {latest.get("Origin", "Majura Gate")}
Receiving Facility: {latest.get("Hospital", "SMIMER Medical College")}
Attending Doctor  : {latest.get("Doctor", "Dr. Specialist")}
Reserved Bed      : {latest.get("Bed", "TRAUMA-BAY #02")}
Ambulance Unit    : {latest.get("Fleet", "GJ-01-EA-108 (ALS)")} | Pilot: {latest.get("Pilot", "Ramesh Kumar")}
"""
    st.code(slip, language="text")
    msg = f"EMERGENCY+ALERT:+Patient+{latest.get('Patient', 'Pooja Sharma')}+dispatched+from+{latest.get('Origin', 'Majura Gate')}+to+{latest.get('Hospital', 'SMIMER Medical College')}.+Bed:+{latest.get('Bed', 'TRAUMA-BAY #02')}.+Token:+{latest.get('Token', '#SOS-2013')}"
    st.markdown(f'''
    <a href="https://wa.me/?text={msg}" target="_blank" style="text-decoration:none;">
        <div style="background-color:#22c55e; color:#ffffff; font-weight:800; font-size:14px; text-align:center; padding:10px; border-radius:8px;">
            📲 Share Emergency Handover Details with Family on WhatsApp
        </div>
    </a>
    ''', unsafe_allow_html=True)
"""

# Write files directly
for path in glob.glob("pages/*Traffic*.py"):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(traffic_py)
    py_compile.compile(path, doraise=True)
    print(f"CLEAN & COMPILED: {path}")

for path in glob.glob("pages/*Police*.py"):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(police_py)
    py_compile.compile(path, doraise=True)
    print(f"CLEAN & COMPILED: {path}")

for path in glob.glob("pages/*Citizen*.py") + glob.glob("pages/*Broadcast*.py"):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(citizen_py)
    py_compile.compile(path, doraise=True)
    print(f"CLEAN & COMPILED: {path}")

for path in glob.glob("pages/*Hospital*.py"):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(hosp_py)
    py_compile.compile(path, doraise=True)
    print(f"CLEAN & COMPILED: {path}")

py_compile.compile("streamlit_app.py", doraise=True)
print("CLEAN & COMPILED: streamlit_app.py")

print("\n>>> ALL SYSTEM PAGES CLEANED AND VERIFIED WITH 0 ERRORS!")