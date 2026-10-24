import streamlit as st
import pandas as pd
import io
import time
from backend import emergency_db
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Hospital Emergency & Admin Command", page_icon="🏥", layout="wide")

# -------------------------------------------------------------
# VIBRANT SIDEBAR BRAND BADGE & EMERGENCY PULSE RADAR
# -------------------------------------------------------------
with st.sidebar:
    st.markdown('''
    <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%);
                border: 2px solid #38bdf8;
                border-radius: 14px;
                padding: 16px 12px;
                text-align: center;
                margin-top: -30px;
                margin-bottom: 22px;
                box-shadow: 0 0 25px rgba(56, 189, 248, 0.35);">
        <div style="font-size: 32px; filter: drop-shadow(0 0 12px #38bdf8); margin-bottom: 4px;">🚨</div>
        <div style="font-size: 21px; font-weight: 900; letter-spacing: -0.5px; background: linear-gradient(90deg, #38bdf8, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            PulseRoute AI
        </div>
        <div style="display: inline-block; background: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e; color: #4ade80; border-radius: 12px; padding: 3px 10px; font-size: 10px; font-weight: 800; letter-spacing: 0.8px; margin-top: 6px; box-shadow: 0 0 10px rgba(34,197,94,0.3);">
            ● SURAT V2X CORRIDOR ACTIVE
        </div>
        <div style="font-size: 10.5px; color: #94a3b8; font-weight: 600; margin-top: 5px;">
            108 Smart Transit Preemption Hub
        </div>
    </div>
    ''', unsafe_allow_html=True)



# -------------------------------------------------------------
# PROFESSIONAL LIFEROUTE AI SIDEBAR BRAND LOGO & BADGE
# -------------------------------------------------------------
with st.sidebar:
    st.markdown('''
    <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.18) 0%, rgba(99, 102, 241, 0.22) 100%);
                border: 1.5px solid rgba(56, 189, 248, 0.35);
                border-radius: 14px;
                padding: 16px 12px;
                text-align: center;
                margin-bottom: 20px;
                box-shadow: 0 4px 20px rgba(14, 165, 233, 0.2);">
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px;">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 0 10px #38bdf8);">
                <rect width="24" height="24" rx="6" fill="#0284c7"/>
                <path d="M12 4V20M4 12H20" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
                <path d="M7 12H10L11.5 8L13.5 16L15 12H17" stroke="#34d399" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div style="font-size: 19px; font-weight: 900; letter-spacing: -0.3px; color: #f8fafc; font-family: sans-serif;">
            LifeRoute <span style="color: #38bdf8;">AI</span>
        </div>
        <div style="font-size: 10px; font-weight: 800; color: #34d399; letter-spacing: 0.8px; margin-top: 2px;">
            ● V2X GREEN WAVE ONLINE
        </div>
        <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">
            Surat Emergency Traffic Grid
        </div>
    </div>
    ''', unsafe_allow_html=True)




# -------------------------------------------------------------
# ADMIN PASSWORD AUTHENTICATION GATEWAY
# -------------------------------------------------------------
if "hospital_admin_logged_in" not in st.session_state:
    st.session_state["hospital_admin_logged_in"] = False

if not st.session_state["hospital_admin_logged_in"]:
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.9); border: 1.5px solid #0284c7; border-radius: 14px; padding: 24px; max-width: 500px; margin: 40px auto 20px auto; text-align: center;">
        <div style="font-size: 32px; margin-bottom: 10px;">🔒</div>
        <div style="font-size: 18px; font-weight: 800; color: #38bdf8; margin-bottom: 6px;">HOSPITAL ADMIN PORTAL LOCKED</div>
        <div style="font-size: 12px; color: #94a3b8;">Restricted Area: Only Authorized Chief Medical Officers & ER Admins Allowed</div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_mid, col_b = st.columns([1, 1.4, 1])
    with col_mid:
        entered_pass = st.text_input("Enter Hospital Admin Access Key:", type="password", key="hosp_admin_pwd")
        c_btn1, c_btn2 = st.columns([1.2, 1])
        with c_btn1:
            if st.button("🔓 Authenticate & Unlock Desk", use_container_width=True, type="primary"):
                # Default Admin Password: admin108
                if entered_pass == "admin108":
                    st.session_state["hospital_admin_logged_in"] = True
                    st.success("Access Granted! Loading Clinical Handover Desk...")
                    st.rerun()
                else:
                    st.error("❌ Invalid Access Key! Unauthorized attempt logged.")
        with c_btn2:
            st.caption("Default Key: `admin108`")

    st.stop()  # Iske aage ka confidential data load nahi hoga jab tak unlock na ho

