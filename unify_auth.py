import os
import glob

# 1. Update Core Auth Engine to merge Hospital and Admin Privileges
auth_unified_code = '''"""
LifeRoute AI - Unified Hospital & Admin Authentication Manager
"""
import streamlit as st

USERS_DB = {
    "admin": {"password": "admin123", "role": "admin", "name": "Hospital Chief Administrator", "facility": "Surat Apex Healthcare Network"},
    "hospital": {"password": "admin123", "role": "admin", "name": "Hospital Duty Incharge", "facility": "Surat Apex Healthcare Network"},
    "user": {"password": "user123", "role": "user", "name": "Emergency Dispatch Operator", "facility": "108 Command Center"}
}

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.role = None
        st.session_state.facility = None

def login(username, password):
    u = username.strip().lower()
    if u in USERS_DB and USERS_DB[u]["password"] == password:
        st.session_state.authenticated = True
        st.session_state.user = USERS_DB[u]["name"]
        st.session_state.role = USERS_DB[u]["role"]
        st.session_state.facility = USERS_DB[u]["facility"]
        return True, "Login successful!"
    return False, "Invalid username or password"

def logout():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.facility = None

def render_login_box(required_role=None):
    init_session()
    
    # If already logged in, check role permission
    if st.session_state.authenticated:
        # If user has admin/hospital unified role, they get access to both hospital and admin desks
        allowed_roles = ["admin"] if required_role in ["admin", "hospital"] else [required_role, "admin"]
        if required_role and st.session_state.role not in allowed_roles:
            st.warning(f"Access Denied: This workstation requires Hospital/Admin credentials. You are currently logged in as {st.session_state.role.upper()}.")
            if st.button("Log In as Hospital / Admin Account"):
                logout()
                st.rerun()
            st.stop()
        return True

    # Modern Cyber Secure Login Card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background:rgba(15,23,42,0.92); border:2px solid #3b82f6; border-radius:14px; padding:22px; box-shadow:0 0 30px rgba(59,130,246,0.3); margin-top:20px;">
            <h3 style="color:#60a5fa; margin:0 0 4px 0; text-align:center; font-weight:900;">🔐 HOSPITAL & ADMIN SECURE PORTAL</h3>
            <p style="color:#94a3b8; font-size:12px; text-align:center; margin:0 0 16px 0;">Sign in to access Clinical Intake & Master Admin Desks</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("auth_unified_login_form"):
            uname = st.text_input("Username", placeholder="e.g. admin or hospital")
            pword = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Sign In to Workstation", use_container_width=True, type="primary")
            
            if submitted:
                success, msg = login(uname, pword)
                if success:
                    st.success(f"Authenticated as {st.session_state.user}!")
                    st.rerun()
                else:
                    st.error(msg)
                    
        st.markdown("""
        <div style="background:rgba(30,41,59,0.7); border:1px dashed #475569; border-radius:8px; padding:10px; font-size:11.5px; color:#cbd5e1; margin-top:10px;">
            🔑 <b>Hospital & Admin Combined Account:</b><br>
            • Username: <code>admin</code> (or <code>hospital</code>)<br>
            • Password: <code>admin123</code>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

def render_sidebar_user_badge():
    init_session()
    with st.sidebar:
        st.markdown("---")
        if st.session_state.authenticated:
            st.markdown(f"""
            <div style="background:rgba(15,23,42,0.9); border:1px solid #334155; border-radius:10px; padding:10px; margin-bottom:10px;">
                <div style="font-size:11px; color:#94a3b8; font-weight:bold;">AUTHORIZED SESSION</div>
                <div style="font-size:13px; font-weight:bold; color:#f8fafc;">{st.session_state.user}</div>
                <div style="font-size:11px; color:#38bdf8;">Access: {st.session_state.role.upper()} ({st.session_state.facility})</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚪 Log Out", use_container_width=True):
                logout()
                st.rerun()
        else:
            st.caption("🔒 Guest Session (Please sign in)")
'''

with open(os.path.join("backend", "app", "core", "auth.py"), "w", encoding="utf-8") as f:
    f.write(auth_unified_code)
print("UNIFIED AUTH SYSTEM CONFIGURED SUCCESSFULLY!")
