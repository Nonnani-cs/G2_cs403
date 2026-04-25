import re

filepath = '/Users/atcharapornn/Desktop/Projest/dispense.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Remove the Sidebar and wrapping div
# Find the start of the flex-row container we added
pattern = r'<div class="flex-1 flex gap-2 overflow-hidden">\s*<!-- Left Sidebar: Drug Selection -->.*?<div class="flex-1 overflow-y-auto p-2 flex flex-col gap-4 text-sm text-gray-800">'
content = re.sub(pattern, r'<div class="flex-1 overflow-y-auto p-2 flex flex-col gap-4 text-sm text-gray-800">', content, flags=re.DOTALL)

# Remove the closing div tag we added
# It was added before <!-- Footer Buttons -->
content = re.sub(r'            </div>\s*(</div>\s*<!-- Footer Buttons -->)', r'\1', content)

# 2. Keep the IDs on inputs (they don't hurt)
# 3. Keep the JS function (it won't be called if the rows are gone)

with open(filepath, 'w') as f:
    f.write(content)

print("Dispense sidebar removed.")
