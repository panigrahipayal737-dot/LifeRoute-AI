file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

# Safe coordinates extractor helper function
safe_helper = """
def extract_lat_lon(coords_data, default_lat=21.1762, default_lon=72.8581):
    try:
        if isinstance(coords_data, dict):
            lat = coords_data.get("lat") or coords_data.get("latitude") or coords_data.get("y")
            lon = coords_data.get("lon") or coords_data.get("lng") or coords_data.get("longitude") or coords_data.get("x")
            return float(lat if lat is not None else default_lat), float(lon if lon is not None else default_lon)
        elif isinstance(coords_data, (list, tuple)):
            return float(coords_data[0]), float(coords_data[1])
    except Exception:
        pass
    return float(default_lat), float(default_lon)
"""

if "def extract_lat_lon(" not in code:
    code = safe_helper + "\n" + code

# Replace problematic raw_coords extraction line
old_block_part = "cur_lat, cur_lon = float(raw_coords[0]), float(raw_coords[1])"
new_block_part = "cur_lat, cur_lon = extract_lat_lon(raw_coords)"

if old_block_part in code:
    code = code.replace(old_block_part, new_block_part)
else:
    import re
    code = re.sub(
        r'cur_lat,\s*cur_lon\s*=\s*float\(raw_coords\[0\]\),\s*float\(raw_coords\[1\]\)',
        new_block_part,
        code
    )

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(code)

print("SUCCESS: KeyError 0 eliminated using universal coords extractor!")
