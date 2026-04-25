import re

def revert(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Revert manage.html
    if 'manage.html' in filepath:
        pattern = r'(<div class="flex-1 overflow-hidden p-2 flex gap-2">)\s*(<div class="flex-1 bg-white border border-green-300 rounded-xl shadow-sm flex flex-col overflow-hidden">.*?<\/div>)\s*(<div class="w-80 bg-white border border-green-300 rounded-xl flex flex-col shadow-sm shrink-0">.*?<\/div>)\s*(<\/div>)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            container_start = match.group(1)
            main_content = match.group(2)
            sidebar = match.group(3)
            container_end = match.group(4)
            new_layout = f"{container_start}\n                {sidebar}\n                {main_content}\n            {container_end}"
            content = content.replace(match.group(0), new_layout)
            
    # Revert receive.html
    elif 'receive.html' in filepath:
        pattern = r'(<div class="flex-1 p-2 flex gap-2 overflow-hidden bg-\[#fffff0\] border-4 border-\[#e0ebd0\]">)\s*(<!-- Right Main Area -->\s*<div class="flex-1 flex flex-col border border-gray-400 bg-white shadow-sm overflow-hidden">.*?<\/div>)\s*(<!-- Left Sidebar -->\s*<div class="w-80 border border-gray-400 bg-white flex flex-col shadow-inner">.*?<\/div>)\s*(<\/div>)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            container_start = match.group(1)
            main_content = match.group(2)
            sidebar = match.group(3)
            container_end = match.group(4)
            new_layout = f"{container_start}\n                {sidebar}\n                {main_content}\n            {container_end}"
            content = content.replace(match.group(0), new_layout)

    with open(filepath, 'w') as f:
        f.write(content)

revert('/Users/atcharapornn/Desktop/Projest/manage.html')
revert('/Users/atcharapornn/Desktop/Projest/receive.html')
print("Reverted swap in both files.")
