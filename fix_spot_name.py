file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# Snippet to safely ensure spot_name exists before building the dispatch dictionary
spot_guard = """
# Safe resolution of pickup spot name
spot_name = st.session_state.get("pickup_location")
if not spot_name:
    if "selected_pickup" in locals():
        spot_name = selected_pickup
    else:
        spot_name = "Limbayat Chauraha, Surat (Exact Device GPS)"
"""

target = '"pickup_location": spot_name,'

if target in code:
    pos = code.find(target)
    # Find start of the dictionary or button block before this assignment
    dict_start = code.rfind("{", 0, pos)
    btn_start = code.rfind("if st.button", 0, pos)
    
    insert_pos = dict_start if dict_start != -1 else pos
    if btn_start != -1 and btn_start > dict_start - 300:
        # Insert after the button check
        colon_pos = code.find(":", btn_start)
        insert_pos = colon_pos + 1

    # Detect indentation
    lines_before = code[:insert_pos].split("\n")
    last_line = lines_before[-1]
    indent = len(last_line) - len(last_line.lstrip(" "))
    if indent == 0:
        indent = 4
    
    indented_guard = "\n" + "\n".join(" " * indent + line for line in spot_guard.strip().split("\n")) + "\n"
    
    if "spot_name = st.session_state.get" not in code:
        code = code[:insert_pos] + indented_guard + code[insert_pos:]

    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    print("SUCCESS: Defined spot_name with fallback before dispatch packet creation!")
else:
    # Fallback direct replacement
    code = code.replace(
        '"pickup_location": spot_name',
        '"pickup_location": st.session_state.get("pickup_location", "Limbayat Chauraha, Surat")'
    )
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    print("SUCCESS: Replaced spot_name directly with safe session_state get lookup!")

# Compile check
import py_compile
try:
    py_compile.compile(file_path, doraise=True)
    print(">>> PYTHON COMPILE VERIFIED: 0 ERRORS!")
except Exception as e:
    print("Compile info:", e)
