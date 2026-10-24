import glob
import os
import py_compile

# Target file dhundhein
hosp_files = glob.glob('pages/*Hospital*.py')
if not hosp_files:
    hosp_files = [r'pages\7_🏥_Hospital_Admin_Desk.py']

target = hosp_files[0]
print(f'Patching Authentication in: {target}')

with open(target, 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# Auth check block banate hain jo page config ke baad lagega
auth_block = '''
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
'''

# Agar pehle se auth nahi laga hai to inject karein
if 'hospital_admin_logged_in' not in code:
    # Page config ke theek baad inject karein
    pos = code.find('st.markdown(')
    if pos != -1:
        code = code[:pos] + auth_block + '\n\n' + code[pos:]
    else:
        code = auth_block + '\n\n' + code

with open(target, 'w', encoding='utf-8', newline='\n') as f:
    f.write(code)

py_compile.compile(target, doraise=True)
print(f'>>> SUCCESS: Password protection added to {target} with 0 errors!')