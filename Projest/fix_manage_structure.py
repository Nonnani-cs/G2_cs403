import re

filepath = '/Users/atcharapornn/Desktop/Projest/manage.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Fix duplicate tbody
content = content.replace('<tbody id="drug-list-body" class="divide-y divide-gray-200"><tbody id="drug-list-body" class="divide-y divide-gray-200">', '<tbody id="drug-list-body" class="divide-y divide-gray-200">')

# 2. Fix the broken div nesting after the checkboxes
# We want to remove the extra closing divs and the misplaced "ข้อความค้นหา"
pattern = r'</div>\s*</div>\s*<div class="flex items-center space-x-2 text-xs pt-1">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>'
# Replace with just closing the checkboxes container
replacement = r'</div>\s*</div>'

# Actually, let's be more precise. 
# We had:
# <div class="w-[60%] ...">
#    <div class="flex items-center"> (Product Code)
#        ...
#        <div class="w-1/4 ..."> (Checkboxes)
#            ...
#        </div> <!-- closes checkboxes -->
#    </div> <!-- closes Product Code row -->
#    ... (rest of rows) ...
# </div> <!-- closes Left Side -->

# The current mess is right after the Product Code row.
mess_pattern = r'</div>\s*</div>\s*<div class="flex items-center space-x-2 text-xs pt-1">.*?<input type="text" class="flex-1 border border-blue-300 p-1 bg-\[#fdfdf0\] outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 rounded-sm">\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>'
content = re.sub(mess_pattern, r'</div>\n                            </div>', content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

print("Manage structure fixed.")
