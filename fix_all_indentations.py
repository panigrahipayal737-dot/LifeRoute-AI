file_path = "streamlit_app.py"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

new_lines = []
i = 0
n = len(lines)

while i < n:
    line = lines[i].replace("\xa0", " ").replace("\ufeff", "").replace("\u200b", "")
    new_lines.append(line)
    
    # Jab bhi koi line ':' par end ho rahi ho (with, if, else, elif, for, while, def, try, except)
    stripped = line.strip()
    if stripped.endswith(":") and not stripped.startswith("#"):
        parent_indent = len(line) - len(line.lstrip(" "))
        
        # Agli non-empty line check karein
        j = i + 1
        while j < n and lines[j].strip() == "":
            new_lines.append(lines[j])
            j += 1
            
        if j < n:
            next_line = lines[j].replace("\xa0", " ").replace("\ufeff", "").replace("\u200b", "")
            next_indent = len(next_line) - len(next_line.lstrip(" "))
            
            # Agar agli line indented nahi hai, to usko parent + 4 spaces pe indent karo
            if next_indent <= parent_indent:
                # Agar line 'with' block ke andar current_radar_text ya kuch aur ho
                fixed_next = " " * (parent_indent + 4) + next_line.lstrip(" ")
                new_lines.append(fixed_next)
                i = j
                i += 1
                continue
    i += 1

# File write karein
with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.writelines(new_lines)

# Verify with Python py_compile
import py_compile
try:
    py_compile.compile(file_path, doraise=True)
    print("SUCCESS: 0 SYNTAX/INDENTATION ERRORS! File perfectly compiled.")
except py_compile.PyCompileError as e:
    # Auto patch the specific line if still flagging
    err_line = e.exc_value.lineno
    print(f"Fine-tuning line {err_line}...")
    with open(file_path, "r", encoding="utf-8") as f:
        l_all = f.readlines()
    
    # Calculate prior line indent
    k = err_line - 2
    while k >= 0 and l_all[k].strip() == "":
        k -= 1
    prev_ind = len(l_all[k]) - len(l_all[k].lstrip(" "))
    l_all[err_line - 1] = " " * (prev_ind + 4) + l_all[err_line - 1].lstrip(" ")
    
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.writelines(l_all)
    py_compile.compile(file_path, doraise=True)
    print("SUCCESS: FINAL PASS COMPILED COMPLETELY WITH 0 ERRORS!")
