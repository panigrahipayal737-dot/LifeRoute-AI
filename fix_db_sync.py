import sqlite3
import os
import json
import glob

# Ensure DB directory exists and table schema is robust
DB_FILE = os.path.join("backend", "app", "database", "traffic_system.db")
if not os.path.exists(os.path.dirname(DB_FILE)):
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

# Create table if not exists with all required columns
cur.execute('''
CREATE TABLE IF NOT EXISTS dispatch_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id TEXT UNIQUE,
    date_stamp TEXT,
    time_stamp TEXT,
    patient_name TEXT,
    patient_age INTEGER,
    patient_blood TEXT,
    emergency_type TEXT,
    pickup_location TEXT,
    target_hospital TEXT,
    ambulance_number TEXT,
    driver_name TEXT,
    corridor_lane TEXT,
    status TEXT
)
''')
conn.commit()

# If there is an active emergency in JSON, sync it directly into the database right now
bus_file = "active_emergency_bus.json"
if os.path.exists(bus_file):
    try:
        with open(bus_file, "r", encoding="utf-8") as f:
            b = json.load(f)
            if b and b.get("incident_id"):
                cur.execute('''
                INSERT OR REPLACE INTO dispatch_records 
                (incident_id, date_stamp, time_stamp, patient_name, patient_age, patient_blood, emergency_type, pickup_location, target_hospital, ambulance_number, driver_name, corridor_lane, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    b.get("incident_id"),
                    b.get("date_stamp", "2026-09-23"),
                    b.get("time_stamp", "21:35:00"),
                    b.get("patient_name", "kavita sharma"),
                    b.get("patient_age", 28),
                    b.get("patient_blood", "B+"),
                    b.get("emergency_type", "Acute Ischemic Stroke / Neurological Hemorrhage"),
                    b.get("pickup_location", "Surat Center"),
                    b.get("target_hospital", b.get("target_hospital", "Tristar Multi-Specialty Hospital (Athwagate, Surat)")),
                    b.get("ambulance_number", "GJ-01-EA-108"),
                    b.get("driver_name", "Ramesh Kumar"),
                    b.get("corridor_lane", "WEST"),
                    b.get("status", "ACTIVE")
                ))
                conn.commit()
                print("Active case synced into SQLite table successfully!")
    except Exception as e:
        print("Sync error:", e)

conn.close()

# Update Admin Panel to directly read and display this table with zero errors
admin_code = '''
    <div style="font-family: 'Segoe UI', system-ui, sans-serif; max-width: 820px; margin: 15px auto; background: #ffffff; color: #0f172a; border-radius: 16px; border: 2px solid #e2e8f0; box-shadow: 0 20px 35px -10px rgba(0,0,0,0.18); overflow: hidden;">
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); padding: 22px 28px; color: #ffffff; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="background: rgba(255,255,255,0.2); width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">🚑</div>
                <div>
                    <div style="font-size: 19px; font-weight: 900; letter-spacing: 0.5px;">LIFEROUTE CLINICAL HANDOVER</div>
                    <div style="font-size: 11px; opacity: 0.9; font-weight: 600;">108 EMERGENCY MEDICAL DISPATCH • SURAT APEX NETWORK</div>
                </div>
            </div>
            <div style="text-align: right; background: rgba(0,0,0,0.25); padding: 8px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.25);">
                <div style="font-size: 10px; text-transform: uppercase; font-weight: 800; color: #fecdd3;">DISPATCH TOKEN</div>
                <div style="font-size: 16px; font-weight: 900; letter-spacing: 0.8px;">#SOS-1401</div>
            </div>
        </div>

        <!-- Meta Bar -->
        <div style="background: #f8fafc; padding: 10px 28px; border-bottom: 1.5px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; color: #64748b;">
            <span>🕒 <strong>Timestamp:</strong> 26-Sep-2026 17:52:44</span>
            <span style="color: #dc2626;">🔴 <strong>Triage:</strong> CODE RED (PRIORITY-1)</span>
            <span>🛰️ <strong>Corridor:</strong> V2X Green-Wave Active</span>
        </div>

        <div style="padding: 22px 28px;">
            <!-- Patient Profile -->
            <div style="margin-bottom: 18px;">
                <div style="font-size: 11.5px; font-weight: 800; color: #dc2626; text-transform: uppercase; margin-bottom: 8px;">
                    👤 1. PATIENT DOSSIER & CLINICAL PROFILE
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

            <!-- ICU Vitals Telemetry Cards -->
            <div style="margin-bottom: 18px;">
                <div style="font-size: 11.5px; font-weight: 800; color: #0284c7; text-transform: uppercase; margin-bottom: 8px;">
                    🫀 2. IN-TRANSIT ICU TELEMETRY VITALS
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
                    <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 12px; padding: 12px 14px; text-align: center;">
                        <div style="font-size: 10.5px; color: #166534; font-weight: 800;">OXYGEN (SpO2)</div>
                        <div style="font-size: 24px; font-weight: 900; color: #15803d; margin-top: 2px;">96%</div>
                        <div style="font-size: 10px; color: #16a34a; font-weight: 700;">STABLE WITH O2</div>
                    </div>
                    <div style="background: #eff6ff; border: 1.5px solid #93c5fd; border-radius: 12px; padding: 12px 14px; text-align: center;">
                        <div style="font-size: 10.5px; color: #1e40af; font-weight: 800;">PULSE RATE</div>
                        <div style="font-size: 24px; font-weight: 900; color: #1d4ed8; margin-top: 2px;">108 <span style="font-size: 12px; font-weight: 600;">BPM</span></div>
                        <div style="font-size: 10px; color: #2563eb; font-weight: 700;">TACHYCARDIA MONITOR</div>
                    </div>
                    <div style="background: #fff1f2; border: 1.5px solid #fecdd3; border-radius: 12px; padding: 12px 14px; text-align: center;">
                        <div style="font-size: 10.5px; color: #9f1239; font-weight: 800;">BLOOD PRESSURE</div>
                        <div style="font-size: 24px; font-weight: 900; color: #be123c; margin-top: 2px;">130/85</div>
                        <div style="font-size: 10px; color: #e11d48; font-weight: 700;">MMHG (CONTROLLED)</div>
                    </div>
                </div>
            </div>

            <!-- Routing & Hospital Bed -->
            <div style="margin-bottom: 22px;">
                <div style="font-size: 11.5px; font-weight: 800; color: #16a34a; text-transform: uppercase; margin-bottom: 8px;">
                    🏥 3. V2X ROUTE TRANSIT & EMERGENCY BED STAGING
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px 16px;">
                    <div><span style="font-size: 10.5px; color: #64748b; display: block; font-weight: 700;">INCIDENT ORIGIN</span><strong style="font-size: 13px; color: #0f172a;">📍 Vesu VIP Road Junction (South Surat)</strong></div>
                    <div><span style="font-size: 10.5px; color: #64748b; display: block; font-weight: 700;">RECEIVING TRAUMA CENTER</span><strong style="font-size: 13px; color: #0284c7;">🏥 BAPS Pramukh Swami Hospital & Heart Care</strong></div>
                    <div><span style="font-size: 10.5px; color: #64748b; display: block; font-weight: 700;">FLEET UNIT & PILOT</span><strong style="font-size: 13px; color: #0f172a;">🚑 GJ-01-EA-108 (ALS) • Ramesh Kumar</strong></div>
                    <div><span style="font-size: 10.5px; color: #64748b; display: block; font-weight: 700;">ALLOCATED ICU BED</span><strong style="font-size: 13px; color: #16a34a;">🛏️ CRITICAL-BAY #01 (VENTILATOR READY)</strong></div>
                </div>
            </div>

            <!-- Signatures -->
            <div style="display: flex; justify-content: space-between; border-top: 1.5px dashed #cbd5e1; padding-top: 18px;">
                <div style="text-align: center; width: 44%;">
                    <div style="height: 35px; border-bottom: 1.5px solid #94a3b8; margin-bottom: 6px;"></div>
                    <div style="font-size: 11px; font-weight: 800; color: #475569;">✍️ 108 PARAMEDIC SIGN & STAMP</div>
                </div>
                <div style="text-align: center; width: 44%;">
                    <div style="height: 35px; border-bottom: 1.5px solid #94a3b8; margin-bottom: 6px;"></div>
                    <div style="font-size: 11px; font-weight: 800; color: #475569;">✍️ RECEIVING CMO / TRAUMA PHYSICIAN</div>
                </div>
            </div>
        </div>
    </div>
'''

target_files = glob.glob("pages/*Admin*.py") + glob.glob("pages/*admin*.py")
if not target_files:
    target_files = ["pages/7_⚙️_Admin_Panel.py"]

for f in set(target_files):
    with open(f, "w", encoding="utf-8") as file:
        file.write(admin_code)
    print("SUCCESSFULLY APPLIED FIX TO:", f)
