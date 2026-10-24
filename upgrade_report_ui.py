import os
import glob

# Search in current directory and pages
candidates = glob.glob("**/*.py", recursive=True)
target_file = None

for f in candidates:
    if any(x in f for x in ["venv", ".git", "__pycache__"]):
        continue
    try:
        with open(f, "r", encoding="utf-8", errors="ignore") as fp:
            c = fp.read()
            if "OFFICIAL CLINICAL HANDOVER SLIP" in c or "IN-TRANSIT ICU TELEMETRY VITALS" in c:
                target_file = f
                break
    except Exception:
        pass

if not target_file:
    target_file = "streamlit_app.py"

print(f"Targeting report file: {target_file}")

with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# Professional modern PDF / HTML clinical handover slip template
clean_modern_template = """
    report_html = f'''
    <div style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 820px; margin: auto; background: #ffffff; color: #0f172a; border-radius: 16px; border: 1.5px solid #e2e8f0; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01); overflow: hidden; padding: 0 0 30px 0;">
        <!-- Header Banner -->
        <div style="background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); padding: 24px 32px; color: #ffffff; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 22px;">🚑</span>
                    <span style="font-size: 20px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase;">LifeRoute Clinical Handover</span>
                </div>
                <div style="font-size: 11px; opacity: 0.85; margin-top: 4px; letter-spacing: 0.3px; font-weight: 500;">EMERGENCY MEDICAL CORRIDOR & TRAUMA APEX NETWORK</div>
            </div>
            <div style="text-align: right; background: rgba(255, 255, 255, 0.15); padding: 8px 14px; border-radius: 8px; backdrop-filter: blur(4px);">
                <div style="font-size: 10px; text-transform: uppercase; font-weight: 700; letter-spacing: 0.8px;">Token ID</div>
                <div style="font-size: 15px; font-weight: 800; letter-spacing: 0.5px;">{token}</div>
            </div>
        </div>

        <div style="padding: 24px 32px;">
            <!-- Timestamp Sub-bar -->
            <div style="display: flex; justify-content: space-between; border-bottom: 2px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 20px; font-size: 12px; color: #64748b; font-weight: 600;">
                <span>📅 Transmit Date: <strong style="color: #1e293b;">{disp_time}</strong></span>
                <span>🚨 Priority Status: <strong style="color: #dc2626;">TRIAGE RED (CODE AMBER)</strong></span>
            </div>

            <!-- Section 1: Patient Profile -->
            <div style="margin-bottom: 22px;">
                <div style="font-size: 12px; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">
                    <span style="color: #dc2626;">●</span> 1. Patient Dossier & Primary Staging
                </div>
                <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 18px;">
                    <div><span style="font-size: 11px; color: #64748b; display: block; font-weight: 600;">PATIENT FULL NAME</span><strong style="font-size: 14px; color: #1e293b;">{p_name}</strong></div>
                    <div><span style="font-size: 11px; color: #64748b; display: block; font-weight: 600;">AGE</span><strong style="font-size: 14px; color: #1e293b;">{p_age}</strong></div>
                    <div><span style="font-size: 11px; color: #64748b; display: block; font-weight: 600;">BLOOD GROUP</span><strong style="font-size: 14px; color: #dc2626;">{p_bg}</strong></div>
                    <div style="grid-column: span 3; border-top: 1px dashed #cbd5e1; padding-top: 8px; margin-top: 4px;">
                        <span style="font-size: 11px; color: #64748b; display: block; font-weight: 600;">PRELIMINARY DIAGNOSIS / CLINICAL COMPLAINT</span>
                        <strong style="font-size: 13.5px; color: #0f172a;">{p_diag}</strong>
                    </div>
                </div>
            </div>

            <!-- Section 2: Vitals Card -->
            <div style="margin-bottom: 22px;">
                <div style="font-size: 12px; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">
                    <span style="color: #dc2626;">●</span> 2. In-Transit ICU Telemetry Vitals
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
                    <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 12px 16px; text-align: center;">
                        <span style="font-size: 11px; color: #166534; font-weight: 700; text-transform: uppercase; display: block;">SpO2 Oxygen</span>
                        <span style="font-size: 20px; font-weight: 900; color: #15803d;">{p_spo2}%</span>
                    </div>
                    <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 10px; padding: 12px 16px; text-align: center;">
                        <span style="font-size: 11px; color: #1e40af; font-weight: 700; text-transform: uppercase; display: block;">Pulse Rate</span>
                        <span style="font-size: 20px; font-weight: 900; color: #1d4ed8;">{p_pulse} <span style="font-size: 12px; font-weight: 600;">BPM</span></span>
                    </div>
                    <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 10px; padding: 12px 16px; text-align: center;">
                        <span style="font-size: 11px; color: #991b1b; font-weight: 700; text-transform: uppercase; display: block;">Blood Pressure</span>
                        <span style="font-size: 20px; font-weight: 900; color: #b91c1c;">{p_bp}</span>
                    </div>
                </div>
            </div>

            <!-- Section 3: Transit Staging -->
            <div style="margin-bottom: 30px;">
                <div style="font-size: 12px; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">
                    <span style="color: #dc2626;">●</span> 3. V2X Green-Wave Transit & Hospital Bed Staging
                </div>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 18px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div><span style="font-size: 11px; color: #64748b; display: block; font-weight: 600;">INCIDENT ORIGIN</span><strong style="font-size: 13px; color: #1e293b;">{p_origin}</strong></div>
                    <div><span style="font-size: 11px; color: #64748b; display: block; font-weight: 600;">RECEIVING TRAUMA CENTER</span><strong style="font-size: 13px; color: #0284c7;">{p_dest}</strong></div>
                    <div><span style="font-size: 11px; color: #64748b; display: block; font-weight: 600;">108 AMBULANCE FLEET / PILOT</span><strong style="font-size: 13px; color: #1e293b;">{p_unit} ({p_pilot})</strong></div>
                    <div><span style="font-size: 11px; color: #64748b; display: block; font-weight: 600;">ALLOCATED ICU TRAUMA BED</span><strong style="font-size: 13px; color: #16a34a;">{p_bed}</strong></div>
                </div>
            </div>

            <!-- Signatures Section -->
            <div style="display: flex; justify-content: space-between; border-top: 1.5px dashed #cbd5e1; padding-top: 24px; margin-top: 20px;">
                <div style="text-align: center; width: 40%;">
                    <div style="height: 35px; border-bottom: 1.5px solid #94a3b8; margin-bottom: 6px;"></div>
                    <div style="font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase;">108 Paramedic Sign & Stamp</div>
                </div>
                <div style="text-align: center; width: 40%;">
                    <div style="height: 35px; border-bottom: 1.5px solid #94a3b8; margin-bottom: 6px;"></div>
                    <div style="font-size: 11px; font-weight: 700; color: #475569; text-transform: uppercase;">Receiving CMO / ER Physician Sign</div>
                </div>
            </div>
        </div>
    </div>
    '''
"""

