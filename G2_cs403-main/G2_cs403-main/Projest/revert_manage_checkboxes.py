import re

filepath = os.path.join(current_dir, 'manage.html')
with open(filepath, 'r') as f:
    content = f.read()

# Revert checkboxes to the right of product code
old_layout = """
                            <div class="flex items-center">
                                <label class="w-1/4 text-right pr-2 text-blue-700 font-medium">***รหัสสินค้า :</label>
                                <input type="text" id="detail-code" class="w-1/2 border border-gray-300 p-1 bg-white outline-none" value="PD-00007">
                                <div class="w-1/4 pl-4 flex flex-col space-y-1">
                                    <label class="flex items-center space-x-1"><input type="checkbox" class="accent-green-500"> <span>ยาฉีดเข้า IV</span></label>
                                    <label class="flex items-center space-x-1"><input type="checkbox" class="accent-green-500"> <span>ยาฉีดเข้าใต้ผิวหนัง (SC)</span></label>
                                    <label class="flex items-center space-x-1"><input type="checkbox" class="accent-green-500"> <span>ยาฉีดเข้าทางกล้ามเนื้อ (IM)</span></label>
                                    <label class="flex items-center space-x-2 cursor-pointer"><input type="checkbox" class="w-4 h-4 accent-green-500"> <span>ยาฉีดเข้าทางไขสันหลัง (IT)</span></label>
                                </div>
                            </div>
"""

# Find the modified part and replace it
content = re.sub(
    r'<div class="flex items-center">\s*<label class="w-1/4 text-right pr-2 text-blue-700 font-medium">\*\*\*รหัสสินค้า :</label>\s*<input type="text" id="detail-code" class="w-1/2 border border-gray-300 p-1 bg-white outline-none" value="PD-00007">\s*</div>\s*<div class="flex items-start">\s*<div class="w-1/4"></div>\s*<div class="w-1/2 flex flex-col space-y-1 pb-2">.*?</div>\s*</div>',
    old_layout.strip(),
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)

print("Reverted manage.html checkboxes.")
