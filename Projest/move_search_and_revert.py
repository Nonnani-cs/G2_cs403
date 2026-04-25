import re

filepath = '/Users/atcharapornn/Desktop/Projest/receive.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Extract the search controls from the sidebar
search_pattern = r'<div class="p-2 bg-\[#f8fdf4\] border-b border-gray-400 space-y-1">.*?</div>'
search_match = re.search(search_pattern, content, flags=re.DOTALL)
if search_match:
    search_html = search_match.group(0)
    # Remove it from the sidebar
    content = content.replace(search_html, "")

# 2. Revert the bottom table logic (Remove IDs and auto-populating cells)
# Restore the active-order-row to empty cells
content = re.sub(
    r'<tr id="active-order-row" class="bg-blue-600 text-white h-6">.*?</tr>',
    r'<tr class="bg-blue-600 text-white h-6"><td class="border-r border-white"></td><td class="border-r border-white"></td><td class="border-r border-white"></td><td class="border-r border-white"></td><td></td></tr>',
    content,
    flags=re.DOTALL
)
content = content.replace('id="order-list-tbody"', "")

# 3. Revert the JS function to simple form population
simple_js = """
    function selectDrugReceive(row, code, name, stock, price) {
        // Clear selection highlight from sidebar
        document.querySelectorAll('.divide-y tr').forEach(r => {
            r.classList.remove('bg-blue-600', 'text-white');
            r.classList.add('hover:bg-blue-50');
            r.querySelectorAll('td').forEach(c => {
                c.classList.remove('border-white');
                c.classList.add('border-gray-200');
            });
        });
        
        // Highlight selected row
        row.classList.remove('hover:bg-blue-50');
        row.classList.add('bg-blue-600', 'text-white');
        row.querySelectorAll('td').forEach(c => {
            c.classList.remove('border-gray-200');
            c.classList.add('border-white');
        });
        
        // Update Right Form
        const codeInput = document.getElementById('receive-drug-code');
        const nameInput = document.getElementById('receive-drug-name');
        const stockInput = document.getElementById('receive-stock-count');
        const priceInput = document.getElementById('receive-price-per-unit');
        
        if (codeInput) codeInput.value = code;
        if (nameInput) nameInput.value = name;
        if (stockInput) stockInput.value = stock || "0";
        if (priceInput) priceInput.value = price || "0.00";

        // Focus
        const orderInput = document.getElementById('receive-order-amount');
        if (orderInput) {
            orderInput.focus();
            orderInput.select();
        }
    }
"""

content = re.sub(
    r'function selectDrugReceive\(row, code, name, stock, price\) \{.*?\}',
    simple_js.strip(),
    content,
    flags=re.DOTALL
)

# 4. Insert the search controls above the bottom table on the right
# We'll style it to fit the right panel
new_search_html = """
                <!-- Search and Filter (Moved from Sidebar) -->
                <div class="p-2 bg-[#f8fdf4] border-t border-gray-400 flex items-center space-x-2 text-xs">
                    <select class="flex-1 border border-green-500 p-1 font-medium outline-none rounded-sm bg-white">
                        <option>แสดงรายชื่อยาทั้งหมด</option>
                        <option>แสดงยา High Alert</option>
                        <option>แสดงยาใกล้หมดอายุ</option>
                        <option>แสดงยาหมดอายุ</option>
                    </select>
                    <input type="text" placeholder="ค้นหาตาม Lot" class="flex-1 border border-gray-400 p-1 outline-none rounded-sm">
                    <input type="text" placeholder="ค้นหาตามชื่อทางการค้า" class="flex-1 border border-gray-400 p-1 outline-none rounded-sm">
                </div>
"""

content = content.replace('<!-- Order List Table -->', new_search_html + '\n                <!-- Order List Table -->')

with open(filepath, 'w') as f:
    f.write(content)

print("Layout updated: Search moved to right table area, bottom table auto-population reverted.")
