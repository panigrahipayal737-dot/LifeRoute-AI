file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# Safe initialization for active_lat and active_lon
init_snippet = """
# Resolve active coordinates for hospital distance sorting
active_lat = st.session_state.get("live_lat", 21.1762)
active_lon = st.session_state.get("live_lon", 72.8581)
"""

target_line = 'h["real_km"] = haversine_km(active_lat, active_lon, h["lat"], h["lon"])'

if target_line in code:
    # Find the loop that starts calculating distances
    # Insert active_lat and active_lon right before the loop/line
    pos = code.find(target_line)
    # Find the loop start (e.g. for h in ...)
    loop_start = code.rfind("for ", 0, pos)
    if loop_start != -1 and "active_lat = " not in code[loop_start-100:loop_start]:
        code = code[:loop_start] + init_snippet.strip() + "\n" + code[loop_start:]
    elif "active_lat = " not in code:
        code = code[:pos] + init_snippet.strip() + "\n" + code[pos:]

    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    print("SUCCESS: active_lat and active_lon defined cleanly before distance loop!")
else:
    # Fallback: define globally if exact line format varies
    import re
    code = re.sub(
        r'(for\s+\w+\s+in\s+.*?:[\s\S]*?haversine_km\s*\(\s*active_lat)',
        init_snippet.strip() + "\n\\1",
        code,
        count=1
    )
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    print("SUCCESS: active_lat patched before haversine execution!")