# Logged in hone par Logout button top-right me
col_head_l, col_head_r = st.columns([5, 1])
with col_head_r:
    if st.button("🔒 Logout Admin", use_container_width=True):
        st.session_state["hospital_admin_logged_in"] = False
        st.rerun()


st.markdown('''

<style>
    /* Vibrant Gradient Sidebar Background */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070e24 0%, #0a1738 50%, #040918 100%) !important;
        border-right: 1.5px solid rgba(56, 189, 248, 0.25) !important;
        box-shadow: 4px 0 25px rgba(2, 132, 199, 0.15) !important;
    }

    /* Navigation Links Glow & Styling */
    section[data-testid="stSidebar"] ul li {
        margin: 4px 0 !important;
    }

    section[data-testid="stSidebar"] a {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 10px !important;
        padding: 9px 14px !important;
        transition: all 0.25s ease-in-out !important;
        font-weight: 700 !important;
        color: #cbd5e1 !important;
    }

    /* Hover Effect */
    section[data-testid="stSidebar"] a:hover {
        background: linear-gradient(90deg, rgba(14, 165, 233, 0.25), rgba(99, 102, 241, 0.25)) !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
        transform: translateX(4px) !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.35) !important;
    }

    /* Active Page Selected Glow */
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background: linear-gradient(90deg, rgba(2, 132, 199, 0.45), rgba(59, 130, 246, 0.45)) !important;
        border: 1.5px solid #38bdf8 !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5) !important;
    }

    /* Hide Default Boring Streamlit App Heading */
    [data-testid="stSidebarNav"] > div:first-child {
        display: none !important;
    }
</style>

<style>
    .stApp {
        background-color: #060d1d !important;
        color: #f8fafc;
    }
    .header-box {
        background: linear-gradient(90deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.85));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 18px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
    }
    .red-pill {
        background: rgba(225, 29, 72, 0.15);
        color: #f43f5e;
        border: 1px solid #f43f5e;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    
    .header-box {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(99, 102, 241, 0.2) 100%) !important;
        border: 1.5px solid rgba(56, 189, 248, 0.4) !important;
        border-radius: 14px;
        padding: 18px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
    }
    .red-pill {
        background: linear-gradient(135deg, rgba(244, 63, 94, 0.25), rgba(225, 29, 72, 0.4)) !important;
        color: #fda4af !important;
        border: 1.5px solid #f43f5e !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 0.8px;
        box-shadow: 0 0 14px rgba(244, 63, 94, 0.45);
    }
    .glass-card-patient {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.85), rgba(30, 58, 138, 0.3)) !important;
        border: 1.5px solid #38bdf8 !important;
        border-radius: 14px;
        padding: 18px;
        min-height: 195px;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
    }
    .glass-card-telemetry {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.85), rgba(6, 78, 59, 0.35)) !important;
        border: 1.5px solid #22c55e !important;
        border-radius: 14px;
        padding: 18px;
        min-height: 195px;
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.2);
    }
    .glass-card-staged {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.85), rgba(120, 53, 15, 0.3)) !important;
        border: 1.5px solid #f59e0b !important;
        border-radius: 14px;
        padding: 18px;
        min-height: 195px;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.2);
    }
    
.glass-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 16px 20px;
        min-height: 195px;
    }
    .card-title {
        font-size: 10.5px;
        font-weight: 800;
        text-transform: uppercase;
        color: #38bdf8;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
    }
</style>
''', unsafe_allow_html=True)

# Top Bar
st.markdown('''
<div class="header-box">
    <div>
        <div style="font-size: 19px; font-weight: 900; letter-spacing: -0.2px; color: #f8fafc; display: flex; align-items: center; gap: 8px;">
            <span>📄</span> HOSPITAL EMERGENCY INTAKE & CLINICAL HANDOVER DESK
        </div>
        <div style="font-size: 11.5px; color: #94a3b8; margin-top: 4px;">Real-Time Patient Telemetry • 1-Click Handover Sheet • ICU Bed & Cath-Lab Staging</div>
    </div>
    <div class="red-pill">ICU TRAUMA BAY ONLINE</div>
</div>
''', unsafe_allow_html=True)

