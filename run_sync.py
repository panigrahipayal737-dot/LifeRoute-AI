import os, json, time
os.makedirs('backend', exist_ok=True)
backend_code = """import json, os, time
DB_FILE = 'incidents_db.json'
DEFAULT_RECORD = {'Token': '#SOS-2013', 'Time': time.strftime('%H:%M:%S'), 'Patient': 'Pooja Sharma', 'Age': '28', 'BloodGroup': 'B+', 'Condition': 'Severe Multi-Trauma / Neurological Shock', 'SpO2': '96%', 'Pulse': '108 BPM', 'BP': '130/85', 'Origin': 'Majura Gate Chauraha (Central Surat)', 'Hospital': 'SMIMER Medical College & Apex ER (Umarwada)', 'Doctor': 'Dr. Ananya Joshi (Neuro Trauma Surgeon)', 'Fleet': 'GJ-01-EA-108 (ALS)', 'Pilot': 'Ramesh Kumar (+91 98765 43210)', 'Corridor': 'EAST Lane', 'Bed': 'TRAUMA-BAY #02', 'ETA': '3.7 mins', 'Radar': '450m', 'Status': 'Active (En-Route)', 'PreemptionActive': True, 'BedReserved': True}
def load_db():
    if not os.path.exists(DB_FILE):
        save_db([DEFAULT_RECORD])
        return [DEFAULT_RECORD]
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            d = json.load(f)
            return d if isinstance(d, list) and len(d) > 0 else [DEFAULT_RECORD]
    except Exception:
        return [DEFAULT_RECORD]
def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
def get_latest_incident():
    records = load_db()
    for r in records:
        if r.get('PreemptionActive', False) or 'Active' in r.get('Status', ''):
            return r
    return records[0] if records else DEFAULT_RECORD
def update_live_draft_location(new_loc):
    records = load_db()
    if records:
        records[0]['Origin'] = str(new_loc).strip()
        save_db(records)
def add_dispatch(patient, age, bg, condition, spo2, pulse, bp, origin, hospital, fleet='GJ-01-EA-108 (ALS)', pilot='Ramesh Kumar (+91 98765 43210)', doctor='Dr. Specialist', corridor='EAST Lane', bed='TRAUMA-BAY #02', eta='3.7 mins', radar='450m'):
    records = load_db()
    for r in records:
        r['PreemptionActive'] = False
        if 'Active' in r.get('Status', ''):
            r['Status'] = 'Resolved (Handed Over)'
    token_num = 2000 + len(records) + 1
    new_token = f'#SOS-{token_num}'
    entry = {'Token': new_token, 'Time': time.strftime('%H:%M:%S'), 'Patient': str(patient).strip() or 'Emergency Patient', 'Age': str(age).strip() or '28', 'BloodGroup': str(bg).strip() or 'B+', 'Condition': str(condition).strip(), 'SpO2': f'{spo2}%' if '%' not in str(spo2) else str(spo2), 'Pulse': f'{pulse} BPM' if 'BPM' not in str(pulse) else str(pulse), 'BP': str(bp), 'Origin': str(origin).strip() or 'Majura Gate Chauraha (Central Surat)', 'Hospital': str(hospital).strip() or 'SMIMER Medical College & Apex ER (Umarwada)', 'Doctor': str(doctor).strip(), 'Fleet': str(fleet).strip(), 'Pilot': str(pilot).strip(), 'Corridor': str(corridor).strip() or 'EAST Lane', 'Bed': str(bed).strip() or 'TRAUMA-BAY #02', 'ETA': eta, 'Radar': radar, 'Status': 'Active (En-Route)', 'PreemptionActive': True, 'BedReserved': True}
    records.insert(0, entry)
    save_db(records)
    return new_token
create_emergency_dispatch = add_dispatch
def update_incident_status(token, status):
    records = load_db()
    for r in records:
        if r.get('Token') == token:
            r['Status'] = status
            if 'Resolved' in status or 'Normal' in status:
                r['PreemptionActive'] = False
            break
    save_db(records)
"""
open('backend/emergency_db.py', 'w', encoding='utf-8').write(backend_code)
open('emergency_db.py', 'w', encoding='utf-8').write('from backend.emergency_db import *\\n')
active_init = [{'Token': '#SOS-2013', 'Time': time.strftime('%H:%M:%S'), 'Patient': 'Pooja Sharma', 'Age': '28', 'BloodGroup': 'B+', 'Condition': 'Severe Multi-Trauma / Neurological Shock', 'SpO2': '96%', 'Pulse': '108 BPM', 'BP': '130/85', 'Origin': 'Majura Gate Chauraha (Central Surat)', 'Hospital': 'SMIMER Medical College & Apex ER (Umarwada)', 'Doctor': 'Dr. Ananya Joshi (Neuro Trauma Surgeon)', 'Fleet': 'GJ-01-EA-108 (ALS)', 'Pilot': 'Ramesh Kumar (+91 98765 43210)', 'Corridor': 'EAST Lane', 'Bed': 'TRAUMA-BAY #02', 'ETA': '3.7 mins', 'Radar': '450m', 'Status': 'Active (En-Route)', 'PreemptionActive': True, 'BedReserved': True}]
json.dump(active_init, open('incidents_db.json', 'w', encoding='utf-8'), indent=4)
print('>>> DATABASE SYNC SCRIPT CREATED SUCCESSFULLY!')
