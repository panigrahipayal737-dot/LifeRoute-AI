file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# 1. Helper function remove karna
if "def get_real_device_location():" in code:
    idx_start = code.find("def get_real_device_location():")
    idx_end = code.find('return 21.1762, 72.8581, "Live Device GPS (Default Node)"')
    if idx_start != -1 and idx_end != -1:
        end_line = code.find("\n", idx_end)
        code = code[:idx_start] + code[end_line + 1:]

# 2. Button block ko purani simple default state me revert karna
old_snippet = """    if st.button("📍 Auto-Detect My Live Location (Google Maps GPS)", use_container_width=True, type="primary"):
        st.session_state["pickup_location"] = "📍 LIVE: Limbayat Chauraha, Surat (Exact Device GPS)"
        st.session_state["live_lat"] = 21.1762
        st.session_state["live_lon"] = 72.8581
        st.success("✅ Device Location Detected: Limbayat Chauraha, Surat (21.1762, 72.8581)")
        st.rerun()"""

import re
# Jo bhi dynamic logic tha use simple hardcoded button se replace karein
code = re.sub(
    r'if st\.button\(["\'][^"\']*Auto-Detect My Live Location[^"\']*["\'][^)]*\):[\s\S]*?(?=\n\s*(?:st\.markdown|st\.selectbox|col|#|\n[a-zA-Z_]))',
    old_snippet + "\n\n",
    code,
    count=1
)

# Clean invisible BOM/unicode characters
code = code.replace('\ufeff', '').replace('\u200b', '').replace('\xa0', ' ')

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(code)

print("SUCCESS: Reverted to the previous stable location configuration!")
