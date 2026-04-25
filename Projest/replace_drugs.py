drugs = [
    "Abraxane (Nab-paclitaxel)",
    "Actinomycin D (Dactinomycin)",
    "Azacitidine",
    "Bendamustine",
    "Bortezomib",
    "Carboplatin",
    "Cetuximab",
    "Cisplatin",
    "Cytarabine",
    "Docetaxel",
    "Etoposide",
    "Fludarabine",
    "Fluorouracil (5-FU)",
    "Gemcitabine",
    "Irinotecan",
    "Mesna",
    "Methotrexate",
    "Oxaliplatin",
    "Paclitaxel",
    "Pemetrexed"
]

def generate_manage_rows():
    rows = []
    for i, name in enumerate(drugs, 1):
        code = f"PD-{i:05d}"
        active_class = "bg-blue-600 text-white cursor-pointer hover:bg-blue-700" if i == 7 else "hover:bg-blue-50 cursor-pointer text-gray-800"
        border_class = "border-r border-gray-300"
        rows.append(f'                            <tr class="{active_class}" onclick="selectDrug(this, \'{code}\', \'{name}\')">\n                                <td class="p-1 border-r border-gray-300 pl-2">{code}</td>\n                                <td class="p-1 pl-2">{name}</td>\n                            </tr>')
    return "\n".join(rows)

def generate_receive_rows():
    rows = []
    for i, name in enumerate(drugs, 1):
        code = f"PD-{i:05d}"
        active_class = "bg-blue-600 text-white cursor-pointer" if i == 7 else "hover:bg-blue-50 cursor-pointer"
        border_class = "border-r border-white" if i == 7 else "border-r border-gray-200"
        rows.append(f'                            <tr class="{active_class}" onclick="selectDrugReceive(this, \'{code}\', \'{name}\', \'\', \'500.00\')"><td class="p-1 {border_class}">{code}</td><td class="p-1 {border_class}">{name}</td><td class="p-1 text-right"></td></tr>')
    return "\n".join(rows)

import re

# Update manage.html
with open('/Users/atcharapornn/Desktop/Projest/manage.html', 'r') as f:
    content = f.read()
new_rows = generate_manage_rows()
content = re.sub(r'<tbody id="drug-list-body".*?</tbody>', f'<tbody id="drug-list-body" class="divide-y divide-gray-200">\n{new_rows}\n                        </tbody>', content, flags=re.DOTALL)
with open('/Users/atcharapornn/Desktop/Projest/manage.html', 'w') as f:
    f.write(content)

# Update receive.html
with open('/Users/atcharapornn/Desktop/Projest/receive.html', 'r') as f:
    content = f.read()
new_rows = generate_receive_rows()
content = re.sub(r'<tbody class="divide-y divide-gray-200">.*?</tbody>', f'<tbody class="divide-y divide-gray-200">\n{new_rows}\n                        </tbody>', content, flags=re.DOTALL)
with open('/Users/atcharapornn/Desktop/Projest/receive.html', 'w') as f:
    f.write(content)

print("Medication lists updated in manage.html and receive.html.")
