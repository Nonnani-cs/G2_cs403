import re

filepath = '/Users/atcharapornn/Desktop/Projest/manage.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Re-construct the main area cleanly
main_area_pattern = r'(<div class="flex-1 p-2 flex gap-2 overflow-hidden bg-\[#fffff0\] border-4 border-\[#e0ebd0\]">).*?(<!-- Tab: ทั่วไป -->)'
# This is too broad. Let's find the container.

# I'll just rewrite the whole main section from line 135 to where the details panel starts.
# Actually, I'll use a safer approach: find the aside-like div and the flex-1 div.

# The current messy sidebar start
sidebar_start = r'<div class="w-80 bg-white border border-green-300 rounded-xl flex flex-col shadow-sm shrink-0">.*?<div class="overflow-y-auto flex-1">'
new_sidebar_header = """
                <div class="w-80 bg-white border border-green-300 rounded-xl flex flex-col shadow-sm shrink-0 overflow-hidden">
                    <div class="p-2 bg-[#f8fdf4] border-b border-green-300 space-y-1">
                        <select class="w-full border border-green-500 p-1 text-xs font-medium outline-none rounded-sm bg-white">
                            <option>แสดงรายชื่อยาทั้งหมด</option>
                            <option>แสดงยา High Alert</option>
                            <option>แสดงยาใกล้หมดอายุ</option>
                            <option>แสดงยาหมดอายุ</option>
                        </select>
                        <input type="text" placeholder="ค้นหาตาม Lot" class="w-full border border-gray-400 p-1 text-xs outline-none rounded-sm">
                        <input type="text" placeholder="ค้นหาตามชื่อทางการค้า" class="w-full border border-gray-400 p-1 text-xs outline-none rounded-sm">
                    </div>
                    <div class="overflow-y-auto flex-1">
"""

content = re.sub(sidebar_start, new_sidebar_header.strip(), content, flags=re.DOTALL)

# Remove the old search block at the bottom if it still exists
content = re.sub(r'<div class="p-3 bg-\[#f8fdf4\] border-t border-green-300 space-y-3">.*?<\/div>\s*<\/div>\s*<\/div>\s*(<div class="flex-1 bg-white border border-green-300 rounded-xl shadow-sm flex flex-col overflow-hidden">)', r'</div>\s*\1', content, flags=re.DOTALL)

# Ensure the container is correct
content = content.replace('<div class="flex-1 overflow-hidden p-2 flex gap-2">\n                <div class="w-80', '<div class="w-80')

with open(filepath, 'w') as f:
    f.write(content)

print("Manage layout fixed and cleaned.")
