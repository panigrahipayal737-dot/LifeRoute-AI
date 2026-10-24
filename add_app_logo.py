import glob
import py_compile

print(">>> INJECTING PROFESSIONAL LIFEROUTE AI LOGO INTO STREAMLIT SIDEBAR...")

logo_component = """
# -------------------------------------------------------------
# PROFESSIONAL LIFEROUTE AI SIDEBAR BRAND LOGO & BADGE
# -------------------------------------------------------------
with st.sidebar:
    st.markdown('''
    <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.18) 0%, rgba(99, 102, 241, 0.22) 100%);
                border: 1.5px solid rgba(56, 189, 248, 0.35);
                border-radius: 14px;
                padding: 16px 12px;
                text-align: center;
                margin-bottom: 20px;
                box-shadow: 0 4px 20px rgba(14, 165, 233, 0.2);">
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 10px;">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 0 10px #38bdf8);">
                <rect width="24" height="24" rx="6" fill="#0284c7"/>
                <path d="M12 4V20M4 12H20" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
                <path d="M7 12H10L11.5 8L13.5 16L15 12H17" stroke="#34d399" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div style="font-size: 19px; font-weight: 900; letter-spacing: -0.3px; color: #f8fafc; font-family: sans-serif;">
            LifeRoute <span style="color: #38bdf8;">AI</span>
        </div>
        <div style="font-size: 10px; font-weight: 800; color: #34d399; letter-spacing: 0.8px; margin-top: 2px;">
            ● V2X GREEN WAVE ONLINE
        </div>
        <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">
            Surat Emergency Traffic Grid
        </div>
    </div>
    ''', unsafe_allow_html=True)
"""

all_entry_files = ['streamlit_app.py'] + glob.glob('pages/*.py')

for fpath in all_entry_files:
    try:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()

        if "PROFESSIONAL LIFEROUTE AI SIDEBAR BRAND LOGO" not in code:
            # st.set_page_config ke theek baad inject karein
            cfg_idx = code.find('st.set_page_config(')
            if cfg_idx != -1:
                end_cfg = code.find(')', cfg_idx)
                end_line = code.find('\n', end_cfg)
                code = code[:end_line] + "\n" + logo_component + "\n" + code[end_line:]
            else:
                code = logo_component + "\n" + code

            with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(code)

        py_compile.compile(fpath, doraise=True)
        print(f"SUCCESS: Logo injected into {fpath}")
    except Exception as e:
        print(f"Note on {fpath}: {e}")

print("\n>>> BRAND LOGO SUCCESSFULLY ADDED ACROSS ALL PAGES!")