# Replace the HTML generator block
import re
pattern = r'report_html\s*=\s*f?[\'"]{3}[\s\S]*?[\'"]{3}'

if re.search(pattern, code):
    code = re.sub(pattern, clean_modern_template.strip(), code, count=1)
    
    # Ensure all variable mappings match safely
    helper_mapping = """
    token = st.session_state.get("active_token", "#SOS-1401")
    disp_time = time.strftime("%d-%b-%Y %H:%M:%S")
    p_name = st.session_state.get("patient_name", "Payal")
    p_age = st.session_state.get("patient_age", "21 Years")
    p_bg = st.session_state.get("patient_blood_group", "B+")
    p_diag = st.session_state.get("patient_condition", "Cardiac Arrest / Sudden Heart Failure")
    p_spo2 = st.session_state.get("patient_spo2", 96)
    p_pulse = st.session_state.get("patient_pulse", 108)
    p_bp = st.session_state.get("patient_bp", "130/85")
    p_origin = st.session_state.get("pickup_location", "Vesu VIP Road Junction (South Surat)")
    p_dest = st.session_state.get("target_hospital_name", "BAPS Pramukh Swami Hospital & Heart Care (Adajan, Surat)")
    p_unit = st.session_state.get("ambulance_id", "GJ-01-EA-108 (ALS)")
    p_pilot = st.session_state.get("driver_name", "Ramesh Kumar")
    p_bed = st.session_state.get("allocated_bed", "CRITICAL-BAY #01")
    """
    
    # Insert variables right before report_html if needed
    if "token =" not in code:
        code = code.replace("report_html = f'''", helper_mapping + "\n    report_html = f'''")

    with open(target_file, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    print(f"SUCCESS: Report formatted into clean modern medical slip inside {target_file}!")
else:
    print("Could not find raw report_html regex, writing clean snippet.")

import py_compile
py_compile.compile(target_file, doraise=True)
print(">>> COMPILE VERIFIED 0 ERRORS!")
