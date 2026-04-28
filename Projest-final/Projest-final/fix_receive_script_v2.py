import re
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(current_dir, 'receive.html')
with open(filepath, 'r') as f:
    content = f.read()

# Replace the entire script block correctly
new_script_block = """
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

# Find the script tag after tailwind and replace everything up to </script>
content = re.sub(
    r'<script>\s*function selectDrugReceive.*?<\/script>',
    new_script_block.strip(),
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)

print("Receive script cleaned and fixed.")
