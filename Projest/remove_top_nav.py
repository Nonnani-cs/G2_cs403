import os
import re

directory = '/Users/atcharapornn/Desktop/Projest'
html_files = [f for f in os.listdir(directory) if f.endswith('.html')]

pattern = r'\s*<nav class="flex space-x-8 text-sm font-bold">.*?</nav>'

for filename in html_files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")

print("Done")
