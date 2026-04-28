room_temp_drugs = [
    "Abraxane (Nab-paclitaxel)", "Actinomycin D (Dactinomycin)", "Azacitidine", "Bendamustine", 
    "Bortezomib", "Carboplatin", "Cetuximab", "Cisplatin", "Cytarabine", "Docetaxel", 
    "Etoposide", "Fludarabine", "Fluorouracil (5-FU)", "Gemcitabine", "Irinotecan", 
    "Mesna", "Methotrexate", "Oxaliplatin", "Paclitaxel", "Pemetrexed"
]

refrigerated_drugs = [
    "Atezolizumab", "Bevacizumab", "Bleomycin", "Cyclophosphamide", "Dacarbazine", 
    "Daratumumab", "Doxorubicin (รวมแบบ Liposomal)", "Eribulin", "Fulvestrant", 
    "Idarubicin", "Ifosfamide", "Infliximab", "Ipilimumab", "Irinotecan (แบบ Liposomal)", 
    "Mitoxantrone", "Nivolumab", "Panitumumab", "Pembrolizumab", "Pemetrexed (บางยี่ห้อ)", 
    "Phesgo", "Rescuvorin (Leucovorin)", "Rituximab", "Romiplostim", "Trastuzumab", 
    "Trastuzumab deruxtecan", "Trastuzumab Emtansine", "Vincristine"
]

def generate_manage_rows():
    rows = []
    for i, name in enumerate(room_temp_drugs, 1):
        code = f"PD-{i:05d}"
        active_class = "bg-blue-600 text-white cursor-pointer hover:bg-blue-700" if i == 7 else "hover:bg-blue-50 cursor-pointer text-gray-800"
        rows.append(f'                            <tr class="{active_class}" data-category="room" onclick="selectDrug(this, \'{code}\', \'{name}\')">\n                                <td class="p-1 border-r border-gray-300 pl-2">{code}</td>\n                                <td class="p-1 pl-2">{name}</td>\n                            </tr>')
    for i, name in enumerate(refrigerated_drugs, 21):
        code = f"PD-{i:05d}"
        active_class = "hover:bg-blue-50 cursor-pointer text-gray-800"
        rows.append(f'                            <tr class="{active_class}" data-category="refrigerated" onclick="selectDrug(this, \'{code}\', \'{name}\')">\n                                <td class="p-1 border-r border-gray-300 pl-2">{code}</td>\n                                <td class="p-1 pl-2">{name}</td>\n                            </tr>')
    return "\n".join(rows)

def generate_receive_rows():
    rows = []
    for i, name in enumerate(room_temp_drugs, 1):
        code = f"PD-{i:05d}"
        active_class = "bg-blue-600 text-white cursor-pointer" if i == 7 else "hover:bg-blue-50 cursor-pointer"
        border_class = "border-r border-white" if i == 7 else "border-r border-gray-200"
        rows.append(f'                            <tr class="{active_class}" data-category="room" onclick="selectDrugReceive(this, \'{code}\', \'{name}\', \'\', \'500.00\')"><td class="p-1 {border_class}">{code}</td><td class="p-1 {border_class}">{name}</td><td class="p-1 text-right"></td></tr>')
    for i, name in enumerate(refrigerated_drugs, 21):
        code = f"PD-{i:05d}"
        active_class = "hover:bg-blue-50 cursor-pointer"
        border_class = "border-r border-gray-200"
        rows.append(f'                            <tr class="{active_class}" data-category="refrigerated" onclick="selectDrugReceive(this, \'{code}\', \'{name}\', \'\', \'500.00\')"><td class="p-1 {border_class}">{code}</td><td class="p-1 {border_class}">{name}</td><td class="p-1 text-right"></td></tr>')
    return "\n".join(rows)

import re

# Update manage.html
with open(os.path.join(current_dir, 'manage.html'), 'r', encoding='utf-8') as f:
    content = f.read()
