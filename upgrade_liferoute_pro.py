import os
import glob

# =========================================================================
# 1. UPGRADE LIVE GIS MAP WITH VEHICLE PROGRESSION & TRAFFIC SIGNALS
# =========================================================================
map_files = glob.glob("pages/*GIS*.py") + glob.glob("pages/*Map*.py") + glob.glob("pages/*map*.py")
if not map_files:
    map_files = ["pages/5_🗺️_Live_GIS_Map.py"]

pro_map_code = '''"""
LifeRoute AI - Advanced Real-Time V2X Corridor with Dynamic Fleet Tracking
Developed for: Surat Municipal Corporation & 108 GVK-EMRI
"""
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import json
import os
import time

from backend.app.core.theme import apply_cyber_theme
from backend.app.core.db import get_latest_active_dispatch

st.set_page_config(
    page_title="LifeRoute AI • Live V2X Radar",
    layout="wide",
    page_icon="🗺️"
)
apply_cyber_theme()

st.markdown("""
<div class="page-header-box">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <h2 style="margin:0; font-size:22px; font-weight:900;">🗺️ SMART V2X RADAR & CORRIDOR JUNCTION OVERRIDE</h2>
            <p style="margin:4px 0 0 0; opacity:0.9; font-size:12.5px; color:#cbd5e1;">Live Road Geometry • Adaptive Signal Preemption • Fleet Progression Radar</p>
        </div>
        <span style="background:rgba(34,197,94,0.15); padding:6px 14px; border-radius:20px; font-size:11px; color:#4ade80; border:1px solid #22c55e; font-weight:bold;">108 ACTIVE V2X STREAM</span>
    </div>
</div>
""", unsafe_allow_html=True)

c = get_latest_active_dispatch()

# Base Coordinates
origin_lat, origin_lon = 21.1762, 72.8581
origin_name = "Limbayat Chauraha, Surat"
dest_lat, dest_lon = 21.1820, 72.8090
dest_name = "Sunshine Global Hospital (Piplod / Dumas Road, Surat)"
inc_id = "SOS-2107"
p_name = "Emergency Patient"

if c:
    inc_id = c.get("incident_id", inc_id)
    origin_name = c.get("pickup_location", origin_name)
    dest_name = c.get("target_hospital", dest_name)
    p_name = c.get("patient_name", p_name)

# Slider for simulated vehicle position along route
st.markdown("#### ⚡ Live Fleet In-Transit Progression Simulator")
col_sim, col_eta = st.columns([3, 1])
with col_sim:
    progress = st.slider("Simulate Ambulance Movement on Green Wave Corridor (%)", 0, 100, 35, step=5)
with col_eta:
    remaining_mins = max(1.5, round(14.0 * (1.0 - (progress / 100.0)), 1))
    st.metric("Live Dynamic ETA", f"{remaining_mins} Mins", delta=f"-{progress}% Traversed")

# Road Routing Engine using OSRM
def get_detailed_road_route(lat1, lon1, lat2, lon2):
    try:
        url = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
        resp = requests.get(url, timeout=4)
        if resp.status_code == 200:
            data = resp.json()
            if "routes" in data and len(data["routes"]) > 0:
                coords = data["routes"][0]["geometry"]["coordinates"]
                return [[pt[1], pt[0]] for pt in coords]
    except Exception:
        pass
    return [
        [21.1762, 72.8581], [21.1785, 72.8520], [21.1820, 72.8450],
        [21.1810, 72.8350], [21.1770, 72.8220], [21.1795, 72.8150], [21.1820, 72.8090]
    ]

full_route = get_detailed_road_route(origin_lat, origin_lon, dest_lat, dest_lon)

# Calculate dynamic ambulance marker coordinates based on slider progress
idx = int((len(full_route) - 1) * (progress / 100.0))
current_amb_pos = full_route[idx]

# Build Folium Map
map_mid = [(origin_lat + dest_lat) / 2, (origin_lon + dest_lon) / 2]
m = folium.Map(location=current_amb_pos, zoom_start=13, tiles="CartoDB dark_matter")

# Route Glowing Polyline
folium.PolyLine(locations=full_route, color="#0284c7", weight=8, opacity=0.45).add_to(m)
folium.PolyLine(locations=full_route, color="#22c55e", weight=5, opacity=0.9, tooltip="Green Wave Preempted Lane").add_to(m)

# Origin Marker
folium.Marker(
    location=[origin_lat, origin_lon],
    popup=f"<b>Origin:</b> {origin_name}",
    tooltip="📍 Pickup Spot",
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(m)

# Target Hospital Marker
folium.Marker(
    location=[dest_lat, dest_lon],
    popup=f"<b>Hospital:</b> {dest_name}",
    tooltip=f"🏥 {dest_name}",
    icon=folium.Icon(color="green", icon="plus")
).add_to(m)

# Active Moving Ambulance Marker
folium.Marker(
    location=current_amb_pos,
    popup=f"<b>108 Ambulance Unit</b><br>Patient: {p_name}<br>Speed: 68 km/h<br>Corridor: LOCKED",
    tooltip="🚑 108 Ambulance Unit (LIVE)",
    icon=folium.Icon(color="red", icon="flag")
).add_to(m)

folium.CircleMarker(
    location=current_amb_pos,
    radius=14,
    color="#ef4444",
    fill=True,
    fill_color="#ef4444",
    fill_opacity=0.35
).add_to(m)

# Preempted Traffic Junctions along route
junctions = [
    {"name": "Limbayat Junction", "pos": [21.1770, 72.8540], "status": "GREEN OVERRIDE"},
    {"name": "Ring Road Flyover", "pos": [21.1820, 72.8450], "status": "GREEN OVERRIDE"},
    {"name": "Majura Gate Cross", "pos": [21.1810, 72.8350], "status": "GREEN OVERRIDE"},
    {"name": "Athwagate Signal", "pos": [21.1770, 72.8220], "status": "GREEN OVERRIDE"}
]

for junc in junctions:
    folium.CircleMarker(
        location=junc["pos"],
        radius=7,
        color="#22c55e",
        fill=True,
        fill_color="#22c55e",
        fill_opacity=0.9,
        tooltip=f"🚦 {junc['name']}: {junc['status']}"
    ).add_to(m)

st_folium(m, width="100%", height=550)

# Junction Override Status Grid
st.markdown("### 🚦 Live Smart Junction Preemption Telemetry")
j1, j2, j3, j4 = st.columns(4)
with j1:
    st.markdown("""<div style="background:rgba(15,23,42,0.85); border:1px solid #22c55e; border-radius:10px; padding:12px; text-align:center;">
        <span style="color:#4ade80; font-weight:bold;">🟢 LIMBAYAT CROSS</span><br><small style="color:#cbd5e1;">Signal: PREEMPTED (GREEN)</small>
    </div>""", unsafe_allow_html=True)
with j2:
    st.markdown("""<div style="background:rgba(15,23,42,0.85); border:1px solid #22c55e; border-radius:10px; padding:12px; text-align:center;">
        <span style="color:#4ade80; font-weight:bold;">🟢 RING ROAD INTERSECTION</span><br><small style="color:#cbd5e1;">Signal: PREEMPTED (GREEN)</small>
    </div>""", unsafe_allow_html=True)
with j3:
    st.markdown("""<div style="background:rgba(15,23,42,0.85); border:1px solid #22c55e; border-radius:10px; padding:12px; text-align:center;">
        <span style="color:#4ade80; font-weight:bold;">🟢 MAJURA GATE</span><br><small style="color:#cbd5e1;">Signal: PREEMPTED (GREEN)</small>
    </div>""", unsafe_allow_html=True)
with j4:
    st.markdown("""<div style="background:rgba(15,23,42,0.85); border:1px solid #22c55e; border-radius:10px; padding:12px; text-align:center;">
        <span style="color:#4ade80; font-weight:bold;">🟢 ATHWAGATE SQUARE</span><br><small style="color:#cbd5e1;">Signal: PREEMPTED (GREEN)</small>
    </div>""", unsafe_allow_html=True)

st.markdown("---")
st.caption("LifeRoute AI • Intelligent Municipal Traffic Network")
'''

for mf in set(map_files):
    with open(mf, "w", encoding="utf-8") as f:
        f.write(pro_map_code)
    print("GIS MAP UPGRADED WITH INTERACTIVE VEHICLE RADAR:", mf)

print("\n--- ALL PROFESSIONAL SMART-CITY MODULES ADDED SUCCESSFULLY! ---")
