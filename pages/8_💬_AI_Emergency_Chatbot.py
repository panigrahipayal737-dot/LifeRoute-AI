import streamlit as st
from backend import emergency_db

st.set_page_config(page_title="AI Emergency Chatbot", page_icon="💬", layout="wide")

st.markdown('''
<style>
    .stApp { background: radial-gradient(circle at 15% 15%, #0a1128 0%, #050814 100%) !important; color: #f8fafc !important; }
    section[data-testid="stSidebar"] { background: linear-gradient(180deg, #070e24 0%, #0a1738 50%, #040918 100%) !important; border-right: 1.5px solid rgba(56, 189, 248, 0.3) !important; }
    section[data-testid="stSidebar"] a { background: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-radius: 10px !important; padding: 9px 14px !important; margin: 4px 0 !important; font-weight: 700 !important; color: #cbd5e1 !important; }
    section[data-testid="stSidebar"] a[aria-current="page"] { background: linear-gradient(90deg, rgba(2, 132, 199, 0.5), rgba(59, 130, 246, 0.5)) !important; border: 1.5px solid #38bdf8 !important; color: #ffffff !important; }
    [data-testid="stSidebarNav"] > div:first-child { display: none !important; }
</style>
''', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('''
    <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.25) 0%, rgba(168, 85, 247, 0.25) 100%); border: 2px solid #38bdf8; border-radius: 14px; padding: 16px 12px; text-align: center; margin-top: -30px; margin-bottom: 22px;">
        <div style="font-size: 32px; margin-bottom: 4px;">🚨</div>
        <div style="font-size: 21px; font-weight: 900; background: linear-gradient(90deg, #38bdf8, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            PulseRoute AI
        </div>
        <div style="display: inline-block; background: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e; color: #4ade80; border-radius: 12px; padding: 3px 10px; font-size: 10px; font-weight: 800; margin-top: 6px;">
            ● SURAT V2X CORRIDOR ACTIVE
        </div>
    </div>
    ''', unsafe_allow_html=True)

inc = emergency_db.get_latest_incident()

st.markdown('''
<div style="background: linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,41,59,0.85)); border: 1.5px solid rgba(168,85,247,0.4); border-radius:14px; padding:18px 24px; display:flex; justify-content:space-between; align-items:center; margin-bottom:18px;">
    <div>
        <div style="font-size: 20px; font-weight: 900; color: #c084fc; display:flex; align-items:center; gap:8px;">
            <span>💬</span> 108 EMERGENCY MEDICAL TRIAGE ASSISTANT (AI AGENT)
        </div>
        <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Real-Time Clinical Protocol • First Aid Guidance • Live Dispatch Status</div>
    </div>
    <div style="background:rgba(168,85,247,0.2); color:#c084fc; border:1.5px solid #a855f7; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:900;">
        AI AGENT ONLINE
    </div>
</div>
''', unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": f"Hello! I am PulseRoute AI Assistant. Active incident **{inc.get('Token')}** is currently being routed to **{inc.get('Hospital')}**. How can I assist you with clinical triage or status updates?"}
    ]

# Render chat messages
for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_query = st.chat_input("Ask about active dispatch status, CPR steps, ICU beds, or blood match...")

if user_query:
    st.session_state["chat_history"].append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    q = user_query.lower()
    if "status" in q or "token" in q or "where" in q:
        reply = f"🚨 **Live Incident Status ({inc.get('Token')}):** Ambulance {inc.get('Fleet')} is en-route from {inc.get('Origin')} to {inc.get('Hospital')}. Corridor {inc.get('Corridor')} is green-preempted. Estimated ETA: ~{inc.get('ETA')}."
    elif "cpr" in q or "heart" in q or "chest" in q:
        reply = "🫀 **Emergency CPR Protocol:** 1. Place hands in center of chest. 2. Push hard and fast (100-120 compressions per minute). 3. Allow full chest recoil. 4. Continue until paramedic arrives."
    elif "bed" in q or "hospital" in q:
        reply = f"🏥 **Bed Allocation:** Bed **{inc.get('Bed')}** is officially locked at {inc.get('Hospital')} under attending doctor {inc.get('Doctor')}."
    elif "blood" in q:
        reply = f"🩸 **Blood Matching:** Patient requires **{inc.get('BloodGroup')}** blood. Units are pre-reserved at the hospital blood bank."
    else:
        reply = f"I have logged your clinical query regarding '{user_query}'. For urgent on-ground dispatch coordination, 108 Emergency Control Room is actively monitoring."

    st.session_state["chat_history"].append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
