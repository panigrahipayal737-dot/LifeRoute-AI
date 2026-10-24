import os
import glob
import sqlite3
import json
from datetime import datetime

print(">>> [1/5] Building Unified SQLite Schemas...")
db_dir = os.path.join("backend", "app", "database")
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "traffic_system.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS dispatch_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id TEXT UNIQUE,
    date_stamp TEXT,
    time_stamp TEXT,
    patient_name TEXT,
    patient_age INTEGER,
    patient_blood TEXT,
    emergency_type TEXT,
    patient_spo2 INTEGER DEFAULT 98,
    patient_pulse INTEGER DEFAULT 82,
    patient_bp TEXT DEFAULT '120/80',
    pickup_location TEXT,
    target_hospital TEXT,
    ambulance_number TEXT,
    driver_name TEXT,
    driver_contact TEXT DEFAULT '+91 98765 43210',
    corridor_lane TEXT,
    bed_assigned TEXT DEFAULT 'CRITICAL-BAY #01',
    status TEXT DEFAULT 'ACTIVE'
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS challans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challan_id TEXT UNIQUE,
    vehicle_number TEXT,
    violation_type TEXT,
    penalty_amount INTEGER,
    location TEXT,
    timestamp TEXT,
    evidence_image TEXT,
    status TEXT DEFAULT 'PENDING'
)
""")

# Ensure initial case is present
cur.execute("SELECT COUNT(*) FROM dispatch_records")
if cur.fetchone()[0] == 0:
    cur.execute("""
    INSERT INTO dispatch_records 
    (incident_id, date_stamp, time_stamp, patient_name, patient_age, patient_blood, emergency_type, patient_spo2, patient_pulse, patient_bp, pickup_location, target_hospital, ambulance_number, driver_name, driver_contact, corridor_lane, bed_assigned, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "SOS-2107", "2026-09-24", "19:45:00", "Pooja Sharma", 28, "B+",
        "Acute Ischemic Stroke / Neurological Hemorrhage", 96, 108, "130/85",
        "Limbayat Chauraha, Surat", "Sunshine Global Hospital (Piplod / Dumas Road, Surat)",
        "GJ-01-EA-108 (ALS)", "Ramesh Kumar", "+91 98765 43210", "WEST", "CRITICAL-BAY #01", "ACTIVE"
    ))

conn.commit()
conn.close()

