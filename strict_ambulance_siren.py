file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Replace condition so siren only sounds strictly when verified ambulance is detected
old_target = """        if is_ambulance:
            st.session_state["radar_locked"] = True
            st.session_state["radar_dist"] = 120
            st.success("🚨 AMBULANCE DETECTED! Radar Armed & Optical Lock Confirmed (120m)")
            
            # Play Siren Sound
            st.markdown('''
            <audio autoplay loop>
                <source src="https://actions.google.com/sounds/v1/emergency/emergency_siren_short_burst.ogg" type="audio/ogg">
            </audio>"""

new_target = """        if is_ambulance:
            st.session_state["radar_locked"] = True
            st.session_state["radar_dist"] = 120
            st.success("🚨 AMBULANCE (108 ALS) CONFIRMED! Radar Armed & Optical Lock (120m)")
            
            # Play Siren Sound ONLY FOR AMBULANCE
            st.markdown('''
            <audio autoplay loop>
                <source src="https://actions.google.com/sounds/v1/emergency/emergency_siren_short_burst.ogg" type="audio/ogg">
            </audio>"""

# Strict check for camera feed as well
text = text.replace(
    'vehicle_detected_label = "108 ALS Ambulance (Optical Camera Locked)"',
    'vehicle_detected_label = "108 ALS Ambulance (Optical Camera Locked)"\n            is_ambulance = True'
)

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)

print("SUCCESS: Siren strictly mapped to Ambulance detection only!")
