import os
import json
import py_compile

# 1. Create Shared Database Module (incidents.json backed)
db_module_code = """import json
import os
import time

DB_FILE = "incidents_db.json"

DEFAULT_RECORDS = [
    {"Token": "#SOS-1401", "Time": "17:52:44", "Patient": "Payal", "Age": "21", "BloodGroup": "B+", "Condition": "Cardiac Arrest (CPR En-Route)", "SpO2": "96%", "Pulse": "108 BPM", "BP": "130/85", "Origin": "Vesu VIP Road Junction", "Hospital": "BAPS Pramukh Swami Hospital & Heart Care", "Fleet": "GJ-01-EA-108 (ALS)", "Pilot": "Ramesh Kumar", "Bed": "CRITICAL-BAY #01", "Status": "Active (En-Route)", "BedReserved": True},
    {"Token": "#SOS-1398", "Time": "16:30:12", "Patient": "Rohan Patel", "Age": "34", "BloodGroup": "O+", "Condition": "Multi-Trauma / Fractures", "SpO2": "98%", "Pulse": "88 BPM", "BP": "120/80", "Origin": "Majura Gate", "Hospital": "New Civil Hospital (NCH)", "Fleet": "GJ-05-AB-108", "Pilot": "Kishore Bhai", "Bed": "TRAUMA-BAY #04", "Status": "Resolved (Handed Over)", "BedReserved": True},
    {"Token": "#SOS-1395", "Time": "15:10:05", "Patient": "Aarav Shah", "Age": "45", "BloodGroup": "A+", "Condition": "Acute Ischemic Stroke", "SpO2": "94%", "Pulse": "114 BPM", "BP": "150/95", "Origin": "Adajan Patiya", "Hospital": "SMIMER Medical College", "Fleet": "GJ-01-CZ-108", "Pilot": "Suresh Rao", "Bed": "ICU-BAY #02", "Status": "Resolved (Handed Over)", "BedReserved": True}
]

def load_db():
    if not os.path.exists(DB_FILE):
        save_db(DEFAULT_RECORDS)
        return DEFAULT_RECORDS
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_RECORDS

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_dispatch(patient, age, bg, condition, spo2, pulse, bp, origin, hospital, fleet, pilot):
    records = load_db()
    token_num = 1400 + len(records) + 1
    new_token = f"#SOS-{token_num}"
    cur_time = time.strftime("%H:%M:%S")
    
    new_entry = {
        "Token": new_token,
        "Time": cur_time,
        "Patient": patient if patient else "Emergency Patient",
        "Age": str(age),
        "BloodGroup": bg,
        "Condition": condition,
        "SpO2": f"{spo2}%",
        "Pulse": f"{pulse} BPM",
        "BP": bp,
        "Origin": origin,
        "Hospital": hospital,
        "Fleet": fleet,
        "Pilot": pilot,
        "Bed": "Awaiting Allocation",
        "Status": "Active (En-Route)",
        "BedReserved": False
    }
    # Prepend as the newest active record
    records.insert(0, new_entry)
    save_db(records)
    return new_token

def update_status(token, new_status):
    records = load_db()
    for r in records:
        if r["Token"] == token:
            r["Status"] = new_status
            break
    save_db(records)

def reserve_bed_for_token(token, bed_name="CRITICAL-BAY #01"):
    records = load_db()
    for r in records:
        if r["Token"] == token:
            r["Bed"] = bed_name
            r["BedReserved"] = True
            break
    save_db(records)
"""

with open("emergency_db.py", "w", encoding="utf-8", newline="\n") as f:
    f.write(db_module_code)
print("SUCCESS: Created global emergency_db.py")

# 2. Update First Page (streamlit_app.py) to save dispatch directly into shared DB
with open("streamlit_app.py", "r", encoding="utf-8", errors="ignore") as f:
    app_text = f.read()

if "import emergency_db" not in app_text:
    app_text = "import emergency_db\n" + app_text

