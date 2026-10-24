import os
import glob

# 1. Clean & Bulletproof Auth Core (backend/app/core/auth.py)
auth_code = """import streamlit as st

def check_access(required_role=None):
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
        st.session_state.user_role = None
        st.session_state.username = None

    with st.sidebar:
        st.markdown("---")
        if st.session_state.is_logged_in:
            st.success(f"Log: **{st.session_state.username}** ({st.session_state.user_role.upper()})")
            if st.button("Logout", key="logout_global_btn", use_container_width=True):
                st.session_state.is_logged_in = False
                st.session_state.user_role = None
                st.session_state.username = None
                st.rerun()
        else:
            st.info("Locked: Login Required")

    # If already logged in, check role
    if st.session_state.is_logged_in:
        # admin/hospital have full access
        if st.session_state.user_role in ["admin", "hospital"]:
            return True
        if required_role and st.session_state.user_role != required_role:
            st.warning("Access Denied for this role.")
            st.stop()
        return True

    # Show Direct Login Box
    st.markdown("### Secure Workstation Login")
    st.caption("Please sign in to view this station.")
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        u_in = st.text_input("Username", key="auth_uname_inp")
        p_in = st.text_input("Password", type="password", key="auth_pass_inp")
        
        if st.button("Sign In", type="primary", use_container_width=True):
            uname = u_in.strip().lower()
            pwd = p_in.strip()
            
            # Hospital and Admin share the exact same access
            if (uname in ["admin", "hospital"]) and pwd == "admin123":
                st.session_state.is_logged_in = True
                st.session_state.user_role = "hospital_admin"
                st.session_state.username = uname
                st.success("Access Granted!")
                st.rerun()
            elif uname == "user" and pwd == "user123":
                st.session_state.is_logged_in = True
                st.session_state.user_role = "user"
                st.session_state.username = "user"
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Invalid credentials! Use admin / admin123")
                
    with col2:
        st.info("**Credentials:**\\n\\n- **Hospital & Admin:** `admin` / `admin123` (or `hospital` / `admin123`)\\n- **User:** `user` / `user123`")
    
    st.stop()
"""

os.makedirs("backend/app/core", exist_ok=True)
with open("backend/app/core/auth.py", "w", encoding="utf-8") as f:
    f.write(auth_code)

# 2. Wire Hospital Intake to use check_access()
hosp_files = glob.glob("pages/*Hospital*.py") + glob.glob("pages/*Intake*.py")
if not hosp_files:
    hosp_files = ["pages/2_Hospital_Intake.py"]

for hf in set(hosp_files):
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove old auth calls if any
    content = content.replace("render_login_box(required_role='hospital')", "check_access('hospital_admin')")
    content = content.replace("render_login_box(required_role='admin')", "check_access('hospital_admin')")
    content = content.replace("render_sidebar_user_badge()", "")
    content = content.replace("from backend.app.core.auth import render_login_box, render_sidebar_user_badge", "from backend.app.core.auth import check_access")
    
    if "from backend.app.core.auth import check_access" not in content:
        content = "from backend.app.core.auth import check_access\n" + content
    if "check_access('hospital_admin')" not in content:
        content = content.replace("apply_cyber_theme()", "apply_cyber_theme()\ncheck_access('hospital_admin')")
        
    with open(hf, "w", encoding="utf-8") as f:
        f.write(content)
    print("Hospital Intake Auth Updated:", hf)

# 3. Wire Admin Panel to use check_access()
adm_files = glob.glob("pages/*Admin*.py") + glob.glob("pages/*admin*.py")
if not adm_files:
    adm_files = ["pages/7_Admin_Panel.py"]

for af in set(adm_files):
    with open(af, "r", encoding="utf-8") as f:
        content = f.read()
        
    content = content.replace("render_login_box(required_role='hospital')", "check_access('hospital_admin')")
    content = content.replace("render_login_box(required_role='admin')", "check_access('hospital_admin')")
    content = content.replace("render_sidebar_user_badge()", "")
    content = content.replace("from backend.app.core.auth import render_login_box, render_sidebar_user_badge", "from backend.app.core.auth import check_access")
    
    if "from backend.app.core.auth import check_access" not in content:
        content = "from backend.app.core.auth import check_access\n" + content
    if "check_access('hospital_admin')" not in content:
        content = content.replace("apply_cyber_theme()", "apply_cyber_theme()\ncheck_access('hospital_admin')")
        
    with open(af, "w", encoding="utf-8") as f:
        f.write(content)
    print("Admin Panel Auth Updated:", af)

print("\n--- ALL PAGES SUCCESSFULLY CONFIGURED WITH UNIFIED LOGIN! ---")
