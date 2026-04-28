import re
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(current_dir, 'receive.html')
with open(filepath, 'r') as f:
    content = f.read()

# 1. Correct the sidebar and main content separation
content = re.sub(r'(</tbody>\s*</table>\s*</div>)\s*(<!-- Right Main Area -->\s*<div class="flex-1 flex flex-col border border-gray-400 bg-white shadow-sm overflow-hidden">)', 
                 r'\1\n            </div>\n            \2', content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

print("Receive layout separation fixed.")
