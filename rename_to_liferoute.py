import os
import glob

# Files aur directories scan karke name replace karna
target_extensions = [".py", ".json", ".md", ".txt"]
replacements = {
    "LifeRoute AI": "LifeRoute AI",
    "liferoute ai": "liferoute ai",
    "LifeRoute": "LifeRoute",
    "liferoute": "liferoute",
    "LIFEROUTE": "LIFEROUTE"
}

modified_files = 0

for root, dirs, files in os.walk("."):
    # venv, git ya cache directories ko skip karna
    if any(ignore in root for ignore in ["venv", ".git", "__pycache__", ".streamlit"]):
        continue
    
    for file in files:
        if any(file.endswith(ext) for ext in target_extensions):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                new_content = content
                for old_val, new_val in replacements.items():
                    new_content = new_content.replace(old_val, new_val)
                
                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Updated branding in: {file_path}")
                    modified_files += 1
            except Exception as e:
                pass

print(f"\nSUCCESS: Total {modified_files} files updated to 'LifeRoute AI'!")
