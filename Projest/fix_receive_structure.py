import re

filepath = '/Users/atcharapornn/Desktop/Projest/receive.html'
with open(filepath, 'r') as f:
    content = f.read()

# Fix the mess after the pharmacist name
mess_pattern = r'</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*<!-- 4 Buttons Grid -->'
# Let's see what's actually there
# Line 178: <input type="text" ...>
# Line 179: <button ...>🔍</button>
# Line 180: </div> (closes max-w-md)
# Then we need one more </div> to close the "flex items-center pt-1" row.
# And one more </div> to close the "space-y-1 w-2/3" container.

fixed_pharmacist_row = """                                </div>
                            </div>
                        </div>
                        <!-- 4 Buttons Grid -->"""

content = re.sub(
    r'</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*<!-- 4 Buttons Grid -->',
    fixed_pharmacist_row,
    content,
    flags=re.DOTALL
)

# Wait, I might have over-replaced. Let's do it carefully.
# Current state:
# 178:                                     <input type="text" ...>
# 179:                                     <button ...>🔍</button>
# 180:                                 </div>
# 181:             </div>
# 182:             </div>
# 183:                         </div>
# 184:                         <!-- 4 Buttons Grid -->

# We want:
# 180:                                 </div> <!-- Closes max-w-md -->
# 181:                             </div> <!-- Closes flex items-center pt-1 -->
# 182:                         </div> <!-- Closes space-y-1 w-2/3 -->
# 183:                         <!-- 4 Buttons Grid -->

content = re.sub(
    r'<div class="flex items-center pt-1">.*?<div class="flex flex-1 max-w-md">.*?</div>\s*</div>\s*</div>\s*</div>\s*<!-- 4 Buttons Grid -->',
    lambda m: m.group(0).split('<!-- 4 Buttons Grid -->')[0].rstrip() + "\n                        </div>\n                        <!-- 4 Buttons Grid -->", # This is too complex.
    content,
    flags=re.DOTALL
)

# Let's just use literal replacement for the mess.
content = content.replace(
    '                                </div>\n            </div>\n            </div>\n                        </div>\n                        <!-- 4 Buttons Grid -->',
    '                                </div>\n                            </div>\n                        </div>\n                        <!-- 4 Buttons Grid -->'
)

with open(filepath, 'w') as f:
    f.write(content)

print("Receive structure fixed.")
