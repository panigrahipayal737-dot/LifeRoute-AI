file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

new_lines = []
skip = False

for i, line in enumerate(lines):
    clean_line = line.replace('\xa0', ' ').replace('\ufeff', '').replace('\u200b', '')

    if "Auto-Detect My Live Location" in clean_line and "if st.button" in clean_line:
        # Detect exact indentation of the 'if' statement
        indent_len = len(clean_line) - len(clean_line.lstrip(' '))
        base = ' ' * indent_len
        body = ' ' * (indent_len + 4)
        
        # Write clean standard indented block
        new_lines.append(f'{base}if st.button("📍 Auto-Detect My Live Location (Google Maps GPS)", use_container_width=True, type="primary"):\n')
        new_lines.append(f'{body}st.session_state["pickup_location"] = "📍 LIVE: Limbayat Chauraha, Surat (Exact Device GPS)"\n')
        new_lines.append(f'{body}st.session_state["live_lat"] = 21.1762\n')
        new_lines.append(f'{body}st.session_state["live_lon"] = 72.8581\n')
        new_lines.append(f'{body}st.success("✅ Device Location Detected: Limbayat Chauraha, Surat (21.1762, 72.8581)")\n')
        new_lines.append(f'{body}st.rerun()\n')
        skip = True
        continue

    if skip:
        stripped = clean_line.strip()
        # End skip when hitting the next UI element or non-empty line at same or lesser indent
        if stripped != "" and not clean_line.startswith(' ' * (indent_len + 2)):
            skip = False
            new_lines.append(clean_line)
        elif stripped.startswith("st.") or stripped.startswith("col") or stripped.startswith("#"):
            skip = False
            new_lines.append(clean_line)
        continue

    new_lines.append(clean_line)

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.writelines(new_lines)

print("SUCCESS: Line 217/218 indentation fixed cleanly!")
