import re

filepath = '/Users/atcharapornn/Desktop/Projest/receive.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add ID to Unit input
content = re.sub(
    r'<input type="text" class="border border-gray-300 p-1 w-full outline-none rounded-sm bg-\[#e0f7fa\] text-center" value="ขวด">',
    r'<input type="text" id="receive-unit" class="border border-gray-300 p-1 w-full outline-none rounded-sm bg-[#e0f7fa] text-center" value="ขวด">',
    content
)

# 2. Add ID to Order List Tbody
content = re.sub(
    r'<tbody>\s*<tr class="bg-blue-600 text-white h-6">',
    r'<tbody id="order-list-tbody">\n                            <tr id="active-order-row" class="bg-blue-600 text-white h-6">',
    content,
    count=1
)

# 3. Add ID to the cells of the active row for easy updates
content = re.sub(
    r'<tr id="active-order-row" class="bg-blue-600 text-white h-6">\s*<td class="border-r border-white"></td><td class="border-r border-white"></td><td class="border-r border-white"></td><td class="border-r border-white"></td><td></td>\s*</tr>',
    r'<tr id="active-order-row" class="bg-blue-600 text-white h-6"><td id="row-code" class="border-r border-white"></td><td id="row-name" class="border-r border-white text-left px-2"></td><td id="row-price" class="border-r border-white text-right px-2"></td><td id="row-amount" class="border-r border-white text-right px-2"></td><td id="row-unit"></td></tr>',
    content
)

# 4. Update selectDrugReceive JS function
new_js = """
    function selectDrugReceive(row, code, name, stock, price) {
        const rows = document.querySelectorAll('#order-list-tbody tr');
        // Clear selection highlight from sidebar
        document.querySelectorAll('tbody tr').forEach(r => {
            r.classList.remove('bg-blue-600', 'text-white');
            r.classList.add('hover:bg-blue-50');
            r.querySelectorAll('td').forEach(c => { c.classList.remove('border-white'); c.classList.add('border-gray-200'); });
        });
        
        row.classList.remove('hover:bg-blue-50');
        row.classList.add('bg-blue-600', 'text-white');
        row.querySelectorAll('td').forEach(c => { c.classList.remove('border-gray-200'); c.classList.add('border-white'); });
        
        // 1-4. Update Right Form
        document.getElementById('receive-drug-code').value = code;
        document.getElementById('receive-drug-name').value = name;
        document.getElementById('receive-stock-count').value = stock || "0";
        document.getElementById('receive-price-per-unit').value = price || "0.00";
        
        // Update Bottom Table Row (Preview)
        document.getElementById('row-code').innerText = code;
        document.getElementById('row-name').innerText = name;
        document.getElementById('row-price').innerText = price || "0.00";
        document.getElementById('row-amount').innerText = "0";
        document.getElementById('row-unit').innerText = document.getElementById('receive-unit').value;

        // 5. Focus
        const orderInput = document.getElementById('receive-order-amount');
        if (orderInput) {
            orderInput.focus();
            orderInput.select();
            
            // Add listener to update bottom table in real-time
            orderInput.oninput = function() {
                document.getElementById('row-amount').innerText = this.value || "0";
            };
        }
    }
"""

content = re.sub(
    r'function selectDrugReceive\(row, code, name, stock, price\) \{.*?\}',
    new_js.strip(),
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)

print("Receive bottom table updated.")
