import os
import glob

# -------------------------------------------------------------------------
# 1. CREATE MODERN MOBILE DUAL-ROLE AUTH ENGINE (backend/app/core/auth.py)
# -------------------------------------------------------------------------
mobile_auth_code = """import streamlit as st

def init_auth_state():
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
        st.session_state.app_mode = None     # 'USER' or 'HOSPITAL_ADMIN'
        st.session_state.user_name = None

def check_access(target_mode):
    init_auth_state()

    # Sidebar Mobile Profile Badge
    with st.sidebar:
        st.markdown("---")
        if st.session_state.is_logged_in:
            role_label = "🏥 Hospital & Admin Desk" if st.session_state.app_mode == "HOSPITAL_ADMIN" else "🚑 Citizen / 108 Pilot App"
            st.markdown(f'''
            <div style="background:rgba(15,23,42,0.9); border:1.5px solid #38bdf8; border-radius:12px; padding:12px; margin-bottom:12px;">
                <div style="font-size:10.5px; color:#94a3b8; font-weight:bold; letter-spacing:0.5px;">ACTIVE APP MODE</div>
                <div style="font-size:13.5px; font-weight:900; color:#38bdf8;">{role_label}</div>
                <div style="font-size:12px; color:#f1f5f9; margin-top:2px;">User: <b>{st.session_state.user_name}</b></div>
            </div>
            ''', unsafe_allow_html=True)
            if st.button("🔄 Switch App / Log Out", use_container_width=True, key=f"switch_mode_btn_{target_mode}"):
                st.session_state.is_logged_in = False
                st.session_state.app_mode = None
                st.session_state.user_name = None
                st.rerun()
        else:
            st.caption("🔒 Guest Mode • Select Portal Below")

    # If already logged into the required portal
    if st.session_state.is_logged_in:
        if target_mode == "HOSPITAL_ADMIN" and st.session_state.app_mode == "HOSPITAL_ADMIN":
            return True
        elif target_mode == "USER" and st.session_state.app_mode == "USER":
            return True
        else:
            # User logged into opposite portal
            st.warning(f"⚠️ Access Restricted: You are currently on the other portal. Please switch profile.")
            if st.button("Switch to this Desk", key=f"switch_desk_btn_{target_mode}"):
                st.session_state.is_logged_in = False
                st.session_state.app_mode = None
                st.session_state.user_name = None
                st.rerun()
            st.stop()

    # Mobile Style App Gateway Card
    _, center_col, _ = st.columns([0.6, 2.2, 0.6])
    with center_col:
        st.markdown('''
        <div style="background:rgba(15,23,42,0.95); border:2px solid #38bdf8; border-radius:18px; padding:22px; box-shadow:0 0 35px rgba(56,189,248,0.25); margin-top:15px; margin-bottom:15px;">
            <div style="text-align:center;">
                <span style="background:rgba(56,189,248,0.15); color:#38bdf8; padding:4px 12px; border-radius:20px; font-size:11px; font-weight:bold;">LIFEROUTE MOBILE GATEWAY</span>
                <h2 style="margin:8px 0 2px 0; color:#ffffff; font-size:22px; font-weight:900;">Choose Your Login Mode</h2>
                <p style="margin:0 0 16px 0; color:#94a3b8; font-size:12.5px;">Select your role to access dedicated mobile workstations</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        tab_user, tab_hospital = st.tabs(["🚑 User / 108 Driver Portal", "🏥 Hospital & Admin Desk"])

        with tab_user:
            st.markdown("#### 📱 Emergency Dispatcher / Citizen App")
            st.caption("For 108 Ambulance Pilots, Paramedics and Surat Citizens")
            u_name = st.text_input("Mobile Number or Pilot ID", value="+91 98765 43210", key="user_phone_inp")
            if st.button("🚀 Enter User Emergency App", type="primary", use_container_width=True, key="login_user_btn"):
                st.session_state.is_logged_in = True
                st.session_state.app_mode = "USER"
                st.session_state.user_name = u_name
                st.success("Welcome to Citizen & Dispatch App!")
                st.rerun()

        with tab_hospital:
            st.markdown("#### 🩺 Hospital CMO & City Admin Desk")
            st.caption("Authorized Medical Officers & Municipal Traffic Enforcers")
            h_user = st.text_input("Hospital / Admin ID", placeholder="admin or hospital", key="hosp_uname_inp")
            h_pass = st.text_input("Secure PIN / Password", type="password", key="hosp_pwd_inp")
            
            if st.button("🔐 Unlock Hospital & Admin Desk", type="primary", use_container_width=True, key="login_hosp_btn"):
                if h_user.strip().lower() in ["admin", "hospital"] and h_pass.strip() == "admin123":
                    st.session_state.is_logged_in = True
                    st.session_state.app_mode = "HOSPITAL_ADMIN"
                    st.session_state.user_name = "Dr. Duty Incharge (CMO)" if h_user.strip().lower() == "hospital" else "City System Administrator"
                    st.success("Authorized! Unlocking Medical Staging & Admin Desk...")
                    st.rerun()
                else:
                    st.error("Invalid credentials! (ID: admin / PIN: admin123)")

        st.caption("💡 Quick Credentials: Hospital/Admin -> `admin` / `admin123` | User -> Click 1-Step Login")

    st.stop()
"""

