import streamlit as st
import numpy as np
import time
import random
from backend.app.services.ann_service import ann_engine
from backend.app.services.traffic_controller import traffic_fsm
from backend.app.services.corridor_service import corridor_manager

st.set_page_config(page_title="AI Smart Traffic & Green Corridor", layout="wide", page_icon="??")

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #0b0f19; }
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    .signal-box { padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 8px; }
    .sig-green { background-color: #065f46; color: #34d399; border: 1px solid #059669; }
    .sig-yellow { background-color: #713f12; color: #facc15; border: 1px solid #ca8a04; }
    .sig-red { background-color: #7f1d1d; color: #f87171; border: 1px solid #dc2626; }
</style>
""", unsafe_allow_html=True)

st.title("?? ANN Intelligent Emergency Traffic & Green Corridor System")
st.caption("AI-driven Priority Decision Engine • Multi-Signal Coordinated Corridor • Hospital & Police Integration")

# Sidebar Controls
st.sidebar.header("??? Simulation & Manual Override")
sim_mode = st.sidebar.radio("Mode", ["Auto-Simulate Stream", "Manual Trigger"])

if "step_count" not in st.session_state:
    st.session_state.step_count = 0

# Grid Layout
col_left, col_right = st.columns([2, 1])

# Simulation Logic
directions = ["NORTH", "SOUTH", "EAST", "WEST"]

if sim_mode == "Auto-Simulate Stream":
    st.session_state.step_count += 1
    is_emergency = (st.session_state.step_count % 3 == 0)
    
    if is_emergency:
        amb_dir = random.choice(directions)
        amb_dist = round(random.uniform(250.0, 850.0), 1)
        amb_eta = round(amb_dist / (60 * 1000 / 60), 2)
    else:
        amb_dir = "NONE"
        amb_dist = -1.0
        amb_eta = -1.0
        
    payload = {
        "current_green": traffic_fsm.active_green,
        "vehicles_n": random.randint(5, 50),
        "vehicles_s": random.randint(5, 50),
        "vehicles_e": random.randint(5, 50),
        "vehicles_w": random.randint(5, 50),
        "wait_n": random.randint(10, 60),
        "wait_s": random.randint(10, 60),
        "wait_e": random.randint(10, 60),
        "wait_w": random.randint(10, 60),
        "has_ambulance": is_emergency,
        "amb_direction": amb_dir,
        "amb_distance_m": amb_dist,
        "amb_eta_min": amb_eta
    }
else:
    # Manual Trigger Options
    is_emergency = st.sidebar.checkbox("Trigger Ambulance Emergency", value=True)
    amb_dir = st.sidebar.selectbox("Ambulance Direction", directions, index=0)
    amb_dist = st.sidebar.slider("Distance (meters)", 100.0, 1200.0, 600.0)
    amb_eta = round(amb_dist / (60 * 1000 / 60), 2)
    
    payload = {
        "current_green": traffic_fsm.active_green,
        "vehicles_n": 25, "vehicles_s": 15, "vehicles_e": 30, "vehicles_w": 10,
        "wait_n": 20, "wait_s": 10, "wait_e": 40, "wait_w": 15,
        "has_ambulance": is_emergency,
        "amb_direction": amb_dir if is_emergency else "NONE",
        "amb_distance_m": amb_dist if is_emergency else -1.0,
        "amb_eta_min": amb_eta if is_emergency else -1.0
    }

# Run ANN Inference
prediction = ann_engine.predict_priority(payload)
target_lane = prediction["predicted_priority"]
confidence = prediction["confidence"]

# State Machine Execution
if payload["has_ambulance"]:
    traffic_fsm.signals = {d: "RED" for d in directions}
    traffic_fsm.signals[target_lane] = "GREEN"
    traffic_fsm.active_green = target_lane
    corridor_manager.corridor_active = True
else:
    traffic_fsm.signals = {d: "RED" for d in directions}
    traffic_fsm.signals[target_lane] = "GREEN"
    traffic_fsm.active_green = target_lane
    corridor_manager.corridor_active = False

# Render Left Column: Digital Twin & ANN Metrics
with col_left:
    st.subheader("?? Multi-Intersection Coordinated Nodes")
    
    if corridor_manager.corridor_active:
        st.error(f"?? EMERGENCY GREEN CORRIDOR ACTIVE: PRIORITY TO [{target_lane}] (ETA: {amb_eta} min)")
    else:
        st.success(f"?? NORMAL DENSITY FLOW: ACTIVE SIGNAL [{traffic_fsm.active_green}]")

    j_col1, j_col2, j_col3 = st.columns(3)
    
    with j_col1:
        st.markdown("**Node J-01 (Cross Road)**")
        for d in ["NORTH", "SOUTH", "EAST", "WEST"]:
            state = traffic_fsm.signals[d]
            cls = "sig-green" if state == "GREEN" else ("sig-yellow" if state == "YELLOW" else "sig-red")
            st.markdown(f"<div class='signal-box {cls}'>{d}: {state}</div>", unsafe_allow_html=True)

    with j_col2:
        st.markdown("**Node J-02 (Hospital Ave)**")
        for d in ["NORTH", "SOUTH", "EAST", "WEST"]:
            state = "GREEN" if (corridor_manager.corridor_active and d == target_lane) else ("RED" if corridor_manager.corridor_active else ("GREEN" if d=="EAST" else "RED"))
            cls = "sig-green" if state == "GREEN" else "sig-red"
            st.markdown(f"<div class='signal-box {cls}'>{d}: {state}</div>", unsafe_allow_html=True)

    with j_col3:
        st.markdown("**Node J-03 (Care Center)**")
        for d in ["NORTH", "SOUTH", "EAST", "WEST"]:
            state = "GREEN" if (corridor_manager.corridor_active and d == target_lane) else ("RED" if corridor_manager.corridor_active else ("GREEN" if d=="WEST" else "RED"))
            cls = "sig-green" if state == "GREEN" else "sig-red"
            st.markdown(f"<div class='signal-box {cls}'>{d}: {state}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("?? ANN Priority & Lane Probabilities")
    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted Priority", target_lane)
    m2.metric("ANN Confidence", f"{confidence * 100:.1f}%")
    m3.metric("Buffer Phase", "3.0s Safe Yellow")

# Render Right Column: Hospital & Police Portals
with col_right:
    st.subheader("?? Hospital Intake Portal")
    if payload["has_ambulance"]:
        st.info(f"**Vehicle ID:** AMB-108 (ICU Unit)\n\n**ETA:** {amb_eta} mins\n\n**Bed Status:** Confirmed (#ICU-04)")
    else:
        st.write("No incoming critical emergencies.")

    st.markdown("---")
    st.subheader("?? Police Traffic Control")
    st.write(f"**Corridor Route:** J-01 ? J-02 ? J-03")
    st.write(f"**Safe Transition Buffer:** 3.0s Yellow Clearance Active")
    st.write(f"**Current Green:** {traffic_fsm.active_green}")

if sim_mode == "Auto-Simulate Stream":
    time.sleep(3)
    st.rerun()

