import streamlit as st
import pandas as pd
import time
from backend import emergency_db

st.set_page_config(page_title="AI Challan Engine", page_icon="📋", layout="wide")

st.markdown('''
<style>
    .stApp { background: radial-gradient(circle at 15% 15%, #0a1128 0%, #050814 100%) !important; color: #f8fafc !important; }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #070e24 0%, #0a1738 50%, #040918 100%) !important; border-right: 1.5px solid rgba(56, 189, 248, 0.3) !important; }
    section[data-testid="stSidebar"] a { background: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-radius: 10px !important; padding: 9px 14px !important; margin: 4px 0 !important; font-weight: 700 !important; color: #cbd5e1 !important; }
    section[data-testid="stSidebar"] a[aria-current="page"] { background: linear-gradient(90deg, rgba(2, 132, 199, 0.5), rgba(59, 130, 246, 0.5)) !important; border: 1.5px solid #38bdf8 !important; color: #ffffff !important; }
    [data-testid="stSidebarNav"] > div:first-child { display: none !important; }
</style>
''', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('''
    <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%); border: 2px solid #38bdf8; border-radius: 14px; padding: 16px 12px; text-align: center; margin-top: -30px; margin-bottom: 22px;">
        <div style="font-size: 32px; margin-bottom: 4px;">🚨</div>
        <div style="font-size: 21px; font-weight: 900; background: linear-gradient(90deg, #38bdf8, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            PulseRoute AI
        </div>
        <div style="display: inline-block; background: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e; color: #4ade80; border-radius: 12px; padding: 3px 10px; font-size: 10px; font-weight: 800; margin-top: 6px;">
            ● SURAT V2X CORRIDOR ACTIVE
        </div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('''
<div style="background: linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border: 1.5px solid rgba(244,63,94,0.4); border-radius:14px; padding:18px 24px; display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
    <div>
        <div style="font-size: 20px; font-weight: 900; color: #fda4af; display:flex; align-items:center; gap:8px;">
            <span>📋</span> AI AUTOMATED E-CHALLAN DISPATCH ENGINE
        </div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Motor Vehicles Act Section 194E • Non-Yielding to Emergency Vehicles Violation</div>
    </div>
    <div style="background:rgba(225,29,72,0.2); color:#fda4af; border:1.5px solid #f43f5e; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:900;">
        ENFORCEMENT ACTIVE
    </div>
</div>
''', unsafe_allow_html=True)

col_u, col_res = st.columns([1.2, 1.8])

with col_u:
    st.markdown("#### 📷 Optical Violation Feed")
    uploaded_v = st.file_uploader("Upload Traffic CCTV Frame for OCR Scan", type=["jpg", "jpeg", "png"], key="challan_uploader")
    demo_plates = ["GJ-05-AB-4921 (White Swift)", "GJ-01-KR-9902 (Creta SUV)", "GJ-27-E-1120 (City Bus)"]
    sel_plate = st.selectbox("Or Select Detected Vehicle from CCTV Stream:", demo_plates)

with col_res:
    st.markdown("#### ⚖️ Violation & Penalty Triage")
    c_p1, c_p2 = st.columns(2)
    c_p1.metric("Fine Penalty", "₹ 10,000", delta="Sec 194E MV Act", delta_color="inverse")
    c_p2.metric("License Action", "3 Months Suspension", delta="Warning Armed")

    if st.button("🚨 Generate & Issue E-Challan Notice", use_container_width=True, type="primary"):
        st.success(f"✅ E-Challan dispatched successfully for vehicle {sel_plate[:13]}! SMS notification sent to registered RTO mobile.")
        challan_slip = f"""================================================================================
SURAT TRAFFIC POLICE • AUTOMATED MOTOR VEHICLE E-CHALLAN
================================================================================
Notice Reference ID   : #CHLN-883921
Offense Date & Time   : 2026-10-22 {time.strftime('%H:%M:%S')}
Location of Violation : Ring Road Junction, Surat Corridor
Offense Description   : Failure to yield Right-of-Way to 108 Emergency Ambulance
Act & Section Code    : Motor Vehicles (Amendment) Act Section 194E
Vehicle Registration  : {sel_plate[:13]}
Penalty Amount        : INR 10,000/- (Payable within 15 days on parivahan.gov.in)
Digital Evidence Ref  : CCTV-CAM-SURAT-CORRIDOR-04
"""
        st.code(challan_slip, language="text")
        st.download_button("📥 Download Official Challan Slip (TXT)", challan_slip, file_name="E_Challan_Notice.txt", use_container_width=True)

st.markdown("---")
st.markdown("### 🗄️ Recent Obstruction Violations Log")
mock_log = pd.DataFrame([
    {"Timestamp": "14:12:05", "Vehicle Reg": "GJ-05-AB-4921", "Corridor": "Majura Gate", "Fine": "₹ 10,000", "Status": "Challan Issued"},
    {"Timestamp": "13:45:20", "Vehicle Reg": "GJ-01-KR-9902", "Corridor": "Ring Road Flyover", "Fine": "₹ 10,000", "Status": "Paid Online"},
    {"Timestamp": "11:20:11", "Vehicle Reg": "GJ-27-E-1120", "Corridor": "Udhna Main Road", "Fine": "₹ 10,000", "Status": "Court Notice Sent"}
])
st.dataframe(mock_log, use_container_width=True, hide_index=True)
