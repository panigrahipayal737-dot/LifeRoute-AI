import os
import re

file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Manual override control block for Step 2
manual_step2_block = """
st.markdown("### 🫀 Step 2: Patient Dossier & Manual Clinical Staging")

# Manual Staging Form
with st.expander("⚙️ Manual Patient & Vitals Override Console (Full Custom Controls)", expanded=True):
    col_p1, col_p2, col_p3 = st.columns([1.5, 1, 1])
    with col_p1:
        custom_p_name = st.text_input("Patient Full Name:", value=st.session_state.get("patient_name", "Payal"), key="in_custom_pname")
    with col_p2:
        custom_p_age = st.number_input("Age (Years):", min_value=1, max_value=115, value=int(st.session_state.get("patient_age", 21)), key="in_custom_page")
    with col_p3:
        bg_list = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
        default_bg_ix = bg_list.index(st.session_state.get("patient_blood_group", "B+")) if st.session_state.get("patient_blood_group", "B+") in bg_list else 2
        custom_p_bg = st.selectbox("Blood Group:", options=bg_list, index=default_bg_ix, key="in_custom_pbg")

    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        custom_p_cond = st.text_input(
            "Primary Diagnosis / Emergency Condition:",
            value=st.session_state.get("patient_condition", "Cardiac Arrest / Sudden Heart Failure (CPR En-Route)"),
            key="in_custom_pcond"
        )
    with col_c2:
        custom_bed_type = st.selectbox(
            "Target Bed Category:",
            ["CRITICAL-BAY #01 (Ventilator)", "TRAUMA-BAY #02", "ICU-ISOLATION #03", "CARDIAC-CATH BAY #04"],
            key="in_custom_bed_type"
        )

    st.markdown("<div style='font-size:12px; font-weight:700; color:#38bdf8; margin-top:8px;'>📊 MANUAL ICU VITALS TELEMETRY OVERRIDE</div>", unsafe_allow_html=True)
    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        custom_spo2 = st.slider("Oxygen Saturation (SpO2 %):", min_value=50, max_value=100, value=int(st.session_state.get("patient_spo2", 96)), key="in_custom_spo2")
    with col_v2:
        custom_pulse = st.slider("Heart / Pulse Rate (BPM):", min_value=30, max_value=220, value=int(st.session_state.get("patient_pulse", 108)), key="in_custom_pulse")
    with col_v3:
        custom_bp = st.text_input("Blood Pressure (mmHg):", value=str(st.session_state.get("patient_bp", "130/85")), key="in_custom_bp")

    col_fl1, col_fl2 = st.columns(2)
    with col_fl1:
        custom_fleet = st.text_input("108 Fleet Unit ID:", value=st.session_state.get("ambulance_id", "GJ-01-EA-108 (ALS)"), key="in_custom_fleet")
    with col_fl2:
        custom_pilot = st.text_input("Pilot / Driver Name:", value=st.session_state.get("driver_name", "Ramesh Kumar"), key="in_custom_pilot")

    # Sync back to global session state
    st.session_state["patient_name"] = custom_p_name
    st.session_state["patient_age"] = str(custom_p_age)
    st.session_state["patient_blood_group"] = custom_p_bg
    st.session_state["patient_condition"] = custom_p_cond
    st.session_state["patient_spo2"] = custom_spo2
    st.session_state["patient_pulse"] = custom_pulse
    st.session_state["patient_bp"] = custom_bp
    st.session_state["ambulance_id"] = custom_fleet
    st.session_state["driver_name"] = custom_pilot
    st.session_state["allocated_bed"] = custom_bed_type
"""

# Replace Step 2 section
start_marker = "Step 2: Patient Dossier"
end_marker = "Step 3:"

idx_start = text.find(start_marker)
idx_end = text.find(end_marker)

if idx_start != -1 and idx_end != -1:
    b_start = text.rfind("\n", 0, idx_start)
    b_end = text.rfind("\n", 0, idx_end)
    text = text[:b_start] + "\n" + manual_step2_block.strip() + "\n\n" + text[b_end:]

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)

print("SUCCESS: Full manual controls added to Step 2 in streamlit_app.py!")

import py_compile
py_compile.compile(file_path, doraise=True)
print(">>> COMPILE VERIFIED 0 ERRORS!")
