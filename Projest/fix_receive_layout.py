import re

filepath = '/Users/atcharapornn/Desktop/Projest/receive.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Clean up the script block entirely
tailwind_cdn = '<script src="https://cdn.tailwindcss.com"></script>'
logic_script = """
<script>
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
        
        // Update Form Fields on the Right
        const codeInput = document.getElementById('receive-drug-code');
        const nameInput = document.getElementById('receive-drug-name');
        const stockInput = document.getElementById('receive-stock-count');
        const priceInput = document.getElementById('receive-price-per-unit');
        
        if (codeInput) codeInput.value = code;
        if (nameInput) nameInput.value = name;
        if (stockInput) stockInput.value = stock || "0";
        if (priceInput) priceInput.value = price || "0.00";

        // Focus on Order Amount
        const orderInput = document.getElementById('receive-order-amount');
        if (orderInput) {
            orderInput.focus();
            orderInput.select();
        }
    }
</script>
"""

# Replace script tags
content = re.sub(r'<script src="https://cdn\.tailwindcss\.com"></script>\s*<script>.*?</script>', tailwind_cdn + "\n" + logic_script.strip(), content, flags=re.DOTALL)

# 2. Ensure Sidebar doesn't have search
# (It seems it was already missing, but let's be sure)
sidebar_header_pattern = r'<div class="w-80 border border-gray-400 bg-white flex flex-col shadow-inner">\s*<div class="p-2 bg-\[#f8fdf4\] border-b border-gray-400 space-y-1">.*?</div>'
sidebar_clean = '<div class="w-80 border border-gray-400 bg-white flex flex-col shadow-inner">'
content = re.sub(sidebar_header_pattern, sidebar_clean, content, flags=re.DOTALL)

# 3. Ensure Search and Filter is above the table on the right
# Find the Order List Table div
search_filter_html = """
                <!-- Search and Filter (Above Table) -->
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

# Check if it's already there
if "Search and Filter (Above Table)" not in content:
    content = re.sub(
        r'(<!-- Order List Table -->)',
        search_filter_html + r'\n                \1',
        content
    )

# 4. Remove the preview logic from the bottom table
# Revert the active-order-row to empty cells
content = re.sub(
    r'<tr id="active-order-row" class="bg-blue-600 text-white h-6">.*?</tr>',
    r'<tr class="bg-blue-600 text-white h-6"><td class="border-r border-white"></td><td class="border-r border-white"></td><td class="border-r border-white"></td><td class="border-r border-white"></td><td></td></tr>',
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)

print("Layout fixed: Search moved to right table area, and preview logic reverted.")
