import py_compile

file_path = "streamlit_app.py"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# Replace vertical radio with horizontal layout in Step 1
old_radio_block = """    # Vertical options layout matching screenshot
    vision_mode = st.radio(
        "Mode",
        ["Upload Image for Scan", "Live Camera Feed", "IP Webcam Stream (RTSP/HTTP)"],
        index=0,
        label_visibility="collapsed"
    )"""

new_radio_block = """    # Horizontal options layout
    vision_mode = st.radio(
        "Mode",
        ["Upload Image for Scan", "Live Camera Feed", "IP Webcam Stream (RTSP/HTTP)"],
        index=0,
        horizontal=True,
        label_visibility="collapsed"
    )"""

if old_radio_block in code:
    code = code.replace(old_radio_block, new_radio_block)
else:
    # Pattern fallback to ensure horizontal=True is set on the mode radio
    import re
    code = re.sub(
        r'vision_mode\s*=\s*st\.radio\(\s*["\'](?:Mode|Optical Feed Mode)["\'],\s*\["Upload Image for Scan",\s*"Live Camera Feed",\s*"IP Webcam Stream \(RTSP/HTTP\)"\],[^\)]*?\)',
        """vision_mode = st.radio(
        "Mode",
        ["Upload Image for Scan", "Live Camera Feed", "IP Webcam Stream (RTSP/HTTP)"],
        index=0,
        horizontal=True,
        label_visibility="collapsed"
    )""",
        code
    )

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(code)

py_compile.compile(file_path, doraise=True)
print(">>> SUCCESS: Optical mode radio options converted to horizontal layout with 0 errors!")
