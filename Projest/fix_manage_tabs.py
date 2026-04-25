import re

filepath = '/Users/atcharapornn/Desktop/Projest/manage.html'
with open(filepath, 'r') as f:
    content = f.read()

# Fix the closing divs after content-general
# Currently:
# </div> <!-- Closes Right Side -->
# </div> <!-- Closes content-general -->
# </div> <!-- Closes main container (BAD) -->
# <!-- Tab: รายละเอียดเพิ่มเติม -->

content = re.sub(
    r'</div>\s*</div>\s*</div>\s*<!-- Tab: รายละเอียดเพิ่มเติม -->',
    r'</div>\n                    </div>\n\n                    <!-- Tab: รายละเอียดเพิ่มเติม -->',
    content
)

# Also check other tabs
# After content-details, there should be a closing div for it.
# After content-expiry, there should be a closing div for it.
# And finally one closing div for the main container at the very end of all tabs.

# Let's see the end of the tabs area
