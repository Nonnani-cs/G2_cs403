import re

filepath = '/Users/atcharapornn/Desktop/Projest/receive.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Remove the redundant Search and Filter (Moved from Sidebar) block
redundant_search_pattern = r'<!-- Search and Filter \(Moved from Sidebar\) -->\s*<div class="p-2 bg-\[#f8fdf4\] border-t border-gray-400 flex items-center space-x-2 text-xs">.*?</div>'
content = re.sub(redundant_search_pattern, '', content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

print("Receive redundant search removed.")
