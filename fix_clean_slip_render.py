file_path = r"pages\7_🏥_Hospital_Admin_Desk.py"

clean_file_content = """import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hospital Desk", page_icon="🏥", layout="wide")

st.markdown('''
<style>
    .stApp {
        background-color: #0b1329 !important;
        color: #f8fafc;
    }
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
</style>
''', unsafe_allow_html=True)

st.title("🏥 Hospital ER & Trauma Apex Command")
st.caption("Surat Municipal Medical Preemption & In-Transit Clinical Staging")

# --- PASSWORD GATEWAY ---
if "hospital_auth" not in st.session_state:
    st.session_state["hospital_auth"] = False

if not st.session_state["hospital_auth"]:
    st.info("🔒 Secure Doctor & ER Reception Gateway: Authorized Medical Personnel Only")
    with st.form("unified_hospital_auth_form"):
        auth_pin = st.text_input("Enter Hospital Reception / Doctor Passcode:", type="password", placeholder="Enter PIN (e.g. 1234 or 108)")
        submitted = st.form_submit_button("🔓 Authenticate & Access Hospital Desk", use_container_width=True)
        if submitted:
            if auth_pin.strip() in ["1234", "108", "cmo", "hospital"]:
                st.session_state["hospital_auth"] = True
                st.success("✅ Access Granted! Loading Unified Hospital Command...")
                st.rerun()
            else:
                st.error("❌ Invalid Passcode. Access Denied.")
    st.stop()

# --- TOP AUTH BAR ---
c_auth1, c_auth2 = st.columns([3, 1])
with c_auth1:
    st.success("🟢 Authenticated: BAPS Pramukh Swami Heart Care / New Civil ER Command Desk")
with c_auth2:
    if st.button("🚪 Logout Portal", use_container_width=True):
        st.session_state["hospital_auth"] = False
        st.rerun()

# --- TABS ---
tab_er, tab_handover = st.tabs([
    "🏥 Hospital ER Command & Bed Matrix", 
    "📋 Clinical Handover Report & Slip"
])

with tab_er:
    st.markdown("### 🛏️ Live Hospital Capacity & Inbound Telemetry")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("🚨 Active Inbound", "1 Unit (108 ALS)", delta="Critical Red")
    kpi2.metric("🛏️ ICU Trauma Beds", "4 Available", delta="2 Reserved")
    kpi3.metric("🫀 Cath Lab Bay", "Standby Armed", delta="Ready")
    kpi4.metric("⏱️ Green Wave ETA", "4 Mins", delta="-3 Mins Preempted")
    
    st.markdown("---")
    st.markdown("#### ⚡ Emergency Department Rapid Actions")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        if st.button("✅ Lock ICU Critical Bay #01 for Inbound Patient", use_container_width=True, type="primary"):
            st.success("Bed #01 Reserved. Ventilator, crash cart & trauma team placed on active standby.")
    with col_a2:
        if st.button("📢 Broadcast Code Red Alarm to ER Bay", use_container_width=True):
            st.warning("Code Red broadcast sent to all ER monitors and on-duty doctors.")

with tab_handover:
    st.markdown("### 📋 Official In-Transit Handover Dossier")
    
    # Pure Clean HTML (No f-string syntax conflict)
    slip_html = '''
    <div style="background-color:#ffffff; color:#000000; padding:22px; border-radius:10px; border:2px solid #b91c1c; font-family:Arial, sans-serif; max-width:850px; margin:auto;">
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
    </div>
    '''
    
    st.markdown(slip_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🖨️ Print Clinical Handover Slip", use_container_width=True):
        st.info("Direct thermal/laser slip sent to reception printer.")
"""

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(clean_file_content)

import py_compile
py_compile.compile(file_path, doraise=True)
print("SUCCESS: 0 ERRORS! Slip code parsed and compiled cleanly.")
