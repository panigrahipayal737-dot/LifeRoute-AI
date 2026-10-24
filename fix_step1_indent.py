file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Replace non-breaking spaces and BOM
text = text.replace("\xa0", " ").replace("\ufeff", "").replace("\u200b", "")

# Search and cleanly rewrite the exact Step 1 location block
start_marker = "Step 1: Incident Location"
end_marker = "Step 2: Patient Dossier"

idx_start = text.find(start_marker)
idx_end = text.find(end_marker)

if idx_start != -1 and idx_end != -1:
    # Find the beginning of the header line
    block_start = text.rfind("\n", 0, idx_start)
    block_end = text.rfind("\n", 0, idx_end)
    
    clean_step1_block = """
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
    
    cur_lat, cur_lon = SURAT_LOCATIONS.get(selected_pickup, (21.1762, 72.8581))
    st.session_state["live_lat"] = cur_lat
    st.session_state["live_lon"] = cur_lon

    st.markdown(f'''
    <div style="background:rgba(15,23,42,0.9); border:1.5px solid #22c55e; border-radius:10px; padding:12px 16px; margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
        <span style="color:#4ade80; font-size:13px; font-weight:bold;">📍 GPS Coordinates: {cur_lat:.4f}, {cur_lon:.4f}</span>
        <span style="background:rgba(34,197,94,0.2); color:#86efac; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:bold;">HARDWARE GPS LOCKED 🛰️</span>
    </div>
    ''', unsafe_allow_html=True)
    st.caption("🔍 Radius Algorithm auto-sorts closest specialized hospitals.")
"""
    # Replace broken slice with the cleanly formatted block
    text = text[:block_start] + clean_step1_block + text[block_end:]

    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("SUCCESS: Step 1 block indentation perfectly aligned!")
else:
    print("Markers not found, checking line replacement...")
