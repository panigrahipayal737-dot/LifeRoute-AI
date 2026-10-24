file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# Session state initialization snippet
radar_init_snippet = """
# Ensure radar session state variables are properly initialized
if "radar_locked" not in st.session_state:
    st.session_state["radar_locked"] = False
if "radar_dist" not in st.session_state:
    st.session_state["radar_dist"] = 450
"""

target_line = 'current_radar_text = f"LOCKED: {st.session_state.radar_dist}m (Armed)" if st.session_state.radar_locked else "Awaiting Camera Optical Lock"'

if target_line in code:
    pos = code.find(target_line)
    code = code[:pos] + radar_init_snippet.strip() + "\n" + code[pos:]
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    print("SUCCESS: radar_locked and radar_dist initialized cleanly before line 636!")
else:
    # Top-level fallback insertion
    search_marker = "st.set_page_config"
    pos = code.find(search_marker)
    if pos != -1:
        end_cfg = code.find(")", pos)
        code = code[:end_cfg + 1] + "\n" + radar_init_snippet + code[end_cfg + 1:]
    else:
        code = radar_init_snippet + "\n" + code
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    print("SUCCESS: radar session variables initialized at page startup!")
