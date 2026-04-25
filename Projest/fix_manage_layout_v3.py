import re

filepath = '/Users/atcharapornn/Desktop/Projest/manage.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Correct the sidebar and main content separation
# We want to find the end of the drug list table and ensure the sidebar is closed.
content = re.sub(r'(</tbody>\s*</table>\s*</div>)\s*(<div class="flex-1 bg-white border border-green-300 rounded-xl shadow-sm flex flex-col overflow-hidden">)', 
                 r'\1\n            </div>\n            \2', content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

print("Manage layout separation fixed.")