# Fetch latest synced records
records = emergency_db.load_db()
latest = records[0]

# TABS
tab_hospital, tab_admin, tab_family = st.tabs([
    "🏥 Hospital ER Command & Bed Reservation",
    "📊 Incident Database & Audit Records",
    "📲 Family Clinical Handover & WhatsApp Dispatch"
])

# ----------------- TAB 1: HOSPITAL ER DESK -----------------
with tab_hospital:
    # Live Pre-alert Bar
    st.markdown(f'''
    <div style="background: rgba(6, 78, 59, 0.35); border: 1px solid #059669; border-radius: 8px; padding: 12px 18px; color: #34d399; font-weight: 700; font-size: 13px; margin-bottom: 18px;">
        🚨 INCOMING AMBULANCE PRE-ALERT: {latest.get("Fleet", "GJ-01-EA-108 (ALS)")} (ETA: ~0.05 min) • ORIGIN: {latest.get("Origin")}
    </div>
    ''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'''
        <div class="glass-card-patient">
            <div class="card-title">PATIENT DOSSIER</div>
            <div style="font-size: 22px; font-weight: 900; color: #f8fafc; margin-bottom: 6px;">{latest.get("Patient")}</div>
            <div style="font-size: 12.5px; color: #cbd5e1; line-height: 1.6;">
                <strong>Age:</strong> {latest.get("Age")} years<br>
                <strong>Blood Group:</strong> <span style="color:#f43f5e; font-weight:800;">{latest.get("BloodGroup")}</span><br>
                <span style="color:#f87171; font-weight:600; font-size:11.5px;">{latest.get("Condition")}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        p_val = latest.get("Pulse", "108").replace("BPM","").strip()
        st.markdown(f'''
        <div class="glass-card-patient" style="border-color: rgba(34, 197, 94, 0.35);">
            <div class="card-title" style="color:#4ade80;">LIVE ICU TELEMETRY (ESP32 V2X LINK)</div>
            <div style="display:flex; justify-content:space-around; text-align:center; margin-top:16px;">
                <div>
                    <div style="font-size: 10px; font-weight: 800; color: #94a3b8; text-transform:uppercase;">PULSE</div>
                    <div style="font-size: 26px; font-weight: 900; color: #22c55e;">{p_val} <span style="font-size:12px; font-weight:600;">BPM</span></div>
                </div>
                <div>
                    <div style="font-size: 10px; font-weight: 800; color: #94a3b8; text-transform:uppercase;">SpO2</div>
                    <div style="font-size: 26px; font-weight: 900; color: #38bdf8;">{latest.get("SpO2")}</div>
                </div>
                <div>
                    <div style="font-size: 10px; font-weight: 800; color: #94a3b8; text-transform:uppercase;">BP</div>
                    <div style="font-size: 26px; font-weight: 900; color: #facc15;">{latest.get("BP")}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''
        <div class="glass-card-patient" style="border-color: rgba(234, 179, 8, 0.35);">
            <div class="card-title" style="color:#fbbf24;">STAGED FACILITY & DOCTOR</div>
            <div style="font-size: 13.5px; font-weight: 800; color: #38bdf8; margin-bottom: 4px;">{latest.get("Hospital")}</div>
            <div style="font-size: 12px; color: #e2e8f0; margin-top: 4px;">👨‍⚕️ <strong>{latest.get("Doctor")}</strong></div>
            <div style="font-size: 11px; color: #94a3b8;">Corridor: {latest.get("Corridor")}</div>
            <div style="margin-top: 8px; font-size: 13px; font-weight: 800; color: #22c55e;">
                Reserved Bed: {latest.get("Bed")}
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if not latest.get("BedReserved", False):
        st.warning(f"⚠️ **Inbound Alert:** Ambulance approaching {latest.get('Hospital')}. Dedicated bed reservation needed.")
        if st.button(f"🔴 Confirm & Lock Emergency Bed ({latest.get('Bed')})", use_container_width=True, type="primary"):
            emergency_db.reserve_hospital_bed(latest.get("Token"), latest.get("Bed"))
            st.success("✅ Bed successfully reserved! Trauma team & crash cart armed on standby.")
            st.rerun()
    else:
        st.success(f"🟢 **Bed Secured:** {latest.get('Bed')} is formally locked for {latest.get('Patient')} ({latest.get('Token')}).")

# ----------------- TAB 2: INCIDENT DATABASE & AUDIT RECORDS -----------------
with tab_admin:
    st.markdown("### 🗄️ Master Incident Ledger (All Sync Records)")
    
    total_cnt = len(records)
    active_cnt = sum(1 for r in records if "Active" in r.get("Status", ""))
    resolved_cnt = sum(1 for r in records if "Resolved" in r.get("Status", ""))
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total Incident Dispatches", str(total_cnt))
    col_m2.metric("Active Live Corridors", str(active_cnt), delta="🚨 En-Route", delta_color="inverse")
    col_m3.metric("Resolved Cases Handed Over", str(resolved_cnt), delta="✅ Safe Admission")
    
    st.markdown("---")
    
    # Clean DataFrame representation
    ledger_data = []
    for r in records:
        ledger_data.append({
            "Token": r.get("Token"),
            "Time": r.get("Time"),
            "Patient": r.get("Patient"),
            "Age": r.get("Age"),
            "Blood": r.get("BloodGroup"),
            "Origin (Pickup)": r.get("Origin"),
            "Destination Hospital": r.get("Hospital"),
            "Allocated Bed": r.get("Bed"),
            "Status": r.get("Status")
        })
    df_ledger = pd.DataFrame(ledger_data)
    st.dataframe(df_ledger, use_container_width=True, hide_index=True)

    # Status update controls
    st.markdown("#### 🔄 Update Incident Archive Status")
    cu1, cu2, cu3 = st.columns([2, 2, 1])
    with cu1:
        sel_t = st.selectbox("Select Incident Token:", options=[r["Token"] for r in records], key="admin_sel_tok")
    with cu2:
        new_st = st.selectbox("Status:", ["Active (En-Route)", "Resolved (Handed Over)", "Pending Triaging"], key="admin_new_st")
    with cu3:
        st.write("")
        st.write("")
        if st.button("Apply Update", use_container_width=True, type="primary"):
            emergency_db.update_incident_status(sel_t, new_st)
            st.success(f"Token {sel_t} updated to {new_st}!")
            st.rerun()

# ----------------- TAB 3: FAMILY SHARE & PDF HANDOVER -----------------
with tab_family:
    st.markdown("### 📋 Official Emergency Clinical Handover Sheet")
    
    # Monospace Handover Sheet Text
    handover_text = f"""================================================================================
PULSEROUTE AI • 108 EMERGENCY PATIENT HANDOVER & TRANSFER SLIP
================================================================================
Incident Reference ID : {latest.get('Token')}
Timestamp Dispatched  : 2026-10-12 {latest.get('Time')}
Preemption Status     : 100% V2X GREEN-WAVE CORRIDOR CLEARED

[1] PATIENT PROFILE
--------------------------------------------------------------------------------
Patient Full Name     : {latest.get('Patient')}
Age                   : {latest.get('Age')} Years
Blood Requirement     : {latest.get('BloodGroup')} (Pre-Matched at Blood Bank)
Primary Diagnosis     : {latest.get('Condition')}

[2] EN-ROUTE TELEMETRY (ESP32 IOT STREAM)
--------------------------------------------------------------------------------
Heart Rate / Pulse    : {latest.get('Pulse')}
SpO2 Blood Oxygen     : {latest.get('SpO2')} (Supplemental O2 Staged)
Blood Pressure        : {latest.get('BP')} mmHg

[3] LOGISTICS & RECEIVING FACILITY
--------------------------------------------------------------------------------
Pickup Origin         : {latest.get('Origin')}
Receiving Hospital    : {latest.get('Hospital')}
Attending Physician   : {latest.get('Doctor')}
Reserved Intensive Bed: {latest.get('Bed')}
Ambulance Registration: {latest.get('Fleet')}
Driver & Paramedic    : {latest.get('Pilot')}
"""
    st.code(handover_text, language="text")

    # Native PDF Generator using ReportLab
    def build_handover_pdf(r):
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        elements = []
        styles = getSampleStyleSheet()

        t_head = Table([
            [Paragraph("<b>LIFEROUTE - OFFICIAL CLINICAL HANDOVER SLIP</b>", ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=13, textColor=colors.white, alignment=1))],
            [Paragraph("108 GVK-EMRI & SURAT MUNICIPAL TRAUMA APEX NETWORK", ParagraphStyle('H2', parent=styles['Normal'], fontSize=8.5, textColor=colors.whitesmoke, alignment=1))]
        ], colWidths=[540])
        t_head.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#b91c1c')), ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8)]))
        elements.append(t_head)
        elements.append(Spacer(1, 12))

        meta = Table([[f"Incident Token: {r.get('Token')}", f"Dispatch Time: {r.get('Time')} | Green Wave Active"]], colWidths=[270, 270])
        meta.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9), ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1'))]))
        elements.append(meta)
        elements.append(Spacer(1, 10))

        p_info = [
            ["1. PATIENT PROFILE", "", ""],
            [f"Name: {r.get('Patient')}", f"Age: {r.get('Age')} Years", f"Blood Group: {r.get('BloodGroup')}"],
            [f"Diagnosis: {r.get('Condition')}", "", ""]
        ]
        t_p = Table(p_info, colWidths=[210, 160, 170])
        t_p.setStyle(TableStyle([('SPAN', (0,0), (2,0)), ('SPAN', (0,2), (2,2)), ('BACKGROUND', (0,0), (2,0), colors.HexColor('#f1f5f9')), ('FONTNAME', (0,0), (2,0), 'Helvetica-Bold'), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5)]))
        elements.append(t_p)
        elements.append(Spacer(1, 10))

        v_info = [
            ["2. IN-TRANSIT VITALS (ESP32 TELEMETRY)", "", ""],
            [f"SpO2: {r.get('SpO2')}", f"Pulse: {r.get('Pulse')}", f"BP: {r.get('BP')}"]
        ]
        t_v = Table(v_info, colWidths=[180, 180, 180])
        t_v.setStyle(TableStyle([('SPAN', (0,0), (2,0)), ('BACKGROUND', (0,0), (2,0), colors.HexColor('#f1f5f9')), ('FONTNAME', (0,0), (2,0), 'Helvetica-Bold'), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5)]))
        elements.append(t_v)
        elements.append(Spacer(1, 10))

        log_info = [
            ["3. TRANSIT LOGISTICS & ALLOCATED BED", ""],
            [f"Origin (Pickup): {r.get('Origin')}", f"Destination: {r.get('Hospital')}"],
            [f"Physician: {r.get('Doctor')}", f"Reserved Bed: {r.get('Bed')}"],
            [f"Fleet: {r.get('Fleet')}", f"Driver: {r.get('Pilot')}"]
        ]
        t_log = Table(log_info, colWidths=[270, 270])
        t_log.setStyle(TableStyle([('SPAN', (0,0), (1,0)), ('BACKGROUND', (0,0), (1,0), colors.HexColor('#f1f5f9')), ('FONTNAME', (0,0), (1,0), 'Helvetica-Bold'), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')), ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5)]))
        elements.append(t_log)
        elements.append(Spacer(1, 30))

        sigs = Table([["____________________________", "____________________________"], ["108 Paramedic Sign & Stamp", "Receiving CMO Signature"]], colWidths=[270, 270])
        sigs.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('FONTNAME', (0,1), (-1,-1), 'Helvetica-Bold'), ('FONTSIZE', (0,1), (-1,-1), 9)]))
        elements.append(sigs)

        doc.build(elements)
        buf.seek(0)
        return buf.getvalue()

    pdf_bytes = build_handover_pdf(latest)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            label=f"📥 Download Official PDF Report ({latest.get('Token')})",
            data=pdf_bytes,
            file_name=f"LifeRoute_Report_{latest.get('Token').replace('#','')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
    with col_d2:
        family_msg = f"EMERGENCY+UPDATE:+Ambulance+dispatched+with+{latest.get('Patient')}+from+{latest.get('Origin')}+to+{latest.get('Hospital')}.+Bed+{latest.get('Bed')}+assigned.+Token:+{latest.get('Token')}"
        st.markdown(f'''
        <a href="https://wa.me/?text={family_msg}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#22c55e; color:#ffffff; font-weight:800; font-size:14px; text-align:center; padding:9px 12px; border-radius:8px;">
                📲 Share Live Report to Family via WhatsApp
            </div>
        </a>
        ''', unsafe_allow_html=True)