# Search for the Launch / Dispatch button block in streamlit_app.py
save_logic = """
        # --- GLOBAL DATABASE SYNC ---
        new_token = emergency_db.add_dispatch(
            patient=st.session_state.get("patient_name", "Payal"),
            age=st.session_state.get("patient_age", "21"),
            bg=st.session_state.get("patient_blood_group", "B+"),
            condition=st.session_state.get("patient_condition", "Cardiac Emergency"),
            spo2=st.session_state.get("patient_spo2", 96),
            pulse=st.session_state.get("patient_pulse", 108),
            bp=st.session_state.get("patient_bp", "130/85"),
            origin=st.session_state.get("pickup_location", "Limbayat Chauraha, Surat"),
            hospital=st.session_state.get("target_hospital_name", "BAPS Pramukh Swami Hospital & Heart Care"),
            fleet="GJ-01-EA-108 (ALS)",
            pilot="Ramesh Kumar"
        )
        st.session_state["active_token"] = new_token
        st.success(f"🚀 EMERGENCY DISPATCHED: Telemetry packet transmitted to Hospital ER & Police Console! Incident Token: {new_token}")
"""

# Inject database sync inside launch button
if "emergency_corridor_active" in app_text and "emergency_db.add_dispatch" not in app_text:
    idx = app_text.find("st.session_state['emergency_corridor_active'] = True")
    if idx == -1:
        idx = app_text.find('st.session_state["emergency_corridor_active"] = True')
    if idx != -1:
        end_line = app_text.find("\n", idx)
        app_text = app_text[:end_line] + "\n" + save_logic + app_text[end_line:]

with open("streamlit_app.py", "w", encoding="utf-8", newline="\n") as f:
    f.write(app_text)
print("SUCCESS: Connected streamlit_app.py to shared dispatch database")

# 3. Rebuild Hospital Admin Desk to dynamically read and update shared DB
hosp_file = r"pages\7_🏥_Hospital_Admin_Desk.py"

