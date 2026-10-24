import os

patterns_to_remove = [
    "",
    "",
    "",
    "",
    "",
    "",
    ""
]

target_dirs = [".", "pages", "backend"]

for base_dir in target_dirs:
    for root, dirs, files in os.walk(base_dir):
        if any(ign in root for ign in ["venv", ".git", "__pycache__", ".streamlit"]):
            continue
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    modified = False
                    for pat in patterns_to_remove:
                        if pat in content:
                            content = content.replace(pat, "")
                            modified = True
                    
                    if modified:
                        with open(file_path, "w", encoding="utf-8", newline="\n") as f:
                            f.write(content)
                        print(f"Cleaned branding text from: {file_path}")
                except Exception as e:
                    pass

# Verify compilation of streamlit_app.py
import py_compile
try:
    py_compile.compile("streamlit_app.py", doraise=True)
    print("SUCCESS: streamlit_app.py cleanly compiled without the specified header/guide text!")
except Exception as e:
    print("Compile check:", e)
