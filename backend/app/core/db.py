"""
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
