"""
LifeRoute AI - Unified Hospital & Admin Gatekeeper
"""
import streamlit as st

def check_hospital_admin_access():
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False
        st.session_state.admin_user = None

    with st.sidebar:
        st.markdown("---")
        st.markdown("<div style='font-size:11px; font-weight:900; color:#38bdf8; letter-spacing:0.8px;'>⚡ LIFEROUTE WORKSTATIONS</div>", unsafe_allow_html=True)
        st.caption("🟢 **Public Pages:** Open Access\n🔒 **Hospital & Admin:** Restricted Access")
        
        if st.session_state.admin_logged_in:
            st.markdown(f"""
            <div style="background:rgba(34,197,94,0.15); border:1.5px solid #22c55e; border-radius:10px; padding:10px; margin:8px 0;">
                <div style="font-size:10px; color:#86efac; font-weight:bold;">WORKSTATION UNLOCKED</div>
                <div style="font-size:12.5px; color:#ffffff; font-weight:900;">{st.session_state.admin_user}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔒 Lock Workstation", use_container_width=True, key="lock_station_btn"):
                st.session_state.admin_logged_in = False
                st.session_state.admin_user = None
                st.rerun()

    if st.session_state.admin_logged_in:
        return True

    _, col_center, _ = st.columns([0.8, 2, 0.8])
    with col_center:
        st.markdown("""
        <div style="background:rgba(15,23,42,0.96); border:2px solid #ef4444; border-radius:18px; padding:26px; box-shadow:0 0 35px rgba(239,68,68,0.3); margin-top:25px; text-align:center;">
            <div style="font-size:36px; margin-bottom:8px;">🏥🔐</div>
            <h3 style="color:#ffffff; margin:0 0 6px 0; font-weight:900;">HOSPITAL & ADMIN DESK</h3>
            <p style="color:#94a3b8; font-size:13px; margin:0 0 18px 0;">Restricted to On-Duty Medical Officers & Municipal Authorities</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("hosp_admin_pin_form"):
            pin_input = st.text_input("Enter Workstation Passcode / PIN", type="password", placeholder="Enter admin123")
            submitted = st.form_submit_button("🔓 Unlock Hospital & Admin Desk", use_container_width=True, type="primary")
            
            if submitted:
                if pin_input.strip() in ["admin123", "hospital123"]:
                    st.session_state.admin_logged_in = True
                    st.session_state.admin_user = "Hospital Incharge / Administrator"
                    st.success("Access Granted! Unlocking Station...")
                    st.rerun()
                else:
                    st.error("Invalid credentials! Enter default password: admin123")
                    
        st.info("💡 **Navigation Notice:** Traffic Control, Police Radar, Citizen Map, and AI Challan are publicly accessible.")
        
    st.stop()