print(">>> [2/5] Updating Backend Database Engine (backend/app/core/db.py)...")
core_db_code = '''"""
LifeRoute AI - Central Synchronized SQLite Database Engine
"""
import sqlite3
import os
import json
from datetime import datetime

DB_DIR = os.path.join("backend", "app", "database")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "traffic_system.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dispatch_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id TEXT UNIQUE,
        date_stamp TEXT,
        time_stamp TEXT,
        patient_name TEXT,
        patient_age INTEGER,
        patient_blood TEXT,
        emergency_type TEXT,
        patient_spo2 INTEGER DEFAULT 98,
        patient_pulse INTEGER DEFAULT 82,
        patient_bp TEXT DEFAULT '120/80',
        pickup_location TEXT,
        target_hospital TEXT,
        ambulance_number TEXT,
        driver_name TEXT,
        driver_contact TEXT DEFAULT '+91 98765 43210',
        corridor_lane TEXT,
        bed_assigned TEXT DEFAULT 'CRITICAL-BAY #01',
        status TEXT DEFAULT 'ACTIVE'
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS challans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        challan_id TEXT UNIQUE,
        vehicle_number TEXT,
        violation_type TEXT,
        penalty_amount INTEGER,
        location TEXT,
        timestamp TEXT,
        evidence_image TEXT,
        status TEXT DEFAULT 'PENDING'
    )
    """)
    conn.commit()

    # Schema Migration Guard
    cur.execute("PRAGMA table_info(dispatch_records)")
    cols = [r["name"] for r in cur.fetchall()]
    cols_to_add = {
        "patient_spo2": "INTEGER DEFAULT 98",
        "patient_pulse": "INTEGER DEFAULT 82",
        "patient_bp": "TEXT DEFAULT '120/80'",
        "bed_assigned": "TEXT DEFAULT 'CRITICAL-BAY #01'",
        "driver_contact": "TEXT DEFAULT '+91 98765 43210'"
    }
    for c, ctype in cols_to_add.items():
        if c not in cols:
            try:
                cur.execute(f"ALTER TABLE dispatch_records ADD COLUMN {c} {ctype}")
            except Exception:
                pass
    conn.commit()
    conn.close()

init_db()

def insert_dispatch_record(rec):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO dispatch_records 
    (incident_id, date_stamp, time_stamp, patient_name, patient_age, patient_blood, emergency_type, patient_spo2, patient_pulse, patient_bp, pickup_location, target_hospital, ambulance_number, driver_name, driver_contact, corridor_lane, bed_assigned, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        rec.get("incident_id", f"SOS-{int(datetime.now().timestamp()) % 10000}"),
        rec.get("date_stamp", datetime.now().strftime("%Y-%m-%d")),
        rec.get("time_stamp", datetime.now().strftime("%H:%M:%S")),
        rec.get("patient_name", "Emergency Patient"),
        rec.get("patient_age", 28),
        rec.get("patient_blood", "B+"),
        rec.get("emergency_type", "Critical Golden Hour Trauma"),
        rec.get("patient_spo2", 96),
        rec.get("patient_pulse", 108),
        rec.get("patient_bp", "130/85"),
        rec.get("pickup_location", "Limbayat Chauraha, Surat"),
        rec.get("target_hospital", "Sunshine Global Hospital (Piplod / Dumas Road, Surat)"),
        rec.get("ambulance_number", "GJ-01-EA-108 (ALS)"),
        rec.get("driver_name", "Ramesh Kumar"),
        rec.get("driver_contact", "+91 98765 43210"),
        rec.get("corridor_lane", "WEST"),
        rec.get("bed_assigned", "CRITICAL-BAY #01"),
        rec.get("status", "ACTIVE")
    ))
    conn.commit()
    conn.close()

    try:
        with open("active_emergency_bus.json", "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=2)
    except Exception:
        pass

def save_dispatch_record(rec):
    insert_dispatch_record(rec)

def get_latest_active_dispatch():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM dispatch_records WHERE status IN ('ACTIVE', 'ENGAGED') ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    if not row:
        cur.execute("SELECT * FROM dispatch_records ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_dispatches(limit=30):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM dispatch_records ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_status(incident_id, status_val):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE dispatch_records SET status = ? WHERE incident_id = ?", (status_val, incident_id))
    conn.commit()
    conn.close()
    try:
        if os.path.exists("active_emergency_bus.json"):
            with open("active_emergency_bus.json", "w", encoding="utf-8") as f:
                json.dump({"incident_id": incident_id, "status": status_val}, f)
    except Exception:
        pass

def insert_challan(ch):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO challans 
    (challan_id, vehicle_number, violation_type, penalty_amount, location, timestamp, evidence_image, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ch.get("challan_id", f"CH-{int(datetime.now().timestamp())}"),
        ch.get("vehicle_number", "GJ-05-AB-1234"),
        ch.get("violation_type", "Green Corridor Obstruction"),
        ch.get("penalty_amount", 1000),
        ch.get("location", "Athwagate Junction, Surat"),
        ch.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ch.get("evidence_image", ""),
        ch.get("status", "PENDING")
    ))
    conn.commit()
    conn.close()

def get_all_challans():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM challans ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
'''
with open(os.path.join("backend", "app", "core", "db.py"), "w", encoding="utf-8") as f:
    f.write(core_db_code)

print(">>> [3/5] Updating Security Gatekeeper (backend/app/core/auth.py)...")
auth_code = '''"""
LifeRoute AI - Unified Hospital & Admin Gatekeeper
"""
import streamlit as st

def check_hospital_admin_access():
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False
        st.session_state.admin_user = None

    with st.sidebar:
        st.markdown("---")
        st.markdown("<div style='font-size:11px; font-weight:900; color:#38bdf8; letter-spacing:0.8px;'>⚡ LIFEROUTE WORKSTATIONS</div>", unsafe_allow_html=True)
        st.caption("🟢 **Public Pages:** Open Access\\n🔒 **Hospital & Admin:** Restricted Access")
        
        if st.session_state.admin_logged_in:
            st.markdown(f"""
            <div style="background:rgba(34,197,94,0.15); border:1.5px solid #22c55e; border-radius:10px; padding:10px; margin:8px 0;">
                <div style="font-size:10px; color:#86efac; font-weight:bold;">WORKSTATION UNLOCKED</div>
                <div style="font-size:12.5px; color:#ffffff; font-weight:900;">{st.session_state.admin_user}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔒 Lock Workstation", use_container_width=True, key="lock_station_btn"):
                st.session_state.admin_logged_in = False
                st.session_state.admin_user = None
                st.rerun()

    if st.session_state.admin_logged_in:
        return True

    _, col_center, _ = st.columns([0.8, 2, 0.8])
    with col_center:
        st.markdown('''
