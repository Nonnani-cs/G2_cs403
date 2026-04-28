import re
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(current_dir, 'dispense.html')
with open(filepath, 'r') as f:
    content = f.read()

# Replace styles for regular inputs/selects
content = re.sub(
    r'border border-green-[23]00 rounded p-1\.5 bg-\[#fdfdf0\]',
    'border border-[#cbd5e1] p-1.5 bg-white rounded-none',
    content
)

# Fix the focus border color too
content = re.sub(
    r'focus:border-green-400',
    'focus:border-blue-400',
    content
)

with open(filepath, 'w') as f:
    f.write(content)

print("Styles updated.")
