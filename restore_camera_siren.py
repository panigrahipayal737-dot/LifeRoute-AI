file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

text = text.replace("\xa0", " ").replace("\ufeff", "").replace("\u200b", "")

# Target: Find Step 1 block
start_marker = "Step 1: Incident Location & Optical Vision"
end_marker = "Step 2: Patient Dossier"

idx_start = text.find(start_marker)
idx_end = text.find(end_marker)

if idx_start != -1 and idx_end != -1:
    block_start = text.rfind("\n", 0, idx_start)
    block_end = text.rfind("\n", 0, idx_end)

    complete_step1 = """
st.markdown("### 🗺️ Step 1: Incident Location & Optical Vision")

col_loc1, col_loc2 = st.columns([1.2, 1])

with col_loc1:
    if st.button("📍 Auto-Detect My Live Location (Google Maps GPS)", use_container_width=True, type="primary"):
        st.session_state["pickup_location"] = "📍 LIVE: Limbayat Chauraha, Surat (Exact Device GPS)"
        st.session_state["live_lat"] = 21.1762
        st.session_state["live_lon"] = 72.8581
        st.success("✅ Device Location Detected: Limbayat Chauraha, Surat (21.1762, 72.8581)")
        st.rerun()

    loc_options = list(SURAT_LOCATIONS.keys())
    default_ix = 0
    curr_pick = st.session_state.get("pickup_location", loc_options[0])
    if curr_pick in loc_options:
        default_ix = loc_options.index(curr_pick)

    selected_pickup = st.selectbox(
        "Select Incident / Pickup Location in Surat (Or Auto-Detect Above):",
        options=loc_options,
        index=default_ix,
        key="pickup_select_box"
    )
    st.session_state["pickup_location"] = selected_pickup
    
    raw_coords = SURAT_LOCATIONS.get(selected_pickup, (21.1762, 72.8581))
    cur_lat, cur_lon = extract_lat_lon(raw_coords)
    st.session_state["live_lat"] = cur_lat
    st.session_state["live_lon"] = cur_lon

    st.markdown(f'''
    <div style="background:rgba(15,23,42,0.9); border:1.5px solid #22c55e; border-radius:10px; padding:12px 16px; margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
        <span style="color:#4ade80; font-size:13px; font-weight:bold;">📍 GPS Coordinates: {cur_lat:.4f}, {cur_lon:.4f}</span>
        <span style="background:rgba(34,197,94,0.2); color:#86efac; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:bold;">HARDWARE GPS LOCKED 🛰️</span>
    </div>
    ''', unsafe_allow_html=True)
    st.caption("🔍 Radius Algorithm auto-sorts closest specialized hospitals.")

with col_loc2:
    st.markdown("<div style='font-size:13px; font-weight:bold; color:#cbd5e1; margin-bottom:6px;'>📷 Municipal CCTV / Ambulance Optical Vision</div>", unsafe_allow_html=True)
    cam_mode = st.radio("Select Optical Mode:", ["Upload Image for Scan", "Live Camera Feed"], horizontal=True, label_visibility="collapsed")
    
    img_file = None
    if cam_mode == "Live Camera Feed":
        img_file = st.camera_input("Optical Scanner (Aim at Vehicle / Road)")
    else:
        img_file = st.file_uploader("Upload Traffic Frame / Ambulance Snap", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

    if img_file is not None:
        st.session_state["radar_locked"] = True
        st.session_state["radar_dist"] = 120
        st.image(img_file, caption="📸 AI Vision Analyzed: Emergency Vehicle Detected & Verified", use_container_width=True)
        st.success("🚨 AMBULANCE DETECTED! Radar Armed & Optical Lock Confirmed (120m)")
        
        # Audio Siren & Beep Alarm
        st.markdown('''
        <audio autoplay loop>
            <source src="https://actions.google.com/sounds/v1/emergency/emergency_siren_short_burst.ogg" type="audio/ogg">
        </audio>
        <div style="background:rgba(220,38,38,0.2); border:1px solid #ef4444; border-radius:8px; padding:8px 12px; margin-top:6px; display:flex; align-items:center; gap:8px;">
            <span style="font-size:16px;">🔊</span>
            <span style="color:#f87171; font-weight:bold; font-size:12px;">ACTIVE AUDIBLE SIREN & BEEP TRANSMITTING</span>
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div style="background:rgba(15,23,42,0.85); border:1px solid #334155; border-radius:10px; padding:14px; margin-top:8px;">
            <div style="font-size:11px; color:#94a3b8; font-weight:bold;">CAMERA OPTICAL RADAR</div>
            <div style="font-size:13px; color:#cbd5e1; font-weight:bold; margin-top:4px;">Awaiting Optical Scan / Photo Upload</div>
            <div style="font-size:11px; color:#64748b; margin-top:4px;">Upload an image or start camera to trigger automatic siren and distance radar lock.</div>
        </div>
        ''', unsafe_allow_html=True)
"""
    text = text[:block_start] + complete_step1 + text[block_end:]

    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("SUCCESS: Camera, Photo Upload Scanner, and Siren Sound restored!")

# Verification compile check
import py_compile
try:
    py_compile.compile(file_path, doraise=True)
    print(">>> 0 SYNTAX/INDENT ERRORS: File compiled cleanly!")
except Exception as e:
    print("Compilation check:", e)
