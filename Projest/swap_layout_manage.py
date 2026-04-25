import re

filepath = '/Users/atcharapornn/Desktop/Projest/manage.html'
with open(filepath, 'r') as f:
    content = f.read()

# Pattern to find the flex container and its two main children
pattern = r'(<div class="flex-1 overflow-hidden p-2 flex gap-2">)\s*(<div class="w-80 bg-white border border-green-300 rounded-xl flex flex-col shadow-sm shrink-0">.*?<\/div>)\s*(<div class="flex-1 bg-white border border-green-300 rounded-xl shadow-sm flex flex-col overflow-hidden">.*?<\/div>)\s*(<\/div>)'

match = re.search(pattern, content, re.DOTALL)
if match:
    container_start = match.group(1)
    sidebar = match.group(2)
    main_content = match.group(3)
    container_end = match.group(4)
    
    # Swap them
    new_layout = f"{container_start}\n                {main_content}\n                {sidebar}\n            {container_end}"
    content = content.replace(match.group(0), new_layout)

with open(filepath, 'w') as f:
    f.write(content)

print("Layout swapped in manage.html")
