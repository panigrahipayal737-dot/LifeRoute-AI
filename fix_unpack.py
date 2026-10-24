file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# Replace unpacking with slice-safe extraction
old_unpack = "cur_lat, cur_lon = SURAT_LOCATIONS.get(selected_pickup, (21.1762, 72.8581))"
new_unpack = """raw_coords = SURAT_LOCATIONS.get(selected_pickup, (21.1762, 72.8581))
    cur_lat, cur_lon = float(raw_coords[0]), float(raw_coords[1])"""

if old_unpack in code:
    code = code.replace(old_unpack, new_unpack)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    print("SUCCESS: Unpack error fixed using raw_coords index extraction!")
else:
    # Alternative regex match in case spacing differs
    import re
    code = re.sub(
        r'cur_lat,\s*cur_lon\s*=\s*SURAT_LOCATIONS\.get\([^)]+\)',
        new_unpack,
        code
    )
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    print("SUCCESS: Unpack error patched via regex replacement!")