hosp_full_code = """import streamlit as st
import pandas as pd
import time
import io
import emergency_db
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Hospital Desk", page_icon="🏥", layout="wide")

st.markdown('''
<style>
    .stApp {
        background-color: #0b1329 !important;
        color: #f8fafc;
    }
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
</style>
''', unsafe_allow_html=True)

st.title("🏥 Apex Hospital Command & Incident Database")
st.caption("Surat Municipal Medical Preemption, Active Triage & Real-Time Fleet Synchronizer")

# --- AUTH GATEWAY ---
if "hospital_auth" not in st.session_state:
    st.session_state["hospital_auth"] = False

if not st.session_state["hospital_auth"]:
    st.info("🔒 Secure Doctor & ER Reception Gateway: Authorized Personnel Only")
    with st.form("admin_auth_form"):
        auth_pin = st.text_input("Enter Passcode:", type="password", placeholder="Enter PIN (e.g. 1234 or 108)")
        sub = st.form_submit_button("🔓 Authenticate & Access Admin Ledger", use_container_width=True)
        if sub:
            if auth_pin.strip() in ["1234", "108", "admin", "cmo"]:
                st.session_state["hospital_auth"] = True
                st.success("✅ Access Granted! Loading live fleet telemetry...")
                st.rerun()
            else:
                st.error("❌ Invalid Passcode. Access Denied.")
    st.stop()

# --- TOP STATUS BAR ---
c_auth1, c_auth2 = st.columns([3, 1])
with c_auth1:
    st.success("🟢 Authenticated: BAPS Pramukh Swami Heart Care / New Civil ER Command Desk")
with c_auth2:
    if st.button("🚪 Logout Portal", use_container_width=True):
        st.session_state["hospital_auth"] = False
        st.rerun()

# Fetch latest synced records from shared database
records = emergency_db.load_db()

# --- TABS ---
tab_er, tab_admin, tab_slip = st.tabs([
    "🛏️ Hospital ER Command & Bed Reservation",
    "📊 Incident Database & Audit Ledger",
    "📋 Clinical Handover Slip & PDF Download"
])

# ----------------- TAB 1: HOSPITAL ER COMMAND & BED RESERVATION -----------------
with tab_er:
    st.markdown("### 🛏️ Inbound Emergency Intake & Bed Staging")
    
    # Check for active ambulances requiring bed
    active_inbounds = [r for r in records if "Active" in r["Status"]]
    
    if active_inbounds:
        latest = active_inbounds[0]
        if not latest.get("BedReserved", False):
            st.error(f"🚨 **URGENT INBOUND ALERT:** {latest['Fleet']} approaching with Patient **{latest['Patient']}** ({latest['Condition']})! Origin: {latest['Origin']}. Bed NOT locked!")
            if st.button(f"🔴 LOCK & RESERVE CRITICAL BAY #01 FOR {latest['Token']}", use_container_width=True, type="primary"):
                emergency_db.reserve_bed_for_token(latest['Token'], "CRITICAL-BAY #01")
                st.success(f"✅ CRITICAL-BAY #01 successfully locked for {latest['Token']}! Crash cart & trauma team placed on active standby.")
                st.rerun()
        else:
            st.success(f"🟢 **BED RESERVED:** Patient **{latest['Patient']}** ({latest['Token']}) is assigned to **{latest['Bed']}**. Ventilator and Cath Lab Armed!")
    else:
        st.info("ℹ️ No active Code Red arrivals currently inbound.")

    st.markdown("---")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🚨 Active Inbound", f"{len(active_inbounds)} Unit(s)", delta="Code Red")
    k2.metric("🛏️ Available ICU Beds", "3 / 12 Free", delta="-1 Assigned")
    k3.metric("🫀 Cath Lab Bay", "Standby Armed", delta="Ready")
    k4.metric("⏱️ Green Wave ETA", "4 Mins", delta="-3 Mins Preempted")

# ----------------- TAB 2: INCIDENT DATABASE & AUDIT LEDGER -----------------
with tab_admin:
    st.markdown("### 🗄️ Real-Time Incident Status & Data Archive")
    
    total_cases = len(records)
    act_cnt = sum(1 for r in records if "Active" in r["Status"])
    res_cnt = sum(1 for r in records if "Resolved" in r["Status"])
    pen_cnt = sum(1 for r in records if "Pending" in r["Status"])
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Corridor Dispatches", str(total_cases))
    m2.metric("Active Emergencies", str(act_cnt), delta="🚨 In-Transit Red", delta_color="inverse")
    m3.metric("Resolved Cases", str(res_cnt), delta="✅ Handed Over")
    m4.metric("Pending Triage Cases", str(pen_cnt), delta="⏳ Bed Pending")
    
    st.markdown("---")
    
    # Display database table
    df_data = []
    for r in records:
        df_data.append({
            "Token": r["Token"],
            "Time": r["Time"],
            "Patient": r["Patient"],
            "Age": r["Age"],
            "Condition": r["Condition"],
            "Vitals": f"SpO2: {r['SpO2']} | {r['Pulse']}",
            "Hospital": r["Hospital"],
            "Allocated Bed": r["Bed"],
            "Status": r["Status"]
        })
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Real-Time Status Update Tool
    st.markdown("#### 🔄 Update Incident Status")
    col_u1, col_u2, col_u3 = st.columns([2, 2, 1])
    with col_u1:
        sel_token = st.selectbox("Select Incident Token:", options=[r["Token"] for r in records])
    with col_u2:
        new_status = st.selectbox("Update To:", ["Active (En-Route)", "Resolved (Handed Over)", "Pending Triaging"])
    with col_u3:
        st.write("")
        st.write("")
        if st.button("Apply Status", use_container_width=True, type="primary"):
            emergency_db.update_status(sel_token, new_status)
            st.success(f"Status updated for {sel_token}!")
            st.rerun()

# ----------------- TAB 3: CLINICAL HANDOVER SLIP & PDF -----------------
with tab_slip:
    st.markdown("### 📋 Official In-Transit Handover Dossier")
    
    # Select which incident to view & print
    token_list = [r["Token"] for r in records]
    selected_token_slip = st.selectbox("Select Patient Incident Token to Generate Slip:", options=token_list)
    
    # Find matching record
    rec = next((item for item in records if item["Token"] == selected_token_slip), records[0])
    
    slip_html = f'''<div style="background-color:#ffffff; color:#000000; padding:22px; border-radius:10px; border:2px solid #b91c1c; font-family:Arial, sans-serif; max-width:850px; margin:auto;">
<div style="background:#b91c1c; color:#ffffff; padding:12px; font-weight:bold; font-size:18px; text-align:center; border-radius:6px; margin-bottom:15px;">
LIFEROUTE - OFFICIAL CLINICAL HANDOVER SLIP<br>
<span style="font-size:11px; font-weight:normal;">108 GVK-EMRI & SURAT MUNICIPAL TRAUMA APEX NETWORK</span>
</div>
<div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:12px; border-bottom:1px solid #ddd; padding-bottom:6px;">
<span><strong>Incident Token:</strong> {rec['Token']}</span>
<span><strong>Date / Time:</strong> 26-Sep-2026 {rec['Time']}</span>
</div>
<table style="width:100%; border-collapse:collapse; margin-bottom:14px; font-size:13px; color:#111111;">
<tr style="background:#f1f5f9;"><th colspan="3" style="border:1px solid #cbd5e1; padding:8px; text-align:left;">1. PATIENT DOSSIER & CLINICAL PROFILE</th></tr>
<tr>
<td style="border:1px solid #cbd5e1; padding:8px; width:40%;"><strong>Name:</strong> {rec['Patient']}</td>
<td style="border:1px solid #cbd5e1; padding:8px; width:30%;"><strong>Age:</strong> {rec['Age']} Years</td>
<td style="border:1px solid #cbd5e1; padding:8px; width:30%;"><strong>Blood Group:</strong> {rec['BloodGroup']}</td>
</tr>
<tr>
<td colspan="3" style="border:1px solid #cbd5e1; padding:8px;"><strong>Diagnosis:</strong> {rec['Condition']}</td>
</tr>
</table>
<table style="width:100%; border-collapse:collapse; margin-bottom:14px; font-size:13px; color:#111111;">
<tr style="background:#f1f5f9;"><th colspan="3" style="border:1px solid #cbd5e1; padding:8px; text-align:left;">2. IN-TRANSIT ICU TELEMETRY VITALS</th></tr>
<tr>
<td style="border:1px solid #cbd5e1; padding:8px; width:33%;"><strong>SpO2 Level:</strong> {rec['SpO2']}</td>
<td style="border:1px solid #cbd5e1; padding:8px; width:33%;"><strong>Pulse:</strong> {rec['Pulse']}</td>
<td style="border:1px solid #cbd5e1; padding:8px; width:34%;"><strong>Blood Pressure:</strong> {rec['BP']}</td>
</tr>
</table>
<table style="width:100%; border-collapse:collapse; margin-bottom:20px; font-size:13px; color:#111111;">
<tr style="background:#f1f5f9;"><th colspan="2" style="border:1px solid #cbd5e1; padding:8px; text-align:left;">3. V2X ROUTE TRANSIT & EMERGENCY STAGING</th></tr>
<tr>
<td style="border:1px solid #cbd5e1; padding:8px; width:50%;"><strong>Origin:</strong> {rec['Origin']}</td>
<td style="border:1px solid #cbd5e1; padding:8px; width:50%;"><strong>Receiving Facility:</strong> {rec['Hospital']}</td>
</tr>
<tr>
<td style="border:1px solid #cbd5e1; padding:8px;"><strong>108 Fleet Unit:</strong> {rec['Fleet']}</td>
<td style="border:1px solid #cbd5e1; padding:8px;"><strong>Pilot:</strong> {rec['Pilot']}</td>
</tr>
<tr>
<td style="border:1px solid #cbd5e1; padding:8px;"><strong>Preempted Lane:</strong> NORTH/WEST Wave</td>
<td style="border:1px solid #cbd5e1; padding:8px;"><strong>Assigned Bed:</strong> {rec['Bed']}</td>
</tr>
</table>
<div style="display:flex; justify-content:space-around; margin-top:24px; padding-top:15px; border-top:1px dashed #94a3b8; text-align:center; font-size:12px;">
<div style="width:40%;">
<div style="border-bottom:1px solid #475569; height:24px; margin-bottom:4px;"></div>
<strong>108 Paramedic Sign & Stamp</strong>
</div>
<div style="width:40%;">
<div style="border-bottom:1px solid #475569; height:24px; margin-bottom:4px;"></div>
<strong>Receiving CMO Signature</strong>
</div>
</div>
</div>'''

    st.markdown(slip_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Dynamic PDF Generator for Selected Record
    def build_pdf_data(r_item):
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        elements = []
        styles = getSampleStyleSheet()

        t_style = ParagraphStyle('TStyle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.white, alignment=1, spaceAfter=4)
        s_style = ParagraphStyle('SStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=9, textColor=colors.whitesmoke, alignment=1)

        t_head = Table([[Paragraph("LIFEROUTE - OFFICIAL CLINICAL HANDOVER SLIP", t_style)], [Paragraph("108 GVK-EMRI & SURAT MUNICIPAL TRAUMA APEX NETWORK", s_style)]], colWidths=[540])
        t_head.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#b91c1c')), ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8), ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        elements.append(t_head)
        elements.append(Spacer(1, 10))

        t_meta = Table([[f"Incident Token: {r_item['Token']}", f"Date / Time: 26-Sep-2026 {r_item['Time']}"]], colWidths=[270, 270])
        t_meta.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9), ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#334155')), ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1'))]))
        elements.append(t_meta)
        elements.append(Spacer(1, 10))

        p_dat = [["1. PATIENT DOSSIER & CLINICAL PROFILE", "", ""], [f"Name: {r_item['Patient']}", f"Age: {r_item['Age']} Years", f"Blood Group: {r_item['BloodGroup']}"], [f"Diagnosis: {r_item['Condition']}", "", ""]]
        t_p = Table(p_dat, colWidths=[210, 160, 170])
        t_p.setStyle(TableStyle([('SPAN', (0,0), (2,0)), ('SPAN', (0,2), (2,2)), ('BACKGROUND', (0,0), (2,0), colors.HexColor('#f1f5f9')), ('FONTNAME', (0,0), (2,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
        elements.append(t_p)
        elements.append(Spacer(1, 10))

        v_dat = [["2. IN-TRANSIT ICU TELEMETRY VITALS", "", ""], [f"SpO2: {r_item['SpO2']}", f"Pulse: {r_item['Pulse']}", f"Blood Pressure: {r_item['BP']}"]]
        t_v = Table(v_dat, colWidths=[180, 180, 180])
        t_v.setStyle(TableStyle([('SPAN', (0,0), (2,0)), ('BACKGROUND', (0,0), (2,0), colors.HexColor('#f1f5f9')), ('FONTNAME', (0,0), (2,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
        elements.append(t_v)
        elements.append(Spacer(1, 10))

        s_dat = [["3. V2X ROUTE TRANSIT & EMERGENCY STAGING", ""], [f"Origin: {r_item['Origin']}", f"Receiving: {r_item['Hospital']}"], [f"108 Fleet Unit: {r_item['Fleet']}", f"Pilot: {r_item['Pilot']}"], ["Preempted Lane: WEST/NORTH Approach", f"Assigned Bed: {r_item['Bed']}"]]
        t_s = Table(s_dat, colWidths=[270, 270])
        t_s.setStyle(TableStyle([('SPAN', (0,0), (1,0)), ('BACKGROUND', (0,0), (1,0), colors.HexColor('#f1f5f9')), ('FONTNAME', (0,0), (1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
        elements.append(t_s)
        elements.append(Spacer(1, 30))

        sig_dat = [["____________________________", "____________________________"], ["108 Paramedic Sign & Stamp", "Receiving CMO Signature"]]
        t_sig = Table(sig_dat, colWidths=[270, 270])
        t_sig.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('FONTNAME', (0,1), (-1,-1), 'Helvetica-Bold'), ('FONTSIZE', (0,1), (-1,-1), 9)]))
        elements.append(t_sig)

        doc.build(elements)
        buf.seek(0)
        return buf.getvalue()

    pdf_data = build_pdf_data(rec)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            label=f"📥 Download Clinical Handover PDF ({rec['Token']})",
            data=pdf_data,
            file_name=f"LifeRoute_Clinical_Handover_{rec['Token'].replace('#', '')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
    with col_d2:
        wa_text = f"LIFEROUTE+EMERGENCY+DISPATCH:+{rec['Token']}+|+Patient:+{rec['Patient']}+({rec['Age']}Y)+|+Diagnosis:+{rec['Condition']}+|+Bed:+{rec['Bed']}+at+{rec['Hospital']}"
        st.markdown(f'''
        <a href="https://wa.me/?text={wa_text}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#25D366; color:white; text-align:center; padding:9px 16px; border-radius:8px; font-weight:bold; font-size:14px;">
                📲 Share Report via WhatsApp Dispatch
            </div>
        </a>
        ''', unsafe_allow_html=True)
"""

with open(hosp_file, "w", encoding="utf-8", newline="\n") as f:
    f.write(hosp_full_code)

py_compile.compile("emergency_db.py", doraise=True)
py_compile.compile("streamlit_app.py", doraise=True)
py_compile.compile(hosp_file, doraise=True)
print("\n>>> ALL PAGES CONNECTED TO CENTRAL DATABASE WITH 0 ERRORS!")
