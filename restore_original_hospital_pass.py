file_path = r"pages\7_🏥_Hospital_Admin_Desk.py"

original_pass_code = """import streamlit as st
import time

st.set_page_config(page_title="Hospital Admin Desk", page_icon="🏥", layout="wide")

st.title("🏥 Hospital ER & Trauma Apex Command")
st.caption("Surat Municipal Medical Preemption & In-Transit Emergency Intake")

# --- PASSWORD AUTHENTICATION GATEWAY ---
if "hospital_auth" not in st.session_state:
    st.session_state["hospital_auth"] = False

if not st.session_state["hospital_auth"]:
    st.info("🔒 Secure Portal: Authorized ER Doctors & Hospital CMO Access Only")
    with st.form("auth_form"):
        auth_pin = st.text_input("Enter Hospital Reception / Doctor Passcode:", type="password", placeholder="Enter 4-digit PIN")
        submitted = st.form_submit_button("🔓 Authenticate & Access Handover Dossier")
        
        if submitted:
            if auth_pin == "1234" or auth_pin == "108" or auth_pin == "cmo":
                st.session_state["hospital_auth"] = True
                st.success("✅ Access Granted! Loading Active Telemetry & Handover Dossier...")
                st.rerun()
            else:
                st.error("❌ Invalid Passcode. Access Denied.")
    st.stop()

# --- AUTHENTICATED HOSPITAL DASHBOARD ---
st.markdown("---")
col_top1, col_top2 = st.columns([3, 1])
with col_top1:
    st.success("🟢 Authenticated: BAPS Pramukh Swami Heart Care / New Civil ER Desk")
with col_top2:
    if st.button("🚪 Logout Terminal"):
        st.session_state["hospital_auth"] = False
        st.rerun()

# KPI Metric Row
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Active Emergency Token", "#SOS-1401")
kpi2.metric("Inbound Fleet Unit", "GJ-01-EA-108")
kpi3.metric("Allocated Bed", "CRITICAL-BAY #01")
kpi4.metric("Preempted Wave ETA", "4 Mins")

st.markdown("---")
st.subheader("📋 In-Transit Clinical Handover Dossier")

# Original Clean Structured Medical Summary Table
st.markdown('''
<div style="background-color:#ffffff; color:#000000; padding:20px; border-radius:10px; border:2px solid #b91c1c; font-family:sans-serif;">
    <div style="background:#b91c1c; color:#fff; padding:12px; font-weight:bold; font-size:18px; text-align:center; border-radius:6px; margin-bottom:15px;">
        LIFEROUTE - OFFICIAL CLINICAL HANDOVER SLIP<br>
        <span style="font-size:11px; font-weight:normal;">108 GVK-EMRI & SURAT MUNICIPAL TRAUMA APEX NETWORK</span>
    </div>
    
    <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:12px; border-bottom:1px solid #ddd; padding-bottom:6px;">
        <span><strong>Incident Token:</strong> #SOS-1401</span>
        <span><strong>Date / Time:</strong> 26-Sep-2026 17:52:44</span>
    </div>

    <table style="width:100%; border-collapse:collapse; margin-bottom:14px; font-size:13px; color:#111;">
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

    <table style="width:100%; border-collapse:collapse; margin-bottom:14px; font-size:13px; color:#111;">
        <tr style="background:#f1f5f9;"><th colspan="3" style="border:1px solid #cbd5e1; padding:8px; text-align:left;">2. IN-TRANSIT ICU TELEMETRY VITALS</th></tr>
        <tr>
            <td style="border:1px solid #cbd5e1; padding:8px; width:33%;"><strong>SpO2 Level:</strong> 96%</td>
            <td style="border:1px solid #cbd5e1; padding:8px; width:33%;"><strong>Pulse:</strong> 108 BPM</td>
            <td style="border:1px solid #cbd5e1; padding:8px; width:34%;"><strong>Blood Pressure:</strong> 130/85</td>
        </tr>
    </table>

    <table style="width:100%; border-collapse:collapse; margin-bottom:20px; font-size:13px; color:#111;">
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
</div>
''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
c_btn1, c_btn2 = st.columns(2)
with c_btn1:
    if st.button("✅ Confirm Emergency Bed Reservation (Critical Bay #01)", use_container_width=True, type="primary"):
        st.success("Bed reserved and ER Trauma Team notified.")
with c_btn2:
    if st.button("🖨️ Print Clinical Handover Slip", use_container_width=True):
        st.info("Direct thermal/laser slip sent to reception printer.")
"""

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(original_pass_code)

import py_compile
py_compile.compile(file_path, doraise=True)
print("SUCCESS: Original Password-Protected Hospital Admin Desk Restored!")
