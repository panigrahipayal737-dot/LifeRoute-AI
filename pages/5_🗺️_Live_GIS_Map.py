import streamlit as st
import folium
from streamlit_folium import st_folium
from backend import emergency_db

st.set_page_config(page_title="Live GIS Map", page_icon="🗺️", layout="wide")

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
    <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%); border: 2px solid #38bdf8; border-radius: 14px; padding: 16px 12px; text-align: center; margin-top: -30px; margin-bottom: 22px;">
        <div style="font-size: 32px; margin-bottom: 4px;">🚨</div>
        <div style="font-size: 21px; font-weight: 900; background: linear-gradient(90deg, #38bdf8, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            PulseRoute AI
        </div>
        <div style="display: inline-block; background: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e; color: #4ade80; border-radius: 12px; padding: 3px 10px; font-size: 10px; font-weight: 800; margin-top: 6px;">
            ● SURAT V2X CORRIDOR ACTIVE
        </div>
    </div>
    ''', unsafe_allow_html=True)

inc = emergency_db.get_latest_incident()

st.markdown('''
<div style="background: linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border: 1.5px solid rgba(56,189,248,0.4); border-radius:14px; padding:18px 24px; display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
    <div>
        <div style="font-size: 20px; font-weight: 900; color: #38bdf8; display:flex; align-items:center; gap:8px;">
            <span>🗺️</span> LIVE GIS EMERGENCY TRANSIT CORRIDOR
        </div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Surat Municipal Smart Traffic Mesh • V2X Spatial Tracking</div>
    </div>
    <div style="background:rgba(34,197,94,0.2); color:#4ade80; border:1.5px solid #22c55e; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:900;">
        GPS LOCK ACTIVE
    </div>
</div>
''', unsafe_allow_html=True)

# Top metrics
c_m1, c_m2, c_m3 = st.columns([2, 1, 1])
with c_m1:
    prog = st.slider("Simulate Ambulance Movement on Green Wave Corridor (%)", 0, 100, 42)
with c_m2:
    rem_dist = round(max(0.1, 4.2 * (1 - prog/100)), 2)
    st.metric("Remaining Distance", f"{rem_dist} km", delta=f"-{prog}% Traversed", delta_color="normal")
with c_m3:
    rem_time = round(max(0.2, 8.5 * (1 - prog/100)), 1)
    st.metric("Live Dynamic ETA", f"{rem_time} Mins", delta="Green Wave Speed", delta_color="inverse")

# Surat Coordinates
LOCS = {
    "Majura Gate": [21.1762, 72.8181],
    "Limbayat": [21.1824, 72.8550],
    "Adajan": [21.1959, 72.7933],
    "Vesu": [21.1442, 72.7758],
    "SMIMER": [21.1980, 72.8450],
    "Civil": [21.1765, 72.8185],
    "Mahavir": [21.1920, 72.8160]
}

start_pt = LOCS["Majura Gate"]
end_pt = LOCS["SMIMER"]

# Interpolate ambulance position
cur_lat = start_pt[0] + (end_pt[0] - start_pt[0]) * (prog / 100)
cur_lon = start_pt[1] + (end_pt[1] - start_pt[1]) * (prog / 100)

# Build Map
m = folium.Map(location=[cur_lat, cur_lon], zoom_start=13, tiles="CartoDB dark_matter")

# Route line
route_coords = [start_pt, [21.1850, 72.8300], [21.1920, 72.8380], end_pt]
folium.PolyLine(route_coords, color="#22c55e", weight=6, opacity=0.85, tooltip="Green Wave Preemption Corridor").add_to(m)

# Markers
folium.Marker(start_pt, tooltip=f"Pickup: {inc.get('Origin')}", icon=folium.Icon(color="orange", icon="info-sign")).add_to(m)
folium.Marker(end_pt, tooltip=f"Target: {inc.get('Hospital')}", icon=folium.Icon(color="red", icon="plus")).add_to(m)
folium.Marker([cur_lat, cur_lon], tooltip=f"Ambulance: {inc.get('Fleet')} (En-Route)", icon=folium.Icon(color="green", icon="play")).add_to(m)

st_folium(m, width="100%", height=460)

st.markdown(f'''
<div style="background: rgba(15,23,42,0.8); border: 1px solid rgba(56,189,248,0.2); border-radius: 10px; padding: 12px 16px; margin-top: 14px; display:flex; justify-content:space-between; font-size:12px;">
    <span>🚑 <strong>Active Unit:</strong> {inc.get('Fleet')}</span>
    <span>🚦 <strong>Preempted Lane:</strong> {inc.get('Corridor')}</span>
    <span>🏥 <strong>Destination Facility:</strong> {inc.get('Hospital')}</span>
</div>
''', unsafe_allow_html=True)
