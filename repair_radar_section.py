file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Replace non-breaking spaces and invisible characters
text = text.replace("\xa0", " ").replace("\ufeff", "").replace("\u200b", "")

# Search for the start of the radar column block and the end before step 3 or patient details
target_var = "current_radar_text"
idx = text.find(target_var)

if idx != -1:
    # Find the nearest "with " statement before this line
    with_pos = text.rfind("with ", 0, idx)
    # Find the end of this sub-block (next step or next top-level markdown)
    next_step = text.find("Step 3", idx)
    if next_step == -1:
        next_step = text.find("st.markdown", idx + 200)

    # Detect the indentation of the "with" statement
    line_start = text.rfind("\n", 0, with_pos) + 1
    indent_spaces = with_pos - line_start
    b_indent = " " * indent_spaces
    i_indent = " " * (indent_spaces + 4)

    # Extract the column variable name (e.g., col_rad, col2, etc.)
    with_line = text[with_pos:text.find("\n", with_pos)]
    
    clean_radar_block = f"""{with_line}
{i_indent}if "radar_locked" not in st.session_state:
{i_indent}    st.session_state["radar_locked"] = False
{i_indent}if "radar_dist" not in st.session_state:
{i_indent}    st.session_state["radar_dist"] = 450

{i_indent}current_radar_text = f"LOCKED: {{st.session_state.radar_dist}}m (Armed)" if st.session_state.radar_locked else "Awaiting Camera Optical Lock"
{i_indent}current_radar_col = "#4ade80" if st.session_state.radar_locked else "#cbd5e1"

{i_indent}st.markdown(f'''
{i_indent}<div style="background:rgba(15,23,42,0.85); border:1px solid #334155; border-radius:10px; padding:12px 16px; margin-top:8px;">
{i_indent}    <div style="font-size:11px; color:#94a3b8; font-weight:bold;">CAMERA RADAR LOCK</div>
{i_indent}    <div style="font-size:13.5px; color:{{current_radar_col}}; font-weight:900; margin-top:3px;">{{current_radar_text}}</div>
{i_indent}</div>
{i_indent}''', unsafe_allow_html=True)
"""
    # Find end of this broken segment (where next unindented block begins)
    lines = text[with_pos:].split("\n")
    cut_idx = len(lines)
    for k in range(1, len(lines)):
        l_str = lines[k]
        stripped = l_str.strip()
        # If line starts at base indent or is a major step header
        if stripped != "" and (len(l_str) - len(l_str.lstrip(" "))) <= indent_spaces and not stripped.startswith("#"):
            cut_idx = k
            break
            
    segment_to_replace = "\n".join(lines[:cut_idx])
    text = text.replace(segment_to_replace, clean_radar_block.rstrip("\n"))

    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("SUCCESS: Radar block cleanly rewritten and aligned!")

# Full python compile test
import py_compile
try:
    py_compile.compile(file_path, doraise=True)
    print("\n>>> 0 ERRORS! File compiled successfully into bytecode!")
except py_compile.PyCompileError as e:
    print(f"\nCompile issue remaining: {e}")
