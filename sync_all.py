import glob
import json
import os
import time

print(">>> STARTING FULL SYSTEM & DATABASE INTERCONNECTION...")

os.makedirs("backend", exist_ok=True)
os.makedirs("pages", exist_ok=True)

# 1. FIXED WRAPPER emergency_db.py (NO SYNTAX ERROR)
with open("emergency_db.py", "w", encoding="utf-8") as f:
    f.write("from backend.emergency_db import *\n")

# 2. CORE BACKEND ENGINE
backend_code = '''import json
import os
import time

DB_FILE = "incidents_db.json"

DEFAULT_RECORD = {
    "Token": "#SOS-2013",
    "Time": time.strftime("%H:%M:%S"),
    "Patient": "Pooja Sharma",
    "Age": "28",
    "BloodGroup": "B+",
    "Condition": "Severe Multi-Trauma / Neurological Shock",
    "SpO2": "96%",
    "Pulse": "108 BPM",
    "BP": "130/85",
    "Origin": "Majura Gate Chauraha (Central Surat)",
    "Hospital": "SMIMER Medical College & Apex ER (Umarwada)",
    "Doctor": "Dr. Ananya Joshi (Neuro Trauma Surgeon)",
    "Fleet": "GJ-01-EA-108 (ALS)",
    "Pilot": "Ramesh Kumar (+91 98765 43210)",
    "Corridor": "EAST Lane",
    "Bed": "TRAUMA-BAY #02",
    "ETA": "3.7 mins",
    "Radar": "450m",
    "Status": "Active (En-Route)",
    "PreemptionActive": True,
    "BedReserved": True
}

def load_db():
    if not os.path.exists(DB_FILE):
        save_db([DEFAULT_RECORD])
        return [DEFAULT_RECORD]
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
            if isinstance(d, list) and len(d) > 0:
                return d
            return [DEFAULT_RECORD]
    except Exception:
        return [DEFAULT_RECORD]

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_latest_incident():
    records = load_db()
    for r in records:
        if r.get("PreemptionActive", False) or "Active" in r.get("Status", ""):
            return r
    return records[0] if records else DEFAULT_RECORD

def update_live_draft_location(new_loc):
    records = load_db()
    if records:
        records[0]["Origin"] = str(new_loc).strip()
        save_db(records)

def add_dispatch(patient, age, bg, condition, spo2, pulse, bp, origin, hospital, fleet="GJ-01-EA-108 (ALS)", pilot="Ramesh Kumar (+91 98765 43210)", doctor="Dr. Specialist", corridor="EAST Lane", bed="TRAUMA-BAY #02", eta="3.7 mins", radar="450m"):
    records = load_db()
    for r in records:
        r["PreemptionActive"] = False
        if "Active" in r.get("Status", ""):
            r["Status"] = "Resolved (Handed Over)"

    token_num = 2000 + len(records) + 1
    new_token = f"#SOS-{token_num}"

    entry = {
        "Token": new_token,
        "Time": time.strftime("%H:%M:%S"),
        "Patient": str(patient).strip() or "Emergency Patient",
        "Age": str(age).strip() or "28",
        "BloodGroup": str(bg).strip() or "B+",
        "Condition": str(condition).strip(),
        "SpO2": f"{spo2}%" if "%" not in str(spo2) else str(spo2),
        "Pulse": f"{pulse} BPM" if "BPM" not in str(pulse) else str(pulse),
        "BP": str(bp),
        "Origin": str(origin).strip() or "Majura Gate Chauraha (Central Surat)",
        "Hospital": str(hospital).strip() or "SMIMER Medical College & Apex ER (Umarwada)",
        "Doctor": str(doctor).strip(),
        "Fleet": str(fleet).strip(),
        "Pilot": str(pilot).strip(),
        "Corridor": str(corridor).strip() or "EAST Lane",
        "Bed": str(bed).strip() or "TRAUMA-BAY #02",
        "ETA": eta,
        "Radar": radar,
        "Status": "Active (En-Route)",
        "PreemptionActive": True,
        "BedReserved": True
    }
    records.insert(0, entry)
    save_db(records)
    return new_token

create_emergency_dispatch = add_dispatch

def update_incident_status(token, status):
    records = load_db()
    for r in records:
        if r.get("Token") == token:
            r["Status"] = status
            if "Resolved" in status or "Normal" in status:
                r["PreemptionActive"] = False
            break
    save_db(records)
'''
with open("backend/emergency_db.py", "w", encoding="utf-8") as f:
    f.write(backend_code)

