import re
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(current_dir, 'receive.html')
with open(filepath, 'r') as f:
    content = f.read()

# 1. Correct the script tag (separate Tailwind from logic)
tailwind_cdn = '<script src="https://cdn.tailwindcss.com"></script>'
logic_script = """
<script>
    function selectDrugReceive(row, code, name, stock, price) {
        // Remove active class from all rows
        const rows = document.querySelectorAll('tbody tr');
        rows.forEach(r => {
            // Restore default hover classes and remove blue selection
            r.classList.remove('bg-blue-600', 'text-white');
            r.classList.add('hover:bg-blue-50');
            
            // Fix cell borders (reset to gray)
            const cells = r.querySelectorAll('td');
            cells.forEach(c => {
                c.classList.remove('border-white');
                c.classList.add('border-gray-200');
            });
        });
        
        // Add active class to clicked row
        row.classList.remove('hover:bg-blue-50');
        row.classList.add('bg-blue-600', 'text-white');
        
        // Change cell borders to white for the selected row
        const selectedCells = row.querySelectorAll('td');
        selectedCells.forEach(c => {
            c.classList.remove('border-gray-200');
            c.classList.add('border-white');
        });
        
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
            orderInput.select(); 
        }
    }
</script>
"""

# Replace the broken script block
content = re.sub(
    r'<script src="https://cdn\.tailwindcss\.com">.*?</script>',
    tailwind_cdn + "\n" + logic_script.strip(),
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)

print("Receive script fixed.")
