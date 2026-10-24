import os
import glob

# -------------------------------------------------------------------------
# 1. CLEAN HOSPITAL & ADMIN ONLY AUTH (backend/app/core/auth.py)
# -------------------------------------------------------------------------
auth_code = """import streamlit as st

def check_hospital_admin_access():
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False
        st.session_state.admin_user = None

    # Sidebar Portal Separation Display
    with st.sidebar:
        st.markdown("---")
        st.markdown("<div style='font-size:11px; font-weight:900; color:#38bdf8; letter-spacing:1px;'>⚡ LIFEROUTE WORKSTATIONS</div>", unsafe_allow_html=True)
        st.caption("🟢 **User Portal:** Public & Field Tools\\n🔒 **Hospital & Admin:** Authorized Only")
        
        if st.session_state.admin_logged_in:
            st.markdown(f'''
            <div style="background:rgba(34,197,94,0.15); border:1px solid #22c55e; border-radius:8px; padding:8px 10px; margin:8px 0;">
                <div style="font-size:10px; color:#86efac; font-weight:bold;">PORTAL UNLOCKED</div>
                <div style="font-size:12px; color:#ffffff; font-weight:bold;">{st.session_state.admin_user}</div>
            </div>
            ''', unsafe_allow_html=True)
            if st.button("🔒 Lock Hospital / Admin", use_container_width=True, key="logout_admin_hub"):
                st.session_state.admin_logged_in = False
                st.session_state.admin_user = None
                st.rerun()

    # If already logged in, let them access
    if st.session_state.admin_logged_in:
        return True

    # Standalone Clean Hospital & Admin Login Screen (No User Tab clutter)
    _, center_col, _ = st.columns([0.8, 2, 0.8])
    with center_col:
        st.markdown('''
        <div style="background:rgba(15,23,42,0.95); border:2px solid #ef4444; border-radius:16px; padding:24px; box-shadow:0 0 35px rgba(239,68,68,0.25); margin-top:20px; text-align:center;">
            <div style="font-size:32px; margin-bottom:6px;">🏥🔐</div>
            <h3 style="color:#ffffff; margin:0 0 4px 0; font-weight:900;">Hospital & Admin Portal</h3>
            <p style="color:#94a3b8; font-size:13px; margin:0 0 16px 0;">Restricted to On-Duty Medical Officers & City Authorities</p>
        </div>
        ''', unsafe_allow_html=True)
        
        with st.form("hosp_admin_direct_login"):
            pin_input = st.text_input("Enter Hospital / Admin PIN or Password", type="password", placeholder="Enter admin123")
            submitted = st.form_submit_button("🔓 Unlock Hospital & Admin Desk", use_container_width=True, type="primary")
            
            if submitted:
                if pin_input.strip() in ["admin123", "hospital123"]:
                    st.session_state.admin_logged_in = True
                    st.session_state.admin_user = "Hospital CMO / Administrator"
                    st.success("Access Granted! Unlocking Station...")
                    st.rerun()
                else:
                    st.error("Access Denied! Incorrect PIN. (Default: admin123)")
                    
        st.info("💡 **Authority Note:** Field Users and Citizens can use all other navigation pages freely without authentication.")
        
    st.stop()
"""

os.makedirs("backend/app/core", exist_ok=True)
with open("backend/app/core/auth.py", "w", encoding="utf-8") as f:
    f.write(auth_code)
print("AUTH ENGINE CONFIGURED FOR HOSPITAL & ADMIN!")

# -------------------------------------------------------------------------
# 2. UPDATE HOSPITAL INTAKE PAGE
# -------------------------------------------------------------------------
hosp_files = glob.glob("pages/*Hospital*.py") + glob.glob("pages/*Intake*.py")
if not hosp_files:
    hosp_files = ["pages/2_🏥_Hospital_Intake.py"]

for hf in set(hosp_files):
    with open(hf, "r", encoding="utf-8") as f:
        c = f.read()
    
    # Remove old checks and bind to check_hospital_admin_access()
    c = c.replace("check_access('HOSPITAL_ADMIN')", "check_hospital_admin_access()")
    c = c.replace("check_access('hospital_admin')", "check_hospital_admin_access()")
    c = c.replace("from backend.app.core.auth import check_access", "from backend.app.core.auth import check_hospital_admin_access")
    
    if "check_hospital_admin_access()" not in c:
        if "from backend.app.core.auth import check_hospital_admin_access" not in c:
            c = "from backend.app.core.auth import check_hospital_admin_access\n" + c
        c = c.replace("apply_cyber_theme()", "apply_cyber_theme()\ncheck_hospital_admin_access()")
        
    with open(hf, "w", encoding="utf-8") as f:
        f.write(c)
    print("Hospital Intake bound to check_hospital_admin_access:", hf)

# -------------------------------------------------------------------------
# 3. UPDATE ADMIN PANEL PAGE
# -------------------------------------------------------------------------
adm_files = glob.glob("pages/*Admin*.py") + glob.glob("pages/*admin*.py")
if not adm_files:
    adm_files = ["pages/7_⚙️_Admin_Panel.py"]

for af in set(adm_files):
    with open(af, "r", encoding="utf-8") as f:
        c = f.read()
        
    c = c.replace("check_access('HOSPITAL_ADMIN')", "check_hospital_admin_access()")
    c = c.replace("check_access('hospital_admin')", "check_hospital_admin_access()")
    c = c.replace("from backend.app.core.auth import check_access", "from backend.app.core.auth import check_hospital_admin_access")
    
    if "check_hospital_admin_access()" not in c:
        if "from backend.app.core.auth import check_hospital_admin_access" not in c:
            c = "from backend.app.core.auth import check_hospital_admin_access\n" + c
        c = c.replace("apply_cyber_theme()", "apply_cyber_theme()\ncheck_hospital_admin_access()")
        
    with open(af, "w", encoding="utf-8") as f:
        f.write(c)
    print("Admin Panel bound to check_hospital_admin_access:", af)

print("\n--- TWO DISTINCT PORTALS READY: USER (OPEN) vs HOSPITAL & ADMIN (SECURE)! ---")
