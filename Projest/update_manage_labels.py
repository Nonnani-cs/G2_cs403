import re

filepath = '/Users/atcharapornn/Desktop/Projest/manage.html'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the search block with the one from receive.html style
new_search_block = """
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
"""

# Find the current search block (which I just moved to the top)
# It's after the header div of the sidebar
sidebar_header = r'<div class="w-80 bg-white border border-green-300 rounded-xl flex flex-col shadow-sm shrink-0">\s*<div class="p-3 bg-\[#f8fdf4\] border-b border-green-300 space-y-3">.*?<\/div>'
content = re.sub(sidebar_header, r'<div class="w-80 bg-white border border-green-300 rounded-xl flex flex-col shadow-sm shrink-0">' + new_search_block.strip(), content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

print("Labels updated in manage.html")
