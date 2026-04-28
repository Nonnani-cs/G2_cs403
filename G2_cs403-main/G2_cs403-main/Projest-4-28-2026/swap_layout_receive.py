import re
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(current_dir, 'receive.html')
with open(filepath, 'r') as f:
    content = f.read()

# Pattern for receive.html layout
# 113: <div class="flex-1 p-2 flex gap-2 overflow-hidden bg-[#fffff0] border-4 border-[#e0ebd0]">
# 114: <!-- Left Sidebar -->
# 115: <div class="w-80 border border-gray-400 bg-white flex flex-col shadow-inner">
# ...
# 187: <div class="flex-1 flex flex-col border border-gray-400 bg-white shadow-sm overflow-hidden">

pattern = r'(<div class="flex-1 p-2 flex gap-2 overflow-hidden bg-\[#fffff0\] border-4 border-\[#e0ebd0\]">)\s*(<!-- Left Sidebar -->\s*<div class="w-80 border border-gray-400 bg-white flex flex-col shadow-inner">.*?<\/div>)\s*(<!-- Right Main Area -->\s*<div class="flex-1 flex flex-col border border-gray-400 bg-white shadow-sm overflow-hidden">.*?<\/div>)\s*(<\/div>)'

match = re.search(pattern, content, re.DOTALL)
if match:
    container_start = match.group(1)
    sidebar = match.group(2)
    main_content = match.group(3)
    container_end = match.group(4)
    
    # Swap them
    new_layout = f"{container_start}\n                {main_content}\n                {sidebar}\n            {container_end}"
    # Wait, I put sidebar first in new_layout? No, sidebar was group 2.
    # To swap: main_content then sidebar.
    new_layout = f"{container_start}\n                {main_content}\n                {sidebar}\n            {container_end}"
    
    # Re-evaluating: Sidebar (group 2) is left. Main (group 3) is right.
    # To swap: Group 3 then Group 2.
    new_layout = f"{container_start}\n                {main_content}\n                {sidebar}\n            {container_end}"
    # Wait, my logic is confused. 
    # Group 2 is Sidebar (Left). Group 3 is Main (Right).
    # To move sidebar to right: Group 3 then Group 2.
    
    content = content.replace(match.group(0), f"{container_start}\n                {main_content}\n                {sidebar}\n            {container_end}")

with open(filepath, 'w') as f:
    f.write(content)

print("Layout swapped in receive.html")
