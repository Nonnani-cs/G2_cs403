import re

filepath = '/Users/atcharapornn/Desktop/Projest/manage.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Clean up the container nesting
content = re.sub(r'<div class="flex-1 p-2 flex gap-2 overflow-hidden bg-\[#fffff0\] border-4 border-\[#e0ebd0\]">\s*<div class="flex-1 overflow-hidden p-2 flex gap-2">', 
                 r'<div class="flex-1 p-2 flex gap-2 overflow-hidden bg-[#fffff0] border-4 border-[#e0ebd0]">', content)

# 2. Fix the sidebar structure
# We want: <aside class="w-80 ..."> <search> <table> </aside>
sidebar_pattern = r'<div class="w-80 bg-white border border-green-300 rounded-xl flex flex-col shadow-sm shrink-0">.*?<tbody id="drug-list-body" class="divide-y divide-gray-200">.*?</tbody>\s*</table>\s*</div>\s*</div>'
# This is too complex.

# Let's find the aside/sidebar div and its contents
# I'll just look for the table and its surrounding divs.
new_sidebar = """
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
                    <table class="w-full text-xs text-left">
                        <thead class="bg-gray-100 border-b sticky top-0 shadow-sm">
                            <tr>
                                <th class="p-2 border-r border-gray-300 font-medium text-center w-24">รหัสสินค้า</th>
                                <th class="p-2 font-medium text-center">ชื่อทางการค้า</th>
                            </tr>
                        </thead>
                        <tbody id="drug-list-body" class="divide-y divide-gray-200">
"""

# Find from start of sidebar to start of tbody
content = re.sub(r'<div class="w-80.*?(<tbody id="drug-list-body")', new_sidebar.strip() + r'\1', content, flags=re.DOTALL)

# Find from end of table to start of main content and clean it up
# We want to remove any extra search divs at the bottom.
content = re.sub(r'</tbody>\s*</table>\s*</div>\s*<div class="p-3 bg-\[#f8fdf4\].*?<\/div>\s*<\/div>\s*(<div class="flex-1 bg-white border border-green-300 rounded-xl shadow-sm flex flex-col overflow-hidden">)', 
                 r'</tbody>\n                    </table>\n                </div>\n            </div>\n            \1', content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

print("Manage layout cleaned.")