new_rows = generate_manage_rows()
content = re.sub(r'<tbody id="drug-list-body".*?</tbody>', f'<tbody id="drug-list-body" class="divide-y divide-gray-200">\n{new_rows}\n                        </tbody>', content, flags=re.DOTALL)
# Add id and onchange to select
content = content.replace('<select class="w-full border border-green-500 p-1 text-xs font-medium outline-none rounded-sm bg-white">', '<select id="drug-filter" onchange="filterDrugs(this.value)" class="w-full border border-green-500 p-1 text-xs font-medium outline-none rounded-sm bg-white">')
# Update options with values
content = content.replace('<option>แสดงรายชื่อยาทั้งหมด</option>', '<option value="all">แสดงรายชื่อยาทั้งหมด</option>')
content = content.replace('<option>แสดงรายการยาที่เก็บอุณหภูมิห้อง</option>', '<option value="room">แสดงรายการยาที่เก็บอุณหภูมิห้อง</option>')
content = content.replace('<option>แสดงรายการยาที่เก็บในตู้เย็น</option>', '<option value="refrigerated">แสดงรายการยาที่เก็บในตู้เย็น</option>')
content = content.replace('<option>แสดงยา High Alert</option>', '<option value="high-alert">แสดงยา High Alert</option>')
content = content.replace('<option>แสดงยาใกล้หมดอายุ</option>', '<option value="expiry-soon">แสดงยาใกล้หมดอายุ</option>')
content = content.replace('<option>แสดงยาหมดอายุ</option>', '<option value="expired">แสดงยาหมดอายุ</option>')

# Add JS filter function to manage.html
if 'function filterDrugs(category)' not in content:
    js_filter = """
    function filterDrugs(category) {
        const rows = document.querySelectorAll('#drug-list-body tr');
        rows.forEach(row => {
            if (category === 'all' || row.dataset.category === category) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
    """
    content = content.replace('</script>', js_filter + '\n</script>')

with open(os.path.join(current_dir, 'manage.html'), 'w', encoding='utf-8') as f:
    f.write(content)

# Update receive.html
with open(os.path.join(current_dir, 'receive.html'), 'r', encoding='utf-8') as f:
    content = f.read()
new_rows = generate_receive_rows()
content = re.sub(r'<tbody class="divide-y divide-gray-200">.*?</tbody>', f'<tbody id="receive-drug-list-body" class="divide-y divide-gray-200">\n{new_rows}\n                        </tbody>', content, flags=re.DOTALL)
# Add id and onchange to select
content = content.replace('<select class="w-full border border-green-500 p-1 text-xs font-medium outline-none rounded-sm bg-white">', '<select id="receive-drug-filter" onchange="filterReceiveDrugs(this.value)" class="w-full border border-green-500 p-1 text-xs font-medium outline-none rounded-sm bg-white">')
# Update options with values
content = content.replace('<option>แสดงรายชื่อยาทั้งหมด</option>', '<option value="all">แสดงรายชื่อยาทั้งหมด</option>')
content = content.replace('<option>แสดงรายการยาที่เก็บอุณหภูมิห้อง</option>', '<option value="room">แสดงรายการยาที่เก็บอุณหภูมิห้อง</option>')
content = content.replace('<option>แสดงรายการยาที่เก็บในตู้เย็น</option>', '<option value="refrigerated">แสดงรายการยาที่เก็บในตู้เย็น</option>')
content = content.replace('<option>แสดงยา High Alert</option>', '<option value="high-alert">แสดงยา High Alert</option>')
content = content.replace('<option>แสดงยาใกล้หมดอายุ</option>', '<option value="expiry-soon">แสดงยาใกล้หมดอายุ</option>')
content = content.replace('<option>แสดงยาหมดอายุ</option>', '<option value="expired">แสดงยาหมดอายุ</option>')

# Add JS filter function to receive.html
if 'function filterReceiveDrugs(category)' not in content:
    js_filter_receive = """
    function filterReceiveDrugs(category) {
        const rows = document.querySelectorAll('#receive-drug-list-body tr');
        rows.forEach(row => {
            if (category === 'all' || row.dataset.category === category) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
    """
    content = content.replace('</script>', js_filter_receive + '\n</script>')

with open(os.path.join(current_dir, 'receive.html'), 'w', encoding='utf-8') as f:
    f.write(content)

print("Filtering functionality added to both pages.")