<div style="font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; max-width: 820px; margin: 15px auto; background: #ffffff; color: #0f172a; border-radius: 18px; border: 2px solid #e2e8f0; box-shadow: 0 20px 30px -10px rgba(0,0,0,0.15); overflow: hidden;">
    <!-- Header -->
    <div style="background: linear-gradient(135deg, #e11d48 0%, #b91c1c 100%); padding: 22px 28px; color: #ffffff; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="background: rgba(255,255,255,0.2); width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">🚑</div>
            <div>
                <div style="font-size: 19px; font-weight: 900; letter-spacing: 0.5px; text-transform: uppercase;">LifeRoute Clinical Handover</div>
                <div style="font-size: 11px; opacity: 0.9; font-weight: 600;">108 EMERGENCY MEDICAL DISPATCH • SURAT APEX NETWORK</div>
            </div>
        </div>
        <div style="text-align: right; background: rgba(0,0,0,0.2); padding: 8px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.25);">
            <div style="font-size: 10px; text-transform: uppercase; font-weight: 700; color: #fecdd3;">DISPATCH TOKEN</div>
            <div style="font-size: 16px; font-weight: 900; letter-spacing: 0.8px;">#SOS-1401</div>
        </div>
    </div>

    <!-- Meta Details -->
    <div style="background: #f8fafc; padding: 10px 28px; border-bottom: 1.5px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; color: #64748b;">
        <span>🕒 <strong>Timestamp:</strong> 26-Sep-2026 11:15:14</span>
        <span style="color: #dc2626;">🔴 <strong>Triage Category:</strong> CODE RED (PRIORITY-1)</span>
        <span>🛰️ <strong>Corridor:</strong> V2X Green-Wave Active</span>
    </div>

    <div style="padding: 24px 28px;">
        <!-- Section 1: Patient Profile -->
        <div style="margin-bottom: 20px;">
            <div style="font-size: 11px; font-weight: 800; color: #e11d48; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                <span>👤</span> 1. PATIENT DOSSIER & CLINICAL PROFILE
            </div>
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px 16px;">
                <div><span style="font-size: 10.5px; color: #64748b; display: block; font-weight: 700;">PATIENT NAME</span><strong style="font-size: 14.5px; color: #0f172a;">Payal</strong></div>
                <div><span style="font-size: 10.5px; color: #64748b; display: block; font-weight: 700;">AGE</span><strong style="font-size: 14.5px; color: #0f172a;">21 Years</strong></div>
                <div><span style="font-size: 10.5px; color: #64748b; display: block; font-weight: 700;">BLOOD GROUP</span><strong style="font-size: 14.5px; color: #dc2626;">B+ (Positive)</strong></div>
                <div style="grid-column: span 3; border-top: 1px dashed #cbd5e1; padding-top: 8px; margin-top: 4px;">
                    <span style="font-size: 10.5px; color: #64748b; display: block; font-weight: 700;">PRIMARY EMERGENCY CONDITION</span>
                    <strong style="font-size: 13.5px; color: #b91c1c;">Cardiac Arrest / Sudden Heart Failure (CPR En-Route)</strong>
                </div>
            </div>
        </div>

        <!-- Section 2: Vitals Telemetry -->
        <div style="margin-bottom: 20px;">
            <div style="font-size: 11px; font-weight: 800; color: #0284c7; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                <span>🫀</span> 2. IN-TRANSIT ICU TELEMETRY VITALS
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
                <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 12px; padding: 12px 14px; text-align: center;">
                    <div style="font-size: 10.5px; color: #166534; font-weight: 800; text-transform: uppercase;">OXYGEN (SpO2)</div>
                    <div style="font-size: 24px; font-weight: 900; color: #15803d; margin-top: 2px;">96%</div>
                    <div style="font-size: 10px; color: #16a34a; font-weight: 700;">STABLE WITH O2</div>
                </div>
                <div style="background: #eff6ff; border: 1.5px solid #93c5fd; border-radius: 12px; padding: 12px 14px; text-align: center;">
                    <div style="font-size: 10.5px; color: #1e40af; font-weight: 800; text-transform: uppercase;">PULSE RATE</div>
                    <div style="font-size: 24px; font-weight: 900; color: #1d4ed8; margin-top: 2px;">108 <span style="font-size: 12px; font-weight: 600;">BPM</span></div>
                    <div style="font-size: 10px; color: #2563eb; font-weight: 700;">TACHYCARDIA MONITOR</div>
                </div>
                <div style="background: #fff1f2; border: 1.5px solid #fecdd3; border-radius: 12px; padding: 12px 14px; text-align: center;">
                    <div style="font-size: 10.5px; color: #9f1239; font-weight: 800; text-transform: uppercase;">BLOOD PRESSURE</div>
                    <div style="font-size: 24px; font-weight: 900; color: #be123c; margin-top: 2px;">130/85</div>
                    <div style="font-size: 10px; color: #e11d48; font-weight: 700;">MMHG (CONTROLLED)</div>
                </div>
            </div>
        </div>

        <!-- Section 3: Transit Routing & Facility -->
        <div style="margin-bottom: 24px;">
            <div style="font-size: 11px; font-weight: 800; color: #16a34a; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                <span>🏥</span> 3. V2X ROUTE TRANSIT & EMERGENCY BED STAGING
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px 16px;">
                <div><span style="font-size: 10.5px; color: #64748b; display: block; font-weight: 700;">INCIDENT ORIGIN</span><strong style="font-size: 13px; color: #0f172a;">📍 Vesu VIP Road Junction (South Surat)</strong></div>
                <div><span style="font-size: 10.5px; color: #64748b; display: block; font-weight: 700;">RECEIVING TRAUMA CENTER</span><strong style="font-size: 13px; color: #0284c7;">🏥 BAPS Pramukh Swami Hospital & Heart Care</strong></div>
                <div><span style="font-size: 10.5px; color: #64748b; display: block; font-weight: 700;">FLEET UNIT & PILOT</span><strong style="font-size: 13px; color: #0f172a;">🚑 GJ-01-EA-108 (ALS) • Ramesh Kumar</strong></div>
                <div><span style="font-size: 10.5px; color: #64748b; display: block; font-weight: 700;">ALLOCATED ICU BED</span><strong style="font-size: 13px; color: #16a34a;">🛏️ CRITICAL-BAY #01 (VENTILATOR READY)</strong></div>
            </div>
        </div>

        <!-- Section 4: Physical Signatures -->
        <div style="display: flex; justify-content: space-between; border-top: 1.5px dashed #cbd5e1; padding-top: 20px;">
            <div style="text-align: center; width: 42%;">
                <div style="height: 38px; border-bottom: 1.5px solid #94a3b8; margin-bottom: 6px;"></div>
                <div style="font-size: 11px; font-weight: 800; color: #475569;">✍️ 108 PARAMEDIC SIGN & STAMP</div>
            </div>
            <div style="text-align: center; width: 42%;">
                <div style="height: 38px; border-bottom: 1.5px solid #94a3b8; margin-bottom: 6px;"></div>
                <div style="font-size: 11px; font-weight: 800; color: #475569;">✍️ RECEIVING CMO / TRAUMA DOCTOR SIGN</div>
            </div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

