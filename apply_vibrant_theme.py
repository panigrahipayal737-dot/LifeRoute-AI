import glob
import py_compile

print(">>> APPLYING VIBRANT HIGH-CONTRAST NEON THEME ACROSS ALL PAGES...")

# Common vibrant CSS injected into all pages
vibrant_css = """
<style>
    /* Dark Cockpit with Vibrant Neon Accents */
    .stApp {
        background: radial-gradient(circle at 15% 15%, #0a1128 0%, #050814 100%) !important;
        color: #f8fafc !important;
    }

    /* Vibrant Buttons */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #059669 0%, #10b981 50%, #34d399 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border: none !important;
        box-shadow: 0 4px 18px rgba(16, 185, 129, 0.45) !important;
        transition: all 0.3s ease !important;
        border-radius: 8px !important;
    }
    .stButton>button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(16, 185, 129, 0.7) !important;
    }

    /* Tab Highlights */
    button[data-baseweb="tab"] {
        font-weight: 700 !important;
        color: #94a3b8 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
    }

    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 900 !important;
    }
</style>
"""

# 1. Update streamlit_app.py CSS
try:
    with open("streamlit_app.py", "r", encoding="utf-8") as f:
        p1 = f.read()
    if "/* Dark Cockpit with Vibrant Neon Accents */" not in p1:
        p1 = p1.replace("<style>", vibrant_css + "\n<style>", 1)
        with open("streamlit_app.py", "w", encoding="utf-8") as f:
            f.write(p1)
    py_compile.compile("streamlit_app.py", doraise=True)
    print("SUCCESS: streamlit_app.py enhanced with vibrant palette!")
except Exception as e:
    print(f"Error on streamlit_app.py: {e}")

# 2. Update Hospital Admin Desk with colorful cards
hosp_files = glob.glob("pages/*Hospital*.py")
if hosp_files:
    hosp_file = hosp_files[0]
    with open(hosp_file, "r", encoding="utf-8") as f:
        h_code = f.read()

    # Vibrant Glass Cards Styling
    vibrant_hosp_styles = """
    .header-box {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(99, 102, 241, 0.2) 100%) !important;
        border: 1.5px solid rgba(56, 189, 248, 0.4) !important;
        border-radius: 14px;
        padding: 18px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.15);
    }
    .red-pill {
        background: linear-gradient(135deg, rgba(244, 63, 94, 0.25), rgba(225, 29, 72, 0.4)) !important;
        color: #fda4af !important;
        border: 1.5px solid #f43f5e !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 0.8px;
        box-shadow: 0 0 14px rgba(244, 63, 94, 0.45);
    }
    .glass-card-patient {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.85), rgba(30, 58, 138, 0.3)) !important;
        border: 1.5px solid #38bdf8 !important;
        border-radius: 14px;
        padding: 18px;
        min-height: 195px;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
    }
    .glass-card-telemetry {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.85), rgba(6, 78, 59, 0.35)) !important;
        border: 1.5px solid #22c55e !important;
        border-radius: 14px;
        padding: 18px;
        min-height: 195px;
        box-shadow: 0 0 20px rgba(34, 197, 94, 0.2);
    }
    .glass-card-staged {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.85), rgba(120, 53, 15, 0.3)) !important;
        border: 1.5px solid #f59e0b !important;
        border-radius: 14px;
        padding: 18px;
        min-height: 195px;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.2);
    }
    """

    h_code = h_code.replace(".glass-card {", vibrant_hosp_styles + "\n.glass-card {")
    h_code = h_code.replace('class="glass-card"', 'class="glass-card-patient"')
    h_code = h_code.replace(
        'class="glass-card" style="border-color: rgba(34, 197, 94, 0.35);"',
        'class="glass-card-telemetry"'
    )
    h_code = h_code.replace(
        'class="glass-card" style="border-color: rgba(234, 179, 8, 0.35);"',
        'class="glass-card-staged"'
    )

    with open(hosp_file, "w", encoding="utf-8") as f:
        f.write(h_code)
    py_compile.compile(hosp_file, doraise=True)
    print(f"SUCCESS: {hosp_file} updated with vivid neon card borders!")

# 3. Add vibrant badges to Traffic and Police rooms
for fpath in glob.glob("pages/*Police*.py") + glob.glob("pages/*Traffic*.py"):
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            txt = f.read()
        if "/* Dark Cockpit with Vibrant Neon Accents */" not in txt:
            txt = txt.replace("<style>", vibrant_css + "\n<style>", 1)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(txt)
        py_compile.compile(fpath, doraise=True)
        print(f"SUCCESS: Vibrant styles added to {fpath}")
    except Exception as e:
        print(f"Note on {fpath}: {e}")

print("\n>>> ALL PAGES NOW STYLED WITH MODERN VIBRANT PRESENTATION THEME!")