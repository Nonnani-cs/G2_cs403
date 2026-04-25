import re

filepath = '/Users/atcharapornn/Desktop/Projest/dispense.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add ID to Ordered Medicine List inputs
content = re.sub(
    r'<input type="text" value="DRUG0001" class="w-32 border border-\[#cbd5e1\] p-1\.5 bg-white rounded-none outline-none font-medium text-blue-700">',
    r'<input type="text" id="order-drug-code" value="DRUG0001" class="w-32 border border-[#cbd5e1] p-1.5 bg-white rounded-none outline-none font-medium text-blue-700">',
    content
)

content = re.sub(
    r'<input type="text" value="Cisplatin" class="flex-1 border border-\[#cbd5e1\] p-1\.5 bg-white rounded-none outline-none focus:border-blue-400 text-gray-700 font-medium">',
    r'<input type="text" id="order-drug-name" value="Cisplatin" class="flex-1 border border-[#cbd5e1] p-1.5 bg-white rounded-none outline-none focus:border-blue-400 text-gray-700 font-medium">',
    content
)

content = re.sub(
    r'<input type="text" value="Platinol" class="flex-1 border border-\[#cbd5e1\] p-1\.5 bg-white rounded-none outline-none focus:border-blue-400 text-gray-700">',
    r'<input type="text" id="order-trade-name" value="Platinol" class="flex-1 border border-[#cbd5e1] p-1.5 bg-white rounded-none outline-none focus:border-blue-400 text-gray-700">',
    content,
    count=1
)

# 2. Add the left sidebar for drug selection
# We need to wrap the existing content in a flex-row container
drug_list_sidebar = """
            <!-- Left Sidebar: Drug Selection -->
            <div class="w-80 border border-gray-400 bg-white flex flex-col shadow-inner shrink-0">
                <div class="p-2 bg-[#f8fdf4] border-b border-gray-400 space-y-1">
                    <select class="w-full border border-green-500 p-1 text-xs font-medium outline-none rounded-sm bg-white">
                        <option>แสดงรายชื่อยาทั้งหมด</option>
                    </select>
                    <input type="text" placeholder="ค้นหาตามชื่อยา..." class="w-full border border-gray-400 p-1 text-xs outline-none rounded-sm">
                </div>
                <div class="overflow-y-auto flex-1 bg-white">
                    <table class="w-full text-xs text-left">
                        <thead class="bg-gray-100 border-b border-gray-400 sticky top-0">
                            <tr>
                                <th class="p-1 border-r border-gray-300 font-medium w-16">รหัสสินค้า</th>
                                <th class="p-1 border-r border-gray-300 font-medium">ชื่อสินค้า</th>
                            </tr>
                        </thead>
                        <tbody id="dispense-drug-list-body" class="divide-y divide-gray-200">
                            <tr class="hover:bg-blue-50 cursor-pointer" onclick="selectDrugDispense(this, 'PD-00001', 'Cyclophosphamide 500mg', 'Endoxan')"><td class="p-1 border-r border-gray-200">PD-00001</td><td class="p-1 border-r border-gray-200">Cyclophosphamide 500mg</td></tr>
                            <tr class="hover:bg-blue-50 cursor-pointer" onclick="selectDrugDispense(this, 'PD-00002', 'Doxorubicin 50mg', 'Adriamycin')"><td class="p-1 border-r border-gray-200">PD-00002</td><td class="p-1 border-r border-gray-200">Doxorubicin 50mg</td></tr>
                            <tr class="hover:bg-blue-50 cursor-pointer" onclick="selectDrugDispense(this, 'PD-00003', '5-Fluorouracil 500mg', 'Adrucil')"><td class="p-1 border-r border-gray-200">PD-00003</td><td class="p-1 border-r border-gray-200">5-Fluorouracil 500mg</td></tr>
                            <tr class="hover:bg-blue-50 cursor-pointer" onclick="selectDrugDispense(this, 'PD-00004', 'Cisplatin 50mg', 'Platinol')"><td class="p-1 border-r border-gray-200">PD-00004</td><td class="p-1 border-r border-gray-200">Cisplatin 50mg</td></tr>
                            <tr class="hover:bg-blue-50 cursor-pointer" onclick="selectDrugDispense(this, 'PD-00005', 'Paclitaxel 100mg', 'Taxol')"><td class="p-1 border-r border-gray-200">PD-00005</td><td class="p-1 border-r border-gray-200">Paclitaxel 100mg</td></tr>
                            <tr class="hover:bg-blue-50 cursor-pointer" onclick="selectDrugDispense(this, 'PD-00006', 'Carboplatin 150mg', 'Paraplatin')"><td class="p-1 border-r border-gray-200">PD-00006</td><td class="p-1 border-r border-gray-200">Carboplatin 150mg</td></tr>
                            <tr class="hover:bg-blue-50 cursor-pointer" onclick="selectDrugDispense(this, 'PD-00007', 'Vincristine 1mg', 'Oncovin')"><td class="p-1 border-r border-gray-200">PD-00007</td><td class="p-1 border-r border-gray-200">Vincristine 1mg</td></tr>
                            <tr class="hover:bg-blue-50 cursor-pointer" onclick="selectDrugDispense(this, 'PD-00008', 'Epirubicin 50mg', 'Ellence')"><td class="p-1 border-r border-gray-200">PD-00008</td><td class="p-1 border-r border-gray-200">Epirubicin 50mg</td></tr>
                            <tr class="hover:bg-blue-50 cursor-pointer" onclick="selectDrugDispense(this, 'PD-00009', 'Gemcitabine 1g', 'Gemzar')"><td class="p-1 border-r border-gray-200">PD-00009</td><td class="p-1 border-r border-gray-200">Gemcitabine 1g</td></tr>
                            <tr class="hover:bg-blue-50 cursor-pointer" onclick="selectDrugDispense(this, 'PD-00010', 'Oxaliplatin 50mg', 'Eloxatin')"><td class="p-1 border-r border-gray-200">PD-00010</td><td class="p-1 border-r border-gray-200">Oxaliplatin 50mg</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
"""

# Insert the sidebar after the first gap-2 flex div
content = re.sub(
    r'(<div class="flex-1 p-2 flex flex-col gap-2 overflow-hidden bg-\[#fffff0\] border-4 border-\[#e0ebd0\]">)\n\s*(<div class="flex-1 overflow-y-auto p-2 flex flex-col gap-4 text-sm text-gray-800">)',
    r'\1\n        <div class="flex-1 flex gap-2 overflow-hidden">\n' + drug_list_sidebar + r'\n            \2',
    content,
    count=1
)

# Close the new flex gap-2 div
# We find the end of the scrollable content div
content = re.sub(
    r'(</div>\s*</div>\s*<!-- Footer Buttons -->)',
    r'            </div>\n        \1',
    content,
    count=1
)

# 3. Add the JS function
new_script_func = """
    function selectDrugDispense(row, code, name, trade) {
        // Remove active class from all rows
        const rows = document.querySelectorAll('#dispense-drug-list-body tr');
        rows.forEach(r => {
            r.className = 'hover:bg-blue-50 cursor-pointer';
        });
        
        // Add active class to clicked row
        row.className = 'bg-blue-600 text-white cursor-pointer';
        
        // Update details
        document.getElementById('order-drug-code').value = code;
        document.getElementById('order-drug-name').value = name;
        document.getElementById('order-trade-name').value = trade;
    }
"""

content = content.replace("function pullPatientData() {", new_script_func + "\n    function pullPatientData() {")

with open(filepath, 'w') as f:
    f.write(content)

print("Dispense page updated with drug selection sidebar.")