tab_intake, tab_admin = st.tabs(["🏥 Emergency Hospital Intake & Triage", "⚙️ Master Admin Audit & PDF Hub"])

c = get_latest_active_dispatch()

with tab_intake:
    if c and c.get("status") in ["ACTIVE", "ENGAGED"]:
        inc_id = c.get("incident_id", "SOS-2107")
        p_name = c.get("patient_name", "Emergency Patient")
        p_age = c.get("patient_age", 28)
        p_blood = c.get("patient_blood", "B+")
        p_diag = c.get("emergency_type", "Acute Medical Emergency")
        p_spo2 = c.get("patient_spo2", 96)
        p_pulse = c.get("patient_pulse", 108)
        p_bp = c.get("patient_bp", "130/85")
        target_hosp = c.get("target_hospital", "Sunshine Global Hospital")
        pickup_spot = c.get("pickup_location", "Limbayat Chauraha, Surat")
        amb_no = c.get("ambulance_number", "GJ-01-EA-108")
        driver_name = c.get("driver_name", "Ramesh Kumar")
        driver_phone = c.get("driver_contact", "+91 98765 43210")
        bed_allocated = c.get("bed_assigned", "CRITICAL-BAY #01")

        st.markdown(f"""
        <div style="background:rgba(69,10,10,0.92); border:2px solid #ef4444; border-radius:14px; padding:22px 26px; box-shadow:0 0 35px rgba(239,68,68,0.3); margin-bottom:18px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#f87171; font-size:18px; font-weight:900;">🚨 INCOMING RESCUE: #{inc_id}</h4>
                <span style="background:#ef4444; color:#ffffff; padding:4px 12px; border-radius:12px; font-size:11px; font-weight:900;">ACTIVE IN-TRANSIT</span>
            </div>
            <div style="margin-top:12px; font-size:14px; color:#f1f5f9; line-height:1.8;">
                🏥 <b>RECEIVING FACILITY:</b> <span style="color:#67e8f9; font-weight:bold;">{target_hosp}</span><br>
                🛣️ <b>PICKUP INCIDENT SPOT:</b> <span style="color:#facc15; font-weight:bold;">{pickup_spot}</span><br>
                👤 <b>PATIENT:</b> {p_name} ({p_age}y) &bull; 🩸 <b>BLOOD:</b> <span style="color:#f43f5e; font-weight:bold;">{p_blood}</span><br>
                🩺 <b>PRIMARY DIAGNOSIS:</b> <span style="color:#fbbf24; font-weight:bold;">{p_diag}</span><br>
                🚑 <b>108 UNIT:</b> {amb_no} &bull; <b>PILOT:</b> {driver_name} ({driver_phone})<br>
                🛏️ <b>RESERVED BED:</b> <span style="color:#4ade80; font-weight:bold;">{bed_allocated} (LOCKED & PREPPED)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🫀 Live Telemetry Monitor")
        v1, v2, v3, v4 = st.columns(4)
        with v1:
            st.metric("SpO2 Oxygen", f"{p_spo2}%")
        with v2:
            st.metric("Pulse Rate", f"{p_pulse} BPM")
        with v3:
            st.metric("Blood Pressure", str(p_bp))
        with v4:
            st.metric("Crossmatched Blood", f"{p_blood} Units Reserved")

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        if st.button("✅ Confirm Patient Reception & Complete Handover", type="primary", use_container_width=True):
            update_status(inc_id, "RESOLVED")
            st.success(f"Emergency #{inc_id} successfully admitted into {bed_allocated}!")
            st.rerun()
    else:
        st.info("ℹ️ No active incoming ambulance pre-alert. Telemetry listening on Surat V2X Network.")

with tab_admin:
    st.markdown("### 🫀 Patient Clinical Dossier & PDF Export")
    if c:
        inc_id = c.get("incident_id", "SOS-2107")
        p_name = c.get("patient_name", "Emergency Patient")
        p_age = c.get("patient_age", 28)
        p_blood = c.get("patient_blood", "B+")
        p_diag = c.get("emergency_type", "Acute Medical Emergency")
        p_spo2 = c.get("patient_spo2", 96)
        p_pulse = c.get("patient_pulse", 108)
        target_hosp = c.get("target_hospital", "Sunshine Global Hospital")

        col_dossier, col_export = st.columns([1.5, 1.5])
        with col_dossier:
            st.markdown(f"""
            <div style="background:rgba(15,23,42,0.9); border:1.5px solid #22c55e; border-radius:12px; padding:18px; box-shadow:0 0 25px rgba(34,197,94,0.25);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#facc15; font-size:16px; font-weight:900;">#{inc_id} - {p_name} ({p_age}y)</h4>
                    <span style="background:rgba(34,197,94,0.2); color:#4ade80; padding:3px 8px; border-radius:10px; font-size:11px; font-weight:bold;">{c.get('status', 'ACTIVE')}</span>
                </div>
                <div style="margin-top:8px; font-size:13px; color:#ffffff; font-weight:bold;">
                    Clinical Diagnosis: <span style="color:#cbd5e1; font-weight:normal;">{p_diag}</span>
                </div>
                <div style="display:flex; gap:16px; margin-top:12px; font-size:12px; color:#cbd5e1;">
                    <div>🩸 Blood: <b style="color:#ef4444;">{p_blood}</b></div>
                    <div>❤️ Pulse: <b style="color:#22c55e;">{p_pulse} BPM</b></div>
                    <div>🫁 SpO2: <b style="color:#38bdf8;">{p_spo2}%</b></div>
                </div>
                <div style="margin-top:10px; font-size:12px; color:#94a3b8;">
                    🏥 Target: <b style="color:#ffffff;">{target_hosp}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_export:
            pdf_bytes, saved_path = generate_and_save_admin_pdf(c)
            
            st.download_button(
                label=f"📄 Download {p_name}'s Report (.PDF)",
                data=pdf_bytes,
                file_name=f"Clinical_Handover_{inc_id}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
            st.success(f"📁 Auto-Saved directly to: `{saved_path}`")
            
            share_msg = (
                f"LIFEROUTE AI - CLINICAL REPORT\\n"
                f"Token: #{inc_id}\\n"
                f"Patient: {p_name} ({p_age}y, Blood: {p_blood})\\n"
                f"Condition: {p_diag}\\n"
                f"Hospital: {target_hosp}\\n"
                f"Vitals: SpO2: {p_spo2}% | Pulse: {p_pulse} BPM\\n"
                f"Saved in Folder: {saved_path}"
            )
            encoded_msg = urllib.parse.quote(share_msg)
            wa_url = f"https://api.whatsapp.com/send?text={encoded_msg}"
            mail_url = f"mailto:?subject=Clinical Handover - Incident {inc_id}&body={encoded_msg}"
            
            s1, s2 = st.columns(2)
            with s1:
                st.markdown(f"""
                <a href="{wa_url}" target="_blank" style="text-decoration:none;">
                    <div style="background:#25D366; color:white; font-weight:bold; font-size:13px; text-align:center; padding:10px; border-radius:8px; display:flex; align-items:center; justify-content:center; gap:8px;">
                        💬 Share on WhatsApp
                    </div>
                </a>
                """, unsafe_allow_html=True)
            with s2:
                st.markdown(f"""
                <a href="{mail_url}" target="_blank" style="text-decoration:none;">
                    <div style="background:#0284c7; color:white; font-weight:bold; font-size:13px; text-align:center; padding:10px; border-radius:8px; display:flex; align-items:center; justify-content:center; gap:8px;">
                        ✉️ Share via Email
                    </div>
                </a>
                """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ No active emergency dispatch record currently selected.")

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # Master Dispatch Records Table
    st.markdown("### 🗄️ Master Emergency Dispatch Records Log")
    records = get_all_dispatches(30)
    if records:
        df = pd.DataFrame(records)
        cols_to_show = ["id", "incident_id", "date_stamp", "time_stamp", "patient_name", "patient_age", "patient_blood", "emergency_type", "target_hospital", "corridor_lane", "bed_assigned", "status"]
        existing_cols = [col for col in cols_to_show if col in df.columns]
        st.dataframe(df[existing_cols], use_container_width=True)
    else:
        st.caption("No records logged in database.")

st.markdown("---")
st.caption("LifeRoute AI • Unified Hospital Intake & Master Admin Desk")
'''

with open("pages/7_🏥_Hospital_Admin_Desk.py", "w", encoding="utf-8") as f:
    f.write(unified_desk_code)

print(">>> [5/5] Re-branding remaining files to 'LifeRoute AI'...")
for root, dirs, files in os.walk("."):
    if any(ignore in root for ignore in ["venv", ".git", "__pycache__", ".streamlit"]):
        continue
    for file in files:
        if file.endswith(".py") or file.endswith(".json"):
            fp = os.path.join(root, file)
            try:
                with open(fp, "r", encoding="utf-8") as rf:
                    cnt = rf.read()
                if "LifeRoute" in cnt or "liferoute" in cnt or "LIFEROUTE" in cnt:
                    cnt = cnt.replace("LifeRoute AI", "LifeRoute AI")
                    cnt = cnt.replace("LifeRoute", "LifeRoute")
                    cnt = cnt.replace("liferoute", "liferoute")
                    cnt = cnt.replace("LIFEROUTE", "LIFEROUTE")
                    with open(fp, "w", encoding="utf-8") as wf:
                        wf.write(cnt)
            except Exception:
                pass

print("\n========================================================")
print("SUCCESS: LIFEROUTE AI 100% UNIFIED & READY!")
print("========================================================")
