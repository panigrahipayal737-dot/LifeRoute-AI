file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# 1. Clean out the misplaced snippet wherever it got inserted
code = code.replace("""if "radar_locked" not in st.session_state:
    st.session_state["radar_locked"] = False
if "radar_dist" not in st.session_state:
    st.session_state["radar_dist"] = 450""", "")

code = code.replace("""# Ensure radar session state variables are properly initialized
if "radar_locked" not in st.session_state:
    st.session_state["radar_locked"] = False
if "radar_dist" not in st.session_state:
    st.session_state["radar_dist"] = 450""", "")

# 2. Safely initialize at global scope right after st.set_page_config
global_init = """
# --- GLOBAL RADAR SESSION STATE INITIALIZATION ---
if "radar_locked" not in st.session_state:
    st.session_state["radar_locked"] = False
if "radar_dist" not in st.session_state:
    st.session_state["radar_dist"] = 450
"""

if "GLOBAL RADAR SESSION STATE INITIALIZATION" not in code:
    pos = code.find("st.set_page_config")
    if pos != -1:
        end_call = code.find(")", pos)
        code = code[:end_call + 1] + "\n" + global_init + code[end_call + 1:]
    else:
        code = global_init + "\n" + code

# 3. Fix the with block around current_radar_text
with_pattern = 'current_radar_text = f"LOCKED: {st.session_state.radar_dist}m (Armed)" if st.session_state.radar_locked else "Awaiting Camera Optical Lock"'

lines = code.split("\n")
fixed_lines = []
for i, line in enumerate(lines):
    if with_pattern in line:
        # Detect if previous line was a 'with' statement
        prev_idx = i - 1
        while prev_idx >= 0 and lines[prev_idx].strip() == "":
            prev_idx -= 1
        
        if prev_idx >= 0 and lines[prev_idx].strip().startswith("with "):
            with_indent = len(lines[prev_idx]) - len(lines[prev_idx].lstrip())
            fixed_lines.append(" " * (with_indent + 4) + line.strip())
            continue
    fixed_lines.append(line)

final_code = "\n".join(fixed_lines)

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(final_code)

print("SUCCESS: Radar variables moved to global scope and with-block indentation fixed cleanly!")