os.makedirs("backend/app/core", exist_ok=True)
with open("backend/app/core/auth.py", "w", encoding="utf-8") as f:
    f.write(mobile_auth_code)
print("MOBILE DUAL-PORTAL ENGINE INSTALLED!")

# -------------------------------------------------------------------------
# 2. BIND HOSPITAL INTAKE PAGE TO HOSPITAL_ADMIN APP MODE
# -------------------------------------------------------------------------
hosp_files = glob.glob("pages/*Hospital*.py") + glob.glob("pages/*Intake*.py")
if not hosp_files:
    hosp_files = ["pages/2_🏥_Hospital_Intake.py"]

for hf in set(hosp_files):
    with open(hf, "r", encoding="utf-8") as f:
        c = f.read()
    if "check_access('HOSPITAL_ADMIN')" not in c:
        if "from backend.app.core.auth import check_access" not in c:
            c = "from backend.app.core.auth import check_access\n" + c
        c = c.replace("check_access('hospital_admin')", "check_access('HOSPITAL_ADMIN')")
        if "check_access('HOSPITAL_ADMIN')" not in c:
            c = c.replace("apply_cyber_theme()", "apply_cyber_theme()\ncheck_access('HOSPITAL_ADMIN')")
        with open(hf, "w", encoding="utf-8") as f:
            f.write(c)
        print("Hospital Intake bound to Hospital/Admin Mobile Login:", hf)

# -------------------------------------------------------------------------
# 3. BIND ADMIN PANEL TO HOSPITAL_ADMIN APP MODE
# -------------------------------------------------------------------------
adm_files = glob.glob("pages/*Admin*.py") + glob.glob("pages/*admin*.py")
if not adm_files:
    adm_files = ["pages/7_⚙️_Admin_Panel.py"]

for af in set(adm_files):
    with open(af, "r", encoding="utf-8") as f:
        c = f.read()
    if "check_access('HOSPITAL_ADMIN')" not in c:
        if "from backend.app.core.auth import check_access" not in c:
            c = "from backend.app.core.auth import check_access\n" + c
        c = c.replace("check_access('hospital_admin')", "check_access('HOSPITAL_ADMIN')")
        if "check_access('HOSPITAL_ADMIN')" not in c:
            c = c.replace("apply_cyber_theme()", "apply_cyber_theme()\ncheck_access('HOSPITAL_ADMIN')")
        with open(af, "w", encoding="utf-8") as f:
            f.write(c)
        print("Admin Panel bound to Hospital/Admin Mobile Login:", af)

print("\n--- APP SUCCESSFULLY TRANSFORMED INTO SEPARATE MOBILE WORKSTATIONS! ---")
