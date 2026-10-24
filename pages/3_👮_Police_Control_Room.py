import streamlit as st
from backend import emergency_db

st.set_page_config(page_title="Police CAD Room", page_icon="👮", layout="wide")

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
eta_str = str(inc.get("ETA", "3.7 mins"))
radar_str = str(inc.get("Radar", "450m"))

st.markdown('''
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
    st.markdown('''
    <div style="background: linear-gradient(135deg, rgba(15,23,42,0.92) 0%, rgba(2,132,199,0.25) 100%); border: 1.5px solid #0284c7; border-radius: 12px; padding: 18px 22px; margin-bottom: 20px;">
        <div style="font-size: 16px; font-weight: 900; color: #38bdf8; margin-bottom: 12px;">
            🚓 ACTIVE V2X POLICE ESCORT: ''' + token_str + '''
        </div>
        <div style="font-size: 13.5px; color: #e2e8f0; line-height: 2.0;">
            <div>📍 <strong>DISPATCH ORIGIN:</strong> <span style="color:#facc15; font-weight:800;">''' + origin_str + '''</span></div>
            <div>🎯 <strong>TARGET DESTINATION:</strong> <span style="color:#38bdf8; font-weight:800;">''' + hosp_str + '''</span></div>
            <div>🚑 <strong>FLEET UNIT:</strong> ''' + fleet_str + ''' | <strong>PILOT:</strong> ''' + pilot_str + '''</div>
            <div>🚦 <strong>CLEARED GREEN LANE:</strong> <span style="color:#4ade80; font-weight:800;">''' + corridor_str + ''' (PREEMPTION ACTIVE 🟢)</span></div>
            <div>⏱️ <strong>ESTIMATED TIME TO ARRIVAL (ETA):</strong> ''' + eta_str + ''' | <strong>RADAR RANGE:</strong> ''' + radar_str + '''</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.info("All Surat junction corridors operating normally. No active emergency preemption requests.")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🚔 Interceptor Dispatch Status")
    st.success("Patrol Car assigned to " + corridor_str + " for clearing transit obstacles.")
with col2:
    st.markdown("#### 🛑 Manual Override")
    if st.button("Mark Route Cleared / Deactivate Police Escort", use_container_width=True):
        emergency_db.update_incident_status(token_str, "Resolved (Handed Over)")
        st.success("Escort deactivated.")
        st.rerun()
