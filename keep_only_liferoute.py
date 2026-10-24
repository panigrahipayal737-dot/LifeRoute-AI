import os
import re

files_to_check = ["streamlit_app.py"]
if os.path.exists("pages"):
    for f in os.listdir("pages"):
        if f.endswith(".py"):
            files_to_check.append(os.path.join("pages", f))

for file_path in files_to_check:
    if not os.path.exists(file_path):
        continue
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Title kiva header la fakatch "LifeRoute" theva
    content = re.sub(r'LifeRoute\s*(AI)?\s*[-–—:]?\s*[^\n"\'<]*', 'LifeRoute', content)
    
    # Extra sub-lines, developer ani guide related text clean kara
    phrases_to_clear = [
        "Autonomous Optical V2X Emergency Traffic Preemption",
        "Dynamic Clinical Staging Matrix",
        "Developed by: Payal Panigrahi & Damini Suryavanshi",
        "Payal Panigrahi & Damini Suryavanshi",
        "Guide: Ms. Donika Mali",
        "Ms. Donika Mali",
        "Target City: Surat, Gujarat"
    ]
    for p in phrases_to_clear:
        content = content.replace(p, "")

    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"Updated {file_path} -> Only 'LifeRoute' preserved.")

import py_compile
py_compile.compile("streamlit_app.py", doraise=True)
print("SUCCESS: Fakt 'LifeRoute' thevle ahe ani baki sarva remove zale!")
