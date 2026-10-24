file_path = r"pages\7_🏥_Hospital_Admin_Desk.py"

clean_hospital_code = """import streamlit as st
import time

st.set_page_config(page_title="Hospital Admin Desk", page_icon="🏥", layout="wide")

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
st.caption("Surat Municipal Medical Preemption & In-Transit Emergency Intake")

# Top KPI Status Row
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("🚨 Active Codes", "1 Code RED", delta="High Priority", delta_color="inverse")
with c2:
    st.metric("🛏️ ICU Trauma Beds", "4 / 12 Free", delta="2 Reserved")
with c3:
    st.metric("🫀 Cath Lab Status", "Ready (Bay 2)", delta="Sterilized")
with c4:
    st.metric("⏱️ Inbound 108 ETA", "4 Mins", delta="-3 Mins Green Wave")

st.markdown("---")

st.subheader("📋 In-Transit Clinical Handover Dossier")

# Modern Structured Clinical Handover Card
st.markdown('''
<div style="font-family: 'Segoe UI', system-ui, sans-serif; max-width: 860px; margin: 10px auto; background: #ffffff; color: #0f172a; border-radius: 16px; border: 2px solid #e2e8f0; box-shadow: 0 15px 30px rgba(0,0,0,0.25); overflow: hidden;">
    <!-- Header -->
    <div style="background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); padding: 20px 24px; color: #ffffff; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: rgba(255,255,255,0.2); width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 22px;">🚑</div>
            <div>
                <div style="font-size: 18px; font-weight: 900; letter-spacing: 0.5px;">LIFEROUTE CLINICAL HANDOVER SLIP</div>
                <div style="font-size: 11px; opacity: 0.9; font-weight: 600;">108 EMERGENCY MEDICAL DISPATCH • SURAT APEX NETWORK</div>
            </div>
        </div>
        <div style="text-align: right; background: rgba(0,0,0,0.25); padding: 6px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.25);">
            <div style="font-size: 9.5px; text-transform: uppercase; font-weight: 800; color: #fecdd3;">DISPATCH TOKEN</div>
            <div style="font-size: 15px; font-weight: 900; letter-spacing: 0.8px;">#SOS-1401</div>
        </div>
    </div>

    <!-- Meta Details Bar -->
    <div style="background: #f8fafc; padding: 10px 24px; border-bottom: 1.5px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 11.5px; font-weight: 600; color: #64748b;">
        <span>🕒 <strong>Timestamp:</strong> 26-Sep-2026 17:52:44</span>
        <span style="color: #dc2626;">🔴 <strong>Triage Category:</strong> CODE RED (PRIORITY-1)</span>
        <span>🛰️ <strong>Corridor:</strong> V2X Green-Wave Active</span>
    </div>

    <div style="padding: 20px 24px;">
        <!-- Section 1: Patient Profile -->
        <div style="margin-bottom: 16px;">
            <div style="font-size: 11px; font-weight: 800; color: #dc2626; text-transform: uppercase; margin-bottom: 6px;">
                👤 1. PATIENT DOSSIER & CLINICAL PROFILE
            </div>
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 10px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 14px;">
                <div><span style="font-size: 10px; color: #64748b; display: block; font-weight: 700;">PATIENT NAME</span><strong style="font-size: 14px; color: #0f172a;">Payal</strong></div>
                <div><span style="font-size: 10px; color: #64748b; display: block; font-weight: 700;">AGE</span><strong style="font-size: 14px; color: #0f172a;">21 Years</strong></div>
                <div><span style="font-size: 10px; color: #64748b; display: block; font-weight: 700;">BLOOD GROUP</span><strong style="font-size: 14px; color: #dc2626;">B+ (Positive)</strong></div>
                <div style="grid-column: span 3; border-top: 1px dashed #cbd5e1; padding-top: 6px; margin-top: 4px;">
                    <span style="font-size: 10px; color: #64748b; display: block; font-weight: 700;">PRIMARY EMERGENCY CONDITION</span>
                    <strong style="font-size: 13px; color: #b91c1c;">Cardiac Arrest / Sudden Heart Failure (CPR En-Route)</strong>
                </div>
            </div>
        </div>

        <!-- Section 2: Vitals Telemetry -->
        <div style="margin-bottom: 16px;">
            <div style="font-size: 11px; font-weight: 800; color: #0284c7; text-transform: uppercase; margin-bottom: 6px;">
                🫀 2. IN-TRANSIT ICU TELEMETRY VITALS
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 10px; padding: 10px 12px; text-align: center;">
                    <div style="font-size: 10px; color: #166534; font-weight: 800;">OXYGEN (SpO2)</div>
                    <div style="font-size: 22px; font-weight: 900; color: #15803d; margin-top: 2px;">96%</div>
                    <div style="font-size: 9.5px; color: #16a34a; font-weight: 700;">STABLE WITH O2</div>
                </div>
                <div style="background: #eff6ff; border: 1.5px solid #93c5fd; border-radius: 10px; padding: 10px 12px; text-align: center;">
                    <div style="font-size: 10px; color: #1e40af; font-weight: 800;">PULSE RATE</div>
                    <div style="font-size: 22px; font-weight: 900; color: #1d4ed8; margin-top: 2px;">108 <span style="font-size: 11px; font-weight: 600;">BPM</span></div>
                    <div style="font-size: 9.5px; color: #2563eb; font-weight: 700;">TACHYCARDIA</div>
                </div>
                <div style="background: #fff1f2; border: 1.5px solid #fecdd3; border-radius: 10px; padding: 10px 12px; text-align: center;">
                    <div style="font-size: 10px; color: #9f1239; font-weight: 800;">BLOOD PRESSURE</div>
                    <div style="font-size: 22px; font-weight: 900; color: #be123c; margin-top: 2px;">130/85</div>
                    <div style="font-size: 9.5px; color: #e11d48; font-weight: 700;">MMHG</div>
                </div>
            </div>
        </div>

        <!-- Section 3: Transit Routing & Facility -->
        <div style="margin-bottom: 20px;">
            <div style="font-size: 11px; font-weight: 800; color: #16a34a; text-transform: uppercase; margin-bottom: 6px;">
                🏥 3. V2X ROUTE TRANSIT & EMERGENCY BED STAGING
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 14px;">
                <div><span style="font-size: 10px; color: #64748b; display: block; font-weight: 700;">INCIDENT ORIGIN</span><strong style="font-size: 12.5px; color: #0f172a;">📍 Vesu VIP Road Junction (South Surat)</strong></div>
                <div><span style="font-size: 10px; color: #64748b; display: block; font-weight: 700;">RECEIVING FACILITY</span><strong style="font-size: 12.5px; color: #0284c7;">🏥 BAPS Pramukh Swami Hospital & Heart Care</strong></div>
                <div><span style="font-size: 10px; color: #64748b; display: block; font-weight: 700;">FLEET UNIT & PILOT</span><strong style="font-size: 12.5px; color: #0f172a;">🚑 GJ-01-EA-108 (ALS) • Ramesh Kumar</strong></div>
                <div><span style="font-size: 10px; color: #64748b; display: block; font-weight: 700;">ALLOCATED ICU BED</span><strong style="font-size: 12.5px; color: #16a34a;">🛏️ CRITICAL-BAY #01 (VENTILATOR READY)</strong></div>
            </div>
        </div>

        <!-- Section 4: Physical Signatures -->
        <div style="display: flex; justify-content: space-between; border-top: 1.5px dashed #cbd5e1; padding-top: 16px;">
            <div style="text-align: center; width: 44%;">
                <div style="height: 32px; border-bottom: 1.5px solid #94a3b8; margin-bottom: 4px;"></div>
                <div style="font-size: 10.5px; font-weight: 800; color: #475569;">✍️ 108 PARAMEDIC SIGN & STAMP</div>
            </div>
            <div style="text-align: center; width: 44%;">
                <div style="height: 32px; border-bottom: 1.5px solid #94a3b8; margin-bottom: 4px;"></div>
                <div style="font-size: 10.5px; font-weight: 800; color: #475569;">✍️ RECEIVING CMO / TRAUMA PHYSICIAN</div>
            </div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Hospital Readiness Action Bar
col_act1, col_act2 = st.columns(2)
with col_act1:
    if st.button("✅ Confirm Emergency Bed Reservation (Critical Bay #01)", use_container_width=True, type="primary"):
        st.success("CRITICAL BAY #01 Locked for Inbound 108 Unit. Crash cart & Cath lab standby notified.")
with col_act2:
    if st.button("🖨️ Print Official Handover PDF Document", use_container_width=True):
        st.info("Triggered direct thermal/laser print queue for Emergency Reception Desk.")
"""

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(clean_hospital_code)

import py_compile
py_compile.compile(file_path, doraise=True)
print("SUCCESS: pages/7_🏥_Hospital_Admin_Desk.py cleanly compiled with 0 syntax errors!")