# 3. INITIALIZE LIVE DATABASE WITH SMIMER INCIDENT
active_init = [{
    "Token": "#SOS-2013",
    "Time": time.strftime("%H:%M:%S"),
    "Patient": "Pooja Sharma",
    "Age": "28",
    "BloodGroup": "B+",
    "Condition": "Severe Multi-Trauma / Neurological Shock",
    "SpO2": "96%",
    "Pulse": "108 BPM",
    "BP": "130/85",
    "Origin": "Majura Gate Chauraha (Central Surat)",
    "Hospital": "SMIMER Medical College & Apex ER (Umarwada)",
    "Doctor": "Dr. Ananya Joshi (Neuro Trauma Surgeon)",
    "Fleet": "GJ-01-EA-108 (ALS)",
    "Pilot": "Ramesh Kumar (+91 98765 43210)",
    "Corridor": "EAST Lane",
    "Bed": "TRAUMA-BAY #02",
    "ETA": "3.7 mins",
    "Radar": "450m",
    "Status": "Active (En-Route)",
    "PreemptionActive": True,
    "BedReserved": True
}]
with open("incidents_db.json", "w", encoding="utf-8") as f:
    json.dump(active_init, f, indent=4)

# 4. CONNECT TRAFFIC CONTROL PAGE
t_code = '''import streamlit as st
from backend import emergency_db

st.set_page_config(page_title="Traffic Preemption Controller", page_icon="🚦", layout="wide")
st.markdown("<style>.stApp { background-color: #060d1d !important; color: #f8fafc; }</style>", unsafe_allow_html=True)

inc = emergency_db.get_latest_incident()
is_active = inc.get("PreemptionActive", True)

st.markdown(f"""
<div style="background: linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:18px 24px; display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
    <div>
        <div style="font-size: 19px; font-weight: 900; color: #f8fafc;">🚦 4-WAY V2X TRAFFIC PREEMPTION CONTROLLER</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Live Intersection Preemption Synchronized With Dispatch Bus</div>
    </div>
    <div style="background:rgba(34,197,94,0.15); color:#22c55e; border:1px solid #22c55e; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:800;">
        {('PREEMPTION ARMED 🚨' if is_active else 'STANDBY CYCLIC MODE')}
    </div>
</div>
""", unsafe_allow_html=True)

if is_active:
    st.markdown(f"""
    <div style="background:rgba(6,78,59,0.35); border:1.5px solid #059669; border-radius:10px; padding:14px 18px; margin-bottom:18px;">
        <div style="font-size:14px; font-weight:800; color:#34d399;">🚨 LIVE EMERGENCY CORRIDOR ENGAGED: {inc.get('Token')}</div>
        <div style="font-size:12.5px; color:#e2e8f0; margin-top:6px; line-height:1.7;">
            • <strong>ORIGIN:</strong> <span style="color:#facc15; font-weight:bold;">{inc.get('Origin')}</span><br>
            • <strong>DESTINATION:</strong> <span style="color:#38bdf8; font-weight:bold;">{inc.get('Hospital')}</span><br>
            • <strong>AMBULANCE:</strong> {inc.get('Fleet')} | <strong>DRIVER:</strong> {inc.get('Pilot')}<br>
            • <strong>PREEMPTION SIGNAL LOCK:</strong> <span style="color:#4ade80; font-weight:900;">{inc.get('Corridor', 'EAST Lane').upper()} (GREEN WAVE ACTIVE 🟢)</span> | <strong>RADAR:</strong> {inc.get('Radar', '450m')}
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("No active emergency preemption detected. Traffic signals operating in standard cyclic rotation.")

st.markdown("### 🚦 Live 4-Way Junction Signal State Machine")
c1, c2, c3 = st.columns(3)
active_corr = inc.get("Corridor", "NORTH").upper()

for col, pole, name in [(c1, "#1", "NORTH APPROACH"), (c2, "#2", "SOUTH APPROACH"), (c3, "#3", "EAST APPROACH")]:
    with col:
        match = (name.split()[0] in active_corr) and is_active
        bg = "background:rgba(6,78,59,0.5); border:1.5px solid #22c55e;" if match else "background:rgba(15,23,42,0.7); border:1px solid rgba(255,255,255,0.08);"
        txt = "🟢 FORCED GREEN WAVE (LOCKED)" if match else "STANDARD CYCLIC"
        col_t = "#4ade80" if match else "#cbd5e1"
        st.markdown(f"<div style='{bg} border-radius:12px; padding:16px; text-align:center;'><div style='font-size:11px; color:#94a3b8;'>JUNCTION POLE {pole}</div><div style='font-size:15px; font-weight:800; margin:6px 0;'>{name}</div><div style='color:{col_t}; font-weight:bold;'>{txt}</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
with b1:
    if st.button("🚨 Lock Green Corridor & Broadcast Signal Override", use_container_width=True, type="primary"):
        emergency_db.update_incident_status(inc.get("Token"), "Active (En-Route)")
        st.rerun()
with b2:
    if st.button("🔄 Revert to Automated Cyclic Phasing", use_container_width=True):
        emergency_db.update_incident_status(inc.get("Token"), "Resolved (Handed Over)")
        st.rerun()
'''
for f in glob.glob("pages/*Traffic*.py"):
    open(f, "w", encoding="utf-8").write(t_code)

