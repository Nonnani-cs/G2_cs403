import re

filepath = '/Users/atcharapornn/Desktop/Projest/manage.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Extract the search block
search_block_match = re.search(r'<div class="p-3 bg-\[#f8fdf4\] border-t border-green-300 space-y-3">.*?<\/div>\s*<\/div>\s*<\/div>\s*<\/div>', content, re.DOTALL)
# Actually, the search block is inside the sidebar aside.
# Let's find the aside content.

aside_pattern = r'(<div class="w-80 bg-white border border-green-300 rounded-xl flex flex-col shadow-sm shrink-0">)\s*(<div class="overflow-y-auto flex-1">.*?<\/div>)\s*(<div class="p-3 bg-\[#f8fdf4\] border-t border-green-300 space-y-3">.*?<\/div>)\s*(<\/div>)'
match = re.search(aside_pattern, content, re.DOTALL)

if match:
    header = match.group(1)
    table_div = match.group(2)
    search_div = match.group(3)
    footer = match.group(4)
    
    # Swap search_div and table_div
    # Also change border-t to border-b for search_div
    search_div = search_div.replace('border-t', 'border-b')
    
    new_aside = f"{header}\n                {search_div}\n                {table_div}\n            {footer}"
    content = content.replace(match.group(0), new_aside)

with open(filepath, 'w') as f:
    f.write(content)

print("Search controls moved to top in manage.html")
