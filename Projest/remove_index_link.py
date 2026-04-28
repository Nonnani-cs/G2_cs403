import os
import re

directory = current_dir
html_files = [f for f in os.listdir(directory) if f.endswith('.html')]

pattern = r'\s*<a href="index\.html"[^>]*>.*?<span[^>]*>หน้าหลัก</span>.*?</a>\s*'
pattern_active = r'\s*<div[^>]*active-link[^>]*>.*?<span[^>]*>หน้าหลัก</span>.*?</div>\s*'

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove index.html link from nav
    new_content = re.sub(pattern, '\n            ', content, flags=re.DOTALL)
    new_content = re.sub(pattern_active, '\n            ', new_content, flags=re.DOTALL)
    
    # Fallback to broader match if the strict one didn't work
    if new_content == content:
         pattern2 = r'\s*<a href="index\.html"[^>]*>.*?หน้าหลัก.*?</a>\s*'
         pattern_active2 = r'\s*<div[^>]*active-link[^>]*>.*?หน้าหลัก.*?</div>\s*'
         new_content = re.sub(pattern2, '\n            ', new_content, flags=re.DOTALL)
         new_content = re.sub(pattern_active2, '\n            ', new_content, flags=re.DOTALL)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")

print("Done")
