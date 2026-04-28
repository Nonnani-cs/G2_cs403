import re
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(current_dir, 'receive.html')
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add missing IDs
content = re.sub(
    r'<input type="text" class="border border-gray-300 p-1 w-full text-red-600 outline-none rounded-sm bg-white text-center" value="1497">',
    r'<input type="text" id="receive-stock-count" class="border border-gray-300 p-1 w-full text-red-600 outline-none rounded-sm bg-white text-center" value="1497">',
    content
)

content = re.sub(
    r'<input type="text" class="border border-gray-300 p-1 w-full outline-none rounded-sm bg-white text-center" value="50">',
    r'<input type="text" id="receive-price-per-unit" class="border border-gray-300 p-1 w-full outline-none rounded-sm bg-white text-center" value="50">',
    content
)

content = re.sub(
    r'<input type="text" class="border border-gray-300 p-1 w-full outline-none rounded-sm bg-white text-center" value="0">',
    r'<input type="text" id="receive-order-amount" class="border border-gray-300 p-1 w-full outline-none rounded-sm bg-white text-center" value="0">',
    content,
    count=1
)

# 2. Update the rows onclick to include stock and price (mocking some prices)
def update_rows(match):
    full_row = match.group(0)
    # Extra data based on some mock logic
    code = re.search(r"selectDrugReceive\(this, '([^']+)'", full_row).group(1)
    name = re.search(r", '([^']+)'\)", full_row).group(1)
    
    # Extract stock from the last TD
    stock_match = re.search(r'<td class="p-1 text-right">([^<]*)</td>', full_row)
    stock = stock_match.group(1) if stock_match else ""
    
    # Mock price
    price = "500.00" if "mg" in name else "1200.00"
    
    new_onclick = f'onclick="selectDrugReceive(this, \'{code}\', \'{name}\', \'{stock}\', \'{price}\')"'
    return re.sub(r'onclick="selectDrugReceive\([^)]+\)"', new_onclick, full_row)

content = re.sub(
    r'<tr class="[^"]+" onclick="selectDrugReceive\([^)]+\)">.*?</tr>',
    update_rows,
    content,
    flags=re.DOTALL
)

# 3. Update the JS function
new_js = """
    function selectDrugReceive(row, code, name, stock, price) {
        // Remove active class from all rows
        const rows = document.querySelectorAll('tbody tr');
        rows.forEach(r => {
            r.className = r.className.replace('bg-blue-600 text-white', 'hover:bg-blue-50').replace('cursor-pointer', 'cursor-pointer');
            if (!r.className.includes('hover:bg-blue-50')) r.className += ' hover:bg-blue-50';
        });
        
        // Add active class to clicked row
        row.className = 'bg-blue-600 text-white cursor-pointer';
        
        // 1. นำรหัสสินค้าไปใส่ในช่อง รหัสสินค้า (ขวา)
        const codeInput = document.getElementById('receive-drug-code');
        if (codeInput) codeInput.value = code;
        
        // 2. นำชื่อสินค้าไปใส่ในช่อง ชื่อสินค้า (ขวา)
        const nameInput = document.getElementById('receive-drug-name');
        if (nameInput) nameInput.value = name;
        
        // 3. นำจำนวนคงเหลือไปใส่ในช่อง "เหลือจำนวน"
        const stockInput = document.getElementById('receive-stock-count');
        if (stockInput) stockInput.value = stock || "0";
        
        // 4. ดึงราคาต่อหน่วย
        const priceInput = document.getElementById('receive-price-per-unit');
        if (priceInput) priceInput.value = price || "0.00";
        
        // 5. โฟกัสไปที่ช่อง "สั่งซื้อจำนวน" เพื่อให้ผู้ใช้พิมพ์ต่อได้ทันที
        const orderInput = document.getElementById('receive-order-amount');
        if (orderInput) {
            orderInput.focus();
            orderInput.select(); // Select existing text for easy overwrite
        }
    }
"""

content = re.sub(
    r'function selectDrugReceive\(row, code, name\) \{.*?\}',
    new_js.strip(),
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)

print("Receive logic updated with full automation and focus.")
