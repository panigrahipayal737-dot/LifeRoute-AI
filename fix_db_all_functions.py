import os
import sqlite3

db_dir = os.path.join("backend", "app", "database")
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "traffic_system.db")

# 1. Ensure all tables exist in SQLite
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Dispatch table
cur.execute("""
CREATE TABLE IF NOT EXISTS dispatch_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id TEXT,
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
    driver_contact TEXT,
    corridor_lane TEXT,
    status TEXT
)
""")

# Challans table
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
conn.close()

# 2. Complete db.py code with all required imports & functions
db_code = '''"""
LifeRoute AI - Complete Master Database Engine
Handles Dispatch Records, AI Traffic Challans, and Status Updates
"""
import sqlite3
import os
from datetime import datetime

DB_DIR = os.path.join("backend", "app", "database")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "traffic_system.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dispatch_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id TEXT,
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
        driver_contact TEXT,
        corridor_lane TEXT,
        status TEXT
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
    conn.close()

init_db()

# --- DISPATCH LOG FUNCTIONS ---
def insert_dispatch_record(rec):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO dispatch_records 
    (incident_id, date_stamp, time_stamp, patient_name, patient_age, patient_blood, emergency_type, pickup_location, target_hospital, ambulance_number, driver_name, driver_contact, corridor_lane, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        rec.get("incident_id"), rec.get("date_stamp"), rec.get("time_stamp"),
        rec.get("patient_name"), rec.get("patient_age"), rec.get("patient_blood"),
        rec.get("emergency_type"), rec.get("pickup_location"), rec.get("target_hospital"),
        rec.get("ambulance_number"), rec.get("driver_name"), rec.get("driver_contact"),
        rec.get("corridor_lane"), rec.get("status", "ACTIVE")
    ))
    conn.commit()
    conn.close()

def save_dispatch_record(rec):
    insert_dispatch_record(rec)

def get_latest_active_dispatch():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM dispatch_records ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def update_status(incident_id, status_val):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE dispatch_records SET status = ? WHERE incident_id = ?", (status_val, incident_id))
    conn.commit()
    conn.close()

# --- AI CHALLAN ENGINE FUNCTIONS ---
def insert_challan(challan_dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO challans 
    (challan_id, vehicle_number, violation_type, penalty_amount, location, timestamp, evidence_image, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        challan_dict.get("challan_id", f"CH-{int(datetime.now().timestamp())}"),
        challan_dict.get("vehicle_number", "GJ-05-XX-0000"),
        challan_dict.get("violation_type", "Corridor Obstruction"),
        challan_dict.get("penalty_amount", 1000),
        challan_dict.get("location", "Surat Apex Corridor"),
        challan_dict.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        challan_dict.get("evidence_image", ""),
        challan_dict.get("status", "PENDING")
    ))
    conn.commit()
    conn.close()

def get_all_challans():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM challans ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
'''

with open(os.path.join("backend", "app", "core", "db.py"), "w", encoding="utf-8") as f:
    f.write(db_code)

print("DATABASE CORE RESTORED WITH ALL CHALLAN & DISPATCH FUNCTIONS!")
