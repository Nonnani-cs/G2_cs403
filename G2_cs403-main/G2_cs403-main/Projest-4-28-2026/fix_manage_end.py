import re
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(current_dir, 'manage.html')
with open(filepath, 'r') as f:
    content = f.read()

# Fix the end of the file
# We expect 3 closing divs before </main>
# Currently:
# 609:             </div>
# 610:             </div>
# 611:         </div>
# 612:     </main>

# Let's count them carefully.
# Div 2 (129) closes at 133.
# Div 3 (135) opens.
# Div 4 (136) opens (Sidebar).
# Div 4 closes at 242.
# Div 5 (244) opens (Right Area).
# Div 5 closes at ???

content = re.sub(
    r'</div>\s*</div>\s*</div>\s*</div>\s*</main>',
    r'</div>\n            </div>\n        </div>\n    </main>',
    content
)

# Also fix any extra closing divs that might be causing the "Error: Mismatched tag </div>, expected </main>"
# This error means there's a </div> where a </main> was expected.

with open(filepath, 'w') as f:
    f.write(content)

print("Manage end fixed.")
