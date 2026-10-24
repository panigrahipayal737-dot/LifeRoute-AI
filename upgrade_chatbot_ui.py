import streamlit as st
import time

st.set_page_config(page_title="LifeRoute AI Chat", page_icon="💬", layout="wide")

# Modern ChatGPT/Gemini Style CSS Theme
st.markdown('''
<style>
    .chat-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 18px;
        background: linear-gradient(90deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.7));
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
    }
    .chat-pill {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .stChatMessage {
        border-radius: 16px !important;
        margin-bottom: 12px;
    }
    .user-bubble {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
</style>
''', unsafe_allow_html=True)

# Top Header Bar
st.markdown('''
<div class="chat-header">
    <div style="font-size: 24px;">🤖</div>
    <div style="flex-grow: 1;">
        <div style="font-size: 17px; font-weight: 800; color: #f8fafc; letter-spacing: -0.3px;">LifeRoute AI Copilot</div>
        <div style="font-size: 12px; color: #94a3b8;">Autonomous Clinical Staging & Emergency Traffic Navigator (Surat Fleet)</div>
    </div>
    <div class="chat-pill">GPT-4o / GEMINI ACTIVE</div>
</div>
''', unsafe_allow_html=True)

# Session State for Messages
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "👋 **Hello Dispatcher! I am your LifeRoute AI Assistant.**\n\nI can help you with:\n- 🚦 Dynamic green-wave route clearances across Surat corridors\n- 🏥 Specialized hospital bed & ICU triage recommendations\n- 🫀 Patient vital staging (SpO2, pulse, GCS) protocols\n\nWhat is your emergency dispatch query?"}
    ]

# Render Message History
for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# Quick Suggested Prompts (Like Gemini & ChatGPT Chips)
st.markdown("<div style='font-size: 11px; font-weight: 700; color: #64748b; margin-top: 15px; margin-bottom: 6px;'>SUGGESTED DISPATCH QUERIES:</div>", unsafe_allow_html=True)
col_q1, col_q2, col_q3 = st.columns(3)

def inject_prompt(p_text):
    st.session_state["pending_prompt"] = p_text

with col_q1:
    if st.button("🚨 Clear Majura to Civil Hospital", use_container_width=True):
        inject_prompt("Clear traffic signals between Majura Gate and New Civil Hospital immediately.")
with col_q2:
    if st.button("🫀 SpO2 dropping to 82% Advice", use_container_width=True):
        inject_prompt("Patient SpO2 dropped below 84% with cardiac arrest history. Suggest immediate ICU staging.")
with col_q3:
    if st.button("🏥 Closest Trauma Care in Limbayat", use_container_width=True):
        inject_prompt("Which is the closest trauma center from Limbayat Chauraha with active ventilator beds?")

# User Chat Input Handling
user_input = st.chat_input("Ask LifeRoute Copilot anything about route, signals, or patient care...")

pending = st.session_state.pop("pending_prompt", None)
prompt = user_input or pending

if prompt:
    # Append user prompt
    st.session_state["chat_history"].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Intelligent Contextual AI Response Generator
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        
        q_lower = prompt.lower()
        if any(w in q_lower for w in ["clear", "signal", "traffic", "green", "route", "majura"]):
            resp = f'''✅ **Corridor Preemption Protocol Activated**
* **Target Corridor:** Majura Sector $\rightarrow$ Ring Road $\rightarrow$ New Civil
* **Signal Status:** Overriding Junction 4 & Junction 6 to **GREEN WAVE (TTL: 180s)**
* **Estimated Speed Advantage:** +38 km/h over peak gridlock
* **V2X Beacon Status:** 5.9 GHz beacon transmitting preemption request.'''
        elif any(w in q_lower for w in ["spo2", "cardiac", "pulse", "bp", "icu", "ventilator"]):
            resp = f'''⚠️ **Critical Patient Alert Protocol (High-Risk)**
* **Assessment:** Hypoxemia with respiratory depression detected.
* **Clinical Action:** 
  1. Switch to High-Flow Nasal Cannula (12-15 L/min) or bag-valve mask.
  2. Telemetry automatically transmitted to **SMIMER Emergency Room**.
  3. Pre-notifying Trauma Bay 1: Readying Bag-Valve, Crash Cart & Defibrillator.'''
        elif any(w in q_lower for w in ["hospital", "closest", "bed", "limbayat"]):
            resp = f'''🏥 **Triangulated Nearest Facility Matrix**
1. **SMIMER Hospital & Medical College** (~2.8 km, 6 mins via Green Wave)
   - *Status:* 4 ICU Beds, 2 Active Cath Labs available.
2. **New Civil Hospital (NCH), Majura Gate** (~4.1 km, 9 mins)
   - *Status:* Level-1 Government Trauma Center, Full Blood Bank ready.'''
        else:
            resp = f'''Understood dispatcher request: *"{prompt}"*. LifeRoute core system is synchronizing live GPS nodes, traffic signal actuators, and clinical hospital triage desks across Surat.'''

        # Simulate natural streaming output (like Claude / ChatGPT)
        full_res = ""
        for chunk in resp.split(" "):
            full_res += chunk + " "
            time.sleep(0.04)
            message_placeholder.markdown(full_res + "▌")
        message_placeholder.markdown(full_res)
        
        st.session_state["chat_history"].append({"role": "assistant", "content": full_res})
