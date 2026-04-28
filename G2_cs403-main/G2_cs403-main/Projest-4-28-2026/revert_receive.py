import re
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(current_dir, 'receive.html')
with open(filepath, 'r') as f:
    content = f.read()

# 1. Put Search/Filter back into the Sidebar
search_filter_sidebar = """
                <div class="p-2 bg-[#f8fdf4] border-b border-gray-400 space-y-1">
                    <select class="w-full border border-green-500 p-1 text-xs font-medium outline-none rounded-sm bg-white">
                        <option>แสดงรายชื่อยาทั้งหมด</option>
                        <option>แสดงยา High Alert</option>
                        <option>แสดงยาใกล้หมดอายุ</option>
                        <option>แสดงยาหมดอายุ</option>
                    </select>
                    <input type="text" placeholder="ค้นหาตาม Lot" class="w-full border border-gray-400 p-1 text-xs outline-none rounded-sm">
                    <input type="text" placeholder="ค้นหาตามชื่อทางการค้า" class="w-full border border-gray-400 p-1 text-xs outline-none rounded-sm">
                </div>
"""

# Find sidebar and insert it
content = re.sub(
    r'(<div class="w-80 border border-gray-400 bg-white flex flex-col shadow-inner">)',
    r'\1' + search_filter_sidebar,
    content
)

# 2. Remove Search/Filter from above the right table
content = re.sub(
    r'<!-- Search and Filter \(Above Table\) -->\s*<div class="p-2 bg-\[#f8fdf4\] border-t border-gray-400 flex items-center space-x-2 text-xs">.*?</div>',
    '',
    content,
    flags=re.DOTALL
)

# 3. Restore the Preview logic in selectDrugReceive
logic_script = """
<script>
    function selectDrugReceive(row, code, name, stock, price) {
        // 1. Clear selection highlight from sidebar
        document.querySelectorAll('.divide-y tr').forEach(r => {
            r.classList.remove('bg-blue-600', 'text-white');
            r.classList.add('hover:bg-blue-50');
            r.querySelectorAll('td').forEach(c => {
                c.classList.remove('border-white');
                c.classList.add('border-gray-200');
            });
        });
        
        // 2. Highlight selected row
        row.classList.remove('hover:bg-blue-50');
        row.classList.add('bg-blue-600', 'text-white');
        row.querySelectorAll('td').forEach(c => {
            c.classList.remove('border-gray-200');
            c.classList.add('border-white');
        });
        
        // 3. Update Right Form
        document.getElementById('receive-drug-code').value = code;
        document.getElementById('receive-drug-name').value = name;
        document.getElementById('receive-stock-count').value = stock || "0";
        document.getElementById('receive-price-per-unit').value = price || "0.00";
        
        // 4. Update Bottom Table Row (Preview)
        const rowCode = document.getElementById('row-code');
        const rowName = document.getElementById('row-name');
        const rowPrice = document.getElementById('row-price');
        const rowAmount = document.getElementById('row-amount');
        const rowUnit = document.getElementById('row-unit');

        if (rowCode) rowCode.innerText = code;
        if (rowName) rowName.innerText = name;
        if (rowPrice) rowPrice.innerText = price || "0.00";
        if (rowAmount) rowAmount.innerText = "0";
        if (rowUnit) rowUnit.innerText = document.getElementById('receive-unit').value;

        // 5. Focus and set up real-time update
        const orderInput = document.getElementById('receive-order-amount');
        if (orderInput) {
            orderInput.focus();
            orderInput.select();
            
            orderInput.oninput = function() {
                const previewAmount = document.getElementById('row-amount');
                if (previewAmount) previewAmount.innerText = this.value || "0";
            };
        }
    }
</script>
"""

# Re-apply the row IDs to the bottom table if they were removed
content = re.sub(
    r'<tr class="bg-blue-600 text-white h-6"><td class="border-r border-white"></td><td class="border-r border-white"></td><td class="border-r border-white"></td><td class="border-r border-white"></td><td></td></tr>',
    r'<tr id="active-order-row" class="bg-blue-600 text-white h-6"><td id="row-code" class="border-r border-white"></td><td id="row-name" class="border-r border-white text-left px-2"></td><td id="row-price" class="border-r border-white text-right px-2"></td><td id="row-amount" class="border-r border-white text-right px-2"></td><td id="row-unit"></td></tr>',
    content
)

# Update script tag
tailwind_cdn = '<script src="https://cdn.tailwindcss.com"></script>'
content = re.sub(
    r'<script src="https://cdn\.tailwindcss\.com"></script>\s*<script>.*?</script>',
    tailwind_cdn + "\n" + logic_script.strip(),
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)

print("Reverted to original layout and restored preview logic.")
