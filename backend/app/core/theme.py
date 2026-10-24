import streamlit as st

def apply_cyber_theme():
    """
    LifeRoute AI - Premium Cyber-Tactical Design System.
    Applies custom OLED glassmorphism, glowing accents, and high-tech typography.
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;600;800&display=swap');

        /* Main App Background */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #0b1528 0%, #050b14 60%, #020408 100%) !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
            color: #e2e8f0 !important;
        }

        /* Sidebar Futuristic Styling */
        section[data-testid="stSidebar"] {
            background-color: #030712 !important;
            border-right: 1px solid rgba(56, 189, 248, 0.15) !important;
            box-shadow: 5px 0 25px rgba(0, 0, 0, 0.6) !important;
        }
        section[data-testid="stSidebar"] .stMarkdown p {
            color: #94a3b8 !important;
        }

        /* Top Header Box (Glassmorphism & Neon Cyan Border) */
        .page-header-box {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(2, 6, 23, 0.95) 100%) !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            border-radius: 16px !important;
            padding: 18px 24px !important;
            margin-bottom: 22px !important;
            box-shadow: 0 8px 32px rgba(2, 132, 199, 0.18), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(12px) !important;
        }
        .page-header-box h2 {
            background: linear-gradient(90deg, #ffffff 0%, #38bdf8 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            letter-spacing: 0.5px !important;
        }

        /* Custom Cards & Containers */
        div[data-testid="stVerticalBlock"] > div[style*="border"] {
            transition: all 0.25s ease-in-out !important;
        }
        div[data-testid="stVerticalBlock"] > div[style*="border"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 25px rgba(14, 165, 233, 0.2) !important;
        }

        /* Primary Action Buttons (Neon Emerald Gradient) */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            color: #ffffff !important;
            border: 1px solid #34d399 !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            font-family: 'JetBrains Mono', monospace !important;
            letter-spacing: 0.5px !important;
            padding: 10px 20px !important;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.35) !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #34d399 0%, #10b981 100%) !important;
            box-shadow: 0 0 30px rgba(16, 185, 129, 0.6) !important;
            transform: scale(1.01) !important;
        }

        /* Secondary Buttons */
        .stButton > button:not([kind="primary"]) {
            background: rgba(15, 23, 42, 0.85) !important;
            color: #cbd5e1 !important;
            border: 1px solid rgba(148, 163, 184, 0.25) !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:not([kind="primary"]):hover {
            background: rgba(30, 41, 59, 0.95) !important;
            border-color: #38bdf8 !important;
            color: #38bdf8 !important;
        }

        /* Inputs, Selectboxes & Number Pickers */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="input"] > div {
            background-color: rgba(11, 19, 38, 0.9) !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            border-radius: 9px !important;
            color: #ffffff !important;
        }
        div[data-baseweb="select"] > div:focus-within, 
        div[data-baseweb="input"] > div:focus-within {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.4) !important;
        }

        /* Tabs Navigation Styling */
        button[data-baseweb="tab"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            color: #94a3b8 !important;
            background: transparent !important;
            border-radius: 8px 8px 0 0 !important;
            padding: 8px 16px !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #38bdf8 !important;
            border-bottom: 2px solid #38bdf8 !important;
        }

        /* Radio Pills / Options Selection */
        div[role="radiogroup"] {
            gap: 10px !important;
        }
        div[role="radiogroup"] label {
            background: rgba(15, 23, 42, 0.7) !important;
            border: 1px solid rgba(71, 85, 105, 0.4) !important;
            border-radius: 10px !important;
            padding: 8px 14px !important;
            transition: all 0.2s ease !important;
        }
        div[role="radiogroup"] label:hover {
            border-color: #38bdf8 !important;
            background: rgba(30, 41, 59, 0.9) !important;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #030712;
        }
        ::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 4px;
            border: 1px solid rgba(56, 189, 248, 0.2);
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #0284c7;
        }
    </style>
    """, unsafe_allow_html=True)

