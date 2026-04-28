import re
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(current_dir, 'receive.html')
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add IDs to inputs
content = re.sub(
    r'<input type="text" class="border border-gray-300 p-1 w-full outline-none rounded-sm bg-\[#e0f7fa\]" value="PD-00007">',
    r'<input type="text" id="receive-drug-code" class="border border-gray-300 p-1 w-full outline-none rounded-sm bg-[#e0f7fa]" value="PD-00007">',
    content
)

content = re.sub(
    r'<input type="text" class="border border-gray-300 p-1 w-full outline-none rounded-sm bg-white" value="ACCUPRIL 20มก\.14\'S">',
    r'<input type="text" id="receive-drug-name" class="border border-gray-300 p-1 w-full outline-none rounded-sm bg-white" value="ACCUPRIL 20มก.14\'S">',
    content
)

# 2. Add onclick to table rows
def add_onclick(match):
    code = match.group(1)
    name = match.group(2)
    return f'<tr class="hover:bg-blue-50 cursor-pointer" onclick="selectDrugReceive(this, \'{code}\', \'{name}\')">'

content = re.sub(
    r'<tr class="hover:bg-blue-50 cursor-pointer"><td class="p-1 border-r border-gray-200">([^<]+)</td><td class="p-1 border-r border-gray-200">([^<]+)</td>',
    add_onclick,
    content
)

# Handle the active row (if any)
content = re.sub(
    r'<tr class="bg-blue-600 text-white cursor-pointer"><td class="p-1 border-r border-gray-200">([^<]+)</td><td class="p-1 border-r border-gray-200">([^<]+)</td>',
    add_onclick,
    content
)

# 3. Add JS function
js_func = """
    function selectDrugReceive(row, code, name) {
        // Remove active class from all rows
        const rows = document.querySelectorAll('tbody tr');
        rows.forEach(r => {
            r.className = 'hover:bg-blue-50 cursor-pointer';
        });
        
        // Add active class to clicked row
        row.className = 'bg-blue-600 text-white cursor-pointer';
        
        // Update details
        const codeInput = document.getElementById('receive-drug-code');
        const nameInput = document.getElementById('receive-drug-name');
        if (codeInput) codeInput.value = code;
        if (nameInput) nameInput.value = name;
    }
"""

if "</script>" in content:
    content = content.replace("</script>", js_func + "\n</script>")
else:
    content = content.replace("</html>", "<script>\n" + js_func + "\n</script>\n</html>")

with open(filepath, 'w') as f:
    f.write(content)

print("Receive page updated with drug selection interaction.")
