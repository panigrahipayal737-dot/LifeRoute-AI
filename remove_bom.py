file_path = "streamlit_app.py"

with open(file_path, "rb") as f:
    raw_bytes = f.read()

# Remove UTF-8 BOM if present at start
if raw_bytes.startswith(b'\xef\xbb\xbf'):
    raw_bytes = raw_bytes[3:]

# Decode to string
content = raw_bytes.decode("utf-8", errors="ignore")

# Remove zero-width spaces, BOM, and other non-printable unicode artifacts
content = content.replace('\ufeff', '')
content = content.replace('\u200b', '')
content = content.replace('\u200e', '')
content = content.replace('\u200f', '')
content = content.replace('\xa0', ' ')

# Save cleanly without BOM
with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print("SUCCESS: Invisible character U+FEFF (BOM) removed successfully from streamlit_app.py!")