# 5. CONNECT POLICE CAD ROOM
p_code = '''import streamlit as st
from backend import emergency_db

st.set_page_config(page_title="Police CAD Room", page_icon="👮", layout="wide")
st.markdown("<style>.stApp { background-color: #060d1d !important; color: #f8fafc; }</style>", unsafe_allow_html=True)

inc = emergency_db.get_latest_incident()
is_active = inc.get("PreemptionActive", True)

st.markdown("""
<div style="background: linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:18px 24px; display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
    <div>
        <div style="font-size: 19px; font-weight: 900; color: #38bdf8;">👮 SURAT TRAFFIC POLICE V2X ENFORCEMENT & CAD ROOM</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Live Corridor Preemption Tracking & Obstruction Surveillance</div>
    </div>
    <div style="background:rgba(225,29,72,0.15); color:#f43f5e; border:1px solid #f43f5e; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:800;">
        POLICE CAD DESK
    </div>
</div>
""", unsafe_allow_html=True)

if is_active:
    st.markdown(f"""
    <div style="background:rgba(15,23,42,0.9); border:1.5px solid #0284c7; border-radius:12px; padding:18px 22px; margin-bottom:20px;">
        <div style="font-size:16px; font-weight:900; color:#38bdf8; margin-bottom:12px;">
            🚓 ACTIVE V2X POLICE ESCORT: {inc.get('Token')}
        </div>
        <div style="font-size:13.5px; color:#e2e8f0; line-height:2.0;">
            <div>📍 <strong>DISPATCH ORIGIN (KAHAN SE NIKLI):</strong> <span style="color:#facc15; font-weight:800;">{inc.get('Origin')}</span></div>
            <div>🎯 <strong>TARGET DESTINATION (KAHAN JAYEGI):</strong> <span style="color:#38bdf8; font-weight:800;">{inc.get('Hospital')}</span></div>
            <div>🚑 <strong>FLEET UNIT:</strong> {inc.get('Fleet')} | <strong>PILOT:</strong> {inc.get('Pilot')}</div>
            <div>🚦 <strong>CLEARED GREEN LANE:</strong> <span style="color:#4ade80; font-weight:800;">{inc.get('Corridor', 'EAST Lane').upper()} (PREEMPTION ACTIVE 🟢)</span></div>
            <div>⏱️ <strong>ESTIMATED TIME TO ARRIVAL (ETA):</strong> {inc.get('ETA', '3.5 mins')} | <strong>RADAR RANGE:</strong> {inc.get('Radar', '450m')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("All Surat junction corridors operating normally. No active emergency preemption requests.")
'''
for f in glob.glob("pages/*Police*.py"):
    open(f, "w", encoding="utf-8").write(p_code)

# 6. CONNECT CITIZEN BROADCAST PORTAL
c_code = '''import streamlit as st
from backend import emergency_db

st.set_page_config(page_title="Citizen Broadcast Portal", page_icon="📢", layout="wide")
st.markdown("<style>.stApp { background-color: #060d1d !important; color: #f8fafc; }</style>", unsafe_allow_html=True)

inc = emergency_db.get_latest_incident()
is_active = inc.get("PreemptionActive", True)

st.markdown("""
<div style="background: linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:18px 24px; display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
    <div>
        <div style="font-size: 19px; font-weight: 900; color: #38bdf8;">📢 SURAT CITIZEN EMERGENCY BROADCAST PORTAL</div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Public Advisory & Emergency Vehicle Right-Of-Way Notices</div>
    </div>
    <div style="background:rgba(245,158,11,0.15); color:#f59e0b; border:1px solid #f59e0b; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:800;">
        PUBLIC BROADCAST
    </div>
</div>
""", unsafe_allow_html=True)

if is_active:
    st.markdown(f"""
    <div style="background:rgba(225,29,72,0.15); border:1.5px solid #f43f5e; border-radius:10px; padding:14px 18px; margin-bottom:18px;">
        <div style="font-size:14px; font-weight:900; color:#f43f5e;">🚨 URGENT PUBLIC ADVISORY: GREEN WAVE CORRIDOR ACTIVE ({inc.get('Token')})</div>
        <div style="font-size:13px; color:#e2e8f0; margin-top:6px; line-height:1.7;">
            High-priority 108 Ambulance ({inc.get('Fleet')}) en-route from <strong>{inc.get('Origin')}</strong> to <strong>{inc.get('Hospital')}</strong>.<br>
            Citizens on <strong>{inc.get('Corridor')}</strong> are requested to keep the left lane clear. ETA: {inc.get('ETA')}.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.success("Standard City Traffic Phase: No active emergency corridor disruptions in Surat.")
'''
for f in glob.glob("pages/*Citizen*.py") + glob.glob("pages/*Broadcast*.py"):
    open(f, "w", encoding="utf-8").write(c_code)
