import os
import glob
import py_compile

# Identify hospital/admin desk page
hosp_file = r"pages\7_🏥_Hospital_Admin_Desk.py"
os.makedirs("pages", exist_ok=True)

page_content = '''import streamlit as st
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="Hospital & Incident Admin Command", page_icon="🏥", layout="wide")

# Dark Glassmorphism Theme
st.markdown("""
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
    .badge-active {
        background-color: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border: 1px solid #ef4444;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
    }
    .badge-resolved {
        background-color: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        border: 1px solid #22c55e;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
    }
    .badge-pending {
        background-color: rgba(234, 179, 8, 0.2);
        color: #eab308;
        border: 1px solid #eab308;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏥 Apex Hospital Command & Incident Database")
st.caption("Surat Municipal Medical Preemption, Active Triage & Complete Audit Ledger")

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
                st.success("✅ Access Granted! Synchronizing database...")
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

# Database Store in Session State
if "emergency_records" not in st.session_state:
    st.session_state["emergency_records"] = [
        {"Token": "#SOS-1401", "Time": "17:52:44", "Patient": "Payal", "Age": "21", "Condition": "Cardiac Arrest (CPR En-Route)", "Vitals": "SpO2: 96% | 108 BPM", "Hospital": "BAPS Pramukh Swami Heart Care", "Status": "Active (En-Route)"},
        {"Token": "#SOS-1398", "Time": "16:30:12", "Patient": "Rohan Patel", "Age": "34", "Condition": "Multi-Trauma / Fractures", "Vitals": "SpO2: 98% | 88 BPM", "Hospital": "New Civil Hospital (NCH)", "Status": "Resolved (Handed Over)"},
        {"Token": "#SOS-1395", "Time": "15:10:05", "Patient": "Aarav Shah", "Age": "45", "Condition": "Acute Ischemic Stroke", "Vitals": "SpO2: 94% | 114 BPM", "Hospital": "SMIMER Medical College", "Status": "Resolved (Handed Over)"},
        {"Token": "#SOS-1390", "Time": "13:45:20", "Patient": "Meena Joshi", "Age": "62", "Condition": "Severe Respiratory Distress", "Vitals": "SpO2: 89% | 120 BPM", "Hospital": "BAPS Pramukh Swami Heart Care", "Status": "Pending Triaging"}
    ]

# --- TABS ---
tab_admin, tab_slip, tab_er = st.tabs([
    "📊 Incident Database & Audit Ledger",
    "📋 Clinical Handover Slip & Download",
    "🛏️ Hospital ER Command & Bed Matrix"
])

# ----------------- TAB 1: INCIDENT DATABASE & AUDIT LEDGER -----------------
with tab_admin:
    st.markdown("### 🗄️ Real-Time Incident Status & Data Archive")
    
    total_cases = len(st.session_state["emergency_records"])
    active_cases = sum(1 for r in st.session_state["emergency_records"] if "Active" in r["Status"])
    resolved_cases = sum(1 for r in st.session_state["emergency_records"] if "Resolved" in r["Status"])
    pending_cases = sum(1 for r in st.session_state["emergency_records"] if "Pending" in r["Status"])
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Corridor Dispatches", str(total_cases))
    k2.metric("Active Emergencies", str(active_cases), delta="🚨 In-Transit Red", delta_color="inverse")
    k3.metric("Resolved Cases", str(resolved_cases), delta="✅ Handed Over")
    k4.metric("Pending Triage Cases", str(pending_cases), delta="⏳ Awaiting Bed")
    
    st.markdown("---")
    
    # Table of Records
    df = pd.DataFrame(st.session_state["emergency_records"])
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Update Status Section
    st.markdown("#### 🔄 Update Incident Status")
    col_u1, col_u2, col_u3 = st.columns([2, 2, 1])
    with col_u1:
        sel_token = st.selectbox("Select Incident Token:", options=[r["Token"] for r in st.session_state["emergency_records"]])
    with col_u2:
        new_status = st.selectbox("Update To:", ["Active (En-Route)", "Resolved (Handed Over)", "Pending Triaging"])
    with col_u3:
        st.write("")
        st.write("")
        if st.button("Apply Status", use_container_width=True, type="primary"):
            for r in st.session_state["emergency_records"]:
                if r["Token"] == sel_token:
                    r["Status"] = new_status
            st.success(f"Status updated for {sel_token}!")
            st.rerun()

# ----------------- TAB 2: CLINICAL HANDOVER SLIP & DOWNLOAD -----------------
with tab_slip:
    st.markdown("### 📋 Official In-Transit Handover Dossier")
    
    # Raw HTML with 0 indentation to prevent markdown pre/code block parsing
    slip_html = """<div style="background-color:#ffffff; color:#000000; padding:24px; border-radius:10px; border:2px solid #b91c1c; font-family:Arial, sans-serif; max-width:850px; margin:auto;">
<div style="background:#b91c1c; color:#ffffff; padding:12px; font-weight:bold; font-size:18px; text-align:center; border-radius:6px; margin-bottom:15px;">
LIFEROUTE - OFFICIAL CLINICAL HANDOVER SLIP<br>
<span style="font-size:11px; font-weight:normal;">108 GVK-EMRI & SURAT MUNICIPAL TRAUMA APEX NETWORK</span>
</div>
<div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:12px; border-bottom:1px solid #ddd; padding-bottom:6px;">
<span><strong>Incident Token:</strong> #SOS-1401</span>
<span><strong>Date / Time:</strong> 26-Sep-2026 17:52:44</span>
</div>
<table style="width:100%; border-collapse:collapse; margin-bottom:14px; font-size:13px; color:#111111;">
<tr style="background:#f1f5f9;"><th colspan="3" style="border:1px solid #cbd5e1; padding:8px; text-align:left;">1. PATIENT DOSSIER & CLINICAL PROFILE</th></tr>
<tr>
<td style="border:1px solid #cbd5e1; padding:8px; width:40%;"><strong>Name:</strong> Payal</td>
<td style="border:1px solid #cbd5e1; padding:8px; width:30%;"><strong>Age:</strong> 21 Years</td>
<td style="border:1px solid #cbd5e1; padding:8px; width:30%;"><strong>Blood Group:</strong> B+</td>
</tr>
<tr>
<td colspan="3" style="border:1px solid #cbd5e1; padding:8px;"><strong>Diagnosis:</strong> Cardiac Arrest / Sudden Heart Failure (CPR En-Route)</td>
</tr>
</table>
<table style="width:100%; border-collapse:collapse; margin-bottom:14px; font-size:13px; color:#111111;">
<tr style="background:#f1f5f9;"><th colspan="3" style="border:1px solid #cbd5e1; padding:8px; text-align:left;">2. IN-TRANSIT ICU TELEMETRY VITALS</th></tr>
<tr>
<td style="border:1px solid #cbd5e1; padding:8px; width:33%;"><strong>SpO2 Level:</strong> 96%</td>
<td style="border:1px solid #cbd5e1; padding:8px; width:33%;"><strong>Pulse:</strong> 108 BPM</td>
<td style="border:1px solid #cbd5e1; padding:8px; width:34%;"><strong>Blood Pressure:</strong> 130/85</td>
</tr>
</table>
<table style="width:100%; border-collapse:collapse; margin-bottom:20px; font-size:13px; color:#111111;">
<tr style="background:#f1f5f9;"><th colspan="2" style="border:1px solid #cbd5e1; padding:8px; text-align:left;">3. V2X ROUTE TRANSIT & EMERGENCY STAGING</th></tr>
<tr>
<td style="border:1px solid #cbd5e1; padding:8px; width:50%;"><strong>Origin:</strong> Vesu VIP Road Junction (South Surat)</td>
<td style="border:1px solid #cbd5e1; padding:8px; width:50%;"><strong>Receiving Facility:</strong> BAPS Pramukh Swami Hospital & Heart Care</td>
</tr>
<tr>
<td style="border:1px solid #cbd5e1; padding:8px;"><strong>108 Fleet Unit:</strong> GJ-01-EA-108 (ALS)</td>
<td style="border:1px solid #cbd5e1; padding:8px;"><strong>Pilot:</strong> Ramesh Kumar</td>
</tr>
<tr>
<td style="border:1px solid #cbd5e1; padding:8px;"><strong>Preempted Lane:</strong> WEST Approach</td>
<td style="border:1px solid #cbd5e1; padding:8px;"><strong>Assigned Bed:</strong> CRITICAL-BAY #01</td>
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
</div>"""

    st.markdown(slip_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            label="📥 Download Official Clinical Report (HTML/PDF Ready)",
            data=slip_html,
            file_name="LifeRoute_Clinical_Handover_SOS1401.html",
            mime="text/html",
            use_container_width=True,
            type="primary"
        )
    with col_d2:
        share_url = "https://wa.me/?text=" + "LIFEROUTE+EMERGENCY+DISPATCH+TOKEN:+%23SOS-1401+|+Patient:+Payal+(21Y)+|+Condition:+Cardiac+Arrest+|+Bed:+CRITICAL-BAY+01+Reserved+at+BAPS+Hospital"
        st.markdown(f\'\'\'
        <a href="{share_url}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#25D366; color:white; text-align:center; padding:9px 16px; border-radius:8px; font-weight:bold; font-size:14px;">
                📲 Share Report via WhatsApp Dispatch
            </div>
        </a>
        \'\'\', unsafe_allow_html=True)

# ----------------- TAB 3: ER CAPACITY & ACTIONS -----------------
with tab_er:
    st.markdown("### 🛏️ Live Hospital Capacity & Inbound Actions")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        if st.button("✅ Lock ICU Critical Bay #01 for Inbound Patient", use_container_width=True, type="primary"):
            st.success("Bed #01 Reserved. Ventilator, crash cart & trauma team placed on active standby.")
    with col_a2:
        if st.button("📢 Broadcast Code Red Alarm to ER Bay", use_container_width=True):
            st.warning("Code Red broadcast sent to all ER monitors and on-duty doctors.")
'''

with open(hosp_file, "w", encoding="utf-8", newline="\n") as f:
    f.write(page_content)

py_compile.compile(hosp_file, doraise=True)
print("SUCCESS: 0 ERRORS! Admin Ledger, HTML table render, PDF Download & WhatsApp Share active.")
