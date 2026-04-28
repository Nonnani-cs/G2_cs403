import os
import re

directory = current_dir
html_files = [f for f in os.listdir(directory) if f.endswith('.html')]

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the <nav> block
    nav_match = re.search(r'(<nav[^>]*>)(.*?)(</nav>)', content, flags=re.DOTALL)
    if nav_match:
        nav_start, nav_inner, nav_end = nav_match.groups()
        
        # Remove dispense links
        nav_inner = re.sub(r'\s*<a href="dispense\.html"[^>]*>.*?จัดการใบสั่งยา.*?</a>\s*', '\n            ', nav_inner, flags=re.DOTALL)
        nav_inner = re.sub(r'\s*<div[^>]*active-link[^>]*>.*?จัดการใบสั่งยา.*?</div>\s*', '\n            ', nav_inner, flags=re.DOTALL)
        
        # Remove prescription links
        nav_inner = re.sub(r'\s*<a href="prescription\.html"[^>]*>.*?จ่ายยา.*?</a>\s*', '\n            ', nav_inner, flags=re.DOTALL)
        nav_inner = re.sub(r'\s*<div[^>]*active-link[^>]*>.*?จ่ายยา.*?</div>\s*', '\n            ', nav_inner, flags=re.DOTALL)
        
        # Clean up double newlines
        nav_inner = re.sub(r'\n\s*\n', '\n', nav_inner)
        
        content = content[:nav_match.start()] + nav_start + nav_inner + nav_end + content[nav_match.end():]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
print("Sidebar updated.")
